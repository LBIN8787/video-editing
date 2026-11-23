# 26. 이야기형 영상의 편집 노하우 — 종이 콜라주·이야기 애니메이션 조사 (2026-11-13)

> 사용자: "미주일기의 퀄리티와 비교하면 너무 졸라맨에 애니메이션 자체가 퀄리티가 너무 낮습니다. 그림 패턴도 너무 매번 똑같구요.
>  단순 미주일기만 벤치마킹하는 것이 아닌 이러한 노하우에 대해서 조사하고 작업해 달라는 의미에요."

v1 이야기 그림판(`story`)을 조사한 노하우로 다시 만들었습니다. 무엇이 부족했고, 어디서 무엇을 가져왔고, 코드에 어떻게 넣었는지 정리합니다.

## 1. v1 이 낮아 보인 이유 (프레임 검토)
| 문제 | 원인 |
|---|---|
| 졸라맨 | 사람을 막대 인물로 — 정보가 없고 유치해 보임. 참고 채널들은 **실제 사진·문서**를 오려 붙임 |
| 얇은 선 아이콘만 | 같은 굵기의 남색 선 그림만 반복 → 화면에 '무게'가 없음 (그림자·종이·질감 없음) |
| 패턴 반복 | 모든 요소가 같은 방식(선 그리기 → 이름표)으로 등장, 배경은 늘 같은 밝은 종이 |
| 평평함 | 한 겹 캔버스라 카메라가 움직여도 깊이가 없음 |
| 움직임 | 등장이 직선적(나타남·그려짐)이고, 놓이는 '손맛'(과장 → 안착, 그림자)이 없음 |

