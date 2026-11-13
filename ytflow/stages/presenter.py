"""말하는 사람 쇼츠 (스타일 presenter-shorts, docs/25-reference-2611.md §2).

사람이 카메라 앞에서 말한 영상 하나 → 세로 쇼츠:
  ① 받아쓰기(faster-whisper)로 말 사이 쉼을 잘라 '점프 컷' ② 컷마다 번갈아 살짝 확대(펀치 인) ③ 9:16 로 자르기
  ④ 첫 몇 초 훅 제목(두세 줄, 한 낱말 강조색 + 로고) ⑤ 말하는 순간 바뀌는 큰 자막(핵심 낱말 노란색)
  ⑥ 말하는 낱말에 맞춰 위쪽에 '끼워 넣는 카드'(목록·숫자·로고) — 사람 얼굴은 아래에 그대로.

    python -m ytflow presenter <프로젝트>      # 02_script/presenter.json → 05_edit/final.mp4 (+ subs.ass)

presenter.json:
{"source": "selfie_0101.mp4", "start": 0, "end": 60, "lang": "ko", "brand": "이어 읽는 시장",
 "face_x": 0.5,                      # 가로 화면에서 얼굴 가운데 (0~1) — 세로로 자를 때
 "hook": {"lines": ["클로드", "우승자가 만든", "최고의 스킬"], "hl": "클로드", "dur": 3.0, "logo": "logo.png"},
 "keywords": ["충격", "인정"],
 "inserts": [{"word": "마케팅", "dur": 2.6, "cards": [{"icon": "📈", "title": "마케팅"}, {"icon": "📝", "title": "콘텐츠"}]},
             {"word": "6,454", "dur": 2.0, "number": "6,454", "label": "모든 영상"}],
 "punch": 1.12, "gap": 0.35}
원본 영상은 04_assets/footage/ 에 (본인 촬영 · 퍼블릭 도메인 · 권리 있는 것만).
"""
from __future__ import annotations

import html as H
import json
import shutil
import subprocess
from pathlib import Path

from ..project import Project
from . import align, hybrid, hyper, paper

W, H_ = 1080, 1920
YEL, ORG = "#FFD84D", "#FF7A3D"


def _e(s) -> str:
    return H.escape(str(s))


def _dur(p: Path) -> float:
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True).stdout or 0)


def segments(words: list, gap: float) -> list:
    """말 덩어리: 단어 사이가 gap 초보다 길면 거기서 자른다 → [(시작, 끝, [단어…])]."""
    segs, cur = [], []
    for w in words:
        if cur and w["start"] - cur[-1]["end"] > gap:
            segs.append(cur)
            cur = []
        cur.append(w)
    if cur:
        segs.append(cur)
    return [(max(0.0, s[0]["start"] - 0.08), s[-1]["end"] + 0.14, s) for s in segs]


def cut(src: Path, segs: list, out: Path, face_x: float, punch: float) -> list:
    """세그먼트를 잘라 9:16 로 + 번갈아 펀치 인 → 이어 붙임. 반환: 새 시간축의 단어 목록."""
    tmp, parts, words, t = out.parent / "cut_parts", [], [], 0.0
    tmp.mkdir(parents=True, exist_ok=True)
    vw = int(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", str(src)],
                            capture_output=True, text=True).stdout.strip().split(",")[0])
    for k, (a, b, ws) in enumerate(segs):
        z = punch if k % 2 else 1.0
        cw = f"ih*9/16/{z}"
        crop = f"crop={cw}:ih/{z}:min(max(0\\,{face_x}*iw-({cw})/2)\\,iw-{cw}):(ih-ih/{z})/2" if vw else "null"
        p = tmp / f"p{k:03d}.mp4"
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{a:.3f}", "-i", str(src), "-t", f"{b - a:.3f}",
                        "-vf", f"{crop},scale={W}:{H_},fps=30,setsar=1", "-af", "aresample=48000,afade=t=in:d=0.03",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac", "-ar", "48000", str(p)], check=True)
        d = _dur(p)
        for w in ws:
            words.append({"word": w["word"], "start": round(t + w["start"] - a, 3), "end": round(t + w["end"] - a, 3)})
        parts.append(p)
        t += d
    lst = tmp / "list.txt"
    lst.write_text("\n".join(f"file '{p.resolve()}'" for p in parts), encoding="utf-8")
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(out)], check=True)
    shutil.rmtree(tmp, ignore_errors=True)
    return words


