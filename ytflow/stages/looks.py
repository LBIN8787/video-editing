"""화풍 목록 (styles/looks.yaml): 모션그래픽·삽화·실사 색보정을 영상마다 고르는 자리.

무엇으로 보여 줄지(실사·모션그래픽·삽화)는 박자가 하는 일이 정하고(manual/12 §0-1), 여기서는 '어떻게 보일지'만 고릅니다.
프로젝트 edit.yaml 의  look: {motion: <id>, illust: <id>, footage: <id>}
  motion  → 그래픽 스킨 (config.load('pipeline') 이 edit.skin 으로 바꿈, edit.yaml 에 skin 을 직접 적으면 그것이 우선)
  illust  → 그림 주문서 화풍 문장 (imagegen.run, art_plan.json 의 style 이 우선)
  footage → 실사 클립 색보정 ffmpeg 필터 (footage_vf)
"""
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
FILE = ROOT / "styles" / "looks.yaml"
KINDS = {"motion": "모션그래픽 화풍", "illust": "삽화 화풍", "footage": "실사 색보정"}
STATUS = {"approved": "합격", "trial": "시안", "available": "사용 가능"}


def load() -> dict:
    return yaml.safe_load(FILE.read_text(encoding="utf-8")) or {}


def get(kind: str, look_id: str) -> dict | None:
    return (load().get(kind) or {}).get(look_id)


def skin_for(look_id: str) -> str:
    d = get("motion", look_id) or {}
    return d.get("skin") or ""


def project_look(project_dir: Path) -> dict:
    p = Path(project_dir) / "edit.yaml"
    d = (yaml.safe_load(p.read_text(encoding="utf-8")) or {}) if p.exists() else {}
    return d.get("look") or (d.get("edit") or {}).get("look") or {}


def illust_prompt(project_dir: Path) -> str:
    lid = project_look(project_dir).get("illust")
    return ((get("illust", lid) or {}).get("prompt") or "") if lid else ""


def footage_vf(project_dir: Path, default: str = "warm-doc") -> str:
    lid = project_look(project_dir).get("footage") or default
    return (get("footage", lid) or {}).get("vf", "")


def listing(kind: str | None = None) -> str:
    data = load()
    out = []
    for k, title in KINDS.items():
        if kind and k != kind:
            continue
        out += [f"## {title} ({k})", "", "| id | 이름 | 모습 | 어울리는 상황 | 피할 때 | 상태 |", "|---|---|---|---|---|---|"]
        for lid, d in (data.get(k) or {}).items():
            out.append(f"| `{lid}` | {d.get('name', '')} | {d.get('look', '')} | {d.get('fits', '')} | {d.get('avoid', '')} | "
                       f"{STATUS.get(d.get('status', ''), d.get('status', ''))} |")
        out.append("")
    out.append("고르기: python -m ytflow look <프로젝트> --motion <id> --illust <id> --footage <id>")
    return "\n".join(out)


def choose(project_dir: Path, motion: str = "", illust: str = "", footage: str = "") -> dict:
    """edit.yaml 의 look 을 바꾸고 지금 값을 돌려줌. 없는 id 는 거절."""
    data = load()
    for k, v in (("motion", motion), ("illust", illust), ("footage", footage)):
        if v and v not in (data.get(k) or {}):
            raise SystemExit(f"[look] '{v}' 는 {KINDS[k]} 목록에 없습니다 — python -m ytflow looks --kind {k}")
    p = Path(project_dir) / "edit.yaml"
    d = (yaml.safe_load(p.read_text(encoding="utf-8")) or {}) if p.exists() else {}
    lk = dict(d.get("look") or {})
    for k, v in (("motion", motion), ("illust", illust), ("footage", footage)):
        if v:
            lk[k] = v
    if motion or illust or footage:
        d["look"] = lk
        p.write_text(yaml.safe_dump(d, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return lk


# ---------------------------------------------------------------- 화풍 목록 갤러리 (2026-11-20 사용자: "화풍목록 보여줘 하면 … 예시를 볼 수 있도록 — 시각적으로")
GALLERY_URL = "https://claude.ai/artifact/K4CRgsyTYsWGCDw5RoCtam"   # 공유 페이지 — 다시 만들면 같은 주소에 올림 (skills/looks-gallery)
FOOTAGE_SRC = "https://assets.mixkit.co/videos/49137/49137-720.mp4"   # 색보정 비교용 실사 (Mixkit 무료 라이선스)
FONT_FAMILY = {"NanumGothic": "'Nanum Gothic'", "NanumMyeongjo": "'Nanum Myeongjo'", "NanumPenScript": "'Nanum Pen Script'"}


def examples_dir() -> Path:
    """삽화 예시 그림을 두는 곳: YTFLOW_DRIVE/looks (PC) → ~/.cache/ytflow/looks. 파일 이름 = <화풍 id>.png|jpg"""
    import os
    d = os.environ.get("YTFLOW_DRIVE")
    p = Path(d) / "looks" if d else Path.home() / ".cache" / "ytflow" / "looks"
    p.mkdir(parents=True, exist_ok=True)
    return p


def _b64_jpg(path: Path, width: int = 720) -> str:
    import base64
    import subprocess
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "x.jpg"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(path), "-vf", f"scale={width}:-2", "-q:v", "5", str(out)], check=True)
        return "data:image/jpeg;base64," + base64.b64encode(out.read_bytes()).decode()


