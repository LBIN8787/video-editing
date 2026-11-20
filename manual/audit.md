# 매뉴얼 정기 검토 — 2026-11-20T23:13 (매뉴얼 v73)

> 자동 생성 (`python -m ytflow manual-audit`, docs/34). **fix** = 판단 없이 고칠 수 있음 → 정기 검토가 고침 · **ask** = 사용자 판단 필요 → 질문으로 남김.

**고칠 것 1 · 물어볼 것 36 · 새로 생김 1 · 지난번 뒤 해결됨 5**

## 물어볼 것 (사용자 판단)

| 종류 | 위치 | 내용 | 왜 | 처음 본 날 |
|---|---|---|---|---|
| 과적합 후보 | manual/04-curiosity.md:141 | 모션그래픽이 넘치면 — 글자가 아래 자막과 같은 문장을 반복하거나(unslop 기각), 글씨·도형만 이어져 지루해진다(사우디 v8 기각). 말이 설명하는 관계를 움직임으로 보여 줄 때만 쓰고, 글자 | 실험 기록 층인데 금지·MUST 로 적힘 — 기본값 문장으로 바꿀지, 원칙·기준으로 확정할지 | 2026-11-20 |
| 과적합 후보 | manual/05-style-matching.md:7 | 자동 검사: 스타일 항목은 SHOULD(권고)·참고뿐입니다 (v34 사용자: "스타일 MUST 들은 전부 굳이 필요하지 않다"). MUST 는 원리를 분명히 어긴 경우만(시장 채널: 말로 숫자를 늘 | 실험 기록 층인데 금지·MUST 로 적힘 — 기본값 문장으로 바꿀지, 원칙·기준으로 확정할지 | 2026-11-20 |
| 과적합 후보 | manual/05-style-matching.md:56 | 장 표지 사진은 주제에 맞게 (주제와 무관한 기본 사진으로 때우지 않음, 같은 사진 두 번 없음): python -m ytflow archive commons "검색어" (PD·CC0·CC BY 만 | 실험 기록 층인데 금지·MUST 로 적힘 — 기본값 문장으로 바꿀지, 원칙·기준으로 확정할지 | 2026-11-20 |
| 과적합 후보 | manual/05-style-matching.md:142 | 고르는 요령 (예): 숫자 하나 → photofill · 연표·인과 지도 → tilt · 비유·인용 → dolly. 장식 효과(dust·leak)·scan 은 드물게(시장 채널은 끔, 09 §6). | 실험 기록 층인데 금지·MUST 로 적힘 — 기본값 문장으로 바꿀지, 원칙·기준으로 확정할지 | 2026-11-20 |
| 과적합 후보 | manual/12-visual-storytelling.md:15 | 기록을 바탕으로 다시 그린 장면은 '재구성'이라고 화면에 표시합니다(§1). 실제 사건 당사자의 얼굴은 그리지 않고, 얼굴을 알아볼 수 있는 실제 인물 사진·영상을 질환·중독·범죄·우울 같은 부정적 | 실험 기록 층인데 금지·MUST 로 적힘 — 기본값 문장으로 바꿀지, 원칙·기준으로 확정할지 | 2026-11-20 |
| 과적합 후보 | manual/06-checklist.md:73 | MUST **화면 글자 겹침 없음** (`05_edit/overlap_qa.json`, 렌더 끝에 자동 — 렌더된 장면을 박자 끝마다 멈춰 실제 글자 상자로 잼): 글자끼리 · 카드·그림에 가려짐  | 실험 기록 층인데 MUST 검사 — 권고로 내릴지 | 2026-11-20 |
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
| 제안함 | proposals\manual\20261119-230847-video-20261117-three.md | [review] 본편 v7 최종 통과. 사용자 원문 “합격입니다. 커밋해주세요” | video-20261117-three 의 제안 — 잠금을 잡은 쪽이 반영(feedback·review·매뉴얼 수정) 뒤 제안 파일의 status 를 done 으로 | 2026-11-20 |
| 제안함 | proposals\manual\20261120-035314-op-infographic-direction.md | [feedback] 제가 강조하려는건 인포그래픽을 이용한 연출과 애니메이션효과에요 | codex/hangeop-infographic-direction 의 제안 — 잠금을 잡은 쪽이 반영(feedback·review·매뉴얼 수정) 뒤 제안 파일의 status 를 done 으로 | 2026-11-20 |
| 제안함 | proposals\manual\20261120-083425-ectionate-faraday-8bp5bx.md | [feedback] 배경음은 그냥 빼줘 여기는 너무 연출이 허접해 다른거로 해줘 | claude/affectionate-faraday-8bp5bx 의 제안 — 잠금을 잡은 쪽이 반영(feedback·review·매뉴얼 수정) 뒤 제안 파일의 status 를 done 으로 | 2026-11-20 |
| 제안함 | proposals\manual\20261120-092042-ectionate-faraday-8bp5bx.md | [feedback] 문제제기를 하였다면 이 문제에 대한 해결방법까지 자연스레 이어져야 한다고 생각하거든 사람들이 호기심을 느끼는 포인트는 왜 그런지 그리고 자연스럽게 어떻게 해야지 이를 극복 가능한 | claude/affectionate-faraday-8bp5bx 의 제안 — 잠금을 잡은 쪽이 반영(feedback·review·매뉴얼 수정) 뒤 제안 파일의 status 를 done 으로 | 2026-11-20 |
| 제안함 | proposals\manual\20261120-092045-ectionate-faraday-8bp5bx.md | [request] 호기심 04 §0-6·§4: 문제제기 → 왜 → 어떻게 극복(원인마다 행동) → 첫 장면에서 해 보기로 이어지는 대본 (사용자 2026-11-20, proposals 참고) | claude/affectionate-faraday-8bp5bx 의 제안 — 잠금을 잡은 쪽이 반영(feedback·review·매뉴얼 수정) 뒤 제안 파일의 status 를 done 으로 | 2026-11-20 |
| 제안함 | proposals\manual\20261120-092108-ectionate-faraday-8bp5bx.md | [feedback] 그니까 단순히 심리나 이런 주제들은 이걸 듣고 얻어가는거 아 이래야 겠구나 이런 느낌을 줄 수 있도록 대본 구성해줘 | claude/affectionate-faraday-8bp5bx 의 제안 — 잠금을 잡은 쪽이 반영(feedback·review·매뉴얼 수정) 뒤 제안 파일의 status 를 done 으로 | 2026-11-20 |
| 제안함 | proposals\manual\20261120-092154-ectionate-faraday-8bp5bx.md | [feedback] 그리고 호기심채널은 말했다싶이 유행 트렌드 이걸 기반으로 해야하니까 추가로 요즘 유행하는 AI같은 주제들로 영상을 뽑는거도 괜찮아보이고 | claude/affectionate-faraday-8bp5bx 의 제안 — 잠금을 잡은 쪽이 반영(feedback·review·매뉴얼 수정) 뒤 제안 파일의 status 를 done 으로 | 2026-11-20 |
| 제안함 | proposals\manual\20261120-092156-ectionate-faraday-8bp5bx.md | [request] 호기심 04 범위: 유행하는 AI 주제도 소재로(사람의 마음·행동 쪽, AI 채널은 사용법) — 사용자 2026-11-20, proposals 참고 | claude/affectionate-faraday-8bp5bx 의 제안 — 잠금을 잡은 쪽이 반영(feedback·review·매뉴얼 수정) 뒤 제안 파일의 status 를 done 으로 | 2026-11-20 |
| 제안함 | proposals\manual\20261120-092211-ectionate-faraday-8bp5bx.md | [feedback] AI로 인한 뭐 여러 사회적 문제나 사람들의 걱정거리 심리 트렌드 이런걸 세부적으로 파고 들 수도 있는거니까 | claude/affectionate-faraday-8bp5bx 의 제안 — 잠금을 잡은 쪽이 반영(feedback·review·매뉴얼 수정) 뒤 제안 파일의 status 를 done 으로 | 2026-11-20 |
| 제안함 | proposals\manual\20261120-101812-ectionate-faraday-8bp5bx.md | [feedback] 여기서 너무 뜬금없이 바로 이야기가 넘어가요 실험에 대해서 알려주고 말해주는게 좋을거같고 영상 길이가 짧은데 일부만 잠깐 만든거죠? | claude/affectionate-faraday-8bp5bx 의 제안 — 잠금을 잡은 쪽이 반영(feedback·review·매뉴얼 수정) 뒤 제안 파일의 status 를 done 으로 | 2026-11-20 |
| 제안함 | proposals\manual\20261120-135059-ectionate-faraday-8bp5bx.md | [feedback] 그리고 지금 대본이 너무 학습쪽으로 가는 것 같아요 학습이 아니라 이야기를 들려준다는 느낌으로 대본 구성해주세요. 영상 길이도 학습쪽으로 너무 긴거같아요 또한 연출도 인물만 사용 | claude/affectionate-faraday-8bp5bx 의 제안 — 잠금을 잡은 쪽이 반영(feedback·review·매뉴얼 수정) 뒤 제안 파일의 status 를 done 으로 | 2026-11-20 |
| 제안함 🆕 | proposals\manual\20261120-140056-ectionate-faraday-8bp5bx.md | [feedback] 심리학 고양이의 대본을참조해주세요 이야기는 삽화로 설명은 모션그래픽으로 증거는 실제 자료 인물사진 등으로 검은 화면이나 중간중간 연출은 마디로 해주세요. 삽화는 잼편처럼 말이죠  | claude/affectionate-faraday-8bp5bx 의 제안 — 잠금을 잡은 쪽이 반영(feedback·review·매뉴얼 수정) 뒤 제안 파일의 status 를 done 으로 | 2026-11-20 |
| 모순 | manual/06 G8 MUST·README §3-7·11 S9·cli upload 기본 | c-20261120-24: manual/06 G8 MUST·README §3-7·11 S9·cli upload 기본 ↔ AGENTS.md 저장 규칙·docs/09 §0 (2026-11-16 사용자) | 어느 쪽이 맞는지 사용자 판단 — 답을 decision 에 적고 status: decided | 2026-11-20 |
| 모순 | channels/ch-issues-daily/channel.yaml 제목·설명, 08 §0-2 | c-20261120-25: channels/ch-issues-daily/channel.yaml 제목·설명, 08 §0-2 ↔ 같은 파일 target_minutes 10, README §2-4 — 매 | 어느 쪽이 맞는지 사용자 판단 — 답을 decision 에 적고 status: decided | 2026-11-20 |
| 모순 | manual/09 §1 시간표 | c-20261120-26: manual/09 §1 시간표 ↔ manual/09 §2 (v63) — 심층 기본과 90분 제작 시간 | 어느 쪽이 맞는지 사용자 판단 — 답을 decision 에 적고 status: decided | 2026-11-20 |
| 모순 | manual/09 §2 표 | c-20261120-27: manual/09 §2 표 ↔ 같은 표 — 토요일 아침 | 어느 쪽이 맞는지 사용자 판단 — 답을 decision 에 적고 status: decided | 2026-11-20 |
| 모순 | channels/brands.yaml identity·05 §0-7 | c-20261120-28: channels/brands.yaml identity·05 §0-7 ↔ 04 §0-7 (v73, 04 §0-8 v60 을 바꿈) — 호기심 채널 정체성 | 어느 쪽이 맞는지 사용자 판단 — 답을 decision 에 적고 status: decided | 2026-11-20 |
| 모순 | data/style_profile.json (writing.py 가 모든 make 대본 프롬프트에 넣음) | c-20261120-30: data/style_profile.json (writing.py 가 모든 make 대본 프롬프트에 넣음) ↔ manual/README §2-1·§2-4, 12 §0 — m | 어느 쪽이 맞는지 사용자 판단 — 답을 decision 에 적고 status: decided | 2026-11-20 |
| 모순 | 정기 작업 "뉴스레터 소재 수집" 05:40 | c-20261120-32: 정기 작업 "뉴스레터 소재 수집" 05:40 ↔ docs/36 §5-1 — 뉴스레터 정기 작업 역할 | 어느 쪽이 맞는지 사용자 판단 — 답을 decision 에 적고 status: decided | 2026-11-20 |
| 모순 | channels/ch-ai-shorts/README.md | c-20261120-33: channels/ch-ai-shorts/README.md ↔ channels/ch-ai-shorts/channel.yaml — AI 쇼츠 기본 스타일 | 어느 쪽이 맞는지 사용자 판단 — 답을 decision 에 적고 status: decided | 2026-11-20 |

## 고칠 것 (판단 불필요)

| 종류 | 위치 | 내용 | 왜 | 처음 본 날 |
|---|---|---|---|---|
| 모순 점검 차례 | manual/contradictions.yaml | 바뀐 지침 6개 모순 점검: AGENTS.md, channels/ch-knowledge/channel.yaml, manual/01-desire-map.md, manual/06-checklist.md | 바뀐 줄이 다른 지침·정기 작업 지시문과 반대인지 확인 → 장부에 적고 manual-audit --checked | 2026-11-20 |

## 지난 검토 뒤 해결됨

- 제안함: [feedback] 심리학 고양이의 대본을참조해주세요 이야기는 삽화로 설명은 모션그래픽으로 증거는 실제 자료 인물사진 등으로 검은 화면이나 중간중간 연출은 마디로 해주세요. 삽화는
- 깨진 참조: docs/54-my-videos-vs-viral.md
- 모순: c-20261120-29: skills/video-sources §3 ↔ docs/50 §0·AGENTS 소스 규칙 — PC 쿠키 사용과 우회 금지
- 모순: c-20261120-31: manual/04 §0-6 순서 ↔ manual/11 단계표·04 v55 — 호기심 intent.md 순서
- 옛 그래프: 매뉴얼 그래프가 옛것

## 검토 기록

| 날짜 | 고칠 것 | 물어볼 것 | 새로 | 해결 | 메모 |
|---|---|---|---|---|---|
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
| 2026-11-20T11:46 | 1 | 27 | 1 | 8 | 과적합 정리 |
| 2026-11-20T23:11 | 3 | 38 | 18 | 5 |  |
| 2026-11-20T23:13 | 1 | 36 | 1 | 5 |  |
