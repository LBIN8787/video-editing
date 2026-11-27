"""삽화 + 카메라 연출 + 단어 싱크 자막 영상 렌더러 (실화 서사형 시험작).
python render.py <plan.json> [--preview 0.5] [--only 3,4] [--frames]
plan: {"art_dir","voice_dir","out","tag","shots":[...]}
shot: {"img": id | "card": {...}, "say": [첫 문장, 끝 문장], "cam": {"from":[cx,cy,w],"to":[cx,cy,w]}, "tr": "cut|dissolve|fade",
       "labels":[{"text","at":[x,y],"say":n}], "line":{"pts":[[x,y],..],"say":n,"dur":s}, "caption":"…", "nosub":false, "recon":true}
카메라 좌표는 그림 기준 0~1 (cx,cy 중심, w 폭 비율; 그림·화면 모두 16:9 라 높이 비율 = w).
"""
import json, math, subprocess, sys, pathlib, functools
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1920, 1080, 30
FONT = pathlib.Path(r"D:\ytflow\wt-books\ytflow\assets\fonts")
F = lambda name, size: ImageFont.truetype(str(FONT / name), size)
plan = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
args = sys.argv[2:]
PREVIEW = float(args[args.index("--preview") + 1]) if "--preview" in args else 1.0
tl = json.loads((pathlib.Path(plan["voice_dir"]) / "timeline.json").read_text(encoding="utf-8"))
SAYS = [e for e in tl["events"] if e["kind"] == "say"]
CHAPS = [e for e in tl["events"] if e["kind"] == "chapter"]
DUR = tl["duration"]

# ---------- 시간표: 샷 시작 = 첫 문장 시작 0.3초 전 (막 카드 뒤면 카드 끝) ----------
shots = plan["shots"]
for k, s in enumerate(shots):
    a = SAYS[s["say"][0]]["start"] - 0.3
    prev_ch = [c for c in CHAPS if c["end"] <= SAYS[s["say"][0]]["start"] + 0.01 and (k == 0 or c["start"] >= SAYS[shots[k - 1]["say"][1]]["end"] - 0.01)]
    if prev_ch: a = max(a, prev_ch[-1]["end"])
    s["t0"] = 0.0 if k == 0 else a
for k, s in enumerate(shots):
    nxt = shots[k + 1]["t0"] if k + 1 < len(shots) else DUR
    ch = [c for c in CHAPS if s["t0"] <= c["start"] < nxt]
    s["t1"] = ch[0]["start"] if ch else nxt
CHAP_SLOTS = [(c["start"], c["end"], c["title"]) for c in CHAPS]

# ---------- 그림 ----------
@functools.lru_cache(maxsize=8)
def art(name):
    im = cv2.imread(str(pathlib.Path(plan["art_dir"]) / f"{name}.png"), cv2.IMREAD_COLOR)
    return im

def ease(u):  # 부드러운 가감속 (sine in-out)
    u = min(max(u, 0.0), 1.0); return 0.5 - 0.5 * math.cos(math.pi * u)

def cam_at(s, t):
    c = s.get("cam") or {"from": [0.5, 0.5, 1.0], "to": [0.5, 0.5, 0.97]}
    u = ease((t - s["t0"]) / max(0.01, s["t1"] - s["t0"]))
    return [c["from"][i] + (c["to"][i] - c["from"][i]) * u for i in range(3)]

