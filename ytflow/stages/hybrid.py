"""하이브리드 스타일 렌더러: 식스시그마의 '원본 영상' + 머니크루의 '논리·인과' + 미주일기의 '종이·손그림'.

한 영상은 hybrid.json(장면 → 박자 beats)으로 씁니다. 박자마다 내레이션 한두 문장이 있고, 화면은 그 박자에 맞춰 움직입니다.
장면 종류(type)마다 화면이 다르고, 같은 종류가 연달아 나오지 않게 대본을 짭니다(prompts/script_hybrid.md).

  footage     원본 영상(전체 화면 또는 종이 위 사진처럼) + 이름 자막(lower third) + 복스식 주석(vox)
  chart       실제 시세 선 그래프 + 마지막 구간으로 카메라 확대 + 도장
  map_causal  영상 내내 자라는 '인과 지도'(노드·손그림 화살표). 지금 이야기하는 칸이 빨갛게
  usmap       손으로 그린 미국 지도 + 주 강조 + 숫자 카운터
  versus · bignum · funnel · apartments · parking · bars · timeline · checklist · compare · quote · analogy · chapter · outro

렌더: 장면마다 HyperFrames 프로젝트를 만들어 MP4 로 → 이어 붙이고 → 자막(아래)·효과음·마스터링(finish.py).
"""
from __future__ import annotations

import html as H
import json
import math
import os
import re
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from .. import config
from ..project import Project
from . import hyper, paper
from .paper import FT, fit
import numpy as np

W, HH = 1920, 1080
GAP = 0.28          # 박자 사이 쉼
LEAD = 0.35         # 장면 시작 후 첫 내레이션까지
TAIL = 0.55         # 마지막 박자 뒤 여유
FPS = 30


def _e(s) -> str:
    return H.escape(str(s))


# ---------------------------------------------------------------- 문서 (hyper.Doc 확장)
class HDoc(hyper.Doc):
    def __init__(self, seed: int):
        from . import skin as _skin
        self.skin = _skin.load()
        _skin.apply_fonts(self.skin)
        paper.OVERRIDE.clear()
        paper.OVERRIDE.update(_skin.paper_override(self.skin))
        super().__init__(seed)
        self.rough_hook = lambda o: _skin.rough_opts(self.skin, o)
        self.media, self.under = [], []   # 영상·사진 (svg 아래), 종이 카드 등 바닥 요소
        self.css = []
        self.sfx = []                     # (효과음 이름, 장면 안 시각)
        self.qa = []                      # 렌더 전 자체 점검 (선이 칸을 지남 등) → layout_qa.json
        self.blue = "#2F5D8C"
        self.yellow = "#F3D36B"

    # 영상 ------------------------------------------------------
    def video(self, src: str, dur: float, frame: str = "full", push: float = 0.06, at: float = 0.0):
        """frame=full: 화면 가득, 아래쪽 어둡게 / photo: 종이 위 흰 테두리 사진 + 테이프 + 살짝 기울임."""
        i = self._id()
        if frame == "photo":
            x, y, w, h, rot = 300, 120, 1320, 742, -1.6
            self.media.append(
                f'<div id="{i}f" style="position:absolute;left:{x - 18}px;top:{y - 18}px;width:{w + 36}px;height:{h + 36}px;'
                f'background:#FBF8F1;box-shadow:0 18px 40px rgba(0,0,0,.28);transform:rotate({rot}deg)"></div>'
                f'<div id="{i}w" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;overflow:hidden;transform:rotate({rot}deg)">'
                f'<video id="{i}" class="clip" src="assets/{src}" muted playsinline data-start="0" data-duration="{dur:.2f}" data-track-index="2" '
                f'style="width:100%;height:100%;object-fit:cover"></video></div>'
                f'<div style="position:absolute;left:{x + w / 2 - 90}px;top:{y - 40}px;width:180px;height:46px;background:rgba(236,220,170,.85);transform:rotate(3deg)"></div>')
            self.js.append(f'tl.fromTo("#{i}f,#{i}w",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.5,ease:"power2.out"}},{at:.2f});')
            self.js.append(f'tl.fromTo("#{i}",{{scale:1.0}},{{scale:{1 + push:.3f},duration:{dur:.2f},ease:"none"}},0);')
        else:
            self.media.append(
                f'<div id="{i}w" style="position:absolute;inset:0;overflow:hidden">'
                f'<video id="{i}" class="clip" src="assets/{src}" muted playsinline data-start="0" data-duration="{dur:.2f}" data-track-index="2" '
                f'style="width:100%;height:100%;object-fit:cover"></video></div>'
                f'<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.25) 0%,rgba(0,0,0,0) 22%,rgba(0,0,0,0) 62%,rgba(0,0,0,.55) 100%)"></div>'
                f'<div style="position:absolute;inset:0;box-shadow:inset 0 0 0 14px #EEE7DA, inset 0 0 0 16px rgba(0,0,0,.15)"></div>')
            self.js.append(f'tl.fromTo("#{i}",{{scale:1.0}},{{scale:{1 + push:.3f},duration:{dur:.2f},ease:"none"}},0);')
        return i

    # 이름 자막 (lower third) ------------------------------------
    def lower(self, name: str, role: str, at: float, dark: bool = False):
        from . import graphics
        if graphics.component(self, "lower") == "bar" and dark:   # 영상 위에서만 얇은 선 스타일 (종이 위는 띠 유지)
            return graphics.lower_bar(self, name, role, at)
        i = self._id()
        f = fit(FT("title"), name, 46, 900)
        w = max(f.getlength(name), fit(FT("label"), role, 26, 900).getlength(role)) + 80
        self.items.append(
            f'<div id="{i}" style="position:absolute;left:96px;top:760px;width:{w:.0f}px;height:118px;background:#FBF8F1;'
            f'box-shadow:0 8px 22px rgba(0,0,0,.25);transform-origin:left center">'
            f'<div style="position:absolute;left:0;top:0;width:10px;height:100%;background:{self.red}"></div>'
            f'<div style="position:absolute;left:34px;top:16px;font-family:serif-x;font-size:{f.size}px;color:{self.ink};white-space:nowrap">{_e(name)}</div>'
            f'<div style="position:absolute;left:36px;top:74px;font-family:sans;font-size:26px;color:#5a5f6a;white-space:nowrap">{_e(role)}</div></div>')
        self.js.append(f'tl.fromTo("#{i}",{{scaleX:0,opacity:0}},{{scaleX:1,opacity:1,duration:0.45,ease:"power3.out"}},{at:.2f});')
        self.sfx.append(("click-soft", at))

    # 복스식 주석: 종이 쪽지 + 형광펜 + 연결선 + 펜 메모 -------------
    def vox(self, text: str, note: str, at: float, x: float = 1060, y: float = 150, on_paper: bool = False):
        i = self._id()
        f = fit(FT("title"), text, 56, 700)
        w = f.getlength(text) + 70
        x = min(x, 1860 - w)  # 화면 오른쪽 밖으로 나가지 않게
        self.items.append(
            f'<div id="{i}" style="position:absolute;left:{x:.0f}px;top:{y:.0f}px;width:{w:.0f}px;height:110px;background:#FBF8F1;'
            f'box-shadow:0 10px 26px rgba(0,0,0,.3);transform:rotate(-1.2deg)">'
            f'<div id="{i}m" style="position:absolute;left:28px;top:58px;width:{w - 56:.0f}px;height:30px;background:{self.yellow};opacity:.8;transform-origin:left center"></div>'
            f'<div style="position:absolute;left:35px;top:18px;font-family:serif-x;font-size:{f.size}px;color:{self.ink};white-space:nowrap">{_e(text)}</div></div>')
        self.js.append(f'tl.fromTo("#{i}",{{opacity:0,y:-24,rotation:-5}},{{opacity:1,y:0,rotation:-1.2,duration:0.5,ease:"back.out(1.6)"}},{at:.2f});')
        self.js.append(f'tl.fromTo("#{i}m",{{scaleX:0}},{{scaleX:1,duration:0.5,ease:"power1.inOut"}},{at + 0.45:.2f});')
        if note:
            nx, ny = x + w - 40, y + 150
            self.rough("line", [nx - 20, y + 108, nx + 10, ny - 10], self.yellow, 3.5, at=at + 0.8, dur=0.25, roughness=0.8)
            nf = fit(FT("note"), note, 40, 760)
            nleft = min(nx - 40, 1870 - nf.getlength(note))  # 메모도 화면 안에
            # 영상 위면 밝은 글씨+그림자, 종이 위(사진 틀 밖)면 잉크색 (대비 3:1 이상)
            ncol, nsh = (self.red, "background:rgba(251,248,241,.92);padding:2px 12px;border-radius:6px;") if on_paper \
                else ("#FFF3C4", "background:rgba(20,20,20,.55);padding:2px 12px;border-radius:6px;text-shadow:0 2px 6px rgba(0,0,0,.8);")
            j = self._id()
            self.items.append(f'<div id="{j}" style="position:absolute;left:{nleft:.0f}px;top:{ny:.0f}px;font-family:pen;font-size:{nf.size}px;'
                              f'color:{ncol};{nsh}white-space:nowrap">{_e(note)}</div>')
            self.js.append(f'tl.fromTo("#{j}",{{opacity:0,y:8}},{{opacity:1,y:0,duration:0.35}},{at + 1.0:.2f});')
        self.sfx.append(("pencil", at + 0.45))

    # 도장 ------------------------------------------------------
    def stamp(self, text: str, x: float, y: float, at: float, rot: float = -8):
        i = self._id()
        f = fit(FT("title"), text, 64, 640)
        w, h = f.getlength(text) + 80, 120
        self.items.append(
            f'<div id="{i}" style="position:absolute;left:{x - w / 2:.0f}px;top:{y - h / 2:.0f}px;width:{w:.0f}px;height:{h}px;'
            f'border:7px double {self.red};border-radius:10px;color:{self.red};font-family:serif-x;font-size:{f.size}px;'
            f'display:flex;align-items:center;justify-content:center;transform:rotate({rot}deg);background:rgba(251,248,241,.72)">{_e(text)}</div>')
        self.js.append(f'tl.fromTo("#{i}",{{opacity:0,scale:1.8}},{{opacity:1,scale:1,duration:0.28,ease:"power4.in"}},{at:.2f});')
        self.sfx.append(("impact-bass-1", at + 0.25))

    def label(self, text: str, dark: bool = False):
        if not text:
            return
        i = self._id()
        col = "#FFFFFF" if dark else "#5a5f6a"
        bg = "rgba(0,0,0,.45)" if dark else "rgba(251,248,241,.85)"
        self.items.append(f'<div id="{i}" style="position:absolute;right:56px;top:40px;padding:6px 14px;background:{bg};border-radius:6px;'
                          f'font-family:sans;font-size:24px;color:{col};white-space:nowrap">{_e(text)}</div>')
        self.js.append(f'tl.fromTo("#{i}",{{opacity:0}},{{opacity:1,duration:0.4}},0.2);')

    def chapter_tag(self, num: str, title: str, dark: bool = False):
        if not num:
            return
        i = self._id()
        col = "#FFFFFF" if dark else self.ink
        acc = (self.skin.get("palette") or {}).get("accent", "#C4452F").lstrip("#")
        lum = sum(int(acc[k:k + 2], 16) * w for k, w in ((0, .299), (2, .587), (4, .114)))
        on_acc = "#111111" if lum > 150 else "#fff"   # 밝은 강조색(청사진의 노랑) 위에는 검은 글자
        back = "background:rgba(12,12,14,.55);padding:4px 14px 4px 4px;border-radius:6px;" if dark else ""   # 밝은 영상 위에서도 읽히게
        self.items.append(f'<div id="{i}" style="position:absolute;left:56px;top:38px;font-family:sans-x;font-size:26px;color:{col};white-space:nowrap;{back}">'
                          f'<span style="background:{self.red};color:{on_acc};padding:2px 12px;border-radius:4px;margin-right:12px">{_e(num)}</span>{_e(title)}</div>')
        self.js.append(f'tl.fromTo("#{i}",{{opacity:0,x:-20}},{{opacity:1,x:0,duration:0.4}},0.15);')

    def h1(self, title: str, at: float = 0.2, y: float = 150, size: int = 62):
        if not title:
            return
        f = fit(FT("title"), title, size, W - 360)
        self.text(W / 2, y, title, FT("title"), f.size, self.ink, at=at)
        w = f.getlength(title)
        self.rough("line", [W / 2 - w / 2, y + size * 0.72, W / 2 + w / 2, y + size * 0.72 + 3], self.red, 3.5, at=at + 0.3, dur=0.35, roughness=1.0)

    def html(self, duration: float, bg_name: str) -> str:
        base = super().html(duration, bg_name)
        media = "".join(self.media)
        base = base.replace('<div id="layer"', media + '<div id="layer"', 1)
        if getattr(self, "top", None):   # 겹치기(layers)의 영상 액자: 렌더러가 찾도록 #layer 밖, 그 위에
            base = base.replace("\n</div></div>\n<script>", "\n</div>" + "".join(self.top) + "</div>\n<script>", 1)
        base = base.replace("</style>", "".join(self.css) + f"video{{filter:{_skin_mod().video_filter(self.skin) or 'none'}}}</style>", 1)
        return _skin_mod().remap_html(base, self.skin)   # 기본 토큰 색 → 고른 스킨의 색


