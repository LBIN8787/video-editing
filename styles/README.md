# 편집 스타일 라이브러리

스타일 하나는 폴더 하나입니다. 어떤 에이전트(Claude Code, Codex)든 같은 파일을 읽고 같은 결과를 냅니다.

| id | 이름 | 렌더러 | 상태 | 쓰는 곳 |
|---|---|---|---|---|
| `sixsigma` | 식스시그마 | sixsigma | reviewed | 기업·투자 뉴스 해설 (원본 발언 + 검은 카드) |
| `mijudiary` | 미주일기 | paper | reviewed | 개념·원리·역사 해설 (종이 콜라주 + 손그림 애니메이션) |

## 폴더 구성
| 파일 | 역할 | 만드는 방법 |
|---|---|---|
| `STYLE.md` | 스타일 문서: 화면 문법, 구현 상태, 체크리스트 | `ytflow style` 이 초안을 쓰고 사람이 다듬음 |
| `edit.yaml` | 렌더러 설정: 색, 속도, 자막 방식 | `ytflow style` 측정값으로 자동 생성 |
| `script.md` | 이 스타일로 대본을 쓸 때 추가 규칙 | 초안 자동 생성 후 사람이 다듬음 |
| `rules.json` / `metrics.json` | 분석 원자료 | `ytflow style` |
| `work/` | 장면 미리보기 이미지 | 타 채널 화면이라 저장소에 올리지 않음 |

## 쓰는 법
```bash
python -m ytflow styles                                         # 목록
python -m ytflow make --style-ref mijudiary                     # 이 스타일로 영상 제작
python -m ytflow style <id> ref1.mp4 ref2.mp4 --title <이름>    # 새 스타일 추가
```
새 스타일을 추가하는 절차는 `skills/edit-style-new/SKILL.md` 에 있습니다.
