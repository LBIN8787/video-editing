"""뉴스레터 → 채널별 소재 목록 (2026-11-15 사용자: 무료 뉴스레터를 소스 탐색·참조용으로 구독, "진행해주세요").

뉴스레터는 **단서**입니다. 문장을 대본·화면에 옮기지 않고, 영상에 넣을 숫자·발언은 링크를 따라 1차 출처로 확인합니다.
메일 하나를 그대로 쌓지 않고, 소재마다 다섯 칸으로 나눕니다:
    소재(원래 제목) · 원문 링크 · 원자료·통계 · 영상·이미지 출처 · 재사용 조건
그리고 채널(market·ai·curiosity·issues)별로 모아 `inbox/newsletters/<YYYYMMDD>.md|json` 에 씁니다.
시장·시사 매일 브리핑은 `daily` 가 그날 파일을 `daily_brief.md` 끝 '⑦ 뉴스레터 화제'로 붙입니다.

메일 가져오기 (클라우드 Python 은 Gmail 에 직접 못 들어감 → 에이전트가 Gmail 커넥터로):
    1) Gmail 검색 `label:뉴스레터 newer_than:2d` (또는 config/newsletters.yaml 의 보낸 사람)
    2) 메일마다 get_message(PLAIN_TEXT) → {"id","sender","subject","date","body"} 를 JSON 으로 `.cache/newsletters/raw/` 에 저장
    3) python -m ytflow newsletters ingest .cache/newsletters/raw/*.json
RSS 는 직접:   python -m ytflow newsletters rss
보기:          python -m ytflow newsletters show [--brand curiosity] [--days 7]
원문 메일 본문은 커밋하지 않습니다(.cache). 커밋하는 것은 제목·링크·분류뿐.
"""
from __future__ import annotations

import json
import re
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

from .. import config

KST = timezone(timedelta(hours=9))
CFG = config.ROOT / "config" / "newsletters.yaml"
OUT = config.ROOT / "inbox" / "newsletters"
BRANDS = ("market", "ai", "curiosity", "issues")
BRAND_KO = {"market": "시장", "ai": "AI", "curiosity": "호기심", "issues": "시사"}
KIND_KO = {"primary": "원문", "data": "원자료·통계", "media": "영상·이미지", "news": "보도·글"}
NOISE_SUBJ = re.compile(r"(?i)confirm|welcome|verify|subscription|preferences|update profile|구독 확인|인증|가입")
GENERIC = re.compile(r"(?i)^(read more|more|here|click here|link|learn more|full story|continue reading|read|sign up|subscribe|"
                     r"view online|this|website|자세히|더 보기|원문|바로가기|기사 보기)\W*$")
UA = {"User-Agent": "ytflow-newsletters (research)"}


def cfg() -> dict:
    return yaml.safe_load(CFG.read_text(encoding="utf-8"))


# ── 날짜: 한국 06:00 이후 도착은 다음 날 영상 몫 (inbox/save 와 같은 규칙) ──
def video_day(iso: str) -> str:
    try:
        t = datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(KST)
    except ValueError:
        t = datetime.now(KST)
    d = t.date() + (timedelta(days=1) if t.hour >= 6 else timedelta(0))
    return d.strftime("%Y%m%d")


# ── 어느 뉴스레터인가 ──
def which(msg: dict, c: dict) -> dict | None:
    who = (msg.get("sender", "") + " " + msg.get("name", "")).lower()
    for s in c["sources"]:
        if any(m.lower() in who for m in s.get("match", [])):
            if s.get("subject") and not re.search(s["subject"], msg.get("subject", "")):
                continue
            return s
    return None


# ── 링크 ──
def unwrap(url: str) -> str:
    """추적 주소 안에 든 진짜 주소 꺼내기 (TLDR 의 /CL0/<인코딩된 주소>/… 등). 못 꺼내면 그대로."""
    m = re.search(r"/CL0/(https?(?::|%3A)[^/]*(?:/|%2F).+?)/\d+/[0-9a-f-]{20,}", url)
    if m:
        url = urllib.parse.unquote(m.group(1))
    else:
        q = urllib.parse.parse_qs(urllib.parse.urlsplit(url).query)
        for k in ("url", "u", "redirect", "target", "r"):
            if k in q and q[k][0].startswith("http"):
                url = q[k][0]
                break
    p = urllib.parse.urlsplit(url)
    keep = [(k, v) for k, v in urllib.parse.parse_qsl(p.query) if not k.lower().startswith(("utm_", "mc_", "ref", "_hs", "mkt_"))]
    return urllib.parse.urlunsplit((p.scheme, p.netloc, p.path, urllib.parse.urlencode(keep), ""))


