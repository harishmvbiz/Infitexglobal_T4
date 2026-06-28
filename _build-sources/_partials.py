#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
OUT = "/home/claude/infitex-site"
# Cache-busting versions for static assets (set by build.py from file content hashes).
CSS_VER = ""
JS_VER = ""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
'<link href="https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@500;600;700;800&family=Source+Sans+3:ital,wght@0,400;0,600;1,400&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">')

NOFLASH = ("<script>(function(){try{var d=document.documentElement;var t=localStorage.getItem('ix-theme')||'light';"
"d.setAttribute('data-theme',t);if(localStorage.getItem('ix-contrast')==='high')d.setAttribute('data-contrast','high');"
"if(localStorage.getItem('ix-grayscale')==='on')d.setAttribute('data-grayscale','on');var ts=localStorage.getItem('ix-textstep');"
"var s=[-2,0,2,4,6];if(ts!==null)d.style.setProperty('--type-scale-step',(s[parseInt(ts,10)]||0)+'px');}catch(e){}})();</script>")

DOMAIN = "https://infitexglobal.com"

LOGO_SVG = ('<svg class="brand-logo" viewBox="0 0 309.3 72.0" role="img" aria-label="INFITEX" focusable="false"><g class="brand-word" transform="translate(0 72.00) scale(0.10465 -0.10465)"><g transform="translate(0.0 0)"><path d="M40 0V688H220V0Z"/></g><g transform="translate(260.0 0)"><path d="M327 0 216 310H211V0H40V688H213L309 421H315V688H486V0Z"/></g><g transform="translate(786.0 0)"><path d="M40 0V688H377V540H220V402H356V254H220V0Z"/></g><g transform="translate(1183.0 0)"><path d="M40 0V688H220V0Z"/></g><g transform="translate(1443.0 0)"><path d="M126 0V535H7V688H426V535H307V0Z"/></g><g transform="translate(1876.0 0)"><path d="M40 0V688H393V540H220V421H367V274H220V148H393V0Z"/></g></g><g class="brand-x"><g class="bx-ring" fill="none"><circle cx="273.11" cy="36.00" r="24.48"/><circle cx="273.11" cy="36.00" r="32.40"/></g><path class="bx-ink" d="M 242.15 0.00 L 253.67 0.00 L 304.07 72.00 L 292.55 72.00 Z"/><rect class="bx-acc" x="262.31" y="-4.32" width="21.60" height="80.64" rx="10.80" transform="rotate(40 273.11 36.00)"/><circle class="bx-dot" cx="273.11" cy="36.00" r="7.20"/></g></svg>')

