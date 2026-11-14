"""이야기 그림판(story-board) 렌더러 — Pillow 벡터, 브라우저 없이.

`ytflow/stages/story.py`(이야기 그림판)는 HTML+GSAP → HyperFrames(node·chromium)로 그린다.
클라우드 컨테이너에는 node·chromium 이 없어 그 길이 막히므로, **같은 문법**(한 장의 큰 종이 위에
선이 그려지고 카메라가 이야기를 따라가는 그림판)을 Pillow 로 옮겨 그린다.

- 그림판 3840×2160 (화면의 2배). 카메라 [cx, cy, zoom] — zoom 1.0 = 화면 한 장(1920×1080).
- 모든 그림은 `02_script/board.json` 의 아이템. `word` 를 적으면 **그 낱말을 말하는 순간** 그려진다
  (03_voice/timings.json 의 단어 시각). `t` 를 적으면 그 초.
- 매 프레임: 종이(배경) 잘라 붙이기 → 아직 그리는 중인 아이템만 벡터로 얹기 → 2배 슈퍼샘플 → 다운스케일.
- 장면 길이 = 03_voice/durations.json + 0.12s(호흡).

쓰는 법
  python3 build/board.py                 # 모든 장면 → 04_assets/scene_XXX_anim.mp4
  python3 build/board.py --scene 5       # 한 장면만
  python3 build/board.py --still 5:2.4   # 5번 장면 2.4초 프레임을 PNG 로 (05_edit/stills/)
"""
from __future__ import annotations

import argparse
import json
import math
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[3]
PROJ = ROOT / "projects" / "20261114-curiosity-test"
FONTS = ROOT / "ytflow" / "assets" / "fonts"
VOICE = PROJ / "03_voice"
ASSETS = PROJ / "04_assets"
STILLS = PROJ / "05_edit" / "stills"

BW, BH = 3840, 2160        # 그림판
W, H = 1920, 1080          # 화면
SS = 2                     # 슈퍼샘플 (화면 대비 2배)
FPS = 30
GAP = 0.12

PAPER = dict(base="#F2EADC", ink="#22304D", red="#C4452F", blue="#2F5D8C", mark="#F3D36B",
             glass="#D9E4EC", cream="#FFFDF6", wood="#D8B383", mute="#7C879B", fog="#FFFFFF")
DARK = dict(base="#1C2537", ink="#F2E9D8", red="#EC8A6E", blue="#93BBD8", mark="#F3D36B",
            glass="#33445C", cream="#25314A", wood="#8E6C46", mute="#8C9AB4", fog="#B9CBDD")
SAND = dict(base="#EBDCC2", ink="#3A2F2A", red="#B8472F", blue="#3E6180", mark="#F0CE72",
            glass="#D7E1E6", cream="#FFFBF0", wood="#C79C68", mute="#8B7A66", fog="#FFFFFF")
PALETTES = dict(paper=PAPER, dark=DARK, sand=SAND)


# ------------------------------------------------------------------ 기본 도구
def hexrgb(c: str) -> tuple[int, int, int]:
    if isinstance(c, str) and not c.startswith("#"):     # 팔레트 이름('ink' 등)도 받아 준다
        return hexrgb(PAPER.get(c, "#22304D"))
    c = c.lstrip("#")
    if len(c) == 3:
        c = "".join(ch * 2 for ch in c)
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def rgba(c, a=255) -> tuple[int, int, int, int]:
    r, g, b = hexrgb(c) if isinstance(c, str) else c[:3]
    return (r, g, b, int(max(0, min(255, a))))


def shade(c: str, f: float, base: str = "#FFFFFF") -> str:
    """c 를 base 쪽으로 f 만큼 섞는다 (종이 위 그림자·반투명 대신 단색 혼합)."""
    a, b = np.array(hexrgb(c), float), np.array(hexrgb(base), float)
    v = np.clip(a * f + b * (1 - f), 0, 255).astype(int)
    return "#%02x%02x%02x" % tuple(v)


_FC: dict = {}


def font(kind: str, size: int) -> ImageFont.FreeTypeFont:
    size = max(6, int(size))
    key = (kind, size)
    if key not in _FC:
        name = {"sans": "NanumGothic-Regular.ttf", "sansb": "NanumGothic-Bold.ttf",
                "sansx": "NanumGothic-ExtraBold.ttf", "pen": "NanumPenScript-Regular.ttf",
                "serif": "NanumMyeongjo-Bold.ttf", "serifx": "NanumMyeongjo-ExtraBold.ttf"}[kind]
        _FC[key] = ImageFont.truetype(str(FONTS / name), size)
    return _FC[key]


def ease_out(p: float) -> float:
    p = max(0.0, min(1.0, p))
    return 1 - (1 - p) ** 3


def ease_io(p: float) -> float:
    p = max(0.0, min(1.0, p))
    return p * p * (3 - 2 * p)


