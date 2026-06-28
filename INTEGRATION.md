# INFITEX Website — Integration & Deployment Guide

How to host this site on **Cloudflare Pages**, wire up the integrations (forms, booking,
WhatsApp, QR), verify search engines, and rebuild the HTML when content changes.

---

## 1. Deploy to Cloudflare Pages

The site is fully static — no build step is required on Cloudflare.

### Option A — Direct upload (fastest)
1. Cloudflare dashboard -> **Workers & Pages** -> **Create** -> **Pages** -> **Upload assets**.
2. Drag in the **contents** of the website bundle (the folder that contains `index.html`).
   Do not nest it inside another folder.
3. Name the project (e.g. `infitex`) and **Deploy**.

### Option B — Git
1. Push the website bundle to a Git repo.
2. Pages -> **Connect to Git** -> select the repo.
3. **Build command:** leave empty. **Build output directory:** `/` (repo root) or the
   folder that holds `index.html`.
4. Deploy.

### Custom domain
- Pages project -> **Custom domains** -> add `infitexglobal.com` (and `www`).
- If your DNS is on Cloudflare, the records are added automatically; otherwise point a
  CNAME at the `*.pages.dev` target.
- Force HTTPS is on by default.

### Redirects & headers
- `_redirects` and `_headers` in the root are read natively by Cloudflare Pages.
  - `_redirects` — add lines like `/old /new 301`. A `www -> apex` (or vice-versa) rule
    lives here; adjust to your canonical host.
  - `_headers` — security/caching headers. Review the CSP/cache rules before launch.
- `netlify.toml` is intentionally **not** included in the hosting bundle (Netlify-specific).

---

## 2. Contact form (Web3Forms)

The enquiry form on `contact.html` posts to **Web3Forms** (no backend needed).

- Access key (already embedded): `348d4025-f324-4e35-9b3f-b7a13bc62f09`
- To change the destination inbox: create/replace the key at https://web3forms.com and
  update the `access_key` hidden field. In source it is set in `_build-sources/build.py`
  (search for `web3formsKey`) and rendered into the form; update there and rebuild, or
  edit the value directly in `contact.html` if you only need a one-off change.
- Submissions are validated client-side in `app.js`; success/error text shows inline.
- The same mechanism powers the **compliance-dates digest** subscribe form on `contact.html`
  (`#subscribeForm`).

---

## 3. Booking, WhatsApp, Email, Call, QR

All wired in `app.js` and the shared partials:

| Action | How it works | Where to change |
|--------|--------------|-----------------|
| **Book a call** | `[data-booking]` opens the Google booking link in a new tab | `bookingLink` in `_build-sources/_partials.py` |
| **WhatsApp** | `[data-open-wa]` opens a dialog that drafts a message to `918500850526` | `whatsapp` number in `_partials.py` |
| **Email** | `[data-open-mail]` opens a prefilled `mailto:` to info@infitexglobal.com | `_partials.py` |
| **Call** | Floating phone button is a `tel:+918500850526` link | `fabs()` in `_partials.py` |
| **QR** | `[data-open-qr]` shows `infitex-contact-qr.svg` in a dialog (also a floating button) | swap the QR asset files |

To regenerate the contact QR, encode a vCard with the name, mobile and email, and replace
`infitex-contact-qr.svg` and `infitex-contact-qr.png` (keep the same filenames).

---

## 4. SEO / GEO / verification

- Each page emits a JSON-LD graph (Organization, WebSite, BreadcrumbList, page type,
  and `speakable` for AI/voice answers).
- `sitemap.xml` lists all 9 pages; `robots.txt` references it. Update `sitemap.xml`
  whenever pages are added/removed.
- Search-engine verification placeholders live in the `<head>` (in `page()` inside
  `_partials.py`). Replace the placeholder tokens for:
  - Google Search Console (`google-site-verification`)
  - Bing, Yandex, Pinterest (optional)
- Open Graph / Twitter cards use `og-image.png` (1200x630). Replace to rebrand previews.
- After deploy: submit `https://infitexglobal.com/sitemap.xml` in Google Search Console
  and Bing Webmaster Tools.

---

## 5. Analytics (optional)

No analytics is bundled. To add Cloudflare Web Analytics: Pages project -> **Metrics**, or
drop the Cloudflare beacon snippet into the `<head>` in `_partials.py` and rebuild. Any
GDPR/privacy-respecting analytics can be added the same way.

---

## 6. Rebuilding the HTML

Generated pages (`*.html`) come from the Python generator in `_build-sources/`.
`styles.css` and `app.js` are static and survive rebuilds.

1. In **`_build-sources/_partials.py`, `validate.py`, `validate2.py`**, set
   `OUT = "<path to the site root>"` (the folder that holds `index.html`).
2. From `_build-sources/`, run:
   ```
   python3 build.py
   python3 validate.py     # expect: 0 issues, 0 warnings
   python3 validate2.py    # expect: 0 issues, 0 warnings, 8 positive checks
   ```
3. Restore `OUT` to its previous value if you changed it.
4. Redeploy the site root.

**Where things live**
- Page content/markup -> `build_<page>()` in `build.py`
- Header, nav, footer, floating buttons, icons, JSON-LD, search index -> `_partials.py`
- Styling -> `styles.css` (direct)
- Interactivity (theme, search, dialogs, sliders, forms, FABs) -> `app.js` (direct)

---

## 8. Caching & the "old theme on first load" fix

Symptom: after a redeploy, the first page load shows the *previous* styling, then
corrects itself on navigation. Cause: `styles.css` / `app.js` were cached for a year
with no version, so browsers reused the old files against the new HTML.

Fix (already in the build):
- `styles.css` and `app.js` are referenced with a content-hash query, e.g.
  `styles.css?v=2b7db34c`. The build recomputes the hash whenever the file changes,
  so the URL changes and browsers fetch the new asset. The long, `immutable` cache in
  `_headers` is now safe because each version has a unique URL.
- HTML stays `Cache-Control: public, max-age=0, must-revalidate` (always fresh).

After deploying this change once, run Cloudflare **Caching → Purge Everything** to
drop any stale edge copies of the old HTML/CSS. From then on it is automatic.

## 9. Pre-launch checklist

- [ ] Custom domain attached and HTTPS verified
- [ ] `_redirects` canonical host rule matches your chosen apex/www
- [ ] Web3Forms key points at the correct inbox; test a submission
- [ ] Booking link, WhatsApp number, phone (`tel:`), email all correct
- [ ] Contact QR encodes the current vCard
- [ ] Google/Bing verification tokens replaced; sitemap submitted
- [ ] `og-image.png` and favicons are final
- [ ] Compliance claims intact (not a registered agent; practice keeps lodgement/sign-off; no prices)
- [ ] Spot-check light/dark themes and mobile nav