# ---- inline SVG icons ----
IC = {
 'search':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4-4"/></svg>',
 'sun':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4.5"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M19.1 4.9l-1.4 1.4M6.3 17.7l-1.4 1.4"/></svg>',
 'access':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="4" r="1.6"/><path d="M4 7h16M9 7l1 5 1.5 7M15 7l-1 5"/></svg>',
 'menu':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 6h18M3 12h18M3 18h18"/></svg>',
 'close':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>',
 'wa':'<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a9.9 9.9 0 0 0-8.5 15l-1.3 4.8 4.9-1.3A10 10 0 1 0 12 2Zm5.6 14.1c-.2.6-1.2 1.2-1.7 1.2s-1 .2-3.3-.7-3.7-3.2-3.8-3.4-1-1.3-1-2.4.6-1.7.8-1.9.4-.3.6-.3h.5c.2 0 .4 0 .6.5l.8 1.9c.1.2.1.4 0 .5l-.3.5-.4.4c-.1.1-.3.3-.1.5l.9 1.4c.6.9 1.4 1.2 1.6 1.3s.4.1.5 0l.7-.8c.2-.2.3-.2.5-.1l1.7.8c.2.1.4.2.4.3.1.2.1.7-.1 1.3Z"/></svg>',
 'mail':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>',
 'top':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 19V5M5 12l7-7 7 7"/></svg>',
 'li':'<svg viewBox="0 0 24 24" fill="currentColor"><path d="M4.98 3.5A2.5 2.5 0 1 1 0 3.5a2.5 2.5 0 0 1 4.98 0ZM.5 8h4V24h-4V8Zm7.5 0h3.8v2.2h.1c.5-1 1.8-2.2 3.8-2.2 4 0 4.8 2.6 4.8 6V24h-4v-6.9c0-1.7 0-3.8-2.3-3.8s-2.7 1.8-2.7 3.7V24H8V8Z"/></svg>',
 'fb':'<svg viewBox="0 0 24 24" fill="currentColor"><path d="M22 12a10 10 0 1 0-11.6 9.9v-7H7.9V12h2.5V9.8c0-2.5 1.5-3.9 3.8-3.9 1.1 0 2.2.2 2.2.2v2.5h-1.3c-1.2 0-1.6.8-1.6 1.6V12h2.8l-.4 2.9h-2.4v7A10 10 0 0 0 22 12Z"/></svg>',
 'ig':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg>',
 'x':'<svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.2 2H21l-6.5 7.4L22 22h-6.8l-4.7-6.2L5 22H2.2l7-8L2 2h6.9l4.3 5.7L18.2 2Zm-1.2 18h1.5L7.1 3.9H5.5L17 20Z"/></svg>',
 'yt':'<svg viewBox="0 0 24 24" fill="currentColor"><path d="M23 12s0-3.2-.4-4.7a2.5 2.5 0 0 0-1.8-1.8C19.3 5 12 5 12 5s-7.3 0-8.8.4A2.5 2.5 0 0 0 1.4 7.2C1 8.8 1 12 1 12s0 3.2.4 4.7a2.5 2.5 0 0 0 1.8 1.8C4.7 19 12 19 12 19s7.3 0 8.8-.4a2.5 2.5 0 0 0 1.8-1.8C23 15.2 23 12 23 12ZM10 15V9l5 3-5 3Z"/></svg>',
 'shield':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 3l7 3v5c0 4.4-3 7.4-7 9-4-1.6-7-4.6-7-9V6l7-3z"/><path d="M9 12l2 2 4-4"/></svg>',
 'stack':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 3l9 5-9 5-9-5 9-5Z"/><path d="M3 13l9 5 9-5M3 17l9 5 9-5"/></svg>',
 'cog':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="3.2"/><path d="M19 12a7 7 0 0 0-.1-1l2-1.5-2-3.4-2.3 1a7 7 0 0 0-1.7-1L14.5 2h-5l-.4 2.6a7 7 0 0 0-1.7 1l-2.3-1-2 3.4L3 11a7 7 0 0 0 0 2l-2 1.5 2 3.4 2.3-1a7 7 0 0 0 1.7 1l.4 2.6h5l.4-2.6a7 7 0 0 0 1.7-1l2.3 1 2-3.4-2-1.5a7 7 0 0 0 .1-1Z"/></svg>',
 'globe':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.5 2.5 15 0 18M12 3c-2.5 2.5-2.5 15 0 18"/></svg>',
 'doc':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8l-5-5Z"/><path d="M14 3v5h5M9 13h6M9 17h6"/></svg>',
 'clock':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
 'users':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="9" cy="8" r="3.2"/><path d="M3 20a6 6 0 0 1 12 0M16 5a3 3 0 0 1 0 6M21 20a5.5 5.5 0 0 0-4-5.3"/></svg>',
 'bolt':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M13 2L4 14h6l-1 8 9-12h-6l1-8Z"/></svg>',
 'lock':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/></svg>',
 'check':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M5 12l5 5 9-11"/></svg>',
 'phone':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L20 13l1 4v3a1 1 0 0 1-1 1A16 16 0 0 1 4 5a1 1 0 0 1 1-1Z"/></svg>',
 'cal':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="4" width="18" height="17" rx="2"/><path d="M3 9h18M8 2v4M16 2v4"/></svg>',
 'building':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="4" y="3" width="16" height="18" rx="1.5"/><path d="M8 7h2M14 7h2M8 11h2M14 11h2M8 15h2M14 15h2M10 21v-3h4v3"/></svg>',
 'trend':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 17l6-6 4 4 7-8"/><path d="M17 7h4v4"/></svg>',
 'pie':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 3a9 9 0 1 0 9 9h-9V3z"/><path d="M14 3.2A9 9 0 0 1 20.8 10H14V3.2z"/></svg>',
 'target':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5" fill="currentColor"/></svg>',
 'cash':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="3"/><path d="M6 9v6M18 9v6"/></svg>',
 'tag':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20.59 13.41 12 22l-9-9V3h10l7.59 7.59a2 2 0 0 1 0 2.82z"/><circle cx="7.5" cy="7.5" r="1.5"/></svg>',
 'wrench':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a4 4 0 0 0 5 5l-9 9a2.83 2.83 0 1 1-4-4z"/><path d="M14.7 6.3 9.7 11.3"/></svg>',
 'headset':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 18v-6a9 9 0 0 1 18 0v6"/><path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"/></svg>',
 'pin':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s7-5.5 7-11a7 7 0 1 0-14 0c0 5.5 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/></svg>',
 'truck':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M1 3h15v13H1z"/><path d="M16 8h4l3 3v5h-7z"/><circle cx="5.5" cy="18.5" r="2"/><circle cx="18.5" cy="18.5" r="2"/></svg>',
 'rocket':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="M12 15l-3-3a22 22 0 0 1 8-10c2.5 0 4 1.5 4 4a22 22 0 0 1-10 8z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/></svg>',
 'factory':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M2 20h20V9l-6 4V9l-6 4V4H4l-2 16z"/><path d="M7 20v-4M12 20v-4M17 20v-4"/></svg>',
 'qr':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><path d="M14 14h3v3M21 14v.01M14 21h.01M17 21h4v-4M21 17v.01"/></svg>',
}

# -----------------------------------------------------------------------------
# NAVIGATION (Accario-style: simple top tabs + "What we do" / "Who we help" mega-menus)
# -----------------------------------------------------------------------------
# A nav entry is either:
#   ("Label", "href")                         -> a simple top-level link
#   ("Label", None, [ (group_label, [ (label, href, desc), ... ]) ... ])  -> a dropdown
#
# "What we do"  = every service, clubbed into categories (keeps the top header simple).
# "Who we help" = the audiences/sections: Business & Industries, Practices, Digitech.

