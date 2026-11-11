from common import *
brief={"brand":"issues","line":"ch-issues","format_length":"quick","series":"이슈의 구조",
 "desire":"수능을 앞둔 가족·학생이 'AI 안경'이 뭔지, 정말 막을 수 있는지, 괜히 오해받지는 않을지 알고 싶다",
 "trigger":"2026-10-29 교육부 '수능 스마트안경 부정행위 대응 계획' + 11월 수능(19일)을 앞둔 현장 불안 보도",
 "why_now":"수능 8일 전 — 전담 인력 배치·처벌 강화가 확정됐고, 수험생·감독관 불안이 커지는 시점",
 "viewer_question":"AI 안경 컨닝, 수능에서 정말 막을 수 있을까?","question_type":"영향","mood":["긴장","실용"],
 "topic":"AI 스마트안경 부정행위 우려 → 교육부 대책(반입 금지·전담 인력·형사 고발·응시 제한 강화 추진) → 현장의 두 걱정(식별 어려움 vs 일반 안경 오해)",
 "our_angle":"'막는다'는 발표와 '구별이 어렵다'는 현장을 같은 무게로 놓고, 수험생이 실제로 알아야 할 것만 정리",
 "driver":{"type":"각도","why":"docs/18: 교육·입시는 소재만으로 약한 편 → 생활 체감 각도(내 아이 시험장)로 띄움","angle":"생활 체감"},
 "as_of":"2026-11-11 09:00 KST",
 "sides":[{"who":"교육부","claim":"스마트안경 부정행위는 형사 고발·수사 의뢰, 응시자격 정지 1년→3년 추진, 시험장마다 전담 인력 1명","source":"https://supple.kr/news/cmvsvyrru4af2m5vuhof0q8gl"},
          {"who":"현장 교원·수험생","claim":"교원 82% '현행 감독 절차로 식별 어렵다'(교원단체 설문), 뿔테 수험생은 일반 안경 오인 걱정","source":"https://www.khan.co.kr/article/202610271701001"}],
 "unknowns":["시험장에서 '의심되는 안경'을 어떤 기준으로 판단할지 세부 매뉴얼","응시 제한 3년 상향은 법 개정이 필요해 올해 수능에 적용되는지","전파 탐지기는 내년 보급 '검토' 단계"],
 "score":{"desire":3,"clarity":3,"timeliness":3,"demand":2,"visuals":2,"angle":2},
 "demand_evidence":[{"kind":"news","detail":"11월 6~11일 주요 언론 10곳 이상 'AI 안경 수능' 보도 (Google 뉴스)","url":"https://news.google.com/search?q=%EC%88%98%EB%8A%A5%20AI%20%EC%95%88%EA%B2%BD"}],
 "visual_sources":["NASA 서울 야경(퍼블릭 도메인)","직접 그린 대책·흐름 도식"],
 "candidates":[{"topic":"AI 안경 컨닝, 수능에서 막을 수 있을까","total":16,"why_not":"선택"},{"topic":"미 하원 국방장관 탄핵소추안","total":11,"why_not":"국내 체감 낮음·정치 편향 위험"},{"topic":"분당 연쇄 추돌 사고","total":9,"why_not":"사건·사고는 소재 약함, 원인 미확인"}]}
