"""board.json 만들기 — v2(2분 완성판).

그림 조각(04_assets/story/gen/*.png) 위에 손글씨 이름표·빨간 펜 표시를 얹을 때,
'그림 안의 어느 지점'을 그림판 좌표로 바꿔 주는 계산을 여기서 한 번만 한다.
그래서 그림을 조금 옮기거나 키워도 이름표·동그라미가 같이 따라간다.

    python3 build/board_spec.py          # 02_script/board.json 다시 쓰기

장면마다 `gap`(장면 사이 숨 고르는 시간)은 scenes.json 이 유일한 출처 — board.py ·
subs_timed.py · build/timeline.py 가 같은 값을 읽어 그림·자막·편집본이 같은 박자로 움직인다.
"""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
PROJ = ROOT / "projects" / "20261114-curiosity-test"
GEN = PROJ / "04_assets" / "story" / "gen"
OUT = PROJ / "02_script" / "board.json"


def size(src: str) -> tuple[int, int]:
    with Image.open(GEN / src) as im:
        return im.size


def art(src: str, cx: float, cy: float, w: float, **kw) -> dict:
    return {"kind": "art", "src": src, "x": round(cx), "y": round(cy), "w": round(w), **kw}


class Placed:
    """그림 조각 하나를 그림판에 놓고, 그 안의 (u,v) → 그림판 좌표를 계산해 준다."""

    def __init__(self, src: str, cx: float, cy: float, w: float):
        self.src, self.cx, self.cy, self.w = src, cx, cy, w
        self.h = w * size(src)[1] / size(src)[0]

    def p(self, u: float, v: float) -> tuple[float, float]:
        return (self.cx + (u - 0.5) * self.w, self.cy + (v - 0.5) * self.h)


def note(text, x, y, fs=54, color="ink", rot=-3, font="pen", **kw) -> dict:
    return {"kind": "note", "text": text, "x": round(x), "y": round(y), "fs": fs, "color": color, "rot": rot,
            "font": font, **kw}


def label(text, x, y, fs=54, **kw) -> dict:
    return {"kind": "note", "text": text, "x": round(x), "y": round(y), "fs": fs, "color": "ink", "rot": 0,
            "font": "pen", **kw}


def leader(p0, p1, sw=3.5, **kw) -> dict:
    return {"kind": "dash", "from": [round(p0[0]), round(p0[1])], "to": [round(p1[0]), round(p1[1])], "sw": sw,
            "color": "ink", **kw}


def pen_circle(p, rx=52, ry=46, sw=7, color="red", **kw) -> dict:
    return {"kind": "circle", "x": round(p[0]), "y": round(p[1]), "rx": rx, "ry": ry, "sw": sw, "color": color, **kw}


def arrow(p0, p1, sw=8, bend=0, color="red", **kw) -> dict:
    return {"kind": "arrow", "from": [round(p0[0]), round(p0[1])], "to": [round(p1[0]), round(p1[1])], "sw": sw,
            "bend": bend, "color": color, **kw}


def path(pts, sw=4, color="mute", alpha=170, dash=None, **kw) -> dict:
    it = {"kind": "penpath", "pts": [[round(x), round(y)] for x, y in pts], "sw": sw, "color": color,
          "alpha": alpha, **kw}
    if dash:
        it["dash"] = dash
    return it


def fill(x0, y0, x1, y1, color="mark", alpha=95, **kw) -> dict:
    return {"kind": "fillrect", "x0": round(x0), "y0": round(y0), "x1": round(x1), "y1": round(y1),
            "color": color, "alpha": alpha, **kw}


scenes = []

# ---------------------------------------------------------------- 1. 창틀 아래 구멍
pl = Placed("window_hole.png", 1900, 1010, 900)
hole = pl.p(0.4965, 0.722)
items = [
    art("window_hole.png", 1900, 1010, 900, dur=0.9, rot=0.8, t=0.0),
    pen_circle(hole, 54, 48, 7, dur=0.6, word="구멍이"),
    arrow((hole[0] + 640, hole[1] + 60), (hole[0] + 95, hole[1] + 22), sw=6, bend=-26, dur=0.6, word="구멍이"),
    note("여기", hole[0] + 700, hole[1] - 20, fs=68, color="red", rot=-6, dur=0.5, word="구멍이"),
]
scenes.append({"id": 1, "bg": "paper", "fade": 0.5,
               "cam": [[0, 1900, 1010, 0.86], [3.0, 1905, 1020, 0.94]], "items": items})

