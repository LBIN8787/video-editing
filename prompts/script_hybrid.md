## 편집 스타일: 하이브리드 (원본 영상 + 논리·인과 + 종이·손그림) — styles/hybrid

식스시그마처럼 **실제 인물·현장 영상**을 가져와 쓰고, 머니크루처럼 **논리 근거와 인과관계**를 단계별로 쌓고,
미주일기처럼 **종이 위 손그림 도식·도형**으로 보여 줍니다. 결과물은 `02_script/hybrid.json` 입니다.

### 1. 이야기 먼저 (시청자가 '무슨 이야기인지' 바로 알게)
- **질문 하나**(question): 영상 전체가 답하는 한 문장 질문. 첫 30초 안에 말합니다.
- **은유 하나를 끝까지**: 어려운 대상을 한 단어로 바꿔 부르고 끝까지 같은 말을 씁니다 (예: 데이터센터 = 'AI 공장').
- **인과 지도(map) 하나를 계속 키웁니다**: 칸(nodes) 4~8개, 화살표(edges). 처음에 길을 보여 주고(map_causal),
  장마다 다시 돌아와 칸을 하나씩 확인·추가하고, 마지막에 전체를 다시 보여 주며 정리합니다. "지금 어디쯤인지"가 늘 보입니다.
- 장(chapter) 5~7개, 장마다 제목은 질문형. 장 시작은 chapter 장면.
- 숫자는 반드시 비교 기준과 함께, 한 박자에 숫자 2개까지. 비유 2개 이상, 과거 사례 1개 이상, 반론 1개.

### 2. 장면과 박자
- 장면(scene) 하나 = 한 가지 화면. 박자(beat) 1~3개, 박자마다 내레이션 1~2문장(say).
- 화면은 박자에 맞춰 움직입니다(박자마다 무엇이 나타나는지 필드로 지정).
- **같은 type 을 연달아 쓰지 않습니다.** 원본 영상(footage)은 20~30초에 한 번은 나오게 합니다.
- 장면 길이 6~20초, 영상 전체 6~9분.

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

자료 화면 사진은 `python -m ytflow archive search "<영문>"` 로 찾고 `ytflow.stages.archive.still_to_clip()` 으로 16:9 영상으로 바꿔 footage 에 넣습니다.

### 4. 원본 영상 (footage) — 소스 먼저
- 쓸 수 있는 영상만: 인물 본인·회사·정부·기관의 **공식 영상**(사용자 PC 에서 rebuild 로 받는 YouTube 공식 채널 포함),
  **퍼블릭 도메인**(NASA·미국 정부), **CC BY/CC0**(위키미디어 공용). CC BY-SA·NC·ND, 다른 해설 유튜버 영상은 쓰지 않습니다.
- 다른 행사·시점의 영상이면 label 과 lower 에 **'자료 화면'과 실제 날짜·장소**를 적습니다(시청자가 현장으로 오해하지 않게).
- footage 의 출처·라이선스는 hybrid.json 의 footage{키: {file, credit, url}} 에 적고, 설명란에 자동으로 들어갑니다.

### 5. 금지
- 같은 레이아웃 반복, 한 문장마다 카드 한 장, 설명 없는 숫자 나열.
- 벤치마킹 채널 이름·대사·캐릭터·로고. 투자 권유. 확인 안 된 숫자의 단정.
