# 38. 모션그래픽 카탈로그 — 어떤 것이 있고, 어떤 상황에 쓰나 (2026-11-16)

> 사용자: "모션그래픽도 그래픽별로 스타일을 조사하고 분류해줘" · "즉 어떤 상황에 어떤 모션그래픽을 사용하고 어떤 모션그래픽들이 존재하는지 정리하고싶어"

**원본은 `styles/motion-catalog.yaml`** (이 문서는 `python scripts/motion_catalog.py` 로 만든 읽는 판 — 고칠 때는 YAML 만).
조사 범위: 설치된 HyperFrames 레지스트리 블록 448개(태그로 10종류에 나눔), 이 저장소의 렌더러·장면 종류·스타일, 모션그래픽 스타일 분류 글(아래 출처).
`docs/32`·`styles/techniques.yaml` 은 더 작은 **연출 기법**(글자 쪼개기·모프…), 이 문서는 화면 한 장을 채우는 **모션그래픽 스타일**이다. `docs/37` 은 그것을 **매끄럽게** 만드는 법.

## 0. 한눈에

- 그래픽 종류 **10** · 모션그래픽 스타일 **52** · 그림체 **12** (§6) — ✅ 있음 32 · ◐ 비슷한 것 6 · 📦 블록 있음 11 · ○ 만들어야 2 · ⏸ 보류 1
- ✅ 우리 렌더러에 있음 · ◐ 비슷한 것 있음 · 📦 HyperFrames 블록으로 바로 가능(설치됨, 연결만) · ○ 만들어야 함 · ⏸ 지금까지 피드백과 부딪혀 보류
- 모두 '스타일 기본값' 층 — 금지·MUST 아님. 강조 예산(1분 1번)·카메라 계열 횟수 안에서.

| 그래픽 종류 | 무엇에 | 스타일 |
|---|---|---|
| **글자 (키네틱 타이포)** | 글자 자체가 움직이며 말을 대신한다. 가장 싸고 빠르고, 숫자·결론·훅에 강하다. | 말하는 순간 단어 등장 · 한 줄 박기 · 단어 바꿔 끼우기 · 섞였다 풀리는 글자 · 손글씨로 써지는 제목·표시 · 인용문 타자 |
| **숫자·데이터** | 말한 숫자가 그 순간 화면에 생긴다 — 시장 채널의 뼈대. | 큰 숫자 하나 · 숫자 칸 대시보드 · 선 그래프 그려지기 · 막대 비교 · 순위 바뀌는 막대 · 차트가 다른 차트로 · 사람·물건 아이콘으로 세기 |
| **지도** | '어디서 어디로'가 이야기의 뼈대일 때. 시사·공급망·전쟁·무역. | 경로 지도 여정 · 나라 색칠 지도 · 위치 짚기 |
| **도식·관계** | 원인 → 결과, 구조, 흐름. 화살표가 말과 함께 그어져야 '이어진다'가 보인다. | 인과 지도 · 단계 흐름 · 분해도·층 쌓기 · 도형이 변신 |
| **그림·인물** | 사람의 행동·마음·이야기. 호기심 채널의 몸. 동사를 그림이 연기한다. | 이야기 그림판 (선으로 그려지는 장면) · 애니메이션 무대 (동사 연기) · 삽화 한 장 위 카메라 · 움직이는 비유 · 종이 콜라주 (컷아웃) · 아이소메트릭 (비스듬한 입체 도시·공장) |
| **사진·영상 자료** | 증거·현장. 실사가 있으면 실사가 이긴다. | 사진 천천히 움직이기 · 사진에 깊이 (2.5D) · 아카이브 도장 · 원본 발언 + 2단 자막 · 문서·기사 캡처 형광펜 |
| **화면·UI** | AI·도구 사용법. 실제 화면이 증거, 모형 UI 는 보조. | AI 대화 화면 · 터미널 타자 · 화면 자동 줌·커서 · 코드 바뀌는 부분 · 기기 틀 위 화면 · 게시물·알림 카드 |
| **정보 겹치기 (자막·이름표·표시)** | 화면 위에 얹는 것. 내용을 돕되 주인공이 되지 않는다. | 이름 자막 (로어 서드) · 큰 자막 (쇼츠) · 출처 줄 · 가리키는 표시 · 뉴스 띠 |
| **장면 이어 주기** | 장면과 장면 사이. 눈에 띄지 않는 것이 기본 — 화려한 전환은 피드백과 부딪힌다(v12 '정신없다'). | 그냥 자르기 (박자 위에서) · 겹쳐 바뀌기 · 같은 것이 다음 화면으로 · 밀어내기·닦기 · 화려한 전환 (휙·글리치·셰이더) |
| **배경·질감·카메라·3D** | 바탕과 공기. 채널 정체성(시사 증거판·시장 대시보드·호기심 칠판·AI 앱 창)을 만든다. | 종이·칠판 질감 · 어두운 대시보드 바탕 · 아주 느린 카메라 · 어두운 스튜디오 3D 물체 · 추상 움직이는 배경 (셰이더) |

