"""시사 편 「대만은 어떻게 한국을 앞질렀나 — 같은 AI 붐, 다른 길」 앞부분 0:00–1:23.

화풍: 합격한 시사 지면 삽화(화풍만). 연출은 새로: 발표장 화면에 숫자가 올라가고, '네 마리 용'은 실제 연이 되어 하늘에 떠서
대만의 연이 한국의 연을 앞질러 오른다. 원화·달러 환산은 환전 창구에서 같은 돈이 바뀌는 장면, 두 나라는 한 하늘 아래 두 도시.
    python scripts/anim/ep_issues.py <art 폴더> <words.json> <out.html>
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from anim import Film  # noqa: E402

art, words, out = map(Path, sys.argv[1:4])
END = 613.1
f = Film("issues", art / "issues", words, END)
A = f.at
INK, RED, GRN = "#1f2a33", "#b23b2a", "#2f6b4a"

def ink(st, tid, s, x, y, size=60, color=INK, z=9, shadow=True):
    st.text(tid, s, x, y, size=size, color=color, font="serif", rot=0, z=z, shadow=shadow, card=shadow)

# ── 3월 10일, 한국은행 발표장 ─────────────────────────────
b = f.set("brief", "briefing.png", focus=(1125, 330, 1.6))
ink(b, "bd", "2026. 3. 10 · 한국은행", 1125, 150, 46, INK, shadow=False)
ink(b, "bt", "2025년 1인당 국민총소득", 1125, 215, 42, "#4a5560", shadow=False)
b.counter("kr", 1125, 290, 92, INK, text="0")
b.text("krn", "한국", 820, 310, size=44, color=INK, font="serif", rot=0, shadow=False)
b.counter("tw", 1125, 400, 92, RED, text="0")
b.text("twn", "대만", 820, 420, size=44, color=RED, font="serif", rot=0, shadow=False)
ink(b, "fix", "6월 수정", 1430, 285, 34, RED, shadow=False)
f._show(0, "brief", "cut")
f._setv(0, "#brief", {"opacity": 0})
f._tween(0, "#brief", {"opacity": 1}, .8)
f._cam(0, "brief", 960, 540, 1.0, .01)
f._cam(.3, "brief", 1125, 340, 1.55, 4.5, "power2.inOut")
A("2026").enter("bd", "write", .8)
A("번소득을").enter("bt", "write", .6)
A("1인당").enter("krn", "write", .3)
f._count(f.cue("3만"), "kr", 0, 36855, 1.6, suf=" 달러")
A("3만").sound("click-soft", .25)
t = f.cue("고친")
f._count(t + .4, "kr", 36855, 36963, .9, suf=" 달러")
f._enter(t + .4, "fix", "write", .4)
f._sound(t + .4, "click-soft", .3)
t = f.cue("대만은")
f._enter(t, "twn", "write", .3)
f._count(t, "tw", 0, 40585, 1.4, suf=" 달러")
f._tween(t + 1.5, "#tw", {"scale": 1.08}, .2, "power2.out")
f._tween(t + 1.7, "#tw", {"scale": 1}, .4, "elastic.out(1,.5)")

# ── 네 마리 용: 연이 하늘로 ───────────────────────────────
k = f.set("sky", "sky.png", focus=(960, 540, 1.0))
kites = [("kite_a", "한국", 560), ("kite_b", "대만", 860), ("kite_c", "홍콩", 1160), ("kite_d", "싱가포르", 1460)]
for i, (pc, nm, x) in enumerate(kites):
    k.raw(f'<div id="kw{i}" style="position:absolute;left:{x}px;top:1250px"><div class="sway">'
          f'<img src="{(f.art / (pc + ".png")).as_uri()}" style="position:absolute;width:190px;left:-95px;top:0">'
          f'<div style="position:absolute;top:-62px;left:-150px;width:300px;text-align:center;font-family:Myeongjo;font-size:40px;color:{INK};'
          f'text-shadow:0 0 12px #fff,0 0 4px #fff">{nm}</div></div></div>', z=6)
t = f.cue("1990")
f._show(t - .2, "sky", "wipe", .9, "brief")
f._sound(t - .2, "whoosh", .22)
for i in range(4):
    f._tween(f.cue("4마리") + i * .18, f"#kw{i}", {"top": 300 + (i % 2) * 30}, 1.8, "power2.out")
    f._sound(f.cue("4마리") + i * .18, "whoosh-short", .1)
# 바람에 흔들림(연만, 화면은 그대로)
for i in range(4):
    for n in range(0, int(END), 2):
        f._tween(n + i * .3, f"#kw{i} .sway", {"rotation": 4 if (n // 2) % 2 else -4, "transformOrigin": "50% 0%"}, 2, "sine.inOut")
t = f.cue("대만보다")
f._tween(t, "#kw0", {"top": 420}, 1.6, "power2.inOut")      # 한국 연이 내려오고
f._tween(t, "#kw1", {"top": 140}, 1.6, "power2.inOut")      # 대만 연이 올라선다
f._tween(t, "#kw1", {"left": 620}, 1.6, "power2.inOut")
f._tween(t, "#kw0", {"left": 800}, 1.6, "power2.inOut")
ink(k, "k20", "20여 년 만에", 1400, 860, 56, RED)
f._enter(f.cue("20여년"), "k20", "write", .6)

# ── 같은 소득, 다른 통화 ─────────────────────────────────
e = f.set("exch", "exchange.png", focus=(960, 600, 1.0))
e.prop("won", "won", 620, 880, 360, z=6, anchor="bottom")
e.prop("dol", "dollar", 1200, 900, 360, z=6, anchor="bottom")
e.counter("wp", 1635, 245, 84, "#a8e6b8", text="")
e.counter("dp", 1635, 445, 84, "#ffb7a3", text="")
ink(e, "wl", "원화로 세면", 1635, 180, 40, "#f3ead8", shadow=False)
ink(e, "dl", "달러로 세면", 1635, 380, 40, "#f3ead8", shadow=False)
ink(e, "rank", "소득은 늘었는데, 순위는 밀렸다", 960, 160, 58, INK)
t = f.cue("그런데", after=29)
f._show(t, "exch", "push", .8, "sky")
f._sound(t, "whoosh", .22)
f._cam(t, "exch", 1150, 560, 1.0, .01)
t = f.cue("원화로")
f._enter(t, "wl", "write", .4)
f._enter(f.cue("5257"), "won", "drop", .8)
f._sound(f.cue("5257") + .5, "impact-bass-2", .15)
f._count(f.cue("4", after=38.5), "wp", 0, 4.6, 1.0, pre="+", suf="%", dec=1)
t = f.cue("달러로는")
f._enter(t, "dl", "write", .4)
f._enter(t + .2, "dol", "slide", .7, dx=-300)
f._count(f.cue("0", after=t), "dp", 0, 0.3, .8, pre="+", suf="%", dec=1)
f._sound(t + .3, "whoosh-short", .2)
t = f.cue("원화로는")
f._tween(t, "#wp", {"scale": 1.12}, .25, "power2.out")
f._tween(t + .25, "#wp", {"scale": 1}, .4, "elastic.out(1,.5)")
f._enter(f.cue("소득은"), "rank", "write", .9)

# ── 대만은 어떻게? (다시 하늘) ────────────────────────────
ink(k, "q1", "인구는 절반, 그런데 어떻게?", 760, 690, 62, INK)
ink(k, "q2", "정말 한국이 뒤처졌다는 뜻일까?", 960, 700, 62, RED)
t = f.cue("인구가")
f._show(t - .2, "sky", "dissolve", .7, "exch")
f._leave(t - .2, "k20", "fade", .1)
f._cam(t, "sky", 760, 420, 1.25, 3)
f._enter(t + .4, "q1", "write", .8)
t = f.cue("역전은")
f._leave(t - .3, "q1", "fade", .3)
f._enter(t, "q2", "write", .8)
f._cam(t, "sky", 960, 540, 1.0, 2)
ink(k, "asof", "11월 17일 기준 자료", 1650, 80, 36, "#4a5560", shadow=True)
f._enter(f.cue("11월", after=60), "asof", "write", .5)

# ── 한 하늘 아래 두 도시 ─────────────────────────────────
c = f.set("cities", "cities.png", w=2600, focus=(700, 700, 1.0))
c.prop("dram", "dram", 760, 640, 560, z=7)
c.prop("gpu", "gpu", 1980, 640, 330, z=7)
ink(c, "mk", "한국 — 메모리", 760, 400, 72, INK)
ink(c, "tk", "대만 — 파운드리·서버", 1980, 400, 72, RED)
ink(c, "ai", "AI", 1300, 260, 150, "#fff7ea", shadow=False)
t = f.cue("두", after=66)
f._show(t - .3, "cities", "dissolve", .9, "sky")
f._sound(t - .3, "whoosh", .2)
f._cam(t, "cities", 1900, 700, 1.0, 4.2)
t = f.cue("바람이")
f._cam(t, "cities", 1300, 760, .8, 3.0)
f._enter(f.cue("인공지능"), "ai", "write", .6)
f._sound(f.cue("인공지능"), "whoosh-cinematic", .2)
t = f.cue("길은", after=80)
f._leave(t - .5, "ai", "fade", .4)
f._enter(t - .3, "dram", "drop", .8)
f._enter(t - .1, "gpu", "drop", .8)
f._enter(t + .3, "mk", "write", .5)
f._enter(t + .4, "tk", "write", .5)
from ep_issues_rest import rest  # noqa: E402
rest(f, A)

f.html(out)
print("ok", out)
