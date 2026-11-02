# -*- coding: utf-8 -*-
import hashlib
from b_common import *
from data_cities import CITIES
from data_niches import N
import b_blog
from b_blog import money, YEAR

PREF = {
 "moskva": ["firma", "internet-magazin", "stomatologiya", "yurist", "salon-krasoty", "restoran", "nedvizhimost", "ekspert-bloger"],
 "sankt-peterburg": ["turfirma", "restoran", "fotograf", "firma", "gruzoperevozki", "nedvizhimost", "salon-krasoty", "gruppa"],
 "sochi": ["turfirma", "restoran", "nedvizhimost", "fotograf", "arenda-avto", "fitnes", "salon-krasoty", "klining"],
 "kazan": ["turfirma", "restoran", "stomatologiya", "salon-krasoty", "avtoservis", "shkola-kursy", "internet-magazin", "firma"],
 "ekaterinburg": ["zavod", "firma", "stroitelstvo", "gruzoperevozki", "avtoservis", "okna-dveri", "mebel", "yurist"],
 "kaliningrad": ["turfirma", "gruzoperevozki", "restoran", "arenda-avto", "fotograf", "nedvizhimost", "stroitelstvo", "firma"],
 "vladivostok": ["gruzoperevozki", "turfirma", "avtoservis", "arenda-avto", "restoran", "internet-magazin", "firma", "stroitelstvo"],
 "irkutsk": ["turfirma", "fotograf", "arenda-avto", "restoran", "stroitelstvo", "klining", "gruppa", "firma"],
 "novosibirsk": ["shkola-kursy", "firma", "internet-magazin", "stomatologiya", "stroitelstvo", "avtomoyka", "remont-kvartir", "ekspert-bloger"],
 "krasnodar": ["nedvizhimost", "stroitelstvo", "restoran", "salon-krasoty", "avtomoyka", "mebel", "fitnes", "internet-magazin"],
}

def niches_for(c):
    slug = c[0]; nm = {n["slug"]: n for n in N}
    if slug in PREF: return [nm[s] for s in PREF[slug]]
    h = int(hashlib.md5(slug.encode()).hexdigest(), 16)
    base = ["firma", "lending"]
    rest = [n["slug"] for n in N if n["slug"] not in base]
    pick = []
    for j in range(20):
        s = rest[(h + j * 5) % len(rest)]
        if s not in pick: pick.append(s)
        if len(pick) == 6: break
    return [nm[s] for s in base + pick]

