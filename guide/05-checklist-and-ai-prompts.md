# Pre-launch checklist and copy-paste AI prompts

You don't need to know how to fix everything yourself. You need to know what to
check, and how to ask your AI to check it properly.

## Pre-launch checklist

Copy this into a GitHub issue or a note and tick items off. If you can't tell
whether an item is done, use the matching prompt further down.

**Secrets**

- [ ] No API keys or passwords written in the code; all of them are in
      environment variables
- [ ] `.env` is listed in `.gitignore`
- [ ] No secret keys in frontend code or in variables starting with
      `NEXT_PUBLIC_`, `VITE_`, `REACT_APP_` or `EXPO_PUBLIC_`
- [ ] Any key that was ever committed to Git has been replaced at the provider
- [ ] GitHub secret scanning is turned on for the repo

**Logins and access**

- [ ] Login uses an auth provider, not homemade password storage
- [ ] Every API route that reads or changes data checks **who** the user is
      **and** that they own that data
- [ ] Supabase: Row Level Security is on for every table, with policies.
      Firebase: Security Rules are not in test mode
- [ ] Tested by hand: logged in as user A, tried to read and change user B's
      data, and it was blocked
- [ ] Admin pages are protected on the server, not just hidden from the menu

**Input**

- [ ] The server validates every input (for example with Zod or Pydantic)
- [ ] No SQL built by gluing strings together with user input
- [ ] No user-written HTML shown raw (`dangerouslySetInnerHTML`, `v-html`,
      `innerHTML`) without a sanitizer
- [ ] File uploads have size and type limits

**AI features** (if your app calls an AI model)

- [ ] Permissions are checked in code, never only by instructions in the prompt
- [ ] Risky actions the AI can trigger (sending, deleting, paying) need the
      user to confirm
- [ ] No secrets in the system prompt
- [ ] AI output is shown as text or sanitized Markdown, never raw HTML, and is
      never run as code or SQL
- [ ] Every user has an AI quota, and every call sets `max_tokens`
- [ ] The model version is pinned in a config setting

**Money**

- [ ] Billing alerts and spending caps on every provider (hosting, database, AI
      APIs, email/SMS)
- [ ] Rate limits on login, signup, password reset, and every endpoint that
      calls a paid API
- [ ] Payment status comes from verified webhooks, not from the browser
- [ ] Webhook handlers check the signature and ignore duplicates
- [ ] The full payment flow was tested in test mode (success, declined card,
      cancel, refund, renewal), and production uses live keys
- [ ] You know how sales tax / VAT applies to what you sell

**Data**

- [ ] Automatic backups are on, and you have restored one as a test
- [ ] Development and production use separate databases and separate keys
- [ ] AI agents have no direct access to the production database or production
      secrets
- [ ] Every migration is read for `DROP`, `DELETE` and `TRUNCATE` before it
      runs on production

**Quality**

- [ ] Sign-up, email verification, login and password reset tested end to end
      with a real email address
- [ ] Automated end-to-end tests cover the money paths (sign-up, login, core
      feature, payment)
- [ ] Every screen has error, empty and loading states; no raw error messages
      shown to users
- [ ] Lists are paginated; no query loads every row
- [ ] Tested on a real phone, including Safari on iPhone
- [ ] Lighthouse run for accessibility and speed

**Running it**

- [ ] HTTPS everywhere
- [ ] Security headers checked with a free scanner (for example Mozilla's HTTP
      Observatory)
- [ ] Error tracking installed (for example Sentry)
- [ ] An uptime monitor watches the site
- [ ] You know where the rollback button is for a bad deploy
- [ ] Logged-in pages are not cached by a CDN (`Cache-Control: private` or
      `no-store`)
- [ ] Scheduled (cron) jobs can't be triggered by strangers, and you'd notice
      if one stopped running
- [ ] Logs never contain passwords, tokens or card numbers
- [ ] 2FA on GitHub, hosting, the domain registrar, the cloud account and AI
      providers, with recovery codes saved
- [ ] Every account is in your name, and the domain is set to auto-renew
- [ ] You know the free-tier limits of every service, and what happens when
      you hit them
- [ ] The lockfile is committed, and every dependency is a real, widely used
      package

**People**

- [ ] If you collect personal data, you've looked up the privacy rules where
      your users live (for example GDPR in the EU), and users can delete their
      account
- [ ] A privacy policy that lists every service receiving user data (including
      AI providers and analytics), plus terms of service
- [ ] Cookie consent, if you use non-essential cookies for EU or UK users
- [ ] A way for users to reach you (support email or feedback button)
- [ ] A README that says how to run, deploy and find every account the app
      uses

---

## Copy-paste prompts for your AI

Paste these into Claude, ChatGPT, Cursor or whatever you build with, with your
project open. They work best one at a time.

### 1. Understand your own app

```
Explain this project to me as if I've never programmed. Draw a simple diagram
of what runs in the browser, what runs on the server, where data is stored,
and which outside services we call. For each part, tell me what is public
(anyone can see it) and what is private.
```

### 2. Secrets audit

```
Audit this project for exposed secrets. Find: hardcoded API keys, passwords or
tokens; secrets in frontend code or in env vars starting with NEXT_PUBLIC_,
VITE_, REACT_APP_ or EXPO_PUBLIC_; whether .env is in .gitignore; and give me
the git command to check whether a secret was ever committed in the history.
List each finding with file and line and how to fix it. Don't change anything
yet.
```

