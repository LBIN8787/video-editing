# 제목·썸네일 — 20261122-market-deep-nvidia-insight

**제목(기본):** "GPU 는 8년 번다" vs "3년이면 끝" — 엔비디아 순환금융, 누가 맞나 (2부)

**제목 후보 (A/B 시험용)**
1. "GPU 는 8년 번다" vs "3년이면 끝" — 엔비디아 순환금융, 누가 맞나 (2부)
2. 돌아온 젠슨 황 vs 짐 채노스 — 엔비디아 1,180억 달러 보증, 근거만 따져 보면
3. 엔비디아 순환금융의 진짜 쟁점은 'GPU 수명'이다

**제목을 이렇게 정한 이유**
- 숫자 대결
- 인물 대결 + 숫자
- 단정 한 마디

## 썸네일
### A — 인물 — 젠슨 황 + GPU 는 8년을 번다?
![A](thumbnail_A.png)

- 당사자 얼굴 + 그의 말 (docs/59)

### B — 인물 — 젠슨 황(스탠퍼드) + 칩을 담보로 빚을 낸다
![B](thumbnail_B.png)

- 당사자 얼굴 + 쟁점

### C — 인물 — 젠슨 황 vs 채노스 (8년 vs 3년)
![C](thumbnail_C.png)

- 인물 + 반대 주장 숫자

### D — 숫자 맞대기 — 8년 vs 3년
![D](thumbnail_D.png)

- 두 시각을 숫자로

### E — 실사 — 기울어지는 GPU·금괴 탑 + 진짜 쟁점은 GPU 수명
![E](thumbnail_E.png)

- 구조·단정

## 올릴 썸네일 (자동 선택 — docs/49·55 근거 점수, `--thumb` 로 바꿀 수 있음)
**A**

- A: 5.0점 — 사건 당사자 얼굴 크게(젠슨 황) +3 — 인물 제목의 터진 영상 42% vs 안 된 10% (docs/55) · 구체적 숫자 +1.5 (docs/49 §3) · 당사자 따옴표 발언 +0.5
- B: 5.0점 — 사건 당사자 얼굴 크게(젠슨 황) +3 — 인물 제목의 터진 영상 42% vs 안 된 10% (docs/55) · 구체적 숫자 +1.5 (docs/49 §3) · 당사자 따옴표 발언 +0.5
- C: 4.5점 — 사건 당사자 얼굴 크게(젠슨 황) +3 — 인물 제목의 터진 영상 42% vs 안 된 10% (docs/55) · 구체적 숫자 +1.5 (docs/49 §3)
- D: 2.0점 — 구체적 숫자 +1.5 (docs/49 §3) · 휴대폰 목록에서도 큰 글씨 +0.5
- E: 1.5점 — 구체적 숫자 +1.5 (docs/49 §3)

## 점검
```json
{
 "A": {
  "timestamp_overlap": false,
  "smallest_text_px_at_168w": 6.0,
  "ok": true,
  "face_area": null
 },
 "B": {
  "timestamp_overlap": false,
  "smallest_text_px_at_168w": 6.0,
  "ok": true,
  "face_area": null
 },
 "C": {
  "timestamp_overlap": false,
  "smallest_text_px_at_168w": 6.8,
  "ok": true,
  "face_area": null
 },
 "D": {
  "timestamp_overlap": false,
  "smallest_text_px_at_168w": 14.4,
  "ok": true
 },
 "E": {
  "timestamp_overlap": false,
  "smallest_text_px_at_168w": 7.9,
  "ok": true
 }
}
```
