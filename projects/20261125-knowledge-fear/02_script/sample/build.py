"""불안 편 — 샘플(대본 4~5장). 사물 그림 없이 모션그래픽 중심 (사용자 11-25: "사물보다는 모션그래픽 등을 활용해주세요 미주일기식으로요").
화면 = 점·선·원·숫자·빛이 내레이션의 동사를 연기. 속도는 역할별(등장 .25~.4 · 강조 .5 · 과정 .8~1.4 · 카메라 계속), 같은 움직임 세 번 연속 금지."""
import json, math, random, re, subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
L = json.load(open(HERE / "assets/vo/lines.json", encoding="utf-8"))
GAP, LEAD = 0.25, 0.4
t = LEAD
for x in L:
    x["start"] = round(t, 2); t += x["dur"] + GAP
END = round(t + 0.8, 2)
GROUPS = [("s1", [0]), ("s2", [1, 2]), ("s3", [3]), ("s4", [4, 5]), ("s5", [6, 7])]
SC = {}
for k, (sid, idx) in enumerate(GROUPS):
    SC[sid] = {"start": 0.0 if k == 0 else round(L[idx[0]]["start"] - .25, 2)}
for k, (sid, _) in enumerate(GROUPS):
    SC[sid]["end"] = SC[GROUPS[k + 1][0]]["start"] if k + 1 < len(GROUPS) else END
    SC[sid]["dur"] = round(SC[sid]["end"] - SC[sid]["start"], 2)

INK, PAPER, RED, GRN, VIO, YEL, NAVY = "#2B2F3A", "#EEE9DF", "#E2563F", "#4FBF85", "#A98BF0", "#F2C94C", "#22345F"


class S:
    def __init__(self, sid, dark=False):
        self.sid, self.s, self.dark = sid, SC[sid], dark
        self.body, self.js = [], []

    def cue(self, i, frac=0.0, off=0.0):
        return round(L[i]["start"] + L[i]["dur"] * frac - self.s["start"] + off, 2)

    def add(self, h): self.body.append(h)
    def j(self, s): self.js.append(s)

    def fixjs(self):
        seen, out = set(), []
        for x in self.js:
            m = re.match(r'tl\.fromTo\("([^"]+)"', x)
            if m:
                if m.group(1) in seen:
                    a, b = x.rsplit("},", 1); x = a + ",immediateRender:false}," + b
                seen.add(m.group(1))
            out.append(x)
        return out

    def html(self):
        bg = "paper_dark.jpg" if self.dark else "paper.jpg"
        fg = "#EDE7DA" if self.dark else INK
        d = self.s["dur"]
        return f"""<template>
<style>
@font-face{{font-family:'NotoKR';src:url('assets/fonts/NotoSansKR-VF.ttf');font-weight:100 900}}
@font-face{{font-family:'Pen';src:url('assets/fonts/NanumPenScript-Regular.ttf')}}
@font-face{{font-family:'Myeongjo';src:url('assets/fonts/NanumMyeongjo-ExtraBold.ttf')}}
#root{{position:absolute;inset:0;overflow:hidden;font-family:'NotoKR';color:{fg};background:{'#1E2128' if self.dark else '#E8E3D9'}}}
.bg{{position:absolute;inset:-40px;background:url('assets/img/{bg}') center/cover}}
.cam{{position:absolute;inset:0;transform-origin:50% 50%}}
.pen{{font-family:'Pen'}} .my{{font-family:'Myeongjo'}}
.tag{{position:absolute;padding:8px 26px;border-radius:40px;font-weight:700;white-space:nowrap}}
.lab{{position:absolute;white-space:nowrap}}
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
tl.fromTo("#{self.sid}-cam", {{scale:1}}, {{scale:1.04, duration:{d}, ease:"sine.inOut"}}, 0);
{''.join(self.fixjs())}
window.__timelines["{self.sid}"] = tl;
</script>
</template>
"""


def svg(inner, extra=""):
    return f'<svg style="position:absolute;left:0;top:0;overflow:visible" width="1920" height="1080" {extra}>{inner}</svg>'


