# 16. 새 연출·그래픽 시험작 (2026-11-08)

기존 하이브리드 연출(`hybrid.py` 장면들)과 기존 그래픽 팩(paper-sketch·clean-flat·dark-doc)은 **건드리지 않고**, 새 연출 장면 4종과 새 그래픽 팩 3종을 **추가만** 했다.
비교가 공정하도록 세 시험작 모두 **같은 이야기(스페인 독감)의 같은 문장, 같은 ElevenLabs 목소리, 같은 자료 화면**을 쓴다. 바뀌는 것은 연출과 그래픽뿐이다.

## 시험작 3편
| 시험작 | 연출 (무엇이 언제 어떻게 바뀌나) | 그래픽 팩 | 어울리는 주제 | 프로젝트 |
|---|---|---|---|---|
| **아카이브 다큐** | 자료 사진·영상 전체 화면 + 천천히 다가가기·옆으로 흐르기(켄 번스) + 시간·장소 도장이 타자기로 찍힘 + 장 사이 검은 화면에 한 줄 문장 | `dark-doc` | 역사·사건·인물 (자료 사진이 많은 주제) | `projects/20261107-style-archive` |
| **지도 여정** | 세계 지도 한 장 위를 카메라가 날아다님: 확대 → 이동 → 경로 선이 그려짐 → 핀·라벨 | `newsprint` (새) | 전파·이동·무역·전쟁 (어디서 어디로) | `projects/20261107-style-journey` |
| **키네틱 타이포** | 내레이션의 단어가 **말하는 순간** 화면에 튀어나옴. 핵심 단어는 크게·강조색. 화면 글자가 곧 자막 | `kinetic-poster` (새) | 쇼츠·훅·결론 요약·명언 (자료 화면이 없을 때) | `projects/20261107-style-kinetic` |

만들기 (다음에도 똑같이):
```bash
python scripts/style_demo.py 20261107-knowledge-스페인독감 20261107-style-archive styles/demos/archive.json
python -m ytflow hybrid 20261107-style-archive      # 렌더 → 자막 → sync-qa 까지 자동
```
스펙(`styles/demos/*.json`)의 박자 `"from": "005_1"` = 원본 프로젝트 5번 장면 1번 박자의 문장과 음성 파일을 그대로 가져온다 → **목소리 비용 0**.

## 새 연출 장면 (`ytflow/stages/directions.py`, `hybrid.json` 의 scene `type`)
기존 장면 타입과 섞어 쓸 수 있다. 등록은 `hybrid.py` 맨 끝의 `directions.register()` 한 줄뿐(실패해도 기존 장면은 그대로 동작).

| type | 필드 | 화면 |
|---|---|---|
| `kb` | `clip{src,start}`, `move`(in/out/left/right/up), `stamp`, `label` | 자료 화면 전체 + 켄 번스 움직임 + 가장자리 어둡게 + 도장 타자기 |
| `card_type` | `lines[]`, `by` | 빈 화면에 줄마다 타자기 (박자 시작에 맞춤), 인용이면 출처 줄 |
| `journey` | `places{key:[경도,위도]}`, `start{goto,zoom}`, 박자마다 `goto`·`zoom`·`route{from,to}`·`pin{at,label,side,dy}`, `pins[]`, `title` | world-atlas 세계 지도 + 카메라 이동 + 곡선 경로 + 핀 라벨 (라벨은 화면 오른쪽 가까이면 왼쪽으로, 겹치면 `dy` 로 위아래 이동) |
| `kinetic` | 박자마다 `hit[]` (강조 단어) | 받아쓰기 단어 시각에 맞춰 단어가 튀어나옴, `hit` 단어·숫자는 크게·강조색 |

## 새 그래픽 팩 (`skins/<id>/skin.yaml`)
| 팩 | 겉모습 | 컴포넌트 |
|---|---|---|
| `newsprint` 신문지 | 누런 종이, 먹색 활자, 진한 빨강, 흑백 사진, 곧은 선 | 막대·사람 그림·상자 흐름 |
| `blueprint` 청사진 | 남색 모눈, 흰 선, 노란 강조 | 막대·도넛·알약 흐름 |
| `kinetic-poster` 키네틱 포스터 | 크림 바탕, 검정 굵은 고딕, 빨강 강조. **아래 자막 숨김**(화면 글자가 자막) | 막대·와플 |

기존 하이브리드 영상에 새 팩만 씌워 보기: `python -m ytflow skin-preview <프로젝트> --skins newsprint,blueprint`.

## 지도 자료
- 국경선: `world-atlas@2.0.2` (ISC, Natural Earth 110m 기반 — 퍼블릭 도메인), 투영: `d3-geo` (ISC). 버전은 `tools/external.json` 에 고정.
- `ytflow/assets/world_map.mjs` 가 위경도 → 화면 좌표·국가 경로를 만든다 (키·네트워크 불필요, npm 설치 후).

## 연출 고르는 기준 (docs/15 와 연결)
- 자료 화면이 20~30초마다 있어야 한다는 규칙 → **아카이브 다큐**가 가장 잘 지킨다(거의 전부 자료 화면). 대신 숫자 비교는 약하니 막대(`compare`) 장면을 섞는다.
- '어디서 어디로'가 이야기의 뼈대이면 **지도 여정**. 한 영상에 2~4번, 지도 한 장을 계속 쓰면 시청자가 위치를 잃지 않는다.
- 정지 화면 비율을 낮추고 싶을 때(docs/15 의 0.5 → 0.26 목표) **키네틱 타이포**가 가장 효과가 크다(단어마다 화면이 바뀜). 다만 9분 내내 쓰면 피로 → 훅(첫 30초)·장 전환·결론에만.
- 실제 운영 추천: 하이브리드(기본) 위에 **도입은 kb + card_type, 전파 장면은 journey, 결론 한 줄은 kinetic** 으로 섞기.
