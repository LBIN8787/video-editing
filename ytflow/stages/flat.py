"""평면 인포그래픽 모션 스타일 (머니크루 화면 분석 기준, styles/moneycrew).

paper.py 의 애니메이션 엔진(요소별 시작·끝 시간, 그려지기·떠오르기·카운트업)을 그대로 쓰고
겉모습만 바꾼다: 무늬 없는 미색 단색 배경, 곧은 선, 굵은 고딕 숫자, 테이프·손글씨 없음.
자막은 화면 위쪽 어두운 글씨(edit.subtitle_position: top)로 media.subtitles 가 처리한다.
"""
from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path

from . import paper

FLAT_PROFILE = {"texture": False, "wobble": 0.0, "tape": False, "underline": False, "top": 130, "tilt": False,
                "mark": "box",
                "fonts": {"title": paper.SANS_X, "value": paper.SANS_X, "box": paper.SANS,
                          "note": paper.SANS, "label": paper.SANS}}


# 식스시그마(검은 배경 미니멀): 같은 엔진, 고딕 보통 굵기, 강조는 상자
DARK_PROFILE = dict(FLAT_PROFILE, top=130,
                    fonts={"title": paper.SANS, "value": paper.SANS, "box": paper.SANS,
                           "note": paper.SANS, "label": paper.FONT_DIR / "NanumGothic-Regular.ttf"})
PROFILES = {"flat": FLAT_PROFILE, "dark": DARK_PROFILE}
CURRENT = {"name": "flat"}


@contextmanager
def _flat():
    old = dict(paper.PROFILE)
    paper.PROFILE.clear()
    paper.PROFILE.update(PROFILES[CURRENT["name"]])
    try:
        yield
    finally:
        paper.PROFILE.clear()
        paper.PROFILE.update(old)


def render_card(card: dict, out: Path, duration: float, seed: int = 1) -> list:
    with _flat():
        return paper.render_card(card, out, duration, seed)


def render_paste(image_path: Path, out: Path, duration: float, caption: str = "", seed: int = 1) -> None:
    with _flat():
        paper.render_paste(image_path, out, duration, caption, seed)


def render_placeholder(out: Path, duration: float, note: str, seed: int = 1) -> None:
    with _flat():
        paper.render_placeholder(out, duration, note, seed)
