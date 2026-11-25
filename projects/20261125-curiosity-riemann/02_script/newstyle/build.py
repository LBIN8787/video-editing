"""리만가설 편 (새 스타일, HyperFrames). assets/vo/lines.json → index.html + compositions/s1~s10.html.
원칙 (2026-11-25 사용자): 선·그래프는 한 번에 그어지지 않고 말하는 동안 펜 끝이 따라가며 천천히 그려진다."""
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
L = json.load(open(HERE / "assets/vo/lines.json", encoding="utf-8"))
GAP, LEAD, CHGAP = 0.22, 0.5, 0.6
t, prev = LEAD, None
for x in L:
    if prev and x["scene"] != prev:
        t += CHGAP
    x["start"] = round(t, 2)
    t += x["dur"] + GAP
    prev = x["scene"]
END = round(t + 1.5, 2)
SC = []
for x in L:
    if not SC or SC[-1]["id"] != x["scene"]:
        SC.append({"id": x["scene"], "lines": []})
    SC[-1]["lines"].append(x["i"])
for k, s in enumerate(SC):
    s["start"] = 0.0 if k == 0 else round(L[s["lines"][0]]["start"] - 0.35, 2)
for k, s in enumerate(SC):
    s["end"] = SC[k + 1]["start"] if k + 1 < len(SC) else END
    s["dur"] = round(s["end"] - s["start"], 2)
SCN = {s["id"]: s for s in SC}

INK, ACC, GRY, BG, PAPER = "#1D2024", "#E2552B", "#8A8F96", "#E8E6E1", "#F3EEDF"
NOISE = ("url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'>"
         "<feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3' seed='4'/><feColorMatrix values='0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .55 0'/>"
         "</filter><rect width='300' height='300' filter='url(%23n)'/></svg>\")")


class Scene:
    def __init__(self, sid):
        self.sid, self.s = sid, SCN[sid]
        self.css, self.body, self.js = [], [], []
        self.n = 0

    def cue(self, i, off=0.0):
        """문장 i 가 시작하는 장면 안 시각 (i 는 lines.json 번호)."""
        return round(L[i]["start"] - self.s["start"] + off, 2)

    def dur(self, i):
        return L[i]["dur"]

    def id(self, p="e"):
        self.n += 1
        return f"{self.sid}-{p}{self.n}"

    def add(self, html, css=""):
        self.body.append(html)
        if css:
            self.css.append(css)

    def j(self, s):
        self.js.append(s)

    # ── 움직임 문법 ───────────────────────────────────────────────
    def pen(self, path_id, dot_id, t, d):
        """선이 펜 끝 점을 따라 천천히 그려짐 (사용자 2026-11-25)."""
        self.j(f'tl.fromTo("#{path_id}",{{drawSVG:"0%"}},{{drawSVG:"100%",duration:{d:.2f},ease:"none"}},{t:.2f});')
        if dot_id:
            self.j(f'tl.fromTo("#{dot_id}",{{opacity:0}},{{opacity:1,duration:.12}},{t:.2f});'
                   f'tl.to("#{dot_id}",{{motionPath:{{path:"#{path_id}",align:"#{path_id}",alignOrigin:[.5,.5]}},duration:{d:.2f},ease:"none"}},{t:.2f});'
                   f'tl.to("#{dot_id}",{{opacity:0,duration:.25}},{t + d:.2f});')

    def write(self, el_id, t, d):
        """글자가 왼쪽부터 써 내려가듯 나타남."""
        self.j(f'tl.fromTo("#{el_id}",{{clipPath:"inset(0 100% 0 0)",opacity:1}},{{clipPath:"inset(0 0% 0 0)",opacity:1,duration:{d:.2f},ease:"none"}},{t:.2f});')

    def appear(self, el_id, t, d=.5, y=24):
        self.j(f'tl.fromTo("#{el_id}",{{opacity:0,y:{y}}},{{opacity:1,y:0,duration:{d},ease:"power3.out"}},{t:.2f});')

    def html(self):
        d = self.s["dur"]
        base = (f"@font-face{{font-family:'NotoKR';src:url('assets/fonts/NotoSansKR-VF.ttf');font-weight:100 900}}"
                f"@font-face{{font-family:'Pen';src:url('assets/fonts/NanumPenScript-Regular.ttf')}}"
                f"#root{{position:absolute;inset:0;background:{BG};overflow:hidden;font-family:'NotoKR';color:{INK}}}"
                ".cam{position:absolute;inset:0;transform-origin:50% 50%}"
                f".grain{{position:absolute;inset:0;background-image:{NOISE};opacity:.16;mix-blend-mode:multiply;pointer-events:none}}"
                ".vig{position:absolute;inset:0;background:radial-gradient(ellipse at center,rgba(0,0,0,0) 55%,rgba(0,0,0,.10) 100%);pointer-events:none}"
                ".pen{font-family:'Pen';}"
                ".hw{position:absolute;white-space:nowrap;clip-path:inset(0 100% 0 0)}"
                ".dot{fill:" + INK + "}")
        return f"""<template>
<style>{base}{''.join(self.css)}</style>
<div id="root" data-composition-id="{self.sid}" data-width="1920" data-height="1080">
<div class="cam" id="{self.sid}-cam"><div class="cam" id="{self.sid}-in">{''.join(self.body)}</div></div>
<div class="grain"></div><div class="vig"></div>
</div>
<script>
gsap.registerPlugin(MotionPathPlugin, DrawSVGPlugin);
const tl = gsap.timeline({{ paused: true }});
tl.fromTo("#{self.sid}-cam", {{scale:1}}, {{scale:1.05, duration:{d}, ease:"sine.inOut"}}, 0);
{''.join(self.js)}
window.__timelines["{self.sid}"] = tl;
</script>
</template>
"""


def svg(sc, inner, w=1920, h=1080, x=0, y=0, extra=""):
    i = sc.id("svg")
    sc.add(f'<svg id="{i}" style="position:absolute;left:{x}px;top:{y}px;overflow:visible" width="{w}" height="{h}" {extra}>{inner}</svg>')
    return i


