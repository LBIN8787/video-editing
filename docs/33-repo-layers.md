# 33. 레포 구조 — 메인 매뉴얼 → 주제 레포 → 상황 → 영상 (2026-11-15)

> 사용자: "이 그래프는 주식 영상을 토대로 만든 것이 아니라 편집에 대한 매뉴얼이자 그래프 — 메인 레포 같은 개념. 이를 토대로 주식이면 주식, 호기심이면 호기심, 주제와 연출법에 맞는 상황으로 편집을 채워 나갔으면. 메인 레포 > 주제별 레포처럼 움직이게." (참고 영상: 민둥이 「맷 포콕이 공개한, AI 하나로 모든 프로젝트를 관리하는 방법」)

## 참고한 생각
맷 포콕(Matt Pocock)은 자기 `.claude/skills` 를 공용 저장소(mattpocock/skills, MIT)로 공개하고, 프로젝트마다 셋업 스킬을 **한 번** 돌려 그 저장소에 맞는 `CLAUDE.md`(이슈 트래커·라벨 같은 프로젝트별 설정)를 만들게 했다. 공용 규칙은 한 곳에서 고치고, 프로젝트는 물려받아 다른 것만 적는다. 우리 편집에 옮기면:

| 맷 포콕 방식 | 우리 편집 |
|---|---|
| 공용 스킬 저장소 | **메인 레포** = `manual/`(원칙·작업 기준·작업 절차) + `manual/situations.yaml`(공통 상황) + `styles/techniques.yaml`(연출 기법) + `manual/glossary.yaml`(용어) |
| 프로젝트 종류별 설정 | **주제 레포** = `topics/<brand>/topic.yaml` — 주식·호기심·AI·시사. `inherits: main` + 스타일 기본값 덮어쓰기 + 상황 더하기·바꾸기·빼기 + 기본으로 안 쓰는 기법 |
| 프로젝트마다 셋업 → CLAUDE.md | **영상 한 편** = `python -m ytflow edit-plan <영상>` → `02_script/EDIT_CONTEXT.md`(이 영상에 적용되는 규칙 묶음, 에이전트가 편집 전에 먼저 읽음) + `edit_plan.json` |

## 상황이란
대본의 한 박자(문장)가 **하는 일** — 장면을 연다, 누가 말했다, 숫자가 움직였다, 원인 → 결과, 말과 행동을 맞댄다 … (`manual/05-style-matching.md` §2 표를 기계가 읽게 옮긴 것). 상황마다 1순위 → 2순위 장면 종류, 함께 쓸 연출 기법, 피할 것, 그 이유(사용자 뜻·매뉴얼 근거), 알아보는 말(signals)이 있다. 주제 레포는 그 주제에만 있는 상황을 더한다:
- **주식**: 말과 행동 맞대기(v26) · 시장을 흔든 사건과 파급(v28) · 실적·가이던스 · 어닝콜 발언 · 다음 주 일정(v29). 기본값 zoom off(v31) · camera calm(v30) · bgm none · motion_beats. 기본으로 안 쓰는 기법: 확대 전환·풀백·사진 깊이·휩 팬.
- **호기심**: 주인공이 무언가를 한다(v22) · 답을 밝히는 순간 · 규모를 느낀다. 장면을 연다·바뀌었다는 stage·story 로 바꿈. 기본값 backbone broll-motion(실사 B-roll + 모션그래픽, v60) · 삽화·stage·story 는 자료가 없는 구간만 · camera fixed · 대본 검토(v23).
- **AI**: 새 도구 소개 · 쓰기 전과 후. 화면의 한 곳은 실제 화면 위 표시.
- **시사**: 양쪽 입장(같은 틀, 영구 원칙) · 아직 모르는 것 · 우리에게 무슨 뜻.

## 영상에 채우기
```bash
python -m ytflow topics                    # 주제 레포마다 물려받고·바꾸고·더한 상황
python -m ytflow edit-plan <프로젝트>       # 박자마다 상황 → 추천 장면·기법, 지금 장면 종류와 맞는지(⚠ = 다시 볼 곳)
```
- 상황 찾기는 낱말 신호라 **추천**이지 정답이 아님. ⚠ 는 '틀렸다'가 아니라 '다시 볼 곳'.
- 기법 상태가 '후보'면 아직 렌더러에 없음(docs/32) — 계획에 그렇게 표시된다.
- `check` G5 SHOULD: `02_script/EDIT_CONTEXT.md` 가 있는지.

## 고치는 곳 (메인을 고치면 모든 주제가 따라감)
| 바꾸고 싶은 것 | 고칠 파일 |
|---|---|
| 모든 영상의 원칙·기준 | `manual/*.md` (버전 올림) |
| 공통 상황의 장면·기법 | `manual/situations.yaml` |
| 한 주제에서만 다르게 | `topics/<brand>/topic.yaml` 의 `situations.override` |
| 그 주제에만 있는 상황 | `situations.add` |
| 그 주제에선 안 쓰는 기법 | `avoid_techniques` |
| 새 주제(채널) | `topics/<새 brand>/topic.yaml` (inherits: main) + 채널 `channel.yaml` 의 brand |

## 그래프
매뉴얼 그래프 첫 탭 **레포 구조**: 메인 → 주제 카드 4개 → 고른 주제의 기본값·안 쓰는 기법·상황표(초록 더함·주황 바꿈·회색 메인) → 그 주제의 영상(상황 찾음 %·장면 맞음 %). 상황을 누르면 실제 영상에서 나온 문장, 영상을 누르면 장면별 계획.

## 지금 측정값 (2026-11-15, 영상 29편)
주식 10편: 상황 찾음 80~96%, 지금 장면 종류가 추천과 맞음 33~50%. 맞지 않는 곳이 많은 상황: '말과 행동 맞대기'(22%, 지금은 quote·chapter 로 처리), '화면의 한 곳을 가리킨다'(0%). → 다음 영상에서 볼 곳.

## 출처
- 영상: 민둥이 | 쉽게 배우는 AI, 「맷 포콕이 공개한, AI 하나로 모든 프로젝트를 관리하는 방법」 (YouTube oEmbed 로 제목만 확인 — 본문은 봇 확인 우회 없이 받지 않음)
- [mattpocock/skills 소개](https://mer.vin/news/mattpocock-skills-the-skill-pack-topping-github-trending/), [프로젝트마다 셋업](https://www.besthub.dev/articles/how-to-build-a-real-ai-coding-environment-with-matt-pocock-s-skills-66aeee935713), [공용 루트 저장소 + 프로젝트 하위 모듈 방식](https://dev.to/jurooravec/one-ai-config-to-rule-all-repos-2n1o)
