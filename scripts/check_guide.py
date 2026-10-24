#!/usr/bin/env python3
"""Check the guide for broken links and missing reel terms.

Usage:
    python3 scripts/check_guide.py              # links inside the repo + term coverage
    python3 scripts/check_guide.py --external   # also check http(s) links

Exits non-zero if anything is broken. Uses only the standard library.
"""
import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = [ROOT / "README.md", *sorted((ROOT / "guide").glob("*.md"))]
GLOSSARY = ROOT / "guide" / "03-the-reel-explained.md"
QUIZ = ROOT / "quiz" / "questions.json"

# The 111 terms from the original @nataindata list, in order.
REEL_TERMS = [
    "Rate Limiting", "Caching", "Load Balancing", "Reverse Proxies", "API Gateways",
    "CI/CD", "Docker", "Kubernetes", "Service Discovery", "Circuit Breakers",
    "Timeouts", "Retries", "Exponential Backoff", "Idempotency", "Message Queues",
    "Pub/Sub", "Event-Driven Architecture", "Distributed Transactions", "Saga Pattern",
    "Dead Letter Queues", "Cron Jobs", "WebSockets", "Long Polling", "Server-Sent Events",
    "Database Indexing", "Query Optimization", "N+1 Queries", "Connection Pooling",
    "Read Replicas", "Sharding", "Partitioning", "Replication", "Leader Election",
    "CAP Theorem", "Eventual Consistency", "Optimistic Locking", "Pessimistic Locking",
    "Distributed Locks", "Race Conditions", "Deadlocks", "Memory Leaks",
    "Garbage Collection", "Thread Safety", "Backpressure", "Autoscaling",
    "Horizontal Scaling", "Vertical Scaling", "CDN", "Edge Caching", "Cache Invalidation",
    "Feature Flags", "Blue-Green Deployment", "Canary Releases", "Rolling Deployments",
    "Rollbacks", "Health Checks", "Liveness & Readiness Probes", "Monitoring", "Logging",
    "Distributed Tracing", "Metrics", "Alerts", "SLOs", "SLIs", "Error Budgets",
    "Observability", "Secrets Management", "IAM", "OAuth", "JWT Rotation", "TLS",
    "Encryption at Rest", "Encryption in Transit", "WAF", "DDoS Protection", "CORS",
    "CSRF", "SQL Injection", "XSS", "SSRF", "Database Migrations", "Schema Versioning",
    "Disaster Recovery", "Backups", "Failover", "Multi-Region Deployment",
    "Chaos Engineering", "Cost Optimization", "Cold Starts", "Serverless Limits",
    "Latency", "Throughput", "P99 Latency", "Tail Latency", "Network Partitions",
    "Clock Skew", "DNS", "TCP vs UDP", "HTTP/2 & HTTP/3", "gRPC", "Webhooks",
    "API Versioning", "Semantic Versioning", "Infrastructure as Code", "Terraform",
    "Helm Charts", "Build Caching", "Dependency Hell", "Production Incidents",
    "On-Call", "Postmortems",
]
# Terms whose glossary heading uses a longer name.
HEADING_FOR = {"OAuth": "JWT / OAuth", "TLS": "TLS/SSL"}

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
HEADING_RE = re.compile(r"^(#{1,6}) (.+)$", re.M)
FENCE_RE = re.compile(r"^```.*?^```", re.M | re.S)


def without_code(text):
    """Drop fenced code blocks, so example text inside them isn't checked."""
    return FENCE_RE.sub("", text)


def headings(path):
    """(title, anchor) for every heading, with the anchors GitHub generates."""
    seen = {}
    result = []
    for _, title in HEADING_RE.findall(without_code(path.read_text())):
        slug = re.sub(r"[^\w\- ]", "", title.strip().lower()).replace(" ", "-")
        count = seen.get(slug, 0)
        seen[slug] = count + 1
        result.append((title.strip(), slug if count == 0 else f"{slug}-{count}"))
    return result


def anchors(path):
    """The heading anchors GitHub generates for a Markdown file."""
    return {anchor for _, anchor in headings(path)}


def heading_anchor(path, name):
    """The anchor of the one heading whose name (before any " — " label) is `name`."""
    matches = [anchor for title, anchor in headings(path) if title.split(" — ")[0] == name]
    if len(matches) != 1:
        raise LookupError(f"{len(matches)} headings named '{name}' in {path.name}")
    return matches[0]


