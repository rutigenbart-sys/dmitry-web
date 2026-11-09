# -*- coding: utf-8 -*-
"""Генератор статей «Сайт для ресторана и кафе в <город>»: python3 tools/gen_restaurant_articles.py
Создаёт /blog/restoran-sayt-<slug-города>/index.html для всех городов из cities_data,
хаб /blog/restoran-sayt-po-gorodam/ и дополняет sitemap.xml. Существующие страницы пересоздаются (идемпотентно)."""
import os, re, sys, hashlib, html, json
sys.path.insert(0, os.path.dirname(__file__))
from cities_data import EXISTING, NEW

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://dmitry-web.ru"
TODAY = "2026-11-09"
TPL = "blog/restoran-sayt-struktura/index.html"   # шаблон шапки/подвала
COVER = "case-restaurant"                            # обложка статей (макет сайта ресторана)

def read(p): return open(os.path.join(ROOT, p), encoding="utf-8").read()
def write(p, s):
    full = os.path.join(ROOT, p); os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(s)
def esc(s): return html.escape(s, quote=False)
def eq(s): return html.escape(s, quote=True)
def h(*parts): return int(hashlib.md5("|".join(map(str, parts)).encode()).hexdigest(), 16)
def pick(slug, key, opts): return opts[h(slug, key) % len(opts)]
def shuf(slug, key, items): return sorted(items, key=lambda m: h(slug, key, m))

TR = dict(zip("абвгдеёжзийклмнопрстуфхцчшщъыьэюя", ["a","b","v","g","d","e","e","zh","z","i","y","k","l","m","n","o","p","r","s","t","u","f","h","ts","ch","sh","sch","","y","","e","yu","ya"]))
def slugify(n):
    out = "".join(TR.get(ch, ch) for ch in n.lower().replace(" ", "-"))
    return re.sub(r"[^a-z0-9-]+", "", out).strip("-")

CITIES = []
for n, loc, reg, fo, pop, tags, slug in EXISTING:
    CITIES.append(dict(name=n, loc=loc, region=reg, fo=fo, pop=pop, tags=tags, slug=slug))
for n, loc, reg, fo, pop, tags in NEW:
    CITIES.append(dict(name=n, loc=loc, region=reg, fo=fo, pop=pop, tags=tags, slug=slugify(n)))
slugs = [c["slug"] for c in CITIES]
assert len(slugs) == len(set(slugs))
assert not {"seo", "stoimost", "struktura", "zachem", "po-gorodam"} & set(slugs)
BY = {c["slug"]: c for c in CITIES}

def size_class(p):
    if p >= 1000: return "mega"
    if p >= 500: return "big"
    if p >= 250: return "mid"
    if p >= 100: return "city"
    return "small"

GROUP = {"tourism": "tour", "resort": "tour", "metal": "ind", "chem": "ind", "mach": "ind", "mining": "ind", "energy": "ind",
         "oil": "ind", "ship": "ind", "defense": "ind", "wood": "ind", "textile": "ind", "auto": "ind",
         "port": "road", "logistics": "road", "agro": "agro", "fishing": "agro", "science": "sci", "trade": "trade"}

# ---------- каркас страницы из существующей статьи ----------
T = read(TPL)
HEADER = T[T.index("<body>"): T.index('<main id="main">')]
FOOTER = T[T.index("</main>"):]
HEAD_PRE = T[: T.index("<title>")]
HEAD_MID = T[T.index('<meta name="theme-color"'): T.index('<meta property="og:type"')]
HEAD_TAIL = T[T.index('<link rel="icon" href="/favicon.ico"'): T.index('<script type="application/ld+json">')]

