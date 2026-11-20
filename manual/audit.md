# 매뉴얼 정기 검토 — 2026-11-20T11:45 (매뉴얼 v70)

> 자동 생성 (`python -m ytflow manual-audit`, docs/34). **fix** = 판단 없이 고칠 수 있음 → 정기 검토가 고침 · **ask** = 사용자 판단 필요 → 질문으로 남김.

**고칠 것 1 · 물어볼 것 34 · 새로 생김 5 · 지난번 뒤 해결됨 4**

## 물어볼 것 (사용자 판단)

| 종류 | 위치 | 내용 | 왜 | 처음 본 날 |
|---|---|---|---|---|
| 과적합 후보 🆕 | manual/05-style-matching.md:7 | 자동 검사: 스타일 항목은 SHOULD(권고)·참고뿐입니다 (v34 사용자: "스타일 MUST 들은 전부 굳이 필요하지 않다"). MUST 는 원리를 분명히 어긴 경우만(시장 채널: 말로 숫자를 늘 | 실험 기록 층인데 금지·MUST 로 적힘 — 기본값 문장으로 바꿀지, 원칙·기준으로 확정할지 | 2026-11-20 |
| 과적합 후보 🆕 | manual/05-style-matching.md:56 | 장 표지 사진은 주제에 맞게 (주제와 무관한 기본 사진으로 때우지 않음, 같은 사진 두 번 없음): python -m ytflow archive commons "검색어" (PD·CC0·CC BY 만 | 실험 기록 층인데 금지·MUST 로 적힘 — 기본값 문장으로 바꿀지, 원칙·기준으로 확정할지 | 2026-11-20 |
| 과적합 후보 🆕 | manual/05-style-matching.md:142 | 고르는 요령 (예): 숫자 하나 → photofill · 연표·인과 지도 → tilt · 비유·인용 → dolly. 장식 효과(dust·leak)·scan 은 드물게(시장 채널은 끔, 09 §6). | 실험 기록 층인데 금지·MUST 로 적힘 — 기본값 문장으로 바꿀지, 원칙·기준으로 확정할지 | 2026-11-20 |
| 층 미정 피드백 | manual/feedback.yaml | 썸네일은 셋다 별로인거같아요 그리고 세번째 썸네일은 너무 싼티나요 저 빨간색이랑 초록색이 말이죠 | 이 말의 층이 정해지지 않음 (자동 추정: 작업 기준) — 영구 원칙·작업 기준·스타일 기본값·실험 기록 중 | 2026-11-20 |
| 층 미정 피드백 | manual/feedback.yaml | 앞으로 그럼 클라우드에서 제 계정으로 로그인하던지 클라우드가 아니라 다운로드가 필요할 때만 뭐 따로 다운로드 하던지 할 수 있도록 해주세요 | 이 말의 층이 정해지지 않음 (자동 추정: 작업 기준) — 영구 원칙·작업 기준·스타일 기본값·실험 기록 중 | 2026-11-20 |
| 층 미정 피드백 | manual/feedback.yaml | 아 우선 피클에게 요청한거 좋아요 | 이 말의 층이 정해지지 않음 (자동 추정: 작업 기준) — 영구 원칙·작업 기준·스타일 기본값·실험 기록 중 | 2026-11-20 |
| 층 미정 피드백 | manual/feedback.yaml | 앞으로브리핑은 매번 심층으로할거고 오늘같은 일 없이 가능하도록 세팅해줘 원본영상 허가할테니까 일단 그냥 진행해줘 | 이 말의 층이 정해지지 않음 (자동 추정: 작업 기준) — 영구 원칙·작업 기준·스타일 기본값·실험 기록 중 | 2026-11-20 |
| 층 미정 피드백 | manual/feedback.yaml | 구성 요소별로 제작 메뉴얼같은거도 따로 작성한거야? 왜냐면 그게 아니면 나중에 재구현 불가능할거아니야 또 예시사진으로는 사실 전부 보여주지 못하고 약간 괴리?가 생기니까 | 이 말의 층이 정해지지 않음 (자동 추정: 작업 기준) — 영구 원칙·작업 기준·스타일 기본값·실험 기록 중 | 2026-11-20 |
| 층 미정 피드백 | manual/feedback.yaml | 영상 구성요소 · 스타일 목록에 이를 올려주세요 (설명 무대) | 이 말의 층이 정해지지 않음 (자동 추정: 스타일 기본값) — 영구 원칙·작업 기준·스타일 기본값·실험 기록 중 | 2026-11-20 |
| 층 미정 피드백 | manual/feedback.yaml | 보면 아직 저 배경 디테일 부터 시작해서 전체적인 디테일들이 많이 부족해보여요 / 솔직히 말해서 퀄리티가 더 낮다 이런느낌이 듭니다 (설명 무대 1차 시험작 → 2차에서 실사 구겨진 종이·굵은 고딕 | 이 말의 층이 정해지지 않음 (자동 추정: 작업 기준) — 영구 원칙·작업 기준·스타일 기본값·실험 기록 중 | 2026-11-20 |
| 층 미정 피드백 | manual/feedback.yaml | 쉽게 설명해야 하는 부분이다 상황설명이 필요하다 = 모션그래픽 을 주로 사용합니다. (설명 무대를 주식 채널 상황 설명 기본으로 — manual/12 §0-1, situations explain·e | 이 말의 층이 정해지지 않음 (자동 추정: 작업 기준) — 영구 원칙·작업 기준·스타일 기본값·실험 기록 중 | 2026-11-20 |
| 용도 미정 기능 | manual/usage.yaml | 그래픽 팩: 구겨진 종이 (설명 무대) (crumpled-paper) | 언제 쓰나·쓰지 않나·대신이 정해지지 않음 — usage.yaml (스타일은 레시피 when·fits, 기법은 techniques.yaml) 에 초안을 써서 확인받기 | 2026-11-20 |
| 용도 미정 기능 | manual/usage.yaml | 그래픽 팩: 어두운 무대 (설명 무대) (dark-stage) | 언제 쓰나·쓰지 않나·대신이 정해지지 않음 — usage.yaml (스타일은 레시피 when·fits, 기법은 techniques.yaml) 에 초안을 써서 확인받기 | 2026-11-20 |
| 제안함 | proposals/manual/20261119-230847-video-20261117-three.md | [review] 본편 v7 최종 통과. 사용자 원문 “합격입니다. 커밋해주세요” | video-20261117-three 의 제안 — 잠금을 잡은 쪽이 반영(feedback·review·매뉴얼 수정) 뒤 제안 파일의 status 를 done 으로 | 2026-11-20 |
| 제안함 | proposals/manual/20261120-035314-op-infographic-direction.md | [feedback] 제가 강조하려는건 인포그래픽을 이용한 연출과 애니메이션효과에요 | codex/hangeop-infographic-direction 의 제안 — 잠금을 잡은 쪽이 반영(feedback·review·매뉴얼 수정) 뒤 제안 파일의 status 를 done 으로 | 2026-11-20 |
| 제안함 | proposals/manual/20261120-083425-ectionate-faraday-8bp5bx.md | [feedback] 배경음은 그냥 빼줘 여기는 너무 연출이 허접해 다른거로 해줘 | claude/affectionate-faraday-8bp5bx 의 제안 — 잠금을 잡은 쪽이 반영(feedback·review·매뉴얼 수정) 뒤 제안 파일의 status 를 done 으로 | 2026-11-20 |
| 제안함 🆕 | proposals/manual/20261120-110411-ccr-6309f6dc-9b0iae.md | [request] 과적합 지침 정리 (사용자: 규칙이 너무 많아지는 걸 막고 정말 중요한 것만) — ccr-6309f6dc-9b0iae | ccr-6309f6dc-9b0iae 의 제안 — 잠금을 잡은 쪽이 반영(feedback·review·매뉴얼 수정) 뒤 제안 파일의 status 를 done 으로 | 2026-11-20 |
| 모순 | manual/06 G8 MUST·README §3-7·11 S9·cli upload 기본 | c-20261120-24: manual/06 G8 MUST·README §3-7·11 S9·cli upload 기본 ↔ AGENTS.md 저장 규칙·docs/09 §0 (2026-11-16 사용자) | 어느 쪽이 맞는지 사용자 판단 — 답을 decision 에 적고 status: decided | 2026-11-20 |
| 모순 | channels/ch-issues-daily/channel.yaml 제목·설명, 08 §0-2 | c-20261120-25: channels/ch-issues-daily/channel.yaml 제목·설명, 08 §0-2 ↔ 같은 파일 target_minutes 10, README §2-4 — 매 | 어느 쪽이 맞는지 사용자 판단 — 답을 decision 에 적고 status: decided | 2026-11-20 |
| 모순 | manual/09 §1 시간표 | c-20261120-26: manual/09 §1 시간표 ↔ manual/09 §2 (v63) — 심층 기본과 90분 제작 시간 | 어느 쪽이 맞는지 사용자 판단 — 답을 decision 에 적고 status: decided | 2026-11-20 |
| 모순 | manual/09 §2 표 | c-20261120-27: manual/09 §2 표 ↔ 같은 표 — 토요일 아침 | 어느 쪽이 맞는지 사용자 판단 — 답을 decision 에 적고 status: decided | 2026-11-20 |
| 모순 | channels/brands.yaml identity·05 §0-7 | c-20261120-28: channels/brands.yaml identity·05 §0-7 ↔ 04 §0-8 (v57·v60) — 호기심 채널 정체성 | 어느 쪽이 맞는지 사용자 판단 — 답을 decision 에 적고 status: decided | 2026-11-20 |
| 모순 | skills/video-sources §3 | c-20261120-29: skills/video-sources §3 ↔ docs/50 §0·AGENTS 소스 규칙 — PC 쿠키 사용과 우회 금지 | 어느 쪽이 맞는지 사용자 판단 — 답을 decision 에 적고 status: decided | 2026-11-20 |
| 모순 | data/style_profile.json (writing.py 가 모든 make 대본 프롬프트에 넣음) | c-20261120-30: data/style_profile.json (writing.py 가 모든 make 대본 프롬프트에 넣음) ↔ manual/README §2-1·§2-4, 12 §0 — m | 어느 쪽이 맞는지 사용자 판단 — 답을 decision 에 적고 status: decided | 2026-11-20 |
| 모순 | manual/04 §0-6 순서 | c-20261120-31: manual/04 §0-6 순서 ↔ manual/11 단계표·04 v55 — 호기심 intent.md 순서 | 어느 쪽이 맞는지 사용자 판단 — 답을 decision 에 적고 status: decided | 2026-11-20 |
| 모순 | 정기 작업 "뉴스레터 소재 수집" 05:40 | c-20261120-32: 정기 작업 "뉴스레터 소재 수집" 05:40 ↔ docs/36 §5-1 — 뉴스레터 정기 작업 역할 | 어느 쪽이 맞는지 사용자 판단 — 답을 decision 에 적고 status: decided | 2026-11-20 |
| 모순 | channels/ch-ai-shorts/README.md | c-20261120-33: channels/ch-ai-shorts/README.md ↔ channels/ch-ai-shorts/channel.yaml — AI 쇼츠 기본 스타일 | 어느 쪽이 맞는지 사용자 판단 — 답을 decision 에 적고 status: decided | 2026-11-20 |
| 모순 | README §2-2·checklist.py G4 MUST(모든 롱폼) | c-20261120-46: README §2-2·checklist.py G4 MUST(모든 롱폼) ↔ reviews v16 한 편(20261112-bg-trials) 장 표지 문구, 11 §3-2( | 어느 쪽이 맞는지 사용자 판단 — 답을 decision 에 적고 status: decided | 2026-11-20 |
| 모순 | 05 §0-5 | c-20261120-47: 05 §0-5 ↔ v11 한 편 기각 "소리 자체가 싫음" — 저음 타격음 코드에서 삭제 | 어느 쪽이 맞는지 사용자 판단 — 답을 decision 에 적고 status: decided | 2026-11-20 |
| 모순 | checklist.py G3 MUST | c-20261120-48: checklist.py G3 MUST ↔ 09 §3-0 2026-11-14 "주식 … 기본적으로 확인" — SAVE 확인 MUST 범위 | 어느 쪽이 맞는지 사용자 판단 — 답을 decision 에 적고 status: decided | 2026-11-20 |
| 모순 | 09 §5-1 | c-20261120-49: 09 §5-1 ↔ 11/20 개정판 한 편 편집 지시 — 시장 장마다 순서·도입 문구 | 어느 쪽이 맞는지 사용자 판단 — 답을 decision 에 적고 status: decided | 2026-11-20 |
| 모순 | AGENTS·05 §0-8 | c-20261120-50: AGENTS·05 §0-8 ↔ fb:18·19 (스타일 층) — 그림판·도형 느낌 탈락 | 어느 쪽이 맞는지 사용자 판단 — 답을 decision 에 적고 status: decided | 2026-11-20 |
| 모순 | prompts/script.md:93 | c-20261120-51: prompts/script.md:93 ↔ README §2-5 — 공통 대본 프롬프트의 전면 금지 | 어느 쪽이 맞는지 사용자 판단 — 답을 decision 에 적고 status: decided | 2026-11-20 |
| 모순 | 06 G5·05 §0-0 | c-20261120-52: 06 G5·05 §0-0 ↔ checklist.py — 강조 아껴 쓰기 단계 | 어느 쪽이 맞는지 사용자 판단 — 답을 decision 에 적고 status: decided | 2026-11-20 |

## 고칠 것 (판단 불필요)

| 종류 | 위치 | 내용 | 왜 | 처음 본 날 |
|---|---|---|---|---|
| 모순 점검 차례 🆕 | manual/contradictions.yaml | 바뀐 지침 3개 모순 점검: manual/06-checklist.md, manual/09-market-daily.md, styles/explain-stage/STYLE.md | 바뀐 줄이 다른 지침·정기 작업 지시문과 반대인지 확인 → 장부에 적고 manual-audit --checked | 2026-11-20 |

## 지난 검토 뒤 해결됨

- 과적합 후보: 고르는 요령: 숫자 하나 → photofill(그 숫자의 장소 사진으로 채움) · 연표·인과 지도 → tilt · 비유·인용 → dolly. 장식 효과(dust·leak)는 내용이
- 과적합 후보: SHOULD | v15 장 표지 사진은 주제에 맞게: 같은 사진을 다시 표지로 쓰지 않고, 주제와 무관한 기본 사진으로 때우지 않음(한 출처로 표지를 모두 채우지 않음), 출처(c
- 과적합 후보: 늘릴 때는 같은 말을 반복하지 않고 그 채널의 뼈대를 채운다 — 호기심은 §2-3(여는 장면의 일화 하나 더 · 당사자의 회고 · 전환점의 장면 · 원리의 생활 속 예 · 퍼져 나
- 옛 그래프: 매뉴얼 그래프가 옛것

## 검토 기록

| 날짜 | 고칠 것 | 물어볼 것 | 새로 | 해결 | 메모 |
|---|---|---|---|---|---|
| 2026-11-19T13:53 | 0 | 1 | 0 | 0 |  |
| 2026-11-19T13:54 | 0 | 0 | 0 | 1 | 사용자 정정 반영 |
| 2026-11-20T10:11 | 20 | 13 | 33 | 0 |  |
| 2026-11-20T10:12 | 0 | 13 | 0 | 20 |  |
| 2026-11-20T10:12 | 0 | 13 | 0 | 0 |  |
| 2026-11-20T10:15 | 6 | 13 | 6 | 0 |  |
| 2026-11-20T10:16 | 2 | 13 | 0 | 4 |  |
| 2026-11-20T10:21 | 2 | 13 | 0 | 0 |  |
| 2026-11-20T10:25 | 1 | 24 | 11 | 1 | 모순·낡은 문장 전체 점검 (사용자 요청) |
| 2026-11-20T10:25 | 0 | 23 | 0 | 2 | 모순·낡은 문장 전체 점검 (사용자 요청) |
| 2026-11-20T10:26 | 1 | 23 | 1 | 0 | 점검 기준 커밋 갱신 |
| 2026-11-20T10:38 | 0 | 33 | 10 | 1 | 범위 점검(피드백·지침 분리) |
| 2026-11-20T10:38 | 1 | 33 | 1 | 0 | 범위 점검 기준 커밋 |
| 2026-11-20T11:45 | 1 | 34 | 5 | 4 |  |
