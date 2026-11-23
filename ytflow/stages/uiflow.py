"""UI 재연·증거 장면 (docs/43-reference-pickle-explainer.md §4) — 레퍼런스에서 구조·기법만 가져온 여섯 가지.

  1. statecard   카드 상태 바꾸기: 같은 카드가 대기 → 진행 → 성공(✓)·실패(빨간 테두리 + X)로 바뀜. 박자마다 state 만 적음
  2. 선 상태 바꾸기: statecard 의 가운데(hub) → 카드 연결선, 그리고 인과 지도(map_causal)의 화살표를
                   지우지 않고 빨간 점선 + X 로 바꿈 (박자 "cut")
  3. chips       실사 영상(footage) 위에 말 칩이 0.6초 간격으로 하나씩 떠오름 (박자 "chips")
  4. docspot     기사·문서 원문 카드: 대사가 닿는 줄만 밝게(나머지 어둡게) + 형광펜 + 옆 숫자 카드
  5. 두 줄 장 표지 chapter "look": "two-line" — 어두운 실사·바탕 위 작은 흰 줄 → 큰 강조색 줄
  6. 모양 매치 아이리스 장면 "iris_out": {"x","y","r"} — 앞 장면의 원이 커져 화면을 덮고, 다음 장면이 원으로 열림

대본 예 (02_script/hybrid.json):
  {"type": "statecard", "title": "AI 비서가 대신 거는 전화", "hub": {"label": "AI 비서", "icon": "bot"},
   "cards": [{"id": "hotel", "label": "호텔 예약", "icon": "phone", "sub": "대기 중"},
             {"id": "kakao", "label": "카카오톡", "icon": "smartphone"}],
   "beats": [{"say": "...", "show": ["hotel", "kakao"]},
             {"say": "...", "state": {"hotel": "run"}, "text": {"hotel": "통화 중"}},
             {"say": "... 막혔습니다.", "state": {"hotel": "ok"}, "cut": ["kakao"]}]}
  {"type": "docspot", "source": "아시아경제 · 11.09", "headline": "...", "paras": ["첫 문단", "둘째 문단"],
   "beats": [{"say": "...", "spot": 1, "num": {"value": "433통", "label": "하루 발신"}}]}
  footage 박자: {"say": "...", "chips": ["프로틴 싸게 사 줘", "메일 좀 정리해 줘"]}
  {"type": "chapter", "look": "two-line", "kicker": "묻지도 않고", "title": "전화를 겁니다", "clip": {...} 또는 bg_src}
  map_causal 박자: {"say": "...", "cut": [["a", "b"]]}
  아무 장면: "iris_out": {"x": 960, "y": 520, "r": 240}
"""
from __future__ import annotations

import html as H
import json
import shutil
from pathlib import Path

W, HH = 1920, 1080
OK, FAIL, RUN, WAIT = "#2FA36B", "#E5484D", "#3B82F6", "#9AA0A8"
CHIP_SLOTS = [(560, 300), (1320, 250), (860, 520), (1440, 580), (500, 690), (1180, 400)]


def _e(s) -> str:
    return H.escape(str(s))


def _pal(D) -> dict:
    return D.skin.get("palette", {}) or {}


def _dark(D) -> bool:
    b = (_pal(D).get("base") or "#F3EFE6").lstrip("#")
    return sum(int(b[i:i + 2], 16) for i in (0, 2, 4)) < 300


def _card_bg(D) -> str:
    return _pal(D).get("card") or ("#1C1F25" if _dark(D) else "#FFFFFF")


def _card_ink(D) -> str:
    return _pal(D).get("ink") or D.ink if _dark(D) else "#1A1C20"


def _sub_ink(D) -> str:
    return _pal(D).get("muted_text") or "#B8C2D0" if _dark(D) else "#5A5F6A"


def notice(D, text: str = "*이해를 돕기 위한 연출입니다"):
    """재연 목업에는 반드시 붙이는 고지 (docs/43 §2 약점: 재연은 실제 화면이 아님)."""
    i = D._id()
    top = 84 if D.__dict__.get("_has_chtag") else 38
    D._hud_or_items().append(f'<div id="{i}" style="position:absolute;left:56px;top:{top}px;font-family:sans;font-size:22px;'
                             f'color:{_sub_ink(D)};white-space:nowrap">{_e(text)}</div>')
    D.js.append(f'tl.fromTo("#{i}",{{opacity:0}},{{opacity:1,duration:0.4}},0.2);')


