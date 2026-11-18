// 확인용 정지 화면: node shots.js scene.html outdir t1 t2 ...
const { chromium } = require('playwright'); const { pathToFileURL } = require('url');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto(pathToFileURL(process.argv[2]).href); await p.waitForTimeout(1500); await p.evaluate(() => document.fonts.ready);
  for (const t of process.argv.slice(4)) { await p.evaluate(t => window.seek(t), Number(t)); await p.screenshot({ path: `${process.argv[3]}/s_${t}.jpg`, type: 'jpeg', quality: 80 }); }
  await b.close(); })();
