"""흰 곰 편 v3 원화 준비 — 2×2 시트(GPT 이미지, PC Codex) → 칸 4장(1920×1080) + 조각 + 논문 판.

    python scripts/anim/prep_whitebear.py <art 폴더> [--paper <논문 첫 장 잘라낸 png>] [--dry]

시트: night · lab · lab2 · mind · end (02_script/art_orders.md). 칸 번호 1=왼쪽 위, 2=오른쪽 위, 3=왼쪽 아래, 4=오른쪽 아래.
--dry: 시트가 아직 없으면 칸마다 이름을 적은 회색 자리 그림을 만든다(대사 시각·연출 점검용 — 완성본에는 쓰지 않음).
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[2]
FONT = ROOT / "ytflow/assets/fonts/NanumGothic-ExtraBold.ttf"
SHEETS = ["night", "lab", "lab2", "mind", "end", "room", "lab3", "assoc", "sleep"]   # v4 에서 뒤 넷 추가
W, H = 1920, 1080


def cut_sheet(sheet: Path, out: Path, name: str) -> None:
    im = Image.open(sheet).convert("RGB")
    w2, h2 = im.width // 2, im.height // 2
    for k, (x, y) in enumerate([(0, 0), (w2, 0), (0, h2), (w2, h2)], 1):
        cell = im.crop((x, y, x + w2, y + h2))
        ImageOps.fit(cell, (W, H), Image.LANCZOS).save(out / f"{name}-{k}.png")


def placeholder(out: Path, name: str) -> None:
    f = ImageFont.truetype(str(FONT), 90)
    for k in range(1, 5):
        im = Image.new("RGB", (W, H), (120 + k * 12, 118 + k * 10, 112 + k * 8))
        d = ImageDraw.Draw(im)
        d.text((W / 2, H / 2), f"{name}-{k} (원화 자리)", font=f, fill=(250, 248, 240), anchor="mm")
        im.save(out / f"{name}-{k}.png")


def pieces(out: Path) -> None:
    """칸 만화에 쓰는 조각: 종(lab-2 가운데), 빨간 차(end-4 가운데)."""
    lab2 = Image.open(out / "lab-2.png")
    side = int(H * 0.6)
    lab2.crop((W // 2 - side // 2 - 260, H // 2 - side // 2, W // 2 + side // 2 - 260, H // 2 + side // 2)).resize((360, 360)).save(out / "bell.png")
    car = Image.open(out / "end-4.png")
    car.crop((W * 0.18, H * 0.2, W * 0.82, H * 0.8)).resize((640, 360)).save(out / "vw.png")


def paper_plate(src: Path, out: Path) -> None:
    """논문 첫 장(저자 공개 PDF 를 잘라낸 그림)을 어두운 바탕 가운데에 — 스포트라이트 좌표는 이 판 기준."""
    bg = Image.new("RGB", (W, H), (18, 18, 22))
    p = Image.open(src).convert("RGB")
    pw = 1500
    ph = round(p.height * pw / p.width)
    p = p.resize((pw, ph), Image.LANCZOS)
    x0, y0 = (W - pw) // 2, (H - ph) // 2
    card = Image.new("RGB", (pw + 40, ph + 40), (252, 250, 244))
    card.paste(p, (20, 20))
    bg.paste(card, (x0 - 20, y0 - 20))
    bg.save(out / "paperdoc.png")
    (out / "paperdoc.box").write_text(f"{x0} {y0} {pw} {ph}", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("art", type=Path)
    ap.add_argument("--paper", type=Path)
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    a.art.mkdir(parents=True, exist_ok=True)
    for s in SHEETS:
        src = next((p for p in (a.art / f"{s}.png", a.art / f"{s}.jpg") if p.exists()), None)
        if src:
            cut_sheet(src, a.art, s)
            print("cut", s)
        elif a.dry:
            placeholder(a.art, s)
            print("placeholder", s)
        else:
            raise SystemExit(f"시트가 없습니다: {a.art / s}.png (PC 원화 주문 확인)")
    pieces(a.art)
    if a.paper:
        paper_plate(a.paper, a.art)
    for n, c in (("black.png", (10, 10, 12)),):
        if not (a.art / n).exists():
            Image.new("RGB", (W, H), c).save(a.art / n)
    print("ok", a.art)


if __name__ == "__main__":
    main()
