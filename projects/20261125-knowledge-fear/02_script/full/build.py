"""불안 편 전체 (대본 v2, 49문장 · 약 6분 20초). 모션그래픽 중심 + 실제 자료(다윈 사진·1872 책·도판).
사용자 11-25: "사물보다는 모션그래픽 등을 활용해주세요 미주일기식으로요" · "일단은 이대로 영상 한번 만들어주세요"."""
import json, math, random, re, subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
L = json.load(open(HERE / "assets/vo/lines.json", encoding="utf-8"))
GAP, LEAD, CHGAP = 0.22, 0.5, 0.6
t = LEAD
for k, x in enumerate(L):
    if k and x["ch"] != L[k - 1]["ch"]:
        t += CHGAP
    x["start"] = round(t, 2); t += x["dur"] + GAP
END = round(t + 1.5, 2)

# 장면 = (id, 첫 문장, 어두운 바탕?)
PLAN = [("a1", 0, 0), ("a2", 1, 0), ("a3", 3, 0), ("a4", 5, 0),
        ("b1", 9, 0), ("b2", 11, 0), ("b3", 12, 0), ("b4", 14, 0), ("b5", 18, 0),
        ("c1", 19, 1), ("c2", 21, 1), ("c3", 22, 1), ("c4", 23, 1),
        ("d1", 25, 0), ("d2", 29, 0), ("d3", 31, 1),
        ("e1", 33, 1), ("e2", 35, 0), ("e3", 37, 0),
        ("f1", 39, 1), ("f2", 40, 1), ("f3", 43, 1),
        ("g1", 44, 0), ("g2", 46, 0), ("g3", 48, 1)]
SC = {}
for k, (sid, i0, dark) in enumerate(PLAN):
    st = 0.0 if k == 0 else round(L[i0]["start"] - .25, 2)
    SC[sid] = {"start": st, "dark": dark, "first": i0}
for k, (sid, _, _) in enumerate(PLAN):
    SC[sid]["end"] = SC[PLAN[k + 1][0]]["start"] if k + 1 < len(PLAN) else END
    SC[sid]["dur"] = round(SC[sid]["end"] - SC[sid]["start"], 2)

INK, RED, GRN, VIO, YEL, NAVY, BLU = "#2B2F3A", "#D9483B", "#3FAE76", "#A98BF0", "#E8B931", "#22345F", "#7FB2E5"
LIGHT = "#EDE7DA"


class S:
    def __init__(self, sid):
        self.sid, self.s = sid, SC[sid]
        self.dark = self.s["dark"]
        self.fg = LIGHT if self.dark else INK
        self.body, self.js, self.n = [], [], 0

    def cue(self, i, frac=0.0, off=0.0):
        return round(max(.05, L[i]["start"] + L[i]["dur"] * frac - self.s["start"] + off), 2)

    def add(self, h): self.body.append(h)
    def j(self, s): self.js.append(s)

    def uid(self, p="e"):
        self.n += 1; return f"{self.sid}-{p}{self.n}"

    # ── 붙이기 ──
    def svg(self, inner, sid=None):
        a = f'id="{sid}" ' if sid else ""
        self.add(f'<svg {a}style="position:absolute;left:0;top:0;overflow:visible" width="1920" height="1080">{inner}</svg>')

    def text(self, x, y, s, size=56, color=None, font="pen", extra="", center=False):
        i = self.uid("t"); color = color or self.fg
        al = f"left:0;width:1920px;text-align:center;" if center else f"left:{x}px;"
        fam = {"pen": "Pen", "my": "Myeongjo", "sans": "NotoKR"}[font]
        self.add(f'<div id="{i}" style="position:absolute;{al}top:{y}px;font-family:{fam};font-size:{size}px;color:{color};white-space:nowrap;opacity:0;font-weight:{800 if font == "sans" else 400};{extra}">{s}</div>')
        return i

    def tag(self, x, y, s, bg=RED, fg="#fff", size=40):
        i = self.uid("g")
        self.add(f'<div id="{i}" style="position:absolute;left:{x}px;top:{y}px;padding:8px 26px;border-radius:40px;background:{bg};color:{fg};font-size:{size}px;font-weight:700;white-space:nowrap;opacity:0">{s}</div>')
        return i

    def name(self, x, y, who, what):
        i = self.uid("n")
        bg = "#F6F1E6" if not self.dark else "#2C313B"
        self.add(f'<div id="{i}" style="position:absolute;left:{x}px;top:{y}px;padding:14px 28px;background:{bg};border-left:8px solid {RED};box-shadow:0 10px 20px rgba(0,0,0,.22);opacity:0">'
                 f'<div style="font-size:46px;font-weight:800;color:{self.fg}">{who}</div><div style="font-size:28px;color:{"#9AA0AA" if self.dark else "#6E6A60"};margin-top:2px">{what}</div></div>')
        return i

    def photo(self, x, y, w, h, img, cap="", rot=0, pos="50% 30%"):
        i = self.uid("p")
        self.add(f'<div id="{i}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;padding:14px 14px 10px;background:#FBF9F4;box-shadow:0 14px 26px rgba(30,24,16,.3);transform:rotate({rot}deg);opacity:0">'
                 f'<img src="assets/img/{img}" style="width:{w - 28}px;height:{h}px;object-fit:cover;object-position:{pos}">'
                 f'<div style="font-family:Pen;font-size:36px;color:{INK};text-align:center;margin-top:4px">{cap}</div></div>')
        return i

    # ── 움직임 (역할별 속도) ──
    def pop(self, i, t, d=.3): self.j(f'tl.fromTo("#{i}",{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:{d},ease:"back.out(2.2)"}},{t});')
    def slide(self, i, t, dx=-400, d=.35): self.j(f'tl.fromTo("#{i}",{{opacity:0,x:{dx}}},{{opacity:1,x:0,duration:{d},ease:"power3.out"}},{t});')
    def drop(self, i, t, d=.45): self.j(f'tl.fromTo("#{i}",{{opacity:0,y:-160}},{{opacity:1,y:0,duration:{d},ease:"bounce.out"}},{t});')
    def rise(self, i, t, d=.4): self.j(f'tl.fromTo("#{i}",{{opacity:0,y:60}},{{opacity:1,y:0,duration:{d},ease:"power2.out"}},{t});')
    def fade(self, i, t, d=.35, a=0, b=1): self.j(f'tl.fromTo("#{i}",{{opacity:{a}}},{{opacity:{b},duration:{d}}},{t});')
    def out(self, ids, t, d=.25): self.j(f'tl.to("{",".join("#" + x for x in ids)}",{{opacity:0,duration:{d}}},{t});')
    def stamp(self, i, t): self.j(f'tl.fromTo("#{i}",{{opacity:0,scale:2}},{{opacity:1,scale:1,duration:.22,ease:"power4.in"}},{t});')
    def draw(self, i, t, d=.6, ease="power1.inOut"): self.j(f'tl.fromTo("#{i}",{{drawSVG:"0%"}},{{drawSVG:"100%",duration:{d},ease:"{ease}"}},{t});')
    def spread(self, i, t, d=.5): self.j(f'tl.fromTo("#{i}",{{drawSVG:"50% 50%"}},{{drawSVG:"0% 100%",duration:{d},ease:"power2.out"}},{t});')
    def shake(self, i, t, n=5, amp=10): self.j(f'tl.fromTo("#{i}",{{x:0}},{{x:{amp},duration:.05,repeat:{n},yoyo:true}},{t});')
    def blink(self, i, t, n=3, d=.18): self.j(f'tl.fromTo("#{i}",{{opacity:1}},{{opacity:.15,duration:{d},repeat:{n * 2 - 1},yoyo:true}},{t});')
    def ring(self, i, t, n=2, d=1.0, s=3): self.j(f'tl.fromTo("#{i}",{{scale:.4,opacity:1,transformOrigin:"50% 50%"}},{{scale:{s},opacity:0,duration:{d},repeat:{n - 1},ease:"power1.out"}},{t});')
    def marker(self, i, t, d=.55): self.j(f'tl.fromTo("#{i}",{{backgroundSize:"0% 40%"}},{{backgroundSize:"100% 40%",duration:{d},ease:"power2.out"}},{t});')
    def count(self, i, t, a, b, d=1.0, comma=True):
        v = f'cv{self.uid("c").replace("-", "_")}'
        fmt = 'toLocaleString("en-US")' if comma else 'toString()'
        self.j(f'const {v}={{v:{a}}};tl.fromTo({v},{{v:{a}}},{{v:{b},duration:{d},ease:"power2.out",onUpdate:function(){{document.getElementById("{i}").textContent=Math.round({v}.v).{fmt}}}}},{t});')

    def anotb(self, y, a, b, t_a, t_x, t_b, size=92):
        """'A가 아니라 B' — A 에 줄, B 에 형광펜."""
        ia = self.text(0, y, a, size, font="my", center=True)
        ib = self.uid("b")
        self.add(f'<div style="position:absolute;left:0;width:1920px;top:{y + size + 50}px;text-align:center">'
                 f'<span id="{ib}" class="mk" style="font-family:Myeongjo;font-size:{size}px;color:{RED};opacity:0;display:inline-block">{b}</span></div>')
        ix = self.uid("x")
        self.svg(f'<path id="{ix}" d="M{960 - len(a) * size * .5:.0f},{y + size * .62:.0f} L{960 + len(a) * size * .5:.0f},{y + size * .5:.0f}" stroke="{RED}" stroke-width="10" stroke-linecap="round" fill="none"/>')
        self.rise(ia, t_a); self.draw(ix, t_x, .25); self.pop(ib, t_b, .3); self.marker(ib, t_b + .3)
        return ia, ib, ix

    def fixjs(self):
        seen, out = set(), []
        for x in self.js:
            m = re.match(r'tl\.fromTo\("([^"]+)"', x)
            if m:
                if m.group(1) in seen and "immediateRender" not in x:
                    a, b = x.rsplit("},", 1); x = a + ",immediateRender:false}," + b
                seen.add(m.group(1))
            out.append(x)
        return out

    def html(self):
        bg = "paper_dark.jpg" if self.dark else "paper.jpg"
        d = self.s["dur"]
        return f"""<template>
<style>
@font-face{{font-family:'NotoKR';src:url('assets/fonts/NotoSansKR-VF.ttf');font-weight:100 900}}
@font-face{{font-family:'Pen';src:url('assets/fonts/NanumPenScript-Regular.ttf')}}
@font-face{{font-family:'Myeongjo';src:url('assets/fonts/NanumMyeongjo-ExtraBold.ttf')}}
#root{{position:absolute;inset:0;overflow:hidden;font-family:'NotoKR';color:{self.fg};background:{'#1E2128' if self.dark else '#E8E3D9'}}}
.bg{{position:absolute;inset:-40px;background:url('assets/img/{bg}') center/cover}}
.cam{{position:absolute;inset:0;transform-origin:50% 50%}}
.mk{{background:linear-gradient(rgba(232,185,49,.55),rgba(232,185,49,.55)) no-repeat 0 88%;background-size:0% 40%}}
.dot{{position:absolute;width:14px;height:14px;margin:-7px 0 0 -7px;border-radius:50%;background:#7D8594}}
</style>
<div id="root" data-composition-id="{self.sid}" data-width="1920" data-height="1080" data-layout-allow-overlap>
<div class="bg" id="{self.sid}-bg"></div>
<div class="cam" id="{self.sid}-cam">{''.join(self.body)}</div>
</div>
<script>
gsap.registerPlugin(MotionPathPlugin, DrawSVGPlugin, ScrambleTextPlugin);
const tl = gsap.timeline({{ paused: true }});
tl.fromTo("#{self.sid}-bg", {{x:0}}, {{x:-30, duration:{d}, ease:"none"}}, 0);
tl.fromTo("#{self.sid}-cam", {{scale:1}}, {{scale:1.035, duration:{d}, ease:"sine.inOut"}}, 0);
{''.join(self.fixjs())}
window.__timelines["{self.sid}"] = tl;
</script>
</template>
"""


