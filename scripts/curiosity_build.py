"""호기심 채널 한 편을 PC 에서 끝까지 — 원화 시트(Drive) → 실제 자료 받기 → 칸 자르기 → 목소리 → 장면 → 렌더 → Drive 보관.

2026-11-20 사용자: "이 호기심 채널 영상제작 자동화 세팅 해달라는거야" · "클라우드에서 하지말고 로컬에서 진행하도록".
PC 일꾼(scripts/pc_worker.py)이 `type: curiosity-build` 할 일을 받으면 이 스크립트를 실행한다. 사람이 직접 돌려도 된다:

    python scripts/curiosity_build.py projects/<프로젝트> [--draft-voice]

프로젝트마다 02_script/build.json 하나로 정한다 (예: projects/20261120-curiosity-whitebear-v2/02_script/build.json):
  narration   낭독본(md, narrate.py 형식)          channel   목소리 채널(channels/<id>/channel.yaml 의 tts.elevenlabs)
  ep_script   장면 스크립트(scripts/anim/ep_*.py)   prep      칸 자르기 명령 (art·project 자리표시)
  art_sheets  원화 시트 이름(YTFLOW_DRIVE/영상/<프로젝트>/art/<이름>.png|jpg)
  assets      실제 자료: {"pdf": URL, "page": n, "crop": [x0,y0,x1,y1](비율), "out": 파일} | {"url": URL, "out": 파일}
  output      완성 파일 이름
결과: YTFLOW_DRIVE/영상/<프로젝트>/05_edit/<output> + 프레임 시트, REPORT.md 에 한 줄.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sh(cmd: list[str], **kw) -> str:
    print("$", " ".join(str(c) for c in cmd), flush=True)
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True, encoding="utf-8", errors="replace", **kw)
    if r.returncode:
        raise SystemExit(f"실패: {cmd[0]} …\n{(r.stdout or '')[-1500:]}\n{(r.stderr or '')[-1500:]}")
    return r.stdout


def fetch(url: str, out: Path) -> Path:
    if not out.exists():
        req = urllib.request.Request(url, headers={"User-Agent": "ytflow-build/1.0"})
        with urllib.request.urlopen(req, timeout=120) as r:
            out.write_bytes(r.read())
    return out


def pdf_crop(pdf: Path, page: int, crop: list[float], out: Path) -> None:
    """PDF 한 쪽 → 그림 → 비율로 자르기 (pypdfium2, 없으면 pdftoppm)."""
    from PIL import Image
    try:
        import pypdfium2 as pdfium
        pg = pdfium.PdfDocument(str(pdf))[page - 1]
        pg.set_cropbox(*pg.get_mediabox())   # pdftoppm 과 같게 쪽 전체 기준 (이 논문은 쪽마다 CropBox 가 달라 비율이 어긋남)
        im = pg.render(scale=220 / 72).to_pil()
    except ImportError:
        tmp = out.with_suffix("")
        sh(["pdftoppm", "-f", page, "-l", page, "-r", 220, "-png", "-singlefile", pdf, tmp])
        im = Image.open(str(tmp) + ".png")
    W, H = im.size
    x0, y0, x1, y1 = crop
    im.convert("RGB").crop((int(W * x0), int(H * y0), int(W * x1), int(H * y1))).save(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("project", type=Path)
    ap.add_argument("--draft-voice", action="store_true", help="ElevenLabs 대신 edge-tts 초안 목소리")
    a = ap.parse_args()
    proj = (ROOT / a.project).resolve() if not a.project.is_absolute() else a.project
    cfg = json.loads((proj / "02_script" / "build.json").read_text(encoding="utf-8"))
    drive = os.environ.get("YTFLOW_DRIVE")
    if not drive:
        raise SystemExit("환경변수 YTFLOW_DRIVE 가 없습니다 (예: G:\\내 드라이브\\ytflow) — docs/09-storage.md §0")
    ep_dir = Path(drive) / "영상" / proj.name
    art_src = ep_dir / "art"
    art = proj / "04_assets" / "art"
    art.mkdir(parents=True, exist_ok=True)

    # 1) 원화 시트 (PC 의 Codex 가 그린 것)
    miss = []
    for s in cfg["art_sheets"]:
        src = next((p for p in (art_src / f"{s}.png", art_src / f"{s}.jpg") if p.exists()), None)
        if src:
            shutil.copy2(src, art / src.name)
        else:
            miss.append(s)
    if miss:
        raise SystemExit(f"원화 시트가 아직 없습니다: {', '.join(miss)} ({art_src}) — 원화 할 일이 먼저 끝나야 함")

    # 2) 실제 자료
    dl = proj / "04_assets" / "dl"
    dl.mkdir(exist_ok=True)
    for it in cfg.get("assets", []):
        out = art / it["out"]
        if out.exists():
            continue
        if "pdf" in it:
            pdf = fetch(it["pdf"], dl / (re.sub(r"\W+", "_", it["pdf"].split("/")[-1])[:60] + ".pdf"))
            pdf_crop(pdf, it["page"], it["crop"], out)
        else:
            fetch(it["url"], out)
        print("자료:", out.name)

    # 3) 칸 자르기
    fill = lambda x: x.replace("{art}", str(art)).replace("{project}", str(proj))
    sh([sys.executable, *[fill(x) for x in cfg["prep"]]], cwd=ROOT)

    # 4) 목소리 (이미 있으면 그대로 — 같은 문장은 ElevenLabs 캐시)
    vdir = proj / "03_voice" / cfg.get("voice_dir", "v")
    if not (vdir / "voice.mp3").exists():
        cmd = [sys.executable, ROOT / "scripts/anim/narrate.py", proj / cfg["narration"], vdir]
        if not a.draft_voice and (os.environ.get("ELEVENLABS_API_KEY") or cfg.get("force_elevenlabs")):
            cmd += ["--channel", cfg["channel"]]
        else:
            print("주의: ELEVENLABS_API_KEY 가 없어 edge-tts 초안 목소리로 만듭니다 (업로드 전 ElevenLabs 로 다시)")
        sh(cmd, cwd=ROOT)

    # 5) 장면 → 6) 렌더
    out_dir = proj / "05_edit" / cfg.get("edit_dir", "build")
    out_dir.mkdir(parents=True, exist_ok=True)
    html = out_dir / "ep.html"
    log = sh([sys.executable, ROOT / cfg["ep_script"], art, vdir, html], cwd=ROOT)
    end = re.search(r"END ([\d.]+)", log).group(1)
    bash = shutil.which("bash") or r"C:\Program Files\Git\bin\bash.exe"
    res = out_dir / cfg["output"]
    sh([bash, (ROOT / "scripts/anim/render_all.sh").as_posix(), (out_dir / "r").as_posix(), html.as_posix(),
        (vdir / "voice.mp3").as_posix(), (vdir / "captions.ass").as_posix(), end, res.as_posix(), str(cfg.get("parts", 4))], cwd=ROOT)

    # 7) 확인용 프레임 시트 + Drive 보관
    sheet = out_dir / (res.stem + "_sheet.jpg")
    sh(["ffmpeg", "-v", "error", "-y", "-i", res, "-vf", f"fps=12/{float(end):.0f},scale=480:-1,tile=4x3", "-frames:v", "1", sheet])
    dst = ep_dir / "05_edit"
    dst.mkdir(parents=True, exist_ok=True)
    for f in (res, sheet):
        shutil.copy2(f, dst / f.name)
    mb = res.stat().st_size / 1e6
    line = f"- PC 자동 빌드 완료: Drive `영상/{proj.name}/05_edit/{res.name}` ({float(end)/60:.1f}분, {mb:.0f}MB) · 프레임 시트 `{sheet.name}`"
    rep = proj / "REPORT.md"
    rep.write_text(rep.read_text(encoding="utf-8").rstrip() + "\n" + line + "\n", encoding="utf-8")
    print(line)


if __name__ == "__main__":
    main()
