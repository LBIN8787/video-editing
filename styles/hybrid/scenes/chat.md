<!-- visual_spec.py 가 만든 파일 — 다시 만들면 덮어씀. 손으로 고치려면 이 줄을 지우세요 -->
# `chat` — AI 대화 화면

**언제:** AI 사용법 — 무엇을 물으면 어떻게 답하나

**무엇:** 질문이 타자로, 답이 단어 단위로 흘러나옴 ('예시(재구성)' 표시)

**예시 (움직임):** [연출 예시 목록](https://claude.ai/artifact/SPHyXdpGmcdPwMQu7cpMdP) 의 `chat` 칸 ▶ — 실제 렌더 영상 · 세 컷 그림은 Drive `ytflow/looks/scenes/chat.jpg`, 영상 `ytflow/looks/scenes/clips/chat.mp4`
  - 예시와 실제의 차이: 예시 첫 컷은 타자 시작 전이라 빈 창

## 화면 구성·움직임 원리

- 앱 창 틀(상표 없음, '재구성 예시' 표시) → 사용자 질문이 타자로 → 답이 낱말 단위로 흘러나옴
- turns 에 문답 순서, 박자마다 한 턴

## 박자표 — 무엇이 언제 나타나나

예시 렌더(아래 대본)의 시간축을 그대로 옮긴 것입니다. 시각은 대사 길이에 따라 달라지고, 순서와 간격이 이 장면의 문법입니다.

| 시각(예시 렌더) | 화면 |
|---|---|
| 0.15초 | 「AI 대화 · 재구성 예시 (unslop 절차대로)」 아래에서 떠오름 |
| 0.20초 | 「재구성 예시 — unslop SKILL.md 의 진…」 아래에서 떠오름 |
| 0.45초 | 「/」 나타남 |
| 0.55초 | 요소 나타남 |
| 1.85초 | 「고치기」 나타남 |
| 2.35초 | 요소 나타남 |

## 대본(`02_script/hybrid.json`)에 쓰는 법

`"type": "chat"`

```json
{
 "type": "chat",
 "app": "AI 대화 · 재구성 예시 (unslop 절차대로)",
 "label": "재구성 예시 — unslop SKILL.md 의 진행 순서",
 "turns": [
  {
   "role": "user",
   "text": "/unslop 이 대시보드",
   "beat": 0
  },
  {
   "role": "ai",
   "text": "고치기 전에 진단부터 할게요. 보라색 그라데이션, 이모지 30개, 느낌표 '!!' 3번이 보여요. 방향 다섯 줄을 먼저 정리해 드릴 테니, 이대로 진행할까요?",
   "beat": 0,
   "delay": 1.6
  }
 ],
 "beats": [
  {
   "say": "이 영상을 만든 클로드 코드 세션에서, 설명서의 절차를 그대로 따라 적용했습니다."
  }
 ]
}
```
대본 공통 키: `edit_v10, map` (예: map_causal 의 `map`)

읽는 키 — 장면: `app, label, turns` · 박자: `—` (렌더러 코드에서 자동)

## 만들기

`python -m ytflow edit-plan <프로젝트>` → `hybrid.json` 에 위 장면 → `python -m ytflow check <프로젝트> --upto G5` → `python -m ytflow hybrid <프로젝트>`

예시를 다시 렌더: `python scripts/visual_catalog.py <작업 폴더> --only chat --force` (그림·영상·이 명세가 함께 갱신)

## 확인할 것

- 화면 요소가 말보다 늦거나 빠르지 않은지 (박자 시작에 맞춰 나타남)
- `layout_qa.json` 이 비었는지 — 글자 겹침·대비

코드: `ytflow/stages/directions.py:461` `s_chat`
