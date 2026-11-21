# 팩트시트 — 11월 21일(토) 심층: AI 반도체 동반 폭락 — 수요가 꺾였나, 몫이 옮겨 갔나

기준: 시세는 **11월 20일(금) 미국 마감**·**11월 20일(금) 한국 마감**, 소식은 **11월 21일 11시(한국 시간)까지**. ✅ 1차 출처·시세 · ⚠️ 보도(원문 접근 못 함 또는 회사 확인 없음) · 💭 인사이트(이름 있는 사람·매체의 시각) · 💬 이 채널의 해석
원인 종류: **이슈**(엔비디아 SEC 회계 조사 보도 — 아침 브리핑에서 다룸) + **보고서**(궈밍치 TF 인터내셔널 업계 조사 — 구글 TPU) + **전망**(쿡 연준 이사 연설, 마이크론·SK하이닉스 회사 전망) + **실적**(엔비디아 3분기 8-K, SK하이닉스 3분기 발표 — 지난 실적이 수요의 기준선)
브리핑/심층: **심층** — manual/09 §2 '매일 두 편'(2026-11-21 사용자). 아침 브리핑(20261121-market-daily)이 그날 전체를 짧게 다뤘고, 이 편은 그중 가장 큰 줄기 'AI 반도체 동반 폭락' 하나를 산업·수요·기술로 깊게 본다. 브리핑의 엔비디아 SEC 보도·세무 조사 비유·한국 시간 순서 장면은 반복하지 않음(§13).
원본 발언: 당사자 영상 없음 — 쿡 이사 연설은 연준 사이트에 영상 없이 원문만, 마이크론·SK하이닉스는 실적 콜(녹음, 이 PC 에서 구간 받기 못 함 — 공식 영상 주소 미확인), 그리핀은 시타델 행사(공식 영상 주소 미확인). → **문서형 심층**: 1차 문서 짧은 인용 + 인사이트 5명 + 직접 계산 + 틀리는 경우 (manual/09 §2, 2026-11-21).

## 핫 키워드
- daily_brief ⑤ 주제어: 급락(9) · 전망(5) · 인상(5) · AI(4) · 금리(4) · 연준(3) — ③ 보도량: 엔비디아·마이크론·AMD
- 국내 제목 반복: '검은 금요일'(연합뉴스·중앙일보 등) · 'AI 투자 우려'(마이크론 특징주 기사) · '폭락'
- ⑥-1 CEO 소식 반복: 마이크론 CEO '2027·2028 더 빠듯' · 마이클 버리 '경고했다' · 드러켄밀러 '반도체에서 물러남' · 쿡 '인상 필요'(로이터 제목)
- → 썸네일 큰 글씨·제목 앞 20자: **반도체 폭락 · 메모리 품절 · 연준** (검은 금요일은 브리핑 썸네일과 겹치므로 B 변형에만)

## 시장 한 장 (11월 20일 금요일 미국 마감, 야후 파이낸스 차트 — 19일 종가 대비)
- M1 ✅ S&P 500 6,910.39 (-3.70%) · 나스닥 22,617.73 (-5.28%) · 필라델피아 반도체 8,408.59 (-10.73%) · VIX 35.89 (+26.20%) · 미 10년물 4.91% (19일 5.05%) — https://finance.yahoo.com/quote/%5ESOX/history
- M2 ✅ 종목 하루: 엔비디아 125.53달러 (-14.01%) · 마이크론 594.51 (-13.89%) · AMD 424.39 (-13.25%) · 브로드컴 304.41 (-12.19%) · TSMC(ADR) 318.71 (-9.48%) · 알파벳 A 265.29 (-2.70%) — https://finance.yahoo.com/quote/MU/history
- M3 ✅ 한 달 (10월 21일 종가 → 11월 20일 종가, 야후 차트 `01_research/prices`): 엔비디아 221.97 → 125.53 (-43.4%) · **마이크론 913.67 → 594.51 (-34.9%)** · 반도체 지수 11,505.56 → 8,408.59 (-26.9%) · TSMC ADR -26.2% · AMD -23.2% · 알파벳 -20.8% · 나스닥 -15.3% · 브로드컴 337.80 → 304.41 (-9.9%)
- M4 ✅ 한국 (11월 20일 금요일 마감, 미국 20일 폭락 **전**): 삼성전자 183,100원 (-7.01%) · SK하이닉스 1,113,000원 (-5.92%) · 한 달(10월 21일 → 11월 20일) 삼성전자 223,500 → 183,100 (-18.1%) · SK하이닉스 1,294,000 → 1,113,000 (-14.0%) — 야후(한국거래소 종가) · 코스피 4,869.96 (-5.21%) ⚠️ 보도(연합뉴스 등)

