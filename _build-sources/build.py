#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the INFITEX static site from shared partials."""
import json, html, re
import _partials as P
from _partials import IC, DOMAIN, ORG_LD, page, breadcrumb, OUT

def ico(name): return IC[name]

def alt_sections(body):
    """Enforce strictly alternating section backgrounds in document order.
    The first content <section class="section"> becomes 'alt', the next plain,
    and so on — so adding/removing sections never breaks the zebra pattern.
    Only matches the content-section wrapper (not .hero, .section-nav, etc.)."""
    state = {"n": 0}
    def repl(m):
        alt = (state["n"] % 2 == 0)
        state["n"] += 1
        return '<section class="section%s"%s' % (" alt" if alt else "", m.group(1))
    return re.sub(r'<section class="section(?: alt)?"(\s|>)', repl, body)

# ---------------------------------------------------------------- dashboard widget
def status_card(cap, rows, foot="Indicative layout — not a live client file."):
    """A 'job status' dashboard panel. rows = list of (label, value, state)
    where state is 'ok' (green), 'warn' (amber) or '' (neutral)."""
    rh = ""
    for label, value, state in rows:
        vc = "v ok" if state == "ok" else ("v warn" if state == "warn" else "v")
        rh += '<div class="ledger-row"><span class="k">%s</span><span class="%s">%s</span></div>' % (label, vc, value)
    return ('<div class="status-card" role="img" aria-label="Illustrative %s dashboard">'
            '<div class="status-card__top"><span class="t">%s</span><span class="dot"></span></div>'
            '%s<div class="status-card__foot">%s</div></div>') % (cap, cap, rh, foot)

def finance_dashboard():
    """Reference-style finance dashboard: KPI cards + bar chart + donut, retoned to Meridian."""
    return ('<div class="dash-visual" role="img" '
        'aria-label="Illustrative finance dashboard with KPIs, a cash-flow trend and a budget breakdown">'
        '<svg class="dash-svg" viewBox="0 0 520 360" xmlns="http://www.w3.org/2000/svg">'
        '<rect x="8" y="8" width="504" height="344" rx="16" fill="var(--bg-2)" stroke="var(--line)"/>'
        '<path d="M8 24a16 16 0 0 1 16-16h472a16 16 0 0 1 16 16v34H8z" fill="var(--bg-3)"/>'
        '<rect x="28" y="26" width="150" height="14" rx="7" fill="var(--muted)" opacity=".55"/>'
        '<rect x="430" y="22" width="62" height="22" rx="11" fill="var(--accent-fill)"/>'
        # 3 KPI cards
        '<g>'
        '<rect x="28" y="76" width="140" height="64" rx="10" fill="var(--bg-3)" stroke="var(--line)"/>'
        '<rect x="44" y="92" width="60" height="8" rx="4" fill="var(--muted)" opacity=".55"/>'
        '<rect x="44" y="108" width="90" height="16" rx="5" fill="var(--positive)"/>'
        '<rect x="184" y="76" width="140" height="64" rx="10" fill="var(--bg-3)" stroke="var(--line)"/>'
        '<rect x="200" y="92" width="60" height="8" rx="4" fill="var(--muted)" opacity=".55"/>'
        '<rect x="200" y="108" width="78" height="16" rx="5" fill="var(--fg)"/>'
        '<rect x="340" y="76" width="152" height="64" rx="10" fill="var(--bg-3)" stroke="var(--line)"/>'
        '<rect x="356" y="92" width="60" height="8" rx="4" fill="var(--muted)" opacity=".55"/>'
        '<rect x="356" y="108" width="70" height="16" rx="5" fill="var(--accent-fill)"/>'
        '</g>'
        # bar chart panel
        '<rect x="28" y="160" width="290" height="168" rx="10" fill="var(--bg-3)" stroke="var(--line)"/>'
        '<rect x="44" y="176" width="120" height="9" rx="4" fill="var(--muted)" opacity=".55"/>'
        '<rect x="60" y="210" width="34" height="40" rx="5" fill="var(--line-2)"/>'
        '<rect x="124" y="192" width="34" height="58" rx="5" fill="var(--line-2)"/>'
        '<rect x="188" y="200" width="34" height="50" rx="5" fill="var(--line-2)"/>'
        '<rect x="252" y="176" width="34" height="74" rx="5" fill="var(--accent)"/>'
        '<rect x="316" y="184" width="34" height="66" rx="5" fill="var(--line-2)"/>'
        '<rect x="380" y="158" width="34" height="92" rx="5" fill="var(--accent)"/>'
        # donut panel
        '<rect x="334" y="160" width="158" height="168" rx="10" fill="var(--bg-3)" stroke="var(--line)"/>'
        '<rect x="350" y="176" width="96" height="9" rx="4" fill="var(--muted)" opacity=".55"/>'
        '<circle cx="413" cy="250" r="40" fill="none" stroke="var(--line-2)" stroke-width="14"/>'
        '<circle cx="413" cy="250" r="40" fill="none" stroke="var(--positive)" stroke-width="14" '
        'stroke-dasharray="150 101" stroke-dashoffset="72" transform="rotate(-90 413 250)" stroke-linecap="round"/>'
        '<circle cx="413" cy="250" r="40" fill="none" stroke="var(--accent-fill)" stroke-width="14" '
        'stroke-dasharray="44 207" stroke-dashoffset="-150" transform="rotate(-90 413 250)" stroke-linecap="round"/>'
        '</svg>'
        '<p class="dash-cap">Indicative finance dashboard — not a live client file.</p></div>')

# ---------------------------------------------------------------- testimonials
TESTIMONIALS = [
    ("INFITEX clears our reconciliations and BAS prep overnight, so the team starts the day ahead instead of behind. The maker–checker review means what lands in our queue is already clean.",
     "Practice Principal", "Boutique accounting firm, VIC"),
    ("Year-end used to swallow our January. Now the workpapers come back to our templates, traceable and ready to sign. We kept lodgement and sign-off exactly where it should be — with us.",
     "Director", "Accounting & advisory practice, NSW"),
    ("We added two seats through tax season without hiring a soul. When it quietened down we scaled back the same week. No recruitment, no overhead hangover.",
     "Operations Manager", "Bookkeeping practice, QLD"),
    ("Our finance function finally feels in-house — named people we actually know, monthly reporting on time, and a Virtual CFO to lean on when the board asks hard questions.",
     "Managing Director", "Construction & trades business, WA"),
    ("They built our new site, sorted the email and the Google profile, and now enquiries actually come through it. One team for the numbers and the website made it painless.",
     "Owner", "Allied health clinic, SA"),
    ("Plain English, quick turnarounds and zero drama. They quietly do the work and we look good in front of our clients. That's exactly what we wanted.",
     "Client Manager", "Accounting practice, ACT"),
    ("The overnight rhythm is the quiet superpower. We send work at close of business and it's reviewed and back in our queue by morning — peak season finally feels manageable.",
     "Partner", "Tax & business services firm, NSW"),
    ("Cash flow used to be a guess. Now we get a rolling 13-week forecast we actually trust, and the monthly pack tells us where to look before problems show up.",
     "Founder", "Retail & e-commerce business, VIC"),
    ("Onboarding was painless — they learned our checklists and software fast, and slotted in without disrupting the team. It genuinely feels like extra hands, not an external vendor.",
     "Finance Manager", "Professional services firm, QLD"),
]

def testimonials_section(items=None, eyebrow="What clients say", title="Trusted by practices and businesses",
                         intro="A few words from the practices and businesses we support across Australia. Names withheld to respect client confidentiality.",
                         id="testimonials", alt=False, slider=False):
    items = items or TESTIMONIALS
    cards = ""
    for quote, who, org in items:
        cards += ('<figure class="tcard"><div class="tquote-mark" aria-hidden="true">&ldquo;</div>'
                  '<blockquote>%s</blockquote>'
                  '<figcaption><span class="tname">%s</span><span class="torg">%s</span></figcaption>'
                  '</figure>') % (quote, who, org)
    if slider:
        prev = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M15 18l-6-6 6-6"/></svg>'
        nxt = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M9 6l6 6-6 6"/></svg>'
        inner = ('<div class="tslider" data-tslider>'
                 '<div class="tslider-viewport"><div class="tslider-track">%s</div></div>'
                 '<div class="tslider-controls">'
                 '<button class="icon-btn tslider-arrow" type="button" data-tprev aria-label="Previous reviews">%s</button>'
                 '<div class="tslider-dots" data-tdots></div>'
                 '<button class="icon-btn tslider-arrow" type="button" data-tnext aria-label="Next reviews">%s</button>'
                 '</div></div>') % (cards, prev, nxt)
    else:
        inner = '<div class="tgrid">%s</div>' % cards
    return section(id, eyebrow, title, intro, inner, alt=alt)

def _sec_visual(caption):
    return ('<div class="sec-visual" aria-hidden="true">'
        '<svg viewBox="0 0 560 420" role="img" xmlns="http://www.w3.org/2000/svg">'
        '<defs>'
        '<linearGradient id="secVault" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="var(--accent-fill)"/><stop offset="1" stop-color="var(--accent)"/></linearGradient>'
        '<linearGradient id="secShield" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="var(--primary-2)" stop-opacity=".30"/><stop offset="1" stop-color="var(--primary)" stop-opacity=".06"/></linearGradient>'
        '</defs>'
        # dashed flight path
        '<path d="M300 70 C 360 44, 420 56, 472 64" fill="none" stroke="var(--accent-2)" stroke-width="2.5" stroke-dasharray="2 8" stroke-linecap="round" opacity=".7"/>'
        # clouds
        '<g fill="var(--line-2)" opacity=".55">'
        '<g><circle cx="118" cy="82" r="13"/><circle cx="138" cy="76" r="17"/><circle cx="158" cy="84" r="12"/><rect x="116" y="82" width="46" height="14" rx="7"/></g>'
        '<g opacity=".85"><circle cx="432" cy="118" r="10"/><circle cx="448" cy="112" r="13"/><rect x="430" y="116" width="34" height="11" rx="5.5"/></g></g>'
        # paper plane
        '<g><path d="M452 84 l54 -24 -16 42 -17 -15 -21 -3z" fill="var(--accent)"/>'
        '<path d="M506 60 l-33 27 -4 18" fill="none" stroke="var(--bg-2)" stroke-width="2.5" stroke-linejoin="round" opacity=".55"/></g>'
        # password field
        '<g><rect x="70" y="104" width="128" height="32" rx="16" fill="var(--bg-2)" stroke="var(--line)" stroke-width="2"/>'
        '<g fill="var(--accent)"><circle cx="92" cy="120" r="5"/><circle cx="112" cy="120" r="5"/><circle cx="132" cy="120" r="5"/><circle cx="152" cy="120" r="5"/><circle cx="172" cy="120" r="5"/></g></g>'
        # ground line
        '<g stroke="var(--line-2)" stroke-width="4" stroke-linecap="round">'
        '<path d="M80 388 H300"/><path d="M326 388 H356"/><path d="M384 388 H474"/></g>'
        # folder (open)
        '<g><path d="M120 296 q0 -10 10 -10 h120 q10 0 10 10 v66 q0 10 -10 10 h-120 q-10 0 -10 -10 z" fill="var(--primary)"/>'
        '<rect x="150" y="276" width="92" height="58" rx="5" fill="var(--bg-2)"/>'
        '<g fill="var(--line-2)"><rect x="160" y="290" width="72" height="6" rx="3"/><rect x="160" y="304" width="56" height="6" rx="3"/></g>'
        '<path d="M120 312 l14 -10 h112 q10 0 10 10 v40 q0 10 -10 10 h-126 q-10 0 -10 -10 z" fill="var(--primary-2)"/></g>'
        # magnifier
        '<g><line x1="203" y1="211" x2="238" y2="246" stroke="var(--primary-2)" stroke-width="13" stroke-linecap="round"/>'
        '<circle cx="176" cy="188" r="37" fill="var(--bg-3)" stroke="var(--primary)" stroke-width="7"/>'
        '<path d="M162 174 a20 20 0 0 1 16 -7" fill="none" stroke="var(--bg-2)" stroke-width="4" stroke-linecap="round" opacity=".7"/></g>'
        # vault / padlock
        '<path d="M286 152 v-20 a52 52 0 0 1 104 0 v20" fill="none" stroke="var(--primary)" stroke-width="17" stroke-linecap="round"/>'
        '<rect x="252" y="150" width="168" height="196" rx="24" fill="url(#secVault)"/>'
        '<rect x="252" y="196" width="168" height="22" fill="#000" fill-opacity=".12"/>'
        '<circle cx="336" cy="276" r="33" fill="var(--bg-2)"/>'
        '<circle cx="336" cy="267" r="9" fill="var(--accent)"/>'
        '<path d="M336 270 l9 26 h-18 z" fill="var(--accent)"/>'
        # shield + check
        '<path d="M454 250 l48 17 v34 c0 35 -24 58 -48 70 -24 -12 -48 -35 -48 -70 v-34 z" fill="url(#secShield)" stroke="var(--primary)" stroke-width="5"/>'
        '<path d="M432 300 l15 15 27 -29" fill="none" stroke="var(--positive)" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'
        # decorative crosses, rings & dots
        '<g stroke="var(--accent-2)" stroke-width="3" stroke-linecap="round" opacity=".8">'
        '<path d="M64 220 l11 11 M75 220 l-11 11"/><path d="M236 116 l9 9 M245 116 l-9 9"/><path d="M404 150 l9 9 M413 150 l-9 9"/></g>'
        '<g fill="none" stroke="var(--accent)" stroke-width="3" opacity=".7"><circle cx="512" cy="208" r="7"/><circle cx="92" cy="300" r="6"/></g>'
        '<g fill="var(--accent-2)" opacity=".6"><circle cx="300" cy="118" r="4"/><circle cx="484" cy="300" r="4"/></g>'
        '</svg>'
        '<p class="sec-cap">%s</p></div>') % caption

