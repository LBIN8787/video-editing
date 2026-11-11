from common import *
brief={"brand":"market","line":"ch-paper-column",
 "desire":"반도체가 반등하는데 내가 아는 대장주 엔비디아만 떨어지는 이유를 정확히 알고 싶다",
 "trigger":"2026-11-09~10 엔비디아 이틀 -9.5% (반도체 지수는 +6.5%) — 11월 8일 이사회 조사 발표와 CEO 사과",
 "why_now":"11월 10일 독립 조사팀 선임 발표, 투자자 집단 소송 — 원인을 사실·의혹·모르는 것으로 나눠 볼 시점",
 "viewer_question":"반도체는 올랐는데 왜 엔비디아만 떨어졌을까?","question_type":"원인","mood":["긴장"],
 "topic":"업종 전체의 이유(11월 5일 반도체 급락) vs 회사만의 이유(11월 9~10일 CEO 사생활·안보 의혹 조사) — 같은 하락도 원인이 다르다",
 "our_angle":"반도체 지수·삼성·하이닉스와 같은 날짜로 나란히 놓아 '업종이냐 회사냐'를 숫자로 가름",
 "driver":{"type":"소재","why":"엔비디아는 국내 투자자 관심 최상위 종목 + 이틀 -9.5% 움직임","angle":"반대 결과 (업종은 오르는데 대장주만 하락)"},
 "score":{"desire":3,"clarity":3,"timeliness":3,"demand":3,"visuals":2,"angle":3},
 "demand_evidence":[{"kind":"news","detail":"11월 9~11일 로이터·CNBC·BBC·AP 등 주요 매체 연속 보도 (Google 뉴스 상위)","url":"https://news.google.com/search?q=Nvidia%20Huang"}],
 "visual_sources":["야후 파이낸스 시세(NVDA·^SOX·005930.KS·000660.KS)","NASA 야경 사진(퍼블릭 도메인)","직접 그린 인과 지도"],
 "candidates":[{"topic":"반도체는 올랐는데 왜 엔비디아만 떨어졌나","total":17,"why_not":"선택"},{"topic":"美 10월 CPI 예상 상회와 금리","total":13,"why_not":"숫자 원문 확인 더 필요"},{"topic":"앤트로픽 상장 공모","total":13,"why_not":"AI 채널에서 다룸"}]}