NAV = [
    ("Home", "index.html"),
    ("What we do", None, [
        ("Accounting & bookkeeping", [
            ("Bookkeeping & reconciliations", "outsourcing.html#scope", "Books kept accurate, coded and reconciled."),
            ("Accounts payable & receivable", "outsourcing.html#scope", "Bills, invoices and debtor follow-up."),
            ("Year-end financials", "outsourcing.html#scope", "Financial statements to your standards."),
            ("Workpapers", "outsourcing.html#scope", "Clean, traceable workpapers behind every job."),
        ]),
        ("Payroll, BAS & compliance", [
            ("Payroll & STP", "outsourcing.html#scope", "Pay runs and Single Touch Payroll, ready to lodge."),
            ("BAS / IAS preparation", "outsourcing.html#scope", "Activity statements drafted for your sign-off."),
            ("Company & trust tax returns", "outsourcing.html#scope", "Returns prepared; your agent signs and lodges."),
            ("SMSF accounts (BGL/Class)", "outsourcing.html#scope", "Self-managed super fund accounts & workpapers."),
        ]),
        ("Advisory & Virtual CFO", [
            ("Virtual CFO", "industry.html#vcfo", "Senior finance leadership, fractionally."),
            ("Management accounts & reporting", "industry.html#what", "Monthly, decision-ready reporting."),
            ("Budgeting & forecasting", "industry.html#what", "Budgets, rolling forecasts and scenarios."),
            ("Cash-flow management", "industry.html#vcfo", "13-week cash-flow and working-capital visibility."),
        ]),
        ("Digitech", [
            ("Web design & build", "digitech.html#services", "Fast, accessible, mobile-first websites."),
            ("Domains, hosting & email", "digitech.html#services", "Set up and managed for you."),
            ("SEO & Google Business Profile", "digitech.html#services", "Be found by local clients."),
            ("Care & maintenance", "digitech.html#services", "Updates, backups and ongoing changes."),
        ]),
    ]),
    ("Who we help", None, [
        ("By audience", [
            ("For accounting practices", "outsourcing.html", "White-label back office for your firm."),
            ("For business & industry", "industry.html", "A dedicated outsourced finance team."),
            ("Digitech", "digitech.html", "Web, email & SEO for client-facing growth."),
        ]),
        ("Industries we serve", [
            ("Construction & trades", "industry.html#industries", "Job costing, payroll and BAS."),
            ("Retail & e-commerce", "industry.html#industries", "High-volume reconciliations and reporting."),
            ("Professional services", "industry.html#industries", "Clean books and management accounts."),
            ("Healthcare & allied health", "industry.html#industries", "Compliant bookkeeping and payroll."),
        ]),
    ]),
    ("About us", None, [
        ("Company", [
            ("About INFITEX", "about.html", "A dependable extension of your team, native to your stack."),
            ("Vision, mission & values", "about.html#vmb", "What we stand for and how we work."),
        ]),
        ("Proof & answers", [
            ("Our stories", "index.html#testimonials", "What practices and businesses say about us."),
            ("FAQ", "index.html#faq", "Honest answers on the compliance line, security and how we work."),
        ]),
    ]),
    ("Contact", "contact.html"),
]

def _flat_nav_pairs():
    """Flatten NAV to (label, href) for mobile + footer fallbacks."""
    pairs = []
    for item in NAV:
        if len(item) == 2:
            pairs.append((item[0], item[1]))
        else:
            for _grp, links in item[2]:
                for label, href, _desc in links:
                    pairs.append((label, href))
    return pairs

def _is_current(href, cur):
    return href and href.split("#")[0] == cur

