"""4.5단계: 소스 클립 확보 — 대본에 적힌 원본 영상 구간만 잘라 받는다.

scene["source"] 형식:
  {"url": "https://www.youtube.com/watch?v=...",
   "start": "1:02.5", "end": "1:25",          # 구간을 알면 직접 지정
   "find": "Naver", "length": 12,              # 모르면 자막에서 키워드를 찾아 시작점 결정
   "pre": 1.0}                                 # find 로 찾은 지점보다 몇 초 앞에서 시작할지

결과: 04_assets/scene_XXX.mp4 (원본 오디오 포함) + 04_assets/clips.csv (성공/실패/구간)
  - YouTube 가 아닌 URL(기사·공시) → 헤드라인 부분 캡처 scene_XXX_shot.png (ytflow/assets/capture.js)
  - YouTube 클립을 못 받으면 → 그 영상의 공개 썸네일로 '임시' 정지화면 scene_XXX_temp.jpg
    (가편집에서 흐름을 보기 위한 것. 업로드 전 반드시 실제 클립으로 교체)

주의
  - YouTube 는 클라우드 서버 IP 의 영상 다운로드를 자주 막는다. 개인 PC 에서 실행하는 것을 권장.
    봇 확인이 뜨면 config/pipeline.yaml 의 clips.cookies_from_browser 에 "chrome" 등을 적는다.
  - 받을 수 없으면 clips.csv 에 URL·구간이 남으므로 직접 받아 같은 파일명으로 넣으면 된다.
  - 타 채널 영상은 저작권 대상이다. 짧게 인용하고 출처 라벨을 반드시 단다 (label 필드).
"""
from __future__ import annotations

import json
import csv
import re
import sys
import subprocess
from pathlib import Path

from .. import config, yt
from ..project import Project


def to_sec(t) -> float | None:
    if t is None or t == "":
        return None
    if isinstance(t, (int, float)):
        return float(t)
    parts = [float(x) for x in str(t).split(":")]
    s = 0.0
    for p in parts:
        s = s * 60 + p
    return s


def _vid(url: str) -> str:
    m = re.search(r"(?:v=|youtu\.be/|shorts/)([\w-]{11})", url)
    return m.group(1) if m else url


def resolve(src: dict, work: Path) -> tuple[float, float, str]:
    """(start, end, 메모) — find 가 있으면 자막에서 첫 등장 위치를 찾는다."""
    start, end = to_sec(src.get("start")), to_sec(src.get("end"))
    if start is not None and end is not None:
        return start, end, "지정 구간"
    if src.get("find"):
        lang = src.get("lang", "en")
        vtt = yt.download_subs(_vid(src["url"]), work, lang)
        if vtt:
            for c in yt.parse_vtt(vtt):
                if re.search(src["find"], c["text"], re.I):
                    st = max(0.0, c["start"] - float(src.get("pre", 1.0)))
                    return st, st + float(src.get("length", 10)), f"자막에서 '{src['find']}' 발견 ({c['text'][:40]})"
            return 0, 0, f"자막에 '{src['find']}' 없음"
        return 0, 0, "자막 없음"
    return 0, 0, "start/end 또는 find 필요"


def download(url: str, start: float, end: float, out: Path) -> bool:
    ccfg = config.load("pipeline").get("clips", {})
    cmd = [sys.executable, "-m", "yt_dlp", "--no-warnings", "--js-runtimes", "node",
           "-f", ccfg.get("format", "bv*[height<=1080]+ba/b[height<=1080]/b"),
           "--download-sections", f"*{start:.2f}-{end:.2f}", "--force-keyframes-at-cuts",
           "--merge-output-format", "mp4", "-o", str(out), url]
    if ccfg.get("cookies_from_browser"):
        cmd[3:3] = ["--cookies-from-browser", ccfg["cookies_from_browser"]]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0 or not out.exists():
        print("    ", (proc.stderr.strip().splitlines() or ["?"])[-1][:160])
        return False
    return True


def is_youtube(url: str) -> bool:
    return bool(re.search(r"(youtube\.com|youtu\.be)/", url))


def capture(url: str, out: Path) -> tuple[bool, str]:
    js = Path(__file__).resolve().parent.parent / "assets" / "capture.js"
    if re.match(r"https?://(x|twitter)\.com/[^/]+/status/\d+", url):
        # X 게시물: 공식 임베드(oEmbed) HTML 을 받아 브라우저로 그린 뒤 캡처 (로그인·스크래핑 없음)
        import json as _j
        import urllib.parse
        import urllib.request
        try:
            api = "https://publish.x.com/oembed?omit_script=1&lang=ko&url=" + urllib.parse.quote(url, safe="")
            with urllib.request.urlopen(urllib.request.Request(api, headers={"User-Agent": "ytflow/0.1"}), timeout=20) as r:
                o = _j.loads(r.read())
        except Exception as e:
            return False, f"X 임베드 실패: {str(e)[:80]}"
        html = out.with_suffix(".embed.html")
        html.write_text(o.get("html", ""), encoding="utf-8")
        proc = subprocess.run(["node", str(js), "--embed", str(html), str(out)], capture_output=True, text=True, timeout=90)
        html.unlink(missing_ok=True)
        msg = (proc.stdout.strip().splitlines() or [proc.stderr.strip()[-120:]])[-1]
        return proc.returncode == 0 and out.exists(), f"{msg} @{o.get('author_name', '')}"
    proc = subprocess.run(["node", str(js), url, str(out)], capture_output=True, text=True, timeout=90)
    msg = (proc.stdout.strip().splitlines() or [proc.stderr.strip()[-120:]])[-1]
    return proc.returncode == 0 and out.exists(), msg


