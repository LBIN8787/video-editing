# 연출 결정 기록 — 20261126-market-deep-dc-funding

여러 연출·편집·스타일 가운데 이것을 고른 근거와 의도 (manual/05 §0-9, docs/66). 렌더 전에 이 한 장으로 검토합니다.

**결과: 통과**

## 영상 방향

- 고른 것: **hybrid — 사람의 말(인용 카드·원본) + 어두운 무대 모션그래픽 + 공시·연준 원문 문서 (드러켄밀러 틀, 09 §5-00)**
- 왜: 시청자는 '사 주는 쪽이 언제까지 낼 수 있나'의 판단을 들으러 온다 — 사는 쪽 CEO·CFO·회사의 말과 연준의 말을 근거(공시 숫자·연준 원문)로 따진다. 원본 영상이 없어 인용 카드 + 원문 문서로 증거를 보인다
- 의도: 끝나면 시청자는 세 층 그림과 '열쇠는 채권시장'이라는 판단, 판가름 숫자 셋을 안다
- 버린 것: `news-desk` — 소식 하나씩 카드로 넘기면 '앞으로 어떻게 되나'의 판단이 아니라 뉴스 요약이 됨
- 버린 것: `data-report` — 숫자 장면만 이어지면 이름 있는 사람의 결론으로 여는 구조가 사라짐
- 버린 것: `evidence-board` — 사건·인물 연결이 아니라 돈의 흐름·층이 핵심이라 코르크 증거판보다 어두운 무대가 맞음
- 이 영상의 장면 어휘(닫힌 목록): quote, versus, bars, bignum, compare, checklist, motionboard, zoomshot
- 근거 문서: manual/09-market-daily.md, manual/12-visual-storytelling.md, recipe:hybrid-causal

## 장면마다

