"""시범작 ① 샘플 — 0장 여는 장면 + 3장 '정확한 0'·계산 (D3 확인용, 초안 목소리 edge-tts).

    python build.py <작업 폴더(E:/ytflow-local/hf-pilot-ai)>

그림 언어 하나: 종이 바탕 위 '시간 · 일 · 돈' 세 칸 기준판. 숫자는 말하는 순간 생기고(카운트·막대·점 격자), 질문 마디만 어두운 바탕.
템포: lines.json 의 pause(대본의 (쉼)·(긴 쉼))가 시간선에 들어감 — 쉬는 동안 화면은 방금 말한 결과를 보여 줌.
"""
import json, random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "scripts" / "anim"))
import hflib as H
from hflib import INK, RED, GRN, YEL, NAVY, BLU, LIGHT

WORK = Path(sys.argv[1])
L = json.load(open(WORK / "assets/vo/lines.json", encoding="utf-8"))
GRY, GOLD = "#9AA0AA", "#C9962B"
PLAN = [("s1", 0, 0), ("s2", 4, 0), ("s3", 8, 1), ("s4", 10, 0), ("s5", 13, 0), ("s6", 16, 0),
        ("s7", 21, 0), ("s8", 25, 0), ("s9", 28, 0)]
H.setup(L, PLAN)
sc = H.scene


def box(c, x, y, w, h, label, col, sid, size=64):
    c.svg(f'<rect id="{sid}" x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="#FBF9F4" stroke="{col}" stroke-width="8"/>')
    t = c.text(x, y + h / 2 - size * .7, label, size, col, "sans", f"width:{w}px;text-align:center")
    return t


# ═══ s1 금요일 오후 — 회의록 세 개가 AI 창으로, 2시간 → 15분 ═══
c = sc("s1")
c.svg(f'<path id="s1-desk" d="M260,760 L1660,760" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
      f'<rect id="s1-lap" x="760" y="450" width="520" height="310" rx="16" fill="#2C313B"/>'
      f'<rect id="s1-scr" x="785" y="475" width="470" height="250" rx="8" fill="#F6F1E6"/>'
      f'<circle id="s1-clk" cx="1520" cy="330" r="150" fill="#FBF9F4" stroke="{INK}" stroke-width="8"/>'
      f'<path id="s1-arc2" d="M1520,180 A150,150 0 0 1 1650,405" fill="none" stroke="{GRY}" stroke-width="26" stroke-opacity=".55"/>'
      f'<path id="s1-arc15" d="M1520,180 A150,150 0 0 1 1626,224" fill="none" stroke="{RED}" stroke-width="26"/>'
      f'<path id="s1-hand" d="M1520,330 L1520,215" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>')
t0 = c.text(300, 170, "금요일 오후 4:00", 76, INK, "sans")
ai = c.text(785, 560, "AI", 92, NAVY, "sans", "width:470px;text-align:center")
docs = []
for k in range(3):
    i = c.uid("d")
    c.add(f'<div id="{i}" style="position:absolute;left:{280 + k * 130}px;top:{430 + k * 30}px;width:150px;height:190px;background:#fff;border:5px solid {INK};border-radius:8px;opacity:0;box-shadow:0 8px 16px rgba(0,0,0,.15)">'
          f'<div style="margin:22px 18px;height:10px;background:{GRY}"></div><div style="margin:14px 18px;height:10px;background:{GRY}"></div><div style="margin:14px 18px;width:70px;height:10px;background:{GRY}"></div>'
          f'<div style="position:absolute;bottom:10px;width:100%;text-align:center;font-size:26px;font-weight:700;color:{INK}">회의록</div></div>')
    docs.append(i)
