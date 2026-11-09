# unslop 시연 자료 — 다시 만들기

예제 화면: heydamir/unslop `examples/dashboard.html` (CC BY 4.0, Damir Sokolovsky) — 커밋 97daa3e 기준. 저장소에는 넣지 않고 받아서 씁니다.

```bash
git clone https://github.com/heydamir/unslop /tmp/unslop && cp /tmp/unslop/examples/dashboard.html original.html
python build_story.py ../../../../ytflow/assets/icons .      # story.html(단계별 CSS) · after.html · before_rebuilt.html
node shot169.js original.html before169.png && node shot169.js after.html after169.png   # 16:9 전/후 화면
node record_morph.js story.html morph                          # 4단계로 고쳐지는 과정 녹화 (우리 코드, unslop 의 story.mjs 는 실행 안 함)
node record_term.js term_log.txt term                          # 실제 설치 기록 재생 녹화
node cap_web.js https://github.com/heydamir/unslop gh_repo.png # 저장소 화면
```
그다음 `04_assets/footage/` 의 mp4 만들기는 `docs/` 대신 이 프로젝트 제작 기록(커밋 메시지)과 같은 ffmpeg 명령을 씁니다:
`morph.mp4` = morph webm 을 1.9초부터 17.5초 → tpad 10초, `term.mp4` = term webm 0.9초부터 → tpad 12초, `gh/before/after.mp4` = `archive.still_to_clip`.
