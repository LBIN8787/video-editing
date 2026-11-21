"""원본 발언 영상 '필요할 때만 PC 에서 받기' 통로 (docs/50-clip-lane.md, 2026-11-20 사용자 요청).

> "클라우드에서 제 계정으로 로그인하던지 클라우드가 아니라 다운로드가 필요할 때만 뭐 따로 다운로드 하던지 할 수 있도록 해주세요"

클라우드에는 계정 로그인(쿠키)을 두지 않는다 — 세션이 일회용·공용이라 계정이 새고, 봇 확인 우회 금지(AGENTS.md '소스').
대신 일을 셋으로 나눈다:

  ① 클라우드: python -m ytflow clip-order <프로젝트>
       hybrid.json 의 footage 중 url·start·end 가 적힌 것(=bite 장면 원본) → 02_script/clip_orders.json
       + inbox/pc-tasks/<KST>-clip-fetch-<프로젝트>.md (PC 에이전트가 볼 할 일) — 둘 다 main 에 푸시
  ② PC:     python -m ytflow clip-fetch <프로젝트>
       본인 브라우저 로그인(config/pipeline.yaml clips.cookies_from_browser)으로 '그 구간만' yt-dlp 로 받음
       → 04_assets/footage/<file> + (YTFLOW_DRIVE 가 있으면) Drive ytflow/cache/clips/<프로젝트>/<file>
       → 04_assets/clip_manifest.json (파일·크기·sha256·주소·구간 — 이것만 git)
       그다음 PC 에서 바로 python -m ytflow hybrid <프로젝트> (원본이 들어간 판) → upload → yt-publish
  ③ 클라우드(선택): python -m ytflow clip-pull <프로젝트>
       Drive 가 이 환경에 붙어 있으면(YTFLOW_DRIVE 폴더 또는 rclone 리모트 YTFLOW_RCLONE_REMOTE) manifest 대로 가져와
       sha256 확인 → 04_assets/footage/. 없으면 'PC 에서 렌더' 안내만 하고 렌더는 인용 카드로 계속(hybrid.bite_fallback).

규칙(manual/09 §3-5 v80): 권리마다 다르게 — public(공공 저작물)·official(본인·회사 공식)은 길이 제한 없음,
  broadcast(방송사·언론사, 적지 않으면 이것)는 한 구간 20초 이내·한 편 60초 안팎. config/rights_blocklist.yaml 의 권리자는 받지 않음.
  내려받은 원본은 git·공개 Release 에 올리지 않음.
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path

from .. import config

MAX_ONE, MAX_ALL = 20.0, 75.0   # 초 — broadcast 만: 한 구간 20초, 한 편 60초 안팎(약간의 여유)
RIGHTS = ("public", "official", "broadcast")
KST = _dt.timezone(_dt.timedelta(hours=9))


def _sec(t) -> float:
    from .clips import to_sec
    v = to_sec(t)
    if v is None:
        raise ValueError(f"구간 시각을 읽을 수 없음: {t!r}")
    return v


def _spec(project) -> dict:
    return json.loads((project.dir("script") / "hybrid.json").read_text(encoding="utf-8"))


def _drive_dir(project) -> Path | None:
    return (config.DRIVE_DIR / "cache" / "clips" / project.path.name) if config.DRIVE_DIR else None


def orders(project) -> list[dict]:
    """hybrid.json 의 footage 가운데 url+start+end 가 있는 원본 구간 목록 (bite 장면이 쓰는 것만)."""
    spec = _spec(project)
    used = {(sc.get("clip") or {}).get("src") for sc in spec["scenes"] if sc.get("type") == "bite"}
    out = []
    for key, m in (spec.get("footage") or {}).items():
        if key not in used or not m.get("url") or m.get("start") is None or m.get("end") is None:
            continue
        st, en = _sec(m["start"]), _sec(m["end"])
        if en <= st:
            raise ValueError(f"{key}: 끝({m['end']})이 시작({m['start']})보다 앞")
        out.append({"key": key, "file": m.get("file") or f"{key}.mp4", "url": m["url"], "start": st, "end": en,
                    "dur": round(en - st, 2), "who": m.get("who", ""), "credit": m.get("credit", ""),
                    "rights": m.get("rights") if m.get("rights") in RIGHTS else "broadcast", "channel": m.get("channel", ""),
                    "scenes": [sc.get("id") for sc in spec["scenes"] if (sc.get("clip") or {}).get("src") == key]})
    return out


def blocklist() -> dict:
    """config/rights_blocklist.yaml — 신고(claim)·경고(strike)를 받은 권리자와 살아 있는 경고의 만료일."""
    import yaml
    f = config.ROOT / "config" / "rights_blocklist.yaml"
    d = (yaml.safe_load(f.read_text(encoding="utf-8")) if f.exists() else None) or {}
    return {"claim": [str(x).lower() for x in d.get("claim") or []], "strike": [str(x).lower() for x in d.get("strike") or []],
            "until": str(d.get("active_strike_until") or "")}


def blocked(o: dict, bl: dict, today: str | None = None) -> str:
    """받으면 안 되는 이유 (없으면 빈 문자열)."""
    text = " ".join(str(o.get(k, "")) for k in ("credit", "channel", "url", "who")).lower()
    for kind, name in (("strike", "저작권 경고를 보낸 권리자"), ("claim", "Content ID 신고를 건 권리자")):
        for w in bl.get(kind, []):
            if w and w in text:
                return f"{name} '{w}'"
    today = today or _dt.datetime.now(KST).strftime("%Y-%m-%d")
    if o.get("rights", "broadcast") == "broadcast" and bl.get("until") and today <= bl["until"]:
        return f"채널에 살아 있는 저작권 경고 ({bl['until']} 까지) — 방송사 원본 쓰지 않음"
    return ""


def order(project, push_task: bool = True) -> Path:
    """① 클라우드: 주문서 02_script/clip_orders.json + PC 할 일 파일."""
    od = orders(project)
    tot = sum(o["dur"] for o in od)
    bl = blocklist()
    warn = []
    for o in od:
        hit = blocked(o, bl)
        if hit:
            o["skip"] = hit
            warn.append(f"{o['key']}: {hit} → 받지 않음, 그 장면은 인용 카드로 (manual/09 §3-5)")
    bc = [o for o in od if o["rights"] == "broadcast" and not o.get("skip")]
    warn += [f"{o['key']} {o['dur']}초 > {MAX_ONE}초 (방송사 원본은 한 장면 20초 이내)" for o in bc if o["dur"] > MAX_ONE]
    btot = sum(o["dur"] for o in bc)
    if btot > MAX_ALL:
        warn.append(f"방송사 원본 합계 {btot:.0f}초 > {MAX_ALL:.0f}초 (한 편 60초 안팎)")
    od = [o for o in od if not o.get("skip")] + [o for o in od if o.get("skip")]
    fdir = project.dir("assets") / "footage"
    for o in od:
        o["have"] = (fdir / o["file"]).exists()
    p = project.dir("script") / "clip_orders.json"
    p.write_text(json.dumps({"project": project.path.name, "made": _dt.datetime.now(KST).isoformat(timespec="minutes"),
                             "total_sec": round(tot, 1), "warnings": warn, "clips": od}, ensure_ascii=False, indent=1), encoding="utf-8")
    need = [o for o in od if not o["have"] and not o.get("skip")]
    print(f"[clip-order] {len(od)}개 · 합계 {tot:.1f}초 · 없는 것 {len(need)}개 → {p}")
    for w in warn:
        print("  ⚠️", w)
    if push_task and need:
        tdir = config.ROOT / "inbox" / "pc-tasks"
        tdir.mkdir(parents=True, exist_ok=True)
        t = tdir / f"{_dt.datetime.now(KST):%Y%m%d-%H%M}-clip-fetch-{project.path.name}.md"
        rows = "\n".join(f"| {o['key']} | {o['who']} | {o['url']} | {o['start']:.1f}~{o['end']:.1f}초 ({o['dur']}초) | 장면 {o['scenes']} |" for o in need)
        t.write_text(f"""---
