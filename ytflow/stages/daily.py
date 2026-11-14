"""매일 시장·시사 브리핑의 주제 찾기 (v17, 사용자 요청 2026-11-12):
"주식·시사는 매일 실시간 분석이 중요 — 전날 주식시장을 보고 무슨 이슈·보고서·전망이 시장을 크게 움직였는지 분석하고,
 이를 바탕으로 설명해 주는 방식으로."

    python -m ytflow daily                      # 시장: 전날(가장 최근 거래일) 기준
    python -m ytflow daily --brand issues       # 시사: 전날 가장 크게 다뤄진 이슈
    python -m ytflow daily --project <이름>     # 결과를 그 프로젝트 01_research 에 (없으면 새로 만듦)

시장 순서: ① 지수·환율·금리·원자재 마감 → ② 업종(미국 섹터 ETF) → ③ 대형주 큰 움직임(±2% 이상, 지수 대비)
         → ④ 움직임마다 뉴스(국문·영문) → 원인 종류 분류: 이슈 · 보고서(증권사·기관) · 전망(가이던스·연준·지표) · 실적
         → ⑤ '시장을 크게 움직인 이야기' 상위 3개 = 움직임 크기 × 보도량 → daily_brief.md / daily_brief.json
여기서 나온 것은 **후보와 단서**입니다. 원인은 반드시 1차 출처(회사 발표·공시·보고서 원문·당국 발표)로 확인한 뒤 대본에 씁니다.
시세: Yahoo Finance 차트(비공식, marketdata.py). 뉴스: Google News RSS. 둘 다 키 불필요.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .. import config

KST = timezone(timedelta(hours=9))

INDICES = [("^GSPC", "S&P 500", "us"), ("^IXIC", "나스닥", "us"), ("^DJI", "다우", "us"), ("^SOX", "필라델피아 반도체", "us"),
           ("^VIX", "VIX(변동성)", "us"), ("^KS11", "코스피", "kr"), ("^KQ11", "코스닥", "kr"),
           ("KRW=X", "원/달러 환율", "fx"), ("^TNX", "미 10년물 금리", "rate"), ("CL=F", "WTI 유가", "cmd"),
           ("GC=F", "금", "cmd"), ("BTC-USD", "비트코인", "crypto")]
SECTORS = [("XLK", "기술"), ("XLC", "커뮤니케이션"), ("XLY", "경기소비재"), ("XLF", "금융"), ("XLV", "헬스케어"),
           ("XLI", "산업재"), ("XLE", "에너지"), ("XLP", "필수소비재"), ("XLU", "유틸리티"), ("XLB", "소재"), ("XLRE", "부동산")]
STOCKS = [("AAPL", "애플", "Apple", "^GSPC"), ("MSFT", "마이크로소프트", "Microsoft", "^GSPC"), ("NVDA", "엔비디아", "Nvidia", "^SOX"),
          ("GOOGL", "알파벳(구글)", "Alphabet", "^GSPC"), ("AMZN", "아마존", "Amazon", "^GSPC"), ("META", "메타", "Meta", "^GSPC"),
          ("TSLA", "테슬라", "Tesla", "^GSPC"), ("AVGO", "브로드컴", "Broadcom", "^SOX"), ("TSM", "TSMC", "TSMC", "^SOX"),
          ("AMD", "AMD", "AMD", "^SOX"), ("MU", "마이크론", "Micron", "^SOX"), ("NFLX", "넷플릭스", "Netflix", "^GSPC"),
          ("PLTR", "팔란티어", "Palantir", "^GSPC"), ("ORCL", "오라클", "Oracle", "^GSPC"), ("JPM", "JP모건", "JPMorgan", "^GSPC"),
          ("LLY", "일라이릴리", "Eli Lilly", "^GSPC"), ("XOM", "엑슨모빌", "Exxon Mobil", "^GSPC"),
          ("005930.KS", "삼성전자", "Samsung Electronics", "^KS11"), ("000660.KS", "SK하이닉스", "SK Hynix", "^KS11"),
          ("373220.KS", "LG에너지솔루션", "LG Energy Solution", "^KS11"), ("207940.KS", "삼성바이오로직스", "Samsung Biologics", "^KS11"),
          ("005380.KS", "현대차", "Hyundai Motor", "^KS11"), ("035420.KS", "NAVER", "Naver", "^KS11"),
          ("035720.KS", "카카오", "Kakao", "^KS11"), ("012450.KS", "한화에어로스페이스", "Hanwha Aerospace", "^KS11"),
          ("068270.KS", "셀트리온", "Celltrion", "^KS11"), ("105560.KS", "KB금융", "KB Financial", "^KS11")]
MARKET_NEWS = [("뉴욕증시 마감", "ko"), ("코스피 마감", "ko"), ("stock market today close", "en"),
               ("증권사 리포트 목표가", "ko"), ("analyst upgrade downgrade price target", "en"),
               ("연준 금리 전망", "ko"), ("Fed rate outlook", "en"), ("실적 발표 가이던스", "ko")]
DRIVERS = {   # 원인 종류: 제목 낱말로 1차 분류 (사람이 확인)
    "보고서": ["리포트", "목표가", "투자의견", "보고서", "애널리스트", "호평", "상향", "하향", "매수 의견", "커버리지", "upgrade", "downgrade", "price target", "analyst", "rating", "initiates"],
    "전망": ["전망", "가이던스", "guidance", "outlook", "forecast", "연준", "fed", "fomc", "cpi", "물가", "금리", "고용", "jobs"],
    "실적": ["실적", "어닝", "매출", "영업이익", "earnings", "revenue", "quarter", "분기", "eps"],
}


def _closed(ticker: str, date: str) -> bool:
    """그 날짜의 장이 이미 끝났나 (장중 값은 '마감'이 아니므로 뺌). 한국 15:30 KST, 미국 16:00 ET(≈21:00 UTC), 그 밖은 하루 지나면."""
    now_utc = datetime.now(timezone.utc)
    if ticker.endswith((".KS", ".KQ")) or ticker in ("^KS11", "^KQ11"):
        end = datetime.fromisoformat(date).replace(hour=6, minute=30, tzinfo=timezone.utc)       # 15:30 KST
    elif ticker.endswith(("=X", "=F", "-USD")):
        end = datetime.fromisoformat(date).replace(tzinfo=timezone.utc) + timedelta(days=1)
    else:
        end = datetime.fromisoformat(date).replace(hour=21, minute=15, tzinfo=timezone.utc)      # 16:00 ET (+여유)
    return now_utc >= end


def _pct(rows: list[dict], day: str, ticker: str = "") -> dict | None:
    """day(YYYY-MM-DD) 이하, 장이 끝난 가장 최근 거래일의 종가와 그 전 거래일 대비 등락 (시장마다 자기 날짜)."""
    rows = [r for r in rows if r["date"] <= day and (not ticker or _closed(ticker, r["date"]))]
    if len(rows) < 2:
        return None
    a, b = rows[-2], rows[-1]
    return {"date": b["date"], "close": b["close"], "prev": a["close"], "pct": round((b["close"] / a["close"] - 1) * 100, 2)}


def driver(title: str) -> str:
    t = title.lower()
    for k, words in DRIVERS.items():
        if any(w in t for w in words):
            return k
    return "이슈"


def _news(q: str, lang: str, hours: int = 36) -> list[dict]:
    from .trends import google_news
    try:
        return google_news(q, lang, hours)[:12]
    except Exception as e:  # noqa: BLE001
        print(f"  ! 뉴스 실패 {q}: {str(e)[:60]}")
        return []


def market(day: str, cache: Path) -> dict:
    from .marketdata import fetch
    cache.mkdir(parents=True, exist_ok=True)
    out = {"brand": "market", "as_of": day, "indices": [], "sectors": [], "movers": [], "stories": [], "market_news": []}
    px = {}
    for t, name, kind in INDICES:
        p = _pct(fetch(t, "1mo", cache), day, t)
        if p:
            px[t] = p
            out["indices"].append(dict(p, ticker=t, name=name, kind=kind))
    for t, name in SECTORS:
        p = _pct(fetch(t, "1mo", cache), day, t)
        if p:
            out["sectors"].append(dict(p, ticker=t, name=name))
    out["sectors"].sort(key=lambda x: x["pct"])
    for t, ko, en, bench in STOCKS:
        p = _pct(fetch(t, "1mo", cache), day, t)
        if not p:
            continue
        bp = px.get(bench, {})
        same = bp.get("date") == p["date"]   # 기준 지수와 같은 날짜일 때만 '지수 대비' (지수 갱신이 늦으면 비교하지 않음)
        rel = round(p["pct"] - bp.get("pct", 0.0), 2) if same else 0.0
        out["movers"].append(dict(p, ticker=t, name=ko, en=en, bench=bench, rel=rel, rel_ok=same))
    out["movers"].sort(key=lambda x: -abs(x["pct"]))
    big = [m for m in out["movers"] if abs(m["pct"]) >= 2.0][:6] or out["movers"][:3]
    for m in big:   # 움직임마다 뉴스 → 원인 종류
        items = _news(f"{m['name']} 주가", "ko") + _news(f"{m['en']} stock", "en")
        seen, news = set(), []
        for n in items:
            key = re.sub(r"\W+", "", n["title"])[:30]
            if key in seen:
                continue
            seen.add(key)
            news.append({"title": n["title"], "source": n["source"], "url": n["url"], "published": n["published"], "driver": driver(n["title"])})
        kinds = Counter(n["driver"] for n in news)
        m["news"] = news[:10]
        m["driver_counts"] = dict(kinds)
        m["score"] = round(abs(m["pct"]) * (1 + len(news) / 5) * (1.3 if abs(m["rel"]) >= 2 else 1.0), 2)
    for q, lang in MARKET_NEWS:
        for n in _news(q, lang)[:6]:
            out["market_news"].append({"q": q, "title": n["title"], "source": n["source"], "url": n["url"], "driver": driver(n["title"])})
    # 시장 전체 뉴스에서 되풀이되는 고유 낱말 = 그날의 주제 (예: 코어위브 실적, 엔비디아 CEO) — 관심 종목 밖의 이야기도 잡기
    stop = {"뉴욕증시", "증시", "마감", "상승", "하락", "코스피", "코스닥", "나스닥", "다우", "일제히", "속보", "오늘", "종합", "리포트",
            "브리핑", "목표가", "투자증권", "증권", "글로벌마켓", "Stock", "Market", "Today", "News", "and", "the", "for", "stock", "market",
            "with", "by", "new", "price", "target", "to", "of", "in", "on", "as", "after", "its", "from", "at", "is", "are", "today"}
    words = Counter(w for n in out["market_news"] for w in set(re.findall(r"[가-힣A-Za-z]{2,}", n["title"])) if w not in stop)
    out["themes"] = [{"word": w, "count": c} for w, c in words.most_common(12) if c >= 3]
    ranked = sorted([m for m in big if m.get("news")], key=lambda x: -x["score"])[:3]
    sox = next((x["pct"] for x in out["indices"] if x["ticker"] == "^SOX"), 0.0)
    for m in ranked:
        lead = max(m["driver_counts"], key=m["driver_counts"].get) if m["driver_counts"] else "이슈"
        alone = abs(m["rel"]) >= 2
        # 브리핑이냐 심층이냐 (docs/23 §2): 신호 둘 이상이면 심층 후보 — 최종 판단은 사람
        sig = []
        if len([k for k, v in m["driver_counts"].items() if k != "이슈" and v >= 3]) >= 1 and m["driver_counts"].get("이슈", 0) >= 5:
            sig.append("원인 종류 여러 갈래")
        if abs(m["pct"]) >= 10 or (abs(sox) >= 4 and m["bench"] == "^SOX" and abs(m["rel"]) >= 3):
            sig.append("시장·업종을 크게 움직임")
        if m["driver_counts"].get("실적", 0) + m["driver_counts"].get("전망", 0) >= 4:
            sig.append("실적·가이던스(어닝콜) 설명이 핵심")
        if (m["ticker"].endswith(".KS") and abs(m["pct"]) >= 5) or (m["ticker"] in ("NVDA", "MU", "TSM") and abs(m["pct"]) >= 5):
            sig.append("한국 시장으로 이어지는 고리")
        out["stories"].append({
            "ticker": m["ticker"], "name": m["name"], "pct": m["pct"], "rel": m["rel"], "bench": m["bench"], "driver": lead,
            "angle": ("업종·지수와 따로 움직임 → 회사만의 이유" if alone else "업종·지수와 같이 움직임 → 시장 전체의 이유"),
            "question": f"{m['name']}는 왜 {'올랐' if m['pct'] > 0 else '떨어졌'}을까?",
            "headlines": [n["title"] for n in m["news"][:4]], "check_first": "회사 발표·공시·보고서 원문·당국 발표로 원인 확인",
            "depth": "심층 후보" if len(sig) >= 2 else "브리핑", "depth_why": sig})
    return out


def issues(day: str) -> dict:
    """전날 가장 크게 다뤄진 이슈: 국내 주요 뉴스 RSS + 분야별 검색 → 제목 낱말 겹침으로 묶고 언론사 수로 순위."""
    from .trends import _get
    import xml.etree.ElementTree as ET
    items = []
    for url in ("https://news.google.com/rss?hl=ko&gl=KR&ceid=KR:ko",
                "https://news.google.com/rss/headlines/section/topic/NATION?hl=ko&gl=KR&ceid=KR:ko",
                "https://news.google.com/rss/headlines/section/topic/WORLD?hl=ko&gl=KR&ceid=KR:ko"):
        raw = _get(url)
        if not raw:
            continue
        for it in ET.fromstring(raw).iter("item"):
            src = it.findtext("source") or ""
            t = re.sub(rf"\s+-\s+{re.escape(src)}$", "", it.findtext("title") or "")
            items.append({"title": t, "source": src, "url": it.findtext("link")})
    def toks(t):
        return {w for w in re.findall(r"[가-힣A-Za-z0-9]{2,}", t) if w not in {"속보", "단독", "종합", "오늘", "이번"}}
    groups = []
    for it in items:
        tk = toks(it["title"])
        for g in groups:
            if len(tk & g["tokens"]) >= 2:
                g["items"].append(it)
                g["tokens"] |= tk
                break
        else:
            groups.append({"tokens": set(tk), "items": [it]})
    for g in groups:
        g["sources"] = len({i["source"] for i in g["items"]})
    groups.sort(key=lambda g: -g["sources"])
    stories = [{"headline": g["items"][0]["title"], "sources": g["sources"], "headlines": [i["title"] for i in g["items"][:5]],
                "urls": [i["url"] for i in g["items"][:5]], "check_first": "당국·기관 발표 원문, 양쪽 입장, 기준 시각"} for g in groups[:8]]
    return {"brand": "issues", "as_of": day, "stories": stories}


def last_session(now: datetime | None = None) -> str:
    """한국 아침 기준 '전날': 가장 최근에 끝난 거래일 (주말이면 금요일)."""
    d = (now or datetime.now(KST)).date() - timedelta(days=1)
    while d.weekday() >= 5:
        d -= timedelta(days=1)
    return d.isoformat()


def to_md(b: dict) -> str:
    if b["brand"] == "issues":
        L = [f"# 전날 이슈 브리핑 후보 — {b['as_of']} 기준", "", "| 순위 | 이슈 | 다룬 언론사 수 |", "|---|---|---|"]
        L += [f"| {i} | {s['headline']} | {s['sources']} |" for i, s in enumerate(b["stories"], 1)]
        for i, s in enumerate(b["stories"][:3], 1):
            L += ["", f"## {i}. {s['headline']}", *[f"- {h}" for h in s["headlines"]], f"- 먼저 확인: {s['check_first']}"]
        return "\n".join(L) + "\n"
    f = lambda x: f"{x['pct']:+.2f}%"
    L = [f"# 전날 시장 브리핑 후보 — {b['as_of']} 마감 기준", "",
         "> 자동 수집한 **후보와 단서**입니다. 원인은 1차 출처(회사 발표·공시·보고서 원문·당국 발표)로 확인한 뒤 대본에 씁니다. 투자 권유 금지.", "",
         "## ① 지수·환율·금리·원자재", "| 항목 | 종가 | 등락 | 날짜 |", "|---|---|---|---|"]
    latest = {}
    for x in b["indices"]:
        latest[x["kind"]] = max(latest.get(x["kind"], ""), x["date"])
    for m in b.get("movers", []):   # 종목 날짜가 지수보다 앞서면 지수 갱신이 늦은 것 (예: 2026-11-13 아침 코스피)
        k = "kr" if m["ticker"].endswith((".KS", ".KQ")) else "us"
        latest[k] = max(latest.get(k, ""), m["date"])
    L += [f"| {x['name']} | {x['close']:,} | {f(x)} | {x['date']}{' ⚠️ 원본 갱신 늦음 — 거래소·기사로 확인' if x['date'] < latest[x['kind']] else ''} |"
          for x in b["indices"]]
    L += ["", "## ② 업종 (미국 섹터 ETF, 약한 순)", "| 업종 | 등락 |", "|---|---|"] + [f"| {x['name']} ({x['ticker']}) | {f(x)} |" for x in b["sectors"]]
    L += ["", "## ③ 대형주 큰 움직임 (지수 대비 = 회사만의 움직임)", "| 종목 | 등락 | 기준 지수 대비 | 원인 종류(뉴스 제목 분류) |", "|---|---|---|---|"]
    L += [f"| {m['name']} ({m['ticker']}) | {f(m)} | {(format(m['rel'], '+.2f') + '%p') if m.get('rel_ok', True) else '— (지수 갱신 늦음)'} ({m['bench']}) | {', '.join(f'{k} {v}' for k, v in (m.get('driver_counts') or {}).items())} |"
          for m in b["movers"][:12]]
    L += ["", "## ④ 시장을 크게 움직인 이야기 — 상위 3개 (움직임 × 보도량)"]
    for i, s in enumerate(b["stories"], 1):
        L += ["", f"### {i}. {s['name']} {s['pct']:+.2f}% — 원인 종류: **{s['driver']}** · **{s.get('depth', '브리핑')}**{' (' + ', '.join(s.get('depth_why') or []) + ')' if s.get('depth_why') else ''}",
              f"- 각도: {s['angle']}", f"- 질문: {s['question']}",
              *[f"- {h}" for h in s["headlines"]], f"- 먼저 확인: {s['check_first']}"]
    L += ["", "## ⑤ 그날의 주제어 (시장 전체 뉴스에 3번 이상) — 관심 종목 밖의 이야기도 여기서", ", ".join(f"{t['word']}({t['count']})" for t in b.get("themes", [])) or "(없음)"]
    L += ["", "## ⑥ 시장 전체 뉴스 (보고서·전망·마감 시황)"]
    L += [f"- [{n['driver']}] {n['title']} — {n['source']}" for n in b["market_news"][:24]]
    return "\n".join(L) + "\n"


def run(brand: str = "market", day: str = "", project: str = "") -> Path:
    from ..project import Project
    day = day or datetime.now(KST).date().isoformat()   # 시장마다 '장이 끝난 가장 최근 거래일'을 씀 (_closed)
    if project:
        root = config.ROOT / "projects" / project
        if not root.exists():
            (root / "01_research").mkdir(parents=True)
            ch = "ch-market-daily" if brand == "market" else "ch-issues-daily"
            (root / "edit.yaml").write_text(f"# 매일 브리핑 ({brand}) — manual v17\nedit:\n  style: hybrid\n  style_ref: hybrid\n  family: source\n"
                                            f"channel: {ch}\nformat: longform\n", encoding="utf-8")
            (root / "state.json").write_text(json.dumps({"name": project, "created": datetime.now(KST).isoformat(timespec="seconds"),
                                                         "done": [], "approved": []}, ensure_ascii=False, indent=2), encoding="utf-8")
        rdir = Project.open(project).dir("research")
    else:
        rdir = Path(config.CACHE_DIR) / "daily" / f"{brand}_{day}"
    rdir.mkdir(parents=True, exist_ok=True)
    print(f"[daily] {brand} · {day} 기준")
    b = market(day, rdir / "prices") if brand == "market" else issues(day)
    (rdir / "daily_brief.json").write_text(json.dumps(b, ensure_ascii=False, indent=1), encoding="utf-8")
    (rdir / "daily_brief.md").write_text(to_md(b), encoding="utf-8")
    print(f"[daily] → {rdir / 'daily_brief.md'}")
    if brand == "market":   # SAVE(오선) 소식은 기본 확인 (2026-11-14 사용자) — 사람이 앱/웹에서 보고 표를 채움 (savecheck.py)
        from . import savecheck
        sp = savecheck.ensure(rdir, day)
        st = savecheck.read(rdir)
        print(f"[daily] SAVE 확인 표 → {sp} · 상태: {st['status']}" + ("" if st["done"] else " — 앱/웹에서 확인해 채우세요 (자동 수집 안 됨)"))
    for i, s in enumerate(b["stories"][:3], 1):
        print(f"  {i}. {s.get('name', s.get('headline'))} {s.get('pct', '')} {s.get('driver', '')}")
    return rdir / "daily_brief.md"