## 1. 고르는 순서
1. 박자가 하는 일 (상황) — 대본 문장의 동사가 정한다
2. 가진 소스 — 실사·원문이 있으면 footage·screen 이 먼저, 없을 때 그림·도식
3. 채널 얼굴 — 같은 상황이라도 채널의 lean 쪽을 먼저
4. 예산 — 강조(1분 1번), 카메라 계열(한 영상 몇 번), 같은 스타일이 3박자 넘게 이어지면 바꿔 보기 (기본값, 금지 아님)

예: "엔비디아 매출이 전년보다 94% 늘었다" → 상황 `metric` → 실적 발표 원문이 있으면 `source-bite` 뒤에, 없으면 `big-number` → 시장 채널이니 `stat-tiles`·`dark-dashboard` 쪽 → 이 1분에 이미 강조를 썼으면 `big-number` 대신 조용한 `line-draw`.

## 2. 상황 → 모션그래픽 (1순위부터)
상황은 `manual/situations.yaml` (대본 한 박자가 하는 일). `edit-plan` 이 박자마다 상황을 찾는다.

| 상황 | 1순위 | 다음 후보 |
|---|---|---|
| `open-scene` 장면을 연다 (사람·장소·날짜) | **사진 천천히 움직이기** ✅ | 아카이브 도장 ✅ · 이야기 그림판 (선으로 그려지는 장면) ✅ · 위치 짚기 ◐ · 사진에 깊이 (2.5D) 📦 |
| `question` 질문·명제 한 줄을 던진다 | **한 줄 박기** ✅ | 말하는 순간 단어 등장 ✅ · 추상 움직이는 배경 (셰이더) 📦 |
| `said` 누가 말했다 | **원본 발언 + 2단 자막** ✅ | 이름 자막 (로어 서드) ✅ · 인용문 타자 ✅ · 게시물·알림 카드 ◐ |
| `cause` 원인 → 결과를 잇는다 | **인과 지도** ✅ | 애니메이션 무대 (동사 연기) ✅ · 분해도·층 쌓기 📦 · 같은 것이 다음 화면으로 📦 |
| `route` 어디서 어디로 움직였다 | **경로 지도 여정** ✅ | 위치 짚기 ◐ |
| `metric` 숫자·지표가 움직였다 | **큰 숫자 하나** ✅ | 선 그래프 그려지기 ✅ · 숫자 칸 대시보드 ◐ · 섞였다 풀리는 글자 📦 |
| `compare` 둘을 비교한다 | **막대 비교** ✅ | 밀어내기·닦기 📦 · 숫자 칸 대시보드 ◐ · 나라 색칠 지도 ✅ |
| `ratio` 비율·규모를 느끼게 한다 | **사람·물건 아이콘으로 세기** ✅ | 차트가 다른 차트로 ○ · 나라 색칠 지도 ✅ · 분해도·층 쌓기 📦 |
| `timeline` 시간 순서 | **단계 흐름** ✅ | 선 그래프 그려지기 ✅ · 순위 바뀌는 막대 📦 · 겹쳐 바뀌기 ✅ |
| `media` 보도·매체가 어떻게 다뤘나 | **문서·기사 캡처 형광펜** ✅ | 종이 콜라주 (컷아웃) ◐ · 게시물·알림 카드 ◐ · 인용문 타자 ✅ |
| `rank` 순위가 바뀌었다 | **순위 바뀌는 막대** 📦 | 막대 비교 ✅ |
| `change` 바뀌었다·변했다 (동사) | **단어 바꿔 끼우기** 📦 | 도형이 변신 ◐ · 애니메이션 무대 (동사 연기) ✅ · 같은 것이 다음 화면으로 📦 · 코드 바뀌는 부분 📦 |
| `point` 화면의 한 곳을 가리킨다 | **가리키는 표시** ✅ | 문서·기사 캡처 형광펜 ✅ · 화면 자동 줌·커서 ✅ · 손글씨로 써지는 제목·표시 ✅ |
| `conclusion` 꼭 기억할 한 문장 (결론·훅) | **한 줄 박기** ✅ | 말하는 순간 단어 등장 ✅ · 큰 자막 (쇼츠) ✅ |
| `ai-ask` AI 에게 어떻게 시키는지 | **AI 대화 화면** ✅ | 화면 자동 줌·커서 ✅ · 기기 틀 위 화면 📦 |
| `command` 설치·실행 명령 | **터미널 타자** ✅ | 코드 바뀌는 부분 📦 · 단계 흐름 ✅ |

