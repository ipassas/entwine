/* <image-slot> — a named photo slot for the Entwine site.
   Usage: <image-slot id="team-daniel" shape="circle" placeholder="DA"></image-slot>
   Loads assets/<id>.jpg; if missing, shows the elegant initials placeholder
   (no random stock faces for real people). Exposes ::part(frame) and ::part(ring). */
(function () {
  if (customElements.get('image-slot')) return;
  class ImageSlot extends HTMLElement {
    connectedCallback() {
      if (this._init) return;
      this._init = true;
      var ph = (this.getAttribute('placeholder') || '').trim();
      var radius = this.getAttribute('shape') === 'circle' ? '50%' : '14px';
      var id = this.id || this.getAttribute('name') || '';
      var src = this.getAttribute('src') || (id ? '/entwine/assets/team/' + id + '.jpg' : '');
      var root = this.attachShadow({ mode: 'open' });
      root.innerHTML =
        '<style>' +
        ':host{display:inline-flex;line-height:0}' +
        '.frame{position:relative;width:100%;height:100%;border-radius:' + radius + ';overflow:hidden;' +
        'display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,.06)}' +
        '.ph{color:inherit;font-family:inherit;font-weight:inherit;font-size:30px;letter-spacing:.05em;line-height:1}' +
        'img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity .45s ease}' +
        'img.show{opacity:1}' +
        '.ring{position:absolute;inset:0;border-radius:' + radius + ';pointer-events:none}' +
        '</style>' +
        '<div class="frame" part="frame"><span class="ph">' + ph + '</span>' +
        '<img part="img" alt="" decoding="async"></div>' +
        '<div class="ring" part="ring"></div>';
      var img = root.querySelector('img');
      var phEl = root.querySelector('.ph');
      if (!src) return;
      img.addEventListener('load', function () { img.classList.add('show'); phEl.style.display = 'none'; });
      img.addEventListener('error', function () { if (img.parentNode) img.parentNode.removeChild(img); });
      img.src = src;
    }
  }
  customElements.define('image-slot', ImageSlot);
})();
