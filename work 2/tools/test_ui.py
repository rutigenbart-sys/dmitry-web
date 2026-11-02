import asyncio, json
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={'width':1440,'height':900})
        pg = await ctx.new_page()
        errs=[]; posts=[]
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: errs.append(m.text) if m.type=='error' else None)
        async def handle(route):
            posts.append(route.request.post_data); await route.fulfill(status=200, content_type='application/json', body='{"ok":true}')
        await pg.route('**/send.php', handle)
        await pg.goto('http://localhost:8765/', wait_until='load'); await pg.wait_for_timeout(2500)
        # scroll to load lazy
        await pg.evaluate("async()=>{for(let y=0;y<document.body.scrollHeight;y+=400){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,80))}}")
        await pg.wait_for_timeout(1500)
        bad = await pg.evaluate("[...document.images].filter(i=>i.complete&&i.naturalWidth===0&&i.currentSrc).map(i=>i.currentSrc)")
        print('broken images:', bad)
        print('images without alt attr:', await pg.evaluate("[...document.images].filter(i=>!i.hasAttribute('alt')).length"))
        # quiz: shop path
        await pg.evaluate("document.querySelector('#quiz').scrollIntoView()")
        await pg.click('label.opt:has(input[value=shop])'); 
        print('shop sum:', await pg.inner_text('.qres .sum'))
        await pg.click('.qstep.on [data-next]'); await pg.wait_for_timeout(400)
        await pg.click('.qstep.on [data-next]'); await pg.wait_for_timeout(400)
        await pg.check('input[name=addcards]'); 
        print('shop+cards sum:', await pg.inner_text('.qres .sum'))
        await pg.click('.qstep.on [data-next]'); await pg.wait_for_timeout(500)
        await pg.fill('#q-name','Тест'); await pg.fill('#q-contact','+79000000000')
        await pg.click('#quizform input[name=agree]')
        await pg.wait_for_timeout(2600)
        await pg.click('#quizform button[type=submit]'); await pg.wait_for_timeout(800)
        print('quiz msg:', await pg.inner_text('#quizform .msg'))
        print('posts:', [json.loads(x)['text'][:200] for x in posts if x])
        await pg.screenshot(path='/tmp/quiz_done.png')
        # honeypot test
        await pg.evaluate("document.querySelector('#contacts').scrollIntoView()")
        await pg.fill('#c-name','Бот'); await pg.fill('#c-contact','x'); await pg.check('form[data-lead] input[name=agree]')
        await pg.evaluate("document.querySelector('form[data-lead] input[name=website]').value='spam'")
        await pg.wait_for_timeout(1700)
        n=len(posts); await pg.click('form[data-lead] button[type=submit]'); await pg.wait_for_timeout(500)
        print('honeypot blocked (no new post):', len(posts)==n)
        # card qty
        await pg.reload(); await pg.wait_for_timeout(1500)
        await pg.evaluate("document.querySelector('#quiz').scrollIntoView()")
        await pg.click('label.opt:has(input[value=card])'); await pg.click('.qstep.on [data-next]')
        await pg.evaluate("const r=document.querySelector('input[name=qty]');r.value=40;r.dispatchEvent(new Event('input',{bubbles:true}))")
        print('cards 40:', await pg.inner_text('.qres .sum'))
        print('errors:', errs)
        await b.close()
asyncio.run(main())