def head(title, desc, url, ld_blocks, article=True, section="Сайт для ресторана"):
    s = HEAD_PRE + "<title>%s</title>" % esc(title) + '<meta name="description" content="%s">' % eq(desc)
    s += '<link rel="canonical" href="%s">' % url
    s += '<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">'
    s += HEAD_MID
    s += '<meta property="og:type" content="%s"><meta property="og:site_name" content="DMITRY·WEB"><meta property="og:locale" content="ru_RU">' % ("article" if article else "website")
    s += '<meta property="og:title" content="%s"><meta property="og:description" content="%s"><meta property="og:url" content="%s">' % (eq(title), eq(desc), url)
    s += '<meta property="og:image" content="%s/assets/img/og-image.jpg?v=2"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="%s">' % (SITE, eq(title))
    if article:
        s += '<meta property="article:published_time" content="%s"><meta property="article:modified_time" content="%s"><meta property="article:author" content="https://dmitry-web.ru/#person"><meta property="article:section" content="%s">' % (TODAY, TODAY, section)
    s += '<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="%s"><meta name="twitter:description" content="%s"><meta name="twitter:image" content="%s/assets/img/og-image.jpg?v=2">' % (eq(title), eq(desc), SITE)
    s += HEAD_TAIL
    s += "".join('<script type="application/ld+json">' + json.dumps(b, ensure_ascii=False, separators=(",", ":")) + "</script>" for b in ld_blocks)
    return s + "</head>"

def cover_picture(alt, lazy=False):
    sz = 'sizes="(max-width:1020px) 100vw, 720px"'
    return ('<figure class="cover"><picture>'
            '<source type="image/avif" srcset="/assets/img/%(c)s-480.avif 480w, /assets/img/%(c)s-800.avif 800w, /assets/img/%(c)s-1200.avif 1200w" %(sz)s>'
            '<source type="image/webp" srcset="/assets/img/%(c)s-480.webp 480w, /assets/img/%(c)s-800.webp 800w, /assets/img/%(c)s-1200.webp 1200w" %(sz)s>'
            '<img src="/assets/img/%(c)s-1200.jpg" srcset="/assets/img/%(c)s-480.jpg 480w, /assets/img/%(c)s-800.jpg 800w, /assets/img/%(c)s-1200.jpg 1200w" %(sz)s '
            'width="1200" height="655" alt="%(a)s" fetchpriority="high" decoding="async" ></picture></figure>') % dict(c=COVER, sz=sz, a=eq(alt))

def neighbours(c, k=8):
    same_region = [x for x in CITIES if x["region"] == c["region"] and x["slug"] != c["slug"]]
    same_fo = [x for x in CITIES if x["fo"] == c["fo"] and x["region"] != c["region"] and x["slug"] != c["slug"]]
    same_region.sort(key=lambda x: -x["pop"])
    same_fo.sort(key=lambda x: h(c["slug"], x["slug"]))
    out = same_region[:k]
    out += same_fo[: max(0, k - len(out))]
    return out

