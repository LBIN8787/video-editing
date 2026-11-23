# 2026-11-11 네 채널 회차 — 대본·팩트시트 생성 스크립트

`projects/20261111-*` 의 `topic_brief.json`·`factsheet.md`·`02_script/hybrid.json`·자료 화면을 만든 스크립트입니다 (다시 만들기·참고용).
NASA 사진은 `common.py` 의 `NASA` 폴더에 미리 받아 두어야 합니다 (images-api.nasa.gov, 퍼블릭 도메인).

```bash
cd scripts/episodes_20261111 && python3 issues.py && python3 curiosity.py && python3 market.py && python3 ai.py
python -m ytflow hybrid 20261111-issues-aiglasses   # 프로젝트마다
```
