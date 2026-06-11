# Entwine site assets

Drop replacement images into the matching subfolder and they appear on the site —
no code changes needed. Keep the **same file name** as listed below.

```
assets/
├── badges/    Store badges (official artwork — already provided)
├── screens/   App screenshots shown inside the phone / preview frames
├── photos/    Hero & content photography
└── team/      Team member headshots
```

## badges/  — store badges
| File | Used for |
| --- | --- |
| `app-store.svg`   | Apple "Download on the App Store" badge |
| `google-play.svg` | Google "Get it on Google Play" badge |

These are the official badges. Every store button on the site renders these two
files at one shared height, so they stay aligned. Replace a file to update the
badge everywhere at once. SVG is preferred; PNG also works if you update the
`src` in `public/store-link` rendering.

## screens/  — app screenshots  (PNG)
Drop a PNG named exactly as below. Until a file exists, a framed placeholder with
a caption is shown. Recommended: portrait PNGs, ~1080×2160 (or 4:5 for previews).

| File | Where it shows |
| --- | --- |
| `app-showcase.png` | Home page — app preview panel |
| `wl-pairing.png`   | Wine Lovers — phone hero (pairing screen) |
| `wl-tap-1.png`     | Wine Lovers — "Choose your dish" tap |
| `wl-tap-2.png`     | Wine Lovers — "Set your filters" tap |
| `wl-tap-3.png`     | Wine Lovers — "Discover the pairing" tap |

## photos/  — content photography  (JPG)
File name = the image's `data-img` name + `.jpg`. Example: a slot named
`download-hero` loads `photos/download-hero.jpg`. If a file is missing, a stock
fallback is fetched automatically. A few of the named slots:
`index-*`, `download-hero`, `download-bg`, `pricing-hero`, `restaurants-hero`,
`partners-hero`, `invest-hero`, `careers-hero`, `insights-hero`, `insight-1..4`,
`ab-hero`, `ab-story`, `tl-hero`, `wl-hero`, `tool-*`.

## team/  — headshots  (JPG)
File name = the person's slot id + `.jpg`. Any image slot named `team-*`
resolves here.

| File |
| --- |
| `team-daniel.jpg` |
| `team-claire.jpg` |
| `team-andrew.jpg` |
| `team-krisztina.jpg` |
| `team-will.jpg` |
