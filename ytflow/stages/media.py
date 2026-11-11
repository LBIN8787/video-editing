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
import os
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
                cmd = [shutil.which("edge-tts") or "edge-tts", "--voice", cfg.get("voice", "ko-KR-InJoonNeural"),
                       f"--rate={cfg.get('rate', '+0%')}", "--text", s["narration"], "--write-media", str(raw)]
                proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
                if proxy:  # edge-tts 는 프록시 환경변수를 자동으로 읽지 않는다
                    cmd[1:1] = ["--proxy", proxy]
                subprocess.run(cmd, check=True)
            elif cfg.get("backend") == "elevenlabs":
                raw = _elevenlabs(s["narration"], vdir / f"{sid}.mp3", cfg.get("elevenlabs") or {})
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


def _elevenlabs(text: str, out: Path, ec: dict) -> Path:
    """ElevenLabs TTS (with-timestamps). 같은 문장·목소리·설정이면 캐시를 써서 크레딧을 다시 쓰지 않는다.
    키: 환경변수 ELEVENLABS_API_KEY, 또는 클라우드 환경의 네트워크 비밀값(api.elevenlabs.io, 헤더 xi-api-key).
    결과: <장면>.mp3 + <장면>.align.json (글자별 시작·끝 초 — 단어 단위 자막에 씀)."""
    import base64
    import hashlib
    import urllib.request
    vid = ec.get("voice_id") or ""
    if not vid:
        raise SystemExit("tts.elevenlabs.voice_id 가 비어 있습니다. 목소리를 정한 뒤 config/pipeline.yaml 또는 channels/<id>/channel.yaml 의 tts 에 적으세요 (docs/08-voice.md)")
    body = {"text": text, "model_id": ec.get("model_id", "eleven_multilingual_v2"),
            "voice_settings": {k: ec[k] for k in ("stability", "similarity_boost", "style", "speed", "use_speaker_boost") if k in ec}}
    if ec.get("language_code"):
        body["language_code"] = ec["language_code"]
    key = hashlib.sha1(json.dumps([vid, body], ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:16]
    cache = config.CACHE_DIR / "elevenlabs" / f"{key}.json"
    if cache.exists():
        data = json.loads(cache.read_text(encoding="utf-8"))
    else:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{vid}/with-timestamps?output_format={ec.get('output_format', 'mp3_44100_128')}"
        req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST", headers={
            "Content-Type": "application/json", "xi-api-key": os.environ.get("ELEVENLABS_API_KEY", "proxy-injected")})
        with urllib.request.urlopen(req, timeout=120) as r:
            data = json.loads(r.read())
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_text(json.dumps(data), encoding="utf-8")
    out.write_bytes(base64.b64decode(data["audio_base64"]))
    if data.get("alignment"):
        out.with_suffix(".align.json").write_text(json.dumps(data["alignment"], ensure_ascii=False), encoding="utf-8")
    return out


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
    paper = ecfg.get("style") in ("paper", "flat")
    top = ecfg.get("subtitle_position") == "top"          # 머니크루식: 화면 위쪽 어두운 글씨
    sub_color = "&H003A2E26" if ecfg.get("subtitle_dark") else "&H00FFFFFF"
    box = 3 if ecfg.get("subtitle_box") else 1           # 3 = 글자 뒤 상자
    back = "&H50101010" if box == 3 else "&H80000000"
    lab_align = 3 if ecfg.get("label_position") == "bottom_right" else 7

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
            vis = find_visual(project, s["id"])
            footage = vis is not None and vis.suffix == ".mp4" and not any(vis.stem.endswith(k) for k in ("_anim", "_auto"))
            tag = "{\\c&H00505A66&\\bord0}" if paper and not footage else ""  # 종이 위에서는 진회색 글씨
            pasted = paper and vis is not None and vis.stem.endswith("_anim") and not s.get("card")
            if not pasted:  # 종이 콜라주는 사진 아래 손글씨 캡션이 출처를 대신한다
                ass_events.append(f"Dialogue: 2,{_ts_ass(t)},{_ts_ass(t + d + GAP)},Label,,0,0,0,,{tag}{s['label']}")
        lt = t
        for li, ln in enumerate(lines):
            ld = d * len(ln) / total
            if en_lines and groups[li]:
                ass_events.append(f"Dialogue: 0,{_ts_ass(lt)},{_ts_ass(lt + ld)},En,,0,0,0,,{groups[li]}")
            srt.append(f"{n}\n{_ts_srt(lt)} --> {_ts_srt(lt + ld)}\n{ln}\n")
            styled = ln
            for w in sorted(s.get("emphasis", []), key=len, reverse=True):
                if w and w in styled:
                    styled = styled.replace(w, f"{{\\c{emph}}}{w}{{\\c{sub_color}}}", 1)  # 강조 뒤 원래 자막색으로
            if box == 3:
                # 상자 자막: 상자(색 바뀜 없이 한 덩어리)와 글자(강조색)를 두 겹으로 → 강조 단어에서 상자가 끊기지 않음
                ass_events.append(f"Dialogue: 0,{_ts_ass(lt)},{_ts_ass(lt + ld)},SubBox,,0,0,0,,{ln}")
                ass_events.append(f"Dialogue: 1,{_ts_ass(lt)},{_ts_ass(lt + ld)},SubText,,0,0,0,,{styled}")
            else:
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
Style: Sub,{font},{size},{sub_color},{sub_color},{back if box == 3 else "&H00000000"},{back},{-1 if top else 0},0,0,0,100,100,0,0,{box},{ecfg.get("subtitle_outline", 12 if box == 3 else (0 if ecfg.get("subtitle_dark") else 2.5))},0,{8 if top else 2},80,80,{ecfg.get("subtitle_margin_v", 30 if top else (50 if box == 3 else 60))},1
Style: SubBox,{font},{size},&HFF000000,&HFF000000,{back},{back},0,0,0,0,100,100,0,0,3,{ecfg.get("subtitle_outline", 12)},0,2,80,80,{ecfg.get("subtitle_margin_v", 50)},1
Style: SubText,{font},{size},{sub_color},{sub_color},&HFF000000,&HFF000000,0,0,0,0,100,100,0,0,1,0,0,2,80,80,{ecfg.get("subtitle_margin_v", 50)},1
Style: En,{font},{int(size * 0.62)},&H00D2D2D2,&H00D2D2D2,{back if box == 3 else "&H00000000"},{back},0,0,0,0,100,100,0,0,{box},{8 if box == 3 else 1.8},0,2,80,80,{(50 if box == 3 else 60) + int(size * (1.6 if box == 3 else 1.25))},1
Style: Label,{font},{int(size * 0.52)},&H00E6E6E6,&H00E6E6E6,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,1.5,0,{lab_align},40,40,30,1
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
    # 우선순위: 직접 넣은 파일 > 받은 클립 > 카드/애니메이션 > 기사 캡처 > 임시 썸네일 > 자리표시
    rank = {"_anim": 2, "_card": 2, "_shot": 3, "_temp": 4, "_auto": 5}
    found.sort(key=lambda p: (next((v for k, v in rank.items() if p.stem.endswith(k)), 1 if p.suffix == ".mp4" else 0), p.suffix != ".mp4"))
    return found[0] if found else None