## 이야기 1 — 수요의 숫자: 회사들이 내놓은 수요 기준선
- D1 ✅ 엔비디아 3분기(10월 25일까지) 매출 1,158억 달러(+103%, 1년 전 대비) · **데이터센터 1,076억 달러(+110%)** · 4분기 전망 1,300억 ±3%(한 주 더 많은 분기, 중국 데이터센터 매출 가정 없음) · 매출총이익률 74.8% — 엔비디아 실적 발표(8-K, 2026-11-17) https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Third-Quarter-Fiscal-2027/default.aspx
- D2 ✅ 콜레트 크레스(임시 CEO): "Vera Rubin is off to an explosive start, our roadmap is on track and our ambition has never been greater." — 같은 발표
- D3 ⚠️ 마이크론 산제이 메로트라 CEO(회계 4분기 실적 콜, 2026년 9월 30일 무렵): "We expect memory and storage supply-demand conditions to be much tighter in calendar 2027 and 2028 than they were in 2026" · "We do not have line of sight to when supply and demand will return to balance." · 2027년 생산량의 75% 넘게 이미 약정, 고객 협상 대부분은 2028년 — 컴퓨터월드(2026-10-01) https://www.computerworld.com/article/4229635/memory-squeeze-set-to-tighten-through-2028-micron-says-3.html · 같은 내용 레지스터·벤징가
- D4 ✅ SK하이닉스 3분기(2026-10-28 발표, 잠정): 매출 104조 6,155억 원 · 영업이익 83조 3,338억 원 · **영업이익률 80%**(2분기 76%) · 14개 주요 고객과 장기 공급 계약(LTA), "The LTA volume secured to date corresponds to more than 50% of total production capacity for 2027 and 2028." · "it expects the structure in which demand exceeds supply to persist through 2030." · 4분기 HBM4 가 출하·매출에서 HBM3E 를 넘을 것 — SK하이닉스 뉴스룸 https://news.skhynix.com/en/q3-2026-business-results/
- D5 ✅ 리사 쿡 연준 이사(11월 20일 칠레 중앙은행 연례 회의): "Companies have announced plans for more than $2 trillion in specific data center construction projects." · "So far, only a fraction of this has been realized." — https://www.federalreserve.gov/newsevents/speech/cook20261120a.htm
- 💬 I1 금요일까지 나온 회사 숫자 가운데 '수요가 줄었다'는 것은 없다: 엔비디아는 다음 분기 매출을 1,158억 → 1,300억으로, 마이크론은 2027년 물량 75%+ 약정, SK하이닉스는 2027·2028년 생산능력 절반 넘게 장기 계약. 그런데 그 '품절'이라는 마이크론이 한 달에 34.9% 빠졌다 — 근거 D1·D3·D4·M3

## 이야기 2 — 몫의 이동: 같은 AI 안에서 누구의 주문이 옮겨 가나
- S1 ⚠️ 궈밍치(TF 인터내셔널 증권) 업계 조사: 구글이 2027년 브로드컴 설계 TPU '8i' 출하 계획을 약 100만 개(예상 물량의 약 20%, 약 500만 → 약 400만 추정) 줄이고, 미디어텍 설계 '8t' 출하를 늘릴 계획(규모 미공개). 줄인 몫 대부분은 값비싼 '8i 맥스'. 이유로 구글이 공급망·데이터센터 전력 제약 속 최첨단 모델 개발을 우선 — 회사 발표 아님, 구글·브로드컴 논평 없음 — 인베스팅닷컴(야후 파이낸스 UK, 2026-11-21) https://uk.finance.yahoo.com/news/google-reportedly-cuts-broadcom-designed-165518878.html
- S2 ⚠️ 같은 기사: 브로드컴 하락을 이 조사 하나로만 돌리면 안 된다(반도체 전반 매도)
- S3 ✅ 브로드컴 한 달 -9.9%로, 반도체 지수(-26.9%)보다 훨씬 덜 빠졌다 — 야후 (M3)
- 💬 I2 궈밍치 조사의 핵심은 '구글이 TPU 를 덜 산다'가 아니라 '같은 TPU 안에서 비싼 설계 → 다른 설계로 몫이 옮겨 간다'이고, 그 이유가 '전력이 모자라서 고른다'는 것 — 수요가 아니라 **병목**이 주문을 고르게 만든다 — 근거 S1

## 이야기 3 — 값의 이동: 모자라면 값이 오르고, 남으면 무너진다
- G1 💭 켄 그리핀(시타델 CEO, 2026-10-20 시타델 '글로벌 시장의 미래' 행사, 뉴욕): AI 는 "almost certainly" 거품 · "Any radical transformation of our economy is generally intertwined with a bubble." · GPU 는 돌리는 추가 비용이 낮아 공급이 수요를 넘으면 값이 급락할 수 있다(항공 좌석 비유 — 기사 요약), 2000년 무렵 광케이블 과잉 투자 뒤 값 하락과 비교 — 디크립트(2026-10-21) https://decrypt.co/381578/ken-griffin-ai-bubble-gpus-airline-seats
- G2 💭 마이클 버리(사이언 자산운용): 그리핀의 GPU 경고를 X 게시물로 지지 — 보도(TIKR·크립토브리핑, 2026-10월 말) https://www.tikr.com/blog/michael-burry-backs-ken-griffins-obvious-gpu-warning-as-market-risk-multiplies · 원문 게시물 주소 미확인 → 대본엔 '보도'로만, 문장 인용 안 함
- G3 ⚠️ 반론 보도: 지금 GPU 임대 값은 공급 과잉을 보여 주지 않는다 · 전력을 못 받는 칩은 과잉을 만들 수 없다 — 같은 보도 묶음(검색 요약) → 대본엔 쓰지 않음(출처 문장 미확인)
- G4 ✅ 마이크론 CFO 마크 머피: "inventory levels and supply remain extremely tight." · 회계 4분기 D램 가격 10%대 후반, 낸드 약 30% 올랐다 — 컴퓨터월드 (D3)
- 💬 I3 메모리 회사의 이익은 '모자람'에서 나온다(SK하이닉스 영업이익률 80%). 시장이 사는 건 오늘의 품절이 아니라 '언제까지 모자라냐'이고, 그리핀의 경고는 그 끝이 오면 값이 한꺼번에 무너질 수 있다는 것 — 근거 D4·G1·G4

