# 제목·썸네일 — 20261122-market-deep-nvidia-circular

**제목(기본):** 돈 빌려주고 칩 판다? 엔비디아 1,180억 달러 보증의 정체

**제목 후보 (A/B 시험용)**
1. 돈 빌려주고 칩 판다? 엔비디아 1,180억 달러 보증의 정체
2. 루슨트의 데자뷔? 엔비디아가 고객에게 돈 대는 이유
3. 이 고리가 끊기면 삼성·하이닉스도 맞는다 — 엔비디아 순환금융

**제목을 이렇게 정한 이유**
- 흔한 오해를 질문으로 + 숫자
- 최신 사건(CEO 사임·복귀) + 숫자
- 한국 계좌로 번역 — 영상 5장

## 썸네일
### A — 실사 — 금고 속 달러 위 GPU + 자기 칩을 자기가 산다?
![A](thumbnail_A.png)

- 젊은 층 (2026-11-22 사용자): 흔한 물음을 구어체로 + 3D 일러스트

### B — 인물형 — 젠슨 황 + 보증 1,180억
![B](thumbnail_B.png)

- 인물(사임) + 영상 핵심 숫자

### C — 실사 — 기울어지는 GPU·금괴 탑 + 돈 빌려주고 칩 파는 구조
![C](thumbnail_C.png)

- 젊은 층: 구조를 한 줄로 + 3D 일러스트

### D — 실사 — 서버 랙 사이를 도는 달러 + 엔비디아 돈이 엔비디아로
![D](thumbnail_D.png)

- 자기 칩 썸네일의 변형 — 돈의 고리를 실사로

## 올릴 썸네일 (자동 선택 — docs/49·55 근거 점수, `--thumb` 로 바꿀 수 있음)
**B**

- A: 0.0점 — 
- B: 5.0점 — 사건 당사자 얼굴 크게(젠슨 황) +3 — 인물 제목의 터진 영상 42% vs 안 된 10% (docs/55) · 구체적 숫자 +1.5 (docs/49 §3) · 휴대폰 목록에서도 큰 글씨 +0.5
- C: 0.0점 — 
- D: 0.0점 — 

## 점검
```json
{
 "A": {
  "timestamp_overlap": false,
  "smallest_text_px_at_168w": 7.9,
  "ok": true
 },
 "B": {
  "timestamp_overlap": false,
  "smallest_text_px_at_168w": 13.7,
  "ok": true,
  "face_area": null
 },
 "C": {
  "timestamp_overlap": false,
  "smallest_text_px_at_168w": 7.9,
  "ok": true
 },
 "D": {
  "timestamp_overlap": false,
  "smallest_text_px_at_168w": 7.9,
  "ok": true
 }
}
```
