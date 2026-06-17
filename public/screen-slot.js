/* screen-slot — drops a real app screenshot into a device/preview frame.
   Markup: <div class="app-screen" data-label="Pairing screen">
             <img data-screen="wl-pairing" alt="…">
           </div>
   Loads /assets/screens/<data-screen>.png. If the file is missing, the image
   is removed and the framed placeholder (the data-label caption) shows instead.
   Replace the PNGs in /assets/screens/ to publish real screens — no code change. */
(function () {
  document.querySelectorAll('img[data-screen]').forEach(function (im) {
    var name = im.getAttribute('data-screen');
    if (!name) return;
    im.addEventListener('load', function () { im.classList.add('is-loaded'); });
    im.addEventListener('error', function () { if (im.parentNode) im.parentNode.removeChild(im); });
    im.src = '/assets/screens/' + name + '.png';
  });
})();
