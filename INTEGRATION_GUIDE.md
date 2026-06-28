# INFITEX Global Advisory — Website Integration & Deployment Guide

A complete, hand-built static website (no frameworks, no build step). Just HTML, CSS and vanilla JavaScript. This guide covers the handful of placeholders to fill in, how to go live on Cloudflare Pages, DNS for your domain and email, and analytics.

---

## 1. What's in this package

```
index.html          Home (hero, who-we-help, stack, divisions, how it works,
                    engagement, compliance cycle, security, Digitech, savings
                    calculator, key dates, about, FAQ, pilot CTA, contact, subscribe)
outsourcing.html    For Practices — white-label compliance cycle + jobs/frequency
industry.html       For Business — outsourced finance + Virtual CFO (NEW)
digitech.html       Digitech — web, email, SEO
privacy.html        Privacy Policy (Privacy Act 1988 / APPs aligned)
terms.html          Terms of Use
sitemap.html        Human-readable sitemap
styles.css          Full Neon Terminal design system (dark default + light theme)
app.js              All interactivity (theme, search, forms, calculator, FAQ, typewriter)
logo.svg            Standalone logo (aligned symmetric X)
favicon.svg         Favicon
og-image.png        1200×630 social share image
robots.txt          Crawl rules + sitemap reference
sitemap.xml         XML sitemap for search engines
```

Everything above sits at the **root** of the site — that's exactly what you upload.

---

## 2. Placeholders to replace (15 minutes)

### 2a. `app.js` — one CONFIG block near the top

```js
var CONFIG = {
  whatsapp: "919000000000",              // your WhatsApp number, digits only, country code first
  email:    "hello@infitexglobal.com",   // your enquiry inbox
  bookingLink: "https://calendar.app.google/...",  // your Google appointment / booking link
  web3formsKey: "YOUR_WEB3FORMS_ACCESS_KEY",
  domain:   "https://infitexglobal.com"
};
```