# ── s1 1872 → 2026, 두 대학, 학술지 ───────────────────────────────
c = S("s1")
c.add(svg(f'<line id="s1-tl" x1="260" y1="640" x2="1660" y2="640" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
          f'<circle id="s1-d0" cx="260" cy="640" r="14" fill="{INK}"/><circle id="s1-d1" cx="1660" cy="640" r="18" fill="{RED}"/>'))
c.add(f'<div id="s1-y0" class="pen lab" style="left:200px;top:665px;font-size:46px">1872 · 다윈</div>')
c.add(f'<div id="s1-yr" class="my lab" style="left:0;width:1920px;text-align:center;top:300px;font-size:230px;color:{INK}"><span id="s1-yv">1872</span></div>')
c.add(f'<div id="s1-m" class="pen lab" style="left:1560px;top:665px;font-size:50px;color:{RED};opacity:0">11월</div>')
c.add(f'<div id="s1-u1" class="tag" style="left:330px;top:180px;background:{RED};color:#fff;font-size:44px;opacity:0">맥길대학교</div>'
      f'<div id="s1-u2" class="tag" style="left:1250px;top:180px;background:{NAVY};color:#fff;font-size:44px;opacity:0">토론토대학교</div>')
c.add(svg(f'<path id="s1-ln" d="M640,212 C 800,140 1100,140 1250,212" fill="none" stroke="{INK}" stroke-width="4" stroke-dasharray="10 10"/>'))
c.add(f'<div id="s1-j" style="position:absolute;left:640px;top:730px;width:640px;padding:22px 30px;background:#FBF9F4;box-shadow:0 12px 24px rgba(30,24,16,.25);opacity:0">'
      f'<div style="font-size:26px;color:#8A857A;letter-spacing:2px">NATURE NEUROSCIENCE · 2026</div>'
      f'<div style="font-size:30px;font-weight:700;margin-top:6px;line-height:1.3">Overlapping representations in the ventral hippocampus…</div></div>')
c.add(f'<div id="s1-ms" class="pen lab" style="left:1300px;top:770px;font-size:44px;color:{RED};opacity:0;transform:rotate(-6deg)">쥐 실험</div>')
c.j('tl.fromTo("#s1-tl",{drawSVG:"0%"},{drawSVG:"100%",duration:1.3,ease:"power2.inOut"},.25);')
c.j(f'tl.fromTo("#s1-yv",{{textContent:1872}},{{textContent:2026,duration:1.3,ease:"power3.in",snap:{{textContent:1}}}},.25);')
c.j('tl.fromTo("#s1-d1",{scale:0,transformOrigin:"50% 50%"},{scale:1,duration:.3,ease:"back.out(3)"},1.5);')
c.j('tl.fromTo("#s1-m",{opacity:0,y:20},{opacity:1,y:0,duration:.25},1.6);')
c.j(f'tl.to("#s1-yr",{{scale:.45,y:-250,duration:.5,ease:"power3.inOut"}},{c.cue(0, .3)});')
c.j(f'tl.fromTo("#s1-u1",{{opacity:0,x:-260}},{{opacity:1,x:0,duration:.3,ease:"power3.out"}},{c.cue(0, .32)});')
c.j(f'tl.fromTo("#s1-u2",{{opacity:0,y:-120}},{{opacity:1,y:0,duration:.35,ease:"bounce.out"}},{c.cue(0, .42)});')
c.j(f'tl.fromTo("#s1-ln",{{drawSVG:"0%"}},{{drawSVG:"100%",duration:.5,ease:"power1.inOut"}},{c.cue(0, .5)});')
c.j(f'tl.to("#s1-yr",{{opacity:0,duration:.25}},{c.cue(0, .5)});')
c.j(f'tl.fromTo("#s1-j",{{opacity:0,y:120,rotation:4}},{{opacity:1,y:0,rotation:-1,duration:.4,ease:"power3.out"}},{c.cue(0, .66)});')
c.j(f'tl.fromTo("#s1-ms",{{opacity:0,scale:1.8}},{{opacity:1,scale:1,duration:.2,ease:"power4.in"}},{c.cue(0, .85)});')
S1 = c

