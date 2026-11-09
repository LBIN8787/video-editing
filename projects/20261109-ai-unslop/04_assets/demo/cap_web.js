// 공개 웹 페이지 화면 캡처 (1920x1080, 기기 배율 1) — node cap_web.js <url> <out.png> [scrollY]
const { chromium } = require('playwright');
(async () => {
  const [url, out, sy] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
  if (sy) await p.evaluate((y) => window.scrollTo(0, +y), sy);
  await p.waitForTimeout(1200);
  await p.screenshot({ path: out });
  await b.close();
})();
