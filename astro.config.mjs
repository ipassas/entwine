// @ts-check
import { defineConfig } from "astro/config";

import react from "@astrojs/react";
import wix from "@wix/astro";
import cloudProviderFetchAdapter from "@wix/cloud-provider-fetch-adapter";
const isBuild = process.env.NODE_ENV == "production";

// Kept deliberately minimal. Running `npm create @wix/new@latest -- headless link`
// will extend this config with the @wix/astro integration, server output, and
// the Wix fetch adapter.
export default defineConfig({
  integrations: [react(), wix()],
  ...(isBuild && { adapter: cloudProviderFetchAdapter({}) }),

  image: {
    domains: ["static.wixstatic.com"]
  },

  output: "server"
});