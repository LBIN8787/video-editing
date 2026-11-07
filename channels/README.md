# 운영 채널

편집 스타일 하나 = 유튜브 채널 하나로 운영합니다. 채널 폴더에는 그 채널의 **설정(channel.yaml)·운영 안내(README.md)·에피소드 기록(episodes.md)** 이 있습니다.
영상 한 편의 작업 파일은 `projects/<날짜>-<채널>-<주제>/` 에 쌓이고, 완성되면 `episodes.md` 에 한 줄이 자동으로 추가됩니다.

| 채널 | 형식 | 편집 스타일 | 계열 | 주기 |
|---|---|---|---|---|
| [`ch-paper-column`](ch-paper-column/README.md) (가칭) 종이 위의 경제 | 롱폼 칼럼 | 미주일기 (`mijudiary`) | 자체 제작 인포그래픽 | 주 1편 |
| [`ch-source-brief`](ch-source-brief/README.md) (가칭) 원본으로 보는 기업 | 롱폼 보고서 | 식스시그마 (`sixsigma`) | 원본 소스 | 주 1~2편 |
| [`ch-data-motion`](ch-data-motion/README.md) (가칭) 숫자로 보는 산업 | 롱폼 데이터 리포트 | 머니크루 (`moneycrew`) | 자체 제작 인포그래픽 | 격주 1편 |
| [`ch-ai-shorts`](ch-ai-shorts/README.md) (가칭) AI 꿀팁 1분 | 쇼츠 안내 | AI 꿀팁 쇼츠 (`shorts-aitips`) | 쇼츠 | 주 3~5편 |
| [`ch-money-shorts`](ch-money-shorts/README.md) (가칭) 1분 경제 상식 | 쇼츠 안내 (정보형) | 쇼츠 (`shorts-aitips`, 카드·큰 글씨) | 쇼츠 | 대기열에서 주 3~5편 |
| [`ch-knowledge`](ch-knowledge/README.md) (가칭) 몰랐던 이유 | 롱폼 교양 (역사·상식·심리) | 하이브리드 (`hybrid`) | 원본 소스 (공공 기록) | 주 1편 + 몰아보기 |

## 소스 찾는 법 (채널마다 출발점이 다름 — docs/07-sourcing.md)
| 채널 | 출발점 | 무엇부터 찾나 |
|---|---|---|
| ch-source-brief | 발언 원본 | 방송·IR·기관 공식 채널의 최근 10일 인터뷰·실적 콜 → 발언 → 공시로 확인·정정 |
| ch-paper-column | 1차 문서 | 연구·논문·IR·SEC·정부 문서 → 개념 칼럼, 사진은 위키미디어 CC |
| ch-data-motion | 숫자 계열 | 시세·통계 + 비교할 과거 시기 → 직접 계산 |
| ch-knowledge | 공공 기록 + 수요 | `demand` 로 잘 되는 질문 유형 → 미국 의회도서관·NASA 자료 화면(`archive search`) → 1차 출처 팩트시트 |
| ch-ai-shorts | 저장소 | GitHub 최근 14일 별 증가 + README |
| ch-money-shorts | 대기열 | 롱폼 주제 선정에서 '안내'형으로 판단된 소재 |

## 형식 나누기
주제 선정(select)이 소스와 글의 깊이를 보고 형식을 정합니다. **서술할 내용이 많고 자세한 분석 → 롱폼, 한 가지를 알려 주는 정보형 → 쇼츠.**
채널 형식과 다른 소재는 버리지 않고 맞는 채널의 `queue.md` 로 보냅니다(`config/pipeline.yaml` 의 `format_channels`).

```bash
python -m ytflow channels                       # 목록·에피소드 수
python -m ytflow make --channel <id>            # 그 채널 규칙으로 한 편
```

## 새 채널 추가
1. `channels/<새 id>/channel.yaml` 을 다른 채널에서 복사해 `title·format·style_ref·niche·seed_keywords·target_minutes` 를 고칩니다.
2. 새 편집 스타일이 필요하면 `skills/edit-style-new` 로 `styles/<id>/` 를 먼저 만듭니다.
3. `episodes.md` 는 빈 표로 만들어 둡니다(형식은 다른 채널과 같게).
