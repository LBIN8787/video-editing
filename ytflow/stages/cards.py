"""검은 배경 인포 카드 렌더러 (식스시그마식 미니멀 스타일).

관찰한 원칙 (docs/03-benchmark-result.md):
  - 순수 검정 배경, 얇은 흰 글씨, 강조는 빨간색 한 가지
  - 얇은 테두리 박스와 가는 선, 그림자·그라데이션·아이콘 없음
  - 큰 숫자 비교, 흐름도, 빨간 박스로 강조한 표, 기사 헤드라인 카드

scene["card"] 형식 (모든 타입 공통):
  {"type": "number_compare" | "flow" | "table" | "bars" | "line" | "headline" | "text",
   "title": "카드 제목 (선택)",
   "items": [{"label": "...", "value": "...", "sub": "...", "highlight": true}],
   "note": "카드 아래 회색 보조 문장 (선택)"}
"""
from __future__ import annotations

import subprocess
from pathlib import Path

from .. import config


def theme() -> dict:
    t = {"bg": "#000000", "fg": "#FFFFFF", "muted": "#9A9A9A", "accent": "#E8402C", "line": 3}
    t.update(config.load("pipeline").get("edit", {}).get("theme", {}) or {})
    return t


def _rgb(h: str) -> tuple:
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def font_path() -> str:
    path = config.load("pipeline").get("edit", {}).get("card_font")
    if path and Path(path).exists():
        return path
    return subprocess.run(["fc-match", "-f", "%{file}", ":lang=ko"], capture_output=True, text=True).stdout.strip()


class Canvas:
    def __init__(self):
        from PIL import Image, ImageDraw, ImageFont

        ecfg = config.load("pipeline").get("edit", {})
        self.W, self.H = ecfg.get("width", 1920), ecfg.get("height", 1080)
        t = theme()
        self.bg, self.fg, self.muted, self.accent = (_rgb(t[k]) for k in ("bg", "fg", "muted", "accent"))
        self.lw = int(t["line"])
        self.img = Image.new("RGB", (self.W, self.H), self.bg)
        self.d = ImageDraw.Draw(self.img)
        fp = font_path()
        self._font = lambda s: ImageFont.truetype(fp, s) if fp else ImageFont.load_default()

    def f(self, size):
        return self._font(int(size))

    def text(self, x, y, s, size, color=None, anchor="mm"):
        s = s.replace("\u2212", "-").replace("\u2013", "-")  # 폰트에 없는 수학 기호 정리
        self.d.text((x, y), s, font=self.f(size), fill=color or self.fg, anchor=anchor)

    def fit(self, s, size, maxw):
        while size > 18 and self.d.textlength(s, font=self.f(size)) > maxw:
            size -= 2
        return size

    def box(self, x0, y0, x1, y1, color=None, width=None):
        self.d.rectangle([x0, y0, x1, y1], outline=color or self.fg, width=width or self.lw)

    def save(self, path: Path):
        self.img.save(path)


# 하단 자막 영역(약 H-200 ~ H)과 상단 라벨(약 0~80)을 피해서 그린다
TOP, BOTTOM = 150, 0.78


def _title(c: Canvas, card: dict):
    if card.get("title"):
        c.text(c.W / 2, TOP, card["title"], c.fit(card["title"], 46, c.W - 200))


def _note(c: Canvas, card: dict, y=None):
    if card.get("note"):
        c.text(c.W / 2, y or c.H * BOTTOM - 10, card["note"], c.fit(card["note"], 34, c.W - 240), c.muted)


def r_number_compare(c: Canvas, card: dict):
    items = card.get("items", [])[:3]
    _title(c, card)
    n = max(len(items), 1)
    for i, it in enumerate(items):
        x = c.W * (i + 0.5) / n
        col = c.accent if it.get("highlight") else c.fg
        if it.get("label"):
            c.text(x, c.H * 0.33, it["label"], 36, c.muted)
        c.text(x, c.H * 0.47, it.get("value", ""), c.fit(it.get("value", ""), 140, c.W / n - 180), col)
        if it.get("sub"):
            c.text(x, c.H * 0.60, it["sub"], c.fit(it["sub"], 38, c.W / n - 80), c.muted)
    _note(c, card)


