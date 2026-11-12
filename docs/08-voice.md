# 08. 목소리 (TTS) — ElevenLabs 로 정함, 영상 확정 후 적용

## 결정 (2026-11-06)
- **운영 목소리는 ElevenLabs** 로 합니다.
- **언제:** 영상의 형식·편집이 마음에 들어 확정된 뒤에 목소리를 고릅니다. 그 전까지 초안은 지금처럼 `edge`(무료)로 만듭니다.
- **주의:** `edge-tts` 는 마이크로소프트 엣지 읽어 주기의 비공식 경로입니다. **수익 채널에 올리는 최종본은 ElevenLabs(또는 본인 녹음)로** 다시 만듭니다.

## 목소리 고르는 순서
1. ElevenLabs 계정에서 API 키를 만듭니다(Profile → API Keys).
2. 키 넣기 — 채팅에 붙여 넣지 않습니다.
   - **PC:** 환경변수 `ELEVENLABS_API_KEY`
   - **클라우드 세션:** 환경 설정의 네트워크 비밀값(호스트 `api.elevenlabs.io`, 헤더 `xi-api-key`)에 저장하면 프록시가 붙여 줍니다.
3. 목소리 후보 듣기 (Voice Library 의 한국어 목소리 또는 직접 만든 목소리의 ID):
   ```bash
   python -m ytflow voice-sample --voice-id <ID>            # .cache/voice_samples/<ID>.mp3
   python -m ytflow voice-sample --voice-id <ID> --text "들어 볼 문장"
   ```
4. 채널마다 목소리를 정해 `channels/<id>/channel.yaml` 맨 아래 `tts` 주석을 풀고 `voice_id` 를 채웁니다.
   (모든 채널 공통이면 `config/pipeline.yaml` 의 `tts.backend: elevenlabs`, `tts.elevenlabs.voice_id`)
5. 이미 만든 영상에 목소리만 바꿔 입히기: `03_voice/scene_*.mp3` 를 지우고
   ```bash
   python -m ytflow stage <프로젝트> voice && python -m ytflow stage <프로젝트> assets && \
   python -m ytflow stage <프로젝트> subtitles && python -m ytflow stage <프로젝트> assemble
   ```
   (장면 길이가 바뀌므로 화면·자막도 다시 맞춥니다)

## 설정 (`tts.elevenlabs`)
| 키 | 기본 | 뜻 |
|---|---|---|
| `voice_id` | (빈칸) | 목소리 ID. 비어 있으면 elevenlabs 백엔드는 멈추고 안내를 띄움 |
| `model_id` | `eleven_multilingual_v2` | 한국어 품질 우선. 빠른 초안은 `eleven_flash_v2_5` |
| `language_code` | `ko` | |
| `stability` / `similarity_boost` / `style` / `speed` | 0.5 / 0.75 / 0.0 / 1.0 | 해설 채널은 안정성 0.5 안팎, 속도 1.0~1.1 |

## 동작 (`ytflow/stages/media.py` 의 `_elevenlabs`)
- `with-timestamps` 엔드포인트로 받아 **글자별 시작·끝 시각**을 `03_voice/scene_XXX.align.json` 에 저장합니다(단어 단위 자막·쇼츠 단어 팝 자막에 쓸 수 있음).
- 같은 문장·목소리·설정이면 `.cache/elevenlabs/` 캐시를 씁니다 → 다시 돌려도 크레딧을 또 쓰지 않습니다.
- 크레딧 감: 한국어 10분 롱폼 ≈ 2,800~3,300자 ≈ 같은 수의 크레딧(모델·요금제에 따라 다름 — ElevenLabs 요금 페이지 확인).


