"""원본 레이더 — 사람의 말(원본 영상)과 큰 날(사건)을 매일 추적한다 (2026-11-23 사용자:
"우리도 사람의 말이나 사건형 원본형처럼 이를 추적할 수 있었으면 해요").

식스시그마·월가인사이드·월터의 월가노트를 보면 출발점은 지표가 아니라 '이름 있는 사람의 말'이고, 시점이 둘이다 (docs/63):
  · 원본형 — 거물 인터뷰·팟캐스트·행사 발언이 공개되고 2~9일 안에 그 한 편을 깊게 (식스시그마 팔란티어 CEO 편 12만)
  · 사건형 — 지수가 크게 움직인 다음 날 "이름 있는 사람들은 뭐라 하나" (월가인사이드 급락 뒤 월가 10명 72만)

    python -m ytflow radar                    # 오늘: 원본 후보 + 큰 날 판단 → inbox/radar/<날짜>.md
    python -m ytflow radar --people 드러켄밀러,젠슨 황   # 몇 사람만
    python -m ytflow radar --no-kr            # 국내 해설(경쟁) 확인 생략 (빠르게)
    python -m ytflow radar --mark <영상id> made|skip|watch   # 추적표 상태 바꾸기

찾는 방법: YouTube 검색 결과 목록(이번 주 필터)과 영상 정보만 읽는다 — 영상·음성은 내려받지 않는다.
봇 확인이 뜨면 우회하지 않고 그 사람을 건너뛴다. 결과는 '단서': 대본의 발언은 원본 영상에서 직접 확인 (manual/09 §3-5).
"""
from __future__ import annotations

import json
import math
import re
import sys
import urllib.parse
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from .. import config

KST = timezone(timedelta(hours=9))
WEEK = "EgIIAw%253D%253D"   # 검색 필터: 이번 주 업로드


def _cfg() -> dict:
    import yaml
    r = yaml.safe_load((config.ROOT / "config" / "radar.yaml").read_text(encoding="utf-8")) or {}
    w = yaml.safe_load((config.ROOT / "config" / "ceo_watch.yaml").read_text(encoding="utf-8")) or {}
    people = [p for p in (w.get("ceos") or []) if p.get("lang") != "ko"] + list(r.get("extra") or [])
    r["people"] = people
    return r


def _ydl(flat: bool):
    import yt_dlp
    return yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True, "skip_download": True, "ignoreerrors": True, "extract_flat": flat})


def _search(y, q: str, n: int = 20) -> list[dict]:
    try:
        r = y.extract_info(f"https://www.youtube.com/results?search_query={urllib.parse.quote_plus(q)}&sp={WEEK}", download=False) or {}
    except Exception as e:  # noqa: BLE001 — 봇 확인·접속 실패: 우회하지 않고 건너뜀
        print(f"  ! 검색 실패 {q}: {str(e)[:80]}", file=sys.stderr)
        return []
    return [e for e in (r.get("entries") or [])[:n] if e and e.get("id")]


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").lower())


def _origness(e: dict, p: dict, cfg: dict) -> tuple[int, str]:
    """원본 같은 정도: 공식·방송·행사 채널 +3, 인증 채널 +1, 제목의 '인터뷰·행사' 말 +1, 해설 말 −2, 이름 없는 제목 −3."""
    t, ch = _norm(e.get("title")), (e.get("channel") or "")
    last = p["en"].split()[-1].lower()
    s, why = 0, []
    official = any(ch.lower() == o.lower() for o in cfg.get("originals") or [])
    full = _norm(p["en"]) in t
    # 성만 맞는 제목은 원본 채널일 때만 (Powell·Ellison 처럼 같은 성의 다른 사람이 섞임)
    if not full and not (re.search(rf"\b{re.escape(last)}\b", t) and official):
        return -3, "제목에 이름 없음"
    if re.search(r"[஀-௿ऀ-ॿ一-鿿぀-ヿЀ-ӿ]", e.get("title") or ""):
        return -3, "다른 나라 해설"   # 타밀·힌디·중국어·일본어·러시아어 제목 = 남의 해설
    if official:
        s += 3
        why.append("원본 채널")
    if e.get("channel_is_verified"):
        s += 1
        why.append("인증")
    if any(w in t for w in cfg.get("original_words") or []):
        s += 1
        why.append("인터뷰·행사")
    if re.search(rf"\b(on|about) ({re.escape(last)}|{re.escape(_norm(p['en']))})\b", t):   # 'Jeff Bezos on Jensen Huang' — 다른 사람이 그 사람을 말함
        s -= 2
        why.append("남이 말함")
    if any(w in t for w in cfg.get("commentary_words") or []):
        s -= 2
        why.append("해설 말투")
    if re.search(r"[가-힣]", e.get("title") or ""):
        s -= 2
        why.append("국내 해설")
    yrs = [int(y) for y in re.findall(r"\b(19[89]\d|20[0-4]\d)\b", e.get("title") or "")]
    if yrs and max(yrs) < datetime.now(KST).year - 1:   # 'Jensen Huang in 2009' — 옛 영상 다시 올린 것
        s -= 3
        why.append("옛 영상")
    return s, "·".join(why)


