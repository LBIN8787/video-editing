---
name: manual-review
description: 매뉴얼 정기 검토(매일 밤 자동 실행·사람이 "매뉴얼 검토해" 할 때). manual-audit 로 충돌·과적합·폐지된 기준 잔재·깨진 참조·층 미정 피드백을 재고, 판단이 필요 없는 것만 고쳐 커밋하고, 판단이 필요한 것은 질문으로 남겨 그래프·알림으로 알린다.
---

# 매뉴얼 정기 검토 (docs/34)

사용자 결정 (2026-11-15): **매일 밤 · 분명한 것만 고침 · 휴대폰 알림 + 그래프**. 매뉴얼 버전은 올리지 않는다 (규칙의 뜻을 바꾸지 않으므로).

## 순서
0. **잠금**: `python -m ytflow manual-lock acquire --purpose "정기 검토 YYYY-MM-DD"` — 정해진 담당은 없고 이 검토도 한 작업일 뿐 (2시간, 잡자마자 main 을 합침). 다른 세션이 잡고 있으면 `manual-lock request "정기 검토 YYYY-MM-DD"` 를 남기고 audit 보고서만 읽어 알림으로 보고하고 끝낸다 (docs/35).
1. 최신으로: `git fetch origin` 후 작업 브랜치를 최신으로 (`git pull --rebase`). 작업 트리에 남의 변경이 있으면 건드리지 않는다. (acquire 가 main 을 이미 합쳤으면 아래 merge 는 할 것 없음)
   - **main 도 합친다** (`git merge origin/main`): 다른 세션이 main 에서 매뉴얼을 고치거나 버전을 올리므로, 검토는 둘을 합친 매뉴얼에 한다. 충돌은 **양쪽 내용을 모두 살려** 푼다. main 이 매뉴얼 버전을 이미 올렸으면 이 브랜치에서 새로 올린 버전은 그 뒤 번호로 바꾼다 (CHANGELOG·본문 표기 모두). 내용이 서로 반대면 고치지 말고 ask 로 남긴다.
   - 원격 `manual/vN` 스냅샷 브랜치는 **덮어쓰지 않는다** (force push 금지). 이미 있는 번호면 새 번호로.