## 이야기 4 — 돈의 값: 연준이 본 AI 건설
- F1 ✅ "The AI infrastructure buildout I previously discussed is a significant contributor to this acceleration." · "The current stance of policy does not appear to be curtailing the AI buildout." · "Furthermore, waiting longer to implement rate increases risks getting behind the curve." · 10월 PCE 물가 3.8%, 근원 3.2%, 물가가 2% 목표를 67개월째 넘음("has been for 67 months") — 쿡 연설 (D5 같은 주소)
- F2 ✅ 쿡 이사는 AI 건설이 칩·첨단 장비 값, 건설 임금, 전기료로 번진다고 짚음(연설 요지) · 10월 동결 때 0.25%p 인상을 주장하며 반대 — 같은 연설
- F3 ✅ 다음 FOMC 12월 8~9일(한국 시간 10일 새벽 결과) — https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm
- F4 ✅ 미 10년물 4.91% (19일 5.05%) — 야후 (M1)
- 💬 I4 연준 이사가 '지금 금리로는 AI 건설이 줄지 않는다'고 말한 건, 거꾸로 '줄 때까지 올릴 수 있다'로 들린다. AI 칩 수요의 적이 기술이 아니라 **돈의 값**이 될 수 있다는 것 — 다만 한 사람의 시각이고, 같은 날 10년물은 내렸다 — 근거 F1·F4

## 이야기 5 — 돈을 굴리는 사람의 행동
- H1 ⚠️ 스탠리 드러켄밀러(듀케인 패밀리 오피스) 13F(9월 30일 기준, 11월 16일 무렵 제출): TSMC 보유 94% 줄임 · AMD·샌디스크·알파벳 등 반도체 관련 8종목 전량 정리 · 금광주(뉴몬트 약 4,400만·배릭 약 4,300만·애그니코 이글 약 4,200만 달러) 새로 삼 · 시게이트 약 3배로 늘림 · 미국 주식 포트폴리오 52억 1천만 → 44억 7천만 달러 — 보도(빌리어네어스 아프리카·뉴스퀙·노던마이너, 2026-11-18 무렵 — SEC 13F 원문 직접 확인 못 함) https://www.newsquawk.com/headlines/druckenmiller-13-f-raises-stake-in-stx-cuts-tsm · https://www.northernminer.com/news/druckenmiller-exits-copper-steel-to-buy-gold-miners/1003897930/
- H2 13F 의 한계: 9월 30일 시점의 미국 상장 주식 매수 포지션만 — 공매도·채권·통화·원자재는 안 보임 (위 보도)
- 💬 I5 드러켄밀러의 행동은 '말'이 아니라 '사실'(공시)이다. 다만 9월 말 기준이라 이번 폭락 전 행동이고, 반도체 안에서도 저장장치(시게이트)는 늘렸다 — 반도체 전체를 버린 게 아니라 고른 것 — 근거 H1·H2

## 이야기 6 — 한국: 모자람의 편에 선 계좌
- K1 ✅ SK하이닉스 영업이익률 80%, 장기 계약이 2027·2028 생산능력의 50% 넘음 (D4)
- K2 ✅ 삼성전자 -7.01%, SK하이닉스 -5.92%(20일) · 한 달 -18.1%·-14.0% (M4)
- K3 ✅ 한국 20일 장은 미국 20일 폭락 전에 닫힘 → 23일(월) 장이 첫 반영 (브리핑에서 다룸 — 이 편은 한 문장만)
- 💬 I6 한국 메모리는 '모자람' 쪽에 서 있다. 그래서 확인할 것은 수요의 크기보다 ① 장기 계약이 그대로 유지되는지 ② 메모리 값이 계속 오르는지 ③ 구글처럼 '고르는' 고객이 메모리 쪽에서도 나오는지 — 근거 D3·D4·S1

## 직접 계산
- C1 마이크론 594.51 ÷ 913.67 − 1 = -34.9% (한 달)
- C2 엔비디아 데이터센터 1,076 ÷ 전체 1,158 = 92.9% · 4분기 전망 1,300 ÷ 3분기 1,158 − 1 = +12.3%
- C3 SK하이닉스 83조 3,338억 ÷ 104조 6,155억 = 79.7% (회사 표기 80%)
- C4 브로드컴 한 달 -9.9% vs 반도체 지수 -26.9% → 17%p 덜 빠짐
- C5 궈밍치 조사: 100만 ÷ 약 500만 = 약 20% (추정치 기준)
- C6 드러켄밀러 미국 주식 44.7 ÷ 52.1 − 1 = 약 -14% (6월 말 → 9월 말)
- C7 마이크론 하루 -13.89% − 반도체 지수 -10.73% = -3.16%p

