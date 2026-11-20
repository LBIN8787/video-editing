## 편집 스타일: 하이브리드 (원본 영상 + 논리·인과 + 종이·손그림) — styles/hybrid

식스시그마처럼 **실제 인물·현장 영상**을 가져와 쓰고, 머니크루처럼 **논리 근거와 인과관계**를 단계별로 쌓고,
미주일기처럼 **종이 위 손그림 도식·도형**으로 보여 줍니다. 결과물은 `02_script/hybrid.json` 입니다.

### 1. 이야기 먼저 (시청자가 '무슨 이야기인지' 바로 알게)
- **인트로 없음**(모든 채널, manual/README §2-1, v24): 인사·채널 소개·순서 예고·구독 부탁을 쓰지 않는다. 첫 장면부터 본론 — 장면 하나(때·곳·사람) 또는 엇갈리는 두 시각 → 3~6문장 안에 오늘의 질문. 말투: 호기심은 README §2-3(3인칭 다큐 내레이터), 시장·시사·AI 는 11-workflow §3-2(차분한 분석형, 어미를 문맥에 맞게 섞고 특정 어미를 강제하지 않음). 말 걸기·감탄 없음.
- **진행 말투**(README §2-2, `check` MUST): "여기까지가 ~였고요." 처럼 연결어미(~고요·~는데요)로 문장을 끝내지 않습니다. 문장은 '~입니다 / ~죠 / ~까요?'로 닫고, 장마다 같은 틀을 반복하지 않습니다.
- **편집 기준**: 전환·사진 장 표지는 자동, 카메라는 고정·배경음은 기본 없음(manual/05 §0-5, README §2-5). 숫자가 '줄었다/늘었다'면 막대보다 `isotype`(사물 아이콘), 장 끝은 `recap`(정리판)을 검토합니다. 먼지·빛샘 같은 장식은 드물게.
- **반복 피로 막기**(manual/05 §0-3, 권고): 글씨·도형만 길게 이어지면 사진·지도·말에 맞춰 생기는 그림을 섞는 것을 검토합니다. 효과(`"fx"`)는 내용과 맞을 때만 — 시장 채널은 tilt·dolly·scan 끔(09 §6).
- **배경**: 자동(manual/05 §0-2). 바꾸려면 장면에 `"bg": "photo|grid|spot|tint|film"`.
- **질문 하나**(question): 영상 전체가 답하는 한 문장 질문. 오프닝 직후 첫 1분 안에 말합니다.
- **은유 하나를 끝까지**: 어려운 대상을 한 단어로 바꿔 부르고 끝까지 같은 말을 씁니다 (예: 데이터센터 = 'AI 공장').
- **인과 지도(map) 하나를 계속 키웁니다**: 칸(nodes) 4~8개, 화살표(edges). 처음에 길을 보여 주고(map_causal),
  장마다 다시 돌아와 칸을 하나씩 확인·추가하고, 마지막에 전체를 다시 보여 주며 정리합니다. "지금 어디쯤인지"가 늘 보입니다.
- 장(chapter) 5~7개, 장마다 제목은 질문형. 장 시작은 chapter 장면.
- 숫자는 반드시 비교 기준과 함께, 한 박자에 숫자 2개까지. 비유 2개 이상, 과거 사례 1개 이상, 반론 1개.

### 2. 장면과 박자
- 장면(scene) 하나 = 한 가지 화면. 박자(beat) 1~3개, 박자마다 내레이션 1~2문장(say).
- 화면은 박자에 맞춰 움직입니다(박자마다 무엇이 나타나는지 필드로 지정).
- **같은 type 을 연달아 쓰지 않습니다.** 원본 영상(footage)은 20~30초에 한 번은 나오게 합니다.
- 장면 길이 6~20초. 영상 전체 길이는 manual/README §2-4 (롱폼은 최소 10분, 짧게 끝낼 것은 쇼츠로).

