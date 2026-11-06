---
name: content-studio
description: 채널별 조사 글에서 쇼츠 안내형과 롱폼 칼럼형 영상을 반복 제작할 때 사용한다.
---

# 채널 콘텐츠 반복 제작

1. studio/README.md, channels/<id>/channel.json, 선택한 styles/<id>/STYLE.md를 읽는다.
2. scripts/content_studio.py inventory로 이전 소재·편을 확인한다. 같은 조사 원장은 재사용하고 영상 중복은 피한다.
3. new 명령으로 편별 작업 문서를 만든다. 기존 파일을 덮어쓰지 않는다.
4. content/topics/<topic>/sources.json → research.md → article.md 순으로 출처와 글을 정리한다. studio/prompts를 따른다.
5. 쇼츠는 간단한 주제 하나의 안내, 롱폼은 주장·근거·사례·반론을 갖춘 칼럼으로 대본화한다. 쇼츠에 장문용 비유·사례 개수를 억지로 맞추지 않는다.
6. 실제 화면·도식·자막으로 장면을 구성하고 채널 고정 보이스를 확인한다. 보이스 실패 시 다른 TTS로 대체하지 않는다.
7. 현재 자동 생성 연결과 롱폼 렌더러는 미완성이다. 사용할 수 있는 도구로 작업하되 미구현 구간을 완료라고 기록하지 않는다.
8. 샘플 피드백 전 계정 생성·업로드·정기 실행은 보류한다. 결과와 남은 작업을 episode의 review.md에 기록한다.

기존 ytflow와 이 스튜디오의 채널 설정을 혼동하지 않는다. 현재 채널에는 channel.json의 고정 음성 정책이 우선한다.
