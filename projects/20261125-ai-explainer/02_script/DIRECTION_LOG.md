# 연출 결정 기록 — 20261125-ai-explainer

여러 연출·편집·스타일 가운데 이것을 고른 근거와 의도 (manual/05 §0-9, docs/66). 렌더 전에 이 한 장으로 검토합니다.

**결과: 통과**

## 영상 방향

- 고른 것: **dark-stage 설명 무대 + 고리 기준 그림 하나 + 이름 있는 시각 인용 (3Blue1Brown 원리 해설)**
- 왜: 보이지 않는 과정(연구 → 모델)을 고리 그림 하나로 잡고 끝까지 같은 그림 위에서 칸을 바꿈 — docs/70 S1·S3·S6
- 의도: 끝나면 시청자가 이런 뉴스를 '닫힌 고리냐, 짧아지는 손이냐'로 읽음
- 버린 것: `hook-shorts` — 실제 화면 녹화 중심 — 이 주제는 원리·구조가 주인공
- 버린 것: `news-desk` — 소식 나열이 아니라 한 질문(어느 칸이 남나)을 따라감
- 이 영상의 장면 어휘(닫힌 목록): share, motionboard, bars, bignum, quote, chapter
- 근거 문서: manual/12-visual-storytelling.md, docs/70-science-explainer-reference.md, manual/11-workflow.md

## 장면마다

| 장면 | 상황 | 고른 것 | 추천(edit-plan) | 버린 것 | 왜 | 의도 |
|---|---|---|---|---|---|---|
| 1 | metric | share | footage → kb → chat | footage, bignum, isotype | 숫자를 원래 대상(코드 전체) 위에 몫으로 | 80% 라는 크기를 눈으로 잡음 |
| 2 | explain | motionboard |  | stage, analogy | 통찰 한 줄을 카드 둘과 질문 하나로 | 이 영상이 무엇을 따라가는지 앎 |
| 4 | explain | motionboard | footage → kb → chat | footage, map_causal, timeline | 3Blue1Brown 식 기준 그림: 고리 하나를 끝까지 들고 감(S1·S3·S6) | 재귀적 자기개선이 고리의 모든 칸을 AI 가 맡는 것임을 앎 |
| 6 | metric | motionboard | chart → bignum → bars | chart, bars, bignum | 숫자 카드 옆에 회사 각주가 붙는 순서(A2) (다른 선택 이유: 장면 1 은 몫 하나라 share, 여기는 숫자 둘과 각주가 한 화면이라 카드 무대) | 회사 숫자에 회사 스스로 단서를 달았음을 앎 |
| 7 | compare | bars | zoomshot → footage | zoomshot, bignum, versus | 사람 4배 · AI 3배 → 52배를 같은 축에 | 1년 사이 변화의 크기를 앎 |
| 8 | metric | bignum | bite → footage → quote | bite, share, chart | 보도 숫자를 2월 0% 와 나란히 (다른 선택 이유: 앞의 숫자들은 회사 원문, 여기는 보도 숫자라 출처를 크게 단 bignum) | 반년 만의 변화를 앎 |
| 10 | explain | motionboard | map_causal → analogy | map_causal, checklist | A3: 같은 고리의 칸 라벨이 하나씩 바뀌고 ①만 사람으로 남음 — 기억할 한 장면 | 고리의 첫 칸이 아직 사람임을 기억 |
| 11 | said | quote |  | bite, motionboard | 회사의 각주를 원문 그대로 | 회사 스스로 인정한 한계를 앎 |
| 12 | said | quote | footage → kb → chat | footage, bite, versus | 회사 밖 기관의 같은 결론을 원문으로(11 §3-3 뒷받침) (다른 선택 이유: 장면 11 은 회사 원문, 여기는 회사 밖 기관 — 같은 틀로 나란히) | 독립 기관도 같은 결론임을 앎 |
| 14 | compare | bignum | chart → bignum → bars | bars, versus | 64% 와 조건 없는 20% 를 나란히(E5) — 반박 근거와 그 조건 (다른 선택 이유: 장면 7 은 같은 단위의 크기 비교라 bars, 여기는 조건이 다른 두 값이라 나란한 bignum) | 연구 감각 시험의 크기와 조건을 함께 앎 |
| 15 | said | quote |  | bite, bignum | 반박 쪽 근거를 원문 구절로 (다른 선택 이유: 장면 11·12 는 '남는다' 쪽, 여기는 '넘어간다' 쪽 근거 — 같은 인용 틀로 무게를 맞춤) | 스스로 고치는 실험이 실제로 있음을 앎 |
| 16 | said | quote | kb → footage → stage | kb, bite, bignum | 반박 쪽 시간표를 이름 있는 사람의 말로 (다른 선택 이유: 같은 '넘어간다' 쪽의 다른 근거(시간표)) | 그 칸이 넘어간다는 쪽의 시간표를 앎 |
| 18 | compare | motionboard | kinetic → card_type → recap | kinetic, checklist, versus | 반론 카드 셋 + 저울 밖 비판 하나 (다른 선택 이유: 장면 14 는 숫자 맞대기, 여기는 반론의 종류를 공간으로 나눔) | 의심하는 쪽의 근거를 앎 |
| 20 | compare | motionboard |  | timeline, versus | 세 갈래를 같은 크기로, 회사 위치 표시 (다른 선택 이유: 장면 18 은 반론 카드, 여기는 회사가 나눈 길 셋) | 회사가 보는 현재 위치를 앎 |
| 21 | metric | bignum |  | chart, bars | 외부 측정 한 줄을 크게 — 내 일과의 연결 (다른 선택 이유: 장면 1·8 과 달리 외부 기관 측정 한 줄) | AI 가 맡는 일의 길이가 빨리 늘고 있음을 앎 |
| 22 | explain | motionboard | footage → kb → chat | footage, checklist, map_causal | 처음 고리의 ① 칸으로 돌아와 '?'로 바뀜 (다른 선택 이유: 장면 10 의 고리를 다시 불러 수미상관) | 앞으로 무엇을 보면 되는지 앎 |
