"""이어 읽는 시장 — 배너·프로필 시안 3종 (주식 느낌: 캔들 차트 + 뉴스 카드를 실로 '이어' 읽기 + 시세 띠).
    python make_brand.py && node render.js
캔들은 장식용(가짜 데이터 아님을 위해 숫자·날짜 없음). 색: 상승 빨강·하락 파랑 (한국 관례).
"""
import random
from pathlib import Path

HERE = Path(__file__).parent
FONTS = "../../../ytflow/assets/fonts"
THEMES = {
    "a": dict(name="신문지 크림", bg="#F3EEE4", bg2="#E9E2D3", ink="#1C2330", sub="#4A5160", up="#D7392B", down="#2457C9",
              grid="rgba(28,35,48,.07)", card="#FFFFFF", cardink="#1C2330", thread="#D7392B", tape="#1C2330", tapeink="#F3EEE4", titlebg="rgba(255,255,255,.92)", hl="#D7392B"),
    "b": dict(name="딥 그린", bg="#0F2B24", bg2="#071A15", ink="#F2F6F3", sub="#B5C9C0", up="#FF5A4E", down="#5B9BFF",
              grid="rgba(160,220,190,.08)", card="#F2F6F3", cardink="#0F2B24", thread="#F2C14E", tape="#F2C14E", tapeink="#0F2B24", titlebg="rgba(7,26,21,.82)", hl="#F2C14E"),
    "c": dict(name="화이트 블루", bg="#FFFFFF", bg2="#EEF3FB", ink="#0F1B33", sub="#4B5B78", up="#E53935", down="#1E63E9",
              grid="rgba(30,99,233,.08)", card="#0F1B33", cardink="#FFFFFF", thread="#1E63E9", tape="#1E63E9", tapeink="#FFFFFF", titlebg="rgba(255,255,255,.94)", hl="#1E63E9"),
}


def candles(n, x0, x1, y_mid, amp, seed):
    rnd = random.Random(seed)
    w = (x1 - x0) / n
    price, out = 0.0, []
    for i in range(n):
        drift = 0.35 * (1 if i > n * 0.55 else -0.15)     # 뒤로 갈수록 오름 (장식)
        o = price
        c = o + rnd.gauss(drift, 1.0)
        h = max(o, c) + abs(rnd.gauss(0, .6))
        l = min(o, c) - abs(rnd.gauss(0, .6))
        price = c
        out.append((x0 + i * w + w / 2, o, c, h, l))
    ps = [v for _, o, c, h, l in out for v in (h, l)]
    lo, hi = min(ps), max(ps)
    Y = lambda v: y_mid + amp / 2 - (v - lo) / (hi - lo) * amp
    return [(x, Y(o), Y(c), Y(h), Y(l)) for x, o, c, h, l in out], w


def candle_svg(cs, w, t, op=1.0):
    s = []
    for x, o, c, h, l in cs:
        col = t["up"] if c < o else t["down"]     # y 가 작을수록 위 → c<o 면 상승
        s.append(f'<line x1="{x:.1f}" y1="{h:.1f}" x2="{x:.1f}" y2="{l:.1f}" stroke="{col}" stroke-width="3" opacity="{op}"/>')
        y, hh = min(o, c), max(4, abs(c - o))
        s.append(f'<rect x="{x - w * .32:.1f}" y="{y:.1f}" width="{w * .64:.1f}" height="{hh:.1f}" fill="{col}" rx="2" opacity="{op}"/>')
    return "".join(s)


