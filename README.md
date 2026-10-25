# Missing Knowledge for Vibe Coders

Basically: teaching vibe coders who build with ChatGPT, Claude, Cursor, Lovable
and so on what they might be missing, and what their AI might be missing for
them.

It started with a viral post by @nataindata: *"Who's gonna tell vibe coders
about..."*, followed by a list of 111 engineering terms. This repo explains
every one of them in plain English, assuming zero coding knowledge, then sorts
them into what you need now, what you need soon, and what you can safely ignore
for a long time.

## Read in this order

**The basics**

1. **[Start here](guide/00-start-here.md)**: how an app actually works, using a
   restaurant as the picture. Five minutes, and it makes everything else make
   sense.
2. **[Reading your project](guide/01-reading-your-project.md)**: the files,
   terminal commands, Git words and code words you see every day, explained.
3. **[Vibe coding well](guide/02-vibe-coding-well.md)**: how to work with AI
   tools: specs, plans, small steps, checkpoints, what the AI can and can't
   see, rules files, and checking its work without reading every line.
4. **[Starting a project safely](guide/03-starting-a-project-safely.md)**: the
   day-one setup that makes most safety items automatic: a sensible stack,
   accounts, the repo, separate development and production, and safe defaults.

**The reel, and what it left out**

5. **[The reel, explained](guide/04-the-reel-explained.md)**: every term from
   the reel, each with a plain explanation, an everyday picture, and what it
   means for you.
6. **[What you actually need](guide/05-what-you-actually-need.md)**: the honest
   triage, what your AI tends to miss, and a learning path.
7. **[Beyond the reel](guide/06-beyond-the-reel.md)**: what the reel left out
   about launching and running an app: securing AI features, taking payments,
   legal basics, testing, launch day, notifications, maintenance after launch,
   and what changes if you sell to teams or ship a mobile app.

**Building it right**

8. **[Your database, explained](guide/07-your-database.md)**: tables and how
   they connect, storing money and time correctly, constraints, deleting,
   search, and changing live data safely.
9. **[Logins, done right](guide/08-logins-done-right.md)**: what your auth
   provider doesn't handle for you: trusting the right user ID, roles,
   redirects, email changes, sessions and two-factor login.
10. **[Building AI features](guide/09-building-ai-features.md)**: tokens and
    cost, choosing models, prompts in your app, structured output, streaming,
    memory, answering from your own data (RAG), tools and agents, outages, and
    testing AI output.
11. **[Testing, for people who don't code](guide/10-testing-for-non-coders.md)**:
    what tests are, which ones matter, reading results, running them on every
    change, and the traps when the AI writes them.

**When it breaks**

12. **[Debugging with AI](guide/11-debugging-with-ai.md)**: how to read an
    error, find where it really happened, give your AI the right clues, and
    escape the loop where every "fix" brings a new error.
13. **[How vibe-coded apps break](guide/12-how-vibe-coded-apps-break.md)**: 19
    common disaster stories, why the AI wrote the code that caused each one,
    and how to prevent it.
14. **[When things go wrong](guide/13-when-things-go-wrong.md)**: an incident
    playbook for leaked keys, exploding bills, data exposure, outages, lost
    data and taken-over accounts, plus how to tell users.
15. **[Rescuing a messy AI-built project](guide/14-rescuing-a-messy-project.md)**:
    getting back in control of an app nobody understands anymore, step by step.

**Before you launch**

16. **[Checklist and AI prompts](guide/15-checklist-and-ai-prompts.md)**: a
    pre-launch checklist and copy-paste prompts that make your AI check these
    things for you.

**Put it into practice**

17. **[Practice project](guide/16-practice-project.md)**: build a small private
    notes app in 13 steps, with a prompt and a "check it yourself" list for
    each, including trying to break in, payments in test mode, and fire drills.
18. **[Working with a developer](guide/17-working-with-a-developer.md)**: when
    to bring in a person, giving access safely, briefing, code reviews,
    quotes and agreements, and offboarding.

## Read it on your phone, and test yourself

The whole guide is also one phone-friendly page, with search, Now/Soon/Later
filters, copy buttons on every prompt, a checklist that remembers your ticks,
and a **quiz** on the essentials (58 questions, each linked to its
explanation).

- `docs/index.html` is that page as a website. To publish it for free with
  GitHub Pages, go to the repo's **Settings → Pages**, choose **Deploy from a
  branch**, pick `main` and the `/docs` folder, and save. GitHub shows the
  address after a minute or two, and the site updates on every merge.
- `site/index.html` is the same page without the outer HTML wrapper, for hosts
  that add their own.

Both are built from the chapters and `quiz/questions.json` by
`scripts/build_page.py`.

## The 30-second version

- **About 12 of the terms matter before you launch.** Nearly all of them come
  down to four things: don't leak your keys, don't let users see each other's
  data, don't get a surprise bill, and don't lose your data.
- **About 25 more matter once real people use your app.**
- **The rest are big-company problems.** Know what the word means, and learn it
  properly when it becomes your problem.

## The labels used in the guide

- 🔴 **Now**: before you put an app with logins, payments or other people's data
  online
- 🟡 **Soon**: once real people use it, or when you hit the problem
- ⚪ **Later**: know the word; skip the details for now

## Keeping it accurate

**Last fact-checked: October 2026.** Every chapter and the quiz were reviewed
by independent AI fact-checkers working from official sources, and every
confirmed finding was fixed. The process is in [FACT-CHECK.md](FACT-CHECK.md),
and a GitHub Action opens a reminder issue every three months to run it again.

A GitHub Action (`.github/workflows/check-guide.yml`) runs on every change. It
fails if a link between pages breaks, if any of the 111 reel terms loses its
entry, if a quiz question is broken, or if the built pages are out of date.
Once a week it also checks that outside links still load. To run it yourself:

```
python3 scripts/check_guide.py              # links, reel terms and quiz
python3 scripts/check_guide.py --external   # also check outside links
python3 scripts/build_page.py               # rebuild the pages after editing a chapter
```

Rebuild the pages in the same change as any chapter edit.

## Contributing

Found a mistake, or know something vibe coders are missing? See
[CONTRIBUTING.md](CONTRIBUTING.md). Reporting a confusing explanation counts.
