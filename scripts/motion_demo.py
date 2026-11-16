"""고성능 모션그래픽 초안 (docs/37) — 움직임 토큰·렌더 모션 블러·카운트업·차트 그리기를 한 장면에.

    python scripts/motion_demo.py [출력폴더]      # → <출력폴더>/motion_demo.mp4 (기본: .cache/motion_demo)

숫자는 **예시 데이터**(화면에 표시) — 실제 영상에는 출처로 확인한 숫자만 쓴다.
HyperFrames(tools/hyperframes) 가 설치돼 있어야 한다: python scripts/install_tools.py
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from ytflow.stages import hyper, motionkit as M  # noqa: E402

W, H, DUR = 1920, 1080, 12.0
BG, INK, MUTED, ACC, UP, GRID = "#0f1218", "#f2f2ee", "#8a909c", "#ffcf3f", "#3ddc97", "#232833"
E, D = M.EASE, M.DUR

TITLE = ["같은", "뉴스,", "세", "개의", "숫자"]
STATS = [("매출", 38.2, "조", "+12%"), ("영업이익", 6.1, "조", "+31%"), ("재고", 4.4, "개월", "-0.8")]
BARS = [("1분기", 42), ("2분기", 55), ("3분기", 61), ("4분기", 88)]
LINE = [0.62, 0.58, 0.64, 0.55, 0.49, 0.52, 0.41, 0.37, 0.30, 0.24]


def build(work: Path) -> Path:
    a = work / "assets"
    (a / "fonts").mkdir(parents=True, exist_ok=True)
    shutil.copy(hyper.GSAP, a / "gsap.min.js")
    for f in ("NanumGothic-Bold.ttf", "NanumGothic-ExtraBold.ttf"):
        shutil.copy(ROOT / "ytflow/assets/fonts" / f, a / "fonts" / f)
    js, items = [], []

    # 1) 제목: 단어마다 흐림 → 또렷 (0.13s, 2프레임 간격), 착지 후 정지 → 한 번에 흐리며 퇴장
    words = "".join(f'<span class="w" id="w{i}">{w}</span> ' for i, w in enumerate(TITLE))
    items.append(f'<div id="title" class="t" style="left:0;width:{W}px;top:430px;text-align:center;font-size:120px">{words}</div>')
    items.append(f'<div id="sub" class="t" style="left:0;width:{W}px;top:590px;text-align:center;font-size:40px;color:{MUTED}">'
                 '말한 것 하나만 움직인다</div>')
    js.append(f'tl.fromTo(".w",{{opacity:0,filter:"blur(8px)"}},{{opacity:1,filter:"blur(0px)",duration:0.13,stagger:0.067,ease:"power1.out"}},0.2);')
    js.append(f'tl.fromTo("#sub",{{opacity:0,y:14}},{{opacity:1,y:0,duration:{D["enter"]},ease:"{E["enter"]}"}},0.75);')
    js.append(f'tl.to("#title,#sub",{{opacity:0,filter:"blur(6px)",duration:{D["exit"]},ease:"{E["exit"]}"}},2.3);')

    # 2) 대시보드 판: 오른쪽에서 빠르게(0.45s) 들어오며 렌더 모션 블러가 이동 방향으로 번짐
    dash = []   # 대시보드 안의 모든 것 — 판과 함께 한 덩어리로 들어온다 (먼저 보이면 안 됨)
    dash.append(f'<div id="board" style="position:absolute;left:120px;top:110px;width:{W-240}px;height:{H-220}px;'
                 f'border:2px solid {GRID};border-radius:28px;background:#141821"></div>')
    dash.append(f'<div id="btitle" class="t" style="left:180px;top:150px;font-size:44px">이번 분기, 무엇이 달라졌나'
                 f'<span style="font-size:26px;color:{MUTED};margin-left:24px">예시 데이터</span></div>')
    js.append(f'tl.fromTo("#dash",{{x:1500}},{{x:0,duration:0.45,ease:"{E["enter"]}"}},2.45);')
    js.append(f'tl.fromTo("#btitle",{{opacity:0,x:60}},{{opacity:1,x:0,duration:{D["enter"]},ease:"{E["enter"]}"}},2.65);')

    # 3) 숫자 칸 3개: 40~80ms 차례 + 겹쳐 시작(OVERLAP), 숫자는 착 붙는 곡선(expo.out)으로 세기
    st = M.stagger(len(STATS))
    for i, (name, v, unit, chg) in enumerate(STATS):
        x = 180 + i * 330
        dash.append(f'<div class="tile" id="s{i}" style="position:absolute;left:{x}px;top:250px;width:300px;height:190px;'
                     f'border-radius:20px;background:#1b2030;border:1px solid {GRID}">'
                     f'<div class="t" style="left:28px;top:24px;font-size:28px;color:{MUTED}">{name}</div>'
                     f'<div class="t" style="left:28px;top:70px;font-size:72px"><span id="n{i}">0.0</span>'
                     f'<span style="font-size:32px;color:{MUTED};margin-left:8px">{unit}</span></div>'
                     f'<div class="t" id="c{i}" style="left:28px;top:150px;font-size:26px;color:{UP if chg.startswith("+") else ACC}">{chg}</div></div>')
        t = 3.1 + i * (st + D["enter"] * M.OVERLAP)
        js.append(f'tl.fromTo("#s{i}",{{opacity:0,y:30,scale:0.96}},{{opacity:1,y:0,scale:1,duration:{D["enter"]},ease:"{E["pop"]}"}},{t:.3f});')
        js.append(f'(function(){{var o={{v:0}},el=document.getElementById("n{i}");tl.to(o,{{v:{v},duration:1.1,ease:"{E["settle"]}",'
                  f'onUpdate:function(){{el.textContent=o.v.toFixed(1)}}}},{t + 0.05:.3f});}})();')
        js.append(f'tl.fromTo("#c{i}",{{opacity:0}},{{opacity:1,duration:0.3}},{t + 0.9:.3f});')

    # 4) 막대: 바닥에서 차례로 자람, 마지막 막대만 강조색 + 살짝 튕김(back.out(1.4), 크기만)
    bx0, by, bw, bh = 180, 900, 120, 360
    for i, (q, v) in enumerate(BARS):
        x, h = bx0 + i * 170, bh * v / 100
        col = ACC if i == len(BARS) - 1 else "#3a4256"
        dash.append(f'<div class="bar" id="b{i}" style="position:absolute;left:{x}px;top:{by - h:.0f}px;width:{bw}px;height:{h:.0f}px;'
                     f'background:{col};border-radius:10px 10px 0 0;transform-origin:50% 100%"></div>')
        dash.append(f'<div class="t" style="left:{x}px;width:{bw}px;top:{by + 14}px;text-align:center;font-size:26px;color:{MUTED}">{q}</div>')
        last = i == len(BARS) - 1
        js.append(f'tl.fromTo("#b{i}",{{scaleY:0}},{{scaleY:1,duration:{0.7 if last else 0.55},ease:"{E["pop"] if last else E["enter"]}"}},{4.6 + i * 0.12:.2f});')
    dash.append(f'<div id="blab" class="t" style="left:{bx0 + 3 * 170 - 30}px;top:{by - bh * 0.88 - 64:.0f}px;font-size:34px;color:{ACC}">+60%</div>')
    js.append(f'tl.fromTo("#blab",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.35,ease:"{E["enter"]}"}},5.55);')

    # 5) 선 그래프: 선이 그려지고(draw), 점이 끝을 따라감 — 오른쪽 칸
    lx0, ly0, lw, lh = 1020, 520, 700, 380
    pts = [(lx0 + i * lw / (len(LINE) - 1), ly0 + (1 - v) * lh * 0.9) for i, v in enumerate(LINE)]   # 값이 줄면 선도 내려감
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    grid = "".join(f'<line x1="{lx0}" x2="{lx0 + lw}" y1="{ly0 + k * lh / 4:.0f}" y2="{ly0 + k * lh / 4:.0f}" stroke="{GRID}" stroke-width="2"/>' for k in range(5))
    dash.append(f'<svg style="position:absolute;inset:0" width="{W}" height="{H}">{grid}'
                 f'<path id="ln" d="{d}" fill="none" stroke="{UP}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" pathLength="1" '
                 f'stroke-dasharray="1" stroke-dashoffset="1"/><circle id="dot" r="13" fill="{UP}" cx="{pts[0][0]:.1f}" cy="{pts[0][1]:.1f}"/></svg>')
    dash.append(f'<div class="t" style="left:{lx0}px;top:{ly0 - 70}px;font-size:30px;color:{MUTED}">재고 개월 수 — 줄어드는 중</div>')
    js.append(f'tl.to("#ln",{{strokeDashoffset:0,duration:{D["draw"] + 0.5},ease:"{E["draw"]}"}},5.2);')
    js.append(f'(function(){{var P={json.dumps([[round(x, 1), round(y, 1)] for x, y in pts])},c=document.getElementById("dot"),o={{p:0}};'
              f'tl.to(o,{{p:1,duration:{D["draw"] + 0.5},ease:"{E["draw"]}",onUpdate:function(){{var f=o.p*(P.length-1),i=Math.min(Math.floor(f),P.length-2),k=f-i;'
              f'c.setAttribute("cx",P[i][0]+(P[i+1][0]-P[i][0])*k);c.setAttribute("cy",P[i][1]+(P[i+1][1]-P[i][1])*k);}}}},5.2);}})();')

    items.append(f'<div id="dash" style="position:absolute;inset:0">' + "".join(dash) + '</div>')
    # 6) 카메라: 박자 하나 내내 아주 느린 확대(sine.inOut) — 떨림 없는 실수 좌표 transform
    js.append(f'tl.fromTo("#cam",{{scale:1}},{{scale:1.035,duration:5.5,ease:"{E["camera"]}"}},2.6);')
    # 7) 결론: 화면을 어둡게 덮고 한 줄 (착지 후 정지)
    items_end = (f'<div id="dim" style="position:absolute;inset:0;background:{BG};opacity:0"></div>'
                 f'<div id="end" class="t" style="left:0;width:{W}px;top:470px;text-align:center;font-size:84px">'
                 f'숫자 셋, <span style="color:{ACC}">방향은 하나</span></div>')
    js.append(f'tl.to("#dim",{{opacity:0.92,duration:0.5,ease:"{E["move"]}"}},9.3);')
    js.append(f'tl.fromTo("#end",{{opacity:0,filter:"blur(8px)"}},{{opacity:1,filter:"blur(0px)",duration:0.2,ease:"power1.out"}},9.55);')

    html = f"""<!doctype html>
