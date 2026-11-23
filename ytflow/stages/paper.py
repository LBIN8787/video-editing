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
    if Path(path) == PEN:  # 손글씨 폰트는 같은 크기에서 글자가 작아 보여 25% 키운다
        size = size * 1.25
    key = (path, int(size))
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(str(path), int(size))
    return _fonts[key]


def _rgb(h: str) -> tuple:
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


OVERRIDE: dict = {}   # 그래픽 스킨이 정한 바탕·글씨·강조색 (skin.paper_override) — edit.yaml 의 paper 보다 우선


def cfg() -> dict:
    e = config.load("pipeline").get("edit", {})
    p = {"base": "#EEE7DA", "ink": "#22304D", "red": "#C4452F", "anim_seconds": 1.2}
    p.update(e.get("paper") or {})
    p.update(OVERRIDE)
    # 카드는 항상 가로 캔버스에 그린다 (쇼츠는 세로 화면 안에 카드를 줄여 넣음): card_width/height 로 따로 지정 가능
    return {"W": e.get("card_width", e.get("width", 1920)), "H": e.get("card_height", e.get("height", 1080)),
            "fps": e.get("fps", 30), **p}


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
        bg = _rgb(c["base"])
        self.muted = tuple(int(b * 0.45 + i * 0.55) for b, i in zip(bg, self.ink))  # 보조 글자색: 배경과 잉크 사이
        self.rng = random.Random(seed)
        self.items: list = []
        self.t = 0.0  # 다음 요소의 기본 시작 시각
        # 배치 관리: 그린 요소가 차지한 사각형. 글자는 서로·도형과 겹치지 않게 옮기거나 줄인다.
        self.occupied: list = []
        self.issues: list = []
        self.safe_top, self.safe_bottom = 36, self.H - 170  # 아래 170px 은 자막 자리

    # --- 배치 관리
    @staticmethod
    def _hit(a, b, pad=6):
        return not (a[2] + pad <= b[0] or b[2] + pad <= a[0] or a[3] + pad <= b[1] or b[3] + pad <= a[1])

    def free(self, rect) -> bool:
        return rect[1] >= self.safe_top and rect[3] <= self.safe_bottom and \
            rect[0] >= 0 and rect[2] <= self.W and not any(self._hit(rect, o) for o in self.occupied)

    def place(self, x0, y0, w, h):
        """(x0,y0) 가 막혀 있으면 가까운 빈 자리를 위아래로 찾는다. 못 찾으면 None."""
        step = h * 0.6 + 6
        for k in [0, 1, -1, 2, -2, 3, -3, 4, -4, 5, -5]:
            yy = y0 + k * step
            if self.free((x0, yy, x0 + w, yy + h)):
                return x0, yy
        return None

    def reserve(self, rect):
        self.occupied.append(tuple(rect))

    def _layout_text(self, x, y, s, font, color, anchor):
        """글자 위치를 정한다: 겹치면 옮기고, 그래도 안 되면 85%씩 최대 3번 줄인다."""
        for _ in range(4):
            tile = _text_tile(s, font, color)
            w, h = tile.size
            x0 = x - {"l": 0, "m": w / 2, "r": w}[anchor[0]]
            y0 = y - {"t": 0, "m": h / 2, "b": h}[anchor[1]]
            x0 = min(max(x0, 8), self.W - w - 8)
            spot = self.place(x0, y0, w, h)
            if spot:
                self.reserve((spot[0], spot[1], spot[0] + w, spot[1] + h))
                return tile, spot
            path = getattr(font, "path", None)
            if not path or font.size < 22:
                break
            font = F(Path(path), int(font.size * 0.85))
        self.issues.append(f"겹침 해결 못 함: '{s[:20]}'")
        self.reserve((x0, y0, x0 + w, y0 + h))
        return tile, (x0, y0)

    def add(self, fn, dur=0.45, at=None, gap=0.12):
        t0 = self.t if at is None else at
        self.items.append((t0, t0 + dur, fn))
        self.t = t0 + gap
        return self

    # --- 기본 요소
    def text(self, x, y, s, font, color, anchor="mm", rise=18, dur=0.45, at=None, gap=0.12, plate=False):
        tile, (x0, y0) = self._layout_text(x, y, s, font, color, anchor)
        if plate:  # 차트 위 라벨: 배경색 판을 깔아 선·캔들 위에서도 읽히게
            bgc = _rgb(self.c["base"])
            pl = Image.new("RGBA", (tile.size[0] + 16, tile.size[1] + 8), bgc + (225,))
            pl.alpha_composite(tile, (8, 4))
            tile, x0, y0 = pl, x0 - 8, y0 - 4

        def draw(img, d, p):
            e = ease(p)
            im = tile if e >= 1 else _fade(tile, e)
            img.alpha_composite(im, (int(x0), int(y0 + (1 - e) * rise)))
        return self.add(draw, dur, at, gap)

    def counter(self, x, y, s, font, color, dur=0.9, at=None, gap=0.15):
        """'4.13%' '990억 달러' 처럼 숫자 하나가 든 값은 0부터 올라가게."""
        m = re.search(r"\d[\d,]*(?:\.\d+)?", s)
        if not m or len(re.findall(r"\d[\d,]*(?:\.\d+)?", s)) > 1:
            return self.text(x, y, s, font, color, dur=dur, at=at, gap=gap)
        num = float(m.group().replace(",", ""))
        dec = len(m.group().split(".")[1]) if "." in m.group() else 0
        comma = "," in m.group()
        final, (fx, fy) = self._layout_text(x, y, s, font, color, "mm")  # 최종 값 크기로 자리 확보
        cx, cy = fx + final.size[0] / 2, fy + final.size[1] / 2
        if final.size[1] < _text_tile(s, font, color).size[1]:  # 자리가 좁아 줄였으면 그 크기로
            font = F(Path(font.path), int(font.size * final.size[1] / _text_tile(s, font, color).size[1]))

        def draw(img, d, p):
            e = ease(p)
            v = num * e
            sv = f"{v:,.{dec}f}" if comma else f"{v:.{dec}f}"
            cur = s[:m.start()] + sv + s[m.end():]
            tile = _text_tile(cur, font, color)
            img.alpha_composite(_fade(tile, min(1, e * 3)), (int(cx - tile.size[0] / 2), int(cy - tile.size[1] / 2)))
        return self.add(draw, dur, at, gap)

    def stroke(self, pts, color, width=4, dur=0.5, at=None, gap=0.1):
        def draw(img, d, p):
            pp = partial(pts, ease(p))
            if len(pp) > 1:
                d.line(pp, fill=color, width=width, joint="curve")
        return self.add(draw, dur, at, gap)

    def box(self, x0, y0, x1, y1, color, width=4, dur=0.45, at=None, gap=0.1, fill=None, register=True):
        pts = rect_path(x0, y0, x1, y1, self.rng)
        if register:
            self.reserve((x0, y0, x1, y1))
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

    def icon(self, name, cx, cy, size, color, dur=0.4, at=None, gap=0.1):
        """선 아이콘이 살짝 커지며 나타난다 (Lucide)."""
        from .icons import icon as _icon
        im = _icon(name, int(size), tuple(color), 2.0 if PROFILE["texture"] else 2.4)
        if im is None:
            return self
        self.reserve((cx - size / 2, cy - size / 2, cx + size / 2, cy + size / 2))

        def draw(img, d, p):
            e = ease(p)
            sc = 0.7 + 0.3 * e
            sp = im if sc >= 0.999 else im.resize((max(1, int(size * sc)), max(1, int(size * sc))))
            img.alpha_composite(_fade(sp, e), (int(cx - sp.width / 2), int(cy - sp.height / 2)))
        return self.add(draw, dur, at, gap)

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
        self.reserve((cx - sprite.width / 2 + 30, cy - sprite.height / 2 + 30, cx + sprite.width / 2 - 30, cy + sprite.height / 2 - 30))

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
    while size > 20 and F(font_path, size).getlength(s) > maxw:  # (F 가 손글씨는 25% 키움)
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
        S.text(S.W / 2, y or S.H * 0.76, card["note"], fit(FT("note"), card["note"], 46, S.W - 400), S.red, dur=0.4)


