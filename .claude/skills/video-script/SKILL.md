---
name: video-script
description: 팩트시트와 편집 스타일 규칙으로 장면(scene) 단위 영상 대본 scenes.json 을 쓴다. 내레이션, 원본 발언(quote), 인포 카드(card), 기사 캡처(screenshot), 원본 영상(source_video) 장면을 설계하고 validate 로 점검한다.
---

# 대본 작성 (script 단계)

## 자동
`python -m ytflow stage <프로젝트> script` 를 실행합니다. 프롬프트는 `prompts/script.md` + `data/style_profile.json`(채널 대본 규칙) + `styles/<style_ref>/script.md`(편집 스타일 규칙)입니다.

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
   - `card`: card 장면이면 `{type, title, items[{label,value,sub,highlight}], note}`. type 은 number_compare | flow | table | bars | headline | text 입니다.
   - `emphasis`: 자막에서 강조할 단어 1개. 문장에 실제로 있는 말이어야 합니다.
   - `visual_brief`: 편집자에게 줄 화면 지시
   - `image_prompt`: ai_image 장면일 때 이미지 생성 프롬프트
3. `python -m ytflow validate <프로젝트>` 가 '✓ 통과'할 때까지 고칩니다.
4. 사람이 읽는 `02_script/script.md` 는 `python -c "from ytflow.project import Project; from ytflow.stages.writing import write_script_md as w; p=Project.open('<프로젝트>'); w(p, p.read_json('script','scenes.json'))"` 로 만듭니다.

## 규칙
- **분량:** 분당 글자 수(style_profile targets) × 목표 분량을 지킵니다.
- **원본 발언:** quote 는 팩트시트 '인물 발언'에서 원문이 확인된 것만 씁니다.
- **단정 금지:** '재확인 필요' 팩트는 단정하지 않습니다. 투자 권유 표현은 금지합니다.
- **카드 강조:** 카드의 highlight 는 한 카드에 하나만 둡니다.