l2h = c.text(1320, 520, "두 시간", 54, GRY, "sans")
l15 = c.text(1320, 600, "→ 15분", 72, RED, "sans")
lout = c.tag(820, 800, "18:00 정시 퇴근", GRN, size=48)
rec = c.text(300, 860, "재구성 장면", 28, GRY, "sans", "font-weight:500")
c.fade("s1-desk", .1, .3); c.rise(t0, .15); c.fade(rec, .3)
c.j('tl.fromTo("#s1-lap,#s1-scr",{opacity:0,y:40},{opacity:1,y:0,duration:.4,ease:"power3.out"},.25);'); c.fade(ai, .4)
for k, d in enumerate(docs):
    c.pop(d, c.cue(1, .3 + k * .08))
tfly = c.cue(1, .75)
for k, d in enumerate(docs):
    c.j(f'tl.to("#{d}",{{x:{560 - k * 130},y:{60 - k * 30},scale:.25,opacity:0,duration:.45,ease:"power2.in"}},{tfly + k * .1:.2f});')
c.j(f'tl.fromTo("#{ai}",{{scale:1}},{{scale:1.18,duration:.18,yoyo:true,repeat:1,transformOrigin:"50% 50%"}},{tfly + .45:.2f});')
c.j(f'tl.fromTo("#s1-clk,#s1-hand",{{opacity:0,scale:.6,transformOrigin:"1520px 330px"}},{{opacity:1,scale:1,duration:.35,ease:"back.out(2)"}},{c.cue(2, .0)});')
c.draw("s1-arc2", c.cue(2, .15), .6); c.fade(l2h, c.cue(2, .2))
c.j('tl.set("#s1-arc15",{opacity:0},0);')
c.j(f'tl.to("#s1-arc2",{{opacity:.15,duration:.3}},{c.cue(2, .6)});tl.set("#s1-arc15",{{opacity:1}},{c.cue(2, .6)});')
c.draw("s1-arc15", c.cue(2, .6), .35); c.pop(l15, c.cue(2, .62))
c.j(f'tl.fromTo("#s1-hand",{{rotation:0,transformOrigin:"50% 100%"}},{{rotation:45,duration:.35}},{c.cue(2, .6)});')
c.stamp(lout, c.cue(3, .45))

# ═══ s2 세 명 중 두 명 66.5% · 1년 전 51.8% · 시간 9.2% 줄었다 ═══
c = sc("s2")
ppl = ""
for k in range(3):
    x = 330 + k * 200
    col = NAVY if k < 2 else GRY
    ppl += (f'<g id="s2-p{k}"><circle cx="{x}" cy="300" r="56" fill="{col}"/>'
            f'<path d="M{x - 80},520 Q{x},360 {x + 80},520 Z" fill="{col}"/></g>')
c.svg(ppl)
n665 = c.text(260, 560, "0", 150, NAVY, "sans")
pct = c.text(650, 610, "%", 90, NAVY, "sans")
cap1 = c.text(260, 740, "일에 AI 를 쓰는 직장인", 50, INK, "sans", "font-weight:600")
src = c.text(260, 820, "한국은행 BOK 이슈노트 · 2026-11-17", 30, GRY, "sans", "font-weight:500")
# 1년 전 vs 올해 막대
c.svg(f'<rect id="s2-b25" x="1060" y="{640 - 518 * .55:.0f}" width="150" height="{518 * .55:.0f}" fill="{GRY}"/>'
      f'<rect id="s2-b26" x="1260" y="{640 - 665 * .55:.0f}" width="150" height="{665 * .55:.0f}" fill="{NAVY}"/>'
      f'<path d="M1020,640 L1460,640" stroke="{INK}" stroke-width="5"/>')
v25 = c.text(1060, 280, "51.8%", 48, GRY, "sans", "width:150px;text-align:center")
v26 = c.text(1260, 200, "66.5%", 48, NAVY, "sans", "width:150px;text-align:center")
y25 = c.text(1060, 660, "2025", 40, GRY, "sans", "width:150px;text-align:center")
y26 = c.text(1260, 660, "2026", 40, NAVY, "sans", "width:150px;text-align:center")
# 일하는 시간 막대 (40시간 → 9.2% 잘려 나감)
c.svg(f'<rect id="s2-h" x="1040" y="760" width="560" height="70" rx="10" fill="{BLU}"/>'
      f'<rect id="s2-hcut" x="{1040 + 560 * .908:.0f}" y="760" width="{560 * .092:.0f}" height="70" fill="{RED}"/>')
