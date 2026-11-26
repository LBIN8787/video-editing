"""인사이트 수집 — 자리 → 판단 → 주제 (2026-11-26 사용자: "다른 사람들의 인사이트 유명 기술자 실리콘밸리의 기술 등등 …
기술 인사이트 시장 인사이트 등 말이죠 사람을 감시하기보다는 좀 더 폭넓게 다루고싶어요", docs/70).

영상의 주어는 소식이 아니라 '앞으로에 대한 누군가의 판단'(manual/09 §5-00). 그래서 모으는 단위도 판단이다.

  1) 자리 훑기 — config/insight_venues.yaml 의 팟캐스트·강연·방송·회사 공식 채널의 이번 주 새 영상 (목록·정보만, 내려받기 없음)
     + 목록 밖에서 찾기: 이번 주 검색(조회가 튄 인터뷰), 해커뉴스 첫 화면의 강연·인터뷰 링크
  2) 1차 거르기 (LLM, 제목·설명만) — 앞으로에 대한 판단이 있나, 무엇에 대한 것인가(주제), 누가, 어느 채널로
  3) 판단 뽑기 (점수 높은 몇 편만, 자막) — 판단 문장 원문·번역·몇 분 몇 초·근거·시간표
  4) 주제별 판단 장부 inbox/insights/ledger.json → 오늘 보고 inbox/insights/<날짜>.md (영상 후보 = 판단 + 반대 판단 + 원본)

    python -m ytflow insights                 # 오늘 전부
    python -m ytflow insights --no-llm        # 자리 훑기만 (거르기·뽑기 없이 목록)
    python -m ytflow insights --extract 4     # 자막까지 열 후보 수
    python -m ytflow insights --mark <영상id> made --our <우리 유튜브 id>   # 만든 원본 (공개→우리 업로드 걸린 날 기록)

지키는 것: 봇 확인·요청 제한(429)이 뜨면 우회하지 않고 건너뜀. 결과는 단서 — 대본의 발언은 원본에서 다시 확인(manual/09 §3-5).
"""
from __future__ import annotations

import json
import math
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

from pydantic import BaseModel, Field

from .. import config

KST = timezone(timedelta(hours=9))
DIR = config.ROOT / "inbox" / "insights"
UA = {"User-Agent": "Mozilla/5.0 (ytflow insights)"}


# ── 설정·저장 ─────────────────────────────────────────────────────────
def _cfg() -> dict:
    import yaml
    c = yaml.safe_load((config.ROOT / "config" / "insight_venues.yaml").read_text(encoding="utf-8")) or {}
    names = []
    try:   # 이름 있는 사람 = 가산점만 (거르는 조건 아님)
        w = yaml.safe_load((config.ROOT / "config" / "ceo_watch.yaml").read_text(encoding="utf-8")) or {}
        r = yaml.safe_load((config.ROOT / "config" / "radar.yaml").read_text(encoding="utf-8")) or {}
        for p in list(w.get("ceos") or []) + list(r.get("extra") or []):
            if isinstance(p, dict) and p.get("en"):
                names.append(p["en"])
    except Exception:  # noqa: BLE001
        pass
    c["boost_names"] = names
    return c


def _load(name: str, default):
    f = DIR / name
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return default


def _save(name: str, data) -> None:
    DIR.mkdir(parents=True, exist_ok=True)
    (DIR / name).write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")


def _get(url: str, timeout: int = 20) -> str:
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read().decode("utf-8", "replace")


def _ydl(flat: bool, items: str = ""):
    import yt_dlp
    o = {"quiet": True, "no_warnings": True, "skip_download": True, "ignoreerrors": True, "extract_flat": flat}
    if items:
        o["playlist_items"] = items
    return yt_dlp.YoutubeDL(o)


