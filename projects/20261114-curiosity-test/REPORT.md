# 제작 보고서 — 비행기 창가의 작은 구멍 (2분 완성판, v2)

- 프로젝트: `20261114-curiosity-test` · 브랜치: `exp/cloud-render-test` (`main` 무관, 업로드 없음)
- 길이 **2분 04초(123.95초)** · 1920×1080 · 30fps · h264 + AAC 48kHz 2ch · **-14.0 LUFS** · true peak -2.4 dBTP · 32.0 MB
- 장면 19개 · 말소리 112.85초 + 장면 사이 숨 고르기 **11.10초**(장면마다 0.5~0.8초)
- 납품물: `downloads/curiosity-gpt-v2/` (final.mp4 · final_sheet.png · delivery_check.json · sync_qa.json · frames 8장 · art 11장 · REPORT.md)

## 이번(v2)에서 바꾼 것 — 지적 세 가지에 대한 답

| 지적 | v1 | v2 |
|---|---|---|
| **영상 템포가 너무 빠르고 내용이 짧다** | 46.29초 · TTS `+8%` · 장면 사이 0.12초 | **123.95초** · TTS **`+0%`** (자연 속도) · 장면 사이 **0.5~0.8초** 숨 고르기 (장면당 `gap`, `scenes.json` 이 유일한 출처) |
| **중간중간 그림체가 휙 바뀐다** | 단면 도해·기압 막대·벽/지름길이 **Pillow 벡터** | 그 세 장면을 모두 **같은 ChatGPT 대화에서 이어 그린 일러스트**로 교체. 남은 벡터는 '빨간 펜 동그라미·화살표·점선·손글씨 이름표' 같은 **주석**뿐 |
| **내용 보강(확인된 사실만)** | 세 겹·구멍·0.23/0.75기압·FAA·김 서림 | + 코멘트 역사(1954 코멧 네모난 창) + 스트레치드 아크릴 + 구멍이 막혔을 때(김 서림 → 봉(seal)이 먼저 지침) |
| **(추가 지시) 인사말 없이, 미주일기처럼 담백하게** | "안녕하세요. … 이야기입니다." | **인트로 인사 삭제** — 첫 문장부터 창가 자리 이야기. `~죠 / ~고요 / ~습니다` 섞은 구어체, 문장 짧게, 지식은 이야기 안에서 자연스럽게 |

## 2. 자료조사 (팩트시트)

기준 시각: 2026-11-14 KST · 확인 상태: ✅ 1차 출처 확인 / ⚠️ 재확인 필요 / ❌ 쓰지 않음

### 1. 창은 세 겹 (사실)
- ✅ 여압 여객기 창은 보통 세 겹: **바깥 창(주 하중 창, main load bearing pane) · 가운데 창(예비 창, fail-safe pane) · 기내 쪽 안쪽 창(scratch pane, 구조 아님)**.
  - FAA AC 25.775-1 (2003-01-17), §6: "Cabin window designs are typically multi-paned construction consisting of two structural panes (a main load bearing pane and a fail-safe pane), inner facing panes…" + "The designs with the structural panes separated by an air gap usually are such that the fail-safe pane is not loaded unless the main pane has failed."
  - https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_25_775-1.pdf
- ✅ 재질은 유리가 아니라 아크릴(PMMA)·스트레치드 아크릴. (AC 25.775-1: "transparent polymeric materials such as polymethyl-methacrylate (acrylic)"; Röhm: 늘인 PMMA 판은 내충격·내화학이 더 좋다)
- ✅ 안쪽 창은 구조 부재가 아니고 바깥 두 창을 긁힘·오염에서 지키는 창(scratch pane). (Slate 2015-05-29 · GKN Aerospace Marlowe Moncur)
- ✅ 두께: 바깥 창 약 0.4인치(≈10mm), 가운데 창 약 0.2인치(≈5mm), 공기층 약 0.25인치. (GKN Aerospace Jason Webb, The Points Guy 경유 — findaflight.eu 정리)

