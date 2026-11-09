# -*- coding: utf-8 -*-
"""Генератор страниц городов: python3 tools/gen_cities.py
Создаёт /cities/<slug>/index.html для всех городов из cities_data.NEW, пересобирает /cities/index.html,
дополняет sitemap.xml. Существующие страницы городов (EXISTING) не перезаписываются."""
import os, re, sys, hashlib, html, json
sys.path.insert(0, os.path.dirname(__file__))
from cities_data import EXISTING, NEW, CFO, SZFO, UFO_S, SKFO, PFO, URFO, SFO, DFO

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://dmitry-web.ru"
TODAY = "2026-11-05"
CSS_V = "82129e1c"; JS_V = "f26429e6"

def read(p): return open(os.path.join(ROOT, p), encoding="utf-8").read()
def write(p, s):
    full = os.path.join(ROOT, p); os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(s)

# ---------- транслитерация ----------
TR = dict(zip("абвгдеёжзийклмнопрстуфхцчшщъыьэюя", ["a","b","v","g","d","e","e","zh","z","i","y","k","l","m","n","o","p","r","s","t","u","f","h","ts","ch","sh","sch","","y","","e","yu","ya"]))
def slugify(n):
    out = "".join(TR.get(ch, ch) for ch in n.lower().replace(" ", "-"))
    return re.sub(r"[^a-z0-9-]+", "", out).strip("-")

def h(*parts):
    return int(hashlib.md5("|".join(map(str, parts)).encode()).hexdigest(), 16)
def pick(slug, key, opts): return opts[h(slug, key) % len(opts)]
def esc(s): return html.escape(s, quote=False)
def eq(s): return html.escape(s, quote=True)

# ---------- данные ----------
CITIES = []
for n, loc, reg, fo, pop, tags, slug in EXISTING:
    CITIES.append(dict(name=n, loc=loc, region=reg, fo=fo, pop=pop, tags=tags, slug=slug, new=False))
for n, loc, reg, fo, pop, tags in NEW:
    CITIES.append(dict(name=n, loc=loc, region=reg, fo=fo, pop=pop, tags=tags, slug=slugify(n), new=True))
slugs = [c["slug"] for c in CITIES]
assert len(slugs) == len(set(slugs)), [s for s in slugs if slugs.count(s) > 1]
BY = {c["slug"]: c for c in CITIES}

def size_class(p):
    if p >= 1000: return "mega"
    if p >= 500: return "big"
    if p >= 250: return "mid"
    if p >= 100: return "city"
    return "small"
def pop_phrase(p):
    return {"mega": "более 1 млн жителей", "big": "от 500 тыс. до 1 млн жителей", "mid": "от 250 до 500 тыс. жителей",
            "city": "от 100 до 250 тыс. жителей", "small": "менее 100 тыс. жителей"}[size_class(p)]

TAG_LABEL = {"tourism": "туризм", "resort": "курортный бизнес", "metal": "металлургия", "chem": "химическая промышленность",
 "mach": "машиностроение", "auto": "автомобильная отрасль", "mining": "добыча полезных ископаемых", "energy": "энергетика",
 "oil": "нефтегазовая отрасль", "ship": "судостроение", "agro": "агросектор", "port": "порт и портовая логистика",
 "logistics": "транспорт и логистика", "fishing": "рыбная отрасль", "science": "наука и образование", "wood": "лесная отрасль",
 "trade": "торговля", "textile": "текстильная отрасль", "defense": "оборонно-промышленный комплекс"}
TAG_GROUP = {"tourism": "tourism", "resort": "resort", "metal": "b2b", "chem": "b2b", "mach": "b2b", "mining": "b2b", "energy": "b2b",
 "oil": "b2b", "ship": "b2b", "defense": "b2b", "agro": "agro", "port": "port", "logistics": "port", "fishing": "fishing",
 "science": "science", "wood": "wood", "trade": "trade", "textile": "textile", "auto": "auto"}
