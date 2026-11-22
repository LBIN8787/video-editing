"""커닝 편: script_v2.md -> beats.json (◇ 설명 박자 추가).
script_v1.md|script_v2.md -> beats.json (문단 = 박자). ● 이야기 ○ 사실 ⬛ 읽는 마디(검은 화면) 🎮 시청자 참여(v2). `[역할]` 표시·(F..) 번호는 읽지 않음."""
import json, re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
t = (HERE / sys.argv[1]).read_text(encoding="utf-8")
beats, ch, title = [], 0, ""
for l in t.splitlines():
    m = re.match(r"## (\d+)\. (.+)$", l)
    if m: ch, title = int(m.group(1)), m.group(2).strip(); continue
    if not ch or not l or l[0] not in "●○◇⬛🎮": continue
    k = {"●": "story", "○": "fact", "◇": "explain", "⬛": "madi", "🎮": "play"}[l[0]]
    role = (re.search(r"`\[(.+?)\]`", l) or [None, ""])[1]
    txt = re.sub(r"`\[.+?\]`", "", l[1:])
    txt = re.sub(r"\s*\((F[0-9F·~]+[^)]*|재현|F[^)]*)\)", "", txt)
    txt = re.sub(r"〔.+?〕", "", txt).strip()
    beats.append({"id": len(beats) + 1, "ch": ch, "chapter": title, "kind": k, "role": role, "text": txt})
(HERE / sys.argv[2]).write_text(json.dumps(beats, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(beats), "박자,", sum(len(b["text"]) for b in beats), "자")