def path(pid, d, color=INK, w=6, extra=""):
    return (f'<path id="{pid}" d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" '
            f'{extra}/>')


def pendot(did, color=INK, r=9):
    return f'<circle id="{did}" r="{r}" fill="{color}" opacity="0"/>'


# ═════════ s1 원고 ═════════
def manuscript(sc, with_stamp=False):
    sc.add(f'<div id="{sc.sid}-ms" style="position:absolute;left:250px;top:150px;width:1420px;height:720px;background:{PAPER};'
           f'transform:rotate(-1.5deg);box-shadow:0 22px 44px rgba(20,22,26,.22);border-radius:4px">'
           f'<div class="hw pen" id="{sc.sid}-t1" style="left:80px;top:50px;font-size:64px;color:#2B2A27">Ueber die Anzahl der Primzahlen unter einer gegebenen Grösse.</div>'
           f'<div class="hw pen" id="{sc.sid}-t2" style="left:80px;top:180px;font-size:58px;color:#2B2A27">… und es ist <span id="{sc.sid}-hl" style="background:linear-gradient(rgba(226,85,43,.45),rgba(226,85,43,.45)) no-repeat 0 85%;background-size:0% 45%">sehr wahrscheinlich</span>, dass alle Wurzeln reell sind.</div>'
           f'<div class="hw pen" id="{sc.sid}-t3" style="left:80px;top:300px;font-size:52px;color:#2B2A27">Hiervon wäre allerdings ein strenger Beweis zu wünschen;</div>'
           f'<div class="hw pen" id="{sc.sid}-t4" style="left:80px;top:390px;font-size:52px;color:#2B2A27">ich habe indess die Aufsuchung desselben … vorläufig bei Seite gelassen</div>'
           f'<div class="hw pen" id="{sc.sid}-ko" style="left:560px;top:520px;font-size:96px;color:{ACC}">매우 그럴듯하다</div>'
           f'<div style="position:absolute;right:40px;bottom:24px;font-size:24px;color:#8B877C">B. 리만, 1859 · 원문 문장 (손글씨는 재현)</div></div>')


sc = Scene("s1")
manuscript(sc)
sc.add(f'<div id="s1-yr" style="position:absolute;left:120px;top:0px;font-weight:900;font-size:110px;letter-spacing:-4px">1859</div>'
       f'<div id="s1-nm" style="position:absolute;left:440px;top:40px;font-weight:800;font-size:46px;color:#4A4F56">베른하르트 리만</div>')
sc.j('tl.fromTo("#s1-ms",{y:900,rotation:4},{y:0,rotation:-1.5,duration:.9,ease:"power3.out"},.1);')
sc.appear("s1-yr", .6)
sc.appear("s1-nm", .9)
sc.write("s1-t1", sc.cue(0, .8), 3.2)
sc.write("s1-t2", sc.cue(1, .1), sc.dur(1) + 1.2)
sc.j(f'tl.fromTo("#s1-hl",{{backgroundSize:"0% 45%"}},{{backgroundSize:"100% 45%",duration:1.6,ease:"none"}},{sc.cue(2, .1)});')
sc.write("s1-ko", sc.cue(2, .4), 1.8)
sc.j(f'tl.to("#s1-ko",{{opacity:0,duration:.4}},{sc.cue(3, -.2)});')
sc.write("s1-t3", sc.cue(3, .1), 2.4)
sc.write("s1-t4", sc.cue(3, 2.3), 3.2)
S1 = sc

# ═════════ s2 167년 시간선 ═════════
sc = Scene("s2")
X0, X1, Y = 160, 1760, 520
yr = lambda y: X0 + (X1 - X0) * (y - 1859) / (2026 - 1859)
inner = (path("s2-ln", f"M{X0},{Y} L{X1},{Y}", INK, 7) + pendot("s2-pd")
         + "".join(f'<circle id="s2-c{k}" cx="{yr(y):.0f}" cy="{Y}" r="14" fill="{c}" opacity="0"/>' for k, (y, c) in enumerate([(1859, INK), (1900, INK), (2000, INK), (2026, ACC)])))
svg(sc, inner)
sc.add(f'<div id="s2-big" style="position:absolute;left:0;width:1920px;top:110px;text-align:center;font-weight:900;font-size:230px;letter-spacing:-8px">1859</div>'
       f'<div id="s2-yrs" style="position:absolute;left:0;width:1920px;top:395px;text-align:center;font-weight:800;font-size:52px;color:{ACC};opacity:0">167년</div>'
       + "".join(f'<div id="s2-l{k}" style="position:absolute;left:{yr(y) - 260:.0f}px;width:520px;text-align:center;top:{Y + 40 if y != 2026 else Y - 150}px;opacity:0">'
                 f'<div style="font-weight:900;font-size:56px">{y}</div><div style="font-weight:700;font-size:34px;color:#4A4F56">{lab}</div></div>'
                 for k, (y, lab) in enumerate([(1859, "리만의 논문"), (1900, "힐베르트 문제 8번"), (2000, "밀레니엄 문제 · 100만 달러"), (2026, "11월 20일")]))
       + f'<div id="s2-env" style="position:absolute;left:640px;top:620px;width:640px;height:300px;background:#FFF;box-shadow:0 18px 36px rgba(20,22,26,.2);opacity:0;border-radius:6px;overflow:hidden">'
       + "".join(f'<div style="position:absolute;left:50px;top:{40 + r * 34}px;width:{540 - (r % 3) * 70}px;height:14px;background:#CACDD1;border-radius:7px;filter:blur(3px);opacity:.55"></div>' for r in range(7))
       + f'<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:58px;color:{ACC};white-space:nowrap;background:rgba(255,255,255,.55)">아직 아무도 읽지 못한 증명</div></div>')
