"""브리핑 썸네일용 기업 사진 (manual/09 §7-1 ⑬).

2026-11-25 사용자: "흑백으로 핵심 기업을 썸네일에 넣고 브리핑은 분석은 인물 등을 하는건 어떻죠?" → "네"
브리핑(…-market-daily·weekly) 썸네일 = 그날 핵심 기업 사진(흑백), 분석(…-market-deep 등) = 인물(컬러).

  python -m ytflow company-photo list                       모음에 있는 회사·사진 수
  python -m ytflow company-photo pick <프로젝트> <회사>      최근 올린 썸네일과 겹치지 않는 사진 하나 → 04_assets/footage/raw/co_<회사>_<n>.jpg
  python -m ytflow company-photo find "<검색어>"             위키미디어 공용에서 후보 찾기 (PD·CC0·CC BY 만)
  python -m ytflow company-photo add <회사> "File:…" --note "간판"   눈으로 확인한 후보를 모음에 더함

모음: config/company_photos.yaml (이미지는 Git 에 두지 않음 — 쓸 때 내려받음, Drive 가 있으면 cache/company_photos 에 보관)
"""
from __future__ import annotations

import json
import re
import shutil
import time
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

from .. import config

LIB = config.ROOT / "config" / "company_photos.yaml"
UA = {"User-Agent": "ytflow-thumb/1.0"}
API = "https://commons.wikimedia.org/w/api.php?"
OK_LICENSE = re.compile(r"^(CC0|Public domain|PD|CC BY \d|CC BY-\d|Attribution)", re.I)


def load() -> dict:
    return yaml.safe_load(LIB.read_text(encoding="utf-8")) or {}


def resolve(name: str) -> str | None:
    """'엔비디아'·'Nvidia'·'nvidia' → 'nvidia'."""
    lib = load()
    n = name.strip().lower()
    for k, v in lib.items():
        if n == k or n in [x.lower() for x in v.get("names", [])]:
            return k
    return None


def _get(url: str, tries: int = 4) -> bytes:
    for i in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(6 * (i + 1))   # 위키미디어는 빠르게 여러 번 부르면 429
    return b""


def _cached(slug: str, i: int, url: str) -> Path:
    cache = config.CACHE_DIR / "company_photos"
    cache.mkdir(parents=True, exist_ok=True)
    f = cache / f"co_{slug}_{i}.jpg"
    if not f.exists() or f.stat().st_size < 5000:
        f.write_bytes(_get(url))
    return f


def credit(ph: dict) -> str:
    return f"사진: {ph.get('author') or '위키미디어 공용'} · {ph.get('license', '')}"


def pick(project_path: str | Path, company: str) -> dict:
    """최근 올린 썸네일에 쓴 사진(co_<회사>_<n>.jpg)을 피해 하나 고르고 프로젝트에 넣음 → {file, credit, company}."""
    from ..project import Project
    from .thumbnail import recent_uploads
    pr = Project.open(str(project_path))
    slug = resolve(company)
    if not slug:
        raise SystemExit(f"[company-photo] 모음에 없는 회사: {company} — company-photo find 로 찾아 add 하세요")
    photos = load()[slug].get("photos") or []
    if not photos:
        raise SystemExit(f"[company-photo] {slug} 사진이 아직 없음 — company-photo find \"{company} headquarters\" → add")
    used = [r["image"] for r in recent_uploads(pr, 5)]
    order = [i for i in range(len(photos)) if f"co_{slug}_{i}.jpg" not in used] or \
            sorted(range(len(photos)), key=lambda i: -max([k for k, u in enumerate(used) if u == f"co_{slug}_{i}.jpg"] or [99]))
    i = order[0]
    src = _cached(slug, i, photos[i]["url"])
    dst = pr.dir("assets") / "footage" / "raw" / f"co_{slug}_{i}.jpg"
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    out = {"company": slug, "file": str(dst.relative_to(pr.path)).replace("\\", "/"), "credit": credit(photos[i]),
           "note": photos[i].get("note", ""), "page": photos[i].get("page", "")}
    if not [k for k in range(len(photos)) if f"co_{slug}_{k}.jpg" not in used]:
        out["warning"] = f"{slug} 사진 {len(photos)}장이 모두 최근에 쓰임 — 가장 오래전 것을 골랐음. find → add 로 늘리세요"
    return out