def l_number_compare(S, card):
    _title(S, card)
    items = card.get("items", [])[:3]
    n = max(len(items), 1)
    has_icon = any(it.get("icon") for it in items)
    base = S.H * (0.50 if has_icon else 0.47)
    for i, it in enumerate(items):
        x = S.W * (i + 0.5) / n
        col = S.red if it.get("highlight") else S.ink
        if it.get("icon"):
            S.icon(it["icon"], x, S.H * 0.27, 96, col)
        if it.get("label"):
            S.text(x, base - S.H * 0.13, it["label"], fit(FT("label"), it["label"], 36, S.W / n - 80), S.muted)
        f = fit(FT("value"), it.get("value", ""), 140, S.W / n - 160)
        S.counter(x, base, it.get("value", ""), f, col)
        if it.get("highlight"):
            w = f.getlength(it.get("value", ""))
            S.underline(x - w / 2, x + w / 2, base + 80, S.red, dur=0.35)
        if it.get("sub"):
            S.text(x, base + S.H * 0.14, it["sub"], fit(FT("note"), it["sub"], 50, S.W / n - 120), S.ink)
    _note(S, card)


def l_flow(S, card):
    """단계·돈의 흐름. 상자 안 글자는 상자 자리 안에 두고, 화살표 설명은 화살표 위 빈 곳에."""
    items = card.get("items", [])[:6]
    if len(items) < 2:  # 상자 하나짜리 흐름도는 비어 보임 → 아이콘·문장 카드로
        it = items[0] if items else {}
        return l_text(S, {"title": card.get("title", ""), "icon": it.get("icon", ""),
                          "items": [{"label": " · ".join(x for x in (it.get("label", ""), it.get("sub", "")) if x)}]})
    _title(S, card)
    n = max(len(items), 1)
    bw = min(330, (S.W - 160) / n - 70)
    gap = (S.W - 160 - bw * n) / max(n - 1, 1)
    y = S.H * 0.48
    h = 170 if any(it.get("icon") for it in items) else 150
    rects = []
    for i, it in enumerate(items):
        x0 = 80 + i * (bw + gap)
        col = S.red if it.get("highlight") else S.ink
        S.box(x0, y - h / 2, x0 + bw, y + h / 2, col, 5 if it.get("highlight") else 4, fill=(246, 242, 233) if PROFILE["texture"] else _rgb(S.c["base"]), register=False)
        top = y - h / 2 + 18
        if it.get("icon"):
            S.icon(it["icon"], x0 + bw / 2, top + 26, 52, col)
            top += 60
        rects.append((x0, y - h / 2, x0 + bw, y + h / 2))
        # 상자 안 글자: 상자와는 겹쳐도 되므로 직접 그린다 (다른 요소와는 상자 경계로 구분)
        lab = it.get("label", "")
        f = fit(FT("box"), lab, 42, bw - 30)
        _inbox_text(S, x0 + bw / 2, top + 26, lab, f, col)
        if it.get("sub"):
            _inbox_text(S, x0 + bw / 2, top + 70, it["sub"], fit(FT("note"), it["sub"], 34, bw - 24), S.muted)
        if i < n - 1:
            ax0, ax1 = x0 + bw + 12, x0 + bw + gap - 12
            S.arrow(ax0, y, ax1, y, S.ink)
    for r in rects:
        S.reserve(r)
    for i, it in enumerate(items[:-1]):  # 화살표 설명: 화살표 바로 위 → 막히면 관리자가 위아래 빈 곳으로
        if it.get("value"):
            x0 = 80 + i * (bw + gap)
            ax0, ax1 = x0 + bw + 12, x0 + bw + gap - 12
            f = fit(FT("note"), it["value"], 36, max(gap - 16, 60))
            if f.size >= 28:   # 화살표 위에 들어가면 그 자리
                S.text((ax0 + ax1) / 2, y - 34, it["value"], f, S.red)
            else:              # 너무 길면 상자 줄 아래로 내려 넓게
                S.text((ax0 + ax1) / 2, y + h / 2 + 40, it["value"], fit(FT("note"), it["value"], 32, bw + gap - 20), S.red)
    _note(S, card)


