"""모라벡 편 v6 — 대본 v6(미주일기 문법, 10.7분, 2026-11-14 통과) + 애니메이션 무대(stage).

대본: projects/20261113-curiosity-moravec/02_script/script_v6.md (한 문장 = 한 박자).
연출 규칙: manual/04 §0-5 (장면 goal·박자 why, 한 화면 4개 이하·글자 하나·동사를 그림이 연기), 인트로 없음 (README §2-1).
실존 인물(튜링·모라벡·카스파로프)은 그림으로 닮게 그리지 않는다 — 카스파로프·딥 블루는 실제 사진, 나머지는 이름 한 줄 + 그 사람이 남긴 것(종이 체스·수레·책).
"""
import re
from pathlib import Path

CR = {"kasparov": "카스파로프: L. Kobus CC BY 4.0", "deepblue": "딥 블루: C. Xu CC BY 2.0"}
g = lambda n: f"gen/{n}.png"
CRS = [g("crumple1"), g("crumple2"), g("crumple3"), g("shirt_crumpled")]
KP = {"src": "photo:kasparov.jpg", "w": 300, "ratio": 1.18, "focus": "50% 25%", "caption": "가리 카스파로프", "credit": CR["kasparov"]}
DB = {"src": "photo:deepblue.jpg", "w": 280, "ratio": 1.25, "caption": "딥 블루 (IBM)", "credit": CR["deepblue"]}

