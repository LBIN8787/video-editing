"""PC 자동 일꾼 — inbox/pc-tasks 의 pending 할 일을 사람이 명령하지 않아도 처리한다 (2026-11-20 사용자:
"나 앞으로 매번 내가 손수 명령하기 싫어 내가 손수 명령 안해도 되도록 자동화 세팅 설정해놔").

Windows 작업 스케줄러가 10분마다 실행한다 (설치: scripts/install_pc_worker.ps1, 한 번만).
    python scripts/pc_worker.py [--once] [--dry-run]

하는 일:
 1. 저장소 옆의 전용 작업 폴더(<저장소>-worker, git worktree, main 추적)를 최신 main 으로 맞춘다
    — 사용자가 쓰는 원래 폴더의 브랜치·변경은 건드리지 않음.
 2. inbox/pc-tasks/*.md 중 status: pending 을 하나씩 집어 status: in_progress 로 바꿔 main 에 푸시(중복 처리 방지).
 3. 할 일이 정한 브랜치(`branch:`, 없으면 main)를 두 번째 작업 폴더(<저장소>-worker-task)에 받아,
    - type: curiosity-build → scripts/curiosity_build.py (원화 → 자료 → 목소리 → 장면 → 렌더 → Drive)
    - 그 밖(art-draw 등) → Codex(ChatGPT 구독, GPT 이미지) 에 지시를 그대로 맡김. Codex 가 없으면 Claude Code(`claude -p`).
    `after: <다른 할 일 파일>` 이 있으면 그 할 일이 done 이 된 뒤에 시작한다 (원화 → 빌드 순서).
    결과는 일꾼이 할 일 파일에 '## 결과' + status: done|failed 로 적어 main 에 푸시.
 4. 실패하면 status: pending 으로 되돌리고 시도 횟수를 남긴다. 2번 실패하면 status: failed 로 두고 멈춘다(무한 반복 방지).
로그: %YTFLOW_DRIVE%/_local/pc-worker/pc_worker.log · 잠금: 같은 폴더 pc_worker.lock (YTFLOW_DRIVE 없으면 %LOCALAPPDATA%/ytflow) (겹쳐 돌지 않게)

클라우드 세션은 이 파일을 실행하지 않는다(CLAUDE_CODE_REMOTE=true 면 바로 끝남).
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# 로그·잠금은 Google Drive(_local) — 2026-11-21 사용자: "작업파일은 c드라이브에 두지 말고 구글드라이브에 보관해줘"
HOME = (Path(os.environ["YTFLOW_DRIVE"]) / "_local" / "pc-worker") if os.environ.get("YTFLOW_DRIVE") else \
    Path(os.environ.get("LOCALAPPDATA") or Path.home() / ".local" / "share") / "ytflow"
LOG = HOME / "pc_worker.log"
LOCK = HOME / "pc_worker.lock"
MAX_TRY = 2
TASK_TIMEOUT = 2 * 60 * 60   # 한 할 일에 최대 2시간 (원화 9장 정도)


def log(msg: str) -> None:
    HOME.mkdir(parents=True, exist_ok=True)
    line = f"{dt.datetime.now():%Y-%m-%d %H:%M:%S} {msg}"
    print(line, flush=True)
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def git(wt: Path, *args: str, check: bool = True) -> str:
    r = subprocess.run(["git", "-C", str(wt), *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if check and r.returncode:
        raise RuntimeError(f"git {' '.join(args)}: {r.stderr.strip()[-400:]}")
    return r.stdout


def worktree() -> Path:
    """사용자 폴더와 분리된 main 전용 작업 폴더."""
    wt = ROOT.parent / (ROOT.name + "-worker")
    if not (wt / ".git").exists():
        git(ROOT, "fetch", "origin", "main")
        git(ROOT, "worktree", "add", "-f", str(wt), "origin/main")
        log(f"작업 폴더 만듦: {wt}")
    git(wt, "fetch", "origin", "main")
    git(wt, "checkout", "-B", "pc-worker", "origin/main")   # 늘 원격 main 그대로에서 시작
    return wt


def set_status(wt: Path, f: Path, status: str, note: str = "") -> None:
    t = f.read_text(encoding="utf-8")
    t = re.sub(r"^status:\s*\S+", f"status: {status}", t, count=1, flags=re.M)
    if note:
        t = t.rstrip() + f"\n\n> pc-worker {dt.datetime.now():%Y-%m-%d %H:%M}: {note}\n"
    f.write_text(t, encoding="utf-8")
    git(wt, "add", str(f))
    git(wt, "commit", "-m", f"pc-worker: {f.name} → {status}", check=False)
    for _ in range(3):   # 다른 세션이 먼저 올렸으면 받아서 다시
        if subprocess.run(["git", "-C", str(wt), "push", "origin", "HEAD:main"], capture_output=True).returncode == 0:
            return
        git(wt, "pull", "--rebase", "origin", "main", check=False)
    raise RuntimeError("main 에 푸시하지 못함")


def tries(t: str) -> int:
    return len(re.findall(r"^> pc-worker .*시도", t, re.M))


PROMPT = """너는 이 PC 의 자동 일꾼이다. 사람에게 묻지 말고 끝까지 처리한다.
지금 폴더는 브랜치 {branch} 의 작업 폴더다. 할 일 파일(읽기용 사본): {task}
1) 저장소 규칙 AGENTS.md 와 inbox/pc-tasks/README.md 를 읽는다.
2) 할 일 파일의 지시를 그대로 수행한다. 그림 생성은 Codex 내장 imagegen(GPT 이미지, ChatGPT 구독)으로 한다. ElevenLabs 로는 그리지 않는다.
   큰 파일(그림·영상)은 환경변수 YTFLOW_DRIVE 아래 지시된 경로에 저장하고 git 에 넣지 않는다.
   코드·문서를 고쳤다면 이 브랜치({branch})에 커밋해 푸시한다 (git push origin HEAD:{branch}).
