# 이야기 서사형 영상 만들기 (템플릿 v2, 2026-11-28)

매뉴얼: `channels/ch-books/template_story_v2.md` · 대본 틀: `channels/ch-books/templates/story_v2.example.json` · 근거: `docs/75-story-ref-eden.md`
완성 예시: `projects/20261127-ref-eden-remake/02_script/remake_full.json` (레퍼런스 『에덴의 동쪽』 전체 재현, 21분)

작업 폴더 `W=E:/ytflow-local/books-video/<편>` (그림·소리·영상, Git 에 넣지 않음 → 끝나면 Google Drive `ytflow/영상/`).

| 단계 | 명령 | 결과 |
|---|---|---|
| 1. 대본 | 틀을 복사해 `02_script/story.json` 작성 → **사용자 대본 검토** | 문장·그림·카메라 |
| 2. 무료 낭독(검토·초안) | `YT_RATE=+28% YT_GAP=0.25 python voice.py story.json $W/voice` | narration.wav, timeline.json(단어 시각), 분당 약 440자 |
| 3. 그림 | `python gen_v2.py story.json $W 5` | 1단계 무대·인물 기준 그림 → 2단계 장면(기준 그림 참조) · 사용자 Codex `$imagegen` |
| 4. 배경음악 | `python bgm.py $W/bgm.wav <길이초>` | 자체 합성 잔잔한 피아노풍, 말보다 약 13dB 낮게 |
| 5. 렌더 계획 | `python build_plan_v2.py story.json $W <이름>.mp4` | 문장 하나 = 그림 하나, 같은 그림이 이어지면 한 샷 |
| 6. 점검 프레임 | `python render.py $W/plan.json --frames` | 샷마다 프레임 — 글자 겹침·인물·방 일관성 확인 |
| 7. 렌더 | `python render.py $W/plan.json` | 1080p, 겹침 전환, 그림 위 장 제목, 상자 없는 단어 싱크 자막, 배경음악 |
| 8. 대조(레퍼런스가 있을 때) | `python compare.py story.json <ref_dir> $W/<이름>.mp4 $W/voice $W/compare <끝초>` | 문장별 나란히 프레임 + 장면 수·길이·카메라 비율·말 속도 |

v1 도구(표·지도·이름표·날씨·전후 그림 — `art_jobs.py`, `keyframes.py`, render.py 의 해당 기능)는 남아 있지만 **v2 이야기형에서는 쓰지 않는다**(plan 의 `"subtitle": "plain", "recon": false`).
