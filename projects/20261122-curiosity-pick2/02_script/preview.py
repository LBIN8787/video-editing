"""렌더 전 정지 화면 확인: python preview.py <TTS> <조각> <출력.jpg> 박자:초 [박자:초 ...]  (SPEC·OVERLAY 환경변수는 render_full.py 와 같음)"""
import json, os, sys
from pathlib import Path
from PIL import Image
import render_full as RF

HERE = Path(__file__).resolve().parent
tts, art, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
spec = json.loads((HERE / os.environ.get("SPEC", "cunning.json")).read_text(encoding="utf-8"))
RF.timeline(spec, tts)
scenes = [{"data": {k: v for k, v in s.items() if not k.startswith("_")}, "K": s["_K"], "D": s["_D"], "A": s["_A"]["t"], "AD": s["_A"]["d"]} for s in spec["scenes"]]
idx = {s["id"]: i for i, s in enumerate(spec["scenes"])}
from playwright.sync_api import sync_playwright
shots = []
with sync_playwright() as pw:
    br = pw.chromium.launch(); pg = br.new_page(viewport={"width": 1920, "height": 1080})
    pg.goto((HERE / os.environ.get("OVERLAY", "cunning_overlay.html")).as_uri())
    pg.evaluate("(a)=>INIT(a[0],a[1])", [scenes, art.resolve().as_uri()])
    pg.wait_for_function("window.READY===true", timeout=60000)
    for a in sys.argv[4:]:
        b, t = a.split(":"); si = idx[int(b)]; t = float(t); sc = spec["scenes"][si]
        sub = next((s for x, y, s in sc["_subs"] if x <= t <= y), "")
        pg.evaluate("(a)=>R(a[0],a[1],a[2])", [si, t, sub])
        p = out.with_name(f"pv_{b}_{t}.jpg"); pg.screenshot(path=str(p), type="jpeg", quality=80); shots.append(p)
    br.close()
cols = 3; w, h = 640, 360
sheet = Image.new("RGB", (cols * w, ((len(shots) + cols - 1) // cols) * h))
for i, p in enumerate(shots):
    sheet.paste(Image.open(p).resize((w, h)), ((i % cols) * w, (i // cols) * h))
sheet.save(out, quality=85); print(out)
