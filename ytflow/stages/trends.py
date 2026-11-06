"""1단계(소스 탐색)의 트렌드 레이더 — 지금 가장 많이, 가장 새로 이야기되는 소재를 여러 매체에서 모은다.

공개 인터페이스만 쓴다 (접근을 막는 곳은 우회하지 않고 건너뜀):
  - Google News RSS (한국어·영어)       최근 window_hours 안의 기사, 매체 수
  - Hacker News (Algolia 공개 API)        기술 커뮤니티 반응(점수·댓글)
  - X 공식 API v2 최근 검색 (선택)         키가 있을 때만: 환경변수 X_BEARER_TOKEN, 또는 실행 환경의 네트워크 시크릿
    키가 없으면 X 게시물은 research 단계의 웹 검색과 x_accounts 목록으로 찾는다.
  - YouTube 이번 주 아웃라이어            discover.py (기존)
산출물: 00_source/trends.json  — 키워드별 화제성 점수 + 최신 헤드라인 목록 (select 단계가 주제를 고를 때 사용)
"""
from __future__ import annotations

import json
import os
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

from .. import config

UA = {"User-Agent": "ytflow/0.1 (trend research)"}


def _get(url: str, headers: dict | None = None, timeout: int = 20) -> bytes | None:
    import time
    import urllib.error
    for attempt in range(3):  # 일시 오류(429·5xx)만 잠깐 쉬고 다시. 401·403 은 바로 포기 (차단은 우회하지 않음)
        try:
            req = urllib.request.Request(url, headers={**UA, **(headers or {})})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < 2:
                time.sleep(2 * (attempt + 1))
                continue
            print(f"  ! {url.split('?')[0][:60]} 실패: {str(e)[:80]}")
            return None
        except Exception as e:
            print(f"  ! {url.split('?')[0][:60]} 실패: {str(e)[:80]}")
            return None
    return None


def _age_h(dt: datetime) -> float:
    return max(0.0, (datetime.now(timezone.utc) - dt).total_seconds() / 3600)


def google_news(q: str, lang: str, window_h: int) -> list[dict]:
    loc = {"ko": "hl=ko&gl=KR&ceid=KR:ko", "en": "hl=en-US&gl=US&ceid=US:en"}[lang]
    days = max(1, round(window_h / 24))
    raw = _get(f"https://news.google.com/rss/search?q={urllib.parse.quote(q)}+when:{days}d&{loc}")
    if not raw:
        return []
    out = []
    for it in ET.fromstring(raw).iter("item"):
        try:
            dt = parsedate_to_datetime(it.findtext("pubDate"))
        except Exception:
            continue
        title = it.findtext("title") or ""
        src = it.findtext("source") or ""
        out.append({"channel": "news", "lang": lang, "title": re.sub(rf"\s+-\s+{re.escape(src)}$", "", title),
                    "source": src, "url": it.findtext("link"), "published": dt.isoformat(), "age_h": round(_age_h(dt), 1)})
    return [x for x in out if x["age_h"] <= window_h]


def hacker_news(q: str, window_h: int) -> list[dict]:
    since = int(datetime.now(timezone.utc).timestamp()) - window_h * 3600
    raw = _get(f"https://hn.algolia.com/api/v1/search?query={urllib.parse.quote(q)}&tags=story"
               f"&numericFilters=created_at_i>{since}&hitsPerPage=20")
    if not raw:
        return []
    out = []
    for h in json.loads(raw).get("hits", []):
        dt = datetime.fromtimestamp(h["created_at_i"], timezone.utc)
        out.append({"channel": "hackernews", "lang": "en", "title": h.get("title") or "", "source": "Hacker News",
                    "url": h.get("url") or f"https://news.ycombinator.com/item?id={h['objectID']}",
                    "published": dt.isoformat(), "age_h": round(_age_h(dt), 1),
                    "engagement": (h.get("points") or 0) + 2 * (h.get("num_comments") or 0)})
    return out


