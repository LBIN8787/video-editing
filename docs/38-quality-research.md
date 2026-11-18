# 38. 모션그래픽이 'AI 슬롭'처럼 보이는 이유와 고품질로 가는 길 (2026-11-18)

> 사용자: "현재 보이는 사진으로만 보면 솔직히 말해서 너무 퀄리티가 낮고 어색해요 품질도 깨지고 있구요."
> "품질이 깨진다는 건 그냥 모션그래픽의 퀄리티가 너무 처참해서 말한 것이에요. 흔히 말하는 AI slop 이라서 그런 거구요."
> "애니메이션이라기보다는 PPT 로 대충 만든 도형들의 집합이라는 느낌이 강합니다."

## 1. 진단 — 왜 슬롭처럼 보이나 (호기심 샘플 40초 프레임 기준)
| 보이는 것 | 왜 싸 보이나 |
|---|---|
| 동그란 머리·점 눈·웃는 입·원통 몸 | 누구나 '기본값'으로 그리는 클립아트. 디자인한 사람이 없다는 신호 |
| 넓은 빈 종이에 물건이 둥둥 | 구도·무대·배경이 없음. 물건이 '어디에' 있는지 정하지 않음 |
| 화면 끝에서 잘린 글자·문서 | 배치를 눈으로 확인하지 않음 — 자동 생성의 전형 |
| 모든 선 굵기·색·그림자가 똑같음 | 빛·깊이·강약 없음. 원근·겹침이 없어 납작함 |
| 움직임 = 이동·크기 바꾸기 트윈 | 예비 동작·관성·표정 변화 없이 미끄러짐 → 인형극이 아니라 슬라이드 |
| 장면마다 같은 틀(코드로 찍은 템플릿) | 장면이 이야기를 위해 '설계'되지 않고 부품을 조립한 티 |

**뿌리:** 그림을 코드(SVG 도형)로 즉석 생성하고 있다는 것. 코드는 움직임을 잘하지만 **그림(디자인) 자체**를 잘 만들지 못합니다. 그래서 움직임을 아무리 손봐도 첫인상이 '슬롭'으로 남습니다.

(덧붙여 고친 것: 최종 인코딩이 1080p 에 약 1 Mbps 로 낮아 종이 결이 뭉개졌음 → `hybrid.py` 를 CRF 15·slow·animation 튜닝으로 올림. 사용자께서 말한 '깨짐'의 원인은 아니지만 유튜브 재압축 대비로 필요.)

