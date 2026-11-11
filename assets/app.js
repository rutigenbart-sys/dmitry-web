(function () {
  "use strict";
  var d = document, $ = function (s, r) { return (r || d).querySelector(s); }, $$ = function (s, r) { return Array.prototype.slice.call((r || d).querySelectorAll(s)); };
  var cfg = {};
  try { cfg = JSON.parse($("#cfg").textContent); } catch (e) {}
  var lang = d.documentElement.lang === "en" ? "en" : "ru";

  /* current year everywhere */
  var y = String(new Date().getFullYear());
  $$("[data-year]").forEach(function (n) { n.textContent = y; });

  /* mobile nav */
  var burger = $(".burger");
  if (burger) {
    burger.addEventListener("click", function () {
      var o = d.body.classList.toggle("nav-open");
      burger.setAttribute("aria-expanded", o ? "true" : "false");
    });
    $$(".nav a").forEach(function (a) { a.addEventListener("click", function () { d.body.classList.remove("nav-open"); burger.setAttribute("aria-expanded", "false"); }); });
    d.addEventListener("keydown", function (e) { if (e.key === "Escape") { d.body.classList.remove("nav-open"); } });
  }

  /* reveal on scroll */
  var rv = $$(".rv");
  if ("IntersectionObserver" in window && rv.length) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: .08 });
    rv.forEach(function (n) { io.observe(n); });
  } else { rv.forEach(function (n) { n.classList.add("in"); }); }

  /* blog filter */
  var fl = $(".filters");
  if (fl) {
    var posts = $$("[data-niche]");
    fl.addEventListener("click", function (e) {
      var b = e.target.closest("button"); if (!b) return;
      $$("button", fl).forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
      var k = b.getAttribute("data-f");
      posts.forEach(function (p) { p.hidden = !(k === "all" || p.getAttribute("data-niche") === k); });
    });
  }


  /* hero: monochrome code rain behind the portrait and the calculator */
  $$(".mx, .mx-q").forEach(function (cv) {
    var ctx = cv.getContext("2d"), W = 0, H = 0, cols = 0, drops = [], fs = 15, vis = false, last = 0, raf = 0, dpr = 1;
    var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
    var chars = "01{}<>/;=()[]#$%&*+-_|abcdefghijklmnopqrstuvwxyz".split("");
    function size() {
      dpr = Math.min(window.devicePixelRatio || 1, 2); W = cv.clientWidth; H = cv.clientHeight;
      cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0); ctx.font = "600 " + fs + "px ui-monospace,Menlo,Consolas,monospace";
      cols = Math.ceil(W / fs); drops = [];
      for (var i = 0; i < cols; i++) drops.push(Math.random() * H / fs * 1.1);
    }
    function step() {
      ctx.globalCompositeOperation = "destination-out"; ctx.fillStyle = "rgba(0,0,0,.09)"; ctx.fillRect(0, 0, W, H);
      ctx.globalCompositeOperation = "source-over";
      for (var i = 0; i < cols; i++) {
        var y = drops[i] * fs;
        if (y > 0) {
          ctx.fillStyle = "rgba(255,255,255," + (0.55 + Math.random() * 0.35).toFixed(2) + ")";
          ctx.fillText(chars[(Math.random() * chars.length) | 0], i * fs, y);
          ctx.fillStyle = "rgba(150,150,150,.55)";
          ctx.fillText(chars[(Math.random() * chars.length) | 0], i * fs, y - fs);
        }
        if (y > H && Math.random() > 0.965) drops[i] = -Math.random() * 14;
        drops[i] += 0.55 + (i % 5) * 0.12;
      }
    }
    function loop(now) { raf = 0; if (now - last > 60) { last = now; step(); } if (vis) raf = requestAnimationFrame(loop); }
    size();
    if (reduce) { for (var k = 0; k < 40; k++) step(); return; }
    window.addEventListener("resize", size);
    if ("IntersectionObserver" in window) { new IntersectionObserver(function (es) { vis = es[0].isIntersecting; if (vis && !raf) raf = requestAnimationFrame(loop); }, { rootMargin: "100px" }).observe(cv); }
    else { vis = true; raf = requestAnimationFrame(loop); }
  });

  /* orbit: ring flows with the page (no pinning) and spills over neighbouring blocks */
  (function () {
    var sec = $("#orbit"); if (!sec) return;
    var host = $(".orbit-stick", sec), cv = $(".orbit-cv", sec), ctx = cv.getContext("2d"), W = 0, H = 0, dpr = 1;
    var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
    var visible = false, raf = 0, t0 = performance.now(), tt = 0.5, e = 1;
    function size() { dpr = Math.min(window.devicePixelRatio || 1, 2); W = cv.clientWidth; H = cv.clientHeight; cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0); }
    function read() {
      var r = host.getBoundingClientRect(), vh = window.innerHeight;
      var t = (vh - r.top) / (vh + r.height); tt = Math.max(0, Math.min(1, t));
      e = Math.pow(Math.sin(Math.PI * tt), 0.7);
    }
    function draw(now) {
      var time = (now - t0) / 1000, cx = W / 2, cy = H / 2, base = Math.min(W, 1000) * 0.46;
      ctx.clearRect(0, 0, W, H);
      var rings = [{ r: 1.00, n: 90, l: 16, s: 1 }, { r: 1.24, n: 110, l: 11, s: -1 }, { r: 1.50, n: 130, l: 7, s: 1 }, { r: 1.80, n: 150, l: 4, s: -1 }];
      var grow = 0.62 + tt * 0.8;
      rings.forEach(function (g, gi) {
        var rad = base * g.r * grow, rot = (tt * 3.2 + time * 0.03) * g.s, a = Math.max(0, Math.min(1, e * 1.25 - gi * 0.08));
        for (var i = 0; i < g.n; i++) {
          var ang = rot + i / g.n * Math.PI * 2, c = Math.cos(ang), s = Math.sin(ang);
          var pulse = 0.55 + 0.45 * Math.sin(ang * 3 + time * 0.8 + gi);
          ctx.strokeStyle = "rgba(255,255,255," + ((0.08 + 0.5 * pulse * a) * (1 - gi * 0.16)).toFixed(3) + ")";
          ctx.lineWidth = gi === 0 ? 1.6 : 1.1;
          ctx.beginPath(); ctx.moveTo(cx + c * rad, cy + s * rad); ctx.lineTo(cx + c * (rad + g.l * (0.6 + e)), cy + s * (rad + g.l * (0.6 + e))); ctx.stroke();
        }
      });
      var dots = 80, dr = base * 2.1 * grow;
      for (var k = 0; k < dots; k++) { var an = k / dots * Math.PI * 2 - time * 0.04; ctx.fillStyle = "rgba(255,255,255," + ((0.1 + 0.2 * Math.abs(Math.sin(k * 1.7 + time))) * e).toFixed(3) + ")"; ctx.fillRect(cx + Math.cos(an) * dr, cy + Math.sin(an) * dr, 1.6, 1.6); }
    }
    function frame(now) {
      raf = 0; read();
      sec.style.setProperty("--p", e.toFixed(3)); sec.style.setProperty("--t", tt.toFixed(3)); draw(now);
      if (visible) raf = requestAnimationFrame(frame);
    }
    function start() { if (!raf) raf = requestAnimationFrame(frame); }
    size();
    if (reduce) { tt = 0.5; e = 1; sec.style.setProperty("--p", "1"); sec.style.setProperty("--t", ".5"); draw(performance.now()); return; }
    read(); sec.style.setProperty("--p", e.toFixed(3)); sec.style.setProperty("--t", tt.toFixed(3)); draw(performance.now());
    window.addEventListener("resize", function () { size(); read(); draw(performance.now()); });
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (es) { visible = es[0].isIntersecting; if (visible) start(); }, { rootMargin: "60% 0px" }).observe(host);
    } else { visible = true; start(); }
  })();

  /* ===== scroll effects ===== */
  (function () {
    var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduce || !("IntersectionObserver" in window)) { $$(".portrait, .chips").forEach(function (n) { n.classList.add("in"); }); return; }

    /* 1. split headings into words */
    $$(".sec h2, .hero h1, .art-h h1, .sec-head h2, .cta h2").forEach(function (h, k) {
      if (h.classList.contains("split") || h.closest(".prose")) return;
      var i = 0;
      (function walk(node) {
        Array.prototype.slice.call(node.childNodes).forEach(function (n) {
          if (n.nodeType === 3) {
            var parts = n.nodeValue.split(/( )/), frag = d.createDocumentFragment();
            parts.forEach(function (p) {
              if (p === "") return;
              if (p === " ") { frag.appendChild(d.createTextNode(" ")); return; }
              var w = d.createElement("span"), s = d.createElement("i");
              w.className = "w"; s.textContent = p; s.style.setProperty("--i", i++); w.appendChild(s); frag.appendChild(w);
            });
            n.parentNode.replaceChild(frag, n);
          } else if (n.nodeType === 1 && n.tagName !== "BR") { walk(n); }
        });
      })(h);
      h.classList.add("split");
    });
    var io2 = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { io2.unobserve(e.target); (function go() { if (d.getElementById("pre")) { setTimeout(go, 150); } else { e.target.classList.add("in"); } })(); } });
    }, { rootMargin: "0px 0px -6% 0px", threshold: .01 });
    /* containers: children enter one by one */
    $$(".steps, .tech, .ticks, .facts, .mess, .gl, .faq").forEach(function (c) {
      c.classList.remove("rv");
      Array.prototype.slice.call(c.children).forEach(function (k, i) { if (!k.classList.contains("rv")) { k.classList.add("rv"); k.style.setProperty("--d", Math.min(i, 7) * 110 + "ms"); io2.observe(k); } });
    });
    $$(".ticks li").forEach(function (k) { k.style.setProperty("--tx", "-36px"); });
    /* hero copy enters in sequence */
    $$(".hero-copy > .eyebrow, .hero-copy > .lead, .hero-copy > .btns").forEach(function (k, i) { k.classList.add("rv"); k.style.setProperty("--d", [0, 500, 650][i] + "ms"); io2.observe(k); });
    /* paragraphs light up word by word as you scroll */
    var scrubs = [];
    $$(".sec:not(#contacts) .lead, .sec-head > p").forEach(function (pp) {
      var words = [];
      (function walk(node) {
        Array.prototype.slice.call(node.childNodes).forEach(function (n) {
          if (n.nodeType === 3) {
            var frag = d.createDocumentFragment();
            n.nodeValue.split(/( )/).forEach(function (t) {
              if (t === "") return;
              if (t === " ") { frag.appendChild(d.createTextNode(" ")); return; }
              var s = d.createElement("span"); s.className = "sw"; s.textContent = t; words.push(s); frag.appendChild(s);
            });
            n.parentNode.replaceChild(frag, n);
          } else if (n.nodeType === 1 && n.tagName !== "BR" && n.tagName !== "SVG") { walk(n); }
        });
      })(pp);
      if (words.length) { pp.classList.add("scrub"); scrubs.push({ p: pp, w: words }); }
    });
    $$(".split, .portrait, .chips").forEach(function (n) { io2.observe(n); });
    $$(".chips .chip").forEach(function (c, i) { c.style.setProperty("--i", i); });

    /* 2. stagger siblings */
    $$(".g3, .g4, .gl, .tech, .facts, .steps, .mess, .faq").forEach(function (g) {
      Array.prototype.slice.call(g.children).forEach(function (c, i) { c.style.setProperty("--d", Math.min(i, 6) * 90 + "ms"); });
    });

    /* 4. parallax, progress bar, strip skew */
    var sp = d.createElement("div"); sp.id = "sp"; sp.setAttribute("aria-hidden", "true"); d.body.appendChild(sp);
    var pars = $$(".frame, .hero-bg, .speed-bg").map(function (n) {
      return { n: n, bg: n.classList.contains("hero-bg") || n.classList.contains("speed-bg"), host: n.classList.contains("frame") ? n : n.parentNode };
    });
    var strip = $$(".strip a"), lastY = window.scrollY, sk = 0, ticking = false;
    function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(update); } }
    function update() {
      ticking = false;
      var y = window.scrollY, vh = window.innerHeight, max = d.documentElement.scrollHeight - vh;
      sp.style.transform = "scaleX(" + (max > 0 ? y / max : 0) + ")";
      pars.forEach(function (o) {
        var r = o.host.getBoundingClientRect();
        if (r.bottom < -100 || r.top > vh + 100) return;
        var k = ((r.top + r.height / 2) - vh / 2) / vh;
        if (o.bg) { o.n.style.setProperty("--py", (k * -70).toFixed(1) + "px"); }
        else { o.n.style.setProperty("--py", (k * -8).toFixed(2) + "%"); o.n.style.setProperty("--sc", (1.12 + Math.max(0, Math.min(1, (r.top + r.height / 2) / vh)) * 0.2).toFixed(3)); }
      });
      scrubs.forEach(function (o) {
        var r = o.p.getBoundingClientRect();
        if (r.bottom < -50 || r.top > vh + 50) return;
        var t = Math.max(0, Math.min(1, (vh * 0.92 - r.top) / (r.height + vh * 0.25)));
        if (r.bottom < vh * 0.45) t = 1;
        var n = o.w.length;
        for (var i = 0; i < n; i++) { var v = Math.max(0, Math.min(1, t * (n + 4) - i)); o.w[i].style.opacity = (0.16 + 0.84 * v).toFixed(2); }
      });
      var v = y - lastY; lastY = y;
      var target = Math.max(-8, Math.min(8, v * -0.35));
      sk += (target - sk) * 0.25;
      if (Math.abs(sk) < 0.05 && Math.abs(target) < 0.05) sk = 0;
      strip.forEach(function (a) { a.style.setProperty("--sk", sk.toFixed(2) + "deg"); });
      if (Math.abs(sk) > 0.05) onScroll();
    }
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);
    update();
  })();

  /* anchor scrolling: block lands centred in the area under the sticky header (or top-aligned if it is taller than the screen) */
  (function () {
    var hdr = $(".hdr"), raf = 0, stopFn = null;
    var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
    function hh() { return hdr ? hdr.offsetHeight : 68; }
    var FOCUS = { quiz: "#quizform", services: ".g3" }; /* the part of the block that matters most */
    function targetY(el) {
      var vh = window.innerHeight, H = hh(), avail = vh - H, wrapEl = $(".wrap", el) || el, box = wrapEl;
      var fs = FOCUS[el.id], fe = fs && $(fs, el);
      if (fe && fe.getBoundingClientRect().height <= avail * 1.6) box = fe;
      var r = box.getBoundingClientRect(), top = r.top + window.pageYOffset, h = r.height, y;
      if (h + 40 < avail) { y = top - H - (avail - h) / 2; } else { y = top - H - 12; }
      var max = Math.max(0, d.documentElement.scrollHeight - vh);
      return Math.max(0, Math.min(max, Math.round(y)));
    }
    function jump(y) { window.scrollTo({ top: y, left: 0, behavior: "instant" }); }
    function goTo(el, animate) {
      if (stopFn) stopFn();
      if (!animate || reduce) { jump(targetY(el)); setTimeout(function () { jump(targetY(el)); }, 350); return; }
      var from = window.pageYOffset, t0 = performance.now(), dur = Math.min(1100, 450 + Math.abs(targetY(el) - from) * 0.25), cancelled = false;
      function cancel() { cancelled = true; if (raf) cancelAnimationFrame(raf); raf = 0; stopFn = null; ["wheel", "touchstart", "keydown", "mousedown"].forEach(function (n) { window.removeEventListener(n, cancel); }); }
      stopFn = cancel;
      ["wheel", "touchstart", "keydown", "mousedown"].forEach(function (n) { window.addEventListener(n, cancel, { passive: true }); });
      function step(now) {
        if (cancelled) return;
        var k = Math.min(1, (now - t0) / dur), e = k < .5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2;
        var y = targetY(el); /* re-read every frame: layout may shift while we scroll */
        jump(from + (y - from) * e);
        if (k < 1) { raf = requestAnimationFrame(step); }
        else { cancel(); jump(targetY(el)); setTimeout(function () { jump(targetY(el)); }, 400); }
      }
      raf = requestAnimationFrame(step);
    }
    function idOf(a) {
      var h = a.getAttribute("href") || "";
      var m = h.match(/^(?:\/)?#([\w-]+)$/);
      if (!m) return null;
      if (h.charAt(0) === "/" && location.pathname !== "/" && location.pathname !== "/index.html") return null;
      return m[1];
    }
    d.addEventListener("click", function (e) {
      var a = e.target.closest && e.target.closest("a[href]");
      if (!a || e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || a.target === "_blank") return;
      var id = idOf(a); if (!id) return;
      var el = d.getElementById(id); if (!el) return;
      e.preventDefault();
      d.body.classList.remove("nav-open"); if (burger) burger.setAttribute("aria-expanded", "false");
      if (id === "top") { window.scrollTo({ top: 0, behavior: reduce ? "instant" : "smooth" }); }
      else { goTo(el, true); }
      try { history.pushState(null, "", "#" + id); } catch (er) {}
    });
    /* direct open of /#quiz etc. */
    var id0 = (location.hash || "").slice(1), el0 = id0 && d.getElementById(id0);
    if (el0 && id0 !== "top") {
      var fire = function () { goTo(el0, false); };
      if (document.readyState === "complete") { setTimeout(fire, 250); } else { window.addEventListener("load", function () { setTimeout(fire, 450); }); }
    }
  })();

  /* guarantees: the shield leans towards the cursor */
  (function () {
    var g = $(".gshield"); if (!g || !window.matchMedia || !matchMedia("(hover:hover)").matches) return;
    var host = g.closest(".guar") || g;
    host.addEventListener("mousemove", function (e) { var r = g.getBoundingClientRect(); g.style.setProperty("--mx", (((e.clientX - r.left) / r.width - .5) * 2).toFixed(2)); g.style.setProperty("--my", (((e.clientY - r.top) / r.height - .5) * 2).toFixed(2)); });
    host.addEventListener("mouseleave", function () { g.style.setProperty("--mx", "0"); g.style.setProperty("--my", "0"); });
  })();

  /* helpers */
  function fmt(n) { return n.toLocaleString("ru-RU").replace(/ /g, " ") + " ₽"; }
  var T = {
    ru: { sent: "Заявка отправлена. Я свяжусь с вами в ближайшее время и пришлю реквизиты для предоплаты.", sentSimple: "Спасибо! Заявка отправлена, я свяжусь с вами в ближайшее время.", fail: "Открываю Telegram: текст заявки уже в сообщении — просто нажмите «Отправить».", copy: "Открываю Telegram. Текст заявки скопирован — вставьте его в чат (долгое нажатие → «Вставить») и нажмите «Отправить».", req: "Заполните имя и контакт и поставьте галочку согласия.", from: "от " },
    en: { sent: "Request sent. I will contact you shortly with the prepayment details.", sentSimple: "Thank you! Your request has been sent, I will contact you shortly.", fail: "Opening Telegram: your request text is already in the message — just press send.", copy: "Opening Telegram. Your request text is copied — paste it into the chat and press send.", req: "Please fill in your name and contact and tick the consent box.", from: "from " }
  }[lang];

  /* lead sending */
  function copyText(s) {
    try { if (navigator.clipboard && navigator.clipboard.writeText) { navigator.clipboard.writeText(s).catch(function () {}); return; } } catch (e) {}
    try { var ta = document.createElement("textarea"); ta.value = s; ta.setAttribute("readonly", ""); ta.style.cssText = "position:fixed;top:0;left:0;opacity:0"; document.body.appendChild(ta); ta.select(); document.execCommand("copy"); document.body.removeChild(ta); } catch (e) {}
  }
  function tgLink(txt) {
    /* с username в t.me текст подставляется сам; ссылка по номеру телефона текст не принимает, поэтому он ещё и копируется */
    var base = cfg.tgUser ? "https://t.me/" + String(cfg.tgUser).replace(/^@/, "") : (cfg.telegram || "");
    return base + (base.indexOf("?") > -1 ? "&" : "?") + "text=" + encodeURIComponent(txt);
  }
  function failMsg() { return cfg.tgUser ? T.fail : T.copy; }
  function sendLead(payload, done) {
    var txt = payload.text;
    copyText(txt);
    if (cfg.telegram || cfg.tgUser) { window.open(tgLink(txt), "_blank", "noopener"); }
    done(false);
  }
  function track(goal) { try { if (window.ym && cfg.metrika) { window.ym(cfg.metrika, "reachGoal", goal); } } catch (e) {} }

  /* generic forms (contact form) */
  $$("form[data-lead]").forEach(function (f) {
    var ts = Date.now();
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var msg = $(".msg", f), btn = $("button[type=submit]", f);
      var name = (f.elements.name.value || "").trim(), contact = (f.elements.contact.value || "").trim();
      if (!name || !contact || !f.elements.agree.checked) { msg.className = "msg err"; msg.textContent = T.req; return; }
      if (f.elements.website.value || Date.now() - ts < 1500) { msg.className = "msg ok"; msg.textContent = T.sentSimple; f.reset(); return; } /* honeypot / too fast: silently drop */
      var text = "Заявка с сайта dmitry-web.ru\nИмя: " + name + "\nКонтакт: " + contact + "\nСообщение: " + ((f.elements.message && f.elements.message.value) || "-") + "\nСтраница: " + location.pathname;
      btn.disabled = true;
      sendLead({ kind: "contact", name: name, contact: contact, message: f.elements.message ? f.elements.message.value : "", page: location.href, website: "", text: text, t: Date.now() - ts }, function (ok) {
        btn.disabled = false;
        msg.className = "msg ok"; msg.textContent = ok ? T.sentSimple : failMsg();
        if (ok) { f.reset(); track("lead_form"); }
      });
    });
  });

  /* quiz */
  var q = $("#quizform");
  if (q) {
    var steps = $$(".qstep", q), bars = $$(".qbar i", q), cur = 0;
    var P = { landing: 15000, shop: 35000, shopFree: 20, shopExtra: 500, card: 350, rush: 30000, en: 4000, art: 3000, city: 3000, place: 1500 };
    var prepay = +q.getAttribute("data-prepay") || 5000;
    var st = { type: "landing", qty: 10, shopFrom: false, xart: 1, xplace: 1, xcity: 1, addCards: false, addQty: 20 };
    var out = { sum: $(".sum", q), list: $(".qlist", q), pre: $(".qpre", q), note: $(".qnote", q) };
    function cnt(el, t) { if (el && el.getAttribute("data-live") && window.DWcount) window.DWcount(el, t); else if (el) el.textContent = t; }
    function lab(n) { var el = $("[data-lab=" + n + "]", q); return el ? el.textContent : n; }
    function calc() {
      var t = (q.elements.type.value) || "landing", total = 0, from = false, rows = [];
      st.type = t;
      var qty = +q.elements.qty.value || 1;
      $("#qty-out", q).textContent = qty;
      var aq = +q.elements.addqty.value || 1; $("#addqty-out", q).textContent = aq;
      if (t === "landing") { total = P.landing; rows.push([lab("rLanding"), fmt(P.landing)]); }
      if (t === "rush") { total = P.rush; rows.push([lab("rRush"), fmt(P.rush)]); }
      if (t === "shop") {
        var sk = Math.max(P.shopFree, +q.elements.skus.value || P.shopFree), ex = sk - P.shopFree, so = $("#skus-out", q); if (so) so.textContent = sk;
        total = P.shop; rows.push([lab("rShop"), fmt(P.shop)]); rows.push([lab("rSkus"), String(sk)]);
        if (ex > 0) { total += ex * P.shopExtra; rows.push([lab("rMore"), ex + " × " + fmt(P.shopExtra)]); }
      }
      if (t === "card") { total = P.card * qty; rows.push([lab("rCards"), qty + " × " + fmt(P.card)]); }
      if (t !== "card" && q.elements.addcards.checked) { total += P.card * aq; rows.push([lab("rAddCards"), aq + " × " + fmt(P.card)]); }
      if (t !== "card") {
        if (q.elements.xen.checked) { total += P.en; rows.push([lab("rEn"), fmt(P.en)]); }
        if (q.elements.xart.checked) { total += P.art * st.xart; rows.push([lab("rArt"), st.xart + " × " + fmt(P.art)]); }
        if (q.elements.xplace.checked) { total += P.place * st.xplace; rows.push([lab("rPlace"), st.xplace + " × " + fmt(P.place)]); }
        if (q.elements.xcity.checked) { total += P.city * st.xcity; rows.push([lab("rCity"), st.xcity + " × " + fmt(P.city)]); }
      }
      cnt(out.sum, (from ? T.from : "") + fmt(total));
      out.list.innerHTML = rows.map(function (r) { return "<dt></dt><dd></dd>"; }).join("");
      var dts = $$("dt", out.list), dds = $$("dd", out.list);
      rows.forEach(function (r, i) { dts[i].textContent = r[0] + ":"; dds[i].textContent = r[1]; });
      if (t === "card") { out.pre.hidden = true; out.note.hidden = false; } else { out.pre.hidden = false; out.note.hidden = true; cnt($(".pv", out.pre), fmt(prepay)); }
      st.total = total; st.from = from; st.rows = rows;
      var vol = $(".qvol", q); if (vol) vol.hidden = !(t !== "card" && ((q.elements.xart.checked && st.xart > 30) || (q.elements.xplace.checked && st.xplace > 30) || (q.elements.xcity.checked && st.xcity > 30)));
      var qt = $(".qterm", q); if (qt) qt.textContent = qt.getAttribute(t === "rush" ? "data-t24" : "data-t3");
      q.classList.toggle("is-rush", t === "rush");
      /* toggle conditional blocks */
      $$("[data-for]", q).forEach(function (b) { b.hidden = b.getAttribute("data-for").split(" ").indexOf(t) < 0; });
      $("#addcards-box", q).hidden = (t === "card");
      $("#addqty-box", q).hidden = !(t !== "card" && q.elements.addcards.checked);
    }
    function show(n) {
      cur = Math.max(0, Math.min(steps.length - 1, n));
      steps.forEach(function (s, i) { s.classList.toggle("on", i === cur); });
      bars.forEach(function (b, i) { b.classList.toggle("on", i <= cur); });
      if (cur > 0) { var r = q.getBoundingClientRect(); if (r.top < 0) { q.scrollIntoView({ behavior: "smooth", block: "start" }); } }
    }
    $$(".stp", q).forEach(function (b) {
      var k = b.getAttribute("data-k"), o = $("output", b), bt = $$("button", b);
      function set(v) { st[k] = Math.max(1, Math.min(200, v)); o.textContent = st[k]; calc(); }
      bt[0].addEventListener("click", function () { set(st[k] - 1); });
      bt[1].addEventListener("click", function () { set(st[k] + 1); });
    });
    $$("input[name=xart],input[name=xplace],input[name=xcity]", q).forEach(function (i) { i.addEventListener("change", function () { $(".stp[data-k=" + i.name + "]", q).hidden = !i.checked; }); });
    var nb = $("[data-none]", q);
    if (nb) nb.addEventListener("click", function () {
      ["xen", "xart", "xplace", "xcity", "addcards"].forEach(function (n) { q.elements[n].checked = false; });
      $$(".stp", q).forEach(function (b) { b.hidden = true; });
      calc(); show(cur + 1); track("quiz_step_" + (cur + 1));
    });
    q.addEventListener("change", calc);
    q.addEventListener("input", calc);
    $$("[data-next]", q).forEach(function (b) { b.addEventListener("click", function () { show(cur + 1); track("quiz_step_" + (cur + 1)); }); });
    $$("[data-prev]", q).forEach(function (b) { b.addEventListener("click", function () { show(cur - 1); }); });
    calc(); show(0);
    var qts = Date.now();
    q.addEventListener("submit", function (e) {
      e.preventDefault();
      var msg = $(".msg", q), btn = $("button[type=submit]", q);
      var name = (q.elements.name.value || "").trim(), contact = (q.elements.contact.value || "").trim();
      if (!name || !contact || !q.elements.agree.checked) { msg.className = "msg err"; msg.textContent = T.req; return; }
      if (q.elements.website.value || Date.now() - qts < 2500) { msg.className = "msg ok"; msg.textContent = T.sent; return; }
      var lines = st.rows.map(function (r) { return r[0] + ": " + r[1]; }).join("\n");
      var text = "Фиксация цены (квиз) dmitry-web.ru\nИмя: " + name + "\nКонтакт: " + contact + "\n" + lines + "\nИтого: " + (st.from ? "от " : "") + fmt(st.total) + (st.type !== "card" ? "\nПредоплата: " + fmt(prepay) : "") + "\nКомментарий: " + (q.elements.comment.value || "-");
      btn.disabled = true;
      sendLead({ kind: "quiz", name: name, contact: contact, message: q.elements.comment.value, page: location.href, website: "", text: text, total: st.total, t: Date.now() - qts }, function (ok) {
        btn.disabled = false;
        msg.className = "msg ok"; msg.textContent = ok ? T.sent : failMsg();
        if (ok) { track("quiz_lead"); var pay = $("#payBtn", q); if (pay) pay.hidden = false; }
      });
    });
  }
})();

