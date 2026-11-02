# -*- coding: utf-8 -*-
import os, json, shutil, datetime
from b_common import *
from data_cities import CITIES
from data_niches import N
import b_blog
from b_blog import money

DATE_POL = "2 ноября 2026 г."

def legal_page(lang, path, title, desc, h1, content, alts):
    ru = lang == "ru"
    crumbs = [("Главная" if ru else "Home", "/" if ru else "/en/"), (h1, path)]
    inner = crumbs_html(crumbs, lang) + f'<section class="sec" style="padding-top:36px"><div class="wrap" style="max-width:820px"><h1 style="font-size:clamp(30px,4.5vw,48px)">{E(h1)}</h1><div class="prose">{content}</div></div></section>'
    return page(lang, path, title, desc, inner, schemas=[crumbs_schema(crumbs)], alts=alts, has_pre=False)

def privacy_ru():
    op = f"самозанятый {CFG['person_full']}" + (f", ИНН {CFG['inn']}" if CFG.get("inn") else "")
    c = f'''<p class="mut">Редакция от {DATE_POL}</p>
<h2>1. Общие положения</h2><p>Настоящая политика определяет порядок обработки и защиты персональных данных посетителей сайта {SITE.replace("https://","")} (далее — Сайт) в соответствии с Федеральным законом № 152-ФЗ «О персональных данных». Оператор персональных данных — {E(op)} (далее — Оператор). Используя Сайт и отправляя формы, вы подтверждаете согласие с настоящей политикой.</p>
<h2>2. Какие данные мы обрабатываем</h2><ul><li>имя, номер телефона, имя пользователя в мессенджере или адрес электронной почты, которые вы указываете в формах;</li><li>текст сообщения и параметры заказа, выбранные в калькуляторе стоимости;</li><li>технические данные: IP-адрес, тип устройства и браузера, страницы, которые вы просматривали, источник перехода (через cookie и сервисы веб-аналитики).</li></ul>
<h2>3. Цели обработки</h2><ul><li>связаться с вами по заявке и ответить на вопросы;</li><li>подготовить расчёт стоимости и заключить договорённость об оказании услуг;</li><li>улучшать работу Сайта и анализировать посещаемость.</li></ul>
<h2>4. Правовое основание</h2><p>Обработка осуществляется на основании вашего согласия, которое вы даёте, отмечая соответствующую галочку в форме и отправляя заявку.</p>
<h2>5. Передача данных</h2><p>Заявки передаются Оператору через мессенджер Telegram и (или) электронную почту. Для аналитики может использоваться сервис Яндекс Метрика. Оператор не продаёт и не передаёт ваши данные третьим лицам, за исключением случаев, предусмотренных законодательством, и сервисов, необходимых для работы Сайта.</p>
<h2>6. Срок хранения</h2><p>Данные хранятся в течение времени, необходимого для достижения целей обработки, но не дольше, чем это требуется для обработки обращения и исполнения обязательств, либо до отзыва согласия.</p>
<h2>7. Файлы cookie</h2><p>Сайт использует cookie и сервисы аналитики для работы и улучшения. Вы можете отключить cookie в настройках браузера, но некоторые функции могут работать некорректно.</p>
<h2>8. Ваши права</h2><p>Вы вправе запросить сведения о обрабатываемых данных, потребовать их уточнения, блокирования или удаления, а также отозвать согласие. Для этого напишите на <a href="mailto:{CFG["email"]}">{CFG["email"]}</a>. Оператор рассмотрит обращение в сроки, установленные законом.</p>
<h2>9. Защита данных</h2><p>Оператор принимает организационные и технические меры для защиты данных от неправомерного доступа, изменения и распространения. Формы Сайта защищены от автоматического спама.</p>
<h2>10. Изменение политики</h2><p>Оператор вправе обновлять политику. Актуальная редакция всегда размещена на этой странице.</p>
<h2>11. Контакты Оператора</h2><p>{E(op)}, Москва. Телефон: <a href="tel:{CFG["phone"]}">{CFG["phone_view"]}</a>. E-mail: <a href="mailto:{CFG["email"]}">{CFG["email"]}</a>.</p>'''
    return legal_page("ru", "/privacy/", "Политика конфиденциальности | DMITRY·WEB", "Политика обработки персональных данных сайта DMITRY·WEB: какие данные собираем, зачем, как храним и как отозвать согласие.", "Политика конфиденциальности", c, {"ru": "/privacy/", "en": "/en/privacy/"})

