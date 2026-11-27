"""v2 대본(remake.json) → 렌더 계획: 문장 하나 = 그림 하나, 같은 그림이 이어지면 한 샷으로(카메라 끊김 없이).
카메라(레퍼런스 측정): 정지 / 밀기 1.13배 / 빼기 / 이동(드묾). 전환은 0.7초 겹침, 첫 1초는 검은 화면에서 밝아짐."""
import json, sys, pathlib
R = json.load(open(sys.argv[1], encoding="utf-8")); proj = pathlib.Path(sys.argv[2])
CAM = {"static": ([0.5, 0.5, 1.0], [0.5, 0.5, 1.0]),
       "push":   ([0.5, 0.5, 1.0], [0.5, 0.47, 0.885]),
       "pull":   ([0.5, 0.47, 0.885], [0.5, 0.5, 1.0]),
       "pan":    ([0.42, 0.5, 0.86], [0.58, 0.5, 0.86])}
lines = []
for sec in R["sections"]:
    for j, ln in enumerate(sec["lines"]):
        lines.append(dict(ln, title=sec.get("title") if j == 0 else None))
shots = []
for i, ln in enumerate(lines):
    base = ln["cam"].rstrip("0123456789")
    if shots and shots[-1]["img"] == ln["img"] and not ln.get("title"):
        shots[-1]["say"][1] = i; continue          # 같은 그림 → 같은 샷을 늘림 (움직임은 첫 문장의 것)
    f, t = CAM[base]
    s = {"img": ln["img"], "say": [i, i], "cam": {"from": f, "to": t}, "tr": "dissolve", "move": base}
    if ln.get("title"): s["title"] = ln["title"]
    shots.append(s)
shots[0]["tr"] = "fade"; shots[0]["fade_dur"] = 1.0
shots[-1]["fade_out"] = True
plan = {"art_dir": str(proj / "art"), "voice_dir": str(proj / "voice"), "out": str(proj / (sys.argv[3] if len(sys.argv) > 3 else "story.mp4")),
        "subtitle": "plain", "recon": False, "bgm": str(proj / "bgm.wav"), "shots": shots}
(proj / "plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=1), encoding="utf-8")
from collections import Counter
print("문장", len(lines), "샷", len(shots), Counter(s["move"] for s in shots))
