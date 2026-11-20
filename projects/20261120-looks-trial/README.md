# 새 화풍 3종 시안 — 화이트보드 · 아이소메트릭 · 종이 디오라마 (2026-11-20)

사용자 결정(docs/53 §5-3 "전부 다"). 같은 내용 **"물건이 집 앞까지 오는 길: 공장 → 물류센터 → 트럭 → 문 앞"** 을 화풍만 바꿔 8초씩.
숫자·사실 주장이 없는 예시 내용입니다(판정 대상은 화면 모습과 움직임).

| 화풍 id | 모습 | 움직임 | 짝 효과음 묶음 | 참고 HyperFrames 블록 |
|---|---|---|---|---|
| `whiteboard` | 흰 판, 검정 마커 손글씨, 파랑 화살표, 빨강 동그라미, 지워진 판서 흔적 | 두 번 그은 선이 한 획씩, 펜촉이 끝을 따라감 | `marker` | whiteboard-ink, hw-callout-circle |
| `isometric` | 격자 바닥 위 세 면 상자 건물, 꺾이는 길 | 건물이 차례로 솟고 소포가 길을 따라감, 카메라 아주 천천히 다가감 | `soft-ui` | exploded-stack, offset-path-traveler |
| `paper-diorama` | 찢은 색종이 층, 팝업 건물, 크림 쪽지 | 층마다 다른 속도로 옆으로(시차), 건물이 세워지고, 트럭이 뚝뚝 끊기며 감 | `paper-pencil` | stop-motion-cadence, torn-paper-rip |

다시 만들기:
```bash
python projects/20261120-looks-trial/02_script/render_trial.py            # 셋 다
python projects/20261120-looks-trial/02_script/render_trial.py isometric  # 하나만
```
→ `05_edit/<id>.mp4`, `05_edit/<id>_{1.5,3.5,5.0,7.6}.jpg`, 묶음 `05_edit/looks-trial-3.mp4` (미디어는 커밋 안 함 — 화풍 하나 15초 안팎 렌더로 언제든 다시 만듦).
화풍 목록 페이지의 화면 화풍 카드는 `05_edit/<id>_7.6.jpg` 가 있으면 그 프레임을 씁니다.

판정: `python -m ytflow review projects/20261120-looks-trial --pass | --reject "이유"` → 합격한 화풍은 `styles/looks.yaml` status 를 approved 로.
