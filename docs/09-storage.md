# 09. 어디에 무엇을 두나 — GitHub / Google Drive / 다시 만들기

Claude Code 와 Codex 가 **같은 GitHub 저장소**(LBIN8787/video-editing)를 씁니다. 코드·문서·기획 파일은 GitHub, 큰 미디어는 Google Drive 에 둡니다.

## 0. 2026-11-15부터: 파일은 Google Drive 에서 관리 (D 드라이브 대신, 사용자 요청)

### 0) Git 과 Drive 의 역할 (2026-11-16 사용자 정정)
> "깃과 드라이브 둘다 보관 할 수 있도록 해줘 내 의도는 그거야 즉 깃에 보관하되 깃에 보관하기 힘든 부분은 드라이브쪽을 활용하라는거야 로컬드라이브 부담을 줄이는게 목적이고"

| 어디 | 무엇 |
|---|---|
| **Git** | 코드·문서·설정·기획(md/json/csv/yaml)·작은 분석 결과, 그리고 Drive 에 둔 큰 파일의 **위치·판본·크기·검수 상태** 메타데이터 |
| **Google Drive** | 큰 영상·오디오·반복 프레임·원자료 묶음 — Git 이력에 부담이 되는 것 |
| GitHub Release (선택) | 공개·권리상 문제없는 완성본만. Drive 대신 강제하지 않음 |

- 모든 파일을 두 곳에 두라는 뜻이 **아니다**. 필요하면 사본을 둘 수 있을 뿐.
- 목적은 PC 저장공간 줄이기. 단, Drive 에 두었다고 PC 용량이 0 은 아니다(앱 캐시·오프라인 사본 설정을 따로 확인).
- 올리기·동기화가 끝나고 보관본을 다시 열어 확인하기 전에는 PC 원본을 지우지 않는다. 지우기는 따로 허락받는다.
- 공개 Git 에는 로그인 화면·비공개 스튜디오 자료·개인정보·자격증명·접근 토큰이 든 링크를 넣지 않는다.
- 이 정정은 저장 위치 규칙일 뿐, PC Drive 동기화 재개·파일 이전·삭제를 승인한 것이 아니다.

**내려받는 것·만드는 큰 파일은 모두 Google Drive 에 둡니다.** PC 에서는 Google Drive for desktop 이 Drive 를 드라이브 문자(보통 `G:`)로 보여 주므로, 그 안의 폴더에 저장하면 자동으로 올라갑니다.

### 1) 한 번만 설정 (PowerShell)
```powershell
# Google Drive for desktop 설치·로그인 후, 탐색기에서 '내 드라이브' 경로를 확인 (예: G:\내 드라이브)
mkdir "G:\내 드라이브\ytflow\refs", "G:\내 드라이브\ytflow\cache", "G:\내 드라이브\ytflow\영상"
setx YTFLOW_DRIVE "G:\내 드라이브\ytflow"
```
새로 연 터미널·Claude Code·Codex 부터 적용됩니다(`echo $env:YTFLOW_DRIVE`).

