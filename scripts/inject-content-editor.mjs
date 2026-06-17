/*
 * Adds the site-content.js include (and the backend URL config) to every page,
 * just before </body>. Re-runnable: it skips pages that already have it.
 *
 *   node scripts/inject-content-editor.mjs
 *
 * To point the site at your deployed backend, edit CONTENT_API_BASE below (or
 * set window.CONTENT_API_BASE another way) and re-run.
 */
import { readdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PAGES_DIR = path.join(__dirname, "..", "src", "pages");

// Where your deployed content backend lives. Leave as-is for local testing.
const CONTENT_API_BASE = "http://localhost:8787";

const MARKER = "site-content.js";
const SNIPPET =
  `<script is:inline>window.CONTENT_API_BASE = ${JSON.stringify(CONTENT_API_BASE)};</script>\n` +
  `<script is:inline src="/site-content.js?v=1" defer></script>\n`;

async function* walk(dir) {
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) yield* walk(full);
    else if (entry.name.endsWith(".astro")) yield full;
  }
}

let changed = 0;
let skipped = 0;
for await (const file of walk(PAGES_DIR)) {
  let html = await readFile(file, "utf8");
  if (html.includes(MARKER)) { skipped++; continue; }
  const idx = html.lastIndexOf("</body>");
  if (idx === -1) {
    console.warn("No </body> in", file, "— skipped");
    continue;
  }
  html = html.slice(0, idx) + SNIPPET + html.slice(idx);
  await writeFile(file, html);
  changed++;
  console.log("injected:", path.relative(PAGES_DIR, file));
}
console.log(`\nDone. ${changed} page(s) updated, ${skipped} already had it.`);