## 2026-11-07 확정 — API 키 없이 ElevenLabs 목소리 입히기
| 채널 | 목소리 | voice_id | 모델 |
|---|---|---|---|
| ch-knowledge (교양·역사) | Nobel Butler — 부드러운 중년 남성 중저음, 다큐·연구 해설 | `YBRudLRm83BV5Mazcr42` | eleven_v4 |
| ch-source-brief / 하이브리드 경제 | Hyun Bin — 차분하고 절제된 남성, 보고서 해설 | `s07IwTCOrCDCaETjUVjx` | eleven_v4 |
| ch-issues (시사, 2026-11-10 시험) | Mina — 또렷·따뜻·차분한 여성, 친근하고 신뢰감 있는 대화체 (MC 톤, 다른 채널과 성별로 구분) | `aiUUgjHa4mpHf6UenZuf` | eleven_v4 |

절차 (키를 저장하지 않는 방법, Claude 의 ElevenLabs 커넥터 또는 ElevenLabs 웹):
1. 대본 박자 문장을 장(chapter) 단위로 묶어 2~3덩어리(덩어리당 약 2,000자)로 만든다. 문장 사이는 빈 줄.
2. 덩어리마다 위 목소리로 음성 생성 → mp3 를 `03_voice/el/part1.mp3, part2.mp3 …` 로 받는다.
3. `python -m ytflow voice-import <프로젝트> 03_voice/el/part1.mp3 03_voice/el/part2.mp3`
   — faster-whisper 단어 시각 + 대본과 글자 단위 맞추기(difflib)로 박자 끝을 찾고, 그 근처 가장 긴 쉼에서 자른다.
   원래 초안 음성은 `03_voice/edge/` 로 옮겨 둔다. 자른 위치는 `03_voice/el/cuts.txt`.
4. `python -m ytflow hybrid <프로젝트>` — 새 음성 길이에 맞춰 장면·자막·효과음이 다시 맞춰진다.
점검: 박자별 받아쓰기와 대본의 일치율(스페인 독감 편 평균 97.3%), 시작·끝 글자가 맞는지.
비용: 약 1크레딧/글자, 기본 2테이크. 계정이 무료 등급이면 'Unusual activity … Free Tier disabled' 로 한 테이크가 실패할 수 있음(다른 테이크는 성공) — 유료 요금제면 사라짐.

### 2026-11-10 — voice-import 숨소리 문제
ElevenLabs 음성은 박자 앞에 숨소리(약 -40dB)가 있어 -45dB 기준으로 자르면 자막이 말보다 최대 1.2초 먼저 뜸 → `voice_import` 자르기 기준을 -38dB 로 올림(싱크 0.3초 안 64% → 94%).
또 박자별 `hb_*.txt`(대사 표시)를 함께 써서, 렌더가 가져온 음성을 대사에 맞는 것으로 알고 그대로 씀. 싱크 점검은 배경음이 섞이기 전 내레이션(`hb_work/voice.wav`)으로 잼.

## 2026-11-13 — 이어 읽는 시장(ch-market-daily) 목소리 결정: **Jaewon** (`QFEOldNoV2d2Bz0I3JNy`), 예비 Jun Lee (`VpI9YrC8mqZsi3NvIQzK`)

### 기준 (채널이 하는 일에서)
| 기준 | 왜 | 재는 법 |
|---|---|---|
| 숫자·영문을 정확히 | 한 편에 지수·%·소수점·조/억·S&P·티커가 20~40개 | 같은 시황 문장을 읽혀 받아쓰기 → 숫자 일치 |
| 아침 앵커 톤 (권위 + 담백) | 1차 출처·사실/해석 구분이 약속 — 들뜬 유튜버 톤은 신뢰를 깎음 | 설명·미리 듣기 |
| 6~8분 매일 들어도 피곤하지 않음 | 1일 1편, 같은 사람이 매일 듣는 채널 | 음높이 폭(너무 크면 연기 톤), 쉼 비율 |
| 다른 채널과 다른 목소리 | 시사=Mina(여성), 하이브리드 경제=Hyun Bin(차분한 남성), 교양=Nobel Butler | 겹치지 않게 |

