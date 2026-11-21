---
from: claude-code
type: clip-fetch
project: 20261120-market-deep-druckenmiller
status: cancelled
---

PC 에서 원본 발언 구간만 받아 주세요 (docs/50-clip-lane.md). 클라우드는 유튜브 봇 확인 때문에 받지 못합니다.

```
git pull
python -m ytflow clip-fetch 20261120-market-deep-druckenmiller      # 본인 브라우저 로그인으로 아래 구간만 받음 → Drive + 04_assets/footage
python -m ytflow hybrid 20261120-market-deep-druckenmiller          # 원본이 들어간 판으로 다시 렌더
git add projects/20261120-market-deep-druckenmiller/04_assets/clip_manifest.json && git commit -m "clip-fetch 20261120-market-deep-druckenmiller" && git push
```

| 원본 | 누구 | 주소 | 구간 | 쓰는 장면 |
|---|---|---|---|---|
| druck_qa | 진행자 · 스탠리 드러켄밀러 | https://www.youtube.com/watch?v=6r3D-CMJkuI | 118.5~131.0초 (12.5초) | 장면 [1] |
| druck_notlose | 스탠리 드러켄밀러 | https://www.youtube.com/watch?v=6r3D-CMJkuI | 490.5~496.8초 (6.3초) | 장면 [2] |
| druck_2027 | 스탠리 드러켄밀러 | https://www.youtube.com/watch?v=6r3D-CMJkuI | 720.5~727.8초 (7.3초) | 장면 [29] |
| druck_break | 스탠리 드러켄밀러 | https://www.youtube.com/watch?v=6r3D-CMJkuI | 555.5~562.8초 (7.3초) | 장면 [31] |

끝나면 이 파일의 status 를 done 으로 바꾸고 아래에 결과(받은 파일·길이·실패 이유)를 적어 주세요.


취소: 같은 주문을 권리 표시(official)와 함께 다시 만든 `20261121-1742-clip-fetch-20261120-market-deep-druckenmiller.md` 로 대체.
