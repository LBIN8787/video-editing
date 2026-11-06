"""종이 질감 손그림 애니메이션 스타일 (미주일기 화면 분석 기준).

관찰한 화면 (2026-11-06, 미주일기 영상 12편의 공개 미리보기 프레임):
  - 구겨진 크림색 종이 배경, 남색 잉크 손그림 선, 빨간 펜 강조
  - 명조체 제목·큰 숫자, 손글씨 메모와 밑줄
  - 인물·뉴스 사진은 종이 위에 붙인 콜라주 또는 전체 화면 + 명조 흰 글씨
  - 하단 가운데 반투명 어두운 상자 자막
움직임(정지 프레임으로는 보이지 않으므로 이 장르의 관행으로 설계):
  - 선과 상자는 펜으로 그리듯 '그려지며' 등장, 글씨는 아래에서 살짝 떠오르며 나타남
  - 숫자는 0에서 목표값까지 올라감, 강조 숫자에는 빨간 밑줄이 그어짐
  - 사진은 살짝 기울어진 채 '툭' 붙고 마스킹테이프가 얹힘
등장 애니메이션(anim_seconds) 뒤에는 마지막 장면을 장면 길이만큼 유지한다.

카드 스키마는 cards.py 와 같다 (number_compare / flow / table / bars / headline / text).
"""
from __future__ import annotations

import math
import random
import re
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from .. import config

FONT_DIR = Path(__file__).resolve().parent.parent / "assets" / "fonts"
SERIF = FONT_DIR / "NanumMyeongjo-ExtraBold.ttf"
SERIF_B = FONT_DIR / "NanumMyeongjo-Bold.ttf"
PEN = FONT_DIR / "NanumPenScript-Regular.ttf"
SANS = FONT_DIR / "NanumGothic-Bold.ttf"
SANS_X = FONT_DIR / "NanumGothic-ExtraBold.ttf"
_fonts: dict = {}

# 렌더러 겉모습 프로필. paper(미주일기)가 기본, flat.py 가 평면 인포그래픽용으로 바꿔 쓴다.
PAPER_PROFILE = {"texture": True, "wobble": 1.0, "tape": True, "underline": True, "top": 130, "tilt": True,
                 "mark": "circle",  # 표 강조: circle(빨간 펜 동그라미) | box(곧은 빨간 상자)
                 "fonts": {"title": SERIF, "value": SERIF, "box": SERIF_B, "note": PEN, "label": SANS}}
PROFILE = dict(PAPER_PROFILE)


def FT(role: str) -> Path:
    return PROFILE["fonts"][role]


def F(path: Path, size: int) -> ImageFont.FreeTypeFont:
    key = (path, int(size))
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(str(path), int(size))
    return _fonts[key]


def _rgb(h: str) -> tuple:
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def cfg() -> dict:
    e = config.load("pipeline").get("edit", {})
    p = {"base": "#EEE7DA", "ink": "#22304D", "red": "#C4452F", "anim_seconds": 1.2}
    p.update(e.get("paper") or {})
    return {"W": e.get("width", 1920), "H": e.get("height", 1080), "fps": e.get("fps", 30), **p}


def ease(p: float) -> float:
    p = min(max(p, 0.0), 1.0)
    return 1 - (1 - p) ** 3


# ---------------------------------------------------------------- 종이 배경
_bg_cache: dict = {}