GROUP_TXT = {
 "tourism": ["Для гостиниц, экскурсионных и туристических компаний сайт — главная точка принятия решения: приезжий за несколько секунд должен понять, что посмотреть, где остановиться и как забронировать. Поэтому структура строится вокруг заявки: понятные цены, фотографии, карта, кнопки звонка и мессенджеров на каждом экране.",
             "Туристический поток сезонный, а значит окно для заявок короткое. Сайт должен открываться мгновенно на телефоне в роуминге и медленном интернете, показывать наличие и цены и принимать бронь без лишних шагов — иначе гость уйдёт к тому, у кого проще."],
 "resort": ["Курортный сезон — всплеск спроса и короткое окно для заявок. Сайт гостиницы, санатория, экскурсионной или медицинской услуги должен быстро грузиться на телефоне, показывать актуальные цены и принимать бронь без лишних шагов: приезжие выбирают с экрана смартфона.",
            "Для курортных городов решает мобильная версия: гость листает варианты в дороге. Нужны крупные фотографии, цены «от», расположение на карте, отзывы и кнопка «Позвонить» или «Написать в мессенджер», доступная одним касанием."],
 "b2b": ["Промышленные и технические компании выигрывают от сайта-каталога: продукция, технические характеристики, сертификаты, реквизиты и форма запроса коммерческого предложения. Закупщик проверяет поставщика по нескольким источникам, и на сайте не должно быть пустых разделов и устаревших цифр.",
         "В отраслях с длинным циклом сделки сайт работает как цифровой офис и визитка для тендеров: о компании, мощности, клиенты, документы и контактное лицо. Хороший B2B-сайт не продаёт «в лоб» — он снимает сомнения и ведёт к запросу коммерческого предложения."],
 "agro": ["Агросектор — это поставщики и переработчики: сайт-каталог с продукцией, объёмами, условиями поставки и формой заявки помогает выходить на оптовых покупателей, в том числе из других регионов. Здесь особенно важны понятные фото продукции, сертификаты и география поставок.",
          "Производителю продуктов и сельхозтоваров сайт даёт возможность продавать мимо посредников: прайс для оптовиков, условия доставки, документы и форма заявки. Для розницы можно добавить небольшой интернет-магазин с заказом в мессенджер."],
 "port": ["Порт, транспорт и логистика — это B2B: перевозчикам и экспедиторам нужны направления, тарифы, сроки и быстрый расчёт. Лендинг с формой расчёта стоимости работает лучше длинного описания компании: клиент оставляет параметры груза и получает предложение.",
          "Логистическим компаниям важно показать маршруты, виды транспорта, сроки и гарантии, а также кейсы с понятными цифрами. Отдельные страницы под направления и услуги помогают находить компанию по узким запросам."],
 "fishing": ["Рыбная отрасль и пищевое производство работают преимущественно с оптом: каталог продукции, сертификаты, условия отгрузки и форма запроса цен — основа сайта. Дополнительно полезна простая страница с контактами для магазинов и заведений, которые ищут местного поставщика.",
             "Для производителей рыбной и морской продукции сайт — способ показать качество и стабильность поставок: производство, фото, документы, география. Это снимает вопросы новых оптовых клиентов ещё до первого звонка."],
 "science": ["Наука и образование — центры знаний: сайты лабораторий, курсов, репетиторов и инжиниринговых команд выигрывают от экспертного контента — статей, кейсов и публикаций. Поисковые системы считают такой контент признаком качества, а клиенты — причиной доверять.",
             "Для научных и образовательных проектов важна структура: программы, преподаватели, результаты, отзывы и простая запись. Современный сайт с описанием методики и честными ценами конвертирует лучше, чем страница в соцсети."],
 "wood": ["Лесопромышленным компаниям важен каталог продукции с породой, сортом, размерами и условиями поставки — покупатели из других регионов ищут именно такие данные. Фото складов и производства, сертификаты и прайс повышают доверие к поставщику.",
          "Деревообработка и лесозаготовка продают оптом, поэтому сайт должен быстро отвечать на технические вопросы: что, сколько, откуда и на каких условиях. Форма запроса цены и понятные контакты отдела продаж закрывают остальное."],
 "trade": ["Торговля и сервис — основа малого бизнеса: магазины, кафе, салоны, мастерские. Для них сайт — это витрина и приёмник заявок: цены, адрес на карте, график работы и быстрая связь. Покупатель сначала смотрит в интернет, а потом идёт в магазин или звонит.",
           "Для торговли и услуг важна простота: клиент должен за пару касаний найти цену и контакт. Каталог, корзина или заявка в мессенджер, отзывы и ответы на частые вопросы превращают посетителя в покупателя."],
 "textile": ["Текстильные и швейные производства работают с оптом и маркетплейсами: каталог тканей и изделий, прайс, минимальная партия и форма запроса помогают получать новых оптовых клиентов. Отдельный сайт снижает зависимость от площадок и комиссий.",
             "Для производителей текстиля и одежды сайт — это каталог для байеров и точка входа для частных заказов. Хорошие фотографии, описание материалов, размерные сетки и простая форма заказа обычно важнее сложного дизайна."],
 "auto": ["Автомобильная отрасль даёт работу целой экосистеме: сервисы, детейлинг, запчасти, аренда, поставщики. Локальный бизнес здесь живёт поиском по карте и в выдаче: адрес, график, цены на популярные услуги, онлайн-запись и отзывы приводят клиентов лучше любой рекламы.",
          "Рядом с автомобильным производством всегда много смежного бизнеса: сервисы, логистика, поставщики комплектующих. Для B2B-поставщиков нужен сайт-каталог с техническими данными и запросом КП, для сервисов — быстрый контакт и честный прайс."],
}