def find(query: str, limit: int = 15) -> list[dict]:
    """위키미디어 공용 검색 — 라이선스(PD·CC0·CC BY, SA 제외)·크기(가로 1200+)로 거른 후보. 고르기는 눈으로."""
    q = {"action": "query", "format": "json", "generator": "search", "gsrsearch": query + " filetype:bitmap",
         "gsrnamespace": 6, "gsrlimit": 30, "prop": "imageinfo", "iiprop": "url|extmetadata|size", "iiurlwidth": 1920}
    d = json.loads(_get(API + urllib.parse.urlencode(q)))
    out = []
    for p in (d.get("query", {}).get("pages", {}) or {}).values():
        ii = p["imageinfo"][0]
        m = ii.get("extmetadata", {})
        lic = m.get("LicenseShortName", {}).get("value", "")
        if "SA" in lic.upper() or not OK_LICENSE.search(lic) or ii.get("width", 0) < 1200:
            continue
        out.append({"commons": p["title"], "license": lic,
                    "author": re.sub("<[^>]+>", "", m.get("Artist", {}).get("value", "")).strip()[:80] or "위키미디어 공용",
                    "url": (ii.get("thumburl") or ii["url"]).split("?")[0], "page": ii.get("descriptionurl", "")})
    return out[:limit]


def add(company: str, title: str, note: str = "") -> dict:
    title = title if title.startswith("File:") else "File:" + title
    q = {"action": "query", "format": "json", "titles": title, "prop": "imageinfo", "iiprop": "url|extmetadata|size", "iiurlwidth": 1920}
    p = next(iter(json.loads(_get(API + urllib.parse.urlencode(q)))["query"]["pages"].values()))
    if "imageinfo" not in p:
        raise SystemExit(f"[company-photo] 없는 파일: {title}")
    ii = p["imageinfo"][0]
    lic = ii.get("extmetadata", {}).get("LicenseShortName", {}).get("value", "")
    if "SA" in lic.upper() or not OK_LICENSE.search(lic):
        raise SystemExit(f"[company-photo] 쓸 수 없는 라이선스: {lic} (PD·CC0·CC BY 만)")
    slug = resolve(company) or re.sub(r"[^a-z0-9]", "", company.lower())
    if not slug:
        raise SystemExit("[company-photo] 회사 이름을 영문 id 로 주세요 (예: micron)")
    text = LIB.read_text(encoding="utf-8")
    head = "".join(ln for ln in text.splitlines(True) if ln.startswith("#"))
    lib = load()
    ent = lib.setdefault(slug, {"names": [company], "photos": []})
    ent.setdefault("photos", [])
    if any(ph["commons"] == p["title"] for ph in ent["photos"]):
        raise SystemExit("[company-photo] 이미 있음")
    ph = {"commons": p["title"], "note": note, "license": lic,
          "author": re.sub("<[^>]+>", "", ii.get("extmetadata", {}).get("Artist", {}).get("value", "")).strip()[:80] or "위키미디어 공용",
          "url": (ii.get("thumburl") or ii["url"]).split("?")[0], "page": ii.get("descriptionurl", "")}
    ent["photos"].append(ph)
    LIB.write_text(head + yaml.safe_dump(lib, allow_unicode=True, sort_keys=False, width=200), encoding="utf-8")
    return dict(ph, company=slug, n=len(ent["photos"]))


def main(args: list[str]) -> None:
    import argparse
    ap = argparse.ArgumentParser(prog="ytflow company-photo")
    ap.add_argument("what", choices=["list", "pick", "find", "add"])
    ap.add_argument("rest", nargs="*")
    ap.add_argument("--note", default="")
    a = ap.parse_args(args)
    if a.what == "list":
        for k, v in load().items():
            n = len(v.get("photos") or [])
            print(f"{k:10s} {n}장 {'(모자람 — find → add)' if n < 3 else ''}  {' · '.join(v.get('names', [])[:3])}")
    elif a.what == "pick":
        if len(a.rest) < 2:
            raise SystemExit("사용: company-photo pick <프로젝트> <회사>")
        print(json.dumps(pick(a.rest[0], a.rest[1]), ensure_ascii=False, indent=1))
    elif a.what == "find":
        for c in find(" ".join(a.rest)):
            print(f"- {c['commons']} · {c['license']} · {c['author'][:40]}\n  {c['page']}")
    elif a.what == "add":
        if len(a.rest) < 2:
            raise SystemExit("사용: company-photo add <회사> \"File:…\" --note \"간판\"")
        r = add(a.rest[0], a.rest[1], a.note)
        print(f"[company-photo] {r['company']} 에 더함 ({r['n']}장째): {r['commons']} · {r['license']}")
