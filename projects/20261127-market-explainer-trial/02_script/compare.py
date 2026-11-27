"""기존 영상 구간과 시안 대조 (같은 목소리라 같은 시각끼리 맞댐).
사용: python compare.py <기존 구간.mp4> <시안.mp4> <출력폴더> [--at 5,20,...]
결과: side_by_side.mp4 · pairs_N.jpg(같은 시각 프레임) · motion.json(1초 간격 움직임)"""
import argparse, json, pathlib, subprocess
from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageStat
ap = argparse.ArgumentParser(); ap.add_argument("orig"); ap.add_argument("new"); ap.add_argument("out"); ap.add_argument("--at", default="5,12,18,24,31,36,40,50,56,62,72,77,84,89,97,100,107,111,117,123,127")
a = ap.parse_args(); OUT = pathlib.Path(a.out); OUT.mkdir(parents=True, exist_ok=True)
F = ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf", 26)

def frame(src, t, w=800):
    p = OUT / "_f.png"; subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(t), "-i", src, "-frames:v", "1", "-vf", f"scale={w}:-1", str(p)], check=True)
    return Image.open(p).convert("RGB")
def tag(im, s):
    d = ImageDraw.Draw(im); d.rectangle([0, 0, d.textlength(s, font=F) + 14, 36], fill=(229, 83, 75)); d.text((7, 2), s, font=F, fill="white"); return im
rows = []
for t in map(float, a.at.split(",")):
    x, y = tag(frame(a.orig, t), f"기존 {t:.0f}s"), tag(frame(a.new, t), f"시안 {t:.0f}s")
    r = Image.new("RGB", (1610, x.height), "white"); r.paste(x, (0, 0)); r.paste(y, (810, 0)); rows.append(r)
for i in range(0, len(rows), 7):
    part = rows[i:i + 7]; sh = Image.new("RGB", (1610, sum(r.height + 8 for r in part)), "white"); yy = 0
    for r in part: sh.paste(r, (0, yy)); yy += r.height + 8
    sh.save(OUT / f"pairs_{i // 7 + 1}.jpg", quality=86)

def motion(src, tag_):
    d = OUT / f"_m_{tag_}"; d.mkdir(exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-vf", "fps=1,scale=160:90", str(d / "%04d.png")], check=True)
    prev, out = None, []
    for f in sorted(d.glob("*.png")):
        im = Image.open(f).convert("L")
        if prev: out.append(ImageStat.Stat(ImageChops.difference(im, prev)).mean[0])
        prev = im
    run = m = 0
    for v in out: run = run + 1 if v < .5 else 0; m = max(m, run)
    n = len(out); big = sum(v >= 4 for v in out)
    return {"초": n, "정지 비율": round(sum(v < .5 for v in out) / n, 2), "큰 변화 간격(초)": round(n / max(1, big), 1), "가장 긴 정지(초)": m, "평균 변화량": round(sum(out) / n, 2), "곡선": [round(v, 1) for v in out]}
res = {"기존": motion(a.orig, "orig"), "시안": motion(a.new, "new")}
(OUT / "motion.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
for k, v in res.items(): print(k, {x: y for x, y in v.items() if x != "곡선"})
lb = Image.new("RGB", (1920, 40), (28, 32, 36)); d = ImageDraw.Draw(lb)
d.text((12, 4), "기존 (다모다란 편 2장, 2:52~)", font=F, fill="white"); d.text((972, 4), "시안 (해설 연출 + 시장 규칙, 같은 목소리)", font=F, fill="white"); lb.save(OUT / "_lb.png")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", a.orig, "-i", a.new, "-loop", "1", "-i", str(OUT / "_lb.png"), "-filter_complex",
                "[0:v]scale=960:540,setsar=1[x];[1:v]scale=960:540,setsar=1[y];[x][y]hstack,pad=1920:580:0:40:color=0x1C2024[s];[s][2:v]overlay=0:0:shortest=1[v]",
                "-map", "[v]", "-map", "1:a", "-c:v", "libx264", "-crf", "24", "-preset", "fast", "-c:a", "aac", "-b:a", "128k", "-shortest", str(OUT / "side_by_side.mp4")], check=True)
print("done")
