"""도입부 시험작 렌더: intro.html 을 프레임마다 render(t) → ffmpeg.
사용: python make_intro.py <작업폴더> [--stills 1,5,30] [--fps 30]
작업폴더에는 make_voice.py 가 만든 voice.wav 가 있어야 한다. 결과: <작업폴더>/intro.mp4"""
import json, pathlib, subprocess, sys, argparse
from playwright.sync_api import sync_playwright
HERE = pathlib.Path(__file__).parent
ap = argparse.ArgumentParser(); ap.add_argument("out"); ap.add_argument("--stills"); ap.add_argument("--fps", type=int, default=30)
a = ap.parse_args(); OUT = pathlib.Path(a.out); OUT.mkdir(parents=True, exist_ok=True)
tl = json.loads((HERE / "timeline.json").read_text(encoding="utf-8"))
html = (HERE / "intro.html").read_text(encoding="utf-8").replace("<script>\nconst W", "<script>window.TL=" + json.dumps(tl, ensure_ascii=False) + ";\nconst W", 1)
page_path = OUT / "intro_page.html"; page_path.write_text(html, encoding="utf-8")
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1920, "height": 1080})
    pg.goto(page_path.as_uri()); pg.wait_for_timeout(500)
    if a.stills:
        for s in a.stills.split(","):
            pg.evaluate(f"render({float(s)})"); pg.screenshot(path=str(OUT / f"still_{float(s):05.1f}.png"))
        b.close(); sys.exit()
    n = int(tl["total"] * a.fps)
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(a.fps), "-i", "-",
                           "-i", str(OUT / "voice.wav"), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "fast",
                           "-c:a", "aac", "-b:a", "160k", "-shortest", str(OUT / "intro.mp4")], stdin=subprocess.PIPE)
    for i in range(n):
        pg.evaluate(f"render({i / a.fps})")
        ff.stdin.write(pg.screenshot(type="jpeg", quality=92))
        if i % 300 == 0: print(i, "/", n, flush=True)
    ff.stdin.close(); ff.wait(); b.close()
print("done")
