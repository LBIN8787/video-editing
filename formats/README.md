# 영상 형식 (format)

ytflow 의 기본 생각: **영상은 '잘 쓴 글'을 화면으로 옮긴 것**입니다.
대화형 LLM(ChatGPT·Claude·Perplexity 등)에게 묻고 답을 받아 정리하던 조사 글을,
① 사실을 확인하고 ② 형식에 맞게 다듬고 ③ 장면 대본으로 나누고 ④ 그림·자막·음성으로 영상화합니다.

```
조사 글(대화형 LLM 답·내 메모·트렌드)        00_source/input.md  (있으면)
   └─ research : 웹 검색으로 숫자·발언 확인    01_research/factsheet.md
   └─ article  : 형식에 맞게 다듬은 글         01_research/article.md   ← 사람이 읽고 고치는 '원고'
   └─ script   : 글 → 장면 대본                02_script/scenes.json
   └─ 소스·음성·화면·자막·편집·마스터링        05_edit/final.mp4
```

| 형식 | 글의 성격 | 길이 | 구조 | 문서 |
|---|---|---|---|---|
| `longform` | **장편 칼럼·보고서 분석**. 하나의 질문을 끝까지 파고든다 | 8~12분 (글 약 2,500~3,500자) | 질문 → 배경 → 데이터 분석 → 과거 사례 → 반론 → 결론·다음에 볼 것 | `formats/longform.md` |
| `shorts` | **짧은 주제 안내**. 한 가지를 빨리 알려 준다 | 30~45초 (글 약 200자) | 결과·이득 → 무엇인가 → 어떻게 → 한 장면 비교 → 저장 CTA | `formats/shorts.md` |

채널마다 형식이 정해져 있습니다(`channels/<id>/channel.yaml` 의 `format`).
