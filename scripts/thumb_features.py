"""thumb_research.py 결과의 썸네일·제목 특징을 재고, 같은 채널 안에서 터진 영상(hit) vs 안 된 영상(low)을 비교한다.
    python scripts/thumb_features.py [.cache/thumbs/<날짜>]
출력: <폴더>/features.json, summary.md, 채널별 비교 시트 sheets/<채널>.jpg (커밋 안 함)
"""
import json, re, statistics, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2

ROOT = Path(__file__).resolve().parents[1]
D = Path(sys.argv[1]) if len(sys.argv) > 1 else sorted((ROOT / ".cache" / "thumbs").iterdir())[-1]
FONT = ROOT / "ytflow" / "assets" / "fonts" / "NanumGothic-Bold.ttf"
face = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


def img_feats(p):
    im = Image.open(p).convert("RGB")
    a = np.asarray(im)[45:315]          # hqdefault 480x360 의 위아래 검은 띠 자르기
    hsv = cv2.cvtColor(a, cv2.COLOR_RGB2HSV)
    h, s, v = hsv[..., 0].astype(int), hsv[..., 1] / 255, hsv[..., 2] / 255
    rg = a[..., 0].astype(int) - a[..., 1]; yb = (a[..., 0].astype(int) + a[..., 1]) / 2 - a[..., 2]
    colorful = float(np.sqrt(rg.std() ** 2 + yb.std() ** 2) + 0.3 * np.sqrt(rg.mean() ** 2 + yb.mean() ** 2))
    vivid = (s > 0.5) & (v > 0.4)
    yellow = float((vivid & (h >= 18) & (h <= 35)).mean()); red = float((vivid & ((h <= 8) | (h >= 170))).mean())
    gray = cv2.cvtColor(a, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    faces = face.detectMultiScale(gray, 1.1, 5, minSize=(30, 30))
    fa = max((w * hh for (_, _, w, hh) in faces), default=0) / gray.size
    # 글자 추정: 아주 밝거나 아주 진한 큰 대비 + 가로로 촘촘한 가장자리
    return {"bright": round(float(v.mean()), 3), "sat": round(float(s.mean()), 3), "contrast": round(float(gray.std() / 255), 3),
            "colorful": round(colorful, 1), "yellow": round(yellow, 4), "red": round(red, 4), "edge": round(float((edges > 0).mean()), 4),
            "faces": int(len(faces)), "face_area": round(fa, 4)}


def title_feats(t):
    return {"len": len(t), "num": bool(re.search(r"\d", t)), "q": "?" in t, "quote": bool(re.search(r"[\"'“”‘’]", t)),
            "pipe": "|" in t, "neg": bool(re.search(r"폭락|위기|붕괴|망|끝|경고|위험|최악|몰락|급락|파산", t)),
            "money": bool(re.search(r"억|조|만원|원|달러|%", t)), "why": bool(re.search(r"왜|이유", t)),
            "you": bool(re.search(r"당신|여러분|지금 당장|꼭|반드시", t))}


rows = json.loads((D / "videos.json").read_text())
feat = []
for r in rows:
    p = D / "img" / f"{r['id']}.jpg"
    if r["group"] not in ("hit", "low") or not p.exists():
        continue
    feat.append({**r, **img_feats(p), **{"t_" + k: v for k, v in title_feats(r["title"] or "").items()}})
(D / "features.json").write_text(json.dumps(feat, ensure_ascii=False, indent=0))

# 같은 채널 안 비교: 채널마다 hit 평균 - low 평균, 그 차이의 중앙값과 '같은 방향' 채널 수
keys = ["bright", "sat", "contrast", "colorful", "yellow", "red", "edge", "faces", "face_area"] + [k for k in feat[0] if k.startswith("t_")]
by = {}
for f in feat:
    by.setdefault(f["channel"], {"hit": [], "low": []})[f["group"]].append(f)
L = ["# 썸네일·제목 특징 — 같은 채널 안 터진 영상(중앙값 3배+) vs 안 된 영상(0.5배 이하)", "",
     f"폴더 {D.name} · 채널 {len(by)} · 영상 hit {sum(f['group']=='hit' for f in feat)} / low {sum(f['group']=='low' for f in feat)}", "",
     "| 특징 | hit 평균 | low 평균 | 채널별 차이 중앙값 | hit 가 큰 채널 / 비교 가능 |", "|---|---|---|---|---|"]
for k in keys:
    hv = [float(f[k]) for f in feat if f["group"] == "hit"]; lv = [float(f[k]) for f in feat if f["group"] == "low"]
    diffs = [statistics.mean(float(x[k]) for x in g["hit"]) - statistics.mean(float(x[k]) for x in g["low"]) for g in by.values() if g["hit"] and g["low"]]
    up = sum(d > 0 for d in diffs)
    L.append(f"| {k} | {statistics.mean(hv):.3f} | {statistics.mean(lv):.3f} | {statistics.median(diffs):+.3f} | {up} / {len(diffs)} |")
L += ["", "## 채널별 터진 영상 (배수 높은 순)", ""]
for ch, g in by.items():
    L.append(f"### {ch}")
    for f in sorted(g["hit"], key=lambda x: -x["x"])[:6]:
        L.append(f"- ×{f['x']} · {f['views']:,} · {f['title']}")
    L.append("")
(D / "summary.md").write_text("\n".join(L))

# 채널별 비교 시트: 위 줄 hit 상위 6, 아래 줄 low 하위 6
(D / "sheets").mkdir(exist_ok=True)
fnt = ImageFont.truetype(str(FONT), 16)
for ch, g in by.items():
    hs = sorted(g["hit"], key=lambda x: -x["x"])[:6]; ls = sorted(g["low"], key=lambda x: x["x"])[:6]
    if not hs or not ls:
        continue
    W, Hh = 320, 180
    S = Image.new("RGB", (W * 6, (Hh + 26) * 2 + 30), (20, 20, 20)); d = ImageDraw.Draw(S)
    d.text((6, 4), f"{ch} — 위: 터진 영상(배수) / 아래: 안 된 영상", font=fnt, fill=(255, 255, 255))
    for row, lst in enumerate((hs, ls)):
        for i, f in enumerate(lst):
            im = Image.open(D / "img" / f"{f['id']}.jpg").convert("RGB").crop((0, 45, 480, 315)).resize((W, Hh))
            y = 30 + row * (Hh + 26)
            S.paste(im, (i * W, y))
            d.text((i * W + 4, y + Hh + 3), f"×{f['x']}  {f['views']:,}", font=fnt, fill=(255, 220, 80) if row == 0 else (170, 170, 170))
    S.save(D / "sheets" / (re.sub(r"[^\w가-힣]+", "_", ch)[:30] + ".jpg"), quality=85)
print(D / "summary.md")
