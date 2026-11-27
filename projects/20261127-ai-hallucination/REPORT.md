# REPORT — 20261127-ai-hallucination (singularity-explainer 예시 영상)

- 주제: AI는 왜 그럴듯하게 거짓말할까 — OpenAI 「Why Language Models Hallucinate」(2025.9) 해설
- 스타일: `styles/singularity-explainer` (학습 요소가 있는 어려운 개념을 쉽게 푸는 해설, 2026-11-27 사용자 결정)
- 길이 4분 36초 · 대사 47줄 1,487자(분당 약 346자) · 장 5개 + 도입·마무리
- 만든 것: `02_script/lines.json`(대본) · `02_script/scenes.js`(연출) · `02_script/timeline.json` · `01_research/factsheet.md`
- 다시 만들기:
  1. `python styles/singularity-explainer/engine/voice.py projects/20261127-ai-hallucination/02_script/lines.json <작업폴더>`
  2. 장 표지 그림 3장(`<작업폴더>/art/cover_exam·cover_birthday·cover_board.png`, Codex 구독 $imagegen, 프롬프트는 STYLE.md 엔진 절)
  3. `python styles/singularity-explainer/engine/render.py projects/20261127-ai-hallucination/02_script <작업폴더> --jobs 4`
- 미디어(final.mp4·그림)는 커밋하지 않음 → 보관은 Drive(`YTFLOW_DRIVE\영상\`)

## 원본 대비 1초 간격 움직임
| 지표 | 원본(AI 특이점, 15분) | 이 영상 |
|---|---|---|
| 정지 비율 | 35% | 21% |
| 큰 변화 간격 | 4.1초 | 3.8초 |
| 가장 긴 정지 | 8초 | 5초 |

## 남은 일
- 목소리: edge-tts 초안 → 확정 시 Gemini(Knox·Riko) 또는 ElevenLabs
- 배경음 없음(원본은 잔잔한 배경음 전 구간)
- 신뢰 기준 t/(1−t) 감점 수치는 논문 본문 요약으로 확인 — 원문 4절 재확인
- 제목·썸네일 A/B/C, 업로드 전 사용자 승인

## 보관 (Drive)
- `ytflow/영상/20261127-ai-hallucination/final_draft_edge.mp4` (57MB, edge-tts 초안)
- `ytflow/영상/20261127-ai-hallucination/art/cover_exam·cover_birthday·cover_board.png`
