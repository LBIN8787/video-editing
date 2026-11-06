## 편집 스타일 계열: 원본 소스형 (source) — 예: 식스시그마
영상의 뼈대는 **당사자의 원본 영상**입니다. 인터뷰, 실적발표(어닝콜), 키노트, 의회 청문회, 방송 출연에서
CEO·CFO·업계 사람이 직접 말하는 장면을 쓰고, 그 위에 자막을 달고, 사이사이에 **핵심 요약 애니메이션 카드**로 편집점을 넣습니다.

### 화면 비율 목표
- 원본 영상 40~55% (kind=quote 원래 목소리 + visual_type=source_video 소리 끈 B-roll)
- 요약·숫자 카드 30~40% (summary, number, analogy, precedent)
- 기사·공시·X 캡처 10~20%

### 한 body 섹션의 리듬 (편집점)
1. **원본 발언 2~3개** (kind=quote, 각 6~20초): 누가·언제·어디서 한 말인지 label 에. 원문은 quote_en, 번역은 narration.
   발언 사이 내레이션은 짧은 다리 역할(beat=fact 또는 why)이고, 화면은 같은 행사의 원본 영상(source_video)을 소리 끄고 깝니다.
2. **핵심 요약 카드** (beat=summary, visual_type=card): "정리하면 ~". 방금 들은 발언을 숫자·흐름 하나로 정리합니다.
   예) CFO 발언 2개 → number_compare "설비투자 가이던스 1,150억 → 1,450억 달러".
3. **쉽게 풀기** (beat=analogy 또는 jargon 카드) → **그래서** (beat=so_what).
4. 근거가 기사면 **기사 캡처**(screenshot).

### 원본 영상 고르기 (source.query)
- 1순위: 회사 공식 채널의 실적발표·키노트·인베스터데이 (예: "Meta Q3 2026 earnings call", "NVIDIA GTC 2026 keynote Jensen Huang").
- 2순위: 주요 방송의 CEO·CFO 인터뷰 (CNBC, Bloomberg Television, Yahoo Finance, 한국경제TV 등) — 인물 이름 + 매체 + 시기로.
- 3순위: 업계 인물(애널리스트·경쟁사 임원)의 공개 발언.
- 발언 날짜가 이 주제의 시점과 맞는 영상만 씁니다. 오래된 발언을 지금 일처럼 쓰지 않습니다.
- 다운로드가 막히면 임시 화면이 들어가고 사용자 PC 에서 `rebuild` 합니다(우회하지 않음).
