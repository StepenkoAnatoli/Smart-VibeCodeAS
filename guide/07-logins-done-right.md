# Logins, done right

"Use an auth provider" is the right first step (see *JWT / OAuth* in
[the reel, explained](03-the-reel-explained.md#1-security)), but it's not the
whole job. Providers handle passwords and tokens; your app still decides what
happens *around* login: where users are sent afterwards, which user a request
belongs to, what changing an email does, and who counts as an admin. Most
account takeovers in small apps happen in that "around".

Labels as elsewhere: 🔴 **Now**, 🟡 **Soon**, ⚪ **Later**.

## Contents

1. [Two questions, always](#1-two-questions-always)
2. [Ways to log in](#2-ways-to-log-in)
3. [Mistakes around login](#3-mistakes-around-login)
4. [Changing email, password and account details](#4-changing-email-password-and-account-details)
5. [Sessions](#5-sessions)
6. [Two-factor login](#6-two-factor-login)
7. [Test it like an attacker](#7-test-it-like-an-attacker)
8. [Copy-paste login prompts](#8-copy-paste-login-prompts)

---

## 1. Two questions, always

Every request your server handles must answer two separate questions:

1. **Authentication: who is this?** Proven by a valid session or token from
   your auth provider.
2. **Authorization: are they allowed to do *this*, to *this* record?** Decided
   by your code and your database rules.

Logins answer the first question only. Most security bugs in vibe-coded apps
answer the first and forget the second (see *Broken Access Control* in
[the reel, explained](03-the-reel-explained.md#1-security)).

---

## 2. Ways to log in

### Choosing login methods — 🟡 Soon

| Method | How it works | Good to know |
|---|---|---|
| **Email + password** | The classic | Users reuse passwords, so you need rate limits and ideally a check against known leaked passwords. Let your provider store them |
| **Magic link / one-time code** | You email a link or a 6-digit code; no password | Simple and no passwords to leak, but the account is only as safe as the user's email, and emails can be slow or land in spam |
| **Social login** ("Continue with Google / Apple / GitHub") | Another company vouches for the user (OAuth / OpenID Connect) | Fast sign-up. iOS apps that offer third-party social logins must also offer an equivalent privacy-friendly option, such as Sign in with Apple (check Apple's current review guidelines) |
| **Passkeys** | The phone or laptop proves who you are with a fingerprint, face or PIN, using a key that never leaves the device | The most phishing-resistant option and increasingly supported by auth providers. Offer it alongside another method |

**What it means for you:** Two or three methods is plenty. Every extra method
is another flow to test and another way in.

---

## 3. Mistakes around login

### Trusting the user ID the browser sends — 🔴 Now

**What it is:** The frontend sends `{ userId: "42", ... }` in the request, and
the server uses that ID to decide whose data to read or change.

**Picture it:** A bank teller who asks your name and believes it, instead of
checking your card.

**What it means for you:** Anyone can edit a request and put in someone else's
ID. Every route and server action must take the user from the **verified
session or token**, never from the request body, the URL or a hidden form
field. Some libraries have one
function that only *reads* the session stored in the browser and another that
*verifies* it with the auth server. Supabase's docs, for example, distinguish
`getSession()` from `getUser()`. In server code, use the verifying one.

### Roles the user can edit themselves — 🔴 Now

**What it is:** The app stores `role: "admin"` somewhere the user can change.
A classic example with Supabase is putting it in `user_metadata`, which
signed-in users can update about themselves through the normal client
library. (`app_metadata` can only be set from the server.)

**What it means for you:** Store roles and plans where only your server can
write: `app_metadata`, or your own `roles` table protected by Row Level
Security. Then test it by trying to make yourself an admin from the browser.

### Redirect URLs and "next" links — 🔴 Now

**What it is:** After login, users are sent back to your app, often to the page
in a `?next=` or `redirect_to=` parameter. Your auth provider also keeps a list
of allowed callback URLs.

**The two mistakes:**

- **Wrong allowed URLs.** Login works on `localhost` but fails on your real
  domain or preview deploys, because only `localhost` is on the provider's
  list. Or, worse, the list allows any URL with a wildcard.
- **Open redirects.** Your app sends users to *whatever* address is in
  `?next=`. Attackers send links like
  `yourapp.com/login?next=https://evil.example` that start on your real domain
  and end on a fake page asking for a password.

**Do:** Keep the allowed callback list exact (your production domain and your
preview pattern). Only redirect to paths on your own site (starting with a
single `/`), never to full URLs from a parameter.

### Unverified emails — 🔴 Now

**What it is:** Signing in or linking accounts based on an email address that
nobody has proven they own.

**What it means for you:** If sign-up doesn't verify the email, someone can
register *your future customer's* address first, and some apps then merge the
real owner into the attacker's account when they sign up later. **Do:** Require
email verification before an account can do anything meaningful. Only link a
social login to an existing account when the provider confirms the email is
verified, and when in doubt, ask the user to log in to the existing account
first.

### Password reset — 🟡 Soon

Reset links must expire (within an hour or so), work once, and be long and
random. The "forgot password" page should say the same thing whether or not
the email has an account. After a reset, sign out the user's other sessions,
since an attacker may be logged in. Your auth provider does most of this; check
it if your AI built a custom flow.

### Guessing passwords at scale — 🟡 Soon

Attackers try leaked email-and-password pairs from other sites on yours
(*credential stuffing*). **Do:** Rate-limit login per account and per IP
address, add a CAPTCHA after a few failures, turn on your provider's
leaked-password protection if it has one, and offer two-factor login.

---

## 4. Changing email, password and account details

### Ask again before sensitive changes — 🔴 Now

**What it is:** Changing the email, password, two-factor settings or payout
details should require the user to prove it's still them: enter the current
password, use a fresh code, or have logged in within the last few minutes.

**Why:** Otherwise, anyone who gets brief access to a logged-in session (a
borrowed laptop, a stolen token) can change the email to theirs, reset the
password, and own the account permanently.

**Do:** Ask again before sensitive changes, send a notice to the **old** email
address when the email or password changes, and make an email change take
effect only after the new address is confirmed.

### Deleting an account — 🟡 Soon

When a user deletes their account, end all their sessions, revoke their
tokens, cancel their subscription, and handle their data according to your
retention rules (see [Your database, explained](06-your-database.md#5-deleting-things)).

---

## 5. Sessions

### How long logins last — 🟡 Soon

A **session** is the period a user stays logged in after proving who they are.
It's usually kept going with short-lived tokens that are refreshed
automatically (see *JWT Rotation* in [the reel, explained](03-the-reel-explained.md#1-security)).
**Do:** Pick deliberate lifetimes: long for a notes app, shorter for anything
with money or admin power. Give users a "log out of all devices" button, and
make sure logging out actually ends the session on the server.

### Where tokens live in the browser — 🟡 Soon

Tokens are kept either in **cookies** set with `HttpOnly` (JavaScript can't
read them, so XSS can't steal them directly) or somewhere JavaScript *can* read
them: browser storage such as `localStorage`, or cookies without `HttpOnly`.
Popular providers including Supabase and Firebase use the readable kind on
purpose, because the browser side needs the token; that's normal, so don't try
to change it. It means preventing XSS is what protects your users' sessions. For server-rendered apps (like Next.js), use
your provider's server/cookie helpers so the server can verify the user.

---

## 6. Two-factor login

### Offer two-factor login — 🟡 Soon (🔴 for admin accounts)

**What it is:** A second proof after the password: a code from an
authenticator app, a passkey, or a security key.

**What it means for you:** Turn it on for **your own** admin accounts today,
and offer it to users once you hold anything valuable. Authenticator apps and
passkeys are much stronger than SMS codes, which can be stolen by moving
someone's phone number to a new SIM (*SIM swapping*). Give users recovery
codes so a lost phone doesn't mean a lost account.

---

## 7. Test it like an attacker

### The login test list — 🔴 Now

Before launch, try each of these yourself, with two test accounts (A and B):

- Logged in as A, change an ID in a URL or request to B's ID. You should be
  blocked.
- Edit a request so it says you're user B. The server should ignore it.
- Try to make yourself an admin by editing your own profile or metadata.
- Open an admin API route as a normal user.
- Use a password reset link twice, and after an hour.
- Log out, press Back, and reload. You should still be logged out.
- Change A's email without entering the password.
- Use `?next=https://example.com` on your login page. It should stay on your
  site.
- Sign up with an email you don't control. It should stay unverified and
  limited.
- Log in on two devices, log out of all devices on one, and reload the other.

---

## 8. Copy-paste login prompts

### Audit the login setup

```
Audit how this app handles login and identity. For every server route and
server action: where does it get the current user from? Flag any place that
trusts a user ID, email or role sent by the browser instead of the verified
session. List where roles and plans are stored and whether the user can edit
them. Check redirect handling after login for open redirects, the allowed
callback URLs, email verification, password reset, re-authentication before
email/password changes, logout, and session lifetime. Show each problem with
file and line, and the smallest fix.
```

### Add a sensitive-change check

```
Before a user can change their email, password, two-factor settings or
payment details, require them to re-enter their password (or use a fresh
one-time code). After any of these changes, email the old address. Use our
auth provider's built-in features where they exist, and show me what you
changed.
```

---

Next: [Building AI features](08-building-ai-features.md)