## 해석
- 💬 I1 수요 숫자는 꺾이지 않았는데, '품절' 회사가 한 달 -34.9% — 근거 D1·D3·D4·M3
- 💬 I2 구글 TPU 조사는 수요 감소가 아니라 병목(전력)이 주문을 고르게 만드는 이야기 — 근거 S1
- 💬 I3 메모리 이익은 모자람에서 나오고, 시장은 '언제까지 모자라냐'를 산다 — 근거 D4·G1·G4
- 💬 I4 연준 이사: 지금 금리로는 AI 건설이 줄지 않는다 → AI 칩의 적이 돈의 값이 될 수 있다 — 근거 F1·F4
- 💬 I5 드러켄밀러는 반도체를 버린 게 아니라 골랐다(9월 말, 폭락 전) — 근거 H1·H2
- 💬 I7 정리: 금요일 동반 폭락이 사고 있는 것은 '수요가 꺾였다'는 증거가 아니라, ① 몫이 옮겨 간다(구글 TPU) ② 모자람이 언젠가 끝난다(그리핀) ③ 돈의 값이 오른다(쿡) 세 가지 '아직 오지 않은 일'의 값이다 — 근거 S1·G1·F1·D1

## 인사이트 (💭 — 사실이 아니라 이름 있는 사람·매체의 시각)
| 누가 (이름·직함·소속) | 어디서 (매체·방송·자리) | 국내·해외 | 날짜 | 원문 한 줄 | 입장 | 근거로 든 것 | 출처 주소 |
|---|---|---|---|---|---|---|---|
| 산제이 메로트라 (마이크론 CEO) | 회계 4분기 실적 콜 (컴퓨터월드 인용) | 해외 | 2026-09-30 | "We do not have line of sight to when supply and demand will return to balance." | 낙관(공급 부족 지속) | 2027년 물량 75%+ 약정 | https://www.computerworld.com/article/4229635/memory-squeeze-set-to-tighten-through-2028-micron-says-3.html |
| 켄 그리핀 (시타델 CEO) | 시타델 '글로벌 시장의 미래' 행사 (디크립트 보도) | 해외 | 2026-10-20 | "Any radical transformation of our economy is generally intertwined with a bubble." | 우려 | GPU 공급 과잉 시 값 급락, 2000년 광케이블 | https://decrypt.co/381578/ken-griffin-ai-bubble-gpus-airline-seats |
| 리사 쿡 (연준 이사) | 칠레 중앙은행 연례 회의 연설 | 해외 | 2026-11-20 | "The current stance of policy does not appear to be curtailing the AI buildout." | 우려(금리 인상) | PCE 3.8%, AI 건설이 물가에 기여 | https://www.federalreserve.gov/newsevents/speech/cook20261120a.htm |
| 궈밍치 (TF 인터내셔널 증권 애널리스트) | 업계 조사 (인베스팅닷컴 보도) | 해외 | 2026-11-20 | 구글이 2027년 브로드컴 설계 TPU 출하 계획을 약 100만 개 줄이고 미디어텍 설계 칩을 늘림 (기사 요약) | 우려(브로드컴)·중립(구글 TPU 전체) | 업계 조사, 전력 제약 | https://uk.finance.yahoo.com/news/google-reportedly-cuts-broadcom-designed-165518878.html |
| 콜레트 크레스 (엔비디아 임시 CEO) | 3분기 실적 발표문 | 해외 | 2026-11-17 | "Vera Rubin is off to an explosive start, our roadmap is on track and our ambition has never been greater." | 낙관 | 데이터센터 +110%, 4분기 1,300억 | https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Third-Quarter-Fiscal-2027/default.aspx |
| SK하이닉스 (회사) | 3분기 실적 발표 | 국내 | 2026-10-28 | "it expects the structure in which demand exceeds supply to persist through 2030." | 낙관 | 14개 고객 장기 계약 | https://news.skhynix.com/en/q3-2026-business-results/ |
| 스탠리 드러켄밀러 (듀케인) | 13F 공시 (행동 — 보도로 확인) | 해외 | 2026-11-16 | (말 아님) TSMC 94% 줄임, AMD·샌디스크·알파벳 정리, 금광주 매수 | 우려(행동) | — | https://www.newsquawk.com/headlines/druckenmiller-13-f-raises-stake-in-stx-cuts-tsm |

