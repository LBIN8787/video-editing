"""의지력 편 v13 장면표 (v12 + 결론만, 2026-11-21 · 심리학 고양이 문법: '당신'이 주인공, 시청자 참여 과제, 장 표지, 흰 선 그림).
화면: 삽화(GPT 원화) + 참여 화면(검은 바탕) + 검은 화면 한 줄. 그래프·표 없음. 장면 위 글은 그 순간의 낱말 하나 정도.
python v12_scenes.py → v12.json
shots: [이미지, 시작 kw 번호(-1=처음), 카메라(in|out|left|right|still), 장면 위 한 줄]"""
import json
from pathlib import Path
HERE = Path(__file__).resolve().parent
beats = json.loads((HERE / "v13_beats.json").read_text(encoding="utf-8"))
A = lambda *shots, **k: dict(mg="art", shots=list(shots), **k)
W = lambda lines, kw, head="": dict(mg="words", head=head, lines=lines, kw=kw)
CARD = dict(mg="card")
WORDS_E = ["table", "read", "pencil", "beach", "letter", "queen", "lemon", "ocean", "seven", "tree"]
C = {
 1: CARD,
 2: A(["kitchen_tl", -1, "in"], ["kitchen_tr", 1, "in"], stamp="밤 11:00", diet="다이어트 14일째", kw=["다이어트", "눈은"]),
 3: A(["cafe_tl", -1, "in"], ["cafe_bl", 0, "in"], ["day_tr", 1, "in"], ["day_bl", 2, "in"], kw=["아메리카노를", "점심엔", "퇴근길엔"]),
 4: A(["kitchen_tl", -1, "out"], think="오늘은 의지력을 다 썼어", thinkk=0, kw=["'오늘은"]),
 5: dict(mg="ask", img="kitchen_tr", q="의지력은 정말 쓰면 닳을까?", kw=["의지력은 정말"]),
 6: CARD,
 7: W([["'참을수록 의지가 닳는다'", 0], ["→ 반만 맞다", 1], ["잘 참는 사람들은, 애초에 덜 참는다", 2]], ["'참을수록", "반만", "그리고 정말"]),
 8: CARD,
 9: A(["lab_bl", -1, "in", "1998 · 로이 바우마이스터"], ["lab_tl", 0, "in"], kw=["갓 구운"]),
 10: A(["lab_tl", -1, "out"], ["lab_tr", 0, "in"], kw=["무를 받은 학생"]),
 11: A(["lab_bl", -1, "in"], ["lab_br", 0, "in"], kw=["포기하고 싶으면"]),
 12: dict(mg="times", img="lab_br", head="포기하고 종을 울리기까지", rows=[["쿠키를 먹은 학생", "19분"], ["쿠키를 참은 학생", "8분"]], kw=["19분", "8분"]),
 13: A(["lab_tr", -1, "in"], ["lab_tr", 1, "still", "'자아 고갈'"], battery={"from": 1, "to": .25, "at": 0, "dur": 3}, kw=["배터리 같은", "'자아 고갈'"]),
 14: A(["cafe_bl", 0, "still"], ["day_tr", 1, "still"], ["day_bl", 2, "still"], ["kitchen_tr", 3, "in"], first=["kitchen_tl", "still"],
       battery={"from": .9, "to": .05, "at": 0, "dur": 4.5}, kw=["라테,", "케이크,", "코트.", "치킨 앞에서는"]),
 15: CARD,
 16: dict(mg="play_e", phase="press", words=WORDS_E, hold=7, kw=[]),
 17: dict(mg="play_e", phase="stop", words=WORDS_E, hold=8, kw=[]),
 18: A(["lab16_tl", -1, "in", "2016 · 23개 연구실 · 2천 명 넘게"], kw=[]),
 19: A(["lab16_tl", 0, "out", "참은 사람 vs 안 참은 사람 → 차이 거의 없음"], ["lab2125_tl", 1, "in", "2021 · 36개 연구실 → 마찬가지"], first=["lab16_bl", "still"],
       kw=["차이가 거의", "2021년"]),
 20: W([["잠깐 참는 정도로는,", 0], ["배터리가 닳지 않았다", 0]], ["잠깐"]),
 21: CARD,
 22: A(["day2_tr", -1, "in"], ["lab2125_bl", 0, "in", "2025 · 훨씬 오래 참으면?"], kw=["2025년, 바로"]),
 23: dict(mg="play_dot", hold=8, kw=[]),
 24: A(["lab2125_bl", -1, "out", "30~40분 동안"], ["lab2125_br", 0, "in", "그다음 · 멈추는 과제"], ["lab2125_br", 1, "still", "오래 참은 사람들 → 멈춰야 할 때 더 자주 누름"],
       kw=["버튼을 누르다가", "오래 참은 사람들은"]),
 25: A(["day2_bl", -1, "in"], ["kitchen_tl", 0, "in", "이유는 배터리가 아닐 수도"], kw=["그런데 그 이유가"]),
 26: CARD,
 27: A(["kitchen_tr", -1, "in", "마이클 인즐리트 · 줄어드는 게 아니라, 옮겨 간다"], kw=[]),
 28: A(["day2_br", -1, "in", "아침 · '열량 덩어리'"], ["kitchen_tr", 0, "in", "밤 11시 · '맛있겠다'"], kw=["그런데 밤 11시의"]),
 29: A(["kitchen_tl", -1, "out"], kw=[]),
 30: CARD,
 31: A(["life_tl", -1, "in", "2012 · 성인 205명 · 일주일 · 호출기"], ["life_tr", 0, "in"], kw=["호출기가 울릴"]),
 32: A(["life_bl", -1, "in", "참아 낸 횟수가 오히려 적었다"], ["life_bl", 0, "still", "참을 일 자체를 덜 만든다"], ["life_bl", 1, "still", "몸에 밴 좋은 습관"],
       kw=["참을 일 자체를", "그 자리에는"]),
 33: W([["브레이크가 좋은 사람이 아니라", 0], ["브레이크 밟을 일이 적은 길로 다니는 사람", 1]], ["브레이크가 좋은", "브레이크 밟을"]),
 34: CARD,
 35: A(["kitchen_bl", -1, "in"], kw=[]),
 36: A(["kitchen_bl", -1, "still", "① 길을 바꾸기 — 참을 일을 줄인다"], ["kitchen_tr", 0, "in", "치킨은 냉장고 맨 안쪽에"], ["day_bl", 1, "in", "장바구니 앱은 첫 화면에서 치우기"],
       kw=["남은 치킨은", "장바구니 앱은"]),
 37: A(["kitchen_br", -1, "in", "② '만약에'를 정해 두기"], ["kitchen_br", 0, "still", "연구 94건 · 목표를 더 잘 이뤘다"], kw=["94건"]),
 38: W([["만약 밤 10시가 넘어 배가 고프면 → 물 한 잔부터", 0], ["만약 장바구니를 열고 싶어지면 → 결제는 하루 뒤에", 1]], ["\"만약 밤", "\"만약 장바구니"], head="예를 들면"),
 39: CARD,
 40: A(["kitchen_tl", -1, "in"], stamp="밤 11:00", kw=[]),
 41: A(["life_br", -1, "in"], kw=[]),
 42: dict(mg="ask", img="life_br", q="오늘 밤, 어떤 '만약에'를 적고 싶나요?", qs=70, qy=860, kw=["어떤"]),
 43: dict(mg="madi"),
}
out = []
for b in beats:
    sc = {**b, **C[b["id"]]}
    for k in sc.get("kw", []):
        assert k in b["text"], (b["id"], k)
    out.append(sc)
(HERE / "v13.json").write_text(json.dumps({"title": "의지력은 정말 쓰면 닳을까? 과학자들의 실험이 엇갈린 이유", "scenes": out}, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(out), "장면")