SCENES = []
def scene(sid):
    c = S(sid); SCENES.append(c); return c

# ═══ 1장 유리 앞의 다윈 ═══════════════════════════════════════════
c = scene("a1")
p1 = c.photo(170, 120, 470, 560, "darwin.jpg", "찰스 다윈", -4)
p2 = c.photo(700, 170, 640, 470, "book.jpg", "『인간과 동물의 감정 표현』", 2, "50% 50%")
p3 = c.photo(1400, 110, 360, 620, "plate7.png", "책 속 도판 · 놀람과 공포", 5, "50% 20%")
y1 = c.text(780, 735, "1872", 120, RED, "my")
cr = c.text(170, 905, "사진: 줄리아 마거릿 캐머런(퍼블릭 도메인) · 책: 레이크스 미술관(CC0) · 도판: 퍼블릭 도메인 — 위키미디어 공용", 22, "#6E6A60", "sans", "font-weight:400")
c.slide(p1, .2, -500)
c.j(f'tl.fromTo("#{y1}",{{opacity:0,textContent:1800}},{{opacity:1,textContent:1872,duration:.8,snap:{{textContent:1}},ease:"power2.out"}},.35);')
c.drop(p2, c.cue(0, .35))
c.fade(cr, c.cue(0, .4))
c.slide(p3, c.cue(0, .7), 500)

c = scene("a2")
GL = f'<rect id="a2-gl" x="930" y="250" width="60" height="460" rx="6" fill="{BLU}" fill-opacity=".35" stroke="{BLU}" stroke-width="5"/>'
SN = 'M1560,560 C 1500,470 1420,650 1350,560 C 1290,480 1220,620 1160,560 C 1120,520 1090,540 1060,560'
c.svg(f'{GL}<path id="a2-sn" d="{SN}" fill="none" stroke="{GRN}" stroke-width="22" stroke-linecap="round"/>'
      f'<circle id="a2-hd" cx="1060" cy="560" r="20" fill="{GRN}"/>'
      f'<circle id="a2-dw" cx="840" cy="480" r="36" fill="{INK}"/><path id="a2-dl" d="M840,520 L840,700" stroke="{INK}" stroke-width="16" stroke-linecap="round"/>'
      f'<path id="a2-ms" d="M560,760 L840,760" stroke="{RED}" stroke-width="6" fill="none"/><path id="a2-m1" d="M560,740 L560,780 M840,740 L840,780" stroke="{RED}" stroke-width="6"/>'
      f'<circle id="a2-fx" cx="990" cy="560" r="60" fill="#fff"/>', "a2-sv")
l_dw = c.text(780, 200, "다윈", 60)
l_gl = c.text(880, 730, "두꺼운 유리", 48, NAVY)
l_sn = c.text(1300, 380, "퍼프애더 (독사)", 52, "#2E7D52")
l_pin = c.text(520, 320, "절대 물러서지 않겠다", 54, RED, extra="transform:rotate(-4deg)")
l_m = c.text(590, 790, "1~2미터", 54, RED)
c.j('tl.set("#a2-fx",{opacity:0},0);')
c.fade(l_dw, .1, .2); c.j('tl.fromTo("#a2-dw,#a2-dl",{opacity:0,scale:.5,transformOrigin:"50% 50%"},{opacity:1,scale:1,duration:.3,ease:"back.out(2)"},.1);')
c.j(f'tl.fromTo("#a2-gl",{{scaleY:0,transformOrigin:"50% 100%"}},{{scaleY:1,duration:.45,ease:"power3.out"}},{c.cue(1, .25)});')
c.fade(l_gl, c.cue(1, .3))
c.draw("a2-sn", c.cue(1, .42), .9, "power2.out"); c.pop("a2-hd", c.cue(1, .5)); c.fade(l_sn, c.cue(1, .5))
c.j(f'tl.fromTo("#{l_pin}",{{opacity:0,scale:1.6}},{{opacity:1,scale:1,duration:.22,ease:"power4.in"}},{c.cue(1, .72)});')
tl2 = c.cue(2, .3)
c.j(f'tl.to("#a2-sn",{{x:-60,duration:.12,ease:"power4.in"}},{tl2});tl.to("#a2-hd",{{x:-70,duration:.12,ease:"power4.in"}},{tl2});')
c.j(f'tl.fromTo("#a2-fx",{{opacity:.9,scale:.3,transformOrigin:"50% 50%"}},{{opacity:0,scale:2.2,duration:.35,immediateRender:false}},{tl2 + .1:.2f});')
c.j(f'tl.to("#a2-dw,#a2-dl",{{x:-280,duration:.18,ease:"power4.out"}},{tl2 + .14:.2f});')
c.j(f'tl.to("#{l_dw}",{{x:-280,duration:.18,ease:"power4.out"}},{tl2 + .14:.2f});')
c.shake(f"{c.sid}-cam", tl2 + .12, 5, 14)
c.out([l_pin], tl2 + .1, .1)
c.draw("a2-ms", c.cue(2, .65), .4); c.fade("a2-m1", c.cue(2, .65), .2); c.pop(l_m, c.cue(2, .72))

c = scene("a3")
q = c.uid("q")
c.add(f'<div id="{q}" style="position:absolute;left:300px;top:240px;width:1320px;padding:46px 60px;background:#FBF9F4;box-shadow:0 18px 30px rgba(30,24,16,.25);opacity:0;transform:rotate(-1deg)">'
      f'<div style="font-family:Myeongjo;font-size:56px;line-height:1.6;color:{INK}">"의지도 이성도, 한 번도 겪어 본 적 없는 위험 앞에서는 <span id="{q}m" class="mk">아무 힘이 없었다</span>"</div>'
      f'<div style="font-size:26px;color:#8A857A;margin-top:24px">찰스 다윈, 『인간과 동물의 감정 표현』(1872) 2장 · 한국어 번역</div></div>')
c.j(f'tl.fromTo("#{q}",{{opacity:0,y:80,rotation:3}},{{opacity:1,y:0,rotation:-1,duration:.45,ease:"power3.out"}},{c.cue(3, .3)});')
c.marker(f"{q}m", c.cue(4, .65), .6)