# ---------------------------------------------------------------- 2. 왜 뚫었을까
items = [
    art("window_hole.png", 1900, 960, 800, dur=0.5, t=0.0),
    pen_circle(Placed("window_hole.png", 1900, 960, 800).p(0.4965, 0.722), 46, 42, 6, dur=0.5, t=0.1),
    {"kind": "big", "text": "?", "x": 2560, "y": 620, "fs": 300, "font": "pen", "color": "red", "dur": 0.5,
     "word": "이상합니다"},
]
scenes.append({"id": 2, "bg": "paper",
               "cam": [[0, 1900, 1000, 0.9], [3.2, 1905, 1005, 0.96]], "items": items})

# ---------------------------------------------------------------- 3. 브리더 홀
items = [
    art("window_hole.png", 1900, 960, 800, dur=0.5, t=0.0),
    pen_circle(Placed("window_hole.png", 1900, 960, 800).p(0.4965, 0.722), 46, 42, 6, dur=0.5, t=0.1),
    note("브리더 홀", 2620, 700, fs=62, color="red", rot=-2, dur=0.5, word="브리더"),
    leader(Placed("window_hole.png", 1900, 960, 800).p(0.4965, 0.722), (2500, 760), 3, word="브리더"),
]
scenes.append({"id": 3, "bg": "paper",
               "cam": [[0, 1900, 1010, 0.9], [3.6, 1905, 1015, 0.97]], "items": items})

# ---------------------------------------------------------------- 4. 세 겹
# 단면 그림은 세로로 긴 판(795×1341)이라, 왼쪽에 세워 두고 오른쪽 여백에 이름표를 단다.
SEC_X, SEC_Y, SEC_W = 1560, 940, 760
SEC_Z = 0.68                      # 판 전체(위·아래 창틀까지)가 자막 위로 들어오는 배율
sec = Placed("section.png", SEC_X, SEC_Y, SEC_W)
items = [
    art("section.png", SEC_X, SEC_Y, SEC_W, dur=0.9, word="옆에서"),
    note("세 겹", sec.p(0.5, 0.30)[0] + 330, sec.p(0.5, 0.30)[1], fs=78, color="red", rot=-4, dur=0.6, word="세 겹"),
]
scenes.append({"id": 4, "bg": "paper",
               "cam": [[0, 1700, 1020, SEC_Z - 0.04], [4.8, 1710, 1025, SEC_Z]], "items": items})

# ---------------------------------------------------------------- 5. 이름표 세 개
outer = sec.p(0.321, 0.55)
middle = sec.p(0.531, 0.55)
inner = sec.p(0.674, 0.55)
LX = sec.p(1.0, 0)[0] + 90          # 판 오른쪽 여백에 이름표를 세로로 늘어놓는다
items = [
    art("section.png", SEC_X, SEC_Y, SEC_W, dur=0.4, t=0.0),
    leader(sec.p(0.321, 0.18), (LX - 30, 640), 3, word="바깥"),
    label("바깥 창", LX, 640, 74, word="바깥"),
    {"kind": "circle", "x": round(sec.p(0.321, 0.18)[0]), "y": round(sec.p(0.321, 0.18)[1]), "rx": 12, "ry": 12,
     "sw": 6, "color": "ink", "dur": 0.3, "word": "바깥"},
    leader(sec.p(0.531, 0.40), (LX - 30, 1010), 3, word="가운데"),
    label("가운데 창", LX, 1010, 74, word="가운데"),
    {"kind": "circle", "x": round(sec.p(0.531, 0.40)[0]), "y": round(sec.p(0.531, 0.40)[1]), "rx": 10, "ry": 10,
     "sw": 6, "color": "ink", "dur": 0.3, "word": "가운데"},
    leader(sec.p(0.674, 0.62), (LX - 30, 1380), 3, word="안쪽"),
    label("안쪽 창", LX, 1380, 74, word="안쪽"),
    {"kind": "circle", "x": round(sec.p(0.674, 0.62)[0]), "y": round(sec.p(0.674, 0.62)[1]), "rx": 10, "ry": 10,
     "sw": 6, "color": "ink", "dur": 0.3, "word": "안쪽"},
]
scenes.append({"id": 5, "bg": "paper",
               "cam": [[0, 1700, 1020, SEC_Z], [3.6, 1710, 1030, SEC_Z + 0.04]], "items": items})

