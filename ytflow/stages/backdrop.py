"""장면 배경(바탕) — 상황에 맞춰 바꿔 쓴다 (manual v8, 사용자 기각: '배경색이 한 가지라 단조롭다').

그래픽 팩(skin)은 색과 질감을 정하고, 이 모듈은 **장면의 목적**에 맞는 바탕을 그 팩의 색으로 만든다.
    film   팩 기본 바탕 (필름 알갱이·가장자리 어둡게)
    grid   숫자·차트·연표 — 옅은 모눈 + 차가운 기운 ("재는 중")
    spot   인용·발언 — 가운데 조명 + 가장자리 어둠 ("한 사람의 말에 집중")
    tint   비유·정리·질문 — 장(chapter)마다 다른 색 기운의 그라데이션 ("지금 몇 장인지 색으로")
    photo  오프닝·끝·키네틱 — 자료 사진을 흐리고 어둡게 깐 바탕 ("이 이야기의 장소")
대본 장면에 "bg": "<종류>" (photo 는 "bg_src": 자료 키) 로 직접 고를 수 있고, 없으면 auto() 가 type 으로 고른다.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

KINDS = ("film", "grid", "spot", "tint", "photo")
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


def make(sk: dict, kind: str, W: int, H: int, chapter: int = 0, photo: Path | None = None) -> Image.Image:
    from . import skin as skm
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
        k = 0.5 if dark else 0.55
        arr = arr * k + base * (1 - k) * (1.0 if dark else 0.9)
        arr *= (1 - 0.45 * r2 / 2)[..., None]
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