### 3. 장면 type (필드는 ytflow/stages/hybrid.py 와 아래 예시 그대로)
| type | 화면 | 주요 필드 |
|---|---|---|
| footage | 원본 영상: 전체 화면(frame=full) 또는 종이 위 사진(frame=photo) | clip{src, start, frame}, 박자의 lower{name, role}, vox{text, note} |
| chart | 실제 시세 선 그래프, 마지막 구간으로 카메라 확대, 도장 | ticker, period, append(시세에 없는 확정 종가), 박자 focus_last, mark, stamp |
| map_causal | 인과 지도 (영상 전체에서 같은 칸 위치) | 박자 reveal[], instant[[a,b]], draw[[a,b]], active, tag{node,text} |
| usmap | 손그림 미국 지도 + 주 강조 + 카운터 | 박자 counter, counter2, highlight[주 영문명], note{state,text} |
| versus | 두 숫자 맞대기 + 질문 | left/right{value,label,icon}, 박자 question |
| chapter | 장 제목 (종이가 밀려 들어옴) | num, title, icon |
| quote | 인물·보고서 발언 카드 + 형광펜 + 이름 자막 | who, role, quote, keyword, note, 박자 mark |
| checklist | 있다/없다/날짜/주의 목록 | rows[{label,state:yes|no|date|warn,value}], 박자 upto, stamp |
| analogy | 실제 ≈ 비유 + 결론 | left/right{icon,label,sub}, result{icon,label} |
| funnel | 줄어드는 빗금 막대 | bars[{value,label,sub,highlight}], unit, 박자 upto |
| apartments | 작은 건물 N개 그리드(전체·대기·취소) | total, waiting, cancel, 박자 stage |
| parking | 100칸 주차장 (비율) | 박자 fill |
| bars | 세로 빗금 막대 비교 | items[{label,value}], unit |
| bignum | 큰 숫자 하나 + 비교 | value, small, compare{label,value} |
| timeline | 연도 축 + 구간·일정 | years[], spans[{from,to,label,tone}] 또는 events[{at,label,sub}], 박자 upto |
| compare | 그때 vs 지금 표 | cols[2], rows[{label,a,b}], 박자 upto |
| outro | 마무리 제목 + 영상 | title, sub, clip |
| people | 사람 100명 그림, 그중 N명 빨갛게 (비율을 사람 수로) | count, value, caption, sub, scatter, 박자 fill |
| newspapers | 두 신문 비교: 검은 줄로 지워진 지면 vs 큰 제목 지면 (재구성 그림) | left{name,sub,stamp}, right{name,sub,headline,note}, 박자 show: left/right |
| shape | 곡선 모양 비교 개념도 (U자 vs W자 등, 숫자 축 없음 — label 에 '개념도') | ticks[{at,label}], 박자 curve{tone,label,label_at,points[[x,y]...],circle,note} |
| afterline | **설명 무대** 사건 이후 누적: 시간선 + 붓 금지 표시 → 붉은 '이후' 구간 → 카드가 하나씩 쌓임 → 수량 문구 | event{name,date,tag,mark}, items{count 또는 labels[], icon(chip·lucide)}, headline{pre,emph}, 박자 show[event·after·items·headline], at{부품:단어} |
| spread | **설명 무대** 두 값의 차이: 재료→공정→제품 소품 → 두 가격 막대·점선 → 괄호로 차이 → 한쪽 값이 바뀌면 간격이 줄어듦 | steps[{icon,label}], low/high{label,value,text}, diff{label,formula}, change{value,text,label}, 박자 show[steps·low·high·diff·change] |
| share | **설명 무대** 전체 중 몫: 전체 막대 → 부분 채움 → 비교 눈금 → 합계 괄호 | total, of, parts[{label,value}], mark{value,label}, sum{parts[],label}, 박자 show[total·p0·p1…·mark·sum] |
| motionboard | **설명 무대** 자유 무대: 인물(사진·실루엣)·소품 카드·글자·화살표·붓·금지·점선을 놓고 박자마다 나타남·옮김·강조·흐리게 | els{이름:{kind:person|card|img|text|arrow|brush|ban|dashed,…}}, 박자 do["이름", {move,to}, {hi}, {dim}, {hide}, {swap,text}], at{이름:단어} |

