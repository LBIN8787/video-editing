# (가칭) 장면의 이유 — 애니 소개 (초안)

1~3화의 스토리 핵심 장면만 잘라 내레이션으로 잇고, 가장 궁금한 지점에서 끊어 "이거 봐야겠다"로 끝내는 소개 채널.
설계·수요 분석: [`docs/37-anime-review-channel.md`](../../docs/37-anime-review-channel.md)

```bash
# 에피소드 파일 → projects/<프로젝트>/04_assets/episodes/ (이름 순서 = 화 순서, 커밋 안 함)
python -m ytflow recap <프로젝트> --transcribe   # 대사표 01_research/episodes.md
python -m ytflow recap <프로젝트> --plan         # 장면·내레이션 초안 02_script/recap.json
python -m ytflow recap <프로젝트> --check        # 규칙 검사
python -m ytflow recap <프로젝트>                # 렌더 05_edit/final.mp4
```

- **규칙 (`recap_rules`):** 앞 3화까지·결말 없음 · 원작 소리 장면 ≤ 8초, 합 ≤ 20% · 끝에 볼 수 있는 곳 · OST 안 씀 · 탐지 회피 편집 안 함
- **가끔 섞는 분석형:** 같은 작품의 복선·연출 분석 (채널이 '요약만 하는 채널'로 보이지 않게)
