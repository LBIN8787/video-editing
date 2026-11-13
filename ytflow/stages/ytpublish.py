"""유튜브 올리기·관리 (공식 YouTube Data API v3, docs/24-youtube-publish.md).

05_edit/youtube.md(yt-pack)의 제목·설명란·태그 + channel.yaml 의 youtube 설정으로
  업로드(예약 공개) → 썸네일 → 자막(한국어) → 재생목록 → 결과 기록(05_edit/youtube_publish.json)
까지 한 번에 한다. 표준 라이브러리 + Pillow 만 쓴다 (GitHub Actions 에서도 그대로 돈다).

인증 (키를 채팅에 쓰지 않음): 환경변수 YT_CLIENT_ID · YT_CLIENT_SECRET · YT_REFRESH_TOKEN
  - 한 번만: 사용자 PC 에서 python scripts/youtube_auth.py client_secret.json --to-github
    (이미 로그인된 브라우저에서 '허용' → 토큰이 GitHub 저장소 비밀값으로 바로 들어감)
  - 실제 올리기는 GitHub Actions(.github/workflows/youtube-publish.yml)가 한다:
    클라우드·PC 어디서든 python -m ytflow yt-publish <프로젝트> --via github

API 로 못 하는 것 (Studio 에서 직접): 썸네일 '테스트 및 비교'(A/B/C), 댓글 고정, 수익 창출 설정, 최종 화면·카드.
"""
from __future__ import annotations

import datetime as dt
import io
import json
import os
import re
import urllib.parse
import urllib.request
from pathlib import Path

from .. import config
from ..project import Project

API = "https://www.googleapis.com/youtube/v3"
UP = "https://www.googleapis.com/upload/youtube/v3"
KST = dt.timezone(dt.timedelta(hours=9))
DEFAULTS = {
    "category_id": "25",            # 25 뉴스/정치 (시장 브리핑), 27 교육, 22 인물/블로그
    "default_language": "ko",
    "made_for_kids": False,
    "license": "youtube",
    "embeddable": True,
    "public_stats": True,
    "notify_subscribers": True,
    "publish_time": "08:00",        # 한국 시간. 이미 지났으면 바로 공개
    "privacy": "public",            # 예약 시간이 지났을 때의 공개 상태 (public | unlisted | private)
    "playlists": {},                 # 종류 → 재생목록 이름 (없으면 만든다)
    "captions": True,
    "synthetic_media": False,       # '변경되거나 합성된 콘텐츠' — 실제처럼 보이는 합성이 있으면 true
}


# ---------------------------------------------------------------- 설정·문구
def settings(pr: Project) -> dict:
    import yaml
    s = dict(DEFAULTS)
    try:
        ed = yaml.safe_load((pr.path / "edit.yaml").read_text(encoding="utf-8")) or {}
        cy = config.ROOT / "channels" / str(ed.get("channel")) / "channel.yaml"
        if cy.exists():
            s.update((yaml.safe_load(cy.read_text(encoding="utf-8")) or {}).get("youtube") or {})
    except Exception:  # noqa: BLE001
        pass
    return s


def pack(pr: Project) -> dict:
    """05_edit/youtube.md → 제목(1번)·설명란·태그."""
    md = (pr.dir("edit") / "youtube.md").read_text(encoding="utf-8")
    title = re.search(r"## 제목[^\n]*\n1\. (.+)", md).group(1).strip()
    desc = re.search(r"## 설명란[^\n]*\n```\n(.*?)\n```", md, re.S).group(1).strip()
    tm = re.search(r"## 태그\n(.+)", md)
    tags = [t.strip() for t in tm.group(1).split(",")] if tm else []
    return {"title": title[:100], "description": desc[:5000], "tags": tags}


def kind_of(pr: Project) -> str:
    n = pr.path.name
    return "weekly" if n.endswith("-weekly") else "analysis" if n.endswith("-analysis") else \
        "deep" if "deep" in n or "call" in n else "briefing"


