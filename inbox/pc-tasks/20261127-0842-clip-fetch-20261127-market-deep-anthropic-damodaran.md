---
from: claude-code
type: clip-fetch
project: 20261127-market-deep-anthropic-damodaran
status: done
done_at: 2026-11-27 08:58 KST (PC 심층 제작 작업이 직접 받음 — 전체 720p 를 TEMP 에 받아 구간 자르기)
---

PC 에서 원본 발언 구간만 받아 주세요 (docs/50-clip-lane.md). 클라우드는 유튜브 봇 확인 때문에 받지 못합니다.

```
git pull
python -m ytflow clip-fetch 20261127-market-deep-anthropic-damodaran      # 본인 브라우저 로그인으로 아래 구간만 받음 → Drive + 04_assets/footage
python -m ytflow hybrid 20261127-market-deep-anthropic-damodaran          # 원본이 들어간 판으로 다시 렌더
git add projects/20261127-market-deep-anthropic-damodaran/04_assets/clip_manifest.json && git commit -m "clip-fetch 20261127-market-deep-anthropic-damodaran" && git push
```

| 원본 | 누구 | 주소 | 구간 | 쓰는 장면 |
|---|---|---|---|---|
| dmd_trillion | 애스워스 다모다란 | https://www.youtube.com/watch?v=IgvDUUn3uuE | 2092.5~2111.0초 (18.5초) | 장면 [1] |
| dmd_double | 애스워스 다모다란 | https://www.youtube.com/watch?v=IgvDUUn3uuE | 1951.2~1959.2초 (8.0초) | 장면 [7] |
| dmd_hat | 애스워스 다모다란 | https://www.youtube.com/watch?v=IgvDUUn3uuE | 2591.4~2600.2초 (8.8초) | 장면 [8] |
| dmd_mismatch | 애스워스 다모다란 | https://www.youtube.com/watch?v=IgvDUUn3uuE | 1908.3~1921.8초 (13.5초) | 장면 [15] |
| dmd_overkill | 애스워스 다모다란 | https://www.youtube.com/watch?v=IgvDUUn3uuE | 2207.5~2219.2초 (11.7초) | 장면 [23] |
| cw_conf | 캐시 우드 | https://www.youtube.com/watch?v=9s_ufgiiyLY | 45.3~54.0초 (8.7초) | 장면 [19] |
| cw_pareto | 캐시 우드 | https://www.youtube.com/watch?v=9s_ufgiiyLY | 139.9~145.4초 (5.5초) | 장면 [20] |

끝나면 이 파일의 status 를 done 으로 바꾸고 아래에 결과(받은 파일·길이·실패 이유)를 적어 주세요.
