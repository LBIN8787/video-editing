# 연출 결정 기록 — 20261124-market-deep-nvidia-return

여러 연출·편집·스타일 가운데 이것을 고른 근거와 의도 (manual/05 §0-9, docs/66). 렌더 전에 이 한 장으로 검토합니다.

**결과: 통과**

## 영상 방향

- 고른 것: **hybrid-causal — 원본 발언으로 열고, 공시 숫자를 체크리스트 + 오른쪽 그림·실제 그래프로 쌓는 시장 G 방식**
- 왜: 질문이 '말을 바꾼 이사회'라서 말(원본·인용)과 공시 숫자를 나란히 놓아야 판단이 선다. 숫자는 제 모양(종가 선·막대)으로 그린다
- 의도: 시청자는 복귀의 이유 두 가지와, 복귀가 되돌린 것(사임 할인)과 못 되돌린 것(순환금융·SEC·금리)을 구분하게 된다
- 버린 것: `docu` — 어두운 다큐 판은 레퍼런스 형식을 먼저 고르고 대사를 끼워 맞춘 시범이 기각됨(005·019, v127) — 이 편은 사람의 말과 공시가 주인공
- 버린 것: `moneycrew` — 평면 인포그래픽만으로는 이사회·장관·분석가의 '말'을 원본으로 들려줄 수 없음
- 버린 것: `news-desk` — 한 소식 한 장 카드는 하루 브리핑용 — 이 편은 한 사건을 각도별로 쌓는 심층
- 이 영상의 장면 어휘(닫힌 목록): bars, bignum, bite, checklist, kinetic, map_causal, motionboard, pricewalk, quote
- 근거 문서: manual/09-market-daily.md, docs/68-explainer-docu-benchmark.md, manual/05-style-matching.md, recipe:hybrid-causal, technique:count-up

## 장면마다