def paper_bg(W: int, H: int, seed: int = 7) -> Image.Image:
    """크림색 + 미세 노이즈 + 구김(큰 얼룩과 접힌 선)."""
    c = cfg()
    key = (W, H, seed, PROFILE["texture"], c["base"])
    if key in _bg_cache:
        return _bg_cache[key].copy()
    if not PROFILE["texture"]:  # 평면 스타일: 무늬 없는 단색 배경
        img = Image.new("RGB", (W, H), _rgb(c["base"]))
        _bg_cache[key] = img
        return img.copy()
    rng = np.random.default_rng(seed)
    base = np.ones((H, W, 3), np.float32) * np.array(_rgb(c["base"]), np.float32)
    small = rng.normal(0, 1, (H // 24 + 1, W // 24 + 1)).astype(np.float32)
    blot = np.array(Image.fromarray(((small - small.min()) / (np.ptp(small) + 1e-6) * 255).astype(np.uint8))
                    .resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(40)), np.float32) / 255.0
    base *= (0.94 + 0.08 * blot)[..., None]
    crease = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(crease)
    for _ in range(9):  # 구김 선
        x0, y0 = rng.uniform(0, W), rng.uniform(0, H)
        ang, ln = rng.uniform(0, math.pi), rng.uniform(300, 1100)
        d.line([x0, y0, x0 + math.cos(ang) * ln, y0 + math.sin(ang) * ln], fill=int(rng.uniform(40, 90)), width=2)
    crease = np.array(crease.filter(ImageFilter.GaussianBlur(6)), np.float32) / 255.0
    base *= (1 - 0.06 * crease)[..., None]
    base += rng.normal(0, 3.2, (H, W, 1)).astype(np.float32)
    img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8))
    _bg_cache[key] = img
    return img.copy()


# ---------------------------------------------------------------- 손그림 도형
def wobble(points, rng, amp=2.2, step=24):
    """직선을 잘게 나눠 손떨림을 준다 (PROFILE wobble=0 이면 곧은 선)."""
    amp *= PROFILE["wobble"]
    out = []
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        n = max(int(math.hypot(x1 - x0, y1 - y0) / step), 1)
        for i in range(n):
            t = i / n
            out.append((x0 + (x1 - x0) * t + rng.uniform(-amp, amp), y0 + (y1 - y0) * t + rng.uniform(-amp, amp)))
    out.append(points[-1])
    return out


def partial(points, p):
    """폴리라인을 전체 길이의 p 만큼만 (펜으로 그리는 효과)."""
    if p >= 1:
        return points
    segs = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(points, points[1:])]
    target, acc, out = sum(segs) * p, 0.0, [points[0]]
    for (a, b), L in zip(zip(points, points[1:]), segs):
        if acc + L >= target:
            t = (target - acc) / L if L else 0
            out.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
            return out
        out.append(b)
        acc += L
    return out


def rect_path(x0, y0, x1, y1, rng):
    o = rng.uniform(4, 9)  # 손으로 그린 상자는 시작점에서 살짝 겹친다
    return wobble([(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0 - 2), (x0 + o * 3, y0 - 1)], rng)


def ellipse_path(cx, cy, rx, ry, rng):
    pts, n = [], 64
    for i in range(n + 6):
        a = -0.6 + 2 * math.pi * i / n
        r = 1 + rng.uniform(-0.03, 0.03)
        pts.append((cx + rx * r * math.cos(a), cy + ry * r * math.sin(a)))
    return pts


def arrow_path(x0, y0, x1, y1, rng):
    body = wobble([(x0, y0), (x1, y1)], rng, amp=1.5)
    ang = math.atan2(y1 - y0, x1 - x0)
    h1 = (x1 - 22 * math.cos(ang - 0.45), y1 - 22 * math.sin(ang - 0.45))
    h2 = (x1 - 22 * math.cos(ang + 0.45), y1 - 22 * math.sin(ang + 0.45))
    return body, [h1, (x1, y1), h2]