# ── s2 경기장: 화면·소리 → 순간이동 → 위험/안전 ────────────────────
c = S("s2", dark=True)
CX, CY, R = 960, 520, 270
segs = ""
for k in range(24):
    a0, a1 = (k / 24) * 2 * math.pi, ((k + .82) / 24) * 2 * math.pi
    x0, y0, x1, y1 = CX + R * math.cos(a0), CY + R * math.sin(a0), CX + R * math.cos(a1), CY + R * math.sin(a1)
    segs += f'<path class="sg" d="M{x0:.1f},{y0:.1f} A{R},{R} 0 0 1 {x1:.1f},{y1:.1f}" stroke="{"#D9D3C4" if k % 2 else "#6C7484"}" stroke-width="34" fill="none"/>'
c.add(f'<div id="s2-ar" style="position:absolute;inset:0;transform-origin:{CX}px {CY}px">'
      + svg(f'<circle id="s2-fl" cx="{CX}" cy="{CY}" r="{R - 22}" fill="#2A2F3A" stroke="#525A69" stroke-width="3"/><g id="s2-sg">{segs}</g>'
            f'<circle id="s2-w1" cx="{CX + R + 70}" cy="{CY}" r="40" fill="none" stroke="{YEL}" stroke-width="5"/>'
            f'<circle id="s2-w2" cx="{CX + R + 70}" cy="{CY}" r="40" fill="none" stroke="{YEL}" stroke-width="5"/>'
            f'<circle id="s2-glow" cx="{CX}" cy="{CY}" r="34" fill="{YEL}" opacity=".25"/><circle id="s2-m" cx="{CX}" cy="{CY}" r="16" fill="#FFF6D8"/>')
      + '</div>')
c.add(f'<div id="s2-l1" class="pen lab" style="left:{CX - R - 230}px;top:{CY - 30}px;font-size:54px;color:#EDE7DA;opacity:0">화면 →</div>'
      f'<div id="s2-l2" class="pen lab" style="left:{CX + R + 130}px;top:{CY - 30}px;font-size:54px;color:{YEL};opacity:0">소리</div>'
      f'<div id="s2-l3" class="pen lab" style="left:{CX - 40}px;top:{CY + 40}px;font-size:44px;color:#FFF6D8;opacity:0">쥐</div>')
c.add(f'<div id="s2-fx" style="position:absolute;inset:0;background:#fff;opacity:0"></div>')
c.add(f'<div id="s2-tp" class="my lab" style="left:0;width:1920px;text-align:center;top:90px;font-size:70px;color:{YEL};opacity:0">순간이동</div>')
# 두 번째 경기장(안전)
c.add(f'<div id="s2-ar2" style="position:absolute;inset:0;opacity:0">'
      + svg(f'<circle cx="{CX + 400}" cy="{CY}" r="{int(R * .62)}" fill="#22332B" stroke="{GRN}" stroke-width="18"/>'
            f'<circle id="s2-rp" cx="{CX + 400}" cy="{CY}" r="40" fill="none" stroke="{GRN}" stroke-width="4"/>') + '</div>')
c.add(svg(f'<path id="s2-zz" d="M{CX - 470},{CY - 120} l40,60 l-30,20 l50,70 l-30,20 l40,60" fill="none" stroke="{RED}" stroke-width="10" stroke-linejoin="round"/>'))
c.add(f'<div id="s2-dl" class="tag" style="left:{CX - 530}px;top:{CY + 200}px;background:{RED};color:#fff;font-size:46px;opacity:0">위험한 곳</div>'
      f'<div id="s2-sl" class="tag" style="left:{CX + 300}px;top:{CY + 200}px;background:{GRN};color:#fff;font-size:46px;opacity:0">안전한 곳</div>')
