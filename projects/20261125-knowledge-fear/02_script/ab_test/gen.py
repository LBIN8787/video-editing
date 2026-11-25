"""고급 사물 렌더 시트 (Codex 구독 이미지 생성) — 미주일기 수준 시험. python gen.py"""
import json, shutil, subprocess, sys
from pathlib import Path
OUT = Path(__file__).resolve().parent / "gen"
STYLE = ("Premium photorealistic 3D product render for a high-end editorial documentary explainer. Realistic materials and fine surface detail, "
         "soft diffused studio lighting from the upper left, gentle ambient occlusion, natural colors gently desaturated toward warm cream and deep navy, "
         "three-quarter front view slightly from above. Exactly three separate objects side by side, each fully visible, fully isolated on a pure flat white "
         "background with wide white gaps between them, no cast shadows on the background, no floor, no text, no letters, no logos, no watermark.")
SHEETS = [
 ("s_alarm", "Objects, left to right: a modern round white ceiling smoke detector with a tiny red indicator LED and fine vent slots; "
             "a single slice of white-bread toast, golden and slightly burnt at the crust edges; a small campfire of three crossed split logs with realistic orange flames."),
 ("s_scale", "Objects, left to right: an elegant antique brass balance scale with two shallow pans and the beam perfectly level; "
             "one shiny gold coin standing upright and slightly angled; a heavy rough dark grey granite stone."),
 ("s_path",  "Objects, left to right: a faceless smooth matte deep-navy mannequin figure walking, seen from the side; "
             "a crooked bent dry tree branch lying flat that looks a little like a snake; a clean white anatomical model of a human eyeball on a small stand."),
]
exe = shutil.which("codex")
log = {}
for sid, subj in SHEETS:
    out = OUT / f"{sid}.png"
    if out.exists():
        continue
    task = (f"Use the $imagegen skill to generate ONE image and save it exactly to {out} (PNG, landscape 3:2). Do not edit any other file. Prompt: {subj} {STYLE}")
    subprocess.run([exe, "exec", "--skip-git-repo-check", "-s", "workspace-write", "-C", str(OUT), task], check=True, timeout=900, stdin=subprocess.DEVNULL)
    print("gen", sid, out.exists(), flush=True)
    log[sid] = {"backend": "codex", "prompt": subj + " " + STYLE}
(OUT / "art_log.json").write_text(json.dumps(log, ensure_ascii=False, indent=1), encoding="utf-8")
