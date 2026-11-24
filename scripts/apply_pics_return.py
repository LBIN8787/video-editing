"""2026-11-24 사용자: "진행해주고" — 젠슨 복귀 편(20261124-market-deep-nvidia-return)에도 다섯 편과 같은 보완:
멈춰 있던 체크리스트에 오른쪽 그림(pics), 6번 인용 장면의 숫자 상자가 화면 밖으로 잘리던 것 고침.
python scripts/apply_pics_return.py  (다시 돌려도 같은 결과)"""
import json
from pathlib import Path

P = Path(__file__).resolve().parent.parent / "projects" / "20261124-market-deep-nvidia-return" / "02_script" / "hybrid.json"

S = {}
S[4] = dict(
    rows=["11.11 사임 수리 — 크레스 임시 CEO", "11.13 주주 서한·머스크 '복귀 열어 두라'", "11.15 베선트 '외부 CEO'",
          "11.17 이사회 '복귀 없다' · 황 '부르면 영광'", "11.20 SEC 조사 보도 — 하루 -14%"],
    pics=[{"t": "11일", "kind": "pins", "head": "위: 복귀를 부르는 쪽 · 아래: 막는 쪽", "range": [10.3, 21.0],
           "ticks": [[11, "11.11"], [13, "11.13"], [15, "11.15"], [17, "11.17"], [20, "11.20"]],
           "items": [{"t": "11일", "at": 11, "name": "사임 수리", "say": "크레스 임시 CEO", "side": "warn", "pos": "down"},
                     {"t": "13일", "at": 13, "name": "주주 서한·머스크", "say": "복귀 열어 두라", "side": "ok", "pos": "up"},
                     {"t": "15일", "at": 15, "name": "베선트 재무장관", "say": "외부 CEO", "side": "warn", "pos": "down"},
                     {"t": "17일", "at": 17, "name": "이사회", "say": "복귀 없다", "side": "warn", "pos": "down"},
                     {"t": "성명을", "at": 17.2, "name": "황 성명", "say": "부르면 영광", "side": "ok", "pos": "up"},
                     {"t": "20일", "at": 20, "name": "SEC 조사 보도", "say": "하루 -14%", "side": "warn", "pos": "down"}]}])
S[11] = dict(
    rows=["의장 하비 존스 — 그대로", "독립 조사위원회 — 결론까지", "수출통제 위원회 — 새로", "최고준법책임자 — 새로 뽑음", "정부 조사에 계속 협조"],
    pics=[{"t": "다섯입니다", "kind": "orbit", "hero": ["user", "젠슨 황", "돌아온 CEO"], "items": [
        {"t": "하비 존스가", "icon": "landmark", "text": "이사회 의장", "sub": "하비 존스 그대로", "side": "info"},
        {"t": "독립 조사위원회는", "icon": "search", "text": "독립 조사위", "sub": "결론까지 간다", "side": "info"},
        {"t": "수출통제 위원회가", "icon": "shield-check", "text": "수출통제 위원회", "sub": "무역·안보 감독", "side": "info"},
        {"t": "최고준법책임자", "icon": "user", "text": "준법책임자", "sub": "새로 뽑음", "side": "info"},
        {"t": "정부 조사에는", "icon": "scale", "text": "정부 조사", "sub": "계속 협조", "side": "info"}]}])
S[21] = dict(
    rows=["받침: 조사·형사 조사·면담 진행 중", "받침: 이사회 말이 5일 만에 바뀜", "어긋남: 정부 '안보 위험 없다'", "어긋남: 감시 장치가 새로 붙음"],
    pics=[{"t": "받치는", "kind": "twocol", "left": "받치는 사실", "right": "어긋나는 사실", "lcolor": "#2E7D4F",
           "items": [{"t": "이사회 조사도", "side": "l", "text": "이사회 독립 조사 · 진행 중"},
                     {"t": "형사", "side": "l", "text": "법무부 형사 조사 · 진행 중"},
                     {"t": "하원", "side": "l", "text": "하원 면담 · 12월 1일"},
                     {"t": "5일", "side": "l", "text": "이사회 말, 5일 만에 바뀜"},
                     {"t": "안보 위험이", "side": "r", "text": "정부 '안보 위험 없다'"},
                     {"t": "감시", "side": "r", "text": "위원회·준법책임자 새로"}],
           "verdict": {"t": "판정은", "text": "근거 있음 — 다만 앞으로의 경고"}}])