hcap = c.text(1040, 845, "일하는 시간  −9.2%", 46, RED, "sans")
laps = "".join(f'<g class="lp"><rect x="{170 + (k % 10) * 160}" y="{170 + (k // 10) * 200}" width="120" height="76" rx="6" fill="#2C313B"/><rect x="{178 + (k % 10) * 160}" y="{178 + (k // 10) * 200}" width="104" height="58" rx="3" fill="#F6F1E6"/></g>' for k in range(30))
c.svg(f'<g id="s2-laps">{laps}</g>')
c.j(f'tl.fromTo("#s2-laps .lp",{{opacity:0,scale:.4,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:.2,stagger:{{each:.05,from:"random"}}}},{c.cue(4, .05)});')
c.j(f'tl.to("#s2-laps",{{opacity:0,duration:.35}},{c.cue(5, .2)});')
for k in range(3):
    c.pop(f"s2-p{k}", c.cue(5, .35 + k * .06))
c.fade(n665, c.cue(5, .7), .15); c.count(n665, c.cue(5, .7), 0, 66.5, .9, False)
c.j(f'tl.to({{}},{{duration:.01,onComplete:function(){{document.getElementById("{n665}").textContent="66.5"}}}},{c.cue(5, .7) + .95:.2f});')
c.fade(pct, c.cue(5, .8)); c.rise(cap1, c.cue(5, .75)); c.fade(src, c.cue(5, .8))
c.j(f'tl.fromTo("#s2-b25",{{scaleY:0,transformOrigin:"50% 100%"}},{{scaleY:1,duration:.5}},{c.cue(6, .25)});'); c.fade(v25, c.cue(6, .4)); c.fade(y25, c.cue(6, .25))
c.j(f'tl.fromTo("#s2-b26",{{scaleY:0,transformOrigin:"50% 100%"}},{{scaleY:1,duration:.6}},{c.cue(6, .55)});'); c.fade(v26, c.cue(6, .75)); c.fade(y26, c.cue(6, .55))
c.j(f'tl.fromTo("#s2-h",{{scaleX:0,transformOrigin:"0% 50%"}},{{scaleX:1,duration:.4}},{c.cue(7, .1)});')
c.j(f'tl.set("#s2-hcut",{{opacity:0}},0);tl.set("#s2-hcut",{{opacity:1}},{c.cue(7, .55)});')
c.j(f'tl.to("#s2-hcut",{{x:80,y:30,rotation:12,opacity:0,duration:.7,ease:"power2.in"}},{c.cue(7, .65)});')
c.fade(hcap, c.cue(7, .55))

# ═══ s3 마디 — 그래서 월급은? (어두운 바탕, 긴 쉼 동안 빈 칸이 기다림) ═══
c = sc("s3")
q1 = c.text(0, 300, "다음 숫자", 64, GRY, "my", center=True)
c.svg(f'<rect id="s3-bx" x="660" y="460" width="600" height="200" rx="20" fill="none" stroke="{LIGHT}" stroke-width="6" stroke-dasharray="18 14"/>')
qm = c.text(0, 490, "?", 140, YEL, "sans", center=True)
q2 = c.text(0, 720, "그래서 월급은 얼마나 올랐을까", 76, LIGHT, "my", center=True)
c.fade(q1, .15); c.draw("s3-bx", c.cue(8, .5), .8)
c.j(f'tl.fromTo("#{qm}",{{opacity:0,scale:.4}},{{opacity:1,scale:1,duration:.4,ease:"back.out(2.5)"}},{c.cue(8, 1.0)});')
c.j(f'tl.fromTo("#{qm}",{{opacity:1}},{{opacity:.35,duration:.5,repeat:3,yoyo:true}},{c.cue(8, 1.0) + .5:.2f});')
c.rise(q2, c.cue(9, .05))