# ── 1) 자리 훑기 ──────────────────────────────────────────────────────
def _rss(cid: str) -> dict:
    """채널 RSS: 영상 id → 올린 때·설명·조회 (최근 15편)."""
    out = {}
    try:
        x = _get(f"https://www.youtube.com/feeds/videos.xml?channel_id={cid}")
    except Exception as e:  # noqa: BLE001
        print(f"  ! RSS 실패 {cid}: {str(e)[:60]}", file=sys.stderr)
        return out
    for ent in x.split("<entry>")[1:]:
        vid = re.search(r"<yt:videoId>([^<]+)", ent)
        if not vid:
            continue
        pub = re.search(r"<published>([^<]+)", ent)
        desc = re.search(r"<media:description>(.*?)</media:description>", ent, re.S)
        views = re.search(r'views="(\d+)"', ent)
        out[vid.group(1)] = {"published": pub.group(1) if pub else "",
                             "desc": (desc.group(1) if desc else "")[:600],
                             "views": int(views.group(1)) if views else 0}
    return out


def _age_days(published: str, now: datetime) -> float:
    try:
        return (now - datetime.fromisoformat(published.replace("Z", "+00:00"))).total_seconds() / 86400
    except Exception:  # noqa: BLE001
        return 99.0


def _commentary(title: str, cfg: dict) -> bool:
    t = (title or "").lower()
    return any(w.lower() in t for w in cfg.get("commentary_words") or [])


def scan_venues(cfg: dict, now: datetime) -> list[dict]:
    cache = _load("venues_cache.json", {})
    win, mins, per = float(cfg.get("window_days", 7)), float(cfg.get("min_minutes", 12)), int(cfg.get("per_venue", 8))
    found = []
    with _ydl(True, f"1-{per}") as y:
        for v in cfg.get("venues") or []:
            h = v["handle"]
            try:
                url = f"https://www.youtube.com/channel/{h}/videos" if re.fullmatch(r"UC[\w-]{22}", h) else f"https://www.youtube.com/@{h}/videos"
                r = y.extract_info(url, download=False) or {}
            except Exception as e:  # noqa: BLE001 — 봇 확인 등: 우회하지 않고 건너뜀
                print(f"  ! 자리 건너뜀 {v['name']}: {str(e)[:60]}", file=sys.stderr)
                continue
            cid = r.get("channel_id") or cache.get(h)
            if not cid:
                print(f"  ! 자리 못 찾음 {v['name']} (@{h})", file=sys.stderr)
                continue
            cache[h] = cid
            rss = _rss(cid)
            for e in r.get("entries") or []:
                if not e or not e.get("id"):
                    continue
                meta = rss.get(e["id"], {})
                age = _age_days(meta.get("published", ""), now)
                dur = (e.get("duration") or 0) / 60
                if age > win or (dur and dur < mins) or _commentary(e.get("title", ""), cfg):
                    continue
                found.append({"id": e["id"], "title": e.get("title", ""), "channel": v["name"], "venue": h,
                              "area": v.get("area", "both"), "weight": v.get("weight", 1), "minutes": round(dur),
                              "views": e.get("view_count") or meta.get("views", 0), "published": meta.get("published", ""),
                              "age": round(age, 1), "desc": meta.get("desc", ""), "via": "자리"})
    _save("venues_cache.json", cache)
    return found


