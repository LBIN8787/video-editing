"""소현세자 샘플 v2 — HyperFrames 한 장면(index.html)을 대본 박자·낱말 시각에서 생성.
레퍼런스 측정(docs/76): 화면이 멈추는 순간 없음, 문장마다 장면 교체, 분위기 층(입자·빛·필름), 결정적 순간에만 큰 글자."""
import asyncio, json, random, shutil, subprocess
from pathlib import Path
import edge_tts
from PIL import Image

EP = Path(r"G:\내 드라이브\ytflow\영상\20261126-history-sohyeon")
HF = EP / "hf"; AS = HF / "assets"; (AS / "fonts").mkdir(parents=True, exist_ok=True)
WORK = Path(__file__).parent / "hfwork"; WORK.mkdir(exist_ok=True)
VOICE, RATE = "ko-KR-InJoonNeural", "-12%"
W, H = 1920, 1080

# ---------------------------------------------------------------- 대본 박자 (v2 콜드 오픈 + 사건 개요 + 마지막)
BEATS = [
 dict(t="1645년 4월, 창경궁 환경당.", pause=0.5),
 dict(t="촛불 아래, 세상을 떠난 사람의 몸을 씻기고 옷을 입히는 염습이 시작됩니다.", pause=0.3),
 dict(t="누워 있는 사람은 조선의 왕세자. 서른셋.", pause=0.5),
 dict(t="그 방에 들어갔던 종친 집안 사람 하나가, 훗날 이렇게 전했습니다.", pause=0.9),
 dict(t="온몸이 전부 검은빛이었고, 이목구비의 일곱 구멍에서는 모두 선혈이 흘러나왔다.", pause=0.5, sub=False),
 dict(t="마치 약물에 중독되어 죽은 사람과 같았다.", pause=1.1, sub=False),
 dict(t="나라의 공식 역사, 조선왕조실록에 남은 문장입니다.", pause=0.4),
 dict(t="그리고 이 죽음은, 380년이 넘도록 풀리지 않았습니다.", pause=1.2, sub=False),
 dict(t="사건을 먼저 정리해 보겠습니다.", pause=0.2),
 dict(t="죽은 사람. 소현세자. 왕 인조의 맏아들, 다음 왕이 될 사람이었습니다.", pause=0.2),
 dict(t="때. 1645년 음력 4월 26일. 곳. 창경궁 환경당.", pause=0.2, sub=False),
 dict(t="청나라에서 8년을 지내고 돌아온 지 두 달 남짓. 4월 23일에 앓아눕고, 나흘째 되던 날 숨을 거둡니다.", pause=0.9),
 dict(t="1644년 가을, 베이징의 천문대에서 둥근 지구의를 받아 들었던 세자.", pause=0.4),
 dict(t="그날 환경당에서 그를 데려간 것은 병이었을까요, 독이었을까요.", pause=0.8),
 dict(t="여러분의 판정은 어느 쪽입니까.", pause=2.6, sub=False),
]


async def tts_all():
    for i, b in enumerate(BEATS):
        mp3 = WORK / f"b{i:02d}.mp3"; js = WORK / f"b{i:02d}.json"
        if not (mp3.exists() and js.exists()):
            c = edge_tts.Communicate(b["t"], VOICE, rate=RATE, boundary="WordBoundary")
            words, audio = [], bytearray()
            async for ch in c.stream():
                if ch["type"] == "audio": audio += ch["data"]
                elif ch["type"] == "WordBoundary": words.append([ch["text"], ch["offset"] / 1e7, ch["duration"] / 1e7])
            mp3.write_bytes(bytes(audio)); js.write_text(json.dumps(words, ensure_ascii=False), encoding="utf-8")
        b["words"] = json.loads(js.read_text(encoding="utf-8"))
        b["dur"] = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp3)], capture_output=True, text=True).stdout)


def timing():
    t = 0.6   # 첫 0.6초 검은 화면에서 열림
    for b in BEATS:
        b["t0"] = t; b["t1"] = t + b["dur"] + b["pause"]; t = b["t1"]
    return t


def w(i, word, k=0):
    """박자 i 에서 낱말(앞부분 일치) 의 시작 시각 (절대)."""
    hits = [x for x in BEATS[i]["words"] if x[0].startswith(word)]
    return BEATS[i]["t0"] + (hits[k][1] if hits else 0)