3) 끝나면 이 폴더 맨 위에 PC_RESULT.md 를 만든다. 첫 줄은 'status: done' 또는 'status: failed',
   그 아래에 확인 시각 · 만든 파일과 경로 · 실패한 것과 이유. (할 일 파일의 상태는 일꾼이 main 에 적는다 — 직접 고치지 않는다.)
"""


def front(t: str, key: str) -> str:
    m = re.search(rf"^{key}:\s*(.+)$", t, re.M)
    return m.group(1).strip() if m else ""


def task_tree(branch: str) -> Path:
    """할 일을 실제로 하는 폴더 (할 일이 정한 브랜치, 없으면 main)."""
    wt = ROOT.parent / (ROOT.name + "-worker-task")
    if not (wt / ".git").exists():
        git(ROOT, "worktree", "add", "-f", "--detach", str(wt))
    git(wt, "fetch", "origin", branch)
    git(wt, "checkout", "-B", f"pcw-{branch}"[:60], f"origin/{branch}")
    git(wt, "branch", f"--set-upstream-to=origin/{branch}", check=False)
    git(wt, "clean", "-fd", "-e", "projects/*/04_assets", "-e", "projects/*/03_voice", check=False)
    return wt


def run_agent(wt: Path, task_text: str, branch: str) -> tuple[int, str]:
    (wt / "PC_TASK.md").write_text(task_text, encoding="utf-8")
    (wt / "PC_RESULT.md").unlink(missing_ok=True)
    prompt = PROMPT.format(task="PC_TASK.md", branch=branch)
    codex, claude = shutil.which("codex"), shutil.which("claude")
    if codex:
        cmd, stdin = [codex, "exec", "--skip-git-repo-check", "--dangerously-bypass-approvals-and-sandbox", "-C", str(wt), "-"], prompt
    elif claude:
        cmd, stdin = [claude, "-p", prompt, "--permission-mode", "bypassPermissions"], None
    else:
        return 127, "status: failed\ncodex·claude 둘 다 없음 — 설치 필요"
    log(f"에이전트 시작: {Path(cmd[0]).name}")
    try:
        r = subprocess.run(cmd, cwd=wt, input=stdin, text=True, encoding="utf-8", errors="replace",
                           capture_output=True, timeout=TASK_TIMEOUT)
        rc = r.returncode
        (HOME / "last_agent.out.txt").write_text((r.stdout or "") + "\n--- stderr ---\n" + (r.stderr or ""), encoding="utf-8")
    except subprocess.TimeoutExpired:
        rc = 124
    res = (wt / "PC_RESULT.md").read_text(encoding="utf-8") if (wt / "PC_RESULT.md").exists() else ""
    return rc, res


def run_build(wt: Path, task_text: str, branch: str) -> tuple[int, str]:
    """type: curiosity-build — 정해진 순서라 에이전트 없이 스크립트로."""
    proj = front(task_text, "project")
    r = subprocess.run([sys.executable, "scripts/curiosity_build.py", f"projects/{proj}"], cwd=wt, capture_output=True,
                       text=True, encoding="utf-8", errors="replace", timeout=TASK_TIMEOUT)
    (HOME / f"build_{proj}.log").write_text((r.stdout or "") + "\n--- stderr ---\n" + (r.stderr or ""), encoding="utf-8")
    if r.returncode:
        return r.returncode, "status: failed\n" + ((r.stdout or "") + (r.stderr or ""))[-1500:]
    git(wt, "add", f"projects/{proj}/REPORT.md")
    git(wt, "commit", "-m", f"pc-worker: {proj} 자동 빌드 완료", check=False)
    subprocess.run(["git", "-C", str(wt), "push", "origin", f"HEAD:{branch}"], capture_output=True)
    last = [l for l in (r.stdout or "").splitlines() if l.startswith("- PC 자동 빌드 완료")]
    return 0, "status: done\n" + (last[-1] if last else "빌드 완료")


def is_ready(wt: Path, t: str) -> bool:
    after = front(t, "after")
    if not after:
        return True
    f = wt / "inbox" / "pc-tasks" / after
    return f.exists() and front(f.read_text(encoding="utf-8"), "status") == "done"


def one_pass(dry: bool) -> int:
    wt = worktree()
    todo = []
    for f in sorted((wt / "inbox" / "pc-tasks").glob("*.md")):
        t = f.read_text(encoding="utf-8")
        if f.name != "README.md" and front(t, "status") == "pending" and is_ready(wt, t):
            todo.append(f)
    if not todo:
        log("할 일 없음")
        return 0
    log(f"할 일 {len(todo)}건: " + ", ".join(f.name for f in todo))
    if dry:
        return len(todo)
    for f in todo:
        t = f.read_text(encoding="utf-8")
        n = tries(t) + 1
        branch = front(t, "branch") or "main"
        set_status(wt, f, "in_progress", f"{n}번째 시도 시작 (브랜치 {branch})")
        tw = task_tree(branch)
        rc, res = (run_build if front(t, "type") == "curiosity-build" else run_agent)(tw, t, branch)
        git(wt, "fetch", "origin", "main")
        git(wt, "checkout", "-B", "pc-worker", "origin/main")
        st = front(res, "status")
        if st in ("done", "failed"):
            body = re.sub(r"^status:.*\n?", "", res, count=1).strip()
            f.write_text(f.read_text(encoding="utf-8").rstrip() + "\n\n## 결과 (pc-worker)\n\n" + body + "\n", encoding="utf-8")
            set_status(wt, f, st, f"끝 (종료 코드 {rc})")
            log(f"끝: {f.name} → {st}")
        elif n >= MAX_TRY:
            set_status(wt, f, "failed", f"{n}번 시도했지만 끝나지 않음 (종료 코드 {rc}) — 로그: {LOG}")
            log(f"실패로 멈춤: {f.name}")
        else:
            set_status(wt, f, "pending", f"{n}번째 시도가 끝나지 않음 (종료 코드 {rc}) — 다음 차례에 다시")
            log(f"다시 대기: {f.name}")
    return len(todo)


def main() -> None:
    if os.environ.get("CLAUDE_CODE_REMOTE") == "true":
        sys.exit(0)
    ap = argparse.ArgumentParser()
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    HOME.mkdir(parents=True, exist_ok=True)
    if LOCK.exists() and time.time() - LOCK.stat().st_mtime < TASK_TIMEOUT + 600:
        log("이미 다른 일꾼이 도는 중 — 이번 차례는 건너뜀")
        return
    LOCK.write_text(str(os.getpid()), encoding="utf-8")
    try:
        one_pass(a.dry_run)
    except Exception as e:  # noqa: BLE001
        log(f"오류: {e}")
    finally:
        LOCK.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