# ---------------------------------------------------------------- 1·2. 상태 카드 (+ 가운데 hub 와 연결선)
BADGE = {"wait": ("◷", WAIT), "run": ("•••", RUN), "ok": ("✓", OK), "fail": ("✕", FAIL)}
SLOTS_HUB = {1: [(1440, 540)], 2: [(470, 540), (1450, 540)], 3: [(470, 360), (470, 720), (1450, 540)],
             4: [(470, 360), (470, 720), (1450, 360), (1450, 720)],
             5: [(470, 290), (470, 540), (470, 790), (1450, 400), (1450, 680)],
             6: [(470, 290), (470, 540), (470, 790), (1450, 290), (1450, 540), (1450, 790)]}


def _slots_row(n: int) -> list:
    if n <= 3:
        gap = 560
        return [(W / 2 + (k - (n - 1) / 2) * gap, 540) for k in range(n)]
    top = (n + 1) // 2
    return [(W / 2 + (k - (top - 1) / 2) * 560, 400) for k in range(top)] + \
           [(W / 2 + (k - (n - top - 1) / 2) * 560, 700) for k in range(n - top)]


class _Card:
    def __init__(self, D, cd: dict, x: float, y: float, cw: float, ch: float):
        self.D, self.cd, self.x, self.y, self.w, self.h = D, cd, x, y, cw, ch
        self.i = D._id()
        self.state = None
        self.shown = False
        ink, sub, bg = _card_ink(D), _sub_ink(D), _card_bg(D)
        icon = ""
        if cd.get("icon"):
            from .icons import svg_markup
            icon = svg_markup(cd["icon"], 64, ink) or ""
        badges = "".join(
            f'<div id="{self.i}b_{k}" style="position:absolute;right:-22px;top:-22px;width:60px;height:60px;border-radius:50%;background:{c};'
            f'color:#fff;font-family:sans-x;font-size:{26 if k == "run" else 34}px;display:flex;align-items:center;justify-content:center;'
            f'opacity:0;box-shadow:0 6px 14px rgba(0,0,0,.25)">{s}</div>' for k, (s, c) in BADGE.items())
        D.items.append(
            f'<div id="{self.i}" style="position:absolute;left:{x - cw / 2:.0f}px;top:{y - ch / 2:.0f}px;width:{cw:.0f}px;height:{ch:.0f}px;'
            f'background:{bg};border:4px solid transparent;border-radius:24px;box-shadow:0 14px 34px rgba(0,0,0,.16);opacity:0">'
            f'<div style="position:absolute;left:30px;top:{ch / 2 - 32:.0f}px;width:64px;height:64px">{icon}</div>'
            f'<div style="position:absolute;left:{120 if icon else 34}px;top:{ch / 2 - 46:.0f}px;font-family:sans-x;font-size:40px;color:{ink};white-space:nowrap">{_e(cd.get("label", ""))}</div>'
            f'<div id="{self.i}s" style="position:absolute;left:{120 if icon else 34}px;top:{ch / 2 + 8:.0f}px;font-family:sans;font-size:28px;color:{sub};white-space:nowrap">{_e(cd.get("sub", ""))}</div>'
            f'<div id="{self.i}v" style="position:absolute;inset:-4px;border-radius:24px;background:rgba(120,124,132,.0);pointer-events:none"></div>'
            f'<!--SUBS-->{badges}</div>')
        self.idx = len(D.items) - 1
        self.cur = f"{self.i}s"

    def show(self, t: float):
        if self.shown:
            return
        self.shown = True
        self.D.js.append(f'tl.fromTo("#{self.i}",{{opacity:0,scale:.82,y:24}},{{opacity:1,scale:1,y:0,duration:.45,ease:"back.out(1.7)"}},{t:.2f});')
        self.D.sfx.append(("pop", t))

    def set(self, state: str, t: float, text: str | None = None):
        D, i = self.D, self.i
        if self.state and self.state != state:
            D.js.append(f'tl.to("#{i}b_{self.state}",{{opacity:0,scale:.6,duration:.2}},{t:.2f});')
            if self.state == "run":
                D.js.append(f'tl.set("#{i}b_run",{{opacity:0}},{t + 0.2:.2f});')
        col = {"wait": WAIT, "run": RUN, "ok": OK, "fail": FAIL}[state]
        D.js.append(f'tl.to("#{i}",{{borderColor:"{col}",duration:.3}},{t:.2f});')
        D.js.append(f'tl.fromTo("#{i}b_{state}",{{opacity:0,scale:.4}},{{opacity:1,scale:1,duration:.35,ease:"back.out(2.2)"}},{t + 0.05:.2f});')
        if state == "run":   # 진행 중: 배지가 숨 쉬듯 (멈춘 화면 줄이기)
            D.js.append(f'tl.to("#{i}b_run",{{scale:1.12,duration:.5,yoyo:true,repeat:5,ease:"sine.inOut"}},{t + 0.4:.2f});')
        dim = "rgba(120,124,132,.28)" if state == "fail" else "rgba(120,124,132,0)"
        D.js.append(f'tl.to("#{i}v",{{backgroundColor:"{dim}",duration:.3}},{t:.2f});')
        if state == "fail":   # 실패는 짧게 흔들림
            D.js.append(f'tl.fromTo("#{i}",{{x:0}},{{x:10,duration:.06,yoyo:true,repeat:5,ease:"none"}},{t:.2f});')
        if text is not None:
            self.say(text, t)
        D.sfx.append(("click-soft" if state != "fail" else "pop", t))
        self.state = state

    def say(self, text: str, t: float):
        """작은 줄 글자 바꾸기: 새 줄을 같은 자리에 겹쳐 두고 옛 줄은 사라지게 (프레임 탐색에도 안전 — tl.call 안 씀)."""
        D, i = self.D, self.i
        j = D._id()
        left = 120 if self.cd.get("icon") else 34
        D.items[self.idx] = D.items[self.idx].replace(
            "<!--SUBS-->", f'<div id="{j}" style="position:absolute;left:{left}px;top:{self.h / 2 + 8:.0f}px;font-family:sans;font-size:28px;'
                           f'color:{_sub_ink(D)};white-space:nowrap;opacity:0">{_e(text)}</div><!--SUBS-->', 1)
        D.js.append(f'tl.to("#{self.cur}",{{opacity:0,y:-10,duration:.2}},{t:.2f});'
                    f'tl.fromTo("#{j}",{{opacity:0,y:10}},{{opacity:1,y:0,duration:.25}},{t + 0.12:.2f});')
        self.cur = j


