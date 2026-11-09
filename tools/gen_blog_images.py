# -*- coding: utf-8 -*-
"""Рендер обложек и инфографики для экспертных статей: python3 tools/gen_blog_images.py
Результат: assets/img/guide-<slug>-(cover|info)-(480|800|1200).(jpg|webp|avif)"""
import os, sys, asyncio, html
sys.path.insert(0, os.path.dirname(__file__))
from blog_guides_data import ARTICLES
from PIL import Image
from playwright.async_api import async_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = "file://" + os.path.join(ROOT, "assets/fonts")
TMP = os.environ.get("GUIDE_TMP", "/tmp")
E = html.escape

CSS = """
@font-face{font-family:Onest;src:url(%(f)s/onest-cyrillic-wght-normal.woff2);font-weight:100 900;unicode-range:U+0400-04FF,U+2116,U+20BD}
@font-face{font-family:Onest;src:url(%(f)s/onest-latin-wght-normal.woff2);font-weight:100 900;unicode-range:U+0000-00FF,U+2013-2014,U+2019,U+201C-201D}
@font-face{font-family:Unb;src:url(%(f)s/unbounded-cyrillic-wght-normal.woff2);font-weight:200 900;unicode-range:U+0400-04FF,U+2116,U+20BD}
@font-face{font-family:Unb;src:url(%(f)s/unbounded-latin-wght-normal.woff2);font-weight:200 900;unicode-range:U+0000-00FF,U+2013-2014}
*{box-sizing:border-box;margin:0;padding:0}
body{width:1200px;height:655px;overflow:hidden;background:#0a0a0a;color:#fff;font-family:Onest,sans-serif;position:relative}
.bg{position:absolute;inset:0}
.logo{position:absolute;left:64px;top:52px;display:flex;align-items:center;gap:12px;font-family:Unb;font-weight:600;font-size:18px;letter-spacing:.06em}
.logo svg{width:34px;height:34px}
.eb{position:absolute;right:64px;top:56px;font-size:15px;letter-spacing:.22em;color:#c9c9c9;border:1px solid #3a3a3a;border-radius:30px;padding:9px 18px}
h1{position:absolute;left:64px;top:170px;width:690px;font-family:Unb;font-weight:600;font-size:52px;line-height:1.14;letter-spacing:-.01em}
.chips{position:absolute;left:64px;bottom:58px;display:flex;gap:12px;flex-wrap:wrap;width:760px}
.chips span{font-size:18px;padding:11px 20px;border-radius:30px;background:#fff;color:#0a0a0a;font-weight:600}
.chips span:nth-child(n+2){background:transparent;color:#fff;border:1px solid #555;font-weight:500}
""" % {"f": FONTS}

LOGO = '<div class="logo"><svg viewBox="0 0 48 48"><path d="M9 7h15a17 17 0 0 1 0 34H9z" fill="none" stroke="#fff" stroke-width="4"/><rect x="20" y="20" width="8" height="8" fill="#fff"/></svg>DMITRY·WEB</div>'

