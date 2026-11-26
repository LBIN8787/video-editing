"""편집 엔진 조각 (build_hf.py 에서 분리). AS 는 호출 쪽에서 정함."""
import random
from pathlib import Path
W, H = 1920, 1080
AS = None
# ---------------------------------------------------------------- 소리 (직접 합성 — 저작권 없음)
def sfx(events, total):
    import numpy as np
    sr = 48000; n = int(total * sr) + sr; out = np.zeros(n)
    rng = np.random.default_rng(7)
    def add(t, sig):
        i = int(t * sr); out[i:i + len(sig)] += sig[: max(0, n - i)]
    def env(L, a=0.01, r=0.3):
        e = np.ones(L); A = int(a * sr); R = int(r * sr)
        e[:A] = np.linspace(0, 1, A); e[-R:] *= np.linspace(1, 0, R); return e
    for kind, t in events:
        if kind == "whoosh":
            L = int(0.45 * sr); x = rng.standard_normal(L); f = np.linspace(0, 1, L)
            x = np.convolve(x, np.ones(30) / 30, "same") * np.sin(np.pi * f) ** 2; add(t - 0.2, 0.5 * x)
        elif kind == "thud":
            L = int(0.6 * sr); tt = np.arange(L) / sr
            x = np.sin(2 * np.pi * (70 - 30 * tt) * tt) * np.exp(-tt * 9) + 0.25 * rng.standard_normal(L) * np.exp(-tt * 40)
            add(t, 0.9 * x)
        elif kind == "hit":   # 긴 저음 충격 + 잔향
            L = int(2.5 * sr); tt = np.arange(L) / sr
            x = (np.sin(2 * np.pi * 45 * tt) + 0.5 * np.sin(2 * np.pi * 90 * tt)) * np.exp(-tt * 1.6)
            add(t, 0.8 * x)
        elif kind == "tick":
            L = int(0.03 * sr); add(t, 0.25 * rng.standard_normal(L) * np.linspace(1, 0, L))
        elif kind == "type":
            L = int(0.04 * sr); add(t, 0.18 * rng.standard_normal(L) * np.linspace(1, 0, L) ** 2)
    # 바닥에 깔리는 어두운 울림(저음 두 개가 천천히 맥놀이)
    tt = np.arange(n) / sr
    drone = 0.05 * (np.sin(2 * np.pi * 55 * tt) + np.sin(2 * np.pi * 55.6 * tt) + 0.6 * np.sin(2 * np.pi * 82.4 * tt))
    drone *= np.minimum(1, tt / 3)
    out += drone
    out = np.clip(out / max(1, np.abs(out).max() / 0.9), -1, 1)
    import wave
    with wave.open(str(AS / "sfx.wav"), "wb") as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(sr); f.writeframes((out * 32767).astype("<i2").tobytes())


# ---------------------------------------------------------------- HTML 조각
R = random.Random(11)
HTML, JS, SFX, DEFS = [], [], [], []
_id = [0]


def nid(p="e"):
    _id[0] += 1; return f"{p}{_id[0]}"


def clip(inner, t0, dur, z=1, extra=""):
    i = nid("c")
    HTML.append(f'<div id="{i}" class="clip" data-start="{t0:.3f}" data-duration="{dur:.3f}" data-track-index="{z}" style="position:absolute;inset:0;z-index:{z};{extra}">{inner}</div>')
    return i


