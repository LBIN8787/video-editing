---
name: channel-run
description: 운영 채널(channels/<id>) 규칙으로 이번 회차 영상을 만든다. "이번 주 영상", "칼럼 채널 한 편", "쇼츠 3개", "이 조사 글로 영상 만들어줘" 같은 반복 제작 요청에 쓴다. 채널의 형식(롱폼 칼럼·보고서 / 쇼츠 안내), 편집 스타일, 키워드, 분량을 적용하고 에피소드 기록까지 남긴다.
---

# 채널 회차 제작 (반복 작업)

> **먼저 `manual/README.md` 를 읽습니다.** 브랜드(ai·market·curiosity)의 욕망 → `01_research/topic_brief.json` → 채널 매뉴얼(`manual/02~04`)의 조사·대본 공식 → `manual/05-style-matching.md` 로 연출·그래픽 → 단계마다 `python -m ytflow check <프로젝트> --upto G<n>`.
> 사용자 결정은 `python -m ytflow review <프로젝트> --pass | --reject "이유"`. 기각 사유는 매뉴얼 기준으로 고친 뒤 `python -m ytflow manual-bump "요약"`.

## 1. 채널 고르기
`python -m ytflow channels` 로 목록을 봅니다. 채널마다 `channels/<id>/README.md`(운영 안내)와 `channel.yaml`(설정)이 있습니다.
- 롱폼 칼럼(자체 제작, 미주일기): `ch-paper-column` — 자체 제작이 필요한 영상의 기본
- 롱폼 보고서(원본 소스, 식스시그마): `ch-source-brief` — PC 에서 `rebuild` 필요
- 롱폼 데이터 리포트(머니크루): `ch-data-motion`
- 쇼츠 안내: `ch-ai-shorts`(AI·GitHub), `ch-money-shorts`(경제 상식, 롱폼 주제 선정에서 '안내'형으로 넘어온 대기열)
- **형식 판단:** 서술할 내용이 많은 분석 → 롱폼, 한 가지 안내 → 쇼츠. 형식이 다른 소재는 `channels/<id>/queue.md` 로 갑니다.

## 2. 시작하기
먼저 기획만 돌려 주제·형식·소스를 확인하는 것을 권합니다 (주제 선정과 글의 내용이 가장 중요).
```bash
python -m ytflow make --channel <id> --plan                  # 트렌드 → 소스 찾기 → 주제·형식 결정까지
python -m ytflow approve <프로젝트> topic --pick N && python -m ytflow run <프로젝트>
python -m ytflow make --channel <id>                         # 트렌드에서 주제 자동
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
- 영상 보관: `python -m ytflow upload <프로젝트>` → Google Drive `ytflow 영상` 아래 채널(편집 스타일) 폴더. PC 에서는 `config/storage.yaml` 의 `local_sync_dir`(Google Drive for desktop 폴더)에 복사, 클라우드에서는 Drive API 토큰(www.googleapis.com)이 필요합니다.
- `python -m ytflow validate <프로젝트>`, 프레임 시트 `05_edit/final_sheet.png` 확인 (`skills/video-edit`).
- `channels/<id>/episodes.md` 에 회차가 자동으로 기록됩니다. 업로드하면 상태 칸을 '업로드 YYYY-MM-DD'로 고칩니다.
- `REPORT.md` 의 남은 일(임시 화면, 재확인 필요)을 사용자에게 알립니다. 기획 문서만 커밋합니다.