- 맞대기: 메로트라 '균형이 언제 올지 안 보인다' ↔ 받치는 숫자: SK하이닉스 장기 계약 50%+, 영업이익률 80% (D4) / 어긋나는 숫자: 마이크론 주가 한 달 -34.9% (M3) — 시장은 회사 말을 믿지 않거나, 이미 값에 들어 있었다고 봄
- 맞대기: 그리핀 '거품, 남으면 값이 무너진다' ↔ 받치는 것: 2000년 광케이블 (그의 비교) / 어긋나는 숫자: 지금 메모리는 모자라고 값이 오르는 중(D램 10%대 후반, G4)
- 맞대기: 쿡 '지금 금리로는 AI 건설이 안 줄어든다' ↔ 받치는 숫자: PCE 3.8%, 데이터센터 계획 2조 달러+ (F1·D5) / 어긋나는 숫자: 같은 날 10년물 5.05 → 4.91% (F4)
- 맞대기: 크레스 '야망이 이보다 컸던 적 없다' ↔ 받치는 숫자: 4분기 전망 +12.3% (C2) / 어긋나는 숫자: 주가 한 달 -43.4% (M3)
- 맞대기: 궈밍치 조사 ↔ 회사 확인 없음, 2027년 '계획' 숫자 (S1) — 브로드컴 한 달 -9.9%로 반도체 지수보다 덜 빠짐(C4)

## 주장 해부 (2026-11-21 사용자: "거품이라는 주장을 뜯어보고 아니라는 주장도 심화적으로")
| 주장 | 고리 | 받치는 사실 | 어긋나는 사실 | 판정 |
|---|---|---|---|---|
| 거품론(그리핀) | ① 큰 변화는 늘 과잉투자 | 2001년 광케이블 85~95% 미사용·대역폭 값 약 -90% (포춘 2025.9) https://fortune.com/2025/09/28/ai-dot-com-bubble-parallels-history-explained-companies-revenue-infrastructure/ | 그 광케이블은 결국 쓰였다(같은 기사) | 근거 있음 |
| 거품론 | ② 투자가 매출보다 빠르다 | 2026 빅테크 설비투자 약 7,250억 달러(골드만삭스 추정, 추정치 6,300억~9,000억) · 세쿼이아 칸(2024) '연 6,000억 달러 매출 필요' · 버리: 칩 수명 5~6년 회계가 비용을 작게(2026~28 1,760억 달러, 그의 추정) | 엔비디아 '오래된 GPU 도 다 쓰인다' 반박 메모 · 메타 5.5년 연장, 아마존 6→5년 단축(2025) | 근거 있음(크기는 추정) |
| 거품론 | ③ 칩이 남기 시작했다 | — | H100 임대료 중간값 약 3.9~4.1달러, 한 집계 1년 +52%(컴퓨트센서스·피니타이저, 11월) — 남는 물건 값이 오르는 중 | 근거 약함(지금은) |
| 모자람론(메로트라·SK하이닉스) | ① 내년 물량이 팔렸다 | 마이크론 2027년 75%+ · SK하이닉스 2027·28 생산능력 50%+ 장기 계약 | 장기 계약도 재협상 가능 | 근거 있음 |
| 모자람론 | ② 전기가 없어 더 못 짓는다 | 2026 계획 16GW 중 착공 5GW(사이트라인 클라이밋, 블룸버그 보도) · PJM 2027~28 6.6GW 부족 전망 | 현장 가스 발전으로 우회하는 사례 | 근거 있음 — 2000년 광케이블과 다른 점 |
| 모자람론 | ③ 임대료가 오른다 | 위 임대료 집계 | 오른 건 오늘의 값 — 전기가 풀리면 공급이 한꺼번에 | 근거 있음(지금) |
| **갈리는 곳** | 시간: 거품론은 몇 년 뒤 공급·회계, 모자람론은 오늘 주문·임대료 | 판가름: GPU 임대료 꺾임 · 메모리 장기 계약 재협상 · 빅테크 설비투자 하향 · 전력 연결 속도 | | |

## CEO 소식
| CEO (회사) | 날짜 | 말했나·했나 | 원문 한 줄 또는 공시 | 출처 주소 | 오늘 이야기와의 연결 |
|---|---|---|---|---|---|
| 산제이 메로트라 (마이크론) | 2026-09-30 | 말 | "much tighter in calendar 2027 and 2028 than they were in 2026" | https://www.computerworld.com/article/4229635/memory-squeeze-set-to-tighten-through-2028-micron-says-3.html | '품절' 회사의 주가 한 달 -34.9% |
| 콜레트 크레스 (엔비디아 임시 CEO) | 2026-11-17 | 말 | "our ambition has never been greater." | https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Third-Quarter-Fiscal-2027/default.aspx | 수요 기준선 |
| 켄 그리핀 (시타델) | 2026-10-20 | 말 | "almost certainly" 거품 (기사 인용) | https://decrypt.co/381578/ken-griffin-ai-bubble-gpus-airline-seats | 모자람이 끝나는 날 |
| 스탠리 드러켄밀러 (듀케인) | 2026-11-16 | 했음 (13F, 보도) | TSMC -94%, AMD 정리, 금광주 매수 | https://www.newsquawk.com/headlines/druckenmiller-13-f-raises-stake-in-stx-cuts-tsm | 고르는 돈 |