def link(D, pts: list, t: float, col: str | None = None, width: float = 5) -> str:
    """깔끔한 연결선(평면 스타일) — 그려지듯 나타남. id 를 돌려줘 나중에 cut_link 로 바꿀 수 있게."""
    i = D._id()
    d = "M" + " L".join(f"{x:.0f},{y:.0f}" for x, y in pts)
    D.svg.append(f'<g id="{i}"><path d="{d}" fill="none" stroke="{col or _sub_ink(D)}" stroke-width="{width}" stroke-linecap="round" '
                 f'stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" id="{i}p"/></g>')
    D.js.append(f'tl.to("#{i}p",{{strokeDashoffset:0,duration:.6,ease:"power2.out"}},{t:.2f});')
    return i


def cut_link(D, gid: str | None, pts: list, t: float):
    """2. 그려진 선을 지우지 않고 '막힌 상태'로: 원래 선은 흐려지고 빨간 점선 + 가운데 X.
    gid: 원래 선을 감싼 <g> id (없으면 덮기만)."""
    i = D._id()
    d = "M" + " L".join(f"{x:.0f},{y:.0f}" for x, y in pts)
    if gid:
        D.js.append(f'tl.to("#{gid}",{{opacity:0.12,duration:.3}},{t:.2f});')
    D.svg.append(f'<path id="{i}" d="{d}" fill="none" stroke="{FAIL}" stroke-width="6" stroke-dasharray="16 14" stroke-linecap="round" opacity="0"/>')
    D.js.append(f'tl.to("#{i}",{{opacity:1,duration:.25}},{t:.2f});'
                f'tl.fromTo("#{i}",{{strokeDashoffset:0}},{{strokeDashoffset:-60,duration:1.2,ease:"none"}},{t:.2f});')
    # 가장 긴 구간의 가운데에 X
    segs = list(zip(pts[:-1], pts[1:]))
    (x0, y0), (x1, y1) = max(segs, key=lambda s: (s[1][0] - s[0][0]) ** 2 + (s[1][1] - s[0][1]) ** 2)
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    j = D._id()
    D.items.append(f'<div id="{j}" style="position:absolute;left:{mx - 32:.0f}px;top:{my - 32:.0f}px;width:64px;height:64px;border-radius:50%;'
                   f'background:{FAIL};color:#fff;font-family:sans-x;font-size:38px;display:flex;align-items:center;justify-content:center;'
                   f'box-shadow:0 6px 16px rgba(0,0,0,.3);opacity:0">✕</div>')
    D.js.append(f'tl.fromTo("#{j}",{{opacity:0,scale:2,rotation:-30}},{{opacity:1,scale:1,rotation:0,duration:.3,ease:"power3.in"}},{t + 0.15:.2f});')
    D.sfx.append(("pop", t + 0.4))