def frame_img(s, t):
    im = art(s["img"]); ih, iw = im.shape[:2]
    cx, cy, w = cam_at(s, t)
    cw, ch = w * iw, w * ih
    x0 = min(max(cx * iw - cw / 2, 0), iw - cw); y0 = min(max(cy * ih - ch / 2, 0), ih - ch)
    sc = W / cw
    M = np.float32([[sc, 0, -x0 * sc], [0, sc, -y0 * sc]])
    out = cv2.warpAffine(im, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
    return out, (x0, y0, sc, iw, ih)

# ---------- 글자 이미지 (RGBA) ----------
def text_rgba(lines, font, fill=(255, 255, 255), box=None, pad=(30, 14), spacing=10, align="center", shadow=False):
    d0 = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    sizes = [d0.textbbox((0, 0), l, font=font) for l in lines]
    tw = max(b[2] - b[0] for b in sizes); lh = font.size + spacing
    wimg, himg = tw + pad[0] * 2, lh * len(lines) - spacing + pad[1] * 2 + 8
    im = Image.new("RGBA", (wimg, himg), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if box: d.rounded_rectangle([0, 0, wimg - 1, himg - 1], radius=10, fill=box)
    for i, l in enumerate(lines):
        bw = sizes[i][2] - sizes[i][0]; x = pad[0] + ((tw - bw) / 2 if align == "center" else 0)
        if shadow:
            for dx, dy in ((2, 2), (0, 3)): d.text((x + dx, pad[1] + i * lh + dy), l, font=font, fill=(0, 0, 0, 170))
        d.text((x, pad[1] + i * lh), l, font=font, fill=fill)
    return np.array(im)

def paste(frame, rgba, x, y, alpha=1.0):
    h, w = rgba.shape[:2]; x, y = int(x), int(y)
    x0, y0, x1, y1 = max(x, 0), max(y, 0), min(x + w, W), min(y + h, H)
    if x1 <= x0 or y1 <= y0: return
    src = rgba[y0 - y:y1 - y, x0 - x:x1 - x]; a = src[..., 3:4].astype(np.float32) / 255 * alpha
    roi = frame[y0:y1, x0:x1].astype(np.float32)
    frame[y0:y1, x0:x1] = (roi * (1 - a) + src[..., 2::-1].astype(np.float32) * a).astype(np.uint8)

# ---------- 자막: 단어 시각으로 한 줄 22자·두 줄까지, 한 덩어리엔 한 문장만 ----------
SUBF = F("NanumGothic-Bold.ttf", 46)
import re as _re
def _norm(s): return _re.sub(r"[^\w]", "", s)
def align_tokens(e):
    """edge-tts 단어(문장부호 없음)를 원문 낱말(문장부호 있음)에 맞춤 → [[원문 낱말, 시작, 끝], …]"""
    toks = e["text"].split(); ws = e["words"]
    if len(toks) == len(ws): return [[t, w[1], w[2]] for t, w in zip(toks, ws)]
    out, j = [], 0
    for t in toks:  # 낱말 하나에 단어 여러 개가 붙거나 그 반대인 경우
        nt = _norm(t); s = e_ = None; acc = ""
        while j < len(ws) and len(acc) < len(nt):
            acc += _norm(ws[j][0]); s = ws[j][1] if s is None else s; e_ = ws[j][2]; j += 1
        if s is None: s, e_ = (out[-1][2], out[-1][2]) if out else (e["start"], e["start"])
        out.append([t, s, e_])
    return out

def chunks(e):
    out, cur = [], []
    def flush():
        if cur: out.append(cur.copy()); cur.clear()
    for w in align_tokens(e):
        if cur and len(" ".join(x[0] for x in cur + [w])) > 40: flush()
        cur.append(w)
        if w[0].endswith((".", "?", "!", "\"", "”")): flush()   # 한 자막엔 한 문장만
        elif w[0].endswith(",") and len(" ".join(x[0] for x in cur)) > 24: flush()
    flush()
    for c in out:  # 자막 끝 마침표는 뗌
        if c[-1][0].endswith("."): c[-1] = [c[-1][0][:-1]] + c[-1][1:]
    res = []
    for c in out:
        txt = " ".join(x[0] for x in c)
        if len(txt) > 22:  # 두 줄로 — 가운데 가까운 띄어쓰기에서
            ws = [x[0] for x in c]; best = min(range(1, len(ws)), key=lambda k: abs(len(" ".join(ws[:k])) - len(txt) / 2))
            lines = [" ".join(ws[:best]), " ".join(ws[best:])]
        else: lines = [txt]
        res.append({"lines": lines, "s": c[0][1], "e": c[-1][2]})
    for i in range(len(res) - 1): res[i]["e"] = max(res[i]["e"], min(res[i + 1]["s"], res[i]["e"] + 0.4))
    res[-1]["e"] += 0.3
    return res
SUBS = [c for e in SAYS for c in chunks(e)]
@functools.lru_cache(maxsize=64)
def sub_img(i): return text_rgba(SUBS[i]["lines"], SUBF, box=(15, 15, 18, 170), pad=(34, 12))

# ---------- 카드 (전체 화면) ----------
TITLEF = F("NanumMyeongjo-ExtraBold.ttf", 64); SMALLF = F("NanumGothic-Regular.ttf", 34); NAMEF = F("NanumMyeongjo-ExtraBold.ttf", 46)
def bg_dark():
    g = np.random.default_rng(7).normal(0, 6, (H, W, 1)).astype(np.float32)
    yy, xx = np.mgrid[0:H, 0:W]; v = 1 - 0.55 * (((xx - W / 2) / W) ** 2 + ((yy - H / 2) / H) ** 2) * 2.2
    base = (np.array([22, 20, 18], np.float32) * v[..., None] + g).clip(0, 255)
    return base.astype(np.uint8)
BG = bg_dark()

@functools.lru_cache(maxsize=64)
def card_frame(key):
    k = json.loads(key); fr = BG.copy(); kind = k["kind"]
    if kind == "lines":       # 질문·답: 보이는 줄만, 지난 줄은 흐리게
        ys = H / 2 - (len(k["lines"]) * 110) / 2
        for i, l in enumerate(k["lines"]):
            if i >= k["n"]: break
            col = (236, 229, 213) if i == k["n"] - 1 or not k.get("dim", True) else (120, 116, 108)
            r = text_rgba([l], TITLEF if len(l) < 26 else F("NanumMyeongjo-ExtraBold.ttf", 54), fill=col)
            paste(fr, r, (W - r.shape[1]) / 2, ys + i * 110)
    elif kind == "names":
        names = k["names"]; cols = 3
        for i, (nm, age) in enumerate(names):
            if i >= k["n"]: break
            r = text_rgba([nm, age], NAMEF, fill=(236, 229, 213))
            x = W / 2 + (i % cols - 1) * 560 - r.shape[1] / 2; y = 200 + (i // cols) * 230
            paste(fr, r, x, y)
    elif kind == "table":
        hdr = text_rgba(["가설", "설명하는 것", "설명 못 하는 것"], SMALLF, fill=(160, 152, 140))
        cols_x = [150, 760, 1250]
        for j, h in enumerate(["가설", "설명하는 것", "설명 못 하는 것"]):
            paste(fr, text_rgba([h], SMALLF, fill=(160, 152, 140), align="left"), cols_x[j], 170)
        for i, row in enumerate(k["rows"][:k["n"]]):
            for j, cell in enumerate(row):
                col = (236, 229, 213) if j == 0 else ((120, 190, 140) if cell.startswith("✓") else (225, 110, 95) if cell.startswith(("✗", "×")) else (220, 190, 120))
                paste(fr, text_rgba([cell], F("NanumGothic-Bold.ttf", 40) if j else NAMEF, fill=col, align="left"), cols_x[j], 270 + i * 190)
    elif kind == "title":
        r = text_rgba(k["lines"], F("NanumMyeongjo-ExtraBold.ttf", k.get("size", 76)), fill=(236, 229, 213), spacing=24)
        paste(fr, r, (W - r.shape[1]) / 2, (H - r.shape[0]) / 2)
    return fr

def card_state(s, t):
    c = dict(s["card"]); steps = c.get("steps")
    if steps is not None:
        c["n"] = sum(1 for st in steps if t >= SAYS[st]["start"] - 0.2)
        c.pop("steps")
    return json.dumps(c, ensure_ascii=False, sort_keys=True)

# ---------- 겹치기: 이름표·지도 선·캡션 ----------
LABF = F("NanumGothic-Bold.ttf", 34); CAPF = F("NanumMyeongjo-ExtraBold.ttf", 38); TAGF = F("NanumGothic-Bold.ttf", 26)
@functools.lru_cache(maxsize=128)
def lab_img(text, kind="label"):
    if kind == "caption": return text_rgba([text], CAPF, fill=(240, 234, 222), box=(10, 10, 12, 150), pad=(22, 10))
    if kind == "tag": return text_rgba([text], TAGF, fill=(255, 255, 255), box=(170, 50, 40, 230), pad=(16, 6))
    if kind == "recon": return text_rgba([text], F("NanumGothic-Regular.ttf", 22), fill=(230, 230, 230), box=(0, 0, 0, 110), pad=(12, 5))
    return text_rgba([text], LABF, fill=(30, 26, 22), box=(240, 232, 214, 235), pad=(16, 6), shadow=False)

@functools.lru_cache(maxsize=16)
def quote_img(text, sub):
    a = text_rgba([text], F("NanumMyeongjo-ExtraBold.ttf", 66), fill=(240, 234, 222), pad=(10, 6))
    if not sub: return a
    b = text_rgba([sub], F("NanumGothic-Regular.ttf", 30), fill=(190, 184, 172), pad=(10, 4))
    w = max(a.shape[1], b.shape[1]); im = np.zeros((a.shape[0] + b.shape[0] + 6, w, 4), np.uint8)
    im[:a.shape[0], (w - a.shape[1]) // 2:(w - a.shape[1]) // 2 + a.shape[1]] = a
    im[a.shape[0] + 6:, (w - b.shape[1]) // 2:(w - b.shape[1]) // 2 + b.shape[1]] = b
    return im

def overlays(fr, s, t, geo):
    x0, y0, sc, iw, ih = geo
    to_scr = lambda p: (p[0] * iw * sc - x0 * sc, p[1] * ih * sc - y0 * sc)
    ln = s.get("line")
    if ln and t >= SAYS[ln["say"]]["start"]:
        u = min(1.0, (t - SAYS[ln["say"]]["start"]) / ln.get("dur", 3.0)); u = ease(u)
        pts = [to_scr(p) for p in ln["pts"]]; segs = list(zip(pts, pts[1:]))
        L = sum(math.dist(a, b) for a, b in segs); goal = L * u; acc = 0
        for a, b in segs:
            d = math.dist(a, b)
            if acc >= goal: break
            f = min(1.0, (goal - acc) / d); e = (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)
            n = int(d * f / 22)
            for q in range(n + 1):
                if q % 2 == 0:
                    p1 = (a[0] + (e[0] - a[0]) * q / max(n, 1), a[1] + (e[1] - a[1]) * q / max(n, 1))
                    p2 = (a[0] + (e[0] - a[0]) * min(q + 1, n) / max(n, 1), a[1] + (e[1] - a[1]) * min(q + 1, n) / max(n, 1))
                    cv2.line(fr, tuple(map(int, p1)), tuple(map(int, p2)), (40, 60, 190), 6, cv2.LINE_AA)
            acc += d
        if u >= 1 and ln.get("end_dot", True): cv2.circle(fr, tuple(map(int, pts[-1])), 12, (40, 60, 190), -1, cv2.LINE_AA)
    for lb in s.get("labels", []):
        if t >= SAYS[lb["say"]]["start"]:
            a = min(1.0, (t - SAYS[lb["say"]]["start"]) / 0.4); r = lab_img(lb["text"]); px, py = to_scr(lb["at"])
            paste(fr, r, px - r.shape[1] / 2, py - r.shape[0] / 2, a)
    q = s.get("quote")
    if q and t >= SAYS[q["say"]]["start"] - 0.2:
        a = min(1.0, (t - SAYS[q["say"]]["start"] + 0.2) / 0.5)
        band = np.zeros((230, W, 4), np.uint8); band[..., 3] = 165
        paste(fr, band, 0, H / 2 - 175, a)
        r = quote_img(q["text"], q.get("sub", "")); paste(fr, r, (W - r.shape[1]) / 2, H / 2 - 175 + (230 - r.shape[0]) / 2, a)
    if s.get("caption"):
        a = min(1.0, (t - s["t0"]) / 0.6, max(0.0, (s["t1"] - t) / 0.4)); paste(fr, lab_img(s["caption"], "caption"), 70, 60, a)
    if s.get("recon", "img" in s):
        r = lab_img("재현 삽화", "recon"); paste(fr, r, W - r.shape[1] - 28, 26, 0.9)

# ---------- 움직임 1: GPT '전·후' 두 장을 말에 맞춰 바꾸기 ----------
def word_time(say, word):
    e = SAYS[say]
    for w in align_tokens(e):
        if word in w[0]: return w[1]
    return e["start"]

def morph(fr, s, t):
    m = s.get("morph")
    if not m: return fr
    t0 = word_time(m["say"], m.get("word", "")) + m.get("offset", 0.0); d = m.get("dur", 0.8)
    if t < t0: return fr
    if m.get("seq"):   # GPT 단계 그림 여러 장을 움짤처럼 (단계마다 step 초, 사이 0.1초 섞기)
        seq, step = m["seq"], m.get("step", 0.22); u = (t - t0) / step
        k = min(int(u), len(seq) - 1); a = min(1.0, (u - k) / 0.45) if k < len(seq) - 1 else 1.0
        cur, _ = frame_img(dict(s, img=seq[k]), t)
        if k + 1 < len(seq) and a > 0.0 and (u - k) > 0.55:
            nxt, _ = frame_img(dict(s, img=seq[k + 1]), t); b = ease(((u - k) - 0.55) / 0.45)
            cur = cv2.addWeighted(nxt, b, cur, 1 - b, 0)
        return cur
    s2 = dict(s, img=m["to"]); fr2, _ = frame_img(s2, t)
    a = ease((t - t0) / d)
    return cv2.addWeighted(fr2, a, fr, 1 - a, 0) if a < 1 else fr2

# ---------- 움직임 2: 날씨·빛 (장면이 필요로 할 때만, 은은하게) ----------
@functools.lru_cache(maxsize=32)
def particles(seed, n):
    r = np.random.default_rng(seed)
    return r.random(n), r.random(n), r.random(n)  # x, y, 크기·속도
@functools.lru_cache(maxsize=4)
def fog_tex(seed):
    r = np.random.default_rng(seed); small = r.random((9, 16)).astype(np.float32)
    big = cv2.resize(small, (W * 2, H), interpolation=cv2.INTER_CUBIC); return cv2.GaussianBlur(big, (0, 0), 60)

def weather(fr, s, t):
    for fx in s.get("fx", []):
        kind, k = (fx, 1.0) if isinstance(fx, str) else (fx[0], fx[1])
        tt = t - s["t0"]; seed = hash(s.get("img", "")) % 1000
        if kind in ("snow", "blizzard"):
            n = int((140 if kind == "snow" else 320) * k); x, y, z = particles(seed, n)
            wind = 60 if kind == "snow" else 260
            px = (x * W + tt * wind * (0.5 + z)) % W; py = (y * H + tt * (70 + 120 * z)) % H
            for i in range(n):
                cv2.circle(fr, (int(px[i]), int(py[i])), 1 + int(z[i] * 2.4), (236, 238, 240), -1, cv2.LINE_AA)
        elif kind == "spray":     # 바닷물보라·진눈깨비: 비스듬한 짧은 선
            n = int(120 * k); x, y, z = particles(seed, n)
            px = (x * W - tt * 380 * (0.6 + z)) % W; py = (y * H + tt * 520 * (0.6 + z)) % H
            for i in range(n):
                p1 = (int(px[i]), int(py[i])); p2 = (int(px[i] + 10 + 14 * z[i]), int(py[i] - 18 - 22 * z[i]))
                cv2.line(fr, p1, p2, (225, 228, 230), 1, cv2.LINE_AA)
        elif kind == "flicker":   # 촛불: 밝기가 아주 조금 흔들림
            v = 1.0 + 0.035 * k * (math.sin(tt * 7.1) * 0.6 + math.sin(tt * 12.7 + 1.3) * 0.4)
            fr[:] = np.clip(fr.astype(np.float32) * v, 0, 255).astype(np.uint8)
        elif kind == "fog":       # 낮게 흐르는 안개
            tex = fog_tex(seed); off = int(tt * 25 * k) % W
            f = tex[:, off:off + W][..., None] * 0.22 * k
            fr[:] = (fr.astype(np.float32) * (1 - f) + 235 * f).astype(np.uint8)
    return fr

def base_frame(s, t):
    if "card" in s: return card_frame(card_state(s, t)).copy(), None
    fr, geo = frame_img(s, t); fr = morph(fr, s, t); fr = weather(fr, s, t); overlays(fr, s, t, geo); return fr, geo

def render_frame(t):
    for (a, b, title) in CHAP_SLOTS:
        if a <= t < b:
            fr = card_frame(json.dumps({"kind": "title", "lines": [title], "size": 70}, ensure_ascii=False, sort_keys=True)).copy()
            al = min(1.0, (t - a) / 0.35, (b - t) / 0.35); return (fr * al).astype(np.uint8)
    k = next((i for i, s in enumerate(shots) if s["t0"] <= t < s["t1"]), None)
    if k is None: return np.zeros((H, W, 3), np.uint8)
    s = shots[k]; fr, _ = base_frame(s, t)
    tr = s.get("tr", "cut"); dt = t - s["t0"]
    if tr == "dissolve" and k > 0 and dt < 0.7 and shots[k - 1]["t1"] >= s["t0"] - 0.01:
        prev, _ = base_frame(shots[k - 1], t); a = ease(dt / 0.7)
        fr = cv2.addWeighted(fr, a, prev, 1 - a, 0)
    elif tr == "fade" and dt < 0.6: fr = (fr * ease(dt / 0.6)).astype(np.uint8)
    if s.get("fade_out") and s["t1"] - t < 0.8: fr = (fr * ease((s["t1"] - t) / 0.8)).astype(np.uint8)
    if plan.get("tag") and t < plan["tag"][1]: paste(fr, lab_img(plan["tag"][0], "tag"), 60, 40 if not s.get("caption") else 130)
    if not s.get("nosub"):
        for i, c in enumerate(SUBS):
            if c["s"] - 0.05 <= t < c["e"]:
                r = sub_img(i); paste(fr, r, (W - r.shape[1]) / 2, H - 70 - r.shape[0]); break
    return fr

# ---------- 출력 ----------
if "--frames" in args:   # 샷마다 가운데 프레임 한 장씩 (점검용)
    od = pathlib.Path(plan["out"]).parent / "check"; od.mkdir(parents=True, exist_ok=True)
    for i, s in enumerate(shots):
        for nm, tt in (("a", s["t0"] + 0.9), ("b", (s["t0"] + s["t1"]) / 2), ("c", s["t1"] - 0.2)):
            cv2.imwrite(str(od / f"{i:02d}{nm}.jpg"), render_frame(tt), [cv2.IMWRITE_JPEG_QUALITY, 85])
    print("frames", od); sys.exit()

out = pathlib.Path(plan["out"]); vw, vh = int(W * PREVIEW) // 2 * 2, int(H * PREVIEW) // 2 * 2
cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
       "-i", str(pathlib.Path(plan["voice_dir"]) / "narration.wav"),
       "-vf", f"scale={vw}:{vh}", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
       "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", str(out)]
p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
N = int(DUR * FPS)
for f in range(N):
    p.stdin.write(render_frame(f / FPS).tobytes())
    if f % (FPS * 60) == 0: print(f"{f / FPS / 60:.0f}min", flush=True)
p.stdin.close(); p.wait(); print("done", out)
