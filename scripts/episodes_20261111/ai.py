from common import *
brief={"brand":"ai","line":"ch-ai-guide",
 "desire":"AI 를 잘 쓰는 것만큼, AI 업계가 지금 어디로 가는지(돈·신뢰) 남보다 먼저 알고 싶다",
 "trigger":"2026-11-10 앤트로픽 상장 공모 로드쇼 시작 (최대 약 640억 달러) + 같은 날 엔비디아 CEO 관련 외부 조사팀 선임",
 "why_now":"AI 업계 '돈'과 '신뢰' 두 큰 소식이 같은 날 — 이용자에게 무엇이 바뀌는지 정리할 시점",
 "viewer_question":"이번 주 AI 업계, 나랑 상관있는 소식은?","question_type":"영향","mood":["미래","실용"],
 "topic":"이번 주 AI 업계 두 소식: ① 앤트로픽 상장 공모(역대 두 번째 규모 가능) — AI는 왜 이렇게 큰돈이 필요한가 ② 엔비디아 CEO 사태 — AI 칩 공급의 신뢰 문제 → 이용자에게 바뀌는 것",
 "our_angle":"업계 뉴스를 '이용자에게 무엇이 바뀌나'로 번역: 상장하면 AI 회사의 숫자·위험을 누구나 볼 수 있게 된다",
 "driver":{"type":"각도","why":"AI·빅테크 소재만으로는 약함(docs/18 0.83) → '돈의 크기 비교'와 '나에게 바뀌는 것' 각도","angle":"생활 체감"},
 "score":{"desire":3,"clarity":2,"timeliness":3,"demand":3,"visuals":2,"angle":2},
 "demand_evidence":[{"kind":"news","detail":"11월 10일 앤트로픽 상장 공모·엔비디아 사태 — 뉴욕타임스·악시오스·로이터·CNBC 등 상위 보도","url":"https://news.google.com/search?q=Anthropic%20IPO"}],
 "visual_sources":["NASA 슈퍼컴퓨터·야경 사진(퍼블릭 도메인)","직접 그린 비교 도식"],
 "candidates":[{"topic":"이번 주 AI 업계: 돈과 신뢰","total":15,"why_not":"선택"},{"topic":"OpenAI·업워크 프리랜서 연구","total":12,"why_not":"원문(openai.com) 자동 접근 차단 → 2차 출처만"},{"topic":"뉴욕 AI 안전법","total":11,"why_not":"시행일 보도가 엇갈림(법률 자문사는 2027.1.1)"}]}
