# 본편 생성기 (HyperFrames)

- `build_full.py` — 대본 v2 전체(문장 = 박자) → edge-tts(낱말 시각) → `hf_full/index.html` + 목소리·효과음. Drive `영상/20261126-history-sohyeon/hf_full/`.
- `eng.py` — 공통 연출 조각(재현 그림 시차·촛불·먼지, 타자기, 도장+흔들림, 번쩍임, 휩, 빛샘, 잉크 번짐, 자막, 합성 효과음).
- `geo.py` — 지도 땅 모양. `geo/land50.json` 은 커밋하지 않음: `https://cdn.jsdelivr.net/npm/world-atlas@2.0.2/land-50m.json` (ISC, tools/external.json 에 고정된 판) 을 내려받아 같은 폴더의 `geo/` 에.
- 실행: `python build_full.py` → `cd hf_full && npx hyperframes check && npx hyperframes render -o ../sohyeon_full_v1.mp4 -q looks`.
- 그림 경로는 Drive 의 `samples/`·`art/` (Codex 생성, A안).