def s_statecard(D, sc: dict, bt: list, dur: float):
    from .hybrid import FT, fit
    D.label(sc.get("label", ""))
    D.chapter_tag(sc.get("_chnum", ""), sc.get("_chtitle", ""))
    D._has_chtag = bool(sc.get("_chnum"))
    if sc.get("notice", True):
        notice(D, sc["notice"] if isinstance(sc.get("notice"), str) else "*이해를 돕기 위한 연출입니다")
    if sc.get("title"):
        D.h1(sc["title"], y=140, size=56)
    cards = sc.get("cards", [])[:6]
    hub = sc.get("hub")
    n = len(cards)
    if hub:
        slots, cw, ch = SLOTS_HUB.get(n, SLOTS_HUB[6]), 460, 150
    else:
        slots, cw, ch = _slots_row(n), 480, 200
    C = {cd["id"]: _Card(D, cd, x, y, cw, ch) for cd, (x, y) in zip(cards, slots)}
    lines = {}
    hx, hy, hr = W / 2, 540, 120
    if hub:
        i = D._id()
        ink = _card_ink(D)
        icon = ""
        if hub.get("icon"):
            from .icons import svg_markup
            icon = svg_markup(hub["icon"], 92, D.red) or ""
        f = fit(FT("label"), hub.get("label", ""), 34, 220)
        D.items.append(f'<div id="{i}" style="position:absolute;left:{hx - hr:.0f}px;top:{hy - hr:.0f}px;width:{2 * hr}px;height:{2 * hr}px;border-radius:50%;'
                       f'background:{_card_bg(D)};border:5px solid {D.red};box-shadow:0 16px 40px rgba(0,0,0,.2);opacity:0">'
                       f'<div style="position:absolute;left:{hr - 46}px;top:{hr - 74}px;width:92px;height:92px">{icon}</div>'
                       f'<div style="position:absolute;left:0;right:0;top:{hr + 28}px;text-align:center;font-family:sans-x;font-size:{f.size}px;color:{ink}">{_e(hub.get("label", ""))}</div></div>')
        D.js.append(f'tl.fromTo("#{i}",{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:.5,ease:"back.out(1.6)"}},{bt[0][0]:.2f});')
        D.js.append(f'tl.to("#{i}",{{y:-8,duration:1.4,yoyo:true,repeat:{max(1, int(dur / 1.4))},ease:"sine.inOut"}},{bt[0][0] + 0.6:.2f});')

    def spoke(c: _Card) -> list:
        sx = 1 if c.x > hx else -1
        return [(hx + sx * hr, hy + (c.y - hy) * 0.25), (c.x - sx * c.w / 2, c.y)]

    for b, (t0, d) in zip(sc["beats"], bt):
        show = b.get("show", [])
        if show == "all":
            show = list(C)
        for k, cid in enumerate(show):
            if cid not in C:
                continue
            c = C[cid]
            ts = t0 + 0.15 + 0.35 * k
            if hub and cid not in lines:
                lines[cid] = link(D, spoke(c), ts)
            c.show(ts + (0.3 if hub else 0))
            if not c.state and c.cd.get("state"):
                c.set(c.cd["state"], ts + 0.35, None)
        texts = b.get("text", {})
        for k, (cid, st) in enumerate((b.get("state") or {}).items()):
            if cid in C:
                C[cid].show(t0)
                C[cid].set(st, t0 + 0.3 + 0.25 * k + b.get("delay", 0.0), texts.get(cid))
        for cid, tx in texts.items():
            if cid in C and cid not in (b.get("state") or {}) and cid not in b.get("cut", []):
                C[cid].say(tx, t0 + 0.3)
        for k, cid in enumerate(b.get("cut", [])):
            if cid in C:
                tc = t0 + 0.5 + 0.3 * k + b.get("delay", 0.0)
                if hub:
                    cut_link(D, lines.get(cid), spoke(C[cid]), tc)
                C[cid].set("fail", tc + 0.2, texts.get(cid))