fact="""# 팩트시트 — 이번 주 AI 업계: 돈과 신뢰 (2026-11-11 확인)

| # | 사실 | 상태 | 출처 |
|---|---|---|---|
| F1 | 2026-11-10 앤트로픽 상장 공모 로드쇼 시작: 클래스 A 8억 2,500만 주(회사 8억 135만 + 기존 주주 2,365만), 공모가 희망 범위 주당 70~78달러, 나스닥 'ANT' | ✅ | Anthropic https://www.anthropic.com/news/roadshow-launch |
| F2 | 계산: 8억 2,500만 주 × 78달러 = 약 644억 달러 (기본 물량·가격 상단) — 추가 배정 옵션 1억 2,375만 주는 제외 | ✅ 계산 | F1 |
| F3 | 6월 1일 비공개 상장 신청 → 10월 26일 S-1 공개 제출 | ✅ | Anthropic https://www.anthropic.com/news/s1-sec |
| F4 | 역대 IPO 규모: SpaceX 2026년 857억 달러, 사우디 아람코 2019년 294억 달러(추가 배정 포함) | ✅ | Wikipedia 'Initial public offering' 표 https://en.wikipedia.org/wiki/Initial_public_offering |
| F5 | 엔비디아: 11월 8일 이사회 독립 조사(CEO 관련 안보 의혹 보도), 11월 10일 외부 조사팀 선임, 이사회 "국가안보·회사 기밀이 침해됐다고 볼 이유는 없다" | ✅ | 엔비디아 https://nvidianews.nvidia.com/news/statement-from-the-independent-members-of-the-nvidia-board · AP(PBS) https://www.pbs.org/newshour/world/what-we-know-and-what-we-dont-as-nvidia-investigates-an-alleged-spy-plot-involving-its-ceo |
| F6 | 보도: 관련 인물이 일했던 회사가 엔비디아 칩 48억 달러어치 구매, 미 상무부가 수출 규제 우회 의혹 조사 (엔비디아는 당시 위법 없음이라고 밝힘) | ⚠️ 보도 | AP(PBS) https://www.pbs.org/newshour/world/nvidia-and-huang-face-lawsuit-alleging-investors-were-misled-about-spy-affair |

## 쓰지 않는 것
- 상장 후 주가·투자 판단 (투자 권유 금지)
- 앤트로픽 기업가치 추정치(보도마다 다름), 매출·손실 숫자(S-1 원문 미확인)
- 엔비디아 사건의 사생활 세부·상대 인물 이름
"""
spec={"title":"이번 주 AI 업계: 돈과 신뢰",
 "core_message":"AI 회사는 칩과 전기를 사느라 사상 손꼽히는 큰돈을 주식시장에서 구하고 있고, 그 칩의 공급망에는 신뢰 문제가 생겼다 — 이용자에게는 'AI 회사의 숫자를 볼 수 있게 되는 것'이 첫 변화다.",
 "question":"이번 주 AI 업계, 나랑 상관있는 소식은?",
 "logic":["AI 는 칩·전기·데이터센터에 큰돈이 든다","앤트로픽: 최대 약 640억 달러 상장 공모 — 역대 두 번째 규모 가능","엔비디아: AI 칩 1위 회사 CEO 관련 조사 → 칩 공급망 신뢰 문제","이용자에게: 상장 회사는 숫자·위험을 공개해야 한다 → 내가 쓰는 AI 회사를 볼 수 있다"],
 "compare_to":[{"value":"약 644억 달러","to":"아람코 2019년 294억 달러의 두 배 이상"},{"value":"약 644억 달러","to":"역대 1위 SpaceX 2026년 857억 달러"}],
 "analogies":[{"a":"AI 회사의 상장","b":"동네 맛집이 체인점을 내려고 손님들에게 가게 지분을 파는 것"},{"a":"AI 칩","b":"AI 라는 공장의 엔진 — 엔진 회사가 흔들리면 공장도 긴장"}],
 "past_cases":[{"case":"2019년 사우디 아람코 상장 294억 달러 — 당시 역대 최대","lesson":"석유의 시대엔 석유 회사, 지금은 AI 회사가 가장 큰돈을 모은다"}],
 "glossary":[{"term":"상장(IPO)","plain":"회사 주식을 처음으로 누구나 사고팔 수 있게 시장에 내놓는 것"},{"term":"로드쇼","plain":"상장 전에 투자자들을 만나 회사를 설명하는 기간"},{"term":"S-1","plain":"미국에서 상장하려는 회사가 숫자와 위험을 적어 내는 신고서"}],
 "scenes":[]}
S=spec["scenes"]; s=S.append
s(dict(type="intro",chapter=0,series="AI 최전선",as_of="11월 11일 기준",bg_src="pleiades",title_lines=["이번 주 AI 업계,","돈과 신뢰"],agenda_beat=2,
  layers=[{"kind":"photo","src":"pleiades","beat":1,"side":"right","w":600,"top":250,"caption":"슈퍼컴퓨터 · NASA 에임스 (2008)"}],
  beats=B("안녕하세요. AI 업계 최전선 소식을 이용자 눈높이로 풀어 드리는, AI 최전선입니다.",
          "이번 주엔 같은 날 두 가지 큰 뉴스가 나왔거든요. 하나는 돈, 하나는 신뢰 이야기입니다.",
          "이런 순서로 보겠습니다. AI 회사의 사상 손꼽히는 상장, AI 칩 회사의 신뢰 문제, 그리고 우리에게 바뀌는 것까지요.",
          "다 보고 나시면, AI 뉴스를 볼 때 무엇을 봐야 할지 감이 오실 거예요. 시작하겠습니다.")))
s(dict(type="kb",chapter=0,clip={"src":"nyc","start":0},move="in",stamp="미국 뉴욕 · 나스닥",label="자료 사진 · NASA STS-59 (1994, 퍼블릭 도메인)",
  layers=[{"kind":"locator","at":[-74.0,40.71],"label":"나스닥 · 뉴욕","beat":0,"side":"right","top":120,"scale":2.2}],
  beats=B("11월 10일, 챗봇 클로드를 만드는 앤트로픽이 상장을 위한 투자자 설명회, 로드쇼를 시작했습니다.","모으려는 돈은 가격 상단 기준으로 약 640억 달러. 우리 돈으로 수십조 원입니다.")))
