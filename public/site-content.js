/*
 * site-content.js — applies editable-text overrides from the content backend.
 *
 * HOW IT WORKS
 *  - On every page load it finds the page's text elements (in a stable order),
 *    reports them to the backend (so the admin panel knows what text exists),
 *    then fetches any saved overrides and swaps the text in.
 *  - The text you see by default is the original hand-coded copy; only fields
 *    you have edited in the admin panel get replaced.
 *
 * SETUP
 *  - Point API_BASE at your deployed backend URL (the one running /backend).
 *    Either edit the line below, or set `window.CONTENT_API_BASE = '...'`
 *    in a <script> before this file loads.
 */
(function () {
  "use strict";

  var API_BASE =
    (window.CONTENT_API_BASE && String(window.CONTENT_API_BASE)) ||
    "http://localhost:8787";
  API_BASE = API_BASE.replace(/\/+$/, "");

  // Tags whose pure-text contents are considered editable copy.
  var TAGS =
    "h1,h2,h3,h4,h5,h6,p,a,li,button,blockquote,figcaption,label,span,strong,em,small,td,th,summary,dt,dd";

  // Stable page identifier (so each route has its own set of fields).
  function pageKey() {
    var p = location.pathname || "/";
    p = p.replace(/index\.html?$/i, "");
    if (p.length > 1) p = p.replace(/\/+$/, "");
    return p === "" ? "/" : p;
  }

  // Collect editable elements in document order. An element is editable when
  // it has no child elements (pure text), has visible text, and is not opted
  // out via [data-no-edit]. Order is deterministic, so the index is a stable key.
  function collect() {
    var nodes = Array.prototype.slice.call(document.querySelectorAll(TAGS));
    var out = [];
    for (var i = 0; i < nodes.length; i++) {
      var el = nodes[i];
      if (el.childElementCount !== 0) continue;
      var text = (el.textContent || "").trim();
      if (!text) continue;
      if (el.closest("[data-no-edit]")) continue;
      out.push(el);
    }
    return out;
  }

  function run() {
    var els = collect();
    if (!els.length) return;

    var page = pageKey();
    var items = els.map(function (el, i) {
      return { key: String(i), original: el.textContent.trim() };
    });

    // 1) Tell the backend what text lives on this page (so the editor lists it).
    try {
      fetch(API_BASE + "/api/seed", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ page: page, title: document.title || page, items: items }),
        keepalive: true,
      }).catch(function () {});
    } catch (e) {}

    // 2) Pull any saved overrides and apply them.
    fetch(API_BASE + "/api/content?page=" + encodeURIComponent(page))
      .then(function (r) {
        return r.ok ? r.json() : { overrides: {} };
      })
      .then(function (data) {
        var ov = (data && data.overrides) || {};
        Object.keys(ov).forEach(function (k) {
          var el = els[Number(k)];
          var val = ov[k];
          if (el && typeof val === "string") el.textContent = val;
        });
      })
      .catch(function () {});
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run);
  } else {
    run();
  }
})();
