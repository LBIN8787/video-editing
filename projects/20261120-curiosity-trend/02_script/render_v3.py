"""넘기기 편 v3 렌더러 — 삽화, 모션그래픽, 실제 사진, 무음 마디.

python render_v3.py <클립 폴더> <TTS 폴더> none <작업 폴더> <출력 mp4>
  TTS 폴더: s<장면>_<박자>.mp3. 삽화와 사진: ARTDIR.
"""
import json, os, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
FONTS = ROOT / "ytflow" / "assets" / "fonts"
W, H, FPS = 1920, 1080, 30
LEAD, GAP, TAIL = 0.35, 0.35, 0.6
try:   # 실사 색보정은 화풍 목록에서 (edit.yaml look.footage, 기본 warm-doc — styles/looks.yaml)
    sys.path.insert(0, str(ROOT))
    from ytflow.stages import looks as _looks
    GRADE = _looks.footage_vf(HERE.parent)
except Exception:
    GRADE = ""
GRADE = GRADE or "eq=contrast=1.06:saturation=0.82:gamma=0.97,colorbalance=rs=0.03:bs=-0.03:rh=0.02:bh=-0.03,vignette=PI/4.5,noise=alls=5:allf=t"
EXTRA = {4: (0.0, 0.6), 5: (0.2, 0.9), 7: (0.0, 0.8), 8: (0.0, 1.6)}   # 장면별 (앞, 뒤) 여유 더하기


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True).stdout)


def chunks(text, n=30):
    out, cur = [], ""
    for w in re.split(r"(?<=,)\s+|\s+", text.strip()):
        if cur and len(cur) + 1 + len(w) > n:
            out.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        out.append(cur)
    return out


def sub_chunks(text, n=28):
    out = []
    for s in re.split(r"(?<=[.?!])\s+", text.strip()):   # 한 자막에 두 문장이 걸치지 않게
        out += chunks(s, n)
    return out


def char_times(mp3, text):
    """s02_0.mp3 옆 s02_0.align.json (ElevenLabs) → text 의 글자마다 (시작, 끝) 초. 글자가 안 맞으면 None."""
    a = Path(mp3).with_name(Path(mp3).stem + ".align.json")
    if not a.exists():
        return None
    d = json.loads(a.read_text(encoding="utf-8"))
    s = "".join(d["characters"])
    off = s.find(text)
    if off < 0:
        return None
    st, en = d["character_start_times_seconds"], d["character_end_times_seconds"]
    return [(st[off + i], en[off + i]) for i in range(len(text))]


def timeline(spec, tts):
    t = 0.0
    for sc in spec["scenes"]:
        pre, post = sc.get("pad", (0, 0))
        lt = LEAD + pre
        sc["_B"] = []
        if sc.get("silent"):   # 마디: 목소리 없이 검은 화면 한 줄
            sc["_B"] = [{"t": 0.0, "d": float(sc["silent"]), "kw": [], "file": None, "abs": t, "subs": []}]
            sc["_D"] = float(sc["silent"])
            sc["_T0"] = t
            t += sc["_D"]
            continue
        for i, text in enumerate(sc["beats"]):
            f = tts / f"s{sc['id']:02d}_{i}.mp3"
            d = dur(f)
            at = char_times(f, text)   # ElevenLabs 글자별 시각 (있으면 정확, 없으면 글자 수 비례)
            pos = lambda k: (lt + at[k][0]) if at else lt + d * k / len(text)
            kws = [pos(max(text.find(k), 0)) for k in (sc.get("kw") or [[]] * len(sc["beats"]))[i]]
            subs, cur = [], 0
            for p in sub_chunks(text):   # 자막: 문장을 넘지 않게 자르고, 실제로 그 말을 하는 동안만
                k = text.find(p, cur); k = cur if k < 0 else k; e = k + len(p) - 1; cur = e + 1
                end = (lt + at[e][1] + 0.2) if at else lt + d * cur / len(text)
                subs.append([pos(k), p, end])
            for a, b in zip(subs, subs[1:]):   # 다음 자막과 겹치지 않게
                a[2] = min(a[2], b[0])
            sc["_B"].append({"t": lt, "d": d, "kw": kws, "file": str(f), "abs": t + lt, "subs": subs})
            lt += d + GAP
        sc["_D"] = lt - GAP + TAIL + post
        sc["_T0"] = t
        t += sc["_D"]
    return t


