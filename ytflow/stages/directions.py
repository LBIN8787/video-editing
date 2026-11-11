"""새 연출 문법 3종 — 기존 hybrid 장면은 그대로 두고 장면 type 만 '추가'한다 (docs/16-new-styles.md).

1) archive  아카이브 다큐 (켄 번스식): 자료 사진·영상을 화면 가득 천천히 훑기 + 타자기 날짜·장소 + 검은 카드 인용
     type "kb"        : clip{src}, move(in|out|left|right|up), stamp "1918 · 프랑스", 박자 lower
     type "card_type" : lines[], by, 박자마다 한 줄씩
2) journey  지도 여정 (Johnny Harris식): 세계 지도 위 카메라 이동 + 경로선 그리기 + 핀
     type "journey"   : places{key:[경도,위도]}, 박자 goto/zoom, route[a,b], pin{at,label}, 장면 시작 때 이미 그려진 drawn[[a,b]]·pins[]
3) kinetic  키네틱 타이포: 목소리가 말하는 순간 그 단어가 화면에 크게 박힘 (단어 시각 = faster-whisper)
     type "kinetic"   : 박자 hit[] (강조 단어), 숫자는 자동으로 크게
4) layers   스타일 조합: 어떤 장면 위에든 다른 스타일 요소를 겹침 (sc["layers"], apply_layers 참고)
장면별 그래픽 팩: sc["skin"] (hybrid.build_scene)
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

from .. import config
from . import hybrid, hyper
from .hybrid import FT, HH, W, _e, fit


def _fam(role: str) -> str:
    """역할 글꼴(그래픽 팩이 정함) → HTML 글꼴 이름."""
    from . import paper
    return {paper.SERIF: "serif-x", paper.SERIF_B: "serif-b", paper.PEN: "pen", paper.SANS: "sans",
            paper.SANS_X: "sans-x"}.get(Path(FT(role)), "sans")


# ---------------------------------------------------------------- 1) 아카이브 다큐
def _typewriter(D, x, y, text, size, color, at, font="sans", anchor="l"):
    i = D._id()
    spans = "".join(f'<span class="{i}c" style="opacity:0">{_e(ch)}</span>' for ch in text)
    tx = {"l": "0", "m": "-50%", "r": "-100%"}[anchor]
    D.items.append(f'<div style="position:absolute;left:{x:.0f}px;top:{y:.0f}px;transform:translate({tx},-50%);font-family:{font};'
                   f'font-size:{size}px;color:{color};white-space:nowrap;letter-spacing:.02em">{spans}</div>')
    D.js.append(f'tl.to(".{i}c",{{opacity:1,duration:0.01,stagger:0.045}},{at:.2f});')
    D.sfx.append(("click-soft", at))
    return at + 0.045 * len(text)


def _stamp_line(D, text, at, color="#F2EBDD", dark=True):
    """왼쪽 위 날짜·장소 도장: 빨간 세로선 + 타자기 글자. 영상 위에서는 어두운 받침(밝은 하늘 위에서도 대비 3:1 이상)."""
    w = fit(FT("label"), text, 40, 2000).getlength(text) + 44
    if dark:
        i = D._id()
        D.items.append(f'<div id="{i}" style="position:absolute;left:72px;top:88px;width:{w + 24:.0f}px;height:60px;border-radius:6px;'
                       f'background:rgba(12,12,14,.62)"></div>')
        D.js.append(f'tl.fromTo("#{i}",{{opacity:0}},{{opacity:1,duration:0.25}},{max(at - 0.2, 0):.2f});')
    D.items.append(f'<div style="position:absolute;left:84px;top:96px;width:6px;height:44px;background:{D.red}"></div>')
    _typewriter(D, 108, 118, text, 40, color, at)


def s_kb(D, sc, bt, dur):
    """자료 화면 가득 + 켄 번스 움직임 + 필름 가장자리 어둡게 + 타자기 날짜·장소."""
    i = D._id()
    mv = {"in": ((1.0, 0, 0), (1.14, 0, -1.5)), "out": ((1.16, 0, 0), (1.0, 0, 0)), "left": ((1.12, 3, 0), (1.12, -3, 0)),
          "right": ((1.12, -3, 0), (1.12, 3, 0)), "up": ((1.12, 0, 3), (1.12, 0, -3))}[sc.get("move", "in")]
    (s0, x0, y0), (s1, x1, y1) = mv
    D.media.append(f'<div style="position:absolute;inset:0;overflow:hidden;background:#000">'
                   f'<video id="{i}" class="clip" src="assets/{sc["_clipfile"]}" muted playsinline data-start="0" data-duration="{dur:.2f}" '
                   f'data-track-index="2" style="width:100%;height:100%;object-fit:cover"></video></div>'
                   f'<div style="position:absolute;inset:0;background:radial-gradient(ellipse at center,rgba(0,0,0,0) 55%,rgba(0,0,0,.55) 100%)"></div>')
    D.js.append(f'tl.fromTo("#{i}",{{scale:{s0},xPercent:{x0},yPercent:{y0}}},{{scale:{s1},xPercent:{x1},yPercent:{y1},duration:{dur:.2f},ease:"none"}},0);')
    D.label(sc.get("label", ""), dark=True)
    if sc.get("stamp"):
        _stamp_line(D, sc["stamp"], 0.5)
    for b, (t0, d) in zip(sc["beats"], bt):
        if b.get("lower"):
            D.lower(b["lower"]["name"], b["lower"]["role"], t0 + 0.2, dark=True)


def s_card_type(D, sc, bt, dur):
    """검은 카드 + 타자기 글줄 (인용·핵심 문장). 박자마다 한 줄."""
    lines = sc["lines"]
    n = len(lines)
    y0 = HH / 2 - (n - 1) * 75 - (40 if sc.get("by") else 0)
    for k, ln in enumerate(lines):
        t = bt[min(k, len(bt) - 1)][0] + 0.2 + (0 if k < len(bt) else 0.9 * (k - len(bt) + 1))
        f = fit(FT("title"), ln, 92, W - 300)
        _typewriter(D, W / 2, y0 + k * 150, ln, f.size, D.ink, t, font=_fam("title"), anchor="m")
    if sc.get("by"):
        D.text(W / 2, y0 + n * 150 + 10, "— " + sc["by"], FT("label"), 36, "#5a5f6a", at=bt[-1][0] + 0.6)


# ---------------------------------------------------------------- 2) 지도 여정
def _world(points: dict, projection: str = "mercator", center=None, scale: float = 1.0, Wd: int = W, Hd: int = HH) -> dict:
    nm = hyper.TOOLS / "node_modules"
    q = {"W": Wd, "H": Hd, "points": points, "projection": projection, "scale": scale}
    if center:
        q["center"] = center
    r = subprocess.run(["node", str(config.ROOT / "ytflow" / "assets" / "world_map.mjs"), str(nm)],
                       input=json.dumps(q), capture_output=True, text=True, check=True)
    return json.loads(r.stdout)


def _arc(a, b):
    (x0, y0), (x1, y1) = a, b
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    lift = min(220, ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5 * 0.28)
    return f"M{x0:.1f},{y0:.1f} Q{mx:.1f},{my - lift:.1f} {x1:.1f},{y1:.1f}"


def _hex(c: str) -> tuple:
    c = c.lstrip("#")
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def _mix(a: str, b: str, t: float) -> str:
    x, y = _hex(a), _hex(b)
    return "#" + "".join(f"{round(x[i] + (y[i] - x[i]) * t):02X}" for i in range(3))


def _map_colors(D) -> dict:
    """지도 색은 그래픽 팩에서 계산: 바다는 바탕색에 푸른 회색을 섞고, 땅은 밝게, 해안선은 바다보다 조금 진하게."""
    pal = D.skin.get("palette", {})
    base, ink = pal.get("base", "#EEE7DA"), pal.get("ink", D.ink)
    dark = sum(_hex(base)) < 300
    sea = _mix(base, "#5E8A94" if not dark else "#0E2A3A", 0.30 if not dark else 0.45)
    land = _mix(base, "#FFFFFF", 0.45) if not dark else _mix(base, "#FFFFFF", 0.12)
    return {"sea": sea, "sea_line": _mix(sea, ink, 0.18), "land": land, "border": _mix(land, ink, 0.35),
            "coast": _mix(land, ink, 0.55), "grat": _mix(sea, "#FFFFFF", 0.35), "sea_text": _mix(sea, ink, 0.45),
            "card": _mix(base, "#FFFFFF", 0.6) if not dark else pal.get("card", _mix(base, "#000000", 0.25)), "ink": ink, "accent": D.red, "dark": dark}


SEAS = [("대 서 양", [-38, 28]), ("태 평 양", [-150, 12]), ("태 평 양", [165, 18]), ("인 도 양", [78, -18])]


def s_journey(D, sc, bt, dur):
    """세계 지도(직사각형, 화면 꽉 채움): 박자마다 카메라 이동(goto+zoom), 경로선 그리기(route), 핀(pin).
    라벨은 확대해도 화면에서 같은 크기, 화면 밖으로 나간 옛 라벨은 사라짐. 바다 이름·해안선 물결·나침반·종이 질감."""
    places = dict(sc["places"])
    seas = sc.get("seas", SEAS)
    for k2, (_, ll) in enumerate(seas):
        places[f"_sea{k2}"] = ll
    world = _world(places, sc.get("projection", "mercator"), sc.get("center"))
    P, fx0, fy0, fx1, fy1 = world["points"], *world["frame"]
    C = _map_colors(D)
    cam = D._id()
    land = "".join(f'<path d="{c["d"]}"/>' for c in world["countries"])
    hl = set(sc.get("highlight", []))
    hls = "".join(f'<path d="{c["d"]}"/>' for c in world["countries"] if c["name"] in hl)
    g = [f'<g id="{cam}" style="transform-origin:0 0">',
         f'<rect x="{fx0 - 400:.0f}" y="{fy0 - 400:.0f}" width="{fx1 - fx0 + 800:.0f}" height="{fy1 - fy0 + 800:.0f}" fill="{C["sea"]}"/>',
         f'<path d="{world["graticule"]}" fill="none" stroke="{C["grat"]}" stroke-width="0.9" opacity=".55"/>',
         # 옛 지도식 해안 물결선: 땅을 굵은 선으로 세 번 겹쳐 그려 바다 쪽으로 번지게
         f'<g fill="none" stroke="{C["sea_line"]}" stroke-linejoin="round">'
         f'<g stroke-width="14" opacity=".18">{land}</g><g stroke-width="8" opacity=".28">{land}</g></g>',
         f'<g fill="{C["land"]}" stroke="{C["border"]}" stroke-width="0.7" stroke-linejoin="round">{land}</g>',
         f'<g fill="{C["accent"]}" fill-opacity=".28" stroke="{C["accent"]}" stroke-width="1.4">{hls}</g>']
    sea_ids = []
    for k2, (name, _) in enumerate(seas):
        x, y = P[f"_sea{k2}"]
        j = D._id()
        sea_ids.append(j)
        g.append(f'<text id="{j}" x="{x}" y="{y}" text-anchor="middle" font-family="serif-x" font-style="italic" font-size="30" '
                 f'letter-spacing="6" fill="{C["sea_text"]}" opacity=".75">{_e(name)}</text>')
    pins_js, labels, instant_labels = [], [], []
    lab_font = fit(FT("label"), "가", 24, 999)
    zc = [sc.get("start", {}).get("zoom", 1)]

    def pin(key, label, at, instant=False, side=None, dy=0):
        x, y = P[key]
        z = zc[0]
        j = D._id()
        r = 10 / z ** 0.8
        g.append(f'<g id="{j}" style="opacity:0"><circle cx="{x}" cy="{y}" r="{r * 2.6:.2f}" fill="{C["accent"]}" opacity=".18"/>'
                 f'<circle cx="{x}" cy="{y}" r="{r:.2f}" fill="{C["accent"]}" stroke="#FFFFFF" stroke-width="{3 / z:.2f}"/></g>')
        pins_js.append(f'tl.fromTo("#{j}",{{opacity:0,scale:{0.2 if not instant else 1},svgOrigin:"{x} {y}"}},{{opacity:1,scale:1,svgOrigin:"{x} {y}",'
                       f'duration:{0.01 if instant else 0.35},ease:"back.out(3)"}},{at:.2f});')
        if label:
            k = D._id()
            fs, pad, h = 24 / z, 14 / z, 40 / z
            lw = lab_font.getlength(label) / z + 2 * pad
            right_side = (side or ("left" if (x * z + _cx[0]) > W * 0.62 else "right")) != "left"
            lx = x + 20 / z if right_side else x - 20 / z - lw
            ly = y - h - 14 / z + dy / z
            g.append(f'<g id="{k}" style="opacity:0"><rect x="{lx + 3 / z:.1f}" y="{ly + 4 / z:.1f}" width="{lw:.1f}" height="{h:.1f}" fill="#000" opacity=".18"/>'
                     f'<rect x="{lx:.1f}" y="{ly:.1f}" width="{lw:.1f}" height="{h:.1f}" fill="{C["card"]}" stroke="{C["ink"]}" stroke-width="{1.6 / z:.2f}"/>'
                     f'<rect x="{lx:.1f}" y="{ly:.1f}" width="{5 / z:.1f}" height="{h:.1f}" fill="{C["accent"]}"/>'
                     f'<text x="{lx + pad + 3 / z:.1f}" y="{ly + h * 0.7:.1f}" font-family="sans" font-size="{fs:.1f}" fill="{C["ink"]}">{_e(label)}</text></g>')
            pins_js.append(f'tl.to("#{k}",{{opacity:1,duration:{0.01 if instant else 0.35}}},{at + (0 if instant else 0.2):.2f});')
            if instant:
                instant_labels.append(k)
            else:
                for old in labels[:-1]:   # 화면에는 최근 라벨 2개만
                    pins_js.append(f'tl.to("#{old}",{{opacity:0,duration:0.3}},{at:.2f});')
                labels.append(k)
        if not instant:
            D.sfx.append(("pop", at))

    def route(a, b, at, instant=False):
        j, sh = D._id(), D._id()
        d = _arc(P[a], P[b])
        w = 4.5 / zc[0] ** 0.7
        g.append(f'<path id="{sh}" d="{d}" fill="none" stroke="#000" stroke-opacity=".15" stroke-width="{w * 1.8:.2f}" stroke-dasharray="1" '
                 f'stroke-dashoffset="1" pathLength="1" stroke-linecap="round" transform="translate(2,3)"/>'
                 f'<path id="{j}" d="{d}" fill="none" stroke="{C["accent"]}" stroke-width="{w:.2f}" stroke-dasharray="1" '
                 f'stroke-dashoffset="1" pathLength="1" stroke-linecap="round"/>')
        pins_js.append(f'tl.to("#{j},#{sh}",{{strokeDashoffset:0,duration:{0.01 if instant else 1.6},ease:"power1.inOut"}},{at:.2f});')
        if not instant:
            D.sfx.append(("whoosh", at))

    _cx = [0.0]

    def clamp(key, zoom):
        x, y = P[key] if key else ((fx0 + fx1) / 2, HH / 2)
        tx, ty = W / 2 - x * zoom, HH / 2 - y * zoom
        tx = min(max(tx, W - fx1 * zoom), -fx0 * zoom)     # 지도 밖(빈 곳)이 보이지 않게
        ty = min(max(ty, HH - (fy1 + 300) * zoom), -(fy0 - 300) * zoom) if zoom > 1 else 0
        return tx, ty

    start = sc.get("start", {"goto": None, "zoom": 1})
    z = start.get("zoom", 1)
    tx, ty = clamp(start.get("goto"), z)
    _cx[0] = tx
    D.js.append(f'tl.set("#{cam}",{{svgOrigin:"0 0",x:{tx:.1f},y:{ty:.1f},scale:{z}}},0);')
    if z > 2:
        D.js.append("".join(f'tl.set("#{j}",{{opacity:0}},0);' for j in sea_ids))
    for a2, b2 in sc.get("drawn", []):
        route(a2, b2, 0.0, True)
    for p in sc.get("pins", []):
        pin(p["at"], p.get("label", ""), 0.0, True, p.get("side"), p.get("dy", 0))
    moved = False
    for b, (t0, d) in zip(sc["beats"], bt):
        if "goto" in b or "zoom" in b:
            zc[0] = b.get("zoom", 1)
            tx, ty = clamp(b.get("goto"), zc[0])
            _cx[0] = tx
            D.js.append(f'tl.to("#{cam}",{{x:{tx:.1f},y:{ty:.1f},scale:{zc[0]},duration:1.8,ease:"power2.inOut"}},{t0 + 0.1:.2f});')
            D.js.append("".join(f'tl.to("#{j}",{{opacity:{0 if zc[0] > 2 else 0.75},duration:0.6}},{t0 + 0.3:.2f});' for j in sea_ids))
            if not moved:   # 앞 장면에서 넘어온 라벨은 카메라가 움직이면 정리
                D.js.append("".join(f'tl.to("#{j}",{{opacity:0,duration:0.4}},{t0 + 0.1:.2f});' for j in instant_labels))
                moved = True
        if b.get("route"):
            route(*b["route"], t0 + 0.6)
        if b.get("pin"):
            pin(b["pin"]["at"], b["pin"].get("label", ""), t0 + (2.2 if b.get("route") else 0.8), False, b["pin"].get("side"), b["pin"].get("dy", 0))
    g.append("</g>")
    # 화면에 고정: 종이 질감(곱하기) + 가장자리 어둡게 + 나침반
    fixed = (f'<image href="assets/{D.bg_name}" x="0" y="0" width="{W}" height="{HH}" preserveAspectRatio="none" opacity=".45" '
             f'style="mix-blend-mode:multiply"/>'
             f'<defs><radialGradient id="vg{cam}" cx="50%" cy="50%" r="70%"><stop offset="60%" stop-color="#000" stop-opacity="0"/>'
             f'<stop offset="100%" stop-color="#000" stop-opacity=".32"/></radialGradient></defs>'
             f'<rect x="0" y="0" width="{W}" height="{HH}" fill="url(#vg{cam})"/>'
             f'<g transform="translate(1800,950)" opacity=".75" stroke="{C["ink"]}" fill="none" stroke-width="2">'
             f'<circle r="40"/><circle r="30" stroke-width="1"/><path d="M0,-52 L8,0 L0,52 L-8,0 Z" fill="{C["card"]}"/>'
             f'<path d="M0,-52 L8,0 L-8,0 Z" fill="{C["accent"]}" stroke="none"/><path d="M-52,0 L52,0" stroke-width="1"/>'
             f'<text y="-60" text-anchor="middle" font-family="serif-x" font-size="22" fill="{C["ink"]}" stroke="none">N</text></g>')
    D.svg.insert(0, "".join(g) + fixed)
    D.js += pins_js
    D.label(sc.get("label", ""))
    if sc.get("title"):   # 옛 지도 제목 상자 (왼쪽 위)
        f = fit(FT("title"), sc["title"], 46, 900)
        tw = f.getlength(sc["title"]) + 72
        i = D._id()
        D.items.append(f'<div id="{i}" style="position:absolute;left:80px;top:64px;width:{tw:.0f}px;height:92px;background:{C["card"]};'
                       f'border:3px double {C["ink"]};box-shadow:0 8px 20px rgba(0,0,0,.18);font-family:serif-x;font-size:{f.size}px;'
                       f'color:{C["ink"]};display:flex;align-items:center;justify-content:center;white-space:nowrap">{_e(sc["title"])}</div>')
        D.js.append(f'tl.fromTo("#{i}",{{opacity:0,y:-20}},{{opacity:1,y:0,duration:0.5}},0.3);')


# ---------------------------------------------------------------- 3) 키네틱 타이포
def _kinetic_beat(D, sc, k, b, t0, d, top=None, max_size=128, band=False, last=False):
    """한 박자의 말을 단어가 말하는 순간 화면에 박히게. top=세로 위치(없으면 가운데), band=영상 위 어두운 띠."""
    pdir = Path(sc["_project_dir"])
    wav = pdir / "03_voice" / f"hb_{sc['id']:03d}_{k}.wav"
    chunks = hybrid._chunks(b["say"], 16)
    words = [w for c in chunks for w in c.split(" ")]
    starts = hybrid._word_starts(wav, words, d) or [d * i / max(len(words), 1) for i in range(len(words))]
    hits = b.get("hit", [])
    y = HH / 2 - max_size * 0.7 if top is None else top
    if band:
        bi = D._id()
        D.items.append(f'<div id="{bi}" style="position:absolute;left:0;right:0;top:{y - max_size * 0.35:.0f}px;height:{max_size * 1.9:.0f}px;'
                       f'background:linear-gradient(90deg,rgba(10,10,12,0),rgba(10,10,12,.62) 18%,rgba(10,10,12,.62) 82%,rgba(10,10,12,0))"></div>')
        D.js.append(f'tl.fromTo("#{bi}",{{opacity:0}},{{opacity:1,duration:0.25}},{t0:.2f});tl.to("#{bi}",{{opacity:0,duration:0.3}},{t0 + d + 0.1:.2f});')
    base_col = "#FFFFFF" if band else D.ink
    hit_col = _mix(D.red, "#FFFFFF", 0.38) if band else D.red   # 어두운 띠 위에서는 밝은 강조색 (대비 3:1 이상)
    wi = 0
    for ci, c in enumerate(chunks):
        ws = c.split(" ")
        gid = D._id()
        c_start = t0 + starts[wi]
        c_end = t0 + (starts[wi + len(ws)] if wi + len(ws) < len(starts) else d + 0.25)
        size = fit(FT("value"), c, max_size, W - 240).size
        spans = []
        for j, w in enumerate(ws):
            big = any(h in w for h in hits) or bool(re.search(r"\d", w))
            col = hit_col if big else base_col
            sz = int(size * (1.25 if big else 1.0))
            sid = D._id()
            shadow = "text-shadow:0 4px 14px rgba(0,0,0,.6);" if band else ""
            spans.append(f'<span id="{sid}" style="display:inline-block;opacity:0;color:{col};font-size:{sz}px;margin:0 .14em;{shadow}">{_e(w)}</span>')
            at = t0 + starts[wi + j]
            D.js.append(f'tl.fromTo("#{sid}",{{opacity:0,y:40,scale:{1.35 if big else 1.0}}},'
                        f'{{opacity:1,y:0,scale:1,duration:{0.22 if big else 0.16},ease:"back.out(2)"}},{at:.2f});')
            if big:
                D.sfx.append(("pop", at))
        D.items.append(f'<div id="{gid}" style="position:absolute;left:120px;right:120px;top:{y:.0f}px;text-align:center;'
                       f'font-family:{_fam("value")};line-height:1.1;white-space:nowrap">{"".join(spans)}</div>')
        if ci < len(chunks) - 1 or not last:   # 다음 덩어리가 오면 위로 밀려 흐려짐
            if band:   # 띠 위에서는 다음 줄이 나오기 전에 완전히 빠진다 (두 줄이 겹쳐 보이지 않게)
                D.js.append(f'tl.to("#{gid}",{{y:-40,opacity:0.0,duration:0.15,ease:"power2.in"}},{max(c_end - 0.22, c_start + 0.3):.2f});')
            else:
                D.js.append(f'tl.to("#{gid}",{{y:-170,opacity:0.0,duration:0.3,ease:"power2.in"}},{max(c_end - 0.12, c_start + 0.3):.2f});')
        wi += len(ws)


def _keyword_pop(D, sc, k, hits, t0, d, top, size=96):
    """겹치기용 강조: 문장 전체가 아니라 '핵심 단어 1~3개'만, 그 말을 하는 순간 한 번 띄웠다 사라진다.
    (아래 자막과 같은 문장을 위에 반복하지 않는다 — 2026-11-09 사용자 판정: 강조 남용 금지)"""
    hits = [h for h in hits if h][:3]
    if not hits:
        return
    pdir = Path(sc["_project_dir"])
    wav = pdir / "03_voice" / f"hb_{sc['id']:03d}_{k}.wav"
    words = sc["beats"][k]["say"].split(" ")
    starts = hybrid._word_starts(wav, words, d) or [d * i / max(len(words), 1) for i in range(len(words))]
    first = next((i for i, w in enumerate(words) if any(h in w for h in hits)), 0)
    at = t0 + starts[first]
    text = " ".join(hits)
    f = fit(FT("value"), text, size, W - 400)
    i = D._id()
    D.items.append(f'<div id="{i}" style="position:absolute;left:0;right:0;top:{top:.0f}px;text-align:center;opacity:0">'
                   f'<span style="display:inline-block;padding:10px 34px;border-radius:10px;background:rgba(12,12,14,.66);'
                   f'font-family:{_fam("value")};font-size:{f.size}px;color:{_mix(D.red, "#FFFFFF", 0.38)};white-space:nowrap">{_e(text)}</span></div>')
    D.js.append(f'tl.fromTo("#{i}",{{opacity:0,scale:1.25}},{{opacity:1,scale:1,duration:0.22,ease:"back.out(2)"}},{at:.2f});'
                f'tl.to("#{i}",{{opacity:0,duration:0.3}},{min(at + 1.8, t0 + d):.2f});')
    D.sfx.append(("pop", at))


def s_kinetic(D, sc, bt, dur):
    """목소리가 말하는 순간 단어가 화면에 박힌다. 덩어리(한 줄) 단위로 위로 밀려 올라가며 바뀜. 강조 단어·숫자는 크게, 강조색."""
    for k, (b, (t0, d)) in enumerate(zip(sc["beats"], bt)):
        _kinetic_beat(D, sc, k, b, t0, d, last=(k == len(bt) - 1))
        if b.get("note"):
            D.text(W / 2, HH / 2 + 170, b["note"], FT("note"), 46, "#5a5f6a", at=t0 + 0.6)
    D.label(sc.get("label", ""))


# ---------------------------------------------------------------- 4) 한 장면 안에서 스타일 겹치기 (layers)
LAYER_KINDS = {"words": "kinetic-type", "photo": "archive-doc", "stamp": "archive-doc", "line": "archive-doc",
               "locator": "map-journey", "number": "data-report", "mark": "hand-annotate"}


def _cut(project, spec, src: str, start: float, dur: float, out: Path, w: int = 1280, h: int = 720):
    f = project.dir("assets") / "footage" / spec["footage"][src]["file"]
    if not out.exists():
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", str(start), "-i", str(f), "-t", f"{dur + 0.5:.2f}", "-an",
                        "-vf", f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},fps=30",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p", str(out)], check=True)
    return out.name


def apply_layers(D, project, spec, sc, bt, dur, adir: Path):
    """sc["layers"]: 바탕 장면(어떤 type 이든) 위에 다른 스타일 요소를 겹친다.
    words   {beat, hit[1~3], y}         핵심 단어만 한 번 (문장 전체 금지, 자막과 중복 금지) — kinetic-type
    photo   {src, start, beat, side, caption, w}   자료 사진·영상 액자 (화면 속 화면)  — archive-doc
    stamp   {text, beat}                타자기 날짜·장소 도장                      — archive-doc
    line    {text, beat}                영상 위 타자기 한 줄 (아래 3분의 1 띠)       — archive-doc
    locator {at:[경도,위도], label, beat, side}   위치 미니 지도                    — map-journey
    number  {value, label, beat, side}  큰 숫자 카드                               — data-report
    """
    def at_of(L):
        k = min(L.get("beat", 0), len(bt) - 1)
        return bt[k][0] + L.get("delay", 0.3), k

    for n, L in enumerate(sc["layers"]):
        kind = L["kind"]
        t, k = at_of(L)
        side = L.get("side", "right")
        if kind == "words":
            _keyword_pop(D, sc, k, L.get("hit", []), bt[k][0], bt[k][1], HH * L.get("y", 0.16), L.get("size", 96))
        elif kind == "photo":
            w = L.get("w", 640)
            h = int(w * 9 / 16)
            name = _cut(project, spec, L["src"], L.get("start", 0), dur, adir / f"layer_{sc['id']:03d}_{n}.mp4")
            x = W - w - 120 if side == "right" else 120
            y = L.get("top", 150)
            i = D._id()
            rot = 2.2 if side == "right" else -2.2
            cap = (f'<div style="position:absolute;left:0;right:0;bottom:16px;text-align:center;font-family:pen;font-size:30px;color:{D.ink}">{_e(L["caption"])}</div>'
                   if L.get("caption") else "")
            if not hasattr(D, "top"):
                D.top = []
            D.top.append(f'<div id="{i}" style="position:absolute;left:{x - 16}px;top:{y - 16}px;width:{w + 32}px;height:{h + (84 if cap else 32)}px;'
                           f'background:#FBF8F1;box-shadow:0 18px 40px rgba(0,0,0,.35);transform:rotate({rot}deg)">'
                           f'<div style="position:absolute;left:16px;top:16px;width:{w}px;height:{h}px;overflow:hidden">'
                           f'<video id="{i}v" class="clip" src="assets/{name}" muted playsinline data-start="0" data-duration="{dur:.2f}" data-track-index="{3 + n}" '
                           f'style="width:100%;height:100%;object-fit:cover;filter:grayscale(.3) contrast(1.05)"></video></div>{cap}'
                           f'<div style="position:absolute;left:{w / 2 - 70:.0f}px;top:-22px;width:140px;height:40px;background:rgba(236,220,170,.85);transform:rotate(-4deg)"></div></div>')
            D.js.append(f'tl.fromTo("#{i}",{{opacity:0,y:60,rotation:{rot * 3}}},{{opacity:1,y:0,rotation:{rot},duration:0.55,ease:"back.out(1.4)"}},{t:.2f});')
            if L.get("until") is not None:
                D.js.append(f'tl.to("#{i}",{{opacity:0,y:40,duration:0.4}},{bt[min(L["until"], len(bt) - 1)][0]:.2f});')
            D.sfx.append(("whoosh", t))
        elif kind == "stamp":
            dark = L.get("dark", True)
            _stamp_line(D, L["text"], t, L.get("color", "#F2EBDD" if dark else D.ink), dark)
        elif kind == "line":
            i = D._id()
            D.items.append(f'<div id="{i}" style="position:absolute;left:0;right:0;top:{HH * 0.62:.0f}px;height:150px;'
                           f'background:linear-gradient(90deg,rgba(8,8,10,.0),rgba(8,8,10,.7) 15%,rgba(8,8,10,.7) 85%,rgba(8,8,10,0))"></div>')
            D.js.append(f'tl.fromTo("#{i}",{{opacity:0}},{{opacity:1,duration:0.3}},{t - 0.1:.2f});')
            f = fit(FT("title"), L["text"], 64, W - 400)
            _typewriter(D, W / 2, HH * 0.62 + 75, L["text"], f.size, "#F6F0E4", t, font=_fam("title"), anchor="m")
        elif kind == "locator":
            mw, mh = 420, 236
            wm = _world({"p": L["at"]}, "mercator", L.get("center", L["at"]), L.get("scale", 3.0), mw, mh)
            C = _map_colors(D)
            px, py = wm["points"]["p"]
            land = "".join(f'<path d="{c["d"]}"/>' for c in wm["countries"])
            x = W - mw - 90 if side == "right" else 90
            y = L.get("top", 120)
            i = D._id()
            lab = (f'<div style="position:absolute;left:0;right:0;bottom:0;height:40px;line-height:40px;text-align:center;font-family:sans;'
                   f'font-size:24px;color:#FFFFFF;background:rgba(12,12,14,.66)">{_e(L.get("label", ""))}</div>') if L.get("label") else ""
            D.items.append(f'<div id="{i}" style="position:absolute;left:{x}px;top:{y}px;width:{mw}px;height:{mh}px;border:4px solid #FBF8F1;'
                           f'box-shadow:0 14px 34px rgba(0,0,0,.4);background:{C["sea"]}">'
                           f'<svg width="{mw}" height="{mh}" viewBox="0 0 {mw} {mh}" style="position:absolute;inset:0">'
                           f'<g fill="{C["land"]}" stroke="{C["border"]}" stroke-width=".8">{land}</g>'
                           f'<circle cx="{px}" cy="{py}" r="26" fill="{D.red}" opacity=".22"/><circle cx="{px}" cy="{py}" r="9" fill="{D.red}" stroke="#fff" stroke-width="3"/></svg>{lab}</div>')
            D.js.append(f'tl.fromTo("#{i}",{{opacity:0,scale:.85}},{{opacity:1,scale:1,duration:0.45,ease:"back.out(1.6)"}},{t:.2f});')
            D.sfx.append(("pop", t + 0.2))
        elif kind == "number":
            i = D._id()
            f = fit(FT("value"), L["value"], 120, 700)
            lf = fit(FT("label"), L.get("label", ""), 34, 700)
            w = max(f.getlength(L["value"]), lf.getlength(L.get("label", ""))) + 90
            x = W - w - 110 if side == "right" else 110
            D.items.append(f'<div id="{i}" style="position:absolute;left:{x:.0f}px;top:{L.get("top", 170)}px;width:{w:.0f}px;height:230px;background:#FBF8F1;'
                           f'box-shadow:0 14px 34px rgba(0,0,0,.35);border-top:10px solid {D.red}">'
                           f'<div style="position:absolute;left:0;right:0;top:26px;text-align:center;font-family:{_fam("value")};font-size:{f.size}px;color:{D.red}">{_e(L["value"])}</div>'
                           f'<div style="position:absolute;left:0;right:0;top:168px;text-align:center;font-family:sans;font-size:{lf.size}px;color:#3a3a3a">{_e(L.get("label", ""))}</div></div>')
            D.js.append(f'tl.fromTo("#{i}",{{opacity:0,y:-30}},{{opacity:1,y:0,duration:0.45,ease:"back.out(1.8)"}},{t:.2f});')
            D.sfx.append(("impact-bass-1", t + 0.1))
        elif kind == "mark":
            _layer_mark(D, L, t, bt[k][0] + bt[k][1])
        else:
            D.qa.append(f"장면 {sc['id']}: 모르는 layer kind '{kind}'")



# ---------------------------------------------------------------- 5) 새 스타일 풀 (2026-11-09, HyperFrames 레지스트리 블록에서 아이디어: chat-thread·code-terminal-run·cursor-zoom-follow·cursor-annotate·world-map)
def _card(D, x, y, w, h, title, dark=False):
    bg, bar, fg = ("#151413", "#232220", "#8E8981") if dark else ("#FFFFFF", "#F1EEE8", "#7D776D")
    i = D._id()
    D.items.append(f'<div id="{i}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:18px;overflow:hidden;'
                   f'background:{bg};box-shadow:0 24px 60px rgba(0,0,0,.22),0 0 0 1px rgba(0,0,0,.06)">'
                   f'<div style="height:52px;background:{bar};display:flex;align-items:center;gap:10px;padding:0 22px">'
                   f'<i style="width:13px;height:13px;border-radius:7px;background:#d9d4cb;display:block"></i><i style="width:13px;height:13px;border-radius:7px;background:#d9d4cb;display:block"></i>'
                   f'<i style="width:13px;height:13px;border-radius:7px;background:#d9d4cb;display:block"></i>'
                   f'<span style="margin-left:14px;font-family:sans;font-size:22px;color:{fg}">{_e(title)}</span></div></div>')
    D.js.append(f'tl.fromTo("#{i}",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.45,ease:"power2.out"}},0.15);')
    return i


def s_chat(D, sc, bt, dur):
    """AI 대화 화면: 질문이 타자로 쳐지고, 답이 단어 단위로 흘러나온다 (상표·로고 없이 '예시(재구성)'로 표시).
    turns: [{role: user|ai, text, beat}]"""
    x, y, w, h = 360, 120, 1200, 800
    _card(D, x, y, w, h, sc.get("app", "AI 대화 · 재구성 예시"))
    cy = y + 90
    for n, tn in enumerate(sc["turns"]):
        k = min(tn.get("beat", n), len(bt) - 1)
        at = bt[k][0] + tn.get("delay", 0.2)
        text = tn["text"]
        f = fit(FT("label"), "가", 30, 999)
        lines = []
        cur = ""
        for word in text.split(" "):
            if f.getlength((cur + " " + word).strip()) > 760 and cur:
                lines.append(cur); cur = word
            else:
                cur = (cur + " " + word).strip()
        lines.append(cur)
        bh = 30 * 1.5 * len(lines) + 44
        user = tn["role"] == "user"
        bx = x + w - 60 - 820 if user else x + 60
        i = D._id()
        bg, fg = ("#171614", "#F6F2EA") if user else ("#F1EEE8", "#171614")
        if user:   # 타자 치듯
            spans = "".join(f'<span class="{i}c" style="opacity:0">{_e(ch)}</span>' for ch in text)
            D.js.append(f'tl.to(".{i}c",{{opacity:1,duration:0.01,stagger:{min(0.04, 1.2 / max(len(text), 1)):.3f}}},{at:.2f});')
        else:      # 단어 단위로 흘러나옴
            spans = "".join(f'<span class="{i}w" style="opacity:0">{_e(wd)} </span>' for wd in text.split(" "))
            D.js.append(f'tl.to(".{i}w",{{opacity:1,duration:0.08,stagger:0.07}},{at + 0.4:.2f});')
        D.items.append(f'<div id="{i}" style="position:absolute;left:{bx}px;top:{cy}px;width:820px;opacity:0">'
                       f'<div style="display:inline-block;{"float:right;" if user else ""}max-width:820px;padding:22px 28px;border-radius:20px;background:{bg};'
                       f'color:{fg};font-family:sans;font-size:30px;line-height:1.5">{spans}</div></div>')
        D.js.append(f'tl.to("#{i}",{{opacity:1,duration:0.2}},{at - 0.1:.2f});')
        cy += bh + 30
    D.label(sc.get("label", ""))


def s_terminal(D, sc, bt, dur):
    """터미널: 명령이 타자로, 결과가 줄 단위로. lines: [{cmd|out, beat}] — 실제 실행 기록만 (설명용이면 label 에 '재구성')."""
    x, y, w, h = 210, 110, 1500, 820
    _card(D, x, y, w, h, sc.get("title", "터미널"), dark=True)
    ly = y + 100
    for n, ln in enumerate(sc["lines"]):
        k = min(ln.get("beat", 0), len(bt) - 1)
        at = bt[k][0] + ln.get("delay", 0.3 + 0.35 * n)
        i = D._id()
        if "cmd" in ln:
            spans = "".join(f'<span class="{i}c" style="opacity:0">{_e(ch)}</span>' for ch in ln["cmd"])
            D.items.append(f'<div style="position:absolute;left:{x + 44}px;top:{ly}px;font-family:monospace;font-size:30px;color:#EDEAE4;white-space:pre">'
                           f'<span style="color:#E8622C">$ </span>{spans}</div>')
            D.js.append(f'tl.to(".{i}c",{{opacity:1,duration:0.01,stagger:0.03}},{at:.2f});')
        else:
            D.items.append(f'<div id="{i}" style="position:absolute;left:{x + 44}px;top:{ly}px;font-family:monospace;font-size:30px;color:#9FB79A;'
                           f'white-space:pre;opacity:0">{_e(ln["out"])}</div>')
            D.js.append(f'tl.to("#{i}",{{opacity:1,duration:0.15}},{at:.2f});')
        ly += 50
    D.label(sc.get("label", ""))


def s_zoomshot(D, sc, bt, dur):
    """화면 녹화 자동 줌: 자료 화면 위에서 카메라가 박자마다 지정한 네모로 다가가고, 그 자리를 얇은 선으로 표시.
    focus: [{beat, box:[x,y,w,h] (1920×1080 기준), label}] — 마지막엔 box 없이 {beat, out:true} 로 전체로 돌아올 수 있음"""
    i = D._id()
    D.media.append(f'<div id="{i}" style="position:absolute;left:0;top:0;width:{W}px;height:{HH}px;overflow:hidden;background:#000;transform-origin:0 0">'
                   f'<video id="{i}v" class="clip" src="assets/{sc["_clipfile"]}" muted playsinline data-start="0" data-duration="{dur:.2f}" '
                   f'data-track-index="2" style="width:100%;height:100%;object-fit:cover"></video></div>')
    for f in sc.get("focus", []):
        k = min(f.get("beat", 0), len(bt) - 1)
        at = bt[k][0] + f.get("delay", 0.2)
        if f.get("out"):
            D.js.append(f'tl.to("#{i}",{{scale:1,x:0,y:0,duration:0.9,ease:"power2.inOut"}},{at:.2f});')
            continue
        bx, by, bw, bh = f["box"]
        z = min(W / bw, HH / bh) * 0.82
        tx, ty = W / 2 - (bx + bw / 2) * z, HH / 2 - (by + bh / 2) * z
        tx, ty = min(0, max(tx, W - W * z)), min(0, max(ty, HH - HH * z))
        D.js.append(f'tl.to("#{i}",{{scale:{z:.3f},x:{tx:.1f},y:{ty:.1f},duration:0.9,ease:"power2.inOut"}},{at:.2f});')
        o = D._id()
        sx, sy = bx * z + tx, by * z + ty
        D.items.append(f'<div id="{o}" style="position:absolute;left:{sx - 8:.0f}px;top:{sy - 8:.0f}px;width:{bw * z + 16:.0f}px;height:{bh * z + 16:.0f}px;'
                       f'border:3px solid {D.red};border-radius:10px;opacity:0"></div>')
        D.js.append(f'tl.to("#{o}",{{opacity:1,duration:0.25}},{at + 0.9:.2f});tl.to("#{o}",{{opacity:0,duration:0.25}},{bt[k][0] + bt[k][1]:.2f});')
        if f.get("label"):
            lb = D._id()
            D.items.append(f'<div id="{lb}" style="position:absolute;left:{sx - 8:.0f}px;top:{max(sy - 58, 20):.0f}px;padding:6px 14px;border-radius:6px;'
                           f'background:{D.red};color:#fff;font-family:sans;font-size:26px;opacity:0;white-space:nowrap">{_e(f["label"])}</div>')
            D.js.append(f'tl.to("#{lb}",{{opacity:1,duration:0.25}},{at + 1.0:.2f});tl.to("#{lb}",{{opacity:0,duration:0.25}},{bt[k][0] + bt[k][1]:.2f});')
    D.label(sc.get("label", ""), dark=True)


def s_choropleth(D, sc, bt, dur):
    """나라별 색칠 지도: values{나라 영문명: 숫자}, 박자마다 show[나라] 를 색칠, 범례. (world-atlas, 직사각형 지도)"""
    world = _world({}, "mercator", sc.get("center"))
    C = _map_colors(D)
    vals = sc["values"]
    hi = max(vals.values()) or 1
    land = "".join(f'<path d="{c["d"]}"/>' for c in world["countries"])
    g = [f'<rect x="0" y="0" width="{W}" height="{HH}" fill="{C["sea"]}"/>',
         f'<g fill="{C["land"]}" stroke="{C["border"]}" stroke-width="0.7">{land}</g>']
    shown = {}
    for k, b in enumerate(sc["beats"]):
        for name in b.get("show", []):
            shown.setdefault(name, k)
    for c in world["countries"]:
        if c["name"] in vals:
            k = min(shown.get(c["name"], 0), len(bt) - 1)
            j = D._id()
            op = 0.25 + 0.75 * vals[c["name"]] / hi
            g.append(f'<path id="{j}" d="{c["d"]}" fill="{C["accent"]}" fill-opacity="{op:.2f}" stroke="{C["accent"]}" stroke-width="1" style="opacity:0"/>')
            D.js.append(f'tl.to("#{j}",{{opacity:1,duration:0.5}},{bt[k][0] + 0.3:.2f});')
    D.svg.insert(0, "".join(g))
    D.label(sc.get("label", ""))
    if sc.get("title"):
        f = fit(FT("title"), sc["title"], 46, 900)
        D.items.append(f'<div style="position:absolute;left:80px;top:64px;padding:14px 30px;background:{C["card"]};border:3px double {C["ink"]};'
                       f'font-family:serif-x;font-size:{f.size}px;color:{C["ink"]}">{_e(sc["title"])}</div>')
    if sc.get("legend"):
        D.items.append(f'<div style="position:absolute;left:80px;bottom:150px;padding:12px 20px;background:{C["card"]};border-radius:8px;font-family:sans;'
                       f'font-size:24px;color:{C["ink"]};display:flex;align-items:center;gap:14px">'
                       f'<span style="width:120px;height:16px;border-radius:4px;background:linear-gradient(90deg,{C["accent"]}40,{C["accent"]})"></span>{_e(sc["legend"])}</div>')


def _layer_mark(D, L, at, end):
    """손그림 표시 (동그라미·밑줄·화살표) — 강조 예산에 포함."""
    x, y, w, h = L["box"]
    shape = L.get("shape", "circle")
    if shape == "circle":
        D.rough("ellipse", [x + w / 2, y + h / 2, w * 1.15, h * 1.35], D.red, 4, at=at, dur=0.5, roughness=1.6)
    elif shape == "underline":
        D.rough("line", [x, y + h + 8, x + w, y + h + 4], D.red, 5, at=at, dur=0.4, roughness=1.4)
    else:
        D.rough("line", [x - 160, y + h + 120, x - 10, y + h / 2 + 10], D.red, 5, at=at, dur=0.4, roughness=1.2)


# ---------------------------------------------------------------- 오프닝 (MC 진행) — manual v8
def s_intro(D, sc, bt, dur):
    """본론 전 MC 오프닝: 시리즈 배지·기준 시각 → 오늘의 제목 → 오늘 순서(장 제목을 대본에서 자동으로).
    박자: 인사(배지) → 오늘 이야기(제목) → 순서 예고(agenda_beat 부터 목록) → '그럼 시작해 보겠습니다'."""
    acc = D.red
    lum = sum(c * w for c, w in zip(_hex(acc), (0.299, 0.587, 0.114)))
    on_acc = "#15171D" if lum > 140 else "#FFFFFF"
    i = D._id()
    D.items.append(f'<div id="{i}" style="position:absolute;left:150px;top:150px;display:flex;align-items:center;gap:18px;font-family:sans-x;font-size:34px;color:{D.ink}">'
                   f'<span style="background:{acc};color:{on_acc};padding:6px 20px;border-radius:6px;font-weight:700">{_e(sc.get("series", ""))}</span>'
                   f'<span style="opacity:.8">{_e(sc.get("as_of", ""))}</span></div>')
    D.js.append(f'tl.fromTo("#{i}",{{opacity:0,x:-30}},{{opacity:1,x:0,duration:0.5}},{bt[0][0] + 0.2:.2f});')
    tb = bt[min(1, len(bt) - 1)][0] + 0.2
    for k, ln in enumerate(sc.get("title_lines", [])):
        f = fit(FT("title"), ln, 84, W - 420)
        _typewriter(D, 150, 290 + k * 112, ln, f.size, D.ink, tb + k * 0.6, font=_fam("title"), anchor="l")
    items = sc.get("agenda") or sc.get("_chapters", [])
    acc_t = hybrid.accent_text(D)   # 밝은 팩에서도 번호가 읽히게
    ab = sc.get("agenda_beat", 2)
    t0 = bt[min(ab, len(bt) - 1)][0] + 0.3
    span = max(1.2, bt[min(ab, len(bt) - 1)][1] - 0.8)
    y0 = 560 if len(items) <= 4 else 530
    gap = min(84, 420 / max(1, len(items)))
    for k, it in enumerate(items):
        j = D._id()
        D.items.append(f'<div id="{j}" style="position:absolute;left:160px;top:{y0 + k * gap:.0f}px;display:flex;align-items:center;gap:22px;'
                       f'font-family:sans-x;font-size:38px;color:{D.ink};opacity:0">'
                       f'<span style="width:52px;height:52px;border-radius:50%;border:3px solid {acc_t};color:{acc_t};display:flex;align-items:center;'
                       f'justify-content:center;font-size:28px;font-weight:700">{k + 1}</span>{_e(it)}</div>')
        D.js.append(f'tl.fromTo("#{j}",{{opacity:0,x:-24}},{{opacity:1,x:0,duration:0.35}},{t0 + k * span / max(1, len(items)):.2f});')


def register():
    hybrid.RENDER.update({"kb": s_kb, "card_type": s_card_type, "journey": s_journey, "kinetic": s_kinetic,
                          "chat": s_chat, "terminal": s_terminal, "zoomshot": s_zoomshot, "choropleth": s_choropleth, "intro": s_intro})


# ---------------------------------------------------------------- 시각 효과 (manual v9: 반복 피로 막기)
FX = {
    "tilt": "3D 기울기로 들어와 펴지는 카메라 (도형·글씨 장면을 '물체'처럼)",
    "dolly": "장면 내내 천천히 밀고 들어가며 옆으로 흐르는 카메라",
    "dust": "빛 속 먼지 입자가 떠다님 (깊이감)",
    "leak": "필름 빛샘이 화면을 쓸고 지나감 (따뜻한 전환감)",
    "photofill": "큰 숫자·글자 안을 자료 사진으로 채움 (bignum·card_type, fill_src)",
    "scan": "위에서 아래로 훑는 스캔 빛줄기 (자료·문서 느낌)",
}


def _rnd(seed):
    import random
    return random.Random(seed)


def apply_fx(D, project, spec, sc, bt, dur, adir):
    fx = sc.get("fx") or []
    if isinstance(fx, str):
        fx = [fx]
    if not fx:
        return
    R = _rnd(sc["id"] * 31 + 7)
    if "tilt" in fx or "dolly" in fx:
        D.css.append("#root{perspective:1800px}#layer{transform-origin:50% 55%;will-change:transform}")
    if "tilt" in fx:
        rx, ry = R.choice([5, -4, 6]), R.choice([-6, 5, -5])   # v12: 기울기 약하게
        D.js.append(f'tl.fromTo("#layer",{{rotationX:{rx},rotationY:{ry},scale:0.9,y:40}},'
                    f'{{rotationX:0,rotationY:0,scale:1,y:0,duration:2.4,ease:"power3.out"}},0);')
        if dur > 6:
            D.js.append(f'tl.to("#layer",{{rotationY:{-ry / 6:.1f},rotationX:{rx / 8:.1f},duration:{dur - 2.6:.2f},ease:"sine.inOut"}},2.4);')
    if "dolly" in fx:
        D.js.append(f'tl.fromTo("#layer",{{scale:1.0,x:{R.choice([30, -30])}}},{{scale:1.07,x:0,duration:{dur:.2f},ease:"none"}},0);')
    if "dust" in fx:
        parts = []
        for k in range(18):   # v12: 먼지 적게
            x, y, s = R.uniform(0, W), R.uniform(0, HH), R.uniform(2, 7)
            j = D._id()
            parts.append(f'<div id="{j}" style="position:absolute;left:{x:.0f}px;top:{y:.0f}px;width:{s:.1f}px;height:{s:.1f}px;border-radius:50%;'
                         f'background:rgba(255,240,210,{R.uniform(.12, .38):.2f});filter:blur({R.uniform(0, 1.6):.1f}px)"></div>')
            D.js.append(f'tl.to("#{j}",{{x:{R.uniform(-80, 80):.0f},y:{R.uniform(-160, -40):.0f},duration:{dur:.2f},ease:"none"}},0);')
        D.top = getattr(D, "top", []) + [f'<div style="position:absolute;inset:0;pointer-events:none">{"".join(parts)}</div>']
    if "leak" in fx:
        j = D._id()
        D.top = getattr(D, "top", []) + [
            f'<div id="{j}" style="position:absolute;left:-60%;top:-20%;width:90%;height:140%;pointer-events:none;mix-blend-mode:screen;opacity:0;'
            f'background:radial-gradient(ellipse at center,rgba(255,170,80,.55) 0%,rgba(255,90,40,.25) 35%,rgba(0,0,0,0) 70%)"></div>']
        t = bt[min(1, len(bt) - 1)][0] if len(bt) > 1 else 0.3
        D.js.append(f'tl.fromTo("#{j}",{{opacity:0,x:0}},{{opacity:1,x:{W * 0.9:.0f},duration:2.6,ease:"sine.inOut"}},{t:.2f});'
                    f'tl.to("#{j}",{{opacity:0,duration:0.8}},{t + 2.2:.2f});')
    if "scan" in fx:
        j = D._id()
        D.top = getattr(D, "top", []) + [
            f'<div id="{j}" style="position:absolute;left:0;right:0;top:-120px;height:120px;pointer-events:none;mix-blend-mode:screen;'
            f'background:linear-gradient(180deg,rgba(120,200,255,0) 0%,rgba(120,200,255,.18) 60%,rgba(200,240,255,.35) 100%)"></div>']
        D.js.append(f'tl.fromTo("#{j}",{{y:0}},{{y:{HH + 240},duration:2.2,ease:"power1.inOut"}},{bt[0][0] + 0.4:.2f});')
    if "photofill" in fx:
        from . import backdrop
        still = backdrop.photo_still(project, spec, sc.get("fill_src") or sc.get("bg_src"))
        if still:
            name = f"fill_{sc['id']:03d}.jpg"
            shutil.copy(still, adir / name)
            target = sc.get("value") or (sc.get("lines") or [""])[0]
            for n, it in enumerate(D.items):
                if f">{_e(target)}</span>" in it:
                    D.items[n] = it.replace("<span id=", f'<span style="background:url(assets/{name}) 50% 50%/cover;-webkit-background-clip:text;'
                                                         f'background-clip:text;color:transparent;-webkit-text-stroke:2px {D.ink}" class="pf" id=', 1)
                    D.js.append(f'tl.fromTo(".pf",{{backgroundPosition:"30% 40%"}},{{backgroundPosition:"70% 60%",duration:{dur:.2f},ease:"none"}},0);')
                    break
