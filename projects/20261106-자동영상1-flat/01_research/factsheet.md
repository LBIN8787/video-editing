# 팩트시트: 국가 슈퍼컴퓨터 6호기 '한강', GPU 8,496장으로 본 한국 AI 컴퓨팅 위치
(기준일 2026-11-06)

## 핵심 주장 (한 문장)
한강은 계약액 3,825억 원, GPU 8,496장(GH200 등)으로 국내 공공 슈퍼컴 중 가장 크지만, 같은 시점 xAI 한 곳의 약 1/90 규모입니다. 6월 TOP500 명단에는 아직 없고, 11월 SC26 발표에서 처음 순위가 매겨집니다.

> ⚠️ **대본 수정이 꼭 필요한 부분**
> 1. 일부 해외 기사(Interesting Engineering)는 "한강이 6월 TOP500에서 12위, 실측 342.6PF"라고 썼습니다. 그런데 TOP500 공식 6월 명단에는 한강이 없고 12위는 Leonardo입니다(F14·F15). 이 주장은 쓰면 안 됩니다.
> 2. "10위권"은 과기정통부의 **전망**이지 확정된 순위가 아닙니다.
> 3. 국내 뉴스의 "24배"는 실측이 아니라 **이론 성능(Rpeak)** 기준입니다.

---

## 팩트 목록