def _inbox_text(S, cx, cy, s, font, color):
    tile = _text_tile(s, font, color)

    def draw(img, d, p):
        e = ease(p)
        img.alpha_composite(tile if e >= 1 else _fade(tile, e), (int(cx - tile.size[0] / 2), int(cy - tile.size[1] / 2)))
    S.add(draw, 0.4, gap=0.05)


def l_table(S, card):
    _title(S, card)
    items = card.get("items", [])[:6]
    top, bot = S.H * 0.27, S.H * 0.74
    rh = min(120, (bot - top) / max(len(items), 1))
    x0, x1, x2, x3 = 200, 560, 1060, S.W - 200
    if any(it.get("icon") for it in items):  # 아이콘 자리만큼 오른쪽으로
        x0, x1, x2 = 280, 620, 1100
    for i, it in enumerate(items):
        y = top + rh * (i + 0.5)
        col = S.red if it.get("highlight") else S.ink
        if it.get("icon"):
            S.icon(it["icon"], x0 - 50, y, 48, col, dur=0.3, gap=0.0)
        S.text(x0, y, it.get("label", ""), fit(FT("label"), it.get("label", ""), 38, x1 - x0 - 20), S.muted if not it.get("highlight") else col, "lm", gap=0.02)
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
                lx = x0 - (96 if items[i].get("icon") else 24)
                S.box(lx, y - rh * 0.45, x3 + 24, y + rh * 0.45, S.red, 4, dur=0.4)
            else:
                lx = x0 - (90 if items[i].get("icon") else 0)
                S.circle((lx + x3) / 2, y, (x3 - lx) / 2 + 30, rh * 0.55, S.red, dur=0.55)
    _note(S, card)


