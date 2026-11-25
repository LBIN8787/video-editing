"""2026-11-25 정적 보완 2단계 — 엔비디아 1부 순환금융.
더 고운 측정(320×180, 자막 줄 제외, 한 곳이라도 바뀌면 변화)으로 6초 넘게 화면이 그대로인 곳 29곳을 찾아,
문장의 명사·숫자를 말하는 순간 그림이 바뀌게 (docs/68 E1·E3·E4). 새 사실 없음 — 모두 대본에 있는 값.
- 그림 없던 체크리스트 3·10·13·20 → 오른쪽에 문장마다 그림 (줄 글은 짧게, 원문은 label_full)
- 2·6·9·12·15·18·19 → 말하는 단어에 상자·카드·글을 붙임
python scripts/fix_static_circular2.py  (fix_static_return_circular.py 다음에, 다시 돌려도 같은 결과)"""
import json
from pathlib import Path

F = Path(__file__).resolve().parent.parent / "projects" / "20261122-market-deep-nvidia-circular" / "02_script" / "hybrid.json"
OK, INK = "#2E7D4F", "#3A3F48"
d = json.loads(F.read_text(encoding="utf-8"))
S = {s["id"]: s for s in d["scenes"]}


def say(sid):
    return " ".join(b["say"] for b in S[sid]["beats"])


def pics(sid, rows, ps):
    sc = S[sid]
    assert len(rows) == len(sc["rows"]), sid
    for r, lab in zip(sc["rows"], rows):
        r.setdefault("label_full", r["label"])
        r["label"] = lab
    for p in ps:
        assert p["t"] in say(sid), (sid, p["t"])
    sc["x"], sc["text_w"] = 150, 880
    sc["pics"] = ps
    for b in sc["beats"]:
        if b.get("motion"):
            b["motion_off"] = b.pop("motion")


def stat(t, icon, value, sub, color=None):
    p = {"t": t, "kind": "stat", "icon": icon, "value": value, "sub": sub}
    if color:
        p["color"] = color
    return p


def motion(sid, bi, m):
    b = S[sid]["beats"][bi]
    assert m["t"] in b["say"], (sid, m["t"])
    ms = b.setdefault("motion", [])
    old = [x for x in ms if x.get("id") and x.get("id") == m.get("id")] or [x for x in ms if not m.get("id") and x == m]
    if old:
        old[0].update(m)
    else:
        ms.append(m)


def C(t, id_, value, label, x, y, w=480, h=120, fs=32):
    return {"t": t, "do": "count", "id": id_, "value": value, "label": label, "x": x, "y": y, "w": w, "h": h, "fs": fs}


def el(sid, bi, key, spec, word):
    sc = S[sid]
    assert word in sc["beats"][bi]["say"], (sid, word)
    sc["els"].setdefault(key, spec)
    b = sc["beats"][bi]
    if key not in b["do"]:
        b["do"].append(key)
    b.setdefault("at", {})[key] = word


# 3 — 의심 넷: 28초 동안 줄만 켜짐 (21.2초 정지)
S[3]["rows"][3]["t"] = "14%"
pics(3, ["황 사임 (11.11) → 23일 복귀", "SEC 장부 조사 보도 (확인 안 됨)", "연준: 순환 금융은 위험 (11.18)", "11.20 엔비디아 -14%"], [
    stat("젠슨 황이", "calendar", "사임", "11월 11일 젠슨 황 CEO 사임", INK),
    stat("SEC가", "search", "보도", "SEC가 장부를 본다 — 확인 안 됨"),
    stat("연준은", "landmark", "위험", "연준 의사록: AI 회사 사이 순환 금융"),
    {"t": "14%", "kind": "drop", "head": "엔비디아, 11월 20일 하루", "value": -14, "note": "7주 연속 하락"},
    # 타임라인은 '돌아왔지만' 에서 (처음엔 '젠슨 황이' 에 붙여 1.3초 만에 넘겨져, 덜 그려진 칸이 뒤 그림과 겹침)
    {"t": "돌아왔지만", "kind": "timeline", "steps": ["사임 11.11", "복귀 11.23", "조사 결론은?"], "gaps": ["12일 뒤", "계속"], "note": "이사회 독립 조사는 결론까지", "boxes": False},
    {"t": "원리부터", "kind": "ask", "q": "이 고리는 무엇이고, 어디서 끊어질 수 있나?"}])
# 10 — 오해 풀기: 그림 없음
S[10]["rows"][0]["t"] = "효력이"
pics(10, ["가장 큰 보증 1,050억 — 효력은 2028~29년부터", "보증으로 실제로 낸 돈 — 0", "데이터센터 매출 절반 남짓은 빅테크", "위험은 몇 년 뒤의 약속에"], [
    stat("효력이", "calendar", "2028~29년", "가장 큰 보증 1,050억이 효력을 갖는 때", INK),
    stat("낸 돈은", "banknote", "0달러", "보증으로 실제로 낸 돈 (지금까지)", OK),
    {"t": "빅테크", "kind": "waffle", "head": "데이터센터 매출 = 점 100개", "parts": [["현금 많은 빅테크", 56, "ok", "빅테크"]], "suffix": "%",
     "note": "601억 ÷ 1,076억 달러 (3분기)"},
    stat("몇 년 뒤", "hourglass", "몇 년 뒤", "위험이 쌓이는 곳 — 오늘 매출이 아니라 약속")])
