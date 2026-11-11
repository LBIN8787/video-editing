"""장면 배경(바탕) — 상황에 맞춰 바꿔 쓴다 (manual v8, 사용자 기각: '배경색이 한 가지라 단조롭다').

그래픽 팩(skin)은 색과 질감을 정하고, 이 모듈은 **장면의 목적**에 맞는 바탕을 그 팩의 색으로 만든다.
    film   팩 기본 바탕 (필름 알갱이·가장자리 어둡게)
    grid   숫자·차트·연표 — 옅은 모눈 + 차가운 기운 ("재는 중")
    spot   인용·발언 — 가운데 조명 + 가장자리 어둠 ("한 사람의 말에 집중")
    tint   비유·정리·질문 — 장(chapter)마다 다른 색 기운의 그라데이션 ("지금 몇 장인지 색으로")
    photo  오프닝·끝·키네틱 — 자료 사진을 흐리고 어둡게 깐 바탕 ("이 이야기의 장소")
  v15 카테고리 개성 (docs/21, ytflow/stages/identity.py):
    duotone 자료 사진을 카테고리의 두 색으로 물들임 ("바로 그 장소", 덜 흐리게)
    cork    코르크 증거판 (시사: 누가 누구와 연결돼 있나)
    chalk   칠판 (호기심: 원리를 배운다)
    dash    짙은 남색 + 옅은 모눈·연결점 (시장: 숫자를 지켜본다)
    glow    짙은 바탕 + 정지한 은은한 빛 두세 개 (AI: 제품 발표 무대)
대본 장면에 "bg": "<종류>" (photo 는 "bg_src": 자료 키) 로 직접 고를 수 있고, 없으면 auto() 가 type 으로 고른다.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

KINDS = ("film", "grid", "spot", "tint", "photo", "duotone", "cork", "chalk", "dash", "glow")
BY_TYPE = {
    "grid": {"bars", "chart", "versus", "timeline", "choropleth", "people", "compare_values", "proportion", "usmap"},
    "spot": {"quote", "statement", "bignum"},
    "tint": {"analogy", "checklist", "card_type", "map_causal", "explain", "lower"},
    "photo": {"intro", "outro", "kinetic"},
}
# 장마다 바뀌는 색 기운 (팩의 바탕에 섞는 양은 어두운 팩 22%, 밝은 팩 10%)
HUES = ["#2E5B8A", "#2F7A6B", "#8A3B3B", "#6B5B2E", "#5B3F86", "#2E6E8A"]


def auto(sc: dict, has_photo: bool = True) -> str:
    if sc.get("bg"):
        return sc["bg"]
    t = sc.get("type", "")
    for k, ts in BY_TYPE.items():
        if t in ts:
            return "spot" if k == "photo" and not has_photo else k
    return "film"


def _rgb(c: str) -> np.ndarray:
    c = c.lstrip("#")
    return np.array([int(c[i:i + 2], 16) for i in (0, 2, 4)], np.float32)


def _dark(base) -> bool:
    return float(base.sum()) < 300


def _noise(rng, H, W, scale: float) -> np.ndarray:
    """부드러운 얼룩 (작은 난수 판을 키워서 흐림) 0~1."""
    h, w = max(2, int(H / scale)), max(2, int(W / scale))
    small = Image.fromarray((rng.random((h, w)) * 255).astype(np.uint8))
    big = small.resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(scale / 3))
    return np.asarray(big, np.float32) / 255


def make_identity(kind: str, W: int, H: int, chapter: int = 0, photo: Path | None = None, duo=None) -> Image.Image:
    """v15 카테고리 바탕. 움직이지 않는 그림 한 장 (v12 '차분하게')."""
    rng = np.random.default_rng(31 + chapter)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r2 = ((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2
    if kind == "duotone" and photo and photo.exists():
        dk, lt = (_rgb(c) for c in (duo or ("#15171D", "#C9A66B")))
        im = Image.open(photo).convert("L")
        s = max(W / im.width, H / im.height)
        im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1))
        im = im.crop(((im.width - W) // 2, (im.height - H) // 2, (im.width - W) // 2 + W, (im.height - H) // 2 + H))
        g = np.asarray(im.filter(ImageFilter.GaussianBlur(2.5)), np.float32) / 255
        g = np.clip((g - 0.04) / 0.85, 0, 1) ** 0.9                     # 대비 살짝
        g = g * 0.78                                                     # 가장 밝은 곳도 강조색의 78% (글자가 보이게)
        arr = dk * (1 - g[..., None]) + lt * g[..., None]
        arr *= (1 - 0.55 * np.clip(r2, 0, 2) / 2)[..., None]             # 가장자리 어둡게
        arr *= (1 - 0.30 * np.exp(-r2 * 2.2))[..., None]                 # 가운데(글자 자리)도 살짝 눌러 줌
        noise = 3
    elif kind == "cork":
        base = _rgb("#7A5A3A")
        n1, n2 = _noise(rng, H, W, 60), _noise(rng, H, W, 9)
        arr = base[None, None, :] * (0.82 + 0.22 * n1[..., None] + 0.12 * n2[..., None])
        sp = rng.random((H, W))
        arr[sp > 0.985] *= 0.55                                          # 코르크 알갱이(어두운 점)
        arr[sp < 0.008] = arr[sp < 0.008] * 0.6 + np.array([222, 190, 140], np.float32) * 0.4
        arr *= (1 - 0.35 * np.clip(r2, 0, 2) / 2)[..., None]
        fr = 26                                                          # 나무 틀
        wood = _rgb("#3E2A1A") * (0.85 + 0.25 * _noise(rng, H, W, 14))[..., None]
        m = (xx < fr) | (xx > W - fr) | (yy < fr) | (yy > H - fr)
        arr[m] = wood[m]
        noise = 3
    elif kind == "chalk":
        base = _rgb("#25332C")
        smudge = _noise(rng, H, W, 140)                                  # 지우개 자국
        swirl = _noise(rng, H, W, 40)
        arr = base[None, None, :] + (np.array([200, 210, 200], np.float32) * (0.035 * smudge + 0.02 * swirl)[..., None])
        arr *= (1 - 0.30 * np.clip(r2, 0, 2) / 2)[..., None]
        fr = 22
        wood = _rgb("#6B4A2B") * (0.8 + 0.3 * _noise(rng, H, W, 12))[..., None]
        m = (xx < fr) | (xx > W - fr) | (yy < fr) | (yy > H - fr)
        arr[m] = wood[m]
        noise = 5
    elif kind == "dash":
        base = _rgb("#0C1626")
        arr = np.ones((H, W, 3), np.float32) * base
        arr *= (1 - 0.40 * np.clip(r2, 0, 2) / 2)[..., None]
        for step, w in ((60, 0.05), (240, 0.10)):
            m = ((xx % step) < 1.2) | ((yy % step) < 1.2)
            arr[m] = arr[m] * (1 - w) + np.array([120, 160, 210], np.float32) * w
        img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
        from PIL import ImageDraw
        d = ImageDraw.Draw(img, "RGBA")
        pts = [(float(rng.uniform(80, W - 80)), float(rng.uniform(80, H - 80))) for _ in range(26)]
        for i, (x, y) in enumerate(pts):                                 # 옅은 연결선 (가까운 점끼리)
            for (x2, y2) in pts[i + 1:]:
                if (x - x2) ** 2 + (y - y2) ** 2 < 330 ** 2:
                    d.line([(x, y), (x2, y2)], fill=(110, 160, 220, 26), width=1)
        for x, y in pts:
            d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(140, 190, 240, 60))
        arr = np.asarray(img, np.float32)
        noise = 2
    else:  # glow
        dk = _rgb((duo or ("#0A1220", "#2DD4BF"))[0])
        lt = _rgb((duo or ("#0A1220", "#2DD4BF"))[1])
        arr = np.ones((H, W, 3), np.float32) * dk
        for (cx, cy, rad, col, a) in ((W * 0.22, H * 0.25, 620, lt, 0.22), (W * 0.82, H * 0.78, 700, _rgb("#5B3FD6"), 0.18),
                                      (W * 0.70, H * 0.15, 420, lt, 0.08)):
            f = np.exp(-(((xx - cx) ** 2 + (yy - cy) ** 2) / (rad ** 2)))[..., None]
            arr = arr * (1 - a * f) + col * a * f
        arr *= (1 - 0.30 * np.clip(r2, 0, 2) / 2)[..., None]
        noise = 2
    arr += rng.normal(0, noise, (H, W, 1))
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.4))


def make(sk: dict, kind: str, W: int, H: int, chapter: int = 0, photo: Path | None = None, duo=None) -> Image.Image:
    from . import skin as skm
    if kind in ("duotone", "cork", "chalk", "dash", "glow"):
        if kind == "duotone" and not (photo and photo.exists()):
            kind = "glow"
        return make_identity(kind, W, H, chapter, photo, duo)
    if kind == "film" or kind not in KINDS:
        return skm.background(sk, W, H)
    pal = sk["palette"]
    base = _rgb(pal["base"])
    dark = _dark(base)
    rng = np.random.default_rng(11 + chapter)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r2 = ((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2
    if kind == "photo" and photo and photo.exists():
        im = Image.open(photo).convert("RGB")
        s = max(W / im.width, H / im.height)
        im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1))
        im = im.crop(((im.width - W) // 2, (im.height - H) // 2, (im.width - W) // 2 + W, (im.height - H) // 2 + H))
        im = im.filter(ImageFilter.GaussianBlur(14))
        arr = np.asarray(im, np.float32)
        if dark:   # 어두운 팩: 사진을 어둡게 깔아 밝은 글자가 보이게
            arr = arr * 0.4 + base * 0.6
            arr *= (1 - 0.45 * r2 / 2)[..., None]
        else:      # 밝은 팩: 사진을 회색조로 바꿔 아주 옅게(밝은 바탕 쪽으로) 깔아 어두운 글자가 보이게 (야경 사진도 밝은 바탕이 되도록)
            g = arr.mean(axis=2, keepdims=True)
            lift = 255 - (255 - g) * 0.35          # 어두운 사진도 밝게 들어 올림
            arr = lift * 0.25 + base * 0.75
            arr *= (1 - 0.12 * r2 / 2)[..., None]
    elif kind == "spot":
        light = base + (np.array([255, 236, 200], np.float32) - base) * (0.10 if dark else 0.25)
        t = np.clip(r2 / 1.6, 0, 1)[..., None]
        arr = light * (1 - t) + base * (0.55 if dark else 0.92) * t
    elif kind == "tint":
        hue = _rgb(HUES[chapter % len(HUES)])
        mix = 0.22 if dark else 0.10
        t = (xx / W * 0.6 + yy / H * 0.4)[..., None]
        arr = base * (1 - mix * (1 - t)) + hue * mix * (1 - t)
        arr *= (1 - 0.3 * r2 / 2)[..., None]
    else:  # grid
        cool = base + (np.array([60, 90, 120], np.float32) - base) * (0.10 if dark else 0.05)
        arr = np.ones((H, W, 3), np.float32) * cool
        arr *= (1 - 0.35 * r2 / 2)[..., None]
        line = (base + (255 - base) * 0.07) if dark else base * 0.92
        for step, w in ((48, 0.5), (240, 1.0)):
            m = ((xx % step) < 1.2) | ((yy % step) < 1.2)
            arr[m] = arr[m] * (1 - w * 0.6) + line * (w * 0.6)
    arr += rng.normal(0, 4 if dark else 2.5, (H, W, 1))
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.4))


def photo_still(project, spec: dict, src: str | None) -> Path | None:
    """자료 화면 키 → 정지 사진 (raw jpg 가 있으면 그것, 없으면 영상 첫 장면)."""
    fo = spec.get("footage") or {}
    if not fo:
        return None
    src = src if src in fo else next(iter(fo))
    fdir = project.dir("assets") / "footage"
    raw = fdir / "raw" / f"{src}.jpg"
    if raw.exists():
        return raw
    out = fdir / f"_still_{src}.jpg"
    if not out.exists():
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "1", "-i", str(fdir / fo[src]["file"]), "-frames:v", "1", str(out)], check=False)
    return out if out.exists() else None


def plan(spec: dict) -> list[str]:
    has = bool(spec.get("footage"))
    return [auto(s, has) for s in spec.get("scenes", [])]
