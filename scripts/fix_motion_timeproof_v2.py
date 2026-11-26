"""2026-11-25 (2) 사용자: "지금 예약 올라간 영상들 모두 저런식으로 수정하고 시간대 고려해서 수정해야 할 내용이 있는지 체크하고 예약 하세요.
일주일이나 며칠만 늦게 올려도 영상 폐기해야 할 일 없도록" — 엔비디아 2부 · 메모리 1부 · 메모리 2부.

1) 글 카드(stat: 아이콘+짧은 글) → 빼고, 원래 있던 모션그래픽을 되살리거나 문장을 연기하는 그림(growth·timeline·cond·ring·balance)으로.
   (11-25 사용자: "글로 설명하지 말고 옆에 설명을 보완하는 모션그래픽, 대본에 따라 매칭")
2) 며칠~일주일 늦게 올려도 틀리지 않게: '지금·아직·이미' 를 날짜·기준으로 (manual/03 §0-5 v126).
fix_static_insight.py · fix_static_memory_*.py 다음에 돌림 (그 스크립트를 다시 돌리면 이 스크립트도 다시).
python scripts/fix_motion_timeproof_v2.py  (다시 돌려도 같은 결과)"""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "3874962b~1"   # 글 카드를 끼우기 전 대본 (원래 그림)


def load(p):
    f = ROOT / "projects" / p / "02_script" / "hybrid.json"
    return f, json.loads(f.read_text(encoding="utf-8"))


def orig_pics(p, sid):
    raw = subprocess.run(["git", "show", f"{BASE}:projects/{p}/02_script/hybrid.json"], cwd=ROOT, capture_output=True, check=True).stdout
    return next(s for s in json.loads(raw.decode("utf-8"))["scenes"] if s["id"] == sid).get("pics")


def resay(sc, old, new):
    """대본 문장 바꾸기 (이미 바뀌었으면 그대로)."""
    for b in sc["beats"]:
        if old in b["say"]:
            b["say"] = b["say"].replace(old, new)
            return
    assert any(new in b["say"] for b in sc["beats"]), (sc["id"], old)


def check_t(sc, pics):
    say = " ".join(b["say"] for b in sc["beats"])
    for p in pics:
        assert p["t"] in say, (sc["id"], p["t"])
        for it in p.get("items", []):
            assert it["t"] in say, (sc["id"], it["t"])


# ── 엔비디아 2부 ──────────────────────────────────────────────────────────
P = "20261122-market-deep-nvidia-insight"
f, d = load(P)
S = {s["id"]: s for s in d["scenes"]}
resay(S[3], "지금까지 실제로 낸 돈은 없습니다", "3분기 보고 기준으로 실제로 낸 돈은 없습니다")
resay(S[4], "지금 시장의 의심은 넷입니다. 첫째, 이 고리를 이끌던 젠슨 황이 물러났습니다. 23일 돌아왔지만, 이사회의 독립 조사는 결론까지 이어집니다.",
      "11월 하순 시장의 의심은 넷이었습니다. 첫째, 이 고리를 이끌던 젠슨 황이 11일 물러났다가 23일 돌아왔고, 이사회의 독립 조사는 결론까지 이어집니다.")
S[4]["rows"][0]["label"] = "① 황 사임(11.11)·복귀(11.23) — 조사는 계속"
S[5]["pics"] = orig_pics(P, 5) + [{"t": "연준과", "kind": "cond", "if": ["trending-down", "'몇 년'이 틀리면"], "then": ["landmark", "손실이 어디까지 번지나"],
                                   "tone": "warn", "note": "연준 · 금리의 의심"}]
S[11]["pics"] = orig_pics(P, 11)
resay(S[15], "8월에 약속된 5,000억 달러는 아직 한 푼도 집행되지 않았고", "8월에 약속된 5,000억 달러는 보도 시점까지 한 푼도 집행되지 않았고")
resay(S[15], "시장이 매긴 값은, 아직은 엔비디아가 더 책임지면 빌려주겠다는 쪽입니다.", "그때 시장이 매긴 값은, 엔비디아가 더 책임지면 빌려주겠다는 쪽이었습니다.")
resay(S[20], "엔비디아가 지금까지 실제로 낸 돈이 없다는 점은", "엔비디아가 실제로 낸 돈이 없다는 점은")
resay(S[28], "그리고 지금 GPU 임대료가 오르고 있다는 사실은", "그리고 10월까지 GPU 임대료가 올랐다는 사실은")
resay(S[29], "지금까지는 0입니다.", "3분기 보고까지는 0입니다.")
resay(S[29], "지금의 64일보다", "3분기의 64일보다")
for r in S[29]["rows"]:
    r["label"] = r["label"].replace("(지금 0)", "(3분기 0)")
