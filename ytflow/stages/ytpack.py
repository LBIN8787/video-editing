"""유튜브 업로드 묶음: 설명란(요약·기준 시각·챕터 타임코드·출처·면책·해시태그) + 제목 후보 + 태그 → 05_edit/youtube.md
    python -m ytflow yt-pack <프로젝트>
챕터는 hybrid_timeline.json 의 장 표지(chapter) 시작 시각으로 (첫 줄은 00:00 오프닝 — 유튜브 챕터 규칙: 0:00 시작·3개 이상·10초 이상).
출처는 01_research/factsheet.md 의 http 주소 (중복 제거, 순서 유지). 채널 기본 틀은 channels/<채널>/brand/about.md 와 같은 형식.
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path

from ..project import Project

DISCLAIMER = "※ 정보 제공 목적이며 투자 권유가 아닙니다. 사실과 가설을 구분해 전달하며, 가설은 영상에서 '가설'이라고 밝힙니다."
TAGS = {"market": ["주식 시황", "미국 주식", "뉴욕증시", "코스피", "반도체", "시장 브리핑", "경제 뉴스", "이어 읽는 시장"]}


def _ts(sec: float) -> str:
    sec = int(round(sec))
    return f"{sec // 60}:{sec % 60:02d}" if sec < 3600 else f"{sec // 3600}:{sec % 3600 // 60:02d}:{sec % 60:02d}"



def tag_scores(tags: list[str], extra: list[str] | None = None, root: Path | None = None) -> tuple[list[dict], list[dict]]:
    """data/tag_stats.json (scripts/tag_research.py — 비교 채널에서 태그별 '채널 중앙값 대비 조회수 배수') 로
    ① 지금 단 태그의 성적 ② 같은 낱말을 품은 잘 나온 태그 후보를 돌려준다 (2026-11-22 사용자: "어떤 태그가 조회수가 잘나오는지 분석하세요
    이후 이를 참조하여 태그를 달고 수정 할 수 있도록"). 인과가 아니라 같은 주제 안에서 어떤 말을 고를지의 참고."""
    f = (root or Path(__file__).resolve().parents[2]) / "data" / "tag_stats.json"
    if not f.exists():
        return [], []
    st = json.loads(f.read_text(encoding="utf-8"))
    idx = {s["key"]: s for s in st.get("tags", [])}
    norm = lambda s: re.sub(r"\s+", "", s).lower()
    mine = [dict(idx[norm(t)], mine=t) for t in tags if norm(t) in idx]
    words = {w for t in list(tags) + list(extra or []) for w in re.findall(r"[가-힣A-Za-z0-9]{2,}", t.lower())}
    have = {norm(t) for t in tags}
    cand = [s for s in st.get("tags", []) if s["key"] not in have and s["x_geo"] >= 1.2 and any(w in s["key"] for w in words)]
    return mine, sorted(cand, key=lambda s: -s["x_geo"])[:20]


def yt_suggest(seeds: list[str], per: int = 8) -> dict:
    """유튜브 검색 자동완성 (공개 주소, 키 없음) — 사람들이 실제로 치는 검색어 (2026-11-22 사용자: "태그에 따라 조회수가 좀 차이나는거같습니다").
    태그 '후보'만 돌려준다. 영상과 맞는 것만 사람이 고른다(manual/09 §7-1 10)."""
    import urllib.parse
    import urllib.request
    out = {}
    for q in seeds:
        try:
            u = "https://suggestqueries.google.com/complete/search?client=firefox&ds=yt&hl=ko&q=" + urllib.parse.quote(q)
            r = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=10)
            out[q] = [x for x in json.loads(r.read().decode("utf-8", "ignore"))[1] if x != q][:per]
        except Exception:  # noqa: BLE001
            out[q] = []
    return out