def r_flow(c: Canvas, card: dict):
    """items 를 왼쪽→오른쪽 체인으로. 4개 넘으면 두 줄."""
    items = card.get("items", [])
    _title(c, card)
    rows = [items] if len(items) <= 5 else [items[: (len(items) + 1) // 2], items[(len(items) + 1) // 2:]]
    ys = [c.H * 0.46] if len(rows) == 1 else [c.H * 0.36, c.H * 0.60]
    for row, y in zip(rows, ys):
        n = len(row)
        bw = min(400, (c.W - 160) / n - 60)
        gap = (c.W - 160 - bw * n) / max(n - 1, 1)
        for i, it in enumerate(row):
            x0 = 80 + i * (bw + gap)
            col = c.accent if it.get("highlight") else c.fg
            h = 120 if not it.get("sub") else 150
            c.box(x0, y - h / 2, x0 + bw, y + h / 2, col, c.lw + (2 if it.get("highlight") else 0))
            c.text(x0 + bw / 2, y - (18 if it.get("sub") else 0), it.get("label", ""), c.fit(it.get("label", ""), 42, bw - 30), col)
            if it.get("sub"):
                c.text(x0 + bw / 2, y + 36, it["sub"], c.fit(it["sub"], 30, bw - 30), c.muted)
            if i < n - 1:
                ax0, ax1 = x0 + bw + 12, x0 + bw + gap - 12
                c.d.line([ax0, y, ax1, y], fill=c.muted, width=c.lw)
                c.d.polygon([(ax1, y), (ax1 - 16, y - 9), (ax1 - 16, y + 9)], fill=c.muted)
                if it.get("value"):
                    c.text((ax0 + ax1) / 2, y - 30, it["value"], c.fit(it["value"], 26, gap - 10), c.muted)
    _note(c, card)


def r_table(c: Canvas, card: dict):
    items = card.get("items", [])[:7]
    _title(c, card)
    top, bot = c.H * 0.24, c.H * 0.74
    rh = min(110, (bot - top) / max(len(items), 1))
    x0, x1, x2, x3 = 200, 560, 1060, c.W - 200
    for i, it in enumerate(items):
        y = top + rh * (i + 0.5)
        col = c.accent if it.get("highlight") else c.fg
        c.text(x0, y, it.get("label", ""), c.fit(it.get("label", ""), 40, x1 - x0 - 20), c.muted if not it.get("highlight") else col, "lm")
        c.text(x1, y, it.get("value", ""), c.fit(it.get("value", ""), 46, x2 - x1 - 20), col, "lm")
        if it.get("sub"):
            c.text(x2, y, it["sub"], c.fit(it["sub"], 36, x3 - x2 - 20), c.muted if not it.get("highlight") else col, "lm")
        if it.get("highlight"):
            c.box(x0 - 30, y - rh / 2 + 6, x3 + 30, y + rh / 2 - 6, c.accent)
    _note(c, card)


def _num(v) -> bool:
    try:
        float(str(v).replace(",", ""))
        return True
    except ValueError:
        return False


def r_bars(c: Canvas, card: dict):
    """가로 막대. value 는 숫자 문자열, sub 는 막대 옆 표기(없으면 value). 숫자가 아니면 표로."""
    items = card.get("items", [])[:8]
    if not items or not all(_num(it.get("value", "")) for it in items):
        return r_table(c, card)
    _title(c, card)
    vals = []
    for it in items:
        try:
            vals.append(float(str(it.get("value", "0")).replace(",", "")))
        except ValueError:
            vals.append(0.0)
    cap = card.get("cap") or (sorted(vals)[-2] * 1.4 if len(vals) > 2 and max(vals) > 4 * sorted(vals)[-2] else max(vals or [1]))
    top, bot = c.H * 0.24, c.H * 0.74
    rh = (bot - top) / max(len(items), 1)
    x0, x1 = 560, c.W - 360
    for i, (it, v) in enumerate(zip(items, vals)):
        y = top + rh * (i + 0.5)
        col = c.accent if it.get("highlight") else c.fg
        c.text(x0 - 30, y, it.get("label", ""), c.fit(it.get("label", ""), 32, 420), col if it.get("highlight") else c.fg, "rm")
        w = (x1 - x0) * min(v / cap, 1) if cap else 0
        c.d.rectangle([x0, y - rh * 0.28, x0 + max(w, 3), y + rh * 0.28], fill=col if it.get("highlight") else c.muted)
        label = it.get("sub") or it.get("value", "")
        c.text(x0 + w + 20, y, label + (" ≫" if v > cap else ""), 30, col, "lm")
    _note(c, card)


def r_headline(c: Canvas, card: dict):
    """흰 박스 안 검은 글씨 — 기사·보도자료 헤드라인 재현(원문 캡처가 있으면 그것을 우선)."""
    x0, y0, x1, y1 = 300, c.H * 0.22, c.W - 300, c.H * 0.66
    c.d.rectangle([x0, y0, x1, y1], fill=c.fg)
    t = card.get("title", "")
    c.text(x0 + 60, y0 + 90, t, c.fit(t, 64, x1 - x0 - 120), c.bg, "lm")
    for i, it in enumerate(card.get("items", [])[:3]):
        c.text(x0 + 60, y0 + 190 + i * 62, it.get("label", ""), c.fit(it.get("label", ""), 36, x1 - x0 - 120),
               c.accent if it.get("highlight") else (70, 70, 70), "lm")
    if card.get("note"):
        c.text(x0 + 60, y1 - 50, card["note"], 26, (120, 120, 120), "lm")


def r_text(c: Canvas, card: dict):
    t = card.get("title", "")
    c.text(c.W / 2, c.H * 0.44, t, c.fit(t, 96, c.W - 300), c.accent if card.get("highlight") else c.fg)
    for i, it in enumerate(card.get("items", [])[:3]):
        c.text(c.W / 2, c.H * 0.56 + i * 56, it.get("label", ""), c.fit(it.get("label", ""), 38, c.W - 300), c.muted)


def r_line(c: Canvas, card: dict):
    """꺾은선 (정지 화면). items 순서대로 x축, value 숫자, highlight 지점에 빨간 점과 값."""
    items = card.get("items", [])
    if len(items) < 2 or not all(_num(it.get("value", "")) for it in items):
        return r_table(c, card)
    vals = [float(str(it["value"]).replace(",", "")) for it in items]
    _title(c, card)
    x0, x1, y0, y1 = 220, c.W - 260, c.H * 0.70, c.H * 0.26
    lo, hi = min(vals), max(vals)
    span = (hi - lo) or 1
    pts = [(x0 + (x1 - x0) * i / (len(vals) - 1), y0 - (v - lo) / span * (y0 - y1)) for i, v in enumerate(vals)]
    c.d.line([x0, y0 + 20, x1, y0 + 20], fill=c.muted, width=1)
    c.d.line(pts, fill=c.fg, width=c.lw + 1)
    for i in (0, len(items) - 1):
        c.text(pts[i][0], y0 + 50, items[i].get("label", ""), 28, c.muted)
    for (x, y), it in zip(pts, items):
        if it.get("highlight"):
            c.d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=c.accent)
            c.text(x, y - 44, it.get("sub") or it.get("value", ""), 44, c.accent)
    _note(c, card)


RENDER = {"line": r_line, "number_compare": r_number_compare, "flow": r_flow, "table": r_table, "bars": r_bars,
          "headline": r_headline, "text": r_text}


def render(card: dict, path: Path) -> None:
    c = Canvas()
    RENDER.get(card.get("type", "text"), r_text)(c, card)
    c.save(path)


def placeholder(path: Path, note: str) -> None:
    """실제 소스가 아직 없는 장면: 검은 화면 + 가운데 회색 안내 (편집 시 교체)."""
    c = Canvas()
    c.box(200, c.H * 0.30, c.W - 200, c.H * 0.62, c.muted, 2)
    c.text(c.W / 2, c.H * 0.40, "[ 소스 필요 ]", 44, c.muted)
    c.text(c.W / 2, c.H * 0.50, note, c.fit(note, 32, c.W - 480), c.muted)
    c.save(path)


def shot_on_black(image_path: Path, out: Path) -> None:
    """기사 캡처를 검은 화면 가운데 놓는다 (식스시그마식 헤드라인 화면)."""
    from PIL import Image

    c = Canvas()
    im = Image.open(image_path).convert("RGB")
    maxw, maxh = c.W - 360, c.H * 0.66
    sc = min(maxw / im.width, maxh / im.height)
    im = im.resize((int(im.width * sc), int(im.height * sc)))
    x, y = (c.W - im.width) // 2, int(c.H * 0.42 - im.height / 2)
    c.img.paste(im, (x, max(y, 90)))
    c.box(x - 1, max(y, 90) - 1, x + im.width, max(y, 90) + im.height, c.muted, 1)
    c.save(out)
