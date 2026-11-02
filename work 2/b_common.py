# -*- coding: utf-8 -*-
import json, os, hashlib, html, datetime, re
ROOT = os.path.dirname(os.path.abspath(__file__))
CFG = json.load(open(os.path.join(ROOT, "config.json"), encoding="utf-8"))
SITE = CFG["site_url"].rstrip("/")
OUT = os.path.join(ROOT, "dist")
TODAY = datetime.date.today().isoformat()
E = lambda s: html.escape(str(s), quote=True)

def _ver(*files):
    h = hashlib.md5()
    for f in files:
        h.update(open(os.path.join(ROOT, "site", "assets", f), "rb").read())
    return h.hexdigest()[:8]
VER_CSS = _ver("style.css"); VER_JS = _ver("app.js")

IC = {
 "tel": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15 15 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.100.400 2.300.600 3.600.600.600 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.500c.600 0 1 .4 1 1 0 1.300.200 2.500.600 3.600.100.400 0 .700-.200 1z"/></svg>',
 "tg": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21.500 3 2.600 10.300c-1 .4-1 1.800.1 2.100l4.800 1.500 1.900 5.900c.3.900 1.400 1.100 2 .4l2.700-2.700 5 3.700c.8.600 1.900.1 2.100-.9L24 4.500c.2-1.100-.8-1.800-2.500-1.500zM9.700 14l8-5-6.200 6-.3 3.200z"/></svg>',
 "wa": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.600 15.100L2 22l5-1.300A10 10 0 1 0 12 2zm0 18.200c-1.500 0-3-.4-4.200-1.200l-.3-.2-3 .8.8-2.900-.2-.3A8.200 8.200 0 1 1 12 20.200zm4.500-6.100c-.2-.1-1.500-.7-1.700-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1-1.500-.7-2.500-1.300-3.400-2.800-.3-.4.2-.4.700-1.300.1-.2.1-.3 0-.5l-.8-1.900c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.5.100-.7.300-.2.300-.9.900-.9 2.200s.9 2.500 1 2.700c.1.200 1.800 2.800 4.400 3.900 1.600.7 2.300.8 3.100.6.500-.1 1.500-.6 1.700-1.200.2-.6.2-1.100.2-1.200-.1-.2-.2-.2-.4-.3z"/></svg>',
 "max": '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill-rule="evenodd" d="M5 3h14a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2zm1.600 14h1.800v-6.200l2.700 4h.1l2.700-4V17h1.800V7.500h-1.700L11.200 12.600 8.300 7.500H6.600z"/></svg>',
}
def ico(name, d):
    return f'<span class="ico"><svg viewBox="0 0 24 24" aria-hidden="true">{d}</svg></span>'
ICONS_S = {
 "speed": '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
 "shield": '<path d="M12 3 4 6v6c0 5 3.500 8 8 9 4.500-1 8-4 8-9V6z"/><path d="m9 12 2 2 4-4"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "pin": '<path d="M12 21s7-6 7-11a7 7 0 0 0-14 0c0 5 7 11 7 11z"/><circle cx="12" cy="10" r="2.500"/>',
 "doc": '<path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5M10 13h6M10 17h6"/>',
 "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/>',
 "star": '<path d="m12 3 2.700 5.600 6.100.8-4.500 4.200 1.100 6.100L12 16.800 6.600 19.700l1.100-6.100L3.200 9.400l6.100-.8z"/>',
 "code": '<path d="m8 8-5 4 5 4M16 8l5 4-5 4M14 5l-4 14"/>',
 "bag": '<path d="M5 8h14l-1 12H6z"/><path d="M9 8a3 3 0 0 1 6 0"/>',
 "img": '<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="10" r="2"/><path d="m4 18 5-5 4 4 3-3 4 4"/>',
 "chat": '<path d="M4 5h16v11H9l-5 4z"/>',
 "check": '<path d="m5 12 5 5 9-10"/>',
}
def sico(n): return ico(n, ICONS_S[n])

