// Rewrites root-absolute URLs in the built site so it can be served from a
// subpath (e.g. GitHub Pages at /entwine). Usage: node scripts/rebase.mjs /entwine
import { readFileSync, writeFileSync, readdirSync, statSync } from "node:fs";
import { join } from "node:path";

const base = process.argv[2];
if (!base || !base.startsWith("/") || base.endsWith("/")) {
  console.error("Usage: node scripts/rebase.mjs /subpath");
  process.exit(1);
}

function walk(dir) {
  return readdirSync(dir).flatMap((name) => {
    const p = join(dir, name);
    return statSync(p).isDirectory() ? walk(p) : [p];
  });
}

let changed = 0;
for (const file of walk("dist")) {
  if (!/\.(html|js|css)$/.test(file)) continue;
  const before = readFileSync(file, "utf8");
  const after = before
    .replaceAll('href="/', `href="${base}/`)
    .replaceAll('src="/', `src="${base}/`)
    .replaceAll("'/assets/", `'${base}/assets/`)
    // collapse the home link: href="/entwine/" stays correct, but guard
    // against double-prefixing if the script ever runs twice
    .replaceAll(`${base}${base}/`, `${base}/`);
  if (after !== before) {
    writeFileSync(file, after);
    changed++;
  }
}
console.log(`rebased ${changed} files onto ${base}`);
