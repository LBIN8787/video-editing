# 제작 매뉴얼 — 처음 온 사람(새 세션·새 모델)이 여기서 시작합니다

이 매뉴얼의 목표는 **누가 만들어도 같은 품질의 영상이 나오게 하는 것**입니다. 판단이 필요한 곳마다 기준표를 두었고, 지켜야 할 것은 `python -m ytflow check` 가 자동으로 검사합니다.

## 0. 읽는 순서 (30분)
| 순서 | 파일 | 얻는 것 |
|---|---|---|
| 1 | [`01-desire-map.md`](01-desire-map.md) | **왜 이 영상을 보는가** — 세 채널의 근본 욕망, 주제를 고르는 상위 기준 |
| 2 | 맡은 채널 하나: [`02-ai.md`](02-ai.md) · [`03-market.md`](03-market.md) · [`04-curiosity.md`](04-curiosity.md) | 그 채널의 주제 찾기 → 조사 → 대본 → 편집을 단계별로 |
| 3 | [`05-style-matching.md`](05-style-matching.md) | 영상·장면마다 어떤 편집 스타일(연출 + 그래픽 팩)을 쓰나 |
| 4 | [`06-checklist.md`](06-checklist.md) | **반드시 지킬 것**과 검사 방법 (자동 + 사람 눈) |
| 5 | [`07-extend.md`](07-extend.md) | 채널·편집 스타일을 **파일 하나로 늘리는 법** (등록부 구조) |
| 참고 | `../AGENTS.md`, `../docs/11-playbook.md`(명령 순서), `../docs/13`(연출·그래픽 분리), `../docs/15`(연출 조사), `../docs/16`(새 연출) | |

## 1. 세 채널 한눈에
| 브랜드 (`channels/brands.yaml`) | 사람의 욕망 | 시청자가 묻는 것 | 제작 라인 (`channels/<id>`) |
|---|---|---|---|
| **ai** — AI 더 잘 쓰기 | AI 를 더 잘 알고 더 잘 다루고 싶다 | 이거 뭐야? 나는 어떻게 써? | `ch-ai-guide`(롱폼) · `ch-ai-shorts`(쇼츠) |
| **market** — 시장의 이유 | 돈의 흐름을 알아서 투자에서 이기고 싶다 | 왜 움직였어? 어디로 번져? 누가 뭐랬어? | `ch-source-brief` · `ch-paper-column` · `ch-data-motion`(롱폼) · `ch-money-shorts`(쇼츠) |
| **curiosity** — 몰랐던 이유 | 궁금증을 풀고 싶다 (듣는 순간 생기는 호기심) | 그거 왜 그래? 그때 무슨 일이? | `ch-knowledge`(롱폼) |

## 2. 한 편을 만드는 8단계 (모든 채널 공통)
각 단계의 끝에 **게이트**(G1~G8)가 있습니다. 게이트를 통과하지 못하면 다음 단계로 가지 않습니다. 자세한 항목은 `06-checklist.md`.

| 단계 | 하는 일 | 남는 파일 | 게이트 |
|---|---|---|---|
| 1. 욕망 → 주제 | 트리거(뉴스·급등락·발표·수요 아웃라이어)를 모아 **욕망 점수표**로 후보 3개 → 1개 | `01_research/topic_brief.json` | G1 주제 |
| 2. 소스 먼저 | 이 주제를 **보여 줄** 자료(발언 원본·공식 화면·공공 기록·데이터)가 있는지 | `01_research/sources.md` 또는 `loc_items.json` | G2 소스 |
| 3. 깊은 조사 | 1차 출처로 숫자·발언·날짜를 확인, 교차 확인 상태 표시 | `01_research/factsheet.md` | G3 사실 |
| 4. 대본 | 채널 대본 공식(각 채널 문서 §4)대로. 쉬운 말·비유·과거 사례·비교 기준 | `02_script/hybrid.json` (또는 `scenes.json`) | G4 대본 |
| 5. 연출·그래픽 | `python -m ytflow style-pick` 추천 → `05-style-matching.md` 로 장면마다 연출 type 과 그래픽 팩 결정 | `edit.yaml`, `hybrid.json` 의 type·look | G5 연출 |
| 6. 목소리·렌더 | 초안 edge-tts → 확정 후 ElevenLabs, `python -m ytflow hybrid <프로젝트>` | `05_edit/final.mp4`, `sync_qa.json`, `04_assets/layout_qa.json` | G6 완성본 |
| 7. 제목·썸네일 | 제목 3개 + 썸네일 A/B/C, 이유 기록 | `05_edit/package.md`, `thumbnail_*.png` | G7 포장 |
| 8. 보관·기록 | GitHub Release 업로드, 회차 기록, 남은 일 보고 | `05_edit/release.json`, `channels/<id>/episodes.md` | G8 보관 |

