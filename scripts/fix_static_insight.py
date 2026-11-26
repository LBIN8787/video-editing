"""2026-11-25 정적 보완 — 엔비디아 2부 (사용자: "나머지 영상들도 작업하세요").
고운 측정(320×180, 자막 줄 제외)으로 6초 넘게 그대로인 곳을 말하는 순간 바뀌게 (docs/68 E1·E3).
새 사실 없음: 모두 대본에 있는 값. 인용 장면 상자는 인용 카드 아래 한 줄(오른쪽은 카드와 겹침, 11-25 젠슨 복귀 편).
python scripts/fix_static_insight.py  (다시 돌려도 같은 결과)"""
import json
from pathlib import Path

F = Path(__file__).resolve().parent.parent / "projects" / "20261122-market-deep-nvidia-insight" / "02_script" / "hybrid.json"
INK, OK = "#3A3F48", "#2E7D4F"
d = json.loads(F.read_text(encoding="utf-8"))
S = {s["id"]: s for s in d["scenes"]}
B = [(790, 850, 430, 110, 24), (1230, 850, 430, 110, 24), (1670, 850, 430, 110, 24)]


def say(sid):
    return " ".join(b["say"] for b in S[sid]["beats"])


def C(t, id_, value, label, x, y, w=560, h=110, fs=28):
    return {"t": t, "do": "count", "id": id_, "value": value, "label": label, "x": x, "y": y, "w": w, "h": h, "fs": fs}


def motion(sid, bi, m):
    b = S[sid]["beats"][bi]
    assert m["t"] in b["say"], (sid, m["t"])
    ms = b.setdefault("motion", [])
    old = [x for x in ms if x.get("id") == m["id"]]
    if old:
        old[0].update(m)
    else:
        ms.append(m)


def stat(t, icon, value, sub, color=None):
    p = {"t": t, "kind": "stat", "icon": icon, "value": value, "sub": sub}
    if color:
        p["color"] = color
    return p


def pics(sid, ps):
    for p in ps:
        assert p["t"] in say(sid), (sid, p["t"])
    S[sid]["pics"] = ps


# 2 — '8년 vs 3년' 뒤로 긴 문장 (14.5초): 사임·복귀, 채노스의 3년
motion(2, 0, C("물러났다가", "ceo", "11.11 사임 → 11.23 복귀", "젠슨 황 · 12일 만", *B[0]))
motion(2, 0, C("3년이라고", "ch3", "짐 채노스: 3년", "공매도 투자자", *B[1]))
# 5 — 1부의 세 도구 (18.5초): 줄마다 그림
pics(5, [stat("첫째", "link", "위험이 겹친다", "파는 쪽이 돈을 대면 — 매출은 진짜여도", INK),
         stat("둘째", "hourglass", "몇 년 뒤", "위험이 쌓이는 곳 — 오늘이 아니라 약속"),
         stat("셋째", "trending-down", "약해지는 곳", "받는 속도 · 회사 값 · 담보 가치"),
         *[p for p in S[5]["pics"] if p.get("t") == "GPU가"],
         stat("연준과", "landmark", "어디까지 번지나", "연준·금리 = 숫자가 틀렸을 때의 손실")])
# 8 — 받치는 숫자: 말하는 순간에 (10.8초 ×2)
S[8]["beats"][1]["at"] = {"e1": "2.88달러", "e2": "30에서 50%"}
for k, v in S[8]["beats"][1]["at"].items():
    assert v in S[8]["beats"][1]["say"], v
# 11 — 어긋나는 숫자 넷
pics(11, [*[p for p in S[11]["pics"] if p.get("t") == "받치는"],
          stat("810억", "banknote", "810억 달러", "못 받은 칩값 · 회수 64일"),
          stat("18억", "trending-down", "18억 달러", "한 분기 투자 손상"),
          stat("20% 넘게", "trending-down", "20%+ 하락", "네오클라우드 주가 (보도)"),
          stat("함께 맞을", "link", "둘 다 맞다", "고객을 잃지 않음 + 고객 돈 사정 빡빡", INK)])
# 15 — 집행 0
motion(15, 0, C("한 푼도", "z0", "집행 0달러", "월가 5,000억 달러 약속 (8월)", 1500, 720, 480))
# 17 — 채노스 (30.5초)
motion(17, 0, C("1년 반마다", "cy", "새 칩은 1년 반마다", "채노스의 근거", *B[0]))
motion(17, 0, C("3분의 1씩을", "th", "3년이면 해마다 1/3씩 비용", "채노스의 셈", *B[1]))
motion(17, 1, C("되물었습니다", "why", "'그럼 왜 직접 안 빌려주나'", "채노스 (9월) · 젠슨 황에게", *B[2]))
# 18 — 버리 (19.5초): 기존 4~6년 상자는 카드와 겹치는 자리 → 아래 줄로
motion(18, 0, C("늘려 잡아", "up", "수명 ↑ → 해마다 비용 ↓", "버리의 주장", *B[0]))
motion(18, 0, C("커 보인다고", "big", "→ 이익이 커 보임", "보도로 전해진 주장", *B[1]))
motion(18, 0, C("4년에서 6년", "life", "회사들: 4~6년이 합당", "반박", *B[2]))
# 19 — 6년·8년을 따로
motion(19, 1, C("13.3억", "d6", "6년: 흑자 13.3억", "비용 16.7억", 1500, 440, 560))
motion(19, 1, C("17.5억", "d8", "8년: 흑자 17.5억", "비용 12.5억", 1500, 580, 560))
# 20 — 매체 프레임
motion(20, 0, C("야후 파이낸스는", "yh", "야후: 6,700억, 늦게 낸다", "해외 · 무게", *B[0]))
motion(20, 0, C("CNN은", "cnn", "CNN: 젠슨 황이라는 사람", "해외 · 초점", *B[1]))
motion(20, 0, C("마켓잉크는", "mi", "마켓잉크: 질문은 보증에", "국내", *B[2]))
# 23 — 31% 의 출발점
motion(23, 0, C("6% 미만에서", "from", "2023년 6% 미만 → 올해 약 31%", "우량 회사채 중 AI 컴퓨팅 빚", 450, 740, 480))
# 24 — 연준 의사록 (16.2초)
motion(24, 0, C("장부 밖", "off", "장부 밖 임대 약속", "연준 의사록 (11.18)", *B[0]))
motion(24, 0, C("실망스러우면", "if", "조건: 수익이 실망스러우면", "→ 손실을 키울 수 있다", *B[1]))
motion(24, 1, C("몇 년을", "yrs", "그 수익 = GPU가 몇 년 버나", "앞의 숫자", *B[2]))
# 25·29 는 등불판(lamps)이 장면 끝까지 남는 구조라 그림을 더하면 겹침 (11-25 overlap_qa) → 그대로 둠
F.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("insight ok")