def security_section(id, eyebrow, title, intro, feats_html, caption, alt=False):
    """Security section: heading + intro + feature list in the left column,
    the data-security visual filling the right column (vertically centred)."""
    h2id = id + "-title"
    head = ('<div class="section-head" style="margin-bottom:22px">'
            '<span class="eyebrow">%s</span>'
            '<h2 class="section-title" id="%s">%s</h2>'
            '<p class="lead" data-tw>%s</p></div>') % (eyebrow, h2id, title, intro)
    left = '<div class="sec-main">%s%s</div>' % (head, feats_html)
    inner = '<div class="split-2 split-2--rev sec-split">%s%s</div>' % (left, _sec_visual(caption))
    cls = "section alt" if alt else "section"
    return '<section class="%s" id="%s" aria-labelledby="%s"><div class="shell">%s</div></section>' % (cls, id, h2id, inner)

def security_split(feats_html, caption):
    return '<div class="split-2 split-2--rev">%s%s</div>' % (feats_html, _sec_visual(caption))

# ---------------------------------------------------------------- helpers
def section(id, eyebrow, title, intro, inner, alt=False, title_tw=False):
    cls = "section alt" if alt else "section"
    head = '<div class="section-head">'
    if eyebrow: head += '<span class="eyebrow">%s</span>' % eyebrow
    h2id = ""
    if title:
        tw = ' data-tw' if title_tw else ''
        h2id = "%s-title" % id
        head += '<h2 class="section-title" id="%s"%s>%s</h2>' % (h2id, tw, title)
    if intro:  head += '<p class="lead" data-tw>%s</p>' % intro
    head += '</div>'
    labelledby = ' aria-labelledby="%s"' % h2id if h2id else ''
    return '<section class="%s" id="%s"%s><div class="shell">%s%s</div></section>' % (cls, id, labelledby, head, inner)

def card(icon, h, p, more=None, more_label="Learn more"):
    m = '<a class="more" href="%s">%s →</a>' % (more, more_label) if more else ''
    return ('<article class="card"><div class="ico">%s</div><h3>%s</h3><p>%s</p>%s</article>'
            % (ico(icon), h, p, m))

def step(h, p):
    return '<div class="step"><div class="num"></div><div><h3>%s</h3><p>%s</p></div></div>' % (h, p)

def feat(icon, b, p):
    return '<li><div class="ico">%s</div><div><b>%s</b><p>%s</p></div></li>' % (ico(icon), b, p)

# ---------------------------------------------------------------- shared: contact section
def contact_section(page_mode=False):
    form = ('<form id="contactForm" class="card" novalidate>'
        '<h3 class="mt-0">Send an enquiry</h3>'
        '<p class="form-note" style="margin:4px 0 14px">We reply by email — see our <a href="privacy.html">Privacy</a> page.</p>'
        + P.lead_fields("contact") +
        '<button type="submit" class="btn btn-primary btn-block">Send enquiry</button>'
        '<p class="form-status" id="contactStatus" role="status"></p>'
        '</form>')
    cards = ('<div class="contact-cards contact-cards--compact">'
        '<article class="card cc-row"><div class="ico">%s</div><div class="cc-body"><h3>WhatsApp</h3>'
        '<p>We\'ll draft a tidy message and open WhatsApp for you.</p>'
        '<button class="btn btn-ghost btn-sm" data-open-wa>Start a WhatsApp enquiry</button></div></article>'
        '<article class="card cc-row"><div class="ico">%s</div><div class="cc-body"><h3>Book a 15-minute call</h3>'
        '<p>A short, no-pressure intro call to see whether we\'re a fit.</p>'
        '<a class="btn btn-ghost btn-sm" data-booking href="contact.html">Book a time</a></div></article>'
        '<article class="card cc-row"><div class="ico">%s</div><div class="cc-body"><h3>Email</h3>'
        '<p>Drop us a line and we\'ll reply by email, usually within one business day.<br>'
        '<a href="mailto:info@infitexglobal.com">info@infitexglobal.com</a><br>'
        '<a href="tel:+918500850526">+91 8500 850 526</a> · AEST/AEDT-friendly hours</p>'
        '<button class="btn btn-ghost btn-sm" data-open-mail>Email us</button></div></article>'
        '<article class="card cc-row cc-qr"><button type="button" class="qr-mini" data-open-qr aria-label="Show QR code to save our contact"><img src="infitex-contact-qr.svg" '
        'alt="QR code to save INFITEX Global Advisory contact details" width="92" height="92" loading="lazy"></button>'
        '<div class="cc-body"><h3>Save our contact</h3>'
        '<p>Tap the code (or scan with your phone camera) to save us — name, mobile and email. Works on iPhone &amp; Android, no app needed.</p></div></article>'
        '</div>') % (ico("wa"), ico("cal"), ico("mail"))
    inner = '<div class="contact-grid">%s%s</div>' % (form, cards)
    if page_mode:
        return ('<section class="section" id="contact" aria-label="Contact form and options">'
                '<div class="shell">%s</div></section>') % inner
    return section("contact", "Contact", "Talk to us about your practice",
                   "Tell us what you need help with and we will come back to you by email. No obligation, and no pressure to commit.",
                   inner, alt=False)

def subscribe_section():
    form = ('<form id="subscribeForm" class="card" novalidate>'
        '<ul class="sub-perks">'
        '<li>%s Quarterly BAS &amp; monthly IAS reminders</li>'
        '<li>%s Super guarantee &amp; STP finalisation dates</li>'
        '<li>%s One tidy email — no spam, unsubscribe anytime</li>'
        '</ul>'
        '<div class="form-row"><label class="lbl" for="sub-email">Email <span class="req">*</span></label>'
        '<input class="input" id="sub-email" name="email" type="email" inputmode="email" autocomplete="email" required>'
        '<span class="field-err">Please enter a valid email address.</span></div>'
        '<label class="optin"><input type="checkbox" required>'
        '<span>I agree to receive the compliance-dates digest and accept the '
        '<a href="privacy.html">Privacy</a> terms. I can unsubscribe at any time (Spam Act 2003 compliant).</span></label>'
        '<button type="submit" class="btn btn-primary" style="margin-top:16px">Subscribe</button>'
        '<p class="form-status" id="subStatus" role="status"></p>'
        '</form>') % (ico("check"), ico("check"), ico("check"))
    preview = ('<div class="digest-preview"><div class="term-bar"><i></i><i></i><i></i>'
        '<span style="margin-left:8px;font-family:var(--font-mono);font-size:.74rem;color:var(--muted)">inbox — what you\'ll get</span></div>'
        '<div class="dp-body"><span class="dp-tag">Sample digest</span>'
        '<div class="dp-row"><span>Q2 BAS (Oct–Dec)</span><span class="d">28/02/2026</span></div>'
        '<div class="dp-row"><span>Monthly IAS</span><span class="d">21/02/2026</span></div>'
        '<div class="dp-row"><span>Super guarantee (Q3)</span><span class="d">28/04/2026</span></div>'
        '<div class="dp-row"><span>STP finalisation</span><span class="d">14/07/2026</span></div>'
        '<p class="note" style="margin:14px 0 0">Indicative reminders only — always confirm with the ATO. One tidy email, no spam.</p>'
        '</div></div>')
    inner = '<div class="digest-grid">%s%s</div>' % (form, preview)
    return section("subscribe", "Stay in the loop", "Australian compliance-dates digest",
                   "An occasional, opt-in email with upcoming BAS, IAS, super and tax reference dates. No spam, unsubscribe anytime.",
                   inner, alt=True)

def cta_band(title, text, primary=("Request a pilot", "contact.html"), ghost=("Book a call", None)):
    g = '<a class="btn btn-ghost" data-booking href="contact.html">%s</a>' % ghost[0] if ghost[1] is None else '<a class="btn btn-ghost" href="%s">%s</a>' % (ghost[1], ghost[0])
    inner = ('<div class="cta-band"><span class="eyebrow">Low-risk pilot</span>'
        '<h2 data-tw>%s</h2><p class="lead" style="margin-inline:auto;max-width:60ch" data-tw>%s</p>'
        '<div class="hero-cta"><a class="btn btn-primary" href="%s">%s</a>%s</div></div>'
        % (title, text, primary[1], primary[0], g))
    return inner

# ---------------------------------------------------------------- software stack
STACK = [
    ("Xero", "#13B5EA"), ("XPM", "#13B5EA"), ("MYOB", "#6100A5"),
    ("QuickBooks", "#2CA01C"), ("Reckon", "#0072CE"), ("FYI Docs", "#1F8EFA"),
    ("Dext", "#00B289"), ("Hubdoc", "#00A4E4"), ("BGL / Class", "#E8542E"),
    ("Karbon", "#6C5CE7"),
]
def stack_strip():
    chips = "".join('<span class="stack-chip"><span class="dot" style="background:%s"></span>%s</span>' % (c, n) for n, c in STACK)
    return '<div class="stack-strip">%s</div>' % chips

# ---------------------------------------------------------------- FAQ data (13)
FAQS = [
 ("Do you contact our clients directly?",
  "No. You keep the client relationship end to end. We work in the background as your white-label team, and nothing we produce carries our name. Your clients only ever deal with your practice."),
 ("Are you a registered Australian tax or BAS agent?",
  "No, and we never present ourselves as one. INFITEX is the preparation and processing layer behind your practice. Your registered agents retain all lodgement and sign-off responsibilities under the Tax Agent Services Act."),
 ("Who lodges and signs off the work?",
  "Your practice does. We prepare and process to your standards and hand the work back for your review, sign-off and lodgement. Final professional judgement always stays with you."),
 ("What tasks can you take on?",
  "Bookkeeping and reconciliations, accounts payable and receivable, payroll and STP, BAS and IAS preparation, year-end financials, company and trust tax returns, SMSF accounts and clean workpapers behind every job."),
 ("Which software do you work in?",
  "The tools you already use — Xero, XPM, MYOB, QuickBooks, Reckon, FYI Docs, Dext, Hubdoc, BGL and Class, and Karbon. We adapt to your stack and workflows rather than asking you to change."),
 ("How do you keep our data secure?",
  "Role-based access, named individuals on your jobs, confidentiality agreements and least-privilege access to your systems. We are aligning our controls to ISO 27001 — certification is on our roadmap, not a current claim."),
 ("Do you use a maker–checker review?",
  "Yes. Work is prepared by one team member and independently reviewed by another before it reaches you, so what lands in your queue is already checked and traceable."),
 ("What turnaround can we expect?",
  "Turnaround depends on scope and volume, and we agree it with you up front. The India–Australia time difference often means work moves overnight, so jobs can be ready for your morning."),
 ("Can we start with a trial?",
  "Yes. We recommend a low-risk pilot on a defined scope — a handful of files or one work type — so you can judge quality and fit before scaling up."),
 ("Are we locked into a contract?",
  "No long lock-in. We earn the relationship through quality and reliability. Engagement models are flexible and can scale up or down as your practice needs change."),
 ("How does the time-zone difference help us?",
  "Work prepared during Australian evening hours can be ready for your team the next morning, which helps smooth peak-period workloads without adding local headcount."),
 ("Why don't you publish pricing?",
  "Because the right price depends on your scope, volume and software. We tailor it to your practice rather than forcing you into a fixed tier — contact us for the best pricing for your practice."),
 ("Do you also build websites and do SEO?",
  "Yes — through our Digitech division. Websites, domains, hosting, business email, SEO and Google Business Profile, built for accounting and bookkeeping practices."),
]
def faq_slides():
    s = ""
    for i, (q, a) in enumerate(FAQS[:6]):
        s += '<div class="faq-slide%s"><p class="faq-q">%s</p><p class="faq-a">%s</p></div>' % (" active" if i == 0 else "", q, a)
    return s
def faq_accordion():
    items = "".join('<details class="faq-item"><summary>%s</summary><p>%s</p></details>' % (q, a) for q, a in FAQS)
    return ('<details class="faq-accordion"><summary>Show all %d questions</summary><div>%s</div></details>'
            % (len(FAQS), items))
def faq_ld():
    return json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS]
    }, ensure_ascii=False)

