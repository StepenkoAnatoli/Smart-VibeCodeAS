# Debugging with AI: how to get unstuck

The moment vibe coding usually breaks down isn't writing the first version.
It's the bug the AI can't fix, where every "fixed it!" brings a new error and
the code grows while the problem stays.

You don't need to read code to get out of that loop. You need to collect the
right clues, hand them to the AI in the right shape, and know when to stop and
undo.

## Contents

1. [What a bug actually is](#1-what-a-bug-actually-is)
2. [Reading an error message](#2-reading-an-error-message)
3. [Where errors hide](#3-where-errors-hide)
4. [Reproduce it before you fix it](#4-reproduce-it-before-you-fix-it)
5. [Shrink the problem](#5-shrink-the-problem)
6. ["Works on my machine, broken in production"](#6-works-on-my-machine-broken-in-production)
7. [Giving your AI the right context](#7-giving-your-ai-the-right-context)
8. [The AI loop, and how to escape it](#8-the-ai-loop-and-how-to-escape-it)
9. [Fixes that aren't fixes](#9-fixes-that-arent-fixes)
10. [After the fix](#10-after-the-fix)
11. [Copy-paste debugging prompts](#11-copy-paste-debugging-prompts)

---

## 1. What a bug actually is

A bug is a difference between **what you expected** and **what happened**.
Most failed debugging starts with a vague description ("login is broken"). Good
debugging starts with a precise one:

> I click "Log in" with a correct email and password. I expect to land on
> /dashboard. Instead the button spins for about 10 seconds and the page shows
> "Something went wrong". It happens on the live site, not on my laptop, and
> started after yesterday's deploy.

That one paragraph already rules out half the possible causes. Write it down
before you ask the AI anything.

---

## 2. Reading an error message

Error messages look scary, but they have the same parts every time:

```
TypeError: Cannot read properties of undefined (reading 'email')
    at ProfileCard (src/components/ProfileCard.tsx:14:22)
    at renderWithHooks (node_modules/react-dom/...)
    ...
```

- **The type** (`TypeError`): the kind of problem.
- **The message** (`Cannot read properties of undefined (reading 'email')`):
  what went wrong, in words. Here the code tried to read `.email` from
  something that doesn't exist yet, usually data that hasn't loaded or a user
  who isn't logged in.
- **The location** (`ProfileCard.tsx:14:22`): the file, line 14, character 22.
- **The stack trace**: the chain of calls that led there. Read it from the top
  and stop at the **first line that's in your own code** (`src/...`), not in
  `node_modules`. That's usually where to look.

### Common errors, translated

| You see | It usually means |
|---|---|
| `Cannot read properties of undefined` / `null` | Code used data that wasn't there yet: still loading, not logged in, or a typo in a field name |
| `X is not a function` / `X is not defined` | A typo, a missing import, or code written for a different library version |
| `Module not found` / `Cannot find module` | A package isn't installed, or an import path is wrong. File names are case-sensitive on servers |
| `Hydration failed` / `hydration mismatch` (React, Next.js) | The page rendered differently on the server and in the browser, often because of dates, random numbers or `window` |
| `blocked by CORS policy` | Your frontend called an API at a different address that hasn't allowed it. See *CORS* |
| `ECONNREFUSED` / `fetch failed` | Nothing answered at that address: the server is down, or the URL or port is wrong |
| `relation "x" does not exist` | The database table doesn't exist *in this database*. A migration didn't run |
| `permission denied` / `new row violates row-level security policy` | Your database rules blocked it, often correctly. Don't just turn the rules off |
| `Invalid API key` / `401` from an outside service | The key is missing, wrong, or not set in this environment |
| `429 Too Many Requests` | You hit a rate limit. Slow down and retry with backoff |
| `Task timed out` / `FUNCTION_INVOCATION_TIMEOUT` | Your function ran longer than the host allows. See *Serverless Limits* |
| `out of memory` / `heap limit` | Something loaded too much data at once, or there's a memory leak |

### HTTP status codes

Every request in the Network tab (next section) has a status code. The first
digit tells you whose problem it is:

| Code | Meaning | Whose problem |
|---|---|---|
| **2xx** (200, 201) | Worked | Nobody's |
| **3xx** (301, 302) | Redirected somewhere else | Usually fine; watch for redirect loops |
| **400** | The request was malformed | The frontend sent bad data |
| **401** | Not logged in, or the login token is invalid or expired | Authentication |
| **403** | Logged in, but not allowed | Permissions (often working correctly) |
| **404** | Nothing at that address | Wrong URL, or the route doesn't exist on this deploy |
| **409 / 422** | Conflict, or data failed validation | The data, not the code |
| **429** | Too many requests | Rate limit |
| **500** | The server crashed while handling it | Backend. Check the server logs |
| **502 / 503 / 504** | The server is down, overloaded or too slow | Hosting, timeouts or an outside service |

---

## 3. Where errors hide

The message a user sees ("Something went wrong") is almost never the real
error. The real one is in one of three places.

### The browser's developer tools

Open them with **F12**, or **Ctrl+Shift+I** on Windows/Linux, or
**Cmd+Option+I** on Mac. (On a phone it's much harder, so reproduce on a
computer if you can.)

- **Console tab:** errors from the frontend code, in red. Copy the *whole*
  text, not a screenshot.
- **Network tab:** every request the page made. Reload the page with this tab
  open, then click any request shown in red. Check its **Status** (see the
  table above), then its **Response** tab, which often contains the real error
  message from the server.

### Your server logs

Errors from backend code (API routes, server functions) appear in your
**host's logs**, not in the browser: on Vercel it's the project's *Logs* tab,
and Netlify, Render, Railway and Supabase each have a logs page. Your error
tracker (Sentry, for example) collects them with more detail.

### Outside services

Payment, email and AI providers have their own dashboards with request logs.
Stripe, for example, shows every webhook it sent and what your server answered.

> A **500 in the Network tab** means "go look at the server logs". The browser
> only knows the server failed; the server log knows why.

---

## 4. Reproduce it before you fix it

A bug you can't trigger on purpose is a bug you can't prove you fixed. Before
asking for a fix, find out:

- **The exact steps:** what you clicked, in what order, with what data.
- **Does it happen every time?** If only sometimes, it may be timing (a race
  condition), a specific user's data, or caching.
- **Where?** Live site only, or locally too? One browser or all? Phone or
  computer?
- **Who?** Every user, or one account? Logged in or out? Admin or regular?
- **Since when?** What changed around then: a deploy, a new package, a changed
  setting, an outside service's outage?

If you can't reproduce it, ask the AI to **add logging** around the suspect
area (what came in, what was found, what decision was made). Then wait for it
to happen again, and read the logs.

---

## 5. Shrink the problem

### Ask: what changed?

Most bugs arrive with a change. Git knows exactly what changed:

- Look at the most recent commits and their diffs on GitHub, or ask the AI
  "show me what changed in the last 3 commits".
- On Vercel and Netlify, every deploy is listed. If the previous deploy works,
  the bug is in the difference between the two.

### Find the last version that worked

If you don't know when it broke, check out older commits until you find the
last good one. Git can do this half-automatically with `git bisect`; ask the
AI to walk you through it. Once you know the commit that broke it, the AI has
a tiny diff to look at instead of your whole project.

### Cut it down

Remove things until the bug disappears, then add them back one at a time.
Does it break with every user or one? With all the data, or one record? With
the AI call switched off? Every "no" narrows it down.

---

## 6. "Works on my machine, broken in production"

This is the most common vibe-coder bug. Check these, in this order:

1. **Environment variables.** Is every variable from your `.env` also set in
   your host's settings, with the production values, for the production
   environment? Many hosts (Vercel among them) only apply changed variables on
   the **next deploy**, so redeploy after changing them.
2. **The database.** Production uses a different database. Did the migrations
   run there? Does it have the tables, columns and data your code expects?
3. **Case-sensitive file names.** Mac and Windows treat `Button.tsx` and
   `button.tsx` as the same file; Linux servers don't. An import that works
   locally fails in the build.
4. **Build mode vs dev mode.** The production build is stricter and optimized.
   Run the production build locally (often `npm run build` then
   `npm run start`) to see the same errors.
5. **Limits.** Function timeouts, memory, request size, and free-tier quotas
   exist in production but not on your laptop.
6. **Addresses.** Hardcoded `localhost` URLs, callback URLs registered with
   your auth provider or Stripe that point at your laptop, or CORS settings
   that only allow `localhost`.
7. **Caching.** A CDN or browser may be serving an old version. Try a private
   window, or a hard reload (Ctrl+Shift+R, or Cmd+Shift+R).

---

## 7. Giving your AI the right context

The AI only knows what you tell it. A bad bug report gets a guess; a good one
gets a diagnosis. Use this shape:

```
What I did:      [exact steps]
What I expected: [what should have happened]
What happened:   [what actually happened]
Error text:      [full text from the Console, Network response, or server
                  logs: pasted as text, not a screenshot]
Where:           [live site / local, browser, which user]
Since when:      [what changed around then]
Already tried:   [what you or the AI already tried, and what happened]
```

And ask for a **diagnosis before a fix**:

```
Don't change any code yet. List the 3 most likely causes, and for each one,
tell me how to confirm or rule it out (what to log, what to check). Then we'll
fix the confirmed cause only.
```

This one habit prevents most loops. The AI stops guessing, and you both work
from evidence.

---

## 8. The AI loop, and how to escape it

### Signs you're in one

- The same error keeps coming back, or a fix you already tried reappears.
- Each attempt adds more code, but the problem stays.
- The error changes but never goes away.
- The AI starts removing checks, adding `try/catch` everywhere, or saying "now
  it should definitely work".
- You've lost track of what it changed.

### How to get out

1. **Stop after three failed attempts at the same bug.** More attempts in the
   same conversation usually make it worse.
2. **Undo.** Go back to the last commit where things worked
   (`git restore .` throws away uncommitted changes; ask the AI to help if
   you need to go back further). Every loop leaves broken code behind.
3. **Start a fresh conversation.** Long chats fill up with wrong guesses the AI
   keeps building on. Paste in a short summary using the template from
   section 7, including what didn't work.
4. **Ask it to explain before it fixes:** "Explain what this code does, line
   by line, and where the data comes from." Misunderstandings show up fast.
5. **Get evidence.** Ask for logging at each step, run it, paste the output.
6. **Take a smaller step.** Instead of "make checkout work", try "make the
   checkout button call the API and log the response".
7. **Look outside the AI.** Search the exact error message (in quotes), read
   the library's official docs for *your* version, and check the library's
   GitHub issues. The AI's knowledge may be out of date.
8. **Try a different model or tool.** A fresh perspective sometimes spots it
   immediately.

**Commit every time something works.** Then a loop costs you minutes, not a
day.

---

## 9. Fixes that aren't fixes

These make the error *disappear* without fixing the bug. When your AI proposes
one, ask why:

- Wrapping code in `try/catch` and ignoring the error
- Deleting or disabling the check that failed: a validation, a permission
  check, a Row Level Security policy, a test
- Hardcoding a value so it works "for now"
- `// @ts-ignore`, `as any` or `eslint-disable` to silence a warning
- Raising a timeout again and again instead of finding out why it's slow
- Retrying in a loop until it happens to succeed
- "Clearing the cache fixed it", without knowing what was cached or why
- Changing the test so it passes, instead of fixing the code it caught

A real fix explains **why** the bug happened, and the explanation matches the
evidence.

---

## 10. After the fix

1. **Confirm it where it failed.** If it broke on the live site, check the live
   site, with the same steps and the same user.
2. **Add a test** that fails without the fix and passes with it, so the bug
   can't quietly come back.
3. **Ask where else it lives:** "Is this same mistake anywhere else in the
   project?" Bugs come in families.
4. **Write two lines in `INCIDENTS.md`:** what broke and why. That's how this
   whole guide becomes something you actually know.

---

## 11. Copy-paste debugging prompts

### Diagnose before fixing

```
Here's a bug report:
[paste the template from section 7]

Don't change code yet. List the 3 most likely causes, ranked, and for each
one tell me exactly how to confirm or rule it out. If you need more
information (logs, a file, a network response), ask for it.
```

### Add logging to find out

```
I can't tell where this is failing. Add temporary logging at each step of
[feature]: what input arrived, what was read from the database or API, and
which branch the code took. Mark every log line with [DEBUG] so we can remove
them afterwards. Don't change any behavior.
```

### Explain an error message

```
Explain this error message to me in plain English: what it means, which line
of MY code (not library code) it points to, and the 2–3 most common causes.

[paste the full error text]
```

### Works locally, broken in production

```
This works locally but fails in production with this error:
[paste error]
Go through the usual causes one by one: missing or different environment
variables, migrations not run on the production database, case-sensitive
file names, build vs dev mode differences, serverless limits, hardcoded
localhost URLs and callback URLs, and caching. For each, tell me how to check
it on my host.
```

### Break the loop

```
We've tried to fix this several times and it isn't working. Stop proposing
fixes. Summarize: what the bug is, every fix we tried and why each one
failed, and what we actually know for certain. Then suggest a different way
to investigate.
```

### Review a proposed fix

```
Before I accept this fix, explain: what caused the bug, why this change fixes
that cause, and whether it removes or weakens any check (validation,
permissions, Row Level Security, tests, error handling). Is this hiding the
symptom or fixing the cause?
```

---

Next: [Pre-launch checklist and copy-paste AI prompts](05-checklist-and-ai-prompts.md)