def header(cur):
    # ---- desktop nav (simple tabs + mega-menus) ----
    links = ""
    for item in NAV:
        if len(item) == 2:
            label, href = item
            ac = ' aria-current="page"' if _is_current(href, cur) else ''
            links += '<a class="nav-link" href="%s"%s>%s</a>' % (href, ac, label)
        else:
            label, _none, groups = item
            mid = label.lower().replace(" ", "-")
            # Mark a mega-menu trigger active only when the current page is the
            # audience landing page it points to (the "Who we help" menu), so the
            # highlight is consistent across pages. "What we do" is a services
            # catalogue (every page appears in it), so it never marks active.
            active = (label == "Who we help") and any(
                href and href.split("#")[0] == cur
                for _g, ls in groups for _l, href, _d in ls)
            ac = ' data-current="true"' if active else ''
            panel = '<div class="mega-grid">'
            for gname, ls in groups:
                panel += '<div class="mega-col"><p class="mega-h">%s</p><ul>' % gname
                for l, h, d in ls:
                    panel += ('<li><a href="%s"><span class="mega-t">%s</span>'
                              '<span class="mega-d">%s</span></a></li>') % (h, l, d)
                panel += '</ul></div>'
            panel += '</div>'
            links += (
                '<div class="nav-item has-mega">'
                '<button type="button" class="nav-link nav-trigger" aria-expanded="false" '
                'aria-haspopup="true" aria-controls="mega-%s"%s>%s'
                '<svg class="caret" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
                '<path d="M6 9l6 6 6-6" fill="none" stroke="currentColor" stroke-width="2" '
                'stroke-linecap="round" stroke-linejoin="round"/></svg></button>'
                '<div class="mega-panel" id="mega-%s" role="region" aria-label="%s">%s</div>'
                '</div>'
            ) % (mid, ac, label, mid, label, panel)

    # ---- mobile nav (accordion for dropdowns, plain links otherwise) ----
    mlinks = ""
    for item in NAV:
        if len(item) == 2:
            label, href = item
            mlinks += '<a class="m-link" href="%s">%s</a>' % (href, label)
        else:
            label, _none, groups = item
            mid = label.lower().replace(" ", "-")
            sub = ""
            for gname, ls in groups:
                sub += '<p class="m-group">%s</p>' % gname
                for l, h, _d in ls:
                    sub += '<a class="m-sublink" href="%s">%s</a>' % (h, l)
            mlinks += (
                '<div class="m-acc">'
                '<button type="button" class="m-acc-btn" aria-expanded="false" '
                'aria-controls="macc-%s">%s'
                '<svg class="caret" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
                '<path d="M6 9l6 6 6-6" fill="none" stroke="currentColor" stroke-width="2" '
                'stroke-linecap="round" stroke-linejoin="round"/></svg></button>'
                '<div class="m-acc-panel" id="macc-%s">%s</div>'
                '</div>'
            ) % (mid, label, mid, sub)

    return ('<a class="skip-link" href="#main">Skip to content</a>'
    '<header class="site-header"><div class="shell header-inner">'
    '<a class="brand" href="index.html" aria-label="INFITEX Global Advisory — home">'+LOGO_SVG+'</a>'
    '<nav class="nav" aria-label="Primary">'+links+'</nav>'
    '<div class="header-tools">'
    '<button class="icon-btn search-btn" data-open-search aria-label="Search the site">'+IC["search"]+'<span>Search</span><kbd>/</kbd></button>'
    '<button class="icon-btn" data-theme-toggle aria-label="Toggle light or dark theme" aria-pressed="false">'+IC["sun"]+'</button>'
    '<button class="icon-btn" data-open-a11y aria-label="Open accessibility settings">'+IC["access"]+'</button>'
    '<button class="icon-btn qr-header-btn" data-open-qr aria-label="Show QR code to save our contact" title="Save our contact (QR)">'+IC["qr"]+'</button>'
    '<a class="btn btn-primary header-cta" href="contact.html">Get in touch</a>'
    '<button class="icon-btn hamburger" data-open-nav aria-label="Open menu" aria-expanded="false">'+IC["menu"]+'</button>'
    '</div></div></header>'
    '<div class="mobile-nav" id="mobileNav" aria-hidden="true"><div class="mobile-nav-top">'
    '<a class="brand" href="index.html" aria-label="INFITEX home">'+LOGO_SVG+'</a>'
    '<button class="icon-btn" data-close-nav aria-label="Close menu">'+IC["close"]+'</button></div>'
    '<nav aria-label="Mobile">'+mlinks+'</nav>'
    '<div style="margin-top:24px;display:flex;gap:10px;flex-wrap:wrap"><button class="btn btn-ghost" data-open-wa>WhatsApp us</button><a class="btn btn-primary" href="contact.html">Get in touch</a></div>'
    '</div>')

def footer():
    return ('<footer class="site-footer"><div class="shell">'
    '<div class="footer-top">'
    '<div class="footer-brand"><a class="brand" href="index.html" aria-label="INFITEX home">'+LOGO_SVG+'</a>'
    '<p class="footer-blurb">A white-label outsourcing and Digitech partner for Australian accounting &amp; bookkeeping practices. We prepare and process; your practice keeps the client, the lodgement and the sign-off.</p>'
    '<ul class="footer-contact">'
    '<li>'+IC["mail"]+'<a href="mailto:info@infitexglobal.com">info@infitexglobal.com</a></li>'
    '<li>'+IC["phone"]+'<a href="tel:+918500850526">+91 8500 850 526</a></li></ul>'
    '<button class="btn btn-ghost btn-sm" data-open-wa>WhatsApp enquiry</button>'
    '<div class="socials">'
    '<a href="https://www.linkedin.com/company/infitexglobal" aria-label="INFITEX on LinkedIn" rel="me noopener" target="_blank">'+IC["li"]+'</a>'
    '<a href="https://www.facebook.com/infitexglobal" aria-label="INFITEX on Facebook" rel="me noopener" target="_blank">'+IC["fb"]+'</a>'
    '<a href="https://www.instagram.com/infitexglobal" aria-label="INFITEX on Instagram" rel="me noopener" target="_blank">'+IC["ig"]+'</a>'
    '<a href="https://x.com/infitexglobal" aria-label="INFITEX on X" rel="me noopener" target="_blank">'+IC["x"]+'</a>'
    '<a href="https://www.youtube.com/@infitexglobal" aria-label="INFITEX on YouTube" rel="me noopener" target="_blank">'+IC["yt"]+'</a>'
    '</div></div>'
    '<div class="footer-cols">'
    '<div class="footer-col"><h4>Who we help</h4><ul>'
    '<li><a href="outsourcing.html">For accounting practices</a></li>'
    '<li><a href="industry.html">For business &amp; industry</a></li>'
    '<li><a href="digitech.html">Digitech</a></li>'
    '<li><a href="industry.html#industries">Industries we serve</a></li></ul></div>'
    '<div class="footer-col"><h4>What we do</h4><ul>'
    '<li><a href="outsourcing.html#scope">Accounting &amp; bookkeeping</a></li>'
    '<li><a href="outsourcing.html#scope">Payroll, BAS &amp; compliance</a></li>'
    '<li><a href="industry.html#vcfo">Virtual CFO &amp; advisory</a></li>'
    '<li><a href="digitech.html#services">Digitech (web &amp; SEO)</a></li></ul></div>'
    '<div class="footer-col"><h4>Company</h4><ul>'
    '<li><a href="about.html">About</a></li>'
    '<li><a href="outsourcing.html#how">How it works</a></li>'
    '<li><a href="index.html#faq">FAQ</a></li>'
    '<li><a href="contact.html">Contact</a></li>'
    '<li><a href="sitemap.html">Sitemap</a></li></ul></div>'
    '</div></div>'
    '<p class="compliance-line">INFITEX is not a registered Australian tax or BAS agent. We are the preparation and processing layer behind your practice, which retains lodgement and sign-off. We do not publish prices — contact us for the best pricing for your practice.</p>'
    '<div class="footer-bottom"><span>&copy; <span data-year>2026</span> INFITEX Global Advisory. All rights reserved.</span>'
    '<span class="footer-legal"><a href="privacy.html">Privacy</a><a href="terms.html">Terms</a><a href="sitemap.html">Sitemap</a></span></div>'
    '</div></footer>')