fact="""# 팩트시트 — 엔비디아만 떨어진 이유 (2026-11-11 확인)

| # | 사실 | 상태 | 출처 |
|---|---|---|---|
| F1 | 종가: 엔비디아 11/4 200.13 → 11/5 181.60(-9.3%) → 11/6 186.64 → 11/9 178.67(-4.3%) → 11/10 168.89(-5.5%) 달러 | ✅ | 야후 파이낸스 NVDA (`01_research/prices`) https://finance.yahoo.com/quote/NVDA/history |
| F2 | 필라델피아 반도체 지수: 11/4 10,268.65 → 11/5 9,011.14(-12.2%) / 11/6 9,390.25 → 11/9 10,033.93 → 11/10 9,998.33 (11/6 대비 +6.5%) | ✅ | 야후 파이낸스 ^SOX https://finance.yahoo.com/quote/%5ESOX/history |
| F3 | 삼성전자 11/6 188,700 → 11/10 198,900원(+5.4%), SK하이닉스 1,132,000 → 1,212,000원(+7.1%) | ✅ | 야후 파이낸스 005930.KS · 000660.KS |
| F4 | 11/9 엔비디아 -4.3%(-7.97달러), 시가총액 약 1,900억 달러 감소 | ✅ | AP (PBS) https://www.pbs.org/newshour/world/nvidia-and-huang-face-lawsuit-alleging-investors-were-misled-about-spy-affair |
| F5 | 11/8(일) 이사회 독립 조사 착수 발표, CEO가 혼외 관계를 인정·사과, 이사회 "국가안보나 회사 기밀이 침해됐다고 볼 이유는 없다", CEO 직은 유지 | ✅ | AP (PBS) https://www.pbs.org/newshour/world/what-we-know-and-what-we-dont-as-nvidia-investigates-an-alleged-spy-plot-involving-its-ceo · 엔비디아 'A Message to Our Company' https://nvidianews.nvidia.com/news/a-message-to-our-company |
| F6 | 11/10 이사회 독립 이사들이 조준 H. 김 전 뉴욕 남부지검 검사장 대행과 와크텔 립튼 로펌에 조사 의뢰 | ✅ | 엔비디아 발표 https://nvidianews.nvidia.com/news/statement-from-the-independent-members-of-the-nvidia-board |
| F7 | 뉴욕타임스 보도: 미 정보당국이 상대 인물(중국 국적 사업가)이 중국 정부를 위해 정보를 모은 것으로 판단 — **보도된 의혹** | ⚠️ 의혹 | AP (PBS) 같은 기사 |
| F8 | 중국 외교부 "근거 없는 중국 비방" | ✅ | AP (PBS) https://www.pbs.org/newshour/world/china-dismisses-claims-of-spy-plot-involving-nvidia-ceo-huang-as-a-smear-campaign |
| F9 | 11/9 투자자 집단 소송 제기(기간 10/9~11/8), 트럼프 대통령 "FBI 가 조사 중" | ✅ | AP (PBS) 소송 기사 |
| F10 | 상대 인물이 일했던 회사는 2년간 엔비디아 칩 48억 달러어치 구매(뉴욕타임스), 미 상무부가 수출 규제 우회 의혹 조사 — 엔비디아는 당시 '위법 없음'이라고 밝힘 | ⚠️ 보도 | AP (PBS) 소송 기사 |
| F11 | 11/5 하락은 회사 발표·공시 없이 업종 전체와 함께 — 데이터센터 수요·선거 불확실성 우려가 거론됨 | ⚠️ 2차 | Trefis https://www.trefis.com/stock/nvda/articles/623357/what-sent-nvidia-stock-lower/2026-11-06 |

## 쓰지 않는 것
- 상대 인물의 이름·사진 (공인 아님, 의혹 단계)
- 사생활 세부 내용
- '주가가 회복된다/더 떨어진다' 같은 전망 단정, 목표가
"""
spec={"title":"반도체는 올랐는데 왜 엔비디아만 떨어졌나","bgm":"digital-clouds",
 "core_message":"11월 5일엔 반도체 전체가 함께 떨어졌지만, 11월 9~10일엔 업종이 오르는데 엔비디아만 떨어졌다 — 이번 하락은 회사만의 불확실성(CEO 관련 조사)이 이유다.",
 "question":"반도체는 올랐는데 왜 엔비디아만 떨어졌을까?",
 "logic":["11월 5일: 반도체 지수 -12.2%, 엔비디아 -9.3% → 업종 전체의 이유","11월 9~10일: 반도체 지수 +6.5%, 삼성·하이닉스 +5~7%, 엔비디아 -9.5% → 회사만의 이유","회사만의 이유: CEO 관련 안보 의혹 → 이사회·FBI 조사, 투자자 소송","확인할 신호: 독립 조사 결과, 다음 실적 발표, 수출 규제 조사"],
 "compare_to":[{"value":"엔비디아 이틀 -9.5%","to":"같은 기간 반도체 지수 +6.5%"},{"value":"11월 9일 시가총액 약 1,900억 달러 감소","to":"하루 만에"}],
 "analogies":[{"a":"업종 전체의 하락","b":"폭풍이 와서 모든 배가 흔들리는 것"},{"a":"회사만의 하락","b":"바다는 잔잔한데 한 배의 선장이 조사를 받는 것"}],
 "past_cases":[{"case":"11월 5일 반도체 동반 급락 (지수 -12.2%, 엔비디아 -9.3%)","lesson":"같은 하락이라도 업종 이유인지 회사 이유인지 나눠 봐야 한다"}],
 "glossary":[{"term":"필라델피아 반도체 지수","plain":"미국에 상장된 주요 반도체 회사 주가를 묶은 지수 — 반도체 업종 전체의 온도계"},{"term":"집단 소송","plain":"같은 피해를 봤다는 여러 투자자를 대표해 한 사람이 내는 소송"},{"term":"수출 규제","plain":"첨단 칩을 특정 나라에 팔지 못하게 막는 정부 규칙"}],
 "scenes":[]}
