"""Wikimedia Commons 검색 → 후보 목록(라이선스·작가·크기). 사용: python commons.py "검색어" [n]"""
import json, sys, time, urllib.parse, urllib.request
UA = {"User-Agent": "ytflow-research/1.0 (educational video research)"}
API = "https://commons.wikimedia.org/w/api.php"


def get(params):
    url = API + "?" + urllib.parse.urlencode(params)
    for a in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:
            time.sleep(3 + a * 4)
    return {}


def search(q, n=12):
    d = get({"action": "query", "generator": "search", "gsrsearch": q, "gsrnamespace": 6, "gsrlimit": n, "prop": "imageinfo",
             "iiprop": "url|size|extmetadata|mime", "iiurlwidth": 2400, "format": "json"})
    out = []
    for p in (d.get("query", {}).get("pages", {}) or {}).values():
        ii = (p.get("imageinfo") or [{}])[0]; m = ii.get("extmetadata", {})
        g = lambda k: (m.get(k, {}) or {}).get("value", "")
        out.append(dict(title=p["title"], w=ii.get("width"), h=ii.get("height"), mime=ii.get("mime"), lic=g("LicenseShortName"),
                        artist=g("Artist")[:120], url=ii.get("thumburl") or ii.get("url"), page=ii.get("descriptionurl")))
    return out


if __name__ == "__main__":
    for r in search(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 12):
        print(f"{r['lic'][:14]:14} {r['w']}x{r['h']} {r['title'][:90]}")