# ---------------------------------------------------------------- key dates
DATES = [
 ("Q1 BAS (Jul–Sep)", "28/10/2025", "Quarterly activity statement"),
 ("Q2 BAS (Oct–Dec)", "28/02/2026", "Quarterly activity statement"),
 ("Q3 BAS (Jan–Mar)", "28/04/2026", "Quarterly activity statement"),
 ("Q4 BAS (Apr–Jun)", "28/07/2026", "Quarterly activity statement"),
 ("Monthly IAS", "21st of the month", "Instalment / activity statement"),
 ("Super guarantee (quarterly)", "28/01 · 28/04 · 28/07 · 28/10", "Employer SG contributions"),
 ("STP finalisation", "14/07/2026", "Single Touch Payroll end-of-year"),
 ("Company tax return", "Varies by lodgement program", "Confirm your concession dates"),
]
def dates_table():
    rows = "".join('<tr><td>%s</td><td class="date">%s</td><td>%s</td></tr>' % d for d in DATES)
    return ('<div style="overflow-x:auto"><table class="dates-table"><caption class="sr-only">Indicative Australian compliance dates</caption>'
            '<thead><tr><th>Obligation</th><th>Indicative date</th><th>Notes</th></tr></thead>'
            '<tbody>%s</tbody></table></div>'
            '<p class="note" style="margin-top:14px">Indicative only and subject to change — always confirm current dates with the ATO and your lodgement program.</p>' % rows)

def dates_section(alt=False):
    return section("dates", "Key Australian dates", "Compliance dates at a glance",
        "A quick reference for common Australian obligations. Always confirm current dates with the ATO.",
        dates_table(), alt=alt)

# ---------------------------------------------------------------- calculator
def calculator():
    return ('<div class="calc" id="calc">'
        '<div>'
        '<div class="field"><label for="calcStaff">Local staff on compliance work</label>'
        '<input type="range" id="calcStaff" min="1" max="20" value="3" step="1">'
        '<div class="rowval"><span>How many people</span><b id="calcStaffV">3</b></div></div>'
        '<div class="field"><label for="calcHours">Hours per person, per week</label>'
        '<input type="range" id="calcHours" min="2" max="40" value="12" step="1">'
        '<div class="rowval"><span>Outsourceable hours</span><b id="calcHoursV">12</b></div></div>'
        '<div class="field"><label for="calcRate">Loaded local cost (AUD/hour)</label>'
        '<input type="range" id="calcRate" min="35" max="120" value="65" step="5">'
        '<div class="rowval"><span>Per hour</span><b id="calcRateV">$65/hr</b></div></div>'
        '</div>'
        '<div class="calc-out">'
        '<span class="eyebrow">Indicative annual saving</span>'
        '<div class="figure"><span id="calcLow">$0</span> – <span id="calcHigh">$0</span></div>'
        '<p class="note" style="margin-top:14px">Based on <span id="calcHrs">0 hrs/yr</span> of outsourceable work and an indicative 40–60% saving band across ~46 working weeks. This is an indicative estimate in AUD, not a quote — contact us for the best pricing for your practice.</p>'
        '</div></div>')

# ---------------------------------------------------------------- section nav (home)
def section_nav():
    items = [("Who we help", "#who"), ("Stack", "#stack"),
             ("Engagement", "#engagement"), ("Security", "#security"), ("Calculator", "#calculator"),
             ("Reviews", "#testimonials"), ("About", "#about"), ("FAQ", "#faq"), ("Contact", "contact.html")]
    lis = "".join('<li><a href="%s">%s</a></li>' % (u, n) for n, u in items)
    return '<nav class="section-nav" aria-label="On this page"><div class="shell"><ul>%s</ul></div></nav>' % lis

# ================================================================ HOME
def build_home():
    hero = ('<section class="hero hero-grid" id="top"><div class="shell"><div class="hero-inner">'
        '<div>'
        '<span class="eyebrow">Outsourced accounting, finance &amp; Virtual CFO · Australia</span>'
        '<h1>Your standards. Our expertise.</h1>'
        '<p class="answer-lede">INFITEX Global Advisory is an India-based, white-label accounting and bookkeeping outsourcing partner for Australian accounting practices and businesses — covering bookkeeping, payroll and STP, BAS, year-end, tax, SMSF, management reporting and Virtual CFO, while your practice keeps lodgement and sign-off.</p>'
        '<ul class="hero-paths hero-paths--list">'
        '<li><a class="path-chip" href="outsourcing.html"><b>For practices</b> <span>— White-label</span></a></li>'
        '<li><a class="path-chip" href="industry.html"><b>For business</b> <span>— Finance &amp; Virtual CFO</span></a></li>'
        '<li><a class="path-chip" href="digitech.html"><b>Digitech</b> <span>— Web &amp; SEO</span></a></li></ul>'
        '</div>'
        '<div class="hero-aside">'
        '<aside class="hero-pilot" aria-labelledby="hero-pilot-title">'
        '<span class="eyebrow">Low-risk pilot</span>'
        '<h2 id="hero-pilot-title">Start with a low-risk pilot</h2>'
        '<p>Pick a small, defined scope. See the quality, the communication and the turnaround for yourself before you scale.</p>'
        '<div class="hero-cta"><a class="btn btn-primary" href="contact.html">Request a pilot</a>'
        '<a class="btn btn-ghost" data-booking href="contact.html">Book a 15-min call</a></div>'
        '</aside>'
        '<div class="hero-contact" aria-label="Quick contact options">'
        '<span class="eyebrow">Talk to us</span>'
        '<div class="hero-contact-actions">'
        '<button type="button" class="hc-btn" data-open-wa><span class="hc-ic">%s</span><span>WhatsApp us</span></button>'
        '<a class="hc-btn" href="contact.html"><span class="hc-ic">%s</span><span>Send an enquiry</span></a>'
        '<button type="button" class="hc-btn" data-open-mail><span class="hc-ic">%s</span><span>Email us</span></button>'
        '<button type="button" class="hc-btn" data-open-qr><span class="hc-ic">%s</span><span>Save our contact</span></button>'
        '</div></div>'
        '</div>'
        '</div></div></section>') % (ico("wa"), ico("doc"), ico("mail"), ico("qr"))

    who = ('<div class="grid grid-2">'
        '<article class="division card"><span class="tag">Who we help · 01</span>'
        '<div class="ico">%s</div><h3>Accounting &amp; bookkeeping practices</h3>'
        '<p>A white-label back office for your firm. We prepare and process the full compliance cycle behind your brand; your practice keeps the client, the lodgement and the sign-off.</p>'
        '<a class="more" href="outsourcing.html">For practices →</a></article>'
        '<article class="division card"><span class="tag">Who we help · 02</span>'
        '<div class="ico">%s</div><h3>Businesses &amp; industry</h3>'
        '<p>A dedicated finance team for your company — bookkeeping, payroll, management accounts and Virtual CFO. Lodgement is handled through a registered BAS/tax agent (yours or a partner).</p>'
        '<a class="more" href="industry.html">For business →</a></article>'
        '</div>') % (ico("users"), ico("building"))
    s_who = section("who", "Who we help", "Two audiences, one finance partner",
        "Whether you run an accounting practice or a growing business, INFITEX slots in as the team behind your numbers.",
        who)

    s_stack = section("stack", "Native to your stack", "We work in the tools you already use",
        "No migrations, no retraining your team. We slot into your existing software and workflows.",
        stack_strip(), alt=True)

    divisions = ('<div class="grid grid-2">'
        '<article class="division card"><span class="tag">Core division</span>'
        '<div class="ico">%s</div><h3>Accounting &amp; bookkeeping outsourcing</h3>'
        '<p>Your white-label back office for the full Australian compliance cycle — bookkeeping, payroll and STP, BAS and IAS, year-end financials, tax returns and SMSF. Prepared and reviewed, ready for your sign-off.</p>'
        '<a class="more" href="outsourcing.html">Explore outsourcing →</a></article>'
        '<article class="division card"><span class="tag">Secondary division</span>'
        '<div class="ico">%s</div><h3>Digitech</h3>'
        '<p>Practical digital services for practices — websites, domains, hosting, business email, SEO and Google Business Profile — so your firm looks as sharp online as the work you deliver.</p>'
        '<a class="more" href="digitech.html">Explore Digitech →</a></article>'
        '</div>') % (ico("stack"), ico("globe"))
    s_div = section("divisions", "Two divisions, one partner", "Everything your practice needs behind the scenes",
        "A dependable extension of your team for the numbers, and a digital partner for everything client-facing online.",
        divisions)

    steps = ('<div class="steps">'
        + step("Scoping call", "We learn how your practice works — software, file types, review standards and the work you'd like to hand over.")
        + step("Low-risk pilot", "We start small on a defined scope so you can judge quality, communication and turnaround before scaling.")
        + step("Prepare &amp; process", "Our named team does the work in your systems, to your templates and checklists.")
        + step("Maker–checker review", "A second reviewer independently checks the job, so what reaches you is already verified and traceable.")
        + step("Handover for sign-off", "You review, sign off and lodge. Final professional judgement always stays with your practice.")
        + '</div>')
    s_how = section("how", "How it works", "A simple, low-risk way to slot into your practice",
        "No big-bang changeover. We earn trust on a small scope first, then scale at your pace.", steps)

    eng = ('<div class="grid grid-3">'
        + card("users", "Dedicated staff", "A named team member (or team) working only on your practice — like hiring, without the overheads or recruitment risk.", )
        + card("doc", "Per-job", "Send work as it comes — individual files, returns or BAS jobs — and we turn them around to your standards.")
        + card("bolt", "Ad-hoc &amp; overflow", "Extra hands during peak periods, leave cover or a backlog clear-out. Flexible, with no long lock-in.")
        + '</div>'
        '<p class="note" style="margin-top:18px">We don\'t publish prices because the right model depends on your scope, volume and software. Contact us for the best pricing for your practice.</p>')
    s_eng = section("engagement", "Engagement models", "Flexible ways to work together",
        "Choose the model that suits your practice today — and change it as your needs change.", eng)

    sec_feats = ('<ul class="feature-list feature-grid-2">'
        + feat("lock", "Role-based, least-privilege access", "Named individuals only, with access scoped to the systems and files each job needs.")
        + feat("shield", "Confidentiality by default", "Signed confidentiality agreements and clear handling rules for client data.")
        + feat("check", "Maker–checker controls", "Independent review on every job before it reaches your queue.")
        + feat("cog", "ISO 27001 alignment (on roadmap)", "We are aligning our controls to ISO 27001. This is a direction of travel, not a current certification claim.")
        + '</ul>')
    s_sec = security_section("security", "Security &amp; trust", "Your clients' data, handled carefully",
        "Security isn't a bolt-on. It's how we set up every engagement from day one.",
        sec_feats, "Every engagement is set up with scoped access, independent review and signed confidentiality.")

    dig = ('<div class="grid grid-3">'
        + card("globe", "Websites that convert", "Fast, accessible, mobile-first sites built for accounting and bookkeeping practices.", "digitech.html")
        + card("mail", "Domains, hosting &amp; email", "Domain setup, reliable hosting and professional business email, configured for you.", "digitech.html")
        + card("search", "SEO &amp; Google Business Profile", "Be found by local clients searching for an accountant or bookkeeper.", "digitech.html")
        + '</div>')
    s_dig = section("digitech", "Digitech", "Look as sharp online as your work",
        "Our secondary division handles the digital side so you don't have to juggle multiple vendors.", dig)

    _bprev = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M15 18l-6-6 6-6"/></svg>'
    _bnxt = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M9 6l6 6-6 6"/></svg>'
    soft_savings = ('<div class="soft-savings">'
        '<p class="eyebrow" style="margin-bottom:14px">Beyond the dollars</p>'
        '<div class="tslider tslider--2up" data-tslider>'
        '<div class="tslider-viewport"><div class="tslider-track">'
        + card("bolt", "Fewer payroll panics", "Pay runs and STP handled on a steady rhythm — no Friday-night scramble before a deadline.")
        + card("shield", "Lower compliance tension", "BAS, IAS and super dates tracked and prepared early, so nothing sneaks up on you.")
        + card("clock", "Hours back in your week", "Routine processing leaves your desk, freeing senior people for advice and client time.")
        + card("users", "Less hiring stress", "Add capacity without recruiting, onboarding or carrying permanent overhead through quiet months.")
        + card("check", "Consistent, reviewed output", "Every job goes through maker–checker review, so what reaches you is clean and traceable.")
        + card("trend", "Capacity that flexes", "Scale up for busy periods and back down when it quietens — without long lock-in or fixed overhead.")
        + '</div></div>'
        '<div class="tslider-controls">'
        '<button class="icon-btn tslider-arrow" type="button" data-tprev aria-label="Previous benefits">%s</button>'
        '<div class="tslider-dots" data-tdots></div>'
        '<button class="icon-btn tslider-arrow" type="button" data-tnext aria-label="Next benefits">%s</button>'
        '</div></div>'
        '<p class="note" style="margin-top:16px">Harder to put a number on — but often the first thing practices say they notice.</p>'
        '</div>') % (_bprev, _bnxt)
    s_calc = section("calculator", "Savings calculator", "Estimate what outsourcing could free up",
        "Move the sliders for an indicative annual range in AUD. It's a guide to start a conversation, not a quote.",
        calculator() + soft_savings, alt=True)

    s_dates = section("dates", "Key Australian dates", "Compliance dates at a glance",
        "A quick reference for common Australian obligations. Always confirm current dates with the ATO.",
        dates_table())

    about = ('<div class="about-snippet">'
        '<p class="lead">INFITEX Global Advisory is an India-based, white-label accounting outsourcing and Digitech partner built for Australian practices and businesses. Our leadership and senior reviewers bring 8+ years of hands-on Australian compliance experience — and we keep the line clear: we prepare and process to your standards, while your practice keeps the client, the lodgement and the sign-off.</p>'
        '<div class="vmb-grid vmb-grid--mini">'
        '<article class="vmb-card"><div class="ico">%s</div><h3>Vision</h3><p>The most trusted offshore finance &amp; Digitech partner for Australia — invisible to your clients, indispensable to you.</p></article>'
        '<article class="vmb-card"><div class="ico">%s</div><h3>Mission</h3><p>Dependable capacity and clarity — accurate preparation, on time, to your standards.</p></article>'
        '<article class="vmb-card"><div class="ico">%s</div><h3>We believe</h3><p>The compliance line is sacred, and good work plus plain English beats hype.</p></article>'
        '</div>'
        '<div style="margin-top:22px"><a class="btn btn-primary" href="about.html">Read more about INFITEX →</a></div>'
        '</div>') % (ico("target"), ico("bolt"), ico("check"))
    s_about = section("about", "About INFITEX", "A quiet, reliable extension of your practice",
        "Built for Australian practices, careful with the compliance line, and easy to work with.", about)

    s_faq = section("faq", "FAQ", "Questions practices ask us",
        "The honest answers — especially on the compliance line, security and how we work.",
        ('<div class="faq-spotlight"><div class="faq-stage" id="faqStage">%s</div>'
         '<div class="faq-controls"><button class="icon-btn" id="faqPrev" aria-label="Previous question">%s</button>'
         '<div class="faq-dots" id="faqDots"></div>'
         '<button class="icon-btn" id="faqNext" aria-label="Next question">%s</button></div>'
         '<div class="faq-progress"><span></span></div>'
         '%s</div>') % (faq_slides(),
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M15 18l-6-6 6-6"/></svg>',
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M9 6l6 6-6 6"/></svg>',
            faq_accordion()),
        alt=True)

    s_pilot = '<section class="section" id="pilot"><div class="shell">%s</div></section>' % cta_band(
        "Start with a low-risk pilot",
        "Pick a small, defined scope. See the quality, the communication and the turnaround for yourself before you scale.")

    s_test = testimonials_section(eyebrow="Our stories", alt=True, slider=True)

    body = (hero + section_nav() + s_stack + s_who + s_div + s_eng + s_sec
            + s_dig + s_calc + s_test + s_about + s_faq)
    body = alt_sections(body)

    website_ld = json.dumps({
        "@context": "https://schema.org", "@type": "WebSite",
        "@id": DOMAIN + "/#website",
        "name": "INFITEX Global Advisory", "url": DOMAIN + "/",
        "publisher": {"@id": DOMAIN + "/#organization"},
        "inLanguage": "en-AU",
        "potentialAction": {"@type": "SearchAction",
            "target": {"@type": "EntryPoint", "urlTemplate": DOMAIN + "/index.html?q={search_term_string}"},
            "query-input": "required name=search_term_string"}
    }, ensure_ascii=False)
    home_service_ld = json.dumps({
        "@context": "https://schema.org", "@type": "Service",
        "serviceType": "White-label accounting & bookkeeping outsourcing",
        "provider": {"@id": DOMAIN + "/#organization"},
        "areaServed": {"@type": "Country", "name": "Australia"},
        "description": "White-label preparation and processing across the Australian compliance cycle — bookkeeping, payroll and STP, BAS and IAS, year-end, tax, SMSF — plus management reporting and Virtual CFO. The client practice retains lodgement and sign-off.",
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "INFITEX services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Accounting & bookkeeping outsourcing"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Payroll, BAS & compliance preparation"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Virtual CFO & management reporting"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Digitech — websites, email & SEO"}},
        ]}
    }, ensure_ascii=False)
    graph = '{"@context":"https://schema.org","@graph":[%s,%s,%s,%s,%s]}' % (
        ORG_LD, website_ld, home_service_ld, faq_ld(),
        breadcrumb([("Home", "index.html")]))
    return page("index.html",
        "White-label accounting outsourcing, Australia | INFITEX",
        "White-label accounting, bookkeeping & Virtual CFO outsourcing for Australian practices and businesses. We prepare; you keep lodgement & sign-off.",
        body, graph, section_nav=True)

