"""판테온 편 장면 명세: beats.json + 아래 표 → pantheon.json (render_full.py 의 SPEC).
shots: [그림, kw 번호(-1 = 처음부터), 카메라(in·out·left·right), 위 띠 글(선택)] — 같은 그림이 이어지면 카메라 한 번, 글만 바뀜.
그림: 원화 조각 <시트>_tl|tr|bl|br (Drive 영상/20261122-curiosity-pick/art), 실제 사진 photo_* (Wikimedia Commons, Sonse · CC BY 2.0 — 화면 오른쪽 위 출처).
python make_spec.py"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
P = {
 1: dict(mg="art", shots=[["garage_tl", -1, "in"], ["garage_tr", 0, "in"]], kw=["지은 지"]),
 2: dict(mg="art", shots=[["garage_tr", -1, "out"], ["garage_bl", 0, "in", "로마 · 비 오는 날"]], kw=["지금 로마에"]),
 3: dict(mg="art", shots=[["garage_br", -1, "in"], ["dome_tl", 0, "in"]], kw=["천장 한가운데가"]),
 4: dict(mg="art", shots=[["photo_dome", -1, "in", "지름 43m · 콘크리트 돔"], ["photo_dome", 0, "in", "철근 0가닥"], ["dome_br", 1, "in", "약 1,900년"]],
         kw=["철근은", "그리고 지어진"]),
 5: dict(mg="madi"),
 6: dict(mg="words", head="", lines=[["튼튼하기만 해서가 아니다", 0], ["금이 가도 무너지지 않게", 1], ["금을 스스로 메우는 재료", 2]],
         kw=["튼튼하기만", "금이 가도", "로마의 콘크리트에는"]),
 7: dict(mg="art", shots=[["struct_tr", -1, "in", "돔 아래쪽 · 세로 균열"], ["struct_tr", 0, "in", "마르며 줄어듦 + 제 무게"]], kw=["콘크리트가 마르며"]),
 8: dict(mg="art", shots=[["dome_bl", -1, "in"], ["dome_tr", 0, "out"]], kw=["그런데 무너지지"]),
 9: dict(mg="art", shots=[["struct_tl", -1, "in", "아래쪽 두께 6m 넘게"], ["struct_tl", 0, "in", "구멍 둘레 1.2m"],
                         ["struct_bl", 1, "right", "무거운 돌 → 가벼운 화산석"], ["struct_br", 2, "in", "천장 홈 = 무게 덜기"]],
         kw=["위로 갈수록", "아래쪽에는 무거운", "천장을 빼곡히"]),
 10: dict(mg="art", shots=[["struct_tl", -1, "out"], ["struct_tl", 0, "out", "보통 무게였다면 → 힘 약 80% 더"]], kw=["80%쯤"]),
 11: dict(mg="art", shots=[["photo_oculus", -1, "in", "꼭대기는 비워 두었다"]], kw=[]),
 12: dict(mg="madi"),
 13: dict(mg="art", shots=[["rust_br", -1, "in"], ["garage_tl", 0, "in"]], kw=["그 누런 녹은"]),
 14: dict(mg="art", shots=[["rust_tl", -1, "in", "누르는 힘에 강함 · 잡아당기는 힘에 약함"], ["rust_bl", 0, "right"]], kw=["덕분에"]),
 15: dict(mg="art", shots=[["rust_tl", -1, "out"], ["rust_tr", 0, "in", "녹 = 철보다 부피가 크다"], ["rust_tr", 1, "in", "콘크리트가 상하는 가장 흔한 이유"]],
          kw=["녹은 철보다", "콘크리트가 상하는"]),
 16: dict(mg="art", shots=[["garage_tl", -1, "in"]], kw=[]),
 17: dict(mg="art", shots=[["struct_tr", -1, "out", "녹슬 철이 없다"]], kw=[]),
 18: dict(mg="madi"),
 19: dict(mg="art", shots=[["lab_tl", -1, "in"], ["lab_tl", 0, "in", "석회 덩어리"], ["lab_tl", 1, "in", "'대충 섞은 흔적'?"]], kw=["석회 덩어리입니다", "오랫동안"]),
 20: dict(mg="art", shots=[["lab_tr", -1, "in", "MIT · 아드미르 마시치 교수"]], kw=[]),
 21: dict(mg="art", shots=[["lab_tr", -1, "out"], ["lab_tl", 0, "in", "이탈리아 로마 유적 · 2cm 조각"], ["lab_tl", 1, "in", "생석회를 그대로 넣은 흔적"]],
          kw=["2센티미터짜리", "로마인들이 물을"]),
 22: dict(mg="art", shots=[["lab_bl", -1, "in"], ["lab_bl", 0, "in", "일부러 금 → 물 흘려보내기"], ["lab_bl", 1, "in", "생석회 뺀 조각도 똑같이"]],
          kw=["일부러 금을", "생석회만 빼고"]),
 23: dict(mg="art", shots=[["lab_br", -1, "in", "2주 뒤"], ["lab_br", 0, "in", "로마 방식: 메워짐 · 생석회 없음: 계속 샘"]], kw=["생석회를 뺀"]),
 24: dict(mg="art", shots=[["end_bl", -1, "in"], ["end_bl", 0, "in", "물 → 석회가 녹음 → 틈 안에서 다시 굳음"], ["end_bl", 1, "in", "틈을 메울 재료의 창고"],
                          ["photo_dome", 2, "out", "판테온 돔에서는 아직 확인 안 됨"]], kw=["스며든 물이", "하얀 점은 실수가", "다만"]),
 25: dict(mg="madi"),
 26: dict(mg="art", shots=[["dome_br", -1, "out"]], kw=[]),
 27: dict(mg="art", shots=[["history_tl", -1, "in", "609년 · 교회가 되다"], ["history_br", 0, "in"]], kw=["쓰는 사람이"]),
 28: dict(mg="art", shots=[["history_tr", -1, "in", "1600년대 · 교황 우르바노 8세"], ["history_bl", 0, "in", "청동 들보 → 대포"],
                          ["history_tr", 1, "out", "\"야만인도 하지 않은 짓을, 바르베리니가\""]], kw=["그 청동의", "로마 사람들은"]),
 29: dict(mg="art", shots=[["history_br", -1, "in"], ["history_br", 0, "in", "라파엘로가 묻힌 곳"]], kw=["화가 라파엘로도"]),
 30: dict(mg="madi"),
 31: dict(mg="art", shots=[["rust_bl", -1, "right", "누르는 힘도 요즘 고강도 콘크리트보다 약함"], ["dome_br", 0, "out", "남은 건물만 보인다"]], kw=["그리고 우리가"]),
 32: dict(mg="art", shots=[["end_bl", -1, "in", "스스로 메우는 콘크리트 · 상용화 시도"], ["garage_tl", 0, "in"]], kw=["녹물이 번지기"]),
 33: dict(mg="art", shots=[["end_tr", -1, "in"], ["end_tl", 0, "in", "작은 배수구 · 가운데가 살짝 솟은 바닥"], ["end_tr", 1, "out", "막지 않고, 받아서 내보낸다"]],
          kw=["구멍 바로 아래", "막지 않고"]),
 34: dict(mg="art", shots=[["end_br", -1, "in"]], kw=[]),
 35: dict(mg="madi"),
}
beats = json.loads((HERE / "beats.json").read_text(encoding="utf-8"))
scenes = []
for b in beats:
    s = dict(b); s.update(P[b["id"]])
    for k in s.get("kw", []):
        assert k in s["text"], (b["id"], k)
        assert s["text"].count(k) == 1, (b["id"], k, "여러 번")
    scenes.append(s)
(HERE / "pantheon.json").write_text(json.dumps({"title": "철근 하나 없는 1,900년 된 돔은 왜 아직 서 있을까?", "scenes": scenes},
                                              ensure_ascii=False, indent=1), encoding="utf-8")
print(len(scenes), "장면")
