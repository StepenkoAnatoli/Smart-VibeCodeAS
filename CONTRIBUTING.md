# Contributing

Thanks for helping. This guide exists so people who build with AI, and don't
come from a coding background, can learn what their apps (and their AI tools)
are missing. Every suggestion, correction and question helps.

## The easiest ways to help

- **Found a mistake?** [Report it](../../issues/new?template=report-a-mistake.yml):
  a wrong fact, outdated advice, a broken link, or an explanation that confused
  you. "This confused me" is a real bug in a beginner guide.
- **Know a term or topic that's missing?** [Suggest it](../../issues/new?template=suggest-a-topic.yml).
- **Something went wrong in your vibe-coded app** that isn't covered yet? Tell
  us the story in an issue. Real stories become entries in
  [How vibe-coded apps break](guide/12-how-vibe-coded-apps-break.md).

You don't need to know Git or Markdown for any of these.

## Editing the guide yourself

The chapters are plain Markdown files in [`guide/`](guide/). Small fixes can be
made right on GitHub with the pencil icon, which opens a pull request for you.

### How entries are written

Each term or topic is a heading with a priority label, using an em dash (—):

```markdown
### Rate Limiting — 🔴 Now

**What it is:** One or two plain sentences.

**Picture it:** An everyday comparison.

**What it means for you:** What a beginner should actually do, and why.
```

- **🔴 Now:** learn before launching an app with logins, payments or other
  people's data.
- **🟡 Soon:** once real people use the app, or when the problem shows up.
- **⚪ Later:** big-system topics; know the word, skip the details for now.

Smaller entries can be a single paragraph that ends with a **For you:**
sentence.

### Style

- Write for someone who has never programmed. Explain every technical word the
  first time it appears, or link to where it's explained.
- Short, direct sentences. Active voice. No jargon without a translation.
- Prefer one concrete example to three abstract rules.
- Give the reader something to *do*: a check, a setting, or a prompt to give
  their AI.
- **Facts must be checkable.** For claims about tools, platforms, prices,
  limits or laws, link a primary source (official docs or the law itself) in
  your pull request. If it's likely to change, say so in the text ("check the
  current guidelines").
- **Legal and tax points are questions to look up,** not advice.
- Don't name or shame real people or companies in failure stories; describe the
  pattern.

### Before you open a pull request

Run the two checks, which need only Python 3:

```
python3 scripts/check_guide.py     # links, the 111 reel terms, and the quiz
python3 scripts/build_page.py      # rebuilds site/index.html and docs/index.html
```

Commit the rebuilt pages together with your chapter changes. CI runs the same
checks and fails if the pages are out of date or a link is broken.

### Adding quiz questions

Questions live in [`quiz/questions.json`](quiz/questions.json). Each one names
the chapter `file` and the `heading` it comes from (the heading's text, without
the " — 🔴 Now" label), so the page can link to the explanation. `answer` is the
position of the right option, counting from 0. The check script validates all
of this.

### Adding a chapter

Name it with the next number (`18-something.md`), add a short menu label for
it in `NAV_LABELS` in `scripts/build_page.py`, add it to the reading order in
the README, and link it from the previous chapter's "Next" line.
