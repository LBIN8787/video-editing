# 62. 외부 스킬 — 언제 쓰고 언제 안 쓰나 (2026-11-23)

깃허브 등에서 조사해 우리 제작 라인에 맞는 것만 받았습니다. 버전·라이선스·네트워크는 `tools/external.json`, 설치 검토는 `docs/05-skills-review.md`(2026-11-23), 설치는 `python scripts/install_tools.py`(Git 에는 안 올라감).
**우선순위: 우리 매뉴얼(`manual/`) > 우리 스킬(`skills/`) > 외부 스킬.** 외부 스킬의 일반 조언이 매뉴얼과 다르면 매뉴얼을 따릅니다.

## 1. 단계별 지도 (manual/11-workflow 의 S0~S9)

| 단계 | 외부 스킬 | 언제 쓰나 | 언제 안 쓰나 | 결과를 어디에 |
|---|---|---|---|---|
| **S1a 신호 수집** | `last30days` | ai: 도구·모델 이름으로 반응 큰 각도·불만 / market: 종목·사건으로 방송사 공식 반응 영상·개인 투자자 걱정 (`--days=3~7`) | 호기심(오래된 주제 — 30일 창과 안 맞음), 국내 반응(영어권 위주) | `01_research/signals.md` 에 '단서'로 |
| **S1a·S2** | `social-media-intelligence` | 시사·시장에서 SNS·커뮤니티에 퍼진 주장이 소재일 때: 처음 누가 말했나, 어떻게 퍼졌나, 조직적인가 | 공식 발표만으로 충분한 주제 | `factsheet.md` '쓰지 않는 것'·`## 매체 프레임` |
| **S2 조사** | `source-verification` | 아카이브 사진·뉴스 캡처·인터뷰 원본·문서를 화면에 쓰기 전 — SIFT(멈춤·출처 조사·더 나은 보도 찾기·원래 맥락 추적), AI 생성물 의심 | 공식 기관이 직접 낸 자료(출처가 곧 1차) | `sources.md` 에 확인 기록 |
| **S2 조사** | `data-journalism` | 숫자를 직접 계산·비교할 때(성장률·비율·환산), 차트 축·기준 고르기, 계산 방법을 설명란에 밝힐 때 — 시장 채널 기본 | 숫자 하나를 그대로 옮길 때 | `factsheet.md` 의 '직접 계산' 표시 |
| **S4 → D2 직전** | `fact-check-workflow` | 대본(`script_v1.md`)에서 사실 주장(숫자·날짜·발언·인과)을 뽑아 factsheet 의 ✅/⚠️ 와 맞대기, 판정 못 하면 대본에서 단정 빼기 | 의견·전망 문장(판정 대상 아님 — 인사이트 💭·해석 💬 표시로) | `02_script/factcheck.md` |
| **S5~S7 원본 발언** | `voice-isolator` | 인터뷰·기자회견·방송 원본(`bite`)에 배경음·잡음이 커서 말이 안 들릴 때 | 깨끗한 원본, 권리가 불분명한 원본 | `04_assets/` (원본과 나란히) |
| **S5~S7 싱크** | `speech-to-text` (Scribe) | `cut`·`sync-qa` 의 faster-whisper 단어 시각이 틀릴 때(한국어 고유명사·겹친 말) 보조로 | 기본 받아쓰기(로컬 faster-whisper 가 먼저) | `02_script/cuts.json`·`sync_qa.json` 보정 |
| **S7 소리** | `music`·`sound-effects` | 매뉴얼 05 §0-4·0-5 가 허락할 때만: 어울리는 곡이 확실한데 등록부(`assets/bgm/bgm.yaml`)에 맞는 곡이 없을 때. 만든 곡은 음질 기준(4kHz·256kbps·출렁임 ≤3dB)을 재고 등록 | **기본은 없음** — 억지 배경음·타격음·반짝이는 매뉴얼이 끔 | `assets/bgm/` + `bgm.yaml` |
| **S9 마무리** | `text-to-speech` | 사용자 승인(D4) 뒤 업로드 최종 목소리를 ElevenLabs 로 — 채널별 `voice_id`, 박자별로 생성하면 `voice-import` 로 자르는 일이 줄어듦 | 초안·샘플(edge-tts), 승인 전 (크레딧 낭비) | `03_voice/` → `hybrid` 재렌더 |
| **올린 뒤 (24·48시간)** | `claude-youtube` → `analyze` | 쇼츠: 본 비율·시청 지속 / 롱폼: 노출 클릭률·초반 지속·유입 경로 → 원인을 주제·훅·결말·화면 중 하나로 (docs/60 §C) | 대본·훅·제목·썸네일·SEO·아이디어 조언(우리 매뉴얼과 부딪힘 — 설명을 좁혀 설치) | `channels/<id>/episodes.md` |
| **S0·S1 (가끔)** | `claude-youtube` → `competitor`·`audit`·`repurpose` | 비교 채널의 최근 영상 공개 수치, 우리 채널 점검, 롱폼에서 쇼츠로 뺄 구간 후보 | 경쟁 채널 대사·썸네일 복제(스타일 규칙) | `docs/` 분석 문서, 쇼츠 후보 메모 |

