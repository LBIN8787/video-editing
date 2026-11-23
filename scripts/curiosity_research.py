"""호기심·이야기 채널 시청자 조사 (docs/29-curiosity-audience.md) — '상권 조사처럼' 시청자를 먼저 안다 (2026-11-14 사용자 기각 반영).
    python scripts/curiosity_research.py      → .cache/curiosity/channels.json · top.json (+ 댓글)
공개 정보만: yt-dlp flat-playlist(제목·조회수·길이·구독자), 상위 영상의 좋아요·댓글 수·다시 본 구간·댓글 상위 100개. 영상 파일은 받지 않음 (봇 확인 우회 금지).
"""
import concurrent.futures as cf
import json
import statistics as st
import subprocess
from pathlib import Path

CH = {"미주일기": "UCLp74JDqjSoKu8Puc44sABw", "사물궁이 잡학지식": "UC7F6UDq3gykPZHWRhrj_BDw", "1분과학": "UCFOixeB9gbedVi6uwnsfHMQ",
      "과학드림": "UCIk1-yPCTnFuzfgu4gyfWqw", "지식해적단": "UC9cCBxBAQW2CzLYeT20q49A", "보다 BODA": "UCoCvTlU0KpNYwnMIgs7MPrA",
      "닥터프렌즈": "UCVfLNEch9YxD4tX1L-crkMQ", "지식한입": "UCi9Sl8GnFdYoqEVXnojBPJw"}
OUT = Path(".cache/curiosity")


def ytj(args, timeout=240):
    r = subprocess.run(["yt-dlp", "--no-warnings", "--ignore-errors", "--js-runtimes", "node", "-J", *args], capture_output=True, text=True, timeout=timeout)
    try:
        return json.loads(r.stdout) or {}
    except Exception:  # noqa: BLE001
        return {}


def channel(cid):
    j = ytj(["--flat-playlist", "--playlist-end", "80", f"https://www.youtube.com/channel/{cid}/videos"])
    vids = [{"id": e["id"], "title": e.get("title"), "views": e.get("view_count") or 0, "dur": e.get("duration") or 0} for e in j.get("entries") or []]
    med = st.median([v["views"] for v in vids if v["views"]] or [0])
    for v in vids:
        v["x"] = round(v["views"] / med, 2) if med else 0
    return {"subs": j.get("channel_follower_count"), "median": med, "videos": vids}


def detail(vid):
    j = ytj(["--skip-download", "--write-comments", "--extractor-args", "youtube:max_comments=120,all,0,0;comment_sort=top", f"https://www.youtube.com/watch?v={vid}"], 400)
    hm = j.get("heatmap") or []
    top = sorted(hm, key=lambda h: -h.get("value", 0))[:3]
    d = j.get("duration") or 1
    return {"id": vid, "title": j.get("title"), "views": j.get("view_count"), "likes": j.get("like_count"), "ncom": j.get("comment_count"),
            "dur": d, "replay": [round(h["start_time"] / d * 100) for h in top], "desc": (j.get("description") or "")[:400],
            "comments": [{"t": c.get("text"), "likes": c.get("like_count")} for c in (j.get("comments") or [])[:120]]}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    with cf.ThreadPoolExecutor(4) as ex:
        data = dict(zip(CH, ex.map(channel, CH.values())))
    (OUT / "channels.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    picks = []
    for name, c in data.items():
        for v in sorted(c["videos"], key=lambda v: -v["x"])[:2]:
            picks.append((name, v["id"]))
    with cf.ThreadPoolExecutor(4) as ex:
        tops = list(ex.map(lambda p: {"ch": p[0], **detail(p[1])}, picks))
    (OUT / "top.json").write_text(json.dumps(tops, ensure_ascii=False, indent=1), encoding="utf-8")
    for name, c in data.items():
        durs = [v["dur"] for v in c["videos"] if v["dur"]]
        print(f"{name}: 구독 {c['subs']} · 중앙값 {c['median']:.0f} · 길이 {st.median(durs) / 60 if durs else 0:.1f}분")


if __name__ == "__main__":
    main()
