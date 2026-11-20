# PC 할 일 — 클라우드가 못 하는 '내려받기·렌더'만 PC 로

클라우드(Claude Code 루틴)는 유튜브를 받지 못합니다(봇 확인, 우회 금지). 원본 발언 구간이 필요하면 클라우드가
`python -m ytflow clip-order <프로젝트>` 로 이 폴더에 한 편 = 한 파일을 올립니다. **PC 의 에이전트(Codex·Claude)** 가 처리합니다.
피클(휴대폰 브라우저)의 `inbox/requests/` 와 다릅니다 — 피클은 위치 찾기, PC 는 받기·렌더.

처리: 파일의 명령(`clip-fetch` → `hybrid`)을 실행하고, frontmatter `status: done` 과 결과(받은 파일·길이·실패 이유)를 적어 main 에 푸시.
원본 영상 파일은 git 에 넣지 않습니다(Drive `ytflow/cache/clips/<프로젝트>/`). 자세한 것: `docs/50-clip-lane.md`.
