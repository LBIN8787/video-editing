"""화풍·연출 갤러리 — '화풍목록 보여줘' (skills/looks-gallery).

두 축을 나눠 보여 줍니다 (2026-11-20 사용자: "화풍 스타일이랑 연출은 아예 다른 분야잖아 … 모션그래픽에 특정 연출을 섞을 수 있는거고,
연출에 따라서 그래픽은 모션그래픽이지만 연출이 달라서 아예 달라질 수도 있는거니까").
  화풍(styles/looks.yaml)  = 어떻게 '보이나' — 색·선·질감·그림체. 같은 한 장면을 화풍마다 (정지 화면)
  연출(styles/techniques.yaml) = 어떻게 '움직이고 보여 주나' — 튀어나오기·그려지기·확대·전환 … 연출마다 움직이는 예시,
                                위에서 고른 화풍으로 다시 칠해짐 → 아무 화풍 × 아무 연출 조합을 바로 봄
"""
from __future__ import annotations

import html as H
import json
from pathlib import Path

import yaml

from . import looks

ROOT = Path(__file__).resolve().parents[2]
TECH = ROOT / "styles" / "techniques.yaml"
TSTATUS = {"have": ("구현됨", "ok"), "partial": ("비슷한 것 있음", "av"), "candidate": ("후보", "trial"), "hold": ("보류", "hold")}


# ---------------------------------------------------------------- 그림 조각 (SVG, 화풍 색은 CSS 변수)
def jar(x, y, w=22, i=0, cls=""):
    fill = "var(--acc)" if i % 3 == 0 else "var(--ink)"
    op = 1 if i % 3 == 0 else .72
    return (f'<g class="j {cls}" style="--i:{i}" transform="translate({x} {y})"><g class="jj">'
            f'<rect x="0" y="{-w * 1.1:.1f}" width="{w}" height="{w * 1.1:.1f}" rx="{w * .2:.1f}" style="fill:{fill};opacity:{op}"/>'
            f'<rect x="-2" y="{-w * 1.4:.1f}" width="{w + 4}" height="{w * .32:.1f}" rx="2" style="fill:var(--card);stroke:var(--ink);stroke-width:1.2"/></g></g>')


def cart(x, y, cls="cart"):
    return (f'<g class="{cls}" transform="translate({x} {y})"><path d="M-22 -26 h8 l6 22 h30 l6 -16 h-38" style="fill:none;stroke:var(--acc);stroke-width:4;stroke-linejoin:round"/>'
            f'<circle cx="-4" cy="4" r="4" style="fill:var(--acc)"/><circle cx="20" cy="4" r="4" style="fill:var(--acc)"/></g>')


def person(x, y, i=0, cls="pp"):
    return f'<g class="{cls}" style="--i:{i}" transform="translate({x} {y})"><circle r="5" cy="-9"/><rect x="-6" y="-3" width="12" height="13" rx="5"/></g>'


def T(txt, cls="tt", x=16, y=28, size=20):
    return f'<text class="{cls}" x="{x}" y="{y}" style="font-size:{size}px">{txt}</text>'