fact="""# 팩트시트 — AI 안경 수능 부정행위 (2026-11-11 09:00 기준)

| # | 사실 | 상태 | 출처 |
|---|---|---|---|
| F1 | 2027학년도 수능은 11월 19일 | ✅ | 전자신문 2026-11-07 https://m.etnews.com/20261107000027 |
| F2 | 교육부 10월 29일 '수능 스마트안경 활용 부정행위 대응 계획' 발표: 형사 고발·수사 의뢰(위계에 의한 공무집행방해·업무방해) | ✅ | 연합뉴스 (서플 전재) https://supple.kr/news/cmvsvyrru4af2m5vuhof0q8gl |
| F3 | 응시자격 정지 1년(현행 고등교육법) → 3년 상향 '추진' (법 개정 필요) | ⚠️ 추진 단계 | 같은 기사 |
| F4 | 전국 1,312개 시험장마다 판별 전담 인력 1명 (총 1,312명), 평가원·교육청 상황실 연결 | ✅ | 같은 기사 |
| F5 | 평가원 10월 15일 수험생 유의사항: 스마트안경을 제출하지 않고 시험 중 착용만 해도 당해 시험 무효 + 다음 해 응시자격 정지(수능 관리규정 제19조), 단순 소지도 무효, 감독관 확인 요구 거부는 중대 부정행위로 제재 가능 | ✅ | 연합뉴스 2026-10-15 (서플 전재) https://supple.kr/news/cmv93ss5q003zzab4cm59ir0d |
| F5-2 | 교육부 10월 29일 계획 교차 확인 (형사 고발·3년 추진·전담 1,312명·2005년 사례) | ✅ | 한국경제 https://www.hankyung.com/article/202610292755Y |
| F6 | 시험장용 전파 탐지기: 내년부터 보급 '검토' | ⚠️ 검토 | 같은 기사 |
| F7 | 10월 대입 논술에서 스마트안경 적발: 연세대(10일)·서울시립대(3일) | ✅ | 같은 기사 |
| F8 | 2005년 휴대전화 조직적 정답 송수신 사건 — 징역 8개월·집행유예 2년 | ✅ | 같은 기사 |
| F9 | 교원 82% '현행 감독 절차로 식별 어렵다' (교원단체 설문), 전교조 '전문 탐지·판별 체계' 촉구 | ✅ | 경향신문 2026-10-27 https://www.khan.co.kr/article/202610271701001 |
| F10 | 뿔테 수험생 '일반 안경 오인' 걱정, 일부는 금속테·렌즈 준비 / 감독관 '민원·책임' 부담 | ✅ | 전자신문 https://m.etnews.com/20261107000027 |

## 쓰지 않는 것
- 'AI 안경으로 수학 만점' 같은 체험 기사 결과(조건이 제각각) — 단정 금지
- 특정 제품·브랜드 이름
"""
spec={"title":"AI 안경 컨닝, 수능에서 정말 막을 수 있을까?",
 "core_message":"수능은 AI 안경을 '쓰기만 해도' 무효로 막기로 했지만, 겉으로 구별하기 어렵다는 현장의 걱정도 그대로다 — 수험생은 '의심받지 않는 준비'가 가장 확실하다.",
 "question":"AI 안경 컨닝, 수능에서 정말 막을 수 있을까?",
 "logic":["AI 기능 스마트안경이 대입 논술에서 실제로 적발","교육부: 반입 금지 + 착용만 해도 무효 + 형사 고발 + 전담 인력","현장: 겉으로 구별이 어렵다(교원 82%), 일반 안경 오해 걱정","남은 것: 판단 기준 매뉴얼·탐지기는 아직"],
 "compare_to":[{"value":"전담 인력 1,312명","to":"전국 수능 시험장 1,312곳 — 한 곳에 한 명"},{"value":"응시 정지 3년 추진","to":"현행 1년"}],
 "analogies":[{"a":"AI 안경","b":"귀에 숨긴 무전기 대신, 안경테에 숨은 카메라와 이어폰"},{"a":"전담 인력 1명","b":"한 학교 전체를 지키는 경비원 한 명"}],
 "past_cases":[{"case":"2005년 휴대전화 정답 송수신 사건 — 징역 8개월·집행유예 2년","lesson":"새 기기가 나올 때마다 규칙이 뒤따라 바뀌었다"}],
 "glossary":[{"term":"스마트안경","plain":"카메라·마이크·스피커가 들어 있어 사진을 찍고 AI 에게 묻고 답을 들을 수 있는 안경"},
             {"term":"응시자격 정지","plain":"정해진 기간 동안 수능을 볼 수 없게 하는 것"},{"term":"위계에 의한 공무집행방해","plain":"속임수로 나라의 공적인 일을 방해한 죄"}],
 "scenes":[]}
S=spec["scenes"]; s=S.append
s(dict(type="intro",chapter=0,series="이슈의 구조",as_of="11월 11일 기준",bg_src="seoul",title_lines=["AI 안경 컨닝,","수능에서 막을 수 있을까?"],agenda_beat=2,
  layers=[{"kind":"photo","src":"seoul","beat":1,"side":"right","w":600,"top":250,"caption":"서울 야경 · NASA ISS (2022)"}],
  beats=B("안녕하세요. 복잡한 뉴스를 한 장의 구조로 풀어 드리는, 이슈의 구조입니다.",
          "오늘은 수능을 8일 앞두고 걱정이 커진 'AI 안경' 이야기입니다. 안경인데, 사진을 찍고 AI 에게 답을 물을 수 있다고 하거든요.",
          "이런 순서로 보겠습니다. 무슨 일이 있었는지, 정부는 어떻게 막겠다는지, 그리고 현장의 걱정은 무엇인지요.",
          "끝까지 보시면 수험생이 시험장에서 뭘 조심하면 되는지 바로 아실 거예요. 시작하겠습니다.")))
