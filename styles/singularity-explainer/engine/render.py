"""singularity-explainer 렌더: base.html + engine.js + <영상>/scenes.js → 프레임 → mp4 (여러 브라우저로 나눠 병렬).
사용: python render.py <02_script 폴더> <작업폴더> [--stills 3,10] [--jobs 4] [--fps 30] [--css extra.css]
작업폴더에 voice.wav(voice.py 결과) 가 있어야 하고, 장 표지 그림은 <작업폴더>/art/*.png 를 ART['이름'] 으로 쓴다."""
import argparse, json, pathlib, subprocess, sys
from concurrent.futures import ProcessPoolExecutor
HERE = pathlib.Path(__file__).parent

def build(script_dir: pathlib.Path, out: pathlib.Path) -> pathlib.Path:
    tl = json.loads((script_dir / "timeline.json").read_text(encoding="utf-8"))
    art = {p.stem: p.resolve().as_uri() for p in sorted((out / "art").glob("*.png"))} if (out / "art").exists() else {}
    css = (script_dir / "scenes.css").read_text(encoding="utf-8") if (script_dir / "scenes.css").exists() else ""
    html = (HERE / "base.html").read_text(encoding="utf-8")
    html = html.replace("/*TL*/", "window.TL=" + json.dumps(tl, ensure_ascii=False) + ";window.ART=" + json.dumps(art) + ";")
    html = html.replace("/*ENGINE*/", (HERE / "engine.js").read_text(encoding="utf-8")).replace("/*SCENES*/", (script_dir / "scenes.js").read_text(encoding="utf-8")).replace("/*EXTRA_CSS*/", css)
    page = out / "page.html"; page.write_text(html, encoding="utf-8"); return page

def chunk(args):
    page, out, i0, i1, fps, k = args
    from playwright.sync_api import sync_playwright
    seg = out / f"seg{k:02d}.mp4"
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1920, "height": 1080})
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(page.as_uri()); pg.wait_for_timeout(800)
        if errs: raise RuntimeError(errs[0])
        ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(fps), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "fast", str(seg)], stdin=subprocess.PIPE)
        for i in range(i0, i1):
            pg.evaluate(f"render({i / fps})"); ff.stdin.write(pg.screenshot(type="jpeg", quality=92))
        ff.stdin.close(); ff.wait(); b.close()
    return seg

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("script_dir"); ap.add_argument("out"); ap.add_argument("--stills"); ap.add_argument("--jobs", type=int, default=4); ap.add_argument("--fps", type=int, default=30)
    a = ap.parse_args(); SD, OUT = pathlib.Path(a.script_dir), pathlib.Path(a.out); OUT.mkdir(parents=True, exist_ok=True)
    page = build(SD, OUT)
    if a.stills:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1920, "height": 1080}); errs = []
            pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: m.type == "error" and errs.append(m.text))
            pg.goto(page.as_uri()); pg.wait_for_timeout(800)
            for s in a.stills.split(","):
                pg.evaluate(f"render({float(s)})"); pg.screenshot(path=str(OUT / f"still_{float(s):06.1f}.png"))
            b.close()
        print("errors:", errs[:5] if errs else "none"); sys.exit()
    total = json.loads((SD / "timeline.json").read_text(encoding="utf-8"))["total"]; n = int(total * a.fps); step = -(-n // a.jobs)
    jobs = [(page, OUT, k * step, min(n, (k + 1) * step), a.fps, k) for k in range(a.jobs)]
    with ProcessPoolExecutor(a.jobs) as ex: segs = list(ex.map(chunk, jobs))
    (OUT / "segs.txt").write_text("".join(f"file '{s.name}'\n" for s in segs), encoding="utf-8")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(OUT / "segs.txt"), "-i", str(OUT / "voice.wav"),
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", str(OUT / "final.mp4")], check=True, cwd=OUT)
    print("done", OUT / "final.mp4")
