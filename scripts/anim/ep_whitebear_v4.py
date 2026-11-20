"""호기심 편 「생각하지 않으려 할수록 더 떠오르는 이유」 v4 (약 9분 20초) — 전체 장면.

v3(ep_whitebear.py, 4분)을 사용자 요청("영상길이 좀 더 길게 해줘")으로 늘린 판. 대사는 02_script/narration_v4.md.
화면의 네 자리 (manual/12 §0-1, 04 §0-7):
  이야기 = GPT 이미지 원화(2×2 시트 9장을 자른 완성 프레임, 컷마다 카메라 고정 — 잼 편 방식)
  설명   = 원화 위 손글씨 쪽지 · 칸 만화(5분 막대 위 종, 두 줄 비교, 잠 연구 2×2, 막대 세 개)
  증거   = 루이스 캐럴 사진(1857, 퍼블릭 도메인) · 논문 그림 1 · 논문 표 2 · 논문 첫 장(저자 공개 PDF)
  마디   = 검은 화면 한 줄 · 장 제목(번호 + 장면 이름)

    python scripts/anim/prep_whitebear.py <art> --paper <paper_crop.png>      # 시트 9장 자르기
    python scripts/anim/ep_whitebear_v4.py <art> <voice v4> <out.html>
    bash scripts/anim/render_all.sh <dir> <out.html> <voice>/voice.mp3 <voice>/captions.ass <END> <result.mp4> 4
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from anim import Film  # noqa: E402
from comic import Page, paper  # noqa: E402
from bench_cur import photo_card  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("art", type=Path)
ap.add_argument("voice", type=Path)
ap.add_argument("out", type=Path)
a = ap.parse_args()

SENT = json.loads((a.voice / "sentences.json").read_text(encoding="utf-8"))
TAIL = 3.4
END = round(SENT[-1][1] + TAIL, 2)
f = Film("whitebear4", a.art, a.voice / "words.json", END)
art = f.art
paper(art / "paper.png")
MISS = []


def T(i, fr=0.0):
    s0, s1 = SENT[i][0], SENT[i][1]
    return s0 + (s1 - s0) * fr


def E(i):
    return SENT[i][1]


def W(word, i):
    """문장 i 안에서 그 낱말을 말하기 시작하는 시각 — ElevenLabs 글자별 시각(seg/NNN.align.json) 기준.
    (받아쓰기 words.json 은 뒤로 갈수록 2~3초 앞당겨져 있어 쓰지 않음 — 실제 소리의 침묵 위치로 확인, 2026-11-20)"""
    al = a.voice / "seg" / f"{i:03d}.align.json"
    try:
        d = json.loads(al.read_text(encoding="utf-8"))
        txt = "".join(d["characters"])
        k = txt.find(word)
        if k >= 0:
            return T(i) + d["character_start_times_seconds"][k]
    except (OSError, KeyError, ValueError):
        pass
    MISS.append(f"{i}:{word}")
    return T(i)


CUR = [None]


def go(t, sid, how="cut", d=0.5):
    if sid == CUR[0]:
        return
    f._show(t, sid, how, d, CUR[0])
    CUR[0] = sid


INK, RED, CREAM, GOLD, GREY = "#2b2118", "#b8432f", "#f3efe6", "#e6b85c", "#5a5146"
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
    return note(s, text, 1660, 40, t, size=32, color=GREY, rot=0, how="fade")


def plain(s, tid, text, x, y, size=40, color=GREY, font="gothic"):
    s.text(tid, text, x, y, size=size, color=color, font=font, rot=0, shadow=False, card=True)
    return tid


# ───────────────────────────────── 원화 판 (한 장 = 한 컷, 카메라 고정)
S = {}
for sheet in ("night", "lab", "lab2", "mind", "end", "room", "lab3", "assoc", "sleep"):
    for k in range(1, 5):
        S[f"{sheet}-{k}"] = f.set(f"{sheet}{k}", f"{sheet}-{k}.png", focus=(960, 540, 1.0))
S["night-1b"] = f.set("night1b", "night-1.png", focus=(960, 540, 1.0))
S["night-3b"] = f.set("night3b", "night-3.png", focus=(960, 540, 1.0))
S["mind-1b"] = f.set("mind1b", "mind-1.png", focus=(960, 540, 1.0))
S["mind-4b"] = f.set("mind4b", "mind-4.png", focus=(960, 540, 1.0))
S["lab3-3b"] = f.set("lab33b", "lab3-3.png", focus=(960, 540, 1.0))
S["room-1b"] = f.set("room1b", "room-1.png", focus=(960, 540, 1.0))

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


def bq(i, tid, text, **k):
    """질문 한 줄 (마디)."""
    bline(tid, text, **k)
    go(T(i) - .2, "blk", "dissolve", .4)
    bshow(T(i), tid)
    bhide(E(i) + .3, [tid])


CH = {2: "잠들기 전 10분", 3: "종을 울린 사람들", 4: "녹음기에 남은 것", 5: "방 안의 모든 것이 흰 곰이 된다",
      6: "머릿속 두 일꾼", 7: "서둘러 잠들기", 8: "빨간 폭스바겐", 9: "다시, 밤 11시 40분"}
for n, ttl in CH.items():
    blk.text(f"chn{n}", f"{n - 1}", 960, 380, size=60, color=GOLD, font="serif", rot=0, shadow=False)
    blk.text(f"cht{n}", ttl, 960, 470, size=92, color=CREAM, font="serif", rot=0, shadow=False)


def chapter(n, i_first, hold=1.2):
    t = T(i_first) - 1.45
    go(t, "blk", "dissolve", .4)
    f._enter(t + .2, f"chn{n}", "fade", .3)
    f._enter(t + .3, f"cht{n}", "write", .7)
    f._leave(T(i_first) + hold - .3, f"chn{n}", "fade", .3)
    f._leave(T(i_first) + hold - .3, f"cht{n}", "fade", .3)
    return T(i_first) + hold


def evidence(sid, img, width=1300, bg="black.png", label=""):
    """실제 자료 한 장을 가운데 흰 바탕 카드로 (증거 자리)."""
    s = f.set(sid, bg, focus=(960, 540, 1.0))
    from PIL import Image
    iw, ih = Image.open(art / img).size
    h = width * ih / iw
    if h > 900:
        width, h = width * 900 / h, 900
    s.raw(f'<div style="position:absolute;left:{960 - width / 2 - 18:.0f}px;top:{520 - h / 2 - 18:.0f}px;width:{width + 36:.0f}px;'
          f'height:{h + 36:.0f}px;background:#fcfaf4;box-shadow:0 18px 40px rgba(0,0,0,.45)"><img src="{(art / img).as_uri()}" '
          f'style="position:absolute;left:18px;top:18px;width:{width:.0f}px;height:{h:.0f}px"></div>', z=5)
    if label:
        s.text(f"{sid}_lb", label, 960, 1010, size=30, color="#d9d2c4", font="gothic", rot=0, shadow=False)
    return s, (960 - width / 2, 520 - h / 2, width, h)


def spot(s, sid, box, frac, z=8):
    """증거 위 스포트라이트(나머지는 어둡게)."""
    x, y, w, h = frac
    X, Y, Wd, Ht = box[0] + x * box[2] - 12, box[1] + y * box[3] - 8, w * box[2] + 24, h * box[3] + 16
    s.raw(f'<div id="{sid}" style="position:absolute;left:{X:.0f}px;top:{Y:.0f}px;width:{Wd:.0f}px;height:{Ht:.0f}px;'
          f'box-shadow:0 0 0 3000px rgba(8,8,10,.6);border:5px solid {GOLD};border-radius:10px;opacity:0"></div>', z=z)
    return sid


# ───────────────────────────────── 0. 흰 곰을 떠올리지 마세요 (마디)
bline("q0", "흰 곰을 떠올리지 마세요.")
go(0.0, "blk", "cut")
bshow(T(0) + .05, "q0")
bhide(E(0) + .8, ["q0"])

# ───────────────────────────────── 1장. 잠들기 전 10분 (이야기 → 증거)
t = chapter(2, 1)
go(t, "night1", "dissolve", .6)
tag(S["night-1"], "재구성 · 가상의 인물", t + .3)
note(S["night-1"], "밤 11:40", 330, 140, W("40분", 1), size=90)
go(T(3), "night4", "cut")
note(S["night-4"], "내일 9:00 · 첫 발표", 520, 150, W("9시", 3), size=80)
go(T(4), "night2", "cut")
go(T(6), "night3", "cut")
n3 = S["night-3"]
note(n3, "첫 문장", 360, 220, W("첫", 7), size=74, rot=-5)
note(n3, "멈춘 화면", 1520, 300, W("멈출", 7), size=74, rot=4)
note(n3, "사람들의 얼굴", 460, 820, W("얼굴", 7), size=74, rot=-2)
go(T(8), "room1", "cut")                                     # 몸을 돌려 커튼 쪽으로
go(W("커튼", 9), "room3", "cut")
go(W("천장", 9), "room2", "cut")
go(T(10), "room4", "cut")                                    # 이불을 머리끝까지
note(S["room-4"], "또 발표…", 1450, 200, W("발표", 10), size=86, color=RED, rot=3)

ok_c = photo_card(art / "carroll_src.jpg", art / "carroll_card.png")
car = f.set("carroll", "paper.png", focus=(960, 540, 1.0))
if ok_c:
    car.prop("ph_car", "carroll_card", 560, 520, 470, z=8, rot=-3)
plain(car, "car_lb", "루이스 캐럴 (1832–1898) · 1857년 사진 · 퍼블릭 도메인", 560, 900, size=30)
car.text("car_q1", "\"더는 생각하지 않겠다!", 1330, 330, size=74, color=INK, font="pen", rot=-2, card=True)
car.text("car_q2", "다른 걸 생각하겠다!\"", 1330, 450, size=74, color=INK, font="pen", rot=-2, card=True)
car.text("car_q3", "…10분쯤 지나면, 다시 그 일 한가운데", 1330, 620, size=64, color=RED, font="pen", rot=-1, card=True)
plain(car, "car_src", "『Curiosa Mathematica』(1893) — Wenzlaff & Wegner(2000) 리뷰의 첫머리 인용", 1330, 790, size=28)
go(T(12), "carroll", "dissolve", .6)
if ok_c:
    f._enter(T(12) + .3, "ph_car", "pop", .6)
f._enter(T(12) + .8, "car_lb", "fade", .4)
f._enter(W("1893", 13), "car_src", "fade", .4)
f._enter(T(15), "car_q1", "write", .9)
f._enter(W("다른", 15), "car_q2", "write", .9)
f._enter(W("10분", 16), "car_q3", "write", 1.0)
bq(17, "q17", "생각하지 않으려 할수록 더 떠오르는 일.")

# ───────────────────────────────── 2장. 종을 울린 사람들 (이야기)
t = chapter(3, 19)
go(t, "lab1", "dissolve", .6)
tag(S["lab-1"], "재구성 · 1987년 실험", t + .3)
note(S["lab-1"], "1987 · 샌안토니오", 420, 140, W("1987", 19) + .1, size=80)
note(S["lab-1"], "학생 34명 (남 14 · 여 20)", 1420, 900, W("서른네", 20), size=66)
go(T(22), "lab2", "cut")                                     # 책상 위 녹음기와 종
go(T(23), "lab31", "cut")                                    # 녹음 버튼
note(S["lab3-1"], "5분 · 떠오르는 것 전부 소리 내어", 960, 900, W("5분", 24), size=70)
go(T(25), "lab32", "cut")                                    # 실험자가 나가며 문을 닫음
note(S["lab3-2"], "\"시작\"", 1500, 200, W("시작", 25), size=90)
go(T(26), "lab24", "cut")                                    # 실험자의 손 · 초시계
go(T(27), "lab3", "cut")                                     # 말하는 학생
note(S["lab-3"], "흰 곰 ✕", 1600, 220, W("흰", 27), size=96, color=RED)
go(T(28), "lab4", "cut")                                     # 종을 누르는 손
note(S["lab-4"], "띵", 1450, 260, W("울려", 28), size=120, color=RED, rot=-8)
go(T(29), "lab33", "cut")                                    # 혼자 남은 학생
note(S["lab3-3"], "학생 · 녹음기 · 종", 1480, 180, W("학생과", 29), size=72)

# ───────────────────────────────── 3장. 녹음기에 남은 것 (설명 → 이야기 → 증거)
t = chapter(4, 30)
pg1 = Page(f, "pg1")
pg1.panel("p1a", 80, 160, 560, 760, "lab2-2.png", crop=(0.5, 0.5, 1.0), caption="참으라고 한 5분")
s1 = pg1.s
s1.raw('<div id="bar1" style="position:absolute;left:720px;top:600px;width:1100px;height:14px;background:#2b2118;border-radius:7px;opacity:0"></div>')
for m in range(6):
    s1.text(f"tk{m}", f"{m}분", 720 + m * 220, 640, size=44, color=GREY, font="gothic", rot=0, shadow=False, card=True)
BELLS = [760, 900, 1010, 1180, 1330, 1450, 1620, 1760]
for k, x in enumerate(BELLS):
    s1.prop(f"b1_{k}", "bell", x, 470 - (k % 2) * 40, 120, z=8)
go(t, "pg1", "dissolve", .5)
pg1.draw(t + .2, "p1a")
f._enter(t + .6, "bar1", "fade", .5)
for m in range(6):
    f._enter(t + .7 + m * .08, f"tk{m}", "fade", .3)
for k in range(len(BELLS)):
    f._enter(T(32) + k * (E(32) - T(32)) / len(BELLS), f"b1_{k}", "pop", .45)
note(s1, "1분에 1번 넘게", 1270, 230, W("1분", 32), size=96, color=RED)

go(T(33), "lab31", "cut")                                    # 녹음을 다시 들음
go(T(34), "lab34", "cut")                                    # 두리번거리는 학생
note(S["lab3-4"], "\"좋아, 그럼 다른 걸 생각하자\"", 960, 900, T(35), size=72)
go(T(36), "lab33b", "cut")                                   # 말이 멈춘 순간
note(S["lab3-3b"], "말이 멈출 때", 1480, 180, W("멈추는", 37), size=80)
note(S["lab3-3b"], "흰 곰", 1480, 320, W("비는", 38), size=110, color=RED, rot=4)

go(T(39), "lab21", "cut")
note(S["lab2-1"], "이제 생각해도 됨", 1450, 180, W("이제", 41), size=80)

pg2 = Page(f, "pg2")
s2 = pg2.s
ROWS = [("처음부터 생각한 학생", 3, 260), ("먼저 참은 학생", 7, 560), ("빨간 차를 정해 둔 학생", 4, 860)]
for r, (lab, n, y) in enumerate(ROWS):
    plain(s2, f"rl{r}", lab, 380, y - 40, size=56, color=INK)
    for k in range(n):
        s2.prop(f"b2_{r}_{k}", "bell", 760 + k * 150, y, 110, z=8)
s2.prop("vwp", "vw", 230, 890, 220, z=8)
plain(s2, "rnote", "종의 개수는 그림 표현 · 실제 수치는 뒤의 논문 표", 960, 1010, size=30)
go(T(42), "pg2", "dissolve", .5)
f._enter(T(42) + .2, "rnote", "fade", .4)
f._enter(W("처음부터", 42), "rl0", "fade", .4)
for k in range(3):
    f._enter(W("처음부터", 42) + .5 + k * .25, f"b2_0_{k}", "pop", .4)
f._enter(W("나머지", 42), "rl1", "fade", .4)
for k in range(7):
    f._enter(T(43) + .3 + k * .25, f"b2_1_{k}", "pop", .4)

fig, fb = evidence("fig1", "ev_fig1.png", width=1050, label="Wegner 외(1987) 그림 1 — 분당 종소리, 5분 동안 · 저자 공개 PDF")
fig.text("fig_n1", "참은 뒤에 생각한 5분 → 갈수록 더 잦아짐", 1500, 170, size=58, color=RED, font="pen", rot=-2, card=True)
fig.text("fig_n2", "다른 5분들 → 갈수록 뜸해짐", 1500, 860, size=54, color=INK, font="pen", rot=-1, card=True)
go(T(44), "fig1", "dissolve", .5)
f._enter(T(44) + .4, "fig1_lb", "fade", .4)
f._enter(W("뜸해", 45), "fig_n2", "write", .8)
f._enter(W("잦아", 45), "fig_n1", "write", .9)
note(fig, "반동 효과", 1500, 330, W("반동", 47), size=96, color=RED)

doc, db = evidence("doc", "paper_crop.png", width=1500, label="Wegner, Schneider, Carter & White (1987) · JPSP 53(1) · 저자 공개 PDF")
spot(doc, "sp_title", db, [0, 0, 1, .45])
spot(doc, "sp_fail", db, [.06, .52, .92, .16])
spot(doc, "sp_reb", db, [.06, .64, .92, .15])
spot(doc, "sp_dis", db, [.06, .83, .92, .16])
go(T(48), "doc", "dissolve", .5)
f._enter(T(48) + .3, "doc_lb", "fade", .4)
f._enter(W("생각", 48), "sp_title", "fade", .4)
f._leave(T(50) - .1, "sp_title", "fade", .3)
f._enter(T(50), "sp_fail", "fade", .4)
f._leave(W("억누른", 50) + .2, "sp_fail", "fade", .3)
f._enter(W("억누른", 50) + .2, "sp_reb", "fade", .4)
bq(51, "q51", "그럼 왜, 참으려 할수록 더 떠오를까요?")

# ───────────────────────────────── 4장. 방 안의 모든 것이 흰 곰이 된다 (이야기 + 설명)
t = chapter(5, 52)
go(t, "lab31", "dissolve", .6)
go(T(53), "lab34", "cut")
l34 = S["lab3-4"]
note(l34, "벽", 380, 230, W("벽", 54), size=96)
note(l34, "의자", 1520, 300, W("의자", 54), size=96)
note(l34, "옷", 1500, 820, W("옷", 54), size=96)
go(T(56), "assoc1", "cut")
a1 = S["assoc-1"]
tag(a1, "비유 · 1987년 논문의 설명을 그림으로", T(56) + .2)
note(a1, "벽 →", 520, 300, W("벽", 57), size=90)
note(a1, "의자 →", 960, 560, W("의자", 57), size=90)
note(a1, "옷 → …", 1400, 820, W("옷", 57), size=90)
go(T(58), "assoc2", "dissolve", .8)                           # 사물마다 흰 곰 그림자
note(S["assoc-2"], "모두 흰 곰의 신호", 960, 140, W("신호", 59) if True else T(59), size=92, color=RED)
go(T(60), "assoc3", "dissolve", .8)                           # 지우의 방 — 커튼·천장에 발표
note(S["assoc-3"], "커튼 · 천장 = 발표의 신호", 960, 900, W("커튼", 61), size=80, color=RED)

# ───────────────────────────────── 5장. 머릿속 두 일꾼 (이야기 + 그림 위 설명)
t = chapter(6, 62)
go(t, "mind1", "dissolve", .6)
tag(S["mind-1"], "비유 · 웨그너의 아이러니 과정 이론(1994)", t + .3)
go(T(64), "mind2", "cut")
note(S["mind-2"], "애써서 · 의식적으로", 1450, 170, W("애써서", 65), size=80)
go(T(67), "mind3", "cut")
note(S["mind-3"], "의식하지 못하는 사이에", 1400, 180, W("의식하지", 68), size=76)
go(T(69), "mind4", "cut")
note(S["mind-4"], "확인하기 = 떠올리기", 960, 900, W("셈", 70) - .3, size=96, color=RED, rot=-2)
go(T(71), "mind2", "cut")
go(T(72), "mind1b", "cut")
f._grade(T(72) + .2, "mind1b", "saturate(.25) brightness(.8)", 1.2)
go(W("흰", 72), "mind4b", "cut")
go(T(73), "mind3", "cut")
note(S["mind-3"], "일꾼이 멈춘 뒤에도 남는 경비원", 960, 900, W("남아", 73), size=74, color=RED)

# ───────────────────────────────── 6장. 서둘러 잠들기 (이야기 → 설명 → 증거 서지)
t = chapter(7, 75)
go(t, "sleep1", "dissolve", .6)
tag(S["sleep-1"], "재구성 · 1996년 연구", t + .3)
note(S["sleep-1"], "\"최대한 빨리 잠드세요\"", 520, 160, W("최대한", 77), size=72)
note(S["sleep-1"], "\"잠이 오면 그때 주무세요\"", 1400, 900, W("잠이", 77), size=72)
pg3 = Page(f, "pg3")
s3 = pg3.s
GX, GY, CW, CHH = 520, 230, 640, 300
for j, h in enumerate(["잔잔한 음악", "수자의 행진곡"]):
    plain(s3, f"gh{j}", h, GX + CW / 2 + j * (CW + 30), GY - 70, size=48, color=INK)
for r, h in enumerate(["\"빨리 잠드세요\"", "\"잠 오면 주무세요\""]):
    plain(s3, f"gr{r}", h, 260, GY + CHH / 2 + r * (CHH + 30) - 30, size=44, color=INK)
CELLS = {(0, 0): ("더 빨리 잠듦", "#2e7d4f"), (0, 1): ("더 늦게 잠듦", RED), (1, 0): ("", INK), (1, 1): ("", INK)}
for (r, c), (txt, col) in CELLS.items():
    x, y = GX + c * (CW + 30), GY + r * (CHH + 30)
    s3.raw(f'<div id="gc{r}{c}" style="position:absolute;left:{x}px;top:{y}px;width:{CW}px;height:{CHH}px;border:6px solid #2b2118;'
           f'border-radius:12px;background:rgba(255,253,247,.9);opacity:0"></div>', z=6)
    if txt:
        s3.text(f"gt{r}{c}", txt, x + CW / 2, y + CHH / 2 - 50, size=82, color=col, font="pen", rot=-2, card=True)
plain(s3, "g_src", "Ansfield, Wegner & Bowser (1996) · Behaviour Research and Therapy 34(7) · 초록 기준", 960, 1010, size=30)
go(T(78), "pg3", "dissolve", .5)
for k, el in enumerate(["gc00", "gc01", "gc10", "gc11"]):
    f._enter(T(78) + .2 + k * .15, el, "fade", .4)
f._enter(T(78) + .4, "gr0", "fade", .4)
f._enter(T(78) + .5, "gr1", "fade", .4)
f._enter(W("잔잔한", 79), "gh0", "fade", .4)
f._enter(W("행진곡", 79), "gh1", "fade", .4)
f._enter(T(79) + .5, "g_src", "fade", .4)
f._enter(W("빨리", 80), "gt00", "write", .8)
go(T(81), "sleep3", "cut")                                    # 행진곡 — 긴장한 얼굴
go(T(82), "pg3", "cut")
f._enter(T(82) + .2, "gt01", "write", .8)
go(T(83), "room4", "cut")                                     # 지우처럼
bq(84, "q84", "그렇다면, 방법은 없을까요?")

# ───────────────────────────────── 7장. 빨간 폭스바겐 (이야기 → 설명 → 증거)
t = chapter(8, 85)
go(t, "lab24", "dissolve", .6)
tag(S["lab2-4"], "재구성 · 같은 논문 두 번째 실험", t + .3)
note(S["lab2-4"], "세 무리", 1450, 200, W("세", 86), size=96)
go(T(89), "lab23", "cut")
note(S["lab2-3"], "흰 곰 → 빨간 폭스바겐", 1400, 900, W("빨간", 89), size=80, color=RED)
go(T(90), "pg2", "dissolve", .5)                              # 칸 만화 ② 로 되짚기 — 세 번째 줄
f._enter(T(90) + .3, "rl2", "fade", .4)
f._enter(T(90) + .4, "vwp", "pop", .5)
for k in range(4):
    f._enter(T(91) + k * .25, f"b2_2_{k}", "pop", .4)
note(s2, "참는 5분: 비슷", 1640, 140, W("비슷", 91), size=72)

tab, tb = evidence("tab2", "ev_tab2.png", width=1200, label="Wegner 외(1987) 표 2 — 생각해도 되는 5분(Expression)의 흰 곰 횟수 · 저자 공개 PDF")
spot(tab, "sp_tab", tb, [.66, .3, .32, .22])
go(T(92), "tab2", "dissolve", .5)
f._enter(T(92) + .4, "tab2_lb", "fade", .4)
f._enter(W("5분에", 92), "sp_tab", "fade", .4)

bars = f.set("bars", "paper.png", focus=(960, 540, 1.0))
BARS = [("처음부터 생각", 15.47, "#5a6b8c"), ("먼저 참음", 34.05, RED), ("빨간 차를 정해 둠", 21.00, "#c98a2b")]
BASE, SCALE = 860, 17.0
for k, (lab, v, col) in enumerate(BARS):
    x = 520 + k * 440
    bars.raw(f'<div id="bar_{k}" style="position:absolute;left:{x - 110}px;top:{BASE}px;width:220px;height:0px;background:{col};'
             f'border-radius:10px 10px 0 0;box-shadow:0 6px 14px rgba(0,0,0,.18)"></div>', z=6)
    bars.counter(f"bv_{k}", x, BASE - v * SCALE - 110, size=86, color=col, font="serif")
    plain(bars, f"bl_{k}", lab, x, BASE + 30, size=46, color=INK)
bars.raw(f'<div style="position:absolute;left:300px;top:{BASE}px;width:1320px;height:6px;background:#2b2118"></div>', z=7)
plain(bars, "bars_t", "생각해도 되는 5분 동안 흰 곰 횟수 (평균)", 960, 90, size=50, color=INK)
plain(bars, "bars_s", "Wegner 외(1987) 표 2", 960, 1010, size=30)
go(T(93), "bars", "dissolve", .4)
f._enter(T(93) + .2, "bars_t", "fade", .4)
f._enter(T(93) + .3, "bars_s", "fade", .4)
for k, (lab, v, col) in enumerate(BARS):
    tk = (W("처음부터", 93), W("먼저", 93), W("빨간", 94))[k]
    f._enter(tk, f"bl_{k}", "fade", .3)
    f._setv(tk, f"#bar_{k}", {"top": f"{BASE}px"})
    f._tween(tk, f"#bar_{k}", {"height": f"{v * SCALE:.0f}px", "top": f"{BASE - v * SCALE:.0f}px"}, 1.1, "power2.out")
    f._count(tk, f"bv_{k}", 0, v, 1.1, "", "", 2)
note(bars, "반동 ↓", 1500, 330, W("줄어든", 95), size=96, color=RED)
go(T(96), "assoc4", "cut")                                    # 빨간 차 하나
note(S["assoc-4"], "신호는 하나로", 960, 160, W("하나만", 97) if True else T(97), size=96, color=RED)
go(T(98), "doc", "dissolve", .5)
f._leave(T(98), "sp_reb", "fade", .2)
f._enter(T(99), "sp_dis", "fade", .4)

# ───────────────────────────────── 8장. 다시, 밤 11시 40분 (이야기 → 설명)
t = chapter(9, 100)
go(t, "night1b", "dissolve", .6)
note(S["night-1b"], "다시, 11:40", 330, 140, t + .3, size=90)
go(T(101), "end1", "dissolve", .6)
note(S["end-1"], "파도 소리", 1460, 160, W("파도", 102), size=88)
go(T(103), "room1b", "cut")
note(S["room-1b"], "커튼 · 천장 ✕ → 파도 소리 하나", 960, 900, W("파도", 103), size=74, color=RED)
go(T(104), "end2", "dissolve", .6)
e2 = S["end-2"]
note(e2, "① 대신 놓을 것 하나 — 하나로", 600, 640, T(106), size=70, rot=-2)
note(e2, "② 머리가 바쁠 때 재촉하지 않기 (해석)", 640, 760, T(108), size=62, rot=-1)
note(e2, "③ '하지 마' → '이걸 하자' (해석)", 600, 880, T(110), size=62, rot=-2)

bline("qa", "흰 곰을 지우려 하지 마세요.", y=440)
bline("qb", "빨간 차를 하나 정해 두세요.", y=560, color=GOLD)
go(T(112) - .2, "blk", "dissolve", .5)
bshow(T(112), "qa")
bshow(T(113), "qb")
go(E(113) + .6, "end3", "dissolve", 1.4)                      # 얼음 위를 걸어가는 흰 곰으로 닫음

f.html(a.out)
print("ok", a.out, "END", END, "missing cues:", MISS)
