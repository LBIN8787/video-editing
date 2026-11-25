"""새 스타일 샘플 생성기: assets/vo/lines.json(문장 길이) → index.html + compositions/*.html. python build.py"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
L = json.load(open(HERE / "assets/vo/lines.json", encoding="utf-8"))
GAP, LEAD = 0.2, 0.5
t = LEAD
for x in L:
    x["start"] = round(t, 2)
    t += x["dur"] + GAP
END = round(t + 1.2, 2)
SHOTS = [("a", [0, 1]), ("b", [2]), ("c", [3]), ("d", [4]), ("e", [5, 6]), ("f", [7, 8])]
shot = {}
for k, (sid, idx) in enumerate(SHOTS):
    s0 = 0.0 if k == 0 else round(L[idx[0]]["start"] - 0.25, 2)
    shot[sid] = {"start": s0, "lines": idx}
for k, (sid, _) in enumerate(SHOTS):
    shot[sid]["end"] = shot[SHOTS[k + 1][0]]["start"] if k + 1 < len(SHOTS) else END
    shot[sid]["dur"] = round(shot[sid]["end"] - shot[sid]["start"], 2)


def loc(sid, i, off=0.0):
    """문장 i 가 시작하는 장면 안 시각."""
    return round(L[i]["start"] - shot[sid]["start"] + off, 2)


INK, ACC, GRY, BG = "#1D2024", "#E2552B", "#8A8F96", "#E8E6E1"
NOISE = ("url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'>"
         "<feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3' seed='4'/><feColorMatrix values='0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .55 0'/>"
         "</filter><rect width='300' height='300' filter='url(%23n)'/></svg>\")")
BASE_CSS = """
@font-face{font-family:'NotoKR';src:url('assets/fonts/NotoSansKR-VF.ttf');font-weight:100 900}
#root{position:absolute;inset:0;background:BG;overflow:hidden;font-family:'NotoKR';color:INK}
.cam{position:absolute;inset:0;transform-origin:50% 50%}
.grain{position:absolute;inset:0;background-image:NOISE;opacity:.16;mix-blend-mode:multiply;pointer-events:none}
.vig{position:absolute;inset:0;background:radial-gradient(ellipse at center,rgba(0,0,0,0) 55%,rgba(0,0,0,.10) 100%);pointer-events:none}
.shadow{box-shadow:0 18px 36px rgba(20,22,26,.18)}
""".replace("BG", BG).replace("INK", INK).replace("NOISE", NOISE)


def scene(sid, css, body, js):
    d = shot[sid]["dur"]
    return f"""<template>
