# What you actually need as a vibe coder

## First: what the reel is really saying

The reel lists the things professional backend and infrastructure engineers
deal with once software runs for real users, at real scale, under real attack.
It's half fair warning and half joke.

- **The fair part:** AI can build an app that works on your laptop without you
  understanding any of this, and a few of these gaps can cost you money, your
  users' data, or your whole database.
- **The joke part:** a lot of the list (Kubernetes, leader election, the Saga
  pattern, multi-region, chaos engineering) are problems of companies with big
  teams and millions of users. Plenty of professional developers rarely touch
  them, and you don't need them to ship a good app.

So you don't need to learn 111 things. You need to learn **about 12 things
well**, **about 25 things roughly**, and know the rest exist.

---

## Tier 1: before you put anything online

*If your app has logins, payments, or anyone else's data, do these first.*
Three of them (marked "not in the reel") are missing from the reel entirely but
matter more than most of what's on it.

1. **Git and GitHub** *(not in the reel)*: your undo button.
   Commit every time something works, and push to GitHub. When the AI breaks
   something, you can go back.

2. **Frontend vs backend**: know what's public.
   Anything that runs in the browser can be read by anyone. See
   [Start here](00-start-here.md).

3. **Secrets management**: keep keys out of your code.
   Keys live in `.env` (which is in `.gitignore`) and in your host's settings.
   None in frontend code. If one leaks, replace it at the provider right away.

4. **Authentication**: don't build login yourself.
   Use Supabase Auth, Clerk, Auth0, Firebase Auth or Better Auth.

5. **Authorization / access control** *(not in the reel by name; the #1
   real-world risk)*: being logged in isn't enough.
   Every route and database rule must check that the user owns the thing
   they're asking for. On Supabase, turn on Row Level Security for every
   table, with policies that check ownership; on Firebase, write real Security Rules. Then test it: log in as user
   A and try to read user B's data by changing an ID.

6. **Data validation on the server**: never trust what arrives.
   Ask your AI to validate every input with Zod or Pydantic.