def _details(y, vid: str) -> dict:
    try:
        r = y.extract_info(f"https://www.youtube.com/watch?v={vid}", download=False) or {}
    except Exception:  # noqa: BLE001
        return {}
    return {k: r.get(k) for k in ("upload_date", "view_count", "like_count", "comment_count", "channel_follower_count", "duration", "channel")} | \
        {"desc": (r.get("description") or "")[:400], "chapters": [c.get("title") for c in (r.get("chapters") or [])][:12]}


def _fresh(age: float, window: float) -> float:
    if age <= 1:
        return 1.0
    if age <= 3:
        return 0.9
    if age <= 5:
        return 0.75
    if age <= window:
        return 0.5
    return 0.15


def _kr_cover(y, p: dict, cfg: dict) -> dict:
    """국내 해설: 이번 주 한국어 제목에 그 사람 이름이 들어간 영상 수·최고 조회·누가 (경쟁 채널 표시)."""
    ko = p["name"].split()[-1] if len(p["name"]) > 4 else p["name"]
    hits = []
    for e in _search(y, p["name"], 25):
        ch = e.get("channel") or e.get("uploader") or ""
        if ko in (e.get("title") or "") and re.search(r"[가-힣]{2}", (e.get("title") or "").replace(ko, "")) and (e.get("duration") or 0) >= 90 and ch:
            hits.append({"title": e.get("title"), "channel": ch, "views": e.get("view_count") or 0, "id": e["id"],
                         "comp": any(c in ch for c in cfg.get("competitors") or [])})
    hits.sort(key=lambda h: -h["views"])
    return {"n": len(hits), "top": hits[:3], "max": hits[0]["views"] if hits else 0, "comp": [h["channel"] for h in hits if h["comp"]]}


def _event(day: str, cfg: dict) -> dict:
    from . import daily
    from .marketdata import fetch
    cache = Path(config.CACHE_DIR) / "radar" / "prices"
    out = []
    names = dict((t, n) for t, n, _ in daily.INDICES)
    for t in cfg.get("event_indices") or []:
        try:
            p = daily._pct(fetch(t, "1mo", cache), day, t)
        except Exception:  # noqa: BLE001
            p = None
        if p:
            out.append(dict(p, ticker=t, name=names.get(t, t)))
    th = float(cfg.get("event_move_pct", 3.0))
    big = [x for x in out if abs(x["pct"]) >= th]
    return {"indices": out, "big": big, "threshold": th}


def _event_voices(cfg: dict, people: list) -> list[dict]:
    """큰 날: 무게 2.5 이상인 사람의 지난 36시간 발언 보도 (says·warns·sees·말했다 …) — 단서."""
    from .trends import google_news
    say = re.compile(r"\b(says|said|warns|sees|expects|thinks|calls|told|believes|predicts)\b|말했|경고|전망|진단", re.I)
    w = cfg.get("weight") or {}
    out = []
    for p in people:
        if w.get(p["name"], 2) < 2.5:
            continue
        try:
            items = google_news(p.get("q") or p["en"], "en", 36)
        except Exception:  # noqa: BLE001
            items = []
        items = [i for i in items if say.search(i["title"])][:2]
        if items:
            out.append({"name": p["name"], "company": p.get("company", ""), "news": items})
    return out


def _tracker_path() -> Path:
    return config.ROOT / "inbox" / "radar" / "tracker.json"


def _tracker() -> dict:
    f = _tracker_path()
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}


