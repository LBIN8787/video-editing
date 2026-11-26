"""2026-11-25 정적 보완 — 메모리 1부 치킨게임 (사용자: "나머지 영상들도 작업하세요").
고운 측정으로 8초 넘게 그대로인 곳에 말하는 순간 상자·그림을 붙임 (docs/68 E1·E3). 새 사실 없음: 모두 대본에 있는 값.
자리는 지난 렌더의 장면 끝 프레임에서 빈 곳을 골랐음 (겹침은 렌더 뒤 overlap_qa 로 다시 확인).
python scripts/fix_static_memory_chicken.py  (다시 돌려도 같은 결과)"""
import json
from pathlib import Path

F = Path(__file__).resolve().parent.parent / "projects" / "20261122-market-deep-memory-chicken" / "02_script" / "hybrid.json"
INK = "#3A3F48"
d = json.loads(F.read_text(encoding="utf-8"))
S = {s["id"]: s for s in d["scenes"]}


def say(sid):
    return " ".join(b["say"] for b in S[sid]["beats"])


def C(t, id_, value, label, x, y, w=480, h=110, fs=28):
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


def add_pics(sid, new, order):
    """기존 그림은 그대로 두고 새 그림을 끼움 (order: 그림의 t 순서)."""
    have = {p["t"]: p for p in S[sid]["pics"]}
    for p in new:
        assert p["t"] in say(sid), (sid, p["t"])
        have[p["t"]] = p
    S[sid]["pics"] = [have[t] for t in order]


motion(2, 0, C("절반밖에", "half", "주문의 절반만 공급", "공급 부족", 1550, 560))
motion(2, 1, C("AI 거품", "bub", "매체: 'AI 거품' 기사", "폭락을 다룬 방식", 1550, 720))
motion(4, 0, C("2027년에야", "f27", "새 공장 공간 = 2027년", "TrendForce", 1650, 700))
motion(8, 0, C("훨씬 가파릅니다", "now", "이번: 1년에 약 4배", "그때는 두 배 넘게", 1600, 700))
motion(13, 1, C("절반을", "half2", "코스피의 절반+", "삼성전자 + SK하이닉스 (6월 보도)", 330, 560))
add_pics(15, [stat("여섯 배", "trending-up", "6배+", "주가 −35%인데 P/E로는 (2015.7)"),
              stat("68%", "trending-up", "+68%", "2018.12: 이익 −75%인데 주가는")],
         ["2010년", "2015년", "여섯 배", "2018년 7월", "2018년 12월", "68%"])
motion(17, 2, C("4분의 1", "q4", "10% 남으면 → 25원", "가정", 1650, 450, 440))
motion(17, 3, C("압도적으로", "win", "① 1만 원 > ② 2,750원", "덜 파는 쪽이 낫다", 1650, 620, 440))
motion(19, 0, C("점유율과", "sh", "먼저 줄이면 → 점유율·고객 잃음", "버틴 쪽은 다음 투자", 280, 420, 400, 110, 24))
motion(19, 0, C("치킨 게임이라고", "ck", "= 치킨 게임", "다들 남이 먼저 줄이길 기다림", 280, 280, 400, 110, 24))
add_pics(21, [stat("얕아질", "trending-up", "얕은 하강?", "2023 큰 적자 → 감산이 더 빨리 (가설)"),
              stat("점유율을 지키겠다는", "trending-down", "깊은 하강", "'점유율 지키기' 말이 다시 나오면 (가설)")],
         ["마이크론과", "14.9조", "키몬다", "얕아질", "점유율을 지키겠다는"])
# 22: 핀(pins)이 장면 끝까지 남아 그림을 더하면 겹쳐 어지러움 (11-25 프레임 확인) → 그대로 둠
motion(25, 0, C("10%대 중반씩", "mu", "마이크론: 해마다 10%대 중반", "중기 비트 수요", 330, 300))
motion(25, 1, C("핸들을 2도만", "car", "핸들 2도 = 차선 이탈", "2~3년 뒤를 5%p 안으로 맞히기", 1640, 300, 440))
motion(26, 0, C("2026년과 27년", "proc", "2026~27년: 공정 전환으로 공급↑", "TrendForce", 1650, 300, 440, 110, 24))
motion(27, 0, C("절반으로", "cut", "SK하이닉스: 투자 절반으로", "지난 하강기", 280, 300, 360, 110, 24))
motion(27, 1, C("몇 달 만에", "fast", "수요는 몇 달, 공급은 1~2년", "속도 차이", 280, 440, 360, 110, 24))
# 31: 핀(pins)이 장면 끝까지 남아 그림을 더하면 겹쳐 어지러움 (11-25 프레임 확인) → 그대로 둠
# 32: 핀(pins)이 장면 끝까지 남아 그림을 더하면 겹쳐 어지러움 (11-25 프레임 확인) → 그대로 둠

# 21 — 핀 세 개가 위로 쌓여 제목 '누가 먼저 줄였나'를 가림(text_occluded) → 셋째(11월 마이크론)는 아래로
for it in S[21]["pics"][0]["items"]:
    if it.get("t") == "11월에":
        it["pos"] = "down"

F.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("memory-chicken ok")