# ---------------------------------------------------------------- 3. 실사 위 말 칩
def chips(D, items: list, at: float, gap: float = 0.6):
    from .hybrid import FT, fit
    for k, it in enumerate(items[:6]):
        it = it if isinstance(it, dict) else {"text": it}
        x, y = it.get("x"), it.get("y")
        if x is None:
            x, y = CHIP_SLOTS[k % len(CHIP_SLOTS)]
        txt = it["text"]
        f = fit(FT("label"), txt, 36, 760)
        w = f.getlength(txt) + 104
        x = min(max(x, 60 + w / 2), W - 60 - w / 2)
        i = D._id()
        D.items.append(
            f'<div id="{i}" style="position:absolute;left:{x - w / 2:.0f}px;top:{y - 38:.0f}px;width:{w:.0f}px;height:76px;border-radius:38px;'
            f'background:rgba(255,255,255,.96);box-shadow:0 12px 30px rgba(0,0,0,.35);opacity:0">'
            f'<div style="position:absolute;left:24px;top:24px;width:28px;height:28px;border-radius:50%;background:{it.get("color", D.red)}"></div>'
            f'<div style="position:absolute;left:68px;top:0;line-height:76px;font-family:sans-x;font-size:{f.size}px;color:#16181C;white-space:nowrap">{_e(txt)}</div></div>')
        t = at + gap * k
        D.js.append(f'tl.fromTo("#{i}",{{opacity:0,y:30,scale:.7}},{{opacity:1,y:0,scale:1,duration:.4,ease:"back.out(1.8)"}},{t:.2f});')
        D.js.append(f'tl.to("#{i}",{{y:-10,duration:1.6,yoyo:true,repeat:3,ease:"sine.inOut"}},{t + 0.45:.2f});')
        D.sfx.append(("pop", t))