c.j('tl.fromTo("#s2-fl",{scale:0,transformOrigin:"50% 50%"},{scale:1,duration:.45,ease:"back.out(1.6)"},.15);')
c.j('tl.fromTo("#s2-sg .sg",{drawSVG:"50% 50%"},{drawSVG:"0% 100%",duration:.25,stagger:.02,ease:"power2.out"},.35);')
c.j('tl.fromTo("#s2-m,#s2-glow",{scale:0,transformOrigin:"50% 50%"},{scale:1,duration:.3,ease:"back.out(3)"},.9);')
c.j('tl.fromTo("#s2-glow",{scale:1},{scale:1.6,duration:.9,repeat:5,yoyo:true,ease:"sine.inOut",transformOrigin:"50% 50%"},1.2);')
c.j(f'tl.fromTo("#s2-l1",{{opacity:0,x:-40}},{{opacity:1,x:0,duration:.3}},{c.cue(1, .12)});')
c.j(f'tl.fromTo("#s2-l3",{{opacity:0}},{{opacity:1,duration:.25}},{c.cue(1, .5)});')
tw = c.cue(1, .25)
c.j(f'tl.fromTo("#s2-l2",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.25}},{tw});')
for k, w in enumerate(("#s2-w1", "#s2-w2")):
    c.j(f'tl.fromTo("{w}",{{scale:.4,opacity:1,transformOrigin:"50% 50%"}},{{scale:3.2,opacity:0,duration:1.1,repeat:2,ease:"power1.out"}},{tw + k * .45:.2f});')
for n, fr in enumerate((.66, .86)):
    tt = c.cue(1, fr)
    c.j(f'tl.fromTo("#s2-fx",{{opacity:.85}},{{opacity:0,duration:.35,ease:"power2.out",immediateRender:false}},{tt});')
    col = ("#4C6FB8", "#9A7A3C")[n]
    c.j(f'tl.to("#s2-sg .sg",{{stroke:(i)=>i%2?"{col}":"#20242C",duration:.05,stagger:.015}},{tt});')
c.j(f'tl.fromTo("#s2-tp",{{opacity:0,scaleX:1.8}},{{opacity:1,scaleX:1,duration:.3,ease:"power3.out"}},{c.cue(1, .66)});')
c.j(f'tl.to("#s2-tp",{{opacity:0,duration:.25}},{c.cue(2, 0, -.3)});')
t2 = c.cue(2, .02)
c.j(f'tl.to("#s2-ar",{{x:-400,scale:.62,duration:.55,ease:"power3.inOut"}},{t2});')
c.j(f'tl.to("#s2-l1,#s2-l2,#s2-l3",{{opacity:0,duration:.2}},{t2});')
c.j(f'tl.to("#s2-sg .sg",{{stroke:"{RED}",duration:.3}},{t2 + .3:.2f});')
c.j(f'tl.fromTo("#s2-zz",{{drawSVG:"0%"}},{{drawSVG:"100%",duration:.22,ease:"none"}},{c.cue(2, .2)});')
c.j(f'tl.fromTo("#s2-ar",{{rotation:0}},{{rotation:3,duration:.06,repeat:5,yoyo:true}},{c.cue(2, .2)});')
c.j(f'tl.fromTo("#s2-dl",{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:.3,ease:"back.out(2)"}},{c.cue(2, .24)});')
c.j(f'tl.fromTo("#s2-ar2",{{opacity:0,x:200}},{{opacity:1,x:0,duration:.45,ease:"power2.out"}},{c.cue(2, .42)});')
c.j(f'tl.fromTo("#s2-rp",{{scale:.5,opacity:1,transformOrigin:"50% 50%"}},{{scale:3.4,opacity:0,duration:1.8,repeat:2,ease:"sine.out"}},{c.cue(2, .45)});')
c.j(f'tl.fromTo("#s2-sl",{{opacity:0,y:40}},{{opacity:1,y:0,duration:.35,ease:"power2.out"}},{c.cue(2, .5)});')
# 쥐가 위험 ↔ 안전을 오감 (배움)
c.j(f'tl.to("#s2-m,#s2-glow",{{motionPath:{{path:[{{x:0,y:0}},{{x:400,y:-200}},{{x:800,y:0}}],curviness:1.2}},duration:.6,ease:"power2.inOut"}},{c.cue(2, .7)});')
c.j(f'tl.to("#s2-m,#s2-glow",{{motionPath:{{path:[{{x:800,y:0}},{{x:400,y:-160}},{{x:0,y:0}}],curviness:1.2}},duration:.45,ease:"power2.inOut"}},{c.cue(2, .85)});')
S2 = c

