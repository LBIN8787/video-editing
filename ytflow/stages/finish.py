"""마스터링: 가편집(draft.mp4) → 유튜브 납품본(final.mp4). ffmpeg-skill 도구를 그대로 부른다.

1. loudness.py  — 2패스 EBU R128 음량 정규화: 유튜브 기준 -14 LUFS, 최대 -1.5 dBTP(AAC 인코딩 여유 0.5, 기준은 -1) (영상은 다시 인코딩하지 않음)
2. check.py     — 유튜브 규격 점검 (길이·화면비·fps·코덱·색·음량) → 05_edit/delivery_check.json
3. look.py      — 프레임 시트 final_sheet.png (사람·에이전트가 눈으로 확인)

배경음 자동 낮춤(ducking)은 assemble 단계에서 이미 한다(edit.bgm). 도구가 없으면 draft.mp4 를 그대로 쓴다.
설치: python scripts/install_tools.py
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys

from .. import config
from ..project import Project

SKILL = config.ROOT / "tools" / "ffmpeg-skill" / "scripts"


def available() -> bool:
    return (SKILL / "loudness.py").exists()


def _run(script: str, *args) -> dict:
    r = subprocess.run([sys.executable, str(SKILL / script), *args, "--json"], capture_output=True, text=True, timeout=1800)
    try:
        return json.loads(r.stdout[r.stdout.find("{"):]) | {"_exit": r.returncode}
    except Exception:
        return {"_exit": r.returncode, "_error": (r.stderr or r.stdout)[-400:]}


def master(project: Project) -> None:
    edir = project.dir("edit")
    draft, final = edir / "draft.mp4", edir / "final.mp4"
    if not draft.exists():
        return
    if not available():
        shutil.copy(draft, final)
        print("[master] ffmpeg-skill 없음 → draft 를 그대로 final 로 (설치: python scripts/install_tools.py)")
        return
    target = config.load("pipeline").get("edit", {}).get("loudness_lufs", -14)
    lo = _run("loudness.py", str(draft), "-I", str(target), "--tp", "-1.5", "-o", str(final), "--overwrite")
    if lo["_exit"] or not final.exists():
        shutil.copy(draft, final)
        print(f"[master] 음량 정규화 실패 → draft 사용: {lo.get('_error', '')[:200]}")
    ck = _run("check.py", str(final), "--platform", "youtube")
    (edir / "delivery_check.json").write_text(json.dumps(ck, ensure_ascii=False, indent=1), encoding="utf-8")
    _run("look.py", str(final), "--tiles", "4x3", "-o", str(edir / "final_sheet.png"), "--overwrite")
    rows = ck.get("checks") or ck.get("rows") or []
    bad = [f"{r.get('name') or r.get('check')}: {r.get('status')}" for r in rows if str(r.get("status", "")).upper() in ("FAIL", "WARN")]
    lufs = next((r.get("actual") or r.get("value") for r in rows if "loud" in str(r.get("name") or r.get("check")).lower()), "?")
    print(f"[master] {final} · 음량 {lufs} · 유튜브 점검 {'통과' if not ck['_exit'] else '문제 있음'}"
          + (f" ({'; '.join(bad[:4])})" if bad else "") + f" · 프레임 시트 {edir / 'final_sheet.png'}")