def _skin_mod():
    from . import skin
    return skin


# ---------------------------------------------------------------- 장면별 화면
def s_footage(D: HDoc, sc: dict, bt: list, dur: float):
    clip = sc["clip"]
    full = clip.get("frame", "full") == "full"
    D.video(sc["_clipfile"], dur, clip.get("frame", "full"))
    D.label(sc.get("label", ""), dark=full)
    D.chapter_tag(sc.get("_chnum", ""), sc.get("_chtitle", ""), dark=full)
    for b, (t0, d) in zip(sc["beats"], bt):
        if b.get("lower"):
            D.lower(b["lower"]["name"], b["lower"]["role"], t0 + 0.2, dark=full)
        if b.get("vox"):
            D.vox(b["vox"]["text"], b["vox"].get("note", ""), t0 + 0.4, x=1000 if full else 1120, y=140 if full else 110, on_paper=not full)


def s_chart(D: HDoc, sc: dict, bt: list, dur: float):
    from . import marketdata
    rows = marketdata.fetch(sc["ticker"], sc.get("period", "3mo"), sc["_prices"])
    last = rows[-1]["date"] if rows else ""
    rows = rows + [r for r in sc.get("append", []) if r["date"] > last]  # 시세 원본에 아직 없는 확정 종가(출처는 label 에)
    rows = rows[-60:]
    D.label(sc.get("label", ""))
    D.h1(sc.get("title", ""), y=130)
    x0, x1, y0, y1 = 200, 1560, 250, 760
    lo, hi = min(r["close"] for r in rows), max(r["close"] for r in rows)
    pad = (hi - lo) * 0.12
    lo, hi = lo - pad, hi + pad
    X = lambda i: x0 + (x1 - x0) * i / (len(rows) - 1)
    Y = lambda v: y1 - (y1 - y0) * (v - lo) / (hi - lo)
    for k in range(5):  # 가격 눈금
        v = lo + (hi - lo) * k / 4
        yy = Y(v)
        D.svg.append(f'<line x1="{x0}" y1="{yy:.0f}" x2="{x1}" y2="{yy:.0f}" stroke="#c9c0ae" stroke-width="1.5" stroke-dasharray="6 8"/>')
        D.items.append(f'<div style="position:absolute;left:{x1 + 20}px;top:{yy - 16:.0f}px;font-family:sans;font-size:24px;color:#6b6f78">{v:,.0f}</div>')
    pts = [(X(i), Y(r["close"])) for i, r in enumerate(rows)]
    D.stroke(pts, D.ink, 4, at=0.3, dur=1.4)
    for lab, idx in ((rows[0]["date"][2:].replace("-", "."), 0), (rows[-1]["date"][2:].replace("-", "."), len(rows) - 1)):
        D.items.append(f'<div style="position:absolute;left:{X(idx) - 60:.0f}px;top:{y1 + 18}px;font-family:sans;font-size:24px;color:#6b6f78">{lab}</div>')
    # 마지막 이틀 강조 + 카메라 확대
    b0 = sc["beats"][0]
    n = b0.get("focus_last", 3)
    seg = pts[-n:]
    t0 = bt[0][0]
    D.stroke(seg, D.red, 8, at=t0 + 1.2, dur=0.6)
    D.circle(seg[-1][0], seg[-1][1], 26, 26, at=t0 + 1.7)
    D.text(seg[-1][0] - 20, seg[-1][1] + 70, f"{rows[-1]['close']:,.0f}", FT("value"), 54, D.red, at=t0 + 1.9, anchor="rm")
    if b0.get("mark"):
        D.text(seg[0][0] - 30, min(p[1] for p in seg) - 70, b0["mark"], FT("note"), 50, D.red, at=t0 + 2.2, anchor="rm")
    D.js.append(f'tl.to("#layer",{{scale:1.18,x:-230,y:40,duration:1.6,ease:"power2.inOut"}},{t0 + 1.0:.2f});')
    D.sfx.append(("pencil", t0 + 1.2))
    if len(sc["beats"]) > 1 and sc["beats"][1].get("stamp"):
        D.js.append(f'tl.to("#layer",{{scale:1,x:0,y:0,duration:0.8,ease:"power2.inOut"}},{bt[1][0] - 0.2:.2f});')
        D.stamp(sc["beats"][1]["stamp"], 820, 520, bt[1][0] + 0.7)


def s_versus(D: HDoc, sc: dict, bt: list, dur: float):
    D.label(sc.get("label", ""))
    D.chapter_tag(sc.get("_chnum", ""), sc.get("_chtitle", ""))
    L, R = sc["left"], sc["right"]
    t0 = bt[0][0]
    for x, it, col, at in ((W * 0.28, L, D.ink, t0 + 0.2), (W * 0.72, R, D.red, t0 + 1.4)):
        D.icon(it["icon"], x, 300, 120, col, at=at)
        D.text(x, 520, it["value"], FT("value"), 210, col, at=at + 0.2, counter=True)
        D.text(x, 680, it["label"], FT("label"), 40, "#5a5f6a", at=at + 0.4)
    D.text(W / 2, 520, "vs", FT("note"), 90, D.muted, at=t0 + 1.2)
    if len(bt) > 1:
        t1 = bt[1][0]
        D.circle(W * 0.72, 520, 210, 130, at=t1 + 0.3)
        q = sc["beats"][1].get("question", "")
        if q:
            D.text(W / 2, 830, q, FT("title"), 64, D.ink, at=t1 + 1.0)
            D.sfx.append(("pop", t1 + 1.0))


def s_chapter(D: HDoc, sc: dict, bt: list, dur: float):
    # 종이 한 장이 오른쪽에서 밀려 들어오며 장 제목 (그래픽 팩 chapter: paper). 'type' 이면 큰 글씨 판.
    from . import graphics
    if graphics.component(D, "chapter", sc) == "type":
        return graphics.chapter_type(D, sc)
    i = D._id()
    D.media.append(f'<div id="{i}" style="position:absolute;inset:0;background:#2b2f3a"></div>')
    j = D._id()
    D.media.append(f'<img id="{j}" src="assets/{getattr(D, 'bg_name', 'paper.jpg')}" style="position:absolute;left:0;top:0;width:{W}px;height:{HH}px;box-shadow:-30px 0 60px rgba(0,0,0,.45)">')
    D.js.append(f'tl.fromTo("#{j}",{{x:{W},rotation:4}},{{x:0,rotation:0,duration:0.7,ease:"power3.out"}},0);')
    D.sfx.append(("whoosh", 0.0))
    D.icon(sc.get("icon", ""), W / 2, 330, 110, D.red, at=0.6)
    D.text(W / 2, 470, f"{sc.get('num', '')}", FT("value"), 120, D.red, at=0.7)
    f = fit(FT("title"), sc["title"], 92, W - 300)
    D.text(W / 2, 640, sc["title"], FT("title"), f.size, D.ink, at=0.9)
    w = f.getlength(sc["title"])
    D.rough("line", [W / 2 - w / 2, 710, W / 2 + w / 2, 714], D.red, 4.5, at=1.3, dur=0.45)


