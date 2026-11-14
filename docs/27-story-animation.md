# 27. 호기심 채널: 대본 → 그림·애니메이션 (2026-11-14)

> 사용자: "호기심 같은 채널은 자료와 함께 설명하기보다 흥미롭게 이야기를 풀어내는 게 핵심이기에, 대본을 바탕으로 애니메이션·이미지를 생성해 주세요.
>  예시로 '보기 잡기 걷기' 단어가 아니라 이미지와 애니메이션으로요. … 졸라맨을 하지 말라 한 거지, 대본에 따른 이미지와 애니메이션을 제작하지 말라 한 게 아니에요."

## 원칙
- 호기심(이야기형)은 **문장이 말하는 행동을 그림이 직접 한다.** 단어 쪽지(보기·잡기·걷기)·자료 캡처는 보조, 주인공은 장면 그림.
- 등장인물·사물은 **한 그림체**로 처음부터 끝까지 (같은 아기·같은 로봇). 자세를 바꿔 이야기를 진행한다.
- 움직임은 행동일 때만(걷기·잡기·헛손질·갸웃), 제자리 흔들림 없음 (2026-11-13 규칙 유지).

## 두 가지 방식 (비교 시험: `scripts/anim_compare/make.py`, 모라벡 편 #6·#9)
| | A. AI 그림 조각 (`cut` · `pose` · `move` · `shake`) | B. 직접 그린 관절 인형 (`puppet` · `act`) |
|---|---|---|
| 그림 | 생성 일러스트(평면 에디토리얼, 크림·남색·벽돌색) — 완성도 높음 | 코드로 그린 평면 벡터 — 단순 |
| 움직임 | 자세 그림을 바꿔 끼움(움츠렸다 펴기) + 걸어가기(걸음마다 튐) + 등장·카메라 | 관절이 실제로 돎: 고개 돌리기·팔 뻗어 잡기·다리 번갈아 걷기·집게 헛집기 |
| 비용 | ElevenLabs 크레딧 약 98/장 (bytedance-seedream-5.5). 인물 1명 = 자세 3개 한 장. 한 편 ≈ 8~12장 ≈ 1,000크레딧 | 0 |
| 자동화 | 그림 주문(프롬프트)을 대본에서 뽑아 생성 → 배경 지우기 → 조각 | 새 캐릭터·행동은 코드 추가 |

## A 만드는 법
1. **인물 한 장에 자세 여러 개 (모델 시트)** — 같은 인물이 장마다 달라지지 않게:
   `Character model sheet: the same <인물 묘사> shown three times side by side, evenly spaced with clear empty space between them, each full body and not overlapping: (1) <자세1>; (2) <자세2>; (3) <자세3>. Flat editorial vector illustration, warm cream, navy blue and muted brick-red palette, confident navy outlines, soft flat shading, subtle paper grain, charming and gentle. Plain pure white background, no ground shadows, no text, no labels.`
2. 사물도 같은 문장 뒤쪽(그림체 부분)을 그대로 붙여 한 장에 여러 개.
3. 흰 배경 지우기 + 조각 나누기: 가장자리와 이어진 흰색만 지움(옷의 흰 부분은 남김), 세로로 빈 열에서 자름 → `04_assets/story/gen/<이름>.png`
   (이번 시험의 코드: 대화 기록 / 정식 명령은 다음 단계에서 `ytflow` 에 넣음).
4. 대본: `{"t": "보고", "do": "cut", "id": "bb", "src": "gen/baby_look.png", "x": 800, "y": 1150, "h": 480}` (y = 발바닥),
   `{"t": "잡고", "do": "pose", "on": "bb", "src": "gen/baby_grab.png"}`, `{"t": "걷는", "do": "move", "on": "bb", "dx": 1250, "dur": 3.0}`, `{"do": "shake"}`.
5. 생성 그림은 미디어라 커밋하지 않고 GitHub Release 에 보관(`upload --archive`). 프롬프트는 이 문서·스크립트에 남겨 다시 만들 수 있게.

## B 만드는 법
`ytflow/stages/puppet.py` — baby(look·grab·walk) · robot(look·reach·fumble·confused·walk) · block · shirt_crumpled · shirt_folded.
`{"do": "puppet", "char": "baby", "id": "bb", "x", "y", "s"}` → `{"do": "act", "on": "bb", "a": "grab", "target": "blk"}`.

## 같이 고친 것
- '모라벡의 역설' 같은 큰 글자가 다른 그림 뒤에 가려짐 → 큰 글자는 기본 앞 겹(z 2) + 종이색 테두리. 배경 연도만 `"z": 0`.
