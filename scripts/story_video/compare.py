"""레퍼런스 ↔ 재현 대조: (1) 문장마다 같은 순간(문장 시작 + 1.2초)의 프레임을 나란히 (2) 같은 방식으로 잰 숫자 비교.
python compare.py <remake.json> <ref_dir> <ours.mp4> <ours_voice_dir> <out_dir> [ref_end_sec]"""
import json, sys, subprocess, pathlib, math, statistics as st, collections
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont
R = json.load(open(sys.argv[1], encoding="utf-8")); REF = pathlib.Path(sys.argv[2]); OURS = sys.argv[3]
V = pathlib.Path(sys.argv[4]); OUT = pathlib.Path(sys.argv[5]); OUT.mkdir(parents=True, exist_ok=True)
END = float(sys.argv[6]) if len(sys.argv) > 6 else 320.0
FONT = r"D:\ytflow\wt-books\ytflow\assets\fonts\NanumGothic-Bold.ttf"
lines = [ln for sec in R["sections"] for ln in sec["lines"]]
says = [e for e in json.load(open(V / "timeline.json", encoding="utf-8"))["events"] if e["kind"] == "say"]

def grab(src, t, dst):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", str(src), "-frames:v", "1", "-vf", "scale=640:360", str(dst)])

# (1) 나란히
pairs = []
for i, ln in enumerate(lines):
    rt = ln["ref_t"] + 1.2; ot = says[i]["start"] + 1.2
    a, b = OUT / f"r{i:03d}.jpg", OUT / f"o{i:03d}.jpg"; grab(REF / "ref360.mp4", rt, a); grab(OURS, ot, b)
    pairs.append((i, rt, ot, a, b, ln["say"]))
f = ImageFont.truetype(FONT, 20); per = 8
for p in range(0, len(pairs), per):
    grp = pairs[p:p + per]; sheet = Image.new("RGB", (1300, len(grp) * 392), (18, 18, 18)); d = ImageDraw.Draw(sheet)
    for k, (i, rt, ot, a, b, say) in enumerate(grp):
        y = k * 392
        sheet.paste(Image.open(a), (0, y + 30)); sheet.paste(Image.open(b), (660, y + 30))
        d.text((6, y + 4), f"#{i:02d} 레퍼런스 {int(rt)//60}:{rt%60:04.1f}", font=f, fill=(255, 220, 90))
        d.text((666, y + 4), f"재현 {int(ot)//60}:{ot%60:04.1f}  · {say[:30]}…", font=f, fill=(140, 220, 255))
    sheet.save(OUT / f"pairs_{p // per:02d}.jpg", quality=84)

# (2) 같은 방식으로 재기: 0.5초 프레임 → 특징점 일치로 장면 경계·카메라
def measure(src, end):
    tmp = OUT / ("m_" + pathlib.Path(src).stem); tmp.mkdir(exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-t", str(end), "-i", str(src), "-vf", "fps=2,scale=320:180", "-q:v", "3", str(tmp / "%05d.jpg")])
    fs = sorted(tmp.glob("*.jpg")); orb = cv2.ORB_create(600); bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True); rows = []
    prev = None
    for i, fn in enumerate(fs):
        g = cv2.imread(str(fn), 0); k, dsc = orb.detectAndCompute(g, None)
        inl, sc, dx = 0, 1.0, 0.0
        if prev and dsc is not None and prev[1] is not None and len(k) > 10 and len(prev[0]) > 10:
            m = bf.match(prev[1], dsc)
            if len(m) >= 8:
                p0 = np.float32([prev[0][x.queryIdx].pt for x in m]); p1 = np.float32([k[x.trainIdx].pt for x in m])
                M, mask = cv2.estimateAffinePartial2D(p0, p1, ransacReprojThreshold=3)
                if M is not None: inl = int(mask.sum()); sc = float(np.hypot(M[0, 0], M[1, 0])); dx = float(M[0, 2])
        rows.append({"t": i * 0.5, "inl": inl if i else 99, "sc": sc, "dx": dx, "mean": float(g.mean())}); prev = (k, dsc)
    b = [r["t"] for r in rows if r["inl"] < 25 and r["mean"] > 12]; bounds = []
    for t in b:
        if not bounds or t - bounds[-1][-1] > 1.0: bounds.append([t])
        else: bounds[-1].append(t)
    cuts = [0.0] + [x[0] for x in bounds] + [rows[-1]["t"]]; kinds = []
    for a, c in zip(cuts, cuts[1:]):
        seg = [r for r in rows if a + 0.6 <= r["t"] <= c - 0.4 and r["inl"] >= 25]
        z = math.prod(r["sc"] for r in seg) if seg else 1.0; dx = sum(r["dx"] for r in seg)
        kinds.append("밀기" if z > 1.04 else "빼기" if z < 0.96 else "이동" if abs(dx) > 25 else "정지")
    durs = [c - a for a, c in zip(cuts, cuts[1:])]
    c = collections.Counter(kinds); n = len(kinds)
    return {"샷 수": n, "샷 길이 중앙(초)": round(st.median(durs), 1), "정지 %": round(c["정지"] / n * 100), "밀기 %": round(c["밀기"] / n * 100),
            "빼기 %": round(c["빼기"] / n * 100), "이동 %": round(c["이동"] / n * 100), "어두운 화면(초)": sum(r["mean"] < 12 for r in rows) * 0.5}
ref_end = END; our_end = says[-1]["end"] + 1.0
m_ref, m_our = measure(REF / "ref360.mp4", ref_end), measure(OURS, our_end)
chars = sum(len(ln["say"]) for ln in lines)
m_ref["말 속도(자/분)"] = round(sum(len(x[2]) for x in json.load(open(REF / "ref_subs.json", encoding="utf-8")) if x[0] < ref_end) / ref_end * 60)
m_our["말 속도(자/분)"] = round(chars / our_end * 60)
json.dump({"ref": m_ref, "ours": m_our}, open(OUT / "metrics.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({"ref": m_ref, "ours": m_our}, ensure_ascii=False, indent=1))
