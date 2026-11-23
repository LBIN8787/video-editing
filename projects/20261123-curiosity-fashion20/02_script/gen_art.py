"""원화 시트 그리기: art_sheets.json → Codex $imagegen (-m gpt-6-sol) → Drive 영상/<편>/art/<이름>.png + <이름>.txt
python gen_art.py <시트>[:<저장이름>] ... [--par 3] [--extra "더할 문장"]
다른 작업자도 동시에 그리므로 실행 출력의 session id 로 ~/.codex/generated_images/<id>/ 를 정확히 찾음(최근 폴더를 짐작하지 않음)."""
import json, os, re, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent.name
DRIVE = Path(os.environ.get("YTFLOW_DRIVE", r"G:\내 드라이브\ytflow"))
ART = DRIVE / "영상" / PROJ / "art"; ART.mkdir(parents=True, exist_ok=True)
LOG = Path(os.environ.get("TEMP", ".")) / PROJ / "codex"; LOG.mkdir(parents=True, exist_ok=True)
J = json.loads((HERE / "art_sheets.json").read_text(encoding="utf-8"))
REFS = [DRIVE / r for r in J["refs"]]
GEN = Path.home() / ".codex" / "generated_images"

args = sys.argv[1:]
par = 3; extra = ""
if "--par" in args: i = args.index("--par"); par = int(args[i + 1]); del args[i:i + 2]
if "--extra" in args: i = args.index("--extra"); extra = args[i + 1]; del args[i:i + 2]


def prompt(sheet):
    body = J["sheets"][sheet]
    return ("Use $imagegen to create exactly one image as described below. The attached images, in order, are: jiwoo_board.png, tasting.png. "
            "Do not write any code and do not edit any file; just generate the image.\n\n" + J["common"] + "\n\n" + body
            + ("\n\n" + extra if extra else "") + "\n\n" + J["tail"])


def one(spec):
    sheet, name = (spec.split(":") + [None])[:2]; name = name or sheet
    p = prompt(sheet); (ART / f"{name}.txt").write_text(p, encoding="utf-8")
    cmd = ["codex", "exec", "--skip-git-repo-check", "-m", "gpt-6-sol"]
    for r in REFS: cmd += ["-i", str(r)]
    t0 = time.time()
    r = subprocess.run(" ".join(f'"{c}"' for c in cmd), input=p, capture_output=True, text=True, encoding="utf-8", errors="replace", shell=True,
                       cwd=str(LOG))
    log = (r.stdout or "") + "\n" + (r.stderr or ""); (LOG / f"{name}.log").write_text(log, encoding="utf-8")
    m = re.search(r"session id:\s*([0-9a-f-]{36})", log)
    if not m:
        return f"{name}: session id 없음 (rc={r.returncode}) — {LOG / (name + '.log')}"
    d = GEN / m.group(1)
    pngs = sorted(d.glob("*.png"), key=lambda q: q.stat().st_mtime) if d.exists() else []
    if not pngs:
        return f"{name}: 그림 없음 (session {m.group(1)})"
    shutil.copy2(pngs[-1], ART / f"{name}.png")
    return f"{name}: ok {len(pngs)}장 중 마지막, {time.time() - t0:.0f}s, session {m.group(1)}"


with ThreadPoolExecutor(par) as ex:
    for res in ex.map(one, args):
        print(res, flush=True)
