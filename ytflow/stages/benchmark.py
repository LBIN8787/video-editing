"""0단계: 벤치마킹 — 기준 채널의 '무엇이 터졌고, 어떻게 만들었는가'를 수치와 규칙으로 뽑는다.

산출물 (data/):
  channels/<name>/videos.json      최근 영상 목록 + 아웃라이어 점수
  channels/<name>/subs/*.vtt       상위 아웃라이어 자막
  channels/<name>/metrics.json     제목/길이/말속도/훅/컷 속도 통계
  style_profile.json               대본·편집 규칙 (이후 모든 단계가 참조)
"""
from __future__ import annotations

import json
import re
import statistics as st
import subprocess
from pathlib import Path

from pydantic import BaseModel, Field

from .. import config, llm, yt


# ---------------------------------------------------------------- 수집
def collect_channel(ch: dict, cfg: dict) -> list[dict]:
    url = ch["url"].rstrip("/")
    if "CHANGE_ME" in url:
        raise SystemExit(f"config/channels.yaml 의 '{ch['name']}' url 을 실제 채널 주소로 바꿔 주세요.")
    data = yt.flat_playlist(f"{url}/videos", cfg.get("recent_videos", 40))
    vids = []
    for e in data.get("entries") or []:
        if not e or not e.get("id"):
            continue
        vids.append({
            "id": e["id"],
            "title": e.get("title", ""),
            "views": e.get("view_count") or 0,
            "duration": e.get("duration") or 0,
        })
    longform = [v for v in vids if v["duration"] > cfg.get("shorts_max_seconds", 70)]
    median = st.median([v["views"] for v in longform]) if longform else 0
    for v in vids:
        v["outlier"] = round(v["views"] / median, 2) if median else 0.0  # 채널 중앙값 대비 배수
        v["is_short"] = v["duration"] <= cfg.get("shorts_max_seconds", 70)
    vids.sort(key=lambda v: v["outlier"], reverse=True)
    return vids


# ---------------------------------------------------------------- 통계
def title_features(titles: list[str]) -> dict:
    n = max(len(titles), 1)
    return {
        "avg_len": round(sum(len(t) for t in titles) / n, 1),
        "has_number": round(sum(bool(re.search(r"\d", t)) for t in titles) / n, 2),
        "has_question": round(sum("?" in t for t in titles) / n, 2),
        "has_quote_or_bracket": round(sum(bool(re.search(r"[\"'“”‘’\[\]()【】]", t)) for t in titles) / n, 2),
        "has_ellipsis_or_bang": round(sum(bool(re.search(r"\.\.\.|…|!", t)) for t in titles) / n, 2),
    }


def transcript_features(cues: list[dict]) -> dict:
    if not cues:
        return {}
    text = " ".join(c["text"] for c in cues)
    dur = max(cues[-1]["end"] - cues[0]["start"], 1)
    hook = " ".join(c["text"] for c in cues if c["start"] < 30)
    sentences = [s for s in re.split(r"(?<=[.?!다요죠])\s+", text) if s.strip()]
    return {
        "chars_per_minute": round(len(text.replace(" ", "")) / dur * 60),
        "avg_sentence_chars": round(sum(len(s) for s in sentences) / max(len(sentences), 1), 1),
        "questions_per_minute": round(text.count("?") / dur * 60, 2),
        "hook_30s": hook[:600],
    }


def cut_features(video: Path, threshold: float = 0.3) -> dict:
    """ffmpeg 장면 변화 감지로 분당 컷 수와 평균 샷 길이를 잰다."""
    proc = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(video), "-vf",
         f"select='gt(scene,{threshold})',showinfo", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    times = [float(m) for m in re.findall(r"pts_time:([\d.]+)", proc.stderr)]
    dur_m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", proc.stderr)
    if not dur_m:
        return {}
    dur = int(dur_m[1]) * 3600 + int(dur_m[2]) * 60 + float(dur_m[3])
    first30 = sum(1 for t in times if t < 30)
    return {
        "cuts_per_minute": round(len(times) / dur * 60, 1),
        "avg_shot_seconds": round(dur / (len(times) + 1), 2),
        "cuts_in_first_30s": first30,
    }


# ---------------------------------------------------------------- 스타일 추출
class ScriptRules(BaseModel):
    hook_patterns: list[str] = Field(description="첫 30초 훅의 반복 패턴 (예: 결론 선공개, 숫자 충격, 반전 질문)")
    structure: list[str] = Field(description="본문 섹션 순서 템플릿")
    tone: str
    sentence_style: str
    retention_devices: list[str] = Field(description="중간 이탈 방지 장치 (예고, 오픈루프, 질문)")
    cta_style: str
    banned: list[str] = Field(description="이 채널들이 하지 않는 것")


class EditRules(BaseModel):
    cut_rhythm: str
    visual_types: list[str] = Field(description="화면 구성 요소 (자료화면, 텍스트카드, 그래프, 밈 등)")
    subtitle_style: str
    emphasis_rules: str
    sound_design: str
    thumbnail_rules: list[str]
    title_formulas: list[str]


