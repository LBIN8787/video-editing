"""소스 먼저 (scout): 주제를 고르기 전에, 채널마다 '무엇을 들고 영상을 만들 수 있나'부터 찾는다.

벤치마킹 결과(docs/07-sourcing.md) — 채널마다 소스의 출발점이 다르다:
- statement (원본 소스형, 식스시그마식): 인물이 직접 말한 **원본 영상**에서 출발한다.
  CNBC·블룸버그 TV·공식 IR 실적발표·투자사·대학·팟캐스트 공식 채널의 최근 10일 영상 → 발언 → 공시·데이터로 교차 확인.
- document (자체 제작 칼럼형, 미주일기식): **1차 문서**에서 출발한다.
  기업 연구 블로그·논문(arXiv)·IR 보도자료·SEC 공시·정부·연구소 → 사진은 위키미디어 공용(CC 라이선스, 저작자 표기).
- data (데이터 리포트형, 머니크루식): **숫자 계열**에서 출발한다. 시세·통계를 직접 계산하고 과거 비슷한 시기와 맞댄다.
- repo (AI 쇼츠): GitHub 저장소·README.

산출물:
  00_source/scout.json   후보 소스 (트렌드 화제별)
  00_source/inventory.json / inventory.md   주제가 정해진 뒤 이 영상에 쓸 소스 목록 (S1, S2 …) — 대본은 이 목록으로 짓는다
"""
from __future__ import annotations

import json
import re
import subprocess
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

from pydantic import BaseModel, Field

from .. import config, llm
from ..project import Project

UA = {"User-Agent": "ytflow/1.0 (YouTube research pipeline; contact: repository owner)"}


# ---------------------------------------------------------------- 공용
def recipe() -> dict:
    """채널의 소스 찾기 방식 (channel.yaml 의 sourcing). 채널이 없으면 스타일 계열로 추정."""
    data = config.load("pipeline")
    cid = data.get("channel")
    if cid:
        s = config.channel(cid).get("sourcing")
        if s:
            return s
    fam = config.style_family()
    return {"start_from": {"source": "statement", "infographic": "document", "shorts": "repo"}.get(fam, "document")}


def channel_videos(handle: str, limit: int = 30, max_age_days: int = 10) -> list[dict]:
    """공식·방송 채널의 최근 영상 목록 (yt-dlp 목록 조회만, 다운로드 없음)."""
    url = f"https://www.youtube.com/{handle}/videos"
    try:
        out = subprocess.run(["yt-dlp", "--flat-playlist", "--playlist-end", str(limit), "--print",
                              "%(id)s\t%(title)s\t%(duration)s\t%(upload_date)s", url],
                             capture_output=True, text=True, timeout=120).stdout
    except Exception:
        return []
    rows = []
    for line in out.splitlines():
        p = line.split("\t")
        if len(p) < 2:
            continue
        rows.append({"id": p[0], "title": p[1], "duration": float(p[2]) if p[2] not in ("NA", "") else None,
                     "date": p[3] if len(p) > 3 and p[3] != "NA" else "", "channel": handle,
                     "url": f"https://www.youtube.com/watch?v={p[0]}"})
    return rows


def commons_photos(query: str, n: int = 4) -> list[dict]:
    """위키미디어 공용 사진 (CC·퍼블릭 도메인만, 저작자·라이선스 표기 정보 포함)."""
    q = urllib.parse.urlencode({"action": "query", "format": "json", "generator": "search", "gsrsearch": query,
                                "gsrnamespace": 6, "gsrlimit": n * 3, "prop": "imageinfo",
                                "iiprop": "url|extmetadata", "iiurlwidth": 1600})
    try:
        with urllib.request.urlopen(urllib.request.Request(f"https://commons.wikimedia.org/w/api.php?{q}", headers=UA), timeout=20) as r:
            pages = json.loads(r.read()).get("query", {}).get("pages", {})
    except Exception:
        return []
    out = []
    for p in pages.values():
        ii = (p.get("imageinfo") or [{}])[0]
        m = ii.get("extmetadata") or {}
        lic = (m.get("LicenseShortName") or {}).get("value", "")
        if not re.search(r"CC|Public domain|PD", lic, re.I) or re.search(r"NC|ND", lic):  # 상업 이용·변형 가능한 것만
            continue
        artist = re.sub(r"<[^>]+>", "", (m.get("Artist") or {}).get("value", "")).strip()
        out.append({"title": p.get("title", "").replace("File:", ""), "image": ii.get("thumburl") or ii.get("url"),
                    "page": ii.get("descriptionurl", ""), "license": lic, "artist": artist[:80]})
        if len(out) >= n:
            break
    return out