S[4]["title"] = S[4]["title"].replace("지금 엔비디아를", "11월 하순, 엔비디아를")
for p in S[29].get("pics", []):
    for it in p.get("items", []):
        it["text"] = it["text"].replace("(지금 0)", "(3분기 0)")
S[3]["small"] = S[3]["small"].replace("지금까지 실제로 낸 돈", "실제로 낸 돈 (3분기 보고 기준)")
for r in S[30]["rows"]:
    r["label"] = r["label"].replace("(지금은 보도뿐)", "(11월 하순엔 보도뿐)")
for sid in (5,):
    check_t(S[sid], S[sid]["pics"])
f.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("nvidia-insight ok")

# ── 메모리 2부 ────────────────────────────────────────────────────────────
P = "20261122-market-deep-memory-insight"
f, d = load(P)
S = {s["id"]: s for s in d["scenes"]}
S[4]["pics"] = [
    {"t": "이름 있는 사람들의", "kind": "ask", "q": "이 사람들의 말, 1부의 도구로 보면 맞을까?"},
    {"t": "첫째", "kind": "growth", "head": "작은 공급 차이 → 큰 값 변화 (1부)", "a": ["공급 차이", 5, "5%p"], "b": ["값 변화", 50, "반토막"],
     "color": "#B5302A", "badge": "몇 %가 값을 몇 배로"},
    {"t": "둘째", "kind": "timeline", "steps": ["증설 결정", "공장 짓는 중", "한꺼번에 시장에"], "gaps": ["2~3년", "동시에"],
     "note": "그사이 수요가 바뀌면 한꺼번에 남는다"},
    {"t": "셋째", "kind": "growth", "head": "같은 용량에 드는 웨이퍼", "a": ["일반 D램", 1, "1"], "b": ["HBM", 3.5, "3~4배"], "color": "#2E7D4F"}]
check_t(S[4], S[4]["pics"])
S[8]["pics"] = orig_pics(P, 8)
resay(S[8], "셋째, 현물값은 이미 한 달 새", "셋째, 현물값은 11월 20일까지 한 달 새")
resay(S[17], "지금 주가가 꼭대기 이익을", "주가가 꼭대기 이익을")
resay(S[20], "값은 아직 오르고 있지만", "4분기 전망까지 값은 오르고 있지만")
S[20]["title"] = S[20]["title"].replace("값은 아직 오르지만", "4분기 전망까지 값은 오르지만")
for r in S[8]["rows"]:
    if r.get("label_full"):
        r["label_full"] = r["label_full"].replace("이미 한 달 새", "11월 20일까지 한 달 새")
for r in S[8]["rows"]:   # 화면 줄도 (11-26 프레임 확인: '이미 하락'이 남아 있었음)
    r["label"] = r["label"].replace("현물값 이미 하락", "현물값 하락 (11.20까지 한 달)")
for r in S[23]["rows"]:
    r["label"] = r["label"].replace("오르는 속도가 이미 8분의 1", "4분기 전망에서 오르는 속도 8분의 1")
f.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("memory-insight ok")

# ── 메모리 1부 ────────────────────────────────────────────────────────────
P = "20261122-market-deep-memory-chicken"
f, d = load(P)
S = {s["id"]: s for s in d["scenes"]}
S[15]["pics"] = orig_pics(P, 15)
S[21]["pics"] = orig_pics(P, 21) + [{"t": "얕아질", "kind": "cond", "if": ["trending-down", "2023 큰 적자 → 감산이 더 빨리"],
                                     "then": ["trending-up", "하강이 얕아짐"], "tone": "ok",
                                     "note": "반대로 '점유율 지키기'가 다시 나오면 깊은 하강 (가설)"}]
for it in S[21]["pics"][0]["items"]:   # 핀 셋이 위로 쌓여 제목을 가리던 것 (11-25 text_occluded)
    if it.get("t") == "11월에":
        it["pos"] = "down"
check_t(S[21], S[21]["pics"][-1:])
for p in S[32].get("pics", []):
    if p.get("ticks"):
        p["ticks"] = [[x, "11월 하순" if lab == "지금" else lab] for x, lab in p["ticks"]]
if "r" in S[34].get("els", {}):
    S[34]["els"]["r"]["label"] = S[34]["els"]["r"]["label"].replace("지금: 값 꼭대기 부근", "11월: 값 꼭대기 부근")
f.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("memory-chicken ok")