7. **SQL injection and XSS**: the two classic attacks.
   Know the red flags (see the [checklist](15-checklist-and-ai-prompts.md#red-flags-stop-and-ask-why))
   and ask your AI to check for them.

8. **HTTPS**: already on with modern hosts. Just never turn it off.

9. **Rate limiting**: on login, signup, password reset, and **every endpoint
   that costs you money** (AI calls, emails, SMS).

10. **Backups**: switched on, restored at least once as a test, and out of
    reach of AI agents.

11. **Spending caps and billing alerts**: on every service that bills you:
    hosting, database, AI APIs, email.

12. **Separate development and production** *(not in the reel)*.
    Use a separate database and separate keys while building. Never let an AI
    agent run commands against production.

The reel also leaves out whole areas a launch depends on: securing your AI
features (prompt injection), testing, payments, privacy law, free-tier limits
on launch day, and maintenance afterwards. Those are in
[Beyond the reel](06-beyond-the-reel.md).

Do these 12 and you've covered the disasters that most often hit vibe-coded
apps: leaked keys, open databases, surprise bills and lost data.

---

## Tier 2: once real people are using it

Learn these as you go. Each one is explained in
[the reel, explained](04-the-reel-explained.md).

- **Seeing what's happening:** logging, metrics, error tracking (Sentry),
  monitoring, an uptime monitor with a health check, alerts, observability.
- **The database:** migrations and schema versioning, indexing, N+1 queries,
  connection pooling (if you're on serverless), transactions for multi-step
  changes, race conditions.
- **Talking to other services:** timeouts, retries, exponential backoff,
  webhooks, idempotency. These move to Tier 1 if you take payments.
- **Speed and cost:** caching and cache invalidation, a CDN for images and
  uploads, latency, serverless limits, cold starts.
- **Shipping safely:** CI (automatic checks before deploy), rollbacks,
  semantic versioning, lockfiles, dependency hygiene.
- **Scheduled work:** cron jobs.
- **The outside world:** DNS for your custom domain and email (SPF, DKIM,
  DMARC).
- **More security:** CORS, CSRF, SSRF (if your server fetches URLs users give
  it), IAM and least privilege, JWT rotation (your auth provider should handle
  it).
- **Real-time** (only if you need it): WebSockets, or Server-Sent Events for
  streaming AI answers.
- **When things go wrong:** a half-page disaster recovery plan, an incident
  playbook, and postmortems.

---

## Tier 3: know the word, learn it when it's your problem

| Terms | You'll need them when... |
|---|---|
| Docker | you move from Vercel/Netlify to your own server |
| Kubernetes, Helm Charts, liveness & readiness probes | you have a team running many services (maybe never) |
| Load balancing, reverse proxies, API gateways | you run your own servers instead of a platform |
| Vertical & horizontal scaling, autoscaling, backpressure | one server can't keep up with your traffic |
| Message queues, pub/sub, event-driven architecture, dead letter queues | you have background jobs that take minutes, or several services |
| Optimistic & pessimistic locking | two users can grab the same last item, or edit the same thing |
| Read replicas, replication, sharding, partitioning, failover, multi-region | one database can't keep up, or downtime costs real money |
| Distributed transactions, Saga pattern, distributed locks, leader election | your data is spread across several services or databases |
| CAP theorem, eventual consistency, network partitions, clock skew | same as above; also handy in interviews |
| Feature flags, blue-green, canary and rolling deployments | you have enough users that a bad release really hurts |
| SLOs, SLIs, error budgets, on-call, distributed tracing | you have a team and paying customers with expectations |
| P99 / tail latency, throughput, query optimization | you start measuring performance seriously |
| TCP vs UDP, HTTP/2 & HTTP/3, gRPC | you build real-time games, video, or internal services |
| Infrastructure as Code, Terraform, build caching | your setup is too big to click together by hand |
| WAF, DDoS protection, encryption at rest, edge caching | mostly provided by your host already; just check the settings |
| Memory leaks, garbage collection, thread safety | your server's memory keeps growing, or you write code that runs several threads |
| Chaos engineering | you run a large system that must not go down |

---

## What your AI is likely to miss, and why

Knowing the words matters because your AI mostly does what you ask, and rarely
volunteers the rest.

- **It tries to make the error go away**, sometimes by removing a safety check:
  turning off Row Level Security, allowing every website through CORS,
  commenting out an auth check, or catching an error and ignoring it.
- **It only sees what you show it.** It doesn't know your production setup,
  your traffic, or your bill.
- **Its knowledge lags behind library versions**, so it writes code for an
  older version than the one you installed.
- **It sounds certain.** "This is now secure" is a claim, not proof. Ask it to
  show what it checked, or to attack its own code.
- **It rarely adds what you didn't ask for:** rate limits, indexes, backups,
  alerts, tests.

The fix is cheap: know the words, then ask. [Vibe coding well](02-vibe-coding-well.md)
covers the working habits that stop most of these problems before they start,
[How vibe-coded apps break](12-how-vibe-coded-apps-break.md) shows what happens
when they're missing, and the [checklist and copy-paste prompts](15-checklist-and-ai-prompts.md)
check for them.

---

## A learning path, if you want to go deeper

Go one step at a time, and practice each step on a tiny app of your own.

1. **How the web works:** [Start here](00-start-here.md), then the "Learn web
   development" section of [MDN Web Docs](https://developer.mozilla.org/).
2. **Your project and Git:** [Reading your project](01-reading-your-project.md)
   for the files, terminal and Git words; then commit, push, branch, and go
   back to an old version on purpose. MIT's free
   [Missing Semester](https://missing.csail.mit.edu/) course goes deeper on Git
   and the terminal.
3. **Working with AI:** [Vibe coding well](02-vibe-coding-well.md). Write a
   spec and a rules file for your next project before any code.
4. **Logins and permissions:** read [Logins, done right](08-logins-done-right.md),
   build a tiny app with login, then work through its test list: prove that
   user A can't see user B's data.
5. **Databases:** [Your database, explained](07-your-database.md), then basic
   SQL, and doing one real backup *and restore*.
6. **Security basics:** read the [OWASP Top 10](https://top10.owasp.org/2025/en/),
   then try the free hands-on labs at
   [PortSwigger Web Security Academy](https://portswigger.net/web-security)
   (start with SQL injection and XSS).
7. **Running it for real:** error tracking, an uptime monitor, a billing
   alert, and rolling back a deploy on purpose so you know how.
8. **If your app uses AI:** [Building AI features](09-building-ai-features.md),
   especially tokens and cost, and testing AI output.
9. **After that:** pick Tier 2 items as you run into them, and take the quiz
   on the one-page version of this guide to check what stuck.

A good way to learn any single term is to ask your AI:

```
Explain [term] using my own project as the example. What is it, does my app
need it right now, and what is the smallest change that would handle it?
Then quiz me with 3 questions.
```

---

Next: [Beyond the reel: launching and running your app](06-beyond-the-reel.md)
