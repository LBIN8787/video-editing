"""Claude 호출 래퍼.

backend (config/pipeline.yaml → llm.backend):
  api         Anthropic API (ANTHROPIC_API_KEY 필요, 사용량만큼 과금)
  claude-cli  로컬 Claude Code CLI(`claude -p`)를 호출. Pro/Max 구독 로그인으로 동작하며
              API 키가 필요 없다. 구독 사용량 한도를 함께 쓴다.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
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


# ---------------------------------------------------------------- claude-cli 백엔드
def _cli(system: str, user: str, schema: dict | None = None, tools: list[str] | None = None) -> dict:
    exe = shutil.which("claude")
    if not exe:
        raise SystemExit("claude CLI 가 없습니다. `npm install -g @anthropic-ai/claude-code` 후 `claude` 로 로그인하세요.")
    cfg = _cfg()
    cmd = [exe, "-p", "--output-format", "json", "--system-prompt", system,
           "--tools", ",".join(tools or []), "--no-session-persistence", "--model", cfg.get("cli_model", "opus")]
    if tools:  # 비대화 실행이므로 지정한 도구(웹 검색 등)만 미리 허용
        cmd += ["--allowedTools", ",".join(tools)]
    if schema is not None:
        cmd += ["--json-schema", json.dumps(schema, ensure_ascii=False)]
    proc = subprocess.run(cmd, input=user, capture_output=True, text=True, timeout=cfg.get("cli_timeout", 1800))
    try:
        out = json.loads(proc.stdout)
    except json.JSONDecodeError:
        raise RuntimeError(f"claude CLI 출력 해석 실패 (exit {proc.returncode}): {proc.stderr[-1500:] or proc.stdout[-1500:]}")
    if out.get("is_error"):
        raise RuntimeError(f"claude CLI 오류: {out.get('result') or out}")
    return out


def _json_from(out: dict):
    if out.get("structured_output") is not None:
        return out["structured_output"]
    raw = out.get("result", "")
    m = re.search(r"```(?:json)?\s*(.*?)```", raw, re.S)
    return json.loads(m.group(1) if m else raw)


def _backend() -> str:
    return _cfg().get("backend", "api")


# ---------------------------------------------------------------- 공용 진입점
def text(system: str, user: str, max_tokens: int = 64000, web: bool = False) -> str:
    """긴 마크다운 출력(대본·리서치). web=True 면 웹 검색·페이지 읽기를 허용한다.
    API 는 스트리밍으로 받아 타임아웃을 피한다."""
    if _backend() == "claude-cli":
        return _cli(system, user, tools=["WebSearch", "WebFetch"] if web else None).get("result", "").strip()
    if web:
        return _api_web(system, user, max_tokens)
    with client().messages.stream(
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
        **_common(),
    ) as stream:
        msg = stream.get_final_message()
    _check(msg)
    return "".join(b.text for b in msg.content if b.type == "text").strip()


def _api_web(system: str, user: str, max_tokens: int) -> str:
    """API 백엔드: 서버측 웹 검색·페이지 읽기 도구를 붙여 리서치."""
    tools = [{"type": "web_search_20260209", "name": "web_search", "max_uses": 15},
             {"type": "web_fetch_20260209", "name": "web_fetch", "max_uses": 10}]
    messages = [{"role": "user", "content": user}]
    for _ in range(5):  # pause_turn 이면 이어서 진행
        with client().messages.stream(max_tokens=max_tokens, system=system, messages=messages, tools=tools,
                                      **_common()) as stream:
            msg = stream.get_final_message()
        if msg.stop_reason != "pause_turn":
            break
        messages.append({"role": "assistant", "content": msg.content})
    _check(msg)
    return "".join(b.text for b in msg.content if b.type == "text").strip()


def structured(system: str, user: str, schema: Type[T], max_tokens: int = 16000,
               images: list | None = None) -> T:
    """스키마로 검증된 JSON 출력. images 를 주면 그림(장면 미리보기 등)을 함께 보고 답한다."""
    if _backend() == "claude-cli":
        if images:
            user += "\n\n# 함께 볼 이미지 (Read 로 열어 보세요)\n" + "\n".join(str(p) for p in images)
        out = _cli(system, user, schema.model_json_schema(), tools=["Read"] if images else None)
        return schema.model_validate(_json_from(out))
    content: list | str = user
    if images:
        import base64
        content = [{"type": "image", "source": {"type": "base64", "media_type": "image/png",
                                                 "data": base64.standard_b64encode(open(p, "rb").read()).decode()}}
                   for p in images] + [{"type": "text", "text": user}]
    resp = client().messages.parse(
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": content}],
        output_format=schema,
        **_common(),
    )
    _check(resp)
    return resp.parsed_output
