---
name: looks-gallery
description: 화풍 목록을 눈으로 보여 준다. 사용자가 "화풍목록 보여줘", "화풍 보여줘", "어떤 화풍 있어?", "화풍 예시"처럼 말하면 쓴다. 모션그래픽·삽화·실사 색보정 화풍을 같은 장면 예시로 비교하는 공유 페이지를 최신 목록(styles/looks.yaml)으로 다시 만들어 열어 준다.
---

# 화풍 목록 보여 주기 (2026-11-20 사용자: "나중에 화풍목록 보여줘 하면 화풍목록의 예시를 볼 수 있도록 — 시각적으로")

공유 페이지: https://claude.ai/artifact/K4CRgsyTYsWGCDw5RoCtam (`ytflow/stages/looks.py` 의 `GALLERY_URL`)

## 순서
1. 페이지를 최신 목록으로 다시 만든다 (모션그래픽은 화풍마다 같은 장면이 움직이는 미리보기, 실사 색보정은 같은 클립에 보정을 바꾼 실제 화면, 삽화는 예시 그림):
   ```bash
   python -m ytflow looks --gallery <스크래치>/looks.html
   ```
2. Artifact 도구로 **같은 주소**(`GALLERY_URL`)에 다시 올리고(`url` 에 그 주소, 처음 읽지 않았으면 `action: read` 먼저), 사용자에게 링크를 준다. 목록이 바뀌지 않았으면 다시 올리지 않고 `action: open` 만.
3. 터미널에도 한 줄 요약: 화풍 수(모션그래픽·삽화·실사), 삽화 예시가 몇 개 채워졌나, 고르는 법 `python -m ytflow look <프로젝트> --motion <id> --illust <id> --footage <id>`.

## 삽화 예시 그림
- 그림은 `<예시 폴더>/<화풍 id>.png` (PC: `YTFLOW_DRIVE/looks/`, 클라우드: `~/.cache/ytflow/looks/`). 있으면 페이지에 자동으로 들어간다.
- 없는 것만 그리기: 사용자 PC 에서 `python -m ytflow looks --draw codex` (Codex 구독, 무료 길). 클라우드에서는 `--draw manual` 로 주문서(`ORDERS.md`)만 만들고, 필요하면 `inbox/requests/` 로 피클에게 요청.
- **ElevenLabs 로 그림을 만들지 않는다** (2026-11-20 사용자). 유료 그림 생성도 사용자 승인 없이 쓰지 않는다.
- 클라우드 세션은 예시 그림이 캐시에 없을 수 있다 — 그러면 Drive `ytflow/looks/` 에서 받아 `~/.cache/ytflow/looks/` 에 두고 만든다(파일당 10MB 이하). 없으면 '준비 중' 칸으로 두고 그렇다고 말한다.

## 화풍을 더하거나 판정이 바뀌면
`styles/looks.yaml` 에 항목을 더하거나 `status`(approved·trial·available)를 고친 뒤 위 1~2 를 다시 한다. 모션그래픽 화풍은 `skins/<id>/skin.yaml` 도 함께.