# ---------------------------------------------------------------- 4. 기사·문서 스포트라이트 + 형광펜 + 옆 숫자 카드
def _wrap(font, text: str, maxw: float) -> list:
    out, cur = [], ""
    for word in text.split(" "):
        nxt = (cur + " " + word).strip()
        if font.getlength(nxt) <= maxw or not cur:
            cur = nxt
            while font.getlength(cur) > maxw:   # 띄어쓰기 없는 긴 낱말은 글자 단위로
                cut = len(cur)
                while cut > 1 and font.getlength(cur[:cut]) > maxw:
                    cut -= 1
                out.append(cur[:cut])
                cur = cur[cut:]
        else:
            out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def s_docspot(D, sc: dict, bt: list, dur: float):
    from . import paper
    D.label(sc.get("label", ""))
    D.chapter_tag(sc.get("_chnum", ""), sc.get("_chtitle", ""))
    has_num = any(b.get("num") for b in sc["beats"])
    x0, cw = (110, 1080) if has_num else (310, 1300)
    y0 = 150
    pad = 56
    t0 = bt[0][0]
    # 출처 꼬리표
    if sc.get("source"):
        i = D._id()
        D.items.append(f'<div id="{i}" style="position:absolute;left:{x0}px;top:{y0 - 58}px;padding:6px 16px;border-radius:8px;background:{D.red};'
                       f'color:#fff;font-family:sans-x;font-size:24px;white-space:nowrap">{_e(sc["source"])}</div>')
        D.js.append(f'tl.fromTo("#{i}",{{opacity:0,x:-16}},{{opacity:1,x:0,duration:.35}},{t0:.2f});')
    card = D._id()
    body = []
    rects = []   # 문단마다 [(x, y, w, h) 줄들]
    y = y0 + pad
    if sc.get("img"):   # 캡처 이미지 모드: spot 은 [x, y, w, h] (그림 안 비율)
        from PIL import Image
        src = Path(sc["_project_dir"]) / "04_assets" / sc["img"]
        dst = D._work / "assets" / f"doc_{sc['id']:03d}{src.suffix}"
        if src.exists():
            shutil.copy(src, dst)
            iw, ih = Image.open(src).size
        else:
            D.qa.append(f"docspot: 그림 {sc['img']} 이 없습니다")
            iw, ih = 16, 9
        bw = cw - 2 * pad
        bh = min(bw * ih / iw, 700)
        bw = bh * iw / ih
        body.append(f'<img src="assets/{dst.name}" style="position:absolute;left:{pad}px;top:{pad}px;width:{bw:.0f}px;height:{bh:.0f}px;border-radius:8px">')
        img_box = (x0 + pad, y0 + pad, bw, bh)
        ch = bh + 2 * pad
    else:
        img_box = None
        hl = sc.get("headline", "")
        if hl:
            fh = paper.F(paper.SANS_X, 46)
            for ln in _wrap(fh, hl, cw - 2 * pad)[:2]:
                body.append(f'<div style="position:absolute;left:{pad}px;top:{y - y0:.0f}px;font-family:sans-x;font-size:46px;color:#16181C;white-space:nowrap">{_e(ln)}</div>')
                y += 64
            body.append(f'<div style="position:absolute;left:{pad}px;right:{pad}px;top:{y - y0 + 12:.0f}px;height:2px;background:#E2E4E8"></div>')
            y += 40
        fb = paper.F(paper.SANS, 34)
        for p in sc.get("paras", []):
            rr = []
            for ln in _wrap(fb, p, cw - 2 * pad):
                if y > y0 + 700:
                    D.qa.append("docspot: 문단이 길어 카드 밖으로 넘칩니다 (문단을 줄이세요)")
                    break
                lw = fb.getlength(ln)
                j = D._id()
                body.append(f'<div id="{j}m" style="position:absolute;left:{pad - 6}px;top:{y - y0 + 6:.0f}px;width:{lw + 12:.0f}px;height:42px;'
                            f'background:#D7F25C;border-radius:4px;transform-origin:left center;opacity:0"></div>'
                            f'<div style="position:absolute;left:{pad}px;top:{y - y0:.0f}px;font-family:sans;font-size:34px;line-height:54px;color:#2A2D33;white-space:nowrap">{_e(ln)}</div>')
                rr.append((x0 + pad, y, lw, 54, f"{j}m"))
                y += 56
            rects.append(rr)
            y += 18
        ch = y - y0 + pad - 18
    D.items.append(f'<div id="{card}" style="position:absolute;left:{x0}px;top:{y0}px;width:{cw}px;height:{ch:.0f}px;background:#FFFFFF;border-radius:20px;'
                   f'box-shadow:0 18px 44px rgba(0,0,0,.22);opacity:0">{"".join(body)}</div>')
    D.js.append(f'tl.fromTo("#{card}",{{opacity:0,y:40}},{{opacity:1,y:0,duration:.5,ease:"power2.out"}},{t0 + 0.1:.2f});')
    # 스포트라이트: 박자마다 구멍 난 어두운 막을 새로 두고 앞의 것과 겹쳐 바꿈 (left/top 을 움직이지 않음 — 픽셀 떨림 없게)
    hole = None
    slot = [len(D.items)]   # 막은 문서 카드 바로 위·숫자 카드 아래에 끼워 넣음

    def new_hole(L, T, Wd, Ht):
        h_ = D._id()
        slot[0] += 1
        D.items.insert(slot[0] - 1, f'<div id="{h_}" style="position:absolute;left:{L:.0f}px;top:{T:.0f}px;width:{Wd:.0f}px;height:{Ht:.0f}px;border-radius:12px;'
                       f'box-shadow:0 0 0 3000px rgba(8,9,12,.62);opacity:0;pointer-events:none"></div>')
        return h_
    num_prev = None
    lit = False
    for b, (tb, d) in zip(sc["beats"], bt):
        sp = b.get("spot")
        if sp is not None:
            if img_box:   # [x, y, w, h] 비율
                ix, iy, iw_, ih_ = img_box
                L, T, Wd, Ht = ix + sp[0] * iw_ - 10, iy + sp[1] * ih_ - 8, sp[2] * iw_ + 20, sp[3] * ih_ + 16
                marks = []
            else:
                idx = sp if isinstance(sp, list) else [sp]
                rr = [r for k in idx if 0 <= k < len(rects) for r in rects[k]]
                if not rr:
                    continue
                L = min(r[0] for r in rr) - 16
                T = min(r[1] for r in rr) - 6
                Wd = max(r[0] + r[2] for r in rr) - L + 16
                Ht = max(r[1] + r[3] for r in rr) - T + 6
                marks = [r[4] for r in rr]
            ts = tb + 0.25
            nh = new_hole(L, T, Wd, Ht)
            D.js.append(f'tl.to("#{nh}",{{opacity:1,duration:.4}},{ts:.2f});')
            if hole:
                D.js.append(f'tl.to("#{hole}",{{opacity:0,duration:.4}},{ts:.2f});')
            hole, lit = nh, True
            if b.get("mark", True):
                for k, m in enumerate(marks):
                    D.js.append(f'tl.fromTo("#{m}",{{scaleX:0,opacity:1}},{{scaleX:1,opacity:1,duration:.45,ease:"power1.inOut"}},{ts + 0.35 + 0.3 * k:.2f});')
                if marks:
                    D.sfx.append(("pencil", ts + 0.35))
        elif lit and "spot" in b and b["spot"] is None:   # "spot": null 이면 막을 걷음
            D.js.append(f'tl.to("#{hole}",{{opacity:0,duration:.3}},{tb:.2f});')
            hole, lit = None, False
        if b.get("num"):
            if num_prev:
                D.js.append(f'tl.to("#{num_prev}",{{opacity:0,y:-20,duration:.25}},{tb:.2f});')
            num_prev = num_card(D, b["num"], tb + 0.5, x=x0 + cw + 60, w=W - (x0 + cw + 60) - 90)


