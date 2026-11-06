"""선 아이콘 (Lucide, MIT 라이선스: ytflow/assets/icons/LICENSE-lucide.txt).

카드 항목의 icon 필드에 이름을 쓰면 렌더러가 그린다. 쓸 수 있는 이름: names().
"""
from __future__ import annotations

import io
from functools import lru_cache
from pathlib import Path

from PIL import Image

ICON_DIR = Path(__file__).resolve().parent.parent / "assets" / "icons"


def names() -> list[str]:
    return sorted(p.stem for p in ICON_DIR.glob("*.svg"))


@lru_cache(maxsize=512)
def icon(name: str, size: int, color: tuple, stroke: float = 2.0) -> Image.Image | None:
    f = ICON_DIR / f"{name}.svg"
    if not name or not f.exists():
        return None
    import cairosvg
    svg = f.read_text(encoding="utf-8").replace("currentColor", "#%02x%02x%02x" % tuple(color[:3]))
    svg = svg.replace('stroke-width="2"', f'stroke-width="{stroke}"')
    png = cairosvg.svg2png(bytestring=svg.encode(), output_width=size, output_height=size)
    return Image.open(io.BytesIO(png)).convert("RGBA")