### 3-1. 쉽게 설명해야 하는 곳 = 모션그래픽 (설명 무대, 2026-11-20 사용자)
> "쉽게 설명해야 하는 부분이다, 상황 설명이 필요하다 = 모션그래픽을 주로 사용합니다."

- **상황 설명이 필요한 박자**(누가 무엇을 누구에게 넘기나 · 어떤 사건 뒤에 무엇이 늘었나 · 두 값의 차이가 왜 줄었나 · 전체 중 몫이 얼마인가 · 제도·구조가 어떻게 작동하나)에는 글·숫자 카드(bignum·checklist·quote) 대신 **설명 무대 장면**(afterline·spread·share·motionboard)을 먼저 씁니다. 맞는 틀이 없으면 motionboard.
- 순서: 자료(차트·기사·발언)로 질문을 열고 → 설명 무대로 원리를 풀고 → 다시 자료에서 그 원리를 확인합니다 (docs/31).
- 한 무대 안에서 앞에 나온 인물·물체·기준선은 남기고, 대사의 **동사**(판다·풀린다·옮긴다·줄어든다)를 말할 때 요소가 바뀌게 `at` 으로 맞춥니다.
- 화면 글자는 주체·단위·날짜·결론만. 나머지는 위치·높이·색이 말하게 합니다. 보고서의 주장이면 title 에 출처('○○ 보고서의 주장')를 남깁니다.
- 실제 인물은 권리가 확인된 사진(`photo`)만, 없으면 얼굴 없는 실루엣 + 이름표. 바탕은 `theme`: paper(기본)·dark·light.
- 스타일 문서: `styles/explain-stage/STYLE.md` (필드·예시), 장면 문서 `docs/51-explain-stage.md`.

**스타일 조합 (권고, manual/05 §0-0·§0-1 — 넘치면/모자라면으로 판단):** 한 스타일로만 쓰지 않습니다. 새 장면 type `kb`·`card_type`·`journey`·`kinetic`(docs/16)을 섞고, 장면에 `"layers"`(words·photo·stamp·line·locator·number)로 다른 스타일 요소를 겹치며, 필요한 장면만 `"skin"` 으로 그래픽 팩을 바꿉니다. 규칙과 필드는 `manual/05-style-matching.md` §0-1.

자료 화면 사진은 `python -m ytflow archive search "<영문>"` 로 찾고 `ytflow.stages.archive.still_to_clip()` 으로 16:9 영상으로 바꿔 footage 에 넣습니다.

### 4. 원본 영상 (footage) — 소스 먼저
- 쓸 수 있는 영상만: 인물 본인·회사·정부·기관의 **공식 영상**(사용자 PC 에서 rebuild 로 받는 YouTube 공식 채널 포함),
  **퍼블릭 도메인**(NASA·미국 정부), **CC BY/CC0**(위키미디어 공용). CC BY-SA·NC·ND, 다른 해설 유튜버 영상은 쓰지 않습니다.
- 다른 행사·시점의 영상이면 label 과 lower 에 **'자료 화면'과 실제 날짜·장소**를 적습니다(시청자가 현장으로 오해하지 않게).
- footage 의 출처·라이선스는 hybrid.json 의 footage{키: {file, credit, url}} 에 적고, 설명란에 자동으로 들어갑니다.

### 4-1. 제목·썸네일 (package)
hybrid.json 에 `package` 를 같이 쓴다: title, title_options(3), title_why, thumbnails(A/B/C: layout·image·lines·hl·marks·why). 규칙은 `prompts/thumbnail.md`.

### 5. 금지
- 같은 레이아웃 반복, 한 문장마다 카드 한 장, 설명 없는 숫자 나열.
- 벤치마킹 채널 이름·대사·캐릭터·로고. 투자 권유. 확인 안 된 숫자의 단정.
