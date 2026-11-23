# 말하는 사람 쇼츠 (presenter-shorts)
> 레퍼런스 분석·장단점: `docs/25-reference-2611.md` §2 · `python -m ytflow presenter <프로젝트>` (`ytflow/stages/presenter.py`) · 시험작 `projects/20261113-style-presenter`

1. **촬영:** 휴대폰 가로 또는 세로, 얼굴이 가운데. 1분 안팎, 말 사이 쉼은 신경 쓰지 않아도 됨(자동으로 자름). 원본은 `04_assets/footage/`.
2. **presenter.json:** `source`, `lang`, 구간 `start`·`end`, `face_x`(가로 영상에서 얼굴 위치), `hook`(두세 줄 + 강조 낱말 `hl` + 로고), `keywords`(노란 자막 낱말 — 한 낱말씩), `inserts`(말하는 낱말 `word` 에 맞춰 카드 `cards[≤3]` 또는 숫자 `number`), `punch`(1.1~1.15), `gap`(0.3~0.4초).
3. **자동:** 받아쓰기 → 쉼 자르기(점프 컷) → 컷마다 번갈아 확대 → 9:16 → 훅 제목 3초 → 말하는 순간 자막 → 카드가 뜨는 동안 얼굴은 아래로 → -14 LUFS.
4. **확인:** 컷이 말 중간을 자르지 않았는지(`gap` 을 올림), 카드 시각, 자막 오타(받아쓰기 틀림은 대본처럼 고칠 수 없으니 다시 말하거나 `keywords` 정리).
- 권리: 본인 촬영·퍼블릭 도메인만. 남의 영상 금지.