c = scene("a4")
c.svg(f'<path id="a4-t1" d="M300,380 L1500,380" stroke="#B9B2A3" stroke-width="6" stroke-dasharray="4 14" fill="none"/>'
      f'<path id="a4-t2" d="M300,620 L1500,620" stroke="#B9B2A3" stroke-width="6" stroke-dasharray="4 14" fill="none"/>'
      f'<path id="a4-fin" d="M1500,300 L1500,700" stroke="{INK}" stroke-width="6"/>'
      f'<circle id="a4-hd" cx="300" cy="380" r="26" fill="{NAVY}"/><circle id="a4-bd" cx="300" cy="620" r="26" fill="{RED}"/>')
lh = c.text(110, 350, "머리", 60, NAVY); lb = c.text(140, 590, "몸", 60, RED)
lh2 = c.text(560, 290, "'안전하다'", 50, NAVY); lb2 = c.text(1530, 590, "먼저 도착", 54, RED)
qm = c.text(0, 420, "?", 220, RED, "my", center=True)
al = c.uid("al")
c.svg(f'<g id="{al}" style="opacity:0"><circle cx="960" cy="470" r="70" fill="{RED}"/><circle id="{al}r" cx="960" cy="470" r="70" fill="none" stroke="{RED}" stroke-width="8"/></g>')
q1 = c.text(0, 190, "왜 확인하기도 전에?", 76, INK, "my", center=True)
q2 = c.text(0, 650, "왜 꺼지지 않을까?", 76, RED, "my", center=True)
c.draw("a4-t1", .2, .3); c.draw("a4-t2", .25, .3); c.fade("a4-fin", .3, .2)
c.pop("a4-hd", .4); c.pop("a4-bd", .45); c.fade(lh, .4); c.fade(lb, .45)
c.fade(lh2, c.cue(5, .1))
c.j(f'tl.to("#a4-bd",{{x:1200,duration:.5,ease:"power3.in"}},{c.cue(5, .4)});')
c.j(f'tl.to("#a4-hd",{{x:520,duration:2.6,ease:"none"}},{c.cue(5, .4)});')
c.pop(lb2, c.cue(5, .4, .5))
t6 = c.cue(6, 0)
c.out(["a4-t1", "a4-t2", "a4-fin", "a4-hd", "a4-bd", lh, lb, lh2, lb2], t6)
c.stamp(qm, t6 + .3)
t7 = c.cue(7, 0)
c.out([qm], t7 - .1)
c.rise(q1, t7 + .1)
c.j(f'tl.fromTo("#{al}",{{opacity:0,scale:.5,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:.3,ease:"back.out(2)"}},{c.cue(8, .05)});')
c.ring(f"{al}r", c.cue(8, .1), 4, .9, 3)
c.rise(q2, c.cue(8, .35))

# ═══ 2장 막대기와 뱀 ═════════════════════════════════════════════
c = scene("b1")
c.svg(f'<path id="b1-p1" d="M700,1080 C 820,800 900,600 930,380" stroke="{INK}" stroke-width="7" fill="none"/>'
      f'<path id="b1-p2" d="M1220,1080 C 1100,800 1020,600 990,380" stroke="{INK}" stroke-width="7" fill="none"/>'
      f'<path id="b1-sk" d="M860,640 C 900,600 930,680 970,640 C 1010,600 1040,680 1080,640" stroke="#7A5A3A" stroke-width="18" stroke-linecap="round" fill="none"/>'
      f'<circle id="b1-w" cx="960" cy="960" r="30" fill="{NAVY}"/>')
n1 = c.name(120, 120, "조지프 르두", "신경과학자 · 뉴욕대")
ex = c.text(1010, 790, "!", 150, RED, "my")
wd = c.text(1180, 560, "<span id='b1-sc'>뱀?</span>", 80, RED, "my")
c.slide(n1, .2, -400)
c.draw("b1-p1", c.cue(9, .3), .8); c.draw("b1-p2", c.cue(9, .3), .8)
c.j(f'tl.fromTo("#b1-w",{{opacity:0,y:120}},{{opacity:1,y:0,duration:.4}},{c.cue(9, .6)});')
c.draw("b1-sk", c.cue(10, .1), .5, "power2.out")
c.j(f'tl.to("#b1-w",{{y:-150,duration:1.2,ease:"none"}},{c.cue(10, .05)});')
c.j(f'tl.to("#b1-w",{{y:-130,duration:.12,ease:"power4.out"}},{c.cue(10, .55)});')
c.stamp(ex, c.cue(10, .55))
c.fade(wd, c.cue(10, .3), .2)
c.j(f'tl.to("#b1-sc",{{scrambleText:{{text:"막대기?",chars:"뱀막대기?",speed:.5}},duration:.6}},{c.cue(10, .42)});')
c.j(f'tl.to("#b1-sc",{{scrambleText:{{text:"뱀?",chars:"뱀막대기?",speed:.5}},duration:.4}},{c.cue(10, .5)});')

c = scene("b2")
c.svg(f'<circle id="b2-eye" cx="300" cy="540" r="70" fill="none" stroke="{INK}" stroke-width="8"/><circle id="b2-pu" cx="300" cy="540" r="26" fill="{INK}"/>'
      f'<rect id="b2-bd" x="1500" y="440" width="200" height="200" rx="30" fill="{RED}" fill-opacity=".15" stroke="{RED}" stroke-width="7"/>'
      f'<path id="b2-sh" d="M380,540 L1500,540" stroke="{RED}" stroke-width="16" stroke-dasharray="30 18" fill="none" style="filter:blur(1.5px)"/>'
      f'<path id="b2-lg" d="M370,500 C 600,120 1000,120 1100,300 C 1200,480 1350,380 1500,470" stroke="{GRN}" stroke-width="10" fill="none"/>'
      f'<rect id="b2-jd" x="930" y="150" width="240" height="110" rx="16" fill="#FBF9F4" stroke="{GRN}" stroke-width="6"/>'
      f'<circle id="b2-s1" cx="380" cy="540" r="18" fill="{RED}"/><circle id="b2-s2" cx="370" cy="500" r="18" fill="{GRN}"/>')
le = c.text(240, 650, "눈", 54); lbd = c.text(1555, 655, "몸", 60, RED)
ljd = c.text(975, 172, "판단", 56, GRN, "sans")
ls = c.text(700, 580, "빠르고 흐릿한 길", 52, RED); ll = c.text(560, 90, "느리고 또렷한 길", 52, GRN)
lst = c.text(1100, 300, "'막대기구나'", 50, GRN)
c.pop("b2-eye", .15); c.pop("b2-pu", .25); c.fade(le, .2); c.pop("b2-bd", .3); c.fade(lbd, .3)
c.draw("b2-lg", c.cue(11, .1), 1.0); c.pop("b2-jd", c.cue(11, .2)); c.fade(ljd, c.cue(11, .2)); c.fade(ll, c.cue(11, .25))
c.spread("b2-sh", c.cue(11, .5), .3); c.fade(ls, c.cue(11, .5))
c.j(f'tl.fromTo("#b2-s1",{{opacity:0}},{{opacity:1,duration:.1}},{c.cue(11, .62)});tl.to("#b2-s1",{{x:1120,duration:.45,ease:"power2.in"}},{c.cue(11, .62)});')
c.j(f'tl.fromTo("#b2-s2",{{opacity:0}},{{opacity:1,duration:.1}},{c.cue(11, .62)});tl.to("#b2-s2",{{motionPath:{{path:"#b2-lg",align:"#b2-lg",alignOrigin:[.5,.5]}},duration:2.6,ease:"none"}},{c.cue(11, .62)});')
c.j(f'tl.fromTo("#b2-bd",{{scale:1,transformOrigin:"50% 50%"}},{{scale:1.18,duration:.12,yoyo:true,repeat:1}},{c.cue(11, .62, .45)});')
c.fade(lst, c.cue(11, .62, 1.6), .3)

c = scene("b3")
n1 = c.name(120, 90, "조지프 르두", "1997년 미국 국립보건원 소식지 인터뷰")
c.svg(f'<path id="b3-beam" d="M560,640 L1360,640" stroke="{INK}" stroke-width="12" stroke-linecap="round"/><path id="b3-fu" d="M960,640 L920,760 L1000,760 Z" fill="{INK}"/>', "b3-sv")
k1 = c.uid("k"); k2 = c.uid("k")
c.add(f'<div id="{k1}" style="position:absolute;left:470px;top:470px;width:360px;padding:18px;background:#FBF9F4;border:5px solid {GRN};border-radius:14px;text-align:center;opacity:0">'
      f'<div style="font-family:Pen;font-size:46px">막대기를 뱀으로</div><div style="font-size:30px;color:{GRN};font-weight:800">잠깐 놀람</div></div>'
      f'<div id="{k2}" style="position:absolute;left:1090px;top:470px;width:360px;padding:18px;background:#FBF9F4;border:5px solid {RED};border-radius:14px;text-align:center;opacity:0">'
      f'<div style="font-family:Pen;font-size:46px">뱀을 막대기로</div><div style="font-size:30px;color:{RED};font-weight:800">물림</div></div>')
