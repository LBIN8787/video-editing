# 12. 키 없이 Google Drive 에 영상 올리기 — Apps Script 자동 복사 (2026-11-07)

## 왜 이 방법인가
| 방법 | 키 | 한계 |
|---|---|---|
| Drive API 토큰 (예전) | 1시간마다 새로 | 매번 넣어야 함 |
| Claude 의 Google Drive 커넥터 | 없음 | **파일 하나 10MB** → 영상 불가, 문서만 |
| **Apps Script (이 문서)** | **없음** — 내 구글 계정 안에서 '나'로 실행 | 처음 한 번 5분 설치 |

흐름: 세션이 `python -m ytflow upload <프로젝트>` → GitHub Release(공개 저장소) →
**15분 안에** 내 Apps Script 가 새 릴리스를 보고 Drive `ytflow 영상/<채널 폴더>/<프로젝트>/` 로 복사.
세션·Codex 는 Drive 에 직접 접근하지 않으므로 키가 필요 없습니다.

## 설치 (한 번, PC 나 휴대폰 브라우저)
1. https://script.google.com → **새 프로젝트** → 이름 `ytflow drive sync`.
2. 왼쪽 `Code.gs` 내용을 지우고 저장소의 [`tools/drive-sync/Code.gs`](../tools/drive-sync/Code.gs) 전체를 붙여넣기.
3. 톱니바퀴(프로젝트 설정) → **'편집기에서 appsscript.json 매니페스트 파일 표시'** 켜기 →
   `appsscript.json` 내용을 [`tools/drive-sync/appsscript.json`](../tools/drive-sync/appsscript.json) 으로 바꾸기.
4. 위쪽 함수 선택에서 **`setup`** → **실행** → 권한 검토 → 내 계정 선택 →
   ('확인되지 않은 앱' 이 나오면 고급 → 이동) → 허용.
   - 허용하는 것: 내 Drive 파일 만들기, 외부 주소(GitHub) 읽기, 15분 반복 실행.
5. 끝. `실행 기록`에 '복사: …' 가 보이면 정상. 지금 있는 릴리스 3개가 바로 복사됩니다.

## 알아 둘 것
- 큰 영상(45MB 넘음)은 16MB 씩 나눠 받아 Drive 이어 올리기로 붙입니다(Apps Script 한 번 받기 50MB 제한).
- 한 번 실행은 6분까지 → 많이 밀려 있으면 다음 15분 회차에 이어서.
- 같은 이름(다시 만든 영상)은 이전 판을 Drive 휴지통으로 보내고 새로 올립니다.
- 채널 폴더 목록은 `Code.gs` 위쪽 `CHANNEL_FOLDERS`(= `config/storage.yaml`). 목록에 없는 채널(ch-knowledge 등)은 `ytflow 영상` 아래 채널 이름 폴더를 새로 만듭니다.
- 멈추기: Apps Script 왼쪽 '트리거' 에서 삭제.
- ⚠ 저장소가 **공개**라서 릴리스 영상도 링크를 아는 누구나 받을 수 있습니다. 공개 전 영상을 숨기려면 저장소를 비공개로 바꾸고,
  Apps Script 에는 GitHub 읽기 전용 토큰(fine-grained, Contents: Read)을 스크립트 속성에 한 번 넣어야 합니다(만료일 길게).