## 3. 채널마다 기본 얼굴
| 채널 | 얼굴 | 먼저 고르는 것 | 덜 쓰는 것 |
|---|---|---|---|
| market | 시장 대시보드 | 큰 숫자 하나 · 숫자 칸 대시보드 · 선 그래프 그려지기 · 막대 비교 · 어두운 대시보드 바탕 · 출처 줄 | 애니메이션 무대 (동사 연기) · 추상 움직이는 배경 (셰이더) |
| issues | 시사 증거판 | 문서·기사 캡처 형광펜 · 원본 발언 + 2단 자막 · 경로 지도 여정 · 나라 색칠 지도 · 인과 지도 · 아카이브 도장 | 섞였다 풀리는 글자 · 추상 움직이는 배경 (셰이더) |
| curiosity | 호기심 칠판 | 이야기 그림판 (선으로 그려지는 장면) · 애니메이션 무대 (동사 연기) · 삽화 한 장 위 카메라 · 손글씨로 써지는 제목·표시 · 사람·물건 아이콘으로 세기 · 종이·칠판 질감 | 숫자 칸 대시보드 · 뉴스 띠 |
| ai | AI 앱 창 | AI 대화 화면 · 터미널 타자 · 화면 자동 줌·커서 · 코드 바뀌는 부분 · 말하는 순간 단어 등장 · 큰 자막 (쇼츠) | 아카이브 도장 · 종이 콜라주 (컷아웃) |

## 4. 그래픽 종류별 전체 목록

### 글자 (키네틱 타이포) (`type`)
글자 자체가 움직이며 말을 대신한다. 가장 싸고 빠르고, 숫자·결론·훅에 강하다.

| 스타일 | 어떻게 보이나 | 상황 | 우리 구현 | HyperFrames 블록 | 상태 |
|---|---|---|---|---|---|
| **말하는 순간 단어 등장** `word-reveal` | 내레이션 단어가 말하는 순간 하나씩 떠오르고 핵심어만 크게·강조색<br>⚠ 롱폼 전체 (지루함) · 자막과 같은 글자를 두 번 | `conclusion`, `question` | `kinetic` | per-word-rise, soft-blur-in, per-word-crossfade, kinetic-center-build, text-stagger | ✅ 있음 |
| **한 줄 박기** `headline-slam` | 짧은 문장이 크게 '쾅' 들어와 멈춤 (흐림→또렷 0.13초, 착지 후 정지)<br>⚠ 1분에 2번 이상 | `conclusion`, `question` | `card_type`, `chapter` | headline-slam, caption-kinetic-slam, titlecard-calm, focus-blur-resolve | ✅ 있음 |
| **단어 바꿔 끼우기** `type-swap` | 문장은 그대로, 한 단어만 슬롯머신·줄긋기로 바뀜 ("예상 → 실제")<br>⚠ 바뀌는 단어가 둘 이상 | `change`, `compare` | — | slot-machine-roll, strikethrough-replace, kinetic-type-swap, text-state-swap, caret-swap | 📦 블록 있음 |
| **섞였다 풀리는 글자** `decode` | 글자가 무작위로 돌다가 정답으로 고정 — 숨긴 답·코드·이름 밝히기<br>⚠ 시사 채널 진지한 장면 (장난스러움) | `metric`, `ai-ask` | — | scramble-reveal, matrix-decode, split-flap-board | 📦 블록 있음 |
| **손글씨로 써지는 제목·표시** `handwritten-title` | 펜이 지나가며 글씨·밑줄·동그라미가 그려짐 (boil 로 살아 있는 선) | `point`, `open-scene` | `mijudiary`, `story`, `illust` | hw-write-title, hw-underline, hw-callout-circle, hw-arrow, hw-box-label | ✅ 있음 |
| **인용문 타자** `quote-type` | 원문 한 문장이 타자처럼 찍히고 출처 줄이 붙음, 핵심 구절만 형광펜 | `said`, `media` | `quote`, `bite` | typewriter, inline-highlight, vox-annotate | ✅ 있음 |

### 숫자·데이터 (`data`)
말한 숫자가 그 순간 화면에 생긴다 — 시장 채널의 뼈대.

