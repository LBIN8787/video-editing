"""연출 제작 명세 (2026-11-20 사용자: "구성 요소별로 제작 메뉴얼 … 그게 아니면 나중에 재구현 불가능할거아니야
또 예시사진으로는 사실 전부 보여주지 못하고 약간 괴리가 생기니까").

예시 그림을 만든 렌더(scripts/visual_catalog.py)마다 styles/visuals/<id>.json 에 남긴다:
  - scenes        그 그림을 만든 대본 그대로 (다시 만들면 같은 화면)
  - renderer      그리는 함수의 파일:줄 · scene_fields / beat_fields (그 함수가 읽는 대본 키)
  - timeline      렌더한 HTML 의 GSAP 시간축을 사람이 읽는 순서로 ('1.20s 「호텔 예약」 튀어나옴')
사람이 쓰는 부분(화면 구성·움직임 원리·소리·예시와 실제의 차이)은 styles/visuals.yaml 의 build / note.
장면별 만드는 법: python scripts/visual_spec.py --md → styles/hybrid/scenes/<장면>.md (손으로 쓴 파일은 건드리지 않음) · transitions.md · overlays.md
"""
from __future__ import annotations

import html as _h
import inspect
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
SPECS = ROOT / "styles" / "visuals"
SCENES_MD = ROOT / "styles" / "hybrid" / "scenes"
PAGE_URL = "https://claude.ai/artifact/SPHyXdpGmcdPwMQu7cpMdP"   # 연출 예시 목록(따로 둔 완성본) — 세 컷 + 움직이는 영상 + 제작 명세


def _el_text(htm: str, eid: str) -> str:
    """id 가 붙은 요소의 글자(안쪽 요소까지) — 없으면 요소 종류(선·그림·영상)."""
    for cand in (eid, eid + "w"):
        m = re.search(rf'<(\w+)[^>]*\bid="{re.escape(cand)}"[^>]*>', htm)
        if not m:
            continue
        tag = m.group(1)
        if tag in ("path", "img", "video", "line", "rect", "circle"):
            return {"path": "선", "img": "그림", "video": "영상", "line": "선", "rect": "도형", "circle": "원"}[tag]
        chunk = htm[m.end():m.end() + 2500]
        depth, i, end = 1, 0, len(chunk)   # 같은 요소가 닫힐 때까지
        for t in re.finditer(r"<(/?)(\w+)[^>]*?(/?)>", chunk):
            if t.group(2) != tag or t.group(3):
                continue
            depth += -1 if t.group(1) else 1
            if depth == 0:
                end = t.start()
                break
        segs = [" ".join(_h.unescape(x).split()) for x in re.split(r"<[^>]+>", re.sub(r"<svg.*?</svg>", " ", chunk[:end], flags=re.S))]
        txt = next((x for x in segs if x), "")   # 첫 글자 덩어리만 (카드 안에 숨겨 둔 상태 글자까지 붙지 않게)
        if txt:
            return txt[:28] + ("…" if len(txt) > 28 else "")
        st = m.group(0)
        for pat, name in (("0 0 0 3000px", "어둡게 깐 막(스포트라이트)"), ("#D7F25C", "형광펜"), ("#F3D36B", "형광펜"),
                          ("border-radius:50%", "원·배지"), ("inset:0", "화면 덮개"), ("height:4px", "진행 막대"), ("height:12px", "밑줄 바")):
            if pat in st:
                return name
        return {"svg": "그림", "g": "선 묶음"}.get(tag, "")
    return ""


