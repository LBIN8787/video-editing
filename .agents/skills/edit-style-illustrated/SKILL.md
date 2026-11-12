---
name: edit-style-illustrated
description: 손그림 삽화 스타일(삽화 한 장 위를 카메라가 박자마다 옮겨 가고, 붓 쓸기 등장·선이 살아 있는 boil·손그림 동그라미·화살표·생각 풍선이 그려짐)로 장면을 만든다. 사람들의 생각·행동·상황, 비유, 옛 사례 재현에 쓴다. 그림은 사람이 준비하고 art-brief 로 주문서를 만든다.
---

# 손그림 삽화 (`styles/illustrated/STYLE.md`, 장면 type `illust`)

1. 대본에 `illust` 장면을 쓴다:
   - `art`: 파일 이름
   - `brief`: 그릴 내용
   - `moves[{beat, focus:[x,y,w,h]}]`: 그림 비율 0~1
   - `marks[{beat, kind: circle|arrow|underline|note|bubble}]`
2. `python -m ytflow art-brief <프로젝트>` 로 `02_script/art_brief.md`(그림 주문서)를 만들어 사용자에게 준다.
3. 그림(16:9, 2400px 이상)이 `04_assets/art/` 에 들어오면 `python -m ytflow hybrid <프로젝트>` 를 실행한다. 그림이 없으면 자리 카드로 렌더된다.
4. 프레임 확인:
   - 카메라가 그림 밖(빈 곳)을 보이지 않는지
   - 표시가 그림의 중요한 곳을 가리지 않는지
   - 확대한 곳이 흐리지 않은지(그림 해상도)

- **규칙:**
  - 그림 안에 글자를 넣지 않는다.
  - 실존 인물을 닮게 그리지 않는다.
  - 채널마다 그림체를 하나로 통일한다.
  - 영상당 2~5장면만 쓴다.