| 스타일 | 어떻게 보이나 | 상황 | 우리 구현 | HyperFrames 블록 | 상태 |
|---|---|---|---|---|---|
| **큰 숫자 하나** `big-number` | 화면 가운데 숫자 하나가 세며 오르고 목표값에 '착' (expo.out), 아래에 비교 기준 한 줄<br>⚠ 비교 기준(compare_to) 없는 숫자 | `metric` | `bignum` | count-up, apple-money-count, number-wheel, number-pop-in, mk-progress-stat | ✅ 있음 |
| **숫자 칸 대시보드** `stat-tiles` | 숫자 칸 2~4개가 차례로(40~80ms) 들어오고 각 칸 숫자가 세어짐, 변화율 색<br>⚠ 5칸 이상 (한 화면 한 생각)<br>※ scripts/motion_demo.py 초안 | `metric`, `compare` | `newsdesk`, `recap` | mk-specs-list, mk-usage-arc, conic-progress-ring | ◐ 비슷한 것 |
| **선 그래프 그려지기** `line-draw` | 선이 왼쪽에서 그려지고 끝점이 따라감, 사건 시점에 깃발<br>⚠ 손그림 가짜 그래프 (실제 데이터만) | `metric`, `timeline` | `chart` | mk-line-graph, decline-chart, chart-story, data-chart | ✅ 있음 |
| **막대 비교** `bars` | 막대가 바닥에서 차례로 자라고 강조 막대만 색·살짝 튕김 | `compare`, `rank` | `bars`, `versus` | animated-bar-chart | ✅ 있음 |
| **순위 바뀌는 막대** `bar-race` | 시간이 흐르며 막대가 자리를 바꿈<br>⚠ 10초 넘게 (지루함) | `rank`, `timeline` | — | bar-chart-race | 📦 블록 있음 |
| **차트가 다른 차트로** `chart-morph` | 같은 숫자가 막대 → 비율 원 → 선으로 모양을 바꾸며 '다른 관점' | `ratio`, `change` | — | facet-morph | ○ 만들어야 |
| **사람·물건 아이콘으로 세기** `isotype` | 100명 중 몇 명이 색이 바뀜 — 비율을 몸으로 느끼게 | `ratio` | `isotype`, `people`, `parking` | stagger-lattice, grid-card-assemble | ✅ 있음 |

### 지도 (`map`)
'어디서 어디로'가 이야기의 뼈대일 때. 시사·공급망·전쟁·무역.

| 스타일 | 어떻게 보이나 | 상황 | 우리 구현 | HyperFrames 블록 | 상태 |
|---|---|---|---|---|---|
| **경로 지도 여정** `route-map` | 지도 위를 카메라가 옮겨 가며 경로 곡선이 그려지고 핀·라벨<br>⚠ 표로 보여 주기 · 매 장면 지도 | `route` | `journey` | nyc-paris-flight, us-map-flow, world-map | ✅ 있음 |
| **나라 색칠 지도** `choropleth` | 해당 나라·주가 차례로 색칠됨, 범례 한 줄 | `ratio`, `compare` | `usmap`, `choropleth` | us-map, us-map-hex, us-map-bubble, spain-map | ✅ 있음 |
| **위치 짚기** `locator` | 넓은 지도에서 한 점으로 다가가 동그라미·이름표 (장면 여는 '어디서')<br>⚠ 확대 남용 (v31) | `open-scene` | — | north-korea-locked-down, pull-back-reveal | ◐ 비슷한 것 |

### 도식·관계 (`diagram`)
원인 → 결과, 구조, 흐름. 화살표가 말과 함께 그어져야 '이어진다'가 보인다.

| 스타일 | 어떻게 보이나 | 상황 | 우리 구현 | HyperFrames 블록 | 상태 |
|---|---|---|---|---|---|
| **인과 지도** `causal-map` | 칸들이 같은 자리에 있고 말할 때마다 화살표가 그어지며 나머지는 어두워짐<br>⚠ 장면마다 새 도식 (칸 위치 유지) | `cause` | `map_causal`, `hybrid` | flowchart, constellation-hub | ✅ 있음 |
| **단계 흐름** `flow-steps` | 1→2→3 상자가 차례로 켜지고 진행 막대가 따라감 | `timeline`, `command` | `timeline`, `checklist` | flowchart-vertical, onboarding-stepper-flow, beat-timeline, marker-checklist-card | ✅ 있음 |
| **분해도·층 쌓기** `exploded` | 한 덩어리가 층별로 벌어지며 각 층 이름 (공급망 층, 비용 구조) | `ratio`, `cause` | — | exploded-stack, camera-rig-depth-stack | 📦 블록 있음 |
| **도형이 변신** `shape-morph` | 원이 쪼개지고 합쳐지고 모양을 바꿈 — 추상 개념(분산·집중·흡수) | `change` | `shape`, `analogy` | morph-swap, goo, facet-morph | ◐ 비슷한 것 |

### 그림·인물 (`illust`)
사람의 행동·마음·이야기. 호기심 채널의 몸. 동사를 그림이 연기한다.