c.slide(n1, .15, -400)
c.fade("b3-beam", c.cue(13, 0), .2); c.fade("b3-fu", c.cue(13, 0), .2)
c.drop(k1, c.cue(13, .1)); c.drop(k2, c.cue(13, .45))
c.j(f'tl.to("#b3-beam,#{k1},#{k2}",{{rotation:0,duration:.01}},0);')
c.j(f'tl.to("#b3-beam",{{rotation:-8,transformOrigin:"50% 50%",duration:.6,ease:"elastic.out(1,.5)"}},{c.cue(13, .62)});')
c.j(f'tl.to("#{k1}",{{y:-55,duration:.6,ease:"elastic.out(1,.5)"}},{c.cue(13, .62)});tl.to("#{k2}",{{y:55,duration:.6,ease:"elastic.out(1,.5)"}},{c.cue(13, .62)});')

c = scene("b4")
n2 = c.name(1300, 90, "랜돌프 네스", "진화 의학자 · 미시간대")
c.svg(f'<path id="b4-ce" d="M300,160 L1620,160" stroke="{INK}" stroke-width="8"/>'
      f'<g id="b4-det"><ellipse cx="960" cy="190" rx="130" ry="40" fill="#FBF9F4" stroke="{INK}" stroke-width="6"/>'
      f'<path d="M890,190 L1030,190 M910,205 L1010,205" stroke="#9A9486" stroke-width="5"/><circle id="b4-led" cx="1060" cy="185" r="12" fill="#7a7a7a"/></g>'
      f'<circle id="b4-w1" cx="960" cy="200" r="60" fill="none" stroke="{RED}" stroke-width="6"/><circle id="b4-w2" cx="960" cy="200" r="60" fill="none" stroke="{RED}" stroke-width="6"/>'
      f'<g id="b4-to"><rect x="470" y="560" width="230" height="170" rx="40" fill="#C98B45" stroke="#6B4524" stroke-width="7"/>'
      f'<path id="b4-sm" d="M540,540 C 520,500 570,480 550,440 M600,540 C 580,500 630,480 610,440 M660,540 C 640,500 690,480 670,440" stroke="#8A857A" stroke-width="7" fill="none" stroke-linecap="round"/></g>'
      f'<g id="b4-fi"><path d="M1270,740 C 1180,660 1220,560 1280,500 C 1290,560 1320,580 1340,540 C 1400,620 1400,700 1330,740 Z" fill="{RED}"/>'
      f'<path d="M1300,740 C 1260,700 1280,640 1305,610 C 1320,650 1350,660 1345,700 Z" fill="{YEL}"/></g>'
      f'<path id="b4-x" d="M1180,470 L1440,770 M1440,470 L1180,770" stroke="{RED}" stroke-width="14" stroke-linecap="round"/>'
      f'<g id="b4-sc"><path id="b4-bm" d="M560,620 L1360,620" stroke="{INK}" stroke-width="12" stroke-linecap="round"/><path d="M960,620 L920,740 L1000,740 Z" fill="{INK}"/>'
      f'<circle id="b4-coin" cx="640" cy="585" r="34" fill="{YEL}" stroke="#9A7A1C" stroke-width="5"/>'
      f'<rect id="b4-rock" x="1200" y="505" width="170" height="110" rx="20" fill="#5B606B"/></g>', "b4-sv")
bp = c.text(800, 330, "삐!", 96, RED, "my")
lt = c.text(470, 760, "살짝 탄 토스트", 50); lf = c.text(1180, 790, "진짜 불", 50, RED)
lc = c.text(560, 470, "헛경보 · 잠깐 귀찮음", 46, "#9A7A1C"); lr = c.text(1150, 410, "놓친 경보 · 목숨", 46, "#3E434E")
st = c.uid("st")
c.add(f'<div id="{st}" style="position:absolute;left:560px;top:820px;padding:6px 36px;border:9px solid {RED};border-radius:14px;color:{RED};font-family:Myeongjo;font-size:72px;transform:rotate(-4deg);opacity:0">연기 감지기 원리</div>')
for k in ("b4-sc",):
    c.j(f'tl.set("#{k}",{{opacity:0}},0);')
c.slide(n2, .15, 400)
c.draw("b4-ce", c.cue(14, .4), .4); c.drop("b4-det", c.cue(14, .55))
c.pop("b4-to", c.cue(15, .05)); c.fade(lt, c.cue(15, .1)); c.draw("b4-sm", c.cue(15, .12), .5)
tb = c.cue(15, .3)
c.j(f'tl.to("#b4-led",{{fill:"{RED}",duration:.05}},{tb});')
c.ring("b4-w1", tb, 3, .7, 3); c.ring("b4-w2", tb + .35, 3, .7, 3); c.stamp(bp, tb)
c.out([bp], tb + 2.2)
c.j(f'tl.to("#b4-led",{{fill:"#7a7a7a",duration:.05}},{c.cue(15, .62)});')
c.pop("b4-fi", c.cue(15, .62)); c.fade(lf, c.cue(15, .65))
c.draw("b4-x", c.cue(15, .85), .3)
t16 = c.cue(16, 0)
c.out(["b4-to", "b4-fi", "b4-x", lt, lf], t16 - .1)
c.fade("b4-sc", t16 + .1, .3)
c.drop("b4-coin", t16 + .3); c.fade(lc, t16 + .4)
c.drop("b4-rock", c.cue(16, .5)); c.fade(lr, c.cue(16, .55))
c.j(f'tl.to("#b4-bm",{{rotation:9,transformOrigin:"50% 50%",duration:.7,ease:"elastic.out(1,.45)"}},{c.cue(16, .72)});')
c.j(f'tl.to("#b4-coin",{{y:-60,duration:.7,ease:"elastic.out(1,.45)"}},{c.cue(16, .72)});tl.to("#b4-rock",{{y:65,duration:.7,ease:"elastic.out(1,.45)"}},{c.cue(16, .72)});')
c.stamp(st, c.cue(17, .45))

c = scene("b5")
c.anotb(300, "고장 나서", "덜 위험한 쪽을 골라서", c.cue(18, .1), c.cue(18, .38), c.cue(18, .5))
sm = c.text(0, 160, "경보가 예민한 까닭", 56, "#6E6A60", "my", center=True)
c.fade(sm, .1)

# ═══ 3장 예상이 빗나간 실험 (샘플 장면 재사용·축약) ═════════════════
c = scene("c1")
qq = c.text(0, 330, "이 빠른 경보는<br>뇌 안에서 어떻게 켜질까?", 84, LIGHT, "my", center=True, extra="line-height:1.5")
c.rise(qq, .3)
c.out([qq], c.cue(20, 0, -.2))
c.svg(f'<line id="c1-tl" x1="260" y1="640" x2="1660" y2="640" stroke="{LIGHT}" stroke-width="5"/><circle id="c1-d0" cx="260" cy="640" r="14" fill="{LIGHT}"/><circle id="c1-d1" cx="1660" cy="640" r="18" fill="{RED}"/>')
y0 = c.text(200, 665, "1872 · 다윈", 46, LIGHT)
yr = c.text(0, 330, "<span id='c1-yv'>1872</span>", 200, LIGHT, "my", center=True)
u1 = c.tag(330, 180, "맥길대학교", RED); u2 = c.tag(1250, 180, "토론토대학교", NAVY)
jn = c.uid("j")
c.add(f'<div id="{jn}" style="position:absolute;left:640px;top:740px;width:640px;padding:22px 30px;background:#FBF9F4;color:{INK};box-shadow:0 12px 24px rgba(0,0,0,.35);opacity:0">'
      f'<div style="font-size:26px;color:#8A857A;letter-spacing:2px">NATURE NEUROSCIENCE · 2026.11</div>'
      f'<div style="font-size:30px;font-weight:700;margin-top:6px;line-height:1.3">Overlapping representations in the ventral hippocampus…</div></div>')
t20 = c.cue(20, 0)
c.draw("c1-tl", t20, 1.1, "power2.inOut"); c.fade("c1-d0", t20, .2); c.fade(y0, t20, .2); c.fade(yr, t20, .2)
c.j(f'tl.fromTo("#c1-yv",{{textContent:1872}},{{textContent:2026,duration:1.1,ease:"power3.in",snap:{{textContent:1}}}},{t20});')
c.pop("c1-d1", t20 + 1.1)
c.j(f'tl.to("#{yr}",{{scale:.4,y:-240,opacity:0,duration:.45,ease:"power3.inOut"}},{c.cue(20, .3)});')
c.slide(u1, c.cue(20, .3), -260); c.drop(u2, c.cue(20, .36))
c.j(f'tl.fromTo("#{jn}",{{opacity:0,y:120,rotation:4}},{{opacity:1,y:0,rotation:-1,duration:.4,ease:"power3.out"}},{c.cue(20, .55)});')
c.j(f'tl.to("#{jn}",{{scale:1.08,duration:.4,yoyo:true,repeat:1}},{c.cue(20, .75)});')

