"""시범작 ② 샘플 — 2장 인터폰 실험(시청자가 참가자) + 5장 감시카메라 219건 (D3 확인용, 초안 목소리 edge-tts).

    python build.py <작업 폴더(E:/ytflow-local/hf-pilot-psych)>

그림 언어 하나: 위에서 본 배치도 — 사람은 점, 방은 칸, 소리는 물결. 실험(듣는 중)은 어두운 바탕, 결과(재는 중)는 종이 바탕.
점들이 대사의 동사를 연기한다(다가간다·막아선다·끌어낸다·두드린다). 사건·다툼은 실루엣 없이 점으로만 — 폭력 묘사 없음.
템포: 2장은 느리게(−6%)·질문 뒤 긴 침묵, 5장 재구성 장면은 빠르게(+2%)·'열 건 중 아홉' 앞뒤 긴 쉼.
"""
import json, random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "scripts" / "anim"))
import hflib as H
from hflib import INK, RED, GRN, YEL, NAVY, BLU, LIGHT

WORK = Path(sys.argv[1])
L = json.load(open(WORK / "assets/vo/lines.json", encoding="utf-8"))
GRY = "#8A909C"
PLAN = [("p1", 0, 1), ("p2", 4, 1), ("p3", 8, 0), ("p4", 12, 1), ("p5", 15, 1), ("p6", 23, 0),
        ("p7", 25, 1), ("p8", 28, 0), ("p9", 30, 0)]
H.setup(L, PLAN)
sc = H.scene
CX, CY = 960, 470
ROOMS = [(560, 200), (1360, 200), (560, 740), (1360, 740)]   # 다른 참가자 방 4개 (가운데가 '나')


def rooms(c, pre, dim=False):
    s = "".join(f'<path id="{pre}-w{k}" d="M{CX},{CY} L{x},{y}" stroke="{GRY}" stroke-width="4" stroke-dasharray="10 10"/>' for k, (x, y) in enumerate(ROOMS))
    s += f'<rect id="{pre}-me" x="{CX - 170}" y="{CY - 130}" width="340" height="260" rx="10" fill="#2C3442" stroke="{LIGHT}" stroke-width="6"/>'
    s += f'<circle id="{pre}-you" cx="{CX}" cy="{CY + 10}" r="26" fill="{YEL}"/>'
    s += f'<path id="{pre}-hp" d="M{CX - 40},{CY + 5} A40,40 0 0 1 {CX + 40},{CY + 5}" fill="none" stroke="{YEL}" stroke-width="8"/>'
    for k, (x, y) in enumerate(ROOMS):
        s += (f'<rect id="{pre}-r{k}" x="{x - 110}" y="{y - 80}" width="220" height="160" rx="10" fill="#232A36" stroke="{GRY}" stroke-width="5"/>'
              f'<circle id="{pre}-o{k}" cx="{x}" cy="{y}" r="20" fill="{GRY}"/>')
    c.svg(s)


# ═══ p1 작은 방, 헤드폰, 인터폰 — 얼굴은 볼 수 없다 ═══
c = sc("p1")
rooms(c, "p1")
you = c.text(CX - 40, CY + 50, "여러분", 40, YEL, "sans")
lab = c.text(140, 70, "1968년 · 뉴욕의 한 대학 실험실 (재구성)", 34, GRY, "sans", "font-weight:500")
see = c.text(0, 880, "", 10)
walls = c.uid("wl")
c.svg(f'<g id="{walls}">' + "".join(f'<rect x="{x - 110}" y="{y - 80}" width="220" height="160" rx="10" fill="#1A1F28"/>' for x, y in ROOMS) + '</g>')
qms = [c.text(x - 14, y - 40, "?", 64, GRY, "sans") for x, y in ROOMS]
c.fade(lab, .2)
c.j(f'tl.fromTo("#p1-me",{{opacity:0,scale:.6,transformOrigin:"{CX}px {CY}px"}},{{opacity:1,scale:1,duration:.4,ease:"back.out(1.8)"}},{c.cue(0, .4)});')
c.pop("p1-you", c.cue(0, .6)); c.fade(you, c.cue(0, .65))
c.draw("p1-hp", c.cue(1, .55), .35)
for k in range(4):
    c.draw(f"p1-w{k}", c.cue(2, .3 + k * .08), .4)
    c.j(f'tl.fromTo("#p1-r{k},#p1-o{k}",{{opacity:0}},{{opacity:1,duration:.3}},{c.cue(2, .4 + k * .08):.2f});')
