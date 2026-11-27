// singularity-explainer 엔진: 한 캔버스(world) 위 요소 등장·카메라·장 표지 그림·챕터 알약·자막.
// 영상마다 scenes.js 가 이 API 로 장면을 적는다. render(t) 는 같은 t 에 늘 같은 화면을 그린다(프레임 단위 렌더).
(function () {
  const W = 1920, H = 1080, NS = 'http://www.w3.org/2000/svg';
  const TL = window.TL; const L = {}, LE = {};
  TL.lines.forEach(l => { L[l.id] = l.start; LE[l.id] = l.end; });
  const world = document.getElementById('world'), covers = document.getElementById('covers');
  const anims = [], fns = [], cams = [[0, 960, 540, 1, 0]], chapters = [], coverList = [];
  const cl = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));
  const ease = x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2, eout = x => 1 - Math.pow(1 - x, 3);
  const back = x => { const c = 1.6; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
  const P = (t, s, d = .4) => cl((t - s) / d);

  const api = {
    W, H, L, LE, cl, ease, eout, P,
    T: id => { if (!(id in L)) throw new Error('no line ' + id); return L[id]; },
    TE: id => LE[id],
    // 월드 좌표에 HTML 요소. anchor 'c' 면 (x,y) 가 가운데
    div(html, x, y, o = {}) {
      const d = document.createElement('div'); d.className = 'it ' + (o.cls || ''); d.innerHTML = html;
      d.style.left = x + 'px'; d.style.top = y + 'px'; if (o.w) d.style.width = o.w + 'px';
      if (o.anchor === 'c') d.dataset.c = 1; if (o.style) d.style.cssText += o.style;
      (o.parent || world).appendChild(d); d.style.opacity = 0; return d;
    },
    svg(x, y, w, h, o = {}) {
      const s = document.createElementNS(NS, 'svg'); s.setAttribute('width', w); s.setAttribute('height', h); s.setAttribute('viewBox', `0 0 ${w} ${h}`);
      s.classList.add('it'); s.style.left = x + 'px'; s.style.top = y + 'px'; s.style.overflow = 'visible'; (o.parent || world).appendChild(s); return s;
    },
    el(tag, a, parent) { const e = document.createElementNS(NS, tag); for (const k in a) e.setAttribute(k, a[k]); parent.appendChild(e); return e; },
    // 등장: kind up·pop·fade·left·right·draw(svg 선)·wipe(왼→오) · tout 이 있으면 그때 사라짐
    on(node, tin, tout = null, kind = 'up', dur = .4) { anims.push({ node, tin, tout, kind, dur }); if (kind === 'draw') { const n = node.getTotalLength ? node.getTotalLength() : 2000; node.style.strokeDasharray = n; node.dataset.len = n; } return node; },
    fn(f) { fns.push(f); },
    cam(t, cx, cy, s = 1, dur = 1.2) { cams.push([t, cx, cy, s, dur]); },
    chapter(t, n, name) { chapters.push([t, n, name]); },
    cover(tin, tout, src, o = {}) {
      const d = document.createElement('div'); d.className = 'cover'; d.innerHTML = `<img src="${src}">` + (o.title ? `<div class="ctitle">${o.title}</div>` : '') + (o.sub ? `<div class="csub">${o.sub}</div>` : '');
      covers.appendChild(d); coverList.push({ d, tin, tout, from: o.from || [1.06, 0, 0], to: o.to || [1.16, -30, -10] });
    },
    count(node, tin, dur, a, b, fmt = v => v.toFixed(0)) { fns.push(t => { node.textContent = fmt(a + (b - a) * ease(P(t, tin, dur))); }); },
    sticker: (name, size = 120, extra = '') => `<svg width="${size}" height="${size}" viewBox="0 0 100 100" ${extra}>${STK[name] || ''}</svg>`,
  };

  // 2톤 스티커 삽화 (남색 외곽 + 크림·주황·청록 면). 채널 고유 마스코트는 'bot'
  const N = '#1F4A5A', O = '#E0703F', G = '#4FB3A5', C = '#FFF7E6', M = '#E6C36A', S = `stroke="${N}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"`;
  const STK = {
    bot: `<ellipse cx="50" cy="94" rx="26" ry="4" fill="#000" opacity=".08"/><line x1="50" y1="12" x2="50" y2="22" ${S}/><circle cx="50" cy="10" r="5" fill="${O}" ${S}/><rect x="22" y="22" width="56" height="44" rx="22" fill="${C}" ${S}/><rect x="29" y="34" width="42" height="18" rx="9" fill="${N}"/><circle cx="41" cy="43" r="4" fill="${G}"/><circle cx="59" cy="43" r="4" fill="${G}"/><path d="M34 70 h32 v14 a6 6 0 0 1 -6 6 h-20 a6 6 0 0 1 -6 -6z" fill="${G}" ${S}/>`,
    botq: `<ellipse cx="50" cy="94" rx="26" ry="4" fill="#000" opacity=".08"/><line x1="50" y1="12" x2="50" y2="22" ${S}/><circle cx="50" cy="10" r="5" fill="${M}" ${S}/><rect x="22" y="22" width="56" height="44" rx="22" fill="${C}" ${S}/><rect x="29" y="34" width="42" height="18" rx="9" fill="${N}"/><circle cx="41" cy="43" r="4" fill="${M}"/><path d="M55 40 q4 -4 8 0" stroke="${M}" stroke-width="3" fill="none"/><path d="M34 70 h32 v14 a6 6 0 0 1 -6 6 h-20 a6 6 0 0 1 -6 -6z" fill="${M}" ${S}/>`,
    botx: `<ellipse cx="50" cy="94" rx="26" ry="4" fill="#000" opacity=".08"/><line x1="50" y1="12" x2="50" y2="22" ${S}/><circle cx="50" cy="10" r="5" fill="${O}" ${S}/><rect x="22" y="22" width="56" height="44" rx="22" fill="${C}" ${S}/><rect x="29" y="34" width="42" height="18" rx="9" fill="${N}"/><path d="M37 39 l8 8 M45 39 l-8 8 M55 39 l8 8 M63 39 l-8 8" stroke="${O}" stroke-width="3"/><path d="M34 70 h32 v14 a6 6 0 0 1 -6 6 h-20 a6 6 0 0 1 -6 -6z" fill="${O}" ${S}/>`,
    cake: `<path d="M20 52 h60 v32 h-60z" fill="${C}" ${S}/><path d="M20 62 q10 8 20 0 q10 8 20 0 q10 8 20 0" fill="none" stroke="${O}" stroke-width="5"/><rect x="47" y="30" width="6" height="22" fill="${G}" ${S}/><path d="M50 16 q6 7 0 12 q-6 -5 0 -12z" fill="${M}" ${S}/><rect x="14" y="84" width="72" height="6" rx="3" fill="${N}"/>`,
    cal: `<rect x="16" y="20" width="68" height="64" rx="8" fill="#fff" ${S}/><path d="M16 38 h68" ${S}/><rect x="16" y="20" width="68" height="18" rx="8" fill="${O}" ${S}/><line x1="32" y1="12" x2="32" y2="26" ${S}/><line x1="68" y1="12" x2="68" y2="26" ${S}/><g fill="${N}" opacity=".5"><circle cx="30" cy="50" r="3"/><circle cx="43" cy="50" r="3"/><circle cx="56" cy="50" r="3"/><circle cx="69" cy="50" r="3"/><circle cx="30" cy="62" r="3"/><circle cx="43" cy="62" r="3"/><circle cx="69" cy="62" r="3"/><circle cx="30" cy="74" r="3"/><circle cx="43" cy="74" r="3"/><circle cx="56" cy="74" r="3"/></g><circle cx="56" cy="62" r="7" fill="${G}" ${S}/>`,
    pencil: `<path d="M24 76 l44 -44 l10 10 l-44 44 l-14 4z" fill="${M}" ${S}/><path d="M68 32 l6 -6 a5 5 0 0 1 7 0 l3 3 a5 5 0 0 1 0 7 l-6 6z" fill="${O}" ${S}/><path d="M24 76 l-4 14 l14 -4" fill="${C}" ${S}/>`,
    omr: `<rect x="20" y="10" width="60" height="80" rx="4" fill="#fff" ${S}/><g fill="none" stroke="${N}" stroke-width="2.5">${[0, 1, 2, 3, 4].map(r => [0, 1, 2, 3].map(c => `<circle cx="${34 + c * 11}" cy="${24 + r * 14}" r="4"/>`).join('')).join('')}</g><circle cx="45" cy="24" r="4" fill="${N}"/><circle cx="56" cy="38" r="4" fill="${N}"/><circle cx="34" cy="52" r="4" fill="${O}"/>`,
    trophy: `<path d="M30 16 h40 v18 a20 20 0 0 1 -40 0z" fill="${M}" ${S}/><path d="M30 22 h-10 a10 10 0 0 0 12 16 M70 22 h10 a10 10 0 0 1 -12 16" fill="none" ${S}/><rect x="44" y="54" width="12" height="14" fill="${M}" ${S}/><rect x="32" y="68" width="36" height="14" rx="3" fill="${N}"/>`,
    book: `<path d="M50 28 q-16 -10 -34 -6 v54 q18 -4 34 6z" fill="${C}" ${S}/><path d="M50 28 q16 -10 34 -6 v54 q-18 -4 -34 6z" fill="#fff" ${S}/><path d="M24 36 h18 M24 46 h18 M58 36 h18 M58 46 h14" stroke="${N}" stroke-width="2.5" opacity=".5"/>`,
    dog: `<path d="M26 34 l-8 -14 l16 6z M74 34 l8 -14 l-16 6z" fill="${O}" ${S}/><circle cx="50" cy="50" r="28" fill="${C}" ${S}/><circle cx="40" cy="46" r="3.5" fill="${N}"/><circle cx="60" cy="46" r="3.5" fill="${N}"/><ellipse cx="50" cy="58" rx="7" ry="5" fill="${N}"/><path d="M44 66 q6 5 12 0" fill="none" ${S}/>`,
    cat: `<path d="M26 36 l2 -22 l16 14z M74 36 l-2 -22 l-16 14z" fill="${G}" ${S}/><circle cx="50" cy="52" r="28" fill="${C}" ${S}/><path d="M38 48 q3 -4 6 0 M56 48 q3 -4 6 0" fill="none" ${S}/><path d="M47 58 h6 l-3 4z" fill="${O}" ${S}/><path d="M30 60 h-12 M30 66 h-12 M70 60 h12 M70 66 h12" ${S}/>`,
    scale: `<line x1="50" y1="20" x2="50" y2="82" ${S}/><path d="M36 86 h28" ${S}/><line x1="18" y1="30" x2="82" y2="30" ${S}/><path d="M18 30 l-10 24 h20z" fill="${C}" ${S}/><path d="M82 30 l-10 24 h20z" fill="${C}" ${S}/><circle cx="50" cy="20" r="5" fill="${O}" ${S}/>`,
    doc: `<path d="M24 10 h38 l16 16 v64 h-54z" fill="#fff" ${S}/><path d="M62 10 v16 h16" fill="${C}" ${S}/><path d="M32 40 h36 M32 50 h36 M32 60 h28 M32 70 h32" stroke="${N}" stroke-width="3" opacity=".45"/>`,
    lens: `<circle cx="42" cy="42" r="24" fill="#fff" ${S}/><path d="M34 42 q8 -10 16 0 q-8 10 -16 0z" fill="${G}" ${S}/><circle cx="42" cy="42" r="3" fill="${N}"/><path d="M60 60 l22 22" stroke="${N}" stroke-width="9" stroke-linecap="round"/>`,
    globe: `<circle cx="50" cy="50" r="32" fill="${G}" ${S}/><path d="M30 38 q10 -6 16 2 q4 8 -6 12 q-8 4 -4 14 M60 24 q-4 10 8 14 q12 2 10 14 M58 70 q8 -6 14 -2" fill="none" stroke="${C}" stroke-width="5" stroke-linecap="round"/>`,
    chat: `<path d="M14 22 h72 a8 8 0 0 1 8 8 v30 a8 8 0 0 1 -8 8 h-40 l-18 14 v-14 h-14 a8 8 0 0 1 -8 -8 v-30 a8 8 0 0 1 8 -8z" fill="#fff" ${S}/><circle cx="34" cy="45" r="4" fill="${N}"/><circle cx="50" cy="45" r="4" fill="${N}"/><circle cx="66" cy="45" r="4" fill="${N}"/>`,
  };
  window.STK = STK;

  let sorted = false;
  function camAt(t) {
    if (!sorted) { cams.sort((x, y) => x[0] - y[0]); sorted = true; }
    let i = 0; while (i + 1 < cams.length && cams[i + 1][0] <= t) i++;
    const c = cams[i], p = cams[Math.max(0, i - 1)], k = i === 0 ? 1 : ease(cl((t - c[0]) / c[4]));
    let cx = p[1] + (c[1] - p[1]) * k, cy = p[2] + (c[2] - p[2]) * k, s = p[3] + (c[3] - p[3]) * k;
    // 숨쉬기: 자리를 잡은 뒤에도 아주 천천히 다가감(완전히 멈춘 화면을 줄임)
    const next = cams[i + 1] ? cams[i + 1][0] : t + 10, held = Math.max(0, t - (c[0] + c[4]));
    const span = Math.max(1, next - (c[0] + c[4]));
    s *= 1 + 0.035 * ease(cl(held / span)); cx += 14 * ease(cl(held / span));
    return [cx, cy, s];
  }
  function applyAnim(a, t) {
    const n = a.node, pin = a.kind === 'pop' ? back(cl((t - a.tin) / a.dur)) : eout(P(t, a.tin, a.dur));
    const pout = a.tout == null ? 0 : eout(P(t, a.tout, .3)), v = t < a.tin ? 0 : Math.min(1, pin) * (1 - pout);
    if (a.kind === 'draw') { n.style.opacity = t < a.tin || pout >= 1 ? 0 : 1 - pout; n.style.strokeDashoffset = n.dataset.len * (1 - eout(P(t, a.tin, a.dur))); return; }
    if (a.kind === 'wipe') { n.style.opacity = t < a.tin ? 0 : 1 - pout; n.style.clipPath = `inset(0 ${100 - 100 * eout(P(t, a.tin, a.dur))}% 0 0)`; return; }
    n.style.opacity = cl(v);
    const c = n.dataset && n.dataset.c ? 'translate(-50%,-50%) ' : '';
    const tr = { up: `translateY(${(1 - Math.min(1, pin)) * 16}px)`, pop: `scale(${t < a.tin ? .6 : .6 + .4 * pin})`, fade: '', left: `translateX(${(1 - Math.min(1, pin)) * -60}px)`, right: `translateX(${(1 - Math.min(1, pin)) * 60}px)` }[a.kind] || '';
    if (n instanceof SVGElement && !(n instanceof SVGSVGElement)) { if (a.kind === 'pop') { const b = n.getBBox(), cx = b.x + b.width / 2, cy = b.y + b.height / 2, s = t < a.tin ? .6 : .6 + .4 * pin; n.setAttribute('transform', `translate(${cx} ${cy}) scale(${s}) translate(${-cx} ${-cy})`); } n.setAttribute('opacity', cl(v)); return; }
    n.style.transform = c + tr;
  }
  window.render = function (t) {
    const [cx, cy, s] = camAt(t);
    world.style.transform = `translate(${W / 2}px,${H / 2}px) scale(${s}) translate(${-cx}px,${-cy}px)`;
    for (const a of anims) applyAnim(a, t);
    for (const f of fns) f(t);
    for (const c of coverList) {
      const vis = t >= c.tin - .02 && t < c.tout + .25, k = cl((t - c.tin) / (c.tout - c.tin));
      c.d.style.display = vis ? 'block' : 'none'; if (!vis) continue;
      c.d.style.opacity = t < c.tout ? Math.min(1, (t - c.tin) / .12 + .001) : 1 - (t - c.tout) / .25;
      const z = c.from[0] + (c.to[0] - c.from[0]) * k, x = c.from[1] + (c.to[1] - c.from[1]) * k, y = c.from[2] + (c.to[2] - c.from[2]) * k;
      c.d.querySelector('img').style.transform = `translate(${x}px,${y}px) scale(${z})`;
      const tt = c.d.querySelector('.ctitle'); if (tt) { const p = eout(P(t, c.tin + .4, .6)); tt.style.opacity = p; tt.style.transform = `translateY(${(1 - p) * 20}px)`; }
      const ts = c.d.querySelector('.csub'); if (ts) { const p = eout(P(t, c.tin + .9, .6)); ts.style.opacity = p; }
    }
    const pill = document.getElementById('chap'); let cur = null; for (const c of chapters) if (t >= c[0]) cur = c;
    if (cur) { const p = eout(P(t, cur[0], .4)) * (1 - eout(P(t, cur[0] + 3.6, .4))); pill.style.opacity = p; pill.innerHTML = `<b>${cur[1]}</b>${cur[2]}`; pill.style.transform = `translateX(${(1 - p) * 20}px)`; } else pill.style.opacity = 0;
    const line = TL.lines.find(l => t >= l.start - .05 && t < l.end + .18);
    document.getElementById('sub').innerHTML = line ? wrap(line.t) : '';
  };
  function wrap(s) {
    if (s.length <= 26) return s; let m = Math.floor(s.length / 2), best = -1;
    for (let d = 0; d < m && best < 0; d++) for (const i of [m - d, m + d]) { if (s[i] === ',' || s[i] === '.' || s[i] === '?') { best = i; break; } }
    if (best < 0 || Math.abs(best - m) > s.length * .3) { best = -1; for (let d = 0; d < m && best < 0; d++) for (const i of [m - d, m + d]) if (s[i] === ' ') { best = i; break; } }
    return best < 0 ? s : s.slice(0, best + 1).trim() + '<br>' + s.slice(best + 1).trim();
  }
  window.X = api;
})();