| 스타일 | 어떻게 보이나 | 상황 | 우리 구현 | HyperFrames 블록 | 상태 |
|---|---|---|---|---|---|
| **이야기 그림판 (선으로 그려지는 장면)** `story-board` | 큰 종이 위에 말하는 순간 사람·사물이 선으로 그려지고 카메라가 이야기를 따라감 | `open-scene`, `timeline` | `story`, `story-board` | whiteboard-ink, svg-stroke-trace, outline-draw, stitched-text-draw | ✅ 있음 |
| **애니메이션 무대 (동사 연기)** `anim-stage` | 인물·물체가 걷고 떨어지고 부딪힘 — 한 화면 한 생각 | `change`, `cause` | `stage`, `anim-stage` | lottie-character-walk, pendulum-swing, physical-exit, velocity-throw-snap, spring-pop | ✅ 있음 |
| **삽화 한 장 위 카메라** `illustrated-pan` | 큰 삽화 위를 박자마다 카메라가 옮겨 가고 붓 쓸기 등장·생각 풍선 | `open-scene`, `change` | `illust`, `illustrated` | pan-stations, push-in | ✅ 있음 |
| **움직이는 비유** `metaphor` | 무리가 한쪽으로 옮겨 가고 의태어가 튀어나옴<br>※ 사용자가 고를 때만 (매뉴얼 기준 아님·품질 보완 필요) | `change`, `ratio` | `metaphor` | — | ◐ 비슷한 것 |
| **종이 콜라주 (컷아웃)** `collage` | 사진 오려 붙이기·찢긴 종이·도장이 겹겹이 — 다큐·시사의 손맛 | `media`, `open-scene` | `mijudiary`, `newspapers` | paper-collage-reveal, torn-paper-rip, halftone-field | ◐ 비슷한 것 |
| **아이소메트릭 (비스듬한 입체 도시·공장)** `isometric` | 30° 기울인 평면 입체 — 공장·데이터센터·물류를 구조로 보여 줌<br>※ 그림 자산이 필요 (art-gen 으로 조각 생성 후 조립) | `cause`, `ratio` | — | — | ○ 만들어야 |

### 사진·영상 자료 (`footage`)
증거·현장. 실사가 있으면 실사가 이긴다.

| 스타일 | 어떻게 보이나 | 상황 | 우리 구현 | HyperFrames 블록 | 상태 |
|---|---|---|---|---|---|
| **사진 천천히 움직이기** `ken-burns` | 자료 사진이 아주 느리게 확대·이동 (실수 좌표, 떨림 없이 — docs/37) | `open-scene`, `media` | `kb`, `archive` | drift-hold, push-in | ✅ 있음 |
| **사진에 깊이 (2.5D)** `parallax-photo` | 사진을 앞·뒤 층으로 나눠 카메라가 움직일 때 층이 다르게 움직임<br>⚠ 한 영상 몇 번만 (카메라 계열) | `open-scene` | — | parallax-zoom, parallax-unzoom, camera-rig-depth-stack | 📦 블록 있음 |
| **아카이브 도장** `archive-stamp` | 흑백 자료 + 시간·장소 타자기 도장 + 검은 화면 한 줄 | `open-scene`, `timeline` | `archive` | freeze-frame-dressing, grain-overlay | ✅ 있음 |
| **원본 발언 + 2단 자막** `source-bite` | 그 사람의 목소리 구간만 잘라 원문·번역 2단, 이름 자막 | `said` | `bite`, `source-cut`, `sixsigma` | lt-kicker-name, lt-clean-bar | ✅ 있음 |
| **문서·기사 캡처 형광펜** `doc-highlight` | 실제 기사·공시 캡처 위에 해당 줄만 형광펜이 그어지고 나머지 어두워짐 | `media`, `point` | `zoomshot`, `newspapers` | yt-feather-highlight, marker-highlight, ui-focus-zoom | ✅ 있음 |

### 화면·UI (`screen`)
AI·도구 사용법. 실제 화면이 증거, 모형 UI 는 보조.

| 스타일 | 어떻게 보이나 | 상황 | 우리 구현 | HyperFrames 블록 | 상태 |
|---|---|---|---|---|---|
| **AI 대화 화면** `chat` | 질문이 타자로 쳐지고 답이 흘러나옴 (스트리밍 글자) | `ai-ask` | `chat` | claude-exchange, chatgpt-exchange, ai-chat-reveal, streaming-text, typed-prompt | ✅ 있음 |
| **터미널 타자** `terminal` | 명령이 쳐지고 결과가 줄줄이 찍힘 | `command` | `terminal` | terminal-simulator, code-terminal-run, code-typing | ✅ 있음 |
| **화면 자동 줌·커서** `screen-zoom` | 실제 화면 녹화에서 클릭하는 곳으로 다가가고 커서가 강조됨 | `point`, `ai-ask` | `zoomshot`, `hookshort` | cursor-zoom-follow, agent-cursor, oversized-cursor, press-ripple, ui-focus-zoom | ✅ 있음 |
| **코드 바뀌는 부분** `code-diff` | 코드에서 바뀐 줄만 빨강→초록으로 바뀌고 나머지 흐림 | `change`, `command` | — | code-diff, code-highlight, code-morph | 📦 블록 있음 |
| **기기 틀 위 화면** `device-stage` | 노트북·휴대폰 틀 안에 화면, 살짝 기울어 들어옴<br>⚠ 제품 광고처럼 보이기 (화려한 회전) | `ai-ask` | — | browser-device-stage, device-frame-stage, multi-device-splay | 📦 블록 있음 |
| **게시물·알림 카드** `social-card` | X 게시물·댓글·알림이 튀어나와 쌓임 (발언 증거, 반응 모음) | `said`, `media` | `screenshot` | x-post, reddit-post, yt-comment-card, notification-stack, notification-cascade | ◐ 비슷한 것 |