def shot(img, t0, dur, crop=(0, 0, 1, 1), move=(1.0, 1.08, 0, -2, 0, 0), fg=None, flick=None, dust=0, tint=None, bright=1.0, grade=""):
    """그림의 한 부분(crop, 0~1)을 화면 가득 → 카메라 move=(s0,s1,x0%,x1%,y0%,y1%). fg=(마스크, 배율) 앞층 시차."""
    cx, cy, cw, ch = crop
    sc = 1 / cw
    base = f"position:absolute;left:{-cx * sc * 100:.2f}%;top:{-cy * sc * 100:.2f}%;width:{sc * 100:.2f}%;height:{(1 / ch) * 100:.2f}%;object-fit:cover;filter:brightness({bright}) {grade}"
    bg, f = nid("bg"), nid("fg")
    inner = f'<div id="{bg}" style="position:absolute;inset:0"><img src="assets/{img}.jpg" style="{base}"></div>'
    if fg:
        mask, par = fg
        inner += f'<div id="{f}" style="position:absolute;inset:0;-webkit-mask-image:{mask};mask-image:{mask}"><img src="assets/{img}.jpg" style="{base}"></div>'
    if flick:   # 촛불 빛(위치 x,y %)
        fx, fy = flick; fl = nid("fl")
        inner += f'<div id="{fl}" style="position:absolute;inset:0;mix-blend-mode:screen;background:radial-gradient(circle at {fx}% {fy}%,rgba(255,170,80,.55),rgba(255,120,40,.12) 22%,transparent 45%)"></div>'
    if tint:
        inner += f'<div style="position:absolute;inset:0;background:{tint}"></div>'
    pid = nid("pd")
    if dust:
        dots = []
        for k in range(dust):
            x, y, s = R.uniform(0, 100), R.uniform(0, 100), R.uniform(2, 6)
            dots.append(f'<i id="{pid}_{k}" style="position:absolute;left:{x:.1f}%;top:{y:.1f}%;width:{s:.1f}px;height:{s:.1f}px;border-radius:50%;background:rgba(255,220,170,{R.uniform(.25,.7):.2f});filter:blur({R.uniform(0,1.5):.1f}px)"></i>')
        inner += "".join(dots)
    inner += '<div style="position:absolute;right:56px;top:118px;font:700 24px Malgun;color:rgba(233,220,196,.55);letter-spacing:.1em" data-layout-ignore>재현 그림</div>'
    cid = clip(inner, t0, dur, z=1)
    s0, s1, x0, x1, y0, y1 = move
    JS.append(f'tl.fromTo("#{bg}",{{scale:{s0},xPercent:{x0},yPercent:{y0}}},{{scale:{s1},xPercent:{x1},yPercent:{y1},duration:{dur:.2f},ease:"sine.inOut"}},{t0:.3f});')
    if fg:
        p = fg[1]
        JS.append(f'tl.fromTo("#{f}",{{scale:{s0 * 1.02},xPercent:{x0 * p},yPercent:{y0 * p}}},{{scale:{s1 * 1.06},xPercent:{x1 * p},yPercent:{y1 * p},duration:{dur:.2f},ease:"sine.inOut"}},{t0:.3f});')
    if flick:
        t = t0; seq = []
        while t < t0 + dur:
            seq.append(f'tl.set("#{fl}",{{opacity:{R.uniform(.55,1):.2f}}},{t:.2f});'); t += R.uniform(.07, .16)
        JS.append("".join(seq))
    for k in range(dust):
        JS.append(f'tl.to("#{pid}_{k}",{{y:{-R.uniform(40,160):.0f},x:{R.uniform(-40,40):.0f},duration:{dur:.2f},ease:"none"}},{t0:.3f});')
    # 들어올 때 빛 흐림이 걷힘
    JS.append(f'tl.fromTo("#{cid}",{{filter:"blur(10px) brightness(1.6)"}},{{filter:"blur(0px) brightness(1)",duration:0.35,ease:"expo.out"}},{t0:.3f});')
    return cid


def text(t0, dur, html, style, z=20, enter="blur"):
    i = nid("tx")
    cid = clip(f'<div id="{i}" style="position:absolute;{style}">{html}</div>', t0, dur, z=z)
    if enter == "blur":
        JS.append(f'tl.fromTo("#{i}",{{opacity:0,filter:"blur(8px)"}},{{opacity:1,filter:"blur(0px)",duration:0.25,ease:"power4.out"}},{t0:.3f});')
    return i


def typewriter(t0, t1, s, style, z=21, sound=True):
    i = nid("tw"); spans = "".join(f'<span style="opacity:0">{c}</span>' for c in s)
    clip(f'<div id="{i}" style="position:absolute;{style}">{spans}</div>', t0, t1 - t0, z=z)
    n = len(s); per = min(0.06, 0.9 / max(1, n))
    for k, c in enumerate(s):
        JS.append(f'tl.set("#{i} span:nth-child({k + 1})",{{opacity:1}},{t0 + k * per:.3f});')
        if sound and c.strip() and k % 2 == 0: SFX.append(("type", t0 + k * per))
    return i


def stamp(t, dur, label, x, y, size=78, rot=-10, color="#a3171b"):
    i = nid("st")
    clip(f'<div id="{i}" style="position:absolute;left:{x}px;top:{y}px;transform-origin:50% 50%;padding:14px 34px;border:7px solid {color};border-radius:12px;color:{color};'
         f'font:700 {size}px Malgun;letter-spacing:.08em;opacity:0;mix-blend-mode:multiply">{label}</div>', t, dur, z=40)
    JS.append(f'tl.fromTo("#{i}",{{opacity:0,scale:2.4,rotation:{rot - 8}}},{{opacity:.92,scale:1,rotation:{rot},duration:0.16,ease:"power4.in"}},{t:.3f});')
    shake(t + 0.16); SFX.append(("thud", t + 0.15))
    return i


def shake(t):
    JS.append(f'tl.to("#cam",{{keyframes:[{{x:14,y:-9,duration:.04}},{{x:-11,y:7,duration:.04}},{{x:7,y:-4,duration:.05}},{{x:-3,y:2,duration:.05}},{{x:0,y:0,duration:.06}}]}},{t:.3f});')


def flash(t, color="255,240,220", peak=.85):
    i = nid("fx"); clip(f'<div id="{i}" style="position:absolute;inset:0;background:rgb({color});opacity:0"></div>', t - 0.1, 0.6, z=60)
    JS.append(f'tl.to("#{i}",{{keyframes:[{{opacity:{peak},duration:.08}},{{opacity:0,duration:.35,ease:"power2.out"}}]}},{t:.3f});')