sc.pen("s2-ln", "s2-pd", sc.cue(4, .2), sc.dur(4) + sc.dur(5) + sc.dur(6) - .2)
sc.j(f'tl.fromTo("#s2-big",{{textContent:1859}},{{textContent:2026,duration:{sc.dur(4) - .4:.2f},ease:"power1.inOut",snap:{{textContent:1}}}},{sc.cue(4, .3)});')
sc.appear("s2-yrs", sc.cue(4, sc.dur(4) - .6))
for k, (i, off) in enumerate([(4, .2), (5, .1), (6, .2), (7, .3)]):
    sc.j(f'tl.fromTo("#s2-c{k}",{{opacity:0,scale:0,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:.3,ease:"back.out(3)"}},{sc.cue(i, off)});')
    sc.appear(f"s2-l{k}", sc.cue(i, off + .1))
sc.j(f'tl.to("#s2-l0,#s2-l1,#s2-l2,#s2-l3",{{y:-260,duration:.8,ease:"power2.inOut"}},{sc.cue(8, -.2)});'
     f'tl.to("#s2-big,#s2-yrs",{{opacity:0,duration:.4}},{sc.cue(8, -.2)});'
     f'tl.to("#{sc.sid}-svg1",{{y:-260,duration:.8,ease:"power2.inOut"}},{sc.cue(8, -.2)});')
sc.appear("s2-env", sc.cue(8, .5), .7, 60)
S2 = sc

# ═════════ s3 소수 수직선 ═════════
sc = Scene("s3")
N, NX0, NX1, NY = 60, 120, 1800, 560
nx = lambda n: NX0 + (NX1 - NX0) * (n - 1) / (N - 1)
primes = [p for p in range(2, N + 1) if all(p % q for q in range(2, int(p ** .5) + 1))]
inner = path("s3-ln", f"M{NX0 - 30},{NY} L{NX1 + 30},{NY}", INK, 5) + pendot("s3-pd")
inner += "".join(f'<line id="s3-tk{n}" x1="{nx(n):.0f}" y1="{NY - 10}" x2="{nx(n):.0f}" y2="{NY + 10}" stroke="{INK}" stroke-width="3" opacity="0"/>' for n in range(1, N + 1))
inner += "".join(f'<circle id="s3-p{p}" cx="{nx(p):.0f}" cy="{NY}" r="15" fill="{ACC}" opacity="0"/>' for p in primes)
gaps = [(23, 29), (31, 37), (47, 53)]
inner += "".join(path(f"s3-g{k}", f"M{nx(a):.0f},{NY + 50} Q{(nx(a) + nx(b)) / 2:.0f},{NY + 130} {nx(b):.0f},{NY + 50}", ACC, 5) for k, (a, b) in enumerate(gaps))
inner += "".join(path(f"s3-tw{k}", f"M{nx(a):.0f},{NY - 50} Q{(nx(a) + nx(b)) / 2:.0f},{NY - 95} {nx(b):.0f},{NY - 50}", INK, 4) for k, (a, b) in enumerate([(5, 7), (11, 13), (17, 19), (29, 31), (41, 43)]))
svg(sc, inner)
sc.add("".join(f'<div id="s3-n{p}" style="position:absolute;left:{nx(p) - 40:.0f}px;width:80px;text-align:center;top:{NY + (28 if k % 2 == 0 else 70)}px;font-weight:900;font-size:34px;opacity:0">{p}</div>' for k, p in enumerate(primes))
       + f'<div id="s3-h" style="position:absolute;left:120px;top:150px;font-weight:900;font-size:110px;letter-spacing:-3px;opacity:0">소수</div>'
       f'<div id="s3-hs" style="position:absolute;left:420px;top:190px;font-weight:700;font-size:44px;color:#4A4F56;opacity:0">1과 자기 자신으로만 나눠지는 수</div>'
       f'<div id="s3-g" style="position:absolute;left:0;width:1920px;top:780px;text-align:center;font-weight:900;font-size:64px;color:{ACC};opacity:0">간격이 제멋대로</div>'
       f'<div id="s3-t" style="position:absolute;left:0;width:1920px;top:330px;text-align:center;font-weight:800;font-size:44px;opacity:0">붙어서 나오다가 · 한참 안 나오다가</div>')
sc.appear("s3-h", sc.cue(9, .2))
sc.pen("s3-ln", "s3-pd", sc.cue(9, .4), sc.dur(9) + 1.0)
for n in range(1, N + 1):
    sc.j(f'tl.fromTo("#s3-tk{n}",{{opacity:0}},{{opacity:1,duration:.1}},{sc.cue(9, .4 + (sc.dur(9) + 1.0) * (n - 1) / N):.2f});')
sc.appear("s3-hs", sc.cue(10, .1))
first = [2, 3, 5, 7, 11]
for k, p in enumerate(primes):
    tt = sc.cue(10, 2.4 + k * .52) if p in first else sc.cue(10, 2.4 + 5 * .52 + (k - 5) * .28)
    sc.j(f'tl.fromTo("#s3-p{p}",{{opacity:0,scale:0,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:.25,ease:"back.out(3)"}},{tt:.2f});'
         f'tl.fromTo("#s3-n{p}",{{opacity:0}},{{opacity:1,duration:.2}},{tt:.2f});')
sc.appear("s3-g", sc.cue(11, .2))
for k in range(len(gaps)):
    sc.pen(f"s3-g{k}", None, sc.cue(11, .5 + k * .8), 1.2)
sc.appear("s3-t", sc.cue(12, .1))
for k in range(5):
    sc.pen(f"s3-tw{k}", None, sc.cue(12, .2 + k * .35), .8)
S3 = sc

# ═════════ s4 계단과 곡선, 그 사이의 틈 ═════════
sc = Scene("s4")
GX0, GX1, GY0, GY1, XM, YM = 200, 1700, 220, 860, 200, 50
gx = lambda x: GX0 + (GX1 - GX0) * x / XM
gy = lambda y: GY1 - (GY1 - GY0) * y / YM
pr = [p for p in range(2, XM + 1) if all(p % q for q in range(2, int(p ** .5) + 1))]
st, c, last = [f"M{gx(0):.1f},{gy(0):.1f}"], 0, 0
for p in pr:
    st.append(f"L{gx(p):.1f},{gy(c):.1f}")
    c += 1
    st.append(f"L{gx(p):.1f},{gy(c):.1f}")
st.append(f"L{gx(XM):.1f},{gy(c):.1f}")


