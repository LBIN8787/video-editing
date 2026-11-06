"""4.3단계: 소스 찾기 — 대본의 검색어(source.query)로 쓸 원본 영상을 골라 URL·구간을 채운다.

고르는 기준 (config/pipeline.yaml → sources):
  - prefer_channels 에 든 공식·주요 언론 채널을 우선
  - 30초 미만(쇼츠)·3시간 초과 영상 제외
  - 같은 영상을 여러 장면에 쓰면 구간을 겹치지 않게 뒤로 민다
결과: scenes.json 의 source.url/start/end/label 갱신 + 04_assets/sources.csv (어떤 영상을 왜 골랐는지)
"""
from __future__ import annotations

import csv
import re
import urllib.parse

from .. import config, yt
from ..project import Project
from .clips import is_youtube


def _fmt(sec: float) -> str:
    return f"{int(sec // 60)}:{sec % 60:04.1f}"


def search(query: str, n: int = 12) -> list[dict]:
    url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
    data = yt.flat_playlist(url, n) or {}
    out = []
    for e in data.get("entries") or []:
        if e and e.get("id") and e.get("duration") and 30 <= e["duration"] <= 3 * 3600:
            out.append({"id": e["id"], "title": e.get("title", ""), "channel": e.get("channel") or e.get("uploader") or "",
                        "duration": e["duration"], "views": e.get("view_count") or 0})
    return out


def _tokens(t: str) -> set[str]:
    import re
    return {w for w in re.findall(r"[0-9A-Za-z가-힣]+", t.lower()) if len(w) >= 2}


def relevance(query: str, title: str) -> float:
    """검색어 단어 중 제목에 들어 있는 비율 (한글은 앞 2글자만 맞아도 인정: '슈퍼컴퓨터'↔'슈퍼컴')."""
    q, t = _tokens(query), title.lower()
    if not q:
        return 0.0
    hit = sum(1 for w in q if w in t or (re.match(r"[가-힣]", w) and w[:2] in t))
    return hit / len(q)


def score(c: dict, prefer: list[str], used: dict, query: str = "") -> float:
    rel = relevance(query, c["title"]) if query else 1.0
    s = rel * 100                                   # 1순위: 제목이 검색어와 맞는가
    if rel >= 0.3 and any(p.lower() in c["channel"].lower() for p in prefer):
        s += 30                                     # 관련 있을 때만 공식·주요 언론 가산점
    s += min(c["views"], 2_000_000) / 200_000       # 조회수는 약하게만 반영
    s -= used.get(c["id"], 0) * 8                   # 같은 영상 반복 사용 억제
    if c["duration"] > 1800:
        s += 3                                      # 긴 원본(키노트·인터뷰)은 쓸 구간이 많다
    return s


MIN_RELEVANCE = 0.3


def run(project: Project) -> None:
    cfg = config.load("pipeline").get("sources", {})
    prefer = cfg.get("prefer_channels", [])
    data = project.read_json("script", "scenes.json")
    cache: dict = {}
    used: dict = {}
    cursor: dict = {}   # 영상별 다음 시작 위치
    rows = []
    for s in data["scenes"]:
        src = s.get("source") or {}
        if src.get("url") and is_youtube(src["url"]):
            used[yt_id(src["url"])] = used.get(yt_id(src["url"]), 0) + 1
            continue
        q = (src.get("query") or "").strip()
        if not q or src.get("url"):
            continue
        if q not in cache:
            cache[q] = search(q)
        cands = [c for c in cache[q] if relevance(q, c["title"]) >= MIN_RELEVANCE]
        cands = sorted(cands, key=lambda c: score(c, prefer, used, q), reverse=True)
        if not cands:  # 관련 영상이 없으면 억지로 붙이지 않고 카드/자리표시로 남긴다
            rows.append([s["id"], q, "NOT FOUND", "", "", "", ""])
            print(f"[sources] #{s['id']} '{q}' → 결과 없음")
            continue
        c = cands[0]
        length = float(src.get("length") or 8)
        start = cursor.get(c["id"], min(c["duration"] * 0.15, 60.0))  # 도입부 로고·인사는 건너뜀
        if start + length > c["duration"] - 2:
            start = max(0.0, c["duration"] * 0.3)
        cursor[c["id"]] = start + length + 3
        used[c["id"]] = used.get(c["id"], 0) + 1
        src.update({"url": f"https://www.youtube.com/watch?v={c['id']}", "start": _fmt(start), "end": _fmt(start + length)})
        s["source"] = src
        if not s.get("label"):
            s["label"] = c["channel"]
        elif c["channel"] and c["channel"] not in s["label"]:
            s["label"] = f"{s['label'].split('·')[0].strip()} · {c['channel']}"
        rows.append([s["id"], q, c["channel"], c["title"][:70], src["url"], src["start"], src["end"]])
        print(f"[sources] #{s['id']} '{q}' → {c['channel']} | {c['title'][:40]} ({src['start']}~{src['end']})")
    project.write_json("script", "scenes.json", data)
    from .writing import write_script_md
    write_script_md(project, data)
    with open(project.dir("assets") / "sources.csv", "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(["scene", "query", "channel", "title", "url", "start", "end"])
        w.writerows(rows)
    print(f"[sources] {len(rows)}개 장면에 영상 지정 → {project.dir('assets')}/sources.csv (바꾸려면 scenes.json 의 source.url 수정)")
    project.mark_done("sources")


def yt_id(url: str) -> str:
    from .clips import _vid
    return _vid(url)
