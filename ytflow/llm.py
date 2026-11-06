"""Claude 호출 래퍼.

backend (config/pipeline.yaml → llm.backend, 또는 환경변수 YTFLOW_LLM_BACKEND):
  claude-cli  Claude Code CLI(`claude -p`). Claude Pro/Max 구독 로그인으로 동작, API 키 불필요
  codex-cli   Codex CLI(`codex exec`). ChatGPT 구독 로그인으로 동작, API 키 불필요
  api         Anthropic API (ANTHROPIC_API_KEY 필요, 사용량만큼 과금)
  manual      프로그램이 LLM 을 부르지 않는다. 요청을 .llm/requests/ 에 파일로 남기고 멈추면,
              작업 중인 에이전트(Claude Code, Codex 등)가 답을 .llm/responses/ 에 쓰고 다시 실행한다.
              → 에이전트 하나가 대화 안에서 모든 판단을 직접 하는 방식 (docs/04-agents.md)
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
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
    return os.environ.get("YTFLOW_LLM_BACKEND") or _cfg().get("backend", "api")


# ---------------------------------------------------------------- codex-cli 백엔드
def strict_schema(schema: dict) -> dict:
    """OpenAI 구조화 출력(strict)용: 모든 객체에 additionalProperties=false, 모든 속성을 required 로."""
    def fix(node):
        if isinstance(node, dict):
            if node.get("type") == "object" and "properties" in node:
                node["additionalProperties"] = False
                node["required"] = list(node["properties"].keys())
            node.pop("default", None)
            for v in node.values():
                fix(v)
        elif isinstance(node, list):
            for v in node:
                fix(v)
        return node
    return fix(json.loads(json.dumps(schema)))


def _codex(system: str, user: str, schema: dict | None = None, web: bool = False, images=None) -> str:
    exe = shutil.which("codex")
    if not exe:
        raise SystemExit("codex CLI 가 없습니다. `npm install -g @openai/codex` 후 `codex login` 하세요.")
    cfg = _cfg()
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "out.txt"
        cmd = [exe] + (["--search"] if web else []) + ["exec", "--skip-git-repo-check", "--ephemeral",
                                                       "-s", "read-only", "-o", str(out)]
        if cfg.get("codex_model"):
            cmd += ["-m", cfg["codex_model"]]
        if schema is not None:
            sf = Path(td) / "schema.json"
            sf.write_text(json.dumps(strict_schema(schema), ensure_ascii=False), encoding="utf-8")
            cmd += ["--output-schema", str(sf)]
        for im in images or []:
            cmd += ["-i", str(im)]
        cmd.append("-")  # 프롬프트는 stdin 으로 (codex exec 에는 별도 system 인자가 없어 앞에 붙인다)
        prompt = f"# 지시\n{system}\n\n# 입력\n{user}"
        proc = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=cfg.get("cli_timeout", 1800))
        if proc.returncode != 0 or not out.exists():
            raise RuntimeError(f"codex exec 실패 (exit {proc.returncode}): {proc.stderr[-1500:]}")
        return out.read_text(encoding="utf-8").strip()


# ---------------------------------------------------------------- manual 백엔드
LLM_DIR = Path(__file__).resolve().parent.parent / ".llm"


class PendingLLM(SystemExit):
    """manual 모드에서 답이 아직 없을 때. 에이전트가 응답 파일을 쓰고 다시 실행하면 이어진다."""


def _manual(kind: str, system: str, user: str, schema: dict | None = None, web: bool = False, images=None):
    key = hashlib.sha1(json.dumps([kind, system, user, schema], ensure_ascii=False).encode()).hexdigest()[:12]
    req, res_dir = LLM_DIR / "requests", LLM_DIR / "responses"
    req.mkdir(parents=True, exist_ok=True)
    res_dir.mkdir(parents=True, exist_ok=True)
    ext = "json" if schema is not None else "md"
    res = res_dir / f"{key}.{ext}"
    if res.exists():
        txt = res.read_text(encoding="utf-8")
        return json.loads(txt) if schema is not None else txt
    body = [f"# LLM 요청 {key} ({kind})", "",
            f"답을 `{res.relative_to(LLM_DIR.parent)}` 에 쓰고 같은 명령을 다시 실행하세요.",
            "웹 검색이 필요한 요청입니다. 직접 검색해 출처 URL 을 다세요." if web else "",
            "", "## 지시 (system)", system, "", "## 입력 (user)", user]
    if images:
        body += ["", "## 함께 볼 이미지", *[str(i) for i in images]]
    if schema is not None:
        body += ["", "## 답 형식: 아래 JSON Schema 를 만족하는 JSON 하나만", "```json",
                 json.dumps(schema, ensure_ascii=False, indent=1), "```"]
    f = req / f"{key}.md"
    f.write_text("\n".join(body), encoding="utf-8")
    raise PendingLLM(f"[manual] LLM 응답이 필요합니다 → 요청: {f.relative_to(LLM_DIR.parent)}  /  답: {res.relative_to(LLM_DIR.parent)}")


# ---------------------------------------------------------------- 공용 진입점
def text(system: str, user: str, max_tokens: int = 64000, web: bool = False) -> str:
    """긴 마크다운 출력(대본·리서치). web=True 면 웹 검색·페이지 읽기를 허용한다.
    API 는 스트리밍으로 받아 타임아웃을 피한다."""
    b = _backend()
    if b == "manual":
        return _manual("text", system, user, web=web)
    if b == "codex-cli":
        return _codex(system, user, web=web)
    if b == "claude-cli":
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
    b = _backend()
    if b == "manual":
        return schema.model_validate(_manual("structured", system, user, schema.model_json_schema(), images=images))
    if b == "codex-cli":
        return schema.model_validate_json(_codex(system, user, schema.model_json_schema(), images=images))
    if b == "claude-cli":
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
