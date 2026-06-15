# Moving Entwine onto Wix Headless (live at entwine.club)

Goal: the site is **served by Wix itself** at `entwine.club` — no iframe, no
`github.io` visible anywhere — and the **forms are part of Wix** (submissions
land in the Wix dashboard and trigger an email to `info@entwine.club`).

The code is already prepared for this. The steps below run **on your machine**
(the Wix CLI opens a browser to log in, which can't happen in the cloud
sandbox). Nothing here changes the current live site until you publish.

---

## 1. Link the repo to Wix Headless (one-time)

```bash
git pull
npm install
npm create @wix/new@latest -- headless link --business-name "Entwine"
```

This logs into Wix in your browser and then:

- creates a **Headless project** under your Wix account (separate from the
  existing editor site — it won't touch it),
- adds `wix.config.json` (site id + app id),
- adds the `@wix/astro` integration to `astro.config.mjs` and sets
  `output: 'server'`,
- rewrites the `package.json` scripts to run through the `wix` CLI.

Commit the files it changes:

```bash
git add wix.config.json astro.config.mjs package.json package-lock.json
git commit -m "Link Wix Headless"
```

## 2. Create the two forms in Wix

In the Wix dashboard for the Headless project → **Forms**, create:

**Careers application** — add fields and set each field's **Field Key** exactly:
`role`, `name`, `email`, `phone`, `links`, `note`
(optionally add a **File upload** field for the CV — see §6).

**Newsletter** — one field, key `email`.

Copy each form's **Form ID** (Form settings → ⋯ → "Copy ID" / the URL).

> The field keys above must match — they're what the site sends. If you'd
> rather use different keys, tell me and I'll remap `src/scripts/wix-forms.js`.

## 3. Get the Headless client id

Dashboard → **Settings → Headless** (OAuth apps) → create/copy the
**Client ID** for a public (visitor) OAuth app.

## 4. Add the env vars

Create `.env` in the repo root (it's already git-ignored):

```
PUBLIC_WIX_CLIENT_ID=<your headless client id>
PUBLIC_WIX_CAREERS_FORM_ID=<Careers application form id>
PUBLIC_WIX_NEWSLETTER_FORM_ID=<Newsletter form id>
```

With these set, the careers form and the insights newsletter submit straight
into Wix Forms. Without them, the site silently falls back (careers drafts an
email), so local/staging builds keep working.

## 5. Send applications to your inbox (Wix Automation)

Dashboard → **Automations** → New:
- Trigger: **Form submission** → *Careers application*
- Action: **Send email** to `info@entwine.club` (include the submitted fields).

Do the same for *Newsletter* if you want a notification, or connect it to
**Marketing → Contacts** so subscribers land in your audience.

## 6. CV upload (final wiring)

Add a **File upload** field to the Careers form and send me its field key. I'll
switch the CV from the email fallback to a real Wix upload (the SDK uploads the
file and attaches it to the submission), so everything — details **and** CV —
lands in Wix. Until then, selecting a CV also opens a pre-filled email to
`info@entwine.club` so the file still reaches you.

## 7. Preview, then publish

```bash
npx wix dev                 # local preview with Wix APIs + forms working
npx wix build && npx wix release
```

`release` prints the live Wix URL. Submit a test application and confirm it
appears under **Forms → Submissions** and that the automation email arrives.

## 8. Point entwine.club at the Headless site (and drop the iframe)

In the Wix dashboard → **Domains**, connect **entwine.club** to the Headless
project. Then remove the old **Custom Embed / iframe** from the Studio site (or
move the domain off it). From this point `entwine.club` is served by Wix
Headless directly:

- no `iframe`, no `ipassas.github.io` in the address bar, network tab, or
  "view source",
- the in-app QR code and every link resolve to `entwine.club` automatically
  (they derive from the current origin),
- canonical/OpenGraph URLs already point at `entwine.club`.

## 9. Retire GitHub Pages (optional)

Once Headless is live you can disable the `Deploy to GitHub Pages` workflow
(`.github/workflows/deploy-pages.yml`) or keep it as a private staging mirror.
It is no longer the public site.

---

### What's already done in the repo

- `src/scripts/wix-forms.js` — Wix Forms submission helper (lazy-loads the Wix
  SDK; inert until `PUBLIC_WIX_CLIENT_ID` is set).
- Careers application form → submits to Wix Forms, with the email draft as a
  fallback.
- Insights newsletter → submits to Wix Forms when configured.
- `@wix/sdk` + `@wix/forms` added as dependencies.

### What only you can do (browser / dashboard / DNS)

- The `wix login` / `wix release` (CLI needs a browser).
- Creating the forms, the client id, the automation, and connecting the domain.
