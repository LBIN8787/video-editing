# (가칭) 원본으로 보는 기업 (`ch-source-brief`)

- **형식:** longform — 장편 칼럼·보고서 분석 (formats/longform.md)
- **편집 스타일:** 원본 소스형 · 식스시그마 스타일 → `styles/sixsigma/`
- **콘셉트:** 실적발표·인터뷰·청문회에서 경영진이 '직접 한 말'을 원본 영상으로 보여 주고, 사이사이 핵심 요약 카드로 숫자를 정리하는 보고서형 채널.
- **분야:** 미국·한국 대형 기술주의 실적발표·경영진 발언 해설. 발언 원문과 공시 숫자로 확인한다. 투자 권유는 하지 않는다.
- **업로드 주기:** 주 1~2편 (실적 시즌에 몰아서)
- **설정:** `channel.yaml` (키워드·분량·목소리). 만든 영상 기록: `episodes.md`

## 한 편 만들기
```bash
python -m ytflow make --channel ch-source-brief                          # 트렌드에서 주제 자동 선정
python -m ytflow make --channel ch-source-brief --topic "주제"            # 주제 지정
python -m ytflow make --channel ch-source-brief --from-text 조사글.md      # 대화형 LLM 답·메모를 영상으로
```
YouTube 원본 클립은 클라우드에서 받을 수 없어 **사용자 PC 에서 `python -m ytflow rebuild <프로젝트>`** 로 채웁니다.

## 올리기 전 점검
- 원본 발언(quote) 4개 이상, 발언 2~3개마다 핵심 요약 카드가 있는가
- 발언 날짜·행사가 label 에 맞게 적혔는가
- 임시 화면(노란 '임시')이 남아 있지 않은가 (rebuild 후)
- `05_edit/final.mp4` (음량 −14 LUFS 마스터링본), `05_edit/delivery_check.json` (유튜브 규격), `REPORT.md` 의 남은 일