## 영상 소스
| 누가 | 채널 (공식) | 영상 제목 | 날짜 | 주소 | 쓸 문장 (원문) | 권리 | 상태 |
|---|---|---|---|---|---|---|---|
| 리사 쿡 | 연준 (federalreserve.gov) | 연설 원문 (칠레 행사 — 연준 사이트에 영상 없음) | 2026-11-20 | https://www.federalreserve.gov/newsevents/speech/cook20261120a.htm | "The current stance of policy does not appear to be curtailing the AI buildout." | 미국 정부 저작물 | 카드로 대체 (영상 없음 — 문서 원문 인용) |
| 산제이 메로트라 | 마이크론 IR 웹캐스트 | 회계 4분기 실적 콜 | 2026-09-30 | 주소 미확인 | "We do not have line of sight to when supply and demand will return to balance." | 회사 웹캐스트 — 20초 이내 인용 | 카드로 대체 (오늘 구간 받기 못 함 — 대기 목록에 올림) |
| 켄 그리핀 | 시타델 행사 (공식 영상 주소 미확인) | Future of Global Markets 2026 | 2026-10-20 | 주소 미확인 | "Any radical transformation of our economy is generally intertwined with a bubble." | 행사 주최 — 20초 이내 인용 | 카드로 대체 |

## 비유·과거 사례
- 품절 식당: 예약이 내년 것까지 다 찬 식당이 있다(마이크론 75%+ 약정). 그런데 그 식당 지분값은 한 달에 3분의 1이 빠졌다 — 손님이 끊겨서가 아니라, 근처에 식당이 더 생기면 지금 받는 비싼 값이 계속될지 의심하기 때문(그리핀의 '남으면 무너진다')
- 같은 손님, 고르는 주문: 전기(테이블)가 모자란 손님(구글)이 비싼 코스(8i 맥스) 대신 다른 주방(미디어텍) 메뉴를 고른다 — 손님이 줄어든 게 아니라 고르기 시작한 것
- 과거 사례 💭: 2000년 무렵 광케이블 과잉 투자 뒤 값 하락 — 그리핀이 직접 든 비교 (디크립트). 숫자는 쓰지 않음(출처에 숫자 없음)
- 과거 사례 ⚠️: 2025년 1월 27일 딥시크 충격 — 엔비디아 하루 -17% (24/7 월스트리트, 브리핑 팩트시트 N5). 그때 질문은 '칩이 덜 필요한가(수요)', 이번 질문은 '누가 얼마에 파나(몫·값)'

## 쓰지 않는 것
- 빅테크 4곳 2026년 설비투자 합계 — 매체마다 다름(5,900억·7,250억·8,000억대), 회사 발표문 원문을 오늘 다 확인하지 못함
- 엔비디아 데이터센터 매출의 하이퍼스케일러·기타 나눔(601억·475억) — 실적 발표문 본문에서 확인 못 함(보도뿐)
- 버리의 X 게시물 문장 — 원문 주소 미확인 (지지했다는 보도만)
- 'GPU 임대 값은 아직 과잉을 보이지 않는다' 반론 — 출처 문장 미확인
- 딜런 파텔(세미애널리시스) '칩이 아니라 인허가' — 11월 발언 원문 못 찾음 (10월 보고서 제목만 확인)
- 미 상원 에너지 인프라 인허가 개편안 가결(SAVE 알림) — 1차 출처 확인 못 함
- SK하이닉스 키옥시아 사채 주식 전환(SAVE 알림) — 오늘 줄기와 무관
- 드러켄밀러 13F 원문 금액의 소수점 — 보도 기준 '약'으로만
- 목표가, 사적 인물

## 주의할 점
- 궈밍치 조사는 업계 조사 — 구글·브로드컴 확인 없음, 2027년 '계획'
- 마이크론 '75%+ 약정'은 9월 30일 무렵 실적 콜 기준(그 뒤 바뀌었을 수 있음)
- 드러켄밀러 13F 는 9월 30일 기준 — 이번 폭락 전, 매수 포지션만
- 그리핀·쿡은 한 사람의 시각 — 맞을 수도 틀릴 수도
- 한국 20일 장은 미국 20일 폭락 전에 닫힘

## 틀리는 경우
1. 다음 실적에서 메모리·AI 칩 회사가 주문 취소나 가격 하락을 밝히면 → '수요는 꺾이지 않았다'는 이 편의 첫 판단이 틀린 것
2. 구글·브로드컴이 2027년 TPU 주문을 다르게 밝히면 → '몫의 이동'은 조사 하나의 과장
3. 연준이 12월에 동결하고 물가가 내려가면 → '돈의 값' 걱정은 지나친 것
4. 메모리 값이 2027년에도 오르고 장기 계약이 그대로면 → 그리핀의 '남으면 무너진다'는 적어도 메모리에선 아직 먼 이야기

## 신호
- ① 23일(월) 09:00 한국 장 — 삼성전자·SK하이닉스가 미국 금요일을 처음 받음
- ② 마이크론·브로드컴 12월 실적 발표(날짜는 회사 공지로 확인) — 약정 비율·TPU 주문 언급
- ③ 12월 10일(목) 새벽 FOMC — 쿡 이사 말대로 인상하나
- ④ 메모리 계약 가격(분기마다 업계 발표) — 오름폭이 줄어드나

