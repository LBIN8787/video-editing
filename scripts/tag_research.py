"""어떤 태그가 조회수가 잘 나오나 (2026-11-22 사용자: "어떤 태그가 조회수가 잘나오는지 분석하세요 이후 이를 참조하여 태그를 달고 수정 할 수 있도록 하세요").

방법 (thumb_research 와 같은 틀):
  1) 시장·경제 개인 채널 모으기 (벤치마크 + 분야 검색, 방송사 제외)
  2) 채널마다 최근 긴 영상 N개 → 채널 중앙값 대비 배수 x (채널 크기 차이를 지움)
  3) 영상 보기 페이지의 공개 태그(videoDetails.keywords)를 읽음 — 키 없음, 차단·봇 확인이 뜨면 멈춤(우회하지 않음)
  4) 태그(띄어쓰기·대소문자 무시)마다: 쓴 영상 수·채널 수·배수 중앙값·'터진 영상'(x≥2) 비율 → data/tag_stats.json
     + 태그 개수·제목과 겹침·채널 이름 태그 같은 '태그 습관'과 배수의 관계
원자료(타 채널 영상 목록)는 .cache/tags/<날짜>/ (커밋 안 함). 결과 요약만 data/tag_stats.json · docs/58-tag-research.md.

    python scripts/tag_research.py [--per 60] [--workers 6]
주의: 태그는 주제를 따라가므로 '이 태그를 달면 조회수가 오른다'는 인과가 아니다. 같은 주제 안에서 어떤 말로 다느냐를 고를 때 참고.
"""
import argparse, collections, concurrent.futures as cf, datetime as dt, json, math, re, statistics, sys, time, urllib.error, urllib.request
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
from thumb_research import EXTRA, BROADCAST, EXCLUDE, channel, search  # noqa: E402

QUERIES = ["미국 증시 마감", "엔비디아 주가 분석", "반도체 주식 전망", "삼성전자 SK하이닉스 주가", "코스피 전망", "AI 버블", "금리 인하 주식",
           "경제 뉴스 해설", "메모리 반도체 전망", "테슬라 주가", "미국 주식 전망", "환율 전망"]
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36",
      "Accept-Language": "ko-KR,ko;q=0.9", "Cookie": "CONSENT=YES+1"}
BLOCKED = {"n": 0}
CACHE_F = ROOT / ".cache" / "tags" / "keywords.json"   # 영상별 태그 캐시 (이어 하기)
CACHE = json.loads(CACHE_F.read_text(encoding="utf-8")) if CACHE_F.exists() else {}


def norm(t: str) -> str:
    return re.sub(r"\s+", "", t).lower()


