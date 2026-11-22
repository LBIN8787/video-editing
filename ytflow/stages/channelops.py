"""채널 운영·분석 — 올린 영상의 수치를 모으고, 무엇이 앞서고 처졌는지·어디서 빠졌는지 보고서로 (docs/63-channel-ops.md).

    python -m ytflow ops                 # config/channel_ops.yaml 의 모든 채널: 수집 → 보고서
    python -m ytflow ops market --no-report
    python -m ytflow ops curiosity --report-only

2026-11-23 사용자: "앞으로 내 채널은 네가 운영하고 네가 분석하길 바래"

모으는 것 (권한별):
- Data API (지금 토큰 youtube.force-ssl 로 됨): 채널·영상의 조회·좋아요·댓글, 공개 상태, 댓글 본문, 올린 자막(장면 찾기용)
- Analytics API (yt-analytics.readonly — scripts/youtube_auth.py 로 한 번 다시 받아야 함): 평균 시청 비율·시간, 구독 증가,
  유입 경로, 시청 지속 곡선(audienceWatchRatio·relativeRetentionPerformance)
- Reporting API (같은 권한): 노출 수·노출 클릭률 (channel_reach_basic_a1 — 작업을 만든 다음 날부터 매일 보고서가 쌓임)

저장: data/analytics/<채널>/ (작은 csv·json, git) · 보고서: channels/<채널 폴더>/ops/<YYYYMMDD>.md
판정은 고정 숫자가 아니라 같은 채널 영상끼리 견줌 (manual README §5 — 숫자 상한·하한 대신 목적).
댓글 작성자 이름은 저장하지 않음. 답글·삭제·공개 상태 변경은 이 명령이 하지 않음(보고서에 제안만).
"""
from __future__ import annotations

import csv
import datetime as dt
import json
import re
import statistics
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

from .. import config
from . import ytpublish as yp

KST = dt.timezone(dt.timedelta(hours=9))
DATA = config.ROOT / "data" / "analytics"
YT = "https://www.googleapis.com/youtube/v3/"
YA = "https://youtubeanalytics.googleapis.com/v2/reports"
YR = "https://youtubereporting.googleapis.com/v1/"
REACH = "channel_reach_basic_a1"
BASIC = ["views", "engagedViews", "estimatedMinutesWatched", "averageViewDuration", "averageViewPercentage",
         "subscribersGained", "subscribersLost", "likes", "shares", "comments"]
TRAFFIC_KO = {"YT_SEARCH": "유튜브 검색", "SUBSCRIBER": "구독 피드", "RELATED_VIDEO": "추천(관련 영상)",
              "BROWSE": "탐색(홈)", "EXT_URL": "외부 링크", "NO_LINK_OTHER": "직접·기타", "PLAYLIST": "재생목록",
              "NOTIFICATION": "알림", "SHORTS": "쇼츠 피드", "YT_CHANNEL": "채널 페이지", "END_SCREEN": "최종 화면",
              "YT_OTHER_PAGE": "유튜브 기타", "HASHTAGS": "해시태그", "ANNOTATION": "카드"}


class NoScope(Exception):
    pass


def cfg() -> dict:
    return yaml.safe_load((config.ROOT / "config" / "channel_ops.yaml").read_text(encoding="utf-8"))


def now() -> dt.datetime:
    return dt.datetime.now(KST)


def _call(tok: str, url: str, params: dict | None = None, method: str = "GET", body=None, raw: bool = False):
    if params:
        url += ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
    h = {"Authorization": f"Bearer {tok}"}
    data = None
    if body is not None:
        h["Content-Type"] = "application/json"
        data = json.dumps(body).encode()
    try:
        with urllib.request.urlopen(urllib.request.Request(url, data=data, method=method, headers=h), timeout=120) as r:
            b = r.read()
            return b if raw else (json.loads(b) if b else {})
    except urllib.error.HTTPError as e:
        msg = e.read()[:400].decode("utf-8", "replace")
        if e.code in (401, 403) and ("insufficient" in msg.lower() or "scope" in msg.lower() or "forbidden" in msg.lower()
                                     or "permission" in msg.lower()):
            raise NoScope(msg)
        raise RuntimeError(f"{method} {url.split('?')[0]} → {e.code}: {msg}")


def _secs(iso: str) -> int:
    m = re.match(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or "")
    d, h, mi, s = (int(x or 0) for x in m.groups()) if m else (0, 0, 0, 0)
    return d * 86400 + h * 3600 + mi * 60 + s


def _ts(s: str) -> dt.datetime:
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(KST)


def project_map() -> dict:
    """video_id → 프로젝트 폴더 이름 (05_edit/youtube_publish*.json)."""
    out = {}
    for f in sorted((config.ROOT / "projects").glob("*/05_edit/youtube_publish*.json")):
        try:
            vid = json.loads(f.read_text(encoding="utf-8")).get("video_id")
        except Exception:
            continue
        if vid:
            out[vid] = f.parts[-3]
    return out


# ---------------------------------------------------------------- 수집