def publish_at(s: dict, at: str | None, now: dt.datetime | None = None) -> str | None:
    """예약 시각(UTC ISO) — at 이 있으면 그것, 없으면 오늘 publish_time(KST). 이미 지났으면 None(바로 공개)."""
    now = now or dt.datetime.now(dt.timezone.utc)
    if at:
        t = dt.datetime.fromisoformat(at)
        t = t if t.tzinfo else t.replace(tzinfo=KST)
    else:
        h, m = map(int, str(s.get("publish_time", "08:00")).split(":"))
        t = now.astimezone(KST).replace(hour=h, minute=m, second=0, microsecond=0)
    if t <= now + dt.timedelta(minutes=5):
        return None
    return t.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")


def ass_to_srt(ass: Path) -> str:
    def t(x):
        h, m, s = x.split(":")
        sec = int(h) * 3600 + int(m) * 60 + float(s)
        return f"{int(sec // 3600):02d}:{int(sec % 3600 // 60):02d}:{int(sec % 60):02d},{int(round(sec % 1 * 1000)) % 1000:03d}"
    out, k = [], 0
    for ln in ass.read_text(encoding="utf-8").splitlines():
        if ln.startswith("Dialogue:"):
            f = ln.split(",", 9)
            k += 1
            out.append(f"{k}\n{t(f[1])} --> {t(f[2])}\n{re.sub(r'{[^}]*}', '', f[9]).replace(chr(92) + 'N', chr(10))}\n")
    return "\n".join(out)


# ---------------------------------------------------------------- API
def _token() -> str:
    miss = [k for k in ("YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN") if not os.environ.get(k)]
    if miss:
        raise SystemExit(f"[yt-publish] 인증 정보 없음: {', '.join(miss)} — docs/24-youtube-publish.md §1 (한 번만: scripts/youtube_auth.py)")
    body = urllib.parse.urlencode({"client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"],
                                   "refresh_token": os.environ["YT_REFRESH_TOKEN"], "grant_type": "refresh_token"}).encode()
    with urllib.request.urlopen(urllib.request.Request("https://oauth2.googleapis.com/token", data=body), timeout=60) as r:
        return json.loads(r.read())["access_token"]


def _req(tok, method, url, body=None, ctype="application/json", headers=None):
    h = {"Authorization": f"Bearer {tok}", **(headers or {})}
    if body is not None:
        h["Content-Type"] = ctype
        if isinstance(body, (dict, list)):
            body = json.dumps(body, ensure_ascii=False).encode()
    import time
    for k in range(4):   # 409 ABORTED·5xx 는 유튜브 쪽 일시 오류 → 잠시 뒤 다시 (2026-11-13 재생목록 409 발생)
        req = urllib.request.Request(url, data=body, method=method, headers=h)
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
                raw = r.read()
                return (json.loads(raw) if raw else {}), r.headers
        except urllib.error.HTTPError as e:
            msg = e.read()[:600].decode("utf-8", "replace")
            if e.code in (409, 500, 502, 503, 504) and k < 3 and "upload/youtube/v3/videos" not in url:
                time.sleep(3 * 2 ** k)
                continue
            raise SystemExit(f"[yt-publish] {method} {url.split('?')[0]} → {e.code}: {msg}")