def _node_box(D: HDoc, key: str, nd: dict, state: str, at: float, instant: bool):
    """인과 지도 칸: state = dim | on | active"""
    x, y = nd["x"], nd["y"]
    bw, bh = BW, BH
    col = D.red if state == "active" else (D.ink if state == "on" else "#a8a29a")
    fill = "rgba(196,69,47,0.22)" if state == "active" else None
    d = 0.01 if instant else 0.45
    from . import graphics
    graphics.node(D, x, y, bw, bh, col, state, at, d)   # 칸 모양은 그래픽 팩(flow: box·pill·sticky·circle)
    D.icon(nd.get("icon", ""), x, y - 30, 48, col, at=at if instant else at + 0.15, gap=0.0)
    D.text(x, y + 34, nd["label"], FT("box"), fit(FT("box"), nd["label"], 34, bw - 30).size, col,
           at=at if instant else at + 0.2, gap=0.0, dur=0.01 if instant else 0.4)


BW, BH = 330, 150   # 인과 지도 칸 크기


def _hits(seg, rect) -> bool:
    """수평·수직·사선 선분이 사각형(여유 포함)을 지나가나."""
    (x0, y0), (x1, y1) = seg
    l, t, r, b = rect
    for k in range(0, 41):
        x, y = x0 + (x1 - x0) * k / 40, y0 + (y1 - y0) * k / 40
        if l < x < r and t < y < b:
            return True
    return False


def _route(a: dict, b: dict, others: list) -> tuple[list, bool]:
    """a 칸 → b 칸 화살표 경로. 다른 칸을 지나지 않는 첫 후보를 고른다 (직선 → ㄱ자 → 줄 사이 빈 띠로 돌아가기)."""
    ax, ay, bx, by = a["x"], a["y"], b["x"], b["y"]
    hw, hh, m = BW / 2, BH / 2, 12
    rects = [(o["x"] - hw - m, o["y"] - hh - m, o["x"] + hw + m, o["y"] + hh + m) for o in others]
    sx = 1 if bx > ax else -1
    sy = 1 if by > ay else -1
    cands = []
    if ay == by:
        cands.append([(ax + sx * hw, ay), (bx - sx * hw, by)])
    if ax == bx:
        cands.append([(ax, ay + sy * hh), (bx, by - sy * hh)])
    if ax != bx and ay != by:
        cands.append([(ax + sx * hw, ay), (bx, ay), (bx, by - sy * hh)])          # 옆으로 나가 꺾어 내려가기
        cands.append([(ax, ay + sy * hh), (ax, by), (bx - sx * hw, by)])          # 아래로 나가 꺾어 옆으로
        cands.append([(ax + sx * hw, ay), (bx - sx * hw, by)])                    # 사선
    # 줄 사이 빈 띠(두 줄 칸 사이)로 돌아가기
    lanes = sorted({(ay + by) / 2, ay + sy * (hh + 70), ay - sy * (hh + 70), by + (hh + 70), by - (hh + 70)},
                   key=lambda v: abs(v - (ay + by) / 2))
    for ly in lanes:
        pa = (ax, ay + (hh if ly > ay else -hh))
        pb = (bx, by + (hh if ly > by else -hh))
        cands.append([pa, (ax, ly), (bx, ly), pb])
    for c in cands:
        segs = list(zip(c[:-1], c[1:]))
        if not any(_hits(sg, r) for sg in segs for r in rects):
            return c, True
    return cands[0], False


def _edge(D: HDoc, a: dict, b: dict, at: float, instant: bool, col: str, others: list | None = None):
    pts, ok = _route(a, b, others or [])
    if not ok:
        D.qa.append(f"인과 지도: '{a['label']}' → '{b['label']}' 화살표가 다른 칸을 지납니다 (칸 위치를 옮기세요)")
    d_body, d_head = (0.01, 0.01) if instant else (0.35 + 0.1 * (len(pts) - 2), 0.15)
    D.rough("linearPath", [[list(p) for p in pts]], col, 3.5, at=at, dur=d_body, roughness=0.9)
    (x0, y0), (x1, y1) = pts[-2], pts[-1]
    ang = math.atan2(y1 - y0, x1 - x0)
    head = [[x1 - 22 * math.cos(ang - 0.45), y1 - 22 * math.sin(ang - 0.45)], [x1, y1],
            [x1 - 22 * math.cos(ang + 0.45), y1 - 22 * math.sin(ang + 0.45)]]
    D.rough("linearPath", [head], col, 3.5, at=at + d_body, dur=d_head, roughness=0.5)


def s_map_causal(D: HDoc, sc: dict, bt: list, dur: float):
    mp = sc["_map"]
    D.label(sc.get("label", ""))
    D.chapter_tag(sc.get("_chnum", ""), sc.get("_chtitle", ""))
    D.h1(sc.get("title", ""), y=150, size=58)
    shown, drawn = [], set()
    # 장면 시작 때 이미 있던 것: 첫 박자의 instant
    first = sc["beats"][0]
    for k in first.get("reveal", []) if first.get("instant") else []:
        pass
    active = None
    for bi, (b, (t0, d)) in enumerate(zip(sc["beats"], bt)):
        newly = [k for k in b.get("reveal", []) if k not in shown]
        inst = set(n for e in b.get("instant", []) for n in e)
        for k_i, k in enumerate(newly):
            instant = k in inst
            _node_box(D, k, mp["nodes"][k], "on", 0.3 if instant else t0 + 0.25 * k_i, instant)
            shown.append(k)
        for e in b.get("instant", []):
            if tuple(e) not in drawn:
                _edge(D, mp["nodes"][e[0]], mp["nodes"][e[1]], 0.35, True, D.ink, [v for k2, v in mp["nodes"].items() if k2 not in e])
                drawn.add(tuple(e))
        for e_i, e in enumerate(b.get("draw", [])):
            if tuple(e) not in drawn:
                _edge(D, mp["nodes"][e[0]], mp["nodes"][e[1]], t0 + 0.6 + 0.55 * e_i, False, D.red if b.get("active") == e[1] else D.ink,
                      [v for k2, v in mp["nodes"].items() if k2 not in e])
                drawn.add(tuple(e))
                D.sfx.append(("pencil", t0 + 0.6 + 0.55 * e_i))
        if b.get("active") and b["active"] != active:
            k = b["active"]
            nd = mp["nodes"][k]
            _node_box(D, k, nd, "active", t0 + 0.9, False)
            active = k
        if b.get("tag"):
            nd = mp["nodes"][b["tag"]["node"]]
            ty = nd["y"] + 120 if nd["y"] < 600 else nd["y"] - 125
            D.marker(nd["x"] - 170, ty, 340, 46, at=t0 + 1.0)
            D.text(nd["x"], ty, b["tag"]["text"], FT("note"), fit(FT("note"), b["tag"]["text"], 40, 360).size, D.red, at=t0 + 1.1)


def s_usmap(D: HDoc, sc: dict, bt: list, dur: float):
    states = sc["_states"]
    D.label(sc.get("label", ""))
    D.chapter_tag(sc.get("_chnum", ""), sc.get("_chtitle", ""))
    D.h1(sc.get("title", ""), y=120, size=56)
    ox, oy, s = 210, 210, 0.82
    g = D._id()
    paths = "".join(f'<path class="{g}" d="{v["d"]}" fill="none" stroke="#7d7568" stroke-width="2.2" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>'
                    for k, v in states.items())
    D.svg.append(f'<g transform="translate({ox},{oy}) scale({s})">{paths}</g>')
    D.js.append(f'tl.to(".{g}",{{strokeDashoffset:0,duration:0.9,ease:"power1.inOut",stagger:0.012}},0.2);')
    D.sfx.append(("pencil", 0.3))
    for b, (t0, d) in zip(sc["beats"], bt):
        for st in b.get("highlight", []):
            v = states[st]
            h = D._id()
            D.svg.append(f'<g transform="translate({ox},{oy}) scale({s})"><path id="{h}" d="{v["d"]}" fill="{D.red}" fill-opacity="0.55" stroke="{D.red}" stroke-width="4"/></g>')
            D.js.append(f'tl.fromTo("#{h}",{{opacity:0}},{{opacity:1,duration:0.5}},{t0 + 0.4:.2f});')
        if b.get("note"):
            v = states[b["note"]["state"]]
            cx, cy = ox + v["c"][0] * s, oy + v["c"][1] * s
            tx, ty = cx - 60, cy + 190  # 주 아래쪽 (오른쪽 숫자와 겹치지 않게)
            D.rough("line", [tx + 20, ty - 40, cx, cy + 14], D.red, 3.5, at=t0 + 0.7, dur=0.35)
            D.text(tx, ty, b["note"]["text"], FT("note"), 50, D.red, at=t0 + 0.9)
        if b.get("counter"):
            c = b["counter"]
            D.text(1640, 330, f'{c["value"]}{c.get("suffix", "")}', FT("value"), 150, D.ink, at=t0 + 0.3, counter=True)
            D.text(1640, 450, c.get("label", ""), FT("label"), 38, "#5a5f6a", at=t0 + 0.5)
        if b.get("counter2"):
            c = b["counter2"]
            D.marker(1460, 590, 360, 70, at=t0 + 0.3)
            D.text(1640, 590, f'{c["value"]} / {c["of"]}', FT("value"), 88, D.red, at=t0 + 0.4, counter=True)
            D.text(1640, 680, c.get("label", ""), FT("label"), 38, D.red, at=t0 + 0.6)
            D.sfx.append(("pop", t0 + 0.5))


