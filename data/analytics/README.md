# data/analytics — 채널 운영 수치 (python -m ytflow ops, docs/63)

| 파일 | 내용 |
|---|---|
| `<채널>/channel.json` | 채널 구독·총 조회 (마지막 수집) |
| `<채널>/videos.json` | 영상 목록: 제목·공개 상태·길이·조회·좋아요·댓글·연결된 프로젝트 |
| `<채널>/snapshots.csv` | 수집할 때마다 한 줄씩 쌓는 조회 기록 → '올린 지 24·48·168시간 때' 견주기 |
| `<채널>/comments.jsonl` | 댓글 본문·좋아요·답글 수 (작성자 이름은 저장 안 함) |
| `<채널>/videos/<id>.json` | 분석 권한이 있을 때: 시청 비율·유입 경로·시청 지속 곡선 |
| `<채널>/reach/*.csv` | 분석 권한이 있을 때: 노출·클릭률 일일 보고서 |
| `experiments.md` | 실험 장부 (한 채널에 한 번에 하나) |

채널 이름은 `config/channel_ops.yaml`. 보고서는 `channels/<채널 폴더>/ops/<날짜>.md`.