# 13 — 루슨트와 같은 점·다른 점 (make_examples 의 점 격자를 실제로)
pics(13, ["같음 — 파는 쪽이 돈을 댄다", "같음 — 직접 고객 다섯 곳이 70%", "다름 — 고객 절반 남짓이 빅테크", "다름 — 큰 보증은 아직 효력 전"], [
    stat("같은 점은", "link", "같은 틀", "파는 쪽이 사는 쪽에 돈을 대며 판다", INK),
    {"t": "다섯 곳이", "kind": "waffle", "head": "받을 돈(매출채권) = 점 100개", "parts": [["직접 고객 다섯 곳", 70, "warn", "다섯 곳이"]], "suffix": "%", "note": "7월 말 기준"},
    {"t": "다른 점도", "kind": "waffle", "head": "데이터센터 매출 = 점 100개", "parts": [["현금 많은 빅테크", 56, "ok", "다른 점도"]], "suffix": "%", "note": "601억 ÷ 1,076억 달러"},
    stat("효력이", "calendar", "효력 전", "가장 큰 보증 — 실제로 낸 돈 0", OK),
    stat("속도는", "trending-up", "더 빠름", "몇 년 뒤의 약속이 커지는 속도")])
# 20 — 다음 소식 읽는 넷 (줄의 '회수' 가 대사에 없어 늦게 켜지던 것도)
S[20]["rows"][0]["t"] = "걸리는 날이"
pics(20, ["받기까지 걸리는 날 (지금 64일)", "지분 투자 손상 (3분기 18억)", "월가 5,000억 칩 금융 집행", "메모리 약정 (지금 3,900억)"], [
    stat("걸리는 날이", "calendar", "64일", "칩값을 받기까지 — 더 길어지나", INK),
    stat("손상이", "trending-down", "18억 달러", "3분기 지분 손상 — 이어지나"),
    stat("집행되는지", "landmark", "0 → ?", "월가 5,000억 칩 금융 — 집행되나", INK),
    stat("메모리 약정이", "boxes", "3,900억 달러", "엔비디아 메모리 약정 — 줄어드나"),
    stat("한국 계좌에", "landmark", "한국 계좌", "가장 가까운 신호 = 메모리 약정")])

# 2 — ① 은 '대신 갚겠다'를 말하는 b0 에서 (b0 10.8초 정지), b1 끝 10.5초: 셋을 다시 짚음
b0, b1 = S[2]["beats"]
r1 = [m for m in b1.get("motion") or [] if m.get("id") == "r1"]
if r1:
    b1["motion"].remove(r1[0])
motion(2, 0, C("대신 갚겠다고", "r1", "① 못 내면 대신 갚는다", "보증", 320, 880, 400, 120, 28))
motion(2, 1, {"t": "순환금융이라고", "do": "pulse", "on": "r1"})
motion(2, 1, {"t": "기사를", "do": "pulse", "on": "r2"})
motion(2, 1, {"t": "복잡합니다", "do": "pulse", "on": "r3"})
# 6 — 돈이 도는 길: 사는 쪽 사정·엔비디아 현금, 경쟁사 막기
el(6, 0, "cu1", {"kind": "text", "x": 420, "y": 790, "text": "버는 돈 < 쓰는 돈 · 빚으로 서버", "size": 32}, "쓰는 돈이")
el(6, 0, "nv1", {"kind": "text", "x": 960, "y": 420, "text": "현금이 넘친다", "size": 32}, "현금이 넘칩니다")
el(6, 1, "or1", {"kind": "text", "x": 1500, "y": 790, "text": "+ 경쟁사를 막는 자리", "size": 32}, "경쟁사를")
# 9 — 메모 문장
motion(9, 1, C("메모에서", "memo", "'매출에 비해 작은 비중'", "엔비디아 메모 (2025.11)", 1560, 780))
# 12 — 루슨트가 고객에게 돈을 빌려준다
motion(12, 0, C("신생 통신사에", "lend", "장비 사는 고객에게 대출", "루슨트 (2000년 무렵)", 300, 740, 420, 120, 30))
# 15 — 지급 기한
motion(15, 0, C("90일에서", "term", "지급 기한 90일 → 최대 1년", "큰 고객에게 늘려 줌", 1600, 600, 440, 130, 32))
# 18 — 장기 계약, 고리의 끝
el(18, 0, "lt", {"kind": "text", "x": 1700, "y": 640, "text": "몇 년 치 물량 — 장기 계약", "size": 30}, "장기 계약으로")
el(18, 1, "end", {"kind": "text", "x": 1700, "y": 300, "text": "고리의 끝 = 한국 메모리", "size": 34}, "끝에는")
# 19 — 틀리는 경우 둘째의 근거 (평가 이익·KB증권)
sc = S[19]
for p in [stat("평가 이익이", "trending-up", "이익 > 손실", "엔비디아 지분 투자 평가 (지금까지)", OK),
          stat("KB증권은", "building", "현금 2배+", "KB증권 (9월): 3년 벌 현금 vs 약속한 돈", OK)]:
    assert p["t"] in say(19)
    if not any(x.get("t") == p["t"] for x in sc["pics"]):
        sc["pics"].insert(2 if p["t"] == "평가 이익이" else 3, p)

F.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("circular2 ok")