def timeline(html_path: Path, limit: int = 40) -> list[str]:
    """렌더한 장면 HTML 의 시간축 → '시각 대상 동작' 줄들."""
    htm = html_path.read_text(encoding="utf-8")
    ev = []
    for m in re.finditer(r'tl\.(fromTo|to|set)\("([^"]+)",(\{[^}]*\})(?:,(\{[^}]*\}))?,([\d.]+)\)', htm):
        kind, sel, a, b, t = m.groups()
        props, frm, t = (b or a), (a if kind == "fromTo" else ""), float(t)
        first = sel.split(",")[0]
        if first.startswith(".r"):
            who = "손그림 선"
        elif first in ("#layer", "#cam"):
            who = "화면 전체(카메라)"
        elif first == "#root":
            who = "장면 전체"
        else:
            base = re.sub(r"(p|u|m|s|v|f|w|pb)$", "", first.lstrip("#")) if re.match(r"#e\d+[a-z]+$", first) else first.lstrip("#")
            who = _el_text(htm, first.lstrip("#")) or _el_text(htm, base) or "요소"
            if who not in ("선", "그림", "영상", "선 묶음", "요소"):
                who = f"「{who}」"
        if "strokeDashoffset:0" in props:
            act = "그려짐"
        elif "strokeDashoffset:-" in props:
            act = "점선이 흐름"
        elif "clipPath" in props:
            act = "원으로 열림" if "circle(0" in frm else "원으로 닫힘"
        elif "borderColor" in props:
            act = "테두리 색 → " + re.search(r'borderColor:"([^"]+)"', props).group(1)
        elif "backgroundColor" in props:
            act = "바탕 색 바뀜" + (" (커지며 화면을 덮음)" if "scale:" in props else "")
        elif "yoyo" in props:
            act = "흔들림" if "x:" in props else "둥실 움직임(반복)"
        elif "scaleX" in props:
            act = "옆으로 펼쳐짐"
        elif "opacity:0" in props and "opacity:1" not in props:
            act = "사라짐"
        elif "scale:1.8" in frm or "scale:2" in frm:
            act = "크게서 찍힘(도장)"
        elif "back.out" in props:
            act = "튀어나옴"
        elif "scale:" in props and first in ("#layer", "#cam", "#root"):
            act = "확대·이동"
        elif "x:" in frm:
            act = "옆에서 밀려 들어옴"
        elif "y:" in frm:
            act = "아래에서 떠오름"
        elif "opacity:1" in props or kind == "set":
            act = "나타남"
        else:
            act = "움직임"
        ev.append((t, f"{t:5.2f}s {who} {act}"))
    for m in re.finditer(r"tl\.to\(o,\{v:([\d.]+).*?\},([\d.]+)\)", htm):
        ev.append((float(m.group(2)), f"{float(m.group(2)):5.2f}s 숫자가 {m.group(1)} 까지 세어 올라감"))
    ev.sort(key=lambda x: x[0])
    out, prev = [], None
    for _, s in ev:
        if s[6:] != prev:
            out.append(s)
        prev = s[6:]
    return out[:limit] + ([f"… (총 {len(out)}개)"] if len(out) > limit else [])


def renderer_info(t: str, key: str = "") -> dict:
    from ytflow.stages import hybrid, uiflow
    f = hybrid.RENDER.get(t)
    if t == "chapter":   # 장 표지는 여러 겹으로 감싸여 있음(uiflow two-line → edit10 photo → identity → hybrid 종이) — 이 예시가 쓰는 함수로
        f = uiflow.chapter_two_line if key.endswith("two-line") else hybrid.s_chapter
    if not f:
        return {}
    src, ln = inspect.getsourcelines(f)
    code = "".join(src)
    if len(src) <= 4:   # 등록용 감싸기(chapter·explain) — 그리는 함수까지 따라감
        mod = inspect.getmodule(f)
        for n in re.findall(r"\b(chapter_\w+|s_\w+|_board)\(", code):
            g = getattr(mod, n, None)
            if callable(g):
                f = g
                src, ln = inspect.getsourcelines(g)
                code = "".join(src)
                break
        if t in ("afterline", "spread", "share", "motionboard"):
            mod = inspect.getmodule(f)
            g = getattr(mod, {"motionboard": "s_board"}.get(t, f"s_{t}"), None)
            if callable(g):
                f = g
                src, ln = inspect.getsourcelines(g)
                code = "".join(src)
    file = Path(inspect.getsourcefile(f)).resolve().relative_to(ROOT).as_posix()
    flds = sorted(set(re.findall(r'sc(?:\.get\(|\[)"(\w+)"', code)) - {"beats"})
    bfl = sorted(set(re.findall(r'\bb0?(?:\.get\(|\[)"(\w+)"', code)) - {"say"})
    return {"renderer": f"{file}:{ln}", "function": f.__name__,
            "scene_fields": [x for x in flds if not x.startswith("_")], "beat_fields": bfl}