def mark(vid: str, status: str) -> None:
    t = _tracker()
    if vid not in t:
        raise SystemExit(f"추적표에 없음: {vid}")
    t[vid]["status"] = status
    t[vid]["status_at"] = datetime.now(KST).isoformat(timespec="minutes")
    _tracker_path().write_text(json.dumps(t, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[radar] {vid} → {status}")


def run(day: str = "", only: list[str] | None = None, kr: bool = True, per_person: int = 2) -> Path:
    cfg = _cfg()
    today = datetime.now(KST).date()
    day = day or today.isoformat()
    window = float(cfg.get("window_days", 9))
    weight = cfg.get("weight") or {}
    people = cfg["people"]
    if only:
        people = [p for p in people if any(o in p["name"] or o.lower() in p["en"].lower() for o in only)]
    print(f"[radar] {day} · 사람 {len(people)}명 · 원본 찾기 (이번 주 검색, 내려받기 없음)")
    found, no_orig = [], []
    with _ydl(True) as yf, _ydl(False) as yd:
        for p in people:
            es = _search(yf, f"{p['en']} interview", 20)
            cands = []
            for e in es:
                if (e.get("duration") or 0) < 360:
                    continue
                s, why = _origness(e, p, cfg)
                if s >= 2:   # 원본 채널이거나, 인증 + 인터뷰·행사 말
                    cands.append((s, e, why))
            cands.sort(key=lambda x: (-x[0], -(x[1].get("view_count") or 0)))
            if not cands:
                if any(p["en"].split()[-1].lower() in _norm(e.get("title")) for e in es):
                    no_orig.append(p["name"])
                continue
            for s, e, why in [c for k_, c in enumerate(cands[:per_person]) if k_ == 0 or c[0] >= 3]:
                d = _details(yd, e["id"])
                up = d.get("upload_date")
                age = (today - date(int(up[:4]), int(up[4:6]), int(up[6:]))).days if up else None
                if age is not None and age > window + 5:
                    continue
                views = d.get("view_count") or e.get("view_count") or 0
                w = float(weight.get(p["name"], 2))
                score = w * _fresh(age if age is not None else window, window) * (1 + math.log10(views + 10) / 3) * (1 + min(s, 5) / 10)
                found.append({"person": p["name"], "en": p["en"], "company": p.get("company", ""), "weight": w, "id": e["id"],
                              "url": f"https://www.youtube.com/watch?v={e['id']}", "title": e.get("title"), "channel": d.get("channel") or e.get("channel") or e.get("uploader") or "?",
                              "duration_min": round((e.get("duration") or 0) / 60), "upload_date": up, "age_days": age, "views": views,
                              "orig": s, "orig_why": why, "score": round(score, 2), "chapters": d.get("chapters") or [], "desc": d.get("desc", "")})
            print(f"  · {p['name']}: 원본 후보 {len(cands)}", file=sys.stderr)
        found.sort(key=lambda f: -f["score"])
        # 같은 사람은 한 줄로 합쳐 국내 해설 확인 (사람마다 검색 한 번)
        covered = {}
        if kr:
            for f in found:
                if f["person"] in covered or len(covered) >= 12:
                    continue
                p = next(x for x in people if x["name"] == f["person"])
                covered[f["person"]] = _kr_cover(yf, p, cfg)
        for f in found:
            f["kr"] = covered.get(f["person"])
    ev = _event(day, cfg)
    voices = _event_voices(cfg, people) if ev["big"] else []
    # 추적표: 처음 본 날·상태 (같은 원본을 매일 다시 올리지 않게, 놓친 마감 보기)
    tr = _tracker()
    for f in found:
        if f["id"] not in tr:
            tr[f["id"]] = {"first_seen": day, "person": f["person"], "title": f["title"], "url": f["url"],
                           "upload_date": f["upload_date"], "status": "new"}
        f["status"] = tr[f["id"]]["status"]
        f["first_seen"] = tr[f["id"]]["first_seen"]
    odir = config.ROOT / "inbox" / "radar"
    odir.mkdir(parents=True, exist_ok=True)
    _tracker_path().write_text(json.dumps(tr, ensure_ascii=False, indent=1), encoding="utf-8")
    res = {"day": day, "event": ev, "voices": voices, "originals": found, "no_original": no_orig}
    (odir / f"{day}.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    md = to_md(res, window)
    (odir / f"{day}.md").write_text(md, encoding="utf-8")
    print(f"[radar] → {odir / (day + '.md')} · 원본 {len(found)} · 큰 날 {'예' if ev['big'] else '아니오'}")
    return odir / f"{day}.md"


def _deadline(f: dict, window: float) -> str:
    if not f.get("upload_date"):
        return "공개일 확인"
    up = f["upload_date"]
    d0 = date(int(up[:4]), int(up[4:6]), int(up[6:]))
    best, last = d0 + timedelta(days=3), d0 + timedelta(days=int(window))
    now = datetime.now(KST).date()
    if now > last:
        return f"늦음 ({last:%m/%d} 지남)"
    if now > best:
        return f"서둘러야 함 — {last:%m/%d} 넘기면 늦음"
    return f"{best:%m/%d}까지 좋음 · {last:%m/%d} 넘기면 늦음"


def _kr_text(k: dict | None) -> str:
    if not k:
        return "—"
    if not k["n"] or not k["top"]:
        return "아직 없음 → **선점**"
    top = k["top"][0]
    if not top["views"]:
        return f"{k['n']}편 ({top['channel']} 등)"
    comp = f" · 경쟁: {', '.join(sorted(set(k['comp'])))}" if k["comp"] else ""
    return f"{k['n']}편, 최고 {top['views']:,}회 ({top['channel']}){comp}"


def to_md(r: dict, window: float = 9) -> str:
    ev, found = r["event"], r["originals"]
    L = [f"# 원본 레이더 — {r['day']}", "",
         "> 단서 목록입니다. 대본에 쓰는 발언은 원본 영상·공식 기록에서 직접 확인하고, 인용은 짧게(한 장면 20초·한 편 60초 안팎, manual/09 §3-5).", ""]
    L += ["## ⓐ 오늘의 판단"]
    live = [f for f in found if f["status"] == "new" and f.get("age_days") is not None and f["age_days"] <= window]
    if ev["big"]:
        mv = ", ".join(f"{x['name']} {x['pct']:+.2f}%" for x in ev["big"])
        L.append(f"- **큰 날 (사건형 먼저)**: {mv} — 24~48시간 안에 \"이름 있는 사람들은 뭐라 했나\" 편. 아래 ⓑ 의 발언 단서에서 3~6명.")
    if live:
        f = live[0]
        L.append(f"- **원본형 1순위**: {f['person']} — 〈{f['title']}〉 ({f['channel']}, {f['duration_min']}분, 공개 {f.get('age_days')}일 전, "
                 f"조회 {f['views']:,}) · {_deadline(f, window)} · 국내 해설 {_kr_text(f.get('kr'))}")
    if not ev["big"] and not live:
        L.append("- 큰 날도, 새 원본도 없음 → 평소 브리핑(daily_brief) 주제로.")
    L += ["", f"## ⓑ 큰 날인가 (사건형, 기준 ±{ev['threshold']:g}%)", "", "| 지수 | 날짜 | 등락 |", "|---|---|---|"]
    for x in ev["indices"]:
        L.append(f"| {x['name']} | {x['date']} | {'**' if x in ev['big'] else ''}{x['pct']:+.2f}%{'**' if x in ev['big'] else ''} |")
    if r["voices"]:
        L += ["", "발언 단서 (지난 36시간 보도 제목 — 원문 확인 필요):"]
        for v in r["voices"]:
            for n in v["news"]:
                L.append(f"- {v['name']} ({v['company']}): {n['title']} — {n['source']} [{n['published'][:16]}]({n['url']})")
    L += ["", "## ⓒ 원본 후보 (원본형 — 공개 2~9일 안, 점수 = 사람 무게 × 새로움 × 조회 × 원본다움)", "",
          "| # | 사람 | 원본 | 공개 | 조회 | 국내 해설 | 마감 | 상태 | 점수 |", "|---|---|---|---|---|---|---|---|---|"]
    for i, f in enumerate(found[:25], 1):
        L.append(f"| {i} | {f['person']} | [{f['title'][:60]}]({f['url']}) · {f['channel']} · {f['duration_min']}분 ({f['orig_why']}) | "
                 f"{f.get('upload_date') or '?'} ({f.get('age_days')}일) | {f['views']:,} | {_kr_text(f.get('kr'))} | {_deadline(f, window)} | {f['status']} | {f['score']} |")
    tops = [f for f in found[:5] if f.get("chapters")]
    if tops:
        L += ["", "### 상위 원본의 챕터 (어느 대목을 자를지 고르는 단서)"]
        for f in tops:
            L.append(f"- {f['person']} 〈{f['title'][:50]}〉: " + " / ".join(f["chapters"][:10]))
    if r["no_original"]:
        L += ["", "## ⓓ 이번 주 해설은 있는데 원본을 못 찾은 사람 (직접 찾아보기)", "- " + ", ".join(r["no_original"])]
    L += ["", "## 고르는 기준 (docs/63)",
          "- 사람의 무게 > 주제: 같은 소재라도 이름 있는 사람의 말이 붙으면 크게 봄.",
          "- 시점: 사건형은 24~48시간, 원본형은 공개 2~9일. 국내에 이미 크게 터졌으면 같은 말 반복 대신 다른 각도(원문 해부·한국 계좌로 연결).",
          "- 끝은 한국 투자자의 종목·계좌로. 설명란에 [원본] 번호 목록(채널·날짜·주소).",
          "- 상태 바꾸기: `python -m ytflow radar --mark <영상id> made|skip|watch`"]
    return "\n".join(L) + "\n"