def s_quote(D: HDoc, sc: dict, bt: list, dur: float):
    D.label(sc.get("label", ""))
    D.chapter_tag(sc.get("_chnum", ""), sc.get("_chtitle", ""))
    i = D._id()
    D.under.append(i)
    D.items.append(f'<div id="{i}" style="position:absolute;left:250px;top:200px;width:1420px;height:540px;background:#FBF8F1;'
                   f'box-shadow:0 14px 34px rgba(0,0,0,.2);transform:rotate(-0.8deg)"></div>')
    D.js.append(f'tl.fromTo("#{i}",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.5}},0.15);')
    D.text(330, 290, "“", FT("value"), 160, D.red, at=0.4, anchor="lm")
    q = sc["quote"]
    lines, cur = [], ""
    for wd in q.split(" "):
        if len((cur + " " + wd).strip()) > 22:
            lines.append(cur.strip())
            cur = wd
        else:
            cur += " " + wd
    lines.append(cur.strip())
    size = 58 if len(lines) <= 3 else 50
    t0 = bt[0][0]
    kw = sc.get("keyword", "")
    for k, ln in enumerate(lines[:5]):
        y = 360 + k * (size + 30)
        D.text(400, y, ln, FT("title"), size, D.ink, at=t0 + 0.3 + k * 0.5, anchor="lm")
        if kw and kw in ln:
            f = paper.F(FT("title"), size)
            pre = f.getlength(ln[:ln.index(kw)])
            mk_at = bt[-1][0] + 0.3 if any(b.get("mark") for b in sc["beats"]) else t0 + 1.6
            card_ix = next(n for n, it in enumerate(D.items) if f'id="{i}"' in it)  # 카드 바로 위, 글자 아래
            D.marker(400 + pre - 6, y + size * 0.18, f.getlength(kw) + 12, size * 0.55, at=mk_at, index=card_ix + 1)
            if sc.get("note"):
                ny = 360 + min(len(lines), 5) * (size + 30) + 6  # 인용문 마지막 줄 아래 (다음 줄과 겹치지 않게)
                D.text(min(400 + pre, 1500 - paper.F(FT("note"), 42).getlength(sc["note"])), ny, "↳ " + sc["note"], FT("note"), 42, D.red, at=mk_at + 0.4, anchor="lm")
            D.sfx.append(("pencil", mk_at))
    D.lower(sc.get("who", ""), sc.get("role", ""), t0 + 0.6)


def s_checklist(D: HDoc, sc: dict, bt: list, dur: float):
    D.label(sc.get("label", ""))
    D.chapter_tag(sc.get("_chnum", ""), sc.get("_chtitle", ""))
    D.h1(sc.get("title", ""), y=150)
    rows = sc["rows"]
    y0, rh = 310, 125
    shown = 0
    for b, (t0, d) in zip(sc["beats"], bt):
        upto = b.get("upto", len(rows))
        for r_i in range(shown, upto):
            r = rows[r_i]
            y = y0 + r_i * rh
            at = t0 + 0.3 + (r_i - shown) * 0.9
            D.rough("rectangle", [380, y - 30, 60, 60], D.ink, 3, at=at, dur=0.3)
            D.text(480, y, r["label"], FT("box"), fit(FT("box"), r["label"], 46, 1000).size, D.ink, at=at + 0.1, anchor="lm")
            st = r.get("state")
            if st == "yes":
                D.rough("linearPath", [[[390, y], [405, y + 20], [436, y - 26]]], "#2E7D4F", 6, at=at + 0.45, dur=0.3)
            elif st == "no":
                D.rough("line", [388, y - 22, 432, y + 22], D.red, 6, at=at + 0.45, dur=0.15)
                D.rough("line", [432, y - 22, 388, y + 22], D.red, 6, at=at + 0.6, dur=0.15)
            elif st == "date":
                D.text(1500, y, r.get("value", ""), FT("value"), 52, D.red, at=at + 0.45, anchor="lm")
            elif st == "warn":
                D.icon("triangle-alert", 410, y, 44, "#C77B12", at=at + 0.4)
            D.sfx.append(("pencil", at))
        shown = upto
        if b.get("stamp"):
            D.stamp(b["stamp"], 1450, 720, t0 + d - 1.2)


def s_analogy(D: HDoc, sc: dict, bt: list, dur: float):
    D.label(sc.get("label", ""))
    D.chapter_tag(sc.get("_chnum", ""), sc.get("_chtitle", ""))
    D.h1(sc.get("title", ""), y=140)
    L, R = sc["left"], sc["right"]
    t0 = bt[0][0]
    for x, it, col, at in ((W * 0.3, L, D.ink, t0 + 0.2), (W * 0.7, R, D.red, t0 + 1.4)):
        D.rough("rectangle", [x - 230, 260, 460, 340], col, 3, at=at, dur=0.4)
        D.icon(it["icon"], x, 370, 130, col, at=at + 0.2)
        D.text(x, 500, it["label"], FT("title"), 58, col, at=at + 0.3)
        D.text(x, 560, it["sub"], FT("note"), 44, "#5a5f6a", at=at + 0.4)
    D.text(W / 2, 430, "≈", FT("value"), 120, D.red, at=t0 + 1.2)
    if len(bt) > 1 and sc.get("result"):
        t1 = bt[1][0]
        D.arrow(W * 0.5, 620, W * 0.5, 740, D.ink, at=t1 - 1.0)
        D.icon(sc["result"]["icon"], W / 2 - 260, 800, 64, D.red, at=t1 - 0.6)
        D.text(W / 2 - 200, 800, sc["result"]["label"], FT("box"), 46, D.red, at=t1 - 0.5, anchor="lm")


def s_funnel(D: HDoc, sc: dict, bt: list, dur: float):
    D.label(sc.get("label", ""))
    D.chapter_tag(sc.get("_chnum", ""), sc.get("_chtitle", ""))
    D.h1(sc.get("title", ""), y=140)
    bars = sc["bars"]
    top = max(b["value"] for b in bars)
    x0, wmax = 560, 860
    shown = 0
    for b, (t0, d) in zip(sc["beats"], bt):
        upto = b.get("upto", len(bars))
        for k in range(shown, upto):
            it = bars[k]
            y = 300 + k * 190
            w = wmax * it["value"] / top
            col = D.red if it.get("highlight") else D.ink
            at = t0 + 0.3
            D.text(x0 - 30, y, it["label"], FT("box"), 40, D.ink, at=at, anchor="rm")
            D.rough("rectangle", [x0, y - 50, max(w, 20), 100], col, 2.5, fill=col, at=at + 0.2, dur=0.9)
            D.text(x0 + max(w, 20) + 26, y - 12, f'{it["value"]}{sc.get("unit", "")}', FT("value"), 64, col, at=at + 0.8, anchor="lm", counter=True)
            D.text(x0 + max(w, 20) + 28, y + 42, it.get("sub", ""), FT("note"), 38, "#5a5f6a", at=at + 1.0, anchor="lm")
            D.sfx.append(("pencil", at + 0.2))
            if it.get("highlight"):
                D.circle(x0 + max(w, 20) + 120, y - 10, 140, 70, at=at + 1.5)
        shown = upto


def s_apartments(D: HDoc, sc: dict, bt: list, dur: float):
    D.label(sc.get("label", ""))
    D.chapter_tag(sc.get("_chnum", ""), sc.get("_chtitle", ""))
    D.h1(sc.get("title", ""), y=140)
    total, waiting, cancel = sc["total"], sc["waiting"], sc["cancel"]
    cols = 20
    cw, ch, gx, gy = 50, 54, 14, 12
    x0 = (W - cols * (cw + gx)) / 2
    y0 = 250
    g = D._id()
    rects = []
    for k in range(total):
        r_, c_ = divmod(k, cols)
        x, y = x0 + c_ * (cw + gx), y0 + r_ * (ch + gy)
        cls = "w" if k >= total - waiting else "n"
        cls2 = " x" if k >= total - cancel else ""
        rects.append(f'<rect class="{g} {g}{cls}{" " + g + "x" if cls2 else ""}" x="{x:.0f}" y="{y:.0f}" width="{cw}" height="{ch}" rx="3" '
                     f'fill="#FBF8F1" stroke="{D.ink}" stroke-width="2.5"/>'
                     f'<rect class="{g}win" x="{x + 14:.0f}" y="{y + 14:.0f}" width="{cw - 28}" height="{ch - 30}" fill="none" stroke="#9a9488" stroke-width="1.5"/>')
    D.svg.append("".join(rects))
    t0 = bt[0][0]
    D.js.append(f'tl.fromTo(".{g},.{g}win",{{opacity:0,y:12}},{{opacity:1,y:0,duration:0.25,stagger:0.006}},{t0 + 0.2:.2f});')
    D.text(W / 2, 830, f"{total}개 동 = 계획 전체 148GW", FT("note"), 44, D.ink, at=t0 + 1.0)
    if len(bt) > 1:
        t1 = bt[1][0]
        D.js.append(f'tl.to(".{g}w",{{fill:"{D.yellow}",duration:0.25,stagger:0.01}},{t1 + 0.2:.2f});')
        D.js.append(f'tl.to(".{g}x",{{fill:"{D.red}",stroke:"{D.red}",duration:0.25,stagger:0.05}},{t1 + 2.2:.2f});')
        D.marker(500, 890, 340, 46, at=t1 + 0.6)
        D.text(670, 890, "허가 대기 60개 동", FT("note"), 42, D.ink, at=t1 + 0.7)
        D.text(1250, 890, "최악이면 취소 12개 동", FT("note"), 42, D.red, at=t1 + 2.4)
        D.sfx.append(("pop", t1 + 2.3))


