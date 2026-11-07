# 13. 연출과 그래픽 분리 — 편집점·편집 포인트는 그대로, 그래픽(인포그래픽·도형·그래프·겉모습)은 갈아 끼운다 (2026-11-07)

영상 한 편 = **연출 층**(무엇이·언제·어떻게 움직이나) + **그래픽 층**(어떻게 보이나).
방송으로 치면 연출은 'PD 큐시트', 그래픽은 '방송사 그래픽 패키지'. 같은 큐시트로 그래픽 패키지만 바꿔 다른 채널처럼 내보낼 수 있다.

```
대본(내레이션)  ─▶  연출 층 (02_script/hybrid.json)          ─▶  그래픽 층 (skins/<id>/skin.yaml)  ─▶  final.mp4
                    편집점 · 편집 포인트 · 의도·데이터 · 리듬          그림(그래프·도형·카드 모양) + 색·글꼴·배경·선 질감·사진 톤·자막
                    "바꾸면 이야기가 달라진다"                         "바꿔도 이야기는 같다"
```

## 1. 연출 층 — `02_script/hybrid.json` (+ 렌더러의 장면 문법 `ytflow/stages/hybrid.py`)
### 1-1. 편집점 (언제 바뀌나)
| 편집점 | 정의 | 어디서 정하나 |
|---|---|---|
| 장면 경계(컷) | 화면 종류가 바뀌는 순간 | `scenes[]` 의 순서 |
| 박자 경계 | 장면 안에서 다음 문장이 시작되는 순간 — 화면 요소가 하나씩 더해짐 | `scenes[].beats[]` |
| 장 경계 | 큰 질문이 바뀌는 순간 (장 표지) | `type: chapter` |
| 자막 줄 경계 | 실제로 그 말을 하기 시작하는 순간 (받아쓰기 단어 시각) | 자동 (`subtitles`) |

리듬 값(장면 시작 후 첫 말 0.35초, 박자 사이 0.28초, 마지막 여유 0.55초)도 연출이다 — `LEAD`, `GAP`, `TAIL`.

### 1-2. 편집 포인트 (그 순간 무엇이 일어나나) — 모두 그래픽과 무관한 '사건'
| 편집 포인트 | 하는 일 | 대본 필드 |
|---|---|---|
| 자료 화면 전환 | 원본 영상·사진으로 컷, 천천히 다가가기(push) | `type: footage`, `clip{frame: full/photo}` |
| 이름 자막 | 인물·장소 소개 띠 | 박자 `lower{name, role}` |
| 쪽지 주석 | 화면 위 핵심어 + 손글씨 메모 | 박자 `vox{text, note}` |
| 형광펜 | 인용문 핵심어 칠하기 | `quote.keyword` + 박자 `mark` |
| 도장 | 결론 한 단어 꽝 | 박자 `stamp` |
| 동그라미·화살표·X | 시선 끌기 | 장면별(versus 질문, 지도 note 등) |
| 숫자 세기 | 0 → 값으로 올라감 | `bignum`, `versus`, `bars`, `counter` |
| 순서대로 드러내기 | 목록·막대·연표가 박자마다 한 칸씩 | 박자 `upto`, `stage`, `fill` |
| 인과 지도 진행 | 칸 등장·화살표 그리기·지금 칸 강조·꼬리표 | `reveal`, `draw`, `instant`, `active`, `tag` |
| 카메라 | 차트 마지막 구간 확대, 영상 push | `focus_last`, (자동 push) |
| 장 전환 | 종이 한 장이 밀려 들어옴 + 휙 소리 | `type: chapter` |
| 효과음 신호 | 펜·팝·딸깍·휙·쿵 (그래픽이 아니라 '사건'에 붙음) | 자동 (편집 포인트마다) |

### 1-3. 연출 문법 (장면 type 묶음 — 어떤 화면 종류를 쓰는가)
| 문법 | 뼈대 | 대본 지시 |
|---|---|---|
| hybrid | 자료 화면 + 인과 지도 + 숫자 도식, 같은 type 연속 금지, 20~30초마다 자료 화면 | `prompts/script_hybrid.md` |
| source | 원본 발언 영상 중심 + 요약 카드 | `prompts/script_source.md` |
| infographic | 자체 도식·차트·비유 그림 중심 | `prompts/script_infographic.md` |
| shorts | 9:16, 고정 훅 + 큰 자막 | `prompts/shorts_script.md` |

## 2. 그래픽 층 = 그래픽 팩 `skins/<id>/skin.yaml` — **그림(컴포넌트) + 겉모습(스킨)**

### 2-1. 그림: 같은 의도를 어떤 인포그래픽·도형·그래프로 그리나 (엔진 `ytflow/stages/graphics.py`)
연출은 **의도와 데이터**만 적는다 (예: "비교: 필라델피아 719, 세인트루이스 347, 강조=필라델피아, 2박자째에 등장").
그래픽 팩의 `components` 가 의도마다 그림을 고른다. 장면 하나만 바꾸려면 대본 장면에 `"look": "donut"`.

