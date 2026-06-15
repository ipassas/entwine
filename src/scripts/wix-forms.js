/* Wix Headless form submission.
 *
 * Submits into Wix Forms so entries land in the Wix dashboard and can trigger
 * Wix Automations (e.g. an email to info@entwine.club) — i.e. forms become part
 * of the Wix infrastructure once the site runs on Wix Headless.
 *
 * Configuration (set when you link Headless — see WIX-HEADLESS.md):
 *   PUBLIC_WIX_CLIENT_ID          — the Headless OAuth app client id
 *   PUBLIC_WIX_CAREERS_FORM_ID    — the "Careers application" Wix Form id
 *   PUBLIC_WIX_NEWSLETTER_FORM_ID — the "Newsletter" Wix Form id
 *
 * With no client id configured this module is inert, so the site keeps working
 * exactly as before (the careers form falls back to a drafted email). The Wix
 * SDK is loaded lazily (dynamic import) so it only ships to the browser once a
 * form is actually submitted.
 */
const CLIENT_ID = import.meta.env.PUBLIC_WIX_CLIENT_ID || '';

export const wixConfigured = Boolean(CLIENT_ID);

let _client = null;
async function getClient() {
  if (_client) return _client;
  const { createClient, OAuthStrategy } = await import('@wix/sdk');
  const { submissions } = await import('@wix/forms');
  _client = createClient({
    modules: { submissions },
    auth: OAuthStrategy({ clientId: CLIENT_ID }),
  });
  return _client;
}

/** Submit a set of field values to a Wix Form. `fields` keys must match the
 *  form's field keys in the Wix dashboard. Returns true on success. */
export async function submitWixForm(formId, fields) {
  if (!wixConfigured || !formId) return false;
  const client = await getClient();
  await client.submissions.createSubmission({
    submission: { formId, submissions: fields, status: 'CONFIRMED' },
  });
  return true;
}