def s_timeline(D: HDoc, sc: dict, bt: list, dur: float):
    D.label(sc.get("label", ""))
    D.chapter_tag(sc.get("_chnum", ""), sc.get("_chtitle", ""))
    D.h1(sc.get("title", ""), y=140)
    ys = sc["years"]
    x0, x1, y = 230, 1690, 560
    X = {v: x0 + (x1 - x0) * k / (len(ys) - 1) for k, v in enumerate(ys)}
    D.rough("line", [x0 - 40, y, x1 + 60, y], D.ink, 4, at=0.3, dur=0.6)
    for v, x in X.items():
        D.rough("line", [x, y - 18, x, y + 18], D.ink, 3, at=0.5, dur=0.1, gap=0.0)
        D.text(x, y + 60, v, FT("value"), 46, D.ink, at=0.55, gap=0.0)
    shown = 0
    items = sc.get("spans") or sc.get("events") or []
    for b, (t0, d) in zip(sc["beats"], bt):
        upto = b.get("upto", len(items))
        for k in range(shown, upto):
            it = items[k]
            at = t0 + 0.3 + (k - shown) * 1.0
            if "from" in it:
                xa, xb = X[it["from"]] - 70, X[it["to"]] + 70
                col = D.red if it.get("tone") == "risk" else "#2E7D4F"
                D.rough("rectangle", [xa, y - 150, xb - xa, 110], col, 3, fill=col, at=at, dur=0.8)
                D.text((xa + xb) / 2, y - 200, it["label"], FT("box"), fit(FT("box"), it["label"], 42, max(xb - xa, 300)).size, col, at=at + 0.5)
            else:
                x = X[it["at"]]
                yy = y - 140 - (k % 2) * 140
                D.icon("calendar", x, yy - 70, 52, D.red, at=at)
                D.text(x, yy, it["label"], FT("box"), fit(FT("box"), it["label"], 38, 520).size, D.ink, at=at + 0.15)
                D.text(x, yy + 48, it.get("sub", ""), FT("note"), 34, "#5a5f6a", at=at + 0.3)
                D.rough("line", [x, yy + 75, x, y - 22], D.red, 2.5, at=at + 0.2, dur=0.25)
            D.sfx.append(("pencil", at))
        shown = upto


def s_bars(D: HDoc, sc: dict, bt: list, dur: float):
    D.label(sc.get("label", ""))
    D.chapter_tag(sc.get("_chnum", ""), sc.get("_chtitle", ""))
    D.h1(sc.get("title", ""), y=140)
    items = sc["items"]
    top = max(i["value"] for i in items)
    t1 = bt[-1][0]
    em = sc.get("emph", 0)   # 강조(강조색) 항목 번호 — 순서는 대본 그대로
    n = len(items)
    step = 440 if n <= 3 else 1180 / (n - 1)       # 4개 이상이면 화면 안에 고르게 (예전 2~3개 배치는 그대로)
    bw = 220 if n <= 3 else min(220, step * 0.55)
    stagger = 1.3 if n <= 3 else 0.7
    vsize = 72 if n <= 3 else 60
    for k, it in enumerate(items):
        x = 520 + k * 440 if n <= 3 else 960 + (k - (n - 1) / 2) * step
        h = 480 * it["value"] / top
        at = t1 + 0.2 + k * stagger
        c = D.red if k == em else D.ink
        D.rough("rectangle", [x - bw / 2, 820 - h, bw, h], c, 2.5, fill=c, at=at, dur=0.8)
        D.text(x, 820 - h - 50, f'{it.get("text", it["value"])}', FT("value"), vsize, c, at=at + 0.5, counter=True)
        D.text(x, 870, it["label"], FT("box"), fit(FT("box"), it["label"], 44, step - 20 if n > 3 else 400).size, D.ink, at=at)
        D.sfx.append(("pencil", at))
    D.text(1640, 870 - 600, sc.get("unit", ""), FT("note"), 40, "#5a5f6a", at=t1)
    D.rough("line", [330, 822, 1600, 824], D.ink, 3.5, at=bt[0][0] + 0.3, dur=0.6)


def s_bignum(D: HDoc, sc: dict, bt: list, dur: float):
    D.label(sc.get("label", ""))
    D.chapter_tag(sc.get("_chnum", ""), sc.get("_chtitle", ""))
    t0 = bt[0][0]
    D.text(W / 2, 300, sc.get("small", ""), FT("label"), 44, "#5a5f6a", at=t0 + 0.2)
    D.text(W / 2, 480, sc["value"], FT("value"), 230, D.red, at=t0 + 0.5, counter=True)
    f = paper.F(FT("value"), 230)
    w = f.getlength(sc["value"])
    D.rough("line", [W / 2 - w / 2, 610, W / 2 + w / 2, 616], D.red, 6, at=t0 + 1.6, dur=0.4)
    if len(bt) > 1 and sc.get("compare"):
        t1 = bt[1][0]
        D.text(W / 2 - 40, 760, sc["compare"]["label"], FT("box"), 52, D.ink, at=t1 + 0.1, anchor="rm")
        D.marker(W / 2 - 10, 760, 300, 64, at=t1 + 0.4)
        D.text(W / 2 + 10, 760, sc["compare"]["value"], FT("value"), 80, D.ink, at=t1 + 0.3, anchor="lm")
        D.sfx.append(("pop", t1 + 0.3))


def s_parking(D: HDoc, sc: dict, bt: list, dur: float):
    D.label(sc.get("label", ""))
    D.chapter_tag(sc.get("_chnum", ""), sc.get("_chtitle", ""))
    D.h1(sc.get("title", ""), y=140)
    g = D._id()
    out = []
    x0, y0 = 560, 250
    for k in range(100):
        r_, c_ = divmod(k, 10)
        x, y = x0 + c_ * 82, y0 + r_ * 56
        out.append(f'<rect x="{x}" y="{y}" width="72" height="46" fill="none" stroke="#9a9488" stroke-width="2"/>')
        if k != 57:
            out.append(f'<rect class="{g}" x="{x + 10}" y="{y + 8}" width="52" height="30" rx="8" fill="{D.ink}"/>')
        else:
            out.append(f'<rect class="{g}h" x="{x + 10}" y="{y + 8}" width="5" height="30" rx="2" fill="{D.red}"/>')
    D.svg.append("".join(out))
    t0 = bt[0][0]
    D.js.append(f'tl.fromTo(".{g}",{{opacity:0,scale:0.4,transformOrigin:"center"}},{{opacity:1,scale:1,duration:0.2,stagger:0.018}},{t0 + 0.3:.2f});')
    D.js.append(f'tl.fromTo(".{g}h",{{opacity:0}},{{opacity:1,duration:0.3}},{t0 + 2.3:.2f});')
    D.circle(x0 + 7 * 82 + 36, y0 + 5 * 56 + 23, 60, 40, at=t0 + 2.6)
    D.text(1500, 520, "0.94%", FT("value"), 110, D.red, at=t0 + 2.4, anchor="lm")
    D.text(1500, 620, "빈자리 비율", FT("note"), 46, D.ink, at=t0 + 2.6, anchor="lm")


def s_compare(D: HDoc, sc: dict, bt: list, dur: float):
    D.label(sc.get("label", ""))
    D.chapter_tag(sc.get("_chnum", ""), sc.get("_chtitle", ""))
    D.h1(sc.get("title", ""), y=140)
    cx = [560, 1020, 1480]
    D.text(cx[1], 290, sc["cols"][0], FT("box"), 46, D.muted, at=0.4)
    D.text(cx[2], 290, sc["cols"][1], FT("box"), 46, D.red, at=0.5)
    D.rough("line", [300, 340, 1720, 342], D.ink, 3, at=0.6, dur=0.5)
    shown = 0
    for b, (t0, d) in zip(sc["beats"], bt):
        upto = b.get("upto", len(sc["rows"]))
        for k in range(shown, upto):
            r = sc["rows"][k]
            y = 440 + k * 170
            at = t0 + 0.3
            D.text(cx[0], y, r["label"], FT("label"), 42, "#5a5f6a", at=at)
            D.text(cx[1], y, r["a"], FT("title"), 56, D.ink, at=at + 0.3)
            D.text(cx[2], y, r["b"], FT("title"), 56, D.red, at=at + 0.8)
            D.marker(cx[2] - 200, y + 10, 400, 40, at=at + 1.0)
            D.sfx.append(("pencil", at + 1.0))
        shown = upto


def s_outro(D: HDoc, sc: dict, bt: list, dur: float):
    D.video(sc["_clipfile"], dur, "photo", push=0.04)
    i = D._id()
    # 사진 위 글자가 읽히도록: 뒤를 살짝 흐리게 + 가운데 종이 카드
    D.items.append(f'<div id="{i}" style="position:absolute;inset:0;background:rgba(238,231,218,.35);backdrop-filter:blur(3px)"></div>')
    D.js.append(f'tl.fromTo("#{i}",{{opacity:0}},{{opacity:1,duration:0.8}},0.6);')
    j = D._id()
    D.items.append(f'<div id="{j}" style="position:absolute;left:{W / 2 - 600:.0f}px;top:360px;width:1200px;height:380px;background:#FBF8F1;'
                   f'box-shadow:0 18px 40px rgba(0,0,0,.28);transform:rotate(-0.8deg)"></div>')
    D.js.append(f'tl.fromTo("#{j}",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.6,ease:"power2.out"}},0.7);')
    D.text(W / 2, 470, sc["title"], FT("title"), 120, D.ink, at=0.9)
    D.rough("line", [W / 2 - 420, 560, W / 2 + 420, 566], D.red, 6, at=1.4, dur=0.5)
    D.text(W / 2, 640, sc.get("sub", ""), FT("note"), 56, D.red, at=1.8)


