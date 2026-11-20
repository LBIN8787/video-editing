# 53. 구성요소·스타일 목록에 더할 레퍼런스 + 비슷하게 모아 둔 스킬·카탈로그 (2026-11-20)

> 사용자: "영상 구성요소 · 스타일 목록 에 추가할만한 레퍼런스 자료들을 조사해줘" / "이런 비슷한 방식으로 모아둔 스킬이나 내용들이 또 있지 않아? 이런거도 조사해줘"
>
> 대상 목록: `styles/components.yaml`(카테고리 8개) · `styles/looks.yaml`(화면 화풍 13·삽화 8·실사 색보정 3) · `styles/techniques.yaml`(연출 기법 26) · `assets/bgm/bgm.yaml`(7).
> 조사(§1~5) 뒤 사용자 결정으로 §5-1·5-2·5-3 을 진행했습니다 — 결과는 §6.

## 0. 무엇을 어떻게 확인했나 (정직하게)
- 웹 검색과 페이지 읽기(2026-11-20). 저장소 README·PyPI 페이지까지 읽었고, **각 저장소의 코드·라이선스 파일을 하나하나 열어 보지는 않았습니다.** 라이선스 칸의 "README 표기"는 목록 페이지에 적힌 값입니다. 쓰기 전에 원문 LICENSE 를 다시 확인합니다(`tools/external.json` 규칙).
- `zhuyansen/awesome-claude-video-skills` 는 페이지가 길어 뒷부분을 다 읽지 못했습니다. 그 목록에서 온 항목 중 **(미확인)** 표시가 있는 것은 이름·설명만 확인한 것입니다.
- 별(★) 수는 조사 당일 값이며 바뀝니다.

## 1. 가장 먼저: 이미 설치돼 있는데 목록에 안 옮긴 것 — HyperFrames registry
`tools/external.json` 에 **hyperframes@0.8.190 과 `skills/hyperframes-registry`·`skills/media-use` 가 이미 고정**돼 있습니다. 그런데 우리 구성요소 목록에는 이 registry 의 블록이 연결돼 있지 않습니다.