# c2: 경기장(위험/안전) → 뇌 → 해마 → 점
c = scene("c2")
CX, CY, R = 960, 520, 230
c.svg(f'<circle id="c2-ra" cx="{CX - 330}" cy="{CY}" r="{R}" fill="#3A2626" stroke="{RED}" stroke-width="22" stroke-dasharray="40 14"/>'
      f'<circle id="c2-ga" cx="{CX + 330}" cy="{CY}" r="{R}" fill="#22332B" stroke="{GRN}" stroke-width="22"/>'
      f'<path id="c2-zz" d="M{CX - 360},{CY - 120} l40,60 l-30,20 l50,70 l-30,20 l40,60" fill="none" stroke="{RED}" stroke-width="10"/>'
      f'<circle id="c2-rp" cx="{CX + 330}" cy="{CY}" r="40" fill="none" stroke="{GRN}" stroke-width="4"/>'
      f'<circle id="c2-m" cx="{CX - 330}" cy="{CY + 120}" r="16" fill="#FFF6D8"/>')
dl = c.tag(CX - 450, CY + 270, "위험한 곳", RED); sl = c.tag(CX + 220, CY + 270, "안전한 곳", GRN)
BRAIN = "M520,620 C 480,420 640,250 900,230 C 1150,210 1380,300 1420,450 C 1450,560 1390,660 1250,700 C 1100,740 900,760 760,740 C 640,725 545,700 520,620 Z"
HIPPO = "M820,560 C 860,470 960,430 1050,450 C 1130,470 1170,540 1140,600 C 1110,560 1060,530 1000,530 C 930,530 880,570 860,620 Z"
c.add(f'<div id="c2-br" style="position:absolute;inset:0;transform-origin:990px 540px">')
c.svg(f'<path id="c2-bo" d="{BRAIN}" fill="rgba(237,231,218,.06)" stroke="{LIGHT}" stroke-width="6"/><path id="c2-hp" d="{HIPPO}" fill="{YEL}" fill-opacity=".85"/>')
hl = c.text(1110, 330, "해마 — 기억", 64, YEL)
c.add('</div>')
rnd = random.Random(7)
DOTS = []
while len(DOTS) < 180:
    x, y = rnd.uniform(330, 1590), rnd.uniform(170, 860)
    if all((x - a) ** 2 + (y - b) ** 2 > 34 ** 2 for a, b in DOTS):
        DOTS.append((x, y))
c.add('<div id="c2-dots" style="position:absolute;inset:0;opacity:0">' + "".join(f'<div class="dot" id="c2-d{k}" style="left:{x:.0f}px;top:{y:.0f}px"></div>' for k, (x, y) in enumerate(DOTS)) + '</div>')
nn = c.text(120, 70, "신경세포 수백 개 — 켜졌다 꺼졌다", 64, YEL)
c.j('tl.fromTo("#c2-ra",{scale:0,transformOrigin:"50% 50%"},{scale:1,duration:.4,ease:"back.out(1.6)"},.15);')
c.draw("c2-zz", .5, .2, "none"); c.shake("c2-ra", .5, 5, 8); c.pop(dl, .55)
c.j('tl.fromTo("#c2-ga",{opacity:0,x:200},{opacity:1,x:0,duration:.45,ease:"power2.out"},.9);')
c.ring("c2-rp", 1.0, 2, 1.6, 3.4); c.rise(sl, 1.0)
c.j('tl.fromTo("#c2-m",{opacity:0},{opacity:1,duration:.2},.4);')
c.j(f'tl.to("#c2-m",{{motionPath:{{path:[{{x:0,y:0}},{{x:330,y:-260}},{{x:660,y:0}}],curviness:1.2}},duration:.6,ease:"power2.inOut"}},{c.cue(21, .15)});')
tb2 = c.cue(21, .3)
c.out(["c2-ra", "c2-ga", "c2-zz", "c2-rp", "c2-m", dl, sl], tb2 - .1)
c.draw("c2-bo", tb2, .8, "power2.inOut")
c.j(f'tl.fromTo("#c2-hp",{{opacity:0,scale:.3,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:.4,ease:"back.out(2)"}},{c.cue(21, .42)});')
c.fade(hl, c.cue(21, .45))
tz = c.cue(21, .62)
c.j(f'tl.to("#c2-br",{{scale:4.2,duration:.7,ease:"power3.in"}},{tz});tl.to("#c2-br",{{opacity:0,duration:.2}},{tz + .55:.2f});')
c.j(f'tl.fromTo("#c2-dots",{{opacity:0,scale:.6,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:.45,ease:"power2.out"}},{tz + .6:.2f});')
c.rise(nn, tz + .7)
b0, b1 = tz + .8, SC["c2"]["dur"] - .2
for k in range(len(DOTS)):
    tt = b0 + rnd.uniform(0, 1.2)
    while tt < b1:
        c.j(f'tl.to("#c2-d{k}",{{backgroundColor:"#FFF3C4",boxShadow:"0 0 18px #E8B931",duration:.08}},{tt:.2f});tl.to("#c2-d{k}",{{backgroundColor:"#7D8594",boxShadow:"0 0 0px #E8B931",duration:.35}},{tt + .12:.2f});')
        tt += rnd.uniform(1.2, 2.8)

side = [rnd.random() < .5 for _ in DOTS]
def cluster(cx, cy, r, n, seed):
    rr = random.Random(seed); return [(cx + r * math.sqrt(rr.random()) * math.cos(a), cy + r * math.sqrt(rr.random()) * math.sin(a)) for a in (rr.uniform(0, 2 * math.pi) for _ in range(n))]
nR = sum(side); nG = len(DOTS) - nR
farR, farG = cluster(520, 500, 230, nR, 1), cluster(1400, 500, 230, nG, 2)
ovR, ovG = cluster(860, 500, 250, nR, 3), cluster(1060, 500, 250, nG, 4)
def targets(tR, tG):
    iR = iG = 0; out = []
    for k in range(len(DOTS)):
        if side[k]: out.append(tR[iR]); iR += 1
        else: out.append(tG[iG]); iG += 1
    return out
FAR, OV = targets(farR, farG), targets(ovR, ovG)

c = scene("c3")
c.add(f'<div style="position:absolute;inset:0">' + "".join(f'<div class="dot" id="c3-d{k}" style="left:{x:.0f}px;top:{y:.0f}px"></div>' for k, (x, y) in enumerate(DOTS)) + '</div>')
ex3 = c.text(120, 90, "예상", 70, YEL, extra=f"border:4px dashed {YEL};padding:4px 26px;transform:rotate(-4deg)")
c.svg(f'<path id="c3-ar" d="M720,500 L1200,500" stroke="{YEL}" stroke-width="7" fill="none" stroke-linecap="round"/>')
fr = c.text(860, 410, "더 또렷하게, 더 멀리", 54, YEL)
c.stamp(ex3, c.cue(22, .05))
tc = c.cue(22, .25)
for k in range(len(DOTS)):
    c.j(f'tl.to("#c3-d{k}",{{backgroundColor:"{RED if side[k] else GRN}",duration:.15}},{tc + (k % 30) * .02:.2f});')
for k, ((x, y), (tx, ty)) in enumerate(zip(DOTS, FAR)):
    c.j(f'tl.to("#c3-d{k}",{{x:{tx - x:.0f},y:{ty - y:.0f},duration:1.3,ease:"power2.inOut"}},{c.cue(22, .5) + k * .004:.2f});')
c.spread("c3-ar", c.cue(22, .8), .5); c.fade(fr, c.cue(22, .82))

c = scene("c4")
c.svg(f'<circle id="c4-cr" cx="860" cy="500" r="290" fill="{RED}" fill-opacity=".10" stroke="{RED}" stroke-width="6"/><circle id="c4-cg" cx="1060" cy="500" r="290" fill="{GRN}" fill-opacity=".10" stroke="{GRN}" stroke-width="6"/>')
c.add(f'<div id="c4-ov" style="position:absolute;left:820px;top:280px;width:280px;height:440px;border-radius:50%;background:radial-gradient({VIO}AA,{VIO}00 70%);opacity:0"></div>')
c.add('<div style="position:absolute;inset:0">' + "".join(f'<div class="dot" id="c4-d{k}" style="left:{x:.0f}px;top:{y:.0f}px;background:{RED if side[k] else GRN}"></div>' for k, (x, y) in enumerate(FAR)) + '</div>')
ex4 = c.text(120, 90, "예상", 70, YEL, extra=f"border:4px dashed {YEL};padding:4px 26px;transform:rotate(-4deg)")
c.j(f'tl.set("#{ex4}",{{opacity:1}},0);')
c.svg(f'<path id="c4-x" d="M110,150 L330,110" stroke="{RED}" stroke-width="9" stroke-linecap="round"/>')
rs = c.text(390, 70, "결과", 84, RED, "my", f"border:9px solid {RED};border-radius:12px;padding:4px 30px;transform:rotate(-5deg)")
ol = c.text(880, 810, "겹쳤다", 64, VIO)
c.j('tl.set("#c4-cr,#c4-cg",{drawSVG:"0%",fillOpacity:0},0);')
c.draw("c4-x", c.cue(23, .1), .25); c.stamp(rs, c.cue(23, .25))
for k, ((x, y), (tx, ty)) in enumerate(zip(FAR, OV)):
    c.j(f'tl.to("#c4-d{k}",{{x:{tx - x:.0f},y:{ty - y:.0f},duration:1.1,ease:"back.inOut(1.4)"}},{c.cue(24, .05) + k * .003:.2f});')
