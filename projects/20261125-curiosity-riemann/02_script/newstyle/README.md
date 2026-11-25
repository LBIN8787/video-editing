# 리만가설 편 — 새 스타일(HyperFrames) 생성기

- 바탕·색·카메라: 샘플 SPEC(`../../../20261125-issues-explainer/02_script/newstyle_sample/SPEC.md`)과 같음
- **선은 천천히 그려짐** (2026-11-25 사용자: "한번에 찍 선이 그어지는게 아니라 천천히 나타나는 그려지는 연출"): 모든 선·축·곡선은 펜 끝 점(MotionPathPlugin)이 따라가며 문장 길이만큼 그려짐(`Scene.pen`), 글자는 왼쪽부터 써 내려감(`Scene.write`)
- 실제 값: 소수 개수 계단(직접 계산), 로그 적분 곡선(직접 계산), 제타 영점 허수부 14.135 … 49.774(널리 알려진 값)
- 코드 화면은 '예시 화면 · 실제 증명 코드 아님' 표시
- 다시 만들기 (작업 폴더 E:\ytflow-local\hf-riemann): 목소리 l00~l53.mp3(edge-tts InJoon -4%) → `python build.py` → `npx hyperframes check` → `npx hyperframes render -o renders/riemann_v1.mp4 --quality delivery`
- 자막: 문장 하나를 말하는 동안 통째로(비례 분할 없음), 길면 두 줄

## 고친 것 (2026-11-25)
- 선 그리기를 `strokeDashoffset`(pathLength=1) 대신 GSAP **DrawSVGPlugin**(`drawSVG: "0%" → "100%"`)으로. 이전 방식은 렌더러가 한 프레임씩 멈춰 찍을 때 그리는 도중의 선이 보이지 않고 끝에 한꺼번에 나타났음 — 사용자의 "그래프가 한 번에 찍 그어진다"의 원인. 펜 끝 점만 움직이고 선은 없던 프레임을 정지 화면으로 확인함.
