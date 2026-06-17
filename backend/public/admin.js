/* Entwine Text Editor — admin panel logic (no framework). */
(function () {
  "use strict";

  // Routes that make up the website (used by "Sync site").
  var ROUTES = [
    "/", "/about", "/accessibility", "/brand-styles", "/careers", "/cookies",
    "/download", "/get", "/insights", "/invest", "/partners", "/pricing",
    "/privacy", "/restaurants", "/sitemap", "/terms", "/tools", "/wine-lovers",
    "/tools/btg-optimiser", "/tools/gap-finder", "/tools/menu-builder",
    "/tools/sommelier-pairing", "/tools/team-trainer", "/tools/wine-list-audit",
    "/tools/wine-list-creator",
    "/insights/ai-changing-how-we-discover-wine",
    "/insights/build-a-wine-list-guests-love",
    "/insights/digital-wine-list-and-cellar-connected",
    "/insights/how-to-read-a-wine-list",
    "/insights/second-cheapest-bottle",
    "/insights/the-story-behind-entwine",
    "/insights/wine-inventory-management-guide",
    "/insights/wine-pairing-101"
  ];

  var TOKEN_KEY = "entwine_admin_token";
  var SITE_KEY = "entwine_site_base";

  var token = localStorage.getItem(TOKEN_KEY) || null;
  var currentPage = null;
  var currentDetail = null;

  var $ = function (id) { return document.getElementById(id); };

  // ---- API ----------------------------------------------------------------
  function api(pathname, opts) {
    opts = opts || {};
    opts.headers = Object.assign(
      { "Content-Type": "application/json" },
      opts.headers || {},
      token ? { Authorization: "Bearer " + token } : {}
    );
    return fetch(pathname, opts).then(function (r) {
      if (r.status === 401) { doLogout(); throw new Error("Session expired"); }
      return r.json().then(function (body) {
        if (!r.ok) throw new Error(body.error || "Request failed");
        return body;
      });
    });
  }

  // ---- auth ---------------------------------------------------------------
  function showLogin() { $("login").hidden = false; $("app").hidden = true; }
  function showApp() { $("login").hidden = true; $("app").hidden = false; loadPages(); }

  $("loginForm").addEventListener("submit", function (e) {
    e.preventDefault();
    var err = $("loginError");
    err.hidden = true;
    fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ password: $("password").value }),
    })
      .then(function (r) { return r.json().then(function (b) { return { ok: r.ok, b: b }; }); })
      .then(function (res) {
        if (!res.ok) throw new Error(res.b.error || "Wrong password");
        token = res.b.token;
        localStorage.setItem(TOKEN_KEY, token);
        $("password").value = "";
        showApp();
      })
      .catch(function (e2) { err.textContent = e2.message; err.hidden = false; });
  });

  function doLogout() {
    token = null;
    localStorage.removeItem(TOKEN_KEY);
    showLogin();
  }
  $("logoutBtn").addEventListener("click", doLogout);

  // ---- pages list ---------------------------------------------------------
  function loadPages() {
    return api("/api/admin/pages").then(function (data) {
      var ul = $("pageList");
      ul.innerHTML = "";
      var pages = data.pages || [];
      $("noPages").hidden = pages.length > 0;
      pages.forEach(function (p) {
        var li = document.createElement("li");
        li.dataset.page = p.page;
        if (p.page === currentPage) li.classList.add("active");
        var label = document.createElement("span");
        label.textContent = p.title || p.page;
        label.title = p.page;
        var count = document.createElement("span");
        count.className = "count";
        count.textContent = p.edited ? p.edited + " edited" : p.total + " fields";
        li.appendChild(label);
        li.appendChild(count);
        li.addEventListener("click", function () { openPage(p.page); });
        ul.appendChild(li);
      });
    });
  }

  // ---- editor -------------------------------------------------------------
  function openPage(page) {
    currentPage = page;
    Array.prototype.forEach.call($("pageList").children, function (li) {
      li.classList.toggle("active", li.dataset.page === page);
    });
    api("/api/admin/page?page=" + encodeURIComponent(page)).then(function (detail) {
      currentDetail = detail;
      renderEditor(detail);
    });
  }

  function renderEditor(detail) {
    $("editorEmpty").hidden = true;
    $("editorBody").hidden = false;
    $("pageTitle").textContent = detail.title || detail.page;
    $("pagePath").textContent = detail.page;
    $("saveState").textContent = "";

    var wrap = $("fields");
    wrap.innerHTML = "";
    detail.items.forEach(function (item) {
      var field = document.createElement("div");
      field.className = "field";
      field.dataset.key = item.key;
      if (item.override != null) field.classList.add("changed");

      var orig = document.createElement("div");
      orig.className = "orig";
      orig.textContent = "Original: " + item.original;

      var row = document.createElement("div");
      row.className = "row";

      var ta = document.createElement("textarea");
      ta.rows = 1;
      ta.value = item.override != null ? item.override : item.original;
      ta.dataset.original = item.original;
      autosize(ta);
      ta.addEventListener("input", function () {
        autosize(ta);
        field.classList.toggle("changed", ta.value !== ta.dataset.original);
      });

      var reset = document.createElement("button");
      reset.className = "reset";
      reset.type = "button";
      reset.textContent = "Reset";
      reset.title = "Restore the original text";
      reset.addEventListener("click", function () {
        ta.value = ta.dataset.original;
        autosize(ta);
        field.classList.remove("changed");
      });

      row.appendChild(ta);
      row.appendChild(reset);
      field.appendChild(orig);
      field.appendChild(row);
      wrap.appendChild(field);
    });
  }

  function autosize(ta) {
    ta.style.height = "auto";
    ta.style.height = ta.scrollHeight + "px";
  }

  $("saveBtn").addEventListener("click", function () {
    if (!currentPage) return;
    var overrides = {};
    Array.prototype.forEach.call($("fields").children, function (field) {
      var ta = field.querySelector("textarea");
      var key = field.dataset.key;
      // Send null when it matches the original (clears the override).
      overrides[key] = ta.value === ta.dataset.original ? null : ta.value;
    });
    $("saveBtn").disabled = true;
    $("saveState").textContent = "Saving…";
    api("/api/admin/save", {
      method: "POST",
      body: JSON.stringify({ page: currentPage, overrides: overrides }),
    })
      .then(function () {
        $("saveState").textContent = "Saved ✓";
        return loadPages();
      })
      .catch(function (e) { $("saveState").textContent = "Error: " + e.message; })
      .then(function () { $("saveBtn").disabled = false; });
  });

  // ---- sync site (visit every page so new text registers) -----------------
  $("syncBtn").addEventListener("click", function () {
    var base = localStorage.getItem(SITE_KEY) || "";
    base = prompt(
      "Enter your live website address (so I can read its pages):",
      base || "https://ipassas.github.io/entwine"
    );
    if (!base) return;
    base = base.replace(/\/+$/, "");
    localStorage.setItem(SITE_KEY, base);

    var frames = $("syncFrames");
    frames.innerHTML = "";
    var i = 0;
    $("syncBtn").disabled = true;
    $("syncBtn").textContent = "Syncing… 0/" + ROUTES.length;

    function next() {
      if (i >= ROUTES.length) {
        $("syncBtn").textContent = "Sync site";
        $("syncBtn").disabled = false;
        frames.innerHTML = "";
        loadPages();
        return;
      }
      var route = ROUTES[i++];
      var f = document.createElement("iframe");
      f.style.cssText = "width:1px;height:1px;border:0;position:absolute;left:-9999px;";
      f.src = base + route;
      frames.appendChild(f);
      $("syncBtn").textContent = "Syncing… " + i + "/" + ROUTES.length;
      // Give each page time to load and self-register, then move on.
      setTimeout(next, 1400);
    }
    next();
  });

  // ---- boot ---------------------------------------------------------------
  if (token) showApp();
  else showLogin();
})();
