"""호기심 편 「생각하지 않으려 할수록 더 떠오르는 이유」(projects/20261120-curiosity-whitebear-v2) v3 — 전체 장면.

화면의 네 자리 (manual/12 §0-1, 04 §0-7):
  이야기 = GPT 이미지 원화(2×2 시트를 자른 완성 프레임, 컷마다 카메라 고정 — 잼 편 방식)
  설명   = 원화 위 손글씨 쪽지 · 칸 만화(5분 막대 위 종, 두·세 줄 비교) — 기억 편 방식
  증거   = 논문 첫 장(저자 공개 PDF) 스포트라이트
  마디   = 검은 화면 한 줄 · 장 제목(번호 + 장면 이름)
시각은 sentences.json(문장) + words.json(낱말, 받아쓰기).

    python scripts/anim/prep_whitebear.py <art> --paper <paper_crop.png> [--dry]
    python scripts/anim/ep_whitebear.py <art> <voice 폴더> <out.html>
    bash scripts/anim/render_all.sh <out 폴더> <out.html> <voice>/voice.mp3 <voice>/captions.ass <END> <result.mp4>
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from anim import Film  # noqa: E402
from comic import Page  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("art", type=Path)
ap.add_argument("voice", type=Path)
ap.add_argument("out", type=Path)
a = ap.parse_args()

SENT = json.loads((a.voice / "sentences.json").read_text(encoding="utf-8"))
TAIL = 3.2                                   # 마지막 컷(얼음 위 흰 곰)을 보여 줄 여유
END = round(SENT[-1][1] + TAIL, 2)
f = Film("whitebear", a.art, a.voice / "words.json", END)
art = f.art
MISS = []


def T(i, fr=0.0):
    s0, s1 = SENT[i][0], SENT[i][1]
    return s0 + (s1 - s0) * fr


def E(i):
    return SENT[i][1]


def W(word, i):
    try:
        t = f.cue(word, after=T(i) - 1.2)   # 받아쓰기 시각이 문장 시작보다 조금 앞설 때가 있음
        if t <= E(i) + 0.3:
            return t
    except KeyError:
        pass
    MISS.append(f"{i}:{word}")
    return T(i)


CUR = [None]


def go(t, sid, how="cut", d=0.5):
    if sid == CUR[0]:
        return
    f._show(t, sid, how, d, CUR[0])
    CUR[0] = sid


INK, RED, CREAM, GOLD, DIM = "#2b2118", "#b8432f", "#f3efe6", "#e6b85c", "#9c968a"
NID = [0]


def note(s, text, x, y, t, size=78, color=INK, rot=-3, card=True, how="write", font="pen"):
    """원화 위 손글씨 쪽지 (설명 자리 — 그림 위에 얹음)."""
    NID[0] += 1
    tid = f"n{NID[0]}"
    s.text(tid, text, x, y, size=size, color=color, rot=rot, card=card, font=font)
    f._enter(t, tid, how, min(1.0, 0.05 * len(text) + 0.3))
    return tid


def tag(s, text, t):
    """'재구성 · 가상의 인물' 같은 작은 표시 (12 §1)."""
    return note(s, text, 1700, 40, t, size=34, color="#5a5146", rot=0, how="fade")


# ───────────────────────────────── 장면 판 (원화 한 장 = 한 컷, 카메라 고정)
S = {}
for sheet in ("night", "lab", "lab2", "mind", "end"):
    for k in range(1, 5):
        S[f"{sheet}-{k}"] = f.set(f"{sheet}{k}", f"{sheet}-{k}.png", focus=(960, 540, 1.0))
S["night-1b"] = f.set("night1b", "night-1.png", focus=(960, 540, 1.0))    # 마지막 장에서 같은 방으로 돌아옴 (되짚기)
S["mind-1b"] = f.set("mind1b", "mind-1.png", focus=(960, 540, 1.0))      # 일꾼이 지쳤을 때 (색을 빼서)

# ───────────────────────────────── 검은 화면 (마디)
blk = f.set("blk", "black.png", focus=(960, 540, 1.0))
BL = {}


def bline(tid, text, y=500, size=76, color=CREAM):
    blk.text(tid, text, 960, y, size=size, color=color, font="serif", rot=0, shadow=False)
    BL[tid] = text


def bshow(t, tid):
    f._enter(t, tid, "write", min(1.6, 0.06 * len(BL[tid]) + 0.3))


def bhide(t, tids):
    for tid in tids:
        f._leave(t, tid, "fade", .3)


CH = {2: "잠들기 전 10분", 3: "종을 울린 사람들", 4: "머릿속 두 일꾼", 5: "빨간 폭스바겐", 6: "다시, 밤 11시 40분"}
for n, ttl in CH.items():
    blk.text(f"chn{n}", f"{n - 1}", 960, 380, size=60, color=GOLD, font="serif", rot=0, shadow=False)
    blk.text(f"cht{n}", ttl, 960, 470, size=96, color=CREAM, font="serif", rot=0, shadow=False)


def chapter(n, i_first, hold=1.2):
    t = T(i_first) - 1.45
    go(t, "blk", "dissolve", .4)
    f._enter(t + .2, f"chn{n}", "fade", .3)
    f._enter(t + .3, f"cht{n}", "write", .7)
    f._leave(T(i_first) + hold - .3, f"chn{n}", "fade", .3)
    f._leave(T(i_first) + hold - .3, f"cht{n}", "fade", .3)
    return T(i_first) + hold


# ───────────────────────────────── 0. 흰 곰을 떠올리지 마세요 (마디)
bline("q0", "흰 곰을 떠올리지 마세요.")
go(0.0, "blk", "cut")
bshow(T(0) + .05, "q0")
bhide(E(0) + .8, ["q0"])

# ───────────────────────────────── 1장. 잠들기 전 10분 (이야기)
t = chapter(2, 1)
go(t, "night1", "dissolve", .6)
tag(S["night-1"], "재구성 · 가상의 인물", t + .3)
note(S["night-1"], "밤 11:40", 330, 140, W("40분", 1), size=90)
go(T(3), "night4", "cut")                                    # 휴대폰을 뒤집는 손 — 내일 아침 9시
note(S["night-4"], "내일 9:00 · 첫 발표", 520, 150, W("9시", 3), size=80)
go(T(4), "night2", "cut")                                    # '그만하자' → 눈을 감음
go(T(6), "night3", "cut")                                    # 그런데 — 천장을 보는 눈
n3 = S["night-3"]
note(n3, "첫 문장", 360, 220, W("첫", 7), size=74, rot=-5)
note(n3, "멈춘 화면", 1520, 300, W("멈출", 7), size=74, rot=4)
note(n3, "사람들의 얼굴", 460, 820, W("얼굴", 7), size=74, rot=-2)
note(n3, "또…", 1500, 800, W("더", 8), size=90, color=RED, rot=3)

# ───────────────────────────────── 2장. 종을 울린 사람들 (이야기 → 설명 → 증거)
t = chapter(3, 10)
go(t, "lab1", "dissolve", .6)
tag(S["lab-1"], "재구성 · 1987년 실험", t + .3)
note(S["lab-1"], "1987 · 샌안토니오", 420, 140, W("1987", 10) + .1, size=80)
go(T(12), "lab2", "cut")                                     # 책상 위 종
go(T(13), "lab24", "cut")                                    # 연구자의 손 · 초시계 — 지시는 간단
go(T(14), "lab3", "cut")                                     # 말하는 참가자
note(S["lab-3"], "5분", 1640, 170, W("5분", 14), size=110)
note(S["lab-3"], "흰 곰 ✕", 1600, 330, W("흰", 15), size=92, color=RED)
go(T(16), "lab4", "cut")                                     # 종을 누르는 손
note(S["lab-4"], "띵", 1450, 260, W("울릴", 16), size=120, color=RED, rot=-8)

# 칸 만화 ① — 참으라고 한 5분 (설명)
pg1 = Page(f, "pg1")
pg1.panel("p1a", 80, 160, 560, 760, "lab2-2.png", crop=(0.5, 0.5, 1.0), caption="참으라고 한 5분")
s1 = pg1.s
s1.raw('<div id="bar1" style="position:absolute;left:720px;top:600px;width:1100px;height:14px;background:#2b2118;border-radius:7px;opacity:0"></div>')
for m in range(6):
    s1.text(f"tk{m}", f"{m}분", 720 + m * 220, 640, size=44, color="#5a5146", font="gothic", rot=0, shadow=False)
BELLS = [760, 900, 1010, 1180, 1330, 1450, 1620, 1760]
for k, x in enumerate(BELLS):
    s1.prop(f"b1_{k}", "bell", x, 470 - (k % 2) * 40, 120, z=8)
go(T(17), "pg1", "dissolve", .5)
pg1.draw(T(17) + .2, "p1a")
f._enter(T(17) + .6, "bar1", "fade", .5)
for m in range(6):
    f._enter(T(17) + .7 + m * .08, f"tk{m}", "fade", .3)
for k in range(len(BELLS)):
    f._enter(T(19) + k * (E(19) - T(19)) / len(BELLS), f"b1_{k}", "pop", .45)
note(s1, "1분에 1번 넘게", 1270, 230, W("1분", 20), size=96, color=RED)

go(T(21), "lab21", "cut")                                    # 다음 5분 — 편해진 참가자
note(S["lab2-1"], "이제 생각해도 됨", 1450, 180, W("이제", 22), size=80)

# 칸 만화 ② — 두 줄(세 줄) 비교: 종의 수는 그림 표현, 논문 요약의 '더 많이/덜'만 (수치 아님)
pg2 = Page(f, "pg2")
s2 = pg2.s
ROWS = [("처음부터 생각한 사람", 3, 230), ("먼저 억누른 사람", 7, 500), ("빨간 차를 정해 둔 사람", 4, 770)]
for r, (lab, n, y) in enumerate(ROWS):
    s2.text(f"rl{r}", lab, 380, y - 40, size=56, color=INK, font="gothic", rot=0, shadow=False, card=True)
    for k in range(n):
        s2.prop(f"b2_{r}_{k}", "bell", 760 + k * 150, y, 110, z=8)
s2.prop("vwp", "vw", 230, 830, 220, z=8)
s2.text("rnote", "종의 개수는 그림 표현 · 논문은 '더 많이 / 덜'로 비교", 960, 960, size=34, color="#5a5146", font="gothic", rot=0, shadow=False)
go(T(23), "pg2", "dissolve", .5)
f._enter(T(23) + .2, "rnote", "fade", .4)
f._enter(W("처음부터", 23), "rl0", "fade", .4)
for k in range(3):
    f._enter(W("처음부터", 23) + .5 + k * .25, f"b2_0_{k}", "pop", .4)
f._enter(W("먼저", 23), "rl1", "fade", .4)
for k in range(7):
    f._enter(W("먼저", 23) + .4 + k * .22, f"b2_1_{k}", "pop", .4)
note(s2, "반동 효과", 1640, 420, W("반동", 25), size=96, color=RED)

# 증거 — 논문 첫 장 (스포트라이트)
doc = f.set("doc", "paperdoc.png", focus=(960, 540, 1.0))
bx = [int(v) for v in (art / "paperdoc.box").read_text().split()] if (art / "paperdoc.box").exists() else [210, 300, 1500, 480]
SPOT = {"title": [0, 0, 1, .45], "fail": [.06, .52, .92, .16], "reb": [.06, .64, .92, .15], "dis": [.06, .83, .92, .16]}
for k, (x, y, w, h) in SPOT.items():
    X, Y, Wd, Ht = bx[0] + x * bx[2] - 12, bx[1] + y * bx[3] - 8, w * bx[2] + 24, h * bx[3] + 16
    doc.raw(f'<div id="sp_{k}" style="position:absolute;left:{X:.0f}px;top:{Y:.0f}px;width:{Wd:.0f}px;height:{Ht:.0f}px;'
            f'box-shadow:0 0 0 3000px rgba(8,8,10,.62);border:5px solid #e6b85c;border-radius:10px;opacity:0"></div>', z=8)
doc.text("doctag", "Wegner, Schneider, Carter & White (1987) · JPSP 53(1) · 저자 공개 PDF", 960, 1010, size=30,
         color="#d9d2c4", font="gothic", rot=0, shadow=False)
go(T(26), "doc", "dissolve", .5)
f._enter(T(26) + .3, "doctag", "fade", .4)
f._enter(W("생각", 26), "sp_title", "fade", .4)
f._leave(T(28) - .1, "sp_title", "fade", .3)
f._enter(T(28), "sp_fail", "fade", .4)
f._leave(W("억누른", 28) + .2, "sp_fail", "fade", .3)
f._enter(W("억누른", 28) + .2, "sp_reb", "fade", .4)

bline("q29", "그럼 왜, 참으려 할수록 더 떠오를까요?")
go(T(29) - .2, "blk", "dissolve", .4)
bshow(T(29), "q29")
bhide(E(29) + .3, ["q29"])

# ───────────────────────────────── 3장. 머릿속 두 일꾼 (이야기 + 그림 위 설명)
t = chapter(4, 30)
go(t, "mind1", "dissolve", .6)
tag(S["mind-1"], "비유 · 웨그너의 설명을 그림으로", t + .3)
go(T(32), "mind2", "cut")
note(S["mind-2"], "다른 생각 찾기", 1450, 170, W("찾아", 32), size=80)
go(T(34), "mind3", "cut")
note(S["mind-3"], "흰 곰 없나?", 1450, 190, W("확인", 35), size=86)
go(T(36), "mind4", "cut")
note(S["mind-4"], "확인하기 = 떠올리기", 960, 900, W("셈", 37) - .3, size=96, color=RED, rot=-2)
go(T(38), "mind1b", "cut")                                   # 찾는 일꾼이 지치면 — 색을 빼서
f._setv(T(38), "#mind1b", {"filter": "saturate(1) brightness(1)"})   # 시작값이 없으면 밝기 0 에서 시작해 검게 깜빡임
f._grade(T(38) + .2, "mind1b", "saturate(.25) brightness(.8)", 1.2)
go(T(39), "mind4", "cut")                                    # 흰 곰이 그대로 떠오름 (되짚기)
note(S["mind-4"], "피곤할 때 · 머리가 바쁠 때", 960, 150, W("피곤", 40), size=74, rot=1)

bline("q41", "그렇다면, 방법은 없을까요?")
go(T(41) - .2, "blk", "dissolve", .4)
bshow(T(41), "q41")
bhide(E(41) + .3, ["q41"])

# ───────────────────────────────── 4장. 빨간 폭스바겐 (이야기 → 설명 → 증거)
t = chapter(5, 42)
go(t, "lab23", "dissolve", .6)
tag(S["lab2-3"], "재구성 · 같은 논문 두 번째 실험", t + .3)
note(S["lab2-3"], "흰 곰 → 빨간 차", 1450, 900, W("빨간", 43), size=84, color=RED)
go(T(44), "pg2", "dissolve", .5)                             # 칸 만화 ② 로 되짚기 — 세 번째 줄
f._enter(T(44) + .3, "rl2", "fade", .4)
f._enter(T(44) + .4, "vwp", "pop", .5)
for k in range(4):
    f._enter(T(44) + .8 + k * .22, f"b2_2_{k}", "pop", .4)
note(s2, "덜 사로잡힘", 1640, 700, W("줄었", 44), size=90, color=RED)
go(T(45), "doc", "dissolve", .5)
f._leave(T(45), "sp_reb", "fade", .2)
f._enter(T(46), "sp_dis", "fade", .4)

# ───────────────────────────────── 5장. 다시, 밤 11시 40분 (이야기 · 수미상관)
t = chapter(6, 47)
go(t, "night1b", "dissolve", .6)
note(S["night-1b"], "다시, 11:40", 330, 140, t + .3, size=90)
go(T(48), "end1", "dissolve", .6)
note(S["end-1"], "파도 소리", 1460, 160, W("파도", 49), size=88)
go(T(50), "end2", "cut")
note(S["end-2"], "① 대신 놓을 것 하나", 560, 760, T(52), size=78, rot=-2)
note(S["end-2"], "② '하지 마' → '이걸 하자'  (해석)", 640, 880, W("하지", 53), size=66, rot=-1)

bline("q54a", "흰 곰을 지우려 하지 마세요.", y=440)
bline("q54b", "빨간 차를 하나 정해 두세요.", y=560, color=GOLD)
go(T(54) - .2, "blk", "dissolve", .5)
bshow(T(54), "q54a")
bshow(T(55), "q54b")
go(E(55) + .6, "end3", "dissolve", 1.4)                      # 얼음 위를 걸어가는 흰 곰으로 닫음

f.html(a.out)
print("ok", a.out, "END", END, "missing cues:", MISS)
