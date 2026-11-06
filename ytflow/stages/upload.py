"""완성 영상을 Google Drive 의 채널(편집 스타일)별 폴더에 올린다.

- 올리는 파일: 05_edit/final.mp4 (없으면 draft.mp4) + 자막 subs.srt + 업로드 문구(upload.json 을 텍스트로)
- 폴더: config/storage.yaml 의 drive.folders (채널 id → 폴더 id). 예전 프로젝트는 스타일로, 실험 프로젝트는 '실험' 폴더로.
- 이미 올린 파일은 05_edit/drive.json 에 기록해 다시 올리지 않는다(파일이 바뀌면 크기로 알아채고 새로 올림).
- 방법 1 (PC, 권장): config/storage.yaml 의 local_sync_dir 에 'Google Drive for desktop' 동기화 폴더를 적으면 복사만 한다.
- 방법 2: Google Drive API 토큰(www.googleapis.com). 이 클라우드 환경에서는 네트워크 비밀값으로 저장하면 프록시가 붙여 준다.
  PC 에서는 환경변수 GOOGLE_DRIVE_TOKEN 에 OAuth 접근 토큰(scope drive.file)을 넣는다.
"""
from __future__ import annotations

import json
import os
import urllib.parse
import urllib.error
import urllib.request

import yaml

from .. import config
from ..project import Project

API = "https://www.googleapis.com"
CHUNK = 8 * 1024 * 1024


def _cfg() -> dict:
    return yaml.safe_load((config.CONFIG_DIR / "storage.yaml").read_text(encoding="utf-8"))["drive"]


def _auth() -> dict:
    tok = os.environ.get("GOOGLE_DRIVE_TOKEN", "proxy-injected")  # 클라우드에서는 프록시가 실제 토큰으로 바꿔 끼운다
    return {"Authorization": f"Bearer {tok}"}


def folder_for(project: Project) -> tuple[str, str]:
    c = _cfg()
    name = project.path.name
    if name in c.get("experiments", []):
        return "experiment", c["folders"]["experiment"]
    pc = config.load("pipeline")
    cid = pc.get("channel") or c.get("style_to_channel", {}).get((pc.get("edit") or {}).get("style_ref", ""), "experiment")
    return cid, c["folders"].get(cid, c["folders"]["experiment"])


def _upload(path, title: str, mime: str, parent: str) -> str:
    """일시적 서버 오류(5xx·429·연결 끊김)는 4번까지 기다렸다가 처음부터 다시 올린다."""
    import time
    for i in range(5):
        try:
            return _upload_once(path, title, mime, parent)
        except urllib.error.HTTPError as e:
            if e.code < 500 and e.code != 429 or i == 4:
                raise
        except (urllib.error.URLError, ConnectionError, TimeoutError):
            if i == 4:
                raise
        time.sleep(2 ** (i + 1))
    return ""


def _upload_once(path, title: str, mime: str, parent: str) -> str:
    size = path.stat().st_size
    meta = json.dumps({"name": title, "parents": [parent]}).encode()
    req = urllib.request.Request(f"{API}/upload/drive/v3/files?uploadType=resumable&fields=id", data=meta, method="POST",
                                 headers={**_auth(), "Content-Type": "application/json; charset=UTF-8",
                                          "X-Upload-Content-Type": mime, "X-Upload-Content-Length": str(size)})
    with urllib.request.urlopen(req, timeout=60) as r:
        session = r.headers["Location"]
    with open(path, "rb") as fh:
        off = 0
        while off < size:
            chunk = fh.read(CHUNK)
            end = off + len(chunk) - 1
            put = urllib.request.Request(session, data=chunk, method="PUT",
                                         headers={**_auth(), "Content-Length": str(len(chunk)),
                                                  "Content-Range": f"bytes {off}-{end}/{size}"})
            try:
                with urllib.request.urlopen(put, timeout=300) as r:
                    return json.loads(r.read() or b"{}").get("id", "")
            except urllib.error.HTTPError as e:
                if e.code != 308:  # 308 = 다음 조각을 계속 보내라
                    raise
            off = end + 1
    return ""