def s_people(D: HDoc, sc: dict, bt: list, dur: float):
    """100명 그림: 그중 count 명이 빨갛게. 비율을 '사람'으로 느끼게 (3명 중 1명, 10명 중 4명)."""
    D.label(sc.get("label", ""))
    D.chapter_tag(sc.get("_chnum", ""), sc.get("_chtitle", ""))
    D.h1(sc.get("title", ""), y=140)
    n = int(sc["count"])
    g = D._id()
    rng = np.random.default_rng(sc["id"])
    hit = set(rng.choice(100, n, replace=False).tolist()) if sc.get("scatter", True) else set(range(n))
    out, x0, y0 = [], 260, 250
    for k in range(100):
        r_, c_ = divmod(k, 10)
        cx, cy = x0 + c_ * 70, y0 + r_ * 64
        cls = f"{g}h" if k in hit else f"{g}n"
        out.append(f'<g class="{g}"><circle cx="{cx}" cy="{cy}" r="9" fill="{D.muted}"/>'
                   f'<path d="M{cx - 15},{cy + 36} v-8 a15,13 0 0 1 30,0 v8 z" fill="{D.muted}"/></g>'
                   f'<g class="{cls}" style="opacity:0"><circle cx="{cx}" cy="{cy}" r="9" fill="{D.red}"/>'
                   f'<path d="M{cx - 15},{cy + 36} v-8 a15,13 0 0 1 30,0 v8 z" fill="{D.red}"/></g>')
    D.svg.append("".join(out))
    t0 = bt[0][0]
    D.js.append(f'tl.fromTo(".{g}",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.25,stagger:0.012}},{t0 + 0.3:.2f});')
    tf = next((t for b, (t, _) in zip(sc["beats"], bt) if b.get("fill")), bt[-1][0])
    D.js.append(f'tl.to(".{g}h",{{opacity:1,duration:0.2,stagger:0.02}},{tf + 0.3:.2f});')
    D.sfx.append(("pop", tf + 0.3))
    D.text(1080, 470, sc["value"], FT("value"), 150, D.red, at=tf + 0.6, anchor="lm", counter=True)
    D.text(1080, 600, sc.get("caption", ""), FT("note"), fit(FT("note"), sc.get("caption", ""), 50, 760).size, D.ink, at=tf + 0.9, anchor="lm")
    if sc.get("sub"):
        D.text(1080, 690, sc["sub"], FT("label"), fit(FT("label"), sc["sub"], 34, 760).size, "#5a5f6a", at=tf + 1.1, anchor="lm")


def s_newspapers(D: HDoc, sc: dict, bt: list, dur: float):
    """두 나라 신문 비교: 왼쪽은 검은 줄로 지워진(검열) 지면, 오른쪽은 큰 제목으로 보도한 지면. 재구성 그림."""
    D.label(sc.get("label", ""))
    D.chapter_tag(sc.get("_chnum", ""), sc.get("_chtitle", ""))
    L, R = sc["left"], sc["right"]
    tl_ = {b.get("show"): t for b, (t, _) in zip(sc["beats"], bt)}
    for k, (it, x) in enumerate(((L, 250), (R, 1010))):
        at = tl_.get("left" if k == 0 else "right", bt[0][0]) + 0.2
        i = D._id()
        D.items.append(f'<div id="{i}" style="position:absolute;left:{x}px;top:200px;width:660px;height:690px;background:#F7F2E6;'
                       f'box-shadow:0 14px 34px rgba(0,0,0,.22);transform:rotate({-1.2 if k == 0 else 1.0}deg)"></div>')
        D.js.append(f'tl.fromTo("#{i}",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.5,ease:"power2.out"}},{at:.2f});')
        D.text(x + 330, 260, it["name"], FT("title"), 46, D.ink, at=at + 0.2)
        D.rough("line", [x + 40, 300, x + 620, 300], D.ink, 3, at=at + 0.3, dur=0.3, roughness=0.6)
        D.text(x + 330, 330, it.get("sub", ""), FT("label"), 26, "#5a5f6a", at=at + 0.3)
        if k == 0:  # 검열: 글줄 위에 검은 띠
            for r_ in range(9):
                y = 400 + r_ * 50
                w = 560 if r_ % 3 != 2 else 380
                D.items.append(f'<div class="{i}l" style="position:absolute;left:{x + 50}px;top:{y - 4}px;width:{w}px;height:8px;background:#B9B09E;border-radius:4px"></div>')
                j = D._id()
                D.items.append(f'<div id="{j}" style="position:absolute;left:{x + 44}px;top:{y - 16}px;width:{w + 12}px;height:30px;'
                               f'background:#1d1d1d;transform-origin:left center"></div>')
                D.js.append(f'tl.fromTo("#{j}",{{scaleX:0}},{{scaleX:1,duration:0.18,ease:"power1.in"}},{at + 0.9 + r_ * 0.12:.2f});')
            D.stamp(L.get("stamp", "검열"), x + 400, 790, at + 2.2, rot=-10)
        else:
            f = fit(FT("title"), it["headline"], 64, 580)
            D.text(x + 330, 430, it["headline"], FT("title"), f.size, D.red, at=at + 0.5)
            D.marker(x + 330 - f.getlength(it["headline"]) / 2 - 10, 440, f.getlength(it["headline"]) + 20, 30, at=at + 1.0, index=len(D.items))
            for r_ in range(7):
                y = 520 + r_ * 46
                D.items.append(f'<div class="{i}l" style="position:absolute;left:{x + 50}px;top:{y - 4}px;width:{560 if r_ % 3 != 2 else 380}px;height:8px;background:#B9B09E;border-radius:4px"></div>')
            if it.get("note"):
                D.text(x + 330, 850, it["note"], FT("note"), 40, D.ink, at=at + 1.4)
        D.js.append(f'tl.fromTo(".{i}l",{{opacity:0,scaleX:0,transformOrigin:"left center"}},{{opacity:1,scaleX:1,duration:0.25,stagger:0.05}},{at + 0.4:.2f});')
        D.sfx.append(("click-soft", at))


def s_shape(D: HDoc, sc: dict, bt: list, dur: float):
    """모양 비교 개념도 (숫자 축 없음): 보통은 U자, 그때는 W자. 박자마다 곡선 하나씩."""
    D.label(sc.get("label", "개념도 · 모양만 나타냄"))
    D.chapter_tag(sc.get("_chnum", ""), sc.get("_chtitle", ""))
    D.h1(sc.get("title", ""), y=140)
    x0, x1, y0, y1 = 380, 1560, 280, 800
    t0 = bt[0][0]
    D.rough("line", [x0, y1, x1 + 40, y1], D.ink, 3.5, at=t0 + 0.2, dur=0.5, roughness=0.7)
    D.rough("line", [x0, y1, x0, y0 - 30], D.ink, 3.5, at=t0 + 0.3, dur=0.5, roughness=0.7)
    D.text(x1 + 40, y1 + 50, sc.get("xlabel", "나이 →"), FT("note"), 40, D.ink, at=t0 + 0.4, anchor="rm")
    D.text(x0 - 30, y0 - 60, sc.get("ylabel", "사망 위험 ↑"), FT("note"), 40, D.ink, at=t0 + 0.4, anchor="lm")
    for k, tick in enumerate(sc.get("ticks", [])):
        D.text(x0 + (x1 - x0) * tick["at"], y1 + 50, tick["label"], FT("label"), 30, "#5a5f6a", at=t0 + 0.5)
    X = lambda u: x0 + (x1 - x0) * u
    Y = lambda v: y1 - (y1 - y0) * v
    for k, (b, (t, _)) in enumerate(zip(sc["beats"], bt)):
        cv = b.get("curve")
        if not cv:
            continue
        col = D.red if cv.get("tone") == "red" else D.muted
        pts = [[X(u), Y(v)] for u, v in cv["points"]]
        D.rough("curve", [pts], col, 6 if col == D.red else 5, at=t + 0.3, dur=1.4, roughness=0.8)
        lx, ly = cv.get("label_at", [0.8, 0.5])
        D.text(X(lx), Y(ly), cv["label"], FT("box"), 44, col, at=t + 1.2)
        if cv.get("circle"):
            cu, cvv = cv["circle"]
            D.circle(X(cu), Y(cvv), 120, 90, at=t + 1.8)
            if cv.get("note"):
                D.text(X(cu), Y(cvv) - 130, cv["note"], FT("note"), 42, D.red, at=t + 2.1)
        D.sfx.append(("pencil", t + 0.4))


RENDER = {"footage": s_footage, "chart": s_chart, "versus": s_versus, "chapter": s_chapter, "map_causal": s_map_causal,
          "usmap": s_usmap, "quote": s_quote, "checklist": s_checklist, "analogy": s_analogy, "funnel": s_funnel,
          "apartments": s_apartments, "timeline": s_timeline, "bars": s_bars, "bignum": s_bignum, "parking": s_parking,
          "compare": s_compare, "outro": s_outro,
          "people": s_people, "newspapers": s_newspapers, "shape": s_shape}


# ---------------------------------------------------------------- 음성·시간
def voice(project: Project, spec: dict) -> dict:
    """박자마다 TTS → 03_voice/hb_<장면>_<박자>.wav, 길이 표."""
    vdir = project.dir("voice")
    vdir.mkdir(parents=True, exist_ok=True)  # 새 프로젝트는 폴더가 없을 수 있음
    cfg = config.load("pipeline").get("tts", {})
    durs = {}
    for sc in spec["scenes"]:
        for k, b in enumerate(sc["beats"]):
            key = f"{sc['id']:03d}_{k}"
            wav = vdir / f"hb_{key}.wav"
            if not wav.exists():
                mp3 = vdir / f"hb_{key}.mp3"
                if cfg.get("backend") == "elevenlabs":
                    from .media import _elevenlabs
                    _elevenlabs(b["say"], mp3, cfg.get("elevenlabs") or {})
                else:
                    cmd = [shutil.which("edge-tts") or "edge-tts", "--voice", cfg.get("voice", "ko-KR-InJoonNeural"),
                           f"--rate={cfg.get('rate', '+0%')}", "--text", b["say"], "--write-media", str(mp3)]
                    px = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
                    if px:
                        cmd[1:1] = ["--proxy", px]
                    for _ in range(3):
                        if subprocess.run(cmd, capture_output=True).returncode == 0 and mp3.exists() and mp3.stat().st_size > 1000:
                            break
                subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(mp3), "-af",
                                "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse",
                                "-ar", "48000", "-ac", "2", str(wav)], check=True)
            durs[key] = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(wav)],
                                             capture_output=True, text=True).stdout)
    return durs


def timing(sc: dict, durs: dict) -> tuple[list, float]:
    t = LEAD + (0.9 if sc["type"] == "chapter" else 0.0)
    bt = []
    for k, _ in enumerate(sc["beats"]):
        d = durs[f"{sc['id']:03d}_{k}"]
        bt.append((round(t, 2), d))
        t += d + GAP
    # 30fps 프레임 격자에 맞춤: 장면 영상 길이 = 음성 길이 (안 맞추면 장면마다 0.01~0.03초씩 밀려 끝에서 0.6초 어긋남)
    return bt, math.ceil((t - GAP + TAIL) * FPS - 1e-6) / FPS


