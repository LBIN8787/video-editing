"""유명 인물 인사이트·인터뷰 해설 영상 조사 (2026-11-20 사용자: "드라켄밀러 인터뷰 영상같이 여러 인사이트에 관해서 처럼
유명인사들의 인사이트나 인터뷰나 발언 인사이트 등을 다루는게 조회수가 높더라구여").

방법: '이름 + 인터뷰/조언/경고/인사이트' 검색으로 해설 영상을 모으고, 그 영상을 올린 채널의 최근 영상 중앙값과 비교(배수 x).
같은 채널 안에서 이런 편이 평소보다 잘 되는지 본다. 원자료 .cache/insight/<날짜>/ (타 채널 자료라 커밋 안 함). 요약 docs/55 §5.

    python scripts/insight_research.py
"""
from __future__ import annotations

import concurrent.futures as cf
import datetime as dt
import json
import re
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from ytflow import yt  # noqa: E402

PEOPLE = ["드러켄밀러", "워런 버핏", "하워드 막스", "레이 달리오", "찰리 멍거", "피터 린치", "마이클 버리", "캐시 우드", "빌 애크먼",
          "젠슨 황", "일론 머스크", "샘 올트먼", "리사 수", "손정의", "빌 게이츠", "제이미 다이먼", "켄 그리핀", "짐 로저스"]
KINDS = ["인터뷰", "조언", "경고", "인사이트"]
BROADCAST = re.compile(r"KBS|MBC|SBS|EBS|tvN|JTBC|YTN|채널A|MBN|TV조선|한국경제TV|매일경제|연합뉴스|머니투데이|SBS Biz|서울경제|이데일리|조선일보|중앙일보|한겨레|경향|뉴스")
INS = re.compile(r"인터뷰|대담|강연|연설|조언|경고|말했|말하는|말한|발언|인사이트|원칙|철학|비밀|한마디|편지|서한|예언|전망|규칙|교훈|마인드|생각")


def search(q):
    try:
        return [e for e in (yt.flat_playlist(f"ytsearch30:{q}", 30).get("entries") or []) if e.get("id")]
    except Exception:
        return []


def channel_median(cid):
    try:
        j = yt.flat_playlist(f"https://www.youtube.com/channel/{cid}/videos", 120)
    except Exception:
        return None, None
    vv = [e.get("view_count") or 0 for e in j.get("entries") or [] if (e.get("duration") or 0) >= 180 and e.get("view_count")]
    return (statistics.median(vv) if len(vv) >= 15 else None), j.get("channel")


def main():
    out = ROOT / ".cache" / "insight" / dt.date.today().isoformat()
    out.mkdir(parents=True, exist_ok=True)
    qs = [f"{p} {k}" for p in PEOPLE for k in KINDS[:2]]
    with cf.ThreadPoolExecutor(6) as ex:
        res = list(ex.map(search, qs))
    vids = {}
    for q, es in zip(qs, res):
        person = q.rsplit(" ", 1)[0]
        for e in es:
            t, ch = e.get("title") or "", e.get("channel") or ""
            if person.split()[-1] not in t or BROADCAST.search(ch) or (e.get("duration") or 0) < 180:
                continue
            vids.setdefault(e["id"], {"id": e["id"], "title": t, "channel": ch, "cid": e.get("channel_id"), "views": e.get("view_count") or 0,
                                      "person": person})
    cids = {v["cid"] for v in vids.values() if v["cid"]}
    with cf.ThreadPoolExecutor(6) as ex:
        meds = dict(zip(cids, ex.map(channel_median, cids)))
    rows = []
    for v in vids.values():
        med = (meds.get(v["cid"]) or (None, None))[0]
        if med:
            v["x"] = round(v["views"] / med, 2)
            v["insight_word"] = bool(INS.search(v["title"]))
            rows.append(v)
    (out / "videos.json").write_text(json.dumps(rows, ensure_ascii=False, indent=0), encoding="utf-8")

    def S(sel):
        xs = [r["x"] for r in sel]
        return {"n": len(xs), "median_x": round(statistics.median(xs), 2) if xs else None,
                "hit_rate": round(sum(x >= 3 for x in xs) / len(xs), 3) if xs else None,
                "low_rate": round(sum(x <= 0.5 for x in xs) / len(xs), 3) if xs else None}
    summ = {"all": S(rows), "channels": len({r["cid"] for r in rows}),
            "by_person": {p: S([r for r in rows if r["person"] == p]) for p in PEOPLE},
            "insight_word": S([r for r in rows if r["insight_word"]]), "no_insight_word": S([r for r in rows if not r["insight_word"]])}
    (out / "summary.json").write_text(json.dumps(summ, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in summ.items() if k != "by_person"}, ensure_ascii=False))
    for p, s in sorted(summ["by_person"].items(), key=lambda kv: -(kv[1]["median_x"] or 0)):
        print(f"  {p:8} n={s['n']:3} 중앙 {s['median_x']} 터짐 {s['hit_rate']} 안됨 {s['low_rate']}")
    for r in sorted(rows, key=lambda r: -r["x"])[:20]:
        print(f"  {r['x']:>6} {r['channel'][:14]} | {r['title'][:80]}")
    print(out)


if __name__ == "__main__":
    main()
