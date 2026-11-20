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


COMPONENTS = ROOT / "styles" / "components.yaml"


def components() -> list[dict]:
    """영상의 구성요소 카테고리마다 고를 수 있는 스타일 [{key, axis, name, what, options: {id: {name, ...}}}]."""
    cats = (yaml.safe_load(COMPONENTS.read_text(encoding="utf-8")) or {}).get("categories", [])
    data = load()
    tech = (yaml.safe_load((ROOT / "styles" / "techniques.yaml").read_text(encoding="utf-8")) or {}).get("techniques", {})
    bgm = (yaml.safe_load((ROOT / "assets" / "bgm" / "bgm.yaml").read_text(encoding="utf-8")) or {}).get("tracks", {})
    for c in cats:
        src = c.get("source") or {}
        if "looks" in src:
            c["options"] = data.get(src["looks"]) or {}
        elif "techniques" in src:
            c["options"] = {k: v for k, v in tech.items() if v.get("group") in src["techniques"]}
        elif "sfx" in src:
            c["options"] = sfx_palettes()
        elif "bgm" in src:
            c["options"] = {k: {"name": k, "look": v.get("mood", ""), "fits": ", ".join(v.get("fits") or []) or "쓰지 않음(판정)",
                                "source": v.get("source") or v.get("credit", "")} for k, v in bgm.items()}
        c["blocks"] = hf_blocks().get(c["key"]) or {}   # 이미 설치된 HyperFrames 블록 중 이 카테고리에 맞는 것 (styles/hyperframes_blocks.yaml)
    return cats


def hf_blocks() -> dict:
    """styles/hyperframes_blocks.yaml {카테고리 key: {블록 이름: {what, maps_to, fit, ...}}} (docs/53 §1)."""
    f = ROOT / "styles" / "hyperframes_blocks.yaml"
    return (yaml.safe_load(f.read_text(encoding="utf-8")) or {}) if f.exists() else {}


SFX = ROOT / "assets" / "sfx" / "sfx.yaml"


def sfx_palettes() -> dict:
    """효과음 묶음 (assets/sfx/sfx.yaml) {id: {name, look, fits, gain, map, status}}."""
    if not SFX.exists():
        return {}
    return (yaml.safe_load(SFX.read_text(encoding="utf-8")) or {}).get("palettes") or {}


def sfx_palette(project_dir: Path) -> dict:
    """이 영상이 고른 효과음 묶음 (edit.yaml look.sfx, 없으면 default)."""
    pals = sfx_palettes()
    sid = (project_look(project_dir) or {}).get("sfx") or "default"
    return pals.get(sid) or pals.get("default") or {"gain": 1.0, "map": {}}