# ── s3 뇌 → 해마 → 현미경 → 깜빡이는 세포 수백 개 ───────────────────
rnd = random.Random(7)
DOTS = []
while len(DOTS) < 180:
    x, y = rnd.uniform(330, 1590), rnd.uniform(170, 860)
    if all((x - a) ** 2 + (y - b) ** 2 > 34 ** 2 for a, b in DOTS):
        DOTS.append((x, y))
c = S("s3", dark=True)
BRAIN = "M520,620 C 480,420 640,250 900,230 C 1150,210 1380,300 1420,450 C 1450,560 1390,660 1250,700 C 1100,740 900,760 760,740 C 640,725 545,700 520,620 Z"
HIPPO = "M820,560 C 860,470 960,430 1050,450 C 1130,470 1170,540 1140,600 C 1110,560 1060,530 1000,530 C 930,530 880,570 860,620 Z"
c.add(f'<div id="s3-br" style="position:absolute;inset:0;transform-origin:990px 540px">'
      + svg(f'<path id="s3-bo" d="{BRAIN}" fill="rgba(237,231,218,.06)" stroke="#EDE7DA" stroke-width="6"/>'
            f'<path id="s3-cb" d="M1250,700 C 1330,700 1400,760 1380,820" fill="none" stroke="#EDE7DA" stroke-width="6"/>'
            f'<path id="s3-hp" d="{HIPPO}" fill="{YEL}" fill-opacity=".85" stroke="{YEL}" stroke-width="4"/>'
            f'<circle id="s3-lens" cx="990" cy="535" r="150" fill="none" stroke="#fff" stroke-width="5" stroke-dasharray="4 10"/>')
      + f'<div id="s3-hl" class="pen lab" style="left:1110px;top:330px;font-size:64px;color:{YEL};opacity:0">해마 — 기억</div>'
      + '</div>')
c.add('<div id="s3-dots" style="position:absolute;inset:0;opacity:0">' + "".join(f'<div class="dot" id="s3-d{k}" style="left:{x:.0f}px;top:{y:.0f}px"></div>' for k, (x, y) in enumerate(DOTS)) + '</div>')
c.add(f'<div id="s3-n" class="pen lab" style="left:120px;top:70px;font-size:64px;color:#F2C94C;opacity:0">신경세포 수백 개 — 켜졌다 꺼졌다</div>')
c.j('tl.fromTo("#s3-bo",{drawSVG:"0%"},{drawSVG:"100%",duration:1.0,ease:"power2.inOut"},.15);')
c.j('tl.fromTo("#s3-cb",{drawSVG:"0%"},{drawSVG:"100%",duration:.4},.9);')
c.j(f'tl.fromTo("#s3-lens",{{opacity:0,x:-700,y:-300}},{{opacity:1,x:0,y:0,duration:.55,ease:"power3.out"}},{c.cue(3, .12)});')
c.j(f'tl.fromTo("#s3-hp",{{opacity:0,scale:.3,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:.45,ease:"back.out(2)"}},{c.cue(3, .3)});')
c.j(f'tl.fromTo("#s3-hl",{{opacity:0,x:30}},{{opacity:1,x:0,duration:.3}},{c.cue(3, .32)});')
tz = c.cue(3, .5)
c.j(f'tl.to("#s3-br",{{scale:4.2,duration:.8,ease:"power3.in"}},{tz});')
c.j(f'tl.to("#s3-br",{{opacity:0,duration:.25}},{tz + .6:.2f});')
c.j(f'tl.fromTo("#s3-dots",{{opacity:0,scale:.6,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:.5,ease:"power2.out"}},{tz + .65:.2f});')
c.j(f'tl.fromTo("#s3-n",{{opacity:0,y:30}},{{opacity:1,y:0,duration:.3}},{tz + .8:.2f});')
blink0, blink1 = tz + .9, SC["s3"]["dur"] - .2
for k in range(len(DOTS)):
    tt = blink0 + rnd.uniform(0, 1.6)
    while tt < blink1:
        c.j(f'tl.to("#s3-d{k}",{{backgroundColor:"#FFF3C4",boxShadow:"0 0 18px #F2C94C",duration:.08}},{tt:.2f});'
            f'tl.to("#s3-d{k}",{{backgroundColor:"#7D8594",boxShadow:"0 0 0px #F2C94C",duration:.35}},{tt + .12:.2f});')
        tt += rnd.uniform(1.4, 3.2)