# ---------------------------------------------------------------- 화풍 카드 — 같은 한 장면 (정지)
def look_scene() -> str:
    shelf = "".join(jar(150 + (i % 6) * 26, 92 + (i // 6) * 34, 18, i) for i in range(12))
    bars = ('<rect x="16" y="120" width="96" height="12" style="fill:var(--acc)"/><rect x="16" y="140" width="64" height="12" style="fill:var(--ink);opacity:.8"/>'
            '<text x="118" y="131" class="lb">60%</text><text x="86" y="151" class="lb">40%</text>')
    ppl = "".join(person(26 + k * 18, 100, k, "pp on" if k < 2 else "pp") for k in range(5))
    return (f'<svg viewBox="0 0 320 180" class="scene">{T("고를 게 많으면<tspan class=acc>?</tspan>")}{shelf}{cart(270, 160, "cartS")}'
            f'{bars}{ppl}<g transform="translate(232 18)"><rect width="74" height="20" rx="4" style="fill:var(--acc)"/>'
            f'<text x="37" y="14" class="chip">멈춘 손님</text></g>'
            f'<path d="M120 60 C 140 40, 160 40, 176 52" class="arr"/></svg>')


# ---------------------------------------------------------------- 연출 예시 — 기법마다 하나의 움직임 (.go 가 붙으면 처음부터)
def demo(tid: str) -> str:
    J = lambda n, y=118, w=20, gap=30, x0=40, cls="": "".join(jar(x0 + (i % 8) * gap, y + (i // 8) * 40, w, i, cls) for i in range(n))
    d = {
        "split-reveal": f'<svg viewBox="0 0 320 180"><text class="big" x="24" y="88"><tspan class="w" style="--i:0">고를 게</tspan> <tspan class="w" style="--i:1">많으면</tspan></text><text class="big" x="24" y="128"><tspan class="w acc" style="--i:2">덜 산다?</tspan></text></svg>',
        "scramble": f'<svg viewBox="0 0 320 180">{T("발표된 숫자", "sm", 24, 52, 14)}<text class="big" x="24" y="112" data-scramble="631억 원">631억 원</text></svg>',
        "count-up": f'<svg viewBox="0 0 320 180">{T("멈춘 손님", "sm", 24, 52, 14)}<text class="huge acc" x="24" y="128" data-count="60" data-suffix="%">60%</text></svg>',
        "rough-highlight": '<svg viewBox="0 0 320 180"><rect x="20" y="30" width="280" height="120" rx="6" class="paper"/>'
                           '<rect class="hl" x="34" y="78" width="210" height="16"/>'
                           + "".join(f'<rect x="36" y="{52 + k * 22}" width="{230 - (k % 2) * 40}" height="6" rx="3" class="line"/>' for k in range(4))
                           + '<path class="ul" d="M36 104 C 100 110, 170 100, 240 106"/></svg>',
        "draw-on": f'<svg viewBox="0 0 320 180">{cart(60, 132, "cartS")}<path class="draw" d="M86 120 C 140 40, 200 150, 256 84"/><g transform="translate(262 84)"><path d="M-18 6 v-18 l18 -14 l18 14 v18 z" class="house"/></g></svg>',
        "morph": '<svg viewBox="0 0 320 180"><text class="sm" x="24" y="40">같은 것이 다른 모습으로</text><rect class="mph" x="125" y="62" width="70" height="70"/></svg>',
        "stagger": f'<svg viewBox="0 0 320 180">{J(16, 96, 20, 30, 40, "st")}</svg>',
        "motion-path": '<svg viewBox="0 0 320 180"><path class="track" d="M30 140 C 100 20, 220 180, 290 50"/><circle class="mover" r="10"/></svg>',
        "match-move": f'<svg viewBox="0 0 320 180"><g class="mmA">{J(6, 120, 18, 40, 50)}</g><text class="sm mmT" x="24" y="40">이 병 하나로</text><g class="mmJ">{jar(130, 118, 18, 0)}</g></svg>',
        "j-l-cut": '<svg viewBox="0 0 320 180"><text class="sm" x="16" y="34">화면</text><rect x="60" y="22" width="120" height="18" class="clipA"/><rect x="180" y="22" width="120" height="18" class="clipB"/>'
                   '<text class="sm" x="16" y="74">소리</text><rect x="60" y="62" width="96" height="18" class="clipA"/><rect x="156" y="62" width="144" height="18" class="clipB"/>'
                   '<path d="M156 52 v40" class="cutline"/><text class="sm acc" x="120" y="112">J컷: 다음 소리가 먼저</text><rect class="play" x="60" y="18" width="2" height="66"/></svg>',
        "xfade-pack": f'<svg viewBox="0 0 320 180"><g class="xa">{J(8, 120, 20, 32, 40)}</g><g class="xb"><rect width="320" height="180" class="bgA"/>{T("다음 장으로", "big", 70, 100, 26)}</g></svg>',
        "zoom-into": f'<svg viewBox="0 0 320 180"><g class="zi">{J(8, 120, 20, 32, 40)}</g></svg>',
        "whip-pan": f'<svg viewBox="0 0 320 180"><g class="wp">{J(8, 120, 20, 32, 40)}</g></svg>',
        "gl-transitions": '<svg viewBox="0 0 320 180"><g class="gl">' + "".join(f'<rect x="{x * 40}" y="{y * 45}" width="40" height="45" style="--i:{x + y}" class="tile"/>' for x in range(8) for y in range(4)) + '</g></svg>',
        "parallax-photo": f'<svg viewBox="0 0 320 180"><g class="px1"><rect x="-20" y="20" width="360" height="90" class="far"/></g><g class="px2">{person(160, 120)}{person(190, 124)}</g><g class="px3">{J(10, 176, 22, 34, 10)}</g></svg>',
        "pull-back": f'<svg viewBox="0 0 320 180"><g class="pb">{J(24, 70, 20, 34, 30)}</g></svg>',
        "bar-race": '<svg viewBox="0 0 320 180">' + "".join(f'<g class="br br{k}"><rect x="70" y="-9" height="18" class="bar"/><text x="16" y="5" class="sm">{n}</text></g>' for k, n in enumerate(["딸기", "포도", "사과"])) + '</svg>',
        "chart-morph": '<svg viewBox="0 0 320 180"><g class="cmBar">' + "".join(f'<rect x="{60 + k * 50}" y="{150 - h}" width="34" height="{h}" class="bar"/>' for k, h in enumerate([60, 100, 40, 80])) + '</g><path class="cmLine" d="M77 90 L127 50 L177 110 L227 70"/></svg>',
        "split-screen": f'<svg viewBox="0 0 320 180"><g class="ssL">{J(8, 110, 14, 18, 10)}{J(8, 150, 14, 18, 10)}<text class="sm" x="12" y="40">24가지</text></g><path d="M160 10 v160" class="divider"/><g class="ssR">{J(6, 130, 18, 24, 172)}<text class="sm" x="172" y="40">6가지</text></g></svg>',
        "spotlight": f'<svg viewBox="0 0 320 180"><g class="spot">{"".join(jar(40 + i * 40, 118, 20, i, "sp" if i == 3 else "") for i in range(7))}</g></svg>',
        "card-state": '<svg viewBox="0 0 320 180"><g class="cs" transform="translate(80 50)"><rect width="160" height="80" rx="10" class="cardr"/><circle cx="28" cy="40" r="12" class="dot"/>'
                      '<text x="52" y="46" class="sm s1">고르는 중</text><text x="52" y="46" class="sm s2">장바구니에 담음</text></g></svg>',
        "link-break": '<svg viewBox="0 0 320 180"><circle cx="70" cy="90" r="22" class="node"/><circle cx="250" cy="90" r="22" class="node"/><path d="M92 90 H228" class="link"/><path d="M92 90 H228" class="broken"/><g class="xmark" transform="translate(160 90)"><path d="M-10 -10 L10 10 M10 -10 L-10 10"/></g></svg>',
        "footage-chips": '<svg viewBox="0 0 320 180"><image href="{{FRAME}}" x="0" y="0" width="320" height="180" preserveAspectRatio="xMidYMid slice"/>'
                         + "".join(f'<g class="chipg" style="--i:{k}" transform="translate(196 {40 + k * 30})"><rect width="110" height="22" rx="11" class="chipbg"/><text x="55" y="15" class="chiptx">{t}</text></g>' for k, t in enumerate(["더 싼 건?", "어제 산 거", "잼 말고 꿀"])) + '</svg>',
        "document-spotlight": '<svg viewBox="0 0 320 180"><rect x="40" y="16" width="240" height="150" rx="4" class="paper"/>' + "".join(f'<rect x="56" y="{34 + k * 18}" width="{200 - (k % 3) * 30}" height="7" rx="3" class="line {"keep" if k == 3 else "dimln"}"/>' for k in range(7)) + '</svg>',
        "chapter-two-line": '<svg viewBox="0 0 320 180"><rect width="320" height="180" class="bgA"/><text x="24" y="80" class="sm l1">2장</text><text x="24" y="118" class="big acc l2">그런데 결과는 반대였다</text></svg>',
        "shape-iris": f'<svg viewBox="0 0 320 180"><g>{J(8, 120, 20, 32, 40)}</g><circle class="iris" cx="160" cy="90" r="0"/><g class="irisB">{T("다음 이야기", "big", 90, 100, 24)}</g></svg>',
    }
    return d.get(tid, f'<svg viewBox="0 0 320 180">{T(H.escape(tid), "sm", 24, 90, 14)}</svg>')


# ---------------------------------------------------------------- 페이지
def _skin_vars(lid: str, d: dict, frames: dict) -> dict:
    from . import skin as _skin
    if not d.get("skin"):
        return {"base": "#111", "ink": "#ffffff", "acc": "#FFD23F", "card": "#1d2027", "font": "'Nanum Gothic'", "bg": f"url({frames.get('warm-doc', '')}) center/cover", "dark": True}
    sk = _skin.load(d["skin"])
    p, bg = sk["palette"], sk.get("background") or {}
    ft = (sk.get("fonts") or {}).get("title", "NanumGothic-ExtraBold.ttf")
    fam = next((v for k, v in looks.FONT_FAMILY.items() if ft.startswith(k)), "'Nanum Gothic'")
    t = bg.get("type", "flat")
    g = bg.get("grid_color", "#24497C")
    layer = {"grid": f"repeating-linear-gradient(0deg,transparent 0 23px,{g} 23px 24px),repeating-linear-gradient(90deg,transparent 0 23px,{g} 23px 24px),",
             "dark": "radial-gradient(ellipse at 50% 45%,rgba(255,255,255,.07),rgba(0,0,0,.45)),",
             "grain": "radial-gradient(ellipse at 50% 45%,rgba(255,255,255,.18),rgba(0,0,0,.12)),",
             "paper": "radial-gradient(ellipse at 30% 20%,rgba(255,255,255,.5),rgba(0,0,0,.08)),"}.get(t, "")
    return {"base": p["base"], "ink": p["ink"], "acc": p["accent"], "card": p["card"], "font": fam, "bg": f"{layer}{p['base']}"}


def _vars_css(v: dict) -> str:
    return f"--base:{v['base']};--ink:{v['ink']};--acc:{v['acc']};--card:{v['card']};--font:{v['font']};background:{v['bg']}"


def _media(out_dir: Path, frames: dict) -> dict:
    """예시 파일을 out_dir/media 로: 렌더한 장면(scenes/*.mp4)·바탕 그림(bg/*.jpg)·효과음(sfx/*.mp3). {상대경로: 파일}"""
    import shutil
    import subprocess
    from . import backdrop, hybrid
    from . import skin as _skin
    md = out_dir / "media"
    files = {}
    src = Path.home() / ".cache" / "ytflow" / "looks" / "scenes"
    (md / "scenes").mkdir(parents=True, exist_ok=True)
    for f in src.glob("*.mp4"):
        shutil.copy(f, md / "scenes" / f.name)
        files[f"media/scenes/{f.name}"] = md / "scenes" / f.name
    (md / "bg").mkdir(parents=True, exist_ok=True)
    skin_for = {"film": "dark-doc", "grid": "slate", "spot": "dark-doc", "tint": "paper-sketch", "photo": "dark-doc"}
    still = Path.home() / ".cache" / "ytflow" / "looks" / "still.jpg"
    if not still.exists():
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "3", "-i", str(Path.home() / ".cache" / "ytflow" / "looks" / "footage_src.mp4"),
                        "-frames:v", "1", str(still)], check=False)
    for k in backdrop.KINDS:
        o = md / "bg" / f"{k}.jpg"
        try:
            img = backdrop.make(_skin.load(skin_for.get(k, "dark-doc")), k, 640, 360, 2, still if k in ("photo", "duotone") else None,
                                ("#15171D", "#C9A66B") if k == "duotone" else None)
            img.convert("RGB").save(o, quality=82)
            files[f"media/bg/{k}.jpg"] = o
        except Exception as e:   # noqa: BLE001
            print(f"[gallery] 바탕 {k} 건너뜀: {e}")
    (md / "sfx").mkdir(parents=True, exist_ok=True)
    for k, f in hybrid.sfx_files().items():
        o = md / "sfx" / f"{k}.mp3"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(f), "-ac", "1", "-b:a", "64k", str(o)], check=False)
        if o.exists():
            files[f"media/sfx/{k}.mp3"] = o
    return files


def _thumb_mock(lid: str, frame: str) -> str:
    """썸네일 레이아웃의 모양 (실제 썸네일이 아니라 틀)."""
    if lid == "photo":
        return (f'<div class="tm" style="background:url({frame}) center/cover;filter:grayscale(1)"></div><div class="tmt" style="left:6%;top:52%">진열대 앞<br><b style="color:#ff4a3d">3%</b>만 샀다</div>'
                '<i class="tmc" style="left:62%;top:20%"></i>')
    if lid == "versus":
        return '<div class="tm" style="background:#efe8da"></div><div class="tmv"><b>24가지</b><span>vs</span><b style="color:#c4452f">6가지</b></div>'
    if lid == "board":
        return ('<div class="tm" style="background:#f4efe4"></div><svg viewBox="0 0 320 180" class="tms"><path d="M40 140 h120 v-60 h-120 z M60 80 v-20 h80 v20" '
                'style="fill:none;stroke:#222;stroke-width:3"/><circle cx="230" cy="70" r="18" style="fill:none;stroke:#222;stroke-width:3"/><path d="M230 88 v40 M210 104 h40 M230 128 l-14 24 M230 128 l14 24" style="stroke:#222;stroke-width:3"/></svg>'
                '<div class="tmt" style="left:6%;top:6%;color:#222;text-shadow:none">고를 게 많으면<br>왜 안 살까?</div>')
    return (f'<div class="tm" style="background:url({frame}) center/cover"></div><div class="tmt" style="left:6%;top:50%"><span style="background:#FFD23F;color:#111;padding:0 6px">60%</span> 멈췄는데</div>'
            '<b class="tmchip">▼ 3%</b>')


def build(out: Path, examples: Path | None = None) -> tuple[Path, dict]:
    """구성요소 카테고리(styles/components.yaml)마다 스타일 카드(진짜 렌더 예시) + 실제 쓰인 조합(styles/presets.yaml) + 조합 판."""
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    cats = looks.components()
    frames = looks._footage_frames()
    files = _media(out.parent, frames)
    ex = examples or looks.examples_dir()
    motion = next(c for c in cats if c["key"] == "motion")["options"]
    pal = {lid: _skin_vars(lid, d, frames) for lid, d in motion.items()}
    presets = (yaml.safe_load((ROOT / "styles" / "presets.yaml").read_text(encoding="utf-8")) or {}).get("presets", {})

    def chip(st):
        lab, cls = TSTATUS.get(st) or (looks.STATUS.get(st, st), st)
        if st == "hold":
            lab, cls = "쓰지 않음·보류", "hold"
        return f'<span class="st {cls}">{H.escape(lab)}</span>' if st else ""

    def meta(key, lid, d):
        what = d.get("look") or d.get("plain") or ""
        when = d.get("fits") or d.get("use_when") or ""
        warn = d.get("avoid") or d.get("caution") or ""
        extra = "".join(f'<small class="tag">{H.escape(x)}</small>' for x in (d.get("group"), d.get("used"), d.get("from") and f"예시: {d['from']}") if x)
        return (f'<figcaption><div class="row"><b>{H.escape(d.get("name", lid))}</b>{chip(d.get("status", ""))}</div><code>{lid}</code>'
                f'<p>{H.escape(str(what))}</p>' + (f'<p class="fit"><span>언제</span>{H.escape(str(when))}</p>' if when else "")
                + (f'<p class="avoid"><span>주의</span>{H.escape(str(warn))}</p>' if warn else "") + (f'<div class="tags">{extra}</div>' if extra else "")
                + f'<button class="pickbtn" data-cat="{key}" data-id="{lid}">조합에 넣기</button></figcaption>')

    def media_vis(k, lid, m):
        if m.endswith(".mp4"):
            if f"media/{m}" not in files:
                return '<figure class="pic"><div class="ph"><b>예시 화면 없음</b><span>이 컴퓨터에 그 장면의 자료가 없어 렌더하지 못함</span></div></figure>'
            return f'<figure class="pic" data-thumb="{k}:{lid}"><video src="media/{m}" muted loop playsinline preload="none"></video></figure>'
        if m.endswith(".jpg"):
            return f'<figure class="pic" data-thumb="{k}:{lid}"><img src="media/{m}" alt="" loading="lazy"></figure>' if f"media/{m}" in files else ""
        return ""

    sp = Path.home() / ".cache" / "ytflow" / "looks" / "scenes" / "scenes.json"
    rendered = json.loads(sp.read_text(encoding="utf-8")) if sp.exists() else {}
    for c in cats:   # 렌더한 예시가 어느 편의 장면인지 표시
        for lid, d in c["options"].items():
            m = str(d.get("media") or "")
            r = rendered.get(m[7:-4]) if m.startswith("scenes/") else None
            if r and r.get("file") and not d.get("from"):
                d["from"] = r.get("project", "") + (" (자료 화면은 대체 영상)" if r.get("placeholder") else "")
    scene = look_scene()
    sections, selects, tpls, have = [], [], [], 0
    for c in cats:
        k, cards = c["key"], []
        for lid, d in c["options"].items():
            m = d.get("media") or ""
            if k == "motion":
                vis = f'<figure class="stage look" style="{_vars_css(pal[lid])}">{scene}</figure>'
            elif k == "illust":
                img = next((p for p in (ex / f"{lid}.png", ex / f"{lid}.jpg", ex / f"{lid}.jpeg") if p.exists()), None)
                if lid == "doc-collage":
                    have += 1
                    inner = (f'<div class="col"><img src="{frames["_raw"]}" alt=""><div class="memo"><small>Iyengar &amp; Lepper (2000), JPSP</small>'
                             '<p>멈춘 손님 중 산 사람<br>6가지 <mark>30%</mark> · 24가지 <mark>3%</mark></p></div><i class="tape"></i></div>')
                elif img:
                    have += 1
                    inner = f'<img src="{looks._b64_jpg(img, 640)}" alt="" loading="lazy">'
                else:
                    inner = '<div class="ph"><b>예시 그림 준비 중</b><span>PC 에서 <code>python -m ytflow looks --draw auto</code></span></div>'
                vis = f'<figure class="pic" data-thumb="{k}:{lid}">{inner}</figure>'
            elif k == "footage":
                vis = f'<figure class="pic" data-thumb="{k}:{lid}"><img src="{frames[lid]}" alt=""></figure>'
            elif k == "font":
                vis = (f'<figure class="pic fontv" style="font-family:{d.get("family")};font-weight:{d.get("weight", 400)}">'
                       f'<div><b>고를 게 많으면 왜 안 살까?</b><span>60% · 24가지 · 3%</span></div></figure>')
            elif k == "subtitle":
                sb = d.get("sub") or {}
                if sb.get("hidden"):
                    inner = '<div class="subk">많을수록 <b>좋을까?</b></div>'
                else:
                    pos = {"top": "top:8%", "mid": "top:42%", "bottom": "bottom:8%"}[sb.get("pos", "bottom")]
                    outl = "text-shadow:-2px -2px 0 #000,2px -2px 0 #000,-2px 2px 0 #000,2px 2px 0 #000;font-size:22px;font-weight:800" if sb.get("outline") else ""
                    orig = '<div class="subo">Thirty percent of them bought a jar.</div>' if sb.get("orig") else ""
                    word = '<b style="color:#FFD23F">30%</b>' if sb.get("outline") else "30%"
                    inner = (f'<div class="subw" style="{pos}">{orig}<span style="background:{sb.get("bg")};color:{sb.get("color")};{outl}">'
                             f'멈춘 손님 가운데 {word}가 샀습니다</span></div>')
                bgimg = "" if sb.get("pos") == "top" else f"background:url({frames['warm-doc']}) center/cover;"
                vis = f'<figure class="pic sub" style="{bgimg}{"background:#F6F2EA;" if sb.get("pos") == "top" else ""}">{inner}</figure>'
            elif k == "thumbnail":
                vis = f'<figure class="pic thumbm">{_thumb_mock(lid, frames["_raw"])}<small class="mock">모양 미리보기</small></figure>'
            elif k == "sfx":
                au = f'<audio controls preload="none" src="media/sfx/{lid}.mp3"></audio>' if f"media/sfx/{lid}.mp3" in files else '<span class="na">파일 없음</span>'
                vis = f'<figure class="stage snd"><svg viewBox="0 0 320 180">' + "".join(
                    f'<rect x="{30 + i * 14}" y="{90 - h}" width="8" height="{2 * h}" rx="3" class="wave" style="--i:{i}"/>' for i, h in enumerate([6, 14, 30, 48, 34, 20, 12, 8, 26, 40, 22, 10, 6, 4, 8, 18, 12, 6, 4])) + f'</svg>{au}</figure>'
            elif k in ("bgm", "voice"):
                vis = ('<figure class="stage snd"><svg viewBox="0 0 320 180">' + "".join(
                    f'<rect x="{20 + i * 12}" y="{90 - h}" width="7" height="{2 * h}" rx="3" class="wave" style="--i:{i}"/>'
                    for i, h in enumerate([10, 24, 40, 18, 52, 30, 14, 44, 26, 12, 36, 48, 20, 30, 16, 40, 22, 10, 28, 34, 18, 12, 8])) + '</svg></figure>')
            elif m:
                vis = media_vis(k, lid, m)
            elif k in ("text", "graphic", "camera", "transition"):
                demo_html = demo(lid).replace("{{FRAME}}", frames["_raw"])
                vis = f'<figure class="stage dir t-{lid}">{demo_html}</figure>'
                tpls.append(f'<template id="tpl-{lid}">{demo_html}</template>')
            else:
                vis = '<figure class="pic"><div class="ph"><b>예시 화면 없음</b><span>아직 쓴 장면이 없어 렌더하지 못함</span></div></figure>'
            cards.append(f'<article class="card" data-card="{k}:{lid}">{vis}{meta(k, lid, d)}</article>')
        n = len(c["options"])
        extra = f' · 예시 {have}/{n}' if k == "illust" else ""
        sections.append(f'<section class="cat" id="cat-{k}"><h2><span class="axis {c.get("axis", "")}">{H.escape(c.get("axis", ""))}</span>{H.escape(c["name"])} <small>{n}가지{extra}</small></h2>'
                        f'<p class="lead">{H.escape(c.get("what", ""))}</p><div class="grid">{"".join(cards)}</div></section>')
        opts = '<option value="">—</option>' + "".join(f'<option value="{lid}">{H.escape(d.get("name", lid))}</option>' for lid, d in c["options"].items())
        selects.append(f'<label><span class="axis {c.get("axis", "")}">{H.escape(c.get("axis", ""))}</span>{H.escape(c["name"])}<select data-cat="{k}">{opts}</select></label>')

    # 실제 쓰인 조합
    sc_names = next(c for c in cats if c["key"] == "scene")["options"]
    pcards = []
    for pid, p in presets.items():
        pick = dict(p.get("pick") or {})
        first = next((t for t in (p.get("scenes") or {}) if t in sc_names), "")
        if first:
            pick.setdefault("scene", first)
        chips = " ".join(f'<span class="sc">{H.escape(sc_names.get(t, {}).get("name", t))} {v}</span>' for t, v in (p.get("scenes") or {}).items())
        vid = f'<video src="media/scenes/{first}.mp4" muted loop playsinline preload="none"></video>' if first and f"media/scenes/{first}.mp4" in files else ""
        pcards.append(f'<article class="preset"><div class="pv2">{vid}</div><div class="pbody"><div class="row"><b>{H.escape(p["name"])}</b><span class="st av">{H.escape(p.get("verdict", ""))}</span></div>'
                      f'<code>{H.escape(str(p.get("project", "")))}</code><p><span class="lbl">편집·연출</span>{H.escape(p.get("edit", ""))}</p>'
                      f'<p><span class="lbl">화풍</span>{H.escape(p.get("look", ""))}</p><div class="chips">{chips}</div>'
                      f'<button class="applybtn" data-pick=\'{H.escape(json.dumps(pick, ensure_ascii=False))}\'>이 조합 불러오기</button></div></article>')
    preset_html = (f'<section class="cat" id="presets"><h2><span class="axis 조합">조합</span>실제로 쓰인 조합 <small>{len(presets)}편</small></h2>'
                   f'<p class="lead">스페인독감·시장·호기심 편이 실제로 쓴 편집·연출·화풍. 장면 수는 그 편 대본에서 센 것입니다. \'이 조합 불러오기\'를 누르면 아래 조합 판에 들어갑니다.</p>'
                   f'<div class="pgrid">{"".join(pcards)}</div></section>')

    composer = f"""<section class="mix"><h2>조합 — 카테고리마다 하나씩 고르면 영상이 됩니다</h2>
<p class="lead">카드의 '조합에 넣기'·위의 '이 조합 불러오기'를 누르거나 여기서 고르세요. 미리보기는 고른 화면 화풍 위에서 ① 글자 → ② 그래픽 → ③ 카메라 → ④ 전환 순서로 재생되고, 오른쪽에 고른 장면·장 표지·바탕·삽화·실사가 모입니다.</p>
<div class="mixgrid"><div class="sels">{''.join(selects)}</div>
<div class="pv"><figure class="stage big" id="pv"><div class="lay" data-step="text"></div><div class="lay" data-step="graphic"></div><div class="lay" data-step="camera"></div><div class="lay" data-step="transition"></div></figure>
<ol class="tl"><li data-step="text">① 글자 연출</li><li data-step="graphic">② 그래픽 연출</li><li data-step="camera">③ 카메라</li><li data-step="transition">④ 장면 전환</li></ol>
<div class="side" id="side"></div>
<pre class="cmd" id="cmd"></pre></div></div></section>"""
    nav = '<a href="#presets">실제 쓰인 조합</a>' + "".join(f'<a href="#cat-{c["key"]}">{H.escape(c["name"])}</a>' for c in cats)
    body = composer + f'<nav class="cats">{nav}</nav>' + preset_html + "".join(sections) + "".join(tpls)
    page = PAGE.replace("{{BODY}}", body).replace("{{PAL}}", json.dumps(pal, ensure_ascii=False)) \
               .replace("{{NC}}", str(len(cats))).replace("{{NS}}", str(sum(len(c["options"]) for c in cats)))
    out.write_text(page, encoding="utf-8")
    return out, files


PAGE = r"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>영상 구성요소 목록</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Nanum+Gothic:wght@400;700;800&family=Nanum+Myeongjo:wght@700;800&family=Nanum+Pen+Script&display=swap">
<style>
:root{--bg:#f5f4f0;--panel:#fff;--fg:#1b1d22;--muted:#5f6470;--line:#dedbd3;--ok:#1f8a4c;--trial:#b26b00;--av:#3358d4;--hold:#8a8f99;color-scheme:light}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#14161b;--panel:#1d2027;--fg:#e9eaee;--muted:#a0a6b3;--line:#2e333e;--ok:#5fd394;--trial:#f0b04f;--av:#7c9bff;--hold:#8a8f99;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#14161b;--panel:#1d2027;--fg:#e9eaee;--muted:#a0a6b3;--line:#2e333e;--ok:#5fd394;--trial:#f0b04f;--av:#7c9bff;--hold:#8a8f99;color-scheme:dark}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.55 'Nanum Gothic',system-ui,sans-serif}
.wrap{max-width:1280px;margin:0 auto;padding:20px 16px 48px}
header h1{margin:0;font-size:24px;font-weight:800}header p{margin:4px 0 0;color:var(--muted);max-width:76ch}
nav.tabs{display:flex;gap:6px;margin:16px 0 8px;position:sticky;top:0;background:var(--bg);padding:8px 0;z-index:3}
nav.tabs button{font:inherit;color:var(--fg);background:var(--panel);border:1px solid var(--line);border-radius:999px;padding:6px 16px;cursor:pointer}
nav.tabs button[aria-selected=true]{background:var(--fg);color:var(--bg);border-color:var(--fg)}
h2{margin:26px 0 10px;font-size:19px}h2 small{font-size:13px;color:var(--muted);font-weight:400}h3{margin:22px 0 8px;font-size:15px;color:var(--muted)}
.lead{color:var(--muted);margin:4px 0 0}
.bar{display:flex;flex-wrap:wrap;gap:8px 16px;align-items:center;background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:10px 14px;position:sticky;top:52px;z-index:2}
.bar select{font:inherit;padding:4px 8px;border-radius:6px;border:1px solid var(--line);background:var(--bg);color:var(--fg)}.hint{font-size:13px;color:var(--muted);flex:1;min-width:240px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:14px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;overflow:hidden;display:flex;flex-direction:column}
figure{margin:0}.pic,.stage{aspect-ratio:16/9;overflow:hidden;position:relative}.pic{background:#000;display:grid;place-items:center}.pic img{width:100%;height:100%;object-fit:cover}
.ph{background:repeating-linear-gradient(45deg,var(--bg) 0 10px,var(--panel) 10px 20px);width:100%;height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;gap:6px;padding:16px;text-align:center;color:var(--muted)}.ph b{color:var(--fg)}.ph span{font-size:12.5px}
figcaption{padding:10px 12px 12px;display:flex;flex-direction:column;gap:4px}figcaption .row{display:flex;justify-content:space-between;gap:8px;align-items:center}figcaption code{font-size:12px;color:var(--muted)}
figcaption p{margin:0;font-size:13px}.fit span,.avoid span{display:inline-block;font-size:11px;border:1px solid var(--line);border-radius:4px;padding:0 5px;margin-right:6px;color:var(--muted)}.avoid{color:var(--muted)}
.st{font-size:11.5px;border-radius:999px;padding:1px 8px;border:1px solid currentColor;white-space:nowrap}.st.approved,.st.ok{color:var(--ok)}.st.trial{color:var(--trial)}.st.available,.st.av{color:var(--av)}.st.hold{color:var(--hold)}
.go-dir{align-self:flex-start;margin-top:4px;font:inherit;font-size:12.5px;background:none;border:1px solid var(--line);border-radius:6px;padding:3px 9px;color:var(--fg);cursor:pointer}
.col{position:relative;width:100%;height:100%;background:#e9e3d6}.col img{position:absolute;left:6%;top:9%;width:50%;height:auto;transform:rotate(-3deg);box-shadow:0 4px 12px rgba(0,0,0,.35);border:6px solid #fff}
.memo{position:absolute;right:5%;top:22%;width:44%;background:#fffdf6;color:#222;padding:8px 10px;transform:rotate(2deg);box-shadow:0 3px 10px rgba(0,0,0,.25);font-size:12px}.memo small{color:#666}.memo p{margin:4px 0 0}.memo mark{background:#ffe066}
.tape{position:absolute;left:22%;top:5%;width:70px;height:20px;background:rgba(255,240,180,.75);transform:rotate(-8deg)}
/* 무대: 화풍 색은 변수로 */
.stage svg{position:absolute;inset:0;width:100%;height:100%}
.stage text{fill:var(--ink);font-family:var(--font),'Nanum Gothic',sans-serif;font-weight:800}
.stage .acc,.stage tspan.acc{fill:var(--acc)}.stage .sm{font-size:14px;font-weight:700}.stage .big{font-size:28px}.stage .huge{font-size:64px}.stage .lb{font-size:11px}
.stage .chip{font-size:11px;fill:var(--base);text-anchor:middle}.stage .arr{fill:none;stroke:var(--acc);stroke-width:2.5;stroke-dasharray:4 4}
.stage .pp{fill:var(--ink);opacity:.3}.stage .pp.on{fill:var(--acc);opacity:1}
.stage.look[data-dark] text{text-shadow:0 2px 6px #000}
.paper{fill:var(--card);stroke:var(--ink);stroke-opacity:.25}.line{fill:var(--ink);opacity:.35}.bar{fill:var(--acc)}
.bgA{fill:var(--base)}.house{fill:var(--card);stroke:var(--ink);stroke-width:3}
/* 연출 — .go 가 붙을 때 처음부터 */
.dir:not(.go) *,.lay:not(.go) *{animation:none!important}
.go .w{opacity:0;animation:up .5s ease-out forwards;animation-delay:calc(var(--i)*.35s + .2s)}
@keyframes up{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
.go .hl{fill:var(--acc);opacity:.35;transform-box:fill-box;transform-origin:left;transform:scaleX(0);animation:sx .7s .4s ease-out forwards}
.go .ul{fill:none;stroke:var(--acc);stroke-width:3;stroke-dasharray:220;stroke-dashoffset:220;animation:dash .6s 1.2s forwards}
@keyframes sx{to{transform:scaleX(1)}}@keyframes dash{to{stroke-dashoffset:0}}
.draw{fill:none;stroke:var(--acc);stroke-width:4;stroke-linecap:round;stroke-dasharray:300;stroke-dashoffset:300}.go .draw{animation:dash 1.4s .3s ease-in-out forwards}
.mph{fill:var(--acc);rx:8px}.go .mph{animation:mph 2.6s ease-in-out forwards}
@keyframes mph{0%{rx:8px}35%{rx:35px}70%{rx:35px;fill:var(--ink)}100%{rx:12px;fill:var(--ink)}}
.jj{transform-box:fill-box;transform-origin:50% 100%}
.go .st .jj{transform:scale(0);animation:pop .4s cubic-bezier(.3,1.6,.5,1) forwards;animation-delay:calc(var(--i)*80ms + .2s)}@keyframes pop{to{transform:scale(1)}}
.track{fill:none;stroke:var(--ink);stroke-width:2;stroke-dasharray:5 6;opacity:.5}.mover{fill:var(--acc);offset-path:path('M30 140 C 100 20, 220 180, 290 50');offset-distance:0%}.go .mover{animation:mp 2.2s .2s ease-in-out forwards}@keyframes mp{to{offset-distance:100%}}
.go .mmA{animation:fadeout .4s .8s forwards}.mmT{opacity:0}.go .mmT{animation:fadein .4s 1.5s forwards}
.mmJ .jj{transform-origin:50% 100%}.go .mmJ{animation:mmj 1s .8s cubic-bezier(.5,0,.2,1) forwards}@keyframes mmj{to{transform:translate(20px,20px) scale(2.2)}}
@keyframes fadeout{to{opacity:0}}@keyframes fadein{to{opacity:1}}
.clipA{fill:var(--ink);opacity:.5}.clipB{fill:var(--acc)}.cutline{stroke:var(--ink);stroke-dasharray:3 3}.play{fill:var(--acc)}.go .play{animation:play 3s linear forwards}@keyframes play{to{transform:translateX(240px)}}
.xb{opacity:0}.go .xb{animation:fadein .9s 1s forwards}
.zi{transform-origin:178px 100px}.go .zi{animation:zi 1.6s .4s ease-in forwards}@keyframes zi{to{transform:scale(7);opacity:.2}}
.go .wp{animation:wp .7s .8s ease-in forwards}@keyframes wp{to{transform:translateX(-340px);filter:blur(6px)}}
.tile{fill:var(--acc);opacity:0}.go .tile{animation:fadein .3s forwards;animation-delay:calc(var(--i)*.12s + .2s)}
.far{fill:var(--ink);opacity:.15}.go .px1{animation:pxa 3s linear forwards}.go .px2{animation:pxb 3s linear forwards}.go .px3{animation:pxc 3s linear forwards}
@keyframes pxa{to{transform:translateX(-6px)}}@keyframes pxb{to{transform:translateX(-16px)}}@keyframes pxc{to{transform:translateX(-34px)}}
.pb{transform-origin:132px 66px;transform:scale(5)}.go .pb{animation:pb 2.2s .3s cubic-bezier(.4,0,.2,1) forwards}@keyframes pb{to{transform:scale(1)}}
.br .bar{width:120px}.br0{transform:translateY(60px)}.br1{transform:translateY(95px)}.br2{transform:translateY(130px)}
.go .br0{animation:r0 2.4s ease-in-out forwards}.go .br2{animation:r2 2.4s ease-in-out forwards}.go .br2 .bar{animation:w2 2.4s forwards}.go .br0 .bar{animation:w0 2.4s forwards}
@keyframes r0{60%,100%{transform:translateY(130px)}}@keyframes r2{60%,100%{transform:translateY(60px)}}@keyframes w2{from{width:90px}to{width:200px}}@keyframes w0{from{width:180px}to{width:110px}}
.cmLine{fill:none;stroke:var(--acc);stroke-width:4;stroke-dasharray:240;stroke-dashoffset:240}.go .cmLine{animation:dash 1s 1.2s forwards}.go .cmBar{animation:dimb .8s .6s forwards}@keyframes dimb{to{opacity:.18}}
.divider{stroke:var(--ink);stroke-width:2}.ssL{transform:translateX(-170px)}.ssR{transform:translateX(170px)}.go .ssL,.go .ssR{animation:ss .7s .2s cubic-bezier(.2,.8,.2,1) forwards}@keyframes ss{to{transform:none}}
.go .spot .j:not(.sp){animation:dimj .6s .6s forwards}@keyframes dimj{to{opacity:.15}}.go .sp .jj{animation:grow .5s 1s forwards}@keyframes grow{to{transform:scale(1.35)}}
.cardr{fill:var(--card);stroke:var(--ink);stroke-opacity:.3}.cs .dot{fill:var(--ink);opacity:.4}.cs .s2{opacity:0}.go .cs .dot{animation:dotc .3s 1.2s forwards}.go .cs .s1{animation:fadeout .2s 1.2s forwards}.go .cs .s2{animation:fadein .3s 1.3s forwards}
@keyframes dotc{to{fill:var(--acc);opacity:1}}
.node{fill:var(--card);stroke:var(--ink);stroke-width:2}.link{stroke:var(--ink);stroke-width:3}.broken{stroke:#d33;stroke-width:3;stroke-dasharray:6 6;opacity:0}.xmark path{stroke:#d33;stroke-width:4;opacity:0}
.go .link{animation:fadeout .2s 1s forwards}.go .broken{animation:fadein .2s 1s forwards}.go .xmark path{animation:fadein .2s 1.2s forwards}
.chipbg{fill:var(--acc)}.chiptx{fill:var(--base);font-size:11px;text-anchor:middle}.chipg{opacity:0}.go .chipg{animation:up .4s forwards;animation-delay:calc(var(--i)*.5s + .3s)}
.dimln{transition:none}.go .dimln{animation:dimb .6s .5s forwards}.go .keep{animation:keep .5s .9s forwards}@keyframes keep{to{fill:var(--acc);opacity:1}}
.l1,.l2{opacity:0}.go .l1{animation:up .4s .2s forwards}.go .l2{animation:up .5s .6s forwards}
.iris{fill:var(--acc)}.go .iris{animation:iris 1.2s .4s ease-in forwards}@keyframes iris{to{r:200}}.irisB{opacity:0}.go .irisB{animation:fadein .4s 1.6s forwards}.irisB text{fill:var(--base)}
@media (prefers-reduced-motion:reduce){.dir *{animation:none!important}}
.mix{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:14px 16px;margin-top:14px}.mix h2{margin:0 0 4px}
.mixgrid{display:grid;grid-template-columns:minmax(220px,300px) 1fr;gap:16px;margin-top:10px}@media (max-width:820px){.mixgrid{grid-template-columns:1fr}}
.sels{display:flex;flex-direction:column;gap:8px}.sels label{display:flex;flex-direction:column;gap:3px;font-size:13px}.sels select{font:inherit;padding:5px 8px;border-radius:6px;border:1px solid var(--line);background:var(--bg);color:var(--fg)}
.axis{display:inline-block;font-size:10.5px;border-radius:4px;padding:0 6px;margin-right:6px;vertical-align:2px;color:#fff;background:#888}.axis.화풍{background:#3358d4}.axis.연출{background:#c4452f}.axis.소리{background:#1f8a4c}
.pv .stage.big{border-radius:10px;border:1px solid var(--line)}.lay{position:absolute;inset:0;opacity:0;transition:opacity .3s}.lay.on{opacity:1}.lay svg{position:absolute;inset:0;width:100%;height:100%}
.tl{display:flex;gap:6px;list-style:none;padding:0;margin:8px 0;flex-wrap:wrap}.tl li{font-size:12.5px;border:1px solid var(--line);border-radius:999px;padding:2px 10px;color:var(--muted)}.tl li.on{background:var(--fg);color:var(--bg)}
.side{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;align-items:start}.side small{color:var(--muted);display:block;margin-bottom:3px}.thumb{aspect-ratio:16/9;border-radius:6px;overflow:hidden;background:var(--bg);position:relative}.thumb img{width:100%;height:100%;object-fit:cover}.thumb .ph{font-size:11px;padding:4px}.thumb .ph span{display:none}
.cmd{white-space:pre-wrap;word-break:break-all;background:var(--bg);border:1px solid var(--line);border-radius:6px;padding:8px 10px;font-size:12px;margin:10px 0 0}
nav.cats{display:flex;flex-wrap:wrap;gap:6px;margin:18px 0 0;position:sticky;top:0;background:var(--bg);padding:8px 0;z-index:3}nav.cats a{color:var(--fg);text-decoration:none;border:1px solid var(--line);border-radius:999px;padding:3px 11px;font-size:12.5px}
.pickbtn{align-self:flex-start;margin-top:4px;font:inherit;font-size:12.5px;background:none;border:1px solid var(--line);border-radius:6px;padding:3px 9px;color:var(--fg);cursor:pointer}
.card.chosen{outline:2.5px solid var(--av);outline-offset:-1px}.card.chosen .pickbtn{background:var(--av);color:#fff;border-color:var(--av)}
.snd .wave{fill:var(--acc);transform-box:fill-box;transform-origin:center;animation:wv 1.2s ease-in-out infinite alternate;animation-delay:calc(var(--i)*-.13s)}@keyframes wv{from{transform:scaleY(.35)}to{transform:scaleY(1)}}
.pic video{width:100%;height:100%;object-fit:cover;display:block}
.tags{display:flex;flex-wrap:wrap;gap:4px}.tag{font-size:11px;color:var(--muted);border:1px solid var(--line);border-radius:4px;padding:0 5px}
.fontv{background:#f6f2ea;color:#1e2a44;display:flex;align-items:center;justify-content:center;text-align:center}.fontv div{display:flex;flex-direction:column;gap:6px;padding:10px}.fontv b{font-size:24px;font-weight:inherit}.fontv span{font-size:30px;color:#c4452f}
.pic.sub{position:relative}.subw{position:absolute;left:0;right:0;text-align:center;font-weight:700;font-size:15px}.subw span{padding:3px 9px;border-radius:3px}.subo{font-size:11px;color:#ddd;margin-bottom:3px}.subk{position:absolute;inset:0;display:grid;place-items:center;background:#F4EDE1;color:#111;font:800 34px 'Nanum Gothic'}.subk b{color:#E2381F}
.thumbm{position:relative}.tm{position:absolute;inset:0}.tmt{position:absolute;color:#fff;font:800 22px/1.2 'Nanum Gothic';text-shadow:0 2px 6px #000}.tmc{position:absolute;width:70px;height:70px;border:4px solid #ff3b2f;border-radius:50%}
.tmv{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;gap:16px;font:800 34px 'Nanum Myeongjo';color:#22304D}.tmv span{font-size:18px;color:#888}.tms{position:absolute;inset:0;width:100%;height:100%}
.tmchip{position:absolute;right:6%;top:10%;background:#e5382a;color:#fff;font:800 18px 'Nanum Gothic';padding:2px 8px;border-radius:4px}.mock{position:absolute;right:6px;bottom:4px;font-size:10px;color:#fff;background:rgba(0,0,0,.5);padding:0 4px;border-radius:3px}
.snd audio{position:absolute;left:8%;right:8%;bottom:8%;width:84%;height:30px}.na{position:absolute;bottom:10%;left:10%;font-size:12px;color:var(--muted)}
.pgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(360px,1fr));gap:14px}@media (max-width:420px){.pgrid{grid-template-columns:1fr}}
.preset{background:var(--panel);border:1px solid var(--line);border-radius:10px;overflow:hidden;display:flex;flex-direction:column}.pv2{aspect-ratio:16/9;background:#111}.pv2 video{width:100%;height:100%;object-fit:cover}
.pbody{padding:10px 12px 12px;display:flex;flex-direction:column;gap:5px}.pbody p{margin:0;font-size:13px}.lbl{display:inline-block;font-size:11px;border:1px solid var(--line);border-radius:4px;padding:0 5px;margin-right:6px;color:var(--muted)}
.chips{display:flex;flex-wrap:wrap;gap:4px}.chips .sc{font-size:11.5px;background:var(--bg);border-radius:999px;padding:1px 8px}
.applybtn{align-self:flex-start;font:inherit;font-size:13px;background:var(--fg);color:var(--bg);border:0;border-radius:6px;padding:5px 12px;cursor:pointer;margin-top:4px}
.axis.구성{background:#8a5bd6}.axis.포장{background:#b26b00}.axis.조합{background:#1b1d22}
#side{display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:8px}#side .it small{display:block;color:var(--muted);font-size:11px;margin-bottom:2px}#side .it .pic,#side .it .stage{border-radius:6px}#side .it b{font-size:12.5px}
.how{margin-top:28px;background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px 16px;font-size:13.5px}.how code{background:var(--bg);padding:1px 6px;border-radius:4px}
</style></head><body><div class="wrap">
<header><h1>영상 구성요소 · 스타일 목록</h1><p>영상은 <b>구성요소 {{NC}}가지</b>(화풍 · 구성 · 연출 · 소리 · 포장)를 카테고리마다 하나씩 골라 <b>조합</b>한 것입니다. 예시 화면은 지금까지 영상에 쓴 장면을 실제 렌더러로 다시 그린 것입니다. 스타일은 모두 {{NS}}가지. 화풍(어떻게 보이나)과 연출(어떻게 움직이나)은 다른 축이라 서로 섞을 수 있고, 같은 모션그래픽이라도 연출이 다르면 전혀 다른 장면이 됩니다.</p></header>
{{BODY}}
<div class="how"><b>정하는 법</b> — <code>python -m ytflow look &lt;프로젝트&gt; --set motion=chalkboard --set text=count-up --set graphic=stagger --set transition=match-move</code> (조합 판 아래 명령을 그대로 복사). 화풍 3종은 렌더에 바로 쓰이고, 연출은 이 영상의 기본값 — 장면마다 바꿀 수 있습니다. 대화로 "칠판 화풍에 카운트업, 전환은 매치 무브"처럼 말해도 됩니다. 원본: <code>styles/components.yaml</code></div>
</div>
<script>
(function(){
var PAL={{PAL}};var STEPS=['text','graphic','camera','transition'];
var SIDE=['scene','chapter','background','structure','slots','layer','fx','beat','illust','footage','font','subtitle','thumbnail'];
var sel={};document.querySelectorAll('.sels select').forEach(function(x){sel[x.dataset.cat]=x});
var DEF={motion:'clean-flat',illust:'cute-casual',footage:'warm-doc',text:'count-up',graphic:'stagger',camera:'pull-back',transition:'match-move',bgm:'rest-now',scene:'bars',chapter:'photo',background:'film'};
try{var saved=JSON.parse(localStorage.getItem('mix2')||'null');if(saved)DEF=saved}catch(e){}
function setv(k,v){if(sel[k]&&[].some.call(sel[k].options,function(o){return o.value===v}))sel[k].value=v}
for(var k in DEF)setv(k,DEF[k]);
function paintAll(){var v=PAL[sel.motion.value];if(!v)return;var css='--base:'+v.base+';--ink:'+v.ink+';--acc:'+v.acc+';--card:'+v.card+';--font:'+v.font+';background:'+v.bg;document.querySelectorAll('.dir,.snd,#pv').forEach(function(d){d.style.cssText=css})}
function name(k){var o=sel[k].options[sel[k].selectedIndex];return o?o.text:''}
function fill(){STEPS.forEach(function(s){var t=sel[s].value&&document.getElementById('tpl-'+sel[s].value);document.querySelector('#pv .lay[data-step='+s+']').innerHTML=t?t.innerHTML:''});
 var side=document.getElementById('side');side.innerHTML='';
 SIDE.concat(['bgm','sfx','voice']).forEach(function(k){if(!sel[k]||!sel[k].value)return;var it=document.createElement('div');it.className='it';
  var lab=document.querySelector('.sels select[data-cat='+k+']').parentNode.childNodes[1].textContent;it.innerHTML='<small>'+lab+'</small>';
  var card=document.querySelector('article.card[data-card="'+k+':'+sel[k].value+'"] figure');
  if(card&&SIDE.indexOf(k)>=0){var c=card.cloneNode(true);c.querySelectorAll('video').forEach(function(v){v.autoplay=true;v.preload='auto'});c.querySelectorAll('audio').forEach(function(a){a.remove()});it.appendChild(c)}
  var b=document.createElement('b');b.textContent=name(k);it.appendChild(b);side.appendChild(it)});
 side.querySelectorAll('video').forEach(function(v){v.play().catch(function(){})});
 document.querySelectorAll('article.card').forEach(function(c){var p=c.dataset.card.split(':');c.classList.toggle('chosen',!!sel[p[0]]&&sel[p[0]].value===p[1])});
 document.getElementById('cmd').textContent='python -m ytflow look <프로젝트> '+Object.keys(sel).filter(function(k){return sel[k].value}).map(function(k){return '--set '+k+'='+sel[k].value}).join(' ');
 var o={};for(var k in sel)o[k]=sel[k].value;try{localStorage.setItem('mix2',JSON.stringify(o))}catch(e){}
 paintAll();}
Object.keys(sel).forEach(function(k){sel[k].onchange=fill});
document.querySelectorAll('.pickbtn').forEach(function(b){b.onclick=function(){sel[b.dataset.cat].value=b.dataset.id;fill();document.querySelector('.mix').scrollIntoView({behavior:'smooth'})}});
document.querySelectorAll('.applybtn').forEach(function(b){b.onclick=function(){var p=JSON.parse(b.dataset.pick);for(var k in p)if(sel[k])sel[k].value=p[k]||'';fill();document.querySelector('.mix').scrollIntoView({behavior:'smooth'})}});
var step=-1;
function restart(el){el.classList.remove('go');void el.offsetWidth;el.classList.add('go');
 el.querySelectorAll('[data-scramble]').forEach(function(x){var t=x.dataset.scramble,n=0,CH='#%&@$*0123456789ABCDEFGHJK가나다라';var iv=setInterval(function(){n++;var k=Math.floor(n/3);x.textContent=t.split('').map(function(c,i){return i<k||c===' '?c:CH[Math.floor(Math.random()*CH.length)]}).join('');if(k>=t.length)clearInterval(iv)},45)});
 el.querySelectorAll('[data-count]').forEach(function(x){var to=+x.dataset.count,s=x.dataset.suffix||'',t0=performance.now();(function f(now){var p=Math.min(1,(now-t0-200)/1200);p=p<0?0:1-Math.pow(1-p,3);x.textContent=Math.round(to*p)+s;if(p<1)requestAnimationFrame(f)})(t0)});}
function tick(){step=(step+1)%4;var s=STEPS[step];
 document.querySelectorAll('#pv .lay').forEach(function(l){var on=l.dataset.step===s;l.classList.toggle('on',on);l.classList.remove('go');if(on)restart(l)});
 document.querySelectorAll('.tl li').forEach(function(li){li.classList.toggle('on',li.dataset.step===s)});}
function loopCards(){document.querySelectorAll('.cat .dir').forEach(restart)}
var io='IntersectionObserver' in window?new IntersectionObserver(function(es){es.forEach(function(e){var v=e.target;if(e.isIntersecting){v.preload='auto';v.play().catch(function(){})}else v.pause()})},{rootMargin:'200px'}):null;
document.querySelectorAll('.cat video').forEach(function(v){if(io)io.observe(v);else{v.autoplay=true}});
fill();tick();loopCards();setInterval(tick,3800);setInterval(loopCards,4200);
})();
</script></body></html>"""
