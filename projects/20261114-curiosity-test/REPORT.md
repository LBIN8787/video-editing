# 제작 보고서 — 비행기 창 아래 작은 구멍, 왜 뚫려 있을까? (호기심 이야기 그림판 시험편)

- 프로젝트: `20261114-curiosity-test` · 편집 스타일: **paper** · 길이 약 **0.7분** · 장면 12개
- 화면 구성: card 12
- 가편집: `05_edit/draft.mp4` · 자막: `05_edit/subs.srt` · 타임라인: `05_edit/timeline.csv`
- 실제 소스로 바꿔야 할 장면: **0개**

## 2. 자료조사 (팩트시트)

# 팩트시트 — 비행기 창 아래 작은 구멍 (ch-knowledge · 이야기 그림판 시험편)

기준 시각: 2026-11-14 KST · 확인 상태: ✅ 1차 출처 확인 / ⚠️ 재확인 필요 / ❌ 쓰지 않음

### 1. 창은 세 겹 (사실)
- ✅ 여압 여객기 창은 보통 세 겹: **바깥 창(주 하중 창, main load bearing pane) · 가운데 창(예비 창, fail-safe pane) · 기내 쪽 안쪽 창(scratch pane, 구조 아님)**.
  - FAA AC 25.775-1 (2003-01-17), §6 Introduction: "Cabin window designs are typically multi-paned construction consisting of two structural panes (a main load bearing pane and a fail-safe pane), inner facing panes, protective coatings, and mounting structure." + "The designs with the structural panes separated by an air gap usually are such that the fail-safe pane is not loaded unless the main pane has failed."
  - https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_25_775-1.pdf
- ✅ 재질은 유리가 아니라 아크릴(PMMA)·스트레치드 아크릴. (FAA AC 25.775-1: "transparent polymeric materials such as polymethyl-methacrylate (acrylic)"; GKN Aerospace 설명)
- ✅ 안쪽 창은 구조 부재가 아니고 바깥 두 창을 긁힘·오염에서 지키는 창(scratch pane). (Slate 2015-05-29, GKN Aerospace 기술총괄 Marlowe Moncur 인터뷰)

### 2. 구멍은 가운데 창에, 아래쪽에 하나 (사실)
- ✅ 구멍 이름은 **breather hole / bleed hole**, **가운데 창 아래쪽에 하나**.
  - Slate(2015): "The middle pane (with the breather hole in it)"; Moncur: "[T]he purpose of the small bleed hole in the [middle] pane is to allow pressure to equilibrate between the passenger cabin and the air gap between the panes, so that the cabin pressure during flight is applied to only the outer pane."
  - https://slate.com/human-interest/2015/05/whats-that-thing-why-are-there-holes-in-airplane-windows.html
  - Travel + Leisure(2025-08): 구멍은 한 창에 하나, 아래 가운데, **바깥까지 뚫린 구멍이 아니라 가운데 창에만** 있다.
  - https://www.travelandleisure.com/why-airplane-windows-have-holes-7971824
- ✅ 그래서 정상 운항 중 하중은 바깥 창이 혼자 진다(가운데 창은 예비). (FAA AC 25.775-1 · Moncur)

### 3. 두 번째 기능 — 김 서림·성에 (사실)
- ✅ 구멍은 두 창 **사이 공기의 습기를 빼내** 김 서림·성에를 막는다. 보잉 상용기 엔지니어 Bret Jensen 설명(Slate 2015). 737 정비교범도 두 창·공기층 설계 목적에 "preclude fogging and frosting"를 적어 둠(Gizmodo 2015-05-11).
  - https://gizmodo.com/why-is-there-a-hole-in-airplane-windows-1703660371

### 4. 숫자 (사실 · 비교 기준 포함)
- ✅ 순항 고도 35,000피트에서 **밖 기압 약 3.4 psi(0.23기압), 기내 약 11 psi(0.75기압)** — 약 3.2배.
  - Gizmodo(2015) 737 정비교범·GKN 설명 인용: "at cruising altitudes of around 35,000 feet, atmospheric pressure ... about 3.4 pounds per square inch ... inside the cabin, pressure is artificially maintained at roughly 11 pounds per square inch".
  - 단위 환산: 3.4 psi = 0.231 atm, 11 psi = 0.749 atm (1 atm = 14.696 psi) — 본문은 "0.23기압 / 0.75기압"으로 읽기 쉽게.
- ✅ 가운데 창은 737 교범상 정상 작동 압력의 **1.5배**를 견디도록 설계(섭씨 70도 기준). (Gizmodo 2015 인용)
- ✅ 가운데 창에 금이 가면 그 비행기는 여압하지 않는다 — 교범: "FAIL-SAFE FEATURE HAS BEEN ELIMINATED". (같은 출처)

