import {chromium} from 'playwright';
import assert from 'node:assert/strict';
const browser=await chromium.launch();
try {
 const page=await browser.newPage({viewport:{width:390,height:844}});
 const errors=[];page.on('pageerror',e=>errors.push(String(e)));
 await page.goto((process.argv[2]||'http://127.0.0.1:8000')+'/index.html#doorway');
 const root=page.locator('.doorway');
 assert.equal(await root.locator('.dw-nodes .dn').count(),9);
 assert.equal(await root.locator('.dw-downloads a[download]').count(),2);
 await page.waitForFunction(()=>document.querySelector('.dw-phase').textContent==='phase 1');
 const state=await root.locator('.dw-state').textContent();
 assert.equal(state,'state (5, 7)');
 assert.equal(await root.locator('.dn.lit').getAttribute('data-d'),'5');
 await root.locator('.dw-pause').click();
 const before=await root.locator('.dw-phase').textContent();
 await page.waitForTimeout(1300);
 assert.equal(await root.locator('.dw-phase').textContent(),before);
 await root.locator('.dw-pause').click();
 for(let cycle=0;cycle<2;cycle++){
 await page.waitForFunction(()=>document.querySelector('.dw-phase').textContent==='phase 24 = 0',null,{timeout:35000,polling:10});
 assert.equal(await root.locator('.dn.lit').getAttribute('data-d'),'2');
 await page.waitForFunction(()=>document.querySelector('.doorway').dataset.stage==='Genesis',null,{timeout:3000});
 }
 assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
 await root.locator('.dw-enter').click();
 assert.equal(new URL(page.url()).hash,'#begin');
 assert.deepEqual(errors,[]);
 const still=await browser.newPage({reducedMotion:'reduce'});
 await still.goto((process.argv[2]||'http://127.0.0.1:8000')+'/index.html');
 assert.equal(await still.locator('.doorway').getAttribute('data-stage'),'Still');
 assert.equal(await still.locator('.dw-trail line').count(),24);
 console.log('Doorway two-cycle, pause, arrival, entry and reduced-motion checks passed');
} finally {await browser.close();}
