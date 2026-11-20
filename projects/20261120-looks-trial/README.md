# 새 화풍 3종 시안 — 화이트보드 · 아이소메트릭 · 종이 디오라마 (2026-11-20)

사용자 결정(docs/53 §5-3 "전부 다"). 같은 내용 **"물건이 집 앞까지 오는 길: 공장 → 물류센터 → 트럭 → 문 앞"** 을 화풍만 바꿔 8초씩.
숫자·사실 주장이 없는 예시 내용입니다(판정 대상은 화면 모습과 움직임).

| 화풍 id | 모습 | 움직임 | 짝 효과음 묶음 | 참고 HyperFrames 블록 |
|---|---|---|---|---|
| `whiteboard` | 흰 판, 검정 마커 손글씨, 파랑 화살표, 빨강 동그라미, 지워진 판서 흔적 | 두 번 그은 선이 한 획씩, 펜촉이 끝을 따라감 | `marker` | whiteboard-ink, hw-callout-circle |
| `isometric` | 격자 바닥 위 세 면 상자 건물, 꺾이는 길 | 건물이 차례로 솟고 소포가 길을 따라감, 카메라 아주 천천히 다가감 | `soft-ui` | exploded-stack, offset-path-traveler |
| `paper-diorama` (v2) | 찢긴 흰 단면이 보이는 종이 층(얼룩 섬유 결), 흰 오림 테두리 + 접는 탭 건물, 이쑤시개 깃발, 실에 매단 구름·종이 해, 테이프 붙인 제목 | 층을 실제 원근 깊이에 세우고 카메라가 옆으로 돌며 시차, 건물이 팝업, 모든 소품이 초당 12장 떨림, 트럭·바퀴도 12장 끊기 | `paper-pencil` | stop-motion-cadence, torn-paper-rip |
| `paper-diorama-v1` | (첫 시안 — 비교용) 평면 층, 쪽지 라벨 | 층이 옆으로 미끄러짐 | `paper-pencil` | |

다시 만들기:
```bash
python projects/20261120-looks-trial/02_script/render_trial.py            # 셋 다
python projects/20261120-looks-trial/02_script/render_trial.py isometric  # 하나만
```
→ `05_edit/<id>.mp4`, `05_edit/<id>_{1.5,3.5,5.0,7.6}.jpg`, 묶음 `05_edit/looks-trial-3.mp4` (미디어는 커밋 안 함 — 화풍 하나 15초 안팎 렌더로 언제든 다시 만듦).
화풍 목록 페이지의 화면 화풍 카드는 `05_edit/<id>_7.6.jpg` 가 있으면 그 프레임을 씁니다.

판정: `python -m ytflow review projects/20261120-looks-trial --pass | --reject "이유"` → 합격한 화풍은 `styles/looks.yaml` status 를 approved 로.

## 판정 (2026-11-20 사용자)
> "화이트보드랑 아이소메트릭은 합격, 종이 디오라마는 다시"

- `whiteboard`·`isometric` → `styles/looks.yaml` status **approved**
- `paper-diorama` → v2 다시 만듦(위 표). v1 의 약점(종이 결이 안 보임·층이 평면으로 미끄러짐·건물이 클립아트 같음)을 고침.
  → 사용자 "종이 디오라마도 합격" (v2) → status **approved**
- 기록: `review --pass --note …` 가 잠금 중이라 제안함 `proposals/manual/20261120-074846-vigilant-lovelace-1uahwn.md` 로 감.
