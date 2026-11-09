const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  for (const [f, o] of process.argv.slice(2).reduce((a, x, i, arr) => (i % 2 ? a : [...a, [arr[i], arr[i + 1]]]), [])) {
    const p = await b.newPage({ viewport: { width: 1440, height: 980 } });
    await p.goto('file://' + require('path').resolve(f), { waitUntil: 'networkidle' });
    await p.waitForTimeout(800);
    await p.screenshot({ path: o });
    await p.close();
  }
  await b.close();
})();
