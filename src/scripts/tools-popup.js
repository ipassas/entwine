/* "Tool under development" lightbox for the tools pages.
 * Shows once per browser session per tool, with a subscribe form that posts to
 * the same Wix newsletter form. Closeable; the page stays usable underneath. */
import { wixConfigured, submitWixForm, NEWSLETTER_FORM_ID, NEWSLETTER_EMAIL_KEY } from './wix-forms.js';

(function () {
  var key = 'ew-tool-dev:' + location.pathname;
  try { if (sessionStorage.getItem(key)) return; } catch (e) {}

  var o = document.createElement('div');
  o.className = 'tdev';
  o.setAttribute('role', 'dialog');
  o.setAttribute('aria-modal', 'true');
  o.setAttribute('aria-label', 'Tool under development');
  o.innerHTML =
    '<div class="tdev__backdrop" data-tdev-close></div>' +
    '<div class="tdev__card" role="document">' +
      '<button class="tdev__x" type="button" data-tdev-close aria-label="Close">×</button>' +
      '<p class="tdev__kick">Coming soon</p>' +
      '<h3 class="tdev__title">This tool is under development</h3>' +
      '<p class="tdev__txt">We’re putting the finishing touches on it. Leave your email and we’ll tell you the moment it’s live — meanwhile, feel free to look around.</p>' +
      '<form class="tdev__form" novalidate><input type="email" required placeholder="Your email address" aria-label="Email address"><button class="btn btn--gold" type="submit">Notify me</button></form>' +
      '<p class="tdev__note">No spam — just one email when it launches.</p>' +
    '</div>';
  document.body.appendChild(o);
  requestAnimationFrame(function () { o.classList.add('open'); });
  try { sessionStorage.setItem(key, '1'); } catch (e) {}

  function close() { o.classList.remove('open'); setTimeout(function () { o.remove(); }, 300); }
  o.addEventListener('click', function (e) { if (e.target.closest('[data-tdev-close]')) close(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && document.body.contains(o)) close(); });

  var f = o.querySelector('.tdev__form'), note = o.querySelector('.tdev__note');
  f.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!f.checkValidity()) { f.reportValidity(); return; }
    var email = f.querySelector('input').value;
    function done(msg) { note.textContent = msg; }
    if (wixConfigured && NEWSLETTER_FORM_ID) {
      var v = {}; v[NEWSLETTER_EMAIL_KEY] = email;
      submitWixForm(NEWSLETTER_FORM_ID, v).then(function (ok) {
        done(ok ? 'Thanks — we’ll be in touch.' : 'Hmm, that didn’t go through. Please try again.');
        if (ok) setTimeout(close, 1300);
      }).catch(function () { done('Hmm, that didn’t go through. Please try again.'); });
    } else { done('Thanks — we’ll be in touch.'); setTimeout(close, 1300); }
  });
})();
