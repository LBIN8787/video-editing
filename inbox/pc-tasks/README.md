# PC 할 일 — 클라우드가 못 하는 '내려받기·렌더'만 PC 로

클라우드(Claude Code 루틴)는 유튜브를 받지 못합니다(봇 확인, 우회 금지). 원본 발언 구간이 필요하면 클라우드가
`python -m ytflow clip-order <프로젝트>` 로 이 폴더에 한 편 = 한 파일을 올립니다. **PC 의 에이전트(Codex·Claude)** 가 처리합니다.
피클(휴대폰 브라우저)의 `inbox/requests/` 와 다릅니다 — 피클은 위치 찾기, PC 는 받기·렌더.

할 일 종류: `clip-fetch`(원본 발언 구간 받기 → `hybrid`), `looks-draw`(화풍 목록의 삽화 예시 그림 — `python -m ytflow looks --draw auto`: Codex 구독 → Gemini 키 → 주문서, ElevenLabs 금지).
PC 의 Claude Code 세션은 시작할 때 pending 할 일을 알림으로 봅니다(`scripts/pc_tasks.py`).

처리: 파일의 명령을 실행하고, frontmatter `status: done` 과 결과(받은 파일·길이·실패 이유)를 적어 main 에 푸시.
원본 영상 파일은 git 에 넣지 않습니다(Drive `ytflow/cache/clips/<프로젝트>/`). 자세한 것: `docs/50-clip-lane.md`.

## (뺌) 자동 처리 — PC 일꾼

2026-11-21 사용자: "자동일꾼 그냥 빼 나 그냥 로컬에서 전부 영상작업 할테니까". 이 폴더의 할 일은 PC 에서 Claude 세션(앱의 호기심 예약 작업 포함)이 열릴 때 처리합니다. 호기심 한 편의 그림·렌더는 `config/local_routines/curiosity.md` 대로 그 세션이 직접 합니다(`scripts/curiosity_build.py`, 설정 `02_script/build.json`).
