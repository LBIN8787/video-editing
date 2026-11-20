---
name: channel-run
description: 운영 채널(channels/<id>) 규칙으로 이번 회차 영상을 만든다. "이번 주 영상", "칼럼 채널 한 편", "쇼츠 3개", "이 조사 글로 영상 만들어줘" 같은 반복 제작 요청에 쓴다. 채널의 형식(롱폼 칼럼·보고서 / 쇼츠 안내), 편집 스타일, 키워드, 분량을 적용하고 에피소드 기록까지 남긴다.
---

# 채널 회차 제작 (반복 작업)

> **먼저 `manual/README.md` 를 읽습니다.** 브랜드(ai·market·curiosity·issues)의 욕망 → `01_research/topic_brief.json` → 채널 매뉴얼(`manual/02~04`·`08`, 시장 매일은 `09`)의 조사·대본 공식 → `manual/05-style-matching.md` 로 연출·그래픽 → 단계마다 `python -m ytflow check <프로젝트> --upto G<n>`.
> 사용자 결정은 `python -m ytflow review <프로젝트> --pass | --reject "이유"`. 기각 사유는 매뉴얼 기준으로 고친 뒤 `python -m ytflow manual-bump "요약"`.

## 1. 채널 고르기
`python -m ytflow channels` 로 목록을 봅니다. 채널마다 `channels/<id>/README.md`(운영 안내)와 `channel.yaml`(설정)이 있습니다.
브랜드별 라인은 `channels/brands.yaml` 의 `lines` 가 원본입니다.
- **market:** `ch-market-daily`(매일, 주력 — `manual/09-market-daily.md`) · `ch-source-brief`(발언 원본, 원본 구간은 `clip-order` → PC `clip-fetch`) · `ch-paper-column`(개념 칼럼, 미주일기) · `ch-data-motion`(숫자 리포트, 머니크루) · `ch-money-shorts`(쇼츠)
- **ai:** `ch-ai-guide`(롱폼) · `ch-ai-shorts`(쇼츠)
- **curiosity:** `ch-knowledge` · **issues:** `ch-issues` · `ch-issues-daily`
- 대부분의 롱폼 라인은 `hybrid` 로 만들고(`python -m ytflow hybrid <프로젝트>`), 장면마다 연출을 다시 고릅니다 (`edit-plan`, manual/05·12).
- **형식 판단:** 서술할 내용이 많은 분석 → 롱폼, 한 가지 안내 → 쇼츠. 형식이 다른 소재는 `channels/<id>/queue.md` 로 갑니다.

## 2. 시작하기
먼저 기획만 돌려 주제·형식·소스를 확인하는 것을 권합니다 (주제 선정과 글의 내용이 가장 중요).
```bash
python -m ytflow make --channel <id> --plan                  # 트렌드 → 소스 찾기 → 주제·형식 결정까지
python -m ytflow approve <프로젝트> topic --pick N && python -m ytflow run <프로젝트>
python -m ytflow make --channel <id>                         # 트렌드에서 주제 자동 (D1 사용자 결정 후, manual/11 §2-2)
python -m ytflow make --channel <id> --topic "주제"
python -m ytflow make --channel <id> --from-text <조사글.md>   # 대화형 LLM 답·메모 → 사실 확인 → 원고 → 영상
```
사용자가 대화에 조사 글을 붙여 넣었다면, 그 글을 파일로 저장해 `--from-text` 로 넘깁니다.

## 3. 원고 검수 (가장 중요)
`01_research/article.md` 를 읽고 형식 규칙(`formats/longform.md` 또는 `formats/shorts.md`)에 맞는지 봅니다.
- 롱폼: 질문 → 배경 → 분석 → 과거 사례 → 반론 → 결론·다음에 볼 것. 숫자마다 비교 기준과 [F번호].
- 쇼츠: 결과 → 무엇 → 어떻게 → 비교 → CTA, 약 200자.
고쳤다면 `python -m ytflow stage <프로젝트> script` 부터 다시 돌립니다.

## 4. 끝난 뒤
- `python -m ytflow check <프로젝트>` 가 MUST 실패 없이 통과해야 사용자에게 보냅니다. `05_edit/checklist.md` 를 결과 보고에 붙입니다.
- 영상 보관: `python -m ytflow upload <프로젝트>` → GitHub Release(공개해도 되는 것만). 큰 파일·비공개 자료는 `--to drive` 또는 PC 의 `YTFLOW_DRIVE` 폴더 (docs/09 §0).
- `python -m ytflow validate <프로젝트>`, 프레임 시트 `05_edit/final_sheet.png` 확인 (`skills/video-edit`).
- 유튜브 올리기: `yt-pack <프로젝트>` → 사용자 최종 승인(D4, 매일 시장 채널만 자동 예약 공개) → `yt-publish <프로젝트>` (docs/24).
- `channels/<id>/episodes.md` 에 회차가 자동으로 기록됩니다. 올린 뒤 상태 칸을 '업로드 YYYY-MM-DD'로 고칩니다.
- `REPORT.md` 의 남은 일(임시 화면, 재확인 필요)을 사용자에게 알립니다. 기획 문서만 커밋합니다.