def _folder(name: str, parent: str) -> str:
    """parent 아래 name 폴더를 찾고, 없으면 만든다 (API 방식)."""
    q = urllib.parse.quote(f"name = '{name}' and '{parent}' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false")
    with urllib.request.urlopen(urllib.request.Request(f"{API}/drive/v3/files?q={q}&fields=files(id)", headers=_auth()), timeout=30) as r:
        hit = json.loads(r.read()).get("files") or []
    if hit:
        return hit[0]["id"]
    body = json.dumps({"name": name, "parents": [parent], "mimeType": "application/vnd.google-apps.folder"}).encode()
    req = urllib.request.Request(f"{API}/drive/v3/files?fields=id", data=body, method="POST",
                                 headers={**_auth(), "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())["id"]


# GitHub 에 올리지 않지만 다시 만들 수 없는 것 (docs/09-storage.md). 음성·렌더·작업 폴더는 다시 만들 수 있어 올리지 않는다.
ARCHIVE_GLOBS = ["04_assets/*_shot.*", "04_assets/*_temp.*", "04_assets/scene_[0-9][0-9][0-9].mp4", "04_assets/repo_full.png",
                 "01_research/subs/*.vtt", "01_research/prices/*.json", "05_edit/final_sheet.png"]


def archive(project: Project) -> None:
    """프로젝트의 보관 자료(장면 소스 캡처·사진·받은 원본 클립·자막·시세)를 '보관 자료/<프로젝트>/' 에 올린다."""
    files = [p for g in ARCHIVE_GLOBS for p in project.path.glob(g) if p.is_file()]
    if not files:
        return
    c = _cfg()
    sync = c.get("local_sync_dir")
    if sync:
        import shutil
        from pathlib import Path
        dst = Path(sync).expanduser() / c["folder_names"]["archive"] / project.path.name
        for p in files:
            (dst / p.parent.name).mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, dst / p.parent.name / p.name)
        print(f"[archive] {project.path.name}: {len(files)}개 → {dst}")
        return
    rec_f = project.dir("edit") / "drive_archive.json"
    rec = json.loads(rec_f.read_text(encoding="utf-8")) if rec_f.exists() else {}
    folder = _folder(project.path.name, c["folders"]["archive"])
    subs = {}
    for p in files:
        key = str(p.relative_to(project.path))
        if rec.get(key, {}).get("size") == p.stat().st_size:
            continue
        sub = subs.get(p.parent.name) or subs.setdefault(p.parent.name, _folder(p.parent.name, folder))
        mime = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".mp4": "video/mp4",
                ".vtt": "text/vtt", ".json": "application/json"}.get(p.suffix.lower(), "application/octet-stream")
        rec[key] = {"id": _upload(p, p.name, mime, sub), "size": p.stat().st_size}
    rec_f.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[archive] {project.path.name}: {len(files)}개 보관")


def run(project: Project) -> None:
    edir = project.dir("edit")
    vid = edir / "final.mp4" if (edir / "final.mp4").exists() else edir / "draft.mp4"
    if not vid.exists():
        print(f"[upload] {project.path.name}: 영상 없음 (건너뜀)")
        return
    cid, parent = folder_for(project)
    rec_f = edir / "drive.json"
    rec = json.loads(rec_f.read_text(encoding="utf-8")) if rec_f.exists() else {}
    up_f = project.dir("package") / "upload.json"
    title = json.loads(up_f.read_text(encoding="utf-8"))["titles"][0] if up_f.exists() \
        else project.state().get("name", project.path.name)
    base = f"{project.path.name[:8]} {title}".replace("/", "·")[:120]
    files = [(vid, f"{base}.mp4", "video/mp4")]
    if (edir / "subs.srt").exists():
        files.append((edir / "subs.srt", f"{base}.srt", "application/x-subrip"))
    up = project.dir("package") / "upload.json"
    if up.exists():  # 업로드 문구를 사람이 읽는 텍스트로
        d = json.loads(up.read_text(encoding="utf-8"))
        txt = project.dir("package") / "upload.txt"
        txt.write_text("제목 후보\n" + "\n".join(d.get("titles", [])) + "\n\n설명\n" + d.get("description", "") +
                       "\n\n태그\n" + ", ".join(d.get("tags", [])) + "\n\n고정 댓글\n" + d.get("pinned_comment", ""), encoding="utf-8")
        files.append((txt, f"{base} - 업로드 문구.txt", "text/plain"))
    sync = _cfg().get("local_sync_dir")
    if sync:  # Google Drive for desktop 동기화 폴더로 복사 (토큰 불필요, 드라이브 앱이 올림)
        import shutil
        from pathlib import Path
        dst = Path(sync).expanduser() / _cfg()["folder_names"][cid]
        dst.mkdir(parents=True, exist_ok=True)
        for path, name, _ in files:
            shutil.copy2(path, dst / name)
            print(f"[upload] → {dst / name}")
        return
    for path, name, mime in files:
        key = path.name
        if rec.get(key, {}).get("size") == path.stat().st_size:
            print(f"[upload] = {name} (이미 올림)")
            continue
        fid = _upload(path, name, mime, parent)
        rec[key] = {"id": fid, "size": path.stat().st_size, "folder": cid, "name": name}
        print(f"[upload] ↑ {cid}/{name} ({path.stat().st_size / 1e6:.1f}MB) → https://drive.google.com/file/d/{fid}/view")
    rec_f.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")


def archive_repo() -> None:
    """프로젝트 밖의 비공개 보관 자료: 벤치마킹 원자료(data/), 스타일 분석 장면 미리보기(styles/*/work/)."""
    c = _cfg()
    files = [p for p in list(config.DATA_DIR.rglob("*")) + list(config.STYLES_DIR.glob("*/work/*"))
             if p.is_file() and p.name != "style_profile.json" and p.name != "jargon.json"]
    sync = c.get("local_sync_dir")
    root_name = "저장소 자료 (data·styles work)"
    if sync:
        import shutil
        from pathlib import Path
        for p in files:
            dst = Path(sync).expanduser() / c["folder_names"]["archive"] / root_name / p.relative_to(config.ROOT).parent
            dst.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, dst / p.name)
        print(f"[archive] 저장소 자료 {len(files)}개 → 동기화 폴더")
        return
    base = _folder(root_name, c["folders"]["archive"])
    for p in files:
        parent = base
        for part in p.relative_to(config.ROOT).parent.parts:
            parent = _folder(part, parent)
        _upload(p, p.name, "application/octet-stream", parent)
    print(f"[archive] 저장소 자료 {len(files)}개 보관")
