"""유명 인물 효과 조사 — 시장·경제 해설 채널에서 '아는 사람'이 제목·썸네일에 나오면 더 터지나 (2026-11-20 사용자:
"유명인사가 썸네일에 나오거나 유명인사를 다룬 주제 내용들이 조회수가 높은 것 같은데 이 특징들을 조사하고 이를 반영해서 분석하고 썸네일이랑 썸네일 제목 생성에 고려해줘").

입력: scripts/thumb_research.py 가 모은 .cache/thumbs/<날짜>/videos.json (채널별 최근 영상, x = 조회수 ÷ 채널 중앙값).
방법: 제목에서 이름 사전(아래 PEOPLE)으로 인물을 찾아 갈래(빅테크 CEO·투자 대가·정책 결정자·정치·한국 재계 …)를 붙이고,
      같은 채널 기준 배수(x)로 '인물 있음 vs 없음'을 비교. 썸네일은 터진/안 된 영상만 받아 둔 이미지에서 얼굴 수·크기를 잼(opencv).
결과: 콘솔 표 + .cache/thumbs/<날짜>/celeb.json (타 채널 자료라 커밋 안 함). 요약은 docs/55-celebrity-effect.md.

    python scripts/celeb_research.py [--date 2026-11-20]
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# 이름(제목에 나오는 표기) → 갈래. 성만 쓰는 경우가 많아 한국어 표기를 여러 개 둠.
PEOPLE = {
    "빅테크 CEO": ["젠슨 황", "젠슨황", "일론 머스크", "머스크", "샘 올트먼", "샘 알트만", "올트먼", "알트먼", "저커버그", "베이조스", "팀 쿡",
                  "나델라", "피차이", "리사 수", "아모데이", "손정의", "마윈", "레이 커즈와일", "빌 게이츠", "게이츠", "스티브 잡스", "잡스",
                  "피터 틸", "마크 앤드리슨", "알렉스 카프", "카프", "에릭 슈미트", "마이클 델", "래리 엘리슨", "엘리슨"],
    "투자 대가": ["워런 버핏", "버핏", "찰리 멍거", "멍거", "레이 달리오", "달리오", "하워드 막스", "모건 하우절", "나발 라비칸트", "피터 린치", "캐시 우드", "마이클 버리",
                "빅쇼트 버리", "조지 소로스", "소로스", "짐 로저스", "로저스", "스탠리 드러켄밀러", "드러켄밀러", "빌 애크먼", "애크먼", "존 템플턴", "켄 피셔",
                "제레미 시겔", "톰 리", "모하메드 엘에리언", "엘에리언", "웰스 와일더", "벤저민 그레이엄", "필립 피셔", "앙드레 코스톨라니", "코스톨라니",
                "닐 게이먼", "마크 미너비니", "미너비니", "윌리엄 오닐", "제시 리버모어", "리버모어"],
    "정책·중앙은행": ["파월", "옐런", "베선트", "라가르드", "우에다", "이창용", "버냉키", "그린스펀", "볼커", "워시", "해싯"],
    "정치 지도자": ["트럼프", "바이든", "시진핑", "푸틴", "이재명", "윤석열", "젤렌스키", "네타냐후", "다카이치", "이시바", "모디 총리", "해리스", "JD 밴스", "밴스 부통령"],
    "한국 재계": ["이재용", "최태원", "정의선", "구광모", "신동빈", "이건희", "정주영", "김범수", "방시혁", "서정진", "이병철", "김승연"],
    "역사 인물": ["케인스", "하이에크", "프리드먼", "마르크스", "애덤 스미스", "나폴레옹", "처칠", "링컨", "루스벨트", "히틀러", "로스차일드", "록펠러", "카네기", "JP 모건(인물)"],
}
NAME = {n: g for g, ns in PEOPLE.items() for n in ns}
# 긴 이름부터 찾아 '젠슨 황' 안의 '황' 같은 짧은 표기와 겹치지 않게
PAT = re.compile("|".join(sorted(map(re.escape, NAME), key=len, reverse=True)))
QUOTE = re.compile(r"[\"“”'‘’「」『』]")
NUM = re.compile(r"\d")
COMPANY = re.compile(r"엔비디아|테슬라|애플|마이크로소프트|구글|알파벳|아마존|메타|오픈AI|오픈에이아이|앤트로픽|삼성|SK하이닉스|하이닉스|TSMC|AMD|인텔|브로드컴|팔란티어|버크셔|코인베이스|넷플릭스|쿠팡|현대차|카카오|네이버")


def tag(title: str) -> dict:
    names = sorted(set(PAT.findall(title or "")))
    return {"names": names, "groups": sorted({NAME[n] for n in names}), "quote": bool(QUOTE.search(title or "")),
            "num": bool(NUM.search(title or "")), "company": bool(COMPANY.search(title or ""))}


def summary(rows: list) -> dict:
    xs = [r["x"] for r in rows if r["x"]]
    if not xs:
        return {"n": 0}
    return {"n": len(xs), "median_x": round(statistics.median(xs), 2), "mean_x": round(statistics.mean(xs), 2),
            "hit_rate": round(sum(x >= 3 for x in xs) / len(xs), 3), "low_rate": round(sum(x <= 0.5 for x in xs) / len(xs), 3)}


def faces(img_dir: Path, ids: list) -> dict:
    try:
        import cv2
    except ImportError:
        return {}
    casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    out = {}
    for i in ids:
        p = img_dir / f"{i}.jpg"
        if not p.exists():
            continue
        im = cv2.imread(str(p))
        if im is None:
            continue
        g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        fs = casc.detectMultiScale(g, 1.1, 5, minSize=(int(g.shape[1] * 0.06),) * 2)
        area = max([w * h for (_, _, w, h) in fs], default=0) / (g.shape[0] * g.shape[1])
        out[i] = {"faces": len(fs), "face_area": round(area, 3)}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default="")
    a = ap.parse_args()
    base = ROOT / ".cache" / "thumbs"
    d = base / (a.date or sorted(p.name for p in base.iterdir() if p.is_dir())[-1])
    rows = [r for r in json.loads((d / "videos.json").read_text(encoding="utf-8")) if r.get("x") and not re.search(r"Fireship", r.get("channel", ""))]
    for r in rows:
        r.update(tag(r["title"]))
    has = [r for r in rows if r["names"]]
    no = [r for r in rows if not r["names"]]
    res = {"date": d.name, "videos": len(rows), "channels": len({r["channel"] for r in rows}),
           "person": summary(has), "no_person": summary(no),
           "company_only": summary([r for r in no if r["company"]]),
           "neither": summary([r for r in no if not r["company"]])}
    res["by_group"] = {g: summary([r for r in has if g in r["groups"]]) for g in PEOPLE}
    res["person_x"] = {"quote": summary([r for r in has if r["quote"]]), "num": summary([r for r in has if r["num"]]),
                       "plain": summary([r for r in has if not r["quote"] and not r["num"]])}
    # 채널마다: 같은 채널 안에서 인물 있음/없음 중앙 배수 (인물 영상이 3편 이상인 채널만)
    per = {}
    for ch in sorted({r["channel"] for r in rows}):
        hs = [r["x"] for r in has if r["channel"] == ch]
        ns = [r["x"] for r in no if r["channel"] == ch]
        if len(hs) >= 3 and len(ns) >= 3:
            per[ch] = {"person_n": len(hs), "person_med": round(statistics.median(hs), 2), "other_med": round(statistics.median(ns), 2)}
    res["per_channel"] = per
    res["channels_person_higher"] = f"{sum(v['person_med'] > v['other_med'] for v in per.values())}/{len(per)}"
    cnt = collections.Counter(n for r in has for n in r["names"])
    res["names"] = [{"name": n, "n": c, **summary([r for r in has if n in r["names"]])} for n, c in cnt.most_common(30)]
    res["top_person_titles"] = [{"channel": r["channel"], "title": r["title"], "x": r["x"]} for r in sorted(has, key=lambda r: -r["x"])[:25]]
    res["low_person_titles"] = [{"channel": r["channel"], "title": r["title"], "x": r["x"]} for r in sorted(has, key=lambda r: r["x"])[:15]]
    # 썸네일 얼굴 (터진·안 된 영상만 이미지가 있음)
    fc = faces(d / "img", [r["id"] for r in rows if r.get("group") in ("hit", "low")])
    if fc:
        def fs(sel):
            v = [fc[r["id"]] for r in sel if r["id"] in fc]
            return {"n": len(v), "face_rate": round(sum(x["faces"] > 0 for x in v) / len(v), 3) if v else None,
                    "big_face_rate": round(sum(x["face_area"] >= 0.08 for x in v) / len(v), 3) if v else None}
        hit = [r for r in rows if r.get("group") == "hit"]
        low = [r for r in rows if r.get("group") == "low"]
        res["thumb_faces"] = {"hit": fs(hit), "low": fs(low),
                              "hit_person_title": fs([r for r in hit if r["names"]]), "low_person_title": fs([r for r in low if r["names"]])}
    (d / "celeb.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in res.items() if k not in ("top_person_titles", "low_person_titles", "names", "per_channel")}, ensure_ascii=False, indent=1))
    print("이름별:", [(x["name"], x["n"], x.get("median_x"), x.get("hit_rate")) for x in res["names"][:20]])
    print("채널별:", per)
    for t in res["top_person_titles"][:15]:
        print(f"  {t['x']:>6} {t['channel'][:12]} | {t['title'][:70]}")
    print(" -- 안 된 인물 제목")
    for t in res["low_person_titles"][:10]:
        print(f"  {t['x']:>6} {t['channel'][:12]} | {t['title'][:70]}")
    print(d / "celeb.json")


if __name__ == "__main__":
    main()