s(dict(type="card_type",chapter=0,lines=["안경을 썼을 뿐인데,","시험이 무효?"],bg="photo",bg_src="seoul2",layers=[{"kind":"locator","at":[126.98,37.57],"label":"대한민국 · 수능 11월 19일","beat":0,"side":"right","top":640,"scale":2.2}],beats=B("안경을 썼을 뿐인데 시험이 무효가 될 수 있다? 올해 수능 수험생 유의사항에 실제로 들어간 내용입니다.")))
s(dict(type="chapter",chapter=1,num="1",title="무슨 일이 있었나",icon="search",beats=B("첫 번째, 무슨 일이 있었을까요?")))
s(dict(type="timeline",chapter=1,label="연합뉴스·전자신문 보도",title="2026년, AI 안경과 시험장",years=["7월","10월 초","10월 29일","11월 19일"],
  events=[{"at":"7월","label":"반입 금지 명시","sub":"착용만 해도 무효"},{"at":"10월 초","label":"대입 논술에서 적발","sub":"서울시립대·연세대"},
          {"at":"10월 29일","label":"교육부 대응 계획","sub":"형사 고발·전담 인력"},{"at":"11월 19일","label":"2027학년도 수능","sub":""}],
  beats=[{"say":"시작은 지난 7월입니다. 교육당국이 수능 반입 금지 물품에 스마트안경을 처음 적어 넣었습니다.","upto":1},
         {"say":"그런데 10월, 대학별 논술 시험장에서 실제로 스마트안경을 쓴 수험생이 잇달아 적발됐습니다.","upto":2},
         {"say":"그러자 교육부가 10월 29일 대응 계획을 내놨고, 이제 11월 19일 수능을 앞두고 있습니다.","upto":4}]))
s(dict(type="analogy",chapter=1,label="자체 정리",title="예전의 무전기, 지금의 안경",
  left={"icon":"phone","label":"예전 부정행위","sub":"숨긴 휴대전화·무전기"},right={"icon":"camera","label":"AI 안경","sub":"안경테 속 카메라·마이크·스피커"},
  result={"icon":"eye","label":"겉으로는 그냥 안경처럼 보인다"},fx=["tilt"],
  beats=[{"say":"예전 부정행위가 귀에 숨긴 무전기였다면, AI 안경은 그 장비를 안경테 안에 넣은 셈입니다."},
         {"say":"문제는 겉으로는 그냥 안경처럼 보인다는 거죠. 그래서 막기가 어렵습니다.","show_result":True}]))
s(dict(type="recap",chapter=1,title="여기까지 정리",items=["AI 안경은 이미 대입 시험장에서 적발됐다"],new_from=0,
  layers=[{"kind":"photo","src":"seoul","beat":0,"side":"right","w":460,"top":560,"caption":"서울 · NASA ISS"}],
  beats=B("정리하면, AI 안경은 걱정이 아니라 이미 시험장에서 적발된 현실입니다.")))
s(dict(type="chapter",chapter=2,num="2",title="정부는 어떻게 막나",icon="shield-alert",beats=B("여기까지가 무슨 일이 있었는지였고요. 두 번째, 정부는 어떻게 막겠다는 걸까요?")))
s(dict(type="checklist",chapter=2,label="교육부 10월 29일 대응 계획 (연합뉴스 보도)",title="수능 AI 안경, 네 겹의 대책",fx=["scan"],
  rows=[{"label":"반입 금지 — 시험 중 착용만 해도 그 시험 무효","state":"yes"},{"label":"응시자격 정지 — 현행 1년, 3년으로 늘리는 방안 추진","state":"warn"},
        {"label":"형사 고발·수사 의뢰","state":"yes"},{"label":"시험장마다 판별 전담 인력 1명","state":"yes"}],
  beats=[{"say":"대책은 네 겹입니다. 먼저, 시험 중에 쓰고만 있어도 그 시험은 무효가 됩니다.","upto":1},
         {"say":"다음 해 수능도 볼 수 없는데, 이 기간을 1년에서 3년으로 늘리는 방안도 추진 중입니다. 다만 법을 고쳐야 하는 일이라 아직 확정은 아닙니다.","upto":2},
         {"say":"그리고 형사 고발까지 하고, 시험장마다 판별을 맡는 사람을 한 명씩 둡니다.","upto":4}]))
