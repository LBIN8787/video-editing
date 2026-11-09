// 대시보드 창을 16:9 화면 가운데에 크게 (1920x1080) — node shot169.js in.html out.png
const { chromium } = require('playwright');
(async () => {
  const [f, out] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto('file://' + require('path').resolve(f), { waitUntil: 'networkidle' });
  await p.evaluate(async () => { await document.fonts.ready; document.body.style.transformOrigin = '0 0';
    document.body.style.transform = 'scale(1.15) translate(114.8px,-20.9px)'; document.body.style.width = '1440px'; });
  await p.waitForTimeout(900);
  await p.screenshot({ path: out });
  await b.close();
})();
