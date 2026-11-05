"""5~8단계: 음성 → 자막 → 소스(화면) 체크 → 1차 가편집 영상 조립 (ffmpeg).

결과물은 '완성본'이 아니라 편집자가 바로 손볼 수 있는 가편집(draft)이다.
  05_edit/draft.mp4      출처 라벨·2단 자막(원문+번역)·카드가 들어간 1차 영상
  05_edit/subs.srt       유튜브 업로드용 자막
  05_edit/subs.ass       강조색이 들어간 번인 자막 (프리미어/캡컷에서도 열림)
  05_edit/timeline.csv   씬별 시작/길이/소스 파일 → NLE 에서 그대로 따라 배치
"""
from __future__ import annotations

import csv
import json
import re
import shutil
import subprocess
from pathlib import Path

from .. import config
from ..project import Project

VISUAL_EXT = (".mp4", ".mov", ".png", ".jpg", ".jpeg", ".webp")


def _ff(args: list[str]) -> None:
    proc = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *args], capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr[-3000:])


def duration(path: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True).stdout.strip()
    return float(out or 0)


# ---------------------------------------------------------------- 5. 음성
def voice(project: Project) -> None:
    cfg = config.load("pipeline").get("tts", {})
    scenes = project.read_json("script", "scenes.json")["scenes"]
    vdir = project.dir("voice")
    durs = {}
    for s in scenes:
        sid = f"scene_{s['id']:03d}"
        if s.get("kind") == "quote":
            # 원본 발언 장면: 내레이션 없이 클립의 원래 소리를 쓴다
            durs[s["id"]] = _quote_audio(project, s, vdir / "clean" / f"{sid}.wav")
            print(f"[voice] {sid} {durs[s['id']]}s (원본 발언)")
            continue
        raw = next((p for p in vdir.glob(f"{sid}.*") if p.suffix in (".wav", ".mp3", ".m4a")), None)
        if raw is None:
            if cfg.get("backend") == "placeholder":
                # 가녹음 없이 흐름만 보는 애니매틱: 글자 수 ÷ 목표 말속도로 길이를 정한 무음
                cpm = (config.style_profile().get("targets") or {}).get("chars_per_minute") or 260
                secs = max(1.5, len(s["narration"].replace(" ", "")) / cpm * 60)
                clean = vdir / "clean" / f"{sid}.wav"
                clean.parent.mkdir(exist_ok=True)
                _ff(["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", f"{secs:.2f}", str(clean)])
                durs[s["id"]] = round(secs, 3)
                print(f"[voice] {sid} {durs[s['id']]}s (placeholder 무음)")
                continue
            if cfg.get("backend") == "edge":
                raw = vdir / f"{sid}.mp3"
                subprocess.run([shutil.which("edge-tts") or "edge-tts", "--voice", cfg.get("voice", "ko-KR-InJoonNeural"),
                                f"--rate={cfg.get('rate', '+0%')}", "--text", s["narration"], "--write-media", str(raw)],
                               check=True)
            else:
                raise SystemExit(f"녹음 파일이 없습니다: {vdir}/{sid}.wav (tts.backend: manual)")
        clean = vdir / "clean" / f"{sid}.wav"
        clean.parent.mkdir(exist_ok=True)
        # 앞뒤 무음 제거 + 음량 정규화 → '숨 쉴 틈 없는' 지식 채널 리듬
        _ff(["-i", str(raw), "-af",
             "silenceremove=start_periods=1:start_threshold=-45dB,areverse,"
             "silenceremove=start_periods=1:start_threshold=-45dB,areverse,loudnorm=I=-16:TP=-1.5",
             "-ar", "48000", "-ac", "2", str(clean)])
        durs[s["id"]] = round(duration(clean), 3)
        print(f"[voice] {sid} {durs[s['id']]}s")
    project.write_json("voice", "durations.json", durs)
    project.mark_done("voice")


