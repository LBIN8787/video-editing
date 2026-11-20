"""로컬 정기 작업 실행기 — 클라우드 루틴 대신 이 PC 에서 시장·호기심 작업을 돌린다 (docs/56-local-routines.md).

2026-11-21 사용자: "시장 자동화도 로컬에서 돌 수 있도록 세팅해주고 매번 클라우드라서 막혔니 뭐니 말이 너무 많아서"
                  "작업파일은 c드라이브에 두지 말고 구글드라이브에 보관해줘"

Windows 작업 스케줄러가 config/local_routines.yaml 의 시각마다 실행한다 (설치: scripts/install_local_routines.ps1).
    python scripts/local_routine.py <작업>            # market-daily | curiosity
    python scripts/local_routine.py <작업> --dry-run  # 준비·에이전트 확인만, 실행 안 함
    python scripts/local_routine.py --list            # 작업|시각 (설치 스크립트가 읽음)

하는 일:
 1. 전용 작업 폴더(E:\ytflow-local\routine-<작업>, git worktree)를 최신 origin/main 으로 맞춘다 — 사용자 폴더는 건드리지 않음.
 2. 그 폴더에서 Claude Code(`claude -p`, Claude 구독)에 config/local_routines/<작업>.md 지시를 맡긴다.
    Claude 가 로그인돼 있지 않으면 Codex(ChatGPT 구독)로 대신 돌리고 보고에 적는다.
 3. 끝나면 만든 큰 파일(영상·음성·그림)을 Google Drive `영상/<프로젝트>/` 로 복사·크기 확인하고,
    보고(LOCAL_RESULT.md)·로그를 Drive `_local/` 에 남기고, Windows 알림을 띄운다.
작업 파일 위치: 로그·보고·잠금 = %YTFLOW_DRIVE%\\_local, 임시 파일 = 저장소 옆 작업 폴더(D:) — C 드라이브는 쓰지 않는다.
"""
from __future__ import annotations

import argparse
import datetime as dt
import glob
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# 작업 폴더·임시 파일: C 드라이브 X, D 드라이브에 새 파일 X (AGENTS.md 저장 위치) → E: (Codex 작업 폴더와 같은 드라이브)
WORK = Path(os.environ.get("YTFLOW_WORK") or ("E:/ytflow-local" if Path("E:/").exists() else ROOT.parent / "ytflow-local"))
MEDIA_EXT = {".mp4", ".mov", ".webm", ".mkv", ".mp3", ".wav", ".m4a", ".png", ".jpg", ".jpeg", ".webp", ".gif"}
PRUNE_DAYS = 7          # Drive 로 복사·확인된 지 이만큼 지난 편의 큰 파일은 작업 폴더에서 지움 (Drive 사본만 남김)

COMMON = """너는 이 PC 의 정기 작업 '{title}' 이다. 사람에게 묻지 말고 끝까지 처리한다. 답과 보고는 한국어.
- 지금 폴더: {wt} (이 작업 전용 git worktree, 브랜치 {branch} = 최신 origin/main). 사용자 폴더 {root} 는 건드리지 않는다.
- 여기는 사용자 PC 다. 클라우드 제약(저장소 붙이기·푸시 권한 확인·유튜브 봇 확인)에 대한 설명은 쓰지 않는다. 안 되는 것이 있으면 보고에 한 줄로만.
- 큰 파일(영상·음성·그림)은 git 에 넣지 않는다. 환경변수 YTFLOW_DRIVE({drive}) 가 Google Drive 의 ytflow 폴더다. 임시 파일은 TEMP 를 쓴다.
- 커밋 끝줄: Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
- 끝나면 이 폴더 맨 위에 LOCAL_RESULT.md 를 쓴다 (git 에 넣지 않음). 형식은 지시문의 '보고' 절.

오늘(한국 시간): {today}

--- 지시문 ({prompt}) ---
"""


def drive_dir() -> Path:
    d = os.environ.get("YTFLOW_DRIVE")
    if not d and os.name == "nt":   # 작업 스케줄러가 예전 환경을 넘겨줄 때 대비: 사용자 환경변수에서 직접
        import winreg
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
                d = winreg.QueryValueEx(k, "YTFLOW_DRIVE")[0]
        except OSError:
            d = None
    if not d:
        sys.exit("YTFLOW_DRIVE 가 없습니다 — setx YTFLOW_DRIVE \"G:\\내 드라이브\\ytflow\" (docs/09-storage.md §0)")
    os.environ["YTFLOW_DRIVE"] = d
    return Path(d)


class Run:
    def __init__(self, job: str):
        self.job = job
        self.drive = drive_dir()
        self.home = self.drive / "_local"
        self.logf = self.home / "logs" / f"{job}.log"
        self.logf.parent.mkdir(parents=True, exist_ok=True)

    def log(self, msg: str) -> None:
        line = f"{dt.datetime.now():%Y-%m-%d %H:%M:%S} {msg}"
        print(line, flush=True)
        with self.logf.open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")


