# 68. 설명 다큐 레퍼런스 — 문장마다 무엇을 보여 주나 (2026-11-25)

> 사용자: "설명이나 학습다큐 즉 시청자에게 설명하고 서술하는 다큐들의 레퍼런스를 수집하고 이 편집방식을 벤치마킹하여 참조하세요"
> 배경: 직전 시험 005(고정 틀)·019(하나 → 여럿)는 기각, 008(관계도)은 호평 ([67 §9](67-docu-reference-analysis.md)). 기각 이유는 "무엇을 나타내려는지 모름", "칩 그림이 왜 필요한가", "정지 화면이 길다", "왼쪽보다 이해가 쉽지 않다".

이 문서는 **설명하는 다큐가 한 문장마다 화면에 무엇을 놓는지**를 실제 영상에서 문장과 화면을 맞대어 본 기록입니다. 이미 본 것([65](65-attention-explainer-benchmark.md) EBS AI 사피엔스, [67](67-docu-reference-analysis.md) EBS 〈자본주의〉·달리오·블룸버그)은 같은 잣대로 다시 재기만 했습니다. 인물·인터뷰 장면은 분석에서 뺐습니다.

## 0. 어떻게 봤나 (정직하게)

- 사용자 PC 의 앱 안 브라우저에서 YouTube 를 **소리 끄고 2배속으로 재생**하며 0.25초(영상 시간)마다 화면을 읽었습니다. 내려받지 않았고, 광고는 '건너뛰기'를 눌러 넘겼습니다.
- **정지** = 64×36 흑백으로 줄인 화면의 평균 밝기 차이가 0.6(0~255) 미만인 상태가 1.5초 이상 이어진 구간. 같은 계산을 내 영상에 쓰려고 [`scripts/hold_measure.py`](../scripts/hold_measure.py) 를 만들었습니다(ffmpeg 로 같은 크기·간격).
- 문장은 플레이어가 받아 오는 자막(제작자 자막 또는 자동 자막)으로 맞췄습니다. 1초마다 저장한 작은 화면을 자막 시작 시각에 놓고 "이 문장 → 이 화면"을 봤습니다.
- 한계: 작은 요소만 바뀌는 어두운 화면은 차이 값이 작게 나와 정지로 잡히기 쉽습니다(우리 영상에 불리). FT 는 실사 카메라가 계속 움직여 정지가 0 으로 나옵니다. 그래서 수치는 **'화면 전체가 살아 있나'**를 보여 줄 뿐, '설명이 좋은가'는 §2 의 문장 대응으로 판단합니다. 영상마다 앞부분 몇 분만 봤습니다.

## 1. 레퍼런스와 측정값