s(dict(type="card_type",chapter=0,lines=["AI는 왜","이렇게 큰돈이 필요할까?"],beats=B("AI 회사는 왜 이렇게 큰돈이 필요할까요? 오늘의 첫 질문입니다.")))
s(dict(type="chapter",chapter=1,num="1",title="돈 — AI 회사의 상장",icon="landmark",beats=B("첫 번째, 돈 이야기부터 보겠습니다.")))
s(dict(type="timeline",chapter=1,label="Anthropic 발표 (2026.6.1 · 10.26 · 11.10)",title="앤트로픽 상장까지",bg="photo",bg_src="sf",years=["6월 1일","10월 26일","11월 10일","상장"],
  events=[{"at":"6월 1일","label":"비공개로 상장 신청","sub":""},{"at":"10월 26일","label":"신고서(S-1) 공개","sub":""},{"at":"11월 10일","label":"로드쇼 시작","sub":"주당 70~78달러"},{"at":"상장","label":"나스닥 'ANT'","sub":"예정"}],
  beats=[{"say":"앤트로픽은 6월에 비공개로 상장을 신청했고, 10월에 신고서를 공개했습니다.","upto":2},
         {"say":"그리고 11월 10일, 주당 70에서 78달러로 8억 2,500만 주를 팔겠다며 로드쇼를 시작했습니다. 나스닥 이름은 'ANT'입니다.","upto":4}]))
s(dict(type="bars",chapter=1,label="Wikipedia 'Initial public offering' · Anthropic 발표로 계산",title="역대 상장 공모 규모 (억 달러)",emph=1,
  layers=[{"kind":"locator","at":[-74.0,40.71],"label":"나스닥 · 뉴욕","beat":1,"side":"right","top":130,"scale":1.7}],
  items=[{"label":"SpaceX (2026)","value":857,"text":"857"},{"label":"앤트로픽 (최대)","value":644,"text":"약 644"},{"label":"사우디 아람코 (2019)","value":294,"text":"294"}],
  beats=[{"say":"얼마나 큰지 비교해 보죠. 2019년 석유 회사 사우디 아람코가 294억 달러를 모아 당시 역대 최대였습니다."},
         {"say":"앤트로픽은 최대 약 644억 달러, 아람코의 두 배가 넘습니다. 올해 상장한 SpaceX 다음, 역대 두 번째 규모가 될 수 있습니다."}]))
s(dict(type="analogy",chapter=1,label="자체 정리",title="AI 회사는 왜 큰돈이 필요할까",
  left={"icon":"microchip","label":"AI 칩","sub":"아주 비싼 부품이 아주 많이"},right={"icon":"zap","label":"전기·데이터센터","sub":"엄청난 양의 전력"},
  result={"icon":"landmark","label":"그래서 주식시장에서 돈을 모은다"},
  layers=[{"kind":"photo","src":"pleiades","beat":0,"side":"right","w":330,"top":690,"caption":"슈퍼컴퓨터 · NASA (2008)"}],
  beats=[{"say":"왜 이렇게 큰돈일까요? AI 는 수많은 칩과 그 칩을 돌릴 전기, 데이터센터가 있어야 만들어지기 때문입니다."},
         {"say":"동네 맛집이 체인점을 내려고 손님들에게 가게 지분을 파는 것처럼, AI 회사도 주식시장에서 돈을 모으는 거죠.","show_result":True}]))
s(dict(type="recap",chapter=1,title="여기까지 정리",items=["AI 회사가 역대 손꼽히는 큰돈을 주식시장에서 모으고 있다"],new_from=0,
  beats=B("정리하면, AI 회사가 역대 손꼽히는 큰돈을 주식시장에서 모으고 있습니다.")))
s(dict(type="chapter",chapter=2,num="2",title="신뢰 — AI 칩 회사",icon="microchip",beats=B("두 번째, 같은 날 나온 신뢰 이야기입니다.")))
s(dict(type="kb",chapter=2,clip={"src":"taiwan","start":0},move="out",stamp="대만·일본 일대 · 우주에서 본 모습",label="자료 사진 · NASA ISS (2014, 퍼블릭 도메인)",
  beats=B("AI 칩 1위 회사 엔비디아의 이사회가, CEO 젠슨 황 관련 안보 의혹 보도를 조사하기 시작했습니다. 11월 10일엔 외부 조사팀까지 꾸렸죠.",
          "이사회는 국가안보나 회사 기밀이 침해됐다고 볼 이유는 없다고 밝혔습니다. 주가 이야기는 시장의 이유 채널에서 자세히 다뤘습니다.")))
s(dict(type="map_causal",chapter=2,label="이 영상 팩트시트 F5~F6 정리",fx=["tilt"],
  beats=[{"say":"AI 업계에 이게 왜 중요할까요? 엔비디아 칩은 거의 모든 AI 회사가 쓰는 엔진입니다.","reveal":["chip","ai"],"draw":[["chip","ai"]],"active":"chip"},
         {"say":"그런데 엔비디아 칩이 수출 규제를 피해 중국으로 갔는지 정부가 조사 중이라는 보도가 겹치면서, 칩이 어디로 가는지에 대한 신뢰가 문제로 떠올랐습니다.","reveal":["probe","export","trust"],"draw":[["probe","trust"],["export","trust"],["trust","chip"]],"active":"trust"}]))
