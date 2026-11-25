"""2026-11-25 정적 보완 — 메모리 2부 (사용자: "나머지 영상들도 작업하세요").
고운 측정으로 8초 넘게 그대로인 곳에 말하는 순간 상자·그림을 붙임 (docs/68 E1·E3). 새 사실 없음: 모두 대본에 있는 값.
자리는 지난 렌더의 장면 끝 프레임에서 빈 곳을 골랐음 (겹침은 렌더 뒤 overlap_qa 로 다시 확인).
python scripts/fix_static_memory_insight.py  (다시 돌려도 같은 결과)"""
import json
from pathlib import Path

F = Path(__file__).resolve().parent.parent / "projects" / "20261122-market-deep-memory-insight" / "02_script" / "hybrid.json"
INK, OK = "#3A3F48", "#2E7D4F"
d = json.loads(F.read_text(encoding="utf-8"))
S = {s["id"]: s for s in d["scenes"]}
B = [(790, 850, 430, 110, 24), (1230, 850, 430, 110, 24), (1670, 850, 430, 110, 24)]


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
    have = {p["t"]: p for p in S[sid].get("pics", [])}
    for p in new:
        assert p["t"] in say(sid), (sid, p["t"])
        have[p["t"]] = p
    S[sid]["pics"] = [have[t] for t in order]


# 4 — 1부의 세 도구: 그림 없던 체크리스트 → 줄은 짧게(원문은 label_full), 오른쪽에 문장마다 그림
sc = S[4]
for r, lab in zip(sc["rows"], ["① 몇 % 차이 → 값은 몇 배", "② 공장 2~3년 → 한꺼번에 닿는다", "③ HBM: 웨이퍼 3~4배"]):
    r.setdefault("label_full", r["label"])
    r["label"] = lab
sc["x"], sc["text_w"] = 150, 880
for b in sc["beats"]:
    if b.get("motion"):
        b["motion_off"] = b.pop("motion")
add_pics(4, [stat("이름 있는 사람들의", "search", "주장 뜯어보기", "1부의 원리를 도구로", INK),
             stat("첫째", "trending-up", "몇 배", "몇 %의 차이 → 값은 몇 배"),
             stat("둘째", "calendar", "2~3년", "공장 → 증설은 한꺼번에 시장에", INK),
             stat("셋째", "boxes", "3~4배", "HBM: 같은 용량에 웨이퍼")],
         ["이름 있는 사람들의", "첫째", "둘째", "셋째"])
# 8 — 최태원의 근거: 받침·어긋남을 하나씩
add_pics(8, [stat("마이크론은", "boxes", "절반~3분의 2", "마이크론: 핵심 고객 수요를 채우는 몫", OK),
             stat("3,900억", "banknote", "3,900억 달러", "엔비디아 공급 약정 — 대부분 메모리", OK),
             stat("오픈AI는", "trending-down", "2030년까지 적자", "돈 내는 쪽: 오픈AI 현금흐름 (보도)"),
             stat("캔터", "trending-down", "PC −10%", "캔터 가정: 비싼 메모리 → PC −10%, 폰 −5%"),
             stat("현물값은", "trending-down", "낸드 −20%", "한 달 현물값 D램 −5% · 낸드 −20%"),
             stat("회장이라는", "building", "파는 쪽", "최태원 = 메모리를 파는 쪽의 회장", INK)],
         ["받치는", "마이크론은", "3,900억", "오픈AI는", "캔터", "현물값은", "회장이라는"])
# 15 — 아리아의 근거, 걸리는 곳
add_pics(15, [stat("담합 소송", "search", "소송 중", "미국 소비자 담합 소송 — 판결 전", INK),
              stat("35에서 40%", "boxes", "35~40%", "클라우드 투자 중 메모리 몫"),
              stat("버는 동안만", "hourglass", "조건", "고객이 돈을 버는 동안만")],
         ["첫째", "둘째", "담합 소송", "셋째", "35에서 40%", "버는 동안만"])
# 16 — 젠슨 황 인용 (16.8초)
motion(16, 0, C("가장 큰 공급 병목", "bn", "가장 큰 병목 = 메모리", "젠슨 황 (5월)", *B[0]))
motion(16, 0, C("사서 쓰는 쪽", "buy", "사는 쪽의 말", "= 더 지어 달라는 요청", *B[1]))
# 19 — P/E 함정 (21.5·24.2·15.5초): 아래 빈 줄에
motion(19, 0, C("가장 낮아 보이고", "pk", "이익 꼭대기 = P/E 가장 낮음", "메모리는 거꾸로", 500, 860, 420, 110, 24))
motion(19, 2, C("주가가 먼저", "first", "2018: 이익보다 주가가 먼저", "9.95 → 8.53달러", 960, 860, 420, 110, 24))
motion(19, 3, C("예외도", "ex", "예외: 2018.12 2.6배 → +68%", "한 회사 · 61번의 기록", 1420, 860, 420, 110, 24))
# 20 — 속도
motion(20, 1, C("0 아래로", "zero", "속도가 0 아래로 → 재고 먼저", "신중한 쪽", 1600, 420, 440, 110, 24))
motion(20, 1, C("2018년처럼", "s18", "2018: 주가는 속도에 먼저", "이익보다", 1600, 560, 440, 110, 24))
# 21 — 경계현
motion(21, 0, C("먼저 생산을 줄인다는", "pre", "전제: 손해 크면 먼저 줄인다", "치킨 게임", 1720, 300, 340, 110, 22))
motion(21, 1, C("2027년 하반기에서", "when", "2027 하반기~2028 상반기 값↓", "경계현 (보도)", 1700, 520, 380, 110, 22))
# 22 — 낸드
motion(22, 0, C("4에서 5% 모자란다고", "prev", "7월: 올해 4~5% 모자람", "TrendForce", 450, 700))
motion(22, 1, C("30%대 하락", "kw", "키움: 범용 D램 30%대 하락", "내년", 450, 840))
motion(22, 1, C("HBM은 이미", "lock", "HBM은 이미 계약으로", "낸드·범용과 다름", 1000, 700, 400, 110, 24))
# 26 — 둘 다 맞을 수 있다
motion(26, 0, C("협상을 이미", "hbm", "SK하이닉스: 내년 HBM 협상 끝", "장기 계약", 960, 420, 420, 110, 24))
motion(26, 1, C("함께 맞을", "both", "2030년까지 + 2027년 말부터", "함께 맞을 수 있다", 960, 560, 420, 110, 24))
motion(26, 1, C("먼저 꺾이고", "kk", "현물·낸드 계약가가 먼저 꺾임", "짧은 계약 쪽", 1480, 860, 480, 110, 24))
# 28 은 등불판(lamps)이 장면 끝까지 남는 구조라 그림을 더하면 겹침 (11-25 overlap_qa) → 그대로 둠

F.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("memory-insight ok")
