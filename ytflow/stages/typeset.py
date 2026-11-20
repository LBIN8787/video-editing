"""한 편 안의 글꼴 통일 — 브랜드(채널) 글꼴 체계 (2026-11-20 사용자: "영상 내 폰트같은걸 좀 통일해야 할 것 같아요 너무 음 화면 전환마다 제각각인거같아서").

문제: 장면마다 그래픽 팩(어두운 다큐·신문지 = 나눔명조 제목, 설명 무대 = 블랙한산스, 숫자 카드 = 나눔고딕, 주석 = 나눔펜)이
따로 글꼴을 정해 한 편에 다섯 계열이 섞였다 (11/20 개정판 측정: 명조 2종 · 고딕 2종 · 블랙한산스 · 펜).

해결: 브랜드 글꼴 체계를 장면 문서(HDoc)를 만든 뒤에 덮어씀 —
  ① 글자 폭을 재는 역할 글꼴(paper.PROFILE fonts: title·value·box·note·label)을 체계 글꼴로,
  ② 장면 HTML 의 글꼴 별칭(serif-x·serif-b·pen·sans·sans-x·heavy·gr·gx)을 모두 체계 글꼴 파일로 다시 연결.
그래서 어떤 장면 종류·그래픽 팩이든 같은 두 계열(제목·숫자 / 본문·라벨)로 그려진다. 자막(ASS)은 원래 나눔고딕.

체계 끄기: hybrid.json "type": "pack" (그래픽 팩 글꼴 그대로). 다른 체계: "type": "<이름>".
"""
from __future__ import annotations

import os
import shutil
from pathlib import Path

from . import paper

BHS = paper.FONT_DIR / "BlackHanSans-Regular.ttf"

# 역할 → 글꼴 파일 (제목·큰 숫자는 굵은 고딕 하나, 나머지는 나눔고딕 두 굵기)
SYSTEMS = {
    "gothic": {
        "roles": {"title": BHS, "value": BHS, "box": paper.SANS_X, "note": paper.SANS, "label": paper.SANS},
        # HTML 별칭 → 파일 (하드코딩된 별칭까지 같은 계열로)
        "alias": {"heavy": BHS, "serif-x": BHS, "serif-b": paper.SANS_X, "pen": paper.SANS,
                  "sans": paper.SANS, "sans-x": paper.SANS_X, "gr": paper.SANS, "gx": paper.SANS_X},
    },
}
BRAND_DEFAULT = {"market": "gothic"}   # 시장 채널 기본 (2026-11-20 사용자 요청). 다른 채널은 그래픽 팩 글꼴 그대로


def for_spec(spec: dict) -> dict | None:
    name = spec.get("type") or BRAND_DEFAULT.get(spec.get("brand", ""), "pack")
    return SYSTEMS.get(name)


def apply(D, assets: Path, ts: dict) -> None:
    """장면 문서 D 에 글꼴 체계를 씌움 (HDoc 를 만든 뒤, 장면을 그리기 전에)."""
    paper.PROFILE["fonts"].update(ts["roles"])
    fdir = assets / "fonts"
    fdir.mkdir(parents=True, exist_ok=True)
    faces = []
    for alias, f in ts["alias"].items():
        if not (fdir / f.name).exists():
            try:
                os.link(f, fdir / f.name)
            except OSError:
                shutil.copy(f, fdir / f.name)
        faces.append(f"@font-face{{font-family:{alias};src:url('assets/fonts/{f.name}')}}")
    D.css.append("".join(faces))   # 기본 글꼴 정의보다 뒤에 붙어 같은 이름을 덮어씀
    D.typeset = ts


def family(path) -> str | None:
    """hyper.Doc.text 가 글꼴 파일 → 별칭을 찾을 때, 체계 글꼴(블랙한산스)도 알아보게."""
    return "heavy" if Path(path) == BHS else None
