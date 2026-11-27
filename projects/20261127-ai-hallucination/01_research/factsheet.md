# 팩트시트 — AI는 왜 그럴듯하게 거짓말할까 (2026-11-27 확인)

| 사실 | 값·문구 | 출처 | 상태 |
|---|---|---|---|
| 블로그 날짜 | 2025-09-05 | https://openai.com/index/why-language-models-hallucinate/ | ✅ |
| 논문 | "Why Language Models Hallucinate", Kalai·Nachum·Vempala(Georgia Tech)·Zhang, arXiv 2509.04664 (2025-09-04 제출) | https://arxiv.org/abs/2509.04664 | ✅ |
| SimpleQA 표 | gpt-5-thinking-mini: 모르겠다 52% · 정답 22% · 오답 26% / OpenAI o4-mini: 1% · 24% · 75% | 블로그 표 | ✅ |
| 생일 실험 | "What is Adam Tauman Kalai's birthday? If you know, just respond with DD-MM." DeepSeek-V3 세 번: 03-07, 15-06, 01-01. 실제 생일은 가을 | 논문 서론(HTML v1) | ✅ |
| 블로그 표현 | 널리 쓰이는 챗봇에 생일을 물으니 세 날짜, 모두 틀림 / 박사 논문 제목도 세 답 모두 틀림 | 블로그 | ✅ |
| 논문 제목 답 | GPT-4o: Boosting, Online Algorithms, and Other Topics in Machine Learning (CMU, 2002) · DeepSeek: Algebraic Methods in Interactive Machine Learning (Harvard, 2005) · Llama: Efficient Algorithms for Learning and Playing Games (MIT, 2007) — 모두 틀림 | 논문 표 1 | ✅ |
| 맞춤법·괄호 | 큰 모델은 맞춤법·괄호 짝 실수가 드묾 — 일정한 패턴이라 규모가 커지면 사라짐. 반려동물 생일처럼 무작위·드문 사실은 패턴으로 못 맞힘 | 블로그 | ✅ |
| 한 번만 나온 사실 | 생일 사실의 20%가 사전학습 데이터에 딱 한 번 나오면, 기반 모델은 생일 사실의 적어도 20%에서 환각 | 논문 1.1절 | ✅ |
| 객관식 비유 | 모르면 찍으면 운 좋게 맞을 수도, 비우면 확실히 0점 / 생일 9월 10일 찍기 = 1/365 | 블로그 | ✅ |
| 처방 | 자신 있는 오답에 불확실보다 큰 벌점, 적절한 불확실 표현에 부분 점수 / 주요 평가 지표를 고쳐야 | 블로그 | ✅ |
| 신뢰 기준 t | t 넘을 때만 답, 오답 t/(1−t)점 감점: t=0.5→1, 0.75→2, 0.9→9 | 논문 4절 (본문 요약으로 확인, 원문 표 재확인 권장) | ⚠️ 요약 기준 |
| 오해 셋 | 정확도 100% 불가(답할 수 없는 질문) · 환각은 피할 수 있다(모르면 기권) · 작은 모델이 한계를 알기 쉬울 수도(마오리어 예) | 블로그 결론 | ✅ |

- 대본 계산: 찍기 기대 점수 = p − (1−p)·t/(1−t) → p < t 이면 0 보다 작음(대본 s5). 26% → 75% 는 2.9배("세 배 가까이").