<style>{BASE_CSS}{css}</style>
<div id="root" data-composition-id="{sid}" data-width="1920" data-height="1080">
<div class="cam" id="{sid}-cam">{body}</div>
<div class="grain"></div><div class="vig"></div>
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
tl.fromTo("#{sid}-cam", {{scale:1}}, {{scale:1.05, duration:{d}, ease:"sine.inOut"}}, 0);
{js}
window.__timelines["{sid}"] = tl;
</script>
</template>
"""


def wave(prefix, n=40, x0=1120, x1=1760, cy=540, hmax=260, dur=10.0, small=False):
    bars, js = [], []
    w = (x1 - x0) / n
    for i in range(n):
        h = 40 + (hmax - 40) * (0.35 + 0.65 * abs(((i * 37) % 17) / 16 - 0.5) * 2)
        bars.append(f'<div id="{prefix}{i}" style="position:absolute;left:{x0 + i * w:.0f}px;top:{cy - h / 2:.0f}px;width:{w * .55:.0f}px;height:{h:.0f}px;'
                    f'border-radius:6px;background:{INK};transform-origin:50% 50%;opacity:{.85 if not small else .6}"></div>')
        rep = int(dur / 0.36)
        js.append(f'tl.fromTo("#{prefix}{i}",{{scaleY:.25}},{{scaleY:1,duration:.18,ease:"sine.inOut",yoyo:true,repeat:{rep}}},{(i % 7) * .05:.2f});')
    return "".join(bars), "".join(js)


# ── A: 11.17 + 통화 파형 → 날짜가 머리글로 ───────────────────────────
dA = shot["a"]["dur"]
wb, wj = wave("aw", dur=dA)
t1 = loc("a", 1)
A = scene("a", """
#a-date{position:absolute;left:120px;top:250px;font-weight:900;font-size:360px;letter-spacing:-12px;line-height:1;transform-origin:0 0}
#a-sub{position:absolute;left:132px;top:650px;font-weight:700;font-size:48px;color:#5C6168}
#a-q{position:absolute;left:120px;top:330px;font-weight:900;font-size:300px;color:ACC;line-height:1}
#a-rule{position:absolute;left:132px;top:700px;width:1100px;height:6px;background:INK;transform-origin:0 50%}
.a-n{position:absolute;font-weight:900;color:#B4B7BB;white-space:nowrap;letter-spacing:-2px}
#a-n1{left:820px;top:300px;font-size:110px}#a-n2{left:900px;top:460px;font-size:76px}#a-n3{left:860px;top:590px;font-size:64px}
#a-who{position:absolute;left:140px;top:740px;font-weight:800;font-size:52px;color:#4A4F56}
""".replace("ACC", ACC).replace("INK", INK),
    f'<div id="a-date">11.17</div><div id="a-sub">엔비디아 3분기 실적 발표 · 통화 음성</div>{wb}'
    f'<div id="a-q">“</div><div id="a-rule"></div>'
    '<div class="a-n" id="a-n1">매출 1,158억 달러</div><div class="a-n" id="a-n2">데이터센터 +110%</div><div class="a-n" id="a-n3">다음 분기 1,300억</div><div id="a-who">하비 존스 · 엔비디아 이사회 의장</div>',
    f'tl.fromTo("#a-date",{{x:-420,opacity:0}},{{x:0,opacity:1,duration:.6,ease:"power3.out"}},.15);'
    f'tl.fromTo("#a-sub",{{opacity:0,y:24}},{{opacity:1,y:0,duration:.5,ease:"power3.out"}},.55);'
    + wj +
    f'tl.to("#a-date",{{scale:.26,x:-10,y:-170,duration:.7,ease:"power2.inOut"}},{t1});'
    f'tl.to("#a-sub",{{opacity:0,duration:.3}},{t1});'
    f'tl.fromTo(".a-n",{{opacity:0,x:80}},{{opacity:1,x:0,duration:.45,ease:"power3.out",stagger:.15}},{t1 + .3});'
    f'tl.to("#aw0,#aw1,#aw2,#aw3,#aw4,#aw5,#aw6,#aw7,#aw8,#aw9,#aw10,#aw11,#aw12,#aw13,#aw14,#aw15,#aw16,#aw17,#aw18,#aw19,#aw20,#aw21,#aw22,#aw23,#aw24,#aw25,#aw26,#aw27,#aw28,#aw29,#aw30,#aw31,#aw32,#aw33,#aw34,#aw35,#aw36,#aw37,#aw38,#aw39",{{opacity:0,duration:.3}},{t1 + .1});'
    f'tl.to(".a-n",{{x:900,opacity:0,duration:.6,ease:"power2.in",stagger:.08}},{t1 + 2.4});'
    f'tl.fromTo("#a-q",{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:.5,ease:"back.out(2)"}},{t1 + 2.5});'
    f'tl.fromTo("#a-rule",{{scaleX:0}},{{scaleX:1,duration:.7,ease:"power2.inOut"}},{t1 + 2.8});'
    f'tl.fromTo("#a-who",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.45,ease:"power3.out"}},{t1 + 3.2});')

# ── B: 인용이 한 글자씩 인쇄 ─────────────────────────────────────────
qt = "복귀시킬 생각은 없다."
chars = "".join(f'<span class="bq" id="bq{i}">{c if c != " " else "&nbsp;"}</span>' for i, c in enumerate(qt))
dB = shot["b"]["dur"]
wb2, wj2 = wave("bw", n=24, x0=1500, x1=1780, cy=150, hmax=90, dur=dB, small=True)
B = scene("b", """
#b-head{position:absolute;left:120px;top:90px;font-weight:900;font-size:94px;letter-spacing:-3px}
#b-q{position:absolute;left:120px;top:330px;font-weight:900;font-size:300px;color:ACC;line-height:1}
#b-text{position:absolute;left:300px;top:380px;font-weight:900;font-size:150px;letter-spacing:-4px;white-space:nowrap}
.bq{display:inline-block}
#b-name{position:absolute;left:310px;top:620px;font-weight:800;font-size:52px}
#b-line{position:absolute;left:310px;top:690px;width:820px;height:8px;background:ACC;transform-origin:0 50%}
#b-orig{position:absolute;left:310px;top:730px;font-weight:500;font-size:34px;color:#6A6F76;font-style:italic}
""".replace("ACC", ACC),
    f'<div id="b-head">11.17</div>{wb2}<div id="b-q">“</div><div id="b-text">{chars}</div>'
    f'<div id="b-name">하비 존스 · 엔비디아 이사회 의장</div><div id="b-line"></div>'
    f'<div id="b-orig">“…does not intend to reinstate Jensen as CEO.”</div>',
    f'tl.fromTo(".bq",{{opacity:0,y:30}},{{opacity:1,y:0,duration:.12,ease:"power3.out",stagger:.075}},.25);'
    + wj2 +
    f'tl.fromTo("#b-name",{{opacity:0,x:-30}},{{opacity:1,x:0,duration:.45,ease:"power3.out"}},1.5);'
    f'tl.fromTo("#b-line",{{scaleX:0}},{{scaleX:1,duration:.6,ease:"power2.inOut"}},1.7);'
    f'tl.fromTo("#b-orig",{{opacity:0}},{{opacity:1,duration:.5}},2.1);')

# ── C: 탁상 달력 17 → 23, 인용에 줄, 도장 ──────────────────────────────
pages = "".join(
    f'<div class="pg" id="cp{d}" data-layout-allow-overlap style="z-index:{40 - d}"><div class="pgd">{d}</div><div class="pgw">{w}</div></div>'
    for d, w in zip(range(17, 24), ["화요일", "수요일", "목요일", "금요일", "토요일", "일요일", "월요일"]))
C = scene("c", """
#c-cal{position:absolute;left:170px;top:150px;width:640px;height:760px;perspective:1600px}
#c-band{position:absolute;left:0;top:0;width:640px;height:150px;background:ACC;border-radius:18px 18px 0 0;z-index:60;
  color:#fff;font-weight:900;font-size:64px;display:flex;align-items:center;justify-content:center;letter-spacing:4px}
.ring{position:absolute;top:-26px;width:26px;height:64px;border-radius:13px;background:#3A3F46;z-index:70}
.pg{position:absolute;left:0;top:150px;width:640px;height:610px;background:#FBFAF7;border-radius:0 0 18px 18px;
  transform-origin:50% 0;box-shadow:0 18px 36px rgba(20,22,26,.18);display:flex;flex-direction:column;align-items:center;justify-content:center}
.pgd{font-weight:900;font-size:330px;line-height:1;letter-spacing:-10px}
.pgw{font-weight:700;font-size:48px;color:#6A6F76;margin-top:10px}
#cp23 .pgd{color:ACC}
#c-six{position:absolute;left:930px;top:180px;font-weight:900;font-size:190px;letter-spacing:-6px}
#c-quote{position:absolute;left:940px;top:470px;font-weight:900;font-size:76px;white-space:nowrap}
#c-strike{position:absolute;left:930px;top:510px;width:780px;height:12px;background:ACC;transform-origin:0 50%}
#c-stamp{position:absolute;left:960px;top:640px;padding:10px 40px;border:12px solid ACC;border-radius:14px;color:ACC;
  font-weight:900;font-size:110px;transform:rotate(-7deg);white-space:nowrap}
""".replace("ACC", ACC),
    f'<div id="c-cal"><div id="c-band">NOV · 2026</div><div class="ring" style="left:150px"></div><div class="ring" style="left:464px"></div>{pages}</div>'
    f'<div id="c-six">엿새 뒤</div><div id="c-quote">복귀시킬 생각은 없다.</div><div id="c-strike"></div><div id="c-stamp">만장일치 복귀</div>',
    'tl.fromTo("#c-cal",{y:900},{y:0,duration:.7,ease:"power3.out"},0);'
    + "".join(f'tl.fromTo("#cp{d}",{{rotationX:0,opacity:1}},{{rotationX:-115,opacity:0,duration:.32,ease:"power2.in"}},{0.75 + (d - 17) * 0.3:.2f});' for d in range(17, 23))
    + 'tl.fromTo("#c-six",{opacity:0,x:60},{opacity:1,x:0,duration:.5,ease:"power3.out"},.6);'
    'tl.fromTo("#c-quote",{opacity:0,y:20},{opacity:1,y:0,duration:.4,ease:"power3.out"},2.7);'
    'tl.fromTo("#c-strike",{scaleX:0},{scaleX:1,duration:.45,ease:"power2.inOut"},3.3);'
    'tl.to("#c-quote",{opacity:.35,duration:.3},3.6);'
    'tl.fromTo("#c-stamp",{opacity:0,scale:1.9},{opacity:1,scale:1,duration:.28,ease:"back.out(2.2)"},4.2);')

# ── D: 실제 종가 선 ─────────────────────────────────────────────────
P = [("11.11", 173.73), ("11.12", 166.19), ("11.13", 162.85), ("11.16", 156.14), ("11.17", 155.46),
     ("11.18", 150.96), ("11.19", 145.98), ("11.20", 125.53), ("11.23", 165.1)]
X0, X1, Y0, Y1, LO, HI = 220, 1640, 270, 860, 115, 185
X = lambda i: X0 + (X1 - X0) * i / (len(P) - 1)
Y = lambda v: Y1 - (Y1 - Y0) * (v - LO) / (HI - LO)
p1 = "M" + " L".join(f"{X(i):.0f},{Y(v):.0f}" for i, (_, v) in enumerate(P[:8]))
p2 = f"M{X(7):.0f},{Y(P[7][1]):.0f} L{X(8):.0f},{Y(P[8][1]):.0f}"
ticks = "".join(f'<div class="tk" style="left:{X(i) - 50:.0f}px">{d}</div>' for i, (d, _) in enumerate(P))
D = scene("d", """
#d-svg{position:absolute;left:0;top:0}
.tk{position:absolute;top:890px;width:100px;text-align:center;font-weight:700;font-size:30px;color:#6A6F76}
#d-hi{position:absolute;left:150px;top:180px;font-weight:900;font-size:56px}
#d-lo{position:absolute;left:1500px;top:770px;font-weight:900;font-size:56px}
#d-big{position:absolute;left:1040px;top:120px;font-weight:900;font-size:140px;color:ACC;letter-spacing:-5px;white-space:nowrap}
#d-src{position:absolute;left:150px;top:148px;font-weight:500;font-size:26px;color:#7A7F86}
#d-title{position:absolute;left:150px;top:90px;font-weight:800;font-size:44px;color:#5C6168}
""".replace("ACC", ACC),
    f'<svg id="d-svg" width="1920" height="1080"><line x1="{X0}" y1="{Y1}" x2="{X1}" y2="{Y1}" stroke="#B9BCC0" stroke-width="3"/>'
    f'<path id="d-l1" d="{p1}" fill="none" stroke="{INK}" stroke-width="9" stroke-linejoin="round" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>'
    f'<path id="d-l2" d="{p2}" fill="none" stroke="{ACC}" stroke-width="14" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>'
    f'<circle id="d-dot" cx="{X(8):.0f}" cy="{Y(P[8][1]):.0f}" r="18" fill="{ACC}"/></svg>{ticks}'
    f'<div id="d-title">엔비디아 주가 (달러)</div><div id="d-hi">173</div><div id="d-lo">125</div><div id="d-big">+30% 넘게</div>'
    f'<div id="d-src">종가: 야후 파이낸스 · 11.23 은 보도 기준(+31.5%)</div>',
    'tl.fromTo("#d-l1",{strokeDashoffset:1},{strokeDashoffset:0,duration:1.9,ease:"none"},.2);'
    'tl.fromTo("#d-hi",{opacity:0},{opacity:1,duration:.3},.2);'
    'tl.fromTo("#d-lo",{opacity:0,y:-20},{opacity:1,y:0,duration:.35},2.0);'
    'tl.fromTo("#d-l2",{strokeDashoffset:1},{strokeDashoffset:0,duration:.45,ease:"power3.out"},2.3);'
    'tl.fromTo("#d-dot",{scale:0,transformOrigin:"50% 50%"},{scale:1,duration:.3,ease:"back.out(3)"},2.7);'
    'tl.fromTo("#d-big",{opacity:0,y:40},{opacity:1,y:0,duration:.45,ease:"power3.out"},2.75);')

# ── E: 8-K 문서 + 형광펜 + 다가가기 ────────────────────────────────
t6 = loc("e", 6)
E = scene("e", """
#e-doc{position:absolute;left:250px;top:90px;width:1420px;height:1100px;background:#FFFFFF;padding:70px 90px;box-sizing:border-box;
  transform:rotate(-1.2deg);box-shadow:0 22px 44px rgba(20,22,26,.22);font-family:'NotoKR';transform-origin:57% 55%}
#e-meta{font-weight:600;font-size:28px;color:#7A7F86;letter-spacing:1px}
#e-head{font-weight:800;font-size:56px;line-height:1.18;margin:26px 0 34px;color:INK}
.e-p{font-weight:500;font-size:36px;line-height:1.62;color:#2A2E33;margin:0 0 22px}
mark{background:linear-gradient(ACCB,ACCB) no-repeat 0 82%;background-size:0% 46%;color:inherit;padding:0 2px}
#e-src{position:absolute;left:250px;top:28px;font-weight:600;font-size:26px;color:#5C6168}
""".replace("INK", INK).replace("ACCB", "rgba(226,85,43,.55)"),
    '<div id="e-doc"><div id="e-meta">NVIDIA · PRESS RELEASE · SANTA CLARA · NOVEMBER 23, 2026</div>'
    '<div id="e-head">NVIDIA Board Reinstates Jensen Huang as President, CEO and Board Director</div>'
    '<p class="e-p">The Board voted unanimously to reinstate Mr. Huang following a series of discussions and meetings with Mr. Huang.</p>'
    '<p class="e-p">In the process of reaching its decision, the Board received input from <mark id="e-mk">senior levels of the United States government</mark>, '
    'and based on that input, the Board is confident that Mr. Huang\'s reinstatement poses no national security risk.</p></div>'
    '<div id="e-src">엔비디아 보도자료 (8-K 첨부, 2026.11.23) — 원문</div>',
    'tl.fromTo("#e-doc",{y:1000,rotation:4},{y:0,rotation:-1.2,duration:.8,ease:"power3.out"},.1);'
    'tl.fromTo("#e-src",{opacity:0},{opacity:1,duration:.4},.7);'
    f'tl.fromTo("#e-mk",{{backgroundSize:"0% 46%"}},{{backgroundSize:"100% 46%",duration:.9,ease:"power2.inOut"}},{t6 - .6});'
    f'tl.to("#e-doc",{{scale:1.35,x:386,y:-80,duration:1.0,ease:"power2.inOut"}},{t6 - .2});'
    f'tl.to("#e-src",{{opacity:0,duration:.3}},{t6 - .2});')

# ── F: 칩 → 유리 금고·자물쇠 → 대표 의자와 두 실 ─────────────────────
t8 = loc("f", 8)
pins = []
for k in range(8):
    o = 70 + k * 31
    pins += [f'<rect x="{o}" y="14" width="14" height="40" rx="4" fill="#C9A24B"/>', f'<rect x="{o}" y="346" width="14" height="40" rx="4" fill="#C9A24B"/>',
             f'<rect x="14" y="{o}" width="40" height="14" rx="4" fill="#C9A24B"/>', f'<rect x="346" y="{o}" width="40" height="14" rx="4" fill="#C9A24B"/>']
chip = (f'<svg width="400" height="400" viewBox="0 0 400 400">{"".join(pins)}'
        '<defs><linearGradient id="fg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3B4149"/><stop offset=".55" stop-color="#22262B"/><stop offset="1" stop-color="#14171A"/></linearGradient>'
        '<linearGradient id="fd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#6E7782"/><stop offset=".5" stop-color="#9AA5B1"/><stop offset="1" stop-color="#55606B"/></linearGradient></defs>'
        '<rect x="50" y="50" width="300" height="300" rx="22" fill="url(#fg)"/><rect x="110" y="110" width="180" height="180" rx="10" fill="url(#fd)"/>'
        + "".join(f'<line x1="{110 + j * 30}" y1="112" x2="{110 + j * 30}" y2="288" stroke="#47515B" stroke-width="2"/>' for j in range(1, 6))
        + '<text x="200" y="335" text-anchor="middle" font-family="NotoKR" font-weight="900" font-size="30" fill="#C9CED4">AI 칩</text></svg>')
lock = ('<svg width="150" height="190" viewBox="0 0 150 190"><path id="f-shackle" d="M35 85 V55 a40 40 0 0 1 80 0 V85" fill="none" stroke="#3A3F46" stroke-width="16" stroke-linecap="round"/>'
        f'<rect x="10" y="80" width="130" height="105" rx="16" fill="{ACC}"/><circle cx="75" cy="122" r="13" fill="#fff"/><rect x="69" y="125" width="12" height="32" rx="5" fill="#fff"/></svg>')
chair = ('<svg width="380" height="520" viewBox="0 0 380 520"><path d="M70 20 h240 a30 30 0 0 1 30 30 v230 h-300 v-230 a30 30 0 0 1 30 -30z" fill="#2C3138"/>'
         '<rect x="20" y="270" width="340" height="70" rx="20" fill="#3A4048"/><rect x="0" y="210" width="40" height="120" rx="14" fill="#2C3138"/><rect x="340" y="210" width="40" height="120" rx="14" fill="#2C3138"/>'
         '<rect x="175" y="340" width="30" height="110" fill="#3A4048"/><path d="M60 500 L190 450 L320 500" fill="none" stroke="#3A4048" stroke-width="22" stroke-linecap="round"/></svg>')
F = scene("f", """
#f-grp{position:absolute;left:0;top:0;width:1920px;height:1080px;transform-origin:50% 50%}
#f-chip{position:absolute;left:760px;top:330px;filter:drop-shadow(0 20px 30px rgba(20,22,26,.3))}
#f-vault{position:absolute;left:690px;top:260px;width:540px;height:540px;border-radius:34px;border:8px solid #8E98A2;
  background:linear-gradient(135deg,rgba(255,255,255,.38),rgba(190,205,215,.18) 60%,rgba(255,255,255,.30));box-sizing:border-box}
#f-shine{position:absolute;left:40px;top:30px;width:120px;height:420px;background:rgba(255,255,255,.35);border-radius:30px;transform:skewX(-12deg)}
#f-lock{position:absolute;left:885px;top:700px}
#f-tag{position:absolute;left:1180px;top:300px;padding:12px 30px;background:ACC;color:#fff;font-weight:900;font-size:60px;border-radius:10px;transform:rotate(6deg);white-space:nowrap}
#f-chair{position:absolute;left:1380px;top:380px}
#f-svg{position:absolute;left:0;top:0}
.f-lb{position:absolute;font-weight:900;font-size:64px;white-space:nowrap}
#f-who{position:absolute;left:0;width:1920px;top:50px;text-align:center;font-weight:900;font-size:120px;letter-spacing:-3px}
""".replace("ACC", ACC),
    f'<div id="f-grp"><div id="f-chip">{chip}</div><div id="f-vault"><div id="f-shine"></div></div><div id="f-lock">{lock}</div>'
    f'<div id="f-tag">국가 안보 자산</div></div>'
    f'<div id="f-chair">{chair}</div>'
    f'<svg id="f-svg" width="1920" height="1080"><path id="f-s1" d="M330 300 C 700 360, 1150 330, 1470 430" fill="none" stroke="{INK}" stroke-width="7" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>'
    f'<path id="f-s2" d="M700 760 C 1000 900, 1300 820, 1480 640" fill="none" stroke="{ACC}" stroke-width="9" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/></svg>'
    f'<div class="f-lb" id="f-l1" style="left:150px;top:390px">회사</div><div class="f-lb" id="f-l2" style="left:470px;top:800px;color:{ACC}">국가</div>'
    '<div id="f-who">누가 정했나?</div>' + '<svg id="f-bld" style="position:absolute;left:120px;top:150px" width="200" height="230" viewBox="0 0 200 230"><rect x="20" y="40" width="160" height="190" rx="6" fill="#3A4048"/><rect x="60" y="10" width="80" height="40" rx="4" fill="#2C3138"/>' + ''.join(f'<rect x="{40 + c * 45}" y="{70 + r * 40}" width="25" height="22" rx="3" fill="#C9CED4"/>' for c in range(3) for r in range(3)) + '</svg>',
    'tl.fromTo("#f-chip",{scale:.7,opacity:0,rotation:-8},{scale:1,opacity:1,rotation:0,duration:.6,ease:"back.out(1.6)"},.2);'
    'tl.fromTo("#f-vault",{y:-900},{y:0,duration:.7,ease:"power3.in"},1.2);'
    'tl.fromTo("#f-lock",{y:300,opacity:0},{y:0,opacity:1,duration:.45,ease:"power3.out"},1.95);'
    'tl.fromTo("#f-shackle",{y:-22},{y:0,duration:.18,ease:"power2.in"},2.45);'
    'tl.fromTo("#f-tag",{opacity:0,scale:1.6},{opacity:1,scale:1,duration:.3,ease:"back.out(2.2)"},2.6);'
    f'tl.to("#f-grp",{{scale:.62,x:-520,y:60,duration:1.0,ease:"power2.inOut"}},{t8});'
    f'tl.fromTo("#f-chair",{{opacity:0,x:200}},{{opacity:1,x:0,duration:.7,ease:"power3.out"}},{t8 + .5});'
    f'tl.fromTo("#f-l1,#f-bld",{{opacity:0}},{{opacity:1,duration:.4}},{t8 + 1.3});'
    f'tl.fromTo("#f-s1",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:.8,ease:"power2.inOut"}},{t8 + 1.4});'
    f'tl.fromTo("#f-l2",{{opacity:0}},{{opacity:1,duration:.4}},{t8 + 2.6});'
    f'tl.fromTo("#f-s2",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:.8,ease:"power2.inOut"}},{t8 + 2.7});'
    f'tl.fromTo("#f-who",{{opacity:0,y:-30}},{{opacity:1,y:0,duration:.5,ease:"power3.out"}},{t8 + 4.4});')

for sid, html in zip("abcdef", [A, B, C, D, E, F]):
    (HERE / "compositions" / f"{sid}.html").write_text(html, encoding="utf-8")

# ── 자막 (말하는 동안만) ─────────────────────────────────────────────
cap = "".join(
    f'<div class="clip cap" id="cap{x["i"]}" data-start="{x["start"] + .05:.2f}" data-duration="{x["dur"] - .25:.2f}" data-track-index="20"><span>{x["text"]}</span></div>'
    for x in L)
# ── 효과음 (보이는 동작에만) ─────────────────────────────────────────
S = lambda sid, tt: round(shot[sid]["start"] + tt, 2)
sfx = [("whoosh-short", S("a", .15)), ("typing", S("b", .25)), ("whoosh", S("c", 0))] + \
      [("click", S("c", .75 + k * .3)) for k in range(6)] + \
      [("impact-bass-2", S("c", 4.2)), ("riser", S("d", 2.0)), ("whoosh-short", S("e", .1)), ("pop", S("f", .2)),
       ("whoosh", S("f", 1.2)), ("click-soft", S("f", 2.45)), ("whoosh-cinematic", S("f", loc("f", 8)))]
aud = "".join(f'<audio id="vo{x["i"]}" class="clip" src="assets/vo/{x["file"]}" data-start="{x["start"]}" data-duration="{x["dur"]}" data-track-index="7" data-volume="1"></audio>' for x in L)
aud += "".join(f'<audio id="sx{k}" class="clip" src="assets/sfx/{n}.mp3" data-start="{tt}" data-duration="{1.6 if n != "typing" else 1.3}" data-track-index="{8 + k % 3}" data-volume="0.35"></audio>' for k, (n, tt) in enumerate(sfx))
hosts = "".join(
    f'<div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" data-start="{shot[sid]["start"]}" '
    f'data-duration="{shot[sid]["dur"]}" data-track-index="1" data-track-kind="graphics" data-width="1920" data-height="1080"></div>'
    for sid, _ in SHOTS)
index = f"""<!doctype html><html><head><meta charset="utf-8">
<script src="assets/gsap.min.js"></script>
<style>
@font-face{{font-family:'NotoKR';src:url('assets/fonts/NotoSansKR-VF.ttf');font-weight:100 900}}
.cap{{position:absolute;left:0;width:1920px;top:950px;text-align:center;z-index:50;font-family:'NotoKR'}}
.cap span{{display:inline-block;background:rgba(29,32,36,.86);color:#fff;font-weight:700;font-size:46px;padding:10px 26px;border-radius:8px;max-width:1600px}}
</style></head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{END}" data-width="1920" data-height="1080">
{hosts}{cap}{aud}
</div>
<script>window.__timelines["main"] = gsap.timeline({{ paused: true }});</script>
</body></html>
"""
(HERE / "index.html").write_text(index, encoding="utf-8")
print("END", END, {k: (v["start"], v["dur"]) for k, v in shot.items()})
