// 단계 CSS(story.html 의 .s1~.s4)를 차례로 켜며 화면이 스스로 고쳐지는 과정을 녹화한다 (우리 코드, Playwright 녹화).
// node record_morph.js story.html out_dir  → out_dir/*.webm + timing.json
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
(async () => {
  const [story, outDir] = process.argv.slice(2);
  fs.mkdirSync(outDir, { recursive: true });
  const b = await chromium.launch();
  const t0 = Date.now();
  const ctx = await b.newContext({ viewport: { width: 1920, height: 1080 }, recordVideo: { dir: outDir, size: { width: 1920, height: 1080 } } });
  const p = await ctx.newPage();
  await p.goto('file://' + path.resolve(story), { waitUntil: 'networkidle' });
  await p.evaluate(async () => { await document.fonts.ready; });
  const steps = await p.evaluate(() => {
    const S = 1.15, TX = 114.8, TY = -20.9;
    const css = document.createElement('style');
    css.textContent = `
      body { transform: scale(${S}) translate(${TX}px, ${TY}px); transform-origin: 0 0; }
      .win, .win *, .wash { transition-property: all !important; transition-duration: 900ms !important;
        transition-timing-function: cubic-bezier(.65,0,.35,1) !important; transition-delay: var(--wave, 0ms) !important; }
      .swap { display: inline-grid; } .swap > * { grid-area: 1 / 1; }
      .swap > .to { opacity: 0; filter: blur(8px); transform: translateY(40%); display: inline-block; }
      .swap > .from { display: inline-block; }
      [data-in] { opacity: 0; }
      #ov { position: fixed; inset: 0; pointer-events: none; z-index: 99; font-family: "IBM Plex Sans", sans-serif; }
      .tag { position: absolute; border: 3px solid #ff4d6a; border-radius: 6px; opacity: 0; transition: opacity .3s; }
      .tag b { position: absolute; left: -3px; top: -34px; background: #ff4d6a; color: #fff; font: 500 18px/30px "IBM Plex Mono", monospace; padding: 0 10px; border-radius: 4px; white-space: nowrap; }
      #step { position: absolute; left: 48px; bottom: 44px; background: rgba(12,12,14,.78); color: #fff; font-size: 30px; font-weight: 500; padding: 10px 22px; border-radius: 10px; opacity: 0; transition: opacity .3s; }
      #credit { position: absolute; right: 36px; bottom: 30px; background: rgba(12,12,14,.62); color: rgba(255,255,255,.86); font-size: 18px; padding: 7px 14px; border-radius: 16px; }
    `;
    document.head.appendChild(css);
    const N = (document.querySelector('meta[name=unslop-steps]')?.content || '').split(',').length;
    let rules = '';
    for (let k = 1; k <= N; k++) rules += `
      html.s${k} .swap[data-at="${k}"] > .from { opacity: 0; filter: blur(10px); transform: translateY(-14px); }
      html.s${k} .swap[data-at="${k}"] > .to { opacity: 1; filter: none; transform: none; }
      html.s${k} [data-in="${k}"] { opacity: 1; }
      html.s${k} [data-out="${k}"] { opacity: 0; max-width: 0 !important; max-height: 0 !important; margin: 0 !important; padding: 0 !important; border-width: 0 !important; overflow: hidden; }`;
    const r2 = document.createElement('style'); r2.textContent = rules; document.head.appendChild(r2);
    // 물결: 왼쪽 위부터 차례로
    for (const el of document.querySelectorAll('.win, .win *')) {
      const r = el.getBoundingClientRect();
      el.style.setProperty('--wave', Math.round((r.left + r.top) * 0.18) + 'ms');
    }
    const ov = document.createElement('div'); ov.id = 'ov';
    ov.innerHTML = '<div id="step"></div><div id="credit">unslop by @heydamir · CC BY 4.0</div>';
    document.documentElement.appendChild(ov);
    for (const el of document.querySelectorAll('[data-slop]')) {
      const r = el.getBoundingClientRect();
      const t = document.createElement('div'); t.className = 'tag';
      Object.assign(t.style, { left: r.left - 6 + 'px', top: r.top - 6 + 'px', width: r.width + 12 + 'px', height: r.height + 12 + 'px' });
      t.innerHTML = '<b>' + el.dataset.slop + '</b>';
      ov.appendChild(t);
    }
    return N;
  });
  const LABELS = ['', '1단계 · 간격', '2단계 · 색과 아이콘', '3단계 · 글꼴과 문구', '4단계 · 마감'];
  const wait = (ms) => p.waitForTimeout(ms);
  const marks = {};
  await wait(900);
  marks.start = Date.now() - t0;
  await wait(1000);
  await p.evaluate(() => document.querySelectorAll('.tag').forEach((t) => (t.style.opacity = 1)));
  marks.slop = Date.now() - t0;
  await wait(2600);
  await p.evaluate(() => document.querySelectorAll('.tag').forEach((t) => (t.style.opacity = 0)));
  await wait(400);
  for (let k = 1; k <= steps; k++) {
    await p.evaluate(([k, label]) => { const s = document.getElementById('step'); s.textContent = label; s.style.opacity = 1; document.documentElement.classList.add('s' + k); }, [k, LABELS[k] || 'Step ' + k]);
    marks['s' + k] = Date.now() - t0;
    await wait(2800);
  }
  await p.evaluate(() => (document.getElementById('step').style.opacity = 0));
  await wait(2200);
  marks.end = Date.now() - t0;
  const vid = await p.video().path();
  await ctx.close(); await b.close();
  fs.writeFileSync(path.join(outDir, 'timing.json'), JSON.stringify({ video: vid, marks }, null, 1));
  console.log(JSON.stringify({ video: vid, marks }));
})();