def fetch(name: str, ch: dict) -> dict:
    d = DATA / name
    d.mkdir(parents=True, exist_ok=True)
    tok = yp._token(ch.get("credentials") or None)
    me = _call(tok, YT + "channels", {"part": "snippet,statistics,contentDetails", "mine": "true"})["items"][0]
    up = me["contentDetails"]["relatedPlaylists"]["uploads"]
    ids, page = [], None
    while True:
        p = {"part": "contentDetails", "maxResults": 50, "playlistId": up}
        if page:
            p["pageToken"] = page
        r = _call(tok, YT + "playlistItems", p)
        ids += [i["contentDetails"]["videoId"] for i in r.get("items", [])]
        page = r.get("nextPageToken")
        if not page:
            break
    pm = project_map()
    vids = []
    for k in range(0, len(ids), 50):
        r = _call(tok, YT + "videos", {"part": "snippet,statistics,status,contentDetails", "id": ",".join(ids[k:k + 50])})
        for x in r.get("items", []):
            s, st = x.get("statistics", {}), x["status"]
            vids.append({"id": x["id"], "title": x["snippet"]["title"], "published": x["snippet"]["publishedAt"],
                         "publish_at": st.get("publishAt"), "privacy": st["privacyStatus"],
                         "duration": _secs(x["contentDetails"]["duration"]),
                         "views": int(s.get("viewCount", 0)), "likes": int(s.get("likeCount", 0)),
                         "comments": int(s.get("commentCount", 0)), "project": pm.get(x["id"])})
            dur = vids[-1]["duration"]
            vids[-1]["chapters"] = len(parse_chapters(x["snippet"].get("description", "")))
            vids[-1]["chapter_problems"] = chapter_problems(x["snippet"].get("description", ""), dur)
            if st["privacyStatus"] == "public":
                vids[-1]["chapters_shown"] = chapters_shown(x["id"])
    t = now().isoformat(timespec="minutes")
    chan = {"id": me["id"], "title": me["snippet"]["title"], "handle": me["snippet"].get("customUrl"),
            "subscribers": int(me["statistics"].get("subscriberCount", 0)),
            "views": int(me["statistics"].get("viewCount", 0)), "videos": int(me["statistics"].get("videoCount", 0)),
            "at": t}
    (d / "channel.json").write_text(json.dumps(chan, ensure_ascii=False, indent=1), encoding="utf-8")
    (d / "videos.json").write_text(json.dumps(vids, ensure_ascii=False, indent=1), encoding="utf-8")
    new = not (d / "snapshots.csv").exists()
    with open(d / "snapshots.csv", "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["at", "video_id", "privacy", "views", "likes", "comments"])
        for v in vids:
            w.writerow([t, v["id"], v["privacy"], v["views"], v["likes"], v["comments"]])
        w.writerow([t, "_channel", "", chan["views"], chan["subscribers"], ""])
    out = {"channel": chan, "videos": vids, "analytics": None, "reach": None}
    out["comments"] = fetch_comments(tok, d, chan["id"])
    try:
        out["analytics"] = fetch_analytics(tok, d, vids)
    except NoScope:
        out["analytics"] = {"ok": False, "why": f"분석 권한 없음 → 사용자 PC 에서 한 번: python scripts/youtube_auth.py "
                                               f"<client_secret.json>{' --name ' + ch['credentials'] if ch.get('credentials') else ''} --to-github"}
    try:
        out["reach"] = fetch_reach(tok, d)
    except NoScope:
        out["reach"] = {"ok": False, "why": "분석 권한 없음 (위와 같음)"}
    except RuntimeError as e:
        out["reach"] = {"ok": False, "why": str(e)[:200]}
    return out


# ---------------------------------------------------------------- 진행 바 챕터 (2026-11-23 사용자: "영상바에 타임라인이 안나타나더라고")
# 유튜브 공식 조건(support.google.com/youtube/answer/9884579): 설명란 첫 타임코드 00:00 · 3개 이상 · 오름차순 · 각 10초 이상,
# 그리고 채널이 '고급 기능'을 쓸 수 있어야 함(Studio 설정 → 채널 → 기능 사용 자격). 설명란이 맞는데도 안 보이면 거의 이것.
TS_LINE = re.compile(r"^\s*\(?((?:\d{1,2}:)?\d{1,2}:\d{2})\)?\s*[-–—:]?\s+(\S.*)$")


def _sec(ts: str) -> int:
    p = [int(x) for x in ts.split(":")]
    return p[0] * 3600 + p[1] * 60 + p[2] if len(p) == 3 else p[0] * 60 + p[1]


def parse_chapters(desc: str) -> list:
    """설명란에서 첫 00:00 줄부터 이어지는 타임코드 줄들 → [(초, 제목)]."""
    out, started = [], False
    for ln in (desc or "").splitlines():
        m = TS_LINE.match(ln)
        if m and (started or _sec(m.group(1)) == 0):
            started = True
            out.append((_sec(m.group(1)), m.group(2).strip()))
        elif started and ln.strip():
            break   # 챕터 목록이 끝남
    return out


def chapter_problems(desc: str, duration: int) -> list:
    ch = parse_chapters(desc)
    if not ch:
        any_ts = any(TS_LINE.match(ln) for ln in (desc or "").splitlines())
        return ["첫 타임코드가 00:00 이 아님" if any_ts else "설명란에 타임코드 없음"]
    p = []
    if len(ch) < 3:
        p.append(f"타임코드 {len(ch)}개 (3개 이상이어야 함)")
    for (a, ta), (b, tb) in zip(ch, ch[1:]):
        if b <= a:
            p.append(f"순서가 거꾸로: {ta} → {tb}")
        elif b - a < 10:
            p.append(f"10초보다 짧은 챕터: '{ta}' ({b - a}초)")
    if duration and duration - ch[-1][0] < 10:
        p.append(f"마지막 챕터 '{ch[-1][1]}' 이 10초보다 짧거나 영상 밖")
    return p


def chapters_shown(video_id: str):
    """공개 시청 페이지에 챕터가 실제로 붙었나 (True/False, 확인 못 하면 None). 봇 확인이 뜨면 우회하지 않고 None."""
    try:
        req = urllib.request.Request(f"https://www.youtube.com/watch?v={video_id}", headers={"User-Agent": "Mozilla/5.0"})
        h = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
    except Exception:
        return None
    if '"videoDetails"' not in h:
        return None
    return '"chapterRenderer"' in h


def fetch_comments(tok: str, d: Path, channel_id: str) -> dict:
    f = d / "comments.jsonl"
    seen = set()
    if f.exists():
        seen = {json.loads(ln)["id"] for ln in f.read_text(encoding="utf-8").splitlines() if ln.strip()}
    new = []
    try:
        r = _call(tok, YT + "commentThreads", {"part": "snippet", "allThreadsRelatedToChannelId": channel_id,
                                              "maxResults": 100, "order": "time", "textFormat": "plainText"})
    except (NoScope, RuntimeError) as e:
        return {"ok": False, "why": str(e)[:200], "new": []}
    for it in r.get("items", []):
        if it["id"] in seen:
            continue
        top = it["snippet"]["topLevelComment"]["snippet"]
        new.append({"id": it["id"], "video_id": it["snippet"].get("videoId"), "at": top["publishedAt"],
                    "text": top.get("textDisplay", "")[:1000], "likes": top.get("likeCount", 0),
                    "replies": it["snippet"].get("totalReplyCount", 0)})
    if new:
        with open(f, "a", encoding="utf-8") as fh:
            for c in sorted(new, key=lambda c: c["at"]):
                fh.write(json.dumps(c, ensure_ascii=False) + "\n")
    return {"ok": True, "new": new}


def fetch_analytics(tok: str, d: Path, vids: list) -> dict:
    pub = [v for v in vids if v["privacy"] == "public"]
    if not pub:
        return {"ok": True, "videos": {}}
    start = min(_ts(v["published"]) for v in pub).date().isoformat()
    end = now().date().isoformat()
    res = {}
    r = _call(tok, YA, {"ids": "channel==MINE", "startDate": start, "endDate": end, "dimensions": "video",
                        "metrics": ",".join(BASIC), "filters": "video==" + ",".join(v["id"] for v in pub),
                        "maxResults": 200, "sort": "-views"})
    cols = [h["name"] for h in r.get("columnHeaders", [])]
    for row in r.get("rows", []):
        res[row[0]] = dict(zip(cols[1:], row[1:]))
    vd = d / "videos"
    vd.mkdir(exist_ok=True)
    for v in pub:
        a = res.setdefault(v["id"], {})
        try:
            t = _call(tok, YA, {"ids": "channel==MINE", "startDate": start, "endDate": end,
                                "dimensions": "insightTrafficSourceType", "metrics": "views",
                                "filters": f"video=={v['id']}", "sort": "-views"})
            a["traffic"] = {row[0]: row[1] for row in t.get("rows", [])}
        except RuntimeError:
            pass
        try:
            rt = _call(tok, YA, {"ids": "channel==MINE", "startDate": start, "endDate": end,
                                 "dimensions": "elapsedVideoTimeRatio",
                                 "metrics": "audienceWatchRatio,relativeRetentionPerformance",
                                 "filters": f"video=={v['id']};audienceType==ORGANIC"})
            a["retention"] = rt.get("rows", [])
        except RuntimeError:
            pass
        (vd / f"{v['id']}.json").write_text(json.dumps(a, ensure_ascii=False, indent=1), encoding="utf-8")
    return {"ok": True, "videos": res}


def fetch_reach(tok: str, d: Path) -> dict:
    """Reporting API 노출·클릭률: 작업이 없으면 만들고, 새 보고서를 내려받아 영상별로 더함."""
    jobs = _call(tok, YR + "jobs").get("jobs", [])
    job = next((j for j in jobs if j.get("reportTypeId") == REACH), None)
    if not job:
        job = _call(tok, YR + "jobs", method="POST", body={"reportTypeId": REACH, "name": "ytflow reach"})
        return {"ok": True, "note": f"노출 보고서 작업을 새로 만듦({job.get('id')}) — 보고서는 하루쯤 뒤부터", "videos": {}}
    rd = d / "reach"
    rd.mkdir(exist_ok=True)
    for rep in _call(tok, YR + f"jobs/{job['id']}/reports").get("reports", []):
        f = rd / f"{rep['startTime'][:10]}_{rep['id']}.csv"
        if not f.exists():
            f.write_bytes(_call(tok, rep["downloadUrl"], raw=True))
    agg: dict = {}
    for f in sorted(rd.glob("*.csv")):
        rows = list(csv.DictReader(f.read_text(encoding="utf-8").splitlines()))
        for row in rows:
            vid = row.get("video_id")
            imp = next((row[k] for k in row if k.endswith("impressions") and "ctr" not in k), None)
            ctr = next((row[k] for k in row if k.endswith("impressions_ctr")), None)
            if not vid or imp in (None, ""):
                continue
            a = agg.setdefault(vid, {"impressions": 0.0, "clicks": 0.0})
            a["impressions"] += float(imp)
            a["clicks"] += float(imp) * float(ctr or 0)
    for a in agg.values():
        a["ctr"] = a["clicks"] / a["impressions"] if a["impressions"] else None
    note = "" if agg else "노출 보고서가 아직 없음 (작업을 만든 뒤 하루쯤 걸림)"
    return {"ok": True, "videos": agg, "note": note}


# ---------------------------------------------------------------- 분석

def views_at(snap: list, vid: str, when: dt.datetime) -> int | None:
    """스냅숏에서 그 시각 즈음(±6시간)의 조회 수."""
    best = None
    for at, v in snap:
        if abs((at - when).total_seconds()) <= 6 * 3600 and (best is None or abs((at - when)) < abs(best[0] - when)):
            best = (at, v)
    return best[1] if best else None


def load_snaps(d: Path) -> dict:
    out: dict = {}
    f = d / "snapshots.csv"
    if f.exists():
        for row in csv.DictReader(f.read_text(encoding="utf-8").splitlines()):
            out.setdefault(row["video_id"], []).append((dt.datetime.fromisoformat(row["at"]), int(row["views"] or 0)))
    return out


def caption_at(tok: str, vid: str, sec: float, cache: dict) -> str:
    """올린 자막에서 그 시각의 말 (장면 찾기). 자막이 없으면 빈 문자열."""
    if vid not in cache:
        cache[vid] = []
        try:
            cl = _call(tok, YT + "captions", {"part": "snippet", "videoId": vid}).get("items", [])
            if cl:
                srt = _call(tok, YT + f"captions/{cl[0]['id']}", {"tfmt": "srt"}, raw=True).decode("utf-8", "replace")
                for blk in srt.split("\n\n"):
                    m = re.search(r"(\d+):(\d+):(\d+),(\d+) --> (\d+):(\d+):(\d+),(\d+)\s*\n(.+)", blk, re.S)
                    if m:
                        g = [int(x) for x in m.groups()[:8]]
                        a = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000
                        b = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
                        cache[vid].append((a, b, " ".join(m.group(9).split())))
        except (NoScope, RuntimeError):
            pass
    for a, b, t in cache[vid]:
        if a - 1 <= sec <= b + 1:
            return t
    return ""


def retention_points(rows: list, dur: int) -> dict:
    """곡선 요약: 30초 시점 남은 비율, 가장 크게 빠진 구간(초반 5% 뒤), 끝까지 남은 비율."""
    if not rows or not dur:
        return {}
    pts = [(float(r[0]), float(r[1]), float(r[2]) if len(r) > 2 and r[2] is not None else None) for r in rows]
    at30 = min(pts, key=lambda p: abs(p[0] - 30 / dur))
    drop, where = 0.0, None
    for (x0, y0, _), (x1, y1, _) in zip(pts, pts[1:]):
        if x0 >= 0.05 and y0 - y1 > drop:
            drop, where = y0 - y1, x1
    rel = [p[2] for p in pts if p[2] is not None]
    return {"at30": at30[1], "end": pts[-1][1], "drop": drop, "drop_sec": (where or 0) * dur,
            "relative": statistics.median(rel) if rel else None}


def report(name: str, ch: dict, got: dict | None = None) -> Path:
    c = cfg()
    d = DATA / name
    chan = json.loads((d / "channel.json").read_text(encoding="utf-8"))
    vids = json.loads((d / "videos.json").read_text(encoding="utf-8"))
    snaps = load_snaps(d)
    an = (got or {}).get("analytics") or {}
    reach = (got or {}).get("reach") or {}
    avids = an.get("videos", {}) if an.get("ok") else {}
    if not avids and (d / "videos").exists():  # 지난 수집분
        avids = {f.stem: json.loads(f.read_text(encoding="utf-8")) for f in (d / "videos").glob("*.json")}
    t = now()
    pub = sorted([v for v in vids if v["privacy"] == "public"], key=lambda v: v["published"], reverse=True)
    for v in pub:
        v["age_h"] = (t - _ts(v["published"])).total_seconds() / 3600
        ss = snaps.get(v["id"], [])
        v["cp"] = {h: views_at(ss, v["id"], _ts(v["published"]) + dt.timedelta(hours=h)) for h in c["checkpoints_h"]}
        v["d24"] = (v["views"] - views_at(ss, v["id"], t - dt.timedelta(hours=24))) if views_at(ss, v["id"], t - dt.timedelta(hours=24)) is not None else None
    lines = [f"# {chan['title']} 운영 보고 — {t:%Y-%m-%d %H:%M}",
             "",
             f"구독 {chan['subscribers']} · 총 조회 {chan['views']:,} · 영상 {chan['videos']} (공개 {len(pub)}) · `python -m ytflow ops {name}`",
             "",
             "## 1. 공개 영상",
             "'중앙값 대비' = 같은 채널 공개 영상과 같은 나이에서 견준 조회 비. (24h·48h·168h) = 올린 지 그 시간 때 조회끼리, "
             "(대략) = 스냅숏이 쌓이기 전이라 이 영상보다 오래된 영상의 지금 조회와 견줌, '이른' = 48시간 전이라 판정 보류. 표시일 뿐 합격선이 아님.",
             "",
             "| 공개 | 나이 | 조회 | 시간당 | 24시간 증가 | 좋아요 | 댓글 | 중앙값 대비 | 평균 시청 | 30초 남음 | 노출 클릭률 | 주 유입 | 제목 |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    flagged = []
    tok = None
    cap: dict = {}
    for v in pub:
        # 같은 나이끼리: 스냅숏이 쌓였으면 '올린 지 h시간 때 조회'를 서로 견주고, 아직이면 48시간 넘은 영상만 대략 견줌
        ratio, basis = None, ""
        for h in sorted(c["checkpoints_h"], reverse=True):
            mine = v["cp"].get(h)
            others = [w["cp"].get(h) for w in pub if w is not v and w["cp"].get(h) is not None]
            if mine is not None and len(others) >= 3:
                med = statistics.median(others)
                ratio, basis = (mine / med if med else None), f"{h}h"
                break
        if ratio is None and v["age_h"] >= 48:
            older = [w["views"] for w in pub if w["age_h"] >= v["age_h"] and w is not v]
            med = statistics.median(older) if older else None
            ratio, basis = (v["views"] / med if med else None), "대략"
        v["basis"] = basis
        mark = ""
        if ratio is not None and ratio >= c["outlier_ratio"]:
            mark = "▲"
            flagged.append(("앞섬", v, ratio))
        elif ratio is not None and ratio <= c["laggard_ratio"] and v["age_h"] >= 48:
            mark = "▼"
            flagged.append(("처짐", v, ratio))
        d24 = "" if v["d24"] is None else f"+{v['d24']:,}"
        rtxt = ("이른" if v["age_h"] < 48 else "") if ratio is None else f"{ratio:.1f}× ({basis})"
        a = avids.get(v["id"], {})
        rp = retention_points(a.get("retention") or [], v["duration"])
        v["rp"] = rp
        avg = f"{a['averageViewPercentage']:.0f}% ({int(a['averageViewDuration'])//60}:{int(a['averageViewDuration'])%60:02d})" if a.get("averageViewPercentage") is not None else "—"
        r30 = f"{rp['at30']*100:.0f}%" if rp.get("at30") is not None else "—"
        rc = (reach.get("videos") or {}).get(v["id"]) if reach.get("ok") else None
        ctr = f"{rc['ctr']*100:.1f}% / {int(rc['impressions']):,}" if rc and rc.get("ctr") is not None else "—"
        tr = a.get("traffic") or {}
        top = ", ".join(TRAFFIC_KO.get(k, k) for k, _ in sorted(tr.items(), key=lambda kv: -kv[1])[:2]) or "—"
        lines.append(f"| {_ts(v['published']):%m-%d %H:%M} | {v['age_h']/24:.1f}일 | {v['views']:,} | {v['views']/max(v['age_h'],1):.1f} | "
                     f"{d24} | {v['likes']} | {v['comments']} | "
                     f"{rtxt} {mark} | {avg} | {r30} | {ctr} | {top} | "
                     f"[{v['title'][:40]}](https://youtu.be/{v['id']}) |")
    lines += ["", "## 2. 눈에 띄는 영상"]
    if not flagged:
        lines.append("- 없음 (모두 같은 채널 중앙값의 0.5~2배 안)")
    for kind, v, ratio in flagged:
        lines.append(f"- **{kind} {ratio:.1f}×** [{v['title']}](https://youtu.be/{v['id']}) — 프로젝트 `{v.get('project') or '연결 없음'}`")
    lines += ["", "## 3. 어디서 빠졌나 (시청 지속)"]
    if not avids:
        lines.append(f"- {an.get('why') or '분석 수치 없음'}")
    else:
        for v in pub[:8]:
            rp = v.get("rp") or {}
            if not rp.get("drop_sec"):
                continue
            if tok is None:
                tok = yp._token(ch.get("credentials") or None)
            sec = rp["drop_sec"]
            said = caption_at(tok, v["id"], sec, cap)
            rel = f" · 비슷한 길이 영상 대비 {rp['relative']:.2f}" if rp.get("relative") is not None else ""
            lines.append(f"- [{v['title'][:40]}](https://youtu.be/{v['id']}?t={int(sec)}) — {int(sec)//60}:{int(sec)%60:02d} 에서 "
                         f"{rp['drop']*100:.0f}%p 빠짐, 끝까지 {rp['end']*100:.0f}%{rel}" + (f" — 그때 말: “{said[:60]}”" if said else ""))
    lines += ["", "## 4. 노출·클릭"]
    lines.append(f"- {reach.get('note') or reach.get('why') or ('영상별 노출 클릭률은 표에' if reach.get('ok') else '없음')}")
    lines += ["", "## 4-1. 진행 바 챕터"]
    bad = [v for v in pub if v.get("chapter_problems")]
    hidden = [v for v in pub if not v.get("chapter_problems") and v.get("chapters_shown") is False]
    shown = [v for v in pub if v.get("chapters_shown")]
    for v in bad:
        lines.append(f"- 설명란 타임코드 문제: [{v['title'][:40]}](https://studio.youtube.com/video/{v['id']}/edit) — {'; '.join(v['chapter_problems'])}")
    if hidden and not shown:
        lines.append(f"- 설명란은 맞는데 공개 영상 {len(hidden)}편 모두 진행 바에 챕터가 안 붙음 → **채널 '고급 기능'이 꺼져 있을 가능성이 큼.** "
                     "사용자: YouTube Studio → 설정 → 채널 → 기능 사용 자격 → 고급 기능(전화 인증 등). 켜진 뒤 "
                     f"`python -m ytflow ops-act {name} resave` 로 설명란을 다시 저장해 반영을 재촉.")
    elif hidden:
        for v in hidden:
            lines.append(f"- 설명란은 맞는데 챕터가 아직 안 붙음 (반영 지연일 수 있음, 24~72시간): [{v['title'][:40]}](https://youtu.be/{v['id']})")
    if not bad and not hidden:
        known = [v for v in pub if v.get("chapters_shown") is not None]
        lines.append(f"- 이상 없음 (확인 {len(known)}편)" if known else "- 확인 못 함 (시청 페이지를 못 읽음)")
    new = ((got or {}).get("comments") or {}).get("new") or []
    lines += ["", f"## 5. 새 댓글 {len(new)}개"]
    titles = {v["id"]: v["title"] for v in vids}
    for cm in new[:30]:
        q = " ❓" if "?" in cm["text"] or "까요" in cm["text"] or "나요" in cm["text"] else ""
        lines.append(f"- ({titles.get(cm['video_id'], cm['video_id'])[:24]}) {cm['text'][:140]}{q} · 좋아요 {cm['likes']}")
    if not new:
        lines.append("- 없음")
    lines += ["", "## 6. 정리할 것 (제안 — 이 명령은 바꾸지 않음)"]
    by_title: dict = {}
    for v in vids:
        by_title.setdefault(re.sub(r"\s+", " ", v["title"]).strip(), []).append(v)
    tidy = 0
    for ttl, vs in by_title.items():
        if len(vs) > 1 and any(v["privacy"] == "public" for v in vs):
            for v in vs:
                if v["privacy"] != "public":
                    tidy += 1
                    lines.append(f"- 공개본이 따로 있는 {v['privacy']} 사본: [{ttl[:40]}](https://studio.youtube.com/video/{v['id']}/edit)")
    for v in vids:
        same = by_title.get(re.sub(r"\s+", " ", v["title"]).strip(), [])
        if v["privacy"] != "public" and not v.get("publish_at") and not any(w["privacy"] == "public" for w in same):
            tidy += 1
            proj = f" · 프로젝트 `{v['project']}`" if v.get("project") else ""
            lines.append(f"- 공개되지 않은 {v['privacy']} (예약 없음, 공개본 없음): "
                         f"[{v['title'][:40]}](https://studio.youtube.com/video/{v['id']}/edit){proj}")
        if v["privacy"] == "private" and v.get("publish_at"):
            lines.append(f"- 예약 공개 대기: {_ts(v['publish_at']):%m-%d %H:%M} [{v['title'][:40]}](https://youtu.be/{v['id']})")
    nolink = [v for v in pub if not v.get("project")]
    for v in nolink:
        lines.append(f"- 프로젝트와 연결 안 됨 (youtube_publish.json 없음): [{v['title'][:40]}](https://youtu.be/{v['id']})")
    if not tidy and not nolink:
        lines.append("- 없음")
    lines += ["", "## 7. 해석과 다음 실험 (운영 에이전트가 채움)",
              "- 앞선 영상과 처진 영상의 차이를 **주제·제목·썸네일·훅(첫 30초)·결말·화면** 중 하나로 짚고, 근거(표의 수치·빠진 지점의 말)를 붙인다.",
              "- 다음 편에서 **하나만** 바꿔 볼 것 (가설 → 바꿀 것 → 무엇으로 확인) — `data/analytics/experiments.md` 에 기록.",
              "- 매뉴얼로 옮기지 않는다: 한두 편의 반응은 '실험 기록' 층(manual README §3-1). 같은 결과가 여러 편 쌓이면 `manual-propose`."]
    out = config.ROOT / "channels" / ch["dir"] / "ops" / f"{t:%Y%m%d}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def run(names: list[str] | None = None, do_fetch: bool = True, do_report: bool = True) -> list[Path]:
    c = cfg()
    outs = []
    for name, ch in c["channels"].items():
        if names and name not in names:
            continue
        got = None
        if do_fetch:
            got = fetch(name, ch)
            a = got.get("analytics") or {}
            print(f"[ops] {name}: 영상 {len(got['videos'])} · 새 댓글 {len(got['comments'].get('new', []))} · "
                  f"분석 {'있음' if a.get('ok') else '없음 — ' + str(a.get('why'))[:80]}")
        if do_report:
            p = report(name, ch, got)
            print(f"[ops] 보고서 → {p.relative_to(config.ROOT)}")
            outs.append(p)
    return outs


# ---------------------------------------------------------------- 운영 행동 (manual/11 §8 의 허용 목록만)
# 2026-11-23 사용자 허용: 제목·썸네일 교체 · 재생목록 · 사본 정리. 공개(D4)·댓글 답글은 허용 아님 — 이 명령에 없음.
# 고정 댓글은 YouTube API 가 '고정'을 지원하지 않아 보고서 제안으로만.

ACTIONS = DATA / "actions.jsonl"


def _log(rec: dict) -> None:
    ACTIONS.parent.mkdir(parents=True, exist_ok=True)
    rec = {"at": now().isoformat(timespec="minutes"), **rec}
    with open(ACTIONS, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def duplicates(vids: list) -> list:
    """공개본과 제목이 같은 비공개·일부공개 사본 (예약 공개 대기는 빼고)."""
    public = {_norm(v["title"]): v for v in vids if v["privacy"] == "public"}
    return [(v, public[_norm(v["title"])]) for v in vids
            if v["privacy"] != "public" and not v.get("publish_at") and _norm(v["title"]) in public]


def title_candidates(project: str) -> list:
    f = config.ROOT / "projects" / project / "05_edit" / "youtube.md"
    if not project or not f.exists():
        return []
    m = re.search(r"## 제목[^\n]*\n((?:\d+\.\s.*\n?)+)", f.read_text(encoding="utf-8"))
    return [re.sub(r"^\d+\.\s*", "", ln).strip() for ln in (m.group(1).splitlines() if m else []) if ln.strip()]


def thumb_file(project: str, letter: str):
    import os
    name = f"thumbnail_{letter.upper()}.png"
    roots = [config.ROOT / "projects" / project / "05_edit"]
    local = Path("E:/ytflow-local")
    if local.exists():
        roots += [p / "projects" / project / "05_edit" for p in local.glob("*") if p.is_dir()]
    if os.environ.get("YTFLOW_DRIVE"):
        roots.append(Path(os.environ["YTFLOW_DRIVE"]) / "영상" / project / "05_edit")
    return next((r / name for r in roots if project and (r / name).exists()), None)


def _act_tidy(name: str, vids: list, tok, dry_run: bool) -> None:
    dup = duplicates(vids)
    if not dup:
        print("[ops-act] 지울 사본 없음")
    for v, twin in dup:
        print(f"[ops-act] {'(시험) ' if dry_run else ''}사본 삭제: {v['id']} {v['privacy']} {v['duration']}s "
              f"'{v['title'][:40]}' — 공개본 {twin['id']} {twin['duration']}s")
        if not dry_run:
            _call(tok, YT + "videos", {"id": v["id"]}, method="DELETE")
            _log({"action": "delete_copy", "channel": name, "video": v["id"], "title": v["title"], "privacy": v["privacy"],
                  "duration": v["duration"], "views": v["views"], "public_twin": twin["id"]})


def _act_playlists(name: str, ch: dict, vids: list, tok, dry_run: bool) -> None:
    from ..project import Project
    s = yaml.safe_load((config.ROOT / "channels" / ch["dir"] / "channel.yaml").read_text(encoding="utf-8")).get("youtube", {})
    pls = s.get("playlists") or {}
    if not pls:
        print("[ops-act] 이 채널은 재생목록 설정이 없음 (channel.yaml youtube.playlists)")
        return
    have: set = set()
    if tok:
        for p in _call(tok, YT + "playlists", {"part": "snippet", "mine": "true", "maxResults": 50}).get("items", []):
            for it in _call(tok, YT + "playlistItems", {"part": "contentDetails", "playlistId": p["id"], "maxResults": 50}).get("items", []):
                have.add(it["contentDetails"]["videoId"])
    for v in vids:
        if v["privacy"] != "public" or not v.get("project") or v["id"] in have:
            continue
        title = pls.get(yp.kind_of(Project(config.ROOT / "projects" / v["project"])))
        if title:
            print(f"[ops-act] {'(시험) ' if dry_run else ''}재생목록 '{title}' ← {v['title'][:40]}")
            if not dry_run:
                yp.playlist(tok, v["id"], title)
                _log({"action": "playlist_add", "channel": name, "video": v["id"], "playlist": title})


def act(name: str, what: str, video=None, to=None, dry_run: bool = False, force: bool = False) -> None:
    ch = cfg()["channels"][name]
    vids = json.loads((DATA / name / "videos.json").read_text(encoding="utf-8"))
    byid = {v["id"]: v for v in vids}
    tok = yp._token(ch.get("credentials") or None)
    if what == "tidy":
        return _act_tidy(name, vids, tok, dry_run)
    if what == "playlists":
        return _act_playlists(name, ch, vids, tok, dry_run)
    if what == "resave":   # 설명란을 그대로 다시 저장 → 챕터 재처리 재촉 (내용은 바꾸지 않음)
        targets = [x for x in vids if x["privacy"] == "public" and (not video or x["id"] == video)
                   and not x.get("chapter_problems") and x.get("chapters_shown") is not True]
        for x in targets:
            print(f"[ops-act] {'(시험) ' if dry_run else ''}설명란 다시 저장: {x['title'][:40]}")
            if not dry_run:
                sn = _call(tok, YT + "videos", {"part": "snippet", "id": x["id"]})["items"][0]["snippet"]
                body = {"id": x["id"], "snippet": {k: sn[k] for k in ("title", "categoryId", "description", "tags", "defaultLanguage") if k in sn}}
                _call(tok, YT + "videos?part=snippet", method="PUT", body=body)
                _log({"action": "resave_description", "channel": name, "video": x["id"]})
        if not targets:
            print("[ops-act] 다시 저장할 영상 없음")
        return
    v = byid.get(video or "")
    if not v:
        raise SystemExit(f"[ops-act] {name} 에 영상 {video} 이 없음 (먼저 python -m ytflow ops {name})")
    age = (now() - _ts(v["published"])).total_seconds() / 3600
    if v["privacy"] != "public" or (age < 48 and not force):
        raise SystemExit("[ops-act] 공개 뒤 48시간이 지난 공개 영상만 바꿈 (그 전에는 판단 근거가 모자람) — 꼭 필요하면 --force")
    prev = [json.loads(ln) for ln in ACTIONS.read_text(encoding="utf-8").splitlines() if ln.strip()] if ACTIONS.exists() else []
    if what in ("retitle", "rethumb") and not force and \
            any(p.get("video") == v["id"] and p["action"] in ("retitle", "rethumb") for p in prev):
        raise SystemExit("[ops-act] 이 영상은 이미 한 번 바꿈 — 한 영상에 한 번만 (결과를 본 뒤 revert, 또는 --force)")
    if what == "retitle":
        cands = title_candidates(v.get("project") or "")
        new = cands[int(to) - 1] if to and to.isdigit() and int(to) <= len(cands) else to
        if not new:
            raise SystemExit(f"[ops-act] 새 제목이 없음 — youtube.md 후보: {cands}")
        print(f"[ops-act] {'(시험) ' if dry_run else ''}제목: '{v['title']}' → '{new}'")
        if not dry_run:
            sn = _call(tok, YT + "videos", {"part": "snippet", "id": v["id"]})["items"][0]["snippet"]
            body = {"id": v["id"], "snippet": {"title": new[:100], "categoryId": sn["categoryId"],
                                                "description": sn.get("description", ""), "tags": sn.get("tags", []),
                                                "defaultLanguage": sn.get("defaultLanguage", "ko")}}
            _call(tok, YT + "videos?part=snippet", method="PUT", body=body)
            _log({"action": "retitle", "channel": name, "video": v["id"], "before": v["title"], "after": new,
                  "views_before": v["views"]})
    elif what == "rethumb":
        f = thumb_file(v.get("project") or "", to or "B")
        if not f:
            raise SystemExit(f"[ops-act] thumbnail_{(to or 'B').upper()}.png 을 찾지 못함 (프로젝트 05_edit · E:/ytflow-local/* · Drive 영상/)")
        print(f"[ops-act] {'(시험) ' if dry_run else ''}썸네일 → {f}")
        if not dry_run:
            yp.thumbnail(tok, v["id"], f)
            _log({"action": "rethumb", "channel": name, "video": v["id"], "after": (to or "B").upper(), "views_before": v["views"]})
    elif what == "revert":
        last = next((p for p in reversed(prev) if p.get("video") == v["id"] and p["action"] in ("retitle", "rethumb")), None)
        if not last:
            raise SystemExit("[ops-act] 되돌릴 기록 없음")
        act(name, last["action"], v["id"], last["before"] if last["action"] == "retitle" else "A", dry_run, force=True)
    else:
        raise SystemExit(f"[ops-act] 모르는 행동: {what}")