LOGO = '<svg viewBox="0 0 48 48" aria-hidden="true" focusable="false"><path d="M9 7h15a17 17 0 0 1 0 34H9z" fill="none" stroke="#fff" stroke-width="4"/><rect x="20" y="20" width="8" height="8" fill="#fff"/></svg>'

IMG_W = [480, 800, 1200]
IMG_DIMS = {}
def _dims():
    from PIL import Image
    d = os.path.join(ROOT, "site", "assets", "img")
    for f in os.listdir(d):
        m = re.match(r"(.+)-(\d+)\.jpg$", f)
        if m:
            im = Image.open(os.path.join(d, f)); IMG_DIMS[(m.group(1), int(m.group(2)))] = im.size
_dims()
def avail(name):
    return sorted(w for (n, w) in IMG_DIMS if n == name)

def pic(name, alt, sizes="100vw", eager=False, cls="", maxw=None, attrs=""):
    ws = [w for w in avail(name) if (maxw is None or w <= maxw)]
    if not ws: raise SystemExit("no image " + name)
    big = ws[-1]; w0, h0 = IMG_DIMS[(name, big)]
    def ss(ext): return ", ".join(f"/assets/img/{name}-{w}.{ext} {w}w" for w in ws)
    load = 'fetchpriority="high" decoding="async"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return (f'<picture><source type="image/avif" srcset="{ss("avif")}" sizes="{sizes}">'
            f'<source type="image/webp" srcset="{ss("webp")}" sizes="{sizes}">'
            f'<img{c} src="/assets/img/{name}-{big}.jpg" srcset="{ss("jpg")}" sizes="{sizes}" width="{w0}" height="{h0}" alt="{E(alt)}" {load} {attrs}></picture>')

def deco(name, cls):
    ws = avail(name); big = ws[-1]; w0, h0 = IMG_DIMS[(name, big)]
    mid = [w for w in ws if w >= 800][0] if any(w >= 800 for w in ws) else big
    return (f'<picture><source type="image/avif" srcset="/assets/img/{name}-{mid}.avif"><source type="image/webp" srcset="/assets/img/{name}-{mid}.webp">'
            f'<img class="{cls}" src="/assets/img/{name}-{mid}.jpg" width="{IMG_DIMS[(name, mid)][0]}" height="{IMG_DIMS[(name, mid)][1]}" alt="" aria-hidden="true" loading="lazy" decoding="async"></picture>')

def jl(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "</script>"

def url(path): return SITE + path

def org_schema(lang="ru"):
    return {
     "@context": "https://schema.org",
     "@graph": [
      {"@type": ["ProfessionalService", "LocalBusiness"], "@id": SITE + "/#org", "name": "DMITRY·WEB — Дмитрий, создание сайтов" if lang == "ru" else "DMITRY·WEB — Dmitry, website development",
       "url": SITE + "/", "logo": SITE + "/assets/icons/icon-512.png", "image": SITE + "/assets/img/og-image.jpg",
       "telephone": CFG["phone"], "email": CFG["email"], "priceRange": "15000–55000 RUB",
       "address": {"@type": "PostalAddress", "addressLocality": "Москва", "addressCountry": "RU"},
       "areaServed": [{"@type": "Country", "name": "Россия"}, {"@type": "Place", "name": "Весь мир"}],
       "knowsLanguage": ["ru", "en"], "founder": {"@id": SITE + "/#person"},
       "contactPoint": [{"@type": "ContactPoint", "telephone": CFG["phone"], "contactType": "sales", "availableLanguage": ["ru", "en"]}],
       "sameAs": [CFG["telegram"], CFG["whatsapp"]]},
      {"@type": "Person", "@id": SITE + "/#person", "name": "Дмитрий" if lang == "ru" else "Dmitry", "jobTitle": "Веб-разработчик" if lang == "ru" else "Web developer",
       "image": SITE + "/assets/img/portrait-832.jpg", "worksFor": {"@id": SITE + "/#org"}, "url": SITE + "/"},
      {"@type": "WebSite", "@id": SITE + "/#site", "url": SITE + "/", "name": "DMITRY·WEB", "inLanguage": ["ru", "en"], "publisher": {"@id": SITE + "/#org"}}
     ]}

def crumbs_schema(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + p} for i, (n, p) in enumerate(items)]}

