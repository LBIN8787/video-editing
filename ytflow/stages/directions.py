"""새 연출 문법 3종 — 기존 hybrid 장면은 그대로 두고 장면 type 만 '추가'한다 (docs/16-new-styles.md).

1) archive  아카이브 다큐 (켄 번스식): 자료 사진·영상을 화면 가득 천천히 훑기 + 타자기 날짜·장소 + 검은 카드 인용
     type "kb"        : clip{src}, move(in|out|left|right|up), stamp "1918 · 프랑스", 박자 lower
     type "card_type" : lines[], by, 박자마다 한 줄씩
2) journey  지도 여정 (Johnny Harris식): 세계 지도 위 카메라 이동 + 경로선 그리기 + 핀
     type "journey"   : places{key:[경도,위도]}, 박자 goto/zoom, route[a,b], pin{at,label}, 장면 시작 때 이미 그려진 drawn[[a,b]]·pins[]
3) kinetic  키네틱 타이포: 목소리가 말하는 순간 그 단어가 화면에 크게 박힘 (단어 시각 = faster-whisper)
     type "kinetic"   : 박자 hit[] (강조 단어), 숫자는 자동으로 크게
"""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

from .. import config
from . import hybrid, hyper
from .hybrid import FT, HH, W, _e, fit


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
        D.items.append(f'<div style="position:absolute;left:84px;top:96px;width:6px;height:44px;background:{D.red}"></div>')
        _typewriter(D, 108, 118, sc["stamp"], 40, "#F2EBDD", 0.5)
    for b, (t0, d) in zip(sc["beats"], bt):
        if b.get("lower"):
            D.lower(b["lower"]["name"], b["lower"]["role"], t0 + 0.2, dark=True)


def s_card_type(D, sc, bt, dur):
    """검은 카드 + 타자기 글줄 (인용·핵심 문장). 박자마다 한 줄."""
    lines = sc["lines"]
    n = len(lines)
    y0 = HH / 2 - (n - 1) * 70
    for k, ln in enumerate(lines):
        t = bt[min(k, len(bt) - 1)][0] + 0.2 + (0 if k < len(bt) else 0.9 * (k - len(bt) + 1))
        f = fit(FT("title"), ln, 66, W - 360)
        _typewriter(D, W / 2, y0 + k * 140, ln, f.size, D.ink, t, font="serif-x", anchor="m")
    if sc.get("by"):
        D.text(W / 2, y0 + n * 140 + 10, "— " + sc["by"], FT("label"), 32, "#5a5f6a", at=bt[-1][0] + 0.6)


# ---------------------------------------------------------------- 2) 지도 여정
def _world(points: dict) -> dict:
    nm = hyper.TOOLS / "node_modules"
    r = subprocess.run(["node", str(config.ROOT / "ytflow" / "assets" / "world_map.mjs"), str(nm)],
                       input=json.dumps({"W": W, "H": HH, "points": points}), capture_output=True, text=True, check=True)
    return json.loads(r.stdout)


def _arc(a, b):
    (x0, y0), (x1, y1) = a, b
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    lift = min(220, ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5 * 0.28)
    return f"M{x0:.1f},{y0:.1f} Q{mx:.1f},{my - lift:.1f} {x1:.1f},{y1:.1f}"


