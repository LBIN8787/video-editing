"""대본(scenes.json) 점검: 형식 + '일반인이 바로 이해하는가' + 편집 스타일 계열별 화면 비율.

errors  = 고쳐야 통과 (validate 실패, script 단계는 한 번 고쳐 쓰기)
warnings = 권고 (통과는 됨)
"""
from __future__ import annotations

import json
import re
from collections import defaultdict

from . import config

NUM = re.compile(r"\d[\d,.]*")
YEAR = re.compile(r"(19|20)\d\d")


def jargon() -> list[str]:
    f = config.DATA_DIR / "jargon.json"
    return json.loads(f.read_text(encoding="utf-8")).get("terms", []) if f.exists() else []


def _has(text: str, term: str) -> bool:
    if re.fullmatch(r"[A-Za-z&]+", term):  # 영문 약어는 단어 경계로 (EPS ≠ EPSON)
        return re.search(rf"(?<![A-Za-z]){re.escape(term)}(?![A-Za-z])", text) is not None
    return term in text


def check(data: dict, family: str = "source") -> tuple[list[str], list[str]]:
    errs, warns = [], []
    scenes = data.get("scenes", [])
    if family == "shorts" or not scenes:
        return errs, warns
    beats = defaultdict(list)
    for s in scenes:
        beats[s.get("beat") or ""].append(s)

    # 0) 레퍼런스 채널 이름을 출처·화면에 쓰지 않는다 (구조와 기법만 벤치마킹)
    for s in scenes:
        for r in ("미주일기", "식스시그마", "머니크루", "AI비즈PT", "AIBizPT", "로제타"):
            if r in s.get("label", "") or r in s["narration"] or r in json.dumps(s.get("card") or {}, ensure_ascii=False):
                errs.append(f"#{s['id']}: 레퍼런스 채널 이름 '{r}' 이 들어 있습니다 (직접 만든 도식의 출처는 '자체 정리')")

    # 1) 핵심과 논리 구조
    if not (data.get("core_message") or "").strip():
        errs.append("core_message(시청자가 기억할 한 문장)가 비어 있습니다")
    elif not NUM.search(data["core_message"]):
        warns.append("core_message 에 숫자가 없습니다 (기억에 남는 숫자 1개를 넣으세요)")
    n = len(data.get("logic") or [])
    if not 3 <= n <= 6:
        errs.append(f"logic(논리 구조)은 3~6단계여야 합니다 (지금 {n}): 사실 → 왜 → 그래서 → 과거 사례 → 반론 → 의미")

    # 2) 쉬운 설명 재료: 비유·과거 사례·반론
    if len(beats["analogy"]) < 2:
        errs.append(f"비유 장면(beat=analogy)이 {len(beats['analogy'])}개입니다. 어려운 숫자·개념마다 일상 비유를 2개 이상 넣으세요")
    if not beats["precedent"]:
        errs.append("과거 사례 장면(beat=precedent)이 없습니다. '전에도 이런 일이 있었나'를 연도·숫자와 함께 1개 이상")
    elif not any(YEAR.search(s["narration"] + json.dumps(s.get("card") or {}, ensure_ascii=False)) for s in beats["precedent"]):
        errs.append("과거 사례 장면에 연도가 없습니다 (예: 2000년 3월 시스코)")
    if not beats["counter"]:
        warns.append("반론 장면(beat=counter)이 없습니다")

    # 3) 숫자는 비교 기준과 함께
    for s in beats["number"]:
        if not (s.get("compare_to") or "").strip():
            errs.append(f"#{s['id']}: 숫자 장면에 비교 기준(compare_to)이 없습니다 (작년 대비·1인당·익숙한 것과 비교)")
    for s in scenes:
        nums = NUM.findall(s["narration"])
        if len(nums) >= 3:
            warns.append(f"#{s['id']}: 한 문장에 숫자 {len(nums)}개 → 둘로 나누면 귀에 잘 들어옵니다")
        if len(s["narration"].replace(" ", "")) > 70:
            warns.append(f"#{s['id']}: 문장이 깁니다 ({len(s['narration'].replace(' ', ''))}자) → 1~2문장, 70자 이내")
    if not any(NUM.search(s["narration"]) for s in scenes[:3]):
        warns.append("첫 3장면에 숫자가 없습니다 (훅은 숫자 사실로 시작)")

    # 4) 어려운 말은 처음 나올 때 풀어 준다
    gl = {g["term"]: g for g in data.get("glossary") or []}
    first = {}
    for s in scenes:
        text = s["narration"] + " " + json.dumps(s.get("card") or {}, ensure_ascii=False)
        for t in jargon():
            if t not in first and _has(text, t):
                first[t] = s["id"]
    for t, sid in first.items():
        g = gl.get(t) or next((v for k, v in gl.items() if t in k or k in t), None)
        if not g:
            errs.append(f"어려운 말 '{t}'(#{sid} 처음)에 쉬운 풀이(glossary)가 없습니다")
        elif g["scene_id"] > sid + 1:
            errs.append(f"'{t}' 풀이가 #{g['scene_id']} 에 있는데 처음 나오는 건 #{sid} 입니다 (처음 나올 때 풀어 주세요)")

    # 5) 섹션마다 '그래서 무슨 뜻인지'
    secs = defaultdict(list)
    for s in scenes:
        secs[s["section"]].append(s)
    for sec, ss in secs.items():
        if sec.startswith("body") and not any(x.get("beat") in ("so_what", "summary") for x in ss):
            warns.append(f"{sec}: '그래서 무슨 뜻인지'(beat=so_what 또는 summary) 장면이 없습니다")

    # 6) 편집 스타일 계열별 화면 비율
    N = len(scenes)
    src = [s for s in scenes if s["visual_type"] == "source_video" or s["kind"] == "quote"]
    card = [s for s in scenes if s["visual_type"] == "card"]
    shot = [s for s in scenes if s["visual_type"] == "screenshot"]
    quotes = [s for s in scenes if s["kind"] == "quote"]
    if family == "source":
        if len(src) / N < 0.35:
            warns.append(f"원본 소스형인데 원본 영상 장면이 {len(src) / N:.0%} 입니다 (목표 40~55%)")
        if len(quotes) < 3:
            warns.append(f"원본 소스형인데 원래 목소리 발언(kind=quote)이 {len(quotes)}개입니다 (목표 4개 이상: CEO·CFO·실적발표)")
        for sec, ss in secs.items():
            if sec.startswith("body") and not any(x.get("beat") == "summary" and x["visual_type"] == "card" for x in ss):
                warns.append(f"{sec}: 원본 영상 뒤 핵심 요약 카드(beat=summary, visual_type=card)가 없습니다")
    elif family == "infographic":
        if (len(card) + len(shot)) / N < 0.70:
            warns.append(f"인포그래픽형인데 카드+캡처 장면이 {(len(card) + len(shot)) / N:.0%} 입니다 (목표 75% 이상)")
        if len(src) / N > 0.20:
            warns.append(f"인포그래픽형인데 원본 영상 장면이 {len(src) / N:.0%} 입니다 (20% 이하)")
        if not any((s.get("card") or {}).get("type") == "analogy" for s in card):
            warns.append("인포그래픽형인데 비유 카드(card.type=analogy)가 없습니다")
    return errs, warns
