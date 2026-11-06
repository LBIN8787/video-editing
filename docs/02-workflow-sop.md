# 02. 제작 워크플로우 SOP — 소스 탐색부터 업로드 패키지까지

## 한 줄 실행 (자동화 전체)

```bash
python -m ytflow style 미주일기 a.mp4 b.mp4        # (스타일을 바꿀 때만) 레퍼런스 영상 → 편집 규칙·설정
python -m ytflow benchmark                         # (월 1회) 채널 벤치마킹 → 대본 규칙
python -m ytflow make --style-ref 미주일기          # 주제 선정 → 자료조사 → 대본 → 소스 → 음성·자막·편집 → 패키지 → 보고서
python -m ytflow rebuild <프로젝트>                 # (PC) 원본 클립을 받아 임시 화면 교체 후 재생성
```

| 자동화된 과정 | 담당 단계 | 사람이 볼 곳 |
|---|---|---|
| 주제 선정 | discover → select (아웃라이어 + Claude 평가) | `00_source/shortlist.md` |
| 소스 탐색 | sources (장면별 YouTube 영상·구간), clips (구간 다운로드·기사 캡처) | `04_assets/sources.csv`, `clips.csv` |
| 자료조사 | research (웹 검색, 출처·날짜·교차확인) | `01_research/factsheet.md` |
| 대본 작성 | script (스타일 프로필 + 팩트시트 → 장면 단위) | `02_script/script.md` |
| 편집점 | 장면 = 문장 단위, 원본 발언 구간, 카드 전환 (timeline) | `05_edit/timeline.csv` |
| 편집 스타일 | style (레퍼런스 영상 측정·해석) → assets/assemble 렌더러 | `data/styles/<이름>/rules.json`, `edit.yaml` |
| 자막 | subtitles (2단 원문+번역, 강조색, 상자형) | `05_edit/subs.srt` |
| 업로드 준비 | package, report | `REPORT.md` |

```
[0 벤치마킹] 월 1회 ─→ data/style_profile.json ──────────────┐ (모든 단계가 참조)
                                                               ▼
[1 소스탐색] → [2 주제선정] ⏸topic → [3 리서치] → [4 대본] ⏸script
   → [5 음성] → [6 자막] → [7 화면소스] → [8 가편집] ⏸draft → [9 패키지] → 업로드(사람)
```
⏸ = 사람 승인 게이트. `config/pipeline.yaml` 의 `gates` 에서 `auto` 로 바꾸면 자동으로 통과합니다.

## 단계별 상세

| # | 단계 | 자동으로 하는 일 | 사람이 하는 일 | 산출물 |
|---|---|---|---|---|
| 0 | benchmark | 기준 채널의 outlier, 제목, 훅, 말 속도, 컷 속도 측정 → 규칙 추출 | 채널 URL 입력, 프로필 검토 | `data/style_profile.json` |
| 1 | discover | 시드 키워드 최신 영상 검색 → **구독자 대비 조회수** 상위 후보, RSS 뉴스 | 시드 키워드 관리 | `00_source/candidates.json` |
| 2 | select | 후보와 뉴스로 주제 5개 제안 (관점, 시의성, 리스크, 점수) | **⏸ 주제 고르기** `approve topic --pick N` | `00_source/shortlist.md` |
| 3 | research | 소스 영상 자막 수집 → 출처·확인상태가 붙은 팩트시트 | `01_research/my_notes.md` 에 자료 추가, '재확인 필요' 검증 | `01_research/factsheet.md` |
| 4 | script | 스타일 프로필대로 **씬 단위 대본** 작성 (내레이션, 큰글씨, 강조어, 화면지시, 이미지 프롬프트, 효과음) | **⏸ 대본 검수** `scenes.json` 직접 수정 가능 | `02_script/scenes.json`, `script.md` |
| 4.5 | clips | 대본의 `source`(URL + 구간 또는 자막 키워드)대로 원본 영상의 해당 구간만 내려받음 | YouTube가 막으면 `clips.csv` 보고 직접 받아 `scene_XXX.mp4`로 넣기 | `04_assets/scene_XXX.mp4`, `clips.csv` |
| 5 | voice | 씬별 TTS(edge-tts) 또는 직접 녹음 → 앞뒤 무음 제거, 음량 정규화 | (manual이면) `scene_001.wav` … 녹음 | `03_voice/clean/*.wav` |
| 6 | subtitles | 20자 단위 자막 분할, 강조어 색 입힘, 큰글씨 레이어, 챕터 계산 | — | `05_edit/subs.srt`, `subs.ass` |
| 7 | assets | 씬별 화면 샷리스트 + 비어 있는 씬 표시 | 이미지·영상을 `04_assets/scene_00N.*` 로 넣기 (AI 이미지 프롬프트 제공) | `04_assets/shotlist.csv` |
| 8 | assemble | 씬 클립 생성(이미지는 켄번스 줌) → 이어붙이기 → 자막 번인 → BGM 더킹 | **⏸ 가편집 확인** 후 프리미어/캡컷에서 마무리 | `05_edit/draft.mp4`, `timeline.csv` |
| 9 | package | 제목 5안, 썸네일 문구와 콘셉트, 설명(챕터 포함), 태그, 고정댓글 | 썸네일 제작, 업로드 | `06_package/upload.json` |

