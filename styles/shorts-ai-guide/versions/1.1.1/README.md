# 시각 안내형 1.1.1

1.1.0의 승인된 색상·글꼴·영역·무효과음·날짜/회차 숨김 기준을 유지한다. 편별 하드코딩 대신 9개 재사용 블록과 `visual_data`를 입력한다. 코드 경로는 studio/renderer/src/template/ShortsGuideTemplate.tsx다.

블록: flow, files, prompt, commands, browser, table, slides, image, check. scripts/visual_brief.py가 글자 수·행 수·데이터 구조·스타일 덮어쓰기를 검사한다. 표·검색·슬라이드는 설명용 자료이며 실제 서비스 조작으로 둔갑시키지 않는다.

새 편 생성 양식과 준비·음성·자막·렌더·검수·보관 명령은 studio/SHORTS-WORKFLOW.md를 따른다. 고정 음성이 없으면 최종 준비를 막는다. 명시적인 무음 미리보기에는 화면 표시와 PREVIEW 파일명 규칙을 적용한다.
