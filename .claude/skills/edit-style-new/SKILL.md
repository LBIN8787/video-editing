---
name: edit-style-new
description: 레퍼런스 유튜브 영상 파일로 새 편집 스타일을 분석해 스타일 라이브러리(styles/<id>/)에 추가한다. 컷 리듬·화면 변화·팔레트·자막·배경음악을 측정하고, 장면 미리보기로 편집 규칙을 정리하고, 렌더러 설정과 문서를 만든다.
---

# 새 편집 스타일 추가

## 1. 레퍼런스 준비
- 사용자가 내려받은 영상 파일(가능하면 720p 이상, 1편 이상)을 받습니다. 채널 이름과 영상 URL 을 기록합니다.
- 파일은 저장소 밖이나 `styles/<id>/work/`(커밋 제외)에 둡니다.

## 2. 측정·해석
```bash
python -m ytflow style <id> ref1.mp4 [ref2.mp4 ...] --title "<채널 이름>"
```
| 생성 파일 | 내용 |
|---|---|
| `styles/<id>/metrics.json` | 하드 컷/분, 화면 변화/분, 정지 비율, 밝은/어두운 비율, 팔레트, 자막 상자, 배경음악 |
| `styles/<id>/rules.json` | 장면 시트를 보고 정리한 규칙 (배경, 배치, 움직임, 반복 요소, 글꼴, 자막, 소리, 렌더러가 못 하는 것) |
| `styles/<id>/edit.yaml` | 렌더러 선택 + 측정한 색·속도 |
| `styles/<id>/STYLE.md`, `script.md` | 초안 (이미 있으면 덮어쓰지 않음) |

manual 백엔드라면 `rules.json` 요청이 `.llm/requests/` 에 남습니다. `styles/<id>/work/` 의 sheet·motion 이미지를 직접 보고 답을 씁니다(`schemas/style_rules.schema.json`).

## 3. 사람처럼 검토하기
1. `styles/<id>/work/sheet_*.png`, `motion_*.png` 를 직접 보고 STYLE.md 의 '화면 문법'을 관찰한 사실로 다듬습니다. 추정은 '추정'이라고 표시합니다.
2. 측정값을 다시 확인합니다. 예: 자막 상자 비율이 0이면 감지 실패일 수 있으니 프레임을 보고 확인합니다.
3. `script.md` 에 이 스타일의 장면 비율, 장면 길이, 고정 장면을 적습니다.
4. STYLE.md 의 '구현 상태' 표에 지금 렌더러로 되는 것과 안 되는 것을 나눕니다.

## 4. 렌더러 정하기
- **기존 렌더러로 충분하면:** `edit.yaml` 의 `style: sixsigma | paper` 와 색·속도만 바꿉니다.
- **새 렌더러가 필요하면** `ytflow/stages/<renderer>.py` 를 만듭니다.
  - 인터페이스: `render_card(card, out_mp4_or_png, duration, seed)`, `render_paste(image, out, duration, caption, seed)`, `render_placeholder(out, duration, note, seed)`
  - 연결: `media.assets()` 와 `media.subtitles()` 에서 `edit.style` 로 분기합니다.
  - 카드 스키마(number_compare / flow / table / bars / headline / text)는 모든 렌더러가 공통으로 따릅니다.

## 5. 확인과 등록
1. **시험 렌더링:** 기존 프로젝트를 복사하고 `edit.yaml` 을 새 스타일로 바꾼 뒤 `assets → subtitles → assemble` 을 돌립니다. 프레임을 뽑아 레퍼런스 시트와 나란히 비교합니다.
2. **등록:** STYLE.md 의 `status` 를 `reviewed` 로 바꾸고, `styles/README.md` 표에 줄을 추가합니다.
3. **스킬 추가:** `skills/edit-style-<id>/SKILL.md` 를 만든 뒤 `python scripts/sync_skills.py` 를 실행합니다.

## 지킬 것
- 레퍼런스의 대사, 고유 캐릭터, 로고, 썸네일을 복제하지 않습니다. 구조와 기법만 가져옵니다.
- 레퍼런스 프레임과 영상은 저장소에 올리지 않습니다(`styles/**/work/` 는 .gitignore).
