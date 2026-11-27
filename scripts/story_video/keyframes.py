"""GPT($imagegen) 로 '전' 그림 만들기 — 기존 그림을 참조(-i)로 붙여 같은 구도·화풍에서 한 순간 앞을 그림."""
import re, shutil, subprocess, time, pathlib, concurrent.futures as cf
from PIL import Image
ROOT = pathlib.Path(r"E:\ytflow-local\books-video"); GEN = pathlib.Path.home() / ".codex" / "generated_images"
HEAD = ("Use $imagegen to create exactly one image. Do not write any code and do not edit any file. "
        "Use the attached image as the exact reference: keep the SAME composition, camera angle, framing, objects, lighting and drawing style, "
        "change ONLY what is described below, so the two images can be cross-faded as one moment before and after.\n\nCHANGE: ")
JOBS = [
 ("dyatlov", "b13_tent_slash", "b13a_tent_pressed", "Make this the moment just BEFORE: the canvas wall is still whole with no cut at all; the hand with the small knife is raised near the canvas, about to cut. Everything else identical."),
 ("dyatlov", "b12_slope_diagram", "b12a_slope_before", "Make this the moment BEFORE the slide: the snow slab is still resting in place on the slope above the cut wall, not yet sliding, the tent stands upright and free; wind-blown snow is drifting onto the slope. No arrow on the slab. Everything else identical."),
]
def fit(src, dst):
    im = Image.open(src).convert("RGB"); w, h = im.size; t = 16 / 9
    if w / h > t: nw = int(h * t); im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else: nh = int(w / t); im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    im.resize((1672, 940), Image.LANCZOS).save(dst)
def one(j):
    proj, ref, k, change = j
    out = ROOT / proj / "art" / f"{k}.png"
    if out.exists(): return f"skip {k}"
    logd = ROOT / proj / "logs"; t0 = time.time()
    for _ in range(2):
        r = subprocess.run(f'"codex" "exec" "--skip-git-repo-check" "-m" "gpt-6-sol" "-i" "{ROOT / proj / "art" / (ref + ".png")}"',
                           input=HEAD + change + " No text anywhere.", capture_output=True, text=True, encoding="utf-8", errors="replace", shell=True, cwd=str(logd))
        log = (r.stdout or "") + (r.stderr or ""); (logd / f"{k}.log").write_text(log, encoding="utf-8")
        m = re.search(r"session id:\s*([0-9a-f-]{36})", log)
        if m and (GEN / m.group(1)).exists():
            pngs = sorted((GEN / m.group(1)).glob("*.png"), key=lambda q: q.stat().st_mtime)
            if pngs: shutil.copy2(pngs[-1], out.with_name(k + "_raw.png")); fit(pngs[-1], out); return f"ok {k} {time.time()-t0:.0f}s"
    return f"FAIL {k}"
with cf.ThreadPoolExecutor(2) as ex:
    for r in ex.map(one, JOBS): print(r, flush=True)
