// AI는 왜 그럴듯하게 거짓말할까 — singularity-explainer 예시 (2026-11-27)
// 사실 출처: 01_research/factsheet.md (OpenAI 블로그 2025-09-05, arXiv 2509.04664)
(function () {
  const { T, TE, div, svg, el, on, fn, cam, chapter, cover, count, sticker, P, eout, cl } = X;
  const ART = window.ART || {};
  const stk = (name, x, y, size, tin, kind = 'pop', tout = null) => on(div(sticker(name, size), x, y), tin, tout, kind);
  const txt = (html, x, y, size, tin, o = {}) => on(div(html, x, y, { style: `font-size:${size}px;font-weight:${o.w || 800};color:${o.c || 'var(--ink)'};white-space:nowrap;${o.s || ''}`, anchor: o.anchor }), tin, o.out ?? null, o.kind || 'up');
  const card = (html, x, y, w, tin, o = {}) => on(div(html, x, y, { cls: 'card', w, style: `padding:${o.pad || '22px 28px'};${o.s || ''}` }), tin, o.out ?? null, o.kind || 'up');
  const chip = (html, x, y, bg, fg, tin, o = {}) => on(div(html, x, y, { cls: 'chip', style: `background:${bg};color:${fg};${o.s || ''}`, anchor: o.anchor }), tin, o.out ?? null, o.kind || 'pop');
  const stamp = (text, x, y, tin, color = 'var(--accent)', rot = -8) => on(div(text, x, y, { style: `border:5px solid ${color};color:${color};font-size:34px;font-weight:900;padding:4px 16px;border-radius:10px;transform:rotate(${rot}deg);background:rgba(255,255,255,.85)` }), tin, null, 'pop', .3);
  const xmark = (x, y, tin, s = 54) => on(div(`<svg width="${s}" height="${s}" viewBox="0 0 10 10"><path d="M2 2 L8 8 M8 2 L2 8" stroke="#E0703F" stroke-width="1.6" stroke-linecap="round"/></svg>`, x, y), tin, null, 'pop', .25);
  const check = (x, y, tin, s = 54) => on(div(`<svg width="${s}" height="${s}" viewBox="0 0 10 10"><path d="M2 5.4 L4.2 7.6 L8.2 2.6" stroke="#4FB3A5" stroke-width="1.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>`, x, y), tin, null, 'pop', .25);
  const ring = (x, y, w, h, tin, tout = null) => { const s = svg(x, y, w, h); const r = el('rect', { x: 3, y: 3, width: w - 6, height: h - 6, rx: h / 2, fill: 'none', stroke: '#E0703F', 'stroke-width': 5 }, s); on(r, tin, tout, 'draw', .45); return s; };
  const arrow = (x1, y1, x2, y2, tin, color = '#E0703F', bend = -40) => { const minx = Math.min(x1, x2) - 60, miny = Math.min(y1, y2) - 80, s = svg(minx, miny, Math.abs(x2 - x1) + 120, Math.abs(y2 - y1) + 160); const ax = x1 - minx, ay = y1 - miny, bx = x2 - minx, by = y2 - miny, mx = (ax + bx) / 2, my = (ay + by) / 2 + bend; const p = el('path', { d: `M${ax} ${ay} Q${mx} ${my} ${bx} ${by}`, fill: 'none', stroke: color, 'stroke-width': 5, 'stroke-linecap': 'round' }, s); on(p, tin, null, 'draw', .5); const ang = Math.atan2(by - my, bx - mx), h = el('path', { d: `M${bx - 18 * Math.cos(ang - .5)} ${by - 18 * Math.sin(ang - .5)} L${bx} ${by} L${bx - 18 * Math.cos(ang + .5)} ${by - 18 * Math.sin(ang + .5)}`, fill: 'none', stroke: color, 'stroke-width': 5, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, s); on(h, tin + .4, null, 'fade', .2); };

  // ───────── R0 척추 그림: 같은 시험, 두 AI 의 답 (SimpleQA)
  const BX = 300, BW = 1360, rows = [{ y: 330, name: 'gpt-5-thinking-mini', acc: 22, err: 26, abs: 52, bot: 'bot' }, { y: 590, name: 'OpenAI o4-mini', acc: 24, err: 75, abs: 1, bot: 'botx' }];
  txt('같은 시험, 두 AI의 답', 300, 120, 46, T('h1'));
  txt('SimpleQA · 정답·오답·모르겠다의 비율', 300, 184, 24, T('h1') + .3, { c: 'var(--muted)', w: 600 });
  txt('출처: OpenAI, Why language models hallucinate (2025.9.5)', 300, 800, 20, T('h1') + .3, { c: 'var(--muted)', w: 500, out: T('h5') });
  const legend = [['정답', 'var(--teal)'], ['틀린 답', 'var(--accent)'], ['모르겠다', '#C9CEC6']];
  legend.forEach(([n, c], i) => txt(`<span style="display:inline-block;width:22px;height:22px;border-radius:5px;background:${c};vertical-align:-3px;margin-right:8px"></span>${n}`, 1150 + i * 175, 128, 24, [T('h2'), T('h3'), T('h4')][i], { w: 700 }));
  const segs = {};
  rows.forEach((r, k) => {
    stk(r.bot, 150, r.y - 18, 120, T('h1') + .2 + k * .25);
    txt(r.name, BX, r.y - 52, 30, T('h1') + .3 + k * .25, { s: 'font-family:Consolas,monospace' });
    on(div('', BX, r.y, { style: `width:${BW}px;height:96px;border:3px dashed #C9D2CC;border-radius:10px` }), T('h1') + .4, null, 'fade');
    const mk = (key, from, w, bg, tin, label) => {
      const d = on(div(`<span class="mono" style="font-size:40px;font-weight:700;color:${key === 'abs' ? 'var(--ink)' : '#fff'}">0%</span>`, BX + from * BW / 100, r.y, { style: `width:${w * BW / 100}px;height:96px;background:${bg};border-radius:${from === 0 ? '10px 0 0 10px' : (from + w >= 99 ? '0 10px 10px 0' : '0')};display:flex;align-items:center;justify-content:center;overflow:visible` }), tin, null, 'wipe', .8);
      const sp = d.querySelector('span'); if (w < 6) { sp.style.position = 'absolute'; sp.style.left = (w * BW / 100 + 14) + 'px'; sp.style.whiteSpace = 'nowrap'; }
      count(sp, tin + .1, .9, 0, label, v => Math.round(v) + '%'); segs[key + k] = d; return d;
    };
    mk('acc', 0, r.acc, 'var(--teal)', T('h2') + .6 + k * .5, r.acc);
    mk('err', r.acc, r.err, 'var(--accent)', T('h3') + .5 + k * .9, r.err);
    mk('abs', r.acc + r.err, r.abs, 'repeating-linear-gradient(45deg,#E4E7E0 0 12px,#D3D8D0 12px 24px)', T('h4') + .9 + k * .5, r.abs);
  });
  chip('틀린 답 26% → 75% · 약 3배', 760, 470, '#FDF0E8', 'var(--accent)', T('h3') + 3.4, { s: 'border:3px solid var(--accent);font-size:30px' });
  ring(BX + 48 * BW / 100 - 20, 314, 52 * BW / 100 + 40, 128, T('h4') + 2.6);
  card('<span style="font-size:30px;font-weight:800">모르겠어요</span>', 1420, 210, null, T('h4') + 3.2, { pad: '10px 22px', s: 'border-radius:20px 20px 20px 4px' });
  cam(T('h2'), 700, 520, 1.3, 1.2); cam(T('h3'), 960, 500, 1.05, 1.2); cam(T('h4') + .6, 1240, 460, 1.25, 1.2);
  // 논문 카드 (R0 아래)
  cam(T('h5'), 960, 1620, 1, 1.4);
  card(`<div style="font-size:22px;color:var(--muted);font-weight:700">arXiv 2509.04664 · OpenAI 블로그 2025.9.5</div><div style="font-size:54px;font-weight:900;line-height:1.1;margin-top:10px;font-family:Georgia,serif">Why Language Models<br>Hallucinate</div><div style="font-size:24px;margin-top:14px;color:#333">Adam Tauman Kalai · Ofir Nachum · Santosh Vempala · Edwin Zhang</div>`, 300, 1230, 820, T('h5') + .3);
  stk('doc', 1180, 1240, 150, T('h5') + .6);
  chip('환각 = Hallucination', 1170, 1430, 'var(--ink)', '#fff', T('h5') + 3.2, { s: 'font-size:32px' });
  stk('trophy', 1140, 1560, 150, T('h6') + 1.2);
  txt('AI는 <span class="hl">점수를 따라</span> 배웠을 뿐', 340, 1600, 56, T('h6') + 1.6);
  arrow(1130, 1660, 870, 1700, T('h6') + 2.4, '#E0703F', 40);
  cam(T('h7'), 960, 1700, 1.05, 1.0);
  stk('botq', 280, 1760, 130, T('h7'));
  card('<span style="font-size:36px;font-weight:800">① 왜 모를 때도 답을 지어낼까?</span>', 440, 1760, null, T('h7') + .4, { pad: '14px 26px' });
  card('<span style="font-size:36px;font-weight:800">② 고칠 방법은 있을까?</span>', 440, 1860, null, T('h7') + 2.8, { pad: '14px 26px' });

  // ───────── R1 환각이란 (x 2400)
  const A = 2400;
  chapter(T('d1'), 1, '환각이란'); cam(T('d1') - .2, A + 960, 540, 1, 1.5);
  card(`<div style="display:flex;align-items:baseline;gap:22px"><span style="font-size:64px;font-weight:900">환각</span><span style="font-size:34px;color:var(--muted);font-weight:700">Hallucination</span></div>`, A + 560, 150, 800, T('d1') + .5, { s: 'text-align:center;display:flex;justify-content:center', out: T('d3') - .3 });
  txt('사실이 아닌 내용을 <span class="hl">자신 있게</span> 말하는 것', A + 960, 330, 44, T('d2') + .4, { anchor: 'c', out: T('d3') - .3 });
  cam(T('d3'), A + 560, 640, 1.25, 1.2);
  stk('bot', A + 150, 560, 130, T('d3'));
  card('<span style="font-size:32px;font-weight:700">애덤 칼라이의 생일은? <span style="color:var(--muted);font-size:24px">(일-월로만)</span></span>', A + 420, 430, null, T('d3') + .8, { pad: '14px 24px', s: 'background:#EAF5F3;border-radius:22px 22px 4px 22px' });
  ['03-07', '15-06', '01-01'].forEach((d, i) => {
    card(`<span class="mono" style="font-size:44px;font-weight:700">${d}</span>`, A + 300 + i * 230, 690, null, T('d4') + .5 + i * .7, { pad: '10px 26px', kind: 'pop', s: 'border-radius:22px 22px 22px 4px' });
    xmark(A + 420 + i * 230, 660, T('d4') + 3.0 + i * .2);
  });
  txt('논문 실험 · DeepSeek-V3 · 실제 생일은 가을', A + 300, 800, 22, T('d4') + 3.6, { c: 'var(--muted)', w: 700 });
  cam(T('d5'), A + 1420, 560, 1.15, 1.3);
  [['GPT-4o', 'Boosting, Online Algorithms, and Other Topics…', 'CMU, 2002'], ['DeepSeek', 'Algebraic Methods in Interactive Machine Learning', 'Harvard, 2005'], ['Llama', 'Efficient Algorithms for Learning and Playing Games', 'MIT, 2007']].forEach(([m, title, w], i) => {
    card(`<div style="font-size:20px;color:var(--muted);font-weight:700">${m}의 답 · 박사 논문 제목</div><div style="font-size:26px;font-weight:800;margin-top:6px;font-family:Georgia,serif;line-height:1.2">${title}</div><div class="mono" style="font-size:20px;color:var(--muted);margin-top:4px">${w}</div>`, A + 1060, 330 + i * 165, 720, T('d5') + .6 + i * .8, { pad: '14px 22px', kind: 'right' });
  });
  stamp('모두 틀림', A + 1600, 300, T('d5') + 3.6);
  // 맞춤법·괄호 (R2 왼쪽으로 이어짐)
  const B = 4800;
  cam(T('d6') + 1.0, B + 560, 520, 1.15, 1.6);
  txt('맞춤법', B + 180, 230, 34, T('d6') + 2.2, { c: 'var(--muted)' });
  card('<span class="mono" style="font-size:44px"><s style="color:var(--accent)">recieve</s> → <b>receive</b></span>', B + 180, 290, null, T('d6') + 2.4, { pad: '14px 26px' });
  check(B + 760, 300, T('d6') + 3.0);
  txt('괄호 짝', B + 180, 430, 34, T('d6') + 3.2, { c: 'var(--muted)' });
  card('<span class="mono" style="font-size:44px">print<b style="color:var(--teal)">(</b>(1+2)*3<b style="color:var(--teal)">)</b></span>', B + 180, 490, null, T('d6') + 3.4, { pad: '14px 26px' });
  check(B + 760, 500, T('d6') + 4.0);

  // ───────── R2 규칙이 없는 사실 (x 4800)
  chapter(T('r1'), 2, '규칙이 없는 사실'); cam(T('r1'), B + 960, 540, 1, 1.3);
  on(div('', B + 960, 120, { style: 'width:4px;height:720px;background:repeating-linear-gradient(#C9D2CC 0 14px,transparent 14px 26px)' }), T('r1'), null, 'fade');
  chip('규칙 있음', B + 180, 120, 'var(--teal)', '#fff', T('r1') + .5, { s: 'font-size:32px' });
  chip('규칙 없음', B + 1080, 120, 'var(--accent)', '#fff', T('r1') + 1.2, { s: 'font-size:32px' });
  { const s = svg(B + 180, 620, 680, 220); on(el('path', { d: 'M40 10 V190 H660', fill: 'none', stroke: '#1F4A5A', 'stroke-width': 3 }, s), T('r2') + 1.0, null, 'draw', .6);
    const c = el('path', { d: 'M50 30 C 200 120, 300 170, 640 180', fill: 'none', stroke: '#E0703F', 'stroke-width': 6, 'stroke-linecap': 'round' }, s); on(c, T('r2') + 1.6, null, 'draw', 1.4);
    const t1 = el('text', { x: 660, y: 214, 'text-anchor': 'end', 'font-size': 24, fill: '#7A8A8F', 'font-weight': 700 }, s); t1.textContent = '배운 글의 양 →'; on(t1, T('r2') + 1.2, null, 'fade');
    const t2 = el('text', { x: 52, y: 26, 'font-size': 24, fill: '#7A8A8F', 'font-weight': 700 }, s); t2.textContent = '실수'; on(t2, T('r2') + 1.2, null, 'fade'); }
  stk('cake', B + 1080, 200, 120, T('r3'));
  txt('생일', B + 1220, 240, 44, T('r3') + .3);
  [['dog', 0], ['cat', 1], ['dog', 2]].forEach(([a, i]) => {
    on(div(`<div style="background:#fff;padding:14px 14px 50px;border:3px solid var(--ink);border-radius:6px;box-shadow:0 8px 20px rgba(0,0,0,.12);transform:rotate(${[-4, 2, -2][i]}deg)">${sticker(a, 170)}<div style="text-align:center;font-size:28px;font-weight:800;color:var(--accent);margin-top:6px">생일 ?</div></div>`, B + 1060 + i * 260, 380), T('r4') + .5 + i * .45, null, 'pop');
  });
  stk('botq', B + 1600, 690, 120, T('r4') + 2.6);
  { const lens = div(sticker('lens', 140), B + 1060, 420); on(lens, T('r5'), T('r6') - .4, 'fade'); fn(t => { const k = cl((t - T('r5')) / 2.6); lens.style.left = (B + 1060 + eout(k) * 520) + 'px'; }); }
  chip('어디에도 안 적혀 있음', B + 1160, 760, '#fff', 'var(--accent)', T('r5') + 1.6, { s: 'border:3px solid var(--accent);font-size:28px' });
  cover(T('r6') - .1, T('r6') + 4.4, ART.cover_birthday, { title: '× 1', sub: '학습 데이터에 딱 한 번 나온 사실' });
  // R2 아래: 나온 횟수
  cam(T('r6') + 4.3, B + 960, 1620, 1, .01);
  txt('사실 10개가 학습 데이터에 나온 횟수', B + 220, 1200, 40, T('r6') + 4.6);
  const freq = [12, 5, 1, 3, 8, 1, 6, 2, 9, 4];
  freq.forEach((n, i) => {
    const one = n === 1, x = B + 220 + i * 150, h = 30 + n * 26;
    on(div(`<div class="mono" style="font-size:28px;font-weight:700;text-align:center;color:${one ? 'var(--accent)' : 'var(--ink)'}">×${n}</div>`, x, 1690 - h - 46, { w: 110 }), T('r6') + 5.0 + i * .12, null, 'up');
    on(div('', x, 1690 - h, { style: `width:110px;height:${h}px;border-radius:8px 8px 0 0;background:${one ? 'var(--accent)' : '#BFD9D4'};border:3px solid ${one ? 'var(--accent)' : 'var(--ink)'}` }), T('r6') + 5.0 + i * .12, null, 'up');
  });
  on(div('', B + 200, 1690, { style: 'width:1520px;height:4px;background:var(--ink)' }), T('r6') + 4.8, null, 'wipe');
  ring(B + 500, 1610, 170, 100, T('r7') + .4); ring(B + 950, 1610, 170, 100, T('r7') + .7);
  chip('딱 한 번 = 2개 / 10개 = 20%', B + 600, 1716, 'var(--accent)', '#fff', T('r7') + 1.6, { s: 'font-size:34px' });
  cam(T('r8'), B + 960, 1700, 1, 1.0);
  card(`<div style="font-size:30px;font-weight:800;margin-bottom:12px">기반 모델의 생일 질문 환각</div><div style="position:relative;width:820px;height:56px;border:3px solid var(--ink);border-radius:10px;background:#fff"><div id="hgFill" style="position:absolute;left:0;top:0;bottom:0;width:0;background:var(--accent);border-radius:7px 0 0 7px"></div><div style="position:absolute;left:164px;top:-14px;bottom:-14px;width:4px;background:var(--ink)"></div></div><div class="mono" style="font-size:30px;font-weight:700;color:var(--accent);margin-top:10px">적어도 20%</div>`, B + 520, 1800, 900, T('r8') + .4, { out: T('r9') + .2 });
  fn(t => { const f = document.getElementById('hgFill'); if (f) f.style.width = (eout(cl((t - T('r8') - 1.2) / 1)) * 164) + 'px'; });
  stk('botx', B + 1480, 1810, 140, T('r8') + 2.2, 'pop', T('r9') + .2);
  chip('한 번 스친 사람의 생일 = ?', B + 900, 1830, 'var(--ink)', '#fff', T('r9') + .5, { anchor: 'c', s: 'font-size:44px' });
  stk('cake', B + 1240, 1770, 120, T('r9') + 1.2);
  cam(T('r10') + 2.4, B + 2400 + 960, 540, 1, 1.6);
  card('<span style="font-size:48px;font-weight:800">배우는 단계</span>', B + 2400 + 300, 440, null, T('r10') + 3.0, { pad: '20px 34px', out: T('e1') });
  arrow(B + 2400 + 720, 480, B + 2400 + 1060, 480, T('r10') + 3.6, '#E0703F', -60);
  card('<span style="font-size:48px;font-weight:800;color:var(--accent)">점수 매기는 방식</span>', B + 2400 + 1100, 440, null, T('r10') + 4.2, { pad: '20px 34px', s: 'border-color:var(--accent)', out: T('e1') });

  // ───────── R3 객관식 시험의 함정 (x 7200)
  const C = 7200;
  chapter(T('e1'), 3, '객관식 시험의 함정');
  cover(T('e1') - .4, T('e2') + .3, ART.cover_exam, { from: [1.04, 0, 20], to: [1.2, 40, -30] });
  cam(T('e2') + .2, C + 960, 540, 1, .01);
  on(div(sticker('omr', 520), C + 140, 150), T('e2') + .3, null, 'up');
  ring(C + 300, 390, 300, 90, T('e2') + .9);
  txt('모르는 문제', C + 610, 410, 30, T('e2') + 1.0, { c: 'var(--accent)' });
  card('<div style="font-size:34px;font-weight:800">비워 두기</div><div class="mono" style="font-size:56px;font-weight:700;color:var(--muted)">0점</div>', C + 880, 200, 380, T('e2') + 1.8, { kind: 'right' });
  card('<div style="font-size:34px;font-weight:800">아무거나 찍기</div><div style="font-size:30px;font-weight:700;color:var(--teal)">맞을 수도 있음</div><div class="mono" style="font-size:44px;font-weight:700;color:var(--teal)">1 / 4</div>', C + 1320, 200, 420, T('e2') + 3.6, { kind: 'right' });
  stamp('이득', C + 1560, 470, T('e3') + .3, 'var(--teal)', 6);
  stk('pencil', C + 1380, 480, 120, T('e3') + .8);
  // 365일 달력
  cam(T('e4'), C + 960, 1620, 1, 1.4);
  { const s = svg(C + 200, 1230, 1000, 620); const sel = 252;
    for (let i = 0; i < 365; i++) { const c = el('circle', { cx: 20 + (i % 27) * 36, cy: 20 + Math.floor(i / 27) * 40, r: i === sel ? 15 : 9, fill: i === sel ? '#E0703F' : '#D3D8D0' }, s); if (i % 27 === 0 || i === sel) on(c, T('e4') + .3 + Math.floor(i / 27) * .05, null, 'fade', .2); else { on(c, T('e4') + .3 + Math.floor(i / 27) * .05, null, 'fade', .2); } } }
  chip('9월 10일', C + 580, 1540, 'var(--accent)', '#fff', T('e4') + 2.0, { s: 'font-size:34px' });
  stk('bot', C + 1300, 1700, 140, T('e4') + 2.2);
  txt('<span class="mono">1 / 365</span>', C + 1260, 1360, 80, T('e4') + 3.8, { c: 'var(--accent)' });
  card('<div style="font-size:34px;font-weight:800">모르겠다</div><div class="mono" style="font-size:56px;font-weight:700;color:var(--muted)">확실히 0점</div>', C + 1250, 1470, 440, T('e5') + .3, { kind: 'right' });
  cover(T('e6') - .1, T('e6') + 4.6, ART.cover_board, { from: [1.02, 0, 30], to: [1.14, 0, -20] });
  // 다시 척추 그림으로: 정답률 순위
  cam(T('e6') + 4.5, 960, 470, 1.05, .01);
  chip('정답률 순위', 760, 236, 'var(--ink)', '#fff', T('e7') + .3, { s: 'font-size:30px' });
  stk('trophy', 1690, 560, 130, T('e7') + 2.2);
  chip('1등', 1700, 700, 'var(--marker)', 'var(--ink)', T('e7') + 2.5);
  ring(BX + 24 * BW / 100 - 16, 574, 75 * BW / 100 + 32, 128, T('e7') + 4.0);

  // ───────── R4 채점표를 바꾸자 (x 9600)
  const D = 9600;
  chapter(T('s1'), 4, '채점표를 바꾸자'); cam(T('s1'), D + 760, 540, 1.1, 1.5);
  stk('pencil', D + 120, 130, 120, T('s1') + .6);
  txt('채점표', D + 260, 150, 52, T('s1') + .8);
  const rowsS = [['정답', '+1', 'var(--teal)'], ['모르겠다', '0', 'var(--muted)'], ['틀린 답', '0', 'var(--muted)']];
  rowsS.forEach(([a, b, c], i) => {
    card(`<div style="display:flex;justify-content:space-between;align-items:center"><span style="font-size:40px;font-weight:800">${a}</span><span class="mono sc${i}" style="font-size:48px;font-weight:700;color:${c}">${b}</span></div>`, D + 140, 270 + i * 140, 700, T('s1') + 1.2 + i * .3, { pad: '18px 30px' });
  });
  fn(t => { const a = document.querySelector('.sc2'), b = document.querySelector('.sc1'); if (!a) return; const k = t >= T('s2') + 1.0; a.textContent = k ? '− 벌점' : '0'; a.style.color = k ? 'var(--accent)' : 'var(--muted)'; const k2 = t >= T('s2') + 3.6; b.textContent = k2 ? '부분 점수' : '0'; b.style.color = k2 ? 'var(--teal)' : 'var(--muted)'; });
  ring(D + 120, 530, 740, 130, T('s2') + 1.0); ring(D + 120, 390, 740, 130, T('s2') + 3.6);
  cam(T('s3'), D + 1300, 470, 1.05, 1.3);
  card(`<div style="font-size:24px;color:var(--muted);font-weight:700">시험지 안내문</div><div style="font-size:38px;font-weight:800;margin-top:8px">확신이 <span class="hl">기준</span>을 넘을 때만 답하세요</div>`, D + 960, 130, 760, T('s3') + .5);
  const bars = [[50, 1], [75, 2], [90, 9]];
  bars.forEach(([p, pen], i) => {
    const x = D + 1030 + i * 240, h = 40 + pen * 40;
    on(div('', x, 760 - h, { style: `width:150px;height:${h}px;background:var(--accent);border-radius:10px 10px 0 0` }), T('s4') + .6 + i * 1.6, null, 'up');
    const v = on(div(`<span class="mono" style="font-size:44px;font-weight:700;color:var(--accent)">0</span><span style="font-size:26px;font-weight:800"> 점 감점</span>`, x - 10, 760 - h - 64, { w: 220 }), T('s4') + .6 + i * 1.6, null, 'up');
    count(v.querySelector('span'), T('s4') + .7 + i * 1.6, .6, 0, pen, n => '−' + Math.round(n));
    txt(`<span class="mono">기준 ${p}%</span>`, x + 4, 776, 28, T('s4') + .4 + i * 1.6, { c: 'var(--ink)' });
  });
  on(div('', D + 1000, 760, { style: 'width:740px;height:4px;background:var(--ink)' }), T('s4') + .2, null, 'wipe');
  cam(T('s5'), D + 960, 1620, 1, 1.4);
  stk('scale', D + 760, 1260, 400, T('s5') + .3, 'up');
  card('<div style="font-size:30px;font-weight:800">찍기의 기대 점수</div><div class="mono" style="font-size:52px;font-weight:700;color:var(--accent)">&lt; 0</div>', D + 320, 1440, 340, T('s5') + 1.4, { kind: 'left' });
  card('<div style="font-size:30px;font-weight:800">모르겠다</div><div class="mono" style="font-size:52px;font-weight:700;color:var(--teal)">= 0</div>', D + 1260, 1440, 300, T('s5') + 2.6, { kind: 'right' });
  stamp('가장 좋은 답', D + 1300, 1640, T('s5') + 4.6, 'var(--teal)', 5);
  cam(T('s6'), D + 960, 2700, 1, 1.4);
  card('<div style="display:flex;align-items:center;gap:20px"><span style="font-size:40px;font-weight:800">환각 시험 하나 더</span></div>', D + 300, 2560, 640, T('s6') + .5, { kind: 'left' });
  xmark(D + 960, 2560, T('s6') + 2.0, 80);
  card('<div style="font-size:40px;font-weight:800">주요 시험의 채점 바꾸기</div>', D + 300, 2740, 640, T('s6') + 3.2, { kind: 'left', s: 'border-color:var(--teal)' });
  check(D + 960, 2740, T('s6') + 4.2, 80);
  [0, 1, 2, 3].forEach(i => stk('doc', D + 1140 + i * 70, 2580 + i * 40, 160, T('s6') + 3.6 + i * .2));

  // ───────── R5 흔한 오해 셋 (x 12000)
  const E = 12000;
  chapter(T('m1'), 5, '흔한 오해 셋'); cam(T('m1'), E + 960, 540, 1, 1.5);
  const myths = [['정확도 100%면<br>환각도 사라진다?', '답할 수 없는 질문이<br>원래 있다', 'm2'], ['환각은<br>피할 수 없다?', '모를 때 답하지<br>않으면 된다', 'm3'], ['큰 모델이어야<br>고칠 수 있다?', '작은 모델이 한계를<br>알기 쉬울 수도', 'm4']];
  myths.forEach(([q, a, id], i) => {
    const x = E + 120 + i * 580;
    card(`<div style="font-size:24px;color:var(--muted);font-weight:800">오해 ${i + 1}</div><div style="font-size:42px;font-weight:900;line-height:1.25;margin-top:8px">${q}</div>`, x, 170, 520, T('m1') + .4 + i * .3, { pad: '26px 30px', s: 'min-height:230px' });
    card(`<div style="font-size:24px;color:var(--teal);font-weight:800">연구진</div><div style="font-size:38px;font-weight:800;line-height:1.3;margin-top:6px">${a}</div>`, x, 450, 520, T(id) + (i === 0 ? 3.6 : 2.2), { pad: '22px 30px', s: 'border-color:var(--teal);min-height:190px' });
    stamp('아니다', x + 330, 360, T(id) + (i === 0 ? 3.0 : 1.4));
    cam(T(id), x + 260, 450, 1.35, 1.2);
  });
  cam(T('m5'), E + 960, 1620, 1, 1.4);
  txt('마오리어 질문을 받으면', E + 960, 1220, 40, T('m5') + .3, { anchor: 'c' });
  stk('botq', E + 330, 1380, 190, T('m5') + .6);
  txt('전혀 모르는 모델', E + 300, 1600, 32, T('m5') + .8, { c: 'var(--muted)' });
  card('<span style="font-size:42px;font-weight:800">모르겠어요.</span>', E + 560, 1360, null, T('m5') + 1.4, { pad: '16px 28px', s: 'border-radius:24px 24px 24px 4px;border-color:var(--teal)' });
  check(E + 870, 1340, T('m5') + 2.2, 64);
  stk('bot', E + 1080, 1320, 250, T('m5') + 2.8);
  txt('조금 아는 모델', E + 1100, 1600, 32, T('m5') + 3.0, { c: 'var(--muted)' });
  card('<span style="font-size:38px;font-weight:800">음… 내가 얼마나 알지?</span>', E + 1360, 1300, null, T('m5') + 3.6, { pad: '16px 28px', s: 'border-radius:24px 24px 24px 4px;border-color:var(--marker)' });

  // ───────── 마무리: 척추 그림으로
  cam(T('f1'), 960, 470, 1.0, 1.6);
  card('<span style="font-size:40px;font-weight:800">AI는 왜 모를 때도 답을 지어낼까?</span>', 800, 30, null, T('f1') + 1.2, { pad: '12px 26px' });
  stk('omr', 470, 712, 110, T('f2') + 1.6, 'pop', T('f4'));
  chip('찍어도 손해 없는 시험으로 매긴 점수', 980, 770, 'var(--ink)', '#fff', T('f2') + 1.8, { anchor: 'c', s: 'font-size:34px', out: T('f4') });
  ring(BX - 14, 312, 22 * BW / 100 + 28, 132, T('f3') + .6, T('f4') + .2); ring(BX - 14, 572, 24 * BW / 100 + 28, 132, T('f3') + .9, T('f4') + .2);
  ring(BX + 48 * BW / 100 - 14, 312, 52 * BW / 100 + 28, 132, T('f3') + 3.0); ring(BX + 99 * BW / 100 - 40, 572, 120, 132, T('f3') + 3.3);
  chip('모른다고 말할 줄 아는가', 960, 770, 'var(--marker)', 'var(--ink)', T('f4') + 1.2, { anchor: 'c', s: 'font-size:44px' });
  // 마무리 질문·끝 카드: 척추 그림 바로 왼쪽 구역 (x -2400) — 멀리 가면 지난 장면이 스쳐 지나감
  const F = -2400;
  cam(T('f5'), F + 960, 540, 1, 1.6);
  stk('botq', F + 860, 140, 200, T('f5') + .5);
  card('<span style="font-size:48px;font-weight:800">믿음이 간다</span>', F + 280, 520, null, T('f5') + 3.4, { pad: '20px 38px', s: 'border-color:var(--teal)', kind: 'left' });
  card('<span style="font-size:48px;font-weight:800">답답하다</span>', F + 1260, 520, null, T('f5') + 5.0, { pad: '20px 38px', s: 'border-color:var(--accent)', kind: 'right' });
  arrow(F + 900, 380, F + 560, 500, T('f5') + 3.0, '#4FB3A5', 30); arrow(F + 1020, 380, F + 1380, 500, T('f5') + 4.6, '#E0703F', 30);
  on(div(`<div style="display:flex;gap:60px;align-items:center"><div style="text-align:center"><div style="width:110px;height:110px;border-radius:50%;background:var(--ink);display:flex;align-items:center;justify-content:center"><svg width="56" height="56" viewBox="0 0 24 24"><path d="M6 17h12l-1.5-2V10a4.5 4.5 0 0 0-9 0v5z M10 19a2 2 0 0 0 4 0" fill="#fff"/></svg></div><div style="font-size:28px;font-weight:800;margin-top:8px">구독</div></div><div style="text-align:center"><div style="width:110px;height:110px;border-radius:50%;background:var(--accent);display:flex;align-items:center;justify-content:center"><svg width="56" height="56" viewBox="0 0 24 24"><path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z" fill="#fff"/></svg></div><div style="font-size:28px;font-weight:800;margin-top:8px">좋아요</div></div></div>`, F + 790, 680), T('f6') + .8, null, 'pop');
})();
