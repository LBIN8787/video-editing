"""업로드 전 종합 검수 — 통과해야 yt-publish 가 새 영상을 올린다.

2026-11-21 사용자: "업로드 하기 전 항상 글씨겹침 그래픽끼리 겹침 자막밀림 자막과 나레이션 싱크 화면과 자막이 일치하는지 등
종합적으로 검수하세요" (manual/09 §9-1)

    python -m ytflow preflight <프로젝트>            # 기계 검사 + 장면 프레임 모음(05_edit/preflight_frames.jpg)
    python -m ytflow preflight <프로젝트> --looked   # 프레임 모음을 눈으로 본 뒤: 사람 눈 확인까지 통과로 기록

무엇을 보나 (왜):
1. 글씨끼리·그래픽끼리·글씨와 카드·자막 자리 겹침, 화면 밖 잘림 — overlapqa 를 완성본 기준으로 새로 돌림 (예전 결과를 믿지 않음)
2. 자막 ↔ 내레이션 싱크 — syncqa 를 새로 돌려 전체 95% 와 **가장 많이 밀린 한 줄**을 함께 봄
   (평균이 좋아도 한 줄이 2~3초 밀리면 보는 사람에게는 밀린 영상이다 — 11/21 심층에서 실제로 그랬음)
3. 화면 ↔ 소리 (영상과 음성 길이·어긋남)
4. 렌더 전 배치 점검 layout_qa 가 비어 있나
5. 대본 검사 check 의 MUST 실패가 없나 (화면 숫자 = 대사 숫자 같은 규칙 포함)
6. 사람 눈: 장면마다 끝 프레임을 한 장에 모은 그림을 실제로 봤나 (--looked)
결과: 05_edit/preflight.json — final.mp4 가 바뀌면 다시 해야 함 (파일 크기·시각을 같이 적음).
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

from ..project import Project

LINE_MAX = 1.0      # 자막 한 줄이 소리보다 이만큼 넘게 어긋나면 실패 — 보는 사람이 '밀렸다'고 느끼는 정도
P95_MAX = 0.5       # manual/09 §9 의 기존 기준 (95% 가 0.5초 안)
AV_MAX = 0.1        # 화면−소리


def _stamp(f: Path) -> dict:
    st = f.stat()
    return {"size": st.st_size, "mtime": int(st.st_mtime)}


def frames_sheet(project: Project) -> Path:
    """장면마다 끝 무렵 프레임 한 장씩 → 한 장의 모음 그림 (사람 눈 확인용)."""
    from PIL import Image, ImageDraw
    edir = project.dir("edit")
    tl = json.loads((edir / "hybrid_timeline.json").read_text(encoding="utf-8"))
    tmp = edir / "hb_work" / "preflight"
    tmp.mkdir(parents=True, exist_ok=True)
    t, shots = 0.0, []
    for x in tl:
        ts = t + x["dur"] * 0.9
        out = tmp / f"{x['scene']:03d}.jpg"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{ts:.2f}", "-i", str(edir / "final.mp4"),
                        "-frames:v", "1", "-vf", "scale=640:-1", str(out)], check=False)
        if out.exists():
            shots.append((x["scene"], out))
        t += x["dur"]
    cols, w, h = 4, 640, 360
    rows = (len(shots) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * w, rows * h), "black")
    for k, (sid, f) in enumerate(shots):
        im = Image.open(f).resize((w, h))
        ImageDraw.Draw(im).text((8, 8), f"#{sid}", fill=(255, 60, 60))
        sheet.paste(im, ((k % cols) * w, (k // cols) * h))
    out = edir / "preflight_frames.jpg"
    sheet.save(out, quality=85)
    return out


def run(project: Project, looked: bool = False) -> dict:
    edir = project.dir("edit")
    final = edir / "final.mp4"
    if not final.exists():
        raise SystemExit("[preflight] 05_edit/final.mp4 가 없습니다 — 먼저 렌더")
    res = {"project": project.path.name, "final": _stamp(final), "at": time.strftime("%Y-%m-%dT%H:%M:%S"), "checks": {}}
    C = res["checks"]

    # 1. 겹침 (완성본 장면 HTML 로 새로)
    from . import overlapqa
    ov = overlapqa.run(project.path.name)
    n_ov = sum(len(v["issues"]) for v in ov["scenes"].values())
    C["overlap"] = {"pass": n_ov == 0, "issues": n_ov, "file": "05_edit/overlap_qa.json"}

    # 2·3. 싱크 (새로 잼)
    from . import syncqa
    sq = syncqa.run(project)
    worst = max((abs(w.get("off", 0)) for w in sq.get("worst", [])), default=0.0)
    C["subtitle_sync"] = {"pass": bool(sq.get("p95_abs_offset") is not None and sq["p95_abs_offset"] <= P95_MAX and worst <= LINE_MAX),
                          "p95": sq.get("p95_abs_offset"), "worst_line": round(worst, 2),
                          "worst": [w for w in sq.get("worst", []) if abs(w.get("off", 0)) > LINE_MAX][:5]}
    av = sq.get("video_minus_audio_s")
    C["av_sync"] = {"pass": av is not None and abs(av) <= AV_MAX, "video_minus_audio_s": av}

    # 4. 배치 점검
    lq = project.dir("assets") / "layout_qa.json"
    lqd = json.loads(lq.read_text(encoding="utf-8")) if lq.exists() else {}
    C["layout"] = {"pass": not lqd, "issues": len(lqd) if isinstance(lqd, (dict, list)) else 1}

    # 5. 대본 검사 (MUST)
    r = subprocess.run([sys.executable, "-m", "ytflow", "check", str(project.path)], capture_output=True, text=True,
                       env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8"})
    C["check_must"] = {"pass": r.returncode == 0, "tail": (r.stdout or r.stderr).strip().splitlines()[-3:]}

    # 6. 사람 눈
    sheet = frames_sheet(project)
    C["looked"] = {"pass": bool(looked), "sheet": str(sheet.relative_to(project.path)).replace("\\", "/"),
                   "note": "프레임 모음을 직접 보고 겹침·잘림·화면 숫자=자막 숫자를 확인한 뒤 --looked 로 다시"}

    res["pass"] = all(v["pass"] for v in C.values())
    (edir / "preflight.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    bad = [k for k, v in C.items() if not v["pass"]]
    print(f"[preflight] {'통과' if res['pass'] else '실패: ' + ', '.join(bad)} → {edir / 'preflight.json'}")
    for k in bad:
        print(f"  ✗ {k}: {json.dumps({kk: vv for kk, vv in C[k].items() if kk != 'pass'}, ensure_ascii=False)[:300]}")
    return res


def gate(project: Project) -> str | None:
    """yt-publish 가 새로 올리기 전에 부름. 문제가 있으면 이유 문장, 없으면 None."""
    edir = project.dir("edit")
    f = edir / "preflight.json"
    if not f.exists():
        return "업로드 전 종합 검수를 안 했습니다 — python -m ytflow preflight <프로젝트> (manual/09 §9-1)"
    d = json.loads(f.read_text(encoding="utf-8"))
    if (edir / "final.mp4").exists() and d.get("final") != _stamp(edir / "final.mp4"):
        return "검수한 뒤 final.mp4 가 바뀌었습니다 — preflight 를 다시"
    if not d.get("pass"):
        bad = [k for k, v in d.get("checks", {}).items() if not v.get("pass")]
        return "종합 검수 실패: " + ", ".join(bad) + " (05_edit/preflight.json)"
    return None