# ================================================================ OUTSOURCING (FOR PRACTICES)
def build_outsourcing():
    crumb = '<div class="shell"><nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> / <span>For Practices</span></nav></div>'
    hero = ('<section class="hero"><div class="shell hero-2col">'
        '<div class="hero-copy">'
        '<span class="eyebrow">Who we help · Accounting practices</span>'
        '<h1>Your outsourced <span class="accent">compliance</span> team.</h1>'
        '<p class="answer-lede">For Australian accounting practices, INFITEX prepares and reviews the full compliance cycle — bookkeeping, payroll and STP, BAS and IAS, year-end financials, tax returns and SMSF — under your brand and to your standards, then hands it back for your sign-off and lodgement.</p>'
        '<p class="hero-sub" data-tw>The full Australian compliance cycle — prepared and reviewed to your standards, then handed back for your sign-off and lodgement. Always under your brand, never in front of your clients.</p>'
        '<p class="hero-sub">INFITEX is the back office behind Australian accounting practices — from bookkeeping and payroll through to year-end, tax and management reporting. Native to Xero, XPM, MYOB and the tools you already use.</p>'
        '<div class="hero-cta"><a class="btn btn-primary" href="contact.html">Request a pilot</a>'
        '<a class="btn btn-ghost" data-booking href="contact.html">Book a call</a></div>'
        '<div class="hero-paths" style="margin-top:18px"><span class="path-chip" style="border-color:var(--accent);color:var(--accent)"><b>For practices</b></span>'
        '<a class="path-chip" href="industry.html">Run a business instead? <b>For business →</b></a></div>'
        '</div>'
        + status_card("Job status · sample", [
            ("Bank reconciliation", "Matched", "ok"),
            ("BAS (Jul–Sep)", "Prepared", "ok"),
            ("Payroll &amp; STP", "Finalised", "ok"),
            ("Year-end workpapers", "Linked", "ok"),
            ("Your review &amp; sign-off", "With you", ""),
        ]) +
        '</div></section>')

    scope = ('<ul class="cycle-list cycle-list--2col">'
        '<li><span class="mark">01</span><div><b>Bookkeeping &amp; reconciliations</b><span>Day-to-day books kept accurate, coded and current.</span></div></li>'
        '<li><span class="mark">02</span><div><b>Accounts payable &amp; receivable</b><span>Bills and invoices processed, matched and chased.</span></div></li>'
        '<li><span class="mark">03</span><div><b>Payroll &amp; STP</b><span>Pay runs prepared and Single Touch Payroll ready for lodgement.</span></div></li>'
        '<li><span class="mark">04</span><div><b>BAS / IAS preparation</b><span>Activity statements drafted for your review and lodgement.</span></div></li>'
        '<li><span class="mark">05</span><div><b>Year-end financials &amp; tax</b><span>Financial statements and company/trust returns prepared to your standards.</span></div></li>'
        '<li><span class="mark">06</span><div><b>SMSF &amp; workpapers</b><span>SMSF accounts in BGL/Class with clean, traceable workpapers.</span></div></li>'
        '</ul>')
    s_scope = section("scope", "Scope of work", "From source documents to sign-off-ready",
        "Hand over as much or as little as you like — from a single work type to the whole compliance cycle, so your team can focus on advice, relationships and growth.", scope)

    job = ('<div class="jobtable-wrap">'
        '<table class="jobtable"><caption>Recurring work</caption>'
        '<thead><tr><th>Job</th><th>Typical frequency</th></tr></thead><tbody>'
        '<tr><td>Bank &amp; ledger reconciliations</td><td>Weekly</td></tr>'
        '<tr><td>Accounts payable / receivable</td><td>Weekly</td></tr>'
        '<tr><td>Payroll &amp; STP</td><td>Weekly / fortnightly</td></tr>'
        '<tr><td>Bookkeeping &amp; coding</td><td>Weekly / monthly</td></tr>'
        '<tr><td>Monthly IAS</td><td>Monthly</td></tr>'
        '<tr><td>Management reports</td><td>Monthly</td></tr>'
        '</tbody></table>'
        '<table class="jobtable"><caption>Periodic work</caption>'
        '<thead><tr><th>Job</th><th>Typical frequency</th></tr></thead><tbody>'
        '<tr><td>BAS preparation</td><td>Quarterly</td></tr>'
        '<tr><td>Super guarantee processing</td><td>Quarterly</td></tr>'
        '<tr><td>Year-end financial statements</td><td>Annually</td></tr>'
        '<tr><td>Company &amp; trust tax returns</td><td>Annually</td></tr>'
        '<tr><td>SMSF accounts &amp; workpapers</td><td>Annually</td></tr>'
        '<tr><td>Ad-hoc / overflow jobs</td><td>As needed</td></tr>'
        '</tbody></table></div>'
        '<p class="note" style="margin-top:16px">Frequencies are typical examples and are tailored to your practice. Your registered agents always retain lodgement and sign-off.</p>')
    s_cycle = section("cycle", "Jobs &amp; frequency", "What we do, and how often",
        "A clear picture of the recurring and periodic work we can take off your plate.", job, alt=True)

    sec = ('<ul class="feature-list feature-grid-2">'
        + feat("lock", "Least-privilege access", "Named individuals, access scoped to each job.")
        + feat("check", "Maker–checker review", "Independent second review on every job.")
        + feat("shield", "Confidentiality agreements", "Clear data-handling rules for client information.")
        + feat("cog", "ISO 27001 alignment (on roadmap)", "Aligning controls to ISO 27001; not yet certified.")
        + '</ul>')
    s_sec = security_section("security", "Security", "Careful with your clients' data",
        "The same controls apply to every engagement, from a single job to a dedicated team.",
        sec, "Scoped access, independent review and signed confidentiality on every job.")

    s_how = section("how", "How it works", "A simple, low-risk way to slot into your practice",
        "No big-bang changeover. We earn trust on a small scope first, then scale at your pace.",
        ('<div class="steps steps--compact">'
         + step("Scoping call", "We learn your software, file types, review standards and the work you'd like to hand over.")
         + step("Low-risk pilot", "We start small on a defined scope so you can judge quality, communication and turnaround.")
         + step("Prepare &amp; process", "Our named team does the work in your systems, to your templates and checklists.")
         + step("Maker–checker review", "A second reviewer independently checks the job, so what reaches you is verified and traceable.")
         + step("Handover for sign-off", "You review, sign off and lodge. Final professional judgement always stays with your practice.")
         + '</div>'))

    s_cta = '<section class="section alt" id="cta"><div class="shell">%s</div></section>' % cta_band(
        "See the quality for yourself",
        "Start with a defined pilot scope. If we're a fit, we scale at your pace — with no long lock-in.")

    s_test = testimonials_section(
        items=[TESTIMONIALS[0], TESTIMONIALS[1], TESTIMONIALS[5]],
        title="Practices that trust us with the work", alt=True)

    cyc_flow = ''
    s_flow = ''

    body = alt_sections(crumb + hero + s_scope + s_cycle + s_how + s_sec + dates_section(alt=True) + s_test + s_cta)
    service_ld = json.dumps({
        "@context": "https://schema.org", "@type": "Service",
        "serviceType": "Accounting and bookkeeping outsourcing (white-label)",
        "provider": {"@type": "ProfessionalService", "name": "INFITEX Global Advisory", "url": DOMAIN + "/"},
        "areaServed": "AU",
        "description": "White-label preparation and processing across the Australian compliance cycle. The client practice retains lodgement and sign-off."
    }, ensure_ascii=False)
    graph = '{"@context":"https://schema.org","@graph":[%s,%s,%s]}' % (
        ORG_LD, service_ld, breadcrumb([("Home", "index.html"), ("For Practices", "outsourcing.html")]))
    return page("outsourcing.html",
        "Accounting outsourcing for Australian practices | INFITEX",
        "White-label accounting & bookkeeping outsourcing across the Australian compliance cycle: BAS/IAS, payroll & STP, year-end, tax and SMSF. You keep sign-off.",
        body, graph, og_type="website")