NICHES = ["vizitka","lending","internet-magazin","salon-krasoty","stomatologiya","remont-kvartir","yurist","klining","avtoservis","avtomoyka","arenda-avto",
          "barbershop","restoran","turfirma","fitnes","fotograf","gruzoperevozki","mebel","nedvizhimost","okna-dveri","shkola-kursy","stroitelstvo","zavod","firma","kuhni","ekspert-bloger","gruppa"]
GROUP_NICHES = {"tourism": ["turfirma","restoran","fotograf"], "resort": ["turfirma","restoran","salon-krasoty","fitnes"],
 "b2b": ["zavod","firma","gruzoperevozki","stroitelstvo"], "auto": ["avtoservis","avtomoyka","arenda-avto","zavod"],
 "agro": ["zavod","gruzoperevozki","firma","internet-magazin"], "port": ["gruzoperevozki","firma","zavod","lending"],
 "science": ["shkola-kursy","ekspert-bloger","firma","yurist"], "fishing": ["zavod","internet-magazin"],
 "wood": ["zavod","mebel","stroitelstvo","okna-dveri"], "trade": ["internet-magazin","salon-krasoty","barbershop","restoran"],
 "textile": ["zavod","internet-magazin"]}

# ---------- блог: карточки ниш ----------
BLOG = read("blog/index.html")
CARDS = {}
for m in re.finditer(r'<a class="card post rv" href="/blog/([a-z0-9-]+)-sayt-zachem/"[^>]*>.*?</a>', BLOG, re.S):
    CARDS[m.group(1)] = m.group(0)
NICHE_NAME = {}
for n in CARDS:
    mm = re.search(r'<h3>([^<]+)</h3>', CARDS[n]); NICHE_NAME[n] = mm.group(1) if mm else n
AVAILABLE_NICHES = [n for n in NICHES if n in CARDS]

# ---------- сквозные куски разметки ----------
SAMPLE = read("cities/kazan/index.html")
HEADER = SAMPLE[SAMPLE.index('<body>') : SAMPLE.index('<main id="main">')]
FOOTER = SAMPLE[SAMPLE.index('</main>') :]
FOOTER = FOOTER.replace("</main>", "", 1)
HEAD_COMMON = ('<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">')
HEAD_TAIL = ('<meta name="theme-color" content="#0a0a0a"><meta name="color-scheme" content="dark"><meta name="author" content="Дмитрий">'
 '<link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg"><link rel="apple-touch-icon" href="/assets/icons/icon-180.png"><link rel="manifest" href="/site.webmanifest">'
 '<link rel="preload" href="/assets/fonts/onest-cyrillic-wght-normal.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="/assets/fonts/unbounded-cyrillic-wght-normal.woff2" as="font" type="font/woff2" crossorigin>'
 '<link rel="stylesheet" href="/assets/style.css?v=%s"><script>(function(d){d.className+=" js";var s=0;try{s=sessionStorage.getItem("pre")}catch(e){}if(s||matchMedia("(prefers-reduced-motion:reduce)").matches)d.className+=" nopre"})(document.documentElement)</script>' % CSS_V)
FOOTER = FOOTER.replace("a6d2e960", CSS_V).replace("c5e1a7d2", JS_V)
IMG = (SAMPLE[SAMPLE.index('<div class="frame">'): SAMPLE.index('</picture></div>', SAMPLE.index('<div class="frame">')) + len('</picture></div>')])

def head(title, desc, url, alt, extra_ld):
    return ('<!doctype html><html lang="ru" prefix="og: https://ogp.me/ns#"><head>' + HEAD_COMMON +
     '<title>%s</title><meta name="description" content="%s"><link rel="canonical" href="%s"><meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">' % (esc(title), eq(desc), url) +
     '<meta property="og:type" content="website"><meta property="og:site_name" content="DMITRY·WEB"><meta property="og:locale" content="ru_RU"><meta property="og:title" content="%s"><meta property="og:description" content="%s"><meta property="og:url" content="%s">' % (eq(title), eq(desc), url) +
     '<meta property="og:image" content="%s/assets/img/og-image.jpg?v=2"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="%s">' % (SITE, eq(alt)) +
     '<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="%s"><meta name="twitter:description" content="%s"><meta name="twitter:image" content="%s/assets/img/og-image.jpg?v=2">' % (eq(title), eq(desc), SITE) +
     HEAD_TAIL + extra_ld + '</head>')