def discover(cfg: dict, now: datetime) -> list[dict]:
    """목록 밖: 이번 주 검색(조회가 튄 인터뷰·강연) + 해커뉴스 첫 화면."""
    d = cfg.get("discover") or {}
    out, mins = [], float(cfg.get("min_minutes", 12))
    week = "EgIIAw%253D%253D"
    with _ydl(True) as y:
        for q in d.get("queries") or []:
            try:
                r = y.extract_info(f"https://www.youtube.com/results?search_query={urllib.parse.quote_plus(q)}&sp={week}", download=False) or {}
            except Exception as e:  # noqa: BLE001
                print(f"  ! 검색 실패 {q}: {str(e)[:60]}", file=sys.stderr)
                continue
            if not r.get("entries"):
                print(f"  ! 검색 결과 없음 (막혔을 수 있음, 우회하지 않음): {q}", file=sys.stderr)
            for e in (r.get("entries") or [])[:20]:
                if not e or not e.get("id"):
                    continue
                t = e.get("title") or ""
                if re.search(r"[가-힣ぁ-んァ-ン一-龥]", t) or _commentary(t, cfg):
                    continue
                if (e.get("duration") or 0) / 60 < mins or (e.get("view_count") or 0) < d.get("min_views", 30000):
                    continue
                out.append({"id": e["id"], "title": t, "channel": e.get("channel") or e.get("uploader") or "",
                            "venue": "", "area": "both", "weight": 1, "minutes": round((e.get("duration") or 0) / 60),
                            "views": e.get("view_count") or 0, "published": "", "age": 3.5, "desc": "", "via": f"검색: {q}"})
    if d.get("hn"):
        try:
            hn = json.loads(_get("https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=60"))
            for h in hn.get("hits") or []:
                u, t = h.get("url") or "", h.get("title") or ""
                m = re.search(r"(?:youtube\.com/watch\?v=|youtu\.be/)([\w-]{11})", u)
                if m or re.search(r"\b(interview|talk|podcast|keynote|conversation|lecture)\b", t, re.I):
                    out.append({"id": m.group(1) if m else "hn:" + str(h.get("objectID")), "title": t, "channel": "Hacker News",
                                "venue": "", "area": "tech", "weight": 1, "minutes": 0, "views": h.get("points", 0) * 100,
                                "published": h.get("created_at", ""), "age": _age_days(h.get("created_at", ""), now),
                                "desc": "", "url": u or f"https://news.ycombinator.com/item?id={h.get('objectID')}", "via": "해커뉴스"})
        except Exception as e:  # noqa: BLE001
            print(f"  ! 해커뉴스 실패: {str(e)[:60]}", file=sys.stderr)
    return out


# ── 2) 1차 거르기 (제목·설명만) ──────────────────────────────────────
class Pick(BaseModel):
    id: str
    forward: bool = Field(description="앞으로(기술·시장·경제가 어떻게 된다)에 대한 판단이 담겼을 가능성이 높은가")
    speaker: str = Field(description="주로 말하는 사람 이름과 직함(영어 원문 이름). 모르면 빈 문자열")
    area: str = Field(description="tech | market | macro | ai-use | society 중 하나")
    theme: str = Field(description="판단의 주제를 한국어 질문 한 줄로 (예: 'AI 에이전트가 소프트웨어 일을 대신할까'). 기존 주제와 같으면 그 문장을 그대로")
    claim_guess: str = Field(description="제목·설명으로 짐작한 판단 한 줄 (한국어, 짐작이라고 표시)")
    strength: int = Field(description="0 판단 없음 · 1 막연한 낙관/비관 · 2 방향이 분명 · 3 날짜·숫자가 있는 구체적 판단")
    route: str = Field(description="market (기술·소식이 돈·기업·시장에 미치는 영향) | ai (AI 를 쓰는 법·일의 변화) | issues (사회·제도)")


class Picks(BaseModel):
    items: list[Pick]


SYS_PICK = """당신은 유튜브 분석 채널의 소재 담당입니다. 시청자는 소식 자체가 아니라 '앞으로 어떻게 되나'에 대한 이름 있는 사람의
판단과 그 근거를 원합니다(manual/09 §5-00). 아래 영상들의 제목·설명만 보고 판단이 담겼을지 짐작하세요.
- 회사 제품 홍보·사용법 강좌·뉴스 요약 클립은 forward=false.
- 주제(theme)는 사람이 아니라 질문으로. 같은 질문이면 '기존 주제' 문장을 그대로 써서 묶이게.
- 없는 사실을 만들지 말 것. claim_guess 는 짐작임을 '(짐작)'으로 표시."""