def whip(t):   # 다음 장면이 휙 들어옴: 카메라 흐림 + 소리
    JS.append(f'tl.fromTo("#cam",{{filter:"blur(0px)"}},{{immediateRender:false,keyframes:[{{filter:"blur(18px)",duration:.12}},{{filter:"blur(0px)",duration:.16}}]}},{t - 0.12:.3f});')
    SFX.append(("whoosh", t))


def leak(t, dur=1.2):
    i = nid("lk")
    clip(f'<div id="{i}" style="position:absolute;inset:-20%;mix-blend-mode:screen;opacity:0;background:radial-gradient(ellipse 40% 70% at 20% 50%,rgba(255,190,120,.9),rgba(255,90,40,.4) 40%,transparent 70%)"></div>', t, dur, z=55)
    JS.append(f'tl.fromTo("#{i}",{{opacity:0,xPercent:-30}},{{keyframes:[{{opacity:.9,xPercent:0,duration:{dur * .4:.2f}}},{{opacity:0,xPercent:30,duration:{dur * .6:.2f}}}]}},{t:.3f});')


def ink(t, cx, cy, r, dur, z=12, color="#7a0d10"):
    i = nid("ink")
    clip(f'<svg style="position:absolute;inset:0" width="{W}" height="{H}"><defs><filter id="{i}f"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="3" seed="4"/>'
         f'<feDisplacementMap in="SourceGraphic" scale="55"/><feGaussianBlur stdDeviation="1.2"/></filter></defs>'
         f'<circle id="{i}" cx="{cx}" cy="{cy}" r="1" fill="{color}" opacity=".78" filter="url(#{i}f)" style="mix-blend-mode:multiply"/></svg>', t, dur, z=z)
    JS.append(f'tl.fromTo("#{i}",{{attr:{{r:1}}}},{{attr:{{r:{r}}},duration:1.6,ease:"power2.out"}},{t:.3f});')


def subtitle(b):
    if not b.get("sub", True): return
    i = nid("sb")
    clip(f'<div id="{i}" style="position:absolute;left:50%;bottom:64px;transform:translateX(-50%);max-width:1500px;padding:12px 30px;border-radius:10px;background:rgba(8,8,12,.62);'
         f'color:#f3eee4;font:700 42px/1.45 Malgun;text-align:center;letter-spacing:-.01em;word-break:keep-all">{b["t"]}</div>', b["t0"], b["t1"] - b["t0"] - 0.05, z=50)




def page(total):
    grain = "".join(f'tl.set("#grain",{{backgroundPosition:"{R.randint(0,300)}px {R.randint(0,300)}px"}},{t / 12:.3f});' for t in range(int(total * 12)))
    flick = "".join(f'tl.set("#flick",{{opacity:{R.uniform(0,.07):.3f}}},{t / 8:.3f});' for t in range(int(total * 8)))
    return f"""<!doctype html>
<html lang="ko"><head><meta charset="UTF-8"><meta name="viewport" content="width=1920, height=1080">
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
@font-face{{font-family:Malgun;src:url(assets/fonts/malgunbd.ttf)}}
@font-face{{font-family:Batang;src:url(assets/fonts/batang.ttc)}}
*{{margin:0;padding:0;box-sizing:border-box}} html,body{{width:1920px;height:1080px;overflow:hidden;background:#000}}
#root{{position:relative;width:1920px;height:1080px;overflow:hidden;background:#000}}
#cam{{position:absolute;inset:0}}
#grain{{position:absolute;inset:0;z-index:70;pointer-events:none;opacity:.16;mix-blend-mode:overlay;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence baseFrequency='.85' numOctaves='2' seed='5'/></filter><rect width='300' height='300' filter='url(%23n)'/></svg>")}}
#vig{{position:absolute;inset:0;z-index:69;pointer-events:none;background:radial-gradient(ellipse at center,transparent 55%,rgba(0,0,0,.6) 100%)}}
#flick{{position:absolute;inset:0;z-index:68;pointer-events:none;background:#000;opacity:0}}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{total:.2f}" data-width="1920" data-height="1080">
<svg width="0" height="0" style="position:absolute"><defs>{"".join(DEFS)}</defs></svg>
<div id="cam" data-layout-allow-overflow data-layout-allow-overlap>
{chr(10).join(HTML)}
</div>
<div id="grain"></div><div id="vig"></div><div id="flick"></div>
<audio id="vo" class="clip" src="assets/vo.wav" data-start="0" data-duration="{total:.2f}" data-track-index="90"></audio>
<audio id="fx" class="clip" src="assets/sfx.wav" data-start="0" data-duration="{total:.2f}" data-track-index="91" data-volume="0.55"></audio>
</div>
<script>
const tl = gsap.timeline({{paused:true}});
{chr(10).join(JS)}
{grain}
{flick}
window.__timelines["main"] = tl;
tl.seek(0);
</script></body></html>"""
