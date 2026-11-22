"""판테온 편 렌더러 (의지력 편 렌더러를 그대로 가져옴): full.json + full_overlay.html(캔버스 모션그래픽·삽화) + 박자별 목소리 → mp4.

python render_full.py <TTS 폴더> <원화 조각 폴더> <작업 폴더> <출력 mp4> [병렬 수]
  TTS 폴더: b<번호>.mp3 + b<번호>.words.json (full_voice.py — 단어별 시각)
  원화 조각 폴더: kitchen_tl.jpg … lab_br.jpg (원본 시트는 Drive 영상/20261121-curiosity-willpower/art)
자막: 단어 시각으로 한 문장 안에서 끊고, 말하는 동안만 띄운다(글자 수 비례 배분 금지 — 2026-11-21 사용자).
"""
import json, re, subprocess, sys, os
from pathlib import Path

HERE = Path(__file__).resolve().parent
FPS = 30
LEAD, TAIL = 0.45, 0.55
MADI_PRE, MADI_POST, CH_GAP = 0.7, 1.3, 0.5
SAY = {"2명이": "두 명이", "'3개": "'세 개"}   # 읽기만 바꿈(자막은 원문) — render_full.py 와 같게
norm = lambda s: re.sub(r"[^0-9A-Za-z가-힣]", "", s)


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True).stdout)


def word_times(text, toks):
    """원문 낱말마다 (시작, 끝). TTS 단어 경계 글자열과 원문 글자열을 difflib 로 맞춘다
    (edge-tts 경계가 글자를 빠뜨리거나 겹쳐 내는 일이 있어 — 판테온 v2 '하나. 철'·'균열. 연 | 열. 연' — 차례 맞춤은 뒤가 밀림)."""
    import difflib
    sc, st = "", []   # TTS 글자·글자마다 (시작, 끝)
    for a, b, w in toks:
        t = norm(w); sc += t; L = max(len(t), 1)
        st += [(a + (b - a) * j / L, a + (b - a) * (j + 1) / L) for j in range(len(t))]   # 한 경계 안에서만 글자로 나눔(문장 전체 비례 배분 아님)
    words = text.split()
    oc, own = "", []
    for i, w in enumerate(words):
        sw = w
        for k, v in SAY.items():
            sw = sw.replace(k, v)
        t = norm(sw); oc += t; own += [i] * len(t)
    m = {}
    for blk in difflib.SequenceMatcher(None, oc, sc, autojunk=False).get_matching_blocks():
        for k in range(blk.size):
            m[blk.a + k] = blk.b + k
    out = [None] * len(words)
    for i in range(len(words)):
        idx = [m[c] for c, o in enumerate(own) if o == i and c in m]
        if idx:
            out[i] = (st[min(idx)][0], st[max(idx)][1])
    if len(m) < len(oc):
        print("  ! 글자 맞춤", len(oc) - len(m), "자 못 맞춤", text[:30])
    last = (0, 0)
    for i in range(len(out)):   # 못 맞춘 낱말(문장부호만 등)은 앞 낱말 끝에 붙임
        if out[i] is None:
            out[i] = (last[1], last[1])
        last = out[i]
    return words, out


