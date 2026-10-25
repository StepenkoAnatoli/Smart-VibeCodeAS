# Working with a developer

AI can take you a long way, but some moments call for an experienced person: a
security review before real users arrive, an incident, a project that's
outgrown what you can steer, or a feature that touches money or sensitive data.
Hiring help is a skill of its own. Done badly, it costs money and can leave you
*less* in control of your app. Done well, it's the fastest way to learn.

Labels as elsewhere: 🔴 **Now**, 🟡 **Soon**, ⚪ **Later**.

## Contents

1. [When to bring in a person](#1-when-to-bring-in-a-person)
2. [Kinds of help](#2-kinds-of-help)
3. [Finding and checking someone](#3-finding-and-checking-someone)
4. [Giving access safely](#4-giving-access-safely)
5. [Briefing them](#5-briefing-them)
6. [Asking for a code review](#6-asking-for-a-code-review)
7. [Quotes and agreements](#7-quotes-and-agreements)
8. [Working together](#8-working-together)
9. [When the work ends](#9-when-the-work-ends)
10. [Copy-paste prompts](#10-copy-paste-prompts)

---

## 1. When to bring in a person

### Moments worth paying for — 🟡 Soon

- **Before launch**, if the app holds personal data or takes payments: a
  security review of access control, secrets and payments.
- **During an incident** involving leaked data, money or lost data (see
  [When things go wrong](13-when-things-go-wrong.md)).
- **When you're stuck in loops** your AI can't get out of, on something
  important.
- **Before handling sensitive data** (health, finance, children), where the
  rules are stricter.
- **When the app outgrows you:** more users, a team, a mobile app, or
  business customers with security questionnaires.

You don't need a developer for everything. A few focused hours at the right
moment are often worth more than months of general help.

---

## 2. Kinds of help

### Matching the help to the need — 🟡 Soon

| Kind | Good for | Typical shape |
|---|---|---|
| **Code review** | Checking what you built for security and serious mistakes | A few hours; you get a list of problems by severity |
| **Freelancer, for a task** | A specific feature or fix with a clear goal | Days to weeks, fixed scope |
| **Freelancer, ongoing** | Steady help as the app grows | Some hours each week |
| **Agency** | A large build with design and project management included | More expensive; you get a team |
| **Fractional CTO / advisor** | Technical decisions and direction, not daily coding | A few hours a month |
| **Mentor or community** | Learning, and a second opinion | Often free or cheap: developer communities, forums, local meetups |

---

## 3. Finding and checking someone

### Choosing well — 🟡 Soon

**Look for:**

- Experience with **your stack** (for example Next.js and Supabase), shown in
  past work.
- Clear, plain explanations. If they can't explain something to you now, they
  won't later.
- References from past clients.
- Willingness to start with a **small paid trial task** before anything big.

**Red flags:**

- They want to **rewrite everything** before understanding what you have.
- They ask for **your passwords** instead of their own access (section 4).
- They won't work in **Git and pull requests**, or they push straight to
  production.
- No written scope or estimate, or an estimate with no breakdown.
- They dismiss tests, backups or security as unnecessary.
- They want to host the app or register accounts **in their name**.

---

## 4. Giving access safely

### Their own access, as little as needed — 🔴 Now

**What it is:** Never share your passwords. Invite the developer with **their
own account** wherever the service supports it, with the smallest role that
does the job (see *IAM* in [the reel, explained](04-the-reel-explained.md#1-security)).

**What it means for you:**

- **GitHub:** add them as a collaborator on the repo. Collaborators can push
  and merge on their own, so agree that they only open pull requests, and turn
  on branch protection if your plan has it (on private repos it needs a paid
  GitHub plan).
- **Hosting, database, payments:** use each service's team or member feature,
  with a limited role where one exists.
- **Development first:** give access to the **development** environment and
  test keys. Production access and live keys only if the job truly needs them,
  and only for as long as it does. On Supabase's Free and Pro plans, a member
  can see **every** project in the organization, so keep your development
  project in its own organization and invite them only there.
- **Vercel's free Hobby plan** has no team members, and commits by other people
  don't deploy (so their pull requests get no preview). Either move to a paid
  team plan for the time they work with you, or review their pull requests
  without previews. Never share your login instead.
- **Secrets:** share them through your host's environment settings or a
  password manager's sharing feature, never in chat or email.
- **Keep a list** of everything you gave access to, so you can remove it later
  (section 9).

---

## 5. Briefing them

### A good brief saves paid hours — 🟡 Soon

Give them, in writing:

- **What the app is** and who uses it: your `SPEC.md`.
- **How it's built:** your `README.md` and an `ARCHITECTURE.md` map (see
  [Rescuing a messy project](14-rescuing-a-messy-project.md#step-3-map-it)).
- **The task:** what "done" looks like, in terms you can check yourself ("a free
  user can't create an 11th note, and there's a test proving it").
- **What not to touch,** and any decisions already made.
- **Constraints:** deadline, budget, and that you need to understand the
  result.

---

## 6. Asking for a code review

### Ask for specifics — 🔴 Now (before launching with real data or money)

A vague "can you take a look?" gets a vague answer. Ask for:

- **Scope:** access control (every route, server action and database policy),
  secrets, payments and webhooks, input validation, the data model, backups,
  and your AI features if you have them.
- **Output:** a list of findings ranked by severity, each with the file, what's
  wrong, how it could be exploited or fail, and the fix.
- **Plain words:** an explanation you can understand, and which findings must
  be fixed before launch.
- **Verification:** for the serious ones, a way to *show* the problem (like
  the attacker tests in [Logins, done right](08-logins-done-right.md#7-test-it-like-an-attacker)),
  and a test that proves the fix.

---

## 7. Quotes and agreements

### Understand what you're agreeing to — 🟡 Soon

*Not legal advice; look up what applies where you and they are.*

- **Hourly or fixed price?** Hourly suits unclear work; fixed price suits a
  well-defined task. A cheap fixed price for vague work usually ends in
  arguments, or in quality being cut.
- **Ask for a breakdown** and a range, not one number, and agree how changes to
  the scope are handled.
- **Pay in milestones** tied to things you can check, not up front.
- **Put in writing:** that **you own the code** they write (often called an IP
  or intellectual property assignment), confidentiality, which open-source
  licenses they use, and what they hand over at the end.
- **Accounts stay yours:** domain, hosting, database, payments and app store
  accounts in your name, with them as invited members.

---

## 8. Working together

### Same rules for people and AI — 🟡 Soon

- All work goes through **pull requests**, with the automatic checks passing
  and, where your hosting plan allows it, a preview deploy you can click
  through.
- Ask for a **plain-words summary** of every pull request: what changed, why,
  and how to check it. You can also ask your own AI to explain it (prompt below).
- They should follow your **rules file** and keep the README and architecture
  notes current. Many developers use AI tools too; that's fine, as long as the
  same rules and reviews apply.
- Agree how often you'll get updates, and what to do when something urgent
  breaks.

---

## 9. When the work ends

### Offboarding — 🔴 Now

When someone's work finishes, the same day:

- **Remove their access** everywhere on your list from section 4: GitHub,
  hosting, database, payments, monitoring, email.
- **Replace any secret they could see,** especially production keys. People
  leave on good terms too; this is just hygiene.
- Make sure all code is **merged into your repo**, and the README and
  architecture notes are current.
- Check that no account, domain or service ended up in **their** name, and
  transfer it if it did.

---

## 10. Copy-paste prompts

### Write a brief for a developer

```
Write a brief I can send to a freelance developer for this task: [task].
Include what the app is (from SPEC.md), how it's built (stack, main folders,
database tables, outside services), exactly what "done" means in terms I can
check myself, what they must not change, and what access they'll need
(development environment only, if possible). Keep it to one page.
```

### Explain a developer's pull request to me

```
Explain this pull request to me in plain words: what changed, why, which
parts of the app it affects, and anything risky (security, data, payments,
removed checks or tests). Then list three questions I should ask the
developer before merging it.
```

### Prepare a code review request

```
Prepare a code review request for an experienced developer, before we launch
with real users. Summarize the app and stack, and list exactly what to review:
access control in every route, server action and database policy; secrets;
payments and webhooks; input validation; the data model; backups; and our AI
features. Ask for findings ranked by severity with files, exploit or failure
scenarios, fixes, and tests that prove the fixes.
```

---

Back to the [start](../README.md)
