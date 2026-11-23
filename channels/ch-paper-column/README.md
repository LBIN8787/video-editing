# (가칭) 종이 위의 경제 (`ch-paper-column`)

- **형식:** longform — 장편 칼럼·보고서 분석 (formats/longform.md)
- **편집 스타일:** 자체 제작 인포그래픽형 · 미주일기 스타일 (HyperFrames 카드) → `styles/mijudiary/`
- **콘셉트:** 한 주의 경제·기업 뉴스 하나를 골라, 칼럼처럼 '왜 그런가'를 끝까지 풀어 주는 채널. 종이 위에 손으로 그려 가며 설명하는 화면(미주일기 스타일)으로, 일반인도 숫자와 비유로 이해하게 한다.
- **분야:** 주식시장 중심의 투자·기술·기업 해설. 돈의 흐름·실적·구조를 숫자·비유·과거 사례로 풀어 준다. 종목 추천·매수 권유는 하지 않는다.
- **업로드 주기:** 주 1편 (예: 목요일 업로드)
- **설정:** `channel.yaml` (키워드·분량·목소리). 만든 영상 기록: `episodes.md`

## 한 편 만들기
```bash
python -m ytflow make --channel ch-paper-column                          # 트렌드에서 주제 자동 선정
python -m ytflow make --channel ch-paper-column --topic "주제"            # 주제 지정
python -m ytflow make --channel ch-paper-column --from-text 조사글.md      # 대화형 LLM 답·메모를 영상으로
```
클라우드에서 끝까지 완성됩니다.

## 올리기 전 점검
- 화면 2초마다 변하는가, 펜 선·숫자가 끝까지 그려지는가
- 비유 카드 2개 이상, 과거 사례 1개 이상이 화면에 있는가
- 자막 상자가 아래에 있고 글자와 겹치지 않는가
- `05_edit/final.mp4` (음량 −14 LUFS 마스터링본), `05_edit/delivery_check.json` (유튜브 규격), `REPORT.md` 의 남은 일