def _footage_frames() -> dict:
    """실사 한 장면에 색보정마다 적용한 정지 화면 (원본 + 각 vf)."""
    import base64
    import subprocess
    import tempfile
    import urllib.request
    cache = Path.home() / ".cache" / "ytflow" / "looks"
    cache.mkdir(parents=True, exist_ok=True)
    src = cache / "footage_src.mp4"
    if not src.exists():
        urllib.request.urlretrieve(FOOTAGE_SRC, src)
    out = {}
    with tempfile.TemporaryDirectory() as td:
        for lid, d in [("_raw", {"vf": "null"})] + list((load().get("footage") or {}).items()):
            o = Path(td) / f"{lid}.jpg"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "3", "-i", str(src), "-frames:v", "1",
                            "-vf", f"{d.get('vf') or 'null'},scale=720:-2", "-q:v", "5", str(o)], check=True)
            out[lid] = "data:image/jpeg;base64," + base64.b64encode(o.read_bytes()).decode()
    return out


def _motion_card(lid: str, d: dict, frames: dict) -> str:
    """같은 장면(제목 → 막대 두 개 → 강조 라벨)을 그 화풍의 색·글꼴·바탕으로 — 실제로 움직이는 미리보기."""
    import html as H
    from . import skin as _skin
    if d.get("skin"):
        sk = _skin.load(d["skin"])
        p = sk["palette"]
        bg = sk.get("background") or {}
        ft = (sk.get("fonts") or {}).get("title", "NanumGothic-ExtraBold.ttf")
        fam = next((v for k, v in FONT_FAMILY.items() if ft.startswith(k)), "'Nanum Gothic'")
        base, ink, acc, card, line = p["base"], p["ink"], p["accent"], p["card"], p.get("line", "#999")
        t = bg.get("type", "flat")
        layer = {"grid": f"repeating-linear-gradient(0deg,transparent 0 23px,{bg.get('grid_color', '#24497C')} 23px 24px),repeating-linear-gradient(90deg,transparent 0 23px,{bg.get('grid_color', '#24497C')} 23px 24px),",
                 "dark": "radial-gradient(ellipse at 50% 45%,rgba(255,255,255,.06),rgba(0,0,0,.45)),",
                 "grain": "radial-gradient(ellipse at 50% 45%,rgba(255,255,255,.18),rgba(0,0,0,.12)),",
                 "paper": "radial-gradient(ellipse at 30% 20%,rgba(255,255,255,.5),rgba(0,0,0,.08)),"}.get(t, "")
        back = f"background:{layer}{base}"
        grain = '<i class="grain"></i>' if t in ("dark", "grain", "paper") else ""
        title_w = "font-weight:700"
    else:   # 실사 위 그래픽 — 바탕이 실사
        base, ink, acc, card, line = "#000", "#fff", "#FFD23F", "rgba(10,12,16,.7)", "#fff"
        back = f"background:url({frames.get('warm-doc', '')}) center/cover"
        grain, fam, title_w = "", "'Nanum Gothic'", "font-weight:800"
    shadow = "text-shadow:0 2px 6px rgba(0,0,0,.7);" if not d.get("skin") else ""
    return f"""<figure class="mg" style="{back};--base:{base};--ink:{ink};--acc:{acc};--card:{card};--ln:{line}">
  {grain}<div class="mg-t" style="font-family:{fam};{title_w};{shadow}">고를 게 많으면<b>?</b></div>
  <div class="mg-row r1"><span style="{shadow}">24가지</span><em class="bar b1"></em><strong style="{shadow}">60%</strong></div>
  <div class="mg-row r2"><span style="{shadow}">6가지</span><em class="bar b2"></em><strong style="{shadow}">40%</strong></div>
  <div class="mg-tag">멈춘 손님</div>
</figure>"""


