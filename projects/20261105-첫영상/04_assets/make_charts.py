"""첫영상 차트 생성. 숫자는 01_research/factsheet.md 의 F번호를 따른다.

    python projects/20261105-첫영상/04_assets/make_charts.py
→ 같은 폴더에 scene_XXX.png (1920x1080) 생성. 직접 만든 소스라 저작권 문제가 없다.
"""
import math
import subprocess
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

OUT = Path(__file__).resolve().parent
FONT = subprocess.run(["fc-match", "-f", "%{file}", ":lang=ko:weight=bold"], capture_output=True, text=True).stdout.strip()
font_manager.fontManager.addfont(FONT)
plt.rcParams["font.family"] = font_manager.FontProperties(fname=FONT).get_name()
plt.rcParams["axes.unicode_minus"] = False

BG, FG, MUTED, ACCENT, HOT, RED = "#0e1422", "#ffffff", "#8a96b0", "#00c8be", "#ffd23c", "#ff5a5a"
SRC = "출처: "


def canvas():
    fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
    fig.patch.set_facecolor(BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 192)
    ax.set_ylim(0, 108)
    ax.axis("off")
    ax.add_patch(plt.Rectangle((0, 0), 1.8, 108, color=ACCENT))
    return fig, ax


def save(fig, sid):
    fig.savefig(OUT / f"scene_{sid:03d}.png", facecolor=BG)
    plt.close(fig)


def title(ax, t, src=""):
    ax.text(10, 98, t, fontsize=40, color=FG, va="top", weight="bold")
    if src:
        ax.text(186, 92, SRC + src, fontsize=18, color=MUTED, ha="right", va="top")


def box(ax, x, y, w, h, text, color=ACCENT, fc=None, size=30, ls="-", tc=None):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.4,rounding_size=2",
                                ec=color, fc=fc or BG, lw=4, ls=ls))
    ax.text(x, y, text, fontsize=size, color=tc or FG, ha="center", va="center", weight="bold")


def arrow(ax, a, b, color=MUTED, ls="-", rad=0.0, lw=4):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=34, color=color, lw=lw,
                                 linestyle=ls, connectionstyle=f"arc3,rad={rad}"))


def hbars(ax, rows, x0=48, x1=170, y0=80, gap=11, vmax=None, unit=""):
    vmax = vmax or max(v for _, v, *_ in rows if v)
    for i, (label, v, *opt) in enumerate(rows):
        y = y0 - i * gap
        color = opt[0] if opt else ACCENT
        txt = opt[1] if len(opt) > 1 else f"{v:g}{unit}"
        ax.text(x0 - 3, y, label, fontsize=32, color=FG, ha="right", va="center")
        w = (x1 - x0) * min(v / vmax, 1) if v else 2
        ax.add_patch(plt.Rectangle((x0, y - 3.4), w, 6.8, color=color))
        if v and v > vmax:
            ax.text(x0 + w - 1, y, "≫", fontsize=34, color=BG, ha="right", va="center", weight="bold")
        ax.text(x0 + w + 2, y, txt, fontsize=30, color=FG, va="center")


# --- #2 주주 순위 (F4)
fig, ax = canvas()
title(ax, "네이버 주주 순위 (엔비디아 납입 후)", "네이버 공시·마켓잉크·솔루션뉴스 보도")
hbars(ax, [("국민연금", 9.49, MUTED, "9.49%"), ("블랙록", 7.2, MUTED, "2대 주주"),
           ("엔비디아", 4.13, HOT, "약 4.13%  NEW"), ("이해진 의장", 3.8, MUTED, "4.03% → 약 3.8%")], vmax=11)
save(fig, 2)

# --- #6, #10 타임라인 (F1, F2, F3, F8)
events = [("6월", "AI 팩토리\n공동개발 합의"), ("7/27", "10억 달러\n투자 발표"), ("10/30", "납입일\n연기 공시"),
          ("11/3", "금액 확정\n1조 3,412억"), ("11/6", "납입"), ("11/27", "신주 상장")]
for sid, hl in ((6, {1}), (10, {4, 5})):
    fig, ax = canvas()
    title(ax, "네이버 × 엔비디아 일정", "네이버 공시, KB Think·Korea Times 보도")
    ax.plot([16, 180], [55, 55], color=MUTED, lw=5)
    for i, (d, lab) in enumerate(events):
        x = 20 + i * 31.5
        c = HOT if i in hl else ACCENT
        ax.add_patch(plt.Circle((x, 55), 2.6, color=c))
        ax.text(x, 66, d, fontsize=36, color=c, ha="center", weight="bold")
        ax.text(x, 44, lab, fontsize=24, color=FG if i in hl else MUTED, ha="center", va="top")
    save(fig, sid)

