"""연출 예시 목록 — 따로 둔 완성본 페이지 (2026-11-20 사용자: "기존 목록에 합치되 그 완성본은 따로둬").

styles/visuals.yaml 의 장면 종류·전환·겹치기 전부를 묶음별로: 실제 렌더 세 컷 + ▶ 움직이는 영상 + 제작 명세(만드는 법·렌더러·실제 움직임 순서).
'영상 구성요소 목록'(화풍목록 보여줘, skills/looks-gallery)과 별개의 페이지 — 공유 주소 PAGE_URL 에 다시 올림.

  python scripts/visual_page.py <out.html>    (예시 그림·영상: <예시 폴더>/scenes/<id>.jpg · scenes/clips/<id>.mp4 — scripts/visual_catalog.py)
"""
from __future__ import annotations

import html as H
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from ytflow.stages import looks  # noqa: E402
from visual_spec import PAGE_URL  # noqa: E402,F401

VISUALS = ROOT / "styles" / "visuals.yaml"


def load_visuals() -> dict:
    import yaml
    return yaml.safe_load(VISUALS.read_text(encoding="utf-8")) or {}


def visual_image(kind: str, vid: str, ex: Path) -> Path | None:
    p = ex / "scenes" / ((f"tr_{vid}" if kind == "transition" else vid.replace("@", "_")) + ".jpg")
    return p if p.exists() else None

# ---------------------------------------------------------------- 따로 둔 완성본: 장면 종류·전환·겹치기만 (2026-11-20 사용자: "기존 목록에 합치되 그 완성본은 따로둬")
SPEC_DIR = ROOT / "styles" / "visuals"   # 제작 명세 (scripts/visual_spec.py)


