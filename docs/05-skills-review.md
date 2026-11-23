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
| **목소리** | ElevenLabs | `tts.backend: elevenlabs` 구현(캐시·글자별 시각). **영상 확정 후 목소리를 골라 적용** → `docs/08-voice.md` | 실제 생성·voice-import 로 운영 중 (docs/08) |

## 2차 조사: 지금 파이프라인에 맞는 후보
| 후보 | ★ / 라이선스 | 채우는 빈칸 | 판단 |
|---|---|---|---|
| [rough.js](https://github.com/rough-stuff/rough) | 21.3k / MIT | 손그림 도형(빗금 채우기·겹선)을 SVG 로. 시드 고정 시 같은 결과 | **다음 도입**: hyper.py 의 막대·상자·동그라미를 빗금 손그림으로 → 미주일기 질감 강화 |
| [hand-drawn-diagrams](https://skills.sh/nexu-io/open-design/hand-drawn-diagrams) (open-design) | 106k / Apache-2.0 (모음 저장소) | 글 → Excalidraw 손그림 도식 + 애니메이션 SVG | 시범 가치 있음: 복잡한 구조도(공급망·지배구조)를 손그림으로. 원본(upstream) 라이선스는 미확인 |
| [faster-whisper](https://github.com/SYSTRAN/faster-whisper) / [WhisperX](https://github.com/m-bain/whisperX) | 26.5k MIT / 25.1k BSD-2 | 단어 단위 시각: 원본 소스형(식스시그마)의 발언 구간 정밀 자르기, 원본 발언 자막 | **원본 소스형에 도입 권장** (사용자 PC rebuild 때 로컬 실행). video-use 의 유료 받아쓰기 대신 |
| [vibe-motion/sound](https://github.com/vibe-motion/sound) | 291 / 라이선스 표기 없음 | Freesound 효과음 검색·다운로드(펜 긋는 소리·종이 소리·팝) | 보류: 저장소 라이선스 표기가 없고 Freesound API 키(무료) 필요. 효과음 파일마다 라이선스 확인 필요 |
| 한국어 TTS: [MeloTTS](https://github.com/myshell-ai/MeloTTS)(MIT), CosyVoice(Apache-2.0) | 7.7k / MIT | 지금 쓰는 edge-tts 는 비공식 경로라 **수익 채널에서는 약관 위험** | 결정됨: 초안 edge, 공개 최종본 ElevenLabs (docs/08, AGENTS '목소리') |
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


## 2026-11-07 그래픽 팩 도구 조사
그래픽 팩(그림 + 겉모습)에 쓸 스킬·도구 조사 결과는 `docs/14-graphic-pack-tools.md`. 추천: HyperFrames 블록(설치됨) → theme-factory(Apache-2.0) → roughViz·chart.xkcd(MIT) → Phosphor(MIT) → 한글 OFL 글꼴 → Open Peeps·ambientCG(CC0).


## 2026-11-15 rea-video (레퍼런스 영상 역분석)
- **무엇:** `JuneYaooo/rea-video` (Apache-2.0, 커밋 `5b09832`). 영상 한 편을 장면(샷)마다 나눠 화면이 어떻게 만들어졌는지(실사·2D 애니메이션·코드 렌더·사진 밀기·정지 화면 등 11종), 위에 얹은 자막·글자·스티커, 효과음 위치, 편집 리듬을 정리해 `VIDEO.md`·`report.html`·`storyboard.jpg` 로 냄.
- **읽은 것:** SKILL.md, references/setup.md, 네트워크 호출(`util.py` 모델 내려받기, `vlm.py` 는 키가 있을 때만). 설치 스크립트는 pip/pipx 만 씀. 자동 유료 호출 없음(`remake-run` 은 쓰지 않음).
- **쓰는 법:** 영상 파일이 있어야 함. 클라우드는 YouTube 봇 확인으로 내려받기가 막히므로(우회하지 않음) 사용자가 받은 mp4 는 Google Drive(`%YTFLOW_DRIVE%\refs\`)에 두고, PC 에서 `rea-video decompose` 를 돌리거나 클라우드가 Drive 커넥터로 가져옴(2026-11-15~, docs/09 §0).
- **절차:** `decompose ref.mp4 -o out/ref --lang en` → `review out/ref` → 에이전트가 장면 그림을 보고 `review_answers.json` 작성 → `apply-review` → `VIDEO.md` 를 읽고 움직임 문법을 매뉴얼로.

## 2026-11-15 ego lite (사용자 PC 의 AI 에이전트용 브라우저)
- **무엇:** `citrolabs/ego-lite` (MIT, 커밋 `bacaece`, 스킬 `ego-browser` 2.2.0). 사용자의 로그인 상태를 가진 Chromium 브라우저를 에이전트가 별도 Space 에서 조종(열기·클릭·스냅샷·캡처). macOS·Windows 만, Linux(클라우드)는 미지원.
- **읽은 것:** README, `skills/ego-browser/SKILL.md`, `references/install*.md`, `scripts/install.sh`(macOS 전용, cdn.ego.app 에서 dmg 를 받음). 실제 사용법은 설치된 앱의 `ego-browser skill` 출력이 기준.
- **쓰는 곳:** `skills/ref-watch-ego` — 레퍼런스 영상을 내려받지 않고 사용자 브라우저에서 '정지 → 이동 → 찍기'로 캡처해 분석. youtube.com 영상 페이지만 열고, 쿠키를 다른 도구에 넘기지 않음.
- **주의:** 로그인된 브라우저라 계정 행동(구독·댓글·좋아요)을 하지 않도록 스킬에 명시. 첫 실행 때 크롬 데이터 가져오기는 사용자가 결정.

## 2026-11-23 last30days (최근 30일 커뮤니티·영상 반응 조사)
- **무엇:** `mvanhorn/last30days-skill` (MIT). v3.33.0(2026-11-09, 커밋 `7869eb1`)에 고정 — 최신 v4.6.0 은 이틀 된 판이라 2주 규칙으로 보류. 주제 하나를 최근 30일 Reddit·HN·YouTube(자막)·GitHub·dev.to·Polymarket 등에서 찾아 반응(추천·댓글·조회)으로 순위를 매김. 엔진은 Python 3.12+ 표준 라이브러리만(의존성 없음).
- **읽은 것:** SKILL.md, references/runtime.md·research-runbook.md, scripts 의 subprocess·네트워크 호스트 전부. `eval/exec` 없음.
- **설치:** `kind: "skill"` — 태그를 임시로 얕게 받아 `skills/last30days` 의 SKILL.md·agents·references·scripts 만 `.claude/skills`·`.agents/skills` 에 복사(데모 그림·음악 14MB 인 assets 는 뺌, `tools/` 에 본체 없음, .gitignore). `python scripts/install_tools.py`.
- **주의 1 — 설정 마법사를 돌리지 않음:** 첫 실행 마법사(`setup_wizard.py`)가 `npx -y` 로 전역 CLI(digg·printing-press 소스)를 **자동 설치**함. 대신 `~/.config/last30days/.env` 를 직접 씀: `SETUP_COMPLETE=true`, `FROM_BROWSER=off`, `REDDIT_SESSION_OFFERED=true`, `REDDIT_BROWSER_CONSENT=false`, `LAST30DAYS_MEMORY_DIR=`(빈 값 = 결과 파일 저장 끔, C 드라이브에 쌓이지 않게).
- **주의 2 — 쿠키·키 없이:** 브라우저 쿠키(X·Reddit 로그인) 읽기는 동의할 때만 동작하고 우리는 끔. ScrapeCreators·X·xAI 등 키는 넣지 않음 → 키 없는 소스만: Reddit 공개 JSON·HN·GitHub·dev.to·YouTube(yt-dlp)·Stocktwits·Polymarket.
- **주의 3 — 이 PC:** `yt-dlp.exe` 가 PATH 에 없어 YouTube 가 빠짐 → 실행할 때 `...\LocalCache\local-packages\Python313\Scripts` 를 PATH 에 더함. Polymarket 은 연결이 끊김(국내 접속 차단으로 보임).
- **쓰는 곳:** 주제 단서·반응 수집 (docs/61). 결과는 커뮤니티 글이라 **사실 출처가 아님** — 숫자·발언은 1차 출처로 다시 확인.

## 2026-11-23 영상 제작용 외부 스킬 묶음 (ElevenLabs·YouTube 분석·저널리즘 확인)
조사·선정 이유와 '언제 쓰나'는 `docs/62-external-skills-map.md`. 모두 `kind: "skill"` 로 커밋 고정(2주 이상 지난 판), 스킬 폴더만 복사.
- **elevenlabs/skills** (MIT, `9763c39` 2026-11-04): text-to-speech·speech-to-text·voice-isolator·music·sound-effects 만. SKILL.md 와 references 만 있고 스크립트 없음. 호출은 api.elevenlabs.io, `ELEVENLABS_API_KEY`. 키가 없을 때 안내하는 `npx -y @elevenlabs/cli@latest onboard init` 은 쓰지 않음.
- **AgriciDaniel/claude-youtube** (MIT, `84c3fa6` 2026-04-10): execution/*.py 를 읽음 — googleapis 만, scope `youtube.readonly`·`yt-analytics.readonly`(읽기 전용), 토큰은 스킬 폴더 tmp/. 설치 스크립트(install.ps1)는 git clone·복사뿐이지만 쓰지 않음. 설명(description)이 'video·script·hook' 에도 걸려 우리 스킬을 가로챌 수 있어, 설치 때 **분석·점검·경쟁·재활용 전용으로 좁힘**(`description_override`).
- **jamditis/claude-skills-journalism** (MIT, `e1f38cb` 2026-11-04): fact-check-workflow·source-verification·social-media-intelligence·data-journalism 만. 지침 문서뿐(스크립트 없음), 외부 자료를 '믿지 않는 데이터'로 다루는 규칙이 들어 있음.
- **보류:** Remotion 공식 스킬, Manim 스킬, YouTube Clipper, Anthropic 디자인 스킬 (이유는 docs/62 §4).
