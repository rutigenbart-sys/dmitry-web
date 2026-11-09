# -*- coding: utf-8 -*-
"""Генератор экспертных статей блога: python3 tools/gen_blog_guides.py  (сначала tools/gen_blog_images.py)
Создаёт /blog/<slug>/index.html, карточки в /blog/index.html, записи в sitemap.xml."""
import os, re, sys, html, json
sys.path.insert(0, os.path.dirname(__file__))
import gen_restaurant_articles as G
from blog_guides_data import ARTICLES

ROOT, SITE, TODAY = G.ROOT, G.SITE, "2026-11-09"
read, write, esc, eq = G.read, G.write, G.esc, G.eq
SZ = 'sizes="(max-width:1020px) 100vw, 720px"'
SZC = 'sizes="(max-width:680px) 100vw, (max-width:1020px) 50vw, 380px"'

def pic(base, alt, w=1200, h=655, sizes=SZ, lazy=True, ws=(480, 800, 1200), card=False):
    ss = lambda ext: ", ".join("/assets/img/%s-%d.%s %dw" % (base, x, ext, x) for x in ws)
    big = ws[-1]
    attrs = 'loading="lazy"' if lazy else 'fetchpriority="high"'
    return ('<picture><source type="image/avif" srcset="%s" %s><source type="image/webp" srcset="%s" %s>'
            '<img src="/assets/img/%s-%d.jpg" srcset="%s" %s width="%d" height="%d" alt="%s" %s decoding="async" ></picture>') % (
        ss("avif"), sizes, ss("webp"), sizes, base, big, ss("jpg"), sizes, w, h, eq(alt), attrs)

def card(a, other=False):
    return ('<a class="card post rv" href="/blog/%s/" data-niche="guide">%s<div class="in"><span class="k">Руководство</span><h3>%s</h3><p>%s</p></div></a>' % (
        a["slug"], pic("guide-%s-cover" % a["slug"], a["alt_cover"], 800, 436, SZC, True, (480, 800)), esc(a["title"]), esc(a["desc"][:118].rsplit(" ", 1)[0] + "…")))