def upload(tok, video: Path, meta: dict) -> str:
    url = f"{UP}/videos?uploadType=resumable&part=snippet,status"
    _, h = _req(tok, "POST", url, meta, headers={"X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(video.stat().st_size)})
    loc = h["Location"]
    data, _ = _req(tok, "PUT", loc, video.read_bytes(), ctype="video/mp4")
    return data["id"]


def thumbnail(tok, vid: str, png: Path) -> None:
    from PIL import Image
    im = Image.open(png).convert("RGB")
    q, buf = 92, io.BytesIO()
    while True:   # 유튜브 썸네일 한도 2MB
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=q)
        if buf.tell() < 2 * 1024 * 1024 or q <= 60:
            break
        q -= 8
    _req(tok, "POST", f"{UP}/thumbnails/set?videoId={vid}&uploadType=media", buf.getvalue(), ctype="image/jpeg")


def captions(tok, vid: str, srt: str, name: str = "한국어") -> None:
    b = "ytflowboundary"
    meta = json.dumps({"snippet": {"videoId": vid, "language": "ko", "name": name, "isDraft": False}}, ensure_ascii=False)
    body = (f"--{b}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n{meta}\r\n"
            f"--{b}\r\nContent-Type: application/octet-stream\r\n\r\n{srt}\r\n--{b}--").encode()
    _req(tok, "POST", f"{UP}/captions?part=snippet&uploadType=multipart", body, ctype=f"multipart/related; boundary={b}")


def playlist(tok, vid: str, title: str) -> str:
    data, _ = _req(tok, "GET", f"{API}/playlists?part=snippet&mine=true&maxResults=50")
    pid = next((p["id"] for p in data.get("items", []) if p["snippet"]["title"] == title), None)
    if not pid:
        made, _ = _req(tok, "POST", f"{API}/playlists?part=snippet,status",
                       {"snippet": {"title": title, "defaultLanguage": "ko"}, "status": {"privacyStatus": "public"}})
        pid = made["id"]
    _req(tok, "POST", f"{API}/playlistItems?part=snippet", {"snippet": {"playlistId": pid, "resourceId": {"kind": "youtube#video", "videoId": vid}}})
    return pid


# ---------------------------------------------------------------- 실행
def build_meta(pr: Project, at: str | None = None, privacy: str | None = None) -> tuple[dict, dict]:
    s, p = settings(pr), pack(pr)
    when = publish_at(s, at)
    status = {"privacyStatus": "private" if when else (privacy or s["privacy"]), "selfDeclaredMadeForKids": bool(s["made_for_kids"]),
              "license": s["license"], "embeddable": bool(s["embeddable"]), "publicStatsViewable": bool(s["public_stats"])}
    if s.get("synthetic_media"):   # '변경되거나 합성된 콘텐츠' 고지 (실제처럼 보이는 합성이 있을 때만)
        status["containsSyntheticMedia"] = True
    if when:
        status["publishAt"] = when
    meta = {"snippet": {"title": p["title"], "description": p["description"], "tags": p["tags"], "categoryId": str(s["category_id"]),
                        "defaultLanguage": s["default_language"], "defaultAudioLanguage": s["default_language"]},
            "status": status}
    return meta, s


def run(project: str, at: str | None = None, privacy: str | None = None, dry_run: bool = False, thumb: str = "A", resume: bool = False) -> dict:
    pr = Project.open(project)
    edir = pr.dir("edit")
    rec_p = edir / "youtube_publish.json"
    old = json.loads(rec_p.read_text(encoding="utf-8")) if rec_p.exists() else {}
    if old.get("video_id") and not dry_run:
        if not resume:
            raise SystemExit(f"[yt-publish] 이미 올림: {rec_p} (못 한 단계만 다시: --resume / 새로 올리려면 이 파일을 지우세요)")
        return _resume(pr, old, rec_p, thumb)
    meta, s = build_meta(pr, at, privacy)
    video = edir / "final.mp4"
    plan = {"title": meta["snippet"]["title"], "privacy": meta["status"]["privacyStatus"], "publishAt": meta["status"].get("publishAt"),
            "category": meta["snippet"]["categoryId"], "tags": len(meta["snippet"]["tags"]),
            "thumbnail": f"thumbnail_{thumb}.png", "playlist": (s.get("playlists") or {}).get(kind_of(pr)), "captions": bool(s["captions"])}
    if dry_run:
        print("[yt-publish] 미리 보기 (올리지 않음):\n" + json.dumps(plan, ensure_ascii=False, indent=1))
        return plan
    if not video.exists():
        raise SystemExit(f"[yt-publish] 영상 없음: {video}")
    tok = _token()
    rec = {"project": pr.path.name, **plan, "steps": []}
    vid = upload(tok, video, meta)
    rec.update(video_id=vid, url=f"https://youtu.be/{vid}", studio=f"https://studio.youtube.com/video/{vid}/edit")
    rec["steps"].append("upload")
    rec_p.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")   # 업로드 직후 기록 (뒤 단계가 실패해도 중복 업로드 방지)
    for name, fn in (("thumbnail", lambda: thumbnail(tok, vid, edir / f"thumbnail_{thumb}.png") if (edir / f"thumbnail_{thumb}.png").exists() else None),
                     ("captions", lambda: captions(tok, vid, ass_to_srt(edir / "subs.ass")) if s["captions"] and (edir / "subs.ass").exists() else None),
                     ("playlist", lambda: playlist(tok, vid, plan["playlist"]) if plan["playlist"] else None)):
        try:
            fn()
            rec["steps"].append(name)
        except SystemExit as e:   # 썸네일은 전화 인증 안 된 채널이면 거절됨 → 영상은 그대로 두고 기록
            rec.setdefault("warnings", []).append(f"{name}: {e}")
    rec["done_at"] = dt.datetime.now(KST).isoformat(timespec="seconds")
    rec_p.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[yt-publish] {rec['url']} · {plan['privacy']}{' → ' + plan['publishAt'] + ' 공개 예약' if plan['publishAt'] else ''} · {', '.join(rec['steps'])}"
          + (f" · 경고 {len(rec['warnings'])}" if rec.get("warnings") else ""))
    return rec


