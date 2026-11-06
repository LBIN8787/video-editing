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
    // X(트위터) 게시물: Python 이 받은 공식 임베드 HTML(oEmbed)을 그려서 게시물 카드만 캡처
    //   node capture.js --embed <oembed.html> <out.png>
    // 페이지 전체 (쇼츠 화면 스크롤용): node capture.js --full <url> <out.png>
    if (url === '--full') {
      const [, target, outFile] = process.argv.slice(2);
      await page.setViewportSize({ width: 1280, height: 900 });
      const r = await page.goto(target, { waitUntil: 'domcontentloaded', timeout: 30000 });
      await page.waitForTimeout(3500);
      if (!r || r.status() >= 400) { console.log('BLOCKED ' + (r ? r.status() : 0)); await browser.close(); process.exit(2); }
      const h = Math.min(await page.evaluate(() => document.body.scrollHeight), 7000);
      await page.screenshot({ path: outFile, fullPage: true });  // 너무 길면 Python 쪽에서 7000px 로 자름
      console.log('OK(full) ' + h + 'px');
      await browser.close();
      process.exit(0);
    }
    if (url === '--embed') {
      const [, html, outFile] = process.argv.slice(2);
      const body = require('fs').readFileSync(html, 'utf8');
      await page.setContent(`<html><body style="margin:0;padding:40px;background:#fff;display:flex;justify-content:center">
        ${body}<script async src="https://platform.twitter.com/widgets.js"></script></body></html>`);
      await page.waitForSelector('iframe[id^="twitter-widget"]', { timeout: 20000 }).catch(() => {});
      await page.waitForTimeout(3500);
      const el = (await page.$('iframe[id^="twitter-widget"]')) || (await page.$('blockquote'));
      await el.screenshot({ path: outFile });
      console.log('OK(x embed)');
      await browser.close();
      process.exit(0);
    }
    const resp = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(3000);
    // 쿠키·구독 동의 팝업 정리: '동의/Accept' 버튼을 누르고, 화면을 덮는 고정 레이어는 숨긴다 (페이지 내용은 그대로)
    await page.evaluate(() => {
      const re = /^(accept|accept all|agree|i agree|allow all|got it|ok|동의|모두 동의|확인|수락)/i;
      for (const b of document.querySelectorAll('button, a[role=button], input[type=button]')) {
        const t = (b.innerText || b.value || '').trim();
        if (t && t.length < 30 && re.test(t)) { try { b.click(); } catch (e) {} }
      }
    }).catch(() => {});
    await page.waitForTimeout(800);
    await page.evaluate(() => {
      for (const el of document.querySelectorAll('body *')) {
        const cs = getComputedStyle(el);
        if ((cs.position === 'fixed' || cs.position === 'sticky') && parseInt(cs.zIndex || '0') >= 100) {
          const r = el.getBoundingClientRect();
          if (r.width * r.height > window.innerWidth * window.innerHeight * 0.15) el.style.display = 'none';
        }
      }
      document.documentElement.style.overflow = 'auto'; document.body.style.overflow = 'auto';
    }).catch(() => {});
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
