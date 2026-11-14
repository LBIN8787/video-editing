"""호기심 채널 · 이야기형 시험작: '체스 챔피언을 이긴 AI는 왜 빨래를 못 갤까?' (모라벡의 역설)
2026-11-13 사용자: "호기심 채널은 이야기를 들려주듯 대본을 쓰고, 그 대본에 맞추어 애니메이션 효과를" (참고: 미주일기 XE-9raLLQTQ)

    python scripts/curiosity_story/make.py            → projects/20261113-curiosity-moravec (기획 문서)
    YTFLOW_TTS=edge python -m ytflow hybrid 20261113-curiosity-moravec    (초안 목소리. 최종은 채널 ElevenLabs)
그림판(story) 좌표는 3840×2160, cam = [가운데 x, 가운데 y, 확대(0.5=전체)]. ytflow/stages/story.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "projects" / "20261113-curiosity-moravec"
FULL = "full"


def S(id_, ch, beats, **kw):
    return {"id": id_, "type": "story", "chapter": ch, "beats": beats, **kw}


def B(say, *draw, **kw):
    return {"say": say, "draw": list(draw), **kw}


SCENES = [
    {"id": 1, "type": "intro", "chapter": 0, "series": "몰랐던 이유", "as_of": "AI 편",
     "title_lines": ["체스는 이기는데", "빨래는 왜 못 갤까?"], "agenda_beat": 2,
     "beats": [
         {"say": "안녕하세요. 누구나 아는 것의 아무도 몰랐던 이유, 몰랐던 이유입니다."},
         {"say": "오늘은 체스 이야기로 시작해서 빨래 이야기로 끝나는, 조금 이상한 AI 이야기입니다."},
         {"say": "끝까지 보시면, 오늘 저녁 빨래를 개는 손이 조금 달라 보이실 거예요. 그날의 체스판부터 가 보겠습니다."}]},

    # ---- 훅: 1997 뉴욕 체스판 → 2019 도쿄 빨래 로봇 (답은 숨김)
    S(2, 0, [
        B("1997년 5월 11일, 미국 뉴욕. 세계 체스 챔피언 가리 카스파로프가 체스판 앞에 앉아 있었습니다.",
          {"t": "1997년", "do": "stamp", "id": "d97", "text": "1997. 5. 11 · 뉴욕", "x": 700, "y": 540, "cam": [1000, 1000, 0.85]},
          {"t": "카스파로프", "do": "figure", "id": "k", "pose": "think", "x": 640, "y": 1000, "s": 460, "label": "카스파로프", "sub": "세계 체스 챔피언"},
          {"t": "체스판", "do": "draw", "id": "bd", "icon": "board", "x": 1200, "y": 1060, "s": 340}),
        B("상대는 IBM이 만든 슈퍼컴퓨터, 딥 블루. 마지막 여섯 번째 판에서, 카스파로프는 고작 열아홉 수 만에 자리에서 일어났습니다.",
          {"t": "딥", "do": "draw", "id": "db", "icon": "server", "x": 1760, "y": 1000, "s": 330, "label": "딥 블루 (IBM)"},
          {"t": "열아홉", "do": "count", "id": "n19", "value": "19수", "x": 1330, "y": 690, "fs": 160, "label": "마지막 판"},
          {"t": "일어났", "do": "note", "id": "lose", "text": "기권", "x": 330, "y": 1000, "fs": 90}),
        B("다음 날 신문들은, 기계가 세계 챔피언을 이겼다고 크게 실었습니다.",
          {"t": "신문", "do": "draw", "id": "np", "icon": "newspaper", "x": 2200, "y": 720, "s": 280, "cam": [1500, 1000, 0.8]},
          {"t": "이겼다", "do": "note", "id": "head", "text": "기계가 이겼다", "x": 2200, "y": 960, "fs": 70}),
        B("그런데 그로부터 이십 년이 넘게 지난 2019년, 일본 도쿄의 한 회사가 문을 닫습니다.",
          {"t": "2019년", "do": "stamp", "id": "d19", "text": "2019 · 도쿄", "x": 2950, "y": 560, "cam": [2950, 1000, 0.85]},
          {"t": "회사", "do": "draw", "id": "co", "icon": "building-2", "x": 2780, "y": 1030, "s": 320, "label": "한 로봇 회사"},
          {"t": "닫습니다", "do": "cross", "on": "co"}),
        B("그 회사가 만들던 건 체스 기계가 아니라, 빨래를 개는 로봇이었습니다.",
          {"t": "빨래를", "do": "draw", "id": "bot", "icon": "bot", "x": 3320, "y": 1060, "s": 320, "label": "빨래 개는 로봇"},
          {"t": "로봇", "do": "draw", "id": "sh", "icon": "shirt", "x": 3320, "y": 650, "s": 230}),
        B("체스 챔피언을 이긴 기계는 이미 있었는데, 왜 티셔츠 한 장 개는 일은 그렇게 어려웠을까요?",
          {"t": "챔피언", "do": "circle", "on": "bd", "cam": FULL, "pad": 50},
          {"t": "티셔츠", "do": "circle", "on": "sh", "pad": 50},
          {"t": "어려웠을까요", "do": "chip", "id": "q", "text": "체스는 이기는데, 빨래는 왜?", "x": 1920, "y": 1560, "fs": 100, "hl": True}),
    ]),
    {"id": 3, "type": "kinetic", "chapter": 0,
     "beats": [{"say": "체스는 이겼는데, 빨래는 왜 못 갰을까요? 오늘의 질문입니다.", "hit": ["빨래는", "왜"]}]},

    {"id": 4, "type": "chapter", "chapter": 1, "num": "1", "title": "한 살 아기보다 서툰 기계", "icon": "bot",
     "beats": [{"say": "이런 순서로 가 보겠습니다. 이 이상한 점을 처음 적은 사람, 쉬운 일이 더 어려운 이유, 그리고 로봇은 언제 빨래를 개 줄지요."},
               {"say": "첫 번째, 이 이상한 점을 처음 또렷하게 적은 사람의 이야기부터 해 보겠습니다."}]},
    S(5, 1, [
        B("1980년대 미국 카네기멜런 대학교. 로봇을 연구하던 한스 모라벡이라는 학자가 있었습니다.",
          {"t": "1980년대", "do": "stamp", "id": "d80", "text": "1980년대 · 카네기멜런대", "x": 900, "y": 600, "fs": 64, "cam": [1000, 1050, 0.9]},
          {"t": "한스", "do": "figure", "id": "m", "pose": "stand", "x": 640, "y": 1060, "s": 440, "label": "한스 모라벡", "sub": "로봇 연구자"}),
        B("그는 1988년에 낸 책에, 로봇을 만들며 겪은 이상한 일을 적었습니다.",
          {"t": "책에", "do": "draw", "id": "bk", "icon": "book", "x": 1360, "y": 1000, "s": 320, "label": "『마음의 아이들』(1988)", "lfs": 58}),
        B("컴퓨터가 지능 검사를 풀거나 체커 게임을 어른만큼 두게 만드는 건, 비교적 쉽다.",
          {"t": "지능", "do": "draw", "id": "cap", "icon": "graduation-cap", "x": 2050, "y": 760, "s": 250, "label": "지능 검사", "cam": [2650, 1050, 0.8]},
          {"t": "체커", "do": "draw", "id": "ck", "icon": "board", "x": 2500, "y": 760, "s": 220, "label": "체커 게임"},
          {"t": "쉽다", "do": "chip", "id": "easy", "text": "어른만큼 → 쉽다", "x": 2280, "y": 1250, "fs": 76}),
        B("그런데 한 살 아기만큼 보고 움직이게 만드는 건, 어렵거나 아예 불가능하다.",
          {"t": "아기", "do": "figure", "id": "baby", "pose": "baby", "x": 3250, "y": 820, "s": 360, "label": "한 살 아기"},
          {"t": "어렵거나", "do": "chip", "id": "hard", "text": "아기만큼 → 어렵다", "x": 3250, "y": 1250, "fs": 76, "tone": "dark"}),
        B("어른의 시험은 쉽고, 아기의 걸음마는 어렵다. 이 뒤집힌 이야기를 사람들은 '모라벡의 역설'이라고 부릅니다.",
          {"t": "어른의", "do": "check", "on": "easy", "cam": FULL},
          {"t": "걸음마", "do": "circle", "on": "baby", "pad": 40},
          {"t": "모라벡의", "do": "chip", "id": "mp", "text": "모라벡의 역설", "x": 1920, "y": 1660, "fs": 120, "hl": True}),
    ]),
    S(6, 1, [
        B("생각해 보면 우리도 그렇습니다. 빨래 더미에서 티셔츠 한 장을 집어 드는 데, 우리는 1초도 고민하지 않죠.",
          {"t": "빨래", "do": "draw", "id": "pile", "icon": "pile", "x": 620, "y": 720, "s": 400, "cam": [1000, 700, 0.9]},
          {"t": "집어", "do": "draw", "id": "hand", "icon": "hand", "x": 980, "y": 470, "s": 200},
          {"t": "1초", "do": "count", "id": "s1", "value": "1초", "x": 1550, "y": 680, "fs": 190, "label": "고민하는 시간"}),
        B("하지만 로봇의 눈에 구겨진 티셔츠는, 볼 때마다 모양이 다른 천 덩어리입니다.",
          {"t": "로봇", "do": "draw", "id": "rb", "icon": "bot", "x": 500, "y": 1440, "s": 280, "label": "로봇", "cam": [1100, 1500, 0.9]},
          {"t": "천", "do": "draw", "id": "cl", "icon": "cloth", "x": 1080, "y": 1440, "s": 320},
          {"t": "모양이", "do": "note", "id": "nm", "text": "볼 때마다 다른 모양", "x": 1080, "y": 1700, "fs": 62}),
        B("소매는 어디인지, 어디를 잡아야 하는지, 천이 미끄러지면 어떻게 할지. 하나하나 다 알아내야 합니다.",
          {"t": "소매는", "do": "chip", "id": "q1", "text": "소매는 어디?", "x": 1760, "y": 1250, "fs": 70, "cam": [1250, 1450, 0.9]},
          {"t": "잡아야", "do": "chip", "id": "q2", "text": "어디를 잡지?", "x": 1760, "y": 1470, "fs": 70},
          {"t": "미끄러지면", "do": "chip", "id": "q3", "text": "미끄러지면?", "x": 1760, "y": 1690, "fs": 70}),
        B("체스는 정반대입니다. 말은 서른두 개, 규칙은 정해져 있고, 판은 언제나 가로세로 여덟 칸이죠.",
          {"t": "체스는", "do": "draw", "id": "bd", "icon": "board", "x": 2760, "y": 900, "s": 500, "cam": [3000, 1000, 0.85]},
          {"t": "서른두", "do": "chip", "id": "c1", "text": "말 32개", "x": 3440, "y": 660, "fs": 74},
          {"t": "규칙은", "do": "chip", "id": "c2", "text": "규칙은 고정", "x": 3440, "y": 900, "fs": 74},
          {"t": "여덟", "do": "chip", "id": "c3", "text": "판은 늘 8×8", "x": 3440, "y": 1140, "fs": 74}),
        B("모양이 매번 다른 천과, 언제나 똑같은 판. 기계에게는 이 차이가 결정적이었습니다.",
          {"t": "천과", "do": "circle", "on": "cl", "cam": FULL, "pad": 40},
          {"t": "똑같은", "do": "circle", "on": "bd", "pad": 30, "color": "#2E7D4F"}),
    ]),
    {"id": 7, "type": "versus", "chapter": 1, "label": "IBM 딥 블루 소개(1997)에 흔히 인용되는 수치 · 비교는 비유",
     "left": {"value": "1초", "label": "사람: 티셔츠 한 장 집기", "icon": "user"},
     "right": {"value": "2억 수", "label": "딥 블루: 1초에 따지는 수", "icon": "cpu"},
     "beats": [{"say": "같은 1초. 사람은 그 1초 동안 티셔츠 한 장을 집어 듭니다."},
               {"say": "딥 블루는 1초에 약 2억 개의 수를 따졌다고 알려져 있죠. 그런데 기계에게 더 어려운 쪽은, 뜻밖에도 티셔츠입니다.",
                "question": "왜 티셔츠가 더 어려울까?"}]},

    {"id": 8, "type": "chapter", "chapter": 2, "num": "2", "title": "쉬운 일이 더 어려운 이유", "icon": "brain",
     "beats": [{"say": "두 번째, 왜 우리에게 쉬운 일이 기계에게는 더 어려울까요?"}]},
    S(9, 2, [
        B("모라벡은 그 답을 진화에서 찾았습니다.",
          {"t": "진화", "do": "line", "id": "tl", "from": [300, 1150], "to": [3540, 1150], "sw": 12, "dur": 1.4},
          {"t": "진화", "do": "note", "id": "old", "text": "아주 먼 옛날", "x": 520, "y": 1280, "fs": 62, "color": "#22304D", "delay": 0.4},
          {"t": "찾았습니다", "do": "note", "id": "now", "text": "오늘", "x": 3420, "y": 1280, "fs": 62, "color": "#22304D"}),
        B("보고, 잡고, 걷는 능력. 이건 우리 조상들이 아주 오랜 세월 살아남기 위해 갈고닦아 온 능력입니다.",
          {"t": "보고", "do": "draw", "id": "eye", "icon": "eye2", "x": 800, "y": 900, "s": 240, "label": "보기"},
          {"t": "잡고", "do": "draw", "id": "hd", "icon": "hand", "x": 1350, "y": 900, "s": 240, "label": "잡기"},
          {"t": "걷는", "do": "figure", "id": "wk", "pose": "walk", "x": 1900, "y": 880, "s": 300, "label": "걷기"},
          {"t": "오랜", "do": "arrow", "id": "ar", "from": [700, 1060], "to": [2200, 1060], "bend": -60, "color": "#2F5D8C", "sw": 9}),
        B("너무 오래, 너무 잘 다듬어져서, 우리는 그게 어려운 일이라는 것조차 느끼지 못합니다.",
          {"t": "느끼지", "do": "chip", "id": "nf", "text": "어려운 줄도 모른다", "x": 1350, "y": 470, "fs": 84, "hl": True}),
        B("반대로 체스나 계산은, 인류가 해 온 지 얼마 안 된 일입니다. 긴 진화의 시간에 비하면, 맨 끝의 한 점이죠.",
          {"t": "체스나", "do": "draw", "id": "cs", "icon": "chess", "x": 3150, "y": 860, "s": 260, "label": "체스·계산", "cam": [2700, 1000, 0.75]},
          {"t": "한", "do": "circle", "id": "dot", "at": [3420, 1150], "size": [40, 40], "pad": 40}),
        B("그래서 우리는 체스를 어렵다고 느끼지만, 기계에게는 오히려 쉽습니다. 우리가 어렵다고 느끼는 것과 실제로 어려운 것은, 다를 수 있다는 겁니다.",
          {"t": "어렵다고", "do": "chip", "id": "f1", "text": "어렵다고 느끼는 것", "x": 1250, "y": 1620, "fs": 80, "cam": FULL},
          {"t": "실제로", "do": "chip", "id": "f2", "text": "실제로 어려운 것", "x": 2650, "y": 1620, "fs": 80, "tone": "dark"},
          {"t": "다를", "do": "note", "id": "ne", "text": "≠", "x": 1960, "y": 1610, "fs": 160}),
    ]),
    {"id": 10, "type": "quote", "chapter": 2, "label": "Steven Pinker, The Language Instinct (1994)",
     "who": "스티븐 핑커", "role": "심리학자·언어학자, 『언어 본능』(1994)",
     "quote": "35년의 AI 연구가 준 가장 큰 교훈은, 어려운 문제는 쉽고 쉬운 문제는 어렵다는 것이다.",
     "keyword": "쉬운 문제는 어렵다", "note": "뒤집힌 난이도",
     "beats": [{"say": "1994년, 심리학자이자 언어학자인 스티븐 핑커는 이 이야기를 한 문장으로 정리했습니다."},
               {"say": "35년의 AI 연구가 준 가장 큰 교훈은, 어려운 문제는 쉽고, 쉬운 문제는 어렵다는 것이다.", "mark": True}]},

    {"id": 11, "type": "chapter", "chapter": 3, "num": "3", "title": "로봇은 언제 빨래를 갤까", "icon": "house",
     "beats": [{"say": "마지막 세 번째, 그럼 로봇은 언제쯤 우리 빨래를 개 줄까요?"}]},
    S(12, 3, [
        B("다시 2019년 일본으로 가 보겠습니다. 빨래 개는 로봇을 만들던 회사 세븐 드리머스는, 그해 4월 파산을 신청했습니다.",
          {"t": "2019년", "do": "stamp", "id": "d19", "text": "2019. 4 · 도쿄", "x": 820, "y": 560, "cam": [1000, 1000, 0.85]},
          {"t": "세븐", "do": "draw", "id": "co", "icon": "building-2", "x": 640, "y": 1010, "s": 360, "label": "세븐 드리머스"},
          {"t": "파산", "do": "cross", "on": "co"}),
        B("남은 빚은 약 2천만 달러, 그때 우리 돈으로 2백억 원이 넘었다고 알려졌습니다.",
          {"t": "2천만", "do": "count", "id": "debt", "value": "2천만 달러", "x": 1550, "y": 820, "fs": 160, "label": "남은 빚 (약 200억 원+)"}),
        B("그런데 요즘은 분위기가 조금 달라졌습니다. 2024년 10월, 미국의 한 스타트업이 건조기에서 빨래를 꺼내 개는 로봇 영상을 공개했거든요.",
          {"t": "2024년", "do": "stamp", "id": "d24", "text": "2024. 10 · 미국", "x": 2750, "y": 560, "cam": [2950, 1000, 0.85]},
          {"t": "빨래를", "do": "draw", "id": "sh", "icon": "shirt", "x": 3350, "y": 1000, "s": 280},
          {"t": "로봇", "do": "draw", "id": "rb", "icon": "bot", "x": 2500, "y": 1000, "s": 330, "label": "π0 (피지컬 인텔리전스)", "lfs": 54},
          {"t": "공개", "do": "arrow", "a": "rb", "b": "sh"}),
        B("규칙을 하나하나 짜 넣는 대신, 수많은 로봇 동작 기록을 보고 스스로 익히게 한 겁니다. 챗GPT가 엄청난 양의 글을 읽고 말을 배운 것처럼요.",
          {"t": "규칙을", "do": "chip", "id": "rule", "text": "규칙 하나하나", "x": 2350, "y": 1500, "fs": 76, "cam": [2950, 1300, 0.85]},
          {"t": "대신", "do": "cross", "on": "rule"},
          {"t": "기록을", "do": "draw", "id": "rec", "icon": "files", "x": 3150, "y": 1500, "s": 220, "label": "동작 기록", "lfs": 56},
          {"t": "익히게", "do": "arrow", "a": "rec", "b": "rb"},
          {"t": "챗GPT가", "do": "note", "id": "gpt", "text": "글로 말을 배운 챗GPT처럼", "x": 3450, "y": 1300, "fs": 56}),
        B("물론 아직은 연구실 이야기입니다. 집집마다 빨래 로봇이 들어오기까지는, 갈 길이 남아 있죠.",
          {"t": "연구실", "do": "cam", "cam": FULL},
          {"t": "집집마다", "do": "draw", "id": "hs", "icon": "house", "x": 1300, "y": 1500, "s": 240, "label": "우리 집은 아직"}),
    ]),
    S(13, 3, [
        B("이제 처음 질문으로 돌아가 보죠. 체스 챔피언을 이긴 기계는, 왜 티셔츠 한 장을 못 갰을까요?",
          {"t": "체스", "do": "draw", "id": "cs", "icon": "chess", "x": 1250, "y": 820, "s": 400},
          {"t": "티셔츠", "do": "draw", "id": "sh", "icon": "shirt", "x": 2600, "y": 820, "s": 400}),
        B("체스는 어려워 보였지만, 말과 규칙과 판이 정해진 세계였습니다.",
          {"t": "정해진", "do": "chip", "id": "w1", "text": "정해진 세계", "x": 1250, "y": 1330, "fs": 90},
          {"t": "세계였습니다", "do": "check", "on": "cs"}),
        B("빨래는 쉬워 보였지만, 우리 몸이 아주 오래 연습해 온, 정답 없는 세계였던 거죠.",
          {"t": "연습해", "do": "circle", "on": "sh", "pad": 50},
          {"t": "정답", "do": "chip", "id": "w2", "text": "정답 없는 세계", "x": 2600, "y": 1330, "fs": 90, "tone": "dark"}),
        B("그러니 오늘 저녁 빨래를 개실 때, 그 손이 해내는 일이 생각보다 대단하다는 걸 떠올려 보셔도 좋겠습니다.",
          {"t": "손이", "do": "draw", "id": "hd", "icon": "hand", "x": 1920, "y": 1560, "s": 230},
          {"t": "대단하다는", "do": "note", "id": "gr", "text": "생각보다 대단한 일", "x": 1920, "y": 1790, "fs": 70}),
    ]),
    {"id": 14, "type": "kinetic", "chapter": 3,
     "beats": [{"say": "기계에게 가장 어려운 일은, 우리가 너무 쉽게 해서 어려운 줄도 몰랐던 일이었습니다.", "hit": ["너무", "쉽게"]}]},
    S(15, 3, [
        B("오늘 몰랐던 이유는 여기까지입니다. 다음에도 누구나 아는 것의 숨은 이유를 이야기로 들려 드리겠습니다.",
          {"t": "오늘", "do": "chip", "id": "end", "text": "몰랐던 이유", "x": 1920, "y": 900, "fs": 170, "hl": True},
          {"t": "다음에도", "do": "note", "id": "nx", "text": "다음 이야기에서 만나요", "x": 1920, "y": 1250, "fs": 90}),
    ], credit="출처는 설명란에"),
]

SPEC = {
    "title": "체스 챔피언을 이긴 AI는 왜 빨래를 못 갤까?",
    "brand": "curiosity",
    "bg_mode": "single",
    "core_message": "기계에게 어려운 건 우리가 어렵다고 느끼는 일(체스)이 아니라, 너무 오래 연습해서 쉬운 줄 아는 일(보고·잡고·걷기)이다 — 모라벡의 역설.",
    "question": "체스 챔피언을 이긴 AI는 왜 빨래를 못 갤까?",
    "logic": ["1997년 딥 블루가 체스 챔피언을 이김 — 그런데 2019년 빨래 개는 로봇 회사는 파산",
              "모라벡(1988): 어른 수준의 시험은 쉽고, 한 살 아기의 보기·움직이기는 어렵다",
              "이유: 보고·잡고·걷는 능력은 아주 긴 진화로 다듬어져 우리가 어려운 줄도 모름, 체스·계산은 최근의 일",
              "체스는 정해진 세계, 빨래는 정답 없는 세계 → 요즘 로봇은 규칙 대신 경험(동작 기록)으로 배우기 시작"],
    "compare_to": [{"value": "19수", "to": "1997년 마지막 판에서 카스파로프가 기권할 때까지 둔 수"},
                   {"value": "1초", "to": "사람이 티셔츠 한 장을 집는 시간 ↔ 딥 블루가 1초에 따지는 약 2억 수"},
                   {"value": "약 2천만 달러", "to": "빨래 로봇 회사가 남긴 빚 (그때 약 200억 원 넘음)"}],
    "analogies": [{"a": "구겨진 티셔츠", "b": "볼 때마다 모양이 다른 천 덩어리 (로봇의 눈)"},
                  {"a": "체스판", "b": "말 32개·규칙 고정·늘 8×8 인 정해진 세계"},
                  {"a": "로봇이 동작 기록으로 배우기", "b": "챗GPT가 엄청난 양의 글로 말을 배운 것"}],
    "past_cases": [{"case": "1997년 딥 블루 대 카스파로프 6국 (19수 만에 기권)", "lesson": "어른에게 어려운 일은 기계에게 먼저 풀렸다"},
                   {"case": "2019년 4월 빨래 로봇 회사 세븐 드리머스 파산", "lesson": "아기도 하는 일(천 다루기)이 기계에게는 더 어려웠다"}],
    "glossary": [{"term": "모라벡의 역설", "plain": "사람에게 어려운 일(계산·체스)은 기계에게 쉽고, 사람에게 쉬운 일(보기·잡기·걷기)은 기계에게 어렵다는 관찰"},
                 {"term": "딥 블루", "plain": "IBM이 만든 체스 전용 슈퍼컴퓨터 (1997년 세계 챔피언에게 승리)"},
                 {"term": "π0 (파이 제로)", "plain": "미국 스타트업 피지컬 인텔리전스가 2024년 10월 공개한 로봇 동작 AI"}],
    "scenes": SCENES,
    "package": {
        "title": "체스 챔피언을 이긴 AI는 왜 빨래를 못 갤까? | 모라벡의 역설",
        "title_options": ["체스 챔피언을 이긴 AI는 왜 빨래를 못 갤까?",
                          "19수 만에 챔피언을 이긴 기계, 티셔츠 한 장 앞에서 멈췄다",
                          "AI에게 어려운 건 체스가 아니라 빨래였다"],
        "title_why": ["훅의 틈(gap) 그대로 — 질문형 (manual/04 §0-3 ①)",
                      "훅의 장면·숫자(1997년 6국 19수) — 장면·숫자형 ②",
                      "상식 깨기형 ③ — '어려운 건 체스'라는 통념을 뒤집음, 답(진화)은 숨김"],
        "thumbnails": [   # layout board v2: 종이 + 실제 사진 폴라로이드 + 스티커 + 큰 글씨 (영상과 같은 재료, docs/26)
            {"id": "A", "name": "체스 vs 빨래 (질문형)", "layout": "board", "top": "몰랐던 이유 · AI 편",
             "lines": ["체스는 이기는데", "빨래는 왜?"], "hl": ["빨래는"], "size": 128, "text_y": 280, "text_w": 640,
             "photos": [{"file": "projects/20261113-curiosity-moravec/04_assets/story/chess.jpg", "x": 880, "y": 230, "w": 300, "h": 200, "rot": -4, "caption": "체스"},
                        {"file": "projects/20261113-curiosity-moravec/04_assets/story/laundry.jpg", "x": 1090, "y": 470, "w": 290, "h": 200, "rot": 3, "caption": "빨래", "focus": [0.62, 0.5]}],
             "marks": [{"type": "circle", "box": [920, 330, 1260, 620]}],
             "why": ["두 장면(체스·빨래) 대비 하나로 '어? 왜?' — 제목 ①과 짝", "영상과 같은 사진·폴라로이드"]},
            {"id": "B", "name": "19수 장면 (숫자형)", "layout": "board", "top": "1997. 5. 11 뉴욕",
             "lines": ["19수 만에 이긴 기계", "티셔츠 앞에서 멈췄다"], "hl": ["멈췄다"], "size": 104, "text_y": 290, "text_w": 700,
             "photos": [{"file": "projects/20261113-curiosity-moravec/04_assets/story/kasparov.jpg", "x": 880, "y": 280, "w": 230, "h": 270, "rot": -5, "caption": "카스파로프", "focus": [0.5, 0.25]},
                        {"file": "projects/20261113-curiosity-moravec/04_assets/story/deepblue.jpg", "x": 1120, "y": 330, "w": 210, "h": 270, "rot": 4, "caption": "딥 블루"}],
             "marks": [{"type": "stamp", "text": "19수 · 기권", "at": [900, 560], "size": 50, "rot": -9}],
             "why": ["훅의 숫자(19수) — 제목 ②와 짝", "실제 인물 사진(CC BY 4.0) + 딥 블루(CC BY 2.0)"]},
            {"id": "C", "name": "상식 깨기", "layout": "board", "top": "모라벡의 역설",
             "lines": ["AI에게 어려운 건", "체스가 아니라 빨래"], "hl": ["빨래"], "size": 112, "text_y": 290, "text_w": 700,
             "photos": [{"file": "projects/20261113-curiosity-moravec/04_assets/story/laundry.jpg", "x": 1000, "y": 300, "w": 360, "h": 250, "rot": -3, "caption": "빨래 개는 손 (1917)", "focus": [0.62, 0.5]}],
             "drawings": [{"sticker": True, "icon": "bot", "x": 1130, "y": 540, "s": 170}],
             "marks": [],
             "why": ["통념('어려운 건 체스')을 뒤집기 — 제목 ③과 짝", "옛 사진(1917) + 로봇 스티커"]},
        ]},
}

TOPIC = {
    "brand": "curiosity", "line": "ch-knowledge", "series": "몰랐던 이유",
    "desire": "AI가 체스·바둑은 이기는데 집안일 로봇은 왜 아직 없는지 궁금하다",
    "trigger": "집안일 로봇 영상(빨래 개기)이 계속 화제 — 2024년 10월 π0 공개 이후 '로봇은 언제 빨래를 개 주나' 질문 증가",
    "why_now": "AI가 글·그림은 잘하는데 몸 쓰는 일은 왜 늦는지 — 로봇 AI 경쟁이 시작된 지금 알면 뉴스가 읽힌다",
    "viewer_question": "체스 챔피언을 이긴 AI는 왜 빨래를 못 갤까?",
    "question_type": "행동의 이유", "mood": ["차분", "과거", "미래"],
    "topic": "모라벡의 역설: 1997 딥 블루 · 1988 모라벡 『마음의 아이들』 · 1994 핑커 · 2019 빨래 로봇 회사 파산 · 2024 π0",
    "our_angle": "'AI는 어려운 걸 못 한다'는 통념 대신 '우리가 쉽다고 느끼는 게 기계에겐 어렵다' — 체스와 빨래 두 장면으로",
    "hook": {"type": "장면", "line": "1997년 5월 11일 미국 뉴욕, 세계 체스 챔피언 카스파로프가 체스판 앞에서 기계에게 졌습니다.",
             "gap": "체스 챔피언을 이긴 기계는 왜 티셔츠 한 장을 못 갰을까?", "withheld": "답(진화가 다듬은 능력)은 2장에서", "payoff_scene": 9},
    "driver": {"type": "각도", "why": "AI 소재 + 일상(빨래) 반전", "angle": "어려움의 기준이 거꾸로"},
    "score": {"desire": 3, "clarity": 3, "timeliness": 2, "demand": 2, "visuals": 2, "angle": 3},
    "demand_evidence": [{"kind": "search", "detail": "'빨래 개는 로봇' '모라벡의 역설' 검색·영상 다수", "url": "https://news.google.com/search?q=%EB%AA%A8%EB%9D%BC%EB%B2%A1%EC%9D%98%20%EC%97%AD%EC%84%A4"}],
    "visual_sources": ["직접 그린 그림판 (막대 인물·선 아이콘 Lucide ISC)", "사진 없음 — 실존 인물은 막대 인물 + 이름표"],
    "candidates": [{"topic": "체스 챔피언을 이긴 AI는 왜 빨래를 못 갤까?", "total": 15, "why_not": "선택"},
                   {"topic": "로봇은 왜 아직 계단을 잘 못 오를까?", "total": 11, "why_not": "같은 역설 — 이번 편에 녹임"},
                   {"topic": "AI는 왜 손가락을 이상하게 그릴까?", "total": 12, "why_not": "출처 정리 더 필요"}],
}

FACTS = """# 팩트시트 — 체스 챔피언을 이긴 AI는 왜 빨래를 못 갤까 (2026-11-13 확인)