| 의도 (연출) | 데이터 | 고를 수 있는 그림 (그래픽) |
|---|---|---|
| **compare** 값 비교 | 항목·값·강조 | `bars` 빗금/면 막대 · `duel` 큰 숫자 맞대기 · `pictogram` 사람 아이콘 줄 |
| **proportion** 비율 | 백분율·문구 | `people` 사람 100명 · `waffle` 네모 칸 100개 · `donut` 도넛 그래프 |
| **flow** 원인→결과 | 칸·화살표·지금 칸 | `box` 손그림 네모 · `pill` 둥근 알약 · `sticky` 포스트잇 · `circle` 동그라미 |
| **chapter** 장 표지 | 번호·질문 | `paper` 종이 한 장이 밀려옴 · `type` 강조색 판 + 거대한 번호 |
| **lower** 이름 자막 | 이름·직함 | `strip` 종이 띠 · `bar` 얇은 선 + 굵은 글씨 (영상 위) |

- 예전 장면 type 은 의도로 자동 변환: `bars`·`versus`(숫자일 때) → compare, `people` → proportion. → **예전 대본도 그래픽 팩만 바꾸면 다른 그림**.
- 숫자가 아닌 맞대기('스페인' vs '?')처럼 변환할 수 없는 장면은 원래 그림을 그대로 쓴다.
- 새 그림을 추가하려면 `graphics.py` 에 함수 하나 + 의도 표에 이름 하나. 대본은 안 바뀐다.

### 2-2. 겉모습: 색·글꼴·배경·선 질감·사진 톤·자막 상자 (엔진 `ytflow/stages/skin.py`)
| 항목 | 정하는 것 | 예 |
|---|---|---|
| `palette` | 색 토큰 20개: base(바탕)·ink(글씨)·accent(강조)·card·muted_text·line·marker(형광펜)·redact·ok·warn … | `skin.py` 의 `TOKENS` 가 기본값 |
| `fonts` | 역할별 글꼴: title·value(숫자)·box·note(손글씨)·label | 명조 / 고딕 / 손글씨 |
| `background` | 바탕: `paper`(구겨진 종이) · `flat`(민무늬) · `grid`(모눈) · `dark`(필름 알갱이·가장자리 어둡게) | |
| `strokes` | 선 질감: 거칠기 배율(0=곧은 선), 휘어짐, 채우기(`hachure` 빗금 / `solid` 면) | |
| `photo` | 자료 화면 톤: `none` · `bw` · `sepia` · `cool` · CSS | |
| `subtitle` | 자막 글꼴·크기·글자색·상자색 | |

만들어 둔 그래픽 팩 (그림 + 겉모습):
| id | 비교 | 비율 | 인과 칸 | 장 표지 | 겉모습 |
|---|---|---|---|---|---|
| `paper-sketch` (기본) | 대본대로(빗금 막대·숫자 맞대기) | 사람 100명 | 손그림 네모 | 종이 한 장 | 구겨진 종이·명조·손글씨·빨간 펜 (미주일기풍) |
| `clean-flat` | 면 막대 | 네모 칸 100개 | 둥근 알약 | 큰 글씨 판 | 민무늬·고딕·곧은 선 (머니크루풍) |
| `dark-doc` | 사람 아이콘 줄 | 도넛 | 포스트잇 | 큰 글씨 판 | 먹색 필름·호박색 강조·흑백 자료 화면 (다큐풍) |

## 3. 쓰는 법
```bash
python -m ytflow skin-preview <프로젝트> --scenes 13,16,21,24 --skins paper-sketch,clean-flat,dark-doc   # 같은 연출, 스킨별 비교표
YTFLOW_SKIN=dark-doc python -m ytflow hybrid <프로젝트>      # 한 번만 다른 스킨으로
```
- 고정하려면 프로젝트 `edit.yaml` 의 `edit.skin: <id>` (채널 기본은 `channels/<id>/channel.yaml` 의 `skin`).
- 새 스킨: `skins/<새 id>/skin.yaml` 을 복사해 값만 바꾼다. 코드 수정 없음. `skin-preview` 로 확인.
- 렌더러에 새 색을 쓸 때는 `skin.py` 의 `TOKENS` 에 이름을 붙인다(안 붙이면 스킨이 못 바꾼다).
- 제목·썸네일(`prompts/thumbnail.md`)도 같은 원리: 문구·배치(연출)는 `package`, 색·사진 톤(그래픽)은 썸네일 스킨값.

## 4. 기존 '편집 스타일' = 연출 문법 + 그래픽 스킨
| 예전 이름 | 연출 문법 | 그래픽 스킨 |
|---|---|---|
| hybrid (지금 두 영상) | hybrid | paper-sketch |
| mijudiary | infographic | paper-sketch |
| moneycrew | infographic | clean-flat |
| sixsigma | source | dark-doc 계열 |

→ "식스시그마 연출에 미주일기 그래픽", "하이브리드 연출에 다큐 그래픽" 처럼 섞어 쓸 수 있다.
