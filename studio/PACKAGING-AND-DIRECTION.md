# 제목·썸네일과 연출/그래픽 분리 기준

앞으로 모든 신규 영상은 **영상 제목, 쇼츠 세로 표지, 가로 썸네일, 선택 이유**를 함께 제작한다. 제목은 영상의 실제 문제·해결 방법과 일치해야 하며, 썸네일은 같은 문장을 반복하기보다 입력과 결과를 한눈에 보여 준다. 조회수·CTR 상승은 실제 게시 후 측정하기 전 보장하지 않는다.

## 서로 다른 세 가지

| 항목 | 결정할 것 | 파일 | 그래픽을 바꿨을 때 |
|---|---|---|---|
| 편집점 | 언제 장면을 자르고 무엇으로 넘어가는가 | edit-points.json | 프레임·순서·길이를 유지 |
| 편집 포인트 | 그 장면에서 무엇을 언제 주목시키는가 | emphasis.json | 강조 대상·시점을 유지 |
| 편집 스타일 | 그것을 어떤 이미지·색·배경·그래픽으로 표현하는가 | skins/*.json 및 이미지 매핑 | 이 부분만 교체 |

편집점과 편집 포인트를 합쳐 연출 계획으로 보고, 그래픽은 별도 스킨으로 둔다. 예를 들어 “파일 선택 장면으로 전환 → 내레이션 파일에 주목”이라는 연출은 그대로 두고, 폴더 그림·실제 파일 화면·다른 색상의 UI 그래픽으로 표현할 수 있다. 실제 이미지에 강조를 넣을 때는 스킨의 focus_regions로 같은 의미 대상의 표시 위치를 지정한다.

대본·자막·음성은 content.json에 있다. 제목·썸네일은 packaging.json에 있다. 이 파일들은 색상·배경을 바꾼다고 다시 생성하지 않는다. 고정 ElevenLabs 음성, 날짜·회차 숨김과 무효과음 기준도 유지한다.

## 이번 두 영상의 패키징

- Remotion: **AI 쇼츠 디자인, 매번 바뀐다면? Remotion으로 편집 틀 고정하기**. 썸네일은 “디자인은 고정 / 내용만 교체”. 동일한 틀의 휴대폰 두 개로 고정과 교체를 구분한다. 제목에는 문제와 도구, 그림에는 작업 방식을 담았다.
- Whisper: **자막 타이핑 줄이는 법｜Whisper로 음성에서 자막 초안 만들기**. 썸네일은 “음성 파일로 / 자막 초안”. MP3 파형에서 SRT로 이어지는 그림으로 입력과 결과를 연결한다. “초안”과 검수 표시로 완전 무검수 자동화처럼 보이지 않게 한다.

각 편 packaging/packaging.json에 제목·문구·선택 이유·이미지 해시를 기록한다. 두 편을 지칭한 이번 요청은 앞서 승인받은 Remotion(005)·Whisper(006)에 적용했다. 기존 다른 편과 혼동하지 않는다.

## 재사용 명령

새 편 생성기는 production-brief와 별도로 packaging.json과 연출 파일 참조를 만든다. 검수된 props를 export_edit_package.py로 내보내면 층별 파일이 생긴다. 편집점은 원래 프레임을 그대로 추출하고, 강조 계획은 별도로 작성·검수한다. 스킨을 바꿀 때는 이 연출 파일을 수정하지 않는다.

```bash
python scripts/export_edit_package.py --props channels/ai/episodes/ai-007/props.json --out-dir channels/ai/episodes/ai-007/layers --packaging channels/ai/episodes/ai-007/packaging.json
```

emphasis.json을 채우고 reviewed를 true로 하기 전에는 컴파일이 차단된다. 기존 연출 파일을 내보내기로 덮어쓰지 않는다. 편별 이미지 매핑은 asset-bindings.json에 두며 공용 스킨에 다른 영상의 이미지를 고정하지 않는다.

```bash
python scripts/compile_edit_package.py --package channels/ai/episodes/006-whisper/layers/production-package.json --skin styles/shorts-ai-guide/skins/blueprint.json --out /tmp/blueprint-props.json
cd studio/renderer
npx remotion still src/index.ts LayeredShorts out/blueprint-preview.png --props /tmp/blueprint-props.json --frame=1030 --browser-executable=/usr/bin/chromium
```

컴파일러는 편집점·강조·내용·자막·음성 해시와 전체 길이를 출력한다. 스킨에 음성·타이밍 필드를 넣거나 강조가 장면 범위를 넘으면 실패한다. 종이색, 블루프린트, 실제 자료 이미지 스킨으로 같은 장면을 렌더하고 연출 해시가 같은지 확인했다. 이번에는 시각 비교 스틸을 확인했으며 모든 새 스킨의 전체 MP4를 다시 출력한 것은 아니다.

각 층을 묶는 참조 구조는 schemas/shorts-production-package.schema.json을 따른다.

제목·썸네일 출력:

```bash
cd studio/renderer
npx remotion still src/index.ts ShortsCoverVertical out/cover.png --props ../../channels/ai/episodes/005-remotion/packaging/cover-props.json --browser-executable=/usr/bin/chromium
npx remotion still src/index.ts ShortsThumbnailWide out/thumbnail.png --props ../../channels/ai/episodes/005-remotion/packaging/cover-props.json --browser-executable=/usr/bin/chromium
```

표지는 1080×1920, 가로 썸네일은 1280×720이다. 제목과 썸네일의 가독성을 축소본에서도 확인하고 문구가 실제 내용과 맞는지 검수한다. 표지 파일 제작과 YouTube에서의 실제 설정은 별도 단계다. 이번 작업에서 게시·표지 변경은 하지 않았다.

## 완료 시 함께 남길 것

MP4, 제목·설명란 초안, 표지·썸네일 원본, 선택 이유, 편집점, 강조 계획, 스킨·이미지 출처, 검수와 보관 링크를 남긴다. 현재 1.1.1의 기존 렌더 입력과 승인된 MP4는 계속 재현할 수 있다. 새 분리 렌더러는 LayeredShorts이며 스킨 교체용 구성이다.
