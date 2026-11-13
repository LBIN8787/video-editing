"""스타일 시험작: 뉴스 데스크 카드(newsdesk) — 레퍼런스 1분코딩 'AI 뉴스 위클리' 의 '한 소식 = 한 장' 틀 (docs/25).
사실은 20261113-market-daily 팩트시트 그대로 (새 사실 없음).
    python scripts/style_ref2/make.py && YTFLOW_TTS=edge python -m ytflow hybrid 20261113-style-ref2
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "projects" / "20261113-style-ref2"


def B(*s):
    return [{"say": x} for x in s]


def main():
    for d in ("01_research", "02_script", "05_edit", "04_assets/footage"):
        (P / d).mkdir(parents=True, exist_ok=True)
    (P / "edit.yaml").write_text("# 스타일 시험작 news-desk (docs/25)\nedit:\n  style: hybrid\n  style_ref: hybrid\n  family: infographic\nformat: longform\n", encoding="utf-8")
    st = P / "state.json"
    if not st.exists():
        st.write_text(json.dumps({"name": P.name, "created": "2026-11-13T00:00:00", "done": [], "approved": []}, indent=2), encoding="utf-8")
    S = [
        dict(type="newsdesk", chapter=0, idx=1, total=3, source="NVIDIA", tag="이슈", tag_color="red", date="11월 11일 공시",
             headline="창업자가 물러났다", hl="물러났다", sub="젠슨 황, 사장·CEO·이사직에서 즉시 사임",
             stats=[{"label": "주가 (11/12)", "value": "-4.34%", "color": "red"}, {"label": "임시 CEO", "value": "크레스 CFO", "color": "white"},
                    {"label": "첫 실적", "value": "11/17", "color": "yellow"}],
             bullets=["이사회 의장은 하비 존스", "정식 CEO는 안팎에서 찾는 중"],
             panel={"kind": "shot", "src": "footage/nvidia.jpg", "caption": "엔비디아 본사 간판 · CC BY 2.0 Will Buckner", "pos": "50% 40%"},
             footer="출처: 엔비디아 8-K 공시·보도자료 (SEC, 2026.11.11)",
             beats=B("첫 번째 소식, 엔비디아입니다. 젠슨 황이 사장과 CEO, 이사직에서 즉시 물러났습니다.",
                     "주가는 4.34% 내렸고, 콜레트 크레스 CFO가 임시 CEO를 맡습니다. 첫 시험대는 11월 17일 실적입니다.")),
        dict(type="newsdesk", chapter=0, idx=2, total=3, source="AMD · BROADCOM", tag="흐름", tag_color="green", date="11월 12일 마감",
             headline="돈은 대안으로 옮겨 갔다", hl="대안으로", sub="엔비디아가 빠진 자리에 경쟁사가 올랐다",
             stats=[{"label": "AMD", "value": "+5.86%", "color": "green"}, {"label": "브로드컴", "value": "+5.54%", "color": "green"},
                    {"label": "엔비디아", "value": "-4.34%", "color": "red"}],
             panel={"kind": "stamp", "text": "업종이 아니라 회사 문제", "sub": "반도체 지수는 -0.54%", "color": "yellow"},
             footer="출처: 야후 파이낸스 종가 (2026.11.12)",
             beats=B("두 번째, 돈이 어디로 갔는지입니다. AMD는 5.86%, 브로드컴은 5.54% 올랐습니다.",
                     "반도체 지수는 0.54%만 내렸죠. 시장은 업종 전체가 아니라 한 회사의 문제로 읽었다는 뜻입니다.")),
        dict(type="newsdesk", chapter=0, idx=3, total=3, source="NAVER", tag="주의", tag_color="yellow", date="11월 12일 마감",
             headline="최대 매출에도 떨어졌다", hl="떨어졌다", sub="실적이 좋아도 주가는 기대와 비교된다",
             stats=[{"label": "주가", "value": "-6.43%", "color": "red"}, {"label": "매출 증가", "value": "+10.7%", "color": "green"}],
             panel={"kind": "bignum", "label": "3분기 매출 (원)", "value": "34,724억"},
             footer="출처: 네이버 3분기 실적 공시 (2026.11)",
             beats=B("세 번째는 네이버입니다. 3분기 매출은 3조 4,724억 원으로 1년 전보다 10.7% 늘었습니다.",
                     "그런데 주가는 6.43% 떨어졌습니다. 좋은 실적도 시장이 기대한 만큼이 아니면 떨어질 수 있습니다.")),
    ]
    for i, x in enumerate(S, 1):
        x["id"] = i
    spec = {"title": "스타일 시험작 — 뉴스 데스크 카드", "core_message": "한 소식 = 한 장, 숫자와 증거를 한눈에", "scenes": S, "package": {}}
    (P / "02_script" / "hybrid.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
    (P / "01_research" / "factsheet.md").write_text("# 시험작 팩트시트\n\n사실은 projects/20261113-market-daily/01_research/factsheet.md 그대로. 새 사실 없음.\n", encoding="utf-8")
    print(P, len(S))


if __name__ == "__main__":
    main()