# ---------------------------------------------------------------- 6. 안쪽 창은 긁힘 방지
items = [
    art("section.png", SEC_X, SEC_Y, SEC_W, dur=0.4, t=0.0),
    label("안쪽 창", inner[0] + 330, inner[1] - 60, 66),
    leader(inner, (inner[0] + 290, inner[1] - 60), 3.5),
    note("힘은 안 받는다", inner[0] + 280, inner[1] + 150, fs=52, color="red", rot=-3, dur=0.5, word="힘을"),
    note("긁힘만 막는다", inner[0] + 300, inner[1] + 330, fs=52, color="ink", rot=-2, dur=0.5, word="긁히지"),
    arrow((inner[0] + 250, inner[1] + 290), (inner[0] + 40, inner[1] + 60), sw=7, bend=30, dur=0.6, word="긁히지"),
]
scenes.append({"id": 6, "bg": "paper",
               "cam": [[0, 1700, 1020, SEC_Z], [4.2, inner[0] - 40, 990, 1.05]], "items": items})

# ---------------------------------------------------------------- 7. 구멍은 가운데 창
hole = sec.p(0.528, 0.792)
items = [
    art("section.png", SEC_X, SEC_Y, SEC_W, dur=0.4, t=0.0),
    pen_circle(hole, 58, 50, 7, dur=0.6, word="구멍은"),
    note("구멍", hole[0] + 230, hole[1] - 20, fs=54, color="red", rot=-3, dur=0.45, word="가운데"),
    {"kind": "cross", "x": round(outer[0]), "y": round(outer[1] + 330), "s": 46, "sw": 9, "dur": 0.5,
     "word": "아니라"},
    note("구멍 없음", outer[0] - 250, outer[1] + 210, fs=44, color="red", rot=-5, dur=0.45, word="아니라"),
]
scenes.append({"id": 7, "bg": "paper",
               "cam": [[0, 1700, 1020, SEC_Z], [3.4, hole[0] + 10, hole[1] - 60, 1.34]], "items": items})

# ---------------------------------------------------------------- 8. 두 기압
items = [
    art("cabin.png", 1900, 985, 1650, dur=0.8, word="3만"),
    {"kind": "stamp", "text": "35,000 ft", "x": 1180, "y": 480, "fs": 48, "rot": -7, "dur": 0.5, "word": "피트"},
    {"kind": "chip", "text": "밖 0.23기압", "x": 950, "y": 760, "fs": 44, "dur": 0.6, "word": "밖의"},
    arrow((1050, 800), (1200, 880), sw=6, bend=18, color="blue", dur=0.5, word="밖의"),
    {"kind": "chip", "text": "기내 0.75기압", "x": 2680, "y": 880, "fs": 44, "hl": 1, "dur": 0.6, "word": "기내는"},
    arrow((2560, 940), (2380, 1030), sw=6, bend=-16, dur=0.5, word="기내는"),
]
scenes.append({"id": 8, "bg": "paper",
               "cam": [[0, 1900, 1000, 0.76], [5.4, 1930, 1015, 0.82]], "items": items})

