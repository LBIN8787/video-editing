// 이 폴더의 banner*.html(2560x1440)·profile*.html(800x800) 을 PNG 로. 실행: node render.js
const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const b = await chromium.launch();
  for (const f of fs.readdirSync(__dirname).filter(n => /^(banner|profile).*\.html$/.test(n))) {
    const big = f.startsWith('banner'); const [w, h] = big ? [2560, 1440] : [800, 800];
    const p = await b.newPage({ viewport: { width: w, height: h } });
    await p.goto('file://' + __dirname + '/' + f); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
    await p.screenshot({ path: __dirname + '/' + f.replace('.html', '.png') }); await p.close();
  }
  await b.close();
})();