def li(x):  # 로그 적분 Li(x) = ∫_2^x dt/ln t (사다리꼴)
    if x <= 2:
        return 0.0
    n, h = 400, (x - 2) / 400
    return sum((1 / math.log(2 + k * h) + 1 / math.log(2 + (k + 1) * h)) * h / 2 for k in range(n))


cv = "M" + " L".join(f"{gx(x):.1f},{gy(li(x)):.1f}" for x in [2 + k * (XM - 2) / 80 for k in range(81)])
inner = (path("s4-ax", f"M{GX0},{GY0 - 20} L{GX0},{GY1} L{GX1 + 30},{GY1}", "#9DA1A6", 4) + pendot("s4-pa", "#9DA1A6", 7)
         + path("s4-st", "".join(st), INK, 6) + pendot("s4-ps")
         + path("s4-cv", cv, ACC, 7) + pendot("s4-pc", ACC))
svg(sc, inner)
sc.add(f'<div id="s4-y" style="position:absolute;left:{GX0 + 20}px;top:150px;font-weight:800;font-size:40px;color:#4A4F56;opacity:0">그 수까지 소수의 개수</div>'
       f'<div id="s4-x" style="position:absolute;left:{GX1 - 140}px;top:{GY1 + 20}px;font-weight:800;font-size:36px;color:#4A4F56;opacity:0">수 (1~200)</div>'
       f'<div id="s4-sl" style="position:absolute;left:1180px;top:520px;font-weight:900;font-size:46px;opacity:0">계단: 실제 소수 개수</div>'
       f'<div id="s4-cl" style="position:absolute;left:760px;top:330px;font-weight:900;font-size:46px;color:{ACC};opacity:0">매끈한 곡선: 리만이 쓴 근사</div>'
       f'<div id="s4-zoom" style="position:absolute;left:1240px;top:640px;width:520px;padding:18px 26px;background:#fff;box-shadow:0 18px 36px rgba(20,22,26,.18);opacity:0">'
       f'<div style="font-weight:900;font-size:54px;color:{ACC}">이 틈의 크기</div><div style="font-weight:700;font-size:36px;margin-top:6px">← 리만가설이 참이면 가장 정확하게</div></div>')
sc.pen("s4-ax", "s4-pa", sc.cue(13, .1), sc.dur(13))
sc.appear("s4-y", sc.cue(13, .6))
sc.appear("s4-x", sc.cue(13, .9))
sc.pen("s4-st", "s4-ps", sc.cue(14, .1), sc.dur(14) * .6)
sc.appear("s4-sl", sc.cue(14, sc.dur(14) * .6))
sc.pen("s4-cv", "s4-pc", sc.cue(14, sc.dur(14) * .55), sc.dur(14) * .45 + .8)
sc.appear("s4-cl", sc.cue(14, sc.dur(14) + .2))
sc.j(f'tl.to("#{sc.sid}-in",{{scale:1.5,x:-420,y:-80,duration:1.4,ease:"power2.inOut"}},{sc.cue(15, .1)});')
sc.appear("s4-zoom", sc.cue(16, .2), .6, 40)
S4 = sc

# ═════════ s5 임계선 위의 영점 ═════════
sc = Scene("s5")
ZX, ZY0, ZY1, HMAX = 1060, 900, 140, 52
zy = lambda h: ZY0 - (ZY0 - ZY1) * h / HMAX
zeros = [14.135, 21.022, 25.011, 30.425, 32.935, 37.586, 40.919, 43.327, 48.005, 49.774]   # 제타 함수의 첫 영점들 (허수부, 널리 알려진 값)
inner = (path("s5-xa", f"M360,{ZY0} L1640,{ZY0}", "#9DA1A6", 4) + path("s5-ya", f"M760,{ZY0 + 40} L760,{ZY1 - 60}", "#9DA1A6", 4)
         + path("s5-cl", f"M{ZX},{ZY0 + 30} L{ZX},{ZY1 - 70}", ACC, 7) + pendot("s5-pd", ACC)
         + "".join(f'<circle id="s5-z{k}" cx="{ZX}" cy="{zy(h):.0f}" r="16" fill="{INK}" opacity="0"/>' for k, h in enumerate(zeros))
         + f'<circle id="s5-gh" cx="{ZX + 70}" cy="{ZY1 - 30}" r="16" fill="none" stroke="{INK}" stroke-width="4" stroke-dasharray="6 6" opacity="0"/>')
svg(sc, inner)
sc.add(f'<div id="s5-l0" style="position:absolute;left:{ZX - 300}px;top:{ZY0 - 160}px;font-weight:800;font-size:38px;color:{ACC};opacity:0">실수부 = 1/2</div>'
       f'<div id="s5-h" style="position:absolute;left:120px;top:110px;font-weight:900;font-size:86px;letter-spacing:-2px;opacity:0">영점</div>'
       f'<div id="s5-hs" style="position:absolute;left:120px;top:220px;font-weight:700;font-size:40px;color:#4A4F56;opacity:0">제타 함수의 특별한 점들</div>'
       f'<div id="s5-rh" style="position:absolute;left:120px;top:360px;width:560px;font-weight:900;font-size:58px;line-height:1.25;opacity:0">모두 한 줄 위에<br><span style="color:{ACC}">= 리만가설</span></div>'
       f'<div id="s5-cnt" style="position:absolute;left:1180px;top:420px;font-weight:900;font-size:110px;letter-spacing:-3px;opacity:0"><span id="s5-cv">0</span>조</div>'
       f'<div id="s5-cs" style="position:absolute;left:1190px;top:540px;font-weight:800;font-size:40px;color:#4A4F56;opacity:0">개 넘게 확인 — 모두 줄 위</div>'
       f'<div id="s5-q" style="position:absolute;left:{ZX + 110}px;top:{ZY1 - 90}px;font-weight:900;font-size:90px;color:{ACC};opacity:0">?</div>'
       f'<div id="s5-pf" style="position:absolute;left:120px;top:580px;opacity:0"><span class="pen" style="font-size:110px;color:{INK}">확인 ≠ 증명</span></div>')
