# AI 실전노트 001 제작 노트

조사일: 2026년 11월 6일 KST. 공개 지표는 조사 당시 스냅샷이며 계속 변합니다.

## 소재 선정

| 후보 | 확인한 사실 | 첫 편 적합성 |
|---|---|---|
| last30days | GitHub API 별 66,774개, 생성 2026-01-23, 마지막 코드 갱신 2026-11-05 21:24 UTC | 여러 탭을 오가며 유행을 찾는 일반인의 문제와 연결돼 선정 |
| anthropics/skills | 공식 Agent Skills 저장소, 웹 페이지에서 약 18.8만 별 표시 | 대중적이지만 범위가 넓어 별도 입문편 후보 |
| Hugging Face 상위 모델 | 공개 API trendingScore 정렬의 당시 첫 항목은 moonshotai/Kimi-K3.1-Pro; likes 1,101, createdAt 2026-11-02 | 모델 비교·실행 검증이 더 필요해 이번 편에서는 제외 |

소스: [last30days 공식 저장소](https://github.com/mvanhorn/last30days-skill),
[GitHub 원본 API](https://api.github.com/repos/mvanhorn/last30days-skill),
[Anthropic 공식 저장소](https://github.com/anthropics/skills),
[Hugging Face 공개 API](https://huggingface.co/api/models?sort=trendingScore&limit=5).
원본 응답도 이 폴더의 JSON 파일로 보존했습니다.

last30days를 신규 출시 제품으로 소개하지 않습니다. 높은 누적 관심과 최근 유지보수를
확인한 기존 스킬을 발굴한 편입니다. 별 수만으로 최근 급상승이나 품질 우위를 주장하지 않습니다.
Hugging Face API의 한 번의 순서는 지속적인 트렌드나 실사용 성능의 증거가 아닙니다.

## 내용 검증과 범위

공식 README와 실행 명세를 대조해 최근 30일의 커뮤니티 자료 조사, 출처를 동반한 정리,
Claude Code 설치 안내와 `/last30days <주제>` 사용 방식을 확인했습니다.
X, YouTube 등은 소스별 인증·도구·추가 서비스와 비용 조건에 영향을 받습니다.
일반 채팅창에 명령어만 입력하면 동작한다고 소개하지 않았습니다.

영상의 PPT 비교 요청은 사용법 설명을 위해 만든 입력 예시입니다. 도구를 설치하거나
실제로 그 요청을 실행한 결과를 보여주는 장면이 아닙니다. 직접 사용한 후기나 시간 절감 수치를 만들지 않았습니다.
X 원문 게시물의 실시간 반응량은 확보하지 못했으므로 X에서의 유행 정도도 수치화하지 않았습니다.

참고한 원문: [README](https://github.com/mvanhorn/last30days-skill/blob/main/README.md),
[실행 명세](https://github.com/mvanhorn/last30days-skill/blob/main/skills/last30days/SKILL.md),
[연결 조건](https://github.com/mvanhorn/last30days-skill/blob/main/CONFIGURATION.md).



이 문서는 샘플 당시 확인 범위다. 다음 제작 시 재확인한다.
