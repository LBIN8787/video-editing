---
name: video-make
description: 주제 선정부터 자료조사, 대본, 소스 탐색, 편집, 자막, 업로드 패키지, 보고서까지 유튜브 영상 1편을 ytflow 파이프라인으로 처음부터 끝까지 만든다. "영상 만들어줘", "이번 주 영상", "자동으로 제작" 같은 요청에 쓴다.
---

# 영상 1편 전체 제작 (ytflow make)

## 준비 (처음 한 번)
1. `pip install -r requirements.txt` 를 실행하고, ffmpeg·node(22+)를 설치합니다. 그다음 `python scripts/install_tools.py` 로 외부 편집 도구(HyperFrames, ffmpeg-skill)를 고정 버전으로 설치합니다.
2. LLM 백엔드를 고릅니다 (`config/pipeline.yaml` → `llm.backend`, 또는 환경변수 `YTFLOW_LLM_BACKEND`).
   - **claude-cli:** Claude 구독. `claude` 로그인이 필요합니다.
   - **codex-cli:** ChatGPT 구독. `codex login` 이 필요합니다.
   - **api:** `ANTHROPIC_API_KEY` 가 필요합니다.
   - **manual:** 에이전트인 당신이 직접 답합니다. 아래 'manual 모드' 참고.
3. 편집 스타일을 고릅니다: `python -m ytflow styles` (두 번째 열이 계열). 먼저 계열을 정합니다.
   - **원본 소스형(source, sixsigma):** 실적발표·인터뷰처럼 당사자의 말이 핵심일 때. 클립을 사용자 PC 에서 `rebuild` 로 받아야 완성됩니다.
   - **자체 제작 인포그래픽형(infographic, mijudiary·moneycrew):** 개념·구조·숫자 비교가 핵심일 때. 클라우드에서 끝까지 완성됩니다.
   스타일 문서는 `styles/README.md`, `styles/<id>/STYLE.md` 에 있습니다.

## 실행
```bash
python -m ytflow make --style-ref <스타일id>                     # 주제 자동 선정
python -m ytflow make --topic "주제" --angle "관점" --style-ref <id>
```
주제는 **트렌드 우선**으로 고릅니다. discover 가 최근 48시간의 여러 매체(Google News 국문·영문, Hacker News, X API 선택)와 이번 주 YouTube 아웃라이어를 모아 `00_source/trends.json` 을 만들고, select 는 여러 매체가 동시에 다루는 가장 새로운 소재를 1순위로 둡니다.
- 키워드는 `config/pipeline.yaml` 의 `discover.seed_keywords`, 영어 검색어는 `trends.english_keywords`, X 감시 계정은 `trends.x_accounts` 에서 정합니다.
- X API 키는 선택입니다. 환경변수 `X_BEARER_TOKEN`, 또는 클라우드 환경의 네트워크 시크릿(api.x.com)으로 넣습니다. 없으면 X 게시물은 research 의 웹 검색으로 찾습니다.

단계 순서: discover → select → research → **article** → script → sources → clips → voice → assets → subtitles → assemble(+마스터링) → package → report.
- **article:** 팩트시트(와 가져온 조사 글)를 형식에 맞는 '읽는 원고' `01_research/article.md` 로 다듬습니다. 롱폼 = 장편 칼럼·보고서 분석, 쇼츠 = 짧은 주제 안내 (`formats/`). script 는 이 원고를 장면으로 나눕니다.
- 채널 단위로 반복 제작할 때는 `skills/channel-run` 을 따릅니다 (`make --channel <id>`, `--from-text <글>`).
중간부터 다시 돌릴 때는 `python -m ytflow stage <프로젝트> <단계>`, 소스를 넣은 뒤에는 `python -m ytflow rebuild <프로젝트>` 를 씁니다.

## manual 모드 (에이전트가 직접 판단할 때)
1. `YTFLOW_LLM_BACKEND=manual python -m ytflow make ...` 를 실행합니다. LLM 이 필요한 단계에서 멈추고 `.llm/requests/<id>.md` 를 남깁니다.
2. 요청 파일을 읽고 답을 `.llm/responses/<id>.json`(또는 `.md`)에 씁니다. JSON 은 요청에 적힌 스키마(`schemas/*.schema.json`)를 지킵니다.
3. 웹 검색이 필요한 요청(자료조사)은 당신의 검색 도구로 출처를 확인합니다. 그리고 `skills/video-research` 규칙을 따릅니다.
4. 멈췄던 단계를 `python -m ytflow stage <프로젝트> <단계>` 로 이어서 실행합니다. 대본을 직접 썼다면 `python -m ytflow validate <프로젝트>` 를 반드시 통과시킵니다.

## 끝난 뒤 확인
- **보고서:** `projects/<프로젝트>/REPORT.md` 에서 '남은 일'(임시 화면, 재확인 필요 팩트)을 사용자에게 알립니다.
- **화면 점검:** `skills/video-edit` 의 프레임 점검을 하고, 문제가 있으면 해당 단계만 다시 돌립니다.
- **커밋:** 기획 문서(md/json/csv)만 커밋합니다. 미디어와 타 채널 화면은 커밋하지 않습니다(.gitignore).

## 지킬 것
- YouTube 봇 확인을 우회하지 않습니다. 클라우드에서 클립 다운로드가 막히면 임시 화면으로 두고, 사용자 PC에서 `rebuild` 하도록 안내합니다.
- 투자 권유 표현을 쓰지 않습니다. 확인되지 않은 숫자는 단정하지 않습니다.
