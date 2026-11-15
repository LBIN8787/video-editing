# 주제 레포 — 메인 매뉴얼을 물려받아 주제별로 채우는 층 (docs/33)

```
메인 레포 (manual/ · manual/situations.yaml · styles/techniques.yaml · manual/glossary.yaml)
   │  원칙·작업 기준·공통 상황·연출 기법 — 모든 영상에 적용
   ├── topics/market/topic.yaml     주식 (이어 읽는 시장 · 칼럼 · 쇼츠)
   ├── topics/curiosity/topic.yaml  호기심 (지식·이야기)
   ├── topics/ai/topic.yaml         AI (가이드·쇼츠)
   └── topics/issues/topic.yaml     시사 (이슈·매일 이슈)
          │  inherits: main + defaults(스타일 기본값 덮어쓰기) + situations(add·override·drop)
          └── projects/<영상>/      python -m ytflow edit-plan <영상>
                                     → 02_script/edit_plan.md·json (박자마다 상황 → 장면·기법)
                                     → 02_script/EDIT_CONTEXT.md (이 영상에 적용되는 규칙 묶음, 에이전트가 먼저 읽음)
```

- 주제 레포는 **메인을 고치지 않고** 그 주제에서 달라지는 것만 적습니다. 메인이 바뀌면 모든 주제가 따라갑니다.
- 주제를 고르는 법: 프로젝트 `edit.yaml` 의 channel → `channels/<id>/channel.yaml` 의 brand → `topics/<brand>/`.
- 새 주제(채널) 추가: 폴더 하나 + `topic.yaml` (inherits: main). `python -m ytflow topics` 로 확인.
