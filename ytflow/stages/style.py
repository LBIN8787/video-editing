"""0.5단계: 편집 스타일 분석 — 레퍼런스 영상 파일을 재고 읽어서 '편집 규칙'과 '렌더러 설정값'을 만든다.

사람이 영상을 보고 손으로 정리하던 일을 자동화한다.
  python -m ytflow style 미주일기 ~/Downloads/a.mp4 ~/Downloads/b.mp4

측정 (ffmpeg + numpy, 사람 판단 없음)
  - 하드 컷 수, 2초 단위 화면 변화 이벤트(분당), 정지 프레임 비율 → 편집 리듬
  - 밝은 화면/어두운 화면 비율, 종이색·잉크색·강조색(빨강/노랑) → 팔레트
  - 하단 가운데 어두운 자막 상자가 있는 비율 → 자막 방식
  - 말 사이 쉬는 구간의 음량 → 배경음악 유무
해석 (Claude 가 장면 미리보기 시트를 직접 보고)
  - 레이아웃, 움직임, 반복 요소, 타이포그래피, 장 전환 방식 → 규칙 문장
산출물: data/styles/<이름>/
  metrics.json   측정값          rules.json   해석한 편집 규칙
  edit.yaml      이 스타일로 편집할 때 프로젝트에 넣는 설정 (make --style-ref <이름>)
  sheet_*.png    장면 미리보기 (타 채널 화면이므로 저장소에 올리지 않음)
"""
from __future__ import annotations

import colorsys
import json
import re
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from pydantic import BaseModel, Field

from .. import config, llm


def _ff_frames(video: Path, fps: float, w: int, h: int, gray: bool) -> np.ndarray:
    pix = "gray" if gray else "rgb24"
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(video), "-vf", f"fps={fps},scale={w}:{h}",
           "-f", "rawvideo", "-pix_fmt", pix, "-"]
    raw = subprocess.run(cmd, capture_output=True).stdout
    ch = 1 if gray else 3
    n = len(raw) // (w * h * ch)
    return np.frombuffer(raw[: n * w * h * ch], np.uint8).reshape((n, h, w) if gray else (n, h, w, 3))


def _duration(video: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(video)],
                         capture_output=True, text=True).stdout.strip()
    return float(out or 0)


def _hard_cuts(video: Path) -> int:
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(video), "-vf", "scale=320:-2,select='gt(scene,0.25)',showinfo",
                          "-f", "null", "-"], capture_output=True, text=True).stderr
    return len(re.findall(r"pts_time:", err))


def _hex(c) -> str:
    return "#%02X%02X%02X" % tuple(int(x) for x in c)