s(dict(type="isotype",chapter=2,label="교육부 대응 계획 (연합뉴스 보도)",title="전국 수능 시험장",icon="school",total=10,lost=0,before="시험장 1,312곳",after="전담 인력도 1,312명 — 한 곳에 한 명",
  layers=[{"kind":"locator","at":[126.98,37.57],"label":"서울","beat":0,"side":"right","top":110,"scale":1.7}],
  beats=B("전국 수능 시험장은 1,312곳. 전담 인력도 1,312명이니, 학교 한 곳에 한 명씩인 셈이죠.","학교 전체를 경비원 한 명이 지키는 것과 비슷합니다. 그래서 감독관 한 사람 한 사람의 눈도 여전히 중요합니다.")))
s(dict(type="bignum",chapter=2,label="연합뉴스 보도 (2005년 사건)",value="2005",small="휴대전화로 정답을 주고받은 부정행위 사건",compare={"label":"선고","value":"징역 8개월·집행유예 2년"},fx=["photofill"],fill_src="seoul2",
  beats=[{"say":"처벌이 말뿐일까요? 2005년, 휴대전화로 정답을 주고받은 사건에서는 실제로 징역형이 선고됐습니다."},
         {"say":"징역 8개월에 집행유예 2년. 새 기기가 나올 때마다 규칙도 뒤따라 바뀌어 왔습니다.","show_compare":True}]))
s(dict(type="chapter",chapter=3,num="3",title="현장의 두 가지 걱정",icon="users",beats=B("그럼 이제 막을 수 있을까요? 현장의 목소리는 조금 다릅니다.")))
s(dict(type="quote",chapter=3,label="경향신문 2026.10.27 보도",who="교원단체 설문",role="교사 응답 82%",quote="현행 감독 절차로는 스마트안경을 식별하기 어렵다.",keyword="식별하기 어렵다",note="걱정 ①",fx=["dust"],
  beats=[{"say":"첫 번째 걱정은 감독하는 쪽입니다. 교원단체 설문에서 교사 82%가 지금 절차로는 구별이 어렵다고 답했습니다."},
         {"say":"물어보면 민원이 걱정되고, 놓치면 책임이 걱정된다는 거죠.","mark":True}]))
s(dict(type="quote",chapter=3,label="전자신문 2026.11.7 보도",who="수험생 커뮤니티 글",role="평소 검정 뿔테를 쓰는 수험생",quote="스마트안경으로 오해받아 안경을 가져가 버리면 어떡하나요.",keyword="오해받아",note="걱정 ②",fx=["dust"],
  beats=[{"say":"두 번째 걱정은 수험생 쪽입니다. 도수가 높아 두꺼운 뿔테를 쓰는 수험생은 일반 안경을 오해받을까 걱정합니다."},
         {"say":"그래서 금속테 안경이나 콘택트렌즈를 따로 준비하는 수험생도 있다고 합니다.","mark":True}]))
s(dict(type="map_causal",chapter=3,label="이 영상 팩트시트 F1~F10 정리",fx=["tilt"],
  beats=[{"say":"한 장으로 보면 이렇습니다. AI 안경이 나오자 정부는 금지와 처벌을 세게 했습니다.","reveal":["glass","rule","punish"],"draw":[["glass","rule"],["rule","punish"]],"active":"rule"},
         {"say":"그런데 겉으로 구별이 어렵다 보니, 감독관은 부담을, 수험생은 오해를 걱정하게 됐습니다.","reveal":["hard","teacher","student"],"draw":[["glass","hard"],["hard","teacher"],["hard","student"]],"active":"hard"}]))
