<!-- visual_spec.py 가 만든 파일 — 다시 만들면 덮어씀. 손으로 고치려면 이 줄을 지우세요 -->
# `terminal` — 터미널

**언제:** 개발 도구·명령 사용법 (실제 실행 기록만)

**무엇:** 명령이 타자로, 결과가 줄 단위로

**예시 (움직임):** [연출 예시 목록](https://claude.ai/artifact/SPHyXdpGmcdPwMQu7cpMdP) 의 `terminal` 칸 ▶ — 실제 렌더 영상 · 세 컷 그림은 Drive `ytflow/looks/scenes/terminal.jpg`, 영상 `ytflow/looks/scenes/clips/terminal.mp4`

## 화면 구성·움직임 원리

- 검은 터미널 창 → 명령(cmd)이 타자로 → 결과(out) 줄 단위로
- 실제 실행 기록만 (설명용 재구성이면 label 에 '재구성')

## 박자표 — 무엇이 언제 나타나나

예시 렌더(아래 대본)의 시간축을 그대로 옮긴 것입니다. 시각은 대사 길이에 따라 달라지고, 순서와 간격이 이 장면의 문법입니다.

| 시각(예시 렌더) | 화면 |
|---|---|
| 0.15초 | 「터미널 · 실제 실행 기록 (2026.11.9)」 아래에서 떠오름 |
| 0.20초 | 「실제 실행 기록」 아래에서 떠오름 |
| 0.65초 | 요소 나타남 |
| 2.75초 | 「Cloning into 'unslop'...」 나타남 |
| 3.35초 | 요소 나타남 |
| 8.64초 | 「SKILL.md agents references s…」 나타남 |

## 대본(`02_script/hybrid.json`)에 쓰는 법

`"type": "terminal"`

```json
{
 "type": "terminal",
 "title": "터미널 · 실제 실행 기록 (2026.11.9)",
 "label": "실제 실행 기록",
 "lines": [
  {
   "cmd": "git clone https://github.com/heydamir/unslop",
   "beat": 0
  },
  {
   "out": "Cloning into 'unslop'...",
   "beat": 0,
   "delay": 2.4
  },
  {
   "cmd": "cp -r unslop/skills/unslop ~/.claude/skills/",
   "beat": 0,
   "delay": 3.0
  },
  {
   "cmd": "ls ~/.claude/skills/unslop",
   "beat": 1,
   "delay": 0.3
  },
  {
   "out": "SKILL.md  agents  references  scripts",
   "beat": 1,
   "delay": 1.4
  }
 ],
 "beats": [
  {
   "say": "설치는 간단합니다. 깃허브에서 내려받아, 클로드의 스킬 폴더에 복사하면 끝이에요."
  },
  {
   "say": "폴더 안에는 SKILL.md라는 설명서 한 장과, 참고 자료, 보조 스크립트가 들어 있습니다."
  }
 ]
}
```
대본 공통 키: `edit_v10, map` (예: map_causal 의 `map`)

읽는 키 — 장면: `label, lines, title` · 박자: `—` (렌더러 코드에서 자동)

## 만들기

`python -m ytflow edit-plan <프로젝트>` → `hybrid.json` 에 위 장면 → `python -m ytflow check <프로젝트> --upto G5` → `python -m ytflow hybrid <프로젝트>`

예시를 다시 렌더: `python scripts/visual_catalog.py <작업 폴더> --only terminal --force` (그림·영상·이 명세가 함께 갱신)

## 확인할 것

- 화면 요소가 말보다 늦거나 빠르지 않은지 (박자 시작에 맞춰 나타남)
- `layout_qa.json` 이 비었는지 — 글자 겹침·대비

코드: `ytflow/stages/directions.py:499` `s_terminal`