def crumbs_html(items, lang="ru"):
    li = []
    for i, (n, p) in enumerate(items):
        if i < len(items) - 1: li.append(f'<li><a href="{p}">{E(n)}</a></li>')
        else: li.append(f'<li aria-current="page">{E(n)}</li>')
    lab = "Хлебные крошки" if lang == "ru" else "Breadcrumbs"
    return f'<nav class="crumbs wrap" aria-label="{lab}"><ol>{"".join(li)}</ol></nav>'

NAV = {
 "ru": [("Услуги", "/#services"), ("Расчёт", "/#quiz"), ("Кейсы", "/#cases"), ("Гарантии", "/#guarantees"), ("Блог", "/blog/"), ("Города", "/cities/"), ("Контакты", "/#contacts")],
 "en": [("Services", "/en/#services"), ("Calculator", "/en/#quiz"), ("Cases", "/en/#cases"), ("Guarantees", "/en/#guarantees"), ("Blog", "/blog/"), ("Cities", "/cities/"), ("Contacts", "/en/#contacts")],
}

def header(lang, alt_url):
    nav = "".join(f'<a href="{u}">{E(t)}</a>' for t, u in NAV[lang])
    home = "/" if lang == "ru" else "/en/"
    if lang == "ru": sw = f'<span aria-current="true">RU</span><a href="{alt_url}" hreflang="en" lang="en" title="English version">EN</a>'
    else: sw = f'<a href="{alt_url}" hreflang="ru" lang="ru" title="Русская версия">RU</a><span aria-current="true">EN</span>'
    langbox = f'<div class="lang" role="group" aria-label="{"Язык" if lang == "ru" else "Language"}">{sw}</div>'
    menu = "Меню" if lang == "ru" else "Menu"
    return (f'<header class="hdr"><div class="wrap"><a class="logo" href="{home}" aria-label="DMITRY·WEB — {"на главную" if lang == "ru" else "home"}">{LOGO}<span>DMITRY·WEB</span></a>'
            f'<nav class="nav" id="nav" aria-label="{"Основное меню" if lang == "ru" else "Main menu"}">{nav}{langbox}</nav>'
            f'<div class="hdr-r"><a class="tel-h" href="tel:{CFG["phone"]}">{CFG["phone_view"]}</a>{langbox}'
            f'<button class="burger" type="button" aria-label="{menu}" aria-expanded="false" aria-controls="nav"><i></i><i></i><i></i></button></div></div></header>')

def messengers_block(lang="ru"):
    t = {"ru": ("Позвонить", "Telegram", "WhatsApp", "Max", "Написать", "Ответ обычно в течение часа"), "en": ("Call", "Telegram", "WhatsApp", "Max", "Message", "Usually replies within an hour")}[lang]
    return (f'<div class="mess">'
            f'<a href="tel:{CFG["phone"]}" data-goal="click_phone">{IC["tel"]}<span>{t[0]}<small>{CFG["phone_view"]}</small></span></a>'
            f'<a href="{CFG["telegram"]}" target="_blank" rel="noopener" data-goal="click_telegram">{IC["tg"]}<span>{t[1]}<small>{t[4]}</small></span></a>'
            f'<a href="{CFG["whatsapp"]}" target="_blank" rel="noopener" data-goal="click_whatsapp">{IC["wa"]}<span>{t[2]}<small>{t[4]}</small></span></a>'
            f'<a href="{CFG["max"]}" target="_blank" rel="noopener" data-goal="click_max">{IC["max"]}<span>{t[3]}<small>{t[4]}</small></span></a></div>')

