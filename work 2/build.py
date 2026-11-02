# -*- coding: utf-8 -*-
"""Сборка сайта dmitry-web.ru: python3 build.py -> папка dist/"""
import os, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from b_common import *
import b_home, b_blog, b_city, b_misc
from data_cities import CITIES
from data_niches import N

if os.path.exists(OUT): shutil.rmtree(OUT)
os.makedirs(OUT)
shutil.copytree(os.path.join(ROOT, "site", "assets"), os.path.join(OUT, "assets"))

urls = []
write("/", b_home.home("ru")); urls.append(("/", {"ru": "/", "en": "/en/"}, "1.0"))
write("/en/", b_home.home("en")); urls.append(("/en/", {"ru": "/", "en": "/en/"}, "0.8"))
write("/privacy/", b_misc.privacy_ru()); urls.append(("/privacy/", {"ru": "/privacy/", "en": "/en/privacy/"}, "0.3"))
write("/en/privacy/", b_misc.privacy_en()); urls.append(("/en/privacy/", {"ru": "/privacy/", "en": "/en/privacy/"}, "0.2"))
write("/terms/", b_misc.terms_ru()); urls.append(("/terms/", None, "0.5"))
write("/404.html", b_misc.page404())
write("/blog/", b_blog.blog_hub()); urls.append(("/blog/", None, "0.8"))
write("/cities/", b_city.cities_hub()); urls.append(("/cities/", None, "0.8"))
for c in CITIES:
    u, t, d, h = b_city.city_page(c); write(u, h); urls.append((u, None, "0.7"))
cnt = 0
for n in N:
    for k in b_blog.KINDS:
        u, t, d, h = b_blog.render_article(n, k); write(u, h); urls.append((u, None, "0.6")); cnt += 1
write("/sitemap.xml", b_misc.sitemap(urls))
b_misc.static_files()
print("pages:", len(urls) + 1, "articles:", cnt, "cities:", len(CITIES))