OPAQUE = ("beehiiv.com", "substack.com/redirect", "list-manage.com/track", "links.", "click.", "email.", "r.", "trk.", "go.")


# Ingestion never dereferences email links. Even HEAD can trigger an action.
MANAGEMENT = re.compile(
    r"unsubscribe|subscription|preferences|opt[-_ ]?out|manage[-_ /]?profile|"
    r"confirm|verification|verify|sign[-_ ]?in|log[-_ ]?in|password|"
    r"구독.?해지|수신.?거부|환경.?설정|본인.?인증", re.I)
PUBLIC_QUERY = {"id", "v", "q", "s", "page", "lang", "language", "year", "month"}
SENSITIVE_QUERY = re.compile(
    r"token|secret|email|recipient|subscriber|signature|auth|session|hash|"
    r"^key$|^code$|^uid$|^cid$|^mid$", re.I)


def public_link(url: str) -> bool:
    """Conservative publication gate, not proof that a URL is safe to visit."""
    try:
        p = urllib.parse.urlsplit(url)
        host = (p.hostname or "").lower()
        if p.scheme not in ("http", "https") or not host or p.username or p.password:
            return False
        decoded = urllib.parse.unquote(url)
        if MANAGEMENT.search(decoded):
            return False
        low = decoded.lower()
        if (host == "beehiiv.com" or host.endswith(".beehiiv.com") or
                host.startswith(("links.", "click.", "email.", "r.", "trk.", "go.")) or
                (host.endswith("substack.com") and p.path.startswith("/redirect")) or
                (host.endswith("list-manage.com") and p.path.startswith("/track"))):
            return False
        # Unknown query keys can be per-recipient identifiers: retain privately
        # for manual canonical-source lookup, never publish or request them.
        pairs = urllib.parse.parse_qsl(p.query, keep_blank_values=True)
        if any(SENSITIVE_QUERY.search(k) or k.lower() not in PUBLIC_QUERY or
               len(v) > 80 or "@" in v for k, v in pairs):
            return False
        if re.search(r"(?:^|/)[A-Za-z0-9_=-]{48,}(?:/|$)", p.path):
            return False
        return True
    except ValueError:
        return False


def resolve(url: str, timeout: int = 8) -> str:
    """Compatibility helper: offline unwrap only; never follows redirects."""
    return unwrap(url)


def kind(url: str, c: dict) -> str:
    u = url.lower()
    for k in ("primary", "data", "media"):
        for d in c["links"][k]:
            host = urllib.parse.urlsplit(u).netloc
            if (d.endswith(".") and host.startswith(d)) or (d.startswith(".") and u.split("?")[0].endswith(d)) or d in u:
                return k
    return "news"


def reuse(url: str, c: dict) -> str:
    host = urllib.parse.urlsplit(url).netloc.lower()
    for d, txt in c["reuse"].items():
        if host == d or host.endswith("." + d) or d in url.lower():
            return txt
    return "보도·글: 단서만 (문장 옮기지 않기, 인용은 짧게 출처 표시)"


def skip(url: str, title: str, c: dict, own: list[str]) -> bool:
    low = (url + " " + title).lower()
    if any(s in low for s in c["skip"]):
        return True
    host = urllib.parse.urlsplit(url).netloc.lower()
    path = urllib.parse.urlsplit(url).path.strip("/")
    return any(o in host for o in own) and len(path) < 12   # 뉴스레터 자기 홈 (기사 주소는 남김)


# ── 메일 본문 → 소재 ──
LINK_MD = re.compile(r"\[([^\]\n]{2,240})\]\((https?://[^)\s]+)\)")
LINK_ANGLE = re.compile(r"([^\n<>]{0,240}?)\s*[<(](https?://[^>)\s]+)[>)]")
LINK_BARE = re.compile(r"https?://[^\s<>()\[\]\"']+")