### 정보 겹치기 (자막·이름표·표시) (`overlay`)
화면 위에 얹는 것. 내용을 돕되 주인공이 되지 않는다.

| 스타일 | 어떻게 보이나 | 상황 | 우리 구현 | HyperFrames 블록 | 상태 |
|---|---|---|---|---|---|
| **이름 자막 (로어 서드)** `lower-third` | 화면 아래 이름·직함이 선과 함께 밀려 들어오고 3~4초 뒤 퇴장 | `said` | `bite`, `sixsigma` | lt-kicker-name, lt-side-rule, lt-accent-underline, lt-dark-card, yt-lower-third | ✅ 있음 |
| **큰 자막 (쇼츠)** `big-caption` | 말하는 순간 바뀌는 큰 자막, 핵심어만 색 | `conclusion` | `hookshort`, `presenter`, `shorts-aitips` | caption-highlight, caption-pill-karaoke, caption-editorial-emphasis, caption-weight-shift | ✅ 있음 |
| **출처 줄** `source-line` | 화면 구석 작은 '출처: …' — 숫자·인용마다 | `metric`, `said`, `media` | `newsdesk`, `sixsigma` | — | ✅ 있음 |
| **가리키는 표시** `callout` | 동그라미·화살표·밑줄이 말과 함께 그려짐 | `point` | `zoomshot` | yt-circle-pointer, cursor-annotate, hw-callout-circle, mk-callout-highlight | ✅ 있음 |
| **뉴스 띠** `ticker` | 아래쪽 흐르는 띠·속보 표시<br>⚠ 매일 브리핑 외에는 산만함 | `media` | — | news-ticker, ticker-takeover | 📦 블록 있음 |

### 장면 이어 주기 (`transition`)
장면과 장면 사이. 눈에 띄지 않는 것이 기본 — 화려한 전환은 피드백과 부딪힌다(v12 '정신없다').

| 스타일 | 어떻게 보이나 | 상황 | 우리 구현 | HyperFrames 블록 | 상태 |
|---|---|---|---|---|---|
| **그냥 자르기 (박자 위에서)** `cut` | 움직임이 가장 빠른 프레임에서 자름, 방향·속도가 이어지게 | `conclusion`, `change` | `all` | — | ✅ 있음 |
| **겹쳐 바뀌기** `crossfade` | 0.3~0.5초 겹쳐 사라짐 — 장 바뀜·시간 흐름 | `timeline` | `chapter`, `edit10.py` | fade-through, transitions-dissolve | ✅ 있음 |
| **같은 것이 다음 화면으로** `match-move` | 앞 장면의 숫자·도형이 그대로 다음 장면 자리로 옮겨 가며 장면이 바뀜 | `change`, `cause` | — | match-cut, text-match-cut, type-match-cut, morph-swap | 📦 블록 있음 |
| **밀어내기·닦기** `wipe` | 한 방향으로 새 장면이 밀고 들어옴 (비교 '이전 → 이후') | `compare`, `change` | — | before-after-wipe, directional-wipe, page-slide, panel-reveal, curtain-reveal | 📦 블록 있음 |
| **화려한 전환 (휙·글리치·셰이더)** `flashy` | 휩 팬·글리치·빛 번짐·소용돌이<br>⚠ 기본으로 쓰지 않음 (v12 '정신없다', v31 확대 금지) | — | — | whip-pan, glitch, light-leak, swirl-vortex, cinematic-zoom | ⏸ 보류 |

### 배경·질감·카메라·3D (`world`)
바탕과 공기. 채널 정체성(시사 증거판·시장 대시보드·호기심 칠판·AI 앱 창)을 만든다.