### 2. 구멍은 가운데 창에, 아래쪽에 하나 (사실)
- ✅ 이름은 **breather hole / bleed hole**, **가운데 창 아래쪽에 하나**. (Slate 2015 · Travel + Leisure 2025-08-23: 구멍은 바깥까지 뚫린 것이 아니라 가운데 창에만)
- ✅ 구멍의 일: 기내 공기가 두 창 사이 공기층으로 들어가 **압력이 같아지게** 해, 순항 중 하중을 **바깥 창 하나**가 지게 한다. (Moncur 인터뷰)
- ✅ 두 번째 기능 — 사이 공기의 습기를 빼내 **김 서림·성에**를 막는다. (보잉 Bret Jensen, Slate 2015; 737 정비교범 "preclude fogging and frosting")

### 3. 숫자 (사실 · 비교 기준 포함)
- ✅ 3만 5천 피트에서 밖 약 **3.4 psi(0.23기압)**, 기내 약 **11 psi(0.75기압)** — 약 3.2배. (Gizmodo 2015, 737 정비교범·GKN 인용 / 1 atm = 14.696 psi 환산)
- ✅ 가운데 창은 737 교범상 정상 작동 압력의 **1.5배**를 견디도록 설계(섭씨 70도 기준). (Gizmodo 2015)
- ✅ 가운데 창에 금이 가면 그 비행기는 여압하지 않는다 — "FAIL-SAFE FEATURE HAS BEEN ELIMINATED". (같은 출처)

### 4. 창이 둥글고 아크릴인 까닭 (사실)
- ✅ 1954년, 초기 제트 여객기 **코멧** 사고 조사에서 창 네 귀퉁이에 응력이 몰린 것이 드러났다 — 창가 응력은 극한강도의 **70%** 수준, 이후 여객기 창은 **둥글게** 바뀌었다. (BBC On This Day 1954-10-19 · BBC Future 2017 · RAE Report ARC R&M 3248)
  - ⚠️ 사고 원인은 창 모양 하나가 아니라 **얇은 피부 + 펀치 리벳 + 반복 여압**이 겹친 것 — 본문은 "압력이 네 귀퉁이에 몰렸고, 결국 창가의 금속에 금이 갔다"까지만 말한다.

### 5. 구멍이 막히면 (사실)
- ✅ 가장 먼저 **김 서림**으로 시야가 나빠진다(비상 탈출 때 승무원·구조대가 안을 확인하기 어려움).
- ✅ 오래 두면 **공기 누설이 더 일찍 생겨 창 수명이 줄어든다**(seal 피로). 구조 엔지니어 Wayne Maltry, RD.com 2025-06-29 갱신.
  - https://www.rd.com/article/little-holes-in-airplane-windows/
- ✅ 구멍은 '압력을 조절'하는 밸브가 아니라 **하중이 걸리는 속도**를 조절한다 (Maltry: "regulate the rate of air pressure loading"). 본문은 "사이 틈의 압력이 기내와 같아진다"까지만 말한다.

### ❌ 쓰지 않는 것
- "구멍이 없으면 창이 터진다" — 확인된 자료 없음(막히면 김 서림·seal 수명 저하가 먼저).
- "구멍으로 숨을 쉰다 / 기내 산소가 샌다" — 구멍은 바깥까지 뚫려 있지 않다(T+L 2025).
- "모든 비행기가 똑같다" — 창 설계는 기종마다 다를 수 있다(2겹·4겹도 있음). 본문은 "보통 세 겹"으로 말한다.
- 구멍 지름(2~3mm) — 2차 블로그만 있어 수치를 말하지 않는다.