def s_journey(D, sc, bt, dur):
    """세계 지도: 박자마다 카메라 이동(goto+zoom), 경로선 그리기(route), 핀(pin). 앞 장면 경로는 drawn 으로 처음부터."""
    world = _world(sc["places"])
    P = world["points"]
    cam = D._id()
    land = "".join(f'<path d="{c["d"]}"/>' for c in world["countries"])
    hl = set(sc.get("highlight", []))
    hls = "".join(f'<path d="{c["d"]}"/>' for c in world["countries"] if c["name"] in hl)
    g = [f'<g id="{cam}" style="transform-origin:0 0">',
         f'<path d="{world["sphere"]}" fill="#F7F2E6" stroke="#9a9488" stroke-width="2"/>',
         f'<path d="{world["graticule"]}" fill="none" stroke="#c9c0ae" stroke-width="0.8" opacity=".7"/>',
         f'<g fill="#B9B09E" stroke="#7d7568" stroke-width="0.6">{land}</g>',
         f'<g fill="#C4452F" fill-opacity=".25" stroke="#C4452F" stroke-width="1.2">{hls}</g>']
    pins_js = []

    def pin(key, label, at, instant=False):
        x, y = P[key]
        j = D._id()
        g.append(f'<g id="{j}" style="opacity:0"><circle cx="{x}" cy="{y}" r="9" fill="#C4452F" stroke="#FBF8F1" stroke-width="3"/>'
                 f'<circle cx="{x}" cy="{y}" r="22" fill="none" stroke="#C4452F" stroke-width="2.5" opacity=".6"/></g>')
        pins_js.append(f'tl.to("#{j}",{{opacity:1,duration:{0.01 if instant else 0.3}}},{at:.2f});')
        if label:
            k = D._id()
            g.append(f'<g id="{k}" style="opacity:0"><rect x="{x + 18}" y="{y - 52}" width="{len(label) * 17 + 34}" height="40" rx="4" '
                     f'fill="#FBF8F1" stroke="#22304D" stroke-width="1.5"/>'
                     f'<text x="{x + 34}" y="{y - 25}" font-family="sans" font-size="24" fill="#22304D">{_e(label)}</text></g>')
            pins_js.append(f'tl.to("#{k}",{{opacity:1,duration:{0.01 if instant else 0.35}}},{at + (0 if instant else 0.2):.2f});')
        if not instant:
            D.sfx.append(("pop", at))

    def route(a, b, at, instant=False):
        j = D._id()
        g.append(f'<path id="{j}" d="{_arc(P[a], P[b])}" fill="none" stroke="#C4452F" stroke-width="4" stroke-dasharray="1" '
                 f'stroke-dashoffset="1" pathLength="1" stroke-linecap="round"/>')
        pins_js.append(f'tl.to("#{j}",{{strokeDashoffset:0,duration:{0.01 if instant else 1.6},ease:"power1.inOut"}},{at:.2f});')
        if not instant:
            D.sfx.append(("whoosh", at))

    for a, b in sc.get("drawn", []):
        route(a, b, 0.0, True)
    for p in sc.get("pins", []):
        pin(p["at"], p.get("label", ""), 0.0, True)

    def cam_to(key, zoom, at, d):
        x, y = P[key] if key else (W / 2, HH / 2)
        tx, ty = W / 2 - x * zoom, HH / 2 - y * zoom
        D.js.append(f'tl.to("#{cam}",{{x:{tx:.1f},y:{ty:.1f},scale:{zoom},duration:{d},ease:"power2.inOut"}},{at:.2f});')

    start = sc.get("start", {"goto": None, "zoom": 1})
    x, y = P[start["goto"]] if start.get("goto") else (W / 2, HH / 2)
    z = start.get("zoom", 1)
    D.js.append(f'tl.set("#{cam}",{{x:{W / 2 - x * z:.1f},y:{HH / 2 - y * z:.1f},scale:{z}}},0);')
    for b, (t0, d) in zip(sc["beats"], bt):
        if "goto" in b or "zoom" in b:
            cam_to(b.get("goto"), b.get("zoom", 1), t0 + 0.1, 1.8)
        if b.get("route"):
            route(*b["route"], t0 + 0.6)
        if b.get("pin"):
            pin(b["pin"]["at"], b["pin"].get("label", ""), t0 + (2.2 if b.get("route") else 0.8))
    g.append("</g>")
    D.svg.insert(0, "".join(g))
    D.js += pins_js
    D.label(sc.get("label", ""))
    if sc.get("title"):
        D.text(W / 2, 70, sc["title"], FT("title"), 54, D.ink, at=0.3)


# ---------------------------------------------------------------- 3) 키네틱 타이포
def s_kinetic(D, sc, bt, dur):
    """목소리가 말하는 순간 단어가 화면에 박힌다. 덩어리(한 줄) 단위로 위로 밀려 올라가며 바뀜. 강조 단어·숫자는 크게, 강조색."""
    from . import align
    pdir = Path(sc["_project_dir"])
    for k, (b, (t0, d)) in enumerate(zip(sc["beats"], bt)):
        wav = pdir / "03_voice" / f"hb_{sc['id']:03d}_{k}.wav"
        chunks = hybrid._chunks(b["say"], 16)
        words = [w for c in chunks for w in c.split(" ")]
        starts = hybrid._word_starts(wav, words, d) or [d * i / max(len(words), 1) for i in range(len(words))]
        hits = b.get("hit", [])
        wi = 0
        for ci, c in enumerate(chunks):
            ws = c.split(" ")
            gid = D._id()
            c_start = t0 + starts[wi]
            c_end = t0 + (starts[wi + len(ws)] if wi + len(ws) < len(starts) else d + 0.25)
            size = fit(FT("value"), c, 128, W - 240).size
            spans = []
            for j, w in enumerate(ws):
                big = any(h in w for h in hits) or bool(re.search(r"\d", w))
                col = D.red if big else D.ink
                sz = int(size * (1.25 if big else 1.0))
                sid = D._id()
                spans.append(f'<span id="{sid}" style="display:inline-block;opacity:0;color:{col};font-size:{sz}px;margin:0 .14em">{_e(w)}</span>')
                at = t0 + starts[wi + j]
                D.js.append(f'tl.fromTo("#{sid}",{{opacity:0,y:40,scale:{1.35 if big else 1.0}}},'
                            f'{{opacity:1,y:0,scale:1,duration:{0.22 if big else 0.16},ease:"back.out(2)"}},{at:.2f});')
                if big:
                    D.sfx.append(("pop", at))
            D.items.append(f'<div id="{gid}" style="position:absolute;left:120px;right:120px;top:{HH / 2 - 90:.0f}px;text-align:center;'
                           f'font-family:serif-x;line-height:1.1;white-space:nowrap">{"".join(spans)}</div>')
            if ci < len(chunks) - 1 or k < len(bt) - 1:   # 다음 덩어리가 오면 위로 밀려 흐려짐
                D.js.append(f'tl.to("#{gid}",{{y:-170,opacity:0.0,duration:0.3,ease:"power2.in"}},{max(c_end - 0.12, c_start + 0.3):.2f});')
            wi += len(ws)
        if b.get("note"):
            D.text(W / 2, HH / 2 + 170, b["note"], FT("note"), 46, "#5a5f6a", at=t0 + 0.6)
    D.label(sc.get("label", ""))


def register():
    hybrid.RENDER.update({"kb": s_kb, "card_type": s_card_type, "journey": s_journey, "kinetic": s_kinetic})
