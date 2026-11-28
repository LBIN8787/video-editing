---
name: edit-style-hybrid
description: 하이브리드 편집 스타일(실제 인터뷰·자료 영상 + 이름 자막·형광펜 주석 + 종이 위 손그림 인과 지도·도식)로 영상을 만들거나 고친다. 식스시그마식 원본 영상, 머니크루식 논리·인과, 미주일기식 손그림을 한 영상에 섞을 때 쓴다.
---

# 하이브리드 스타일 (renderer: hybrid)

- **규칙 원본:** `styles/hybrid/STYLE.md`, 대본 문법: `prompts/script_hybrid.md` (장면 type 표와 필드)
- **대본:** `projects/<프로젝트>/02_script/hybrid.json` — 질문(question)·핵심 한 문장·인과 지도(map)·장면(scenes: type + beats[say…])·footage(출처·라이선스)
- **원본 영상 확보:** `04_assets/footage/<키>.mp4` 에 넣고 hybrid.json 의 footage 에 credit·url 을 적습니다.
  - 클라우드에서 되는 곳: NASA 이미지·영상 라이브러리(퍼블릭 도메인, images-api.nasa.gov). 위키미디어 공용(CC BY)은 클라우드 IP 가 자주 429 로 막힘 → PC 에서.
  - YouTube 공식 채널 영상 구간은 `python -m ytflow clip-order <프로젝트>`(클라우드 주문서) → 사용자 PC 에서 `clip-fetch` (대본이 쓰는 구간만 — 방송사 원본은 20초 이내, 공공·공식은 길이 제한 없음, footage `"rights"`, manual/09 §3-5). 봇 확인 우회 금지, 막힌 페이지는 `inbox/requests/` 로 피클에게.
- **글씨 카드로 끝나는 설명 다시 보기 (렌더 전, manual/05 §0-10):** `python -m ytflow edit-plan <프로젝트>` → `02_script/EDIT_CONTEXT.md` §5 에 '글씨 카드인데 대본이 구조·원리·원인·변화를 설명하는 장면'과 더할 장면 후보가 나옵니다. 장면마다 그 설명을 연기하는 장면을 카드 앞뒤에 더할지 판단합니다 — 구조·공간·연결 → `cutaway3d`(3D 구조 세트, `python -m ytflow cutaway3d list|sheet`, `styles/hybrid/scenes/cutaway3d.md`) · 원리 → `mechanism` · 차이·몫·누적 → `spread`·`share`·`afterline` · 사물 → `motionboard`. 더하지 않으면 이유를 `decide` 기록에 한 줄.
- **만들기:** `python -m ytflow hybrid <프로젝트>` → 박자별 음성 → 장면별 HyperFrames 렌더(병렬) → 이어 붙이기·자막·효과음 → 마스터링(final.mp4)
- **점검:** 장면마다 `hyperframes check` 결과가 `04_assets/layout_qa.json` 에. 프레임을 뽑아 직접 확인(`skills/video-edit`).
  - 같은 type 연속, 20~30초 넘게 원본 영상 없음, 숫자만 나열된 박자가 없는지.
- **효과음:** HyperFrames media-use 의 내장 효과음(Pixabay 라이선스, 상업 사용 가능)을 작게 섞습니다.
