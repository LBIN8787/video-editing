# 하이브리드 장면 — 만드는 법과 움직이는 예시 (2026-11-20)

> **실제 완성본에서 잘라 낸 예시 37개**(진짜 대본·목소리와 함께): [real-examples.md](real-examples.md)

> 사용자: "왜냐하면 예시로 이런거는 저 예시사진으로는 다 안보이잖아" · "일단은 자주 쓰는 스타일과 화풍부터 해줘"
> → 예시 사진 한 장이 아니라 **움직임(박자표) + 짧은 예시 영상**으로. 먼저 지난 회차(시장 8편)에 매번 쓰인 장면 10가지.

장면마다: 언제 쓰나 · **박자표**(대사의 어느 말에서 무엇이 나타나나 — 렌더러 코드 그대로) · `hybrid.json` 쓰는 법 · 확인할 것 · 예시 영상(Drive, 소리 포함 — 말과 화면이 맞물리는 걸 들으며 보기).

| 장면 | 이름 | 언제 | 예시 |
|---|---|---|---|
| [`bignum`](bignum.md) | 큰 숫자 한 개 | 오늘 이야기의 출발점이 되는 숫자 하나(종가·규모·비율). 숫자가 곧 질문일 때 | [영상](https://drive.google.com/file/d/1yD_LnfPrK2pW6p0l_6o-t8hHcMFCzWmn/view) |
| [`bars`](bars.md) | 막대 비교 | 같은 단위의 값 2~6개를 한눈에 비교 (지수 등락·업종·종목). 음수는 기준선 아래로 | [영상](https://drive.google.com/file/d/1pnlWsrvCke45fr1kE6UkvVUm9OVZFfxx/view) |
| [`chapter`](chapter.md) | 장 표지 | 장이 바뀌는 순간. 번호 + 짧은 제목 한 줄 | [영상](https://drive.google.com/file/d/1Aa_JCX4AKbPSD5BaeLtZ6r2s4VHtYhM5/view) |
| [`checklist`](checklist.md) | 줄 목록 | 사건·조건·주장 3~5개를 차례로 쌓을 때. 줄마다 상태(확인 ✓ / 경고 △ / 아님 ✗ / 날짜) | [영상](https://drive.google.com/file/d/1WB0v-x5RTestBbb7_GtmIbfVX0XSvXyf/view) |
| [`map_causal`](map_causal.md) | 인과 지도 (코르크판) | 원인 → 결과가 이어지는 흐름. 카드(노드)가 하나씩 꽂히고 실(화살표)이 이어짐 | [영상](https://drive.google.com/file/d/15-88mqDELcl3jkfHOidgv6lyztGGDkyk/view) |
| [`analogy`](analogy.md) | 비유 두 칸 | 어려운 구조를 생활 속 물건으로 옮길 때. 왼쪽(익숙한 것) ≈ 오른쪽(지금 일) | [영상](https://drive.google.com/file/d/1gntzQVakAUmd7VBrmajqud_Aa8oXgbpH/view) |
| [`quote`](quote.md) | 인용 카드 | 이름 있는 사람·매체의 말 한 문장. 원문 + 번역, 핵심어 형광펜 | [영상](https://drive.google.com/file/d/1duJVu6iZNVg8qR3mvE84gWIsvGfNgq5v/view) |
| [`versus`](versus.md) | 맞대기 | 엇갈린 두 시각·주장 vs 부인·기대 vs 현실 | [영상](https://drive.google.com/file/d/1uze0c79ORRf8IRmXsjG541SM-n_fSjn9/view) |
| [`kinetic`](kinetic.md) | 키네틱 글자 | 결론 한 문장·장 전환 한 줄. 목소리가 말하는 순간 낱말이 박힘 (화면 글자가 곧 자막) | [영상](https://drive.google.com/file/d/10QIVmNXXiB_opqz4RQsLb9J-HeiepuTS/view) |
| [`outro`](outro.md) | 마무리 카드 | 영상 끝. 실사·자료 영상 위에 흐린 막 + 종이 카드 한 장 | [영상](https://drive.google.com/file/d/1LELn4La13CQ7QoulbhPu619tz6UtT8lp/view) |

## 나머지 장면 — 같은 틀의 만드는 법 (2026-11-20, 자동 생성 + 사람 설명)

> 사용자: "구성 요소별로 제작 메뉴얼같은거도 따로 작성한거야? … 그게 아니면 나중에 재구현 불가능할거아니야 또 예시사진으로는 사실 전부 보여주지 못하고 약간 괴리가 생기니까"

위 10가지 말고 렌더러에 있는 장면 전부. 파일마다 **화면 구성·움직임 원리**(사람이 코드를 읽고 씀, `styles/visuals.yaml` 의 `build`) · **박자표**(예시 렌더의 시간축에서 자동) · **그 예시를 만든 대본 그대로**(`styles/visuals/<id>.json`) · 읽는 키·코드 위치. 움직이는 예시는 [연출 예시 목록](https://claude.ai/artifact/SPHyXdpGmcdPwMQu7cpMdP)에서 ▶. 다시 만들기 `python scripts/visual_catalog.py <작업 폴더> --only <id> --force` → `python scripts/visual_spec.py --md`.

| 장면 | 이름 | 묶음 | 언제 |
|---|---|---|---|
| [`compare`](compare.md) | 비교표 | 숫자·크기 비교 | 항목 여러 개를 두 대상으로 비교 |
| [`chart`](chart.md) | 시세 선 그래프 | 숫자·크기 비교 | 주가·지수·환율의 최근 흐름 (시장 채널) |
| [`isotype`](isotype.md) | 사물 아이콘 줄 | 숫자·크기 비교 | '10통 중 3통' 같은 몫을 물건으로 느끼게 |
| [`people`](people.md) | 100명 그림 | 숫자·크기 비교 | 비율을 '사람'으로 (3명 중 1명) |
| [`share`](share.md) | 전체 중 몫 | 숫자·크기 비교 | 매출 중 지역 비중, 전체 대비 몫 |
| [`spread`](spread.md) | 두 값 사이 간격 | 숫자·크기 비교 | 마진·스프레드·가격 차이가 어디서 생기나 |
| [`apartments`](apartments.md) | 칸 채우기 (세대 수) | 숫자·크기 비교 | 수백~수천 단위의 몫을 한눈에 |
| [`parking`](parking.md) | 주차장 칸 | 숫자·크기 비교 | 공급·수요, 자리가 차고 비는 비유 |
| [`funnel`](funnel.md) | 깔때기 | 구조·흐름·인과 | 단계별로 줄어드는 수 (지원 → 합격 → 등록) |
| [`statecard`](statecard.md) | 상태 카드 (+ 가운데 주체) | 구조·흐름·인과 | AI·앱이 '무엇을 대신 하나', 단계마다 결과가 나는 일 (AI 채널) |
| [`timeline`](timeline.md) | 연표 | 구조·흐름·인과 | 사건의 순서, 과거 사례와 지금 |
| [`afterline`](afterline.md) | 사건 이후 누적 | 구조·흐름·인과 | 제재·발표 '이후에도' 계속된 일 |
| [`shape`](shape.md) | 모양 비교 개념도 | 구조·흐름·인과 | 정확한 수치 없이 패턴의 차이만 말할 때 |
| [`motionboard`](motionboard.md) | 자유 무대 | 구조·흐름·인과 | 정해진 틀에 안 맞는 설명 — 사람과 물건 사이 관계가 움직일 때 |
| [`docspot`](docspot.md) | 기사 스포트라이트 | 증거·원문·실제 화면 | 기사·발표문·약관의 한 줄이 근거일 때 |
| [`newsdesk`](newsdesk.md) | 뉴스 데스크 카드 | 증거·원문·실제 화면 | 여러 소식을 차례로 (AI 뉴스 정리, 브리핑) |
| [`newspapers`](newspapers.md) | 두 나라 신문 | 증거·원문·실제 화면 | 같은 사건을 다르게 다룬 매체 비교 |
| [`bite`](bite.md) | 원본 발언 컷 | 증거·원문·실제 화면 | CEO·연준·정부의 실제 발언 (원본이 있을 때만) |
| [`zoomshot`](zoomshot.md) | 화면 자동 줌 | 증거·원문·실제 화면 | 웹페이지·앱 화면의 한 곳을 가리킬 때 |
| [`chat`](chat.md) | AI 대화 화면 | 증거·원문·실제 화면 | AI 사용법 — 무엇을 물으면 어떻게 답하나 |
| [`terminal`](terminal.md) | 터미널 | 증거·원문·실제 화면 | 개발 도구·명령 사용법 (실제 실행 기록만) |
| [`kb`](kb.md) | 자료 사진 켄 번스 | 증거·원문·실제 화면 | 역사·사건의 자료 사진 (아카이브 다큐) |
| [`footage`](footage.md) | 실사 영상 | 실사 영상 | 실제 장면이 있을 때 — 신뢰·현장감 |
| [`journey`](journey.md) | 지도 여정 | 지도·장소 | 어디서 어디로 — 전파·이동·공급망 |
| [`choropleth`](choropleth.md) | 나라 색칠 지도 | 지도·장소 | 여러 나라의 수치 비교 |
| [`usmap`](usmap.md) | 미국 주 지도 | 지도·장소 | 미국 주별 이야기 (선거·규제) |
| [`story`](story.md) | 이야기 그림판 | 이야기·그림·애니메이션 | 누가·언제·어디서·무엇을 한 이야기 (호기심 채널) |
| [`stage`](stage.md) | 애니메이션 무대 | 이야기·그림·애니메이션 | 호기심 채널 이야기형, 기억할 한 장면 |
| [`illust`](illust.md) | 손그림 삽화 카메라 | 이야기·그림·애니메이션 | 사람들의 생각·행동·상황, 옛 사례 재현 (그림은 사람이 준비) |
| [`metaphor`](metaphor.md) | 움직이는 비유 | 이야기·그림·애니메이션 | 사용자가 고를 때만 (따로 쓰는 스타일) |
| [`studio3d`](studio3d.md) | 3D 무대 | 이야기·그림·애니메이션 | 물건 하나를 입체로 보여 줄 때 (시안) |
| [`recap`](recap.md) | 장 끝 정리판 | 장 나누기·정리·강조 문장 | 긴 영상의 장 끝 정리 |
| [`card_type`](card_type.md) | 검은 카드 타자기 | 장 나누기·정리·강조 문장 | 인용·핵심 문장, 무거운 한 마디 |
| [`chapter@two-line`](chapter_two-line.md) | 두 줄 장 표지 | 장 나누기·정리·강조 문장 | 문제·비판 꼭지를 나눌 때 (앞부분은 표지 없이 흐르다가) |

전환·겹치기: [`transitions.md`](transitions.md) (fade·push·wipe·zoom·iris·모양 매치 아이리스) · [`overlays.md`](overlays.md) (실사 위 말 칩·선 끊김)

## 모든 장면에 공통
- **박자(`beats`)**: 한 장면 = 박자 여러 개, 박자 하나 = 대사 한두 문장. 화면 요소는 박자 시작 시각에 맞춰 나타난다.
- **`t` 낱말**: 항목·줄에 `"t": "낱말"` 을 주면 그 낱말을 **말하는 순간**(받아쓰기로 맞춘 시각) 나타난다 — 화면이 말보다 늦거나 빠르지 않게 하는 핵심.
- **숫자 카드(`motion`)**: 박자에 `{"t":"낱말","do":"count","value":"…","label":"…","x":…,"y":…}` — 그 낱말에서 작은 카드가 튀어나와 숫자가 세어진다. 어느 장면 위에나 얹힌다.
- **겹치기(`layers`)**: 낱말 띄우기·자료 사진 액자·날짜 도장·위치 지도·숫자 카드 (05 §0-1).
- **화풍(바탕·색)**: 장면의 `skin`(dark-doc·newsprint …) 또는 `look`(board) — 화풍 목록은 `styles/looks.yaml`, `python -m ytflow looks`.

## 다음에 채울 것
- 자동 생성한 장면(위 '나머지 장면')은 실제 완성본에서 쓴 예시가 생기면 손으로 다듬어 첫 줄 표시를 지움 (그 뒤로는 자동 생성이 덮어쓰지 않음).
- 화풍(`styles/looks.yaml`)마다 같은 장면이 어떻게 달라 보이는지는 화풍 목록 페이지(`skills/looks-gallery`)가 움직이는 미리보기로 보여 준다.
