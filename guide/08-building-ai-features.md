# Building AI features: what the API docs assume you know

Many vibe-coded apps *are* AI apps: a chat assistant, a summarizer, a writing
helper, a tool that reads documents. Calling an AI model takes a few lines of
code, and AI tools write those lines happily. What they rarely explain is how
these features cost money, fail, drift and get abused. This chapter covers
that. The security side is in [Beyond the reel](05-beyond-the-reel.md#1-your-ai-features).

It applies to any provider (OpenAI, Anthropic, Google and others); names of
specific settings vary a little between them.

Labels as elsewhere: 🔴 **Now**, 🟡 **Soon**, ⚪ **Later**.

## Contents

1. [How an AI API call actually works](#1-how-an-ai-api-call-actually-works)
2. [Tokens and cost](#2-tokens-and-cost)
3. [Choosing and pinning a model](#3-choosing-and-pinning-a-model)
4. [Prompts that live in your app](#4-prompts-that-live-in-your-app)
5. [Getting answers your code can use](#5-getting-answers-your-code-can-use)
6. [Long conversations and memory](#6-long-conversations-and-memory)
7. [Answering from your own data (RAG)](#7-answering-from-your-own-data-rag)
8. [Letting the AI take actions (tools and agents)](#8-letting-the-ai-take-actions-tools-and-agents)
9. [When the AI provider has a bad day](#9-when-the-ai-provider-has-a-bad-day)
10. [Testing AI features (evals)](#10-testing-ai-features-evals)
11. [Copy-paste prompts for AI features](#11-copy-paste-prompts-for-ai-features)

---

## 1. How an AI API call actually works

### Every call starts from zero — 🔴 Now

**What it is:** Your server sends the model a list of **messages** and gets
one reply back. Usually that's a *system* message (your instructions), then the
conversation so far: *user* messages and the model's earlier *assistant*
replies. The model remembers nothing between calls. To continue a chat, the
**whole conversation** has to be read again on every call. Usually your app
resends it; some APIs can store it for you, but you're still billed for all of
it as input each time.

**Picture it:** A brilliant consultant with no memory. Each time you ask a
follow-up, you hand over the entire file of everything said so far.

**What it means for you:**

- A chat gets **more expensive with every message**, because each new call
  includes (and bills) all the earlier ones.
- "Memory" across chats is something *you* build, by saving and resending
  information. It isn't a property of the model.
- The call must happen on your **server**, with the key in server-side
  environment variables (see *The API key in the browser* in
  [How vibe-coded apps break](10-how-vibe-coded-apps-break.md#security)).

---

## 2. Tokens and cost

### What a token is — 🔴 Now

**What it is:** Models read and write text in small pieces called **tokens**.
In English a token is roughly ¾ of a word on average; other languages, code
and unusual words often take more tokens. Images, audio and files are converted
to tokens too.

**What it means for you:** You pay per token, separately for:

- **Input tokens:** everything you send, including the system prompt, the
  conversation history and any documents.
- **Output tokens:** everything the model writes. Output usually costs several
  times more per token than input.

Every API response reports how many tokens it used. **Do:** Save those numbers
with each request, so you can see cost per user and per feature.

### Keeping cost under control — 🔴 Now

- Set a **maximum output length** on every call (`max_tokens` on Claude,
  `max_completion_tokens` or `max_output_tokens` on OpenAI; the name varies by
  provider and API).
- Give each user a **quota** (messages per day or tokens per month), and
  rate-limit anonymous use.
- **Trim history:** send the last few messages plus a short summary, not the
  whole chat forever (see section 6).
- Use a **smaller, cheaper model** for simple jobs (classifying, extracting,
  short replies) and the big one only where quality matters.
- **Cache** answers to repeated identical questions. Many providers also offer
  *prompt caching*: a discount when the start of your prompt (like a long
  system prompt or document) is repeated across calls.
- For work that doesn't need an instant answer (overnight summaries, bulk
  tagging), providers' **batch** options are usually cheaper.
- Set billing alerts in the provider's dashboard, and a hard spending limit
  where offered. Prepaid credits with auto-recharge turned off also work as a
  cap. (A Google Cloud "budget" only alerts; it doesn't stop spending.)

---

## 3. Choosing and pinning a model

### Bigger isn't always better — 🟡 Soon

Providers offer a range: large models (smartest, slowest, most expensive) down
to small ones (fast and cheap). Many app features (sorting support tickets,
pulling a date out of an email, writing a one-line title) work well on small
models at a fraction of the cost. **Do:** Start with a mid-sized model, then try
the task on a smaller one using your test set (section 10) and keep the
cheapest model that passes.

### Pin the version — 🟡 Soon

Model names often come in two forms: a moving *alias* that silently points to
the newest version, and a specific, dated version. Aliases can change behavior
overnight. **Do:** Use a specific version in production, keep the model name in
one config setting, and re-run your tests before switching. Watch for
retirement notices; old versions are eventually switched off (see *Model
changes and retirements* in [Beyond the reel](05-beyond-the-reel.md#1-your-ai-features)).

---

## 4. Prompts that live in your app

### The system prompt is product code — 🟡 Soon

**What it is:** The instructions your app sends with every request: who the
assistant is, what it should and shouldn't do, what format to answer in, and
often a few examples.

**What it means for you:**

- Treat it like code: keep it in a file in your repo, change it deliberately,
  and test changes (section 10).
- Be specific. "Answer in 2–3 sentences, in the user's language, and say
  'I don't know' when the answer isn't in the provided documents" beats "be
  helpful and concise".
- Examples of good answers ("few-shot" examples) often help more than more
  rules.
- **Assume users can see it.** People can usually coax a model into revealing
  its system prompt, so never put secrets, keys or private business data in it.
- **Rules in the prompt aren't security.** "Only discuss our product" and
  "don't reveal other users' data" can be talked around. Enforce anything that
  matters in code (see *Prompt injection* in
  [Beyond the reel](05-beyond-the-reel.md#1-your-ai-features)).

### Temperature and randomness — ⚪ Later

Many APIs have a *temperature* setting: lower means more predictable answers,
higher means more varied ones. Use low values for extraction and
classification and moderate values for creative writing. Even at low settings,
the same input can give slightly different answers, so never assume an exact
reply.

---

## 5. Getting answers your code can use

### Structured output — 🔴 Now (if your code uses the answer)

**What it is:** When your code needs to *use* the answer (save fields to the
database, show a list, decide what to do next), free text is fragile. Most
providers can make the model reply in an exact JSON shape you define, often
called *structured outputs*, or through *tool calling*. (Plain *JSON mode* only
promises valid JSON, not your shape.)

**What it means for you:** Ask your AI to use the provider's structured-output
feature with a schema, and **still validate** the result with Zod or Pydantic
before using it: values can be missing, wrong or made up. Decide what happens
when validation fails: retry once, then show a friendly error.

### Streaming — 🟡 Soon

**What it is:** Showing the answer word by word as the model writes it, instead
of waiting for the whole thing. It usually uses Server-Sent Events.

**What it means for you:** Streaming makes a 20-second answer feel fast, and it
helps with serverless time limits (see *Serverless Limits* in
[the reel, explained](03-the-reel-explained.md#5-operations--resilience)). Handle a
stream that stops halfway, and record token usage when the stream finishes.

### Showing AI text safely — 🔴 Now

Model output is untrusted text: render it as plain text or sanitized Markdown,
never as raw HTML, and never run it as code or SQL (see *AI output is untrusted
input* in [Beyond the reel](05-beyond-the-reel.md#1-your-ai-features)).

---

## 6. Long conversations and memory

### The context window — 🟡 Soon

**What it is:** Each model has a maximum amount of text it can take in one call
(its *context window*), counted in tokens. Long chats and big documents
eventually hit it. Before that, quality can drop: details in the middle of a
very long prompt are easier for the model to miss.

**Do:**

- Keep the last several messages word for word, and replace older ones with a
  running summary.
- Don't paste whole documents into every message; retrieve only the relevant
  parts (section 7).
- If you build "memory" (facts the assistant remembers about a user), store it
  in your database, let users see and delete it, and include only what's
  relevant in each call.

---

## 7. Answering from your own data (RAG)

### Retrieval-augmented generation — 🟡 Soon

**What it is:** Letting the AI answer from *your* documents (help articles,
product data, a user's uploaded files) without pasting everything into every
prompt. It works in three steps:

1. **Split** documents into small passages (*chunks*).
2. Turn each chunk into an **embedding**: a list of numbers representing its
   meaning, made by an *embedding model*. Store them in a database that can
   search by meaning: a *vector database*, or Postgres with the `pgvector`
   extension (available on Supabase).
3. For each question, **find** the most similar chunks and send only those to
   the model with the question: "answer using these passages".

**Picture it:** Instead of making the consultant read the whole library, a
librarian brings the five most relevant pages.

**What it means for you:**

- **Permissions apply to search too.** Retrieval must only return chunks the
  current user is allowed to see. Otherwise one customer's question pulls
  another customer's documents into the answer. Filter by owner in the search
  itself.
- **Show sources.** Link the passages used, so users can check the answer.
- **Tell the model what to do when the answer isn't there:** say so, rather
  than guessing.
- **Retrieved text can contain prompt injection,** especially from uploads or
  web pages.
- **Keep it fresh.** When a document changes or is deleted, update or delete its
  chunks.

---

## 8. Letting the AI take actions (tools and agents)

### Tool calling — 🟡 Soon

**What it is:** You describe functions your app offers (for example
`search_orders` or `create_ticket`), and the model can reply with a request to
call one, with arguments. **Your code** decides whether to run it, runs it, and
sends the result back. An *agent* is a loop of these steps until the task is
done. (*MCP* is a standard way to package tools so different AI apps can use
them.)

**What it means for you:**

- The model only *asks*; your code acts. That's where you enforce everything.
- **Check permissions** for every tool call as the current user, exactly as you
  would for a normal request.
- **Validate the arguments,** since the model can produce wrong or harmful
  ones.
- Require **confirmation** before anything irreversible: sending, deleting,
  paying.
- **Limit the loop:** a maximum number of steps and a budget per task, so an
  agent can't run up a bill going in circles.
- Log every tool call, so you can see what happened.

---

## 9. When the AI provider has a bad day

### Rate limits, timeouts and outages — 🟡 Soon

AI providers have rate limits (errors with status `429`), slow periods and
occasional outages. **Do:**

- Retry `429` and `5xx` errors with exponential backoff. Many official SDKs do
  this already, so check before adding your own.
- Set a timeout, and show the user a clear message instead of an endless
  spinner.
- For important features, consider a **fallback**: a second model or provider
  to use when the first fails. Test that the fallback's answers are acceptable.
- Watch your provider's status page, and point your own status page at it.

---

## 10. Testing AI features (evals)

### Build a test set — 🟡 Soon

**What it is:** Because AI output varies, you can't test it like normal code
("the answer must equal X"). Instead you keep an **eval set**: 20–100 realistic
inputs, including tricky and adversarial ones, each with a description of what a
good answer must do ("mentions the refund deadline", "refuses to give medical
dosages", "returns valid JSON with a date").

**What it means for you:** Run the set every time you change the prompt, the
model or the retrieval, and compare results before shipping. Check simple
things with code (valid JSON, required fields, length). For judgment calls, you
can read the answers yourself or use another model as a grader with a clear
checklist (*LLM-as-judge*), spot-checking it. Add every bad answer a user
reports to the set, so it can't come back.

### Watch it in production — 🟡 Soon

Log, for each request: model and prompt version, token counts, cost, how long
it took, and whether it failed. Add a thumbs-up/down button. Be careful with
what you store: prompts and answers often contain personal data, so keep them
only as long as needed and say so in your privacy policy.

---

## 11. Copy-paste prompts for AI features

### Review an AI feature

```
Review every place this app calls an AI model. For each call: is it on the
server with the key in server-side env vars? Is there a maximum output
length, a per-user quota and a rate limit? Is the model version pinned in one config setting?
Is the whole conversation resent every time, and how could we trim it? Is
output validated (schema + Zod/Pydantic) before use, and rendered safely? Are
token counts and cost logged per request? Is there a timeout, retry with
backoff and a friendly error? List problems with file and line, and fixes.
```

### Estimate the cost

```
Estimate what this AI feature costs. Using the model and prompts in the code,
estimate input and output tokens for a typical request and for a long
conversation, and the cost per request, per active user per month, and at
1,000 users. Then suggest the three changes that would cut cost most without
hurting quality, with how much each would save.
```

### Build an eval set

```
Create an eval set for [feature]: 30 realistic test inputs, including edge
cases, tricky phrasings and prompt-injection attempts, each with what a good
answer must and must not do. Write a script that runs them all against the
current prompt and model, checks what can be checked automatically (valid
JSON, required fields, length), and saves the answers to a file I can review.
```

---

Next: [Debugging with AI: how to get unstuck](09-debugging-with-ai.md)
