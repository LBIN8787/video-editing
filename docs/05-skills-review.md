# 영상편집 skill 조사 (2026-11-06)

## 도입 현황 (2026-11-06 2차)
| 도구 | 버전 고정 | 어디에 쓰나 | 설치 |
|---|---|---|---|
| HyperFrames | `hyperframes@0.8.190` (10/23 릴리스), `gsap@3.13.0` | `ytflow/stages/hyper.py`: 미주일기 카드(text·number_compare·analogy·flow·table·bars·headline)를 HTML+GSAP 로 렌더. 펜으로 그려지는 선, 숫자 카운트업, 형광펜. 렌더 전 `hyperframes check` 로 레이아웃·대비 점검 | `python scripts/install_tools.py` |
| ffmpeg-skill | commit `2d9f5ac` (v2.12.0, 10/23) | `ytflow/stages/finish.py`: assemble 뒤 유튜브 음량 −14 LUFS 마스터링(final.mp4), 유튜브 규격 점검(delivery_check.json), 프레임 시트(final_sheet.png) | 같은 스크립트 |

- 목록과 버전: `tools/external.json`. 도구 본체(`tools/<이름>/`)와 그 skill 복사본은 저장소에 올리지 않습니다.
- agent skill(`hyperframes`, `hyperframes-cli`, `hyperframes-registry`, `media-use`, `ffmpeg-skill`)은 `.claude/skills/`·`.agents/skills/` 에 들어가 Claude Code·Codex 가 같이 씁니다.
- HyperFrames 사용 통계는 끕니다(`HYPERFRAMES_NO_TELEMETRY=1`). 설치 스크립트는 `npm --ignore-scripts` 로 설치 단계 스크립트를 실행하지 않습니다.
- 미주일기 스타일은 `card_engine: hyperframes` 가 기본입니다. 도구가 없거나 렌더가 실패하면 기존 `paper.py` 로 자동 대체합니다.
- 렌더 속도: 카드 1장 약 25초(이 환경은 GPU 없음, 소프트웨어 렌더) → 3개씩 병렬.

## 3차 도입 (2026-11-06)
| 항목 | 고정 버전·라이선스 | 어디에 | 확인한 것 |
|---|---|---|---|
| **rough.js** | `roughjs@4.6.6` (2023-11), MIT | `ytflow/stages/hyper.py` + `ytflow/assets/rough_paths.mjs`: 미주일기 카드의 밑줄·상자·동그라미·화살표를 rough.js 손그림 선으로, **막대는 빗금 채우기**, 강조 상자는 옅은 빗금. 시드 고정 → 같은 카드는 늘 같은 그림. 경로는 카드를 만들 때 node 로 미리 계산해 HTML 에 그대로 넣음(HyperFrames 계약 준수) | 숫자 카드·흐름도·막대 렌더 확인, `hyperframes check` 문제 0 |
| **faster-whisper** | `faster-whisper==1.2.1`, MIT | `ytflow/stages/align.py`: 원본 발언(quote) 클립을 앞뒤 3초 여유로 받은 뒤 **단어 단위 받아쓰기 → 대본 quote_en 과 가장 잘 맞는 구간만 남기고 다시 자름**. 오디오는 ffmpeg 로 직접 읽어 PyAV 버전 문제를 피함 | 11.6초 시험 클립에서 해당 발언 3.9초만 정확히 잘라냄(일치도 1.00, CPU 약 6초) |
| WhisperX | (선택) BSD-2 | 음소 단위가 더 필요할 때 `align.engine` 확장 예정. torch 가 필요해 기본 설치에서 뺌 | — |
| **hand-drawn-diagrams** (시범) | commit `c8ffd6c`, MIT (원본 muthuishere) | 에이전트 skill 로 설치(`.claude/skills`, `.agents/skills`). 복잡한 구조도(공급망·지배구조)를 Excalidraw 손그림으로 그려 PNG 를 `04_assets/scene_XXX_shot.png` 로 넣고 rebuild → 미주일기 종이 콜라주로 들어감 | ⚠ 렌더 스크립트가 **스스로 `uv run playwright install chromium` 으로 브라우저를 내려받음** → PC 에서만 렌더. 편집 링크는 작성자 GitHub Pages 주소에 그림 데이터를 URL 로 실어 엶(서버 업로드 아님) |
| 효과음 skill (vibe-motion/sound) | — | **보류 유지**: 저장소에 LICENSE 파일이 없음(=사용 허락 없음). Freesound API 키 필요. ElevenLabs 를 쓰게 되면 ElevenLabs 효과음 생성 API 가 대안 | |
| **목소리** | ElevenLabs | `tts.backend: elevenlabs` 구현(캐시·글자별 시각). **영상 확정 후 목소리를 골라 적용** → `docs/08-voice.md` | 가짜 응답으로 요청 형식·캐시 확인(실제 호출 안 함) |