# ---------------------------------------------------------------- 1) 트렌드 화제별 후보 소스 (select 전에)
class SourceCand(BaseModel):
    kind: str = Field(description="video(인터뷰·실적발표·키노트·팟캐스트 원본) | document(공시·보도자료·논문·정부·연구소) | "
                                  "data(시세·통계 계열) | news(주요 언론) | x_post | repo")
    title: str
    publisher: str = Field(description="발행처 (회사 IR, SEC, CNBC, arXiv …)")
    date: str = Field(description="YYYY-MM-DD (모르면 빈 문자열)")
    url: str = Field(description="실제로 찾은 URL만 (지어내지 말 것)")
    speaker: str = Field("", description="video·x_post: 말한 사람과 직함")
    claim: str = Field(description="이 소스가 주는 핵심 한 줄 (발언 요지·숫자)")
    use_as: str = Field(description="quote(원래 목소리 발언) | screenshot(문서 캡처) | card_data(카드·차트 숫자) | photo | broll")


class TopicSources(BaseModel):
    topic: str = Field(description="화제 한 줄")
    sources: list[SourceCand]
    depth: str = Field(description="이 화제로 쓸 수 있는 글의 깊이: '분석'(서로 이어지는 주장 3개 이상, 숫자·반론·과거 사례가 있음) | '안내'(한 가지 사실·방법·도구, 5문장이면 끝남)")
    depth_reason: str


class ScoutResult(BaseModel):
    topics: list[TopicSources]


def run(project: Project) -> None:
    r = recipe()
    tf = project.dir("source") / "trends.json"
    trends = json.loads(tf.read_text(encoding="utf-8")) if tf.exists() else {}
    kws = [k["keyword"] for k in (trends.get("keywords") or [])[:6]]
    heads = (trends.get("headlines") or [])[:60]
    sl = project.dir("source") / "shortlist.json"
    if not kws and sl.exists():  # 주제를 직접 준 경우: 그 주제 하나의 소스만 찾는다
        given = json.loads(sl.read_text(encoding="utf-8"))[0]
        kws, heads = [given["title_working"]], [given["title_working"] + (" — " + given["angle"] if given.get("angle") else "")]
    found = {"recipe": r, "videos": [], "topics": []}
    if r.get("start_from") == "statement":  # 공식·방송 채널의 최근 원본 영상부터 훑는다 (목록만 조회)
        age = r.get("max_age_days", 10)
        cutoff = (datetime.now(timezone.utc) - timedelta(days=age)).strftime("%Y%m%d")
        for h in r.get("video_channels", []):
            vids = [v for v in channel_videos(h, 40, age) if (v["duration"] or 0) >= r.get("min_seconds", 240)]
            vids = [v for v in vids if not v["date"] or v["date"] >= cutoff]
            print(f"[scout] {h}: 최근 원본 후보 {len(vids)}개")
            found["videos"] += vids
    hint = {
        "statement": "인물이 직접 말한 원본 영상(인터뷰·실적발표 콜·키노트·청문회·팟캐스트)을 먼저 찾고, 그 발언을 확인할 공시·데이터를 붙이세요. "
                     "아래 '최근 원본 영상 목록'에서 화제와 맞는 영상을 우선 고르세요.",
        "document": "1차 문서(기업 연구 블로그·논문·IR 보도자료·SEC 공시·정부·연구소 보고서)를 먼저 찾고, 그 문서가 말하는 숫자·주장을 정리하세요. "
                    "인물 발언은 X 게시물이나 공식 영상이 있으면 덧붙입니다.",
        "data": "직접 계산하고 그릴 수 있는 숫자 계열(시세 티커, 통계 기관 지표, 수출 통계)과 비교할 과거 시기를 먼저 찾고, 해석은 주요 언론·공시로 확인하세요.",
        "repo": "GitHub 저장소·README·공식 문서를 찾으세요.",
    }[r.get("start_from", "document")]
    user = (f"# 오늘\n{datetime.now().date().isoformat()}\n\n# 채널 분야\n{config.load('pipeline').get('channel_niche', '')}\n\n"
            f"# 소스 찾는 방식\n{hint}\n추가 규칙: {json.dumps(r, ensure_ascii=False)}\n\n# 화제 키워드\n{kws}\n\n"
            f"# 최근 헤드라인\n{json.dumps(heads, ensure_ascii=False)[:30000]}\n\n"
            f"# 최근 원본 영상 목록 (공식·방송 채널)\n{json.dumps(found['videos'], ensure_ascii=False)[:20000]}")
    print("[scout] 화제별 소스 찾는 중 (웹 검색)")
    res = llm.structured(config.prompt("scout"), user, ScoutResult, web=True, max_tokens=16000)
    found["topics"] = [t.model_dump() for t in res.topics]
    project.write_json("source", "scout.json", found)
    for t in found["topics"]:
        kinds = {}
        for s in t["sources"]:
            kinds[s["kind"]] = kinds.get(s["kind"], 0) + 1
        print(f"[scout] {t['depth']:2} · {t['topic'][:44]} — " + ", ".join(f"{k} {v}" for k, v in kinds.items()))
    project.mark_done("scout")