S=spec["scenes"]; s=S.append
s(dict(type="intro",chapter=0,series="시장의 이유",as_of="11월 11일 기준",bg_src="sf",title_lines=["반도체는 올랐는데,","왜 엔비디아만?"],agenda_beat=2,
  layers=[{"kind":"photo","src":"sf","beat":1,"side":"right","w":600,"top":250,"caption":"샌프란시스코만 일대 · NASA ISS (2013)"}],
  beats=B("안녕하세요. 움직인 이유를, 연결된 것까지 쉽게 풀어 드리는 시장의 이유입니다.",
          "오늘은 엔비디아입니다. 이번 주 반도체 주식은 다시 올랐는데, 엔비디아만 이틀 연속 떨어졌거든요.",
          "이런 순서로 보겠습니다. 숫자로 무엇이 움직였는지, 엔비디아만의 이유는 무엇인지, 그리고 앞으로 확인할 신호까지요.",
          "다 보고 나시면, 같은 하락도 원인이 다를 수 있다는 걸 바로 구별하실 수 있을 거예요. 시작하겠습니다.")))
s(dict(type="kb",chapter=0,clip={"src":"sf","start":0},move="in",stamp="미국 실리콘밸리 일대 · 11월 10일",label="자료 사진 · NASA ISS (2013, 퍼블릭 도메인)",
  layers=[{"kind":"locator","at":[-121.96,37.35],"label":"엔비디아 본사 · 산타클라라","beat":0,"side":"right","top":120,"scale":2.2}],
  beats=B("11월 10일 기준, 엔비디아 주가는 168.89달러. 11월 6일보다 9.5% 낮습니다.","같은 기간 반도체 지수는 오히려 6.5% 올랐습니다. 대장주가 업종과 반대로 간 거죠.")))
s(dict(type="card_type",chapter=0,lines=["업종은 올랐는데,","왜 대장주만 떨어졌을까?"],
  beats=B("업종은 올랐는데 왜 대장주만 떨어졌을까요? 오늘 풀어 볼 질문입니다.")))
s(dict(type="chapter",chapter=1,num="1",title="숫자로 보면",icon="chart-line",beats=B("첫 번째, 먼저 숫자부터 보겠습니다.")))
s(dict(type="chart",chapter=1,label="야후 파이낸스 엔비디아 일별 종가 (NVDA) · 2026.11.10 기준",ticker="NVDA",period="3mo",title="엔비디아 주가 (달러)",
  beats=[{"say":"엔비디아는 10월 말 210달러대에서 내려오기 시작했고, 11월 5일 하루 9.3% 떨어졌습니다."},
         {"say":"그리고 11월 9일과 10일, 이틀 연속 다시 떨어져 168달러대가 됐습니다.","focus_last":4,"mark":"181.6 → 168.9"}]))
s(dict(type="versus",chapter=1,label="야후 파이낸스 종가 · 11월 6일 → 11월 10일",left={"value":"+6.5%","label":"필라델피아 반도체 지수","icon":"trending-up"},
  right={"value":"-9.5%","label":"엔비디아","icon":"trending-down"},bg="photo",bg_src="taiwan",
  layers=[{"kind":"locator","at":[127.0,37.5],"label":"삼성·SK하이닉스 +5~7%","beat":0,"side":"right","top":700,"scale":2.0}],
  beats=[{"say":"같은 날짜로 나란히 놓아 볼게요. 11월 6일부터 10일까지 반도체 지수는 6.5% 올랐고, 삼성전자와 SK하이닉스도 5~7% 올랐습니다."},
         {"say":"그런데 엔비디아만 9.5% 떨어졌습니다.","question":"업종이 아니라, 회사의 문제?"}]))
s(dict(type="bars",chapter=1,label="야후 파이낸스 종가 · 11월 4일 → 5일",title="11월 5일은 달랐다: 하루 낙폭 (%)",unit="%",
  items=[{"label":"반도체 지수","value":12.2,"text":"-12.2"},{"label":"엔비디아","value":9.3,"text":"-9.3"}],
  beats=[{"say":"비교를 위해 일주일 전을 보죠. 11월 5일엔 반도체 지수가 12% 넘게 떨어졌고, 엔비디아는 오히려 그보다 덜 떨어졌습니다."},
         {"say":"그때는 업종 전체의 이유, 이번엔 엔비디아만의 이유라는 뜻입니다."}]))
s(dict(type="recap",chapter=1,title="여기까지 정리",items=["11월 5일은 업종 전체, 11월 9~10일은 엔비디아만 떨어졌다"],new_from=0,
  layers=[{"kind":"photo","src":"taiwan","beat":0,"side":"right","w":460,"top":560,"caption":"대만·일본 일대 · NASA ISS (2014)"}],
  beats=B("정리하면, 같은 하락이라도 11월 5일은 업종 전체, 이번엔 엔비디아 혼자였습니다.")))