| # | 사실 | 상태 | 출처 |
|---|---|---|---|
| F1 | 1997-05-11 뉴욕, 딥 블루와의 재대결 6국에서 카스파로프가 19수 만에 기권, 경기 3.5-2.5로 딥 블루 승 — 다판 승부에서 현역 세계 챔피언이 컴퓨터에 진 첫 사례 | ✅ | https://en.wikipedia.org/wiki/Deep_Blue_versus_Kasparov,_1997,_Game_6 · https://www.history.com/this-day-in-history/may-11/deep-blue-defeats-garry-kasparov-in-chess-match |
| F2 | 딥 블루는 1초에 약 2억 개의 체스 국면을 계산 (흔히 인용되는 수치 — 대본에서 '알려져 있다'로) | ✅(인용) | https://historyofinformation.com/detail.php?entryid=1372 |
| F3 | 모라벡 『Mind Children』(1988, p.15 무렵): 컴퓨터가 지능 검사·체커에서 어른 수준을 보이게 하는 건 비교적 쉽고, 한 살 아기의 지각·이동 능력을 주는 건 어렵거나 불가능 | ✅ | https://en.wikipedia.org/wiki/Moravec%27s_paradox |
| F4 | 모라벡의 설명: 사람의 능력은 자연선택이 설계한 생물학적 기계로 구현 — 오래된 감각·운동 능력일수록 더 다듬어짐 | ✅ | 같은 문서 |
| F5 | 핑커 『The Language Instinct』(1994): "35년 AI 연구의 큰 교훈은 어려운 문제는 쉽고 쉬운 문제는 어렵다는 것" | ✅(2차 인용) | https://en.wikipedia.org/wiki/Moravec%27s_paradox |
| F6 | 빨래 개는 로봇 '런드로이드' 개발사 세븐 드리머스(도쿄), 2019-04-23 파산 신청, 부채 약 2천만 달러(테이코쿠 데이터뱅크) | ✅ | https://techcrunch.com/2019/04/23/the-company-behind-laundroid-files-for-bankruptcy/ · https://en.wikipedia.org/wiki/Laundroid · https://www.japantimes.co.jp/news/2019/04/24/business/corporate-business/tokyo-based-developer-laundry-folding-robot-files-bankruptcy |
| F7 | 2024년 10월 피지컬 인텔리전스 π0 공개: 건조기에서 빨래를 꺼내 개는 시연, 7종 로봇·68개 작업 데이터로 사전학습 | ✅ | https://physicalintelligence.company/blog/pi0 · https://arxiv.org/abs/2410.24164 |
| F8 | 2천만 달러 ≈ 2019년 4월 환율(약 1,140원) 기준 약 228억 원 → 대본 '2백억 원이 넘었다' | ✅(계산) | 한국은행 환율 (2019-04) |