S[25] = dict(
    rows=["한 달: 하이닉스 -29% · 삼성 -24%", "원인은 하나가 아니다", "24일 첫 반응: 하이닉스·삼성 +6.7%"],
    pics=[{"t": "지난 한 달", "kind": "drop", "head": "SK하이닉스, 한 달 (10.29 → 11.23)", "value": -28.9, "note": "삼성전자 -23.5% · 코스피 -20.7%"},
          {"t": "하나로", "kind": "lamps", "items": [
              {"t": "하나로", "icon": "user", "text": "황의 사임", "tag": "하나만이 아님", "side": "warn"},
              {"t": "금리와", "icon": "percent", "text": "금리", "tag": "겹침", "side": "warn"},
              {"t": "순환금융", "icon": "refresh-cw", "text": "순환금융 의심", "tag": "겹침", "side": "warn"},
              {"t": "SEC 보도가", "icon": "search", "text": "SEC 조사 보도", "tag": "겹침", "side": "warn"}]},
          {"t": "시간을", "kind": "timeline", "steps": ["한국 장 마감", "복귀 발표 (23일 밤)", "첫 반응 = 24일 장"],
           "gaps": ["몇 시간 뒤", "다음 날 아침"], "note": "23일 하락은 복귀를 모르고 움직인 값"},
          {"t": "올랐습니다", "kind": "stat", "icon": "trending-up", "value": "+6.7%", "sub": "24일 SK하이닉스·삼성전자 (코스피 +6.3%)"}])
S[26] = dict(
    rows=["11.25 재무부에 우회 수출 답변", "12.1·2 황·법률총괄 하원 면담", "미정: 상원 청문회·독립위 결론", "매일: 종가가 사임 전 수준 지키나"],
    pics=[{"t": "11월 25일", "kind": "pins", "head": "판가름 날짜", "range": [24.2, 36.0],
           "ticks": [[25, "11.25"], [31.5, "12.1·2"]],
           "items": [{"t": "11월 25일", "at": 25, "name": "재무부 답변", "say": "우회 수출", "side": "warn", "pos": "up"},
                     {"t": "12월 1일과", "at": 31, "name": "황", "say": "하원 비공개 면담", "side": "warn", "pos": "up"},
                     {"t": "법률총괄이", "at": 32, "name": "법률총괄 테터", "say": "하원 면담", "side": "warn", "pos": "down"},
                     {"t": "상원", "at": 35, "name": "날짜 미정", "say": "상원 청문회·독립위 결론", "side": "warn", "pos": "up"}]},
          {"t": "지키면", "kind": "cond", "if": ["trending-up", "종가가 사임 전 수준을 지킴"], "then": ["building", "시장: 회사 차원의 문제는 아니다"], "tone": "ok"},
          {"t": "무너지면", "kind": "cond", "if": ["trending-down", "종가가 무너짐"], "then": ["search", "조사 쪽 위험을 다시 값에 넣음"], "tone": "warn"}])


def main():
    doc = json.loads(P.read_text(encoding="utf-8"))
    for sid, spec in S.items():
        sc = next(s for s in doc["scenes"] if s["id"] == sid)
        assert len(spec["rows"]) == len(sc["rows"]), sid
        for r, lab in zip(sc["rows"], spec["rows"]):
            r.setdefault("label_full", r["label"])
            r["label"] = lab
        sc["x"], sc["text_w"] = 150, 880
        sc["pics"] = spec["pics"]
        for b in sc["beats"]:
            if b.get("motion"):
                b["motion_off"] = b.pop("motion")
        print("ok", sid, len(spec["pics"]))
    # 6번: 대통령 발언 숫자 상자가 오른쪽 밖으로 잘림 → 글을 줄이고 상자를 안쪽으로
    sc = next(s for s in doc["scenes"] if s["id"] == 6)
    for b in sc["beats"]:
        for m in b.get("motion") or []:
            if m.get("id") == "tr":
                m.update(value="'상관없다' → '다시 고용' → 22일 결의", x=1180, w=660, fs=24)
                print("ok 6")
    P.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()