sc.pen("s5-xa", None, sc.cue(17, .1), 1.6)
sc.pen("s5-ya", None, sc.cue(17, .6), 1.4)
sc.appear("s5-h", sc.cue(17, .3))
sc.appear("s5-hs", sc.cue(17, 1.0))
sc.pen("s5-cl", "s5-pd", sc.cue(18, .1), 2.6)
sc.appear("s5-l0", sc.cue(18, 1.2))
for k in range(len(zeros)):
    sc.j(f'tl.fromTo("#s5-z{k}",{{opacity:0,scale:0,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:.3,ease:"back.out(3)"}},{sc.cue(18, 1.6 + k * .42):.2f});')
sc.appear("s5-rh", sc.cue(18, sc.dur(18) - 1.5))
sc.appear("s5-cnt", sc.cue(19, .2))
sc.j(f'tl.fromTo("#s5-cv",{{textContent:0}},{{textContent:10,duration:{sc.dur(19) - .6:.2f},ease:"power2.out",snap:{{textContent:1}}}},{sc.cue(19, .3)});')
sc.appear("s5-cs", sc.cue(19, sc.dur(19) - .6))
sc.j(f'tl.to("#{sc.sid}-in",{{y:40,scale:1.03,duration:{sc.dur(20) + sc.dur(21):.2f},ease:"sine.inOut"}},{sc.cue(20, 0)});')
sc.j(f'tl.fromTo("#s5-gh",{{opacity:0}},{{opacity:1,duration:.6}},{sc.cue(21, .4)});')
sc.appear("s5-q", sc.cue(21, .8))
sc.j(f'tl.to("#{sc.sid}-in",{{y:0,scale:1,duration:1.0,ease:"power2.inOut"}},{sc.cue(22, -.1)});')
sc.write("s5-pf", sc.cue(22, .8), 1.8)
S5 = sc

# ═════════ s6 같은 날 두 증명 ═════════
sc = Scene("s6")
inner = path("s6-dv", "M960,90 L960,900", INK, 4) + pendot("s6-pd")
svg(sc, inner)
pages = "".join(f'<div class="s6-pg" id="s6-pg{k}" style="left:{300 + (k % 3) * 4}px;top:{760 - k * 18}px;transform:rotate({(k % 5 - 2) * .8}deg)"></div>' for k in range(22))
code = "".join(f'<div class="s6-cd">{ln}</div>' for ln in [
    "theorem step_%d : ∀ s, P s → Q s := by" % k if k % 4 == 0 else
    ("  intro s hs" if k % 4 == 1 else ("  exact lemma_%d s hs" % (k * 37 % 997) if k % 4 == 2 else "  simp [zeta_eq, h_%d]" % k)) for k in range(90)])
sc.add(f'<div id="s6-date" style="position:absolute;left:0;width:1920px;top:40px;text-align:center;font-weight:900;font-size:64px;opacity:0">2026. 11. 20</div>'
       f'<div id="s6-L" style="position:absolute;left:0;top:0;width:960px;height:1080px">{pages}'
       f'<div id="s6-lt" style="position:absolute;left:120px;top:170px;font-weight:900;font-size:76px;opacity:0">940쪽</div>'
       f'<div id="s6-ls" style="position:absolute;left:120px;top:270px;font-weight:700;font-size:40px;color:#4A4F56;opacity:0">스탠퍼드 수학자의 원고</div>'
       f'<div id="s6-lq" style="position:absolute;left:120px;top:330px;font-weight:900;font-size:46px;color:{INK};opacity:0">"전부 사람이 쓴, AI 없는 증명"</div>'
       f'<div id="s6-lr" style="position:absolute;left:120px;top:395px;font-weight:600;font-size:28px;color:#7A7F86;opacity:0">— 미국수학회 회장 (블로그 소개)</div></div>'
       f'<div id="s6-R" style="position:absolute;left:960px;top:0;width:960px;height:1080px;overflow:hidden">'
       f'<div id="s6-codebox" style="position:absolute;left:90px;top:440px;width:780px;height:420px;background:#22262B;border-radius:12px;overflow:hidden;opacity:0">'
       f'<div id="s6-code" style="position:absolute;left:28px;top:20px">{code}</div>'
       f'<div style="position:absolute;right:14px;bottom:10px;font-size:20px;color:#8A9099">예시 화면 · 실제 증명 코드 아님</div></div>'
       f'<div id="s6-rt" style="position:absolute;left:90px;top:170px;font-weight:900;font-size:76px;opacity:0">1,700만 줄</div>'
       f'<div id="s6-rs" style="position:absolute;left:90px;top:270px;font-weight:700;font-size:40px;color:#4A4F56;opacity:0">레벤트 알푀게 (앤트로픽) · 클로드와 함께</div>'
       f'<div id="s6-rq" class="hw pen" style="left:90px;top:325px;font-size:58px;color:{ACC}">"클로드와 함께, 증명을 발견했다고 믿는다"</div></div>',
       ".s6-pg{position:absolute;width:420px;height:40px;background:#FBFAF7;border:1px solid #D9D6CE;box-shadow:0 4px 8px rgba(20,22,26,.12);opacity:0}"
       ".s6-cd{font-family:'JetBrains Mono',monospace;font-size:22px;line-height:1.5;color:#C9D1D9;white-space:nowrap}")
sc.appear("s6-date", sc.cue(23, .1))
sc.pen("s6-dv", "s6-pd", sc.cue(23, .6), sc.dur(23) - .4)
sc.appear("s6-lt", sc.cue(24, .2))
sc.appear("s6-ls", sc.cue(24, .7))
for k in range(22):
    sc.j(f'tl.fromTo("#s6-pg{k}",{{opacity:0,y:-60}},{{opacity:1,y:0,duration:.22,ease:"power2.out"}},{sc.cue(24, 1.0 + k * (sc.dur(24) - 1.2) / 22):.2f});')
