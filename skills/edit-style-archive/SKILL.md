---
name: edit-style-archive
description: 아카이브 다큐 편집 스타일(자료 사진·영상 전체 화면 + 켄 번스 움직임 + 시간·장소 도장 타자기 + 검은 화면 한 줄 문장)로 영상이나 장면을 만든다. 역사·사건·인물, 위기·과거 사례처럼 자료 화면이 풍부한 주제의 영상 전체 또는 훅(첫 30초)에 쓴다.
---

# 아카이브 다큐 (레시피 `styles/recipes/archive-doc.yaml`, 그래픽 팩 `dark-doc`)

- **언제:** `python -m ytflow style-pick <프로젝트>` 가 추천했거나, 자료 사진·영상이 5개 이상이고 분위기가 위기·과거일 때. 숫자 비교가 핵심이면 bars·versus 장면을 섞습니다.
- **장면 type** (`ytflow/stages/directions.py`, 필드는 `docs/16-new-styles.md`):
  - `kb`: `clip{src,start}`, `move`(in/out/left/right/up), `stamp`("1918 · 프랑스 서부전선" — 사진 원래 설명의 날짜·장소 그대로), `label`(출처)
  - `card_type`: `lines[]`(줄마다 타자기), `by`(인용 출처)
- **리듬:** kb 2~3장면 → card_type 1장면. card_type 2연속 금지. kb 한 장면 15초 넘으면 `move` 를 바꾼 kb 로 나눕니다.
- **자료:** `python -m ytflow archive search "<영문>"` → `archive.still_to_clip()` 로 16:9 영상. credit·url 필수 (CC BY·CC0·퍼블릭 도메인만).
- **만들기:** `edit.yaml` 의 `skin: dark-doc` → `python -m ytflow hybrid <프로젝트>` → `python -m ytflow check <프로젝트>`.
- **시험작:** `projects/20261107-style-archive` (`styles/demos/archive.json`).