def _clean(t: str) -> str:
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)   # 마크다운 링크 → 글자만
    t = re.sub(r"https?://\S+", "", t)
    t = re.sub(r"[*#>`]+|(?<!\w)_|_(?!\w)", "", t)
    t = re.sub(r"\((\d+ )?min(ute)? read\)|\(GitHub Repo\)|\(Sponsor\)", "", t, flags=re.I)
    t = re.sub(r"\s+", " ", t).strip(" -–—:|·•")
    return t[:180]


def extract(body: str) -> list[tuple[str, str]]:
    """[(제목, 주소)] — 마크다운 링크 → '글 <주소>' → 맨 주소(앞줄을 제목으로) 순서로."""
    out, seen_spans = [], []
    lines = body.splitlines()
    for rx in (LINK_MD, LINK_ANGLE):
        for m in rx.finditer(body):
            if any(a <= m.start() < b for a, b in seen_spans):
                continue
            seen_spans.append(m.span())
            title, url = _clean(m.group(1)), m.group(2)
            if not title or GENERIC.match(title):   # 'Read more' → 앞 줄을 제목으로
                before = body[: m.start()].rstrip().splitlines()
                title = _clean(before[-1]) if before else ""
            out.append((m.start(), title, url))
    for m in LINK_BARE.finditer(body):
        if any(a <= m.start() < b for a, b in seen_spans):
            continue
        ln = body.count("\n", 0, m.start())
        title = _clean(lines[ln][: m.start() - (body.rfind("\n", 0, m.start()) + 1)]) or (_clean(lines[ln - 1]) if ln else "")
        out.append((m.start(), title, m.group(0).rstrip(".,;")))
    return [(t, u) for _, t, u in sorted(out)]   # 본문 순서대로 (원자료 링크를 바로 앞 소재에 붙이려면)


def route(title: str, src: dict, c: dict) -> str:
    bs = src.get("brands") or ["curiosity"]
    if len(bs) == 1:
        return bs[0]
    t = f" {title.lower()} "
    score = {b: sum(1 for w in c["route"].get(b, []) if w in t) for b in bs}
    best = max(bs, key=lambda b: (score[b], -bs.index(b)))
    return best if score[best] else bs[0]


def items_from(msg: dict, c: dict, do_resolve: bool = True) -> list[dict]:
    src = which(msg, c)
    if not src or NOISE_SUBJ.search(msg.get("subject", "")):
        return []
    own = [m.lower() for m in src.get("match", [])]
    out, urls = [], set()
    for title, url in extract(msg.get("body", "")):
        # Filter raw link/label BEFORE unwrapping. No email-link HTTP requests,
        # including when do_resolve=True (legacy API compatibility).
        if len(title) < 8 or MANAGEMENT.search(urllib.parse.unquote(url) + " " + title):
            continue
        if skip(url, title, c, own):
            continue
        try:
            url = unwrap(url)
        except ValueError:
            continue
        if not public_link(url) or skip(url, title, c, own) or url in urls:
            continue
        urls.add(url)
        k = kind(url, c)
        if out and ((k in ("data", "media") and len(title.split()) <= 4) or title == out[-1]["title"]):   # 'See the data' 같은 짧은 링크 → 앞 소재의 원자료·이미지
            out[-1].setdefault("extra", []).append({"kind": k, "url": url, "reuse": reuse(url, c)})
            continue
        out.append({"title": title, "url": url, "kind": k, "reuse": reuse(url, c), "brand": route(title, src, c),
                    "source": src["id"], "source_name": src["name"], "msg": msg.get("id", ""), "date": msg.get("date", "")})
    return out


# ── 저장 (날짜 파일에 덧붙임, 같은 주소·같은 메일은 한 번만) ──
def _load(day: str) -> dict:
    p = OUT / f"{day}.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"day": day, "messages": [], "items": []}


def _save(d: dict) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{d['day']}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    p = OUT / f"{d['day']}.md"
    p.write_text(to_md(d), encoding="utf-8")
    return p