c.j(f'tl.set("#{walls}",{{opacity:0}},0);tl.to("#{walls}",{{opacity:1,duration:.5}},{c.cue(3, .3)});')
for k, q in enumerate(qms):
    c.pop(q, c.cue(3, .45 + k * .05))

# ═══ p2 목소리가 이상해진다 — 도와 달라 — 알리겠습니까? (긴 침묵) ═══
c = sc("p2")
rooms(c, "p2")
x0, y0 = ROOMS[1]
wv = c.uid("wv")
c.svg(f'<path id="{wv}" d="M{x0 - 100},{y0} q25,-30 50,0 t50,0 t50,0 t50,0" fill="none" stroke="{BLU}" stroke-width="7"/>')
wr = c.uid("wr")
c.svg(f'<path id="{wr}" d="M{x0 - 100},{y0} l20,-60 l20,110 l20,-120 l20,90 l20,-70 l20,100 l20,-80 l20,60 l20,-30" fill="none" stroke="{RED}" stroke-width="7" opacity="0"/>')
help_ = c.text(x0 - 120, y0 + 100, "“도와 줘요…”", 46, RED, "pen")
door = c.uid("dr")
c.svg(f'<rect id="{door}" x="{CX + 150}" y="{CY - 50}" width="22" height="100" rx="4" fill="{YEL}" opacity="0"/>')
q = c.text(0, 820, "여러분이라면?", 80, LIGHT, "my", center=True)
c.j(f'tl.set("#p2-r0,#p2-r1,#p2-r2,#p2-r3,#p2-o0,#p2-o1,#p2-o2,#p2-o3,#p2-w0,#p2-w1,#p2-w2,#p2-w3",{{opacity:.9}},0);')
c.draw(wv, c.cue(4, .15), .5)
c.j(f'tl.to("#{wv}",{{opacity:0,duration:.2}},{c.cue(4, .7)});tl.to("#{wr}",{{opacity:1,duration:.15}},{c.cue(4, .7)});')
c.shake(wr, c.cue(5, .1), 8, 6); c.blink("p2-o1", c.cue(5, .2), 4, .15)
c.rise(help_, c.cue(6, .25))
c.j(f'tl.fromTo("#{door}",{{opacity:0}},{{opacity:1,duration:.3}},{c.cue(7, .2)});')
c.j(f'tl.fromTo("#{door}",{{opacity:1}},{{opacity:.25,duration:.6,repeat:3,yoyo:true}},{c.cue(7, .9)});')
c.rise(q, c.cue(7, .15))
c.j(f'tl.to("#p2-you",{{x:60,duration:1.2,ease:"sine.inOut",yoyo:true,repeat:1}},{c.cue(7, .95)});')

# ═══ p3 결과 — 혼자 85% · 한 명 더 62% · 네 명 더 31% (종이 바탕, 재는 중) ═══
c = sc("p3")
hd = c.text(0, 90, "‘나 말고 몇 명이 듣고 있다’고 믿었나", 56, INK, "my", center=True)
rows = [(1, 85, 9), (2, 62, 10), (5, 31, 11)]
for r, (n, v, li) in enumerate(rows):
    y = 270 + r * 210
    dots = "".join(f'<circle cx="{220 + k * 62}" cy="{y}" r="24" fill="{YEL if k == 0 else GRY}"/>' for k in range(n))
    c.svg(f'<g id="p3-d{r}">{dots}</g><rect id="p3-b{r}" x="600" y="{y - 45}" width="{v * 11}" height="90" rx="8" fill="{NAVY}"/>')
    lab = c.text(220, y + 40, ["혼자", "+1명", "+4명"][r], 38, INK, "sans")
    val = c.text(620 + v * 11, y - 52, "0", 84, NAVY, "sans")
    t = c.cue(li, .55 if r == 0 else .6)
    c.j(f'tl.fromTo("#p3-d{r}",{{opacity:0,x:-40}},{{opacity:1,x:0,duration:.3}},{c.cue(li, .05)});'); c.fade(lab, c.cue(li, .05))
    c.j(f'tl.fromTo("#p3-b{r}",{{scaleX:0,transformOrigin:"0% 50%"}},{{scaleX:1,duration:.7,ease:"power2.out"}},{t});')
    c.fade(val, t, .1); c.count(val, t, 0, v, .7, False)
c.fade(hd, c.cue(8, .2))
src = c.text(1250, 880, "달리·라타네, 1968 (2차 자료 기준 — 원 논문 확인 중)", 26, GRY, "sans", "font-weight:500")
c.fade(src, c.cue(9, .3))

