# 20261114-cloud-test — 클라우드 렌더링 시험작 (약 40초)

키 없는 리눅스 환경에서 이 저장소의 렌더 경로가 끝까지 도는지 확인하는 시험편입니다. 유튜브 업로드 없음, `main` 무관.

- 편집 스타일: `paper` (미주일기 인포그래픽 렌더러 — 카드는 PIL, 자막은 libass, 폰트는 `ytflow/assets/fonts/` 동봉 나눔)
- 목소리: `edge-tts` (ko-KR-InJoonNeural, rate +8%) — 유료 키 불필요
- 화면: 카드 10장 (외부 영상·사진 0장, 유튜브 다운로드 없음)
- 마스터링: ffmpeg-skill `loudness.py`(2패스, -14 LUFS) → `check.py`(유튜브 규격) → `look.py`(프레임 시트)
- 대본 LLM: `YTFLOW_LLM_BACKEND=manual` (에이전트가 직접 작성 → `.llm/` 요청 없음)

## 다시 만들기
```bash
pip install -r requirements.txt && pip install numpy Pillow fonttools
python scripts/install_tools.py                 # 또는 ffmpeg-skill 만: tools/ffmpeg-skill (고정 커밋 2d9f5ac)
python -m ytflow validate projects/20261114-cloud-test
for s in voice assets subtitles assemble report; do python -m ytflow stage projects/20261114-cloud-test $s; done
```
결과: `05_edit/final.mp4` · `05_edit/final_sheet.png` · `05_edit/delivery_check.json` · `05_edit/subs.srt` · `REPORT.md`

## 이번 시험에서 확인한 것 (2026-11-14, 리눅스 컨테이너)
- 길이 39.7초 · 1920x1080 · 30fps · h264 · AAC 48kHz · **-14.0 LUFS** · true peak -2.4 dBTP · 5.9MB
- `delivery_check.json`: 실패 0, 경고 1(자막 트랙을 따로 넣지 않고 화면에 굽는 방식이라 `subtitles: none`) — 의도된 경고
- `layout_qa.json` 비어 있음(겹침 0) · 나눔 폰트로 □ 글자 없음