# ═══ s4 통념 — 일이 빨라진다 → 돈이 된다 ═══
c = sc("s4")
hd = c.text(0, 170, "흔히 하는 말", 60, GRY, "my", center=True)
a = box(c, 240, 420, 560, 220, "일이 빨라진다", NAVY, "s4-a", 60)
b = box(c, 1120, 420, 560, 220, "돈이 된다", GOLD, "s4-b", 60)
c.svg(f'<path id="s4-ar" d="M830,530 L1090,530" stroke="{INK}" stroke-width="12" stroke-linecap="round"/><path id="s4-ah" d="M1060,500 L1095,530 L1060,560" fill="none" stroke="{INK}" stroke-width="12" stroke-linecap="round"/>')
sub = c.text(0, 720, "AI 를 잘 쓰는 사람이 몸값도 오른다", 54, INK, "sans", center=True, extra="font-weight:600")
c.fade(hd, c.cue(10, .1))
c.rise(sub, c.cue(11, .1))
c.j(f'tl.fromTo("#s4-a",{{opacity:0,scale:.7,transformOrigin:"520px 530px"}},{{opacity:1,scale:1,duration:.35,ease:"back.out(2)"}},{c.cue(12, .0)});'); c.fade(a, c.cue(12, .05))
c.draw("s4-ar", c.cue(12, .4), .4); c.fade("s4-ah", c.cue(12, .6), .15)
c.j(f'tl.fromTo("#s4-b",{{opacity:0,scale:.7,transformOrigin:"1400px 530px"}},{{opacity:1,scale:1,duration:.35,ease:"back.out(2)"}},{c.cue(12, .6)});'); c.fade(b, c.cue(12, .65))

# ═══ s5 2만 5천 명을 2년 동안 — 소득 변화 0 (같은 화살표가 끊김) ═══
c = sc("s5")
rr = random.Random(3)
dots = "".join(f'<circle class="pd" cx="{160 + (k % 25) * 26}" cy="{230 + (k // 25) * 26}" r="9" fill="{NAVY}" opacity="0"/>' for k in range(250))
c.svg(f'<g id="s5-dots">{dots}</g>')
nd = c.text(160, 520, "25,000명 · 2년", 64, NAVY, "sans")
nds = c.text(160, 610, "같은 사람의 쓰임새와 실제 소득을 맞대어", 38, GRY, "sans", "font-weight:500")
# 소득 변화 그래프
c.svg(f'<path d="M1000,250 L1000,700 L1760,700" fill="none" stroke="{INK}" stroke-width="5"/>'
      f'<path d="M1000,475 L1760,475" stroke="{GRY}" stroke-width="3" stroke-dasharray="10 10"/>'
      f'<path id="s5-ln" d="M1000,475 C1150,470 1250,480 1400,476 S1650,472 1760,475" fill="none" stroke="{RED}" stroke-width="10" stroke-linecap="round"/>')
gy = c.text(1010, 200, "소득 변화", 44, INK, "sans")
zero = c.text(1640, 250, "0", 150, RED, "my")
c.j(f'tl.to("#s5-dots .pd",{{opacity:.9,duration:.05,stagger:{{each:.006,from:"random"}}}},{c.cue(13, .3)});')
c.rise(nd, c.cue(14, .05)); c.fade(nds, c.cue(14, .3))
c.fade(gy, c.cue(14, .55)); c.draw("s5-ln", c.cue(14, .6), 1.3, "none")
c.stamp(zero, c.cue(15, .05))
gnote = c.text(1000, 720, "선은 결과(효과 0)를 나타낸 그림 — 실제 시계열 아님", 26, "#6E6A60", "sans", "font-weight:500")
c.fade(gnote, c.cue(14, .7))

# ═══ s6 세 칸 기준판 — 시간 · 일 · 돈, 기준 두 가지 ═══
c = sc("s6")
q = c.text(0, 130, "시간은 줄었는데, 돈은 왜 그대로일까", 60, INK, "my", center=True)
tA = box(c, 170, 360, 420, 230, "시간", BLU, "s6-a", 80)
tB = box(c, 750, 360, 420, 230, "일", NAVY, "s6-b", 80)
tC = box(c, 1330, 360, 420, 230, "돈", GOLD, "s6-c", 80)
c.svg(f'<path id="s6-br1" d="M590,475 L750,475" stroke="{INK}" stroke-width="16"/>'
      f'<path id="s6-br2" d="M1170,475 L1330,475" stroke="{INK}" stroke-width="5" stroke-dasharray="14 14"/>')