## 2. 잘 만드는 곳은 어떻게 하나
- **Kurzgesagt** — 일러스트레이터가 Illustrator 로 장면 그림을 먼저 완성 → 부품으로 나눠 After Effects 로 가져가 캐릭터마다 관절을 달고(rig) 움직임. 한 편 1,200시간, 애니메이터 2~3명이 8~12주. **그림이 먼저, 움직임은 그다음.** ([1,200시간 제작기](https://rosetta.to/u/kurzgesagt/how-to-make-a-kurzgesagt-video-in-1200-hours), [GIGAZINE 정리](https://www.gigazine.net/gsc_news/en/20200217-science-animation-making/), [공식 강의](https://www.skillshare.com/en/classes/Motion-Graphics-with-Kurzgesagt-%E2%80%93-Part-1/631970755))
- **AI 를 쓰는 얼굴 없는 채널의 공통점** — 캐릭터 정체성을 프롬프트가 아니라 **턴어라운드 시트(정면·측면·3/4·뒷면, 같은 조명)** 에 담아 두고, 장면마다 그 시트를 참조 이미지로 넣음. 자주 나오는 인물은 LoRA 까지. ([fal.ai 가이드](https://fal.ai/learn/tools/ai-character-consistency), [Scenario 턴어라운드](https://help.scenario.com/en/articles/generate-character-turnarounds/), [Lemonlight 워크숍](https://www.lemonlight.com/blog/how-to-create-consistent-ai-characters/))
  - 평면 스타일 문구 예: *"bold outlines, flat colors, minimal shading, consistent line weight"* + 색을 hex 로 고정 ([Jeff Bullas 포럼](https://www.jeffbullas.com/reply/125997/)), 시트 문구 예: *"character design sheet, front / side / back views, orthographic camera, consistent lighting across all views"*.
  - 주의: 한 번의 프롬프트로는 자주 실패하고 여러 번 다시 뽑아야 한다는 보고도 있음 ([Dream Pixel Forge](https://www.dreampixelforge.com/blog/character-turnaround)).
- **그림 한 장 → 움직이는 부품으로** — Qwen-Image-Layered 는 그림 한 장을 투명 레이어 여러 장으로 나눔(공개 모델, fal.ai 약 $0.05/장). 움직임은 따로 붙여야 함 ([논문](https://arxiv.org/html/2512.15603), [fal.ai](https://fal.ai/models/fal-ai/qwen-image-layered), [DataCamp](https://www.datacamp.com/ja/tutorial/qwen-image-layered)).
- **벡터(SVG)로 바로 생성** — Recraft V4 Vector $0.08/장, Pro $0.30/장. 편집 가능한 SVG 라 우리 HyperFrames·GSAP 로 부품을 바로 움직일 수 있음 ([OpenRouter](https://openrouter.ai/recraft/recraft-v4-vector)). 레이어 분리를 보장하지는 않음.
- **핵심 장면만 그림 → 영상(I2V)** — Seedance·Kling·Veo 등. 초당 수십 원~수백 원. 인물 연기는 가장 자연스럽지만 장면마다 그림체가 흔들릴 수 있어 '참조 그림 고정'이 필수.

## 3. 갈 수 있는 길
| 길 | 품질 | 비용·시간 | 위험 |
|---|---|---|---|
| A. 지금처럼 코드로 그리되 다듬기 | 낮음 → 조금 나음 | 무료 | **천장이 낮음.** 슬롭 인상은 그대로 |
| **B. 그림은 생성(고정 스타일·인물 시트) → 부품으로 나눠 → 우리 코드로 움직임** | 중상 | 한 편 그림 30~60장 기준 수천~1만 원대 | 그림체 일관성 관리가 일 |
| C. B + 핵심 장면 2~4개만 I2V | 상 | 한 편 몇천~수만 원 추가 | 비용, 장면 간 그림체 차이 |
| D. 사람 일러스트레이터에게 인물·소품 세트 의뢰 | 최상 (채널 정체성) | 한 번 큰 비용, 이후 재사용 | 시간 |
| E. 그림을 덜 쓰는 형식 (자료 사진·실제 화면·글자 연출 위주) | 중 | 무료 | 호기심 채널의 '이야기 애니메이션' 방향과 다름 |

## 4. 추천
1. **'그림 먼저' 순서로 바꾸기** — 움직임을 만들기 전에 *스타일 프레임*(완성 화면 정지 그림 3장: 인물 시트 1 + 대표 장면 2)을 먼저 만들어 사용자 확인(D3 앞에 '룩 확인'). 이 단계를 통과하지 못한 그림은 움직이지 않음.
2. **호기심 채널은 길 B 로 시험 1장면(20~30초)** — 주인공 시트 → 같은 그림체로 장면 그림 3장 → 레이어 분리 → 예비 동작·관성·표정을 넣어 움직임. 예상 비용 몇천 원 이내(유료라 승인 필요).
3. **AI·시사 채널은 그림보다 '실제 화면·자료 사진·도표'의 완성도** — 캐릭터 대신 원문 캡처·같은 축 차트·지도를 정돈된 레이아웃으로(여백·정렬·글자 위계). 코드로 그린 사람 아이콘은 빼는 쪽.
4. 사용자께서 '이 정도면 좋다'고 생각하는 **레퍼런스 영상 1~2편**을 주시면, 그 그림체·움직임 밀도를 기준선으로 삼아 스타일 프레임을 맞춤.
