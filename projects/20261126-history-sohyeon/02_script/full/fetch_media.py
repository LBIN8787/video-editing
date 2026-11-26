"""v3 재료: Mixkit 영상(무료 라이선스) + Commons 영상·음악 → Drive real/video, real/music + credits_media.json"""
import json, re, time, urllib.request, subprocess
from pathlib import Path
from commons import get, UA

EP = Path(r"G:\내 드라이브\ytflow\영상\20261126-history-sohyeon\real")
VD = EP / "video"; MD = EP / "music"; VD.mkdir(exist_ok=True); MD.mkdir(exist_ok=True)
MIX = {"palace": 20095, "candle": 48919, "candles": 17426, "smoke": 45298, "ink": 487, "snowforest": 35040, "snowpine": 25106,
       "raven": 8671, "crow": 34633, "mistforest": 28342, "mist": 50943, "bonfire": 45676, "flames": 52304, "greatwall": 20806,
       "rockwaves": 9294, "bigwave": 7194, "moon": 4433, "moon2": 45584, "leaves": 10050, "hooves": 14899, "horses": 15829,
       "dust": 47285, "books": 21587}
COMMONS_V = {"mukden_drone1": "File:Mukden Palace (Shenyang Gugong) drone footage 1.webm",
             "mukden_drone2": "File:Mukden Palace (Shenyang Gugong) drone footage 2.webm",
             "seoul1901": "File:First ever recorded video footage of Seoul, Korea, by Burton Holmes circa 1901.webm"}
COMMONS_A = {"ossuary1": "File:Ossuary 1 - A Beginning (ISRC USUAN1500043).mp3", "ossuary5": "File:Ossuary 5 - Rest (ISRC USUAN1500047).mp3",
             "ossuary6": "File:Ossuary 6 - Air (ISRC USUAN1500048).mp3", "longnote2": "File:Long Note Two (ISRC USUAN1100420).mp3",
             "longnote3": "File:Long Note Three (ISRC USUAN1100424).mp3", "longnote4": "File:Long Note Four (ISRC USUAN1100467).mp3",
             "himalayan": "File:Himalayan Atmosphere (MacLeod, Kevin) (ISRC USUAN1100204).oga",
             "desolation": "File:Peaceful Desolation (Kevin MacLeod) (ISRC USUAN1200017).oga"}
cred = {}


def dl(url, out, ua=UA):
    if out.exists(): return True
    for a in range(6):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=ua), timeout=120) as r: out.write_bytes(r.read())
            return True
        except Exception as e:
            print("  retry", out.name, e); time.sleep(15 + 15 * a)
    return False


for k, vid in MIX.items():
    ok = dl(f"https://assets.mixkit.co/videos/{vid}/{vid}-720.mp4", VD / f"MK_{k}.mp4", {"User-Agent": "Mozilla/5.0"})
    cred[f"MK_{k}"] = dict(source=f"https://mixkit.co (video {vid})", license="Mixkit Stock Video Free License")
    print(k, ok); time.sleep(1)
for k, t in {**COMMONS_V, **COMMONS_A}.items():
    d = get({"action": "query", "titles": t, "prop": "imageinfo", "iiprop": "url|extmetadata", "format": "json"})
    p = next(iter(d.get("query", {}).get("pages", {}).values()), {}); ii = (p.get("imageinfo") or [{}])[0]; m = ii.get("extmetadata", {})
    g = lambda x: re.sub("<[^>]+>", "", (m.get(x, {}) or {}).get("value", "")).strip()
    url = ii.get("url")
    if not url: print("MISS", k); continue
    ext = url.rsplit(".", 1)[-1]
    out = (VD if k in COMMONS_V else MD) / f"C_{k}.{ext}"
    ok = dl(url, out); time.sleep(6)
    cred[f"C_{k}"] = dict(file=t, license=g("LicenseShortName"), artist=g("Artist")[:100], page=ii.get("descriptionurl"))
    print(k, ok, cred[f"C_{k}"]["license"])
json.dump(cred, open(EP / "credits_media.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
