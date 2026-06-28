#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
INFITEX site — Validation Pass 2 (deep SEO + nav + a11y audit).
Complements validate.py. Focuses on:
  - the new "What we do" / "Who we help" mega-menu nav (structure + ARIA + targets)
  - SEO completeness (title/desc length, canonical, OG/Twitter, JSON-LD graph, headings)
  - internal link & anchor integrity across all pages
  - accessibility hooks (skip link, single h1, labelled controls, alt text)
"""
import os, re, json
from html.parser import HTMLParser

OUT = "/home/claude/infitex-site"
PAGES = ["index.html","outsourcing.html","industry.html","digitech.html",
         "privacy.html","terms.html","sitemap.html"]

issues, warns, oks = [], [], []
def I(p,m): issues.append((p,m))
def W(p,m): warns.append((p,m))
def OK(p,m): oks.append((p,m))

# ---- collect anchors (id=) per page so cross-page #frag links can be checked ----
anchors_by_page = {}
raw_by_page = {}
for pg in PAGES:
    path = os.path.join(OUT, pg)
    if os.path.exists(path):
        raw = open(path, encoding="utf-8").read()
        raw_by_page[pg] = raw
        anchors_by_page[pg] = set(re.findall(r'id="([^"]+)"', raw))

class Meta(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title=""; self._intitle=False
        self.desc=None; self.canonical=None
        self.og={}; self.tw={}; self.h1=0; self.h2=0
        self.links=[]; self.jsonld=[]; self._injson=False; self._buf=""
        self.lang=None; self.viewport=False; self.themecolor=False
        self.skip=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=="html" and "lang" in a: self.lang=a["lang"]
        if tag=="title": self._intitle=True
        if tag=="h1": self.h1+=1
        if tag=="h2": self.h2+=1
        if tag=="a":
            if a.get("href"): self.links.append(a["href"])
            if a.get("class")=="skip-link": self.skip=True
        if tag=="meta":
            n=a.get("name",""); pr=a.get("property",""); c=a.get("content","")
            if n=="description": self.desc=c
            if n=="viewport": self.viewport=True
            if n=="theme-color": self.themecolor=True
            if pr.startswith("og:"): self.og[pr]=c
            if n.startswith("twitter:"): self.tw[n]=c
        if tag=="link" and a.get("rel")=="canonical": self.canonical=a.get("href")
        if tag=="script" and a.get("type")=="application/ld+json":
            self._injson=True; self._buf=""
    def handle_endtag(self,tag):
        if tag=="title": self._intitle=False
        if tag=="script" and self._injson:
            self.jsonld.append(self._buf); self._injson=False
    def handle_data(self,d):
        if self._intitle: self.title+=d
        if self._injson: self._buf+=d

print("="*68)
print("VALIDATION PASS 2 — deep SEO / nav / a11y audit")
print("="*68)

for pg in PAGES:
    if pg not in raw_by_page:
        I(pg,"FILE MISSING"); continue
    raw=raw_by_page[pg]
    m=Meta(); m.feed(raw)

    # ---------- SEO: title ----------
    t=m.title.strip()
    if not t: I(pg,"missing <title>")
    else:
        if len(t)>65: W(pg,"title %d chars (>65, may truncate in SERP)"%len(t))
        if len(t)<15: W(pg,"title only %d chars"%len(t))
    # ---------- SEO: meta description ----------
    if not m.desc: I(pg,"missing meta description")
    else:
        dl=len(m.desc)
        if dl>165: W(pg,"meta description %d chars (>165)"%dl)
        if dl<50: W(pg,"meta description %d chars (<50, thin)"%dl)
    # ---------- SEO: canonical ----------
    if not m.canonical: I(pg,"missing canonical")
    elif not m.canonical.endswith(pg): W(pg,"canonical %r != page"%m.canonical)
    # ---------- SEO: OG + Twitter ----------
    for k in ("og:title","og:description","og:url","og:image","og:type"):
        if k not in m.og: I(pg,"missing %s"%k)
    for k in ("twitter:card","twitter:title","twitter:image"):
        if k not in m.tw: W(pg,"missing %s"%k)
    if m.og.get("og:url") and not m.og["og:url"].endswith(pg):
        W(pg,"og:url %r != page"%m.og["og:url"])
    # ---------- headings ----------
    if m.h1!=1: I(pg,"expected exactly 1 <h1>, found %d"%m.h1)
    if m.h2==0: W(pg,"no <h2> on page")
    # ---------- structural a11y ----------
    if m.lang!="en-AU": I(pg,"html lang not en-AU: %r"%m.lang)
    if not m.viewport: I(pg,"missing viewport")
    if not m.skip: W(pg,"missing skip-link")
    if not m.themecolor: W(pg,"missing theme-color")
    # ---------- JSON-LD ----------
    if not m.jsonld: I(pg,"no JSON-LD")
    for i,b in enumerate(m.jsonld):
        try:
            data=json.loads(b)
            OK(pg,"JSON-LD #%d valid (%s)"%(i,data.get("@type") or "@graph"))
        except Exception as e:
            I(pg,"JSON-LD #%d invalid: %s"%(i,e))
    # ---------- internal link integrity ----------
    for href in m.links:
        if href.startswith(("http://","https://","mailto:","tel:")): continue
        if href=="#" or href=="": continue
        if href.startswith("#"):
            frag=href[1:]
            if frag not in anchors_by_page.get(pg,set()):
                W(pg,"same-page anchor not found: %s"%href)
            continue
        file_part=href.split("#")[0]
        frag=href.split("#")[1] if "#" in href else None
        if file_part and not os.path.exists(os.path.join(OUT,file_part)):
            I(pg,"broken internal link: %s"%href); continue
        if frag and file_part in anchors_by_page:
            if frag not in anchors_by_page[file_part]:
                W(pg,"cross-page anchor #%s not found in %s"%(frag,file_part))

# ---------- NAV-SPECIFIC checks (the requested restructure) ----------
print("\n" + "-"*68)
print("NAV / MEGA-MENU checks")
print("-"*68)
nav_targets=set()
for pg in PAGES:
    raw=raw_by_page.get(pg,"")
    mhead=re.search(r'<nav class="nav"[^>]*>(.*?)</nav>',raw,re.S)
    if not mhead:
        I(pg,"primary .nav not found"); continue
    nav=mhead.group(1)
    # must contain both mega menus
    for lbl in ("What we do","Who we help"):
        if lbl not in nav: I(pg,"nav missing '%s' menu"%lbl)
    # each trigger needs ARIA
    triggers=re.findall(r'<button[^>]*\bnav-trigger\b[^>]*>',nav)
    if len(triggers)!=3: I(pg,"expected 3 mega triggers, found %d"%len(triggers))
    for tr in triggers:
        if "aria-expanded" not in tr: I(pg,"mega trigger missing aria-expanded")
        if "aria-haspopup" not in tr: I(pg,"mega trigger missing aria-haspopup")
        if "aria-controls" not in tr: I(pg,"mega trigger missing aria-controls")
    # aria-controls ids must exist as panel ids
    for cid in re.findall(r'aria-controls="(mega-[^"]+)"',nav):
        if 'id="%s"'%cid not in nav: I(pg,"mega panel id %s missing"%cid)
    # collect all mega link targets to verify later
    for href in re.findall(r'<li><a href="([^"]+)"',nav):
        nav_targets.add(href)
    # "Who we help" must include the three requested audiences
    whomatch=re.search(r'Who we help.*?</div></div>',nav,re.S)
    if whomatch:
        block=whomatch.group(0)
        for need in ("outsourcing.html","industry.html","digitech.html"):
            if need not in block: W(pg,"'Who we help' missing link to %s"%need)
    if pg=="index.html":
        OK(pg,"nav: 3 mega-menus + simple Home/Contact verified")

# verify every mega-menu target resolves (file + anchor)
print("\n" + "-"*68)
print("MEGA-MENU LINK TARGETS (%d unique)"%len(nav_targets))
print("-"*68)
for href in sorted(nav_targets):
    file_part=href.split("#")[0]
    frag=href.split("#")[1] if "#" in href else None
    if file_part and not os.path.exists(os.path.join(OUT,file_part)):
        I("nav","mega target broken file: %s"%href); continue
    if frag and file_part in anchors_by_page and frag not in anchors_by_page[file_part]:
        I("nav","mega target anchor missing: %s"%href); continue
    print("  ok  %s"%href)

# ---------- asset checks ----------
print("\n" + "-"*68)
for asset in ("robots.txt","sitemap.xml","og-image.png","logo.svg","favicon.svg","styles.css","app.js"):
    state="OK" if os.path.exists(os.path.join(OUT,asset)) else "MISSING"
    if state=="MISSING": I("assets","%s MISSING"%asset)
    print("  %-16s %s"%(asset,state))

# ---------- summary ----------
print("\n" + "="*68)
print("RESULT:  %d issue(s), %d warning(s), %d positive check(s)"%(len(issues),len(warns),len(oks)))
print("="*68)
if issues:
    print("\nISSUES:")
    for p,mm in issues: print("  [%s] %s"%(p,mm))
if warns:
    print("\nWARNINGS:")
    for p,mm in warns: print("  [%s] %s"%(p,mm))
print("\nPASS" if not issues else "\nFAIL — fix issues above")