# ---------------------------------------------------------------- 2) 주제가 정해진 뒤: 이 영상의 소스 목록
def inventory(project: Project) -> list[dict]:
    """select 가 고른 주제의 소스를 S번호 목록으로 확정하고, 필요한 사진(CC)을 붙인다."""
    from .writing import chosen_topic
    topic = chosen_topic(project)
    sc = project.read_json("source", "scout.json") if (project.dir("source") / "scout.json").exists() else {"topics": []}
    picked = next((t for t in sc["topics"] if t["topic"] == topic.get("scout_topic")), None) or \
        (sc["topics"][topic.get("scout_index", 0)] if sc["topics"] else {"sources": []})
    inv = []
    for i, s in enumerate(picked.get("sources", []), 1):
        inv.append({"id": f"S{i}", **s})
    if recipe().get("photos") and topic.get("entities"):  # 인물·장소 사진: 위키미디어 공용 CC
        for e in topic["entities"][:4]:
            for ph in commons_photos(e, 2):
                inv.append({"id": f"S{len(inv) + 1}", "kind": "photo", "title": ph["title"], "publisher": "Wikimedia Commons",
                            "date": "", "url": ph["page"], "image": ph["image"], "speaker": "", "claim": e,
                            "use_as": "photo", "license": ph["license"], "artist": ph["artist"]})
    project.write_json("source", "inventory.json", inv)
    md = ["# 소스 목록 (대본은 이 목록의 S번호로 장면을 짓습니다)\n", "| S | 종류 | 쓰임 | 제목 | 발행처·말한 사람 | 날짜 | 핵심 |", "|---|---|---|---|---|---|---|"]
    for s in inv:
        who = s.get("speaker") or s.get("publisher", "")
        lic = f" ({s['license']}, {s.get('artist', '')})" if s.get("license") else ""
        md.append(f"| {s['id']} | {s['kind']} | {s['use_as']} | [{s['title'][:50]}]({s['url']}) | {who[:30]}{lic} | {s.get('date', '')} | {s['claim'][:60]} |")
    (project.dir("source") / "inventory.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"[inventory] 소스 {len(inv)}개 → {project.dir('source')}/inventory.md")
    return inv
