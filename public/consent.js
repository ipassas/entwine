/* Cookie consent banner — injected on every page.
   Remembers via localStorage AND cookie (localStorage survives Safari's
   third-party-cookie limits while the site runs inside the Wix frame).
   Note: the age gate lives on the app download flow, not the website. */
(function () {
  var CONSENT_KEY = 'ew-consent';

  function get(k) {
    try { var v = localStorage.getItem(k); if (v) return v; } catch (e) {}
    var m = document.cookie.match(new RegExp('(?:^|; )' + k + '=([^;]*)'));
    return m ? decodeURIComponent(m[1]) : null;
  }
  function set(k, v, days) {
    try { localStorage.setItem(k, v); } catch (e) {}
    try { document.cookie = k + '=' + encodeURIComponent(v) + '; max-age=' + (days * 86400) + '; path=/; SameSite=Lax'; } catch (e) {}
  }

  /* ---------- cookie banner ---------- */
  function showBanner() {
    if (get(CONSENT_KEY)) return;
    var b = document.createElement('div');
    b.className = 'ck';
    b.setAttribute('role', 'dialog');
    b.setAttribute('aria-label', 'Cookies');
    b.innerHTML =
      '<div class="ck__txt"><b>A word on cookies.</b> Essential cookies keep the site working; with your consent we also use analytics cookies to improve it. Read our <a href="/cookies">Cookie Policy</a>.</div>' +
      '<div class="ck__btns">' +
      '<button type="button" class="btn btn--gold" data-ck="all">Accept all</button>' +
      '<button type="button" class="btn btn--outline-light" data-ck="essential">Essential only</button>' +
      '</div>';
    document.body.appendChild(b);
    b.addEventListener('click', function (e) {
      var c = e.target.closest('[data-ck]');
      if (!c) return;
      set(CONSENT_KEY, c.getAttribute('data-ck'), 365);
      b.classList.add('ck--hide');
      setTimeout(function () { b.remove(); }, 450);
    });
  }

  function init() {
    showBanner();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