### 출처 목록 (설명란용)
- S1 FAA AC 25.775-1 "Windows and Windshields" (2003-01-17) — https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_25_775-1.pdf
- S2 Slate, Mark Vanhoenacker (2015-05-29) — GKN Aerospace Marlowe Moncur · Boeing Bret Jensen 인터뷰 — https://slate.com/human-interest/2015/05/whats-that-thing-why-are-there-holes-in-airplane-windows.html
- S3 Gizmodo, Robbie Gonzalez (2015-05-11) — 보잉 737 정비교범 인용 — https://gizmodo.com/why-is-there-a-hole-in-airplane-windows-1703660371
- S4 Travel + Leisure (2025-08-23) — https://www.travelandleisure.com/why-airplane-windows-have-holes-11755762
- S5 Reader's Digest (2025-06-29 갱신) — Wayne Maltry 인터뷰 — https://www.rd.com/article/little-holes-in-airplane-windows/
- S6 BBC On This Day, 1954-10-19 "Metal fatigue caused Comet crashes" — http://news.bbc.co.uk/onthisday/hi/dates/stories/october/19/newsid_3112000/3112466.stm
- S7 BBC Future (2017-04-04) "The British airliner that changed the world" — https://www.bbc.com/future/article/20170404-the-british-airliner-that-changed-the-world
- S8 서스캐차원 항공 구조 자료(코멧 응력 43,100 psi·극한강도 70%) — Cranfield/RAE ARC R&M 3248 PDF
- S9 findaflight.eu "The Science Behind Aircraft Cabin Windows" (GKN Jason Webb 두께 인터뷰 정리)

## 3. 대본 (19장면 · 2분 04초)

| # | 구간 | 내레이션 | 화면 |
|---|---|---|---|
| 1 | hook | 비행기 창가 자리에 앉으면, 창틀 아래쪽에 작은 구멍이 하나 있습니다. | 창 안쪽 클로즈업 + 빨간 동그라미 '여기' |
| 2 | hook | 처음 보면 좀 이상합니다. 유리에 왜 구멍을 뚫어 놨을까 싶죠. | 같은 창 + 큰 물음표 |
| 3 | hook | 이 구멍에는 이름이 있습니다. 브리더 홀, 우리말로는 숨구멍입니다. | 구멍 + 이름표 '브리더 홀' |
| 4 | body-1 | 답은 창을 옆에서 보면 보입니다. 창은 유리 한 장이 아니라, 세 겹입니다. | 세 겹 단면 일러스트 등장, '세 겹' |
| 5 | body-1 | 바깥 창, 가운데 창, 안쪽 창. 바깥 창이 가장 두껍고, 가운데 창은 그 절반쯤입니다. | 단면 + 이름표 3개(지시선) |
| 6 | body-1 | 손으로 만질 수 있는 건 안쪽 창인데요. 이건 힘을 받지 않습니다. 다른 두 창이 긁히지 않게 막아 주는 역할이죠. | 안쪽 창 확대 + '힘은 안 받는다 / 긁힘만 막는다' |
| 7 | body-1 | 그런데 구멍은 바깥 창이 아니라, 가운데 창 아래쪽에 뚫려 있습니다. | 단면 아래쪽 확대, 구멍 동그라미, 바깥 창 X |
| 8 | body-2 | 비행기가 3만 5천 피트를 날 때, 밖의 공기는 0.23기압쯤입니다. 기내는 0.75기압 정도로 맞춰 두고요. | 기내가 열린 여객기 단면 + '35,000 ft' · '밖 0.23기압' · '기내 0.75기압' |
| 9 | body-2 | 기내 공기가 그 구멍으로 스며들면, 두 창 사이 틈도 기내와 같은 압력이 됩니다. | 단면: 구멍으로 들어오는 화살표 + 사이 틈 형광펜 |
| 10 | body-2 | 그러면 3만 5천 피트의 압력은 바깥 창 하나가 혼자 견디게 됩니다. | 바깥 창에 빨간 화살표 3개 + '힘은 여기로' |
| 11 | body-2 | 구멍은 압력이 지나가는 지름길인 셈입니다. | 돌벽·작은 나무 문 일러스트, 돌아가는 점선 X, 문으로 빨간 화살표 |
| 12 | body-3 | 가운데 창은 그동안 아무 일도 하지 않는 예비 선수입니다. 바깥 창이 깨지는 일은 거의 없지만, 그런 일이 생기면 바로 이어받죠. | 창 + 벤치의 예비 선수, '예비 선수' |
| 13 | body-3 | 2003년 미국 연방항공청 지침에도, 이 구조를 주 하중 창과 예비 창으로 나눠 적어 두었습니다. | 바랜 종이 문서 AC 25.775-1, 형광펜 두 문구, '2003 · FAA' |
| 14 | body-4 | 창이 둥근 것도 이 이야기와 이어집니다. 1954년, 초기 제트 여객기 코멧은 네모난 창을 달았습니다. | 1950년대 제트 여객기 + 네모난 창 동그라미, '1954' |
| 15 | body-4 | 압력이 창의 네 귀퉁이에 몰렸고, 결국 창가의 금속에 금이 갔습니다. | 그 창으로 확대, 펜으로 그은 금 |
| 16 | body-4 | 그 뒤로 여객기의 창은 둥글어졌습니다. 재질도 유리가 아니라, 늘여 만든 아크릴이고요. | 둥근 창 + 두꺼운 아크릴 판, '스트레치드 아크릴' |
| 17 | body-5 | 구멍이 막히면 어떻게 될까요. 먼저 창이 뿌옇게 서립니다. | 김 서린 창 / 구멍 있어 맑은 창 나란히 |
| 18 | body-5 | 오래 두면 압력이 새는 틈이 더 일찍 생긴다고 합니다. | 김 서린 창으로 확대, '봉이 먼저 지친다' |
| 19 | outro | 그러니까 다음에 창가에 앉거든, 그 구멍을 한 번 보세요. 창이 버티는 이유가 거기 있습니다. | 창가의 여행자 + 창, 구멍 동그라미 |