### 2) 무엇을 어디에
| 무엇 | 위치 |
|---|---|
| 레퍼런스 영상 캡처·rea-video 분석 결과 (`skills/ref-watch-ego`) | `%YTFLOW_DRIVE%\refs\<영상ID>\` |
| 사용자가 받은 원본 영상·자료 화면 | `%YTFLOW_DRIVE%\refs\` 또는 `%YTFLOW_DRIVE%\cache\` |
| ytflow 캐시 (받은 자료·측정) | `YTFLOW_DRIVE` 가 있으면 자동으로 `%YTFLOW_DRIVE%\cache` (`ytflow/config.py`) |
| 완성 영상·자막·업로드 문구 | `%YTFLOW_DRIVE%\영상\` (GitHub Release 는 공개해도 되는 것만 선택) |
| 클라우드 세션에서 만든 파일 | Drive 커넥터로 `ytflow` 폴더에 업로드(파일당 10MB). 큰 영상은 rclone(§2 표) 또는 GitHub Release |

### 3) 예외 — Drive 동기화 폴더에 두면 안 되는 것
Drive 동기화는 파일 수만 개짜리 폴더와 계속 바뀌는 잠금 파일에 약해서 아래는 망가지거나 동기화가 멈춥니다. **PC 의 기존 위치에 그대로** 둡니다(새로 만들지 않음).
- git 저장소 `video-editing` (`.git` 이 깨질 수 있음)
- 파이썬 가상환경(`reavenv`)·pip/npm 캐시·Playwright 브라우저·받아쓰기 모델(`HF_HOME`)·`REA_VIDEO_MODELS`
- 렌더 중간 파일(`04_assets/hb*`, `05_edit/*work/`) — 다시 만들 수 있으므로 저장소 안에 두고 Release 뒤 지웁니다.

아래 'D 드라이브' 절은 이 예외 항목에만 해당하는 예전 기록입니다.

## 1. GitHub (git)
코드(`ytflow/`), 문서(`docs/`, `AGENTS.md`), 절차서(`skills/`), 설정(`config/`, `channels/`, `styles/*/` 의 md·yaml·json),
프로젝트 기획 파일(`projects/*/` 의 md·json·csv·srt·ass·yaml: 소스 목록·팩트시트·원고·대본·업로드 문구·보고서).

## 2. 영상 보관 — GitHub Release (선택: 공개해도 되는 것만, 키 불필요) — 2026-11-07부터 · 2026-11-20 사용자 "깃과 드라이브로 나눠서 해줘" 로 기본은 Drive(§0)
`python -m ytflow upload <프로젝트> [--archive]` → 릴리스 `video-<프로젝트>` 에 final.mp4·자막·업로드 문구(+ footage.zip).
임시 브랜치 `media/<프로젝트>` 를 push 하면 `.github/workflows/media-release.yml` 이 릴리스에 붙이고 브랜치를 지웁니다.
Drive 토큰처럼 1시간마다 만료되는 키가 없습니다. 주소는 `05_edit/release.json`. 자세한 절차: `docs/11-playbook.md`.

### 왜 Drive 를 기본에서 뺐나
| 방법 | 문제 |
|---|---|
| Drive API 토큰(네트워크 비밀값) | Google 접근 토큰은 약 1시간 뒤 만료 → 매번 새로 넣어야 함 |
| Claude 의 Google Drive 커넥터 | 키는 필요 없지만 파일 하나 **10MB 제한** → 문서·업로드 문구용으로만 |
| Drive + rclone (선택) | PC 에서 `rclone authorize "drive"` 로 받은 **오래가는 토큰**을 환경 변수 `RCLONE_CONFIG_GDRIVE_TYPE=drive`, `RCLONE_CONFIG_GDRIVE_TOKEN=<JSON>` 로 한 번만 넣으면 이후 자동 갱신. 원하면 이 방식으로 `--to drive` 를 연결 |

## 2-1. (예전 방식) Google Drive — `ytflow 영상` 폴더 (`config/storage.yaml`)
| 폴더 | 무엇 | 올리는 명령 |
|---|---|---|
| `롱폼 · 미주일기 스타일 (ch-paper-column)` 등 채널별 6개 | 완성 영상(final.mp4, 없으면 draft.mp4) + 자막 .srt + 업로드 문구 .txt | `python -m ytflow upload <프로젝트>` / `--all` |
| `보관 자료 (GitHub 밖)/<프로젝트>/` | **다시 만들 수 없는 것**: 장면 소스(기사·문서 캡처, 위키미디어 사진, 임시 썸네일), 받은 원본 클립, 조사용 자막·시세 캐시, 프레임 시트 | `python -m ytflow upload --all --archive` |
| `보관 자료 (GitHub 밖)/저장소 자료 (data·styles work)/` | 벤치마킹 원자료(`data/`: 채널 지표·자막), 스타일 분석 장면 미리보기(`styles/*/work/`) — **타 채널 자료라 비공개 보관만** | 같은 명령(`--all --archive`) |
| `워크플로우 문서 (영상 제작 기준)` | `00 영상 제작 워크플로우 기준(먼저 읽기)` + 운영 루틴·채널·편집 스타일·형식·소스 찾기·목소리·보관·도구 도입 기록 (GitHub 문서의 **읽기용 사본** — 원본은 GitHub) | 문서가 크게 바뀌면 에이전트가 Drive 커넥터로 다시 올림 |
| 채널 폴더 안 `<날짜> <제목> - 원고·업로드 문구` | 영상별 제목 후보·썸네일 문구·설명·태그·내레이션 전문 (영상 파일 옆에 두는 읽기용) | 같은 방식 |
| `ytflow 영상 목록` (문서) | 영상 목록·길이·GitHub 경로 | 수동 갱신 |

- 이미 올린 파일은 `05_edit/drive.json`, `drive_archive.json` 에 기록되어 다시 올리지 않습니다.
- **올리는 방법 두 가지**
  1. **PC (권장):** Google Drive for desktop 을 설치하고 `config/storage.yaml` 의 `local_sync_dir` 에 `ytflow 영상` 동기화 폴더 경로를 적습니다 → 복사만 하면 드라이브 앱이 올립니다(토큰 불필요).
  2. **클라우드 세션:** 환경 설정 → 네트워크 비밀값에 `www.googleapis.com` 용 Drive 토큰(Authorization: Bearer, drive.file 권한)을 넣으면 API 로 이어 올리기합니다.

## 3. 다시 만들 수 있어 어디에도 올리지 않는 것
| 무엇 | 다시 만드는 명령 |
|---|---|
| 내레이션 음성 `03_voice/` | `stage <프로젝트> voice` |
| 장면 렌더 결과 `04_assets/*_anim.mp4`, `*_card.png` | `stage <프로젝트> assets` |
| HyperFrames 작업 폴더 `04_assets/hf/` (카드 HTML) | `stage <프로젝트> assets` |
| 편집 중간 파일 `05_edit/work/` | `stage <프로젝트> assemble` |
| 외부 도구 `tools/`, 외부 skill 복사본 | `python scripts/install_tools.py` |
| 캐시 `.cache/` (ElevenLabs 음성 캐시 포함) | 자동 (ElevenLabs 캐시는 지우면 크레딧이 다시 듦 → 지우지 않기 권장) |

## 4. 2026-11-06 현황 — 업로드 완료
- Drive 토큰(네트워크 비밀값, drive.file 권한)으로 `python -m ytflow upload --all --archive` 실행 완료.
- 영상 14편(프로젝트마다 final.mp4, 없으면 draft.mp4) + 자막 .srt + 업로드 문구 .txt → 채널별 폴더. 실험 프로젝트 8개는 `실험` 폴더.
- 보관 자료 230개(장면 소스·원본 클립·조사 자막·시세·프레임 시트) → `보관 자료 (GitHub 밖)/<프로젝트>/`, 저장소 자료 25개(data·styles work).
- 총 296개, 약 610MB. Drive 의 파일 크기를 원본과 대조해 불일치 0개.
- 올린 기록: `projects/*/05_edit/drive.json`, `drive_archive.json` (GitHub 에 커밋됨 → Codex 도 무엇이 올라갔는지 압니다).
- 주의: drive.file 권한 토큰은 **이 앱이 만든 파일만** 봅니다. 커넥터로 만든 폴더 안에 올리는 것은 되지만, 그 폴더의 다른 파일 목록은 API 로 보이지 않습니다.
- 다음부터는 영상을 만든 뒤 `python -m ytflow upload <프로젝트> --archive` 한 번이면 됩니다(이미 올린 것은 건너뜀, 일시 오류는 자동 재시도).

## (예전, 2026-11-11) 내 PC 에서 돌릴 때 — C 드라이브 대신 D 드라이브 쓰기
> 2026-11-15부터 파일은 Google Drive(§0). 이 절은 §0-3 예외 항목(저장소·도구 설치)의 기존 위치 기록입니다.
영상 한 편에 렌더 중간 파일이 0.5~1GB 생깁니다. **모든 작업은 D 드라이브에서** 합니다.

### 1) 저장소를 D 에 두기 (가장 중요)
```powershell
D:
mkdir D:\ytflow
cd D:\ytflow
git clone https://github.com/LBIN8787/video-editing.git
cd video-editing
```
이미 C 에 받아 두었다면 폴더째 `D:\ytflow\video-editing` 로 옮기면 됩니다(옮긴 뒤 그 폴더에서 Claude Code / Codex 를 엽니다).
프로젝트(`projects/`)·렌더 도구(`tools/`)·배경음(`assets/bgm/`)이 모두 저장소 안에 있으므로 함께 D 로 갑니다.

### 2) 저장소 밖으로 새는 캐시도 D 로 (한 번만, PowerShell)
| 무엇 | 환경변수 | 값 |
|---|---|---|
| ytflow 캐시 (받은 자료·음성 캐시·측정) | `YTFLOW_CACHE_DIR` | `D:\ytflow\cache` |
| 받아쓰기 모델(faster-whisper, 수백 MB) | `HF_HOME` | `D:\ytflow\hf` |
| 렌더용 브라우저(Playwright) | `PLAYWRIGHT_BROWSERS_PATH` | `D:\ytflow\ms-playwright` |
| npm 캐시 | `npm_config_cache` | `D:\ytflow\npm-cache` |
| pip 캐시 | `PIP_CACHE_DIR` | `D:\ytflow\pip-cache` |
| 임시 파일 | `TMP`, `TEMP` | `D:\ytflow\tmp` |

```powershell
mkdir D:\ytflow\cache, D:\ytflow\hf, D:\ytflow\ms-playwright, D:\ytflow\npm-cache, D:\ytflow\pip-cache, D:\ytflow\tmp
setx YTFLOW_CACHE_DIR D:\ytflow\cache
setx HF_HOME D:\ytflow\hf
setx PLAYWRIGHT_BROWSERS_PATH D:\ytflow\ms-playwright
setx npm_config_cache D:\ytflow\npm-cache
setx PIP_CACHE_DIR D:\ytflow\pip-cache
setx TMP D:\ytflow\tmp
setx TEMP D:\ytflow\tmp
```
`setx` 는 **새로 연 창부터** 적용됩니다. 터미널·Claude Code·Codex 를 다시 연 뒤 `echo $env:YTFLOW_CACHE_DIR` 로 확인하세요.
(TMP/TEMP 를 바꾸면 다른 프로그램의 임시 파일도 D 로 갑니다. 원치 않으면 이 두 줄은 빼도 됩니다.)

### 3) 공간 정리 (영상을 Release 에 올린 뒤)
렌더 중간 파일은 언제든 다시 만들 수 있습니다. Release 에 올린 프로젝트는 아래를 지워도 됩니다:
`04_assets/hb/`, `04_assets/hb_*.mp4`, `05_edit/hb_work/`, `05_edit/draft.mp4` (완성본 `final.mp4`·기획 문서·목소리는 남김)