# --- #9 달러 고정, 원화만 감소 (F2, F3)
fig, ax = canvas()
title(ax, "달러는 그대로, 원화만 줄었다", "네이버 공시 (7/27 발표, 11/3 정정)")
for i, (lab, krw, label, sh, pct) in enumerate([("7월 발표", 1.48, "약 1조 4,800억 원", "724만 주", "약 4.5%"),
                                                ("11월 확정", 1.3412, "1조 3,412억 원", "655만 주", "약 4.13%")]):
    x = 60 + i * 72
    h = krw / 1.5 * 42
    ax.add_patch(plt.Rectangle((x - 14, 30), 28, h, color=MUTED if i == 0 else HOT))
    ax.text(x, 32 + h, label, fontsize=34, color=FG, ha="center", va="bottom", weight="bold")
    ax.text(x, 27, f"{lab}  ·  {sh}  ·  {pct}", fontsize=24, color=FG, ha="center", va="top")
    ax.text(x, 84, "10억 달러", fontsize=30, color=ACCENT, ha="center", weight="bold")
save(fig, 9)

# --- #14 브룩필드 → 네이버 (F6)
fig, ax = canvas()
title(ax, "엔비디아 투자의 조건", "Korea Times, UPI (2026-07-27)")
box(ax, 40, 70, 50, 14, "엔비디아\n10억 달러", HOT)
box(ax, 40, 34, 50, 14, "브룩필드\n최대 90억 달러", ACCENT)
box(ax, 140, 52, 46, 16, "네이버", FG, size=40)
arrow(ax, (66, 68), (116, 56), HOT)
arrow(ax, (66, 36), (116, 48), ACCENT)
ax.text(40, 22, "비구속 텀싯 · 조달이 확정돼야 투자 성립", fontsize=24, color=MUTED, ha="center")
save(fig, 14)

# --- #16, #36 순환 흐름도 (F6, F13)
for sid, warn in ((16, False), (36, True)):
    fig, ax = canvas()
    title(ax, "순환 투자 비판" if warn else "돈이 흐르는 순서", "Barchart 논평" if warn else "")
    pts = {"엔비디아": (96, 80), "네이버\n(+브룩필드)": (150, 54), "AI 데이터센터": (96, 28), "GPU 구매": (42, 54)}
    names = list(pts)
    for n, (x, y) in pts.items():
        box(ax, x, y, 40, 14, n, HOT if n == "엔비디아" else ACCENT, size=28)
    for a, b in zip(names, names[1:] + names[:1]):
        (x1, y1), (x2, y2) = pts[a], pts[b]
        arrow(ax, (x1 + (x2 - x1) * 0.28, y1 + (y2 - y1) * 0.28), (x1 + (x2 - x1) * 0.72, y1 + (y2 - y1) * 0.72),
              RED if warn else MUTED, "--" if warn else "-", rad=-0.15)
    if warn:
        ax.add_patch(plt.Circle((96, 54), 38, fill=False, ec=RED, lw=3, ls="--"))
    save(fig, 16 if not warn else 36)

# --- #20 코어위브 vs 네이버 (F14)
fig, ax = canvas()
title(ax, "갚을 힘의 차이 (증권가 분석)", "KB Think(연합인포맥스 분석)")
box(ax, 55, 52, 64, 40, "코어위브\n\n부채 증가\n조달 금리 ↑", RED, size=32)
box(ax, 137, 52, 64, 40, "네이버\n\n연 2조 원+ 이익\n안정적 신용등급", ACCENT, size=32)
save(fig, 20)

# --- #22 엔비디아 ⇄ 네이버
fig, ax = canvas()
title(ax, "서로 필요한 걸 맞바꾼 거래")
box(ax, 45, 52, 50, 18, "엔비디아", HOT, size=40)
box(ax, 147, 52, 50, 18, "네이버", ACCENT, size=40)
arrow(ax, (72, 58), (120, 58), HOT)
arrow(ax, (120, 46), (72, 46), ACCENT)
ax.text(96, 66, "수요 확보", fontsize=30, color=HOT, ha="center")
ax.text(96, 34, "GPU 우선 공급", fontsize=30, color=ACCENT, ha="center")
save(fig, 22)

# --- #24~#26 2026 지분 투자 막대 (F10), 단위: 억 달러
inv = [("코어위브 (1월)", 20), ("오픈AI (2월)", 300), ("루멘텀 (3월)", 20), ("코히어런트 (3월)", 20),
       ("네비우스 (3월)", 20), ("마벨 (봄)", 20), ("코닝 (5월)", 5), ("네이버 (7월)", 10)]