def gallery(out: Path, examples: Path | None = None) -> Path:
    """화풍 목록을 눈으로 고르는 한 장짜리 페이지 (자체 완결 HTML — 예시 그림은 안에 담김)."""
    import html as H
    data = load()
    frames = _footage_frames()
    ex = examples or examples_dir()

    def meta(lid, d):
        st = d.get("status", "")
        return (f'<figcaption><div class="row"><b>{H.escape(d.get("name", lid))}</b><span class="st {st}">{STATUS.get(st, st)}</span></div>'
                f'<code>{lid}</code><p>{H.escape(d.get("look", ""))}</p>'
                f'<p class="fit"><span>어울림</span>{H.escape(d.get("fits", ""))}</p>'
                + (f'<p class="avoid"><span>피함</span>{H.escape(d.get("avoid", ""))}</p>' if d.get("avoid") else "") + "</figcaption>")

    cards = {"motion": [], "illust": [], "footage": []}
    for lid, d in (data.get("motion") or {}).items():
        cards["motion"].append(f'<article class="card">{_motion_card(lid, d, frames)}{meta(lid, d)}</article>')
    have = 0
    for lid, d in (data.get("illust") or {}).items():
        img = next((p for p in (ex / f"{lid}.png", ex / f"{lid}.jpg", ex / f"{lid}.jpeg") if p.exists()), None)
        if lid == "doc-collage":   # 그림 생성이 아니라 실제 자료를 오려 붙임 — 여기서 바로 보여 줌
            have += 1
            vis = (f'<div class="col"><img src="{frames["_raw"]}" alt="자료 사진"><div class="memo"><small>Iyengar &amp; Lepper (2000), JPSP</small>'
                   '<p>멈춘 손님 중 산 사람<br>6가지 <mark>30%</mark> · 24가지 <mark>3%</mark></p></div>'
                   '<i class="tape"></i></div>')
        elif img:
            have += 1
            vis = f'<img src="{_b64_jpg(img)}" alt="{H.escape(d.get("name", lid))} 예시">'
        else:
            vis = ('<div class="ph"><b>예시 그림 준비 중</b><span>같은 장면(진열대 앞에서 잼을 고르는 사람)을 이 화풍으로 그리면 여기에 들어갑니다 — PC 에서 <code>python -m ytflow looks --draw codex</code></span></div>')
        cards["illust"].append(f'<article class="card"><figure class="pic">{vis}</figure>{meta(lid, d)}</article>')
    cards["footage"].append(f'<article class="card"><figure class="pic"><img src="{frames["_raw"]}" alt="원본"></figure>'
                            f'<figcaption><div class="row"><b>원본 (보정 전)</b></div><p>비교용 원본 클립 화면 (Mixkit 무료 클립)</p></figcaption></article>')
    for lid, d in (data.get("footage") or {}).items():
        cards["footage"].append(f'<article class="card"><figure class="pic"><img src="{frames[lid]}" alt="{H.escape(d.get("name", lid))}"></figure>{meta(lid, d)}</article>')

    n_ill = len(data.get("illust") or {})
    sections = [
        ("motion", "모션그래픽 화풍", "같은 장면(제목 → 막대 두 개 → 라벨)을 화풍마다 그 색·글꼴·바탕으로 움직여 보여 줍니다. 쉽게 설명해야 하는 박자에 씁니다."),
        ("illust", "삽화 화풍", f"실사도 모션그래픽도 어려운 박자에만 부분적으로 씁니다. 같은 장면을 화풍마다 그린 예시 {have}/{n_ill}."),
        ("footage", "실사 색보정", "같은 실사 화면에 색보정을 바꿔 적용한 실제 화면입니다. 한 편의 클립은 같은 보정으로 묶습니다."),
    ]
    body = "".join(f'<section id="{k}"><h2>{t}</h2><p class="lead">{L}</p><div class="grid">{"".join(cards[k])}</div></section>' for k, t, L in sections)
    page = PAGE.replace("{{BODY}}", body).replace("{{N}}", str(sum(len(v) for v in cards.values()) - 1))
    out = Path(out)
    out.write_text(page, encoding="utf-8")
    return out


