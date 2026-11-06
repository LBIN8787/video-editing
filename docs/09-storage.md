# 09. 어디에 무엇을 두나 — GitHub / Google Drive / 다시 만들기

Claude Code 와 Codex 가 **같은 GitHub 저장소**(LBIN8787/video-editing)를 씁니다. 코드·문서·기획 파일은 GitHub, 큰 미디어는 Google Drive 에 둡니다.

## 1. GitHub (git)
코드(`ytflow/`), 문서(`docs/`, `AGENTS.md`), 절차서(`skills/`), 설정(`config/`, `channels/`, `styles/*/` 의 md·yaml·json),
프로젝트 기획 파일(`projects/*/` 의 md·json·csv·srt·ass·yaml: 소스 목록·팩트시트·원고·대본·업로드 문구·보고서).

## 2. Google Drive — `ytflow 영상` 폴더 (`config/storage.yaml`)
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
