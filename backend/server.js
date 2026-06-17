import express from "express";
import cors from "cors";
import crypto from "node:crypto";
import path from "node:path";
import { fileURLToPath } from "node:url";

import {
  load,
  seed,
  overridesFor,
  pageList,
  pageDetail,
  saveOverrides,
} from "./store.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const PORT = process.env.PORT || 8787;
const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD || "BErlin123!@#";
// Token secret is derived from the password so logins survive restarts.
const SECRET =
  process.env.SESSION_SECRET ||
  crypto.createHash("sha256").update("entwine::" + ADMIN_PASSWORD).digest("hex");

load();

const app = express();
app.use(cors()); // public site fetches from a different origin
app.use(express.json({ limit: "2mb" }));

// ---- auth helpers ---------------------------------------------------------
function makeToken() {
  return crypto.createHmac("sha256", SECRET).update("entwine-admin").digest("hex");
}
const VALID_TOKEN = makeToken();

function timingSafeEqual(a, b) {
  const ba = Buffer.from(String(a));
  const bb = Buffer.from(String(b));
  if (ba.length !== bb.length) return false;
  return crypto.timingSafeEqual(ba, bb);
}

function requireAuth(req, res, next) {
  const header = req.headers.authorization || "";
  const token = header.replace(/^Bearer\s+/i, "");
  if (token && timingSafeEqual(token, VALID_TOKEN)) return next();
  return res.status(401).json({ error: "Unauthorized" });
}

// ---- public API (used by the website) -------------------------------------
app.post("/api/seed", (req, res) => {
  const { page, title, items } = req.body || {};
  seed(page, title, items);
  res.json({ ok: true });
});

app.get("/api/content", (req, res) => {
  const page = req.query.page;
  if (!page) return res.status(400).json({ error: "Missing page" });
  res.json({ page, overrides: overridesFor(page) });
});

// ---- auth ----------------------------------------------------------------
app.post("/api/login", (req, res) => {
  const { password } = req.body || {};
  if (password && timingSafeEqual(password, ADMIN_PASSWORD)) {
    return res.json({ token: VALID_TOKEN });
  }
  return res.status(401).json({ error: "Wrong password" });
});

// ---- admin API (password-protected) --------------------------------------
app.get("/api/admin/pages", requireAuth, (_req, res) => {
  res.json({ pages: pageList() });
});

app.get("/api/admin/page", requireAuth, (req, res) => {
  const detail = pageDetail(req.query.page);
  if (!detail) return res.status(404).json({ error: "Unknown page" });
  res.json(detail);
});

app.post("/api/admin/save", requireAuth, (req, res) => {
  const { page, overrides } = req.body || {};
  const ok = saveOverrides(page, overrides);
  if (!ok) return res.status(400).json({ error: "Could not save" });
  res.json({ ok: true, page, overrides: overridesFor(page) });
});

// ---- admin web UI ---------------------------------------------------------
app.use("/", express.static(path.join(__dirname, "public")));

app.get("/health", (_req, res) => res.json({ ok: true }));

app.listen(PORT, () => {
  console.log(`Entwine content backend listening on http://localhost:${PORT}`);
  console.log(`Admin panel:  http://localhost:${PORT}/`);
});
