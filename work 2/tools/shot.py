import asyncio, sys
from playwright.async_api import async_playwright
async def main(url, out, w, h, full, wait=2500, js=None):
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1)
        pg = await ctx.new_page()
        errs = []
        pg.on('console', lambda m: errs.append(m.text) if m.type in ('error', 'warning') else None)
        pg.on('pageerror', lambda e: errs.append('PAGEERR ' + str(e)))
        pg.on('requestfailed', lambda r: errs.append('REQFAIL ' + r.url))
        await pg.goto(url, wait_until='load')
        await pg.wait_for_timeout(wait)
        if full:
            await pg.evaluate("async()=>{for(let y=0;y<document.body.scrollHeight;y+=500){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,120))}window.scrollTo(0,0)}")
            await pg.wait_for_timeout(1200)
        if js: await pg.evaluate(js); await pg.wait_for_timeout(600)
        await pg.screenshot(path=out, full_page=full)
        print('errors:', errs[:10])
        await b.close()
a = sys.argv
asyncio.run(main(a[1], a[2], int(a[3]), int(a[4]), a[5] == '1', int(a[6]) if len(a) > 6 else 2500, a[7] if len(a) > 7 else None))