def lead_fields(prefix):
    # name, email, mobile (country combo + 10 digits), business, interest, message + honeypot
    return ('<div class="form-row"><label class="lbl" for="%s-name">Name <span class="req">*</span></label>'
    '<input class="input" id="%s-name" name="name" type="text" autocomplete="name" required>'
    '<span class="field-err">Please enter your name (letters, at least 2 characters).</span></div>'
    '<div class="form-row"><label class="lbl" for="%s-email">Work email <span class="req">*</span></label>'
    '<input class="input" id="%s-email" name="email" type="email" autocomplete="email" inputmode="email" required>'
    '<span class="field-err">Please enter a valid email address.</span></div>'
    '<div class="form-row"><label class="lbl" for="%s-mobile">Mobile <span class="req">*</span></label>'
    '<div class="tel-wrap"><div class="cc-combo" data-cc>'
    '<input class="cc-input" type="text" inputmode="tel" aria-label="Country dialing code" value="+61" autocomplete="off">'
    '<div class="cc-list" role="listbox" aria-label="Country dialing codes"></div></div>'
    '<input class="input tel-num" id="%s-mobile" name="mobile_local" type="tel" inputmode="numeric" maxlength="10" placeholder="4XX XXX XXX" aria-label="Mobile number (10 digits)"></div>'
    '<span class="field-err">Enter a 10-digit mobile number (digits only).</span></div>'
    '<div class="form-row"><label class="lbl" for="%s-company">Business name <span class="req">*</span></label>'
    '<input class="input" id="%s-company" name="company" type="text" autocomplete="organization" required>'
    '<span class="field-err">Please enter your business name.</span></div>'
    '<div class="form-row"><label class="lbl" for="%s-interest">Enquiring about</label>'
    '<select class="input" id="%s-interest" name="interest"><option value="">Choose a topic…</option>'
    '<option>Accounting outsourcing</option><option>Bookkeeping &amp; reconciliations</option><option>Payroll &amp; STP</option>'
    '<option>BAS / IAS preparation</option><option>Year-end financials &amp; tax</option><option>SMSF accounts</option>'
    '<option>A low-risk pilot</option><option>Digitech (website / SEO)</option><option>Something else</option></select></div>'
    '<div class="form-row"><label class="lbl" for="%s-message">Message</label>'
    '<textarea class="input" id="%s-message" name="message" placeholder="A line or two about your practice and what you need help with."></textarea>'
    '<span class="field-err">Please add a short message (at least 10 characters).</span></div>'
    '<input type="text" class="hp" name="botcheck" tabindex="-1" autocomplete="off" aria-hidden="true">'
    )%((prefix,)*12)

