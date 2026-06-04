# Entwine — Home page

A faithful, hand-coded build of the **Entwine Website → Home** Figma design
(file `QTN5HNupb4aM5NyiuohELz`, frame `8:1788`). Plain HTML + CSS, no build step,
no framework — so it stays easy to edit and deploys anywhere.

## Files

| File | Purpose |
|------|---------|
| `index.html` | Home page markup + real copy from the Figma comp |
| `styles.css` | All styling. Design tokens (colours, fonts, spacing) live in `:root` at the top |
| `brand-styles.html` | Living style guide — logo, colour, type scale, components, grid, motion. Reference when building new pages |
| `assets/` | Drop replacement images / fonts here (see note below) |

## Preview locally

Open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8000
# then visit http://localhost:8000
```

## Editing

- **Colours / fonts / spacing** — edit the CSS variables in `:root` at the top of `styles.css`
  (e.g. `--gold: #b8a86a`, `--ink: #0a0a0a`).
- **Copy** — edit directly in `index.html`; sections are commented (`<!-- HERO -->`, etc.).
- **Fonts** — Outfit only, self-hosted from `assets/` via `@font-face` (no external font CDNs).

## Images / assets ⚠️

The photographic backgrounds (hero bottle, the wine-glass "Why choose" background,
the phone mockup, the channel-partner texture) currently point at **temporary Figma
asset URLs that expire ~7 days after export**. Before that, download the real exports
from Figma into `assets/` and swap the `src` / `background` URLs in
`index.html` / `styles.css`. Every image sits on a solid fallback colour, so the layout
never breaks if an image fails to load.

The App Store / Google Play badge icons are inline SVG (in the small script at the
bottom of `index.html`) — no external assets needed.

## Deploying to Wix

This is a self-contained static page, so options are:
1. **Wix headless** (Wix CLI) — host this front-end and call Wix APIs for data.
2. **Embed** — drop the markup into a Wix Studio *Embed / Custom Element* block.

Editing then happens in code (this repo), which is the trade-off chosen for
pixel-fidelity to the Figma.

## Pages

- `index.html` — Home
- `restaurants.html` — For Restaurants (built from the wireframe; brand-styled)
- `brand-styles.html` — Web style guide / bible

Navigation is a shared **mega menu** (categorised: Tools mega-panel + Company dropdown), with a mobile burger that opens an accordion. It lives in each page's `<header class="nav">`.

## Images (named assets + Unsplash fallback)

Images use a small helper: each `<img data-img="NAME" data-kw="keywords" data-w data-h>` first tries `assets/NAME.jpg`; if that's missing it falls back to a relevant **Unsplash** image (then LoremFlickr). **To use your own, drop a file at `assets/NAME.jpg`** — no code change needed.

Current named images:

| File to add | Used on | Suggested shot |
|-------------|---------|----------------|
| `assets/restaurants-hero.jpg` | /restaurants hero | Sommelier presenting wine at a table |
| `assets/restaurants-platform.jpg` | /restaurants "what changes" | Wine cellar / tablet in a restaurant |

(Home's hero/why/phone/partners images still use temporary Figma URLs — to be migrated to this same named-asset system.)