c.j(f'tl.to("#c4-cr,#c4-cg",{{drawSVG:"100%",fillOpacity:.1,duration:.7}},{c.cue(24, .35)});')
c.j(f'tl.fromTo("#c4-ov",{{opacity:0,scale:.4}},{{opacity:1,scale:1,duration:.5}},{c.cue(24, .5)});')
c.rise(ol, c.cue(24, .55))

# ═══ 4장 골키퍼의 선택 ═══════════════════════════════════════════
c = scene("d1")
qd = c.text(0, 380, "왜 공포는 기억을 흐리게 만들었을까?", 76, INK, "my", center=True)
c.rise(qd, .2); c.out([qd], c.cue(26, 0, -.2))
c.svg(f'<path id="d1-goal" d="M560,700 L560,300 L1360,300 L1360,700" stroke="{INK}" stroke-width="12" fill="none" stroke-linejoin="round"/>'
      f'<path id="d1-net" d="M560,700 L1360,700" stroke="#B9B2A3" stroke-width="5" stroke-dasharray="10 10"/>'
      f'<rect id="d1-k" x="930" y="470" width="60" height="230" rx="28" fill="{NAVY}"/>'
      f'<circle id="d1-b" cx="960" cy="960" r="30" fill="#fff" stroke="{INK}" stroke-width="5"/>')
lk = c.text(1010, 420, "골키퍼", 50, NAVY); lb = c.text(1010, 930, "공", 50)
lw = c.text(0, 160, "끝까지 보고 움직이면 → 늦음", 60, RED, "my", center=True)
lp = c.text(0, 160, "차는 순간 먼저 몸을 날림", 60, GRN, "my", center=True)
tally = c.text(1420, 330, "", 64, INK, "sans")
t26 = c.cue(26, 0)
c.draw("d1-goal", t26, .6); c.fade("d1-net", t26 + .3, .2)
c.j(f'tl.fromTo("#d1-k",{{opacity:0,scaleY:.2,transformOrigin:"50% 100%"}},{{opacity:1,scaleY:1,duration:.3,ease:"back.out(2)"}},{t26 + .4:.2f});')
c.fade(lk, t26 + .5); c.pop("d1-b", t26 + .6); c.fade(lb, t26 + .6)
# ① 기다리다 늦음
ta = c.cue(27, .05)
c.fade(lw, ta)
c.j(f'tl.to("#d1-b",{{x:-300,y:-560,duration:.35,ease:"power2.out"}},{ta + .5:.2f});')
c.j(f'tl.to("#d1-k",{{x:-300,rotation:-60,transformOrigin:"50% 100%",duration:.3}},{ta + .85:.2f});')
c.out([lw, lb], c.cue(27, .5))
c.j(f'tl.to("#d1-b,#d1-k",{{x:0,y:0,rotation:0,duration:.01}},{c.cue(27, .55)});')
c.fade(lp, c.cue(27, .58))
# ② 미리 날기 — 세 번 (✓ ✓ ✗ ✓)
outs = [(-300, -560, -300, "✓"), (320, -540, 320, "✓"), (-300, -520, 300, "✗"), (300, -560, 300, "✓")]
t0 = c.cue(27, .7)
for k, (bx, by, kx, r) in enumerate(outs):
    tt = t0 + k * 1.5
    c.j(f'tl.to("#d1-k",{{x:{kx},rotation:{-60 if kx < 0 else 60},transformOrigin:"50% 100%",duration:.25,ease:"power2.out"}},{tt:.2f});')
    c.j(f'tl.to("#d1-b",{{x:{bx},y:{by},duration:.35,ease:"power2.out"}},{tt + .05:.2f});')
    c.j(f'tl.to("#{tally}",{{scrambleText:{{text:"{"  ".join(o[3] for o in outs[:k + 1])}",chars:"✓",speed:1}},opacity:1,duration:.15}},{tt + .4:.2f});')
    c.j(f'tl.to("#d1-b,#d1-k",{{x:0,y:0,rotation:0,duration:.25}},{tt + 1.0:.2f});')

c = scene("d2")
nr = c.name(120, 90, "로버트 로제스키", "논문 제1저자 · 토론토대 심리학과")
c.svg(f'<path id="d2-bm" d="M560,600 L1360,600" stroke="{INK}" stroke-width="12" stroke-linecap="round"/><path id="d2-fu" d="M960,600 L920,720 L1000,720 Z" fill="{INK}"/>')
la = c.text(500, 480, "정확함", 74, NAVY, "my"); lsp = c.text(1220, 480, "속도", 74, RED, "my")
c.slide(nr, .15, -400)
c.fade("d2-bm", c.cue(30, 0), .2); c.fade("d2-fu", c.cue(30, 0), .2); c.pop(la, c.cue(30, .1)); c.pop(lsp, c.cue(30, .2))
c.j(f'tl.to("#d2-bm",{{rotation:9,transformOrigin:"50% 50%",duration:.8,ease:"elastic.out(1,.45)"}},{c.cue(30, .55)});')
c.j(f'tl.to("#{la}",{{y:-62,duration:.8,ease:"elastic.out(1,.45)"}},{c.cue(30, .55)});tl.to("#{lsp}",{{y:62,duration:.8,ease:"elastic.out(1,.45)"}},{c.cue(30, .55)});')

c = scene("d3")
c.svg(f'<circle id="d3-cr" cx="860" cy="500" r="290" fill="{RED}" fill-opacity=".10" stroke="{RED}" stroke-width="6"/><circle id="d3-cg" cx="1060" cy="500" r="290" fill="{GRN}" fill-opacity=".10" stroke="{GRN}" stroke-width="6"/>', "d3-venn")
c.add(f'<div id="d3-ov" style="position:absolute;left:820px;top:280px;width:280px;height:440px;border-radius:50%;background:radial-gradient({VIO}AA,{VIO}00 70%)"></div>')
c.add('<div id="d3-dots" style="position:absolute;inset:0">' + "".join(f'<div class="dot" id="d3-d{k}" style="left:{x:.0f}px;top:{y:.0f}px;background:{RED if side[k] else GRN}"></div>' for k, (x, y) in enumerate(OV)) + '</div>')
c.svg(f'<circle id="d3-in" cx="1700" cy="500" r="26" fill="{GRN}"/><circle id="d3-hit" cx="960" cy="500" r="120" fill="none" stroke="{YEL}" stroke-width="8"/>')
li = c.text(1610, 560, "비슷한 장면", 46, GRN); lr2 = c.text(700, 840, "위험의 기억도 함께 → 바로 피함", 56, RED)
w1 = c.text(1230, 120, "날카롭게", 88, LIGHT, "my"); w2 = c.text(1260, 250, "흐리게", 96, VIO, "my")
c.svg(f'<path id="d3-x2" d="M1220,180 L1600,160" stroke="{RED}" stroke-width="9" stroke-linecap="round"/>')
c.j(f'tl.fromTo("#d3-in",{{opacity:0,x:200}},{{opacity:1,x:0,duration:.3}},{c.cue(31, .1)});'); c.fade(li, c.cue(31, .1))
c.j(f'tl.to("#d3-in",{{x:-740,duration:.7,ease:"power2.in"}},{c.cue(31, .3)});')
th = c.cue(31, .3, .7)
c.ring("d3-hit", th, 2, .7, 2.5)
reds = [k for k in range(len(DOTS)) if side[k]]
c.j(f'tl.to("{",".join(f"#d3-d{k}" for k in reds)}",{{scale:2,boxShadow:"0 0 16px {RED}",duration:.15,yoyo:true,repeat:3}},{th:.2f});')
c.out([li], th); c.rise(lr2, th + .3)
c.out([lr2], c.cue(32, 0))
c.fade(w1, c.cue(32, .1)); c.draw("d3-x2", c.cue(32, .3), .25); c.pop(w2, c.cue(32, .55))
c.j(f'tl.fromTo("#d3-venn",{{filter:"blur(0px)"}},{{filter:"blur(14px)",duration:1.4,ease:"sine.inOut"}},{c.cue(32, .55)});')
c.j(f'tl.fromTo("#d3-dots",{{filter:"blur(0px)"}},{{filter:"blur(5px)",duration:1.4,ease:"sine.inOut"}},{c.cue(32, .55)});')

# ═══ 5장 너무 빨리 울리는 경보 ═══════════════════════════════════
c = scene("e1")
c.svg(f'<circle id="e1-g" cx="760" cy="520" r="120" fill="#22332B" stroke="{GRN}" stroke-width="12"/><circle id="e1-r" cx="1160" cy="520" r="120" fill="#3A2626" stroke="{RED}" stroke-width="12"/>'
      f'<path id="e1-link" d="M880,520 C 940,440 1000,440 1040,520" stroke="{YEL}" stroke-width="6" stroke-dasharray="8 8" fill="none"/>'
      f'<circle id="e1-gl" cx="760" cy="520" r="120" fill="{GRN}"/><circle id="e1-rl" cx="1160" cy="520" r="120" fill="{RED}"/>')
