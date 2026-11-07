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

절차 (키를 저장하지 않는 방법, Claude 의 ElevenLabs 커넥터 또는 ElevenLabs 웹):
1. 대본 박자 문장을 장(chapter) 단위로 묶어 2~3덩어리(덩어리당 약 2,000자)로 만든다. 문장 사이는 빈 줄.
2. 덩어리마다 위 목소리로 음성 생성 → mp3 를 `03_voice/el/part1.mp3, part2.mp3 …` 로 받는다.
3. `python -m ytflow voice-import <프로젝트> 03_voice/el/part1.mp3 03_voice/el/part2.mp3`
   — faster-whisper 단어 시각 + 대본과 글자 단위 맞추기(difflib)로 박자 끝을 찾고, 그 근처 가장 긴 쉼에서 자른다.
   원래 초안 음성은 `03_voice/edge/` 로 옮겨 둔다. 자른 위치는 `03_voice/el/cuts.txt`.
4. `python -m ytflow hybrid <프로젝트>` — 새 음성 길이에 맞춰 장면·자막·효과음이 다시 맞춰진다.
점검: 박자별 받아쓰기와 대본의 일치율(스페인 독감 편 평균 97.3%), 시작·끝 글자가 맞는지.
비용: 약 1크레딧/글자, 기본 2테이크. 계정이 무료 등급이면 'Unusual activity … Free Tier disabled' 로 한 테이크가 실패할 수 있음(다른 테이크는 성공) — 유료 요금제면 사라짐.
