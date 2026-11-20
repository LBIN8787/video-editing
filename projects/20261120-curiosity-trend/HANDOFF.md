# 인계 — 로컬(PC)에서 이어 하기 (2026-11-20, 클라우드 세션 → PC)

사용자: "이 작업을 로컬에서 이어가주세요". 클라우드 세션에서는 PC 폴더를 붙일 수 없어(Remote Control 이 이 폴더를 클라우드에 열어 주지 않음) 이 문서로 넘깁니다.

## 지금 상태
| 단계 | 상태 |
|---|---|
| D1 주제 | 통과 — '권태사회'·넘기기 (`01_research/topic_card.md`) |
| 대본 | **v3 검토 대기** — `02_script/script_v3.md` (심리학 고양이 문법: 이야기 = 삽화, 설명 = 모션그래픽, 증거 = 실제 자료·인물 사진, 마디 = 검은 화면, 8~9분). v1(14분 30초, 실사 위주)은 사용자 기각 → v2(이야기형) → v3 |
| 원화 | **PC 할 일** — `inbox/pc-tasks/20261120-2310-art-curiosity-trend.md` · 주문서 `02_script/art_orders.md` (잼 편 화풍, 2×2 시트 5장: night1·room·lab·night2·ending) |
| 렌더 | v3 는 아직. v1 렌더러(`render_full.py`·`full_overlay.html`·`build_full.py`)의 모션그래픽 구성요소(점 그림·띠·막대·도장·빠져드는 막대·목록·끝 화면)를 그대로 쓰고, 실사 칸을 원화 칸으로 바꾸면 됨 |
| 업로드 | '한겹 더 보면' 채널, **일부 공개** (`channels/ch-knowledge/channel.yaml` youtube: expected_channel·privacy unlisted·publish_time null). `yt-publish` 가 올리기 직전 권한 채널 이름을 확인하고 다르면 멈춤 |

## 사용자가 정해 둔 것 (원문은 `manual/feedback.yaml`)
- 이야기를 들려주듯, 학습형 금지, 길이는 짧게 (v1 은 너무 김)
- 문제 → 왜 → 어떻게 극복으로 이어지게, 시청자가 "아 이래야겠구나"를 얻어 가게 (지우의 다음 날 밤: 묻기·머물기·나가기·챙기기)
- 실험은 결과 전에 '무엇을 묻는 실험인지' 먼저
- 배경음 없음
- 삽화는 잼 편처럼, 연출은 메모리 편처럼, 실제 자료가 있으면 넣기
- 출처 줄은 설명란으로 충분(화면은 선택), '자료 화면' 표시는 실사 스톡을 안 쓰면 거의 필요 없음
- 업로드는 앞으로 **구글 드라이브를 거쳐서** (원본 화질). 클라우드 Drive 커넥터는 한 번에 ~3MB 라 못 함 → PC 의 Drive for desktop(`YTFLOW_DRIVE`)에 원본을 두고 올리는 경로가 필요 (`ytflow/stages/ytpublish.py` 는 지금 GitHub Release 영상을 받음 — Release 는 100MB 아래로 다시 압축됨)

## PC 에서 순서
1. `git pull` → `inbox/pc-tasks/20261120-2310-art-curiosity-trend.md` 대로 원화 5장 (Codex imagegen) → Drive `영상/20261120-curiosity-trend/art/`
2. 대본 v3 사용자 확인(D2) → 장면표 v3 (`build_full.py` 를 v3 문단·화면 표시(🎨📊📷⬛)에 맞게 고침, 원화 칸 자르기: `python -m ytflow art-cut` 또는 직접)
3. 실제 자료: 러셀 흑백 사진(Commons 'Bertrand Russell, 1894.jpg', 퍼블릭 도메인), 대니얼 길버트(Commons 'Daniel Gilbert.jpg' — 라이선스 다시 확인), 논문 제목은 글자로 다시 씀
4. 목소리: 초안 edge-tts(ko-KR-InJoonNeural, +4%, 업로드 전 사용자 확인) → 최종 ElevenLabs(채널 voice_id YBRudLRm83BV5Mazcr42, eleven_v4)
5. 렌더 → 프레임 확인 → `05_edit/youtube.md`(이미 있음, 챕터 시각은 v3 로 다시) · 썸네일 A/B/C(있음, 필요하면 다시)
6. 원본을 Drive `영상/20261120-curiosity-trend/` 에 두고 유튜브 일부 공개 업로드 → 링크를 사용자에게

## 파일
- 대본: `02_script/script_v1.md`(기각) · `script_v2.md` · **`script_v3.md`**
- 조사: `01_research/factsheet.md`(F1~F15), `audience.md`, `topic_brief.json`, `benchmark.md`, `appeal_and_contrast.md`
- 렌더러(v1): `02_script/render_full.py` · `full_overlay.html` · `build_full.py` · `full.json` · 샘플 `render_sample.py`
- 클립 목록(v1, 실사): `04_assets/clips.md`
