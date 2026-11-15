# 32. 연출 기법 조사 — 깃허브 등 열린 구현 (2026-11-15)

> 사용자: "용어 사전에 스타일·기법을 정리한 것처럼, 관련된 연출 스타일들을 조사하고 추가해 줘 — 깃허브 같은 데 많지 않아?"

`docs/14`(그래픽 팩 도구)·`docs/17`(스타일 풀·HyperFrames 블록)은 **도구·블록** 단위였다. 이번은 그보다 작은 **연출 기법**(화면 문법) 단위 — 글자 등장, 모양 바뀌기, 장면 이어 주기, 사진 깊이, 데이터 움직임, 화면 나누기 — 를 조사해 `styles/techniques.yaml` 에 카탈로그로 넣었다. 매뉴얼 그래프 '용어 사전 → 연출 기법' 에서 원리 움직임 예시·구현 방법·도구·라이선스·기존 용어와의 관계를 본다.

## 가장 큰 발견: GSAP 플러그인이 모두 무료
우리가 이미 고정해 쓰는 `gsap@3.13.0`(tools/external.json)부터 SplitText·MorphSVG·DrawSVG·ScrambleText·Flip·MotionPath 등 예전 유료(Club) 플러그인이 **모두 무료, 상업 사용 가능**(GreenSock standard no-charge license, Webflow 인수 후). → 새 의존성 없이 글자 쪼개기·스크램블·모프·매치 무브·모션 패스를 렌더러에 더할 수 있다. (클라우드에는 tools/ 가 설치돼 있지 않아 플러그인 파일 존재는 PC 에서 `python scripts/install_tools.py` 후 확인.)

## 카탈로그 (20개, 모두 '스타일 기본값' 층 — 금지·MUST 아님)
| 묶음 | 기법 | 상태 | 쓸 도구 (라이선스) |
|---|---|---|---|
| 글자 | 글자 쪼개 등장 | 비슷한 것 있음 (kinetic) | GSAP SplitText (무료) |
| 글자 | 글자 섞였다 풀리기 | 후보 | GSAP ScrambleText (무료) |
| 글자 | 숫자 세며 오르기 | 있음 (bignum·motion count) | countUp.js (MIT) |
| 글자 | 손그림 형광펜·밑줄·괄호 (차례로) | 비슷한 것 있음 (layers mark) | rough-notation (MIT) |
| 선·모양 | 선이 그려지기 | 있음 (rough.js) | GSAP DrawSVG, vivus (MIT) |
| 선·모양 | 모양 바뀌기 (모프) | 후보 | GSAP MorphSVG, flubber (MIT) |
| 선·모양 | 차례로 등장 (스태거) | 있음 | GSAP stagger, Manim LaggedStart (MIT) |
| 선·모양 | 길 따라 움직이기 | 비슷한 것 있음 (journey) | GSAP MotionPath |
| 이어 주기 | 같은 것이 다음 화면으로 (매치 무브·Flip) | 후보 | GSAP Flip, Manim TransformMatching (MIT) |
| 이어 주기 | 소리 먼저·소리 남기 (J컷·L컷) | 후보 | ffmpeg adelay/amix |
| 이어 주기 | 장면 전환 묶음 (xfade) | 비슷한 것 있음 (edit10) | ffmpeg xfade, Motion Canvas 전환 개념 |
| 이어 주기 | 확대해 들어가며 다음 장면 | **보류** — 시장 v31 과 충돌 | Motion Canvas zoomInTransition 개념 |
| 이어 주기 | 휙 넘기기 (휩 팬) | **보류** — v12 기각과 충돌 | ffmpeg xfade hblur |
| 이어 주기 | 셰이더 전환 모음 | **보류** — 전환마다 라이선스 다름 + v12 | gl-transitions |
| 사진·깊이 | 사진에 깊이 (2.5D 시차) | 후보 (몇 장만) | render-image-depth (MIT) · DepthFlow 는 AGPL 이라 그대로 안 씀 |
| 사진·깊이 | 한 점에서 물러나며 전체 (풀백) | 후보 | HyperFrames pull-back-reveal (Apache-2.0, 설치됨) |
| 데이터 | 순위가 바뀌는 막대 | 후보 | dexplo/bar_chart_race (MIT), HyperFrames bar-chart-race |
| 데이터 | 차트가 다른 차트로 바뀜 | 후보 | MorphSVG, flubber |
| 화면 나누기 | 나란히 맞대기 (말과 행동) | 비슷한 것 있음 (versus·compare) | — (layers 두 칸) |
| 화면 나누기 | 나머지 어둡게 (스포트라이트) | 있음 (map_causal) | — |

