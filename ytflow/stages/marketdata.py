"""시세 데이터 — 그래프에 실제 가격을 쓰기 위해.

기본 소스: Yahoo Finance 차트 데이터(공개 엔드포인트, 비공식 API). 미국(NVDA)·한국(005930.KS, 000660.KS)
지수(^IXIC, ^GSPC, ^SOX, ^KS11) 모두 된다. 응답은 프로젝트 01_research/prices/ 에 캐시해 재현 가능하게 둔다.
다른 소스로 바꾸려면 fetch() 만 교체하면 된다 (반환 형식: [{date, open, high, low, close}]).
주의: 비공식 엔드포인트라 형식이 바뀌거나 막힐 수 있다. 막히면 카드의 items(수동 값)로 대체된다.
"""
from __future__ import annotations

import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

INTERVAL = {"5d": "1h", "1mo": "1d", "3mo": "1d", "6mo": "1d", "1y": "1wk", "2y": "1wk", "5y": "1mo", "10y": "1mo"}


def fetch(ticker: str, period: str = "6mo", cache_dir: Path | None = None) -> list[dict]:
    period = period if period in INTERVAL else "6mo"
    cache = cache_dir / f"{ticker.replace('^', 'IDX_')}_{period}.json" if cache_dir else None
    if cache and cache.exists():
        return json.loads(cache.read_text(encoding="utf-8"))
    url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.request.quote(ticker)}"
           f"?range={period}&interval={INTERVAL[period]}")
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 ytflow"}), timeout=20) as r:
            res = json.loads(r.read())["chart"]["result"][0]
    except Exception as e:
        print(f"  ! 시세 실패 {ticker}: {str(e)[:80]}")
        return []
    q = res["indicators"]["quote"][0]
    rows = []
    for i, ts in enumerate(res.get("timestamp") or []):
        o, h, l, c = (q.get(k, [None])[i] for k in ("open", "high", "low", "close"))
        if None in (o, h, l, c):
            continue
        rows.append({"date": datetime.fromtimestamp(ts, timezone.utc).strftime("%Y-%m-%d"),
                     "open": round(o, 2), "high": round(h, 2), "low": round(l, 2), "close": round(c, 2)})
    meta = res.get("meta", {})
    if rows and cache:
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")
        (cache.with_suffix(".meta.json")).write_text(json.dumps(
            {"ticker": ticker, "currency": meta.get("currency"), "source": "Yahoo Finance chart",
             "fetched": datetime.now(timezone.utc).isoformat()}, ensure_ascii=False), encoding="utf-8")
    return rows


def currency(ticker: str, cache_dir: Path | None = None) -> str:
    if cache_dir:
        for f in cache_dir.glob(f"{ticker.replace('^', 'IDX_')}_*.meta.json"):
            return json.loads(f.read_text()).get("currency") or ""
    return "KRW" if ticker.endswith((".KS", ".KQ")) else "USD"


def fmt_price(v: float, cur: str) -> str:
    if cur == "KRW":
        return f"{v:,.0f}원"
    if cur in ("USD", ""):
        return f"${v:,.2f}" if v < 1000 else f"{v:,.0f}"
    return f"{v:,.2f}"
