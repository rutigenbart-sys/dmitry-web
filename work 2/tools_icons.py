import asyncio, base64
from playwright.async_api import async_playwright
IC='/home/claude/work/site/assets/icons/'
IM='/home/claude/work/site/assets/img/'
fav=open(IC+'favicon.svg').read()
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':512,'height':512})
        for s in (16,32,48,180,192,512):
            await pg.set_viewport_size({'width':s,'height':s})
            await pg.set_content(f'<body style="margin:0;background:transparent">{fav.replace("<svg ","<svg width=%d height=%d "%(s,s),1)}</body>')
            await pg.screenshot(path=f'{IC}icon-{s}.png',omit_background=True)
        # OG
        bg=base64.b64encode(open('/home/claude/work/src_img/Gemini_Generated_Image_hiyammhiyammhiya.jpeg','rb').read()).decode()
        html=f'''<body style="margin:0;width:1200px;height:630px;position:relative;overflow:hidden;background:#0a0a0a;font-family:Inter,Arial,sans-serif;color:#fff">
<img src="data:image/jpeg;base64,{bg}" style="position:absolute;inset:0;width:1200px;height:630px;object-fit:cover">
<div style="position:absolute;inset:0;background:linear-gradient(90deg,#0a0a0a 0%,#0a0a0acc 45%,transparent 100%)"></div>
<div style="position:absolute;left:72px;top:64px;display:flex;align-items:center;gap:16px"><svg width="56" height="56" viewBox="0 0 48 48"><path d="M9 7h15a17 17 0 0 1 0 34H9z" fill="none" stroke="#fff" stroke-width="4"/><rect x="20" y="20" width="8" height="8" fill="#fff"/></svg><span style="font-size:26px;letter-spacing:.18em;font-weight:600">DMITRY·WEB</span></div>
<div style="position:absolute;left:72px;top:200px;width:700px;font-size:68px;line-height:1.05;font-weight:700;letter-spacing:-.02em">Сайт с нуля<br>под ключ за 3 дня</div>
<div style="position:absolute;left:72px;top:430px;font-size:30px;color:#cfcfcf">Лендинг — 15 000 ₽ · Магазин — от 55 000 ₽</div>
<div style="position:absolute;left:72px;bottom:56px;font-size:24px;color:#9a9a9a;letter-spacing:.06em">dmitry-web.ru · +7 926 854-23-33</div></body>'''
        pg2=await b.new_page(viewport={'width':1200,'height':630})
        await pg2.set_content(html); await pg2.wait_for_timeout(400)
        await pg2.screenshot(path=IM+'og-image.jpg',type='jpeg',quality=88)
        await b.close()
asyncio.run(main())
from PIL import Image
im=Image.open(IC+'icon-48.png'); 
Image.open(IC+'icon-32.png').save(IC+'favicon.ico',sizes=[(16,16),(32,32),(48,48)])
print('ok')