sc.appear("s6-lq", sc.cue(25, .3))
sc.appear("s6-lr", sc.cue(25, 1.0))
sc.appear("s6-rs", sc.cue(26, .4))
sc.appear("s6-rt", sc.cue(26, .1))
sc.j(f'tl.fromTo("#s6-codebox",{{opacity:0,y:40}},{{opacity:1,y:0,duration:.6,ease:"power3.out"}},{sc.cue(26, 1.2)});'
     f'tl.fromTo("#s6-code",{{y:0}},{{y:-1500,duration:{sc.s["dur"] - sc.cue(26, 1.2):.2f},ease:"none"}},{sc.cue(26, 1.2)});')
sc.write("s6-rq", sc.cue(27, .1), sc.dur(27))
S6 = sc

# ═════════ s7 Lean 검사 ═════════
sc = Scene("s7")
rows = "".join(f'<div class="s7-r" id="s7-r{k}"><span class="s7-c">{["theorem", "lemma", "have", "exact", "simp", "intro"][k % 6]} …</span><span class="s7-ok" id="s7-k{k}">✓</span></div>' for k in range(12))
sc.add(f'<div id="s7-gate" style="position:absolute;left:560px;top:120px;width:800px;height:740px;border:8px solid {INK};border-radius:18px;background:#FBFAF7;opacity:0">'
       f'<div style="position:absolute;left:0;right:0;top:-70px;text-align:center;font-weight:900;font-size:52px">Lean 검사기</div>'
       f'<div style="position:absolute;left:40px;top:30px">{rows}</div></div>'
       f'<div id="s7-a" style="position:absolute;left:90px;top:300px;width:420px;font-weight:800;font-size:40px;line-height:1.3;opacity:0">사람이 읽는 글 ✗<br><span style="color:{ACC}">컴퓨터가 검사하는 코드</span></div>'
       f'<div id="s7-m1" style="position:absolute;left:1420px;top:250px;width:440px;font-weight:800;font-size:36px;line-height:1.3;opacity:0">MIT 앤드루 서덜랜드<br><span style="font-weight:600;color:#4A4F56">직접 실행</span></div>'
       f'<div id="s7-m2" style="position:absolute;left:1420px;top:420px;width:440px;font-weight:800;font-size:36px;line-height:1.3;opacity:0">Lean·Mathlib 공동체<br><span style="font-weight:600;color:#4A4F56">"맞다고 믿는다" 성명</span></div>'
       f'<div id="s7-flag" style="position:absolute;left:90px;top:620px;width:420px;padding:16px 22px;background:#fff;border-left:12px solid {ACC};box-shadow:0 12px 24px rgba(20,22,26,.15);opacity:0">'
       f'<div style="font-weight:900;font-size:40px">사람의 940쪽</div><div style="font-weight:700;font-size:32px;color:{ACC}">몇 시간 만에 문제 지적</div></div>'
       f'<div id="s7-pass" style="position:absolute;left:1420px;top:620px;width:440px;font-weight:900;font-size:56px;color:#2E7D4F;opacity:0">1,700만 줄<br>통과 중 ✓</div>',
       ".s7-r{display:flex;justify-content:space-between;width:720px;font-family:'JetBrains Mono',monospace;font-size:30px;line-height:56px;opacity:0}"
       ".s7-c{color:#3A3F46}.s7-ok{color:#2E7D4F;font-weight:900;opacity:0}")
sc.j('tl.fromTo("#s7-gate",{opacity:0,scale:.94},{opacity:1,scale:1,duration:.6,ease:"power3.out"},.2);')
sc.appear("s7-a", sc.cue(29, .4))
total = sc.cue(33, sc.dur(33)) - sc.cue(30, 0)
for k in range(12):
    tt = sc.cue(30, .3) + k * (total - 1) / 12
    sc.j(f'tl.fromTo("#s7-r{k}",{{opacity:0,x:-30}},{{opacity:1,x:0,duration:.3}},{tt:.2f});'
         f'tl.fromTo("#s7-k{k}",{{opacity:0,scale:2}},{{opacity:1,scale:1,duration:.25,ease:"back.out(3)"}},{tt + .5:.2f});')
sc.appear("s7-m1", sc.cue(31, .3))
sc.appear("s7-m2", sc.cue(31, sc.dur(31) * .5))
sc.appear("s7-flag", sc.cue(32, .3), .5, 30)
sc.appear("s7-pass", sc.cue(33, .3), .5, 30)
S7 = sc

# ═════════ s8 맞지만, 아무도 모른다 ═════════
sc = Scene("s8")
head = ("M300,700 C300,520 360,380 520,350 C690,320 800,420 810,560 C815,620 850,650 860,700 C870,740 830,760 815,760 "
        "C815,820 790,850 740,850 L700,850 L700,930")
inner = path("s8-hd", head, INK, 8) + pendot("s8-ph")
svg(sc, inner)
sc.add(f'<div id="s8-q" style="position:absolute;left:470px;top:440px;font-weight:900;font-size:220px;color:{ACC};opacity:0">?</div>'
       + "".join(f'<div class="s8-pg" id="s8-pg{k}" style="left:{960 + (k % 4) * 6}px;top:{520 - k * 14}px;transform:rotate({(k % 5 - 2) * 1.1}deg)"></div>' for k in range(26))
       + f'<div id="s8-pn" style="position:absolute;left:1000px;top:150px;font-weight:900;font-size:110px;letter-spacing:-3px;opacity:0">25만 쪽+</div>'
       f'<div id="s8-ps" style="position:absolute;left:1010px;top:280px;font-weight:700;font-size:38px;color:#4A4F56;opacity:0">AI 로 쓴 영어 설명 (올리지 않음)</div>'
       f'<div id="s8-g1o" style="position:absolute;left:1100px;top:640px;width:560px;height:54px;border:5px solid {INK};border-radius:27px;box-sizing:border-box;opacity:0">'
       f'<div id="s8-g1f" style="position:absolute;left:4px;top:4px;right:4px;bottom:4px;border-radius:20px;background:{INK};transform-origin:0 50%;transform:scaleX(0)"></div></div>'
       f'<div id="s8-g2o" style="position:absolute;left:1100px;top:760px;width:560px;height:54px;border:5px solid {INK};border-radius:27px;box-sizing:border-box;opacity:0"></div>'
       f'<div id="s8-g1l" style="position:absolute;left:1100px;top:585px;font-weight:900;font-size:40px;opacity:0">맞다 (컴퓨터)</div>'
       f'<div id="s8-g2l" style="position:absolute;left:1100px;top:705px;font-weight:900;font-size:40px;color:{ACC};opacity:0">왜 맞는지 (사람) — ?</div>'
       f'<div id="s8-ins" style="position:absolute;left:0;width:1920px;top:110px;text-align:center;opacity:0"><span class="pen" style="font-size:120px">맞다 ≠ 이해했다</span></div>'
       f'<div id="s8-hg" style="position:absolute;left:1100px;top:300px;width:520px;padding:20px 28px;background:#fff;box-shadow:0 14px 28px rgba(20,22,26,.16);opacity:0">'
       f'<div style="font-weight:900;font-size:44px">사람의 검토</div><div style="font-weight:700;font-size:36px;color:#4A4F56">이제 시작 · 몇 달 ~ 몇 년</div>'
       f'<div style="font-weight:600;font-size:30px;color:{ACC};margin-top:10px">문제를 코드로 옮긴 방식도 점검</div></div>',
       ".s8-pg{position:absolute;width:300px;height:34px;background:#FBFAF7;border:1px solid #D9D6CE;box-shadow:0 3px 6px rgba(20,22,26,.12);opacity:0}")
