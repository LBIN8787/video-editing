"""어텐션 설명 장면 실험(docs/64) 렌더: attention.html → 프레임 → mp4 (소리 없음).
python scripts/attention_scene/render.py <출력폴더> [--fps 30] [--stills 0.5,3,...]"""
import argparse, subprocess, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def gsap_js() -> str:
    """GSAP 은 scripts/install_tools.py 가 tools/hyperframes 에 설치(tools/external.json 고정 버전). YTFLOW_GSAP 로 경로 지정 가능."""
    import os
    for c in [os.environ.get("YTFLOW_GSAP", ""), str(ROOT / "tools/hyperframes/node_modules/gsap/dist/gsap.min.js")]:
        if c and Path(c).exists():
            return Path(c).read_text(encoding="utf-8")
    sys.exit("GSAP 이 없습니다: python scripts/install_tools.py 를 먼저 실행하거나 YTFLOW_GSAP 를 지정하세요")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out"); ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--stills", default="")
    a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page(viewport={"width": 1920, "height": 1080})
        built = out / "attention.built.html"
        built.write_text((HERE / "attention.html").read_text(encoding="utf-8").replace("/*GSAP*/", gsap_js()), encoding="utf-8")
        pg.goto(built.as_uri() + "?still")
        pg.wait_for_function("window.READY === true")
        pg.evaluate("document.fonts.ready")
        total = pg.evaluate("window.DURATION")
        if a.stills:
            for t in [float(x) for x in a.stills.split(",")]:
                pg.evaluate(f"seek({t})")
                pg.screenshot(path=str(out / f"still_{t:05.1f}.jpg"), type="jpeg", quality=88)
        else:
            fr = out / "frames"; fr.mkdir(exist_ok=True)
            n = int(total * a.fps)
            for i in range(n):
                pg.evaluate(f"seek({i / a.fps})")
                pg.screenshot(path=str(fr / f"{i:05d}.jpg"), type="jpeg", quality=88)
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(a.fps), "-i", str(fr / "%05d.jpg"),
                            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", str(out / "attention_scene.mp4")], check=True)
        br.close()
    print(f"길이 {total:.1f}초 → {out}")

if __name__ == "__main__":
    sys.exit(main())