lg = c.text(670, 680, "안전한 순간", 52, GRN); lr = c.text(1060, 680, "위험의 기억", 52, RED)
cost = c.text(0, 200, "대가", 96, LIGHT, "my", center=True)
c.rise(cost, .2)
c.pop("e1-g", c.cue(33, .5)); c.pop("e1-r", c.cue(33, .6)); c.draw("e1-link", c.cue(33, .7), .4)
c.j('tl.set("#e1-gl,#e1-rl",{opacity:0},0);')
c.fade(lg, c.cue(34, .05)); c.fade(lr, c.cue(34, .4))
c.j(f'tl.to("#e1-gl",{{opacity:.85,duration:.08}},{c.cue(34, .2)});tl.to("#e1-rl",{{opacity:.85,duration:.08}},{c.cue(34, .35)});')
c.blink("e1-rl", c.cue(34, .45), 4, .15)

c = scene("e2")
nb = c.text(0, 110, "2015년 · 불안 장애 실험 44개를 모아 분석", 52, INK, "my", center=True)
c.svg(f'<g id="e2-pp"><circle cx="760" cy="430" r="60" fill="#8A93A3"/><path d="M660,640 C 660,500 860,500 860,640 Z" fill="#8A93A3"/><circle cx="1160" cy="430" r="60" fill="{RED}"/><path d="M1060,640 C 1060,500 1260,500 1260,640 Z" fill="{RED}"/></g>')
pq = c.text(0, 690, "사람에게서도?", 66, INK, "my", center=True)
c.j('tl.fromTo("#e2-pp",{opacity:0,y:60},{opacity:1,y:0,duration:.4,ease:"back.out(1.8)"},.25);')
c.pop(pq, .6)
c.out(["e2-pp", pq], c.cue(36, 0, -.1))
c.svg(f'<path id="e2-ax" d="M600,800 L1320,800" stroke="{INK}" stroke-width="6"/>'
      f'<rect id="e2-b1" x="700" y="560" width="180" height="240" fill="#8A93A3"/><rect id="e2-b2" x="1040" y="380" width="180" height="420" fill="{RED}"/>')
lb1 = c.text(640, 820, "대조군 1,222명", 40, INK, "sans", "font-weight:600")
lb2 = c.text(990, 820, "불안 장애 963명", 40, RED, "sans", "font-weight:600")
lq = c.text(1260, 300, "'안전하다'는 신호에도<br>더 큰 공포 반응", 50, RED, extra="line-height:1.3")
note = c.text(560, 920, "막대 높이는 '더 크다'는 방향만 나타냄 — 실제 수치 아님", 24, "#8A857A", "sans", "font-weight:400")
c.rise(nb, c.cue(36, .02))
n44 = c.text(0, 260, "<span id='e2-c'>0</span>개 연구", 72, NAVY, "sans", center=True)
c.fade(n44, c.cue(36, .1), .2); c.count("e2-c", c.cue(36, .1), 0, 44, .8, False)
c.out([n44], c.cue(36, .35))
c.draw("e2-ax", c.cue(36, .35), .3)
c.j(f'tl.fromTo("#e2-b1",{{scaleY:0,transformOrigin:"50% 100%"}},{{scaleY:1,duration:.5,ease:"power2.out"}},{c.cue(36, .45)});')
c.j(f'tl.fromTo("#e2-b2",{{scaleY:0,transformOrigin:"50% 100%"}},{{scaleY:1,duration:.8,ease:"back.out(1.5)"}},{c.cue(36, .6)});')
c.fade(lb1, c.cue(36, .45)); c.fade(lb2, c.cue(36, .6)); c.pop(lq, c.cue(36, .8)); c.fade(note, c.cue(36, .8))

c = scene("e3")
nb2 = c.name(120, 90, "마크 브랜던", "교신저자 · 맥길대 정신의학과")
c.svg(f'<path id="e3-arc" d="M660,760 A300,300 0 0 1 1260,760" stroke="#B9B2A3" stroke-width="40" fill="none"/>'
      f'<path id="e3-red" d="M1160,520 A300,300 0 0 1 1260,760" stroke="{RED}" stroke-width="40" fill="none"/>'
      f'<path id="e3-nd" d="M960,760 L960,500" stroke="{INK}" stroke-width="14" stroke-linecap="round"/><circle cx="960" cy="760" r="26" fill="{INK}"/>')
ln = c.text(640, 800, "정상적인 생존 장치", 50, INK); lo = c.text(1180, 450, "너무 세게", 56, RED)
br = c.text(0, 880, "고장 ✗  ·  너무 세게 돌아감", 60, INK, "my", center=True)
sw = c.text(0, 300, "'위험 모드'로 넘어가는 그 순간 → 치료의 실마리?", 58, NAVY, "my", center=True)
c.slide(nb2, .15, -400)
c.draw("e3-arc", c.cue(37, .1), .5); c.draw("e3-red", c.cue(37, .3), .3); c.fade(ln, c.cue(37, .25))
c.j(f'tl.fromTo("#e3-nd",{{rotation:-80,transformOrigin:"50% 100%"}},{{rotation:68,duration:1.0,ease:"back.out(1.7)"}},{c.cue(37, .5)});')
c.pop(lo, c.cue(37, .7)); c.rise(br, c.cue(37, .78))
c.out([br], c.cue(38, 0)); c.rise(sw, c.cue(38, .3))
c.j(f'tl.to("#e3-nd",{{rotation:20,duration:1.2,ease:"power2.inOut"}},{c.cue(38, .5)});')

# ═══ 6장 아직 남은 질문 ══════════════════════════════════════════
c = scene("f1")
c.svg(f'<g id="f1-mo"><ellipse cx="560" cy="560" rx="120" ry="70" fill="#7D8594"/><circle cx="470" cy="500" r="30" fill="#7D8594"/><path d="M680,570 C 760,600 780,660 740,700" stroke="#7D8594" stroke-width="8" fill="none"/></g>'
      f'<g id="f1-hu"><circle cx="1360" cy="380" r="70" fill="{LIGHT}"/><path d="M1240,700 C 1240,520 1480,520 1480,700 Z" fill="{LIGHT}"/></g>'
      f'<path id="f1-ln" d="M720,520 L1220,520" stroke="{YEL}" stroke-width="7" stroke-dasharray="14 14" fill="none"/>')
lmo = c.text(500, 680, "쥐", 56, LIGHT); lhu = c.text(1320, 730, "사람", 56, LIGHT)
qf = c.text(930, 400, "?", 150, YEL, "my")
c.pop("f1-mo", c.cue(39, .05)); c.fade(lmo, c.cue(39, .05))
c.draw("f1-ln", c.cue(39, .3), .6); c.pop("f1-hu", c.cue(39, .45)); c.fade(lhu, c.cue(39, .5)); c.stamp(qf, c.cue(39, .7))

c = scene("f2")
nl = c.name(120, 90, "조지프 르두", "신경과학자")
c.svg(f'<path id="f2-ax" d="M300,620 L1640,620" stroke="{LIGHT}" stroke-width="6"/><path id="f2-ah" d="M1610,595 L1645,620 L1610,645" stroke="{LIGHT}" stroke-width="6" fill="none"/>'
      f'<circle id="f2-p1" cx="620" cy="620" r="34" fill="{RED}"/><circle id="f2-p2" cx="1260" cy="620" r="34" fill="{VIO}"/>'
      f'<path id="f2-gap" d="M660,700 L1220,700" stroke="{YEL}" stroke-width="5" stroke-dasharray="8 10"/>')
l1 = c.text(470, 470, "몸의 반응", 62, RED, "my"); l2 = c.text(1110, 470, "'무섭다'는 느낌", 62, VIO, "my")
lt = c.text(1560, 650, "시간", 40, "#9AA0AA")
lx = c.text(0, 260, "같은 일이 아니다", 76, LIGHT, "my", center=True)
lw1 = c.text(540, 760, "숲길의 사람 · 다윈", 46, YEL)
c.slide(nl, .15, -400)
c.draw("f2-ax", c.cue(41, 0), .5); c.fade("f2-ah", c.cue(41, .1))
c.pop("f2-p1", c.cue(41, .25)); c.fade(l1, c.cue(41, .25)); c.pop("f2-p2", c.cue(41, .5)); c.fade(l2, c.cue(41, .5))
c.rise(lx, c.cue(41, .75))
c.out([lx], c.cue(42, 0)); c.fade(lw1, c.cue(42, .1))
c.j(f'tl.fromTo("#f2-p2",{{x:-640,opacity:0}},{{x:0,opacity:1,duration:1.6,ease:"power1.inOut",immediateRender:false}},{c.cue(42, .35)});')
c.draw("f2-gap", c.cue(42, .4), 1.6, "power1.inOut")

