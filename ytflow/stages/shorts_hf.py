"""세로 쇼츠 (Claude 판, 2026-11-09) — HyperFrames 한 장(1080×1920)으로 쇼츠 전체를 그린다.

    python -m ytflow short <프로젝트>      # 02_script/short.json → 05_edit/final.mp4 (+ subs.ass, sync-qa)

비교 기준: Codex 'AI 실전노트' 쇼츠 (Drive 'AI 실전노트 — 쇼츠 자동화 보관', shorts-ai-guide 1.0.0).
같이 지키는 것: 위치가 고정된 배치(머리말·두 줄 제목·가운데 화면·자막 상자·출처), 차분한 움직임, 효과음·배경음 없음, -16 LUFS,
강조는 영상 하나에 한 색(제목 속 한 단어)만. 다른 점: 가운데는 그림(모형) 대신 **직접 실행·녹화한 실제 화면**이 주인공.

short.json:
{"brand": "AI 더 잘 쓰기", "skin": {...선택}, "footage": {키: {file, credit, url}},
 "scenes": [{"kicker": "1 · 무엇", "title": ["AI가 만든 티,", "이렇게 지웁니다"], "hl": "티,",
             "media": {"src": "morph", "start": 0, "pos": "50% 30%", "zoom": 1.0}, "source": "출처 한 줄",
             "beats": [{"say": "..."}]}]}
"""
from __future__ import annotations

import html as H
import json
import math
import os
import shutil
import subprocess
from pathlib import Path

from ..project import Project
from . import hybrid, hyper, paper

W, H_ = 1080, 1920
FPS = 30
GAP, LEAD, TAIL = 0.28, 0.25, 0.45
PANEL = (40, 430, 1000, 930)   # x, y, w, h — 가운데 실제 화면
SKIN = {"bg": "#F4F1EA", "ink": "#171614", "muted": "#7D776D", "accent": "#E8622C", "panel": "#FFFFFF",
        "sub_bg": "#171614", "sub_fg": "#F6F2EA"}


def _e(s) -> str:
    return H.escape(str(s))


def _dur(p: Path) -> float:
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True).stdout or 0)


def plan(spec: dict, durs: dict) -> list:
    """장면마다 [시작, 길이, 박자들(시작, 길이)] — 박자 사이 짧은 쉼."""
    out, t = [], 0.0
    for sc in spec["scenes"]:
        bt, x = [], LEAD
        for k, _ in enumerate(sc["beats"]):
            d = durs[f"{sc['id']:03d}_{k}"]
            bt.append((x, d))
            x += d + GAP
        dur = math.ceil((x - GAP + TAIL) * FPS) / FPS
        out.append((t, dur, bt))
        t += dur
    return out


