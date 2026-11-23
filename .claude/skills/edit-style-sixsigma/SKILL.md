---
name: edit-style-sixsigma
description: 식스시그마 편집 스타일(원본 인터뷰·방송 영상 중심 + 검은 배경 인포 카드 + 출처 라벨 + 원문·번역 2단 자막)로 영상을 만들거나 검토한다. 기업·투자 뉴스, 실적·지분·딜 해설에 쓴다.
---

# 식스시그마 스타일

- **규칙 원본:** `styles/sixsigma/STYLE.md` (먼저 읽기), 대본 추가 규칙: `styles/sixsigma/script.md`
- **제작:** `python -m ytflow make --style-ref sixsigma [--topic "..."]`
- **기존 프로젝트에 적용:** `cp styles/sixsigma/edit.yaml projects/<프로젝트>/edit.yaml` 후 assets → subtitles → assemble
- **핵심 점검:**
  - 모든 화면에 날짜·출처 라벨이 있는가
  - 원본 발언이 원문 확인된 것인가
  - 카드 강조색이 하나뿐인가
  - 배경음악·줌이 없는가
- **저작권:** 뉴스·인터뷰 클립은 짧게 인용합니다. 저작권 위험을 줄이려면 공식 채널 영상과 공시 화면을 우선합니다(B안 방식).
