# Start here: how an app actually works (the 5-minute version)

Every word in the reel is about one of the pieces below. Learn these pieces first
and the rest of the list stops looking like a foreign language.

## Your app is a restaurant

| In the restaurant | In your app |
|---|---|
| The customer | The **user**, using a browser or phone |
| The dining room and the menu they see | The **frontend** (also called the *client*): the pages, buttons and JavaScript that run **on the user's device** |
| The waiter who takes orders to the kitchen | The **API**: the agreed way the frontend asks the backend for things |
| The kitchen | The **backend** (also called the *server*): code running on a computer you rent |
| The pantry and fridge | The **database**: where data is stored permanently |
| The street address | The **domain** (`myapp.com`) and **DNS**, which turns that name into a real address |
| Suppliers | **Third-party services**: Stripe (payments), OpenAI or Anthropic (AI), Resend (email), and so on |
| The building and the landlord | **Hosting**: Vercel, Netlify, Render, Railway, Supabase, Firebase, AWS... |

## The one rule that prevents the worst disasters

**Everything in the frontend is public.**

Anyone can open their browser's developer tools and read every line of your
frontend code, including any key or password you put there. The kitchen
(backend) is private. The dining room (frontend) is not.

This one fact explains a lot of the reel:

- why **secrets management** matters (an AI that puts your OpenAI key in React
  code has just published it);
- why you need a backend at all for anything secret or paid;
- why hiding the "Admin" button in the frontend protects nothing: the kitchen
  must check who is asking;
- why, with Supabase or Firebase (where the frontend talks to the database
  directly with a *public* key), the database rules (Row Level Security,
  Security Rules) are the **only** lock on your data.

## What happens when someone opens your app

```
 You type myapp.com
        |
        v
 1. DNS turns "myapp.com" into the server's number address    <- DNS
        |
        v
 2. Browser connects over HTTPS (encrypted)                   <- TLS/SSL
        |
        v
 3. Server sends the frontend (the page and its JavaScript)
        |
        v
 4. You tap "My orders": the frontend calls the API           <- request
        |
        v
 5. Backend checks: who are you? are you allowed to see this? <- authentication + authorization
        |
        v
 6. Backend asks the database for your orders                 <- query
        |
        v
 7. The answer travels back and the page shows it             <- response
                                                                 (time taken = latency)
```

Nearly every term in the reel is about one of these steps going wrong, being
slow, being attacked, or having to handle a million people at once.

## "Works on my laptop" vs "works in production"

- **Local / development**: the app running on your own computer. Only you use
  it. Mistakes are free.
- **Production**: the real, live app on the internet. Real users, real data,
  real money, real attackers.

The reel is a list of things that never show up on your laptop but do show up
in production:

1. **Attackers**: people deliberately sending weird input. *(Security)*
2. **Things breaking**: servers crash, networks drop, a service you depend on
   goes down. *(Reliability, resilience)*
3. **Lots of users**: what works for 10 people chokes at 10,000.
   *(Performance, scaling)*
4. **Change over time**: updating the app without breaking it or losing data.
   *(Deployments, migrations, versioning)*
5. **Money**: every request costs something. *(Cost optimization)*

AI tools are very good at getting an app working on your laptop. They are much
less reliable at that list unless you ask, and you can only ask about things
you know exist. That gap is what this repo is for.

## Words you'll see everywhere

- **Request / response**: the frontend asks (request), the backend answers
  (response).
- **Endpoint** or **route**: one specific "door" in your API, like
  `/api/orders`.
- **Query**: a question to the database ("give me every order for user 42").
- **SQL**: the language most databases speak (Postgres, MySQL, SQLite).
  Supabase is Postgres underneath.
- **Deploy**: put a new version of your app live.
- **Environment variables** (the `.env` file): settings and secrets kept
  outside your code. Careful: any variable whose name starts with
  `NEXT_PUBLIC_`, `VITE_`, `REACT_APP_` or `EXPO_PUBLIC_` is copied into the
  frontend and is public, so never give a secret one of those names.
- **Repository (repo)**: your project folder, tracked by Git.
- **Git**: the full history of your project, and your undo button. It isn't in
  the reel, but it's the most important tool on this page.
- **Server**: just a computer that runs all the time and answers requests.
- **Serverless**: you upload functions and the host runs them only when they're
  called. There are still servers; you just don't manage them.

---

Next: [Reading your project: the files, commands and words you'll see](01-reading-your-project.md)