# ---------------------------------------------------------------- 자산
def assets():
    srcs = {"A1": EP / "samples" / "A1_yeomseup.png", "A3": EP / "samples" / "A3_observatory.png",
            "N10": EP / "art" / "N10_scribe.png", "N11": EP / "art" / "N11_injo.png", "N5": EP / "art" / "N5_return.png",
            "N6": EP / "art" / "N6_physician.png", "N2": EP / "art" / "N2_diplomacy.png"}
    for k, p in srcs.items():
        out = AS / f"{k}.jpg"
        if not out.exists():
            Image.open(p).convert("RGB").resize((2400, 1350)).save(out, quality=90)
    for f in ["malgunbd.ttf", "batang.ttc"]:
        if not (AS / "fonts" / f).exists(): shutil.copy(rf"C:\Windows\Fonts\{f}", AS / "fonts" / f)
    # 목소리 한 줄
    lst = WORK / "vo.txt"; parts = []
    for i, b in enumerate(BEATS):
        wv = WORK / f"p{i:02d}.wav"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(WORK / f"b{i:02d}.mp3"), "-af", f"apad=pad_dur={b['pause']}", "-ar", "48000", "-ac", "2", str(wv)], check=True)
        parts.append(wv)
    lead = WORK / "lead.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", "0.6", str(lead)], check=True)
    lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in [lead] + parts), encoding="utf-8")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), str(AS / "vo.wav")], check=True)


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
HTML, JS, SFX = [], [], []
_id = [0]


def nid(p="e"):
    _id[0] += 1; return f"{p}{_id[0]}"


def clip(inner, t0, dur, z=1, extra=""):
    i = nid("c")
    HTML.append(f'<div id="{i}" class="clip" data-start="{t0:.3f}" data-duration="{dur:.3f}" data-track-index="{z}" style="position:absolute;inset:0;z-index:{z};{extra}">{inner}</div>')
    return i


def shot(img, t0, dur, crop=(0, 0, 1, 1), move=(1.0, 1.08, 0, -2, 0, 0), fg=None, flick=None, dust=0, tint=None):
    """그림의 한 부분(crop, 0~1)을 화면 가득 → 카메라 move=(s0,s1,x0%,x1%,y0%,y1%). fg=(마스크, 배율) 앞층 시차."""
    cx, cy, cw, ch = crop
    sc = 1 / cw
    base = f"position:absolute;left:{-cx * sc * 100:.2f}%;top:{-cy * sc * 100:.2f}%;width:{sc * 100:.2f}%;height:{(1 / ch) * 100:.2f}%;object-fit:cover"
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


