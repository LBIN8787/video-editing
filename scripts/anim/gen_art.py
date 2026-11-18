"""원화 주문서(orders.json) → Codex 구독 이미지 생성(ChatGPT 한도 안, 추가 요금 없음) → 시트는 조각으로 자름.

    python scripts/anim/gen_art.py <출력폴더> [--video curiosity] [--only id1,id2] [--workers 3] [--refs <합격 화풍 그림 폴더>]

plate 은 그대로 <video>/<id>.png, sheet 은 <video>/<id>_sheet.png → <video>/<piece>.png (ytflow.stages.imagegen.cut).
이미 있는 파일은 건너뜀(다시 만들려면 지우고 실행).
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from cutout import cut  # noqa: E402  (scipy 없이)

PLATE = ("16:9 wide landscape PNG. No text, no letters, no logos, no watermark. ")
SHEET = ("Wide landscape PNG on a plain pure white background. The items are arranged in one horizontal row, "
         "each complete, not overlapping, with generous empty white space between them and no ground shadows. "
         "No text, no labels, no numbers, no logos. ")


def one(o: dict, style: dict, out: Path, refs: Path) -> str:
    vd = out / o["video"]
    vd.mkdir(parents=True, exist_ok=True)
    png = vd / (f"{o['id']}_sheet.png" if o["kind"] == "sheet" else f"{o['id']}.png")
    if not png.exists():
        prompt = (SHEET if o["kind"] == "sheet" else PLATE) + style["text"] + " " + o["prompt"]
        task = (f"Use the $imagegen skill to generate ONE image and save it exactly to {png.resolve()} . "
                f"Use the attached image(s) only as the art-style reference (do not copy their content). "
                f"Do not edit any other file. Prompt: {prompt}")
        cmd = [shutil.which("codex") or "codex", "exec", "--skip-git-repo-check", "-s", "workspace-write", "-C", str(vd.resolve()), "-"]   # 프롬프트는 표준입력, -i 는 뒤에 (값을 여러 개 받음)
        for r in style["ref"]:
            cmd += ["-i", str((refs / r).resolve())]
        for r in o.get("ref", []):   # 같은 인물 유지: 이미 그린 시트를 참조로
            cmd += ["-i", str((out / o["video"] / r).resolve())]
        for attempt in range(2):   # 한 장이 실패해도 나머지는 계속 (한 번 다시 시도)
            try:
                subprocess.run(cmd, input=task, text=True, encoding="utf-8", check=True, timeout=1200,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                break
            except Exception as e:
                if attempt:
                    return f"FAIL {o['id']}: {e}"
        if not png.exists():
            return f"FAIL {o['id']}: not saved"
    if o["kind"] == "sheet" and not all((vd / f"{p}.png").exists() for p in o["pieces"]):
        try:
            cut(png, vd, o["pieces"])
        except Exception as e:  # 조각 수가 다르면 다시 생성해야 함
            return f"CUT? {o['id']}: {e}"
    return f"ok {o['id']}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out", type=Path)
    ap.add_argument("--video", default="")
    ap.add_argument("--only", default="")
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--refs", type=Path, default=Path("G:/내 드라이브/ytflow/영상/20261118-script-motion/art"))
    ap.add_argument("--orders", type=Path, default=Path(__file__).with_name("orders.json"))
    a = ap.parse_args()
    spec = json.loads(a.orders.read_text(encoding="utf-8"))
    only = {x for x in a.only.split(",") if x}
    todo = [o for o in spec["orders"] if (not a.video or o["video"] == a.video) and (not only or o["id"] in only)]
    with ThreadPoolExecutor(a.workers) as ex:
        for r in ex.map(lambda o: one(o, spec["styles"][o["video"]], a.out, a.refs), todo):
            print(r, flush=True)


if __name__ == "__main__":
    main()
