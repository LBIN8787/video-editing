# 영상편집 — ytflow

유튜브 채널 **식스시그마**를 기준으로 하고 **AI비즈PT**와 **로제타**를 보조 기준으로 삼아,
"영상 하나를 따라 만드는 것"이 아니라 **기획부터 편집까지 제작 시스템 전체를 벤치마킹해 자동화**하는 파이프라인입니다.

```
벤치마킹(월1) → 소스탐색 → 주제선정⏸ → 리서치 → 대본⏸ → 음성 → 자막 → 화면소스 → 가편집⏸ → 업로드 패키지
```

- **docs/01-benchmark.md**: 무엇을 어떻게 벤치마킹하나 (측정 틀, 장르 가설 체크리스트, 주의점)
- **docs/02-workflow-sop.md**: 단계별 SOP, 사람과 자동화의 역할 분담, 크론 운영, 품질 체크리스트
- **docs/03-benchmark-result.md**: 식스시그마·AI비즈PT 실제 벤치마킹 결과 (규칙 원본: `data/style_profile.json`)

## 설치

```bash
cd video-editing
pip install -r requirements.txt     # ffmpeg/ffprobe 는 OS 패키지로 설치
```

**Claude 연결 방식** (`config/pipeline.yaml` → `llm.backend`)
- `claude-cli` (기본): Claude Pro/Max **구독**으로 동작합니다. API 키가 필요 없습니다.
  `npm install -g @anthropic-ai/claude-code` 로 설치하고, `claude` 를 한 번 실행해 구독 계정으로 로그인하세요. 구독 사용량 한도를 함께 씁니다.
- `api`: Anthropic API를 씁니다. `export ANTHROPIC_API_KEY=...` 가 필요하고, 쓴 만큼 과금됩니다.

1. `config/channels.yaml`: 벤치마킹 채널 목록입니다. 식스시그마(기준)와 AI비즈PT가 들어 있고, 로제타는 주소를 확인하면 추가합니다.
2. `config/pipeline.yaml`: 채널 분야, 시드 키워드, TTS 목소리, 폰트, BGM, 게이트를 설정합니다.

## 빠른 시작

```bash
python -m ytflow benchmark --video        # data/style_profile.json 생성
python -m ytflow new "첫-영상"
python -m ytflow run 첫-영상                # 게이트마다 멈추면 approve 후 다시 run
```

## 구성

| 경로 | 내용 |
|---|---|
| `ytflow/stages/benchmark.py` | 채널 outlier, 제목, 자막 훅, 말 속도, 컷 속도 측정 → Claude가 스타일 규칙 추출 |
| `ytflow/stages/discover.py` | 키워드 최신 영상 + 구독자 대비 조회수 아웃라이어 + RSS |
| `ytflow/stages/writing.py` | 주제 선정, 팩트시트, 씬 단위 대본, 업로드 패키지 (Claude 구조화 출력) |
| `ytflow/stages/media.py` | TTS/녹음 정리, ASS/SRT 자막(강조색, 큰글씨), 샷리스트, ffmpeg 가편집, 타임라인 CSV |
| `prompts/*.md` | 각 단계 프롬프트. 채널 톤에 맞게 자유롭게 고치세요 |
| `data/`, `projects/` | 실행 결과 (git 제외) |

## 한계 (솔직하게)

- 이 도구를 만든 환경에서는 YouTube에 접속할 수 없어서, **세 채널의 실제 측정은 아직 하지 않았습니다**.
  처음 `benchmark` 를 돌렸을 때 나오는 결과가 진짜 벤치마킹입니다.
- `draft.mp4` 는 **가편집**입니다. 밈 삽입, 정밀한 효과음 위치, 색보정은 편집자가 `timeline.csv` 를 보며 마무리합니다.
- YouTube 페이지 구조가 바뀌면 yt-dlp를 업데이트해야 할 수 있습니다 (`pip install -U yt-dlp`).
- 업로드는 자동화하지 않았습니다 (최종 확인은 사람이 하도록).
