# 연출 결정 기록 — 20261122-market-deep-nvidia-circular

여러 연출·편집·스타일 가운데 이것을 고른 근거와 의도 (manual/05 §0-9, docs/66). 렌더 전에 이 한 장으로 검토합니다.

**결과: 통과**

## 영상 방향

- 고른 것: **hybrid-causal — 원본 발언으로 열고, 공시 숫자를 체크리스트 + 오른쪽 그림·실제 그래프로 쌓는 시장 G 방식**
- 왜: 순환금융은 '돈이 도는 길'이 핵심이라 원리는 움직이는 관계도로, 크기는 막대·숫자로, 위험 신호는 체크리스트 + 그림으로 나눈다
- 의도: 시청자는 순환금융이 가짜 매출이 아니라 위험이 한곳에 겹치는 구조라는 것과, 무엇을 보면 고리가 약해지는지 안다
- 버린 것: `docu` — 어두운 다큐 판은 레퍼런스 형식을 먼저 고르고 대사를 끼워 맞춘 시범이 기각됨(005·019, v127) — 이 편은 사람의 말과 공시가 주인공
- 버린 것: `moneycrew` — 평면 인포그래픽만으로는 이사회·장관·분석가의 '말'을 원본으로 들려줄 수 없음
- 버린 것: `news-desk` — 한 소식 한 장 카드는 하루 브리핑용 — 이 편은 한 사건을 각도별로 쌓는 심층
- 이 영상의 장면 어휘(닫힌 목록): bars, bignum, bite, checklist, kinetic, motionboard
- 근거 문서: manual/09-market-daily.md, docs/68-explainer-docu-benchmark.md, manual/05-style-matching.md, recipe:hybrid-causal, technique:count-up

## 장면마다

| 장면 | 상황 | 고른 것 | 추천(edit-plan) | 버린 것 | 왜 | 의도 |
|---|---|---|---|---|---|---|
| 1 | call-bite | bite | bite → quote | quote | 의심에 대한 회사의 답을 당시 임시 CEO 본인 목소리로 연다 | 회사가 '아니다'라고 답했다는 것을 직접 듣고, 그럼 무엇이 사실인지 궁금해진다 |
| 2 | metric | bignum | newspapers → quote | newspapers, bars | 실적 자료의 보증 1,180억 달러를 새기고, 순환금융의 세 고리를 말하는 순간 상자로 붙인다 | 보증의 크기와 순환금융이 무엇으로 이뤄지는지(보증·지분·임대) 안다 |
| 3 | timeline | checklist | map_causal → kb → chart | map_causal, bignum | 지금 이 고리를 둘러싼 의심을 일어난 순서대로 켠다 (사임·복귀, SEC 보도 …) | 이 편이 왜 지금 나오는지 사건 순서로 안다 |
| 4 | question | checklist | map_causal → kb → chart | map_causal, card_type | 흔한 생각 세 가지를 명제로 세워 두고 영상이 하나씩 답한다 | 자기가 가진 생각이 셋 중 무엇인지 짚고 답을 기다린다 |
| 6 | explain | motionboard | versus → bars → compare | versus, map_causal | 돈이 파는 쪽에서 사는 쪽으로, 다시 파는 쪽으로 도는 길을 화살표로 한 바퀴 그린다 | 순환금융의 원리를 한 바퀴 도는 그림으로 이해한다 |
| 7 | explain | motionboard | card_type → chapter | card_type, versus | '가짜 매출일까?'에서 갚으면/무너지면 두 갈래로 가르고, 빅테크·주문을 말하는 순간 덧붙인다 | 매출은 진짜지만 위험이 겹친다는 구분을 한 그림으로 가져간다 |
| 9 | metric | bars | bignum → chart → bars | bignum, chart | 고객 쪽에 걸어 둔 네 가지를 같은 축척 막대로 세우고, 한 분기 매출·1년 전 메모를 말하는 순간 붙인다 (다른 선택 이유: 2번은 보증 하나의 크기, 여기는 네 항목 견주기 — 같은 축척(E5)) | 하나하나가 한 분기 매출과 견줄 크기라는 것을 막대 길이로 본다 |
| 10 | explain | checklist | bars → versus → bignum | bars, motionboard | '매출 대부분이 자기 돈'이라는 오해를 조건 하나씩 풀어 준다 (다른 선택 이유: 6·7번은 돈이 도는 길(관계), 여기는 오해를 푸는 조건 목록) | 보증이 바로 매출을 만든 것이 아니라 조건부라는 것을 안다 |
| 12 | metric | bignum | bignum → chart → bars | chart, bars | 같은 틀의 과거 사례 루슨트를 숫자 하나로 세우고, 파산·약정 축소를 말하는 순간 붙인다 | 파는 쪽이 사는 쪽에 돈을 댄 끝이 어땠는지 숫자로 본다 |
| 13 | compare | checklist | versus → bars → compare | versus, bars | 루슨트와 엔비디아의 같은 점·다른 점을 하나씩 켜고 점 격자로 비중을 보여 준다 | 엔비디아가 루슨트와 어디가 같고 어디가 다른지 스스로 구분한다 |
| 15 | metric | bars | bignum → chart → bars | bignum, chart | 아직 받지 못한 칩값이 1월에서 10월로 늘어난 것을 막대로 보여 준다 (다른 선택 이유: 9번과 같은 막대지만 여기는 한 항목의 시점 변화) | 칩값을 받는 데 시간이 더 걸리기 시작했다는 첫 신호를 본다 |
| 16 | hub-event | checklist | bignum → chart → bars | bignum, map_causal | 고리가 약해지는 신호 다섯을 하나씩 켜고, 오른쪽 그림을 신호마다 바꾼다 (손상·빈 그릇·시간 줄·하락) | 지금 보이는 신호가 무엇이고 각각 얼마나 큰지 안다 |
| 18 | explain-market | motionboard | zoomshot | zoomshot, map_causal | 엔비디아의 약정이 한국 메모리 회사의 주문으로 이어지는 길을 말하는 순간 카드로 잇는다 | 순환금융이 한국 메모리 회사의 장기 계약과 이어진다는 것을 안다 |
| 19 | cause | checklist | bars → versus → bignum | bars, map_causal | 이 설명이 틀리는 조건을 하나씩 켜고 '만약 → 그러면'으로 결과를 붙인다 | 이 설명이 언제 틀리는지 알고 자기 판단의 경계를 정한다 |
| 20 | next-week | checklist | zoomshot | zoomshot, timeline | 다음 소식을 읽을 때 볼 지표 넷을 목록으로 남긴다 | 다음 실적에서 무엇을 보면 고리가 약해지는지 스스로 읽는다 |
| 21 | conclusion | kinetic | map_causal → kb → chart | map_causal, card_type | 순환금융의 정의를 한 문장으로 닫는다 | '가짜 매출이 아니라 주문을 당겨 온 것'을 기억한다 |
