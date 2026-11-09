# -*- coding: utf-8 -*-
"""Уникальные обложки для статей по нишам (27 ниш x 4 типа): python3 tools/gen_article_covers.py [--only slug-prefix]
Рисует assets/img/cover-<ниша>-<тип>-(480|800|1200).(jpg|webp|avif) и подставляет их в статьи, карточки, OG и JSON-LD."""
import os, re, sys, glob, asyncio, html, hashlib
from PIL import Image
from playwright.async_api import async_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = "file://" + os.path.join(ROOT, "assets/fonts")
TMP = os.environ.get("COVER_TMP", "/tmp")
E = html.escape
os.chdir(ROOT)

TYPES = {
 "zachem":    ("ЗАЧЕМ НУЖЕН", "Зачем нужен и что даёт бизнесу", "зачем нужен сайт", "Обложка статьи «%s: зачем нужен сайт» — воронка от посетителей к клиентам"),
 "struktura": ("СТРУКТУРА", "Какие блоки и в каком порядке", "структура сайта", "Обложка статьи «%s: структура сайта» — схема блоков страницы"),
 "stoimost":  ("СТОИМОСТЬ", "Сколько стоит и из чего складывается цена", "сколько стоит сайт", "Обложка статьи «%s: сколько стоит сайт» — цена и состав стоимости"),
 "seo":       ("SEO", "Как попасть в Яндекс и Google", "SEO-продвижение сайта", "Обложка статьи «%s: SEO-продвижение» — схема поисковой выдачи"),
}
ACC = ["#ff7a45", "#36d6a3", "#5b8cff", "#f5c542", "#c77dff", "#ff5d8f", "#4ad0e8", "#9be15d"]

def niches():
    s = open("blog/index.html", encoding="utf-8").read()
    out = []
    for m in re.finditer(r'data-f="([a-z0-9-]+)" aria-pressed="false">([^<]+)</button>', s):
        if m.group(1) not in ("guide", "all"): out.append((m.group(1), m.group(2)))
    return out

def accent(slug): return ACC[int(hashlib.md5(slug.encode()).hexdigest(), 16) % len(ACC)]

CSS = """
@font-face{font-family:Onest;src:url(%(f)s/onest-cyrillic-wght-normal.woff2);font-weight:100 900;unicode-range:U+0400-04FF,U+2116,U+20BD}
@font-face{font-family:Onest;src:url(%(f)s/onest-latin-wght-normal.woff2);font-weight:100 900;unicode-range:U+0000-00FF,U+2013-2014,U+2019,U+201C-201D}
@font-face{font-family:Unb;src:url(%(f)s/unbounded-cyrillic-wght-normal.woff2);font-weight:200 900;unicode-range:U+0400-04FF,U+2116,U+20BD}
@font-face{font-family:Unb;src:url(%(f)s/unbounded-latin-wght-normal.woff2);font-weight:200 900;unicode-range:U+0000-00FF,U+2013-2014}
*{box-sizing:border-box;margin:0;padding:0}
body{width:1200px;height:655px;overflow:hidden;background:#0a0a0a;color:#fff;font-family:Onest,sans-serif;position:relative}
.ph{position:absolute;inset:0;background-size:cover;background-position:center}
.sh{position:absolute;inset:0}
.logo{position:absolute;left:60px;top:48px;display:flex;align-items:center;gap:12px;font-family:Unb;font-weight:600;font-size:17px;letter-spacing:.06em}
.logo svg{width:32px;height:32px}
.tag{position:absolute;left:60px;top:132px;font-size:15px;letter-spacing:.22em;font-weight:600;color:#0a0a0a;background:var(--a);border-radius:30px;padding:9px 18px}
h1{position:absolute;left:60px;top:190px;width:620px;font-family:Unb;font-weight:600;font-size:50px;line-height:1.13;letter-spacing:-.01em}
.sub{position:absolute;left:60px;top:%(subtop)spx;width:560px;font-size:23px;line-height:1.38;color:#d4d4d4}
.chips{position:absolute;left:60px;bottom:50px;display:flex;gap:12px}
.chips span{font-size:17px;padding:10px 19px;border-radius:30px;border:1px solid #666;color:#fff;background:rgba(10,10,10,.5)}
.chips span:first-child{background:#fff;color:#0a0a0a;border-color:#fff;font-weight:650}
.panel{position:absolute;left:712px;top:50%%;transform:translateY(-50%%);width:428px;min-height:400px;border-radius:28px;background:rgba(14,14,14,.88);border:1px solid #333;padding:26px 28px;box-shadow:0 30px 70px rgba(0,0,0,.5);backdrop-filter:blur(6px)}
.pt{font-size:14px;letter-spacing:.18em;color:#9a9a9a;margin-bottom:20px}
.bar{height:62px;border-radius:14px;margin-bottom:14px;display:flex;align-items:center;padding:0 20px;font-weight:650;font-size:19px;color:#0a0a0a}
.row{display:flex;align-items:center;gap:12px;border:1px solid #333;border-radius:14px;padding:14px 16px;margin-bottom:11px;font-size:18px;background:#161616}
.row i{width:34px;height:34px;border-radius:10px;background:var(--a);display:block;flex:none}
.row b{font-weight:600}
.big{font-family:Unb;font-weight:600;font-size:44px;margin:6px 0 4px}
.seg{display:flex;height:46px;border-radius:12px;overflow:hidden;margin:20px 0 14px}
.seg div{display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:650;color:#0a0a0a}
.lg{display:flex;flex-wrap:wrap;gap:8px 14px;font-size:16px;color:#bbb}
.lg span:before{content:"";display:inline-block;width:10px;height:10px;border-radius:3px;background:var(--c);margin-right:8px}
.sb{border:1px solid #444;border-radius:30px;padding:13px 20px;font-size:18px;color:#ddd;margin-bottom:16px;background:#151515}
.res{border-radius:14px;padding:13px 16px;margin-bottom:10px;border:1px solid #2a2a2a;background:#141414}
.res u{display:block;text-decoration:none;font-size:14px;color:#888;margin-bottom:3px}
.res b{display:block;font-size:17px;font-weight:600}
.res.me{border-color:var(--a);background:#1b1b1b}
.res.me u{color:var(--a)}
.up{margin-top:16px;text-align:right;font-size:15px;color:var(--a);letter-spacing:.06em}
"""

