// 실제로 실행한 터미널 기록(term_log.txt: '$ '로 시작하면 명령)을 타자 치듯 재생해 녹화 — node record_term.js term_log.txt out_dir
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const [log, outDir] = process.argv.slice(2);
  const lines = fs.readFileSync(log, 'utf8').trimEnd().split('\n');
  fs.mkdirSync(outDir, { recursive: true });
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 1920, height: 1080 }, recordVideo: { dir: outDir, size: { width: 1920, height: 1080 } } });
  const p = await ctx.newPage();
  await p.setContent(`<!doctype html><html><head><link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>body{margin:0;background:#2A2826;height:1080px;display:grid;place-items:center;font-family:'IBM Plex Mono',monospace}
  .w{width:1500px;height:820px;background:#151413;border-radius:14px;box-shadow:0 30px 70px rgba(0,0,0,.28);overflow:hidden}
  .bar{height:52px;background:#232220;display:flex;align-items:center;padding:0 22px;gap:10px}
  .bar i{width:14px;height:14px;border-radius:7px;background:#4a4744;display:block}
  .bar span{margin-left:16px;color:#8E8981;font-size:20px}
  pre{margin:0;padding:34px 40px;color:#D9D4CB;font:400 28px/1.55 'IBM Plex Mono',monospace;white-space:pre-wrap;word-break:break-all}
  .c{color:#EDEAE4}.p{color:#E8622C}.o{color:#9FB79A}.cur{display:inline-block;width:14px;height:30px;background:#E8622C;vertical-align:-5px;animation:b 1s steps(1) infinite}
  @keyframes b{50%{opacity:0}}</style></head><body><div class="w"><div class="bar"><i></i><i></i><i></i><span>터미널 · 실제 실행 기록</span></div><pre id="t"></pre></div></body></html>`);
  await p.evaluate(() => document.fonts.ready);
  const t0 = Date.now();
  await p.waitForTimeout(700);
  const start = Date.now() - t0;
  for (const ln of lines) {
    if (ln.startsWith('$ ')) {
      await p.evaluate(() => { const t = document.getElementById('t'); t.insertAdjacentHTML('beforeend', '<span class="p">$ </span><span class="c"></span><span class="cur"></span>'); });
      for (const ch of ln.slice(2)) {
        await p.evaluate((ch) => { const cs = document.querySelectorAll('#t .c'); cs[cs.length - 1].textContent += ch; }, ch);
        await p.waitForTimeout(28);
      }
      await p.waitForTimeout(350);
      await p.evaluate(() => { document.querySelectorAll('#t .cur').forEach((c) => c.remove()); document.getElementById('t').insertAdjacentHTML('beforeend', '\n'); });
    } else {
      await p.evaluate((ln) => { const s = document.createElement('span'); s.className = 'o'; s.textContent = ln + '\n'; document.getElementById('t').appendChild(s); }, ln);
      await p.waitForTimeout(140);
    }
  }
  await p.evaluate(() => document.getElementById('t').insertAdjacentHTML('beforeend', '<span class="p">$ </span><span class="cur"></span>'));
  await p.waitForTimeout(2500);
  const vid = await p.video().path();
  await ctx.close(); await b.close();
  console.log(JSON.stringify({ video: vid, start }));
})();