/* count-up numbers: hero chips and "about" facts run from 0 to the final value when they appear */
(function () {
  var d = document, reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var els = Array.prototype.slice.call(d.querySelectorAll(".chip b, .fact b")), items = [];
  els.forEach(function (b) {
    var m = b.textContent.match(/^(\d+(?:[\s ]\d{3})*)(.*)$/);
    if (!m) return;
    var raw = m[1], to = parseInt(raw.replace(/[\s ]/g, ""), 10), sep = /[\s ]/.test(raw);
    if (!to) return;
    items.push({ b: b, to: to, sep: sep, tail: m[2], full: b.textContent });
  });
  if (!items.length || reduce || !("IntersectionObserver" in window)) return;
  function fmt(n, it) { var s = String(n); if (it.sep) s = n.toLocaleString("ru-RU").replace(/[\s  ]/g, " "); return s + it.tail; }
  items.forEach(function (it) {
    var b = it.b; b.style.display = "inline-block"; b.style.minWidth = b.getBoundingClientRect().width + "px"; b.style.fontVariantNumeric = "tabular-nums";
    b.textContent = fmt(0, it);
  });
  function run(it) {
    var dur = 1500 + Math.min(it.to, 20000) / 20000 * 500, t0 = performance.now();
    (function step(now) {
      var p = Math.min(1, (now - t0) / dur), e = 1 - Math.pow(1 - p, 3);
      it.b.textContent = p < 1 ? fmt(Math.round(it.to * e), it) : it.full;
      if (p < 1) requestAnimationFrame(step);
    })(t0);
  }
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting) return;
      io.unobserve(e.target);
      var it = items.filter(function (x) { return x.b === e.target; })[0];
      (function go() { if (d.getElementById("pre")) setTimeout(go, 150); else setTimeout(function () { run(it); }, 250); })();
    });
  }, { threshold: .6 });
  items.forEach(function (it) { io.observe(it.b); });
})();

