"""구겨진 종이 바탕 (설명 무대용, docs/51). 내려받지 않고 직접 만든다.

면(보로노이 조각마다 다른 기울기) + 접힌 선(무작위 직선의 꺾임) → 높이 → 왼쪽 위 빛으로 음영.
그 위에 종이 섬유·잔 얼룩·가장자리 어둡게. 같은 seed 는 같은 그림.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image


def _up(a: np.ndarray, W: int, H: int) -> np.ndarray:
    return np.asarray(Image.fromarray(a.astype(np.float32), mode="F").resize((W, H), Image.BICUBIC))


def _blur(a: np.ndarray, r: float) -> np.ndarray:
    """가우시안 흐림 (분리 합성곱, numpy 만)."""
    k = max(1, int(r * 3))
    x = np.arange(-k, k + 1, dtype=np.float32)
    g = np.exp(-x ** 2 / (2 * r * r))
    g /= g.sum()
    a = np.apply_along_axis(lambda v: np.convolve(np.pad(v, k, mode="edge"), g, "valid"), 1, a.astype(np.float32))
    return np.apply_along_axis(lambda v: np.convolve(np.pad(v, k, mode="edge"), g, "valid"), 0, a)


def _noise(rng, W, H, cell) -> np.ndarray:
    g = rng.standard_normal((max(2, H // cell + 2), max(2, W // cell + 2)))
    return _up(g, W, H)


def make(W: int = 1920, H: int = 1080, seed: int = 7, base: str = "#E8E3D9", strength: float = 1.0) -> Image.Image:
    rng = np.random.default_rng(seed)
    w, h = W // 4, H // 4
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    # 1) 접힌 선: 무작위 직선을 따라 꺾임 (|거리| → 능선·골). 연속이라 면 사이가 끊기지 않는다.
    fold = np.zeros_like(xx)
    for _ in range(34):
        a = rng.uniform(0, np.pi)
        cx, cy = rng.uniform(0, w), rng.uniform(0, h)
        dist = (xx - cx) * np.sin(a) - (yy - cy) * np.cos(a)
        reach = rng.uniform(30, 160)
        # 접힘은 선 근처에서만 (멀어질수록 평평): 부드럽게 포화
        fold += rng.uniform(-1, 1) * reach * np.tanh(np.abs(dist) / reach)
    # 2) 잔주름: 능선 잡음 (1-|잡음|)
    ridge = sum((1 - np.abs(_noise(rng, w, h, c))) * wgt for c, wgt in ((40, 6), (16, 3), (7, 1.2)))
    hgt = fold * 0.7 + ridge + _noise(rng, w, h, 60) * 10
    hgt = _up(hgt, W, H)
    # 3) 빛: 왼쪽 위에서
    dy, dx = np.gradient(hgt)
    nx, ny, nz = -dx, -dy, np.full_like(dx, 1.6)
    L = np.array([-0.55, -0.6, 0.58])
    shade = (nx * L[0] + ny * L[1] + nz * L[2]) / np.sqrt(nx ** 2 + ny ** 2 + nz ** 2)
    shade = np.tanh((shade - np.median(shade)) * 2.2) * 0.5 * strength
    # 4) 섬유·얼룩·가장자리
    fiber = (rng.standard_normal((H, W)).astype(np.float32) * 0.6 + _up(rng.standard_normal((H // 2, W // 2)), W, H) * 0.6) * 0.018
    streak = rng.standard_normal((H // 2, W // 8))
    streak = _up(streak, W, H) * 0.006
    blot = _noise(rng, W, H, 220) * 0.025 + _noise(rng, W, H, 60) * 0.012
    Y, X = np.mgrid[0:H, 0:W].astype(np.float32)
    vig = 1 - 0.16 * (((X - W / 2) / (W / 2)) ** 2 + ((Y - H / 2) / (H / 2)) ** 2) ** 1.4
    b = np.array([int(base[i:i + 2], 16) for i in (1, 3, 5)], np.float32) / 255
    lum = np.clip((1 + shade * 0.32 + fiber + streak + blot) * vig, 0, 1.2)
    img = np.clip(b[None, None] * lum[..., None] * 255, 0, 255)
    # 그림자 쪽은 약간 차갑게 (회색 종이 느낌)
    img[..., 2] += np.clip(-shade, 0, None) * 6
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))


def cached(cache_dir: Path, seed: int = 7, base: str = "#E8E3D9") -> Path:
    p = Path(cache_dir) / f"crumple_{seed}_{base.strip('#')}_v2.jpg"
    if not p.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
        make(seed=seed, base=base).save(p, quality=90)
    return p


# ---------------------------------------------------------------- 실사 종이 (ambientCG Paper003, CC0)
# 구겨진 실제 종이 사진(CC0 1.0, https://ambientcg.com/view?id=Paper003)을 처음 한 번 내려받아 캐시에 둔다.
# 저장소에는 그림을 넣지 않는다(미디어 커밋 금지). 받을 수 없으면 위의 직접 만든 종이로.
AMBIENT = "https://ambientcg.com/get?file=Paper003_2K-JPG.zip"


def _ambient(cache_dir: Path) -> Path | None:
    p = Path(cache_dir) / "ambientcg" / "Paper003_2K-JPG_Color.jpg"
    if p.exists():
        return p
    import io
    import urllib.request
    import zipfile
    try:
        req = urllib.request.Request(AMBIENT, headers={"User-Agent": "Mozilla/5.0 (ytflow)"})
        with urllib.request.urlopen(req, timeout=60) as r:
            z = zipfile.ZipFile(io.BytesIO(r.read()))
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(z.read("Paper003_2K-JPG_Color.jpg"))
        return p
    except Exception:  # noqa: BLE001
        return None


def make_photo(src: Path, W: int = 1920, H: int = 1080, seed: int = 7, base: str = "#E8E3D9",
               contrast: float = 1.0) -> Image.Image:
    im = Image.open(src).convert("L")
    s = im.size[0]
    rng = np.random.default_rng(seed)
    ch = int(s * H / W)
    y0 = int(rng.uniform(0, s - ch))
    im = im.crop((0, y0, s, y0 + ch)).resize((W, H), Image.LANCZOS)
    if seed % 2:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    g = np.asarray(im, np.float32) / 255
    g = (g - np.median(g)) / max(float(np.percentile(np.abs(g - np.median(g)), 99)), 1e-3)   # 주름만 남김 (-1..1)
    g = np.clip(g, -1.4, 1.2) * 0.085 * contrast
    Y, X = np.mgrid[0:H, 0:W].astype(np.float32)
    vig = 1 - 0.13 * (((X - W / 2) / (W / 2)) ** 2 + ((Y - H / 2) / (H / 2)) ** 2) ** 1.5
    grain = rng.standard_normal((H, W)).astype(np.float32) * 0.012 + _noise(rng, W, H, 240) * 0.02
    b = np.array([int(base[i:i + 2], 16) for i in (1, 3, 5)], np.float32)
    lum = (1 + g + grain) * vig
    img = b[None, None] * lum[..., None]
    img[..., 2] += np.clip(-g, 0, None) * 18   # 그늘은 살짝 차갑게
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))


def background(cache_dir: Path, seed: int = 7, base: str = "#E8E3D9") -> Path:
    """설명 무대 바탕: 실사 구겨진 종이(가능하면) → 아니면 직접 만든 종이."""
    src = _ambient(cache_dir)
    tag = "photo" if src else "proc"
    p = Path(cache_dir) / f"paper_{tag}_{seed}_{base.strip('#')}_v2.jpg"
    if not p.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
        (make_photo(src, seed=seed, base=base) if src else make(seed=seed, base=base)).save(p, quality=90)
    return p


def dark(cache_dir: Path, seed: int = 7, base: str = "#1B1D22") -> Path:
    """어두운 무대 바탕: 가운데가 조금 밝은 숯색 + 고운 결 (종이 대신, 설명 무대 theme=dark)."""
    p = Path(cache_dir) / f"dark_{seed}_{base.strip('#')}_v1.jpg"
    if p.exists():
        return p
    W, H = 1920, 1080
    rng = np.random.default_rng(seed)
    Y, X = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((X - W * 0.48) / (W * 0.62)) ** 2 + ((Y - H * 0.42) / (H * 0.7)) ** 2)
    glow = np.clip(1.45 - r, 0, 1) ** 1.6 * 0.55
    grain = rng.standard_normal((H, W)).astype(np.float32) * 0.035 + _noise(rng, W, H, 180) * 0.05
    b = np.array([int(base[i:i + 2], 16) for i in (1, 3, 5)], np.float32)
    img = b[None, None] * (1 + glow + grain)[..., None]
    p.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).save(p, quality=90)
    return p