def dialogs():
    return (
    # a11y
    '<dialog id="a11yDialog" aria-label="Accessibility settings"><div class="dialog-card">'
    '<div class="dialog-head"><h2>Accessibility</h2><button class="icon-btn" data-close aria-label="Close">'+IC["close"]+'</button></div>'
    '<div class="dialog-body">'
    '<div class="form-row"><label class="lbl">Text size</label><div style="display:flex;gap:8px">'
    '<button class="btn btn-ghost" data-text="dec" aria-label="Decrease text size">A–</button>'
    '<button class="btn btn-ghost" data-text="reset" aria-label="Reset text size">Reset</button>'
    '<button class="btn btn-ghost" data-text="inc" aria-label="Increase text size">A+</button></div></div>'
    '<div class="form-row"><label class="lbl">Theme</label><button class="btn btn-ghost" data-theme-toggle aria-pressed="false"><span data-theme-label>Light</span> mode</button></div>'
    '<div class="form-row"><label class="lbl">High contrast</label><button class="btn btn-ghost" data-contrast-toggle aria-pressed="false">Toggle high contrast</button></div>'
    '<div class="form-row"><label class="lbl">Grayscale</label><button class="btn btn-ghost" data-gray-toggle aria-pressed="false">Toggle grayscale</button></div>'
    '<p class="form-note">Your preferences are saved on this device.</p>'
    '</div></div></dialog>'
    # whatsapp
    '<dialog id="waDialog" aria-label="WhatsApp enquiry"><div class="dialog-card"><form id="waForm" novalidate>'
    '<div class="dialog-head"><h2>WhatsApp enquiry</h2><button type="button" class="icon-btn" data-close aria-label="Close">'+IC["close"]+'</button></div>'
    '<div class="dialog-body"><p class="form-note" style="margin-bottom:16px">We\'ll draft a tidy message and open WhatsApp for you to send.</p>'
    +lead_fields("wa")+
    '<p class="form-status" id="waStatus" role="status"></p></div>'
    '<div class="dialog-foot"><button type="button" class="btn btn-ghost" data-close>Cancel</button><button type="submit" class="btn btn-primary">Draft &amp; open WhatsApp</button></div>'
    '</form></div></dialog>'
    # email
    '<dialog id="mailDialog" aria-label="Email enquiry"><div class="dialog-card"><form id="mailForm" novalidate>'
    '<div class="dialog-head"><h2>Email enquiry</h2><button type="button" class="icon-btn" data-close aria-label="Close">'+IC["close"]+'</button></div>'
    '<div class="dialog-body"><p class="form-note" style="margin-bottom:16px">We\'ll draft a tidy email and open your mail app for you to send.</p>'
    +lead_fields("mail")+
    '<p class="form-status" id="mailStatus" role="status"></p></div>'
    '<div class="dialog-foot"><button type="button" class="btn btn-ghost" data-close>Cancel</button><button type="submit" class="btn btn-primary">Draft &amp; open email</button></div>'
    '</form></div></dialog>'
    # QR / save contact
    '<dialog id="qrDialog" aria-label="Save our contact">'
    '<div class="dialog-card qr-dialog-card">'
    '<div class="dialog-head"><h2>Save our contact</h2><button type="button" class="icon-btn" data-close aria-label="Close">'+IC["close"]+'</button></div>'
    '<div class="dialog-body" style="text-align:center">'
    '<p class="form-note" style="margin-bottom:16px">Scan with your phone camera — iPhone or Android — to save INFITEX Global Advisory to your contacts.</p>'
    '<div class="qr-dialog-img"><img src="infitex-contact-qr.svg" alt="QR code to save INFITEX Global Advisory contact details" width="220" height="220"></div>'
    '<p class="form-note" style="margin-top:14px">Or reach us directly:<br>'
    '<a href="mailto:info@infitexglobal.com">info@infitexglobal.com</a> · '
    '<a href="tel:+918500850526">+91 8500 850 526</a></p>'
    '</div></div></dialog>'
    )

def search_overlay():
    return ('<div class="search-overlay" id="searchOverlay" aria-hidden="true" role="dialog" aria-label="Search">'
    '<div class="search-panel"><div class="search-input-row">'+IC["search"]+
    '<input id="searchInput" type="text" placeholder="Search pages, services, FAQs…" aria-label="Search" autocomplete="off">'
    '</div><div class="search-results" id="searchResults"></div>'
    '<div class="search-foot"><span>Up / Down to navigate</span><span>Enter to open</span><span>Esc to close</span></div>'
    '</div></div>')

def fabs():
    cal = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="17" rx="2"/><path d="M3 9h18M8 2v4M16 2v4"/></svg>'
    return ('<div class="fab">'
    '<a class="fab-cta" data-booking href="contact.html" data-fab-label="Book a 15-min call" role="button" aria-label="Book a 15-min call">'+cal+'</a>'
    '<a class="wa" href="#" data-open-wa data-fab-label="WhatsApp us" role="button" aria-label="WhatsApp us">'+IC["wa"]+'</a>'
    '<a class="callfab" href="tel:+918500850526" data-fab-label="Call +91 8500 850 526" aria-label="Call +91 8500 850 526">'+IC["phone"]+'</a>'
    '<button class="mailfab" data-open-mail data-fab-label="Email us" aria-label="Email us">'+IC["mail"]+'</button>'
    '<button class="qrfab" data-open-qr data-fab-label="Save our contact" aria-label="Show QR code to save our contact">'+IC["qr"]+'</button>'
    '<button id="backTop" aria-label="Back to top">'+IC["top"]+'</button></div>')