# (장면 목표, 배경, [(why, [acts])...]) — 박자 순서는 script_v6.md 의 문장 순서와 같다
S = [
 ("2015년 큰 기대를 받은 빨래 기계가 4년 만에 무너졌다는 것, 그리고 체스 챔피언을 이긴 기계와의 대비로 영상의 질문을 품는다", "paper", [
  ("여는 장면(docs/30 ①): 전시장 한가운데의 기계와 그 앞에 모인 사람들 — 큰 기대의 순간",
   [{"t": "2015년", "do": "text", "id": "yr", "kind": "year", "text": "2015. 10 · 도쿄", "y": 130},
    {"t": "냉장고만", "do": "in", "id": "lr", "src": g("laundroid"), "x": 1200, "y": 850, "h": 540, "from": "rise"},
    {"do": "in", "id": "vs", "src": g("visitors"), "x": 560, "y": 900, "h": 400, "from": "walk", "wdur": 2.6}]),
  ("기계가 약속한 것 = 반듯하게 갠 옷 더미가 나옴",
   [{"t": "빨래를", "do": "in", "id": "sh0", "src": g("shirt_crumpled"), "x": 560, "y": 560, "h": 200, "from": "pop"},
    {"t": "기다리면", "do": "into", "on": "sh0", "target": "lr"},
    {"t": "반듯하게", "do": "in", "id": "fs", "src": g("folded_stack"), "x": 1640, "y": 860, "h": 210, "from": "right"},
    {"t": "런드로이드", "do": "fx", "on": "lr", "kind": "sparkle", "dx": 0.2}]),
  ("기대의 크기를 숫자 하나로 (② 그 일의 크기)",
   [{"t": "이 기계를", "do": "out", "on": ["vs", "fs", "yr"]},
    {"t": "600억", "do": "count", "id": "c600", "to": 600, "fmt": "{n}억 원", "kind": "num", "x": 560, "y": 380, "dur": 1.2},
    {"t": "해방시키겠다고", "do": "act", "on": "lr", "a": "hop", "n": 1}]),
  ("4년 뒤 같은 기계가 연기를 내며 주저앉음 — 기대가 무너지는 장면",
   [{"t": "그러나", "do": "out", "on": "c600"},
    {"t": "2019년", "do": "text", "id": "y19", "kind": "year", "text": "2019. 4", "y": 130},
    {"t": "파산을", "do": "act", "on": "lr", "a": "sink"},
    {"t": "파산을", "do": "fx", "on": "lr", "kind": "smoke", "delay": 0.3, "dx": 0.2}]),
  ("'한참'을 시계로: 구겨진 티셔츠 앞에서 시곗바늘이 도는 동안",
   [{"t": "티셔츠", "do": "in", "id": "ts", "src": g("shirt_crumpled"), "x": 560, "y": 840, "h": 260, "from": "left"},
    {"t": "한참이", "do": "in", "id": "cl", "src": g("clock"), "x": 560, "y": 520, "h": 200, "from": "pop"},
    {"t": "한참이", "do": "act", "on": "cl", "a": "wobble", "n": 3}]),
  ("시간을 22년 거슬러: 체스판이 먼저 무대에 오름 — 영상의 모티프 ①",
   [{"t": "기계가", "do": "out", "on": "all", "to": "left"},
    {"t": "1997년의", "do": "text", "id": "y97", "kind": "year", "text": "1997", "y": 130},
    {"t": "체스", "do": "in", "id": "bd", "src": g("chessboard"), "x": 560, "y": 800, "h": 320, "from": "left", "delay": 0.1},
    {"t": "이긴", "do": "fx", "on": "bd", "kind": "sparkle"}]),
  ("영상 전체의 질문을 두 주인공의 대결로: 체스판(이김) vs 구겨진 티셔츠(고전) — 끝까지 다시 나올 그림",
   [{"t": "티셔츠", "do": "in", "id": "ts2", "src": g("shirt_crumpled"), "x": 1360, "y": 800, "h": 300, "from": "right"},
    {"t": "고전했을까요", "do": "act", "on": "ts2", "a": "wobble", "n": 3},
    {"t": "고전했을까요", "do": "fx", "on": "ts2", "kind": "?", "hold": 0}]),
 ]),
 ("체스는 오랫동안 '지능의 상징'이었고, 연필로 한 수에 30분 걸리던 체스가 1초에 2억 수를 따지는 기계로 세계 챔피언을 이기는 흐름을 따라간다", "paper", [
  ("체스 = 기계 지능의 시험장. 체스판 하나로 시작",
   [{"t": "체스로", "do": "in", "id": "bd", "src": g("chessboard"), "x": 960, "y": 830, "h": 400, "from": "drop"}]),
  ("'생각할 수 있다는 증거' — 체스판에 왕관처럼 반짝임, 글자는 핵심어 하나",
   [{"t": "증거가", "do": "text", "id": "w", "kind": "word", "text": "지능의 상징", "y": 170},
    {"t": "증거가", "do": "fx", "on": "bd", "kind": "sparkle"}]),
  ("튜링은 실존 인물 — 사진 대신 그가 남긴 것(종이 위의 체스)과 이름 한 줄로",
   [{"t": "1948년", "do": "out", "on": ["bd", "w"]},
    {"t": "1948년", "do": "text", "id": "nm", "kind": "name", "text": "1948 · 앨런 튜링", "y": 150, "delay": 0.1},
    {"t": "프로그램을", "do": "in", "id": "pc", "src": g("paper_chess"), "x": 960, "y": 850, "h": 470, "from": "rise"}]),
  ("컴퓨터 대신 연필과 종이: 계산한 종이가 옆에 쌓여 감",
   [{"t": "1952년", "do": "out", "on": "nm"},
    {"t": "1952년", "do": "text", "id": "y52", "kind": "year", "text": "1952", "y": 150, "delay": 0.1},
    {"t": "연필과", "do": "in", "id": "ps", "src": g("paper_stack"), "x": 1520, "y": 850, "h": 380, "from": "drop"}]),
  ("한 수에 30분 = 시계가 돌고, '졌습니다'에 종이 체스가 주저앉음",
   [{"t": "30분", "do": "in", "id": "cl", "src": g("clock"), "x": 420, "y": 520, "h": 210, "from": "pop"},
    {"t": "30분", "do": "act", "on": "cl", "a": "wobble", "n": 4},
    {"t": "졌습니다", "do": "act", "on": "pc", "a": "sink"}]),
  ("세월이 흘러 체스판이 다시 — 시험장의 무대",
   [{"t": "그", "do": "out", "on": "all"},
    {"t": "시험장이", "do": "in", "id": "bd2", "src": g("chessboard"), "x": 800, "y": 830, "h": 380, "from": "fade", "delay": 0.2}]),
  ("넘지 못한 벽 = 판 옆에 우뚝 선 왕(세계 챔피언의 자리)",
   [{"t": "세계", "do": "in", "id": "kg", "src": g("chessking"), "x": 1400, "y": 830, "h": 330, "from": "drop"},
    {"t": "넘지", "do": "act", "on": "kg", "a": "pulse"}]),
  ("1996년 첫 도전: 실제 인물·기계 사진으로 두 상대를 마주 세움",
   [{"t": "1996년", "do": "out", "on": ["bd2", "kg"]},
    {"t": "1996년", "do": "text", "id": "y96", "kind": "year", "text": "1996. 2 · 필라델피아", "y": 130, "delay": 0.1},
    {"t": "딥", "do": "in", "id": "db", **DB, "x": 1360, "y": 860, "from": "right"},
    {"t": "카스파로프에게", "do": "in", "id": "k", **KP, "x": 560, "y": 860, "from": "left"}]),
  ("첫 판은 기계, 승부는 사람: 점수 하나로",
   [{"t": "첫", "do": "act", "on": "db", "a": "pulse"},
    {"t": "4대", "do": "out", "on": "y96"},
    {"t": "4대", "do": "text", "id": "sc", "kind": "num", "text": "4 : 2", "y": 200, "delay": 0.1},
    {"t": "가져갔습니다", "do": "act", "on": "k", "a": "pulse"}]),
  ("사람의 직관이 앞서는 듯 — 사람 쪽에 반짝임",
   [{"t": "직관이", "do": "fx", "on": "k", "kind": "sparkle"}]),
  ("1년 동안 다시 다듬음 — 사람은 잠시 퇴장하고 기계만 남아 덜컹거림",
   [{"t": "그러나", "do": "out", "on": ["k", "sc"]},
    {"t": "다듬었습니다", "do": "act", "on": "db", "a": "shake"},
    {"t": "다듬었습니다", "do": "fx", "on": "db", "kind": "lines", "dx": -0.2}]),
  ("연필의 30분 → 기계의 1초 2억 수: 시계와 올라가는 숫자의 대비",
   [{"t": "튜링이", "do": "in", "id": "cl2", "src": g("clock"), "x": 420, "y": 560, "h": 200, "from": "pop"},
    {"t": "2억", "do": "count", "id": "n2", "to": 200000000, "fmt": "1초에 {n}수", "kind": "num", "x": 760, "y": 200, "fs": 96, "dur": 1.6}]),
  ("1997년 재대결의 마지막 판: 체스 왕이 쓰러지고(기권) 사람 사진이 자리를 뜸",
   [{"t": "1997년", "do": "out", "on": ["cl2", "n2"]},
    {"t": "1997년", "do": "text", "id": "y97", "kind": "year", "text": "1997. 5. 11 · 뉴욕", "y": 130, "delay": 0.1},
    {"t": "카스파로프는", "do": "in", "id": "k2", **KP, "x": 520, "y": 860, "from": "left"},
    {"t": "19수", "do": "in", "id": "kg2", "src": g("chessking"), "x": 960, "y": 820, "h": 220, "from": "drop"},
    {"t": "일어났고", "do": "act", "on": "kg2", "a": "tip"},
    {"t": "일어났고", "do": "act", "on": "k2", "a": "rise", "delay": 0.35}]),
  ("'지능의 꼭대기에 오른 순간' = 기계가 무대 가운데로 커지고 기자들의 플래시",
   [{"t": "꼭대기라고", "do": "out", "on": ["kg2", "y97"]},
    {"t": "꼭대기라고", "do": "to", "on": "db", "x": 960, "scale": 1.3, "dur": 0.9},
    {"t": "순간이었습니다", "do": "fx", "kind": "flash", "n": 3}]),
 ]),
 ("같은 무렵 방 하나를 건너는 데 다섯 시간이 걸린 수레 — 체스와 정반대의 벽을 보고 '모라벡의 역설'을 안다", "paper", [
  ("두 기계의 대비를 처음부터: 작은 체스판(왼쪽)과 방 안의 의자(오른쪽)",
   [{"t": "같은", "do": "in", "id": "bd", "src": g("chessboard"), "x": 420, "y": 800, "h": 230, "from": "fade"},
    {"t": "정반대의", "do": "in", "id": "ch", "src": g("chair_a"), "x": 1420, "y": 840, "h": 320, "from": "right"}]),
  ("모라벡은 이름 한 줄, 그가 만든 수레가 주인공 — 카메라를 단 바퀴 수레가 들어옴",
   [{"t": "스탠퍼드", "do": "out", "on": "bd"},
    {"t": "스탠퍼드", "do": "text", "id": "nm", "kind": "name", "text": "한스 모라벡 · 스탠퍼드 대학원생", "y": 150, "delay": 0.1},
    {"t": "수레가", "do": "in", "id": "ct", "src": g("stanford_cart"), "x": 360, "y": 860, "h": 330, "from": "walk"}]),
  ("방을 건너는 수레: 의자 사이를 걸음걸음 지나가고, 걸린 시간은 숫자 하나",
   [{"t": "1979년", "do": "out", "on": "nm"},
    {"t": "의자", "do": "in", "id": "ch2", "src": g("chair_b"), "x": 980, "y": 840, "h": 290, "from": "drop"},
    {"t": "건너는", "do": "to", "on": "ct", "x": 640, "dur": 2.4, "walk": True},
    {"t": "다섯", "do": "count", "id": "h5", "to": 5, "fmt": "약 {n}시간", "kind": "num", "y": 200, "dur": 0.8}]),
  ("멈춰 서서 계산하는 수레: 물음표(분석 중)와 시계",
   [{"t": "조금", "do": "out", "on": "h5"},
    {"t": "멈춰", "do": "fx", "on": "ct", "kind": "?", "hold": 2.5},
    {"t": "10분에서", "do": "in", "id": "cl", "src": g("clock"), "x": 1650, "y": 520, "h": 190, "from": "pop"},
    {"t": "계산해야", "do": "act", "on": "cl", "a": "wobble", "n": 3}]),
  ("모티프를 나란히: 체스판(챔피언과 겨룰 기계) vs 진땀 흘리는 수레(반나절)",
   [{"t": "체스판", "do": "out", "on": "all"},
    {"t": "체스판", "do": "in", "id": "bd2", "src": g("chessboard"), "x": 560, "y": 800, "h": 300, "from": "left", "delay": 0.2},
    {"t": "의자를", "do": "in", "id": "ct2", "src": g("stanford_cart"), "x": 1360, "y": 840, "h": 300, "from": "walk"},
    {"t": "반나절을", "do": "fx", "on": "ct2", "kind": "sweat", "dx": 0.1}]),
  ("기록으로 남김 = 책이 떨어져 펼쳐짐",
   [{"t": "훗날", "do": "out", "on": "all"},
    {"t": "1988년", "do": "text", "id": "y88", "kind": "year", "text": "1988 · 카네기멜런", "y": 150},
    {"t": "책에", "do": "in", "id": "bk", "src": g("book"), "x": 960, "y": 800, "h": 360, "from": "drop"}]),
  ("관찰을 시소로: 처음엔 '시험' 쪽이 내려가 있음(우리 생각) → '어렵거나 불가능' 순간 아기 쪽으로 넘어감",
   [{"t": "컴퓨터가", "do": "out", "on": ["bk", "y88"]},
    {"t": "컴퓨터가", "do": "seesaw", "id": "ss", "left": g("examtaker"), "right": g("baby_walk"), "x": 960, "y": 720, "w": 1200, "lh": 300, "rh": 260, "deg": -12, "delay": 0.15},
    {"t": "어렵거나", "do": "tilt", "on": "ss", "deg": 13, "dur": 1.2}]),
  ("뒤집힌 시소 위에 이름 한 줄 — 이 영상의 개념은 이 한 번만 글자로",
   [{"t": "모라벡의", "do": "text", "id": "mp", "kind": "word", "text": "모라벡의 역설", "y": 150, "fs": 110}]),
 ]),
 ("36년 뒤에도 로봇은 문 앞에서 넘어졌다 — 바로 그해 빨래 기계가 출발했다는 아이러니를 느낀다", "paper", [
  ("36년의 거리: 옛 수레(왼쪽)와 2015년의 로봇(오른쪽)",
   [{"t": "모라벡의", "do": "in", "id": "ct", "src": g("stanford_cart"), "x": 520, "y": 860, "h": 260, "from": "fade"},
    {"t": "36년이", "do": "text", "id": "yy", "kind": "year", "text": "1979 → 2015", "y": 150},
    {"t": "2015년에도", "do": "in", "id": "dr", "src": g("dr_door"), "x": 1320, "y": 880, "h": 480, "from": "walk"}]),
  ("어디서 무엇이 — 대회 이름 한 줄",
   [{"t": "넉", "do": "out", "on": ["ct", "yy"]},
    {"t": "다르파는", "do": "text", "id": "dp", "kind": "name", "text": "2015. 6 · 다르파 로봇 대회", "y": 150},
    {"t": "로봇들의", "do": "to", "on": "dr", "x": 960, "dur": 0.9}]),
  ("과제를 하나씩 — 로봇이 문 앞에서 움찔",
   [{"t": "문을", "do": "act", "on": "dr", "a": "pulse"},
    {"t": "밸브를", "do": "act", "on": "dr", "a": "shake"}]),
  ("'망설이다 넘어졌다'를 그대로: 물음표 → 쓰러진 자세",
   [{"t": "망설였고", "do": "fx", "on": "dr", "kind": "?", "hold": 1.5},
    {"t": "넘어졌습니다", "do": "pose", "on": "dr", "src": g("dr_fallen")},
    {"t": "넘어졌습니다", "do": "fx", "on": "dr", "kind": "lines", "delay": 0.2}]),
  ("우승 팀의 해법을 움직임으로: 무릎을 꿇고 바퀴로 굴러감 (그림은 특정 로봇을 닮게 그리지 않음)",
   [{"t": "우승은", "do": "out", "on": ["dr", "dp"]},
    {"t": "카이스트", "do": "text", "id": "kh", "kind": "name", "text": "우승 · 카이스트 '휴보'", "y": 150},
    {"t": "휴보는", "do": "in", "id": "hb", "src": g("dr_kneel"), "x": 520, "y": 870, "h": 330, "from": "walk"},
    {"t": "바퀴로", "do": "to", "on": "hb", "x": 1200, "dur": 2.2}]),
  ("2위 로봇의 한 장면: 손을 흔들다(wobble) 그 자리에서 쓰러짐",
   [{"t": "모든", "do": "out", "on": ["hb", "kh"]},
    {"t": "2위를", "do": "in", "id": "d2", "src": g("dr_door"), "x": 960, "y": 880, "h": 460, "from": "fade"},
    {"t": "흔들다가", "do": "act", "on": "d2", "a": "wobble", "n": 4},
    {"t": "넘어지기도", "do": "pose", "on": "d2", "src": g("dr_fallen")}]),
  ("아이러니를 한 화면에: 쓰러진 로봇(왼쪽)과 같은 해 기대를 받은 빨래 기계(오른쪽)",
   [{"t": "세계", "do": "out", "on": "all"},
    {"t": "세계", "do": "in", "id": "fl", "src": g("dr_fallen"), "x": 560, "y": 880, "h": 260, "from": "left", "delay": 0.2},
    {"t": "빨래", "do": "in", "id": "lr", "src": g("laundroid"), "x": 1380, "y": 870, "h": 470, "from": "right"},
    {"t": "600억", "do": "fx", "on": "lr", "kind": "sparkle", "dx": 0.2}]),
 ]),
 ("티셔츠는 놓일 때마다 모양이 다르고 체스는 언제나 같다 — 기계에게 무엇이 어려운지 눈으로 본다", "paper", [
  ("전환점의 질문(⑤ '그렇다면'): 구겨진 티셔츠 하나와 물음표",
   [{"t": "그렇다면", "do": "in", "id": "ts", "src": g("shirt_crumpled"), "x": 960, "y": 830, "h": 330, "from": "pop"},
    {"t": "어려운", "do": "fx", "on": "ts", "kind": "?", "hold": 0}]),
  ("생활 속 예 하나(docs/30 ⑥): 손이 빨래 더미에서 티셔츠를 휙 들어 올림",
   [{"t": "빨래", "do": "out", "on": "ts"},
    {"t": "빨래", "do": "in", "id": "hp", "src": g("hand_pick"), "x": 960, "y": 910, "h": 600, "from": "rise", "delay": 0.1},
    {"t": "집어", "do": "act", "on": "hp", "a": "lift"}]),
  ("눈이 하는 일: 렌즈 안의 천 모양이 계속 바뀜",
   [{"t": "구겨진", "do": "out", "on": "hp"},
    {"t": "구겨진", "do": "in", "id": "vw", "src": "lens:gen/crumple1.png", "x": 960, "y": 460, "r": 310, "from": "pop", "delay": 0.1},
    {"t": "놓일", "do": "morph", "on": "vw", "srcs": CRS + [g("crumple2")], "every": 0.55}]),
  ("손가락이 하는 일: 빠져나가려다 다시 움켜쥠 (흔들림 → 들어 올림)",
   [{"t": "손가락은", "do": "out", "on": "vw"},
    {"t": "손가락은", "do": "in", "id": "hp2", "src": g("hand_pick"), "x": 960, "y": 910, "h": 600, "from": "fade", "delay": 0.1},
    {"t": "빠져나가려는", "do": "act", "on": "hp2", "a": "shake"},
    {"t": "움켜쥡니다", "do": "act", "on": "hp2", "a": "lift"}]),
  ("같은 티셔츠의 세 모습을 나란히 — 말하는 순서대로 하나씩",
   [{"t": "같은", "do": "out", "on": "hp2"},
    {"t": "뒤집혀", "do": "in", "id": "a1", "src": g("crumple1"), "x": 460, "y": 800, "h": 270, "from": "drop"},
    {"t": "소매가", "do": "in", "id": "a2", "src": g("crumple2"), "x": 960, "y": 800, "h": 250, "from": "drop"},
    {"t": "엉켜", "do": "in", "id": "a3", "src": g("tangle"), "x": 1460, "y": 820, "h": 280, "from": "drop"}]),
  ("사람에겐 같은 옷, 로봇에겐 매번 처음: 로봇의 렌즈 속 모양이 계속 바뀜",
   [{"t": "사람은", "do": "out", "on": ["a1", "a2", "a3"]},
    {"t": "로봇에게는", "do": "in", "id": "rb", "src": g("robot_stare"), "x": 560, "y": 880, "h": 540, "from": "walk"},
    {"t": "로봇에게는", "do": "in", "id": "vw2", "src": "lens:gen/crumple3.png", "x": 1340, "y": 440, "r": 270, "from": "pop", "delay": 0.3},
    {"t": "처음", "do": "morph", "on": "vw2", "srcs": [g("crumple1"), g("tangle"), g("crumple2"), g("shirt_crumpled")], "every": 0.5}]),
  ("정반대 = 체스판이 떨어져 '딱' 고정",
   [{"t": "체스는", "do": "out", "on": "all"},
    {"t": "정반대입니다", "do": "in", "id": "bd", "src": g("chessboard"), "x": 960, "y": 840, "h": 440, "from": "drop"}]),
  ("정해진 것들: 숫자 하나(말 32개)와 판의 테두리",
   [{"t": "서른두", "do": "count", "id": "n32", "to": 32, "fmt": "말 {n}개", "kind": "num", "y": 170, "dur": 0.9},
    {"t": "여덟", "do": "mark", "on": "bd", "kind": "box", "pad": 20}]),
  ("'정해진 세계' — 테두리 안의 체스판에 이름 한 줄",
   [{"t": "따져야", "do": "out", "on": "n32"},
    {"t": "정해진", "do": "text", "id": "w", "kind": "word", "text": "정해진 세계", "y": 170}]),
 ]),
 ("보고·잡고·걷기는 수백만 년 다듬어진 깊은 부품이고 체스는 그 위의 얇은 새 층 — 시간의 길이와 깊이로 느낀다", "dark", [
  ("진화의 시간을 화면 끝에서 끝까지 이어지는 긴 선 하나로",
   [{"t": "진화에서", "do": "line", "id": "tl", "from": [80, 760], "to": [1840, 760], "dur": 1.6, "sw": 8}]),
  ("조상이 직접 보고·잡고·걸으며 긴 길을 걸어감",
   [{"t": "보고", "do": "in", "id": "an", "src": g("anc_look"), "x": 220, "y": 760, "h": 330, "from": "fade"},
    {"t": "잡고", "do": "pose", "on": "an", "src": g("anc_grab")},
    {"t": "걷는", "do": "pose", "on": "an", "src": g("anc_walk")},
    {"t": "수백만", "do": "to", "on": "an", "x": 1100, "dur": 3.6, "walk": True}]),
  ("증거 하나: 화산재 위의 발자국 → 오늘의 아기는 아무렇지 않게 걸음",
   [{"t": "발자국은", "do": "in", "id": "fp", "src": g("footprints"), "x": 520, "y": 860, "h": 150, "from": "fade"},
    {"t": "360만", "do": "text", "id": "t36", "kind": "year", "text": "360만 년 전", "y": 160},
    {"t": "느끼지", "do": "out", "on": "an"},
    {"t": "느끼지", "do": "in", "id": "bb", "src": g("baby_walk"), "x": 1100, "y": 760, "h": 260, "from": "fade", "delay": 0.1},
    {"t": "느끼지", "do": "act", "on": "bb", "a": "hop", "n": 1, "delay": 0.4}]),
  ("'생물학적 기계' = 오래된 톱니 기계 위에 얇은 회로가 얹힌 그림",
   [{"t": "모라벡의", "do": "out", "on": ["tl", "fp", "bb", "t36"]},
    {"t": "생물학적", "do": "in", "id": "ly", "src": g("layers"), "x": 960, "y": 880, "h": 560, "from": "rise"}]),
  ("깊은 곳의 부품 vs 위의 얇은 층: 핵심어 하나",
   [{"t": "가장", "do": "act", "on": "ly", "a": "pulse"},
    {"t": "얇은", "do": "text", "id": "th", "kind": "word", "text": "오래된 부품 위의 얇은 층", "y": 160, "color": "#F3D36B"}]),
  ("보이지 않는 매끄러움: 깊은 부품이 조용히 반짝임",
   [{"t": "매끄러워서", "do": "fx", "on": "ly", "kind": "sparkle", "dx": -0.1, "dy": 0.1}]),
  ("체스의 1,400년은 긴 선의 맨 끝 한 점",
   [{"t": "반면", "do": "out", "on": ["ly", "th"]},
    {"t": "체스는", "do": "line", "id": "tl2", "from": [80, 760], "to": [1840, 760], "dur": 1.0, "sw": 8},
    {"t": "1,400년", "do": "in", "id": "cg", "src": g("chaturanga"), "x": 1740, "y": 752, "h": 130, "from": "pop"},
    {"t": "1,400년", "do": "dot", "id": "pt", "x": 1835, "y": 760, "r": 15, "delay": 0.4}]),
  ("'어제 익힌 기술' — 긴 선의 맨 앞에는 발자국",
   [{"t": "진화의", "do": "in", "id": "fp2", "src": g("footprints"), "x": 260, "y": 840, "h": 110, "from": "fade"}]),
  ("느낌과 실제: 체스 말이 커졌다(우리 느낌) 다시 작아짐(기계에겐 쉬움)",
   [{"t": "어렵다고", "do": "act", "on": "cg", "a": "grow", "scale": 2.4},
    {"t": "기계가", "do": "act", "on": "cg", "a": "shrink", "scale": 1}]),
  ("한 문장 정리를 화면 글자 하나로",
   [{"t": "1994년", "do": "text", "id": "pk", "kind": "word", "text": "어려운 문제는 쉽고, 쉬운 문제는 어렵다", "y": 200, "fs": 72, "color": "#F3D36B"}]),
 ]),
 ("빨래 기계는 규칙을 짜 넣는 방식으로 실패했지만, 이제 로봇은 움직임을 보고 배운다", "dark", [
  ("실패한 기계를 다시 무대에: 연기를 내며 주저앉음",
   [{"t": "세븐", "do": "in", "id": "lr", "src": g("laundroid"), "x": 1240, "y": 880, "h": 480, "from": "fade"},
    {"t": "역설", "do": "act", "on": "lr", "a": "sink"},
    {"t": "역설", "do": "fx", "on": "lr", "kind": "smoke", "dx": 0.2, "delay": 0.3}]),
  ("규칙 책에 ✕, 실패의 크기는 숫자 하나",
   [{"t": "규칙을", "do": "in", "id": "rk", "src": g("book"), "x": 480, "y": 620, "h": 220, "from": "drop"},
    {"t": "어려웠고", "do": "mark", "on": "rk", "kind": "cross"},
    {"t": "2천만", "do": "count", "id": "debt", "to": 2000, "fmt": "{n}만 달러", "kind": "num", "x": 520, "y": 200, "fs": 110, "dur": 1.4}]),
  ("'방식이 달라졌다'를 배경이 어두운 종이 → 밝은 종이로",
   [{"t": "그러나", "do": "out", "on": "all"},
    {"t": "달라졌습니다", "do": "bg", "mode": "paper"}]),
  ("새 로봇 팔이 올라오고 빨래를 갬",
   [{"t": "2024년", "do": "text", "id": "y24", "kind": "year", "text": "2024. 10", "y": 130},
    {"t": "로봇을", "do": "in", "id": "ra", "src": g("robotarms"), "x": 1100, "y": 880, "h": 520, "from": "rise"},
    {"t": "공개했습니다", "do": "fx", "on": "ra", "kind": "sparkle", "dx": 0.3}]),
  ("'동작 기록을 보고 익혔다'를 움직임으로: 필름이 로봇 속으로 빨려 들어감",
   [{"t": "이", "do": "out", "on": "y24"},
    {"t": "일곱", "do": "in", "id": "mf", "src": g("motionfilm"), "x": 420, "y": 800, "h": 440, "from": "left"},
    {"t": "익혔습니다", "do": "into", "on": "mf", "target": "ra"}]),
  ("챗GPT 비유: 배운 로봇이 반짝이며 '딱'",
   [{"t": "챗GPT처럼", "do": "act", "on": "ra", "a": "pulse"},
    {"t": "배우는", "do": "fx", "on": "ra", "kind": "sparkle", "dx": 0.3}]),
 ]),
 ("아직 연구실 — 진짜 마지막 벽은 우리 집의 뒤죽박죽 빨래 바구니", "paper", [
  ("연구실의 로봇 팔 (아직 여기에)",
   [{"t": "연구실에", "do": "to", "on": "ra", "x": 560, "scale": 0.8, "dur": 0.9}]),
  ("'갈 길'을 거리로: 로봇과 집 사이에 점선 길",
   [{"t": "집집마다", "do": "in", "id": "hs", "src": g("house"), "x": 1520, "y": 840, "h": 380, "from": "right"},
    {"t": "갈", "do": "line", "id": "rd", "from": [820, 800], "to": [1300, 800], "dash": True, "dur": 1.6, "sw": 12}]),
  ("실제 바구니의 뒤죽박죽: 바구니에서 하나씩 튀어나옴",
   [{"t": "연구실의", "do": "out", "on": ["ra", "hs", "rd"]},
    {"t": "실제", "do": "in", "id": "bs", "src": g("basket"), "x": 960, "y": 880, "h": 380, "from": "drop"},
    {"t": "양말과", "do": "in", "id": "sk", "src": g("sock"), "x": 480, "y": 560, "h": 170, "from": "pop"},
    {"t": "니트", "do": "in", "id": "kn", "src": g("knit"), "x": 1460, "y": 560, "h": 230, "from": "pop"},
    {"t": "운동복이", "do": "in", "id": "tg", "src": g("tangle"), "x": 1500, "y": 880, "h": 220, "from": "pop"}]),
  ("'가장 높은 벽' = 바구니가 덜컹",
   [{"t": "뒤죽박죽이야말로", "do": "act", "on": "bs", "a": "shake"},
    {"t": "벽일지도", "do": "fx", "on": "bs", "kind": "!", "hold": 1.8}]),
 ]),
 ("튜링의 연필 체스와 카스파로프가 다시 만나는 장면으로 처음과 끝을 잇는다 (수미상관)", "paper", [
  ("2012년: 튜링의 종이 체스가 다시 무대에",
   [{"t": "2012년", "do": "text", "id": "y12", "kind": "year", "text": "2012 · 튜링 탄생 100주년", "y": 130},
    {"t": "되살려", "do": "in", "id": "pc", "src": g("paper_chess"), "x": 760, "y": 860, "h": 440, "from": "rise"}]),
  ("그 상대: 15년 전의 그 챔피언(실제 사진)",
   [{"t": "카스파로프였습니다", "do": "in", "id": "k", **KP, "x": 1460, "y": 860, "from": "right"}]),
  ("16수 만의 승리: 숫자 하나와 반짝임",
   [{"t": "16수", "do": "out", "on": "y12"},
    {"t": "16수", "do": "count", "id": "n16", "to": 16, "fmt": "{n}수", "kind": "num", "y": 200, "dur": 0.8},
    {"t": "이겼습니다", "do": "fx", "on": "k", "kind": "sparkle"}]),
  ("반세기의 거리: 종이 체스 → 딥 블루 사이에 화살 같은 점선",
   [{"t": "체스", "do": "out", "on": "all"},
    {"t": "반나절이", "do": "in", "id": "pc2", "src": g("paper_chess"), "x": 420, "y": 860, "h": 320, "from": "left"},
    {"t": "세계", "do": "in", "id": "db", **DB, "x": 1480, "y": 860, "from": "right"},
    {"t": "반세기가", "do": "line", "id": "l1", "from": [660, 700], "to": [1260, 700], "dash": True, "dur": 1.2, "sw": 12}]),
  ("더 긴 거리: 수레 → 빨래 로봇 사이의 점선은 더 천천히 그려짐",
   [{"t": "그리고", "do": "out", "on": "all"},
    {"t": "의자", "do": "in", "id": "ct", "src": g("stanford_cart"), "x": 380, "y": 860, "h": 280, "from": "walk"},
    {"t": "빨래를", "do": "in", "id": "ra", "src": g("robotarms"), "x": 1520, "y": 860, "h": 360, "from": "right"},
    {"t": "훨씬", "do": "line", "id": "l2", "from": [620, 760], "to": [1300, 760], "dash": True, "dur": 3.2, "sw": 12}]),
 ]),
 ("기계에게 가장 어려운 일은 우리가 너무 오래 해 와서 잊은 일 — 오늘 저녁의 티셔츠 한 장", "paper", [
  ("의미 한 문장 = 빨래를 개는 손",
   [{"t": "기계에게", "do": "in", "id": "hf", "src": g("hands_fold"), "x": 900, "y": 880, "h": 540, "from": "rise"}]),
  ("마지막 장면: 반듯하게 갠 티셔츠와 반짝임 — 수백만 년의 연습",
   [{"t": "티셔츠", "do": "in", "id": "sf", "src": g("shirt_folded"), "x": 1560, "y": 860, "h": 230, "from": "drop"},
    {"t": "수백만", "do": "fx", "on": "hf", "kind": "sparkle", "dx": 0.2}]),
 ]),
]


