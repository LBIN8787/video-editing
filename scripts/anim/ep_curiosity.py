"""호기심 편 「시계는 똑같이 가는데, 왜 1년은 점점 짧아질까」 앞부분 0:00–1:30 — 원화를 층으로 움직이는 새 연출.

화풍: 합격한 캐주얼 셀 애니메이션(Codex 원화의 화풍만). 연출은 새로: 인물이 걸어 들어오고 자세·표정으로 연기,
카메라는 이야기의 시점이 옮겨 갈 때만 천천히, 장면 사이는 의미가 이어지는 전환(달력 → 여름 → 사무실 → 같은 30일 나란히).
    python scripts/anim/ep_curiosity.py <art 폴더> <words.json> <out.html>
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from anim import Film  # noqa: E402

art, words, out = map(Path, sys.argv[1:4])
END = 593.1
f = Film("curiosity", art / "curiosity", words, END)
A = f.at

# ── 1877 파리 ─────────────────────────────────────────────
s = f.set("paris", "paris.png", focus=(1250, 430, 1.35))
s.actor("janet", ["janet_walk", "janet_read", "janet_think", "janet_point"], x=-260, y=1045, h=760)
s.text("t1877", "1877 · 파리", 640, 170, size=104, rot=-3)
s.text("tillu", "내부의 착시", 1180, 170, size=104, color="#5a2a1a", rot=-2)
for i in range(6):
    s.prop(f"pg{i}", "calpage", 2150 + i * 90, 300 + (i % 3) * 140, 150 - i * 6, z=8, rot=-10 + i * 7)
for i, y in enumerate(["1877", "1925", "1980", "2026"]):
    s.text(f"yr{i}", y, 1180, 120, size=120, color="#5a2a1a", rot=-2)

f._show(0, "paris", "cut")
f._setv(0, "#paris", {"opacity": 0})
f._tween(0, "#paris", {"opacity": 1}, 1.2)
f._cam(0, "paris", 960, 540, 1.0, 4.2)
A("1877").enter("t1877", "write", 1.0)
A("철학자", d=-0.4).walk("janet", 1300, 3.6, bob=10)
A("철학자", d=-0.4).sound("whoosh-short", .12)
A("실었습니다").pose("janet", "janet_read")
A("실었습니다").leave("t1877", "fade", .6)
A("내부의").cam("paris", 1040, 520, 1.22, 1.6)
A("내부의").enter("tillu", "write", .9)
A("내부의").sound("pop", .2)
A("안쪽에서").pose("janet", "janet_think")
# 누구나 겪어 본 착시 → 달력 장이 바람에 날려 거리를 가로지른다, 점점 빨리
t0 = f.cue("누구나")
for i in range(6):
    st = t0 + [0, 1.6, 2.8, 3.7, 4.3, 4.7][i]
    f._enter(st, f"pg{i}", "fade", .2)
    f._move(st, f"pg{i}", dx=-2700, dy=180 + i * 30, dur=[2.6, 2.3, 2.0, 1.7, 1.5, 1.3][i], rot=-200 - i * 40, ease="sine.in")
    f._sound(st + .3, "whoosh-short", .12)
A("짧아진다는").cam("paris", 960, 540, 1.0, 2.0)
A("설명은").pose("janet", "janet_point")
A("설명은").leave("tillu", "fade", .5)
# 140년 → 같은 설명이 시대를 건너 꺼내 들린다 (연도가 바뀌고 화면이 바래 간다)
A("140년").grade("paris", "sepia(.55) saturate(.8)", 1.5)
A("140년").cam("paris", 1080, 560, 1.1, 6)
for i, w in enumerate(["140년", "들면", "때마다", "들었습니다"]):
    t = f.cue(w)
    f._enter(t, f"yr{i}", "write", .4)
    f._sound(t, "click-soft", .25)
    if i < 3:
        f._leave(f.cue(["들면", "때마다", "들었습니다"][i]) - .05, f"yr{i}", "fade", .15)

# ── 지금, 11월의 방 ─────────────────────────────────────
r = f.set("room", "room.png")
r.actor("woman", ["woman_look", "woman_sigh", "woman_turn", "woman_flip"], x=980, y=1050, h=800)
r.prop("cal", "calendar", 1720, 470, 320, hidden=False, z=4)
r.text("calm", "11월", 1720, 352, size=58, color="#fff8ee", rot=0, shadow=False)
r.prop("clk", "clockface", 1500, 190, 200, z=4)
r.raw('<svg id="hands" style="position:absolute;left:1400px;top:90px;opacity:0" width="200" height="200" viewBox="-100 -100 200 200">'
      '<g id="hh"><path d="M0 6 L0 -42" stroke="#5a3a26" stroke-width="7" stroke-linecap="round"/></g>'
      '<g id="mh"><path d="M0 8 L0 -62" stroke="#5a3a26" stroke-width="5" stroke-linecap="round"/></g>'
      '<g id="sh"><path d="M0 12 L0 -70" stroke="#b5452e" stroke-width="2.5" stroke-linecap="round"/></g>'
      '<circle r="6" fill="#5a3a26"/></svg>', z=5)
for i in range(5):
    r.prop(f"tear{i}", "calpage", 1720, 520, 270, z=6)
r.text("tsigh", "벌써 한 해가…", 760, 170, size=92, rot=-3)

t = f.cue("그리고", after=37.9)
f._show(t, "room", "push", .9, "paris")
f._enter(t + .9, "calm", "write", .3)
f._sound(t - .1, "whoosh", .25)
A("달력").cam("room", 1450, 470, 1.3, 1.8)
A("달력").pose("woman", "woman_look")
A("말을").cam("room", 1150, 560, 1.05, 1.6)
A("벌써").pose("woman", "woman_sigh")
A("벌써").enter("tsigh", "write", 1.0)
t = f.cue("시계는")
f._leave(t - .2, "tsigh", "fade", .4)
f._enter(t, "clk", "pop", .5)
f._setv(t + .25, "#hands", {"opacity": 1})
f._cam(t, "room", 1480, 330, 1.45, 1.4)
f._sound(t, "pop", .2)
for k in range(8):   # 초침이 똑같은 속도로
    f._spin(t + .3 + k, "#sh", 6, .12, "back.out(3)")
    f._sound(t + .3 + k, "click-soft", .08)
f._setv(t, "#mh", {"rotation": 50, "svgOrigin": "0 0"})
f._setv(t, "#hh", {"rotation": 300, "svgOrigin": "0 0"})
f._setv(t, "#sh", {"svgOrigin": "0 0"})
t = f.cue("1년은")
f._cam(t, "room", 1300, 520, 1.1, 1.2)
f.at("1년은").pose("woman", "woman_flip")
for i in range(5):   # 달력이 한 장씩, 점점 빨리 넘어간다
    st = t + .5 + [0, .7, 1.2, 1.55, 1.8][i]
    f._enter(st, f"tear{i}", "fade", .05)
    f._move(st, f"tear{i}", dx=-520 - i * 60, dy=640, dur=1.1, rot=-90 - i * 20, ease="power1.in")
    f._leave(st + .9, f"tear{i}", "fade", .2)
    f._sound(st, "whoosh-short", .14)
A("짧아지는").pose("woman", "woman_turn")

# ── 어린 시절의 여름방학 ───────────────────────────────
su = f.set("summer", "summer.png", w=2400, focus=(1200, 420, 1.0))
su.actor("kid", ["kid_wow", "kid_run", "kid_dragonfly", "kid_wave"], x=-250, y=1335, h=560, show="kid_run")
su.text("tgae", "개학", 1880, 560, size=46, color="#7a2f22", rot=0)
t = f.cue("어린")
f._show(t, "summer", "iris", 1.0, "room")
f._sound(t, "whoosh", .25)
f._cam(t, "summer", 1200, 620, 1.0, 3.2)
A("여름방학을").walk("kid", 1150, 2.4, bob=22)
A("이상할").cam("summer", 1200, 675, .8, 3.0)
A("이상할").pose("kid", "kid_wow")
A("까마득").enter("tgae", "write", .6)
A("까마득").cam("summer", 1500, 600, .8, 2.0)
A("하루하루").leave("tgae", "fade", .5)
A("하루하루").cam("summer", 1000, 860, 1.0, 1.6)
A("바닷가").hop("kid", -320, .8, 50)
A("바닷가").pose("kid", "kid_wow")
A("바닷가").cam("summer", 640, 820, 1.05, 1.3)
A("잠자리").pose("kid", "kid_dragonfly")
A("잠자리").cam("summer", 620, 1000, 1.55, 1.1)
A("잠자리").sound("pop", .18)
A("버스").hop("kid", 820, 1.0, 70)
A("버스").pose("kid", "kid_wave")
A("버스").cam("summer", 1450, 900, 1.0, 1.4)

# ── 어른의 한 달 ─────────────────────────────────────────
o = f.set("office", "office.png")
o.actor("worker", ["worker_tired", "worker_type", "worker_look", "worker_rush"], x=1270, y=1050, h=780, show="worker_tired")
o.prop("ocal", "calendar", 1640, 470, 330, hidden=False, z=4)
o.text("dmon", "월", 1640, 520, size=150, color="#7a2f22", rot=0, shadow=False)
o.text("dfri", "금", 1640, 520, size=150, color="#7a2f22", rot=0, shadow=False)
for i in range(6):
    o.prop(f"otear{i}", "calpage", 1640, 520, 290, z=6)
t = f.cue("어른이")
f._show(t, "office", "dissolve", 1.0, "summer")
f._sound(t, "whoosh", .2)
f._cam(t, "office", 1100, 560, 1.0, 1)
A("월요일").enter("dmon", "write", .3)
A("월요일").sound("click-soft", .3)
A("월요일").cam("office", 1300, 540, 1.15, 1.2)
t = f.cue("금요일")
f._leave(t - .1, "dmon", "fade", .1)
f._enter(t, "dfri", "write", .2)
f._sound(t, "click-soft", .35)
f._pose(t, "worker", "worker_look")
t = f.cue("넘기는가")
f._leave(t, "dfri", "fade", .2)
for i in range(6):
    st = t + [0, 1.9, 2.3, 2.6, 2.8, 2.95][i]
    f._enter(st, f"otear{i}", "fade", .05)
    f._move(st, f"otear{i}", dx=-700 - i * 40, dy=700, dur=1.0, rot=-120 - i * 15, ease="power1.in")
    f._leave(st + .85, f"otear{i}", "fade", .15)
    f._sound(st, "whoosh-short", .15)
A("때가").pose("worker", "worker_tired")

# ── 같은 30일, 나란히 ───────────────────────────────────
o.text("l30b", "30일", 1270, 150, size=96, color="#2b2118", rot=0)
su.text("l30a", "30일", 960, 640, size=96, color="#2b2118", rot=0)
t = f.cue("같은", after=82.7)
f._setv(t, "#summer", {"opacity": 1, "zIndex": 3, "clipPath": "inset(0 50% 0 0)", "x": 0, "y": 0})
f._setv(t, "#office", {"zIndex": 2})
f._grade(t, "summer", "sepia(0) saturate(1)", .01)
f._cam(t, "summer", 1440, 900, 1.0, .01)
f._move(t, "kid", dx=-440, dur=.01)
f._cam(t, "office", 800, 560, 1.2, .01)
f._enter(t + .3, "l30a", "write", .4)
f._enter(t + .3, "l30b", "write", .4)
f._sound(t, "whoosh", .25)
t = f.cue("끝없이")
f._tween(t, "#summer", {"clipPath": "inset(0 20% 0 0)"}, 1.4, "power2.inOut")


t = f.cue("깜짝")
f._tween(t - .1, "#summer", {"clipPath": "inset(0 3% 0 0)"}, .35, "power3.in")

f._sound(t - .1, "whoosh-short", .3)
from ep_curiosity_rest import rest  # noqa: E402
rest(f, A)
from bench_cur import apply as bench  # noqa: E402  (docs/47 반영: 검은 화면 한 줄·번호 정리·실제 인물 사진)
bench(f, A, Path("G:/내 드라이브/ytflow/refs/people"))

f.html(out)
print("ok", out)
