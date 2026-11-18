"""AI 편 「AI 가 내 카드로 결제를 시작했다 — 그런데 가게들은 왜 문을 닫을까」 앞부분 0:00–1:05.

화풍: 합격한 민트색 플랫 제품 일러스트(화풍만). 연출은 새로: 작은 에이전트 로봇이 주인공으로 직접 겪는다 —
항공사 탑승구에서 막히고(11일), 이틀 뒤 지갑을 받고·가게와 악수하고·밤새 일하고(13일), 마지막엔 '지갑은 쥐었는데 문은 잠긴' 두 화면.
    python scripts/anim/ep_ai.py <art 폴더> <words.json> <out.html>
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from anim import Film  # noqa: E402

art, words, out = map(Path, sys.argv[1:4])
END = 635.8
f = Film("ai-guide", art / "ai-guide", words, END)
A = f.at
NAVY = "#18334a"

def label(st, tid, s, x, y, size=64, color=NAVY, rot=0, z=9):   # 제품 설명 화풍: 고딕, 기울임 없음
    st.text(tid, s, x, y, size=size, color=color, font="gothic", rot=rot, z=z)

# ── 11월 11일, 탑승구 ───────────────────────────────────
ap = f.set("airport", "airport.png", focus=(1100, 600, 1.2))
ap.actor("ag1", ["agent_walk", "agent_stop", "agent_proud", "agent_work"], x=-150, y=990, h=330)
ap.prop("stop", "hand_stop", 1470, 470, 400, z=8)
ap.prop("lock1", "padlock", 1690, 650, 170, z=9)
label(ap, "d11", "11월 11일 (수)", 760, 300, 70)
label(ap, "dua", "허락 없는 AI 예약 → 차단", 760, 400, 54, "#b5452e")
f._show(0, "airport", "cut")
f._setv(0, "#airport", {"opacity": 0})
f._tween(0, "#airport", {"opacity": 1}, .8)
f._cam(0, "airport", 960, 540, 1.0, 3)
A("2026").enter("d11", "write", .8)
A("고객이").leave("d11", "fade", .4)
A("에이전트가", after=8).walk("ag1", 1350, 4.2, bob=12)
A("에이전트가", after=8).cam("airport", 1150, 640, 1.15, 4.2)
t = f.cue("맞겠다는")
f._enter(t, "stop", "slide", .5, dx=-700)
f._pose(t + .1, "ag1", "agent_stop")
f._enter(t + .25, "lock1", "drop", .7)
f._sound(t, "whoosh-short", .3)
f._sound(t + .8, "impact-bass-1", .25)
f._enter(t + .2, "dua", "write", .6)

# ── 다른 길도 모두 ─────────────────────────────────────
st = f.set("street", "street.png", focus=(960, 560, 1.0))
st.actor("ag2", ["agent_walk", "agent_stop", "agent_proud", "agent_work"], x=-150, y=905, h=290)
for i, x in enumerate([990, 1365, 1725]):
    st.prop(f"slock{i}", "padlock", x, 640, 130, z=7)
label(st, "s1", "항공사 앱", 990, 470, 46)
label(st, "s2", "홈페이지", 1365, 470, 46)
label(st, "s3", "여행사·비교 사이트", 1725, 470, 46)
t = f.cue("자사액")
f._show(t - .3, "street", "push", .7, "airport")
f._sound(t - .3, "whoosh", .2)
f._walk(t, "ag2", 950, 3.6, bob=10)
for i, w in enumerate(["자사액", "홈페이지", "여행사"]):
    tt = f.cue(w, after=15)
    f._enter(tt, f"slock{i}", "drop", .6)
    f._enter(tt, f"s{i+1}", "write", .4)
    f._sound(tt + .5, "click", .25)
f._pose(f.cue("포함해서요") , "ag2", "agent_stop")

# ── 13일 금요일: 지갑·악수 ───────────────────────────────
label(st, "d13", "11월 13일 (금)", 960, 90, 70)
st.prop("give", "hand_give", 230, 560, 520, z=8)
st.prop("card", "card", 500, 500, 210, z=8, rot=-8)
st.prop("shake", "handshake", 980, 470, 500, z=8)
label(st, "pp", "에이전트 ↔ 가게 공용 규칙 1.0", 900, 200, 50)
t = f.cue("이틀")
f._tween(t, "#street", {"filter": "brightness(1.08)"}, .6)
for i in range(3):
    f._leave(t, f"slock{i}", "fade", .4)
    f._leave(t, f"s{i+1}", "fade", .4)
f._move(t + .2, "ag2", dx=-300, dur=.01)
f._pose(t + .2, "ag2", "agent_walk")
f._cam(t, "street", 700, 600, 1.3, 1.4)
f._enter(t + .2, "d13", "write", .6)
f._sound(t, "whoosh-short", .2)
f._leave(f.cue("오픈") - .3, "d13", "fade", .3)
t = f.cue("오픈")
f._enter(t, "give", "slide", .8, dx=600)
f._sound(t, "whoosh-short", .2)
t = f.cue("결제하는")
f._pose(t - .6, "ag2", "agent_proud")
f._sound(t - .6, "sparkle", .2)
f._move(t - .4, "give", dx=-500, dur=.6, ease="power2.in")
f._enter(f.cue("카드로", after=30), "card", "pop", .5)
f._move(f.cue("카드로", after=30) + .5, "card", dy=-14, dur=1.2, ease="sine.inOut")
t = f.cue("가게가")
f._leave(t - .4, "card", "shrink", .3)
f._enter(t, "shake", "pop", .6)
f._sound(t, "pop", .25)
f._enter(f.cue("공용"), "pp", "write", .7)

# ── 계속 일하는 에이전트 ─────────────────────────────────
nt = f.set("night", "night.png", focus=(1300, 560, 1.15))
nt.actor("ag3", ["agent_work", "agent_walk", "agent_stop", "agent_proud"], x=1330, y=708, h=240)
label(nt, "always", "부르지 않아도, 계속", 700, 160, 60, "#e8fff6")
t = f.cue("엔트로픽")
f._show(t - .2, "night", "dissolve", .8, "street")
f._sound(t - .2, "whoosh", .18)
f._cam(t, "night", 1200, 560, 1.0, 4.5)
f._enter(f.cue("부르지"), "always", "write", .7)
for k in range(9):   # 타자 치는 몸짓 — 작게 들썩
    f._tween(t + .3 + k * .45, "#ag3 .sq", {"y": -6}, .15, "sine.out")
    f._tween(t + .45 + k * .45, "#ag3 .sq", {"y": 0}, .2, "sine.in")
f._sound(f.cue("부르지"), "typing", .15)

# ── 지갑은 쥐었는데, 문은 잠겼다 ─────────────────────────
t = f.cue("한쪽에서는")
f._setv(t, "#street", {"opacity": 1, "zIndex": 3, "clipPath": "inset(0 50% 0 0)", "filter": "none"})
f._setv(t, "#airport", {"opacity": 1, "zIndex": 2, "clipPath": "inset(0 0 0 50%)"})
f._setv(t, "#night", {"opacity": 0})
f._leave(t, "shake", "fade", .1)
f._leave(t, "pp", "fade", .1)
f._leave(t, "dua", "fade", .1)
f._cam(t, "street", 960, 560, 1.15, .01)
f._move(t, "ag2", dx=-250, dur=.01)
f._pose(t, "ag2", "agent_proud")
f._cam(t, "airport", 1040, 600, 1.15, .01)
f._sound(t, "whoosh", .25)
label(st, "lw", "지갑을 쥐여 주고", 520, 330, 62)
label(ap, "lr", "문은 잠그고", 1450, 880, 66, "#b5452e")
f._enter(f.cue("지갑을"), "lw", "write", .5)
f._enter(f.cue("잠근"), "lr", "write", .4)
f._tween(f.cue("잠근"), "#lock1 .mv", {"scale": 1.25}, .15, "power2.out")
f._tween(f.cue("잠근") + .15, "#lock1 .mv", {"scale": 1}, .4, "elastic.out(1,.5)")
f._sound(f.cue("잠근"), "click", .35)

# ── 그렇다면, 지금 정말 될까 ──────────────────────────────
label(st, "q1", "지금 정말 될까?", 1180, 230, 84)
label(st, "q2", "무엇이 막고 있나?", 1180, 230, 84, "#b5452e")
t = f.cue("그렇다면")
f._tween(t, "#street", {"clipPath": "inset(0 0% 0 0)"}, .8, "power3.inOut")
f._leave(t, "lw", "fade", .3)
f._sound(t, "whoosh-short", .2)
f._cam(t, "street", 960, 560, 1.0, 1.0)
f._walk(t + .3, "ag2", 650, 2.0, bob=10)
f._pose(t + .3, "ag2", "agent_walk")
st.prop("slock9", "padlock", 990, 640, 150, z=7)
f._enter(f.cue("사는"), "slock9", "drop", .6)
f._pose(f.cue("사는") + .4, "ag2", "agent_stop")
f._sound(f.cue("사는") + .5, "click", .3)
f._enter(f.cue("정말"), "q1", "write", .6)
t = f.cue("되지")
f._leave(t - .2, "q1", "fade", .2)
f._enter(t, "q2", "write", .6)
f._cam(t, "street", 960, 600, 1.35, 2.2)
from ep_ai_rest import rest  # noqa: E402
rest(f, A)

f.html(out)
print("ok", out)
