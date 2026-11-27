// 시안: 다모다란 편 2장 「값의 4분의 3은 10년 뒤에 있다」(171.7~300초)를 singularity-explainer 문법 + 시장 채널 규칙으로 다시 그림.
// 목소리·대사·숫자는 원본 그대로(원본 음성 사용). 바뀐 것은 화면뿐 → 대조용.
(function () {
  const { T, div, svg, el, on, fn, cam, chapter, cover, count, sticker, P, eout, ease, cl } = X;
  const ART = window.ART || {};
  const stk = (name, x, y, size, tin, kind = 'pop', tout = null) => on(div(sticker(name, size), x, y), tin, tout, kind);
  const txt = (html, x, y, size, tin, o = {}) => on(div(html, x, y, { style: `font-size:${size}px;font-weight:${o.w || 800};color:${o.c || 'var(--ink)'};${o.s || ''}`, anchor: o.anchor }), tin, o.out ?? null, o.kind || 'up');
  const card = (html, x, y, w, tin, o = {}) => on(div(html, x, y, { cls: 'card', w, style: `padding:${o.pad || '20px 26px'};${o.s || ''}`, anchor: o.anchor }), tin, o.out ?? null, o.kind || 'up');
  const chip = (html, x, y, bg, fg, tin, o = {}) => on(div(html, x, y, { cls: 'chip', style: `background:${bg};color:${fg};${o.s || ''}`, anchor: o.anchor }), tin, o.out ?? null, o.kind || 'pop');
  const block = (x, y, w, h, bg, tin, o = {}) => on(div(o.html || '', x, y, { style: `width:${w}px;height:${h}px;background:${bg};border-radius:${o.r ?? 6}px;${o.s || ''}` }), tin, o.out ?? null, o.kind || 'up', o.dur || .5);
  const arrow = (x1, y1, x2, y2, tin, color = '#E3A93B', bend = -40, w = 5) => { const minx = Math.min(x1, x2) - 60, miny = Math.min(y1, y2) - 90, s = svg(minx, miny, Math.abs(x2 - x1) + 120, Math.abs(y2 - y1) + 180); const ax = x1 - minx, ay = y1 - miny, bx = x2 - minx, by = y2 - miny, mx = (ax + bx) / 2, my = (ay + by) / 2 + bend; on(el('path', { d: `M${ax} ${ay} Q${mx} ${my} ${bx} ${by}`, fill: 'none', stroke: color, 'stroke-width': w, 'stroke-linecap': 'round' }, s), tin, null, 'draw', .55); const ang = Math.atan2(by - my, bx - mx); on(el('path', { d: `M${bx - 20 * Math.cos(ang - .5)} ${by - 20 * Math.sin(ang - .5)} L${bx} ${by} L${bx - 20 * Math.cos(ang + .5)} ${by - 20 * Math.sin(ang + .5)}`, fill: 'none', stroke: color, 'stroke-width': w, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, s), tin + .45, null, 'fade', .2); };
  const bracketH = (x1, x2, y, label, tin, color = '#E3A93B') => { const s = svg(x1, y - 20, x2 - x1, 40); on(el('path', { d: `M2 30 V10 H${x2 - x1 - 2} V30`, fill: 'none', stroke: color, 'stroke-width': 4 }, s), tin, null, 'draw', .45); return txt(label, (x1 + x2) / 2, y - 46, 30, tin + .3, { anchor: 'c', c: color }); };
  const RED = 'var(--accent)', BLUE = 'var(--teal)', GOLD = 'var(--marker)';

  // 출처 줄(시장 채널 규칙: 숫자가 보이는 화면엔 항상 출처·해석 표시)
  const src = document.createElement('div'); src.id = 'srcl'; document.body.appendChild(src);
  const SRC = [[8.0, '<b>원문</b>다모다란 블로그 평가표(2026.11.18 수정판) · 1조 7,279억 중 10년 뒤 가치 1조 3,381억 · 비율은 이 채널 계산'],
    [T('s14'), '<b>해석 · 이 채널 계산</b>다모다란 평가표(11.18)를 다시 짠 틀 · 2~5년차 성장률만 바꿈 · 이익률·투자·자본비용·빚 그대로'],
    [T('s28'), '<b>개념도</b>막대 크기는 원리 설명용 · 최악의 길 수치는 다모다란 11월 2일 자료'],
    [T('s35'), '<b>해석 · 이 채널 계산</b>같은 틀에 11.25 종가 82.79달러를 넣고 10년차 매출을 거꾸로 구함(2~5년차 연 43.6%)']];
  fn(t => { let cur = ''; for (const [a, h] of SRC) if (t >= a) cur = h; src.innerHTML = cur; src.style.opacity = t < 8 ? 0 : 1; });

  // ── 장 표지 (누아르 그림)
  cover(0, 7.95, ART.cover_ch2, { title: '값의 4분의 3은 10년 뒤에 있다', from: [1.03, 0, 20], to: [1.13, -20, -10] });
  chapter(8.0, 2, '값의 4분의 3은 10년 뒤에 있다');

  // ── R0 가치 = 앞으로 벌 현금을 지금 돈으로 바꿔 더한 것 (개념도)
  cam(7.9, 960, 520, 1, .01);
  txt('회사 가치 = 앞으로 벌 현금을 <span class="hl">지금 돈으로 바꿔</span> 더한 것', 960, 190, 50, T('s2') + .3, { anchor: 'c', out: T('s7') });
  stk('coins', 120, 560, 150, T('s3') + .2);
  const AX = 760, bw = 60, pv = i => 20 + 8 * i, fv = i => Math.min(330, pv(i) * Math.pow(1.11, i + 1));
  on(div('', 230, AX, { style: 'width:1300px;height:4px;background:#59626B' }), T('s3'), null, 'wipe', .6);
  for (let i = 0; i < 10; i++) {
    const x = 240 + i * 95;
    on(div('', x, AX - fv(i), { style: `width:${bw}px;height:${fv(i)}px;border:3px dashed #7C858D;border-radius:6px 6px 0 0` }), T('s3') + .4 + i * .08, null, 'up');
    const b = block(x, AX - fv(i), bw, fv(i), RED, T('s3') + 1.2 + i * .08, { r: 0, kind: 'fade', s: 'border-radius:6px 6px 0 0;transform-origin:bottom' });
    fn(t => { const k = eout(cl((t - T('s3') - 2.4) / 1.4)); const h = fv(i) + (pv(i) - fv(i)) * k; b.style.top = (AX - h) + 'px'; b.style.height = h + 'px'; });
    txt(`${2027 + i}`, x + bw / 2, AX + 34, 20, T('s3') + .4, { anchor: 'c', c: '#9AA3AA', w: 600 });
  }
  txt('↓ 지금 돈으로', 760, 300, 34, T('s3') + 2.6, { c: GOLD });
  const TX = 1230, TW = 260, TV = 433;
  on(div('', TX, AX - 560, { style: `width:${TW}px;height:560px;border:3px dashed #7C858D;border-radius:8px 8px 0 0` }), T('s4') - .6, null, 'up');
  const term = block(TX, AX - TV, TW, TV, BLUE, T('s4') - .2, { kind: 'fade', s: 'border-radius:8px 8px 0 0', html: '<div style="padding:16px;font-size:30px;font-weight:800;color:#10202E">10년 뒤<br>가치</div>' });
  txt('2037~', TX + TW / 2, AX + 34, 20, T('s4'), { anchor: 'c', c: '#9AA3AA', w: 600 });
  bracketH(240, TX + TW, AX - 600, '', T('s4') + .3, GOLD);
  const total = card('<div style="font-size:24px;color:#AEB6BC;font-weight:700">그의 표에서 합</div><div class="mono" style="font-size:52px;font-weight:700;color:var(--marker)"><span id="tot">0</span>억 달러</div>', 70, 300, null, T('s4') + .6, { kind: 'pop', out: T('s7') });
  count(document.getElementById('tot') || total.querySelector('#tot'), T('s4') + .3, 1.6, 0, 17279, v => { v = Math.round(v); return v >= 10000 ? `${Math.floor(v / 10000)}조 ${(v % 10000).toLocaleString()}` : v.toLocaleString(); });
  txt('개념도 · 해마다 막대 크기는 설명용', 230, AX + 70, 20, T('s3') + 1, { c: '#7C858D', w: 600 });
  // 막대 → 한 줄 몫 막대(척추)
  cam(T('s7'), 960, 820, .9, 1.3);
  const SY = 1000, SX = 260, SW = 1400;
  on(div('', SX, SY, { style: `width:${SW}px;height:110px;border:3px solid #59626B;border-radius:10px` }), T('s6') + .4, null, 'fade');
  block(SX, SY, SW * .23, 110, RED, T('s8') - .2, { kind: 'wipe', dur: .7, r: 10, html: `<div style="height:110px;display:flex;align-items:center;justify-content:center;font-size:44px;font-weight:800;color:#fff" class="mono"><span id="p23">0%</span></div>` });
  const blueS = block(SX + SW * .23, SY, SW * .77, 110, BLUE, T('s9') - .1, { kind: 'wipe', dur: .9, r: 10, html: `<div style="height:110px;display:flex;align-items:center;justify-content:center;font-size:44px;font-weight:800;color:#10202E" class="mono"><span id="p77">0%</span></div>` });
  fn(t => { const a = document.getElementById('p23'), b = document.getElementById('p77'); if (a) a.textContent = Math.round(23 * ease(cl((t - T('s8')) / .8))) + '%'; if (b) b.textContent = Math.round(77 * ease(cl((t - T('s9')) / .9))) + '%'; });
  txt('앞 10년 현금', SX, SY + 128, 30, T('s8'), { c: RED });
  txt('10년이 지난 뒤의 가치', SX + SW * .23 + 20, SY + 128, 30, T('s9'), { c: BLUE });
  // 10년 뒤 가치는 어디서 오나
  stk('building', 1700, 330, 120, T('s10') + .3);
  card('<div style="font-size:26px;color:#AEB6BC;font-weight:700">10년 뒤 가치의 재료</div><div style="font-size:36px;font-weight:800;margin-top:4px">2036년 <span style="color:var(--marker)">매출</span> × 이익률</div>', 1520, 470, null, T('s10') + .8, { kind: 'right' });
  arrow(1640, 600, 1420, 990, T('s10') + 1.6, GOLD, 30);
  // 흔들림: 2036년 매출이 흔들리면 값의 4분의 3이 같이
  fn(t => { const k = (t > T('s11') + 1.2 && t < T('s13')) ? Math.sin(t * 34) * 7 * Math.min(1, (t - T('s11') - 1.2) / .4) : 0; term.style.transform = `translateX(${k}px)`; blueS.style.transform = `translateX(${k}px)`; });
  bracketH(SX + SW * .23, SX + SW, SY - 26, '값의 4분의 3', T('s12'), GOLD);
  cam(T('s13'), 960, 980, .95, 1.0);
  card('<div style="font-size:48px;font-weight:900;font-family:\'Noto Serif KR\',serif">“매출이 안 오면 다 무너진다”</div><div style="font-size:26px;color:#AEB6BC;margin-top:8px;font-weight:700;text-align:right">— 애스워스 다모다란 (뉴욕대 교수)</div>', 960, 1270, null, T('s13') + .3, { anchor: 'c', kind: 'pop', pad: '24px 40px', s: 'border-color:var(--marker)' });

  // ── R1 같은 틀에서 매출만 바꾸면 (이 채널 계산)
  const A = 2400;
  cam(T('s14'), A + 960, 540, 1, 1.4);
  chip('여기서부터 이 채널의 계산', A + 140, 190, GOLD, '#1C2024', T('s14') + .3, { s: 'font-size:30px' });
  stk('calc', A + 150, 270, 140, T('s15') + .2);
  card('<div style="font-size:24px;color:#AEB6BC;font-weight:700">다시 짜서 돌린 값</div><div class="mono" style="font-size:46px;font-weight:700">75.87<span style="font-size:26px"> 달러</span></div>', A + 330, 270, 320, T('s16'), { kind: 'right' });
  card('<div style="font-size:24px;color:#AEB6BC;font-weight:700">그의 값</div><div class="mono" style="font-size:46px;font-weight:700">76.43<span style="font-size:26px"> 달러</span></div>', A + 720, 270, 300, T('s17') - .4, { kind: 'right' });
  chip('1% 안', A + 1050, 315, 'var(--teal)', '#10202E', T('s17') + .8, { s: 'font-size:30px' });
  stk('lock', A + 1240, 250, 110, T('s18') + .2);
  card('<div style="font-size:28px;font-weight:800">이익률 · 투자 · 자본비용 · 빚</div><div style="font-size:26px;color:#AEB6BC;font-weight:700">그대로</div>', A + 1370, 260, null, T('s18') + .4, { kind: 'right' });
  chip('매출 길만 바꿈', A + 1440, 400, RED, '#fff', T('s19'), { s: 'font-size:30px' });
  cam(T('s20') - .3, A + 960, 580, 1, 1.2);
  txt('2036년 매출', A + 330, 480, 26, T('s20') - .2, { c: '#AEB6BC' });
  txt('주당 값', A + 1300, 480, 26, T('s20') - .2, { c: '#AEB6BC' });
  const ROWS = [['1조', 1, 76, '76달러', 's20'], ['8,000억', .8, 56, '56달러', 's21'], ['6,000억', .6, 37, '37달러', 's22'], ['5,000억 (절반)', .5, 27.5, '27.5달러', 's24'], ['4,000억', .4, 18, '18달러', 's25']];
  ROWS.forEach(([lab, r, p, ptxt, id], k) => {
    const y = 520 + k * 76, hl = k === 3, t0 = T(id);
    txt(lab, A + 300, y + 8, 30, t0, { c: hl ? GOLD : 'var(--ink)', s: 'text-align:right;width:240px', w: 800 });
    block(A + 560, y, 600 * r, 56, hl ? GOLD : '#8A949C', t0 + .1, { kind: 'wipe', dur: .5 });
    arrow(A + 560 + 600 * r + 20, y + 28, A + 1290, y + 28, t0 + .5, hl ? GOLD : '#59626B', 0, 3);
    block(A + 1300, y, 480 * p / 76, 56, hl ? GOLD : BLUE, t0 + .9, { kind: 'wipe', dur: .5 });
    txt(`<span class="mono">${ptxt}</span>`, A + 1310 + 480 * p / 76, y + 6, 32, t0 + 1.2, { c: hl ? GOLD : 'var(--ink)' });
  });
  card('<div class="mono" style="font-size:52px;font-weight:700">매출 <span style="color:var(--marker)">½</span> → 값 <span style="color:var(--accent)">약 ⅓</span></div>', A + 960, 420, null, T('s26') + .6, { anchor: 'c', kind: 'pop', pad: '14px 36px', s: 'border-color:var(--marker);z-index:3' });
  txt('매출보다 값이 훨씬 크게 움직인다', A + 960, 920, 34, T('s27') + .2, { anchor: 'c', c: GOLD });

  // ── R1 아래: 왜 — 고정비와 빚은 그대로 (개념도)
  cam(T('s28'), A + 960, 1620, 1, 1.3);
  stk('botq', A + 640, 1215, 110, T('s28') + .2);
  txt('왜 이렇게 크게 움직일까?', A + 780, 1245, 44, T('s28') + .4);
  const BASE = 1880, U = 4.4, FIX = 38;
  const col = (cx, rev, label, t0, neg) => {
    const H = rev * U, fh = FIX * U;
    txt(label, cx + 90, neg ? BASE - fh - 60 : BASE + 30, 28, t0, { anchor: 'c', c: neg ? 'var(--accent)' : '#AEB6BC' });
    block(cx, BASE - Math.min(H, fh), 180, Math.min(H, fh), 'repeating-linear-gradient(45deg,#4A525A 0 12px,#3E454C 12px 24px)', t0 + .2, { r: 4, html: '<div style="padding:8px;font-size:22px;font-weight:800;color:#D8DDE1">고정비·빚</div>' });
    if (!neg) block(cx, BASE - H, 180, H - fh, BLUE, t0 + .7, { r: 4, html: '<div style="padding:8px;font-size:22px;font-weight:800;color:#10202E">남는 몫</div>' });
    on(div('', cx - 10, BASE - H - 6, { style: 'width:200px;height:0;border-top:4px dashed var(--marker)' }), t0 + .1, null, 'wipe');
  };
  on(div('', A + 300, BASE, { style: 'width:1320px;height:4px;background:#C9D0D5' }), T('s29'), null, 'wipe');
  col(A + 380, 100, '매출 1조 길', T('s29') + .3);
  col(A + 760, 50, '매출 절반', T('s29') + 1.6);
  stk('lock', A + 970, BASE - FIX * U - 140, 70, T('s30') + .2);
  on(div('', A + 380, BASE - FIX * U, { style: 'width:560px;height:0;border-top:3px dashed #D8DDE1' }), T('s30') + .4, null, 'wipe');
  txt('매출이 줄어도 그대로 뺀다', A + 1050, BASE - FIX * U - 120, 30, T('s30') + .8, { c: '#D8DDE1' });
  // 최악의 길
  col(A + 1240, 20, '최악: 매출 2,000억', T('s31') + .3, true);
  block(A + 1240, BASE + 4, 180, 150, RED, T('s33') - .6, { kind: 'up', r: 4, html: '<div style="padding:8px;font-size:22px;font-weight:800;color:#fff">지분 가치</div>' });
  card('<div class="mono" style="font-size:44px;font-weight:700;color:var(--accent)">−3,730억 달러</div><div style="font-size:22px;color:#AEB6BC;font-weight:700">다모다란 11월 2일 자료</div>', A + 1450, BASE - 30, null, T('s33'), { kind: 'right' });
  on(div('버틸 수 없다', A + 1480, BASE - 190, { style: 'border:5px solid var(--accent);color:var(--accent);font-size:36px;font-weight:900;padding:4px 16px;border-radius:10px;transform:rotate(-7deg);background:rgba(28,32,36,.85)' }), T('s34') + .2, null, 'pop', .3);
  cam(T('s31'), A + 1000, 1660, .95, 1.2);

  // ── R2 거꾸로 풀면 — 82.79달러가 깔고 있는 매출
  const B = 4800;
  cam(T('s35'), B + 960, 520, 1, 1.4);
  txt('거꾸로 풀기', B + 140, 150, 44, T('s35') + .3, { out: T('s39') });
  stk('tag', B + 1500, 200, 150, T('s36') + .2);
  card('<div style="font-size:24px;color:#AEB6BC;font-weight:700">11월 25일 종가</div><div class="mono" style="font-size:54px;font-weight:700">82.79<span style="font-size:28px"> 달러</span></div>', B + 1140, 230, 340, T('s36') + .6, { kind: 'right' });
  arrow(B + 1120, 300, B + 760, 300, T('s37') + .2, GOLD, -70);
  stk('target', B + 140, 200, 150, T('s38'));
  card('<div style="font-size:24px;color:#AEB6BC;font-weight:700">필요한 2036년 매출</div><div class="mono" style="font-size:54px;font-weight:700;color:var(--marker)">약 <span id="rev">0</span></div>', B + 300, 230, 440, T('s38') + .2, { kind: 'pop' });
  fn(t => { const e = document.getElementById('rev'); if (!e) return; const v = Math.round(10770 * ease(cl((t - T('s38') - .3) / 1.2))); e.textContent = v >= 10000 ? `1조 ${(v - 10000).toLocaleString()}억` : `${v.toLocaleString()}억`; });
  const SC = 0.085; // 1억 = 0.085px → 1조 = 850px
  const hb = (y, val, label, color, t0, txtv) => { txt(label, B + 140, y - 40, 28, t0, { c: '#AEB6BC', w: 700 }); block(B + 140, y, val * SC, 60, color, t0 + .1, { kind: 'wipe', dur: .7 }); txt(`<span class="mono">${txtv}</span>`, B + 160 + val * SC, y + 10, 34, t0 + .6, { c: color === GOLD ? GOLD : 'var(--ink)' }); };
  cam(T('s39'), B + 960, 640, 1, 1.2);
  hb(560, 10044, '다모다란이 낙관의 모자를 쓰고 그린 길', '#8A949C', T('s39') + .2, '1조 44억');
  hb(700, 10770, '주가가 깔고 있는 길', GOLD, T('s40') - .4, '1조 770억');
  chip('+7%', B + 1240, 640, GOLD, '#1C2024', T('s40') + 1.4, { s: 'font-size:32px' });
  hb(840, 7250, '아마존 · 월마트 연 매출 (7,000억~7,500억)', BLUE, T('s41') + .2, '7,000억~7,500억');
  chip('약 1.5배', B + 1240, 830, BLUE, '#10202E', T('s42') + .2, { s: 'font-size:32px' });
  cam(T('s43'), B + 960, 560, .95, 1.2);
  card('<div style="font-size:46px;font-weight:900">주가는 이미 <span class="hl">가장 밝은 길</span>을 조금 넘게 깔고 있다</div>', B + 960, 452, null, T('s44') - .2, { anchor: 'c', kind: 'pop', pad: '18px 40px', s: 'border-color:var(--marker);z-index:4' });
})();