def ld(obj): return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + '</script>'

# ---------- соседи ----------
def neighbours(c, k=8):
    same_region = [x for x in CITIES if x["region"] == c["region"] and x["slug"] != c["slug"]]
    same_fo = [x for x in CITIES if x["fo"] == c["fo"] and x["region"] != c["region"] and x["slug"] != c["slug"]]
    same_region.sort(key=lambda x: (-x["pop"]))
    same_fo.sort(key=lambda x: h(c["slug"], x["slug"]))
    out = same_region[:k]
    out += same_fo[: max(0, k - len(out))]
    return out

# ---------- страница города ----------
def make_page(c):
    N, L, R, slug = c["name"], c["loc"], c["region"], c["slug"]
    sc = size_class(c["pop"]); pp = pop_phrase(c["pop"]); url = "%s/cities/%s/" % (SITE, slug)
    tags = c["tags"]; groups = []
    for t in tags:
        g = TAG_GROUP.get(t)
        if g and g not in groups: groups.append(g)
    title = pick(slug, "title", [
        "Создание сайтов %s под ключ — лендинг 15 000 ₽ за 3 дня | DMITRY·WEB",
        "Заказать сайт %s под ключ — лендинг 15 000 ₽, магазин от 35 000 ₽ | DMITRY·WEB",
        "Разработка сайтов %s: лендинг за 3 дня, магазин от 35 000 ₽ | DMITRY·WEB"]) % L
    desc = pick(slug, "desc", [
        "Создание сайтов %s (%s): лендинг 15 000 ₽ за 3 дня, интернет-магазин от 35 000 ₽, SEO внутри. Работаю онлайн, без поездок и посредников.",
        "Нужен сайт %s? Лендинг под ключ за 3 дня — 15 000 ₽, интернет-магазин от 35 000 ₽ (до 20 карточек товара). Регион: %s. Работа онлайн.",
        "Сайты под ключ для бизнеса %s (%s): быстрый запуск за 3 дня, SEO-настройка, заявки в Telegram и мессенджеры. Лендинг — 15 000 ₽."]) % (L, R)
    # --- блоки ---
    # 1. вводный абзац по размеру города
    intro = {
     "mega": ["%s — город с населением %s, и конкуренция за внимание клиента здесь высокая: по большинству запросов вида «заказать…» или «цена…» в выдаче уже стоят десятки компаний. Выигрывает тот, чей сайт открывается мгновенно, понятен с первого экрана и вызывает доверие." % (N, pp)],
     "big": ["%s (%s) — город с населением %s. Рынок ёмкий, и онлайн-заявки здесь давно стали отдельным каналом продаж, но компаний с сильным сайтом пока меньше, чем в столицах. Грамотно собранная страница способна заметно выделить бизнес среди конкурентов." % (N, R, pp)],
     "mid": ["%s — город в регионе «%s», население — %s. Рынок достаточно большой, чтобы заявки из интернета стали стабильным источником клиентов, и в то же время конкурентов в выдаче заметно меньше, чем в мегаполисах: хороший сайт здесь может занять сильные позиции по локальным запросам." % (N, R, pp)],
     "city": ["%s — город с населением %s (регион — %s). Клиенты здесь привыкли выбирать по рекомендациям и отзывам, поэтому сайт — это прежде всего доверие: реальные фотографии, прозрачные цены, отзывы и понятные контакты. Именно это проверяют перед звонком." % (N, pp, R)],
     "small": ["%s — небольшой город (%s), регион — %s. Большинство клиентов приходят по рекомендациям, но всё чаще проверяют компанию в интернете до звонка. Сайт, который находится по запросу с названием города, закрывает именно этот момент — и работает на вас круглосуточно." % (N, pp, R)],
    }[sc][0]
    remote = pick(slug, "remote", [
        "Я работаю из Москвы и веду проекты дистанционно: созвон, мессенджеры, демонстрация экрана. Для заказчика %s это ничего не меняет: цена, сроки и качество те же, что и при личной встрече, а на согласования через посредников не уходит время." % L,
        "Весь процесс проходит онлайн: вы отправляете материалы, мы обсуждаем структуру в мессенджере или по телефону, а готовый сайт запускается на вашем домене. Расстояние до Москвы не влияет ни на стоимость, ни на сроки.",
        "Заказчикам %s не нужно ехать в Москву: бриф, согласование макета, правки и запуск происходят дистанционно. Договариваемся в удобном вам мессенджере и фиксируем цену до начала работ." % L])
    sector = ""
    if tags:
        labs = ", ".join(TAG_LABEL[t] for t in tags if t in TAG_LABEL)
        sector = '<p>В экономике города (%s) заметны такие направления, как %s. Для них у сайта разные задачи.</p>' % (R, labs)
        for g in groups[:2]:
            sector += '<p>' + pick(slug, "g-" + g, GROUP_TXT[g]) + '</p>'
    else:
        sector = '<p>Как и везде, основу бизнеса %s составляют малый и средний бизнес: магазины, услуги, строительство, красота и здоровье, образование. Для таких компаний сайт — это витрина, визитка и приёмник заявок одновременно, а карточка на карте и страница в соцсети лишь дополняют его.</p>' % L
    # 2. что должно быть на сайте
    musts = [
      "Понятное предложение на первом экране: кто вы, что продаёте и в чём выгода — без «о нас» вместо смысла",
      "Цены или вилка «от» — клиенты %s чаще оставляют заявку, когда понимают порядок затрат" % L,
      "Реальные фотографии, примеры работ и отзывы: они снимают сомнения лучше любого текста",
      "Телефон, Telegram, WhatsApp и Max одним касанием на каждом экране — особенно на смартфоне",
      "Адрес, режим работы и карта, написанные так же, как в Яндекс Бизнесе, Google и 2ГИС",
      "Быстрая загрузка: страница, которая открывается дольше трёх секунд, теряет заметную часть посетителей"]
    musts = sorted(musts, key=lambda m: h(slug, m))
    # 3. шаги
    steps = [
      ("Заявка и бриф", pick(slug, "s1", ["Вы пишете в мессенджер или оставляете заявку — я уточняю задачу, нишу, пожелания и примеры сайтов, которые нравятся.", "Короткий разговор или переписка: что продаёте, кому, какие страницы и функции нужны. Бриф занимает 10–15 минут."])),
      ("Предоплата 5 000 ₽", pick(slug, "s2", ["Предоплата фиксирует цену и срок: с этого момента отсчитываются 3 дня на лендинг.", "После предоплаты 5 000 ₽ цена остаётся неизменной, а срок начинает идти. Остальное — после готовности сайта."])),
      ("Материалы", pick(slug, "s3", ["Вы присылаете тексты или описание бизнеса, фото, логотип и контакты. Чем полнее материалы, тем быстрее результат.", "Нужны описание услуг, цены, фотографии, логотип (если есть) и контакты. Недостающее подскажу и помогу оформить."])),
      ("Дизайн, вёрстка и SEO", pick(slug, "s4", ["Собираю адаптивный сайт: дизайн под вашу нишу, быстрая вёрстка, мета-теги, микроразметка, карта сайта и аналитика.", "Рисую структуру, верстаю под все экраны и сразу закладываю SEO: title, description, Schema.org, Open Graph, sitemap."])),
      ("Запуск и передача", pick(slug, "s5", ["Размещаю сайт на вашем домене, подключаю формы, заявки в Telegram и счётчики. Домен и доступы остаются у вас.", "Запуск на вашем домене, проверка форм и мессенджеров, передача доступов. Вы платите остаток — и сайт работает."]))]
    # 4. локальное SEO
    seo_items = [
      "Заполните карточки компании в Яндекс Бизнесе, Google Business Profile и 2ГИС: название, адрес, график, телефон, категории и фото",
      "Укажите на сайте город, район и зоны обслуживания в тех же формулировках, что и в карточках — данные должны совпадать до мелочей",
      "Используйте в заголовках и текстах естественные запросы: «%s», «заказать сайт %s», «разработка сайта %s» — без переспама" % (("создание сайтов " + L), N, N),
      "Собирайте отзывы на картах и на сайте и отвечайте на них — это влияет и на выбор клиента, и на видимость организации",
      "Добавьте на сайт блок вопросов и ответов и схему организации в формате Schema.org — поисковикам проще понять, чем вы занимаетесь",
      "Подключите Яндекс Метрику и Вебмастер: видно, по каким запросам находят сайт и откуда приходят заявки"]
    seo_items = sorted(seo_items, key=lambda m: h(slug, "seo", m))[:5]
    # 5. ниши
    pool = []
    for g in groups:
        pool += GROUP_NICHES.get(g, [])
    rest = sorted(AVAILABLE_NICHES, key=lambda n: h(slug, "n", n))
    chosen = []
    for n in pool + rest:
        if n in CARDS and n not in chosen: chosen.append(n)
        if len(chosen) == 4: break
    cards = "".join(CARDS[n] for n in chosen)
    # 6. соседи
    nb = neighbours(c)
    nb_html = "".join('<a href="/cities/%s/">%s</a>' % (x["slug"], esc(x["name"])) for x in nb)
    # 7. FAQ
    faq = [
      ("Сколько стоит сайт %s?" % L, "Цены не зависят от города: лендинг под ключ — 15 000 ₽, интернет-магазин — от 35 000 ₽ (в цену входит до 20 карточек товара, каждая следующая — 500 ₽), нейрокарточки для маркетплейсов — 350 ₽ за штуку. В течение года дополнительно платите только за домен — около 500 ₽."),
      ("Как заказать сайт %s, если вы в Москве?" % L, "Всё проходит онлайн: вы присылаете материалы, мы созваниваемся или переписываемся, а готовый сайт запускается на вашем домене. Для вас ничего не меняется по сравнению со встречей лично. Работаю как самозанятый и выдаю чек."),
      ("За какое время делается сайт?", "Одностраничный сайт — за 3 дня с момента предоплаты 5 000 ₽. Для интернет-магазина срок зависит от количества карточек товара и обсуждается заранее. Если срочно — есть тариф «сайт за 24 часа»."),
      ("Нужен ли сайт, если у бизнеса %s уже есть страница в соцсетях?" % L, "Соцсеть — это чужая площадка с правилами, которые могут измениться. Сайт принадлежит вам, находится в поиске по названию и услугам, принимает заявки и работает как цифровой офис. Лучше всего они работают вместе: соцсети приводят людей, сайт превращает их в клиентов."),
      ("Что входит в интернет-магазин за 35 000 ₽?", "Каталог, карточки товаров с галереей, корзина и форма заказа, заказы в Telegram, SEO-настройка и микроразметка Product. В цену входит до 20 карточек товара, каждая следующая — 500 ₽. От вас нужны папки по товарам: описание и фотографии."),
      ("Попадёт ли сайт в выдачу по запросам %s?" % L, "Я закладываю техническую основу: скорость, мета-теги, микроразметку, карту сайта и локальные данные. Позиции зависят ещё и от конкуренции, контента и времени, поэтому гарантировать конкретное место честно нельзя, но сайт будет полностью готов к индексации.")]
    faq_html = "".join("<details><summary>%s</summary><p>%s</p></details>" % (esc(q), esc(a)) for q, a in faq)
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
    svc_ld = {"@context": "https://schema.org", "@type": "Service", "@id": url + "#service", "name": "Создание сайтов " + L, "serviceType": "Web development",
      "provider": {"@id": SITE + "/#org"}, "areaServed": {"@type": "City", "name": N, "containedInPlace": {"@type": "AdministrativeArea", "name": R}}, "url": url,
      "offers": [{"@type": "Offer", "name": "Лендинг под ключ", "price": 15000, "priceCurrency": "RUB"},
                 {"@type": "Offer", "name": "Интернет-магазин до 20 карточек товара", "priceSpecification": {"@type": "PriceSpecification", "minPrice": 35000, "priceCurrency": "RUB"}}]}
    bc_ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
      {"@type": "ListItem", "position": 1, "name": "Главная", "item": SITE + "/"}, {"@type": "ListItem", "position": 2, "name": "Города", "item": SITE + "/cities/"},
      {"@type": "ListItem", "position": 3, "name": "Создание сайтов " + L, "item": url}]}
    lead = pick(slug, "lead", [
        "Лендинг за 3 дня — 15 000 ₽. Интернет-магазин — от 35 000 ₽. SEO внутри, быстрая загрузка на телефоне, заявки в мессенджеры. Работаю с клиентами %s онлайн." % L,
        "Сайт под ключ для бизнеса %s: лендинг за 3 дня — 15 000 ₽, интернет-магазин — от 35 000 ₽ (до 20 карточек товара). SEO внутри, заявки в Telegram." % L])
    hero = ('<section class="sec" style="padding-top:36px"><div class="wrap g2"><div><span class="eyebrow">%s</span><h1 style="font-size:clamp(32px,5vw,58px)">Создание сайтов %s под ключ</h1><p class="lead">%s</p>' % (esc(N), esc(L), esc(lead)) +
      '<div class="btns"><a class="btn" href="/#quiz">Рассчитать стоимость</a><a class="btn ghost" href="https://t.me/+79268542333" target="_blank" rel="noopener">Написать в Telegram</a></div></div>' +
      IMG.replace("создание сайтов в Казани", "создание сайтов " + L) + '</div></section>')
    article = ('<section class="sec alt"><div class="wrap" style="max-width:860px"><div class="prose"><span class="eyebrow">О рынке</span><h2>Сайты для бизнеса %s</h2><p>%s</p><p>%s</p>%s</div></div></section>' % (esc(L), esc(intro), esc(remote), sector) +
      '<section class="sec"><div class="wrap g2"><div><span class="eyebrow">Что на сайте</span><h2>Что должно быть на сайте компании %s</h2><p>Независимо от отрасли, сайты, которые приводят заявки, собраны по одной логике. Вот шесть вещей, без которых сайт остаётся «визиткой для галочки»:</p></div><div><ul>%s</ul></div></div></section>' % (esc(L), "".join("<li>%s</li>" % esc(m) for m in musts)) +
      '<section class="sec alt"><div class="wrap g2"><div><span class="eyebrow">Цены</span><h2>Сколько стоит сайт %s</h2><p>Стоимость не зависит от города: вы платите за работу, а не за адрес. Цена фиксируется до начала, скрытых платежей нет.</p><p class="mut" style="font-size:14px">Предоплата 5 000 ₽, остальное — после готовности. В цену магазина входит до 20 карточек товара, каждая следующая — 500 ₽. Домен (около 500 ₽ в год) оформляется на вас. <a href="/terms/">Условия работы</a>.</p></div><div><table><thead><tr><th>Услуга</th><th>Срок</th><th>Цена</th></tr></thead><tbody><tr><td>Лендинг под ключ</td><td>3 дня</td><td>15 000 ₽</td></tr><tr><td>Срочный сайт</td><td>24 часа</td><td>30 000 ₽</td></tr><tr><td>Интернет-магазин до 20 карточек товара</td><td>по договорённости</td><td>от 35 000 ₽</td></tr><tr><td>Нейрокарточки для маркетплейсов</td><td>по объёму</td><td>350 ₽ / шт</td></tr></tbody></table></div></div></section>' % esc(L) +
      '<section class="sec"><div class="wrap"><div class="sec-head"><span class="eyebrow">Ниши</span><h2>Какие сайты заказывают %s</h2><p class="lead">Практические статьи по вашей теме: зачем нужен сайт, что на нём должно быть и как он приводит клиентов.</p></div><div class="g4">%s</div></div></section>' % (esc(L), cards) +
      '<section class="sec alt"><div class="wrap g2"><div><span class="eyebrow">Как это работает</span><h2>Как заказать сайт %s</h2><p>Пять шагов от заявки до запуска. Лендинг занимает три дня с момента предоплаты.</p></div><div><ol>%s</ol></div></div></section>' % (esc(L), "".join("<li><b>%s.</b> %s</li>" % (esc(a), esc(b)) for a, b in steps)) +
      '<section class="sec"><div class="wrap g2"><div><span class="eyebrow">Локальное SEO</span><h2>Как сайту быть заметным %s</h2><p>Сайт — только часть картины. Чтобы клиенты вас находили, сделайте пять вещей:</p></div><div><ol>%s</ol></div></div></section>' % (esc(L), "".join("<li>%s</li>" % esc(m) for m in seo_items)) +
      '<section class="sec alt"><div class="wrap"><div class="sec-head"><span class="eyebrow">Рядом</span><h2>Сайты в других городах региона и округа</h2><p class="lead">Работаю с клиентами из любого региона. %s находится в регионе «%s» (%s федеральный округ), ниже — другие города рядом.</p></div><div class="cities">%s<a href="/cities/">Все города →</a></div></div></section>' % (esc(N), esc(R), esc(c["fo"]), nb_html) +
      '<section class="sec"><div class="wrap" style="max-width:860px"><div class="sec-head"><span class="eyebrow">FAQ</span><h2>Вопросы клиентов %s</h2></div><div class="faq">%s</div><div class="btns" style="margin-top:34px"><a class="btn" href="/#contacts">Обсудить проект</a><a class="btn ghost" href="tel:+79268542333">Позвонить +7 926 854-23-33</a></div></div></section>' % (esc(L), faq_html))
    crumbs = '<nav class="crumbs wrap" aria-label="Хлебные крошки"><ol><li><a href="/">Главная</a></li><li><a href="/cities/">Города</a></li><li aria-current="page">Создание сайтов %s</li></ol></nav>' % esc(L)
    page = head(title, desc, url, "Создание сайтов %s — DMITRY·WEB" % L, ld(svg_dummy(svc_ld)) + ld(faq_ld) + ld(bc_ld)) + HEADER + '<main id="main">' + crumbs + hero + article + '</main>' + FOOTER
    return page

