---
from: claude
type: youtube-check
url: https://www.youtube.com/watch?v=FGQApSFoQAc
status: done
title: 썸네일 약속 → 편집 연출 부분 확인 (식스시그마 · hit 9.1배)
---

## 목적
docs/49-thumbnail-research.md §5: 같은 채널 안 터진 영상과 안 된 영상의 **편집·연출 차이를 부분적으로** 확인합니다. 같은 채널 짝 요청이 하나 더 있습니다(파일명 thumb-edit-*). 썸네일 문구(참고): "충격은 2~3년 풍요는 20년 뒤 (빌 게이츠)". 이미 처리한 thumb-hook-* 요청과 같은 방식이면 됩니다.

## 필요한 입력
1. 공개 페이지에서 영상 ID·채널 일치, 길이·조회수(확인 시각). 대상이 다르면 대체하지 말고 보고.
2. **첫 30초**: 2초 간격 정지 → 캡처(15장 안팎, 어려우면 0·5·10·20·30초 5장 + 희소 표본 표시). 장마다 한 줄 — 화면에 무엇(인물 얼굴·숫자 카드·자료 화면·진행자·자막), **썸네일의 얼굴·숫자·문구가 처음 보이는 초**.
3. **중간 1분** (전체 길이의 40% 지점부터 60초): 5초 간격 캡처(12장 안팎). 장마다 한 줄 — 화면 종류, 직전 장과 비교해 **장면이 바뀌었나**(컷), 화면 위 글자·도표·원본 영상 여부.
4. 스크립트 패널이 있으면 위 두 구간의 대사 첫 문장만 (전문은 비공개 Drive 에만).
5. 챕터(설명란 타임코드) 목록.
6. 저장: 캡처는 비공개 Drive ytflow/refs/thumb-study-20261119/FGQApSFoQAc/ 에만. 공개 저장소에는 상태·개수·관찰 요약만.

## 제한
로그인 정보 입력·결제·설치·우회·쿠키 추출 금지. 내려받기 없이 재생 화면 캡처만. 심층 분석·매뉴얼 변경 하지 않기.

## 결과

### 확인시각
- **2026-11-19 14:55~15:08 KST** (원격 브라우저, 로그인 없이 공개 재생, 프리롤·재생 중 광고 미관찰). 조회수·좋아요·댓글은 14:55 KST 관찰값.

### 대상/일치
| 항목 | 값 |
|---|---|
| 영상 ID·URL | `FGQApSFoQAc` · https://www.youtube.com/watch?v=FGQApSFoQAc |
| 채널 | **Six Sigma \| 식스시그마** (채널 ID `UCb55ivT0IMLtiAcVu3B-vKQ`, 구독자 1.89만명) — 요청 대상과 일치, 대체 없이 진행 |
| 제목 | AI가 못 오를 사무직은 없다 \| 빌 게이츠 |
| 길이 | **682초 (플레이어 표기 11:21, lengthSeconds 682, video.duration 681.46)** |
| 공개일 | 2026-10-30T18:05:48-07:00 = **KST 2026-10-31 10:05:48** |
| 조회수 | **109,398회** (14:55 KST) · 좋아요 623 · 댓글 307 |
| 공개 상태 | playabilityStatus **OK**, isFamilySafe true, 카테고리 Education |
| 자막 | playerResponse에 ko·en-US·en(자동) 트랙 보고, 다만 플레이어 CC 버튼은 "자막 사용 불가". 화면 자막은 **영상에 직접 그려진 영어·한국어 이중 자막**(CC 아님)이고, **'스크립트 표시' 패널(자동 스크립트)은 사용 가능** |
| 썸네일 | 빌 게이츠 실사 컷아웃(손바닥 펴고 설명하는 제스처) + 좌측 검은 패널 대형 카피 **"충격은 2~3년"**('충격은' 흰색 / '2~3년' 주황빨강) · **"풍요는 20년 뒤"**('풍요는' 흰색 / '20년 뒤' 회색) + 우상단 6σ 로고. 요청서 참고 문구의 "(빌 게이츠)"는 썸네일에 텍스트로는 없음 |

### 첫 30초 — 2초 간격 16장(0~30초) + 경계 확인 3장(15·17·29초) = 19장
일시정지 후 목표 초로 이동해 `seeked` 뒤 실제 `currentTime` 일치를 확인하고 캡처했습니다. 1466x825 PNG.