S3 = c

# ── s4·s5 예상(갈라짐) → 결과(겹침) → 경계가 흐려짐 ─────────────────
side = [rnd.random() < .5 for _ in DOTS]
def cluster(cx, cy, r, n, seed):
    rr = random.Random(seed); pts = []
    for _ in range(n):
        a, d = rr.uniform(0, 2 * math.pi), r * math.sqrt(rr.random())
        pts.append((cx + d * math.cos(a), cy + d * math.sin(a)))
    return pts
nR = sum(side); nG = len(DOTS) - nR
farR, farG = cluster(520, 520, 230, nR, 1), cluster(1400, 520, 230, nG, 2)
ovR, ovG = cluster(860, 520, 250, nR, 3), cluster(1060, 520, 250, nG, 4)

def dots_html(pfx):
    return "".join(f'<div class="dot" id="{pfx}{k}" style="left:{x:.0f}px;top:{y:.0f}px"></div>' for k, (x, y) in enumerate(DOTS))

def move_js(sc, pfx, tgtR, tgtG, t0, dur, ease, stag=.004, base=None):
    iR = iG = 0
    for k, (x, y) in enumerate(base or DOTS):
        if side[k]: tx, ty = tgtR[iR]; iR += 1
        else: tx, ty = tgtG[iG]; iG += 1
        sc.j(f'tl.to("#{pfx}{k}",{{x:{tx - x:.0f},y:{ty - y:.0f},duration:{dur},ease:"{ease}"}},{t0 + k * stag:.2f});')

c = S("s4", dark=True)
c.add(f'<div id="s4-dots" style="position:absolute;inset:0">{dots_html("s4-d")}</div>')
c.add(f'<div id="s4-ex" class="pen lab" style="left:120px;top:90px;font-size:70px;color:{YEL};border:4px dashed {YEL};padding:4px 26px;opacity:0;transform:rotate(-4deg)">예상</div>')
c.add(svg(f'<path id="s4-ar" d="M720,520 L1200,520" stroke="{YEL}" stroke-width="7" fill="none" stroke-linecap="round"/>'
          f'<path id="s4-a1" d="M740,495 L712,520 L740,545" stroke="{YEL}" stroke-width="7" fill="none"/><path id="s4-a2" d="M1180,495 L1208,520 L1180,545" stroke="{YEL}" stroke-width="7" fill="none"/>'))
c.add(f'<div id="s4-fr" class="pen lab" style="left:860px;top:430px;font-size:58px;color:{YEL};opacity:0">더 멀리</div>'
      f'<div id="s4-rl" class="tag" style="left:400px;top:800px;background:{RED};color:#fff;font-size:42px;opacity:0">위험한 곳 세포</div>'
      f'<div id="s4-gl" class="tag" style="left:1270px;top:800px;background:{GRN};color:#fff;font-size:42px;opacity:0">안전한 곳 세포</div>')
c.j(f'tl.fromTo("#s4-ex",{{opacity:0,scale:1.6}},{{opacity:1,scale:1,duration:.25,ease:"power4.in"}},{c.cue(4, .08)});')
tcol = c.cue(4, .45)
for k in range(len(DOTS)):
    c.j(f'tl.to("#s4-d{k}",{{backgroundColor:"{RED if side[k] else GRN}",duration:.15}},{tcol + (k % 30) * .02:.2f});')