| 장면 | 상황 | 고른 것 | 추천(edit-plan) | 버린 것 | 왜 | 의도 |
|---|---|---|---|---|---|---|
| 1 | call-bite | bite | bars → versus → bignum | bars, quote | 반전(복귀 없다 → 5일 뒤 복귀)의 출발점인 의장 발언을 본인 목소리로 들려준다 | 이사회가 '복귀 없다'고 분명히 말했다는 것을 시청자가 직접 듣는다 |
| 2 | metric | bignum | map_causal → kb → chart | map_causal, chart | 숫자 '5일' 하나가 반전의 크기라 크게 새기고, 결의 내용·11일은 말하는 순간 상자로 붙인다 | '5일 만에 뒤집혔다'를 기억하고 다음 질문(왜?)으로 넘어간다 |
| 4 | timeline | checklist | bignum → chart → bars | bignum, timeline | 사임 뒤 일주일을 날짜 순서로 걸고, 복귀를 부르는 쪽(위)과 막는 쪽(아래)을 시간 핀으로 가른다 | 사임 뒤 첫 주에 압력이 어느 쪽에서 왔는지 한 그림으로 본다 |
| 5 | said | quote | bite → footage → quote | bite, footage | 흐름을 바꾼 장관의 말을 출처(보도)와 함께 그대로 보여 준다 | 외부 CEO를 말하던 정부 쪽이 태도를 바꿨다는 것을 안다 |
| 6 | said | quote |  | bite, versus | 같은 사람이 16일과 주말에 다르게 말한 것을 한 카드 위 상자 변화로 보여 준다 | 대통령의 말도 복귀 쪽으로 옮겨 갔다는 것을 본다 |
| 8 | said | quote | versus → bite → compare | versus, bite | 이사회가 공시에 적은 복귀 이유 문장을 원문 그대로 읽힌다 | 복귀 이유 둘(솔직함·지도력, 정부 고위층 의견)을 공시 원문으로 확인한다 |
| 9 | explain | motionboard | versus → bite → compare | versus, map_causal | 여기서부터 해석임을 밝히고, 걸림돌(수출통제·안보)이 풀리는 순서를 카드와 화살표로 잇는다 | 복귀를 막던 것이 개인사가 아니라 수출통제였다는 해석을 근거와 함께 따라간다 |
| 11 | explain | checklist | versus → bite → compare | versus, motionboard | 복귀와 함께 붙은 다섯 조건을 하나씩 켜고, 오른쪽에 돌아온 CEO 둘레로 붙는 감시 장치를 그린다 (다른 선택 이유: 같은 '풀어 주기'지만 9번은 이어진 원인, 11번은 이어지지 않는 조건 목록이라 모양이 다름) | 복귀가 무조건이 아니라 다섯 장치가 붙은 복귀라는 것을 본다 |
| 13 | metric | bars | bignum → chart → bars | chart, bignum | 고점·사임·바닥·복귀 네 종가를 같은 축척 막대로 세우고, -47%·95%를 말하는 순간 상자로 붙인다 (다른 선택 이유: 2번은 간격 하나(5일), 여기는 네 값의 높낮이 — 숫자는 제 모양으로(E4)) | 주가가 어디서 어디까지 빠졌다가 어디로 돌아왔는지 높이로 기억한다 |
| 14 | said | bite | bite → footage → quote | quote, footage | 복귀 전에 '1조 달러'를 말한 분석가의 원본 발언 — 다음 장면의 계산과 맞대기 위해 (다른 선택 이유: 5·6·8번은 원본이 없어 인용 카드, 여기는 방송 원본이 있어 본인 목소리) | 아이브스가 무엇을 예상했는지 직접 듣고, 다음 장면에서 실제 값과 맞대 본다 |
| 15 | metric | pricewalk | bignum → chart → bars | bignum, bars | 대사가 '같은 그래프'를 가리키므로 실제 종가 선을 주인공으로 두고, 말하는 순간 구간·괄호·계산을 붙인다 (다른 선택 이유: 13번 막대는 네 값의 높낮이, 여기는 그 사이 날짜의 흐름과 구간 — 대사가 선 위의 구간을 가리킴) | 하루에 붙은 9,560억 달러와, 10월 고점까지 남은 -31%를 한 그래프에서 구분한다 |
| 16 | media | quote | newspapers → quote | newspapers, bite | 같은 공시를 매체마다 어떻게 읽었는지 제목을 나란히 인용한다 | 포브스·코타쿠·국내 매체가 각각 무엇에 초점을 뒀는지 비교한다 |
| 18 | said | bite | bite → footage → quote | quote, footage | 주장 A('젠슨이 곧 엔비디아')를 그 주장을 한 운용사 대표의 목소리로 연다 (다른 선택 이유: 14번과 같은 이유 — 원본 방송이 있어 본인 목소리) | 주장 A 가 누구의 말인지 듣고 다음 장면에서 그 고리를 따라간다 |
| 19 | explain | motionboard | bars → versus → bignum | bars, versus | 주장 A 의 세 고리(관계를 쥔 사람 → 속도 → 시장의 값)를 화살표로 잇는다 | '젠슨이 곧 엔비디아'가 어떤 고리로 이어지는 주장인지 따라간다 |
| 20 | said | quote | bite → footage → quote | bite, versus | 주장 B('풀린 건 없다')를 지배구조 전문가의 말로 연다 | 반대편 주장이 누구의 말이고 무엇을 문제 삼는지 안다 |
| 21 | compare | checklist | journey → usmap | journey, versus | 주장 B 를 받치는 사실과 어긋나는 사실을 두 칸에 나눠 쌓고 판정을 붙인다 | 주장 B 가 근거는 있지만 '앞으로의 경고'라는 판정을 스스로 따라간다 |
| 22 | cause | map_causal | map_causal → analogy | analogy, motionboard | 두 주장이 갈리는 질문 하나에서 두 결과로 갈라지는 길을 그린다 | 어느 쪽이 맞는지는 '회사 차원이었나'라는 한 질문에 달렸다는 것을 본다 |
| 24 | metric | bignum | map_causal → kb → chart | map_causal, chart | 1부에서 본 약정 3,900억 달러를 한 숫자로 다시 불러 한국 계좌로 잇는다 | 엔비디아의 약정이 한국 메모리 회사의 주문이라는 연결을 다시 떠올린다 |
| 25 | metric | checklist | bignum → chart → bars | bignum, chart | 한 달 하락 → 원인 넷 → 시간 순서 → 24일 첫 반응을 오른쪽 그림으로 차례로 바꾼다 (다른 선택 이유: 같은 숫자 상황이지만 여기는 원인 구분이 핵심이라 목록 + 그림 넷) | 한국 반도체 하락을 황의 사임 하나로 읽지 않고, 24일 반응이 복귀를 처음 반영한 값임을 안다 |
| 26 | timeline | checklist | map_causal → kb → chart | map_causal, bignum | 앞으로 판가름 날 날짜를 시간 핀에 꽂고, 종가가 지키면/무너지면 두 갈래를 붙인다 | 언제 무엇을 보면 어느 주장이 맞는지 스스로 확인할 날짜를 가져간다 |
| 27 | conclusion | kinetic |  | card_type, recap | 영상 전체를 한 문장으로 닫는다 | '돌아왔지만 끝난 건 없다'를 기억한다 |