def classify(items: list[dict], themes: list[str]) -> dict:
    from .. import llm
    out = {}
    for i in range(0, len(items), 30):
        chunk = items[i:i + 30]
        body = "기존 주제:\n" + "\n".join(f"- {t}" for t in themes[-80:]) + "\n\n영상:\n" + "\n".join(
            f"[{it['id']}] {it['channel']} · {it['minutes']}분 · 조회 {it['views']:,}\n제목: {it['title']}\n설명: {it['desc'][:300]}"
            for it in chunk)
        try:
            r = llm.structured(SYS_PICK, body, Picks, task="insights")
            for p in r.items:
                out[p.id] = p.model_dump()
        except Exception as e:  # noqa: BLE001
            print(f"  ! 거르기 실패 ({len(chunk)}편): {str(e)[:120]}", file=sys.stderr)
    return out


def score(it: dict, cfg: dict) -> float:
    s = it.get("pick") or {}
    if not s.get("forward"):
        return 0.0
    fresh = max(0.4, 1.0 - it.get("age", 3.5) / 10)
    pop = math.log10(max(it.get("views") or 0, 1000)) - 2   # 1천=1 · 10만=3 · 100만=4
    who = 1.3 if any(n.lower() in (it["title"] + " " + s.get("speaker", "")).lower() for n in cfg.get("boost_names") or []) else 1.0
    return round(it.get("weight", 1) ** 0.5 * (1 + s.get("strength", 0)) * fresh * pop * who, 2)


# ── 3) 판단 뽑기 (자막) ──────────────────────────────────────────────
def transcript(vid: str) -> list[tuple[float, str]]:
    """자동 자막(영어) → [(초, 글)]. 요청 제한·봇 확인이면 빈 목록 (우회하지 않음)."""
    with _ydl(False) as y:
        try:
            info = y.extract_info(f"https://www.youtube.com/watch?v={vid}", download=False) or {}
        except Exception:  # noqa: BLE001
            return []
    tracks = (info.get("subtitles") or {}).get("en") or (info.get("automatic_captions") or {}).get("en") or []
    url = next((t["url"] for t in tracks if t.get("ext") == "json3"), "")
    if not url:
        return []
    try:
        j = json.loads(_get(url, 30))
    except Exception as e:  # noqa: BLE001
        print(f"  ! 자막 건너뜀 {vid}: {str(e)[:60]}", file=sys.stderr)
        return []
    segs = []
    for ev in j.get("events") or []:
        t = "".join(s.get("utf8", "") for s in ev.get("segs") or []).strip()
        if t:
            segs.append((ev.get("tStartMs", 0) / 1000, t.replace("\n", " ")))
    return segs


class Judgment(BaseModel):
    quote: str = Field(description="판단이 담긴 말 그대로 (자막 원문, 고치지 말 것)")
    ko: str = Field(description="한국어 번역")
    at: int = Field(description="말한 시각(초) — 자막 앞의 [초] 표시에서")
    claim: str = Field(description="앞으로 어떻게 된다는 판단 한 줄 (한국어)")
    basis: str = Field(description="그가 든 근거 (한국어, 그가 말한 것만)")
    horizon: str = Field(description="시간표가 있으면 (예: '2027년', '1~2년 안'), 없으면 빈 문자열")
    stance: str = Field(description="주제 질문에 대한 입장: yes | no | mixed")


class Extract(BaseModel):
    speaker: str
    theme: str
    judgments: list[Judgment]


SYS_EXT = """아래는 인터뷰·강연 자막입니다(앞의 [초] 는 말한 시각). '앞으로 어떻게 된다'는 판단을 최대 5개 뽑으세요.
- quote 는 자막 원문 그대로. 자막에 없는 말을 만들지 말 것. 근거(basis)도 그가 실제로 말한 것만.
- 소식 전달·제품 설명은 판단이 아님. 날짜·숫자가 있는 판단을 앞에.
- theme 은 주어진 주제 질문을 그대로 쓰되, 판단이 다른 질문에 더 맞으면 새 질문 한 줄로."""