def svg_dummy(x): return x

def make_hub():
    old = read("cities/index.html")
    # переиспользуем оригинальный блок карточек (первые 25 городов)
    gi = old.index('<div class="g3">'); ge = old.index('</div></div></section>', gi)
    cards = old[gi:ge] + '</div>'
    groups = [("Центральный федеральный округ", CFO), ("Северо-Западный федеральный округ", SZFO), ("Южный федеральный округ", UFO_S), ("Северо-Кавказский федеральный округ", SKFO),
              ("Приволжский федеральный округ", PFO), ("Уральский федеральный округ", URFO), ("Сибирский федеральный округ", SFO), ("Дальневосточный федеральный округ", DFO)]
    blocks = ""
    for title, fo in groups:
        items = sorted([x for x in CITIES if x["fo"] == fo], key=lambda x: x["name"])
        blocks += '<h2 style="font-size:clamp(22px,2.6vw,30px);margin-top:44px">%s</h2><div class="cities" style="margin-top:16px">%s</div>' % (esc(title), "".join('<a href="/cities/%s/">%s</a>' % (x["slug"], esc(x["name"])) for x in items))
    title = "Создание сайтов по городам России — %d городов | DMITRY·WEB" % len(CITIES)
    desc = "Создание сайтов под ключ в %d городах России: лендинг 15 000 ₽ за 3 дня, интернет-магазин от 35 000 ₽. Работа онлайн, личные встречи в Москве." % len(CITIES)
    url = SITE + "/cities/"
    items_ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Создание сайтов по городам России", "url": url,
      "mainEntity": {"@type": "ItemList", "numberOfItems": len(CITIES), "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": "%s/cities/%s/" % (SITE, x["slug"]), "name": "Создание сайтов " + x["loc"]} for i, x in enumerate(CITIES)]}}
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Главная", "item": SITE + "/"}, {"@type": "ListItem", "position": 2, "name": "Города", "item": url}]}
    main = ('<main id="main"><nav class="crumbs wrap" aria-label="Хлебные крошки"><ol><li><a href="/">Главная</a></li><li aria-current="page">Города</li></ol></nav><section class="sec" style="padding-top:36px"><div class="wrap"><div class="sec-head"><span class="eyebrow">География</span><h1 style="font-size:clamp(32px,5vw,56px)">Создание сайтов по городам России</h1><p class="lead">Работаю с клиентами из любых регионов онлайн, лично встречаюсь в Москве. Выберите город, чтобы увидеть условия и полезные материалы.</p></div>'
        + cards + '<div class="sec-head" style="margin-top:56px;margin-bottom:0"><span class="eyebrow">Все города</span><h2>Города по федеральным округам</h2></div>' + blocks + '</div></section></main>')
    return head(title, desc, url, "Создание сайтов по городам России — DMITRY·WEB", ld(items_ld) + ld(bc)) + HEADER + main + FOOTER

def main():
    made = 0; words = []
    for c in CITIES:
        if not c["new"]: continue
        p = make_page(c); write("cities/%s/index.html" % c["slug"], p); made += 1
        txt = re.sub(r"<[^>]+>", " ", p[p.index('<main'):]); words.append(len(txt.split()))
    write("cities/index.html", make_hub())
    # sitemap
    sm = read("sitemap.xml")
    add = ""
    for c in CITIES:
        u = "%s/cities/%s/" % (SITE, c["slug"])
        if u in sm: continue
        add += '<url><loc>%s</loc><lastmod>%s</lastmod><priority>0.6</priority>\n</url>\n' % (u, TODAY)
    sm = sm.replace("</urlset>", add + "</urlset>")
    sm = sm.replace("<loc>https://dmitry-web.ru/cities/</loc><lastmod>2026-11-03</lastmod>", "<loc>https://dmitry-web.ru/cities/</loc><lastmod>%s</lastmod>" % TODAY)
    write("sitemap.xml", sm)
    print("pages", made, "words min/avg/max", min(words), sum(words) // len(words), max(words))

if __name__ == "__main__":
    main()
