"""템플릿 v2 그림 만들기 (사용자 Codex $imagegen).
1단계: 무대 기준 그림(set_*)·인물 기준 그림(char_*)  2단계: 장면 — 무대 기준 그림 + 등장인물 기준 그림을 참조(-i)로 붙여 '같은 방, 같은 얼굴, 구도만'.
python gen_v2.py <remake_full.json> <out_dir> [병렬]"""
import json, re, shutil, subprocess, sys, time, pathlib, concurrent.futures as cf
from PIL import Image
R = json.load(open(sys.argv[1], encoding="utf-8")); OUT = pathlib.Path(sys.argv[2]); ART = OUT / "art"; LOG = OUT / "logs"
ART.mkdir(parents=True, exist_ok=True); LOG.mkdir(exist_ok=True); PAR = int(sys.argv[3]) if len(sys.argv) > 3 else 5
GEN = pathlib.Path.home() / ".codex" / "generated_images"
HEAD = "Use $imagegen to create exactly one image as described below. Do not write any code and do not edit any file; just generate the image.\n\n"
TAIL = "\n\nFRAMING: wide 16:9 landscape, cinematic, the subject readable when cropped to the central 80%. No text anywhere."

def fit(src, dst):
    im = Image.open(src).convert("RGB"); w, h = im.size; t = 16 / 9
    if w / h > t: nw = int(h * t); im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else: nh = int(w / t); im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    im.resize((1672, 940), Image.LANCZOS).save(dst)

def run(k, prompt, refs):
    out = ART / f"{k}.png"
    if out.exists(): return f"skip {k}"
    cmd = '"codex" "exec" "--skip-git-repo-check" "-m" "gpt-6-sol"' + "".join(f' "-i" "{r}"' for r in refs)
    t0 = time.time()
    for _ in range(3):
        r = subprocess.run(cmd, input=prompt, capture_output=True, text=True, encoding="utf-8", errors="replace", shell=True, cwd=str(LOG))
        log = (r.stdout or "") + (r.stderr or ""); (LOG / f"{k}.log").write_text(log, encoding="utf-8")
        m = re.search(r"session id:\s*([0-9a-f-]{36})", log)
        if m and (GEN / m.group(1)).exists():
            pngs = sorted((GEN / m.group(1)).glob("*.png"), key=lambda q: q.stat().st_mtime)
            if pngs: fit(pngs[-1], out); return f"ok {k} {time.time() - t0:.0f}s"
        time.sleep(20)
    return f"FAIL {k}"

style = R["style"]
# 1단계
jobs1 = [(f"set_{s}", HEAD + "PLACE (an empty establishing view, no people): " + d + "\n\n" + style + TAIL, []) for s, d in R["sets"].items()]
jobs1 += [(f"char_{c}", HEAD + "CHARACTER REFERENCE: " + d + " Waist-up, three-quarter view, standing in a plain dim farmhouse room with warm lamplight, neutral expression, clearly lit face." + "\n\n" + style + TAIL, [])
          for c, d in R["chars"].items()]
with cf.ThreadPoolExecutor(PAR) as ex:
    for res in ex.map(lambda j: run(*j), jobs1): print(res, flush=True)
# 2단계
jobs2 = []
for k, (st, chars, desc) in R["images"].items():
    refs, notes = [], []
    if st and (ART / f"set_{st}.png").exists(): refs.append(ART / f"set_{st}.png"); notes.append("Attached image 1 is the PLACE reference: keep exactly the same place — same furniture, walls, window, lamp, colours and lighting — and change only the camera framing and what happens.")
    for c in chars[:3]:
        if (ART / f"char_{c}.png").exists(): refs.append(ART / f"char_{c}.png"); notes.append(f"Attached image {len(refs)} is the CHARACTER reference for {c}: keep the same face, hair and clothes.")
    who = ("People in this scene: " + ", ".join(R["chars"][c] for c in chars) + ".") if chars else "No people in this scene."
    p = HEAD + " ".join(notes) + "\n\nSCENE: " + desc + "\n" + who + "\n\n" + style + " " + R["rules"] + TAIL
    jobs2.append((k, p, refs))
with cf.ThreadPoolExecutor(PAR) as ex:
    for res in ex.map(lambda j: run(*j), jobs2): print(res, flush=True)
