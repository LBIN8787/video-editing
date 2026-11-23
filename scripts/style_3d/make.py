"""스타일 시험작 v2: 어두운 스튜디오 3D 비유 (studio3d). 사실은 20261112-market-call 팩트시트(E5·E8·E9).
    python scripts/style_3d/make.py && python -m ytflow hybrid 20261112-style-3d
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "projects" / "20261112-style-3d"
LBL = "코어위브 3분기 어닝콜 공식 녹취록 (2026.11.10) · 회사 발표"


def main():
    for d in ("01_research", "02_script", "05_edit"):
        (P / d).mkdir(parents=True, exist_ok=True)
    (P / "edit.yaml").write_text("# 스타일 시험작 v2 studio3d (docs/22)\nedit:\n  style: hybrid\n  style_ref: hybrid\n  family: infographic\n  skin: midnight\nformat: longform\n", encoding="utf-8")
    st = P / "state.json"
    if not st.exists():
        st.write_text(json.dumps({"name": P.name, "created": "2026-11-12T00:00:00", "done": [], "approved": []}, indent=2), encoding="utf-8")
    S = [
        dict(type="studio3d", preset="stack", left="공급 가능한 용량", right="검증된 수요", n=10, label=LBL, chapter=0,
             beats=[{"say": "코어위브 CEO는 2027년 말까지 공급할 수 있는 용량보다,"},
                    {"say": "검증된 수요가 10배 많다고 했습니다."}]),
        dict(type="studio3d", preset="swap", out="무담보 채권", **{"in": "고객 선지급금"}, label=LBL, chapter=0,
             beats=[{"say": "돈을 마련하는 방법도 바꿨습니다."},
                    {"say": "담보 없는 채권 대신, 고객이 미리 내는 돈으로. 앞으로 3개월 동안만 약 90억 달러입니다."}]),
        dict(type="studio3d", preset="glow", object="옛 세대 GPU", tag="+30~50%", label=LBL, chapter=0,
             beats=[{"say": "그리고 몇 년 된 옛 GPU는,"},
                    {"say": "이용료가 지난 분기보다 30에서 50% 올랐습니다."}]),
    ]
    for i, x in enumerate(S, 1):
        x["id"] = i
    spec = {"title": "스타일 시험작 v2 — 어두운 스튜디오 3D 비유", "core_message": "글 대신 빛과 물체로", "scenes": S, "package": {}}
    (P / "02_script" / "hybrid.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
    (P / "01_research" / "factsheet.md").write_text("# 시험작 팩트시트\n\n사실은 projects/20261112-market-call/01_research/factsheet.md 의 E5·E8·E9 그대로. 새 사실 없음.\n", encoding="utf-8")
    print(P, len(S))


if __name__ == "__main__":
    main()
