# 이 상자는 언제 매출이 될까?

32초짜리 한국어 설명 영상. 고객에게 인도할 때 매출을 인식하는 가상 계약을 다룬다. 상자 세 개의 번호를 포장선, 닫힌 출하문, 트럭, 고객 창고까지 유지하고, 인수증 서명 뒤에 7월 장부에 금액을 찍는다.

- 기준 영상 분석은 [월텍남 모션그래픽 벤치마크](../../docs/31-motion-grammar.md)에 있다.
- 완성본은 Google Drive의 `ytflow/영상/20261120-inventory-motion/inventory-to-revenue.mp4`에 있다. H.264, 1280 × 720, 24 fps, 한국어 내레이션과 자막을 포함한다.
- Windows에서 빈 작업 폴더를 현재 경로로 두고 이 프로젝트에 있는 `voice.py`, `sound.py`, `film.py`를 Python으로 차례로 실행한다. FFmpeg, edge-tts, NumPy, Pillow, OpenCV와 Windows 기본 글꼴을 쓴다. 음성 합성에는 네트워크 연결이 필요하다. `film.py qa`로 주요 화면을 미리 본다.
