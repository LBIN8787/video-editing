# (가칭) AI 꿀팁 1분 (`ch-ai-shorts`)

- **형식:** shorts — 짧은 주제 안내 (formats/shorts.md)
- **편집 스타일:** 쇼츠 · AI 꿀팁 쇼츠 스타일 (9:16) → `styles/shorts-aitips/`
- **콘셉트:** GitHub 에서 뜨는 AI 도구·Claude/Codex 스킬·MCP 서버 하나를 30~45초에 '무엇이고 어떻게 쓰나'만 안내하는 쇼츠 채널.
- **분야:** AI 활용법과 GitHub 화제 저장소 안내. README 에 있는 기능만 말한다.
- **업로드 주기:** 주 3~5편
- **설정:** `channel.yaml` (키워드·분량·목소리). 만든 영상 기록: `episodes.md`

## 한 편 만들기
```bash
python -m ytflow make --channel ch-ai-shorts                          # 트렌드에서 주제 자동 선정
python -m ytflow make --channel ch-ai-shorts --topic "주제"            # 주제 지정
python -m ytflow make --channel ch-ai-shorts --from-text 조사글.md      # 대화형 LLM 답·메모를 영상으로
```
GitHub 최근 14일 별 증가로 소재를 고릅니다.

## 올리기 전 점검
- 첫 2초에 결과·이득이 나오는가
- README 에 없는 기능을 말하지 않는가
- 자막이 유튜브 UI 에 가리지 않는가
- `05_edit/final.mp4` (음량 −14 LUFS 마스터링본), `05_edit/delivery_check.json` (유튜브 규격), `REPORT.md` 의 남은 일
