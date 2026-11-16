# 37. 고성능 모션그래픽 — 조사와 도입 (2026-11-16)

> 사용자: "고성능 모션그래픽을 만드는 방법에 대해서 노하우를 조사하고 도입해줘"

`docs/32` 는 **무슨 기법**(글자 쪼개기·모프·매치 무브 …)을 쓸지였다. 이번은 같은 기법을 **얼마나 매끄럽고 또렷하게** 만드느냐 — 움직임의 질, 렌더 정확도, 출력 화질, 그리고 그것을 재는 법이다.
결론부터: 우리 영상이 '싸 보이는' 이유는 기법이 모자라서보다 **① 정수 픽셀로 반올림되는 확대(떨림) ② 렌더러마다 제각각인 길이·곡선 ③ 측정 없이 눈으로만 확인**이 컸다. 셋 다 고쳤다.

## 1. 노하우 — 세 층

### 1-1. 움직임의 질 (모션 디자인)
| 노하우 | 내용 | 우리 기본값 (`ytflow/stages/motionkit.py`) |
|---|---|---|
| **움직임 토큰** | 길이·곡선을 색·글꼴처럼 토큰으로 정하고 렌더러마다 숫자를 새로 쓰지 않는다. 디자인 시스템들이 공통으로 권함 | `DUR`·`EASE`·`STAGGER` |
| 등장은 감속, 퇴장은 가속 | 들어오는 것은 빠르게 와서 부드럽게 멈추고(ease-out), 나가는 것은 천천히 출발해 빠르게 사라진다(ease-in) | enter `expo.out` · exit `power3.in` |
| **퇴장은 등장보다 짧게** | 약 2/3~3/4. 사라지는 것이 시선을 붙잡지 않게 | enter 0.5s · exit 0.28s (HyperFrames 측정: 퇴장은 40~50% 짧게) |
| 거리·중요도에 비례한 길이 | 작은 강조 0.15~0.2s, 등장 0.35~0.6s, 화면 안 이동 ~0.8s(1.2s 이하), 카메라는 박자 하나 내내 | micro 0.18 · move 0.8 · camera 2.5 |
| 위치 이동에 직선 곡선 금물 | 일정 속도(linear)는 기계적으로 보인다. 걷기·흐르는 배경처럼 '일정해야 하는 것'만 예외 | move `power2.inOut` |
| **차례 간격 상한** | 항목당 30~70ms, 전체가 너무 길어지지 않게 상한 — 많을수록 간격을 좁힌다 | `stagger(n)`: 0.06s, 전체 ≤ 0.8s · `OVERLAP` 0.4 (앞 요소 30~50% 진행 시 다음 시작) |
| 넘침(overshoot)은 아껴서 | 10~20% 넘침까지. 매번 튕기면 장난스럽다 — 숫자 확정·성공 같은 '특별한 순간'에만 | pop `back.out(1.4)` (감쇠비 0.7~0.85 '고급' 수준) |
| 예비 동작(anticipation) | 큰 움직임 직전 반대쪽으로 살짝(본동작의 20~30% 길이). 이미 `stage` 의 떨어지기·납작해지기에 있음 | — |
| **셔터 흐림(모션 블러)** | 빠른 이동이 '뚝뚝 순간이동'처럼 보이는 것을 막는다. 영화 기본 180°(프레임 시간의 절반 노출) = 높은 fps 로 그려 하위 프레임 평균 | `motion_blur_vf(120, 30)` → `tmix=frames=2,fps=30` |
| 한 순간 한 초점 | 한 시점에 5개 넘게 동시에 나오면 시선이 갈 곳이 없다 (우리 '강조 예산' v4 와 같은 뜻) | lint `crowd` |

