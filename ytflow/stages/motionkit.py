"""고성능 모션그래픽 도구 묶음 (docs/37-motion-performance.md).

렌더러(hyper·stage·story·hybrid·shorts …)가 같이 쓰는 '움직임의 질' 부품:

1. 움직임 토큰 — 길이(DUR)·곡선(EASE)·차례 간격(STAGGER). 숫자를 렌더러마다 새로 정하지 않고 여기서 고른다.
2. smooth_zoom — 떨림 없는 확대(켄 번스). ffmpeg 의 scale(eval=frame)+crop·zoompan 은 정수 픽셀로 반올림돼
   확대가 '멈춤·점프'를 번갈아 한다(ffmpeg trac #4298). 실수 좌표 아핀 변환으로 프레임마다 그린다.
3. motion_blur_vf — 빠른 움직임에 셔터 흐림. 높은 fps 로 그린 영상을 셔터 각도만큼 평균(tmix) → 목표 fps.
4. encode_args / dither_vf — 모션그래픽용 x264 설정과 그라데이션 띠(banding) 막는 옅은 잡음.
5. lint_gsap — 만든 HTML 의 GSAP 타임라인에서 느리거나 어색한 움직임 찾기 (레이아웃 속성 애니메이션,
   위치 이동에 직선 곡선, 너무 짧은/긴 등장, 과한 튕김, 한 순간에 너무 많은 등장).

모두 '스타일 기본값' 층(manual/README §3-1) — 금지·MUST 가 아니라 기본으로 켜는 부품이다.
"""
from __future__ import annotations

import re
from pathlib import Path

# ---------------------------------------------------------------- 1. 움직임 토큰
# 영상(시청 거리·1x 재생) 기준. UI 보다 조금 길다: 화면 글자는 읽혀야 하고, 등장은 말의 박자에 붙는다.
DUR = {
    "micro": 0.18,     # 강조 깜빡임·작은 튕김
    "enter": 0.45,     # 글자·카드 등장 (0.35~0.6)
    "exit": 0.3,       # 퇴장은 등장의 약 2/3 — 사라지는 것은 시선을 붙잡지 않는다
    "move": 0.8,       # 화면 안 이동·매치 무브 (거리 클수록 길게, 1.2 이하)
    "draw": 1.1,       # 선·차트 그려지기
    "camera": 2.5,     # 카메라 이동·확대 (느리게, 박자 하나 내내)
}
EASE = {
    "enter": "power3.out",     # 빠르게 들어와 부드럽게 멈춤 (expo.out 은 더 급함)
    "exit": "power2.in",       # 천천히 출발해 빠르게 사라짐
    "move": "power2.inOut",    # 화면 안에서 A→B
    "draw": "power1.inOut",    # 선 그리기: 펜 속도가 거의 일정
    "pop": "back.out(1.7)",    # 튕김은 10~20% 넘침까지 (back.out(1.7) ≈ 10%)
    "settle": "expo.out",      # 숫자·막대가 목표값에 '착' 붙음
    "camera": "sine.inOut",    # 카메라는 가속이 눈에 띄지 않게
}
STAGGER = {"tight": 0.04, "normal": 0.07, "loose": 0.12, "max_total": 0.8}  # 차례 간격 + 전체 상한


def stagger(n: int, kind: str = "normal") -> float:
    """n개를 차례로 낼 때 간격. 전체가 max_total 을 넘지 않게 줄인다 (많을수록 간격이 좁아짐)."""
    if n <= 1:
        return 0.0
    return round(min(STAGGER.get(kind, STAGGER["normal"]), STAGGER["max_total"] / (n - 1)), 3)


def gsap_tokens_js() -> str:
    """GSAP HTML 맨 앞에 넣는 토큰 상수 (window.M.dur.enter, window.M.ease.pop …)."""
    import json
    return f"window.M={json.dumps({'dur': DUR, 'ease': EASE, 'stagger': STAGGER})};"


# ---------------------------------------------------------------- 2. 떨림 없는 확대
def _ease(p: float, kind: str) -> float:
    import math
    return {"inout": 0.5 - 0.5 * math.cos(math.pi * p), "out": 1 - (1 - p) ** 3, "linear": p}[kind]


