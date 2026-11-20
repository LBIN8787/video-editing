"""viral_research.py 결과의 제목 특징을 카테고리별로 비교 (같은 채널 안 배수 비 포함).

    python scripts/viral_titles.py [.cache/viral/<날짜>/videos.json]
"""
import collections, json, re, statistics, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
FEATS = {
    "물음표 ?": r"\?",
    "따옴표 발언 \"…\"": r"[\"“”‘’']",
    "'~이유'": r"이유",
    "'벌어지는/생기는 일'": r"(벌어지는|벌어질|생기는|생길|닥칠) 일",
    "'특징·유형'": r"특징|유형|공통점",
    "'진짜·실체·숨겨진·비밀'": r"진짜|실체|숨겨진|숨긴|비밀|몰래",
    "'몰락·망한·무너진'": r"몰락|망한|망했|무너|최후|파산|폭망",
    "'역설·착각'": r"역설|착각|오히려",
    "'총정리·모든 것·몰아보기'": r"총정리|모든 것|모든것|몰아보기|풀버전|한 번에|한번에",
    "숫자": r"\d",
    "출연자 (교수·원장·기자…)": r"교수|원장|기자|소장|작가|박사|대표|전문가|위원|총재",
    "'지금·요즘·근황'": r"지금|요즘|근황|최근",
    "명령 ('~하세요·사라')": r"하세요|사세요|사라|마세요|팔지|하지 마",
    "'당신·나·우리'": r"당신|나는|내가|우리",
    "나라·전쟁": r"한국|미국|중국|일본|러시아|북한|이란|이스라엘|우크라|전쟁|대만|유럽",
}


def main():
    p = Path(sys.argv[1]) if len(sys.argv) > 1 else sorted((ROOT / ".cache" / "viral").glob("*/videos.json"))[-1]
    rows = [r for r in json.loads(p.read_text(encoding="utf-8")) if r["views"] > 0]
    for cat in ["market", "curiosity", "issues"]:
        cr = [r for r in rows if r["cat"] == cat]
        print(f"\n### {cat}  (영상 {len(cr)}, 터짐 3배+ {sum(r['x']>=3 for r in cr)})")
        print("| 제목 특징 | 편수 | 3배+ 비율 (있음) | 3배+ 비율 (없음) | 같은 채널 안 배수 비 (높은 채널/비교 가능) |")
        print("|---|---|---|---|---|")
        for name, rx in FEATS.items():
            has = [r for r in cr if re.search(rx, r["title"])]; no = [r for r in cr if not re.search(rx, r["title"])]
            if len(has) < 8:
                continue
            hr = sum(r["x"] >= 3 for r in has) / len(has); nr = sum(r["x"] >= 3 for r in no) / max(1, len(no))
            ratios = []; up = 0
            by = collections.defaultdict(lambda: ([], []))
            for r in cr:
                by[r["channel"]][0 if re.search(rx, r["title"]) else 1].append(r["x"])
            for a, b in by.values():
                if len(a) >= 3 and len(b) >= 3:
                    ra = statistics.median(a) / max(0.01, statistics.median(b)); ratios.append(ra); up += ra > 1
            rr = f"{statistics.median(ratios):.2f} ({up}/{len(ratios)})" if ratios else "-"
            print(f"| {name} | {len(has)} | {hr:.1%} | {nr:.1%} | {rr} |")


if __name__ == "__main__":
    main()