## 4. 그림 — 한 대화에서 이어 그린 일러스트로 통일

- 사용 계정: `s99078634@gmail.com` (브라우저에 로그인되어 있음) · 대화 `https://chatgpt.com/c/6af7ee3a-ba8c-83ec-a206-55bc82da427d`
- v1에 있던 6조각(창가의 여행자 · 창 구멍 클로즈업 · 여객기 · 벤치의 예비 선수 · 김 서림 비교)은 그대로 쓰고, **같은 대화에서 4번 더 그려** 5조각을 새로 만들었다(그중 1장은 두 그림이 한 장에 있어 잘라 씀):

| 그림 | 쓰는 장면 | 원본 |
|---|---|---|
| 세 겹 창 단면(정면·직각, 원근 없음) | 4·5·6·7·9·10 | `section.png` |
| 기내가 열린 여객기 단면(사람·구름) | 8 | `cabin.png` |
| 돌벽과 작은 나무 문, 문으로 빠져나가는 바람 | 11 | `gate.png` |
| 1950년대 초기 제트 여객기(네모난 창) | 14·15 | `era_sheet.png` 왼쪽 |
| 구멍 뚫린 두꺼운 아크릴 창 한 장 | 16 | `era_sheet.png` 오른쪽 |

- 프롬프트 원칙: 같은 대화에서 "Same illustration style, ○번째 separate image"로 이어 그림체 고정 · **흰 배경(#FFFFFF)** · **글자·숫자·화살표·라벨 없음** → 한글 이름표·빨간 펜 표시는 렌더러가 위에 얹는다.
- 오리기: 테두리와 이어진 흰색만 플러드필로 지우고 1px 페더 → 투명 PNG(`build/art_assets.py`). 벤치 다리 사이처럼 **그림 안에 갇힌 흰 바탕**은 `fill_enclosed` 로 따로 지운다(v2 추가).
- 좌표: 그림 안의 지점(구멍·창·틈)을 `build/board_spec.py` 의 `Placed.p(u,v)` 로 그림판 좌표로 바꿔 이름표·동그라미를 붙인다 — 그림을 옮겨도 표시가 따라간다.
- **벡터 도해 제거**: v1의 `section`(벡터 단면)·`bars`(기압 막대)·`wall`(지름길 벽) 아이템은 v2 대본에서 쓰지 않는다. 화면에 남는 벡터는 펜 주석(동그라미·화살표·점선·형광펜·손글씨)과 '바랜 종이 문서' 카드뿐.

## 5. 렌더 경로 (이번에 실제로 돈 것)

| 단계 | 실제로 돈 것 |
|---|---|
| 대본 | 에이전트 직접 작성 → `02_script/scenes.json` (gap 포함) |
| 그림판 | `build/board_spec.py` → `02_script/board.json` → `build/board.py`(Pillow, 3840×2160 그림판 + 카메라) |
| 목소리 | `build/tts_timed.py` — edge-tts `ko-KR-InJoonNeural` **+0%**, 무음 정리(0.55초 넘는 침묵만 0.36초로), faster-whisper `base` 로 단어 시각 |
| 자막 | `build/subs_timed.py` — 단어 시각으로 줄 시각. **한 겹 상자 자막(SubOne)** — 두 겹(상자용+글자용)으로 그리면 libass 가 두 줄로 밀어내 상자와 글자가 어긋난다(v2에서 고침) |
| 타임라인 | `build/timeline.py` — 장면 길이 = 말소리 + gap → `05_edit/timeline.json` |
| 가편집·마스터링 | `python -m ytflow stage 20261114-curiosity-test assemble` → `finish.master` (-14 LUFS · check.py · final_sheet.png) |
| 싱크 점검 | `build/sync_check.py` — 받아쓰기로 자막−말 시각 실측 → `05_edit/sync_qa.json` |

## 6. 검증 결과 (실측)

- 길이 **123.95초** · 1920×1080 · 30fps · h264 + AAC 48kHz 2ch · **-14.0 LUFS** · true peak **-2.4 dBTP** · 32.0 MB
- `delivery_check.json`: **PASS 11 / WARN 1** — 경고는 자막을 화면에 구워 별도 자막 트랙이 없다는 것(의도)
- `sync_qa.json`: 47줄 · **중앙값 0.03초** · 0.5초 이내 85% · 최대 1.75초
- 장면 19개 전부 같은 일러스트 세계 — 프레임시트(`final_sheet.png`)와 대표 프레임 8장(`frames/`)을 눈으로 확인
- 글자 깨짐(□) 0 — 그림판은 저장소 동봉 나눔(고딕·명조·손글씨), 자막은 나눔고딕
- 남은 흠(알고 있는 것): ① 4·5·9·10장면의 세로로 긴 단면 판이 화면 위쪽에 살짝 붙어 있다(위 48px 여백) ② 12장면 '예비 선수' 손글씨가 소년 머리 옆에 붙어 있다 — 내용·가독성에는 지장 없음

## 7. 지킨 편집 규칙 (manual/reviews.md · manual/04 §0)
- 저음 타격음 없음 — 배경음 자체를 넣지 않았다(`edit.bgm: ""`), 장면 전환음도 없음.
- 마무리 상투구 없음 — 마지막 문장은 첫 질문의 답("창이 버티는 이유가 거기 있습니다").
- 강조 자막은 47줄 중 6줄(세 겹 · 가운데 창 · 0.75기압 · 주 하중 창 · 1954년 · 예비 선수)에만.
- 인사말·자기소개 없이 첫 문장부터 이야기(이번 지시 반영).
- 업로드 없음 · `main` 브랜치 손대지 않음(`manual/04-curiosity.md` 그대로).
