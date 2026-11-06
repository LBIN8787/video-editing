---
name: video-edit
description: 대본과 소스로 음성(TTS/녹음), 장면 화면(카드·애니메이션), 자막(2단·상자형), 가편집 영상을 만들고 프레임을 뽑아 품질을 점검한다. 편집 스타일(styles/<id>)의 렌더러와 설정을 적용한다.
---

# 편집 (voice → assets → subtitles → assemble)

```bash
python -m ytflow stage <프로젝트> voice       # TTS(edge) 또는 03_voice/scene_XXX.wav 녹음 사용. quote 장면은 클립 원음
python -m ytflow stage <프로젝트> assets      # 스타일 렌더러로 장면 화면 생성 + 04_assets/shotlist.csv
python -m ytflow stage <프로젝트> subtitles   # 05_edit/subs.ass(번인) · subs.srt(업로드) · chapters.json
python -m ytflow stage <프로젝트> assemble    # 05_edit/draft.mp4 · timeline.csv → 마스터링 final.mp4
```
assemble 끝에 ffmpeg-skill 로 마스터링합니다(`ytflow/stages/finish.py`): 유튜브 음량 −14 LUFS(`final.mp4`), 유튜브 규격 점검(`delivery_check.json`), 프레임 시트(`final_sheet.png`).
배경음은 `edit.bgm` 에 음원 경로를 주면 내레이션 아래로 자동으로 낮춰 깝니다. 업로드는 `final.mp4` 로 합니다.
```bash
```
- **스타일 적용:** 프로젝트 폴더의 `edit.yaml` 이 `styles/<id>/edit.yaml` 을 따릅니다. `make --style-ref` 가 복사합니다.
- **스타일 바꾸기:** `edit.yaml` 의 내용을 다른 스타일 것으로 바꾸고 assets 부터 다시 돌립니다(음성은 재사용).
- **화면 우선순위:** 직접 넣은 파일(`scene_XXX.png/.mp4`) > 받은 클립 > 카드/애니메이션 > 기사 캡처 > 임시 썸네일 > 자리표시

## 품질 점검 (반드시 직접 본다)
1. **프레임 뽑기:** 장면별로 `05_edit/timeline.json` 의 start + 1.5초 지점 프레임을 뽑습니다.
   `ffmpeg -ss <초> -i 05_edit/draft.mp4 -frames:v 1 -vf scale=640:-1 frame.png`
2. **확인할 것:**
   - 글자가 잘리거나 겹치지 않는가
   - 자막이 화면 요소를 가리지 않는가
   - 애니메이션이 끝까지 그려진 상태로 멈추는가 (장면 끝 0.3초 전 프레임으로 확인)
   - 빠진 글자(□)가 없는가 (폰트에 없는 기호)
   - 스타일 문서(`styles/<id>/STYLE.md`)의 품질 체크리스트
3. **수정:** 문제가 있으면 렌더러(`ytflow/stages/cards.py`, `paper.py`)나 대본을 고치고 해당 단계부터 다시 돌립니다.

## 길이
- **목표:** 목표 분량의 ±15% 안이어야 합니다.
- **짧을 때:** `tts.rate` 를 낮추거나 대본에 근거 장면을 추가합니다.