# ---------------------------------------------------------------- 9. 공기가 구멍으로
hole = sec.p(0.528, 0.792)
g1 = (sec.p(0.399, 0)[0], sec.p(0.501, 0)[0])
g2 = (sec.p(0.561, 0)[0], sec.p(0.641, 0)[0])
glass_top, glass_bot = sec.p(0, 0.215)[1], sec.p(0, 0.80)[1]
items = [
    art("section.png", SEC_X, SEC_Y, SEC_W, dur=0.5, t=0.0),
    arrow((sec.p(1.0, 0.0)[0] + 560, hole[1] - 150), (hole[0] + 16, hole[1] - 6), sw=8, bend=-62, color="blue",
          dur=0.9, word="구멍으로"),
    note("기내 공기", sec.p(1.0, 0)[0] + 470, hole[1] - 300, fs=50, color="blue", rot=-3, dur=0.45, word="구멍으로"),
    fill(g1[0], glass_top, g1[1], glass_bot, "mark", 95, dur=0.7, word="틈도"),
    fill(g2[0], glass_top, g2[1], glass_bot, "mark", 95, dur=0.7, word="틈도"),
    note("사이 틈도 같은 압력", sec.p(0.30, 0)[0], glass_top - 120, fs=40, color="ink", rot=-1, dur=0.45, word="같은"),
]
scenes.append({"id": 9, "bg": "paper",
               "cam": [[0, 1690, 1020, SEC_Z], [4.6, 1730, 1030, SEC_Z + 0.04]], "items": items})

# ---------------------------------------------------------------- 10. 압력은 바깥 창 하나에
items = [
    art("section.png", SEC_X, SEC_Y, SEC_W, dur=0.4, t=0.0),
    fill(g1[0], glass_top, g1[1], glass_bot, "mark", 95, dur=0.2, t=0.0),
    fill(g2[0], glass_top, g2[1], glass_bot, "mark", 95, dur=0.2, t=0.0),
    arrow((g1[1] - 8, glass_top + 190), (sec.p(0.399, 0)[0] + 14, glass_top + 190), sw=13, bend=0, dur=0.4, word="바깥"),
    arrow((g1[1] - 8, glass_top + 430), (sec.p(0.399, 0)[0] + 14, glass_top + 430), sw=13, bend=0, dur=0.4, word="바깥"),
    arrow((g1[1] - 8, glass_top + 670), (sec.p(0.399, 0)[0] + 14, glass_top + 670), sw=13, bend=0, dur=0.4, word="바깥"),
    note("힘은 여기로", outer[0] - 470, glass_top + 210, fs=54, color="red", rot=-4, dur=0.5, word="혼자"),
    arrow((outer[0] - 300, glass_top + 260), (outer[0] + 40, glass_top + 360), sw=7, bend=20, dur=0.6, word="혼자"),
]
scenes.append({"id": 10, "bg": "paper",
               "cam": [[0, 1690, 1020, SEC_Z], [3.6, 1670, 1030, SEC_Z + 0.03]], "items": items})

# ---------------------------------------------------------------- 11. 지름길
gate = Placed("gate.png", 1950, 1150, 2300)
items = [
    art("gate.png", 1950, 1150, 2300, dur=0.8, t=0.0),
    note("압력", 1000, 980, fs=54, color="red", rot=-3, dur=0.5, word="지나가는"),
    path([(1060, 1060), (1120, 800), (1800, 740), (2700, 800), (2880, 1060)], sw=5, color="mute", alpha=180,
         dash=(26, 22), dur=1.2, word="지나가는"),
    {"kind": "cross", "x": 1950, "y": 750, "s": 54, "sw": 10, "dur": 0.5, "word": "지나가는"},
    arrow((1450, 1170), (2400, 1170), sw=9, bend=0, dur=0.8, word="지름길"),
]
scenes.append({"id": 11, "bg": "paper",
               "cam": [[0, 1950, 1120, 0.70], [3.0, 1960, 1130, 0.78]], "items": items})

