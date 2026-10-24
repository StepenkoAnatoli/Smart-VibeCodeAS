#!/usr/bin/env python3
"""Build the one-page, phone-friendly version of the guide.

Usage:
    python3 scripts/build_page.py           # write site/index.html
    python3 scripts/build_page.py --check   # fail if site/index.html is out of date

The page embeds every chapter's Markdown and renders it in the browser, with
search, Now/Soon/Later filters and copy buttons. Uses only the standard library.
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_guide import GLOSSARY, HEADING_FOR, REEL_TERMS  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
GUIDE = ROOT / "guide"
TEMPLATE = ROOT / "scripts" / "page_template.html"
OUTPUT = ROOT / "site" / "index.html"
CHECKLIST = GUIDE / "09-checklist-and-ai-prompts.md"

# Short names for the chapter menu, by file-name prefix.
NAV_LABELS = {
    "00": "Start here",
    "01": "Your project",
    "02": "Vibe coding well",
    "03": "The reel, explained",
    "04": "What you need",
    "05": "Beyond the reel",
    "06": "Your database",
    "07": "Debugging",
    "08": "How apps break",
    "09": "Checklist",
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
    data = json.dumps({
        "chapters": chapters,
        "numbers": numbers,
        "glossary": ids_by_file[GLOSSARY.name],
        "checklist": ids_by_file[CHECKLIST.name],
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
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text() != page:
            print("error: site/index.html is out of date. Run: python3 scripts/build_page.py")
            return 1
        print("OK: site/index.html matches the guide.")
        return 0
    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(page)
    print(f"Wrote {OUTPUT.relative_to(ROOT)} ({len(page) // 1024} KB).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
