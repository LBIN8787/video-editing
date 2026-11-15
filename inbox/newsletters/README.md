# 뉴스레터 소재가 쌓이는 곳

`<YYYYMMDD>.md` (사람이 읽는 표) · `<YYYYMMDD>.json` (기계용) — 그날 영상 몫. 한국 06:00 이후 도착분은 다음 날 파일.
만드는 법·규칙: `docs/36-newsletters.md`. 명령: `python -m ytflow newsletters ingest|rss|show|sources`.

- 소재마다: 원래 제목 · 원문·기사 · 원자료·통계 · 영상·이미지 · 재사용 조건 · 뉴스레터 (채널별: 시장·AI·호기심·시사)
- **단서**입니다. 문장을 대본·화면에 옮기지 않고, 숫자·발언은 1차 출처로 확인합니다.
- 메일 본문은 여기 두지 않습니다 (`.cache/newsletters/raw/`, 커밋 안 함).
- 시장·시사 매일 브리핑은 `daily` 가 이 파일을 `daily_brief.md` 끝 '⑦ 뉴스레터 화제'로 붙입니다.