def load_quiz():
    return json.loads(QUIZ.read_text())


def check_quiz():
    if not QUIZ.exists():
        return []
    rel = QUIZ.relative_to(ROOT)
    try:
        questions = load_quiz()
    except json.JSONDecodeError as error:
        return [f"{rel}: not valid JSON ({error})"]
    problems, ids = [], set()
    for n, q in enumerate(questions, 1):
        where = f"{rel}: question {n} ({q.get('id', 'no id')})"
        missing = [k for k in ("id", "q", "options", "answer", "why", "file", "heading") if k not in q]
        if missing:
            problems.append(f"{where}: missing {', '.join(missing)}")
            continue
        if q["id"] in ids:
            problems.append(f"{where}: duplicate id")
        ids.add(q["id"])
        if not 2 <= len(q["options"]) <= 5 or len(set(q["options"])) != len(q["options"]):
            problems.append(f"{where}: needs 2-5 different options")
        if not isinstance(q["answer"], int) or not 0 <= q["answer"] < len(q["options"]):
            problems.append(f"{where}: answer must be the index of one of the options")
        target = ROOT / "guide" / q["file"]
        if not target.exists():
            problems.append(f"{where}: no chapter {q['file']}")
            continue
        try:
            heading_anchor(target, q["heading"])
        except LookupError as error:
            problems.append(f"{where}: {error}")
    return problems


def check_internal_links():
    problems = []
    for doc in DOCS:
        for link in LINK_RE.findall(without_code(doc.read_text())):
            if link.startswith(("http://", "https://", "mailto:")):
                continue
            target_part, _, anchor = link.partition("#")
            target = (doc.parent / target_part).resolve() if target_part else doc
            rel = doc.relative_to(ROOT)
            if not target.exists():
                problems.append(f"{rel}: link to missing file {link}")
            elif anchor and target.suffix == ".md" and anchor not in anchors(target):
                problems.append(f"{rel}: link to missing heading {link}")
    return problems


def check_reel_terms():
    text = without_code(GLOSSARY.read_text())
    names = [re.split(r" — ", h)[0] for h in re.findall(r"^### (.+)$", text, re.M)]
    problems = []
    for term in REEL_TERMS:
        heading = HEADING_FOR.get(term, term)
        if not any(n == heading or n.startswith(heading + " (") for n in names):
            problems.append(f"{GLOSSARY.relative_to(ROOT)}: no entry for reel term '{term}'")
    for name in sorted({n for n in names if names.count(n) > 1}):
        problems.append(f"{GLOSSARY.relative_to(ROOT)}: duplicate entry '{name}'")
    return problems


def fetch_status(url):
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (guide link check)"})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return response.status
    except urllib.error.HTTPError as error:
        return error.code


def check_external_links():
    urls = sorted({link for doc in DOCS for link in LINK_RE.findall(without_code(doc.read_text()))
                   if link.startswith(("http://", "https://"))})
    problems, warnings = [], []
    for url in urls:
        status, error = None, None
        for attempt in range(3):
            try:
                status = fetch_status(url)
                if status < 500:
                    break
            except (urllib.error.URLError, TimeoutError, OSError) as exc:
                error = exc
            time.sleep(2 ** attempt)
        if status is not None and status < 400:
            continue
        if status in (403, 429):
            # Some sites block automated requests; worth a look, not a failure.
            warnings.append(f"{url}: HTTP {status} (may be blocking bots)")
        else:
            problems.append(f"{url}: {f'HTTP {status}' if status else error}")
    return problems, warnings


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--external", action="store_true", help="also check http(s) links")
    args = parser.parse_args()

    problems = check_internal_links() + check_reel_terms() + check_quiz()
    warnings = []
    if args.external:
        external_problems, warnings = check_external_links()
        problems += external_problems

    for warning in warnings:
        print(f"warning: {warning}")
    for problem in problems:
        print(f"error: {problem}")
    if problems:
        print(f"\n{len(problems)} problem(s) found.")
        return 1
    quiz = f", {len(load_quiz())} quiz questions valid" if QUIZ.exists() else ""
    print(f"OK: {len(DOCS)} files checked, all {len(REEL_TERMS)} reel terms covered{quiz}"
          + (", external links reachable." if args.external else "."))
    return 0


if __name__ == "__main__":
    sys.exit(main())
