"""훅 쇼츠 — 얼굴 없이 (스타일 hook-shorts, docs/25 §2-1). 레퍼런스 PICKIT 쇼츠의 '편집 기법'만 가져옴 (얼굴은 쓰지 않음, 2026-11-13 사용자).

AI 목소리(채널 목소리) + 실제 화면(저장소·문서 캡처, 화면 녹화)을 꽉 채운 세로 쇼츠:
  ① 첫 3초 훅 제목(로고 + 세 줄, 한 낱말 강조색) ② 박자마다 화면이 '탁' 바뀜 — 같은 화면이면 번갈아 확대(펀치 인)·다른 곳으로 이동
  ③ 말하는 순간 바뀌는 큰 자막(흰 글씨 + 검은 테두리, 핵심 낱말 노랑) ④ 말에 맞춰 튀어나오는 카드(목록·숫자·명령어)
  ⑤ 박자 사이 쉼 0.12초 (점프 컷 같은 빠른 리듬) ⑥ 위 왼쪽 작은 채널 이름

    python -m ytflow hookshort <프로젝트>     # 02_script/hookshort.json → 05_edit/final.mp4 (+ subs.ass, sync-qa)

hookshort.json:
{"brand": "AI 더 잘 쓰기", "hook": {"lines": ["앤트로픽이", "직접 푼", "클로드 스킬"], "hl": "클로드 스킬", "logo": "footage/logo.png", "dur": 3.0},
 "keywords": ["스킬", "19만"],
 "scenes": [{"media": {"file": "footage/repo_top.png", "pos": "50% 0%", "zoom": 1.0},     # 그림·영상 (04_assets 아래)
             "beats": [{"say": "...", "insert": {"cards": [{"icon": "🎨", "title": "디자인"}]}},       # 카드 묶음
                       {"say": "...", "insert": {"number": "19만", "label": "GitHub 별"}},           # 큰 숫자
                       {"say": "...", "insert": {"code": "/plugin marketplace add anthropics/skills"}}]}],   # 명령어
 "source": "출처 한 줄"}
"""
from __future__ import annotations

import html as H
import json
import shutil
import subprocess
from pathlib import Path

from ..project import Project
from . import hybrid, hyper, paper

W, H_ = 1080, 1920
YEL, ORG = "#FFD84D", "#FF7A3D"
LEAD, GAP, TAIL = 0.15, 0.12, 0.5


def _e(s) -> str:
    return H.escape(str(s))


def _dur(p: Path) -> float:
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True).stdout or 0)


def _insert_html(ins: dict) -> str:
    if ins.get("cards"):
        cards = "".join(f'<div class="cd" style="width:290px;height:300px;background:#fff;border-radius:24px;box-shadow:0 14px 34px rgba(0,0,0,.4);'
                        f'display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px">'
                        f'<div style="width:92px;height:92px;border-radius:46px;background:{YEL};display:flex;align-items:center;justify-content:center;font-size:50px">{_e(c.get("icon", ""))}</div>'
                        f'<div style="font-family:gx;font-size:44px;color:#111">{_e(c.get("title", ""))}</div>'
                        f'<div style="font-family:gr;font-size:24px;color:#777">{_e(c.get("sub", ""))}</div></div>' for c in ins["cards"][:3])
        return f'<div style="display:flex;gap:26px;justify-content:center">{cards}</div>'
    if ins.get("code"):
        return (f'<div style="font-family:gr;font-size:30px;color:#888;text-align:center;margin-bottom:22px">{_e(ins.get("label", "이렇게 입력"))}</div>'
                f'<div style="background:#111;color:#7CFFB2;border-radius:16px;padding:30px 34px;font-family:monospace;font-size:40px;line-height:1.35;'
                f'word-break:break-all">$ {_e(ins["code"])}</div>')
    return (f'<div style="text-align:center;font-family:gr;font-size:38px;color:#555">{_e(ins.get("label", ""))}</div>'
            f'<div style="text-align:center;font-family:gx;font-size:170px;line-height:1.1;color:#111">{_e(ins.get("number", ""))}</div>')