# ---------------------------------------------------------------- 장면 렌더
def build_scene(project: Project, spec: dict, sc: dict, bt: list, dur: float, work: Path) -> HDoc:
    work.mkdir(parents=True, exist_ok=True)
    a = work / "assets"
    (a / "fonts").mkdir(parents=True, exist_ok=True)
    shutil.copy(hyper.GSAP, a / "gsap.min.js")
    _env_skin = os.environ.get("YTFLOW_SKIN")
    if sc.get("skin"):   # 장면별 그래픽 팩 (스타일 조합: 한 영상 안에서 구간마다 다른 팩)
        os.environ["YTFLOW_SKIN"] = sc["skin"]
    try:
        D = HDoc(sc["id"] * 7 + 3)
    finally:
        if _env_skin is None:
            os.environ.pop("YTFLOW_SKIN", None)
        else:
            os.environ["YTFLOW_SKIN"] = _env_skin
    for p in (paper.SERIF, paper.SERIF_B, paper.PEN, paper.SANS, paper.SANS_X, paper.FONT_DIR / "NanumGothic-Regular.ttf"):
        if not (a / "fonts" / p.name).exists():   # 글꼴은 그래픽 팩(장면별일 수 있음)이 정한 뒤에 연결
            try:
                os.link(p, a / "fonts" / p.name)
            except OSError:
                shutil.copy(p, a / "fonts" / p.name)
    from . import backdrop   # 장면 목적에 맞는 바탕 (film·grid·spot·tint·photo, manual 05 §0-2)
    kind = backdrop.auto(sc, bool(spec.get("footage")))
    chap = int(sc.get("chapter", 0) or 0)
    tag = {"tint": f"_c{chap}", "photo": f"_{sc.get('bg_src', '')}"}.get(kind, "")
    bg_name = f"bg_{D.skin['id']}_{kind}{tag}.jpg"
    bg = a / bg_name
    if not bg.exists():
        still = backdrop.photo_still(project, spec, sc.get("bg_src")) if kind == "photo" else None
        backdrop.make(D.skin, kind, W, HH, chap, still).save(bg, quality=92)
    if sc.get("clip"):  # 원본 영상 구간을 장면 길이만큼 잘라 넣는다 (소리 없음)
        src = project.dir("assets") / "footage" / spec["footage"][sc["clip"]["src"]]["file"]
        out = a / f"clip_{sc['id']:03d}.mp4"
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", str(sc["clip"]["start"]), "-i", str(src),
                        "-t", f"{dur + 0.5:.2f}", "-an", "-vf", "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", str(out)], check=True)
        sc["_clipfile"] = out.name
    sc["_map"] = spec.get("map")
    sc["_chapters"] = [x.get("title", "") for x in spec["scenes"] if x.get("type") == "chapter"]
    sc["_project_dir"] = str(project.path)   # 새 연출(directions.py)이 박자 음성·단어 시각을 찾을 때
    sc["_prices"] = project.dir("research") / "prices"
    if sc["type"] == "usmap":
        sc["_states"] = us_states()
    D.bg_name = bg_name
    from . import graphics
    if not graphics.dispatch(D, sc, bt, dur, RENDER):   # 그래픽 팩이 다른 컴포넌트(그림)를 고르면 그걸로
        RENDER[sc["type"]](D, sc, bt, dur)
    if sc.get("layers"):   # 한 장면 안에서 스타일 겹치기 (directions.apply_layers)
        from . import directions
        directions.apply_layers(D, project, spec, sc, bt, dur, a)
    if sc.get("fx"):   # 시각 효과 (반복 피로 막기, manual 05 §0-3)
        from . import directions as _dir
        _dir.apply_fx(D, project, spec, sc, bt, dur, a)
    idx, html = work / "index.html", D.html(dur, bg_name)
    if not idx.exists() or idx.read_text(encoding="utf-8") != html:  # 바뀐 장면만 다시 렌더
        idx.write_text(html, encoding="utf-8")
    (work / "hyperframes.json").write_text(json.dumps({"name": work.name}), encoding="utf-8")
    return D


def us_states() -> dict:
    cache = config.ROOT / ".cache" / "us_states_1500x860.json"
    if not cache.exists():
        cache.parent.mkdir(parents=True, exist_ok=True)
        r = subprocess.run(["node", str(config.ROOT / "ytflow" / "assets" / "us_states.mjs"), str(hyper.TOOLS / "node_modules"), "1500", "860"],
                           capture_output=True, text=True, check=True)
        cache.write_text(r.stdout, encoding="utf-8")
    return json.loads(cache.read_text(encoding="utf-8"))


def render_scene(work: Path, out: Path) -> str:
    r = subprocess.run([str(hyper.BIN), "render", "--quality", "looks", "-o", str(out.resolve())], cwd=work, env=hyper._env(),
                       capture_output=True, text=True, timeout=1800)
    if r.returncode or not out.exists():
        return (r.stderr or r.stdout)[-300:]
    return ""


# ---------------------------------------------------------------- 자막·효과음·조립
def _ass_time(t: float) -> str:
    h, r = divmod(t, 3600)
    m, s = divmod(r, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def _chunks(text: str, n: int = 24) -> list[str]:
    """자막 한 줄 단위: 문장 끝(. ? !) → 쉼표 → 띄어쓰기 순으로 자연스럽게 끊는다 (한 줄 최대 n자 안팎)."""
    sents = [x.strip() for x in re.split(r"(?<=[.?!])\s+", text) if x.strip()]
    if len(sents) > 1:
        return [c for x in sents for c in _chunks(x, n)]
    if len(text) > n and "," in text:
        parts = [x.strip() for x in re.split(r"(?<=,)\s+", text) if x.strip()]
        if len(parts) > 1 and all(len(x) >= 6 for x in parts):
            return [c for x in parts for c in _chunks(x, n)]
    # 숫자와 단위는 한 줄에 (예: '200만 명을' 이 '200만 / 명을' 로 갈라지지 않게)
    glued = re.sub(r"(\d[\d,.]*[만억천조]?)\s+(명|개|년|원|달러|배|곳|척|대|건|번|살|채|퍼센트|%)", "\\1\u00a0\\2", text)
    words, out, cur = glued.split(" "), [], ""
    for w in words:
        if len((cur + " " + w).strip()) > n and cur:
            out.append(cur.strip())
            cur = w
        else:
            cur += " " + w
    if cur.strip():
        out.append(cur.strip())
    if len(out) > 1 and len(out[-1]) < 7 and len(out[-2]) + len(out[-1]) <= n + 8:  # 짧은 꼬리 줄은 앞 줄에 붙임
        out[-2:] = [out[-2] + " " + out[-1]]
    return [o.replace("\u00a0", " ") for o in out]


def _word_starts(wav: Path, parts: list[str], dur: float) -> list[float] | None:
    """자막 줄마다 '그 줄의 첫 글자를 말하기 시작하는 시각'(박자 음성 기준 초).
    받아쓴 단어의 글자 누적 위치와 대본 글자 누적 위치를 비율로 맞춘다 (받아쓰기가 조금 틀려도 위치는 맞음)."""
    from . import align
    if not align.available():
        return None
    try:
        words = align.transcribe(Path(wav), "ko")
    except Exception:  # noqa: BLE001
        return None
    import difflib
    norm = align._norm
    R, owner = "", []
    for wi, w in enumerate(words):
        t = norm(w["word"])
        R += t
        owner += [wi] * len(t)
    if not R:
        return None
    S, pos = "", []
    for p in parts:
        pos.append(len(S))
        S += norm(p)
    blocks = [b for b in difflib.SequenceMatcher(None, S, R, autojunk=False).get_matching_blocks() if b.size]

    def s2r(p: int) -> int:  # 대본 글자 위치 → 받아쓰기 글자 위치 (글자 단위 맞추기, 숫자·띄어쓰기 차이에 강함)
        prev = (0, 0)
        for b in blocks:
            if b.a <= p < b.a + b.size:
                return b.b + (p - b.a)
            if b.a > p:
                a0, r0 = prev
                return r0 + int((p - a0) * max(b.b - r0, 0) / max(b.a - a0, 1))
            prev = (b.a + b.size, b.b + b.size)
        return len(R) - 1

    # 받아쓰기는 단어 시작을 앞의 쉼(무음) 속으로 당겨 잡기도 한다 → 실제 말소리 시작(무음 끝)으로 보정
    sil, st = [], None
    pr = subprocess.run(["ffmpeg", "-hide_banner", "-nostdin", "-i", str(wav), "-af", "silencedetect=n=-40dB:d=0.15", "-f", "null", "-"],
                        capture_output=True, text=True)
    for ln in pr.stderr.splitlines():
        if "silence_start:" in ln:
            st = float(ln.split("silence_start:")[1].split()[0])
        elif "silence_end:" in ln and st is not None:
            sil.append((st, float(ln.split("silence_end:")[1].split()[0])))
            st = None

    def onset(t: float) -> float:
        for s0, e0 in sil:
            if s0 - 0.3 <= t < e0 - 0.05 and e0 - t <= 1.5:
                return e0
        return t

    out = []
    for p in pos:
        wi = owner[min(max(s2r(p), 0), len(owner) - 1)]
        out.append(min(max(onset(float(words[wi]["start"])) - 0.05, 0.0), dur))
    out[0] = 0.0
    return out


def subtitles(events: list, path: Path) -> None:
    """events: (시작, 끝, 문장). 아래 가운데 상자형 자막."""
    head = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,{font},{size},{text},{text},{outline},{box},1,0,0,0,100,100,0,0,{border_style},{outline_w},0,2,80,80,{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = []
    for ev in events:
        t0, t1, text = ev[:3]
        wav = ev[3] if len(ev) > 3 else None
        parts = _chunks(text)
        starts = _word_starts(wav, parts, t1 - t0) if wav else None
        if starts:  # 실제로 그 말을 하는 순간에 자막이 바뀐다 (faster-whisper 단어 시각)
            for k, p in enumerate(parts):
                a = t0 + starts[k]
                b = t0 + starts[k + 1] - 0.02 if k + 1 < len(parts) else t1 + 0.15
                lines.append(f"Dialogue: 0,{_ass_time(a)},{_ass_time(max(b, a + 0.3))},Sub,,0,0,0,,{p}")
            continue
        tot = sum(len(p) for p in parts) or 1
        t = t0
        for p in parts:
            d = (t1 - t0) * len(p) / tot
            lines.append(f"Dialogue: 0,{_ass_time(t)},{_ass_time(t + d - 0.02)},Sub,,0,0,0,,{p}")
            t += d
    sk = _skin_mod()
    head = head.format(**sk.subtitle_style(sk.load()))   # 자막 상자도 그래픽 스킨이 정함
    path.write_text(head + "\n".join(lines) + "\n", encoding="utf-8")


def sfx_files() -> dict:
    base = config.ROOT / ".claude" / "skills" / "media-use" / "audio" / "assets" / "sfx"
    if not base.exists():
        base = config.ROOT / ".agents" / "skills" / "media-use" / "audio" / "assets" / "sfx"
    files = {k: base / f"{k}.mp3" for k in ("whoosh", "pop", "click-soft", "impact-bass-1")}
    pen = config.ROOT / ".cache" / "sfx" / "pencil.wav"
    if not pen.exists() or pen.stat().st_size < 1000:
        # 연필 긁는 소리: 내려받지 않고 직접 만듦 (분홍 잡음 → 대역 통과 → 빠른 떨림 → 페이드)
        pen.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i",
                        "anoisesrc=color=pink:duration=0.9:amplitude=0.6:seed=7",
                        "-af", "highpass=f=1800,lowpass=f=6500,tremolo=f=11:d=0.7,afade=t=in:d=0.05,afade=t=out:st=0.6:d=0.3",
                        "-ar", "48000", "-ac", "2", str(pen)], check=False)
    if pen.exists() and pen.stat().st_size > 1000:
        files["pencil"] = pen
    return {k: v for k, v in files.items() if v.exists()}


