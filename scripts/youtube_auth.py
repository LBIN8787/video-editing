"""유튜브 올리기 권한을 한 번만 받는다 (사용자 PC 에서 실행, docs/24-youtube-publish.md §1).

    python scripts/youtube_auth.py client_secret.json --to-github
    python scripts/youtube_auth.py client_secret.json --name knowledge --to-github   # 채널별 (호기심 '한겹 더 보면')
    (2026-11-23 부터 분석 읽기 권한 yt-analytics.readonly 도 함께 받음 — 예전 토큰이면 한 번 다시 실행, docs/63)

1) 브라우저가 열리면 이미 로그인된 구글 계정으로 → **채널 '이어읽는시장'(브랜드 계정)을 고르고** → 허용.
2) 받은 '갱신 토큰'을 GitHub 저장소 비밀값(YT_CLIENT_ID · YT_CLIENT_SECRET · YT_REFRESH_TOKEN)에 바로 넣는다
   (gh CLI 로그인 필요: gh auth login). --to-github 없이 실행하면 PC 의 파일(.youtube_token.json, 커밋 안 됨)에만 저장.
토큰은 화면·채팅에 출력하지 않는다. 표준 라이브러리만 씀.
"""
import argparse
import http.server
import json
import secrets
import subprocess
import sys
import threading
import urllib.parse
import urllib.request
import webbrowser
from pathlib import Path

# 올리기·관리 + 읽기 전용 분석 (2026-11-23: 채널 운영·분석을 에이전트에게 맡김 — 시청 지속·유입 경로·노출 클릭률, docs/63)
SCOPES = ("https://www.googleapis.com/auth/youtube.upload https://www.googleapis.com/auth/youtube.force-ssl"
          " https://www.googleapis.com/auth/yt-analytics.readonly")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("client_secret", help="구글 클라우드 콘솔에서 받은 OAuth 클라이언트(데스크톱 앱) JSON")
    ap.add_argument("--to-github", action="store_true", help="gh CLI 로 저장소 비밀값에 바로 넣기")
    ap.add_argument("--repo", default="LBIN8787/video-editing")
    ap.add_argument("--name", default="", help="채널별 권한 이름 (channel.yaml youtube.credentials, 예: knowledge) — 비밀값 YT_*_KNOWLEDGE")
    a = ap.parse_args()
    c = json.loads(Path(a.client_secret).read_text(encoding="utf-8"))
    c = c.get("installed") or c.get("web")
    got = {}

    class H(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            got.update({k: v[0] for k, v in q.items()})
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write("권한을 받았습니다. 이 창은 닫아도 됩니다.".encode())

        def log_message(self, *x):
            pass

    srv = http.server.HTTPServer(("127.0.0.1", 0), H)
    redirect = f"http://127.0.0.1:{srv.server_port}"
    state = secrets.token_urlsafe(16)
    url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode({
        "client_id": c["client_id"], "redirect_uri": redirect, "response_type": "code", "scope": SCOPES,
        "access_type": "offline", "prompt": "consent", "state": state})
    th = threading.Thread(target=srv.handle_request)
    th.start()
    print("브라우저에서 계정 → 올릴 채널 선택 → 허용 (창이 안 열리면 이 주소를 여세요):\n" + url)
    webbrowser.open(url)
    th.join(timeout=600)
    if got.get("state") != state or "code" not in got:
        sys.exit(f"권한을 받지 못했습니다: {got.get('error', '시간 초과')}")
    body = urllib.parse.urlencode({"code": got["code"], "client_id": c["client_id"], "client_secret": c["client_secret"],
                                   "redirect_uri": redirect, "grant_type": "authorization_code"}).encode()
    tok = json.loads(urllib.request.urlopen(urllib.request.Request("https://oauth2.googleapis.com/token", data=body)).read())
    if "refresh_token" not in tok:
        sys.exit("갱신 토큰이 없습니다 — https://myaccount.google.com/permissions 에서 이 앱 권한을 지우고 다시 실행하세요")
    # 어느 채널로 받았는지 확인 (브랜드 계정을 잘못 고르면 다른 채널에 올라감)
    me = json.loads(urllib.request.urlopen(urllib.request.Request(
        "https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true",
        headers={"Authorization": f"Bearer {tok['access_token']}"})).read())
    names = [x["snippet"]["title"] for x in me.get("items", [])]
    print("권한을 준 채널:", ", ".join(names) or "(없음)")
    vals = {"YT_CLIENT_ID": c["client_id"], "YT_CLIENT_SECRET": c["client_secret"], "YT_REFRESH_TOKEN": tok["refresh_token"]}
    # PC 에도 늘 저장 (yt-publish --via here 가 바로 씀, 커밋 안 됨) — 위치: 환경변수 YTFLOW_SECRETS, 없으면 ~/.ytflow
    import os
    d = Path(os.environ.get("YTFLOW_SECRETS") or Path.home() / ".ytflow")
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"youtube_{(a.name or 'default').lower()}.json"
    p.write_text(json.dumps(vals), encoding="utf-8")
    print(f"PC 에 저장: {p}")
    if a.to_github:
        sfx = f"_{a.name.upper()}" if a.name else ""
        for k, v in vals.items():
            subprocess.run(["gh", "secret", "set", k + sfx, "--repo", a.repo, "--body", v], check=True, capture_output=True)
        print(f"GitHub 비밀값 3개 저장 완료 ({a.repo}, 이름 끝 '{sfx or '없음'}').")
    print("이제 이 PC 에서 바로: python -m ytflow yt-publish <프로젝트> --via here")


if __name__ == "__main__":
    main()