def city_page(c):
    slug, name, prep, en, sectors, note = c
    pl, ps, pc, pp = money(CFG["price_landing"]), money(CFG["price_shop"]), money(CFG["price_card"]), money(CFG["prepay"])
    moscow = slug == "moskva"
    url_ = f"/cities/{slug}/"
    title = f"Создание сайтов {prep} под ключ — лендинг {pl} за 3 дня | DMITRY·WEB"
    desc = (f"Создание сайтов {prep}: лендинг {pl} за 3 дня, интернет-магазин от {ps}, SEO внутри, быстрая загрузка. " + ("Личная встреча в Москве." if moscow else "Работаю онлайн, без поездок и посредников."))
    ns = niches_for(c)
    cards = "".join(b_blog.card(n, "zachem") for n in ns)
    meet = ("Я живу и работаю в Москве, поэтому можем встретиться лично: обсудить сайт или проект вживую, показать примеры и сразу договориться об условиях. Для тех, кому удобнее онлайн, всё то же самое проходит по видеосвязи и в мессенджерах."
            if moscow else f"Лично встречаюсь только в Москве, а клиентам {prep} удобнее онлайн: созвон, мессенджеры, демонстрация экрана. Так проект идёт без поездок и согласований через посредников — а результат тот же.")
    near = [x for x in CITIES if x[0] != slug]
    h = int(hashlib.md5(slug.encode()).hexdigest(), 16)
    near = [near[(h + j * 3) % len(near)] for j in range(8)]
    near = list({x[0]: x for x in near}.values())
    nl_html = "".join(f'<a href="/cities/{x[0]}/">{E(x[1])}</a>' for x in near)
    faq = [
      (f"Сколько стоит сайт {prep}?", f"Цены не зависят от города: лендинг под ключ — {pl}, интернет-магазин до 100 артикулов — от {ps}, нейрокарточки для маркетплейсов — {pc} за штуку. В течение года дополнительно платите только за домен — около {money(CFG['domain_cost'])}."),
      (f"Как заказать сайт {prep}, если мы не в Москве?" if not moscow else "Можно ли встретиться лично?", ("Всё проходит онлайн: вы присылаете материалы, мы созваниваемся или переписываемся, а готовый сайт запускается на вашем домене. Для вас ничего не меняется по сравнению со встречей лично." if not moscow else "Да, в Москве. Договоримся о времени и месте, обсудим проект вживую. Если вам удобнее онлайн, всё делается удалённо.")),
      ("За какое время делается сайт?", "Одностраничный сайт — за 3 дня с момента предоплаты. Для интернет-магазина срок зависит от количества артикулов и обсуждается заранее."),
      (f"Попадёт ли сайт в выдачу по запросам {prep}?", "Я закладываю техническую основу: скорость, мета-теги, микроразметку, карту сайта и локальные данные. Позиции зависят ещё и от конкуренции и контента, поэтому гарантировать конкретное место нельзя, но сайт будет полностью готов к индексации."),
    ]
    crumbs = [("Главная", "/"), ("Города", "/cities/"), (f"Создание сайтов {prep}", url_)]
    local = [f"заполните карточку компании в Яндекс Бизнесе, Google Business Profile и 2ГИС — название, адрес, график, телефон, категории, фото",
             f"укажите на сайте район, зоны обслуживания и адрес так же, как в карточках: данные должны совпадать до мелочей",
             f"добавьте отзывы клиентов и отвечайте на них — они влияют на выбор человека и на видимость организации",
             f"используйте запросы с названием города в заголовках и текстах: «{prep}», «в городе», названия районов"]
    inner = (crumbs_html(crumbs) +
      f'<section class="sec" style="padding-top:36px"><div class="wrap g2"><div><span class="eyebrow">{E(name)}</span><h1 style="font-size:clamp(32px,5vw,58px)">Создание сайтов {E(prep)} под ключ</h1>'
      f'<p class="lead">Лендинг за 3 дня — {pl}. Интернет-магазин — от {ps}. SEO внутри, быстрая загрузка на телефоне, заявки в мессенджеры. Актуальные подходы <span data-year>{YEAR}</span> года.</p>'
      f'<div class="btns"><a class="btn" href="/#quiz">Рассчитать стоимость</a><a class="btn ghost" href="{CFG["telegram"]}" target="_blank" rel="noopener">{IC["tg"]} Написать в Telegram</a></div></div>'
      f'<div class="frame">{pic("service-landing", f"Макет одностраничного сайта на ноутбуке и смартфоне — создание сайтов {prep}", sizes="(max-width:1020px) 100vw, 560px", eager=True, maxw=1200)}</div></div></section>'
      f'<section class="sec alt"><div class="wrap g2"><div><span class="eyebrow">Почему я</span><h2>Сайты для бизнеса {E(prep)}</h2>'
      f'<p>{E(note)}</p><p>Бизнес {prep}, как правило, связан с такими направлениями: {E(sectors)}. Для каждого из них важны скорость загрузки, понятные цены и быстрый контакт — это и закладывается в сайт.</p><p>{meet}</p></div>'
      f'<div><table><thead><tr><th>Услуга</th><th>Срок</th><th>Цена</th></tr></thead><tbody><tr><td>Лендинг под ключ</td><td>3 дня</td><td>{pl}</td></tr><tr><td>Интернет-магазин до 100 артикулов</td><td>по договорённости</td><td>от {ps}</td></tr><tr><td>Нейрокарточки для маркетплейсов</td><td>по объёму</td><td>{pc} / шт</td></tr></tbody></table>'
      f'<p class="mut" style="font-size:14px">Предоплата {pp}, остальное — после готовности. Домен (около {money(CFG["domain_cost"])} в год) оформляется на вас. <a href="/terms/">Условия работы</a>.</p></div></div></section>'
      f'<section class="sec"><div class="wrap"><div class="sec-head"><span class="eyebrow">Ниши</span><h2>Какие сайты заказывают {E(prep)}</h2><p class="lead">Читайте практические статьи по вашей теме: зачем нужен сайт, что на нём должно быть и как он приводит клиентов.</p></div><div class="g4">{cards}</div></div></section>'
      f'<section class="sec alt"><div class="wrap g2"><div><span class="eyebrow">Локальное SEO</span><h2>Как сайту быть заметным {E(prep)}</h2><p>Сайт — только часть картины. Чтобы клиенты вас находили, сделайте четыре вещи:</p></div><div>{b_blog.ol(local)}</div></div></section>'
      f'<section class="sec"><div class="wrap" style="max-width:860px"><div class="sec-head"><span class="eyebrow">FAQ</span><h2>Вопросы клиентов {E(prep)}</h2></div><div class="faq">{"".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in faq)}</div>'
      f'<div class="btns" style="margin-top:34px"><a class="btn" href="/#contacts">Обсудить проект</a><a class="btn ghost" href="tel:{CFG["phone"]}">Позвонить {CFG["phone_view"]}</a></div></div></section>'
      f'<section class="sec alt"><div class="wrap"><h2 style="font-size:clamp(24px,3vw,34px)">Другие города</h2><div class="cities" style="margin-top:20px">{nl_html}<a href="/cities/">Все города →</a></div></div></section>')
    svc = {"@context": "https://schema.org", "@type": "Service", "@id": SITE + url_ + "#service", "name": f"Создание сайтов {prep}", "serviceType": "Web development", "provider": {"@id": SITE + "/#org"},
           "areaServed": {"@type": "City", "name": name}, "url": SITE + url_,
           "offers": [{"@type": "Offer", "name": "Лендинг под ключ", "price": CFG["price_landing"], "priceCurrency": "RUB"}, {"@type": "Offer", "name": "Интернет-магазин до 100 артикулов", "priceSpecification": {"@type": "PriceSpecification", "minPrice": CFG["price_shop"], "priceCurrency": "RUB"}}]}
    faqs = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
    return url_, title, desc, page("ru", url_, title, desc, inner, schemas=[svc, faqs, crumbs_schema(crumbs)], has_pre=False, og_alt=f"Создание сайтов {prep} — DMITRY·WEB")

