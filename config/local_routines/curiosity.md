호기심 채널 '한겹 더 보면'(`channels/ch-knowledge`, 브랜드 curiosity, 주 1편)의 제작을 다음 사용자 결정 지점까지 진행하세요.
사용자 결정(D1 주제 · D2 대본 · D3 화면 · D4 최종 승인)은 대신 내리지 않습니다 — 그 지점에서 멈추고 결정 요청 파일만 남깁니다.

## 0. 준비
- 지금 폴더는 이 작업 전용 git worktree 이고, 최신 origin/main 에서 시작했습니다. 결과는 `git push origin HEAD:main` 으로 올립니다(거부되면 `git pull --rebase origin main` 후 다시, 최대 3번). 편이 다른 브랜치에 있으면(`REPORT.md`·pc-tasks 의 `branch:`) 그 브랜치에서 이어 갑니다.
- 먼저 AGENTS.md, manual/README.md, **manual/04-curiosity.md**, **manual/11-workflow.md**(S0~S9·D1~D4), `channels/ch-knowledge/channel.yaml`·`episodes.md`, `inbox/pc-tasks/README.md` 를 읽습니다.
- 사용량을 아낍니다: 하루에 한 편을 한 결정 지점만큼만 밀고, 렌더는 PC 일꾼(pc-tasks)에 맡깁니다.

## 1. 진행 중인 편 찾기
`projects/*/01_research/topic_brief.json` 의 brand 가 curiosity 이고 최근 45일 안에 시작했으며, 아직 올리지 않은 편(`05_edit/youtube_publish.json` 없음, episodes.md 에 '올림' 없음)을 찾습니다. `_sample-` 로 시작하는 폴더와 시험용(sample·broll-sample) 편은 뺍니다.
`inbox/decisions/` 에서 그 편의 열린 결정 요청과, 사용자가 남긴 답(`review` 기록·`script_review.md`·`topic_brief.decision`·REPORT.md 의 사용자 원문)을 확인합니다.

## 2. 편마다 지금 단계 → 다음 결정 지점까지 (manual/11 §1 표)
- **D1 답 없음** (topic_card 있음, decision 비어 있음) → 그대로 대기. 결정 요청 파일이 없을 때만 다시 씁니다.
- **D1 답 있음, `02_script/script_v1.md` 없음** → S2 조사(factsheet·sources·`audience.md`) → S3 `intent.md` → S4 줄글 대본 `script_v1.md` → `check --upto G4` → **D2 요청**.
- **D2 기각** → 사유대로 S3/S4 다시 → D2 요청.
- **D2 통과, 장면 기획 없음** → S5 장면표(`shotlist.md` + `hybrid.json`/`build.json`)·원화 주문서 → `check --upto G5` → `inbox/pc-tasks/` 에 할 일 두 개(`art-draw` → `after:` 로 이은 `curiosity-build`)를 올립니다. 그림부터 완성 영상까지는 PC 일꾼(`scripts/pc_worker.py`, 10분마다)이 만듭니다. D3 는 사용자가 "샘플 없이"라고 하지 않았다면 대표 장면 샘플 확인을 요청합니다.
- **pc-tasks 빌드가 failed** → 결과의 실패 이유를 한 가지 고쳐 다시 pending 으로(같은 원인으로 두 번째 실패면 고치지 말고 보고).
- **빌드 done, D4 답 없음** → S8 포장(제목 3·썸네일 A/B/C·`yt-pack`) → `check` → **D4 요청** (`final.mp4` 은 Google Drive `영상/<프로젝트>/05_edit/`).
- **D4 통과** (`review --pass` 기록) → S9: 승인 조건대로 목소리 확인 → `yt-publish <프로젝트>`(채널 설정: 일부 공개) → episodes.md 한 줄.
- **D4 기각** → `review --reject` 로 원문이 기록됐는지 확인하고, 이유에 따라 S4·S5·S7 로.

## 3. 진행 중인 편이 없을 때
마지막 편 시작이 7일 이상 지났으면(주 1편) 새 편: S0 착수 메모 → S1a 신호(`inbox/newsletters/` 의 호기심 소재·`python -m ytflow demand --channel ch-knowledge`) → S1b 후보 3개 주제 카드(`topic_brief.json` candidates·`topic_card.md`) → `check --upto G1` → **D1 요청**. 7일이 안 됐으면 아무것도 만들지 않고 '대기'로 끝냅니다.

## 4. 결정 요청 파일
`inbox/decisions/<YYYYMMDD>-<프로젝트>-D<n>.md`, 머리말 `status: open`, `project:`, `decision: D<n>`. 본문은 짧게: 무엇을 보면 되나(파일 경로·Drive 경로), 묻는 것 한 줄, 예상 소요 시간. 답이 기록되면 다음 실행에서 `status: answered` 로 바꿉니다.

## 지킬 것
- 사실·숫자는 1차 출처(원 논문·후속 연구·기관 자료)로 확인한 것만. 레퍼런스 채널의 대사·캐릭터·썸네일을 복제하지 않습니다.
- 사이트 차단·봇 확인을 우회하지 않습니다. 막히면 다른 출처를 쓰고 보고에 한 줄만.
- 그림은 Codex imagegen(GPT 이미지, PC 일꾼)으로. ElevenLabs 로 그리지 않습니다. 큰 파일은 git 에 넣지 않습니다(Google Drive).
- 매뉴얼·규칙 파일(manual/OWNERS.yaml 의 protected)은 고치지 않습니다. 고칠 점이 보이면 `python -m ytflow manual-propose` 로 제안만.

## 보고 (LOCAL_RESULT.md)
첫 줄: `호기심 <날짜>: <프로젝트> <한 일> → <D? 결정 기다림 | PC 빌드 중 | 대기>` 한 줄.
그 아래 짧게: 편마다 단계, 새로 연 결정 요청 파일, 막힌 것.
