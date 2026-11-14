"""그림 생성 — 여러 길 (2026-11-14 사용자: "모든 걸 일레븐랩스로 하는 게 아니라 GPT 이미지 2.6 같은 다른 방법도").

호기심 채널 이야기형(docs/27): 대본의 장면을 그림이 직접 보여 준다. 인물·사물은 '한 장에 자세 여러 개'(모델 시트)로 만들어
같은 모습을 유지하고, 흰(또는 투명) 배경을 지워 조각으로 자른다 → story 장면의 cut·pose·move.

    python -m ytflow art-gen <프로젝트> [--backend openai|gemini|codex|manual] [--only baby,robot]
    python -m ytflow art-cut <시트.png> <출력폴더> 이름1,이름2,이름3          # 시트 → 조각 (어느 길로 만들었든)

주문서: 02_script/art_plan.json
  {"style": "(비우면 STYLE 기본)", "sheets": [
     {"id": "baby", "prompt": "the same chubby toddler ... (1) ...; (2) ...; (3) ...", "pieces": ["baby_look", "baby_grab", "baby_walk"]}]}
결과: 04_assets/story/gen/<sheet id>_sheet.png + <piece>.png, 기록 04_assets/story/gen/art_log.json (길·모델·비용 추정·프롬프트)

길(backend):
| openai | OpenAI Images API (gpt-image-2 계열, OPENAI_API_KEY) — 투명 배경 지원, 품질 low/medium/high 로 값 조절 |
| gemini | Google Gemini API 이미지 (Nano Banana 계열, GEMINI_API_KEY) — 참조 그림으로 같은 인물 유지에 강함 |
| codex  | 사용자 PC 의 Codex CLI($imagegen, ChatGPT 구독 한도 안) — 로그인된 PC 에서만, 추가 요금 없음 |
| manual | 주문서(02_script/art_orders.md)만 씀 → 에이전트가 ElevenLabs 커넥터(GPT Image 2.6·Seedream 등)로 만들거나 사람이 그림을 넣음 |
키는 채팅에 쓰지 않고 환경변수·네트워크 비밀값으로 (AGENTS.md 규칙).
"""
from __future__ import annotations

import base64
import json
import os
import shutil
import subprocess
import urllib.request
from pathlib import Path

STYLE = ("Flat editorial vector illustration, warm cream, navy blue and muted brick-red palette, confident navy outlines, "
         "soft flat shading, subtle paper grain, charming and gentle. Plain pure white background, no ground shadows, no text, no labels.")
SHEET = ("{subject}. Each one shown side by side, evenly spaced with clear empty space between them, each full and not overlapping. ")


def plan(project) -> dict:
    p = project.dir("script") / "art_plan.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"sheets": []}


def full_prompt(spec: dict, sh: dict) -> str:
    return SHEET.format(subject=sh["prompt"].rstrip(". ")) + (spec.get("style") or STYLE)


# ---------------------------------------------------------------- 길마다
def _post(url: str, body: dict, headers: dict, timeout: int = 300) -> dict:
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json", **headers})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def gen_openai(prompt: str, out: Path, model: str = "", quality: str = "medium") -> dict:
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY 없음 (환경변수·네트워크 비밀값으로 넣기)")
    model = model or os.environ.get("YTFLOW_OPENAI_IMAGE_MODEL", "gpt-image-2")
    d = _post("https://api.openai.com/v1/images/generations",
              {"model": model, "prompt": prompt, "size": "1536x1024", "quality": quality, "n": 1, "background": "transparent"},
              {"Authorization": f"Bearer {key}"})
    out.write_bytes(base64.b64decode(d["data"][0]["b64_json"]))
    return {"backend": "openai", "model": model, "quality": quality, "usage": d.get("usage")}


def gen_gemini(prompt: str, out: Path, model: str = "", refs: list[Path] | None = None) -> dict:
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY 없음 (환경변수·네트워크 비밀값으로 넣기)")
    model = model or os.environ.get("YTFLOW_GEMINI_IMAGE_MODEL", "gemini-2.5-flash-image")
    parts = [{"text": prompt}] + [{"inline_data": {"mime_type": "image/png", "data": base64.b64encode(r.read_bytes()).decode()}} for r in refs or []]
    d = _post(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
              {"contents": [{"parts": parts}], "generationConfig": {"responseModalities": ["IMAGE"]}}, {"x-goog-api-key": key})
    for c in d.get("candidates", []):
        for p in c.get("content", {}).get("parts", []):
            data = (p.get("inlineData") or p.get("inline_data") or {}).get("data")
            if data:
                out.write_bytes(base64.b64decode(data))
                return {"backend": "gemini", "model": model, "usage": d.get("usageMetadata")}
    raise RuntimeError(f"그림이 오지 않음: {str(d)[:200]}")


def gen_codex(prompt: str, out: Path) -> dict:
    """사용자 PC 의 Codex CLI 로 (ChatGPT 구독 한도). 클라우드 세션에는 codex 로그인이 없어 쓰지 않는다."""
    if not shutil.which("codex"):
        raise RuntimeError("codex CLI 없음 — Codex 를 쓰는 PC 에서 실행하세요")
    task = (f"Use the $imagegen skill to generate ONE image and save it exactly to {out.resolve()} (PNG, landscape). "
            f"Do not edit any other file. Prompt: {prompt}")
    subprocess.run(["codex", "exec", "--skip-git-repo-check", task], check=True, timeout=900)
    if not out.exists():
        raise RuntimeError("codex 가 그림을 저장하지 않음")
    return {"backend": "codex", "model": "gpt-image (ChatGPT 구독)"}