# ---------------------------------------------------------------- 12. 예비 선수
wh = Placed("window_hole.png", 780, 1040, 470)
items = [
    art("window_hole.png", 780, 1040, 470, dur=0.7, rot=-1, t=0.0),
    art("bench.png", 2280, 1100, 1260, dur=0.9, rot=-0.8, t=0.2),
    note("바깥 창이 깨지면", 780, 1390, fs=46, color="mute", rot=-3, dur=0.45, word="깨지는"),
    note("예비 선수", 2620, 860, fs=56, color="red", rot=-4, dur=0.5, word="예비"),
    arrow((1180, 1270), (1760, 1200), sw=9, bend=-30, dur=0.7, word="이어받죠"),
]
scenes.append({"id": 12, "bg": "sand",
               "cam": [[0, 1750, 1150, 0.7], [5.6, 1780, 1160, 0.77]], "items": items})

# ---------------------------------------------------------------- 13. FAA 지침
items = [
    {"kind": "doc", "x": 1000, "y": 430, "w": 1040, "h": 1160, "dur": 0.9, "word": "2003년",
     "head": "AC 25.775-1", "sub": "Windows and Windshields · FAA · 2003. 1. 17", "lines": 6,
     "quotes": ["main load bearing pane", "fail-safe pane"],
     "glosses": ["주 하중 창 — 기내 압력을 혼자 견딘다", "예비 창 — 주 창이 깨지면 대신 견딘다"],
     "quote_fs": 32, "gloss_fs": 28},
    {"kind": "stamp", "text": "2003 · FAA", "x": 2320, "y": 900, "fs": 52, "rot": -8, "dur": 0.55, "word": "적어"},
    {"kind": "check", "x": 2250, "y": 1290, "s": 64, "sw": 11, "color": "red", "dur": 0.55, "word": "두었습니다"},
    {"kind": "credit", "text": "출처 · FAA Advisory Circular AC 25.775-1 (2003. 1. 17)", "x": 1000, "y": 1650,
     "fs": 25, "dur": 0.6, "t": 0.2},
]
scenes.append({"id": 13, "bg": "paper",
               "cam": [[0, 1700, 1030, 0.76], [5.0, 1730, 1040, 0.82]], "items": items})

# ---------------------------------------------------------------- 14. 1954, 네모난 창
VIN_X, VIN_Y, VIN_W = 1900, 980, 2100
vin = Placed("vintage.png", VIN_X, VIN_Y, VIN_W)
win = vin.p(0.61, 0.48)
items = [
    art("vintage.png", VIN_X, VIN_Y, VIN_W, dur=0.9, word="1954년"),
    pen_circle(win, 66, 58, 7, dur=0.6, word="네모난"),
    note("네모난 창", win[0] - 120, win[1] + 250, fs=52, color="red", rot=-3, dur=0.45, word="네모난"),
    {"kind": "stamp", "text": "1954", "x": 2760, "y": 720, "fs": 54, "rot": -8, "dur": 0.55, "word": "1954년"},
]
scenes.append({"id": 14, "bg": "paper",
               "cam": [[0, 1900, 1000, 0.7], [4.4, 1980, 1010, 0.78]], "items": items})

# ---------------------------------------------------------------- 15. 창가의 금속에 금
items = [
    art("vintage.png", VIN_X, VIN_Y, VIN_W, dur=0.4, t=0.0),
    pen_circle(win, 66, 58, 7, dur=0.3, t=0.0),
    {"kind": "crack", "x": round(win[0]), "y": round(win[1]), "s": 0.95, "sw": 5, "dur": 0.7, "word": "금이"},
    note("창가 금속에 금", win[0] + 230, win[1] + 250, fs=50, color="red", rot=-2, dur=0.45, word="금이"),
    note("네 귀퉁이에 힘이 몰려서", win[0] - 160, win[1] + 40, fs=44, color="ink", rot=-2, dur=0.45, word="귀퉁이에"),
]
scenes.append({"id": 15, "bg": "paper",
               "cam": [[0, 1900, 1000, 0.7], [2.8, win[0] - 260, win[1] + 40, 1.5]], "items": items})