# ═══ p4 반전 — 다른 목소리는 녹음이었다, 방엔 여러분 한 명 ═══
c = sc("p4")
rooms(c, "p4")
tapes = []
for k, (x, y) in enumerate(ROOMS):
    i = c.uid("tp")
    c.svg(f'<g id="{i}" opacity="0"><rect x="{x - 60}" y="{y - 34}" width="120" height="68" rx="8" fill="none" stroke="{RED}" stroke-width="5"/>'
          f'<circle cx="{x - 25}" cy="{y}" r="14" fill="none" stroke="{RED}" stroke-width="5"/><circle cx="{x + 25}" cy="{y}" r="14" fill="none" stroke="{RED}" stroke-width="5"/></g>')
    tapes.append(i)
rec = c.tag(CX - 100, 60, "미리 녹음된 목소리", RED, size=40)
one = c.text(0, 860, "그 방에 있던 사람은 여러분 한 명", 64, YEL, "my", center=True)
bel = c.text(0, 860, "‘누군가 듣고 있다’는 믿음만으로", 64, LIGHT, "my", center=True)
for k in range(4):
    t = c.cue(12, .45 + k * .06)
    c.j(f'tl.to("#p4-o{k}",{{opacity:0,duration:.2}},{t:.2f});'); c.fade(tapes[k], t)
c.pop(rec, c.cue(12, .5))
c.j(f'tl.to("#p4-r0,#p4-r1,#p4-r2,#p4-r3,#p4-w0,#p4-w1,#p4-w2,#p4-w3,{",".join("#" + x for x in tapes)}",{{opacity:.12,duration:.6}},{c.cue(13, .1)});')
c.j(f'tl.fromTo("#p4-me",{{scale:1,transformOrigin:"{CX}px {CY}px"}},{{scale:1.12,duration:.6}},{c.cue(13, .1)});')
c.rise(one, c.cue(13, .3)); c.out([rec], c.cue(13, .2))
c.out([one], c.cue(14, .0), .3); c.rise(bel, c.cue(14, .1))
c.j(f'tl.to("#p4-r0,#p4-r1,#p4-r2,#p4-r3",{{opacity:.55,strokeDasharray:"12 10",duration:.6}},{c.cue(14, .4)});')

# ═══ p5 감시 화면 하나 (재구성) — 점들이 동작을 연기 ═══
c = sc("p5")
c.svg(f'<rect x="150" y="70" width="1620" height="800" rx="14" fill="#141820" stroke="#3A4252" stroke-width="10"/>'
      f'<path d="M150,640 L1770,640" stroke="#2C3442" stroke-width="4"/>'
      f'<circle id="p5-rec" cx="210" cy="130" r="14" fill="{RED}"/>')
cam = c.text(240, 108, "CAM 03 · 금요일 밤 · 재구성", 34, "#9AA0AA", "sans", "font-weight:500")
A, B = (880, 520), (1040, 520)
BY = [(520, 470), (640, 600), (1380, 460), (1500, 590), (760, 360), (1260, 350), (400, 590), (1620, 400)]
s = f'<circle id="p5-A" cx="{A[0]}" cy="{A[1]}" r="30" fill="{RED}"/><circle id="p5-B" cx="{B[0]}" cy="{B[1]}" r="30" fill="#E07A5F"/>'
s += "".join(f'<circle id="p5-y{k}" cx="{x}" cy="{y}" r="24" fill="{GRY}"/>' for k, (x, y) in enumerate(BY))
c.svg(s)
c.blink("p5-rec", .1, 20, .5)
c.fade(cam, .1)
c.j(f'tl.fromTo("#p5-A,#p5-B",{{opacity:0}},{{opacity:1,duration:.3}},{c.cue(16, .1)});')
c.j(f'tl.fromTo("[id^=p5-y]",{{opacity:0}},{{opacity:1,duration:.3,stagger:.05}},{c.cue(16, .3)});')
t = c.cue(17, .55); c.j(f'tl.to("#p5-A",{{x:70,duration:.15}},{t});'); c.shake("p5-B", t + .15, 6, 8)
l1 = c.text(470, 380, "✋ 진정", 40, YEL, "sans")
c.j(f'tl.to("#p5-y0",{{x:260,y:30,duration:.6,ease:"power2.out"}},{c.cue(18, .5)});tl.to("#p5-y0",{{fill:"{YEL}",duration:.2}},{c.cue(18, .5)});'); c.pop(l1, c.cue(19, .05))
l2 = c.text(900, 650, "막아서기", 40, YEL, "sans")
c.j(f'tl.to("#p5-y5",{{x:-260,y:170,duration:.5,ease:"power3.out"}},{c.cue(20, .45)});tl.to("#p5-y5",{{fill:"{YEL}",duration:.2}},{c.cue(20, .45)});')
c.j(f'tl.to("#p5-B",{{x:40,duration:.3}},{c.cue(20, .7)});'); c.pop(l2, c.cue(20, .75))
l3 = c.text(560, 650, "떼어 놓기", 40, YEL, "sans")
c.j(f'tl.to("#p5-y4",{{x:80,y:150,duration:.4}},{c.cue(21, .3)});tl.to("#p5-y4",{{fill:"{YEL}",duration:.2}},{c.cue(21, .3)});')
c.j(f'tl.to("#p5-A,#p5-y4",{{x:"-=220",duration:.7,ease:"power2.inOut"}},{c.cue(21, .65)});'); c.pop(l3, c.cue(21, .7))
l4 = c.text(1150, 650, "챙기기", 40, YEL, "sans")
c.j(f'tl.to("#p5-y2",{{x:-260,y:80,duration:.5}},{c.cue(22, .3)});tl.to("#p5-y2",{{fill:"{YEL}",duration:.2}},{c.cue(22, .3)});')
rg = c.uid("rg"); c.svg(f'<circle id="{rg}" cx="{B[0] + 40}" cy="{B[1]}" r="40" fill="none" stroke="{YEL}" stroke-width="5" opacity="0"/>')
c.ring(rg, c.cue(22, .75), 2, .8, 2.2); c.pop(l4, c.cue(22, .7))