# ================================================================ INDUSTRY (FOR BUSINESS)
INDUSTRIES = [
    ("Retail & e-commerce", "tag"),
    ("Professional services", "doc"),
    ("Construction & trades", "wrench"),
    ("Healthcare & allied health", "shield"),
    ("Hospitality & food", "headset"),
    ("Property & real estate", "pin"),
    ("Manufacturing", "factory"),
    ("Transport & logistics", "truck"),
    ("Not-for-profit", "users"),
    ("Startups & scale-ups", "rocket"),
]

def build_industry():
    crumb = '<div class="shell"><nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> / <span>For Business</span></nav></div>'
    hero = ('<section class="hero"><div class="shell hero-2col">'
        '<div class="hero-copy">'
        '<span class="eyebrow">Who we help · Business &amp; industry</span>'
        '<h1>Your outsourced <span class="accent">finance team</span> — from bookkeeping to Virtual CFO</h1>'
        '<p class="answer-lede">For Australian businesses, INFITEX runs a dedicated outsourced finance function — bookkeeping, payroll and STP, accounts payable and receivable, management reporting, budgeting, cash-flow forecasting and Virtual CFO — on your software, with named people, while lodgement stays with you or your registered BAS or tax agent.</p>'
        '<p class="hero-sub" data-tw>A dedicated finance function for Australian businesses, without the overhead of building one in-house. We run the day-to-day books, the monthly reporting and the strategic numbers — and coordinate lodgement through a registered BAS or tax agent.</p>'
        '<p class="hero-sub">INFITEX is the finance team behind Australian businesses — from bookkeeping and payroll through to management reporting and Virtual CFO. Native to Xero, XPM, MYOB and the tools you already use.</p>'
        '<div class="hero-cta"><a class="btn btn-primary" href="contact.html">Request a pilot</a>'
        '<a class="btn btn-ghost" data-booking href="contact.html">Book a 15-min call</a></div>'
        '<div class="hero-paths" style="margin-top:18px"><span class="path-chip" style="border-color:var(--accent);color:var(--accent)"><b>For business</b></span>'
        '<a class="path-chip" href="outsourcing.html">Run an accounting practice? <b>For practices →</b></a></div>'
        '</div>'
        + finance_dashboard() +
        '</div></section>')

    # who this is for / industries
    ind_cards = "".join(
        '<div class="ind-card"><span class="ind-ic">%s</span><span>%s</span></div>' % (ico(icon), name)
        for name, icon in INDUSTRIES)
    s_ind = section("industries", "Who we help", "Finance support across Australian industries",
        "Whatever you do, the numbers still have to be right. We support growing businesses across a range of sectors — if you don't see yours, ask.",
        '<div class="ind-grid">%s</div>' % ind_cards, alt=True)

    # what we do (business)
    what = ('<div class="grid grid-3">'
        + card("doc", "Bookkeeping &amp; reconciliations", "Day-to-day books kept accurate, coded and reconciled in your software.")
        + card("doc", "Accounts payable &amp; receivable", "Bills paid, invoices raised, debtors followed up — your cash kept moving.")
        + card("users", "Payroll &amp; STP", "Pay runs processed and Single Touch Payroll prepared, ready for lodgement.")
        + card("pie", "Management accounts &amp; reporting", "Monthly management accounts and clear, decision-ready reporting.")
        + card("trend", "Budgeting &amp; forecasting", "Budgets, rolling forecasts and scenario planning to guide decisions.")
        + card("cash", "Cash-flow management", "13-week cash-flow forecasts and working-capital visibility.")
        + card("doc", "BAS &amp; compliance prep", "Activity statements and year-end prepared; lodged via a registered agent.")
        + card("shield", "Systems &amp; controls", "Clean processes, approvals and controls so your numbers stay trustworthy.")
        + card("bolt", "Catch-up &amp; clean-up", "Behind on the books? We get you current and keep you there.")
        + '</div>')
    s_what = section("what", "What we do", "A complete finance function, modular by design",
        "Take the whole finance stack or just the parts you need — and add Virtual CFO when you want strategy on top.",
        what)

    # Virtual CFO spotlight
    vcfo = ('<div class="viz-grid">'
        '<div class="prose" style="max-width:none">'
        '<p data-tw>A Virtual CFO gives you senior financial leadership on a fractional basis — the insight of a CFO without a full-time executive salary. We turn your numbers into decisions.</p>'
        '<ul class="feature-list" style="margin-top:18px">'
        + feat("pie", "Management &amp; board reporting", "Monthly packs that tell the story behind the numbers.")
        + feat("cash", "Cash-flow forecasting", "Rolling 13-week and longer-range cash-flow visibility.")
        + feat("target", "Budgeting &amp; KPIs", "Budgets, targets and KPI dashboards your team can act on.")
        + feat("trend", "Profitability &amp; pricing", "Margin, product and customer profitability analysis.")
        + feat("users", "Lender &amp; investor support", "Numbers and packs ready for banks, lenders and investors.")
        + feat("cog", "Systems &amp; process", "The right finance stack and controls as you scale.")
        + '</ul></div>'
        '<div class="viz-card"><span class="viz-cap">illustrative · bookkeeping → strategy</span>'
        '<div class="flow" style="margin-top:8px">'
        '<svg class="flow-line" viewBox="0 0 1000 8" preserveAspectRatio="none" aria-hidden="true">'
        '<line class="track" x1="0" y1="4" x2="1000" y2="4"/><line class="flow-beam" x1="0" y1="4" x2="1000" y2="4"/></svg>'
        '<div class="flow-row" style="grid-template-columns:repeat(3,1fr)">'
        '<div class="flow-stage"><span class="flow-node">1</span><b>Record</b><p>Accurate books &amp; payroll.</p></div>'
        '<div class="flow-stage"><span class="flow-node">2</span><b>Report</b><p>Management accounts &amp; KPIs.</p></div>'
        '<div class="flow-stage"><span class="flow-node">3</span><b>Advise</b><p>Forecasts &amp; CFO strategy.</p></div>'
        '</div></div>'
        '<p class="note" style="margin-top:14px">Engage Virtual CFO on its own or layered on top of your bookkeeping — fractional and flexible.</p>'
        '</div></div>')
    s_vcfo = section("vcfo", "Virtual CFO", "Senior finance leadership, fractionally",
        "Strategy, forecasting and reporting from an experienced finance team — scaled to your size and stage.",
        vcfo, alt=True)

    # how it works
    steps = ('<div class="steps">'
        + step("Discovery call", "We learn your business, systems, numbers and what you want to hand over.")
        + step("Dedicated team &amp; pilot", "You get named people and a single point of contact, starting on a defined scope.")
        + step("Run the finance function", "Books, payroll and reporting handled in your systems, to an agreed rhythm.")
        + step("Review &amp; advise", "Monthly reporting and, where engaged, Virtual CFO insight to guide decisions.")
        + step("Lodge via a registered agent", "BAS and tax are lodged by a registered agent — yours, or a partner we coordinate with.")
        + '</div>')
    s_how = section("how", "How it works", "A dedicated team, a single point of contact",
        "You work with named people who know your business — not an anonymous queue.", steps)

    # engagement
    eng = ('<div class="grid grid-3">'
        + card("users", "Dedicated staff", "A named bookkeeper or accountant (or team) working only on your business.")
        + card("trend", "Fractional Virtual CFO", "Senior finance leadership a few days a month — scaled to your needs.")
        + card("bolt", "Project &amp; catch-up", "One-off clean-ups, system migrations or reporting builds, done and handed over.")
        + '</div>'
        '<p class="note" style="margin-top:18px">We don\'t publish prices — the right model depends on your size, volume and software. Contact us for the best pricing for your business.</p>')
    s_eng = section("engagement", "Engagement models", "Flexible ways to work together",
        "Start with what you need today and scale up or down as your business changes.", eng, alt=True)

    sec_feats = ('<ul class="feature-list feature-grid-2">'
        + feat("lock", "Least-privilege access", "Named individuals, access scoped to each task in your systems.")
        + feat("check", "Maker–checker review", "Independent second review before reporting reaches you.")
        + feat("shield", "Confidentiality agreements", "Clear data-handling rules for your financial information.")
        + feat("cog", "ISO 27001 alignment (on roadmap)", "Aligning controls to ISO 27001; not yet certified.")
        + '</ul>')
    s_sec = security_section("security", "Security", "Your financial data, handled carefully",
        "The same controls apply whether you take a single role or a full finance team.",
        sec_feats, "Role-based access, independent review and confidentiality by design.")

    # Why INFITEX — finance team that feels in-house (from reference, AU-aligned)
    why = ('<div class="grid grid-2">'
        + card("trend", "Cut the cost of in-house", "Senior and routine finance capability for a fraction of local salaries.")
        + card("stack", "Scales with you", "Add or dial back hours as your business changes — no permanent overhead.")
        + card("users", "Named, accountable people", "You know who works on your file. No anonymous call centre.")
        + card("shield", "Secure &amp; AU-aligned", "Role-based access and confidentiality; ISO 27001 alignment on our roadmap (not yet certified).")
        + '</div>'
        '<p class="compliance-line" style="margin-top:18px">INFITEX prepares and processes your finance work and provides management-level support. We are not a registered Australian tax or BAS agent and do not provide audit or AFSL-regulated financial product advice; lodgement and statutory sign-off remain with you or your registered agent.</p>')
    s_why = section("why", "Why INFITEX", "A finance team that feels in-house",
        "All the capability of an in-house team, without the cost, the recruitment or the overhead.", why, alt=True)

    s_cta = '<section class="section alt" id="cta"><div class="shell">%s</div></section>' % cta_band(
        "Get a finance team without the overhead",
        "Start with a defined pilot. Add Virtual CFO when you're ready for strategy on top. No long lock-in.")

    s_test = testimonials_section(
        items=[TESTIMONIALS[3], TESTIMONIALS[2], TESTIMONIALS[4]],
        title="Businesses that run on our numbers")

    body = alt_sections(crumb + hero + s_ind + s_what + s_vcfo + s_how + s_eng + s_sec + s_why + dates_section(alt=True) + s_test + s_cta)
    service_ld = json.dumps({
        "@context": "https://schema.org", "@type": "Service",
        "serviceType": "Outsourced accounting, finance and Virtual CFO services",
        "provider": {"@type": "ProfessionalService", "name": "INFITEX Global Advisory", "url": DOMAIN + "/"},
        "areaServed": "AU",
        "description": "Outsourced finance team for Australian businesses: bookkeeping, payroll & STP, management accounts, budgeting & forecasting, cash-flow and Virtual CFO. Lodgement is handled via a registered BAS/tax agent."
    }, ensure_ascii=False)
    graph = '{"@context":"https://schema.org","@graph":[%s,%s,%s]}' % (
        ORG_LD, service_ld, breadcrumb([("Home", "index.html"), ("For Business", "industry.html")]))
    return page("industry.html",
        "Outsourced finance team & Virtual CFO, Australia | INFITEX",
        "A dedicated outsourced finance team for Australian businesses: bookkeeping, payroll & STP, management accounts, forecasting and Virtual CFO.",
        body, graph, og_type="website")