def num_card(D, nm: dict, at: float, x: float = 1250, w: float = 580, y: float = 300) -> str:
    """B3·A6 숫자 카드: 작은 이름표 → 큰 숫자(세어 올라감) → 밑줄 바 → 비교 기준 한 줄."""
    from .hybrid import FT, fit
    i = D._id()
    v = str(nm["value"])
    f = fit(FT("value"), v, 132, w - 70)
    D.items.append(f'<div id="{i}" style="position:absolute;left:{x:.0f}px;top:{y}px;width:{w:.0f}px;height:330px;background:#FFFFFF;border-radius:24px;'
                   f'box-shadow:0 18px 44px rgba(0,0,0,.28);opacity:0">'
                   f'<div style="position:absolute;left:36px;top:30px;font-family:sans;font-size:30px;color:#5A5F6A;white-space:nowrap">{_e(nm.get("label", ""))}</div>'
                   f'<div style="position:absolute;left:36px;top:206px;width:{w - 72:.0f}px;height:12px;border-radius:6px;background:#EEF0F3"></div>'
                   f'<div id="{i}u" style="position:absolute;left:36px;top:206px;width:{w - 72:.0f}px;height:12px;border-radius:6px;background:{D.red};'
                   f'transform-origin:left center;opacity:0"></div>'
                   f'<div style="position:absolute;left:36px;top:240px;font-family:sans;font-size:28px;color:#5A5F6A;white-space:nowrap">{_e(nm.get("sub", ""))}</div></div>')
    D.js.append(f'tl.fromTo("#{i}",{{opacity:0,x:40}},{{opacity:1,x:0,duration:.45,ease:"power3.out"}},{at:.2f});')
    D.text(x + 36, y + 130, v, FT("value"), f.size, "#16181C", at=at + 0.25, anchor="lm", counter=True)
    # D.text 는 카드 밖 요소라 카드와 함께 사라지게 묶음
    last = D.items[-1]
    D.items[-1] = last.replace('class="t"', f'class="t {i}g"', 1)
    D.js.append(f'tl.fromTo("#{i}u",{{scaleX:0,opacity:1}},{{scaleX:1,opacity:1,duration:.6,ease:"power2.out"}},{at + 0.9:.2f});')
    D.sfx.append(("pop", at + 0.25))
    return f"{i},.{i}g"


# ---------------------------------------------------------------- 5. 두 줄 장 표지
def _lift(c: str, k: float = 0.38) -> str:
    """어두운 막 위 큰 글자: 강조색을 흰색 쪽으로 밝혀 대비를 올림 (색 계열은 유지)."""
    c = c.lstrip("#")
    return "#" + "".join(f"{round(int(c[i:i + 2], 16) * (1 - k) + 255 * k):02X}" for i in (0, 2, 4))