c.j(f'tl.fromTo("#s4-rl",{{opacity:0,x:-80}},{{opacity:1,x:0,duration:.3}},{c.cue(5, .2)});')
c.j(f'tl.fromTo("#s4-gl",{{opacity:0,x:80}},{{opacity:1,x:0,duration:.3}},{c.cue(5, .25)});')
move_js(c, "s4-d", farR, farG, c.cue(5, .05), 1.3, "power2.inOut")
c.j(f'tl.fromTo("#s4-ar",{{drawSVG:"50% 50%"}},{{drawSVG:"0% 100%",duration:.6,ease:"power2.out"}},{c.cue(5, .45)});')
c.j(f'tl.fromTo("#s4-a1,#s4-a2",{{opacity:0}},{{opacity:1,duration:.15}},{c.cue(5, .5)});')
c.j(f'tl.fromTo("#s4-fr",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.25}},{c.cue(5, .55)});')
S4 = c

c = S("s5", dark=True)
# 시작 상태 = s4 끝 (멀리 갈라짐)
far_html = ""
FARPOS = []
iR = iG = 0
for k in range(len(DOTS)):
    if side[k]: (x, y) = farR[iR]; iR += 1
    else: (x, y) = farG[iG]; iG += 1
    FARPOS.append((x, y))
    far_html += f'<div class="dot" id="s5-d{k}" style="left:{x:.0f}px;top:{y:.0f}px;background:{RED if side[k] else GRN}"></div>'
c.add(svg(f'<circle id="s5-cr" cx="860" cy="520" r="290" fill="{RED}" fill-opacity=".10" stroke="{RED}" stroke-width="6"/>'
          f'<circle id="s5-cg" cx="1060" cy="520" r="290" fill="{GRN}" fill-opacity=".10" stroke="{GRN}" stroke-width="6"/>', 'id="s5-venn"'))
c.add(f'<div id="s5-ov" style="position:absolute;left:820px;top:300px;width:280px;height:440px;border-radius:50%;background:radial-gradient({VIO}AA,{VIO}00 70%);opacity:0"></div>')
c.add(f'<div id="s5-dots" style="position:absolute;inset:0">{far_html}</div>')
c.add(f'<div id="s5-ex" class="pen lab" style="left:120px;top:90px;font-size:70px;color:{YEL};border:4px dashed {YEL};padding:4px 26px;transform:rotate(-4deg)">예상</div>')
c.add(svg(f'<path id="s5-x" d="M110,150 L330,110" stroke="{RED}" stroke-width="9" stroke-linecap="round"/>'))
c.add(f'<div id="s5-rs" style="position:absolute;left:390px;top:70px;padding:4px 30px;border:9px solid {RED};border-radius:12px;color:{RED};font-family:Myeongjo;font-size:84px;transform:rotate(-5deg);opacity:0">결과</div>')
c.add(f'<div id="s5-ol" class="pen lab" style="left:880px;top:820px;font-size:60px;color:{VIO};opacity:0">겹쳤다</div>')
c.add(f'<div id="s5-who" class="tag" style="left:110px;top:860px;background:#EDE7DA;color:{INK};font-size:36px;opacity:0">마크 브랜던 · 맥길대 · 교신저자</div>')
c.add(f'<div id="s5-w1" class="my lab" style="left:1230px;top:120px;font-size:88px;color:#EDE7DA;opacity:0">날카롭게</div>'
      f'<div id="s5-w2" class="my lab" style="left:1260px;top:250px;font-size:96px;color:{VIO};opacity:0">흐리게</div>')
