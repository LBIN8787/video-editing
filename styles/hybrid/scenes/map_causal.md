# `map_causal` — 인과 지도 (코르크판)

**언제:** 원인 → 결과가 이어지는 흐름. 카드(노드)가 하나씩 꽂히고 실(화살표)이 이어짐

**예시 영상 (움직임):** [map_causal.mp4](https://drive.google.com/file/d/15-88mqDELcl3jkfHOidgv6lyztGGDkyk/view) — Drive `ytflow/style-examples/` · 원본: `projects/20261120-market-deep` 완성본 2:26~3:00

## 박자표 — 무엇이 언제 나타나나
| 언제 | 화면 |
|---|---|
| 박자 시작 + 0.25초×순서 | `reveal` 의 카드가 하나씩 꽂힘 |
| +0.6초 + 0.55초×순서 | `draw` 의 실이 그어짐(연필 소리) — 지금 말하는 곳으로 가는 실은 빨강 |
| +0.9초 | `active` 카드에 빨간 동그라미(지금 이야기하는 곳) |
| `cut` | 이미 그은 실을 지우지 않고 빨간 점선 + X 로 바꿈 |
| `tag` | 카드 옆에 형광펜 쪽지(+1.0초) |

## 대본(`02_script/hybrid.json`)에 쓰는 법
```json
{"type":"map_causal","look":"board",
 "map":{"nodes":{"q":{"label":"질문을 먼저 받은 곳: 엔비디아 -34%","icon":"circle-alert","x":960,"y":260}, …},
        "edges":[["q","alt"],["alt","d19"],["d19","all"]]},
 "beats":[{"say":"…","reveal":["q","alt"],"draw":[["q","alt"]],"active":"alt"},
          {"say":"…","reveal":["d19","all"],"draw":[["alt","d19"],["d19","all"]],"active":"all"}]}
```

## 만들기
`python -m ytflow edit-plan <프로젝트>` → `hybrid.json` 에 위 장면 → `python -m ytflow check <프로젝트> --upto G5` → `python -m ytflow hybrid <프로젝트>`

## 확인할 것
카드 글이 칸을 넘지 않는지 · 실이 다른 카드를 가로지르지 않는지(layout_qa) · `active` 가 대사의 초점과 맞는지

코드: `ytflow/stages/hybrid.py `s_map_causal` · `_node_box` · `_edge``