def write_spec(key: str, work: Path, src: str):
    p = work / key.replace("@", "_")
    hj = p / "02_script" / "hybrid.json"
    if not hj.exists():
        return None
    spec = json.loads(hj.read_text(encoding="utf-8"))
    scenes = spec.pop("scenes")
    spec.pop("footage", None)
    spec.pop("title", None)
    info = renderer_info(scenes[0]["type"], key) if not key.startswith("tr_") else \
        {"renderer": "ytflow/stages/edit10.py:apply (전환) · ytflow/stages/uiflow.py:iris_out (모양 매치)"}
    tls = []
    for k, sc in enumerate(scenes, 1):
        h = p / "04_assets" / "hb" / f"scene_{k:03d}" / "index.html"
        if h.exists():
            tls.append({"scene": k, "type": sc["type"], "events": timeline(h)})
    SPECS.mkdir(parents=True, exist_ok=True)
    out = {"id": key, "type": scenes[0]["type"], "example_source": src, **info,
           "rebuild": f"python scripts/visual_catalog.py <작업 폴더> --only {key if not key.startswith('tr_') else 'transitions'} --force",
           "spec_common": spec, "scenes": scenes, "timeline": tls}
    f = SPECS / f"{key.replace('@', '_')}.json"
    f.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    return f


GEN_MARK = "<!-- visual_spec.py 가 만든 파일 — 다시 만들면 덮어씀. 손으로 고치려면 이 줄을 지우세요 -->"


def _beat_table(spec: dict) -> list[str]:
    """예시 렌더의 시간축을 박자 경계와 함께 표로 (손으로 쓴 장면 파일의 '박자표'와 같은 자리)."""
    rows = []
    for tl in spec.get("timeline", []):
        if len(spec.get("timeline", [])) > 1:
            rows.append(f"| **장면 {tl['scene']}** (`{tl['type']}`) | |")
        for e in tl["events"]:
            t, _, what = e.strip().partition("s ")
            if "카메라" in what and "확대" in what:
                continue
            rows.append(f"| {t}초 | {what} |")
    return ["| 시각(예시 렌더) | 화면 |", "|---|---|"] + rows


def _md_one(kind: str, vid: str, d: dict, spec: dict) -> str:
    key = (f"tr_{vid}" if kind == "transition" else vid).replace("@", "_")
    name = d.get("name", vid)
    L = [GEN_MARK, f"# `{vid}` — {name}", "", f"**언제:** {d.get('fits', '')}" + (f" · **피할 때:** {d['avoid']}" if d.get("avoid") else ""), "",
         f"**무엇:** {d.get('what', '')}", "",
         f"**예시 (움직임):** [연출 예시 목록]({PAGE_URL}) 의 `{vid}` 칸 ▶ — 실제 렌더 영상 · 세 컷 그림은 Drive `ytflow/looks/scenes/{key}.jpg`, 영상 `ytflow/looks/scenes/clips/{key}.mp4`"]
    if d.get("note"):
        L.append(f"  - 예시와 실제의 차이: {d['note']}")
    build = d.get("build") or []
    if build:
        L += ["", "## 화면 구성·움직임 원리", ""] + [f"- {x}" for x in (build if isinstance(build, list) else [build])]
    if spec.get("timeline"):
        L += ["", "## 박자표 — 무엇이 언제 나타나나", "",
              "예시 렌더(아래 대본)의 시간축을 그대로 옮긴 것입니다. 시각은 대사 길이에 따라 달라지고, 순서와 간격이 이 장면의 문법입니다.", ""] + _beat_table(spec)
    if spec.get("scenes"):
        ex = [dict(sc) for sc in spec["scenes"]]
        for sc in ex:
            for k in ("id", "chapter"):
                sc.pop(k, None)
        txt = json.dumps(ex[0] if len(ex) == 1 else ex, ensure_ascii=False, indent=1)
        if len(txt) > 2600:
            txt = txt[:2600] + "\n … (전체: styles/visuals/" + key + ".json)"
        L += ["", "## 대본(`02_script/hybrid.json`)에 쓰는 법", "", f"`{d.get('key', '')}`", "", "```json", txt, "```"]
        if spec.get("spec_common"):
            L.append(f"대본 공통 키: `{', '.join(spec['spec_common'])}` (예: map_causal 의 `map`)")
    if spec.get("scene_fields") or spec.get("beat_fields"):
        L += ["", f"읽는 키 — 장면: `{', '.join(spec.get('scene_fields') or []) or '—'}` · 박자: `{', '.join(spec.get('beat_fields') or []) or '—'}` (렌더러 코드에서 자동)"]
    L += ["", "## 만들기", "",
          "`python -m ytflow edit-plan <프로젝트>` → `hybrid.json` 에 위 장면 → `python -m ytflow check <프로젝트> --upto G5` → `python -m ytflow hybrid <프로젝트>`", "",
          f"예시를 다시 렌더: `{spec.get('rebuild', f'python scripts/visual_catalog.py <작업 폴더> --only {vid} --force')}` (그림·영상·이 명세가 함께 갱신)", ""]
    chk = []
    if d.get("avoid"):
        chk.append(d["avoid"])
    chk.append("화면 요소가 말보다 늦거나 빠르지 않은지 (박자 시작에 맞춰 나타남)")
    chk.append("`layout_qa.json` 이 비었는지 — 글자 겹침·대비")
    L += ["## 확인할 것", ""] + [f"- {x}" for x in chk]
    if spec.get("renderer"):
        L += ["", f"코드: `{spec['renderer']}` `{spec.get('function', '')}`"]
    return "\n".join(L) + "\n"


