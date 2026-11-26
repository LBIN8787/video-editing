"""2026-11-25 사용자: "고쳐야 할 점은 수정하시고" — 엔비디아 1부·2부(11-22 제작)는 '황은 이제 없다'로 쓰였는데
11-22(현지) 이사회가 복귀를 결의했다(8-K 11-23 제출, 크레스는 CFO 로 계속). 과거 사실은 그대로 두고 복귀를 덧붙인다.
python scripts/fix_ceo_return_nvidia.py  (다시 돌려도 같은 결과)"""
import json
from pathlib import Path

R = Path(__file__).resolve().parent.parent / "projects"


def sc(doc, i):
    return next(s for s in doc["scenes"] if s["id"] == i)


def rep(s, old, new):
    if new in s:
        return s
    assert old in s, old[:40]
    return s.replace(old, new)


def circular():
    p = R / "20261122-market-deep-nvidia-circular" / "02_script" / "hybrid.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    s = sc(d, 1)
    s["role"] = "엔비디아 당시 임시 CEO(CFO) · CNBC (11월 18일)"
    b = s["beats"][0]
    b["say"] = rep(b["say"], "젠슨 황이 물러난 뒤 임시 CEO가 된 콜레트 크레스는", "젠슨 황이 물러나 있던 동안 임시 CEO를 맡았던 콜레트 크레스는")
    s = sc(d, 3)
    b = s["beats"][0]
    b["say"] = rep(b["say"], "11월 20일 엔비디아는 하루에 14% 빠졌습니다.",
                   "11월 20일 엔비디아는 하루에 14% 빠졌습니다. 황은 11월 23일 CEO로 돌아왔지만, 이사회의 독립 조사는 결론까지 이어집니다.")
    s["rows"][0]["label"] = "젠슨 황 사임 (11.11) → 23일 복귀"
    s = sc(d, 16)
    b = s["beats"][2]
    b["say"] = rep(b["say"], "넷째, 이 고리를 이끌던 사람이 바뀌었습니다.", "넷째, 이 고리를 이끌던 사람이 흔들렸습니다.")
    b["say"] = rep(b["say"], "이사회 독립위원회의 조사도 진행 중입니다.",
                   "황은 12일 만인 11월 23일 돌아왔지만, 이사회 독립위원회의 조사는 결론까지 이어집니다.")
    r = s["rows"][2]
    r["label"] = "황 사임 → 크레스 임시 → 23일 복귀"
    r["label_full"] = "11월 11일(미국 시간) 젠슨 황 사임 — 크레스 CFO 임시 CEO — 11월 23일 황 복귀"
    s["pics"][2] = {"t": "물러났고", "kind": "timeline", "steps": ["황 사임 (11.11)", "크레스 임시 CEO", "황 복귀 (11.23)"],
                    "gaps": ["같은 날", "12일 뒤"], "note": "이사회 독립 조사는 결론까지"}
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    for f in ("05_edit/youtube.md",):
        q = p.parent.parent / f
        t = q.read_text(encoding="utf-8")
        q.write_text(t.replace("월가 5,000억 미집행, CEO 교체.", "월가 5,000억 미집행, CEO 사임과 12일 만의 복귀."), encoding="utf-8")
    d2 = d.get("package", {})
    print("circular ok")


def insight():
    p = R / "20261122-market-deep-nvidia-insight" / "02_script" / "hybrid.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    b = sc(d, 2)["beats"][0]
    b["say"] = rep(b["say"], "이 말을 한 젠슨 황은 이제 엔비디아에 없습니다. 11월 11일 CEO에서 물러났습니다. 그런데 그가 남긴 이 8년이라는 숫자가, 지금 엔비디아를 둘러싼 의심의 한가운데 있습니다.",
                   "이 말을 한 젠슨 황은 11월 11일 CEO에서 물러났다가, 12일 만인 23일 돌아왔습니다. 그사이 그가 남긴 이 8년이라는 숫자가, 엔비디아를 둘러싼 의심의 한가운데 놓였습니다.")
    s = sc(d, 4)
    b = s["beats"][0]
    b["say"] = rep(b["say"], "첫째, 이 고리를 이끌던 젠슨 황이 떠났습니다. 사임 이유는 공시에 없습니다.",
                   "첫째, 이 고리를 이끌던 젠슨 황이 물러났습니다. 23일 돌아왔지만, 이사회의 독립 조사는 결론까지 이어집니다.")
    s["rows"][0]["label"] = "① 젠슨 황 사임 (11.11) → 23일 복귀"
    s["rows"][0]["label_full"] = "① 고리를 이끌던 젠슨 황이 물러났다 (11월 11일) — 11월 23일 복귀, 독립 조사는 계속"
    it = s["pics"][0]["items"][0]
    it["text"], it["tag"] = "젠슨 황 사임·복귀", "독립 조사는 계속"
    s["label"] = rep(s["label"], "엔비디아 8-K(11.11) 젠슨 황 사임", "엔비디아 8-K(11.11) 젠슨 황 사임 · 8-K(11.22) 복귀")
    b = sc(d, 6)["beats"][0]
    b["say"] = rep(b["say"], "그는 이 인터뷰 몇 주 뒤 CEO에서 물러났습니다. 말한 사람은 떠났지만 이 논리는 지금도 엔비디아 방어의 중심이고, 새 경영진이 이 약속들을 그대로 이어 갈지가 질문으로 남았습니다.",
                   "그는 이 인터뷰 몇 주 뒤 CEO에서 물러났다가 11월 23일 돌아왔습니다. 이 논리는 지금도 엔비디아 방어의 중심이고, 돌아온 그가 이 약속들을 그대로 지켜 갈지가 질문으로 남았습니다.")
    b = sc(d, 9)["beats"][0]
    b["say"] = rep(b["say"], "두 번째, 젠슨 황의 자리를 이어받은 콜레트 크레스 임시 CEO입니다.",
                   "두 번째, 황이 물러나 있던 동안 임시 CEO를 맡았던 콜레트 크레스입니다.")
    s = sc(d, 10)
    s["label"] = rep(s["label"], "엔비디아 임시 CEO (전 CFO)", "엔비디아 당시 임시 CEO (CFO)")
    if "role" in s:
        s["role"] = "엔비디아 당시 임시 CEO(CFO) · CNBC (11월 18일)"
    b = sc(d, 31)["beats"][0]
    b["say"] = rep(b["say"], "젠슨 황은 떠났지만 그가 남긴 질문은 그대로입니다.", "젠슨 황은 돌아왔지만 그가 남긴 질문은 그대로입니다.")
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print("insight ok")


if __name__ == "__main__":
    circular()
    insight()