from: claude-code
type: clip-fetch
project: {project.path.name}
status: pending
---

PC 에서 원본 발언 구간만 받아 주세요 (docs/50-clip-lane.md). 클라우드는 유튜브 봇 확인 때문에 받지 못합니다.

```
git pull
python -m ytflow clip-fetch {project.path.name}      # 본인 브라우저 로그인으로 아래 구간만 받음 → Drive + 04_assets/footage
python -m ytflow hybrid {project.path.name}          # 원본이 들어간 판으로 다시 렌더
git add projects/{project.path.name}/04_assets/clip_manifest.json && git commit -m "clip-fetch {project.path.name}" && git push
```

| 원본 | 누구 | 주소 | 구간 | 쓰는 장면 |
|---|---|---|---|---|
{rows}

끝나면 이 파일의 status 를 done 으로 바꾸고 아래에 결과(받은 파일·길이·실패 이유)를 적어 주세요.
""", encoding="utf-8")
        print(f"[clip-order] PC 할 일 → {t.relative_to(config.ROOT)}")
    return p


def _sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def _manifest_path(project) -> Path:
    return project.dir("assets") / "clip_manifest.json"


def fetch(project, force: bool = False) -> dict:
    """② PC: 주문서의 구간만 받는다 (본인 브라우저 로그인). 클라우드에서 실행하면 막힐 수 있음 — 우회하지 않음."""
    from .clips import download
    p = project.dir("script") / "clip_orders.json"
    od = json.loads(p.read_text(encoding="utf-8"))["clips"] if p.exists() else orders(project)
    fdir = project.dir("assets") / "footage"
    fdir.mkdir(parents=True, exist_ok=True)
    ddir = _drive_dir(project)
    if ddir:
        ddir.mkdir(parents=True, exist_ok=True)
    mp = _manifest_path(project)
    man = json.loads(mp.read_text(encoding="utf-8")) if mp.exists() else {"project": project.path.name, "clips": {}}
    ok = 0
    bl = blocklist()
    for o in od:
        why = o.get("skip") or blocked(o, bl)
        if why:   # 신고·경고 받은 권리자, 또는 살아 있는 경고 동안의 방송사 원본 → 받지 않음 (manual/09 §3-5)
            print(f"[clip-fetch] {o['key']} 건너뜀 — {why}")
            continue
        out = fdir / o["file"]
        if out.exists() and not force:
            print(f"[clip-fetch] {o['key']} 이미 있음")
        else:
            tmp = out.with_suffix(".dl.mp4")
            tmp.unlink(missing_ok=True)
            print(f"[clip-fetch] {o['key']} {o['url']} {o['start']:.1f}~{o['end']:.1f}초 받는 중")
            if not download(o["url"], o["start"], o["end"], tmp):
                print(f"[clip-fetch] {o['key']} 실패 — 봇 확인이면 config/pipeline.yaml clips.cookies_from_browser 확인 (우회하지 않음)")
                man["clips"][o["key"]] = {**man["clips"].get(o["key"], {}), "status": "failed"}
                continue
            # Drive·클라우드 커넥터(파일당 10MB)에 맞게 1080p·H.264 로 다시 묶음 (원본 오디오 유지)
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(tmp), "-vf", "scale=-2:min(1080\\,ih)",
                            "-c:v", "libx264", "-crf", "23", "-preset", "medium", "-c:a", "aac", "-b:a", "160k",
                            "-movflags", "+faststart", str(out)], check=True)
            tmp.unlink(missing_ok=True)
        if ddir:
            shutil.copy2(out, ddir / o["file"])
        man["clips"][o["key"]] = {"file": o["file"], "bytes": out.stat().st_size, "sha256": _sha(out), "url": o["url"],
                                  "start": o["start"], "end": o["end"], "status": "ok",
                                  "drive": f"ytflow/cache/clips/{project.path.name}/{o['file']}" if ddir else "",
                                  "fetched": _dt.datetime.now(KST).isoformat(timespec="minutes")}
        ok += 1
    mp.write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[clip-fetch] {ok}/{len(od)} 준비됨 → {mp}" + ("" if ddir else " (YTFLOW_DRIVE 없음: Drive 사본 없이 이 PC 에만)"))
    return man


def pull(project) -> int:
    """③ 클라우드(선택): Drive 가 붙어 있으면 manifest 대로 가져온다. 몇 개를 새로 가져왔는지 돌려줌."""
    mp = _manifest_path(project)
    if not mp.exists():
        return 0
    man = json.loads(mp.read_text(encoding="utf-8"))
    fdir = project.dir("assets") / "footage"
    fdir.mkdir(parents=True, exist_ok=True)
    ddir = _drive_dir(project)
    remote = os.environ.get("YTFLOW_RCLONE_REMOTE")   # 예: "gdrive:" (rclone config 에 사용자가 만든 리모트)
    got = 0
    for key, m in man.get("clips", {}).items():
        if m.get("status") != "ok":
            continue
        dst = fdir / m["file"]
        if dst.exists() and _sha(dst) == m["sha256"]:
            continue
        src = ddir / m["file"] if ddir and (ddir / m["file"]).exists() else None
        if src:
            shutil.copy2(src, dst)
        elif remote and shutil.which("rclone") and m.get("drive"):
            subprocess.run(["rclone", "copyto", f"{remote}{m['drive']}", str(dst)], check=False)
        if dst.exists() and _sha(dst) == m["sha256"]:
            got += 1
            print(f"[clip-pull] {key} 가져옴 ({m['bytes'] / 1e6:.1f}MB)")
        else:
            dst.unlink(missing_ok=True)
            print(f"[clip-pull] {key} 못 가져옴 — 이 환경에 Drive 가 없음. PC 에서 clip-fetch 뒤 hybrid 로 렌더 (docs/50)")
    return got
