"""S6 샘플 영상 (30~60초+): 콜드 오픈 + 사건 개요 + 마지막 질문. 초안 목소리 edge-tts.
문장마다: 음성 → 길이 측정 → 화면(삽화 켄 번스 / 사건 파일 카드 / 검은 화면) + 자막 → 이어 붙임."""
import asyncio, json, math, os, random, subprocess
from pathlib import Path
import edge_tts
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(r"G:\내 드라이브\ytflow\영상\20261126-history-sohyeon")
S = ROOT / "samples"
WORK = Path(__file__).parent / "sv"
WORK.mkdir(exist_ok=True)
W, H, FPS = 1920, 1080, 30
F_SUB = ImageFont.truetype(r"C:\Windows\Fonts\malgunbd.ttf", 44)
F_SER = ImageFont.truetype(r"C:\Windows\Fonts\batang.ttc", 54)
F_SER_S = ImageFont.truetype(r"C:\Windows\Fonts\batang.ttc", 34)
F_STAMP = ImageFont.truetype(r"C:\Windows\Fonts\malgunbd.ttf", 40)
F_BIG = ImageFont.truetype(r"C:\Windows\Fonts\malgunbd.ttf", 64)
VOICE, RATE = "ko-KR-InJoonNeural", "-12%"
RED = (150, 28, 28)

# (문장, 화면 종류, 화면 값, 자막 여부, 뒤 쉼 초)
BEATS = [
    ("1645년 4월, 창경궁 환경당.", "img", ("A1_yeomseup", "date:1645년 4월 · 창경궁 환경당 · 재현"), True, 0.6),
    ("촛불 아래, 세상을 떠난 사람의 몸을 씻기고 옷을 입히는 염습이 시작됩니다.", "img", ("A1_yeomseup", ""), True, 0.3),
    ("누워 있는 사람은 조선의 왕세자. 서른셋.", "img", ("A1_yeomseup", ""), True, 0.4),
    ("그 방에 들어갔던 종친 집안 사람 하나가, 훗날 이렇게 전했습니다.", "img", ("A1_yeomseup", ""), True, 1.0),
    ("온몸이 전부 검은빛이었고, 이목구비의 일곱 구멍에서는 모두 선혈이 흘러나왔다.", "quote", 1, False, 0.6),
    ("마치 약물에 중독되어 죽은 사람과 같았다.", "quote", 2, False, 1.2),
    ("나라의 공식 역사, 조선왕조실록에 남은 문장입니다.", "black", "조선왕조실록", False, 0.5),
    ("그리고 이 죽음은, 380년이 넘도록 풀리지 않았습니다.", "file", "cover", False, 1.2),
    ("사건을 먼저 정리해 보겠습니다.", "file", 0, True, 0.3),
    ("죽은 사람. 소현세자. 왕 인조의 맏아들, 다음 왕이 될 사람이었습니다.", "file", 1, False, 0.2),
    ("때. 1645년 음력 4월 26일. 곳. 창경궁 환경당.", "file", 3, False, 0.2),
    ("청나라에서 8년을 지내고 돌아온 지 두 달 남짓. 4월 23일에 앓아눕고, 나흘째 되던 날 숨을 거둡니다.", "file", 4, False, 1.0),
    ("1644년 가을, 베이징의 천문대에서 둥근 지구의를 받아 들었던 세자.", "img", ("A3_observatory", "date:1644년 가을 · 베이징 천문대 · 재현"), True, 0.5),
    ("그날 환경당에서 그를 데려간 것은 병이었을까요, 독이었을까요.", "img", ("A3_observatory", ""), True, 0.8),
    ("여러분의 판정은 어느 쪽입니까.", "black", "판정: 미해결", False, 2.5),
]


async def tts(i, text):
    p = WORK / f"a{i:02d}.mp3"
    if not p.exists():
        await edge_tts.Communicate(text, VOICE, rate=RATE).save(str(p))
    return p


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True).stdout)


def wrap(text, font, width, draw):
    lines, cur = [], ""
    for ch in text.split(" "):
        t = (cur + " " + ch).strip()
        if draw.textlength(t, font=font) > width and cur:
            lines.append(cur); cur = ch
        else:
            cur = t
    return lines + [cur]