### 5. 해석 (사실과 구분)
- 사실: 구멍은 가운데 창에 있고, 기내 공기가 두 창 사이 공기층으로 들어가 압력이 바깥 창에만 걸리게 한다.
- 해석(영상의 비유): "구멍은 압력이 지나가는 지름길", "가운데 창은 예비 선수" — 위 사실을 그림으로 옮긴 비유. 사실 주장이 아니다.
- ⚠️ 구조 엔지니어 Wayne Maltry(RD.com 2025)는 "구멍은 기내 압력을 조절하는 게 아니라 창에 걸리는 압력 하중의 '속도'를 조절한다"고 설명 — 영상에서는 "압력이 바깥 창 하나에만 걸린다"까지만 말하고, 압력 '조절'이라고 단정하지 않는다.
  - https://www.rd.com/article/little-holes-in-airplane-windows/

### ❌ 쓰지 않는 것
- "구멍이 없으면 창이 터진다" — 확인된 자료 없음(구멍이 막히면 김 서림·봉(seal) 수명 저하가 먼저). 과장 금지.
- "구멍으로 숨을 쉰다 / 기내 산소가 새어 나간다" — 구멍은 바깥까지 뚫려 있지 않다(T+L 2025).
- "모든 비행기가 똑같다" — 창 설계는 기종마다 다를 수 있음(2겹·4겹 설계도 있음). 본문은 "보통 세 겹"으로 말한다.
- 1900년대 초 무여압기의 창 이야기는 이번 40~50초 편에 넣지 않음(별도 편 주제).

### 출처 목록 (설명란용)
- S1 FAA Advisory Circular AC 25.775-1 "Windows and Windshields" (2003-01-17) — https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_25_775-1.pdf
- S2 Slate, Mark Vanhoenacker, "Why Do Airplane Windows Have Tiny Holes?" (2015-05-29) — GKN Aerospace Marlowe Moncur·Boeing Bret Jensen 인터뷰 — https://slate.com/human-interest/2015/05/whats-that-thing-why-are-there-holes-in-airplane-windows.html
- S3 Gizmodo, Robbie Gonzalez, "Why Is There A Hole In Airplane Windows?" (2015-05-11) — 보잉 737 정비교범 인용 — https://gizmodo.com/why-is-there-a-hole-in-airplane-windows-1703660371
- S4 Travel + Leisure (2025-08-23) — https://www.travelandleisure.com/why-airplane-windows-have-holes-7971824
- S5 Reader's Digest (2025-06-29 갱신) — 구조 엔지니어 Wayne Maltry 인터뷰 — https://www.rd.com/article/little-holes-in-airplane-windows/


## 3. 대본과 소스

| # | 구간 | 내레이션 / 원문 발언 | 화면 | 소스 | 상태 |
|---|---|---|---|---|---|
| 1 | intro | 안녕하세요. 비행기 창 구멍 이야기입니다. | card |  |  |
| 2 | hook | 창가 자리에 앉으면, 창틀 아래 작은 구멍이 보입니다. | card |  |  |
| 3 | body-1 | 유리에 왜 구멍을 뚫어 뒀을까요? | card |  |  |
| 4 | body-1 | 그 창은 유리 한 장이 아니라 세 겹입니다. | card |  |  |
| 5 | body-1 | 구멍은 바깥 창이 아니라, 가운데 창에 있습니다. | card |  |  |
| 6 | body-2 | 3만 5천 피트. 밖은 0.23, 기내는 0.75기압입니다. | card |  |  |
| 7 | body-2 | 기내 공기가 구멍으로 사이에 차면, 압력은 바깥 창에만 걸립니다. | card |  |  |
| 8 | body-2 | 구멍은 압력이 지나가는 지름길인 셈입니다. | card |  |  |
| 9 | body-3 | 그럼 가운데 창은 뭘까요. 예비 선수입니다. 바깥 창이 깨질 때만 나서죠. | card |  |  |
| 10 | body-3 | 2003년 미국 연방항공청 지침도 '주 창과 예비 창'으로 적었습니다. | card |  |  |
| 11 | body-4 | 구멍은 김 서림도 막습니다. 사이 공기 습기가 빠져나가니까요. | card |  |  |
| 12 | outro | 창가에 앉거든 그 구멍을 보세요. 창이 버티는 이유가 거기 있습니다. | card |  |  |

---

## 7. 이번 시험에서 쓴 렌더러 (정확히 무엇이 돌았나)

