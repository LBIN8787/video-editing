---
name: edit-style-hybrid
description: 하이브리드 편집 스타일(실제 인터뷰·자료 영상 + 이름 자막·형광펜 주석 + 종이 위 손그림 인과 지도·도식)로 영상을 만들거나 고친다. 식스시그마식 원본 영상, 머니크루식 논리·인과, 미주일기식 손그림을 한 영상에 섞을 때 쓴다.
---

# 하이브리드 스타일 (renderer: hybrid)

- **규칙 원본:** `styles/hybrid/STYLE.md`, 대본 문법: `prompts/script_hybrid.md` (장면 type 표와 필드)
- **대본:** `projects/<프로젝트>/02_script/hybrid.json` — 질문(question)·핵심 한 문장·인과 지도(map)·장면(scenes: type + beats[say…])·footage(출처·라이선스)
- **원본 영상 확보:** `04_assets/footage/<키>.mp4` 에 넣고 hybrid.json 의 footage 에 credit·url 을 적습니다.
  - 클라우드에서 되는 곳: NASA 이미지·영상 라이브러리(퍼블릭 도메인, images-api.nasa.gov). 위키미디어 공용(CC BY)은 클라우드 IP 가 자주 429 로 막힘 → PC 에서.
  - YouTube 공식 채널 영상은 사용자 PC 에서(yt-dlp, 봇 확인 우회 금지).
- **만들기:** `python -m ytflow hybrid <프로젝트>` → 박자별 음성 → 장면별 HyperFrames 렌더(병렬) → 이어 붙이기·자막·효과음 → 마스터링(final.mp4)
- **점검:** 장면마다 `hyperframes check` 결과가 `04_assets/layout_qa.json` 에. 프레임을 뽑아 직접 확인(`skills/video-edit`).
  - 같은 type 연속, 20~30초 넘게 원본 영상 없음, 숫자만 나열된 박자가 없는지.
- **효과음:** HyperFrames media-use 의 내장 효과음(Pixabay 라이선스, 상업 사용 가능)을 작게 섞습니다.