PAGE = """<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ytflow 화풍 목록</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@400;700;800&family=Nanum+Myeongjo:wght@700;800&family=Nanum+Pen+Script&display=swap">
<style>
:root{--bg:#f5f4f0;--panel:#fff;--fg:#1b1d22;--muted:#5f6470;--line:#dedbd3;--ok:#1f8a4c;--trial:#b26b00;--av:#3358d4;color-scheme:light}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#14161b;--panel:#1d2027;--fg:#e9eaee;--muted:#a0a6b3;--line:#2e333e;--ok:#5fd394;--trial:#f0b04f;--av:#7c9bff;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#14161b;--panel:#1d2027;--fg:#e9eaee;--muted:#a0a6b3;--line:#2e333e;--ok:#5fd394;--trial:#f0b04f;--av:#7c9bff;color-scheme:dark}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.55 'Nanum Gothic',system-ui,sans-serif}
.wrap{max-width:1280px;margin:0 auto;padding:20px 16px 48px}
header h1{margin:0;font-size:24px;font-weight:800}header p{margin:4px 0 0;color:var(--muted);max-width:70ch}
nav{display:flex;gap:6px;flex-wrap:wrap;margin:16px 0 4px;position:sticky;top:0;background:var(--bg);padding:8px 0;z-index:2}
nav a{color:var(--fg);text-decoration:none;border:1px solid var(--line);border-radius:999px;padding:4px 12px;font-size:13px}
section{margin-top:28px}h2{margin:0;font-size:19px}.lead{margin:2px 0 12px;color:var(--muted);font-size:13.5px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:14px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;overflow:hidden;display:flex;flex-direction:column}
figure{margin:0}.pic{aspect-ratio:16/9;background:#000;display:grid;place-items:center;overflow:hidden}.pic img{width:100%;height:100%;object-fit:cover;display:block}
.ph{background:repeating-linear-gradient(45deg,var(--bg) 0 10px,var(--panel) 10px 20px);width:100%;height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;gap:6px;padding:16px;text-align:center;color:var(--muted)}
.ph b{color:var(--fg)}.ph span{font-size:12.5px}
figcaption{padding:10px 12px 12px;display:flex;flex-direction:column;gap:4px}
figcaption .row{display:flex;justify-content:space-between;gap:8px;align-items:center}figcaption code{font-size:12px;color:var(--muted)}
figcaption p{margin:0;font-size:13px}.fit span,.avoid span{display:inline-block;font-size:11px;border:1px solid var(--line);border-radius:4px;padding:0 5px;margin-right:6px;color:var(--muted)}
.avoid{color:var(--muted)}
.st{font-size:11.5px;border-radius:999px;padding:1px 8px;border:1px solid currentColor;white-space:nowrap}.st.approved{color:var(--ok)}.st.trial{color:var(--trial)}.st.available{color:var(--av)}
.col{position:relative;width:100%;height:100%;background:#e9e3d6}.col img{position:absolute;left:6%;top:9%;width:50%;height:auto;transform:rotate(-3deg);box-shadow:0 4px 12px rgba(0,0,0,.35);border:6px solid #fff;filter:grayscale(.3)}
.memo{position:absolute;right:5%;top:22%;width:44%;background:#fffdf6;color:#222;padding:8px 10px;transform:rotate(2deg);box-shadow:0 3px 10px rgba(0,0,0,.25);font:12px/1.45 Georgia,serif}.memo small{font:11px 'Nanum Gothic';color:#666}.memo p{margin:4px 0 0}.memo mark{background:#ffe066}
.tape{position:absolute;left:22%;top:5%;width:70px;height:20px;background:rgba(255,240,180,.75);transform:rotate(-8deg)}
.how{margin-top:28px;background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px 16px;font-size:13.5px}.how code{background:var(--bg);padding:1px 6px;border-radius:4px}
/* 모션그래픽 미리보기 — 6초마다 반복 */
.mg{position:relative;aspect-ratio:16/9;overflow:hidden;color:var(--ink);font-family:'Nanum Gothic',sans-serif}
.mg .grain{position:absolute;inset:0;opacity:.18;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2'/%3E%3C/filter%3E%3Crect width='120' height='120' filter='url(%23n)' opacity='.6'/%3E%3C/svg%3E");mix-blend-mode:overlay}
.mg-t{position:absolute;left:7%;top:12%;font-size:clamp(18px,6.2cqw,30px);animation:mgT 6s infinite}.mg-t b{color:var(--acc)}
.mg{container-type:inline-size}
.mg-row{position:absolute;left:7%;right:7%;display:flex;align-items:center;gap:8px;font-size:clamp(11px,3.6cqw,15px);font-weight:700}
.mg-row span{width:3.6em}.mg-row strong{font-size:1.25em;font-weight:800}
.r1{top:46%}.r2{top:64%}
.bar{display:block;height:clamp(10px,4.5cqw,20px);background:var(--acc);border-radius:2px;transform-origin:left;transform:scaleX(0)}
.b1{width:60%;animation:mgB 6s .6s infinite}.b2{width:40%;background:var(--ink);opacity:.85;animation:mgB 6s 1.1s infinite}
.mg-row strong{opacity:0;animation:mgF 6s 1.3s infinite}.r2 strong{animation-delay:1.8s}
.mg-tag{position:absolute;right:7%;top:14%;background:var(--acc);color:var(--base);border:0;border-radius:4px;padding:2px 8px;font-size:clamp(10px,3cqw,13px);font-weight:700;opacity:0;animation:mgP 6s 2.2s infinite}
@keyframes mgT{0%{opacity:0;transform:translateY(8px)}8%,88%{opacity:1;transform:none}100%{opacity:0}}
@keyframes mgB{0%{transform:scaleX(0)}18%,80%{transform:scaleX(1)}92%,100%{transform:scaleX(0)}}
@keyframes mgF{0%{opacity:0}8%,75%{opacity:1}88%,100%{opacity:0}}
@keyframes mgP{0%{opacity:0;transform:scale(.6)}6%{opacity:1;transform:scale(1.08)}10%,70%{opacity:1;transform:scale(1)}82%,100%{opacity:0}}
@media (prefers-reduced-motion:reduce){.mg *{animation:none!important;opacity:1!important;transform:none!important}}
</style></head><body><div class="wrap">
<header><h1>화풍 목록</h1><p>영상마다 언제든 고르는 '보이는 모습' {{N}}가지. 무엇으로 보여 줄지(실사·모션그래픽·삽화)는 박자가 하는 일이 정하고(manual/12 §0-1), 여기서는 그 화풍만 고릅니다. 상태: <b style="color:var(--ok)">합격</b> · <b style="color:var(--trial)">시안</b>(판정 전) · <b style="color:var(--av)">사용 가능</b>.</p></header>
<nav><a href="#motion">모션그래픽</a><a href="#illust">삽화</a><a href="#footage">실사 색보정</a></nav>
{{BODY}}
<div class="how"><b>고르는 법</b> — 대화에서 "이 영상은 칠판 + 귀여운 그림으로" 처럼 말하거나, <code>python -m ytflow look &lt;프로젝트&gt; --motion chalkboard --illust cute-casual --footage warm-doc</code>. 고른 값은 그 영상의 edit.yaml 에 남고 렌더에 바로 쓰입니다. 목록 원본: <code>styles/looks.yaml</code>.</div>
</div></body></html>"""