| 장면 | 상황 | 고른 것 | 추천(edit-plan) | 버린 것 | 왜 | 의도 |
|---|---|---|---|---|---|---|
| 1 | call-bite | quote | bite → quote | bite, bignum | 09 §5-00 결론 먼저 — 사는 쪽에서 가장 많이 쓰는 회사 CEO 의 결론을 첫 화면에, 원문·번역 2단 | 첫 30초에 '사는 쪽은 멈출 생각이 없다'는 결론을 그 사람의 말로 듣는다 |
| 2 | said | quote | map_causal → analogy | map_causal, bite, versus | 맞서는 결론도 이름 있는 기관의 원문으로 — 같은 무게(09 §5-0-2) | '이제 빚이다'라는 반대 결론을 원문으로 듣는다 |
| 3 | compare | versus | map_causal → analogy | map_causal, bars | 두 결론을 좌우로 맞대고 가운데에 이 영상의 해석(열쇠 = 채권시장)을 얹음 | 이 영상이 무엇을 따라가는지(두 말이 둘 다 맞을 수 있는 조건) 안다 |
| 5 | earnings | bars | bars → versus → bignum | versus, bignum | 번 돈·쓴 돈 개념을 처음 세우는 장면 — 막대 두 개가 말과 함께 자람 | 번 돈과 쓴 돈을 구분하고 아마존이 그 차이만큼 비었다는 것을 본다 |
| 6 | metric | bignum | bignum → chart → bars | chart, bars | 아마존 1년 잉여현금흐름 한 숫자를 크게, 장기부채 변화는 작은 숫자로 | 한 분기가 아니라 1년 내내 비었다는 크기를 기억한다 |
| 7 | compare | compare |  | versus, bars | 나머지 네 회사를 같은 두 칸(번 돈·쓴 돈)으로 줄 세워 한 번에 (다른 선택 이유: 네 회사 두 값씩 — 막대 여덟 개보다 표가 한눈에 읽힘(장면 3은 두 결론)) | 아마존만이 아니라 넷 중 셋이 넘친다는 것을 본다 |
| 8 | metric | bars | bignum → chart → bars | bignum, chart | 다섯 곳 합계와 마이크로소프트를 뺀 값을 막대로 맞대 '한 회사가 가려 준다'를 보임 (다른 선택 이유: 116 과 136 두 값을 나란히 — 숫자 하나가 아님) | 합계 116%, 빼면 136% — 위층 한 곳이 나머지를 가린다는 것을 안다 |
| 10 | call-bite | quote | bars → versus → bignum | bite, bars | 두 번째 사는 쪽 목소리 — 리스라는 '보이지 않는 돈'을 그 회사 CFO 의 입으로 | 빈 곳을 메우는 첫 방법(리스)이 있다는 것을 듣는다 |
| 11 | explain-market | motionboard | motionboard → spread → share → afterline | map_causal, share | 리스 → 담보 → 별도 회사에 쌓이는 빚을 카드와 화살표로 한 단계씩(한 문장 한 고리) | 빚이 빅테크 장부가 아니라 다른 곳에 쌓이는 구조를 그릴 수 있다 |
| 12 | metric | bars | map_causal → kb → chart | map_causal, share, bignum | 장부 밖 약속 두 종류(1조·2조)를 막대로 — '할인 안 한 금액' 단서를 출처 줄에 (다른 선택 이유: 두 종류 약속을 나눠 보이려 막대) | 장부 밖 약속의 크기와 성격(비교 한계)을 안다 |
| 13 | say-vs-do | bignum | bignum → chart → bars | versus, compare | '아직 채권시장은 쓰지 않았다' 다음 날의 행동을 숫자 하나로 | 가장 여유 있던 회사도 빚을 꺼냈다는 말과 행동의 차이를 본다 |
| 15 | said | quote |  | bite, checklist | 회사가 스스로 적은 자금 계획 원문 — 네 가지 중 번 돈은 하나 (다른 선택 이유: 회사 보도자료 원문 — 사람 발언(장면 2)과 같은 인용 카드) | 메타가 바깥 돈 셋을 공식 계획으로 적었다는 것을 안다 |
| 16 | earnings | checklist | bignum → chart → bars | bignum, bars, versus | 성격이 다른 세 줄을 말하는 순서대로 하나씩 켜 '지금 → 내년 → 칩 회사의 의향' (다른 선택 이유: 성격이 다른 세 줄(지금·내년·의향)이라 막대 대신 목록) | 주식으로 얼마를 언제 모으는지, 칩 회사가 사는 쪽 주식을 산다는 그림을 안다 |
| 17 | say-vs-do | compare | motionboard → spread → share → afterline | motionboard, versus, bars | 1년 전 vs 지금, 두 회사 — 0 이 표에서 더 또렷 (다른 선택 이유: 1년 전 vs 지금의 행동 비교라 표) | 자사주가 멈췄다는 사실을 숫자로 본다 |
| 18 | metric | bars | bignum → chart → bars | bignum, compare | 금고가 가득한데 밖에서 돈을 구한 모순을 막대 길이로 (다른 선택 이유: 금고(2,651억)와 밖에서 구한 돈의 크기 대비가 메시지라 막대) | 금고가 비어서가 아니라 추가분을 밖에서 가져왔다는 것을 본다 |
| 19 | point | zoomshot | bignum → chart → bars | bars, bignum | 증거 → 실제 자료(README §2-6): 연준 원문 문장을 가리켜 6,800억·31% | 이 숫자가 중앙은행 보고서 원문에 있다는 것을 눈으로 본다 |
| 21 | explain-market | motionboard | motionboard → spread → share → afterline | compare, map_causal | 모아 보기(09 §5-00 ④) — 세 층을 위에서 아래로 쌓아 앞 장면들을 한자리에 (다른 선택 이유: 같은 상황 — 이번엔 층(위·가운데·아래)을 쌓는 무대) | 같은 빅테크가 아니라 세 층이라는 그림을 머리에 남긴다 |
| 22 | earnings | bars | bars → versus → bignum | versus, bignum | 코어위브의 산수를 막대로 — 이자 막대가 영업이익의 네 배로 솟음 (다른 선택 이유: 세 숫자의 크기 대비라 막대) | 맨 아래층은 이자가 이익을 넘는다는 것을 본다 |
| 23 | metric | bignum | bignum → chart → bars | bars, chart | 민감도 계산(03 §0-4 ⑥)을 한 숫자로, 가정은 화면 출처 줄에 밝힘 (다른 선택 이유: 가정 계산 결과 하나 — 가정을 출처 줄에) | 금리 1%p 가 이 회사에 얼마나 큰지 감을 잡는다 |
| 24 | earnings | checklist | bignum → chart → bars | bignum, bars, versus | 오라클은 숫자와 사건이 섞여 있어 줄마다 켜는 목록 (다른 선택 이유: 성격이 다른 사실 셋(이자·계약·보도)을 순서대로 — 막대로 묶을 수 없음) | 오라클은 코어위브보다 한 칸 위지만 약속이 크다는 것을 안다 |
| 26 | compare | compare | map_causal → kb → chart | map_causal, versus, bars | 반대편이 문제 삼는 고리(돈의 출처)를 그들의 표 그대로 (다른 선택 이유: 두 시기 × 세 항목 표 — 결론 맞대기(장면 3)와 다름) | 사는 쪽은 빚을 늘리고 칩 회사는 갚았다는 것을 안다 |
| 27 | point | zoomshot | map_causal → kb → chart | map_causal, chart, quote | 연준 원문 문장 끝의 '적어도 올해까지는'을 직접 가리킴 — 이 영상의 전환점 | 통신 붐과의 차이(빚)가 올해 줄기 시작했다는 근거를 원문으로 본다 |
| 28 | compare | bars | bignum → chart → bars | versus, bignum | 같은 우량 등급인데 AI 빚만 더 비싸졌다는 차이를 막대로 (다른 선택 이유: 두 값의 크기 차이가 메시지라 막대) | 빌려주는 쪽이 AI 빚에 값을 더 매기기 시작했다는 것을 본다 |
| 29 | said | versus | versus → bars → compare | quote, bite | 같은 채권시장 안의 반대 시각을 같은 무게로 좌우에 (다른 선택 이유: 두 사람의 엇갈린 말을 한 화면에 — 결론 맞대기) | 두 시각이 '어느 층을 보나'에서 갈린다는 것을 안다 |
| 31 | explain-market | motionboard | bignum → chart → bars | bignum, map_causal, bars | 사는 쪽 빚 → 칩값 → 파는 쪽 현금, 돈의 방향을 화살표로 (다른 선택 이유: 같은 상황 — 이번엔 돈의 방향(화살표)) | 빌린 돈의 상당 부분이 파는 쪽 현금으로 쌓였다는 연결을 본다 |
| 32 | earnings | checklist | bars → versus → bignum | versus, bars | 장기계약이 묶는 것(물량)과 못 묶는 것(지불 능력)을 두 줄로 (다른 선택 이유: 묶는 것/못 묶는 것 두 줄의 대비) | '장기계약 = 수요 확정'이라는 오해를 고친다 |
| 33 | said | versus | bars → versus → bignum | quote, bars | 국내 두 시각을 같은 무게로 — 무엇을 보는지(사는 쪽 돈 / 파는 쪽 사이클) 라벨에 (다른 선택 이유: 국내 증권가 두 시각을 좌우로) | 두 시각이 다른 것을 보고 있다는 것을 안다 |
| 35 | next-week | checklist | bignum → chart → bars | bignum, timeline, versus | 틀리는 경우 셋을 하나씩 켜는 목록(09 §5-0-1) | 이 해석이 틀릴 조건을 안다 |
| 37 | next-week | checklist | bars → versus → bignum | timeline, bars | 판가름 숫자 셋을 기준선과 함께 — 줄마다 날짜 | 다음에 무엇을 보면 되는지 숫자로 안다 |
