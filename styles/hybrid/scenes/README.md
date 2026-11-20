# 하이브리드 장면 — 만드는 법과 움직이는 예시 (2026-11-20)

> 사용자: "왜냐하면 예시로 이런거는 저 예시사진으로는 다 안보이잖아" · "일단은 자주 쓰는 스타일과 화풍부터 해줘"
> → 예시 사진 한 장이 아니라 **움직임(박자표) + 짧은 예시 영상**으로. 먼저 지난 회차(시장 8편)에 매번 쓰인 장면 10가지.

장면마다: 언제 쓰나 · **박자표**(대사의 어느 말에서 무엇이 나타나나 — 렌더러 코드 그대로) · `hybrid.json` 쓰는 법 · 확인할 것 · 예시 영상(Drive, 소리 포함 — 말과 화면이 맞물리는 걸 들으며 보기).

| 장면 | 이름 | 언제 | 예시 |
|---|---|---|---|
| [`bignum`](bignum.md) | 큰 숫자 한 개 | 오늘 이야기의 출발점이 되는 숫자 하나(종가·규모·비율). 숫자가 곧 질문일 때 | [영상](https://drive.google.com/file/d/1yD_LnfPrK2pW6p0l_6o-t8hHcMFCzWmn/view) |
| [`bars`](bars.md) | 막대 비교 | 같은 단위의 값 2~6개를 한눈에 비교 (지수 등락·업종·종목). 음수는 기준선 아래로 | [영상](https://drive.google.com/file/d/1pnlWsrvCke45fr1kE6UkvVUm9OVZFfxx/view) |
| [`chapter`](chapter.md) | 장 표지 | 장이 바뀌는 순간. 번호 + 짧은 제목 한 줄 | [영상](https://drive.google.com/file/d/1Aa_JCX4AKbPSD5BaeLtZ6r2s4VHtYhM5/view) |
| [`checklist`](checklist.md) | 줄 목록 | 사건·조건·주장 3~5개를 차례로 쌓을 때. 줄마다 상태(확인 ✓ / 경고 △ / 아님 ✗ / 날짜) | [영상](https://drive.google.com/file/d/1WB0v-x5RTestBbb7_GtmIbfVX0XSvXyf/view) |
| [`map_causal`](map_causal.md) | 인과 지도 (코르크판) | 원인 → 결과가 이어지는 흐름. 카드(노드)가 하나씩 꽂히고 실(화살표)이 이어짐 | [영상](https://drive.google.com/file/d/15-88mqDELcl3jkfHOidgv6lyztGGDkyk/view) |
| [`analogy`](analogy.md) | 비유 두 칸 | 어려운 구조를 생활 속 물건으로 옮길 때. 왼쪽(익숙한 것) ≈ 오른쪽(지금 일) | [영상](https://drive.google.com/file/d/1gntzQVakAUmd7VBrmajqud_Aa8oXgbpH/view) |
| [`quote`](quote.md) | 인용 카드 | 이름 있는 사람·매체의 말 한 문장. 원문 + 번역, 핵심어 형광펜 | [영상](https://drive.google.com/file/d/1duJVu6iZNVg8qR3mvE84gWIsvGfNgq5v/view) |
| [`versus`](versus.md) | 맞대기 | 엇갈린 두 시각·주장 vs 부인·기대 vs 현실 | [영상](https://drive.google.com/file/d/1uze0c79ORRf8IRmXsjG541SM-n_fSjn9/view) |
| [`kinetic`](kinetic.md) | 키네틱 글자 | 결론 한 문장·장 전환 한 줄. 목소리가 말하는 순간 낱말이 박힘 (화면 글자가 곧 자막) | [영상](https://drive.google.com/file/d/10QIVmNXXiB_opqz4RQsLb9J-HeiepuTS/view) |
| [`outro`](outro.md) | 마무리 카드 | 영상 끝. 실사·자료 영상 위에 흐린 막 + 종이 카드 한 장 | [영상](https://drive.google.com/file/d/1LELn4La13CQ7QoulbhPu619tz6UtT8lp/view) |

## 모든 장면에 공통
- **박자(`beats`)**: 한 장면 = 박자 여러 개, 박자 하나 = 대사 한두 문장. 화면 요소는 박자 시작 시각에 맞춰 나타난다.
- **`t` 낱말**: 항목·줄에 `"t": "낱말"` 을 주면 그 낱말을 **말하는 순간**(받아쓰기로 맞춘 시각) 나타난다 — 화면이 말보다 늦거나 빠르지 않게 하는 핵심.
- **숫자 카드(`motion`)**: 박자에 `{"t":"낱말","do":"count","value":"…","label":"…","x":…,"y":…}` — 그 낱말에서 작은 카드가 튀어나와 숫자가 세어진다. 어느 장면 위에나 얹힌다.
- **겹치기(`layers`)**: 낱말 띄우기·자료 사진 액자·날짜 도장·위치 지도·숫자 카드 (05 §0-1).
- **화풍(바탕·색)**: 장면의 `skin`(dark-doc·newsprint …) 또는 `look`(board) — 화풍 목록은 `styles/looks.yaml`, `python -m ytflow looks`.

## 다음에 채울 것
- 같은 틀로: `footage`(실사 B-roll, 호기심 v60 기본)·`bite`(원본 발언)·`timeline`·`people` — 예시 영상이 있는 완성본이 생기면.
- 화풍(`styles/looks.yaml`)마다 같은 장면이 어떻게 달라 보이는지는 화풍 목록 페이지(`skills/looks-gallery`)가 움직이는 미리보기로 보여 준다.
