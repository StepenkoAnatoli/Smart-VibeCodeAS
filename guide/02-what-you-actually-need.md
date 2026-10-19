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

So you don't need to learn 100 things. You need to learn **about 12 things
well**, **about 20 things roughly**, and know the rest exist.

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
   Use Supabase Auth, Clerk, Auth0, Firebase Auth or Auth.js.

5. **Authorization / access control** *(not in the reel by name; the #1
   real-world risk)*: being logged in isn't enough.
   Every route and database rule must check that the user owns the thing
   they're asking for. On Supabase, turn on Row Level Security for every
   table; on Firebase, write real Security Rules. Then test it: log in as user
   A and try to read user B's data by changing an ID.

6. **Data validation on the server**: never trust what arrives.
   Ask your AI to validate every input with Zod or Pydantic.

7. **SQL injection and XSS**: the two classic attacks.
   Know the red flags (see the [checklist](03-checklist-and-ai-prompts.md#red-flags-stop-and-ask-why))
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

Do these 12 and you've covered the disasters that most often hit vibe-coded
apps: leaked keys, open databases, surprise bills and lost data.

---

## Tier 2: once real people are using it

Learn these as you go. Each one is explained in
[the reel, explained](01-the-reel-explained.md).

- **Seeing what's happening:** logging, error tracking (Sentry), monitoring,
  an uptime monitor with a health check, alerts, observability.
- **The database:** migrations and schema versioning, indexing, N+1 queries,
  connection pooling (if you're on serverless), transactions for multi-step
  changes.
- **Talking to other services:** timeouts, retries, exponential backoff,
  webhooks, idempotency. These move to Tier 1 if you take payments.
- **Speed and cost:** caching and cache invalidation, latency, serverless
  limits, cold starts.
- **Shipping safely:** CI (automatic checks before deploy), knowing how to roll
  back, semantic versioning, lockfiles, dependency hygiene.
- **The outside world:** DNS for your custom domain and email (SPF, DKIM,
  DMARC).
- **More security:** CSRF, SSRF (if your server fetches URLs users give it),
  IAM and least privilege.
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
| Message queues, pub/sub, event-driven architecture, dead letter queues | you have background jobs that take minutes, or several services |
| Optimistic & pessimistic locking | two users can grab the same last item, or edit the same thing |
| Read replicas, replication, partitioning, failover, multi-region | one database can't keep up, or downtime costs real money |
| Distributed transactions, Saga pattern, distributed locks, leader election | your data is spread across several services or databases |
| CAP theorem, eventual consistency, network partitions, clock skew | same as above; also handy in interviews |
| Feature flags, blue-green, canary and rolling deployments | you have enough users that a bad release really hurts |
| SLOs, error budgets, on-call, distributed tracing | you have a team and paying customers with expectations |
| P99 / tail latency, throughput, query optimization | you start measuring performance seriously |
| TCP vs UDP, HTTP/2 & HTTP/3, gRPC | you build real-time games, video, or internal services |
| Infrastructure as Code, Terraform, build caching | your setup is too big to click together by hand |
| WAF, DDoS protection, encryption at rest | mostly provided by your host already; just check the settings |
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

The fix is cheap: know the words, then ask. The
[checklist and copy-paste prompts](03-checklist-and-ai-prompts.md) do exactly
that.

---

## A learning path, if you want to go deeper

Go one step at a time, and practice each step on a tiny app of your own.

1. **How the web works:** [Start here](00-start-here.md), then the "Learn web
   development" section of [MDN Web Docs](https://developer.mozilla.org/).
2. **Git basics:** commit, push, branch, and going back to an old version.
   MIT's free [Missing Semester](https://missing.csail.mit.edu/) course covers
   Git and the terminal.
3. **Logins and permissions:** build a tiny app with login, then prove that
   user A can't see user B's data.
4. **Databases:** tables, basic SQL, indexes, migrations, and doing one real
   backup *and restore*.
5. **Security basics:** read the [OWASP Top 10](https://top10.owasp.org/2025/en/),
   then try the free hands-on labs at
   [PortSwigger Web Security Academy](https://portswigger.net/web-security)
   (start with SQL injection and XSS).
6. **Running it for real:** error tracking, an uptime monitor, a billing
   alert, and rolling back a deploy on purpose so you know how.
7. **After that:** pick Tier 2 items as you run into them.

A good way to learn any single term is to ask your AI:

```
Explain [term] using my own project as the example. What is it, does my app
need it right now, and what is the smallest change that would handle it?
Then quiz me with 3 questions.
```

---

Next: [Pre-launch checklist and copy-paste AI prompts](03-checklist-and-ai-prompts.md)