# ================================================================ DIGITECH
def build_digitech():
    crumb = '<div class="shell"><nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> / <span>Digitech</span></nav></div>'
    hero = ('<section class="hero"><div class="shell">'
        '<span class="eyebrow">Secondary division · Digitech</span>'
        '<h1>Look as sharp <span class="accent">online</span> as your work</h1>'
        '<p class="answer-lede">Digitech is the INFITEX web division for Australian accounting and bookkeeping practices, delivering fast, accessible websites plus domains, hosting, business email, SEO and Google Business Profile setup — one partner for everything client-facing online.</p>'
        '<p class="hero-sub" data-tw>Practical digital services for accounting and bookkeeping practices — websites, domains, hosting, business email, SEO and Google Business Profile. One partner, fewer vendors to juggle.</p>'
        '<div class="hero-cta"><a class="btn btn-primary" href="contact.html">Get in touch</a>'
        '<a class="btn btn-ghost" data-booking href="contact.html">Book a call</a></div>'
        '</div></section>')

    serv = ('<div class="grid grid-3">'
        + card("globe", "Web design &amp; build", "Fast, accessible, mobile-first websites that turn visitors into enquiries — built and maintained for you.")
        + card("mail", "Domains, hosting &amp; email", "Domain registration, reliable hosting and professional business email, set up and managed.")
        + card("search", "SEO", "On-page SEO and local search so the right clients find your practice.")
        + card("globe", "Google Business Profile", "Set up and optimised so you show up in local map results.")
        + card("doc", "Content &amp; landing pages", "Clear, compliant copy and pages designed around your services.")
        + card("cog", "Care &amp; maintenance", "Updates, backups and small changes handled, so your site stays current and secure.")
        + '</div>')
    s_serv = section("services", "Services", "Everything client-facing, online",
        "From a first website to ongoing SEO, we cover the digital side so you can focus on clients.", serv)

    # animated workflow with a light beam flowing stage 1 -> last (5 stages)
    flow = ('<div class="viz-card"><span class="viz-cap">workflow · brief → live → looked after</span>'
        '<div class="flow flow-5">'
        '<svg class="flow-line" viewBox="0 0 1000 8" preserveAspectRatio="none" aria-hidden="true">'
        '<line class="track" x1="0" y1="4" x2="1000" y2="4"/>'
        '<line class="flow-beam" x1="0" y1="4" x2="1000" y2="4"/></svg>'
        '<div class="flow-row flow-row-5">'
        '<div class="flow-stage"><span class="flow-node">1</span><b>Discover</b><p>We agree goals, pages, domain and how clients should find you.</p></div>'
        '<div class="flow-stage"><span class="flow-node">2</span><b>Design</b><p>A clean, on-brand, mobile-first layout for your review.</p></div>'
        '<div class="flow-stage"><span class="flow-node">3</span><b>Build</b><p>Built fast and accessible, with hosting, email and DNS set up.</p></div>'
        '<div class="flow-stage"><span class="flow-node">4</span><b>Launch</b><p>On-page SEO, Google Business Profile, analytics and a clean go-live.</p></div>'
        '<div class="flow-stage"><span class="flow-node">5</span><b>Care</b><p>Updates, backups and support so it stays secure and current.</p></div>'
        '</div></div></div>')
    s_proc = section("process", "How we work", "From brief to live, without the fuss",
        "A clear path with no jargon. Watch it flow from the first conversation through to ongoing care.", flow, alt=True)

    # illustrative growth chart + channel equaliser bars
    bars = "".join('<div class="bar" style="--h:%s"></div>' % h for h in ["16%","27%","41%","58%","78%","92%"])
    chart = ('<div class="viz-grid">'
        '<div class="viz-card">'
        '<span class="viz-cap">illustrative · online visibility over time</span>'
        '<div class="chart">' + bars +
        '<svg class="chart-trend" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">'
        '<polyline points="8,84 25,73 42,59 59,42 76,22 92,8"/></svg>'
        '</div>'
        '<div class="chart-legend"><span>Mo 1</span><span>Mo 3</span><span>Mo 6</span><span>Mo 9</span><span>Mo 12</span><span>Mo 15</span></div>'
        '<p class="note" style="margin-top:12px">Illustrative shape only — not a forecast. Real results depend on your market, competition and effort.</p>'
        '</div>'
        '<div class="viz-card"><span class="viz-cap">channels we cover</span>'
        '<div class="eq">'
        '<div class="eq-item"><div class="eq-bars"><span></span><span></span><span></span><span></span></div><b>Website</b><span class="lbl">build</span></div>'
        '<div class="eq-item"><div class="eq-bars"><span></span><span></span><span></span><span></span></div><b>SEO</b><span class="lbl">search</span></div>'
        '<div class="eq-item"><div class="eq-bars"><span></span><span></span><span></span><span></span></div><b>Email</b><span class="lbl">business</span></div>'
        '<div class="eq-item"><div class="eq-bars"><span></span><span></span><span></span><span></span></div><b>Profile</b><span class="lbl">local</span></div>'
        '</div></div>'
        '</div>')
    s_viz = section("growth", "Built to grow", "A digital presence that compounds",
        "Each channel reinforces the others — a clean site, found in search, backed by email and a strong local profile.",
        chart)

    # what's included (tick grid) — reassurance for non-technical buyers
    incl = ['Mobile-first, responsive layout','Accessibility-minded build (WCAG)',
            'Fast Core Web Vitals','SEO-ready metadata &amp; schema',
            'SSL / HTTPS secured','Forms with spam protection',
            'Analytics-ready (GA4)','You own your domain &amp; content',
            'Plain-English handover &amp; training']
    incl_html = '<ul class="incl-grid">' + "".join(
        '<li>%s<span>%s</span></li>' % (ico("check"), t) for t in incl) + '</ul>'
    s_incl = section("included", "What's included", "Every build comes with the essentials",
        "No surprises — these come as standard on every website we build, on every device.", incl_html)

    # website care plans — 3 tiers, no published rates
    def plan(tier, head, blurb, feats, featured=False, pill=None):
        cls = "plan-card featured" if featured else "plan-card"
        tierhtml = '<div class="tier"><span>%s</span>%s</div>' % (
            tier, ('<span class="pill">%s</span>' % pill) if pill else '')
        fl = "".join('<li>%s</li>' % f for f in feats)
        return ('<article class="%s">%s<h3>%s</h3><p class="blurb">%s</p>'
                '<ul class="plan-feats">%s</ul>'
                '<p class="plan-price">Contact us for the best pricing for your practice.</p>'
                '</article>') % (cls, tierhtml, head, blurb, fl)
    plans = ('<div class="plan-grid">'
        + plan("Essential", "Keep it safe &amp; online",
               "For simple sites that need a solid, secure foundation.",
               ["Managed hosting","SSL &amp; uptime monitoring","Software updates","Monthly backups","Email support"])
        + plan("Growth", "Care + improvements",
               "For active sites that need regular changes and attention.",
               ["Everything in Essential","Priority updates &amp; testing","Security monitoring","Monthly support time for edits","Monthly performance report"],
               featured=True, pill="Popular")
        + plan("Complete", "Full-service partner",
               "For business-critical sites needing hands-on care.",
               ["Everything in Growth","Daily backups","Performance optimisation","SEO check-ins","First-priority support"])
        + '</div>')
    s_care = section("care", "Website care plans", "Keep your site secure, fast and current",
        "A website isn't a one-off — it needs updates, backups and the occasional change. Pick the level of care that fits and we'll tailor the rest. We don't publish rates.",
        plans, alt=True)

    # why Digitech — trust cards (kept; add-ons & platforms intentionally omitted for focus)
    why = ('<div class="grid grid-2">'
        + card("users", "One team, end to end", "The same group that supports your practice can build and run your website — one point of contact.")
        + card("doc", "Plain-English, always", "No jargon. We explain what we're doing and why, and hand over something you can actually manage.")
        + card("clock", "Time-zone advantage", "Work done during our day is ready for your AEST/AEDT morning — quick turnarounds on changes.")
        + card("shield", "You own everything", "Your domain, content and accounts stay in your name. No lock-in, no hostage situations.")
        + '</div>')
    s_why = section("why", "Why Digitech", "A web partner that already knows you",
        "Because we already support the numbers behind your practice, the web work fits the way you already operate.", why)

    # --- "Found on Google" split with search-ranking visual (from reference, retoned) ---
    found_svg = ('<svg class="dt-svg" viewBox="0 0 460 300" role="img" '
        'aria-label="Ranking as the top result in search, with rising visibility" xmlns="http://www.w3.org/2000/svg">'
        '<rect x="28" y="22" width="404" height="40" rx="20" fill="var(--bg-2)" stroke="var(--line)"/>'
        '<circle cx="54" cy="42" r="8" fill="none" stroke="var(--muted)" stroke-width="2"/>'
        '<line x1="60" y1="48" x2="68" y2="56" stroke="var(--muted)" stroke-width="2" stroke-linecap="round"/>'
        '<rect x="84" y="36" width="150" height="12" rx="6" fill="var(--muted)" opacity=".45"/>'
        '<rect x="28" y="80" width="404" height="96" rx="12" fill="var(--bg-2)" stroke="var(--primary)" stroke-width="2"/>'
        '<rect x="48" y="98" width="64" height="18" rx="9" fill="var(--accent-fill)"/>'
        '<text x="58" y="111" font-family="ui-sans-serif,system-ui,sans-serif" font-size="11" font-weight="700" fill="var(--accent-ink)">#1 spot</text>'
        '<rect x="48" y="128" width="236" height="13" rx="6" fill="var(--primary)"/>'
        '<rect x="48" y="150" width="330" height="8" rx="4" fill="var(--muted)" opacity=".45"/>'
        '<rect x="48" y="162" width="286" height="8" rx="4" fill="var(--muted)" opacity=".45"/>'
        '<rect x="28" y="190" width="270" height="12" rx="6" fill="var(--bg-3)"/>'
        '<rect x="28" y="210" width="240" height="12" rx="6" fill="var(--bg-3)"/>'
        '<rect x="28" y="230" width="255" height="12" rx="6" fill="var(--bg-3)"/>'
        '<rect x="320" y="224" width="16" height="26" rx="3" fill="var(--line-2)"/>'
        '<rect x="346" y="210" width="16" height="40" rx="3" fill="var(--line-2)"/>'
        '<rect x="372" y="196" width="16" height="54" rx="3" fill="var(--line-2)"/>'
        '<rect x="398" y="178" width="16" height="72" rx="3" fill="var(--line-2)"/>'
        '<rect x="424" y="158" width="16" height="92" rx="3" fill="var(--primary)"/>'
        '<path d="M322 232 L420 150" fill="none" stroke="var(--accent-fill)" stroke-width="2.5" stroke-linecap="round"/>'
        '<path d="M404 150 l16 0 0 16" fill="none" stroke="var(--accent-fill)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>')
    found_inner = ('<div class="dt-split">'
        '<div><p class="eyebrow">Found on Google</p><h2 class="section-title">Built to be found</h2>'
        '<p class="lead">Every site is structured for search from day one — clean metadata, structured data and a properly configured Google Business Profile — so nearby clients land on you first.</p>'
        '<ul class="ticks"><li>On-page SEO &amp; structured data</li><li>Google Business Profile setup</li><li>Search Console &amp; sitemap submission</li></ul></div>'
        '<div class="dt-visual">%s</div></div>') % found_svg
    s_found = '<section class="section alt" id="found"><div class="shell">%s</div></section>' % found_inner

    # --- responsive "looks right on every device" split ---
    device_svg = ('<svg class="dt-svg" viewBox="0 0 460 320" role="img" '
        'aria-label="The same website shown on desktop and mobile" xmlns="http://www.w3.org/2000/svg">'
        '<rect x="30" y="28" width="300" height="200" rx="12" fill="var(--bg-2)" stroke="var(--line)"/>'
        '<path d="M30 40a12 12 0 0 1 12-12h276a12 12 0 0 1 12 12v16H30z" fill="var(--bg-3)"/>'
        '<circle cx="48" cy="43" r="3.5" fill="var(--primary)"/><circle cx="60" cy="43" r="3.5" fill="var(--muted)" opacity=".5"/>'
        '<rect x="50" y="70" width="260" height="42" rx="8" fill="var(--primary)"/>'
        '<rect x="64" y="82" width="110" height="9" rx="4" fill="var(--primary-ink)"/>'
        '<rect x="64" y="96" width="74" height="7" rx="3" fill="var(--primary-ink)" opacity=".6"/>'
        '<rect x="50" y="124" width="124" height="84" rx="8" fill="var(--bg-3)" stroke="var(--line)"/>'
        '<rect x="186" y="124" width="124" height="84" rx="8" fill="var(--bg-3)" stroke="var(--line)"/>'
        '<rect x="300" y="150" width="120" height="150" rx="16" fill="var(--bg-2)" stroke="var(--line)"/>'
        '<rect x="312" y="168" width="96" height="40" rx="7" fill="var(--primary)"/>'
        '<rect x="312" y="216" width="96" height="20" rx="5" fill="var(--bg-3)" stroke="var(--line)"/>'
        '<rect x="312" y="242" width="96" height="20" rx="5" fill="var(--bg-3)" stroke="var(--line)"/>'
        '<circle cx="360" cy="286" r="6" fill="var(--line-2)"/></svg>')
    incl2_inner = ('<div class="dt-split dt-split-rev">'
        '<div class="dt-visual">%s</div>'
        '<div><p class="eyebrow">Every device</p><h2 class="section-title">Looks right on every screen</h2>'
        '<p class="lead">Mobile-first by default. Whether a client finds you on a phone on the train or a desktop at the office, your site stays fast, clear and easy to use.</p>'
        '<ul class="ticks"><li>Responsive, mobile-first layouts</li><li>Fast Core Web Vitals</li><li>Accessible to WCAG guidelines</li></ul></div></div>') % device_svg
    s_device = '<section class="section" id="devices"><div class="shell">%s</div></section>' % incl2_inner

    s_cta = '<section class="section" id="cta"><div class="shell">%s</div></section>' % cta_band(
        "Ready to refresh your online presence?",
        "Tell us where you are today and where you'd like to be. We'll suggest a practical next step.",
        primary=("Get in touch", "contact.html"))

    body = alt_sections(crumb + hero + s_serv + s_incl + s_device + s_found + s_proc + s_care + s_why + s_viz + s_cta)
    service_ld = json.dumps({
        "@context": "https://schema.org", "@type": "Service",
        "serviceType": "Digital services for accounting practices (web, email, SEO)",
        "provider": {"@type": "ProfessionalService", "name": "INFITEX Global Advisory", "url": DOMAIN + "/"},
        "areaServed": "AU",
        "description": "Websites, domains, hosting, business email, SEO and Google Business Profile for Australian accounting and bookkeeping practices.",
        "hasOfferCatalog": {
            "@type": "OfferCatalog", "name": "Digitech web services",
            "itemListElement": [
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Web design & build"}},
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Domains, hosting & business email"}},
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "SEO & Google Business Profile"}},
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Website care & maintenance"}}
            ]
        }
    }, ensure_ascii=False)
    graph = '{"@context":"https://schema.org","@graph":[%s,%s,%s]}' % (
        ORG_LD, service_ld, breadcrumb([("Home", "index.html"), ("Digitech", "digitech.html")]))
    return page("digitech.html",
        "Digitech — websites, email & SEO for accountants | INFITEX",
        "Digitech by INFITEX: websites, domains, hosting, business email, SEO and Google Business Profile, built for Australian accounting and bookkeeping practices.",
        body, graph, og_type="website")

