# AGENTS.md — ytflow (영상편집 자동화)

이 저장소는 **유튜브 영상 제작 워크플로우**를 코드와 문서로 담은 것입니다.
조사해서 글로 정리하던 일(대화형 LLM 의 답을 다듬던 일)을 이어서, 그 글을 **원고 → 대본 → 화면 → 영상**으로 바꾸는 반복 제작 라인입니다.
롱폼은 장편 칼럼·보고서 분석, 쇼츠는 짧은 주제 안내입니다. 채널은 사람의 욕망 하나로 나뉘고(`channels/brands.yaml`), `channels/<id>/` 는 그 아래의 제작 라인(형식 + 기본 편집 스타일)입니다.
**순서: 소스 먼저 → 소스가 강한 주제·형식 결정 → 글(원고) → 소스에 맞춘 편집 → 편집 스타일은 그 위에.**
서술할 내용이 많고 자세한 분석이면 롱폼, 한 가지를 알려 주는 정보형이면 쇼츠로 나눕니다(다른 형식 소재는 그 채널 대기열로).
주제 선정 → 소스 탐색 → 자료조사 → 대본 → 편집점 → 편집 스타일 → 자막 → 업로드 준비 순서로 진행합니다.
Claude Code, Codex 등 어떤 코딩 에이전트든 이 파일과 `skills/` 를 따라 **같은 절차로** 작업합니다.

## 가장 먼저: 제작 매뉴얼 (`manual/`)
**새 세션·새 모델은 `manual/README.md` 부터 읽습니다.** 네 채널은 사람의 욕망으로 나뉩니다 (`channels/brands.yaml`):
**ai**(AI 를 더 잘 다루고 싶다) · **market**(돈의 흐름을 알아 이기고 싶다) · **curiosity**(궁금증을 풀고 싶다) · **issues**(세상이 어떻게 돌아가는지 알고 싶다).
한 편마다 `01_research/topic_brief.json`(욕망 → 트리거 → 질문 → 주제)을 먼저 쓰고, 단계마다 `python -m ytflow check <프로젝트>` 를 통과해야 다음으로 갑니다.
사용자 검토 결과는 `python -m ytflow review <프로젝트> --pass | --reject "이유"` 로 기록하고, 기각 사유는 매뉴얼 기준으로 바꿔 `manual-bump` 로 버전을 올립니다 (`manual/CHANGELOG.md`, 스냅샷 브랜치 `manual/vN`).