def fab(lang):
    l = {"ru": ("Позвонить", "Написать в Telegram", "Написать в WhatsApp", "Написать в Max"), "en": ("Call", "Message on Telegram", "Message on WhatsApp", "Message on Max")}[lang]
    return (f'<div class="fab" role="group" aria-label="{"Быстрая связь" if lang == "ru" else "Quick contact"}">'
            f'<a href="tel:{CFG["phone"]}" aria-label="{l[0]}" data-goal="click_phone">{IC["tel"]}</a>'
            f'<a class="dk" href="{CFG["telegram"]}" target="_blank" rel="noopener" aria-label="{l[1]}" data-goal="click_telegram">{IC["tg"]}</a>'
            f'<a class="dk" href="{CFG["whatsapp"]}" target="_blank" rel="noopener" aria-label="{l[2]}" data-goal="click_whatsapp">{IC["wa"]}</a>'
            f'<a class="dk" href="{CFG["max"]}" target="_blank" rel="noopener" aria-label="{l[3]}" data-goal="click_max">{IC["max"]}</a></div>')

def footer(lang):
    ru = lang == "ru"
    inn = f", ИНН {CFG['inn']}" if CFG.get("inn") else ""
    priv = "/privacy/" if ru else "/en/privacy/"
    if ru:
        cols = (f'<div><a class="logo" href="/" style="margin-bottom:14px">{LOGO}<span>DMITRY·WEB</span></a><p>Создание сайтов с нуля под ключ. Лендинг за 3 дня, интернет-магазины, нейрокарточки для маркетплейсов. Москва и весь мир, русский и английский.</p></div>'
                '<div><h4>Услуги</h4><ul><li><a href="/#services">Лендинг — 15 000 ₽</a></li><li><a href="/#services">Интернет-магазин от 55 000 ₽</a></li><li><a href="/#services">Нейрокарточки — 350 ₽</a></li><li><a href="/#quiz">Рассчитать стоимость</a></li></ul></div>'
                '<div><h4>Разделы</h4><ul><li><a href="/blog/">Блог о сайтах</a></li><li><a href="/cities/">Сайты по городам</a></li><li><a href="/terms/">Условия работы</a></li><li><a href="/privacy/">Политика конфиденциальности</a></li><li><a href="/en/">English</a></li></ul></div>'
                f'<div><h4>Контакты</h4><ul><li><a href="tel:{CFG["phone"]}">{CFG["phone_view"]}</a></li><li><a href="mailto:{CFG["email"]}">{CFG["email"]}</a></li><li><a href="{CFG["telegram"]}" rel="noopener" target="_blank">Telegram</a></li><li><a href="{CFG["whatsapp"]}" rel="noopener" target="_blank">WhatsApp</a></li><li><a href="{CFG["max"]}" rel="noopener" target="_blank">Max</a></li></ul></div>')
        legal = (f'<p>Исполнитель: самозанятый {CFG["person_full"]}{inn}. Москва. Сайт носит информационный характер и не является публичной офертой.</p>'
                 f'<p><b>Условия.</b> Внесение предоплаты {CFG["prepay"]:,} ₽ означает согласие с <a href="/terms/">условиями работы</a>: одностраничный сайт изготавливается за 3 дня. Если материалы не переданы вовремя, проект всё равно закрывается через 3 дня, а оставшаяся сумма оплачивается по сроку.</p>'
                 f'<p>© <span data-year>{datetime.date.today().year}</span> DMITRY·WEB · <a href="{priv}">Политика конфиденциальности</a> · <a href="/terms/">Условия работы</a></p>').replace(f"{CFG['prepay']:,}", f"{CFG['prepay']:,}".replace(",", " "))
    else:
        cols = (f'<div><a class="logo" href="/en/" style="margin-bottom:14px">{LOGO}<span>DMITRY·WEB</span></a><p>Websites built from scratch, turnkey. Landing page in 3 days, online stores, AI product cards for marketplaces. Moscow and worldwide, Russian and English.</p></div>'
                '<div><h4>Services</h4><ul><li><a href="/en/#services">Landing page — 15,000 ₽</a></li><li><a href="/en/#services">Online store from 55,000 ₽</a></li><li><a href="/en/#services">AI product cards — 350 ₽</a></li><li><a href="/en/#quiz">Price calculator</a></li></ul></div>'
                '<div><h4>Pages</h4><ul><li><a href="/blog/">Blog (Russian)</a></li><li><a href="/cities/">Cities (Russian)</a></li><li><a href="/en/privacy/">Privacy policy</a></li><li><a href="/">Русский</a></li></ul></div>'
                f'<div><h4>Contacts</h4><ul><li><a href="tel:{CFG["phone"]}">{CFG["phone_view"]}</a></li><li><a href="mailto:{CFG["email"]}">{CFG["email"]}</a></li><li><a href="{CFG["telegram"]}" rel="noopener" target="_blank">Telegram</a></li><li><a href="{CFG["whatsapp"]}" rel="noopener" target="_blank">WhatsApp</a></li><li><a href="{CFG["max"]}" rel="noopener" target="_blank">Max</a></li></ul></div>')
        legal = (f'<p>Contractor: self-employed {CFG["person_full"]}{inn}, Moscow. This site is informational and is not a public offer.</p>'
                 f'<p><b>Terms.</b> Paying the 5,000 ₽ prepayment means you accept the terms: a one-page website is delivered in 3 days. If materials are not provided on time, the project is still closed on day 3 and the remaining amount becomes due.</p>'
                 f'<p>© <span data-year>{datetime.date.today().year}</span> DMITRY·WEB · <a href="{priv}">Privacy policy</a></p>')
    return f'<footer class="ftr"><div class="wrap"><div class="ftr-g">{cols}</div><div class="legal">{legal}</div></div></footer>'

