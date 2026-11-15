"""매뉴얼 관리: 담당자 1명 + 잠금 — 한 번에 한 명만 매뉴얼·규칙 파일을 고친다 (docs/35, manual/OWNERS.yaml).

    python -m ytflow manual-lock status                    지금 누가 잡고 있나
    python -m ytflow manual-lock acquire --purpose "…"     잡기 (담당이거나, 비어 있거나, 유효 시간이 지났을 때)
    python -m ytflow manual-lock acquire --force --reason "사용자 허락: …"   사용자가 넘기라고 했을 때만
    python -m ytflow manual-lock release                   풀기
    python -m ytflow manual-lock check [--path 파일]        지금 이 브랜치가 고쳐도 되나 (hook 용, 안 되면 종료 코드 2)
    python -m ytflow manual-propose "내용" [--kind …]       담당이 아니면: 제안함에 남기기 (proposals/manual/)

잠금은 원격 브랜치 `locks` 의 `manual-lock.json` 한 파일. 잡기·풀기는 그 파일만 바꾼 커밋을 push 하고,
두 세션이 동시에 잡으려 하면 늦은 쪽의 push 가 거절돼(빨리 감기 아님) 다시 읽고 포기한다 — git 이 순서를 정한다.
"""
from __future__ import annotations

import datetime as dt
import fnmatch
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path

import yaml

from .. import config

ROOT = config.ROOT
OWNERS = ROOT / "manual" / "OWNERS.yaml"
PROPOSALS = ROOT / "proposals" / "manual"
def _cache() -> Path:
    """마지막으로 읽은 잠금 (오프라인 hook 용) — 여러 작업 폴더(worktree)가 함께 보는 git 공용 폴더에."""
    try:
        d = subprocess.run(["git", "rev-parse", "--git-common-dir"], cwd=ROOT, capture_output=True, text=True, timeout=10).stdout.strip()
        base = (ROOT / d) if d and not Path(d).is_absolute() else Path(d or ROOT / ".git")
        return base / "manual-lock.json"
    except Exception:
        return ROOT / ".git" / "manual-lock.json"


def _git(*a, check=True, cwd=None) -> str:
    r = subprocess.run(["git", *a], cwd=cwd or ROOT, capture_output=True, text=True, timeout=60)
    if check and r.returncode != 0:
        raise RuntimeError((r.stderr or r.stdout).strip()[:300])
    return r.stdout


def owners() -> dict:
    try:
        return yaml.safe_load(OWNERS.read_text(encoding="utf-8")) or {}
    except Exception:
        return {}


def branch() -> str:
    try:
        return _git("rev-parse", "--abbrev-ref", "HEAD").strip()
    except Exception:
        return ""


def is_protected(path: str) -> bool:
    o = owners()
    p = str(path).replace("\\", "/")
    try:
        p = str(Path(p).resolve().relative_to(ROOT)).replace("\\", "/")
    except Exception:
        p = p.lstrip("./")
    if any(fnmatch.fnmatch(p, g) for g in o.get("open") or []):
        return False
    return any(fnmatch.fnmatch(p, g) or (g.endswith("/**") and p.startswith(g[:-3] + "/")) for g in o.get("protected") or [])


def _now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def read_lock(fetch: bool = True) -> dict:
    o = owners().get("lock") or {}
    br, fn = o.get("branch", "locks"), o.get("file", "manual-lock.json")
    lock, got = {}, False
    if fetch:
        try:
            _git("fetch", "-q", "origin", br)
            lock, got = json.loads(_git("show", f"FETCH_HEAD:{fn}")), True
        except Exception:
            got = False
        if got:
            try:
                _cache().write_text(json.dumps(lock, ensure_ascii=False), encoding="utf-8")
            except Exception:
                pass
    if not got:
        try:
            lock = json.loads(_cache().read_text(encoding="utf-8"))
        except Exception:
            lock = {}
            if not fetch:   # 캐시가 없으면 한 번은 원격에서 읽음 (새 클론·새 작업 폴더)
                return read_lock(fetch=True)
    return lock


def expired(lock: dict) -> bool:
    try:
        return _now() > dt.datetime.fromisoformat(lock["expires"])
    except Exception:
        return True


def holder_ok(lock: dict | None = None, me: str | None = None) -> tuple[bool, str]:
    """이 브랜치가 지금 보호 파일을 고쳐도 되나 → (되나, 이유)."""
    me = me or branch()
    lock = read_lock(fetch=False) if lock is None else lock
    if not lock or not lock.get("branch"):
        return False, "잠금이 없음 — python -m ytflow manual-lock acquire --purpose \"…\" 로 먼저 잡기"
    if lock["branch"] == me and not expired(lock):
        return True, f"잠금 보유 ({lock.get('purpose', '')})"
    if expired(lock):
        return False, f"잠금이 {lock.get('branch')} 에게 있었지만 만료됨 — 다시 잡기(acquire)"
    return False, (f"지금 매뉴얼은 '{lock.get('who', lock['branch'])}' 가 고치는 중 ({lock.get('purpose', '')}, {lock.get('expires', '')[:16]} 까지). "
                   f"매뉴얼에 넣을 것은 python -m ytflow manual-propose \"…\" 로 제안함에 남기세요 (docs/35)")


