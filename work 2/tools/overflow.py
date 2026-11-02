import asyncio,sys
from playwright.async_api import async_playwright
paths=["","en/","blog/","blog/avtomoyka-sayt-zachem/","blog/vizitka-sayt-stoimost/","cities/","cities/moskva/","privacy/","terms/","en/privacy/","404.html"]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for w in (360,390,768):
            pg=await (await b.new_context(viewport={'width':w,'height':800})).new_page()
            for u in paths:
                r=await pg.goto('http://localhost:8765/'+u,wait_until='load')
                await pg.wait_for_timeout(300)
                o=await pg.evaluate("""()=>{const W=document.documentElement.clientWidth;const bad=[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.right>W+1&&getComputedStyle(e).position!=='fixed'}).slice(0,3).map(e=>e.tagName+'.'+e.className);return [document.documentElement.scrollWidth-W,bad]}""")
                if r.status!=200 and u!="404.html" or o[0]>0: print(w,u,r.status,o)
        print('done'); await b.close()
asyncio.run(main())
