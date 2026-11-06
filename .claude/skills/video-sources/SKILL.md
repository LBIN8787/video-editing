---
name: video-sources
description: 대본 장면에 쓸 원본 영상과 기사 캡처를 찾아 넣는다. 검색어로 YouTube 영상·구간을 고르고(sources), 구간만 내려받고 기사 헤드라인을 캡처한다(clips). 다운로드가 막히면 임시 화면을 두고 PC 에서 rebuild 하도록 안내한다.
---

# 소스 탐색과 확보 (sources → clips)

## 0. 소스 먼저 (scout) — 주제를 고르기 전에
`python -m ytflow stage <프로젝트> scout`: 채널의 `sourcing.start_from` 에 따라 화제별 소스를 먼저 찾습니다(`docs/07-sourcing.md`).
- **statement** (원본 소스형): CNBC·블룸버그·야후·폭스 비즈니스 공식 채널의 최근 10일·4분 이상 영상 목록 → 인물 발언 → 공시·데이터로 확인할 거리
- **document** (칼럼형): 기업 연구·논문·IR·SEC·정부·연구소 문서 + 위키미디어 공용 CC 사진
- **data** (데이터형): 시세 티커·통계 지표 + 비교할 과거 시기
- 다른 해설 유튜버의 영상은 소스로 쓰지 않습니다. 인물 본인·회사·방송사·주최 기관의 공식 채널만.
주제가 정해지면 `00_source/inventory.md`(S번호 소스 목록)가 만들어지고, 원고·대본이 이 목록으로 장면을 짓습니다(`source_ref`).

## 계열별 차이
- **원본 소스형(source):** 이 단계가 영상 품질을 좌우합니다. 검색어는 인물 이름 + 행사·매체 + 시기로 씁니다
  (예: "Susan Li Meta Q3 2026 earnings call", "Jensen Huang CNBC interview November 2026"). 공식 실적발표·키노트 → 주요 방송 인터뷰 순으로 고릅니다.
- **인포그래픽형(infographic):** 원본 영상 장면이 적어 대부분 기사 캡처만 확보합니다.

## 1. 영상 고르기: `python -m ytflow stage <프로젝트> sources`
- **대상:** `source.query` 가 있고 url 이 빈 장면에 YouTube 검색으로 영상과 구간을 채웁니다.
- **선정 기준:**
  - 제목과 검색어가 맞는 정도가 최소 0.3 이상이어야 합니다.
  - 그중 `config/pipeline.yaml` 의 `sources.prefer_channels`(공식·주요 언론)를 우선합니다.
  - 같은 영상을 다시 쓰면 구간이 겹치지 않게 뒤로 밉니다.
  - 이번 주 업로드를 먼저 찾고(`sources.recent_first`), 관련 영상이 2개 미만이면 전체 기간에서 보충합니다.
- **결과 확인:** `04_assets/sources.csv` 를 열어 영상이 장면 내용과 맞는지 확인합니다. 틀리면 `scenes.json` 의 `source.url/start/end` 를 직접 고치고, `query` 를 더 구체적으로 바꿔 다시 실행합니다.

## 2. 내려받기·캡처: `python -m ytflow stage <프로젝트> clips`
- **YouTube:** 지정 구간만 `04_assets/scene_XXX.mp4` 로 받습니다(원음 포함).
- **기사·공시 URL:** 헤드라인 부분을 `scene_XXX_shot.png` 로 캡처합니다(`ytflow/assets/capture.js`, Playwright).
- **X 게시물 URL** (`x.com/<계정>/status/<id>`): 공식 임베드(oEmbed)로 게시물 카드를 그려 캡처합니다. 로그인·스크래핑은 쓰지 않습니다.
- **실패하면:**
  - YouTube 클립은 그 영상의 공개 썸네일로 `scene_XXX_temp.jpg` 임시 화면을 만듭니다(노란 '임시' 표시).
  - 접근을 막는 사이트(403, 보안 확인)는 실패로 남깁니다.

## 3. PC 에서 실제 클립 채우기
- 클라우드 서버에서는 YouTube 가 영상 다운로드를 봇 확인으로 막습니다. **우회하지 않습니다.**
- 사용자 PC 에서 `python -m ytflow rebuild <프로젝트>` 를 실행하게 합니다.
- 봇 확인이 뜨면 `clips.cookies_from_browser: chrome` 을 설정합니다.
- 그래도 실패한 구간은 `04_assets/clips.csv` 의 URL·구간으로 직접 받아 `04_assets/scene_XXX.mp4` 로 넣고 다시 rebuild 합니다.

## 저작권·윤리
- 뉴스·인터뷰는 짧게 인용하고 해설을 붙이며, 출처 라벨을 반드시 답니다.
- 공식 채널(기업·정부)을 우선합니다.
- 받은 미디어와 타 채널 화면은 저장소에 커밋하지 않습니다.