for sid, n in ((24, 2), (25, 5), (26, 8)):
    fig, ax = canvas()
    title(ax, "엔비디아 2026 지분 투자", "CNBC, Quartz, PhotonCap 보도 (단위: 억 달러)")
    rows = []
    for i, (lab, v) in enumerate(inv):
        if i >= n:
            rows.append((lab, 0, BG, ""))
            continue
        c = HOT if (lab.startswith("네이버") and sid == 26) else ACCENT
        rows.append((lab, v, c, "300 (축 밖)" if v == 300 else f"{v}"))
    hbars(ax, rows, x0=58, x1=168, y0=82, gap=8.4, vmax=30)
    save(fig, sid)

# --- #3 #28 #29 #30 #34 #40 #41 지분 지도
customers = ["오픈AI", "코어위브", "네비우스", "네이버"]
supply = ["루멘텀", "코히어런트", "코닝", "마벨"]


def stake_map(sid, show_left=True, show_right=True, links=False, naver_only=False, ttl="엔비디아 지분 지도 2026"):
    fig, ax = canvas()
    title(ax, ttl, "CNBC, Quartz, PhotonCap, 네이버 공시")
    box(ax, 96, 52, 34, 14, "엔비디아", HOT, size=34)
    if show_left:
        ax.text(34, 86, "고객: 수요를 묶는다", fontsize=28, color=ACCENT, ha="center", weight="bold")
    if show_right:
        ax.text(158, 86, "공급망: 물량을 묶는다", fontsize=28, color=ACCENT, ha="center", weight="bold")
    pos = {}
    for side, names, x in ((show_left, customers, 34), (show_right, supply, 158)):
        if not side:
            continue
        for i, n in enumerate(names):
            y = 74 - i * 13
            pos[n] = (x, y)
            dim = naver_only and n != "네이버"
            c = HOT if (naver_only and n == "네이버") else (MUTED if dim else ACCENT)
            box(ax, x, y, 34, 9, n, c, size=26, tc=MUTED if dim else FG)
            arrow(ax, (96 + (-17 if x < 96 else 17), 52), (x + (17 if x < 96 else -17), y), MUTED if dim else c, lw=2.5)
    if links:
        (x1, y1), (x2, y2) = pos["마벨"], pos["루멘텀"]
        ax.plot([x1 + 18, x1 + 24, x2 + 24, x2 + 18], [y1, y1, y2, y2], color=HOT, lw=4)
        ax.text(186, (y1 + y2) / 2, "합병", fontsize=26, color=HOT, ha="right", va="center", rotation=90)
    save(fig, sid)


stake_map(3, ttl="2026년 엔비디아가 지분을 산 회사들")
stake_map(28, show_right=False)
stake_map(29)
stake_map(30)
stake_map(34, links=True)
stake_map(40, links=True, ttl="고객과 공급망, 양쪽의 주주")
stake_map(41, links=True, naver_only=True, ttl="지도 위 첫 한국 회사")

# --- #31 지분 보유액 (F11)
fig, ax = canvas()
title(ax, "엔비디아의 AI 기업 지분 보유액", "Quartz (2026-07-26 기준 집계)")
for i, (lab, v) in enumerate([("1년 전", 70), ("2026년 7월", 990)]):
    x = 70 + i * 60
    h = v / 1000 * 62
    h = v / 1000 * 48
    ax.add_patch(plt.Rectangle((x - 16, 28), 32, h, color=MUTED if i == 0 else HOT))
    ax.text(x, 30 + h, f"약 {v}억 달러", fontsize=34, color=FG, ha="center", va="bottom", weight="bold")
    ax.text(x, 25, lab, fontsize=28, color=FG, ha="center", va="top")
save(fig, 31)

# --- #33 마벨 + 루멘텀 (F12)
fig, ax = canvas()
title(ax, "엔비디아가 투자한 두 회사가 합친다", "TradingKey, Motley Fool 보도 (확정 조건은 공식 발표 확인)")
box(ax, 55, 52, 48, 18, "마벨", ACCENT, size=40)
box(ax, 137, 52, 48, 18, "루멘텀", ACCENT, size=40)
ax.text(96, 52, "+", fontsize=70, color=HOT, ha="center", va="center")
for x in (55, 137):
    ax.text(x, 36, "엔비디아 지분 20억 달러", fontsize=24, color=HOT, ha="center")
save(fig, 33)

print("charts:", sorted(p.name for p in OUT.glob("scene_*.png") if "_auto" not in p.name))
