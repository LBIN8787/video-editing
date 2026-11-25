"""2026-11-25 정적 보완 — 오픈AI 편 (사용자: "나머지 영상들도 작업하세요").
고운 측정으로 9초 넘게 그대로인 곳에 말하는 순간 상자·그림을 붙임 (docs/68 E1·E3). 새 사실 없음: 모두 대본에 있는 값.
자리는 지난 렌더의 장면 끝 프레임에서 빈 곳을 골랐음 (겹침은 렌더 뒤 overlap_qa 로 다시 확인).
python scripts/fix_static_openai.py  (다시 돌려도 같은 결과)"""
import json
from pathlib import Path

F = Path(__file__).resolve().parent.parent / "projects" / "20261122-market-deep-openai" / "02_script" / "hybrid.json"
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
    old = [x for x in ms if x.get("id") == m["id"] or (not x.get("id") and x.get("t") == m["t"])]
    if old:
        old[0].update(m)
    else:
        ms.append(m)


def stat(t, icon, value, sub, color=None):
    p = {"t": t, "kind": "stat", "icon": icon, "value": value, "sub": sub}
    if color:
        p["color"] = color
    return p


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


# 4 — 공시 vs 추정 (19.2초)
motion(4, 0, C("장부가 없습니다", "nob", "오픈AI: 공개된 장부 없음", "비상장", 1380, 820))
motion(4, 0, C("단정하지 않고", "how", "이 영상: 누가 어디서 한 말인지", "단정하지 않음", 540, 820))
# 7 — 현금흐름 −2,780억 (15초·11초)
motion(7, 0, C("밖에서 구해야", "ext", "5년간 밖에서 구할 돈", "≈ 2,780억 달러", 1500, 880))
motion(7, 1, C("갚지 못할 수", "wsj", "CFO 내부 우려: 계약을 못 갚을 수도", "WSJ (4월 보도)", 540, 880, 520))
# 11 — 올트먼 인용 (24초)
motion(11, 0, C("너무 많아서", "dem", "'돈이 너무 많아 공급 부족'", "올트먼 (11.18 CNBC)", *B[0]))
motion(11, 1, C("3월의 대형 유치는", "m3", "받침: 3월 대형 유치", "보도", *B[1]))
motion(11, 1, C("절반에 그쳤다는", "half", "어긋남: 11월 모집 절반", "보도", *B[2]))
# 13 — 앤트로픽 상장 (22.8초)
motion(13, 1, C("액시오스는", "ax", "셈법을 맞춰도 순서 그대로", "액시오스 분석", 1520, 440, 440, 110, 24))
motion(13, 2, C("장부가 공개된", "open", "장부가 공개된 선택지가 생김", "돈을 넣을 사람들에게", 1520, 580, 440, 110, 24))
# 15 — 위워크: 그림 없던 체크리스트
pics(15, ["길게 빌리고, 짧게 번다", "2019.1  기업 가치 약 470억", "2019.8  상장 서류 → 손실 드러남", "2019.9  상장 철회"], [
    stat("위워크는", "building", "십수 년 vs 몇 달", "건물은 길게 빌리고, 고객엔 짧게", INK),
    stat("470억", "trending-up", "470억 달러", "2019년 1월 기업 가치"),
    stat("8월에", "search", "장부 공개", "손실과 임대 약속의 크기가 드러남"),
    stat("한 달 남짓", "trending-down", "상장 철회", "2019년 9월"),
    stat("소프트뱅크였습니다", "building", "소프트뱅크", "위워크의 최대 투자자", INK)])
# 16 — 같은 점·다른 점
pics(16, ["같음 — 길게 약속, 짧게 번다", "같음 — 장부 닫힘 · 최대 투자자 소프트뱅크", "다름 — 매출이 빠르게 는다", "다름 — 상대가 MS·오라클·엔비디아"], [
    stat("같은 점은", "link", "같은 구조", "길게 약속하고 짧게 번다", INK),
    stat("장부가", "search", "장부 닫힘", "비상장 · 최대 투자자 소프트뱅크"),
    stat("다른 점도", "trending-up", "매출 ↑", "3분기 약 100억 달러 (보도)", OK),
    stat("상대가", "building", "큰 상대", "마이크로소프트 · 오라클 · 엔비디아", OK),
    stat("단정할 수 없습니다", "search", "단정 못 함", "위워크와 같은 결말?", INK)])
# 18 — 얼마나 버티나
motion(18, 1, C("2027년 중반을", "when", "분석가 2027년 중반 · 로이터 2028년", "갈리는 답", 960, 770, 560, 100, 24))
# 21 — 오라클
motion(21, 1, C("가장 아래 칸으로", "bbb", "S&P: 투자 등급 맨 아래 칸", "7월 강등", 420, 860))
motion(21, 2, C("모두 확보했다고", "fund", "오라클: 자금 모두 확보 (11.20)", "자기 몫의 돈", 380, 300, 400, 110, 24))
# 24 — 낙관 vs 우려 (20초)
motion(24, 0, C("오라클이", "orc", "오라클 = 가장 큰 계약 상대", "낙관 쪽", 540, 830))
motion(24, 0, C("빅쇼트의", "eis", "아이스먼 = 빅쇼트의 실제 인물", "우려 쪽", 1380, 830))
# 26·28·30·31 — 인용
motion(26, 0, C("공급이 모자랐다고", "dem2", "'공급이 모자랐다'", "올트먼 (11.18)", *B[0]))
motion(26, 0, C("절반만 모였다는", "half2", "어긋남: 목표의 절반만", "11월 보도", *B[1]))
motion(28, 0, C("누가 먼저 맞는지", "who", "무너지면 누가 먼저 맞나", "아이스먼의 요지", *B[0]))
motion(28, 0, C("파산 경고라는", "head", "매체 제목: '파산 경고'", "결이 다름", *B[1]))
motion(30, 0, C("앤트로픽을 놓친", "miss", "앤트로픽을 놓친 것 = 실수", "손정의 (11.19 도쿄)", *B[0]))
motion(30, 0, C("13%를", "keep", "그래도 지분 약 13% 유지", "소프트뱅크", *B[1]))
motion(31, 0, C("300억", "last", "오픈AI 투자는 300억이 마지막", "젠슨 황 (3월)", *B[0]))
motion(31, 0, C("창이 닫힌다는", "win", "상장 가까워 → 비상장 투자 창 닫힘", "이유", *B[2]))
# 35 — 틈을 메우는 세 길
motion(35, 1, C("자기 매출과 지분이", "own", "MS·엔비디아·소프트뱅크: 받칠 이유", "자기 매출·지분", 1650, 300, 440, 110, 24))
motion(35, 2, C("상한과 단계별", "cap", "상한·단계별 → 늦추거나 줄임", "오픈AI엔 숨통", 300, 300, 440, 110, 24))
motion(35, 2, C("가장 먼저 느끼는", "fx", "반대편엔: 매출이 뒤로", "오라클·코어위브·칩 주문", 1650, 450, 440, 110, 24))

F.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("openai ok")