## 다음 일정 (한국 시간)
| 날짜(한국 시간) | 무엇 | 종류 | 지난번·가이던스 | 볼 것 | 출처 |
|---|---|---|---|---|---|
| 23일(월) 09:00 | 한국 장 — 미국 20일 장 첫 반영 | 시장 | 삼성전자 -7.01%, SK하이닉스 -5.92% | 메모리 두 종목 | M4 |
| 12월 (회사 공지) | 마이크론 회계 1분기 실적 | 실적 | 2027년 물량 75%+ 약정 | 약정 비율·가격 | D3 |
| 12월 (회사 공지) | 브로드컴 회계 4분기 실적 | 실적 | — | 구글 TPU 언급 | S1 |
| 12월 10일(목) 새벽 | FOMC 결과 | 정책 | 3.75~4.00% 동결(10월) | 인상 여부 | F3 |

## 자료 지도 (날짜 순)
| 날짜 | 누가 | 종류 | 무엇 (원문 한 줄) | 의미 💬 | 출처 |
|---|---|---|---|---|---|
| 2026-09-30 | 마이크론 메로트라 | 발언 | "much tighter in calendar 2027 and 2028" | 공급 쪽이 '모자람'을 말함 | 컴퓨터월드 |
| 2026-09-30 (분기 말) | 드러켄밀러 | 행동 | TSMC -94%, AMD 정리, 금광주 매수 (13F) | 큰손은 이미 골랐다 | 보도 |
| 2026-10-20 | 켄 그리핀 | 발언 | "almost certainly" 거품 · GPU 남으면 값 급락 | 모자람의 끝을 경고 | 디크립트 |
| 2026-10-21 | 시장 | 행동 | 반도체 지수 11,505.56 · 마이크론 913.67 | 한 달 비교 기준 | 야후 |
| 2026-10-28 | SK하이닉스 | 보고서 | 영업이익률 80%, 장기 계약 2027·28 생산능력 50%+ | 모자람의 이익 | 회사 |
| 2026-11-17 | 엔비디아 | 보고서 | 데이터센터 1,076억(+110%), 4분기 1,300억 | 수요는 커지는 중 | 8-K |
| 2026-11-20 | 궈밍치 | 보고서 | 구글 2027년 브로드컴 TPU 약 100만 개 감축, 미디어텍 늘림 | 몫이 옮겨 감 | 인베스팅닷컴 |
| 2026-11-20 | 리사 쿡 | 발언 | "does not appear to be curtailing the AI buildout" | 돈의 값이 오를 수 있음 | 연준 |
| 2026-11-20 | 시장 | 행동 | 반도체 -10.73%, 마이크론 -13.89%, 10년물 4.91% | 동반 폭락 | 야후 |

- 말과 행동 맞대기: 메로트라·크레스·SK하이닉스는 '모자라다·야망이 크다'(말) ↔ 드러켄밀러는 9월 말에 반도체를 줄이고 금을 샀다(행동) ↔ 시장은 한 달에 반도체 지수 -26.9%(행동)

## 파급 경로
1. 회사: 엔비디아 SEC 보도·브로드컴 TPU 조사 (브리핑) → 반도체 지수 -10.73% (M1)
2. 업종: 수요가 아니라 몫·값을 의심 — 마이크론 -13.89%, 한 달 -34.9% (M2·M3)
3. 병목: 전력이 주문을 고르게 함 — 구글 TPU (S1)
4. 금리: 쿡 '지금 금리로는 AI 건설이 안 줄어든다' (F1)
5. 한국: 삼성전자·SK하이닉스 — 23일 장이 미국 금요일 반영 (K2·K3)

## 매체 프레임 (11/20~21 제목, 검색 결과·daily_brief 목록에서 확인)
| 매체 | 제목 | 강조점 | 빠진 것 | 입장 |
|---|---|---|---|---|
| CNBC (해외) | Nvidia stock plunges 14%, wraps up longest weekly losing streak since 2008 financial crisis | 7주 연속 하락 | 메모리 회사들의 공급 부족 발언 | 우려 |
| 인베스팅닷컴 (해외) | Google reportedly cuts Broadcom-designed AI chip shipments | TPU 주문 이동 | 전체 TPU 수요는 줄지 않음 | 중립 |
| 국내 특징주 기사 (국내) | [美특징주]마이크론 테크놀로지, AI 투자 우려에 7거래일 연속 하락…주가 14%↓ | AI 투자 우려 | 회사는 2027년 물량 75%+ 약정 | 우려 |
| 국내 매체 (국내) | 마이크론 CTO "메모리 반도체 공급 제약 2027년에 더 심화" | 공급 부족 | 주가와의 어긋남 | 낙관 |
| 연합뉴스 (국내) | 또 '검은 금요일'…코스피 4,800대로 후퇴, 10개월만 최저 | 한국 급락 | 메모리 이익 구조 | 우려 |

