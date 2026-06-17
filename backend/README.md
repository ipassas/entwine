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

The backend is a standard Node app — host it anywhere that runs Node 18+
(Render, Railway, Fly.io, a small VPS, etc.). Example with **Render**:

1. Push this repo to GitHub (already done).
2. On Render: **New ➜ Web Service**, pick this repo.
3. Settings:
   - **Root Directory:** `backend`
   - **Build Command:** `npm install`
   - **Start Command:** `npm start`
   - **Environment ➜ Add:** `ADMIN_PASSWORD = BErlin123!@#`
   - (Recommended) add a **persistent disk** mounted at `/data` and set
     `DATA_DIR = /data` so your edits survive restarts/redeploys.
4. Deploy. You'll get a URL like `https://entwine-editor.onrender.com`.

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