## 일상 운영 명령

```bash
export ANTHROPIC_API_KEY=...            # 또는 `ant auth login`
python -m ytflow new "이번주-영상"
python -m ytflow run 이번주-영상          # topic 게이트에서 멈춤
python -m ytflow approve 이번주-영상 topic --pick 2
python -m ytflow run 이번주-영상          # script 게이트에서 멈춤
python -m ytflow approve 이번주-영상 script
#   (04_assets 에 화면 소스를 넣는다)
python -m ytflow run 이번주-영상          # draft 게이트에서 멈춤
python -m ytflow approve 이번주-영상 draft
python -m ytflow run 이번주-영상          # 패키지 생성 → 완료
python -m ytflow status 이번주-영상
```

단계 하나만 다시 돌리기: `python -m ytflow stage 이번주-영상 script`
(대본을 고친 뒤에는 `voice → subtitles → assets → assemble` 순서로 다시 실행)

## 주간 자동화 (크론 예시)

```cron
# 매월 1일 03:10 벤치마킹 갱신
10 3 1 * *  cd /path/video-editing && python -m ytflow benchmark --video >> logs/bench.log 2>&1
# 매주 월요일 07:40 새 프로젝트 생성 + 주제 후보까지 (topic 게이트에서 멈춰 사람을 기다림)
40 7 * * 1  cd /path/video-editing && python -m ytflow new "weekly" && python -m ytflow run weekly >> logs/weekly.log 2>&1
```
게이트에서 멈추면 `shortlist.md` 나 `script.md` 를 메일, 슬랙, 노션으로 보내는 알림을 붙이면 좋습니다
(n8n이나 Make의 '파일 생성 감지 → 메시지 전송' 흐름 하나로 충분합니다).

## 역할 분담 (1인 / 소규모 팀 기준)

| 역할 | 맡는 게이트 | 주당 예상 시간 |
|---|---|---|
| 기획자(=채널 운영자) | topic, 최종 업로드 | 30분 |
| 작가/검수 | script, 팩트 '재확인 필요' 검증 | 1~2시간 |
| 편집자 | assets 채우기, draft 마무리 (색보정, 밈, 효과음 정밀 배치), 썸네일 | 2~4시간 |

## 품질 체크리스트 (draft 게이트에서)

- [ ] 첫 5초 안에 훅 문장과 큰 글씨가 나온다
- [ ] 화면이 5초 넘게 멈춰 있는 구간이 없다 (`timeline.csv` duration 확인)
- [ ] 강조색 단어가 한 줄에 2개를 넘지 않는다
- [ ] 숫자와 고유명사 자막에 오타가 없다 (TTS 발음도 확인)
- [ ] 타 채널 화면이나 저작권이 불분명한 이미지가 없다
- [ ] 팩트시트의 '재확인 필요' 항목이 대본에서 단정적으로 쓰이지 않았다
- [ ] 측정 목표(`style_profile.targets`)와 실제 분량, 말 속도 차이가 ±15% 안이다

## 성과 피드백 루프

업로드 1주 뒤 각 영상의 조회수, 평균 시청 지속 시간, CTR을 `data/my_channel_results.csv` 에 적어 두고,
월간 벤치마킹 때 **내 채널을 `role: reference` 로 channels.yaml 에 추가**하면
스타일 프로필이 '남의 채널 + 내 실제 성과'를 같이 반영합니다.
