# 운영 채널

편집 스타일 하나 = 유튜브 채널 하나로 운영합니다. 채널 폴더에는 그 채널의 **설정(channel.yaml)·운영 안내(README.md)·에피소드 기록(episodes.md)** 이 있습니다.
영상 한 편의 작업 파일은 `projects/<날짜>-<채널>-<주제>/` 에 쌓이고, 완성되면 `episodes.md` 에 한 줄이 자동으로 추가됩니다.

| 채널 | 형식 | 편집 스타일 | 계열 | 주기 |
|---|---|---|---|---|
| [`ch-paper-column`](ch-paper-column/README.md) (가칭) 종이 위의 경제 | 롱폼 칼럼 | 미주일기 (`mijudiary`) | 자체 제작 인포그래픽 | 주 1편 |
| [`ch-source-brief`](ch-source-brief/README.md) (가칭) 원본으로 보는 기업 | 롱폼 보고서 | 식스시그마 (`sixsigma`) | 원본 소스 | 주 1~2편 |
| [`ch-data-motion`](ch-data-motion/README.md) (가칭) 숫자로 보는 산업 | 롱폼 데이터 리포트 | 머니크루 (`moneycrew`) | 자체 제작 인포그래픽 | 격주 1편 |
| [`ch-ai-shorts`](ch-ai-shorts/README.md) (가칭) AI 꿀팁 1분 | 쇼츠 안내 | AI 꿀팁 쇼츠 (`shorts-aitips`) | 쇼츠 | 주 3~5편 |

```bash
python -m ytflow channels                       # 목록·에피소드 수
python -m ytflow make --channel <id>            # 그 채널 규칙으로 한 편
```

## 새 채널 추가
1. `channels/<새 id>/channel.yaml` 을 다른 채널에서 복사해 `title·format·style_ref·niche·seed_keywords·target_minutes` 를 고칩니다.
2. 새 편집 스타일이 필요하면 `skills/edit-style-new` 로 `styles/<id>/` 를 먼저 만듭니다.
3. `episodes.md` 는 빈 표로 만들어 둡니다(형식은 다른 채널과 같게).