c = scene("f3")
nn2 = c.name(1240, 90, "랜돌프 네스", "진화 의학자")
rr = random.Random(11); al = []
for k in range(12):
    x, y = 420 + (k % 6) * 210, 420 + (k // 6) * 230
    al.append((x, y))
c.svg("".join(f'<circle id="f3-a{k}" cx="{x}" cy="{y}" r="44" fill="{RED}" fill-opacity=".85"/>' for k, (x, y) in enumerate(al)))
lq3 = c.text(0, 860, "왜 어떤 사람의 경보만 멈추지 않을까 — 아직 모름", 58, YEL, "my", center=True)
c.slide(nn2, .15, 400)
for k in range(12):
    c.pop(f"f3-a{k}", c.cue(43, .05) + k * .05, .25)
for k in range(12):
    if k != 8:
        c.j(f'tl.to("#f3-a{k}",{{opacity:.15,duration:.4}},{c.cue(43, .4) + rr.uniform(0, .5):.2f});')
c.blink("f3-a8", c.cue(43, .5), 6, .2)
c.rise(lq3, c.cue(43, .65))

# ═══ 7장 늦지 않는 쪽 ═══════════════════════════════════════════
c = scene("g1")
c.anotb(300, "고장 나서", "틀리더라도 늦지 않는 쪽을 골라서", c.cue(45, .1), c.cue(45, .4), c.cue(45, .5), 84)
hd = c.text(0, 160, "불안이 그렇게 빨리 켜지는 까닭", 56, "#6E6A60", "my", center=True)
c.fade(hd, c.cue(44, .5))

c = scene("g2")
c.svg(f'<rect id="g2-gl" x="930" y="250" width="60" height="460" rx="6" fill="{BLU}" fill-opacity=".35" stroke="{BLU}" stroke-width="5"/>'
      f'<path id="g2-sn" d="{SN}" fill="none" stroke="{GRN}" stroke-width="22" stroke-linecap="round"/>'
      f'<circle id="g2-dw" cx="840" cy="480" r="36" fill="{INK}"/><path id="g2-dl" d="M840,520 L840,700" stroke="{INK}" stroke-width="16" stroke-linecap="round"/>', "g2-sv")
lg2 = c.text(880, 730, "유리가 있다는 걸 알았다", 52, NAVY)
c.j(f'tl.fromTo("#g2-gl",{{scaleY:0,transformOrigin:"50% 100%"}},{{scaleY:1,duration:.4}},{c.cue(46, .05)});')
c.draw("g2-sn", c.cue(46, .1), .5); c.j(f'tl.fromTo("#g2-dw,#g2-dl",{{opacity:0}},{{opacity:1,duration:.2}},{c.cue(46, .1)});')
c.fade(lg2, c.cue(46, .4))
tj = c.cue(47, .05)
c.j(f'tl.to("#g2-dw,#g2-dl",{{x:-280,duration:.18,ease:"power4.out"}},{tj});'); c.shake(f"{c.sid}-cam", tj, 5, 12)
# 헛경보 수없이 → 조상의 줄
rr = random.Random(5)
fa = "".join(f'<circle class="fa" cx="{rr.uniform(150, 1770):.0f}" cy="{rr.uniform(120, 880):.0f}" r="{rr.uniform(8, 18):.0f}" fill="{RED}" opacity="0"/>' for _ in range(70))
c.svg(f'<g id="g2-fa">{fa}</g>')
c.j(f'tl.to("#g2-fa .fa",{{opacity:.75,duration:.08,stagger:{{each:.03,from:"random"}}}},{c.cue(47, .3)});')
c.j(f'tl.to("#g2-fa .fa",{{opacity:.12,duration:.3,stagger:{{each:.02,from:"random"}}}},{c.cue(47, .55)});')
lh = c.text(0, 820, "수없이 많은 헛경보 ↔ 살아남은 조상", 58, RED, "my", center=True)
c.rise(lh, c.cue(47, .6))

c = scene("g3")
c.svg(f'<path d="M300,160 L1620,160" stroke="{LIGHT}" stroke-width="8"/>'
      f'<ellipse cx="960" cy="190" rx="130" ry="40" fill="#2C313B" stroke="{LIGHT}" stroke-width="6"/><circle id="g3-led" cx="1060" cy="185" r="14" fill="{RED}"/>'
      f'<circle id="g3-gw" cx="1060" cy="185" r="60" fill="{RED}" opacity=".35"/>')
lend = c.text(0, 420, "경보를 없애기보다<br>너무 일찍 울린 경보를 알아보기", 72, LIGHT, "my", center=True, extra="line-height:1.5")
c.rise(lend, c.cue(48, .35))
c.j(f'tl.fromTo("#g3-gw",{{scale:1,opacity:.5,transformOrigin:"50% 50%"}},{{scale:2.2,opacity:0,duration:1.2,repeat:2}},.2);')
c.j(f'tl.to("#g3-led",{{fill:"#5a5a5a",duration:1.6,ease:"sine.inOut"}},{c.cue(48, .7)});')
c.j(f'tl.to("#{lend}",{{opacity:0,duration:.6}},{SC["g3"]["dur"] - .9:.2f});')

# ═══ 묶기 ═══════════════════════════════════════════════════════
for s in SCENES:
    (HERE / "compositions" / f"{s.sid}.html").write_text(s.html(), encoding="utf-8")
caps = "".join(f'<div class="clip cap" id="cap{x["i"]}" data-start="{x["start"] + .05:.2f}" data-duration="{x["dur"] - .25:.2f}" data-track-index="20"><span>{x["text"]}</span></div>' for x in L)
aud = "".join(f'<audio id="vo{x["i"]}" class="clip" src="assets/vo/{x["file"]}" data-start="{x["start"]}" data-duration="{x["dur"]}" data-track-index="7" data-volume="1"></audio>' for x in L)
def _d(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(HERE / f)], capture_output=True, text=True).stdout)
SFX = [("whoosh-short", 0, .2), ("pop", 1, .25), ("whoosh", 1, .42), ("impact-bass-2", 2, .3), ("whoosh-short", 3, .3), ("pencil", 4, .65),
       ("whoosh", 5, .4), ("impact-bass-2", 6, .1), ("riser", 8, .05), ("whoosh-short", 9, .05), ("pencil", 10, .1), ("click", 10, .55),
       ("whoosh-cinematic", 11, .62), ("pop", 13, .1), ("pop", 13, .45), ("click-soft", 14, .55), ("chime", 15, .3), ("impact-bass-2", 16, .55), ("click", 17, .45),
       ("pencil", 18, .38), ("whoosh-cinematic", 20, .0), ("pop", 20, .3), ("whoosh", 21, .15), ("whoosh-cinematic", 21, .62), ("click", 22, .05),
       ("impact-bass-2", 23, .25), ("riser", 24, .0), ("whoosh-short", 26, .0), ("whoosh", 27, .1), ("whoosh-short", 27, .7), ("whoosh-short", 28, .2),
       ("click-soft", 30, .55), ("whoosh", 31, .3), ("pencil", 32, .3), ("chime", 34, .2), ("click", 36, .1), ("pop", 36, .6), ("whoosh-short", 37, .05),
       ("click-soft", 37, .5), ("pop", 39, .7), ("whoosh-short", 41, .25), ("pop", 43, .05), ("pencil", 45, .4), ("pop", 45, .5), ("impact-bass-2", 47, .05),
       ("chime", 48, .7)]
for k, (n, i, fr) in enumerate(SFX):
    f = f"assets/sfx/{n}.{'wav' if n == 'pencil' else 'mp3'}"
    tt = round(L[i]["start"] + L[i]["dur"] * fr, 2)
    aud += f'<audio id="sx{k}" class="clip" src="{f}" data-start="{tt}" data-duration="{min(1.4, _d(f)):.2f}" data-track-index="{8 + k % 3}" data-volume="{0.16 if n in ("pencil", "riser") else 0.28}"></audio>'
hosts = "".join(f'<div id="{s.sid}" data-composition-id="{s.sid}" data-composition-src="compositions/{s.sid}.html" data-start="{s.s["start"]}" '
                f'data-duration="{s.s["dur"]}" data-track-index="1" data-track-kind="graphics" data-width="1920" data-height="1080"></div>' for s in SCENES)
(HERE / "index.html").write_text(f"""<!doctype html><html><head><meta charset="utf-8">
<script src="assets/gsap.min.js"></script><script src="assets/MotionPathPlugin.min.js"></script><script src="assets/DrawSVGPlugin.min.js"></script><script src="assets/ScrambleTextPlugin.min.js"></script>
<style>
@font-face{{font-family:'NotoKR';src:url('assets/fonts/NotoSansKR-VF.ttf');font-weight:100 900}}
.cap{{position:absolute;left:0;width:1920px;top:960px;text-align:center;z-index:50;font-family:'NotoKR'}}
.cap span{{display:inline-block;background:rgba(29,32,36,.82);color:#fff;font-weight:600;font-size:40px;padding:6px 22px;border-radius:6px;max-width:1720px;line-height:1.35}}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{END}" data-width="1920" data-height="1080">
{hosts}{caps}{aud}
</div>
<script>window.__timelines["main"] = gsap.timeline({{ paused: true }});</script>
</body></html>""", encoding="utf-8")
print("END", END, len(SCENES), {k: (v["start"], v["dur"]) for k, v in SC.items()})
