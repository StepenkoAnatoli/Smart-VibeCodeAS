#!/usr/bin/env python3
"""Build the one-page, phone-friendly version of the guide.

Usage:
    python3 scripts/build_page.py           # write site/index.html and docs/index.html
    python3 scripts/build_page.py --check   # fail if either is out of date

The page embeds every chapter's Markdown and renders it in the browser, with
search, Now/Soon/Later filters, copy buttons and a quiz. site/index.html is the
page body (for hosts that add the document wrapper, like Claude artifacts);
docs/index.html is a complete page for GitHub Pages. Uses only the standard
library.
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_guide import GLOSSARY, HEADING_FOR, QUIZ, REEL_TERMS, heading_anchor, load_quiz  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
GUIDE = ROOT / "guide"
TEMPLATE = ROOT / "scripts" / "page_template.html"
OUTPUT = ROOT / "site" / "index.html"
PAGES_OUTPUT = ROOT / "docs" / "index.html"

# Base styles the artifact host adds around site/index.html; the standalone page needs them too.
STANDALONE_HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<style>
:root { color-scheme: light; padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px); }
body { margin: 0; font: 14px/1.5 system-ui, -apple-system, "Segoe UI", sans-serif; }
img { max-width: 100%; }
[hidden] { display: none !important; }
</style>
"""
BODY_START = '<div class="wrap" id="top">'
# Chapters whose checkboxes the page remembers, found by name so renumbering can't break them.
CHECKLIST = next(GUIDE.glob("*-checklist-and-ai-prompts.md"))
PRACTICE = next(GUIDE.glob("*-practice-project.md"))

# Short names for the chapter menu, by file-name prefix.
NAV_LABELS = {
    "00": "Start here",
    "01": "Your project",
    "02": "Vibe coding well",
    "03": "Day-one setup",
    "04": "The reel, explained",
    "05": "What you need",
    "06": "Beyond the reel",
    "07": "Your database",
    "08": "Logins",
    "09": "AI features",
    "10": "Testing",
    "11": "Debugging",
    "12": "How apps break",
    "13": "When things go wrong",
    "14": "Rescuing a project",
    "15": "Checklist",
    "16": "Practice project",
    "17": "Working with a developer",
}

LINK_RE = re.compile(r"\]\(([^)\s]+)\)")


def chapter_id(path):
    return "ch" + str(int(path.name[:2]))


def rewrite_links(markdown, this_id, ids_by_file):
    """Point links between chapter files at anchors on the single page."""

    def replace(match):
        target = match.group(1)
        if target.startswith(("http://", "https://", "mailto:")):
            return match.group(0)
        path, _, anchor = target.partition("#")
        name = Path(path).name
        if not path:
            target_id = this_id
        elif name == "README.md":
            return "](#top)"
        elif name in ids_by_file:
            target_id = ids_by_file[name]
        else:
            raise SystemExit(f"build_page: don't know where to point the link '{target}'")
        return f"](#{target_id}-{anchor})" if anchor else f"](#{target_id})"

    return LINK_RE.sub(replace, markdown)


def build():
    files = sorted(GUIDE.glob("[0-9][0-9]-*.md"))
    ids_by_file = {f.name: chapter_id(f) for f in files}
    chapters = []
    for f in files:
        label = NAV_LABELS.get(f.name[:2])
        if label is None:
            raise SystemExit(f"build_page: add a menu label for {f.name} to NAV_LABELS")
        chapters.append({
            "id": ids_by_file[f.name],
            "label": label,
            "md": rewrite_links(f.read_text(), ids_by_file[f.name], ids_by_file),
        })
    numbers = {HEADING_FOR.get(term, term): i + 1 for i, term in enumerate(REEL_TERMS)}
    quiz = []
    if QUIZ.exists():
        for q in load_quiz():
            target = GUIDE / q["file"]
            quiz.append({
                "id": q["id"], "q": q["q"], "options": q["options"], "answer": q["answer"], "why": q["why"],
                "read": f"#{ids_by_file[target.name]}-{heading_anchor(target, q['heading'])}",
            })
    data = json.dumps({
        "chapters": chapters,
        "numbers": numbers,
        "glossary": ids_by_file[GLOSSARY.name],
        "checklist": ids_by_file[CHECKLIST.name],
        "practice": ids_by_file[PRACTICE.name],
        "quiz": quiz,
    }, ensure_ascii=False)
    # Keep the embedded JSON from closing its <script> tag early.
    data = data.replace("</", "<\\/").replace("<!--", "<\\u0021--")
    return (TEMPLATE.read_text()
            .replace("__CHAPTER_COUNT__", str(len(chapters)))
            .replace("__GUIDE_DATA__", data))


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true",
                        help="fail if site/index.html doesn't match the guide")
    args = parser.parse_args()

    page = build()
    # The template's title, meta tags and styles come before the first wrapper; they go in <head>.
    head, body = page.split(BODY_START, 1)
    standalone = f"{STANDALONE_HEAD}{head}</head>\n<body>\n{BODY_START}{body}\n</body>\n</html>\n"
    outputs = {OUTPUT: page, PAGES_OUTPUT: standalone}
    if args.check:
        stale = [path for path, text in outputs.items() if not path.exists() or path.read_text() != text]
        for path in stale:
            print(f"error: {path.relative_to(ROOT)} is out of date. Run: python3 scripts/build_page.py")
        if stale:
            return 1
        print("OK: site/index.html and docs/index.html match the guide.")
        return 0
    for path, text in outputs.items():
        path.parent.mkdir(exist_ok=True)
        path.write_text(text)
        print(f"Wrote {path.relative_to(ROOT)} ({len(text) // 1024} KB).")
    # GitHub Pages: serve the files as they are, without Jekyll processing.
    (PAGES_OUTPUT.parent / ".nojekyll").touch()
    return 0


if __name__ == "__main__":
    sys.exit(main())
