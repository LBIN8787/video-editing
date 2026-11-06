// 기사·공시 페이지의 헤드라인 부분만 캡처한다 (식스시그마식 '헤드라인 캡처' 화면용).
// 사용: node capture.js <url> <out.png>
// 필요: npm i playwright && npx playwright install chromium (클라우드 세션에는 설치돼 있음)
// 접근을 막는 사이트(403, 보안 확인 화면)는 우회하지 않고 실패로 남긴다.
const { chromium } = require('playwright');

(async () => {
  const [url, out] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1400, height: 1100 }, locale: 'ko-KR' });
  let code = 0;
  try {
    const resp = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(3000);
    const status = resp ? resp.status() : 0;
    const title = await page.title();
    if (status >= 400 || /보안 확인|Just a moment|Access Denied|403/i.test(title)) {
      console.log(`BLOCKED ${status} ${title}`);
      code = 2;
    } else {
      const box = await page.evaluate(() => {
        const h = document.querySelector('h1') || document.querySelector('h2');
        if (!h) return null;
        h.scrollIntoView({ block: 'center' });
        const r = h.getBoundingClientRect();
        return { x: r.left, y: r.top, w: r.width, h: r.height, text: h.innerText };
      });
      if (!box) {
        await page.screenshot({ path: out });
        console.log('OK(full) ' + title);
      } else {
        const W = 1400, x0 = Math.max(0, box.x - 60), w = Math.min(W - x0, Math.max(box.w + 120, 1000));
        const y0 = Math.max(0, box.y - 90), h = Math.min(1100 - y0, box.h + 380);
        await page.screenshot({ path: out, clip: { x: x0, y: y0, width: w, height: h } });
        console.log('OK ' + box.text.replace(/\s+/g, ' ').slice(0, 80));
      }
    }
  } catch (e) {
    console.log('FAIL ' + e.message.slice(0, 120));
    code = 1;
  }
  await browser.close();
  process.exit(code);
})();