# ---------------------------------------------------------------- 장면들
def build():
    B = BEATS
    def T(i): return B[i]["t0"]
    def E(i): return B[i]["t1"]
    # 0: 촛불 클로즈업 → 날짜 타자기
    shot("A1", 0.6, E(0) - 0.6, crop=(0.55, 0.62, 0.32, 0.32), move=(1.0, 1.12, 0, 0, 0, -3), flick=(55, 45), dust=26)
    typewriter(T(0) + 0.1, E(0), "1645년 4월 · 창경궁 환경당", "left:96px;top:86px;font:700 40px Malgun;color:#e9dcc4;letter-spacing:.06em;text-shadow:0 2px 8px #000")
    clip('<div style="position:absolute;right:90px;top:92px;font:700 26px Malgun;color:rgba(233,220,196,.6)">재현</div>', 0.6, E(13) - 0.6, z=45)
    # 1: 넓게(앞층 시차) → 흰 베와 두 여인
    mid = w(1, "세상을")
    shot("A1", T(1), mid - T(1), move=(1.06, 1.12, 2, -2, 0, 0), fg=("linear-gradient(90deg,#000 0%,#000 30%,transparent 42%)", 2.6), flick=(77, 63), dust=18)
    shot("A1", mid, E(1) - mid, crop=(0.3, 0.22, 0.55, 0.55), move=(1.0, 1.08, -2, 2, 0, 0), flick=(37, 72), dust=14)
    # 2: 덮인 몸 클로즈업 → '서른셋'
    shot("A1", T(2), E(2) - T(2), crop=(0.33, 0.5, 0.42, 0.42), move=(1.0, 1.14, 0, 0, 0, 0), flick=(60, 85), tint="radial-gradient(circle at 50% 50%,transparent 30%,rgba(0,0,0,.55) 75%)")
    t33 = w(2, "서른셋")
    text(t33, E(2) - t33, "33", "right:180px;top:300px;font:400 220px Batang;color:rgba(240,228,205,.85);letter-spacing:-.02em")
    SFX.append(("hit", t33))
    # 3: 문간의 종친 → 어두워짐
    shot("A1", T(3), E(3) - T(3), crop=(0.0, 0.0, 0.46, 0.46), move=(1.0, 1.1, 0, 2, 0, 0), flick=(95, 95))
    JS.append(f'tl.to("#cam",{{filter:"brightness(0.15)",duration:0.6,ease:"power2.in"}},{E(3) - 0.6:.3f});tl.set("#cam",{{filter:"brightness(1)"}},{E(3):.3f});')
    # 4-5: 실록 종이 — 말하는 낱말마다 줄이 생기고, '중독되어'에 붉은 잉크
    paper = ('<div id="pp" style="position:absolute;left:230px;top:120px;width:1460px;height:820px;border-radius:6px;'
             'background:radial-gradient(ellipse at 30% 20%,#e9dcbc,#cdb98d 75%,#a88f63);box-shadow:0 40px 90px rgba(0,0,0,.7)">'
             '<svg width="1460" height="820" style="position:absolute;inset:0;opacity:.35"><filter id="pn"><feTurbulence baseFrequency=".9" numOctaves="2" seed="2"/><feColorMatrix values="0 0 0 0 .3 0 0 0 0 .22 0 0 0 0 .12 0 0 0 .6 0"/></filter><rect width="1460" height="820" filter="url(#pn)"/></svg></div>')
    clip('<div style="position:absolute;inset:0;background:#0c0b0a"></div>' + paper, T(4), E(5) - T(4), z=2)
    JS.append(f'tl.fromTo("#pp",{{rotationX:12,rotationY:-8,scale:.92,y:40,transformPerspective:1400}},{{rotationX:2,rotationY:3,scale:1.03,y:0,duration:{E(5) - T(4):.2f},ease:"sine.out"}},{T(4):.3f});')
    whip(T(4)); SFX.append(("hit", T(4)))
    text(T(4) + 0.1, E(5) - T(4) - 0.1, "仁祖實錄 卷四十六 · 인조 23년(1645) 6월 27일", "left:300px;top:170px;font:700 30px Batang;color:#6b5033")
    lines = [("온몸이 전부 검은빛이었고,", 4, "온몸이"), ("이목구비의 일곱 구멍에서는", 4, "이목구비의"), ("모두 선혈이 흘러나왔다.", 4, "모두"), ("마치 약물에 중독되어 죽은 사람과 같았다.", 5, "마치")]
    for k, (ln, bi, wd) in enumerate(lines):
        t = w(bi, wd)
        i = nid("ln"); words = "".join(f'<span style="opacity:0;filter:blur(6px)">{x} </span>' for x in ln.split())
        clip(f'<div id="{i}" style="position:absolute;left:320px;top:{270 + k * 120}px;font:400 64px Batang;color:#2a1d14">{words}</div>', t, E(5) - t, z=22)
        for j, _ in enumerate(ln.split()):
            JS.append(f'tl.to("#{i} span:nth-child({j + 1})",{{opacity:1,filter:"blur(0px)",duration:.14}},{t + j * 0.33:.3f});')
    tdok = w(5, "중독되어")
    ink(tdok, 720, 680, 120, E(5) - tdok)
    i = nid("ul"); clip(f'<svg style="position:absolute;inset:0" width="{W}" height="{H}"><line id="{i}" x1="590" y1="700" x2="850" y2="700" stroke="#9a1015" stroke-width="9" stroke-linecap="round" stroke-dasharray="260" stroke-dashoffset="260"/></svg>', tdok, E(5) - tdok, z=30)
    JS.append(f'tl.to("#{i}",{{attr:{{"stroke-dashoffset":0}},duration:.4,ease:"power2.out"}},{tdok + .1:.3f});')
    stamp(E(5) - 1.0, 1.0, "기록", 1380, 760, size=64)
    # 6: 실록을 쓰는 사관(시차·등불) + 이름표
    shot("N10", T(6), E(6) - T(6), move=(1.05, 1.13, -2, 2, 0, -1), fg=("linear-gradient(90deg,transparent 30%,#000 45%,#000 75%,transparent 85%)", 2.0), flick=(52, 40), dust=20)
    leak(T(6) - 0.3)
    i = text(w(6, "조선왕조실록"), E(6) - w(6, "조선왕조실록"), '<span style="font:700 46px Malgun;color:#f1e6cf">조선왕조실록</span><br><span style="font:700 26px Malgun;color:rgba(241,230,207,.7)">나라가 펴낸 공식 역사</span>',
             "left:110px;top:640px;padding:18px 28px;border-left:6px solid #a3171b;background:rgba(0,0,0,.45)")
    # 7: 사건 파일 — 1645 → 2026 카운트, '미해결' 도장
    clip('<div style="position:absolute;inset:0;background:radial-gradient(circle at 50% 40%,#2a2722,#0b0a09 80%)"></div>'
         '<div id="fold" style="position:absolute;left:360px;top:110px;width:1200px;height:860px;background:linear-gradient(#d4bf8e,#c2a873);border-radius:8px 8px 4px 4px;box-shadow:0 30px 80px rgba(0,0,0,.8)">'
         '<div style="position:absolute;left:60px;top:60px;font:700 36px Batang;color:#5a4128;letter-spacing:.2em">사건 파일 · 001</div>'
         '<div style="position:absolute;left:60px;top:150px;font:700 96px Batang;color:#24180f">소현세자의 죽음</div>'
         '<div style="position:absolute;left:60px;top:300px;width:1080px;height:3px;background:#7a5c38"></div></div>', T(7), E(7) - T(7), z=2)
    whip(T(7))
    JS.append(f'tl.fromTo("#fold",{{y:900,rotation:4}},{{y:0,rotation:-1.5,duration:.55,ease:"expo.out"}},{T(7):.3f});')
    tc = w(7, "380년이")
    cnt = nid("ct")
    clip(f'<div style="position:absolute;left:420px;top:540px;font:700 48px Malgun;color:#5a4128">1645 →</div>'
         f'<div style="position:absolute;left:640px;top:470px;font:400 150px Batang;color:#24180f"><span id="{cnt}">1645</span></div>', tc - 0.6, E(7) - tc + 0.6, z=25)
    JS.append(f'(function(){{var o={{v:1645}};tl.to(o,{{v:2026,duration:1.3,ease:"power2.inOut",onUpdate:function(){{document.getElementById("{cnt}").textContent=Math.round(o.v)}}}},{tc - 0.5:.3f});}})();')
    for k in range(10): SFX.append(("tick", tc - 0.5 + k * 0.13))
    i = text(tc + 0.9, E(7) - tc - 0.9, "380년 넘게 풀리지 않음", "left:420px;top:700px;font:700 54px Malgun;color:#a3171b")
    stamp(E(7) - 1.3, 1.3, "미해결", 1120, 640, size=110, rot=-14)
    flash(E(7) - 1.12, peak=.35)
    # 8-11: 증거판 — 사진이 핀으로 꽂히고 붉은 실, 마지막에 연표가 그려짐
    board = '<div style="position:absolute;inset:0;background:radial-gradient(circle at 50% 45%,#2b2a27,#121110 85%)"></div>'
    t8 = T(8); tEnd = E(11)
    clip(board + '<div style="position:absolute;left:0;right:0;top:40px;text-align:center;font:700 34px Batang;color:#cdb98d;letter-spacing:.4em">사 건 개 요</div>', t8, tEnd - t8, z=2)
    whip(t8)
    JS.append(f'tl.fromTo("#cam",{{scale:1.12}},{{immediateRender:false,scale:1.0,duration:{tEnd - t8:.2f},ease:"sine.inOut"}},{t8:.3f});tl.set("#cam",{{scale:1}},{tEnd:.3f});')
    def polaroid(img, crop, x, y, rot, t, cap, dur):
        i = nid("po"); cx, cy, cw, ch = crop; sc = 1 / cw
        clip(f'<div id="{i}" style="position:absolute;left:{x}px;top:{y}px;width:380px;padding:16px 16px 58px;background:#efe9dc;box-shadow:0 18px 40px rgba(0,0,0,.6);transform-origin:50% 0">'
             f'<div style="width:348px;height:260px;overflow:hidden;position:relative"><img src="assets/{img}.jpg" style="position:absolute;left:{-cx * sc * 100:.1f}%;top:{-cy * sc * 100:.1f}%;width:{sc * 100:.1f}%;height:{(1 / ch) * 100:.1f}%;object-fit:cover;filter:sepia(.35) contrast(1.05)"></div>'
             f'<div style="position:absolute;left:0;right:0;bottom:12px;text-align:center;font:700 26px Malgun;color:#2a2018">{cap}</div>'
             f'<i style="position:absolute;left:176px;top:-12px;width:28px;height:28px;border-radius:50%;background:radial-gradient(circle at 35% 35%,#e24a4a,#7a0d10)"></i></div>', t, dur, z=24)
        JS.append(f'tl.fromTo("#{i}",{{y:-120,opacity:0,rotation:{rot + 12}}},{{y:0,opacity:1,rotation:{rot},duration:.45,ease:"back.out(1.6)"}},{t:.3f});')
        SFX.append(("thud", t + 0.3))
    tp = w(9, "소현세자"); polaroid("A3", (0.0, 0.08, 0.5, 0.5), 160, 150, -5, tp, "소현세자 (1612~1645)", tEnd - tp)
    tk = w(9, "왕"); polaroid("N11", (0.3, 0.18, 0.4, 0.4), 620, 120, 4, tk, "아버지 · 인조", tEnd - tk)
    tt = w(10, "때"); polaroid("A1", (0.2, 0.25, 0.6, 0.6), 1100, 160, -3, tt, "창경궁 환경당", tEnd - tt)
    i = nid("str"); clip(f'<svg style="position:absolute;inset:0" width="{W}" height="{H}"><path id="{i}" d="M350 170 Q 560 300 810 140 T 1290 180" fill="none" stroke="#b0161b" stroke-width="5" stroke-dasharray="1200" stroke-dashoffset="1200"/></svg>', tk, tEnd - tk, z=26)
    JS.append(f'tl.to("#{i}",{{attr:{{"stroke-dashoffset":0}},duration:1.2,ease:"power2.inOut"}},{tk + .3:.3f});')
    td = w(10, "1645년"); text(td, E(10) - td + 0.1, "1645. 4. 26 (음력)", "left:1150px;top:470px;font:700 40px Malgun;color:#f1e6cf;background:#7a0d10;padding:8px 18px;transform:rotate(-3deg)")
    # 연표: 1637 → 1645.2.18 → 4.23 → 4.26
    t11 = T(11)
    i = nid("tl"); clip(f'<svg style="position:absolute;inset:0" width="{W}" height="{H}"><line id="{i}" x1="180" y1="640" x2="1740" y2="640" stroke="#e9dcc4" stroke-width="4" stroke-dasharray="1560" stroke-dashoffset="1560"/></svg>', t11, E(11) - t11, z=27)
    JS.append(f'tl.to("#{i}",{{attr:{{"stroke-dashoffset":0}},duration:.9,ease:"power2.out"}},{t11:.3f});')
    marks = [(200, "1637", "심양으로", w(11, "청나라에서")), (1240, "1645.2.18", "귀국", w(11, "돌아온")), (1480, "4.23", "앓아누움", w(11, "4월")), (1700, "4.26", "죽음", w(11, "나흘째"))]
    for x, top, bot, t in marks:
        i = nid("mk")
        clip(f'<div id="{i}"><i style="position:absolute;left:{x - 14}px;top:626px;width:28px;height:28px;border-radius:50%;background:{"#c11c22" if bot == "죽음" else "#e9dcc4"}"></i>'
             f'<div style="position:absolute;left:{x - 110}px;width:220px;top:560px;text-align:center;font:700 34px Malgun;color:#f1e6cf">{top}</div>'
             f'<div style="position:absolute;left:{x - 110}px;width:220px;top:670px;text-align:center;font:700 28px Malgun;color:rgba(241,230,207,.75)">{bot}</div></div>', t, E(11) - t, z=28)
        JS.append(f'tl.fromTo("#{i}",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.3,ease:"expo.out"}},{t:.3f});'); SFX.append(("tick", t))
    tb = w(11, "두"); i = nid("br")
    clip(f'<div id="{i}" style="position:absolute;left:1240px;top:700px;width:460px;height:24px;border:4px solid #c11c22;border-top:none"><div style="position:absolute;left:0;right:0;top:30px;text-align:center;font:700 34px Malgun;color:#ff6a5a">두 달 남짓</div></div>', tb, E(11) - tb, z=29)
    JS.append(f'tl.fromTo("#{i}",{{scaleX:0}},{{scaleX:1,duration:.4,ease:"power3.out",transformOrigin:"0 0"}},{tb:.3f});')
    # 12: 천문대 — 빛샘 전환, 앞층 시차(세자), 지구의 빛
    leak(T(12) - 0.4, 1.4); SFX.append(("whoosh", T(12)))
    shot("A3", T(12), E(12) - T(12), move=(1.04, 1.12, -1, 1, 0, -1), fg=("linear-gradient(90deg,#000 0%,#000 40%,transparent 52%)", 2.4), dust=30)
    g = nid("gl"); clip(f'<div id="{g}" style="position:absolute;left:36%;top:52%;width:380px;height:380px;margin:-190px;border-radius:50%;mix-blend-mode:screen;background:radial-gradient(circle,rgba(255,200,120,.55),transparent 65%)"></div>', T(12), E(12) - T(12), z=6)
    JS.append(f'tl.fromTo("#{g}",{{opacity:0,scale:.6}},{{opacity:1,scale:1.15,duration:{E(12) - T(12):.2f},ease:"sine.inOut"}},{T(12):.3f});')
    typewriter(T(12) + 0.1, E(12), "1644년 가을 · 베이징 천문대", "left:96px;top:86px;font:700 40px Malgun;color:#f6e7c8;letter-spacing:.06em;text-shadow:0 2px 8px #000")
    # 13: 화면 둘로 — 병? / 독?
    t13 = T(13); half = 'position:absolute;top:0;bottom:0;overflow:hidden'
    i = nid("sp")
    clip(f'<div id="{i}a" style="{half};left:0;width:50%"><img src="assets/A3.jpg" style="position:absolute;left:-30%;top:0;height:100%;filter:grayscale(.7) brightness(.7)"></div>'
         f'<div id="{i}b" style="{half};left:50%;width:50%"><img src="assets/A1.jpg" style="position:absolute;left:-60%;top:0;height:100%;filter:brightness(.6)"></div>'
         f'<div style="position:absolute;left:50%;top:0;bottom:0;width:4px;background:#c11c22"></div>', t13, E(13) - t13, z=3)
    JS.append(f'tl.fromTo("#{i}a",{{xPercent:-100}},{{xPercent:0,duration:.5,ease:"expo.out"}},{t13:.3f});tl.fromTo("#{i}b",{{xPercent:100}},{{xPercent:0,duration:.5,ease:"expo.out"}},{t13:.3f});')
    SFX.append(("whoosh", t13))
    tb1 = w(13, "병이었을까요"); tb2 = w(13, "독이었을까요")
    text(tb1, E(13) - tb1, "병?", "left:330px;top:380px;font:700 170px Malgun;color:#f1e6cf")
    text(tb2, E(13) - tb2, "독?", "left:1290px;top:380px;font:700 170px Malgun;color:#e0373c")
    SFX.append(("hit", tb2))
    # 14: 판정 — 검은 화면, 잉크, 도장
    t14 = T(14)
    clip('<div style="position:absolute;inset:0;background:#050505"></div>', t14, E(14) - t14, z=2)
    text(t14 + 0.2, E(14) - t14 - 0.2, "여러분의 판정은?", "left:0;right:0;top:330px;text-align:center;font:700 64px Malgun;color:#e9e2d4")
    ink(t14 + 1.3, 960, 640, 260, E(14) - t14 - 1.3, z=8, color="#6e0b0e")
    stamp(t14 + 1.6, E(14) - t14 - 1.6, "판정 : 미해결", 690, 560, size=96, rot=-6, color="#d8c9a8")
    for b in BEATS: subtitle(b)


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


async def main():
    await tts_all()
    total = timing() + 0.2
    assets()
    build()
    sfx(SFX, total)
    (HF / "index.html").write_text(page(total), encoding="utf-8")
    print("total", round(total, 1), "s, clips", len(HTML), "js", len(JS), "sfx", len(SFX))


asyncio.run(main())
