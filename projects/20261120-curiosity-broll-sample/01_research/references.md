# 실사 B-roll + 모션그래픽 레퍼런스 조사 (2026-11-20)

요청 (2026-11-20 사용자): 잼·기억 편처럼 삽화로 끌고 가는 대신, **사람이 나오는 짧은 실사 영상과 모션그래픽으로 설명**합니다. 자료를 구하기 어렵거나 넣기 힘든 장면에만 **삽화를 부분적으로** 씁니다.

**확인 방법:** YouTube 검색 결과로 제목·URL·채널을 확인했습니다. 화면은 공개 자동 프레임(영상 25·50·75% 지점, `i.ytimg.com` hq1~3)을 영상마다 3장씩 봤습니다. watch 페이지는 봇 확인에 막혀 우회하지 않았습니다. 그래서 **비율은 추정치**이고, 컷 리듬·슬로모션·매치 컷처럼 움직임으로만 알 수 있는 것은 **미확인**입니다. 움직임 분석이 필요하면 PC 에서 `skills/ref-watch-ego` 로 봅니다.

## 1. 잘 맞는 레퍼런스 (실사 중심)

| 채널 | 예시 영상 | 실사 : 그래픽 : 삽화 (추정) | 화면에서 확인한 것 | 가져올 것 |
|---|---|---|---|---|
| **EBS 지식채널e** | [걸으면 집중이 되살아나는 데에는 이유가 있다](https://www.youtube.com/watch?v=BSApOCxaSyg) · [나를 사랑하는, 가장 쉬운 방법](https://www.youtube.com/watch?v=-Z51loHlJgk) | 85 : 15 : 0 | 걷는 군중, 혼자 걷는 사람, 아기 손 같은 일상 실사 위 가운데에 흰 글자 2~3줄을 얹고 핵심어만 굵게 씀. 가장자리는 어둡게(비네트) 처리하고 채도는 낮춤 | **가장 가까운 원형.** 문장 하나에 일상 컷 하나를 깔고, 핵심어는 화면 가운데 타이포로 |
| **Aperture** | [The Psychology of People Who Never Feel Good Enough](https://www.youtube.com/watch?v=DMtN9yJwc3w) · [Absurdism: Life is Meaningless](https://www.youtube.com/watch?v=GBoHxeCQHRE) | 75 : 5 : 0 (진행자 약 20) | 시네마틱 스톡 인물 장면(표정 클로즈업, 지하철의 헤드폰 쓴 사람). 위아래 띠를 둔 와이드 화면, 어두운 색보정 | 감정 단어 하나에 표정 컷 하나. **한 가지 색보정으로 통일**해 서로 무관한 클립을 한 영상으로 묶음 |
| **북툰** | [The Surprising Healing Power of Art…](https://www.youtube.com/watch?v=t0HYJOVView) | 70 : 25 : 5 | 스톡 인물 위에 **동그라미 라벨 콜아웃**("노래 집단", "놀이 집단")과 체크 아이콘, 4분할 비교 화면, 하단 자막 | 실사 위 UI 라벨·분할 비교. 한국어 심리·과학 채널이라 형식이 가장 비슷함 |
| **BBC Reel** | [Why you're not stuck with the brain you're born with](https://www.youtube.com/watch?v=OpFHhOG3pao) | 80 : 20 : 0 | 일상 스톡(빵 반죽하는 아이, 실내 자전거)에 3D 그래픽 합성 | 실사 속 사물에서 그래픽이 생겨나는 합성. 편마다 형식이 다름([Dunning-Kruger 편](https://www.youtube.com/watch?v=JTRQ8iyga6Q)은 인터뷰 중심) |
| **스브스뉴스** | [근데 폰 꺼놓으면 안 울리는 거 아니에요?](https://www.youtube.com/watch?v=yKLDfi2l03E) | 70 : 30 : 0 | 거리에서 찍은 일반인 **얼굴을 블러 처리**, 큰 하단 자막, 문서 캡처 카드, 좌상단 장 꼬리표 | 알아볼 수 있는 일반인은 블러로 가리고, 장 꼬리표로 진행 위치를 표시 |
| **비디오머그** | [메타버스 법당에 사람들이 모여드는 이유](https://www.youtube.com/watch?v=JH5TUbDqFiA) | 60 : 35 : 5 | 실사(하단에 출처)와 질감 배경 위 장 제목 타이포 카드를 번갈아 씀 | 장 전환 타이포 카드, 하단 출처 한 줄 |
| **PolyMatter** | [Why This is the World's Pirate Capital](https://www.youtube.com/watch?v=OMnJ24XG5Gc) | 프레임 3장 모두 실사 (그래픽 비율 미확인) | 항공 촬영 화물선, 깃발, 시추선 같은 장소·사물 실사 | 장소와 사물 B-roll 로 맥락 깔기 |
| **14F 일사에프** | [세계가 원조를 줄이는 지금…](https://www.youtube.com/watch?v=Mv1Y2_lA-pQ) | 진행자 60 : 실사 30 : 그래픽 10 | 진행자 사이에 스톡 실사, 하단 자막, 질문 카드 | 질문 카드 디자인만 참고 |

## 2. 기법 하나만 빌릴 곳

| 채널 | 예시 | 확인한 것 | 빌릴 것 |
|---|---|---|---|
| Pursuit of Wonder | [Cosmic Insignificance Theory](https://www.youtube.com/watch?v=tGYMrBOPQVI) | 실사 B-roll 이 아니라 스톡 사진을 오려 붙인 초현실 콜라주 | 삽화 전 단계의 대체 수단: 스톡 인물 콜라주 |
| Academy of Ideas | [Pursue Pain, Not Pleasure](https://www.youtube.com/watch?v=UNIx3GcYh1g) | 스톡·정지 이미지와 텍스트 카드 | 영상이 없을 때 정지 사진에 천천히 다가가기 |
| Vox | [Why the Myers-Briggs test is totally meaningless](https://www.youtube.com/watch?v=Q5pggDCnt5M) | 직접 촬영한 인물, 방송 자료 화면 | 실험을 연기로 재현하는 연출(스톡과는 다른 길) |
| 김지윤의 지식Play | [Immigrants and Refugees…](https://www.youtube.com/watch?v=4kPO2LIlOnc) | 진행자와 보도사진 | 사진 하단 출처 표기 |

**맞지 않음(프레임으로 확인):** 사물궁이([예](https://www.youtube.com/watch?v=U8EwFZykjGI), 전부 삽화) · 지식해적단(삽화·콜라주) · The School of Life(플랫 삽화) · Einzelgänger(명화·삽화) · Better Ideas, CNBC Make It(진행자형) · Johnny Harris([이번 편](https://www.youtube.com/watch?v=20CgG5pUv9Q)은 현장 진행, 지도 연출은 미확인) · LEMMiNO(자체 그래픽). 닥터프렌즈는 미확인.

## 3. 공통으로 쓸 기법 → 예시 영상에 적용한 것

| 기법 | 레퍼런스 | 예시 영상(`broll_v1`)에서 |
|---|---|---|
| 문장 하나에 일상 컷 하나, 핵심어만 화면 가운데 | 지식채널e | 3번 "많을수록 / 좋을까?", 7번 "선택 과부하", 끝 문장 |
| 모든 클립을 한 색보정으로 통일 | Aperture, 지식채널e | 채도 0.82·따뜻한 중간톤·비네트·옅은 필름 입자를 모든 클립에 같은 값으로 |
| 실사 위 UI 콜아웃 | 북툰 | 1번 인물에 모서리 괄호 + "고르는 중" + 초 세기, 8번 상품 목록 타일이 흘러가다 ✕ |
| 실사를 깔고 그 위에 데이터 | BBC Reel, 북툰 | 5번 지나가는 손님 위로 60%·40% 막대, 9번 흐린 군중 위로 메타분석 축 |
| 데이터만 보여 줄 때는 실사를 걷어냄 | — | 6번 100명 점 그림(3명 vs 30명) |
| 대체 수단의 순서: 실사 → 정지 사진 → 콜라주 → 삽화 | Academy of Ideas, Pursuit of Wonder | 4번 1990년대 실험 현장만 **재구성 삽화**(당시 영상 없음) |
| 같은 상황의 다른 사람·장소일 때 표시 | 스브스뉴스(블러), manual/12 §1 | 5번 "자료 화면 · 실험 장소 아님", 4번 "재구성 삽화" |

## 4. 무료 스톡 영상 소스

| 소스 | 유튜브 상업 사용 | 출처 표기 | 키 | 인물 관련 제한 |
|---|---|---|---|---|
| **Mixkit** ([License](https://mixkit.co/license/)) | 클립이 Free 라이선스면 가능 (Restricted 는 비상업만) | 필요 없음 | 없이 내려받기 가능 (이번 예시에 사용) | 본문이 팝업이라 인물 조항 **미확인** — 사람이 라이선스 창에서 확인 |
| **Pexels** ([License](https://www.pexels.com/license/), [ToS](https://pexels.com/terms-of-service)) | 가능 | 필요 없음 (API 표시 시 링크) | API 키 필요 (새 키 발급 여부 미확인) | 약관 5조: 알아볼 수 있는 사람을 **신체·정신 질환을 앓는 것처럼** 묘사 금지, 정치·약물·명예훼손·보증 암시 금지 |
| **Pixabay** ([요약](https://pixabay.com/service/license-summary/)) | 가능 | 필요 없음 | 무료 키 필요 | 알아볼 수 있는 사람이 나오는 부도덕·불법·오해를 부르는 사용 금지 |
| **Coverr** ([License](https://coverr.co/license)) | 가능 | 필요 없음 | API 키 필요 | **AI 생성 인물 클립이 섞여 있음** → 실제 사건처럼 쓰지 말 것. Content ID 등록 금지 |
| Videvo / Wikimedia Commons | 클립마다 다름 | CC-BY 는 필요 | — | Videvo "Editorial Use Only" 는 상업 금지 |

**심리 채널 규칙 제안:** 우울·불안·중독·외로움을 말하는 문장 밑에 **얼굴이 보이는 스톡 인물을 '환자'처럼 쓰지 않습니다**(Pexels 약관 5조). 이런 장면은 뒷모습·실루엣·손·흐린 군중이나 블러를 쓰고, 맞는 컷이 없으면 삽화로 대체합니다. 클립마다 출처·라이선스·내려받은 날짜를 `04_assets/clips.md` 에 남깁니다.
