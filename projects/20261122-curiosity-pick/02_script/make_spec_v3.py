"""판테온 편 v3 장면 명세: v2 명세(make_spec_v2.P)에서 검은 바탕 돔 단면 도식(mg=dome) 박자를 모두 지우 화풍 설계 스케치 삽화(plan1~4 시트)로 바꿈.
v2 D4 기각(2026-11-22 "중간중간 지우의 이미지화풍이 너무달라서 확 깨") → build1·build2·build3·lime 시트를 지우 기준 그림(jiwoo_ref)으로 다시 그림(art_sheets_v3.json, 칸 이름은 그대로).
추가 지시(2026-11-22 "중간중간 인포그래픽 설명도 삽화로 … 어떤 느낌으로 설계했는지 보여주는 식으로 … 이해만 되면") → 도식 대신 plan 시트(화살표는 그림 안 손그림, 짧은 이름표는 위 띠 글, 숫자는 말로).
python make_spec_v3.py  (대본·박자 = beats_v2.json 그대로)"""
import json, importlib.util, io, contextlib
from pathlib import Path
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("v2", HERE / "make_spec_v2.py"); v2 = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(v2)
P = {k: dict(v) for k, v in v2.P.items()}
A = lambda shots, kw: dict(mg="art", shots=shots, kw=kw)
P.update({
 8: A([["build1_tl", -1, "in"], ["plan1_tl", 0, "in", "지름 43m · 시내버스 4대 길이"], ["plan1_tl", 1, "in", "높이도 43m · 15층쯤"], ["plan1_tl", 2, "in", "공 하나가 꼭 들어가는 방"]],
      ["시내버스", "아파트로", "커다란 공"]),
 10: A([["build1_br", -1, "in"], ["plan1_tr", 0, "in", "제 무게에 눌린다"], ["plan1_tr", 1, "in", "치마 밑단이 퍼지듯"]], ["꼭대기 쪽은", "바깥으로"]),
 11: A([["plan4_br", -1, "in", "누르는 힘에 강함 · 잡아당기는 힘에 약함"], ["plan1_bl", 1, "in", "벌어지는 아래에 세로 금"]], ["누르는 힘에는", "세로로 금이"]),
 13: A([["build2_tl", -1, "in", "시도 2"], ["build2_tl", 0, "in", "밑단 두께 6m 넘게"], ["plan1_br", 1, "in", "어른 키 세 사람으로도 모자람"],
       ["build2_tr", 2, "in", "계단 고리로 밑단을 누른다"]], ["6미터가", "어른 키", "계단처럼"]),
 14: A([["plan2_tl", -1, "in", "위로 갈수록 얇게"], ["plan2_tl", 0, "in", "6m → 1.2m, 5분의 1쯤"]], ["1.2미터"]),
 15: A([["build2_bl", -1, "in"], ["plan2_tr", 0, "in", "아래 · 무거운 돌"], ["plan2_tr", 1, "in", "중간 · 벽돌"], ["plan2_tr", 2, "in", "꼭대기 · 물에 뜨는 화산석"],
       ["plan4_bl", 3, "in", "위로 갈수록 가볍게"]], ["아래에는", "중간에는", "꼭대기 가까이에는", "위로 갈수록"]),
 16: A([["build2_br", -1, "in"], ["plan2_bl", 0, "in"], ["plan2_bl", 1, "in"], ["plan4_bl", 2, "in", "돔도 똑같다"]], ["맨 위에", "거꾸로", "돔도 똑같습니다"]),
 17: A([["build3_tl", -1, "in"], ["build3_tl", 0, "in", "다섯 줄 × 스물여덟 개"], ["plan2_br", 1, "in", "천장 홈 = 무게 덜기"]], ["다섯 줄", "그만큼 무게가"]),
 18: A([["plan3_tl", -1, "in", "전부 보통 무게 콘크리트였다면?"], ["plan3_tl", 0, "in", "구조에 걸리는 힘 약 80% 더"]], ["80%쯤"]),
 20: A([["build3_tr", -1, "in"], ["build3_tr", 0, "in", "가장 높이, 가장 멀리 매달리는 자리"], ["plan3_tr", 1, "in", "덮지 않는다"],
       ["photo_oculus", 2, "in", "지름 약 9m · 하늘이 그대로"]], ["가장 멀리", "덮지 않기로", "지름 9미터쯤"]),
 21: A([["build3_bl", -1, "in"], ["plan3_bl", 1, "in"], ["plan3_bl", 2, "in", "막지 않고, 받아서 흘려보낸다"]], ["그럼 비는", "바닥을", "막지 않고"]),
 24: A([["struct_tr", -1, "in"], ["struct_tr", 0, "in", "실제 판테온 · 아래쪽 세로 균열"], ["struct_tr", 1, "in", "마르며 줄어듦 + 제 무게"],
       ["plan3_br", 2, "in", "시도 1의 그 벌어지는 힘"]], ["아래쪽에서부터", "콘크리트가 마르며", "첫 번째 시도에서"]),
 25: A([["plan4_tl", -1, "in"], ["plan4_tl", 0, "in", "금은 벌어지는 아래에만"], ["plan4_tl", 1, "in", "위쪽은 서로 누르며 버팀"], ["plan4_tl", 2, "in", "밑단과 고리가 붙잡는다"],
       ["build3_br", 3, "in"]], ["금은 아래쪽", "서로를 꽉", "두꺼운 밑단과", "가벼워진 지붕은"]),
 39: A([["end_tl", -1, "in"], ["plan4_tr", 1, "in", "두꺼운 밑단 · 가벼워지는 지붕 · 비워 둔 꼭대기"], ["end_tr", 2, "in"]], ["지우는 다시", "두꺼운 밑단,", "처음 들어왔을"]),
})
assert not [k for k, v in P.items() if v["mg"] == "dome"], "도식 박자가 남음"
beats = json.loads((HERE / "beats_v2.json").read_text(encoding="utf-8"))
scenes = []
for b in beats:
    s = dict(b); s.update(P[b["id"]])
    for k in s.get("kw", []):
        assert k in s["text"] and s["text"].count(k) == 1, (b["id"], k)
    for sh in s.get("shots", []):
        assert sh[1] < len(s.get("kw", [])), (b["id"], sh)
    scenes.append(s)
(HERE / "pantheon_v3.json").write_text(json.dumps({"title": "철근 하나 없는 1,900년 된 돔은 왜 아직 서 있을까?", "version": "v3", "scenes": scenes},
                                                 ensure_ascii=False, indent=1), encoding="utf-8")
print(len(scenes), "장면")
