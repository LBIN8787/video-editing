"""AI 암호 해독 편 — D3 샘플(대본 1~2장). 이미지 중심 새 방식 (docs/71).
원칙: 장면마다 실제 이미지·그림 사물, 글자는 쪽지·이름표, 움직임 속도는 역할별(등장 .3 · 강조 .6 · 과정 1~1.4 · 카메라 계속), 같은 움직임 세 번 연속 금지."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
L = json.load(open(HERE / "assets/vo/lines.json", encoding="utf-8"))
GAP, LEAD = 0.22, 0.4
t = LEAD
for x in L:
    x["start"] = round(t, 2)
    t += x["dur"] + GAP
END = round(t + 1.0, 2)
GROUPS = [("c1", [0, 1]), ("c2", [2, 3]), ("c3", [4, 5]), ("c4", [6, 7, 8]), ("c5", [9]), ("c6", [10, 11])]
SC = {}
for k, (sid, idx) in enumerate(GROUPS):
    SC[sid] = {"start": 0.0 if k == 0 else round(L[idx[0]]["start"] - .3, 2), "lines": idx}
for k, (sid, _) in enumerate(GROUPS):
    SC[sid]["end"] = SC[GROUPS[k + 1][0]]["start"] if k + 1 < len(GROUPS) else END
    SC[sid]["dur"] = round(SC[sid]["end"] - SC[sid]["start"], 2)

INK, RED, NAVY, YEL = "#2B2F3A", "#B23A2F", "#22345F", "rgba(236,200,80,.75)"


class S:
    def __init__(self, sid, bg="paper"):
        self.sid, self.s, self.bg = sid, SC[sid], bg
        self.body, self.js, self.n = [], [], 0

    def cue(self, i, frac=0.0, off=0.0):
        """문장 i 의 frac(0~1) 지점 + off 초 (장면 안 시각)."""
        return round(L[i]["start"] + L[i]["dur"] * frac - self.s["start"] + off, 2)

    def add(self, h):
        self.body.append(h)

    def j(self, s):
        self.js.append(s)

    # 움직임 (역할별 속도)
    def pop(self, i, t, d=.3):
        self.j(f'tl.fromTo("#{i}",{{opacity:0,scale:.7}},{{opacity:1,scale:1,duration:{d},ease:"back.out(2.2)"}},{t});')

    def slide(self, i, t, dx=-500, d=.35, rot=0):
        self.j(f'tl.fromTo("#{i}",{{opacity:0,x:{dx},rotation:{rot - 6}}},{{opacity:1,x:0,rotation:{rot},duration:{d},ease:"power3.out"}},{t});')

    def rise(self, i, t, d=.45):
        self.j(f'tl.fromTo("#{i}",{{opacity:0,y:120}},{{opacity:1,y:0,duration:{d},ease:"power3.out"}},{t});')

    def fade(self, i, t, d=.4, to=1):
        self.j(f'tl.fromTo("#{i}",{{opacity:{1 - to}}},{{opacity:{to},duration:{d}}},{t});')

    def stamp(self, i, t):
        self.j(f'tl.fromTo("#{i}",{{opacity:0,scale:1.9}},{{opacity:1,scale:1,duration:.22,ease:"power4.in"}},{t});')

    def marker(self, i, t, d=.6):
        self.j(f'tl.fromTo("#{i}",{{backgroundSize:"0% 42%"}},{{backgroundSize:"100% 42%",duration:{d},ease:"power2.out"}},{t});')

    def draw(self, i, t, d):
        self.j(f'tl.fromTo("#{i}",{{drawSVG:"0%"}},{{drawSVG:"100%",duration:{d},ease:"power1.inOut"}},{t});')

    def kb(self, i, t0, d, s0=1.0, s1=1.08, x=0, y=0):
        self.j(f'tl.fromTo("#{i}",{{scale:{s0},x:0,y:0}},{{scale:{s1},x:{x},y:{y},duration:{d},ease:"none"}},{t0});')

    def polaroid(self, i, img, x, y, w, cap, rot=0, credit=""):
        self.add(f'<div id="{i}" class="pol" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg);opacity:0">'
                 f'<img src="assets/img/{img}" style="width:{w - 28}px;height:{(w - 28) * 1.2:.0f}px;object-fit:cover;object-position:50% 20%">'
                 f'<div class="pen" style="font-size:40px;color:{INK};text-align:center;margin-top:6px">{cap}</div></div>')

    def note(self, i, x, y, text, size=44, color=INK, rot=-3, bg="#F6E7A8"):
        self.add(f'<div id="{i}" class="note pen" style="left:{x}px;top:{y}px;font-size:{size}px;color:{color};background:{bg};transform:rotate({rot}deg);opacity:0">{text}</div>')

    def obj(self, i, img, x, y, w, rot=0, extra=""):
        self.add(f'<img id="{i}" src="assets/gen/{img}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg);'
                 f'filter:drop-shadow(0 16px 18px rgba(30,24,16,.28));opacity:0;{extra}">')

    def fixjs(self):
        import re
        seen, out = set(), []
        for x in self.js:
            m = re.match(r'tl\.fromTo\("([^"]+)"', x)
            if m:
                if m.group(1) in seen:
                    a, b = x.rsplit("},", 1)
                    x = a + ",immediateRender:false}," + b
                seen.add(m.group(1))
            out.append(x)
        return out

    def html(self):
        bgimg = "paper.jpg" if self.bg == "paper" else "paper_dark.jpg"
        d = self.s["dur"]
        return f"""<template>
