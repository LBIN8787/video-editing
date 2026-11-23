# 제목·썸네일 — 20261122-market-deep-memory-insight

**제목(기본):** "2030년까지 부족" vs "2027년 말부터 하락" — 메모리 호황, 누구 말이 맞나 (2부)

**제목 후보 (A/B 시험용)**
1. "2030년까지 부족" vs "2027년 말부터 하락" — 메모리 호황, 누구 말이 맞나 (2부)
2. 최태원·마이크론 CEO·월가가 말하는 메모리 호황의 끝 — 근거만 따져 보면
3. 메모리 슈퍼사이클은 진짜 다를까? 낙관과 신중, 근거끼리 맞대기

**제목을 이렇게 정한 이유**
- 숫자 대결 + 인물·기관
- 이름 있는 사람들 + 근거 검증
- 트렌드 키워드(슈퍼사이클) + 질문

## 썸네일
### A — 인물 — 최태원 + 사이클이 훨씬 길어진다
![A](thumbnail_A.png)

- 당사자 얼굴 + 그의 말 (docs/59)

### B — 인물 — 메로트라 + 부족은 2026년을 훨씬 넘는다
![B](thumbnail_B.png)

- 당사자 얼굴 + 숫자

### C — 인물 — 젠슨 황 + 수요가 세계 생산보다 크다
![C](thumbnail_C.png)

- 가장 큰 이름 (젠슨 황 효과, docs/55)

### D — 숫자 맞대기 — 2030 vs 2027
![D](thumbnail_D.png)

- 두 시각을 숫자로

### E — 실사 — 웨이퍼 더미 셋 + 누구 말이 맞나
![E](thumbnail_E.png)

- 구조·호기심

## 올릴 썸네일 (자동 선택 — docs/49·55 근거 점수, `--thumb` 로 바꿀 수 있음)
**C**

- C: 5.5점 — 사건 당사자 얼굴 크게(젠슨 황) +3 — 인물 제목의 터진 영상 42% vs 안 된 10% (docs/55) · 제목 앞에도 같은 이름 +1 · 구체적 숫자 +1.5 (docs/49 §3)
- A: 5.0점 — 사건 당사자 얼굴 크게(최태원) +3 — 인물 제목의 터진 영상 42% vs 안 된 10% (docs/55) · 구체적 숫자 +1.5 (docs/49 §3) · 당사자 따옴표 발언 +0.5
- B: 5.0점 — 사건 당사자 얼굴 크게(산제이 메로트라) +3 — 인물 제목의 터진 영상 42% vs 안 된 10% (docs/55) · 구체적 숫자 +1.5 (docs/49 §3) · 당사자 따옴표 발언 +0.5
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