## 2. 조사한 노하우와 출처
### A. 종이 콜라주(컷아웃) 영상의 재료와 질감
- 컷아웃은 종이·천·**사진**을 오려 만든 납작한 인물·소품·배경으로 움직이는 형식 — 사진을 오려 쓰는 것이 기본 ([Prolific Studio](https://prolificstudio.co/blog/cut-out-animation/), [Adobe](https://www.adobe.com/uk/creativecloud/animation/discover/cut-out-animation.html)).
- '이음새가 보이는' 맛: 종이 결, 살짝 거친 가장자리, **아래로 떨어지는 그림자**(펠트 판에 핀으로 꽂은 듯) ([adwave 스타일 가이드](https://wavemaker.adwave.com/video-styles/paper_cutout), [videoai 가이드](https://videoai.me/blog/how-to-make-paper-collage-explainer-video)).
- 정지 콜라주는 포스터일 뿐 — **장면마다 한 가지를 가르치고, 움직임이 눈을 이끈다** ([videoai](https://videoai.me/blog/how-to-make-paper-collage-explainer-video)).
- 뉴스 해설형(Vox 계열) 요소: 종이 질감, 손으로 오린 그림, 오린 글자, **손그림 화살표·라벨** ([videoai: Vox-style](https://videoai.me/blog/what-is-vox-style-video-explained-2026), [PremiumBeat](https://www.premiumbeat.com/blog/replicating-vox-motion-graphic/)).
- After Effects 실무: 블렌드 모드 겹침, 로토로 층 나누기, 콜라주 안 모션 트래킹, **Posterize Time 12fps**로 스톱모션 느낌 ([Envato Tuts+](https://photography.tutsplus.com/articles/collage-animation-in-after-effects--cms-93666)).
### B. 깊이 — 2.5D 패럴랙스
- 사진을 앞·가운데·뒤 층으로 나누고, 가까운 층이 더 많이 움직이게 → 카메라가 움직이는 착시. 다큐의 '패럴랙스 켄 번스' ([PictureCorrect](https://www.picturecorrect.com/parallax-animation-bringing-still-photographs-to-life/), [Creators Project: Joe Fellows](https://thecreatorsproject.vice.com/blog/joe-fellows-teaches-us-how-to-master-25D-photography)). 뒤 층을 흐리게 하면 심도 표현.
### C. 움직임 원칙 (디즈니 12원칙의 모션그래픽 판)
- 모션그래픽에서 가장 쓸모 있는 것: **이징(천천히-빠르게-천천히), 타이밍, 따라오는 움직임·겹침, 예비 동작** ([LottieFiles](https://lottiefiles.com/blog/tips-and-tutorials/mastering-disney-12-principles-animation), [Motion Array](https://motionarray.com/learn/motion-array/12-principles-of-animation-and-how-to-use-them-in-2024/), [ion interactive](https://ioninteractive.com/?p=16206)).
### D. 일관성과 다양성
- **같은 손이 그린 것처럼**: 정성 들인 그림과 대충 그린 그림을 섞으면 두 영상처럼 보인다. 팔레트·글꼴·선 질감·전환은 고정 ([sketch 가이드 모음](https://pexo.ai/tutorial/how-to-make-a-sketch-explainer-video)).
- 다양성은 '새 스타일'이 아니라 **배경·구도·내용**으로 만든다. 막대 인물은 본래 시각 변화가 적어 금방 지루해진다 ([simpleshow](https://videomaker.simpleshow.com/new-smart-illustration-style-simpleshow-video-maker/), [stick figure 가이드](https://pexo.ai/tutorial/how-to-make-a-stick-figure-explainer-video)).
### E. 이야기 장면 설계 (Kurzgesagt 제작 과정)
- 대본이 끝나면 **장면마다 시각적 비유와 장면 사이 전환**을 먼저 스케치하고, 어느 장면에 공을 들일지 정한다. 목표는 "말을 가장 분명하게 보여 줄 그림 + 볼거리" ([Kurzgesagt 공식](https://kurzgesagt.org/youtube/), [Skillshare: Motion Graphics with Kurzgesagt](https://www.skillshare.com/en/classes/motion-graphics-with-kurzgesagt-part-1/631970755)).
### F. 미주일기 측정값 (styles/mijudiary/rules.json, 다른 편 240p 프레임 분석)
- 2초마다 요소 하나(분당 22.7회 변화), 정지 비율 0.26, 하드컷 적음, 밝은 종이 73% · 어두운 종이 18% · 사진 전체 배경,
  **논문·기사 캡처 + 형광펜**, **실사 폴라로이드 + 손글씨 이름**, 남색 평면 아이콘, 큰 숫자, 단락 사이 검은 화면.

## 3. v2 에 넣은 것 (`ytflow/stages/story_kit.py`, `story.py`)
| 노하우 | 구현 |
|---|---|
| 사진을 오려 붙임 (A) | `photo`: polaroid(흰 테두리·테이프·손글씨 이름) · cut(찢은 가장자리 + 종이 테두리) · round(동그란 인물) |
| 문서가 증거 (A·F) | `doc`: 기사·논문·백과 캡처를 종이처럼, `mark`: 말하는 순간 그 문장에 형광펜이 칠해짐 |
| 막대 인물 대신 | 사진이 있으면 사진, 없으면 `card`(인물 이름 카드: 직함·이름·한 줄) |
| 무게 있는 아이콘 (F) | `sticker`: 남색(또는 크림) 원 + 종이 테두리 + 그림자 |
| 같은 손 (D) | 모든 재료에 같은 종이 테두리·그림자·기울기, 사진은 같은 색 보정(GRADE), 이름표는 모두 종이 띠 |
| 깊이 (B) | 뒤(큰 글자)·가운데(사진·문서)·앞(스티커·쪽지) 세 겹이 카메라에 다른 속도로 (0.92 / 1.0 / 1.07) |
| 움직임 원칙 (C) | 과장 뒤 안착(back.out), 그림자가 떠 있다 내려앉음(LIFT → SHADOW), 머무는 동안 아주 느린 밀기 |
| 패턴 반복 막기 (D) | 등장 방식 돌려 쓰기(떨어뜨리기·밀어 넣기·뒤집기·내려놓기·펼치기, **같은 방식 연속 금지**), 배경 바꾸기 `bg`(밝은 종이·어두운 종이·사진 전체), 장면에 같은 재료가 50% 넘으면 `layout_qa` 경고 |
| 전환 (F) | 이야기 장면은 검은 화면에서 밝아짐 (단락 사이) |
| 12fps 스톱모션 (A) | **넣지 않음** — 이번 지적이 '품질'이라 끊기는 움직임은 거칠어 보일 위험. 손맛은 그림자·안착으로 |

## 4. 재료 구하기 규칙
- 사람: 위키미디어 공용 CC0·CC BY·퍼블릭 도메인만 (CC BY-SA·NC·ND 제외, `python -m ytflow archive commons`). 없으면 이름 카드.
- 옛 장면: 미국 의회도서관(1930년 이전·'No known restrictions') `python -m ytflow archive search`.
- 문서: 실제 기사·논문·백과 페이지 캡처(`clips.capture`), 막히면(예: Vercel 보안 검사) 우회하지 않고 다른 1차 출처로.
- 사진 설명은 사실대로: 사진이 그 장면이 아니면 쓰지 않는다(예: 2023년 카스파로프 사진은 '인물'로만, '1997년 그날'로 쓰지 않음).
- 위키미디어는 연달아 부르면 429 — 요청 사이 15초 이상.