### 후보 (ElevenLabs 라이브러리 한국어 · '뉴스/금융 브리핑' 설명)
| 목소리 | 설명 | 판단 |
|---|---|---|
| **Jaewon** | "news bulletins, financial briefings, analytical commentary" — 중간 음역, 절제된 진행 | **채택** — 같은 문장 시험 통과 |
| Jun Lee | 밝은 서울 억양, 미리 듣기 자체가 '오늘의 시장 브리핑' (S&P·나스닥·국채 금리) | **예비** — 같은 문장 시험은 생성 혼잡으로 못 함 |
| JaeGyu | 낮고 차분, "숫자·용어 발음 명확" | 크레딧 소진으로 시험 못 함 — 심층편 후보 |
| Emily | 30대 여성, 금융 뉴스 | 시사 채널(Mina)과 성별 겹침 |
| Gihong | 빠른 MZ 뉴스 톤 | 쇼츠용 — 롱폼 아침 시황엔 가벼움 |
| Hyun Bin | 기존 하이브리드 경제 목소리 | 채널 구분을 위해 제외 |

### 같은 문장 시험 (2026-11-13, eleven_v4, 2테이크, 384 크레딧)
문장: 고정 오프닝 + S&P·나스닥 %, 엔비디아 4.34%, 코스피 5,342.73, 네이버 3조 4,724억 원, "여기서부터는 해석입니다".
| | 길이 | 숫자 정확 | 빠뜨림 | 쉼 비율 | 음높이 폭(10~90%) |
|---|---|---|---|---|---|
| Jaewon 테이크 1 | 29.8초 | 10/10 | 없음 | 0.02 | 10.9 반음 |
| Jaewon 테이크 2 | 29.6초 | 10/10 | **"이어 읽는," 반복 한 번 빠짐** | 0.01 | 10.1 반음 |
| edge 초안 (InJoon +8%) | 34.3초 | 10/10 | 없음 | 0.22 | 19.7 반음 |
→ 숫자는 모두 정확, 억양 폭이 edge 의 절반(담백한 앵커 톤), 같은 글을 4.5초 빨리 읽음(쉼이 적음 → 렌더의 박자 쉼 0.28초가 숨 쉴 곳이 됨).
→ **반복 구절은 빠뜨릴 수 있다**: 고정 오프닝 "이어 읽는, 이어 읽는 시장"처럼 같은 말이 붙으면 테이크마다 확인. `voice-import` 가 박자별 일치율을 재므로 빠진 테이크는 거기서 걸러진다 (일치율 95% 미만 박자 → 다른 테이크).

### 운영
- 설정: `channels/ch-market-daily/channel.yaml` 의 `tts` (eleven_v4, stability 0.55, speed 1.0).
- **크레딧:** 한국어 1글자 ≈ 0.83 크레딧(이번 시험 실측 192/232자). 한 편 2,500~3,300자 → 테이크 1개 ≈ 2,100~2,800, 매일이면 **월 7만~9만 크레딧**. 지금 계정 한도는 월 1만(2026-11-13 소진)이라 매일 운영은 불가 → 월 10만 크레딧 이상 요금제가 필요. 무료 등급은 상업 이용(수익 채널)에 쓸 수 없으니 요금제 조건을 ElevenLabs 요금 페이지에서 확인.
- **자동 제작(매일 06:05)**: 키가 없으면 edge 초안으로 만든다. 자동으로 ElevenLabs 를 쓰려면 이 환경에 `api.elevenlabs.io` 키를 네트워크 비밀값(헤더 `xi-api-key`)으로 저장하고 `config/pipeline.yaml` → `tts.backend: elevenlabs`.
- 같은 문장 재시험(크레딧 충전 뒤): Jun Lee·JaeGyu 를 같은 문장으로 읽혀 위 표에 추가.