def temp_still(src: dict, out: Path) -> bool:
    """공개 썸네일(i.ytimg.com)로 임시 정지화면. 구간 위치에 가까운 자동 프레임(hq1~3)을 고른다."""
    import urllib.request
    from PIL import Image, ImageDraw, ImageFont

    vid = _vid(src["url"])
    st = to_sec(src.get("start")) or 0
    names = ["maxresdefault", "hq1", "hq2", "hq3"] if st < 30 else ["hq2", "hq1", "hq3", "maxresdefault"]
    for n in names:
        try:
            with urllib.request.urlopen(f"https://i.ytimg.com/vi/{vid}/{n}.jpg", timeout=15) as r:
                data = r.read()
            tmp = out.with_suffix(".dl")
            tmp.write_bytes(data)
            im = Image.open(tmp).convert("RGB")
            tmp.unlink()
            w, h = im.size
            if h / w > 0.7:  # 4:3 썸네일의 위아래 검은 띠 제거
                im = im.crop((0, int(h * 0.125), w, int(h * 0.875)))
            im = im.resize((1920, 1080))
            d = ImageDraw.Draw(im)
            fp = Path(__file__).resolve().parent.parent / "assets" / "fonts" / "NanumGothic-Bold.ttf"
            f = ImageFont.truetype(str(fp), 30) if fp.exists() else ImageFont.load_default()
            d.rectangle([1920 - 470, 20, 1900, 72], fill=(0, 0, 0))
            d.text((1920 - 455, 30), "임시 화면 · 실제 클립으로 교체", font=f, fill=(255, 210, 60))
            im.save(out, quality=92)
            return True
        except Exception:
            continue
    return False


def run(project: Project) -> None:
    scenes = project.read_json("script", "scenes.json")["scenes"]
    adir = project.dir("assets")
    work = adir / "work_subs"
    rows, ok = [], 0
    invf = project.dir("source") / "inventory.json"
    photos = {x["url"]: x for x in json.loads(invf.read_text(encoding="utf-8"))} if invf.exists() else {}
    for s in scenes:
        src = s.get("source")
        if not src or not src.get("url"):
            continue
        ph = photos.get(src["url"])
        if ph and ph.get("kind") == "photo" and ph.get("image"):  # 위키미디어 공용 사진(CC): 원본 이미지를 받는다
            shot = adir / f"scene_{s['id']:03d}_shot.jpg"
            try:
                import urllib.request
                req = urllib.request.Request(ph["image"], headers={"User-Agent": "ytflow/1.0 (YouTube research pipeline)"})
                shot.write_bytes(urllib.request.urlopen(req, timeout=30).read())
                rows.append([s["id"], "PHOTO", src["url"], "", "", f"{ph.get('artist', '')} · {ph.get('license', '')}", ph["title"]])
                ok += 1
                print(f"[clips] #{s['id']} PHOTO {ph['title'][:40]} ({ph.get('license')})")
            except Exception as e:
                rows.append([s["id"], "FAILED", src["url"], "", "", "", f"사진 받기 실패: {e}"])
            continue
        if not is_youtube(src["url"]):
            shot = adir / f"scene_{s['id']:03d}_shot.png"
            good, msg = (True, "기존 캡처") if shot.exists() else capture(src["url"], shot)
            ok += good
            rows.append([s["id"], "SHOT" if good else "FAILED", src["url"], "", "", s.get("label", ""), msg])
            print(f"[clips] #{s['id']} {'SHOT' if good else 'FAILED'} {msg}")
            continue
        out = adir / f"scene_{s['id']:03d}.mp4"
        if out.exists():
            rows.append([s["id"], "OK(기존)", src["url"], "", "", s.get("label", ""), ""])
            ok += 1
            continue
        st, en, memo = resolve(src, work)
        from . import align
        quote = s.get("kind") == "quote" and s.get("quote_en") and align.available()
        if quote:  # 원본 발언: 앞뒤 3초 여유를 두고 받은 뒤 단어 단위로 다시 자른다
            st, en = max(0.0, st - 3.0), en + 3.0
        good = en > st and download(src["url"], st, en, out)
        if good and quote:
            fixed, note = align.refine(out, s["quote_en"])
            memo += f" / {note}"
        ok += good
        if not good and temp_still(src, adir / f"scene_{s['id']:03d}_temp.jpg"):
            memo += " / 임시 썸네일 사용"
        rows.append([s["id"], "OK" if good else "FAILED", src["url"], f"{st:.1f}", f"{en:.1f}", s.get("label", ""), memo])
        print(f"[clips] #{s['id']} {'OK' if good else 'FAILED'} {st:.1f}-{en:.1f}s {memo}")
    with open(adir / "clips.csv", "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(["scene", "status", "url", "start_sec", "end_sec", "label", "memo"])
        w.writerows(rows)
    print(f"[clips] {ok}/{len(rows)}개 확보 → {adir}/clips.csv (실패한 구간은 직접 받아 scene_XXX.mp4 로 넣어도 됩니다)")
    project.mark_done("clips")