s(dict(type="chapter",chapter=2,num="2",title="엔비디아만의 이유",icon="building-2",beats=B("여기까지가 숫자였고요. 두 번째, 엔비디아만의 이유는 무엇이었을까요?")))
s(dict(type="timeline",chapter=2,label="AP(PBS)·엔비디아 발표",title="11월, 엔비디아에 무슨 일이",years=["10월 9일","11월 8일","11월 9일","11월 10일"],
  events=[{"at":"10월 9일","label":"뉴욕타임스 첫 보도","sub":"CEO와 한 사업가의 만남"},{"at":"11월 8일","label":"이사회 독립 조사 착수","sub":"CEO 사과"},
          {"at":"11월 9일","label":"-4.3%, 투자자 소송","sub":"FBI 조사(대통령 언급)"},{"at":"11월 10일","label":"외부 조사팀 선임","sub":"-5.5%"}],
  beats=[{"say":"10월, 뉴욕타임스가 CEO 젠슨 황과 한 중국 국적 사업가의 관계를 보도했습니다. 미 정보당국은 이 사업가가 중국을 위해 정보를 모았다고 판단했다는 보도였죠.","upto":1},
         {"say":"11월 8일 일요일, 엔비디아 이사회가 독립 조사를 시작했고, 젠슨 황은 혼외 관계를 인정하고 사과했습니다.","upto":2},
         {"say":"다음 날 주가는 4.3% 떨어졌고, 투자자 소송도 나왔습니다. 10일에는 외부 조사팀까지 꾸려졌죠.","upto":4}]))
s(dict(type="quote",chapter=2,label="AP 보도 (PBS) · 2026.11.9",who="엔비디아 이사회",role="11월 8일 발표",quote="국가안보나 회사 기밀이 침해됐다고 볼 이유는 없다.",keyword="이유는 없다",note="회사 입장",fx=["dust"],
  beats=[{"say":"회사 입장은 이렇습니다. 국가안보나 회사 기밀이 침해됐다고 볼 이유는 없다. 그리고 젠슨 황은 CEO 를 계속 맡습니다."},
         {"say":"다만 조사는 이제 시작입니다.","mark":True}]))
s(dict(type="quote",chapter=2,label="AP 보도 (PBS) · 2026.11.9",who="중국 외교부 대변인",role="11월 9일 정례 브리핑",quote="이른바 중국 스파이 의혹은 근거가 없다. 중국에 대한 비방일 뿐이다.",keyword="근거가 없다",note="중국 입장",fx=["dust"],
  beats=[{"say":"중국 정부는 정면으로 부인했습니다. 근거 없는 의혹이고, 중국에 대한 비방일 뿐이라는 거죠."},
         {"say":"즉 지금은 의혹과 부인이 맞서 있는 단계입니다.","mark":True}]))
s(dict(type="analogy",chapter=2,label="자체 정리",title="폭풍과 선장",fx=["tilt"],
  left={"icon":"wind","label":"11월 5일","sub":"폭풍 — 모든 배가 흔들림"},right={"icon":"ship","label":"11월 9~10일","sub":"잔잔한 바다 — 한 배의 선장이 조사받음"},
  result={"icon":"circle-alert","label":"회사만의 불확실성은 그 회사 주가만 움직인다"},
  beats=[{"say":"비유하면 11월 5일은 폭풍이 와서 모든 배가 흔들린 날입니다. 이번은 바다는 잔잔한데 한 배의 선장이 조사를 받는 상황이죠."},
         {"say":"배가 고장 난 건 아니어도, 선장에 대한 질문이 풀리기 전까지 승객은 불안합니다.","show_result":True}]))
s(dict(type="map_causal",chapter=2,label="이 영상 팩트시트 F4~F10 정리",
  beats=[{"say":"한 장으로 보면 이렇습니다. CEO 관련 보도가 이사회와 FBI 조사, 투자자 소송으로 이어졌고,","reveal":["news","probe","suit","risk"],"draw":[["news","probe"],["news","suit"],["probe","risk"],["suit","risk"]],"active":"risk"},
         {"say":"이 사업가가 일했던 회사가 엔비디아 칩을 대량으로 사 갔고, 수출 규제를 피했는지 정부가 조사 중이라는 보도까지 겹쳐, 불확실성이 커졌습니다.","reveal":["export","price"],"draw":[["export","risk"],["risk","price"]],"active":"price"}]))