def sentences() -> list[list[str]]:
    s = (Path(__file__).resolve().parents[2] / "projects/20261113-curiosity-moravec/02_script/script_v6.md").read_text(encoding="utf-8")
    body = s[s.index("## 1. 대본"):s.index("## 2. v5")]
    out, cur = [], None
    for ln in body.splitlines():
        if ln.startswith("### "):
            cur = []
            out.append(cur)
            continue
        if cur is None or not ln.strip() or ln.startswith("## "):
            continue
        cur += [x for x in re.split(r"(?<=[.?!])\s+", ln.strip()) if x]
    return out


def scenes() -> list[dict]:
    secs = sentences()
    assert len(secs) == len(S), (len(secs), len(S))
    out = []
    for i, (sec, (goal, bg, beats)) in enumerate(zip(secs, S), start=1):
        assert len(sec) == len(beats), (i, len(sec), len(beats))
        out.append({"id": i, "type": "stage", "goal": goal, "bg": bg,
                    "beats": [{"say": say, "why": why, "act": act} for say, (why, act) in zip(sec, beats)]})
    return out


# ---------------------------------------------------------------- 장면 나누기 (스타일 섞기 규칙: 같은 type 3연속 없음 · 4종 이상, manual/05)
# 대본 문장 순서는 그대로 두고, 그 문장의 성격에 맞는 장면 형식을 고른다:
#   질문·전환 한 문장 → kinetic(말하는 순간 글자가 박힘) / 숫자 하나가 주인공 → bignum / 두 숫자의 대비 → versus / 그 사람이 남긴 말 → quote
BG = {0: "film", 1: "tint", 2: "grid", 3: "spot", 4: "film", 5: "dark", 6: "dark", 7: "tint", 8: "spot", 9: "film"}
PLAN = [  # (절 번호, 박자 범위, type, 덧붙일 필드)
 (0, (0, 2), "stage", {}),
 (0, (2, 3), "bignum", {"label": "세븐 드리머스 시리즈 B 투자 (2016. 11, 보도)", "small": "2016년 · 약 60억 엔", "value": "600억 원"}),
 (0, (3, 7), "stage", {}),
 (1, (0, 11), "stage", {}),
 (1, (11, 12), "versus", {"label": "튜로챔프 (1952) · 딥 블루 (1997, 흔히 인용되는 수치)",
                          "left": {"value": "30분", "label": "1952 · 연필로 한 수", "icon": "clock"},
                          "right": {"value": "2억 수", "label": "1997 · 딥 블루의 1초", "icon": "cpu"}}),
 (1, (12, 14), "stage", {}),
 (2, (0, 1), "kinetic", {}),
 (2, (1, 5), "stage", {}),
 (2, (5, 7), "quote", {"label": "Hans Moravec, Mind Children (1988) — 풀어 옮김", "who": "한스 모라벡", "role": "로봇 연구자, 『마음의 아이들』(1988)",
                       "quote": "지능 검사나 체커를 어른처럼 하게 만드는 건 비교적 쉽다. 한 살 아기만큼 보고 움직이게 만드는 건 어렵거나 불가능하다.",
                       "keyword": "한 살 아기만큼", "note": "뒤집힌 관찰"}),
 (2, (7, 8), "stage", {}),
 (3, (0, 7), "stage", {}),
 (4, (0, 1), "kinetic", {}),
 (4, (1, 9), "stage", {}),
 (5, (0, 9), "stage", {}),
 (5, (9, 10), "quote", {"label": "Steven Pinker, The Language Instinct (1994)", "who": "스티븐 핑커", "role": "심리학자, 『언어 본능』(1994)",
                        "quote": "35년 인공지능 연구의 가장 큰 교훈은, 어려운 문제는 쉽고 쉬운 문제는 어렵다는 것이다.", "keyword": "쉬운 문제는 어렵다", "note": "뒤집힌 난이도"}),
 (6, (0, 1), "stage", {}),
 (6, (1, 2), "bignum", {"label": "세븐 드리머스 파산 (2019. 4, 테이코쿠 데이터뱅크·TechCrunch)", "small": "파산 당시 남은 빚", "value": "2천만 달러",
                        "compare": {"label": "우리 돈", "value": "200억 원+"}}),
 (6, (2, 6), "stage", {"merge_next": True}),
 (7, (0, 4), "stage", {}),
 (8, (0, 2), "stage", {}),
 (8, (2, 3), "bignum", {"label": "튜링 탄생 100주년 학회 (2012, 맨체스터)", "small": "카스파로프 vs 되살린 튜로챔프", "value": "16수"}),
 (8, (3, 5), "stage", {}),
 (9, (0, 1), "kinetic", {}),
 (9, (1, 2), "stage", {}),
]
# 나뉜 장면의 첫 박자에서 앞 장면에 있던 주인공을 다시 세움 / 다른 형식으로 옮긴 박자의 연출을 바꿈
FIX = {
 (0, 3): [{"t": "그러나", "do": "in", "id": "lr", "src": g("laundroid"), "x": 1200, "y": 850, "h": 540, "from": "fade"},
          {"t": "2019년", "do": "text", "id": "y19", "kind": "year", "text": "2019. 4", "y": 130},
          {"t": "파산을", "do": "act", "on": "lr", "a": "sink"},
          {"t": "파산을", "do": "fx", "on": "lr", "kind": "smoke", "delay": 0.3, "dx": 0.2}],
 (1, 12): [{"t": "1997년", "do": "text", "id": "y97", "kind": "year", "text": "1997. 5. 11 · 뉴욕", "y": 130},
           {"t": "1997년", "do": "in", "id": "db", **DB, "x": 1440, "y": 860, "from": "right"},
           {"t": "카스파로프는", "do": "in", "id": "k2", **KP, "x": 480, "y": 860, "from": "left"},
           {"t": "19수", "do": "in", "id": "kg2", "src": g("chessking"), "x": 960, "y": 820, "h": 220, "from": "drop"},
           {"t": "일어났고", "do": "act", "on": "kg2", "a": "tip"},
           {"t": "일어났고", "do": "act", "on": "k2", "a": "rise", "delay": 0.35}],
 (2, 1): [{"t": "스탠퍼드", "do": "text", "id": "nm", "kind": "name", "text": "한스 모라벡 · 스탠퍼드 대학원생", "y": 150},
          {"t": "수레가", "do": "in", "id": "ct", "src": g("stanford_cart"), "x": 360, "y": 860, "h": 330, "from": "walk"},
          {"t": "방을", "do": "in", "id": "ch", "src": g("chair_a"), "x": 1420, "y": 840, "h": 320, "from": "right"}],
 (2, 7): [{"t": "뒤집힌", "do": "seesaw", "id": "ss", "left": g("examtaker"), "right": g("baby_walk"), "x": 960, "y": 720, "w": 1200, "lh": 300, "rh": 260, "deg": -12},
          {"t": "관찰은", "do": "tilt", "on": "ss", "deg": 13, "dur": 1.2},
          {"t": "모라벡의", "do": "text", "id": "mp", "kind": "word", "text": "모라벡의 역설", "y": 150, "fs": 110}],
 (6, 2): [{"t": "그러나", "do": "bg", "mode": "paper"},
          {"t": "달라졌습니다", "do": "fx", "kind": "flash", "n": 1}],
 (8, 3): [{"t": "체스", "do": "in", "id": "pc2", "src": g("paper_chess"), "x": 420, "y": 860, "h": 320, "from": "left"},
          {"t": "세계", "do": "in", "id": "db", **DB, "x": 1480, "y": 860, "from": "right"},
          {"t": "반세기가", "do": "line", "id": "l1", "from": [660, 700], "to": [1260, 700], "dash": True, "dur": 1.2, "sw": 12}],
 (9, 1): [{"t": "오늘", "do": "in", "id": "hf", "src": g("hands_fold"), "x": 900, "y": 880, "h": 540, "from": "rise"},
          {"t": "티셔츠", "do": "in", "id": "sf", "src": g("shirt_folded"), "x": 1560, "y": 860, "h": 230, "from": "drop"},
          {"t": "수백만", "do": "fx", "on": "hf", "kind": "sparkle", "dx": 0.2}],
}
WHY_FIX = {(0, 3): "4년 뒤 같은 기계가 연기를 내며 주저앉음 — 기대가 무너지는 장면", (2, 1): "모라벡은 이름 한 줄, 그가 만든 수레가 주인공 — 의자가 놓인 방으로 들어옴",
           (2, 7): "관찰을 시소로: '시험' 쪽이 내려가 있던 시소가 '뒤집힌' 순간 아기 쪽으로 넘어감 — 그때 이름 한 줄",
           (6, 2): "'방식이 달라졌다'를 배경이 어두운 종이 → 밝은 종이로", (8, 3): "반세기의 거리: 종이 체스 → 딥 블루 사이에 점선",
           (9, 1): "마지막 장면: 빨래를 개는 손과 반듯하게 갠 티셔츠 — 수백만 년의 연습"}


def scenes_mixed() -> list[dict]:
    secs = sentences()
    out, i = [], 0
    pending = None
    for sec, (a, b), typ, extra in PLAN:
        goal, bg, beats = S[sec]
        says = secs[sec][a:b]
        if typ == "stage":
            bb = []
            for k in range(a, b):
                why, act = beats[k]
                bb.append({"say": secs[sec][k], "why": WHY_FIX.get((sec, k), why), "act": FIX.get((sec, k), act)})
            if pending:   # 앞 절과 한 장면으로 이어 붙임 (8 → 9절)
                pending["beats"] += bb
                pending = None
                continue
            i += 1
            sc = {"id": i, "type": "stage", "goal": goal, "bg": BG[sec], "beats": bb}
            out.append(sc)
            if extra.get("merge_next"):
                pending = sc
            continue
        i += 1
        sc = {"id": i, "type": typ, **extra, "beats": [{"say": s} for s in says]}
        out.append(sc)
    return out
