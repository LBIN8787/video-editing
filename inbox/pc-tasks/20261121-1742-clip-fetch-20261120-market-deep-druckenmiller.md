---
from: claude-code
type: clip-fetch
project: 20261120-market-deep-druckenmiller
status: done
---

**가장 쉬운 방법: 저장소 폴더의 `pc-clip-fetch.bat` 를 더블클릭** (받기·렌더·기록 올리기까지 한 번에).

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

> PC 2026-11-21 22:10 완료 (브랜치 claude/gallant-hawking-asp7le)
> - 대담 4구간(druck_*)은 19:20 에 받은 것을 그대로 씀(구간은 manifest 의 넓힌 창 유지). 모건스탠리 7구간(hl_*)은 이 PC 에서 새로 받음 → 11/11 ok, Drive `ytflow/cache/clips/20261120-market-deep-druckenmiller/`
> - `hl_broll`(소리 없는 화면)은 인용한 hl 구간을 이은 뒤 **드러켄밀러가 나오는 컷만** 다시 골라 33.5초로 만듦(처음 판은 진행자만 비춤). 장면 #37 화면 시작 14.7 → 15.7초(#12 와 같은 컷 반복 방지)
> - 썸네일 A·B 얼굴: 같은 공식 영상 화면 한 장(`04_assets/footage/raw/druckenmiller.jpg`, hl_broll 8초) → A 6.0점 추천
> - 렌더: 장면 44/44, 910.6초, -14.1 LUFS, 겹침 0, sync-qa 통과(중앙값 0.05초). 목소리는 edge 초안(ElevenLabs 401 — 키 확인 필요)
> - 완성본: Drive `ytflow/영상/20261120-market-deep-druckenmiller/druckenmiller_final_clips.mp4` (+ thumbnail_A/B/C)
> - 처음 렌더 실패 원인: C 드라이브 여유 3.6GB → HyperFrames 임시 프레임 공간 부족. TEMP 를 E 로 돌려 해결
