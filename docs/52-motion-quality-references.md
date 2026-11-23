# 52. 고퀄리티 모션그래픽 레퍼런스 — 디테일을 올리는 요소 (2026-11-20)

> 사용자: "이런 여러 고퀄리티 모션그래픽 레퍼런스 자료들을 추가로 조사해주세요"
> 배경: 월텍남 〈앤트로픽 대실망에, AMD 공매도까지〉 [4:57](https://youtu.be/DsUWN5-FR-4?t=297) 화면(구겨진 종이, 굵은 검정 제목, 손으로 칠한 붉은 금지 표시, 굵은 붉은 붓 자국 '제재 이후' 구간, 금색 핀이 달린 실물형 칩 그림 카드 여섯 장, 붉은 '6개 버전 이상')과 비교해 [설명 무대](51-explain-stage.md)의 렌더가 덜 고급스러워 보인다는 피드백.

이미 본 것은 반복하지 않습니다: 월텍남 해당 편([31](31-motion-grammar.md)), 식스시그마·BBC 코리아·Nerdwriter·Every Frame a Painting·미주일기·Kurzgesagt 다이슨 구·3Blue1Brown·Vox 레오나르도·한스 로슬링·TED-Ed·Pudding·D3 순위 막대([50](50-motion-graphics-editing-references.md)), 기법 카탈로그([32](32-technique-research.md)), 화풍·소재 사이트([39](39-visual-references.md)), 호기심 채널 20곳([47](47-curiosity-channel-benchmark.md)).

## 0. 무엇을 어떻게 확인했나 (정직하게)

- **YouTube 재생 페이지는 클라우드에서 봇 확인(HTTP 429 → google.com/sorry)으로 막혔습니다. 우회하지 않았습니다.** 그래서 영상 안의 정확한 시각에 무엇이 나오는지는 직접 보지 못했습니다.
- 대신 세 가지로 확인했습니다.
  1. **제목·채널**: YouTube 공식 oEmbed 로 영상 ID 와 제목이 맞는지 확인.
  2. **실제 화면 표본**: YouTube 가 공개하는 자동 미리보기 프레임 3장(`i.ytimg.com/vi/<ID>/hq1~3.jpg`). 영상에서 뽑힌 진짜 프레임이지만 **몇 분 몇 초인지는 알 수 없습니다**(월텍남 편으로 대조해 보니 길이의 1/4·1/2·3/4 지점과 맞지 않았음). 표에는 "표본 프레임(위치 미상)"으로 적었습니다.
  3. **시각(&t=)**: rosetta.to 의 대본 요약에 실린 장(chapter) 시작·인용 대사 시각. **그 시각의 화면은 미확인**이며, 대사 내용상 그 부근에 그래픽이 나올 가능성이 높은 곳입니다.
- 제작기(breakdown)·인터뷰는 글로 읽은 내용만 적었고, 원문에 없는 설정값은 지어내지 않았습니다.
- 국내 채널은 장면을 확인할 길이 없었습니다(§3). PC 에서 확인할 요청서 문안을 §3 끝에 두었습니다.

## 1. 해외 영상 — 장면과 가져올 기법

| 장면 | 원본과 확인 위치 | 화면에서 확인한 것 | 제작에서 가져올 기법 |
|---|---|---|---|
| **진짜 종이 공예 소품으로 만든 차트** | Vox 〈Teaching in the US vs. the rest of the world〉 (4:38) · 근무 시간 대사 [0:51](https://www.youtube.com/watch?v=wFqQm1541aA&t=51s) · 장 'Teacher Work Hours' [1:25](https://www.youtube.com/watch?v=wFqQm1541aA&t=85s) · [미술감독 인터뷰(Storybench)](https://www.storybench.org/?p=21229) | 표본 프레임(위치 미상): 미색 종이 판 위에 **종이로 오린 시계**, 시계 일부가 붉은 부채꼴(가장자리 노란 점선)로 채워지고 위에 'UNITED STATES / 9 hours 14 minutes' 굵은 흰 글자. 다른 표본: 종이로 만든 교실 두 칸·국기·나무가 세워진 입체 디오라마, 종이 사이에 **실제 조명이 만든 부드러운 그림자**. 미술감독 조이 센다이디에고는 "아이 공작 같은 색종이 그림"을 일부러 골랐고, 미국과 다른 나라의 근무 시간을 "종이 시계를 파이 차트로" 바꿔 보여 줬다고 설명. | ① 숫자를 **사물(시계)에 담아** 비교 — 시간은 시계, 돈은 지폐 묶음, 물량은 상자. ② 강조 조각은 채움 + **다른 색 점선 외곽**(테두리 하나로 '이 부분'이 읽힘). ③ 실물 촬영 대신: 생성 이미지로 '종이 공예 시계' 판을 만들고(같은 조명 방향), 부채꼴만 SVG `path`(호)로 덮어 GSAP 으로 각도를 키움. 판과 부채꼴 사이에 2겹 그림자. |
| **지도 위 사진 배지·날짜 띠·출처 각주** | Johnny Harris 〈Why This Island Could Trigger World War 3〉 (29:03) · 장 'Civil War' [0:00](https://www.youtube.com/watch?v=x-XdOaZPhBw&t=0s) · 반도체 대사 [27:10](https://www.youtube.com/watch?v=x-XdOaZPhBw&t=1630s) | 표본 프레임(위치 미상): 채도를 낮춘 분홍·회색 지도(바다는 옅은 회색, 미세한 종이 결), 중국 쪽에 **팔각형으로 오린 선전 포스터 사진**(굵은 테두리) + 아래 검은 띠 'COMMUNIST PARTY OF CHINA', 대만 위 작은 원형 휘장과 'TAIWAN'. 위쪽 가운데 검은 날짜 띠 'October 1, 1949 ■ MAO DECLARES A NEW COUNTRY', **왼쪽 아래 아주 작은 출처 각주**(저자·문헌). 27:10 의 칩 장면 화면은 미확인. | ① 지도는 **빼고**(낮은 채도·두 색), 주인공만 사진으로 — 사진은 원·팔각 같은 **기하 모양으로 오려 테두리**. ② 날짜 띠 `날짜 ■ 사건` 한 줄은 우리 사실 규칙(날짜·출처)과 그대로 맞음 → `afterline`·`journey` 공통 부품으로. ③ 출처 각주를 화면 구석에 상시 — 신뢰감이 '고급스러움'의 일부. |
| **지도 제작 과정 전체 (제작기)** | Johnny Harris 〈How I Make My Maps〉 (29:29) · 장: Original Workflow [3:56](https://www.youtube.com/watch?v=GsojLuJpe_0&t=236s) · Geo Layers [11:29](https://www.youtube.com/watch?v=GsojLuJpe_0&t=689s) · Map Comp [12:49](https://www.youtube.com/watch?v=GsojLuJpe_0&t=769s) · Zooming [19:25](https://www.youtube.com/watch?v=GsojLuJpe_0&t=1165s) · Animating [22:14](https://www.youtube.com/watch?v=GsojLuJpe_0&t=1334s) · Labeling [23:28](https://www.youtube.com/watch?v=GsojLuJpe_0&t=1408s) · Finalizing [24:10](https://www.youtube.com/watch?v=GsojLuJpe_0&t=1450s) | 장 목록과 대본(rosetta.to) 기준: 예전 방식은 Illustrator 지도 파일을 After Effects 에 넣고 **null 조종자에 붙여 크기·위치만** 움직임, 색은 색조·채도 효과로. 지금은 GEOlayers 에 Mapbox Studio 로 꾸민 지도를 불러와 **위도·경도·확대·방위(bearing)·기울기(pitch)** 를 키프레임, 방위를 조금 돌려 '공전'하는 카메라, 라벨은 지도에 고정, 마지막에 색보정·LUT. 표본 프레임 3장은 모두 진행자 화면(지도 화면 미확인). | 우리 `journey` 에 **기울기(CSS `rotateX` 10~25°)와 느린 방위 회전(0.5~2°/초)** 를 더하면 평면 지도가 '책상 위 지도'처럼 됨. 라벨은 지도 레이어의 자식으로 두어 같이 움직이게. 최종본에 ffmpeg `lut3d` 로 한 가지 색감을 입히면 장면 간 톤이 맞음. |
| **지도에 종이 질감을 '먹이는' 법** | aescripts 〈[Give your maps a paper texture](https://aescripts.com/learn/give-your-maps-a-paper-texture-in-adobe-after-effects)〉(Boone Loves Video, PQ Grit Kit 사용) · 참고: Johnny Harris 와 일한 지도 애니메이터 제이슨 분의 [팟캐스트](https://bluebird-star-4e83.squarespace.com/episode/jason-boone-animating-maps-for-a-living-working-with-johnny-harris-amp-joining-a-tech-startup-mbm56) | 검색 요약 기준(페이지·영상은 403 으로 직접 못 엶): aescripts 소개는 "변위 맵과 혼합 모드로 지도에 종이 질감". 같은 계열 튜토리얼 요약: 종이 사진을 **곱하기(Multiply)** 로 얹고, 같은 종이를 복제해 지도 아래에 두어 **변위 맵의 조종 이미지**로 씀(종이 굴곡대로 지도 선이 미세하게 휨), 잔 결이 변위를 망치지 않게 변위용 종이에 가우스 흐림. Johnny Harris 의 정확한 설정은 미확인. | 지금 렌더는 종이 사진 위에 요소가 '스티커처럼' 떠 있음. **같은 종이 이미지를 `<feImage>` 로 불러 `feDisplacementMap` 의 in2 로** 쓰면 선·붓 자국이 종이 주름을 따라 휨. 그리고 맨 위에 종이 사진을 `mix-blend-mode:multiply; opacity:.25~.4` 로 한 번 더 깔아 **모든 요소에 같은 결**이 비치게. |
| **Vox 의 작은 질감 장치들** | PremiumBeat 〈Replicating VOX's Motion Graphic Style〉([글](https://www.premiumbeat.com/blog/replicating-vox-motion-graphic/), 2021) · 글이 예로 든 Vox 〈How Jair Bolsonaro brought the far-right to power in Brazil〉 [영상](https://www.youtube.com/watch?v=H1DXtQua074) | 글에서 확인: ① 24fps 편집 안에서 그래픽만 **12fps(두 프레임에 한 번)** 로 움직여 손맛, ② 자막 상자 가장자리를 매끈하게 두지 않고 **거칠게**, ③ 3D 카메라가 **뒤로 빠지며 짧게 흐려지는** 전환, ④ 정지 사진 뒤 배경 질감을 **초당 2~3번 바꿔** 미세하게 움직이게, ⑤ 화면 **가장자리에만 색수차·흐림**. 글의 시각(0:14·1:39·8:54)은 어느 영상인지 밝히지 않아 미확인. 볼소나루 편 표본 프레임: 어두운 바탕에 흑백 인물 사진과 굵은 흰 이름 'Lula da Silva (2003 – 2011)'. | 전부 HTML 로 됨: ① GSAP `ease: "steps(…)"` 또는 타임라인을 1/12초 단위로 반올림(텍스처·손그림 선에만, 카메라는 부드럽게), ④ 종이·잡티 이미지 3장을 0.4초마다 교체(`boil`, 기존 illust 의 boil 과 같은 원리), ⑤ 맨 위에 방사형 마스크로 가장자리만 `blur(1.5px)` + R/B 채널 1~2px 어긋남. ③ 은 다음 장면 들어갈 때 `scale 1→0.92` + `filter: blur(0→6→0px)` 0.35초. |
| **흑백 사진 컷아웃 + 손그림 한 점 + 입체 소품** | Vox 〈Where Sicko Mode's weirdest moments came from〉 (Earworm) [영상](https://www.youtube.com/watch?v=5Ci5XTpPq94) · PremiumBeat 글이 Vox 표본으로 링크 | 표본 프레임(위치 미상): 검은 바탕 우주 같은 공간에 **흑백 인물 사진을 오려** 옷만 옅은 청록으로 물들이고, 머리 위에 **노란 손그림 왕관**(검은 외곽선), 주변에 회색 입체 스피커 상자가 떠 있음, 작은 노란 빛 점. | 월텍남의 '붉은 손칠 금지 표시'와 같은 문법: **사실 자료(사진)는 무채색, 해석·강조는 손그림 한 가지 색**. 우리 `bite`·`docspot` 의 인물 사진에 흑백 + 한 색 손그림(동그라미·왕관·X)을 얹는 규칙으로. |
| **속이 빈 큰 숫자 + 위에서 본 소품** | PolyMatter 〈Why Apple Can't Leave China (yet)〉 (18:12) · 장 The Scale Challenge [2:38](https://www.youtube.com/watch?v=-JbIOGGTRTY&t=158s) · Apple's Inventory Problem [3:56](https://www.youtube.com/watch?v=-JbIOGGTRTY&t=236s) · '하루 비즈니스석 50석' 대사는 9~11분 부근(요약 추정, 시각 미확인) | 표본 프레임(위치 미상): 짙은 붉은 그라데이션 + 흐린 비행기 사진 바탕, **외곽선만 있는 거대한 '50'**, 그 앞에 **위에서 내려다본 흰 비행기 동체**(좌석 줄이 보임), 왼쪽 위 작은 비행기 아이콘과 곡선 경로 끝 'SAN FRANCISCO / USA'. | ① 숫자는 **채우지 않고 굵은 외곽선**으로 깔고 그 앞에 소품을 겹치면 숫자·사물이 한 덩어리로 읽힘(SVG `text` 에 `fill:none; stroke-width:6`). ② 소품은 **한 시점(위·정면)으로 통일**. ③ 바탕은 단색 대신 **같은 계열 그라데이션 + 흐린 실사**(사진 `blur(18px)`, 불투명도 .3). |
| **같은 물건을 겹쳐 '여러 개'를 보여 주기** | PolyMatter 〈How China Won the Electric Vehicle Race〉 (17:00) · 장 The Oil Problem [2:19](https://www.youtube.com/watch?v=8-NcTawauXA&t=139s) · Enter Electric Vehicles [4:46](https://www.youtube.com/watch?v=8-NcTawauXA&t=286s) · The Red Carpet [9:39](https://www.youtube.com/watch?v=8-NcTawauXA&t=579s) | 표본 프레임(위치 미상): 붉은 바탕(가장자리 어둡게, 큰 원형 빛망울)에 **초록 번호판 두 장이 비스듬히 겹쳐** 있고, 뒤 판은 아래로 밀려 일부만 보임. 번호판은 둥근 모서리·볼트 구멍·옅은 하이라이트·아래쪽 그림자까지 그린 **실물형 일러스트**. | 월텍남 '칩 카드 여섯 장'의 고급판: 카드를 같은 간격으로 늘어놓기 전에 **한 장을 크게 보여 준 뒤 뒤로 겹쳐 쌓이며** 개수가 늘게. 소품은 볼트·하이라이트·그림자 같은 **작은 실물 디테일 3개**가 있어야 '아이콘'이 아니라 '물건'으로 보임. |
| **플랫 일러스트에 빛을 넣는 법** | Kurzgesagt 〈SOUTH KOREA IS OVER〉 (14:46) · 장 Population Projections [2:16](https://www.youtube.com/watch?v=Ufmu1WD2TSk&t=136s) · Economic Collapse [3:27](https://www.youtube.com/watch?v=Ufmu1WD2TSk&t=207s) · The Root Causes [4:40](https://www.youtube.com/watch?v=Ufmu1WD2TSk&t=280s) | 표본 프레임(위치 미상): 'KORAIL' 기관차가 정면으로 달려오고 뒤에서 **방사형 빛줄기**, 새 캐릭터들이 올라탐. 다른 표본: 한복 짓는 노인·도자기 빚는 노인 두 칸 나눈 화면(각 칸 다른 바탕색), 위에서 비스듬히 본 도로·버스·자동차. 평면 도형이지만 **면마다 밝은 쪽·어두운 쪽 두 톤**, 바탕은 그라데이션. 한국을 다룬 편이라 소품(코레일·한복·백자)이 우리 시청자에게 바로 읽힘. | 아이콘을 '평면 + 한 색'으로 두지 말고 **면마다 하이라이트 한 톤·그늘 한 톤**(SVG 에 `linearGradient` 하나, 또는 같은 모양 복제 후 위쪽 절반 흰색 .15). 주목해야 할 물건 뒤에만 **빛줄기·후광**. 화면 둘로 나눌 때 칸마다 바탕색을 달리해 비교. |
| **사진을 '인화된 사진'으로 두기** | Johnny Harris 〈Why Groceries Are SO Expensive Now〉 (26:56) · 장 The Journey of Your Food [5:11](https://www.youtube.com/watch?v=wyo1u9WxUG4&t=311s) · Why Food Is Getting So Expensive [11:25](https://www.youtube.com/watch?v=wyo1u9WxUG4&t=685s) · 이익률 대사 [14:52](https://www.youtube.com/watch?v=wyo1u9WxUG4&t=892s) | 표본 프레임(위치 미상): 성조기 바탕 위에 아이젠하워 사진이 **흰 테두리가 있는 인화지**처럼 놓임. 나머지 표본 2장은 진행자·인터뷰(그래픽 장면 미확인). | 공공 기록 사진(PD)을 화면에 넣을 때 **흰 테두리 12~20px + 2겹 그림자 + 회전 −2~3°** 만으로 '자료를 책상에 올려놓은' 느낌. 이미 `archive` 계열에 쓰는 사진에 바로 적용 가능. |

## 2. 제작기 — 디테일을 어떻게 만드나 (글로 확인)

| 무엇 | 출처 | 확인한 내용 | 우리에게 |
|---|---|---|---|
| WSJ 웹 일러스트 3겹 구조 | Storybench 〈WSJ built a series with artful animations〉 [글](https://www.storybench.org/wall-street-journal-built-series-artful-animations-investigative-series/) (〈The Unraveling of Tom Hayes〉, 2015) | 장면마다 **정지 JPEG 바탕 + SVG 인물 + 움직이는 선** 세 겹. 일러스트레이터의 포토샵 파일을 분해해 SVG 로 만들고, 실이 풀리는 선은 Snap.svg 로 그리며 **Verlet 물리**로 한 점에 고정된 채 늘어나 늘어지게 함. 물리 최적화가 가장 어려웠다고. | 생성 이미지 한 장을 **바탕 / 움직일 소품 / 선** 세 겹으로 나누는 것이 핵심(docs/38 의 레이어 분리와 같은 결론). 매달린 줄·늘어지는 선은 간단한 Verlet 몇 줄로 '진짜 물체' 느낌. |
| Vox 미술감독의 원칙 | Storybench [Vox 인터뷰](https://www.storybench.org/?p=21229) | 미술감독은 **대본 단계부터** 참여해 "무엇이 가장 보여 줘야 할 것인가"를 묻는다. 주제마다 화풍을 바꾼다(종이 공예, AI 편은 떠다니는 글자, 사진이 없을 땐 시위 포스터 양식). **지나친 광택은 광고처럼 보인다**고 경계. 지도는 국경 정확성 검수가 따로 붙는다. | '고급스러움'은 광택이 아니라 **재료의 일관성**. 편마다 재료(종이·포스터·사진 인화)를 하나 정해 끝까지. 지도 국경·지명은 사실 검수 대상. |
| 종이를 진짜처럼 | befores & afters, 다니엘 기스(종이 캐릭터 연출) [인터뷰](https://beforesandafters.com/2022/10/03/heres-how-one-director-tackled-the-delicate-art-of-rendering-characters-made-of-paper/) | 라이트 테이블에 종이를 비춰 보고 **스캔·촬영한 종이를 투과 질감**으로 사용(뒤에서 빛이 오면 반대편 그림이 비침). 두께를 변위로 주면 가장자리가 가죽처럼 부풀어 실패 → 주름·움푹한 곳을 조각한 고해상도 종이를 덮음. 손그림 실수를 지우지 않고 살림. | 카드·종이 조각 가장자리를 두껍게 부풀리지 말 것(변위 `scale` 은 선에만, 종이 판 테두리는 얇게). 실수·떨림을 일부 남기는 편이 진짜 같음. |
| 표지 그림을 움직이게 나누기 | Talking Biz News 〈How The Economist covers come alive〉 [글](https://talkingbiznews.com/they-talk-biz-news/how-the-economist-covers-come-alive/) | 이코노미스트 표지 애니메이션은 일러스트레이터가 **움직일 부분(손·팔)을 따로 그려** 넘기고, 모션 담당이 겹을 쌓아 배경 디테일을 더함. 한 주 일정(화 아이디어 → 수 확정 → 목 공개). | 그림 주문서(`art-brief`)에 **움직일 부품을 미리 적어** 따로 그리게 하면 나중에 자르는 비용이 줄어듦. |
| Vox 지도의 3D 위성 화면 | Google Earth 블로그(이미 docs/50 에 인용) | — | 반복 생략. |

## 3. 국내 채널 — 확인 범위

| 채널 | 확인한 것 | 확인 못 한 것 |
|---|---|---|
| **MBC 14F(일사에프)** | 팀 인터뷰에서 "빠른 편집에 밈과 인서트 영상, **이해를 돕는 모션 그래픽**을 많이 활용", "기획부터 촬영·편집·모션까지 시청자 이해를 위해" ([패스트캠퍼스 인터뷰](https://fastcampus.co.kr/media_article_14f), [기자협회 인터뷰](https://journalist.or.kr/news/article.html?no=53063)) | 도구·질감 규칙·특정 영상의 장면 |
| **EBS 지식채널e** | 내레이션 없이 **사진(스틸)·자막·음악**만으로 5분 안팎 ([세계일보](https://www.segye.com/newsView/20250916514275), [주간경향](https://weekly.khan.co.kr/article/17558)) — 글자가 곧 화면인 키네틱 계열의 교과서 | 자막 글꼴·조판 |
| 슈카월드 · 머니인사이드 · KBS 크랩 · 비디오머그 · 스브스뉴스 · 엠빅뉴스 · 삼프로TV | 제작 방식 인터뷰·제작기를 찾지 못함. 크랩은 "빠른 편집과 밈" 정도로만 소개됨([에스콰이어](https://www.esquirekorea.co.kr/article/1896497)) | **장면 전부 미확인** — 클라우드에서 영상 확인 불가 |

국내 장면은 PC 에서 확인해야 합니다. AGENTS.md 의 '막히는 일은 피클에게' 규칙에 맞춘 요청서 문안(파일은 만들지 않았음):

```
inbox/requests/<KST 시각>-kr-motion-refs.md
목적: 국내 경제·시사 채널의 '소품·종이·붓' 모션그래픽 장면 확인 (docs/52 §3)
채널: 슈카월드, 머니인사이드, KBS 크랩, 14F, 비디오머그, 스브스뉴스
요청: 채널마다 최근 경제·반도체·무역 편 1편 → 모션그래픽 구간 3곳을 정지 캡처(ego lite, 내려받기 없음)
기록: 영상 제목·URL·시각(초) / 바탕 재질 / 소품이 아이콘인지 실물형 그림인지 / 그림자 / 강조색 / 글꼴 굵기
결과: inbox/requests/done/ 에 캡처 목록과 메모
```

## 4. 디테일을 올리는 요소 — 효과 큰 순서

지금 설명 무대(`ytflow/stages/explain.py`)는 이미 실사 구겨진 종이 바탕, Black Han Sans, 붓 필터(`feTurbulence`+`feDisplacementMap`), 카드 3겹 그림자를 갖고 있습니다. 레퍼런스와의 차이는 아래 순서로 큽니다.

| 순위 | 요소 | 지금 | 레퍼런스에서 본 것 | HTML·SVG·GSAP 로 하는 법 |
|---|---|---|---|---|
| 1 | **소품 그림의 재질** | 칩·상자 등은 `icons.svg_markup` 의 평면 아이콘 | 월텍남 금색 핀 칩, PolyMatter 번호판·비행기, Kurzgesagt 두 톤 면 — **볼트·하이라이트·그림자 같은 실물 디테일** | 소품은 생성 이미지(투명 배경, "top-left soft light, subtle contact shadow, editorial illustration" 고정 문구, docs/28 `art-gen`)나 PD 사진 컷아웃으로. 한 편 안에서 **같은 광원 방향·같은 화풍**. 아이콘을 쓸 땐 최소 `linearGradient` 두 톤 + 하이라이트 선 하나. |
| 2 | **모든 요소가 같은 종이 위에 있게** | 종이 사진 위에 요소가 스티커처럼 얹힘 | Johnny Harris·Boone 의 곱하기 + 변위, Vox 종이 공예의 실제 그림자 | ① 맨 위에 종이 사진 `multiply` .25~.4 한 겹 더. ② 같은 종이를 `feImage` 로 불러 붓·선의 `feDisplacementMap` 입력으로(주름 따라 휨). ③ 화면 가장자리 비네트 + 왼쪽 위가 밝은 **불균일 조명**(방사형 그라데이션 `soft-light`). |
| 3 | **빛 하나, 그림자 두 겹** | 카드에만 3겹 그림자 | 종이 디오라마의 부드러운 그림자, PolyMatter 번호판 아래 그림자 | 소품마다 **접지 그림자(작고 진함) + 확산 그림자(크고 옅음)**, 방향은 한 편 내내 같게(오른쪽 아래). 붓 자국·글자에는 아주 옅은 것만. 물체가 '떠오를 때' 그림자가 커지고 옅어지게 GSAP 로 함께 움직이면 깊이가 생김. |
| 4 | **붓·잉크 가장자리의 실감** | 필터로 가장자리를 흔들고 가로 결을 입힘 | 손으로 칠한 금지 표시, 굵은 붓 구간, Vox 의 거친 자막 상자 | 붓 자국은 **실제 붓 스캔 PNG(CC0)를 마스크**로 쓰고, 드러나는 방향은 붓질 방향으로(`mask-position` 또는 `clipPath` 사각형을 GSAP 로 늘림). 선은 perfect-freehand(MIT)로 **굵기가 변하는 획**을 만들고 `stroke-dashoffset` 로 그림. 끝부분 갈라짐은 마스크 PNG 로. |
| 5 | **움직임의 질감** | 등장이 부드러운 보간 위주 | Vox 12fps 손맛, 질감 2~3회/초 교체 | 카메라·이동은 부드럽게(`expo.out`, `back.out(1.4)` 로 살짝 넘침), **손그림·질감만 `steps`/12fps**. 종이 잡티 오버레이 3장을 0.4초마다 교체. 여러 개는 `stagger` 0.08~0.12초. |
| 6 | **카메라** | 장면 안 카메라 거의 없음 | Johnny Harris 기울기·공전, Vox 뒤로 빠지며 흐려지는 전환 | 박자마다 **2~4% 천천히 밀기**, 바탕·소품·글자 3겹을 다른 속도로(시차). 장면 바뀔 때 뒤로 빠지며 0.3초 흐림. 지도는 `rotateX` 기울기. |
| 7 | **타이포 마감** | 굵은 글꼴, 그림자 선택 | 날짜 띠·출처 각주(Johnny Harris), 외곽선 숫자(PolyMatter) | 검정은 순흑 대신 `#1d1d1f`, 굵은 제목에 `xink` 를 아주 약하게(`scale` 1~2, 인쇄 번짐). 숫자는 채움/외곽선 두 가지를 의미로 구분. 화면 구석 **출처 한 줄·날짜 띠**를 고정 부품으로. |
| 8 | **최종 마감** | 장면별 색 그대로 | Johnny Harris 색보정·LUT, Vox 가장자리 색수차 | 완성 MP4 에 ffmpeg 로 **한 LUT + 아주 옅은 필름 그레인(`noise=alls=4:allf=t`) + 비네트**. 가장자리만 색수차 1px. |
| 9 | **소리** | 내레이션·BGM | (레퍼런스의 효과음은 이번에 측정 못 함) | 종이 바스락·도장 쿵·마커 슥 같은 **소품 재질에 맞는 효과음**을 등장 시점에. 효과음 출처는 라이선스 확인 후(media-use 스킬). |

**한 줄 요약:** 1·2·3(재질 있는 소품, 같은 종이, 일관된 빛)이 '저퀄' 인상의 대부분입니다. 4~9 는 그 위에 얹는 마감입니다. 하나씩 넣을 때마다 같은 장면(월텍남 4:57 대응 `afterline`)을 다시 렌더해 전후를 비교하는 것을 권합니다.

## 5. 디테일용 소재와 라이선스

큰 이미지 파일은 Git 이 아니라 캐시·Drive 에 둡니다(AGENTS.md 저장 규칙). Git 에는 출처·라이선스·파일 이름만.

**종이·질감**

| 소재 | 라이선스 | 메모 |
|---|---|---|
| [ambientCG](https://ambientcg.com) — Paper, Cardboard 등 | **CC0 1.0** ([원문](https://docs.ambientcg.com/license/)) — 상업 사용·수정·재배포 가능, 출처 불요 | 구겨진 종이 사진 텍스처. 1순위 |
| [Poly Haven](https://polyhaven.com) 텍스처 | **CC0** ([원문](https://polyhaven.com/license)) — 에셋만 CC0, 사이트 로고·렌더 예시는 아님 | 종이·판지 종류는 적음, 나무 책상 바탕 등 |
| [Textures.com](https://www.textures.com) 무료 계정 | 상업 사용 가능, **재배포 금지** ([FAQ](https://www.textures.com/faq-license), [약관](https://www.textures.com/about/terms-of-use)) — 영상 사용은 명시 없음(추정 허용) | 파일 자체를 공개 저장소·Release 에 올리면 안 됨 |
| [OpenGameArt 〈100 grunge brushstrokes and splatters〉](https://opengameart.org/content/100-grunge-brushstrokes-and-splatters-set) | **CC0** | 붓 자국·물감 튐 PNG → 마스크용 |
| freesvg.org 〈[Patterns for Paintbrush imitation #01](https://freesvg.org/patterns-for-paintbrush-imitation-01)〉·〈[#02](https://freesvg.org/patterns-for-paintbrush-imitation-02)〉·〈[brush stroke 2](https://freesvg.org/brush-stroke-2)〉 | **Public Domain(CC0)** 표기 | 경로를 따라 늘이는 마른 붓 패턴(Inkscape) |
| SVG Repo·Vecteezy·Icons8 붓 자국 | 항목마다 다름(출처 표기 필요·유료 섞임) | 개별 확인 전에는 쓰지 않음 |

**굵은 한글 글꼴** (모두 영상 사용 가능, 글꼴 파일을 따로 파는 것만 금지 — OFL 공통)

| 글꼴 | 라이선스 | 메모 |
|---|---|---|
| Black Han Sans | SIL OFL 1.1 (Google Fonts) | 지금 설명 무대 제목. 월텍남류 '두꺼운 검정 제목'에 가장 가까움 |
| Do Hyeon (배민 도현) | SIL OFL 1.1 (Google Fonts) | 둥근 굵은 고딕, 덜 공격적 |
| Pretendard Black(900) | SIL OFL 1.1, 예약 이름 Pretendard ([저장소](https://github.com/orioncactus/pretendard)) | 라벨·숫자. 가변 글꼴이라 굵기 단계 조절 쉬움 |
| SUIT Heavy(900) | SIL OFL 1.1 ([저장소](https://github.com/sun-typeface/SUIT)) | 숫자 모양이 좋음, 표·데이터 라벨 |
| G마켓 산스 Bold | SIL OFL 1.1로 안내(산돌구름), 'GmarketSans' 이름은 상표 — 수정본에 원래 이름 사용 불가 | 배포처마다 표기가 달라 **동봉 라이선스 파일 확인 후** |
| Noto Sans KR Black | SIL OFL 1.1 | 예비 |

**코드·필터 참고**

| 무엇 | 라이선스·출처 | 쓰는 곳 |
|---|---|---|
| perfect-freehand | MIT ([README](https://cdn.jsdelivr.net/npm/perfect-freehand@1.2.3/README.md)) | 굵기가 변하는 붓·펜 획 윤곽 |
| rough.js · GSAP | 이미 도입(`tools/external.json`, docs/32) | — |
| Codrops 〈[SVG Filter Effects: Creating Texture with feTurbulence](https://tympanus.net/codrops/2019/02/19/svg-filter-effects-creating-texture-with-feturbulence/)〉 | 글 | 노이즈 + 조명(`feDiffuseLighting`)으로 종이 결 만들기 |
| Smashing 〈[A Deep Dive Into SVG Displacement Filtering](https://www.smashingmagazine.com/2021/09/deep-dive-wonderful-world-svg-displacement-filtering/)〉 | 글 | 변위 필터 가장자리 들쭉날쭉 문제 다루기 |

## 6. 다음 단계 제안 (사용자 결정)

1. §4 의 1~3(실물형 소품 그림 · 종이 한 겹 더 · 빛 하나 그림자 두 겹)을 `afterline` 한 장면에만 넣어 **전후 비교 2장**을 만듭니다. 소품 그림 생성은 유료일 수 있어 승인 후.
2. 국내 채널 장면은 §3 요청서를 피클에게 보내 PC 에서 캡처합니다.
3. 마음에 드는 것을 고르시면 [연출 기법 등록부](../styles/techniques.yaml)에 '스타일 기본값' 층으로 올립니다(금지·MUST 아님).
