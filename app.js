/* =========================================================================
   INFITEX Global Advisory — app.js  (vanilla, no dependencies)
   ========================================================================= */
(function(){
  "use strict";

  /* ---------- EDITABLE CONFIG (see INTEGRATION_GUIDE.md) ---------- */
  var CONFIG = {
    whatsapp: "918500850526",                 // WHATSAPP_NUMBER digits only, country code first
    email: "info@infitexglobal.com",
    bookingLink: "https://calendar.app.google/EJbx9HqLDzSr5vqW7",  // Google appointment / booking link for "Book a call"
    web3formsKey: "348d4025-f324-4e35-9b3f-b7a13bc62f09",
    domain: "https://infitexglobal.com"
  };
  window.INFITEX_CONFIG = CONFIG;

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $  = function(s,c){return (c||document).querySelector(s);};
  var $$ = function(s,c){return Array.prototype.slice.call((c||document).querySelectorAll(s));};

  /* =======================================================================
     THEME + ACCESSIBILITY (persisted)
     ===================================================================== */
  var root = document.documentElement;
  function store(k,v){try{localStorage.setItem(k,v);}catch(e){}}
  function recall(k){try{return localStorage.getItem(k);}catch(e){return null;}}

  function applyTheme(t){ root.setAttribute("data-theme",t); store("ix-theme",t); updateThemeButtons(t); }
  function updateThemeButtons(t){
    $$("[data-theme-toggle]").forEach(function(b){
      b.setAttribute("aria-pressed", t==="light" ? "true":"false");
      var lbl=b.querySelector("[data-theme-label]"); if(lbl) lbl.textContent = t==="light"?"Light":"Dark";
    });
  }
  function toggleTheme(){ applyTheme(root.getAttribute("data-theme")==="light"?"dark":"light"); }

  // text size
  var TEXT_STEPS=[-2,0,2,4,6], textIdx=1;
  (function(){ var s=recall("ix-textstep"); if(s!==null){ textIdx=parseInt(s,10)||1; setText(textIdx,true);} })();
  function setText(i,silent){ textIdx=Math.max(0,Math.min(TEXT_STEPS.length-1,i));
    root.style.setProperty("--type-scale-step", TEXT_STEPS[textIdx]+"px"); if(!silent) store("ix-textstep",textIdx); }

  function applyContrast(v){ if(v==="high") root.setAttribute("data-contrast","high"); else root.removeAttribute("data-contrast"); store("ix-contrast",v); syncToggle("[data-contrast-toggle]", v==="high"); }
  function applyGray(v){ if(v==="on") root.setAttribute("data-grayscale","on"); else root.removeAttribute("data-grayscale"); store("ix-grayscale",v); syncToggle("[data-gray-toggle]", v==="on"); }
  function syncToggle(sel,on){ $$(sel).forEach(function(b){ b.setAttribute("aria-pressed", on?"true":"false"); }); }

  // restore on load
  (function(){
    var c=recall("ix-contrast"); if(c) applyContrast(c);
    var g=recall("ix-grayscale"); if(g) applyGray(g);
    updateThemeButtons(root.getAttribute("data-theme")||"dark");
  })();

  document.addEventListener("click",function(e){
    var t=e.target.closest("[data-theme-toggle]"); if(t){ toggleTheme(); }
    var c=e.target.closest("[data-contrast-toggle]"); if(c){ applyContrast(root.getAttribute("data-contrast")==="high"?"off":"high"); }
    var g=e.target.closest("[data-gray-toggle]"); if(g){ applyGray(root.getAttribute("data-grayscale")==="on"?"off":"on"); }
    var ti=e.target.closest("[data-text='inc']"); if(ti) setText(textIdx+1);
    var td=e.target.closest("[data-text='dec']"); if(td) setText(textIdx-1);
    var tr=e.target.closest("[data-text='reset']"); if(tr) setText(1);
  });

  /* a11y dialog */
  var a11yDialog=$("#a11yDialog");
  $$("[data-open-a11y]").forEach(function(b){ b.addEventListener("click",function(){ if(a11yDialog&&a11yDialog.showModal) a11yDialog.showModal(); }); });
  if(a11yDialog){ a11yDialog.addEventListener("click",function(e){ if(e.target.closest("[data-close]")) a11yDialog.close(); }); }

  /* =======================================================================
     MOBILE NAV
     ===================================================================== */
  var mnav=$("#mobileNav");
  $$("[data-open-nav]").forEach(function(b){ b.addEventListener("click",function(){ if(mnav){mnav.classList.add("open"); mnav.setAttribute("aria-hidden","false");} }); });
  if(mnav){
    mnav.addEventListener("click",function(e){ if(e.target.closest("[data-close-nav]")||e.target.tagName==="A"){ mnav.classList.remove("open"); mnav.setAttribute("aria-hidden","true"); } });
  }
  document.addEventListener("keydown",function(e){ if(e.key==="Escape"&&mnav&&mnav.classList.contains("open")){ mnav.classList.remove("open"); } });

  /* =======================================================================
     DESKTOP MEGA-MENU  (hover via CSS; click + keyboard via JS)
     ===================================================================== */
  var megaItems=$$(".nav-item.has-mega");
  function closeAllMega(except){
    megaItems.forEach(function(it){
      if(it===except) return;
      it.classList.remove("open");
      var t=it.querySelector(".nav-trigger");
      if(t) t.setAttribute("aria-expanded","false");
    });
  }
  megaItems.forEach(function(it){
    var trigger=it.querySelector(".nav-trigger");
    if(!trigger) return;
    trigger.addEventListener("click",function(e){
      e.preventDefault();
      var isOpen=it.classList.contains("open");
      closeAllMega(it);
      if(isOpen){ it.classList.remove("open"); trigger.setAttribute("aria-expanded","false"); }
      else { it.classList.add("open"); trigger.setAttribute("aria-expanded","true"); }
    });
    // close when focus leaves the whole item (keyboard tab-out)
    it.addEventListener("focusout",function(e){
      if(!it.contains(e.relatedTarget)){ it.classList.remove("open"); trigger.setAttribute("aria-expanded","false"); }
    });
  });
  // click outside closes any open mega panel
  document.addEventListener("click",function(e){
    if(!e.target.closest(".nav-item.has-mega")) closeAllMega(null);
  });
  // Escape closes mega panels and returns focus to the trigger
  document.addEventListener("keydown",function(e){
    if(e.key==="Escape"){
      megaItems.forEach(function(it){
        if(it.classList.contains("open")){
          it.classList.remove("open");
          var t=it.querySelector(".nav-trigger");
          if(t){ t.setAttribute("aria-expanded","false"); t.focus(); }
        }
      });
    }
  });

  /* =======================================================================
     MOBILE NAV ACCORDION
     ===================================================================== */
  $$(".m-acc-btn").forEach(function(btn){
    btn.addEventListener("click",function(){
      var panel=document.getElementById(btn.getAttribute("aria-controls"));
      var open=btn.getAttribute("aria-expanded")==="true";
      btn.setAttribute("aria-expanded", open?"false":"true");
      if(panel) panel.classList.toggle("open", !open);
    });
  });

  /* =======================================================================
     SCROLL REVEAL + TYPEWRITER-ON-SCROLL
     ===================================================================== */
  (function(){
    var rev=$$(".reveal");
    if(!rev.length) return;
    if(reduceMotion){ rev.forEach(function(el){el.classList.add("in");}); return; }
    var io=new IntersectionObserver(function(en){ en.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add("in"); io.unobserve(e.target);} }); },{threshold:.12});
    rev.forEach(function(el){ io.observe(el); });
  })();

  /* Static text: the scroll-triggered typewriter has been disabled by request.
     All [data-tw] copy now renders in full immediately (no per-character animation). */
  (function(){ /* intentionally a no-op — headings and leads stay static */ })();

  function typeOut(holder, text){
    if(!holder) return;
    var caret=document.createElement("span"); caret.className="tw-caret";
    holder.appendChild(caret);
    var i=0, speed=text.length>46?13:24;
    (function step(){
      if(i<text.length){
        caret.insertAdjacentText("beforebegin", text.charAt(i)); i++;
        setTimeout(step, speed + Math.random()*26);
      } else { setTimeout(function(){ if(caret.parentNode) caret.remove(); }, 1100); }
    })();
  }

  /* hero console typing */
  (function(){
    var box=$("#heroConsole"); if(!box) return;
    var lines=[
      {t:"$ ", k:"infitex ", x:"prepare --practice=yours", cls:""},
      {t:"› bookkeeping ", ok:"reconciled", cls:""},
      {t:"› BAS / IAS ", ok:"drafted", cls:""},
      {t:"› payroll + STP ", ok:"processed", cls:""},
      {t:"› maker → checker ", ok:"passed", cls:""},
      {t:"› handover to practice for ", cy:"lodgement & sign-off", cls:""}
    ];
    if(reduceMotion || !("IntersectionObserver" in window)){
      box.innerHTML=lines.map(function(l){
        return '<span class="cl"><span class="pr">'+esc(l.t)+'</span>'+(l.k?'<span class="ok">'+esc(l.k)+'</span>':'')+
          (l.x?esc(l.x):'')+(l.ok?'<span class="ok">'+esc(l.ok)+'</span>':'')+(l.cy?'<span class="cy">'+esc(l.cy)+'</span>':'')+'</span>';
      }).join("")+'<span class="caret"></span>';
      return;
    }
    var li=0;
    function nextLine(){
      if(li>=lines.length){ box.insertAdjacentHTML("beforeend",'<span class="caret"></span>'); return; }
      var l=lines[li++], el=document.createElement("span"); el.className="cl"; box.appendChild(el);
      var seq=[];
      if(l.t) seq.push(["pr",l.t]);
      if(l.k) seq.push(["ok",l.k]);
      if(l.x) seq.push(["",l.x]);
      if(l.ok) seq.push(["ok",l.ok]);
      if(l.cy) seq.push(["cy",l.cy]);
      typeSeq(el,seq,0,0,function(){ setTimeout(nextLine, 130); });
    }
    function typeSeq(parent,seq,si,ci,done){
      if(si>=seq.length){ done(); return; }
      var cls=seq[si][0], str=seq[si][1];
      var span=parent.querySelector('[data-i="'+si+'"]');
      if(!span){ span=document.createElement("span"); if(cls) span.className=cls; span.setAttribute("data-i",si); parent.appendChild(span); }
      if(ci<str.length){ span.textContent+=str.charAt(ci); setTimeout(function(){typeSeq(parent,seq,si,ci+1,done);}, 16+Math.random()*22); }
      else { typeSeq(parent,seq,si+1,0,done); }
    }
    var started=false;
    var io=new IntersectionObserver(function(en){ en.forEach(function(e){ if(e.isIntersecting&&!started){started=true; nextLine(); io.disconnect();} }); },{threshold:.3});
    io.observe(box);
  })();
  function esc(s){ return (s||"").replace(/[&<>]/g,function(m){return {"&":"&amp;","<":"&lt;",">":"&gt;"}[m];}); }

  /* =======================================================================
     SECTION NAVIGATOR active state
     ===================================================================== */
  (function(){
    var navLinks=$$(".section-nav a"); if(!navLinks.length) return;
    var map={};
    navLinks.forEach(function(a){ var id=a.getAttribute("href").split("#")[1]; if(id){ var s=document.getElementById(id); if(s) map[id]=a; } });
    var io=new IntersectionObserver(function(en){
      en.forEach(function(e){ if(e.isIntersecting){ navLinks.forEach(function(a){a.classList.remove("active");}); if(map[e.target.id]) map[e.target.id].classList.add("active"); } });
    },{rootMargin:"-40% 0px -55% 0px"});
    Object.keys(map).forEach(function(id){ io.observe(document.getElementById(id)); });
  })();

  /* =======================================================================
     COUNTRY-CODE COMBOBOX  (face shows only the dial code)
     ===================================================================== */
  var COUNTRIES=[
    ["+61","Australia"],["+91","India"],["+64","New Zealand"],["+1","United States"],["+1","Canada"],
    ["+44","United Kingdom"],["+353","Ireland"],["+65","Singapore"],["+60","Malaysia"],["+62","Indonesia"],
    ["+63","Philippines"],["+852","Hong Kong"],["+971","United Arab Emirates"],["+966","Saudi Arabia"],["+974","Qatar"],
    ["+27","South Africa"],["+49","Germany"],["+33","France"],["+34","Spain"],["+39","Italy"],["+31","Netherlands"],
    ["+41","Switzerland"],["+46","Sweden"],["+47","Norway"],["+45","Denmark"],["+351","Portugal"],["+48","Poland"],
    ["+81","Japan"],["+82","South Korea"],["+86","China"],["+66","Thailand"],["+84","Vietnam"],["+880","Bangladesh"],
    ["+94","Sri Lanka"],["+92","Pakistan"],["+977","Nepal"],["+55","Brazil"],["+52","Mexico"],["+54","Argentina"],
    ["+20","Egypt"],["+254","Kenya"],["+234","Nigeria"],["+90","Turkey"],["+7","Russia"],["+972","Israel"]
  ];
  function initCombo(combo){
    var input=combo.querySelector(".cc-input");
    var list=combo.querySelector(".cc-list");
    var active=-1, filtered=COUNTRIES.slice();
    function render(){
      list.innerHTML="";
      filtered.forEach(function(c,idx){
        var o=document.createElement("div");
        o.className="cc-opt"; o.setAttribute("role","option"); o.setAttribute("data-code",c[0]);
        o.setAttribute("aria-selected", idx===active?"true":"false");
        o.innerHTML='<span class="code">'+c[0]+'</span><span class="cn">'+c[1]+'</span>';
        o.addEventListener("mousedown",function(ev){ ev.preventDefault(); choose(c[0]); });
        list.appendChild(o);
      });
    }
    function open(){ list.classList.add("open"); render(); }
    function close(){ list.classList.remove("open"); active=-1; }
    function choose(code){ input.value=code; close(); input.dispatchEvent(new Event("change")); }
    function filter(){
      var q=input.value.trim().toLowerCase().replace(/^\+/,"");
      filtered=COUNTRIES.filter(function(c){
        return c[0].replace("+","").indexOf(q)===0 || c[1].toLowerCase().indexOf(q)>-1 || q==="";
      });
      active=-1; open();
    }
    input.addEventListener("focus",open);
    input.addEventListener("input",filter);
    input.addEventListener("keydown",function(e){
      var opts=list.querySelectorAll(".cc-opt");
      if(e.key==="ArrowDown"){ e.preventDefault(); active=Math.min(opts.length-1,active+1); markActive(opts); }
      else if(e.key==="ArrowUp"){ e.preventDefault(); active=Math.max(0,active-1); markActive(opts); }
      else if(e.key==="Enter"){ if(active>-1&&opts[active]){ e.preventDefault(); choose(opts[active].getAttribute("data-code")); } }
      else if(e.key==="Escape"){ close(); }
    });
    function markActive(opts){ opts.forEach(function(o,i){ o.setAttribute("aria-selected", i===active?"true":"false"); if(i===active) o.scrollIntoView({block:"nearest"}); }); }
    document.addEventListener("click",function(e){ if(!combo.contains(e.target)) close(); });
    input.addEventListener("blur",function(){
      // normalise: ensure it begins with + and digits
      var v=input.value.trim(); if(v && v[0]!=="+") v="+"+v.replace(/[^0-9]/g,""); if(!v) v="+61"; input.value=v.replace(/[^+0-9]/g,"");
      setTimeout(close,120);
    });
    render();
  }
  $$("[data-cc]").forEach(initCombo);

  /* restrict mobile number: digits only, max 10 */
  $$(".tel-num").forEach(function(inp){
    inp.addEventListener("input",function(){
      var v=inp.value.replace(/\D/g,"").slice(0,10);
      if(v!==inp.value) inp.value=v;
    });
    inp.addEventListener("keypress",function(e){
      if(e.key.length===1 && /\D/.test(e.key)) e.preventDefault();
    });
  });

  /* =======================================================================
     VALIDATION + MESSAGE COMPOSITION
     ===================================================================== */
  function validName(v){ return v && v.trim().length>=2 && /[A-Za-z]/.test(v); }
  function validEmail(v){ return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test((v||"").trim()); }
  function validMobile(v){ return /^\d{10}$/.test((v||"").trim()); }

  function setErr(row,on){ if(!row) return; row.classList.toggle("invalid", !!on); }

  function composeMessage(d){
    var enquiry = d.interest && d.interest.trim() ? d.interest : "your services";
    var L=[
      "Hi INFITEX,",
      "",
      "This is "+d.name+" from "+d.business+". I'm enquiring about "+enquiry+".",
      "",
      "My contact details are as follows:",
      "Email: "+d.email,
      "Mobile: "+d.dial+" "+d.mobile
    ];
    if(d.message && d.message.trim()){ L.push("",'Message: '+d.message.trim()); }
    L.push("","Thanks & regards,",d.name,d.business);
    return L.join("\n");
  }
  window.INFITEX_compose = composeMessage;

  function readLeadFields(scope){
    return {
      name:    (val(scope,"[name='name']")||"").trim(),
      business:(val(scope,"[name='company']")||val(scope,"[name='business']")||"").trim(),
      email:   (val(scope,"[name='email']")||"").trim(),
      dial:    (val(scope,".cc-input")||"+61").trim(),
      mobile:  (val(scope,".tel-num")||"").trim(),
      interest:(val(scope,"[name='interest']")||"").trim(),
      message: (val(scope,"[name='message']")||"").trim()
    };
  }
  function val(scope,sel){ var el=scope.querySelector(sel); return el?el.value:""; }

  function validateLead(scope, opts){
    opts=opts||{};
    var ok=true;
    var f={
      name: scope.querySelector("[name='name']"),
      email: scope.querySelector("[name='email']"),
      mobile: scope.querySelector(".tel-num"),
      company: scope.querySelector("[name='company']")||scope.querySelector("[name='business']"),
      message: scope.querySelector("[name='message']")
    };
    function rowOf(el){ return el?el.closest(".form-row"):null; }
    if(f.name){ var v=validName(f.name.value); setErr(rowOf(f.name),!v); ok=ok&&v; }
    if(f.email){ var v2=validEmail(f.email.value); setErr(rowOf(f.email),!v2); ok=ok&&v2; }
    if(f.mobile){ var v3=validMobile(f.mobile.value); setErr(rowOf(f.mobile),!v3); ok=ok&&v3; }
    if(opts.requireCompany && f.company){ var v4=f.company.value.trim().length>=2; setErr(rowOf(f.company),!v4); ok=ok&&v4; }
    if(opts.requireMessage && f.message){ var v5=f.message.value.trim().length>=10; setErr(rowOf(f.message),!v5); ok=ok&&v5; }
    return ok;
  }

  /* =======================================================================
     POPOVERS (WhatsApp + Email)
     ===================================================================== */
  function openDialog(id){ var d=document.getElementById(id); if(d&&d.showModal) d.showModal(); }
  $$("[data-open-wa]").forEach(function(b){ b.addEventListener("click",function(){ openDialog("waDialog"); }); });
  $$("[data-open-mail]").forEach(function(b){ b.addEventListener("click",function(){ openDialog("mailDialog"); }); });
  $$("[data-open-qr]").forEach(function(b){ b.addEventListener("click",function(){ openDialog("qrDialog"); }); });
  $$("dialog [data-close]").forEach(function(b){ b.addEventListener("click",function(){ b.closest("dialog").close(); }); });

  var waForm=$("#waForm");
  if(waForm){
    waForm.addEventListener("submit",function(e){
      e.preventDefault();
      if(waForm.querySelector(".hp") && waForm.querySelector(".hp").value) return;
      if(!validateLead(waForm,{})) return;
      var d=readLeadFields(waForm);
      var msg=composeMessage(d);
      window.open("https://wa.me/"+CONFIG.whatsapp+"?text="+encodeURIComponent(msg),"_blank","noopener");
      var st=$("#waStatus"); if(st){ st.className="form-status ok"; st.textContent="Opening WhatsApp with your enquiry drafted…"; }
    });
  }
  var mailForm=$("#mailForm");
  if(mailForm){
    mailForm.addEventListener("submit",function(e){
      e.preventDefault();
      if(mailForm.querySelector(".hp") && mailForm.querySelector(".hp").value) return;
      if(!validateLead(mailForm,{})) return;
      var d=readLeadFields(mailForm);
      var msg=composeMessage(d);
      var subject="Enquiry from "+(d.business||d.name)+(d.interest?(" — "+d.interest):"");
      window.location.href="mailto:"+CONFIG.email+"?subject="+encodeURIComponent(subject)+"&body="+encodeURIComponent(msg);
      var st=$("#mailStatus"); if(st){ st.className="form-status ok"; st.textContent="Opening your mail app with the enquiry drafted…"; }
    });
  }

  /* =======================================================================
     CONTACT FORM (Web3Forms) + SUBSCRIBE
     ===================================================================== */
  var contactForm=$("#contactForm");
  if(contactForm){
    contactForm.addEventListener("submit",function(e){
      e.preventDefault();
      var st=$("#contactStatus");
      if(contactForm.querySelector(".hp") && contactForm.querySelector(".hp").value) return; // bot
      if(!validateLead(contactForm,{requireCompany:true,requireMessage:true})){ if(st){st.className="form-status err";st.textContent="Please fix the highlighted fields.";} return; }
      var d=readLeadFields(contactForm);
      var composed=composeMessage(d);

      if(!CONFIG.web3formsKey || CONFIG.web3formsKey==="YOUR_WEB3FORMS_ACCESS_KEY"){
        if(st){ st.className="form-status ok"; st.innerHTML="Demo mode — no Web3Forms key set yet. Your enquiry is drafted below. <a href='#' id='waFallback'>Send via WhatsApp</a> or <a href='#' id='mailFallback'>email instead</a>."; }
        wireFallback(d,composed);
        return;
      }
      if(st){ st.className="form-status"; st.textContent="Sending…"; }
      var payload={
        access_key:CONFIG.web3formsKey,
        subject:"New website enquiry — "+(d.business||d.name)+(d.interest?(" ("+d.interest+")"):""),
        from_name:d.name,
        name:d.name, email:d.email, business:d.business,
        mobile:d.dial+" "+d.mobile, interest:d.interest,
        message:composed
      };
      fetch("https://api.web3forms.com/submit",{method:"POST",headers:{"Content-Type":"application/json",Accept:"application/json"},body:JSON.stringify(payload)})
        .then(function(r){return r.json();})
        .then(function(j){
          if(j.success){ if(st){st.className="form-status ok";st.textContent="Thanks "+d.name+" — your enquiry has been sent. We'll reply by email shortly.";} contactForm.reset(); resetCombos(contactForm); }
          else { if(st){st.className="form-status err";st.textContent="Sorry, that didn't send. Please try WhatsApp or email.";} }
        })
        .catch(function(){ if(st){st.className="form-status err";st.textContent="Network issue — please try WhatsApp or email instead.";} });
    });
  }
  function wireFallback(d,composed){
    var w=$("#waFallback"), m=$("#mailFallback");
    if(w) w.addEventListener("click",function(e){e.preventDefault(); window.open("https://wa.me/"+CONFIG.whatsapp+"?text="+encodeURIComponent(composed),"_blank","noopener");});
    if(m) m.addEventListener("click",function(e){e.preventDefault(); window.location.href="mailto:"+CONFIG.email+"?subject="+encodeURIComponent("Enquiry from "+(d.business||d.name))+"&body="+encodeURIComponent(composed);});
  }
  function resetCombos(scope){ $$(".cc-input",scope).forEach(function(i){i.value="+61";}); }

  var subForm=$("#subscribeForm");
  if(subForm){
    subForm.addEventListener("submit",function(e){
      e.preventDefault();
      var st=$("#subStatus");
      var emailEl=subForm.querySelector("[name='email']");
      if(!validEmail(emailEl.value)){ setErr(emailEl.closest(".form-row"),true); if(st){st.className="form-status err";st.textContent="Please enter a valid email address.";} return; }
      setErr(emailEl.closest(".form-row"),false);
      if(!CONFIG.web3formsKey || CONFIG.web3formsKey==="YOUR_WEB3FORMS_ACCESS_KEY"){
        if(st){st.className="form-status ok";st.textContent="Demo mode — subscription captured. Add a Web3Forms key to go live.";}
        subForm.reset(); return;
      }
      fetch("https://api.web3forms.com/submit",{method:"POST",headers:{"Content-Type":"application/json",Accept:"application/json"},
        body:JSON.stringify({access_key:CONFIG.web3formsKey,subject:"New compliance-digest subscriber",email:emailEl.value,message:"Subscribe request — compliance-dates digest — "+emailEl.value})})
        .then(function(r){return r.json();}).then(function(j){
          if(st){ st.className="form-status "+(j.success?"ok":"err"); st.textContent=j.success?("You're subscribed. You can unsubscribe anytime via the link in any email."):"Couldn't subscribe right now — please try again."; }
          if(j.success) subForm.reset();
        }).catch(function(){ if(st){st.className="form-status err";st.textContent="Network issue — please try again.";} });
    });
  }

  /* =======================================================================
     SAVINGS CALCULATOR (indicative only, AUD)
     ===================================================================== */
  (function(){
    var calc=$("#calc"); if(!calc) return;
    var staff=$("#calcStaff"), hours=$("#calcHours"), rate=$("#calcRate");
    var staffV=$("#calcStaffV"), hoursV=$("#calcHoursV"), rateV=$("#calcRateV");
    var outLow=$("#calcLow"), outHigh=$("#calcHigh"), outHrs=$("#calcHrs");
    function fmt(n){ return "$"+Math.round(n).toLocaleString("en-AU"); }
    function update(){
      var s=+staff.value, h=+hours.value, r=+rate.value;
      staffV.textContent=s; hoursV.textContent=h; rateV.textContent="$"+r+"/hr";
      var weeklyHours=s*h, annualHours=weeklyHours*46;          // ~46 working weeks
      var localCost=annualHours*r;
      var low=localCost*0.40, high=localCost*0.60;              // indicative 40–60% saving band
      outHrs.textContent=annualHours.toLocaleString("en-AU")+" hrs/yr";
      outLow.textContent=fmt(low); outHigh.textContent=fmt(high);
    }
    [staff,hours,rate].forEach(function(el){ el.addEventListener("input",update); });
    update();
  })();

  /* =======================================================================
     FAQ SPOTLIGHT CAROUSEL + ACCORDION SYNC
     ===================================================================== */
  (function(){
    var stage=$("#faqStage"); if(!stage) return;
    var slides=$$(".faq-slide",stage);
    var dotsWrap=$("#faqDots"), prog=$("#faqProgress span");
    var idx=0, timer=null, DURATION=6000, hovered=false;
    var dots=slides.map(function(_,i){ var b=document.createElement("button"); b.className="faq-dot"+(i===0?" on":""); b.type="button";
      b.setAttribute("aria-label","Show question "+(i+1)); b.addEventListener("click",function(){ go(i,true); }); dotsWrap.appendChild(b); return b; });
    function show(i){ slides.forEach(function(s,k){ s.classList.toggle("active",k===i); }); dots.forEach(function(d,k){ d.classList.toggle("on",k===i); }); idx=i; }
    function go(i,manual){ show((i+slides.length)%slides.length); if(manual) restart(); }
    function restart(){ if(timer){clearTimeout(timer);} if(reduceMotion||hovered) return; animateProgress(); timer=setTimeout(function(){ go(idx+1); },DURATION); }
    function animateProgress(){ if(!prog) return; prog.style.transition="none"; prog.style.width="0%";
      requestAnimationFrame(function(){ prog.style.transition="width "+DURATION+"ms linear"; prog.style.width="100%"; }); }
    $("#faqPrev").addEventListener("click",function(){ go(idx-1,true); });
    $("#faqNext").addEventListener("click",function(){ go(idx+1,true); });
    stage.addEventListener("mouseenter",function(){ hovered=true; if(timer)clearTimeout(timer); if(prog)prog.style.width=getComputedStyle(prog).width; });
    stage.addEventListener("mouseleave",function(){ hovered=false; restart(); });
    stage.addEventListener("focusin",function(){ hovered=true; if(timer)clearTimeout(timer); });
    stage.addEventListener("focusout",function(){ hovered=false; restart(); });
    show(0); restart();
  })();

  /* =======================================================================
     TESTIMONIALS SLIDER (4 per row, auto-advancing)
     ===================================================================== */
  $$("[data-tslider]").forEach(function(root){
    var vp=$(".tslider-viewport",root), track=$(".tslider-track",root);
    var dotsWrap=$("[data-tdots]",root), prevB=$("[data-tprev]",root), nextB=$("[data-tnext]",root);
    if(!vp||!track||!dotsWrap) return;
    var pages=1, cur=0, timer=null, DUR=5000, hovered=false, st=null, rt=null;
    function pageW(){ return vp.clientWidth||1; }
    function calcPages(){ return Math.max(1, Math.round(track.scrollWidth/pageW())); }
    function goTo(i,manual){ cur=((i%pages)+pages)%pages;
      vp.scrollTo({left:cur*pageW(), behavior:reduceMotion?"auto":"smooth"}); if(manual) restart(); }
    function sync(){ var c=Math.round(vp.scrollLeft/pageW()); if(c>pages-1)c=pages-1; if(c<0)c=0; cur=c;
      Array.prototype.forEach.call(dotsWrap.children,function(d,k){ d.classList.toggle("on",k===cur); }); }
    function buildDots(){ pages=calcPages(); dotsWrap.innerHTML="";
      for(var i=0;i<pages;i++){ (function(i){ var b=document.createElement("button"); b.type="button";
        b.setAttribute("aria-label","Show reviews "+(i+1)); b.addEventListener("click",function(){ goTo(i,true); });
        dotsWrap.appendChild(b); })(i); } sync(); }
    function restart(){ if(timer)clearTimeout(timer); if(reduceMotion||hovered||pages<2) return; timer=setTimeout(function(){ goTo(cur+1); },DUR); }
    if(prevB) prevB.addEventListener("click",function(){ goTo(cur-1,true); });
    if(nextB) nextB.addEventListener("click",function(){ goTo(cur+1,true); });
    vp.addEventListener("scroll",function(){ clearTimeout(st); st=setTimeout(function(){ sync(); restart(); },120); });
    root.addEventListener("mouseenter",function(){ hovered=true; if(timer)clearTimeout(timer); });
    root.addEventListener("mouseleave",function(){ hovered=false; restart(); });
    root.addEventListener("focusin",function(){ hovered=true; if(timer)clearTimeout(timer); });
    root.addEventListener("focusout",function(){ hovered=false; restart(); });
    window.addEventListener("resize",function(){ clearTimeout(rt); rt=setTimeout(buildDots,200); });
    buildDots(); restart();
  });

  /* =======================================================================
     SITE SEARCH
     ===================================================================== */
  var SEARCH_INDEX=window.INFITEX_SEARCH||[];
  (function(){
    var overlay=$("#searchOverlay"); if(!overlay) return;
    var input=$("#searchInput"), results=$("#searchResults");
    var openBtns=$$("[data-open-search]");
    var current=-1, flat=[];

    function open(prefill){ overlay.classList.add("open"); overlay.setAttribute("aria-hidden","false"); input.value=prefill||""; input.focus(); run(input.value); }
    function close(){ overlay.classList.remove("open"); overlay.setAttribute("aria-hidden","true"); }
    openBtns.forEach(function(b){ b.addEventListener("click",function(){ open(); }); });
    overlay.addEventListener("click",function(e){ if(e.target===overlay) close(); });
    document.addEventListener("keydown",function(e){
      if(e.key==="/" && !/INPUT|TEXTAREA|SELECT/.test((e.target.tagName||"")) && !overlay.classList.contains("open")){ e.preventDefault(); open(); }
      if(e.key==="Escape" && overlay.classList.contains("open")){ close(); }
    });

    function esc2(s){ return s.replace(/[.*+?^${}()|[\]\\]/g,"\\$&"); }
    function hl(text,q){ if(!q) return esc(text); try{ return esc(text).replace(new RegExp("("+esc2(q)+")","ig"),"<mark>$1</mark>"); }catch(e){ return esc(text); } }
    function score(item,q){ var t=item.title.toLowerCase(), s=(item.snippet||"").toLowerCase(); q=q.toLowerCase();
      if(t.indexOf(q)===0) return 100; if(t.indexOf(q)>-1) return 70; if(s.indexOf(q)>-1) return 40; return 0; }

    function run(q){
      q=(q||"").trim();
      results.innerHTML=""; flat=[]; current=-1;
      var groups={Pages:[],Sections:[],Services:[],FAQs:[]};
      var items = SEARCH_INDEX.map(function(it){ return {it:it, sc: q? score(it,q): 1}; })
        .filter(function(x){ return x.sc>0; })
        .sort(function(a,b){ return b.sc-a.sc; });
      if(!q){ items=SEARCH_INDEX.map(function(it){return {it:it};}); }
      items.forEach(function(x){ var g=x.it.type; if(groups[g]) groups[g].push(x.it); });
      var any=false;
      ["Pages","Sections","Services","FAQs"].forEach(function(g){
        if(!groups[g].length) return; any=true;
        var lbl=document.createElement("div"); lbl.className="search-group-label"; lbl.textContent=g; results.appendChild(lbl);
        groups[g].forEach(function(it){
          var a=document.createElement("a"); a.className="search-result"; a.href=it.url;
          a.innerHTML='<div class="r-title">'+hl(it.title,q)+'</div>'+(it.snippet?'<div class="r-snip">'+hl(it.snippet,q)+'</div>':'');
          results.appendChild(a); flat.push(a);
        });
      });
      if(!any){ results.innerHTML='<div class="search-empty">No matches for “'+esc(q)+'”. Try “BAS”, “SMSF”, “pilot” or “SEO”.</div>'; }
    }
    var t;
    input.addEventListener("input",function(){ clearTimeout(t); t=setTimeout(function(){ run(input.value); },90); });
    input.addEventListener("keydown",function(e){
      if(e.key==="ArrowDown"){ e.preventDefault(); current=Math.min(flat.length-1,current+1); mark(); }
      else if(e.key==="ArrowUp"){ e.preventDefault(); current=Math.max(0,current-1); mark(); }
      else if(e.key==="Enter"){ if(current>-1&&flat[current]){ window.location.href=flat[current].href; } }
    });
    function mark(){ flat.forEach(function(a,i){ a.classList.toggle("active",i===current); if(i===current) a.scrollIntoView({block:"nearest"}); }); }

    // ?q= deep link
    var params=new URLSearchParams(window.location.search);
    if(params.get("q")){ open(params.get("q")); }
  })();

  /* =======================================================================
     FLOATING: back-to-top
     ===================================================================== */
  (function(){
    var bt=$("#backTop"); if(!bt) return;
    window.addEventListener("scroll",function(){ bt.classList.toggle("show", window.scrollY>600); },{passive:true});
    bt.addEventListener("click",function(){ window.scrollTo({top:0,behavior:reduceMotion?"auto":"smooth"}); });
  })();

  /* year */
  $$("[data-year]").forEach(function(el){ el.textContent=new Date().getFullYear(); });

  /* illustrative growth chart: arm (collapse) then grow when scrolled into view */
  (function(){
    var charts=$$(".chart"); if(!charts.length) return;
    if(reduceMotion || !("IntersectionObserver" in window)) return; // bars already at full height
    charts.forEach(function(c){ c.classList.add("armed"); });
    var io=new IntersectionObserver(function(en){ en.forEach(function(e){
      if(e.isIntersecting){ e.target.classList.add("grow"); io.unobserve(e.target); }
    }); },{threshold:.3});
    charts.forEach(function(c){ io.observe(c); });
  })();

  /* Booking: set any [data-booking] link href from CONFIG (single edit point) */
  (function(){
    var url=CONFIG.bookingLink;
    var live=url && url!=="BOOKING_LINK";
    var contactHref = document.getElementById("contact") ? "#contact" : "index.html#contact";
    $$("[data-booking]").forEach(function(a){
      if(live){ a.setAttribute("href",url); a.setAttribute("target","_blank"); a.setAttribute("rel","noopener"); }
      else { a.setAttribute("href",contactHref); a.title="Add your booking link in app.js CONFIG to enable instant booking."; }
    });
  })();

})();