s(dict(type="chapter",chapter=3,num="3",title="우리에게 바뀌는 것",icon="user",beats=B("마지막 세 번째, 그래서 우리에게는 무엇이 바뀔까요?")))
s(dict(type="checklist",chapter=3,label="11월 11일 기준 · 투자 권유가 아닙니다",title="이용자에게 바뀌는 것",fx=["scan"],
  rows=[{"label":"당장 서비스 요금·사용법이 바뀐다는 발표는 없다","state":"yes"},{"label":"상장 회사는 매출·손실·위험을 공개해야 한다 → 내가 쓰는 AI 회사를 볼 수 있다","state":"yes"},
        {"label":"AI 칩 공급 소식은 'AI 서비스 가격·속도'로 이어질 수 있는 신호","state":"warn"}],
  beats=[{"say":"먼저, 당장 서비스 요금이나 사용법이 바뀐다는 발표는 없습니다. 대신 상장한 회사는 매출과 손실, 위험을 정기적으로 공개해야 합니다.","upto":2},
         {"say":"그리고 AI 칩 공급 소식은 결국 AI 서비스의 가격과 속도로 이어질 수 있으니, 계속 지켜볼 신호입니다.","upto":3}]))
s(dict(type="kinetic",chapter=3,beats=[{"say":"AI 를 잘 쓰려면, 이제 AI 를 만드는 돈의 흐름도 봐야 합니다.","hit":["돈의","흐름"]}]))
s(dict(type="outro",chapter=3,title="AI 최전선",sub="11월 11일 기준 · 출처는 설명란에",clip={"src":"sf","start":0},beats=B("오늘 AI 최전선은 여기까지입니다. 바로 써먹는 활용법은 쇼츠에서, 업계 소식은 다음 주에 또 찾아오겠습니다.")))
spec["map"]={"nodes":{"chip":{"label":"엔비디아 AI 칩","icon":"microchip","x":350,"y":420},"ai":{"label":"거의 모든 AI 서비스","icon":"bot","x":350,"y":760},
  "probe":{"label":"CEO 관련 이사회 조사","icon":"search","x":1000,"y":300},"export":{"label":"수출 규제 우회 의혹 조사 (보도)","icon":"globe","x":1000,"y":560},
  "trust":{"label":"칩 공급망 신뢰 문제","icon":"circle-alert","x":1600,"y":430}},
  "edges":[["chip","ai"],["probe","trust"],["export","trust"],["trust","chip"]]}
spec["package"]={"title":"이번 주 AI 업계: 돈과 신뢰 | 역대 2위 규모 상장, AI 칩 회사의 조사","title_options":["이번 주 AI 업계: 돈과 신뢰 | 역대 2위 규모 상장, AI 칩 회사의 조사","AI 회사가 640억 달러를 모으는 이유","AI 업계 이번 주 두 소식, 나에게 바뀌는 것"],
 "title_why":["업계 뉴스 정리형","숫자 + 이유 질문","생활 체감"],
 "thumbnails":[{"id":"A","name":"슈퍼컴퓨터 + 두 단어","layout":"photo","photo_side":"full","image":{"file":"04_assets/footage/raw/pleiades.jpg","focus":[0.5,0.5]},"top":"AI 최전선 · 이번 주","lines":["AI 업계,","돈과 신뢰"],"hl":["신뢰"],"sub":"11월 11일 기준","size":140,"text_y":330,"marks":[],"why":["두 단어로 요약"]},
  {"id":"B","name":"규모 비교","layout":"versus","left":{"value":"294억","label":"아람코 2019"},"right":{"value":"644억","label":"앤트로픽 (최대)"},"headline":"AI 회사의 상장 규모","hl":[],"marks":[],"why":["숫자 대비"]},
  {"id":"C","name":"뉴욕","layout":"photo","photo_side":"full","image":{"file":"04_assets/footage/raw/nyc.jpg","focus":[0.5,0.5]},"top":"나스닥","lines":["AI 회사가","시장에 온다"],"hl":["시장에"],"sub":"","size":140,"text_y":330,"marks":[],"why":["장소 + 변화"]}]}
project("20261111-ai-industry-week","ch-ai-guide","clean-flat","AI 채널 · 이번 주 AI 업계: 돈과 신뢰 (활용법을 넘어 업계 소식) — manual v11",{"pleiades":"ARC-2008-ACD08-0272-001","nyc":"STS059-50-003","taiwan":"iss040e081462","sf":"iss037e002604"},brief,fact,spec)
