---
name: video-script
description: 팩트시트와 편집 스타일 규칙으로 장면(scene) 단위 영상 대본 scenes.json 을 쓴다. 내레이션, 원본 발언(quote), 인포 카드(card), 기사 캡처(screenshot), 원본 영상(source_video) 장면을 설계하고 validate 로 점검한다.
---

# 대본 작성 (script 단계)

## 자동
`python -m ytflow stage <프로젝트> script` 를 실행합니다. 프롬프트는 다음을 합친 것입니다.
- `prompts/script.md`: 모든 스타일 공통. **일반인이 바로 이해하는 대본** 원칙과 카드 규격
- `prompts/script_<계열>.md`: 편집 스타일 계열의 화면 문법 (`source` 원본 소스형 / `infographic` 자체 제작 인포그래픽형)
- `data/style_profile.json`(채널 대본 규칙), `styles/<style_ref>/script.md`(스타일 추가 규칙)

다 쓰면 점검(`ytflow/scriptcheck.py`)을 돌리고, 걸린 것이 있으면 한 번 고쳐 씁니다.

## 일반인용 대본의 뼈대
1. **핵심 한 문장** `core_message`: 다 본 사람이 기억할 문장. 숫자 1개 포함.
2. **논리 구조** `logic` 3~6단계: 무슨 일(사실·숫자) → 왜 → 그래서 → 전에도?(과거 사례) → 반론 → 의미.
3. **장면 역할** `beat`: fact · number · why · so_what · analogy · precedent · jargon · question · quote · summary · counter · takeaway · next.
4. **숫자**는 비교 기준과 함께(`compare_to`: 작년 대비, 1인당, 익숙한 규모). 한 문장에 숫자 2개까지.
5. **비유** 2개 이상: `card.type=analogy` (items[0] 실제 ≈ items[1] 일상 비유). 규모 비율은 실제와 맞춥니다.
6. **과거 사례** 1개 이상: 연도·숫자·출처. 상장사는 chart 카드에 `ticker` + `start`/`end` 로 그때 주가를 그립니다. '그때와 다른 점'도 한 장면.
7. **어려운 말**은 처음 나올 때 풀어 줍니다: `glossary`[{term, plain, scene_id}]. 점검 대상 목록은 `data/jargon.json`.

## 직접 쓸 때
1. 다음을 읽습니다.
   - `01_research/factsheet.md`, `01_research/articles.json`
   - `data/style_profile.json`
   - `styles/<id>/STYLE.md`, `styles/<id>/script.md`
2. `02_script/scenes.json` 을 씁니다(스키마 `schemas/scenes.schema.json`). 장면 하나의 필드는 다음과 같습니다.
   - `id`: 1부터 순서대로
   - `section`: hook / intro / body-N / turn / takeaway / outro
   - `kind`: narration 또는 quote
   - `narration`: 읽을 문장. quote 장면이면 원문의 한국어 번역
   - `quote_en`: quote 일 때 원문
   - `label`: `YYYY.MM.DD · 출처` (화면 왼쪽 위)
   - `visual_type`: source_video | card | screenshot | stock | ai_image
   - `source`:
     - source_video 는 url 을 비우고 `query`(YouTube 검색어)와 `length`(초)를 적습니다.
     - screenshot 은 articles.json 에 있는 URL 을 `url` 에 적습니다.
     - quote 는 확인된 영상 url 과 `start`/`end`(m:ss)를 적습니다.
   - `card`: card 장면이면 `{type, title, items[{label,value,sub,highlight,icon}], note}`. type 은 chart | line | number_compare | bars | flow | table | headline | text | analogy 입니다. chart 는 `ticker`, `period` 또는 `start`/`end`.
   - `beat`: 장면의 역할 (위 '뼈대' 3번), `compare_to`: number 장면의 비교 기준
   - 대본 맨 위: `core_message`, `logic`, `glossary`
   - `emphasis`: 자막에서 강조할 단어 1개. 문장에 실제로 있는 말이어야 합니다.
   - `visual_brief`: 편집자에게 줄 화면 지시
   - `image_prompt`: ai_image 장면일 때 이미지 생성 프롬프트
3. `python -m ytflow validate <프로젝트>` 가 '✓ 통과'할 때까지 고칩니다. ✗ 는 반드시 고치고, ⚠(계열별 화면 비율, 긴 문장 등)는 가능한 만큼 고칩니다.
4. 사람이 읽는 `02_script/script.md` 는 `python -c "from ytflow.project import Project; from ytflow.stages.writing import write_script_md as w; p=Project.open('<프로젝트>'); w(p, p.read_json('script','scenes.json'))"` 로 만듭니다.

## 규칙
- **분량:** 분당 글자 수(style_profile targets) × 목표 분량을 지킵니다.
- **원본 발언:** quote 는 팩트시트 '인물 발언'에서 원문이 확인된 것만 씁니다.
- **단정 금지:** '재확인 필요' 팩트는 단정하지 않습니다. 투자 권유 표현은 금지합니다.
- **카드 강조:** 카드의 highlight 는 한 카드에 하나만 둡니다.
