/* Smart store routing for download CTAs.
   Android -> Google Play, iOS -> App Store, desktop -> /download page.
   Explicit store badges always deep-link to their named store. */
(function () {
  var PLAY = 'https://play.google.com/store/apps/details?id=club.entwine.app';
  var APPSTORE = 'https://apps.apple.com/mt/app/entwine-pairing/id6760898191';
  var ua = navigator.userAgent || '';
  var isAndroid = /android/i.test(ua);
  var isIOS = /iphone|ipad|ipod/i.test(ua) ||
    (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);

  function external(a, url) {
    a.href = url; a.target = '_blank'; a.rel = 'noopener';
  }

  // App Store / Google Play badges name their store explicitly
  document.querySelectorAll('a.badge[data-icon]').forEach(function (b) {
    external(b, b.getAttribute('data-icon') === 'apple' ? APPSTORE : PLAY);
  });

  // Generic download buttons route by platform; desktop keeps the /download page
  if (isAndroid || isIOS) {
    var store = isAndroid ? PLAY : APPSTORE;
    document.querySelectorAll('a.btn[href$="/download"], a.nav-cta[href$="/download"]').forEach(function (a) {
      external(a, store);
    });
  }
})();