def build_visuals(out: Path, examples: Path | None = None) -> Path:
    """styles/visuals.yaml 전부를 묶음(group)별로 — 한 칸 = 실제 렌더한 세 컷. 구성요소 목록(build)과 같은 항목·그림."""
    v = load_visuals()
    ex = examples or looks.examples_dir()
    groups = v.get("groups") or {}
    by, n, have = {g: [] for g in groups}, 0, 0
    for kind in ("scene", "transition", "overlay"):
        for vid, d in (v.get(kind) or {}).items():
            img = visual_image(kind, vid, ex)
            have += bool(img)
            pic = (f'<img src="{looks._b64_jpg(img, 1200)}" alt="{H.escape(d.get("name", vid))} 예시 세 컷">' if img else
                   f'<div class="ph"><b>예시 그림 준비 중</b><span><code>python scripts/visual_catalog.py &lt;작업 폴더&gt; --only {H.escape(vid)}</code></span></div>')
            key = (f"tr_{vid}" if kind == "transition" else vid).replace("@", "_")
            clip = ex / "scenes" / "clips" / f"{key}.mp4"
            if clip.exists():   # 사진만으로는 다 못 보여 줌 (2026-11-20 사용자) — 실제 렌더 영상을 페이지에 담음 (640px, 소리 없음)
                import base64
                vsrc = "data:video/mp4;base64," + base64.b64encode(clip.read_bytes()).decode()
                pic = (f'<div class="vwrap">{pic}<video muted loop playsinline preload="none" data-src="{vsrc}"></video>'
                       f'<button class="play" type="button" aria-label="{H.escape(d.get("name", vid))} 움직임 보기">▶ 움직임 보기</button></div>')
            sp = SPEC_DIR / f"{key}.json"
            spec = json.loads(sp.read_text(encoding="utf-8")) if sp.exists() else {}
            build = d.get("build") or []
            build = build if isinstance(build, list) else [build]
            how = ""
            if build or spec:
                how = ('<details class="how1"><summary>만드는 법 · 실제 움직임 순서</summary>'
                       + ("<ul>" + "".join(f"<li>{H.escape(x)}</li>" for x in build) + "</ul>" if build else "")
                       + (f'<p class="key"><span>렌더러</span><code>{H.escape(spec.get("renderer", ""))}</code></p>' if spec.get("renderer") else "")
                       + (f'<p class="key"><span>읽는 키</span><code>장면 {H.escape(", ".join(spec.get("scene_fields") or []) or "—")} · '
                          f'박자 {H.escape(", ".join(spec.get("beat_fields") or []) or "—")}</code></p>' if spec.get("renderer") else "")
                       + (f'<p class="key"><span>예시 대본</span><code>styles/visuals/{key}.json</code></p>' if spec else "")
                       + "".join(f'<pre>{H.escape(chr(10).join(t["events"]))}</pre>' for t in spec.get("timeline", []))
                       + "</details>")
            cap = (f'<figcaption><div class="row"><b>{H.escape(d.get("name", vid))}</b><code class="id">{H.escape(vid)}</code></div>'
                   f'<p>{H.escape(d.get("what", ""))}</p><p class="fit"><span>언제</span>{H.escape(d.get("fits", ""))}</p>'
                   + (f'<p class="avoid"><span>주의</span>{H.escape(d["avoid"])}</p>' if d.get("avoid") else "")
                   + f'<p class="key"><span>대본</span><code>{H.escape(d.get("key", ""))}</code></p>'
                   + (f'<p class="avoid"><span>예시</span>{H.escape(d["note"])}</p>' if d.get("note") else "") + how + "</figcaption>")
            by.setdefault(d.get("group", "structure"), []).append(f'<article class="card"><figure class="strip">{pic}</figure>{cap}</article>')
            n += 1
    nav = "".join(f'<a href="#v-{g}">{H.escape(t)}</a>' for g, t in groups.items() if by.get(g))
    body = "".join(f'<section id="v-{g}"><h2>{H.escape(t)} <small>{len(by[g])}</small></h2><div class="grid">{"".join(by[g])}</div></section>'
                   for g, t in groups.items() if by.get(g))
    page = VPAGE.replace("{{NAV}}", nav).replace("{{BODY}}", body).replace("{{N}}", str(n)).replace("{{H}}", str(have))
    out = Path(out)
    out.write_text(page, encoding="utf-8")
    return out


