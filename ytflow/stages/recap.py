"""애니 소개형 (채널 ch-anime-review, docs/37 §2). 스토리 핵심 장면만 잘라 내레이션으로 이어 주는 '보게 만드는' 영상.

원작 에피소드(사용자가 정식으로 본 파일, PC 에서 준비) → 받아쓰기 → 핵심 장면 고르기 → 내레이션 → 조립.

    python -m ytflow recap <프로젝트> --transcribe   # 04_assets/episodes/* 받아쓰기 → 01_research/episodes.md (타임코드 대사표)
    python -m ytflow recap <프로젝트> --plan         # 대사표 → 02_script/recap.json 초안 (LLM, prompts/recap.md)
    python -m ytflow recap <프로젝트> --check        # 규칙 검사만 → 05_edit/recap_qa.json
    python -m ytflow recap <프로젝트>                # 검사 → 렌더 05_edit/final.mp4 + subs.srt

02_script/recap.json:
{"title": "...", "work": {"name": "작품명", "where": "넷플릭스", "max_ep": 3},
 "episodes": {"e1": {"file": "episodes/ep01.mkv", "ep": 1, "lang": "ja"}},
 "scenes": [
   {"type": "live", "clip": {"src": "e1", "from": "12:03.0", "to": "12:08.5"}, "ko": "번역 자막"},   # 원작 소리 그대로 (≤8초) — 첫 장면 훅·명대사·반전
   {"type": "narr", "clip": {"src": "e1", "from": "03:10"}, "beats": [{"say": "내레이션"}]},          # 원작 소리 낮추고 내레이션, 화면은 from 부터 말 길이만큼
   {"type": "narr", "end": true, "clip": {...}, "beats": [{"say": "다음 이야기는 넷플릭스에서…"}]}]}   # 끝: 결말 앞에서 끊고 볼 수 있는 곳

규칙 (channels/ch-anime-review/channel.yaml 의 recap_rules, 위반이면 렌더 안 함):
  원작 소리 장면 1개 ≤ 8초 · 원작 소리 합 ≤ 영상의 20% · 다루는 화 ≤ max_ep · 마지막 장면은 end + 볼 수 있는 곳
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from ..project import Project
from . import align, hybrid
from .media import _ts_srt, chunk_text

W, H = 1920, 1080
FPS = 30
BED = 0.12            # 내레이션 아래 원작 소리 크기
LIVE_MAX = 8.0
LIVE_SHARE = 0.20
PAD = 0.25            # 내레이션 끝 여유
VEXT = (".mp4", ".mkv", ".mov", ".webm", ".avi", ".m4v")


def _t(s) -> float:
    """'1:02:03.5' · '12:03' · 723.5 → 초."""
    if isinstance(s, (int, float)):
        return float(s)
    sec = 0.0
    for p in str(s).strip().split(":"):
        sec = sec * 60 + float(p)
    return sec


def _tc(t: float) -> str:
    m, s = divmod(t, 60)
    return f"{int(m // 60)}:{int(m % 60):02d}:{s:04.1f}" if m >= 60 else f"{int(m):02d}:{s:04.1f}"


def _dur(p: Path) -> float:
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True).stdout.strip() or 0)


def _rules(project: Project) -> dict:
    """채널 recap_rules (edit.yaml 의 channel, 없으면 ch-anime-review)."""
    import yaml

    from .. import config
    ch = "ch-anime-review"
    try:
        ch = (yaml.safe_load((project.path / "edit.yaml").read_text(encoding="utf-8")) or {}).get("channel") or ch
    except Exception:  # noqa: BLE001
        pass
    cy = config.ROOT / "channels" / str(ch) / "channel.yaml"
    r = ((yaml.safe_load(cy.read_text(encoding="utf-8")) or {}).get("recap_rules") or {}) if cy.exists() else {}
    return {"max_ep": int(r.get("max_ep", 3)), "live_max": float(r.get("live_max_sec", LIVE_MAX)),
            "live_share": float(r.get("live_share_max", LIVE_SHARE))}


def _spec(project: Project) -> dict:
    spec = json.loads((project.dir("script") / "recap.json").read_text(encoding="utf-8"))
    for i, sc in enumerate(spec["scenes"], 1):
        sc["id"] = i
        sc.setdefault("beats", [])
    return spec


# ------------------------------------------------------------------ 1. 받아쓰기
def _lines(words: list[dict], gap: float = 0.8, max_len: float = 7.0, lang: str | None = None) -> list[tuple[float, float, str]]:
    sep = "" if (lang or "")[:2] in ("ja", "zh") else " "
    out, cur = [], []
    for w in words:
        if cur and (w["start"] - cur[-1]["end"] > gap or w["end"] - cur[0]["start"] > max_len):
            out.append((cur[0]["start"], cur[-1]["end"], sep.join(x["word"] for x in cur)))
            cur = []
        cur.append(w)
    if cur:
        out.append((cur[0]["start"], cur[-1]["end"], sep.join(x["word"] for x in cur)))
    return out


def episodes_of(project: Project) -> dict:
    """recap.json 의 episodes, 없으면 04_assets/episodes/ 의 파일을 이름 순서로 e1, e2…"""
    p = project.dir("script") / "recap.json"
    if p.exists():
        eps = json.loads(p.read_text(encoding="utf-8")).get("episodes")
        if eps:
            return eps
    d = project.dir("assets") / "episodes"
    files = sorted(f for f in d.glob("*") if f.suffix.lower() in VEXT) if d.exists() else []
    return {f"e{i}": {"file": f"episodes/{f.name}", "ep": i, "lang": "ja"} for i, f in enumerate(files, 1)}


def transcribe(project: Project) -> Path:
    eps = episodes_of(project)
    if not eps:
        raise SystemExit(f"에피소드 파일이 없습니다: {project.dir('assets') / 'episodes'} (mp4·mkv 를 넣으세요, 커밋되지 않음)")
    if not align.available():
        raise SystemExit("faster-whisper 가 없습니다: pip install -r requirements.txt")
    md = ["# 에피소드 대사표 (받아쓰기, 타임코드는 그 화 시작 기준)", "",
          "recap.json 의 clip.from/to 에 이 타임코드를 씁니다. 받아쓰기는 틀릴 수 있으니 장면은 영상으로 확인하세요.", ""]
    for key, e in eps.items():
        f = project.dir("assets") / e["file"]
        words = align.transcribe(f, e.get("lang"))
        md += [f"## {key} · {e.get('ep', '?')}화 · {f.name} · {_tc(_dur(f))}", ""]
        md += [f"- `{_tc(a)}–{_tc(b)}` {txt}" for a, b, txt in _lines(words, lang=e.get("lang"))]
        md.append("")
    out = project.dir("research") / "episodes.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(md), encoding="utf-8")
    print(f"[recap] 대사표 → {out}")
    return out


# ------------------------------------------------------------------ 2. 초안
def plan(project: Project) -> Path:
    from pydantic import BaseModel

    from .. import config, llm

    class Clip(BaseModel):
        src: str
        start: str
        end: str | None = None

    class Beat(BaseModel):
        say: str

    class Scene(BaseModel):
        type: str          # live | narr
        clip: Clip
        beats: list[Beat] = []
        ko: str | None = None
        end: bool = False

    class Work(BaseModel):
        name: str
        where: str
        max_ep: int = 3

    class Recap(BaseModel):
        title: str
        work: Work
        scenes: list[Scene]

    tbl = project.dir("research") / "episodes.md"
    if not tbl.exists():
        transcribe(project)
    brief = project.dir("research") / "topic_brief.json"
    system = (config.ROOT / "prompts" / "recap.md").read_text(encoding="utf-8")
    try:
        topic = project.state().get("topic", "")
    except Exception:  # noqa: BLE001  state.json 없이 만든 프로젝트
        topic = ""
    user = f"# 주제\n{topic}\n\n" + \
        (f"# topic_brief\n{brief.read_text(encoding='utf-8')}\n\n" if brief.exists() else "") + \
        f"# 에피소드\n{json.dumps(episodes_of(project), ensure_ascii=False)}\n\n" + tbl.read_text(encoding="utf-8")
    r = llm.structured(system, user, Recap, max_tokens=32000)
    spec = {"title": r.title, "work": r.work.model_dump(), "episodes": episodes_of(project), "scenes": []}
    for s in r.scenes:
        c = {"src": s.clip.src, "from": s.clip.start, **({"to": s.clip.end} if s.clip.end else {})}
        sc = {"type": s.type, "clip": c}
        if s.beats:
            sc["beats"] = [b.model_dump() for b in s.beats]
        if s.ko:
            sc["ko"] = s.ko
        if s.end:
            sc["end"] = True
        spec["scenes"].append(sc)
    out = project.dir("script") / "recap.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[recap] 초안 → {out} (사람이 장면을 영상으로 확인하고 고친 뒤 렌더)")
    return out


# ------------------------------------------------------------------ 3. 시간표·검사
def timeline(project: Project, spec: dict, durs: dict | None = None) -> list[dict]:
    """장면마다 원작 구간과 길이. durs 가 없으면 내레이션 길이를 글자 수로 어림 (초당 7자)."""
    rows = []
    for sc in spec["scenes"]:
        c = sc["clip"]
        a = _t(c["from"])
        if sc["type"] == "live":
            d = _t(c["to"]) - a if c.get("to") is not None else LIVE_MAX
            beats = []
        else:
            beats = []
            for k, b in enumerate(sc["beats"]):
                bd = (durs or {}).get(f"{sc['id']:03d}_{k}") or max(1.0, len(b["say"].replace(" ", "")) / 7.0)
                beats.append(bd)
            d = sum(beats) + PAD * len(beats)
            if c.get("to") is not None:
                d = max(d, _t(c["to"]) - a)
        rows.append({"id": sc["id"], "type": sc["type"], "src": c["src"], "a": a, "d": round(d, 3), "beats": beats})
    return rows


def check(project: Project, spec: dict | None = None, durs: dict | None = None) -> dict:
    spec = spec or _spec(project)
    rows = timeline(project, spec, durs)
    total = sum(r["d"] for r in rows) or 1.0
    live = [r for r in rows if r["type"] == "live"]
    live_sum = sum(r["d"] for r in live)
    eps = spec.get("episodes") or episodes_of(project)
    R = _rules(project)
    max_ep = min(int((spec.get("work") or {}).get("max_ep", R["max_ep"])), R["max_ep"])
    used_eps = sorted({int(eps.get(r["src"], {}).get("ep", 0)) for r in rows})
    problems = []
    for r in live:
        if r["d"] > R["live_max"] + 1e-6:
            problems.append(f"장면 {r['id']}: 원작 소리 {r['d']:.1f}초 > {R['live_max']:.0f}초")
    if live_sum / total > R["live_share"]:
        problems.append(f"원작 소리 합 {live_sum:.0f}초 = {live_sum / total:.0%} > {R['live_share']:.0%}")
    if used_eps and max(used_eps) > max_ep:
        problems.append(f"{max(used_eps)}화까지 다룸 > max_ep {max_ep} (소개형은 앞부분만, 결말 없음)")
    for r in rows:
        if r["src"] not in eps:
            problems.append(f"장면 {r['id']}: 에피소드 '{r['src']}' 가 episodes 에 없음")
        if r["type"] not in ("live", "narr"):
            problems.append(f"장면 {r['id']}: type 은 live | narr")
        if r["type"] == "narr" and not r["beats"]:
            problems.append(f"장면 {r['id']}: narr 장면에 내레이션(beats) 없음")
    last = spec["scenes"][-1] if spec["scenes"] else {}
    where = str((spec.get("work") or {}).get("where", ""))
    if not last.get("end"):
        problems.append("마지막 장면에 end: true 가 없음 (결말 앞에서 끊고 볼 수 있는 곳 안내)")
    elif where and where not in " ".join(b["say"] for b in last.get("beats", [])):
        problems.append(f"마지막 장면 내레이션에 볼 수 있는 곳('{where}')이 없음")
    qa = {"total_sec": round(total, 1), "live_sec": round(live_sum, 1), "live_share": round(live_sum / total, 3),
          "narr_share": round(1 - live_sum / total, 3), "episodes": used_eps, "scenes": len(rows),
          "estimated": durs is None, "problems": problems}
    out = project.dir("edit") / "recap_qa.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(qa, ensure_ascii=False, indent=1), encoding="utf-8")
    return qa


# ------------------------------------------------------------------ 4. 렌더
VF = (f"scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:black,"
      f"fps={FPS},format=yuv420p,setsar=1")
ENC = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]


def _seg(src: Path, a: float, d: float, out: Path, narr: Path | None) -> None:
    base = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{a:.3f}", "-t", f"{d:.3f}", "-i", str(src)]
    has_audio = bool(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index",
                                     "-of", "csv=p=0", str(src)], capture_output=True, text=True).stdout.strip())
    if narr is None:
        if has_audio:
            cmd = base + ["-vf", VF, "-af", "aresample=48000,aformat=channel_layouts=stereo", *ENC, str(out)]
        else:
            cmd = base + ["-f", "lavfi", "-t", f"{d:.3f}", "-i", "anullsrc=r=48000:cl=stereo",
                          "-vf", VF, "-map", "0:v", "-map", "1:a", *ENC, str(out)]
    else:
        bed = f"[0:a]aresample=48000,aformat=channel_layouts=stereo,volume={BED}[b];" if has_audio else \
              f"anullsrc=r=48000:cl=stereo,atrim=0:{d:.3f}[b];"
        fc = (bed + "[1:a]aresample=48000,aformat=channel_layouts=stereo,apad[n];"
              f"[b][n]amix=inputs=2:duration=first:normalize=0,atrim=0:{d:.3f}[a]")
        cmd = base + ["-i", str(narr), "-filter_complex", fc, "-vf", VF, "-map", "0:v", "-map", "[a]", *ENC, str(out)]
    subprocess.run(cmd, check=True)


def _narr_track(project: Project, sc: dict, beats: list[float], out: Path) -> Path:
    """박자 음성을 PAD 쉼으로 이어 한 파일로."""
    ins, fc = [], []
    for k, _ in enumerate(beats):
        ins += ["-i", str(project.dir("voice") / f"hb_{sc['id']:03d}_{k}.wav")]
        fc.append(f"[{k}:a]aresample=48000,aformat=channel_layouts=stereo,apad=pad_dur={PAD}[p{k}];")
    fc.append("".join(f"[p{k}]" for k in range(len(beats))) + f"concat=n={len(beats)}:v=0:a=1[a]")
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *ins, "-filter_complex", "".join(fc),
                    "-map", "[a]", str(out)], check=True)
    return out


def render(project: Project, force: bool = False) -> Path:
    spec = _spec(project)
    pre = check(project, spec)
    if pre["problems"] and not force:
        raise SystemExit("[recap] 규칙 위반 → 05_edit/recap_qa.json\n  - " + "\n  - ".join(pre["problems"]))
    narr_spec = {"scenes": [sc for sc in spec["scenes"] if sc["beats"]]}
    durs = hybrid.voice(project, narr_spec) if narr_spec["scenes"] else {}
    qa = check(project, spec, durs)
    if qa["problems"] and not force:
        raise SystemExit("[recap] 규칙 위반 (실제 내레이션 길이 기준) → 05_edit/recap_qa.json\n  - " + "\n  - ".join(qa["problems"]))
    rows = timeline(project, spec, durs)
    eps = spec.get("episodes") or episodes_of(project)
    work = project.dir("edit") / "recap_work"
    work.mkdir(parents=True, exist_ok=True)
    segs, srt, t, n = [], [], 0.0, 1
    for sc, r in zip(spec["scenes"], rows):
        src = project.dir("assets") / eps[r["src"]]["file"]
        out = work / f"s{sc['id']:03d}.mp4"
        narr = _narr_track(project, sc, r["beats"], work / f"n{sc['id']:03d}.wav") if r["type"] == "narr" else None
        _seg(src, r["a"], r["d"], out, narr)
        segs.append(out)
        # 자막: 내레이션은 박자를 짧은 줄로 나눠 글자 수 비율로, 원작 소리는 번역 한 줄
        if r["type"] == "narr":
            bt = t
            for b, bd in zip(sc["beats"], r["beats"]):
                parts = chunk_text(b["say"], 24)
                while len(parts) > 1 and len(parts[-1]) <= 6:      # '섭니다.' 같은 짧은 꼬리는 앞 줄에 붙임
                    parts[-2:] = [parts[-2] + " " + parts[-1]]
                tot = sum(len(p) for p in parts) or 1
                for j, p in enumerate(parts):
                    pd = bd * len(p) / tot
                    hold = PAD if j == len(parts) - 1 else 0.0      # 박자 사이 쉼에도 자막을 남김
                    srt.append(f"{n}\n{_ts_srt(bt)} --> {_ts_srt(bt + pd + hold)}\n{p}\n")
                    n += 1
                    bt += pd
                bt += PAD
        elif sc.get("ko"):
            srt.append(f"{n}\n{_ts_srt(t)} --> {_ts_srt(t + r['d'])}\n{sc['ko']}\n")
            n += 1
        t += _dur(out)
    lst = work / "list.txt"
    lst.write_text("".join(f"file '{p.name}'\n" for p in segs), encoding="utf-8")
    edir = project.dir("edit")
    joined = work / "joined.mp4"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
                    "-c", "copy", str(joined)], check=True)
    subs = edir / "subs.srt"
    subs.write_text("\n".join(srt), encoding="utf-8")
    final = edir / "final.mp4"
    from .paper import FONT_DIR as font_dir
    style = "FontName=NanumGothic ExtraBold,FontSize=22,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=3,Shadow=0,MarginV=40"
    sub_f = f"subtitles={subs.as_posix()}:force_style='{style}'" + (f":fontsdir={font_dir.as_posix()}" if font_dir.exists() else "")
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(joined), "-vf", sub_f,
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-c:a", "copy", str(final)], check=True)
    print(f"[recap] {final} · {qa['total_sec']:.0f}초 · 원작 소리 {qa['live_share']:.0%} · {qa['episodes']}화")
    return final


def main(project: Project, mode: str = "render", force: bool = False) -> None:
    if mode == "transcribe":
        transcribe(project)
    elif mode == "plan":
        plan(project)
    elif mode == "check":
        qa = check(project)
        print(json.dumps(qa, ensure_ascii=False, indent=1))
        if qa["problems"]:
            raise SystemExit(1)
    else:
        render(project, force)
