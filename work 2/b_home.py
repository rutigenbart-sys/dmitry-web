# -*- coding: utf-8 -*-
import json, os, datetime
from b_common import *
from data_cities import CITIES
from data_niches import N
import b_blog

def money(n): return f"{n:,}".replace(",", " ") + " ₽"

def load_reviews():
    p = os.path.join(ROOT, "reviews.json")
    if not os.path.exists(p): return []
    return [r for r in json.load(open(p, encoding="utf-8")) if r.get("published")]

def faq_items(lang):
    pl, ps, pc, pp = money(CFG["price_landing"]), money(CFG["price_shop"]), money(CFG["price_card"]), money(CFG["prepay"])
    if lang == "ru":
        return [
         ("Сколько стоит сайт и что входит в цену?", f"Одностраничный сайт (лендинг) под ключ стоит {pl}. В цену входят дизайн, адаптивная вёрстка, SEO-настройка, формы заявок, кнопки звонка и мессенджеров, политика конфиденциальности и подключение аналитики. Скрытых платежей нет: в течение года вы платите только за домен — около {money(CFG['domain_cost'])}."),
         ("За какое время делается сайт?", "Одностраничный сайт — за 3 дня с момента предоплаты. Чтобы уложиться в срок, пришлите все материалы сразу: тексты или описание бизнеса, фотографии, логотип (если есть), контакты и пожелания."),
         ("Как проходит оплата?", f"Предоплата {pp}, остальное — после готовности сайта. Если после предоплаты материалы не переданы вовремя, проект всё равно закрывается через 3 дня и оставшаяся сумма оплачивается в этот срок: у меня очередь из заказов."),
         ("Сколько стоит интернет-магазин?", f"Интернет-магазин до 100 артикулов — от {ps} под ключ: каталог, карточки товаров, корзина и форма заказа, SEO-настройка. От вас нужны папки по артикулам: в каждой — описание товара и фотографии для галереи."),
         ("Что такое нейрокарточки для маркетплейсов?", f"Вы присылаете фотографии товара, а я делаю с помощью нейросетей и дизайна продающие карточки с инфографикой для Wildberries, Ozon и других площадок. Стоимость — {pc} за одну карточку."),
         ("Сайт попадёт в топ Яндекса и Google?", "Я закладываю в сайт всё, что зависит от разработчика: скорость, чистую структуру, микроразметку, карту сайта и мета-теги. Но позиции в выдаче зависят ещё и от конкуренции, контента и времени, поэтому гарантировать конкретное место честно нельзя. Хорошая техническая основа и регулярный контент — лучший путь к росту."),
         ("На каком домене будет сайт и кому он принадлежит?", "Домен регистрируется на вас — это ваш актив. Я подскажу, как выбрать короткий и запоминаемый адрес в зоне .ru и помогу с подключением."),
         ("Можно встретиться лично?", "Да, в Москве. Остальные города и страны — онлайн: созвоны, мессенджеры, демонстрация экрана. Работаю с любыми регионами и на русском и английском языках, при необходимости сделаю сайт и на других языках."),
        ]
    return [
     ("How much does a website cost and what is included?", f"A one-page website (landing page) costs {pl} turnkey. It includes design, responsive layout, SEO setup, lead forms, call and messenger buttons, a privacy policy and analytics. No hidden fees: during the year you only pay for the domain, about {money(CFG['domain_cost'])}."),
     ("How long does it take?", "A one-page website takes 3 days from the prepayment. To keep to the deadline, send all materials at once: texts or a business description, photos, a logo (if you have one), contacts and wishes."),
     ("How does payment work?", f"Prepayment of {pp}, the rest after the site is ready. If materials are not provided on time, the project is still closed after 3 days and the remaining amount is due then."),
     ("How much is an online store?", f"An online store of up to 100 products starts at {ps} turnkey: catalogue, product pages, cart and order form, SEO setup. You provide folders per product with a description and gallery photos."),
     ("What are AI product cards?", f"You send product photos and I create selling cards with infographics for Wildberries, Ozon and other marketplaces using AI tools and design. The price is {pc} per card."),
     ("Will the site reach the top of Google and Yandex?", "I build in everything a developer controls: speed, clean structure, structured data, sitemap and meta tags. Rankings also depend on competition, content and time, so no honest developer can promise a specific position."),
     ("Who owns the domain?", "The domain is registered in your name — it is your asset. I will help you choose a short memorable .ru name and connect it."),
     ("Can we meet in person?", "Yes, in Moscow. Other cities and countries are handled online. I work worldwide in Russian and English, and can build a site in other languages on request."),
    ]