PRELOADER = ('<div id="pre" role="status" aria-label="Загрузка"><canvas aria-hidden="true"></canvas><div class="pre-c">'
  '<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M9 7h15a17 17 0 0 1 0 34H9z"/><rect x="20" y="20" width="8" height="8"/></svg>'
  '<div class="pre-t">DMITRY·WEB</div><div class="pre-l"><i></i></div></div></div>'
  '<script>(function(){var p=document.getElementById("pre");if(!p)return;var c=p.querySelector("canvas"),x=c.getContext("2d"),W,H,cols,dr,run=1,S=performance.now();'
  'function rs(){W=c.width=innerWidth;H=c.height=innerHeight;cols=Math.ceil(W/16);dr=[];for(var i=0;i<cols;i++)dr[i]=Math.random()*-60}rs();addEventListener("resize",rs);'
  'var ch="01{}<>/=;:+*#";function fr(){if(!run)return;x.fillStyle="rgba(0,0,0,.14)";x.fillRect(0,0,W,H);x.font="14px monospace";for(var i=0;i<cols;i++){var t=ch[Math.random()*ch.length|0];x.fillStyle=Math.random()>.97?"#fff":"rgba(255,255,255,.35)";x.fillText(t,i*16,dr[i]*16);if(dr[i]*16>H&&Math.random()>.975)dr[i]=0;dr[i]+=.6}requestAnimationFrame(fr)}'
  'fr();function off(){var w=Math.max(0,1100-(performance.now()-S));setTimeout(function(){p.classList.add("off");try{sessionStorage.setItem("pre","1")}catch(e){}setTimeout(function(){run=0;p.remove()},650)},w)}'
  'if(document.readyState==="complete")off();else addEventListener("load",off);setTimeout(off,4500)})();</script>')

HEAD_JS = ('<script>(function(d){d.className+=" js";var s=0;try{s=sessionStorage.getItem("pre")}catch(e){}'
           'if(s||matchMedia("(prefers-reduced-motion:reduce)").matches)d.className+=" nopre"})(document.documentElement)</script>')

