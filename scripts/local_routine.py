"""로컬 정기 작업 실행기 — 클라우드 루틴 대신 이 PC 에서 시장·호기심 작업을 돌린다 (docs/56-local-routines.md).

2026-11-21 사용자: "시장 자동화도 로컬에서 돌 수 있도록 세팅해주고 매번 클라우드라서 막혔니 뭐니 말이 너무 많아서"
                  "작업파일은 c드라이브에 두지 말고 구글드라이브에 보관해줘"

Windows 작업 스케줄러가 config/local_routines.yaml 의 시각마다 실행한다 (설치: scripts/install_local_routines.ps1).
    python scripts/local_routine.py <작업>            # market-daily | curiosity
    python scripts/local_routine.py <작업> --dry-run  # 준비·에이전트 확인만, 실행 안 함
    python scripts/local_routine.py --list            # 작업|시각 (설치 스크립트가 읽음)

하는 일:
 1. 전용 작업 폴더(E:/ytflow-local/routine-<작업>, git worktree)를 최신 origin/main 으로 맞춘다 — 사용자 폴더는 건드리지 않음.
 2. 그 폴더에서 Claude Code(`claude -p`, Claude 구독)에 config/local_routines/<작업>.md 지시를 맡긴다.
    Claude 가 로그인돼 있지 않으면 Codex(ChatGPT 구독)로 대신 돌리고 보고에 적는다.
 3. 끝나면 만든 큰 파일(영상·음성·그림)을 Google Drive `영상/<프로젝트>/` 로 복사·크기 확인하고,
    보고(LOCAL_RESULT.md)·로그를 Drive `_local/` 에 남기고, Windows 알림을 띄운다.
작업 파일 위치: 로그·보고·잠금 = %YTFLOW_DRIVE%/_local, 작업 폴더·임시 파일 = E:/ytflow-local (YTFLOW_WORK) — C 드라이브는 쓰지 않는다.
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
        # Google Drive 가 잠깐 안 붙어 있어도(G: 없음) 작업은 돈다 — 로그·잠금·보고는 E: 에, 큰 파일은 작업 폴더에 남겨 다음 차례에 Drive 로 (2026-11-25)
        self.drive_ok = self.drive.exists()
        self.home = self.drive / "_local" if self.drive_ok else WORK / "_local"
        self.logf = self.home / "logs" / f"{job}.log"
        self.logf.parent.mkdir(parents=True, exist_ok=True)
        if not self.drive_ok:
            self.log(f"Google Drive 가 연결돼 있지 않음({self.drive}) — 로그·잠금은 {self.home}, 큰 파일은 작업 폴더에 둠")

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
    for f in ("ROUTINE_STOP", "DEEP_SCAN.md", "DEEP_WATCH.json"):   # 지난 차례의 단계 사이 쪽지
        (wt / f).unlink(missing_ok=True)
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


_READY: dict = {}


def claude_ready(exe: str, env: dict) -> bool:
    """로그인 확인. 종료 코드만 보면 안 됨 — 짧은 답도 'Reached max turns (1)' 로 1 을 돌려줄 때가 있어
    로그인돼 있는데도 Codex 로 넘어갔다(2026-11-25 호기심·심층 감시). 로그인·인증 오류 문구가 있을 때만 '안 됨'. 한 번 확인하면 이번 실행 동안 기억."""
    if exe in _READY:
        return _READY[exe]
    try:
        r = subprocess.run([exe, "-p", "ok 라고만 답해", "--max-turns", "2"], capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=180, env=env)
        out = (r.stdout + r.stderr).lower()
        ok = not any(k in out for k in ("not logged in", "please run /login", "invalid api key", "authentication_error",
                                         "oauth token has expired", "401"))
        ok = ok and (r.returncode == 0 or "max turns" in out)
    except Exception:  # noqa: BLE001
        ok = False
    _READY[exe] = ok
    return ok


def agent_cmd(wt: Path, env: dict, run: Run, model: str | None = None) -> tuple[list[str], str]:
    exe = find_claude()
    if exe and claude_ready(exe, env):
        # model: 단계마다 모델을 고름 (예: 심층 감시의 판단·검수 = claude-fable-5-2, 2026-11-24 사용자 "판단은 fable이 해주세요")
        return [exe, "-p", "--permission-mode", "bypassPermissions"] + (["--model", model] if model else []), \
            f"claude({model})" if model else "claude"
    if exe:
        run.log(f"Claude Code 로그인 안 됨 ({exe}) — Codex 로 대신 (docs/56 §1 한 번 로그인)")
    codex = shutil.which("codex")
    if codex:
        return [codex, "exec", "--skip-git-repo-check", "--dangerously-bypass-approvals-and-sandbox", "-C", str(wt), "-"], "codex"
    return [], ""


def mirror_media(wt: Path, run: Run) -> list[str]:
    """작업 폴더의 큰 파일(git 무시 파일) → Drive 영상/<프로젝트>/ (없거나 크기가 다르면 복사, 복사 뒤 크기 확인)."""
    out, cut = [], time.time() - 2 * 86400
    if not run.drive_ok:
        return ["Drive 연결 안 됨 — 큰 파일은 작업 폴더에 그대로 (다음 차례에 옮김)"]
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
    if not run.drive_ok:
        return
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
            print(f"{k}|{v['time']}|{v.get('repeat_hours', '')}")   # 반복 작업(심층 감시)은 시간 간격
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
    # wait_for: 이 작업들이 도는 중이면 이번 차례는 건너뜀 (예: 심층 감시는 아침 브리핑이 렌더하는 동안 PC·목소리 크레딧을 나눠 쓰지 않음)
    for other in (load_jobs(ROOT).get(a.job) or {}).get("wait_for") or []:
        ol = run.home / "locks" / f"{other}.lock"
        if ol.exists() and time.time() - ol.stat().st_mtime < 6 * 3600:
            run.log(f"{other} 가 도는 중 — 이번 차례는 건너뜀")
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
                   YTFLOW_LOCAL_ROUTINE=a.job,
                   # 하위 에이전트를 백그라운드로 돌려도 claude -p 가 10분 뒤 끊지 않게 (11-23 AI 커닝 편 조사 중단)
                   CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS="0")
        # 단계: steps 가 있으면 차례로 (단계마다 지시문·모델·시간), 없으면 prompt 하나.
        # 어느 단계든 작업 폴더에 ROUTINE_STOP 을 만들면 거기서 끝 (예: 판단 단계가 '안 만듦').
        steps = job.get("steps") or [{"name": a.job, "prompt": job["prompt"], "timeout_min": job.get("timeout_min", 180)}]
        stop_f = wt / "ROUTINE_STOP"
        stop_f.unlink(missing_ok=True)
        results, outs, who, rc, t0, stopped_at = [], [], "", 0, time.time(), None
        for i, st in enumerate(steps):
            prompt = COMMON.format(title=job.get("title", a.job), wt=wt, branch=branch, root=ROOT, drive=run.drive,
                                   today=f"{dt.datetime.now():%Y-%m-%d (%a) %H:%M}", prompt=st["prompt"]) + \
                (wt / st["prompt"]).read_text(encoding="utf-8")
            cmd, who = agent_cmd(wt, env, run, st.get("model") or job.get("model"))
            if not cmd:
                raise SystemExit("claude·codex 둘 다 실행할 수 없음 — docs/56 §1")
            run.log(f"시작: {a.job}/{st.get('name', i)} ({who}) · 작업 폴더 {wt}")
            if a.dry_run:
                continue
            try:
                r = subprocess.run(cmd, cwd=wt, input=prompt, text=True, encoding="utf-8", errors="replace",
                                   capture_output=True, timeout=int(st.get("timeout_min", 180)) * 60, env=env)
                rc, out = r.returncode, (r.stdout or "") + "\n--- stderr ---\n" + (r.stderr or "")
            except subprocess.TimeoutExpired as e:
                rc, out = 124, f"시간 초과 ({st.get('timeout_min')}분)\n{e.stdout or ''}"
            outs.append(f"===== {st.get('name', i)} ({who}) 종료 코드 {rc} =====\n{out}")
            res_f = wt / "LOCAL_RESULT.md"
            if res_f.exists():
                results.append(res_f.read_text(encoding="utf-8").rstrip())
                res_f.unlink()
            if stop_f.exists() or rc:
                stopped_at = i
                break
        if a.dry_run:
            run.log("dry-run: 여기까지 (에이전트 실행 안 함)")
            return
        mins = (time.time() - t0) / 60
        res = "\n\n".join(results) or f"{a.job}: 보고 없음 (종료 코드 {rc}) — 로그 확인"
        first = res.strip().splitlines()[0] if res.strip() else a.job
        qs = job.get("quiet_skip")
        quiet = [steps[0].get("name")] if qs is True else (qs or [])
        if stopped_at is not None and not rc and steps[stopped_at].get("name") in quiet:
            # 훑기·판단 단계에서 멈춤(새 소재 없음·안 만듦) — 2시간마다 알림·보고 파일을 쌓지 않고 로그 한 줄만
            run.log(f"끝: {first} ({mins:.0f}분)")
            (run.home / "logs" / f"{a.job}.last.txt").write_text("\n\n".join(outs), encoding="utf-8")
            return
        moved = mirror_media(wt, run)
        prune_media(wt, run)
        rep = run.home / "reports" / f"{stamp}-{a.job}.md"
        rep.parent.mkdir(parents=True, exist_ok=True)
        rep.write_text(res.rstrip() + f"\n\n---\n에이전트 {who} · 종료 코드 {rc} · {mins:.0f}분\n"
                       + ("\n".join(f"- {m}" for m in moved) or "- Drive 로 옮길 새 큰 파일 없음") + "\n", encoding="utf-8")
        (run.home / "logs" / f"{stamp}-{a.job}.agent.txt").write_text("\n\n".join(outs), encoding="utf-8")
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