def build_html(project: Project, spec: dict, P: list, work: Path) -> tuple[str, list]:
    S = dict(SKIN, **(spec.get("skin") or {}))
    a = work / "assets"
    (a / "fonts").mkdir(parents=True, exist_ok=True)
    for f in (paper.FONT_DIR / "NanumGothic-Bold.ttf", paper.FONT_DIR / "NanumGothic-ExtraBold.ttf", paper.FONT_DIR / "NanumGothic-Regular.ttf"):
        if not (a / "fonts" / f.name).exists():
            shutil.copy(f, a / "fonts" / f.name)
    shutil.copy(hyper.GSAP, a / "gsap.min.js")
    total = P[-1][0] + P[-1][1]
    px, py, pw, ph = PANEL
    media, items, js, subs = [], [], [], []
    for n, (sc, (t0, dur, bt)) in enumerate(zip(spec["scenes"], P)):
        m = sc["media"]
        clip = a / f"m_{n:02d}.mp4"
        src = project.dir("assets") / "footage" / spec["footage"][m["src"]]["file"]
        z = m.get("zoom", 1.0)
        # 패널 비율로 잘라 낸 실제 화면 (pos: 어디를 보여 줄지, zoom: 얼마나 가까이)
        vf = (f"scale={int(pw * z)}:{int(ph * z)}:force_original_aspect_ratio=increase,"
              f"crop={pw}:{ph}:(in_w-{pw})*{m.get('fx', 0.5)}:(in_h-{ph})*{m.get('fy', 0.5)},fps={FPS}")
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", str(m.get("start", 0)), "-i", str(src),
                        "-t", f"{dur + 0.4:.2f}", "-an", "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
                        "-pix_fmt", "yuv420p", str(clip)], check=True)
        vid = f"v{n}"
        media.append(f'<video id="{vid}" class="clip" src="assets/{clip.name}" muted playsinline data-start="{t0:.3f}" '
                     f'data-duration="{dur:.3f}" data-track-index="{2 + n % 2}" style="position:absolute;left:{px}px;top:{py}px;'
                     f'width:{pw}px;height:{ph}px;object-fit:cover;border-radius:22px;opacity:0"></video>')
        js.append(f'tl.set("#{vid}",{{opacity:1}},{t0:.3f});tl.set("#{vid}",{{opacity:0}},{t0 + dur:.3f});')
        if n == 0 or sc["media"]["src"] != spec["scenes"][n - 1]["media"]["src"]:   # 화면이 바뀔 때만 살짝 들어옴
            js.append(f'tl.fromTo("#{vid}",{{y:24}},{{y:0,duration:0.35,ease:"power2.out"}},{t0:.3f});')
        # 제목 (두 줄, 왼쪽 정렬) · 머리말 줄의 회차
        hl = sc.get("hl", "")
        lines = "".join(f'<div>{_e(l).replace(_e(hl), f"<span style=color:{S["accent"]}>{_e(hl)}</span>") if hl else _e(l)}</div>'
                        for l in sc["title"])
        tid = f"t{n}"
        items.append(f'<div id="{tid}" style="position:absolute;left:60px;top:188px;width:960px;font-family:gx;font-size:78px;'
                     f'line-height:1.18;color:{S["ink"]};letter-spacing:-0.01em;opacity:0">{lines}</div>'
                     f'<div id="k{n}" style="position:absolute;left:60px;top:148px;font-family:gb;font-size:30px;color:{S["muted"]};opacity:0">{_e(sc.get("kicker", ""))}</div>'
                     f'<div id="s{n}" style="position:absolute;left:60px;top:1690px;width:960px;font-family:gr;font-size:26px;line-height:1.45;color:{S["muted"]};opacity:0">{_e(sc.get("source", ""))}</div>')
        js.append(f'tl.fromTo("#{tid}",{{opacity:0,y:18}},{{opacity:1,y:0,duration:0.32,ease:"power2.out"}},{t0 + 0.02:.3f});'
                  f'tl.set("#k{n},#s{n}",{{opacity:1}},{t0 + 0.02:.3f});tl.set("#{tid},#k{n},#s{n}",{{opacity:0}},{t0 + dur:.3f});')
        # 자막: 말하는 순간 덩어리로 바뀜 (faster-whisper 단어 시각)
        for k, (b, (bs, bd)) in enumerate(zip(sc["beats"], bt)):
            wav = project.dir("voice") / f"hb_{sc['id']:03d}_{k}.wav"
            parts = hybrid._chunks(b["say"], 18)
            st = hybrid._word_starts(wav, parts, bd) or [bd * i / len(parts) for i in range(len(parts))]
            for j, ptxt in enumerate(parts):
                s0 = t0 + bs + st[j]
                s1 = t0 + bs + (st[j + 1] - 0.02 if j + 1 < len(parts) else bd + 0.15)
                sid = f"c{n}_{k}_{j}"
                items.append(f'<div id="{sid}" style="position:absolute;left:60px;right:60px;top:1405px;text-align:center;opacity:0">'
                             f'<span style="display:inline-block;max-width:960px;padding:18px 30px;border-radius:14px;background:{S["sub_bg"]};'
                             f'color:{S["sub_fg"]};font-family:gb;font-size:52px;line-height:1.3">{_e(ptxt)}</span></div>')
                js.append(f'tl.set("#{sid}",{{opacity:1}},{s0:.3f});tl.set("#{sid}",{{opacity:0}},{max(s1, s0 + 0.3):.3f});')
                subs.append((s0, max(s1, s0 + 0.3), ptxt))
    brand = (f'<div style="position:absolute;left:60px;top:84px;display:flex;align-items:center;gap:14px;font-family:gx;font-size:32px;color:{S["ink"]}">'
             f'<span style="width:14px;height:14px;border-radius:7px;background:{S["accent"]};display:inline-block"></span>{_e(spec.get("brand", ""))}</div>')
    frame = (f'<div style="position:absolute;left:{px - 1}px;top:{py - 1}px;width:{pw + 2}px;height:{ph + 2}px;border-radius:23px;'
             f'box-shadow:0 18px 44px rgba(23,22,20,.16),0 0 0 1px rgba(23,22,20,.08)"></div>')
    prog = (f'<div style="position:absolute;left:60px;right:60px;top:1830px;height:6px;border-radius:3px;background:rgba(23,22,20,.08)"></div>'
            f'<div id="pg" style="position:absolute;left:60px;top:1830px;width:960px;height:6px;border-radius:3px;background:{S["ink"]};'
            f'transform-origin:left center;transform:scaleX(0)"></div>')
    js.append(f'tl.to("#pg",{{scaleX:1,duration:{total:.3f},ease:"none"}},0);')
    doc = f"""<!doctype html>
<html lang="ko"><head><meta charset="UTF-8"><meta name="viewport" content="width={W}, height={H_}">
<script src="assets/gsap.min.js"></script>
<style>
@font-face{{font-family:gr;src:url('assets/fonts/NanumGothic-Regular.ttf')}}
@font-face{{font-family:gb;src:url('assets/fonts/NanumGothic-Bold.ttf')}}
@font-face{{font-family:gx;src:url('assets/fonts/NanumGothic-ExtraBold.ttf')}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H_}px;overflow:hidden;background:{S["bg"]}}}
#root{{position:relative;width:100%;height:100%;background:{S["bg"]}}}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{total:.3f}" data-width="{W}" data-height="{H_}">
{frame}{"".join(media)}
<div id="layer" class="clip" data-start="0" data-duration="{total:.3f}" data-track-index="1" data-layout-allow-overlap>
{brand}{"".join(items)}{prog}
</div></div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
window.__timelines["main"] = tl;
tl.seek(0);
</script></body></html>"""
    return doc, subs