# ═══ p6 연구팀이 센 행동들 ═══
c = sc("p6")
hd = c.text(0, 150, "연구팀이 ‘도움’으로 센 행동", 60, INK, "my", center=True)
acts = ["진정시키는 손짓", "막아서기", "떼어 놓기", "다친 사람 챙기기"]
ids = [c.tag(180 + k * 410, 420, a, NAVY, size=44) for k, a in enumerate(acts)]
cnt = c.text(0, 640, "219건, 하나하나", 70, RED, "sans", center=True)
c.fade(hd, c.cue(23, .02))
for k, i in enumerate(ids):
    c.pop(i, c.cue(23, .1 + k * .22))
c.rise(cnt, c.cue(24, .5))

# ═══ p7 열 건 중 아홉 (긴 쉼 동안 화면이 하나씩 켜짐) ═══
c = sc("p7")
grid = ""
for k in range(10):
    x, y = 210 + (k % 5) * 310, 170 + (k // 5) * 330
    grid += (f'<rect x="{x}" y="{y}" width="270" height="200" rx="10" fill="#141820" stroke="#3A4252" stroke-width="6"/>'
             f'<circle cx="{x + 110}" cy="{y + 110}" r="16" fill="{RED}"/><circle cx="{x + 160}" cy="{y + 110}" r="16" fill="#E07A5F"/>'
             f'<circle id="p7-h{k}" cx="{x + 135}" cy="{y + 60}" r="15" fill="{YEL}" opacity="0"/>'
             f'<rect id="p7-f{k}" x="{x}" y="{y}" width="270" height="200" rx="10" fill="none" stroke="{GRN if k != 6 else RED}" stroke-width="8" opacity="0"/>')
c.svg(grid)
big = c.text(0, 760, "열 건 중 아홉", 96, YEL, "my", center=True)
order = [0, 1, 2, 3, 4, 5, 7, 8, 9]
t0 = c.cue(24, .9)
for n, k in enumerate(order):
    tt = t0 + n * .17
    c.j(f'tl.fromTo("#p7-h{k}",{{opacity:0,y:-30}},{{opacity:1,y:0,duration:.25}},{tt:.2f});tl.to("#p7-f{k}",{{opacity:1,duration:.15}},{tt + .1:.2f});')
c.j(f'tl.to("#p7-f6",{{opacity:.8,duration:.2}},{t0 + 1.7:.2f});')
c.stamp(big, c.cue(26, .1))

# ═══ p8 세 도시 — 비슷했다 ═══
c = sc("p8")
cities = [("랭커스터", "영국"), ("암스테르담", "네덜란드"), ("케이프타운", "남아공")]
for k, (nm, ct) in enumerate(cities):
    x = 330 + k * 470
    c.svg(f'<rect id="p8-b{k}" x="{x}" y="{700 - 380}" width="200" height="380" rx="10" fill="{NAVY}"/>')
    t1 = c.text(x - 60, 720, nm, 48, INK, "sans", "width:320px;text-align:center")
    t2 = c.text(x - 60, 790, ct, 34, GRY, "sans", "width:320px;text-align:center")
    tt = c.cue(28, .2 + k * .15)
    c.j(f'tl.fromTo("#p8-b{k}",{{scaleY:0,transformOrigin:"50% 100%"}},{{scaleY:1,duration:.5}},{tt:.2f});'); c.fade(t1, tt); c.fade(t2, tt)
note = c.tag(1290, 200, "체감 치안이 훨씬 낮은 곳", RED, size=34)
c.pop(note, c.cue(29, .2))
eq = c.text(0, 120, "나서는 비율: 크게 다르지 않았다", 54, INK, "my", center=True)
for k in range(2):
    ap = c.text(620 + k * 470, 420, "≈", 110, INK, "sans"); c.fade(ap, c.cue(29, .8))
nt = c.text(1180, 870, "막대 높이는 ‘비슷함’을 나타낸 그림 — 실제 비율 아님", 26, GRY, "sans", "font-weight:500"); c.fade(nt, c.cue(28, .4))
c.rise(eq, c.cue(29, .75))

# ═══ p9 구경꾼이 많을수록 — 줄어든 게 아니라 오히려 늘었다 ═══
c = sc("p9")
c.svg(f'<path d="M260,180 L260,760 L1700,760" fill="none" stroke="{INK}" stroke-width="5"/>'
      f'<path id="p9-exp" d="M300,280 C700,420 1100,600 1650,700" fill="none" stroke="{GRY}" stroke-width="8" stroke-dasharray="18 14"/>'
      f'<path id="p9-x" d="M900,420 L1050,580 M1050,420 L900,580" stroke="{RED}" stroke-width="12" stroke-linecap="round"/>'
      f'<path id="p9-real" d="M300,560 C700,480 1100,380 1650,250" fill="none" stroke="{GRN}" stroke-width="12" stroke-linecap="round"/>')
yl = c.text(280, 120, "누군가 도와줄 가능성", 44, INK, "sans")
xl = c.text(1380, 780, "구경꾼 수 →", 44, INK, "sans")
el = c.text(1250, 640, "흔히 생각한 모습", 36, GRY, "sans")
rl = c.text(1300, 170, "실제: 오히려 늘었다", 50, GRN, "sans")
pdots = "".join(f'<circle class="pp" cx="{320 + k * 45}" cy="790" r="12" fill="{GRY}" opacity="0"/>' for k in range(30))
c.svg(f'<g id="p9-pp">{pdots}</g>')
c.fade(yl, c.cue(30, .2)); c.fade(xl, c.cue(30, .3))
nt = c.text(280, 830, "선은 방향만 나타낸 그림 — 논문: 구경꾼 1명 늘 때마다 도움받을 오즈 1.1배", 26, GRY, "sans", "font-weight:500"); c.fade(nt, c.cue(32, .3))
c.j(f'tl.to("#p9-pp .pp",{{opacity:1,duration:.05,stagger:.08}},{c.cue(30, .3)});')
c.draw("p9-exp", c.cue(31, .1), 1.0); c.fade(el, c.cue(31, .5))
c.j(f'tl.set("#p9-x",{{opacity:0}},0);tl.set("#p9-x",{{opacity:1}},{c.cue(31, .95)});'); c.draw("p9-x", c.cue(31, .95), .25)
c.draw("p9-real", c.cue(32, .05), .9, "power2.out"); c.rise(rl, c.cue(32, .3))
c.j(f'tl.to("#p9-exp,#{el}",{{opacity:.25,duration:.4}},{c.cue(32, .6)});')
c.j(f'tl.fromTo("#p9-real",{{strokeWidth:12}},{{strokeWidth:18,duration:.4,yoyo:true,repeat:1}},{c.cue(33, .6)});')

SFX = [("click-soft", 0, .6), ("whoosh-short", 2, .4), ("click", 3, .3), ("riser", 6, .1), ("pop", 9, .55), ("pop", 10, .6), ("pop", 11, .6),
       ("impact-bass-2", 12, .5), ("click-soft", 18, .5), ("whoosh-short", 20, .45), ("whoosh-short", 21, .65), ("chime", 22, .75),
       ("pop", 23, .1), ("pop", 23, .32), ("pop", 23, .54), ("pop", 23, .76), ("impact-bass-2", 26, .1), ("chime", 32, .3)]
H.write(WORK, SFX)
