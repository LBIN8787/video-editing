---
name: edit-style-hook-shorts
description: 훅 쇼츠 스타일(얼굴 없이 — AI 목소리 + 저장소·문서 캡처·화면 녹화를 꽉 채운 세로 화면, 첫 3초 훅 제목, 말하는 순간 바뀌는 큰 자막, 말에 맞춰 튀어나오는 카드·숫자·명령어, 박자 사이 0.12초의 빠른 리듬)로 AI·시장 쇼츠를 만든다.
---
# 훅 쇼츠 (`styles/recipes/hook-shorts.yaml`, `python -m ytflow hookshort <프로젝트>`)
1. 사실 확인 → `01_research/factsheet.md` (숫자·명령어는 화면에서 확인한 것만, 기준 날짜).
2. 화면 준비: 공개 페이지 캡처(Playwright, 세로 900×1600 @1.5) 또는 화면 녹화를 `04_assets/footage/`.
3. `02_script/hookshort.json`: brand, hook(lines·hl·logo·dur), keywords, scenes[media(file·pos·zoom), beats(say, insert: cards|number|code)], source.
   - 박자 하나 = 한 문장(12~20자 덩어리 1~2개). 같은 화면이 이어지면 자동으로 번갈아 확대.
   - 카드는 박자 2개에 하나 정도. 훅은 3초, 강조 낱말 하나.
4. 렌더 → 프레임 확인(자막 한 줄·화면 끝에 닿지 않음, 카드가 자막을 가리지 않음).