### 3. Access control audit (the most important one)

```
For every API route, server action and database query in this project, tell
me: (1) does it check the user is logged in? (2) does it check the user is
allowed to access THIS specific record, not just any record? Make a table:
route | logged-in check | ownership check | risk. Then show me exactly how a
logged-in user could read or change another user's data, if they can. If we
use Supabase or Firebase, list every table or collection and whether Row Level
Security or Security Rules protect it.
```

### 4. Security review with an attacker's mindset

```
Act as an attacker trying to break this app. Look specifically for: SQL
injection, XSS, CSRF, SSRF, broken access control, missing input validation,
missing rate limits, unsafe file uploads and exposed secrets. For each real
issue, show the exact request I would send to exploit it, the file and line,
how severe it is, and the smallest fix. Don't report theoretical issues you
can't point to in the code.
```

### 5. Cost and abuse review

```
Find every place this app spends money: AI API calls, emails or SMS, storage,
database, serverless functions. For each one: could an anonymous user or a bot
trigger it over and over? Is there a rate limit? Could a bug make it loop?
Estimate the worst-case cost per day if it were abused, and suggest rate
limits and spending caps.
```

### 6. Database health

```
Review the database code for: N+1 queries (database calls inside loops),
missing indexes on columns we filter or sort by, multi-step changes that
should be wrapped in a transaction, and migrations that could delete data.
Show each problem and the fix.
```

### 7. Outside services and reliability

```
For every call to an outside service (AI API, payments, email, other APIs):
Is there a timeout? What does the user see if it fails or is slow? Are retries
safe to repeat (idempotent)? Is there exponential backoff for 429 and 5xx
errors? Are webhooks signature-checked and protected against duplicates?
```

### 8. Production readiness

```
I'm about to launch this to real users. Go through this checklist and tell me
what's done, what's missing, and what's risky, ordered by how badly each
missing item could hurt me. Keep the fixes minimal.

[paste the checklist from above]
```

### 9. The guard: paste this whenever your AI proposes a fix

```
Before applying this fix: does it remove or weaken any safety check (login or
permission checks, Row Level Security or Security Rules, CORS, input
validation, rate limits, HTTPS)? If yes, explain why that's safe, or find a
fix that keeps the check.
```

### 10. Learn a term

```
Explain [term] using my own project as the example. What is it, does my app
need it right now, and what is the smallest change that would handle it?
Then quiz me with 3 questions.
```

### 11. AI feature security (if your app calls an AI model)

```
Review every place this app sends text to an AI model. For each one: could a
user, or a web page, email or document the AI reads, contain instructions
that change what the AI does (prompt injection)? What tools, data or actions
can the AI reach, and are permissions checked in code rather than in the
prompt? Is AI output ever shown as raw HTML, or run as code or SQL? Are there
secrets in the system prompt? Is there a per-user quota and max_tokens on
every call? Show the worst realistic attack and the smallest fixes.
```

### 12. Tests for the money paths

```
Write end-to-end tests (Playwright) for the paths this app can't afford to
break: sign up, log in, password reset, the core feature, and payment in test
mode. Then show me each test failing when I break the feature on purpose, so I
know the tests actually check something. Don't change app code to make tests
pass without telling me.
```

### 13. Launch day readiness

```
List every outside service this app uses (hosting, database, auth, storage,
email, AI, payments, analytics). For each: which plan am I on, what are its
limits (requests, storage, emails, bandwidth, rate limits), what happens when
I hit one, and does a free project pause when inactive? If 1,000 people
signed up in one hour, what would break first?
```

### 14. Privacy data map

```
Make a table of every piece of personal data this app collects (emails, names,
IPs, uploads, chat messages, payment info): where it's stored, which outside
services receive it (including AI providers, analytics and logs), how long we
keep it, and how a user can export or delete it. I'll use this to write my
privacy policy.
```

---

## Red flags: stop and ask why

If you see your AI do any of these, pause and use prompt 9 above. If it's
doing them while stuck on a bug, see [Debugging with AI](04-debugging-with-ai.md#8-the-ai-loop-and-how-to-escape-it).

- Turns off Row Level Security, or sets Firebase rules to
  `allow read, write: if true`
- Changes CORS to allow every website just to make an error go away (fine for a
  truly public API, risky for anything with logins)
- Comments out a login or permission check "for testing"
- Relies on the AI prompt to protect data ("only show the user their own
  records") instead of checking in code
- Changes a test so it passes, instead of fixing the bug it caught
- Puts a secret key in a frontend file or in a `NEXT_PUBLIC_` / `VITE_` /
  `REACT_APP_` / `EXPO_PUBLIC_` variable
- Builds SQL by gluing strings: `"... WHERE id = " + id`, or `${id}` inside a
  raw SQL string
- Uses `dangerouslySetInnerHTML`, `v-html`, `innerHTML` or `eval(` with data a
  user could control
- Writes `catch (e) {}`, swallowing an error so it silently disappears
- Disables certificate checks: `verify=False`, `rejectUnauthorized: false`
- Runs `DROP`, `TRUNCATE`, `DELETE` without a `WHERE`, `prisma migrate reset`,
  `rm -rf` or anything with `--force` near production
- Installs a package you've never heard of that has few downloads
- Says "this is now secure" without showing what it checked

---

Back to the [start](../README.md)