def chapter_two_line(D, sc: dict, bt: list, dur: float):
    from .hybrid import FT, fit
    if sc.get("_clipfile"):
        D.video(sc["_clipfile"], dur, "full", push=0.04)
    i = D._id()
    D.media.append(f'<div id="{i}" style="position:absolute;inset:0;background:rgba(8,9,12,{sc.get("dim", 0.62)})"></div>')
    kick, title = sc.get("kicker", ""), sc.get("title", "")
    acc = sc.get("color") or ("#C8F25A" if sc.get("lime") else _lift(D.red))
    fk = fit(FT("label"), kick, 54, W - 300)
    ft = fit(FT("title"), title, 128, W - 260)
    yk, yt = (430, 560) if kick else (0, 520)
    if kick:
        j = D._id()
        D.items.append(f'<div id="{j}" style="position:absolute;left:0;right:0;top:{yk}px;text-align:center;font-family:sans;font-size:{fk.size}px;'
                       f'color:#FFFFFF;opacity:0">{_e(kick)}</div>')
        D.js.append(f'tl.fromTo("#{j}",{{opacity:0,y:26}},{{opacity:1,y:0,duration:.4,ease:"power2.out"}},0.45);')
    k = D._id()
    D.items.append(f'<div id="{k}" style="position:absolute;left:0;right:0;top:{yt}px;text-align:center;font-family:sans-x;font-size:{ft.size}px;'
                   f'color:{acc};opacity:0;text-shadow:0 6px 24px rgba(0,0,0,.45)">{_e(title)}</div>')
    D.js.append(f'tl.fromTo("#{k}",{{opacity:0,y:40,scale:.94}},{{opacity:1,y:0,scale:1,duration:.45,ease:"power3.out"}},0.85);')
    D.sfx.append(("whoosh-short", 0.8))


# ---------------------------------------------------------------- 6. 모양 매치 아이리스
def iris_out(D, sc: dict, dur: float, nxt_color: str | None = None):
    """앞 장면의 원(x, y, r)이 테두리째 커져 화면을 덮음 → 다음 장면은 같은 색 바탕에서 원으로 열림(iris_in)."""
    io = sc["iris_out"]
    x, y, r = io.get("x", W / 2), io.get("y", HH / 2), io.get("r", 200)
    col = io.get("color") or nxt_color or _pal(D).get("base") or "#F3EFE6"
    far = max(((x - cx) ** 2 + (y - cy) ** 2) ** 0.5 for cx in (0, W) for cy in (0, HH))
    i = D._id()
    D.top = getattr(D, "top", []) + [
        f'<div id="{i}" style="position:absolute;left:{x - r:.0f}px;top:{y - r:.0f}px;width:{2 * r:.0f}px;height:{2 * r:.0f}px;border-radius:50%;'
        f'border:{io.get("ring", 8)}px solid {io.get("ring_color", D.red)};background:transparent;opacity:0;z-index:60" data-layout-ignore></div>']
    t = max(0.0, dur - 0.75)
    D.js.append(f'tl.to("#{i}",{{opacity:1,duration:.2}},{t:.2f});'
                f'tl.to("#{i}",{{scale:{far / r * 1.05:.2f},backgroundColor:"{col}",duration:.55,ease:"power2.in"}},{t + 0.2:.2f});')
    D.sfx.append(("whoosh-short", t + 0.2))
    return col


def iris_in(D, col: str, at: tuple | None = None):
    x, y = (at or (W / 2, HH / 2))
    D.css.append(f"html,body{{background:{col} !important}}")
    D.js.append(f'tl.fromTo("#root",{{clipPath:"circle(0px at {x:.0f}px {y:.0f}px)"}},'
                f'{{clipPath:"circle(1400px at {x:.0f}px {y:.0f}px)",duration:.6,ease:"power2.out"}},0);')


# ---------------------------------------------------------------- 등록
def register():
    from . import hybrid
    hybrid.RENDER["statecard"] = s_statecard
    hybrid.RENDER["docspot"] = s_docspot
    orig = hybrid.RENDER["chapter"]

    def chapter(D, sc, bt, dur):
        return chapter_two_line(D, sc, bt, dur) if sc.get("look") == "two-line" else orig(D, sc, bt, dur)
    hybrid.RENDER["chapter"] = chapter