def _ass(subs: list, path: Path):
    t = lambda x: f"{int(x // 3600)}:{int(x % 3600 // 60):02d}:{x % 60:05.2f}"
    head = ("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\n\n[V4+ Styles]\n"
            "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, "
            "ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
            "Style: Sub,NanumGothic,52,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,1,0,0,0,100,100,0,0,1,0,0,2,60,60,500,1\n\n"
            "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
    path.write_text(head + "".join(f"Dialogue: 0,{t(a)},{t(b)},Sub,,0,0,0,,{x}\n" for a, b, x in subs), encoding="utf-8")


def make(project: Project) -> Path:
    spec = json.loads((project.dir("script") / "short.json").read_text(encoding="utf-8"))
    for i, sc in enumerate(spec["scenes"], 1):
        sc["id"] = i
    durs = hybrid.voice(project, spec)
    P = plan(spec, durs)
    edir = project.dir("edit")
    work = edir / "short_work"
    work.mkdir(parents=True, exist_ok=True)
    doc, subs = build_html(project, spec, P, work)
    (work / "index.html").write_text(doc, encoding="utf-8")
    (work / "hyperframes.json").write_text(json.dumps({"name": "short"}), encoding="utf-8")
    vid = work / "video.mp4"
    err = hybrid.render_scene(work, vid)
    if err:
        raise SystemExit(f"[short] 렌더 실패: {err}")
    vdur = _dur(vid)
    # 소리: 박자 음성을 제자리에 놓고, 효과음·배경음 없이 -16 LUFS (Codex 쇼츠와 같은 기준)
    inputs, filt, k = [], [], 0
    for sc, (t0, dur, bt) in zip(spec["scenes"], P):
        for j, (bs, bd) in enumerate(bt):
            inputs += ["-i", str(project.dir("voice") / f"hb_{sc['id']:03d}_{j}.wav")]
            ms = int(round((t0 + bs) * 1000))
            filt.append(f"[{k}:a]adelay={ms}|{ms}[a{k}]")
            k += 1
    filt.append("".join(f"[a{i}]" for i in range(k)) + f"amix=inputs={k}:normalize=0,apad,atrim=0:{vdur:.3f},loudnorm=I=-16:TP=-1.5:LRA=7[out]")
    aud = work / "audio.wav"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *inputs, "-filter_complex", ";".join(filt), "-map", "[out]",
                    "-ar", "48000", "-ac", "2", str(aud)], check=True)
    final = edir / "final.mp4"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(vid), "-i", str(aud), "-map", "0:v", "-map", "1:a",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                    "-movflags", "+faststart", "-shortest", str(final)], check=True)
    _ass(subs, edir / "subs.ass")
    project.write_json("edit", "short_timeline.json", [{"scene": sc["id"], "start": t0, "dur": d, "beats": bt}
                                                       for sc, (t0, d, bt) in zip(spec["scenes"], P)])
    from . import syncqa
    syncqa.run(project)
    print(f"[short] {final} ({_dur(final):.1f}초)")
    return final