SEARCH_INDEX_JS = """<script>window.INFITEX_SEARCH=[
{type:"Pages",title:"Home",snippet:"White-label accounting outsourcing & Digitech for Australian practices.",url:"index.html"},
{type:"Pages",title:"For Accounting Practices",snippet:"White-label outsourcing across the full Australian compliance cycle.",url:"outsourcing.html"},
{type:"Pages",title:"For Business & Industry",snippet:"Outsourced accounting, finance and Virtual CFO for Australian companies.",url:"industry.html"},
{type:"Services",title:"Virtual CFO",snippet:"Management & board reporting, cash-flow forecasting, budgeting and KPI dashboards.",url:"industry.html#vcfo"},
{type:"Services",title:"Management accounts & reporting",snippet:"Monthly management accounts and decision-ready reporting.",url:"industry.html#what"},
{type:"Services",title:"Budgeting & forecasting",snippet:"Budgets, rolling forecasts and scenario planning.",url:"industry.html#what"},
{type:"Services",title:"Cash-flow management",snippet:"13-week cash-flow forecasts and working-capital visibility.",url:"industry.html#vcfo"},
{type:"Pages",title:"Digitech",snippet:"Websites, domains, hosting, business email, SEO and Google Business Profile.",url:"digitech.html"},
{type:"Pages",title:"Privacy",snippet:"How we handle data, aligned to the Privacy Act 1988 and the APPs.",url:"privacy.html"},
{type:"Pages",title:"Terms",snippet:"Terms of use for the INFITEX website and services.",url:"terms.html"},
{type:"Pages",title:"Contact",snippet:"Send an enquiry, WhatsApp, book a call or email us.",url:"contact.html"},
{type:"Pages",title:"Sitemap",snippet:"Every page and key section in one place.",url:"sitemap.html"},
{type:"Sections",title:"How it works",snippet:"A simple, low-risk way to slot into your practice.",url:"outsourcing.html#how"},
{type:"Sections",title:"Engagement models",snippet:"Dedicated staff, per-job or ad-hoc — flexible and pilot-friendly.",url:"index.html#engagement"},
{type:"Sections",title:"Security",snippet:"Role-based access, named individuals, ISO 27001 alignment on our roadmap.",url:"index.html#security"},
{type:"Sections",title:"Savings calculator",snippet:"Indicative annual saving range in AUD — not a quote.",url:"index.html#calculator"},
{type:"Sections",title:"Key Australian dates",snippet:"BAS, IAS, super and tax reference dates.",url:"outsourcing.html#dates"},
{type:"Pages",title:"About INFITEX",snippet:"Our vision, mission and values; how we work with Australian practices.",url:"about.html"},
{type:"Sections",title:"Start a pilot",snippet:"Begin with a low-risk pilot on a defined scope.",url:"index.html#pilot"},
{type:"Services",title:"Bookkeeping & reconciliations",snippet:"Day-to-day books kept accurate and current.",url:"outsourcing.html#cycle"},
{type:"Services",title:"Accounts payable & receivable",snippet:"Bills and invoices processed and matched.",url:"outsourcing.html#cycle"},
{type:"Services",title:"Payroll & STP",snippet:"Pay runs prepared and Single Touch Payroll ready.",url:"outsourcing.html#cycle"},
{type:"Services",title:"BAS / IAS preparation",snippet:"Activity statements drafted for your review and lodgement.",url:"outsourcing.html#cycle"},
{type:"Services",title:"Year-end financials",snippet:"Financial statements prepared to your standards.",url:"outsourcing.html#cycle"},
{type:"Services",title:"Company & trust tax returns",snippet:"Returns prepared; your practice signs off and lodges.",url:"outsourcing.html#cycle"},
{type:"Services",title:"SMSF accounts (BGL/Class)",snippet:"Self-managed super fund accounts and workpapers.",url:"outsourcing.html#cycle"},
{type:"Services",title:"Workpapers",snippet:"Clean, traceable workpapers behind every job.",url:"outsourcing.html#cycle"},
{type:"Services",title:"Web design & build",snippet:"Fast, accessible websites for your practice.",url:"digitech.html"},
{type:"Services",title:"Domains, hosting & business email",snippet:"Set up and managed for you.",url:"digitech.html"},
{type:"Services",title:"SEO & Google Business Profile",snippet:"Be found by local clients.",url:"digitech.html"},
{type:"FAQs",title:"Do you contact our clients?",snippet:"No — you keep the client relationship.",url:"index.html#faq"},
{type:"FAQs",title:"Are you a registered AU tax or BAS agent?",snippet:"No — your practice keeps lodgement and sign-off.",url:"index.html#faq"},
{type:"FAQs",title:"Who lodges and signs off?",snippet:"Your practice does; we prepare and process.",url:"index.html#faq"},
{type:"FAQs",title:"Which software do you work in?",snippet:"XPM, Xero, MYOB, QuickBooks, FYI, Dext, BGL/Class, Karbon.",url:"index.html#faq"},
{type:"FAQs",title:"How do you keep our data secure?",snippet:"Role-based access, named individuals, confidentiality.",url:"index.html#faq"},
{type:"FAQs",title:"Can we start with a trial?",snippet:"Yes — a low-risk pilot on a defined scope.",url:"index.html#faq"},
{type:"FAQs",title:"Do you publish pricing?",snippet:"No — contact us for the best pricing for your practice.",url:"index.html#faq"}
];</script>"""

