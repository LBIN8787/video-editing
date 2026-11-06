---
name: edit-style-mijudiary
description: 미주일기 편집 스타일(구겨진 종이 배경 + 손그림 선이 그려지는 애니메이션 + 숫자 카운트업 + 사진·문서 콜라주 + 상자 자막)로 영상을 만들거나 검토한다. 개념·원리·역사 해설, 원본 클립이 부족한 주제에 쓴다.
---

# 미주일기 스타일 (paper 렌더러)

- **규칙 원본:** `styles/mijudiary/STYLE.md` (먼저 읽기), 대본 추가 규칙: `styles/mijudiary/script.md`
- **제작:** `python -m ytflow make --style-ref mijudiary [--topic "..."]`
- **기존 프로젝트에 적용:** `cp styles/mijudiary/edit.yaml projects/<프로젝트>/edit.yaml` 후 assets → subtitles → assemble
- **핵심 점검:**
  - 약 2초마다 화면이 변하는가
  - 애니메이션이 끝까지 그려진 뒤 멈추는가
  - 강조색(빨강·노랑)을 아주 조금만 썼는가
  - 자막이 상자 안에 있는가
- **아직 렌더러에 없는 기법**(STYLE.md '구현 상태'):
  - 한 장의 캔버스 + 카메라 이동, 형광펜 와이프, 검은 종이 + 딥 투 블랙, 원근 바닥
  - 이것들이 꼭 필요한 장면은 `visual_brief` 에 지시를 남겨 편집자가 마무리하게 합니다.