VPAGE = """<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>연출 예시 목록</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@400;700;800&display=swap">
<style>
:root{--bg:#f5f4f0;--panel:#fff;--fg:#1b1d22;--muted:#5f6470;--line:#dedbd3;color-scheme:light}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#14161b;--panel:#1d2027;--fg:#e9eaee;--muted:#a0a6b3;--line:#2e333e;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#14161b;--panel:#1d2027;--fg:#e9eaee;--muted:#a0a6b3;--line:#2e333e;color-scheme:dark}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.55 'Nanum Gothic',system-ui,sans-serif}
.wrap{max-width:1280px;margin:0 auto;padding:20px 16px 48px}header h1{margin:0;font-size:24px;font-weight:800}header p{margin:4px 0 0;color:var(--muted);max-width:75ch}
nav{display:flex;gap:6px;flex-wrap:wrap;margin:16px 0 4px;position:sticky;top:0;background:var(--bg);padding:8px 0;z-index:2}
nav a{color:var(--fg);text-decoration:none;border:1px solid var(--line);border-radius:999px;padding:4px 12px;font-size:13px}
section{margin-top:28px}h2{margin:0 0 12px;font-size:19px}h2 small{color:var(--muted);font-weight:400;font-size:13px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,520px),1fr));gap:14px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;overflow:hidden;display:flex;flex-direction:column}
figure{margin:0}.strip{background:#111}.strip img{width:100%;height:auto;display:block}
.ph{aspect-ratio:16/3;background:repeating-linear-gradient(45deg,var(--bg) 0 10px,var(--panel) 10px 20px);display:flex;flex-direction:column;justify-content:center;align-items:center;gap:4px;color:var(--muted);text-align:center;padding:8px}.ph b{color:var(--fg)}.ph span{font-size:12px}
figcaption{padding:10px 12px 12px;display:flex;flex-direction:column;gap:4px}figcaption .row{display:flex;justify-content:space-between;gap:8px;align-items:center}
figcaption p{margin:0;font-size:13px}code{font-size:12px}code.id{font-size:12.5px;background:var(--bg);padding:1px 6px;border-radius:4px}
.fit span,.avoid span,.key span{display:inline-block;font-size:11px;border:1px solid var(--line);border-radius:4px;padding:0 5px;margin-right:6px;color:var(--muted)}.avoid{color:var(--muted)}.key code{word-break:break-all}
.how{margin-top:28px;background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px 16px;font-size:13.5px}
.vwrap{position:relative}.vwrap video{display:none;width:100%;height:auto;aspect-ratio:16/9;background:#000}.vwrap.on img{display:none}.vwrap.on video{display:block}
.play{position:absolute;right:10px;bottom:10px;border:0;border-radius:999px;padding:6px 14px;background:rgba(0,0,0,.72);color:#fff;font:700 13px 'Nanum Gothic',sans-serif;cursor:pointer}
.play:focus-visible{outline:2px solid #fff;outline-offset:2px}
.how1{margin-top:6px;font-size:13px}.how1 summary{cursor:pointer;color:var(--fg);font-weight:700}.how1 ul{margin:6px 0;padding-left:18px}.how1 li{margin:2px 0}
.how1 pre{background:var(--bg);border:1px solid var(--line);border-radius:6px;padding:8px;font-size:11.5px;line-height:1.5;overflow-x:auto;max-height:240px;margin:6px 0 0}
</style></head><body><div class="wrap">
<header><h1>연출 예시 목록</h1><p>화면에서 무엇이 어떻게 움직이나 — 장면 종류·전환·겹치기 {{N}}가지 (예시 그림 {{H}}개). 그림 한 칸은 실제로 렌더한 세 컷(처음·가운데·끝 무렵, 전환은 앞 장면 끝 → 다음 장면 처음)이고, ▶ 를 누르면 실제 렌더 영상이 움직입니다. 칸마다 「만드는 법 · 실제 움직임 순서」를 열면 다시 만들 수 있는 제작 명세가 나옵니다(같은 내용이 저장소 styles/hybrid/scenes/&lt;장면&gt;.md 에). 이름이 기억나지 않으면 그림으로 고르고 "<code>id</code> 로 해줘" 라고 말하세요.</p></header>
<nav>{{NAV}}</nav>
{{BODY}}
<div class="how">화풍·자막·소리까지 모든 구성요소를 섞어 고르는 곳은 <b>'영상 구성요소 · 스타일 목록'</b>(화풍목록 보여줘)입니다. 이 페이지는 그중 연출(장면 종류·전환·겹치기)만 따로 모아, 실제 렌더 영상과 다시 만들 수 있는 제작 명세를 붙인 완성본입니다. 장면마다 만드는 법은 저장소 <code>styles/hybrid/scenes/</code>. 목록 원본 <code>styles/visuals.yaml</code>, 예시 그림 <code>scripts/visual_catalog.py</code>.</div>
</div>
<script>
document.querySelectorAll('.vwrap .play').forEach(function(b){b.addEventListener('click',function(){var w=b.parentNode,v=w.querySelector('video');
 if(!w.classList.contains('on')){if(!v.src)v.src=v.dataset.src;w.classList.add('on');b.textContent='■ 세 컷으로';v.play().catch(function(){})}
 else{v.pause();w.classList.remove('on');b.textContent='▶ 움직임 보기'}})});
</script></body></html>"""


if __name__ == "__main__":
    out = build_visuals(Path(sys.argv[1]))
    print(f"[visual-page] {out} → 공유 페이지 {PAGE_URL} 에 다시 올림")