def _quote_audio(project: Project, s: dict, out: Path) -> float:
    from .clips import to_sec

    out.parent.mkdir(exist_ok=True)
    clip = project.dir("assets") / f"scene_{s['id']:03d}.mp4"
    if clip.exists():
        _ff(["-i", str(clip), "-vn", "-af", "loudnorm=I=-16:TP=-1.5", "-ar", "48000", "-ac", "2", str(out)])
        return round(duration(out), 3)
    src = s.get("source") or {}
    st, en = to_sec(src.get("start")), to_sec(src.get("end"))
    secs = (en - st) if (st is not None and en is not None and en > st) else float(src.get("length", 8))
    _ff(["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", f"{secs:.2f}", str(out)])
    return round(secs, 3)


# ---------------------------------------------------------------- 6. 자막
def chunk_text(text: str, max_chars: int = 20) -> list[str]:
    """한 줄 max_chars 이내로 어절 단위 분할 (지식 채널식 짧은 자막)."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > max_chars:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
        if re.search(r"[.?!]$", cur):
            lines.append(cur)
            cur = ""
    if cur:
        lines.append(cur)
    return lines


def _ts_srt(t: float) -> str:
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def _ts_ass(t: float) -> str:
    cs = int(round(t * 100))
    return f"{cs // 360000}:{cs // 6000 % 60:02d}:{cs // 100 % 60:02d}.{cs % 100:02d}"


GAP = 0.12  # 씬 사이 호흡


def subtitles(project: Project) -> None:
    ecfg = config.load("pipeline").get("edit", {})
    scenes = project.read_json("script", "scenes.json")["scenes"]
    durs = {int(k): v for k, v in project.read_json("voice", "durations.json").items()}
    W, H = ecfg.get("width", 1920), ecfg.get("height", 1080)
    font, size = ecfg.get("font", "Noto Sans CJK KR"), ecfg.get("subtitle_size", 50)
    emph = ecfg.get("emphasis_color", "&H002C40E8")
    logo = ecfg.get("logo_text", "")

    srt, ass_events, timeline, chapters = [], [], [], []
    t, n, last_section = 0.0, 1, None
    for s in scenes:
        d = durs[s["id"]]
        base = s["section"]
        if base != last_section:
            chapters.append({"t": round(t, 2), "label": s["section"]})
            last_section = base
        lines = chunk_text(s["narration"], ecfg.get("subtitle_chars", 28))
        total = sum(len(x) for x in lines) or 1
        en_lines = chunk_text(s["quote_en"], 60) if s.get("kind") == "quote" and s.get("quote_en") else []
        if en_lines:
            # 원문은 한국어 줄 수에 맞춰 같은 비율로 나눠 위에 작게 띄운다
            per = max(1, round(len(en_lines) / max(len(lines), 1)))
            groups = [" ".join(en_lines[i * per:(i + 1) * per]) for i in range(len(lines))]
            groups[-1] = " ".join(en_lines[(len(lines) - 1) * per:]) or groups[-1]
        if s.get("label"):
            ass_events.append(f"Dialogue: 2,{_ts_ass(t)},{_ts_ass(t + d + GAP)},Label,,0,0,0,,{s['label']}")
        lt = t
        for li, ln in enumerate(lines):
            ld = d * len(ln) / total
            if en_lines and groups[li]:
                ass_events.append(f"Dialogue: 0,{_ts_ass(lt)},{_ts_ass(lt + ld)},En,,0,0,0,,{groups[li]}")
            srt.append(f"{n}\n{_ts_srt(lt)} --> {_ts_srt(lt + ld)}\n{ln}\n")
            styled = ln
            for w in sorted(s.get("emphasis", []), key=len, reverse=True):
                if w and w in styled:
                    styled = styled.replace(w, f"{{\\c{emph}}}{w}{{\\c&H00FFFFFF}}", 1)
            ass_events.append(f"Dialogue: 0,{_ts_ass(lt)},{_ts_ass(lt + ld)},Sub,,0,0,0,,{styled}")
            lt += ld
            n += 1
        timeline.append({"scene": s["id"], "start": round(t, 3), "duration": round(d + GAP, 3),
                         "section": s["section"], "visual_type": s["visual_type"], "visual_brief": s["visual_brief"],
                         "sfx": s.get("sfx", "")})
        t += d + GAP

    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,{font},{size},&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,2.5,0,2,80,80,60,1
Style: En,{font},{int(size * 0.62)},&H00B4B4B4,&H00B4B4B4,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,1.8,0,2,80,80,{60 + int(size * 1.25)},1
Style: Label,{font},{int(size * 0.52)},&H00E6E6E6,&H00E6E6E6,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,1.5,0,7,40,40,30,1
Style: Logo,{font},{int(size * 0.56)},&H00DCDCDC,&H00DCDCDC,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,1.5,0,9,40,40,30,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    if logo:
        ass_events.append(f"Dialogue: 3,{_ts_ass(0)},{_ts_ass(t)},Logo,,0,0,0,,{logo}")
    edir = project.dir("edit")
    (edir / "subs.srt").write_text("\n".join(srt), encoding="utf-8")
    (edir / "subs.ass").write_text(header + "\n".join(ass_events) + "\n", encoding="utf-8")
    project.write_json("edit", "chapters.json", chapters)
    project.write_json("edit", "timeline.json", timeline)
    print(f"[subtitles] {n - 1}줄, 총 {t:.1f}s → {edir}/subs.srt, subs.ass")
    project.mark_done("subtitles")


# ---------------------------------------------------------------- 7. 화면 소스
def find_visual(project: Project, sid: int) -> Path | None:
    """scene_007.png 처럼 직접 넣은 파일을 _auto 임시 카드보다 우선한다."""
    found = [p for p in sorted(project.dir("assets").glob(f"scene_{sid:03d}*")) if p.suffix.lower() in VISUAL_EXT]
    found.sort(key=lambda p: (p.stem.endswith("_auto"), p.stem.endswith("_card")))
    return found[0] if found else None


def assets(project: Project, auto_cards: bool = True) -> None:
    """샷리스트 작성 + 카드 렌더링.
    - scene["card"] 가 있으면 검은 배경 인포 카드(scene_XXX_card.png)를 매번 새로 그린다
    - 직접 넣은 파일(scene_XXX.png/.mp4)이 있으면 그것이 우선
    - 그래도 없으면 '[소스 필요]' 자리표시(scene_XXX_auto.png)"""
    from . import cards

    scenes = project.read_json("script", "scenes.json")["scenes"]
    adir = project.dir("assets")
    for s in scenes:
        for old in adir.glob(f"scene_{s['id']:03d}_auto.png"):
            old.unlink()
        if s.get("card"):
            cards.render(s["card"], adir / f"scene_{s['id']:03d}_card.png")
        elif auto_cards and find_visual(project, s["id"]) is None:
            cards.placeholder(adir / f"scene_{s['id']:03d}_auto.png", f"{s['visual_type']} · {s['visual_brief']}")
    f = project.dir("assets") / "shotlist.csv"
    missing = 0
    with open(f, "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(["scene", "file", "status", "visual_type", "label", "visual_brief", "image_prompt", "source_url"])
        for s in scenes:
            p = find_visual(project, s["id"])
            auto = p is not None and "_auto" in p.stem
            missing += p is None or auto
            status = "AUTO(임시카드)" if auto else "OK" if p else "MISSING"
            w.writerow([s["id"], p.name if p else f"scene_{s['id']:03d}.png", status,
                        s["visual_type"], s.get("label", ""), s["visual_brief"], s.get("image_prompt", ""),
                        (s.get("source") or {}).get("url", "")])
    print(f"[assets] 샷리스트 → {f}\n         실제 소스가 필요한 씬 {missing}개 (임시 카드/단색으로 대체됨)")
    project.mark_done("assets")


# ---------------------------------------------------------------- 8. 가편집 조립
def assemble(project: Project) -> None:
    ecfg = config.load("pipeline").get("edit", {})
    W, H, fps = ecfg.get("width", 1920), ecfg.get("height", 1080), ecfg.get("fps", 30)
    timeline = project.read_json("edit", "timeline.json")
    edir = project.dir("edit")
    work = edir / "work"
    work.mkdir(exist_ok=True)
    fit = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,fps={fps}"

    clips, audios = [], []
    for row in timeline:
        sid, d = row["scene"], row["duration"]
        out = work / f"v_{sid:03d}.mp4"
        src = find_visual(project, sid)
        if src is None:
            _ff(["-f", "lavfi", "-i", f"color=c=black:s={W}x{H}:r={fps}:d={d}",
                 "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out)])
        elif src.suffix.lower() in (".mp4", ".mov"):
            _ff(["-stream_loop", "-1", "-i", str(src), "-t", str(d), "-an", "-vf", fit,
                 "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out)])
        else:
            frames = max(int(d * fps), 1)
            vf = (f"scale={W * 2}:{H * 2}:force_original_aspect_ratio=increase,crop={W * 2}:{H * 2},"
                  f"zoompan=z='min(1+0.0008*on,1.15)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
                  f":d={frames}:s={W}x{H}:fps={fps},setsar=1")
            # 차트·카드는 가장자리가 잘리면 안 되므로 줌은 사진류에만
            if not (ecfg.get("kenburns", False) and row.get("visual_type") in ("ai_image", "stock", "screenshot", "meme")):
                vf = fit
            _ff(["-loop", "1", "-i", str(src), "-t", str(d), "-vf", vf,
                 "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out)])
        clips.append(out)
        a = work / f"a_{sid:03d}.wav"
        _ff(["-i", str(project.dir("voice") / "clean" / f"scene_{sid:03d}.wav"), "-af", "apad",
             "-t", str(d), "-ar", "48000", "-ac", "2", str(a)])
        audios.append(a)

    for name, items in (("video.txt", clips), ("audio.txt", audios)):
        (work / name).write_text("".join(f"file '{p.resolve()}'\n" for p in items), encoding="utf-8")
    _ff(["-f", "concat", "-safe", "0", "-i", str(work / "video.txt"), "-c", "copy", str(work / "video.mp4")])
    _ff(["-f", "concat", "-safe", "0", "-i", str(work / "audio.txt"), "-c", "copy", str(work / "voice.wav")])

    ass = str((edir / "subs.ass").resolve()).replace("\\", "/").replace(":", "\\:")
    args = ["-i", str(work / "video.mp4"), "-i", str(work / "voice.wav")]
    bgm = ecfg.get("bgm")
    if bgm and Path(bgm).exists():
        args += ["-stream_loop", "-1", "-i", bgm]
        # 내레이션이 나올 때 BGM 을 자동으로 눌러 주는 사이드체인 더킹
        fc = (f"[0:v]ass='{ass}'[v];[1:a]asplit=2[n1][n2];[2:a]volume={ecfg.get('bgm_volume', 0.1)}[b];"
              f"[b][n1]sidechaincompress=threshold=0.05:ratio=8[bd];"
              f"[n2][bd]amix=inputs=2:duration=first:normalize=0[a]")
    else:
        fc = f"[0:v]ass='{ass}'[v];[1:a]anull[a]"
    _ff([*args, "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
         "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-c:a", "aac", "-b:a", "192k",
         "-shortest", str(edir / "draft.mp4")])

    with open(edir / "timeline.csv", "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=list(timeline[0].keys()) + ["source"])
        w.writeheader()
        for row in timeline:
            src = find_visual(project, row["scene"])
            w.writerow({**row, "source": src.name if src else "(없음)"})
    print(f"[assemble] {edir}/draft.mp4 ({duration(edir / 'draft.mp4'):.1f}s)\n"
          f"           확인 후: ytflow approve {project.path.name} draft")
    project.mark_done("assemble")