## 쓰지 않는 것
- 런드로이드가 셔츠 한 장 개는 데 걸린 시간 (보도마다 다르고 측정값 없음) · 가격 (1천 달러/1만6천 달러로 엇갈림)
- 모라벡의 '10억 년의 경험' 문장 직접 인용 (원문 페이지 미확인 → '아주 오랜 세월'로)
- 요즘 집안일 로봇 출시 시기 전망 (확인된 일정 없음)
"""


def apply_v2():   # V2 apply: 그림 재료 v2 (scripts/curiosity_story/v2.py) — 대본은 그대로
    import importlib.util
    spec_ = importlib.util.spec_from_file_location("v3", Path(__file__).with_name("v3.py"))   # v3: AI 그림 조각 (2026-11-14), v2 는 사진·스티커판
    v2 = importlib.util.module_from_spec(spec_)
    spec_.loader.exec_module(v2)
    for sc in SCENES:
        if sc["id"] in v2.V3:
            for b, draws in zip(sc["beats"], v2.V3[sc["id"]]):
                b["draw"] = draws
            sc.pop("credit", None)


def apply_v4():   # v4: 애니메이션 무대 (stage) — 2026-11-14 기각 반영, 제작 의도 02_script/intent.md, manual/04 §0-5
    import importlib.util
    spec_ = importlib.util.spec_from_file_location("v4", Path(__file__).with_name("v4.py"))
    v4 = importlib.util.module_from_spec(spec_)
    spec_.loader.exec_module(v4)
    v4.apply(SCENES)


def main():
    apply_v2()
    apply_v4()
    for d in ("01_research", "02_script", "05_edit"):
        (P / d).mkdir(parents=True, exist_ok=True)
    (P / "01_research" / "topic_brief.json").write_text(json.dumps(TOPIC, ensure_ascii=False, indent=1), encoding="utf-8")
    (P / "01_research" / "factsheet.md").write_text(FACTS, encoding="utf-8")
    (P / "02_script" / "hybrid.json").write_text(json.dumps(SPEC, ensure_ascii=False, indent=1), encoding="utf-8")
    (P / "edit.yaml").write_text("# 호기심 채널 · 이야기형 (story-board) 시험작 — 2026-11-13\nedit:\n  style: hybrid\n  style_ref: hybrid\n  family: source\n"
                                 "  skin: paper-sketch\nchannel: ch-knowledge\nformat: longform\n", encoding="utf-8")
    st = P / "state.json"
    if not st.exists():
        st.write_text(json.dumps({"name": P.name, "created": "2026-11-13T18:00:00", "done": ["script"]}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(P)


if __name__ == "__main__":
    main()
