# Evidence Motion Lab — 독립 실험 스타일 v0.1

상태: **experimental / 사용자 미승인 / 운영 자동선택 금지**.
기존 Claude 매뉴얼, 레시피, 채널 설정, hybrid 렌더러를 바꾸지 않는다.
이 폴더는 독립 프레임 생성 프로토타입이다. 완성 영상 스타일 전체와 동등한 품질을 검증했다는 뜻이 아니다.

## 기준 자료와 검증 범위
참고 https://www.youtube.com/watch?v=BS8s9fWXlQY
사용자 제공 1080p 30fps 파일, 429.987초. SHA256 c4ee103fe7cc1d7400e9d8a808b40cb2895a76c040d2c770e13774ce14d13cd8.
rea-video 0.1.0의 95샷은 자동 후보이다. 일부 연속 프레임을 직접 비교했다. 전체 음성 청취·전 샷 수동 분석은 미완이다. 원본 제작툴·3D/AI 생성 여부·스톡 출처는 미확인이다.

## 다섯 층을 따로 교체
- 연출: scene.mode, labels, cues. 현재 설명하는 대상에 시선을 넘긴다.
- 움직임: motion.enter/stagger/dim/ease. 시간 단위 초. 샘플 기본값이며 전 채널 의무 기준 아님.
- 그래픽: skin.background/card/ink/accent/radius/font. 라임·원본 캐릭터를 복제하지 않고 청록 기하 아이콘을 사용한다. 스킨 교체는 타이밍을 바꾸지 않는다.
- 자막: subtitle 레이어. 화면 하단 안전영역, 본문과 독립. 대본 자체를 이 스타일에서 만들지 않는다.
- 사운드: 기본 꺼짐. 실제 청취 및 권리 확인 후 외부 어댑터에서 붙인다. 소리가 구현되었다고 주장하지 않는다.

## 관찰 → 구현 모드
| 모드 | 근거 / 설계 | 구현 |
|---|---|---|
| evidence_shift | 00:07~10.5 기존 근거 약화→새 근거 등장→강조 | 두 패널의 순차 등장·대비 이동·밑줄 진행 |
| orbit_accumulate | 00:11~12.5 기준점 유지→서비스 누적 | 독자 기하 기준점 주변 네 슬롯까지 누적 |
| process_cascade | 03:33~35.75 진행바→카드 순차 누적 | 시간 기반 진행바·최대 네 UI 상태 슬롯 |
| metaphor_reveal | 05:45.20~45.55 작은 원→비유 물체 fade | 배지+중앙 슬롯 등장; 실제 금고/캐릭터 에셋 미포함 |
| source_focus | 자료 중심 구간을 수용하기 위한 설계 | 넓은 자료 슬롯, 실제 이미지 합성 어댑터 미포함 |
| comparison | 비교 설명용 확장 설계, 원본 측정 결과 아님 | 좌우 슬롯 |

**정정:** 05:45 장면을 전체 화면 아이리스 와이프로 재현하지 않는다. 연속 표본은 작은 배지와 금고 fade를 보여준다.

## 코드 사용 (영상 제작 아님)
Python 표준 라이브러리만 사용. engine.frame(scene, seconds, overrides)는 SVG 문자열을 반환한다. 파일을 자동 저장하거나 ffmpeg/네트워크/음성 생성/업로드를 실행하지 않는다.

```python
from engine import frame
scene = {'mode':'evidence_shift','labels':['근거 A','근거 B'],
         'cues':[0,1.5], 'duration':4, 'subtitle':'기술 검증용 문구'}
svg = frame(scene, 2, {'skin':{'accent':'#6750a4'}})
```

표준 레시피 등록이 없으므로 `python -m ytflow make --style-ref evidence-motion-lab`은 지원하지 않는다. 승인 후 별도 어댑터가 frame()을 프레임 시각에 호출하도록 연결해야 한다. 임의 채널/프로젝트에 자동 적용하지 않는다.

## 검증과 다음 게이트
실행: `PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s styles/evidence-motion-lab -v`.
9개 단위 테스트 통과: 6모드 XML 파싱, easing, dim, stagger, 스킨/모션 독립, 결정성, 텍스트 escape, 기본 배치 경계, 잘못된 입력 거부.
**아직 미검증:** 브라우저/영상 실제 렌더, 실제 한글 글꼴 폭과 겹침, 오디오·자막 싱크, 자료 이미지/영상 합성, 장면 간 전환, 실제 영상 품질. 테스트 통과는 사용자 합격이 아니다.
운영 통합 전에 주제·대본 승인을 받은 테스트 프로젝트에서 실제 프레임/모션/사운드를 검수하고 사용자가 스타일을 승인해야 한다. 원본 매뉴얼은 보존한다.

## 보관
작은 코드/설정/검증 문서는 실험 Git 브랜치. 원본·rea 결과·프레임은 기존 비공개 Google Drive refs에 별도 보관. 공개 Git에 원본 미디어·비공개 Drive 링크·토큰 없음. PC 원본/동기화 설정 변경 없음.