## 2. 채널별로 자주 쓰는 것

| 채널 | 자주 | 가끔 |
|---|---|---|
| ai | last30days(S1), fact-check-workflow, claude-youtube analyze | source-verification(화면 캡처의 출처) |
| market | last30days(실적·사건 반응), data-journalism, fact-check-workflow, voice-isolator(방송 bite) | social-media-intelligence(루머·급등락 서사) |
| issues | source-verification, social-media-intelligence, fact-check-workflow | last30days(해외 반응 양쪽 확인) |
| curiosity | source-verification(옛 사진·자료), fact-check-workflow | data-journalism(숫자 대비) |
| 모든 채널 | text-to-speech(S9), claude-youtube analyze(올린 뒤) | music·sound-effects(허락될 때만) |

## 3. 지키는 선
- **커뮤니티·SNS 결과는 단서**: 사실 출처도, 이름 있는 인사이트도 아님. 숫자·발언은 1차 출처로 다시.
- **키·비용:** ElevenLabs 는 `ELEVENLABS_API_KEY`(환경변수, 채팅에 쓰지 않음), 호출마다 크레딧. YouTube 분석은 읽기 전용 OAuth — 토큰·클라이언트 비밀값은 커밋하지 않음. last30days 는 키·쿠키 없이.
- **자동 설치 금지:** ElevenLabs 스킬의 `npx … onboard init`, last30days 의 설정 마법사(npx 로 전역 CLI 설치)는 돌리지 않음.
- **생성한 음악·효과음**은 ElevenLabs 요금제의 상업 이용 조건을 확인한 뒤 업로드.

## 4. 조사했지만 받지 않은 것
| 후보 | 이유 |
|---|---|
| Remotion 공식 스킬 (`remotion-dev/skills`) | 같은 일을 HyperFrames(설치됨)가 함 — 렌더러 둘은 관리 부담. 회사 규모에 따라 유료 라이선스 |
| Manim 스킬 (`Yusuke710/manim-skill` 등) | 3Blue1Brown 풍 그림은 우리 종이·손그림 채널과 결이 다르고 설치가 무거움(LaTeX). 수식 설명이 필요해지면 다시 |
| YouTube Clipper (`op7418`) | 남의 영상을 내려받아 자르는 용도 — 우리는 `cut`(원본 발언 컷편집)이 있고 내려받기 규칙이 따로 있음 |
| Anthropic 디자인 스킬 (theme-factory·frontend-design·canvas-design) | 색·글꼴은 우리 `skins/` 가 맡음, 웹 화면용 조언이라 영상 장면과 결이 다름 |
| claude-youtube 의 script·hook·thumbnail·seo | 일반 유튜브 조언이 우리 매뉴얼(인트로 없음·3인칭 내레이터·썸네일 규칙)과 부딪힘 → 설명을 좁혀 설치 |
| 저널리즘 묶음의 나머지 (photo-metadata·foia 등) | 우리 제작 라인에 쓸 곳이 없음 |