def numeric(v) -> bool:
    try:
        float(str(v).replace(",", ""))
        return True
    except ValueError:
        return False


def l_bars(S, card):
    items = card.get("items", [])[:8]
    if len(items) < 2:  # 막대 하나는 비교가 아니라 숫자 하나 → 큰 숫자 카드로
        return l_number_compare(S, card)
    if not all(numeric(it.get("value", "")) for it in items):
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
    y = S.H * 0.43
    if card.get("icon"):
        S.icon(card["icon"], S.W / 2, S.H * 0.26, 150, S.red if card.get("highlight") else S.ink)
        y = S.H * 0.50
    f = fit(FT("title"), t, 104, S.W - 300)
    S.text(S.W / 2, y, t, f, S.red if card.get("highlight") else S.ink, rise=26, dur=0.6)
    w = f.getlength(t)
    S.underline(S.W / 2 - w / 2, S.W / 2 + w / 2, y + 70, S.red, dur=0.45)
    for i, it in enumerate(card.get("items", [])[:3]):
        S.text(S.W / 2, y + S.H * 0.14 + i * 64, it.get("label", ""), fit(FT("note"), it.get("label", ""), 52, S.W - 300), S.ink)


def l_line(S, card):
    """꺾은선(수동 값). 모든 점에 값을 적고(8개 이하), y축 눈금에 가격을 쓴다. 왼쪽→오른쪽으로 그려진다."""
    items = card.get("items", [])
    if len(items) < 2 or not all(numeric(it.get("value", "")) for it in items):
        return l_table(S, card)
    _title(S, card)
    vals = [float(str(it["value"]).replace(",", "")) for it in items]
    unit = card.get("unit", "")
    _plot_series(S, [it.get("label", "") for it in items], vals, unit,
                 marks={i: (it.get("sub") or "") for i, it in enumerate(items) if it.get("highlight")},
                 label_all=len(vals) <= 8)
    _note(S, card)


def _fmt(v: float, unit: str = "") -> str:
    from .marketdata import fmt_price
    if unit in ("USD", "KRW"):
        return fmt_price(v, unit)
    txt = f"{v:,.0f}" if abs(v) >= 100 else f"{v:,.2f}".rstrip("0").rstrip(".")
    return txt + unit