def keywords(vid: str) -> list | None:
    if BLOCKED["n"] >= 5:
        return None
    if vid in CACHE:
        return CACHE[vid]
    try:
        html = urllib.request.urlopen(urllib.request.Request(f"https://www.youtube.com/watch?v={vid}&hl=ko", headers=UA), timeout=15).read().decode("utf-8", "ignore")
    except urllib.error.HTTPError as e:
        if e.code == 429:            # 요청 제한 — 우회하지 않고 멈춤. 읽은 것은 캐시에 남아 다음 실행이 이어서 함
            BLOCKED["n"] += 5
        return None
    except Exception:
        return None
    if "/sorry/" in html or "unusual traffic" in html or "봇이 아님" in html:
        BLOCKED["n"] += 1
        return None
    m = re.search(r'"videoDetails":\{.*?"keywords":(\[[^\]]*\])', html)
    if not m:
        CACHE[vid] = []
        return []
    try:
        CACHE[vid] = json.loads(m.group(1))
    except Exception:
        CACHE[vid] = []
    return CACHE[vid]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--per", type=int, default=60); ap.add_argument("--workers", type=int, default=2); ap.add_argument("--max-channels", type=int, default=60)
    a = ap.parse_args()
    out = ROOT / ".cache" / "tags" / dt.date.today().isoformat(); out.mkdir(parents=True, exist_ok=True)
    # 1) 채널
    ch = dict(EXTRA)
    seen = collections.Counter(); ids = {}
    with cf.ThreadPoolExecutor(6) as ex:
        for es in ex.map(search, QUERIES):
            for e in es:
                nm, cid = e.get("channel") or "", e.get("channel_id")
                if cid and nm and not BROADCAST.search(nm) and not EXCLUDE.search(nm):
                    seen[nm] += 1; ids[nm] = cid
    for nm, _ in seen.most_common():      # 검색에 여러 번 걸린 채널부터 (분야에서 활발한 곳)
        if len(ch) >= a.max_channels:
            break
        ch.setdefault(nm, ids[nm])
    print(f"[tags] 채널 후보 {len(ch)}개", flush=True)
    # 2) 채널별 최근 영상
    with cf.ThreadPoolExecutor(6) as ex:
        chans = dict(zip(ch, ex.map(lambda c: channel(c, a.per), ch.values())))
    chans = {k: v for k, v in chans.items() if v.get("median") and len(v.get("videos", [])) >= 15}
    print(f"[tags] 쓸 수 있는 채널 {len(chans)}개 (긴 영상 15편+)", flush=True)
    vids = [(nm, v) for nm, c in chans.items() for v in c["videos"] if v["x"]]
    # 3) 태그
    def one(item):
        nm, v = item
        time.sleep(0.8)
        return nm, v, keywords(v["id"])
    rows = []
    with cf.ThreadPoolExecutor(a.workers) as ex:
        for nm, v, kw in ex.map(one, vids):
            if kw is None:
                continue
            rows.append({"channel": nm, "id": v["id"], "title": v["title"], "views": v["views"], "x": v["x"], "tags": kw})
    print(f"[tags] 영상 {len(rows)}/{len(vids)} 태그 읽음 · 차단 {BLOCKED['n']}", flush=True)
    CACHE_F.parent.mkdir(parents=True, exist_ok=True); CACHE_F.write_text(json.dumps(CACHE, ensure_ascii=False), encoding="utf-8")
    if len(rows) < 300:
        print("[tags] 읽은 영상이 적어 통계를 만들지 않음 — 요청 제한이 풀린 뒤 다시 실행하면 이어서 함", flush=True)
        return
    (out / "raw.json").write_text(json.dumps({"channels": {k: {kk: vv for kk, vv in c.items() if kk != 'videos'} for k, c in chans.items()}, "rows": rows}, ensure_ascii=False), encoding="utf-8")

    # 4) 분석
    by = collections.defaultdict(lambda: {"xs": [], "ch": set(), "show": collections.Counter()})
    for r in rows:
        for t in dict.fromkeys(norm(t) for t in r["tags"]):
            pass
        seen = set()
        for t in r["tags"]:
            k = norm(t)
            if not k or k in seen:
                continue
            seen.add(k)
            by[k]["xs"].append(r["x"]); by[k]["ch"].add(r["channel"]); by[k]["show"][t.strip()] += 1
    allx = [r["x"] for r in rows]
    base_hit = sum(x >= 2 for x in allx) / max(1, len(allx))
    stats = []
    for k, d in by.items():
        n, nc = len(d["xs"]), len(d["ch"])
        if n < 6 or nc < 3:      # 한 채널 습관이 아니라 여러 채널에서 쓰인 태그만
            continue
        xs = d["xs"]
        stats.append({"tag": d["show"].most_common(1)[0][0], "key": k, "videos": n, "channels": nc,
                      "x_median": round(statistics.median(xs), 2), "x_geo": round(math.exp(statistics.fmean(math.log(max(x, 0.05)) for x in xs)), 2),
                      "hit_rate": round(sum(x >= 2 for x in xs) / n, 3)})
    stats.sort(key=lambda s: -s["x_geo"])
    # 태그 습관
    def bucket(rs, f):
        g = collections.defaultdict(list)
        for r in rs:
            g[f(r)].append(r["x"])
        return {k: {"videos": len(v), "x_median": round(statistics.median(v), 2), "hit_rate": round(sum(x >= 2 for x in v) / len(v), 3)} for k, v in sorted(g.items()) if len(v) >= 10}
    def title_overlap(r):
        tt = norm(r["title"])
        ts = [norm(t) for t in r["tags"]]
        if not ts:
            return "태그 없음"
        share = sum(1 for t in ts if t and t in tt) / len(ts)
        return "제목과 거의 안 겹침(<20%)" if share < 0.2 else ("일부 겹침(20~50%)" if share < 0.5 else "제목과 많이 겹침(50%+)")
    def ntags(r):
        n = len(r["tags"])
        return "0개" if n == 0 else ("1~5개" if n <= 5 else ("6~15개" if n <= 15 else ("16~30개" if n <= 30 else "31개+")))
    def chname(r):
        c = norm(r["channel"])
        return "채널 이름 태그 있음" if any(norm(t) and (norm(t) in c or c in norm(t)) for t in r["tags"]) else "채널 이름 태그 없음"
    habits = {"태그 개수": bucket(rows, ntags), "제목과 겹침": bucket(rows, title_overlap), "채널 이름 태그": bucket(rows, chname)}
    res = {"date": dt.date.today().isoformat(), "channels": len(chans), "videos": len(rows), "base_hit_rate": round(base_hit, 3),
           "method": "채널 중앙값 대비 배수 x · 태그는 띄어쓰기·대소문자 무시 · 6편+ & 3채널+ 태그만 · x_geo=배수 기하평균",
           "habits": habits, "tags": stats}
    (ROOT / "data" / "tag_stats.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[tags] 태그 {len(stats)}개 통계 → data/tag_stats.json", flush=True)


if __name__ == "__main__":
    main()
