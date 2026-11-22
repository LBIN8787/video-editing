"""프레임 미리보기: SPEC 의 (박자 id, 장면 안 초) 목록 → <출력 폴더>/p<id>_<초>.jpg + 한 장 모음. 렌더 전 화면 확인용.
python preview.py <TTS 폴더> <조각 폴더> <출력 폴더> 3:5.0 13:2.5 ..."""
import json, os, sys, importlib.util
from pathlib import Path
from PIL import Image
HERE = Path(__file__).resolve().parent
spec_ = importlib.util.spec_from_file_location("rf", HERE / "render_full.py"); rf = importlib.util.module_from_spec(spec_)
sys.argv_backup = sys.argv; spec_.loader.exec_module(rf)
tts, art, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]); out.mkdir(parents=True, exist_ok=True)
spec = json.loads((HERE / os.environ.get("SPEC", "soldout.json")).read_text(encoding="utf-8"))
rf.timeline(spec, tts)
scenes = [{"data": {k: v for k, v in s.items() if not k.startswith("_")}, "K": s["_K"], "D": s["_D"], "A": s["_A"]["t"], "AD": s["_A"]["d"]} for s in spec["scenes"]]
ids = {s["id"]: i for i, s in enumerate(spec["scenes"])}
from playwright.sync_api import sync_playwright
files = []
with sync_playwright() as pw:
    br = pw.chromium.launch(); pg = br.new_page(viewport={"width": 1920, "height": 1080})
    pg.goto((HERE / os.environ.get("OVERLAY", "soldout_overlay.html")).as_uri())
    pg.evaluate("(a)=>INIT(a[0],a[1])", [scenes, art.resolve().as_uri()]); pg.wait_for_function("window.READY===true", timeout=60000)
    for a in sys.argv[4:]:
        bid, t = a.split(":"); si = ids[int(bid)]; t = float(t); sc = spec["scenes"][si]; sub = ""
        for x0, x1, s in sc["_subs"]:
            if x0 <= t <= x1: sub = s
        pg.evaluate("(a)=>R(a[0],a[1],a[2])", [si, t, sub]); f = out / f"p{int(bid):02d}_{t:05.1f}.jpg"; pg.screenshot(path=str(f), type="jpeg", quality=85); files.append(f)
    br.close()
n = len(files); cols = 3; rows = (n + cols - 1) // cols; sheet = Image.new("RGB", (cols * 640, rows * 360))
for i, f in enumerate(files): sheet.paste(Image.open(f).resize((640, 360)), ((i % cols) * 640, (i // cols) * 360))
sheet.save(out / "sheet.jpg", quality=85); print(out / "sheet.jpg")