def git(wt: Path, *args: str, check: bool = True) -> str:
    r = subprocess.run(["git", "-C", str(wt), *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if check and r.returncode:
        raise RuntimeError(f"git {' '.join(args)}: {r.stderr.strip()[-400:]}")
    return r.stdout


def load_jobs(base: Path) -> dict:
    import yaml
    return (yaml.safe_load((base / "config" / "local_routines.yaml").read_text(encoding="utf-8")) or {}).get("jobs", {})


def worktree(job: str) -> tuple[Path, str]:
    wt = WORK / f"routine-{job}"
    branch = f"local/{job}"
    if not (wt / ".git").exists():
        git(ROOT, "fetch", "origin", "main")
        wt.parent.mkdir(parents=True, exist_ok=True)
        git(ROOT, "worktree", "add", "-f", "--detach", str(wt), "origin/main")
    git(wt, "fetch", "origin", "main")
    git(wt, "checkout", "-f", "-B", branch, "origin/main")   # 늘 원격 main 그대로에서 시작 (지난 실행의 미푸시 커밋은 버림)
    git(wt, "clean", "-fd", "-e", "projects/*/0[0-9]_*", check=False)   # 추적 안 되는 기획 찌꺼기만, 미디어(무시 파일)는 남김
    (wt / "LOCAL_RESULT.md").unlink(missing_ok=True)
    return wt, branch


def find_claude() -> str | None:
    p = shutil.which("claude")
    if p:
        return p
    base = os.environ.get("LOCALAPPDATA", "")
    cands = glob.glob(os.path.join(base, "Claude-Data", "*", "claude-code", "*", "*", "claude.exe")) + \
        glob.glob(os.path.join(base, "AnthropicClaude", "**", "claude.exe"), recursive=True)
    cands.sort(key=os.path.getmtime, reverse=True)
    return cands[0] if cands else None


def claude_ready(exe: str, env: dict) -> bool:
    try:
        r = subprocess.run([exe, "-p", "ok 라고만 답해", "--max-turns", "1"], capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=120, env=env)
    except Exception:  # noqa: BLE001
        return False
    return r.returncode == 0 and "Not logged in" not in (r.stdout + r.stderr)


def agent_cmd(wt: Path, env: dict, run: Run) -> tuple[list[str], str]:
    exe = find_claude()
    if exe and claude_ready(exe, env):
        return [exe, "-p", "--permission-mode", "bypassPermissions"], "claude"
    if exe:
        run.log(f"Claude Code 로그인 안 됨 ({exe}) — Codex 로 대신 (docs/56 §1 한 번 로그인)")
    codex = shutil.which("codex")
    if codex:
        return [codex, "exec", "--skip-git-repo-check", "--dangerously-bypass-approvals-and-sandbox", "-C", str(wt), "-"], "codex"
    return [], ""


def mirror_media(wt: Path, run: Run) -> list[str]:
    """작업 폴더의 큰 파일(git 무시 파일) → Drive 영상/<프로젝트>/ (없거나 크기가 다르면 복사, 복사 뒤 크기 확인)."""
    out, cut = [], time.time() - 2 * 86400
    for proj in sorted((wt / "projects").glob("*")):
        if not proj.is_dir():
            continue
        files = [f for f in proj.rglob("*") if f.is_file() and f.suffix.lower() in MEDIA_EXT]
        recent = [f for f in files if f.stat().st_mtime >= cut]
        if not recent:
            continue
        n = 0
        for f in recent:
            if git(wt, "ls-files", "--error-unmatch", str(f.relative_to(wt)), check=False):
                continue   # git 에 있는 작은 그림은 그대로
            dst = run.drive / "영상" / proj.name / f.relative_to(proj)
            if dst.exists() and dst.stat().st_size == f.stat().st_size:
                continue
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, dst)
            if dst.stat().st_size != f.stat().st_size:
                run.log(f"Drive 복사 크기 다름: {dst}")
                continue
            n += 1
        if n:
            out.append(f"{proj.name}: {n}개 → Drive 영상/{proj.name}/")
    return out


def prune_media(wt: Path, run: Run) -> None:
    """Drive 에 같은 크기 사본이 있고 PRUNE_DAYS 넘게 손대지 않은 큰 파일만 작업 폴더에서 지운다 (PC 용량 줄이기)."""
    cut, gone = time.time() - PRUNE_DAYS * 86400, 0
    for f in (wt / "projects").rglob("*"):
        if f.is_file() and f.suffix.lower() in MEDIA_EXT and f.stat().st_mtime < cut:
            proj = f.relative_to(wt / "projects").parts[0]
            dst = run.drive / "영상" / proj / f.relative_to(wt / "projects" / proj)
            if dst.exists() and dst.stat().st_size == f.stat().st_size and \
                    not git(wt, "ls-files", "--error-unmatch", str(f.relative_to(wt)), check=False):
                f.unlink()
                gone += 1
    if gone:
        run.log(f"Drive 사본이 있는 오래된 큰 파일 {gone}개를 작업 폴더에서 지움")


def notify(title: str, text: str) -> None:
    if os.name != "nt":
        return
    q = lambda s: s.replace("'", "''")[:240]   # noqa: E731
    ps = ("Add-Type -AssemblyName System.Windows.Forms; $n=New-Object System.Windows.Forms.NotifyIcon; "
          "$n.Icon=[System.Drawing.SystemIcons]::Information; $n.Visible=$true; "
          f"$n.ShowBalloonTip(15000,'{q(title)}','{q(text)}',[System.Windows.Forms.ToolTipIcon]::Info); Start-Sleep 16; $n.Dispose()")
    subprocess.Popen(["powershell", "-NoProfile", "-WindowStyle", "Hidden", "-Command", ps],
                     creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))


