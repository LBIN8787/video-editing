"""원화 시트 그리기: art_sheets.json(common + 시트 + tail) → Codex 내장 imagegen (-m gpt-6-sol, 참조 = channel.yaml character.refs 두 장만).
그림은 ~/.codex/generated_images/<세션id>/ 에 생김 → 실행 출력의 세션 id 로 자기 폴더만 찾아 Drive 영상/<편>/art/<시트><접미>.png 로 옮김
(다른 작업자도 동시에 그리므로 '가장 최근 폴더'를 짐작으로 집지 않음).
python art_gen.py <시트> [접미(예: _r2)] [추가 문장]"""
import json, os, re, shutil, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent.name
DRIVE = Path(os.environ["YTFLOW_DRIVE"])
ART = DRIVE / "영상" / PROJ / "art"; ART.mkdir(parents=True, exist_ok=True)
REFS = [DRIVE / "refs/ch-knowledge/jiwoo_board.png", DRIVE / "영상/20261119-curiosity-choice-blindness/art/tasting.png"]

sheet = sys.argv[1]; suf = sys.argv[2] if len(sys.argv) > 2 else ""; extra = sys.argv[3] if len(sys.argv) > 3 else ""
d = json.loads((HERE / "art_sheets.json").read_text(encoding="utf-8"))
prompt = d["common"] + "\n\nTHE FOUR FRAMES: " + d["sheets"][sheet] + ("\n\n" + extra if extra else "") + "\n\n" + d["tail"] + \
    "\n\nGenerate the image with your built-in image generation tool. Do not write any code or files yourself; just generate the one image."
(ART / f"{sheet}{suf}.txt").write_text(prompt, encoding="utf-8")
cmd = ["codex", "exec", "-m", "gpt-6-sol", "--skip-git-repo-check"]
for r in REFS:
    cmd += ["-i", str(r)]
p = subprocess.run(" ".join(f'"{c}"' for c in cmd), input=prompt, capture_output=True, text=True, encoding="utf-8", errors="replace", shell=True)
out = (p.stdout or "") + "\n" + (p.stderr or "")
m = re.search(r"session id:\s*([0-9a-f-]{36})", out)
if not m:
    print(out[-3000:]); sys.exit(f"세션 id 를 못 찾음 ({sheet})")
sid = m.group(1)
g = Path.home() / ".codex" / "generated_images" / sid
pngs = sorted(g.glob("*.png"), key=lambda q: q.stat().st_mtime) if g.exists() else []
if not pngs:
    print(out[-3000:]); sys.exit(f"그림 없음: {g}")
dst = ART / f"{sheet}{suf}.png"
shutil.copy2(pngs[-1], dst)
from PIL import Image
print("ok", sheet, sid, dst, Image.open(dst).size, f"({len(pngs)}장)")