def footage(sc, clips, work):
    out = work / f"bg_{sc['id']:02d}.mp4"
    D = sc["_D"]
    if out.exists() and abs(dur(out) - D) < 0.1:
        return out
    if sc.get("feed"):   # 휴대폰 피드 합성: 흐린 실사 바탕 + 가운데 세로 화면 안에서 실제 클립이 위로 넘어감
        f = sc["feed"]
        x, y, w, h = f["x"], f["y"], f["w"], f["h"]
        n = len(f["clips"]); X = 0.3
        seg = (D + X * (n - 1)) / n
        ins, fl = [], []
        ins += ["-ss", str(f.get("bg_start", 0)), "-i", str(clips / f"{f['bg']}.mp4")]
        fl.append(f"[0:v]setpts=1.3*PTS,fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},{GRADE},boxblur=14,eq=brightness=-0.18,"
                  f"tpad=stop_mode=clone:stop_duration=20,trim=duration={D:.3f},setsar=1[bg]")
        for k, (cid, st) in enumerate(f["clips"]):
            ins += ["-stream_loop", "-1", "-ss", str(st), "-i", str(clips / f"{cid}.mp4")]
            fl.append(f"[{k+1}:v]fps={FPS},scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},{GRADE},"
                      f"tpad=stop_mode=clone:stop_duration=10,trim=duration={seg:.3f},setsar=1,settb=AVTB[c{k}]")
        prev = "c0"
        for k in range(1, n):
            fl.append(f"[{prev}][c{k}]xfade=transition=slideup:duration={X}:offset={seg * k - X * k:.3f}[x{k}]")
            prev = f"x{k}"
        fl.append(f"[bg][{prev}]overlay={x}:{y}:shortest=1,trim=duration={D:.3f}[v]")
        subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fl), "-map", "[v]", "-an",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p", str(out)], check=True)
        return out
    if sc["kind"] != "footage":
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=black:s={W}x{H}:r={FPS}:d={D:.3f}",
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out)], check=True)
        return out
    parts = sc.get("clips") or [[sc["clip"], sc["start"], 1.0]]
    if sc.get("beat_clips"):   # 박자마다 클립: 박자 시작 시각으로 나눔
        cuts = [0.0] + [b["t"] - 0.15 for b in sc["_B"][1:]] + [D]
        parts = [[c[0], c[1], (cuts[i + 1] - cuts[i]) / D] for i, c in enumerate(sc["beat_clips"])]
    segs = []
    for j, (cid, st, share) in enumerate(parts):
        d = D * share
        slow = sc.get("slow", 1.0)
        pre = "crop=1080:608:0:(ih-608)/2," if sc.get("vertical") else ""
        dirn = 1 if (sc["id"] + j) % 2 else -1
        x = f"(iw-{W})/2+{dirn}*(iw-{W})/2*(t/{d:.2f}-0.5)"
        vf = (f"{pre}setpts={slow}*PTS,fps={FPS},scale=2040:1148:force_original_aspect_ratio=increase,"
              f"crop={W}:{H}:'{x}':(ih-{H})/2,"
              + GRADE)
        if sc.get("blur"):
            vf += f",boxblur={sc['blur']}"
        if sc.get("dim"):
            vf += f",eq=brightness=-{sc['dim'] * 0.35:.3f}"
        vf += f",tpad=stop_mode=clone:stop_duration=10,trim=duration={d:.3f},setsar=1"
        seg = work / f"bg_{sc['id']:02d}_{j}.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-stream_loop", "-1", "-ss", str(st), "-i", str(clips / f"{cid}.mp4"), "-an", "-vf", vf,
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p", str(seg)], check=True)
        segs.append(seg)
    lst = work / f"bg_{sc['id']:02d}.txt"
    lst.write_text("".join(f"file '{s}'\n" for s in segs))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(out)], check=True)
    return out


