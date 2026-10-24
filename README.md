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

1. **[Start here](guide/00-start-here.md)**: how an app actually works, using a
   restaurant as the picture. Five minutes, and it makes everything else make
   sense.
2. **[The reel, explained](guide/01-the-reel-explained.md)**: every term from
   the reel, each with a plain explanation, an everyday picture, and what it
   means for you.
3. **[What you actually need](guide/02-what-you-actually-need.md)**: the honest
   triage, what your AI tends to miss, and a learning path.
4. **[Beyond the reel](guide/03-beyond-the-reel.md)**: what the reel left out
   about launching and running an app: securing AI features, taking payments,
   legal basics, testing, launch day, maintenance after launch, and what
   changes if you sell to teams or ship a mobile app.
5. **[Debugging with AI](guide/04-debugging-with-ai.md)**: how to read an error,
   find where it really happened, give your AI the right clues, and escape the
   loop where every "fix" brings a new error.
6. **[Checklist and AI prompts](guide/05-checklist-and-ai-prompts.md)**: a
   pre-launch checklist and copy-paste prompts that make your AI check these
   things for you.

## Read it on your phone

`site/index.html` is the whole guide on one page, with search, Now/Soon/Later
filters, copy buttons on every prompt, and a checklist that remembers your
ticks. It's built from the chapters by `scripts/build_page.py`.

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

A GitHub Action (`.github/workflows/check-guide.yml`) runs
`scripts/check_guide.py` on every change. It fails if a link between pages
breaks or if any of the 111 reel terms loses its entry. Once a week it also
checks that outside links still load. To run it yourself:

```
python3 scripts/check_guide.py              # links inside the repo + term coverage
python3 scripts/check_guide.py --external   # also check outside links
python3 scripts/build_page.py               # rebuild site/index.html after editing a chapter
```

The check also fails if `site/index.html` is out of date, so rebuild it in the
same change as any chapter edit.