def subtitle(img, text):
    d = ImageDraw.Draw(img, "RGBA")
    lines = wrap(text, F_SUB, 1500, d)
    lh = 60; total = lh * len(lines) + 30
    y0 = H - 70 - total
    wmax = max(d.textlength(l, font=F_SUB) for l in lines)
    d.rounded_rectangle([(W - wmax) / 2 - 30, y0, (W + wmax) / 2 + 30, y0 + total], 12, fill=(10, 10, 14, 170))
    for k, l in enumerate(lines):
        d.text((W / 2, y0 + 15 + k * lh + lh / 2), l, font=F_SUB, fill="white", anchor="mm")


def stamp(img, text, xy, color=RED, angle=-8):
    t = Image.new("RGBA", (900, 140), (0, 0, 0, 0)); d = ImageDraw.Draw(t)
    tw = d.textlength(text, font=F_STAMP)
    d.rounded_rectangle([10, 20, tw + 50, 115], 10, outline=color + (230,), width=6)
    d.text((30, 67), text, font=F_STAMP, fill=color + (230,), anchor="lm")
    t = t.rotate(angle, expand=True, resample=Image.BICUBIC)
    img.paste(t, xy, t)


def paper(w, h, seed=1):
    random.seed(seed)
    p = Image.new("RGB", (w, h), (214, 200, 164))
    noise = Image.effect_noise((w, h), 22).convert("L")
    p = Image.blend(p, Image.merge("RGB", [noise] * 3).point(lambda v: v * 0.9 + 20), 0.12)
    return p


def desk():
    bg = Image.new("RGB", (W, H), (18, 20, 26))
    vign = Image.new("L", (W, H), 0); ImageDraw.Draw(vign).ellipse([-300, -200, W + 300, H + 200], fill=255)
    return Image.composite(bg, Image.new("RGB", (W, H), (6, 6, 9)), vign.filter(ImageFilter.GaussianBlur(200)))


def quote_card(stage):
    img = desk(); p = paper(1500, 780, 3); img.paste(p, (210, 130)); d = ImageDraw.Draw(img)
    d.text((270, 175), "인조실록 46권 · 인조 23년(1645) 6월 27일", font=F_SER_S, fill=(90, 70, 50))
    lines = ["온몸이 전부 검은빛이었고,", "이목구비의 일곱 구멍에서는", "모두 선혈이 흘러나왔다."]
    y = 280
    for l in lines:
        d.text((300, y), l, font=F_SER, fill=(40, 30, 25)); y += 90
    if stage >= 2:
        l = "마치 약물에 중독되어 죽은 사람과 같았다."
        d.text((300, y + 30), l, font=F_SER, fill=(40, 30, 25))
        x0 = 300 + d.textlength("마치 약물에 ", font=F_SER); x1 = x0 + d.textlength("중독되어", font=F_SER)
        d.line([x0, y + 100, x1, y + 100], fill=RED, width=7)
        stamp(img, "기록 확인", (1300, 700))
    return img


def file_card(stage):
    img = desk(); p = paper(1400, 900, 7); img.paste(p, (260, 90)); d = ImageDraw.Draw(img)
    if stage == "cover":
        d.text((W / 2, 380), "사건 파일 001", font=F_SER, fill=(60, 45, 35), anchor="mm")
        d.text((W / 2, 520), "소현세자의 죽음", font=F_BIG, fill=(30, 22, 18), anchor="mm")
        d.text((W / 2, 640), "1645 · 조선 · 창경궁", font=F_SER_S, fill=(90, 70, 50), anchor="mm")
        stamp(img, "미해결", (1180, 720), angle=-12)
        return img
    d.text((330, 140), "사건 개요", font=F_SER, fill=(30, 22, 18))
    rows = [("죽은 사람", "소현세자 — 인조의 맏아들, 왕세자"), ("때", "1645년 음력 4월 26일"), ("곳", "창경궁 환경당"),
            ("경과", "2월 18일 귀국 → 4월 23일 앓아누움 → 4월 26일 죽음")]
    y = 270
    for k, (a, b) in enumerate(rows):
        d.line([330, y + 85, 1590, y + 85], fill=(150, 130, 100), width=2)
        d.text((340, y + 22), a, font=ImageFont.truetype(r"C:\Windows\Fonts\malgunbd.ttf", 36), fill=(95, 70, 45))
        if k < stage:
            d.text((560, y + 15), b, font=ImageFont.truetype(r"C:\Windows\Fonts\batang.ttc", 40), fill=(30, 22, 18))
        y += 120
    return img