| 초 | 화면에 나오는 것 | 화면 자막(연출 카피) | 장면 변화 / 썸네일 요소 최초 노출 |
|---|---|---|---|
| 0.0 | 빌 게이츠 클로즈업(원본 인터뷰). 좌상단 `2026.10.22 · Decoder (The Verge)` + `빌 게이츠 · 마이크로소프트 공동창업자`, 우상단 6σ | 없음(첫 자막 전) | **썸네일 얼굴이 0.0초 첫 프레임에 그대로.** 타이틀·인트로 없이 콜드오픈 |
| 2.0 | 같은 컷 | "The good stuff does take time." / "좋은 일은 시간이 걸립니다." | 게이츠가 **손바닥 편 제스처**(썸네일 컷아웃과 같은 손 모양) |
| 4.0 | 같은 컷 | "…cyber attacks and the job market thing," / "사이버 공격이나 일자리 문제…" | 키워드('job market'·'일자리') 주황 강조 |
| 6.0 | 같은 컷 | 같은 자막 유지 | 변화 없음 |
| 8.0 | 같은 컷 | "even in the next **2 to 3 years**, you'll see significant negative effects…" / "**2~3년** 안에도…" | **썸네일 숫자 '2~3년' 최초 노출**(표본 8초, 실제 전환은 6~8초 사이) |
| 10.0 | 같은 컷 | 같은 자막 | 변화 없음 |
| 12.0 | 같은 컷 | 같은 자막 | 변화 없음 |
| 14.0 | 같은 컷 | 같은 자막 | 손바닥 제스처 반복 |
| 15.0 | 같은 컷 | 같은 자막(경계 확인) | 컷 없음 |
| 16.0 | **닐레이 파텔 클로즈업**(리액션, 무발화) | 없음 | **컷 ①** (15~16초 사이) |
| 17.0 | **와이드 투샷**(파텔 좌·게이츠 우) | 없음 | **컷 ②** |
| 18.0 | **게이츠 클로즈업** | "And as the AI achieves superhuman intelligence," | **컷 ③** |
| 20.0 | 같은 컷 | 같은 자막 | 변화 없음 |
| 22.0 | 같은 컷 | 같은 자막 | 변화 없음 |
| 24.0 | 같은 컷 | "the **scarcity of white-collar skills** goes away," / "화이트칼라 능력의 **희소성**" | 자막 2번째 카드, 키워드 주황 |
| 26.0 | 같은 컷 | 같은 자막 | 변화 없음 |
| 28.0 | 같은 컷 | 같은 자막 | 변화 없음 |
| 29.0 | **와이드 투샷** | "So that things like doing telesales or telesupport…" / "전화 영업이나 전화 상담…" | **컷 ④** (28~29초 사이) |
| 30.0 | 같은 와이드 투샷 | 같은 자막 계속 | 컷 없음 |

- 0~30초 하드 컷 **4회**(15~16 / 16~17 / 17~18 / 28~29초), 나머지는 한 앵글 유지 + **2~8초 간격 자막 교체**.
- **인트로 범퍼·채널 로고 애니메이션 없음.** 0초부터 본편 인터뷰 소스가 바로 시작됩니다.
- 첫 30초 화면은 **원본 인터뷰(클로즈업·리액션·투샷) + 로어서드 라벨 + 이중 자막**뿐이고, 숫자 카드·도표·자료 화면·키워드 그래픽은 0장입니다.

### 중간 1분 — 273~333초(전체 682초의 40.06%부터 60초), 5초 간격 13장

| 초 | 화면 | 자막 | 직전 장 대비 컷 |
|---|---|---|---|
| 4:33 | 와이드 투샷(인터뷰 룸) | "…true **abundance** will have to find" / "진정한 **풍요**의 시대…" | 기준 |
| 4:38 | 게이츠 클로즈업 | "and hopefully they still have the control." | **컷** |
| 4:43 | 와이드 투샷 | "My big concern is this **20-year transition period**" / "**20년**의 전환기" | **컷** |
| 4:48 | 게이츠 클로즈업 | "have **winners and losers** and a lot of disruption," | **컷** |
| 4:53 | 같은 클로즈업 | "…get to that period of abundance." | 컷 없음 |
| 4:58 | **파텔 클로즈업**(로어서드가 `닐레이 파텔 · 더 버지 편집장`으로 교체) | "You think it's 20 years from now?" / "**20년 뒤**라고 보시는 건가요?" | **컷** |
| 5:03 | **원본 자료 영상: Boston Dynamics 아틀라스**(좌상단 `2025.08.20 · Boston Dynamics`, 우측 PIP 다른 앵글) | "There's a variety of milestones." | **컷(소스 B롤 진입)** |
| 5:08 | 같은 B롤 | "humanoid robots… two or three years away" / "**2~3년**이면 된다는 사람도 있고" | 컷 없음 |
| 5:13 | 같은 B롤 | "or more like eight years away" / "**8년**쯤 걸린다는 사람도 있죠" | 컷 없음 |
| 5:18 | 같은 B롤 | "Given the amount of **capital** and number of companies, particularly in China," | 컷 없음 |
| 5:23 | 같은 B롤(로봇 동작 진행) | 같은 자막 | 컷 없음 |
| 5:28 | 같은 B롤 | "…deliver physical labor at very, very low cost." | 컷 없음 |
| 5:33 | 같은 B롤 | 자막 유지 | 컷 없음 |

- 60초 안 하드 컷 **5회**(273~278 / 278~283 / 283~288 / 293~298 / 298~303초 사이, 5초 표본이라 ±5초).
- **303~333초(30초 이상)는 한 컷도 없이 이어지는 원본 자료 영상 1편**(휴머노이드 로봇 실사 + PIP + 출처·날짜 라벨).
- 화면 위 글자는 로어서드(출처·날짜·발언자 소속), 이중 자막(핵심어 주황 강조), 출처 라벨뿐이고 도표·수치 그래픽은 없습니다.