def make(project: Project) -> Path:
    spec = json.loads((project.dir("script") / "hookshort.json").read_text(encoding="utf-8"))
    for i, sc in enumerate(spec["scenes"], 1):
        sc["id"] = i
    durs = hybrid.voice(project, spec)   # 채널 목소리 (channel.yaml tts) 또는 초안
    edir = project.dir("edit")
    work = edir / "hookshort_work"
    a = work / "assets"
    (a / "fonts").mkdir(parents=True, exist_ok=True)
    for f in ("NanumGothic-ExtraBold.ttf", "NanumGothic-Regular.ttf"):
        if not (a / "fonts" / f).exists():
            shutil.copy(paper.FONT_DIR / f, a / "fonts" / f)
    shutil.copy(hyper.GSAP, a / "gsap.min.js")
    # 시간표: 박자를 짧은 쉼으로 잇는다
    t, plan = LEAD, []
    for sc in spec["scenes"]:
        for k, b in enumerate(sc["beats"]):
            d = durs[f"{sc['id']:03d}_{k}"]
            plan.append((sc, k, b, t, d))
            t += d + GAP
    total = t - GAP + TAIL
    media, items, js, subs = [], [], [], []
    kws = spec.get("keywords", [])
    prev_file, flip = None, 0
    for n, (sc, k, b, t0, d) in enumerate(plan):
        m = dict(sc.get("media") or {}, **(b.get("media") or {}))
        src = project.dir("assets") / m["file"]
        name = f"m{n:02d}{src.suffix}"
        if not (a / name).exists():
            shutil.copy(src, a / name)
        same = m["file"] == prev_file
        flip = (flip + 1) % 2 if same else 0
        z = m.get("zoom", 1.0) * (1.12 if flip else 1.0)          # 같은 화면이면 번갈아 확대 (펀치 인)
        pos = m.get("pos", "50% 0%")
        end = t0 + d + (GAP if n + 1 < len(plan) else TAIL)
        vid = f"md{n}"
        if src.suffix.lower() in (".mp4", ".mov", ".webm"):
            media.append(f'<video id="{vid}" class="clip" src="assets/{name}" muted playsinline data-start="{t0 - (LEAD if n == 0 else 0):.3f}" '
                         f'data-duration="{end - t0:.3f}" data-track-index="{2 + n % 2}" style="position:absolute;inset:0;width:100%;height:100%;'
                         f'object-fit:cover;object-position:{pos};transform:scale({z});transform-origin:{pos}"></video>')
        else:
            media.append(f'<div id="{vid}" style="position:absolute;inset:0;overflow:hidden;opacity:0;background:#0d1117">'
                         f'<img src="assets/{name}" style="width:100%;height:100%;object-fit:cover;object-position:{pos};transform-origin:{pos};transform:scale({z})"></div>')
            js.append(f'tl.set("#{vid}",{{opacity:1}},{(0 if n == 0 else t0):.3f});tl.set("#{vid}",{{opacity:0}},{end:.3f});'
                      f'tl.fromTo("#{vid} img",{{scale:{z}}},{{scale:{z * 1.04:.3f},duration:{end - t0:.3f},ease:"none"}},{t0:.3f});')
        prev_file = m["file"]
        # 자막: 말하는 순간 바뀜
        wav = project.dir("voice") / f"hb_{sc['id']:03d}_{k}.wav"
        parts = hybrid._chunks(b["say"], spec.get("chunk", 12))
        st = hybrid._word_starts(wav, parts, d) or [d * i / len(parts) for i in range(len(parts))]
        for j, ptxt in enumerate(parts):
            s0 = t0 + st[j]
            s1 = t0 + (st[j + 1] - 0.02 if j + 1 < len(parts) else d + GAP * 0.8)
            h = _e(ptxt)
            for kw in kws:
                h = h.replace(_e(kw), f'<span style="color:{YEL}">{_e(kw)}</span>')
            cid = f"c{n}_{j}"
            fs = min(72, int(940 / max(len(ptxt), 1)))   # 한 줄에 들어가게 (2026-11-13: 긴 덩어리가 화면 끝에 닿음)
            items.append(f'<div id="{cid}" style="position:absolute;left:50px;right:50px;top:1330px;text-align:center;font-family:gx;font-size:{fs}px;white-space:nowrap;'
                         f'line-height:1.2;color:#fff;-webkit-text-stroke:4px #000;paint-order:stroke fill;text-shadow:0 4px 14px rgba(0,0,0,.75);opacity:0">{h}</div>')
            js.append(f'tl.set("#{cid}",{{opacity:1}},{s0:.3f});tl.set("#{cid}",{{opacity:0}},{max(s1, s0 + 0.2):.3f});')
            subs.append((s0, max(s1, s0 + 0.2), ptxt))
        # 끼워 넣는 카드
        if b.get("insert"):
            iid = f"in{n}"
            ti = t0 + b["insert"].get("delay", 0.15)
            items.append(f'<div id="{iid}" style="position:absolute;left:40px;right:40px;top:520px;padding:56px 34px;background:rgba(246,244,238,.97);'
                         f'border-radius:32px;box-shadow:0 24px 70px rgba(0,0,0,.5);opacity:0">{_insert_html(b["insert"])}</div>')
            js.append(f'tl.fromTo("#{iid}",{{opacity:0,scale:0.88,y:30}},{{opacity:1,scale:1,y:0,duration:0.3,ease:"back.out(1.8)"}},{ti:.3f});'
                      f'tl.from("#{iid} .cd",{{opacity:0,y:30,stagger:0.12,duration:0.25}},{ti + 0.1:.3f});'
                      f'tl.to("#{iid}",{{opacity:0,duration:0.15}},{t0 + d:.3f});')
    # 위·아래 어둡게(글자 대비) · 채널 이름 · 훅 제목 · 출처
    items.insert(0, '<div style="position:absolute;inset:0;background:rgba(0,0,0,.22)"></div>'
                    '<div style="position:absolute;left:0;right:0;top:0;height:900px;background:linear-gradient(180deg,rgba(0,0,0,.72),rgba(0,0,0,0))"></div>'
                    '<div style="position:absolute;left:0;right:0;bottom:0;height:900px;background:linear-gradient(0deg,rgba(0,0,0,.7),rgba(0,0,0,0))"></div>'
                    f'<div style="position:absolute;left:60px;top:70px;font-family:gx;font-size:30px;color:#fff;letter-spacing:2px">{_e(spec.get("brand", ""))}</div>')
    hk = spec.get("hook") or {}
    if hk:
        hl = hk.get("hl", "")
        lines = "".join(f'<div style="color:{ORG if hl and hl in l else "#fff"}">{_e(l)}</div>' for l in hk["lines"])
        logo = ""
        if hk.get("logo") and (project.dir("assets") / hk["logo"]).exists():
            shutil.copy(project.dir("assets") / hk["logo"], a / "logo.png")
            logo = '<img src="assets/logo.png" style="width:130px;height:130px;border-radius:28px;margin-bottom:28px;display:block">'
        items.append(f'<div id="hk" style="position:absolute;left:70px;top:300px;width:940px;font-family:gx;font-size:104px;line-height:1.12;'
                     f'-webkit-text-stroke:3px rgba(0,0,0,.6);paint-order:stroke fill;text-shadow:0 6px 26px rgba(0,0,0,.7)">{logo}{lines}</div>')
        js.append(f'tl.fromTo("#hk",{{opacity:0,y:24}},{{opacity:1,y:0,duration:0.3,ease:"power3.out"}},0.02);'
                  f'tl.to("#hk",{{opacity:0,duration:0.2}},{hk.get("dur", 3.0):.2f});')
    if spec.get("source"):
        items.append(f'<div style="position:absolute;left:60px;right:60px;top:1800px;font-family:gr;font-size:24px;color:rgba(255,255,255,.75)">{_e(spec["source"])}</div>')
    doc = f"""<!doctype html>
<html lang="ko"><head><meta charset="UTF-8"><meta name="viewport" content="width={W}, height={H_}">
<script src="assets/gsap.min.js"></script>
<style>
@font-face{{font-family:gr;src:url('assets/fonts/NanumGothic-Regular.ttf')}}
@font-face{{font-family:gx;src:url('assets/fonts/NanumGothic-ExtraBold.ttf')}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H_}px;overflow:hidden;background:#000}}
#root{{position:relative;width:100%;height:100%;background:#000}}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{total:.3f}" data-width="{W}" data-height="{H_}">
{"".join(media)}
<div id="layer" class="clip" data-start="0" data-duration="{total:.3f}" data-track-index="1" data-layout-allow-overlap>
{"".join(items)}
</div></div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
window.__timelines["main"] = tl;
tl.seek(0);
</script></body></html>"""
    (work / "index.html").write_text(doc, encoding="utf-8")
    (work / "hyperframes.json").write_text(json.dumps({"name": "hookshort"}), encoding="utf-8")
    vid = work / "video.mp4"
    err = hybrid.render_scene(work, vid)
    if err:
        raise SystemExit(f"[hookshort] 렌더 실패: {err}")
    vdur = _dur(vid)
    inputs, filt = [], []
    for i, (sc, k, b, t0, d) in enumerate(plan):
        inputs += ["-i", str(project.dir("voice") / f"hb_{sc['id']:03d}_{k}.wav")]
        ms = int(round(t0 * 1000))
        filt.append(f"[{i}:a]adelay={ms}|{ms}[a{i}]")
    filt.append("".join(f"[a{i}]" for i in range(len(plan))) + f"amix=inputs={len(plan)}:normalize=0,apad,atrim=0:{vdur:.3f},loudnorm=I=-14:TP=-1.5:LRA=7[out]")
    aud = work / "audio.wav"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *inputs, "-filter_complex", ";".join(filt), "-map", "[out]",
                    "-ar", "48000", "-ac", "2", str(aud)], check=True)
    final = edir / "final.mp4"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(vid), "-i", str(aud), "-map", "0:v", "-map", "1:a",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                    "-movflags", "+faststart", "-shortest", str(final)], check=True)
    from .shorts_hf import _ass
    _ass(subs, edir / "subs.ass")
    from . import syncqa
    try:
        syncqa.run(project)
    except Exception as e:  # noqa: BLE001
        print(f"[hookshort] 싱크 점검 건너뜀: {e}")
    print(f"[hookshort] {final} ({_dur(final):.1f}초) · 박자 {len(plan)}개")
    return final