EXAMPLE_SCENE = ("A young woman stands in a supermarket aisle, hesitating in front of a long shelf crowded with dozens of colorful jam jars, "
                 "one hand raised toward the jars, a shopping basket on her arm. Wide 16:9 landscape composition with some empty space at the top. ")


def draw_examples(backend: str = "manual", only: list[str] | None = None) -> list[str]:
    """예시가 없는 삽화 화풍마다 같은 장면을 그림. codex = 사용자 PC 의 Codex 구독(무료 길), manual = 주문서만.
    ElevenLabs 로는 그리지 않음 (2026-11-20 사용자: '일레븐랩스는 이미지 생성으로 사용하지 말아주세요')."""
    if backend in ("elevenlabs", "eleven"):
        raise SystemExit("[looks] ElevenLabs 로는 그림을 만들지 않습니다 (2026-11-20 사용자) — codex 또는 manual")
    ex = examples_dir()
    lines, done = ["# 화풍 예시 그림 주문서 (같은 장면 · 화풍만 바꿈)", "", f"저장 위치: {ex}/<화풍 id>.png", ""], []
    for lid, d in (load().get("illust") or {}).items():
        if only and lid not in only:
            continue
        if not d.get("prompt") or any((ex / f"{lid}.{e}").exists() for e in ("png", "jpg", "jpeg")):
            continue
        prompt = EXAMPLE_SCENE + d["prompt"]
        lines += [f"## {lid} — {d.get('name', '')}", "", "```", prompt, "```", ""]
        if backend == "codex":
            from . import imagegen
            imagegen.gen_codex(prompt, ex / f"{lid}.png")
            done.append(lid)
    (ex / "ORDERS.md").write_text("\n".join(lines), encoding="utf-8")
    return done