def _plot_series(S, xlabels, vals, unit, marks=None, label_all=False, ohlc=None):
    """공통 차트: 눈금(가격) · 선 또는 캔들 · 값 라벨 · 최고/최저/마지막 표시."""
    marks = marks or {}
    x0, x1, y0, y1 = 170, S.W - 330, S.H * 0.70, S.H * 0.25
    lo = min(r["low"] for r in ohlc) if ohlc else min(vals)
    hi = max(r["high"] for r in ohlc) if ohlc else max(vals)
    pad = (hi - lo) * 0.08 or 1
    lo, hi = lo - pad, hi + pad
    Y = lambda v: y0 - (v - lo) / (hi - lo) * (y0 - y1)
    n = len(vals)
    X = lambda i: x0 + (x1 - x0) * (i / max(n - 1, 1)) if not ohlc else x0 + (x1 - x0) * (i + 0.5) / n
    bg = _rgb(S.c["base"])
    grid = tuple(int(b * 0.8 + i * 0.2) for b, i in zip(bg, S.ink))  # 배경과 잉크 사이 옅은 선
    for k in range(4):  # 가격 눈금
        v = lo + (hi - lo) * (k + 0.5) / 4
        yy = Y(v)
        S.stroke([(x0, yy), (x1, yy)], grid, 1, 0.2, gap=0.0)
        S.text(x1 + 20, yy, _fmt(v, unit), F(FT("label"), 28), (130, 130, 130), "lm", rise=0, dur=0.2, gap=0.0)
    S.reserve((x0, y1 - 10, x1, y0 + 10))  # 차트 영역: 다른 글자가 들어오지 않게 (값 라벨은 아래에서 따로)
    idx = sorted({0, n // 2, n - 1}) if not label_all else range(n)
    for i in idx:
        lab = xlabels[i] if i < len(xlabels) else ""
        if lab:
            S.text(X(i), y0 + 40, lab, fit(FT("label"), lab, 28, max((x1 - x0) / max(len(list(idx)), 1) - 10, 60)), (120, 120, 120), rise=0, dur=0.2, gap=0.0)
    up, down = S.red, (48, 110, 209)
    if ohlc:  # 캔들 (한국식: 오르면 빨강, 내리면 파랑)
        cw = max(2, (x1 - x0) / n * 0.6)

        def candles(img, d, p):
            m = int(n * ease(p))
            for i, r in enumerate(ohlc[:m]):
                c = up if r["close"] >= r["open"] else down
                x = X(i)
                d.line([x, Y(r["high"]), x, Y(r["low"])], fill=c, width=max(1, int(cw / 4)))
                d.rectangle([x - cw / 2, Y(max(r["open"], r["close"])), x + cw / 2, Y(min(r["open"], r["close"])) + 1], fill=c)
        S.add(candles, 1.4, gap=1.4)
    else:
        S.stroke([(X(i), Y(v)) for i, v in enumerate(vals)], S.ink, 5, min(1.6, 0.2 * n + 0.4), gap=min(1.6, 0.2 * n + 0.4))
    # 값 라벨: 표시할 점 = 지정 강조 + (전부 또는 최고·최저·마지막)
    hi_i = max(range(n), key=lambda i: (ohlc[i]["high"] if ohlc else vals[i]))
    lo_i = min(range(n), key=lambda i: (ohlc[i]["low"] if ohlc else vals[i]))
    show = dict(marks)
    if label_all:
        for i in range(n):
            show.setdefault(i, "")
    for i, tag in ((hi_i, "최고"), (lo_i, "최저"), (n - 1, "")):
        show.setdefault(i, tag)
    for i in sorted(show, key=lambda i: (i != n - 1, i)):
        v = ohlc[i]["high"] if (ohlc and i == hi_i and i != n - 1) else (ohlc[i]["low"] if (ohlc and i == lo_i and i != n - 1) else vals[i])
        txt = f"{show[i]} {_fmt(v, unit)}".strip() if show[i] in ("최고", "최저", "") else f"{_fmt(v, unit)} · {show[i]}"
        last = i == n - 1
        col = S.red if (last or i in marks) else S.ink
        x, y = X(i), Y(v)

        def dot(img, d, p, x=x, y=y, col=col):
            r = 9 * ease(p)
            d.ellipse([x - r, y - r, x + r, y + r], fill=col)
        S.add(dot, 0.2, gap=0.0)
        if last:  # 마지막 가격: 차트 오른쪽 위 빈 곳에 크게 (캔들·축과 겹치지 않게)
            S.text(x1, y1 - 34, txt, fit(FT("value"), txt, 46, x1 - x0 - 200), col, "rm", rise=8, dur=0.3, gap=0.08)
            continue
        f = F(FT("value"), 30)
        # 사건 라벨은 점 위쪽, 배경판을 깔고 → 겹치면 관리자가 옮김. 차트 영역 예약을 잠시 빼고 배치
        area = S.occupied.pop(S.occupied.index((x0, y1 - 10, x1, y0 + 10)))
        S.text(x, y - 36, txt, f, col, "mm", rise=8, dur=0.3, gap=0.08, plate=True)
        S.occupied.append(area)


def l_chart(S, card):
    """실제 시세 차트. assets 단계가 card['_series'] (marketdata.fetch 결과)를 넣어 준다.
    items 는 표시할 사건: label=날짜(YYYY-MM-DD), sub=설명 → 그 날짜에 점과 설명."""
    rows = card.get("_series") or []
    if len(rows) < 5:
        return l_line(S, card) if card.get("items") else l_text(S, card)
    _title(S, card)
    cur = card.get("_currency", "")
    dates = [r["date"] for r in rows]
    marks = {}
    for it in card.get("items", []):
        d = it.get("label", "")
        if d:
            i = min(range(len(dates)), key=lambda k: abs((_d(dates[k]) - _d(d)).days) if _d(d) else 9e9)
            marks[i] = it.get("sub") or it.get("value") or ""
    _plot_series(S, [x[2:].replace("-", ".") for x in dates], [r["close"] for r in rows], cur, marks=marks,
                 ohlc=rows if card.get("style", "candle") == "candle" and len(rows) <= 140 else None)
    src = f"자료: {card.get('_source', 'Yahoo Finance')} · {card.get('ticker', '')} · {dates[-1]} 기준"
    S.text(170, PROFILE.get("top", 130) + 72, src, F(FT("label"), 24), (140, 140, 140), "lm", rise=0, dur=0.2)  # 출처는 제목 아래 왼쪽
    _note(S, card, y=S.H * 0.805)


def _d(s):
    from datetime import date
    try:
        y, m, dd = (int(x) for x in s[:10].split("-"))
        return date(y, m, dd)
    except Exception:
        return None


def l_analogy(S, card):
    """비유 카드: 왼쪽 = 실제 숫자·개념, 오른쪽 = 일상의 비유, 가운데 '≈'.
    items[0] 실제, items[1] 비유 (label · value · sub · icon). 항목이 하나면 문장 카드로."""
    items = card.get("items", [])[:2]
    if len(items) < 2:
        return l_text(S, card)
    _title(S, card)
    xs = (S.W * 0.27, S.W * 0.73)
    for i, (x, it) in enumerate(zip(xs, items)):
        col = S.red if (it.get("highlight") or i == 1) else S.ink
        at = 0.25 + i * 0.9  # 실제 → (잠깐) → 비유 순서로 등장
        if it.get("icon"):
            S.icon(it["icon"], x, S.H * 0.32, 120, col, at=at)
        if it.get("label"):
            S.text(x, S.H * 0.46, it["label"], fit(FT("label"), it["label"], 40, S.W * 0.36), S.muted, at=at + 0.1)
        if it.get("value"):
            f = fit(FT("value"), it["value"], 104, S.W * 0.36)
            S.text(x, S.H * 0.57, it["value"], f, col, at=at + 0.2)
        if it.get("sub"):
            S.text(x, S.H * 0.68, it["sub"], fit(FT("note"), it["sub"], 44, S.W * 0.38), S.ink, at=at + 0.3)
    S.text(S.W / 2, S.H * 0.56, "≈", F(FT("value"), 130), S.red, at=1.0)
    _note(S, card, S.H * 0.79)


LAYOUT = {"chart": l_chart, "line": l_line, "number_compare": l_number_compare, "flow": l_flow, "table": l_table, "bars": l_bars,
          "headline": l_headline, "text": l_text, "analogy": l_analogy}


# ---------------------------------------------------------------- 공개 함수
def render_card(card: dict, out: Path, duration: float, seed: int = 1) -> list:
    """카드를 애니메이션으로 렌더링. 해결 못 한 겹침 목록을 돌려준다 (qa 보고서용)."""
    S = Scene(seed)
    LAYOUT.get(card.get("type", "text"), l_text)(S, card)
    S.render(out, duration)
    return S.issues


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
