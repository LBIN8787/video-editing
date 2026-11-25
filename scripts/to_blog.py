"""영상 한 편 → 블로그 글 한 편 (수익화 경로 B, docs/80-revenue-plan.md).

이미 쓴 대본(02_script/hybrid.json)과 팩트시트 출처, 올린 영상 주소로
티스토리·네이버 블로그에 붙여 넣을 마크다운을 만든다. 새 사실을 더하지 않고
대본의 문장만 옮긴다(사실 규칙 그대로). 결과: 05_edit/blog.md

    python scripts/to_blog.py projects/20261125-market-daily
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

DISCLAIMER = (
    "※ 정보 제공 목적이며 투자 권유가 아닙니다. 숫자는 글 끝의 출처로 확인한 것만 썼고, "
    "'해석'이라고 적은 부분은 이 채널의 판단입니다."
)


def _chapters(scenes: list[dict]) -> list[tuple[str, list[str]]]:
    out: list[tuple[str, list[str]]] = []
    cur_title, cur_lines, cur_ch = "", [], None
    for s in scenes:
        ch = s.get("chapter")
        if s.get("type") == "outro":
            continue
        if ch != cur_ch or s.get("type") == "chapter":
            if cur_lines:
                out.append((cur_title, cur_lines))
            cur_title, cur_lines, cur_ch = "", [], ch
        if s.get("type") == "chapter":
            cur_title = s.get("title") or s.get("label") or ""
        for b in s.get("beats", []):
            say = (b.get("say") or "").strip()
            if say:
                cur_lines.append(say)
    if cur_lines:
        out.append((cur_title, cur_lines))
    return out


def _sources(factsheet: str, limit: int = 15) -> list[str]:
    urls, seen = [], set()
    for u in re.findall(r"https?://[^\s)|,]+", factsheet):
        u = u.rstrip(".")
        if u not in seen:
            seen.add(u)
            urls.append(u)
    return urls[:limit]


def build(project: Path) -> str:
    h = json.loads((project / "02_script/hybrid.json").read_text(encoding="utf-8"))
    pkg = h.get("package") or {}
    title = (pkg.get("title_options") or [pkg.get("title") or h.get("title")])[0]
    pub = project / "05_edit/youtube_publish.json"
    url = json.loads(pub.read_text(encoding="utf-8")).get("url") if pub.exists() else None
    fs = project / "01_research/factsheet.md"
    sources = _sources(fs.read_text(encoding="utf-8")) if fs.exists() else []

    lines = [f"# {title}", ""]
    if h.get("core_message"):
        lines += ["> **세 줄 요약** — " + h["core_message"], ""]
    if url:
        lines += [f"▶ 영상으로 보기: {url}", ""]
    for i, (ct, says) in enumerate(_chapters(h.get("scenes", []))):
        if i == 0 and not ct:
            ct = "무슨 일이 있었나"
        if ct:
            lines += [f"## {ct}", ""]
        lines += [" ".join(says), ""]
    if h.get("glossary"):
        lines += ["## 용어 풀이", ""]
        lines += [f"- **{g['term']}** — {g['plain']}" for g in h["glossary"]]
        lines.append("")
    if sources:
        lines += ["## 출처", ""] + [f"- {u}" for u in sources] + [""]
    lines += ["---", DISCLAIMER, ""]
    if url:
        lines += [f"매일 아침 시장 정리는 유튜브 채널에서 영상으로 올립니다: {url}", ""]
    return "\n".join(lines)


def main() -> None:
    project = Path(sys.argv[1])
    out = project / "05_edit/blog.md"
    out.write_text(build(project), encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
