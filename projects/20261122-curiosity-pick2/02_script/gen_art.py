"""커닝 편 원화 생성: art_sheets.json(make_art_sheets.py) → Codex $imagegen(-m gpt-6-sol, 참조 = channel.yaml character.refs 두 장) → Drive art/<이름>.png + <이름>.txt
python gen_art.py <시트,시트|all> [--suffix _r2] [--workers 3] [--extra "더할 지시"]
그림은 ~/.codex/generated_images/<세션 id>/ 에 생김 → 이 실행 출력의 세션 id 로 정확히 찾음(다른 작업자도 동시에 그리므로 '가장 최근 폴더'를 집지 않음)."""
import argparse, json, os, re, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import make_art_sheets as M  # noqa: E402

DRIVE = Path(os.environ["YTFLOW_DRIVE"])
ART = DRIVE / "영상/20261122-curiosity-pick2/art"
REFS = [DRIVE / "refs/ch-knowledge/jiwoo_board.png", DRIVE / "영상/20261119-curiosity-choice-blindness/art/tasting.png"]
GEN = Path.home() / ".codex/generated_images"
WORK = Path(os.environ.get("TEMP", "/tmp")) / "20261122-curiosity-pick2" / "codex"
HEAD = ("Use $imagegen to create exactly one image as described below. The attached images, in order, are: jiwoo_board.png, tasting.png. "
        "Do not write any code and do not edit any file; just generate the image.\n\n")


def one(name, suffix, extra):
    out = ART / f"{name}{suffix}.png"
    if out.exists():
        return f"skip {out.name}"
    body = M.prompt(name)
    if extra:
        body = body.replace("\n\nKeep the main subject", "\n\n" + extra + "\n\nKeep the main subject")
    text = HEAD + body
    (ART / f"{name}{suffix}.txt").write_text(text, encoding="utf-8")
    WORK.mkdir(parents=True, exist_ok=True)
    cmd = [shutil.which("codex") or "codex", "exec", "-m", "gpt-6-sol", "--skip-git-repo-check", "-C", str(WORK)]
    for r in REFS:
        cmd += ["-i", str(r)]
    cmd += ["-"]
    for attempt in range(2):
        r = subprocess.run(cmd, input=text, text=True, encoding="utf-8", errors="replace", capture_output=True, timeout=1500)
        log = (r.stdout or "") + "\n" + (r.stderr or "")
        (WORK / f"{name}{suffix}.log").write_text(log, encoding="utf-8")
        sid = re.findall(r"session id:\s*([0-9a-fA-F-]{20,})", log)
        cands = []
        if sid:
            d = GEN / sid[0]
            if d.exists():
                cands = sorted(d.glob("*.png"), key=lambda p: p.stat().st_mtime)
        if not cands:   # 출력에 적힌 경로(세션 id 가 들어 있는 것만)
            cands = [Path(h) for h in re.findall(r"[A-Za-z]:[^\s()\[\]`'\"]*generated_images[^\s()\[\]`'\"]*?\.png", log)
                     if Path(h).exists() and (not sid or sid[0] in h)]
        if cands:
            shutil.copy2(cands[-1], out)
            return f"ok {out.name} ← {cands[-1]}"
    return f"FAIL {name}{suffix} (rc={r.returncode}, sid={sid}) — log {WORK / (name + suffix + '.log')}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("names")
    ap.add_argument("--suffix", default="")
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--extra", default="")
    a = ap.parse_args()
    ART.mkdir(parents=True, exist_ok=True)
    names = list(M.SHEETS) if a.names == "all" else a.names.split(",")
    with ThreadPoolExecutor(a.workers) as ex:
        for res in ex.map(lambda n: one(n, a.suffix, a.extra), names):
            print(res, flush=True)


if __name__ == "__main__":
    main()
