# 07. 늘리기 — 채널·스타일·상황을 파일 하나로 추가

이 저장소는 **등록부 + 자동 선택** 구조입니다. 코드는 등록부를 읽기만 하므로, 늘릴 때 코드를 고치지 않습니다.

```
channels/brands.yaml      브랜드(욕망) 등록부  ─┐
channels/<라인>/           제작 라인 등록부      ├─→ topic_brief.json (욕망·질문 유형·분위기)
styles/recipes/*.yaml     편집 스타일 등록부  ─┘        │
skins/<id>/skin.yaml      그래픽 팩 등록부              ▼
                                         python -m ytflow style-pick → 영상 전체·훅·결론 스타일
                                         python -m ytflow check      → 등록부 기준으로 검사
```

## 1. 편집 스타일(레시피) 추가 — 상황에 맞춰 쓰이게
1. `styles/recipes/_template.yaml` → `styles/recipes/<새 id>.yaml` 복사.
2. `fits` 를 채웁니다: 어떤 **브랜드**, 어떤 **질문 유형**(01 §2 의 정해진 단어), 어떤 **분위기**, 어떤 **소스**가 있어야 하는지. 이것이 '적재적소'의 기준입니다.
3. `roles`: 영상 전체(whole) / 본론(body) / 훅(hook) / 결론(ending) 중 어디에 쓰는지.
4. 새 장면 type 이 필요하면 `ytflow/stages/directions.py` 에 함수 하나 + `register()` 에 이름 추가 (기존 장면은 건드리지 않음). 새 겉모습이 필요하면 `skins/<id>/skin.yaml`.
5. 시험작: `styles/demos/<id>.json` 스펙 → `python scripts/style_demo.py <원본> <시험작> styles/demos/<id>.json` → `python -m ytflow hybrid <시험작>` (같은 문장·목소리 재사용, 비용 0).
6. `status`: idea → demo(시험작 있음) → approved(사용자가 `review --pass`). 상태가 높을수록 style-pick 이 우선합니다.
7. 스킬 문서가 필요하면 `skills/edit-style-<id>/SKILL.md` → `python scripts/sync_skills.py`.

## 2. 채널(브랜드) 추가
1. `channels/brands.yaml` 에 항목: `desire`(상위 욕망 한 줄), `viewer_questions`, `triggers`, `lines`, `manual`.
2. 제작 라인 `channels/<id>/channel.yaml` (다른 라인 복사, `brand:` 를 새 브랜드로) + `README.md` + 빈 `episodes.md`.
3. 채널 매뉴얼 `manual/0X-<브랜드>.md`: 02~04 와 같은 목차 (주제 찾기 · 깊은 조사 · 대본 공식 · 소스 · 포장 · 이 채널만의 검사).
4. 스타일 등록부의 `fits.brands` 에 새 브랜드를 넣은 레시피가 1개 이상 있어야 style-pick 이 추천합니다.
5. `ytflow/stages/checklist.py` 의 `BRANDS` 에 이름 추가 (유일한 코드 수정).

## 3. 질문 유형·분위기 추가
`manual/01-desire-map.md` §2 표(굵은 이름) + `schemas/topic_brief.schema.json` 의 enum + 해당 레시피의 `fits.questions` 를 함께 고칩니다.

## 4. 늘린 뒤
`python -m ytflow manual-bump "무엇을 추가"` → 커밋 → `git push origin HEAD:refs/heads/manual/vN` (기준 변경 기록·백업).