def write_md() -> list[Path]:
    """styles/hybrid/scenes/ — 손으로 쓴 장면 파일은 그대로 두고, 없는 장면만 같은 틀로. 전환·겹치기는 한 파일씩."""
    import yaml
    v = yaml.safe_load((ROOT / "styles" / "visuals.yaml").read_text(encoding="utf-8"))
    SCENES_MD.mkdir(parents=True, exist_ok=True)
    out = []

    def spec_of(kind, vid):
        f = SPECS / f"{(f'tr_{vid}' if kind == 'transition' else vid).replace('@', '_')}.json"
        return json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}

    for vid, d in (v.get("scene") or {}).items():
        f = SCENES_MD / f"{vid.replace('@', '_')}.md"
        if f.exists() and GEN_MARK not in f.read_text(encoding="utf-8"):
            continue   # 손으로 쓴 파일 (박자표·확인할 것이 사람 판단) — 건드리지 않음
        f.write_text(_md_one("scene", vid, d, spec_of("scene", vid)), encoding="utf-8")
        out.append(f)
    for kind, fname, title, lead in (
            ("transition", "transitions.md", "장면 전환 — 렌더러에 있는 전환", "장면 사이 넘어가는 법. 대본의 다음 장면에 `\"tr\": \"<id>\"`(기본 fade, 장 표지는 push). 모양 매치 아이리스만 앞 장면에 `iris_out`."),
            ("overlay", "overlays.md", "겹치기 — 다른 장면 위에 얹는 것", "실사·인과 지도 같은 장면 위에 박자 키 하나로 얹는 연출.")):
        parts = [GEN_MARK, f"# {title}", "", lead, "", f"예시 영상: [연출 예시 목록]({PAGE_URL})", ""]
        for vid, d in (v.get(kind) or {}).items():
            body = _md_one(kind, vid, d, spec_of(kind, vid)).replace(GEN_MARK + "\n", "")
            parts.append(body.replace("\n# ", "\n## ", 1).replace("# `", "## `", 1).replace("\n## ", "\n### ").replace("### `", "## `", 1))
        f = SCENES_MD / fname
        f.write_text("\n".join(parts), encoding="utf-8")
        out.append(f)
    return out


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="work", default="", help="이미 렌더한 작업 폴더(쉼표로 여럿) → 명세 다시 씀")
    ap.add_argument("--md", action="store_true", help="styles/hybrid/scenes/ 에 없는 장면의 만드는 법 + transitions.md·overlays.md")
    a = ap.parse_args()
    if a.work:
        sys.path.insert(0, str(ROOT / "scripts"))
        import visual_catalog as vc
        src = {k: v[2] for k, v in vc.jobs().items()}
        for wd in a.work.split(","):
            for d in sorted(Path(wd).iterdir()):
                if (d / "02_script" / "hybrid.json").exists():
                    key = next((k for k in src if k.replace("@", "_") == d.name), d.name)
                    print("[spec]", key, write_spec(key, Path(wd), src.get(key, "scripts/visual_catalog.py TRANSITIONS")))
    if a.md:
        for f in write_md():
            print("[spec] 만드는 법 →", f.relative_to(ROOT))
