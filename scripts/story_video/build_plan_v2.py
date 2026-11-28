"""v2 대본(story.json) → 렌더 계획: 문장 하나 = 그림 하나, 같은 그림이 이어지면 한 샷으로(카메라 끊김 없이).
카메라 사전(docs/76): 정지·밀기·빼기·이동 + 기울이기·흐르기·조여 오기·빠른 밀기·드러내기 / 렌즈: 초점 맞추기·흔들림·가장자리 조이기 / 전환: 겹침·휙(드묾).
문장에 쓸 수 있는 키: cam(이름, 같은 그림을 이어 쓰면 push2 처럼 숫자), at([x,y] 카메라가 향할 곳), focus(true|초), shake(0~1), vignette(0~1), tr("whip")."""
import json, sys, pathlib
R = json.load(open(sys.argv[1], encoding="utf-8")); proj = pathlib.Path(sys.argv[2])

def cam(name, at):
    x, y = at or (0.5, 0.47)
    return {
        "static":    ([0.5, 0.5, 1.0], [0.5, 0.5, 1.0]),                    # 정지: 말에 집중, 여운, 대사
        "push":      ([0.5, 0.5, 1.0], [x, y, 0.885]),                       # 밀기: 마음속으로 들어감, 깨달음
        "pull":      ([x, y, 0.885], [0.5, 0.5, 1.0]),                       # 빼기: 맥락·고립, 장면을 닫음
        "pan":       ([0.42, 0.5, 0.86], [0.58, 0.5, 0.86]),                 # 이동(오른쪽): 따라가기, 공간 잇기
        "pan_l":     ([0.58, 0.5, 0.86], [0.42, 0.5, 0.86]),                 # 이동(왼쪽): 되돌아봄
        "tilt_up":   ([0.5, 0.6, 0.82], [0.5, 0.4, 0.82]),                   # 올려 기울이기: 커지는 존재, 희망, 위압
        "tilt_down": ([0.5, 0.4, 0.82], [0.5, 0.6, 0.82]),                   # 내려 기울이기: 무너짐, 시선이 떨어짐
        "drift":     ([0.49, 0.5, 0.95], [0.51, 0.49, 0.94]),                # 흐르기: 거의 정지, 긴 여운에 숨만 붙임
        "dread":     ([0.5, 0.5, 1.0], [x, y, 0.76]),                        # 조여 오기: 끝까지 같은 속도로 다가감(불안·진실 직전)
        "snap":      ([0.5, 0.5, 1.0], [x, y, 0.62]),                        # 빠른 밀기(크래시 줌): 충격의 한 단어 (편당 0~2번)
        "reveal":    ([x, y, 0.5], [0.5, 0.5, 1.0]),                         # 드러내기: 작은 단서에서 시작해 전체로 (반전·규모)
    }[name]
lines = []
for sec in R["sections"]:
    for j, ln in enumerate(sec["lines"]):
        lines.append(dict(ln, title=sec.get("title") if j == 0 else None))
shots = []
for i, ln in enumerate(lines):
    base = ln["cam"].rstrip("0123456789")
    if shots and shots[-1]["img"] == ln["img"] and not ln.get("title") and not ln.get("new_shot"):
        shots[-1]["say"][1] = i; continue          # 같은 그림 → 같은 샷을 늘림 (움직임은 첫 문장의 것)
    f, t = cam(base, ln.get("at"))
    s = {"img": ln["img"], "say": [i, i], "cam": {"from": f, "to": t}, "tr": ln.get("tr", "dissolve"), "move": base}
    if base == "dread": s["cam"]["ease"] = "linear"
    if base == "snap": s["cam"]["snap"] = float(ln.get("snap_at", 0.6))
    if ln.get("focus"): s["focus"] = {"from": float(ln["focus"]) if not isinstance(ln["focus"], bool) else 0.2, "dur": 1.4, "blur": 14}
    for k in ("shake", "vignette"):
        if ln.get(k): s[k] = ln[k]
    if ln.get("title"): s["title"] = ln["title"]
    shots.append(s)
shots[0]["tr"] = "fade"; shots[0]["fade_dur"] = 1.0
shots[-1]["fade_out"] = True
plan = {"art_dir": str(proj / "art"), "voice_dir": str(proj / "voice"), "out": str(proj / (sys.argv[3] if len(sys.argv) > 3 else "story.mp4")),
        "subtitle": "plain", "recon": False, "bgm": str(proj / "bgm.wav"), "shots": shots}
(proj / "plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=1), encoding="utf-8")
from collections import Counter
print("문장", len(lines), "샷", len(shots), Counter(s["move"] for s in shots))
