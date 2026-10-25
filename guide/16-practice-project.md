# Practice project: build a small app the safe way

Reading this guide gives you the words. Building something with them gives you
the skill. This chapter walks you through one small, real app, step by step.
Each step uses a part of the guide, gives you the prompt to hand your AI, and,
most importantly, tells you **how to check it yourself**.

**What you'll build:** *Private Notes*, a web app where people sign up, write
notes that only they can see, and can upgrade to a "Pro" plan (in Stripe's
**test mode**, so no real money) to store more than 10 notes.

It's small on purpose, but it has everything that goes wrong in real apps:
logins, private data, a limit people will try to get around, payments,
webhooks, tests, deploys and backups.

**Time:** a weekend, or a few evenings. **Cost:** free tiers are enough.
**Stack:** the default from [Starting a project safely](03-starting-a-project-safely.md#1-a-sensible-default-stack):
Next.js, Supabase, Vercel and Stripe in test mode. Your AI tool does the
coding; you do the deciding and the checking.

Tick the boxes as you go. On the one-page version of this guide, your ticks are
remembered in your browser.

## Contents

1. [Step 1: Spec and rules](#step-1-spec-and-rules)
2. [Step 2: Accounts and repo](#step-2-accounts-and-repo)
3. [Step 3: Development database and first run](#step-3-development-database-and-first-run)
4. [Step 4: Logins](#step-4-logins)
5. [Step 5: The notes table, locked down](#step-5-the-notes-table-locked-down)
6. [Step 6: Try to break in](#step-6-try-to-break-in)
7. [Step 7: Validation and the free limit](#step-7-validation-and-the-free-limit)
8. [Step 8: Payments in test mode](#step-8-payments-in-test-mode)
9. [Step 9: Tests and CI](#step-9-tests-and-ci)
10. [Step 10: Deploy](#step-10-deploy)
11. [Step 11: Watch it](#step-11-watch-it)
12. [Step 12: Fire drills](#step-12-fire-drills)
13. [Step 13: Final review](#step-13-final-review)
14. [What you practiced](#what-you-practiced)

---

## Step 1: Spec and rules

**Goal:** Decide what you're building before any code exists.
**Uses:** [Vibe coding well](02-vibe-coding-well.md#1-before-you-prompt).

```
Help me write SPEC.md for "Private Notes": users sign up with email, verify
it, and write private notes (title + text) that only they can see, edit and
delete. Free users can have 10 notes; Pro users (paid with Stripe, test mode
only) have unlimited notes. No sharing, no teams, no AI features for now.
Ask me anything that's unclear, then write SPEC.md. Then draft a CLAUDE.md /
AGENTS.md with the stack (Next.js + TypeScript, Supabase, Stripe, Zod,
Tailwind), the safety rules from the guide, and "propose a plan before
changing more than one file".
```

**Check it yourself:**

- [ ] `SPEC.md` describes who can see what, and the 10-note limit
- [ ] The rules file includes "never disable Row Level Security" and "validate
      input on the server"

---

## Step 2: Accounts and repo

**Goal:** Secure the foundations before writing code.
**Uses:** [Starting a project safely](03-starting-a-project-safely.md#2-accounts-before-code).

Create accounts at GitHub, Supabase, Vercel and Stripe, each with two-factor
login on. Then:

```
Create a new Next.js + TypeScript project for Private Notes. Before anything
else: a .gitignore that excludes .env, .env.local and node_modules; a
.env.example listing every variable we'll need with blank values; and a
README explaining how to run it. Commit and push to my private GitHub repo.
```

**Check it yourself:**

- [ ] The GitHub repo is **private**
- [ ] Create a `.env.local` file with a fake value, run `git status`, and
      confirm the file is **not** listed
- [ ] Two-factor login is on for all four accounts

---

## Step 3: Development database and first run

**Goal:** A database you're free to break.
**Uses:** [Two of everything](03-starting-a-project-safely.md#4-two-of-everything-development-and-production).

Create a Supabase project called `private-notes-dev`. Put its address and
**publishable** key in `.env.local`, never the secret key in anything the
browser loads.

```
Connect the app to Supabase using the URL and publishable key in .env.local.
Use Supabase's server helpers so server code can verify the user. Show me
how to start the app locally.
```

**Check it yourself:**

- [ ] `npm run dev` starts the app, and it opens at `http://localhost:3000`
- [ ] Search the code for `secret` or `service_role`: no secret key is in any
      file that runs in the browser

---

## Step 4: Logins

**Goal:** Sign-up and login, with the provider doing the hard parts.
**Uses:** [Logins, done right](08-logins-done-right.md).

In Supabase's auth settings, make sure email confirmation is on and the
allowed redirect URLs include `http://localhost:3000`.

```
Add sign up, email verification, log in, log out and "forgot password"
using Supabase Auth. Server code must get the user from the verified
session (getUser or equivalent), never from anything the browser sends.
After login, only redirect to paths on our own site.
```

**Check it yourself:**

- [ ] Sign up with a real email address you own, click the verification link,
      and log in
- [ ] Log out, press the browser's Back button, reload: you're still logged
      out
- [ ] "Forgot password" sends a link, and the link doesn't work a second time
- [ ] Visit `/login?next=https://example.com`, log in, and confirm you stay on
      your own site

---

## Step 5: The notes table, locked down

**Goal:** Private data that the database itself protects.
**Uses:** [Your database, explained](07-your-database.md) and *Broken Access
Control* in [the reel, explained](04-the-reel-explained.md#1-security).

```
Create a migration for a notes table: id (uuid), user_id (references the
auth user), title (text, max 200 characters), body (text, max 20,000
characters), created_at and updated_at (timestamptz). Turn on Row Level
Security with policies so users can only select, insert, update and delete
their own notes (auth.uid() = user_id). Add an index on user_id. Then build
the pages to list, create, edit and delete notes. Show me the migration
before running it.
```

**Check it yourself:**

- [ ] In Supabase's dashboard, the `notes` table shows **RLS enabled**, with
      policies that mention `auth.uid()`
- [ ] None of the policies is "allow everyone" (`using (true)`)
- [ ] The migration file is saved in the repo

---

## Step 6: Try to break in

**Goal:** Prove the lock works, from the attacker's side.
**Uses:** [Test it like an attacker](08-logins-done-right.md#7-test-it-like-an-attacker).

Create two accounts, A and B (two email addresses, or one email with `+a` and
`+b` before the `@` if your provider supports that). Write a note as each.

```
Write a short script I can run that logs in as user A and tries, using the
normal Supabase client and the publishable key, to: read user B's notes,
update one of user B's notes by its id, delete it, and insert a note with
user_id set to B. Print what happened for each. All four must fail.
```

**Check it yourself:**

- [ ] All four attempts are **blocked**
- [ ] Open note B's page URL while logged in as A: you get "not found" or "not
      allowed", never the note
- [ ] Now the lesson: temporarily turn off RLS on the `notes` table in your
      **dev** project, run the script again, and watch A read B's notes. Turn
      RLS back on and confirm the script is blocked again.

---

## Step 7: Validation and the free limit

**Goal:** Rules enforced where users can't skip them.
**Uses:** *Data Validation* and *Race Conditions* in
[the reel, explained](04-the-reel-explained.md#2-databases--performance).

```
Validate note input on the server with Zod (title 1–200 characters, body up
to 20,000). Enforce the 10-note limit for free users on the server and in the
database, not only in the UI, so that two requests at the same moment can't
both get past it. Add a rate limit on creating notes. Explain where each rule
is enforced.
```

**Check it yourself:**

- [ ] Creating an 11th note as a free user is refused, with a friendly message
- [ ] Submitting an empty title, or one that's 500 characters long, is refused
      **by the server** (ask your AI how to send a request that skips the form)
- [ ] Double-clicking "Save" on the 10th note doesn't produce an 11th

---

## Step 8: Payments in test mode

**Goal:** The safe payment pattern, with no real money.
**Uses:** *Webhooks* and *Idempotency* in [the reel, explained](04-the-reel-explained.md#6-performance-metrics--networking),
and [How vibe-coded apps break](12-how-vibe-coded-apps-break.md#money).

Use Stripe in **test mode** only. Install the Stripe command-line tool, which
can forward webhooks to your laptop (`stripe listen --forward-to ...`) and send
test events (`stripe trigger ...`).

```
Add an "Upgrade to Pro" button using Stripe Checkout in test mode. The price
comes from a Stripe price ID stored on the server, never from the browser.
Pro status changes only in a webhook handler that verifies Stripe's
signature and records processed event IDs so a repeated event does nothing.
Store the plan where only the server can write it. The success page only
says thank you. Show me how to test it locally with the Stripe CLI.
```

**Check it yourself:**

- [ ] Upgrade with Stripe's test card `4242 4242 4242 4242` (any future date,
      any CVC): the account becomes Pro
- [ ] With a fresh free account, type the success page's address directly: the
      account stays **free**
- [ ] Resend the same webhook event (from Stripe's dashboard, or the CLI): Pro
      status doesn't break, nothing happens twice
- [ ] Send a fake request to your webhook URL without a valid signature: it's
      rejected

---

## Step 9: Tests and CI

**Goal:** A safety net that runs on every change.
**Uses:** [Testing, for people who don't code](10-testing-for-non-coders.md).

```
Set up Playwright end-to-end tests for: sign up and log in, creating /
editing / deleting a note, the 10-note limit, and upgrading with Stripe's
test card. Turn the Step 6 script into an automated access-control test.
Use a separate test database. Add a GitHub Actions workflow that runs build,
lint and all tests on every pull request.
```

**Check it yourself:**

- [ ] The tests pass locally and on GitHub (green check on a pull request)
- [ ] **Break it on purpose:** in your dev database, change the notes policy so
      it allows everyone. The access-control test must fail. Undo it.
- [ ] No test is skipped (`.skip`) or marked `.only`

---

## Step 10: Deploy

**Goal:** A live copy, with production kept separate.
**Uses:** [Starting a project safely](03-starting-a-project-safely.md#4-two-of-everything-development-and-production).

Create a second Supabase project, `private-notes-prod`, and run your
migrations there. Import the repo into Vercel. Set the **Production**
environment variables to the prod project, and **Preview** to the dev project.
Keep Stripe in **test mode** even in production: this is practice, and
Vercel's free plan isn't for apps that take real money.

```
Help me deploy to Vercel: list every environment variable for Production and
for Preview, the redirect URLs to add in Supabase Auth for the production
and preview addresses, and the Stripe webhook endpoint to register (test
mode). Then open a small pull request so I can check its preview deploy.
```

**Check it yourself:**

- [ ] The production address works: sign up, verify, log in, write a note
- [ ] A pull request gets its own preview address, which uses the **dev**
      database
- [ ] The production project's `notes` table has RLS on (re-run the Step 6
      script against production with two throwaway accounts)

---

## Step 11: Watch it

**Goal:** Know when it breaks before your users tell you.
**Uses:** *Observability* in [the reel, explained](04-the-reel-explained.md#4-deployments--reliability).

```
Add Sentry error tracking (with personal data filtered out) and a test
route, only available in development, that throws an error so I can see it
arrive. Tell me how to set up a free uptime monitor for the production
address.
```

**Check it yourself:**

- [ ] A test error shows up in Sentry
- [ ] An uptime monitor watches the production address
- [ ] Billing alerts are set on Vercel, Supabase and Stripe where offered

---

## Step 12: Fire drills

**Goal:** Practice recovery while nothing is at stake. This is the step people
skip, and the one that matters most on a bad day.
**Uses:** [When things go wrong](13-when-things-go-wrong.md).

Do each of these on **dev** or with test data:

- [ ] **Leaked key drill:** create a new secret key in Supabase (and Stripe
      test mode), update the environment variables, redeploy, then delete the
      old key. Confirm the app still works.
- [ ] **Bad deploy drill:** merge a small visible change, then roll back to
      the previous deploy in Vercel. Note how long it took.
- [ ] **Data loss drill:** export your dev database (or use a backup if your
      plan has one), delete a few notes, then restore the export into a
      **new** database and confirm the notes are there.
- [ ] **Write your incident kit** (`INCIDENT-PLAYBOOK.md`) with the prompt in
      [When things go wrong](13-when-things-go-wrong.md#6-copy-paste-incident-prompts).

---

## Step 13: Final review

**Goal:** Check the whole app with fresh eyes.

- [ ] Run the all-in-one prompt from
      [How vibe-coded apps break](12-how-vibe-coded-apps-break.md#ask-your-ai-to-check-for-all-of-these)
      in a **new** conversation, and fix what it finds
- [ ] Go through the [pre-launch checklist](15-checklist-and-ai-prompts.md)
- [ ] Take the quiz on the one-page version of this guide

---

## What you practiced

| Step | What you now know how to do | Chapter |
|---|---|---|
| 1 | Specs and rules files | [Vibe coding well](02-vibe-coding-well.md) |
| 2–3 | Safe accounts, repo and environments | [Starting a project safely](03-starting-a-project-safely.md) |
| 4 | Logins, redirects, password reset | [Logins, done right](08-logins-done-right.md) |
| 5–6 | Row Level Security, and testing it like an attacker | [Your database, explained](07-your-database.md) |
| 7 | Server-side validation, limits, race conditions | [The reel, explained](04-the-reel-explained.md) |
| 8 | Payments, verified webhooks, idempotency | [How vibe-coded apps break](12-how-vibe-coded-apps-break.md) |
| 9 | Tests that fail when they should, and CI | [Testing](10-testing-for-non-coders.md) |
| 10–11 | Deploys, environments, monitoring | [Beyond the reel](06-beyond-the-reel.md) |
| 12 | Key rotation, rollback, restore | [When things go wrong](13-when-things-go-wrong.md) |

When you build your own app, follow the same order. Most of the disasters in
this guide happen when one of these steps was skipped.

---

Next: [Working with a developer](17-working-with-a-developer.md)
