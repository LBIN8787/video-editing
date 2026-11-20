"""카테고리별 '터진 영상' 조사 — 썸네일·제목·대본·편집 (2026-11-20 사용자:
"각 카테고리 채널 별 조회수가 잘터지는 영상들의 썸네일과 대본 편집스타일들의 특징을 조사해주세요").

docs/49(시장 썸네일)와 같은 방법을 시장·호기심(심리)·시사로 넓힘:
분야 검색 + 벤치마크 채널 → 채널별 최근 롱폼 → 배수 = 조회수 ÷ 채널 중앙값 → 터진(3배+)/안 된(0.5배-).
원자료·썸네일은 .cache/viral/<날짜>/ (타 채널 자료라 커밋 안 함).

    python scripts/viral_research.py [--per 60]
"""
import argparse, collections, concurrent.futures as cf, datetime as dt, json, re, statistics, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from ytflow import yt  # noqa: E402

# 1차 탐색(분야 검색 + 이름 검색, 2026-11-20)에서 걸린 개인 채널 중 방송 재편집·오디오북·쇼 클립을 뺀 목록.
# 검색 결과가 실행마다 달라져서 재현할 수 있게 이름으로 고정한다.
CHANNELS = {
    "market": ["머니크루 MoneyCrew", "소비더머니", "머니인사이드", "이효석아카데미", "크랩 KLAB", "지식인사이드", "지식한입",
               "슈카월드", "궁금소", "교양이를 부탁해", "미국회계사 EK", "유치한경제학", "머니코믹스 Money Comics"],
    "curiosity": ["심리학 고양이", "사물궁이 잡학지식", "지식해적단", "1분과학에서 재범이로", "놀면서 배우는 심리학", "보다 BODA",
                  "기묘한 밤", "kimwontv김원", "어른이 심리학교", "14F 일사에프"],
    "issues": ["김지윤의 지식Play", "별별역사", "이다지do", "리뷰엉이: Owl's Review", "써에이스쇼 sirace show", "지정학연구소",
               "14F 일사에프", "머니인사이드", "크랩 KLAB", "보다 BODA", "지식해적단"],
}
PINNED = {  # 이름 검색이 흔들리는 채널은 id 고정
    "지식해적단": "UC9cCBxBAQW2CzLYeT20q49A", "1분과학에서 재범이로": "UCFOixeB9gbedVi6uwnsfHMQ",
    "kimwontv김원": "UCRSEOIfPNgUYY8xkEzxqfVg", "지정학연구소": "UCwD_xccmY2wv4j8VNZ5sv3A", "머니인사이드": "UCxfko2YOD6DODYRGzeOPhIQ",
    "사물궁이 잡학지식": "UC7F6UDq3gykPZHWRhrj_BDw", "지식인사이드": "UCA_hgsFzmynpv1zkvA5A7jA", "머니코믹스 Money Comics": "UCJo6G1u0e_-wS-JQn3T-zEw",
}


def search(q, n=30):
    try:
        return yt.flat_playlist(f"ytsearch{n}:{q}", n).get("entries", []) or []
    except Exception:
        return []


def find_id(name):
    if name in PINNED:
        return PINNED[name]
    for e in search(name, 5):
        if e.get("channel") == name:
            return e.get("channel_id")
    return None


def ko_titles(cid, n):
    """한국어 원문 제목 (lang=ko 목록은 조회수가 빠져서 따로 받아 id 로 합침)."""
    raw = yt._run(["-J", "--flat-playlist", "--extractor-args", "youtube:lang=ko", "--playlist-end", str(n),
                   f"https://www.youtube.com/channel/{cid}/videos"])
    try:
        return {e["id"]: e.get("title") for e in json.loads(raw).get("entries", [])}
    except Exception:
        return {}


def channel(cid, n):
    try:
        j = yt.flat_playlist(f"https://www.youtube.com/channel/{cid}/videos", n)
    except Exception:
        return {}
    ko = ko_titles(cid, n)
    vids = [{"id": e.get("id"), "title": ko.get(e.get("id")) or e.get("title"), "views": e.get("view_count") or 0,
             "dur": e.get("duration") or 0} for e in j.get("entries", []) or [] if e.get("id")]
    vids = [v for v in vids if v["dur"] >= 180]          # 쇼츠 제외
    vv = [v["views"] for v in vids if v["views"]]
    med = statistics.median(vv) if len(vv) >= 10 else 0
    for v in vids:
        v["x"] = round(v["views"] / med, 2) if med else 0
    return {"name": j.get("channel"), "subs": j.get("channel_follower_count"), "median": med, "videos": vids}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--per", type=int, default=60)
    a = ap.parse_args()
    out = ROOT / ".cache" / "viral" / dt.date.today().isoformat(); (out / "img").mkdir(parents=True, exist_ok=True)
    names = sorted({n for ns in CHANNELS.values() for n in ns})
    with cf.ThreadPoolExecutor(4) as ex:
        ids = dict(zip(names, ex.map(find_id, names)))
    print("못 찾은 채널:", [n for n, c in ids.items() if not c])
    with cf.ThreadPoolExecutor(4) as ex:
        chans = dict(zip(names, ex.map(lambda nm: channel(ids[nm], a.per) if ids[nm] else {}, names)))
    rows = []
    for cat, ns in CHANNELS.items():
        for nm in ns:
            c = chans.get(nm) or {}
            if not c.get("median"):
                print("비어 있음:", nm); continue
            for v in c["videos"]:
                grp = "hit" if v["x"] >= 3 else "low" if v["x"] <= 0.5 else "mid"
                rows.append({**v, "cat": cat, "channel": nm, "subs": c.get("subs"), "median": c["median"], "group": grp})
    (out / "videos.json").write_text(json.dumps(rows, ensure_ascii=False, indent=0), encoding="utf-8")
    for cat in CHANNELS:
        cr = [r for r in rows if r["cat"] == cat]
        print(f"[{cat}] 채널 {len({r['channel'] for r in cr})} 영상 {len(cr)} 터짐 {sum(r['group']=='hit' for r in cr)} 바닥 {sum(r['group']=='low' for r in cr)}")
    sel = [r for r in rows if r["group"] in ("hit", "low")]

    def get(r):
        p = out / "img" / f"{r['id']}.jpg"
        if not p.exists():
            subprocess.run(["curl", "-sfL", "-o", str(p), f"https://i.ytimg.com/vi/{r['id']}/hqdefault.jpg"], timeout=30)
    with cf.ThreadPoolExecutor(12) as ex:
        list(ex.map(get, sel))


if __name__ == "__main__":
    main()
