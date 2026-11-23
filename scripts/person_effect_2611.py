"""인물·인터뷰 효과 다시 재기 (2026-11-23 사용자: "인터뷰나 유명인사를 적극 활용해야한다 썸네일에도 내용에도 라고 느껴지는게 현재 제 채널 조회수도 그렇고 이 분야 이 시장자체의 조회수도 이곳에 사람들이 집중되는 것 같은데 분석해주세요").
docs/55 (11/20) 를 최근 영상으로 다시: 시장·경제 개인 채널 × 최근 긴 영상, 채널 중앙값 대비 배수.
제목 특징: ① 인물 이름(빅테크 CEO·투자 대가·연준·정치) ② 인터뷰·발언 낱말('말하는·경고·인터뷰·발언·"…"') ③ 둘 다 ④ 둘 다 없음.
원자료는 .cache/person/ (커밋 안 함), 요약은 docs/59-person-interview-2611.md
    python scripts/person_effect_2611.py [--per 50] [--max-channels 70]
"""
import argparse, collections, concurrent.futures as cf, datetime as dt, json, re, statistics, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "scripts"))
from thumb_research import EXTRA, BROADCAST, EXCLUDE, channel, search  # noqa: E402

QUERIES = ["미국 증시 마감", "엔비디아 주가 분석", "반도체 주식 전망", "삼성전자 SK하이닉스 주가", "코스피 전망", "AI 버블", "금리 인하 주식",
           "경제 뉴스 해설", "메모리 반도체 전망", "미국 주식 전망", "버핏 인터뷰", "젠슨 황 인터뷰"]
PEOPLE = {
    "빅테크·AI CEO": ["젠슨 황", "젠슨황", "황 CEO", "머스크", "올트먼", "알트먼", "저커버그", "나델라", "피차이", "팀 쿡", "리사 수", "베이조스", "아모데이", "손정의", "최태원", "이재용", "크레스"],
    "투자 대가": ["버핏", "멍거", "드러켄밀러", "달리오", "버리", "캐시 우드", "애크먼", "하워드 막스", "피터 린치", "짐 로저스", "그리핀", "다이먼", "채노스", "아이스먼", "손정의"],
    "연준·정책": ["파월", "워시", "쿡 이사", "리사 쿡", "베선트", "연준 의장", "옐런"],
    "정치": ["트럼프", "시진핑", "푸틴", "이재명"],
}
TALK = re.compile(r"말하는|말한|경고|인터뷰|발언|조언|고백|폭로|예언|원칙|\"[^\"]{2,}\"|'[^']{2,}'|“[^”]{2,}”|‘[^’]{2,}’")


def kind(title):
    hit = [g for g, names in PEOPLE.items() if any(n in title for n in names)]
    return hit, bool(TALK.search(title))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--per", type=int, default=50); ap.add_argument("--max-channels", type=int, default=70)
    a = ap.parse_args()
    ch = dict(EXTRA); seen = collections.Counter(); ids = {}
    with cf.ThreadPoolExecutor(6) as ex:
        for es in ex.map(search, QUERIES):
            for e in es:
                nm, cid = e.get("channel") or "", e.get("channel_id")
                if cid and nm and not BROADCAST.search(nm) and not EXCLUDE.search(nm):
                    seen[nm] += 1; ids[nm] = cid
    for nm, _ in seen.most_common():
        if len(ch) >= a.max_channels:
            break
        ch.setdefault(nm, ids[nm])
    with cf.ThreadPoolExecutor(6) as ex:
        chans = dict(zip(ch, ex.map(lambda c: channel(c, a.per), ch.values())))
    rows = []
    for nm, c in chans.items():
        if not c.get("median") or len(c.get("videos", [])) < 15:
            continue
        for v in c["videos"]:
            if not v["x"]:
                continue
            ppl, talk = kind(v["title"] or "")
            rows.append({"channel": nm, "title": v["title"], "views": v["views"], "x": v["x"], "people": ppl, "talk": talk})
    out = ROOT / ".cache" / "person"; out.mkdir(parents=True, exist_ok=True)
    (out / f"{dt.date.today().isoformat()}.json").write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")

    def stat(rs):
        xs = [r["x"] for r in rs]
        if not xs:
            return "0편"
        return f"{len(xs)}편 · 중앙 {statistics.median(xs):.2f}배 · 3배+ {sum(x >= 3 for x in xs) / len(xs):.0%} · 0.5배- {sum(x <= 0.5 for x in xs) / len(xs):.0%}"
    print("채널", len({r['channel'] for r in rows}), "영상", len(rows))
    print("전체:", stat(rows))
    print("인물 없음·발언 없음:", stat([r for r in rows if not r["people"] and not r["talk"]]))
    print("인물만:", stat([r for r in rows if r["people"] and not r["talk"]]))
    print("발언만:", stat([r for r in rows if not r["people"] and r["talk"]]))
    print("인물+발언:", stat([r for r in rows if r["people"] and r["talk"]]))
    for g in PEOPLE:
        print(" ", g, stat([r for r in rows if g in r["people"]]))
    for g in PEOPLE:
        for n in PEOPLE[g]:
            rs = [r for r in rows if n in r["title"]]
            if len(rs) >= 3:
                print("    ", n, stat(rs))
    # 채널 안 비교 (인물 제목 3편+ 채널)
    print("채널 안 비교 (인물 3편+):")
    by = collections.defaultdict(list)
    for r in rows:
        by[r["channel"]].append(r)
    up = down = 0
    for nm, rs in by.items():
        p = [r["x"] for r in rs if r["people"]]; q = [r["x"] for r in rs if not r["people"]]
        if len(p) >= 3 and len(q) >= 5:
            mp, mq = statistics.median(p), statistics.median(q)
            up += mp > mq; down += mp <= mq
            print(f"   {nm[:18]:18} 인물 {mp:.2f} ({len(p)}) vs 없음 {mq:.2f} ({len(q)})")
    print("인물 쪽이 높은 채널", up, "/ 낮은 채널", down)
    print("터진 인물 영상 예:")
    for r in sorted([r for r in rows if r["people"]], key=lambda r: -r["x"])[:15]:
        print(f"   {r['x']:5.1f}배 · {r['channel'][:14]} · {r['title'][:70]}")
    print("안 된 인물 영상 예:")
    for r in sorted([r for r in rows if r["people"]], key=lambda r: r["x"])[:10]:
        print(f"   {r['x']:5.2f}배 · {r['channel'][:14]} · {r['title'][:70]}")


if __name__ == "__main__":
    main()