def panel(t, label, acc):
    if t == "zachem":
        w = [("Посетители сайта", 100, "#fff"), ("Заявки и звонки", 72, acc), ("Клиенты", 46, "#fff")]
        inner = '<div class="pt">ВОРОНКА</div>' + "".join('<div class="bar" style="width:%d%%;background:%s">%s</div>' % (p, c, E(n)) for n, p, c in w)
        inner += '<div style="margin-top:22px;font-size:18px;color:#bbb;line-height:1.5">Сайт собирает обращения круглосуточно, пока вы заняты делом.</div>'
    elif t == "struktura":
        blocks = ["Главный экран и кнопка заявки", "Услуги и цены", "Преимущества", "Примеры работ", "Отзывы", "Контакты и карта"]
        inner = '<div class="pt">БЛОКИ СТРАНИЦЫ</div>' + "".join('<div class="row"><i style="opacity:%.2f"></i><b>%s</b></div>' % (1 - k * .1, E(b)) for k, b in enumerate(blocks))
    elif t == "stoimost":
        inner = ('<div class="pt">ЛЕНДИНГ ПОД КЛЮЧ</div><div class="big">15 000 ₽</div><div style="color:#bbb;font-size:18px">3 дня, предоплата 5 000 ₽</div>'
                 '<div class="seg"><div style="width:34%%;background:%s">Дизайн</div><div style="width:26%%;background:#fff">Вёрстка</div><div style="width:22%%;background:#bbb">SEO</div><div style="width:18%%;background:#777">Формы</div></div>'
                 '<div class="lg"><span style="--c:%s">дизайн под нишу</span><span style="--c:#fff">адаптив</span><span style="--c:#bbb">SEO-основа</span><span style="--c:#777">заявки в Telegram</span></div>'
                 '<div style="margin-top:22px;border-top:1px solid #333;padding-top:16px;font-size:17px;color:#bbb">Интернет-магазин — от 35 000 ₽</div>') % (acc, acc)
    else:
        inner = ('<div class="pt">ПОИСК</div><div class="sb">%s</div>'
                 '<div class="res"><u>конкурент.ru</u><b>Первый результат в выдаче</b></div>'
                 '<div class="res me"><u>ваш-сайт.ru</u><b>%s — цены, примеры, заявка</b></div>'
                 '<div class="res"><u>другой-сайт.ru</u><b>Следующий результат</b></div>'
                 '<div class="up">▲ рост по запросам</div>') % (E(label.lower()), E(label))
    return '<div class="panel">' + inner + "</div>"

