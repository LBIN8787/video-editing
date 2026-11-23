"""10단계: 제작 보고서 — 영상 1편의 자료조사·대본·소스·편집·업로드 정보를 한 문서로 (REPORT.md)."""
from __future__ import annotations

import csv
import json
from pathlib import Path

from .. import config
from ..project import Project


def _csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with open(path, encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def run(project: Project) -> None:
    P = project
    st = P.state()
    style = config.load("pipeline").get("edit", {}).get("style", "sixsigma")
    scenes = P.read_json("script", "scenes.json")
    sc = scenes["scenes"]
    durs = json.loads((P.dir("voice") / "durations.json").read_text()) if (P.dir("voice") / "durations.json").exists() else {}
    total = sum(durs.values()) if durs else 0
    pkg = json.loads((P.dir("package") / "upload.json").read_text(encoding="utf-8")) if (P.dir("package") / "upload.json").exists() else {}
    fact = (P.dir("research") / "factsheet.md").read_text(encoding="utf-8") if (P.dir("research") / "factsheet.md").exists() else ""
    clips = {r["scene"]: r for r in _csv(P.dir("assets") / "clips.csv")}
    shots = {r["scene"]: r for r in _csv(P.dir("assets") / "shotlist.csv")}
    kinds = {}
    for s in sc:
        kinds[s["visual_type"]] = kinds.get(s["visual_type"], 0) + 1
    todo = [r for r in shots.values() if not r["status"].startswith("OK")]

    L = [f"# 제작 보고서 — {scenes['title_working']}", "",
         f"- 프로젝트: `{P.path.name}` · 편집 스타일: **{style}** · 길이 약 **{total / 60:.1f}분** · 장면 {len(sc)}개",
         f"- 화면 구성: " + ", ".join(f"{k} {v}" for k, v in sorted(kinds.items())),
         f"- 가편집: `05_edit/draft.mp4` · 자막: `05_edit/subs.srt` · 타임라인: `05_edit/timeline.csv`",
         f"- 실제 소스로 바꿔야 할 장면: **{len(todo)}개**" + (" (아래 '남은 일')" if todo else ""), ""]
    if pkg:
        L += ["## 1. 업로드 패키지", "", "**제목 후보**", *[f"{i}. {t}" for i, t in enumerate(pkg.get("titles", []), 1)], "",
              "**썸네일 문구**: " + " / ".join(pkg.get("thumbnail_texts", [])), "",
              "**설명란**", "```", pkg.get("description", ""), "```",
              "**태그**: " + ", ".join(pkg.get("tags", [])), "", f"**고정 댓글**: {pkg.get('pinned_comment', '')}", ""]
    L += ["## 2. 자료조사 (팩트시트)", "", fact.replace("\n# ", "\n### ").replace("\n## ", "\n### "), ""]
    L += ["## 3. 대본과 소스", "", "| # | 구간 | 내레이션 / 원문 발언 | 화면 | 소스 | 상태 |", "|---|---|---|---|---|---|"]
    for s in sc:
        sid = str(s["id"])
        src = s.get("source") or {}
        rng = f" {src.get('start', '')}~{src.get('end', '')}" if src.get("start") else ""
        link = f"[{s.get('label') or '링크'}]({src['url']}){rng}" if src.get("url") else (s.get("label") or "")
        text = s["narration"].replace("|", "/")
        if s.get("kind") == "quote":
            text = f"🎙 \"{s.get('quote_en', '')}\" → {text}"
        status = (shots.get(sid) or {}).get("status", "")
        if clips.get(sid, {}).get("status") == "FAILED":
            status += " · 클립 다운로드 실패"
        L.append(f"| {sid} | {s['section']} | {text} | {s['visual_type']} | {link} | {status} |")
    L.append("")
    if todo:
        L += ["## 4. 남은 일", "",
              "1. 본인 PC에서 `python -m ytflow rebuild " + P.path.name + "` 실행 → YouTube 클립을 받아 임시 화면을 교체",
              "2. 받기 실패한 장면은 `04_assets/clips.csv` 의 URL·구간으로 직접 받아 `04_assets/scene_XXX.mp4` 로 넣고 다시 rebuild",
              "3. 팩트시트의 '재확인 필요' 항목 확인 → 썸네일 제작 → 업로드", "",
              "| 장면 | 상태 | 화면 지시 |", "|---|---|---|",
              *[f"| {r['scene']} | {r['status']} | {r['visual_brief']} |" for r in todo], ""]
    (P.path / "REPORT.md").write_text("\n".join(L), encoding="utf-8")
    print(f"[report] {P.path}/REPORT.md")
    P.mark_done("report")
