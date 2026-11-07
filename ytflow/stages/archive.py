"""공공 기록 영상·사진 (역사·교양 주제의 '자료 화면').

클라우드에서 막히지 않고, 저작권 걱정이 없는 곳만 씁니다.
- 미국 의회도서관(LoC) loc.gov JSON API: 사진(photos)·영화(film-and-videos).
  1930년 이전 발행물은 미국에서 퍼블릭 도메인. 사진은 대부분 'No known restrictions'.
  항목마다 rights 를 저장하고, 'copyright' 표기가 있으면 쓰지 않습니다.
- NASA images-api (퍼블릭 도메인) — media.py/clips 쪽에서 사용.

사진은 still_to_clip() 으로 16:9 무음 영상(세로 사진은 흐린 배경 채움)으로 바꿔
hybrid.json 의 footage 에 넣습니다. 하이브리드 렌더러가 천천히 다가가는 움직임을 더합니다.

    python -m ytflow archive search "influenza 1918" [--films]
"""
from __future__ import annotations

import json
import subprocess
import time
import urllib.parse
import urllib.request
from pathlib import Path

UA = {"User-Agent": "ytflow (research; contact via repo)"}


def _get(url: str, timeout: int = 40) -> bytes:
    for k in range(4):  # LoC 는 빠르게 여러 번 부르면 429
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read()
        except Exception as e:  # noqa: BLE001
            if k == 3:
                raise
            time.sleep(4 * (k + 1))
    return b""


def loc_search(term: str, films: bool = False, n: int = 12) -> list[dict]:
    kind = "film-and-videos" if films else "photos"
    d = json.loads(_get(f"https://www.loc.gov/{kind}/?q={urllib.parse.quote(term)}&fo=json&c={n}"))
    out = []
    for r in d.get("results", [])[:n]:
        im = r.get("image_url") or []
        out.append({"title": r.get("title", ""), "date": r.get("date", ""), "item": r.get("id"),
                    "image": im[-1].split("#")[0] if im else ""})
    return out


def loc_item(item_url: str) -> dict:
    """항목의 권리 표기와 내려받을 파일(가장 큰 jpg 또는 mp4)."""
    d = json.loads(_get(item_url.replace("http://", "https://").rstrip("/") + "/?fo=json"))
    it = d.get("item", {})
    rights = it.get("rights_advisory") or it.get("rights") or ""
    rights = " ".join(rights) if isinstance(rights, list) else str(rights)
    files = [x for r in d.get("resources", []) for f in r.get("files", []) for x in f]
    mp4 = [x for x in files if (x.get("url") or "").endswith(".mp4")]
    jpg = sorted([x for x in files if (x.get("url") or "").endswith(".jpg")], key=lambda x: x.get("width") or 0)
    best = (mp4 or jpg[-1:] or [{}])[0] if mp4 else (jpg[-1] if jpg else {})
    return {"title": it.get("title"), "date": it.get("date"), "rights": rights[:400], "url": best.get("url"),
            "usable": "copyright" not in rights.lower() or "no known" in rights.lower() or "not aware of any" in rights.lower()}


def download(url: str, out: Path) -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(_get(url, timeout=300))
    return out


def still_to_clip(img: Path, out: Path, dur: float = 30.0, tone: str = "") -> Path:
    """사진 → 1920x1080 무음 영상. 가로 사진은 꽉 채우고, 세로 사진은 흐린 배경 위에 가운데."""
    from PIL import Image
    w, h = Image.open(img).size
    if w / h >= 1.25:
        vf = "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080"
    else:
        vf = ("split[a][b];[a]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,boxblur=30:3,eq=brightness=-0.08[bg];"
              "[b]scale=-2:1080[fg];[bg][fg]overlay=(W-w)/2:0")
    if tone:
        vf += "," + tone
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-loop", "1", "-i", str(img), "-t", f"{dur:.1f}",
                    "-filter_complex", vf + ",format=yuv420p", "-r", "30", "-c:v", "libx264", "-crf", "18", "-tune", "stillimage",
                    str(out)], check=True)
    return out


def main(argv: list[str]) -> None:
    if not argv or argv[0] != "search":
        print(__doc__)
        return
    films = "--films" in argv
    for t in [a for a in argv[1:] if not a.startswith("--")]:
        print("#", t)
        for r in loc_search(t, films):
            print(f"  {r['date'][:10]:10s} | {r['title'][:80]} | {r['item']} | {r['image']}")