def sub_chunks(words, wt, n=30):
    """문장 단위로 나눈 뒤, 27자를 넘는 문장은 고른 길이로 나눔(끝에 한 낱말만 남지 않게, 쉼표 뒤를 먼저). [시작, 끝, 글]"""
    import math
    sents, cur = [], []
    for i, w in enumerate(words):
        cur.append(i)
        if re.search(r"[.?!]['’”]?$", w):
            sents.append(cur); cur = []
    if cur:
        sents.append(cur)
    res = []
    for sn in sents:
        # 나눔 자리 고르기(동적 계획): 줄마다 n자 이하, 줄 길이는 고르게, 쉼표 뒤에서 끊으면 가산점, 짧은 꼬리 줄은 벌점
        m = len(sn); L = len(" ".join(words[i] for i in sn)); k = max(1, math.ceil(L / n)); target = L / k
        seg = lambda a, b: len(" ".join(words[sn[x]] for x in range(a, b)))
        best = [0.0] + [math.inf] * m; prev = [0] * (m + 1)
        for b in range(1, m + 1):
            for a in range(b):
                l = seg(a, b)
                if l > n and b - a > 1:
                    continue
                c = (l - target) ** 2 + (400 if l < 9 else 0) - (60 if words[sn[b - 1]].endswith(",") and b < m else 0)
                if best[a] + c < best[b]:
                    best[b], prev[b] = best[a] + c, a
        cuts, b = [], m
        while b > 0:
            cuts.append((prev[b], b)); b = prev[b]
        for a, b in reversed(cuts):
            ids = sn[a:b]
            res.append([wt[ids[0]][0], wt[ids[-1]][1], " ".join(words[x] for x in ids)])
    for k in range(len(res) - 1):   # 다음 자막과 0.35초 안쪽이면 이어 붙여 깜빡임 없앰
        if res[k + 1][0] - res[k][1] < 0.35:
            res[k][1] = res[k + 1][0]
    return res


def timeline(spec, tts):
    t, prev_ch = 0.0, None
    for sc in spec["scenes"]:
        f = tts / f"b{sc['id']:02d}.mp3"
        if sc.get("silent"):   # 소리 없는 장 표지·카드
            d, f = float(sc["silent"]), None
            words, wt = [], []
        else:
            d = dur(f)
            toks = json.loads(f.with_suffix(".words.json").read_text(encoding="utf-8"))
            words, wt = word_times(sc["text"], toks)
        madi = sc["mg"] == "madi"
        lead = LEAD + (MADI_PRE if madi else 0) + (CH_GAP if prev_ch is not None and sc["ch"] != prev_ch else 0)
        if sc.get("silent"):
            lead = 0.0
        # kw: 그 낱말을 말하기 시작하는 시각(장면 안 초)
        K = []
        for k in sc.get("kw", []):
            ci = sc["text"].index(k); wi = len(sc["text"][:ci].split()) - (0 if sc["text"][:ci].endswith(" ") or ci == 0 else 1)
            K.append(round(lead + wt[max(wi, 0)][0], 3))
        sc["_K"] = K
        sc["_subs"] = [] if (madi or sc.get("silent")) else [[round(lead + a, 3), round(lead + b + 0.12, 3), s] for a, b, s in sub_chunks(words, wt)]
        sc["_A"] = {"file": str(f) if f else None, "t": lead, "d": d}
        sc["_D"] = lead + d + (0 if sc.get("silent") else TAIL) + (MADI_POST if madi else 0) + float(sc.get("hold", 0))   # hold: 시청자가 직접 해 보는 시간
        sc["_T0"] = t
        t += sc["_D"]; prev_ch = sc["ch"]
    return t


def frames_of(spec, total):
    sc_list, fr, si = spec["scenes"], [], 0
    for f in range(int(round(total * FPS))):
        T = f / FPS
        while si < len(sc_list) - 1 and T >= sc_list[si + 1]["_T0"]:
            si += 1
        sc = sc_list[si]; lt = T - sc["_T0"]; sub = ""
        for a, b, s in sc["_subs"]:
            if a <= lt <= b:
                sub = s
        fr.append([si, round(lt, 4), sub])
    return fr