## 추가 (2026-11-22) — 이익 -2/3 는 칩 값 얼마? 과거 하강기 값 하락과 공급 과잉 폭
사용자 질문: "공급과 수요비가 어느정도여야 이정도로 낮아질건지 예측하고싶단거에요"
- ✅ SK하이닉스 3분기 매출 104.6조·영업이익 83.3조 원 → 영업이익률 약 80% (앞 항목)
- 💬 계산(가정: 파는 양·비용 그대로): 이익 -68% → 0.8×0.32=0.256, 비용 0.2 → 필요한 매출 0.456 → 값 약 -54%
- ✅ 1996: "Prices for DRAM fell by more than 75% during our fiscal 1996" — 마이크론 연차보고서, Fabricated Knowledge 인용 https://www.fabricatedknowledge.com/p/lessons-from-history-the-1990s-semiconductor (가동률 95%→86%)
- ⚠️ 2018~19: "DRAM prices fell roughly 60% over four quarters" — Chiplog(2차 자료) https://www.chiplog.io/p/dram-was-the-worst-business-in-chips · 마이크론 영업이익 2018 정점 대비 2020 -80% (Uncover Alpha) https://www.uncoveralpha.com/p/every-memory-cycle-ends-the-same
- ✅ 2021~23: DDR4 8Gb PC 계약가 2021년 7월 4.10달러(DRAMeXchange, KED Global https://www.kedglobal.com/newsView/ked202107300012) → 2023년 10월 1.50달러(TrendForce https://www.trendforce.com/news/2023/12/26/news-improvement-in-memory-inventory-leads-to-first-price-increase-in-two-and-a-half-years/) = -63%
- ⚠️ 2019 D램 공급 비트 +19.0% vs 수요 +14.6% (TrendForce 표, Evertiq 재인용 https://evertiq.com/news/52248 — 나중 발표 표라 2019년 당시 전망과 같은지 미확인)
- ✅(전망) 2023 D램 수요 비트 +8.3% vs 공급 +14.1% "severely oversupplied" — TrendForce 2022.8 https://www.trendforce.com/presscenter/news/20220803-11328.html (낸드: 수요 +28.9% vs 공급 +32.1%)
- 💬 해석: 공급이 수요보다 한 해 4~6%p 더 늘면 D램 값은 절반 넘게 빠졌다 (사례 셋, 법칙 아님). 메모리 수요는 값이 내려도 크게 늘지 않고 공장은 쉽게 멈추지 못해서.
- 💭 반대 시각: 'HBM 이 2027년 웨이퍼 30%를 쓰고 미세화로 늘어나는 비트가 절반이라 2019년식 과잉은 와도 2029년' — Korea Invest Insights(서브스택) https://koreainvestinsights.substack.com/p/if-a-2019-style-dram-glut-returns (영상 미사용, 확인 필요)

## 추가 (2026-11-22) — 메모리 P/E 와 그 뒤 1년 주가 (직접 계산)
방법: 마이크론 분기 희석 EPS(SEC XBRL companyconcept EarningsPerShareDiluted, 4분기는 연간−3개 분기) 4분기 합 = 지난 1년 EPS. 분기 끝 30일 뒤(실적 발표 뒤) 야후 종가 ÷ EPS = P/E, 그 날부터 365일 뒤 종가로 1년 수익률. 2010.10~2025.9, 61번. 원자료: E:/ytflow-local/tmp/cmp/mu_pe.json (재현 스크립트는 세션 기록)
- 💬 적자일 때 14번: 1년 뒤 중간값 +100%, 오른 비율 79%
- 💬 P/E 20배+ 15번: 중간값 +75%, 87%
- 💬 10~20배 11번: -16%, 45% · 7~10배 9번: +13%, 67%
- 💬 7배 미만 12번: -10.5%, 42%(12번 중 5번)
- 💬 사례: 2010.10 3.8배 → -38% · 2015.7 6.1배 → -35% · 2018.7 5.5배 → -26% · 예외 2018.12 2.6배 → +68% (주가 5월 정점 대비 약 절반)
- ⚠️ 한계: 한 회사, 61번, 2025년 급등기 포함(20배+ 구간을 끌어올림 — 2024.9 전까지만 보면 20배+ 중간값 +58%, 82%). 투자 판단 근거 아님.
- 참고(2차): Theta Research 2018.5 정점 trailing 7.3x·forward 5.6x → 7개월 -56% https://www.theta.md/research/mu-cycle-peak-anatomy · StockResearch 2018.8 trailing 5.2 → 10개월 -34% https://www.stockresearch.app/blog/memory-stocks-low-pe-cycle-peak

## 추가 (2026-11-22) — 쿡 이사 연설 원문
https://www.federalreserve.gov/newsevents/speech/cook20261120a.htm "The U.S. Economy in Global Context" (칠레 중앙은행 제29회 연례 회의)
- ✅ "there is evidence of spillovers ... in the price of chips and high-tech equipment, construction wages, and electricity costs"
- ✅ "The current stance of policy does not appear to be curtailing the AI buildout, and equity prices continue to support consumer spending"
- ✅ 3분기 성장 연율 3.4%, AI 건설이 "a significant contributor to this acceleration" · PCE 3.8%, 근원 3.2%, 67개월 · 9월 인상 3.75~4%, 10월 동결 반대(0.25%p 인상)
- ✅ 생산성: 효과는 "wider adoption" 에 달림 · 금융 여건 "too accommodative" · 중립금리 언급 없음
- 💬 해석(이 채널): 투자는 지을 때 수요, 공급은 보급 뒤 → 그 사이 물가 / 금리 인상 세 경우(나머지 경제 조임·P/E 압박 / 생산성 먼저 1996~97 / 늦은 대응 1999.6 4.75%→2000.5 6.5%)
