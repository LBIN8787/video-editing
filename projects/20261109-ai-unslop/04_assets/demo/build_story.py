"""unslop 시연: 예제 대시보드(heydamir/unslop examples/dashboard.html, CC BY 4.0)를 unslop 절차대로 고친 결과를
스토리 파일(story.html, 단계별 CSS)과 완성본(after.html)으로 만든다. 아이콘은 Lucide(ISC).
    python build_story.py <lucide 아이콘 폴더> <출력 폴더>
"""
import re
import sys
from pathlib import Path

ICONS, OUT = Path(sys.argv[1]), Path(sys.argv[2])
BELL = '<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>'


def ic(name, size=16):
    inner = BELL if name == "bell" else re.sub(r"^.*?<svg[^>]*>|</svg>\s*$", "", (ICONS / f"{name}.svg").read_text(), flags=re.S)
    return (f'<svg class="ic" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{inner}</svg>')


def emo(e, icon, size=16):
    """이모지 → 선 아이콘 (같은 상자에 겹쳐 두고 2단계에서 서로 바뀜)."""
    return f'<span class="ibox"><span class="emo">{e}</span><span class="ico">{ic(icon, size)}</span></span>'


def swap(at, a, b, cls=""):
    return f'<span class="swap {cls}" data-at="{at}"><span class="from">{a}</span><span class="to">{b}</span></span>'


NAV = [("🏠", "house", "Overview", True, None), ("📥", "mail", "Inbox", False, "12"), ("🚀", "layers", "Projects", False, "new"),
       ("👥", "users", "Customers", False, None), ("💸", "receipt", "Invoices", False, None), ("📊", "chart-column", "Reports", False, None)]
PLANS = [("🏢", "building-2", "Enterprise", "18"), ("💼", "briefcase", "Business", "64"), ("⚡", "zap", "Pro", "210"),
         ("🌱", "leaf", "Starter", "480"), ("🎁", "gift", "Free", "1.2k")]
# 원래 화면의 들쭉날쭉한 줄 높이·간격 (0단계 그대로)
NAV_H, NAV_MT, NAV_G = [46, 30, 40, 32, 44, 31], [0, 12, 0, 8, 1, 14], [6, 6, 8, 5, 9, 6]
PLAN_H, PLAN_MT, PLAN_G = [42, 28, 38, 44, 34], [0, 9, 2, 12, 5], [6, 8, 4, 7, 6]
BARS = [120, 172, 133, 225, 161, 97, 143]
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

nav = []
for k, (e, i, label, active, extra) in enumerate(NAV):
    tail = ""
    if extra == "12":
        tail = '<span class="cnt hot">12</span>'
    elif extra == "new":
        tail = '<span class="cnt glow" data-out="3">New ✨</span>'
    nav.append(f'<a class="nrow{" act" if active else ""}" style="height:{NAV_H[k]}px;margin-top:{NAV_MT[k]}px">'
               f'{"<span class=actbg></span>" if active else ""}{emo(e, i)}<span class="nl" style="margin-left:{NAV_G[k]}px">{label}</span>{tail}</a>')
plans = []
for k, (e, i, label, n) in enumerate(PLANS):
    plans.append(f'<div class="prow" style="height:{PLAN_H[k]}px;margin-top:{PLAN_MT[k]}px">{emo(e, i)}'
                 f'<span class="nl" style="margin-left:{PLAN_G[k]}px">{label}</span><span class="cnt glow">{n}<span data-out="2">&nbsp;👤</span></span></div>')
bars = "".join(f'<div class="bar{" now" if k == 3 else ""}" style="height:{h}px"></div>' for k, h in enumerate(BARS))
days = "".join(f'<span class="day">{d}</span>' for d in DAYS)

HTML = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="unslop-steps" content="Spacing, Color and icons, Type and copy, Details">
<meta name="unslop-frame" content="200 22 1040">
<title>EmberAI Dashboard — unslop</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
/* ---------- 0단계: 원래 화면 (examples/dashboard.html 을 같은 값으로 옮김) ---------- */
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ width: 1440px; min-height: 980px; }}
body {{ font-family: Inter, sans-serif; background-color: #2e1872; position: relative; color: #fff;
  transition: background-color .6s; }}
