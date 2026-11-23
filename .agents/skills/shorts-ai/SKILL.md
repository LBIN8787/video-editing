---
name: shorts-ai
description: AI 활용법·GitHub 화제 저장소(Claude/Codex 스킬, MCP 서버, AI 에이전트)를 소재로 9:16 유튜브 쇼츠(30~45초)를 만든다. 최근 14일 GitHub 별 증가와 AI 뉴스로 소재를 고르고, 저장소 화면을 캡처해 고정 훅·큰 자막 형식으로 편집한다.
---

# AI 꿀팁 쇼츠

- **스타일 문서:** `styles/shorts-aitips/STYLE.md` (벤치마킹 근거와 화면 문법)
- **실행:**
  ```bash
  python -m ytflow shorts                         # 소재 자동 선택 (GitHub·HN·뉴스)
  python -m ytflow shorts --repo owner/name       # 저장소 지정
  python -m ytflow shorts --topic "챗GPT 표 정리 팁"  # 저장소 없는 팁
  ```
- **산출물:** `projects/<날짜>-shorts-*/`
  - `00_source/ai_trends.json`, `pick.json`
  - `01_research/repo.json`
  - `02_script/shorts.json`(훅·장면), `scenes.json`
  - `04_assets/repo_full.png`(저장소 전체 캡처)
  - `05_edit/draft.mp4`(1080×1920), `REPORT.md`
- **점검:** 장면 2~3개 프레임을 뽑아 확인합니다. 볼 것은 세 가지입니다.
  - 고정 훅이 잘리지 않는가
  - 자막이 가운데 창 아래에 있는가
  - 페이지가 스크롤되는가
- **지킬 것:**
  - README·저장소에 있는 내용만 말합니다.
  - 해킹·우회·개인정보 수집 도구는 다루지 않습니다.
  - 저장소 라이선스를 확인합니다.