# ---------------------------------------------------------------- 시트 → 조각
def cut(sheet: Path, outdir: Path, names: list[str], white: int = 232, gap: int = 40) -> list[Path]:
    """흰 배경(가장자리와 이어진 흰색만) 또는 투명 배경을 지우고, 세로 빈 열에서 잘라 조각으로. 옷의 흰 부분은 남김."""
    import numpy as np
    from PIL import Image
    from scipy import ndimage
    im = Image.open(sheet).convert("RGBA")
    a = np.asarray(im).astype(int)
    if (a[..., 3] < 250).mean() > 0.05:   # 이미 투명 배경 (openai background=transparent)
        fg = a[..., 3] > 20
    else:
        rgb = a[..., :3]
        corners = np.concatenate([rgb[:20, :20].reshape(-1, 3), rgb[:20, -20:].reshape(-1, 3), rgb[-20:, :20].reshape(-1, 3), rgb[-20:, -20:].reshape(-1, 3)])
        bgc = np.median(corners, axis=0)   # 배경색을 귀퉁이에서 (흰색이 아니어도: 크림 종이색 등)
        near = np.abs(rgb - bgc).max(axis=2) < max(14, 255 - white)
        lab, _ = ndimage.label(near)
        border = set(np.unique(np.r_[lab[0], lab[-1], lab[:, 0], lab[:, -1]])) - {0}
        fg = ~np.isin(lab, list(border))
        fg = ndimage.binary_opening(fg, iterations=2)
    cols = fg.sum(axis=0) > 3
    segs, run, s0 = [], False, 0
    for x, c in enumerate(cols):
        if c and not run:
            run, s0 = True, x
        if not c and run:
            run = False
            segs.append([s0, x])
    if run:
        segs.append([s0, len(cols)])
    merged = []
    for s in segs:
        if merged and s[0] - merged[-1][1] < gap:
            merged[-1][1] = s[1]
        else:
            merged.append(s)
    merged = [s for s in merged if s[1] - s[0] > 80]
    if len(merged) != len(names):
        raise RuntimeError(f"조각 수가 다름: 시트에서 {len(merged)}개, 이름 {len(names)}개 — 프롬프트의 '간격' 문장을 확인하거나 다시 생성")
    alpha = ndimage.gaussian_filter(fg.astype(float), 1.0)
    rgba = np.dstack([a[..., :3].astype(np.uint8), (alpha * 255).clip(0, 255).astype(np.uint8)])
    outdir.mkdir(parents=True, exist_ok=True)
    outs = []
    for (x0, x1), nm in zip(merged, names):
        ys = np.where(fg[:, x0:x1].any(axis=1))[0]
        y0, y1 = max(0, ys[0] - 10), min(a.shape[0], ys[-1] + 10)
        o = outdir / f"{nm}.png"
        Image.fromarray(rgba[y0:y1, max(0, x0 - 10):x1 + 10]).save(o)
        outs.append(o)
    return outs


def run(project, backend: str = "manual", only: list[str] | None = None) -> Path:
    spec = plan(project)
    gdir = project.dir("assets") / "story" / "gen"
    gdir.mkdir(parents=True, exist_ok=True)
    logp = gdir / "art_log.json"
    log = json.loads(logp.read_text(encoding="utf-8")) if logp.exists() else {}
    orders = ["# 그림 주문서 (art_plan.json → 시트 한 장 = 같은 대상의 여러 모습)", "",
              "각 시트를 생성한 뒤 `04_assets/story/gen/<id>_sheet.png` 로 저장하고 `python -m ytflow art-cut` 으로 조각을 냅니다.", ""]
    for sh in spec.get("sheets", []):
        if only and sh["id"] not in only:
            continue
        prompt = full_prompt(spec, sh)
        sheet = gdir / f"{sh['id']}_sheet.png"
        orders += [f"## {sh['id']} → {', '.join(sh['pieces'])}", "", "```", prompt, "```", ""]
        if backend == "manual":
            continue
        if not sheet.exists():
            info = {"openai": lambda: gen_openai(prompt, sheet), "gemini": lambda: gen_gemini(prompt, sheet),
                    "codex": lambda: gen_codex(prompt, sheet)}[backend]()
            log[sh["id"]] = {**info, "prompt": prompt}
            print(f"[art-gen] {sh['id']} ← {info['backend']} {info.get('model', '')}")
        cut(sheet, gdir, sh["pieces"])
        print(f"[art-gen] {sh['id']} → {len(sh['pieces'])}조각")
    (project.dir("script") / "art_orders.md").write_text("\n".join(orders), encoding="utf-8")
    logp.write_text(json.dumps(log, ensure_ascii=False, indent=1), encoding="utf-8")
    return gdir


def main_gen(argv: list[str]) -> None:
    import argparse
    from ..project import Project
    ap = argparse.ArgumentParser(prog="art-gen")
    ap.add_argument("project")
    ap.add_argument("--backend", default=os.environ.get("YTFLOW_IMAGE_BACKEND", "manual"), choices=["openai", "gemini", "codex", "manual"])
    ap.add_argument("--only", default="")
    a = ap.parse_args(argv)
    run(Project.open(a.project), a.backend, [x for x in a.only.split(",") if x] or None)


def main_cut(argv: list[str]) -> None:
    sheet, outdir, names = Path(argv[0]), Path(argv[1]), argv[2].split(",")
    for o in cut(sheet, outdir, names):
        print(o)