qq = c.text(1215, 380, "?", 80, RED, "sans")
chk = c.text(0, 700, "☐ 기준 하나      ☐ 기준 둘", 58, INK, "sans", center=True, extra="font-weight:600")
c.rise(q, c.cue(16, .1))
for bid, tid, tt in (("s6-a", tA, c.cue(16, .1)), ("s6-c", tC, c.cue(16, .55)), ("s6-b", tB, c.cue(18, .38))):
    c.j(f'tl.fromTo("#{bid}",{{opacity:0,y:40}},{{opacity:1,y:0,duration:.3,ease:"power3.out"}},{tt});'); c.fade(tid, tt + .05)
dn = c.text(250, 610, "↓ 줄었다", 44, BLU, "sans"); c.pop(dn, c.cue(16, .3))
fl = c.text(1420, 610, "→ 그대로", 44, GOLD, "sans"); c.pop(fl, c.cue(16, .75))
up = c.tag(700, 230, "월급이 오른 사람들은 무엇이 달랐나?", RED, size=40); c.pop(up, c.cue(17, .3))
c.out([up], c.cue(18, .2)); c.out([dn, fl], c.cue(19, .2))
c.j(f'tl.fromTo("#s6-br1",{{scaleX:0,transformOrigin:"0% 50%"}},{{scaleX:1,duration:.4}},{c.cue(19, .3)});')
c.j(f'tl.fromTo("#s6-br2",{{scaleX:0,transformOrigin:"0% 50%"}},{{scaleX:1,duration:.6}},{c.cue(19, .55)});'); c.pop(qq, c.cue(19, .8))
c.rise(chk, c.cue(20, .5))

# ═══ s7 3장 — 덴마크 연구: '정확한 0' (돈 칸을 확대, 2% 띠) ═══
c = sc("s7")
card = c.name(160, 130, "덴마크 · 2만 5천 명 · 소득 행정자료", "훔룸·베스테르고르, NBER WP 33777 (2025, 2026 개정)")
c.svg(f'<rect id="s7-band" x="1000" y="{520 - 2 * 45}" width="700" height="{4 * 45}" fill="{YEL}" fill-opacity=".25"/>'
      f'<path d="M1000,520 L1700,520" stroke="{INK}" stroke-width="5"/>'
      f'<circle id="s7-pt" cx="1350" cy="520" r="26" fill="{RED}"/>')
bl = c.text(1720, 410, "+2%", 40, GOLD, "sans"); bl2 = c.text(1720, 585, "−2%", 40, GOLD, "sans")
gl = c.text(1000, 300, "소득·근로시간 변화 (출시 2년 뒤)", 42, INK, "sans")
z = c.text(0, 680, "‘정확한 0’", 120, RED, "my", center=True)
chips = ["많이 쓰는 사람", "일찍 쓴 사람", "투자 많이 한 회사", "성과급 직업"]
cids = [c.tag(160 + k * 410, 840, s + " → 0", NAVY, size=34) for k, s in enumerate(chips)]
c.slide(card, .2)
c.fade(gl, c.cue(21, .3)); c.j(f'tl.fromTo("#s7-pt",{{opacity:0,scale:0,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:.3,ease:"back.out(3)"}},{c.cue(21, .6)});')
c.stamp(z, c.cue(22, .55))
c.j(f'tl.fromTo("#s7-band",{{scaleY:0,transformOrigin:"50% 50%"}},{{scaleY:1,duration:.5}},{c.cue(23, .55)});'); c.fade(bl, c.cue(23, .6)); c.fade(bl2, c.cue(23, .6))
for k, i in enumerate(cids):
    c.pop(i, c.cue(24, .08 + k * .2))

