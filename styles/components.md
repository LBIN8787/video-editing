<!-- scripts/components_doc.py 가 만든 파일 — 목록(styles/components.yaml·techniques.yaml)을 고친 뒤 다시 만드세요 -->
# 구성요소별 만드는 법 — 화면·글자·그래픽·카메라·전환·소리

> 사용자 2026-11-20: "다른 목록들도 마찬가지로 해줘" — 영상 = 구성요소 카테고리마다 고른 스타일의 조합(`styles/components.yaml`).
> **움직이는 예시**: 화풍 목록 페이지(https://claude.ai/artifact/K4CRgsyTYsWGCDw5RoCtam) 의 카테고리 칸 ▶ (`media` 열의 영상). 장면 종류는 `styles/hybrid/scenes/`, 화풍은 `styles/looks/README.md`.

고르는 법: `python -m ytflow look <프로젝트> --set <카테고리>=<id>` → `edit.yaml` 의 `look` (이 영상의 기본값, 장면마다 바꿀 수 있음).

## 화면 화풍 (그래픽 팩) (`motion`)

바탕색·글꼴·선·자막 상자를 한 벌로 — 도형·글자·막대가 '어떻게 보이나'

→ 화풍 목록 `styles/looks.yaml` 의 `motion` — 만드는 법은 `styles/looks/README.md`.

## 바탕 (`background`)

장면 목적에 맞춰 바뀌는 뒷배경 (manual/05 §0-2·§0-6) — 정지한 한 장

| id | 이름 | 어떻게 보이나 | 언제 | 구현·값 | 예시 |
|---|---|---|---|---|---|
| `film` | 필름 알갱이 | 팩 기본 바탕에 옅은 필름 입자 | 대부분의 장면 (기본) | backdrop.py | `bg/film.jpg` |
| `grid` | 모눈 | 옅은 모눈 — 숫자·차트용 | 막대·차트·맞대기·연표·사람 수 | backdrop.py | `bg/grid.jpg` |
| `spot` | 가운데 조명 | 가운데가 밝고 가장자리가 어두움 | 인용·발언·큰 숫자 | backdrop.py | `bg/spot.jpg` |
| `tint` | 장마다 색 기운 | 장(chapter)마다 다른 옅은 색 | 비유·체크리스트·인과 지도 | backdrop.py | `bg/tint.jpg` |
| `photo` | 흐린 자료 사진 | 그 편의 자료 사진을 흐리게 깔기 | 마무리·키네틱 (사진이 있을 때) | backdrop.py | `bg/photo.jpg` |
| `duotone` | 듀오톤 사진 | 카테고리 두 색으로 칠한 사진 | 장 표지 (v15) | backdrop.make_identity | `bg/duotone.jpg` |
| `cork` | 코르크 증거판 | 갈색 코르크 판 | 시사 — 누가 누구와 연결돼 있나 | backdrop.make_identity | `bg/cork.jpg` |
| `chalk` | 칠판 | 녹회색 칠판과 분필 자국 | 호기심 — 원리를 배운다 | backdrop.make_identity | `bg/chalk.jpg` |
| `dash` | 대시보드 모눈 | 남색 모눈과 연결점 | 시장 — 숫자로 시작하는 장 | backdrop.make_identity | `bg/dash.jpg` |
| `glow` | 은은한 빛 | 움직이지 않는 부드러운 빛 | AI 앱 창·사진이 없을 때 듀오톤 대신 | backdrop.make_identity | `bg/glow.jpg` |

## 장 표지 (`chapter`)

장(chapter)이 바뀔 때의 표지 — 카테고리마다 모양이 다름 (v15)

| id | 이름 | 어떻게 보이나 | 언제 | 구현·값 | 예시 |
|---|---|---|---|---|---|
| `board` | 증거판 표지 | 코르크 위 핀 꽂은 장 제목 카드 | 시사·시장 (관계 이야기) | identity.chapter_board | `scenes/chapter-board.mp4` |
| `dash` | 대시보드 표지 | 남색 모눈 + CHAPTER 숫자 | 시장 — 다음 장이 숫자로 시작할 때 | identity.chapter_dash | `scenes/chapter-dash.mp4` |
| `photo` | 듀오톤 사진 표지 | 주제 사진을 두 색으로 | 자료 사진이 있는 장 (기본) | edit10.chapter_photo | `scenes/chapter-photo.mp4` |
| `chalk` | 칠판 표지 | 칠판에 분필 제목 | 호기심 — 원리를 배운다 | identity.chapter_chalk | `scenes/chapter-chalk.mp4` |
| `window` | 앱 창 표지 | 은은한 빛 위에 뜬 창 + 탭 이름 | AI — 제품·도구 이야기 | identity.chapter_window | `scenes/chapter-window.mp4` |
| `paper` | 종이 한 장 표지 | 종이가 밀려 들어오며 제목 | 손그림 종이 팩 | hybrid.s_chapter | `scenes/chapter-paper.mp4` |
| `type` | 큰 글씨 표지 | 화면 가득 큰 글씨 | 평면 팩 | graphics.chapter_type | `scenes/chapter-type.mp4` |
| `two-line` | 두 줄 표지 | 작은 흰 줄 다음 큰 강조색 줄 | 앞 장 결론 → 다음 질문 | uiflow | — |

## 관계 그림의 모양 (`structure`)

인과·관계 지도를 카테고리에 맞는 모양으로 (v15 identity.structure)

| id | 이름 | 어떻게 보이나 | 언제 | 구현·값 | 예시 |
|---|---|---|---|---|---|
| `board` | 증거판 (시사·시장) | 코르크에 핀 꽂은 카드와 붉은 실 | 누가 누구와 연결돼 있나 | identity.py board | `scenes/board-evidence.mp4` |
| `chalk` | 칠판 (호기심) | 칠판 위 분필 화살표와 칸 | 원리·과정 | identity.py chalk | `scenes/chalk-causal.mp4` |
| `paper` | 종이 손그림 인과 지도 | 종이 위 손그림 칸과 화살표 | 스페인독감 편처럼 종이 팩 | hybrid.s_map_causal | `scenes/map_causal-paper.mp4` |

## 그림 모양 (비교·비율·흐름) (`slots`)

같은 숫자를 팩마다 다른 그림으로 — 비교는 막대/그림 기호, 비율은 사람/네모 칸/도넛, 흐름은 상자/알약/포스트잇

| id | 이름 | 어떻게 보이나 | 언제 | 구현·값 | 예시 |
|---|---|---|---|---|---|
| `compare-bars` | 비교 — 막대 | 가로 막대 | 평면·슬레이트 팩 | graphics.py compare | `scenes/compare-bars.mp4` |
| `compare-pictogram` | 비교 — 그림 기호 | 사물 아이콘 줄 | 어두운 다큐·포레스트·청사진 팩 | graphics.py compare | `scenes/compare-pictogram.mp4` |
| `proportion-people` | 비율 — 사람 100명 | 100명 중 N명 색칠 | 사람 수로 느끼게 | graphics.py proportion | `scenes/proportion-people.mp4` |
| `proportion-waffle` | 비율 — 네모 칸 | 100칸 중 N칸 | 평면·신문지 팩 | graphics.py proportion | `scenes/proportion-waffle.mp4` |
| `proportion-donut` | 비율 — 도넛 | 고리 그래프 | 미드나이트·어두운 팩 | graphics.py proportion | `scenes/proportion-donut.mp4` |
| `flow-sticky` | 흐름 — 포스트잇 | 포스트잇 칸과 선 | 어두운 다큐·포레스트 | graphics.py flow | `scenes/flow-sticky.mp4` |
| `flow-pill` | 흐름 — 둥근 알약 | 알약 모양 칸 | 평면·슬레이트·미드나이트 | graphics.py flow | `scenes/flow-pill.mp4` |

## 삽화 화풍 (`illust`)

실사도 모션그래픽도 어려운 박자에 부분적으로 쓰는 그림의 그림체

→ 화풍 목록 `styles/looks.yaml` 의 `illust` — 만드는 법은 `styles/looks/README.md`.

## 실사 색보정 (`footage`)

인물 실사 소스영상을 한 편 안에서 같은 색으로 묶는 보정

→ 화풍 목록 `styles/looks.yaml` 의 `footage` — 만드는 법은 `styles/looks/README.md`.

## 글꼴 (`font`)

제목·숫자·상자·메모·라벨 칸마다 팩이 고르는 글꼴 (ytflow/assets/fonts)

| id | 이름 | 어떻게 보이나 | 언제 | 구현·값 | 예시 |
|---|---|---|---|---|---|
| `gothic` | 나눔고딕 | 또렷한 고딕 — 자막·상자·라벨 | 거의 모든 팩의 상자·자막 | `'Nanum Gothic'` 700 | — |
| `gothic-x` | 나눔고딕 ExtraBold | 굵은 고딕 — 제목·큰 숫자 | 평면·하얀 평면·미드나이트·키네틱 포스터 제목 | `'Nanum Gothic'` 800 | — |
| `myeongjo` | 나눔명조 ExtraBold | 무게 있는 명조 — 제목·숫자 | 어두운 다큐·증거판·포레스트·슬레이트·신문지·종이 손그림 제목 | `'Nanum Myeongjo'` 800 | — |
| `pen` | 나눔손글씨 펜 | 손글씨 — 메모·주석·칠판 글씨 | 칠판 팩 전체 | `'Nanum Pen Script'` 400 | — |
| `blackhan` | 검은고딕 (Black Han Sans) | 아주 굵은 제목체 | 설명 무대(explain) 제목·숫자 | `'Black Han Sans'` 400 | — |

## 자막 모양 (`subtitle`)

아래 자막의 상자·색·위치 (팩의 subtitle, media.py)

| id | 이름 | 어떻게 보이나 | 언제 | 구현·값 | 예시 |
|---|---|---|---|---|---|
| `box-navy` | 남색 반투명 상자 | 흰 글씨 + 남색 상자 | 종이·평면 팩 (기본) | bg=rgba(30,42,68,.6), color=#fff, pos=bottom | — |
| `box-black` | 검은 반투명 상자 | 흰 글씨 + 검은 상자 | 어두운 팩 | bg=rgba(0,0,0,.6), color=#fff, pos=bottom | — |
| `amber` | 호박색 글씨 | 호박색 글씨 + 어두운 상자 | 어두운 다큐 팩 | bg=rgba(30,30,30,.55), color=#FFE684, pos=bottom | — |
| `top-dark` | 위쪽 진한 글씨 | 화면 위쪽 진한 글씨 (머니크루식) | 무늬 없는 미색 인포그래픽 | bg=transparent, color=#1E2A44, pos=top | — |
| `two-line` | 원문·번역 2단 | 위에 작은 원문 | 인용·원본 발언(bite) | bg=rgba(0,0,0,.6), color=#fff, pos=bottom, orig=True | — |
| `shorts-big` | 쇼츠 큰 자막 | 큰 흰 글씨 + 검은 테두리 | 훅 쇼츠·말하는 사람 쇼츠 | bg=transparent, color=#fff, pos=mid, outline=True | — |
| `hidden` | 자막 숨김 | 화면 글자가 곧 자막 | 키네틱 포스터 팩 | hidden=True | — |

## 장면 종류 (`scene`)

한 장면의 뼈대 — 지금까지 영상에 쓴 장면을 진짜 렌더러로 그린 예시 (manual/usage.yaml)

→ 장면 종류마다 `styles/hybrid/scenes/<장면>.md` (박자표·대본 예·예시 영상), 실제 완성본 예시는 `real-examples.md`.

## 장면 위 겹치기 (`layer`)

장면 하나 위에 층을 하나 더 얹기 (directions.apply_layers)

| id | 이름 | 어떻게 보이나 | 언제 | 구현·값 | 예시 |
|---|---|---|---|---|---|
| `photo` | 액자 사진 | 장면 한쪽에 자료 사진 액자 | 글씨·도형뿐인 장면이 길 때 (시장 §6) | directions.py | `scenes/layer-photo.mp4` |
| `locator` | 위치 미니 지도 | 구석의 작은 지도에 위치 점 | 나라·도시가 나올 때 | directions.py | `scenes/layer-locator.mp4` |
| `stamp` | 타자기 날짜 도장 | 날짜·장소가 타자기로 찍힘 | 자료 화면의 시점·장소 | directions.py | `scenes/layer-stamp.mp4` |
| `mark` | 표시 (동그라미·밑줄·화살표) | 손그림 표시가 그려짐 | 화면의 한 곳을 가리킬 때 | directions.py | `scenes/layer-mark.mp4` |
| `number` | 큰 숫자 카드 | 장면 위에 큰 숫자 카드 | 숫자 하나를 각인 · 피함: 이 층이 쓰는 저음 효과음(impact-bass)은 사용자 판정으로 쓰지 않음 | directions.py | `scenes/layer-number.mp4` |
| `words` | 핵심 단어 | 장면 위에 낱말이 박힘 | 핵심어 하나 | directions.py | — |
| `line` | 하단 타자 한 줄 | 아래쪽에 한 줄이 타자로 | 자료 화면의 설명 한 줄 | directions.py | — |

## 장면 안 효과 (`fx`)

장면 전체에 얹는 움직임·질감 (directions.FX) — 시장 채널은 확대·스캔 끔

| id | 이름 | 어떻게 보이나 | 언제 | 구현·값 | 예시 |
|---|---|---|---|---|---|
| `tilt` | 기울여 다가가기 (hold) | 화면이 살짝 기울며 다가옴 | 호기심·시사 (시장은 끔 v31) |  | `scenes/fx-tilt.mp4` |
| `dolly` | 앞으로 미끄러지기 (hold) | 카메라가 천천히 앞으로 | 호기심·시사 (시장은 끔 v31) |  | `scenes/fx-dolly.mp4` |
| `scan` | 빛 훑기 (스캔) (hold) | 빛줄기가 훑고 지나감 | — · 피함: 사용자 판정으로 뺌 (v32 "상황에 안 맞고 과해요") |  | `scenes/fx-scan.mp4` |
| `dust` | 먼지 입자 | 떠다니는 먼지 | 옛 자료·역사 (한 편 2장면까지) |  | `scenes/fx-dust.mp4` |
| `leak` | 빛 번짐 | 필름 빛 번짐이 지나감 | 회상·전환 (한 편 2장면까지) |  | `scenes/fx-leak.mp4` |
| `photofill` | 사진 채우기 | 사진이 장면 뒤를 채움 | 큰 숫자 뒤 맥락 |  | `scenes/fx-photofill.mp4` |

## 말에 맞춰 생기는 사물 (박자 motion) (`beat`)

내레이션이 그 낱말을 말하는 순간 화면에 생기는 것 (motion2.py, 시장 §6 v27)

| id | 이름 | 어떻게 보이나 | 언제 | 구현·값 | 예시 |
|---|---|---|---|---|---|
| `count` | 숫자 세기 | 말한 숫자가 굴러 올라감 | 화면에 없는 숫자를 말할 때 |  | `scenes/motion-count.mp4` |
| `icon` | 사물 아이콘 | 말한 사물(은행·공장 …) 아이콘이 생김 | 주체·사물 |  | `scenes/motion-icon.mp4` |
| `arrow` | 화살표 | 둘 사이에 화살표가 그려짐 | 이동·영향 |  | `scenes/motion-arrow.mp4` |
| `out` | 빠져나감 | 요소가 밖으로 빠져나감 | 유출·감소 |  | `scenes/motion-out.mp4` |
| `check` | 체크 | 체크 표시가 찍힘 | 확인한 것 |  | `scenes/motion-check.mp4` |
| `anchor` | 기준선 | 기준선이 생기고 값이 거기에 붙음 | 기준 대비 |  | `scenes/motion-anchor.mp4` |
| `pulse` | 맥박 | 지금 말하는 칸이 한 번 뜀 | 지금 여기 |  | `scenes/motion-pulse.mp4` |
| `folder` | 폴더·파일 | 폴더·파일이 생김 | 문서·자료 이야기 |  | — |
| `gear` | 톱니 | 톱니가 돎 | 작동 원리 |  | — |
| `type` | 타자 | 낱말이 타자로 찍힘 | 이름·용어 |  | — |

## 글자 연출 (`text`)

제목·숫자·핵심어가 어떻게 나타나나

| 기법 | 상태 | 어떻게 보이나 | 언제 | 주의 | 만드는 법 |
|---|---|---|---|---|---|
| 글자 쪼개 등장 (SplitText) | partial | 제목·핵심 한 줄이 아래에서 낱말씩 떠오르며 완성됨 | 장 표지 제목, 결론 한 문장, 쇼츠 훅 — 한 영상에 몇 번만 | 강조 예산(1분 1번, v4) 안에서. 자막과 같은 문장을 다시 띄우지 않음 (v4 기각) | GSAP SplitText(gsap 3.13 에 포함, 무료) 로 글자 묶음을 만들고 stagger 로 차례 등장 — 지금 kinetic 은 낱말 단위만 직접 나눔 |
| 글자 섞였다 풀리기 (스크램블) | candidate | "#%A9..." 가 "631억" 으로 굳어짐 — 해독되는 느낌 | 숫자·코드·이름이 '밝혀지는' 순간 (AI 채널 명령어, 시장의 발표 숫자). 한 영상 1~2번 | 정보형 장면에선 읽기 방해 — 결과가 바로 읽혀야 하는 표에는 쓰지 않음 | GSAP ScrambleTextPlugin(무료) — 박자 시각에 맞춰 0.6~1초 |
| 숫자 세며 오르기 (카운트업) | have | 0 → 631억 이 1초 동안 굴러 올라감 | 크기를 느끼게 할 숫자 하나 — 말하는 순간에 맞춰 (beat-motion 의 count) |  | 지금 bignum·motion count 가 GSAP 로 구현. 바깥 도구가 필요하면 countUp.js(MIT) |
| 손그림 형광펜·밑줄·괄호 (차례로) | partial | 기사 캡처의 한 줄에 노란 형광펜이 쓱 칠해지고, 이어서 옆 숫자에 동그라미 | 증거(기사·공시·논문 캡처)에서 '여기' 를 가리킬 때 — 말하는 순간 | 한 화면에 표시 2개까지 (강조 예산) | 지금 layers mark(rough.js)가 동그라미·밑줄을 그림. rough-notation 은 같은 rough.js 바탕에 highlight·bracket·strike-through·묶음 순서(annotationGroup)를 더함 |
| 두 줄 장 표지 | have | 작은 흰 줄 다음 큰 강조색 줄이 뜸 | 앞 장의 결론에서 다음 질문으로 넘어가는 자리 | 매 장면에 반복하지 않고 읽을 시간·배경 대비를 확보 | chapter 장면 look: two-line, kicker·title·clip 사용 — docs/43-reference-pickle-explainer.md §6 |

## 그래픽 연출 (`graphic`)

사물·도형·데이터·관계가 어떻게 움직이며 설명하나

| 기법 | 상태 | 어떻게 보이나 | 언제 | 주의 | 만드는 법 |
|---|---|---|---|---|---|
| 선이 그려지기 (드로우 온) | have | 인과 지도의 화살표가 A 에서 B 로 그어짐 | 연결·흐름·경로를 말할 때 — '이것이 저것으로 이어진다' |  | 지금 hybrid·story 가 rough.js 선을 stroke-dashoffset 으로 그림. GSAP DrawSVGPlugin(무료)·vivus(MIT) 도 같은 원리 |
| 모양 바뀌기 (모프) | candidate | 동그라미(회사) 가 지도 모양(나라)으로, 막대가 사람 모양으로 스르르 바뀜 | "A 가 사실은 B 다", "이것이 저것이 된다" — 말의 동사(바뀌다·변하다)를 그림이 연기할 때 (04 §0-5) | 의미 없는 모프는 장식 — 바뀌는 이유를 대본이 말할 때만 | GSAP MorphSVGPlugin(무료) 또는 flubber(MIT) 로 SVG 경로 보간 → 박자 시각에 1초 안팎 |
| 차례로 등장 (스태거) | have | 사람 아이콘 10개가 왼쪽부터 톡톡톡 채워짐 | 목록·사람 수·여러 항목 — 눈이 하나씩 따라가게 |  | GSAP stagger (지금 isotype·people 등에서 사용). Manim 의 LaggedStart 와 같은 개념 |
| 길 따라 움직이기 (모션 패스) | partial | 공급망 지도 위로 컨테이너 아이콘이 대만 → 미국 길을 따라 미끄러짐 | 공급망·자금 흐름·전파 — '어디서 어디로' |  | journey 는 경로를 그리고 핀을 찍음. GSAP MotionPathPlugin(무료) 로 아이콘을 경로에 태움 |
| 순위가 바뀌는 막대 (바 차트 레이스) | candidate | 2015 → 2025 시가총액 순위에서 엔비디아 막대가 아래에서 1위로 올라옴 | 순위·점유율이 시간에 따라 바뀐 이야기 (시장) — 데이터 출처 필수 | 숫자가 많아 읽기 바쁨 — 막대 10개 이하, 15초 안팎 | HyperFrames bar-chart-race 블록(설치됨) 또는 Python dexplo/bar_chart_race(MIT) 로 영상 조각 |
| 차트가 다른 차트로 바뀜 | candidate | 매출 막대 5개가 모여 하나의 원이 되며 비중이 보임 | "그런데 비중으로 보면" 처럼 관점이 바뀌는 문장 |  | 각 막대·조각을 SVG 경로로 그리고 MorphSVG(무료)·flubber(MIT) 로 보간 |
| 나란히 맞대기 (스플릿 스크린) | partial | 왼쪽엔 CEO 발언 자막, 오른쪽엔 같은 날 공시 문장 — 말과 행동이 나란히 | 시장 v26 '말과 행동 맞대기', 시사 '양쪽 입장 같은 틀(08 §4)' | 양쪽 크기·색·길이를 같게 (한쪽 편들기 금지 — 영구 원칙) | versus·compare 는 도식으로 비교. 영상·캡처 두 개를 나란히 놓는 장면은 layers 두 칸 배치로 확장 |
| 나머지 어둡게 (스포트라이트) | have | 인과 지도 칸 7개 중 지금 말하는 칸만 진하고 나머지는 옅어짐 | 복잡한 도식에서 지금 어디를 보는지 알려 줄 때 — 카메라 이동 대신 |  | map_causal 의 dim·on·active 상태 (hybrid.py) |
| 카드 상태 변화 | have | 같은 카드가 대기 → 진행 → 성공·실패로 바뀜 | 예약·결제·처리 결과가 시간 순서로 달라지는 박자 | 실제 화면이 있으면 먼저 보여 주고, 목업에는 연출 고지를 유지 | statecard 장면 cards·hub와 박자 show·state·text 사용 — docs/43-reference-pickle-explainer.md §6 |
| 연결선 끊김 | have | 이미 그린 선을 빨간 점선과 X로 바꿔 차단을 남김 | 서비스 차단·흐름 중단처럼 연결이 실패하는 순간 | 실패가 확인된 연결에만 쓰고 빨강과 X를 함께 사용 | statecard 박자 cut: [카드id], map_causal 박자 cut: [[출발id,도착id]] — docs/43-reference-pickle-explainer.md §6 |
| 실사 위 요청 칩 | have | 실사 위에 짧은 요청 칩이 차례로 떠오름 | 같은 장소의 여러 요청·사용 사례를 소개할 때 | 얼굴·핵심 동작·자막을 가리지 않게 위치 조정; 실제 발언처럼 보이는 예시에는 고지 | footage 박자 chips 배열과 chip_gap 사용 — docs/43-reference-pickle-explainer.md §6 |
| 문서 스포트라이트 | have | 본문 나머지를 어둡게 하고 읽는 문단만 밝게 남김 | 기사·공식 문서에서 근거 문장을 짚을 때 | 원문·출처를 확인; 텍스트 재구성은 실제 캡처와 구별; 어둡힌 문단 대비 경고는 수동 검토 | docspot 장면 paras 또는 img, 박자 spot·mark·num 사용 — docs/43-reference-pickle-explainer.md §6 |
| 사건 이후 누적 (시간선 + 쌓이는 카드) | have | 제재 표식 → 붉은 붓 구간이 오른쪽으로 칠해짐 → 칩 카드 1·2·3…6 이 같은 간격으로 내려앉음 → '6개 버전 이상' | 사건 뒤에도 계속됐다 · 그 이후 몇 번 — 시간 조건과 수량을 한 화면에 | 카드 간격은 시간 간격이 아니라 개수 (날짜를 붙이지 않는 한). 보고서 주장이면 제목에 출처 | ytflow/stages/explain.py s_afterline — 박자 show[event·after·items·headline], at 으로 말하는 단어에 |
| 두 값 사이 간격 (괄호·점선 기준) | have | 원유 → 공장 → 휘발유, 두 막대, 점선, '정제마진' 괄호, 제품값이 내려가며 간격이 좁아짐 | 두 값의 차이가 이름을 가진 개념일 때 — 마진·스프레드·괴리·차익 | 단순화한 설명 모델이면 '예시 값'·'개념도'를 표시 | ytflow/stages/explain.py s_spread — show[steps·low·high·diff·change] |
| 전체 중 몫 (채워지는 막대 + 비교 눈금) | have | 흰 막대 → 중국·홍콩, 싱가포르가 차례로 채워짐 → 3분의 1 점선 → '합치면 3분의 1 넘게' | 전체 중 얼마를 차지하나, 합치면 기준을 넘나 | 분모(무엇의 100%인지)를 화면에 남김 | ytflow/stages/explain.py s_share — show[total·p0…·mark·sum] |
| 자유 무대 (인물·물체가 움직이며 설명) | have | 초기 투자자 → '보호예수 해제' → 주식 카드가 옮겨 감 → 새 투자자 등장·화살표 '매도' → 붉은 테두리 강조 | 누가 무엇을 누구에게 넘기나, 제도·구조가 어떻게 작동하나 — 위 세 틀에 안 맞는 상황 설명 | 실제 인물은 권리가 확인된 사진만, 없으면 실루엣 + 이름표. 캐릭터 몸짓 애니메이션은 stage·illust | ytflow/stages/explain.py s_board — els{kind:person／card／img／text／arrow／brush／ban／dashed}, do[이름, move, hi, dim, hide, swap] |

## 카메라·깊이 (`camera`)

화면을 어디서 보고 어떻게 다가가나

| 기법 | 상태 | 어떻게 보이나 | 언제 | 주의 | 만드는 법 |
|---|---|---|---|---|---|
| 사진에 깊이 (2.5D 시차) | candidate | 옛 사진 속 사람이 배경에서 살짝 떠 보이며 아주 천천히 깊어짐 | 역사·인물 사진이 오래 머무는 장 표지·여는 장면 (호기심·시사) | 카메라를 억지로 움직이는 것과 같은 계열(v30) — 사진이 이야기의 증거로 오래 머물 때만, 한 영상 몇 장. 시장 채널은 v31 로 쓰지 않음 | 깊이 추정(Depth Anything) → 깊이에 따라 층을 나눠 GSAP 로 다른 속도 이동. 브라우저만으로 되는 render-image-depth(MIT) 방식이 렌더러와 맞음 |
| 한 점에서 물러나며 전체 보기 (풀백 리빌) | candidate | "0.3%" 한 칸에서 물러나면 수천 칸짜리 표 전체가 보임 | 훅 — 작은 것이 사실은 큰 것의 일부라는 반전 (시장·호기심) | 카메라 이동이므로 한 영상 1번, 시장 채널은 v31(확대·축소 없음) 확인 후 | HyperFrames 레지스트리 블록 pull-back-reveal 아이디어 (Apache-2.0, 설치됨, docs/17 후보) — GSAP scale 1 → 큰 값의 역방향 |

## 장면 전환 (`transition`)

한 장면에서 다음 장면으로 어떻게 넘어가나

| 기법 | 상태 | 어떻게 보이나 | 언제 | 주의 | 만드는 법 |
|---|---|---|---|---|---|
| 같은 것이 다음 화면으로 이어짐 (매치 무브·Flip) | candidate | 표지의 '631억' 카드가 작아지며 다음 장면 표의 한 칸으로 들어가 앉음 | 앞 장면의 결론이 다음 장면의 출발점일 때 — 장면이 '넘어가는' 게 아니라 '이어지는' 느낌 (README §2-1 진행 멘트 대신) | 화면 전체를 움직이는 카메라가 아님 — 요소 하나만 이동 (v12·v30 억지 움직임과 다름) | GSAP Flip(무료) — 이전 위치를 기록하고 새 레이아웃으로 옮김. 장면 경계에서 두 장면을 겹쳐 렌더해야 함 (edit10 전환 구간 0.3초 활용) |
| 소리 먼저·소리 남기 (J컷·L컷) | candidate | CEO 얼굴이 나오기 0.5초 전부터 그의 목소리가 들리기 시작함 | 원본 발언(bite)·자료 영상으로 넘어갈 때 — 하드 컷의 덜컥거림 없이 |  | cutedit·footage 의 오디오 시작을 화면 경계보다 0.3~0.8초 앞(J)·뒤(L)로 — ffmpeg adelay/atrim, 내레이션은 그 구간 낮춤 |
| 장면 전환 묶음 (xfade) | partial | 앞 장면이 원으로 오므라들며 다음 장면이 드러남 (circleopen) | 장 표지 앞뒤처럼 '단락이 바뀐다' 를 보여 줄 때만 | v12 기각 '매 장면 휙 전환은 정신없다' — 보통 장면은 부드러운 겹침(fade) 하나만 | 지금 edit10 이 HTML 안에서 wipe·push·zoom·iris 를 돌려 씀. 영상 조각을 이을 땐 ffmpeg xfade=transition=fade／dissolve／wipeleft／slideup／circleopen／pixelize… |
| 확대해 들어가며 다음 장면 (줌 인 전환) | hold | 지도 위 한 도시로 들어가면 그 도시의 거리 사진이 펼쳐짐 | 전체 → 한 부분으로 '들어가는' 이야기 (호기심·역사) | 시장 채널 v31 '확대·축소 쓰지 않음' 과 충돌 — 시장 채널은 쓰지 않음. 다른 채널도 한 영상 1번 이하 | Motion Canvas zoomInTransition 개념을 GSAP 로 — 앞 장면 scale 확대 + 다음 장면 페이드 |
| 휙 넘기기 (휩 팬) | hold | 가로로 흐려진 띠가 지나가며 장면이 바뀜 | 빠른 쇼츠의 시간·장소 점프 | v12 기각('매 장면 휙 전환·휙 소리 — 정신없다')과 정면 충돌 — 롱폼에서는 쓰지 않음 | 앞 장면 끝·다음 장면 처음에 가로 이동 + 가로 흐림(ffmpeg xfade hblur 또는 CSS blur) |
| 셰이더 전환 모음 (gl-transitions) | hold | 장면이 물결처럼 일렁이며 바뀜 | 지금은 쓰지 않음 (보류) — 쓴다면 쇼츠의 장면 점프 한두 번, 전환마다 라이선스를 확인한 것만 | 전환마다 라이선스가 따로 적혀 있음(한 줄로 정리 안 됨) + 화려한 전환은 v12 '정신없다' 기각과 충돌 — 보류 | ffmpeg-gl-transition 이나 브라우저 WebGL 로 렌더 |
| 원 모양을 잇는 아이리스 | have | 앞 장면의 원이 확대되어 덮고 다음 장면이 같은 색에서 원으로 열림 | 금고 보호 범위 등 원 모양이 다음 이야기로 이어질 때 | 현 구현은 바탕색을 거쳐 열림; 원 안에 다음 장면이 곧바로 보이는 합성은 미구현 | 앞 장면 iris_out: {x, y, r, color, to}; edit10 전환이 켜져 있어야 함 — docs/43-reference-pickle-explainer.md §6 |

## 배경음 (`bgm`)

내레이션 밑에 까는 음악의 분위기 (시장 채널은 기본 없음)

→ 배경음 목록 `assets/bgm/bgm.yaml` (곡·라이선스·어울리는 분위기). 기본은 없음 — 어울리는 곡이 확실할 때만(05 §0-5).

## 효과음 (`sfx`)

장 전환·정리·튀어나옴에 아주 조금 (v12 '덜'이 기본) — 눌러서 들어 보기

| id | 이름 | 어떻게 보이나 | 언제 | 구현·값 | 예시 |
|---|---|---|---|---|---|
| `whoosh` | 휙 | 장 표지로 넘어갈 때 | 장 전환 (push) |  | — |
| `whoosh-short` | 짧은 휙 | 짧은 넘김 | 빠른 전환 |  | — |
| `pop` | 톡 | 튀어나옴 | 아이콘 줄(isotype)·작은 등장 |  | — |
| `click-soft` | 부드러운 딸깍 | 체크·선택 | 체크리스트 |  | — |
| `riser` | 차오름 | 장 표지 직전 | 장 표지 앞 |  | — |
| `chime` | 차임 | 정리판 | 장 끝 정리(recap) |  | — |
| `pencil` | 연필 긁기 | 손그림 선이 그려질 때 | 종이 손그림 (직접 만든 소리) |  | — |
| `impact-bass` | 저음 두웅 (hold) | — | — · 피함: 사용자 판정 "소리 자체가 싫다" (2026-11-10) — 쓰지 않음 |  | — |

## 목소리 (`voice`)

내레이터 (초안 edge-tts, 업로드 최종본 ElevenLabs — 채널별)

| id | 이름 | 어떻게 보이나 | 언제 | 구현·값 | 예시 |
|---|---|---|---|---|---|
| `nobel-butler` | Nobel Butler | 차분한 남성 내레이터 (ElevenLabs) | 호기심 (ch-knowledge) — 잼 편 v7 |  | — |
| `mina` | Mina | 여성 내레이터 (ElevenLabs) | 시사 (ch-issues) |  | — |
| `teo` | Teo | 남성 브리핑 (ElevenLabs) | 시장 이어 읽는 시장 (예비 Sung-ho) |  | — |
| `hyun-bin` | Hyun Bin | 남성 (ElevenLabs) | 원본 소스형·하이브리드 경제 |  | — |
| `injoon` | 인준 (edge-tts) | 초안용 무료 음성 | 모든 채널 초안 — 업로드 전 교체 |  | — |

## 썸네일 레이아웃 (`thumbnail`)

제목·썸네일 A/B/C 의 틀 (thumbnail.py, prompts/thumbnail.md)

| id | 이름 | 어떻게 보이나 | 언제 | 구현·값 | 예시 |
|---|---|---|---|---|---|
| `photo` | 사진 + 큰 두 줄 | 흑백 자료 사진 + 큰 두 줄 + 빨간 동그라미·도장 | 시사·역사·시장 (가장 많이 씀) |  | — |
| `versus` | 숫자 맞대기 | 종이 위 두 숫자 맞대기 (어두운 판은 punch 처럼) | 대비가 핵심인 편 |  | — |
| `board` | 그림판 | 종이 + 같은 선 그림 + 큰 글씨 | 호기심 이야기형 |  | — |
| `punch` | 시장 펀치 | 컬러 사진 + 노란 상자 강조 + ▲▼ 숫자 칩 | 시장 (2026-11-19) |  | — |
