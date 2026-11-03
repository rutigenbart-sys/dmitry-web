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


  /* orbit: smooth scroll-driven ring of ticks */
  (function () {
    var sec = $("#orbit"); if (!sec) return;
    var cv = $(".orbit-cv", sec), ctx = cv.getContext("2d"), W = 0, H = 0, dpr = 1;
    var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
    var target = 0, p = reduce ? 1 : 0, visible = false, raf = 0, t0 = performance.now();
    function size() { dpr = Math.min(window.devicePixelRatio || 1, 2); W = cv.clientWidth; H = cv.clientHeight; cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0); }
    function readScroll() { var r = sec.getBoundingClientRect(), total = sec.offsetHeight - window.innerHeight; target = total > 0 ? Math.max(0, Math.min(1, -r.top / total)) : 1; }
    function draw(now) {
      var time = (now - t0) / 1000, cx = W / 2, cy = H * 0.46, base = Math.min(W, H) * 0.30;
      ctx.clearRect(0, 0, W, H);
      var rings = [{ r: 1.00, n: 90, l: 16, s: 1 }, { r: 1.22, n: 110, l: 11, s: -1 }, { r: 1.46, n: 130, l: 7, s: 1 }, { r: 1.74, n: 150, l: 4, s: -1 }];
      rings.forEach(function (g, gi) {
        var rad = base * g.r * (0.6 + p * 0.55), rot = (p * 1.6 + time * 0.03) * g.s, a = Math.max(0, Math.min(1, p * 2.2 - gi * 0.12));
        for (var i = 0; i < g.n; i++) {
          var ang = rot + i / g.n * Math.PI * 2, c = Math.cos(ang), s = Math.sin(ang);
          var pulse = 0.55 + 0.45 * Math.sin(ang * 3 + time * 0.8 + gi);
          ctx.strokeStyle = "rgba(255,255,255," + (0.10 + 0.55 * pulse * a) * (1 - gi * 0.18) + ")";
          ctx.lineWidth = gi === 0 ? 1.6 : 1.1;
          ctx.beginPath(); ctx.moveTo(cx + c * rad, cy + s * rad); ctx.lineTo(cx + c * (rad + g.l * (0.5 + p)), cy + s * (rad + g.l * (0.5 + p))); ctx.stroke();
        }
      });
      var dots = 70, dr = base * 2.15 * (0.6 + p * 0.55);
      for (var k = 0; k < dots; k++) { var an = k / dots * Math.PI * 2 - time * 0.04; ctx.fillStyle = "rgba(255,255,255," + (0.12 + 0.2 * Math.abs(Math.sin(k * 1.7 + time))) + ")"; ctx.fillRect(cx + Math.cos(an) * dr, cy + Math.sin(an) * dr, 1.6, 1.6); }
    }
    function frame(now) {
      raf = 0; readScroll();
      p += (target - p) * 0.09; if (Math.abs(target - p) < 0.0005) p = target;
      sec.style.setProperty("--p", p.toFixed(4)); draw(now);
      if (visible) raf = requestAnimationFrame(frame);
    }
    function start() { if (!raf) raf = requestAnimationFrame(frame); }
    size(); readScroll(); sec.style.setProperty("--p", p.toFixed(4)); draw(performance.now());
    if (reduce) { return; }
    window.addEventListener("resize", function () { size(); draw(performance.now()); });
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (es) { visible = es[0].isIntersecting; if (visible) start(); }, { rootMargin: "100px" }).observe(sec);
    } else { visible = true; start(); }
  })();

  /* helpers */
  function fmt(n) { return n.toLocaleString("ru-RU").replace(/ /g, " ") + " ₽"; }
  var T = {
    ru: { sent: "Заявка отправлена. Я свяжусь с вами в ближайшее время и пришлю реквизиты для предоплаты.", sentSimple: "Спасибо! Заявка отправлена, я свяжусь с вами в ближайшее время.", fail: "Не удалось отправить автоматически. Открываю Telegram с готовым текстом — просто отправьте сообщение.", req: "Заполните имя и контакт и поставьте галочку согласия.", from: "от " },
    en: { sent: "Request sent. I will contact you shortly with the prepayment details.", sentSimple: "Thank you! Your request has been sent, I will contact you shortly.", fail: "Could not send automatically. Opening Telegram with a ready message — just press send.", req: "Please fill in your name and contact and tick the consent box.", from: "from " }
  }[lang];

  /* lead sending */
  function sendLead(payload, done) {
    var body = JSON.stringify(payload);
    var txt = payload.text;
    function fallback() {
      if (cfg.telegram) { window.open(cfg.telegram + (cfg.telegram.indexOf("?") > -1 ? "&" : "?") + "text=" + encodeURIComponent(txt), "_blank", "noopener"); }
      done(false);
    }
    if (!cfg.endpoint) { fallback(); return; }
    var ctl = ("AbortController" in window) ? new AbortController() : null;
    var t = setTimeout(function () { if (ctl) ctl.abort(); }, 9000);
    fetch(cfg.endpoint, { method: "POST", headers: { "Content-Type": "application/json" }, body: body, signal: ctl ? ctl.signal : undefined, keepalive: true })
      .then(function (r) { clearTimeout(t); return r.ok ? r.json().catch(function () { return {}; }) : Promise.reject(); })
      .then(function (j) { if (j && j.ok === false) { fallback(); } else { done(true); } })
      .catch(function () { clearTimeout(t); fallback(); });
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
        msg.className = ok ? "msg ok" : "msg err"; msg.textContent = ok ? T.sentSimple : T.fail;
        if (ok) { f.reset(); track("lead_form"); }
      });
    });
  });

  /* quiz */
  var q = $("#quizform");
  if (q) {
    var steps = $$(".qstep", q), bars = $$(".qbar i", q), cur = 0;
    var P = { landing: 15000, shop: 55000, card: 350 };
    var prepay = +q.getAttribute("data-prepay") || 5000;
    var st = { type: "landing", qty: 10, shopFrom: false, extras: [], addCards: false, addQty: 20 };
    var out = { sum: $(".sum", q), list: $(".qlist", q), pre: $(".qpre", q), note: $(".qnote", q) };
    function lab(n) { var el = $("[data-lab=" + n + "]", q); return el ? el.textContent : n; }
    function calc() {
      var t = (q.elements.type.value) || "landing", total = 0, from = false, rows = [];
      st.type = t;
      var qty = +q.elements.qty.value || 1;
      $("#qty-out", q).textContent = qty;
      var aq = +q.elements.addqty.value || 1; $("#addqty-out", q).textContent = aq;
      if (t === "landing") { total = P.landing; rows.push([lab("rLanding"), fmt(P.landing)]); }
      if (t === "shop") { total = P.shop; from = true; rows.push([lab("rShop"), T.from + fmt(P.shop)]); var sv = q.elements.skus.value; rows.push([lab("rSkus"), sv]); }
      if (t === "card") { total = P.card * qty; rows.push([lab("rCards"), qty + " × " + fmt(P.card)]); }
      if (t !== "card" && q.elements.addcards.checked) { total += P.card * aq; rows.push([lab("rAddCards"), aq + " × " + fmt(P.card)]); }
      var ex = $$("input[name=extra]:checked", q).map(function (i) { return i.value; });
      if (ex.length) rows.push([lab("rExtra"), ex.join(", ")]);
      out.sum.textContent = (from ? T.from : "") + fmt(total);
      out.list.innerHTML = rows.map(function (r) { return "<dt></dt><dd></dd>"; }).join("");
      var dts = $$("dt", out.list), dds = $$("dd", out.list);
      rows.forEach(function (r, i) { dts[i].textContent = r[0] + ":"; dds[i].textContent = r[1]; });
      if (t === "card") { out.pre.hidden = true; out.note.hidden = false; } else { out.pre.hidden = false; out.note.hidden = true; $(".pv", out.pre).textContent = fmt(prepay); }
      st.total = total; st.from = from; st.rows = rows;
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
        msg.className = ok ? "msg ok" : "msg err"; msg.textContent = ok ? T.sent : T.fail;
        if (ok) { track("quiz_lead"); var pay = $("#payBtn", q); if (pay) pay.hidden = false; }
      });
    });
  }
})();