MOTIF = {
 "rings": '<svg class="bg" viewBox="0 0 1200 655"><defs><radialGradient id="g" cx="50%" cy="50%"><stop offset="0" stop-color="#fff" stop-opacity=".18"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient></defs><circle cx="930" cy="360" r="330" fill="url(#g)"/>' + "".join('<circle cx="930" cy="360" r="%d" fill="none" stroke="#fff" stroke-opacity="%.2f" stroke-width="1.5"/>' % (r, o) for r, o in [(70,.9),(130,.6),(200,.4),(280,.25),(370,.14)]) + '<circle cx="930" cy="360" r="14" fill="#fff"/></svg>',
 "grid": '<svg class="bg" viewBox="0 0 1200 655">' + "".join('<line x1="%d" y1="0" x2="%d" y2="655" stroke="#fff" stroke-opacity=".07"/>' % (x, x) for x in range(780, 1200, 60)) + "".join('<line x1="780" y1="%d" x2="1200" y2="%d" stroke="#fff" stroke-opacity=".07"/>' % (y, y) for y in range(0, 655, 60)) + '<rect x="840" y="180" width="260" height="260" rx="22" fill="none" stroke="#fff" stroke-width="3"/><rect x="900" y="240" width="140" height="140" rx="14" fill="#fff"/><circle cx="1100" cy="180" r="10" fill="#fff"/></svg>',
 "bars": '<svg class="bg" viewBox="0 0 1200 655">' + "".join('<rect x="%d" y="%d" width="52" height="%d" rx="8" fill="#fff" fill-opacity="%.2f"/>' % (800 + i * 74, 520 - hh, hh, .25 + i * .15) for i, hh in enumerate([120, 200, 290, 380])) + '<path d="M800 430 L874 360 L948 300 L1022 210 L1096 140" stroke="#fff" stroke-width="3" fill="none"/><circle cx="1096" cy="140" r="11" fill="#fff"/></svg>',
 "split": '<svg class="bg" viewBox="0 0 1200 655"><rect x="800" y="150" width="150" height="300" rx="16" fill="none" stroke="#fff" stroke-width="3"/>' + "".join('<rect x="816" y="%d" width="118" height="26" rx="6" fill="#fff" fill-opacity="%.2f"/>' % (170 + i * 46, .9 - i * .12) for i in range(5)) + '<rect x="980" y="150" width="150" height="300" rx="16" fill="none" stroke="#fff" stroke-width="3"/>' + "".join('<rect x="%d" y="%d" width="52" height="52" rx="8" fill="#fff" fill-opacity=".55"/>' % (996 + (i % 2) * 66, 172 + (i // 2) * 66) for i in range(6)) + '</svg>',
 "pin": '<svg class="bg" viewBox="0 0 1200 655">' + "".join('<circle cx="940" cy="360" r="%d" fill="none" stroke="#fff" stroke-opacity="%.2f" stroke-width="1.5" stroke-dasharray="4 8"/>' % (r, o) for r, o in [(120,.5),(200,.3),(290,.16)]) + '<path d="M940 190c-62 0-110 48-110 108 0 82 110 190 110 190s110-108 110-190c0-60-48-108-110-108z" fill="#fff"/><circle cx="940" cy="298" r="40" fill="#0a0a0a"/></svg>',
}

def cover_html(a):
    c = a["cover"]
    return "<!doctype html><html><head><meta charset=utf-8><style>%s</style></head><body>%s%s<div class=eb>%s</div><h1>%s</h1><div class=chips>%s</div></body></html>" % (
        CSS, MOTIF[c["motif"]], LOGO, E(c["eyebrow"]), E(c["title"]), "".join("<span>%s</span>" % E(x) for x in c["chips"]))

INFO_CSS = """
.t{position:absolute;left:64px;top:132px;font-family:Unb;font-weight:600;font-size:40px;line-height:1.15;width:1000px}
.grid{position:absolute;left:64px;right:64px;top:240px;display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.it{background:#141414;border:1px solid #2c2c2c;border-radius:20px;padding:22px 24px;height:162px;position:relative}
.it b{display:block;font-size:23px;font-weight:650;margin:10px 0 8px;line-height:1.2}
.it span{font-size:17px;color:#b8b8b8;line-height:1.35}
.n{font-family:Unb;font-size:15px;color:#0a0a0a;background:#fff;border-radius:50%;width:34px;height:34px;display:flex;align-items:center;justify-content:center;font-weight:700}
.foot{position:absolute;left:64px;bottom:34px;color:#8a8a8a;font-size:15px;letter-spacing:.08em}
"""

def info_html(a):
    i = a["info"]
    items = "".join('<div class=it><div class=n>%d</div><b>%s</b><span>%s</span></div>' % (k + 1, E(t), E(d)) for k, (t, d) in enumerate(i["items"]))
    return "<!doctype html><html><head><meta charset=utf-8><style>%s%s</style></head><body>%s<div class=eb>ИНФОГРАФИКА</div><div class=t>%s</div><div class=grid>%s</div><div class=foot>dmitry-web.ru</div></body></html>" % (CSS, INFO_CSS, LOGO, E(i["title"]), items)

def save_sizes(png, base):
    im = Image.open(png).convert("RGB")
    for w in (1200, 800, 480):
        r = im if w == 1200 else im.resize((w, round(w * 655 / 1200)), Image.LANCZOS)
        p = os.path.join(ROOT, "assets/img/%s-%d" % (base, w))
        r.save(p + ".jpg", quality=86, optimize=True, progressive=True)
        r.save(p + ".webp", quality=84, method=6)
        r.save(p + ".avif", quality=62)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1200, "height": 655})
        for a in ARTICLES:
            for kind, fn in (("cover", cover_html), ("info", info_html)):
                f = os.path.join(TMP, "g-%s-%s.html" % (a["slug"], kind))
                open(f, "w", encoding="utf-8").write(fn(a))
                await pg.goto("file://" + f); await pg.wait_for_timeout(500)
                png = f.replace(".html", ".png"); await pg.screenshot(path=png)
                save_sizes(png, "guide-%s-%s" % (a["slug"], kind))
            print("ok", a["slug"])
        await b.close()

asyncio.run(main())
