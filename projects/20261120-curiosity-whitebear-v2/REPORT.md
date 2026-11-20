# REPORT — 호기심 「생각하지 않으려 할수록 더 떠오르는 이유」 (흰 곰 편, 2026-11-20)

## 단계
| 단계 | 상태 |
|---|---|
| D1 주제 | 통과 — 사용자: "생각하지 않으려 할수록 더 떠오르는 이유 대본 주제 나쁘지 않네요" |
| D2 대본 | **통과** — v3 (사용자 2026-11-20: "대본 좋습니다 제작해주세요") → 사용자 "영상길이 좀 더 길게 해줘" → **v4 `02_script/script_v4.md`·`narration_v4.md` (약 9분 25초), 사용자 확인 대기** |
| D3 검토본 | 원화 대기 — PC Codex(GPT 이미지) 주문 `inbox/pc-tasks/*-art-whitebear.md` (main) |
| D4 최종 | 사용자만 |

## 판본
- v1 `projects/20261120-pattern-curiosity-whitebear` — docs/53 패턴 예시(하이브리드 판, 1:47)
- v2 (이 폴더 `05_edit/final.mp4`) — 네 자리로 나눴지만 이야기 칸이 막대 인물 선 그림 → 사용자 이전 피드백('도형으로 칠한 느낌')과 어긋나 v3 로 교체
- **v3** — 잼·기억 편 방식: GPT 원화 20컷(2×2 시트 5장) + 원화 위 쪽지 + 칸 만화 + 논문 첫 장 + 검은 화면 장 제목

## 만드는 법 (v3)
```
python scripts/anim/narrate.py projects/20261120-curiosity-whitebear-v2/02_script/narration_v3.md $PWD/projects/20261120-curiosity-whitebear-v2/03_voice/v3 --channel ch-knowledge
# 원화 5장(night·lab·lab2·mind·end)을 Drive 영상/20261120-curiosity-whitebear-v2/art/ 에서 04_assets/art/ 로
python scripts/anim/prep_whitebear.py $PWD/projects/20261120-curiosity-whitebear-v2/04_assets/art --paper $PWD/projects/20261120-curiosity-whitebear-v2/04_assets/paper_crop.png
python scripts/anim/ep_whitebear.py <art> <voice v3> <05_edit/v3/ep.html>
bash scripts/anim/render_all.sh <05_edit/v3/r> <ep.html> <voice.mp3> <captions.ass> 251.18 <05_edit/v3/whitebear_v3.mp4> 4
```
- 목소리: ElevenLabs 채널 목소리(ch-knowledge, eleven_v4) 56문장 4:07 — 클라우드에서는 edge-tts 가 프록시에 막혀 `narrate.py --channel` 추가.
- 논문 첫 장: 저자 공개 PDF(하버드 Wegner 아카이브) 1쪽을 잘라 씀 — PDF·그림은 커밋하지 않음.
- PC 자동 빌드 완료: Drive `영상/20261120-curiosity-whitebear-v2/05_edit/whitebear_v4.mp4` (9.4분, 62MB) · 프레임 시트 `whitebear_v4_sheet.jpg`
- 2026-11-20 클라우드에서 PC 자동 빌드를 흉내 내 끝까지 시험(가짜 Drive·자리 그림 시트) — 통과. 고친 것: PDF 쪽 기준(CropBox→MediaBox), 색 빼기 효과의 검은 깜빡임, 1장 끝 10초 검은 화면.
