---
name: manual-review
description: 매뉴얼 정기 검토(매일 밤 자동 실행·사람이 "매뉴얼 검토해" 할 때). manual-audit 로 충돌·과적합·폐지된 기준 잔재·깨진 참조·층 미정 피드백을 재고, 판단이 필요 없는 것만 고쳐 커밋하고, 판단이 필요한 것은 질문으로 남겨 그래프·알림으로 알린다.
---

# 매뉴얼 정기 검토 (docs/34)

사용자 결정 (2026-11-15): **매일 밤 · 분명한 것만 고침 · 휴대폰 알림 + 그래프**. 매뉴얼 버전은 올리지 않는다 (규칙의 뜻을 바꾸지 않으므로).

## 순서
1. 최신으로: `git fetch origin` 후 작업 브랜치를 최신으로 (다른 세션의 커밋이 있으면 `git pull --rebase`). 작업 트리에 남의 변경이 있으면 건드리지 않는다.
2. 재기: `python -m ytflow manual-graph` → `python -m ytflow manual-audit`. `manual/audit.md` 를 읽는다.
3. **fix 항목만 고친다** (판단이 필요 없는 것):
   | 종류 | 고치는 법 |
   |---|---|
   | 폐지된 기준이 남음 (retired) | `why` 칸의 현재 기준대로 그 문장만 고쳐 쓴다 (예: 순서 예고 → 삭제, intro 장면 → 본론 장면, 8~10분 → 10분~). 사용자 원문 인용(`>`)은 고치지 않는다 |
   | 깨진 참조 (ref) | 같은 내용의 지금 절 번호·파일로 바꾼다. 같은 내용이 없으면 **고치지 말고** ask 로 남긴다 |
   | 코드 위치 바뀜 (coderef) | glossary 는 `code` 의 글자를 지금 코드에 맞게, intents 는 새 줄에 같은 판정을 옮기고 옛 줄은 지운다 (`manualgraph.save_annotation`) |
   | 주제 레포 오류 (topic) | 비슷한 이름의 장면·기법으로 고치되, 확실하지 않으면 ask |
   | 옛 그래프 (stale) | `python -m ytflow manual-graph` |
   고친 것마다 한 줄 요약을 모아 둔다.
4. **ask 항목은 고치지 않는다** (충돌·과적합·반영 대기·층 미정·어긋난 해석). 규칙의 뜻·층·MUST 여부는 사용자가 정한다 (manual/README §3-1). 같은 질문이 이미 며칠째 남아 있으면 알림에 '며칠째'만 적고 새로 길게 쓰지 않는다.
5. 마무리:
   - `python -m ytflow manual-audit --note "정기 검토" --fixed "고친 것 한 줄" --fixed "…"` — 다시 재서 해결 여부를 기록하고, 고친 것을 보고서·그래프('지난 검토에서 고친 것')에 남긴다.
   - `python -m ytflow manual-graph --artifact <스크래치>/manual-graph.html` → Artifact 도구로 **같은 공유 페이지**(`ytflow/stages/manualgraph.py` 의 `ARTIFACT_URL`)에 다시 올린다.
   - 바뀐 것이 있으면 커밋·푸시 (커밋 메시지: `정기 검토 YYYY-MM-DD: 고친 것 N · 물어볼 것 M`).
6. 알림 (PushNotification 도구): `매뉴얼 검토 MM/DD — 고친 것 N · 물어볼 것 M` + 물어볼 것 첫 1~2개 한 줄씩 + 공유 페이지 '한눈에 → 정기 검토'. 물어볼 것도 고친 것도 없으면 짧게 "깨끗함".

## 하지 않는 것
- 매뉴얼 버전 올리기(`manual-bump`), 규칙의 층·MUST 바꾸기, 사용자 원문(`>` 인용·reviews·feedback) 고치기, 영상 렌더·업로드.
- 판단이 애매한 fix 는 고치지 말고 ask 로 남기기 (한 번의 추측으로 규칙을 바꾸지 않는다).
