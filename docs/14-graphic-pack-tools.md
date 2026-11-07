# 14. 그래픽 팩에 쓸 수 있는 스킬·도구 조사 (2026-11-07)

그래픽 팩 = **그림(컴포넌트: 그래프·도형·카드·지도·아이콘·일러스트)** + **겉모습(색·글꼴·배경·질감)** (docs/13).
조사 기준: ① 상업 유튜브에 써도 되는 라이선스 ② 클라우드·PC 둘 다 키 없이 ③ 지금 렌더러(HyperFrames HTML + rough.js)에 붙이기 쉬움 ④ 대본(연출)을 안 바꿔도 됨.

## 추천 (도입 순서)
| # | 도구 | 그래픽 팩에서 맡을 것 | 라이선스 (원문 확인) | 붙이는 법 | 판단 |
|---|---|---|---|---|---|
| 1 | **HyperFrames 레지스트리 블록** (이미 설치, 448개) | 이름 자막 14종(`lt-clean-bar`, `lt-soft-pill`, `lt-kicker-name`, `lt-side-rule` …), 지도(`world-map`, `spain-map`, `us-map-hex`), 차트·도식(`data-chart`, `bar-chart-race`, `flowchart`, `heatmap`), 손그림(`hw-*`), 질감(`halftone-field`, `caption-texture`) | Apache-2.0 (hyperframes 0.8.190 고정) | `hyperframes add <블록>` → 컴포넌트 변형으로 등록(`graphics.py` 의 lower·map·compare) | **바로 도입** — 추가 설치·비용 없음 |
| 2 | **Anthropic `theme-factory` 스킬** | 겉모습 팩: 색 팔레트 + 글꼴 짝 10종(Ocean Depths, Modern Minimalist, Golden Hour …) + 새 테마 즉석 생성 | **Apache-2.0** (LICENSE.txt 확인) | 테마 10종을 `skins/<id>/skin.yaml` 로 옮김(색 → palette 토큰, 글꼴 → 한글 OFL 글꼴로 대응) | **도입** — 우리 스킨과 개념이 같음 |
| 3 | **roughViz.js** · **chart.xkcd** | 손그림 차트 종류 확장: 원형·도넛·꺾은선·산점도·누적 막대 (rough.js 기반) | 둘 다 **MIT** (원문 확인) | npm 고정 버전 → HTML 장면에서 SVG 로 그린 뒤 GSAP 로 그리기 애니메이션 | **도입** — compare·proportion·trend 의 '손그림' 변형 |
| 4 | **Phosphor Icons** | 아이콘 팩: 같은 아이콘을 6가지 굵기(thin·light·regular·bold·fill·duotone)로 → 팩마다 아이콘 느낌만 바꿈 | **MIT** (원문 확인) | `ytflow/assets/icons/<팩>/` 에 SVG, `skin.yaml` 에 `icons: phosphor-duotone` | **도입** — 지금 Lucide(ISC) 1종 → 팩별 선택 |
| 5 | **한글 OFL 글꼴** (Google Fonts: Black Han Sans, Do Hyeon, Gowun Batang·Dodum, Noto Serif/Sans KR) | 글꼴 팩: 썸네일·장 표지용 굵은 제목체, 다큐용 바탕체 | SIL OFL 1.1 (배포 시 라이선스 문서 같이) | `ytflow/assets/fonts/` + `skin.yaml` 의 fonts | **도입** |
| 6 | **Open Peeps** (Pablo Stanley) | 손그림 사람 일러스트(조합식) — 비유·사람 수·인물 실루엣 | **CC0** | SVG 몇 장만 골라 `ytflow/assets/illust/` (출처 기록) | 도입 (필요한 만큼) |
| 7 | **ambientCG · Poly Haven 질감** | 배경 팩: 종이·판지·필름·콘크리트 질감 | **CC0** | `skin.yaml` 의 `background: {type: image, file: …}` | 도입 (배경 종류 늘릴 때) |

## 조건부 / 보류
| 도구 | 이유 |
|---|---|
| LottieFiles 무료 애니메이션 | 공개 파일은 'Lottie Simple License'(상업 가능, 출처 표시 권장)지만 **작가별로 다른 조건**이 붙기도 함 → 파일마다 라이선스 확인 후 1개씩만 |
| unDraw 일러스트 | 상업 무료·색 바꾸기 가능하지만 **묶음(팩) 재배포 금지** → 저장소에 모아 두지 말고 쓸 때 한 장씩 받기 |
| Humaaans | 출처마다 라이선스 설명이 달라(CC0 / 상업 무료 / NC 표시) 확인 전 보류 |
| Style Dictionary (Apache-2.0) · W3C 디자인 토큰 형식(DTCG 2025.10) | `skin.yaml` 을 표준 토큰 형식으로 바꿔 다른 도구(Figma 등)와 주고받을 때만. 지금은 불필요 |

## 도입하지 않음
| 도구 | 이유 |
|---|---|
| Remotion | 직원 4명 이상 회사는 유료 라이선스, React 로 렌더러를 다시 써야 함 |
| Motion Canvas / Revideo (MIT) | 라이선스는 좋지만 지금 HyperFrames 렌더러와 겹침 → 렌더러 교체 비용만 큼 |

## 출처
- theme-factory: [anthropics/skills LICENSE.txt](https://raw.githubusercontent.com/anthropics/skills/main/skills/theme-factory/LICENSE.txt), [소개](https://mcpservers.org/agent-skills/anthropic/theme-factory)
- roughViz: [LICENSE (MIT)](https://raw.githubusercontent.com/jwilber/roughViz/master/LICENSE) · chart.xkcd: [LICENSE (MIT)](https://raw.githubusercontent.com/timqian/chart.xkcd/master/LICENSE)
- Phosphor: [LICENSE (MIT)](https://raw.githubusercontent.com/phosphor-icons/core/main/LICENSE), [굵기 6종 안내](https://allsvgicons.com/blog/phosphor-icons-complete-guide/)
- Open Peeps: [openpeeps.com (CC0)](https://openpeeps.com) · unDraw: [license](https://undraw.co/license) · Poly Haven: [license (CC0)](https://www.polyhaven.com/license) · ambientCG: [소개](https://app.cinevva.com/guides/free-textures-hdris-materials)
- Lottie: [Animation licensing basics](https://help.lottiefiles.com/animation-licensing-basics-), [Commercial use](https://help.lottiefiles.com/commercial-use-guide)
- 한글 글꼴: [Black Han Sans (fontsource)](https://fontsource.org/fonts/black-han-sans/about), [Noto Serif KR](https://fontsource.org/fonts/noto-serif-kr/about), [Gowun Batang](https://online-fonts.com/fonts/gowun-batang)
- Remotion: [License](https://remotion.dev/docs/license) · Motion Canvas 비교: [remotion.dev/docs/compare/motion-canvas](https://www.remotion.dev/docs/compare/motion-canvas)
- 디자인 토큰: [W3C DTCG 형식](https://camoa.github.io/dev-guides/design-systems/tailwind-tokens/w3c-design-tokens-format)
