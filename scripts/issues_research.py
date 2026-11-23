"""시사 채널 비교 데이터 다시 모으기 (docs/18-issues-research.md).
    python scripts/issues_research.py            → .cache/issues/channels.json · meta.json · thumbs/ + 제목 특징 표 출력
공개 정보만 (yt-dlp flat-playlist·영상 메타데이터·썸네일 이미지). 영상 파일·스토리보드는 받지 않는다 (봇 확인 우회 금지).
"""
import concurrent.futures as cf
import json
import re
import statistics as st
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ytflow import yt  # noqa: E402

CH = {"지식한입": "UCi9Sl8GnFdYoqEVXnojBPJw", "14F 일사에프": "UCLKuglhGlMmDteQKoniENIQ", "스브스뉴스": "UCQabORQKQRHP-iUqe-xIFvg",
      "비디오머그": "UCMEbRpvuwTbXxGiyDb1mT8w", "씨리얼": "UCqRHncabshHQm_8t2SuMUrA", "김지윤의 지식Play": "UCXql5C57vS4ogUt6CPEWWHA",
      "크랩 KLAB": "UCoxT1kQSLq564FwpK473w-g", "슈카월드": "UCsJ6RuBiTVWRX156FVbeaGg"}
FEATS = {"몰락·붕괴·망함·위기": r"몰락|붕괴|망했|망함|무너|추락|위기|파산", "정리·총정리·N분": r"정리|총정리|한눈에|요약|\d+분",
         "왜·이유": r"왜|이유", "나라·지정학": r"러시아|중국|미국|이란|북한|일본|사우디|이스라엘|인도|베네수엘라|우크라이나|트럼프|푸틴|김정은|중동|전쟁",
         "숫자": r"\d", "근황·지금·요즘": r"근황|지금|요즘|최근", "물음표": r"\?", "진짜·속내·숨은": r"진짜|속내|숨은|실체|정체|민낯"}
OUT = Path(".cache/issues")


def channel(cid: str) -> dict:
    j = json.loads(yt._run(["-J", "--flat-playlist", "--playlist-end", "80", "--extractor-args", "youtube:lang=ko",
                            f"https://www.youtube.com/channel/{cid}/videos"]) or "{}")
    vids = [{"id": e["id"], "title_ko": e.get("title"), "views": e.get("view_count") or 0, "dur": e.get("duration") or 0}
            for e in j.get("entries", []) or []]
    med = st.median([v["views"] for v in vids if v["views"]] or [0])
    for v in vids:
        v["x"] = round(v["views"] / med, 2) if med else 0
    return {"subs": j.get("channel_follower_count"), "median": med, "videos": vids}


def main():
    (OUT / "thumbs").mkdir(parents=True, exist_ok=True)
    with cf.ThreadPoolExecutor(4) as ex:
        data = dict(zip(CH, ex.map(channel, CH.values())))
    (OUT / "channels.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    V = [v for k in data for v in data[k]["videos"] if v["views"]]
    for name, pat in FEATS.items():
        a = [v["x"] for v in V if re.search(pat, v["title_ko"] or "")]
        b = [v["x"] for v in V if not re.search(pat, v["title_ko"] or "")]
        if len(a) >= 8:
            print(f"{name:<16} n={len(a):<4} {st.median(a):.2f} / {st.median(b):.2f} → {st.median(a) / st.median(b):.2f}배")
    for k in data:
        for v in sorted(data[k]["videos"], key=lambda x: -x["x"])[:4]:
            f = OUT / "thumbs" / f"{k.split()[0]}_{v['id']}.jpg"
            if not f.exists():
                urllib.request.urlretrieve(f"https://i.ytimg.com/vi/{v['id']}/hqdefault.jpg", f)


if __name__ == "__main__":
    main()