def banner(k, t):
    cs, w = candles(46, 40, 2520, 760, 620, 7)
    ma = " ".join(f"{x:.0f},{(o + c) / 2:.0f}" for x, o, c, h, l in cs)
    # 뉴스 카드 → 캔들 실 (이어 읽기)
    cards = [("실적", 420, 300, 9), ("어닝콜", 950, 1020, 20), ("연준", 1620, 330, 30), ("공시", 2140, 1010, 40)]
    card_html, threads = [], []
    for lab, cx, cy, ci in cards:
        x, o, c, h, l = cs[ci]
        ty = h if cy < 700 else l
        threads.append(f'<path d="M{cx},{cy + (60 if cy < 700 else -60)} Q{(cx + x) / 2},{(cy + ty) / 2 + 60} {x:.0f},{ty:.0f}" fill="none" stroke="{t["thread"]}" stroke-width="4" stroke-dasharray="2 12" stroke-linecap="round"/>'
                       f'<circle cx="{x:.0f}" cy="{ty:.0f}" r="11" fill="{t["thread"]}"/>')
        card_html.append(f'<div class="card" style="left:{cx - 130}px;top:{cy - 60}px"><span class="ct">{lab}</span><i></i><i style="width:70%"></i></div>')
    tape = " · ".join(["S&amp;P 500", "나스닥", "다우", "필라델피아 반도체", "코스피", "코스닥", "원/달러", "미 10년물", "WTI", "금"] * 2)
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:gx;src:url('{FONTS}/NanumGothic-ExtraBold.ttf')}}
@font-face{{font-family:gb;src:url('{FONTS}/NanumGothic-Bold.ttf')}}
html,body{{margin:0;width:2560px;height:1440px;overflow:hidden}}
body{{background:linear-gradient(180deg,{t["bg"]},{t["bg2"]});position:relative;font-family:gb;color:{t["ink"]}}}
.grid{{position:absolute;inset:0;background-image:linear-gradient({t["grid"]} 1px,transparent 1px),linear-gradient(90deg,{t["grid"]} 1px,transparent 1px);background-size:120px 120px}}
svg{{position:absolute;inset:0}}
.card{{position:absolute;width:260px;height:120px;background:{t["card"]};border-radius:14px;box-shadow:0 10px 24px rgba(0,0,0,.18);padding:18px 22px;box-sizing:border-box}}
.card .ct{{display:inline-block;font-family:gx;font-size:30px;color:{t["cardink"]};margin-bottom:12px}}
.card i{{display:block;height:9px;width:100%;border-radius:5px;background:{t["cardink"]};opacity:.18;margin-top:9px}}
.titlebox{{position:absolute;left:600px;top:540px;width:1360px;height:360px;background:{t["titlebg"]};border-radius:28px;box-shadow:0 18px 50px rgba(0,0,0,.18)}}
.title{{position:absolute;left:0;right:0;top:580px;text-align:center;font-family:gx;font-size:160px;letter-spacing:4px;color:{t["ink"]}}}
.title b{{color:{t["hl"]}}}
.sub{{position:absolute;left:0;right:0;top:790px;text-align:center;font-size:46px;color:{t["sub"]}}}
.tape{{position:absolute;left:0;right:0;bottom:0;height:86px;background:{t["tape"]};color:{t["tapeink"]};font-family:gx;font-size:34px;line-height:86px;white-space:nowrap;letter-spacing:2px;padding-left:30px}}
</style></head><body><div class="grid"></div>
<svg width="2560" height="1440">{candle_svg(cs, w, t, .9)}
<polyline points="{ma}" fill="none" stroke="{t["ink"]}" stroke-opacity=".35" stroke-width="4"/>{"".join(threads)}</svg>
{"".join(card_html)}
<div class="titlebox"></div>
<div class="title">이어 읽는 <b>시장</b></div>
<div class="sub">숫자 뒤의 뉴스를 이어, 시장의 의미까지</div>
<div class="tape">{tape}</div>
</body></html>'''


def profile(k, t):
    cs, w = candles(5, 210, 590, 360, 300, 3)
    cs = [(x, o, c, h, l) for x, o, c, h, l in cs]
    pts = " ".join(f"{x:.0f},{min(o, c) - 20:.0f}" for x, o, c, h, l in cs)
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:gx;src:url('{FONTS}/NanumGothic-ExtraBold.ttf')}}
html,body{{margin:0;width:800px;height:800px;overflow:hidden}}
body{{background:radial-gradient(460px 460px at 50% 42%,{t["bg"]},{t["bg2"]});position:relative}}
svg{{position:absolute;inset:0}}
.t{{position:absolute;left:0;right:0;top:545px;text-align:center;font-family:gx;font-size:120px;color:{t["ink"]};letter-spacing:2px}}
.t b{{color:{t["hl"]}}}
</style></head><body>
<svg width="800" height="800">{candle_svg([(x, o, c, h, l) for x, o, c, h, l in cs], w * 1.35, t)}
<polyline points="{pts}" fill="none" stroke="{t["thread"]}" stroke-width="10" stroke-dasharray="4 18" stroke-linecap="round"/>
{"".join(f'<circle cx="{x:.0f}" cy="{min(o, c) - 20:.0f}" r="14" fill="{t["thread"]}"/>' for x, o, c, h, l in cs)}</svg>
<div class="t">이어<b>읽는</b></div></body></html>'''


for k, t in THEMES.items():
    (HERE / f"banner_{k}.html").write_text(banner(k, t), encoding="utf-8")
    (HERE / f"profile_{k}.html").write_text(profile(k, t), encoding="utf-8")
print("ok")