def build(a):
    slug = a["slug"]; url = "%s/blog/%s/" % (SITE, slug)
    secs = a["sections"]
    body = "<figure class=\"cover\">" + pic("guide-%s-cover" % slug, a["alt_cover"], lazy=False) + "</figure>"
    body += "<p><b>%s</b></p>" % esc(a["desc"])
    for k, (sid, h2, inner) in enumerate(secs):
        body += '<h2 id="%s">%s</h2>%s' % (sid, esc(h2), inner)
        if k == 0:
            body += '<figure class="cover" style="margin:1.6em 0">' + pic("guide-%s-info" % slug, a["info"]["alt"]) + "</figure>"
        if k == 1:
            body += '<div class="inline-cta"><p>Хотите узнать цену для вашего проекта? Рассчитайте её за минуту и зафиксируйте предоплатой.</p><a class="btn" href="/#quiz">Рассчитать стоимость</a></div>'
    body += '<h2 id="faq">Частые вопросы</h2><div class="faq">' + "".join("<details><summary>%s</summary><p>%s</p></details>" % (esc(q), esc(t)) for q, t in a["faq"]) + "</div>"
    body += '<p>Сайт под ключ: лендинг — 15 000 ₽ за 3 дня, интернет-магазин — от 35 000 ₽. Подробности на странице <a href="/#services">услуг и цен</a> и в <a href="/terms/">условиях работы</a>.</p>'
    words = len(re.sub(r"<[^>]+>", " ", body).split())
    toc = [(s[0], s[1]) for s in secs] + [("faq", "Частые вопросы")]
    aside = ('<aside class="aside"><nav class="card toc" aria-label="Содержание статьи"><b>Содержание</b><ol>' + "".join('<li><a href="#%s">%s</a></li>' % (i, esc(t)) for i, t in toc) +
             '</ol></nav><div class="cta"><h3>Сайт за 3 дня под ключ</h3><p>Лендинг — 15 000 ₽, интернет-магазин — от 35 000 ₽. Скрытых платежей нет.</p><a class="btn" href="/#quiz">Рассчитать стоимость</a></div></aside>')
    others = [x for x in ARTICLES if x["slug"] != slug]
    start = ARTICLES.index(a)
    rel = [ARTICLES[(start + i) % len(ARTICLES)] for i in (1, 2, 3)]
    related = '<section class="rel"><div class="wrap"><h2 style="font-size:clamp(24px,3vw,34px)">Читайте также</h2><div class="g3" style="margin-top:24px">' + "".join(card(x) for x in rel) + "</div></div></section>"
    crumbs = '<nav class="crumbs wrap" aria-label="Хлебные крошки"><ol><li><a href="/">Главная</a></li><li><a href="/blog/">Блог</a></li><li aria-current="page">%s</li></ol></nav>' % esc(a["short"])
    meta = ('<div class="wrap art-h"><span class="tag">Руководство</span><h1>%s</h1><div class="meta"><span>Автор: Дмитрий, веб-разработчик, опыт 10 лет</span>'
            '<span>Обновлено: <time datetime="%s">9 ноября 2026</time></span><span>Чтение: %d мин</span></div></div>' % (esc(a["title"]), TODAY, max(3, round(words / 180))))
    main = '<main id="main">' + crumbs + meta + '<div class="wrap art"><article class="prose">' + body + "</article>" + aside + "</div>" + related + "</main>"
    ld = [{"@context": "https://schema.org", "@type": "Article", "@id": url + "#article", "headline": a["title"], "description": a["desc"],
           "image": ["%s/assets/img/guide-%s-cover-1200.jpg" % (SITE, slug), "%s/assets/img/guide-%s-info-1200.jpg" % (SITE, slug)],
           "datePublished": TODAY, "dateModified": TODAY, "inLanguage": "ru", "author": {"@id": SITE + "/#person"}, "publisher": {"@id": SITE + "/#org"},
           "mainEntityOfPage": {"@type": "WebPage", "@id": url}, "articleSection": "Руководство", "wordCount": words, "keywords": a["keywords"]},
          {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": t}} for q, t in a["faq"]]},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": "Главная", "item": SITE + "/"}, {"@type": "ListItem", "position": 2, "name": "Блог", "item": SITE + "/blog/"},
              {"@type": "ListItem", "position": 3, "name": a["title"], "item": url}]}]
    page = G.head(a["title"], a["desc"], url, ld, True, "Руководство") + G.HEADER + main + G.FOOTER
    img = "%s/assets/img/guide-%s-cover-1200.jpg" % (SITE, slug)
    page = page.replace("%s/assets/img/og-image.jpg?v=2" % SITE, img)
    page = re.sub(r'(og:image:alt" content=")[^"]*', lambda m: m.group(1) + eq(a["alt_cover"]), page)
    return page

def main():
    for a in ARTICLES:
        write("blog/%s/index.html" % a["slug"], build(a))
    # индекс блога
    p = "blog/index.html"; s = read(p)
    s = re.sub(r'<a class="card post rv" href="/blog/(%s)/" data-niche="guide">.*?</a>' % "|".join(x["slug"] for x in ARTICLES), "", s, flags=re.S)
    first = s.index('<a class="card post rv"')
    s = s[:first] + "".join(card(a) for a in ARTICLES) + s[first:]
    if 'data-f="guide"' not in s:
        s = s.replace('<button type="button" data-f="all" aria-pressed="true">Все</button>', '<button type="button" data-f="all" aria-pressed="true">Все</button><button type="button" data-f="guide" aria-pressed="false">Руководства</button>', 1)
    s = s.replace("108 практических статей: зачем нужен сайт", "116 статей: 8 руководств и 108 статей по нишам — зачем нужен сайт")
    s = s.replace("Блог о создании сайтов: 108 статей", "Блог о создании сайтов: 116 статей")
    s = s.replace("108 статей про цены", "116 статей про цены")
    write(p, s)
    # sitemap
    sm = read("sitemap.xml"); add = ""
    for a in ARTICLES:
        u = "%s/blog/%s/" % (SITE, a["slug"])
        if "<loc>%s</loc>" % u not in sm:
            add += '<url><loc>%s</loc><lastmod>%s</lastmod><priority>0.7</priority>\n</url>\n' % (u, TODAY)
    if add: write("sitemap.xml", sm.replace("</urlset>", add + "</urlset>"))
    print("guides:", len(ARTICLES), "sitemap +", add.count("<url>"))

if __name__ == "__main__":
    main()