def worker(job_path, k, n):
    from playwright.sync_api import sync_playwright
    job = json.loads(Path(job_path).read_text(encoding="utf-8"))
    fr = job["frames"]; per = (len(fr) + n - 1) // n; a, b = k * per, min(len(fr), (k + 1) * per)
    out = Path(job["work"]) / f"seg_{k:02d}.mp4"
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "image2pipe", "-framerate", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p", str(out)], stdin=subprocess.PIPE)
    with sync_playwright() as pw:
        br = pw.chromium.launch(); pg = br.new_page(viewport={"width": 1920, "height": 1080})
        pg.goto((HERE / os.environ.get("OVERLAY", "full_overlay.html")).as_uri())
        pg.evaluate("(a)=>INIT(a[0],a[1])", [job["scenes"], Path(job["art"]).resolve().as_uri()])
        pg.wait_for_function("window.READY===true", timeout=60000)
        for i in range(a, b):
            si, lt, sub = fr[i]
            pg.evaluate("(a)=>R(a[0],a[1],a[2])", [si, lt, sub])
            ff.stdin.write(pg.screenshot(type="jpeg", quality=93))
            if (i - a) % 600 == 0:
                print(f"[{k}] {i - a}/{b - a}", flush=True)
        br.close()
    ff.stdin.close(); ff.wait()


def main(tts, art, work, out, n=6):
    tts, work, out, n = Path(tts), Path(work), Path(out), int(n)
    work.mkdir(parents=True, exist_ok=True)
    spec = json.loads((HERE / os.environ.get("SPEC", "full.json")).read_text(encoding="utf-8"))
    total = timeline(spec, tts)
    print(f"총 {total:.1f}초 ({total / 60:.1f}분)")
    scenes = [{"data": {k: v for k, v in s.items() if not k.startswith("_")}, "K": s["_K"], "D": s["_D"], "A": s["_A"]["t"],
               "AD": s["_A"]["d"]} for s in spec["scenes"]]
    job = {"frames": frames_of(spec, total), "scenes": scenes, "art": str(art), "work": str(work)}
    jp = work / "job.json"; jp.write_text(json.dumps(job, ensure_ascii=False), encoding="utf-8")
    # 검토용 기록 (git): 장면 시각·자막
    (HERE.parent / "05_edit").mkdir(exist_ok=True)
    (HERE.parent / "05_edit" / os.environ.get("TIMELINE", "full_timeline.json")).write_text(json.dumps(
        [{"id": s["id"], "ch": s["ch"], "t0": round(s["_T0"], 2), "dur": round(s["_D"], 2), "mg": s["mg"],
          "kw": dict(zip(s.get("kw", []), s["_K"])), "subs": s["_subs"]} for s in spec["scenes"]], ensure_ascii=False, indent=1), encoding="utf-8")

    # 소리: 박자별 목소리를 제 자리에
    ins, flt = [], []
    k = 0
    for s in spec["scenes"]:
        if not s["_A"]["file"]:
            continue
        ins += ["-i", s["_A"]["file"]]; ms = int((s["_T0"] + s["_A"]["t"]) * 1000)
        flt.append(f"[{k}:a]aresample=48000,adelay={ms}|{ms}[a{k}]"); k += 1
    m = k
    flt.append("".join(f"[a{k}]" for k in range(m)) + f"amix=inputs={m}:normalize=0,loudnorm=I=-15:TP=-1.5:LRA=9,apad[aout]")
    audio = work / "audio.m4a"
    subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(flt), "-map", "[aout]", "-t", f"{total:.3f}",
                    "-c:a", "aac", "-b:a", "192k", str(audio)], check=True)

    if os.environ.get("ONLY_TIMING"):
        return
    ps = [subprocess.Popen([sys.executable, __file__, "--worker", str(jp), str(k), str(n)]) for k in range(n)]
    for p in ps:
        p.wait()
    (work / "segs.txt").write_text("".join(f"file '{(work / f'seg_{k:02d}.mp4').as_posix()}'\n" for k in range(n)))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(work / "segs.txt"), "-i", str(audio),
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "copy", "-shortest", "-movflags", "+faststart", str(out)], check=True)
    print("완료", out)


if __name__ == "__main__":
    if sys.argv[1] == "--worker":
        worker(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
    else:
        main(*sys.argv[1:])