| 스타일 | 어떻게 보이나 | 상황 | 우리 구현 | HyperFrames 블록 | 상태 |
|---|---|---|---|---|---|
| **종이·칠판 질감** `paper-bg` | 구겨진 종이·칠판·격자 노트 — 손그림 계열의 바탕 | `all` | `mijudiary`, `story-board`, `skins` | grain-field, halftone-field | ✅ 있음 |
| **어두운 대시보드 바탕** `dark-dashboard` | 어두운 남색 + 은은한 중심 빛 + 격자선 — 시장·AI 채널 | `metric`, `compare` | `newsdesk`, `identity` | mesh-gradient-bg, vignette, grain-overlay | ✅ 있음 |
| **아주 느린 카메라** `slow-camera` | 박자 하나 내내 1~3% 확대·이동 (sine.inOut) — 정지 화면에 숨<br>⚠ 빠른 확대·줌인 전환 (v31) | `all` | `identity`, `edit10.py` | drift-hold, push-in, rack-focus | ✅ 있음 |
| **어두운 스튜디오 3D 물체** `studio-3d` | 칩·서버·지폐 같은 물체가 조명 아래 천천히 돎<br>⚠ 정보 없이 멋만 (한 영상 1~2번) | `open-scene`, `conclusion` | `studio3d` | product-turntable, ui-3d-reveal, chrome-orb | ✅ 있음 |
| **추상 움직이는 배경 (셰이더)** `abstract-bg` | 오로라·물결·입자 — 장 표지·쇼츠 훅 뒤<br>⚠ 글자 뒤에서 대비를 깎음 · 정보 화면 뒤 | `question` | — | aurora, flowing-gradient, mesh-gradient, plasma | 📦 블록 있음 |

## 5. 다음에 붙일 것 (📦·○)
먼저: 상황 표의 1순위인데 아직 없는 것 → 그다음 채널 얼굴에 들어 있는 것.

- **단어 바꿔 끼우기** (글자 (키네틱 타이포), 📦 블록 있음) — slot-machine-roll, strikethrough-replace, kinetic-type-swap · *상황 1순위*
- **순위 바뀌는 막대** (숫자·데이터, 📦 블록 있음) — bar-chart-race · *상황 1순위*
- **섞였다 풀리는 글자** (글자 (키네틱 타이포), 📦 블록 있음) — scramble-reveal, matrix-decode, split-flap-board
- **분해도·층 쌓기** (도식·관계, 📦 블록 있음) — exploded-stack, camera-rig-depth-stack
- **사진에 깊이 (2.5D)** (사진·영상 자료, 📦 블록 있음) — parallax-zoom, parallax-unzoom, camera-rig-depth-stack
- **코드 바뀌는 부분** (화면·UI, 📦 블록 있음) — code-diff, code-highlight, code-morph
- **기기 틀 위 화면** (화면·UI, 📦 블록 있음) — browser-device-stage, device-frame-stage, multi-device-splay
- **뉴스 띠** (정보 겹치기 (자막·이름표·표시), 📦 블록 있음) — news-ticker, ticker-takeover
- **같은 것이 다음 화면으로** (장면 이어 주기, 📦 블록 있음) — match-cut, text-match-cut, type-match-cut
- **밀어내기·닦기** (장면 이어 주기, 📦 블록 있음) — before-after-wipe, directional-wipe, page-slide
- **추상 움직이는 배경 (셰이더)** (배경·질감·카메라·3D, 📦 블록 있음) — aurora, flowing-gradient, mesh-gradient
- **차트가 다른 차트로** (숫자·데이터, ○ 만들어야) — facet-morph
- **아이소메트릭 (비스듬한 입체 도시·공장)** (그림·인물, ○ 만들어야) — 블록 없음

## 6. 그림체 (애니메이션 스타일) — 두 번째 축
위 §4 는 **무엇을** 그리나(글자·숫자·지도…), 여기는 **어떤 그림체로** 그리나. 둘을 곱해 화면 하나: 예) 숫자·데이터 × 아이소메트릭, 그림·인물 × 클레이.
견본: `python scripts/motion_styles_reel.py` — 같은 장면(동전이 떨어져 성장 탑이 쌓인다)을 12가지 그림체로 렌더 (43초, 1080p).
'끊는 움직임'(⏯)은 일부러 프레임을 끊는 그림체라 `motion-qa` 의 멈칫·점프가 정상이다.