def _write_lock(new: dict | None, msg: str, force: bool = False) -> None:
    """locks 브랜치의 잠금 파일만 바꾼 커밋을 push — 동시에 잡으면 늦은 쪽 push 가 거절됨."""
    o = owners().get("lock") or {}
    br, fn = o.get("branch", "locks"), o.get("file", "manual-lock.json")
    with tempfile.TemporaryDirectory() as td:
        wt = Path(td) / "lock"
        exists = subprocess.run(["git", "ls-remote", "--exit-code", "--heads", "origin", br], cwd=ROOT,
                                capture_output=True, timeout=60).returncode == 0
        if exists:
            _git("fetch", "-q", "origin", br)
            _git("worktree", "add", "-q", "--detach", str(wt), "FETCH_HEAD")
        else:
            _git("worktree", "add", "-q", "--detach", str(wt), "HEAD")
            _git("checkout", "-q", "--orphan", f"tmp-{br}", cwd=wt)
            _git("rm", "-rq", "--cached", ".", cwd=wt, check=False)
            for p in wt.iterdir():
                if p.name != ".git":
                    subprocess.run(["rm", "-rf", str(p)])
            (wt / "README.md").write_text("# locks — 매뉴얼 잠금 (docs/35). 이 브랜치는 잠금 파일만 담습니다.\n", encoding="utf-8")
            _git("add", "README.md", cwd=wt)
        try:
            f = wt / fn
            try:   # 쓰기 직전에 원격의 실제 잠금을 다시 확인 (앞에서 잘못 읽었더라도 여기서 막음)
                have = json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}
            except Exception:
                have = {}
            me = branch()
            if have.get("branch") and have["branch"] != me and not expired(have) and not force:
                raise SystemExit(f"[manual-lock] 못 바꿈 — 원격 잠금은 {have.get('who', have['branch'])} 가 쥐고 있음 ({have.get('expires', '')[:16]} UTC 까지)")
            if new is None:
                f.write_text("{}\n", encoding="utf-8")
            else:
                f.write_text(json.dumps(new, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
            _git("add", fn, cwd=wt)
            _git("-c", "user.name=ytflow-lock", "-c", "user.email=ytflow-lock@users.noreply.github.com",
                 "commit", "-q", "-m", msg, cwd=wt)
            r = subprocess.run(["git", "push", "origin", f"HEAD:refs/heads/{br}"], cwd=wt, capture_output=True, text=True, timeout=120)
            if r.returncode != 0:
                raise RuntimeError("다른 세션이 먼저 잠금을 바꿈 — status 로 다시 확인하세요\n" + r.stderr[-300:])
        finally:
            _git("worktree", "remove", "--force", str(wt), check=False)
    try:
        _cache().write_text(json.dumps(new or {}, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass


def acquire(purpose: str, force: bool = False, reason: str = "", hours: float | None = None) -> dict:
    o = owners()
    me = branch()
    cur = read_lock()
    steward = (o.get("steward") or {}).get("branch")
    if cur.get("branch") and cur["branch"] != me and not expired(cur) and not force:
        raise SystemExit(f"[manual-lock] 못 잡음 — {cur.get('who', cur['branch'])} 가 '{cur.get('purpose', '')}' 중 ({cur.get('expires', '')[:16]} UTC 까지).\n"
                         f"  매뉴얼에 넣을 것은 python -m ytflow manual-propose \"…\" 로. 사용자가 넘기라고 했으면 --force --reason \"사용자 허락: …\"")
    if force and not reason:
        raise SystemExit("[manual-lock] --force 는 --reason \"사용자 허락: …\" 과 함께만")
    h = hours or float((o.get("lock") or {}).get("hours", 26))
    new = {"branch": me, "who": "매뉴얼 담당" if me == steward else f"세션 {me}", "steward": me == steward,
           "purpose": purpose, "since": _now().isoformat(timespec="minutes"),
           "expires": (_now() + dt.timedelta(hours=h)).isoformat(timespec="minutes"),
           "taken_from": cur.get("branch") if force and cur.get("branch") != me else None, "reason": reason or None}
    _write_lock(new, f"잠금: {new['who']} — {purpose}" + (f" (넘겨받음: {reason})" if force else ""), force=force)
    print(f"[manual-lock] 잡음 — {new['who']} · {purpose} · {new['expires'][:16]} UTC 까지")
    return new


def release() -> None:
    cur = read_lock()
    if cur.get("branch") and cur["branch"] != branch():
        raise SystemExit(f"[manual-lock] 내 잠금이 아님 ({cur.get('who')})")
    _write_lock(None, f"잠금 풀기: {branch()}")
    print("[manual-lock] 풀었음")


def status() -> str:
    cur = read_lock()
    o = owners()
    st = (o.get("steward") or {}).get("branch")
    if not cur.get("branch"):
        s = "잠금 없음 (아무도 매뉴얼을 고치는 중이 아님)"
    else:
        s = (f"{cur.get('who')} ({cur['branch']}) — {cur.get('purpose', '')} · {cur.get('since', '')[:16]} ~ {cur.get('expires', '')[:16]} UTC"
             + (" · 만료됨" if expired(cur) else ""))
    ok, why = holder_ok(cur)
    return f"매뉴얼 담당: {st}\n지금 잠금: {s}\n이 브랜치({branch()}): {'고칠 수 있음' if ok else '고칠 수 없음'} — {why}"


def propose(text: str, kind: str = "fix", project: str = "", source: str = "") -> Path:
    PROPOSALS.mkdir(parents=True, exist_ok=True)
    ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    me = re.sub(r"[^\w.-]", "_", branch())[-24:]
    f = PROPOSALS / f"{ts}-{me}.md"
    f.write_text("---\n" + yaml.safe_dump({"kind": kind, "project": project or None, "from_branch": branch(), "date": ts,
                                           "source": source or None, "status": "new"}, allow_unicode=True, sort_keys=False)
                 + "---\n" + text.strip() + "\n", encoding="utf-8")
    print(f"[manual-propose] 제안함에 남김 → {f.relative_to(ROOT)} (매뉴얼 담당이 다음 정기 검토에서 반영)")
    return f


CLOSED = {"done", "rejected", "declined", "closed", "merged"}


def proposals(status: str | None = "new") -> list[dict]:
    out = []
    for f in sorted(PROPOSALS.glob("*.md")) if PROPOSALS.exists() else []:
        s = f.read_text(encoding="utf-8")
        m = re.match(r"---\n(.*?)\n---\n(.*)", s, re.S)
        meta = (yaml.safe_load(m.group(1)) or {}) if m else {}
        st = str(meta.get("status") or "new")
        # 'open' = 아직 반영 안 된 것 전부 (new·pending 등 — 다른 에이전트가 다른 이름을 써도 놓치지 않게)
        if status == "open":
            if st in CLOSED:
                continue
        elif status and st != status:
            continue
        out.append({"file": str(f.relative_to(ROOT)), **meta, "text": (m.group(2) if m else s).strip()})
    return out


def can_write() -> bool:
    """매뉴얼을 바꾸는 명령(review·feedback·bump·graph 저장)이 쓰기 전에 묻는다. YTFLOW_MANUAL_GUARD=off 면 끔(혼자 쓸 때)."""
    if os.environ.get("YTFLOW_MANUAL_GUARD", "").lower() == "off":
        return True
    ok, _ = holder_ok()
    return ok


def guard_or_exit(what: str) -> None:
    if not can_write():
        ok, why = holder_ok()
        raise SystemExit(f"[{what}] 매뉴얼은 지금 이 브랜치가 고칠 수 없습니다 — {why}")


def hook_check_stdin() -> int:
    """Claude Code PreToolUse hook: stdin 의 도구 입력에서 파일 경로를 꺼내 보호 파일이면 잠금 확인. 막으면 종료 코드 2."""
    import sys
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    ti = data.get("tool_input") or {}
    paths = [ti.get("file_path") or ti.get("notebook_path") or ""]
    paths = [p for p in paths if p]
    bad = [p for p in paths if is_protected(p)]
    if not bad or can_write():
        return 0
    ok, why = holder_ok()
    print(f"매뉴얼·규칙 파일({', '.join(Path(p).name for p in bad)})은 한 번에 한 명만 고칩니다 (docs/35). {why}", file=sys.stderr)
    return 2


def precommit() -> int:
    """git pre-commit: 보호 파일을 커밋하려는데 잠금이 없으면 막음."""
    import sys
    staged = _git("diff", "--cached", "--name-only").split()
    bad = [p for p in staged if is_protected(p)]
    if not bad or can_write():
        return 0
    ok, why = holder_ok()
    print(f"[pre-commit] 매뉴얼·규칙 파일은 한 번에 한 명만 (docs/35): {', '.join(bad[:5])}\n  {why}\n"
          f"  → 이 변경을 빼고(git restore --staged <파일>) manual-propose 로 제안하세요.", file=sys.stderr)
    return 1