def make(project: Project, workers: int = 3) -> Path:
    spec = json.loads((project.dir("script") / "hybrid.json").read_text(encoding="utf-8"))
    chapters = {sc["chapter"]: sc for sc in spec["scenes"] if sc["type"] == "chapter"}
    for sc in spec["scenes"]:  # 장 표시(왼쪽 위)
        ch = chapters.get(sc.get("chapter"))
        if ch and sc["type"] != "chapter":
            sc["_chnum"], sc["_chtitle"] = ch["num"], ch["title"]
    print("[hybrid] 음성")
    durs = voice(project, spec)
    adir = project.dir("assets")
    plan = []
    for sc in spec["scenes"]:
        bt, dur = timing(sc, durs)
        plan.append((sc, bt, dur))
    print(f"[hybrid] 장면 {len(plan)}개, 총 {sum(p[2] for p in plan):.1f}초 → 렌더 (병렬 {workers})")
    sfx_events = []
    t_acc = 0.0

    def job(item):
        sc, bt, dur = item
        work = adir / "hb" / f"scene_{sc['id']:03d}"
        out = adir / f"hb_{sc['id']:03d}.mp4"
        D = build_scene(project, spec, sc, bt, dur, work)
        issues = D.qa + hyper.check(work)
        err = "" if out.exists() and out.stat().st_mtime > (work / "index.html").stat().st_mtime else render_scene(work, out)
        return sc["id"], D.sfx, issues, err

    results = {}
    with ThreadPoolExecutor(workers) as ex:
        for sid, sfx, issues, err in ex.map(job, plan):
            results[sid] = (sfx, issues, err)
            print(f"[hybrid] #{sid} {'✗ ' + err if err else 'ok'}{' · 점검 ' + str(len(issues)) if issues else ''}")
    # 이어 붙이기 + 음성 + 자막 + 효과음
    edir = project.dir("edit")
    edir.mkdir(parents=True, exist_ok=True)
    work = edir / "hb_work"
    work.mkdir(parents=True, exist_ok=True)
    vlist, alist, subs = [], [], []
    for sc, bt, dur in plan:
        vfile = adir / f"hb_{sc['id']:03d}.mp4"
        vlist.append(f"file '{vfile.resolve()}'")
        # 렌더러가 장면 길이를 0.1초 단위로 올려 잡는다 → 실제 영상 길이를 재서 음성·자막·효과음을 거기에 맞춘다
        # (안 그러면 장면마다 0.01~0.03초씩 화면이 소리보다 늦어져 6분이면 0.5초 어긋남)
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(vfile)],
                                   capture_output=True, text=True).stdout or dur)
        # 장면 음성: 박자 사이 쉼을 넣어 한 파일로
        parts, t = [], 0.0
        for k, (t0, d) in enumerate(bt):
            parts.append((t0, project.dir("voice") / f"hb_{sc['id']:03d}_{k}.wav"))
            if sc["type"] != "kinetic" and sc.get("subs", True):   # 키네틱 장면은 화면 글자가 자막
                subs.append((t_acc + t0, t_acc + t0 + d, sc["beats"][k]["say"], project.dir("voice") / f"hb_{sc['id']:03d}_{k}.wav"))
        for name, at in results[sc["id"]][0]:
            sfx_events.append((name, t_acc + at))
        sa = work / f"a_{sc['id']:03d}.wav"
        inputs, filt = [], []
        for k, (t0, wav) in enumerate(parts):
            inputs += ["-i", str(wav)]
            filt.append(f"[{k + 1}:a]adelay={int(t0 * 1000)}|{int(t0 * 1000)}[d{k}]")  # 0번 입력은 무음 바탕(anullsrc) → 박자 음성은 k+1번
        mix = "".join(f"[d{k}]" for k in range(len(parts)))
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-t", f"{dur:.3f}", "-i", "anullsrc=r=48000:cl=stereo",
                        *inputs, "-filter_complex", ";".join(filt) + f";[0:a]{mix}amix=inputs={len(parts) + 1}:normalize=0:duration=first[a]",
                        "-map", "[a]", "-t", f"{dur:.3f}", str(sa)], check=True)
        alist.append(f"file '{sa.resolve()}'")
        t_acc += dur
    (work / "v.txt").write_text("\n".join(vlist), encoding="utf-8")
    (work / "a.txt").write_text("\n".join(alist), encoding="utf-8")
    ff = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]
    subprocess.run(ff + ["-f", "concat", "-safe", "0", "-i", str(work / "v.txt"), "-c", "copy", str(work / "video.mp4")], check=True)
    subprocess.run(ff + ["-f", "concat", "-safe", "0", "-i", str(work / "a.txt"), "-c", "copy", str(work / "voice.wav")], check=True)
    subtitles(subs, edir / "subs.ass")
    # 효과음 섞기 (작게)
    files = sfx_files()
    ev = [(n, t) for n, t in sfx_events if n in files]
    sfx_wav = work / "sfx.wav"
    if ev:
        inputs, filt = [], []
        vol = {"pencil": 0.12, "whoosh": 0.35, "pop": 0.3, "click-soft": 0.25, "impact-bass-1": 0.3}
        for k, (n, t) in enumerate(ev[:180]):
            inputs += ["-i", str(files[n])]
            filt.append(f"[{k}:a]atrim=0:{1.4 if n == 'pencil' else 2.5},volume={vol.get(n, 0.3)},adelay={int(t * 1000)}|{int(t * 1000)}[s{k}]")
        mix = "".join(f"[s{k}]" for k in range(len(filt)))
        subprocess.run(ff + inputs + ["-filter_complex", ";".join(filt) + f";{mix}amix=inputs={len(filt)}:normalize=0[o]",
                                      "-map", "[o]", "-ar", "48000", "-ac", "2", "-t", f"{t_acc:.2f}", str(sfx_wav)], check=True)
    ass = str((edir / "subs.ass").resolve()).replace(":", "\\:")
    fdir = str(paper.FONT_DIR).replace(":", "\\:")
    a_in = ["-i", str(work / "voice.wav")] + (["-i", str(sfx_wav)] if ev else [])
    amix = "[1:a][2:a]amix=inputs=2:normalize=0:duration=first[a]" if ev else "[1:a]anull[a]"
    subprocess.run(ff + ["-i", str(work / "video.mp4"), *a_in, "-filter_complex", f"[0:v]ass='{ass}':fontsdir='{fdir}'[v];{amix}",
                         "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-c:a", "aac", "-b:a", "192k",
                         str(edir / "draft.mp4")], check=True)
    project.write_json("edit", "hybrid_timeline.json", [{"scene": sc["id"], "type": sc["type"], "dur": dur, "beats": bt} for sc, bt, dur in plan])
    issues = {sid: r[1] for sid, r in results.items() if r[1]}
    project.write_json("assets", "layout_qa.json", {str(k): v for k, v in issues.items()})
    from .finish import master
    master(project)
    print(f"[hybrid] {edir}/final.mp4 ({t_acc:.1f}초)")
    if spec.get("package"):  # 제목·썸네일 (영상과 함께 만든다 — prompts/thumbnail.md)
        from . import thumbnail
        thumbnail.run(project)
    try:  # 완성본 싱크를 받아쓰기로 재서 05_edit/sync_qa.json 에 (자막·목소리 0.3초 이내 95% 이상이면 통과)
        from . import syncqa
        syncqa.run(project)
    except Exception as e:  # noqa: BLE001
        print(f"[hybrid] 싱크 점검 건너뜀: {e}")
    return edir / "final.mp4"


try:  # 새 연출 문법(아카이브 다큐·지도 여정·키네틱 타이포)의 장면 type 을 추가 등록 — 기존 장면은 그대로
    from . import directions as _directions
    _directions.register()
except Exception as _e_dir:  # noqa: BLE001
    print(f"[hybrid] 새 연출 장면 등록 건너뜀: {_e_dir}")
