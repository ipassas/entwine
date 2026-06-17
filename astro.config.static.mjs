// @ts-check
import { defineConfig } from "astro/config";

// Static build config used by the GitHub Pages deploy workflow.
//
// The default `astro.config.mjs` is wired for Wix Headless hosting
// (`@wix/astro` integration + `output: "server"`), which needs the Wix CLI and
// a WIX_CLIENT_ID at build time. The pages themselves are plain, fully static
// HTML/CSS, so for the GitHub Pages → Wix iframe path we build them statically
// here with no Wix credentials required. The Wix Headless path is unchanged.
export default defineConfig({
  output: "static",
  image: {
    domains: ["static.wixstatic.com"]
  }
});