| 레퍼런스 | 본 구간 | 성격 | 정지 비율 | 가장 긴 정지 |
|---|---|---|---|---|
| TED-Ed 〈How does the stock market work?〉 [p7HKvqRI_Bo](https://youtu.be/p7HKvqRI_Bo) | 전체 4:30 | 평면 일러스트 애니메이션, 주식시장 | 19% | 4.3초 |
| WSJ 〈Why Bond Yields Are a Key Economic Barometer〉 [7x8vIvwYzFg](https://youtu.be/7x8vIvwYzFg) | 전체 5:17 (인터뷰 포함) | 청사진 격자 + 실물 증서 그래픽, 채권 | 28% | 6.8초 |
| Kurzgesagt 〈Universal Basic Income Explained〉 [kl39KHS07Xc](https://youtu.be/kl39KHS07Xc) | 0:00–3:20 | 캐릭터 애니메이션, 정책·경제 | 4% | 2.5초 |
| PolyMatter 〈China's Fundamental Economic Problem〉 [d7SVsqg4Jzk](https://youtu.be/d7SVsqg4Jzk) | 0:00–3:00 | 차트 틀 + 자료 영상, 거시경제 | 5% | 3.8초 |
| 달리오 〈How The Economic Machine Works〉 [PHe0bXAIuk0](https://youtu.be/PHe0bXAIuk0) | 1:00–4:00 | 흰 바탕 선 그림(우리처럼 성긴 화면) | 26% | 5.0초 |
| EBS 지식채널e 〈호르무즈 해협〉 [6EONSMddyyU](https://youtu.be/6EONSMddyyU) | 전체 5:01 | 내레이션 없음, 자막·지도·실사 | 22% | 6.1초 |
| EBS 다큐프라임 〈자본주의〉 1부 조각 #501 [JCSo1K4rm0I](https://youtu.be/JCSo1K4rm0I) | 전체 8:54 | 애니메이션 + 실사 | 4% | 5.2초 |
| FT Film 〈Why governments are 'addicted' to debt〉 [n1jhoU9Mp_U](https://youtu.be/n1jhoU9Mp_U) | 0:40–3:20 (+전체 15초 간격 훑기) | 인터뷰 + 지폐 테두리 그래픽 | 0% (카메라가 늘 움직임) | — |
| KBS 다큐 인사이트 〈반도체 머니, 돈의 궤적〉 [7Ykq8ZifZ2w](https://youtu.be/7Ykq8ZifZ2w) | 전체 24초 간격 훑기 | 사람·관찰 촬영 중심 | — | — |

KBS 편은 훑어본 120장 중 그래픽이 5장 안팎이었습니다. **방송사의 시장 다큐는 사람과 현장으로 설명하는 경우가 많아, 얼굴 없이 그래픽으로 설명하는 우리에게는 설명 그래픽 전문 제작물(WSJ·FT·PolyMatter·TED-Ed·Kurzgesagt·EBS 애니메이션 부분)이 맞는 레퍼런스**입니다.

**같은 잣대로 잰 우리 영상**

| 영상 | 정지 비율 | 가장 긴 정지 |
|---|---|---|
| 11-24 아침 브리핑 final | 75% | 9.2초 |
| 11-24 엔비디아 복귀 심층 final | 71% | 10.5초 |
| 시범 005 기존 / 고정 틀 | 87% / 96% | 6.5초 / 17.8초 |
| 시범 008 기존 / 관계도 | 73% / 87% | 5.0초 / 16.8초 |
| 시범 019 기존 / 하나 → 여럿 | 89% / 92% | 6.0초 / 12.5초 |

레퍼런스는 0~28%(실사 FT 제외 4~28%), 우리는 71~96%입니다. 작은 요소가 바뀌는 어두운 화면이라 불리하게 잡히는 몫을 빼도, **화면 넓은 부분이 문장마다 바뀌거나 계속 숨 쉬는 레퍼런스와 구조가 다릅니다.** 호평받은 008 도 화면 전체로 보면 오래 멈춰 있었습니다. 008 이 좋았던 이유는 움직임의 양이 아니라 §2 의 첫 규칙(그림 = 대사의 내용)이었습니다.

## 2. 문장 → 화면 (실제로 본 것)

시각은 영상 안 시각입니다. 문장은 자막을 줄여 옮겼습니다.

### TED-Ed — 주식시장
| 시각 | 문장 | 화면 |
|---|---|---|
| 0:07 | "In the 1600s" | 배 무늬 위 '1600s' 카드 |
| 0:11 | "trade gold, porcelain, spices, and silks" | 금·도자기·향신료·비단 그릇이 말한 순서대로 놓임 |
| 0:21 | "the company turned to private citizens… who could invest" | 회사 사람 옆에 시민들이 줄지어 섬 |
| 0:36 | "increasing profits for both" | 항로 지도 위 동전 더미가 자람 |
| 1:14 | "imagine a new coffee company" | 커피잔 캐릭터 등장 — 끝까지 이 회사의 얼굴 |
| 1:18 | "advertise itself to big investors" | 커피잔이 이젤 앞에서 양복 입은 사람들에게 발표 |
| 1:26 | "initial public offering, or IPO" | 'IPO' 글자 |
| 1:40 | "partial owners in the business" | 투자자가 커피 로고의 **잘린 조각**을 들고 있음 (주식 = 회사의 한 조각) |
| 1:48 | "more buyers… start buying stocks" | 계산대 앞 줄이 길어짐 |
| 2:41 | "this see-saw of supply and demand" | 수요·공급 이름표가 붙은 실제 시소 |
| 3:10 | "day-to-day noise in the market" | 들쭉날쭉한 선 |
| 3:24 | "confidence… booms to financial crises" | 풍선이 날아감, 올라가는 화살표, 무너지는 격자 |

### WSJ — 채권 금리 (설명 부분, 0:57 부터)
| 시각 | 문장 | 화면 |
|---|---|---|
| 0:57 | "When we talk about a bond yield…" | 사전 표제어 카드, **읽는 대로 정의문에 형광 표시** |
| 1:06 | "A bond is a contract…" | 채권 증서 (실물 모양) |
| 1:10 | "maturity date… two to 30 years" | 0~30년 눈금자, 2~30 구간 표시 |
| 1:16 | "two and 10 years are also called notes" | 2~10 구간에 괄호 |
| 1:20 | "face value… guaranteed to pay on the maturity date" | 증서에 $ 와 'Face Value' 이름표 |
| 1:28 | "coupon rate… pays each year up to its maturity date" | 눈금자의 해마다 작은 쿠폰 상자 |
| 1:37 | "buys a new 10-year treasury note… $1,000… 4%" | 증서가 눈금자 위로, '$1,000' 표시 |
| 1:57 | "she can sell it to other investors" | 증서가 옆으로 옮겨 감 |
| 2:07 | "new bonds will be issued at a higher yield" | 옆에 **새 증서(5%)**가 같은 모양으로 나타남 — 옛 증서(4%)와 나란히 |
| 2:21 | "less attractive… the price has dropped" | 옛 증서에 가격표, 값이 내려감 |
| 2:23 | "When the price goes down, the yield goes up" | 가격표 숫자가 바뀜 |
| 2:37 | "yields and stocks both going up" | 실제 WSJ 기사 제목 |

### Kurzgesagt — 기본소득 (1:20–3:20)
| 시각 | 문장 | 화면 |
|---|---|---|
| 1:21 | "will people just spend it on booze" | 돈을 든 새 캐릭터들, 하나가 술병을 듦 |
| 1:27 | "A 2013 study by the World Bank" | 지구 로고 + 건물 |
| 1:41 | "the richer you are, the more drugs and alcohol" | 지폐 격자에 술병이 늘어남 |
| 1:59 | "1% of the recipients stopped working" | 집들 위 '−1%' |
| 2:03 | "reduced their working hours by less than 10%" | 책상 앞 사람 + 시계 '−10%' |
| 2:22 | "a lot of strings attached" | 캐릭터에 **진짜 꼭두각시 줄** |
| 3:01 | "a benefit of $1,000… if you earn a single dollar extra the whole thing is taken away" | 'WELFARE $1,000' 동전 더미와 'JOB $1,200' 더미를 나란히, 캐릭터가 더미를 오름 |

### PolyMatter — 중국 경제 (0:20–1:30)
| 시각 | 문장 | 화면 |
|---|---|---|
| 0:23 | "youth unemployment… doubled… government simply stopped publishing data" | 같은 틀의 선 그래프가 말하는 동안 그려지고, 끊긴 끝에 경고 표시 |
| 0:39 | "Chinese stock market… lost about 40%" | 주가 선이 그려짐 |
| 0:47 | "land sales reached their lowest level this century" | 막대 그래프, **마지막 막대만 노란색** |
| 1:11 | "Its population has begun to shrink" | 인구 곡선, 꼭짓점 표시 |
| 1:21 | "'West is declining' and 'East is rising'" | 수사(修辭)에는 자료 영상(건물·깃발) |

### FT Film — 정부 부채 (0:40–3:20)
- 장 제목 "The 'debt addiction'"을 **지폐 무늬 테두리** 안에 — 그래프·정의 카드가 모두 같은 테두리 안에 나옵니다(한 편 한 시각 언어).
- "부채 위기" 이야기에는 실제 FT 기사 제목("Foreign debt crisis looms", "Bond 'police' are back")을 종이 질감 그대로.
- 나라별 정부 부채는 가로 막대가 **하나씩** 노랗게 차오릅니다. 이어서 'Government debt' 정의 카드.

### EBS 지식채널e — 호르무즈 (내레이션 없음)
- 실제 유조선·컨테이너선 영상 위에 그 배에 붙은 숫자('1/5', '1/3', '○만 배럴').
- 위성 지도 → 단순화한 지도로 넘어간 뒤, **같은 지도에 나라 색·항로·우회 송유관을 한 겹씩** 더함(지도는 그대로, 겹만 바뀜).
- 좁은 해협을 설명할 때 **고속도로의 붉은 한 차로**를 비유 화면으로.

## 3. 공통 문법 — 레퍼런스가 지킨 것

| # | 규칙 | 근거 (§2) | 우리 시범에 대 보면 |
|---|---|---|---|
| E1 | **그림은 문장의 명사·동사 그 자체다.** 실물(채권 증서, 실제 차트, 실제 기사)이거나, 한 번 소개하고 끝까지 쓰는 구체적 대역(커피잔 = 그 회사, 새 = 사람). 내용과 무관한 장식 상징은 없다 | WSJ 증서, TED-Ed 커피잔, PolyMatter 차트 | 008 ✅ 실제 회사·약정 / 005 ❌ 칩 그림은 주가와 무관 |
| E2 | **주인공 사물 하나를 문장들 내내 들고 간다.** 새 정보는 그 사물에 붙이거나 바꾼다(이름표·가격표·새 경쟁 사물). 장면을 지우고 새로 시작하지 않는다 | WSJ 증서에 이름표 → 가격표 → 옆에 새 증서 | 008 ✅ 엔비디아 중심 그림이 자람 |
| E3 | **문장(때로 구절)마다 화면이 바뀐다.** 가장 긴 정지는 2.5~6.8초. 오래 멈추는 것은 정의문을 읽힐 때·숫자 하나를 새길 때뿐 | §1 측정 | 005 17.8초, 019 12.5초 ❌ |
| E4 | **숫자는 제 모양의 그래프로, 말하는 순간에 그린다.** 요점 하나에 표시(마지막 막대만 색, 끊긴 곳에 경고, 꼭짓점 이름표) | PolyMatter, FT 막대 | 005 는 주가인데 선 그래프가 아니었음 ❌ |
| E5 | **비교는 같은 종류의 사물을 나란히.** 같은 모양·같은 축척 | WSJ 4% vs 5% 증서, Kurzgesagt 복지 vs 일 동전 더미 | — |
| E6 | **관용구·추상은 몸으로 하는 동작으로 바꾼다** — 숫자가 아니라 개념에만 | '조건이 붙은' → 꼭두각시 줄, 수요·공급 → 시소, 신뢰 → 풍선 | 019 '다들 기다린다'는 아무도 움직이지 않아 동작이 없었음 ❌ |
| E7 | **증거는 실물, 수사는 자료 영상, 설명은 그림.** | WSJ·FT 기사 제목, PolyMatter 깃발 영상 | — |
| E8 | **한 편 한 시각 언어.** 틀·색·질감이 처음부터 끝까지 같다 | FT 지폐 테두리, PolyMatter 붉은 차트 틀, WSJ 청사진 격자 | 우리 '어두운 판'은 이미 해당 |

**008 이 통한 이유**는 E1·E2 를 지켰기 때문입니다. **005·019 가 실패한 이유**는 E1(무관한 상징)·E3(긴 정지)·E4(숫자인데 그래프 아님)·E6(동작 없음)을 어겼기 때문입니다.

## 4. 레퍼런스라면 그 두 장면을 어떻게 했을까 (가설 — 아직 만들지 않음)

- **005 엔비디아 주가 (10/6 239.24 → 11/11 173.73 → 11/20 125.53 → 11/23 165.05):** PolyMatter·WSJ 식이면 **실제 주가 선**을 날짜 축 위에 말하는 순서대로 그립니다(E4). '사임' 날짜에 표지, 금요일 → 월요일 오른 폭에 괄호 '+31%', 10월 고점까지 남은 폭에 괄호 '아직 −31%'. 칩 그림은 쓰지 않습니다(E1).
- **019 치킨 게임:** Kurzgesagt·TED-Ed 식이면 '다들 기다린다'를 **동작**으로 만듭니다(E6). 예: 회사 셋이 각자 '감산' 손잡이에 손을 올린 채 서로 눈치만 보고(아무도 당기지 않음), 그 사이 창고 재고 더미가 자라며 값 표지가 내려갑니다. '치킨 게임'에서는 마주 달리는 두 차로 바꿀 수 있습니다. '약속하면'에는 손잡이를 같이 당기는 순간 벌금 도장.

## 5. 앞으로 장면마다 쓸 점검 (매뉴얼 반영 후보 — 사용자 확인 전)

1. **이 문장의 명사·동사는 무엇인가 → 그림은 그것이다.** 상징을 그리려 하면 "레퍼런스라면 실물·실제 그래프를 썼을까"를 먼저 묻습니다(E1·E4·E7).
2. **주인공 사물은 무엇이고, 문장마다 그 위에 무엇이 붙나**(E2).
3. **구절마다 바뀌는 것을 적는다.** 5초 넘게 큰 변화가 없으면 이유를 적습니다(정의 읽히기·숫자 새기기)(E3). `python scripts/hold_measure.py <장면.mp4>` 로 잽니다.
4. **기존판과 나란히 놓고 "무엇이 더 잘 이해되는지" 한 문장**을 적지 못하면 바꾸지 않습니다([67 §9](67-docu-reference-analysis.md)).

연출 결정 기록(`decide`, 매뉴얼 05 §0-9)의 `refs` 에 이 문서의 §2 줄(예: `docs/68-explainer-docu-benchmark.md`)과 규칙 번호(E1~E8)를 적어 근거로 씁니다.
