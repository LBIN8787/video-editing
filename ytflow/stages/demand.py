"""수요 분석: 분야별 YouTube 검색 → 많이 걸린 개인 채널 → 채널별 최근 영상 아웃라이어.

    python -m ytflow demand [--channel ch-knowledge] [--top 25]

결과는 `.cache/demand/<날짜>/` 에 원자료(JSON, 타 채널 자료라 커밋 안 함)와
`summary.md`(채널 표 · 2배 이상 영상 · 길이·제목 유형별 배수)를 씁니다.
summary.md 를 보고 docs/10-knowledge-demand.md 와 channels/<id>/queue.md 를 갱신합니다.
아웃라이어 배수 = 조회수 ÷ 그 채널 최근 영상 조회수 중앙값.
"""
from __future__ import annotations

import collections
import concurrent.futures as cf
import datetime as dt
import json
import re
import statistics

from .. import config, yt

BROADCAST = re.compile(r"KBS|MBC|SBS|EBS|tvN|JTBC|YTN|채널A|MBN|TV조선|디글|Diggle|E채널|세바시")
PATTERNS = {
    "왜·이유": r"왜|이유|[Ww]hy|reason",
    "몰아보기·총정리": r"몰아|총정리|한 ?번에|요약|[Ss]ummar|[Bb]inge|Comprehensive|Overview",
    "~하면 생기는 일": r"생기는 일|하면 |If ",
    "충격·비밀": r"충격|정체|진짜|비밀|Shocking|Secret|[Tt]ruth",
    "순위·TOP": r"TOP|Top|순위|\d+가지",
    "전쟁·군사": r"전쟁|[Ww]ar|무기|군대|Military|Army",
}


def _search(q: str) -> list[dict]:
    try:
        return yt.flat_playlist(f"ytsearch40:{q}", 40).get("entries", []) or []
    except Exception:  # noqa: BLE001
        return []


def _channel(cid: str, n: int) -> dict:
    try:
        j = yt.flat_playlist(f"https://www.youtube.com/channel/{cid}/videos", n)
    except Exception:  # noqa: BLE001
        return {}
    vids = [{"title": e.get("title"), "views": e.get("view_count") or 0, "dur": e.get("duration") or 0, "id": e.get("id")}
            for e in j.get("entries", []) or []]
    v = [x["views"] for x in vids if x["views"]]
    med = statistics.median(v) if v else 0
    for x in vids:
        x["x"] = round(x["views"] / med, 2) if med else 0
    return {"subs": j.get("channel_follower_count"), "median": med, "videos": vids}


def run(channel_id: str = "ch-knowledge", top: int = 25) -> str:
    cfg = (config.channel(channel_id) or {}).get("demand", {})
    queries: dict = cfg.get("queries") or {"상식": ["우리가 몰랐던 상식"]}
    per = int(cfg.get("per_channel", 80))
    min_s = int(cfg.get("min_seconds", 180))
    out = config.CACHE_DIR / "demand" / dt.date.today().isoformat()
    out.mkdir(parents=True, exist_ok=True)

    jobs = [(cat, q) for cat, qs in queries.items() for q in qs]
    with cf.ThreadPoolExecutor(6) as ex:
        res = dict(zip(jobs, ex.map(lambda j: _search(j[1]), jobs)))
    (out / "search.json").write_text(json.dumps({f"{c}|{q}": v for (c, q), v in res.items()}, ensure_ascii=False), encoding="utf-8")
    ch = collections.defaultdict(lambda: {"views": 0, "n": 0, "cats": set(), "id": None})
    for (cat, _), es in res.items():
        for e in es:
            name = e.get("channel") or ""
            if not name or BROADCAST.search(name) or not e.get("view_count"):
                continue
            c = ch[name]
            c["views"] += e["view_count"]; c["n"] += 1; c["cats"].add(cat); c["id"] = e.get("channel_id")
    pick = sorted(ch.items(), key=lambda kv: -kv[1]["views"])[:top]
    with cf.ThreadPoolExecutor(6) as ex:
        chans = dict(zip([n for n, _ in pick], ex.map(lambda kv: _channel(kv[1]["id"], per), pick)))
    (out / "channels.json").write_text(json.dumps(chans, ensure_ascii=False), encoding="utf-8")

    lines = [f"# 수요 분석 {dt.date.today()} ({channel_id})", "", "| 채널 | 구독자 | 중앙 조회수 | 분야 |", "|---|---|---|---|"]
    for n, c in pick:
        d = chans.get(n) or {}
        lines.append(f"| {n} | {d.get('subs') or '?'} | {int(d.get('median') or 0):,} | {', '.join(sorted(c['cats']))} |")
    V = [dict(v, ch=n) for n, d in chans.items() if d for v in d["videos"] if v["dur"] >= min_s and v["views"]]
    lines += ["", "## 2배 이상 영상 (상위 60)", ""]
    for v in sorted([v for v in V if v["x"] >= 2], key=lambda v: -v["x"])[:60]:
        lines.append(f"- ×{v['x']} · {v['views']:,}회 · {v['dur'] // 60}분 · [{v['ch']}] {v['title']}")
    lines += ["", "## 유형별 배수 중앙값", "", "| 유형 | 영상 수 | 배수 중앙값 | 2배 이상 비율 |", "|---|---|---|---|"]
    groups = {"4~12분": lambda v: 240 <= v["dur"] < 720, "12~30분": lambda v: 720 <= v["dur"] < 1800, "30분 이상": lambda v: v["dur"] >= 1800}
    groups.update({k: (lambda v, p=p: re.search(p, v["title"] or "")) for k, p in PATTERNS.items()})
    for k, f in groups.items():
        xs = [v["x"] for v in V if f(v)]
        if xs:
            lines.append(f"| {k} | {len(xs)} | {statistics.median(xs):.2f} | {sum(x >= 2 for x in xs) / len(xs) * 100:.0f}% |")
    (out / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[demand] {out / 'summary.md'}")
    return str(out / "summary.md")
