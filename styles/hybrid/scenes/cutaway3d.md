# `cutaway3d` — 3D 구조 세트

**언제:** 대본이 처음 듣는 구조·공간·연결을 설명하는데 화면이 글씨 카드(체크리스트·큰 숫자)로 끝날 때 — "무엇이 어디에 있고 어떻게 이어지나" (manual/05 §0-10). `edit-plan` 의 `EDIT_CONTEXT.md` §5 가 후보 장면과 샷을 붙여 준다.

**무엇:** 미리 짜 둔 3D 무대(세트) 안을 카메라가 박자마다 옮겨 가며 문을 열고, 연결선에 빛을 흘리고, 이름표를 붙인다. 대본이 고르는 것은 **샷**(세트의 한 구간)뿐이고, 그 구간이 말 길이에 맞춰 늘거나 줄어 재생된다.

**세트:** `styles/3d-docu-motion/sets.yaml` · 목록 `python -m ytflow cutaway3d list` · 샷 미리보기 `python -m ytflow cutaway3d sheet --set dc-rack`

| 세트 | 샷 | 맞는 이야기 |
|---|---|---|
| `dc-rack` | room · scaleout · open · optic · copper · scale · now · future | 스케일업/스케일아웃(NVLink·이더넷·인피니밴드), 광모듈·광섬유·CPO, 구리 케이블·AEC, 랙 단위 서버 |

## 대본(`02_script/hybrid.json`)에 쓰는 법

```json
{"type": "cutaway3d", "set": "dc-rack", "label": "개념 재현 · 배선과 비례 단순화",
 "titles": {"scaleout": ["랙 간 연결", "이더넷·인피니밴드"], "open": ["랙 안 연결", "NVLink"]},
 "labels": {"광 링크": "이더넷·인피니밴드", "GPU 간 연결": "NVLink", "가상 광 경로": ""},
 "beats": [
  {"say": "AI 데이터센터에는 연결이 두 종류 있습니다.", "shot": "room"},
  {"say": "랙과 랙 사이는 스위치와 광 케이블로 잇습니다.", "shot": "scaleout"},
  {"say": "한 랙 안을 열어 보면 GPU들이 NVLink 로 묶여 있습니다.", "shot": "open"},
  {"say": "그 연결은 지금 대부분 구리선입니다.", "shot": "copper", "at": "구리선"}
 ]}
```

- `shot`: 문자열 하나, 또는 `[{"shot": "copper"}, {"shot": "scale", "at": "늘어나면"}]` 처럼 한 박자에 여럿. `at` 은 그 낱말을 말하는 순간에 샷을 시작한다. shot 이 없는 박자는 앞 샷이 이어진다.
- 이웃한 샷끼리는 카메라가 이어서 움직이고, 건너뛰면 컷이 된다.
- `chrome`: `lite`(기본: 왼쪽 위 구간 표시 + 이름표 + 오른쪽 위 범례, 아래 자막 자리 비움) · `full`(아래 큰 제목까지 — 자막과 겹칠 수 있음) · `none`(3D 만).
- `labels` 의 원문 글자는 `sets.yaml` 의 샷마다 `labels`. `""` 로 바꾸면 그 이름표를 지운다.

## 사실 규칙
3D 는 개념 재현이다. `label` 을 남기고, 확인되지 않은 수치·제품 구성을 이름표로 붙이지 않는다. 전망은 `future` 샷처럼 점선으로 현재와 구별한다.

## 만드는 방식·비용
브라우저(WebGL2, 헤드리스는 SwiftShader)로 1920×1080 프레임을 뽑아 `04_assets/hb/scene_NNN/assets/cut3d_*.mp4` 를 만들고 원본 영상처럼 깐다. 이 PC 에서 초당 약 3.4프레임(20초 장면 ≈ 3분). 같은 대본·같은 시각이면 다시 만들지 않는다. 원본: 마벨 광학 편 V2 (`styles/3d-docu-motion/scene.html`, 2026-11-28).
