# 15. 연출 조사 — 편집점·편집 포인트·리듬·이야기 구조 (2026-11-07)

연출 = 무엇이 **언제**(편집점) **무슨 일**(편집 포인트)로 바뀌고, 그 **리듬**과 **이야기 구조**가 어떤가. 그래픽(docs/13·14)과 무관하게 시청 유지를 좌우한다.

## 1. 측정: 벤치마크 채널 vs 우리 영상 (같은 측정기 `ytflow.stages.style.measure`)
| 영상 | 하드 컷/분 | 화면 변화/분 | 변화 간격(중앙) | 정지 화면 비율 | 비고 |
|---|---|---|---|---|---|
| 미주일기 (11.9분) | 1.35 | **22.7** | 2.0초 | **0.26** | 한 화면 위에 요소를 계속 쌓음 |
| 머니크루 (18.7분) | 0.0 | 12.4 | 4.0초 | 0.63 | 크로스페이드, 누적 빌드 |
| 우리: 스페인 독감 (9.1분) | 2.64 | 16.6 | 2.5초 | **0.55** | |
| 우리: 데이터센터 (6.1분) | 3.92 | 18.9 | 2.0초 | **0.51** | |

대본에서 센 연출 밀도:
| 영상 | 장면/분 | 박자/분 | 편집 포인트/분 | 자료 화면 비중 | **자료 화면 없이 가장 오래 간 구간** | 평균 장면 |
|---|---|---|---|---|---|---|
| 스페인 독감 | 4.5 | 8.6 | 6.8 | 24% | **155초** | 13.3초 |
| 데이터센터 | 5.7 | 10.3 | 10.1 | 14% | **118초** | 10.5초 |

**읽기:**
- 화면 변화 횟수는 두 벤치마크 사이(12~23회/분)로 괜찮다.
- 그러나 **정지 화면 비율이 0.5 이상** → 요소가 다 나온 뒤 화면이 멈춰 있는 시간이 길다(미주일기는 0.26).
- 우리 규칙 "자료 화면 20~30초마다"를 **두 영상 모두 어김**(최장 155초·118초).

## 2. 조사한 연출 원칙 (출처는 맨 아래)
| 원칙 | 내용 | 근거의 성격 |
|---|---|---|
| **첫 1분이 가장 중요** | 이탈이 가장 많은 구간. 처음 30~60초에 강한 시각 '닻'(장면)으로 약속 → 이후 증거로 갚기 | MrBeast 제작 지침 유출본(2차 보도), Johnny Harris 분석 |
| **다시 붙잡기(re-hook)** | 약 3분마다 새 질문·반전으로 다시 끌어당김. 1~3분, 3~6분이 단계 | MrBeast 지침(2차 보도) |
| **패턴 깨기 간격** | 출처마다 10~20초 / 15~30초 / 30~60초 / 90~120초로 제각각 → **정답 숫자는 없음**, 채널 시청 유지 곡선으로 맞출 것 | 크리에이터 블로그(동료 평가 연구 없음) |
| **점점 넓어지는 리듬** | 초반엔 10~20초마다 작은 변화, 뒤로 갈수록 간격을 넓힘. 25세 이상 시청자는 과한 편집이 오히려 유지율을 낮춤 | 업체 가이드 1곳 |
| **보여 주고 말하기(visual first)** | 말로 설명하기 전에 화면 증거를 먼저 계획. 원자료를 '소품'처럼 밑줄 긋고 표시 | Vox·Johnny Harris |
| **닻 → 다리 → 닻** | 강한 장면(닻)과 설명(다리)을 번갈아 | Harris 스타일 커뮤니티 분석 |
| **J컷·L컷 (소리와 화면을 엇갈려 바꾸기)** | 다음 장면 소리가 먼저(J) 또는 앞 장면 소리가 남아서(L) 넘어가면 자연스럽다. 30fps 기준 6~12프레임(0.2~0.4초)부터, 길게는 0.5~2초 | 편집 교육 자료 다수 |
| **누적 빌드** | 같은 구도에 요소를 하나씩 더하고 지우지 않음 → 컷 없이도 변화 | 우리 측정(머니크루·미주일기) |

## 3. 우리 연출에 바로 반영할 것 (제안)
| # | 할 일 | 왜 | 어디에 |
|---|---|---|---|
| 1 | **자료 화면 간격 점검**: 45초 넘게 자료 화면(영상·사진)이 없으면 `validate` 경고. 도식 장면 안에 작은 사진 삽입(화면 속 화면)도 인정 | 두 영상 모두 규칙 위반(118~155초) | `scriptcheck.py`, `prompts/script_hybrid.md` |
| 2 | **멈춘 화면 줄이기**: 요소가 다 나온 뒤에도 천천히 다가가기(카메라 push)·형광펜·숫자 강조 같은 작은 움직임을 4~5초마다 | 정지 비율 0.51~0.55 → 미주일기 0.26 수준으로 | `hybrid.py` 공통 (그래픽 무관) |
| 3 | **J컷**: 장 전환·자료 화면 진입 때 다음 장면 내레이션·효과음을 0.3초 먼저 | 소리와 화면이 동시에 바뀌는 딱딱함 완화 | `timing()`, 조립 단계 |
| 4 | **다시 붙잡기 점검**: 약 3분마다 '질문형 장 표지' 또는 반전 문장이 있는지 `validate` | 첫 1분·3분 단계 원칙 | `scriptcheck.py` |
| 5 | **첫 30초 구조 점검**: 장면(닻) → 통념 → 질문 → 오늘의 지도 | 첫 1분 이탈 | 이미 `script_knowledge.md` — 점검만 추가 |
| 6 | **리듬 곡선**: 초반 장면 짧게(6~10초), 중반 길게(12~20초), 결론 전 다시 짧게 | 점점 넓어지는 리듬 + 결말 가속 | `prompts/script_hybrid.md` |
| 7 | **업로드 후 시청 유지 곡선으로 보정**: 이탈 지점 ↔ 장면 대조표 → 다음 회 규칙 수정 | 정답 간격은 채널마다 다름 | vidIQ `vidiq-retention-analysis` 스킬(세션에 있음, 채널 연결·크레딧 필요) 또는 YouTube Studio |