/* count-up for calculator and price numbers: from 0 on first view, smooth tween on changes */
(function () {
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var RE = /\d+(?:[\u00a0\u202f ]\d{3})*/g;
  function nums(t) { return (t.match(RE) || []).map(function (x) { return parseInt(x.replace(/[\u00a0\u202f ]/g, ""), 10); }); }
  function fmtN(n, big) { var s = String(n); if (big || n >= 1000) s = n.toLocaleString("ru-RU").replace(/[\u202f ]/g, "\u00a0"); return s; }
  function build(t, vals) { var i = 0; return t.replace(RE, function (m) { var v = Math.round(vals[i++]); return fmtN(v, /[\u00a0\u202f ]/.test(m)); }); }
  function node(el) { for (var i = 0; i < el.childNodes.length; i++) { var c = el.childNodes[i]; if (c.nodeType === 3 && /\d/.test(c.nodeValue)) return c; } return null; }
  function tween(el, to, from, dur) {
    if (el.__raf) cancelAnimationFrame(el.__raf);
    var nd = node(el), tn = nums(to);
    if (!nd) { el.textContent = to; return; }
    if (reduce || !tn.length || tn.length !== from.length) { nd.nodeValue = to; return; }
    var t0 = performance.now();
    (function step(now) {
      var p = Math.min(1, (now - t0) / dur), e = 1 - Math.pow(1 - p, 3);
      nd.nodeValue = p < 1 ? build(to, tn.map(function (v, i) { return from[i] + (v - from[i]) * e; })) : to;
      el.__raf = p < 1 ? requestAnimationFrame(step) : 0;
    })(t0);
  }
  window.DWcount = function (el, to) { var nd = node(el); tween(el, to, nd ? nums(nd.nodeValue) : [], 700); };
  function fromZero(el) { var nd = node(el); if (!nd) return; var t = nd.nodeValue; tween(el, t, nums(t).map(function () { return 0; }), 1500); }
  if (reduce || !("IntersectionObserver" in window)) { Array.prototype.forEach.call(document.querySelectorAll(".sum, .pv"), function (e) { e.setAttribute("data-live", "1"); }); return; }
  function when(el, fn, th) {
    var io = new IntersectionObserver(function (es) {
      if (!es[0].isIntersecting) return; io.disconnect();
      (function go() { if (document.getElementById("pre")) setTimeout(go, 150); else setTimeout(fn, 200); })();
    }, { threshold: th || .5 });
    io.observe(el);
  }
  /* zero them out until they are seen */
  function zero(el) { var nd = node(el); if (!nd) return null; var t = nd.nodeValue; nd.nodeValue = build(t, nums(t).map(function () { return 0; })); return t; }
  Array.prototype.forEach.call(document.querySelectorAll(".price, .opt .p"), function (el) {
    var nd = node(el); if (!nd) return; var t = zero(el);
    when(el, function () { nd.nodeValue = t; fromZero(el); }, .6);
  });
  var res = document.querySelector(".qres");
  if (res) {
    var targets = [".sum", ".pv"].map(function (q) { return res.querySelector(q); }).filter(Boolean);
    when(res, function () {
      targets.forEach(function (el) { fromZero(el); setTimeout(function () { el.setAttribute("data-live", "1"); }, 1600); });
      Array.prototype.forEach.call(res.querySelectorAll(".qlist dd"), fromZero);
    }, .4);
  }
})();
