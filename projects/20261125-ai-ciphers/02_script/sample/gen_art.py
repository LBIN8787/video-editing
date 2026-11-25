"""그림 사물 생성 (Codex 구독, ytflow imagegen.gen_codex) → 시트 → 조각. python gen_art.py"""
import json, sys
from pathlib import Path
sys.path.insert(0, "D:/ytflow/wt-visual-first")
from ytflow.stages.imagegen import cut, SHEET
import shutil, subprocess
def gen_codex(prompt, out):
    exe = shutil.which("codex")   # Windows: npm 의 codex.cmd 를 전체 경로로
    task = (f"Use the $imagegen skill to generate ONE image and save it exactly to {out.resolve()} (PNG, landscape). "
            f"Do not edit any other file. Prompt: {prompt}")
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([exe, "exec", "--skip-git-repo-check", "-s", "workspace-write", "-C", str(out.parent.resolve()), task], check=True, timeout=900, stdin=subprocess.DEVNULL)
    if not out.exists():
        raise RuntimeError("codex 가 그림을 저장하지 않음")
    return {"backend": "codex", "model": "gpt-image (ChatGPT 구독)"}
OUT = Path("E:/ytflow-local/hf-ciphers/assets/gen")
STYLE = ("Soft matte 3D illustration like painted clay or carved wood, warm muted palette of cream, deep navy, brick red and aged brass, "
         "gentle soft studio light, subtle texture, tactile and charming, documentary editorial look. Plain pure white background, "
         "no ground shadows, no text, no letters, no numbers unless asked, no labels, no logos.")
SHEETS = [
 ("s_letter", "a folded early-1800s military letter sealed with a red wax seal; a Napoleonic-era courier riding a galloping horse, seen from the side, small; "
              "an old opened letter page filled entirely with rows of handwritten numbers in brown ink (no words)", ["letter_sealed", "courier", "letter_numbers"]),
 ("s_archive", "an old wooden archive drawer pulled out, packed with yellowed folded letters and a little dust; a brass hourglass with sand; "
               "a person seen from behind sitting at a desk with a glowing laptop at night (anonymous silhouette, no face)", ["drawer", "hourglass", "laptop_person"]),
]
log = {}
for sid, subj, pieces in SHEETS:
    sheet = OUT / f"{sid}.png"
    prompt = SHEET.format(subject=subj) + STYLE
    if not sheet.exists():
        info = gen_codex(prompt, sheet)
        log[sid] = {**info, "prompt": prompt}
        print("gen", sid, flush=True)
    try:
        cut(sheet, OUT, pieces)
        print("cut", sid, pieces, flush=True)
    except Exception as e:
        print("cut fail", sid, e, flush=True)
(OUT / "art_log.json").write_text(json.dumps(log, ensure_ascii=False, indent=1), encoding="utf-8")