def choose_any(project_dir: Path, pairs: list[str]) -> dict:
    """--set key=id 여러 개 → edit.yaml look.<key>. 카테고리·스타일 이름을 확인하고 없으면 거절."""
    cats = {c["key"]: c for c in components()}
    p = Path(project_dir) / "edit.yaml"
    d = (yaml.safe_load(p.read_text(encoding="utf-8")) or {}) if p.exists() else {}
    lk = dict(d.get("look") or {})
    for kv in pairs:
        k, _, v = kv.partition("=")
        if k not in cats:
            raise SystemExit(f"[look] 카테고리 '{k}' 없음 — {', '.join(cats)}")
        if v not in cats[k]["options"]:
            raise SystemExit(f"[look] '{v}' 는 {cats[k]['name']} 에 없습니다 — {', '.join(cats[k]['options'])}")
        lk[k] = v
    if pairs:
        d["look"] = lk
        p.write_text(yaml.safe_dump(d, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return lk


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


def gallery(out: Path, examples: Path | None = None) -> Path:
    """화풍·연출 갤러리 (looksgallery.build) — 화풍 탭(같은 장면을 화풍마다) + 연출 탭(연출마다 움직이는 예시, 고른 화풍으로 칠함)."""
    from . import looksgallery
    return looksgallery.build(out, examples)


EXAMPLE_SCENE = ("A young woman stands in a supermarket aisle, hesitating in front of a long shelf crowded with dozens of colorful jam jars, "
                 "one hand raised toward the jars, a shopping basket on her arm. Wide 16:9 landscape composition with some empty space at the top. ")


MANIFEST = ROOT / "styles" / "looks_examples.json"   # 어떤 예시 그림이 어디 있나 (git, 그림 파일은 Drive ytflow/looks/)
KST_OFFSET = 9


def _which_backend(backend: str) -> str:
    """auto: 이 컴퓨터에서 쓸 수 있는 무료 길을 차례로 — Codex 구독 → Gemini 키 → 주문서만(사람이 앱에서 그림)."""
    import os
    import shutil
    if backend != "auto":
        return backend
    if shutil.which("codex"):
        return "codex"
    if os.environ.get("GEMINI_API_KEY"):
        return "gemini"
    return "manual"


def _record(lid: str, f: Path, backend: str) -> None:
    import datetime as dt
    import hashlib
    import json
    m = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else {}
    m[lid] = {"file": f"looks/{f.name}", "bytes": f.stat().st_size, "sha256": hashlib.sha256(f.read_bytes()).hexdigest(),
              "backend": backend, "date": dt.date.today().isoformat()}
    MANIFEST.write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding="utf-8")


def draw_examples(backend: str = "auto", only: list[str] | None = None) -> list[str]:
    """예시가 없는 삽화 화풍마다 같은 장면을 그림.
    codex  = 이 PC 의 Codex CLI(ChatGPT 구독) — 로컬 Claude Code 세션도 이 명령으로 Codex 에게 맡김
    gemini = Gemini API 키(GEMINI_API_KEY, Google AI Studio)
    manual = 주문서(ORDERS.md)만 — 사람이 ChatGPT·Gemini 앱에 붙여 그리고 <예시 폴더>/<id>.png 로 저장
    auto   = 위 순서로 쓸 수 있는 것
    ElevenLabs 로는 그리지 않음 (2026-11-20 사용자)."""
    if backend in ("elevenlabs", "eleven"):
        raise SystemExit("[looks] ElevenLabs 로는 그림을 만들지 않습니다 (2026-11-20 사용자) — codex · gemini · manual")
    backend = _which_backend(backend)
    ex = examples_dir()
    lines = ["# 화풍 예시 그림 주문서 (같은 장면 · 화풍만 바꿈)", "",
             f"저장: {ex}/<화풍 id>.png  (PC 는 YTFLOW_DRIVE/looks — Drive 로 동기화)",
             "그리는 길: ① Codex(`looks --draw codex`) ② Gemini 키(`looks --draw gemini`) ③ 둘 다 없으면 아래 문장을 ChatGPT·Gemini 앱에 붙여 그린 뒤 이 폴더에 저장 → `looks --register`", ""]
    done = []
    for lid, d in (load().get("illust") or {}).items():
        if only and lid not in only:
            continue
        if not d.get("prompt") or any((ex / f"{lid}.{e}").exists() for e in ("png", "jpg", "jpeg")):
            continue
        prompt = EXAMPLE_SCENE + d["prompt"]
        lines += [f"## {lid} — {d.get('name', '')}  →  {lid}.png", "", "```", prompt, "```", ""]
        if backend in ("codex", "gemini"):
            from . import imagegen
            out = ex / f"{lid}.png"
            try:
                (imagegen.gen_codex if backend == "codex" else imagegen.gen_gemini)(prompt, out)
                _record(lid, out, backend)
                done.append(lid)
                print(f"  ✓ {lid} ({backend})")
            except Exception as e:   # 하나가 실패해도 나머지는 계속
                print(f"  ✗ {lid}: {e}")
    (ex / "ORDERS.md").write_text("\n".join(lines), encoding="utf-8")
    return done


def register() -> list[str]:
    """사람이 앱에서 그려 넣은 그림까지 manifest 에 올림 (예시 폴더의 <id>.png|jpg)."""
    ex, got = examples_dir(), []
    for lid in (load().get("illust") or {}):
        f = next((ex / f"{lid}.{e}" for e in ("png", "jpg", "jpeg") if (ex / f"{lid}.{e}").exists()), None)
        if f:
            _record(lid, f, "manual-or-earlier")
            got.append(lid)
    return got


def order() -> Path | None:
    """클라우드: 예시가 없는 삽화 화풍을 PC 할 일로 올림 (inbox/pc-tasks — PC 의 Claude Code·Codex 세션이 처리)."""
    import datetime as dt
    import json
    have = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else {}
    need = [(k, d) for k, d in (load().get("illust") or {}).items() if d.get("prompt") and k not in have]
    if not need:
        print("[looks] 모든 삽화 화풍에 예시가 있습니다")
        return None
    t = ROOT / "inbox" / "pc-tasks" / f"{dt.datetime.now(dt.timezone(dt.timedelta(hours=KST_OFFSET))):%Y%m%d-%H%M}-looks-draw.md"
    t.parent.mkdir(parents=True, exist_ok=True)
    rows = "\n".join(f"| `{k}` | {d.get('name', '')} | {d.get('status', '')} |" for k, d in need)
    t.write_text(f"""---
from: claude-code
type: looks-draw
status: pending
---

화풍 목록의 삽화 예시 그림을 PC 에서 그려 주세요 (같은 장면, 화풍만 바꿈). 클라우드에는 Codex 로그인·Gemini 키가 없고, ElevenLabs 로는 그리지 않습니다(2026-11-20 사용자).

```
git pull
python -m ytflow looks --draw auto        # Codex 구독 → Gemini 키(GEMINI_API_KEY) → 둘 다 없으면 주문서만
python -m ytflow looks --gallery looks.html   # 확인용 (선택)
git add styles/looks_examples.json && git commit -m "looks: 예시 그림" && git push
```

- 그림 파일은 `YTFLOW_DRIVE/looks/<id>.png` (Drive 로 동기화) — git 에는 `styles/looks_examples.json` 만.
- Codex 도 Gemini 키도 없으면: `YTFLOW_DRIVE/looks/ORDERS.md` 의 문장을 ChatGPT·Gemini 앱에 붙여 그리고 같은 폴더에 `<id>.png` 로 저장 → `python -m ytflow looks --register` → 위처럼 커밋.

| id | 화풍 | 상태 |
|---|---|---|
{rows}

끝나면 이 파일의 status 를 done 으로 바꾸고 아래에 결과(그린 것·실패 이유)를 적어 main 에 푸시해 주세요.
""", encoding="utf-8")
    print(f"[looks] PC 할 일 → {t.relative_to(ROOT)}")
    return t
