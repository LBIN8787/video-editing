"""호기심 편 「기억은 꺼낼 때마다 다시 쓰인다」(projects/20261118-curiosity-next) — 전체 장면.

화면의 자리(manual/04 §0-7, docs/47): 이야기 = 셀 애니메이션 원화, 증거 = 실제 기록 사진(퍼블릭 도메인),
실험 = 칸 만화(실험 순서 = 칸 순서), 정리·질문 = 검은 화면 한 줄. 실제 사건 당사자의 얼굴은 그리지 않는다.
시각은 대본 문장(sentences.json, 초안 목소리를 문장마다 이어 붙인 정확한 시각) 기준 + 필요할 때만 낱말.

    python scripts/anim/ep_memory.py <art 폴더(curiosity)> <voice 폴더> <out.html> [--refs <사진 폴더>]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from anim import Film  # noqa: E402
from comic import Page  # noqa: E402
from bench_cur import black, photo_card  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("art", type=Path)
ap.add_argument("voice", type=Path)
ap.add_argument("out", type=Path)
ap.add_argument("--refs", type=Path, default=Path("G:/내 드라이브/ytflow/refs/people"))
a = ap.parse_args()

SENT = json.loads((a.voice / "sentences.json").read_text(encoding="utf-8"))
END = round(SENT[-1][1] + 1.6, 2)
f = Film("memory", a.art, a.voice / "words.json", END)
art = f.art


def T(i, fr=0.0):
    s0, s1 = SENT[i][0], SENT[i][1]
    return s0 + (s1 - s0) * fr


def E(i):
    return SENT[i][1]


def W(word, i, end=False):
    """문장 i 안의 낱말 시각(받아쓰기). 못 찾으면 문장 시작."""
    try:
        t = f.cue(word, after=T(i) - 0.15, end=end)
        if t <= E(i) + 0.3:
            return t
    except KeyError:
        pass
    MISS.append(f"{i}:{word}")
    return T(i)


MISS = []


CUR = [None]


def go(t, sid, how="dissolve", d=0.6):
    if sid == CUR[0]:   # 같은 장면으로 '전환'하면 자기 자신을 숨겨 버림 → 건너뜀
        return
    f._show(t, sid, how, d, CUR[0])
    CUR[0] = sid


def foot(s, fr=0.92):
    return min(s.ph * fr, s.ph / 2 + 500)


def top(s, dy=120):
    return s.ph / 2 - 540 + dy


# ───────────────────────────────── 검은 화면 (질문·정리·장 제목)
black(art)
blk = f.set("blk", "black.png", focus=(960, 540, 1.0))
CREAM, GOLD, DIM = "#f3efe6", "#e6b85c", "#9c968a"
BL = {}


def bline(tid, text, y=500, size=72, color=CREAM, font="serif"):
    blk.text(tid, text, 960, y, size=size, color=color, font=font, rot=0, shadow=False)
    BL[tid] = text


def bshow(t, tids, dur=None):
    for k, tid in enumerate(tids):
        f._enter(t + k * 0.0, tid, "write", dur or min(1.6, 0.06 * len(BL[tid]) + 0.3))


def bhide(t, tids):
    for tid in tids:
        f._leave(t, tid, "fade", .25)


CH = ["종이 한 장", "녹화가 아니다", "단어 하나", "없던 사건까지", "뇌 안에서 일어나는 일",
      "왜 이렇게 만들어졌을까", "확신이라는 착각", "확신이 치른 대가", "우리가 할 수 있는 것", "다시, 그 종이"]
for n, ttl in enumerate(CH, 1):
    blk.text(f"chn{n}", f"{n}", 960, 380, size=60, color=GOLD, font="serif", rot=0, shadow=False)
    blk.text(f"cht{n}", ttl, 960, 470, size=96, color=CREAM, font="serif", rot=0, shadow=False)


def chapter(n, i_first, hold=1.3):
    """장 사이 쉼(1.6초)에 검은 화면 + 장 제목. 반환: 다음 장면으로 넘어갈 시각."""
    t = T(i_first) - 1.45
    go(t, "blk", "dissolve", .4)
    f._enter(t + .2, f"chn{n}", "fade", .3)
    f._enter(t + .3, f"cht{n}", "write", .7)
    f._sound(t + .2, "whoosh-short", .1)
    f._leave(T(i_first) + hold - .3, f"chn{n}", "fade", .3)
    f._leave(T(i_first) + hold - .3, f"cht{n}", "fade", .3)
    return T(i_first) + hold


# ───────────────────────────────── 1. 종이 한 장
sky = f.set("sky", "sky86.png")
sky.text("d0", "1986년 1월 28일", 520, top(sky, 120), size=88, rot=-2)
sky.text("d0b", "미국 플로리다", 520, top(sky, 230), size=60, rot=-2)
ok_ch = photo_card(a.refs / "challenger.jpg", art / "photo_challenger.png")
if ok_ch:
    sky.prop("ph_ch", "photo_challenger", 1380, sky.ph * 0.42 - 20, 520, z=9, rot=3)
    sky.text("ph_chn", "챌린저호 · 1986.1.28 · 사진 NASA", 1380, sky.ph * 0.42 + 230, size=30, font="gothic", rot=0, card=True)
go(0, "sky", "cut")
f._setv(0, "#sky", {"opacity": 0})
f._tween(0, "#sky", {"opacity": 1}, 1.2)
f._cam(0, "sky", sky.pw / 2, sky.ph * 0.62, 1.25, 0.1)
f._cam(0.2, "sky", sky.pw / 2, sky.ph * 0.42, 1.05, 6.0, "sine.inOut")
f._enter(0.6, "d0", "write", 1.0)
f._enter(1.6, "d0b", "write", .6)
if ok_ch:
    t = T(0, .82)
    f._enter(t, "ph_ch", "drop", .7)
    f._enter(t + .4, "ph_chn", "write", .6)
    f._sound(t + .6, "click-soft", .2)

cls = f.set("cls", "class86.png")
Y = foot(cls)
cls.actor("nei", ["nei_stack", "nei_hand", "nei_ask", "nei_think"], x=-250, y=Y, h=700)
cls.actor("stu", ["stu_write", "stu_think", "stu_sure", "stu_shock"], x=1430, y=Y, h=500, flip=True)
cls.actor("sbm", ["sb_m_write", "sb_m_talk"], x=1050, y=Y + 10, h=480, flip=True)
cls.actor("sbf", ["sb_f_write", "sb_f_shrug"], x=1720, y=Y - 10, h=470, flip=True)
cls.text("t1", "다음 날 아침 · 에모리대학교", 960, top(cls, 90), size=64, rot=-1, card=True)
cls.text("q3", "어디서 · 누구에게 · 어떻게", 960, top(cls, 200), size=80, rot=-2, card=True)
for k, (x, y) in enumerate([(1180, Y - 300), (1560, Y - 330), (1820, Y - 290)]):
    cls.prop(f"sh{k}", "sheet86", x, y, 150, z=8, rot=-8 + k * 7)
for aid in ("stu", "sbm", "sbf"):
    pass
go(T(1) - .3, "cls", "push", .9)
f._sound(T(1) - .35, "whoosh", .2)
f._enter(T(1) + .4, "t1", "write", .8)
f._cam(T(1), "cls", 960, cls.ph / 2, 1.0, .1)
f._walk(T(2) - .2, "nei", 820, 3.0, bob=10)
f._leave(T(2) + 1.5, "t1", "fade", .4)
f._pose(W("나눠", 2), "nei", "nei_hand")
for k in range(3):
    f._enter(W("나눠", 2) + .25 + k * .25, f"sh{k}", "slide", .5, dx=-500, dy=0)
    f._sound(W("나눠", 2) + .25 + k * .25, "whoosh-short", .1)
f._pose(T(3), "nei", "nei_ask")
f._enter(T(4, .2), "q3", "write", 1.2)
f._sound(T(4, .2), "pop", .15)
f._leave(E(4), "q3", "fade", .4)
f._cam(T(5), "cls", 1400, cls.ph / 2 + 60, 1.25, 2.0)
for k in range(3):
    f._leave(T(5) + .2, f"sh{k}", "fade", .3)
f._sound(T(5) + .3, "typing", .12)

# 기억의 조각들: 기숙사 · 식당 · 친구
dorm = f.set("dorm", "dorm86.png")
dorm.actor("stud", ["stu_think", "stu_sure"], x=700, y=foot(dorm), h=700)
dorm.text("lbd", "기숙사 방에서", 1300, top(dorm, 110), size=78, rot=-3)
cafe = f.set("cafe", "cafe86.png")
cafe.actor("sbmc", ["sb_m_talk"], x=1250, y=foot(cafe), h=690, flip=True)
cafe.text("lbc", "식당에서", 640, top(cafe, 110), size=78, rot=-3)
cafe.text("lbf", "친구에게서", 640, top(cafe, 220), size=78, rot=-2)
go(W("기숙사", 6) - .15, "dorm", "cut")
f._enter(W("기숙사", 6), "lbd", "write", .5)
f._cam(W("기숙사", 6), "dorm", dorm.pw / 2 + 80, dorm.ph / 2, 1.08, 2.4)
go(W("식당", 6) - .1, "cafe", "cut")
f._enter(W("식당", 6), "lbc", "write", .4)
f._enter(W("친구", 6), "lbf", "write", .4)
f._sound(W("식당", 6), "click-soft", .15)

off = f.set("off", "office88.png")
off.actor("neio", ["nei_stack", "nei_think"], x=1350, y=foot(off), h=720, flip=True)
off.prop("drw", "drawer86", 520, foot(off) - 260, 460, z=4, hidden=False)
off.prop("stk", "stack86", 1150, foot(off) - 420, 200, z=8, hidden=False)
off.text("t25", "2년 반 뒤", 960, top(off, 110), size=96, rot=-2, card=True)
go(T(7) - .2, "off", "dissolve", .6)
f._move(T(7, .45), "stk", dx=-640, dy=170, dur=1.4, rot=-6)
f._leave(T(7, .45) + 1.3, "stk", "fade", .3)
f._sound(T(7, .45) + 1.2, "click", .2)
f._pose(T(7, .7), "neio", "nei_think")
f._grade(T(8), "off", "sepia(.25) saturate(.9)", 1.0)
f._enter(T(8, .1), "t25", "write", .7)
f._cam(T(8), "off", 960, off.ph / 2, 1.06, 4)

go(T(9) - .2, "cls", "dissolve", .5)
f._leave(T(9) - .2, "t25", "fade", .1)
f._cam(T(9) - .2, "cls", 1350, cls.ph / 2 + 40, 1.12, .1)
f._pose(T(9), "stu", "stu_sure")
f._pose(T(9, .4), "sbm", "sb_m_talk")
f._pose(T(9, .7), "sbf", "sb_f_shrug")
f._cam(T(10), "cls", 1450, cls.ph / 2 + 20, 1.3, 3)

# 나란히 놓자 — 칸 만화 두 칸: 그날 쓴 종이 / 지금의 기억
pg1 = Page(f, "pg1")
pg1.panel("p1a", 80, 150, 860, 760, "dorm86.png", crop=(0.5, 0.55, 1.1),
          actors=[("stu_write", 430, 720, 470)], props=[("sheet86", 690, 300, 230)], caption="1986년 1월 29일 · 직접 쓴 종이")
pg1.panel("p1b", 980, 150, 860, 760, "cafe86.png", crop=(0.5, 0.55, 1.1),
          actors=[("stu_sure", 430, 740, 600)], caption="2년 반 뒤 · 지금의 기억")
go(W("나란히", 11) - .4, "pg1", "dissolve", .4)
pg1.draw(W("나란히", 11) - .2, "p1a")
pg1.draw(W("나란히", 11) + .5, "p1b")
pg1.focus(T(12), "p1a", 1.25, 1.2)
pg1.focus(W("사람이", 12), "p1b", 1.25, 1.2)
f._cam(W("어떤", 12), "pg1", 960, 540, 1.0, 1.0)

go(T(13) - .2, "cls", "dissolve", .5)
f._cam(T(13) - .2, "cls", 1430, cls.ph / 2 + 30, 1.45, .1)
f._pose(T(13, .3), "stu", "stu_shock")
f._pose(W("믿는", 14), "stu", "stu_sure")
f._sound(T(13, .3), "pop", .15)

bline("b15a", "확신의 크기", 400, 84)
bline("b15b", "≠", 520, 84, GOLD)
bline("b15c", "기억의 정확도", 640, 84)
go(T(15) - .1, "blk", "cut")
bshow(T(15, .25), ["b15a"])
bshow(W("맞았는지", 15), ["b15b", "b15c"])
bline("b16", "그토록 생생한 기억은, 어떻게 바뀌었을까", 470, 64)
bline("b17", "그리고 왜, 바뀐 줄을 모를까", 600, 64, GOLD)
bhide(T(16) - .2, ["b15a", "b15b", "b15c"])
bshow(T(16), ["b16"], 1.6)
bshow(T(17), ["b17"], 1.2)
bhide(E(17) + .3, ["b16", "b17"])

# ───────────────────────────────── 2. 녹화가 아니다
t = chapter(2, 18)
dorm.text("rec", "다시 틀어 보기?", 560, dorm.ph * 0.5 - 250, size=72, rot=-3, card=True)
go(t, "dorm", "dissolve", .5)
f._leave(t, "lbd", "fade", .01)
f._setv(t, "#stud", {"opacity": 0})
f._cam(t, "dorm", dorm.pw * 0.35, dorm.ph * 0.5, 1.15, .1)
f._cam(t + .1, "dorm", dorm.pw * 0.3, dorm.ph * 0.48, 1.6, 5, "sine.inOut")
f._enter(W("틀어", 19), "rec", "write", .7)
f._grade(W("흐려", 20), "dorm", "blur(5px) saturate(.6)", 1.2)
f._leave(E(20), "rec", "fade", .3)

c32 = f.set("c32", "cam32.png")
Y = foot(c32)
c32.actor("bar", ["bar_read", "bar_listen", "bar_write", "bar_point"], x=560, y=Y, h=720)
c32.actor("s32", ["s32_think", "s32_tell", "s32_shrug"], x=1400, y=Y, h=700, flip=True)
c32.text("t32", "1932년 · 영국 케임브리지", 960, top(c32, 90), size=66, rot=-1, card=True)
c32.counter("rt", 1400, top(c32, 200), size=64, color="#2b2118", font="pen", card=True)
c32.text("t29", "재생이 아니라, 재구성", 960, top(c32, 110), size=92, color="#5a2a1a", font="serif", rot=0, card=True)
ok_bar = photo_card(a.refs / "bartlett.jpg", art / "photo_bartlett.png")
if ok_bar:
    c32.prop("ph_bar", "photo_bartlett", 1000, c32.ph / 2 - 60, 330, z=9, rot=-3)
    c32.text("ph_barn", "프레더릭 바틀렛 (1886–1969) · 사진 1948", 1000, c32.ph / 2 + 200, size=30, font="gothic", rot=0, card=True)
go(T(21) - .3, "c32", "push", .9)
f._sound(T(21) - .35, "whoosh", .2)
f._grade(T(21) - .3, "dorm", "none", .1)
f._enter(T(21, .3), "t32", "write", .9)
f._leave(E(21) + .2, "t32", "fade", .3)
if ok_bar:
    tb = W("바틀렛", 22)
    f._enter(tb, "ph_bar", "drop", .7)
    f._enter(tb + .3, "ph_barn", "write", .6)
    f._leave(tb + 4.0, "ph_bar", "fade", .4)
    f._leave(tb + 4.0, "ph_barn", "fade", .4)
f._pose(T(22, .6), "bar", "bar_read")

riv = f.set("riv", "river.png")
riv.prop("canoe", "canoe", -300, riv.ph * 0.62, 620, z=5, hidden=False)
riv.prop("boat", "boat", 900, riv.ph * 0.62, 520, z=5)
riv.text("tg", "유령들의 전쟁", 960, top(riv, 140), size=96, color="#f3efe6", font="serif", rot=0, shadow=False)
go(T(23) - .2, "riv", "dissolve", 1.0)
f._enter(W("유령", 23), "tg", "write", 1.2)
f._move(T(23), "canoe", dx=1200, dur=7.5, ease="sine.out")
f._cam(T(23), "riv", riv.pw / 2, riv.ph / 2, 1.1, 6)
f._leave(E(23) + .2, "tg", "fade", .5)

go(T(24) - .1, "c32", "dissolve", .5)
f._pose(T(24), "bar", "bar_listen")
f._pose(T(24, .3), "s32", "s32_tell")
f._count(T(24, .4), "rt", 1, 4, 3.5, "", "번째 다시 말하기")
f._pose(T(25), "s32", "s32_think")
f._pose(T(25, .5), "bar", "bar_write")
f._leave(E(25), "rt", "fade", .3)
f._cam(T(26), "c32", 1300, c32.ph / 2, 1.3, 2.5)
f._pose(T(26, .4), "s32", "s32_tell")

# 카누 → 보트 (같은 자리에서 바뀜)
go(T(27) - .2, "riv", "dissolve", .5)
f._cam(T(27) - .2, "riv", 900, riv.ph * 0.6, 1.5, .1)
tc = W("보트", 27)
f._tween(tc - .2, "#canoe > .mv", {"scaleY": .85, "scaleX": 1.05}, .15)
f._leave(tc, "canoe", "fade", .35)
f._enter(tc, "boat", "pop", .5)
f._sound(tc, "sparkle", .2)

go(T(28) - .1, "c32", "dissolve", .5)
f._cam(T(28) - .1, "c32", 960, c32.ph / 2, 1.0, .1)
f._pose(T(28, .4), "s32", "s32_shrug")
f._pose(T(29), "bar", "bar_point")
f._enter(W("재구성", 29) - .3, "t29", "write", 1.0)
f._sound(W("재구성", 29), "pop", .18)
f._leave(E(30) - .5, "t29", "fade", .4)

# ───────────────────────────────── 3. 단어 하나
t = chapter(3, 31, hold=.9)
lab = f.set("lab", "lab74.png")
Y = foot(lab)
lab.actor("lof", ["lof_show", "lof_ask", "lof_note", "lof_point"], x=430, y=Y, h=720)
lab.actor("s74", ["s74_watch", "s74_write", "s74_sure", "s74_unsure"], x=1460, y=Y + 10, h=500, flip=True)
lab.text("t74", "1974년 · 미국 워싱턴대학교", 960, top(lab, 90), size=66, rot=-1, card=True)
lab.text("t2nd", "두 번째 실험 · 150명 · 일주일 뒤", 960, top(lab, 90), size=62, rot=-1, card=True)
go(t, "lab", "dissolve", .5)
f._enter(t + .2, "t74", "write", .8)
f._leave(E(31) + 2.5, "t74", "fade", .4)
f._pose(W("영상", 32), "lof", "lof_show")

road = f.set("road", "road74.png", w=2400)
RY = road.ph * 0.66
road.prop("car_a", "car_a", -500, RY, 520, z=5, hidden=False)
road.prop("car_b", "car_b", road.pw + 500, RY + 20, 520, z=6, hidden=False, )
road.prop("glass", "glass", road.pw / 2, RY + 150, 420, z=7)
road.text("film", "실험 영상", 300, top(road, 80), size=52, color="#f3efe6", font="gothic", rot=0, shadow=False)


def crash(t0, glass=False):
    f._setv(t0, "#car_a > .mv", {"x": 0})
    f._setv(t0, "#car_b > .mv", {"x": 0})
    f._move(t0, "car_a", dx=road.pw / 2 + 240, dur=1.6, ease="power1.in")
    f._move(t0, "car_b", dx=-(road.pw / 2 + 240), dur=1.6, ease="power1.in")
    f._move(t0 + 1.6, "car_a", dx=-60, dy=-10, dur=.35, rot=-4, ease="power2.out")
    f._move(t0 + 1.6, "car_b", dx=60, dy=-6, dur=.35, rot=3, ease="power2.out")
    f._sound(t0 + 1.55, "impact-bass-1", .25)


tf = W("짧은", 32)
go(tf, "road", "iris", .7)
f._cam(tf, "road", road.pw / 2, road.ph / 2, 1.0, .1)
f._enter(tf + .3, "film", "fade", .3)
crash(tf + .5)
go(T(33) - .1, "lab", "dissolve", .4)
f._pose(T(33), "lof", "lof_ask")
f._pose(T(33, .5), "s74", "s74_write")

# 질문지 한 줄 — 빈칸의 낱말만 바뀜
from comic import paper  # noqa: E402
paper(art / "paper.png")
qp = f.set("qp", "paper.png", focus=(960, 540, 1.0))
qp.text("qa", "두 차가 서로", 960, 330, size=78, font="serif", rot=0, shadow=False)
qp.text("qv1", "부딪쳤을 때,", 960, 450, size=110, color="#5a2a1a", font="pen", rot=-1, shadow=False)
qp.text("qv2", "닿았을 때,", 960, 450, size=110, color="#2f5d8a", font="pen", rot=-1, shadow=False)
qp.text("qv3", "부딪쳤을 때,", 960, 450, size=110, color="#5a2a1a", font="pen", rot=-1, shadow=False)
qp.text("qv4", "박살 났을 때,", 960, 450, size=110, color="#b5452e", font="pen", rot=-1, shadow=False)
qp.text("qb", "차는 얼마나 빨리 달리고 있었나요?", 960, 600, size=70, font="serif", rot=0, shadow=False)
go(T(35) - .3, "qp", "dissolve", .4)
f._enter(T(35), "qa", "write", .5)
f._enter(W("부딪", 35), "qv1", "write", .5)
f._enter(W("얼마나", 35), "qb", "write", .9)
f._leave(T(36, .6), "qv1", "fade", .25)
f._enter(W("닿았", 37), "qv2", "write", .4)
f._leave(W("부딪", 37) - .1, "qv2", "fade", .1)
f._enter(W("부딪", 37), "qv3", "write", .4)
f._leave(W("박살", 37) - .1, "qv3", "fade", .1)
f._enter(W("박살", 37), "qv4", "write", .4)
f._sound(W("박살", 37), "impact-bass-2", .18)
for tid in ("qa", "qv4", "qb"):
    f._leave(E(38), tid, "fade", .3)

# 속도 — 칸 두 개
pg2 = Page(f, "pg2")
pg2.panel("p2a", 80, 140, 860, 800, "road74.png", crop=(0.3, 0.6, 1.0), props=[("speedo", 430, 500, 380)], caption="'닿았을 때'라고 물으면")
pg2.panel("p2b", 980, 140, 860, 800, "road74.png", crop=(0.7, 0.6, 1.0), props=[("speedo", 430, 500, 380)], caption="'박살 났을 때'라고 물으면")
pg2.s.counter("v51", 510, 760, size=96, color="#2f5d8a", font="gothic", card=True)
pg2.s.counter("v66", 1410, 760, size=96, color="#b5452e", font="gothic", card=True)
go(E(38) + .1, "pg2", "dissolve", .4)
pg2.draw(W("닿았", 39) - .3, "p2a")
f._count(W("51", 39), "v51", 0, 51, 1.3, "시속 약 ", "km")
pg2.draw(W("박살", 39) - .3, "p2b")
f._count(W("66", 39), "v66", 0, 66, 1.3, "시속 약 ", "km")
f._sound(W("66", 39) + 1.2, "pop", .15)

go(T(40) - .2, "lab", "dissolve", .5)
f._pose(T(40), "lof", "lof_note")
f._pose(T(41), "lof", "lof_point")
f._enter(T(42), "t2nd", "write", .9)
f._pose(T(43), "lof", "lof_ask")
f._pose(T(43, .5), "s74", "s74_watch")
lab.text("q44", "깨진 유리 조각을 보셨나요?", 1180, top(lab, 230), size=70, rot=-2, card=True)
f._leave(T(43), "t2nd", "fade", .4)
f._enter(T(44), "q44", "write", .9)
f._leave(E(44) + .2, "q44", "fade", .3)

# 영상에는 유리가 없다
road.text("noglass", "영상 속 깨진 유리 — 없음", 1200, top(road, 140), size=66, rot=-2, card=True)
go(T(45) - .2, "road", "dissolve", .4)
f._cam(T(45) - .2, "road", road.pw / 2, road.ph / 2 + 30, 1.3, .1)
f._enter(T(45, .4), "noglass", "write", .8)

# 유리를 봤다는 답 — 칸 세 개
pg3 = Page(f, "pg3")
for k, (cap, x) in enumerate([("'박살 났을 때' 질문", 70), ("'부딪쳤을 때' 질문", 670), ("속도 질문 없음", 1270)]):
    gl = [("glass", 290, 560, [320, 160, 140][k])]
    pg3.panel(f"p3{k}", x, 150, 580, 760, "lab74.png", crop=(0.5, 0.6, 1.0),
              actors=[("s74_sure" if k == 0 else "s74_unsure", 300, 700, 520)], props=gl, caption=cap)
    pg3.s.counter(f"g{k}", x + 290, 740, size=92, color=["#b5452e", "#5a2a1a", "#5a2a1a"][k], font="gothic", card=True)
go(T(46) - .3, "pg3", "dissolve", .4)
pg3.draw(W("박살", 46), "p30")
f._count(W("32", 46), "g0", 0, 32, 1.0, "", "%")
pg3.draw(T(47), "p31")
f._count(W("14", 47), "g1", 0, 14, .8, "", "%")
pg3.draw(W("속도", 47), "p32")
f._count(W("12", 47), "g2", 0, 12, .8, "", "%")
f._sound(W("12", 47) + .8, "pop", .15)

# 기억 속 장면에 유리가 그려 넣어짐
go(T(48) - .2, "road", "dissolve", .6)
f._leave(T(48) - .2, "noglass", "fade", .01)
f._grade(T(48) - .2, "road", "sepia(.45) saturate(.8)", .5)
f._cam(T(49), "road", road.pw / 2, RY + 60, 1.7, 3.5)
f._enter(W("그려", 50) - .4, "glass", "fade", 1.6)
f._sound(W("그려", 50), "sparkle", .2)
bline("b51a", "오정보 효과", 470, 110)
bline("b51b", "나중에 들은 말이, 기억 속 장면에 섞여 들어간다", 620, 50, DIM)
go(T(51) - .1, "blk", "cut")
f._grade(T(51), "road", "none", .1)
bshow(W("오정보", 51), ["b51a"], .8)
bshow(W("오정보", 51) + 1.0, ["b51b"], 1.4)
bhide(E(51) + .9, ["b51a", "b51b"])

# ───────────────────────────────── 4. 없던 사건까지
t = chapter(4, 52, hold=.0)
bline("b52", "사건 하나를, 통째로 심을 수도 있을까", 520, 70)
bshow(t + .1, ["b52"], 1.4)
bhide(E(52) + .2, ["b52"])
r95 = f.set("r95", "room95.png")
Y = foot(r95)
r95.actor("pt", ["pt_read", "pt_recall", "pt_tell"], x=1300, y=Y, h=520, flip=True)
r95.actor("iv", ["int_ask"], x=560, y=Y, h=700)
r95.text("t95", "1995년 · 로프터스 & 피크렐 · 24명", 960, top(r95, 90), size=62, rot=-1, card=True)
r95.text("real3", "가족이 들려준 진짜 일화 × 3", 760, top(r95, 220), size=58, rot=-2, card=True)
r95.text("fake1", "+ 끼워 넣은 가짜 일화 × 1", 1160, top(r95, 320), size=58, color="#b5452e", rot=-2, card=True)
go(E(52) + .4, "r95", "dissolve", .6)
f._enter(T(53, .2), "t95", "write", .9)
f._leave(T(54), "t95", "fade", .3)
f._enter(W("실제", 54), "real3", "write", .7)
f._enter(W("가짜", 54), "fake1", "write", .7)
f._sound(W("가짜", 54), "pop", .18)

mall = f.set("mall", "mall.png")
Y = foot(mall)
mall.actor("kid", ["kid_lost", "kid_cry"], x=760, y=Y, h=380)
mall.actor("help", ["helper"], x=2300, y=Y, h=640, flip=True)
mall.actor("hug", ["kid_hug"], x=1420, y=Y, h=480)
mall.text("t5y", "다섯 살 무렵 · 쇼핑몰", 960, top(mall, 100), size=62, rot=-2, card=True)
f._setv(0, "#hug", {"opacity": 0})
go(T(55) - .3, "mall", "dissolve", .7)
f._leave(T(55) - .3, "real3", "fade", .2)
f._leave(T(55) - .3, "fake1", "fade", .2)
f._grade(T(55) - .3, "mall", "sepia(.35) saturate(.85)", .1)
f._enter(T(55, .1), "t5y", "write", .7)
f._cam(T(55), "mall", 760, mall.ph / 2 + 60, 1.25, .1)
f._pose(W("울다", 55), "kid", "kid_cry")
f._walk(W("어른", 55) - .6, "help", -1100, 1.6, bob=8)
f._cam(W("어른", 55) - .6, "mall", 1000, mall.ph / 2 + 40, 1.1, 1.6)
f._leave(W("만났", 55) - .2, "t5y", "fade", .3)
f._tween(W("만났", 55), "#hug", {"opacity": 1}, .5)
f._leave(W("만났", 55), "kid", "fade", .4)

go(T(56) - .2, "r95", "dissolve", .5)
f._pose(T(56, .55), "pt", "pt_recall")
go(T(57) - .1, "mall", "dissolve", .8)
f._grade(T(57) - .1, "mall", "sepia(.6) saturate(.6) blur(1.5px)", .1)
f._setv(T(57) - .1, "#hug", {"opacity": 0})
f._setv(T(57) - .1, "#kid", {"opacity": 1})
f._pose(T(57) - .1, "kid", "kid_lost")
f._cam(T(57), "mall", 900, mall.ph / 2, 1.0, 3)
f._cam(T(58), "mall", 1200, mall.ph / 2 - 40, 1.7, 2.0)
mall.text("t58", "옷차림까지", 1400, top(mall, 220), size=74, rot=-3, card=True)
f._enter(W("옷차림", 58), "t58", "write", .6)

bline("b59a", "'넷 중 한 명꼴로 없던 기억이 생긴다'", 470, 64)
bline("b59b", "— 널리 알려진 결과", 590, 46, DIM)
go(T(59) - .1, "blk", "cut")
f._leave(T(59), "t58", "fade", .01)
bshow(W("4중", 59), ["b59a"], 1.2)
bshow(W("널리", 59), ["b59b"], .7)
bhide(E(59) + .5, ["b59a", "b59b"])

pg4 = Page(f, "pg4")
pg4.panel("p4a", 80, 150, 860, 760, "room95.png", crop=(0.5, 0.6, 1.1), actors=[("pt_tell", 430, 730, 600)], caption="알려진 것 · '없던 기억이 생겼다'")
pg4.panel("p4b", 980, 150, 860, 760, "room95.png", crop=(0.5, 0.6, 1.1), actors=[("pt_recall", 430, 700, 480)], caption="다시 보니 · '그랬을 수도…' · 다른 기억과 섞임")
pg4.s.text("p4t", "완전히 지어낸 기억 — 훨씬 드물었다", 960, 960, size=60, color="#b5452e", font="gothic", rot=0, card=True)
go(T(60) - .2, "pg4", "dissolve", .5)
pg4.draw(T(60, .3), "p4a")
pg4.draw(T(61, .3), "p4b")
f._enter(W("드물", 62) - .6, "p4t", "write", 1.0)
pg4.focus(T(63), "p4b", 1.3, 1.5)
f._cam(E(63), "pg4", 960, 540, 1.0, .8)

bline("b65", "기억은 아무것이나 받아들이는 백지가 아니다", 430, 60)
bline("b66", "하지만 있는 조각에, 그럴듯한 조각은 쉽게 붙는다", 580, 60, GOLD)
go(T(64) - .1, "blk", "dissolve", .4)
bshow(T(65), ["b65"], 1.4)
bshow(T(66), ["b66"], 1.5)
bhide(E(66) + .6, ["b65", "b66"])

# ───────────────────────────────── 5. 뇌 안에서 일어나는 일
t = chapter(5, 67, hold=.0)
bline("b67", "기억은 왜 이렇게 쉽게 고쳐질까", 520, 72)
bshow(t + .1, ["b67"], 1.2)
bhide(E(68), ["b67"])
lib = f.set("lib", "library.png")
lib.prop("brain", "brain", 960, top(lib, 330), 520, z=8)
lib.prop("bk_a", "book_a", 380, lib.ph / 2 + 40, 130, z=7)
lib.prop("bk_b", "book_b", 1560, lib.ph / 2 + 10, 130, z=7)
lib.prop("bk_c", "book_a", 960, lib.ph / 2 - 120, 120, z=7)
lib.text("lv", "본 모습 → 시각 영역", 380, lib.ph / 2 + 180, size=48, rot=-2, card=True)
lib.text("la", "들은 소리 → 청각 영역", 1560, lib.ph / 2 + 150, size=48, rot=2, card=True)
lib.text("le", "감정 → 감정 영역", 960, lib.ph / 2 + 20, size=48, rot=-1, card=True)
lib.prop("hippo", "hippo", 960, lib.ph / 2 + 230, 260, z=9)
lib.text("lh", "해마", 1150, lib.ph / 2 + 190, size=72, color="#8a5a10", rot=-3, card=True)
lib.prop("icard", "indexcard", 1250, lib.ph / 2 + 260, 300, z=10, rot=6)
lib.text("lic", "색인 카드", 1300, lib.ph / 2 + 400, size=56, rot=2, card=True)
lib.text("gap", "빈칸", 700, lib.ph / 2 + 250, size=96, color="#b5452e", rot=-2, card=True)
for k, s_ in enumerate(["지금 아는 것", "그럴 거라는 기대", "방금 들은 질문의 단어"]):
    lib.text(f"fill{k}", s_, [520, 960, 1400][k], lib.ph / 2 + 390, size=46, color="#2f5d8a", rot=[-3, 1, 3][k], card=True)
go(T(69) - .3, "lib", "dissolve", .7)
f._cam(T(69) - .3, "lib", lib.pw / 2, lib.ph / 2, 1.0, .1)
f._enter(T(69, .3), "brain", "pop", .7)
f._leave(T(70) - .1, "brain", "shrink", .5)
f._enter(W("본", 70), "bk_a", "pop", .5)
f._enter(W("본", 70) + .2, "lv", "write", .6)
f._enter(W("소리", 70), "bk_b", "pop", .5)
f._enter(W("소리", 70) + .2, "la", "write", .6)
f._enter(W("감정", 70), "bk_c", "pop", .5)
f._enter(W("감정", 70) + .2, "le", "write", .5)
for k, x in enumerate(["bk_a", "bk_b", "bk_c"]):
    f._sound(W(["본", "소리", "감정"][k], 70), "pop", .12)
f._enter(W("헤마", 71), "hippo", "pop", .7)
f._enter(W("헤마", 71) + .3, "lh", "write", .5)
f._sound(W("헤마", 71), "sparkle", .2)
for x in ("lv", "la", "le"):
    f._leave(T(72), x, "fade", .3)
f._enter(W("카드", 72), "icard", "drop", .7)
f._enter(W("카드", 72) + .4, "lic", "write", .5)
f._cam(W("카드", 72), "lib", 1150, lib.ph / 2 + 250, 1.5, 1.6)
# 떠올림 = 조각을 다시 모아 조립 (책들이 가운데 탁자로)
f._cam(T(73), "lib", lib.pw / 2, lib.ph / 2 + 120, 1.0, 1.6)
f._leave(T(73), "lic", "fade", .3)
f._leave(T(73), "icard", "fade", .3)
f._move(W("조각", 73), "bk_a", dx=440, dy=260, dur=1.2, rot=-10)
f._move(W("조각", 73) + .2, "bk_b", dx=-460, dy=290, dur=1.2, rot=8)
f._move(W("조각", 73) + .4, "bk_c", dx=120, dy=420, dur=1.2, rot=-4)
f._sound(W("조각", 73), "whoosh-short", .15)
f._enter(T(74, .3), "gap", "pop", .5)
f._sound(T(74, .3), "pop", .18)
for k, w_ in enumerate(["지금", "기대", "질문"]):
    tt = W(w_, 75)
    f._enter(tt, f"fill{k}", "write", .6)
f._cam(T(75), "lib", lib.pw / 2, lib.ph / 2 + 300, 1.3, 2.0)

# 쥐 실험 — 칸 네 개 (실험 순서 = 칸 순서)
rl = f.set("rl", "ratlab.png")
rl.actor("nad", ["nad_note", "nad_surprise"], x=1450, y=foot(rl), h=720, flip=True)
rl.text("t00", "2000년 · 뉴욕대학교 · 나더 & 르두 연구팀", 860, top(rl, 90), size=60, rot=-1, card=True)
go(T(76) - .3, "rl", "dissolve", .6)
f._enter(T(76, .15), "t00", "write", 1.0)
f._cam(T(76), "rl", rl.pw / 2 + 100, rl.ph / 2, 1.08, 6)

pg5 = Page(f, "pg5")
RC = (0.45, 0.6, 1.25)
pg5.panel("p5a", 70, 70, 880, 460, "ratlab.png", crop=RC, actors=[("rat_freeze", 440, 420, 170)], caption="① 소리 + 약한 자극 → 소리를 두려워함")
pg5.panel("p5b", 970, 70, 880, 460, "ratlab.png", crop=RC, actors=[("rat_freeze", 440, 420, 170)], caption="② 하루 뒤 · 소리로 기억을 떠올린 직후 + 약물")
pg5.panel("p5c", 70, 550, 880, 460, "ratlab.png", crop=RC, actors=[("rat_calm", 440, 420, 170)], caption="③ 다음 날 · 예전만큼 두려워하지 않음")
pg5.panel("p5d", 970, 550, 880, 460, "ratlab.png", crop=RC, actors=[("rat_freeze", 440, 420, 170)], caption="④ 6시간 뒤에 약물 · 아무 일도 없음")
go(T(77) - .3, "pg5", "dissolve", .5)
pg5.draw(T(77) - .1, "p5a")
pg5.draw(T(78), "p5b")
pg5.focus(T(79), "p5b", 1.5, 1.2)
pg5.s.text("amy", "편도체 · 새 단백질을 못 만들게", 1410, 455, size=36, color="#b5452e", font="gothic", rot=0, card=True)
f._enter(W("편도체", 79), "amy", "write", .8)
f._cam(T(80) - .2, "pg5", 960, 540, 1.0, .8)
pg5.draw(T(80), "p5c")
pg5.draw(W("6시간", 82) - .2, "p5d")
f._sound(T(80, .5), "pop", .15)

# 재응고화 — 원고를 열어 고치고 다시 넣음
dn = f.set("dn", "desknight.png")
dn.prop("ms", "manuscript", 900, dn.ph / 2 + 90, 520, z=6, rot=-4)
dn.prop("msn", "pagenew", 900, dn.ph / 2 + 90, 520, z=5, rot=-4, hidden=False)
dn.prop("pen", "pencil", 1180, dn.ph / 2 + 10, 320, z=8, rot=0)
dn.text("open", "꺼내면 → 잠시 열림", 640, top(dn, 260), size=66, rot=-3, card=True)
dn.text("save", "→ 다시 저장", 1240, top(dn, 260), size=66, rot=2, card=True)
dn.text("newi", "그사이 들어온 정보", 1450, dn.ph / 2 + 340, size=50, color="#2f5d8a", rot=3, card=True)
go(T(83) - .2, "dn", "dissolve", .6)
f._cam(T(83) - .2, "dn", 900, dn.ph / 2 + 60, 1.15, .1)
f._enter(W("꺼낼", 84), "open", "write", .7)
f._enter(W("꺼낼", 84) + .3, "pen", "drop", .6)
f._enter(W("저장", 84), "save", "write", .6)
f._sound(W("꺼낼", 84), "click-soft", .2)
bline("b85", "재응고화", 470, 120)
bline("b85b", "떠올린 기억은 잠시 불안정해졌다가 다시 굳는다", 620, 48, DIM)
go(T(85) - .1, "blk", "cut")
bshow(W("재흥", 85), ["b85"], .7)
bshow(W("재흥", 85) + .8, ["b85b"], 1.3)
bhide(E(85) + .4, ["b85", "b85b"])
go(T(86) - .1, "dn", "dissolve", .4)
f._leave(T(86) - .1, "open", "fade", .1)
f._leave(T(86) - .1, "save", "fade", .1)
f._enter(T(86, .1), "ms", "fade", .6)
for k in range(4):   # 연필이 원고 위를 오가며 고쳐 씀
    f._move(T(86, .2) + k * .6, "pen", dx=-180 if k % 2 == 0 else 180, dy=40, dur=.55, rot=-4 if k % 2 == 0 else 4, ease="sine.inOut")
f._sound(T(86, .2), "typing", .1)
f._enter(T(87, .3), "newi", "slide", .8, dx=400, dy=0)
f._move(T(87, .6), "newi", dx=-450, dy=-150, dur=1.2, scale=.6)
f._leave(E(87), "newi", "fade", .4)

# 되짚기: 유리 조각 · 나이서의 학생들
go(T(88) - .2, "road", "dissolve", .5)
f._grade(T(88) - .2, "road", "sepia(.45) saturate(.8)", .1)
f._cam(T(88) - .2, "road", road.pw / 2, RY + 60, 1.6, .1)
go(W("나이소", 88) - .2, "cls", "dissolve", .5)
f._cam(W("나이소", 88) - .2, "cls", 1430, cls.ph / 2 + 30, 1.35, .1)
f._pose(W("나이소", 88), "stu", "stu_think")
f._grade(W("나이소", 88), "cls", "sepia(.3)", 1.5)

# ───────────────────────────────── 6. 왜 이렇게 만들어졌을까
t = chapter(6, 89, hold=.0)
bline("b90", "뇌는 왜 이렇게 불안정한 방식으로 기억을 다룰까", 450, 62)
bline("b91", "정확하게 녹화해 두는 편이 더 좋지 않았을까", 580, 56, DIM)
f._grade(t, "cls", "none", .1)
bshow(T(90), ["b90"], 1.5)
bshow(T(91), ["b91"], 1.3)
bhide(E(91) + .3, ["b90", "b91"])
cr = f.set("cr", "crossing.png")
Y = foot(cr)
cr.actor("me", ["me_walk", "me_imagine", "me_speech"], x=-200, y=Y, h=700)
cr.prop("bub", "bubble", 1300, top(cr, 300), 640, z=8)
cr.prop("bb_a", "book_a", 1180, top(cr, 300), 100, z=9)
cr.prop("bb_b", "book_b", 1420, top(cr, 290), 100, z=9)
cr.prop("bb_c", "indexcard", 1300, top(cr, 330), 150, z=9)
cr.text("t92", "하버드대학교 · 대니얼 섀크터", 960, top(cr, 90), size=62, rot=-1, card=True)
cr.text("q93", "기억의 목적이 과거 보관이 아니라면?", 1000, top(cr, 90), size=62, rot=-2, card=True)
cr.text("q94", "앞일을 대비하는 데 있다면?", 1000, top(cr, 200), size=62, color="#2f5d8a", rot=-2, card=True)
go(T(92) - .2, "cr", "dissolve", .6)
f._enter(T(92, .1), "t92", "write", .9)
f._walk(T(92), "me", 820, 3.4, bob=10)
f._leave(T(93) - .1, "t92", "fade", .3)
f._enter(T(93), "q93", "write", 1.1)
f._pose(T(94), "me", "me_imagine")
f._enter(T(94, .2), "q94", "write", 1.0)
f._leave(E(94) + .2, "q93", "fade", .3)
f._leave(E(94) + .2, "q94", "fade", .3)

pg6 = Page(f, "pg6")
pg6.panel("p6a", 80, 150, 860, 700, "library.png", crop=(0.5, 0.55, 1.1), props=[("book_a", 330, 420, 150), ("book_b", 520, 430, 150)], caption="지난 일을 떠올릴 때")
pg6.panel("p6b", 980, 150, 860, 700, "crossing.png", crop=(0.5, 0.6, 1.1), actors=[("me_imagine", 430, 690, 560)], caption="앞일을 상상할 때")
pg6.s.text("p6t", "해마를 포함한, 거의 같은 뇌 영역이 함께 움직인다", 960, 900, size=50, color="#2b2118", font="gothic", rot=0, card=True)
go(T(95) - .2, "pg6", "dissolve", .5)
pg6.draw(W("떠올릴", 95) - .2, "p6a")
pg6.draw(W("상상할", 95) - .2, "p6b")
f._enter(W("같은", 95), "p6t", "write", 1.2)

go(T(96) - .1, "cr", "dissolve", .5)
f._cam(T(96) - .1, "cr", 1150, cr.ph / 2 - 40, 1.1, .1)
f._enter(T(97), "bub", "pop", .6)
f._sound(T(97), "pop", .15)
f._enter(W("떼었다", 97), "bb_a", "pop", .4)
f._enter(W("떼었다", 97) + .3, "bb_b", "pop", .4)
f._move(W("붙였다", 97), "bb_a", dx=90, dy=10, dur=.6, rot=12)
f._move(W("붙였다", 97), "bb_b", dx=-90, dy=10, dur=.6, rot=-12)
f._enter(W("그려", 97), "bb_c", "pop", .5)
f._pose(W("발표", 98), "me", "me_speech")
f._cam(W("발표", 98), "cr", 900, cr.ph / 2, 1.2, 2)

bline("b99", "조각을 자유롭게 다시 붙이는 능력 → 내일을 미리 그려 본다", 430, 50)
bline("b100", "그 유연함의 대가 → 과거를 조립할 때 생기는 오차", 560, 50, GOLD)
bline("b101", "'결함이 아니라, 쓸모 있는 설계의 부작용'", 470, 66)
bline("b101b", "— 대니얼 섀크터", 590, 44, DIM)
go(T(99) - .1, "blk", "dissolve", .4)
for x in ("bub", "bb_a", "bb_b", "bb_c"):
    f._leave(T(99), x, "fade", .1)
bshow(T(99, .1), ["b99"], 1.5)
bshow(T(100, .1), ["b100"], 1.5)
bhide(T(101) - .2, ["b99", "b100"])
bshow(T(101, .1), ["b101"], 1.6)
bshow(T(101, .6), ["b101b"], .6)
bhide(E(101) + .4, ["b101", "b101b"])

# ───────────────────────────────── 7. 확신이라는 착각
t = chapter(7, 102, hold=.0)
bline("b102", "평생 잊지 못할 것 같은 기억이라면?", 520, 72)
bshow(t + .1, ["b102"], 1.2)
bhide(E(103), ["b102"])
lg = f.set("lg", "lounge01.png")
lg.actor("s01", ["s01_write", "s01_sure", "s01_think"], x=1450, y=foot(lg), h=500, flip=True)
lg.text("t01", "2001년 9월 12일 · 듀크대학교 · 54명", 900, top(lg, 90), size=62, rot=-1, card=True)
go(T(104) - .2, "lg", "dissolve", .6)
f._enter(T(104, .1), "t01", "write", 1.0)
f._cam(T(104), "lg", lg.pw / 2 + 150, lg.ph / 2, 1.1, 6)

pp = f.set("pp", "paper.png", focus=(960, 540, 1.0))
pp.prop("pc", "pola_c", 560, 400, 560, z=6, rot=-4)
pp.prop("pb", "pola_b", 560, 400, 560, z=7, rot=-4)
pp.prop("pa", "pola_a", 1360, 400, 560, z=6, rot=4)
pp.text("lpc", "9·11 소식을 들은 순간", 560, 730, size=54, font="gothic", rot=0, card=True)
pp.text("lpa", "같은 즈음의 평범한 하루", 1360, 730, size=54, font="gothic", rot=0, card=True)
pp.counter("cc", 560, 815, size=58, color="#b5452e", font="gothic", card=True)
pp.counter("ca", 1360, 815, size=58, color="#5a2a1a", font="gothic", card=True)
pp.text("t106", "몇 주 ~ 몇 달 뒤", 960, 90, size=66, rot=-2, card=True)
go(T(105) - .2, "pp", "dissolve", .5)
f._enter(W("순간", 105) - .4, "pc", "drop", .7)
f._enter(W("순간", 105) - .1, "lpc", "write", .6)
f._enter(W("평범", 105), "pa", "drop", .7)
f._enter(W("평범", 105) + .3, "lpa", "write", .6)
f._enter(T(106, .3), "t106", "write", .8)
# 둘 다 바뀜: 9·11 사진은 내용이 바뀌고, 평범한 하루는 흐려짐
f._move(T(107, .2), "pc", dx=0, dy=0, dur=.1)
f._leave(T(107, .3), "pc", "fade", 1.6)
f._enter(T(107, .3), "pb", "fade", 1.6)
f._grade(T(107, .3), "pp", "none", .1)
f._tween(T(107, .3), "#pa", {"filter": "blur(4px) saturate(.4)", "opacity": .75}, 2.0)
f._count(W("평범한", 110), "ca", 90, 40, 2.2, "확신 ", "")
f._count(W("9", 110) + .3, "cc", 90, 92, 1.2, "확신 ", "")
f._sound(W("9", 110) + 1.4, "pop", .15)
bline("b112", "생생함", 400, 92)
bline("b112b", "≠", 520, 84, GOLD)
bline("b112c", "정확성", 640, 92)
go(T(111) - .1, "lg", "dissolve", .4)
f._pose(T(111, .2), "s01", "s01_sure")
f._cam(T(111), "lg", 1400, lg.ph / 2 + 30, 1.4, 2.5)
go(T(112) - .1, "blk", "cut")
bshow(T(112, .1), ["b112"], .5)
bshow(W("정확", 112), ["b112b", "b112c"], .6)
bhide(E(112) + .3, ["b112", "b112b", "b112c"])
go(T(113) - .1, "cls", "dissolve", .5)
f._grade(T(113) - .1, "cls", "none", .1)
f._cam(T(113) - .1, "cls", 1430, cls.ph / 2 + 30, 1.4, .1)
f._pose(T(113) - .1, "stu", "stu_shock")
f._pose(W("믿었던", 113), "stu", "stu_sure")

# ───────────────────────────────── 8. 확신이 치른 대가 (당사자는 그리지 않음)
t = chapter(8, 114, hold=.0)
bline("b114", "이 확신이 가장 무거운 대가를 치르는 곳", 520, 66)
bshow(t + .1, ["b114"], 1.3)
bhide(E(114) + .2, ["b114"])
ct = f.set("ct", "court84.png")
ct.text("t84", "1984년 · 미국 노스캐롤라이나", 960, top(ct, 90), size=62, rot=-1, card=True)
ct.prop("lu", "lineup", 960, ct.ph / 2 + 60, 620, z=8)
ct.prop("gv", "gavel", 1400, ct.ph / 2 + 260, 320, z=9)
for k, s_ in enumerate(["사진", "대면 확인", "법정 증언"]):
    ct.text(f"st{k}", s_, [560, 960, 1360][k], ct.ph / 2 + 170, size=58, rot=[-2, 0, 2][k], card=True)
go(T(115) - .2, "ct", "dissolve", .7)
f._grade(T(115) - .2, "ct", "saturate(.7) brightness(.92)", .1)
f._enter(T(115, .1), "t84", "write", .9)
f._cam(T(115), "ct", ct.pw / 2, ct.ph / 2, 1.0, .1)
f._cam(T(116), "ct", ct.pw * 0.62, ct.ph / 2, 1.35, 9, "sine.inOut")
f._leave(T(116), "t84", "fade", .4)
f._cam(T(117) - .3, "ct", ct.pw / 2, ct.ph / 2 + 40, 1.0, 1.0)
f._enter(W("사진", 117), "lu", "pop", .6)
f._sound(W("사진", 117), "click-soft", .2)
f._leave(T(118), "lu", "fade", .3)
f._enter(W("유죄", 118), "gv", "drop", .5)
f._sound(W("유죄", 118) + .4, "impact-bass-2", .25)

cel = f.set("cel", "cell.png")
cel.counter("yrs", 960, top(cel, 150), size=110, color="#f3efe6", font="serif")
cel.prop("dna", "dnarep", 960, cel.ph / 2 + 60, 520, z=8, rot=-3)
cel.text("t95d", "1995년 · DNA 검사 · 무죄", 960, cel.ph / 2 + 380, size=60, rot=-1, card=True)
go(T(119) - .2, "cel", "dissolve", .9)
f._cam(T(119) - .2, "cel", cel.pw / 2, cel.ph / 2, 1.0, .1)
f._cam(T(119), "cel", cel.pw / 2, cel.ph / 2 - 20, 1.15, 8, "sine.inOut")
f._count(T(119, .2), "yrs", 1984, 1995, 3.8, "", "년", grp=False)
f._enter(W("DNA", 120), "dna", "pop", .7)
f._enter(W("밝혀", 120), "t95d", "write", .8)
f._sound(W("DNA", 120), "click-soft", .2)
go(T(121) - .2, "ct", "dissolve", .7)
f._leave(T(121), "gv", "fade", .1)
f._cam(T(121) - .2, "ct", ct.pw * 0.4, ct.ph / 2, 1.2, .1)
f._cam(T(121), "ct", ct.pw * 0.6, ct.ph / 2, 1.2, 8, "sine.inOut")
f._enter(W("사진", 123), "st0", "write", .5)
f._enter(W("대면", 123), "st1", "write", .5)
f._enter(W("법정", 123), "st2", "write", .5)
f._cam(T(123), "ct", ct.pw / 2, ct.ph / 2 + 120, 1.0, 1.4)

cs = f.set("cs", "paper.png", focus=(960, 540, 1.0))
for k in range(10):
    x, y = 260 + (k % 5) * 350, 330 + (k // 5) * 330
    cs.prop(f"cf{k}", "casefile", x, y, 250, z=6, rot=[-4, 3, -2, 5, -3][k % 5], hidden=False)
    if k < 7:
        cs.prop(f"cr{k}", "casered", x, y, 250, z=7, rot=[-4, 3, -2, 5, -3][k % 5])
cs.text("cst", "DNA로 뒤집힌 유죄 판결 · 열에 일곱 정도에 목격자의 잘못된 지목", 960, 900, size=46, font="gothic", rot=0, card=True)
go(T(124) - .2, "cs", "dissolve", .6)
for k in range(10):
    f._enter(T(124) + k * .08, f"cf{k}", "pop", .35)
for k in range(7):
    f._enter(W("7건", 124) + k * .15, f"cr{k}", "pop", .35)
    f._sound(W("7건", 124) + k * .15, "click-soft", .1)
f._enter(W("7건", 124) + 1.2, "cst", "write", 1.2)
ct.text("t125", "목격자 확인 절차를 바꾸기 시작", 960, top(ct, 110), size=64, rot=-1, card=True)
go(T(125) - .2, "ct", "dissolve", .6)
for k in range(3):
    f._leave(T(125) - .2, f"st{k}", "fade", .1)
f._grade(T(125) - .2, "ct", "none", 2.0)
f._enter(T(125, .3), "t125", "write", 1.0)

# ───────────────────────────────── 9. 우리가 할 수 있는 것
t = chapter(9, 127, hold=.0)
bline("b127", "그렇다면 우리는, 자기 기억을 믿을 수 없는 걸까", 520, 62)
bshow(t + .1, ["b127"], 1.4)
bhide(E(127) + .2, ["b127"])
hm = f.set("hm", "home.png")
Y = foot(hm)
hm.actor("sa", ["sib_a"], x=650, y=Y, h=720)
hm.actor("sb", ["sib_b"], x=1300, y=Y, h=700, flip=True)
hm.actor("mom", ["mom_ask"], x=700, y=Y, h=520)
hm.actor("kd", ["kid_tell"], x=1180, y=Y, h=440, flip=True)
hm.text("big", "큰 줄기는 단단하다", 960, top(hm, 100), size=74, rot=-2, card=True)
hm.text("det", "흔들리는 것은 세부 — 누가 · 언제 · 어디서 · 무슨 말", 960, top(hm, 210), size=54, color="#b5452e", rot=-1, card=True)
f._setv(0, "#mom", {"opacity": 0})
f._setv(0, "#kd", {"opacity": 0})
go(T(128) - .2, "hm", "dissolve", .6)
f._cam(T(128), "hm", hm.pw / 2, hm.ph / 2, 1.05, 8)
f._enter(T(129, .2), "big", "write", .8)
f._enter(T(131), "det", "write", 1.2)
f._leave(E(132), "big", "fade", .3)
f._leave(E(132), "det", "fade", .3)

bline("b133", "연구자들이 공통으로 권하는 습관", 230, 52, DIM)
bline("h1", "① 중요한 일은 그 자리에서 바로 적어 두기", 400, 58)
bline("h2", "② 확신과 정확성을 따로 생각하기", 540, 58)
bline("h3", "③ 물을 때, 답을 담은 단어를 피하기", 680, 58)
go(T(133) - .1, "blk", "dissolve", .4)
bshow(T(133, .1), ["b133"], .8)
bshow(T(134), ["h1"], 1.0)
bshow(T(136), ["h2"], 1.0)
bshow(T(138), ["h3"], 1.0)
bhide(E(138) + .1, ["b133", "h1", "h2", "h3"])

hm.text("qbad", "'그 사람이 때렸지?'", 760, top(hm, 140), size=70, color="#8a8a8a", rot=-2, card=True)
hm.text("qgood", "'무슨 일이 있었어?'", 1200, top(hm, 250), size=76, color="#2f5d8a", rot=2, card=True)
go(T(139) - .1, "hm", "dissolve", .4)
for x, v in (("#sa", 0), ("#sb", 0), ("#mom", 1), ("#kd", 1)):
    f._setv(T(139) - .1, x, {"opacity": v})
f._cam(T(139) - .1, "hm", 950, hm.ph / 2 + 60, 1.25, .1)
f._enter(T(139), "qbad", "write", .7)
f._tween(W("대신", 139), "#qbad", {"opacity": .35}, .4)
f._enter(W("무슨", 139), "qgood", "write", .7)
f._sound(W("무슨", 139), "pop", .15)

hm.prop("bub1", "bubble", 330, top(hm, 190), 360, z=8)
hm.prop("bub2", "bubble", 1650, top(hm, 190), 360, z=8)
hm.prop("bp1", "pola_a", 330, top(hm, 180), 190, z=9, rot=-6)
hm.prop("bp2", "pola_b", 1650, top(hm, 180), 190, z=9, rot=6)
go(T(140) - .2, "hm", "cut")
for x, v in (("#sa", 1), ("#sb", 1), ("#mom", 0), ("#kd", 0)):
    f._setv(T(140) - .2, x, {"opacity": v})
f._leave(T(140) - .2, "qbad", "fade", .1)
f._leave(T(140) - .2, "qgood", "fade", .1)
f._cam(T(140) - .2, "hm", hm.pw / 2, hm.ph / 2, 1.0, .1)
f._enter(W("다르게", 140), "bub1", "pop", .5)
f._enter(W("다르게", 140) + .2, "bp1", "pop", .5)
f._enter(W("다르게", 140) + .4, "bub2", "pop", .5)
f._enter(W("다르게", 140) + .6, "bp2", "pop", .5)
f._sound(W("다르게", 140), "pop", .15)
f._cam(T(142), "hm", hm.pw / 2, hm.ph / 2 - 30, 1.1, 5)

# ───────────────────────────────── 10. 다시, 그 종이
t = chapter(10, 143, hold=.0)
dn.prop("old", "sheet86", 760, dn.ph / 2 + 120, 360, z=7, rot=-3)
dn.text("d29", "1986년 1월 29일", 760, dn.ph / 2 - 160, size=56, rot=-3, card=True)
go(t + .2, "dn", "dissolve", .9)
f._setv(t + .2, "#ms", {"opacity": 0})
f._setv(t + .2, "#msn", {"opacity": 0})
f._setv(t + .2, "#pen", {"opacity": 0})
f._cam(t + .2, "dn", dn.pw / 2, dn.ph / 2, 1.0, .1)
f._cam(t + .4, "dn", 760, dn.ph / 2 + 80, 1.3, 7, "sine.inOut")
f._enter(W("종이", 143), "old", "fade", 1.0)
f._enter(W("종이", 143) + .6, "d29", "write", .8)
f._leave(T(144, .5), "d29", "fade", .4)
f._enter(T(145), "ms", "fade", 1.0)
f._move(T(145), "ms", dx=360, dy=-20, dur=1.0)
f._enter(T(145, .3), "pen", "fade", .4)
for k in range(4):
    f._move(T(145, .4) + k * .55, "pen", dx=-160 if k % 2 == 0 else 160, dy=30, dur=.5, rot=-4 if k % 2 == 0 else 4, ease="sine.inOut")
f._cam(T(145), "dn", dn.pw / 2 + 80, dn.ph / 2 + 60, 1.1, 2)
go(W("내일", 146) - .3, "cr", "dissolve", .7)
f._cam(W("내일", 146) - .3, "cr", cr.pw / 2, cr.ph / 2, 1.0, .1)
f._setv(W("내일", 146) - .3, "#me", {"opacity": 1})
f._pose(W("내일", 146) - .3, "me", "me_imagine")
go(W("대가", 146) - .2, "dn", "dissolve", .7)

bline("bend1", "지금 당신이 가장 확신하는 그 기억은,", 450, 66)
bline("bend2", "몇 번째로 다시 쓴 원고일까요", 580, 76, GOLD)
go(T(147) - .3, "blk", "dissolve", .9)
bshow(T(147), ["bend1"], 1.6)
bshow(W("몇", 147), ["bend2"], 1.4)

# ───────────────────────────────── 보완 (2026-11-19): 가까운 샷 완성 장면
# 사용자: "전체적인 화면 퀄리티 자체는 codex가 우세하지만 편집법 연출법 자체는 클로드가 좋았다" — 연출은 그대로 두고,
# 이야기의 핵심 순간에 인물·배경·빛이 한 장에 그려진 가까운 샷(손·어깨 너머·표정)을 끼워 넓은 '무대' 장면만 이어지지 않게.
SHOTS = os.environ.get("YTFLOW_MEMORY_SHOTS", "1") == "1"


def insert(name, t0, t1, back, how_in="dissolve", how_out="dissolve", push=(0.5, 0.5, 1.0, 0.5, 0.45, 1.08), grade=None, texts=()):
    if not (art / f"{name}.png").exists():
        print(f"[shot] 없음: {name} — 건너뜀")
        return
    sid = "x_" + name
    s = f.set(sid, f"{name}.png")
    for tid, txt, x, y, size, color in texts:
        s.text(tid, txt, x, y, size=size, color=color, rot=-2, card=True)
    f._show(t0, sid, how_in, .5 if how_in != "cut" else 0, back)
    x0, y0, s0, x1, y1, s1 = push
    f._cam(t0, sid, s.pw * x0, s.ph * y0, s0, .05)
    f._cam(t0 + .05, sid, s.pw * x1, s.ph * y1, s1, max(.5, t1 - t0), "sine.inOut")
    if grade:
        f._grade(t0, sid, grade, .05)
    for k, (tid, *_r) in enumerate(texts):
        f._enter(t0 + .6 + k * 1.2, tid, "write", .7)
    f._show(t1, back, how_out, .4 if how_out != "cut" else 0, sid)


if SHOTS:
    insert("sh_hand86", T(2, .5), E(2) + .25, "cls")
    insert("sh_write86", T(5) - .1, E(5) + .1, "cls", push=(0.45, 0.5, 1.0, 0.55, 0.5, 1.1))
    insert("sh_shock88", T(13) + .5, T(15) - .2, "cls", how_out="cut", push=(0.5, 0.45, 1.0, 0.5, 0.4, 1.12))
    insert("sh_bart32", T(25) - .1, E(25) + .1, "c32")
    insert("sh_film74", T(32, .15), W("짧은", 32) - .05, "lab", how_out="cut", push=(0.5, 0.5, 1.0, 0.55, 0.45, 1.1))
    insert("sh_check74", T(44) - .1, T(45) - .3, "lab", how_out="cut", push=(0.5, 0.5, 1.0, 0.5, 0.5, 1.15))
    insert("sh_interview95", T(56, .3), E(56) + .1, "r95")
    insert("sh_mall", T(57) + .85, E(57) + .15, "mall", grade="sepia(.4) saturate(.85)", push=(0.5, 0.5, 1.0, 0.48, 0.5, 1.1))
    insert("sh_rat00", T(76, .45), E(76) + .1, "rl")
    insert("sh_write01", T(104, .5), E(104) + .1, "lg")
    insert("sh_lineup84", T(117) - .1, E(117) + .1, "ct", grade="saturate(.75) brightness(.92)")
    insert("sh_family", T(129) - .1, E(130) + .1, "hm")
    insert("sh_ask", T(139) + .35, E(139) + .15, "hm",
           texts=[("aq1", "'그 사람이 때렸지?'", 470, 700, 58, "#8a8a8a"), ("aq2", "'무슨 일이 있었어?'", 1250, 560, 64, "#2f5d8a")])
    insert("sh_drawer", T(143, .3), E(143) + .1, "dn", push=(0.5, 0.55, 1.0, 0.5, 0.6, 1.12))

f.html(a.out)
print("ok", a.out, END)
if MISS:
    print("낱말 못 찾음(문장 시작으로):", " ".join(MISS))
