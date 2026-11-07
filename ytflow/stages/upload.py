"""완성 영상을 Google Drive 의 채널(편집 스타일)별 폴더에 올린다.

- 올리는 파일: 05_edit/final.mp4 (없으면 draft.mp4) + 자막 subs.srt + 업로드 문구(upload.json 을 텍스트로)
- 폴더: config/storage.yaml 의 drive.folders (채널 id → 폴더 id). 예전 프로젝트는 스타일로, 실험 프로젝트는 '실험' 폴더로.
- 이미 올린 파일은 05_edit/drive.json 에 기록해 다시 올리지 않는다(파일이 바뀌면 크기로 알아채고 새로 올림).
- **방법 0 (기본, 키 불필요): GitHub Release.** `upload <프로젝트> --to github` — 영상·자막·업로드 문구(+ --archive 면 자료 화면 묶음)를
  임시 브랜치 media/<프로젝트> 로 밀어 올리면 .github/workflows/media-release.yml 이 'video-<프로젝트>' 릴리스에 붙이고 브랜치를 지운다.
  git 자격 증명만 쓰므로 Drive 토큰이 필요 없다. 파일 하나 100MB 미만(넘으면 화질을 조금 낮춘 사본을 만든다).
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


# ---------------------------------------------------------------- GitHub Release (키 불필요)
LIMIT = 95 * 1024 * 1024  # git push 파일 하나 한도(100MB) 아래


def _fit(path, work):
    """100MB 넘는 영상은 화질을 조금 낮춘 사본으로 (해상도는 그대로)."""
    import subprocess
    if path.stat().st_size < LIMIT:
        return path
    out = work / path.name
    for crf in (23, 26, 29):
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(path), "-c:v", "libx264", "-preset", "medium",
                        "-crf", str(crf), "-c:a", "copy", str(out)], check=True)
        if out.stat().st_size < LIMIT:
            return out
    raise SystemExit(f"{path.name}: 100MB 아래로 줄이지 못했습니다")


def github_release(project: Project, with_archive: bool = False) -> str:
    """영상·자막·업로드 문구를 GitHub Release 'video-<프로젝트>' 에 붙인다 (Actions 가 처리). 반환: 릴리스 주소."""
    import shutil
    import subprocess
    import tempfile
    from pathlib import Path
    root = config.ROOT
    name = project.path.name
    edir = project.dir("edit")
    vid = edir / "final.mp4" if (edir / "final.mp4").exists() else edir / "draft.mp4"
    if not vid.exists():
        raise SystemExit(f"[upload] {name}: 영상 없음")
    work = Path(tempfile.mkdtemp(prefix="ytflow-rel-"))
    files = [_fit(vid, work)]
    for f in (edir / "subs.srt", edir / "subs.ass", edir / "upload.txt", project.dir("package") / "upload.txt"):
        if f.exists():
            files.append(f)
    if with_archive and (project.dir("assets") / "footage").is_dir():  # 다시 받기 어려운 자료 화면 원본
        z = shutil.make_archive(str(work / "footage"), "zip", project.dir("assets") / "footage")
        files.append(Path(z) if Path(z).stat().st_size < LIMIT else None)
        files = [f for f in files if f]
    pc = config.load("pipeline")
    notes = work / "release_notes.md"
    up_txt = next((f for f in files if f.name == "upload.txt"), None)
    head = up_txt.read_text(encoding="utf-8").split("\n")[0] if up_txt else name
    notes.write_text(
        f"## {head.replace('제목: ', '')}\n\n- 프로젝트: `projects/{name}` (기획·대본·팩트시트는 main 브랜치)\n"
        f"- 채널: `{pc.get('channel', '')}` · 스타일: `{(pc.get('edit') or {}).get('style_ref', '')}`\n"
        f"- 다시 만들기: `python -m ytflow hybrid {name}` (방법: AGENTS.md, skills/edit-style-hybrid)\n"
        f"- 파일: " + ", ".join(f"`{f.name}`" for f in files) + "\n", encoding="utf-8")
    files.append(notes)
    # 작업 트리를 건드리지 않고(plumbing) main 위에 커밋 하나를 만들어 media/<이름> 으로 push
    env = dict(os.environ, GIT_INDEX_FILE=str(work / "index"))
    g = lambda *a, **k: subprocess.run(["git", *a], cwd=root, env=env, capture_output=True, text=True, check=True, **k).stdout.strip()
    g("read-tree", "HEAD")
    for f in files:
        sha = g("hash-object", "-w", str(f))
        g("update-index", "--add", "--cacheinfo", f"100644,{sha},_media/{name}/{f.name}")
    tree = g("write-tree")
    commit = g("commit-tree", tree, "-p", "HEAD", "-m", f"media: {name} (Actions 가 릴리스에 붙이고 이 브랜치를 지움)")
    for k in range(4):
        r = subprocess.run(["git", "push", "-f", "origin", f"{commit}:refs/heads/media/{name}"], cwd=root, capture_output=True, text=True)
        if r.returncode == 0:
            break
        import time
        time.sleep(2 ** (k + 1))
    else:
        raise SystemExit(r.stderr[-800:])
    shutil.rmtree(work, ignore_errors=True)
    url = subprocess.run(["git", "remote", "get-url", "origin"], cwd=root, capture_output=True, text=True).stdout.strip()
    repo = url.rstrip("/").removesuffix(".git").split("github.com/")[-1]
    rel = f"https://github.com/{repo}/releases/tag/video-{urllib.parse.quote(name)}"
    rec = edir / "release.json"
    rec.write_text(json.dumps({"release": rel, "files": [f.name for f in files], "video_bytes": files[0].stat().st_size if files[0].exists() else None},
                              ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[upload] GitHub Release 로 보냄 (1~2분 뒤 생성): {rel}")
    return rel
