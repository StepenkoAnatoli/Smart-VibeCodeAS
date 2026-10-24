# Rescuing a messy AI-built project

It happens to almost everyone who builds fast with AI: the app works (mostly),
but nobody understands it anymore. Every new feature breaks two old ones, the
AI keeps "fixing" the same bug, and you're afraid to touch anything. This
chapter is the way back to control, step by step, without throwing away what
works.

The order matters: **safety first, understanding second, cleanup last.**

## Contents

1. [Signs you need a rescue](#1-signs-you-need-a-rescue)
2. [Step 1: Stop and secure what you have](#step-1-stop-and-secure-what-you-have)
3. [Step 2: Make it run from scratch](#step-2-make-it-run-from-scratch)
4. [Step 3: Map it](#step-3-map-it)
5. [Step 4: Fix what's dangerous](#step-4-fix-whats-dangerous)
6. [Step 5: Put a safety net around what works](#step-5-put-a-safety-net-around-what-works)
7. [Step 6: Clean up in small slices](#step-6-clean-up-in-small-slices)
8. [Rewrite or repair?](#rewrite-or-repair)
9. [Moving out of an app builder](#moving-out-of-an-app-builder)
10. [When to get human help](#when-to-get-human-help)
11. [Copy-paste rescue prompts](#copy-paste-rescue-prompts)

---

## 1. Signs you need a rescue

- You can't explain, in plain words, where your data lives and who can see it.
- Fixing one bug regularly creates another.
- The same logic exists in several places, and the AI changes the wrong one.
- There are no tests, or the tests were switched off.
- You're not sure the code on GitHub matches what's live.
- Keys or passwords are scattered across files.
- You're afraid to deploy.

Two or more of these: stop adding features and work through this chapter.

---

## Step 1: Stop and secure what you have

**Freeze features.** Every new feature added to a codebase you don't understand
makes the rescue longer. Tell users (if any) that you're doing maintenance.

Then make sure nothing can be lost:

- **Commit everything,** but first make sure `.env` and any other files holding
  keys are listed in `.gitignore`. Then push it to a **private** GitHub repo
  in **your** name. If the app lives in an app builder, connect it to GitHub
  or export it first.
- **Back up the database** and download a copy. Check your plan's backup
  settings.
- **List every account and service** the app uses (hosting, database, auth,
  storage, email, payments, AI providers, domain) and confirm you can log in to
  each, with 2FA on.
- **Find exposed secrets** (keys in code, in frontend files, in Git history)
  and **replace them** at each provider. Assume anything that was ever in the
  code is known.
- **Set spending caps** on everything that bills you.

---

## Step 2: Make it run from scratch

If the app can only be run from one person's laptop or one builder's
workspace, you don't control it yet.

1. Clone the repo into a **new, empty folder** (or have someone else try).
2. Follow the README to install and run it. If there's no README, or it's wrong,
   that's the first thing to fix.
3. Make a `.env.example` listing every setting the app needs, without the
   secret values.
4. Get a **separate development database** with fake data (see *Test data and
   seed scripts* in [Your database, explained](06-your-database.md#6-habits-that-save-you-later)).
5. Confirm the production build works (`npm run build`) and that deploying
   from GitHub produces the same app that's live.

At the end of this step you can rebuild the whole thing from GitHub plus your
list of accounts. That alone removes most of the fear.

---

## Step 3: Map it

You don't need to read the code; you need a map. Ask your AI to produce, and
save in the repo as `ARCHITECTURE.md`:

- **The pieces:** frontend, backend routes, database, outside services, and how
  they connect.
- **The data:** every table, what it holds, who owns each row, and who can read
  it.
- **The features:** each one, with the files that implement it.
- **The flows:** sign-up, login, the core feature, and payment, step by step.
- **The mess:** duplicated logic, dead code, unused packages, very large files,
  and anything it doesn't understand.

Read it. Wherever the map surprises you ("wait, the frontend talks to the
database directly?"), you've found something to check in step 4.

---

## Step 4: Fix what's dangerous

Before any tidying, close the holes that can hurt users or cost money, in this
order:

1. **Secrets** in the browser or in Git (step 1 replaced them; now remove them
   from the code).
2. **Access control:** every route and table checks that the user owns the data.
   With Supabase or Firebase, Row Level Security or Security Rules with real
   policies on every table.
3. **Money:** prices decided on the server, access granted by verified webhooks,
   no double charges.
4. **Data safety:** tested backups, no production credentials in reach of AI
   tools, migrations reviewed.
5. **Abuse and cost:** rate limits and quotas on login and on anything that
   costs money.

The all-in-one prompt in [How vibe-coded apps break](10-how-vibe-coded-apps-break.md#ask-your-ai-to-check-for-all-of-these)
checks for all 19 common failures at once. Fix one problem per change, and test
each fix.

---

## Step 5: Put a safety net around what works

Before changing working code, write tests that pin down what it **currently**
does. (Developers call these *characterization tests*.) Even if the current
behavior is a bit odd, the tests make sure cleanup doesn't change it by
accident.

Start with end-to-end tests of the money paths: sign-up, login, the core
feature and payment (see *Testing the paths that matter* in
[Beyond the reel](05-beyond-the-reel.md#3-does-it-actually-work)). Run them in CI
on every change. From now on, a change that breaks a test doesn't get merged.

---

## Step 6: Clean up in small slices

Now improve the code, one small, testable slice at a time, each in its own
branch and pull request:

- **Delete dead code** and unused packages. It's the safest cleanup and makes
  everything else easier.
- **Merge duplicates:** when the same logic exists in several places, keep one
  shared version and point everything at it.
- **Split giant files** into focused ones.
- **Add types** and fix the errors they reveal (TypeScript, or Python type
  hints).
- **Write the rules down:** start a rules file (see
  [Vibe coding well](02-vibe-coding-well.md#3-what-your-ai-can-and-cant-see))
  with the conventions you settle on, so the AI stops reintroducing the mess.

After each slice: tests pass, you click through the app, you commit. Never
combine cleanup with new features in the same change.

---

## Rewrite or repair?

"Let's just rebuild it from scratch" is tempting, and usually wrong. A rewrite
throws away all the small fixes the old version collected, takes longer than
expected, and the AI will happily produce a new mess if the process doesn't
change.

**Repair** (steps 1–6) when the app basically works and the data model is
sound.

**Rewrite** a part, not the whole, when:

- the app is still small, with few users;
- the **data model** is fundamentally wrong (for example, everything stored in
  one JSON blob), and fixing it piece by piece would touch everything anyway;
- or a piece is built on a tool you've decided to leave.

Even then, replace one part at a time behind the same screens and data,
switching over gradually, and keep the old data. Migrate it; don't abandon it.

---

## Moving out of an app builder

Projects often start in an app builder and outgrow it. The usual path:

1. **Connect the project to GitHub** (most builders support this) or export the
   code.
2. **Run it locally** (step 2), with your own `.env` settings.
3. **Keep the backend services you already use.** If the database and logins
   are on Supabase, your users and data stay where they are; only the code
   moves. This only works if that Supabase project is in **your own** Supabase
   account. If your builder hosts the backend for you (Lovable Cloud, for
   example), you must first migrate the data and users to a project you own.
   Plan for it, and check whether users will need to reset their passwords.
4. **Deploy from GitHub** to a host like Vercel or Netlify, on a temporary
   address first. Set the same environment variables there.
5. **Test everything** on the temporary address: login (add the new address to
   your auth provider's allowed redirect URLs), payments in test mode, and
   emails.
6. **Switch the domain** (DNS) to the new host, then watch error tracking
   closely for a few days.

---

## When to get human help

AI can do most of this with you, but some moments call for an experienced
person:

- a **suspected breach** or leaked user data;
- **payments** behaving strangely or money going missing;
- a real risk of **losing data** (a broken migration on production, failing
  backups);
- before a big launch, or before handling sensitive data (health, finance,
  children).

A short, paid code review by an experienced developer is often enough. Ask for
something specific: "review access control, secrets and payment handling, and
list problems by severity", and share your `ARCHITECTURE.md` to save their
time (and your money).

---

## Copy-paste rescue prompts

### Map the project

```
I don't understand this project anymore. Read the whole codebase and write
ARCHITECTURE.md for a non-programmer: the pieces (frontend, backend routes,
database, outside services) and how they connect; every table, what it holds,
who owns each row and who can read it; each feature and the files behind it;
the sign-up, login, core and payment flows step by step; and a "mess" section
listing duplicated logic, dead code, unused packages, very large files and
anything you don't understand. Don't change any code.
```

### Make it run from scratch

```
Make this project runnable from a fresh clone. Check that the README's setup
steps actually work, write a .env.example listing every environment variable
the code uses (without secret values) and what each is for, add a seed script
with realistic fake data for a development database, and tell me anything
that only works on the original machine or workspace.
```

### Plan the cleanup

```
Using ARCHITECTURE.md, propose a cleanup plan as a list of small, independent
steps, each one a single pull request that keeps the app working: safety fixes
first, then tests around the main flows, then dead code, duplicates and giant
files. For each step: what changes, the risk, and how I'll check it still
works. Don't start yet.
```

---

Next: [Pre-launch checklist and copy-paste AI prompts](12-checklist-and-ai-prompts.md)
