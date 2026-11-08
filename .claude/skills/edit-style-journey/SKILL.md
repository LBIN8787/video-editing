---
name: edit-style-journey
description: 지도 여정 편집 스타일(세계 지도 한 장 위를 카메라가 확대·이동하고, 경로 곡선이 그려지고, 핀·라벨이 찍힘)로 장면을 만든다. 전파·이동·무역·공급망·전쟁처럼 '어디서 어디로'가 이야기의 뼈대일 때 본론에 2~4번 쓴다.
---

# 지도 여정 (레시피 `styles/recipes/map-journey.yaml`, 그래픽 팩 `newsprint` 권장)

- **장면 type `journey`** (`ytflow/stages/directions.py`):
  - `places{키:[경도,위도]}` — 이 장면에 나오는 곳만
  - `start{goto,zoom}` — 앞 장면의 끝 카메라와 같게 두면 끊김 없이 이어집니다
  - 박자마다: `goto`(카메라 중심), `zoom`(1=세계, 3~4=대륙, 6+=나라), `route{from,to}`(곡선이 그려짐), `pin{at,label,side,dy}`
  - `pins[]`: 처음부터 찍혀 있는 핀 (이전 장면에서 찍은 것)
- **라벨 규칙:** 화면 오른쪽 38% 안의 핀은 라벨이 자동으로 왼쪽. 가까운 두 핀은 하나에 `dy: -40`(위로) 또는 `side: left`. 렌더 후 프레임으로 겹침 확인.
- **지도 자료:** world-atlas@2.0.2 (ISC, Natural Earth 기반) + d3-geo, `ytflow/assets/world_map.mjs`. 키·네트워크 불필요(npm 설치 후).
- **하지 않기:** 장소 1~2곳뿐인 이야기, 한 영상 5번 이상, 국경이 논쟁 중인 지역을 단정하는 라벨.
- **시험작:** `projects/20261107-style-journey` (`styles/demos/journey.json`).