### 1-2. 렌더 정확도 (매끄러움은 대부분 여기서 결정)
- **시간으로 그리기(결정적 렌더)**: 실시간 재생을 녹화하지 않고, 멈춘 타임라인을 프레임 시각으로 `seek` 해서 한 장씩 찍는다 → 렌더 속도와 무관하게 프레임 빠짐이 없다. HyperFrames(`tl` paused + seek)가 이미 이렇게 한다. Playwright 로 직접 찍을 때도 `requestAnimationFrame`·`setTimeout` 에 기대지 말 것.
- **정수 픽셀 반올림 = 떨림**: ffmpeg 의 `scale(eval=frame)+crop`·`zoompan` 은 자르는 위치·크기를 정수로 반올림해 느린 확대가 '멈춤·점프'를 번갈아 한다(ffmpeg trac #4298, 10년째 열려 있음). 흔한 처방은 '크게 키운 뒤 zoompan'인데 **우리 측정으로는 4배로도 남는다**(아래 표). → 프레임마다 **실수 좌표 아핀 변환**으로 그리는 `motionkit.smooth_zoom` 을 만들었다.
- **transform·opacity 만 움직이기**: `left/top/width/height` 를 움직이면 레이아웃을 다시 계산하고 픽셀 단위로 떨린다. `x·y·scale·rotation` 으로.
- **비싼 효과는 짧게**: `filter: blur()`·큰 `box-shadow`·그라데이션은 프레임마다 다시 그린다. 헤드리스 크롬은 GPU 를 끄므로 더 느리다(Remotion 문서). 흐림 애니메이션은 짧게, 그림자는 그림(PNG)으로 굽기.
- **병렬은 측정해서**: 렌더 동시 실행 수는 많을수록 빠르지 않다 — 너무 많으면 크롬이 느려진다(Remotion: 기본 = 스레드의 절반, benchmark 로 고르기).

### 1-3. 출력 화질 (유튜브가 다시 압축한다)
- **x264 설정** `motionkit.encode_args(kind)`: 납품 `-crf 17 -preset slow -x264-params aq-mode=3`, 그래픽만 있는 장면은 `-crf 16 -tune animation`(넓은 평면·또렷한 테두리용 — 실사 섞이면 쓰지 않음), GOP 2초, `+faststart`, `yuv420p`.
  - `aq-mode=3` 은 어두운 평면에 비트를 더 줘서 어두운 배경 그라데이션의 띠·네모 깨짐을 줄인다.
- **그라데이션 띠(banding)**: 8비트는 256단계라 넓은 그라데이션·비네트·어두운 배경에 계단이 생기고, 유튜브 재압축에서 더 심해진다. 잡음(grain)이 자연스러운 디더 역할 → 8비트로 내기 직전 눈에 안 보이는 시간 잡음 `dither_vf()` = `noise=alls=2:allf=t`.
- **정수 fps**: 30 또는 60. 29.97 은 움직임 박자가 어긋난다.
- **1440p 업로드 요령 (논쟁 있음, 시험 필요)**: 1440p 이상으로 올리면 유튜브가 VP9/AV1 높은 비트레이트로 처리한다는 경험담이 많지만 공식 문서는 없고, 가는 글자·선은 1080p 업로드가 더 낫다는 반대 시험도 있다. → 기본은 1080p, 빠른 움직임이 많은 편 하나로 1080p/1440p 둘 다 올려 비교한 뒤 정한다(비공개 업로드).

## 2. 측정 — `python -m ytflow motion-qa <프로젝트 | 영상.mp4>`
사람 눈의 '뚝뚝 끊긴다·떨린다'를 숫자로 바꿨다 (`ytflow/stages/motionqa.py`, 결과 `05_edit/motion_qa.json`).
- 프레임마다 앞 프레임과의 차이(움직임 양)를 재고, 주변 9프레임의 윗사분위를 '정상 움직임'으로 삼는다.
- **멈칫**: 움직이는 중에 거의 같은 프레임(정상의 30% 미만) — 프레임 중복·정수 반올림.
- **점프**: 정상의 1.5배 넘게 튐 — 프레임 빠짐(fps 변환·렌더 누락)·정수 픽셀 확대.
- **고름(smoothness)**: 움직이는 프레임 중 멈칫·점프가 아닌 비율. 15프레임 안에 3번 이상 몰리면 '문제 구간'.
- 규격: 정수 fps·yuv420p·코덱. 4초 넘게 화면이 멈춘 곳(`long_holds`)도 기록(시청 유지 참고).
- 프로젝트를 주면 그 안의 HyperFrames `index.html` 도 `lint_gsap` 으로 점검: `layout-prop`·`blur-anim`·`linear-move`·`too-fast`(<0.12s)·`too-slow`(>2s)·`overshoot`(back.out > 2.5)·`crowd`(한 순간 5개 이상).

### 측정 결과 (1080×1920, 3초, 1.00→1.04 확대, 같은 그림)
| 방법 | 고름 | 문제 |
|---|---|---|
| 예전 쇼츠 `scale(eval=frame)+crop` | **42%** | 멈칫 49프레임 — 프레임 절반이 멈추고 절반이 3px 점프 |
| zoompan, 4배 키운 뒤 | 92% | 멈칫·점프 2구간 |
| zoompan, 8배 키운 뒤 | 97% | 없음 — 그러나 한 프레임이 8640×15360(약 400MB)이라 실무 불가 |
| 프레임 하나씩 빠진 영상(시험용) | 81% | 점프 11프레임 — 프레임 빠짐도 잡는다 |
| **`motionkit.smooth_zoom` (실수 좌표 아핀)** | **100%** | 없음, 움직임 양이 sine 곡선 그대로 |

## 3. 도입한 것
| 무엇 | 어디 |
|---|---|
| 움직임 토큰·차례 간격·GSAP 상수(`gsap_tokens_js`) | `ytflow/stages/motionkit.py` |
| 떨림 없는 확대 `smooth_zoom` | 같은 파일 · **쇼츠 렌더러에 적용** (`ytflow/stages/shorts.py` 큰 글씨 장면: 고름 42% → 100%) |
| 셔터 흐림 `motion_blur_vf` · 띠 막기 `dither_vf` · 인코딩 `encode_args` | 같은 파일 (렌더러가 골라 씀) |
| GSAP 타임라인 점검 `lint_gsap` | 같은 파일, `motion-qa` 가 프로젝트 HTML 에 자동 실행 |
| 움직임 측정 명령 `motion-qa` | `ytflow/stages/motionqa.py`, `python -m ytflow motion-qa` |

## 4. 아직 안 한 것 (다음 차례)
- **다른 렌더러의 정수 확대**: `media.py`(켄 번스 `zoompan`)·`archive.py`·`directions.py` 의 확대도 같은 문제일 가능성이 크다. `motion-qa` 로 하나씩 재고 `smooth_zoom` 으로 바꾼다 (영상 입력은 사진과 달리 프레임마다 원본이 바뀌므로 같은 방식의 영상판이 필요).
- ~~HyperFrames 렌더에 셔터 흐림~~ → **해결**: HyperFrames 0.8.190 에 렌더 모션 블러가 있다. 컴포지션 뿌리에 `data-motion-blur="on"`(이동은 요소별 필터, 회전·확대는 진짜 하위 프레임 캡처, `data-motion-blur-shutter` 로 길이). `--fps` 는 240 까지. ffmpeg `motion_blur_vf` 는 HyperFrames 밖의 렌더러용으로 남긴다.
- **렌더러의 숫자를 토큰으로**: `stage.py` 의 `back.out(3)`·`back.out(2.5)`(넘침 과함)처럼 렌더러마다 흩어진 길이·곡선을 `motionkit.EASE/DUR` 로 모은다 — 장면 모양이 바뀌므로 렌더러 담당이 비교 렌더를 보고 결정.
- **매뉴얼 반영**: 매뉴얼은 지금 담당(정기 검토 세션)이 잠금을 가지고 있어 이 세션은 고치지 않았다. `motion-qa` 를 체크리스트 SHOULD 로, 움직임 토큰을 '스타일 기본값' 층으로 넣자고 제안함(`proposals/manual/`)에 남겼다.

## 5. HyperFrames 자체 기준 (설치 후 확인, `tools/hyperframes/.../skills/hyperframes/references/motion.md`)
공식 런치 필름을 프레임 단위로 잰 기본값 — 우리 토큰을 여기에 맞췄다.
- 빠른 이동은 0.3~0.6초 + 가장 빠른 프레임에 흐림 6~12px(글자 크기)·15~20px(화면 전체).
- 착지는 긴 꼬리(`expo.out`·`power4.out`), 카메라·색 번짐은 양쪽(`power2.inOut`), 빠져나가는 확대·퇴장은 가속(`power3.in`). **모든 곳에 같은 `power2.out` 0.5초 = '생성된 영상' 느낌.**
- 퇴장은 등장보다 40~50% 짧게, 다음 요소는 앞 요소가 30~50% 진행됐을 때. 글자 1프레임·단어 60~120ms·목록 40~80ms 간격.
- 착지한 제목은 완전히 정지 — 움직임은 다음 요소·카메라·배경으로 넘긴다. 읽어야 할 줄은 0.5초 + 단어당 0.3초 머문다.
- 제목 등장은 영상 안에서 바꿔 가며: 단어별 흐림→또렷(0.13초, 0.067초 간격) · 회색→먹색 · 한 줄 흐림 · 글자별 · 슬롯머신.

## 6. 초안 — `python scripts/motion_demo.py [출력폴더]`
시장 대시보드 계열 12초(예시 데이터): 단어별 흐림 등장 → 대시보드 판이 0.45초에 미끄러져 들어오며 렌더 모션 블러 → 숫자 칸 3개 차례·겹침 + 착 붙는 카운트업 → 막대 차례 성장, 강조 막대만 튕김 → 선 그리기 + 끝점 따라가기 → 아주 느린 카메라 → 어둡게 덮고 결론 한 줄.
- 렌더 60초(1920×1080, 30fps, 워커 1), `lint_gsap` 0건, `motion-qa` 고름 97% 문제 0.
- 처음 렌더에서 프레임을 뽑아 보니 ① 대시보드 안 글자·격자가 제목 화면에 미리 보였고 ② '줄어드는 값'인데 선이 올라갔다(SVG 의 y 는 아래로 커짐) → 고침. **프레임을 뽑아 직접 보는 단계가 여전히 필요하다.**
- `motion-qa` 개선: 짧은 움직임의 느린 시작·착지를 '멈칫'으로 잘못 잡던 것을 '앞뒤에 큰 움직임이 있는 골짜기'만 잡도록 고침 (초안 90% → 97%, 예전 쇼츠 확대는 여전히 46%로 잡힘).

## 출처
- 정수 확대 떨림: [FFmpeg trac #4298 zoompan creates shaky image](https://trac.ffmpeg.org/ticket/4298), [ffmpeg-devel 패치 "fix shaking when zooming"](https://ffmpeg.org/pipermail/ffmpeg-devel/2020-February/257073.html), [Bannerbear — Ken Burns with FFmpeg(키운 뒤 zoompan)](https://www.bannerbear.com/blog/how-to-do-a-ken-burns-style-effect-with-ffmpeg/)
- 움직임 원칙·토큰: [12 principles of animation (userinterface-wiki)](https://userinterface-wiki.vercel.app/12-principles-of-animation), [UI/UX Atlas — 12 principles adapted to UI](https://uiux-atlas.pages.dev/lessons/motion/the-12-principles-of-animation-adapted-to-ui), [Sprout Social Seeds — Motion](https://seeds.sproutsocial.com/visual/motion/), [Cognite Aura — Motion](https://docs.cognite.com/aura-design-system/foundations/motion), [Motion Design Principles](https://madegooddesigns.com/motion-design-principles/)
- 셔터 흐림: [RenderMan — Motion Blur](https://rmanwiki.pixar.com/x/144NB), [Redshift — Motion Blur](https://help.maxon.net/c4d/en-us/Content/_REDSHIFT_/html/Motion+Blur+-+Advanced.html), [Unity Recorder — Accumulation](https://docs.unity3d.com/Packages/com.unity.recorder@5.1/manual/RecorderAccumulationProperties.html)
- 렌더 성능: [Remotion — Performance](https://www.remotion.dev/docs/performance), [Remotion — GPU](https://www.remotion.dev/docs/gpu)
- 띠·디더·x264: [Fora Soft — banding](https://www.forasoft.com/learn/video-quality/articles-vqm/banding-gradient-steps), [Fora Soft — dithering](https://www.forasoft.com/learn/video-encoding/glossary/terms/dithering), [doom9 — banding 토론](https://forum.doom9.org/archive/index.php/t-167706.html)
- 1440p 업로드 (논쟁): [OBS 포럼 — upscaling lifehack](https://obsproject.com/forum/threads/lifehack-how-to-improve-image-quality-of-livestreams-uploads-to-youtube-by-upscaling.140425), [VEGAS 포럼 — 1440p worth it?](https://www.vegascreativesoftware.info/us/forum/youtubers-vp09-upscaling-to-1440p-worth-it-or-not--118289), [VideoHelp — 반대 시험](https://forum.videohelp.com/showthread.php?p=2778685)