## 4. 연출 관련 도구·스킬
| 도구 | 용도 | 라이선스 | 판단 |
|---|---|---|---|
| **우리 측정기** (`ytflow style` = ffmpeg 장면 변화·정지 비율) | 벤치마크·우리 영상 리듬 측정 | 자체 | 사용 중 → 영상마다 자동 기록 제안 |
| **PySceneDetect** | 장면 경계 검출(더 정밀), 참고 영상 컷 목록 | BSD-3 (공식 확인) | 도입 가능 — 측정기 보강 |
| **OpenTimelineIO** | 우리 타임라인(장면·박자·자료 화면 구간)을 Premiere·DaVinci·Final Cut 이 읽는 형식으로 내보내기 → 사람이 미세 조정 | Apache-2.0 (원문 확인) | **추천** — 연출 데이터를 편집 프로그램과 주고받음 |
| **auto-editor** | 직접 녹음한 목소리의 무음·실수 구간 자동 자르기 | Unlicense(퍼블릭 도메인, 원문 확인) | 직접 녹음할 때만 |
| **ffmpeg-skill** (설치됨) | 장면 검출·하이라이트·접촉 시트 | MIT | 사용 중 |
| **HyperFrames 전환 블록** (설치됨, 109종) | 장 전환·자료 화면 진입 변형(와이프·마스크·줌) | Apache-2.0 | 그래픽 팩의 '전환' 컴포넌트로 |
| **retention-editing 스킬** (thecraighewitt/skills) | '시청 유지 편집 전략가' 역할 지시문(형식·시청 유지 곡선을 묻고 편집 조언) | MIT (원문 확인), 보안 점검 통과 표시 | 참고용 — 내용이 일반론, 우리 규칙(위 표)이 더 구체적 |
| **vidIQ retention-analysis** (세션에 있음) | 실제 업로드 영상의 이탈 지점 분석 | vidIQ 계정·크레딧 | 업로드 후 보정 단계에서 (비용 확인 후) |
| Remotion / Motion Canvas | 프로그램 방식 영상 | 회사 유료 / MIT | 도입 안 함(렌더러 겹침, docs/14) |

## 출처
- 시청 유지·패턴 깨기: [AIR Media-Tech](https://air.io/en/youtube-hacks/advanced-retention-editing-cutting-patterns-that-keep-viewers-past-minute-8), [socialk.it](https://socialk.it/en/blog/youtube-audience-retention-guide), [Pixflow](https://pixflow.net/blog/?p=93140), [Overseeros](https://www.overseeros.com/blog/youtube-audience-retention-9-fixes-viewer-drop-off)
- MrBeast 제작 지침(2차 보도): [Tubefilter](https://www.tubefilter.com/2024/09/17/mrbeast-internal-production-guide-leaked-key-points/), [OMR](https://omr.com/de/daily/mrbeast-doc-pdf-leak), [NetInfluencer](https://www.netinfluencer.com/mrbeast-productions-leaked-internal-document-rosanna-pansino/)
- Vox·Johnny Harris: [The Long Story](https://thelongstory.substack.com/p/why-the-best-journalists-on-youtube), [Medium 분석](https://medium.com/@LMK_writing/how-johnny-harris-mastered-visual-storytelling-on-youtube-343ddf9160ec), [The Explainers](https://theexplainers.substack.com/p/making-the-trivialnontrivial-how)
- J컷·L컷: [TechSmith](https://www.techsmith.com/blog/how-to-edit-videos-l-cuts-and-j-cuts/), [Backstage](https://www.backstage.com/magazine/article/j-cut-film-editing-how-to-75535/), [Spotlight FX](https://spotlightfx.com/blog/what-are-j-cuts-and-l-cuts-professional-dialogue-editing-explained)
- 도구: [PySceneDetect 라이선스](https://scenedetect.com/copyright), [OpenTimelineIO LICENSE](https://raw.githubusercontent.com/AcademySoftwareFoundation/OpenTimelineIO/main/LICENSE.txt), [auto-editor LICENSE](https://raw.githubusercontent.com/WyattBlue/auto-editor/master/LICENSE), [retention-editing 스킬](https://skills.sh/thecraighewitt/skills/retention-editing)
