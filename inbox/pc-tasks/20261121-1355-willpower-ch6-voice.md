---
from: claude-code
type: render-sample
project: 20261121-curiosity-willpower
status: done
---

의지력 편 6장 D3 샘플에 ElevenLabs 음성을 붙여 주세요. 클라우드는 elevenlabsusercontent.com 다운로드가 프록시에서 막힙니다(403).

음성: ElevenLabs Nobel Butler, eleven_v4, take 1 (generation `oErb9yIBJ2S7mfmo3YNx`, 117.44초). ElevenLabs 웹 기록(Text to Speech 기록) 또는 flow `wX73J0zv3tgB6c34ue7b` 에서 mp3 를 받으세요.

```
git pull
pip install playwright && python -m playwright install chromium   # 처음 한 번
python projects/20261121-curiosity-willpower/02_script/render_ch6.py <출력>/ch6_sample.mp4 <받은>/ch6_take1.mp3
#   음성이 있으면 문단 사이 쉼으로 박자 시각을 다시 맞춤 → 05_edit/ch6_timing.json
#   확인: 자막·화면이 말과 맞는지 직접 보기(06 EYE), 음량
```
결과 mp4 는 Drive(`YTFLOW_DRIVE`), Git 에는 `05_edit/ch6_timing.json` 만 커밋. 사용자 D3 검토용.


## 처리 (2026-11-22 호기심 정기 작업)
- 해당 없음으로 닫음: 의지력 편은 v16 최종본(ElevenLabs 전체 음성)으로 통과해 2026-11-22 18:00 공개 예약됨 — 6장 D3 샘플은 더 필요 없음.
