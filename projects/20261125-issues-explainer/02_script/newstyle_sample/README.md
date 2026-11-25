# 새 스타일 샘플 (D3) — 시사 편 1장, HyperFrames

v1(설명 무대 카드)이 기각된 뒤(사용자 11-25 "기존 편집방식과 다르지 않은거같아요 글로 설명하은 느낌이 강하다") 만든 51초 샘플.
레퍼런스: 딥텔러(docs/69) — 밝은 종이 바닥 위 큰 사물·큰 타이포·실제 문서, 주황 한 색, 끊임없는 느린 카메라.

- `SPEC.md` 화면 규칙(숫자로) · `build.py` 장면 생성기(→ index.html + compositions/a~f.html) · `lines.json` 문장별 목소리 길이
- 다시 만들기 (작업 폴더 E:\ytflow-local\hf-sample-issues): 목소리 l00~l08.mp3(edge-tts ko-KR-InJoonNeural -4%) → `python build.py` → `npx hyperframes check` → `npx hyperframes render -o renders/sample_new_style.mp4 --quality delivery`
- 글꼴 Noto Sans KR(OFL) · 효과음 media-use 스킬 묶음(Pixabay 라이선스) · GSAP 로컬 파일
- 측정: 정지 비율 0.34(v1 0.73), 가장 긴 정지 5.8초(8-K 문서 읽기)
