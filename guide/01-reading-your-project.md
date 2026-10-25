# Reading your project: the files, commands and words you'll see

Your AI writes the code, but you still live inside the project: you see its
files, paste its errors, run its commands and approve its changes. This
chapter is the vocabulary for that. You don't need to write any of it; you need
to recognize it, so you can tell when something looks wrong and ask better
questions.

The examples use a typical JavaScript/TypeScript web project (React, Next.js,
Vite, Supabase), because that's what most AI tools build by default. Python
projects use different names for the same ideas.

## Contents

1. [The files in a typical project](#1-the-files-in-a-typical-project)
2. [The terminal in ten commands](#2-the-terminal-in-ten-commands)
3. [Git in plain words](#3-git-in-plain-words)
4. [Reading a diff](#4-reading-a-diff)
5. [Words for the code itself](#5-words-for-the-code-itself)
6. [Words for how apps talk to each other](#6-words-for-how-apps-talk-to-each-other)
7. [Words for your tools](#7-words-for-your-tools)
8. [Words for where code runs](#8-words-for-where-code-runs)

---

## 1. The files in a typical project

| File or folder | What it is | Should you touch it? |
|---|---|---|
| `package.json` | The project's ID card: its name, the packages it uses (*dependencies*) and its commands (*scripts*, like `dev` and `build`) | Read it; let the AI or `npm` change it |
| `package-lock.json` (or `pnpm-lock.yaml`, `yarn.lock`) | The *lockfile*: the exact version of every package installed | Never edit by hand; always commit it |
| `node_modules/` | Thousands of downloaded packages. Huge, rebuilt by `npm install` | Never edit, never commit (it should be in `.gitignore`) |
| `.env`, `.env.local` | Your secrets and settings for this computer. Variables starting with `NEXT_PUBLIC_`, `VITE_`, `REACT_APP_` or `EXPO_PUBLIC_` are copied into the frontend and are public | Edit yourself; **never commit**; never give a secret a public prefix |
| `.env.example` | A copy of `.env` with the values blanked out, so others know which settings exist | Commit it; keep it in sync |
| `.gitignore` | The list of files Git should never save (`.env`, `node_modules`) | Check that `.env` is in it |
| `src/` | "Source": where most of your app's code lives | This is what the AI edits |
| `app/` or `pages/` | In Next.js, each folder or file here is a page or route of your site. `app/dashboard/page.tsx` is the page at `/dashboard` | AI edits it |
| `app/api/` or `pages/api/`, any `route.ts`, and any file starting with `"use server"` | Backend code that runs on the server: API endpoints, and Next.js *Server Actions*. Anyone can call these directly, not just your buttons | AI edits it; check every route and every server action for login and permission checks |
| `components/` | Reusable pieces of the interface: buttons, cards, forms | AI edits it |
| `lib/` or `utils/` | Shared helper code: database connections, formatting | AI edits it |
| `public/` | Files served as they are: images, icons, `robots.txt` | Anything here is public |
| `supabase/migrations/`, `prisma/schema.prisma`, `drizzle/` | Your database structure and its history of changes | Read every new migration before it runs on production |
| `README.md` | The project's front page: what it is and how to run it | Keep it current; it helps you *and* your AI |
| `CLAUDE.md`, `AGENTS.md`, `.cursor/rules` | Standing instructions your AI tool reads every session | Write your project rules here (see [Vibe coding well](02-vibe-coding-well.md)) |
| `tsconfig.json`, `next.config.ts` (or `.js`/`.mjs`), `vite.config.ts`, and `tailwind.config.js` in older Tailwind projects (Tailwind v4 keeps its settings in your main CSS file) | Settings for TypeScript, your framework and your styling | Rarely; ask before changing |
| `.github/workflows/` | Automatic checks that run on GitHub (CI) | Keep them; don't let AI delete failing ones |
| `Dockerfile` | Instructions to package the app as a container | Only if you deploy with Docker |
| `.next/`, `dist/`, `build/` | Generated output of a build | Never edit, never commit |

Files whose names start with a dot (`.env`, `.gitignore`) are hidden by default
on Mac and Linux. In VS Code and Cursor they show up in the file list anyway.

---

## 2. The terminal in ten commands

The terminal (also called the command line, shell or console) is a text window
where you type commands instead of clicking. Your AI tool often runs these for
you; this is so you know what it's doing.

| Command | What it does |
|---|---|
| `cd my-app` | Move into the folder `my-app` (*change directory*). `cd ..` goes up one level |
| `ls` (Mac/Linux) or `dir` (Windows) | List the files in the current folder |
| `npm install` | Download every package listed in `package.json` into `node_modules/`. Run it after cloning a project or when packages change |
| `npm install some-package` | Add a new package to the project. **Check the package is real and popular first** |
| `npm run dev` | Start the app on your computer in development mode. It prints an address like `http://localhost:3000`; open it in your browser |
| `npm run build` | Make the production version. Errors here are the errors your host will hit when deploying |
| `Ctrl+C` | Stop whatever is running in the terminal (like the dev server) |
| `git status` | Show which files changed since your last commit |
| `git add .` then `git commit -m "message"` | Save a checkpoint of everything you changed, with a description. (On Mac/Linux you can join them with `&&`; the older Windows PowerShell doesn't accept that) |
| `git push` | Send your commits to GitHub |

Two habits: read a command before you approve it (especially anything with
`rm`, `sudo`, `--force`, `reset`, `drop` or `deploy`), and copy errors from the
terminal as text when you report them.

---

## 3. Git in plain words

Git is the history of your project; GitHub is a website that stores that
history online and adds collaboration tools.

- **Repository (repo):** your project folder, plus its whole history.
- **Commit:** a saved checkpoint, with a message describing the change. You can
  always go back to any commit.
- **Branch:** a parallel line of work. `main` is usually what's live. You make a
  branch to try something without touching `main`.
- **Push / pull:** send your commits to GitHub / bring down commits from
  GitHub.
- **Clone:** download a full copy of a repo to your computer.
- **Pull request (PR):** a request to merge one branch into another, with a
  page showing every change for review. Hosts like Vercel build a preview of
  each one.
- **Merge:** combine a branch's changes into another branch.
- **Merge conflict:** two branches changed the same lines differently, and Git
  needs a human (or your AI) to choose.
- **Revert:** a new commit that undoes an earlier one. Safe, because it keeps
  history.
- **Reset / force push:** rewrite history. Powerful and dangerous; on a shared
  branch it can destroy other people's work. Don't approve these casually.
- **`.gitignore`:** files Git never saves.

The one rule: **commit every time something works.** Then any mistake, yours
or the AI's, is one step from undone.

---

## 4. Reading a diff

A *diff* is the list of changes between two versions. Your AI tool, GitHub and
pull requests all show changes this way:

```diff
  export async function getOrder(orderId, user) {
-   const order = await db.orders.find(orderId)
+   const order = await db.orders.find({ id: orderId, userId: user.id })
    return order
  }
```

- Lines starting with `-` (usually red) were **removed**.
- Lines starting with `+` (usually green) were **added**.
- Lines with neither are unchanged context.

You don't need to understand every line. Check three things:

1. **Which files changed.** Does the list match what you asked for? A request to
   change a button's color shouldn't touch the database or login code.
2. **How big it is.** A one-line request that comes back as 400 changed lines
   deserves a question.
3. **What was removed.** Deleted checks, deleted tests and deleted error
   handling are the changes that hurt later.

The example above is a good change, by the way. It adds a check that the order
belongs to the logged-in user, which is exactly the *Broken Access Control*
fix.

---

## 5. Words for the code itself

- **Variable:** a named box holding a value: `const price = 10`. `const`
  can't be reassigned; `let` can.
- **Function:** a named, reusable set of steps: `function addTax(price) { ... }`.
  *Calling* it runs it. The values you pass in are *arguments* or *parameters*;
  what comes out is the *return value*.
- **String, number, boolean:** text (`"hello"`), numbers (`42`), and true/false.
- **Array:** an ordered list: `["a", "b", "c"]`.
- **Object:** a group of named values: `{ name: "Ana", plan: "pro" }`. Each name
  is a *key* or *property*.
- **`null` and `undefined`:** "nothing here". Most "Cannot read properties of
  undefined" errors come from code expecting something that turned out to be
  nothing.
- **Import / export:** how one file uses code from another file or from a
  package: `import { useState } from "react"`.
- **If / else:** run code only when a condition is true.
- **Loop:** repeat code for each item (`for`, `.map()`, `.forEach()`). A database
  call inside a loop is the *N+1 Queries* problem.
- **Async / await, promise:** some things take time (network, database). `await`
  means "wait for this to finish". A missing `await` is a classic AI bug: the
  code moves on before the data arrives.
- **Error / exception:** something went wrong. `throw` raises one, and
  `try { } catch { }` handles one. An empty `catch` hides errors.
- **Type:** what kind of value something is. TypeScript checks types before the
  code runs, which catches many mistakes early. `any` switches that checking
  off.
- **Component (React):** a reusable piece of interface, written as a function
  that returns what to show. Names start with a capital letter: `<ProfileCard />`.
- **Props:** values passed into a component, like settings.
- **State:** data a component remembers and that changes the screen when it
  changes (`useState`).
- **Hook:** a React helper whose name starts with `use` (`useState`,
  `useEffect`). A `useEffect` that changes its own inputs can run in an endless
  loop, sometimes calling a paid API every time.
- **Comment:** a note in the code that doesn't run: `// like this`.

---

## 6. Words for how apps talk to each other

- **API:** the set of requests a program accepts. Your backend has one; Stripe
  and OpenAI have theirs.
- **Endpoint (or route):** one address in an API, like `/api/orders`.
- **Request / response:** the question and the answer.
- **HTTP methods:** the verb of a request. `GET` reads, `POST` creates, `PUT`
  or `PATCH` updates, `DELETE` deletes. A `GET` should never change data.
- **JSON:** the text format most APIs use: `{ "name": "Ana", "plan": "pro" }`.
- **Headers:** extra information sent with a request, such as login tokens
  (`Authorization`) and content type.
- **Query string:** the part of a URL after `?`: `/search?q=shoes&page=2`.
- **Status code:** the number saying how a request went (200 OK, 404 not found,
  500 server crashed). See the table in [Debugging with AI](11-debugging-with-ai.md#2-reading-an-error-message).
- **REST:** the most common style of API, built from URLs and HTTP methods.
  GraphQL and gRPC are other styles.
- **SDK:** a ready-made package for using someone's API from your code, like
  Stripe's or OpenAI's library.
- **API key:** a password for an API. Secret keys stay on the server.
- **Webhook:** a service calling *your* endpoint when something happens.

---

## 7. Words for your tools

- **Programming language:** JavaScript and TypeScript (most web apps), Python
  (data, AI, many backends), and SQL (databases).
- **Framework:** a full structure your app is built inside, which decides where
  files go and how pages work: Next.js, Remix, SvelteKit, Django, Rails.
- **Library:** a tool your code calls when it wants: React (interfaces), Zod
  (validation), date-fns (dates).
- **Package (dependency):** a library you install with a package manager.
- **Package manager:** the tool that installs packages: `npm`, `pnpm`, `yarn`
  for JavaScript, `pip` or `uv` for Python.
- **Node.js:** the program that runs JavaScript outside the browser, on
  servers and on your computer.
- **React:** the most common library for building interfaces from components.
- **Next.js:** a framework on top of React that adds pages, routing and
  backend code in one project.
- **Vite:** a fast tool that runs and builds frontend projects. Many AI app
  builders produce Vite + React projects.
- **Tailwind CSS:** a styling system using short class names right in the
  markup: `className="p-4 text-lg"`.
- **ORM / query builder:** a library that talks to the database for you, so the
  code doesn't contain raw SQL: Prisma, Drizzle, the Supabase client.
- **Supabase / Firebase:** hosted backends that bundle a database, logins, file
  storage and more.
- **Linter / formatter:** tools that flag likely mistakes (ESLint) and tidy
  layout (Prettier).
- **IDE / editor:** where code is written and read: VS Code, and AI-first
  editors such as Cursor.

---

## 8. Words for where code runs

- **Client vs server:** the user's browser vs your computer in the cloud. See
  [Start here](00-start-here.md).
- **Localhost:** "this computer". `http://localhost:3000` is the app running on
  your own machine; nobody else can open it.
- **Port:** the number after the colon (`:3000`, `:5173`). It lets one computer
  run several programs that each accept connections.
- **Environment:** a place the app runs, with its own settings and data:
  *development* (your laptop), *preview* or *staging* (a test copy online),
  *production* (the real thing).
- **Build:** turning your source code into the optimized files that actually
  run. *Bundling* combines many files into a few.
- **Runtime:** the program actually running your code (a browser, Node.js,
  an edge runtime). Code that works in one can fail in another.
- **CSR, SSR, SSG:** three ways to make a page. *Client-side rendering* builds
  it in the browser with JavaScript. *Server-side rendering* builds it on the
  server for each visit. *Static generation* builds it once, ahead of time.
- **Server and client components:** in Next.js, components run on the server
  unless the file starts with `"use client"` **or is imported by a file that
  does**. Server components can use secrets; client components, and everything
  they import, are public. Ask your AI to add `import "server-only"` to files
  that use secrets, so a mistake fails the build instead of leaking.
- **Middleware** (called `proxy.ts` in Next.js 16 and later): code that runs
  before every request (or a matching set), often used to redirect people who
  aren't logged in. It's not enough on its own: every route and server action
  must still check who is asking.
- **Edge:** running code on servers close to the user (on the CDN). It's fast,
  but often with fewer features and tighter limits than a normal server.
- **Hydration:** the moment a server-rendered page "comes alive" in the browser.
  "Hydration mismatch" errors mean the server and browser produced different
  HTML.

---

Next: [Vibe coding well: working with AI tools](02-vibe-coding-well.md)
