# Entwine — Marketing site

A faithful, hand-coded build of the **Entwine Website** Figma design
(file `QTN5HNupb4aM5NyiuohELz`). Now packaged as an **Astro 5** project so it
links directly to **Wix Headless** (see `HEADLESS.md`), while every page stays
the same plain HTML + CSS it always was — Astro is only the wrapper that
serves and deploys it.

## Files

| Path | Purpose |
|------|---------|
| `src/pages/*.astro` | One file per page — the same HTML markup as before, served at `/<name>` (e.g. `src/pages/pricing.astro` → `/pricing`) |
| `public/styles.css` | All styling. Design tokens (colours, fonts, spacing) live in `:root` at the top |
| `public/assets/` | Fonts + drop replacement images here (see note below) |
| `public/image-slot.js` | `<image-slot>` web component (team avatars with initials fallback) |
| `src/pages/brand-styles.astro` | Living style guide — logo, colour, type scale, components, grid, motion |
| `HEADLESS.md` | Step-by-step: link this repo to Wix Headless and publish |
| `build_pages.py` | **Retired.** Generated the original root-level HTML pages; the source of truth is now `src/pages/` |

## Preview locally

```bash
npm install
npm run dev        # http://localhost:4321
```

## Editing

- **Colours / fonts / spacing** — edit the CSS variables in `:root` at the top of `public/styles.css`
  (e.g. `--gold: #b8a86a`, `--ink: #0a0a0a`).
- **Copy** — edit directly in `src/pages/<page>.astro`; sections are commented (`<!-- HERO -->`, etc.).
- **Fonts** — Outfit only, self-hosted from `public/assets/` via `@font-face` (no external font CDNs).
- **Links** — internal links are root-absolute routes: `/restaurants`, `/pricing`, `/tools#audit`.
- Keep inline `<script is:inline>` / `<style is:inline>` attributes as-is — they stop Astro
  from reprocessing the hand-written scripts and styles.

## Pages

Home (`index`), `restaurants`, `wine-lovers`, `tools`, `pricing`, `download`,
`about`, `insights`, `careers`, `partners`, `invest`, and the `brand-styles`
style guide.

Navigation is a shared **mega menu** (categorised: Tools mega-panel + Company
dropdown), with a mobile burger that opens an accordion. It lives in each
page's `<header class="nav">`.

## Images (named assets + Unsplash fallback)

Images use a small helper: each `<img data-img="NAME" data-kw="keywords" data-w data-h>`
first tries `/assets/NAME.jpg`; if that's missing it falls back to a relevant
**Unsplash** image (then LoremFlickr). **To use your own, drop a file at
`public/assets/NAME.jpg`** — no code change needed.

⚠️ A few home-page backgrounds still point at **temporary Figma asset URLs that
expire ~7 days after export** — migrate them to the named-asset system above.
Every image sits on a solid fallback colour, so the layout never breaks if an
image fails to load.

## Current hosting (temporary)

Every merge to the main branch auto-builds and publishes the site to the
`gh-pages` branch (GitHub Pages → `https://ipassas.github.io/entwine/`).
A full-viewport iframe embed on the **entwine** Wix Studio site
(Custom Embed `d6e62675-8ee7-44a2-ada0-ce05073897eb`) shows it at
`https://ipassasdesign.wixstudio.com/entwine`.

> One-time setup: GitHub repo → **Settings → Pages** → Source:
> *Deploy from a branch* → Branch: `gh-pages` / `/ (root)` → Save.

This is the "for now" setup — the proper long-term path is Wix Headless below.

## Deploying to Wix (proper / long-term)

⚠️ **entwine.club serves the Wix Headless release, not the GitHub Pages build.**
Merging to `main` does NOT update entwine.club by itself — a Wix release must
run. Either run it locally (below), or add a `WIX_API_KEY` repository secret
(Wix dashboard → Account Settings → API Keys, on the account that owns the
headless project) and the `Release to Wix` workflow releases automatically on
every push to `main`.

Follow `HEADLESS.md` — short version:

```bash
npm create @wix/new@latest -- headless link --business-name "Entwine"   # one-time, on your machine
npx wix dev        # local dev with Wix APIs
npx wix build && npx wix release   # publish
```
