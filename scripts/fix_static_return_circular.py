"""2026-11-25 사용자: "정적인 부분을 보완하는 영상을 업로드하려고 합니다" → "네 수정하세요"
젠슨 복귀 편·엔비디아 1부 순환금융 — 화면이 오래 멈춘 곳(hold_measure 6초+, check G4 '말은 많은데 화면이 멈춘 박자')을
말하는 순간 바뀌게. 그림은 문장의 명사·숫자 그 자체(docs/68 E1·E3·E4), 새 사실은 넣지 않음(모두 대본·팩트시트에 있는 값).
python scripts/fix_static_return_circular.py  (다시 돌려도 같은 결과)"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "projects"


def load(p):
    f = ROOT / p / "02_script" / "hybrid.json"
    return f, json.loads(f.read_text(encoding="utf-8"))


def sc_(doc, sid):
    return next(s for s in doc["scenes"] if s["id"] == sid)


def add_motion(beat, m):
    ms = beat.setdefault("motion", [])
    old = [x for x in ms if x.get("id") == m["id"]]
    assert m["t"] in beat["say"], (m["t"], beat["say"][:40])
    if old:
        old[0].update(m)
    else:
        ms.append(m)


def C(t, id_, value, label, x, y, w=560, h=110, fs=28):
    return {"t": t, "do": "count", "id": id_, "value": value, "label": label, "x": x, "y": y, "w": w, "h": h, "fs": fs}


# ── 젠슨 복귀 ─────────────────────────────────────────────────────────────
f, d = load("20261124-market-deep-nvidia-return")
s = sc_(d, 2)   # 6.7초 정지: '5일' 상자 뒤로 긴 문장 — 결의 내용·11일을 말하는 순간 붙임
add_motion(s["beats"][0], C("만장일치로", "un", "만장일치 — CEO·사장·이사 복귀", "이사회 결의 (8-K, 11.22)", 1500, 540))
add_motion(s["beats"][0], C("11일", "d11", "사임 11.11 → 결의 11.22", "11일 만", 1500, 380))
s = sc_(d, 13)  # G4 13-2: '95%' 를 말하는데 화면이 그대로
add_motion(s["beats"][1], C("95%", "r95", "사임한 날 종가의 95%", "165.05 ÷ 173.73 (11.11 종가)", 1500, 460))
s = sc_(d, 15)  # 10.5초 정지(가장 긴 곳): 숫자 카드 → 실제 종가 선 위에서 계산 (docs/68 §6 pricewalk, E2·E4)
if s["type"] != "pricewalk":
    s.setdefault("was", {k: s[k] for k in ("type", "small", "value") if k in s})
    for k in ("small", "value"):
        s.pop(k, None)
    s.update(type="pricewalk", ticker="NVDA", period="3mo", **{"from": "2026-10-01"}, to="2026-11-23", lo=100, hi=250,
             title="엔비디아 주가 — 하루에 되찾은 것과 남은 것",
             label="종가: 야후 파이낸스 · 주식 수: 엔비디아 3분기 CFO 코멘터리 희석 가중평균 241.86억 주 · 계산은 11.23 종가 기준")
    for b in s["beats"]:
        b.pop("motion", None)
    s["beats"][0]["do"] = [
        {"line": "2026-11-20", "t": "계산해", "dur": 2.0},
        {"dot": "2026-11-20", "label": "11/20 (금)|125.53", "side": "below", "t": "계산해"},
        {"seg": ["2026-11-20", "2026-11-23"], "tone": "up", "t": "40달러가", "group": "b0"},
        {"dot": "2026-11-23", "label": "", "t": "올랐고", "color": "#4FCB86"},
        {"bracket": [125.53, 165.05], "tone": "up", "label": "+39.52달러", "sub": "125.53 → 165.05 · +31.5%", "t": "올랐고", "group": "b0"},
        {"calc": "39.52달러 × 241.86억 주", "value": "≈ 9,560억 달러", "tag": "거의 1조 달러 — 아이브스의 계산과 비슷", "t": "242억"},
        {"calcval": True, "t": "9,560억"},
        {"calctag": True, "t": "1조"}]
    s["beats"][1]["do"] = [
        {"clear": "calc", "t": "그런데"},
        {"dim": "b0", "t": "그래프가"},
        {"level": "2026-11-11", "label": "사임한 날 173.73", "t": "사임한"},
        {"dot": "2026-10-06", "label": "10/6 최고가|239.24", "side": "above", "t": "10월"},
        {"bracket": [165.05, 239.24], "tone": "down", "label": "아직 −31%", "sub": "165.05 / 239.24", "t": "31%"},
        {"seg": ["2026-11-11", "2026-11-20"], "tone": "down", "label": "사임 뒤에 빠진 몫", "t": "사임 뒤에"},
        {"seg": ["2026-11-20", "2026-11-23"], "tone": "up", "t": "되돌린"},
        {"seg": ["2026-10-06", "2026-11-11"], "tone": "down", "t": "전부가"}]
    s["beats"][2]["do"] = [
        {"note": "남은 의심 ① 1,180억 달러 보증 — 순환금융", "y": 236, "t": "1,180억"},
        {"note": "② SEC 회계 조사 보도", "y": 276, "t": "SEC"},
        {"note": "③ 금리", "y": 316, "t": "금리입니다"}]
f.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("return ok")

# ── 엔비디아 1부 ─────────────────────────────────────────────────────────
f, d = load("20261122-market-deep-nvidia-circular")
s = sc_(d, 2)   # 8.8초 정지: 순환금융의 세 고리를 말하는데 숫자 하나만
b = s["beats"][1]
add_motion(b, C("보증하고", "r1", "① 못 내면 대신 갚는다", "보증", 320, 880, 400, 120, 28))
add_motion(b, C("지분을", "r2", "② 사는 회사의 지분을 산다", "지분 투자", 740, 880, 400, 120, 28))
add_motion(b, C("빌려 씁니다", "r3", "③ 남는 서버를 다시 빌린다", "임대 약정", 1160, 880, 400, 120, 28))
s = sc_(d, 7)   # 7.8초 정지: '빅테크'·'무너지면'을 말하는 동안 그대로
s["els"].setdefault("bt", {"kind": "text", "x": 500, "y": 790, "text": "고객의 큰 몫 = 현금 많은 빅테크", "size": 34})
s["els"].setdefault("ord", {"kind": "text", "x": 1420, "y": 790, "text": "+ 그 돈에 기댄 주문도 사라짐", "size": 34})
b0, b1 = s["beats"]
if "bt" not in b0["do"]:
    b0["do"].append("bt"); b0["at"]["bt"] = "빅테크"
if "ord" not in b1["do"]:
    b1["do"].append("ord"); b1["at"]["ord"] = "주문도"
b1["at"]["a2"] = "무너지면"
s = sc_(d, 9)   # 8.3초 정지: 매출 기준선·메모 문장에서 화면이 그대로
b = s["beats"][1]
for m in b.get("motion") or []:
    if m.get("id") == "m25":
        m["y"] = 620
add_motion(b, C("1,158억", "rev", "한 분기 매출 1,158억 달러", "견줄 기준 (3분기)", 1560, 460, 480, 120, 32))
if not any(m.get("do") == "pulse" for m in b["motion"]):
    assert "달라졌습니다" in b["say"]
    b["motion"].append({"t": "달라졌습니다", "do": "pulse", "on": "nm"})
s = sc_(d, 12)  # 7.6초 정지: 루슨트 약정이 늘고 줄어드는 과정
add_motion(s["beats"][1], C("파산했습니다", "wsx", "윈스타 파산", "빌린 돈으로 장비를 산 고객", 1640, 700, 440, 120, 32))
add_motion(s["beats"][1], C("22억", "l22", "고객 대출 약정 84억 → 22억", "루슨트", 1640, 860, 440, 120, 32))
s = sc_(d, 18)  # 7.3초 정지: '메모리 회사들의' 가 대사에 없어 마지막 카드가 늦게 뜸 → 말하는 순간에
s["beats"][0]["at"] = {"a1": "2,790억", "mem": "메모리 구매", "kr": "SK하이닉스"}
for k, v in s["beats"][0]["at"].items():
    assert v in s["beats"][0]["say"], v
f.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("circular ok")
