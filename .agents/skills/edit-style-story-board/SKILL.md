---
name: edit-style-story-board
description: 이야기 그림판 스타일(큰 종이 한 장 위에 내레이션이 말하는 순간 사람·사물이 선으로 그려지고, 날짜 도장·종이 쪽지·말풍선·화살표가 생기며 카메라가 이야기를 따라감)로 호기심 채널의 이야기형 장면을 만든다. 누가·언제·어디서·무엇을 한 이야기를 들려줄 때 쓴다.
---

# 이야기 그림판 (`styles/story-board/STYLE.md`, 장면 type `story`)

1. 대본을 **이야기**로 쓴다 (manual/04 §0-4): 장면(때·곳·사람) → 사건 → 이상한 점 → 질문. 보도문 말투 대신 "~였습니다 / ~였죠 / ~거든요".
2. `story` 장면의 박자마다 `draw` 목록을 쓴다:
   - `{"t": "말하는 낱말", "do": "figure|draw|stamp|chip|note|count|bubble|arrow|circle|cross|check|hl|dim|cam", "id", "x", "y", ...}`
   - 좌표는 그림판 3840×2160. `cam: [x, y, 확대]` (0.5 = 전체, 0.85 = 한 구역), `"full"`.
   - 예: `scripts/curiosity_story/make.py`.
3. `python -m ytflow check <프로젝트> --upto G4` → `YTFLOW_TTS=edge python -m ytflow hybrid <프로젝트>` (초안) → 최종은 채널 ElevenLabs.
4. 프레임 확인:
   - 그림이 그 낱말을 말할 때 생기는지
   - 화살표가 가리킬 그림보다 먼저 나오지 않는지
   - 자막(아래 15%)과 겹치지 않는지
   - 카메라가 종이 밖을 보이지 않는지
5. 썸네일은 `layout: board` (종이 + 같은 선 그림 + 큰 글씨, prompts/thumbnail.md).

- **재료 (v2, docs/26-story-craft.md):** photo(polaroid·cut·round) · doc + mark · sticker · card · big · bg(paper·dark·photo). 사진은 04_assets/story/ 에, 라이선스는 credit 에.
- **규칙:** 실존 인물은 실제 사진(허용 라이선스) 또는 이름 카드(막대 인물 금지). 영상의 60~85%까지 이 스타일을 뼈대로 쓰고, 나머지는 kinetic(질문·결론 한 줄)·quote(인용)·versus(숫자 대비)로 숨을 쉰다.