def _resume(pr: Project, rec: dict, rec_p: Path, thumb: str) -> dict:
    """이미 올린 영상에 빠진 단계(썸네일·자막·재생목록)만 다시."""
    s, edir, vid, tok = settings(pr), pr.dir("edit"), rec["video_id"], _token()
    steps = {"thumbnail": lambda: thumbnail(tok, vid, edir / f"thumbnail_{thumb}.png"),
             "captions": lambda: captions(tok, vid, ass_to_srt(edir / "subs.ass")),
             "playlist": lambda: playlist(tok, vid, rec["playlist"]) if rec.get("playlist") else None}
    rec["warnings"] = []
    for name, fn in steps.items():
        if name in rec["steps"]:
            continue
        try:
            fn()
            rec["steps"].append(name)
        except SystemExit as e:
            rec["warnings"].append(f"{name}: {e}")
    rec["resumed_at"] = dt.datetime.now(KST).isoformat(timespec="seconds")
    rec_p.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[yt-publish] 다시: {', '.join(rec['steps'])}" + (f" · 경고 {len(rec['warnings'])}" if rec["warnings"] else ""))
    return rec


def request_github(project: str, at: str | None = None, privacy: str | None = None, thumb: str = "A", resume: bool = False) -> None:
    """GitHub Actions 에 올리기를 맡긴다: publish/<프로젝트> 브랜치에 요청 파일 하나를 올리면 워크플로가 Release 영상을 받아 올린다."""
    import subprocess
    import tempfile
    root = config.ROOT
    pr = Project.open(project)
    name = pr.path.name
    if not (pr.dir("edit") / "youtube.md").exists():
        raise SystemExit("[yt-publish] 05_edit/youtube.md 가 없습니다 — 먼저 python -m ytflow yt-pack " + name)
    if not resume and not (pr.dir("edit") / "release.json").exists():
        raise SystemExit("[yt-publish] 영상이 GitHub Release 에 없습니다 — 먼저 python -m ytflow upload " + name)
    req = json.dumps({"project": name, "at": at, "privacy": privacy, "thumb": thumb, "resume": resume}, ensure_ascii=False)
    work = Path(tempfile.mkdtemp(prefix="ytflow-pub-"))
    (work / "req.json").write_text(req, encoding="utf-8")
    env = dict(os.environ, GIT_INDEX_FILE=str(work / "index"))
    g = lambda *a: subprocess.run(["git", *a], cwd=root, env=env, capture_output=True, text=True, check=True).stdout.strip()
    g("read-tree", "HEAD")
    g("update-index", "--add", "--cacheinfo", f"100644,{g('hash-object', '-w', str(work / 'req.json'))},_publish/{name}.json")
    commit = g("commit-tree", g("write-tree"), "-p", "HEAD", "-m", f"publish: {name} (Actions 가 유튜브에 올리고 이 브랜치를 지움)")
    r = subprocess.run(["git", "push", "-f", "origin", f"{commit}:refs/heads/publish/{name}"], cwd=root, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(r.stderr[-600:])
    print(f"[yt-publish] GitHub Actions 에 요청함 → 몇 분 뒤 05_edit/youtube_publish.json 이 main 에 기록됩니다 (Actions 탭 'youtube-publish')")
