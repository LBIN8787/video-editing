# 제목·썸네일 — 20261121-market-daily

**제목(기본):** 검은 금요일, 엔비디아·브로드컴·삼성전자가 같이 빠진 이유 | 11월 21일

**제목 후보 (A/B 시험용)**
1. 엔비디아 SEC 회계 조사 보도에 하루 -14%, 월요일 한국 장은? | 11월 21일
2. 엔비디아 -14%·나스닥 -5.28% — 숫자는 같은데 무엇이 바뀌었나 | 11월 21일
3. 검은 금요일 다음 날, 엔비디아·브로드컴·삼성전자가 같이 빠진 이유 | 11월 21일

**제목을 이렇게 정한 이유**
- 핫 키워드(엔비디아·SEC·회계 조사·14%)를 앞 20자 안에 + 내 계좌로 번역(월요일 한국 장) + 날짜
- 숫자 대비 + 질문
- 장면(검은 금요일) + 다룬 종목

## 썸네일
### A — 검은 엔비디아 간판 + 단정 + 숫자 (photo full)
![A](thumbnail_A.png)

- 핫 키워드(엔비디아·SEC) 큰 글씨 + 구체적 숫자, 질문 없이 단정
- manual/09 §7-1 ③ 기본 모양 — 사건의 회사 사진을 어둡게

### B — 숫자 대비 (dark)
![B](thumbnail_B.png)

- 숫자 둘 대비

### C — 검은 여의도 + 검은 금요일 (photo full)
![C](thumbnail_C.png)

- 다음 일정 + 한국 계좌
- 국내 제목 '검은 금요일' 키워드

### D — 연준 쿡 이사 인물 + 검은 금요일 (person)
![D](thumbnail_D.png)

- 영상 이야기 3의 당사자(연설 원문 ✅) + 사용자가 고른 '검은 금요일'
- 주식이 빠진 날 연준은 인상 쪽 — 반전

### E — 구글 TPU 보드 + 주문 이동 (photo full)
![E](thumbnail_E.png)

- 영상 이야기 2 — 구글·브로드컴
- 조사일 뿐이라 아래 줄에 확인 없음을 밝힘

### F — 숫자 대비: TPU 100만 개 vs 브로드컴 -12% (versus dark)
![F](thumbnail_F.png)

- 구글·브로드컴 숫자 둘 대비
- 'AI가 끝났나'보다 '누구 몫이 줄었나'(I3)

## 올릴 썸네일 (자동 선택 — docs/49·55 근거 점수, `--thumb` 로 바꿀 수 있음)
**D** (대본에서 지정)

- A: 3.5점 — 핫 키워드 큰 글씨(SEC) +2 (manual/09 §7-1 ①) · 구체적 숫자 +1.5 (docs/49 §3)
- B: 2.0점 — 구체적 숫자 +1.5 (docs/49 §3) · 휴대폰 목록에서도 큰 글씨 +0.5
- C: 1.5점 — 구체적 숫자 +1.5 (docs/49 §3)
- D: -3.0점 — 점검 실패(글자 크기·재생 시간 자리) −5 · 구체적 숫자 +1.5 (docs/49 §3) · 당사자 따옴표 발언 +0.5
- E: 1.5점 — 구체적 숫자 +1.5 (docs/49 §3)
- F: 2.0점 — 구체적 숫자 +1.5 (docs/49 §3) · 휴대폰 목록에서도 큰 글씨 +0.5

## 점검
```json
{
 "A": {
  "timestamp_overlap": false,
  "smallest_text_px_at_168w": 7.3,
  "ok": true
 },
 "B": {
  "timestamp_overlap": false,
  "smallest_text_px_at_168w": 11.0,
  "ok": true
 },
 "C": {
  "timestamp_overlap": false,
  "smallest_text_px_at_168w": 7.3,
  "ok": true
 },
 "D": {
  "timestamp_overlap": false,
  "smallest_text_px_at_168w": 6.8,
  "ok": false,
  "face_area": 0
 },
 "E": {
  "timestamp_overlap": false,
  "smallest_text_px_at_168w": 7.3,
  "ok": true
 },
 "F": {
  "timestamp_overlap": false,
  "smallest_text_px_at_168w": 11.6,
  "ok": true
 }
}
```
