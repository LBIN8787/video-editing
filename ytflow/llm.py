"""Claude 호출 래퍼. 긴 출력은 스트리밍, JSON 은 Pydantic 구조화 출력."""
from __future__ import annotations

from typing import Type, TypeVar

import anthropic
from pydantic import BaseModel

from . import config

T = TypeVar("T", bound=BaseModel)

_client: anthropic.Anthropic | None = None


def _cfg() -> dict:
    return config.load("pipeline").get("llm", {})


def client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic()  # ANTHROPIC_API_KEY 또는 `ant auth login` 프로필
    return _client


def _common() -> dict:
    cfg = _cfg()
    kw: dict = {
        "model": cfg.get("model", "claude-opus-5-5"),
        "thinking": {"type": "adaptive"},
        "output_config": {"effort": cfg.get("effort", "high")},
    }
    if cfg.get("fallbacks", True):
        # 안전 분류기가 거절하면 서버가 카테고리에 맞는 대체 모델로 재실행
        kw["extra_headers"] = {"anthropic-beta": "server-side-fallback-2026-07-01"}
        kw["extra_body"] = {"fallbacks": "default"}
    return kw


def _check(msg) -> None:
    if msg.stop_reason == "refusal":
        detail = getattr(msg, "stop_details", None)
        raise RuntimeError(f"모델이 요청을 거절했습니다: {detail}")
    if msg.stop_reason == "max_tokens":
        raise RuntimeError("출력이 max_tokens 에서 잘렸습니다. 입력을 줄이거나 단계를 나눠 주세요.")


def text(system: str, user: str, max_tokens: int = 64000) -> str:
    """긴 마크다운 출력(대본 등). 스트리밍으로 받아 타임아웃을 피한다."""
    with client().messages.stream(
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
        **_common(),
    ) as stream:
        msg = stream.get_final_message()
    _check(msg)
    return "".join(b.text for b in msg.content if b.type == "text").strip()


def structured(system: str, user: str, schema: Type[T], max_tokens: int = 16000) -> T:
    """스키마로 검증된 JSON 출력."""
    resp = client().messages.parse(
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
        output_format=schema,
        **_common(),
    )
    _check(resp)
    return resp.parsed_output