def paper_bg(kind: str, seed: int) -> Image.Image:
    """그림판 종이 (3840×2160). 결·얼룩·아주 약한 비네트."""
    pal = PALETTES[kind]
    rng = np.random.default_rng(seed)
    base = np.array(hexrgb(pal["base"]), float)
    def norm(a):
        return (a - a.min()) / max(float(a.max() - a.min()), 1e-6) * 255
    small = norm(rng.normal(0, 2.2, (BH // 8, BW // 8)).astype(np.float32))
    small = np.array(Image.fromarray(small.astype(np.uint8)).resize((BW, BH), Image.BICUBIC), float)
    fibre = norm(rng.normal(0, 1.1, (BH, BW // 4)).astype(np.float32))
    fibre_img = np.array(Image.fromarray(fibre.astype(np.uint8)).resize((BW, BH), Image.BICUBIC), float)
    noise = (small - 127) * 0.10 + (fibre_img - 127) * 0.05
    img = np.clip(base[None, None, :] + noise[:, :, None], 0, 255).astype(np.uint8)
    im = Image.fromarray(img, "RGB")
    # 비네트
    yy, xx = np.mgrid[0:BH, 0:BW]
    r = np.sqrt(((xx - BW / 2) / (BW / 2)) ** 2 + ((yy - BH / 2) / (BH / 2)) ** 2)
    v = np.clip(1 - 0.10 * np.clip(r - 0.45, 0, None) ** 1.5, 0, 1)
    vimg = Image.fromarray((v * 255).astype(np.uint8), "L").filter(ImageFilter.GaussianBlur(60))
    black = Image.new("RGB", (BW, BH), hexrgb(shade(pal["base"], 0.80, "#000000")))
    return Image.composite(im, black, vimg)


class Cam:
    def __init__(self, cx, cy, z):
        self.z = z
        self.left = cx - (W / z) / 2
        self.top = cy - (H / z) / 2
        self.k = SS * z

    def pt(self, x, y):
        return ((x - self.left) * self.k, (y - self.top) * self.k)

    def ln(self, v):
        return max(1.0, v * self.k)


# ------------------------------------------------------------------ 벡터 도구
def polyline(d: ImageDraw.ImageDraw, cam: Cam, pts, color, width, prog=1.0, alpha=255, close=False, dash=None):
    if len(pts) < 2:
        return
    P = [cam.pt(x, y) for x, y in pts]
    if close:
        P = P + [P[0]]
    seg = [math.dist(P[i], P[i + 1]) for i in range(len(P) - 1)]
    total = sum(seg) or 1
    want = total * max(0.0, min(1.0, prog))
    w = cam.ln(width)
    col = rgba(color, alpha)
    acc = 0.0
    for i, L in enumerate(seg):
        if acc > want:
            break
        a, b = P[i], P[i + 1]
        f = min(1.0, (want - acc) / L) if L else 1.0
        bb = (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)
        if dash:
            d.line([a, bb], fill=col, width=int(max(1, w)))
        else:
            d.line([a, bb], fill=col, width=int(max(1, w)))
            if w > 3:  # 둥근 캡·이음
                r = w / 2
                for p in (a, bb):
                    d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=col)
        acc += L


def rrect_pts(x, y, w, h, r, n=6):
    r = min(r, w / 2, h / 2)
    pts = []
    for cx, cy, a0 in ((x + w - r, y + r, -90), (x + w - r, y + h - r, 0), (x + r, y + h - r, 90), (x + r, y + r, 180)):
        for i in range(n + 1):
            a = math.radians(a0 + 90 * i / n)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def rrect(d, cam, box, r, fill=None, outline=None, width=3, prog=1.0, alpha=255, dash=None):
    x0, y0, x1, y1 = box
    if fill is not None:
        d.rounded_rectangle([cam.pt(x0, y0), cam.pt(x1, y1)], radius=cam.ln(r), fill=rgba(fill, alpha))
    if outline is not None:
        polyline(d, cam, rrect_pts(x0, y0, x1 - x0, y1 - y0, r), outline, width, prog, alpha, close=True, dash=dash)


def ellipse(d, cam, cx, cy, rx, ry, fill=None, outline=None, width=3, alpha=255):
    box = [cam.pt(cx - rx, cy - ry), cam.pt(cx + rx, cy + ry)]
    if fill is not None:
        d.ellipse(box, fill=rgba(fill, alpha))
    if outline is not None:
        d.ellipse(box, outline=rgba(outline, alpha), width=int(max(1, cam.ln(width))))


def text_at(d, cam, x, y, s, fs, color, kind="sans", anchor="mm", alpha=255, rot=0.0, max_w=None):
    size = int(round(fs * cam.k))
    f = font(kind, size)
    col = rgba(color, alpha)
    if max_w:  # 폭에 맞춰 줄인다
        tw = d.textlength(s, font=f)
        if tw > cam.ln(max_w):
            size = max(8, int(size * cam.ln(max_w) / tw))
            f = font(kind, size)
    if not rot:
        d.text(cam.pt(x, y), s, font=f, fill=col, anchor=anchor)
        return
    tw = d.textlength(s, font=f)
    asc, desc = f.getmetrics()
    pad = 8
    im = Image.new("RGBA", (int(tw) + pad * 2, asc + desc + pad * 2), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((pad, pad), s, font=f, fill=col)
    im = im.rotate(rot, expand=True, resample=Image.BICUBIC)
    px, py = cam.pt(x, y)
    d._image.paste(im, (int(px - im.width / 2), int(py - im.height / 2)), im)


def arrow(d, cam, p0, p1, color, sw=8, bend=0.0, prog=1.0, alpha=255, head=True):
    """p0 → p1 손그림 화살표. bend 는 화살표를 휘게 한다(보드 px)."""
    (x0, y0), (x1, y1) = p0, p1
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy) or 1
    cx, cy = mx - dy / L * bend, my + dx / L * bend
    pts = [((1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t * t * x1,
            (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t * t * y1) for t in np.linspace(0, 1, 24)]
    polyline(d, cam, pts, color, sw, prog, alpha)
    if head and prog > 0.55:
        ax, ay = pts[-1]
        px, py = pts[-5]
        ang = math.atan2(ay - py, ax - px)
        hl, hw = sw * 4.6, sw * 2.1
        tri = [(ax, ay),
               (ax - hl * math.cos(ang) + hw * math.sin(ang), ay - hl * math.sin(ang) - hw * math.cos(ang)),
               (ax - hl * math.cos(ang) - hw * math.sin(ang), ay - hl * math.sin(ang) + hw * math.cos(ang))]
        d.polygon([cam.pt(*q) for q in tri], fill=rgba(color, alpha))


def cloud_shape(d, cam, cx, cy, w, h, fill, outline, sw=5, alpha=255, prog=1.0):
    """종이를 오려 붙인 구름: 원 세 개의 합집합. 테두리는 '조금 큰 원을 먼저 깔고 안을 채우는' 방식."""
    parts = [(-0.26, 0.06, 0.24), (-0.02, -0.10, 0.29), (0.24, 0.07, 0.22)]
    if outline:
        for dx, dy, r in parts:
            ellipse(d, cam, cx + dx * w, cy + dy * h, (r * w) * 1.10, (r * w) * 1.02, fill=outline, alpha=alpha)
    for dx, dy, r in parts:
        ellipse(d, cam, cx + dx * w, cy + dy * h, r * w, r * w * 0.92, fill=fill, alpha=alpha)


def shadow(d, cam, cx, cy, rx, ry, pal, alpha=60):
    col = shade(pal["base"], 0.72, "#000000") if pal is not DARK else shade(pal["base"], 1.6, "#FFFFFF")
    ellipse(d, cam, cx, cy, rx, ry, fill=col, alpha=alpha)


# ------------------------------------------------------------------ 아이템
def i_window(d, cam, it, p, pal):
    """기내에서 본 창: 둥근 사각 틀 + 하늘 + 종이 구름 + (옵션) 구멍."""
    x, y, w, h = it["x"], it["y"], it["w"], it["h"]
    r = it.get("r", 120)
    hole = it.get("hole")
    e = ease_out(p)
    shadow(d, cam, x + w / 2, y + h + 26, w * 0.44, 26, pal, int(55 * e) if pal is not DARK else 0)
    rrect(d, cam, (x, y, x + w, y + h), r, fill=pal["cream"], outline=None, width=6, alpha=int(255 * min(1, e * 2)))
    rrect(d, cam, (x, y, x + w, y + h), r, outline=pal["ink"], width=6, prog=e)
    rrect(d, cam, (x + w * 0.055, y + h * 0.06, x + w * 0.945, y + h * 0.94), r * 0.9,
          fill=pal["glass"], alpha=int(240 * min(1, e * 1.5)))
    rrect(d, cam, (x + w * 0.055, y + h * 0.06, x + w * 0.945, y + h * 0.94), r * 0.9,
          outline=pal["ink"], width=4, prog=max(0.0, e * 1.4 - 0.4))
    if it.get("clouds", True):
        cw = w * 0.40
        cloud_shape(d, cam, x + w * 0.34, y + h * 0.62, cw, cw * 0.6, pal["fog"], pal["mute"], 4,
                    alpha=int(150 * ease_out(p)), prog=ease_out(p))
        cloud_shape(d, cam, x + w * 0.68, y + h * 0.34, cw * 0.72, cw * 0.5, pal["fog"], pal["mute"], 4,
                    alpha=int(120 * ease_out(p)), prog=ease_out(p))
    if hole:
        ell_hole(d, cam, hole, it.get("hole_r", 20), pal, 1.0)


def ell_hole(d, cam, xy, r, pal, alpha=255):
    ellipse(d, cam, xy[0], xy[1], r, r, fill=shade(pal["glass"], 0.55, "#000000"), alpha=alpha)
    ellipse(d, cam, xy[0], xy[1], r, r, outline=pal["ink"], width=3, alpha=alpha)


def i_hole(d, cam, it, p, pal):
    r = it.get("r", 22)
    e = ease_out(p)
    ellipse(d, cam, it["x"], it["y"], r * (0.4 + 0.9 * e), r * (0.4 + 0.9 * e),
            fill=shade(pal["glass"], 0.45, "#000000"), alpha=int(255 * e))
    ellipse(d, cam, it["x"], it["y"], r * (0.4 + 0.9 * e), r * (0.4 + 0.9 * e),
            outline=pal["red"], width=4, alpha=int(255 * e))


def i_circle(d, cam, it, p, pal):
    cx, cy, rx, ry = it["x"], it["y"], it.get("rx", 70), it.get("ry", 70)
    col = pal[it.get("color", "red")]
    pts = [(cx + rx * math.cos(a), cy + ry * math.sin(a) * (1 + 0.05 * math.sin(a * 3)))
           for a in np.linspace(-0.4, 2 * math.pi - 0.2, 60)]
    polyline(d, cam, pts, col, it.get("sw", 7), ease_out(p))


def i_cross(d, cam, it, p, pal):
    s, w = it.get("s", 60), it.get("sw", 10)
    e = ease_out(p)
    polyline(d, cam, [(it["x"] - s, it["y"] - s), (it["x"] + s, it["y"] + s)], pal["red"], w, e)
    polyline(d, cam, [(it["x"] + s, it["y"] - s), (it["x"] - s, it["y"] + s)], pal["red"], w, e)


def i_check(d, cam, it, p, pal):
    s, w = it.get("s", 55), it.get("sw", 10)
    col = pal[it.get("color", "ok")] if it.get("color", "ok") in pal else "#2E7D4F"
    polyline(d, cam, [(it["x"] - s * 0.9, it["y"] + s * 0.1), (it["x"] - s * 0.15, it["y"] + s * 0.8),
                      (it["x"] + s, it["y"] - s * 0.8)], col, w, ease_out(p))


def i_arrow(d, cam, it, p, pal):
    col = pal[it.get("color", "red")]
    arrow(d, cam, tuple(it["from"]), tuple(it["to"]), col, it.get("sw", 9),
          it.get("bend", 0.0), ease_out(p))


def i_dash(d, cam, it, p, pal):
    col = pal[it.get("color", "mute")]
    polyline(d, cam, [tuple(it["from"]), tuple(it["to"])], col, it.get("sw", 4), ease_out(p), 170)


def i_note(d, cam, it, p, pal):
    col = pal[it.get("color", "ink")]
    e = ease_out(p)
    text_at(d, cam, it["x"], it["y"] - (1 - e) * 16, it["text"], it.get("fs", 58), col,
            it.get("font", "pen"), it.get("anchor", "mm"), int(255 * min(1, e * 1.4)), it.get("rot", 0))


def i_chip(d, cam, it, p, pal):
    """종이 쪽지 + (옵션) 형광펜."""
    fs = it.get("fs", 54)
    e = ease_out(p)
    tmp = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    tw = cam.ln(len(it["text"]) * fs * 0.52)
    w, h = tw + cam.ln(60), cam.ln(fs * 1.9)
    cx, cy = cam.pt(it["x"], it["y"] - (1 - e) * 14)
    box = [cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2]
    d.rounded_rectangle([box[0] + w * 0.02, box[1] + h * 0.10, box[2] + w * 0.02, box[3] + h * 0.10],
                        radius=w * 0.06, fill=rgba(shade(pal["base"], 0.8, "#000000"), int(50 * e)))
    d.rounded_rectangle(box, radius=w * 0.06, fill=rgba(pal["cream"], int(250 * e)),
                        outline=rgba(pal["ink"], int(120 * e)), width=max(1, int(cam.ln(2))))
    if it.get("hl"):
        d.rounded_rectangle([box[0] + w * 0.04, box[1] + h * 0.58, box[2] - w * 0.04, box[1] + h * 0.92],
                            radius=w * 0.02, fill=rgba(pal["mark"], int(150 * e)))
    text_at(d, cam, it["x"], it["y"] - (1 - e) * 14, it["text"], fs, pal[it.get("color", "ink")], "sansb",
            "mm", int(255 * e))


def i_stamp(d, cam, it, p, pal):
    fs = it.get("fs", 58)
    e = ease_out(p)
    rot = it.get("rot", -7)
    size = int(fs * cam.k)
    f = font(it.get("font", "sansx"), size)
    tmp = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    tw = tmp.textlength(it["text"], font=f)
    pad = int(size * 0.42)
    im = Image.new("RGBA", (int(tw) + pad * 2, size + pad * 2), (0, 0, 0, 0))
    dd = ImageDraw.Draw(im)
    col = rgba(pal["red"], int(235 * e))
    dd.rounded_rectangle([2, 2, im.width - 3, im.height - 3], radius=size * 0.18, outline=col, width=max(2, int(size * 0.07)))
    dd.rounded_rectangle([int(size * 0.13), int(size * 0.13), im.width - int(size * 0.13) - 1, im.height - int(size * 0.13) - 1],
                         radius=size * 0.12, outline=col, width=max(1, int(size * 0.03)))
    dd.text((im.width / 2, im.height / 2), it["text"], font=f, fill=col, anchor="mm")
    im = im.rotate(rot, expand=True, resample=Image.BICUBIC)
    px, py = cam.pt(it["x"], it["y"])
    if e > 0.02:
        d._image.paste(im, (int(px - im.width / 2), int(py - im.height / 2)), im)


def i_big(d, cam, it, p, pal):
    e = ease_out(p)
    text_at(d, cam, it["x"], it["y"] - (1 - e) * 24, it["text"], it.get("fs", 260), pal[it.get("color", "ink")],
            it.get("font", "serifx"), "mm", int(255 * min(1, e * 1.3)))


def i_figure(d, cam, it, p, pal):
    """사람 — 막대 인물이 아니라 몸통(면)·팔·다리가 있는 평면 벡터. 얼굴 표정은 그리지 않는다."""
    x, y = it["x"], it["y"]
    s = it.get("s", 1.0)
    pose = it.get("pose", "stand")
    body = it.get("color") or ("#4C6E80" if pal is not DARK else "#8FA9BC")
    leg = shade(body, 0.78, pal["ink"])
    skin = "#F4D8BE"
    ink = pal["ink"]
    e = ease_out(p)
    a = int(255 * min(1, e * 1.5))
    y = y - (1 - e) * 22 * s
    shadow(d, cam, x + 40 * s, it["y"] + 4, 130 * s, 15 * s, pal, int(45 * e))
    sitting = pose in ("sit", "sit_point", "bench")
    if sitting:
        if it.get("seat", True):     # 의자
            rrect(d, cam, (x - 34 * s, y - 132 * s, x + 122 * s, y - 104 * s), 10, fill=pal["wood"],
                  outline=ink, width=3, alpha=a)
            for lx in (x - 22 * s, x + 106 * s):
                rrect(d, cam, (lx, y - 104 * s, lx + 14 * s, y), 5, fill=shade(pal["wood"], 0.85, ink),
                      outline=ink, width=2, alpha=a)
        hip = (x, y - 116 * s)
        knee = (x + 96 * s, y - 112 * s)
        ankle = (x + 92 * s, y - 12 * s)
        polyline(d, cam, [hip, knee], leg, 42 * s, 1, a)
        polyline(d, cam, [knee, ankle], leg, 32 * s, 1, a)
        ellipse(d, cam, ankle[0] + 10 * s, ankle[1], 26 * s, 11 * s, fill=ink, alpha=a)
        tors = [(x - 30 * s, y - 246 * s), (x + 28 * s, y - 236 * s), (x + 24 * s, y - 112 * s), (x - 26 * s, y - 116 * s)]
        sh = (x + 12 * s, y - 232 * s)
        if pose == "sit_point":
            arm = [(sh, (x + 76 * s, y - 214 * s)), ((x + 76 * s, y - 214 * s), (x + 140 * s, y - 200 * s))]
        else:
            arm = [(sh, (x + 34 * s, y - 150 * s)), ((x + 34 * s, y - 150 * s), (x + 52 * s, y - 118 * s))]
    elif pose == "run":
        hip = (x, y - 150 * s)
        polyline(d, cam, [hip, (x - 64 * s, y - 56 * s)], leg, 34 * s, 1, a)
        polyline(d, cam, [(x - 64 * s, y - 56 * s), (x - 76 * s, y - 8 * s)], leg, 28 * s, 1, a)
        polyline(d, cam, [hip, (x + 72 * s, y - 70 * s)], leg, 34 * s, 1, a)
        polyline(d, cam, [(x + 72 * s, y - 70 * s), (x + 62 * s, y - 6 * s)], leg, 28 * s, 1, a)
        tors = [(x - 28 * s, y - 280 * s), (x + 26 * s, y - 272 * s), (x + 22 * s, y - 146 * s), (x - 24 * s, y - 150 * s)]
        arm = [((x + 8 * s, y - 262 * s), (x - 66 * s, y - 214 * s)),
               ((x + 8 * s, y - 262 * s), (x + 70 * s, y - 276 * s))]
    else:
        hip = (x, y - 148 * s)
        polyline(d, cam, [hip, (x - 24 * s, y - 8 * s)], leg, 36 * s, 1, a)
        polyline(d, cam, [hip, (x + 28 * s, y - 8 * s)], leg, 36 * s, 1, a)
        tors = [(x - 30 * s, y - 286 * s), (x + 26 * s, y - 278 * s), (x + 22 * s, y - 144 * s), (x - 26 * s, y - 148 * s)]
        arm = [((x + 8 * s, y - 268 * s), (x + 56 * s, y - 186 * s))]
    d.polygon([cam.pt(px, py) for px, py in tors], fill=rgba(body, a), outline=rgba(ink, a),
              width=int(max(1, cam.ln(3))))
    for (a0, a1) in arm:
        polyline(d, cam, [a0, a1], body, 24 * s, 1, a)
        ellipse(d, cam, a1[0], a1[1], 14 * s, 14 * s, fill=skin, alpha=a)
    hc = (x + 2 * s, y - 322 * s) if not sitting else (x + 2 * s, y - 282 * s)
    polyline(d, cam, [(hc[0], hc[1] + 34 * s), (hc[0], hc[1] + 52 * s)], skin, 20 * s, 1, a)
    ellipse(d, cam, hc[0], hc[1], 33 * s, 35 * s, fill=skin, outline=ink, width=3, alpha=a)
    d.chord([cam.pt(hc[0] - 34 * s, hc[1] - 38 * s), cam.pt(hc[0] + 34 * s, hc[1] + 4 * s)],
            178, 362, fill=rgba(ink, a))
    if it.get("jersey"):
        text_at(d, cam, x + 2 * s, (y - 200 * s) if sitting else (y - 220 * s), it["jersey"], 34 * s,
                pal["cream"], "sansb", "mm", a)
    if it.get("tag"):
        text_at(d, cam, x + 4 * s, it["y"] + 56 * s, it["tag"], 48, pal["ink"], "pen", "mm", a)


def i_plane(d, cam, it, p, pal):
    x, y, s = it["x"], it["y"], it.get("s", 1.0)
    e = ease_out(p)
    a = int(245 * min(1, e * 1.5))
    dy = (1 - e) * -26
    body = pal["cream"] if pal is not DARK else shade(pal["cream"], 1.25, "#FFFFFF")
    ink = pal["ink"] if pal is not DARK else pal["mute"]
    y += dy

    def P(pts):
        return [cam.pt(px, py) for px, py in pts]

    # 날개 (아래로 뻗은 뒷날개)
    wing = [(x + 26 * s, y + 10 * s), (x - 70 * s, y + 150 * s), (x - 8 * s, y + 150 * s), (x + 78 * s, y + 14 * s)]
    d.polygon(P(wing), fill=rgba(shade(body, 0.86, ink), a), outline=rgba(ink, a), width=int(max(1, cam.ln(3))))
    # 꼬리 날개
    fin = [(x - 118 * s, y - 6 * s), (x - 172 * s, y - 92 * s), (x - 136 * s, y - 96 * s), (x - 96 * s, y - 8 * s)]
    d.polygon(P(fin), fill=rgba(body, a), outline=rgba(ink, a), width=int(max(1, cam.ln(3))))
    hstab = [(x - 150 * s, y + 4 * s), (x - 214 * s, y + 34 * s), (x - 150 * s, y + 32 * s)]
    d.polygon(P(hstab), fill=rgba(body, a), outline=rgba(ink, a), width=int(max(1, cam.ln(2))))
    # 동체
    d.rounded_rectangle([cam.pt(x - 170 * s, y - 30 * s), cam.pt(x + 150 * s, y + 30 * s)],
                        radius=cam.ln(30 * s), fill=rgba(body, a), outline=rgba(ink, a),
                        width=int(max(1, cam.ln(4))))
    # 기수
    d.polygon(P([(x + 128 * s, y - 28 * s), (x + 182 * s, y - 2 * s), (x + 128 * s, y + 28 * s)]),
              fill=rgba(body, a), outline=rgba(ink, a), width=int(max(1, cam.ln(3))))
    # 엔진 · 창문
    rrect(d, cam, (x - 60 * s, y + 26 * s, x + 10 * s, y + 58 * s), 14 * s, fill=shade(body, 0.8, ink),
          outline=ink, width=2, alpha=a)
    for k in range(5):
        ellipse(d, cam, x + (60 + 14 * k) * s, y - 6 * s, 4.5 * s, 4.5 * s, fill=ink, alpha=a)


def i_section(d, cam, it, p, pal):
    """옆에서 본 창 단면 — 종이 카드 안에 담는다(돋보기처럼): 하늘 · 세 겹 · 기내."""
    cx = it.get("cx", 1900)
    y0, y1 = it.get("y0", 620), it.get("y1", 1500)
    H_ = y1 - y0
    thick = it.get("thick", 34)
    gap = it.get("gap", 185)
    thin = max(10, thick * 0.5)
    side = it.get("side", 800)
    total = thick * 2 + thin + gap * 2
    x_out = cx - total / 2
    xs = [x_out, x_out + thick + gap, x_out + thick + gap + thick + gap]
    show = it.get("show", 3)
    e = ease_out(p)
    a = int(255 * min(1, e * 1.6))
    hole_xy = (xs[1] + thick / 2, y1 - 88)
    # 카드 (그림판 위에 붙인 종이)
    cx0, cy0 = x_out - side, y0 - 150
    cx1, cy1 = xs[2] + thin + side, y1 + 190
    shadow(d, cam, (cx0 + cx1) / 2 + 16, cy1 + 22, (cx1 - cx0) / 2, 26, pal, int(50 * e))
    rrect(d, cam, (cx0, cy0, cx1, cy1), 26, fill=pal["cream"], outline=None, alpha=int(250 * e))
    # 하늘 · 기내
    d.rectangle([cam.pt(cx0 + 8, y0 - 110), cam.pt(x_out, y1 + 150)], fill=rgba(pal["glass"], int(215 * e)))
    d.rectangle([cam.pt(xs[2] + thin, y0 - 110), cam.pt(cx1 - 8, y1 + 150)],
                fill=rgba(shade(pal["cream"], 0.93, pal["base"]), int(215 * e)))
    cloud_shape(d, cam, x_out - side * 0.52, y0 + H_ * 0.22, 420, 260, pal["fog"], pal["mute"], 4,
                alpha=int(160 * e), prog=e)
    if show >= 3 and it.get("cabin_figure", True):
        i_figure(d, cam, {"x": xs[2] + thin + side * 0.58, "y": y1 + 60, "s": 0.62, "pose": "sit", "seat": False},
                 p, pal)
    # 창틀 (위·아래)
    for yy in (y0 - 40, y1 + 12):
        rrect(d, cam, (x_out - 26, yy, xs[2] + thin + 26, yy + 34), 12, fill=pal["wood"], outline=pal["ink"],
              width=3, alpha=a)
    # 세 겹
    for i, xx in enumerate(xs):
        th = thin if i == 2 else thick
        if i >= show:
            continue
        fill = shade(pal["glass"], 0.97 if i == 1 else 1.0, pal["cream"])
        rrect(d, cam, (xx, y0, xx + th, y1), 10, fill=fill, outline=None, alpha=a)
        for k in range(10):     # 유리 결
            yy = y0 + 40 + k * (H_ - 80) / 9
            polyline(d, cam, [(xx + 6, yy), (xx + th - 6, yy + 10)], pal["mute"], 2, 1.0, int(55 * e))
        rrect(d, cam, (xx, y0, xx + th, y1), 10, outline=pal["ink"], width=4, prog=1.0, alpha=a)
    if it.get("hole", True) and show >= 2:
        ell_hole(d, cam, hole_xy, it.get("hole_r", 15), pal, e)
    if it.get("gap_fill"):
        q = ease_out(p)
        for xx in (xs[0] + thick, xs[1] + thick):
            d.rectangle([cam.pt(xx, y0), cam.pt(xx + gap, y1)], fill=rgba(pal["mark"], int(95 * q)))
    if it.get("flow"):
        f = ease_out(p)
        arrow(d, cam, (xs[2] + thin + 330, hole_xy[1] - 10), (xs[0] + thick + gap * 0.30, hole_xy[1] - 10),
              pal["blue"], 8, -46, f)
        arrow(d, cam, (xs[0] + thick + gap * 0.42, hole_xy[1] - 40),
              (xs[0] + thick + gap * 0.42, y0 + H_ * 0.40), pal["blue"], 8, -52, max(0.0, f * 1.5 - 0.5))
    if it.get("pressure"):
        f = ease_out(p)
        for k, fy in enumerate((0.22, 0.47, 0.72)):
            yy = y0 + H_ * fy
            arrow(d, cam, (xs[0] + thick + gap * 0.80, yy), (xs[0] + thick + 16, yy), pal["red"], 9, 0,
                  max(0.0, f - k * 0.15))
    if it.get("labels", True):
        la = int(255 * e)
        for xx, th, nm in ((xs[0], thick, "바깥 창"), (xs[1], thick, "가운데 창"), (xs[2], thin, "안쪽 창")):
            if xs.index(xx) >= show:
                continue
            polyline(d, cam, [(xx + th / 2, y1 + 54), (xx + th / 2, y1 + 108)], pal["mute"], 3, 1.0, la)
            text_at(d, cam, xx + th / 2, y1 + 146, nm, 48, pal["ink"], "pen", "mm", la, -3)
        text_at(d, cam, cx0 + 150, cy0 + 62, "하늘", 48, pal["mute"], "pen", "lm", la)
        text_at(d, cam, cx1 - 150, cy0 + 62, "기내", 48, pal["mute"], "pen", "rm", la)
    # 카드 테두리 (맨 위)
    rrect(d, cam, (cx0, cy0, cx1, cy1), 26, outline=pal["ink"], width=5, prog=e)
    return hole_xy, xs


def i_bars(d, cam, it, p, pal):
    """기압 막대 두 개 (밖 0.23 · 기내 0.75)."""
    x, base, hmax = it["x"], it["y"], it.get("hmax", 760)
    items = it["items"]
    e = ease_out(p)
    shadow(d, cam, x + 320, base + 18, 330, 18, pal, 45)
    for k, (lbl, v, col) in enumerate(items):
        bx = x + k * 300
        hh = hmax * v / max(i[1] for i in items) * e
        w = 170
        rrect(d, cam, (bx, base - hh, bx + w, base), 10, fill=pal[col], outline=pal["ink"], width=4)
        text_at(d, cam, bx + w / 2, base + 76, lbl, 52, pal["ink"], "sansb", "mm", int(255 * e))
        text_at(d, cam, bx + w / 2, base - hh - 58, it.get("vals", ["", ""])[k], 64, pal["ink"], "serifx", "mm",
                int(255 * min(1, e * 1.5)))
    polyline(d, cam, [(x - 30, base + 8), (x + 590, base + 8)], pal["ink"] if pal is not DARK else pal["ink"], 4, e, 140)


def i_bench(d, cam, it, p, pal):
    x, y, w = it["x"], it["y"], it.get("w", 820)
    e = ease_out(p)
    shadow(d, cam, x + w / 2, y + 92, w * 0.5, 16, pal, 45)
    for k in range(2):
        yy = y + k * 44
        rrect(d, cam, (x, yy, x + w, yy + 32), 8, fill=pal["wood"], outline=pal["ink"], width=4)
    for lx in (x + 46, x + w - 66):
        rrect(d, cam, (lx, y + 66, lx + 20, y + 156), 6, fill=pal["wood"], outline=pal["ink"], width=3, alpha=255)
    polyline(d, cam, [(x + 46, y + 150), (x + w - 46, y + 150)], pal["ink"], 6, e, 170)


def i_doc(d, cam, it, p, pal):
    """규정 문서 한 장: 머리글 · 회색 글줄 · 형광펜 문구 · 도장."""
    x, y, w, h = it["x"], it["y"], it["w"], it["h"]
    e = ease_out(p)
    shadow(d, cam, x + w / 2 + 18, y + h / 2 + 22, w * 0.52, h * 0.52, pal, 50)
    rrect(d, cam, (x, y, x + w, y + h), 14, fill=pal["cream"], outline=shade(pal["ink"], 0.3, pal["cream"]), width=4)
    # 머리글
    polyline(d, cam, [(x + w * 0.08, y + h * 0.14), (x + w * 0.92, y + h * 0.14)], pal["ink"], 3, e, 120)
    text_at(d, cam, x + w * 0.08, y + h * 0.075, it.get("head", "AC 25.775-1"), it.get("head_fs", 46),
            pal["ink"], "sansx", "lm", int(255 * e))
    text_at(d, cam, x + w * 0.08, y + h * 0.185, it.get("sub", "Windows and Windshields · FAA · 2003. 1. 17"),
            it.get("sub_fs", 30), pal["mute"], "sans", "lm", int(255 * e))
    # 회색 글줄
    for k in range(it.get("lines", 7)):
        yy = y + h * (0.27 + 0.045 * k)
        ww = w * (0.84 if k % 3 else 0.62)
        polyline(d, cam, [(x + w * 0.08, yy), (x + w * 0.08 + ww, yy)], pal["mute"], 7, e, 55)
    # 형광펜 문구
    for k, q in enumerate(it.get("quotes", [])):
        qy = y + h * (0.62 + 0.10 * k)
        fw = w * 0.84
        if k == 0:
            d.rounded_rectangle([cam.pt(x + w * 0.06, qy - 38), cam.pt(x + w * 0.06 + fw, qy + 18)],
                                radius=cam.ln(6), fill=rgba(pal["mark"], int(140 * e)))
        text_at(d, cam, x + w * 0.08, qy, q, it.get("quote_fs", 34), pal["ink"], "sansb", "lm", int(255 * e), max_w=w * 0.82)
        gl = (it.get("glosses") or [])
        if k < len(gl):
            text_at(d, cam, x + w * 0.08, qy + 34, gl[k], it.get("gloss_fs", 26), pal["mute"], "sans", "lm",
                    int(235 * e), max_w=w * 0.82)
        polyline(d, cam, [(x + w * 0.06, qy + 62), (x + w * 0.06 + fw, qy + 62)], pal["ink"], 2, e, 80)


def i_fog(d, cam, it, p, pal):
    """김 서림: 유리 전체가 뿌옇게 덮이고 물방울이 맺힌다."""
    x, y, w, h = it["x"], it["y"], it["w"], it["h"]
    e = ease_out(p)
    d.rounded_rectangle([cam.pt(x + w * 0.055, y + h * 0.06), cam.pt(x + w * 0.945, y + h * 0.94)],
                        radius=cam.ln(90), fill=rgba(pal["fog"], int(105 * e)))
    for k, (dx, dy, rr) in enumerate(((0.26, 0.30, 0.045), (0.64, 0.22, 0.035), (0.40, 0.48, 0.052),
                                      (0.72, 0.56, 0.040), (0.30, 0.68, 0.038), (0.56, 0.74, 0.030),
                                      (0.46, 0.34, 0.028), (0.80, 0.38, 0.026))):
        ellipse(d, cam, x + w * dx, y + h * dy, w * rr, w * rr, fill=shade(pal["fog"], 0.80, pal["mute"]),
                alpha=int(120 * e))
    for k, dx in enumerate((0.18, 0.34, 0.52, 0.70, 0.84)):
        polyline(d, cam, [(x + w * dx, y + h * (0.16 + 0.03 * k)), (x + w * (dx + 0.01), y + h * (0.44 + 0.05 * k))],
                 shade(pal["fog"], 0.72, pal["mute"]), 2.5, 1.0, int(90 * e))


def i_crack(d, cam, it, p, pal):
    x, y, s = it["x"], it["y"], it.get("s", 1.0)
    e = ease_out(p)
    branches = [[(0, 0), (-20, 60), (6, 120), (-14, 190)],
                [(0, 0), (50, 40), (110, 30), (170, 56)],
                [(0, 0), (-60, 30), (-110, 90)],
                [(0, 0), (20, -60), (-6, -120)]]
    for b in branches:
        polyline(d, cam, [(x + dx * s, y + dy * s) for dx, dy in b], pal["red"] if False else pal["ink"], 4, e, 220)


def i_wall(d, cam, it, p, pal):
    """벽: 벽돌 줄이 그어진 두 덩어리 + 문설주 (지름길 비유)."""
    x, y0, y1 = it["x"], it["y0"], it["y1"]
    w = it.get("w", 96)
    g0, g1 = it.get("gap", (1150, 1330))
    e = ease_out(p)
    for a, b in ((y0, g0), (g1, y1)):
        rrect(d, cam, (x - w / 2, a, x + w / 2, b), 8, fill=pal["cream"], outline=None, alpha=int(240 * e))
        rrect(d, cam, (x - w / 2, a, x + w / 2, b), 8, outline=pal["ink"], width=4, prog=e)
        k = 0
        yy = a + 34
        while yy < b - 18:
            polyline(d, cam, [(x - w / 2 + 5, yy), (x + w / 2 - 5, yy)], pal["mute"], 2, e, 150)
            xx = x - w / 2 + (0 if k % 2 else 24)
            while xx < x + w / 2 - 6:
                polyline(d, cam, [(xx, yy - 30), (xx, yy)], pal["mute"], 2, e, 110)
                xx += 48
            yy += 32
            k += 1
    for yy in (g0, g1):
        rrect(d, cam, (x - w / 2 - 16, yy - 14, x + w / 2 + 16, yy + 14), 4, fill=pal["wood"],
              outline=pal["ink"], width=3, alpha=int(250 * e))


def i_path(d, cam, it, p, pal):
    col = pal[it.get("color", "ink")]
    polyline(d, cam, [tuple(q) for q in it["pts"]], col, it.get("sw", 8), ease_out(p), it.get("alpha", 255))


def i_credit(d, cam, it, p, pal):
    text_at(d, cam, it["x"], it["y"], it["text"], it.get("fs", 30), pal["mute"], "sans", it.get("anchor", "lm"),
            int(190 * ease_out(p)))


KIND = dict(window=i_window, hole=i_hole, circle=i_circle, cross=i_cross, check=i_check, arrow=i_arrow,
            dash=i_dash, note=i_note, chip=i_chip, stamp=i_stamp, big=i_big, figure=i_figure, plane=i_plane,
            section=i_section, path=i_path, wall=i_wall, bars=i_bars, bench=i_bench, doc=i_doc, fog=i_fog, crack=i_crack, credit=i_credit)


# ------------------------------------------------------------------ 장면 문법
def cam_at(keys, t):
    if not keys:
        return Cam(BW / 2, BH / 2, 0.5)
    if t <= keys[0][0]:
        return Cam(keys[0][1], keys[0][2], keys[0][3])
    for i in range(len(keys) - 1):
        t0, x0, y0, z0 = keys[i]
        t1, x1, y1, z1 = keys[i + 1]
        if t0 <= t <= t1:
            f = ease_io((t - t0) / max(t1 - t0, 1e-6))
            return Cam(x0 + (x1 - x0) * f, y0 + (y1 - y0) * f, z0 + (z1 - z0) * f)
    k = keys[-1]
    return Cam(k[1], k[2], k[3])


def item_time(it, timing, last_idx):
    """`word` → 말한 시각(초). 대본 글자 표(timings.json)에서 그 낱말의 첫 위치를 찾는다."""
    if "t" in it:
        return float(it["t"]), last_idx
    w = it.get("word")
    if not w:
        return 0.0, last_idx
    nar = re.sub(r"\s+", "", timing["narration"])
    idx = nar.find(re.sub(r"\s+", "", w), last_idx)
    if idx < 0:
        idx = nar.find(re.sub(r"\s+", "", w))
    if idx < 0:
        return 0.0, last_idx
    ct = timing["chars"]
    t = 0.0
    for i, s in ct:
        if i >= idx:
            t = s
            break
    else:
        t = ct[-1][1] if ct else 0.0
    return max(0.0, t - it.get("lead", 0.06)), max(last_idx, idx)


def render_scene(sc, timing, bg_cache, out_path: Path, voice_dur: float, still_at: float | None = None):
    bg = bg_cache[sc.get("bg", "paper")]
    pal = PALETTES[sc.get("bg", "paper")]
    total = voice_dur + GAP
    # 아이템 시각
    last = 0
    items = []
    for it in sc.get("items", []):
        t, last = item_time(it, timing, last)
        items.append((t, it))
    n = max(1, int(round(total * FPS)))
    frames = [still_at] if still_at is not None else [i / FPS for i in range(n)]
    for ti, t in enumerate(frames):
        cam = cam_at(sc.get("cam", []), t)
        crop = bg.crop(tuple(int(v) for v in (cam.left, cam.top, cam.left + W / cam.z, cam.top + H / cam.z)))
        frame = crop.resize((W, H), Image.LANCZOS).convert("RGBA")
        art = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
        d = ImageDraw.Draw(art, "RGBA")
        d._image = art
        for t0, it in items:
            if t < t0:
                continue
            prog = 1.0
            dur = float(it.get("dur", 0.6))
            if dur > 0:
                prog = min(1.0, (t - t0) / dur)
            KIND[it["kind"]](d, cam, it, prog, pal)
        art_small = art.resize((W, H), Image.LANCZOS)
        frame.alpha_composite(art_small)
        if sc.get("fade", 0) and t < sc["fade"]:   # 장면 첫머리: 검은 화면에서 밝아짐
            k = ease_out(t / sc["fade"])
            frame = Image.blend(Image.new("RGBA", (W, H), (12, 14, 20, 255)), frame, 0.25 + 0.75 * k)
        rgb = frame.convert("RGB")
        if still_at is not None:
            STILLS.mkdir(parents=True, exist_ok=True)
            p = STILLS / f"scene_{sc['id']:03d}_{still_at:05.2f}s.png"
            rgb.save(p)
            print(f"[board] still → {p}")
            return p
        if ti == 0:
            proc = subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                                     "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                                     "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                                     "-r", str(FPS), str(out_path)], stdin=subprocess.PIPE)
        proc.stdin.write(rgb.tobytes())
    proc.stdin.close()
    proc.wait()
    print(f"[board] #{sc['id']} {total:.2f}s → {out_path.name}")
    return out_path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scene", type=int, default=0)
    ap.add_argument("--still", type=str, default="")
    a = ap.parse_args()
    board = json.loads((PROJ / "02_script" / "board.json").read_text(encoding="utf-8"))
    timings = json.loads((VOICE / "timings.json").read_text(encoding="utf-8"))
    durs = json.loads((VOICE / "durations.json").read_text(encoding="utf-8"))
    bg_cache = {k: paper_bg(k, 7 + i) for i, k in enumerate(("paper", "dark", "sand"))}
    ASSETS.mkdir(parents=True, exist_ok=True)
    if a.still:
        sid, tt = a.still.split(":")
        sc = next(s for s in board["scenes"] if s["id"] == int(sid))
        render_scene(sc, timings[sid], bg_cache, ASSETS / "x.mp4", durs[sid], still_at=float(tt))
        return
    todo = [s for s in board["scenes"] if not a.scene or s["id"] == a.scene]
    for sc in todo:
        sid = str(sc["id"])
        render_scene(sc, timings[sid], bg_cache, ASSETS / f"scene_{sc['id']:03d}_anim.mp4", durs[sid])
    print(f"[board] 장면 {len(todo)}개 완료 · 말소리 {sum(durs.values()):.1f}s")


if __name__ == "__main__":
    main()
