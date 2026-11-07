# 시각 안내 강화 수정본

이전 MP4와 입력은 보존한다. 최신 화면 입력은 이 폴더 props.json, 스타일은 shorts-ai-guide 1.1.0 / ShortsGuideV2다. 고정 음성·대본·자막 시간은 이전 편의 것을 재사용한다. 신규 음성 생성은 없다.

화면 날짜와 상단 회차 번호를 제거했다. 설명 문단 대신 예시 자료·행동·결과 화면을 사용한다. 실제 자료와 설명용 UI 도식을 표시한다. 새 렌더 명령은 아래와 같다.

```bash
python scripts/render_short.py --props channels/ai/episodes/006-whisper/revisions/visual-v2/props.json --out studio/renderer/out/AI-Shorts-006-Whisper-Visual-v2.mp4
```

실제 YouTube 게시와 정기 실행은 이 작업에 포함하지 않았다.