def smooth_zoom(image, out: Path, W: int, H: int, dur: float, fps: int = 30, z0: float = 1.0, z1: float = 1.04,
                fx: float = 0.5, fy: float = 0.5, ease: str = "inout", vf: str = "", enc: str = "final") -> Path:
    """정지 그림 → 떨림 없는 확대(켄 번스) 영상.

    ffmpeg 의 scale(eval=frame)+crop·zoompan 은 자르는 위치·크기를 정수 픽셀로 반올림해서 확대가 '멈춤·점프'를
    번갈아 한다(ffmpeg trac #4298; 4배 키운 뒤 zoompan 해도 남음 — docs/37 측정). 여기서는 프레임마다
    실수 좌표 아핀 변환(바이큐빅)으로 그려 ffmpeg 에 넘긴다 → 움직임 양이 프레임마다 고르다.
    z0→z1 확대, (fx, fy) 다가가는 중심(0~1), vf: 뒤에 붙일 ffmpeg 필터(페이드 등).
    """
    import subprocess
    from PIL import Image
    im = image if isinstance(image, Image.Image) else Image.open(image)
    im = im.convert("RGB")
    s0 = max(W / im.width, H / im.height)            # 화면을 꽉 채우는 배율
    n = max(int(round(dur * fps)), 1)
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-"]
    cmd += (["-vf", vf] if vf else []) + encode_args(enc, fps) + [str(out)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    cx, cy = im.width * fx, im.height * fy           # 다가가는 점 (원본 좌표)
    for i in range(n):
        z = z0 + (z1 - z0) * _ease(i / max(n - 1, 1), ease)
        k = 1 / (s0 * z)                                # 출력 1px = 원본 k px
        # 출력의 (fx·W, fy·H) 가 원본 (cx, cy) 에 고정 → 그 점을 향해 다가감
        ox, oy = cx - fx * W * k, cy - fy * H * k
        ox = min(max(ox, 0), im.width - W * k); oy = min(max(oy, 0), im.height - H * k)
        fr = im.transform((W, H), Image.AFFINE, (k, 0, ox, 0, k, oy), resample=Image.BICUBIC)
        p.stdin.write(fr.tobytes())
    p.stdin.close()
    p.wait()
    return out


# ---------------------------------------------------------------- 3. 셔터 흐림
def motion_blur_vf(src_fps: int, fps: int = 30, shutter: float = 180.0) -> str:
    """src_fps(목표의 정수배)로 그린 영상 → 셔터 각도만큼 하위 프레임을 평균 → fps.

    180° = 프레임 시간의 절반만 열림(영화 기본). 예: 120fps 로 그리고 30fps 로 내면 4장 중 2장 평균.
    빠른 이동·회전(휙 지나가는 카드, 튀어나오는 숫자)에만 — 글자가 오래 머무는 화면은 흐림이 필요 없다.
    """
    k = src_fps // fps
    if k < 2:
        return f"fps={fps}"
    m = max(1, round(k * shutter / 360))
    return f"tmix=frames={m}:weights='{' '.join(['1'] * m)}',fps={fps}"


# ---------------------------------------------------------------- 4. 인코딩
def encode_args(kind: str = "final", fps: int = 30) -> list[str]:
    """x264 설정. graphic: 자체 제작 그래픽만 있는 장면(평면·글자), final: 실사·그래픽 섞인 납품본, draft: 빠른 초안.

    - aq-mode=3: 어두운 평면·그라데이션에 비트를 더 줌 → 띠(banding)·네모 깨짐 줄임
    - tune animation: 넓은 평면 + 또렷한 테두리에 맞춤 (실사가 섞이면 쓰지 않음)
    - GOP = 2초, faststart: 유튜브 권장 업로드 형식
    """
    base = ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-g", str(fps * 2), "-movflags", "+faststart"]
    if kind == "draft":
        return base + ["-preset", "veryfast", "-crf", "21"]
    if kind == "graphic":
        return base + ["-preset", "slow", "-crf", "16", "-tune", "animation", "-x264-params", "aq-mode=3"]
    return base + ["-preset", "slow", "-crf", "17", "-x264-params", "aq-mode=3"]


def dither_vf(strength: int = 2) -> str:
    """8비트로 줄이기 전에 옅은 시간 잡음 — 그라데이션·비네트·어두운 배경의 띠를 흩어 준다 (눈에는 안 보이는 세기 1~3)."""
    return f"noise=alls={strength}:allf=t"


# ---------------------------------------------------------------- 5. GSAP 타임라인 점검
_TWEEN = re.compile(r"tl\.(fromTo|to|from)\(\s*([^,]+),\s*(\{[^{}]*\})(?:\s*,\s*(\{[^{}]*\}))?\s*,\s*([0-9.]+)\s*\)")
_LAYOUT = re.compile(r"(?<![A-Za-z])(left|top|width|height|margin\w*|padding\w*)\s*:")
_NUM = lambda key, s: (lambda m: float(m.group(1)) if m else None)(re.search(rf"{key}\s*:\s*([0-9.]+)", s))


def lint_gsap(html: str) -> list[dict]:
    """HTML 안의 GSAP 트윈을 읽어 움직임 문제를 찾는다. [{code, at, msg}]"""
    out, starts = [], {}
    for m in _TWEEN.finditer(html):
        kind, target, a, b, at = m.group(1), m.group(2).strip(), m.group(3), m.group(4) or "", float(m.group(5))
        vars_ = b if kind == "fromTo" else a
        props = a + b
        dur = _NUM("duration", vars_) or 0.5
        ease = (re.search(r'ease\s*:\s*"([^"]+)"', vars_) or [None, ""])[1]
        moves = bool(re.search(r"(?<![A-Za-z])(x|y)\s*:", props))
        if _LAYOUT.search(props):
            out.append({"code": "layout-prop", "at": at, "msg": f"{target}: left/top/width/height 를 움직임 → transform(x·y·scale)으로 (계산이 무겁고 픽셀 단위로 떨림)"})
        if "filter" in props and "blur" in props:
            out.append({"code": "blur-anim", "at": at, "msg": f"{target}: filter:blur 애니메이션은 프레임마다 다시 그려 느림 — 짧게만"})
        if moves and ease in ("none", "linear") and "repeat" not in vars_:
            out.append({"code": "linear-move", "at": at, "msg": f"{target}: 위치 이동에 직선 곡선 → 기계적으로 보임 (걷기·흐르는 배경이 아니면 {EASE['move']})"})
        if "opacity" in props and dur < 0.12:
            out.append({"code": "too-fast", "at": at, "msg": f"{target}: {dur}s 등장 — 30fps 에서 4프레임 미만이면 '뚝' 나타난 것처럼 보임"})
        if moves and dur > 2.0 and "repeat" not in vars_:
            out.append({"code": "too-slow", "at": at, "msg": f"{target}: {dur}s 이동 — 카메라가 아니면 1.2s 이하"})
        bo = re.search(r"back\.out\(([0-9.]+)\)", ease)
        if bo and float(bo.group(1)) > 2.5:
            out.append({"code": "overshoot", "at": at, "msg": f"{target}: {ease} — 넘침이 커서 장난스러움, 1.4~2.0 권장"})
        if "opacity" in props and "stagger" not in vars_:
            starts.setdefault(round(at, 1), []).append(target)
    for at, ts in sorted(starts.items()):
        if len(ts) >= 5:
            out.append({"code": "crowd", "at": at, "msg": f"{at}s 에 {len(ts)}개가 한꺼번에 등장 — 시선이 갈 곳이 없음, stagger 로 차례로"})
    return out


def lint_dir(root: Path) -> dict:
    """폴더 아래 모든 index.html 을 점검. {파일: [문제]}"""
    res = {}
    for f in sorted(Path(root).rglob("index.html")):
        found = lint_gsap(f.read_text(encoding="utf-8", errors="ignore"))
        if found:
            res[str(f)] = found
    return res