.wash {{ position: absolute; inset: 0; background: linear-gradient(180deg, #5b34b8, #2e1872 50%, #170d3d); transition: opacity .6s; }}
.win {{ position: absolute; left: 220px; top: 40px; width: 1000px; height: 900px; display: flex; overflow: hidden; border-radius: 14px;
  box-shadow: 0 40px 110px rgba(76,29,149,.6), 0 0 0 1px rgba(167,139,250,.4); }}
.side {{ width: 272px; flex-shrink: 0; display: flex; flex-direction: column; background: #140e33; border-right: 1px solid #2c2470;
  padding: 10px 22px 0 10px; }}
.brand {{ display: flex; align-items: center; height: 36px; }}
.logo {{ position: relative; width: 32px; height: 32px; border-radius: 12px; display: grid; place-items: center; overflow: hidden;
  background: #8b5cf6; box-shadow: 0 0 18px rgba(139,92,246,.7); }}
.logo .lg {{ position: absolute; inset: 0; background: linear-gradient(135deg, #8b5cf6, #3b82f6); }}
.logo .spark {{ position: relative; font-size: 15px; }}
.logo .glyph {{ position: absolute; inset: 0; display: grid; place-items: center; opacity: 0; }}
.glyph i {{ width: 10px; height: 14px; border-radius: 6px 6px 3px 3px; background: #151413; transform: rotate(8deg); display: block; }}
.wm {{ position: relative; margin-left: 7px; font-size: 19px; font-weight: 800; color: #c4b5fd; }}
.wm .wg {{ position: absolute; inset: 0; background: linear-gradient(135deg, #c4b5fd, #60a5fa); -webkit-background-clip: text; background-clip: text; color: transparent; }}
.wm2 {{ position: relative; color: #e9d5ff; }}
.wm2 .wg2 {{ position: absolute; inset: 0; background: linear-gradient(135deg, #e9d5ff, #818cf8); -webkit-background-clip: text; background-clip: text; color: transparent; }}
.pro {{ margin-left: 8px; }}
.bell {{ margin-left: auto; }}
.glow {{ border-radius: 9px; padding: 2px 8px; font-size: 10.5px; font-weight: 700; color: #fff; background-color: #7c4ff0;
  box-shadow: 0 0 12px rgba(168,85,247,.55); }}
.hot {{ border-radius: 9px; padding: 2px 6px; font-size: 11px; font-weight: 800; color: #fff; background-color: #f43f5e; }}
.search {{ margin-top: 26px; display: flex; align-items: center; height: 46px; border-radius: 23px; border: 1px solid #5b4bc4; background: #1f1850;
  padding: 0 7px 0 11px; box-shadow: 0 0 18px rgba(139,92,246,.4); }}
.search .sl {{ margin-left: 5px; font-size: 14px; font-weight: 600; color: #968ee0; }}
.kbd {{ margin-left: auto; border-radius: 9px; padding: 2px 8px; font-size: 10.5px; font-weight: 700; color: #fff; background-color: #7c4ff0;
  box-shadow: 0 0 12px rgba(168,85,247,.55); border: 1px solid transparent; }}
.div {{ height: 1px; background: #2f2672; margin: 12px -22px 0 -10px; }}
.div2 {{ margin-top: 30px; }}
.lab {{ margin-top: 22px; font-size: 11px; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; color: #968ee0; }}
.nav {{ margin-top: 4px; }}
.plans {{ margin-top: 5px; }}
.nrow, .prow {{ position: relative; display: flex; align-items: center; border-radius: 12px; padding: 0 13px 0 7px; color: #d6d2ff;
  transition: none; }}
.actbg {{ position: absolute; inset: 0; border-radius: inherit; background: linear-gradient(135deg, #7c3aed, #2563eb);
  box-shadow: 0 8px 24px rgba(124,58,237,.55); }}
.act {{ color: #fff; background-color: #6d3fe8; }}
.nl {{ position: relative; font-size: 14.5px; font-weight: 600; }}
.cnt {{ margin-left: auto; position: relative; }}
.ibox {{ position: relative; display: inline-grid; width: 16px; height: 16px; place-items: center; flex-shrink: 0; }}
.ibox > * {{ grid-area: 1 / 1; }}
.emo {{ font-size: 12px; line-height: 1; }}
.ico {{ opacity: 0; display: grid; }}
.main {{ position: relative; flex: 1; min-width: 0; overflow: hidden; background: #0d1131; padding: 0 0 0 18px; }}
.mwash {{ position: absolute; inset: 0; pointer-events: none;
  background: radial-gradient(70% 50% at 85% 0%, rgba(139,92,246,.4), transparent 70%), radial-gradient(60% 40% at 10% 100%, rgba(59,130,246,.25), transparent 70%); }}
.crumb {{ position: relative; margin-top: 10px; height: 36px; display: flex; align-items: center; font-size: 14.5px; font-weight: 700; }}
.crumb .nl {{ margin-left: 7px; font-weight: 700; }}
h1 {{ position: relative; margin-top: 4px; font-size: 35px; font-weight: 800; line-height: 1.25; color: #e9d5ff; }}
.gt {{ background: linear-gradient(135deg, #f0abfc, #818cf8); -webkit-background-clip: text; background-clip: text; color: transparent; }}
.stats {{ position: relative; margin-top: 44px; display: flex; }}
.card {{ position: relative; overflow: hidden; border-radius: 24px; padding: 12px; background-color: #241f6a;
  border: 1px solid rgba(167,139,250,.5); box-shadow: inset 0 1px 0 rgba(255,255,255,.22), 0 14px 34px rgba(124,58,237,.42); }}
.card > .cg {{ position: absolute; inset: 0; background: radial-gradient(120% 90% at 0% 0%, rgba(255,255,255,.12), rgba(255,255,255,0) 60%),
  linear-gradient(115deg, #2b1f6e, #1f2269 48%, #122666); }}
.card > *:not(.cg) {{ position: relative; }}
.stat {{ width: 316px; height: 123px; }}
.stat + .stat {{ margin-left: 26px; }}
.cl {{ font-size: 11.5px; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; color: #d6d2ff; display: flex; align-items: center; gap: 6px; }}
.fig {{ margin-top: 4px; font-size: 32px; font-weight: 800; line-height: 1.2; color: #e9d5ff; font-variant-numeric: tabular-nums; }}
.chg {{ margin-top: 10px; font-size: 13px; font-weight: 700; color: #4ade80; }}
.deco {{ position: absolute !important; right: 6px; bottom: 20px; font-size: 54px; filter: drop-shadow(0 0 14px rgba(168,85,247,.8)); }}
.dot {{ width: 6px; height: 6px; border-radius: 3px; background: #E8622C; display: inline-block; }}
.chart {{ margin-top: 28px; width: 660px; height: 392px; }}
.chart .fig {{ font-size: 30px; }}
.chart .chg {{ margin-top: 6px; }}
.plot {{ position: absolute !important; left: 12px; right: 0; top: 128px; bottom: 30px; }}
.grid {{ position: absolute; left: 0; right: 0; height: 1px; background: rgba(139,92,246,.3); }}
.bars {{ position: absolute; left: 0; right: 0; bottom: 0; display: flex; align-items: flex-end; gap: 16px; }}
.bar {{ width: 40px; border-radius: 20px; background-color: #7c6cf0; box-shadow: inset 0 1px 0 rgba(255,255,255,.35), 0 0 22px rgba(139,92,246,.55); }}
.bar.now {{ background-color: #c084fc; }}
.days {{ position: absolute; left: 0; right: 0; bottom: -24px; display: flex; gap: 16px; font-size: 11px; font-weight: 700; letter-spacing: .08em;
  text-transform: uppercase; color: rgba(196,181,253,.75); }}
.day {{ width: 40px; text-align: center; }}

/* ---------- 1단계: 간격 (4px 격자, 같은 것은 같은 크기) ---------- */
.s1 .side {{ padding: 16px 16px 0 16px; }}
.s1 .search {{ margin-top: 20px; height: 36px; padding: 0 8px 0 12px; }}
.s1 .search .sl {{ margin-left: 10px; }}
.s1 .div {{ margin: 16px -16px 0 -16px; }}
.s1 .div2 {{ margin-top: 24px; }}
.s1 .lab {{ margin-top: 24px; }}
.s1 .nav, .s1 .plans {{ margin-top: 8px; }}
.s1 .nrow, .s1 .prow {{ height: 32px !important; margin-top: 2px !important; padding: 0 8px; }}
.s1 .nav .nrow:first-child, .s1 .plans .prow:first-child {{ margin-top: 0 !important; }}
.s1 .nrow .nl, .s1 .prow .nl {{ margin-left: 10px !important; }}
.s1 .main {{ padding: 0 32px; }}
.s1 .crumb {{ margin-top: 24px; }}
.s1 h1 {{ margin-top: 8px; }}
.s1 .stats {{ margin-top: 32px; }}
.s1 .card {{ padding: 20px; }}
.s1 .stat + .stat {{ margin-left: 16px; }}
.s1 .chart {{ margin-top: 16px; }}
.s1 .plot {{ left: 20px; right: 20px; top: 136px; bottom: 44px; }}

/* ---------- 2단계: 색과 아이콘 (따뜻한 흑연 무채색 + 숯불 주황 하나) ---------- */
.s2 body {{ background-color: #0f0e0d; }}
.s2 .wash, .s2 .mwash, .s2 .actbg, .s2 .card > .cg, .s2 .logo .lg, .s2 .wm .wg, .s2 .wg2 {{ opacity: 0; }}
.s2 .wm2 {{ color: #EDEAE4; }}
.s2 .win {{ box-shadow: 0 24px 60px rgba(0,0,0,.5), 0 0 0 1px rgba(245,240,232,.08); }}
.s2 .side {{ background: #171615; border-right-color: rgba(245,240,232,.08); }}
.s2 .main {{ background: #121110; }}
.s2 .logo {{ background: #E8622C; box-shadow: none; }}
.s2 .logo .spark {{ opacity: 0; }}
.s2 .logo .glyph {{ opacity: 1; }}
.s2 .wm {{ color: #EDEAE4; }}
.s2 .glow, .s2 .hot {{ background-color: transparent; box-shadow: none; color: #8E8981; }}
.s2 .search {{ background: #1d1c1a; border-color: rgba(245,240,232,.08); box-shadow: none; }}
.s2 .search .sl {{ color: #8E8981; }}
.s2 .kbd {{ background-color: #262422; box-shadow: none; color: #A9A49B; }}
.s2 .div {{ background: rgba(245,240,232,.08); }}
.s2 .lab {{ color: #77736C; }}
.s2 .nrow, .s2 .prow {{ color: #A9A49B; }}
.s2 .act {{ background-color: #262422; color: #EDEAE4; box-shadow: inset 0 0 0 1px rgba(245,240,232,.06); }}
.s2 .emo {{ opacity: 0; }}
.s2 .ico {{ opacity: 1; }}
.s2 .crumb {{ color: #A9A49B; }}
.s2 h1, .s2 .fig {{ color: #EDEAE4; }}
.s2 .card {{ background-color: #1a1918; border-color: rgba(245,240,232,.08); box-shadow: none; }}
.s2 .cl {{ color: #A9A49B; }}
.s2 .chg {{ color: #8FBF8A; }}
.s2 .deco {{ opacity: 0; }}
.s2 .grid {{ background: rgba(245,240,232,.06); }}
.s2 .bar {{ background-color: #3A3835; box-shadow: none; }}
.s2 .bar.now {{ background-color: #E8622C; }}
.s2 .days {{ color: #77736C; }}

/* ---------- 3단계: 글꼴과 문구 (무게 400~500, 대문자 라벨 없애기, 느낌표·인사말 없애기) ---------- */
.s3 body {{ font-family: "IBM Plex Sans", sans-serif; }}
.s3 .wm {{ font-weight: 600; font-size: 17px; margin-left: 10px; }}
.s3 .lab, .s3 .cl, .s3 .days {{ letter-spacing: 0; text-transform: none; font-weight: 500; }}
.s3 .lab {{ font-size: 12px; }}
.s3 .cl {{ font-size: 13px; }}
.s3 .nl {{ font-size: 14px; font-weight: 400; }}
.s3 .act .nl {{ font-weight: 500; }}
.s3 .crumb, .s3 .crumb .nl {{ font-weight: 500; font-size: 13px; }}
.s3 h1 {{ font-size: 28px; font-weight: 500; }}
.s3 .fig {{ font-size: 30px; font-weight: 500; }}
.s3 .chg {{ font-size: 13px; font-weight: 400; }}
.s3 .glow, .s3 .hot, .s3 .days, .s3 .kbd {{ font-family: "IBM Plex Mono", monospace; font-weight: 400; font-size: 12px; }}
.s3 .search .sl {{ font-weight: 400; }}

/* ---------- 4단계: 마감 (모서리 반지름 규칙, 키캡, 막대 모양, 표시 점) ---------- */
.s4 .logo {{ border-radius: 8px; }}
.s4 .search {{ border-radius: 8px; }}
.s4 .kbd {{ border-radius: 4px; border-color: rgba(245,240,232,.12); padding: 0 6px; }}
.s4 .nrow, .s4 .prow {{ border-radius: 8px; }}
.s4 .card {{ border-radius: 14px; }}
.s4 .bar {{ border-radius: 4px 4px 0 0; }}
</style>
</head>
<body>
<div class="wash"></div>
<div class="win">
  <aside class="side">
    <div class="brand" data-gap="side">
      <div class="logo" data-slop="Glowing gradient logo"><span class="lg"></span><span class="spark">✨</span><span class="glyph"><i></i></span></div>
      <span class="wm">EmberAI<span class="wg">EmberAI</span></span>
      <span class="glow pro" data-out="3">PRO</span>
      <span class="bell">{emo("🔔", "bell")}</span>
    </div>
    <div class="search" data-gap="side" data-radius>{emo("🔍", "search")}<span class="sl">{swap(3, "Search anything...", "Search")}</span><span class="kbd">⌘K</span></div>
    <div class="div"></div>
    <p class="lab" data-gap="side">Navigation</p>
    <nav class="nav" data-gap="side">{"".join(nav)}</nav>
    <div class="div div2"></div>
    <p class="lab"><span data-out="2">💳&nbsp;</span>Plans</p>
    <div class="plans" data-gap="side">{"".join(plans)}</div>
    <div data-gap="side" style="height:1px"></div>
  </aside>
  <main class="main">
    <div class="mwash"></div>
    <div class="crumb"><span data-out="2">📊</span><span class="nl">Overview</span></div>
    <h1>{swap(3, '<span class="gt" data-slop="Gradient text">Welcome back, Damir! 👋</span>', "November 2026")}</h1>
    <div class="stats">
      <div class="card stat" data-radius><span class="cg"></span>
        <p class="cl"><span data-out="2">💰</span>Paid this month</p>
        <p class="fig"><span class="wm2">$48,210<span class="wg2">$48,210</span></span></p>
        <p class="chg">{swap(3, "🔥 +12%!!", "+12% vs last month")}</p>
        <span class="deco" data-slop="Emoji decoration">💳</span>
      </div>
      <div class="card stat"><span class="cg"></span>
        <p class="cl"><span data-out="2">⚠️</span><span class="dot" data-in="4"></span>Overdue</p>
        <p class="fig">{swap(3, '<span class="gt">07</span>', "7")}</p>
        <p class="chg">{swap(3, "😬 3 less!!", "3 fewer vs last month")}</p>
      </div>
    </div>
    <div class="card chart" data-radius><span class="cg"></span>
      <p class="cl"><span data-out="2">📈</span>Revenue</p>
      <p class="fig">{swap(3, '<span class="gt">$124,860.40</span>', "$124,860")}</p>
      <p class="chg">{swap(3, "🚀 +4.2% this month!!", "+4.2% vs last month")}</p>
      <div class="plot">
        <div class="grid" style="top:0"></div><div class="grid" style="top:25%"></div><div class="grid" style="top:50%"></div><div class="grid" style="top:75%"></div>
        <div class="bars" data-slop="Glowing pill bars">{bars}</div>
        <div class="days">{days}</div>
      </div>
    </div>
  </main>
</div>
</body>
</html>
'''
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "story.html").write_text(HTML, encoding="utf-8")
# 완성본: 모든 단계를 적용한 정지 화면 (스토리 효과 없이)
after = HTML.replace('<html lang="en">', '<html lang="en" class="s1 s2 s3 s4">', 1).replace("</style>", """
.swap > .from { display: none; } [data-out] { display: none !important; } [data-in] { opacity: 1; }
</style>""", 1)
(OUT / "after.html").write_text(after, encoding="utf-8")
before = HTML.replace("</style>", ".swap > .to { display: none; } [data-in] { opacity: 0; }\n</style>", 1)
(OUT / "before_rebuilt.html").write_text(before, encoding="utf-8")
print("ok", OUT)