| 단계 | 표준 경로 | 이번에 실제로 돈 것 |
|---|---|---|
| 대본 | `ytflow script` (LLM) | **에이전트 직접 작성** (`YTFLOW_LLM_BACKEND` 불필요, `.llm/` 요청 없음) → `02_script/scenes.json` |
| 그림 | 호기심 그림판 = `ytflow/stages/story.py` → **HyperFrames(HTML+GSAP) → node + chromium** | **`build/board.py` (Pillow 벡터)** — 이 컨테이너에는 node·chromium·`tools/hyperframes` 가 없어 `story.py` 경로가 실행 불가 | 
| 목소리 | `ytflow stage voice` (edge-tts → 무음 제거·정규화) | **`build/tts_timed.py`** — 같은 edge-tts(ko-KR-InJoonNeural, +8%) + 무음 정리 + **받아쓰기(faster-whisper base)로 단어 시각**까지 저장 |
| 그림 타이밍 | `story.json` 의 `t`(초) | `02_script/board.json` 의 `word` — **그 낱말을 말하는 순간** 그려진다 (`03_voice/timings.json` 의 글자별 시각) |
| 자막 | `ytflow stage subtitles` (장면 길이를 글자 수 비례 배분) | 단계가 만든 스타일 머리글을 그대로 쓰고 줄 시각만 **`build/subs_timed.py`** 로 단어 시각에 다시 박음 |
| 가편집·마스터링 | `ytflow stage assemble` → `finish.master` (loudness -14 LUFS · check.py · look.py) | **그대로 실행** (ffmpeg-skill 고정본 `tools/ffmpeg-skill`) |
| `assets` 단계 | 종이 카드(`paper.py`) 렌더 | **건너뜀** — 이 단계는 `scene_XXX_anim.mp4` 를 지우고 카드로 대체하므로, 그림판 렌더 결과를 직접 `04_assets/scene_XXX_anim.mp4` 로 넣었다. 샷리스트·겹침 점검은 `ytflow qa` 로 대체 |

### 그림판 렌더러(`build/board.py`)가 하는 일
- 그림판 3840×2160(화면 2배) 종이 한 장. 카메라는 `[[초, 중심x, 중심y, 확대], …]` 키프레임 — **장면당 1~2회만** 천천히 움직인다(2026-11-11 "화면이 정신없이 움직임" 기각 반영).
- 매 프레임: 종이 자르기 → 아직 그리는 중인 아이템만 벡터로 얹기 → 2배 슈퍼샘플 → 1920×1080. ffmpeg 로 바로 파이프.
- 아이템: `window`(기내 창) · `hole`(구멍) · `section`(옆에서 본 세 겹 단면 카드) · `figure`(평면 벡터 사람: 몸통·팔·다리, 얼굴 표정 없음) · `plane` · `wall`(벽과 문) · `doc`(규정 문서 + 형광펜) · `bars` · `bench` · `fog` · `crack` · `chip` · `note`(손글씨) · `stamp` · `big` · `arrow` · `path` · `circle` · `cross` · `check` · `credit`.
- 등장은 **선이 그려지듯**(`prog` 로 폴리라인 부분 그리기) 또는 살짝 떠올랐다 안착. 제자리 흔들림 없음.
- 배경은 장면마다 바꿈: 밝은 종이(대부분) · 어두운 종이(#6 숫자) · 모래색(#9 벤치).

### 지킨 편집 규칙 (manual/reviews.md · manual/04 §0)
- 저음 타격음 없음 — 배경음 자체를 넣지 않았다(`edit.bgm: ""`), 장면 전환음도 없음.
- "여기까지가 ~였고요" 같은 마무리 상투구 없음 — 마지막 문장은 첫 질문의 답("창이 버티는 이유가 거기 있습니다").
- 강조 자막은 22줄 중 4줄(가운데 창 · 0.75기압 · 예비 선수 · 2003년)에만.
- 타이틀 화면의 큰 글자가 자막과 같은 문장을 반복하지 않게, 그림판 위 글자는 이름표·수치·손글씨 낱말로만.

## 8. 검증 결과 (실측)
- 길이 **46.29초** · 1920×1080 · 30fps · h264 + AAC 48kHz 2ch · **-14.0 LUFS** · true peak -2.3 dBTP · 11.2MB
- `delivery_check.json`: **PASS 11 / WARN 1** — 경고는 자막을 화면에 구워 별도 자막 트랙이 없다는 것(의도)
- `python -m ytflow qa` → **겹침 없음**
- `sync_qa.json`(받아쓰기로 자막−말 시각 실측): 22줄 · **중앙값 0.05초** · 0.5초 이내 86% · 최대 2.28초.
  크게 어긋난 4줄 중 2줄은 숫자("0.23/0.75")를 받아쓰기가 다르게 적어 **측정값이 튄 것**이고, 2줄은 장면 첫 줄이다.
- 글자 깨짐(□) 0 — 그림판 텍스트는 저장소 동봉 나눔(고딕·명조·손글씨), 자막은 나눔고딕.
- 프레임 확인: `05_edit/final_sheet.png`(4×3), `05_edit/samples/f_*.png`(7장)
