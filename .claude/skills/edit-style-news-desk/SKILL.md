---
name: edit-style-news-desk
description: 뉴스 데스크 카드 스타일(어두운 고정 틀 위 '한 소식 = 한 장': 순번·진행 막대·꼬리표·강조 제목·숫자 3칸·증거 패널·출처 줄)로 여러 소식을 차례로 정리한다. 주간 정리, 매일 시장 브리핑의 소식 2~3개, AI 업계 위클리에 쓴다.
---
# 뉴스 데스크 카드 (`styles/news-desk/STYLE.md`, 장면 `newsdesk`)
1. 소식마다 `newsdesk` 장면 하나: idx/total/source, tag(주의·사례·지금 할 일), headline+hl, sub, stats≤3, bullets≤3, panel(shot/bignum/stamp), footer. 박자 2개.
2. 숫자·캡처는 1차 출처로 확인된 것만. 캡처는 `04_assets/` 아래 경로.
3. 2~3장마다 다른 장면(인과 지도·차트·bite)을 섞는다 — 이 틀만 이어지면 지루함.
4. `python -m ytflow hybrid <프로젝트>` 후 프레임 확인: 제목이 오른쪽 패널을 침범하지 않는지(14자 안팎), 도장 글자가 한 줄인지.

5. 오른쪽 패널 대신 **모션 무대**(`beats[].motion`, x 1100~1800·y 200~700)로 말에 맞춰 사물이 생기게 할 수 있다 — 흐름·이동·관계 소식에 (docs/25 §5).
