# 시각 안내형 갱신

최신 입력은 props.json, 양식은 production-brief.json(001/002), 상태는 voice-status.json 및 review.md를 본다. 1.1.1 / ShortsGuideTemplate을 사용하며 이전 소스와 MP4는 보존한다.

이 편은 고정 음성 생성 혼잡으로 무음 미리보기다. 최종판은 아직 준비되지 않았다.

```bash
python scripts/render_short.py --props channels/ai/episodes/002-ppt-master/revisions/visual-v2/props.json --silent-preview --out studio/renderer/out/AI-Shorts-002-PPTMaster-Visual-v2-PREVIEW-MUTED.mp4
```

음성 재시도 시 production-brief의 검수된 원고를 한 번만 생성하고 단어별 타이밍을 다시 만들면 된다. 고정 음성 메타데이터와 해시 검증을 통과하기 전 게시하지 않는다.
