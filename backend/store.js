// Tiny JSON-file "database" for the editable text.
//
// Shape on disk (data/content.json):
// {
//   "pages": {
//     "/pricing": {
//       "title": "Entwine — Pricing",
//       "items": {
//         "0": { "original": "Simple pricing", "override": "Honest pricing" },
//         "1": { "original": "Per location",   "override": null }
//       }
//     }
//   }
// }

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DATA_DIR = process.env.DATA_DIR || path.join(__dirname, "data");
const DATA_FILE = path.join(DATA_DIR, "content.json");

let db = { pages: {} };
let writeTimer = null;

function ensureDir() {
  if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });
}

export function load() {
  try {
    ensureDir();
    if (fs.existsSync(DATA_FILE)) {
      db = JSON.parse(fs.readFileSync(DATA_FILE, "utf8")) || { pages: {} };
      if (!db.pages) db.pages = {};
    }
  } catch (err) {
    console.error("Could not read data file, starting empty:", err.message);
    db = { pages: {} };
  }
}

function persist() {
  // Debounced write so bursts of seeds don't hammer the disk.
  if (writeTimer) clearTimeout(writeTimer);
  writeTimer = setTimeout(() => {
    try {
      ensureDir();
      fs.writeFileSync(DATA_FILE, JSON.stringify(db, null, 2));
    } catch (err) {
      console.error("Failed to write data file:", err.message);
    }
  }, 150);
}

// Record the text that exists on a page. Updates originals, preserves overrides,
// adds any newly-seen fields. Never deletes (a page may render partially).
export function seed(page, title, items) {
  if (!page || !Array.isArray(items)) return;
  const entry = db.pages[page] || { title: title || page, items: {} };
  if (title) entry.title = title;
  for (const it of items) {
    if (!it || it.key == null) continue;
    const key = String(it.key);
    const original = typeof it.original === "string" ? it.original : "";
    const prev = entry.items[key];
    entry.items[key] = {
      original,
      override: prev ? prev.override ?? null : null,
    };
  }
  db.pages[page] = entry;
  persist();
}

// Overrides only (what the public site applies), for one page.
export function overridesFor(page) {
  const entry = db.pages[page];
  const out = {};
  if (!entry) return out;
  for (const [key, item] of Object.entries(entry.items)) {
    if (typeof item.override === "string" && item.override !== item.original) {
      out[key] = item.override;
    }
  }
  return out;
}

// Summary list for the admin panel.
export function pageList() {
  return Object.entries(db.pages)
    .map(([page, entry]) => {
      const items = Object.values(entry.items);
      const edited = items.filter(
        (i) => typeof i.override === "string" && i.override !== i.original
      ).length;
      return { page, title: entry.title || page, total: items.length, edited };
    })
    .sort((a, b) => a.page.localeCompare(b.page));
}

// Full field list for one page (admin editing view).
export function pageDetail(page) {
  const entry = db.pages[page];
  if (!entry) return null;
  const items = Object.entries(entry.items)
    .map(([key, item]) => ({
      key,
      original: item.original,
      override: typeof item.override === "string" ? item.override : null,
    }))
    .sort((a, b) => Number(a.key) - Number(b.key));
  return { page, title: entry.title || page, items };
}

// Save edits for one page. `overrides` is { key: string | null }.
// A null/empty value (or value equal to the original) clears the override.
export function saveOverrides(page, overrides) {
  const entry = db.pages[page];
  if (!entry || !overrides || typeof overrides !== "object") return false;
  for (const [key, value] of Object.entries(overrides)) {
    const item = entry.items[key];
    if (!item) continue;
    if (value == null || value === "" || value === item.original) {
      item.override = null;
    } else {
      item.override = String(value);
    }
  }
  persist();
  return true;
}
