"""완성 영상의 움직임 품질을 잰다 (docs/37-motion-performance.md).

    python -m ytflow motion-qa <프로젝트 | 영상.mp4> [--html-dir 폴더]

사람 눈이 '뚝뚝 끊긴다·떨린다·덜컥거린다'고 느끼는 것을 숫자로:
1. 프레임마다 앞 프레임과의 차이(움직임 양) d[i] 를 잰다 (흑백, 가로 960).
2. 차이가 갑자기 아주 크면 장면 바뀜(컷) — 구간을 나눈다.
3. 움직이는 구간마다
   - 멈칫(stall): 움직이는 중간에 거의 같은 프레임 (주변 9프레임 윗사분위의 30% 미만) → 프레임 중복·정수 픽셀 반올림
   - 점프(jump): 움직임 양이 주변의 1.5배 넘게 튐 → 프레임 빠짐(fps 변환·렌더 누락)·정수 픽셀 확대
   - smoothness: 움직이는 프레임 중 멈칫·점프가 아닌 비율 (1.0 이 완벽)
4. 영상 규격: fps(정수)·픽셀 형식(yuv420p)·코덱 (비트레이트는 기록만 — CRF 인코딩은 단순한 화면에서 낮게 나오는 게 정상)
5. (있으면) 프로젝트의 GSAP HTML 을 motionkit.lint_gsap 으로 점검
결과: 05_edit/motion_qa.json — 통과 기준: 문제 구간 0(멈칫·점프가 15프레임 안에 3번 이상 몰린 곳), 규격 경고 0 (SHOULD, 검사 게이트 아님).
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import numpy as np

from . import motionkit

W_ANALYZE = 960


def probe(path: Path) -> dict:
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height,r_frame_rate,pix_fmt,codec_name,bit_rate:format=bit_rate,duration",
                          "-of", "json", str(path)], capture_output=True, text=True).stdout
    d = json.loads(out or "{}")
    s = (d.get("streams") or [{}])[0]
    num, den = (s.get("r_frame_rate") or "30/1").split("/")
    br = s.get("bit_rate") or (d.get("format") or {}).get("bit_rate") or 0
    return {"width": s.get("width"), "height": s.get("height"), "fps": round(int(num) / int(den or 1), 3),
            "pix_fmt": s.get("pix_fmt"), "codec": s.get("codec_name"), "mbps": round(int(br) / 1e6, 2),
            "duration": float((d.get("format") or {}).get("duration") or 0)}


def diffs(path: Path, info: dict) -> np.ndarray:
    w = W_ANALYZE
    h = int(round(info["height"] * w / info["width"] / 2) * 2)
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(path), "-vf", f"scale={w}:{h}:flags=area,format=gray",
                          "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    size, prev, out = w * h, None, []
    while True:
        buf = p.stdout.read(size)
        if len(buf) < size:
            break
        f = np.frombuffer(buf, np.uint8).astype(np.int16)
        if prev is not None:
            out.append(float(np.abs(f - prev).mean()))
        prev = f
    p.wait()
    return np.array(out)


def _roll(x: np.ndarray, k: int, fn) -> np.ndarray:
    pad = np.pad(x, (k // 2, k // 2), mode="edge")
    return np.array([fn(pad[i:i + k]) for i in range(len(x))])


def analyze(d: np.ndarray, fps: float) -> dict:
    """프레임 차이 d[i] → 컷·움직이는 구간·멈칫/점프 프레임."""
    n = len(d)
    if n < 3:
        return {"frames": n + 1, "cuts": 0, "moving_ratio": 0, "problems": [], "long_holds": []}
    still = 0.08                                     # 이보다 작으면 '멈춘 화면' (잡음 수준)
    mv = d[d > still]
    cut = max(12.0, float(np.median(mv)) * 8 if len(mv) else 12.0)
    is_cut = d > cut
    local = _roll(np.where(is_cut, np.nan, d), 9, lambda w: np.nanpercentile(w, 75) if np.isfinite(w).any() else 0.0)  # 주변 9프레임의 윗사분위 = 이 구간의 '정상 움직임'
    near = _roll(d, 5, np.max) > still              # 근처에서 움직이는 중
    active = near & ~is_cut & (local > 0.25)         # 아주 느린 움직임(배경 숨쉬기)은 판정하지 않음
    stall = active & (d < local * 0.3)               # 움직이는 중에 거의 같은 프레임 → 프레임 중복·멈춤
    jump = active & (d > local * 1.5) & (d - local > 0.3)   # 갑자기 많이 움직임 → 프레임 빠짐·정수 픽셀 점프
    # 같은 종류가 반복되면 문제 구간 (한두 번은 연출일 수 있음): 15프레임 안에 붙은 표시를 묶는다
    flagged = np.where(stall | jump)[0]
    groups, cur = [], []
    for i in flagged:
        if cur and i - cur[-1] > 15:
            groups.append(cur); cur = []
        cur.append(int(i))
    if cur:
        groups.append(cur)
    bad = []
    for g in groups:
        a, b = g[0], g[-1] + 1
        ns, nj = int(stall[a:b].sum()), int(jump[a:b].sum())
        if ns + nj < 3:
            continue
        flags = ([f"멈칫 {ns}프레임"] if ns else []) + ([f"점프 {nj}프레임"] if nj else [])
        bad.append({"start": round(a / fps, 2), "end": round(b / fps, 2), "stalls": ns, "jumps": nj,
                    "median_motion": round(float(np.median(local[a:b])), 2), "flags": flags})
    moving = d > still
    holds, run = [], 0
    for k, m in enumerate(list(moving) + [True]):
        if not m:
            run += 1
        else:
            if run / fps >= 4:
                holds.append({"start": round((k - run) / fps, 2), "seconds": round(run / fps, 1)})
            run = 0
    smooth = 1 - float((stall | jump)[active].mean()) if active.any() else 1.0
    return {"frames": int(n + 1), "cuts": int(is_cut.sum()), "moving_ratio": round(float(moving.mean()), 3),
            "active_frames": int(active.sum()), "smoothness": round(smooth, 3), "problems": bad, "long_holds": holds}


def spec_warnings(info: dict) -> list[str]:
    w = []
    if info["fps"] and abs(info["fps"] - round(info["fps"])) > 0.01:
        w.append(f"fps {info['fps']} — 정수 fps(30·60)로 (29.97 등은 움직임 박자가 어긋남)")
    if info["pix_fmt"] not in ("yuv420p", "yuv420p10le"):
        w.append(f"픽셀 형식 {info['pix_fmt']} — 유튜브 납품은 yuv420p")
    if info["codec"] not in ("h264", "hevc", "vp9", "av1", "prores"):
        w.append(f"코덱 {info['codec']} — 유튜브 업로드는 H.264(CRF 16~18) 권장")
    return w


def run(target: str, html_dir: str | None = None) -> dict:
    t = Path(target)
    proj = None
    if not t.is_file():
        from ..project import Project
        proj = Project.open(target)
        edir = proj.dir("edit")
        t = next((edir / n for n in ("final.mp4", "draft.mp4") if (edir / n).exists()), None)
        if t is None:
            raise SystemExit(f"{edir} 에 final.mp4·draft.mp4 가 없음")
        html_dir = html_dir or str(proj.path)
    info = probe(t)
    res = {"video": str(t), "spec": info, "spec_warnings": spec_warnings(info), **analyze(diffs(t, info), info["fps"] or 30)}
    if html_dir:
        lint = motionkit.lint_dir(Path(html_dir))
        res["gsap_lint"] = {k: v[:20] for k, v in lint.items()}
        res["gsap_lint_count"] = sum(len(v) for v in lint.values())
    res["pass"] = not res["problems"] and not res["spec_warnings"]
    out = (proj.dir("edit") / "motion_qa.json") if proj else t.with_suffix(".motion_qa.json")
    out.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[motion-qa] {t.name}: {info['width']}x{info['height']} {info['fps']}fps {info['mbps']}Mbps · 컷 {res['cuts']} · "
          f"움직임 고름 {res['smoothness']:.0%} · 문제 {len(res['problems'])} · 규격 경고 {len(res['spec_warnings'])}"
          + (f" · GSAP 점검 {res['gsap_lint_count']}" if html_dir else "") + f" → {out}")
    for p in res["problems"][:10]:
        print(f"  ! {p['start']}~{p['end']}s {', '.join(p['flags'])}")
    for w in res["spec_warnings"]:
        print(f"  ! {w}")
    return res