2. 재기: `python -m ytflow manual-graph` → `python -m ytflow manual-audit`. `manual/audit.md` 를 읽는다.
2-1. **모순 점검** (2026-11-20 사용자: "모순되는 지침은 없는지 체크하고 주기적으로 이를 관리 할 수 있도록") — 장부 `manual/contradictions.yaml`.
   - **매일 (변경분):** audit 에 `모순 점검 차례: 바뀐 지침 N개` 가 있으면, 그 파일들의 바뀐 줄(`git diff <장부 last_commit>..HEAD -- <파일>`)을 읽고 같은 주제를 말하는 다른 지침을 `git grep` 으로 찾아 맞댄다. 대상: manual/ 본문, AGENTS.md·README·CLAUDE.md, skills/*/SKILL.md, prompts/, styles/*/STYLE.md·recipes, channels/*/channel.yaml, topics/, docs/(현재 기준으로 쓰인 절만).
   - **7일마다 (전체):** audit 에 `전체 모순 점검 차례` 가 있으면 주제별로 지침 전체를 맞댄다 — ① 대본·영상 구조(인트로·길이·마무리·말투·브리핑/심층·시간표·요일 형식·목소리) ② 화면·편집(채널별 기본 스타일·모션그래픽/삽화/실사 순서·카메라·배경음·그림 도구) ③ 운영(저장 위치·커밋·브랜치·잠금·검토 지점·업로드·PC 할 일·피클 요청) ④ **범위 — 피드백과 지침 분리** (2026-11-20 사용자: "특정 주제나 한 영상에 한해서 적용되는 내용이 모든 영상 지침에 쓸데없이 남지는 않았는지"): 공통 자리(README·01·05·06·11·12·AGENTS·공통 프롬프트·검사 코드)에 있거나 MUST·금지로 적힌 규칙의 출처를 CHANGELOG·reviews·feedback 으로 따라가, 한 영상·한 주제·한 채널의 반응인데 사용자가 "앞으로·모든 채널·공통"으로 넓히지 않았으면 범위를 적거나(채널 문서·topic.yaml 로) 층을 내림(스타일 기본값·실험 기록). 자동 층 추정이 틀린 '영구 원칙'(사실·법·권리·안전이 아닌 것)은 `manual/rule_tiers.yaml` 에 "Claude 판정 — 사용자 확인 필요"로 바로잡음. 에이전트를 나눠 돌려도 된다(읽기만 시키고, 고치기는 이 세션이).
   - **정기 작업 지시문:** 전체 점검 때 `list_triggers` 로 이 계정의 정기 작업 지시문을 읽어 저장소 규칙(시간표·형식·브랜치·공유 페이지 주소·절차)과 맞댄다. 장부에는 `file: "schedule:<작업 이름>"` 으로 적는다. 지시문 고치기(`update_trigger`)는 낡은 쪽이 분명할 때만, 바꾼 문장을 알림에 적는다.
   - **판정** (권위 순서: 날짜 있는 사용자 원문 > CHANGELOG 최신 버전 규칙 > manual 본문 > AGENTS > skills·prompts·styles·channels·topics > docs): 범위(채널·장면·형식)가 달라 둘 다 맞으면 모순 아님(필요하면 범위를 적어 줌). 낡은 쪽이 분명하면 **바로 고치고** 장부에 `status: resolved`. 둘 다 그럴듯하면 고치지 말고 `status: open` (→ 물어볼 것). 사용자가 답하면 `decision` 에 원문을 적고 `decided` → 낡은 쪽 고침 → `resolved`.
   - 폐지된 기준이 새로 생기면 `ytflow/stages/audit.py` 의 `RETIRED` 에 한 줄 더한다 (다음부터는 글자로 자동으로 잡힘).
   - 끝나면 `python -m ytflow manual-audit --checked` (전체 점검이었으면 `--checked --full`) — 장부의 기준 커밋·날짜가 지금으로 바뀐다.
3. **fix 항목만 고친다** (판단이 필요 없는 것):
   | 종류 | 고치는 법 |
   |---|---|
   | 폐지된 기준이 남음 (retired) | `why` 칸의 현재 기준대로 그 문장만 고쳐 쓴다 (예: 순서 예고 → 삭제, intro 장면 → 본론 장면, 8~10분 → 10분~). 사용자 원문 인용(`>`)은 고치지 않는다 |
   | 깨진 참조 (ref) | 같은 내용의 지금 절 번호·파일로 바꾼다. 같은 내용이 없으면 **고치지 말고** ask 로 남긴다 |
   | 코드 위치 바뀜 (coderef) | glossary 는 `code` 의 글자를 지금 코드에 맞게, intents 는 새 줄에 같은 판정을 옮기고 옛 줄은 지운다 (`manualgraph.save_annotation`) |
   | 주제 레포 오류 (topic) | 비슷한 이름의 장면·기법으로 고치되, 확실하지 않으면 ask |
   | 옛 그래프 (stale) | `python -m ytflow manual-graph` |
   | 모순 (contra, decided) | `decision` 대로 낡은 쪽을 고치고 장부 `status: resolved` |
   | 모순 점검 차례 (sweep) | 위 2-1 |
   고친 것마다 한 줄 요약을 모아 둔다.
3-1. **제안함** (`proposal` 항목, `proposals/manual/`): 다른 에이전트가 남긴 것. 영상 검토(review)·사용자 원문 피드백(feedback)은 그 명령으로 그대로 옮기고(원문 유지), 규칙을 바꾸자는 제안은 ask 로 사용자에게 묻는다. 반영한 제안 파일은 `status: done` 으로.
3-1. **모델 역할 점검** (2026-11-22 사용자: "모델이 새로 나오면 이도 재 설정하고"): 이 세션의 환경 정보(시스템 프롬프트의 최신 모델 목록)에 `config/models.yaml` 보다 새 모델(같은 계열의 더 높은 버전)이 보이면 ask 로 남긴다 — 바꿀지는 사용자. 사용자가 바꾸라고 하면 `models.yaml` 의 model·cli·checked 와 `.claude/agents/*.md` 의 model 을 함께 고친다 (manual/11 §1-1).
4. **ask 항목은 고치지 않는다** (모순 open·충돌·과적합·반영 대기·층 미정·어긋난 해석). 규칙의 뜻·층·MUST 여부는 사용자가 정한다 (manual/README §3-1). 같은 질문이 이미 며칠째 남아 있으면 알림에 '며칠째'만 적고 새로 길게 쓰지 않는다.
5. 마무리:
   - `python -m ytflow manual-audit --note "정기 검토" --fixed "고친 것 한 줄" --fixed "…"` — 다시 재서 해결 여부를 기록하고, 고친 것을 보고서·그래프('지난 검토에서 고친 것')에 남긴다.
   - `python -m ytflow manual-graph --artifact <스크래치>/manual-graph.html` → Artifact 도구로 **같은 공유 페이지**(`ytflow/stages/manualgraph.py` 의 `ARTIFACT_URL`)에 다시 올린다.
   - 바뀐 것이 있으면 커밋·푸시 (커밋 메시지: `정기 검토 YYYY-MM-DD: 고친 것 N · 물어볼 것 M`).
   - **main 반영**: 작업 브랜치에서 main 으로 PR 을 만들어 합친다 (사용자 허락 2026-11-15, docs/35). 충돌이 있으면 합치지 말고 보고.
   - **잠금 풀기**: `python -m ytflow manual-lock release` — 다음 세션이 바로 이 결과 위에서 고칠 수 있게. 기다리던 요청(`kind: request`)이 있으면 처리했거나 알림에 적는다.
6. 알림 (PushNotification 도구): `매뉴얼 검토 MM/DD — 고친 것 N · 물어볼 것 M · 열린 모순 K` + 물어볼 것 첫 1~2개 한 줄씩 + 공유 페이지 '한눈에 → 정기 검토'. 물어볼 것도 고친 것도 없으면 짧게 "깨끗함".

## 하지 않는 것
- 매뉴얼 버전 올리기(`manual-bump`), 규칙의 층·MUST 바꾸기, 사용자 원문(`>` 인용·reviews·feedback) 고치기, 영상 렌더·업로드.
- 판단이 애매한 fix 는 고치지 말고 ask 로 남기기 (한 번의 추측으로 규칙을 바꾸지 않는다).