def metrika():
    mid = CFG.get("metrika_id")
    if not mid: return ""
    return ('<script>(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();'
            'for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})'
            f'(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym({mid},"init",{{clickmap:true,trackLinks:true,accurateTrackBounce:true}});</script>'
            f'<noscript><div><img src="https://mc.yandex.ru/watch/{mid}" style="position:absolute;left:-9999px" alt=""></div></noscript>')

def page(lang, path, title, desc, body, schemas=(), alts=None, og_img="/assets/img/og-image.jpg", og_alt=None, noindex=False,
         preload="", og_type="website", extra_head="", has_pre=True, art=None):
    """alts: {'ru': '/', 'en': '/en/'} -> hreflang; alt switch url computed"""
    canon = url(path)
    hl = ""
    if alts:
        for l, p in alts.items(): hl += f'<link rel="alternate" hreflang="{l}" href="{url(p)}">'
        hl += f'<link rel="alternate" hreflang="x-default" href="{url(alts.get("ru", path))}">'
    alt_url = (alts or {}).get("en" if lang == "ru" else "ru", "/en/" if lang == "ru" else "/")
    robots = "noindex,follow" if noindex else "index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"
    ver = ""
    vm = ""
    if CFG.get("yandex_verification"): vm += f'<meta name="yandex-verification" content="{E(CFG["yandex_verification"])}">'
    if CFG.get("google_verification"): vm += f'<meta name="google-site-verification" content="{E(CFG["google_verification"])}">'
    locale = "ru_RU" if lang == "ru" else "en_US"
    og_alt = og_alt or title
    artmeta = ""
    if art:
        artmeta = (f'<meta property="article:published_time" content="{art["pub"]}"><meta property="article:modified_time" content="{art["mod"]}">'
                   f'<meta property="article:author" content="{SITE}/#person"><meta property="article:section" content="{E(art["section"])}">')
    cfgjson = json.dumps({"endpoint": CFG["form_endpoint"], "telegram": CFG["telegram"], "metrika": CFG.get("metrika_id") or None}, ensure_ascii=False)
    h = (f'<!doctype html><html lang="{lang}" prefix="og: https://ogp.me/ns#"><head><meta charset="utf-8">'
         f'<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
         f'<title>{E(title)}</title><meta name="description" content="{E(desc)}">'
         f'<link rel="canonical" href="{canon}"><meta name="robots" content="{robots}">{hl}{vm}'
         f'<meta name="theme-color" content="#0a0a0a"><meta name="color-scheme" content="dark"><meta name="author" content="Дмитрий">'
         f'<meta property="og:type" content="{og_type}"><meta property="og:site_name" content="DMITRY·WEB"><meta property="og:locale" content="{locale}">'
         f'<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{canon}">'
         f'<meta property="og:image" content="{SITE}{og_img}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{E(og_alt)}">{artmeta}'
         f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{E(title)}"><meta name="twitter:description" content="{E(desc)}"><meta name="twitter:image" content="{SITE}{og_img}">'
         f'<link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg"><link rel="apple-touch-icon" href="/assets/icons/icon-180.png">'
         f'<link rel="manifest" href="/site.webmanifest">'
         f'<link rel="preload" href="/assets/fonts/inter-400.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="/assets/fonts/inter-700.woff2" as="font" type="font/woff2" crossorigin>{preload}'
         f'<link rel="stylesheet" href="/assets/style.css?v={VER_CSS}">{HEAD_JS}{extra_head}{"".join(jl(s) for s in schemas)}</head>')
    b = (f'<body><a class="skip" href="#main">{"К содержанию" if lang == "ru" else "Skip to content"}</a>{PRELOADER if has_pre else ""}'
         f'{header(lang, alt_url)}<main id="main">{body}</main>{footer(lang)}{fab(lang)}'
         f'<script type="application/json" id="cfg">{cfgjson}</script><script src="/assets/app.js?v={VER_JS}" defer></script>{metrika()}</body></html>')
    return h + b

def write(path, content):
    fp = os.path.join(OUT, path.lstrip("/"))
    if path.endswith("/"): fp = os.path.join(fp, "index.html")
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, "w", encoding="utf-8").write(content)