| 무엇 | 내용 | 우리 카테고리 | 라이선스 |
|---|---|---|---|
| [HyperFrames registry](https://github.com/heygen-com/hyperframes/tree/main/registry) · [카탈로그](https://hyperframes.heygen.com/catalog) | 약 450개 블록·컴포넌트를 편집 가능한 HTML 원본으로: 전환·겹치기·제목·키네틱 글자·자막·차트·지도·3D·카메라 이동. `npx hyperframes add <블록>` 한 줄로 `compositions/` 에 HTML 한 파일 | transition · text · graphic · camera | 저장소 Apache-2.0, **블록별 라이선스 표기는 페이지에 없음 — 확인 필요** |
| `@hyperframes/shader-transitions` | WebGL 셰이더 전환 (예: flash-through-white) | transition (지금 `gl-transitions` 가 hold) | Apache-2.0 |
| `/media-use` 스킬 | 음악·효과음·그림·아이콘·목소리·**색보정 룩**을 무료 소스나 HeyGen 도구로 | bgm · footage | 스킬 문서 확인 필요 (HeyGen 유료 도구 호출은 쓰지 않음) |
| [frame.md 디자인 템플릿](https://hyperframes.studio/design) | Biennale Yellow·Bold Poster·Broadside·Cobalt Grid 등 색·글꼴 토큰 묶음 | motion (화면 화풍) — `skins/` 와 같은 층 | 확인 필요 |

**제안:** registry.json 을 읽어 블록마다 우리 카테고리(text/graphic/camera/transition)로 나눈 표를 만들고, `techniques.yaml` 의 tools 칸에 "HyperFrames 블록 <이름>"을 구현 후보로 연결. 새로 설치할 것이 없어 비용이 가장 낮습니다.

## 2. 카테고리별로 더할 만한 레퍼런스

### 2-1. 화면 화풍·삽화 화풍 (`looks.motion` · `looks.illust`)
| 자료 | 무엇 | 우리에게 |
|---|---|---|
| [Futurepedia AI Style Atlas](https://www.futurepedia.io/resources/ai-style-atlas) (docs/39 에 이미 있음) · [3D Style Atlas](https://www.futurepedia.io/resources/3d-style-atlas) | 설명형 86화풍(14계열: 화이트보드·클레이·블루프린트·Manim 수학 …) + 3D 37화풍, 화풍마다 Claude 프롬프트·소리 묶음 | **화풍 후보를 고르는 비교표로 가장 바로 씀.** 우리에 없는 계열: 화이트보드(마커)·픽셀·로우폴리·복셀·종이 디오라마·Manim 수학 |
| [ChatCut 설명형 스타일 10](https://chatcut.io/docs/explainer-videos.md) | 화풍마다 스킬 하나(Paper Diorama, Pixel Art …) | '화풍 = 스킬 하나' 구조가 우리 looks + 스킬 방식과 같음 |
| [iart-ai/explainer-video-skills](https://github.com/iart-ai/explainer-video-skills) (MIT, ★125) | 5개 스킬: explainer-video, diagram-animation(차례로 드러남·자라는 막대·카운트업), whiteboard-animation, **isometric-animation(2.5D 층·분해도·카메라 표류)** | **아이소메트릭**은 docs/39 에서 '공급망·결제 흐름' 후보였는데 아직 looks 에 없음 |
| PHANTOMTONYT/motion-design-skills (미확인) | 5스타일: 3D 장난감·키네틱 글자·손그림·시스템 도식·데이터 차트 | 3D 장난감 = 우리 `clay-miniature` 와 비교 |
| artemnovitckii/claude-animation-skills (미확인) | 로우폴리·복셀 삽화 화풍 | 호기심 채널 화풍 후보 |
| [Explainer Video Kits](https://www.producthunt.com/products/explainer-video-kits/launches) | 유료, 미리 그린 스타일 프레임 | 사지 않더라도 '스타일 프레임' 단위로 고르는 방식 참고 |
| 분류 글: [moonb 12 스타일](https://www.moonb.io/blog/animation-styles) · [B2W 16 스타일](https://www.b2w.tv/blog/animation-styles) · [Blue Forest 가이드](https://blueforeststudios.squarespace.com/definitive-guide-to-animation-styles) | 업체가 쓴 화풍 분류 | 이름 붙이기·분류 기준 참고용 (예시는 각 스튜디오 포트폴리오로 확인) |

**looks 에 없는 계열(후보):** 화이트보드 마커 · 아이소메트릭 · 종이 디오라마/팝업 · 픽셀 · 로우폴리/복셀 · Manim 수학 칠판(지금 `chalkboard` 와 다름: 수식이 변형되는 움직임).

### 2-2. 글자 연출 (`text`)
| 자료 | 무엇 | 라이선스 |
|---|---|---|
| [iart-ai/kinetic-typography-skills](https://github.com/iart-ai/kinetic-typography-skills) | 낱말 드러남·박자 맞춘 글자 | 확인 필요 (상위 모음 motion-skills 는 MIT) |
| [Effect Atlas](https://effectatlas.com) | 웹 움직임 효과 50+ (글자·호버·스크롤·전환)를 HTML/CSS/JS 로, AI 가 읽는 설명 포함 | 자체 라이선스 — 확인 필요 |
| [greensock/gsap-skills](https://github.com/greensock/gsap-skills) | GSAP 공식 에이전트 스킬 (타임라인 등) | MIT. 우리는 gsap 3.13 사용 중 — SplitText·ScrambleText 후보(`split-reveal`·`scramble`)를 구현할 때 기준 문서로 |
| [SHARPLEE00/lookbk-skills](https://github.com/SHARPLEE00/lookbk-skills) | 8개 스킬, HyperFrames+GSAP 키네틱 제목 영상 포함 | MIT (README 표기) |

### 2-3. 그래픽·데이터 연출 (`graphic`)
| 자료 | 무엇 | 우리 후보와 연결 |
|---|---|---|
| [iart-ai/data-animation-skills](https://github.com/iart-ai/data-animation-skills) | CSV → 움직이는 차트 3스킬 | `bar-race`·`chart-morph`(candidate) |
| [iart-ai/map-animation-skills](https://github.com/iart-ai/map-animation-skills) | 경로·나라 색칠 지도 움직임 | 이미 있는 journey·choropleth 보강 |
| HyperFrames `data-chart` 블록 ([페이지](https://hyperframes.heygen.com/catalog/blocks/data-chart)) | GSAP 막대·선 차트 한 파일 | 이미 설치된 도구 안 |
| DbgKinggg/plotbeat (미확인) | HyperFrames 차트 영상 템플릿 | `bar-race` |
| [georgesmomo/tech-to-motion](https://github.com/georgesmomo/tech-to-motion) | HyperFrames+GSAP 도식 설명 영상 | AI 채널 시스템 도식 |
| [jangtrinh/design-os-svg-animation](https://github.com/jangtrinh/design-os-svg-animation) | SVG 움직임 1080p 60fps | **PolyForm Shield — 오픈소스 아님, 보류** |

### 2-4. 카메라·깊이 (`camera`)
| 자료 | 무엇 | 우리 후보와 연결 |
|---|---|---|
| sanskarprajapati/parallax-doc (미확인) | 2.5D 패럴랙스 다큐 | `parallax-photo`(candidate) |
| Moh4696/cinematic-skill (미확인) | 사진 여러 장 위를 한 번의 이어진 카메라로 | `pull-back`·아카이브 다큐 |
| JohnChow90/video-shotcraft (미확인) | 샷 레시피 카드 157장, 2.5D 카메라 이동 | **카메라 카테고리를 채우는 목록으로 가장 큼** — 이름·분류만 가져와도 유용 |
| RajaskaJanuardani/motion-craft (미확인) | Remotion, 43 스타일·카메라·전환 | Remotion(별도 라이선스)이라 구조만 참고 |

### 2-5. 장면 전환 (`transition`)
| 자료 | 무엇 | 라이선스 | 판단 |
|---|---|---|---|
| [cut-fx](https://pypi.org/project/cut-fx/) ([GitHub](https://github.com/tomastimelock/cut-fx)) | **이름 붙은 전환 559개를 11묶음으로** (motion 119·light_fx 93·shape_mask 44·film_retro 35·optical_blur 31 …), ffmpeg·NumPy·HTML/CSS·GLSL 네 방식 | MIT, 0.1.5 Beta | MP4 두 개를 잇는 후처리라 HTML 장면 안 전환과는 다름. **전환 분류표(이름 사전)로 가치 큼.** 화려한 전환이 많아 우리 피드백(휩 팬·줌 인 전환 hold)과 부딪힘 — 묶음 중 shape_mask·optical_blur 정도만 후보 |
| [gl-transitions](https://www.npmjs.com/package/gl-transitions) | 셰이더 전환 모음 | MIT | 이미 hold 로 기록됨 |
| [@pyreon/kinetic-presets](https://pyreon.github.io/pyreon/docs/kinetic-presets) | CSS 등장·퇴장 프리셋 (slide·scale·blur) + 조합 | 확인 필요 | 작은 요소 등장용 |
| [Material motion design kit](https://m2.material.io/resources/motion-design-kit) | 화면 전환 패턴(컨테이너 변형·공유 축·페이드 스루) | Google 문서 | `match-move`(Flip) 의 설계 기준으로 |

### 2-6. 움직임 원리·이징 (카테고리 공통 — '어떻게 움직이나'의 기준)
- [Motion in Design](https://teranya.github.io/uimotionref/) — Fluent·Carbon·Material 3·Salesforce 의 시간·이징 기준을 한 표로. Carbon 의 **productive(정보형) / expressive(표현형)** 나눔은 우리 '정보형 장면 vs 이야기형 장면'과 그대로 맞음.
- [LottieFiles motion-design-skill](https://skills.sh/LottieFiles/motion-design-skill/motion-design) (MIT) — 등장은 ease-out·퇴장은 ease-in, **재질별 시간표(탄성·유체·종이·기체·유리)**. 우리 화풍마다 기본 이징을 붙일 때 근거로.
- [iart-ai/motion-design-skills](https://github.com/iart-ai/motion-design-skills) — 시간·이징·구성·색 9스킬.
- [A List Apart: 디자인 시스템에 애니메이션 넣기](https://alistapart.com/article/integrating-animation-into-a-design-system) — 움직임 종류를 분류하는 법(IBM·Salesforce 비교).

### 2-7. 실사 색보정 (`footage`) — 레퍼런스가 가장 빈약한 곳
에이전트 스킬 모음 어디에도 LUT·색보정 카탈로그는 없었습니다(HyperFrames `/media-use` 의 '색보정 룩'이 유일).
| 자료 | 라이선스 | 판단 |
|---|---|---|
| [FreeVisuals 22 Mega LUT Pack](https://www.freevisuals.net/luts/free-22-cinematic-luts-pack) | 무료·상업 가능·출처 불요 (페이지 표기) | 80s·틸앤오렌지 등 — 우리 3개 외 후보 |
| [FreeVisuals 10 Cinematic](https://www.freevisuals.net/luts/free-10-cinematic-luts-pack) | 무료·상업 가능 (페이지 표기) | 따뜻함·도시·인물 |
| [PremiumBeat 무료 LUT 모음](https://www.premiumbeat.com/blog/29-free-luts-for-video/) | 묶음마다 다름 | Juan Melara 팩 = 정확한 보정용(꾸밈 적음) |
| FreeVisuals 50 Travel Documentary · Envato 다큐 팩 · [Filmora 다큐 팩](https://filmora.wondershare.com/video-creative-tips/free-documentary-lut-pack.html) | 상업은 유료 / 라이선스 미표기 | 보류 |

**제안:** LUT 파일보다 우리 `finish.py` 의 ffmpeg `lut3d`/`eq` 값으로 화풍을 정의하는 지금 방식을 유지하고, 위 무료 팩은 "이 느낌" 비교용으로만. 후보 화풍: 바랜 70년대(호기심 역사), 틸앤오렌지 약하게(시장 인물), 중립 정확 보정(인터뷰 원본).

### 2-8. 배경음 (`bgm`)
| 자료 | 라이선스 | 분위기 분류 |
|---|---|---|
| YouTube Audio Library (Studio 안) | 곡마다 다름 — 출처 표기 필요한 곡 있음 | 분위기·장르 필터 있음 |
| Pixabay Music | Pixabay Content License (상업·출처 불요) | 비트 맞춤 검색 |
| Mixkit | 자체 무료 라이선스 | 장르·분위기 |
| Incompetech · Bensound 무료 | CC BY — 설명란 표기 필요 | |
| [georgesmomo/idea-to-motion](https://github.com/georgesmomo/idea-to-motion) (MIT) | 박자 격자에 맞춘 **절차적 음악·합성 효과음** | 라이선스 걱정 없는 '만든 음악' 길 — 분위기 7개 외 후보 |
| kmilo93sd/agent-video-editor (미확인) | CC0 효과음 128·그래픽 26 | 효과음 카테고리가 생기면 |

**구성요소 카테고리 후보:** 지금 8개에 **효과음(SFX)** 이 없습니다. 여러 스킬 모음(idea-to-motion·product-launch-motion·agent-video-editor)이 음악과 효과음을 따로 다룹니다.

## 3. 비슷한 방식으로 모아 둔 스킬·카탈로그 (메타 목록)
우리 `components.yaml`·`looks.yaml`·`techniques.yaml` 처럼 "골라 쓰는 목록"을 이미 만든 곳들입니다.

| 모음 | 성격 | 규모 | 라이선스 | 가져올 점 |
|---|---|---|---|---|
| [zhuyansen/awesome-claude-video-skills](https://github.com/zhuyansen/awesome-claude-video-skills) | Claude Code·Codex 영상 스킬 저장소를 **종류별로 나누고 보안 등급(SAFE/CAUTION)·실행 결과**를 붙인 목록 | 180~526개 (페이지 안에서 숫자가 다름) — 설명형 93·모션그래픽 40·이야기·애니메이션 35 … | 표기 확인 필요 | 새 스킬을 들일 때 **보안 등급 먼저 보는 습관** — 우리 docs/05 검토와 같은 목적 |
| [frankxai/awesome-motion-design-agent-skills](https://github.com/frankxai/awesome-motion-design-agent-skills) | GSAP·Remotion·Lottie·Rive 스킬 지도 + 자체 스킬 5개(motion-director 등) | 큐레이션 약 25 | CC0 | 'motion-director' = 장면마다 움직임을 고르는 역할 — 우리 edit-plan 과 비교 |
| [iart-ai/motion-skills](https://github.com/iart-ai/motion-skills) | **56개 스킬을 19개 팩으로** (키네틱 글자·데이터·설명형·지도·웹 움직임·수학 …) | ★1.9k | MIT | 카테고리 = 팩 구조가 우리 components 와 가장 닮음 |
| [iart-ai/awesome-motion-skills](https://github.com/iart-ai/awesome-motion-skills) | 위 팩들의 목록 | 15 | CC0 | |
| [HyperFrames registry](https://hyperframes.heygen.com/catalog) | 블록 약 450 | | Apache-2.0 | §1 — 이미 설치됨 |
| [remotion-dev/skills](https://github.com/remotion-dev/skills) | Remotion 공식 13 스킬 (maps·captions 등) | | 표기 확인 필요, Remotion 은 별도 라이선스 | 카탈로그 아님. 우리는 HyperFrames 라 참고만 |
| [Futurepedia Style Atlas](https://www.futurepedia.io/resources/ai-style-atlas) | 화풍 86 + 3D 37, 같은 주제로 미리 보기 | | 사이트 이용 조건 | 우리 `looks-gallery` 와 같은 '같은 내용, 화풍만 바꿔 보기' |
| [ChatCut 설명형 스타일](https://chatcut.io/docs/explainer-videos.md) | 화풍 = 스킬 하나, 10개 | | 서비스 문서 | |
| [cut-fx](https://pypi.org/project/cut-fx/) | 전환 이름 사전 559 | | MIT | §2-5 |
| [Effect Atlas](https://effectatlas.com) | 웹 효과 50+ HTML/CSS/JS | | 자체 | §2-2 |
| 정리 글: [trinhstudio 17 저장소](https://trinhstudio.com/inside/claude-motion-graphics-repos-2026) · [Keyframes 6 스킬](https://getkeyframes.com/blogs/guides/claude-video-skills) · [agentskillshub 530 등급](https://agentskillshub.top/best/claude-video-skills/) | 블로그·목록 사이트 | | — | 목록을 다시 훑을 때 시작점 |
| 그 밖 HyperFrames 기반 스킬 묶음 | [unclejobs-ai/motion-video-skill](https://github.com/unclejobs-ai/motion-video-skill) · [Sunwood-ai-labs/hyperframes-motion-reel-skill](https://github.com/Sunwood-ai-labs/hyperframes-motion-reel-skill) · bangtutorial/bang-motion(설명형 5스타일) · Neelshah1810/Claude-Video-Skills(11 스킬) | | 각자 확인 | 대부분 홍보 영상용 — 설명형은 bang-motion·Neelshah 정도 |

## 4. 넣을 때의 주의 (지금까지 피드백과 부딪히는 점)
- 이 모음들 대부분은 **제품 홍보·런치 영상**용이라 빠르고 화려합니다. 우리 기준(정보형은 천천히 나타나고 움직임, 휩 팬·줌 인 전환 hold, 강조 예산)과 맞는 것만 고릅니다.
- "코드로만 그린 화풍"은 docs/38 의 도형 모음 한계를 가집니다(05 §0-8: 그림은 원화, 코드는 움직임). Style Atlas·ChatCut 은 화풍 **고르기**에 쓰고 그림은 원화·생성 이미지로.
- 새 스킬을 설치하면 `tools/external.json` 에 고정하고 docs/05 에 SKILL.md·네트워크 호출 검토를 남깁니다. PolyForm·Remotion 처럼 오픈소스가 아닌 라이선스는 보류.

## 5. 다음 단계 (사용자 결정)
1. **HyperFrames registry 정리(설치 비용 0):** registry.json → 카테고리별 블록 표 → 쓸 만한 것을 techniques 후보로. 가장 먼저 권합니다.
2. **새 카테고리 '효과음'** 을 components 에 둘지.
3. **looks 후보 3개 골라 시험:** 아이소메트릭(시사·AI 공급망) · 화이트보드 마커 · 종이 디오라마 중에서.
4. 카메라 카테고리 보강: video-shotcraft 157 카드의 이름·분류만 읽어 와 `camera` 후보표 만들기 (라이선스 확인 후).


## 6. 진행 결과 (2026-11-20, 사용자: "1. 응 2.응 3.전부 다")
| 결정 | 한 일 | 파일 |
|---|---|---|
| 1. HyperFrames 블록 정리 | 설치된 v0.8.190 registry 456개를 읽어, 설명형에 맞는 **76개**를 우리 카테고리(글자 18·그래픽 25·카메라 9·전환 13·바탕 6·예시 5)로 고르고 기법 id(`maps_to`)·맞음 정도(바로 맞음/고쳐 쓰면/보류)를 붙임. 화풍 목록 페이지의 각 카테고리 아래 '이미 설치된 HyperFrames 블록' 접힌 목록으로 보임. 전체 456개는 부록 A | `styles/hyperframes_blocks.yaml`, `looks.components()` 의 `blocks` |
| 2. 효과음 카테고리 | 구성요소 '효과음 묶음'(`sfx_set`, 소리 축 — 소리 하나하나의 목록 `sfx` 와 별개). 묶음 6개: 기본 · 종이와 연필 · 화이트보드 마커 · 부드러운 앱 소리 · 다큐 조용히 · 없음. 새 소리는 내려받지 않고 이미 있는 Pixabay 묶음(상업·출처 불요)과 ffmpeg 합성(종이 바스락·마커 끽끽). `look <프로젝트> --set sfx_set=<id>` → hybrid·hookshort 렌더가 사건 소리를 그 묶음으로 바꾸고 크기(gain)를 곱함 | `assets/sfx/sfx.yaml`, `styles/components.yaml`, `ytflow/stages/hybrid.py` `sfx_files(project_dir)`, `looks.sfx_palette` |
| 3. 새 화풍 3종 시안 | 같은 내용(물건이 집 앞까지 오는 길)을 화이트보드·아이소메트릭·종이 디오라마로 8초씩 렌더(HyperFrames), 짝인 효과음 묶음을 입힘. 화면 화풍 3개(status: trial, 스킨 포함) + 삽화 화풍 2개(아이소메트릭·종이 디오라마 그림 생성 문장) 등록 | `projects/20261120-looks-trial/`, `skins/{whiteboard,isometric,paper-diorama}/`, `styles/looks.yaml` |

**남은 것**
- 시안 판정은 사용자 몫: `python -m ytflow review projects/20261120-looks-trial --pass | --reject "이유"` 후 looks.yaml status 를 approved 로.
- 아이소메트릭·종이 디오라마의 '모양'(상자 투영·팝업 건물·찢은 종이 층)은 시안 렌더러에만 있습니다. 합격하면 장면 종류(렌더러)로 옮겨야 다른 영상에서 씁니다. 지금 스킨은 색·글꼴만 바꿉니다.
- 삽화 화풍 2개의 예시 그림은 PC 에서 그립니다(`looks --order` → PC `looks --draw auto`). 이 세션은 main 에 올리지 않아 주문서를 만들지 않았습니다.
- **공유 화풍 목록 페이지는 아직 갱신하지 않음**: 같은 시각 다른 세션(`claude/bold-cray-oc587w`, 잠금 '구성요소 목록 확장')이 구성요소 21가지·스타일 176가지 판을 올려 두어, 이 브랜치 판으로 올리면 그 작업을 덮어씀. 합치는 요청을 남김(`proposals/manual/20261120-074232-vigilant-lovelace-1uahwn.md`) — 시험 합치기에서 충돌 세 곳 모두 '둘 다 살림'으로 풀림. 그쪽 '효과음'(sfx)은 소리 하나하나의 목록, 이쪽 '효과음 묶음'(sfx_set)은 한 영상의 소리 한 벌이라 둘 다 둠.
- `techniques.yaml`(잠금 대상)에 블록 이름을 tools 로 잇는 일, 목록에 없는 기법 후보(`strikethrough-replace` 정정 연출, `pan-stations` 정거장 카메라, `decline-chart` 하락 차트)는 잠금을 잡을 때 반영.

## 부록 A. HyperFrames v0.8.190 registry 전체 456개 — 태그로 나눈 목록 (자동 분류, 이름 = `npx hyperframes add <이름>`)
분류는 registry-item.json 의 태그로 기계적으로 나눈 것입니다(한 블록이 여러 태그를 가지면 위 순서에서 먼저 걸린 곳). 설명형에 맞게 고른 76개와 우리 카테고리 연결은 `styles/hyperframes_blocks.yaml`.

- **글자 연출** (83): `canopy-part-title`, `carousel-text-circle-1`, `carousel-text-circle-2`, `carousel-text-circle-3`, `carousel-text-circle-4`, `carousel-text-circle-5`, `extruded-logo`, `glass-hero`, `glass-shard-title`, `hw-frame`, `hw-path-text`, `hw-pipeline`, `hw-text-cloud`, `hw-title`, `hw-write-title`, `lower-third-bild`, `lt-accent-underline`, `lt-bold-block`, `lt-clean-bar`, `lt-color-block`, `lt-dark-card`, `lt-kicker-name`, `lt-mask-reveal`, `lt-neon-border`, `lt-side-rule`, `lt-soft-pill`, `lt-stack-bars`, `news-ticker`, `split-flap-board`, `vfx-text-cursor`, `weight-wave`, `wireframe-portal-title`, `yt-prism-title`, `blur-out-up`, `bottom-up-letters`, `caption-blend-difference`, `caret-swap`, `char-slam-explode`, `cursor-text-select`, `extended-keyframe`, `focus-blur-resolve`, `headline-slam`, `hw-arrow`, `hw-boil`, `hw-box-label`, `hw-callout-circle`, `hw-underline`, `inline-highlight`, `kinetic-center-build`, `kinetic-type-swap`, `line-by-line-slide`, `line-swap`, `logo-brand-close`, `marker-checklist-card`, `marker-highlight`, `matrix-decode`, `mk-emphasis-type`, `morph-text`, `particle-text-dissolve`, `per-word-crossfade`, `per-word-rise`, `perspective-marquee`, `rgb-glitch-text`, `scan-band`, `scramble-reveal`, `shared-axis-y`, `shared-axis-z`, `shimmer-sweep`, `slot-machine-roll`, `soft-blur-in`, `staggered-fade-up`, `strikethrough-replace`, `text-shimmer`, `texture-mask-text`, `ticker-takeover`, `titlecard-calm`, `titlecard-lockup`, `top-down-letters`, `tracking-in`, `typewriter`, `variable-axis-type`, `vox-annotate`, `wordmark-tiles`
- **데이터·지도** (21): `bar-chart-race`, `data-chart`, `flowchart-vertical`, `flowchart`, `north-korea-locked-down`, `nyc-paris-flight`, `oscilloscope-trace`, `spain-map`, `us-map-bubble`, `us-map-flow`, `us-map-hex`, `us-map`, `week-in-merges`, `world-map`, `animated-bar-chart`, `chart-story`, `conic-progress-ring`, `decline-chart`, `logo-wall`, `number-wheel`, `star-rating-fill`
- **카메라·깊이** (15): `camcorder-hud`, `camera-dolly-zoom`, `rack-focus`, `camera-scan-gate`, `camera-shake`, `cursor-zoom-follow`, `drift-hold`, `filmed-screen`, `focus-rack`, `pan-stations`, `pull-back-reveal`, `push-in`, `scroll-camera-story`, `ui-focus-zoom`, `yt-camera-move`
- **장면 전환** (74): `beat-freeze-cut`, `chromatic-radial-split`, `cinematic-zoom`, `code-slice-hero`, `cross-warp-morph`, `domain-warp-dissolve`, `editorial-flash-overlay`, `flash-through-white`, `glitch`, `gravitational-lens`, `hw-scribble-transition`, `light-leak`, `mk-clone-wall-transition`, `organic-light-leak-overlay`, `ridged-burn`, `ripple-waves`, `sdf-iris`, `swirl-vortex`, `thermal-distortion`, `transitions-3d`, `transitions-blur`, `transitions-cover`, `transitions-destruction`, `transitions-dissolve`, `transitions-distortion`, `transitions-grid`, `transitions-light`, `transitions-mechanical`, `transitions-other`, `transitions-push`, `transitions-radial`, `transitions-scale`, `whip-pan`, `avatar-group-hover`, `badge-pop`, `before-after-wipe`, `caption-clip-wipe`, `card-resize`, `chromatic-aberration-wipe`, `colorama-wipe`, `comparison-split`, `curtain-reveal`, `cut-the-curve`, `directional-wipe`, `fade-through`, `grid-pixelate-wipe`, `halftone-dissolve`, `icon-swap`, `input-feedback`, `iris-reveal`, `match-cut`, `menu-morph`, `micro-transitions`, `morph-swap`, `number-pop-in`, `ordered-dither-pass`, `page-slide`, `panel-reveal`, `paper-collage-reveal`, `parallax-device-dive`, `parallax-unzoom`, `parallax-zoom`, `rubber-band-bumper`, `skeleton-reveal`, `success-check`, `tabs-slide-indicator`, `text-match-cut`, `text-stagger`, `text-state-swap`, `tilt-card`, `torn-paper-rip`, `type-match-cut`, `whip-pan-cut`, `zoom-through-transition`
- **바탕·질감** (53): `aurora`, `blob`, `chrome-orb`, `code-shader-dissolve`, `color-wheel`, `cosmic-orb`, `falling-lines`, `flowing-gradient`, `fractal-noise`, `frost`, `gabor-noise`, `gallery-tunnel`, `godrays`, `goo`, `halftone-field`, `heatmap`, `hologram`, `holographic`, `lens-flare`, `light-edge`, `liquid-metal`, `marble`, `mesh-gradient`, `mk-background`, `nebula`, `obsidian`, `plasma`, `plastic`, `prism`, `ripples`, `sine-wave`, `spiral-galaxy`, `spiral`, `strands`, `stripes`, `sun-burst`, `swirl`, `thin-film`, `vfx-anamorphic-flare`, `vfx-liquid-background`, `voronoi`, `water`, `waveform`, `worley-noise`, `yt-lcd-background`, `ascii-render-pass`, `aurora-drift`, `beat-pulse-background`, `dynamic-grid`, `grain-field`, `grain-overlay`, `ink-bleed-reveal`, `yt-screen-warp`
- **겹치기·커서** (30): `freeze-frame-dressing`, `instagram-follow`, `macos-notification`, `reddit-post`, `snow`, `spotify-card`, `starfield`, `tiktok-follow`, `x-post`, `yt-comment-card`, `yt-lower-third`, `agent-cursor`, `cursor-annotate`, `cursor-context-menu`, `cursor-drag-drop`, `cursor-glyph-trail`, `cursor-marquee-select`, `dart-cursor`, `light-sweep-pass`, `magnetic-cursor`, `multiplayer-cursors`, `native-notification-pop`, `oversized-cursor`, `press-ripple`, `sheet-spring-up`, `touch-indicator`, `typing-indicator`, `vignette`, `yt-circle-pointer`, `yt-feather-highlight`
- **자막 스타일** (16): `mk-callout-highlight`, `caption-camera-follow`, `caption-editorial-emphasis`, `caption-emoji-pop`, `caption-glitch-rgb`, `caption-gradient-fill`, `caption-highlight`, `caption-kinetic-slam`, `caption-matrix-decode`, `caption-neon-accent`, `caption-neon-glow`, `caption-parallax-layers`, `caption-particle-burst`, `caption-pill-karaoke`, `caption-texture`, `caption-weight-shift`
- **앱·코드 화면** (50): `ai-answer-rank`, `ai-chat-reveal`, `app-showcase`, `chatgpt-exchange`, `claude-exchange`, `code-3d-extrude`, `code-diff`, `code-highlight`, `code-morph`, `code-particle-assemble`, `code-scroll`, `code-snippet-apple-terminal-pro`, `code-snippet-dark-2026`, `code-snippet-dark-modern`, `code-typing`, `message-thread-reveal`, `notes-reveal`, `notification-cascade`, `share-sheet-carousel`, `slack-notification-ad`, `vpn-youtube-spot`, `browser-device-stage`, `chat-message`, `chat-thread`, `code-terminal-run`, `cta-close`, `cta-lockup`, `device-frame-stage`, `focus-swap`, `gesture-tap`, `icon-morph-beat`, `notes-typing`, `notification-pileup`, `notification-stack`, `offset-path-traveler`, `screen-flow-carousel`, `segmentation-flood`, `soft-blob-touch`, `spring-stack-shuffle`, `state-chip-rail`, `sticky-mock-swap`, `store-badge-lockup`, `streaming-text`, `telemetry-hud`, `terminal-simulator`, `testimonial-card`, `toggle-flip`, `tracing-beam`, `typed-prompt`, `vector-editor-rig`
- **3D** (26): `carousel-orbit-1`, `carousel-orbit-2`, `carousel-orbit-3`, `carousel-orbit-4`, `carousel-orbit-5`, `carousel-vision-1`, `carousel-vision-2`, `carousel-vision-3`, `carousel-vision-4`, `carousel-vision-5`, `cuboid-carousel`, `exploded-stack`, `frost-sequence-camera-orbit`, `ios26-liquid-glass`, `liquid-glass-notification`, `liquid-glass-widgets`, `macos-tahoe-liquid-glass`, `orbit-card`, `product-turntable`, `ui-3d-reveal`, `vfx-iphone-device`, `vfx-liquid-glass`, `vfx-magnetic`, `vfx-portal`, `vfx-shatter`, `three-orbiting-cards`
- **기타 움직임** (80): `apple-money-count`, `blue-sweater-intro-video`, `carousel-circle-1`, `carousel-circle-2`, `carousel-circle-3`, `carousel-circle-4`, `carousel-circle-5`, `carousel-path-1`, `carousel-path-2`, `carousel-path-3`, `carousel-path-4`, `carousel-path-5`, `cinemagraph`, `gooey-split`, `heygen-avatar-promo-card`, `logo-outro`, `lottie-character-walk`, `mk-line-graph`, `mk-placeholder-grid`, `mk-progress-stat`, `mk-specs-list`, `thread-message-stack`, `yt-logo-intro`, `yt-vertical-fill`, `arc-motion-path`, `ascii-trail-reveal`, `avatar-cloud`, `beat-accent`, `beat-timeline`, `blur-in`, `camera-rig-depth-stack`, `confetti`, `constellation-hub`, `count-up`, `echo-smear`, `echo-trail`, `facet-morph`, `gloss-sweep`, `grade-split-reveal`, `grid-card-assemble`, `keyframe-scrub-stack`, `locked-nucleus-orbit`, `logo-sting`, `mesh-gradient-bg`, `mk-usage-arc`, `modal-morph`, `motion-blur`, `multi-device-splay`, `onboarding-stepper-flow`, `outline-draw`, `overwhelm-surround`, `particle-image-reveal`, `pendulum-swing`, `physical-exit`, `pull-to-refresh`, `radial-surround`, `scroll-feed`, `separator`, `settings-toggle-flow`, `shutter-slam`, `signup-flow`, `slit-scan-reveal`, `social-proof-card`, `split-tilt-cards`, `spotlight-card`, `spring-pop`, `stagger-cascade`, `stagger-lattice`, `stitched-text-draw`, `stop-motion-cadence`, `svg-line-draw-loader`, `svg-mask-reveal`, `svg-stroke-trace`, `swipe-rail`, `testimonial-proof-card`, `trust-strip`, `variable-font-flex`, `velocity-throw-snap`, `whiteboard-ink`, `x-follow-card`
- **통째 예시** (8): `decision-tree`, `kinetic-type`, `nyt-graph`, `play-mode`, `product-promo`, `swiss-grid`, `vignelli`, `warm-grain`
