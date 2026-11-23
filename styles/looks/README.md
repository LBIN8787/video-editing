# 자주 쓰는 화풍 — 만드는 법 (2026-11-20, 승인된 10가지)

> 사용자: "왜냐하면 예시로 이런거는 저 예시사진으로는 다 안보이잖아" · "일단은 자주 쓰는 스타일과 화풍부터 해줘"
> 목록·고르기는 `styles/looks.yaml` · `python -m ytflow look <프로젝트> --set motion=<id> --set illust=<id> --set footage=<id>` (→ `edit.yaml` 의 `look`).
> **움직이는 미리보기**: 화풍 목록 페이지(`skills/looks-gallery`, 같은 장면이 화풍마다 어떻게 움직이는지) · 장면별 움직임은 `styles/hybrid/scenes/`.

화풍(어떻게 보이나)과 장면·연출(어떻게 움직이나)은 다른 축입니다 — 같은 `bars` 장면이 화풍만 바꾸면 전혀 다르게 보입니다. 아래는 화풍마다 **무엇이 바뀌고, 어떻게 켜고, 무엇을 준비하나**.

## 1. 모션그래픽 화풍 — 그래픽 스킨을 갈아 끼움 (`look.motion`)
켜는 법: `look --set motion=<id>` → 렌더 때 `skins/<id>/skin.yaml`(색·글꼴·바탕·선 질감)이 모든 그래픽 장면에 적용. 장면 하나만 바꾸려면 그 장면에 `"skin": "<id>"`. 준비물 없음(코드가 그림).

| id | 이름 | 언제 | 피할 때 | 움직이는 예시 |
|---|---|---|---|---|
| `clean-flat` | 평면 인포그래픽 | 숫자·비교·과정, 시장 기본 | 감정·회상 | 화풍 목록 페이지 |
| `chalkboard` | 칠판 | 원리·과정·구조 (호기심) | 관계도·숫자 비교, 너무 자주 | 화풍 목록 페이지 |
| `corkboard` | 증거판 | 누가 누구와 연결 (시사) — `map_causal` 과 짝 | 숫자 비교 | [map_causal.mp4](https://drive.google.com/file/d/15-88mqDELcl3jkfHOidgv6lyztGGDkyk/view) (`look: board`) |
| `dark-doc` | 어두운 다큐 | 원본 영상·발언 사이의 정리 화면, 역사·위기 | 밝은 생활 정보 | [bars.mp4](https://drive.google.com/file/d/1pnlWsrvCke45fr1kE6UkvVUm9OVZFfxx/view) · [versus.mp4](https://drive.google.com/file/d/1uze0c79ORRf8IRmXsjG541SM-n_fSjn9/view) |
| `footage-overlay` | 실사 위 그래픽 | 실제 자료 영상 위 이름표·막대·핵심어 | 그래픽이 실사를 덮을 때(패널은 화면 절반 이하) | 예시 프로젝트 `20261120-curiosity-broll-sample` |

(참고: `newsprint` 는 '사용 가능' 단계 — 11/20 심층의 `checklist` 가 이 스킨: [checklist.mp4](https://drive.google.com/file/d/1WB0v-x5RTestBbb7_GtmIbfVX0XSvXyf/view))

## 2. 삽화 화풍 — 원화를 그려 층으로 움직임 (`look.illust`)
켜는 법: `look --set illust=<id>` → `art-gen`/`looks --draw` 가 `styles/looks.yaml` 의 `prompt` 로 원화를 그림(PC: Codex 구독·Gemini, 클라우드는 주문서). 움직임은 공통 순서(`docs/44`): 원화 → 층 분리 → 장면 HTML → 렌더 → 정지 화면 묶음 확인. 한 편 안에서 인물·색을 유지(05 §0-8). 삽화는 실사·모션그래픽으로 어려운 박자에만(04 §0-8).

| id | 이름 | 언제 | 피할 때 | 준비물 |
|---|---|---|---|---|
| `casual-cel` | 캐주얼 셀 애니메이션 | 일상·기억·회상, 인물의 감정 | 정밀한 수치·기계 구조 | 원화 + 인물 자세 몇 장(움직임은 자세 바꾸기·층 이동, docs/45 §3) |
| `editorial-ink` | 시사 지면 삽화 | 기관·도시·산업, 실제 장소 | 감정 코미디 | 장소 원화(실제 장소와 다르면 '재구성 삽화' 표시) |
| `mint-flat` | 민트 플랫 제품 일러스트 | 앱·결제·권한 같은 제품 설명 (AI) | 역사·감정 | 손·기기 원화, 화면 부분은 실제 캡처로 바꿔 끼울 수 있게 |
| `doc-collage` | 실제 자료 콜라주 | 증거·인용·날짜 | 이야기 몰입 구간 | 그리지 않음 — 원문·사진 캡처(출처·라이선스) 위에 형광펜·표시 (`hand-annotate`·`zoomshot`) |

## 3. 실사 색보정 (`look.footage`)
켜는 법: `look --set footage=<id>` → 렌더 때 모든 실사 클립에 같은 ffmpeg 필터(`vf`)를 걸어 한 영상처럼 묶음. 준비물: 클립과 출처·라이선스 기록(`04_assets/clips.md`).

| id | 이름 | 언제 | 필터 |
|---|---|---|---|
| `warm-doc` | 따뜻한 다큐 | 생활·심리·호기심 (기본) | 채도 조금 낮춤 · 따뜻한 중간톤 · 비네트 · 옅은 입자 (`styles/looks.yaml` 의 `vf`) |

## 다음에 채울 것
- 삽화 화풍의 **움직이는 예시**: 실제 편에 쓴 완성본이 생기면 그 구간을 잘라 Drive `ytflow/style-examples/` 에.
- 시험(trial) 단계 화풍(귀여운 캐주얼·플랫 벡터·2.5D 미니어처)은 쓰기로 정해지면 같은 틀로.