<style>
@font-face{{font-family:'NotoKR';src:url('assets/fonts/NotoSansKR-VF.ttf');font-weight:100 900}}
@font-face{{font-family:'Pen';src:url('assets/fonts/NanumPenScript-Regular.ttf')}}
@font-face{{font-family:'Myeongjo';src:url('assets/fonts/NanumMyeongjo-ExtraBold.ttf')}}
#root{{position:absolute;inset:0;overflow:hidden;font-family:'NotoKR';color:{INK};background:#E8E3D9}}
.bg{{position:absolute;inset:-40px;background:url('assets/img/{bgimg}') center/cover}}
.cam{{position:absolute;inset:0;transform-origin:50% 50%}}
.pen{{font-family:'Pen'}}
.my{{font-family:'Myeongjo'}}
.pol{{position:absolute;background:#FBF9F4;padding:14px 14px 10px;box-shadow:0 14px 26px rgba(30,24,16,.3)}}
.note{{position:absolute;padding:10px 26px 12px;box-shadow:0 8px 14px rgba(30,24,16,.22);white-space:nowrap}}
.mk{{background:linear-gradient({YEL},{YEL}) no-repeat 0 90%;background-size:0% 42%}}
.tag{{position:absolute;font-size:22px;color:#6E6A60;background:rgba(255,255,255,.7);padding:2px 10px}}
</style>
<div id="root" data-composition-id="{self.sid}" data-width="1920" data-height="1080">
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


# ── c1 지도 · 두 초상 · 편지가 날아감 ──────────────────────────────
c = S("c1")
c.add('<div id="c1-map" style="position:absolute;left:220px;top:90px;width:1480px;height:840px;overflow:hidden;opacity:0;'
      'box-shadow:0 18px 34px rgba(30,24,16,.3);transform:rotate(-1.5deg)"><img id="c1-mapi" src="assets/img/map1809.jpg" style="width:1480px;height:1077px;object-fit:cover;margin-top:-120px"></div>')
c.add('<div class="tag" style="left:240px;top:930px">1809년 북이탈리아 지도 · 퍼블릭 도메인 · 위키미디어 공용</div>')
c.note("c1-n", 120, 60, "1809년 봄 · 이탈리아", 56)
c.polaroid("c1-eu", "eugene.jpg", 150, 260, 340, "외젠 드 보아르네", -5)
c.polaroid("c1-ma", "marmont.jpg", 1430, 250, 340, "마르몽 장군", 4)
c.add(f'<svg style="position:absolute;left:0;top:0" width="1920" height="1080"><path id="c1-rt" d="M480,560 C 800,380 1100,380 1430,520" fill="none" stroke="{RED}" stroke-width="6" stroke-dasharray="14 12"/></svg>')
c.obj("c1-let", "letter_sealed.png", 420, 470, 190)
c.obj("c1-cou", "courier.png", 820, 640, 260)
c.j('tl.fromTo("#c1-map",{opacity:0,scale:1.08},{opacity:1,scale:1,duration:.7,ease:"power2.out"},.1);')
c.kb("c1-mapi", .1, SC["c1"]["dur"], 1.0, 1.12, -40, -20)
c.pop("c1-n", c.cue(0, .1))
c.slide("c1-eu", c.cue(1, .2), -520, .35, -5)
c.j(f'tl.fromTo("#c1-n",{{opacity:1}},{{opacity:0,duration:.3}},{c.cue(1, .15)});')
c.slide("c1-ma", c.cue(1, .62), 520, .35, 4)
c.draw("c1-rt", c.cue(1, .7), .9)
c.pop("c1-let", c.cue(1, .7), .25)
c.j(f'tl.to("#c1-let",{{motionPath:{{path:"#c1-rt",align:"#c1-rt",alignOrigin:[.5,.5],autoRotate:false}},duration:1.3,ease:"power1.inOut"}},{c.cue(1, .78)});')
c.slide("c1-cou", c.cue(1, .78), -400, 1.3)
C1 = c

# ── c2 숫자 편지 → 어두운 자료실, 200년 ────────────────────────────
c = S("c2")
c.obj("c2-let", "letter_numbers.png", 470, 70, 980, -2)
c.add('<div class="tag" id="c2-tg" style="left:520px;top:880px;opacity:0">재구성 그림 · 실제 편지 아님</div>')
c.add('<div id="c2-dark" style="position:absolute;inset:-40px;background:url(\'assets/img/paper_dark.jpg\') center/cover;opacity:0"></div>')
c.obj("c2-dr", "drawer.png", 560, 300, 800)
c.add('<div id="c2-yr" class="my" style="position:absolute;left:120px;top:110px;font-size:150px;color:#E9E3D6;opacity:0">1809</div>'
      '<div id="c2-yrs" class="pen" style="position:absolute;left:130px;top:280px;font-size:64px;color:#E8B04A;opacity:0">200년 넘게, 아무도</div>')
c.j('tl.fromTo("#c2-let",{opacity:0,scale:1.25,rotation:6},{opacity:1,scale:1,rotation:-2,duration:.55,ease:"power3.out"},.15);')
c.fade("c2-tg", .7)
c.kb("c2-let", .7, 5.0, 1.0, 1.1, 0, -30)
t3 = c.cue(3, 0, -.2)
c.fade("c2-dark", t3, .45)
c.j(f'tl.to("#c2-let,#c2-tg",{{opacity:0,duration:.35}},{t3});')
c.rise("c2-dr", t3 + .3, .6)
c.fade("c2-yr", t3 + .4, .3)
c.j(f'tl.fromTo("#c2-yr",{{textContent:1809}},{{textContent:2026,duration:1.6,ease:"power2.in",snap:{{textContent:1}}}},{t3 + .6});')
c.pop("c2-yrs", t3 + 2.4)
C2 = c

# ── c3 217년 vs 6시간, 사람 ✗ AI ─────────────────────────────────
c = S("c3")
c.obj("c3-hg", "hourglass.png", 820, 170, 300)
c.add(f'<div id="c3-a" class="my" style="position:absolute;left:170px;top:330px;font-size:170px;color:{INK};opacity:0">217년</div>'
      f'<div id="c3-b" style="position:absolute;left:1240px;top:300px;padding:6px 40px;border:12px solid {RED};border-radius:14px;color:{RED};'
      f'font-family:Myeongjo;font-size:150px;transform:rotate(-6deg);opacity:0">6시간</div>'
      f'<div id="c3-p" class="pen" style="position:absolute;left:560px;top:700px;font-size:96px;opacity:0">사람</div>'
      f'<div id="c3-ai" class="pen mk" style="position:absolute;left:1080px;top:700px;font-size:110px;opacity:0;color:{NAVY}">인공지능</div>')
c.add(f'<svg style="position:absolute;left:0;top:0" width="1920" height="1080"><path id="c3-x" d="M540,780 L760,740" stroke="{RED}" stroke-width="10" stroke-linecap="round" fill="none"/></svg>')
c.note("c3-d", 170, 160, "2026년 9월", 72, RED, -4)
c.pop("c3-d", .2)
c.rise("c3-a", c.cue(4, .2), .4)
c.j('tl.fromTo("#c3-hg",{opacity:0,y:-80,rotation:-12},{opacity:1,y:0,rotation:0,duration:.5,ease:"bounce.out"},.45);')
c.stamp("c3-b", c.cue(4, .72))
c.fade("c3-p", c.cue(5, .05), .25)
c.draw("c3-x", c.cue(5, .3), .35)
c.fade("c3-ai", c.cue(5, .5), .2)
c.marker("c3-ai", c.cue(5, .55))
C3 = c

# ── c4 처치 · 경험 없음 · 흐린 복사본 ────────────────────────────
c = S("c4")
c.obj("c4-lp", "laptop_person.png", 230, 220, 760)
c.note("c4-n1", 1080, 220, "카터 처치 · 27세 · 보안 엔지니어", 50, rot=-2)
c.note("c4-n2", 1120, 380, "암호 해독: 거의 배운 적 없음", 50, RED, 3, "#FFFFFF")
c.add('<div id="c4-cp" style="position:absolute;left:1060px;top:520px;width:600px;opacity:0;filter:grayscale(1) blur(2.2px) contrast(.8);'
      'transform:rotate(3deg);box-shadow:0 12px 22px rgba(30,24,16,.3)"><img src="assets/gen/letter_numbers.png" style="width:600px;background:#EEE"></div>'
      '<div class="tag" id="c4-tg" style="left:1080px;top:930px;opacity:0">흐린 복사본 · 재구성 그림</div>')
c.add(f'<div id="c4-ai" class="note" style="left:1230px;top:470px;font-size:42px;font-family:NotoKR;font-weight:800;background:{NAVY};color:#fff;opacity:0">GPT-6 아스트라</div>')
c.j('tl.fromTo("#c4-lp",{opacity:0,y:60},{opacity:1,y:0,duration:.6,ease:"power2.out"},.15);')
c.pop("c4-n1", c.cue(6, .62))
c.slide("c4-n2", c.cue(7, .1), 400, .35, 3)
c.j(f'tl.to("#c4-n1,#c4-n2",{{opacity:0,y:-30,duration:.3}},{c.cue(8, 0, -.1)});')
c.pop("c4-ai", c.cue(8, .25))
c.j(f'tl.fromTo("#c4-cp",{{opacity:0,y:200,rotation:12}},{{opacity:1,y:0,rotation:3,duration:.5,ease:"power3.out"}},{c.cue(8, .55)});')
c.fade("c4-tg", c.cue(8, .65))
C4 = c

# ── c5 작업대: 옮겨 적기 · 분석 · 코드 · 대조 (네 가지 다른 움직임) ─────
c = S("c5")
D9 = L[9]["dur"]
c.obj("c5-let", "letter_numbers.png", 120, 150, 720, -2)
c.add(f'<div id="c5-scan" style="position:absolute;left:140px;top:160px;width:700px;height:10px;background:rgba(80,170,255,.75);'
      f'box-shadow:0 0 22px rgba(80,170,255,.9);opacity:0"></div>'
      f'<div id="c5-tr" class="pol" style="left:890px;top:130px;width:480px;opacity:0;font-family:JetBrains Mono,monospace;font-size:38px;line-height:1.5;color:{INK}">'
      f'<div id="c5-r1">738 104 592 417</div><div id="c5-r2">860 203 975 681</div><div id="c5-r3">309 746 518 264</div></div>'
      f'<div id="c5-fq" style="position:absolute;left:1400px;top:150px;width:400px;height:260px;opacity:0">'
      + "".join(f'<div class="fb" style="position:absolute;left:{k * 48}px;bottom:0;width:34px;height:{h}px;background:{NAVY};transform-origin:50% 100%"></div>' for k, h in enumerate([210, 120, 180, 90, 150, 60, 110, 70]))
      + f'</div><div id="c5-code" style="position:absolute;left:920px;top:520px;width:560px;height:300px;background:#20242B;border-radius:10px;opacity:0;overflow:hidden;'
      f'box-shadow:0 14px 24px rgba(0,0,0,.35)"><div id="c5-cl" style="position:absolute;left:20px;top:16px;font-family:JetBrains Mono,monospace;font-size:22px;line-height:1.5;color:#C9D1D9">'
      + "<br>".join(["for key in candidates:", "  text = decode(cipher, key)", "  score = french_words(text)", "  if score > best: best = key"] * 4)
      + f'</div><div style="position:absolute;right:10px;bottom:6px;font-size:18px;color:#8A9099">예시 화면</div></div>')
c.polaroid("c5-mp", "map1809.jpg", 1520, 520, 320, "당시 기록과 대조", 5)
c.add(f'<div id="c5-ok" style="position:absolute;left:1700px;top:470px;font-size:120px;color:#2E7D4F;font-weight:900;opacity:0">✓</div>')
c.j('tl.fromTo("#c5-let",{opacity:0,x:-300},{opacity:1,x:0,duration:.45,ease:"power3.out"},.1);')
t1 = c.cue(9, .02)
c.fade("c5-scan", t1, .15)
c.j(f'tl.fromTo("#c5-scan",{{y:0}},{{y:560,duration:1.1,ease:"none"}},{t1});')
c.j(f'tl.to("#c5-scan",{{opacity:0,duration:.2}},{t1 + 1.1});')
c.slide("c5-tr", t1 + .4, 300, .35)
for k in range(3):
    c.j(f'tl.from("#c5-r{k+1}",{{scrambleText:{{text:"",chars:"0123456789",speed:.6}},duration:.5}},{t1 + .5 + k * .3:.2f});')
t2 = c.cue(9, .3)
c.fade("c5-fq", t2, .2)
c.j(f'tl.fromTo("#c5-fq .fb",{{scaleY:0}},{{scaleY:1,duration:.35,ease:"back.out(1.6)",stagger:.06}},{t2});')
t3 = c.cue(9, .52)
c.pop("c5-code", t3, .3)
c.j(f'tl.fromTo("#c5-cl",{{y:0}},{{y:-260,duration:{D9 * .45:.2f},ease:"none"}},{t3 + .3});')
t4 = c.cue(9, .8)
c.slide("c5-mp", t4, 400, .35, 5)
c.stamp("c5-ok", t4 + .55)
C5 = c

# ── c6 숫자가 문장으로 · 지도 위 8만 ─────────────────────────────
c = S("c6")
c.obj("c6-let", "letter_numbers.png", 200, 90, 860, -1)
c.add(f'<div id="c6-ov" style="position:absolute;left:230px;top:300px;width:880px;padding:24px 30px;background:rgba(251,249,244,.93);'
      f'box-shadow:0 10px 20px rgba(30,24,16,.25);opacity:0;font-family:Myeongjo;font-size:44px;line-height:1.5;white-space:nowrap;color:{INK}">'
      f'<span id="c6-t1">738 104 592 417 860 203</span><br><span id="c6-t2">975 681 309 746 518</span></div>'
      f'<div class="tag" id="c6-tg" style="left:260px;top:880px;opacity:0">해독문(한국어 번역) · 유로뉴스 인용 기준</div>')
c.add('<div id="c6-map" style="position:absolute;left:1140px;top:200px;width:660px;height:520px;overflow:hidden;opacity:0;box-shadow:0 14px 26px rgba(30,24,16,.3);transform:rotate(2deg)">'
      '<img src="assets/img/map1809.jpg" style="width:900px;margin-left:-160px;margin-top:-40px"></div>')
c.add(f'<svg style="position:absolute;left:0;top:0" width="1920" height="1080"><path id="c6-ar" d="M1870,150 C 1800,260 1760,330 1700,400" fill="none" stroke="{RED}" stroke-width="9" stroke-linecap="round"/>'
      f'<circle id="c6-fr" cx="1690" cy="410" r="26" fill="none" stroke="{RED}" stroke-width="7"/></svg>'
      f'<div id="c6-ru" class="pen" style="position:absolute;left:1560px;top:80px;font-size:46px;color:{RED};opacity:0">러시아군 →</div>'
      f'<div id="c6-cnt" class="my" style="position:absolute;left:1330px;top:760px;font-size:96px;color:{RED};opacity:0"><span id="c6-cv">0</span>명</div>'
      f'<div id="c6-fl" class="pen" style="position:absolute;left:1350px;top:880px;font-size:44px;opacity:0">프리울리의 군대</div>')
c.j('tl.fromTo("#c6-let",{opacity:0},{opacity:1,duration:.3},.05);')
c.pop("c6-ov", c.cue(10, .2), .3)
c.j(f'tl.to("#c6-t1",{{scrambleText:{{text:"러시아군이 오스트리아를 향해 진군 중",chars:"0123456789",speed:.4}},duration:1.2}},{c.cue(10, .45)});')
c.j(f'tl.to("#c6-t2",{{scrambleText:{{text:"프리울리의 군대는 오늘 8만 명",chars:"0123456789",speed:.4}},duration:1.2}},{c.cue(10, .7)});')
c.fade("c6-tg", c.cue(10, .9))
c.slide("c6-map", c.cue(11, .05), 500, .4, 2)
c.draw("c6-ar", c.cue(11, .15), .7)
c.pop("c6-ru", c.cue(11, .15))
c.draw("c6-fr", c.cue(11, .6), .4)
c.fade("c6-cnt", c.cue(11, .62), .2)
c.fade("c6-fl", c.cue(11, .62), .2)
c.j(f'const cv={{v:0}};tl.fromTo(cv,{{v:0}},{{v:80000,duration:1.0,ease:"power2.out",'
    f'onUpdate:function(){{document.getElementById("c6-cv").textContent=(Math.round(cv.v/1000)*1000).toLocaleString("en-US")}}}},{c.cue(11, .64)});')
C6 = c

SCENES = [C1, C2, C3, C4, C5, C6]
for s in SCENES:
    (HERE / "compositions" / f"{s.sid}.html").write_text(s.html(), encoding="utf-8")
caps = "".join(f'<div class="clip cap" id="cap{x["i"]}" data-start="{x["start"] + .05:.2f}" data-duration="{x["dur"] - .3:.2f}" data-track-index="20"><span>{x["text"]}</span></div>' for x in L)
aud = "".join(f'<audio id="vo{x["i"]}" class="clip" src="assets/vo/{x["file"]}" data-start="{x["start"]}" data-duration="{x["dur"]}" data-track-index="7" data-volume="1"></audio>' for x in L)
SFX = [("whoosh-short", "c1", 1, .2), ("pop", "c1", 1, .62), ("whoosh", "c1", 1, .78), ("whoosh-short", "c2", 2, 0), ("riser", "c2", 3, .1),
       ("click", "c3", 4, .45), ("impact-bass-2", "c3", 4, .72), ("pencil", "c3", 5, .3), ("pop", "c4", 6, .62), ("whoosh-short", "c4", 8, .55),
       ("typing", "c5", 9, .05), ("pop", "c5", 9, .52), ("click", "c5", 9, .9), ("typing", "c6", 10, .45), ("pencil", "c6", 11, .15)]
import subprocess
def _d(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(HERE / f)], capture_output=True, text=True).stdout)
for k, (n, sid, i, fr) in enumerate(SFX):
    f = f"assets/sfx/{n}.{'wav' if n == 'pencil' else 'mp3'}"
    tt = round(L[i]["start"] + L[i]["dur"] * fr, 2)
    aud += f'<audio id="sx{k}" class="clip" src="{f}" data-start="{tt}" data-duration="{min(1.2, _d(f)):.2f}" data-track-index="{8 + k % 3}" data-volume="{0.2 if n in ("pencil", "typing") else 0.35}"></audio>'
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