def run(project: str):
    pr = Project.open(project)
    spec = json.loads((pr.dir("script") / "hybrid.json").read_text(encoding="utf-8"))
    tl = json.loads((pr.dir("edit") / "hybrid_timeline.json").read_text(encoding="utf-8"))
    pk = spec.get("package") or {}
    t, chapters = 0.0, [("00:00", "오프닝")]   # 공식 도움말 표기 00:00 (support.google.com/youtube/answer/9884579)
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
    # 편마다 태그 (2026-11-21 사용자: "영상노출을 높이기 위해 태그 등도 검토해주세요"): hybrid.json package.tags(그 편의 사건·인물·기업·
    # 핫 키워드 — 사람들이 검색할 말) 먼저, 채널 공통은 뒤에. 유튜브 태그 합계 500자 안. 해시태그는 package.hashtags 또는 편 태그 앞 3개.
    tags = []
    for x in list(pk.get("tags") or []) + TAGS.get(brand, []):
        if x and x not in tags and len(", ".join(tags + [x])) <= 480:
            tags.append(x)
    hashtags = pk.get("hashtags") or (pk.get("tags") or tags)[:3]
    desc = [spec.get("core_message", ""), ""]
    if as_of:
        desc += [f"📌 기준: {as_of}", ""]
    # 원본 영상·사진 출처 (manual/09 §3-5 '설명란 [원본] 목록', CC BY 표시 의무 — 2026-11-21 빠져 있던 것 채움)
    used = {sc.get("clip", {}).get("src") for sc in spec["scenes"] if isinstance(sc.get("clip"), dict)} | {sc.get("bg_src") for sc in spec["scenes"]}
    clips_, photos_ = [], []
    for k, f in (spec.get("footage") or {}).items():
        if k not in used or not isinstance(f, dict):
            continue
        if f.get("who") and f.get("url"):
            clips_.append(f"- {f['who']} — {f.get('credit', '')} {f['url']}".strip())
        elif f.get("credit") and "CC BY" in f.get("license", f.get("credit", "")):
            photos_.append(f"- {f['credit']}" + (f" {f['url']}" if f.get("url") else ""))
    extra = (["", "🎬 원본 영상 (짧은 인용)"] + clips_ if clips_ else []) + (["", "📷 사진"] + photos_ if photos_ else [])
    # 자료 기준일은 영상 끝 화면이 아니라 설명란에 (2026-11-23 사용자: "마지막에 ~~일까지의 자료 이런거 꼭 필요할꺼요?")
    asof = [f"📅 자료 기준: {spec['asof']}"] if spec.get("asof") else []
    desc += ["📌 챕터"] + [f"{a} {b}" for a, b in chapters] + ["", "📚 출처"] + asof + [f"- {u}" for u in urls[:20]] + extra + ["", DISCLAIMER, " ".join("#" + re.sub(r"\s+", "", x).lstrip("#") for x in hashtags[:3])]
    md = [f"# 유튜브 업로드 — {project}", "", "## 제목 (기본 → 테스트 및 비교 후보)"]
    md += [f"{i}. {x}" for i, x in enumerate([pk.get("title", spec.get("title", ""))] + [x for x in pk.get("title_options", []) if x != pk.get("title")], 1)]
    seeds = pk.get("tag_seeds") or [x for x in (pk.get("tags") or [])][:8]
    sug = yt_suggest(seeds) if seeds and os.environ.get("YTFLOW_OFFLINE") != "1" else {}
    sug_md = ["## 검색 자동완성 (태그 후보 — 영상과 맞는 것만 package.tags 앞쪽으로, manual/09 §7-1 10)"] + [f"- {q} → {', '.join(v) or '(없음)'}" for q, v in sug.items()] + [""] if sug else []
    mine, cand = tag_scores(tags, [v for vs in sug.values() for v in vs])
    perf_md = []
    if mine or cand:
        perf_md = ["## 태그 성적 (비교 채널, data/tag_stats.json — 1.0 = 그 채널 평소, 높을수록 잘 나온 영상에 많이 쓰임)"]
        perf_md += ["- 지금 단 태그: " + (", ".join(f"{m['mine']} ×{m['x_geo']}({m['videos']}편)" for m in sorted(mine, key=lambda m: -m['x_geo'])) or "(자료 없음)")]
        perf_md += ["- 같은 낱말의 잘 나온 태그 후보(영상과 맞는 것만): " + (", ".join(f"{c['tag']} ×{c['x_geo']}" for c in cand) or "(없음)"), ""]
    md += ["", "## 설명란 (그대로 붙여 넣기)", "```", *desc, "```", "", "## 태그", ", ".join(tags), "", *perf_md, *sug_md,
           "## 썸네일", "05_edit/thumbnail_A.png · B · C → 유튜브 '테스트 및 비교'에 세 장 모두",
           "", "## 체크", "- 공개 예약: 한국 시간 08:30 (평일, 채널 publish_time)  - 재생목록: 아침 브리핑 / 심층 / 주간",
           f"- 챕터 {len(chapters)}개 (유튜브는 3개 이상·각 10초 이상이어야 표시)",
           "- '변경되거나 합성된 콘텐츠': 실제 인물·사건처럼 보이는 합성 없음 → 아니요 (AI 목소리 사용은 설명란·채널 정보에 밝힘)",
           "- 고정 댓글: 정정이 생기면 여기에 (manual/09 §12)"]
    out = pr.dir("edit") / "youtube.md"
    out.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"[yt-pack] 챕터 {len(chapters)}개 · 출처 {len(urls)}개 → {out}")
    return out