# ================================================================ PRIVACY
def build_privacy():
    crumb = '<div class="shell"><nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> / <span>Privacy</span></nav></div>'
    body = crumb + ('<section class="section"><div class="shell legal-shell">'
        '<span class="eyebrow">Legal</span><h1>Privacy Policy</h1>'
        '<p class="lead">This Privacy Policy explains how INFITEX Global Advisory ("INFITEX", "we", "us", "our") collects, uses, discloses, stores and protects personal information. It is written to align with the <em>Privacy Act 1988</em> (Cth), the Australian Privacy Principles (APPs) and the Notifiable Data Breaches (NDB) scheme. Last updated: <span data-year>2026</span>.</p>'
        '<div class="legal-toc"><strong>On this page</strong><ol>'
        '<li><a href="#p-scope">Scope of this policy</a></li>'
        '<li><a href="#p-collect">Personal information we collect</a></li>'
        '<li><a href="#p-how">How we collect it</a></li>'
        '<li><a href="#p-why">Why we collect, hold and use it</a></li>'
        '<li><a href="#p-controller">When we act for a practice</a></li>'
        '<li><a href="#p-marketing">Direct marketing &amp; the Spam Act</a></li>'
        '<li><a href="#p-disclose">Disclosure to third parties</a></li>'
        '<li><a href="#p-overseas">Overseas disclosure</a></li>'
        '<li><a href="#p-security">Security &amp; retention</a></li>'
        '<li><a href="#p-breach">Data breaches</a></li>'
        '<li><a href="#p-cookies">Cookies &amp; analytics</a></li>'
        '<li><a href="#p-rights">Access, correction &amp; your rights</a></li>'
        '<li><a href="#p-complaints">Complaints</a></li>'
        '<li><a href="#p-children">Children</a></li>'
        '<li><a href="#p-changes">Changes to this policy</a></li>'
        '<li><a href="#p-contact">How to contact us</a></li>'
        '</ol></div>'
        '<div class="prose">'
        '<h2 id="p-scope">1. Scope of this policy</h2>'
        '<p>This policy applies to personal information we handle through this website and in the course of providing white-label accounting outsourcing and Digitech services. "Personal information" has the meaning given in the Privacy Act: information or an opinion about an identified individual, or an individual who is reasonably identifiable, whether true or not and whether recorded in a material form or not.</p>'
        '<h2 id="p-collect">2. Personal information we collect</h2>'
        '<p>We aim to collect only what we need. Depending on how you interact with us, this may include:</p>'
        '<ul>'
        '<li><strong>Contact and enquiry details</strong> — your name, business or practice name, work email, phone number, country dialling code and the content of your message.</li>'
        '<li><strong>Subscription details</strong> — your email address if you opt in to our compliance-dates digest.</li>'
        '<li><strong>Engagement information</strong> — where your practice engages us, the information needed to perform the agreed work, which may include client financial records supplied to us by the practice.</li>'
        '<li><strong>Technical information</strong> — limited information such as approximate location, device and browser type, and pages viewed, where analytics are enabled.</li>'
        '</ul>'
        '<p>We do not seek sensitive information (such as health, racial or political information) to respond to a website enquiry, and ask that you do not send it to us unless it is necessary for an agreed engagement.</p>'
        '<h2 id="p-how">3. How we collect it</h2>'
        '<p>We collect personal information directly from you when you complete a form, email, call or message us, or subscribe to our digest. Where your practice engages us, we receive information from the practice under that engagement. Where it is lawful and practicable, we will collect information directly from you rather than from a third party.</p>'
        '<h2 id="p-why">4. Why we collect, hold and use it</h2>'
        '<ul>'
        '<li>To respond to your enquiry and provide the information or services you request.</li>'
        '<li>To perform the services agreed with your practice, and to communicate with you about them.</li>'
        '<li>To send the compliance-dates digest where you have opted in (you can unsubscribe at any time).</li>'
        '<li>To improve and secure our website and services.</li>'
        '<li>To meet our legal, regulatory and record-keeping obligations.</li>'
        '</ul>'
        '<p>If we cannot collect the information we reasonably need, we may be unable to respond to your enquiry or provide a service.</p>'
        '<h2 id="p-controller">5. When we act on behalf of a practice</h2>'
        '<p>When we prepare and process work for an accounting or bookkeeping practice, we handle the relevant information on that practice\'s instructions and for the purposes of the engagement. The practice remains responsible for its own privacy obligations to its clients. We are not a registered Australian tax or BAS agent; lodgement and sign-off remain with the practice and its registered agents.</p>'
        '<h2 id="p-marketing">6. Direct marketing &amp; the Spam Act</h2>'
        '<p>We only send marketing or digest emails where you have opted in. Every such email contains a functional unsubscribe facility and identifies INFITEX as the sender, consistent with the <em>Spam Act 2003</em> (Cth). We do not sell or rent your contact details for third-party marketing.</p>'
        '<h2 id="p-disclose">7. Disclosure to third parties</h2>'
        '<p>We do not sell your personal information. We may disclose it to:</p>'
        '<ul>'
        '<li>service providers who help us operate (for example, form handling, email delivery, scheduling, hosting and analytics providers), bound to use it only for those purposes;</li>'
        '<li>the relevant practice, where the information relates to an engagement we perform for them;</li>'
        '<li>professional advisers, or where we are required or authorised by law, a court or a regulator.</li>'
        '</ul>'
        '<h2 id="p-overseas">8. Overseas disclosure</h2>'
        '<p>INFITEX operates from India, so personal information may be accessed, processed or stored in India. Some of our service providers may also store data in other countries (for example, the United States or the European Union) depending on where their infrastructure is located. Before disclosing personal information overseas we take steps that are reasonable in the circumstances to ensure recipients handle it consistently with the APPs.</p>'
        '<h2 id="p-security">9. Security &amp; retention</h2>'
        '<p>We use technical and organisational measures including role-based, least-privilege access, confidentiality agreements, maker–checker review and secure transmission. We are aligning our information-security controls to ISO 27001; this is a roadmap commitment, not a current certification. We keep personal information only for as long as we need it for the purposes described or as required by law, and then take reasonable steps to destroy or de-identify it.</p>'
        '<h2 id="p-breach">10. Data breaches</h2>'
        '<p>We maintain a data-breach response process. Where a breach is likely to result in serious harm to affected individuals, we will notify those individuals and the Office of the Australian Information Commissioner (OAIC) as required under the Notifiable Data Breaches scheme.</p>'
        '<h2 id="p-cookies">11. Cookies &amp; analytics</h2>'
        '<p>This site uses minimal cookies and local storage to remember preferences such as your theme choice. Where analytics are enabled, they are used to understand aggregate usage and improve the site, not to identify you personally. You can control or clear cookies through your browser settings; some features may not work without them.</p>'
        '<h2 id="p-rights">12. Access, correction &amp; your rights</h2>'
        '<p>You may request access to, or correction of, the personal information we hold about you. We will respond within a reasonable time and may need to verify your identity first. If we decline a request, we will explain why and how you can seek a review. From June 2025, individuals also have a statutory right to sue for serious invasions of privacy under Australian law.</p>'
        '<h2 id="p-complaints">13. Complaints</h2>'
        '<p>If you believe we have mishandled your personal information, please contact us first using the details below so we can investigate and respond. If you are not satisfied with our response, you may complain to the OAIC at <a href="https://www.oaic.gov.au" rel="noopener" target="_blank">oaic.gov.au</a>.</p>'
        '<h2 id="p-children">14. Children</h2>'
        '<p>Our website and services are directed at businesses and practices, not children. We do not knowingly collect personal information from children.</p>'
        '<h2 id="p-changes">15. Changes to this policy</h2>'
        '<p>We may update this policy from time to time. The current version is always available on this page, with the "last updated" date shown above. Material changes will be reflected here.</p>'
        '<h2 id="p-contact">16. How to contact us</h2>'
        '<p>Privacy questions or requests: <a href="mailto:info@infitexglobal.com">info@infitexglobal.com</a> or <a href="tel:+918500850526">+91 8500 850 526</a>.</p>'
        '<p class="note">This page is general information, not legal advice. Please obtain advice tailored to your circumstances.</p>'
        '</div></div></section>')
    legal_ld = ('{"@context":"https://schema.org","@type":"WebPage","name":"Privacy Policy",'
        '"datePublished":"2026-06-01","dateModified":"2026-06-27","inLanguage":"en-AU",'
        '"publisher":{"@id":"%s/#organization"}}') % DOMAIN
    graph = '{"@context":"https://schema.org","@graph":[%s,%s,%s]}' % (
        ORG_LD, legal_ld, breadcrumb([("Home", "index.html"), ("Privacy", "privacy.html")]))
    return page("privacy.html", "Privacy Policy — INFITEX Global Advisory",
        "How INFITEX Global Advisory handles personal information, aligned to the Australian Privacy Act 1988 and the Australian Privacy Principles (APPs).",
        body, graph)

# ================================================================ TERMS
def build_terms():
    crumb = '<div class="shell"><nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> / <span>Terms</span></nav></div>'
    body = crumb + ('<section class="section"><div class="shell legal-shell">'
        '<span class="eyebrow">Legal</span><h1>Terms of Use</h1>'
        '<p class="lead">These Terms of Use ("Terms") govern your access to and use of the INFITEX Global Advisory website and the information on it. By using this website you agree to these Terms. Last updated: <span data-year>2026</span>.</p>'
        '<div class="legal-toc"><strong>On this page</strong><ol>'
        '<li><a href="#t-about">About this website</a></li>'
        '<li><a href="#t-noadvice">No professional advice</a></li>'
        '<li><a href="#t-line">The compliance line</a></li>'
        '<li><a href="#t-pricing">No pricing &amp; indicative figures</a></li>'
        '<li><a href="#t-enquiries">Enquiries are not a contract</a></li>'
        '<li><a href="#t-accept">Acceptable use</a></li>'
        '<li><a href="#t-ip">Intellectual property</a></li>'
        '<li><a href="#t-third">Third-party links &amp; tools</a></li>'
        '<li><a href="#t-avail">Availability &amp; changes</a></li>'
        '<li><a href="#t-disc">Disclaimers</a></li>'
        '<li><a href="#t-liab">Limitation of liability</a></li>'
        '<li><a href="#t-acl">Australian Consumer Law</a></li>'
        '<li><a href="#t-law">Governing law</a></li>'
        '<li><a href="#t-contact">Contact</a></li>'
        '</ol></div>'
        '<div class="prose">'
        '<h2 id="t-about">1. About this website</h2>'
        '<p>This website provides general information about INFITEX Global Advisory and our white-label accounting outsourcing and Digitech services. It is provided "as is" for information purposes.</p>'
        '<h2 id="t-noadvice">2. No professional advice</h2>'
        '<p>Nothing on this website constitutes accounting, tax, financial, legal or other professional advice, and it must not be relied upon as such. You should obtain advice appropriate to your circumstances before acting.</p>'
        '<h2 id="t-line">3. The compliance line</h2>'
        '<p>INFITEX is <strong>not</strong> a registered Australian tax or BAS agent and does not provide audit or AFSL-regulated financial product advice. We provide preparation and processing support to accounting and bookkeeping practices. Lodgement, statutory sign-off and final professional judgement always remain with the client practice and its registered agents. We do not contact your clients unless expressly authorised within an engagement.</p>'
        '<h2 id="t-pricing">4. No pricing &amp; indicative figures</h2>'
        '<p>We do not publish prices on this website. Any figures shown — including the savings calculator — are illustrative estimates only, are not a quote, offer or guarantee, and should not be relied upon as a projection of actual savings. Contact us for pricing tailored to your practice.</p>'
        '<h2 id="t-enquiries">5. Enquiries are not a contract</h2>'
        '<p>Submitting an enquiry, subscribing to the digest or booking a call does not create a contract or engagement. An engagement begins only when separately agreed in writing between INFITEX and your practice or business.</p>'
        '<h2 id="t-accept">6. Acceptable use</h2>'
        '<p>You agree not to misuse this website, including by attempting to gain unauthorised access, introducing malicious code, scraping at scale, interfering with its operation, or using it for unlawful purposes or to send spam.</p>'
        '<h2 id="t-ip">7. Intellectual property</h2>'
        '<p>The content, branding, layout, graphics and code of this website are owned by INFITEX or used under licence, and are protected by intellectual-property laws. You may view and print pages for your own reference, but you may not reproduce, republish or commercially exploit them without our written consent.</p>'
        '<h2 id="t-third">8. Third-party links &amp; tools</h2>'
        '<p>This website may link to or integrate third-party services (for example WhatsApp, scheduling and form tools). We do not control those services and are not responsible for their content or practices; their own terms and privacy policies apply to your use of them.</p>'
        '<h2 id="t-avail">9. Availability &amp; changes</h2>'
        '<p>We aim to keep the website available but do not guarantee uninterrupted access. We may change, suspend or withdraw any part of the website, and may update these Terms, at any time. The current version is always available on this page.</p>'
        '<h2 id="t-disc">10. Disclaimers</h2>'
        '<p>To the maximum extent permitted by law, we make no warranties that the website will be error-free, secure or that information on it is complete, accurate or current. You use the website at your own risk.</p>'
        '<h2 id="t-liab">11. Limitation of liability</h2>'
        '<p>To the extent permitted by law, INFITEX and its personnel are not liable for any indirect, incidental or consequential loss, or any loss arising from reliance on information on this website.</p>'
        '<h2 id="t-acl">12. Australian Consumer Law</h2>'
        '<p>Nothing in these Terms excludes, restricts or modifies any consumer guarantee, right or remedy that cannot lawfully be excluded under the Australian Consumer Law or other applicable law. Where our liability cannot be excluded but can be limited, it is limited to the maximum extent permitted by law.</p>'
        '<h2 id="t-law">13. Governing law</h2>'
        '<p>These Terms are governed by the laws applicable in Australia, and you submit to the non-exclusive jurisdiction of the courts of Australia, without affecting any mandatory protections available to you where you are located.</p>'
        '<h2 id="t-contact">14. Contact</h2>'
        '<p>Questions about these Terms: <a href="mailto:info@infitexglobal.com">info@infitexglobal.com</a> or <a href="tel:+918500850526">+91 8500 850 526</a>.</p>'
        '<p class="note">This page is general information, not legal advice. Please obtain advice tailored to your circumstances.</p>'
        '</div></div></section>')
    legal_ld = ('{"@context":"https://schema.org","@type":"WebPage","name":"Terms of Service",'
        '"datePublished":"2026-06-01","dateModified":"2026-06-27","inLanguage":"en-AU",'
        '"publisher":{"@id":"%s/#organization"}}') % DOMAIN
    graph = '{"@context":"https://schema.org","@graph":[%s,%s,%s]}' % (
        ORG_LD, legal_ld, breadcrumb([("Home", "index.html"), ("Terms", "terms.html")]))
    return page("terms.html", "Terms of Use — INFITEX Global Advisory",
        "Terms of use for the INFITEX Global Advisory website. INFITEX is not a registered Australian tax or BAS agent; your practice retains lodgement and sign-off.",
        body, graph)

