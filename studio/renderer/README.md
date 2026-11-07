# AI 실전노트 영상 렌더러

현재 기본은 **ShortsGuideTemplate / 1.1.1**이다. 승인된 시각 안내형 디자인에 파일·요청문·표·슬라이드·흐름·결과 확인 데이터를 넣는다. 날짜·상단 회차는 표시하지 않는다. 음성은 channels/ai/channel.json의 ElevenLabs Han Aim / eleven_v4로 고정한다.

제작 양식과 전체 명령은 ../SHORTS-WORKFLOW.md를 따른다. production-brief → 고정 음성/단어별 시간 → props → MP4 순서다. 원본 자료와 설명용 예시는 구분한다.

```bash
npm ci
npm run typecheck
npx remotion studio src/index.ts --no-open
```

저장소 루트에서 실제 입력을 검증하고 렌더한다.

```bash
python scripts/render_short.py --props channels/ai/episodes/003-xlsx/revisions/visual-v2/props.json --check-only
python scripts/render_short.py --props channels/ai/episodes/003-xlsx/revisions/visual-v2/props.json --out studio/renderer/out/AI-Shorts-003-XLSX-Visual-v2.mp4
```

미디어는 assets-index.json과 각 편 archive.json에 따라 Drive 보관본에서 복원한다. Chromium이 PATH에 없으면 --browser로 경로를 전달한다. Windows는 PYTHONUTF8=1을 사용한다. 비밀정보와 node_modules는 Git에 넣지 않는다.

001·002의 최신 화면은 고정 음성 생성 혼잡으로 무음 미리보기다. `--silent-preview`와 PREVIEW 파일명이 필요하며 최종 음성 영상으로 게시할 수 없다. 003은 기존 고정 음성을 재사용한다. 005·006의 승인된 1.1.0 입력은 그대로 재현할 수 있다.

1.0.0 / ShortsGuideV1, 1.1.0 / ShortsGuideV2와 과거 편별 구성은 이력이다. 새 편의 기본으로 고르지 않는다. 전체 정기 제작과 롱폼 렌더러가 완성됐다는 뜻은 아니다.