sc.pen("s8-hd", "s8-ph", sc.cue(34, .1), sc.dur(34) + 1.0)
sc.appear("s8-q", sc.cue(35, .2))
sc.appear("s8-pn", sc.cue(36, .1))
sc.appear("s8-ps", sc.cue(36, .6))
for k in range(26):
    sc.j(f'tl.fromTo("#s8-pg{k}",{{opacity:0,y:-50}},{{opacity:1,y:0,duration:.18}},{sc.cue(35, .5) + k * (sc.dur(35) + sc.dur(36) - .8) / 26:.2f});')
sc.j(f'tl.to(".s8-pg,#s8-pn,#s8-ps",{{opacity:0,duration:.4}},{sc.cue(37, -.1)});')
sc.j(f'tl.fromTo("#s8-g1o,#s8-g2o",{{opacity:0}},{{opacity:1,duration:.4}},{sc.cue(37, .2)});')
sc.appear("s8-g1l", sc.cue(37, .3))
sc.j(f'tl.fromTo("#s8-g1f",{{scaleX:0}},{{scaleX:1,duration:{sc.dur(37):.2f},ease:"power1.inOut"}},{sc.cue(37, .6)});')
sc.appear("s8-g2l", sc.cue(38, .2))
sc.write("s8-ins", sc.cue(39, .2), 2.2)
sc.j(f'tl.to("#s8-q",{{opacity:0,duration:.3}},{sc.cue(40, -.1)});')
sc.appear("s8-hg", sc.cue(40, .2), .6, 30)
S8 = sc

# ═════════ s9 두 목소리 ═════════
sc = Scene("s9")
beam = path("s9-bm", "M460,330 L1460,330", INK, 8) + path("s9-pl", "M960,330 L960,880", INK, 8) + pendot("s9-pd")
svg(sc, beam)
V = [("s9-v1", 140, 380, "앤드루 서덜랜드 · MIT", "This is indeed an historic moment.", "정말 역사적인 순간", 43),
     ("s9-v2", 140, 640, "제임스 메이너드 · 옥스퍼드, 필즈상", "…clearly a historic milestone in mathematics.", "수학의 역사적 이정표", 44),
     ("s9-v3", 1140, 380, "케빈 버저드 · 임페리얼 칼리지", "…we don't even know why the theorem is true.", "왜 참인지조차 모른다", 45),
     ("s9-v4", 1140, 640, "유네스 람주리 · 로렌대", "Mathematics is mainly about understanding why…", "수학은 왜 참인지 이해하는 일", 46)]
for vid, x, y, who, en, ko, cue in V:
    sc.add(f'<div id="{vid}" style="position:absolute;left:{x}px;top:{y}px;width:640px;padding:20px 26px;background:#fff;box-shadow:0 14px 28px rgba(20,22,26,.16);opacity:0">'
           f'<div style="font-weight:900;font-size:44px;line-height:1.2">{ko}</div><div style="font-weight:500;font-style:italic;font-size:26px;color:#6A6F76;margin-top:6px">"{en}"</div>'
           f'<div style="font-weight:800;font-size:28px;color:{ACC};margin-top:8px">{who}</div></div>')
sc.add(f'<div id="s9-h1" style="position:absolute;left:140px;top:240px;font-weight:900;font-size:58px;opacity:0">역사적 순간</div>'
       f'<div id="s9-h2" style="position:absolute;left:1140px;top:240px;font-weight:900;font-size:58px;color:{ACC};opacity:0">이유를 모른다</div>'
       f'<div id="s9-v5" style="position:absolute;left:560px;top:40px;width:800px;padding:16px 26px;background:{INK};color:#fff;opacity:0">'
       f'<div style="font-weight:900;font-size:38px">아비셰크 사하 · 런던 퀸메리대</div><div style="font-weight:700;font-size:32px">"내 머릿속 세계가 무너졌다" · 공은 사람(알푀게)에게</div></div>')
sc.pen("s9-bm", "s9-pd", sc.cue(42, .1), sc.dur(42))
sc.pen("s9-pl", None, sc.cue(42, .5), sc.dur(42))
sc.appear("s9-h1", sc.cue(43, .1))
sc.appear("s9-v1", sc.cue(43, 2.6), .5, 30)
sc.appear("s9-v2", sc.cue(44, 1.6), .5, 30)
sc.appear("s9-h2", sc.cue(45, .1))
sc.appear("s9-v3", sc.cue(45, 2.6), .5, 30)
sc.appear("s9-v4", sc.cue(46, 1.4), .5, 30)
sc.j(f'tl.to("#s9-v1,#s9-v2,#s9-v3,#s9-v4,#s9-h1,#s9-h2,#{sc.sid}-svg1",{{opacity:.35,duration:.4}},{sc.cue(47, -.1)});')
sc.appear("s9-v5", sc.cue(47, .3), .5, 30)
S9 = sc