def home(lang):
    ru = lang == "ru"
    L = lambda a, b: a if ru else b
    home_path = "/" if ru else "/en/"
    pl, ps, pc, pp = money(CFG["price_landing"]), money(CFG["price_shop"]), money(CFG["price_card"]), money(CFG["prepay"])
    yr = f'<span data-year>{datetime.date.today().year}</span>'
    pre = "/#" if ru else "/en/#"
    # ---------- hero
    hero = f'''<section class="hero" id="top">{deco("hero-grid", "hero-bg")}<div class="wrap"><div class="hero-grid">
<div class="hero-copy"><span class="eyebrow">{L("Создание сайтов с нуля · Москва и весь мир","Websites from scratch · Moscow and worldwide")}</span>
<h1>{L('Создаю сайты <em>с&nbsp;нуля</em> под&nbsp;ключ за&nbsp;3&nbsp;дня','I build websites <em>from scratch</em>, turnkey, in 3&nbsp;days')}</h1>
<p class="lead">{L(f"Быстрые адаптивные сайты со встроенным SEO — по актуальным правилам {yr} года. Лендинг — {pl} без скрытых платежей: в течение года вы платите только за домен (около {money(CFG['domain_cost'])}).",
 f"Fast responsive websites with built-in SEO, following the {yr} rules. Landing page — {pl} with no hidden fees: during the year you only pay for the domain (about {money(CFG['domain_cost'])}).")}</p>
<div class="btns"><a class="btn" href="#quiz" data-goal="hero_quiz">{L("Рассчитать и зафиксировать цену","Calculate and lock the price")}</a>
<a class="btn ghost" href="{CFG['telegram']}" target="_blank" rel="noopener" data-goal="click_telegram">{IC["tg"]} {L("Написать в Telegram","Message on Telegram")}</a></div>
<div class="chips"><span class="chip"><b>3 {L("дня","days")}</b> {L("срок лендинга","for a landing")}</span><span class="chip"><b>{pl}</b> {L("под ключ","turnkey")}</span><span class="chip"><b>RU / EN</b> {L("версии сайта","site versions")}</span><span class="chip"><b>{L("Москва","Moscow")}</b> {L("личная встреча","meet in person")}</span></div></div>
<figure class="portrait" style="margin:0">{pic("portrait", L("Дмитрий — разработчик сайтов с опытом 10 лет, Москва: чёрно-белый портрет на тёмном фоне","Dmitry — web developer with 10 years of experience, Moscow: black and white portrait on a dark background"), sizes="(max-width:1020px) 380px, 460px", eager=True, maxw=832)}
<figcaption>{L("Дмитрий — разработчик сайтов с опытом 10 лет","Dmitry — web developer with 10 years of experience")}</figcaption></figure>
</div></div></section>'''
    # ---------- marquee
    items = "".join(f'<a href="{b_blog.art_url(n, "zachem")}">{E(L("Сайт для " + n["gen"], "Website: " + n["name"]))}</a>' for n in N)
    items = items.replace("Website: ", "Website: ") if not ru else items
    strip = f'<div class="strip" aria-label="{L("Ниши, для которых я делаю сайты","Niches I build websites for")}"><div class="strip-in">{items}{items}</div></div>'
    if not ru:
        strip = f'<div class="strip" aria-label="Niches I build websites for"><div class="strip-in">' + "".join(f'<a href="{b_blog.art_url(n, "zachem")}" hreflang="ru" lang="ru">Сайт для {E(n["gen"])}</a>' for n in N) * 2 + '</div></div>'
    # ---------- about
    about = f'''<section class="sec" id="about"><div class="wrap g2">
<div class="rv"><span class="eyebrow">{L("Обо мне","About me")}</span><h2>{L("Дмитрий. Делаю сайты с нуля — 10&nbsp;лет опыта","Dmitry. I build websites from scratch — 10&nbsp;years of experience")}</h2>
<p class="lead">{L("Я не продаю шаблоны. Каждый сайт проектирую под вашу задачу: чтобы он быстро открывался, нравился людям и приводил заявки.","I do not sell templates. Every site is designed around your goal: it opens fast, earns trust and brings enquiries.")}</p>
<div class="facts"><div class="fact"><b>10</b><span>{L("лет опыта","years of experience")}</span></div><div class="fact"><b>3</b><span>{L("дня на лендинг","days for a landing")}</span></div><div class="fact"><b>2</b><span>{L("языка: RU и EN","languages: RU and EN")}</span></div></div>
<ul class="ticks"><li>{L("Работаю на результат: сайт должен приводить обращения, а не просто выглядеть красиво","Result-driven: a site must bring enquiries, not just look good")}</li>
<li>{L("Один исполнитель от идеи до запуска — без менеджеров и пересказов между людьми","One person from idea to launch — no account managers, no lost-in-translation")}</li>
<li>{L("Личная встреча в Москве: можно обсудить сайт или проект вживую. Это возможно далеко не у каждого подрядчика","In-person meeting in Moscow: we can discuss your site or project face to face")}</li>
<li>{L("Работаю с любыми городами и странами онлайн, на русском и английском, по запросу — на других языках","I work online with any city or country, in Russian and English, other languages on request")}</li></ul>
<a class="btn" href="#contacts">{L("Обсудить проект","Discuss your project")}</a></div>
<div class="frame rv">{pic("about-workspace", L("Рабочее место разработчика сайтов Дмитрия: ноутбук с кодом, чашка кофе и настольная лампа в тёмной комнате","Web developer Dmitry's workspace: a laptop with code, a coffee cup and a desk lamp in a dark room"), sizes="(max-width:1020px) 100vw, 560px")}</div></div></section>'''
    # ---------- services
    def svc(img, alt, tag, title, price, unit, lis, cta, goal):
        li = "".join(f"<li>{x}</li>" for x in lis)
        return f'''<article class="card pad0 svc rv">{pic(img, alt, sizes="(max-width:680px) 100vw, (max-width:1020px) 50vw, 380px")}<div class="in"><span class="tag">{tag}</span><h3>{title}</h3>
<div class="price">{price}<small>{unit}</small></div><ul>{li}</ul><a class="btn sm" href="#quiz" data-goal="{goal}">{cta}</a></div></article>'''
    services = f'''<section class="sec alt" id="services"><div class="wrap"><div class="sec-head rv"><span class="eyebrow">{L("Услуги и цены","Services and prices")}</span><h2>{L("Понятные цены под ключ","Clear turnkey prices")}</h2>
<p class="lead">{L("Фиксированная стоимость, фиксированные сроки и никаких скрытых платежей.","Fixed price, fixed deadlines and no hidden fees.")}</p></div>
<div class="g3">
{svc("service-landing", L("Макет одностраничного сайта на ноутбуке и смартфоне — лендинг под ключ за 3 дня","One-page website mockup on a laptop and a smartphone — landing page turnkey in 3 days"), L("Самое популярное","Most popular"), L("Лендинг","Landing page"), "15 000 ₽".replace(" ", "&nbsp;"), L("под ключ","turnkey"),
  [L("Срок — 3 дня","Delivered in 3 days"), L("Дизайн под ваш бизнес, адаптив под все экраны","Custom design, responsive on every screen"), L("SEO внутри: title, description, Schema.org, Open Graph, sitemap","SEO built in: title, description, Schema.org, Open Graph, sitemap"), L("Кнопки звонка, Telegram, WhatsApp, Max","Call, Telegram, WhatsApp and Max buttons"), L("Формы со спам-защитой, заявки в Telegram","Spam-protected forms, leads to Telegram"), L("Политика конфиденциальности и подключение аналитики","Privacy policy and analytics setup")], L("Заказать лендинг","Order a landing"), "svc_landing")}
{svc("service-shop", L("Интернет-магазин на ноутбуке: каталог товаров, корзина и сумка с покупкой на тёмном столе","Online store on a laptop: product catalogue, cart and a shopping bag on a dark desk"), L("До 100 артикулов","Up to 100 products"), L("Интернет-магазин","Online store"), L("от&nbsp;55&nbsp;000&nbsp;₽","from&nbsp;55,000&nbsp;₽"), L("под ключ","turnkey"),
  [L("Каталог, карточки товаров с галереей","Catalogue and product pages with gallery"), L("Корзина и форма заказа, заказы в Telegram","Cart and order form, orders to Telegram"), L("SEO карточек и микроразметка Product","Product SEO and structured data"), L("От вас — папки по артикулам: описание и фото","From you — a folder per product: description and photos"), L("Быстрая загрузка на мобильных","Fast on mobile")], L("Рассчитать магазин","Calculate a store"), "svc_shop")}
{svc("service-cards", L("Фото кроссовка до и после: обычный снимок на столе и рекламная нейрокарточка с графикой","A sneaker before and after: an ordinary photo on a table and a promotional AI product card"), L("Для маркетплейсов","For marketplaces"), L("Нейрокарточки товаров","AI product cards"), L("350&nbsp;₽","350&nbsp;₽"), L("за карточку","per card"),
  [L("Нейрогенерация и инфографика","AI generation and infographics"), L("Wildberries, Ozon, Яндекс Маркет","Wildberries, Ozon, Yandex Market"), L("Вы присылаете любое фото товара","You send any product photo"), L("Выделяют товар в выдаче маркетплейса","Make your product stand out in the feed")], L("Заказать карточки","Order cards"), "svc_cards")}
</div></div></section>'''
    # ---------- speed / tech
    tech = [
     (L("Загрузка менее 2 секунд","Loads in under 2 seconds"), L("Цель — зелёная зона Core Web Vitals в PageSpeed Insights","Goal: green Core Web Vitals in PageSpeed Insights")),
     ("AVIF / WebP", L("Лёгкие изображения нового поколения с запасным JPG","Next-gen lightweight images with JPG fallback")),
     ("Schema.org", L("Разметка организации, услуг, статей и хлебных крошек","Markup for organization, services, articles and breadcrumbs")),
     ("sitemap.xml · robots.txt", L("Поисковики быстро находят и индексируют страницы","Search engines find and index pages quickly")),
     ("Open Graph", L("Красивое превью ссылки в Telegram и WhatsApp","Rich link previews in Telegram and WhatsApp")),
     ("hreflang · RU / EN", L("Отдельные title и description для каждого языка","Separate title and description for each language")),
     (L("Mobile-first","Mobile-first"), L("Сначала проектирую под смартфон, затем под ПК","Designed for smartphones first, then desktop")),
     (L("Доступность","Accessibility"), L("Контраст, фокус, семантика, поддержка клавиатуры","Contrast, focus, semantics, keyboard support")),
    ]
    tg = "".join(f"<div><b>{a}</b>{b}</div>" for a, b in tech)
    speed = f'''<section class="sec speed" id="speed">{deco("speed-tunnel", "speed-bg")}<div class="wrap"><div class="sec-head rv"><span class="eyebrow">{L("Технологии","Technology")}</span>
<h2>{L(f"Быстро на любом устройстве и актуально в {yr}&nbsp;году","Fast on every device and up to date in " + yr)}</h2>
<p class="lead">{L("Правила поисковиков меняются, поэтому я строю сайты на стандартах, которые не устаревают, и слежу за обновлениями. Ваш сайт остаётся современным и в следующем году, и через пять лет.","Search rules change, so I build on lasting standards and follow the updates. Your website stays modern next year and five years from now.")}</p></div>
<div class="tech rv" style="max-width:820px">{tg}</div></div></section>'''
    # ---------- process
    proc = f'''<section class="sec" id="process"><div class="wrap"><div class="sec-head rv"><span class="eyebrow">{L("Как это работает","How it works")}</span><h2>{L("Три дня от предоплаты до запуска","Three days from prepayment to launch")}</h2></div>
<div class="steps rv"><div class="step"><span class="num">{L("ДЕНЬ 1","DAY 1")}</span><h3>{L("Бриф и структура","Brief and structure")}</h3><p>{L("Получаю материалы, уточняю задачи, продумываю структуру и оффер под вашу аудиторию.","I receive your materials, clarify goals and design the structure and offer for your audience.")}</p></div>
<div class="step"><span class="num">{L("ДЕНЬ 2","DAY 2")}</span><h3>{L("Дизайн и вёрстка","Design and build")}</h3><p>{L("Рисую дизайн, верстаю адаптивный сайт, подключаю формы, кнопки связи и заявки в Telegram.","I design and code the responsive site, connect forms, contact buttons and Telegram leads.")}</p></div>
<div class="step"><span class="num">{L("ДЕНЬ 3","DAY 3")}</span><h3>{L("SEO, проверка и запуск","SEO, QA and launch")}</h3><p>{L("Настраиваю SEO, проверяю скорость и ошибки, запускаю сайт и подключаю Метрику и Вебмастер.","I set up SEO, test speed and errors, launch the site and connect Metrica and Webmaster tools.")}</p></div></div>
<p class="mut rv" style="margin-top:22px;max-width:70ch">{L("Чтобы уложиться в три дня, передайте все материалы сразу: описание бизнеса или тексты, фотографии, логотип (если есть), контакты и пожелания по дизайну.","To finish in three days, send all materials at once: business description or texts, photos, a logo (if any), contacts and design wishes.")}</p></div></section>'''
    # ---------- quiz
    qopt = lambda name, val, price, title, sub, checked=False: (f'<label class="opt"><input type="radio" name="{name}" value="{val}"{" checked" if checked else ""}><span><b>{title}</b><small>{sub}</small></span><span class="p">{price}</span></label>')
    quiz = f'''<section class="sec alt" id="quiz"><div class="wrap"><div class="sec-head rv"><span class="eyebrow">{L("Калькулятор","Calculator")}</span><h2>{L("Рассчитайте стоимость за минуту","Calculate the price in a minute")}</h2>
<p class="lead">{L(f"Три шага — и вы увидите цену. Её можно зафиксировать, внеся предоплату {pp}.",f"Three steps and you see the price. Lock it with a {pp} prepayment.")}</p></div>
<form class="quiz rv" id="quizform" data-prepay="{CFG["prepay"]}" novalidate>{deco("quiz-bg", "quiz-bg")}
<div class="quiz-in"><div>
<div class="qbar" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
<div hidden><span data-lab="rLanding">{L("Лендинг","Landing page")}</span><span data-lab="rShop">{L("Интернет-магазин","Online store")}</span><span data-lab="rSkus">{L("Артикулов","Products")}</span><span data-lab="rCards">{L("Нейрокарточки","AI cards")}</span><span data-lab="rAddCards">{L("Доп. нейрокарточки","Extra AI cards")}</span><span data-lab="rExtra">{L("Опции","Options")}</span></div>
<fieldset class="qstep on" style="border:0;padding:0;margin:0"><legend class="eyebrow" style="padding:0">{L("Шаг 1 из 3","Step 1 of 3")}</legend><h3>{L("Что вам нужно?","What do you need?")}</h3><div class="opts">
{qopt("type","landing",pl,L("Лендинг","Landing page"),L("Одностраничный сайт под ключ за 3 дня","One-page website turnkey in 3 days"),True)}
{qopt("type","shop",L("от ","from ")+ps,L("Интернет-магазин","Online store"),L("Каталог, корзина, форма заказа","Catalogue, cart, order form"))}
{qopt("type","card",pc+L(" / шт"," / pc"),L("Нейрокарточки для маркетплейсов","AI cards for marketplaces"),L("Только карточки товаров, без сайта","Product cards only, no website"))}
</div><div class="qnav"><button type="button" class="btn" data-next>{L("Далее","Next")}</button></div></fieldset>
<fieldset class="qstep" style="border:0;padding:0;margin:0"><legend class="eyebrow" style="padding:0">{L("Шаг 2 из 3","Step 2 of 3")}</legend><h3>{L("Объём работы","Scope")}</h3>
<div data-for="landing"><p class="mut">{L("Лендинг включает всё необходимое: дизайн, адаптив, SEO, формы и контакты. Приступим к опциям.","The landing page includes everything: design, responsive layout, SEO, forms and contacts. On to the options.")}</p></div>
<div data-for="shop" hidden><div class="opts">
<label class="opt"><input type="radio" name="skus" value="{L("до 100","up to 100")}" checked><span><b>{L("До 100 артикулов","Up to 100 products")}</b><small>{L("Входит в базовую цену","Included in the base price")}</small></span></label>
<label class="opt"><input type="radio" name="skus" value="{L("больше 100","over 100")}"><span><b>{L("Больше 100 артикулов","Over 100 products")}</b><small>{L("Стоимость обсудим индивидуально","We will discuss the price individually")}</small></span></label></div></div>
<div data-for="card" hidden><p class="mut">{L("Сколько карточек нужно?","How many cards do you need?")}</p><div class="qty"><input type="range" name="qty" min="1" max="200" value="10" aria-label="{L("Количество карточек","Number of cards")}"><output id="qty-out">10</output></div></div>
<div class="qnav"><button type="button" class="btn ghost" data-prev>{L("Назад","Back")}</button><button type="button" class="btn" data-next>{L("Далее","Next")}</button></div></fieldset>
<fieldset class="qstep" style="border:0;padding:0;margin:0"><legend class="eyebrow" style="padding:0">{L("Шаг 3 из 3","Step 3 of 3")}</legend><h3>{L("Что ещё нужно?","Anything else?")}</h3><div class="opts">
<label class="opt"><input type="checkbox" name="extra" value="{L("Версия на английском","English version")}"><span><b>{L("Версия на английском","English version")}</b><small>{L("Отдельные title и description для каждого языка","Separate title and description per language")}</small></span></label>
<label class="opt"><input type="checkbox" name="extra" value="{L("Блог со статьями","Blog with articles")}"><span><b>{L("Блог со статьями","Blog with articles")}</b><small>{L("Структура под SEO-статьи","Structure for SEO articles")}</small></span></label>
<label class="opt"><input type="checkbox" name="extra" value="{L("Страницы по городам","City pages")}"><span><b>{L("Страницы по городам","City pages")}</b><small>{L("Региональное продвижение","Regional promotion")}</small></span></label>
<label class="opt" id="addcards-box"><input type="checkbox" name="addcards"><span><b>{L("Нейрокарточки для маркетплейсов","AI product cards")}</b><small>{pc} {L("за карточку","per card")}</small></span></label>
<div id="addqty-box" hidden class="qty" style="padding:0 6px"><input type="range" name="addqty" min="1" max="200" value="20" aria-label="{L("Количество карточек","Number of cards")}"><output id="addqty-out">20</output></div>
</div><div class="qnav"><button type="button" class="btn ghost" data-prev>{L("Назад","Back")}</button><button type="button" class="btn" data-next>{L("Зафиксировать цену","Lock the price")}</button></div></fieldset>
<fieldset class="qstep" style="border:0;padding:0;margin:0"><legend class="eyebrow" style="padding:0">{L("Финал","Final")}</legend><h3>{L("Оставьте контакт — зафиксирую цену","Leave a contact — I will lock the price")}</h3>
<div class="form"><div class="fld"><label for="q-name">{L("Имя","Name")}</label><input id="q-name" name="name" autocomplete="name" required></div>
<div class="fld"><label for="q-contact">{L("Телефон или Telegram","Phone or Telegram")}</label><input id="q-contact" name="contact" autocomplete="tel" required></div>
<div class="fld"><label for="q-comment">{L("Комментарий (необязательно)","Comment (optional)")}</label><textarea id="q-comment" name="comment"></textarea></div>
<div class="hp" aria-hidden="true"><label>Website <input name="website" tabindex="-1" autocomplete="off"></label></div>
<label class="agree"><input type="checkbox" name="agree" required><span>{L(f'Согласен на обработку персональных данных согласно <a href="/privacy/" target="_blank">политике конфиденциальности</a> и с <a href="/terms/" target="_blank">условиями работы</a>.',f'I agree to personal data processing under the <a href="/en/privacy/" target="_blank">privacy policy</a> and accept the terms (prepayment means acceptance; delivery in 3 days).')}</span></label>
<div class="msg" role="status" aria-live="polite"></div>
<div class="btns"><button class="btn" type="submit">{L("Отправить и зафиксировать цену","Send and lock the price")}</button><button type="button" class="btn ghost" data-prev>{L("Назад","Back")}</button></div>
<a id="payBtn" class="btn" hidden href="{E(CFG["pay_url"]) if CFG.get("pay_url") else CFG["telegram"]}" target="_blank" rel="noopener">{L("Перейти к предоплате","Go to prepayment")}</a></div></fieldset>
</div>
<aside class="qres" aria-live="polite"><span class="eyebrow">{L("Ваша стоимость","Your price")}</span><div class="sum">0 ₽</div><dl class="qlist"></dl><hr>
<div class="pre qpre"><span>{L("Предоплата","Prepayment")}</span><span class="pv">{pp}</span></div>
<p class="mut qnote" hidden style="font-size:14px">{L("Условия оплаты нейрокарточек согласуем в мессенджере.","We will agree the payment terms for AI cards in the messenger.")}</p>
<p class="mut" style="font-size:13px;margin:14px 0 0">{L("Предоплата означает согласие со сроком изготовления 3 дня.","Prepayment means you accept the 3-day delivery term.")}</p></aside></div></form></div></section>'''
    # ---------- cases (concepts) + reviews
    def case(img, alt, title, n, desc):
        return f'''<a class="card pad0 post case rv" href="{b_blog.art_url(n, "struktura")}"{"" if ru else ' hreflang="ru" lang="ru"'}><span class="tag">{L("Концепт","Concept")}</span>{pic(img, alt, sizes="(max-width:680px) 100vw, (max-width:1020px) 50vw, 380px")}<div class="in"><h3>{title}</h3><p>{desc}</p></div></a>'''
    nmap = {n["slug"]: n for n in N}
    cases = f'''<section class="sec" id="cases"><div class="wrap"><div class="sec-head rv"><span class="eyebrow">{L("Кейсы","Cases")}</span><h2>{L("Концепты сайтов для разных ниш","Website concepts for different niches")}</h2>
<p class="lead">{L("Это демонстрационные макеты: так может выглядеть ваш сайт. Реальные проекты и отзывы клиентов добавляются по мере запуска.","These are demonstration mockups of how your site could look. Real projects and client reviews are added as they launch.")}</p></div>
<div class="g3">{case("case-carwash", L("Макет сайта автомойки на ноутбуке: тёмный дизайн с фото чёрного автомобиля в пене","Car wash website mockup on a laptop: dark design with a photo of a black car covered in foam"), L("Автомойка","Car wash"), nmap["avtomoyka"], L("Прайс по классам авто, запись онлайн, карта и акции.","Prices by car class, online booking, map and offers."))}
{case("case-kitchen", L("Макет сайта кухонь на заказ на ноутбуке: светлая вёрстка с фото современной кухни","Custom kitchens website mockup on a laptop: light layout with a photo of a modern kitchen"), L("Кухни на заказ","Custom kitchens"), nmap["kuhni"], L("Портфолио по стилям, материалы, запись на замер.","Portfolio by style, materials, booking a measurement visit."))}
{case("case-factory", L("Макет сайта завода на ноутбуке в мастерской: фото станков и каталог продукции","Factory website mockup on a laptop in a workshop: photo of machinery and a product catalogue"), L("Завод и производство","Factory and manufacturing"), nmap["zavod"], L("Каталог продукции, мощности, сертификаты, запрос КП.","Product catalogue, capacity, certificates, quotation request."))}
</div></div></section>'''
    revs = load_reviews()
    if revs:
        rcards = "".join(f'<figure class="card rev rv" style="margin:0"><q>{E(r["text"])}</q><figcaption><b>{E(r["name"])}</b><br><span class="mut">{E(r.get("role",""))}</span></figcaption></figure>' for r in revs[:6])
        cases += f'<section class="sec alt" id="reviews"><div class="wrap"><div class="sec-head rv"><span class="eyebrow">{L("Отзывы","Reviews")}</span><h2>{L("Что говорят клиенты","What clients say")}</h2></div><div class="g3">{rcards}</div></div></section>'
    # ---------- guarantees
    gl = [("clock", L("Фиксированные сроки","Fixed deadlines"), L("Лендинг — за 3 дня с момента предоплаты.","Landing page in 3 days from the prepayment.")),
          ("check", L("Работа на результат","Result-driven"), L("Сайт строится под ваши заявки, а не ради картинки.","The site is built for your enquiries, not for looks only.")),
          ("doc", L("Честные условия","Honest terms"), L("Цена фиксируется заранее, скрытых платежей нет.","The price is fixed upfront, no hidden fees.")),
          ("shield", L("Официальный подход","Official approach"), L("Работаю как самозанятый, выдаю чек.","I work as self-employed and issue a receipt.")),
          ("pin", L("Личная встреча в Москве","Meeting in Moscow"), L("Обсудим проект вживую. В других городах — онлайн.","We can discuss the project in person. Elsewhere — online.")),
          ("globe", L("Домен — ваш","The domain is yours"), L("Адрес регистрируется на вас и остаётся вашим активом.","The address is registered in your name and remains your asset."))]
    gcards = "".join(f'<div class="card">{sico(i)}<h3>{t}</h3><p>{d}</p></div>' for i, t, d in gl)
    guar = f'''<section class="sec alt" id="guarantees"><div class="wrap"><div class="guar"><div class="rv frame">{pic("guarantee-shield", L("Стеклянный щит с тонкими белыми линиями — символ надёжности и защиты проекта","A glass shield with thin white lines — a symbol of reliability and project protection"), sizes="(max-width:1020px) 100vw, 480px")}</div>
<div class="rv"><span class="eyebrow">{L("Гарантии и условия","Guarantees and terms")}</span><h2>{L("Снимаю риски до начала работы","Removing the risk before we start")}</h2><div class="gl">{gcards}</div></div></div>
<div class="cond rv"><b>{L("Условия:","Terms:")}</b> {L(f"предоплата {pp}, остальное — после готовности сайта. Внесение предоплаты означает согласие с тем, что одностраничный сайт изготавливается за 3 дня. Если после предоплаты материалы не переданы вовремя, проект всё равно закрывается через 3 дня и оставшаяся сумма оплачивается в этот срок — у меня очередь из заказов. Подробности — на странице <a href='/terms/'>условий работы</a>.",
 f"prepayment {pp}, the rest after the site is ready. Paying the prepayment means you accept that a one-page website is delivered in 3 days. If materials are not provided on time, the project is still closed after 3 days and the remaining amount is due then — I run a queue of orders.")}</div></div></section>'''
    # ---------- cities
    cl = "".join(f'<a href="/cities/{c[0]}/"{"" if ru else " hreflang=ru lang=ru"}>{L(c[1], c[3])}</a>' for c in CITIES)
    cities = f'''<section class="sec" id="cities"><div class="wrap"><div class="sec-head rv"><span class="eyebrow">{L("География","Geography")}</span><h2>{L("Делаю сайты по всей России и миру","Websites across Russia and worldwide")}</h2>
<p class="lead">{L("Лично встречаюсь в Москве, с остальными городами работаю онлайн — так же быстро и с тем же качеством.","I meet in person in Moscow and work online with all other cities — equally fast and with the same quality.")}</p></div>
<div class="cities rv">{cl}</div></div></section>'''
    # ---------- blog teaser
    tz = [n for n in N if n["slug"] in ("avtomoyka", "kuhni", "fotograf", "zavod", "internet-magazin", "lending")]
    pc_ = "".join(b_blog.card(n, "zachem", L, ru) for n in tz)
    blog = f'''<section class="sec alt" id="blog"><div class="wrap"><div class="sec-head rv" style="display:flex;justify-content:space-between;align-items:end;gap:20px;flex-wrap:wrap;max-width:none"><div><span class="eyebrow">{L("Блог","Blog")}</span><h2 style="margin:0">{L("Полезно о сайтах для бизнеса","Useful about business websites")}</h2></div><a class="btn ghost sm" href="/blog/">{L("Все статьи","All articles")} →</a></div>
<div class="g3" style="margin-top:36px">{pc_}</div></div></section>'''
    # ---------- domain advice
    dom = f'''<section class="sec" id="domain"><div class="wrap g2"><div class="rv"><span class="eyebrow">{L("Совет","Tip")}</span><h2>{L("Как выбрать домен для сайта","How to choose a domain")}</h2>
<p class="lead">{L("Домен почти не влияет на позиции напрямую, зато влияет на запоминаемость и доверие.","A domain barely affects rankings directly, but it affects memorability and trust.")}</p></div>
<ul class="ticks rv"><li>{L("Берите короткое запоминаемое имя в зоне <b>.ru</b> — оно проще вводится и надёжнее открывается в мессенджерах.","Pick a short memorable name in <b>.ru</b> — it is easier to type and opens more reliably in messengers.")}</li>
<li>{L("Бренд лучше длинного ключа: «ваш-бренд.ru» запоминается, а «создание-сайтов-под-ключ.ru» выглядит как спам.","A brand beats a long keyword: it is remembered, while a keyword-stuffed domain looks like spam.")}</li>
<li>{L("Не больше одного дефиса, без цифр и сложных слов.","At most one hyphen, no digits, no complex words.")}</li>
<li>{L("Регистрируйте на себя и включайте автопродление — домен ваш актив. Стоит около 500 ₽ в год.","Register it in your name and enable auto-renewal — it is your asset. About 500 ₽ per year.")}</li></ul></div></section>'''
    # ---------- faq
    fq = faq_items(lang)
    faq = f'''<section class="sec alt" id="faq"><div class="wrap" style="max-width:860px"><div class="sec-head rv"><span class="eyebrow">FAQ</span><h2>{L("Частые вопросы","Frequently asked questions")}</h2></div>
<div class="faq rv">{"".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in fq)}</div></div></section>'''
    # ---------- contacts
    contacts = f'''<section class="sec" id="contacts"><div class="wrap contact"><div class="rv"><span class="eyebrow">{L("Контакты","Contacts")}</span><h2>{L("Обсудим ваш сайт","Let us discuss your website")}</h2>
<a class="bigtel" href="tel:{CFG["phone"]}" data-goal="click_phone">{CFG["phone_view"]}</a><p class="mut"><a href="mailto:{CFG["email"]}">{CFG["email"]}</a></p>
{messengers_block(lang)}
<div class="frame">{pic("meeting-moscow", L("Москва-Сити ночью из окна кафе: ноутбук с кодом и две чашки кофе — место для личной встречи по проекту сайта","Moscow City at night seen from a cafe window: a laptop with code and two coffee cups — a place to meet about your website project"), sizes="(max-width:1020px) 100vw, 560px")}</div>
<p class="mut" style="margin-top:14px">{L("Личная встреча — в Москве. Остальные города и страны — онлайн.","In-person meetings in Moscow. Other cities and countries — online.")}</p></div>
<div class="rv"><div class="card"><h3>{L("Оставить заявку","Send a request")}</h3><p class="mut">{L("Опишите задачу — отвечу в мессенджере или по телефону.","Describe your task — I will reply in a messenger or by phone.")}</p>
<form class="form" data-lead novalidate><div class="fld"><label for="c-name">{L("Имя","Name")}</label><input id="c-name" name="name" autocomplete="name" required></div>
<div class="fld"><label for="c-contact">{L("Телефон или Telegram","Phone or Telegram")}</label><input id="c-contact" name="contact" autocomplete="tel" required></div>
<div class="fld"><label for="c-msg">{L("Что нужно сделать?","What do you need?")}</label><textarea id="c-msg" name="message"></textarea></div>
<div class="hp" aria-hidden="true"><label>Website <input name="website" tabindex="-1" autocomplete="off"></label></div>
<label class="agree"><input type="checkbox" name="agree" required><span>{L('Согласен на обработку персональных данных согласно <a href="/privacy/" target="_blank">политике конфиденциальности</a>.','I agree to personal data processing under the <a href="/en/privacy/" target="_blank">privacy policy</a>.')}</span></label>
<div class="msg" role="status" aria-live="polite"></div><button class="btn" type="submit">{L("Отправить заявку","Send request")}</button></form></div></div></div></section>'''
    body = hero + strip + about + services + speed + proc + quiz + cases + guar + cities + blog + dom + faq + contacts
    # ---------- meta + schema
    if ru:
        title = "Создание сайтов с нуля под ключ за 3 дня — лендинг 15 000 ₽ | DMITRY·WEB"
        desc = "Дмитрий, Москва: создание сайтов с нуля под ключ. Лендинг за 3 дня — 15 000 ₽, интернет-магазин от 55 000 ₽, нейрокарточки 350 ₽. SEO внутри, быстро, RU/EN."
    else:
        title = "Websites from scratch, turnkey in 3 days — landing page 15,000 ₽ | DMITRY·WEB"
        desc = "Dmitry, Moscow: websites built from scratch, turnkey. Landing page in 3 days — 15,000 RUB, online store from 55,000 RUB, AI product cards 350 RUB. SEO built in, fast, RU/EN."
    offers = [("Лендинг под ключ" if ru else "Landing page turnkey", CFG["price_landing"], False), ("Интернет-магазин до 100 артикулов" if ru else "Online store up to 100 products", CFG["price_shop"], True), ("Нейрокарточки для маркетплейсов" if ru else "AI product cards for marketplaces", CFG["price_card"], False)]
    svc_s = {"@context": "https://schema.org", "@graph": [
      {"@type": "Service", "@id": SITE + home_path + "#service", "name": "Создание сайтов с нуля под ключ" if ru else "Website development turnkey", "serviceType": "Web development", "provider": {"@id": SITE + "/#org"},
       "areaServed": [{"@type": "Country", "name": "Россия"}, {"@type": "Place", "name": "Worldwide"}],
       "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Услуги" if ru else "Services", "itemListElement": [
          {"@type": "Offer", "itemOffered": {"@type": "Service", "name": n}, "priceSpecification": ({"@type": "PriceSpecification", "price": p, "priceCurrency": "RUB", "minPrice": p} if frm else {"@type": "PriceSpecification", "price": p, "priceCurrency": "RUB"})} for n, p, frm in offers]}},
      {"@type": "WebPage", "@id": SITE + home_path + "#webpage", "url": SITE + home_path, "name": title, "description": desc, "inLanguage": lang, "isPartOf": {"@id": SITE + "/#site"}, "about": {"@id": SITE + "/#org"},
       "primaryImageOfPage": {"@type": "ImageObject", "url": SITE + "/assets/img/portrait-832.jpg"}},
      {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in fq]}]}
    prel = '<link rel="preload" as="image" href="/assets/img/portrait-640.avif" type="image/avif" imagesrcset="/assets/img/portrait-420.avif 420w, /assets/img/portrait-640.avif 640w, /assets/img/portrait-832.avif 832w" imagesizes="(max-width:1020px) 380px, 460px" fetchpriority="high">'
    alts = {"ru": "/", "en": "/en/"}
    return page(lang, home_path, title, desc, body, schemas=[org_schema(lang), svc_s], alts=alts, preload=prel,
                og_alt=L("DMITRY·WEB — создание сайтов с нуля под ключ за 3 дня", "DMITRY·WEB — websites from scratch, turnkey in 3 days"))
