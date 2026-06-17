/* Download experience for Entwine.
   - Mobile (iOS / Android): every download CTA and store-badge row collapses to
     a single one-tap deep link to THAT device's store.
   - Desktop: store-badge rows become "Download available at [apple][google] +
     Download button", and every download button opens a QR-code modal. Scanning
     the QR opens /get, which routes the phone to the right store automatically.
   The named store badges inside the modal stay as explicit deep links. */
(function () {
  var PLAY = 'https://play.google.com/store/apps/details?id=club.entwine.app';
  var APPSTORE = 'https://apps.apple.com/mt/app/entwine-pairing/id6760898191';

  var ua = navigator.userAgent || '';
  var isAndroid = /android/i.test(ua);
  var isIOS = /iphone|ipad|ipod/i.test(ua) ||
    (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  var isMobile = isAndroid || isIOS;
  var deviceStore = isAndroid ? PLAY : APPSTORE;

  /* Work out the subpath the site is served under (e.g. /entwine on GitHub
     Pages) from the stylesheet href, which the build rewrites. Used only for
     the QR target — asset literals below are rewritten by the build itself. */
  function basePath() {
    var css = document.querySelector('link[rel="stylesheet"]');
    if (css) { var m = (css.getAttribute('href') || '').match(/^(.*)\/styles\.css/); if (m) return m[1]; }
    return '';
  }
  function smartLink() { return location.origin + basePath() + '/get'; }

  function badgeImg(kind) {
    var src = kind === 'apple' ? '/assets/badges/app-store.svg' : '/assets/badges/google-play.svg';
    var alt = kind === 'apple' ? 'Download on the App Store' : 'Get it on Google Play';
    return '<img class="badge__img" src="' + src + '" alt="' + alt + '">';
  }

  /* ---------------- QR modal (desktop) ---------------- */
  var modal;
  function buildModal() {
    if (modal) return;
    var qr = 'https://api.qrserver.com/v1/create-qr-code/?size=320x320&margin=0&data=' +
      encodeURIComponent(smartLink());
    modal = document.createElement('div');
    modal.className = 'ew-qr';
    modal.setAttribute('role', 'dialog');
    modal.setAttribute('aria-modal', 'true');
    modal.setAttribute('aria-label', 'Download the Entwine app');
    modal.innerHTML =
      '<div class="ew-qr__backdrop" data-qr-close></div>' +
      '<div class="ew-qr__card" role="document">' +
        '<button class="ew-qr__x" type="button" data-qr-close aria-label="Close">×</button>' +
        '<p class="ew-qr__kick">Get the app</p>' +
        '<h3 class="ew-qr__title">Scan to download Entwine</h3>' +
        '<div class="ew-qr__code"><img alt="QR code to download the Entwine app" width="220" height="220" src="' + qr + '"></div>' +
        '<p class="ew-qr__hint">Point your phone’s camera at the code — it opens the App Store or Google Play automatically.</p>' +
        '<div class="ew-qr__or"><span>or download directly</span></div>' +
        '<div class="ew-qr__stores">' +
          '<a class="badge" href="' + APPSTORE + '" target="_blank" rel="noopener" aria-label="Download on the App Store">' + badgeImg('apple') + '</a>' +
          '<a class="badge" href="' + PLAY + '" target="_blank" rel="noopener" aria-label="Get it on Google Play">' + badgeImg('google') + '</a>' +
        '</div>' +
      '</div>';
    document.body.appendChild(modal);
    modal.addEventListener('click', function (e) { if (e.target.closest('[data-qr-close]')) closeModal(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeModal(); });
  }
  function openModal() {
    buildModal();
    requestAnimationFrame(function () { modal.classList.add('open'); });
    document.body.style.overflow = 'hidden';
  }
  function closeModal() {
    if (modal) { modal.classList.remove('open'); document.body.style.overflow = ''; }
  }

  /* ---------------- desktop download widget ---------------- */
  function widgetHTML() {
    return '<div class="ew-dl">' +
      '<span class="ew-dl__avail">Download available at' +
        '<span class="ew-dl__ics" aria-hidden="true">' +
          '<iconify-icon icon="ph:apple-logo-fill"></iconify-icon>' +
          '<iconify-icon icon="ph:google-play-logo-fill"></iconify-icon>' +
        '</span>' +
      '</span>' +
      '<button class="btn btn--gold ew-dl__btn" type="button" data-qr-open>Download <span class="arrow">→</span></button>' +
    '</div>';
  }

  /* ---------------- transform store-badge rows ---------------- */
  var rows = [];
  document.querySelectorAll('a.badge[data-icon]').forEach(function (b) {
    if (rows.indexOf(b.parentNode) === -1) rows.push(b.parentNode);
  });
  rows.forEach(function (row) {
    var apple = row.querySelector('a.badge[data-icon="apple"]');
    var google = row.querySelector('a.badge[data-icon="google"]');
    if (isMobile) {
      var keep = isAndroid ? google : apple, drop = isAndroid ? apple : google;
      if (drop) drop.remove();
      if (keep) { keep.href = deviceStore; keep.target = '_blank'; keep.rel = 'noopener'; }
    } else {
      row.innerHTML = widgetHTML();
    }
  });

  /* ---------------- generic download buttons ---------------- */
  document.querySelectorAll('a[href$="/download"]').forEach(function (a) {
    if (isMobile) {
      a.href = deviceStore; a.target = '_blank'; a.rel = 'noopener';
    } else {
      a.addEventListener('click', function (e) { e.preventDefault(); openModal(); });
    }
  });

  /* desktop widget "Download" buttons */
  document.addEventListener('click', function (e) {
    var t = e.target.closest ? e.target.closest('[data-qr-open]') : null;
    if (t) { e.preventDefault(); openModal(); }
  });

  /* ---------------- mobile sticky download bar ----------------
     Full-width bar above the menu on phones, with the right store icon.
     Hides on scroll-down, reappears (pushing the menu down) on scroll-up.
     Hidden on desktop via CSS. */
  (function () {
    var bar = document.createElement('a');
    bar.className = 'mdl';
    var icon = isIOS ? 'ph:apple-logo-fill' : isAndroid ? 'ph:google-play-logo-fill' : 'ph:download-simple-bold';
    bar.innerHTML = '<iconify-icon icon="' + icon + '"></iconify-icon><span>Download the app</span>';
    if (isMobile) { bar.href = deviceStore; bar.target = '_blank'; bar.rel = 'noopener'; }
    else { bar.href = '#'; bar.addEventListener('click', function (e) { e.preventDefault(); openModal(); }); }
    document.body.insertBefore(bar, document.body.firstChild);

    var lastY = window.pageYOffset || 0, ticking = false;
    function update() {
      var y = window.pageYOffset || 0;
      if (y < 60) document.body.classList.remove('mdl-hidden');
      else if (y > lastY + 4) document.body.classList.add('mdl-hidden');
      else if (y < lastY - 4) document.body.classList.remove('mdl-hidden');
      lastY = y; ticking = false;
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { window.requestAnimationFrame(update); ticking = true; }
    }, { passive: true });
  })();
})();