def main() -> None:
    if os.environ.get("CLAUDE_CODE_REMOTE") == "true":
        sys.exit(0)   # 클라우드 세션은 실행하지 않음
    ap = argparse.ArgumentParser()
    ap.add_argument("job", nargs="?")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    if a.list:   # 설치 스크립트가 읽음 — 영문만 (콘솔 인코딩과 무관하게)
        for k, v in load_jobs(ROOT).items():
            print(f"{k}|{v['time']}")
        return
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if not a.job:
        ap.error("작업 이름이 필요합니다 (--list 로 목록)")

    run = Run(a.job)
    lock = run.home / "locks" / f"{a.job}.lock"
    lock.parent.mkdir(parents=True, exist_ok=True)
    if lock.exists() and time.time() - lock.stat().st_mtime < 6 * 3600:
        run.log("이미 도는 중 — 이번 차례는 건너뜀")
        return
    lock.write_text(f"{os.getpid()} {dt.datetime.now():%Y-%m-%d %H:%M}", encoding="utf-8")
    stamp = f"{dt.datetime.now():%Y%m%d-%H%M}"
    try:
        wt, branch = worktree(a.job)
        jobs = load_jobs(wt)
        if a.job not in jobs:
            raise SystemExit(f"config/local_routines.yaml 에 '{a.job}' 작업이 없습니다")
        job = jobs[a.job]
        tmp = WORK / "tmp" / a.job   # 임시 파일: C 드라이브(기본 TEMP) 대신 E:
        shutil.rmtree(tmp, ignore_errors=True)
        tmp.mkdir(parents=True, exist_ok=True)
        env = dict(os.environ, TEMP=str(tmp), TMP=str(tmp), PYTHONUTF8="1", PYTHONIOENCODING="utf-8",
                   YTFLOW_LOCAL_ROUTINE=a.job)
        prompt = COMMON.format(title=job.get("title", a.job), wt=wt, branch=branch, root=ROOT, drive=run.drive,
                               today=f"{dt.date.today():%Y-%m-%d (%a)}", prompt=job["prompt"]) + \
            (wt / job["prompt"]).read_text(encoding="utf-8")
        cmd, who = agent_cmd(wt, env, run)
        if not cmd:
            raise SystemExit("claude·codex 둘 다 실행할 수 없음 — docs/56 §1")
        run.log(f"시작: {a.job} ({who}) · 작업 폴더 {wt}")
        if a.dry_run:
            run.log("dry-run: 여기까지 (에이전트 실행 안 함)")
            return
        t0 = time.time()
        try:
            r = subprocess.run(cmd, cwd=wt, input=prompt, text=True, encoding="utf-8", errors="replace",
                               capture_output=True, timeout=int(job.get("timeout_min", 180)) * 60, env=env)
            rc, out = r.returncode, (r.stdout or "") + "\n--- stderr ---\n" + (r.stderr or "")
        except subprocess.TimeoutExpired as e:
            rc, out = 124, f"시간 초과 ({job.get('timeout_min')}분)\n{e.stdout or ''}"
        mins = (time.time() - t0) / 60
        res_f = wt / "LOCAL_RESULT.md"
        res = res_f.read_text(encoding="utf-8") if res_f.exists() else f"{a.job}: 보고 없음 (종료 코드 {rc}) — 로그 확인"
        moved = mirror_media(wt, run)
        prune_media(wt, run)
        rep = run.home / "reports" / f"{stamp}-{a.job}.md"
        rep.parent.mkdir(parents=True, exist_ok=True)
        rep.write_text(res.rstrip() + f"\n\n---\n에이전트 {who} · 종료 코드 {rc} · {mins:.0f}분\n"
                       + ("\n".join(f"- {m}" for m in moved) or "- Drive 로 옮길 새 큰 파일 없음") + "\n", encoding="utf-8")
        (run.home / "logs" / f"{stamp}-{a.job}.agent.txt").write_text(out, encoding="utf-8")
        first = res.strip().splitlines()[0] if res.strip() else a.job
        run.log(f"끝: {first} (종료 코드 {rc}, {mins:.0f}분) · 보고 {rep}")
        notify(job.get("title", a.job), first)
    except Exception as e:  # noqa: BLE001
        run.log(f"오류: {e}")
        notify(f"ytflow {a.job} 실패", str(e))
        raise
    finally:
        lock.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
