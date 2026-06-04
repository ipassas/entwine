# Deploying Entwine as a Wix Headless site (Wix CLI)

Our site is currently **static** (`index.html`, `restaurants.html`, `brand-styles.html`, `styles.css`, `assets/`).
Wix Headless hosts a **JS-framework app** (default **Next.js** starter) under your Wix domain, with Wix APIs
(OAuth) available for data. So the static pages get folded into a headless project.

> ⚠️ Run these on **your machine** — the Wix CLI needs Node 18+, network, and a browser for OAuth login.
> They cannot run from the cloud sandbox.

## 1. Authenticate
```bash
npx @wix/cli login
```

## 2. Scaffold a headless project
Follow the starter at <https://dev.wix.com/docs/go-headless>. Create it next to this repo, e.g. `entwine-headless/`.

## 3. Bring in the front-end
Two options:

**A. Quickest — serve our files as static assets** (good for a pure marketing site):
```bash
cp styles.css index.html restaurants.html brand-styles.html entwine-headless/public/
cp -r assets entwine-headless/public/
```
Then route the framework's home to `public/index.html` (or rename routes to avoid clashing with the
framework's own `/`). Relative links (`restaurants.html`, `styles.css`, `assets/...`) keep working from `/public`.

**B. Cleanest — port pages into framework routes** (recommended for SEO + data later):
Convert each page into a route/component. **I can do this conversion in this repo** (Astro or Next) so it
drops straight into the headless project — just say the word and which framework.

## 4. Install + pull env
```bash
cd entwine-headless
npm install
npx @wix/cli env pull
```

## 5. Build, preview, release
```bash
npx @wix/cli build
npx @wix/cli release
```

## Recommended sequencing
We're still designing pages. Porting to a framework now means editing every page twice. Suggested plan:
1. Keep building + approving page designs in this static repo (previewable via the current Wix embed).
2. Once the page set is approved, I port them all into a Wix Headless (Astro/Next) project in one pass.
3. You run the CLI steps above to deploy under your Wix domain.
