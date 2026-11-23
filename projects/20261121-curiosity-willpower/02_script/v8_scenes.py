"""의지력 편 v8 장면표 (서윤의 하루가 뼈대, 실험은 '그날 실험실' 삽화, 검은 바탕, 그래프 없음).
python v8_scenes.py [장 번호,…] → v8.json"""
import json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
beats = json.loads((HERE / "v8_beats.json").read_text(encoding="utf-8"))
only = {int(c) for c in sys.argv[1].split(",")} if len(sys.argv) > 1 else None
A = lambda *shots, **k: dict(mg="art", shots=list(shots), **k)
C = {
 1: A(["kitchen_tl", -1, "in"], ["kitchen_tr", 0, "in"], stamp="밤 11:00", kw=["손은"]),
 2: dict(mg="speak", img="kitchen_tl", say="오늘은 진짜 의지력을 다 썼어", kw=[]),
 3: dict(mg="ask", img="kitchen_tr", q="의지력은 정말 쓰면 닳을까?", kw=["의지력은 정말"]),
 4: A(["lab_tl", 0, "in", "쿠키와 무 한 접시"], ["lab16_tl", 1, "left", "그 뒤로 수천 명"], first=["kitchen_tl", "out"], kw=["쿠키와 무", "그 뒤로"]),
 5: dict(mg="rewind", from_="", seq=["day_br", "day_bl", "day_tr", "day_tl"], stamp="오전 9:30", kw=["아침부터"]),
 6: A(["day_tl", -1, "in"], stamp="오전 9:30", kw=[]),
 7: A(["day_tl", -1, "out"], kw=[]),
 8: A(["lab_bl", -1, "in", "1998 · 케이스웨스턴리저브대학 · 학생 67명"], kw=[]),
 9: A(["lab_tl", -1, "in"], ["lab_tr", 0, "in"], kw=["어떤 학생은 쿠키를"]),
 10: A(["lab_bl", -1, "in"], ["lab_br", 0, "in", "잰 것 · 종을 울리기까지 버틴 시간"], kw=["종을 울리기까지"]),
 11: dict(mg="times", img="lab_br", head="포기하고 종을 울리기까지", rows=[["쿠키를 먹은 학생", "19분"], ["음식 없이", "21분"], ["쿠키를 참은 학생", "8분"]],
        foot="절반도 안 되는 시간", kw=["19분", "21분", "8분", "절반도"]),
 12: A(["lab_tr", -1, "in", "'자아 고갈'"], kw=[]),
 13: A(["day_tl", -1, "out"], kw=[]),
}
out = []
for b in beats:
    if only and b["ch"] not in only:
        continue
    sc = {**b, **C[b["id"]]}
    if sc.get("from_") is not None:
        sc["from"] = "kitchen_tl"; sc.pop("from_")
    for k in sc.get("kw", []):
        assert k in b["text"], (b["id"], k)
    out.append(sc)
(HERE / "v8.json").write_text(json.dumps({"title": "의지력 편 v8", "scenes": out}, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(out), "장면")
