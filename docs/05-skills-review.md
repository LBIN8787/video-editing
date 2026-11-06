# 영상편집 skill 조사 (2026-11-06)

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
