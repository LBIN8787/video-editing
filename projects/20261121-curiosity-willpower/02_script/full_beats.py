"""script_v5.md → 문단(박자) 목록 → full_beats.json. 문단 하나 = 박자 하나 (●이야기 ○연구 [마디]검은 화면).
python full_beats.py [대본 md] [출력 json]"""
import json, re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
t = (HERE / (sys.argv[1] if len(sys.argv) > 1 else "script_v5.md")).read_text(encoding="utf-8").split("\n---", 1)[0]
beats, ch = [], 0
for l in t.splitlines():
    m = re.match(r"## (\d+)\. (.+?)(?: \[|$)", l)
    if m: ch = int(m.group(1)); title = m.group(2); continue
    if "title" not in dir(): title = ""
    k = {"●": "story", "○": "fact"}.get(l[:1]) or ("madi" if l.startswith("[마디]") else None)
    if l.startswith("🎮"):
        k = "play"
    if l.startswith("⬛"):   # ⬛ 「장 제목」 = 소리 없는 장 표지, ⬛ "질문" = 소리 없는 질문 카드, 그 밖의 ⬛ = 읽는 마디(검은 화면)
        body = l[1:].strip()
        if body.startswith("「") or body.startswith('"') or body.startswith("마디:"):
            beats.append({"id": len(beats) + 1, "ch": max(ch, 1), "chapter": title if ch else "", "kind": "card", "silent": 2.2,
                          "text": body.replace("마디:", "").strip().strip('「」"')})
            continue
        k = "madi"; l = "[마디] " + body
    if l.startswith("🎮"):
        l = "● " + l[1:].strip()
    if k and ch:
        txt = re.sub(r"^(●|○|\[마디\])\s*", "", l).strip()
        txt = re.sub(r"\s*\((F[0-9F·~]+)\)", "", txt).strip()   # 팩트시트 번호는 읽지 않음
        beats.append({"id": len(beats) + 1, "ch": ch, "chapter": title, "kind": k, "text": txt})
for i, b in enumerate(beats):   # 장 표지는 다음 장에 속함
    if b["kind"] == "card" and i + 1 < len(beats) and (beats[i + 1]["ch"] != b["ch"] or not b["chapter"]):
        b["ch"], b["chapter"] = beats[i + 1]["ch"], beats[i + 1]["chapter"]
(HERE / (sys.argv[2] if len(sys.argv) > 2 else "full_beats.json")).write_text(json.dumps(beats, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(beats), "박자,", sum(len(b["text"]) for b in beats), "자")
