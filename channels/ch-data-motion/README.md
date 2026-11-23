# (가칭) 숫자로 보는 산업 (`ch-data-motion`)

- **형식:** longform — 장편 칼럼·보고서 분석 (formats/longform.md)
- **편집 스타일:** 자체 제작 인포그래픽형 · 머니크루 스타일 (flat 렌더러) → `styles/moneycrew/`
- **콘셉트:** 산업·공급망·실적을 차트와 막대, 굵은 숫자로 비교하는 데이터 리포트형 채널. 과거 사례(같은 축의 주가 차트)와 지금을 나란히 놓는다.
- **분야:** 반도체·AI·에너지 산업의 공급망과 실적 비교. 실제 시세 차트와 공시 숫자로 설명한다. 투자 권유는 하지 않는다.
- **업로드 주기:** 격주 1편
- **설정:** `channel.yaml` (키워드·분량·목소리). 만든 영상 기록: `episodes.md`

## 한 편 만들기
```bash
python -m ytflow make --channel ch-data-motion                          # 트렌드에서 주제 자동 선정
python -m ytflow make --channel ch-data-motion --topic "주제"            # 주제 지정
python -m ytflow make --channel ch-data-motion --from-text 조사글.md      # 대화형 LLM 답·메모를 영상으로
```
클라우드에서 끝까지 완성됩니다.

## 올리기 전 점검
- 차트에 가격·날짜가 적혀 있는가
- 과거와 지금이 같은 형식의 카드로 비교되는가
- 비교 기준(작년 대비 등)이 화면에 있는가
- `05_edit/final.mp4` (음량 −14 LUFS 마스터링본), `05_edit/delivery_check.json` (유튜브 규격), `REPORT.md` 의 남은 일
