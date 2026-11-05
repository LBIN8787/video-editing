"""1단계: 소스 탐색 — '작은 채널인데 터진 영상'과 뉴스에서 주제 후보를 모은다.

아웃라이어 = 조회수 / 구독자수. 구독자 대비 많이 터진 영상은 채널 파워가 아니라
'주제·제목·썸네일'의 힘으로 터졌을 가능성이 높아 벤치마킹 가치가 크다.
"""
from __future__ import annotations

import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

from .. import config, yt
from ..project import Project


# YouTube 검색 필터: 업로드 날짜 = 이번 주 (관련도순). 최근 1주 안에 터진 영상을 찾는다.
WEEK_FILTER = "EgIIAw%253D%253D"


def search_keyword(kw: str, n: int) -> list[dict]:
    url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(kw)}&sp={WEEK_FILTER}"
    data = yt.flat_playlist(url, n) or {}
    out = []
    for e in data.get("entries") or []:
        if e and e.get("id") and (e.get("duration") or 0) > 70:
            out.append({"id": e["id"], "title": e.get("title", ""), "channel": e.get("channel") or e.get("uploader"),
                        "views": e.get("view_count") or 0, "duration": e.get("duration") or 0, "keyword": kw})
    return out


def enrich(c: dict) -> dict:
    info = yt.video_info(c["id"]) or {}
    subs = info.get("channel_follower_count") or 0
    up = info.get("upload_date")
    days = max((datetime.now() - datetime.strptime(up, "%Y%m%d")).days, 1) if up else None
    c.update({
        "subscribers": subs,
        "upload_date": up,
        "outlier": round(c["views"] / subs, 2) if subs else None,
        "views_per_day": round(c["views"] / days) if days else None,
        "description": (info.get("description") or "")[:500],
        "tags": (info.get("tags") or [])[:15],
    })
    return c


def read_rss(urls: list[str], limit: int = 15) -> list[dict]:
    items = []
    for u in urls:
        try:
            with urllib.request.urlopen(u, timeout=15) as r:
                root = ET.fromstring(r.read())
            for it in root.iter("item"):
                items.append({"title": it.findtext("title"), "link": it.findtext("link"), "feed": u})
                if len(items) >= limit:
                    break
        except Exception as e:  # 피드 하나가 죽어도 전체는 계속
            print(f"  ! RSS 실패 {u}: {e}")
    return items


def run(project: Project, keywords: list[str] | None = None) -> None:
    cfg = config.load("pipeline").get("discover", {})
    kws = keywords or cfg.get("seed_keywords", [])
    pool: dict[str, dict] = {}
    for kw in kws:
        print(f"[discover] 검색: {kw}")
        for c in search_keyword(kw, cfg.get("search_per_keyword", 25)):
            pool.setdefault(c["id"], c)
    ranked = sorted(pool.values(), key=lambda c: c["views"], reverse=True)[: cfg.get("deep_check_top", 15)]
    print(f"[discover] 상위 {len(ranked)}개 아웃라이어 계산")
    enriched = [enrich(c) for c in ranked]
    min_o = cfg.get("min_outlier", 2.0)
    enriched.sort(key=lambda c: (c["outlier"] or 0), reverse=True)
    for c in enriched:
        c["pass"] = bool(c["outlier"] and c["outlier"] >= min_o)
    project.write_json("source", "candidates.json", enriched)
    project.write_json("source", "news.json", read_rss(cfg.get("rss_feeds", [])))
    print(f"[discover] 기준 통과 {sum(c['pass'] for c in enriched)}개 → {project.dir('source')}/candidates.json")
    project.mark_done("discover")
