"""2026-11-25 사용자: "요일 상관없이 언제 올려도 되도록 영상자체 방향성을 정해주세요"
심층 편은 올리는 날에 묶이지 않게: '오늘·내일·최근'처럼 올린 날에 따라 뜻이 바뀌는 말을 날짜나 '이 영상'으로 바꾼다.
('오늘의 매출'처럼 시점이 아니라 개념인 말은 그대로.)  python scripts/fix_timeproof_deep.py  (다시 돌려도 같은 결과)"""
import json
from pathlib import Path

R = Path(__file__).resolve().parent.parent / "projects"
FIX = {
    "20261124-market-deep-nvidia-return": [
        (2, 1, "그래서 오늘 질문은 둘입니다.", "그래서 이 영상의 질문은 둘입니다."),
        (23, "title", "한국 계좌로 — 메모리 약정과 내일의 장", "한국 계좌로 — 메모리 약정과 24일 한국 장"),
        (25, "title", "한국 반도체 — 한 달과 오늘", "한국 반도체 — 한 달과 24일"),
    ],
    "20261122-market-deep-nvidia-circular": [
        (3, 1, "오늘은 그 한가운데 있는 이 고리가", "이 영상에서는 그 한가운데 있는 이 고리가"),
    ],
    "20261122-market-deep-nvidia-insight": [
        (4, 1, "그래서 오늘 질문은 둘입니다.", "그래서 이 영상의 질문은 둘입니다."),
    ],
    "20261122-market-deep-openai": [
        (4, 0, "그래서 오늘 나오는 오픈AI의 숫자는", "그래서 이 영상에 나오는 오픈AI의 숫자는"),
    ],
    "20261122-market-deep-memory-chicken": [
        (2, 1, "오늘은 메모리 값이 왜", "이 영상은 메모리 값이 왜"),
        (26, 1, "최근 낸드 현물값이 한 달 새 20% 가까이 빠진", "10월 중순부터 한 달 새 낸드 현물값이 20% 가까이 빠진"),
        (32, 1, "최근 한 달 사이 현물값이", "11월 20일까지 한 달 사이 현물값이"),
        (36, 0, "둘째, 오늘 쓴 세 회사 계산은", "둘째, 이 영상에서 쓴 세 회사 계산은"),
    ],
    "20261122-market-deep-memory-insight": [
        (29, 0, "1부의 원리와 오늘의 신호를", "1부의 원리와 이 영상의 신호를"),
    ],
}
MD = {"20261124-market-deep-nvidia-return": [("메모리 약정과 내일의 장", "메모리 약정과 24일 한국 장"),
                                              ("📅 자료 기준: 2026년 11월 23일", "📅 자료 기준: 2026년 11월 24일 (미국 시각 23일 종가·한국 24일 종가)")]}


def main():
    for proj, fixes in FIX.items():
        p = R / proj / "02_script" / "hybrid.json"
        d = json.loads(p.read_text(encoding="utf-8"))
        for sid, where, old, new in fixes:
            s = next(x for x in d["scenes"] if x["id"] == sid)
            if where == "title":
                tgt, key = s, "title"
            else:
                tgt, key = s["beats"][where], "say"
            if new in tgt[key]:
                continue
            assert old in tgt[key], (proj, sid, old)
            tgt[key] = tgt[key].replace(old, new)
            print("ok", proj[-16:], sid, where)
        p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    for proj, reps in MD.items():
        for f in ("youtube.md", "package.md"):
            q = R / proj / "05_edit" / f
            if q.exists():
                t = q.read_text(encoding="utf-8")
                for a, b in reps:
                    t = t.replace(a, b)
                q.write_text(t, encoding="utf-8")


if __name__ == "__main__":
    main()
