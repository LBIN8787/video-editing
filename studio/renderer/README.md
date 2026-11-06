# AI 실전노트 Remotion 소스

기존 AI 3편과 퀴즈 2편의 React 구성·자막을 보관한다. 현재 파일은 편별로 작성한 샘플이며 새 대본을 자동으로 넣는 공통 렌더러로 완성된 것은 아니다.

```bash
cd studio/renderer
npm ci
npm run typecheck
npx remotion studio src/index.ts
npx remotion render src/index.ts AIRadar003 out/AI-Shorts-003-raw.mp4 --codec=h264 --browser-executable=/usr/bin/chromium --concurrency=2
```

Chromium 경로는 실행 호스트에 맞게 조정한다. 렌더 전 assets-index.json의 미디어를 public/에 복원해야 한다. public/README.md 참고. 과거 음성·효과음이 필요한 구형 구성은 이력으로 남겼으며 현재 고정 보이스 정책을 통과하지 못한다. 최신 AIRadar003은 ElevenLabs Han Aim 음성 파일을 사용한다.

실제 도구 조작 화면이 없는 장면은 설명용 그래픽이다. 고정 음성을 설정한다고 기존 MP4의 음성이 바뀌지 않는다. 새 제작 시 채널 설정을 확인하고 음성을 생성한 다음 타이밍에 맞게 장면·자막을 조정한다.