# ---------- тексты ----------
def build(c):
    N, L, R, slug = c["name"], c["loc"], c["region"], c["slug"]
    sc = size_class(c["pop"])
    LC = L[0].upper() + L[1:]
    url = "%s/blog/restoran-sayt-%s/" % (SITE, slug)
    groups = []
    for t in c["tags"]:
        g = GROUP.get(t)
        if g and g not in groups: groups.append(g)

    title = pick(slug, "title", [
        "Сайт для ресторана и кафе %s: сколько стоит и что на нём разместить" % L,
        "Заказать сайт для ресторана или кафе %s — цена и сроки" % L,
        "Сайт для кафе и ресторана %s под ключ: от 15 000 ₽ за 3 дня" % L])
    desc = pick(slug, "desc", [
        "Сайт для ресторана и кафе %s: меню с ценами, бронь стола, доставка. Лендинг 15 000 ₽ за 3 дня, интернет-магазин от 35 000 ₽. Работаю онлайн." % L,
        "Что нужно сайту ресторана или кафе %s и сколько он стоит: лендинг под ключ — 15 000 ₽, срок 3 дня, SEO и заявки в Telegram внутри." % L,
        "Заказать сайт заведению %s: меню, бронирование столика, доставка и акции. Цена от 15 000 ₽, запуск за 3 дня, предоплата 5 000 ₽." % L])
    if len(desc) > 165: desc = desc[:162].rstrip() + "…"

    intro = {
        "mega": ["%s — город с сотнями кафе и ресторанов, и гость выбирает заведение за считаные секунды: по запросу «ресторан %s» он открывает несколько вкладок и остаётся там, где быстро видит меню, цены и кнопку брони." % (N, N),
                 "Рынок общепита в таком городе, как %s, плотный: рядом с вами десятки конкурентов, а у гостя нет времени разбираться. Побеждает заведение, чей сайт мгновенно открывается на телефоне и сразу отвечает: что в меню, сколько стоит, как попасть." % N],
        "big": ["%s ресторанов и кафе хватает, и гости привыкли выбирать по карточке на карте и сайту. Если на сайте нет актуального меню и цен, человек выберет соседнее заведение, где они есть." % LC,
                "%s — большой город, и люди давно ищут, где поесть, через интернет. Сайт заведения здесь — это меню, бронь стола и доставка в одном месте, а не только визитка." % N],
        "mid": ["%s гости выбирают заведение по отзывам и по сайту: хочется заранее увидеть меню и цены, а не гадать по фото на карте." % LC,
                "%s — достаточно большой город, чтобы у кафе и ресторанов была реальная конкуренция за вечер пятницы, но не такой, чтобы затеряться. Сайт с меню и бронью помогает выделиться." % N],
        "city": ["%s люди выбирают, где поесть, по рекомендациям и по карточке на карте. Сайт добавляет доверия: гость видит меню, цены, фото зала и может позвонить или написать в один клик." % LC,
                 "%s — город, где заведение узнают по репутации, но всё чаще сначала смотрят в телефон. Короткий быстрый сайт с меню и контактами закрывает этот первый шаг." % N],
        "small": ["%s — небольшой город, где многие гости приходят по знакомству. Но приезжие, заказчики банкетов и те, кто ищет доставку, сначала проверяют сайт и карточку на картах." % N,
                  "%s заведений немного, и каждый гость на счету. Сайт с меню, адресом и кнопкой звонка помогает тем, кто ещё не знает вас лично." % LC],
    }[sc]
    p_intro = pick(slug, "intro", intro)

    tour = ["Заметную часть гостей здесь составляют приезжие, поэтому сайт должен работать как путеводитель по вашему заведению: фото зала и блюд, цены, адрес с картой и бронь стола. Для иностранных гостей полезна версия на английском.",
            "Туристический поток — это сезонные пики, и сайт должен выдерживать их без суеты: онлайн-бронь, актуальный график и чёткие правила для групп и банкетов избавляют администратора от потока одинаковых звонков."]
    ind = ["В экономике города сильна промышленность, поэтому у заведений есть постоянная аудитория: рабочие и офисные сотрудники. Бизнес-ланчи, комплексные обеды и доставка в офис удобнее всего продавать через сайт с понятным расписанием и прайсом.",
           "Рядом с предприятиями спрос на обеды стабилен: смены, командировочные, корпоративные заказы. На сайте стоит вынести бизнес-ланч с ценой и временем, а также форму заявки на банкет и кейтеринг."]
    road = ["Через город идёт транзит и деловые поездки, поэтому гости нередко выбирают заведение впервые. Им нужны адрес с маршрутом, режим работы, парковка и честные цены прямо на первом экране.",
            "Для заведений рядом с транспортными маршрутами важны скорость и ясность: человек в пути листает варианты на телефоне и выбирает то, где сразу видно меню и как добраться."]
    agro = ["Город живёт агросектором и пищевой отраслью, а местные гости ценят «своё»: сезонное меню, фермерские продукты, понятное происхождение блюд. Об этом стоит рассказать на сайте — это отличает вас от сетей.",
            "Когда рядом есть производство продуктов, у кухни сильный аргумент: свежее местное сырьё. Покажите его на сайте — в описании блюд и в блоке «о заведении»."]
    sci = ["В городе много студентов, преподавателей и приезжих специалистов: для них важны бизнес-ланчи, понятные цены, вай-фай и удобная бронь для встреч и мероприятий. Всё это легко собрать на одном лендинге.",
           "Аудитория — студенты, учёные и гости конференций. Сайт с понятным меню, акциями и возможностью заказать зал для события работает на вас круглый год."]
    trade = ["В городе развита торговля, а значит, много людей обедает рядом с магазинами и офисами. Сайт с бизнес-ланчем, доставкой и акциями помогает забрать эту аудиторию у соседних заведений.",
             "Рядом с торговыми точками решает удобство: быстро найти ваше заведение, увидеть цены и заказать на вынос. Короткий сайт с кнопкой звонка закрывает эту задачу."]
    gtxt = {"tour": tour, "ind": ind, "road": road, "agro": agro, "sci": sci, "trade": trade}
    sector = "".join("<p>%s</p>" % pick(slug, "g-" + g, gtxt[g]) for g in groups[:2])
    if not sector:
        sector = "<p>" + pick(slug, "gen", [
            "Для заведения общепита сайт — это витрина и администратор в одном лице: он отвечает на вопросы «что в меню», «сколько стоит», «есть ли места» круглосуточно, пока вы заняты на кухне и в зале.",
            "Большинство гостей сначала смотрит меню и цены, и только потом звонит. Сайт, который показывает всё это сразу, избавляет вас от десятков одинаковых вопросов в день."]) + "</p>"

    queries = shuf(slug, "q", [
        "ресторан %s" % N, "кафе %s" % N, "бизнес-ланч %s" % N, "забронировать столик %s" % N,
        "доставка еды %s" % N, "банкет %s" % N, "кафе рядом со мной", "где поужинать %s" % N])[:5]

    musts_all = [
        ("Меню с ценами и фото", "Текстом, а не картинкой или PDF: так оно открывается на телефоне и индексируется поиском. Фото блюд — настоящие, из вашей кухни."),
        ("Бронирование стола", "Короткая форма или кнопка звонка и мессенджера. Заявки приходят вам в Telegram, а не пропадают в почте."),
        ("Доставка и самовывоз", "Условия, зона, минимальный заказ и время. Если нужен свой каталог с корзиной, это уже интернет-магазин."),
        ("Атмосфера и зал", "Фото интерьера, вместимость, описание залов для банкетов и мероприятий — гость должен представить, как проведёт вечер."),
        ("Акции и бизнес-ланчи", "Отдельный блок с ценой и временем действия. Это самое частое, что ищут днём, и самое простое, что можно обновлять."),
        ("Адрес, карта и график", "Данные в точности как в карточках Яндекс Бизнеса, Google и 2ГИС, плюс кнопка «Проложить маршрут»."),
    ]
    musts = shuf(slug, "musts", musts_all)

    prices = [
        ("Лендинг для заведения", "15 000 ₽", "3 дня: дизайн, меню, бронь, акции, карта, кнопки звонка и мессенджеров, SEO и аналитика"),
        ("Интернет-магазин с доставкой", "от 35 000 ₽", "свой каталог блюд с корзиной и заказами в Telegram; до 20 позиций входит в цену, каждая следующая — 500 ₽"),
        ("Версия на английском", "4 000 ₽", "переключатель RU/EN и перевод всех текстов — полезно, если к вам приезжают иностранные гости"),
        ("Размещение вашей статьи", "1 500 ₽ за статью", "у вас есть готовый текст об истории заведения, шефе или сезонном меню — оформлю и размещу его на сайте красиво и грамотно. Если статей больше 30, цена обсуждается: чем больше, тем дешевле"),
    ]

    seo_items = shuf(slug, "seo", [
        "Заполните карточки заведения в Яндекс Бизнесе, Google Business Profile и 2ГИС: название, адрес, график, телефон, категории, меню и фото.",
        "Указывайте город в заголовках и текстах естественно: «%s» и «%s» — без переспама ключами." % (queries[0], queries[1] if len(queries) > 1 else "кафе " + N),
        "Собирайте отзывы на картах и отвечайте на них: от этого зависит и выбор гостя, и место карточки в выдаче.",
        "Добавьте на сайт вопросы и ответы (график, парковка, банкеты, детское меню) и разметку Schema.org: поисковикам проще понять, чем вы занимаетесь.",
        "Подключите Яндекс Метрику и Вебмастер, чтобы видеть, по каким запросам приходят гости и сколько заявок даёт сайт.",
        "Обновляйте акции и сезонное меню на сайте: свежие страницы поисковики индексируют охотнее.",
        "Добавьте в карточки и на сайт ссылки друг на друга: единые название, адрес и телефон повышают доверие поисковиков."])[:5]

    remote = pick(slug, "remote", [
        "Я работаю из Москвы и веду проекты дистанционно: бриф, согласование и запуск проходят в мессенджере и по телефону. Заказчику %s ехать никуда не нужно." % L,
        "Весь процесс идёт онлайн: вы присылаете фото, меню и контакты, я собираю сайт и показываю результат. Для заведения %s это ничем не отличается от работы с местной студией, кроме цены и скорости." % L,
        "Заказчикам %s не нужно приезжать в Москву: договариваемся по телефону, материалы приходят в мессенджер, сайт запускается на вашем домене." % L])

    faq_pool = [
        ("Сколько стоит сайт для ресторана или кафе %s?" % L, "Лендинг для заведения стоит 15 000 ₽ и делается за 3 дня. Если нужен каталог блюд с корзиной для доставки — интернет-магазин от 35 000 ₽ (до 20 позиций входит в цену). Домен в течение года обойдётся примерно в 500 ₽."),
        ("Можно ли принимать бронь столов через сайт?", "Да. Форма брони отправляет заявку вам в Telegram, а кнопки звонка и мессенджеров дублируют её. Онлайн-касса и оплата не обязательны."),
        ("Нужно ли ехать в Москву или встречаться лично?", "Нет. Для заведений %s работа ведётся онлайн: созвон, мессенджер, демонстрация экрана. Лично встречаюсь только в Москве." % L),
        ("Как быстро заведение окажется в поиске?", "Сайт запускается с готовой SEO-основой, но позиции зависят от конкуренции и времени. Быстрее всего помогают карточки в Яндекс Бизнесе, Google и 2ГИС и отзывы гостей — подключайте их сразу."),
        ("У меня уже есть текст про заведение. Можно разместить?", "Да. Оформлю готовую статью на сайте: заголовки, фото, ссылки и SEO-разметка. Размещение стоит 1 500 ₽ за статью."),
        ("Можно ли обновлять меню и цены самому?", "Меню на сайте — обычный текст. Присылайте правки в мессенджер, и я обновлю меню и акции. Так цены на сайте всегда совпадают с залом."),
    ]
    faq = [faq_pool[0]] + shuf(slug, "faq", faq_pool[1:])[:2]

    # ---------- разметка ----------
    toc = [("chto-ischut", "Что ищут гости %s" % L), ("na-sayte", "Что должно быть на сайте"), ("stoimost", "Сколько стоит сайт"),
           ("prodvizhenie", "Как заметить заведение в поиске"), ("faq", "Частые вопросы")]
    body = cover_picture("Макет сайта ресторана на ноутбуке: меню с ценами, фото блюда и кнопка бронирования стола")
    body += '<h2 id="chto-ischut">Что ищут гости %s</h2><p>%s</p>%s' % (esc(L), esc(p_intro), sector)
    body += "<p>Чаще всего гости набирают в поиске такие запросы:</p><ul>" + "".join("<li>«%s»</li>" % esc(q) for q in queries) + "</ul>"
    body += "<p>На каждый из них отвечает сайт заведения вместе с карточками на картах. Если сайта нет, вы отдаёте эти запросы тем, у кого он есть.</p>"
    body += '<h2 id="na-sayte">Что должно быть на сайте ресторана или кафе</h2><p>Шесть блоков закрывают почти все вопросы гостя заведения %s:</p><ol>' % esc(L)
    body += "".join("<li><b>%s.</b> %s</li>" % (esc(a), esc(b)) for a, b in musts) + "</ol>"
    body += '<div class="inline-cta"><p>Нужен сайт для заведения %s? Рассчитайте цену за минуту и зафиксируйте её предоплатой.</p><a class="btn" href="/#quiz">Рассчитать стоимость</a></div>' % esc(L)
    body += '<h2 id="stoimost">Сколько стоит сайт для ресторана или кафе</h2><p>Цены фиксированные, без скрытых платежей. Предоплата 5 000 ₽, остальное — после готовности сайта.</p><ul>'
    body += "".join("<li><b>%s — %s.</b> %s.</li>" % (esc(a), esc(b), esc(d[0].upper() + d[1:])) for a, b, d in prices) + "</ul>"
    body += "<p>%s</p>" % esc(remote)
    body += '<h2 id="prodvizhenie">Как заметить заведение в поиске</h2><p>Сайт — только часть работы. Чтобы вас нашли гости %s, сделайте несколько простых шагов:</p><ul>' % esc(L)
    body += "".join("<li>%s</li>" % esc(x) for x in seo_items) + "</ul>"
    body += '<h2 id="faq">Частые вопросы</h2><div class="faq">' + "".join("<details><summary>%s</summary><p>%s</p></details>" % (esc(q), esc(a)) for q, a in faq) + "</div>"

    nb = [x for x in neighbours(c)]
    body += '<h2>Сайты для ресторанов в других городах</h2><p>Статьи для соседних городов и всего региона:</p><div class="cities">'
    body += "".join('<a href="/blog/restoran-sayt-%s/">%s</a>' % (x["slug"], esc(x["name"])) for x in nb)
    body += '<a href="/blog/restoran-sayt-po-gorodam/">Все города →</a></div>'
    body += '<p style="margin-top:1.2em">Общие страницы по теме: <a href="/cities/%s/">создание сайтов %s</a>, <a href="/blog/restoran-sayt-struktura/">структура сайта ресторана</a>, <a href="/blog/restoran-sayt-stoimost/">сколько стоит сайт ресторана</a>.</p>' % (slug, esc(L))

    words = len(re.sub(r"<[^>]+>", " ", body).split())
    aside = ('<aside class="aside"><nav class="card toc" aria-label="Содержание статьи"><b>Содержание</b><ol>' +
             "".join('<li><a href="#%s">%s</a></li>' % (i, esc(t)) for i, t in toc) +
             '</ol></nav><div class="cta"><h3>Сайт за 3 дня под ключ</h3><p>Лендинг — 15 000 ₽, интернет-магазин — от 35 000 ₽. Скрытых платежей нет.</p><a class="btn" href="/#quiz">Рассчитать стоимость</a></div></aside>')

    crumbs = ('<nav class="crumbs wrap" aria-label="Хлебные крошки"><ol><li><a href="/">Главная</a></li><li><a href="/blog/">Блог</a></li><li aria-current="page">%s</li></ol></nav>' % esc(title))
    meta = ('<div class="wrap art-h"><span class="tag">Сайт для ресторана · %s</span><h1>%s</h1><div class="meta"><span>Автор: Дмитрий, веб-разработчик, опыт 10 лет</span>'
            '<span>Обновлено: <time datetime="%s">9 ноября 2026</time></span><span>Чтение: %d мин</span></div></div>' % (esc(N), esc(title), TODAY, max(2, round(words / 180))))
    page_main = '<main id="main">' + crumbs + meta + '<div class="wrap art"><article class="prose">' + body + "</article>" + aside + "</div></main>"

    ld = [
        {"@context": "https://schema.org", "@type": "Article", "@id": url + "#article", "headline": title, "description": desc,
         "image": ["%s/assets/img/%s-1200.jpg" % (SITE, COVER)], "datePublished": TODAY, "dateModified": TODAY, "inLanguage": "ru",
         "author": {"@id": SITE + "/#person"}, "publisher": {"@id": SITE + "/#org"}, "mainEntityOfPage": {"@type": "WebPage", "@id": url},
         "articleSection": "Сайт для ресторана", "wordCount": words,
         "keywords": ", ".join(["сайт для ресторана %s" % N, "сайт для кафе %s" % N, "заказать сайт %s" % N, "создание сайта ресторана", "бронирование столика"]),
         "about": {"@type": "Thing", "name": "Сайт для ресторана и кафе"}},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Главная", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Блог", "item": SITE + "/blog/"},
            {"@type": "ListItem", "position": 3, "name": title, "item": url}]},
    ]
    return head(title, desc, url, ld) + HEADER + page_main + FOOTER, words