| 그림체 | 생김새 | 언제 | 채널 | 제작 부담 | 상태 |
|---|---|---|---|---|---|
| **플랫 2D** `flat` | 단순한 면·그림자 없는 색 면<br>⚠ 흔해서 개성은 색·비율로 | 무엇이든 — 가장 흔한 설명 애니메이션 | curiosity, market, ai | 낮음 | ✅ 있음 · 우리: `stage`, `anim-stage` |
| **라인 아트 (모노라인)** `line` | 같은 굵기 선만·면 없음 | 기술·개념·구조 설명, 선이 그려지는 과정이 곧 설명 | ai, market | 낮음 | ✅ 있음 · 우리: `chart`, `map_causal` |
| **화이트보드 손그림** `whiteboard` | 떨리는 펜 선(boil 8fps)·손글씨 ⏯ | 강의·원리·긴 해설을 싸게 | curiosity | 낮음 | ✅ 있음 · 우리: `mijudiary`, `story-board`, `illust` |
| **아이소메트릭** `isometric` | 30° 비스듬한 입체 블록 | 공장·도시·데이터센터·공급망의 '구조' | market, issues, ai | 중간 | ○ 만들어야 |
| **리퀴드 모션** `liquid` | 물방울이 합쳐지고 늘어남 (goo 필터)<br>⚠ 정보 전달보다 분위기 — 한 영상 1~2번 | 흐름·흡수·합병·자금 유입, 장 표지 | market | 중간 | ○ 만들어야 |
| **종이 컷아웃 (스톱모션)** `paper` | 종이 질감·그림자·두 프레임에 한 번 끊는 움직임 ⏯ | 따뜻한 이야기·옛 사례·시사의 손맛 | curiosity, issues | 중간 | ✅ 있음 · 우리: `newspapers` |
| **2.5D 시차** `parallax` | 평면 그림 층이 카메라에 따라 다르게 움직여 깊이<br>⚠ 카메라 계열 — 한 영상 몇 번 (v31) | 장면 열기·풍경·사진에 공간감 | issues, curiosity | 중간 | 📦 블록 있음 |
| **픽셀 / 8비트** `pixel` | 큰 네모 픽셀·칸 단위 이동<br>⚠ 진지한 시사·시장엔 맞지 않음 ⏯ | 레트로·게임·가벼운 쇼츠 | ai | 낮음 | ○ 만들어야 |
| **네온 글로우** `neon` | 어두운 바탕에 빛나는 선<br>⚠ 정보 많은 화면은 눈이 피곤 ⏯ | AI·테크·밤·데이터 흐름 | ai | 낮음 | ○ 만들어야 |
| **하프톤 레트로 인쇄** `halftone` | 망점·색 어긋남(CMYK) | 옛 신문·만화·경제사, 시대 표시 | issues, market | 낮음 | 📦 블록 있음 · 우리: `archive` |
| **3D (CSS·three.js)** `css3d` | 진짜 입체가 회전 | 제품·물체·데이터 구조를 돌려 보기 | ai, market | 중간~높음 | ✅ 있음 · 우리: `studio3d` |
| **클레이 (말랑한 입체)** `clay` | 부푼 입체 + 크게 눌리고 튕김(스쿼시·스트레치) | 친근·귀여움·생활·캐릭터 감정 | curiosity | 중간 | ○ 만들어야 |

## 출처
- HyperFrames 레지스트리 0.8.190 (`hyperframes catalog --json`, 448개, Apache-2.0) — 블록 이름은 `hyperframes add <이름>` 로 설치
- 모션그래픽 스타일 분류: [b2w — 12 motion graphics styles](https://www.b2w.tv/blog/types-of-motion-graphics), [Yans Media — motion graphics styles](https://www.yansmedia.com/blog/best-motion-graphics-styles), [Yans Media — types & use cases](https://www.yansmedia.com/blog/types-of-motion-graphics), [ManyPixels — 9 types](https://www.manypixels.co/blog/motion-design/types), [Blue Forest — animation styles](https://blueforeststudios.squarespace.com/definitive-guide-to-animation-styles), [Biteable — animation styles](https://biteable.com/blog/animation-styles-types/), [moonb — 12 animation styles](https://www.moonb.io/blog/animation-styles), [Yum Yum Videos — animation styles](https://www.yumyumvideos.com/types_of_animation_styles)
  - 공통 결론: 글자(키네틱)·화이트보드가 가장 싸고 빠름, 인포그래픽은 숫자·보고서, 아이소메트릭은 복잡한 구조, 2.5D 는 3D 의 싼 대안(층 나누기가 가장 어려움). 대부분 제작사 블로그라 홍보 성격이 있다.
- 설명형 유튜브 채널의 화면 문법(지도 설명·일관된 일러스트): [Johnny Harris 의 시각 이야기](https://medium.com/@LMK_writing/how-johnny-harris-mastered-visual-storytelling-on-youtube-343ddf9160ec), [Vox 식 지도 애니메이션](https://rizzle.com/blog/post/how-to-create-an-engaging-map-animation-channel-like-vox-youtube), [Digiday — 설명 영상](https://digiday.com/media/publishers-flocking-explainer-videos/), [vidpros — 설명 채널](https://vidpros.com/best-explainer-youtube-channels/) — 레퍼런스 채널의 그림·캐릭터는 복제하지 않고 구조만 (AGENTS 스타일 규칙)