def extract(it: dict) -> dict | None:
    from .. import llm
    segs = transcript(it["id"])
    if not segs:
        return None
    lines, last, buf = [], -99.0, []
    for t, s in segs:
        if t - last >= 20 and buf:
            lines.append(f"[{int(last)}] " + " ".join(buf))
            buf = []
        if not buf:
            last = t
        buf.append(s)
    if buf:
        lines.append(f"[{int(last)}] " + " ".join(buf))
    text = "\n".join(lines)[:90000]
    p = it.get("pick") or {}
    try:
        r = llm.structured(SYS_EXT, f"영상: {it['title']} ({it['channel']})\n말하는 사람(짐작): {p.get('speaker')}\n주제 질문: {p.get('theme')}\n\n{text}",
                           Extract, task="insights")
    except Exception as e:  # noqa: BLE001
        print(f"  ! 판단 뽑기 실패 {it['id']}: {str(e)[:120]}", file=sys.stderr)
        return None
    return r.model_dump()


# ── 4) 장부·보고 ─────────────────────────────────────────────────────
def _ledger() -> dict:
    return _load("ledger.json", {"themes": {}, "seen": {}})


def mark(vid: str, status: str, our: str = "") -> None:
    L = _ledger()
    s = L["seen"].setdefault(vid, {})
    s["status"] = status
    if our:
        s["our"] = our
        s["made_at"] = datetime.now(KST).isoformat(timespec="minutes")
        if s.get("published"):
            s["lag_days"] = round(_age_days(s["published"], datetime.now(timezone.utc)), 1)
    _save("ledger.json", L)
    print(f"[insights] {vid} → {status}" + (f" · 우리 {our} · 공개 뒤 {s.get('lag_days', '?')}일" if our else ""))


def run(extract_n: int | None = None, use_llm: bool = True, day: str = "") -> Path:
    cfg = _cfg()
    now = datetime.now(timezone.utc)
    day = day or datetime.now(KST).date().isoformat()
    L = _ledger()
    print(f"[insights] {day} · 자리 {len(cfg.get('venues') or [])}곳 훑기 (목록·정보만)")
    items = scan_venues(cfg, now)
    print(f"[insights] 자리에서 {len(items)}편 · 목록 밖 찾기")
    items += discover(cfg, now)
    uniq = {}
    for it in items:
        if it["id"] not in uniq or it["via"] == "자리":
            uniq[it["id"]] = it
    items = list(uniq.values())
    new = [it for it in items if it["id"] not in L["seen"]]
    todo = [it for it in items if not (L["seen"].get(it["id"]) or {}).get("pick")]   # --no-llm 로 먼저 본 것도 거름
    print(f"[insights] 후보 {len(items)}편 (새로 본 것 {len(new)}편)")
    if use_llm and todo:
        picks = classify(todo, list(L["themes"]))
        for it in todo:
            it["pick"] = picks.get(it["id"])
    for it in items:
        old = L["seen"].get(it["id"])
        if old and old.get("pick") and not it.get("pick"):
            it["pick"] = old["pick"]
        it["score"] = score(it, cfg)
        keep = {k: it.get(k) for k in ("title", "channel", "area", "minutes", "views", "published", "via", "pick", "score", "url")}
        L["seen"][it["id"]] = {**(old or {}), **keep, "first_seen": (old or {}).get("first_seen", day)}
    ranked = sorted([it for it in items if it["score"] > 0], key=lambda x: -x["score"])
    n = int(cfg.get("extract_top", 8) if extract_n is None else extract_n)
    done = 0
    if use_llm:
        for it in ranked:
            if done >= n:
                break
            s = L["seen"][it["id"]]
            if s.get("extracted") or it["id"].startswith("hn:") or s.get("tries", 0) >= 3:
                continue
            ex = extract(it)
            s["tries"] = s.get("tries", 0) + 1   # 자막 요청 제한(429)이면 다음 차례에 다시 (최대 3번)
            if ex:
                s["extracted"] = day
            done += 1
            if not ex:
                continue
            th = ex["theme"] or (it.get("pick") or {}).get("theme") or "기타"
            T = L["themes"].setdefault(th, {"first": day, "judgments": []})
            for j in ex["judgments"]:
                T["judgments"].append({**j, "speaker": ex["speaker"], "id": it["id"], "title": it["title"], "channel": it["channel"],
                                       "published": it.get("published", ""), "day": day,
                                       "link": f"https://youtu.be/{it['id']}?t={j['at']}"})
            print(f"  · {ex['speaker']} — {th} · 판단 {len(ex['judgments'])}개")
    _save("ledger.json", L)
    md = to_md(L, ranked, day)
    f = DIR / f"{day}.md"
    f.write_text(md, encoding="utf-8")
    print(f"[insights] → {f}")
    return f


