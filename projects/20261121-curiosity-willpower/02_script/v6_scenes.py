"""의지력 편 v6 장면표 (D4 기각 반영: 이야기가 앞, 연구는 실험실 장면으로, 검은 바탕, 그래프 없음).
python v6_scenes.py [장 번호,…] → v6.json  (예: 1,4 = D3 샘플)
화면 = 원화(실험실·서윤) 위에 그 순간 필요한 낱말·숫자만. 기준 화면은 서윤의 냉장고 메모(실험실을 나올 때마다 표시)."""
import json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
beats = json.loads((HERE / "v6_beats.json").read_text(encoding="utf-8"))
only = {int(c) for c in sys.argv[1].split(",")} if len(sys.argv) > 1 else None
A = lambda *shots, **k: dict(mg="art", shots=list(shots), **k)   # [이미지, 시작 kw 번호(-1=처음), 움직임, 화면 위 글]
C = {
 1: A(["kitchen_tl", -1, "in"], ["kitchen_tr", 0, "in"], stamp="밤 11:00", kw=["손은"]),
 2: A(["kitchen_tl", -1, "out"], thought="오늘 참을 만큼 참았으니… 이제 바닥났다", kw=["오늘 참을"]),
 3: A(["lab_tl", 0, "in", "1998"], ["lab_br", 1, "in", "1998"], ["lab16_tl", 2, "left", "그 뒤 · 수천 명"], ["black", 3, "", "2025"],
      first=["kitchen_tl", "out"], kw=["1998년", "퍼즐을 훨씬", "그런데 그 뒤", "2025년"]),
 4: A(["lab16_tl", -1, "in"], ["kitchen_tl", 0, "in"], doors=True, kw=["서윤의 이 밤도"]),
 5: dict(mg="madi"),
 14: dict(mg="memo", marks=[], kw=["'자제력은", "이 메모 옆에"]),
 15: A(["lab16_tl", -1, "in", "2016 · 23개 연구실"], ["lab_tl", 0, "out", "쿠키와 무 — 이번엔 아님"], ["lab16_bl", 1, "in", "같은 이론 · 다른 연구진의 컴퓨터 과제"],
       kw=["쿠키와 무를", "다른 연구진이"]),
 16: dict(mg="etask", kw=["쉬운 집단은", "어려운 집단은", "e가 모음", "두 번째 과제"]),
 17: dict(mg="result", img="lab16_tl", lines=[["계획을 미리 공개 · 원래 이론의 연구자도 검토", 0], ["2,141명", 1], ["효과: 있다 해도 아주 작음", 2], ["오차 범위가 0을 포함", 2.8]],
        mark="q", marks=[], kw=["원래 이론을", "2,141명", "결과는", "메모 옆에"]),
 18: dict(mg="madi"),
}
out = []
for b in beats:
    if only and b["ch"] not in only:
        continue
    sc = {**b, **C[b["id"]]}
    for k in sc.get("kw", []):
        assert k in b["text"], (b["id"], k)
    out.append(sc)
(HERE / "v6.json").write_text(json.dumps({"title": "의지력 편 v6", "scenes": out}, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(out), "장면")