def add(items: list[dict], msgs: list[dict]) -> list[Path]:
    """날짜 파일에 덧붙임. 최근 2주에 이미 나온 주소는 새로 넣지 않고 '같이 다룸'에 뉴스레터만 더함."""
    days: dict[str, dict] = {}
    if OUT.exists():
        for p in sorted(OUT.glob("*.json"))[-14:]:
            days[p.stem] = _load(p.stem)
    touched = set()
    for m in msgs:
        d = days.setdefault(video_day(m.get("date", "")), _load(video_day(m.get("date", ""))))
        if m.get("id") and m["id"] not in {x["id"] for x in d["messages"]}:
            d["messages"].append({"id": m["id"], "subject": m.get("subject", "")[:120], "sender": m.get("sender", ""), "date": m.get("date", "")})
            touched.add(d["day"])
    for it in items:
        old = next(((dd, x) for dd in days.values() for x in dd["items"] if x["url"] == it["url"]), None)
        if old:
            dd, x = old
            if it["source"] != x["source"] and it["source"] not in x.setdefault("also", []):
                x["also"].append(it["source"])
                touched.add(dd["day"])
            continue
        d = days.setdefault(video_day(it["date"]), _load(video_day(it["date"])))
        d["items"].append(it)
        touched.add(d["day"])
    return [_save(days[k]) for k in sorted(touched)]


def ingest(paths: list[str], do_resolve: bool = True) -> list[Path]:
    c = cfg()
    msgs = []
    for p in paths:
        x = json.loads(Path(p).read_text(encoding="utf-8"))
        msgs += x if isinstance(x, list) else [x]
    items = [it for m in msgs for it in items_from(m, c, do_resolve)]
    known = [m for m in msgs if which(m, c) and not NOISE_SUBJ.search(m.get("subject", ""))]
    out = add(items, known)
    skipped = [m.get("subject", "")[:50] for m in msgs if m not in known]
    print(f"[newsletters] 메일 {len(msgs)}통 → 뉴스레터 {len(known)}통 · 소재 {len(items)}개" + (f" · 건너뜀(구독 확인·모르는 보낸 사람): {skipped}" if skipped else ""))
    for p in out:
        print(f"[newsletters] → {p}")
    return out


def rss() -> list[Path]:
    """config 의 rss 소스 (Simon Willison 등) — 최근 2일 글."""
    import xml.etree.ElementTree as ET
    c = cfg()
    items = []
    for s in (s for s in c["sources"] if s.get("rss")):
        root = ET.fromstring(urllib.request.urlopen(urllib.request.Request(s["rss"], headers=UA), timeout=30).read())
        ns = {"a": "http://www.w3.org/2005/Atom"}
        ents = root.findall("a:entry", ns) or root.findall(".//item")
        for e in ents:
            title = (e.findtext("a:title", None, ns) or e.findtext("title") or "").strip()
            link = e.find("a:link", ns)
            url = link.get("href") if link is not None else (e.findtext("link") or "")
            date = e.findtext("a:updated", None, ns) or e.findtext("a:published", None, ns) or e.findtext("pubDate") or ""
            try:
                t = datetime.fromisoformat(date.replace("Z", "+00:00"))
            except ValueError:
                continue
            if datetime.now(timezone.utc) - t > timedelta(days=2) or not title or not url:
                continue
            url = unwrap(url)
            if not public_link(url):
                continue
            items.append({"title": _clean(title), "url": url, "kind": kind(url, c), "reuse": reuse(url, c), "brand": route(title, s, c),
                          "source": s["id"], "source_name": s["name"], "msg": "rss", "date": t.isoformat()})
    out = add(items, [])
    print(f"[newsletters] RSS 소재 {len(items)}개")
    return out