def black(text):
    img = Image.new("RGB", (W, H), (4, 4, 6)); d = ImageDraw.Draw(img)
    if text == "판정: 미해결":
        d.text((W / 2, H / 2), "판정 :", font=F_BIG, fill=(220, 215, 205), anchor="rm")
        d.text((W / 2 + 30, H / 2), "미해결", font=F_BIG, fill=(190, 40, 40), anchor="lm")
    else:
        d.text((W / 2, H / 2), text, font=F_SER, fill=(220, 215, 205), anchor="mm")
    return img


def kenburns(src, out, seconds, z0, z1, overlay_fn):
    """원화를 크게 잘라 z0→z1 로 천천히 확대 (프레임 PNG 대신 ffmpeg zoompan)."""
    still = WORK / (out.stem + "_base.png")
    im = Image.open(src).convert("RGB").resize((W, H))
    overlay_fn(im); im.save(still)
    n = max(1, int(seconds * FPS))
    zexpr = f"{z0}+({z1}-{z0})*on/{n}"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", str(still), "-vf",
                    f"scale=3840:-1,zoompan=z='{zexpr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}:fps={FPS},format=yuv420p",
                    "-frames:v", str(n), str(out)], check=True)


def still_clip(img, out, seconds):
    p = WORK / (out.stem + ".png"); img.save(p)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", str(p), "-t", f"{seconds:.3f}", "-r", str(FPS),
                    "-vf", "format=yuv420p", str(out)], check=True)


async def main():
    audios = [await tts(i, b[0]) for i, b in enumerate(BEATS)]
    # 같은 삽화가 이어지는 구간은 확대를 이어서 (켄 번스가 끊기지 않게)
    segs, zoom_state = [], {}
    total_by_img = {}
    for i, b in enumerate(BEATS):
        if b[1] == "img":
            total_by_img[b[2][0]] = total_by_img.get(b[2][0], 0) + dur(audios[i]) + b[4]
    for i, (text, kind, val, sub, pause) in enumerate(BEATS):
        a = audios[i]; sec = dur(a) + pause
        v = WORK / f"v{i:02d}.mp4"
        if kind == "img":
            name, tag = val
            done = zoom_state.get(name, 0.0); tot = total_by_img[name]
            z0 = 1.0 + 0.12 * done / tot; z1 = 1.0 + 0.12 * (done + sec) / tot
            zoom_state[name] = done + sec
            def ov(im, tag=tag, text=text, sub=sub):
                if tag.startswith("date:"):
                    d = ImageDraw.Draw(im, "RGBA"); t = tag[5:]
                    F_D = ImageFont.truetype(r"C:\Windows\Fonts\malgunbd.ttf", 38)
                    d.rectangle([60, 60, 60 + d.textlength(t, font=F_D) + 40, 128], fill=(0, 0, 0, 160))
                    d.text((80, 94), t, font=F_D, fill=(235, 225, 200), anchor="lm")
                if sub: subtitle(im, text)
            kenburns(S / f"{name}.png", v, sec, z0, z1, ov)
        else:
            img = quote_card(val) if kind == "quote" else file_card(val) if kind == "file" else black(val)
            if sub: subtitle(img, text)
            still_clip(img, v, sec)
        # 음성 + 쉼
        aw = WORK / f"w{i:02d}.wav"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(a), "-af", f"apad=pad_dur={pause}", "-ar", "48000", "-ac", "2", str(aw)], check=True)
        segs.append((v, aw, sec))
    lst = WORK / "list.txt"
    vs = WORK / "video.mp4"; aud = WORK / "audio.wav"
    lst.write_text("".join(f"file '{s[0].as_posix()}'\n" for s in segs), encoding="utf-8")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(vs)], check=True)
    al = WORK / "alist.txt"; al.write_text("".join(f"file '{s[1].as_posix()}'\n" for s in segs), encoding="utf-8")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(al), str(aud)], check=True)
    out = ROOT / "sample.mp4"
    # 낮은 배경 울림(저음 사인파) — 저작권 문제 없는 임시 소리
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(vs), "-i", str(aud),
                    "-f", "lavfi", "-i", "sine=frequency=55:sample_rate=48000",
                    "-filter_complex", "[2:a]volume=0.035,afade=t=in:d=2[bg];[1:a][bg]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-16:TP=-1.5[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-crf", "20", "-c:a", "aac", "-b:a", "192k", "-shortest", str(out)], check=True)
    print("saved", out, round(sum(s[2] for s in segs), 1), "s")


asyncio.run(main())