<html lang="ko"><head><meta charset="UTF-8"><meta name="viewport" content="width={W}, height={H}">
<script src="assets/gsap.min.js"></script>
<style>
@font-face{{font-family:sans;src:url('assets/fonts/NanumGothic-Bold.ttf')}}
@font-face{{font-family:sansx;src:url('assets/fonts/NanumGothic-ExtraBold.ttf')}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:{BG};font-family:sansx;color:{INK}}}
#root{{position:relative;width:100%;height:100%;background:radial-gradient(ellipse at 50% 40%,#161b26 0%,{BG} 70%)}}
#cam{{position:absolute;inset:0;transform-origin:62% 55%}}
.t{{position:absolute;white-space:nowrap;line-height:1.15}}
.w{{display:inline-block}}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.2f}" data-width="{W}" data-height="{H}" data-motion-blur="on">
<div id="layer" class="clip" data-start="0" data-duration="{DUR:.2f}" data-track-index="0" data-layout-allow-overlap>
<div id="cam">{''.join(items)}</div>{items_end}
</div></div>
<script>
window.M={M.gsap_tokens_js()[len('window.M='):-1]};
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
window.__timelines["main"] = tl;
tl.seek(0);
</script></body></html>"""
    (work / "index.html").write_text(html, encoding="utf-8")
    return work


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / ".cache" / "motion_demo"
    work = build(out / "hf")
    print("lint:", M.lint_gsap((work / "index.html").read_text()) or "문제 없음")
    print("check:", hyper.check(work) or "문제 없음")
    mp4 = (out / "motion_demo.mp4").resolve()
    r = subprocess.run([str(hyper.BIN), "render", "--quality", "looks", "--fps", "30", "-o", str(mp4)], cwd=work, env=hyper._env(),
                       capture_output=True, text=True, timeout=900)
    print((r.stdout + r.stderr)[-600:])
    print("→", mp4)


if __name__ == "__main__":
    main()