# ═══ s8 97.7% '영향 없음' · 아낀 시간 중 3~7% 만 소득 ═══
c = sc("s8")
g = "".join(f'<rect class="cl" x="{180 + (k % 10) * 56}" y="{220 + (k // 10) * 56}" width="44" height="44" rx="6" fill="{GRY if k < 98 else GOLD}" opacity="0"/>' for k in range(100))
c.svg(f'<g id="s8-g">{g}</g>')
n977 = c.text(180, 800, "97.7% ‘소득엔 영향 없었다’", 54, INK, "sans")
c.svg(f'<circle id="s8-pie" cx="1380" cy="480" r="230" fill="{BLU}" fill-opacity=".35" stroke="{BLU}" stroke-width="6"/>'
      f'<path id="s8-sl" d="M1380,480 L1380,250 A230,230 0 0 1 1480,273 Z" fill="{GOLD}"/>')
pl = c.text(1180, 760, "아낀 시간 중 소득이 된 몫", 44, INK, "sans")
p37 = c.text(1520, 180, "3~7%", 84, GOLD, "sans")
sk = c.text(1180, 830, "근로자 스스로 추정", 32, GRY, "sans", "font-weight:500")
c.j(f'tl.to("#s8-g .cl",{{opacity:1,duration:.04,stagger:{{each:.025}}}},{c.cue(25, .1)});')
ask = c.text(180, 130, "AI 를 쓰는 사람에게 물었다: 소득이 달라졌나?", 46, INK, "sans"); c.rise(ask, c.cue(25, .05))
c.rise(n977, c.cue(26, .5))
c.j(f'tl.fromTo("#s8-pie",{{opacity:0,scale:.5,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:.4}},{c.cue(27, .1)});'); c.fade(pl, c.cue(27, .2))
c.j(f'tl.fromTo("#s8-sl",{{opacity:0,scale:0,transformOrigin:"1380px 480px"}},{{opacity:1,scale:1,duration:.4,ease:"back.out(2)"}},{c.cue(27, .7)});')
c.pop(p37, c.cue(27, .72)); c.fade(sk, c.cue(27, .8))

# ═══ s9 계산 — 주 3.7시간 × 3~7% ≈ 주 7~16분 (가정) ═══
c = sc("s9")
hd = c.text(0, 140, "만약 한국도 같다면", 60, GRY, "my", center=True)
a1 = c.tag(260, 380, "주 3.7시간 아낌", BLU, size=58)
xx = c.text(880, 375, "×", 90, INK, "sans")
a2 = c.tag(1000, 380, "3~7%", GOLD, size=58)
eq = c.text(1330, 375, "≈", 90, INK, "sans")
a3 = c.tag(1450, 380, "주 7~16분", RED, size=58)
note = c.tag(0, 640, "가정 계산 · 크기를 가늠하는 숫자", "#6E6A60", size=40)
c.j(f'tl.set("#{note}",{{left:"50%",xPercent:-50}},0);')
c.fade(hd, c.cue(28, .2)); c.pop(a1, c.cue(29, .2)); c.fade(xx, c.cue(29, .4)); c.pop(a2, c.cue(29, .45))
c.fade(eq, c.cue(29, .65)); c.stamp(a3, c.cue(29, .72)); c.rise(note, c.cue(30, .35))
c.j(f'tl.fromTo("#{a3}",{{scale:1}},{{scale:.85,duration:.8,ease:"power2.inOut",transformOrigin:"50% 50%"}},{c.cue(30, .6)});')

SFX = [("click-soft", 1, .3), ("whoosh-short", 1, .75), ("pop", 2, .62), ("chime", 3, .45), ("pop", 5, .7), ("whoosh-short", 7, .65),
       ("impact-bass-2", 15, .05), ("pop", 18, .1), ("pop", 18, .38), ("pop", 18, .66), ("impact-bass-2", 22, .55), ("click", 24, .1),
       ("click-soft", 27, .7), ("pop", 29, .72)]
H.write(WORK, SFX)
