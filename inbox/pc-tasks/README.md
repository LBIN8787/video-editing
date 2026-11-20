# PC 할 일 — 클라우드가 못 하는 '내려받기·렌더'만 PC 로

클라우드(Claude Code 루틴)는 유튜브를 받지 못합니다(봇 확인, 우회 금지). 원본 발언 구간이 필요하면 클라우드가
`python -m ytflow clip-order <프로젝트>` 로 이 폴더에 한 편 = 한 파일을 올립니다. **PC 의 에이전트(Codex·Claude)** 가 처리합니다.
피클(휴대폰 브라우저)의 `inbox/requests/` 와 다릅니다 — 피클은 위치 찾기, PC 는 받기·렌더.

할 일 종류: `clip-fetch`(원본 발언 구간 받기 → `hybrid`), `looks-draw`(화풍 목록의 삽화 예시 그림 — `python -m ytflow looks --draw auto`: Codex 구독 → Gemini 키 → 주문서, ElevenLabs 금지).
PC 의 Claude Code 세션은 시작할 때 pending 할 일을 알림으로 봅니다(`scripts/pc_tasks.py`).

처리: 파일의 명령을 실행하고, frontmatter `status: done` 과 결과(받은 파일·길이·실패 이유)를 적어 main 에 푸시.
원본 영상 파일은 git 에 넣지 않습니다(Drive `ytflow/cache/clips/<프로젝트>/`). 자세한 것: `docs/50-clip-lane.md`.

## 자동 처리 — PC 일꾼 (2026-11-20 사용자: "나 앞으로 매번 내가 손수 명령하기 싫어 … 자동화 세팅 설정해놔" · "이 호기심 채널 영상제작 자동화" · "로컬에서 진행하도록")

PC 에서 **한 번만** 설치하면, 로그인해 있는 동안 10분마다 이 폴더의 `status: pending` 을 사람 명령 없이 처리합니다.

```powershell
# 저장소 폴더에서 (PowerShell) — 한 번만
powershell -ExecutionPolicy Bypass -File scripts\install_pc_worker.ps1
# 끄기: Unregister-ScheduledTask -TaskName ytflow-pc-worker -Confirm:$false     로그: %LOCALAPPDATA%\ytflow\pc_worker.log
```
필요한 것: `codex login`(ChatGPT 구독 — GPT 이미지), `YTFLOW_DRIVE`(Drive for desktop 의 ytflow 폴더), Git Bash·ffmpeg·node(렌더), 목소리 최종본은 `ELEVENLABS_API_KEY`(없으면 edge-tts 초안).

일꾼(`scripts/pc_worker.py`)은 사용자 폴더를 건드리지 않고 옆에 작업 폴더 두 개(`<저장소>-worker` = main, `<저장소>-worker-task` = 할 일의 브랜치)를 씁니다.
할 일 하나를 집으면 `in_progress` 로 바꿔 main 에 올리고(중복 방지), 끝나면 `## 결과 (pc-worker)` 와 `done|failed` 를 적어 올립니다. 2번 실패하면 `failed` 로 멈춥니다.

할 일 파일 머리말:
| 키 | 뜻 |
|---|---|
| `type` | `curiosity-build` 이면 `scripts/curiosity_build.py projects/<project>` 를 그대로 실행(원화 시트 → 실제 자료 → 칸 자르기 → 목소리 → 장면 → 렌더 → Drive `영상/<project>/05_edit/`). 그 밖(`art-draw`·`clip-fetch`·`looks-draw` …)은 Codex(없으면 Claude Code)가 본문 지시를 수행 |
| `project` | `projects/` 아래 폴더 이름 |
| `branch` | 프로젝트 파일이 있는 브랜치 (없으면 main) |
| `after` | 먼저 done 이 되어야 하는 할 일 파일 이름 (예: 원화 → 빌드) |

**호기심 한 편의 흐름:** 클라우드(또는 PC)가 대본·낭독본·장면 스크립트·`02_script/build.json`·원화 주문서를 쓰고 → 할 일 두 개(`art-draw` → `after:` 로 이어진 `curiosity-build`)를 올리면 → PC 일꾼이 그림부터 완성 영상까지 만듭니다.
