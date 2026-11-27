"""원본 도입부와 시험작 대조: 나란히 영상 · 박자 맞춘 프레임 대조표 · 1초 간격 움직임 지표.
사용: python compare.py <원본.mp4> <시험작.mp4> <출력폴더>
원본 박자 시각은 레퍼런스 자막(ref.ko.vtt)에서 읽은 값, 시험작은 timeline.json."""
import json, pathlib, subprocess, sys
from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageStat

HERE = pathlib.Path(__file__).parent
ORIG, OURS, OUT = map(pathlib.Path, sys.argv[1:4]); OUT.mkdir(parents=True, exist_ok=True)
FONT = ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf", 30)
# 원본 박자 시작(초): 자막 시간표에서 같은 내용이 시작하는 지점
ORIG_BEATS = {"article": 1.5, "lift": 6.9, "quote": 10.9, "axis": 17.4, "scrub": 20.2, "p1": 26.0, "p2": 29.0, "p3": 33.0,
              "p4": 35.0, "p5": 38.0, "below": 43.0, "internal": 46.0, "band": 51.0, "face": 57.0, "cap": 60.0,
              "q1": 65.0, "q2": 70.0, "hello": 76.0}
ours_beats = {l["id"]: l["start"] for l in json.loads((HERE / "timeline.json").read_text(encoding="utf-8"))["lines"]}

def frame(src, t, w=640):
    p = OUT / "_f.png"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", str(src), "-frames:v", "1", "-vf", f"scale={w}:-1", str(p)], check=True)
    return Image.open(p).convert("RGB")

def label(img, text):
    d = ImageDraw.Draw(img); d.rectangle([0, 0, d.textlength(text, font=FONT) + 16, 40], fill=(31, 74, 90)); d.text((8, 2), text, font=FONT, fill="white"); return img

# 1) 박자 맞춘 대조표: 박자 시작 + 1.8초 장면
rows = []
for k, ot in ORIG_BEATS.items():
    a = label(frame(ORIG, ot + 1.8), f"원본 {ot + 1.8:.0f}s · {k}"); b = label(frame(OURS, ours_beats[k] + 1.8), f"시험작 {ours_beats[k] + 1.8:.0f}s")
    r = Image.new("RGB", (1290, a.height), "white"); r.paste(a, (0, 0)); r.paste(b, (650, 0)); rows.append(r)
for i in range(0, len(rows), 6):
    part = rows[i:i + 6]; sheet = Image.new("RGB", (1290, sum(r.height + 10 for r in part)), "white"); y = 0
    for r in part: sheet.paste(r, (0, y)); y += r.height + 10
    sheet.save(OUT / f"beats_{i // 6 + 1}.jpg", quality=88)

# 2) 1초 간격 움직임 지표
def motion(src, dur):
    d = OUT / f"_m_{src.stem}"; d.mkdir(exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-t", str(dur), "-i", str(src), "-vf", "fps=1,scale=160:90", str(d / "%04d.png")], check=True)
    fs = sorted(d.glob("*.png")); prev = None; out = []
    for f in fs:
        im = Image.open(f).convert("L")
        if prev: out.append(ImageStat.Stat(ImageChops.difference(im, prev)).mean[0])
        prev = im
    run = m = 0
    for v in out: run = run + 1 if v < .5 else 0; m = max(m, run)
    n = len(out)
    return {"초": n, "정지 비율": round(sum(v < .5 for v in out) / n, 2), "작은 변화 비율": round(sum(.5 <= v < 4 for v in out) / n, 2),
            "큰 변화 횟수(≥4)": sum(v >= 4 for v in out), "큰 변화 간격(초)": round(n / max(1, sum(v >= 4 for v in out)), 1),
            "가장 긴 정지(초)": m, "평균 변화량": round(sum(out) / n, 2), "곡선": [round(v, 1) for v in out]}
tl_total = json.loads((HERE / "timeline.json").read_text(encoding="utf-8"))["lines"][-1]["start"]
res = {"원본": motion(ORIG, 76), "시험작": motion(OURS, tl_total)}
(OUT / "motion.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
for k, v in res.items(): print(k, {a: b for a, b in v.items() if a != "곡선"})

# 3) 나란히 영상(원본 왼쪽 · 시험작 오른쪽, 소리는 시험작), 같은 시각끼리 재생
lb = Image.new("RGB", (1920, 40), (31, 74, 90)); d = ImageDraw.Draw(lb)
d.text((12, 2), "원본 (AI 특이점, 0:00~)", font=FONT, fill="white"); d.text((972, 2), "시험작 (singularity-explainer, 소리는 이쪽)", font=FONT, fill="white"); lb.save(OUT / "_lb.png")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-t", "84", "-i", str(ORIG), "-t", "84", "-i", str(OURS), "-loop", "1", "-i", str(OUT / "_lb.png"), "-filter_complex",
                "[0:v]scale=960:540,setsar=1,tpad=stop_mode=clone:stop_duration=10[a];[1:v]scale=960:540,setsar=1[b];[a][b]hstack,pad=1920:580:0:40:color=0xFAF9F2[s];[s][2:v]overlay=0:0:shortest=1[v]",
                "-map", "[v]", "-map", "1:a", "-c:v", "libx264", "-crf", "22", "-preset", "fast", "-c:a", "aac", "-t", "84", str(OUT / "side_by_side.mp4")], check=True)
print("done")
