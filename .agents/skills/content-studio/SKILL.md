---
name: content-studio
description: 채널별 조사 글에서 쇼츠 안내형과 롱폼 칼럼형 영상을 반복 제작할 때 사용한다.
---

# 채널 콘텐츠 반복 제작

1. studio/README.md, channels/<id>/channel.json, 선택한 styles/<id>/STYLE.md를 읽는다.
2. scripts/content_studio.py inventory로 이전 소재·편을 확인한다. 같은 조사 원장은 재사용하고 영상 중복은 피한다.
3. AI 채널은 work-cases/README.md를 읽고 사용자의 실제 작업·완료 기준을 먼저 정한다. AI 도구를 적용해 실제 산출물과 증거를 남긴 뒤 공개할 범위를 정리한다. work-case 명령으로 원장을 만들고 new --work-case로 편별 작업 문서를 만든다. 기존 파일을 덮어쓰지 않는다.
4. content/topics/<topic>/sources.json → research.md → article.md 순으로 출처와 글을 정리한다. studio/prompts를 따른다.
5. 쇼츠는 간단한 주제 하나의 안내, 롱폼은 주장·근거·사례·반론을 갖춘 칼럼으로 대본화한다. 쇼츠에 장문용 비유·사례 개수를 억지로 맞추지 않는다.
6. 실제 화면·도식·자막으로 장면을 구성하고 채널 고정 보이스를 확인한다. 보이스 실패 시 다른 TTS로 대체하지 않는다.
7. 현재 자동 생성 연결과 롱폼 렌더러는 미완성이다. 사용할 수 있는 도구로 작업하되 미구현 구간을 완료라고 기록하지 않는다.
8. AI 채널은 개설·운영 요청을 받았다. channels/ai/launch/README.md를 따라 연결하되 실제 계정·OAuth가 없으면 게시하지 않는다. 퀴즈는 보류한다. 결과와 남은 작업을 episode의 review.md에 기록한다.

기존 ytflow와 이 스튜디오의 채널 설정을 혼동하지 않는다. 현재 채널에는 channel.json의 고정 음성 정책이 우선한다.

AI 쇼츠 신규·수정 제작은 shorts-ai-guide 1.1.0 / ShortsGuideV2를 기본으로 사용한다. styles/shorts-ai-guide/versions/1.1.0/README.md와 style-lock.json을 읽는다. 화면 날짜·회차는 표시하지 않고, 입력·행동·결과를 구체적인 자료로 보여준다. 고정 음성은 유지한다. 과거 1.0.0 구성은 재현용으로 보존한다. 디자인 변경은 새 버전으로 기록하고 scripts/render_short.py --check-only로 폰트와 입력을 검사한다.
