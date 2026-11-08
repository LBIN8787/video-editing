---
name: edit-style-kinetic
description: 키네틱 타이포 편집 스타일(내레이션 단어가 말하는 순간 화면에 튀어나오고 핵심 단어는 크게·강조색, 화면 글자가 곧 자막)로 장면을 만든다. 훅(첫 30초), 장 전환, 결론 한 문장, 쇼츠에 쓴다. 롱폼 전체에는 쓰지 않는다.
---

# 키네틱 타이포 (레시피 `styles/recipes/kinetic-type.yaml`, 그래픽 팩 `kinetic-poster`)

- **장면 type `kinetic`:** 박자마다 `say` 와 `hit[]`(강조 단어 — say 안의 어절 그대로). 숫자가 든 어절은 자동 강조.
- **타이밍:** 박자 음성을 받아쓰기(faster-whisper)한 단어 시각에 맞춰 나타납니다 (`hybrid._word_starts`). 음성을 바꾸면 다시 렌더.
- **자막:** kinetic-poster 팩은 아래 자막을 숨깁니다(화면 글자가 자막). 다른 팩으로 쓰면 아래 자막과 겹치니 키네틱 장면만 쓰는 영상이 아니면 그래픽 팩은 영상 기본 팩을 따릅니다.
- **분량:** 한 장면 1~2박자, 박자당 25어절 이하. hit 은 박자당 1~3개.
- **시험작:** `projects/20261107-style-kinetic` (`styles/demos/kinetic.json`).