def main(clips, tts, bgm, work, out):
    clips, tts, work, out = (Path(path).resolve() for path in (clips, tts, work, out))
    work.mkdir(parents=True, exist_ok=True)
    out.parent.mkdir(parents=True, exist_ok=True)
    spec = json.loads((HERE / "v3.json").read_text(encoding="utf-8"))
    art_dir = Path(os.environ.get("ARTDIR", ".")).resolve()
    for scene in spec["scenes"]:
        if art := scene.get("art"):
            art["ok"] = (art_dir / f"{art['sheet']}_{art['q']}.jpg").is_file()
        if photo := scene.get("photo"):
            scene["photoOk"] = (art_dir / photo).is_file()
    total = timeline(spec, tts)
    print(f"총 {total:.1f}초", flush=True)
    flat = all(scene["kind"] != "footage" and not scene.get("feed") for scene in spec["scenes"])
    base = work / "base.mp4"
    if not flat:
        bgs = [footage(sc, clips, work) for sc in spec["scenes"]]
        (work / "bg.txt").write_text("".join(f"file '{b.as_posix()}'\n" for b in bgs), encoding="utf-8")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(work / "bg.txt"), "-c", "copy", str(base)], check=True)

    # 소리: 내레이션 + 잔잔한 배경음(목소리 밑으로 낮춤)
    narr_in, flt = [], []
    for sc in spec["scenes"]:
        for b in sc["_B"]:
            if not b["file"]:
                continue
            k = len(narr_in) // 2
            narr_in += ["-i", b["file"]]
            ms = int(b["abs"] * 1000)
            flt.append(f"[{k}:a]aresample=48000,adelay={ms}|{ms}[a{k}]")
    n = len(narr_in) // 2
    flt.append("".join(f"[a{k}]" for k in range(n)) + f"amix=inputs={n}:normalize=0,volume=1.0[nar]")
    use_bgm = str(bgm).lower() != "none"   # 배경음 없음이 기본 (사용자 2026-11-20: "배경음은 그냥 빼줘")
    if use_bgm:
        flt.append(f"[{n}:a]aresample=48000,volume=0.16,afade=t=in:d=1.5,afade=t=out:st={total - 3:.2f}:d=3[bgm]")
        flt.append("[nar][bgm]amix=inputs=2:normalize=0,loudnorm=I=-15:TP=-1.5:LRA=9[aout]")
    else:
        flt.append("[nar]loudnorm=I=-15:TP=-1.5:LRA=9,apad[aout]")
    audio = work / "audio.m4a"
    subprocess.run(["ffmpeg", "-v", "error", "-y", *narr_in, *(["-stream_loop", "-1", "-i", str(bgm)] if use_bgm else []), "-filter_complex", ";".join(flt),
                    "-map", "[aout]", "-t", f"{total:.3f}", "-c:a", "aac", "-b:a", "192k", str(audio)], check=True)

    # 그래픽 층: 프레임마다 그려서 실사 위에 겹침
    html = (HERE / "v3_overlay.html").read_text(encoding="utf-8")
    html = html.replace("FONTDIR", FONTS.as_uri()).replace("ARTDIR", art_dir.as_uri())
    html = html.replace("THUMBDIR", Path(os.environ.get("THUMBDIR", ".")).resolve().as_uri())
    page_file = work / "overlay.html"
    page_file.write_text(html, encoding="utf-8")
    scenes = spec["scenes"]
    frames, si = [], 0
    for f in range(int(round(total * FPS))):
        T = f / FPS
        while si < len(scenes) - 1 and T >= scenes[si + 1]["_T0"]:
            si += 1
        sc = scenes[si]
        t = T - sc["_T0"]
        sub = ""
        for b in sc["_B"]:
            if b["t"] - 0.05 <= t <= b["t"] + b["d"] + 0.15:
                for st, txt, *en in b["subs"]:
                    if st - 0.05 <= t <= (en[0] if en else 1e9):
                        sub = txt
        frames.append([si, round(t, 4), sub])
    job = {"frames": frames, "scenes": [{"data": {k: v for k, v in s.items() if not k.startswith("_")}, "B": s["_B"], "D": s["_D"]} for s in scenes]}
    (work / "frames.json").write_text(json.dumps(job, ensure_ascii=False), encoding="utf-8")
    image_input = ["-f", "image2pipe", "-framerate", str(FPS)]
    if flat:
        image_input += ["-c:v", "mjpeg"]
        inputs = [*image_input, "-i", "-", "-i", str(audio), "-map", "0:v", "-map", "1:a",
                  "-vf", "scale=in_range=pc:out_range=tv,format=yuv420p"]
    else:
        inputs = ["-i", str(base), *image_input, "-i", "-", "-i", str(audio),
                  "-filter_complex", "[0:v][1:v]overlay=0:0:format=auto,format=yuv420p[v]",
                  "-map", "[v]", "-map", "2:a"]
    pending = out.with_name(f"{out.stem}.rendering{out.suffix}")
    command = ["node", str(HERE / "sample_frames.mjs"), str(work / "frames.json"), str(page_file)]
    if flat:
        command.append("jpeg")
    with subprocess.Popen(command, stdout=subprocess.PIPE) as shot:
        enc = subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-c:v", "libx264", "-preset", "fast",
                              "-crf", "18", "-c:a", "copy", "-shortest", "-movflags", "+faststart", str(pending)],
                             stdin=shot.stdout)
        shot.stdout.close()
        shot_status = shot.wait()
    enc.check_returncode()
    if shot_status:
        raise subprocess.CalledProcessError(shot_status, command)
    pending.replace(out)
    # 장면 시각 기록 (검토용)
    (work / "timeline.json").write_text(json.dumps([{"id": s["id"], "t0": round(s["_T0"], 2), "dur": round(s["_D"], 2),
                                                     "kind": s["kind"], "mg": s.get("mg")} for s in scenes], ensure_ascii=False, indent=1))
    print("완료", out)


if __name__ == "__main__":
    main(*sys.argv[1:6])
