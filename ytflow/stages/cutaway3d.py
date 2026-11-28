"""3D 구조 장면 (cutaway3d) — 글씨 카드로 끝내기 아까운 '구조·공간·내부·연결' 설명을 3D 세트로 보여 준다.

(2026-11-29 사용자: "단순 글씨카드에서 끝나는게 아니라 추가 설명이 있으면 좋은 장면은 3d그래픽이나 상황에 따라
 모션그래픽 등을 추가 할 수 있도록") — 마벨 광학 편 3D(styles/3d-docu-motion, GPT 제작)를 시간 고정 영상에서
 '대본으로 움직이는 세트'로 바꿨다. 세트·샷 목록은 styles/3d-docu-motion/sets.yaml.

장면 (hybrid.json):
  {"type": "cutaway3d", "set": "dc-rack", "label": "개념 재현 · 배선과 비례 단순화",
   "chrome": "lite",                       # lite(기본): 왼쪽 위 구간 표시 + 이름표 + 오른쪽 위 범례 / full: 아래 큰 제목까지 / none: 3D 만
   "titles": {"open": ["NVLink", "한 랙 안 GPU 72개를 하나로"]},   # 샷 id → [구간 이름, 큰 제목, 작은 줄] (null 은 기본값)
   "labels": {"광 링크": "이더넷·인피니밴드", "가상 광 경로": ""},  # 이름표·범례 글자 바꾸기 ("" = 지움)
   "beats": [
     {"say": "AI 데이터센터에는 연결이 두 종류 있습니다.", "shot": "room"},
     {"say": "랙과 랙 사이는 빛으로 잇고,", "shot": "scaleout", "at": "랙과 랙"},   # at: 그 낱말을 말하는 순간 샷 시작
     {"say": "한 랙 안의 GPU 끼리는 구리로 묶습니다.", "shot": [{"shot": "open"}, {"shot": "copper", "at": "구리"}]}
   ]}
shot 이 없는 박자는 앞 샷이 이어진다. 샷 구간은 박자 길이에 맞춰 0.6~2배 빠르기로 늘거나 줄고, 다 돌면 마지막 화면에 멈춘다.
렌더는 브라우저(WebGL2·SwiftShader)로 프레임을 뽑아 04_assets/hb/scene_NNN/assets/cut3d_*.mp4 를 만들고 원본 영상처럼 깐다
(같은 장면·같은 시각이면 다시 만들지 않음).

미리보기: python -m ytflow cutaway3d sheet [--set dc-rack] [--out 경로.jpg]   # 샷마다 한 장씩 모은 접촉 인화
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import subprocess
from pathlib import Path

import yaml

from .. import config

KIT = config.ROOT / "styles" / "3d-docu-motion"
FONT = config.ROOT / "ytflow" / "assets" / "fonts" / "NanumGothic-ExtraBold.ttf"
FPS = 30
CHROME_WIN = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
GL_ARGS = ["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"]


def sets() -> dict:
    return (yaml.safe_load((KIT / "sets.yaml").read_text(encoding="utf-8")) or {}).get("sets", {}) or {}


def get_set(sid: str) -> dict:
    s = sets().get(sid)
    if not s:
        raise ValueError(f"cutaway3d: 세트 '{sid}' 없음 — styles/3d-docu-motion/sets.yaml ({', '.join(sets())})")
    return s


# ---------------------------------------------------------------- 시간: 박자 → 세트 시각
def cues(sc: dict, bt: list) -> list[tuple[float, str]]:
    """[(장면 안 초, 샷 id)] — 박자의 shot(문자열·목록)과 at 낱말로."""
    from . import motion2
    out = []
    for k, (b, (t0, d)) in enumerate(zip(sc.get("beats") or [], bt)):
        sh = b.get("shot")
        if not sh:
            continue
        items = [sh] if isinstance(sh, (str, dict)) else list(sh)
        for i, it in enumerate(items):
            it = {"shot": it} if isinstance(it, str) else it
            at = it.get("at") or (b.get("at") if i == 0 and isinstance(b.get("at"), str) else None)
            t = t0 + (0.0 if i == 0 else 0.6 * i)
            if at and sc.get("_project_dir"):
                w = motion2.row_time(sc, k, b, t0, d, at)
                if w is not None:
                    t = max(t0, w - 0.15)
            out.append((round(t, 3), it["shot"]))
    out.sort()
    if not out:
        out = [(0.0, s) for s in (sc.get("shots") or [])[:1]]
    if out:
        out[0] = (0.0, out[0][1])
    return out


def timemap(sset: dict, cs: list, dur: float, fps: int = FPS) -> list[float]:
    """장면 프레임마다 세트 시각 t."""
    shots = sset["shots"]
    n = max(1, int(round(dur * fps)))
    ts = []
    for f in range(n):
        tau = f / fps
        i = max(j for j, (s, _) in enumerate(cs) if s <= tau + 1e-9)
        s0, sid = cs[i]
        a, b = shots[sid]["span"]
        end = cs[i + 1][0] if i + 1 < len(cs) else dur
        slot = max(0.3, end - s0)
        rate = min(2.0, max(0.6, (b - a) / slot))
        ts.append(round(min(a + (tau - s0) * rate, b - 0.02), 4))
    return ts


# ---------------------------------------------------------------- 렌더
def _launch(p):
    for kw in ({}, {"executable_path": "/opt/pw-browsers/chromium"}, {"executable_path": CHROME_WIN}):
        exe = kw.get("executable_path")
        if exe and not os.path.isfile(exe):
            continue
        try:
            return p.chromium.launch(args=GL_ARGS, **kw)
        except Exception:  # noqa: BLE001 — 설치된 판이 다르면 다음 후보로
            continue
    raise RuntimeError("cutaway3d: WebGL2 를 돌릴 Chromium/Chrome 을 찾지 못함")


def _cfg(sc: dict) -> dict:
    return {"chrome": sc.get("chrome", "lite"), "titles": sc.get("titles") or {}, "labels": sc.get("labels") or {},
            "scale": 1.5, "font": FONT.as_uri() if FONT.exists() else None}


def frames(sid: str, cfg: dict, ts: list[float], batch: int = 12):
    """세트를 열어 t 목록마다 JPEG 바이트를 낸다."""
    from playwright.sync_api import sync_playwright
    sset = get_set(sid)
    html = KIT / sset["file"]
    with sync_playwright() as p:
        br = _launch(p)
        pg = br.new_page(viewport={"width": 1920, "height": 1080})
        pg.add_init_script(f"window.CFG={json.dumps(cfg, ensure_ascii=False)};")
        pg.goto(html.as_uri())
        pg.wait_for_function("() => window.frame && window.ready", timeout=120000)
        pg.evaluate("() => window.ready")
        for i in range(0, len(ts), batch):
            for d in pg.evaluate("ts => ts.map(t => frame(t, 'image/jpeg'))", ts[i:i + batch]):
                yield base64.b64decode(d)
        br.close()


def plate(sc: dict, bt: list, dur: float, outdir: Path) -> Path:
    sid = sc.get("set", "dc-rack")
    sset = get_set(sid)
    cs = cues(sc, bt)
    bad = [s for _, s in cs if s not in sset["shots"]]
    if bad:
        raise ValueError(f"cutaway3d #{sc.get('id')}: 세트 {sid} 에 없는 샷 {bad} — 있는 샷: {', '.join(sset['shots'])}")
    ts = timemap(sset, cs, dur)
    cfg = _cfg(sc)
    key = hashlib.sha1(json.dumps([sid, cfg["chrome"], cfg["titles"], cfg["labels"], ts,
                                   (KIT / sset["file"]).stat().st_mtime_ns], ensure_ascii=False).encode()).hexdigest()[:10]
    out = Path(outdir) / f"cut3d_{int(sc.get('id', 0)):03d}_{key}.mp4"
    if out.exists() and out.stat().st_size > 0:
        return out
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(".part.mp4")
    ff = subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "image2pipe", "-vcodec", "mjpeg",
                           "-framerate", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                           "-pix_fmt", "yuv420p", str(tmp)], stdin=subprocess.PIPE)
    try:
        for jpg in frames(sid, cfg, ts):
            ff.stdin.write(jpg)
    finally:
        ff.stdin.close()
        ff.wait()
    if ff.returncode != 0:
        raise RuntimeError(f"cutaway3d: ffmpeg 실패 ({ff.returncode})")
    tmp.replace(out)
    print(f"[cutaway3d] #{sc.get('id')} {sid}: 샷 {' → '.join(s for _, s in cs)} · {len(ts)} 프레임 → {out.name}")
    return out


def s_cutaway3d(D, sc, bt, dur):
    work = Path(getattr(D, "_work"))
    f = plate(sc, bt, dur, work / "assets")
    D.video(f.name, dur, "full", push=0.0)
    D.label(sc.get("label", "개념 재현 · 배선과 비례 단순화"), dark=True)
    D.chapter_tag(sc.get("_chnum", ""), sc.get("_chtitle", ""), dark=True)
    cs = cues(sc, bt)
    for t, _ in cs[1:]:   # 샷이 바뀌는 순간 가벼운 이동 소리
        D.sfx.append(("whoosh-short", t))


def register():
    from . import hybrid
    hybrid.RENDER["cutaway3d"] = s_cutaway3d
    hybrid.CAM_SKIP.add("cutaway3d")   # 자체 카메라가 있으므로 박자 카메라(확대·이동) 없음


# ---------------------------------------------------------------- 미리보기
def sheet(sid: str = "dc-rack", out: Path | None = None) -> Path:
    """샷마다 가운데 시각 한 장 → 접촉 인화 (어떤 샷을 고를지 볼 때)."""
    sset = get_set(sid)
    ids = list(sset["shots"])
    ts = [round(sum(sset["shots"][i]["span"]) / 2 + 0.6, 2) for i in ids]
    out = Path(out or (config.ROOT / ".cache" / "cutaway3d" / f"{sid}_sheet.jpg"))
    out.parent.mkdir(parents=True, exist_ok=True)
    tmpd = out.parent / f"_{sid}_frames"
    tmpd.mkdir(exist_ok=True)
    paths = []
    for i, jpg in zip(ids, frames(sid, _cfg({"chrome": "full"}), ts)):
        p = tmpd / f"{i}.jpg"
        p.write_bytes(jpg)
        paths.append(p)
    cols = 2
    args = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]
    for p in paths:
        args += ["-i", str(p)]
    while len(paths) % cols:
        paths.append(paths[-1])
        args += ["-i", str(paths[-1])]
    rows = len(paths) // cols
    # 샷 이름은 화면 왼쪽 위 구간 표시로 보임 (ffmpeg drawtext 는 Windows 에서 글꼴 설정이 없어 쓰지 않음) — 순서는 sets.yaml 순
    fc = ";".join(f"[{r * cols + c}:v]scale=960:540[v{r * cols + c}]" for r in range(rows) for c in range(cols))
    fc += ";" + ";".join("".join(f"[v{r * cols + c}]" for c in range(cols)) + f"hstack=inputs={cols}[r{r}]" for r in range(rows))
    fc += ";" + "".join(f"[r{r}]" for r in range(rows)) + f"vstack=inputs={rows}"
    subprocess.run(args + ["-filter_complex", fc, "-frames:v", "1", str(out)], check=True)
    return out


def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(prog="ytflow cutaway3d", description="3D 구조 세트 — 목록·샷 미리보기")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("list", help="세트·샷 목록")
    sh = sub.add_parser("sheet", help="샷마다 한 장씩 모은 접촉 인화")
    sh.add_argument("--set", default="dc-rack")
    sh.add_argument("--out")
    a = ap.parse_args(argv)
    if a.cmd == "sheet":
        print(sheet(a.set, Path(a.out) if a.out else None))
        return 0
    for k, s in sets().items():
        print(f"{k}: {s['name']}")
        for i, x in s["shots"].items():
            print(f"  {i:9s} {x['span'][0]:>5}–{x['span'][1]:<5} {x['shows']}")
    return 0
