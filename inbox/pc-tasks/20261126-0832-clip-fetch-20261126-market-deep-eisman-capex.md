---
from: claude-code
type: clip-fetch
project: 20261126-market-deep-eisman-capex
status: done
---

PC 에서 원본 발언 구간만 받아 주세요 (docs/50-clip-lane.md). 클라우드는 유튜브 봇 확인 때문에 받지 못합니다.

```
git pull
python -m ytflow clip-fetch 20261126-market-deep-eisman-capex      # 본인 브라우저 로그인으로 아래 구간만 받음 → Drive + 04_assets/footage
python -m ytflow hybrid 20261126-market-deep-eisman-capex          # 원본이 들어간 판으로 다시 렌더
git add projects/20261126-market-deep-eisman-capex/04_assets/clip_manifest.json && git commit -m "clip-fetch 20261126-market-deep-eisman-capex" && git push
```

| 원본 | 누구 | 주소 | 구간 | 쓰는 장면 |
|---|---|---|---|---|
| eis_fail | 스티브 아이스먼 | https://www.youtube.com/watch?v=4Unch--PmW0 | 1516.0~1532.2초 (16.2초) | 장면 [1] |
| eis_change | 스티브 아이스먼 | https://www.youtube.com/watch?v=4Unch--PmW0 | 1539.8~1551.3초 (11.5초) | 장면 [16] |
| eis_70 | 스티브 아이스먼 | https://www.youtube.com/watch?v=4Unch--PmW0 | 1307.0~1315.2초 (8.2초) | 장면 [8] |
| eis_slow | 스티브 아이스먼 | https://www.youtube.com/watch?v=4Unch--PmW0 | 1994.8~2009.9초 (15.1초) | 장면 [18] |
| eis_peak | 스티브 아이스먼 | https://www.youtube.com/watch?v=4Unch--PmW0 | 2270.0~2278.3초 (8.3초) | 장면 [20] |
| sher_demand | 에릭 셰리든 | https://www.youtube.com/watch?v=XymmJNOQmD8 | 1065.5~1078.5초 (13.0초) | 장면 [2] |
| sher_15 | 에릭 셰리든 | https://www.youtube.com/watch?v=XymmJNOQmD8 | 919.5~929.0초 (9.5초) | 장면 [23] |
| cham_roi | 차마스 팔리하피티야 | https://www.youtube.com/watch?v=XymmJNOQmD8 | 526.0~537.0초 (11.0초) | 장면 [27] |
| cham_1pct | 차마스 팔리하피티야 | https://www.youtube.com/watch?v=XymmJNOQmD8 | 566.5~578.0초 (11.5초) | 장면 [28] |
| cham_bump | 차마스 팔리하피티야 | https://www.youtube.com/watch?v=XymmJNOQmD8 | 1351.5~1364.5초 (13.0초) | 장면 [30] |

끝나면 이 파일의 status 를 done 으로 바꾸고 아래에 결과(받은 파일·길이·실패 이유)를 적어 주세요.

## 결과 (2026-11-26 08:51 KST, deep-watch 2단계가 같은 PC 에서 처리)
- 10/10 받음 → `04_assets/clip_manifest.json`, Drive `ytflow/cache/clips/20261126-market-deep-eisman-capex/`
- `clip-fetch`(DASH 구간 받기)가 ffmpeg 에서 멈춤 → yt-dlp 로 720p 영상·영어 원음을 통째로 TEMP 에 받아 구간만 잘라 씀(전체 파일은 지움)