# ---------------------------------------------------------------- 16. 둥근 창, 아크릴
items = [
    art("window_hole.png", 1150, 1000, 720, dur=0.7, rot=1, t=0.0),
    art("acrylic.png", 2380, 1000, 430, dur=0.8, rot=1.5, t=0.5, word="아크릴"),
    note("둥근 창", 1150, 1400, fs=48, color="mute", rot=-3, dur=0.45, word="둥글어졌습니다"),
    note("스트레치드 아크릴", 2380, 1400, fs=54, color="red", rot=-3, dur=0.5, word="아크릴"),
]
scenes.append({"id": 16, "bg": "paper",
               "cam": [[0, 1800, 1000, 0.72], [3.6, 1820, 1010, 0.78]], "items": items})

# ---------------------------------------------------------------- 17. 구멍이 막히면
fr_ = Placed("fog_right.png", 2200, 1000, 620)
items = [
    art("fog_left.png", 1450, 1000, 620, dur=0.8, rot=-1, t=0.0),
    art("fog_right.png", 2200, 1000, 620, dur=0.8, rot=1, t=0.1),
    note("김 서림", 1450, 640, fs=50, color="mute", rot=-3, dur=0.45, word="서립니다"),
    note("구멍이 없으면", 1450, 1400, fs=50, color="red", rot=-3, dur=0.45, word="서립니다"),
    note("구멍 있으면", 2200, 1400, fs=50, color="mute", rot=-3, dur=0.45, word="서립니다"),
    pen_circle(fr_.p(0.503, 0.741), 44, 40, 6, dur=0.5, word="서립니다"),
]
scenes.append({"id": 17, "bg": "paper",
               "cam": [[0, 1820, 1010, 0.72], [4.4, 1830, 1020, 0.79]], "items": items})

# ---------------------------------------------------------------- 18. 봉이 먼저 지친다
items = [
    art("fog_left.png", 1450, 1000, 620, dur=0.5, rot=-1, t=0.0),
    art("fog_right.png", 2200, 1000, 620, dur=0.5, rot=1, t=0.0),
    note("김 서림", 1450, 640, fs=50, color="mute", rot=-3, t=0.0),
    note("구멍이 없으면", 1450, 1400, fs=50, color="red", rot=-3, t=0.0),
    note("봉이 먼저 지친다", 2600, 1120, fs=48, color="red", rot=-2, dur=0.5, word="틈이"),
    arrow((2560, 1230), (2150, 1180), sw=7, bend=-30, dur=0.6, word="틈이"),
]
scenes.append({"id": 18, "bg": "paper",
               "cam": [[0, 1820, 1010, 0.79], [3.4, 1500, 1010, 0.94]], "items": items})

# ---------------------------------------------------------------- 19. 아웃트로
wh2 = Placed("window_hole.png", 2850, 1010, 700)
items = [
    art("passenger.png", 1650, 1030, 1100, dur=0.6, rot=-1, t=0.0),
    art("window_hole.png", 2850, 1010, 700, dur=0.8, rot=1, t=0.2),
    pen_circle(wh2.p(0.4965, 0.722), 46, 42, 7, dur=0.7, word="구멍을"),
    arrow((2340, 1110), (2600, 1130), sw=7, bend=20, dur=0.6, word="구멍을"),
]
scenes.append({"id": 19, "bg": "paper",
               "cam": [[0, 1900, 1030, 0.62], [5.2, 1900, 1040, 0.55]], "items": items})

gaps = {s["id"]: float(s.get("gap", 0.6))
        for s in json.loads((PROJ / "02_script" / "scenes.json").read_text(encoding="utf-8"))["scenes"]}
for sc in scenes:            # 숨 고르는 시간은 scenes.json 이 유일한 출처
    sc["gap"] = gaps.get(sc["id"], 0.6)

board = {
    "_설명": "이야기 그림판 대본 v2 — 그림판 3840×2160 기준 좌표. word = 그 낱말을 말하는 순간 그려진다(03_voice/timings.json). "
            "gap = 장면 뒤 숨 고르는 시간(초). cam = [[초, 중심x, 중심y, 확대], ...]. 이 파일은 build/board_spec.py 가 만든다(직접 고치지 말 것).",
    "scenes": scenes,
}
OUT.write_text(json.dumps(board, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"[board_spec] 장면 {len(scenes)}개 → {OUT}")
