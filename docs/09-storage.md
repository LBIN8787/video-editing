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

## 4. 2026-11-06 현황
- Drive 에 만든 것: 채널별 폴더 6개, `보관 자료 (GitHub 밖)` 폴더, `ytflow 영상 목록` 문서, `benchmark_metrics.json`.
- **아직 못 올린 것:** 영상 16개(약 693MB), 장면 소스 이미지 277개(48MB), 스타일 분석 이미지 8개(32MB), 벤치마킹·조사 자막 20개(2MB).
  클라우드 세션에 Drive 토큰이 없어서입니다(커넥터는 파일 내용을 대화에 실어 보내는 방식이라 큰 파일을 못 옮김). 위 2의 방법 1 또는 2로 `upload --all --archive` 한 번이면 됩니다.
- 클라우드 컨테이너는 세션이 끝나면 사라집니다. 그 전에 올리지 못한 영상은 이 세션에서 보낸 파일을 내려받거나, PC 에서 `rebuild` 로 다시 만듭니다(기획 파일은 GitHub 에 있어 같은 영상이 다시 나옵니다. 목소리·시세는 그날 값).
