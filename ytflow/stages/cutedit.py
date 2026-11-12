"""원본 발언 컷편집 (스타일 source-cut, docs/24 · styles/source-cut/STYLE.md).

긴 원본(어닝콜·기자회견·인터뷰 영상) 전체를 받아쓰기해서, 대본이 말하는 내용과 맞는 부분만 단어 단위로 잘라
'그 사람이 직접 말하는 장면(bite)'으로 넣는다. 여러 군데를 잘라 이으면 점프 컷(짧은 흰 번쩍임)으로 붙인다.

대본 (02_script/hybrid.json):
  "footage": {"fomc": {"file": "fomc_20230614_part.mp4", "credit": "Federal Reserve · 퍼블릭 도메인"}},
  {"type": "bite", "who": "제롬 파월", "role": "연준 의장 · 2023년 6월 14일 기자회견",
   "beats": [{"say": "파월 의장의 설명을 직접 들어 보겠습니다."}],          # 앞 내레이션 (없어도 됨: [])
   "clip": {"src": "fomc", "cuts": [
       {"find": "원문 문장 그대로 (받아쓰기·공식 녹취록)", "ko": "번역 자막"},
       {"from": "시작 몇 단어", "to": "끝 몇 단어", "ko": "번역 자막"}]}}  # 긴 구간은 처음·끝 몇 단어로

명령: python -m ytflow cut <프로젝트>   → 원본 받아쓰기(캐시) → 구간 찾기 → 02_script/cuts.json (사람이 확인·수정 가능)
       hybrid 렌더가 cuts.json 으로 잘라 붙인다 (bite 장면이 있으면 자동으로 cut 부터).
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from . import align

PAD_BEFORE, PAD_AFTER = 0.12, 0.35   # 말 앞뒤 여유 (숨소리 잘림 방지)
MIN_SCORE = 0.6
JOIN = 0.18                          # 점프 컷 사이 흰 번쩍임 길이(초)


def _src(project, spec: dict, key: str) -> Path:
    return project.dir("assets") / "footage" / spec["footage"][key]["file"]


def _find_span(words: list[dict], frm: str, to: str) -> tuple[float, float, float] | None:
    a = align.find_quote(words, frm)
    if not a:
        return None
    i0 = next(k for k, w in enumerate(words) if w["start"] >= a[0] - 1e-6)
    rest = words[i0:]
    b = align.find_quote(rest, to)
    if not b:
        return None
    return a[0], b[1], min(a[2], b[2])


def find(project, spec: dict | None = None, force: bool = False) -> dict:
    """bite 장면의 cuts 를 원본에서 찾아 02_script/cuts.json 에 쓴다. 이미 있는 항목(사람이 고친 것)은 그대로 둔다."""
    spec = spec or json.loads((project.dir("script") / "hybrid.json").read_text(encoding="utf-8"))
    out_p = project.dir("script") / "cuts.json"
    old = json.loads(out_p.read_text(encoding="utf-8")) if out_p.exists() and not force else {}
    res, report = {}, []
    for sc in spec["scenes"]:
        if sc.get("type") != "bite":
            continue
        clip = sc["clip"]
        src = _src(project, spec, clip["src"])
        lang = clip.get("lang", "en")
        segs = []
        for k, c in enumerate(clip["cuts"]):
            key = c.get("find") or f"{c.get('from')} … {c.get('to')}"
            prev = next((s for s in old.get(str(sc["id"]), []) if s.get("key") == key), None)
            if prev and prev.get("start") is not None:
                segs.append({**prev, "ko": c.get("ko", prev.get("ko", ""))})
                continue
            if "start" in c and "end" in c:   # 사람이 시각을 직접 준 경우
                hit = (float(c["start"]), float(c["end"]), 1.0)
            else:
                words = align.transcribe(src, lang)
                hit = align.find_quote(words, c["find"]) if c.get("find") else _find_span(words, c["from"], c["to"])
            if not hit or hit[2] < MIN_SCORE:
                report.append(f"#{sc['id']} 구간 {k + 1}: 찾지 못함 (일치도 {hit[2] if hit else 0:.2f}) — '{key[:50]}'")
                segs.append({"key": key, "start": None, "end": None, "score": round(hit[2], 2) if hit else 0, "ko": c.get("ko", "")})
                continue
            st, en, scr = hit
            words = align.transcribe(src, lang)
            heard = " ".join(w["word"] for w in words if st - 1e-3 <= w["start"] and w["end"] <= en + 1e-3)
            segs.append({"key": key, "start": round(max(0.0, st - PAD_BEFORE), 2), "end": round(en + PAD_AFTER, 2),
                         "score": round(scr, 2), "heard": heard, "ko": c.get("ko", "")})
            report.append(f"#{sc['id']} 구간 {k + 1}: {st:.1f}~{en:.1f}s (일치도 {scr:.2f})")
        res[str(sc["id"])] = segs
    out_p.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    for r in report:
        print("[cut]", r)
    return res


def prepare(project, spec: dict) -> None:
    """bite 장면마다 잘린 구간을 이어 붙인 영상·소리를 만들고 sc['_bite'] 에 정보(길이·구간 시각)를 넣는다."""
    bites = [sc for sc in spec["scenes"] if sc.get("type") == "bite"]
    if not bites:
        return
    p = project.dir("script") / "cuts.json"
    cuts = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    if any(str(sc["id"]) not in cuts for sc in bites):
        cuts = find(project, spec)
    bdir = project.dir("assets") / "bites"
    bdir.mkdir(parents=True, exist_ok=True)
    for sc in bites:
        segs = [s for s in cuts.get(str(sc["id"]), []) if s.get("start") is not None]
        if not segs:
            raise SystemExit(f"[cut] #{sc['id']} 쓸 구간이 없습니다 — 02_script/cuts.json 에 start/end 를 직접 넣거나 find 문장을 고치세요")
        src = _src(project, spec, sc["clip"]["src"])
        sig = json.dumps([(s["start"], s["end"]) for s in segs]) + str(src.stat().st_size)
        vid, wav, side = bdir / f"bite_{sc['id']:03d}.mp4", bdir / f"bite_{sc['id']:03d}.wav", bdir / f"bite_{sc['id']:03d}.txt"
        if not (vid.exists() and wav.exists() and side.exists() and side.read_text(encoding="utf-8") == sig):
            parts_v, parts_a, n = [], [], len(segs)
            for k, s in enumerate(segs):
                pv, pa = bdir / f"_b{sc['id']}_{k}.mp4", bdir / f"_b{sc['id']}_{k}.wav"
                d = s["end"] - s["start"]
                fade = f",fade=t=in:st=0:d={JOIN}:color=white" if k else ""
                subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{s['start']:.3f}", "-i", str(src), "-t", f"{d:.3f}",
                                "-an", "-vf", "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30" + fade,
                                "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", str(pv)], check=True)
                af = f"afade=t=in:d=0.06,afade=t=out:st={max(d - 0.12, 0):.3f}:d=0.12"
                subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{s['start']:.3f}", "-i", str(src), "-t", f"{d:.3f}",
                                "-vn", "-af", af + ",loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000", "-ac", "2", str(pa)], check=True)
                parts_v.append(pv)
                parts_a.append(pa)
            lst = bdir / f"_b{sc['id']}.txt"
            lst.write_text("\n".join(f"file '{x.resolve()}'" for x in parts_v), encoding="utf-8")
            subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(vid)], check=True)
            lst.write_text("\n".join(f"file '{x.resolve()}'" for x in parts_a), encoding="utf-8")
            subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(wav)], check=True)
            for x in parts_v + parts_a + [lst]:
                x.unlink(missing_ok=True)
            side.write_text(sig, encoding="utf-8")
            del n
        t, segt = 0.0, []
        for s in segs:
            d = s["end"] - s["start"]
            segt.append({"t0": round(t, 3), "t1": round(t + d, 3), "ko": s.get("ko", ""), "en": s.get("heard", "")})
            t += d
        # 실제 이어 붙인 길이 (프레임 반올림 차이)
        real = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(wav)],
                                    capture_output=True, text=True).stdout or t)
        sc["_bite"] = {"video": str(vid), "wav": str(wav), "dur": round(real, 3), "segs": segt,
                       "credit": spec["footage"][sc["clip"]["src"]].get("credit", "")}


# ---------------------------------------------------------------- 화면 (hybrid 장면 type "bite")
def _en_chunks(text: str, n: int = 78) -> list[str]:
    out, cur = [], ""
    for wd in text.split():
        if len((cur + " " + wd).strip()) > n and cur:
            out.append(cur.strip())
            cur = wd
        else:
            cur += " " + wd
    if cur.strip():
        out.append(cur.strip())
    return out


def s_bite(D, sc: dict, bt: list, dur: float):
    """앞 내레이션 동안: 원본 첫 화면을 멈춘 사진으로(어둡게, 천천히 당김) + 이름 카드 →
    말이 시작되면: 원본 영상(소리는 make 가 섞음) + 이름 자막 + 원문(영어) 한 줄 + 번역은 아래 자막."""
    import os
    import shutil as _sh
    from .hybrid import _e, W
    b = sc["_bite"]
    a = D._work / "assets"
    name = f"bite_{sc['id']:03d}.mp4"
    still = f"bite_{sc['id']:03d}.jpg"
    if not (a / name).exists() or (a / name).stat().st_size != Path(b["video"]).stat().st_size:
        try:
            if (a / name).exists():
                (a / name).unlink()
            os.link(b["video"], a / name)
        except OSError:
            _sh.copy(b["video"], a / name)
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", "0.2", "-i", b["video"], "-frames:v", "1", "-q:v", "3", str(a / still)], check=True)
    tb = sc["_bite_at"]
    bd = b["dur"]
    i = D._id()
    if tb > 0.05:   # 앞 내레이션 구간: 멈춘 첫 화면
        D.media.append(f'<div id="{i}s" style="position:absolute;inset:0;overflow:hidden"><img src="assets/{still}" '
                       f'style="width:100%;height:100%;object-fit:cover;filter:saturate(.75) brightness(.55)"></div>')
        D.js.append(f'tl.fromTo("#{i}s img",{{scale:1.0}},{{scale:1.05,duration:{tb + 0.5:.2f},ease:"none"}},0);')
        D.js.append(f'tl.to("#{i}s",{{opacity:0,duration:0.25}},{tb - 0.05:.2f});')
        who, role = sc.get("who", ""), sc.get("role", "")
        D.items.append(f'<div id="{i}c" style="position:absolute;left:0;right:0;top:400px;text-align:center;color:#fff">'
                       f'<div style="font-family:sans;font-size:30px;letter-spacing:6px;opacity:.85">직접 들어 봅니다</div>'
                       f'<div style="font-family:serif-x;font-size:84px;margin-top:18px;text-shadow:0 4px 18px rgba(0,0,0,.6)">{_e(who)}</div>'
                       f'<div style="font-family:sans;font-size:30px;margin-top:14px;opacity:.85">{_e(role)}</div></div>')
        D.js.append(f'tl.fromTo("#{i}c",{{opacity:0,y:16}},{{opacity:1,y:0,duration:0.5}},0.3);')
        D.js.append(f'tl.to("#{i}c",{{opacity:0,duration:0.25}},{tb - 0.1:.2f});')
    D.media.append(f'<div id="{i}w" style="position:absolute;inset:0;overflow:hidden;opacity:0">'
                   f'<video id="{i}" class="clip" src="assets/{name}" muted playsinline data-start="{tb:.2f}" data-duration="{bd:.2f}" '
                   f'data-track-index="2" style="width:100%;height:100%;object-fit:cover"></video></div>'
                   f'<div id="{i}g" style="position:absolute;inset:0;opacity:0;background:linear-gradient(180deg,rgba(0,0,0,.35) 0%,rgba(0,0,0,0) 18%,'
                   f'rgba(0,0,0,0) 58%,rgba(0,0,0,.6) 100%)"></div>')
    D.js.append(f'tl.set("#{i}w,#{i}g",{{opacity:1}},{tb:.2f});')
    D.js.append(f'tl.fromTo("#{i}",{{scale:1.0}},{{scale:1.04,duration:{bd:.2f},ease:"none"}},{tb:.2f});')
    D.label(" · ".join(x for x in (sc.get("label", ""), b.get("credit", "")) if x), dark=True)
    D.chapter_tag(sc.get("_chnum", ""), sc.get("_chtitle", ""), dark=True)
    D.lower(sc.get("who", ""), sc.get("role", ""), tb + 0.4, dark=True)
    if sc.get("show_en", True):   # 원문 한 줄 (번역 자막 위, 작게): 원문·번역 2단
        for s in b["segs"]:
            parts = _en_chunks(s.get("en", ""))
            if not parts:
                continue
            tot = sum(len(p) for p in parts)
            t = tb + s["t0"]
            for p in parts:
                d = (s["t1"] - s["t0"]) * len(p) / tot
                j = D._id()
                D.items.append(f'<div id="{j}" style="position:absolute;left:0;right:0;top:898px;text-align:center;opacity:0">'
                               f'<span style="font-family:sans;font-size:28px;color:#E8E8E8;background:rgba(0,0,0,.5);padding:4px 14px;border-radius:5px">'
                               f'{_e(p)}</span></div>')
                D.js.append(f'tl.set("#{j}",{{opacity:1}},{t:.2f});tl.set("#{j}",{{opacity:0}},{t + d - 0.03:.2f});')
                t += d
    for s in b["segs"][1:]:   # 점프 컷 소리
        D.sfx.append(("click-soft", tb + s["t0"]))


def register():
    from . import hybrid
    hybrid.RENDER["bite"] = s_bite
