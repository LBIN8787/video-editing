"""스타일 시험작: 움직이는 비유 애니메이션 (motion-metaphor). 사실은 20261112-market-call 팩트시트(E5·E8·E9)에서.
    python scripts/style_motion/make.py && python -m ytflow hybrid 20261112-style-motion
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "projects" / "20261112-style-motion"
LBL = "코어위브 3분기 어닝콜 공식 녹취록 (2026.11.10) · 회사 발표"


def main():
    for d in ("01_research", "02_script", "05_edit"):
        (P / d).mkdir(parents=True, exist_ok=True)
    (P / "edit.yaml").write_text("# 스타일 시험작 motion-metaphor\nedit:\n  style: hybrid\n  style_ref: hybrid\n  family: infographic\n  skin: clean-white\nformat: longform\n", encoding="utf-8")
    st = P / "state.json"
    if not st.exists():
        st.write_text(json.dumps({"name": P.name, "created": "2026-11-12T00:00:00", "done": [], "approved": []}, indent=2), encoding="utf-8")
    S = [
        dict(type="metaphor", mode="migrate", chapter=0, label=LBL, title="수요가 용량의 10배", hl="10배",
             target={"label": "공급 가능한 용량", "color": "#D9412B", "kind": "bus"},
             sources=[{"label": "AI 연구소", "color": "#2F6FB3"}, {"label": "기업", "color": "#2E9D6A"}, {"label": "금융사", "color": "#E0A82E"}],
             crowd={"icon": "person", "n": 40, "start": "right", "beat": 1, "board": 0.85},
             words=[{"text": "바글바글", "side": "left", "beat": 1}, {"text": "줄 서는 중", "side": "right", "beat": 1}], arrow={"beat": 0},
             beats=[{"say": "코어위브 CEO는 2027년 말까지 공급할 수 있는 용량보다, 검증된 수요가 10배 많다고 했습니다."},
                    {"say": "버스 한 대에 손님이 열 배 몰린 셈이죠. 회사는 다 태우지 않고, 더 좋은 조건을 기다린다고까지 했습니다."}]),
        dict(type="metaphor", mode="migrate", chapter=0, label=LBL, title="빚 대신, 고객이 미리 낸 돈", hl="미리",
             target={"label": "코어위브", "color": "#3B4A6B", "kind": "building"},
             sources=[{"label": "고객", "color": "#2E9D6A", "kind": "building"}, {"label": "고객", "color": "#2F6FB3", "kind": "building"}],
             crowd={"icon": "banknote", "color": "#2E9D6A", "n": 26, "start": "right", "beat": 1, "board": 1.0},
             words=[{"text": "두둑", "side": "left", "beat": 1}, {"text": "선지급!", "side": "right", "beat": 1}], arrow={"beat": 0},
             beats=[{"say": "두 번째는 돈의 길입니다. 은행에서 빌리는 대신, 고객에게서 돈이 먼저 들어옵니다."},
                    {"say": "앞으로 3개월 동안만 약 90억 달러. 올해 계약의 70%에서 고객이 미리 돈을 냈습니다."}]),
        dict(type="metaphor", mode="pop", chapter=0, label=LBL, title="낡은 줄 알았던 GPU", hl="GPU",
             object={"label": "옛 세대 GPU", "kind": "box", "color": "#55657A"}, tag={"to": "+30~50%", "beat": 1},
             words=[{"text": "아직 쌩쌩", "side": "left", "beat": 1}],
             beats=[{"say": "세 번째는 옛 GPU입니다. 몇 년 된 칩이라 값이 떨어질 줄 알았는데,"},
                    {"say": "이용료가 지난 분기보다 30에서 50% 올랐습니다."},
                    {"say": "원래 계약보다도 비싸게 다시 팔렸죠."}]),
    ]
    for i, x in enumerate(S, 1):
        x["id"] = i
    spec = {"title": "스타일 시험작 — 움직이는 비유 애니메이션", "core_message": "글 대신 움직임으로 비유", "scenes": S, "package": {}, "edit_v10": True}
    (P / "02_script" / "hybrid.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
    (P / "01_research" / "factsheet.md").write_text("# 시험작 팩트시트\n\n사실은 projects/20261112-market-call/01_research/factsheet.md 의 E5(선지급금)·E8(수요 10배)·E9(옛 GPU 가격)에서 그대로. 새 사실 없음.\n", encoding="utf-8")
    print(P, len(S))


if __name__ == "__main__":
    main()
