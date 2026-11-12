"""유튜브 업로드 묶음: 설명란(요약·기준 시각·챕터 타임코드·출처·면책·해시태그) + 제목 후보 + 태그 → 05_edit/youtube.md
    python -m ytflow yt-pack <프로젝트>
챕터는 hybrid_timeline.json 의 장 표지(chapter) 시작 시각으로 (첫 줄은 00:00 오프닝 — 유튜브 챕터 규칙: 0:00 시작·3개 이상·10초 이상).
출처는 01_research/factsheet.md 의 http 주소 (중복 제거, 순서 유지). 채널 기본 틀은 channels/<채널>/brand/about.md 와 같은 형식.
"""
from __future__ import annotations

import json
import re

from ..project import Project

DISCLAIMER = "※ 정보 제공 목적이며 투자 권유가 아닙니다. 사실과 해석을 구분해 전달하며, 해석은 영상에서 '해석'이라고 밝힙니다."
TAGS = {"market": ["주식 시황", "미국 주식", "뉴욕증시", "코스피", "반도체", "시장 브리핑", "경제 뉴스", "이어 읽는 시장"]}


def _ts(sec: float) -> str:
    sec = int(round(sec))
    return f"{sec // 60}:{sec % 60:02d}" if sec < 3600 else f"{sec // 3600}:{sec % 3600 // 60:02d}:{sec % 60:02d}"


def run(project: str):
    pr = Project.open(project)
    spec = json.loads((pr.dir("script") / "hybrid.json").read_text(encoding="utf-8"))
    tl = json.loads((pr.dir("edit") / "hybrid_timeline.json").read_text(encoding="utf-8"))
    pk = spec.get("package") or {}
    t, chapters = 0.0, [("0:00", "오프닝")]
    by_id = {s["id"]: s for s in spec["scenes"]}
    for x in tl:
        sc = by_id.get(x["scene"], {})
        if sc.get("type") == "chapter" and t >= 10:
            chapters.append((_ts(t), f"{sc.get('num', '')}. {sc.get('title', '')}".strip(". ")))
        t += x["dur"]
    fs = (pr.dir("research") / "factsheet.md")
    urls = []
    if fs.exists():
        for u in re.findall(r"https?://[^\s)>\]]+", fs.read_text(encoding="utf-8")):
            u = u.rstrip(".,")
            if u not in urls:
                urls.append(u)
    tb = {}
    tbp = pr.dir("research") / "topic_brief.json"
    if tbp.exists():
        tb = json.loads(tbp.read_text(encoding="utf-8"))
    as_of = (tb.get("daily") or {}).get("as_of") or ""
    brand = spec.get("brand") or tb.get("brand") or ""
    tags = TAGS.get(brand, [])
    desc = [spec.get("core_message", ""), ""]
    if as_of:
        desc += [f"📌 기준: {as_of}", ""]
    desc += ["📌 챕터"] + [f"{a} {b}" for a, b in chapters] + ["", "📚 출처"] + [f"- {u}" for u in urls[:20]] + ["", DISCLAIMER, " ".join("#" + re.sub(r"\s+", "", x) for x in tags[:3])]
    md = [f"# 유튜브 업로드 — {project}", "", "## 제목 (기본 → 테스트 및 비교 후보)"]
    md += [f"{i}. {x}" for i, x in enumerate([pk.get("title", spec.get("title", ""))] + [x for x in pk.get("title_options", []) if x != pk.get("title")], 1)]
    md += ["", "## 설명란 (그대로 붙여 넣기)", "```", *desc, "```", "", "## 태그", ", ".join(tags), "",
           "## 썸네일", "05_edit/thumbnail_A.png · B · C → 유튜브 '테스트 및 비교'에 세 장 모두",
           "", "## 체크", "- 공개 예약: 한국 시간 08:00 (평일)  - 재생목록: 아침 브리핑 / 심층 / 주간",
           f"- 챕터 {len(chapters)}개 (유튜브는 3개 이상·각 10초 이상이어야 표시)",
           "- '변경되거나 합성된 콘텐츠': 실제 인물·사건처럼 보이는 합성 없음 → 아니요 (AI 목소리 사용은 설명란·채널 정보에 밝힘)",
           "- 고정 댓글: 정정이 생기면 여기에 (manual/09 §12)"]
    out = pr.dir("edit") / "youtube.md"
    out.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"[yt-pack] 챕터 {len(chapters)}개 · 출처 {len(urls)}개 → {out}")
    return out