# ── 보기 ──
def to_md(d: dict) -> str:
    day = d["day"]
    L = [f"# 뉴스레터 소재 — {day[:4]}-{day[4:6]}-{day[6:]} 영상 몫", "",
         "> 자동 정리한 **단서**입니다. 문장을 대본·화면에 옮기지 않고, 숫자·발언은 링크를 따라 1차 출처로 확인합니다 (docs/36).",
         f"> 메일 {len(d['messages'])}통 · 소재 {len(d['items'])}개 · 한국 06:00 이후 도착분은 다음 날 파일", ""]
    for b in BRANDS:
        its = [x for x in d["items"] if x["brand"] == b]
        if not its:
            continue
        L += [f"## {BRAND_KO[b]} ({len(its)})", "", "| 소재 (원래 제목) | 원문·기사 | 원자료·통계 | 영상·이미지 | 재사용 조건 | 뉴스레터 |", "|---|---|---|---|---|---|"]
        its.sort(key=lambda x: (-len(x.get("also", [])), ["primary", "data", "media", "news"].index(x["kind"])))
        for x in its:
            col = {"primary": [], "news": [], "data": [], "media": []}
            for lk in [x] + x.get("extra", []):
                host = urllib.parse.urlsplit(lk["url"]).netloc.removeprefix("www.")
                col[lk["kind"]].append(f"[{host}{' (1차)' if lk['kind'] == 'primary' else ''}]({lk['url']})")
            cell = lambda *ks: " ".join(v for k in ks for v in col[k]) or "—"
            rs = " / ".join(dict.fromkeys([x["reuse"]] + [e["reuse"] for e in x.get("extra", [])]))
            also = f" (+{', '.join(x['also'])})" if x.get("also") else ""
            L.append(f"| {x['title'].replace('|', '/')} | {cell('primary', 'news')} | {cell('data')} | {cell('media')} | {rs.replace('|', '/')} | {x['source_name']}{also} |")
        L.append("")
    return "\n".join(L)


def section(brands: tuple[str, ...], day: str, n: int = 15) -> str:
    """daily_brief.md 에 붙일 '⑦ 뉴스레터 화제'. day 는 YYYY-MM-DD 또는 YYYYMMDD (영상 날짜)."""
    d = _load(day.replace("-", ""))
    its = [x for x in d["items"] if x["brand"] in brands]
    L = ["", f"## ⑦ 뉴스레터 화제 ({'·'.join(BRAND_KO[b] for b in brands)}) — 단서, 1차 출처로 확인"]
    if not its:
        L.append(f"(이 날짜 뉴스레터 소재 없음 — `inbox/newsletters/{d['day']}.md`. 수집: docs/36)")
        return "\n".join(L) + "\n"
    its.sort(key=lambda x: (-len(x.get("also", [])), ["primary", "data", "media", "news"].index(x["kind"])))
    for x in its[:n]:
        also = f", 같이 다룸: {', '.join(x['also'])}" if x.get("also") else ""
        L.append(f"- [{KIND_KO[x['kind']]}] {x['title']} — {x['source_name']}{also} · {x['url']}")
    if len(its) > n:
        L.append(f"- … 나머지 {len(its) - n}개: `inbox/newsletters/{d['day']}.md`")
    return "\n".join(L) + "\n"


def show(brand: str = "", days: int = 1) -> None:
    today = datetime.now(KST).date()
    for k in range(days):
        day = (today - timedelta(days=k)).strftime("%Y%m%d")
        d = _load(day)
        its = [x for x in d["items"] if not brand or x["brand"] == brand]
        if not its:
            continue
        print(f"# {day} ({len(its)})")
        for x in its:
            print(f"  [{BRAND_KO[x['brand']]}/{KIND_KO[x['kind']]}] {x['title'][:80]} — {x['source']} · {x['url']}")


def sources() -> None:
    for s in cfg()["sources"]:
        print(f"  {s['status']:10s} | {s['name'][:28]:28s} | {','.join(s['brands']):24s} | {s['cadence']:8s} | 도착 {s['arrives']}")


def main(argv: list[str]) -> None:
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return
    cmd, rest = argv[0], argv[1:]
    if cmd == "ingest":
        ingest([a for a in rest if not a.startswith("--")], do_resolve="--no-resolve" not in rest)
    elif cmd == "rss":
        rss()
    elif cmd == "show":
        brand = rest[rest.index("--brand") + 1] if "--brand" in rest else ""
        days = int(rest[rest.index("--days") + 1]) if "--days" in rest else 1
        show(brand, days)
    elif cmd == "sources":
        sources()
    else:
        print(__doc__)

