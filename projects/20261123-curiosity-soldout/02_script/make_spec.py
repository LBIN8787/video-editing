"""품절 임박 편 장면 명세: beats.json(← beats.py script_v2.md) + 아래 표 → soldout.json (render_full.py 의 SPEC, 화면 soldout_overlay.html).
shots: [조각, kw 번호(-1 = 처음부터), 카메라(in·out·still·left·right·z=휴대폰 화면으로 다가감), 위 띠 글, 말풍선]
ui: 지우의 휴대폰 화면(지어낸 쇼핑 앱 — 원화의 빈 화면 위에만): timer [남은 초, kw], stock [[숫자, kw]...], toast kw, zero kw
fx: 원화를 어둡게 깔고 그 위 설명 겹(rows·dots·clock·stock·rate, soldout_overlay.html FX)
화면의 네 자리: 이야기 = 지우 원화 / 설명 = fx 모션그래픽(원화 위) / 증거 = 실제 논문 첫 장(ev_*) / 마디 = 검은 화면 한 줄.
python make_spec.py"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCR = json.loads((HERE / "screens.json").read_text(encoding="utf-8"))
UIROT = {"room1_br": [985, 91, 700, 1435, 7.28]}   # 엄지 클로즈업: 화면 위쪽은 화면 밖, 결제 버튼이 엄지 아래에 오게
A = lambda shots, kw, **k: dict(mg="art", shots=shots, kw=kw, **k)
P = {
 1: A([["room1_br", -1, "in"], ["room1_tr", 1, "in"]], ["'3개 남음'이라는", "여러분도"], ui=dict(stock=[[3, 0]])),
 2: A([["room1_tl", -1, "in"], ["room1_bl", 0, "z"]], ["화면에는"], stamp="블랙프라이데이 · 밤 11:50", ui=dict()),
 3: A([["room2_tl", -1, "in"], ["room2_tr", 1, "in"], ["room1_bl", 2, "z"]], ["'조금", "그런데 오늘", "가격 아래", "'3개 남음'.", "그 옆에는", "9분 59초,"],
      think="조금 더 생각해 보자", thinkk=0, thinku=1, ui=dict(stock=[[5, 2], [3, 3]], toast=4, timer=[599, 5])),
 4: A([["room1_br", -1, "still"], ["room2_bl", 0, "out"], ["room2_br", 1, "in"]], ["패딩은", "그런데 왜"],
      ui=dict(stock=[[3, -1]], toast=-1, timer=[596, -1])),
 5: A([["room2_bl", -1, "in", "패딩 · 두 주 전과 그대로"], ["room1_bl", 0, "z"], ["room1_bl", 1, "z", "줄어드는 건 '기회'"]], ["달라진 건", "그 화면 속에서,"],
      ui=dict(stock=[[3, -1]], toast=-1, timer=[589, -1])),
 6: A([["room1_br", -1, "still"], ["cookie1_tl", 0, "in"]], ["쿠키 병"], ui=dict(stock=[[3, -1]], toast=-1, timer=[581, -1])),
 7: A([["cookie1_tl", -1, "in"], ["cookie1_tl", 0, "in", "쿠키 10개"], ["cookie1_tr", 1, "in", "쿠키 2개"]], ["열 개", "이번에는"], hold=1.2),
 8: A([["ev_worchel", -1, "in", "1975 · 워첼·리·아데월레 논문"], ["cookie1_bl", 0, "in", "미국의 한 대학 실험실"], ["cookie1_tl", 1, "in", "10개"], ["cookie1_tr", 2, "in", "2개"]],
      ["미국의 한", "열 개,", "두 개가"]),
 9: A([["cookie1_br", -1, "in"]], ["맛보고", "맛있었나요.", "매력적인가요.", "더 먹고"],
      fx=[dict(type="rate", kw=1, cols=[["cookie1_tl", "10개 병"], ["cookie1_tr", "2개 병"]],
               rows=[["맛", 1, ["", ""]], ["매력", 2, ["", ""]], ["더 먹고 싶음", 3, ["", ""]]])]),
 10: A([["cookie2_tl", -1, "in"]], ["두 개짜리", "매력적이고", "더 먹고"],
       fx=[dict(type="rate", kw=1, cols=[["cookie1_tl", "10개 병"], ["cookie1_tr", "2개 병"]],
                rows=[["맛", 1, ["", ""]], ["매력", 1, ["", "↑"]], ["더 먹고 싶음", 1, ["", "↑"]]], mk=[1, 1, 2])]),
 11: A([["cookie2_tl", -1, "in"], ["cookie2_tr", 2, "in", "같은 쿠키"]], ["맛 점수만은", "차이가", "모두 같은"],
       fx=[dict(type="rate", kw=0, until=2, cols=[["cookie1_tl", "10개 병"], ["cookie1_tr", "2개 병"]],
                rows=[["맛", 0, ["=", "="]], ["매력", 0, ["", "↑"]], ["더 먹고 싶음", 0, ["", "↑"]]], mk=[1, 0, 0])]),
 12: dict(mg="madi"),
 13: A([["room1_bl", -1, "z"], ["cookie2_bl", 3, "in"]], ["5였던", "3으로", "옆에는", "같은 실험에,"],
       ui=dict(stock=[[5, -1], [3, 1]], toast=2, timer=[421, -1])),
 14: A([["cookie1_tl", -1, "in", "처음엔 10개"], ["cookie2_bl", 0, "in"], ["cookie2_br", 1, "in", "10개 → 2개"]], ["문이 열리고", "그는 학생"]),
 15: A([["cookie3_tl", -1, "in", "숨겨 둔 버튼 · 짜인 장면"], ["cookie3_tr", 0, "in"]], ["학생은", "열 개였던", "두 개가"],
       fx=[dict(type="dots", kw=1, n=10, cols=5, gap=150, r=48, cy=470, cookie=True, keep=2, kwHi=2, hiText="10개 → 2개", hiCol="#e0ad4c")]),
 16: A([["cookie3_tr", -1, "in"]], ["처음부터", "더 먹고", "값도"],
       fx=[dict(type="rate", kw=0, cw=330, cols=[["cookie1_tl", "처음부터 10개"], ["cookie1_tr", "처음부터 2개"], ["cookie2_br", "10개 → 2개"]],
                rows=[["더 먹고 싶음", 1, ["", "↑", "↑↑"]], ["값", 2, ["", "", "↑"]]])]),
 17: A([["cookie2_bl", -1, "in"], ["cookie3_bl", 1, "in", "", "실수로 가져갔네요", 1380, 200], ["cookie3_br", 2, "in", "", "참가자들이 많이 먹어서요", 1300, 200]],
       ["두 가지", "\"제가", "아니면,"]),
 18: A([["cookie3_br", -1, "in"], ["cookie4_tl", 2, "in", "연구자들의 풀이"]], ["남들이 먹어서", "더 원했습니다.", "다들 먹는"],
       fx=[dict(type="rate", kw=0, until=2, cols=[["cookie3_bl", "실수로 줄어듦"], ["cookie3_br", "남들이 먹어서 줄어듦"]],
                rows=[["더 먹고 싶음", 0, ["", "↑"]]], mk=[1])]),
 19: A([["cookie3_tr", -1, "in", "연구자들의 풀이"], ["ev_barton", 0, "in", "2022 · 연구 131건을 모은 분석"], ["cookie4_tr", 1, "in", "대부분 가상의 상황에서 물어본 연구"]],
       ["그 뒤에", "대부분은"]),
 20: A([["room1_bl", -1, "still"]], ["적다.", "눈앞에서", "남들이", "'3개", "5에서", "그리고"],
       ui=dict(stock=[[3, -1]], toast=-1, timer=[383, -1]),
       fx=[dict(type="rows", kw=0, head="지우의 화면", rows=[["적다", "'3개 남음'", 0, 3], ["눈앞에서 줄었다", "5 → 3", 1, 4], ["남들이 가져가서", "'방금 2명이 구매'", 2, 5]])]),
 21: dict(mg="madi"),
 22: A([["room3_tl", -1, "in"], ["room1_bl", 0, "z"], ["room3_tr", 1, "in"]], ["저 3과", "진짜일까요?"],
       ui=dict(stock=[[3, -1]], toast=-1, timer=[301, -1])),
 23: A([["ev_mathur", -1, "in", "2019 · 프린스턴대 등"], ["office_bl", 0, "in", "쇼핑 사이트 약 11,000곳"], ["room3_br", 1, "in", "거꾸로 가는 시계 393개"],
        ["office_br", 2, "in", "같은 사이트를 여러 번 다시"]], ["프로그램으로", "거꾸로 가는", "연구진은 같은"]),
 24: A([["room3_br", -1, "still", "157개"]], ["157개는", "시간이 끝나도"],
       fx=[dict(type="clock", kw=0, mode="reset", **{"from": 3}, resetTo=599, cap="0이 되면 처음으로 · 또는 끝나도 할인 그대로")]),
 25: A([["room1_bl", -1, "z"]], [], ui=dict(stock=[[3, -1]], toast=-1, timer=[279, -1])),
 26: A([["office_br", -1, "in", "재고 숫자를 꾸며 낸 곳 17곳"], ["office_br", 0, "still", "16곳 · 미리 정해 둔 일정대로"], ["office_br", 1, "still", "1곳 · 열 때마다 무작위"]],
       ["열여섯 곳은", "한 곳은"],
       fx=[dict(type="stock", kw=0, until=1, mode="schedule", **{"from": 5}), dict(type="stock", kw=1, mode="random")]),
 27: A([["cookie2_br", -1, "in", "눈앞에서 줄어드는 숫자"], ["cookie2_br", 0, "still", "그 장면을 일정표로"]], ["일정표로"],
       fx=[dict(type="stock", kw=0, mode="schedule", **{"from": 5})]),
 28: A([["office_tl", -1, "in", "2026 · 공정거래위원회·한국소비자원"], ["office_tr", 0, "in", "'시간제한 할인' 상품 535개"], ["office_tr", 1, "still", "108개 · 다섯 개 가운데 하나"]],
       ["'시간제한", "108개,"],
       fx=[dict(type="dots", kw=1, n=5, cols=5, gap=190, r=60, cy=480, hi=1, kwHi=1, hiText="할인이 끝난 뒤에도 같거나 더 쌌음")]),
 29: A([["room4_tr", -1, "in", "영국 소비자단체 Which? · 175개 · 한 해 동안"], ["room4_tr", 0, "still", "열 개 가운데 아홉 넘게 (94%)"]], ["열 개 가운데"],
       fx=[dict(type="dots", kw=0, n=10, cols=10, gap=140, r=44, cy=480, hi=9, kwHi=0, stagger=.04, hiText="다른 때에도 같거나 더 쌌음")]),
 30: A([["room4_bl", -1, "in"], ["room4_br", 0, "in"]], ["다만"]),
 31: dict(mg="madi"),
 32: A([["room4_br", -1, "in"], ["cookie4_bl", 0, "in"]], ["쿠키 실험에는"]),
 33: A([["cookie4_bl", -1, "in", "두 번째 실험"]], ["66명", "13명이"],
       fx=[dict(type="dots", kw=0, n=66, cols=11, gap=78, r=26, cy=470, hi=13, kwHi=1, stagger=.012, hiCol="#e0ad4c", hiText="13명 · 실험의 뜻을 알아챔")]),
 34: A([["cookie4_br", -1, "in", "13명: 줄어든 병의 쿠키를 가장 낮게"], ["cookie4_br", 0, "still", "사람 수가 적어 확실한 결과는 아님"]], ["사람 수가"]),
 35: A([["cookie4_br", -1, "still"]], ["무슨 장면인지", "일어나지"],
       fx=[dict(type="rows", kw=0, head="줄어든 병이 더 좋아 보였나", rows=[["알아채지 못한 사람들", "실험 1과 비슷한 쪽", 0, 0], ["알아챈 13명", "일어나지 않음", 0, 1]])]),
 36: A([["room2_br", -1, "in"], ["room2_br", 0, "in", "연구가 시험한 방법은 아님"]], ["연구가 시험해"]),
 37: A([["room5_tl", -1, "in", "첫째 · 이름 붙이기"], ["room1_bl", 0, "z"], ["room5_tl", 1, "in", "'서두르라는 신호'"]], ["'3개 남음'과", "그러니 이름은"],
       ui=dict(stock=[[3, -1]], toast=-1, timer=[240, -1])),
 38: A([["room5_tr", -1, "in", "둘째 · 질문 바꾸기"], ["room5_tr", 0, "in", "", "백 개 남아 있어도 살까?", 1300, 200], ["cookie1_br", 1, "in", "맛을 묻기"]],
       ["\"이게", "쿠키로"]),
 39: A([["room1_tl", -1, "in"], ["room1_bl", 0, "z"]], ["59초,", "2가"], stamp="밤 11:59",
       ui=dict(stock=[[3, -1], [2, 1]], toast=-1, timer=[59, 0])),
 40: A([["room5_bl", -1, "in"], ["room5_br", 0, "in", "", "백 개 남아 있어도, 살까?", 1300, 200]], ["속으로"],
       ui=dict(stock=[[2, -1]], toast=-1, timer=[50, -1])),
 41: A([["room6_tl", -1, "in"], ["room6_bl", 0, "in"]], ["답이 어느"]),
 42: A([["room6_tr", -1, "still"], ["room6_br", 1, "in"]], ["0이 됩니다.", "그 뒤 화면이"],
       ui=dict(stock=[[2, -1]], toast=-1, timer=[1.0, -1], zero=0)),
 43: A([["room6_br", -1, "out"]], []),
 44: dict(mg="madi"),
}
beats = json.loads((HERE / "beats.json").read_text(encoding="utf-8"))
assert len(beats) == len(P), (len(beats), len(P))
scenes = []
for b in beats:
    s = dict(b); s.update(P[b["id"]])
    assert (s["mg"] == "madi") == (b["kind"] == "madi"), b["id"]
    for k in s.get("kw", []):
        assert k in s["text"] and s["text"].count(k) == 1, (b["id"], k)
    nk = len(s.get("kw", []))
    for sh in s.get("shots", []):
        assert sh[1] < nk, (b["id"], sh)
    for f in s.get("fx", []):
        assert f["kw"] < nk, (b["id"], f)
    if "ui" in s:
        s["scr"] = {sh[0]: SCR[sh[0]] for sh in s["shots"] if sh[0] in SCR and SCR[sh[0]].get("area", 0) > 0.03 and "rot" in SCR[sh[0]]}   # 작은 화면(먼 휴대폰)은 그대로 빛나게
        s["uirot"] = {k: v for k, v in UIROT.items() if k in s["scr"]}
    scenes.append(s)
(HERE / "soldout.json").write_text(json.dumps({"title": "'품절 임박'을 보면 왜 손이 먼저 나갈까", "version": "v1", "scenes": scenes},
                                             ensure_ascii=False, indent=1), encoding="utf-8")
print(len(scenes), "장면")
