# 반복 운영 안내 (채널 운영 루틴)

ytflow 는 한 번 쓰고 끝내는 스크립트가 아니라 **매주 같은 순서로 도는 제작 라인**입니다.
조사하고 글로 정리하던 일(대화형 LLM 에 묻고 답을 다듬던 일)을 그대로 이어서, 그 글을 대본·화면·영상으로 바꿉니다.

## 1. 한 편이 만들어지는 길
| 단계 | 명령 (`python -m ytflow stage <프로젝트> <단계>`) | 산출물 | 사람이 볼 것 |
|---|---|---|---|
| 트렌드 | `discover` | `00_source/trends.json` | — |
| **소스 먼저** | `scout` (채널별 출발점: 발언 영상 / 1차 문서 / 숫자 계열) | `00_source/scout.json` | 화제마다 쓸 수 있는 원본이 있나 |
| 주제·형식 | `select` (소스가 강한 화제, 분석=롱폼 / 안내=쇼츠) | `shortlist.md`, 다른 형식은 `channels/<id>/queue.md` | **주제와 형식 — 가장 먼저 볼 곳** |
| 소스 목록 | research 시작 때 `inventory` | `00_source/inventory.md` (S번호, 사진 라이선스) | 이 영상의 재료 |
| 조사 | `research` | `01_research/factsheet.md`, `articles.json` | 숫자·발언의 출처, '재확인 필요' |
| **원고** | `article` | `01_research/article.md` | **칼럼(롱폼) / 안내(쇼츠) 원고 — 가장 중요한 검수 지점** |
| 대본 | `script` | `02_script/scenes.json`, `script.md` | 장면 나눔, 비유·과거 사례 (`validate`) |
| 소스 | `sources` → `clips` | `04_assets/sources.csv`, 캡처 | 원본 소스형만 중요 |
| 영상 | `voice` → `assets` → `subtitles` → `assemble` | `05_edit/final.mp4`, `final_sheet.png` | 프레임 시트 |
| 업로드 | `package` → `report` | `06_package/upload.json`, `REPORT.md` | 제목·썸네일 문구, 남은 일 |
| 보관 | `python -m ytflow upload <프로젝트>` | Google Drive `ytflow 영상/<채널·스타일>/` 에 영상·자막·업로드 문구 | Drive 폴더 (`config/storage.yaml`) |

## 2. 시작 방법
```bash
# ⓪ 기획만 먼저 (권장): 트렌드 → 소스 찾기 → 주제·형식 결정에서 멈춤 → shortlist.md 확인 후 진행
python -m ytflow make --channel ch-source-brief --plan
python -m ytflow approve <프로젝트> topic --pick 2 && python -m ytflow run <프로젝트>
```

```bash
# ① 트렌드에서 자동으로 (주제 선정부터)
python -m ytflow make --channel ch-paper-column

# ② 주제를 정해서
python -m ytflow make --channel ch-paper-column --topic "메타는 왜 번 돈보다 더 쓰나"

# ③ 이미 조사한 글이 있을 때 (대화형 LLM 답, 내 메모, 리포트 요약)
python -m ytflow make --channel ch-paper-column --from-text notes/메타-현금흐름.md
```
③ 은 가져온 글을 **사실 확인 대상**으로 다룹니다: research 가 글 속 숫자·발언을 1차 출처로 확인하고, article 이 형식에 맞게 다시 씁니다. 확인되지 않은 주장은 빠지거나 '확인되지 않았다'로 남습니다.

## 3. 주간 루틴 (예시)
| 요일 | 할 일 | 채널 |
|---|---|---|
| 월 | `make --channel ch-paper-column` → article.md 검수 → 필요하면 고치고 `stage <프로젝트> script` 부터 다시 | 롱폼 칼럼 |
| 화 | 실적 시즌이면 `make --channel ch-source-brief` → **PC 에서 `rebuild`** 로 원본 클립 채우기 | 롱폼 보고서 |
| 수·금 | `make --channel ch-ai-shorts` 2~3편 | 쇼츠 |
| 목 | final.mp4·REPORT.md 점검 → 업로드 → `episodes.md` 의 상태를 '업로드'로 | 전체 |
| 격주 | `make --channel ch-data-motion` | 데이터 리포트 |

## 4. 고칠 때는 그 단계부터
- 원고가 마음에 안 들면 `01_research/article.md` 를 직접 고치고 `stage <프로젝트> script` 부터.
- 대본만 고치면 `02_script/scenes.json` 수정 → `validate` → `stage voice` 부터 (`rebuild` 는 clips 부터 전부).
- 카드 하나만 다시 그리려면 `04_assets/hf/scene_XXX/index.html` 을 고치고 HyperFrames 로 다시 렌더(`skills/edit-style-mijudiary`).

## 5. 저장소에 남는 것
- 채널 설정·에피소드 기록(`channels/`), 원고·대본·팩트시트·업로드 문구(`projects/*/`의 md·json·csv)는 커밋합니다 → 지난 영상의 원고가 다음 영상의 자료가 됩니다.
- 영상·음성·이미지·외부 도구 본체는 커밋하지 않습니다(.gitignore).