class ChannelNote(BaseModel):
    channel: str
    note: str


class StyleProfile(BaseModel):
    summary: str
    script: ScriptRules
    edit: EditRules
    per_channel_notes: list[ChannelNote]
    differentiation_ideas: list[str] = Field(description="그대로 베끼지 않고 우리 채널이 다르게 가져갈 점")


def build_profile(all_metrics: dict) -> dict:
    sys_prompt = config.prompt("style_extract")
    user = json.dumps(all_metrics, ensure_ascii=False, indent=1)
    profile = llm.structured(sys_prompt, user, StyleProfile).model_dump()
    # 수치 목표는 LLM 이 아니라 측정값으로 고정
    primary = [m for m in all_metrics.values() if m.get("role") == "primary"] or list(all_metrics.values())
    nums = [m.get("transcript_avg", {}).get("chars_per_minute") for m in primary]
    nums = [n for n in nums if n]
    cuts = [m.get("cuts_avg", {}).get("cuts_per_minute") for m in primary]
    cuts = [c for c in cuts if c]
    durs = [m.get("median_longform_minutes") for m in primary if m.get("median_longform_minutes")]
    profile["targets"] = {
        "chars_per_minute": round(st.mean(nums)) if nums else None,
        "cuts_per_minute": round(st.mean(cuts), 1) if cuts else None,
        "video_minutes": round(st.mean(durs), 1) if durs else None,
    }
    return profile


def _avg(dicts: list[dict]) -> dict:
    keys = {k for d in dicts for k, v in d.items() if isinstance(v, (int, float))}
    return {k: round(st.mean([d[k] for d in dicts if k in d]), 2) for k in keys}


# ---------------------------------------------------------------- 실행
def run(with_video: bool = False, skip_llm: bool = False) -> Path:
    cfg = config.load("channels")
    all_metrics: dict = {}
    from . import style as style_stage
    for ch in cfg["channels"]:
        if ch.get("reference_videos"):  # 편집 스타일 레퍼런스 영상 분석 (파일이 있을 때만)
            vids = [v for v in ch["reference_videos"] if Path(v).expanduser().exists()]
            if vids:
                style_stage.run(ch["name"], vids)
    for ch in [c for c in cfg["channels"] if c.get("role") != "style"]:
        name = ch["name"]
        base = config.DATA_DIR / "channels" / name
        base.mkdir(parents=True, exist_ok=True)
        print(f"[benchmark] {name}: 영상 목록 수집")
        vids = collect_channel(ch, cfg)
        (base / "videos.json").write_text(json.dumps(vids, ensure_ascii=False, indent=1), encoding="utf-8")

        longform = [v for v in vids if not v["is_short"]]
        top = longform[: cfg.get("deep_dive_top", 6)]
        tfeats, cfeats, hooks = [], [], []
        for v in top:
            print(f"  - 상세 분석: {v['title'][:40]} (x{v['outlier']})")
            vtt = yt.download_subs(v["id"], base / "subs")
            if vtt:
                tf = transcript_features(yt.parse_vtt(vtt))
                if tf:
                    tfeats.append(tf)
                    hooks.append({"title": v["title"], "outlier": v["outlier"], "hook_30s": tf.get("hook_30s", "")})
            if with_video:
                mp4 = yt.download_lowres(v["id"], base / "video")
                if mp4:
                    cf = cut_features(mp4)
                    if cf:
                        cfeats.append(cf)
                    mp4.unlink(missing_ok=True)  # 원본 영상은 보관하지 않음

        metrics = {
            "role": ch.get("role", "reference"),
            "weight": ch.get("weight", 1),
            "video_count": len(vids),
            "shorts_ratio": round(sum(v["is_short"] for v in vids) / max(len(vids), 1), 2),
            "median_longform_minutes": round(st.median([v["duration"] for v in longform]) / 60, 1) if longform else None,
            "titles_all": title_features([v["title"] for v in vids]),
            "titles_top": title_features([v["title"] for v in top]),
            "top_titles": [f"{v['title']} (x{v['outlier']})" for v in longform[:10]],
            "bottom_titles": [v["title"] for v in longform[-5:]],
            "transcript_avg": _avg([{k: v for k, v in t.items() if k != "hook_30s"} for t in tfeats]),
            "cuts_avg": _avg(cfeats),
            "hooks": hooks,
        }
        (base / "metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=1), encoding="utf-8")
        all_metrics[name] = metrics

    out = config.DATA_DIR / "benchmark_metrics.json"
    out.write_text(json.dumps(all_metrics, ensure_ascii=False, indent=1), encoding="utf-8")
    if skip_llm:
        print(f"[benchmark] 수치만 저장: {out}")
        return out
    print("[benchmark] 스타일 프로필 생성 (Claude)")
    profile = build_profile(all_metrics)
    pf = config.DATA_DIR / "style_profile.json"
    pf.write_text(json.dumps(profile, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[benchmark] 완료: {pf}")
    return pf