## 지금까지 피드백과의 관계 (카탈로그 `caution` 칸)
- **사용자의 핵심 뜻 '말하는 것이 화면에 생긴다'(작업 기준)에 가장 잘 맞는 후보**: 모프(동사를 모양이 연기) · 스크램블·카운트업(숫자가 밝혀짐) · 매치 무브(장면이 이어짐) · 맞대기(말과 행동) — 화면 전체를 흔드는 카메라가 아니라 **말한 것 하나가 바뀌는** 움직임.
- **보류 3개**는 기각(v12 '정신없다', v31 '확대·축소 쓰지 말라')과 부딪혀서. 사진 깊이·풀백도 카메라 계열이라 '한 영상 몇 번'.
- 모든 기법은 강조 예산(v4: 1분 1번·자막과 중복 금지) 안에서.

## 늘리는 법
`styles/techniques.yaml` 에 한 항목 추가(name·group·status·plain·look·use_when·caution·how·tools·related·anim) → `python -m ytflow manual-graph` → 용어 사전에 바로 나온다. 후보를 구현하면 status 를 have 로 바꾸고 렌더러 위치를 how 에 적는다. 도구를 실제로 설치할 때는 `tools/external.json` 에 버전 고정 + `docs/05-skills-review.md` 기록(AGENTS 외부 도구 규칙).

## 더 볼 곳 (기법 아이디어 모음, 라이선스는 항목마다 다시 확인)
- iart-ai/motion-skills — 에이전트용 모션그래픽 스킬 50여 개(키네틱 타이포·설명 영상·데이터 시각화·Manim), 목록 사이트상 MIT
- doong-jo/kinetic-typography (MIT) · fliptheweb/motion-ui-design · bitjson/awesome-web-animation — 웹 모션 예시·라이브러리 목록
- Manim Community (MIT) — 수학·개념 설명 애니메이션 문법(Transform·Write·LaggedStart)

## 출처
- GSAP 무료화: [gsap npm README](https://cdn.jsdelivr.net/npm/gsap@3.15.0/README.md), [GSAP 플러그인 스킬(GreenSock)](https://tessl.io/registry/skills/github/greensock/gsap-skills/gsap-plugins)
- flubber: [github.com/veltman/flubber](https://github.com/veltman/flubber) · rough-notation: [roughnotation.com](https://roughnotation.com), [README](https://cdn.jsdelivr.net/npm/rough-notation@0.5.1/README.md) · vivus: [ossinsight](https://ossinsight.io/analyze/maxwellito/vivus) · countUp.js: [github.com/inorganik/countUp.js](https://www.github.com/inorganik/countUp.js)
- Manim: [manim.community](https://manim.community/), [LaggedStart](https://docs.manim.community/en/stable/reference/manim.animation.composition.LaggedStart.html)
- Motion Canvas 전환: [motioncanvas.io/docs/transitions](https://motioncanvas.io/docs/transitions), [API](https://motioncanvas.io/api/core/transitions)
- ffmpeg xfade: [trac.ffmpeg.org/wiki/Xfade](https://trac.ffmpeg.org/wiki/Xfade), [예시](https://ottverse.com/crossfade-between-videos-ffmpeg-xfade-filter/)
- gl-transitions: [README](https://unpkg.com/gl-transitions@1.76.1/README.md), [npm](https://npmjs.com/package/gl-transitions)
- 2.5D 깊이: [DepthFlow (PyPI)](https://pypi.org/project/depthflow), [render-image-depth](https://awesome.ecosyste.ms/projects/github.com%2Factiveguild%2Frender-image-depth)
- 바 차트 레이스: [dexplo/bar_chart_race](https://awesome.ecosyste.ms/projects/github.com%2Fdexplo%2Fbar_chart_race)
- 편집 문법(매치 컷·J/L컷·휩 팬): [Storyblocks](https://www.storyblocks.com/resources/tutorials/film-editing-techniques), [Descript](https://www.descript.com/blog/article/learn-the-10-best-video-cuts-every-pro-editor-should-know), [Photography News](https://www.photographynews.co.uk/learning/the-essential-cuts-every-video-editor-needs-to-know/)
- 모음: [iart-ai/motion-skills](https://github.com/iart-ai/motion-skills), [kinetic-typography](https://awesome.ecosyste.ms/projects/github.com%2Fdoong-jo%2Fkinetic-typography), [awesome-web-animation](https://github.com/bitjson/awesome-web-animation)