## 2차 조사: 지금 파이프라인에 맞는 후보
| 후보 | ★ / 라이선스 | 채우는 빈칸 | 판단 |
|---|---|---|---|
| [rough.js](https://github.com/rough-stuff/rough) | 21.3k / MIT | 손그림 도형(빗금 채우기·겹선)을 SVG 로. 시드 고정 시 같은 결과 | **다음 도입**: hyper.py 의 막대·상자·동그라미를 빗금 손그림으로 → 미주일기 질감 강화 |
| [hand-drawn-diagrams](https://skills.sh/nexu-io/open-design/hand-drawn-diagrams) (open-design) | 106k / Apache-2.0 (모음 저장소) | 글 → Excalidraw 손그림 도식 + 애니메이션 SVG | 시범 가치 있음: 복잡한 구조도(공급망·지배구조)를 손그림으로. 원본(upstream) 라이선스는 미확인 |
| [faster-whisper](https://github.com/SYSTRAN/faster-whisper) / [WhisperX](https://github.com/m-bain/whisperX) | 26.5k MIT / 25.1k BSD-2 | 단어 단위 시각: 원본 소스형(식스시그마)의 발언 구간 정밀 자르기, 원본 발언 자막 | **원본 소스형에 도입 권장** (사용자 PC rebuild 때 로컬 실행). video-use 의 유료 받아쓰기 대신 |
| [vibe-motion/sound](https://github.com/vibe-motion/sound) | 291 / 라이선스 표기 없음 | Freesound 효과음 검색·다운로드(펜 긋는 소리·종이 소리·팝) | 보류: 저장소 라이선스 표기가 없고 Freesound API 키(무료) 필요. 효과음 파일마다 라이선스 확인 필요 |
| 한국어 TTS: [MeloTTS](https://github.com/myshell-ai/MeloTTS)(MIT), CosyVoice(Apache-2.0) | 7.7k / MIT | 지금 쓰는 edge-tts 는 비공식 경로라 **수익 채널에서는 약관 위험** | 운영 전 결정 필요: ① 본인 녹음(manual) ② Azure 공식 TTS(유료, 저렴) ③ 오픈 모델(품질 시험 필요) |
| vidIQ (이 세션에 연결된 커넥터) | — | 제목 점수·썸네일 생성·키워드·경쟁 채널 분석 | 업로드 패키지 단계에 활용 가능 (크레딧 차감) |
| 썸네일 skill (ez-thumb, claude-thumbnails 등) | 수십 개 / Gemini 유료 | 썸네일 생성 | 보류: 대부분 유료 이미지 API 필요, 검증된 것이 적음 |
| HyperFrames registry (약 450 블록) | 위와 같음 | 전환 효과·차트·키네틱 타이포 | 시범: `hyperframes add` 로 장 전환 블록 1~2개 |

에이전트(Claude Code·Codex)용으로 공개된 영상편집 skill 중 ytflow 에 도입할 만한 것을 검토했습니다.
별 수·라이선스·최근 업데이트는 GitHub 검색 API 기준(2026-11-06)이고, 기능은 각 README 기준입니다.

## 요약
| skill | ★ | 라이선스 | 유료 키 | ytflow 에 주는 것 | 판단 |
|---|---|---|---|---|---|
| [HyperFrames](https://github.com/heygen-com/hyperframes) (HeyGen) | 79.8k | Apache-2.0 | 없음 | HTML/CSS/GSAP 애니메이션 → MP4. 차트 블록, 셰이더 전환, 키네틱 자막 | **도입 1순위 (시범)** |
| [ffmpeg-skill](https://github.com/kajisho5/ffmpeg-skill) | 4.6k | MIT | 없음 | 음량 −14 LUFS, 배경음 자동 낮춤(ducking), 단어별 강조 자막, 9:16 재구성, 한글 자막 폰트 | **도입 2순위 (부분)** |
| [video-use](https://github.com/browser-use/video-use) (browser-use) | 30.6k | MIT | ElevenLabs 필요 | 긴 원본 영상을 받아쓰기 기반으로 자르기(군더더기 말·공백 제거), 단어 단위 자막 | 방식만 차용 |
| [Remotion skills](https://github.com/remotion-dev/skills) | 6.4k | (Remotion 자체 라이선스) | 없음 | React 로 모션 그래픽 | 보류 |
| [claude-code-video-toolkit](https://github.com/digitalsamba/claude-code-video-toolkit) | 2.5k | MIT | 일부 ElevenLabs | Remotion 템플릿·차트·전환·효과음·음악 생성 | 보류 |
| [video-editor-skills](https://github.com/appariciojunior/video-editor-skills) | 0.4k | CC BY-NC (비상업) | — | DaVinci Resolve 편집 | 제외 |

## 1. HyperFrames — 도입 1순위 (인포그래픽형 렌더러 후보)
- **무엇:** HTML·CSS·미디어·애니메이션(GSAP, Lottie, Three.js)을 프레임 단위로 그려 MP4 로 만드는 오픈소스 프레임워크와 agent skill.
- **왜 유용한가:**
  - 지금 렌더러(`paper.py`·`flat.py`)는 PIL 로 한 프레임씩 그립니다. 화면 배치·글자 겹침 방지를 직접 계산해야 합니다.
    HTML 은 레이아웃(flex·grid), 한글 웹폰트, 글자 줄바꿈을 브라우저가 처리하므로 **겹침이 구조적으로 줄고**, 움직임 표현(GSAP 이징, 셰이더 전환)이 훨씬 풍부합니다.
  - `data-chart`(움직이는 차트) 같은 블록과 전환 효과 목록이 있어 **"시각적으로 계속 보기엔 부족하다"** 는 문제에 직접 도움이 됩니다.
  - Apache-2.0 이라 **수익 채널에서 써도 렌더 비용이나 상업 사용 제한이 없습니다.**
- **요구 사항:** Node.js 22+, FFmpeg, 헤드리스 Chrome. 이 환경(Node 22.23, FFmpeg 6.1, Playwright Chromium)에서 충족.
- **설치:** `npx skills add heygen-com/hyperframes`, 또는 Claude Code 플러그인 `heygen-com/hyperframes`.
- **도입안:** 카드 JSON(scenes.json 의 card)을 HTML 템플릿으로 바꾸는 `html` 렌더러를 추가하고, 머니크루 스타일로 같은 대본을 두 렌더러로 뽑아 비교 → 나으면 인포그래픽형 기본값으로.
- **확인 필요:** README 에 한글(CJK) 자막 언급은 없습니다. 웹폰트로 해결될 것으로 보이지만 시범에서 확인합니다.

## 2. ffmpeg-skill — 도입 2순위 (마무리 공정)
- **무엇:** ffmpeg 기반 도구 42개 + MCP 서버. 자르기·잇기·공백 제거·자막·음량·플랫폼별 내보내기. 클라우드·API 키 없음.
- **ytflow 에 비어 있는 것을 채움:**
  - **음량:** 유튜브 기준 −14 LUFS / −1 dBTP 정규화 (지금은 TTS 만 −16 으로 맞춤).
  - **배경음 자동 낮춤(ducking):** 내레이션이 나올 때 BGM 을 낮춤 → 레퍼런스 3채널 모두 BGM 이 깔려 있음.
  - **단어별 강조 자막(karaoke·pop):** 쇼츠에서 아직 못 한 '단어 튀어나오는 자막'.
  - **9:16 재구성:** 본편 장면을 쇼츠로 재활용할 때.
  - 한글 자막 폰트 자동 선택(README 요약 기준).
- **도입안:** 스킬로 설치해 에이전트가 쓰게 하고, ytflow 의 assemble 단계에는 음량·ducking 설정만 같은 값으로 옮겨 넣습니다(의존성을 늘리지 않음).

## 3. video-use — 방식만 차용 (원본 소스형)
- **무엇:** 원본 촬영본을 넣으면 받아쓰기(ElevenLabs Scribe, 단어 단위 시각) → 군더더기 말·공백을 잘라 내고 → 색 보정·자막·오버레이까지 하는 skill.
- **원본 소스형(식스시그마)에 맞는 부분:** 1시간짜리 실적발표·인터뷰에서 **발언 구간을 단어 단위로 정확히 잘라 내는 것**. 지금은 YouTube 자막 시각으로 자르므로 앞뒤가 몇 초 어긋날 수 있습니다.
- **걸리는 점:** ElevenLabs API 키(유료)가 필요합니다.
- **도입안:** 같은 일을 로컬 받아쓰기(faster-whisper)로 하는 `quote_trim` 단계를 ytflow 에 추가 (사용자 PC 에서 rebuild 할 때 실행).

## 4. 보류·제외
- **Remotion skills / claude-code-video-toolkit:** 기능은 HyperFrames 와 겹칩니다. Remotion 은 자체 라이선스(일정 규모 이상 회사는 유료 라이선스로 알려져 있으나, 이 세션에서 라이선스 페이지를 열지 못해 확인하지 못함)라 HyperFrames 를 먼저 씁니다.
- **video-editor-skills:** 비상업 라이선스(CC BY-NC)라 수익 채널에 쓸 수 없고, DaVinci Resolve 가 필요합니다.

## 설치 전 주의
타사 skill 은 설치 전에 SKILL.md 와 스크립트를 읽어 봅니다(에이전트가 실행할 명령이 들어 있음). 설치는 `.claude/skills/`(프로젝트) 단위로 하고 `skills/` 원본과 섞지 않습니다.
