---
from: claude-code
type: clip-fetch
project: 20261120-market-deep-druckenmiller
status: pending
---

드러켄밀러 인물 인사이트 편(샘플)의 원본 발언 구간을 PC 에서 찾아 받아 주세요 (docs/50-clip-lane.md). 클라우드는 유튜브 봇 확인 때문에 자막·구간을 받지 못합니다.

원본: iConnections 공식 채널 "Stan Druckenmiller: Why He's "Not Playing" Right Now | TomorrowX Summit" https://www.youtube.com/watch?v=6r3D-CMJkuI (1417초)

1) 자막만 받아 아래 문장의 시각을 찾기 (영상 전체는 받지 않음)
```
yt-dlp --cookies-from-browser <브라우저> --skip-download --write-auto-subs --sub-langs en --sub-format vtt -o druck https://www.youtube.com/watch?v=6r3D-CMJkuI
```
| 장면 | 찾을 문장 (보도 인용 — 실제 말과 조금 다를 수 있음) |
|---|---|
| bite 1 | We're trying to not lose money, as opposed to make money. |
| bite 2 | I'm really alert to the fact that the second half of '27 could be economically disappointing |
| bite 3 | I'm just taking a break, which could last two days or six months. |

2) 문장 앞뒤 0.5초 여유로 각 20초 이내 구간을 `projects/20261120-market-deep-druckenmiller/02_script/hybrid.json` 의 `footage.druck` 에 넣기.
   한 원본에 구간이 셋이라 `druck1`·`druck2`·`druck3` 세 키로 나누고(같은 url, 각자 start·end·file), 각 bite 장면의 `clip.src` 를 맞춰 바꿉니다. 실제 말이 인용과 다르면 `find`·`ko` 를 실제 말로 고칩니다.
   번역본 요지(팩트시트 S7: '토큰이 아니라 일을 판다', 신용 스프레드, 정치·자금 위험)도 자막에서 원문을 찾으면 팩트시트에 원문을 적고 ⚠️ → ✅ 로.

3) 받고 다시 렌더
```
python -m ytflow clip-order 20261120-market-deep-druckenmiller
python -m ytflow clip-fetch 20261120-market-deep-druckenmiller
python -m ytflow hybrid 20261120-market-deep-druckenmiller
```

끝나면 status 를 done 으로 바꾸고 결과(찾은 시각·받은 파일·실패 이유)를 적어 주세요.
