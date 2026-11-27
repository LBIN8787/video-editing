"""Mixkit 무료 영상 목록(JSON-LD) — python mixkit.py 검색어 [검색어 ...] → id|이름|라이선스"""
import json, re, sys, urllib.request
UA = {"User-Agent": "Mozilla/5.0"}


def items(q):
    h = urllib.request.urlopen(urllib.request.Request(f"https://mixkit.co/free-stock-video/{q}/", headers=UA), timeout=40).read().decode("utf-8")
    out = []
    for blk in re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', h, re.S):
        try: d = json.loads(blk)
        except Exception: continue
        for g in (d.get("@graph") or [d]) if isinstance(d, dict) else d:
            if isinstance(g, dict) and g.get("@type") == "VideoObject":
                vid = re.search(r"videos/(\d+)/", g.get("contentUrl", ""))
                out.append(dict(id=vid.group(1) if vid else "", name=g.get("name"), url=g.get("contentUrl"), lic=g.get("license", ""), thumb=g.get("thumbnailUrl")))
    return out


if __name__ == "__main__":
    for q in sys.argv[1:]:
        print("##", q)
        for it in items(q): print(it["id"], "|", it["name"], "|", it["lic"].split("#")[-1])
