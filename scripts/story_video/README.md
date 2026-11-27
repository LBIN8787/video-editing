# 실화·명작 서사형 영상 렌더 (시험작, 2026-11-27)

1. `art_jobs.py` — 장면 삽화를 사용자 Codex `$imagegen` 으로 (편마다 시대 기록물 화풍 한 가지)
2. `keyframes.py` — 같은 구도의 '전' 그림을 GPT 로 (참조 이미지 `-i`), 말에 맞춰 바뀌는 순간용
3. `voice.py <script.md> <out>` — 무료 edge-tts + 단어 시각 → `narration.wav`, `timeline.json`
4. `render.py <shot_plan.json> [--frames]` — 샷마다 카메라 한 방향(밀기·빼기·이동·멈춤, 사인 가감속, 소수점 이동), 디졸브·페이드·이어 받는 컷, 막 카드, 단어 싱크 자막(한 자막 한 문장), 지도 선·이름표·인용 띠, 날씨·빛(눈·물보라·촛불·안개), 전·후 그림 바꾸기
샷 계획(`projects/*/02_script/shot_plan.json`)의 `why` 에 그 카메라 움직임을 쓴 이유를 적는다. 이유 없는 확대·축소 반복 금지.
그림·소리·영상 파일은 `E:/ytflow-local/books-video/`(작업)·Google Drive `ytflow/영상/ch-books-samples/`(보관), Git 에는 넣지 않음.