def build_hub():
    url = SITE + "/blog/restoran-sayt-po-gorodam/"
    title = "Сайт для ресторана и кафе по городам России: статьи для %d городов" % len(CITIES)
    desc = "Сайт для ресторана и кафе в вашем городе: цены, сроки и что разместить. Выберите свой город из %d — лендинг 15 000 ₽ за 3 дня." % len(CITIES)
    order = ["Центральный", "Северо-Западный", "Южный", "Северо-Кавказский", "Приволжский", "Уральский", "Сибирский", "Дальневосточный"]
    fos = []
    for c in CITIES:
        if c["fo"] not in fos: fos.append(c["fo"])
    fos.sort(key=lambda f: order.index(f) if f in order else 99)
    body = cover_picture("Макет сайта ресторана на ноутбуке")
    body += "<p>Для каждого города подготовлена отдельная статья: что ищут гости, что разместить на сайте заведения и сколько это стоит. Выберите свой город.</p>"
    for fo in fos:
        lst = sorted([c for c in CITIES if c["fo"] == fo], key=lambda c: c["name"])
        body += "<h2>%s федеральный округ</h2><div class=\"cities\">" % esc(fo) + "".join('<a href="/blog/restoran-sayt-%s/">%s</a>' % (c["slug"], esc(c["name"])) for c in lst) + "</div>"
    body += '<div class="inline-cta"><p>Нужен сайт для ресторана или кафе? Рассчитайте цену за минуту.</p><a class="btn" href="/#quiz">Рассчитать стоимость</a></div>'
    crumbs = ('<nav class="crumbs wrap" aria-label="Хлебные крошки"><ol><li><a href="/">Главная</a></li><li><a href="/blog/">Блог</a></li><li aria-current="page">Сайты для ресторанов по городам</li></ol></nav>')
    meta = ('<div class="wrap art-h"><span class="tag">Сайт для ресторана · Города</span><h1>%s</h1><div class="meta"><span>Автор: Дмитрий, веб-разработчик, опыт 10 лет</span><span>Обновлено: <time datetime="%s">9 ноября 2026</time></span></div></div>' % (esc(title), TODAY))
    main = '<main id="main">' + crumbs + meta + '<div class="wrap art"><article class="prose">' + body + "</article></div></main>"
    ld = [{"@context": "https://schema.org", "@type": "CollectionPage", "@id": url + "#page", "name": title, "description": desc, "url": url, "inLanguage": "ru",
           "isPartOf": {"@id": SITE + "/#site"}},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": "Главная", "item": SITE + "/"},
              {"@type": "ListItem", "position": 2, "name": "Блог", "item": SITE + "/blog/"},
              {"@type": "ListItem", "position": 3, "name": "Сайты для ресторанов по городам", "item": url}]}]
    return head(title, desc, url, ld, article=False) + HEADER + main + FOOTER

def main():
    total_words = 0
    for c in CITIES:
        page, w = build(c); total_words += w
        write("blog/restoran-sayt-%s/index.html" % c["slug"], page)
    write("blog/restoran-sayt-po-gorodam/index.html", build_hub())
    # sitemap
    sm = read("sitemap.xml")
    urls = ["%s/blog/restoran-sayt-%s/" % (SITE, c["slug"]) for c in CITIES] + [SITE + "/blog/restoran-sayt-po-gorodam/"]
    add = ""
    for u in urls:
        if "<loc>%s</loc>" % u not in sm:
            add += '<url><loc>%s</loc><lastmod>%s</lastmod><priority>0.5</priority>\n</url>\n' % (u, TODAY)
    if add: sm = sm.replace("</urlset>", add + "</urlset>")
    write("sitemap.xml", sm)
    print("articles:", len(CITIES), "avg words:", total_words // len(CITIES), "sitemap added:", add.count("<url>"))

if __name__ == "__main__":
    main()
