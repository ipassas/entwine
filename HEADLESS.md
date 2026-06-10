# Deploying Entwine as a Wix Headless site

This repo is now an **Astro 5** project (the format the Wix CLI requires —
Astro 6 is not yet supported by Wix). All 12 pages live in `src/pages/` as
routes; static files (CSS, fonts, images) live in `public/`. The build output
has been verified byte-equivalent to the original hand-coded HTML pages.

The path below uses **Wix-managed headless**: Wix hosts the site, handles
OAuth, environment variables, and infrastructure. Docs:
<https://dev.wix.com/docs/go-headless/wix-managed-headless/get-started/connect-an-existing-astro-project>

> ⚠️ Run these on **your machine** — the Wix CLI needs a browser for OAuth
> login, so they can't run from a cloud sandbox.
>
> Prerequisites: Node.js v20.11+ and Git. Be logged into your Wix account in
> the browser.

## 1. Clone / pull this branch and install

```bash
git pull
npm install
```

Sanity check — the site should run locally before any Wix involvement:

```bash
npm run dev          # http://localhost:4321
```

## 2. Link the project to Wix (one-time)

From the repo root:

```bash
npm create @wix/new@latest -- headless link --business-name "Entwine"
```

This will (after a browser login prompt):

- Provision a **new Wix business + site** for the headless project (it will
  appear in your Wix sites list — it does not touch the existing `entwine`
  editor site).
- Add `wix.config.json` (site id + private-app id) to the repo root.
- Add the `@wix/astro` integration to `astro.config.mjs` and set
  `output: 'server'`.
- Replace `package.json` scripts so `dev`, `build`, `preview`, and `release`
  route through the `wix` CLI.

Commit the changes it makes (`wix.config.json`, `astro.config.mjs`,
`package.json`) so the link survives on every machine.

## 3. Develop / preview

```bash
npx wix dev          # local dev with hot reload + Wix APIs available
```

## 4. Publish

```bash
npx wix build
npx wix release      # pushes to Wix and publishes; prints the live URL
```

Re-run these two commands any time you want to ship changes.

## 5. (Later) point the real domain at it

The headless project starts on a `*.wixstudio.com` / Wix Pages URL. When
you're ready, connect your custom domain (e.g. `entwine.club`) to the headless
project from the Wix dashboard → Settings → Domains. The old `entwine` editor
site keeps working until you switch the domain over.

## Calling Wix APIs later (forms, CMS, bookings…)

Once linked, any Wix JavaScript SDK module works inside Astro front matter,
e.g.:

```bash
npm install @wix/members
```

```astro
---
import { members } from "@wix/members";
const memberList = await members.listMembers();
---
```

## Editing pages after the port

- **Copy / markup** — edit the page in `src/pages/<name>.astro` (same HTML as
  before, one file per page).
- **Styling** — `public/styles.css`, same as always.
- **Images / fonts** — `public/assets/`.
- Internal links are root-absolute now: `/restaurants`, `/pricing`, etc.
  (not `restaurants.html`).