**사업·조달**
- [F1] 2026-11-02 대전 KISTI 본원에서 가동식을 열었습니다. 9월부터 연구자를 모집해 시범 서비스를 운영해 왔습니다. — 출처: [정책브리핑(과기정통부)](https://www.korea.kr/news/policyNewsView.do?newsId=148974819) (2026-11-02), [경향신문](https://www.khan.co.kr/article/202611021000001) (2026-11-02) — 확인됨
- [F2] 공식 서비스 개시일은 과기정통부·정책브리핑과 코리아중앙데일리가 **12월 14일**, 서울경제가 **12월 16일**로 적었습니다. 정부 발표 기준인 12/14를 우선합니다. — 출처: [정책브리핑](https://www.korea.kr/news/policyNewsView.do?newsId=148974819), [Korea JoongAng Daily](https://www.koreajoongangdaily.com/business/koreas-sixth-national-supercomputer-hangang-begins-running/12950419), [서울경제](https://www.sedaily.com/article/20109087) (모두 2026-11-02) — 날짜만 재확인 필요
- [F3] 납품사는 HPE(한국휴렛팩커드)입니다. 계약은 2025-05-12 체결, 금액은 **3,825억 원**이며 5년 유지보수비 780억 원이 포함돼 있습니다. 입찰에는 2개 사가 참여했습니다. — 출처: [바이라인네트워크](https://byline.network/2025/05/14-469/) (2025-05-14), [머니투데이](https://www.mt.co.kr/tech/2025/05/14/2025051315215140024) (2025-05-14), [HPE 보도자료](https://www.hpe.com/us/en/newsroom/press-release/2025/05/korea-institute-of-science-and-technology-information-selects-hewlett-packard-enterprise-to-build-south-koreas-largest-supercomputer.html) (2025-05) — 확인됨. 다른 입찰사 이름은 확인하지 못했습니다.
- [F4] 총사업비는 2,929억 원에서 4,483억 원으로 1,553억 원(53%) 늘었습니다. 2024-11-04 국가초고성능컴퓨팅위원회에서 결정됐습니다. 서울경제는 4,482억 원으로 적어 1억 원 차이가 납니다(반올림 차이로 추정). — 출처: [머니투데이](https://www.mt.co.kr/tech/2024/11/05/2024110509300092225) (2024-11-05), [서울경제](https://www.sedaily.com/article/20109087) (2026-11-02) — 확인됨
- [F5] GPU 가격이 급등해 입찰이 **4차례 유찰**됐습니다. 당초 서비스 목표는 2025년이었습니다. — 출처: [머니투데이](https://www.mt.co.kr/tech/2024/11/05/2024110509300092225) (2024-11-05), [바이라인네트워크](https://byline.network/2025/05/14-469/)("수차례") — 확인됨
- [F6] 예비타당성조사 통과 시점은 출처마다 다릅니다. 테크수다·서울경제는 2022년(8월), 머니투데이(2024)는 2023년 8월로 적었습니다. — 재확인 필요 (기재부·KISTI 원문 확인 권장)

**사양**
- [F7] GPU 8,496개(엔비디아 GH200 등), CPU 9,936개, 이론 성능 614PF, 저장공간 205PB, 네트워크 400Gbps 이상입니다. 누리온 대비 이론 성능 24배, 저장공간 10배, 네트워크 4배입니다. — 출처: [정책브리핑](https://www.korea.kr/news/policyNewsView.do?newsId=148974819), [Korea JoongAng Daily](https://www.koreajoongangdaily.com/business/koreas-sixth-national-supercomputer-hangang-begins-running/12950419) (2026-11-02) — 확인됨
- [F8] GPU 수 표기는 매체마다 다릅니다. 머니투데이(2025-05) 부제는 "GH200 8,694장", 경향 제목은 "8,400장"(반올림)입니다. 일부 자료는 "GPU 파티션 GH200 8,336개 + CPU 파티션 AMD EPYC 1,608개(또는 804개)"로 적었습니다. 영상에서는 정부 공식 수치인 8,496을 씁니다. 다만 "8,496장이 전부 GH200"이라는 표현은 피하세요. 정부도 "GH200 **등**"이라고 썼습니다. — 출처: [머니투데이](https://www.mt.co.kr/tech/2025/05/14/2025051315215140024), [경향신문](https://www.khan.co.kr/article/202611021000001) — GH200 수량 재확인 필요
- [F9] 구조는 HPE Cray EX4000 위의 두 파티션입니다. 하나는 GH200, 다른 하나는 5세대 AMD EPYC이고, Slingshot 400 인터커넥트와 100% 팬리스 직접 수냉을 씁니다. — 출처: [HPE 보도자료](https://www.hpe.com/us/en/newsroom/press-release/2025/05/korea-institute-of-science-and-technology-information-selects-hewlett-packard-enterprise-to-build-south-koreas-largest-supercomputer.html), [insideHPC](https://insidehpc.com/2025/05/koreas-kisti-selects-hpe-for-600pflops-supercomputer/) (2025-05) — 확인됨
- [F10] PUE(전력효율 지표)는 5호기 1.35에서 1.15로 좋아졌습니다. — 출처: [서울경제](https://www.sedaily.com/article/20109087) (2026-11-02) — 단일 출처, 재확인 필요
- [F11] 자원 배분은 R&D 혁신 55%, 국가전략 30%, 산업혁신(중소·중견) 15%입니다. — 출처: [서울경제](https://www.sedaily.com/article/20109087), [Interesting Engineering](https://interestingengineering.com/innovation/614-petaflops-supercomputer-hangang) (2026-11-02) — 확인됨
- [F12] 양자컴퓨터와 연동하는 하이브리드 구성을 2027년 상반기에 계획하고 있습니다. — 출처: [서울경제](https://www.sedaily.com/article/20109087), [Interesting Engineering](https://interestingengineering.com/innovation/614-petaflops-supercomputer-hangang) — 확인됨(계획)

**순위**
- [F13] 과기정통부는 SC26(시카고, 11/15~20) TOP500에서 "10위권 등재"를 전망했습니다. — 출처: [정책브리핑](https://www.korea.kr/news/policyNewsView.do?newsId=148974819), [Korea JoongAng Daily](https://www.koreajoongangdaily.com/business/koreas-sixth-national-supercomputer-hangang-begins-running/12950419) — 전망으로서 확인됨
- [F14] TOP500 2026년 6월 명단의 1~20위에 한강(KISTI-6)은 없습니다. 한국 최고 순위는 NHN클라우드 NIPA-CL-1로 **20위**(Rmax 137.4PF)입니다. — 출처: [TOP500 June 2026](https://top500.org/lists/top500/list/2026/06/), [디일렉](https://www.thelec.net/news/articleView.html?idxno=11706) — 확인됨
- [F15] "6월 12위, 342.6PF"라는 주장(Interesting Engineering)은 TOP500 공식 명단과 맞지 않습니다. 공식 명단의 12위는 Leonardo(241.2PF)입니다. — 출처: [Interesting Engineering](https://interestingengineering.com/innovation/614-petaflops-supercomputer-hangang) vs [TOP500](https://top500.org/lists/top500/list/2026/06/) — **사용 금지 / 재확인 필요**
- [F16] 5호기 누리온의 TOP500 순위 변화: 2018-06 11위 → 2018-11 13위 → 2020-11 21위 → 2026-06 **144위**(Rmax 13.93PF). — 출처: [TOP500 KISTI 사이트 페이지](https://www.top500.org/site/50770/) — 확인됨

**국가 GPU 정책 맥락**
- [F17] 1차 추경 1조 4,600억 원으로 GPU를 확보하는 사업자로 네이버클라우드(H200 3,056장), NHN클라우드(B200 7,656장), 카카오(B200 2,424장)가 선정됐습니다. 합계 약 1.3만 장입니다. — 출처: [머니투데이](https://www.mt.co.kr/tech/2025/07/28/2025072818560947822) (2025-07-28), [DCD](https://www.datacenterdynamics.com/en/news/nhn-launches-7656-gpu-cluster-in-seoul-south-korea/) — 확인됨
- [F18] 엔비디아는 2025-10-31 APEC에서 한국에 GPU 26만 장 공급을 발표했습니다. 배분은 정부 5만, 삼성·SK·현대차 각 5만, 네이버 약 6만입니다. 공급 시기는 "향후 수년에 걸쳐"로, 일정이 확정된 것은 아닙니다. — 출처: [머니투데이](https://www.mt.co.kr/tech/2025/10/31/2025103112075597559), [헤럴드경제](https://www.heraldk.com/article/2025103022433635047) (2025-10-31) — 확인됨

**엔비디아 '소버린 AI'**
- [F19] FY2026(2026년 1월 끝난 회계연도) 소버린 AI 매출은 **300억 달러 이상**으로 전년의 3배 넘게 늘었습니다. 주요 고객국으로 캐나다·프랑스·네덜란드·싱가포르·영국이 언급됐고, 한국은 이 목록에 없습니다. 같은 해 총매출은 2,159억 달러, 데이터센터 매출은 1,937억 달러입니다. — 출처: [NVIDIA 8-K (SEC)](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000019/q4fy26pr.htm) (2026-02-25), [Q4 FY26 콜 녹취 (Motley Fool)](https://www.fool.com/earnings/call-transcripts/2026/02/25/nvidia-nvda-q4-2026-earnings-call-transcript/) — 확인됨
- [F20] FY27 2분기부터 엔비디아는 소버린 매출을 따로 공개하지 않습니다. 소버린·지역 네오클라우드·엔터프라이즈를 묶은 **ACIE** 항목으로 보고하며, ACIE는 400억 달러(전 분기 대비 +25%, 전년 대비 +138%)입니다. 2분기 총매출은 962억 달러, 데이터센터 매출은 890억 달러입니다. — 출처: [NVIDIA 8-K Q2 FY27 (SEC)](https://www.sec.gov/Archives/edgar/data/0001045810/000104581026000073/q2fy27pr.htm), [Investing.com 녹취](https://www.investing.com/news/transcripts/earnings-call-transcript-nvidia-beats-q2-2026-estimates-as-ai-demand-stays-hot-93ch-4878028) (2026-08-26) — 확인됨
- [F21] 한강 GPU 매출이 엔비디아 장부에서 '소버린'으로 잡히는지는 공개 자료로 확인되지 않습니다. 한강은 HPE를 거친 OEM 납품이고, 엔비디아는 국가별·고객별 소버린 내역을 공개하지 않습니다. — 재확인 필요 (대본에서는 "확인 불가"로 표기하세요)

**빅테크 클러스터**
- [F22] xAI: 2026-09-25 머스크의 X 게시물 기준 Colossus 2는 GB200 11만 + GB300 44만 = 약 55만 장입니다. Colossus 1은 약 23만 장(H100 15만, H200 5만, GB200 3만)입니다. 연말까지 GB300 22만 장씩 3차례 추가하는 계획을 합치면 총 약 144만 장입니다. — 출처: [Invezz](https://invezz.com/news/2026/09/25/elon-musk-says-xais-colossus-2-could-more-than-double-nvidia-chip-count-by-year-end/), [CoinCentral](https://coincentral.com/musk-says-colossus-2-data-center-could-double-nvidia-chip-count-by-year-end) (2026-09-25) — 확인됨(머스크 본인 발언을 2차 보도로 확인. 로이터 등 주요 통신사 보도는 찾지 못함)
- [F23] Meta Prometheus(오하이오)는 "수십만 개 GPU"를 운영 중이고 목표는 약 100만 개, 1GW입니다. 확정된 현재 수량은 없습니다. — 출처: [The Register](https://www.theregister.com/systems/2026/10/20/tens-of-thousands-of-nvidia-gpus-sit-in-metas-prometheus-supercluster-waiting-for-a-failure/5304269) (2026-10-20) — 확인됨(현재 수량은 미공개)
- [F24] MS Fairwater(위스콘신)는 "수십만 개 GB200"이라고만 밝혔고 공식 수량은 없습니다. Epoch AI는 위스콘신 약 17.6만, 애틀랜타 약 30.4만으로 추정합니다. — 출처: [Tom's Hardware](https://www.tomshardware.com/tech-industry/artificial-intelligence/microsoft-announces-worlds-most-powerful-ai-data-center-315-acre-site-to-house-hundreds-of-thousands-of-nvidia-gpus-and-enough-fiber-to-circle-the-earth-4-5-times), [ComputeAtlas](https://computeatlas.net/blog/deep-dive-microsoft-fairwater) — 공식 수치 아님(추정)

---

## 숫자·데이터 (카드·차트용)

**카드 1. 돈 (단순 나눗셈은 출처 숫자로 직접 계산)**
| 항목 | 값 |
|---|---|
| 총사업비(변경 후) | 4,483억 원 (당초 2,929억, +53%) |
| HPE 계약액 | 3,825억 원 (유지보수 780억 포함) |
| 계약액 ÷ GPU 8,496 | 약 4,500만 원 |
| (계약액 − 유지보수) ÷ 8,496 | 약 3,580만 원 |
⚠️ 이 값은 **GPU 단가가 아닙니다.** CPU 파티션, 205PB 스토리지, 네트워크, 수냉 설비가 모두 들어간 금액입니다. 화면에 "GPU 1장당 시스템 비용(단순 계산)"이라고 표기하세요. 실제 GH200 단가는 공개되지 않았습니다.

**카드 2. 몇 분의 1인가 (GPU 개수만 비교)**
| 클러스터 | GPU 수 | 한강 대비 |
|---|---|---|
| 한강 | 8,496 | 1 |
| 정부 추경 GPU (3사 합계) | 약 13,136 | 약 1.5배 |
| xAI Colossus 2 (2026-09) | 약 55만 | 약 65배 |
| xAI Colossus 1+2 (2026-09) | 약 78만 | 약 92배 |
| xAI 연말 계획 | 약 144만 | 약 170배 |
| Meta Prometheus 목표 | 약 100만 | 약 118배 |
⚠️ GB200·GB300은 GH200보다 세대가 뒤의 칩이라 장당 AI 성능 격차가 더 큽니다. 빅테크 수치는 회사 발표나 추정치입니다.

**카드 3. TOP500 위치 (2026년 6월, Rmax 실측 기준)**
- 1위 LineShine(중국) 2,198PF / 10위 Alps 434.9PF / 한국 1위 NHN NIPA-CL-1 20위 137.4PF
- 한강의 이론 성능 614PF는 Rpeak입니다. 순위는 실측(Rmax)으로 매겨집니다. 6월 명단에서 10위 안에 들려면 Rmax 434.9PF 이상이 필요했습니다.
- 6월 명단의 한국 시스템: 20위 NHN, 25위 삼성 SSC-24, 39위 카카오(NIPA), 40위 NHN CL-2, 72위 네이버 세종, 144위 누리온 등 — [TOP500 sublist](https://top500.org/statistics/sublist/)
- 누리온 순위 그래프: 11위(2018) → 144위(2026)

**카드 4. 엔비디아 소버린 AI**
- FY26: 300억 달러 이상(3배 넘게 성장), 총매출 2,159억 달러의 약 14%(계산값)
- FY27 2분기: ACIE 400억 달러, 데이터센터 매출 890억 달러의 약 45%(계산값)

**카드 5. 지연 타임라인**
예타(2022 또는 2023, F6) → 4차례 유찰 → 2024-11 사업비 53% 증액 → 2025-05 HPE 계약 → 2026-09 시범 서비스 → 2026-11-02 가동식 → 2026-12-14 공식 서비스

---

## 인물 발언 (확인된 것만)
- **김성수 과기정통부 연구개발정책실장**, 2026-11-02 가동식: "국가슈퍼컴 6호기 '한강'은 AI와 과학기술의 융합을 지원해 새로운 과학적 발견을 이끌어 갈 핵심 기반" — [정책브리핑](https://www.korea.kr/news/policyNewsView.do?newsId=148974819)
- **이식 KISTI 원장**, 2026-11-02 가동식: "한강이 국내 연구자들의 도전적인 연구를 뒷받침하는 기반이 될 수 있도록 할 것", "그동안 쌓은 슈퍼컴퓨터 운영 경험을 토대로 이용자 지원에 최선을 다하겠다" — [경향신문](https://www.khan.co.kr/article/202611021000001)
- **이식 KISTI 원장**, 2026-11-02(서울경제 취재): "두 컴퓨터를 연결하면 서로의 약점은 보완하고 장점은 살리는 하이브리드 컴퓨터가 될 수 있다" — [서울경제](https://www.sedaily.com/article/20109087)
- **하정우 국가AI전략위원회 부위원장**은 한강이 "K-문샷 프로젝트의 기반"이 될 것이라고 말했습니다. 기사에서는 요약 인용이라 원문 그대로인지 재확인이 필요합니다. — [서울경제](https://www.sedaily.com/article/20109087)
- **콜렛 크레스 엔비디아 CFO**, 2026-02-25 FY26 4분기 실적 콜: "In fiscal year 2026, our Sovereign AI business more than tripled year over year to over $30,000,000,000" — [Motley Fool 녹취](https://www.fool.com/earnings/call-transcripts/2026/02/25/nvidia-nvda-q4-2026-earnings-call-transcript/)
- **콜렛 크레스**, 2026-08-26 FY27 2분기 실적 콜: "ACIE revenue of $40 billion increased 25% sequentially and 138% year-over-year." — [Investing.com](https://www.investing.com/news/transcripts/earnings-call-transcript-nvidia-beats-q2-2026-estimates-as-ai-demand-stays-hot-93ch-4878028)

## 반론·한계
- **비교 기준이 다릅니다.** TOP500은 FP64 과학계산(HPL) 순위입니다. 빅테크 AI 클러스터는 대부분 TOP500에 제출하지 않습니다(MS Eagle만 7위). 그래서 "한강이 세계 10위권"이라는 말이 "AI 컴퓨팅 세계 10위권"을 뜻하지는 않습니다.
- **세대 차이가 있습니다.** GH200은 호퍼 세대로, 2022년 기획한 사양이 유찰 끝에 2026년에 가동된 셈입니다. 같은 해 xAI·Meta는 블랙웰(GB200·GB300)을 대량 배치했습니다.
- **목적이 다릅니다.** 한강은 공공 연구용입니다. 자원의 55%가 R&D이고 CPU 파티션도 포함돼 있어, 대형 AI 모델 학습만 하는 클러스터와 1:1로 비교하기 어렵습니다.
- **국가 AI 자원은 한강만이 아닙니다.** 추경 GPU 1.3만 장(F17)과 26만 장 계획(F18)이 따로 있습니다. "한국 AI 컴퓨팅 = 한강"으로 표현하면 오해를 부릅니다.
- **확인되지 않은 것:** GPU 실제 단가, 다른 입찰사, GH200 정확한 수량, 엔비디아 매출에서의 분류는 모두 미확인입니다.

## 다음에 볼 것
- **SC26 TOP500 발표**(시카고, 11/15~20): 한강의 실측 Rmax와 순위, "10위권" 전망이 맞는지 확인. 후속편 소재입니다. — [TOP500](https://top500.org/)
- **엔비디아 FY27 3분기 실적**(2026-11-17, 오후 2시 PT): ACIE·소버린 언급, 한국 관련 발언. 매출 가이던스는 1,080억 달러 ±2%입니다. — [NVIDIA IR](https://nvidianews.nvidia.com/news/nvidia-sets-conference-call-for-third-quarter-financial-results-6928873)
- **한강 공식 서비스 개시**(12/14, 서울경제는 12/16)
- **xAI Colossus 2 GB300 추가 물량**(11월·12월분)이 실제로 들어오는지
- **정부 5만 장·국가 AI컴퓨팅센터** 진행 상황, **양자컴 연동**(2027년 상반기)

---

## Sources
- [정책브리핑](https://www.korea.kr/news/policyNewsView.do?newsId=148974819) · [경향신문](https://www.khan.co.kr/article/202611021000001) · [서울경제](https://www.sedaily.com/article/20109087) · [Korea JoongAng Daily](https://www.koreajoongangdaily.com/business/koreas-sixth-national-supercomputer-hangang-begins-running/12950419) · [테크수다](https://www.techsuda.com/msit-hangang-supercomputer-6-launch/) · [Interesting Engineering](https://interestingengineering.com/innovation/614-petaflops-supercomputer-hangang)
- [바이라인네트워크](https://byline.network/2025/05/14-469/) · [머니투데이 2025-05](https://www.mt.co.kr/tech/2025/05/14/2025051315215140024) · [머니투데이 2024-11](https://www.mt.co.kr/tech/2024/11/05/2024110509300092225) · [HPE 보도자료](https://www.hpe.com/us/en/newsroom/press-release/2025/05/korea-institute-of-science-and-technology-information-selects-hewlett-packard-enterprise-to-build-south-koreas-largest-supercomputer.html) · [insideHPC](https://insidehpc.com/2025/05/koreas-kisti-selects-hpe-for-600pflops-supercomputer/)
- [TOP500 June 2026](https://top500.org/lists/top500/list/2026/06/) · [TOP500 KISTI](https://www.top500.org/site/50770/) · [TOP500 sublist](https://top500.org/statistics/sublist/) · [디일렉](https://www.thelec.net/news/articleView.html?idxno=11706)
- [머니투데이 GPU 1.3만장](https://www.mt.co.kr/tech/2025/07/28/2025072818560947822) · [DCD](https://www.datacenterdynamics.com/en/news/nhn-launches-7656-gpu-cluster-in-seoul-south-korea/) · [머니투데이 26만장](https://www.mt.co.kr/tech/2025/10/31/2025103112075597559) · [헤럴드경제](https://www.heraldk.com/article/2025103022433635047)
- [NVIDIA 8-K FY26 Q4](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000019/q4fy26pr.htm) · [NVIDIA 8-K FY27 Q2](https://www.sec.gov/Archives/edgar/data/0001045810/000104581026000073/q2fy27pr.htm) · [Motley Fool 녹취](https://www.fool.com/earnings/call-transcripts/2026/02/25/nvidia-nvda-q4-2026-earnings-call-transcript/) · [Investing.com 녹취](https://www.investing.com/news/transcripts/earnings-call-transcript-nvidia-beats-q2-2026-estimates-as-ai-demand-stays-hot-93ch-4878028) · [NVIDIA 실적 일정](https://nvidianews.nvidia.com/news/nvidia-sets-conference-call-for-third-quarter-financial-results-6928873)
- [Invezz](https://invezz.com/news/2026/09/25/elon-musk-says-xais-colossus-2-could-more-than-double-nvidia-chip-count-by-year-end/) · [CoinCentral](https://coincentral.com/musk-says-colossus-2-data-center-could-double-nvidia-chip-count-by-year-end) · [The Register](https://www.theregister.com/systems/2026/10/20/tens-of-thousands-of-nvidia-gpus-sit-in-metas-prometheus-supercluster-waiting-for-a-failure/5304269) · [Tom's Hardware](https://www.tomshardware.com/tech-industry/artificial-intelligence/microsoft-announces-worlds-most-powerful-ai-data-center-315-acre-site-to-house-hundreds-of-thousands-of-nvidia-gpus-and-enough-fiber-to-circle-the-earth-4-5-times) · [ComputeAtlas](https://computeatlas.net/blog/deep-dive-microsoft-fairwater)

*이 자료는 정보 제공용이며 투자 권유가 아닙니다.*