# ================================================================ SITEMAP (human)
def build_sitemap_html():
    crumb = '<div class="shell"><nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> / <span>Sitemap</span></nav></div>'
    groups = [
        ("Main pages", [("Home", "index.html"), ("For Practices", "outsourcing.html"),
                        ("For Business", "industry.html"), ("Digitech", "digitech.html"), ("About", "about.html"), ("Contact", "contact.html")]),
        ("Home sections", [("Software stack", "index.html#stack"), ("Divisions", "index.html#divisions"),
                           ("How it works", "outsourcing.html#how"), ("Engagement models", "index.html#engagement"),
                           ("Security", "index.html#security"), ("Savings calculator", "index.html#calculator"),
                           ("About", "about.html"),
                           ("FAQ", "index.html#faq"), ("Contact", "contact.html")]),
        ("Outsourcing", [("Scope of work", "outsourcing.html#scope"), ("Jobs & frequency", "outsourcing.html#cycle"),
                         ("How it works", "outsourcing.html#how"), ("Key Australian dates", "outsourcing.html#dates"), ("Security", "outsourcing.html#security")]),
        ("Legal", [("Privacy Policy", "privacy.html"), ("Terms of Use", "terms.html")]),
    ]
    blocks = ""
    for title, links in groups:
        lis = "".join('<li><a href="%s">%s</a></li>' % (u, n) for n, u in links)
        blocks += '<div class="footer-col" style="margin-bottom:26px"><h4>%s</h4><ul>%s</ul></div>' % (title, lis)
    body = crumb + ('<section class="section"><div class="shell" style="max-width:80ch">'
        '<span class="eyebrow">Sitemap</span><h1>Everything in one place</h1>'
        '<p class="lead">A human-friendly map of the INFITEX site. There is also an <a href="sitemap.xml">XML sitemap</a> for search engines.</p>'
        '<div class="grid grid-2" style="align-items:start">%s</div>'
        '</div></section>') % blocks
    graph = '{"@context":"https://schema.org","@graph":[%s,%s]}' % (
        ORG_LD, breadcrumb([("Home", "index.html"), ("Sitemap", "sitemap.html")]))
    return page("sitemap.html", "Sitemap — INFITEX Global Advisory",
        "A human-readable sitemap of the INFITEX Global Advisory website.", body, graph)

# ================================================================ ABOUT (dedicated page)
def build_about():
    crumb = '<div class="shell"><nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> / <span>About</span></nav></div>'
    hero = ('<section class="hero"><div class="shell">'
        '<span class="eyebrow">About INFITEX Global Advisory</span>'
        '<h1>A quiet, reliable <span class="accent">extension</span> of your practice</h1>'
        '<p class="answer-lede">INFITEX Global Advisory is an India-based, white-label accounting outsourcing and Digitech partner built specifically for Australian accounting and bookkeeping practices and the businesses they serve. We prepare and process to your standards, while your practice keeps the client, the lodgement and the sign-off.</p>'
        '<div class="hero-cta"><a class="btn btn-primary" href="contact.html">Request a pilot</a>'
        '<a class="btn btn-ghost" data-booking href="contact.html">Book a 15-min call</a></div>'
        '</div></section>')

    prose = ('<div class="about-prose prose">'
        '<p>INFITEX Global Advisory is an India-based accounting outsourcing and Digitech partner built specifically for Australian accounting and bookkeeping practices and the businesses they serve. We exist to be the dependable, accountable team behind your team — and we have built our reputation one carefully delivered job at a time.</p>'
        '<p>Our leadership and senior reviewers bring more than eight years of hands-on Australian compliance experience, with people who have worked the full cycle of a practice — from data entry and bank reconciliations through to BAS, year-end financials, company and trust returns and SMSF. We understand how an Australian practice actually runs at month-end and through the BAS and tax-season peaks, because we have lived those deadlines. That practitioner mindset shapes everything: clean workpapers, sensible coding, sound judgement on what to query, and work that is genuinely ready for your review rather than half-finished.</p>'
        '<p>We are deliberately not a tax or BAS agent. Our job is to prepare and process accurately, to your standards and templates, so your registered professionals can review, sign off and lodge with confidence. That line never blurs — your practice keeps the client relationship, the professional judgement, the lodgement and the sign-off, every time.</p>'
        '<p>We work natively in the software you already use — Xero, XPM, MYOB, QuickBooks, Reckon, BGL, Class, Karbon, Dext, Hubdoc and FYI Docs — so there is no migration and no retraining of your team. A named, accountable individual (or a dedicated team) is assigned to your practice, supported by an independent maker–checker review on every job, role-based least-privilege access and signed confidentiality. We are aligning our controls to ISO 27001 as a direction of travel.</p>'
        '<p>Practices and businesses choose us for three reasons: the quality and traceability of the work, plain-English communication without jargon or surprises, and the overnight rhythm the India–Australia time difference makes possible — work sent at the close of your day is reviewed and ready for your morning, smoothing peak-period workloads without adding local headcount, recruitment risk or permanent overhead.</p>'
        '</div>'
        '<div class="grid grid-2 about-cards">'
        '<div class="card"><div class="ico">%s</div><h3>What we are</h3><p>A white-label preparation and processing team, native to your software, working under your brand and your sign-off.</p></div>'
        '<div class="card"><div class="ico">%s</div><h3>What we are not</h3><p>We are not a registered Australian tax or BAS agent, and we never contact your clients. Lodgement and sign-off stay with your practice.</p></div>'
        '</div>') % (ico("users"), ico("shield"))
    s_about = section("about", "Who we are", "Built for Australian practices", "", prose)

    vmb = ('<div class="vmb-grid">'
        '<article class="vmb-card"><div class="ico">%s</div><h3>Our vision</h3>'
        '<p>To be the most trusted offshore finance and Digitech partner for Australian practices and businesses — invisible to your clients, indispensable to you.</p></article>'
        '<article class="vmb-card"><div class="ico">%s</div><h3>Our mission</h3>'
        '<p>To give every practice dependable capacity and clarity — accurate preparation, on time, to your standards — so your people are free to advise, grow and look after clients.</p></article>'
        '<article class="vmb-card"><div class="ico">%s</div><h3>What we believe</h3>'
        '<p>That the compliance line is sacred, that people deserve named and accountable teams, and that good work plus plain-English communication beats hype every time.</p></article>'
        '</div>') % (ico("target"), ico("bolt"), ico("check"))
    s_vmb = section("vmb", "Vision, mission &amp; values", "What we stand for", "", vmb, alt=True)

    s_cta = '<section class="section" id="cta"><div class="shell">%s</div></section>' % cta_band(
        "Start with a low-risk pilot",
        "Pick a small, defined scope. See the quality, the communication and the turnaround for yourself before you scale.")

    body = alt_sections(crumb + hero + s_about + s_vmb + s_cta)
    graph = '{"@context":"https://schema.org","@graph":[%s,%s]}' % (
        ORG_LD, breadcrumb([("Home", "index.html"), ("About", "about.html")]))
    return page("about.html",
        "About INFITEX Global Advisory | White-label accounting outsourcing",
        "About INFITEX Global Advisory — an India-based, white-label accounting outsourcing and Digitech partner for Australian practices and businesses. Our vision, mission and values.",
        body, graph)

# ================================================================ CONTACT (dedicated page)
def build_contact():
    crumb = '<div class="shell"><nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> / <span>Contact</span></nav></div>'
    hero = ('<section class="hero"><div class="shell">'
        '<span class="eyebrow">Contact</span>'
        '<h1>Talk to us about your <span class="accent">practice</span></h1>'
        '<p class="answer-lede">Tell us what you need help with and we will come back to you by email — no obligation, and no pressure to commit. Prefer chat or a quick call? Use WhatsApp, book a time, or email us directly.</p>'
        '</div></section>')
    subscribe = ('<section class="section" id="subscribe" aria-labelledby="subscribe-title"><div class="shell">'
        '<div class="subscribe-block subscribe-row">'
        '<div class="sb-text">'
        '<span class="eyebrow">Stay in the loop</span>'
        '<h2 class="section-title" id="subscribe-title">Australian compliance-dates digest</h2>'
        '<p class="lead" style="margin:0">An occasional, opt-in email with upcoming BAS, IAS, super and tax dates.</p></div>'
        '<form id="subscribeForm" class="fs-form" novalidate>'
        '<div class="fs-row"><label class="sr-only" for="sub-email">Email</label>'
        '<input class="input" id="sub-email" name="email" type="email" inputmode="email" autocomplete="email" placeholder="you@yourfirm.com.au" required>'
        '<button type="submit" class="btn btn-primary">Subscribe</button></div>'
        '<label class="optin"><input type="checkbox" required><span>I agree to receive the compliance-dates digest and accept the <a href="privacy.html">Privacy</a> terms. Unsubscribe anytime (Spam Act 2003 compliant).</span></label>'
        '<p class="form-status" id="subStatus" role="status"></p>'
        '</form></div></div></section>')
    body = alt_sections(crumb + hero + contact_section(page_mode=True) + subscribe)
    graph = '{"@context":"https://schema.org","@graph":[%s,%s]}' % (
        ORG_LD, breadcrumb([("Home", "index.html"), ("Contact", "contact.html")]))
    return page("contact.html",
        "Contact INFITEX Global Advisory | Outsourced accounting, Australia",
        "Contact INFITEX Global Advisory — white-label accounting outsourcing and Digitech for Australian practices and businesses. Send an enquiry, WhatsApp, book a call or email us.",
        body, graph)

# ================================================================ write all
def write(fn, content):
    with open(OUT + "/" + fn, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", fn, "(%d bytes)" % len(content.encode("utf-8")))

if __name__ == "__main__":
    # Cache-busting: hash styles.css / app.js so each deploy gets fresh asset URLs.
    import hashlib
    def _ver(fn):
        try:
            with open(OUT + "/" + fn, "rb") as f: return hashlib.sha1(f.read()).hexdigest()[:8]
        except OSError:
            return ""
    P.CSS_VER = _ver("styles.css")
    P.JS_VER = _ver("app.js")
    print("asset versions -> css:%s js:%s" % (P.CSS_VER or "(none)", P.JS_VER or "(none)"))
    write("index.html", build_home())
    write("outsourcing.html", build_outsourcing())
    write("industry.html", build_industry())
    write("digitech.html", build_digitech())
    write("about.html", build_about())
    write("contact.html", build_contact())
    write("privacy.html", build_privacy())
    write("terms.html", build_terms())
    write("sitemap.html", build_sitemap_html())
    print("ALL PAGES BUILT")
