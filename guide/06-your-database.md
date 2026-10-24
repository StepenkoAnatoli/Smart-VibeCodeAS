# Your database, explained

The database is the one part of your app that's hard to change later. Code can
be rewritten in an afternoon; data that was stored the wrong way stays wrong,
and fixing it means migrating every row while the app is live. AI tools
usually design the database in the first few minutes of a project, without
asking you anything, so this is where a little knowledge pays off most.

Labels as elsewhere: 🔴 **Now** (before you have real data), 🟡 **Soon**,
⚪ **Later**.

## Contents

1. [Tables, rows and columns](#1-tables-rows-and-columns)
2. [How tables connect](#2-how-tables-connect)
3. [Storing values the right way](#3-storing-values-the-right-way)
4. [Rules the database enforces for you](#4-rules-the-database-enforces-for-you)
5. [Deleting things](#5-deleting-things)
6. [Habits that save you later](#6-habits-that-save-you-later)
7. [Copy-paste database prompts](#7-copy-paste-database-prompts)

---

## 1. Tables, rows and columns

### The basic shape — 🔴 Now

**What it is:** A database (like Postgres, which Supabase uses) stores data in
**tables**. Each table holds one kind of thing: `users`, `projects`,
`invoices`. Each **row** is one of those things, and each **column** is one
fact about it.

**Picture it:** A spreadsheet per kind of thing. The `users` sheet has a row
per user, with columns for `id`, `email`, `name` and `created_at`.

| id | email | name | created_at |
|---|---|---|---|
| 7f3a… | ana@example.com | Ana | 2026-03-02 09:14 UTC |
| 91bc… | ben@example.com | Ben | 2026-03-05 17:40 UTC |

**What it means for you:** Before building, list the *things* in your app
(nouns from your spec) and the facts about each. That list is your database
design. Ask the AI to show it to you as tables before it creates anything.

### Primary keys and IDs — 🔴 Now

Every row needs a unique **ID** (its *primary key*), so other data can point
to it. There are two common kinds:

- **Counting numbers** (1, 2, 3...): simple, but they reveal how many
  customers you have, and they're easy to guess: if your order is 1041, try
  1040.
- **Random IDs** such as UUIDs (`7f3a9c2e-…`): impossible to guess and safe to
  show in URLs.

**Do:** Prefer random IDs for anything that appears in a URL. But remember that
a hard-to-guess ID is *not* security. Every request must still check that the
user may see that row (see *Broken Access Control*).

---

## 2. How tables connect

### One-to-many — 🔴 Now

**What it is:** One user has many projects; each project belongs to one user.
You store this by giving each project a `user_id` column holding its owner's
ID. That column is a **foreign key**: a pointer to a row in another table.

| projects.id | name | user_id |
|---|---|---|
| p1 | Website redesign | 7f3a… (Ana) |
| p2 | Spring campaign | 7f3a… (Ana) |
| p3 | Podcast | 91bc… (Ben) |

**What it means for you:** That `user_id` column is also how access control
works: "show projects where `user_id` = the logged-in user", and how Row Level
Security policies are written. If a table holds private data, it needs a column
saying whose data it is.

### Many-to-many — 🟡 Soon

**What it is:** A user can be in many teams, and a team has many users. You
can't store that in one column, so you add a third table in between, often
called a *join table*: `team_members` with columns `team_id`, `user_id` and
maybe `role`.

**What it means for you:** If the AI stores a list of IDs inside a single text
or JSON column instead ("member_ids: [1, 5, 9]"), questions like "which teams
is Ben in?" become slow and error-prone, and permissions get hard to enforce.
Ask for a join table.

### Don't store the same fact twice — 🟡 Soon

If the customer's email is copied into every order row, changing it means
updating every copy, and some will be missed. Store each fact once and point to
it with an ID. (Experts call this *normalization*.) The exception is a deliberate
**snapshot**: an invoice *should* keep the price and address as they were on
the day it was issued, even if they change later.

### JSON columns: handy, easy to overuse — 🟡 Soon

Databases can store a whole JSON object in one column. That's useful for
genuinely free-form data (settings, raw webhook payloads). It's a trap for data
you'll search, filter, sort, total or protect, because the database can't
check it, index it well or enforce relationships inside it. If you'll ask
questions about it, it deserves real columns.

---

## 3. Storing values the right way

### Money: whole numbers of cents — 🔴 Now

**What it is:** Computers store decimal numbers like 0.1 approximately, so
`0.1 + 0.2` comes out as `0.30000000000000004`. Add up thousands of prices this
way and the totals drift.

**Do:** Store money as **integers in the smallest unit** (cents: `1999` for
$19.99), plus a `currency` column. Stripe does exactly this. Only format it as
"$19.99" when you show it. (Postgres's `numeric` type is the other safe
choice.) Never let the AI use a floating-point number for money.

### Time: UTC, with the time zone — 🔴 Now

**What it is:** "9:00" means nothing without a time zone, and clocks shift for
daylight saving time.

**Do:** Store moments in time in **UTC**, in a column type that knows about
time zones (in Postgres, `timestamptz`). Convert to the user's local time only
for display. Add `created_at` and `updated_at` to every table; you'll want them
when debugging. Store a pure date (a birthday, a due date) as a `date`, not a
time.

### Status fields — 🟡 Soon

Many things move through stages: an order is `pending`, `paid`, `shipped`,
`refunded`. Store this as one `status` column limited to a fixed list of
allowed values (an *enum* or a *check constraint*), not as several true/false
columns (`is_paid`, `is_shipped`) that can contradict each other.

### What not to store — 🔴 Now

- **Passwords:** let your auth provider handle them. If they must be stored,
  only as a hash (bcrypt or argon2), never as text you could read.
- **Card numbers:** never. Your payment provider stores them; you keep only
  its customer and payment IDs. Handling card numbers yourself brings heavy
  security rules (PCI DSS).
- **Secrets and API keys** in normal tables: keep them in environment
  variables or a secrets manager.
- **Anything you don't need.** Every extra column of personal data is something
  that can leak.

---

## 4. Rules the database enforces for you

### Constraints — 🟡 Soon

**What it is:** Rules attached to the database itself, which it enforces on
every write, no matter which piece of code (or which bug) is writing:

- `NOT NULL`: this column must have a value.
- `UNIQUE`: no two rows may share this value (like an email, or one
  "like" per user per post).
- **Foreign keys:** `user_id` must point to a user that exists.
- `CHECK`: a custom rule, such as `price_cents >= 0`.

**Why it matters for vibe coders:** Code validation can be skipped, forgotten
or bypassed by a bug. Database constraints can't. A `UNIQUE` rule is also one of
the simplest fixes for *Race Conditions*: two simultaneous "redeem coupon"
requests can't both succeed if the second insert violates a unique rule.

### Indexes on the columns you search — 🟡 Soon

Covered in *Database Indexing* in [the reel, explained](03-the-reel-explained.md#2-databases--performance).
In short: add an index for every foreign key and every column you filter or
sort by.

---

## 5. Deleting things

### Hard delete vs soft delete — 🟡 Soon

- **Hard delete:** the row is actually removed. Simple, and what privacy laws
  often require when a user asks for deletion.
- **Soft delete:** the row stays, with a `deleted_at` time set, and your app
  hides it. It allows "undo" and keeps history, but every query must remember
  to filter deleted rows out. When one forgets, "deleted" data appears again.

**Do:** Decide per table, on purpose. Use soft delete where undo or history
matters, hard delete for personal data a user asked you to remove, and make
sure your backups and logs follow the same rules.

### What happens to related rows — 🟡 Soon

When you delete a user, what happens to their projects, comments and invoices?
Foreign keys let you choose: **cascade** (delete them too), **set null** (keep
them, with the owner removed), or **restrict** (refuse the delete while related
rows exist). AI often picks *cascade* without asking. That can be right
(private drafts), or a disaster: deleting one user silently deletes invoices
you're legally required to keep. Ask which rule each foreign key uses.

---

## 6. Habits that save you later

### Every change is a migration — 🔴 Now

Change the database's structure only through migrations that are saved in Git,
never by clicking around in the production dashboard. Read each migration
before it runs on production, and back up first. (See *Database Migrations* in
[the reel, explained](03-the-reel-explained.md#2-databases--performance).)

### Changing a column that has data — 🟡 Soon

Renaming or retyping a column that holds data, or deleting it, can break the
running app between deploy and migration, or lose data. The safe pattern:
**add** the new column, make the code **write to both** columns, **copy** the
old data across, switch the code to **read** from the new column, and only
later **remove** the old one. (Skip the "write to both" step and any rows saved
during the copy are lost.) Ask the AI for this
"expand and contract" approach on any live table.

### Test data and seed scripts — 🟡 Soon

A *seed script* fills a development database with realistic fake data: users,
projects, a few thousand rows. It lets you test empty states, long lists and
slow queries without touching real users' data. Never copy production data to
your laptop just to test.

### Look at your data — 🟡 Soon

Open your database's table viewer (Supabase has one built in) every so often.
Duplicate rows, empty columns, prices of 0 and broken links between tables are
early warnings of bugs that the app's screens hide.

---

## 7. Copy-paste database prompts

### Design before building

```
Before creating any tables, propose a database design for this app based on
SPEC.md. Show each table with its columns and types, primary keys, foreign
keys and which rule each one uses on delete (cascade, set null or restrict),
unique and check constraints, indexes, and which column says who owns each
row. Use random IDs (UUID), integer cents for money, and timestamptz in UTC
for times. Explain each choice in plain words. Don't create anything yet.
```

### Review an existing database

```
Review this project's database schema and migrations. Look for: money stored
as floating-point numbers; times without time zones; lists of IDs stored in
one column instead of a join table; facts stored twice; missing NOT NULL,
UNIQUE, foreign key or CHECK constraints; foreign keys that cascade deletes
where data should be kept; missing indexes on foreign keys and filtered
columns; tables of private data with no owner column or without Row Level
Security. For each problem, show the safe migration to fix it.
```

### Change a live column safely

```
I need to [rename / change the type of / remove] the column [name] in
[table], which already has real data. Plan it as an expand-and-contract
change: add the new column, deploy code that writes to both columns, backfill
the old rows, switch reads to the new column, then remove the old column in a
later migration. Show each migration and the order of deploys.
```

---

Next: [Logins, done right](07-logins-done-right.md)