def page(filename, title, desc, body, jsonld, og_type="website", section_nav=False):
    canon = DOMAIN + "/" + filename
    # WebPage + speakable node tells AI assistants which parts to read/quote.
    webpage_ld = ('{"@context":"https://schema.org","@type":"WebPage","@id":"%s#webpage",'
        '"url":"%s","name":"%s","description":"%s","inLanguage":"en-AU",'
        '"isPartOf":{"@id":"%s/#website"},"about":{"@id":"%s/#organization"},'
        '"speakable":{"@type":"SpeakableSpecification","cssSelector":["h1",".answer-lede"]}}'
        ) % (canon, canon, title.replace('"','\\"'), desc.replace('"','\\"'), DOMAIN, DOMAIN)
    # splice the webpage node into the @graph if present, else wrap.
    if '"@graph":[' in jsonld:
        jsonld_full = jsonld.replace('"@graph":[', '"@graph":[' + webpage_ld + ',', 1)
    else:
        jsonld_full = jsonld
    head = ('<!doctype html><html lang="en-AU"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
    '<title>%s</title><meta name="description" content="%s">'
    '<meta name="author" content="INFITEX Global Advisory">'
    '<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">'
    '<link rel="canonical" href="%s">'
    '<!-- SEO/GEO verification scaffold — replace PLACEHOLDER tokens after deploy --><meta name="google-site-verification" content="GOOGLE_SITE_VERIFICATION"><!-- <meta name="msvalidate.01" content="BING_SITE_VERIFICATION"> --><!-- <meta name="yandex-verification" content="YANDEX_SITE_VERIFICATION"> --><!-- <meta name="p:domain_verify" content="PINTEREST_SITE_VERIFICATION"> -->'
    '<meta property="og:type" content="%s"><meta property="og:site_name" content="INFITEX Global Advisory">'
    '<meta property="og:title" content="%s"><meta property="og:description" content="%s">'
    '<meta property="og:url" content="%s"><meta property="og:image" content="%s/og-image.png">'
    '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
    '<meta property="og:image:alt" content="INFITEX Global Advisory — white-label accounting outsourcing for Australian practices">'
    '<meta property="og:locale" content="en_AU">'
    '<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="%s">'
    '<meta name="twitter:description" content="%s"><meta name="twitter:image" content="%s/og-image.png">'
    '<meta name="twitter:image:alt" content="INFITEX Global Advisory">'
    '<meta name="theme-color" content="#F7F6F1" media="(prefers-color-scheme: light)"><meta name="theme-color" content="#14211C" media="(prefers-color-scheme: dark)">'
    '<link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="favicon.svg">'
    '<link rel="sitemap" type="application/xml" title="Sitemap" href="sitemap.xml">'
    +NOFLASH+FONTS+
    ('<link rel="stylesheet" href="styles.css%s">' % (("?v="+CSS_VER) if CSS_VER else ""))+
    '<script type="application/ld+json">%s</script>'
    '</head><body>') % (title,desc,canon,og_type,title,desc,canon,DOMAIN,title,desc,DOMAIN,jsonld_full)
    tail = (dialogs()+search_overlay()+fabs()+footer()+SEARCH_INDEX_JS+('<script src="app.js%s" defer></script></body></html>' % (("?v="+JS_VER) if JS_VER else "")))
    return head + header(filename) + '<main id="main">' + body + '</main>' + tail

# ----------------------------- ORG JSON-LD (shared) -----------------------------
# Entity-dense Organization node: AI search engines (ChatGPT, Gemini, Perplexity)
# index on knowsAbout/serviceType/areaServed/contactPoint, so these are spelled out.
ORG_LD = ('{"@context":"https://schema.org","@type":"ProfessionalService","@id":"%s/#organization",'
'"name":"INFITEX Global Advisory","alternateName":"INFITEX",'
'"slogan":"A finance team that works to your standards.",'
'"description":"INFITEX Global Advisory is an India-based, white-label accounting and bookkeeping outsourcing partner for Australian accounting practices and businesses, covering bookkeeping, payroll and STP, BAS and IAS, year-end financials, tax and SMSF, plus management reporting and Virtual CFO. The client practice always retains lodgement and sign-off. A Digitech division provides websites, business email and SEO.",'
'"url":"%s/","logo":"%s/logo.svg","image":"%s/og-image.png","email":"info@infitexglobal.com",'
'"telephone":"+91-8500-850-526","priceRange":"Contact for a tailored quote","currenciesAccepted":"AUD",'
'"areaServed":{"@type":"Country","name":"Australia"},'
'"knowsLanguage":["en-AU","en"],"availableLanguage":["English"],'
'"knowsAbout":["White-label accounting outsourcing","Bookkeeping","Bank reconciliations",'
'"Accounts payable and receivable","Payroll","Single Touch Payroll (STP)","BAS preparation","IAS preparation",'
'"Year-end financial statements","Company and trust tax returns","SMSF accounting","BGL","Class",'
'"Xero","XPM","MYOB","QuickBooks","Reckon","Karbon","Dext","Hubdoc","FYI Docs",'
'"Management reporting","Budgeting and forecasting","Cash-flow forecasting","Virtual CFO","Australian tax compliance"],'
'"serviceType":["Accounting outsourcing","Bookkeeping outsourcing","Payroll outsourcing",'
'"BAS and IAS preparation","Virtual CFO","Management reporting","Web design and SEO (Digitech)"],'
'"contactPoint":{"@type":"ContactPoint","contactType":"sales","email":"info@infitexglobal.com",'
'"telephone":"+91-8500-850-526","areaServed":"AU","availableLanguage":["en-AU","en"]},'
'"address":{"@type":"PostalAddress","addressCountry":"IN"},'
'"sameAs":["https://www.linkedin.com/company/infitexglobal","https://www.facebook.com/infitexglobal",'
'"https://www.instagram.com/infitexglobal","https://x.com/infitexglobal","https://www.youtube.com/@infitexglobal"]}') % (DOMAIN,DOMAIN,DOMAIN,DOMAIN)

def breadcrumb(items):
    el=",".join('{"@type":"ListItem","position":%d,"name":"%s","item":"%s/%s"}'%(i+1,n,DOMAIN,u) for i,(n,u) in enumerate(items))
    return '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[%s]}'%el

print("partials ready")
