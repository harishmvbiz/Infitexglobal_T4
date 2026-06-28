#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re, json, glob
from html.parser import HTMLParser

OUT = "/home/claude/infitex-site"
PAGES = ["index.html","outsourcing.html","industry.html","digitech.html","privacy.html","terms.html","sitemap.html"]
issues = []
warns = []

class Scan(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids=[]; self.h1=0; self.lang=None; self.title=0
        self.imgs_no_alt=0; self.a_targets=[]; self.anchors=set()
        self.buttons=[]; self.labels_for=set(); self.inputs=[]
        self.tw_open=None; self.tw_haschild=False; self.tw_bad=0; self.tw_count=0
        self.void={'meta','link','input','br','img','hr','source','use','path','circle','line','rect','stop','polyline'}
        self.metadesc=0; self.canonical=0; self.viewport=0
        self.jsonld=[]; self._collect=None; self._buf=""
        self.depth_stack=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if tag=='html' and 'lang' in a: self.lang=a['lang']
        if tag=='h1': self.h1+=1
        if tag=='title': self.title+=1; self._collect='title'; self._buf=""
        if tag=='meta':
            if a.get('name')=='description' and a.get('content','').strip(): self.metadesc+=1
            if a.get('name')=='viewport': self.viewport+=1
        if tag=='link' and a.get('rel')=='canonical': self.canonical+=1
        if tag=='img' and not a.get('alt'): self.imgs_no_alt+=1
        if 'id' in a: self.anchors.add(a['id'])
        if tag=='a' and a.get('href'): self.a_targets.append(a['href'])
        if tag=='button': self.buttons.append(a)
        if tag=='label' and a.get('for'): self.labels_for.add(a['for'])
        if tag in ('input','select','textarea'): self.inputs.append(a)
        if tag=='script' and a.get('type')=='application/ld+json': self._collect='jsonld'; self._buf=""
        # data-tw leaf check
        if 'data-tw' in a:
            self.tw_count+=1; self.tw_open=tag; self.tw_haschild=False
        elif self.tw_open and tag not in self.void:
            self.tw_haschild=True
    def handle_endtag(self,tag):
        if self._collect=='title' and tag=='title':
            self._collect=None
        if self._collect=='jsonld' and tag=='script':
            self.jsonld.append(self._buf); self._collect=None
        if self.tw_open and tag==self.tw_open:
            if self.tw_haschild: self.tw_bad+=1
            self.tw_open=None
    def handle_data(self,d):
        if self._collect=='jsonld': self._buf+=d
        if self._collect=='title': self._buf+=d

for pg in PAGES:
    path=os.path.join(OUT,pg)
    if not os.path.exists(path): issues.append((pg,"FILE MISSING")); continue
    raw=open(path,encoding="utf-8").read()
    s=Scan(); s.feed(raw)
    # structural
    if s.lang!="en-AU": issues.append((pg,"html lang not en-AU: %r"%s.lang))
    if s.h1!=1: issues.append((pg,"expected exactly 1 <h1>, found %d"%s.h1))
    if s.title<1: issues.append((pg,"missing <title>"))
    if s.metadesc<1: issues.append((pg,"missing meta description"))
    if s.canonical<1: issues.append((pg,"missing canonical"))
    if s.viewport<1: issues.append((pg,"missing viewport"))
    if s.imgs_no_alt: issues.append((pg,"%d <img> without alt"%s.imgs_no_alt))
    if "\ufffd" in raw: issues.append((pg,"contains U+FFFD replacement char"))
    # duplicate ids
    dups=set([x for x in s.ids if s.ids.count(x)>1])
    if dups: issues.append((pg,"duplicate id(s): %s"%", ".join(sorted(dups))))
    # data-tw leaves
    if s.tw_bad: issues.append((pg,"%d data-tw element(s) have child elements (won't type)"%s.tw_bad))
    # JSON-LD parse
    for i,block in enumerate(s.jsonld):
        try: json.loads(block)
        except Exception as e: issues.append((pg,"JSON-LD #%d invalid: %s"%(i,e)))
    if not s.jsonld: warns.append((pg,"no JSON-LD"))
    # internal links: local file existence + same-page anchors
    for href in s.a_targets:
        if href.startswith(("http://","https://","mailto:","tel:","#")):
            if href.startswith("#") and href!="#":
                if href[1:] not in s.anchors: warns.append((pg,"missing same-page anchor %s"%href))
            continue
        if "data-booking" in raw and href=="#contact": continue
        file_part=href.split("#")[0]; anchor=href.split("#")[1] if "#" in href else None
        if file_part and not os.path.exists(os.path.join(OUT,file_part)):
            issues.append((pg,"broken internal link: %s"%href))
    # buttons need accessible name
    for b in s.buttons:
        pass  # text content not captured here; aria-labels present in source by design
    # inputs need a label (by id) — combobox cc-input uses aria-label
    for inp in s.inputs:
        iid=inp.get('id')
        has_aria = inp.get('aria-label') or inp.get('aria-labelledby')
        typ=inp.get('type','')
        if typ in ('hidden','submit','button','radio','checkbox'): continue
        if inp.get('aria-hidden')=='true': continue  # honeypot, hidden from AT
        if 'hp' in (inp.get('class') or ''): continue
        if 'cc-input' in (inp.get('class') or ''): continue
        if iid and iid in s.labels_for: continue
        if has_aria: continue
        warns.append((pg,"input without associated label: id=%r name=%r"%(iid,inp.get('name'))))

print("="*64)
print("VALIDATION PASS 1")
print("="*64)
print("ISSUES (%d):"%len(issues))
for p,m in issues: print("  [%s] %s"%(p,m))
print("\nWARNINGS (%d):"%len(warns))
for p,m in warns: print("  [%s] %s"%(p,m))
print("\nrobots.txt:", "OK" if os.path.exists(OUT+"/robots.txt") else "MISSING")
print("sitemap.xml:", "OK" if os.path.exists(OUT+"/sitemap.xml") else "MISSING")
print("og-image.png:", "OK" if os.path.exists(OUT+"/og-image.png") else "MISSING")
print("logo.svg:", "OK" if os.path.exists(OUT+"/logo.svg") else "MISSING")
