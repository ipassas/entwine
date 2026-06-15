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

## 2. Create the Newsletter form in Wix

Careers applications now go straight to your inbox (the Apply button opens the
visitor's email app addressed to `info@entwine.club` with the job title as the
subject — no Wix form needed). So the only Wix form to create is:

**Newsletter Subscribe** — one email field.

Copy its **Form ID** (Form settings → ⋯ → "Copy ID" / the URL) and the email
field's **field key**, and send them to me (or set them in `.env` below). If
the field key isn't `email`, set `PUBLIC_WIX_NEWSLETTER_EMAIL_KEY`.

## 3. Get the Headless client id

Dashboard → **Settings → Headless** (OAuth apps) → create/copy the
**Client ID** for a public (visitor) OAuth app.

## 4. Add the env vars

Create `.env` in the repo root (it's already git-ignored):

```
PUBLIC_WIX_CLIENT_ID=<your headless client id>
PUBLIC_WIX_NEWSLETTER_FORM_ID=<Newsletter Subscribe form id>
PUBLIC_WIX_NEWSLETTER_EMAIL_KEY=email   # only if the field key isn't "email"
```

With these set, the careers form and the insights newsletter submit straight
into Wix Forms. Without them, the site silently falls back (careers drafts an
email), so local/staging builds keep working.

## 5. Send applications to your inbox (Wix Automation)

Careers applications already arrive as a normal email to `info@entwine.club`
(with the CV attached by the applicant). For the **Newsletter Subscribe** form,
add an Automation if you want a notification, or connect it to
**Marketing → Contacts** so subscribers land in your audience.

## 6. Careers / CV

Careers is intentionally email-based: clicking **Apply** on a role (or **Send
us your CV**) opens the visitor's email client to `info@entwine.club` with the
job title as the subject and a prefilled body — they attach their CV and send.
No Wix form or file-upload wiring required.

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