def chunks(words: list, n: int = 14) -> list:
    out, cur = [], []
    for w in words:
        txt = " ".join(x["word"] for x in cur + [w])
        if cur and (len(txt) > n or cur[-1]["word"].endswith((".", "?", "!", ","))):
            out.append(cur)
            cur = []
        cur.append(w)
    if cur:
        out.append(cur)
    return out


def make(project: Project) -> Path:
    spec = json.loads((project.dir("script") / "presenter.json").read_text(encoding="utf-8"))
    src = project.dir("assets") / "footage" / spec["source"]
    edir = project.dir("edit")
    work = edir / "presenter_work"
    a = work / "assets"
    (a / "fonts").mkdir(parents=True, exist_ok=True)
    for f in ("NanumGothic-Bold.ttf", "NanumGothic-ExtraBold.ttf", "NanumGothic-Regular.ttf"):
        if not (a / "fonts" / f).exists():
            shutil.copy(paper.FONT_DIR / f, a / "fonts" / f)
    shutil.copy(hyper.GSAP, a / "gsap.min.js")
    words = [w for w in align.transcribe(src, spec.get("lang")) if spec.get("start", 0) <= w["start"] and w["end"] <= spec.get("end", 1e9)]
    segs = segments(words, spec.get("gap", 0.35))
    cutv = a / "cut.mp4"
    nw = cut(src, segs, cutv, spec.get("face_x", 0.5), spec.get("punch", 1.12))
    total = _dur(cutv)
    items, js, subs = [], [], []
    # 아래 자막 쪽 어둡게 + 위쪽 어둡게 (글자 대비)
    items.append('<div style="position:absolute;left:0;right:0;top:0;height:760px;background:linear-gradient(180deg,rgba(0,0,0,.55),rgba(0,0,0,0))"></div>'
                 '<div style="position:absolute;left:0;right:0;bottom:0;height:820px;background:linear-gradient(0deg,rgba(0,0,0,.45),rgba(0,0,0,0))"></div>')
    # 브랜드 (위 왼쪽 작게, 계속)
    items.append(f'<div style="position:absolute;left:60px;top:70px;font-family:gx;font-size:30px;color:#fff;letter-spacing:2px">{_e(spec.get("brand", ""))}</div>')
    # 훅 제목
    hk = spec.get("hook") or {}
    if hk:
        hl = hk.get("hl", "")
        lines = "".join(f'<div style="color:{ORG if hl and hl in l else "#fff"}">{_e(l)}</div>' for l in hk["lines"])
        logo = ""
        if hk.get("logo") and (project.dir("assets") / hk["logo"]).exists():
            shutil.copy(project.dir("assets") / hk["logo"], a / "logo.png")
            logo = '<img src="assets/logo.png" style="width:120px;height:120px;border-radius:26px;margin-bottom:26px;display:block">'
        items.append(f'<div id="hk" style="position:absolute;left:70px;top:330px;width:940px;font-family:gx;font-size:96px;line-height:1.14;'
                     f'text-shadow:0 6px 24px rgba(0,0,0,.6)">{logo}{lines}</div>')
        js.append(f'tl.fromTo("#hk",{{opacity:0,y:24}},{{opacity:1,y:0,duration:0.35,ease:"power3.out"}},0.05);'
                  f'tl.to("#hk",{{opacity:0,duration:0.25}},{hk.get("dur", 3.0):.2f});')
    # 자막 (말하는 순간 덩어리, 핵심 낱말 노란색)
    kws = [k.lower() for k in spec.get("keywords", [])]
    chs = chunks(nw, spec.get("chunk", 14))
    for k, ch in enumerate(chs):
        s0, s1 = ch[0]["start"], ch[-1]["end"] + 0.12
        if k + 1 < len(chs):   # 다음 자막과 겹치지 않게 (2026-11-13 시험작에서 두 줄이 겹쳐 보임)
            s1 = min(s1, chs[k + 1][0]["start"] - 0.02)
        txt = " ".join(f'<span style="color:{YEL if any(q in w["word"].lower() for q in kws) else "#fff"}">{_e(w["word"])}</span>' for w in ch)
        cid = f"c{k}"
        items.append(f'<div id="{cid}" style="position:absolute;left:50px;right:50px;top:1330px;text-align:center;font-family:gx;font-size:76px;'
                     f'line-height:1.2;-webkit-text-stroke:3px #000;paint-order:stroke fill;text-shadow:0 4px 12px rgba(0,0,0,.7);opacity:0">{txt}</div>')
        s1 = max(s1, s0 + 0.15)
        js.append(f'tl.set("#{cid}",{{opacity:1}},{s0:.3f});tl.set("#{cid}",{{opacity:0}},{s1:.3f});')
        subs.append((s0, s1, " ".join(w["word"] for w in ch)))
    # 끼워 넣는 카드 (위쪽 절반, 말하는 낱말에 맞춰)
    for k, ins in enumerate(spec.get("inserts", [])):
        hit = next((w for w in nw if ins["word"].lower() in w["word"].lower()), None)
        if not hit:
            print(f"[presenter] 카드 {k + 1}: '{ins['word']}' 를 말하는 곳을 못 찾음 — 건너뜀")
            continue
        t0, d = hit["start"], ins.get("dur", 2.5)
        iid = f"in{k}"
        if ins.get("cards"):
            cards = "".join(f'<div class="cd" style="width:270px;height:300px;background:#fff;border-radius:22px;box-shadow:0 12px 30px rgba(0,0,0,.35);'
                            f'display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px">'
                            f'<div style="width:86px;height:86px;border-radius:43px;background:{YEL};display:flex;align-items:center;justify-content:center;font-size:48px">{_e(c.get("icon", ""))}</div>'
                            f'<div style="font-family:gx;font-size:44px;color:#111">{_e(c.get("title", ""))}</div>'
                            f'<div style="font-family:gr;font-size:24px;color:#777">{_e(c.get("sub", ""))}</div></div>' for c in ins["cards"][:3])
            body = f'<div style="display:flex;gap:30px;justify-content:center">{cards}</div>'
        else:
            body = (f'<div style="text-align:center;font-family:gr;font-size:36px;color:#555">{_e(ins.get("label", ""))}</div>'
                    f'<div style="text-align:center;font-family:gx;font-size:150px;color:#111">{_e(ins.get("number", ""))}</div>')
        # 카드가 뜨는 동안 얼굴(영상)을 아래 절반으로 내린다 — 카드가 얼굴을 가리지 않게 (레퍼런스 PICKIT 의 위 카드·아래 사람 배치)
        js.append(f'tl.to("#v",{{y:560,duration:0.3,ease:"power2.out"}},{t0:.3f});tl.to("#v",{{y:0,duration:0.3,ease:"power2.inOut"}},{t0 + d:.3f});')
        items.append(f'<div id="{iid}" style="position:absolute;left:40px;right:40px;top:190px;padding:60px 30px;background:rgba(246,244,238,.97);'
                     f'border-radius:30px;box-shadow:0 20px 60px rgba(0,0,0,.4);opacity:0">{body}</div>')
        js.append(f'tl.fromTo("#{iid}",{{opacity:0,scale:0.9,y:20}},{{opacity:1,scale:1,y:0,duration:0.3,ease:"back.out(1.8)"}},{t0:.3f});'
                  f'tl.from("#{iid} .cd",{{opacity:0,y:30,stagger:0.12,duration:0.25}},{t0 + 0.1:.3f});'
                  f'tl.to("#{iid}",{{opacity:0,duration:0.2}},{t0 + d:.3f});')
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
<video id="v" class="clip" src="assets/cut.mp4" muted playsinline data-start="0" data-duration="{total:.3f}" data-track-index="2" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover"></video>
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
    (work / "hyperframes.json").write_text(json.dumps({"name": "presenter"}), encoding="utf-8")
    vid = work / "video.mp4"
    err = hybrid.render_scene(work, vid)
    if err:
        raise SystemExit(f"[presenter] 렌더 실패: {err}")
    final = edir / "final.mp4"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(vid), "-i", str(cutv), "-map", "0:v", "-map", "1:a",
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=9", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", str(final)], check=True)
    from .shorts_hf import _ass
    _ass(subs, edir / "subs.ass")
    project.write_json("edit", "presenter_timeline.json", {"cuts": len(segs), "removed_s": round(sum(w["end"] - w["start"] for w in words) and
                                                                                         (words[-1]["end"] - words[0]["start"]) - total, 2), "duration": total})
    print(f"[presenter] {final} ({_dur(final):.1f}초) · 컷 {len(segs)}개")
    return final