_x_disabled = False


def x_recent(q: str, window_h: int) -> list[dict]:
    """X API v2 최근 검색. 키가 없거나 권한이 없으면 한 번 알리고 이번 실행에서는 끈다."""
    global _x_disabled
    if _x_disabled:
        return []
    token = os.environ.get("X_BEARER_TOKEN")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    query = urllib.parse.quote(f"{q} -is:retweet")
    raw = _get(f"https://api.x.com/2/tweets/search/recent?query={query}&max_results=25"
               f"&tweet.fields=created_at,public_metrics,author_id&expansions=author_id&user.fields=username,verified",
               headers)
    if not raw:
        _x_disabled = True
        print("  · X API 사용 안 함 (키 없음/권한 없음) → X 게시물은 research 단계 웹 검색으로 찾습니다")
        return []
    data = json.loads(raw)
    users = {u["id"]: u for u in (data.get("includes") or {}).get("users", [])}
    out = []
    for t in data.get("data", []):
        dt = datetime.fromisoformat(t["created_at"].replace("Z", "+00:00"))
        if _age_h(dt) > window_h:
            continue
        u = users.get(t.get("author_id"), {})
        m = t.get("public_metrics") or {}
        out.append({"channel": "x", "lang": "", "title": t.get("text", "")[:200], "source": "@" + u.get("username", ""),
                    "url": f"https://x.com/{u.get('username', 'i')}/status/{t['id']}", "published": dt.isoformat(),
                    "age_h": round(_age_h(dt), 1),
                    "engagement": m.get("like_count", 0) + 3 * m.get("retweet_count", 0) + 2 * m.get("reply_count", 0)})
    return out


def collect(keywords: list[str]) -> dict:
    cfg = config.load("pipeline").get("trends", {})
    window = int(cfg.get("window_hours", 48))
    en_map = cfg.get("english_keywords", {})
    rows, items = [], []
    for kw in keywords:
        print(f"[trends] {kw}")
        en = en_map.get(kw, kw if re.fullmatch(r"[\x00-\x7f]+", kw) else "")
        got = google_news(kw, "ko", window)
        if en:
            got += google_news(en, "en", window)
            if cfg.get("hackernews", True):
                got += hacker_news(en, window)
            if cfg.get("x_api", True):
                got += x_recent(en, window)
        news = [g for g in got if g["channel"] == "news"]
        srcs = {g["source"] for g in news}
        fresh = sum(1 for g in got if g["age_h"] <= 12)
        eng = sum(g.get("engagement", 0) for g in got)
        # 화제성: 매체 다양성 × 최신성 + 커뮤니티 반응 (단순 합산 점수, 순위 비교용)
        score = len(srcs) * 2 + fresh * 3 + min(eng, 3000) / 100
        rows.append({"keyword": kw, "score": round(score, 1), "articles": len(news), "outlets": len(srcs),
                     "last_12h": fresh, "community_engagement": eng,
                     "top": sorted(got, key=lambda g: (g["age_h"], -g.get("engagement", 0)))[:8]})
        for g in got:
            g["keyword"] = kw
        items += got
    # X 공식 계정 감시 목록: API 키가 있을 때만 from: 검색
    for acc in cfg.get("x_accounts", []):
        items += [dict(x, keyword=f"@{acc}") for x in x_recent(f"from:{acc}", window)]
    seen, heads = set(), []
    for g in sorted(items, key=lambda g: (g["age_h"], -g.get("engagement", 0))):
        k = re.sub(r"\W+", "", g["title"].lower())[:60]
        if k and k not in seen:
            seen.add(k)
            heads.append(g)
    rows.sort(key=lambda r: r["score"], reverse=True)
    return {"generated": datetime.now(timezone.utc).isoformat(), "window_hours": window,
            "keywords": rows, "headlines": heads[: int(cfg.get("max_headlines", 80))]}
