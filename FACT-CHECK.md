# Keeping the guide accurate

This guide names real tools, plans, limits, prices and laws, and those change
fast. In one review, several claims that had been correct a year earlier had
gone out of date: renamed API keys, a recommended library that was no longer
maintained, a framework file that had been renamed. A guide for beginners that
is confidently out of date is worse than no guide, because beginners can't
tell.

So the guide gets an independent fact-check **every three months**. A GitHub
Action opens a reminder issue labeled `fact-check` on the first day of January,
April, July and October (`.github/workflows/quarterly-fact-check.yml`).

## What a fact-check covers

- **Product facts:** names, features, defaults and file names of the tools the
  guide mentions (Supabase, Vercel, Netlify, Stripe, Next.js, GitHub, the AI
  providers and coding tools, and so on).
- **Plan limits and terms:** free-tier limits, what free plans allow, and which
  features need a paid plan.
- **Laws and rules:** GDPR timelines, app store rules, consumer and email rules.
- **Security advice:** anything a beginner would follow that could leave an app
  less secure, lose data or cost money if it's wrong.
- **The quiz:** every marked answer is still right, and no wrong option has
  become right.

Style, wording and "could say more" are out of scope for a fact-check.

## How to run one

1. Split the chapters into three or four groups (for example 00–03, 04–06,
   07–10, 11–17, plus `quiz/questions.json`).
2. For each group, start a **fresh** conversation with an AI that can search the
   web, and give it the prompt below with the file paths. Fresh conversations
   matter: a reviewer that helped write the text tends to agree with it.
3. Check each finding's source yourself before changing anything. Reject
   findings without a source or a clear explanation.
4. Fix the confirmed findings in one pull request, listing each finding and its
   source in the description. Run `python3 scripts/check_guide.py --external`
   and `python3 scripts/build_page.py` before committing.
5. Update the **Last fact-checked** date in the README, and close the issue.

## The reviewer prompt

```
You are an independent technical fact-checker. Today's date is [date].

Review these files for errors: [file paths]

Context: they're part of a beginner guide for "vibe coders", people who build
apps with AI tools and have no coding background. Simplification is
intentional and fine. Legal points are framed as things to look up, not legal
advice. Do not report style preferences, wording taste, or "could add more
detail".

Report ONLY concrete problems:
1. Factual errors: wrong technical, product, legal or platform claims.
2. Outdated claims as of today's date: product features, defaults, names,
   plan limits or rules that changed.
3. Misleading simplifications that would lead a beginner to a wrong or
   dangerous conclusion.
4. Dangerous advice: anything that would make an app less secure, lose data,
   break the law or cost money if followed.
5. Quiz questions whose marked answer (a 0-based index into "options") is
   wrong or ambiguous.
6. Contradictions within or between the files.

Verify anything you're not certain about with web search or official
documentation. Prefer fewer, solid findings over many weak ones. Do NOT edit
any files.

Return findings most serious first, each with: file and line(s), the exact
quoted text, what's wrong (one or two sentences), the corrected text you'd
suggest in the same plain style, and confidence (high/medium) with the source
URL. End with one line: the total number of findings.
```

## Between fact-checks

- Readers can report anything wrong with the
  [Report a mistake](../../issues/new?template=report-a-mistake.yml) form.
- The `Check guide` workflow checks every outside link once a week.