## 먼저 읽을 것
| 하려는 일 | 읽을 파일 |
|---|---|
| **대본 매뉴얼 — 대본이 언제나 1순위 (v82, 2026-11-21 사용자: "앞으로는 주제선정과 대본작성 자체를 1순위로 후에 그에 맞춘 연출을 하세요. 즉 언제나 가장 우선순위는 대본이며 대본의 메뉴얼을 구체화하세요")** — 쓰기 전 여섯 가지·전진하는 대본·사실과 해석 대조표·유형별 중심축·D2 반복, D2 통과 전 그림·음성·렌더 없음 | `manual/13-script.md` (채널 문서의 대본 절보다 먼저) |
| **제작 매뉴얼 (욕망 → 주제 → 조사 → 대본 → 연출 → 검사)** | `manual/README.md` → `manual/01~12` |
| **편집 스타일 등록부·자동 추천** (상황에 맞는 스타일, 파일 하나로 늘림) | `styles/recipes/`, `python -m ytflow style-pick <프로젝트>`, `manual/07-extend.md` |
| **스타일 풀 늘리기** (조사·후보·라이선스, 새 장면 chat·terminal·zoomshot·choropleth·mark, 세로 쇼츠 Claude 판) | `docs/17-style-pool.md`, `skills/edit-style-pool`, `python -m ytflow short <프로젝트>` |
| **시사·역사 채널** — 기존 스페인독감 편처럼 실제 자료·지도·연표·비교로 사건을 설명 | `manual/08-issues.md` §0-3, `channels/ch-issues/` |
| **표현 방식과 인포그래픽 레퍼런스** — 인포그래픽·삽화·인물 사진·자료 영상 선택 | `manual/12-visual-storytelling.md`, `manual/05-style-matching.md` §2 |
| **배경 후보·채널별 검토 (조사 기록)** | `docs/21-background-styles.md`, `docs/20-channel-review.md`, `docs/19-manual-gaps.md`, `manual/05-style-matching.md` §0-4, `ytflow/stages/edit10.py` |
| **카테고리 개성 (v15)** — 채널을 묶어도 카테고리마다 다른 화면: 시사 증거판·시장 대시보드·호기심 칠판·AI 앱 창, 장 표지 사진은 주제에 맞게 듀오톤 | `channels/brands.yaml` 의 `identity`, `manual/05-style-matching.md` §0-7, `ytflow/stages/identity.py`, `python -m ytflow archive commons "검색어"` |
| **매일 브리핑 (v17)** — 시장: 전날 시장을 크게 움직인 이슈·보고서·전망·실적 / 시사: 전날 구조적 이슈 하나 | `manual/03-market.md` §0, `manual/08-issues.md` §0-2, `channels/ch-market-daily`, `ch-issues-daily`, `ytflow/stages/daily.py` |
| **이어 읽는 시장 — 매일 운영 매뉴얼 (v19)** — 하루 시간표, SAVE(오선) 소식 확인(§3-0, `inbox/save/`, docs/28 §1), 원인별 1차 출처, 대본 장면표·고정 문구, 업로드 순서, 예외 대응 | `manual/09-market-daily.md`, `python -m ytflow yt-pack <프로젝트>` |
| **머니크루 수준의 깊이 (v33)** — 주제 선정(다른 층·한국 계좌로 귀결·큰 사건은 각도별 연속), 대본 뼈대 11단계(반전 숫자→원문 해부→메커니즘→계산→같은 틀 역사 비교→틀리는 경우→기준선 신호), 깊이 기법 7 | `docs/31-moneycrew-reverse.md`, `manual/03-market.md` §0-4 |
| **뻔한 사실 말고 자료를 엮어서 (v26, 시장 분석·심층·주간)** — 알려진 것(`known`) 대신 엮어야 보이는 것(`new_angle`)으로 제목·훅, 팩트시트 `## 자료 지도`(보고서·발언·행동을 날짜 순, 자료마다 의미)·`## 매체 프레임`(국내·해외 매체가 어떻게 다뤘나), 말과 행동 맞대기 | `manual/03-market.md` §0-2, `manual/09-market-daily.md` §2·§5 |
| **사람·매체 인사이트 + 인터뷰·방송 영상 소스 (v36, 2026-11-17)** — 사실 ✅ / 인사이트 💭 / 해석 💬 를 나눠 이름 있는 사람·매체의 시각을 모으고(`## 인사이트`), 인터뷰·방송은 공식 채널에서, 권리별 길이로 인용(v80: 공공·본인/회사 공식은 길이 제한 없음, 방송사는 짧게, 신고·경고 권리자는 `config/rights_blocklist.yaml` 로 막음 — `## 영상 소스`, `bite`), 원본이 없으면 인용 카드로 | `manual/09-market-daily.md` §3-4·§3-5, `ytflow/stages/hybrid.py` `bite_fallback` |
| **인사이트 수집 (2026-11-26)** — 사람이 아니라 '앞으로에 대한 판단'을 넓게: 기술·시장 인사이트가 나오는 자리(팟캐스트·강연·방송·회사 공식) + 목록 밖(조회가 튄 인터뷰·해커뉴스)을 매일 훑어 주제별 판단 장부 → 영상 후보(판단 + 반대 판단 + 원본). 분석 영상의 주어는 소식이 아니라 그 판단(09 §5-00) | `docs/70-insight-collection.md`, `manual/09-market-daily.md` §3-0-3·§5-00, `config/insight_venues.yaml`, `python -m ytflow insights`, `inbox/insights/` |
| **기술 분석·미래 전망 + CEO 소식 (v42, 2026-11-17)** — 시장 채널이 기술이 어디로 가는지도 다룸(로드맵·학회·리서치 → 누가 이기나·시간표·틀리는 경우), CEO 의 공개 발언·공식 행동을 1차 출처로 모음(`config/ceo_watch.yaml`, 팩트시트 `## CEO 소식`) | `manual/09-market-daily.md` §2-2·§3-4-2 |
| **뉴스레터 소재 (2026-11-15)** — 구독한 무료 뉴스레터를 매일 모아 채널별 소재 목록(제목·링크·분류만). SAVE 와 같은 '단서' 자리: 문장을 옮기지 않고 숫자·발언은 1차 출처로 | `docs/36-newsletters.md`, `manual/09-market-daily.md` §3-0-1, `inbox/newsletters/`, `python -m ytflow newsletters` |
| **유튜브 올리기·관리 자동화** — 업로드·설명란(더보기)·태그·카테고리·예약 공개·썸네일·자막·재생목록 (공식 API, GitHub Actions) | `docs/24-youtube-publish.md`, `python -m ytflow yt-publish <프로젝트>`, `scripts/youtube_auth.py`, `.github/workflows/youtube-publish.yml` |
| **주식 채널 개설 계획** — 이름 후보(겹침 확인)·1일 1영상 운영(처음 계획 — 지금 운영은 `manual/09-market-daily.md` §0-00: 평일·토요일은 주제 쌓기(영상 없음, 2026-11-25 사용자), 분석은 쌓였을 때·큰 날·원본 발언이 나올 때, 일요일 한 주 종합) | `docs/23-stock-channel-plan.md`, `channels/ch-market-daily/channel.yaml` |
| **어닝콜 해부·연결과 의미 (v18)** — 숫자·약속 → 시장의 걱정과 경영진의 답(원문+번역) → 무엇으로 이어지나(해석) → 남은 숙제 | `manual/03-market.md` §0-1, `ytflow/stages/earnings.py` |
| **호기심 채널: 설명보다 호기심 먼저 (v18)** — 첫 문장부터 훅(답은 숨김, 인트로 없음 v24) → 이야기, 제목은 훅에서 | `manual/04-curiosity.md` §0, `topic_brief.hook` |
| **원본 발언 컷편집 (v20)** — 어닝콜·기자회견 긴 원본에서 대본과 맞는 문장만 단어 단위로 잘라 그 사람의 목소리로 (`bite` 장면, 원문·번역 2단) | `styles/source-cut/STYLE.md`, `skills/edit-style-source-cut`, `python -m ytflow cut <프로젝트>`, `ytflow/stages/cutedit.py` |
| **손그림 삽화 (v20)** — 삽화 한 장 위를 카메라가 박자마다 옮겨 가며 설명 (붓 쓸기 등장·boil·손그림 표시·생각 풍선, 그림체는 자유). 그림은 사람이 준비 | `styles/illustrated/STYLE.md`, `skills/edit-style-illustrated`, `python -m ytflow art-brief <프로젝트>`, `ytflow/stages/illust.py` |
| **레퍼런스 2편 분석 (2026-11-13)** — 뉴스 데스크 카드(한 소식 = 한 장, `newsdesk` 장면) · 훅 쇼츠(얼굴 없이: 실제 화면 꽉 채움·훅 제목·큰 자막·튀어나오는 카드) · 말하는 사람 쇼츠(본인 촬영 있을 때만), 기존 스타일과 차이·장단점, AI 채널 적용 | `docs/25-reference-2611.md`, `styles/news-desk/`, `styles/recipes/hook-shorts.yaml`, `python -m ytflow hookshort <프로젝트>`, `python -m ytflow presenter <프로젝트>` |
| **이야기 그림판 — 호기심 채널 이야기형 (v21)** — 말하는 순간 종이 위에 사람·사물이 선으로 그려지고 카메라가 따라감, 정보형(주식)과 다른 양식, 썸네일 `board` | `manual/04-curiosity.md` §0-4, `styles/story-board/STYLE.md`, `skills/edit-style-story-board`, `ytflow/stages/story.py`, `scripts/curiosity_story/make.py` |
| **인트로 없음·대본 형식/진행/말투 (v24, 모든 채널)** — 인사·채널 소개·순서 예고 없이 첫 문장부터 본론, 미주일기 문법(여는 장면 → 질문 → 한 줄기 이야기를 시간 순서로 → 수미상관 → 의미), 말투는 호기심 = 3인칭 다큐 내레이터 '~습니다', 시장·시사·AI = 분석형 어미 혼합(`manual/11-workflow.md` §3-2) | `manual/README.md` §2-1·§2-3, `docs/30-script-voice.md` |
| **시청자 먼저 — 호기심 채널 (v23)** — 상권 조사처럼 주 시청자·유입 경로·유입 이유를 먼저(`01_research/audience.md`), 대본에서 인물의 행동 또는 실험이 남긴 질문을 따라갈 이유를 찾아 `intent.md`에 기록, **편집 전에 대본만 사용자 검토** | `docs/29-curiosity-audience.md`, `manual/04-curiosity.md` §0-6, `scripts/curiosity_research.py` |
| **의도 먼저 — 애니메이션 무대 (v22)** — 만들기 전에 제작 목표·시청자 욕망·기억할 한 장면(`02_script/intent.md`), 장면 goal·박자 why 필수, 한 화면 한 생각·글자 하나·대본의 동사를 그림이 연기 (`stage` 장면) | `manual/04-curiosity.md` §0-5, `styles/anim-stage/STYLE.md`, `ytflow/stages/stage.py` |
| **대본 → 그림·애니메이션 (호기심)** — AI 그림 조각(cut·pose·move) vs 관절 인형(puppet), 그림 생성 여러 길(OpenAI GPT Image·Gemini·Codex 구독·수동 — ElevenLabs 로는 그리지 않음, 2026-11-20 사용자) | `docs/27-story-animation.md`, `docs/28-save-and-imagegen.md` §2, `python -m ytflow art-gen <프로젝트> --backend ...`, `python -m ytflow art-cut`, `ytflow/stages/imagegen.py`, `ytflow/stages/puppet.py` |
| **움직이는 비유 애니메이션 (따로 쓰는 스타일, 매뉴얼 기준 아님·품질 보완 필요)** — 무리가 한쪽으로 옮겨 가고 의태어가 튀어나오는 비유 장면 (`metaphor` 장면, migrate·pop). 사용자가 고를 때만 | `styles/motion-metaphor/STYLE.md`, `docs/22-motion-reference.md`(레퍼런스 재분석·v2 방향), `styles/recipes/motion-metaphor.yaml`, `ytflow/stages/motion.py` |
| **매뉴얼 그래프·의도 정렬·고치기 도구** — 피드백 → 매뉴얼 규칙 → 코드·검사를 그래프로(`manual/graph.json`), 용어 사전(`manual/glossary.yaml`), 의도 정렬(`manual/intents.yaml`), 브라우저에서 매뉴얼 편집·검토 기록 | `docs/31-manual-graph.md`, `python -m ytflow manual-graph`, `python -m ytflow manual-ui`, `ytflow/stages/manualgraph.py` |
| **레포 구조: 메인 → 주제 레포 → 상황 → 영상 (2026-11-15)** — 매뉴얼이 메인 레포, `topics/<brand>/topic.yaml`(주식·호기심·AI·시사)이 메인을 물려받아 기본값·상황을 바꾸고 더함. 영상마다 `edit-plan` 으로 박자별 상황 → 장면 종류·연출 기법을 채우고 `02_script/EDIT_CONTEXT.md` 를 **편집 전에 먼저 읽음** | `docs/33-repo-layers.md`, `topics/README.md`, `manual/situations.yaml`, `python -m ytflow topics`, `python -m ytflow edit-plan <프로젝트>`, `ytflow/stages/layers.py` |
| **연출 기법 카탈로그** (깃허브 등 열린 구현 조사: 글자 쪼개기·스크램블·모프·매치 무브·J/L컷·사진 깊이·순위 막대·맞대기 …, 이미 있음/후보/보류·라이선스·내 피드백과 부딪히는 점) — GSAP 3.13 플러그인 전부 무료 | `docs/32-technique-research.md`, `styles/techniques.yaml`, 매뉴얼 그래프 '용어 사전 → 연출 기법' |
| **내 피드백 → 매뉴얼 수용 점검 (2026-11-18)** — 피드백마다 층·반영 위치·과적합 여부, 남은 질문 | `docs/48-feedback-ledger.md`, `manual/feedback.yaml`, `manual/rule_tiers.yaml` |
| **매뉴얼 정기 검토 (매일 밤 자동, 2026-11-15)** — 충돌·과적합·폐지된 기준 잔재·깨진 참조·층 미정 피드백을 재고, 판단이 필요 없는 것만 고쳐 커밋, 판단이 필요한 것은 질문으로 (그래프 '한눈에 → 정기 검토' + 휴대폰 알림). 매뉴얼 버전은 올리지 않음 | `docs/34-manual-review.md`, `skills/manual-review/SKILL.md`, `python -m ytflow manual-audit`, `manual/audit.md` |
| **레퍼런스 영상 움직임 분석 — PC 의 ego lite + rea-video** — 클라우드는 YouTube 에 막히므로 사용자 PC 의 에이전트가 ego lite 로 재생 화면을 '정지 → 이동 → 찍기' 캡처(내려받기 없음) → rea-video 장면 분석 → 요소가 대본의 동사를 연기하는 움직임 문법 정리 | `skills/ref-watch-ego/SKILL.md`, `scripts/frames_to_clip.py`, `docs/31-motion-grammar.md`(결과) |
| **매뉴얼 관리 — 한 번에 한 명만, 고칠 때만 잠금 (2026-11-16)** — 정해진 담당 없음: 고칠 세션이 짧게(2시간) 잠금(`locks` 브랜치) → 잡자마자 main 합침 → 고치고 main 에 합침 → 풂. 잠겨 있으면 `manual-lock request`. 막는 장치 세 겹(명령·Claude hook·git pre-commit) | `docs/35-manual-ownership.md`, `manual/OWNERS.yaml`, `python -m ytflow manual-lock status` |
| **원본 발언 영상 — 필요할 때만 PC 에서 받기 (2026-11-20)** — 피클이 위치(주소·구간) → 클라우드 `clip-order` 주문서 + `inbox/pc-tasks/` → PC `clip-fetch`(본인 브라우저 로그인, 20초 이내 구간만, Drive 보관) → `hybrid`. 클라우드 로그인은 하지 않음 | `docs/50-clip-lane.md`, `python -m ytflow clip-order|clip-fetch|clip-pull <프로젝트>`, `ytflow/stages/cliplane.py` |
| **지금의 고리 — 최신 시사·핫 키워드로 주제 고르기·제목·썸네일 (2026-11-20, 모든 채널 공통 규칙)** — 후보를 고르기 전에 이번 주 키워드(뉴스·검색 급증·아웃라이어·뉴스레터·계절 행사)를 모으고, 후보마다 '지금의 고리'(키워드·날짜·출처·이어지는 방식)를 적음. 시사는 입구, 본론은 채널 기준대로. 억지 고리·사고 재난 입구 금지 | `manual/01-desire-map.md` §3-1, `manual/04-curiosity.md` §2 |
| **외부 스킬 — 언제 꺼내 쓰나 (2026-11-23)** — 최근 30일 반응(last30days), 사실 확인(fact-check-workflow·source-verification·social-media-intelligence·data-journalism), ElevenLabs(text-to-speech·speech-to-text·voice-isolator·music·sound-effects), 올린 뒤 성과 분석(claude-youtube analyze). 매뉴얼 > 우리 스킬 > 외부 스킬, 커뮤니티 결과는 단서 | `manual/11-workflow.md` §2-5, `docs/62-external-skills-map.md`, `docs/61-last30days.md`, `tools/external.json`, `python scripts/install_tools.py` |
| **채널 운영·분석 (2026-11-23, 에이전트가 맡음)** — 매일 22:10 올린 영상 수치(조회·시청 지속·유입 경로·노출 클릭률·댓글) → 앞섬·처짐 해석 → 실험 장부 → `ops/next.md` 로 다음 편에 하나. 운영 권한: 공개는 지금대로, 제목·썸네일 교체·재생목록·사본 정리는 에이전트, 댓글 답글은 초안만 | `manual/11-workflow.md` §8·S10, `docs/63-channel-ops.md`, `python -m ytflow ops`, `python -m ytflow ops-act`, `config/channel_ops.yaml`, `data/analytics/` |
| **연출 결정 기록 (2026-11-24)** — 여러 연출·스타일 가운데 '이것'을 고른 근거·버린 대안·의도를 렌더 전에 기록(영상 `direction` + 장면 `decide`), 같은 상황 같은 선택, 11-25 이후 MUST. 방송·대형 팀 사례 조사, 다큐 개념 장면 `docu`(칩·관계선·판 기울기·신호 퍼짐·관계도→순위, 개념 설명 장면만 카메라 허용) | `manual/05-style-matching.md` §0-9, `docs/66-broadcast-direction-decisions.md`, `docs/65-attention-explainer-benchmark.md`, `python -m ytflow decide <프로젝트> [--draft]`, `ytflow/stages/decisions.py`, `ytflow/stages/docu.py` |
| **설명 다큐 문법 — 문장마다 무엇을 보여 주나 (2026-11-25)** — TED-Ed·WSJ·Kurzgesagt·PolyMatter·달리오·EBS·FT 9편의 문장 → 화면 대응과 정지 측정(레퍼런스 정지 0~28%, 우리 71~96%), 공통 문법 E1~E8(그림 = 문장의 명사·동사, 주인공 사물 하나, 구절마다 변화, 숫자는 제 모양 그래프), 장면 점검 4가지 | `docs/68-explainer-docu-benchmark.md`, `python scripts/hold_measure.py <영상>` |
| **미스터리 역사 사건 파일 템플릿 (`mystery-archive`, 2026-11-28)** — 실제 자료 사진·장소 영상이 주인공, 구절마다 컷(정지 3초 넘으면 분위기 영상 끼움), 사건 파일·단서 다섯 칸·증거판·지도·가계도·판정표, 배경음악 목소리보다 약 18dB 아래·효과음 없음. 터진 역사 영상 10편 실측 근거, 예시 사진 MA-01~13 | `styles/mystery-archive/STYLE.md`, `styles/recipes/mystery-archive.yaml`, `styles/mystery-archive/engine/` |
| **반드시 지킬 것·검사** | `manual/06-checklist.md`, `python -m ytflow check <프로젝트>` |
| **제작 업무 체계 (v38)** — 단계 S0~S9 · 사용자 결정 지점 D1~D4(**최종 승인은 사용자만**) · 한 편씩 진행 · 뉴스레터로 주제 탐색 · AI 롱폼 네 형식 · 분석형 내레이션 | `manual/11-workflow.md` |
| **자료 고르기·화풍 목록 (v61, 2026-11-20, 모든 채널)** — 박자가 하는 일로: 스쳐 지나가며 떠올리게 → 인물 실사 소스영상, 쉽게 설명·상황 설명 → 화풍별 모션그래픽(천천히 나타나고 움직임), 증거 → 실제 자료, 둘 다 어려우면 삽화. 모션그래픽·삽화·실사 색보정 화풍은 목록에서 영상마다 고름 | `manual/12-visual-storytelling.md` §0-1, `styles/looks.yaml`, `python -m ytflow looks`, `python -m ytflow look <프로젝트> --motion --illust --footage` · **영상 = 구성요소 카테고리(화면 화풍·삽화 화풍·실사 색보정·글자 연출·그래픽 연출·카메라·장면 전환·배경음)마다 고른 스타일의 조합** `styles/components.yaml`, `look <프로젝트> --set 카테고리=스타일` · "화풍목록 보여줘" → `skills/looks-gallery` (공유 페이지 https://claude.ai/artifact/K4CRgsyTYsWGCDw5RoCtam) |
| **설명 무대 — 상황 설명 모션그래픽 (2026-11-20)** — 쉽게 설명·상황 설명 박자: 사건 이후 누적(`afterline`)·두 값 사이 간격(`spread`)·전체 중 몫(`share`)·인물·물체 자유 무대(`motionboard`), 바탕 구겨진 종이·어두운 무대(`theme`), 주식 채널 상황 설명 기본 | `styles/explain-stage/STYLE.md`, `docs/51-explain-stage.md`, `docs/52-motion-quality-references.md`, `skills/edit-style-explain-stage`, `ytflow/stages/explain.py` |
| **화면의 네 자리 (v73, 2026-11-20, 모든 채널)** — 이야기는 삽화, 설명은 모션그래픽(이야기 중이면 삽화 위에), 증거는 실제 자료(인물 사진·원본 발언·문서), 마디는 검은 화면 한 줄. 채널마다 어느 자리가 많은지만 다름(시장은 이야기가 거의 없음). 스톡 실사 B-roll 은 기본에서 뺌 | `manual/12-visual-storytelling.md` §0-1, `manual/04-curiosity.md` §0-7, 근거 `docs/54-my-videos-vs-viral.md` §5 |
| **화풍·연출을 상황에 맞춰 (2026-11-18)** — 모션그래픽이 최우선(2026-11-20 사용자), 그림은 원화·코드는 움직임, 화풍은 편 단위·연출은 장면마다, 화풍 승인과 영상 판정 분리, 귀여운 캐주얼·플랫 벡터·2.5D 등 화풍 표 | `manual/05-style-matching.md` §0-8, `docs/45-style-and-direction-map.md`, `docs/44-painted-layer-animation.md`, `docs/42-script-to-motion.md`, `docs/47-curiosity-channel-benchmark.md` |
| **연출의 원리 (v38)** — 숫자 상한·하한 대신 목적·상황·넘치면/모자라면, `check` 의 참고(ℹ️)는 측정값일 뿐 | `manual/05-style-matching.md` §0-0, README §5 |
| 채널 회차 만들기 (반복 운영) | `skills/channel-run/SKILL.md`, `channels/README.md`, `docs/06-operations.md` |
| 영상 1편 만들기 | `skills/video-make/SKILL.md` |
| 형식: 롱폼 칼럼·보고서 / 쇼츠 안내 | `formats/README.md` |
| 자료조사 / 대본 / 소스 / 편집만 | `skills/video-research`, `video-script`, `video-sources`, `video-edit` |
| **호기심 채널 — 심리학·현대인의 일상** (잼 편의 행동 중심, 기억 편의 실험 중심) | `manual/04-curiosity.md` §0-6·§0-7, `channels/ch-knowledge/`, `prompts/script_knowledge.md` |
| 하이브리드 (식스시그마 영상 + 머니크루 논리 + 미주일기 손그림) | `styles/hybrid/STYLE.md`, `prompts/script_hybrid.md`, `skills/edit-style-hybrid` |
| 편집 스타일 고르기·적용 | `styles/README.md`(계열 구분), `styles/<id>/STYLE.md`, `skills/edit-style-<id>` |
| 새 편집 스타일 추가 (레퍼런스 영상 분석) | `skills/edit-style-new/SKILL.md` |
| 전체 설계·에이전트별 차이 | `docs/04-agents.md`, `docs/02-workflow-sop.md` |
| 영상편집 skill 도입 검토 | `docs/05-skills-review.md` |
| **소스 찾기 (벤치마킹 채널 방식, 소스 먼저)** | `docs/07-sourcing.md`, `channels/<id>/channel.yaml` 의 `sourcing` |
| 목소리(ElevenLabs, 영상 확정 후 적용) | `docs/08-voice.md` |
| **어디에 무엇을 두나** (GitHub / Google Drive / 다시 만들기) | `docs/09-storage.md` |
| **제작 플레이북: 다음에도 똑같이 만들기** (명령 순서·자동 점검·보관) | `docs/11-playbook.md` |
| **연출과 그래픽 분리** (편집점·편집 포인트는 대본, 색·글꼴·배경은 갈아 끼우는 스킨) | `docs/13-direction-vs-graphics.md`, `skins/` |
| 그래픽 팩에 쓸 스킬·도구 (라이선스 확인·도입 순서) | `docs/14-graphic-pack-tools.md` |
| **연출 조사** (시청 유지 원칙·벤치마크 대비 측정·개선안·연출 도구) | `docs/15-direction-research.md` |
| **새 연출·그래픽 시험작** (아카이브 다큐·지도 여정·키네틱 타이포, 새 팩 newsprint·blueprint·kinetic-poster) | `docs/16-new-styles.md`, `ytflow/stages/directions.py`, `styles/demos/` |
| 키 없이 Google Drive 로 자동 복사 (Apps Script, 한 번 설치) | `docs/12-drive-sync.md`, `tools/drive-sync/` |

스킬은 `skills/` 가 원본입니다. `.claude/skills/`(Claude Code)와 `.agents/skills/`(Codex)는 `python scripts/sync_skills.py` 로 만든 복사본입니다. **원본만 고치고 동기화하세요.**

## 환경
```bash
pip install -r requirements.txt      # Python 3.10+, 그리고 ffmpeg·node(Playwright 캡처용)가 필요 (faster-whisper 포함)
python scripts/install_tools.py      # 외부 편집 도구·skill 고정 버전: HyperFrames·GSAP·rough.js, ffmpeg-skill, hand-drawn-diagrams
python -m ytflow --help
```

### LLM 백엔드 (`config/pipeline.yaml` → `llm.backend`, 또는 환경변수 `YTFLOW_LLM_BACKEND`)
| 값 | 언제 | 비용 |
|---|---|---|
| `claude-cli` | Claude Code 를 쓰는 사람 (`claude` 로그인) | Claude 구독 |
| `codex-cli` | Codex 를 쓰는 사람 (`codex login`) | ChatGPT 구독 |
| `api` | 서버·자동 실행 (`ANTHROPIC_API_KEY`) | 사용량 과금 |
| `manual` | **에이전트가 대화 안에서 직접 판단**. 요청이 `.llm/requests/` 에 쌓이면 답을 `.llm/responses/` 에 쓰고 다시 실행 | 에이전트 세션 안 |

## 주요 명령
```bash
python -m ytflow make --channel <채널id> [--topic "주제" | --from-text 조사글.md]   # 채널 규칙으로 한 편
python -m ytflow make --style-ref <스타일id> [--topic "주제"]   # 스타일만 지정해 한 편
python -m ytflow make --channel <채널id> --plan                  # 트렌드 → 소스 찾기 → 주제·형식 결정까지만 (검토용)
python -m ytflow channels                                       # 채널 목록
python -m ytflow daily [--brand market|issues] --project <YYYYMMDD>-market-daily   # 매일 브리핑 주제 찾기: 전날 시장(지수·업종·큰 움직임·이슈/보고서/전망·실적) / 전날 시사 이슈
python -m ytflow cut <프로젝트>                                   # 원본 발언 컷편집: bite 장면 문장을 긴 원본에서 찾아 02_script/cuts.json
python -m ytflow art-brief <프로젝트>                             # 손그림 삽화 주문서 → 02_script/art_brief.md
python -m ytflow hookshort <프로젝트>                             # 훅 쇼츠 (얼굴 없이): AI 목소리 + 실제 화면 꽉 채움·훅 제목·큰 자막·카드 (02_script/hookshort.json)
python -m ytflow presenter <프로젝트>                             # 말하는 사람 쇼츠: 본인 촬영 → 점프 컷·펀치 인·훅·큰 자막·카드 (02_script/presenter.json)
python -m ytflow yt-publish <프로젝트> [--dry-run] [--at 시각]     # 유튜브 올리기·관리 (공식 API, Actions 가 업로드·설명란·예약·썸네일·자막·재생목록)
python -m ytflow yt-pack <프로젝트>                               # 유튜브 업로드 묶음: 설명란(챕터 타임코드·출처·면책)·제목 후보·태그 → 05_edit/youtube.md
python -m ytflow earnings-call <프로젝트> <녹취록 PDF·주소> --ticker CRWV --period 3Q26   # 어닝콜 정리: 핵심 발언·애널리스트 질문표·질문 주제 (manual/03 §0-1)
python -m ytflow demand [--channel ch-knowledge]                 # 분야별 수요 분석 (검색 → 채널 → 아웃라이어 배수)
python -m ytflow archive search "influenza 1918" [--films]       # 공공 기록 사진·영상 (미국 의회도서관, 퍼블릭 도메인)
python -m ytflow hybrid <프로젝트>                                # 하이브리드 영상 (02_script/hybrid.json → final.mp4, 끝에 sync-qa 자동)
python -m ytflow skin-preview <프로젝트> [--skins a,b,c]          # 같은 연출을 그래픽 스킨별로 렌더해 비교 (YTFLOW_SKIN=<id> 로 한 번만 바꾸기)
python -m ytflow thumbnail <프로젝트>                             # 제목·썸네일 A/B/C (hybrid.json 의 package, 규칙 prompts/thumbnail.md)
python -m ytflow short <프로젝트>                                  # 세로 쇼츠 Claude 판 (02_script/short.json, 실제 화면 중심)
python -m ytflow recipes | style-pick <프로젝트>                    # 편집 스타일 등록부 / 이 영상에 맞는 스타일 추천
python -m ytflow edit-plan <프로젝트>                            # 메인 → 주제 레포 → 이 영상: 박자마다 상황 → 장면·기법 → 02_script/EDIT_CONTEXT.md (편집 전에 먼저)
python -m ytflow check <프로젝트> [--upto G4]                     # 체크리스트 자동 검사 (MUST 실패 시 종료 코드 1)
python -m ytflow review <프로젝트> --pass | --reject "이유"        # 사용자 검토 기록 → 기각은 매뉴얼 '반영 대기'로
python -m ytflow manual-bump "바꾼 기준 요약"                      # 기각 사유 반영 후 매뉴얼 버전 올리기
python -m ytflow manual-audit [--fixed "고친 것"]                   # 매뉴얼 정기 검토: 충돌·과적합·폐지된 기준 잔재·깨진 참조 → manual/audit.md (매일 밤 자동, docs/34)
python -m ytflow manual-graph | manual-ui [--port 8770]           # 매뉴얼 지식 그래프(manual/graph.json) / 그래프 보기·매뉴얼 고치기 도구
python -m ytflow sync-qa <프로젝트>                               # 완성본 자막·목소리·화면 싱크를 받아쓰기로 측정 → 05_edit/sync_qa.json
python -m ytflow voice-import <프로젝트> part1.mp3 [...]          # ElevenLabs 긴 음성을 대본 박자별로 자르기 (키 없이)
python -m ytflow upload <프로젝트> [--archive]                    # 완성 영상 → Google Drive (기본), --to github 는 공개해도 되는 것만 GitHub Release (docs/09-storage.md)
python -m ytflow stage <프로젝트> <단계>                          # 단계 하나
python -m ytflow rebuild <프로젝트>                               # 소스 넣은 뒤 재생성
python -m ytflow validate <프로젝트>                              # 대본 점검 (직접 쓴 뒤 필수)
python -m ytflow style <id> ref.mp4 --title <이름>               # 새 편집 스타일 분석
python -m ytflow styles | schemas | status <프로젝트>
```

## 트렌드 소스
| 소스 | 방식 | 필요한 것 |
|---|---|---|
| Google News (국문·영문) | 공개 RSS | 없음 |
| Hacker News | 공개 Algolia API | 없음 |
| YouTube 이번 주 아웃라이어 | 검색 결과 페이지 | 없음 |
| X 최근 게시물·공식 계정 | X API v2 최근 검색 | `X_BEARER_TOKEN` (선택, 유료 요금제) |
| X 게시물 캡처 | 공식 임베드(oEmbed) | 없음 (게시물 URL 만) |
| Reddit | 공개 JSON | 클라우드 IP 는 403 으로 막힘 → 쓰지 않음 |

## 편집 스타일 계열
| 계열 | 뼈대 | 스타일 | 대본 화면 문법 |
|---|---|---|---|
| `source` 원본 소스형 | CEO·CFO 인터뷰·실적발표 원본 영상 + 자막 + 핵심요약 애니메이션 | sixsigma, **hybrid**(원본 영상 + 인과 지도 + 손그림, `python -m ytflow hybrid <프로젝트>`) | `prompts/script_source.md`, hybrid 는 `prompts/script_hybrid.md` |
| `infographic` 자체 제작 인포그래픽형 | 직접 그린 도식·차트·비유 그림 | **mijudiary(기본)**, moneycrew | `prompts/script_infographic.md` |
| `shorts` 쇼츠 | 9:16 고정 훅 + 큰 자막 | shorts-aitips | `prompts/shorts_script.md` |

## 규칙 (모든 에이전트 공통)
- **main 에 직접 커밋·푸시 허용 — 모든 세션 (2026-11-21 사용자: "이 세션애서 main에 직접 커밋하고 푸쉬하는 것을 허용합니다" · "이 세션만이 아니라 모든 세션에서 이를 허용합니다"):** 작업 브랜치를 따로 만들지 않고 main 에서 커밋하고 `git push origin main` 해도 됩니다. 매뉴얼·규칙 파일은 그대로 잠금 절차(아래 '매뉴얼은 한 번에 한 명만')를 따르고, 미디어 커밋 금지·사실 규칙도 그대로입니다. 푸시 전에 `git fetch` 로 main 이 앞서 있지 않은지 확인합니다.
- **PC(로컬)에서 시작하면 `inbox/pc-tasks/` 의 `status: pending` 부터 (2026-11-20 사용자):** 클라우드가 못 하는 일(원본 구간 받기·예시 그림 그리기)이 여기 쌓입니다. 파일의 명령을 실행하고 done 으로 바꿔 main 에 푸시. Claude Code 는 시작할 때 알림이 뜹니다(`scripts/pc_tasks.py`).
- **매뉴얼은 한 번에 한 명만 — 고칠 때만 잠그고 순서대로 (2026-11-15·16 사용자 요청, docs/35):** 매뉴얼·규칙 파일(`manual/OWNERS.yaml` 의 protected — manual/, topics/, styles/recipes·techniques, skills/, AGENTS.md, 검사 코드)은 **잠금을 가진 한 명만** 고칩니다. 절차: `manual-lock acquire` → 고치기 → main 에 합치기 → `manual-lock release` (잠겨 있으면 `manual-lock request`, 자세한 것은 docs/35). **잠금은 '한 번에 한 명'만 지키는 장치이지 기본으로 잠가 두는 것이 아닙니다(2026-11-18 사용자: "깃이 비었는데도 아무도 사용 안하는데 락을 걸어서 깃을 사용하지 않는 상황이 이루어지지 않도록").** 비어 있으면 `review`·`feedback`·보호 파일 편집·커밋이 그 자리에서 자동으로 잡고(짧게, 저절로 풀림) 바로 씁니다. 다른 사람이 쓰는 중일 때만 요청·제안함으로 갑니다. 처음 클론하면 `git config core.hooksPath .githooks`. 영상 프로젝트·렌더러·자료는 각자 브랜치에서 자유롭게.
- **트렌드·핫이슈와 이어진 주제 선정·제목·썸네일 (모든 채널 공통, 2026-11-20 사용자: "모든 공통규칙으로 트렌드 핫이슈 유행과 연관있는 주제선정 썸네일 생성으로 넣어주세요"):** 후보를 고르기 전에 이번 주 키워드(뉴스 상위·검색 급증·유튜브 아웃라이어·뉴스레터·계절 행사)를 모으고, 후보마다 '지금의 고리'(`topic_brief.json` 의 `why_now`: 키워드·날짜·출처)를 적어 고리가 있는 후보를 먼저 고릅니다. 그 키워드를 제목 앞 20자와 썸네일 큰 글씨에 넣습니다. 시사는 입구, 본론은 채널 기준대로. 영상에 없는 유행어로 낚거나 사고·재난 피해를 입구로 쓰지 않습니다 — `manual/01-desire-map.md` §3-1, `prompts/thumbnail.md` '지금의 고리', 시장은 `manual/09-market-daily.md` §7-1.
- **모든 시각효과는 목록 + 움직이는 예시 + 제작 명세 (2026-11-20 사용자: "말로만 하면 내가 나중에 이게 뭐였지? 하고 까먹으니까 이는 공통규칙이야" · "예시사진으로는 전부 보여주지 못하고 괴리가 생기니까"):** 화풍·장면 종류·연출·전환·겹치기·바탕·글자·소리는 id 로 고를 수 있게 분류하고, 정지 사진이 아니라 움직이는 예시와 다시 만들 수 있는 제작 명세(박자표·대본 키·코드 위치)를 함께 둡니다. 새로 만들면 같은 틀로 더함 — `manual/12-visual-storytelling.md` §0-1, `styles/hybrid/scenes/`(+`real-examples.md`), `styles/looks/README.md`, `styles/components.md`, 페이지: 화풍 목록 https://claude.ai/artifact/K4CRgsyTYsWGCDw5RoCtam · 연출 예시 목록 https://claude.ai/artifact/SPHyXdpGmcdPwMQu7cpMdP
- **피드백 → 그래프 (2026-11-15 사용자 요청):** 사용자가 피드백하면 원문 그대로 기록하고 매뉴얼 그래프와 공유 페이지를 갱신합니다.
  1) 영상 판정은 `python -m ytflow review <프로젝트> --pass | --reject "원문"`, 그 밖의 말(방향 요청·"그런 뜻이 아니었다"·도구 요청)은 `python -m ytflow feedback "원문" --kind direction|clarify|tool [--about intent:xxxx] [--pending]` — 둘 다 `manual/graph.json` 을 자동으로 다시 만듭니다.
  2) 모델 해석이 틀렸다는 말이면 `manual/intents.yaml` 에 뜻한 것·뜻하지 않은 것·판정도 적습니다(`manual-ui` '의도 정렬').
  3) `python -m ytflow manual-graph --artifact <스크래치>/manual-graph.html` → Artifact 도구로 **같은 공유 페이지**(`ytflow/stages/manualgraph.py` 의 `ARTIFACT_URL`)에 다시 올리고 → 커밋·push. 매뉴얼을 고쳤는데 그래프가 옛것이면 `check` G0 SHOULD 가 알려 줍니다.