def _audio(video: Path) -> dict:
    raw = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(video), "-vn", "-ac", "1", "-ar", "8000",
                          "-f", "s16le", "-"], capture_output=True).stdout
    a = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    if a.size < 8000:
        return {}
    win = 4000  # 0.5초
    rms = np.sqrt(np.mean(a[: a.size // win * win].reshape(-1, win) ** 2, axis=1) + 1e-12)
    db = 20 * np.log10(rms)
    p10, p50 = float(np.percentile(db, 10)), float(np.percentile(db, 50))
    # 말과 말 사이(하위 10%)도 일정 음량 이상이면 배경음악이 깔린 것으로 본다
    return {"median_db": round(p50, 1), "quiet_p10_db": round(p10, 1), "bgm_likely": p10 > -42}


def measure(video: Path, out: Path, tag: str) -> dict:
    dur = _duration(video)
    g = _ff_frames(video, 2, 160, 90, True).astype(np.float32)
    d = np.abs(np.diff(g, axis=0)).mean(axis=(1, 2)) if len(g) > 1 else np.zeros(1)
    ev = [i for i in range(1, len(d) - 1) if d[i] > 2.5 and d[i] >= d[i - 1] and d[i] >= d[i + 1]]
    gaps = np.diff(np.array(ev) / 2) if len(ev) > 1 else np.array([0])
    rgb = _ff_frames(video, 1, 320, 180, False)
    lum = rgb.mean(axis=3)
    bright = lum.mean(axis=(1, 2)) > 170
    dark = lum.mean(axis=(1, 2)) < 90
    m = {"file": video.name, "duration_min": round(dur / 60, 2), "hard_cuts": _hard_cuts(video)}
    m["hard_cuts_per_min"] = round(m["hard_cuts"] / max(dur / 60, 1e-6), 2)
    m.update({"change_events_per_min": round(len(ev) / max(dur / 60, 1e-6), 1),
              "median_change_gap_s": round(float(np.median(gaps)), 2),
              "static_ratio": round(float((d < 0.6).mean()), 2),
              "bright_ratio": round(float(bright.mean()), 2), "dark_ratio": round(float(dark.mean()), 2)})
    # 팔레트: 밝은 화면에서 종이(가장 흔한 밝은 색), 잉크(어둡고 채도 낮은 색), 강조(채도 높은 색)
    if bright.any():
        px = rgb[bright][:, 20:-40, :, :].reshape(-1, 3).astype(np.float32)  # 아래 자막 영역 제외
        L = px.mean(axis=1)
        m["paper"] = _hex(np.median(px[L > np.percentile(L, 40)], axis=0))
        hsv = np.array([colorsys.rgb_to_hsv(*(p / 255)) for p in px[:: max(1, len(px) // 40000)]])
        sub = px[:: max(1, len(px) // 40000)]
        ink = sub[(hsv[:, 2] < 0.45) & (hsv[:, 2] > 0.08)]
        if len(ink):
            m["ink"] = _hex(np.median(ink, axis=0))
        sat = (hsv[:, 1] > 0.45) & (hsv[:, 2] > 0.35)
        for name, (h0, h1) in {"red": (0.95, 1.0), "red2": (0.0, 0.05), "yellow": (0.11, 0.18), "blue": (0.55, 0.70)}.items():
            sel = sat & (hsv[:, 0] >= h0) & (hsv[:, 0] <= h1)
            if sel.sum() > 30:
                m[f"accent_{name}"] = _hex(np.median(sub[sel], axis=0))
                m[f"accent_{name}_share"] = round(float(sel.mean()), 4)
    # 자막 상자: 하단 가운데 띠(높이의 90~95%)가 바로 위 종이보다 확실히 어두운 화면의 비율
    lightish = lum.mean(axis=(1, 2)) > 130
    if lightish.any():
        band = lum[lightish][:, 162:171, 110:210]
        above = lum[lightish][:, 148:157, 110:210]
        box = ((band < 135).mean(axis=(1, 2)) > 0.45) & ((above.mean(axis=(1, 2)) - band.mean(axis=(1, 2))) > 40)
        m["subtitle_box_ratio"] = round(float(box.mean()), 2)
    m["audio"] = _audio(video)
    # 장면 미리보기 시트 (10초마다 1장, 시트당 36장)
    frames = _ff_frames(video, 0.1, 320, 180, False)
    sheets = []
    for k in range(0, len(frames), 36):
        im = Image.new("RGB", (1920, 1080))
        dr = ImageDraw.Draw(im)
        for i, fr in enumerate(frames[k:k + 36]):
            im.paste(Image.fromarray(fr), ((i % 6) * 320, (i // 6) * 180))
            t = (k + i) * 10
            dr.text(((i % 6) * 320 + 4, (i // 6) * 180 + 2), f"{t // 60}:{t % 60:02d}", fill=(255, 0, 0))
        f = out / f"sheet_{tag}_{k // 36}.png"
        im.save(f)
        sheets.append(f)
    # 움직임 띠: 변화가 큰 구간 3곳을 0.2초 간격으로
    strips = []
    for j, i in enumerate(sorted(ev, key=lambda i: -d[i])[:3]):
        f = out / f"motion_{tag}_{j}.png"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(max(0, i / 2 - 1)), "-t", "3", "-i", str(video),
                        "-vf", "fps=5,scale=320:180,tile=5x3", "-frames:v", "1", str(f)])
        if f.exists():
            strips.append(f)
    return {"metrics": m, "images": sheets[:2] + strips}


class StyleRules(BaseModel):
    summary: str
    backgrounds: list[str] = Field(description="배경 종류와 언제 쓰는지")
    layout: list[str] = Field(description="화면 배치 규칙")
    motion: list[str] = Field(description="움직임·전환 규칙 (무엇이 어떻게 나타나고 카메라가 어떻게 움직이는지)")
    recurring_elements: list[str] = Field(description="반복해서 나오는 요소 (종이 칩, 사진, 캐릭터, 형광펜 등)")
    typography: list[str]
    subtitles: str
    sound: str
    renderer_gaps: list[str] = Field(description="현재 ytflow 렌더러(검은 카드 sixsigma / 종이 손그림 paper)가 아직 못 하는 것")


def run(name: str, videos: list[str]) -> Path:
    out = config.DATA_DIR / "styles" / name
    out.mkdir(parents=True, exist_ok=True)
    results = []
    for i, v in enumerate(videos):
        print(f"[style] 측정: {Path(v).name}")
        results.append(measure(Path(v).expanduser(), out, f"v{i}"))
    metrics = [r["metrics"] for r in results]
    (out / "metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")

    def avg(k):
        vals = [m[k] for m in metrics if isinstance(m.get(k), (int, float))]
        return round(sum(vals) / len(vals), 2) if vals else None

    def first(k):
        return next((m[k] for m in metrics if m.get(k)), None)

    paperish = (avg("bright_ratio") or 0) > 0.5
    red = first("accent_red") or first("accent_red2")
    edit = {"style": "paper" if paperish else "sixsigma", "subtitle_box": (avg("subtitle_box_ratio") or 0) > 0.3}
    if paperish:
        gap = avg("median_change_gap_s") or 2.0
        edit["paper"] = {k: v for k, v in {"base": first("paper"), "ink": first("ink"), "red": red,
                                           "anim_seconds": round(min(max(gap * 0.6, 0.8), 1.8), 2)}.items() if v}
    else:
        edit["theme"] = {k: v for k, v in {"accent": red}.items() if v}
    if all(m.get("audio", {}).get("bgm_likely") for m in metrics if m.get("audio")):
        edit["bgm_hint"] = "레퍼런스에 배경음악이 깔려 있음 → edit.bgm 에 음원 파일을 지정하세요"
    import yaml
    (out / "edit.yaml").write_text(f"# {name} 레퍼런스 영상에서 자동 측정한 편집 설정 (ytflow style)\n"
                                   + yaml.safe_dump({"edit": edit}, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print(f"[style] 측정값 → {out}/metrics.json, 설정 → {out}/edit.yaml")
    imgs = [p for r in results for p in r["images"]][:8]
    print("[style] 장면 시트를 Claude 가 읽고 규칙 작성 중")
    rules = llm.structured(
        "당신은 유튜브 편집 감독입니다. 레퍼런스 채널의 장면 미리보기 시트(10초 간격)와 움직임 띠(0.2초 간격), "
        "측정값을 보고 '다른 영상에도 재현 가능한 편집 규칙'을 한국어로 정리하세요. 관찰한 것만 쓰고, 추정은 '추정'이라고 표시하세요. "
        "대사·고유 캐릭터·로고를 베끼는 규칙은 쓰지 말고 구조와 기법만 적으세요.",
        json.dumps({"channel": name, "metrics": metrics}, ensure_ascii=False), StyleRules, images=imgs)
    (out / "rules.json").write_text(json.dumps(rules.model_dump(), ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[style] 규칙 → {out}/rules.json")
    return out
