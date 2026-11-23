"""스타일 시험작: 원본 발언 컷편집(bite) + 손그림 삽화(illust).
원본: 연준 FOMC 기자회견 2023.6.14 (Federal Reserve 공식 영상, 미국 정부 저작물 = 퍼블릭 도메인)
      archive.org/details/youtube-L61NSlLRGe8 의 mp4 에서 3560초부터 21분을 잘라 04_assets/footage/fomc_20230614_part.mp4
삽화: 사용자가 준비 (2026-11-13). 시험작은 시카고 미술관 퍼블릭 도메인(CC0) 그림을 '임시 그림'으로 씀.
    python scripts/style_cut/make.py && python -m ytflow cut 20261113-style-cut && python -m ytflow hybrid 20261113-style-cut
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "projects" / "20261113-style-cut"
FED = "FOMC 기자회견 2023.6.14"
WHO, ROLE = "제롬 파월", "연준 의장 · 2023년 6월 14일 FOMC 기자회견"
TMP = "임시 그림"


def B(*s):
    return [{"say": x} for x in s]


def main():
    for d in ("01_research", "02_script", "05_edit", "04_assets/footage", "04_assets/art"):
        (P / d).mkdir(parents=True, exist_ok=True)
    (P / "edit.yaml").write_text("# 스타일 시험작: source-cut + illustrated (2026-11-13)\nedit:\n  style: hybrid\n  style_ref: hybrid\n  family: source\n  skin: clean-flat\nformat: longform\n", encoding="utf-8")
    st = P / "state.json"
    if not st.exists():
        st.write_text(json.dumps({"name": P.name, "created": "2026-11-13T00:00:00", "done": [], "approved": []}, indent=2), encoding="utf-8")
    S = [
        dict(type="illust", chapter=0, art="havre.jpg", reveal="paint",
             credit=f"{TMP}: 카미유 피사로 「르아브르 광장」 1893 · 시카고 미술관 CC0",
             brief="1950년대풍 미국 거리, 장바구니를 든 사람들이 가게 앞 가격표를 보며 한숨 (오른쪽 위는 은행 건물)",
             moves=[{"beat": 0, "focus": [0, 0, 1, 1]}, {"beat": 1, "focus": [0.0, 0.42, 0.55, 0.58]}, {"beat": 2, "focus": [0.45, 0.35, 0.55, 0.65]}],
             marks=[{"beat": 1, "kind": "bubble", "at": [1380, 230], "text": "또 올랐네…"},
                    {"beat": 2, "kind": "note", "at": [1180, 200], "text": "금리 +5%p"}],
             beats=B("2023년 6월, 미국 사람들은 1년 넘게 오른 물가에 지쳐 있었습니다.",
                     "5월 소비자물가는 1년 전보다 4% 올랐습니다. 연준이 목표로 하는 2%의 두 배죠.",
                     "연준은 그사이 금리를 5%포인트나 올렸습니다. 그리고 이날, 처음으로 인상을 멈췄습니다.")),
        dict(type="bite", chapter=0, who=WHO, role=ROLE, label=FED,
             beats=B("파월 의장의 설명을 직접 들어 보겠습니다."),
             clip={"src": "fomc", "lang": "en", "cuts": [
                 {"from": "We've covered a lot of ground", "to": "have yet to be felt", "ko": "우리는 많이 왔고, 긴축의 효과는 아직 다 나타나지 않았습니다."},
                 {"from": "today we decided to leave", "to": "policy interest rate unchanged", "ko": "그래서 오늘, 정책금리를 그대로 두기로 했습니다."}]}),
        dict(type="illust", chapter=0, art="cafe.jpg", reveal="iris",
             credit=f"{TMP}: 페르낭 룽그렌 「카페에서」 1882~84 · 시카고 미술관 CC0",
             brief="빈 카페에서 한 사람이 시계를 보며 기다림, 탁자 위 식은 커피 (기다림의 비유)",
             moves=[{"beat": 0, "focus": [0, 0, 1, 1]}, {"beat": 1, "focus": [0.0, 0.1, 0.62, 0.9]}, {"beat": 2, "focus": [0.3, 0.25, 0.7, 0.75]}],
             marks=[{"beat": 1, "kind": "bubble", "at": [1250, 240], "text": "효과는 언제쯤?"},
                    {"beat": 2, "kind": "arrow", "from": [420, 760], "to": [900, 560]}],
             beats=B("효과가 아직 다 나타나지 않았다. 금리는 올린 그날 바로 경제를 바꾸지 않는다는 뜻입니다.",
                     "이자가 오르면 사람들은 집과 차를 덜 사고, 회사는 투자를 미룹니다. 그게 물가에 닿기까지 몇 달이 걸리죠.",
                     "그래서 이번엔 한 번 기다려 보기로 했습니다. 파월 의장의 말로 다시 들어 보죠.")),
        dict(type="bite", chapter=0, who=WHO, role=ROLE, label=FED, beats=[],
             clip={"src": "fomc", "lang": "en", "cuts": [
                 {"from": "considering how far and how fast", "to": "implications for monetary policy",
                  "ko": "얼마나 멀리, 얼마나 빨리 왔는지를 생각하면, 금리를 그대로 두는 게 신중하다고 판단했습니다. 새로 나오는 정보를 보고 그 의미를 따져 보려는 겁니다."}]}),
        dict(type="illust", chapter=0, art="park.jpg", reveal="paint",
             credit=f"{TMP}: 윌리엄 메릿 체이스 「도시 공원」 1887년경 · 시카고 미술관 CC0",
             brief="공원 길 벤치에 앉아 쉬는 사람, 길은 앞으로 길게 이어짐 (멈춤이 아니라 쉬어 감)",
             moves=[{"beat": 0, "focus": [0, 0, 1, 1]}, {"beat": 1, "focus": [0.4, 0.2, 0.6, 0.8]}],
             marks=[{"beat": 0, "kind": "bubble", "at": [700, 220], "text": "이제 끝인가?"},
                    {"beat": 1, "kind": "arrow", "from": [700, 900], "to": [1250, 430]},
                    {"beat": 1, "kind": "note", "at": [1280, 360], "text": "7월, 한 번 더"}],
             beats=B("그렇다면 금리 인상은 이걸로 끝난 걸까요? 파월 의장은 같은 자리에서 이렇게 말했습니다.",
                     "멈춘 게 아니라 쉬어 간 거였죠. 실제로 연준은 다음 달인 7월, 금리를 한 번 더 올렸습니다.")),
        dict(type="bite", chapter=0, who=WHO, role=ROLE, label=FED, beats=[],
             clip={"src": "fomc", "lang": "en", "cuts": [
                 {"from": "nearly all committee participants view it as likely", "to": "appropriate this year",
                  "ko": "거의 모든 위원이, 올해 안에 금리를 조금 더 올리는 게 적절할 것으로 봅니다."}]}),
    ]
    # 마지막 bite 를 공원 장면의 첫 박자 뒤로: 공원 장면을 둘로 나눠 '질문 → 대답(원본) → 해설' 순서로
    park = S[4]
    q = dict(park, beats=park["beats"][:1], moves=park["moves"][:1], marks=[m for m in park["marks"] if m["beat"] == 0])
    a = dict(park, reveal="fade", beats=park["beats"][1:], moves=[{"beat": 0, "focus": [0.4, 0.2, 0.6, 0.8]}],
             marks=[dict(m, beat=0) for m in park["marks"] if m["beat"] == 1])
    S = S[:4] + [q, S[5], a]
    for i, x in enumerate(S, 1):
        x["id"] = i
    spec = {"title": "스타일 시험작 — 원본 발언 컷편집 + 손그림 삽화", "core_message": "그 사람의 목소리로, 그림 위를 옮겨 다니며",
            "footage": {"fomc": {"file": "fomc_20230614_part.mp4", "credit": "Federal Reserve · 퍼블릭 도메인",
                                 "url": "https://archive.org/details/youtube-L61NSlLRGe8 (연준 공식 채널 영상, 3560초부터)"}},
            "scenes": S, "package": {}}
    (P / "02_script" / "hybrid.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
    (P / "01_research" / "factsheet.md").write_text(
        "# 시험작 팩트시트 (2023년 6월 FOMC)\n\n"
        "| # | 사실 | 출처 |\n|---|---|---|\n"
        "| F1 | 2023.6.14 FOMC 정책금리 5~5.25% 동결 (2022년 초부터 5%p 인상 뒤 첫 동결) | 파월 의장 기자회견 모두발언 (원본 영상 받아쓰기 380~410초 구간) |\n"
        "| F2 | 5월 소비자물가 1년 전보다 4%, 근원 5.3% | 같은 모두발언 229초 구간 |\n"
        "| F3 | '거의 모든 위원이 올해 추가 인상이 적절할 것으로 봄' | 같은 모두발언 75초 구간 |\n"
        "| F4 | 2023.7.26 FOMC 0.25%p 인상 (5.25~5.5%) | 연준 7월 성명 (federalreserve.gov, 2023.7.26) |\n\n"
        "## 해석\n- '동결'은 끝이 아니라 효과를 기다리는 쉼이었다 (F3 → F4 로 확인).\n", encoding="utf-8")
    print(P, len(S))


if __name__ == "__main__":
    main()