- **규칙의 네 층 (2026-11-15 사용자 요청, manual/README §3-1):** 영구 원칙(사실·법·권리·안전 — 진짜 금지) · 작업 기준(제작 방법) · 스타일 기본값(소리·카메라·바탕·비율 — 금지라고 쓰지 않고 켬/끔 기본값과 범위로) · 실험 기록(한 영상의 반응 — 매뉴얼 금지·MUST 로 옮기지 않음). 피드백을 매뉴얼로 옮기기 전에 `feedback --scope` 로 층부터 정하고, 애매하면 실험 기록으로 둡니다. 스타일 층을 MUST 검사로 만들지 않습니다. 분류: `manual/rule_tiers.yaml`, 확인: 매뉴얼 그래프 '한눈에 → 과적합 후보'.
- **쉬운 대본:** 시청자는 일반인입니다. 핵심 한 문장(`core_message`), 논리 구조(`logic`), 숫자마다 비교 기준(`compare_to`), 비유 2개 이상, 과거 사례 1개 이상, 어려운 말 풀이(`glossary`)를 넣습니다. `prompts/script.md`, `validate` 가 점검합니다.
- **사실:** 숫자와 발언은 출처로 확인된 것만 씁니다. '재확인 필요'는 단정하지 않습니다. 투자 권유 표현은 금지합니다.
- **소스:** YouTube 봇 확인이나 사이트 접근 차단을 **우회하지 않습니다.** 막히면 임시 화면을 두고 사용자 PC 에서 `rebuild` 하게 안내합니다. **작업에서 막히는 일(유튜브 재생·자막·봇 확인·로그인이 필요한 페이지)은 피클에게 요청합니다** — `inbox/requests/<KST 시각>-<slug>.md` 한 파일 = 한 요청을 main 에 올리고, 결과는 `inbox/requests/done/` 에서 이어 받습니다 (2026-11-19 사용자: "작업에서 막히는 일은 피클에게 요청하시면 됩니다", `inbox/requests/README.md`).
- **스타일:** 레퍼런스 채널의 대사, 고유 캐릭터, 로고, 썸네일을 복제하지 않습니다. 구조와 기법만 가져옵니다.
- **커밋 대상:** 기획 문서(md/json/csv/yaml)는 커밋합니다. 미디어(mp4/wav/png/jpg), 타 채널 자막, `styles/**/work/`, `.llm/` 은 커밋하지 않습니다(.gitignore). 완성 영상과 다시 만들 수 없는 자료 화면은 **Google Drive**(기본) 또는 공개해도 되는 것만 **GitHub Release** 에 보관합니다(`upload <프로젝트> --archive`, 키 불필요, `docs/09-storage.md`·`docs/11-playbook.md`).
- **제목·썸네일:** 모든 영상은 제목(후보 3개)과 썸네일 3장(A/B/C)을 함께 만듭니다(`prompts/thumbnail.md`). 사진 장소·숫자는 영상과 같은 사실 규칙.
- **결과 확인:** `layout_qa.json` 이 비어 있는지(화살표·글자 겹침, 대비) 보고, 영상을 만든 뒤에는 프레임을 뽑아 직접 확인하고(`skills/video-edit`), `REPORT.md` 의 남은 일을 사용자에게 알립니다.
- **목소리:** 초안은 edge-tts, **업로드 최종본은 ElevenLabs**(영상 확정 후 채널별 voice_id 지정). API 키는 채팅에 쓰지 않고 환경변수·네트워크 비밀값으로.
- **모델 — 판단의 중요도에 따라 세 층, 세션은 Opus (2026-11-27 사용자: "판단이 필요한 부분이 아니라 단순 작업은 소넷이 판단이 필요하면 작업은 opus 종합적인 검수가 필요한 부분은 페이블이 계층적으로 판단의 중요성에 따라서 이를 나누어줘" · 2026-11-22: "그냥 opus로 세션진행하고 fable은 중요할때만 호출하게 해보세요 … 토큰이 녹았거든요"):** ① **단순 작업(판단 없음) = Sonnet 5.5 `worker`** — 자료 수집·옮겨 적기·렌더·프레임 캡처·자막 생성·음성 자르기·파일 정리·Drive 올리기. 메인이 직접 하지 않고 넘깁니다(2026-11-27: "기계적인 단계는 소넷으로 … 설정해줘"). ② **판단이 필요한 작업 = Opus 5.5** — 메인 세션(주제·대본 쓰기·제목·연출 결정·D1~D4 정리)과 `senior`(새 맥락에서 근거 검수표·대조표·장면표·분석). ③ **종합적인 검수 = Fable 5.2 `fable`** — 대본 D2 직전·완성 영상 D4 직전에 전체를 한 번 보는 검수, 엇갈린 근거 최종 판정, 사용자가 요청할 때. 필요한 파일만 넘겨 짧게 묻습니다. 애매하면 한 층 위로. 모델 이름은 `config/models.yaml`, 자세히는 `manual/11-workflow.md` §1-1. 긴 작업·예약 작업은 새 세션에서.
- **ElevenLabs 는 API 로만, MCP 로 생성하지 않음 (2026-11-22 사용자: "일레븐랩스 사용시 반드시 api로 mcp로 사용하지 마세요 보니까 크레딧소모가 더 큰 것 같더라구요 진위 확인하고 맞다면 이렇게 해주세요."):** 같은 문장(33자, Teo·eleven_v4)을 실측: **직접 API 15 크레딧**(응답 헤더 `Character-Cost`) vs **MCP `creative_generate_speech` 1테이크 33 크레딧·기본 2테이크 66 크레딧**(estimate_only) — MCP 가 1테이크도 2.2배, 기본값이면 4.4배. 목소리는 `ytflow` 의 직접 API(`media.py` `_elevenlabs`, `voice-sample`, `hybrid`)로만 만들고, ElevenLabs MCP 의 생성 도구(speech·image·video 등 크레딧을 쓰는 것)는 쓰지 않습니다. 계정 사용량 확인처럼 크레딧을 쓰지 않는 조회만 예외 (`docs/08-voice.md`).
- **외부 도구:** 버전은 `tools/external.json` 에 고정합니다. 올릴 때는 그 도구의 SKILL.md·스크립트를 다시 읽고(네트워크 호출·자동 설치 확인) `docs/05-skills-review.md` 에 기록합니다.
- **저장 위치 — Git 과 Drive 를 나눠서 (2026-11-16 사용자: "깃에 보관하되 깃에 보관하기 힘든 부분은 드라이브쪽을 활용하라는거야 로컬드라이브 부담을 줄이는게 목적이고"):** 코드·문서·설정·기획·작은 분석 결과(md/json/csv/yaml)는 **Git** 에 둡니다. 큰 영상·오디오·프레임 묶음·원자료처럼 Git 이력에 부담이 되는 **파일은 Google Drive** 에 두고, Git 에는 위치·판본·크기 같은 최소 메타데이터만 남깁니다(접근 토큰이 든 링크·비공개 자료는 공개 Git 금지). 모든 파일을 두 곳에 두라는 뜻은 아니며, 목적은 **PC 저장공간 부담 줄이기**입니다. 올리고 다시 열어 확인하기 전에는 PC 원본을 지우지 않습니다. PC 는 Google Drive for desktop 의 `ytflow` 폴더를 환경변수 `YTFLOW_DRIVE`(예: `G:\내 드라이브\ytflow`)로 지정해 그 아래에 저장하고(`refs\`·`cache\`·`영상\`), 클라우드 세션은 Drive 커넥터(파일당 10MB 까지)·rclone 으로 올립니다. D 드라이브에 새 파일을 만들지 않고, C 드라이브도 쓰지 않습니다. 동기화하면 깨지는 git 저장소·가상환경·설치 도구는 예외(`docs/09-storage.md` §0).
- **올린 영상은 유튜브 링크로 대체, 재료는 그대로 (2026-11-21 사용자: "유튜브에 업로드하면 유튜브 링크를 올리고 드라이브에서 삭제" · "재료는 삭제하는걸 원하지 않아요 단지 영상을 이제 하이퍼링크처럼 대체한다 느낌"):** 유튜브에 올리고 처리(processed)가 끝난 것을 확인하면 Drive 에서 **완성본·중간 렌더 mp4 만** 지우고, 그 자리는 `05_edit/youtube_publish.json`(영상 주소, Git)이 대신합니다. 어떻게 만들었는지를 다시 만들 수 있는 **재료는 지우지 않습니다** — 대본·편집 계획(Git), 목소리 mp3 와 글자별 시각(`*.align.json`), 삽화·사진, 썸네일 A/B/C, 자막(ass). 고칠 때는 완성본이 아니라 재료로 다시 렌더합니다. 유튜브에서 내려받은 사본은 다시 압축된 것이라 확인·참고용입니다(`docs/09-storage.md` §0-4).
- **스키마:** 에이전트가 직접 쓰는 JSON 은 `schemas/*.schema.json` 을 따릅니다(`python -m ytflow schemas` 로 갱신).

## 폴더
| 경로 | 내용 |
|---|---|
| `channels/` | 운영 채널: `channel.yaml`(형식·스타일·키워드·분량), `README.md`, `episodes.md`(회차 기록) |
| `formats/` | 영상 형식: 롱폼(칼럼·보고서) / 쇼츠(짧은 안내) 원고 구조 |
| `tools/external.json` | 외부 편집 도구 고정 버전 (HyperFrames, ffmpeg-skill). 본체는 설치 후 `tools/` 에 (커밋 안 함) |
| `ytflow/` | 파이프라인 코드 |
| `ytflow/stages/` | 단계별 코드. 렌더러는 `cards.py`(sixsigma), `paper.py`(paper), `flat.py`(flat), `hyper.py`(미주일기 카드 HTML + rough.js 손그림), `hybrid.py`(하이브리드: 원본 영상·인과 지도·손그림 장면), 마스터링 `finish.py`, 발언 단어 정렬 `align.py`, 소스 먼저 `scout.py`, 보관 `upload.py`, 공공 기록 자료 `archive.py`, 수요 분석 `demand.py` |
| `prompts/` | 단계별 LLM 지시문 |
| `config/` | 채널·파이프라인 설정 |
| `styles/` | 편집 스타일 라이브러리 (연출 문법 + 그래픽 스킨의 묶음, docs/13) |
| `skins/` | **그래픽 스킨**: 색 토큰·글꼴·배경·선 질감·사진 톤·자막 상자 (`skin.yaml`) |
| `skills/` | 에이전트용 절차서 |
| `schemas/` | JSON Schema |
| `projects/` | 영상별 작업 폴더. 기획 문서만 버전 관리 |
| `data/style_profile.json` | 채널 대본 규칙 (benchmark) |