# ---------------------------------------------------------------- 타임라인 요소
class Scene:
    """요소마다 (시작초, 끝초, 그리기 함수(img, draw, 진행도 0~1))."""

    def __init__(self, seed=1):
        c = cfg()
        self.c, self.W, self.H, self.fps = c, c["W"], c["H"], c["fps"]
        self.ink, self.red = _rgb(c["ink"]), _rgb(c["red"])
        self.rng = random.Random(seed)
        self.items: list = []
        self.t = 0.0  # 다음 요소의 기본 시작 시각

    def add(self, fn, dur=0.45, at=None, gap=0.12):
        t0 = self.t if at is None else at
        self.items.append((t0, t0 + dur, fn))
        self.t = t0 + gap
        return self

    # --- 기본 요소
    def text(self, x, y, s, font, color, anchor="mm", rise=18, dur=0.45, at=None, gap=0.12):
        tile = _text_tile(s, font, color)
        w, h = tile.size
        ax = {"l": 0, "m": w / 2, "r": w}[anchor[0]]
        ay = {"t": 0, "m": h / 2, "b": h}[anchor[1]]

        def draw(img, d, p):
            e = ease(p)
            im = tile if e >= 1 else _fade(tile, e)
            img.alpha_composite(im, (int(x - ax), int(y - ay + (1 - e) * rise)))
        return self.add(draw, dur, at, gap)

    def counter(self, x, y, s, font, color, dur=0.9, at=None, gap=0.15):
        """'4.13%' '990억 달러' 처럼 숫자 하나가 든 값은 0부터 올라가게."""
        m = re.search(r"\d[\d,]*(?:\.\d+)?", s)
        if not m or len(re.findall(r"\d[\d,]*(?:\.\d+)?", s)) > 1:
            return self.text(x, y, s, font, color, dur=dur, at=at, gap=gap)
        num = float(m.group().replace(",", ""))
        dec = len(m.group().split(".")[1]) if "." in m.group() else 0
        comma = "," in m.group()

        def draw(img, d, p):
            e = ease(p)
            v = num * e
            sv = f"{v:,.{dec}f}" if comma else f"{v:.{dec}f}"
            cur = s[:m.start()] + sv + s[m.end():]
            tile = _text_tile(cur, font, color)
            img.alpha_composite(_fade(tile, min(1, e * 3)), (int(x - tile.size[0] / 2), int(y - tile.size[1] / 2)))
        return self.add(draw, dur, at, gap)

    def stroke(self, pts, color, width=4, dur=0.5, at=None, gap=0.1):
        def draw(img, d, p):
            pp = partial(pts, ease(p))
            if len(pp) > 1:
                d.line(pp, fill=color, width=width, joint="curve")
        return self.add(draw, dur, at, gap)

    def box(self, x0, y0, x1, y1, color, width=4, dur=0.45, at=None, gap=0.1, fill=None):
        pts = rect_path(x0, y0, x1, y1, self.rng)
        if fill:
            def bg(img, d, p):
                if p > 0.2:
                    d.rectangle([x0 + 3, y0 + 3, x1 - 3, y1 - 3], fill=fill)
            self.add(bg, dur, at, 0)
        return self.stroke(pts, color, width, dur, at, gap)

    def arrow(self, x0, y0, x1, y1, color, dur=0.4, at=None, gap=0.1):
        body, head = arrow_path(x0, y0, x1, y1, self.rng)
        t0 = self.t if at is None else at
        self.stroke(body, color, 4, dur * 0.7, t0, 0)
        return self.stroke(head, color, 4, dur * 0.3, t0 + dur * 0.7, gap)

    def underline(self, x0, x1, y, color, dur=0.35, at=None, gap=0.1):
        if not PROFILE["underline"]:
            return self
        pts = wobble([(x0, y), ((x0 + x1) / 2, y + 4), (x1, y - 2)], self.rng, amp=1.6, step=30)
        return self.stroke(pts, color, 6, dur, at, gap)

    def circle(self, cx, cy, rx, ry, color, dur=0.5, at=None, gap=0.1):
        return self.stroke(ellipse_path(cx, cy, rx, ry, self.rng), color, 5, dur, at, gap)

    def photo(self, im: Image.Image, cx, cy, maxw, maxh, angle=-2.0, caption="", dur=0.5, at=None, gap=0.2):
        """종이 위에 사진을 붙인다: 흰 테두리 + 그림자 + 테이프, 살짝 커지며 등장."""
        im = im.convert("RGB")
        sc = min(maxw / im.width, maxh / im.height)
        im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))))
        b = 14
        card = Image.new("RGBA", (im.width + 2 * b, im.height + 2 * b), (250, 248, 243, 255))
        card.paste(im, (b, b))
        shadow = Image.new("RGBA", (card.width + 60, card.height + 60), (0, 0, 0, 0))
        ImageDraw.Draw(shadow).rectangle([30, 36, 30 + card.width, 36 + card.height], fill=(40, 30, 20, 90))
        shadow = shadow.filter(ImageFilter.GaussianBlur(12))
        shadow.alpha_composite(card, (30, 30))
        if PROFILE["tape"]:
            tape = Image.new("RGBA", (180, 46), (236, 224, 190, 170))
            shadow.alpha_composite(tape.rotate(4, expand=True), (shadow.width // 2 - 90, 6))
        sprite = shadow.rotate(angle, expand=True, resample=Image.BICUBIC)

        def draw(img, d, p):
            e = ease(p)
            s = 0.92 + 0.08 * e
            sp = sprite if s >= 0.999 else sprite.resize((int(sprite.width * s), int(sprite.height * s)))
            img.alpha_composite(_fade(sp, min(1, e * 2)), (int(cx - sp.width / 2), int(cy - sp.height / 2)))
        self.add(draw, dur, at, gap)
        if caption:
            self.text(cx, cy + sprite.height / 2 + 8, caption, F(FT("note"), 40), self.ink, "mt", dur=0.4)
        return self

    # --- 렌더링
    def render(self, out: Path, duration: float):
        last = max([t1 for _, t1, _ in self.items] + [self.t])  # 가장 늦게 끝나는 요소까지 다 그린 뒤 정지
        anim = min(max(last + 0.25, float(self.c["anim_seconds"])), max(duration, 0.5))
        n = max(1, int(round(anim * self.fps)))
        bg = paper_bg(self.W, self.H).convert("RGBA")
        hold = max(0.0, duration - n / self.fps)
        cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
               "-s", f"{self.W}x{self.H}", "-r", str(self.fps), "-i", "-",
               "-vf", f"tpad=stop_mode=clone:stop_duration={hold:.3f}",
               "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "20", str(out)]
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        for i in range(n):
            t = i / self.fps
            frame = bg.copy()
            d = ImageDraw.Draw(frame)
            for t0, t1, fn in self.items:
                if t >= t0:
                    fn(frame, d, (t - t0) / max(t1 - t0, 1e-3))
            proc.stdin.write(frame.convert("RGB").tobytes())
        proc.stdin.close()
        proc.wait()

    def still(self, out: Path):
        frame = paper_bg(self.W, self.H).convert("RGBA")
        d = ImageDraw.Draw(frame)
        for t0, t1, fn in self.items:
            fn(frame, d, 1.0)
        frame.convert("RGB").save(out)


_tile_cache: dict = {}
_cmaps: dict = {}


def _has_glyphs(font, s) -> bool:
    path = getattr(font, "path", None)
    if not path:
        return True
    if path not in _cmaps:
        from fontTools.ttLib import TTFont
        _cmaps[path] = set(TTFont(path, lazy=True).getBestCmap().keys())
    return all(ord(ch) in _cmaps[path] or ch.isspace() for ch in s)


def _text_tile(s, font, color):
    s = s.replace("\u2212", "-").replace("\u2013", "-")
    key = (s, id(font), color)
    if not _has_glyphs(font, s):  # 원문자는 나눔 글꼴에 없어서 '1.' 형태로
        s = s.translate(str.maketrans({"①": "1.", "②": "2.", "③": "3.", "④": "4.", "⑤": "5."}))
    if key not in _tile_cache and not _has_glyphs(font, s):
        # 손글씨 폰트에 없는 글자(→ · 등)가 있으면 같은 크기의 고딕으로 대신 쓴다
        font = F(SANS, int(font.size * 0.8))
    if key not in _tile_cache:
        bb = font.getbbox(s)
        im = Image.new("RGBA", (bb[2] - bb[0] + 8, bb[3] - bb[1] + 8), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((4 - bb[0], 4 - bb[1]), s, font=font, fill=color)
        _tile_cache[key] = im
    return _tile_cache[key]


def _fade(im, a):
    if a >= 1:
        return im
    r, g, b, al = im.split()
    return Image.merge("RGBA", (r, g, b, al.point(lambda v: int(v * a))))


def fit(font_path, s, size, maxw):
    while size > 20 and F(font_path, size).getlength(s) > maxw:
        size -= 2
    return F(font_path, size)


# ---------------------------------------------------------------- 카드 레이아웃
TOP = 130  # 제목 y


def _title(S: Scene, card: dict):
    TOP = PROFILE.get("top", 130)  # 위쪽 자막을 쓰는 스타일은 제목을 아래로
    if card.get("title"):
        f = fit(FT("title"), card["title"], 60, S.W - 300)
        S.text(S.W / 2, TOP, card["title"], f, S.ink)
        w = f.getlength(card["title"])
        S.underline(S.W / 2 - w / 2, S.W / 2 + w / 2, TOP + 44, S.red, dur=0.3)


def _note(S: Scene, card: dict, y=None):
    if card.get("note"):
        S.text(S.W / 2, y or S.H * 0.80, card["note"], fit(FT("note"), card["note"], 50, S.W - 400), S.red, dur=0.4)


def l_number_compare(S, card):
    _title(S, card)
    items = card.get("items", [])[:3]
    n = max(len(items), 1)
    for i, it in enumerate(items):
        x = S.W * (i + 0.5) / n
        col = S.red if it.get("highlight") else S.ink
        if it.get("label"):
            S.text(x, S.H * 0.33, it["label"], F(FT("label"), 36), (90, 96, 110))
        f = fit(FT("value"), it.get("value", ""), 150, S.W / n - 160)
        S.counter(x, S.H * 0.48, it.get("value", ""), f, col)
        if it.get("highlight"):
            w = f.getlength(it.get("value", ""))
            S.underline(x - w / 2, x + w / 2, S.H * 0.48 + 82, S.red, dur=0.35)
        if it.get("sub"):
            S.text(x, S.H * 0.62, it["sub"], fit(FT("note"), it["sub"], 54, S.W / n - 120), S.ink)
    _note(S, card)


def l_flow(S, card):
    _title(S, card)
    items = card.get("items", [])
    n = max(len(items), 1)
    bw = min(330, (S.W - 160) / n - 70)
    gap = (S.W - 160 - bw * n) / max(n - 1, 1)
    y = S.H * 0.47
    for i, it in enumerate(items):
        x0 = 80 + i * (bw + gap)
        col = S.red if it.get("highlight") else S.ink
        h = 150
        S.box(x0, y - h / 2, x0 + bw, y + h / 2, col, 5 if it.get("highlight") else 4, fill=(246, 242, 233))
        S.text(x0 + bw / 2, y - (20 if it.get("sub") else 0), it.get("label", ""), fit(FT("box"), it.get("label", ""), 44, bw - 30), col)
        if it.get("sub"):
            S.text(x0 + bw / 2, y + 36, it["sub"], fit(FT("note"), it["sub"], 42, bw - 24), (90, 96, 110))
        if i < n - 1:
            ax0, ax1 = x0 + bw + 14, x0 + bw + gap - 14
            S.arrow(ax0, y, ax1, y, S.ink)
            if it.get("value"):
                S.text((ax0 + ax1) / 2, y - 40, it["value"], fit(FT("note"), it["value"], 40, gap), S.red)
    _note(S, card)


def l_table(S, card):
    _title(S, card)
    items = card.get("items", [])[:6]
    top, bot = S.H * 0.27, S.H * 0.74
    rh = min(120, (bot - top) / max(len(items), 1))
    x0, x1, x2, x3 = 200, 560, 1060, S.W - 200
    for i, it in enumerate(items):
        y = top + rh * (i + 0.5)
        col = S.red if it.get("highlight") else S.ink
        S.text(x0, y, it.get("label", ""), fit(FT("label"), it.get("label", ""), 38, x1 - x0 - 20), (90, 96, 110) if not it.get("highlight") else col, "lm", gap=0.02)
        S.text(x1, y, it.get("value", ""), fit(FT("value"), it.get("value", ""), 50, x2 - x1 - 20), col, "lm", gap=0.02)
        if it.get("sub"):
            S.text(x2, y, it["sub"], fit(FT("note"), it["sub"], 48, x3 - x2 - 20), col, "lm", gap=0.02)
        S.t += 0.14
        if i < len(items) - 1:
            S.stroke(wobble([(x0, y + rh / 2), (x3, y + rh / 2)], S.rng, amp=1.0, step=60), (170, 165, 150), 2, 0.3, gap=0.02)
    for i, it in enumerate(items):
        if it.get("highlight"):
            y = top + rh * (i + 0.5)
            if PROFILE.get("mark") == "box":
                S.box(x0 - 24, y - rh * 0.45, x3 + 24, y + rh * 0.45, S.red, 4, dur=0.4)
            else:
                S.circle((x0 + x3) / 2, y, (x3 - x0) / 2 + 30, rh * 0.55, S.red, dur=0.55)
    _note(S, card)


def numeric(v) -> bool:
    try:
        float(str(v).replace(",", ""))
        return True
    except ValueError:
        return False


def l_bars(S, card):
    items = card.get("items", [])[:8]
    if not items or not all(numeric(it.get("value", "")) for it in items):
        return l_table(S, card)  # 값이 순수 숫자가 아니면 막대를 그릴 수 없으므로 표로
    _title(S, card)
    vals = []
    for it in items:
        try:
            vals.append(float(str(it.get("value", "0")).replace(",", "")))
        except ValueError:
            vals.append(0.0)
    srt = sorted(vals)
    cap = card.get("cap") or (srt[-2] * 1.4 if len(vals) > 2 and srt[-1] > 4 * srt[-2] else max(vals or [1]))
    top, bot = S.H * 0.24, S.H * 0.76
    rh = (bot - top) / max(len(items), 1)
    x0, x1 = 560, S.W - 360
    for i, (it, v) in enumerate(zip(items, vals)):
        y = top + rh * (i + 0.5)
        col = S.red if it.get("highlight") else S.ink
        S.text(x0 - 30, y, it.get("label", ""), fit(FT("label"), it.get("label", ""), 34, 420), col, "rm", gap=0.02)
        w = (x1 - x0) * min(v / cap, 1) if cap else 0
        hh = rh * 0.26

        def bar(img, d, p, y=y, w=w, col=col, hh=hh):
            ww = max(3, w * ease(p))
            d.rectangle([x0, y - hh, x0 + ww, y + hh], fill=col + (255,) if len(col) == 3 else col)
            if PROFILE["texture"]:
                for k in range(int(x0) + 8, int(x0 + ww), 14):  # 손그림 빗금 느낌
                    d.line([k, y + hh, k + 10, y - hh], fill=(238, 231, 218), width=1)
        S.add(bar, 0.5, gap=0.02)
        S.text(x0 + w + 20, y, (it.get("sub") or it.get("value", "")) + (" ≫" if v > cap else ""), F(FT("note"), 44), col, "lm", gap=0.1)
    _note(S, card)


def l_headline(S, card):
    """신문 스크랩처럼 흰 종이 조각을 붙인다."""
    w, h = 1300, 470
    clip = Image.new("RGB", (w, h), (252, 251, 247))
    d = ImageDraw.Draw(clip)
    t = card.get("title", "")
    d.text((60, 70), t, font=fit(FT("title"), t, 72, w - 120), fill=(25, 25, 25))
    d.line([60, 170, w - 60, 170], fill=(60, 60, 60), width=2)
    for i, it in enumerate(card.get("items", [])[:3]):
        d.text((60, 205 + i * 70), it.get("label", ""), font=fit(FT("label"), it.get("label", ""), 40, w - 120),
               fill=_rgb(cfg()["red"]) if it.get("highlight") else (70, 70, 70))
    if card.get("note"):
        d.text((60, h - 60), card["note"], font=F(FT("label"), 26), fill=(130, 130, 130))
    S.photo(clip, S.W / 2, S.H * 0.45, w, h, angle=-1.5 if PROFILE.get("tilt", True) else 0.0)


def l_text(S, card):
    t = card.get("title", "")
    f = fit(FT("title"), t, 104, S.W - 300)
    S.text(S.W / 2, S.H * 0.43, t, f, S.red if card.get("highlight") else S.ink, rise=26, dur=0.6)
    w = f.getlength(t)
    S.underline(S.W / 2 - w / 2, S.W / 2 + w / 2, S.H * 0.43 + 70, S.red, dur=0.45)
    for i, it in enumerate(card.get("items", [])[:3]):
        S.text(S.W / 2, S.H * 0.58 + i * 64, it.get("label", ""), fit(FT("note"), it.get("label", ""), 56, S.W - 300), S.ink)


def l_line(S, card):
    """꺾은선(주가·지표 추이). items 순서대로 x축, value 는 숫자. 왼쪽에서 오른쪽으로 그려진다.
    highlight 항목에 점과 값 표시, sub 는 그 지점 설명."""
    _title(S, card)
    items = card.get("items", [])
    if len(items) < 2 or not all(numeric(it.get("value", "")) for it in items):
        return l_table(S, card)  # 숫자 시계열이 아니면 표로
    vals = [float(str(it["value"]).replace(",", "")) for it in items]
    x0, x1, y0, y1 = 220, S.W - 260, S.H * 0.70, S.H * 0.26
    lo, hi = min(vals), max(vals)
    span = (hi - lo) or 1
    pts = [(x0 + (x1 - x0) * i / (len(vals) - 1), y0 - (v - lo) / span * (y0 - y1)) for i, v in enumerate(vals)]
    S.stroke([(x0, y0 + 20), (x1, y0 + 20)], (200, 196, 186), 2, 0.25, gap=0.05)      # 기준선
    for i in (0, len(items) - 1):
        S.text(pts[i][0], y0 + 50, items[i].get("label", ""), F(FT("label"), 30), (120, 120, 120), gap=0.0)
    S.stroke(pts, S.ink, 5, min(1.6, 0.25 * len(pts)), gap=min(1.6, 0.25 * len(pts)))
    for (x, y), it, v in zip(pts, items, vals):
        if it.get("highlight"):
            col = S.red

            def dot(img, d, p, x=x, y=y, col=col):
                r = 10 * ease(p)
                d.ellipse([x - r, y - r, x + r, y + r], fill=col)
            S.add(dot, 0.25, gap=0.05)
            S.text(x, y - 46, it.get("sub") or it.get("value", ""), fit(FT("value"), it.get("sub") or it.get("value", ""), 54, 500), col, dur=0.35)
    _note(S, card)


LAYOUT = {"line": l_line, "number_compare": l_number_compare, "flow": l_flow, "table": l_table, "bars": l_bars,
          "headline": l_headline, "text": l_text}


# ---------------------------------------------------------------- 공개 함수
def render_card(card: dict, out: Path, duration: float, seed: int = 1) -> None:
    S = Scene(seed)
    LAYOUT.get(card.get("type", "text"), l_text)(S, card)
    S.render(out, duration)


def render_paste(image_path: Path, out: Path, duration: float, caption: str = "", seed: int = 1) -> None:
    """기사 캡처·임시 화면을 종이 위 콜라주로."""
    S = Scene(seed)
    im = Image.open(image_path)
    # 사진+캡션이 하단 자막(아래 ~230px)을 침범하지 않도록
    S.photo(im, S.W / 2, S.H * 0.41, S.W * 0.70, S.H * 0.56,
            angle=S.rng.choice([-2.2, -1.4, 1.2, 2.0]) if PROFILE.get("tilt", True) else 0.0, caption=caption)
    S.render(out, duration)


def render_placeholder(out: Path, duration: float, note: str, seed: int = 1) -> None:
    S = Scene(seed)
    x0, y0, x1, y1 = 300, S.H * 0.28, S.W - 300, S.H * 0.64
    pts = rect_path(x0, y0, x1, y1, S.rng)
    dashed = [pts[i:i + 3] for i in range(0, len(pts) - 2, 4)]
    for seg in dashed:
        S.stroke(seg, (150, 140, 120), 3, 0.05, gap=0.012)
    S.text(S.W / 2, S.H * 0.40, "소스 필요", F(FT("note"), 70), S.red)
    S.text(S.W / 2, S.H * 0.52, note, fit(FT("note"), note, 44, x1 - x0 - 80), S.ink)
    S.render(out, duration)
