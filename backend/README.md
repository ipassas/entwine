# Entwine Text Editor (content backend)

A tiny password-protected backend that lets you change the text of the Entwine
website from any device — without touching code. You log in, pick a page, edit
the words, and hit **Save**. The live site updates automatically.

- **Password:** `BErlin123!@#` (change via the `ADMIN_PASSWORD` env var)
- **Stores:** edits in a simple JSON file (`backend/data/content.json`)
- **No database to set up.**

---

## How it fits together

```
 Visitor opens a page  ──►  site-content.js  ──►  GET /api/content   ──►  shows your edited text
 You open the panel    ──►  /  (login)       ──►  POST /api/admin/*  ──►  saves your edits
```

1. Every page on the website loads `public/site-content.js`. It reports the
   text on that page to the backend and applies any edits you've saved.
2. The admin panel (served at `/`) is where you log in and edit the text.

---

## Run it locally (to try it out)

```bash
cd backend
npm install
npm start
```

Open **http://localhost:8787**, log in with the password, and you're in.

For the website to talk to it locally, run the site (`npm run dev` in the repo
root) — `site-content.js` is already pointed at `http://localhost:8787`.
Open a few pages so they register, then they'll appear in the panel (or click
**Sync site** and enter `http://localhost:4321`).

---

## Put it online (so you can edit from anywhere)

### One-click deploy to Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/ipassas/entwine)

1. Click the button above.
2. Log in to Render with your **GitHub** account (free, no credit card).
3. Render reads `render.yaml`, creates the service, and clicks Deploy for you.
4. After ~1–2 minutes you'll get a URL like
   `https://entwine-text-editor.onrender.com`. That's your editor. Open it,
   log in with the password, done.

> **Persistence note (important):** the **free** Render instance has a
> temporary disk, so your saved edits reset whenever the app goes to sleep and
> wakes up. Fine for trying it out. To keep edits **permanently**, upgrade the
> service to Render's **Starter** plan (~$7/mo) and add a disk — the exact
> steps are commented at the bottom of `render.yaml`.

### Any other Node host (Railway, Fly.io, a VPS…)

The backend is a standard Node 18+ app:
- **Root directory:** `backend`
- **Build:** `npm install`
- **Start:** `npm start`
- **Env:** `ADMIN_PASSWORD=BErlin123!@#` (and `DATA_DIR` pointed at a
  persistent volume so edits survive restarts).
- You'll get a URL like `https://entwine-editor.onrender.com`.

Then point the website at that URL:

1. Edit `scripts/inject-content-editor.mjs` → set
   `CONTENT_API_BASE = "https://entwine-editor.onrender.com"`.
2. Run `node scripts/inject-content-editor.mjs` (it updates the config on every
   page; safe to re-run).
3. Commit & deploy the site as usual.

Now open your backend URL on your phone or laptop, log in, click **Sync site**
(enter your live site address, e.g. `https://ipassas.github.io/entwine`), and
every page's text becomes editable.

---

## Using the panel

- **Pages** (left): every page that has been visited/synced.
- Click a page to see all its text fields. **Original** text is shown above each
  box; type your replacement and press **Save changes**.
- **Reset** restores the original wording for a single field.
- Edits are per-field, so leaving a box untouched keeps the original copy.

### What's editable?
Any plain-text heading, paragraph, button, link, list item, etc. (Text that's
mixed with inline formatting in the same element, images, and icons aren't
captured — those still live in the page source.)

---

## Environment variables

| Variable         | Default                     | Purpose                                   |
|------------------|-----------------------------|-------------------------------------------|
| `ADMIN_PASSWORD` | `BErlin123!@#`              | Login password for the panel              |
| `PORT`           | `8787`                      | Port to listen on (hosts often set this)  |
| `DATA_DIR`       | `backend/data`              | Where `content.json` is stored            |
| `SESSION_SECRET` | derived from password       | Signs login tokens                        |