s(dict(type="chapter",chapter=4,num="4",title="수험생이 알아 둘 것",icon="graduation-cap",beats=B("마지막으로, 그래서 수험생은 무엇을 알아 두면 될까요?")))
s(dict(type="checklist",chapter=4,label="11월 11일 기준",title="시험장에서 알아 둘 것",
  rows=[{"label":"스마트안경·전자기기는 아예 가져가지 않기","state":"yes"},{"label":"감독관의 안경 확인 요청에는 꼭 응하기 (거부하면 중대 부정행위)","state":"yes"},
        {"label":"아직 모르는 것: 의심 안경 판단 세부 기준 · 3년 정지 적용 시기","state":"no"}],
  beats=[{"say":"첫째, 스마트안경이나 전자기기는 아예 가져가지 않는 게 가장 확실합니다. 둘째, 감독관이 안경 확인을 요청하면 꼭 응하세요. 거부하면 그 자체로 중대한 부정행위가 될 수 있거든요.","upto":2},
         {"say":"아직 확인되지 않은 것도 있습니다. 의심되는 안경을 어떤 기준으로 판단할지, 3년 정지가 언제부터인지는 더 지켜봐야 합니다.","upto":3}]))
s(dict(type="kinetic",chapter=4,beats=[{"say":"막는 규칙은 세졌지만, 가장 확실한 방법은 의심받지 않는 준비입니다.","hit":["의심받지","준비입니다."]}]))
s(dict(type="outro",chapter=4,title="이슈의 구조",sub="11월 11일 기준 · 출처는 설명란에",clip={"src":"seoul","start":0},beats=B("오늘 이슈의 구조는 여기까지입니다. 수험생 여러분, 모두 좋은 결과 있기를 바랍니다.")))
spec["map"]={"nodes":{"glass":{"label":"AI 스마트안경 등장","icon":"camera","x":250,"y":400},"rule":{"label":"반입 금지·착용만 해도 무효","icon":"ban","x":800,"y":400},
  "punish":{"label":"형사 고발·응시 제한","icon":"gavel","x":1450,"y":400},"hard":{"label":"겉으로 구별 어려움","icon":"eye","x":550,"y":720},
  "teacher":{"label":"감독관: 민원·책임 부담","icon":"users","x":1100,"y":720},"student":{"label":"수험생: 일반 안경 오해 걱정","icon":"user","x":1600,"y":720}},
  "edges":[["glass","rule"],["rule","punish"],["glass","hard"],["hard","teacher"],["hard","student"]]}
spec["package"]={"title":"AI 안경 컨닝, 수능에서 정말 막을 수 있을까? | 착용만 해도 무효","title_options":["AI 안경 컨닝, 수능에서 정말 막을 수 있을까? | 착용만 해도 무효","수능 8일 전, 'AI 안경' 때문에 바뀐 것 정리","안경 썼을 뿐인데 시험 무효? 수능 AI 안경 대책의 구조"],
 "title_why":["질문형(왜·이유 1.29배 계열) + 생활 체감","'정리' 1.30배","반전형 첫 문장"],
 "thumbnails":[{"id":"A","name":"서울 야경 + 질문","layout":"photo","photo_side":"full","image":{"file":"04_assets/footage/raw/seoul.jpg","focus":[0.5,0.5]},"top":"수능 D-8 · 11월 11일 기준","lines":["AI 안경 컨닝,","막을 수 있을까"],"hl":["막을 수"],"sub":"착용만 해도 무효","size":140,"text_y":330,"marks":[],"why":["시사 문법: 아래 큰 두 줄 + 노란 강조 하나"]},
  {"id":"B","name":"숫자 대비","layout":"versus","left":{"value":"1,312곳","label":"수능 시험장"},"right":{"value":"1,312명","label":"전담 인력"},"headline":"한 곳에 한 명","hl":[],"marks":[],"why":["숫자 둘로 대책 크기를 바로 보여 줌"]},
  {"id":"C","name":"반전 문장","layout":"photo","photo_side":"full","image":{"file":"04_assets/footage/raw/seoul2.jpg","focus":[0.5,0.5]},"top":"2027학년도 수능","lines":["안경 썼을 뿐인데","시험 무효?"],"hl":["무효?"],"sub":"수험생이 알아 둘 것","size":140,"text_y":330,"marks":[],"why":["첫 문장 반전"]}]}
project("20261111-issues-aiglasses","ch-issues","dark-doc","시사 채널 2편 · AI 안경 수능 부정행위 — manual v11",{"seoul":"iss066e158841","seoul2":"iss037e005370"},brief,fact,spec)