def cities_hub():
    title = f"Создание сайтов в {len(CITIES)} городах России — под ключ за 3 дня | DMITRY·WEB"
    desc = f"Делаю сайты для бизнеса в {len(CITIES)} городах России и по всему миру: лендинг {money(CFG['price_landing'])} за 3 дня, интернет-магазин от {money(CFG['price_shop'])}. Личная встреча в Москве."
    crumbs = [("Главная", "/"), ("Города", "/cities/")]
    cards = "".join(f'<a class="card post rv" href="/cities/{c[0]}/" style="padding:22px;gap:6px;text-decoration:none"><h3 style="margin:0 0 6px">Сайты {E(c[2])}</h3><p style="margin:0;font-size:14px">{E(c[4].capitalize())}</p></a>' for c in CITIES)
    inner = (crumbs_html(crumbs) + f'<section class="sec" style="padding-top:36px"><div class="wrap"><div class="sec-head"><span class="eyebrow">География</span><h1 style="font-size:clamp(32px,5vw,56px)">Создание сайтов по городам России</h1>'
             f'<p class="lead">Работаю с клиентами из любых регионов онлайн, лично встречаюсь в Москве. Выберите город, чтобы увидеть условия и полезные материалы.</p></div><div class="g3">{cards}</div></div></section>')
    schema = {"@context": "https://schema.org", "@type": "CollectionPage", "name": title, "url": SITE + "/cities/", "inLanguage": "ru", "isPartOf": {"@id": SITE + "/#site"},
              "mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": SITE + f"/cities/{c[0]}/", "name": f"Создание сайтов {c[2]}"} for i, c in enumerate(CITIES)]}}
    return page("ru", "/cities/", title, desc, inner, schemas=[schema, crumbs_schema(crumbs)], has_pre=False)
