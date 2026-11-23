# 넘기기 편 v3 인계 (2026-11-20)

## 지금 상태
| 단계 | 상태 |
|---|---|
| D1 주제 | 통과 — '권태사회'·넘기기 (`01_research/topic_card.md`) |
| 대본 | `02_script/script_v3.md`로 진행. 사용자 답변 "이대로 진행해줘"를 `02_script/script_review.md`에 기록했습니다. |
| 원화·사진 | Drive `ytflow/영상/20261120-curiosity-trend/art/`에 원화 5장, 16:9 JPG 20칸, 러셀 초상 1장. PC 사본과 Drive 사본의 해시가 일치합니다. |
| v3 검토본 | `05_edit/v3_art_review.mp4`(Drive). 38장면, 삽화 적용 19장면, 무음 마디 8개, 실제 사진 1장. 초안 목소리 기준 약 7분 29초, 1920×1080, 30fps, 배경음 없음. |
| 업로드 자료 | `05_edit/youtube.md`에 v3 챕터·출처를 반영했습니다. 썸네일 A/B/C는 Drive `05_edit/`에 있습니다. |
| 최종본·업로드 | 원화 적용본 확인 → 채널 ElevenLabs 목소리 → 최종 재렌더 및 챕터 갱신 → D4 사용자 승인 → ‘한겹 더 보면’ 일부 공개. |

## 소스와 프레임 확인

- Codex 내장 imagegen에 `02_script/art_orders.md`의 주문을 사용했습니다. 잼 편 `tasting.png`의 화풍을 참고했고, 첫날 밤 시트는 다음 시트에서 지우와 침실을 맞추는 데 썼습니다.
- 러셀 1894년 파일 요청이 제한되어 맥마스터대 기록관의 1893년 사진을 `art/russell.jpg`로 저장했습니다. [기록관 사진 목록](https://www.humanities.mcmaster.ca/~bertrand/youngbr.html) · [라이선스 기록](https://commons.wikimedia.org/wiki/File:Portrait_of_Bertrand_Russell_in_1893.jpg)
- 실험 영상의 개수와 조건은 색이 다른 재생 카드로 도식화했습니다. 사진과 모션그래픽 및 모든 삽화의 배치를 장면별 중간과 끝쪽 프레임에서 확인했습니다.

## 사용자가 정해 둔 것 (원문은 `manual/feedback.yaml`)
- 이야기를 들려주듯, 학습형 금지, 길이는 짧게 (v1 은 너무 김)
- 문제 → 왜 → 어떻게 극복으로 이어지게, 시청자가 "아 이래야겠구나"를 얻어 가게 (지우의 다음 날 밤: 묻기·머물기·나가기·챙기기)
- 실험은 결과 전에 '무엇을 묻는 실험인지' 먼저
- 배경음 없음
- 삽화는 잼 편처럼, 연출은 메모리 편처럼, 실제 자료가 있으면 넣기
- 출처 줄은 설명란으로 충분(화면은 선택), '자료 화면' 표시는 실사 스톡을 안 쓰면 거의 필요 없음
- 업로드는 앞으로 **구글 드라이브를 거쳐서** (원본 화질). 클라우드 Drive 커넥터는 한 번에 ~3MB 라 못 함 → PC 의 Drive for desktop(`YTFLOW_DRIVE`)에 원본을 두고 올리는 경로가 필요 (`ytflow/stages/ytpublish.py` 는 지금 GitHub Release 영상을 받음 — Release 는 100MB 아래로 다시 압축됨)

## 다시 렌더하고 업로드할 때

1. `02_script/build_v3.py`는 대본을 바꿨을 때 `v3.json`을 다시 만듭니다. 렌더러는 `ARTDIR`의 `<시트>_<칸>.jpg`와 `russell.jpg`를 실행할 때 읽습니다. 칸 이름은 `tl`, `tr`, `bl`, `br`입니다.
2. `python 02_script/render_v3.py <클립 폴더> <음성 폴더> none <작업 폴더> <출력 mp4>`를 실행합니다. 음성 이름은 `s<장면>_0.mp3`입니다. Windows에서 설치된 Chrome을 쓰려면 `YTFLOW_CHROMIUM`에 실행 파일 경로를 넣고, 로컬 Playwright가 설치된 `node_modules`를 `NODE_PATH`에 지정합니다.
3. 원화 적용 화면을 확인한 뒤 최종 음성은 `ch-knowledge`에 지정된 ElevenLabs Nobel Butler (`YBRudLRm83BV5Mazcr42`, `eleven_v4`)로 만듭니다. 출력 `timeline.json` 기준으로 최종 영상과 자막, `05_edit/youtube.md`의 챕터를, 현재 검토본과 같은 기준으로 다시 확인합니다.
4. D4 승인 뒤 최종 MP4를 Drive에 보관합니다. 업로드 대상은 ‘한겹 더 보면’, 상태는 `unlisted`, 기본 썸네일은 A입니다. `yt-publish --dry-run --via here --privacy unlisted`로 메타데이터를 점검할 수 있습니다. 실제 업로드 입력은 Drive에 보관한 최종 MP4와 동일한 원본을 사용합니다.

## 파일
- 대본: `02_script/script_v1.md`(기각) · `script_v2.md` · **`script_v3.md`**
- 조사: `01_research/factsheet.md`(F1~F15), `audience.md`, `topic_brief.json`
- 렌더러(v1): `02_script/render_full.py` · `full_overlay.html` · `build_full.py` · `full.json` · 샘플 `render_sample.py`
- 클립 목록(v1, 실사): `04_assets/clips.md`