# ═════════ s10 다시, 1859년의 한 문장 ═════════
sc = Scene("s10")
manuscript(sc)
sc.add(f'<div id="s10-st" data-layout-allow-overlap style="position:absolute;left:1080px;top:520px;padding:10px 34px;border:12px solid {ACC};border-radius:14px;color:{ACC};'
       f'font-weight:900;font-size:76px;transform:rotate(-8deg);white-space:nowrap;opacity:0">컴퓨터 검사 통과</div>'
       f'<div id="s10-st2" style="position:absolute;left:1180px;top:650px;font-weight:800;font-size:38px;color:#4A4F56;transform:rotate(-8deg);opacity:0">사람의 검토는 진행 중</div>'
       f'<div id="s10-q" class="hw pen" style="left:0;width:1920px;text-align:center;top:780px;font-size:96px;color:{INK}">소수는 왜, 한 줄로 서 있을까?</div>')
sc.j('tl.set("#s10-t1,#s10-t2,#s10-t3,#s10-t4",{clipPath:"inset(0 0% 0 0)"},0);')
sc.j(f'tl.fromTo("#s10-hl",{{backgroundSize:"0% 45%"}},{{backgroundSize:"100% 45%",duration:1.4,ease:"none"}},{sc.cue(49, .3)});')
sc.j(f'tl.fromTo("#s10-st",{{opacity:0,scale:1.8}},{{opacity:1,scale:1,duration:.3,ease:"back.out(2.2)"}},{sc.cue(50, .4)});')
sc.appear("s10-st2", sc.cue(50, 1.0))
sc.j(f'tl.to("#s10-ms,#s10-st,#s10-st2",{{y:-90,duration:.8,ease:"power2.inOut"}},{sc.cue(51, .2)});')
sc.write("s10-q", sc.cue(52, .1), sc.dur(52) + .6)
S10 = sc

SCENES = [S1, S2, S3, S4, S5, S6, S7, S8, S9, S10]
for s in SCENES:
    (HERE / "compositions" / f"{s.sid}.html").write_text(s.html(), encoding="utf-8")

# ── 자막·목소리·효과음 ────────────────────────────────────────────
def chunks(text, n=30):
    if len(text) <= n:
        return [text]
    mid = len(text) // 2
    cut = min((k for k, c in enumerate(text) if c in ",." and 8 < k < len(text) - 6), key=lambda k: abs(k - mid), default=None)
    if cut is None:
        sp = [k for k, c in enumerate(text) if c == " "]
        cut = min(sp, key=lambda k: abs(k - mid)) if sp else mid
    return [text[:cut + 1].strip(), text[cut + 1:].strip()]


caps = []   # 비례 자막 금지(메모리 규칙) — 문장 하나를 말하는 동안 통째로, 길면 두 줄로 감쌈
for x in L:
    caps.append(f'<div class="clip cap" id="cap{x["i"]}" data-start="{x["start"] + .05:.2f}" data-duration="{x["dur"] - .3:.2f}" data-track-index="20"><span>{x["text"]}</span></div>')
SCS = {s.sid: s for s in SCENES}
sfx = []
for s in SCENES:
    base = s.s["start"]
    for js in s.js:
        if "drawSVG:\"100%\"" in js:
            tt = float(js.rsplit(",", 1)[1].rstrip(");"))
            sfx.append(("pencil", round(base + tt, 2)))
sfx += [("impact-bass-2", round(SCN["s10"]["start"] + SCS["s10"].cue(50, .4), 2)), ("whoosh", round(SCN["s1"]["start"] + .1, 2))]
sfx = sorted(sfx, key=lambda z: z[1])
dedup, lastt = [], -9
for n, tt in sfx:
    if tt - lastt > .8:
        dedup.append((n, tt))
        lastt = tt
aud = "".join(f'<audio id="vo{x["i"]}" class="clip" src="assets/vo/{x["file"]}" data-start="{x["start"]}" data-duration="{x["dur"]}" data-track-index="7" data-volume="1"></audio>' for x in L)
import subprocess
def _d(f):
    return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(HERE / f)],capture_output=True,text=True).stdout)
SFXD = {n: _d(f"assets/sfx/{n}.{'wav' if n == 'pencil' else 'mp3'}") for n in set(n for n, _ in dedup)}
aud += "".join(f'<audio id="sx{k}" class="clip" src="assets/sfx/{n}.{"wav" if n == "pencil" else "mp3"}" data-start="{tt}" data-duration="{min(1.2, SFXD[n]):.2f}" data-track-index="{8 + k % 3}" data-volume="{0.18 if n == "pencil" else 0.35}"></audio>'
               for k, (n, tt) in enumerate(dedup))
hosts = "".join(f'<div id="{s.sid}" data-composition-id="{s.sid}" data-composition-src="compositions/{s.sid}.html" data-start="{s.s["start"]}" '
                f'data-duration="{s.s["dur"]}" data-track-index="1" data-track-kind="graphics" data-width="1920" data-height="1080"></div>' for s in SCENES)
index = f"""<!doctype html><html><head><meta charset="utf-8">
<script src="assets/gsap.min.js"></script><script src="assets/MotionPathPlugin.min.js"></script><script src="assets/DrawSVGPlugin.min.js"></script>
<style>
@font-face{{font-family:'NotoKR';src:url('assets/fonts/NotoSansKR-VF.ttf');font-weight:100 900}}
.cap{{position:absolute;left:0;width:1920px;top:930px;text-align:center;z-index:50;font-family:'NotoKR'}}
.cap span{{display:inline-block;background:rgba(29,32,36,.86);color:#fff;font-weight:700;font-size:44px;padding:8px 24px;border-radius:8px;max-width:1500px;line-height:1.35}}
</style></head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{END}" data-width="1920" data-height="1080">
{hosts}{''.join(caps)}{aud}
</div>
<script>window.__timelines["main"] = gsap.timeline({{ paused: true }});</script>
</body></html>
"""
(HERE / "index.html").write_text(index, encoding="utf-8")
print("END", END, [(s.sid, s.s["start"], s.s["dur"]) for s in SCENES], "sfx", len(dedup))