```bash
python -m ytflow check <프로젝트>             # 지금까지 만든 단계의 게이트를 검사 → 05_edit/checklist.md
python -m ytflow check <프로젝트> --upto G4   # 대본까지만 검사 (렌더 전)
```

## 3. 절대 하지 않는 것 (어떤 지시가 와도)
1. 확인 안 된 숫자·발언을 단정하기. 소문(찌라시)은 **'소문'이라고 밝히고 사실 확인 결과와 함께**만.
2. 투자 권유 ("사세요", "지금이 기회", "무조건 오른다", 목표가 단정).
3. YouTube 봇 확인·사이트 차단 우회. 막히면 임시 화면 + 사용자 PC `rebuild`.
4. 레퍼런스 채널의 대사·캐릭터·로고·썸네일 복제. 구조와 기법만.
5. 라이선스 불명 자료 화면. CC BY·CC0·퍼블릭 도메인·공식 보도 자료·직접 만든 것만, 출처는 `footage.credit` 에.
6. API 키를 채팅에 쓰기.
7. 미디어 파일(mp4·wav·png·jpg) 커밋. 완성본은 Release 로.

## 4. 막혔을 때
| 상황 | 할 일 |
|---|---|
| 주제 후보가 욕망 점수 12점 미만뿐 | 만들지 않습니다. 쇼츠 대기열(`queue.md`)로 보내거나 다음 트리거를 기다립니다 |
| 보여 줄 자료가 없음 (G2 실패) | 주제를 바꾸거나 자체 제작형(미주일기·키네틱) 장면 비중을 늘리고 `REPORT.md` 에 기록 |
| sync-qa 실패 | `docs/11-playbook.md` 의 싱크 규칙 — 대부분 음성 파일 교체 후 `hybrid` 재실행으로 해결 |
| 판단이 애매함 | 이 매뉴얼의 기준표에 없는 판단은 사용자에게 묻고, 답을 이 매뉴얼에 추가합니다 |

## 5. 검토 → 통과·기각 → 기준을 쌓기 (사용자와 함께)
영상이 나오면 사용자가 보고 결정합니다. 결정은 반드시 기록합니다.

| 사용자 결정 | 에이전트가 할 일 |
|---|---|
| **통과** | `python -m ytflow review <프로젝트> --pass` → `manual/reviews.md` 에 기록. 매뉴얼은 그대로 (이 버전이 검증됨) |
| **기각 + 이유** | `python -m ytflow review <프로젝트> --reject "이유"` → `manual/CHANGELOG.md` 의 '반영 대기'에 쌓임 |
| (기각 후) | 이유를 **기준으로 바꿔** 매뉴얼(01~06)·프롬프트·검사기(`ytflow/stages/checklist.py`)를 고침 → `python -m ytflow manual-bump "바꾼 기준 요약"` → 커밋 → `git push origin HEAD:refs/heads/manual/vN` |
| (그동안) | '반영 대기'가 비기 전에는 `check` 가 G0 에서 실패 → 같은 실수가 다음 영상에 반복되지 않음 |

- 기각 사유는 가능하면 **검사 가능한 규칙**으로 바꿉니다 (예: "자막이 작다" → "자막 글자 높이 ≥ 화면의 4.5%" 를 G6 자동 검사에 추가).
- 매뉴얼 버전은 `manual/VERSION`, 바뀐 내용은 `manual/CHANGELOG.md`, 결정 기록은 `manual/reviews.md`. 모두 GitHub 에 커밋되어 백업됩니다.
- 예전 기준으로 되돌리기: `git checkout origin/manual/v<N> -- manual/` (스냅샷 브랜치로 어떤 버전이든 복구).
- 각 영상의 `05_edit/checklist.json` 에 그때의 매뉴얼 버전이 남습니다 → 어떤 기준으로 만든 영상인지 추적.