def privacy_en():
    op = f"self-employed {CFG['person_full']}" + (f", Tax ID {CFG['inn']}" if CFG.get("inn") else "")
    c = f'''<p class="mut">Effective {DATE_POL.replace("г.","").replace("ноября","November")}</p>
<h2>1. General</h2><p>This policy describes how personal data of visitors of {SITE.replace("https://","")} is processed and protected. The data operator is {E(op)} (the “Operator”). By using the site and submitting forms you agree with this policy.</p>
<h2>2. Data we process</h2><ul><li>name, phone number, messenger username or e-mail you enter into forms;</li><li>your message and the order parameters chosen in the price calculator;</li><li>technical data: IP address, device and browser type, pages viewed, referrer (via cookies and web analytics).</li></ul>
<h2>3. Purposes</h2><ul><li>to contact you about your request;</li><li>to prepare a price estimate and agree on services;</li><li>to improve the site and analyse traffic.</li></ul>
<h2>4. Legal basis</h2><p>Processing is based on your consent, given by ticking the checkbox and submitting a form.</p>
<h2>5. Sharing</h2><p>Requests are delivered to the Operator via Telegram and/or e-mail. Yandex Metrica may be used for analytics. The Operator does not sell your data or share it with third parties except as required by law and by services necessary to run the site.</p>
<h2>6. Retention</h2><p>Data is kept only as long as needed for the purposes above or until you withdraw your consent.</p>
<h2>7. Your rights</h2><p>You may request access to, correction, blocking or deletion of your data and withdraw consent by writing to <a href="mailto:{CFG["email"]}">{CFG["email"]}</a>.</p>
<h2>8. Contacts</h2><p>{E(op)}, Moscow. Phone: <a href="tel:{CFG["phone"]}">{CFG["phone_view"]}</a>. E-mail: <a href="mailto:{CFG["email"]}">{CFG["email"]}</a>.</p>'''
    return legal_page("en", "/en/privacy/", "Privacy policy | DMITRY·WEB", "Privacy policy of DMITRY·WEB: what data we collect, why, how long we keep it and how to withdraw consent.", "Privacy policy", c, {"ru": "/privacy/", "en": "/en/privacy/"})

def terms_ru():
    pp, pl, ps, pc = money(CFG["prepay"]), money(CFG["price_landing"]), money(CFG["price_shop"]), money(CFG["price_card"])
    rest = money(CFG["price_landing"] - CFG["prepay"])
    c = f'''<p class="mut">Редакция от {DATE_POL}. Документ носит информационный характер и описывает условия, на которых оказываются услуги.</p>
<h2>1. Услуги и цены</h2><ul><li><b>Одностраничный сайт (лендинг) под ключ</b> — {pl}. В цену входят дизайн, адаптивная вёрстка, SEO-настройка, формы заявок, кнопки звонка и мессенджеров, политика конфиденциальности, подключение аналитики.</li><li><b>Интернет-магазин до 100 артикулов</b> — от {ps} под ключ: каталог, корзина, форма заказа.</li><li><b>Нейрокарточки и инфографика для маркетплейсов</b> — {pc} за одну карточку.</li></ul>
<h2>2. Сроки</h2><p>Одностраничный сайт изготавливается за <b>3 дня</b> с момента внесения предоплаты. Срок для интернет-магазина согласуется отдельно.</p>
<h2>3. Предоплата и оплата</h2><p>Предоплата составляет {pp}, остальная сумма ({rest} для лендинга) оплачивается после готовности сайта. <b>Внесение предоплаты означает, что заказчик согласен с настоящими условиями, в том числе со сроком изготовления 3 дня.</b></p>
<h2>4. Материалы заказчика</h2><p>Заказчик передаёт материалы (описание бизнеса или тексты, фотографии, логотип при наличии, контакты, пожелания) сразу после предоплаты. Для интернет-магазина материалы передаются по папкам артикулов: в каждой папке описание товара и фотографии для галереи.</p>
<h2>5. Закрытие проекта</h2><p>Если после предоплаты материалы не переданы вовремя, проект всё равно закрывается через 3 дня, а оставшаяся сумма оплачивается в этот срок: у исполнителя очередь из заказов и фиксированные сроки.</p>
<h2>6. Домен</h2><p>Домен регистрируется на заказчика и оплачивается им отдельно (ориентировочно {money(CFG["domain_cost"])} в год). Других обязательных регулярных платежей в течение года нет.</p>
<h2>7. Встречи</h2><p>Личная встреча возможна в Москве. С остальными городами и странами работа ведётся онлайн на русском и английском языках; другие языки — по запросу.</p>
<h2>8. Результат продвижения</h2><p>Исполнитель обеспечивает техническую готовность сайта к индексации и скорость загрузки, но не гарантирует конкретные позиции в поисковой выдаче: они зависят от конкуренции, контента и алгоритмов поисковых систем.</p>
<h2>9. Контакты</h2><p>{CFG["person_full"]}, самозанятый. Телефон: <a href="tel:{CFG["phone"]}">{CFG["phone_view"]}</a>, e-mail: <a href="mailto:{CFG["email"]}">{CFG["email"]}</a>.</p>'''
    return legal_page("ru", "/terms/", "Условия работы: сроки, предоплата, оплата | DMITRY·WEB", "Условия работы DMITRY·WEB: срок изготовления лендинга 3 дня, предоплата 5 000 ₽, порядок оплаты, материалы и закрытие проекта.", "Условия работы", c, None)