def _mmss(s: int) -> str:
    return f"{s // 60}:{s % 60:02d}"


def candidates(L: dict) -> list[tuple[str, dict, str]]:
    """영상 후보: 판단이 둘 이상의 입장으로 갈렸거나, 한 사람이라도 날짜·숫자 있는 판단이 둘 이상."""
    out = []
    for th, T in L["themes"].items():
        js = T["judgments"]
        stances = {j.get("stance") for j in js}
        speakers = {j.get("speaker") for j in js}
        dated = [j for j in js if j.get("horizon")]
        if len(speakers) >= 2 and len(stances - {"mixed"}) >= 2:
            out.append((th, T, "맞서는 판단 있음 — 맞대기 편"))
        elif len(dated) >= 2:
            out.append((th, T, "한 사람의 구체적 판단 — 드러켄밀러형 편"))
    return sorted(out, key=lambda x: -len(x[1]["judgments"]))


def to_md(L: dict, ranked: list[dict], day: str) -> str:
    md = [f"# 인사이트 — {day}", "",
          "> 소식이 아니라 '앞으로 어떻게 되나'에 대한 판단을 모읍니다 (manual/09 §5-00, docs/70). 결과는 단서 — 대본의 말은 원본에서 다시 확인.", ""]
    md += ["## ① 영상 후보 (판단 + 반대 판단 + 원본)", ""]
    cs = candidates(L)
    if not cs:
        md.append("(아직 없음 — 장부가 쌓이면 나옵니다)")
    for th, T, why in cs[:8]:
        md.append(f"### {th}  · {why}")
        for j in T["judgments"][-6:]:
            md.append(f"- **{j['speaker']}** ({j['channel']}, [{_mmss(int(j['at']))}]({j['link']})) — {j['claim']}"
                      + (f" · 시간표 {j['horizon']}" if j.get("horizon") else "") + f" · 입장 {j.get('stance')}")
            md.append(f"  - 원문: \"{j['quote'][:220]}\"  / 근거: {j['basis'][:160]}")
        md.append("")
    md += ["", "## ② 오늘 높은 순 (거르기 결과)", "", "| 점수 | 영역 | 누가 · 무엇 (짐작) | 영상 | 경로 |", "|---|---|---|---|---|"]
    for it in ranked[:25]:
        p = it.get("pick") or {}
        link = it.get("url") or f"https://youtu.be/{it['id']}"
        md.append(f"| {it['score']} | {p.get('area', it['area'])}→{p.get('route', '')} | {p.get('speaker', '')} · {p.get('claim_guess', '')[:70]} "
                  f"| [{it['title'][:60]}]({link}) · {it['channel']} · {it['minutes']}분 · 조회 {it['views']:,} · {it['age']}일 전 | {it['via']} |")
    md += ["", "## ③ 주제별 판단 장부", ""]
    for th, T in sorted(L["themes"].items(), key=lambda x: -len(x[1]["judgments"]))[:30]:
        sp = sorted({j['speaker'] for j in T['judgments']})
        md.append(f"- **{th}** — 판단 {len(T['judgments'])}개 · {', '.join(sp)[:120]}")
    return "\n".join(md) + "\n"
