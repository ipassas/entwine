/* Age gate (18+) + cookie consent banner — injected on every page.
   Remembers via localStorage AND cookie (localStorage survives Safari's
   third-party-cookie limits while the site runs inside the Wix frame). */
(function () {
  var AGE_KEY = 'ew-age', CONSENT_KEY = 'ew-consent';

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

  /* ---------- age gate ---------- */
  function showGate() {
    var g = document.createElement('div');
    g.className = 'ag';
    g.setAttribute('role', 'dialog');
    g.setAttribute('aria-modal', 'true');
    g.setAttribute('aria-label', 'Age verification');
    g.innerHTML =
      '<div class="ag__in">' +
      '<svg class="ag__mark" viewBox="0 0 42 52" fill="currentColor" aria-hidden="true"><use href="#ew-mark"/></svg>' +
      '<p class="ag__kick">Welcome to Entwine</p>' +
      '<h2 class="ag__title">Are you of legal <span>drinking age?</span></h2>' +
      '<p class="ag__sub">Entwine is a wine platform. To visit, you must be 18 or older.</p>' +
      '<div class="ag__btns">' +
      '<button type="button" class="btn btn--gold" data-ag="yes">I’m 18 or older — Enter <span class="arrow">→</span></button>' +
      '<button type="button" class="btn btn--outline-light" data-ag="no">I’m under 18</button>' +
      '</div>' +
      '<p class="ag__note">Please drink responsibly.</p>' +
      '</div>';
    document.body.appendChild(g);
    var prevOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';

    g.addEventListener('click', function (e) {
      var c = e.target.closest('[data-ag]');
      if (!c) return;
      if (c.getAttribute('data-ag') === 'yes') {
        set(AGE_KEY, 'ok', 365);
        g.classList.add('ag--done');
        document.body.style.overflow = prevOverflow;
        setTimeout(function () { g.remove(); }, 500);
        showBanner();
      } else {
        g.querySelector('.ag__in').innerHTML =
          '<svg class="ag__mark" viewBox="0 0 42 52" fill="currentColor" aria-hidden="true"><use href="#ew-mark"/></svg>' +
          '<p class="ag__kick">Entwine</p>' +
          '<h2 class="ag__title">See you in <span>a few years.</span></h2>' +
          '<p class="ag__sub">You must be 18 or older to visit Entwine. Please drink responsibly.</p>';
      }
    });
  }

  function init() {
    if (get(AGE_KEY) === 'ok') { showBanner(); } else { showGate(); }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