def page404():
    inner = ('<section class="nf"><div class="wrap"><b>404</b><h1 style="font-size:clamp(24px,4vw,40px)">Страница не найдена</h1><p class="lead" style="margin:0 auto 26px">Возможно, ссылка устарела или адрес введён с ошибкой. Вернитесь на главную или посмотрите полезные разделы.</p>'
             '<div class="btns" style="justify-content:center"><a class="btn" href="/">На главную</a><a class="btn ghost" href="/blog/">Блог</a><a class="btn ghost" href="/cities/">Города</a></div></div></section>')
    return page("ru", "/404.html", "Страница не найдена (404) | DMITRY·WEB", "Такой страницы нет. Вернитесь на главную страницу DMITRY·WEB.", inner, noindex=True, has_pre=False)

def sitemap(urls):
    x = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for u, alts, pr in urls:
        x.append(f"<url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority>")
        if alts:
            for l, p in alts.items(): x.append(f'<xhtml:link rel="alternate" hreflang="{l}" href="{SITE}{p}"/>')
            x.append(f'<xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{alts["ru"]}"/>')
        x.append("</url>")
    x.append("</urlset>")
    return "\n".join(x)

def llms():
    pl, ps, pc = money(CFG["price_landing"]), money(CFG["price_shop"]), money(CFG["price_card"])
    t = [f"# DMITRY·WEB", "", f"> Дмитрий, Москва — создание сайтов с нуля под ключ. Лендинг за 3 дня — {pl}, интернет-магазин до 100 артикулов — от {ps}, нейрокарточки для маркетплейсов — {pc}. Русский и английский языки, работа по всему миру, личные встречи в Москве.", "",
         "## Основное", f"- [Главная]({SITE}/): услуги, цены, калькулятор, условия", f"- [English]({SITE}/en/): English version", f"- [Условия работы]({SITE}/terms/)", f"- [Политика конфиденциальности]({SITE}/privacy/)", "",
         "## Контакты", f"- Телефон: {CFG['phone_view']}", f"- E-mail: {CFG['email']}", "", "## Блог (по нишам)"]
    for n in N: t.append(f"- [{b_blog.titles(n, 'zachem')[0]}]({SITE}{b_blog.art_url(n, 'zachem')})")
    t += ["", "## Города"] + [f"- [Создание сайтов {c[2]}]({SITE}/cities/{c[0]}/)" for c in CITIES]
    return "\n".join(t) + "\n"

def static_files():
    write("/robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    write("/llms.txt", llms())
    write("/site.webmanifest", json.dumps({"name": "DMITRY·WEB — создание сайтов", "short_name": "DMITRY·WEB", "lang": "ru", "start_url": "/", "display": "standalone", "background_color": "#0a0a0a", "theme_color": "#0a0a0a",
        "icons": [{"src": "/assets/icons/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/assets/icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}]}, ensure_ascii=False, indent=1))
    write("/CNAME", CFG["domain"] + "\n")
    write("/_headers", "/assets/*\n  Cache-Control: public, max-age=31536000, immutable\n/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  Permissions-Policy: camera=(), microphone=(), geolocation=()\n")
    write("/.htaccess", f'''# Apache (shared hosting): HTTPS, www -> non-www, cache, compression, 404
RewriteEngine On
RewriteCond %{{HTTPS}} off
RewriteRule ^ https://{CFG["domain"]}%{{REQUEST_URI}} [R=301,L]
RewriteCond %{{HTTP_HOST}} ^www\\. [NC]
RewriteRule ^ https://{CFG["domain"]}%{{REQUEST_URI}} [R=301,L]
ErrorDocument 404 /404.html
DirectoryIndex index.html
<IfModule mod_deflate.c>
AddOutputFilterByType DEFLATE text/html text/css application/javascript application/json image/svg+xml
</IfModule>
<IfModule mod_expires.c>
ExpiresActive On
ExpiresByType image/avif "access plus 1 year"
ExpiresByType image/webp "access plus 1 year"
ExpiresByType image/jpeg "access plus 1 year"
ExpiresByType image/png "access plus 1 year"
ExpiresByType font/woff2 "access plus 1 year"
ExpiresByType text/css "access plus 1 year"
ExpiresByType application/javascript "access plus 1 year"
ExpiresByType text/html "access plus 10 minutes"
</IfModule>
''')
    shutil.copy(os.path.join(ROOT, "site", "assets", "icons", "favicon.ico"), os.path.join(OUT, "favicon.ico"))