### 스크립트 패널 (두 구간 대사 첫 문장만, 전문은 비공개 Drive)
- 0:00 "The good stuff does take time and some of the things like cyber attacks and the job market"
- 0:06 "thing, you know, even in the next two to three years, you'll see significant negative effects in those two areas."
- 0:15 "And as the AI achieves superhuman intelligence, the scarcity of white-collar skills goes away."
- 0:28 "So that things like doing telesales or telesupport or helping in the accounting"
- 4:33 "to organize and have purpose uh and hopefully they they still have the control yeah my big concern"
- 4:41 "is this 20-year transition period where they'll have winners and losers and a lot of disruption"
- 4:50 "and we have to get through that in order to get to that period of abundance. You think it's 20 years from now?"
- 4:58 "You know, I pick that as a reasonably safe number. There's a variety of milestones."
- 5:04 "For example, humanoid robots, you know, are those two or three years away, as some would say,"
- 5:12 "or more like eight years away, as other people would say."

### 챕터 (설명란 [목차] = 플레이어 '챕터' 목록, 5개)
- 0:00 인트로
- 1:13 1장. 왜 사무직부터인가
- 3:48 2장. 끝은 풍요, 그 앞은 20년
- 7:01 3장. 왜 그 시차가 문제인가
- 8:34 4장. 그 20년 동안 사람에게 남는 것

### §5 관점 요약 — 썸네일 약속과 편집·연출
- **얼굴**: 썸네일 게이츠 얼굴이 **0.0초 첫 프레임**(원본 인터뷰 클로즈업)이고, 2초에 썸네일과 같은 손바닥 편 제스처까지 나옵니다. 썸네일 컷아웃의 순간이 곧 오프닝입니다.
- **숫자 '2~3년'**: 약 **8초**에 자막("2 to 3 years" / "2~3년", 주황 강조)으로 회수. 같은 숫자를 5:04~5:08에 다시 말하며 그때는 로봇 실사 B롤을 붙입니다.
- **'풍요는 20년 뒤'**: 첫 30초에는 없고 **4:24~4:58**(중반 2장)에서 '20년' 자막·발화로 회수됩니다. 즉 썸네일의 두 숫자 중 앞 숫자는 초반, 뒤 숫자는 중반에 지급되는 구조입니다.
- **오프닝 구성**: 인트로 범퍼 없이 원본 인터뷰 소스로 콜드오픈, 좌상단에 출처·날짜(`2026.10.22 · Decoder (The Verge)`)와 발언자 소속을 즉시 표기. 0~30초는 클로즈업·리액션·투샷 4컷과 2~8초 간격 자막 교체로 리듬을 만듭니다.
- **중반 구성**: 인터뷰 3컷 뒤 30초 넘게 이어지는 원본 자료 영상(Boston Dynamics, 날짜 라벨 + PIP)으로 '휴머노이드 로봇' 주장에 시각 근거를 붙입니다. 이 구간에는 자막 외 그래픽이 없습니다.
- 같은 채널 짝(식스시그마 · low 0.08배 `ej6CLCNjqzM`)은 별도 요청 `thumb-edit-ej6CLCNjqzM`에서 다루므로, 이 문서는 이 영상 단독 관찰만 담았습니다. 채널별 표본 1건이므로 **경향 근거**로만 쓰고 단정은 피해야 합니다.

### 저장
- 비공개 Drive 상대 경로: `ytflow/refs/thumb-study-20261119/FGQApSFoQAc/`
  - 구성: `frames/` PNG **32장**, `thumb-reference.png` 1, `meta.json` 1, `frame-index.md` 1, `script.txt` 1 = **파일 36개 + 하위 폴더 1**.
  - 기존 `thumb-study-20261119` 폴더를 **재사용**했고(새로 만들지 않음), 하위 `FGQApSFoQAc` 폴더가 없던 것을 확인한 뒤 1개만 생성(중복 폴더 없음). 업로드 후 Drive 목록·바이트 합계를 로컬과 대조(32장 30,704,507바이트 일치), 폴더 권한은 소유자 1명(비공개).
- 공개 저장소에는 상태·개수·관찰 요약·비공개 Drive 상대 경로만 기록했고, 캡처 파일·Drive 링크는 올리지 않았습니다.

### 방법·한계
- 방법: 공개 페이지에서 재생 → 일시정지 → 목표 초로 이동(seeked 확인 + 실제 `currentTime` 재확인) → 재생 화면 영역 캡처. 내려받기·스트림 추출·로그인·우회·쿠키 추출 없음.
- 한계: 2초·5초 간격이라 표본 사이에 스치는 자막·모션·이징은 판정 불가(컷 초는 표본 간격만큼 오차). **음성 톤·BGM·발음은 미확인**(원격 브라우저 오디오 청취 불가) — 근거는 화면에 그려진 자막 텍스트·그래픽·스크립트 패널뿐입니다. 심층 분석·매뉴얼 변경은 하지 않았습니다.
