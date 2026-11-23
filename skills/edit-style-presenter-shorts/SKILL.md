---
name: edit-style-presenter-shorts
description: 말하는 사람 쇼츠 스타일(본인이 카메라에 대고 말한 영상 → 쉼을 자른 점프 컷·번갈아 펀치 인·9:16·훅 제목·말하는 순간 바뀌는 큰 자막·끼워 넣는 카드)로 세로 쇼츠를 만든다. 사용자가 촬영 영상을 줄 때만 쓴다.
---
# 말하는 사람 쇼츠 (`styles/presenter-shorts/STYLE.md`)
1. 촬영 영상을 `04_assets/footage/` 에, `02_script/presenter.json` 작성(source, lang, start/end, face_x, hook, keywords, inserts, punch, gap).
2. `python -m ytflow presenter <프로젝트>` → `05_edit/final.mp4`.
3. 프레임 확인: 훅 3초, 자막 겹침 없음, 카드가 얼굴을 가리지 않음, 컷이 말 중간을 자르지 않음.
4. 본인 촬영·퍼블릭 도메인만. 남의 영상 금지.