c.add(svg(f'<path id="s5-x2" d="M1220,180 L1600,160" stroke="{RED}" stroke-width="9" stroke-linecap="round"/>'))
c.j(f'tl.fromTo("#s5-x",{{drawSVG:"0%"}},{{drawSVG:"100%",duration:.25}},{c.cue(6, .05)});')
c.j(f'tl.fromTo("#s5-rs",{{opacity:0,scale:2}},{{opacity:1,scale:1,duration:.22,ease:"power4.in"}},{c.cue(6, .12)});')
move_js(c, "s5-d", ovR, ovG, c.cue(6, .45), 1.1, "back.inOut(1.4)", .003, base=FARPOS)
c.j(f'tl.fromTo("#s5-cr,#s5-cg",{{drawSVG:"0%",fillOpacity:0}},{{drawSVG:"100%",fillOpacity:.1,duration:.7,ease:"power1.inOut"}},{c.cue(6, .62)});')
c.j(f'tl.fromTo("#s5-ov",{{opacity:0,scale:.4}},{{opacity:1,scale:1,duration:.5,ease:"power2.out"}},{c.cue(6, .75)});')
c.j(f'tl.fromTo("#s5-ol",{{opacity:0,y:30}},{{opacity:1,y:0,duration:.25,ease:"back.out(2)"}},{c.cue(6, .78)});')
t7 = c.cue(7, 0)
c.j(f'tl.to("#s5-ex,#s5-x,#s5-rs,#s5-ol",{{opacity:0,duration:.25}},{t7});')
c.j(f'tl.fromTo("#s5-who",{{opacity:0,x:-100}},{{opacity:1,x:0,duration:.3,ease:"power3.out"}},{t7 + .1:.2f});')
c.j(f'tl.fromTo("#s5-w1",{{opacity:0,y:-20}},{{opacity:1,y:0,duration:.25}},{c.cue(7, .5)});')
c.j(f'tl.fromTo("#s5-x2",{{drawSVG:"0%"}},{{drawSVG:"100%",duration:.25}},{c.cue(7, .62)});')
c.j(f'tl.fromTo("#s5-w2",{{opacity:0,filter:"blur(0px)"}},{{opacity:1,filter:"blur(0px)",duration:.3}},{c.cue(7, .7)});')
c.j(f'tl.fromTo("#s5-venn",{{filter:"blur(0px)"}},{{filter:"blur(14px)",duration:1.4,ease:"sine.inOut"}},{c.cue(7, .72)});')
c.j(f'tl.fromTo("#s5-dots",{{filter:"blur(0px)"}},{{filter:"blur(5px)",duration:1.4,ease:"sine.inOut"}},{c.cue(7, .72)});')
c.j(f'tl.fromTo("#s5-w2",{{filter:"blur(0px)"}},{{filter:"blur(3px)",duration:1.0,ease:"sine.inOut"}},{c.cue(7, .85)});')
S5 = c

SCENES = [S1, S2, S3, S4, S5]
for s in SCENES:
    (HERE / "compositions" / f"{s.sid}.html").write_text(s.html(), encoding="utf-8")
caps = "".join(f'<div class="clip cap" id="cap{x["i"]}" data-start="{x["start"] + .05:.2f}" data-duration="{x["dur"] - .3:.2f}" data-track-index="20"><span>{x["text"]}</span></div>' for x in L)
aud = "".join(f'<audio id="vo{x["i"]}" class="clip" src="assets/vo/{x["file"]}" data-start="{x["start"]}" data-duration="{x["dur"]}" data-track-index="7" data-volume="1"></audio>' for x in L)
def _d(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(HERE / f)], capture_output=True, text=True).stdout)
SFX = [("whoosh-short", 0, .1), ("pop", 0, .42), ("click", 0, .85), ("whoosh", 1, .05), ("chime", 1, .25), ("whoosh-cinematic", 1, .66), ("click-soft", 1, .86),
       ("impact-bass-2", 2, .2), ("pop", 2, .5), ("whoosh-short", 2, .7), ("pencil", 3, .05), ("whoosh-cinematic", 3, .5), ("pop", 4, .08), ("whoosh", 5, .05),
       ("impact-bass-2", 6, .12), ("riser", 6, .4), ("click", 7, .62)]
for k, (n, i, fr) in enumerate(SFX):
    f = f"assets/sfx/{n}.{'wav' if n == 'pencil' else 'mp3'}"
    tt = round(L[i]["start"] + L[i]["dur"] * fr, 2)
    aud += f'<audio id="sx{k}" class="clip" src="{f}" data-start="{tt}" data-duration="{min(1.4, _d(f)):.2f}" data-track-index="{8 + k % 3}" data-volume="{0.18 if n in ("pencil", "riser") else 0.32}"></audio>'
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
print("END", END, {k: (v["start"], v["dur"]) for k, v in SC.items()})