- **whatsapp** — full international number, digits only, no `+`, spaces or dashes. Example: Australian `+61 4XX XXX XXX` → `614XXXXXXXX`; Indian `+91 90000 00000` → `919000000000`.
- **bookingLink** — your Google appointment (or any) booking link. Until set, every "Book a call" button gracefully falls back to the contact form.
- **web3formsKey** — see step 3. Until set, all three lead channels run in **demo mode** (they validate and draft the message, but don't actually send) so nothing breaks while you test.

### 2b. `GOOGLE_SITE_VERIFICATION` (all HTML files)

Each page has `<meta name="google-site-verification" content="GOOGLE_SITE_VERIFICATION">`. When you add the site to Google Search Console (step 7), replace that token with the value Google gives you. Find-and-replace across all `.html` files.

### 2c. Social handles (`styles.css` not needed — they're in the footer of every page)

The footer links currently point to placeholder handles:
`linkedin.com/company/infitexglobal`, `facebook.com/infitexglobal`, `instagram.com/infitexglobal`, `x.com/infitexglobal`, `youtube.com/@infitexglobal`. Update these to your real profiles (find-and-replace works well, or regenerate — see step 9).

### 2d. Phone number

The header and footer show `+91 90000 00000` (`tel:+919000000000`). Replace with your real number across the HTML files if different.

---

## 3. Web3Forms (the form/WhatsApp/email engine) — free

1. Go to **web3forms.com**, enter your destination email, and copy the **Access Key** they email you.
2. Paste it into `CONFIG.web3formsKey` in `app.js`.
3. Done. The contact form now emails you each submission; the WhatsApp and Email buttons draft the same tidy paragraph and open WhatsApp / the user's mail app.

**The auto-drafted message looks like this:**

```
Hi INFITEX,

This is [Name] from [Business]. I'm enquiring about [topic].

My contact details are as follows:
Email: [email]
Mobile: +61 4XXXXXXXX

Thanks & regards,
[Name]
[Business]
```

The phone field uses a searchable country-code combo (shows only the dial code, defaults to **+61**) and restricts the local number to exactly **10 digits**.

---

## 4. Deploy to Cloudflare Pages (free, ~5 minutes)

**Drag-and-drop method (no Git needed):**

1. Sign in at **dash.cloudflare.com** → **Workers & Pages** → **Create** → **Pages** → **Upload assets**.
2. Name the project (e.g. `infitex`).
3. Drag the **contents** of this folder (all the files listed in section 1 — not the folder itself) into the upload box.
4. **Deploy**. You'll get a `*.pages.dev` URL immediately to test.

**To update later:** make your edits locally, then re-upload the folder contents (Cloudflare keeps version history).

---

## 5. Connect your domain (infitexglobal.com)

If your domain is registered at **Spaceship** (or any registrar):

1. In Cloudflare Pages → your project → **Custom domains** → **Set up a custom domain** → enter `infitexglobal.com` (and `www.infitexglobal.com`).
2. Cloudflare will either:
   - ask you to **change nameservers** at Spaceship to the two Cloudflare nameservers it shows you (recommended — gives you full DNS + CDN), **or**
   - give you **CNAME/A records** to add at Spaceship if you keep DNS there.
3. In Spaceship → your domain → **Nameservers / DNS**, apply whichever Cloudflare asked for. Propagation is usually minutes to a few hours.
4. Cloudflare issues a free SSL certificate automatically — your site will be `https://`.

---

## 6. Business email DNS (so hello@infitexglobal.com works)

Pick one provider and add its records in your DNS (Cloudflare if you moved nameservers, otherwise Spaceship). Exact values come from your provider's setup screen — below is what each needs:

| Provider | Records you'll add |
|---|---|
| **Google Workspace** | MX → `smtp.google.com` (priority 1); SPF `TXT` → `v=spf1 include:_spf.google.com ~all`; DKIM `TXT` from the Admin console (`google._domainkey`); DMARC `TXT` at `_dmarc` |
| **Microsoft 365** | MX → `<tenant>.mail.protection.outlook.com`; SPF `TXT` → `v=spf1 include:spf.protection.outlook.com -all`; DKIM (2 CNAMEs from Microsoft); CNAME `autodiscover` → `autodiscover.outlook.com`; DMARC |
| **Zoho Mail** | MX → `mx.zoho.com` (10), `mx2.zoho.com` (20), `mx3.zoho.com` (50); SPF `TXT` → `v=spf1 include:zoho.com ~all`; DKIM from Zoho; DMARC |

**Recommended DMARC to start (monitor only):**
`_dmarc TXT → v=DMARC1; p=none; rua=mailto:dmarc@infitexglobal.com`
Tighten to `p=quarantine` then `p=reject` once you confirm legitimate mail passes.

> Tip: keep email DNS and website DNS in the **same** place to avoid confusion. If you moved nameservers to Cloudflare, add the email records there.

---

## 7. Google Search Console + sitemap

1. Go to **search.google.com/search-console** → add property `https://infitexglobal.com`.
2. Choose the **HTML tag** verification method, copy the `content` value, and paste it over `GOOGLE_SITE_VERIFICATION` in all `.html` files (step 2b). Re-deploy.
3. Once verified → **Sitemaps** → submit `sitemap.xml`.
4. `robots.txt` already references the sitemap and allows crawling (it only disallows the internal `?q=` search URLs).

---

## 8. Analytics (optional)

**Cloudflare Web Analytics** (privacy-friendly, no cookie banner needed): Pages project → **Analytics** → enable. Zero code.

**Google Analytics 4 (GA4):** create a property, copy your `G-XXXXXXX` snippet, and paste it just before `</head>` in each HTML file (or in `_partials.py` `page()` if you regenerate). Note: GA4 uses cookies — if you add it, consider a consent notice.

---

## 9. Editing content later

The pages are plain HTML — you can edit text directly in any editor. If you prefer to regenerate from source, the build tooling is included:

- `_partials.py` — shared header, footer, forms, icons, JSON-LD.
- `build.py` — page content and structure. Run `python3 build.py` to regenerate all six pages.
- `validate.py` — run `python3 validate.py` to re-check structure, links and JSON-LD after edits.

(These three `.py` files and the `_og.svg` are **build sources** — they do **not** need to be uploaded to the live site.)

---

## 10. Built-in features (already working)

- **Dark/light theme toggle** + accessibility panel (text size, high contrast, grayscale) — preferences saved per device.
- **Typed-on-scroll** copy — section intros type out in real time as they enter the viewport (with a blinking caret), and fall back to instant text for `prefers-reduced-motion` and for SEO/screen readers (full text stays in the DOM).
- **Site search** (press `/`) across pages, sections, services and FAQs, with a `?q=` deep link.
- **Savings calculator** — indicative AUD range, no pricing published.
- **FAQ carousel** synced with a full accordion.
- **Floating WhatsApp / email / back-to-top** buttons.

---

## 11. Compliance notes (kept consistent across the site)

- INFITEX is presented as the **preparation & processing layer** — **never** as a registered Australian tax or BAS agent. Lodgement and sign-off stay with the practice. Please keep this language if you edit.
- **No prices** are published anywhere — only "contact us for the best pricing for your practice."
- ISO 27001 is described as **alignment / on roadmap**, not certification.
- Australian English, AUD, DD/MM/YYYY dates, AEST/AEDT, Privacy Act 1988 + APPs, Spam Act 2003 opt-in for the email digest.
- Key compliance dates are marked **indicative — confirm with the ATO.**

---

*Questions about the build? Everything is plain, well-commented HTML/CSS/JS — no hidden dependencies, nothing to compile.*
