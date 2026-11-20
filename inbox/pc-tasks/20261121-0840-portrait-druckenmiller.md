---
from: claude-code
type: art
project: 20261120-market-deep-druckenmiller
status: pending
---

드러켄밀러 썸네일용 **손그림 초상 삽화** 한 장을 그려 주세요 (2026-11-21 사용자 선택: "손그림 초상 삽화").
위키미디어 공용에 자유 사진이 없고, 뉴스 사진·방송 캡처는 썸네일에 쓰지 않으므로(manual/09 §13) 사진을 그대로 쓰지 말고 **새로 그린 그림**이어야 합니다.

- 저장: `projects/20261120-market-deep-druckenmiller/04_assets/footage/raw/druckenmiller_portrait.png` (git 에 올리지 않음 — Drive `ytflow/cache/` 에도 보관)
- 크기: 세로 1600px 이상, 어깨 위 상반신, 정면 또는 살짝 옆, **얼굴이 그림 높이의 40~50%**
- 그림체: 굵은 펜 선 + 면 2~3색(살구·회색·남색), 종이 결 약간, 배경은 단색(짙은 남색 #0E1626 또는 흰색) — 글자 넣지 않음
- 특징: 70대 초반 미국 남성, 짧게 넘긴 흰머리, 마른 얼굴, 짙은 눈썹, 정장 재킷·흰 셔츠(넥타이 없음), 차분하고 진지한 표정
- 참고는 공개 사진·인터뷰 화면을 **보고 그리기만** (사진을 덧그리거나 그대로 옮기지 않음)
- 방법 (아무거나): ① Codex `$imagegen` (구독 한도 안) ② ChatGPT 웹·Canva ③ 직접 그리기 — ElevenLabs 로는 그리지 않음

그린 뒤:
```
python -m ytflow thumbnail 20261120-market-deep-druckenmiller
```
썸네일 A 가 초상 + '벌기보다 안 잃기' 로 만들어집니다. 끝나면 status 를 done 으로 바꾸고 결과를 적어 주세요.