def page(slug, label, t, photo=False):
    acc = accent(slug)
    tag, tagline, _, _ = TYPES[t]
    nlines = 2 if len(label) > 17 else 1
    subtop = 190 + nlines * 58 + 18 + (0 if len(label) <= 34 else 58)
    bg = ""
    if photo:
        bg = '<div class="ph" style="background-image:url(file://%s)"></div><div class="sh" style="background:linear-gradient(90deg,rgba(10,10,10,.94) 0,rgba(10,10,10,.85) 48%%,rgba(10,10,10,.35) 100%%)"></div>' % os.path.join(ROOT, "assets/img/niche-%s-1200.jpg" % slug)
    else:
        bg = ('<div class="sh" style="background:radial-gradient(520px 420px at 18%% 12%%,%s33,transparent 70%%),radial-gradient(600px 500px at 90%% 100%%,%s22,transparent 70%%)"></div>'
              '<svg class="sh" viewBox="0 0 1200 655">%s</svg>') % (acc, acc, "".join('<line x1="%d" y1="0" x2="%d" y2="655" stroke="#fff" stroke-opacity=".035"/>' % (x, x) for x in range(0, 1200, 60)))
    logo = '<div class="logo"><svg viewBox="0 0 48 48"><path d="M9 7h15a17 17 0 0 1 0 34H9z" fill="none" stroke="#fff" stroke-width="4"/><rect x="20" y="20" width="8" height="8" fill="#fff"/></svg>DMITRY·WEB</div>'
    css = (CSS % {"f": FONTS, "subtop": subtop})
    chips = "".join("<span>%s</span>" % c for c in ("Лендинг 15 000 ₽", "3 дня", "Под ключ"))
    return ('<!doctype html><html><head><meta charset=utf-8><style>%s</style></head><body style="--a:%s">%s%s<div class="tag">%s</div><h1>%s</h1><div class="sub">%s</div><div class="chips">%s</div>%s</body></html>'
            % (css, acc, bg, logo, E(tag), E(label), E(tagline), chips, panel(t, label, acc)))

def save_sizes(png, base):
    im = Image.open(png).convert("RGB")
    for w in (1200, 800, 480):
        r = im if w == 1200 else im.resize((w, round(w * 655 / 1200)), Image.LANCZOS)
        p = "assets/img/%s-%d" % (base, w)
        r.save(p + ".jpg", quality=84, optimize=True, progressive=True)
        r.save(p + ".webp", quality=82, method=6)
        r.save(p + ".avif", quality=58, speed=8)

async def render(only):
    done = []
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1200, "height": 655})
        for slug, label in niches():
            if only and not slug.startswith(only): continue
            photo = os.path.exists("assets/img/niche-%s-1200.jpg" % slug)
            for t in TYPES:
                f = os.path.join(TMP, "c-%s-%s.html" % (slug, t))
                open(f, "w", encoding="utf-8").write(page(slug, label, t, photo))
                await pg.goto("file://" + f); await pg.wait_for_timeout(350)
                png = f.replace(".html", ".png"); await pg.screenshot(path=png)
                save_sizes(png, "cover-%s-%s" % (slug, t)); done.append((slug, t))
        await b.close()
    return done

BASE = re.compile(r"(?:case|blog|service|niche|cover)-[a-z0-9-]+?-(480|800|1200)\b")

def patch(only):
    labels = dict(niches()); n = 0
    for f in glob.glob("**/*.html", recursive=True):
        s = open(f, encoding="utf-8").read(); o = s
        def card(m):
            slug, t = m.group(1), m.group(2)
            if slug not in labels or (only and not slug.startswith(only)): return m.group(0)
            seg = BASE.sub(lambda x: "cover-%s-%s-%s" % (slug, t, x.group(1)), m.group(0))
            return re.sub(r'\balt="[^"]*"', lambda _: 'alt="%s"' % (TYPES[t][3] % labels[slug]).replace('"', "'"), seg)
        s = re.sub(r'<a class="card post rv" href="/blog/([a-z0-9-]+)-sayt-(zachem|struktura|stoimost|seo)/"[^>]*>.*?</a>', card, s, flags=re.S)
        m = re.match(r"blog/([a-z0-9-]+)-sayt-(zachem|struktura|stoimost|seo)/index\.html$", f)
        if m and m.group(1) in labels and not (only and not m.group(1).startswith(only)):
            slug, t = m.groups()
            i = s.index('<figure class="cover">'); j = s.index("</figure>", i)
            seg = BASE.sub(lambda x: "cover-%s-%s-%s" % (slug, t, x.group(1)), s[i:j])
            seg = re.sub(r'\balt="[^"]*"', lambda _: 'alt="%s"' % (TYPES[t][3] % labels[slug]).replace('"', "'"), seg)
            s = s[:i] + seg + s[j:]
            img = "https://dmitry-web.ru/assets/img/cover-%s-%s-1200.jpg" % (slug, t)
            s = re.sub(r'(<meta property="og:image" content=")[^"]*', lambda x: x.group(1) + img, s)
            s = re.sub(r'(<meta name="twitter:image" content=")[^"]*', lambda x: x.group(1) + img, s)
            s = re.sub(r'(og:image:alt" content=")[^"]*', lambda x: x.group(1) + (TYPES[t][3] % labels[slug]).replace('"', "'"), s)
            s = re.sub(r'"image":\["[^"]+"\]', '"image":["%s"]' % img, s, 1)
        if s != o: open(f, "w", encoding="utf-8").write(s); n += 1
    return n

if __name__ == "__main__":
    only = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else ""
    if "--patch-only" not in sys.argv:
        d = asyncio.run(render(only)); print("rendered", len(d))
    print("patched files", patch(only))