s(dict(type="chapter",chapter=3,num="3",title="확인할 신호",icon="target",beats=B("마지막 세 번째, 그럼 앞으로 무엇을 보면 될까요?")))
s(dict(type="checklist",chapter=3,label="11월 11일 기준 · 투자 권유가 아닙니다",title="확인할 신호",
  rows=[{"label":"독립 조사 결과 — 안보·기밀 문제가 있었나","state":"warn"},{"label":"미 정부 조사 — 칩 수출 규제 위반이 있었나","state":"warn"},
        {"label":"다음 실적 발표 — 사업 숫자는 그대로인가","state":"warn"},{"label":"이 판단이 틀렸다면: 반도체 지수와 다시 같이 움직이기 시작할 때","state":"no"}],
  beats=[{"say":"확인할 신호는 세 가지입니다. 독립 조사 결과, 수출 규제에 대한 정부 조사, 그리고 다음 실적 발표의 사업 숫자입니다.","upto":3},
         {"say":"그리고 이 판단이 틀렸다면, 엔비디아가 다시 반도체 지수와 같은 방향으로 움직이기 시작할 겁니다. 회사만의 이유가 옅어졌다는 뜻이니까요.","upto":4}]))
s(dict(type="kinetic",chapter=3,beats=[{"say":"업종이 아니라 회사가 흔들릴 때, 주가는 혼자 움직입니다.","hit":["회사가","혼자"]}]))
s(dict(type="outro",chapter=3,title="시장의 이유",sub="11월 11일 기준 · 출처는 설명란에",clip={"src":"beijing","start":0},beats=B("오늘 시장의 이유는 여기까지입니다. 출처는 모두 설명란에 남겨 두겠습니다.")))
spec["map"]={"nodes":{"news":{"label":"CEO 관련 보도 (10월~)","icon":"newspaper","x":250,"y":400},"probe":{"label":"이사회·FBI 조사","icon":"search","x":800,"y":300},
  "suit":{"label":"투자자 집단 소송","icon":"gavel","x":800,"y":520},"risk":{"label":"회사만의 불확실성","icon":"circle-alert","x":1300,"y":400},
  "export":{"label":"칩 수출 규제 조사 보도","icon":"microchip","x":800,"y":760},"price":{"label":"엔비디아 이틀 -9.5%","icon":"trending-down","x":1680,"y":600}},
  "edges":[["news","probe"],["news","suit"],["probe","risk"],["suit","risk"],["export","risk"],["risk","price"]]}
spec["package"]={"title":"반도체는 올랐는데 왜 엔비디아만 떨어졌나 | 업종이냐 회사냐","title_options":["반도체는 올랐는데 왜 엔비디아만 떨어졌나 | 업종이냐 회사냐","엔비디아 이틀 -9.5%, 반도체 지수는 +6.5% — 진짜 이유는?","같은 하락, 다른 이유: 11월 5일 vs 11월 10일 엔비디아"],
 "title_why":["[움직임 + 이유 질문] market 공식","숫자 대비","비교형"],
 "thumbnails":[{"id":"A","name":"실리콘밸리 야경 + 질문","layout":"photo","photo_side":"full","image":{"file":"04_assets/footage/raw/sf.jpg","focus":[0.5,0.5]},"top":"11월 10일 기준","lines":["반도체는 올랐는데","엔비디아만?"],"hl":["엔비디아만?"],"sub":"업종이냐 회사냐","size":140,"text_y":330,"marks":[],"why":["질문 + 장소"]},
  {"id":"B","name":"숫자 대비","layout":"versus","left":{"value":"+6.5%","label":"반도체 지수"},"right":{"value":"-9.5%","label":"엔비디아"},"headline":"같은 이틀, 반대 방향","hl":[],"marks":[],"why":["숫자 둘이 질문을 만듦"]},
  {"id":"C","name":"폭풍과 선장","layout":"photo","photo_side":"full","image":{"file":"04_assets/footage/raw/taiwan.jpg","focus":[0.5,0.5]},"top":"엔비디아","lines":["폭풍이 아니라","선장 문제"],"hl":["선장"],"sub":"","size":140,"text_y":330,"marks":[],"why":["비유 한 줄"]}]}
project("20261111-market-nvidia","ch-paper-column","paper-sketch","시장 채널 · 반도체는 올랐는데 왜 엔비디아만 떨어졌나 — manual v11",{"sf":"iss037e002604","taiwan":"iss040e081462","nyc":"STS059-50-003","beijing":"iss040e091715"},brief,fact,spec)
