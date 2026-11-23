"""조회수 높은 썸네일 조사 (2026-11-19 사용자: "조회수가 높은 썸네일들을 조사해주세요").

방법: 분야 검색 → 개인 채널 → 채널별 최근 영상 → 같은 채널 안에서 '터진 영상'(중앙값 3배+)과
'안 된 영상'(0.5배 이하) 썸네일을 비교 (채널 크기·구독자 차이를 지움).
원자료·썸네일 이미지는 .cache/thumbs/<날짜>/ (타 채널 자료라 커밋 안 함).

    python scripts/thumb_research.py [--per 60] [--top 18]
"""
import argparse, collections, concurrent.futures as cf, datetime as dt, json, re, statistics, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from ytflow import yt  # noqa: E402

QUERIES = {
    "시장": ["미국 증시 마감", "엔비디아 주가 분석", "반도체 주식 전망", "코스피 전망", "삼성전자 SK하이닉스 주가", "경제 뉴스 해설", "금리 인하 주식", "AI 버블"],
    "경제 해설": ["경제 이야기 쉽게", "돈의 흐름", "기업 분석 다큐", "부동산 경제 위기"],
}
EXTRA = {  # 시장 채널 벤치마크로 직접 넣는 개인 채널 (검색만으로는 안 걸릴 수 있음)
    "슈카월드": "UCsJ6RuBiTVWRX156FVbeaGg", "소수몽키": "UCC3yfxS5qC6PCwDzetUuEWg", "815Money talk": "UCCG6BEYjfQMGzypJw2EJCDQ",
    "김작가 TV": "UCvil4OAt-zShzkKHsg9EQAw", "이효석아카데미": "UCxvdCnvGODDyuvnELnLkQWw", "Six Sigma | 식스시그마": "UCb55ivT0IMLtiAcVu3B-vKQ",
    "미국주식으로 은퇴하기 - 미주은": "UCNnwmqZOxSuOiF3_c7mAGWA", "월가아재의 과학적 투자": "UCpqD9_OJNtF6suPpi6mOQCQ", "머니크루 MoneyCrew": "UCkQEj8inWqrv1AIETIiB-bQ",
}
EXCLUDE = re.compile(r"LG에너지솔루션|비디오머그|강지영")
BROADCAST = re.compile(r"KBS|MBC|SBS|EBS|tvN|JTBC|YTN|채널A|MBN|TV조선|한국경제TV|매일경제|연합뉴스|머니투데이|SBS Biz|서울경제|이데일리|조선일보|중앙일보|한겨레|경향|뉴스")


def search(q):
    try:
        return yt.flat_playlist(f"ytsearch40:{q}", 40).get("entries", []) or []
    except Exception:
        return []


def channel(cid, n):
    try:
        j = yt.flat_playlist(f"https://www.youtube.com/channel/{cid}/videos", n)
    except Exception:
        return {}
    vids = [{"id": e.get("id"), "title": e.get("title"), "views": e.get("view_count") or 0, "dur": e.get("duration") or 0}
            for e in j.get("entries", []) or [] if e.get("id")]
    vids = [v for v in vids if v["dur"] >= 180]          # 쇼츠 제외
    vv = [v["views"] for v in vids if v["views"]]
    med = statistics.median(vv) if len(vv) >= 10 else 0
    for v in vids:
        v["x"] = round(v["views"] / med, 2) if med else 0
    return {"name": j.get("channel"), "subs": j.get("channel_follower_count"), "median": med, "videos": vids}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--per", type=int, default=60); ap.add_argument("--top", type=int, default=18)
    a = ap.parse_args()
    out = ROOT / ".cache" / "thumbs" / dt.date.today().isoformat(); (out / "img").mkdir(parents=True, exist_ok=True)
    jobs = [(c, q) for c, qs in QUERIES.items() for q in qs]
    with cf.ThreadPoolExecutor(6) as ex:
        res = dict(zip(jobs, ex.map(lambda j: search(j[1]), jobs)))
    ch = collections.defaultdict(lambda: {"views": 0, "n": 0, "id": None, "cat": set()})
    for (cat, _), es in res.items():
        for e in es:
            nm = e.get("channel") or ""
            if not nm or BROADCAST.search(nm) or EXCLUDE.search(nm) or not e.get("view_count"):
                continue
            c = ch[nm]; c["views"] += e["view_count"]; c["n"] += 1; c["id"] = e.get("channel_id"); c["cat"].add(cat)
    pick = sorted(ch.items(), key=lambda kv: -kv[1]["views"])[: a.top]
    have = {n for n, _ in pick}
    for nm, cid in EXTRA.items():
        if nm not in have:
            ch[nm]["id"] = cid; ch[nm]["cat"].add("시장(직접)"); pick.append((nm, ch[nm]))
    with cf.ThreadPoolExecutor(6) as ex:
        chans = dict(zip([n for n, _ in pick], ex.map(lambda kv: channel(kv[1]["id"], a.per), pick)))
    rows = []
    for nm, c in chans.items():
        for v in c.get("videos", []):
            if not c.get("median"):
                continue
            grp = "hit" if v["x"] >= 3 else "low" if v["x"] <= 0.5 else "mid"
            rows.append({**v, "channel": nm, "subs": c.get("subs"), "median": c["median"], "group": grp,
                         "cat": sorted(ch[nm]["cat"])})
    (out / "videos.json").write_text(json.dumps(rows, ensure_ascii=False, indent=0), encoding="utf-8")
    sel = [r for r in rows if r["group"] in ("hit", "low")]
    def get(r):
        p = out / "img" / f"{r['id']}.jpg"
        if not p.exists():
            subprocess.run(["curl", "-sfL", "-o", str(p), f"https://i.ytimg.com/vi/{r['id']}/hqdefault.jpg"])
    with cf.ThreadPoolExecutor(8) as ex:
        list(ex.map(get, sel))
    print(out, "채널", len(chans), "영상", len(rows), "hit", sum(r["group"] == "hit" for r in rows), "low", sum(r["group"] == "low" for r in rows))
    for nm, c in chans.items():
        print(f"  {nm} · 구독 {c.get('subs')} · 중앙 {c.get('median')} · 영상 {len(c.get('videos', []))}")


if __name__ == "__main__":
    main()