def _headline_fallback(project: Project, s: dict) -> dict | None:
    url = (s.get("source") or {}).get("url", "")
    f = project.dir("research") / "articles.json"
    arts = json.loads(f.read_text(encoding="utf-8")) if f.exists() else []
    a = next((x for x in arts if x.get("url") == url), None)
    if not a:
        return None
    title = a.get("title", "")
    host = url.split("/")[2] if "//" in url else ""
    if len(title) < 18 or title.split("(")[0].strip().lower() in (a.get("publisher", "").lower(), host.lower()):
        title = f"\u201c{s['narration'][:58]}\u201d"  # 기사 제목을 모르면 그 기사로 뒷받침한 문장을 인용 카드로
    return {"type": "headline", "title": title[:60],
            "items": [{"label": f"{a.get('publisher', '')} · {a.get('date', '')}", "value": "", "sub": "", "highlight": False}],
            "note": url.split("/")[2] if "//" in url else ""}


def assets(project: Project, auto_cards: bool = True) -> None:
    """샷리스트 작성 + 장면 화면 만들기. 스타일(edit.style)에 따라:
    sixsigma: 카드 → 검은 배경 PNG, 기사 캡처 → 검은 화면 위 캡처, 없으면 '[소스 필요]' PNG
    paper:    카드 → 손그림 애니메이션 MP4, 캡처/임시화면 → 종이 위 콜라주 애니메이션, 없으면 자리표시 애니메이션
    직접 넣은 파일(scene_XXX.png/.mp4)과 받은 클립이 있으면 항상 그것이 우선."""
    from . import cards

    style = config.load("pipeline").get("edit", {}).get("style", "sixsigma")
    if style == "shorts":  # 세로 쇼츠는 전용 화면 구성 (ytflow/stages/shorts.py)
        from .shorts import assets as shorts_assets
        return shorts_assets(project)
    scenes = project.read_json("script", "scenes.json")["scenes"]
    adir = project.dir("assets")
    dfile = project.dir("voice") / "durations.json"
    durs = {int(k): v for k, v in json.loads(dfile.read_text()).items()} if dfile.exists() else {}
    from . import marketdata, hyper
    qa = {}
    engine = config.load("pipeline").get("edit", {}).get("card_engine", "pil")  # pil(paper.py) | hyperframes(hyper.py)
    hf_jobs = []
    for s in scenes:
        sid = s["id"]
        card = s.get("card")
        if card and card.get("ticker"):  # 실제 시세 차트: 데이터 받아 카드에 넣기 (01_research/prices 캐시)
            pdir = project.dir("research") / "prices"
            card = dict(card, type="chart", _series=marketdata.fetch(card["ticker"], card.get("period") or "6mo", pdir,
                                                                    card.get("start") or "", card.get("end") or ""),
                        _currency=marketdata.currency(card["ticker"], pdir))
        for old in list(adir.glob(f"scene_{sid:03d}_auto.*")) + list(adir.glob(f"scene_{sid:03d}_anim.mp4")) \
                + list(adir.glob(f"scene_{sid:03d}_card.png")):
            old.unlink()
        own = find_visual(project, sid)  # 직접 넣은 파일·받은 클립만 남은 상태
        own = own if own is not None and not any(own.stem.endswith(k) for k in ("_shot", "_temp")) else None
        pasted = next((p for k in ("_shot", "_temp") for p in adir.glob(f"scene_{sid:03d}{k}.*")), None)
        d = durs.get(sid, 5.0) + GAP
        brief = f"{s['visual_type']} · {s['visual_brief']}"
        if not card and own is None and pasted is None and s["visual_type"] == "screenshot":
            card = _headline_fallback(project, s)  # 캡처 실패 → 기사 제목·매체·날짜로 헤드라인 카드
        if style == "sixsigma" and card:  # 식스시그마 카드도 같은 엔진(검은 배경 프로필)으로 → 겹침 방지·차트·아이콘
            from . import flat as flat_mod
            flat_mod.CURRENT["name"] = "dark"
            qa[sid] = flat_mod.render_card(card, adir / f"scene_{sid:03d}_anim.mp4", d, seed=sid)
            flat_mod.CURRENT["name"] = "flat"
            print(f"[assets] #{sid} sixsigma card")
            continue
        if style in ("paper", "flat"):  # 둘 다 애니메이션 MP4 렌더러 (같은 인터페이스)
            from . import flat as flat_mod
            from . import paper as paper_mod
            paper = flat_mod if style == "flat" else paper_mod
            out = adir / f"scene_{sid:03d}_anim.mp4"
            if card and style == "paper" and engine == "hyperframes" and hyper.available() and card.get("type") in hyper.SUPPORTED:
                hf_jobs.append((sid, card, out, d))  # HTML+GSAP 렌더는 느려서 모아서 병렬로
            elif card:
                qa[sid] = paper.render_card(card, out, d, seed=sid)
            elif own is None and pasted is not None:
                paper.render_paste(pasted, out, d, caption=s.get("label", ""), seed=sid)
            elif own is None and auto_cards:
                paper.render_placeholder(adir / f"scene_{sid:03d}_auto.mp4", d, brief, seed=sid)
            print(f"[assets] #{sid} {style} {'card' if s.get('card') else 'paste' if pasted is not None and own is None else 'own' if own else 'placeholder'}")
        else:
            if s.get("card"):
                cards.render(s["card"], adir / f"scene_{sid:03d}_card.png")
            elif own is None and pasted is not None and pasted.stem.endswith("_shot"):
                cards.shot_on_black(pasted, adir / f"scene_{sid:03d}_card.png")
            elif own is None and pasted is None and auto_cards:
                cards.placeholder(adir / f"scene_{sid:03d}_auto.png", brief)
    if hf_jobs:  # HyperFrames 카드: 3개씩 병렬 렌더 (실패하면 hyper.py 가 paper.py 로 대체)
        from concurrent.futures import ThreadPoolExecutor
        print(f"[assets] HyperFrames 카드 {len(hf_jobs)}개 렌더 (병렬 {config.load('pipeline').get('edit', {}).get('hf_workers', 3)})")
        with ThreadPoolExecutor(config.load("pipeline").get("edit", {}).get("hf_workers", 3)) as ex:
            futs = {sid: ex.submit(hyper.render_card, card, out, d, sid, adir / "hf" / f"scene_{sid:03d}")
                    for sid, card, out, d in hf_jobs}
            for sid, fu in futs.items():
                qa[sid] = fu.result()
                print(f"[assets] #{sid} hyperframes card")
    project.write_json("assets", "layout_qa.json", {str(k): v for k, v in qa.items() if v})
    if any(qa.values()):
        print(f"[assets] ⚠ 겹침을 자동으로 못 푼 장면 {sum(1 for v in qa.values() if v)}개 → 04_assets/layout_qa.json")
    f = project.dir("assets") / "shotlist.csv"
    missing = 0
    with open(f, "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(["scene", "file", "status", "visual_type", "label", "visual_brief", "image_prompt", "source_url"])
        for s in scenes:
            p = find_visual(project, s["id"])
            temp = next(project.dir("assets").glob(f"scene_{s['id']:03d}_temp.*"), None)
            auto = p is not None and p.stem.endswith("_auto")
            real = p is not None and not auto and not p.stem.endswith("_temp") and \
                not (temp is not None and p.stem.endswith("_anim") and not s.get("card"))
            missing += not real
            status = "OK" if real else "TEMP(임시 썸네일 · 클립 교체 필요)" if temp is not None else "MISSING(자리표시)"
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

    # 화면 움직임: 생성한 장면은 천천히 다가가고(push_in), 모든 장면은 배경색에서 부드럽게 나타난다(fade_in)
    push = float(ecfg.get("push_in", 0.0))
    fade = float(ecfg.get("fade_in", 0.0))
    bgc = "0x" + str((ecfg.get("paper") or {}).get("base", "#000000")).lstrip("#") if ecfg.get("style") != "sixsigma" else "black"

    def polish(d: float, generated: bool) -> str:
        f = ""
        if generated and push > 0:
            f += f",scale=w='{W}*(1+{push}*t/{d:.3f})':h=-2:eval=frame:flags=bicubic,crop={W}:{H}"
        if fade > 0:
            f += f",fade=t=in:st=0:d={fade}:color={bgc}"
        return f

    clips, audios = [], []
    for row in timeline:
        sid, d = row["scene"], row["duration"]
        out = work / f"v_{sid:03d}.mp4"
        src = find_visual(project, sid)
        gen = src is not None and any(src.stem.endswith(k) for k in ("_anim", "_card", "_shot", "_temp", "_auto"))
        if src is None:
            _ff(["-f", "lavfi", "-i", f"color=c=black:s={W}x{H}:r={fps}:d={d}",
                 "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out)])
        elif src.suffix.lower() in (".mp4", ".mov"):
            _ff(["-stream_loop", "-1", "-i", str(src), "-t", str(d), "-an", "-vf", fit + polish(d, gen),
                 "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out)])
        else:
            frames = max(int(d * fps), 1)
            vf = (f"scale={W * 2}:{H * 2}:force_original_aspect_ratio=increase,crop={W * 2}:{H * 2},"
                  f"zoompan=z='min(1+0.0008*on,1.15)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
                  f":d={frames}:s={W}x{H}:fps={fps},setsar=1")
            # 차트·카드는 가장자리가 잘리면 안 되므로 줌은 사진류에만
            if not (ecfg.get("kenburns", False) and row.get("visual_type") in ("ai_image", "stock", "screenshot", "meme")):
                vf = fit
            _ff(["-loop", "1", "-i", str(src), "-t", str(d), "-vf", vf + polish(d, gen),
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
    fdir = str((Path(__file__).resolve().parent.parent / "assets" / "fonts")).replace("\\", "/").replace(":", "\\:")
    args = ["-i", str(work / "video.mp4"), "-i", str(work / "voice.wav")]
    bgm = ecfg.get("bgm")
    if bgm and Path(bgm).exists():
        args += ["-stream_loop", "-1", "-i", bgm]
        # 내레이션이 나올 때 BGM 을 자동으로 눌러 주는 사이드체인 더킹
        fc = (f"[0:v]ass='{ass}':fontsdir='{fdir}'[v];[1:a]asplit=2[n1][n2];[2:a]volume={ecfg.get('bgm_volume', 0.1)}[b];"
              f"[b][n1]sidechaincompress=threshold=0.05:ratio=8[bd];"
              f"[n2][bd]amix=inputs=2:duration=first:normalize=0[a]")
    else:
        fc = f"[0:v]ass='{ass}':fontsdir='{fdir}'[v];[1:a]anull[a]"
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
    from .finish import master
    master(project)  # 유튜브 음량 -14 LUFS·규격 점검·프레임 시트 (ffmpeg-skill) → final.mp4
    project.mark_done("assemble")
