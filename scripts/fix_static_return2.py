"""2026-11-25 정적 보완 2단계 — 젠슨 복귀 편.
고운 측정(320×180, 자막 줄 제외)으로 6초 넘게 그대로인 곳 중 긴 것 — 인용 장면 4곳(25초 안팎), 질문·숫자 장면 —
에 말하는 순간 붙는 상자를 더함 (docs/68 E1·E3). 새 사실 없음: 모두 대본·팩트시트에 있는 말과 값. 인용 부호는 원문 그대로일 때만.
python scripts/fix_static_return2.py  (fix_static_return_circular.py 다음에, 다시 돌려도 같은 결과)"""
import json
from pathlib import Path

F = Path(__file__).resolve().parent.parent / "projects" / "20261124-market-deep-nvidia-return" / "02_script" / "hybrid.json"
d = json.loads(F.read_text(encoding="utf-8"))
S = {s["id"]: s for s in d["scenes"]}


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


def el(sid, bi, key, spec, word):
    sc = S[sid]
    assert word in sc["beats"][bi]["say"], (sid, word)
    sc["els"].setdefault(key, spec)
    b = sc["beats"][bi]
    if key not in b["do"]:
        b["do"].append(key)
    b.setdefault("at", {})[key] = word


# 2 — 이 영상의 질문 둘 (11.5초 정지)
motion(2, 1, C("왜 뒤집었나", "q1", "① 이사회는 왜 뒤집었나?", "이 영상의 질문", 520, 720, 600))
motion(2, 1, C("다 풀린", "q2", "② 돌아오면 다 풀리나?", "이 영상의 질문", 520, 860, 600))
# 5 — 베선트 (26.8초 정지): 말이 바뀐 것, 쟁점, 기한
motion(5, 0, C("외부 CEO를", "bs0", "11.15 외부 CEO → 11.22 그는 밖에 있다", "베선트 재무장관의 말", 1500, 500))
motion(5, 1, C("개인사가", "bs1", "쟁점: 어느 단계가 수출통제 문제를 알았나", "개인사가 아니라 (CBS, 11.22)", 1500, 640))
motion(5, 1, C("11월 25일까지", "bs2", "재무부 답변 기한 11월 25일", "우회 수출 질의 · 보도", 1500, 780))
# 8 — 이사회가 든 이유 둘, 회사 밖 근거 하나 (26.8초 정지)
motion(8, 0, C("솔직함과", "rs1", "이유 ① 솔직함·지도력에 만족", "8-K (11.22 결의)", 1500, 500))
motion(8, 0, C("다른 하나가", "rs2", "이유 ② 정부 고위층 의견", "→ 국가안보 위험 없다", 1500, 640))
motion(8, 1, C("경영 실력이", "rs3", "회사 밖 근거 = 정부의 판단 하나", "경영 실력이 아니라", 1500, 780))
# 13 — 복귀 날 +31%
motion(13, 1, C("31% 올라", "up31", "하루 +31.5% (125.53 → 165.05)", "11월 23일 종가", 1500, 620))
# 16 — 매체 프레임 (24.8초 정지): 매체마다 무엇을 앞세웠나, 제목에서 빠진 것
motion(16, 0, C("코타쿠는", "m1", "코타쿠 — 며칠 만의 번복에 무게", "게임 매체 · 제목", 1500, 500))
motion(16, 0, C("KBS는", "m2", "KBS — 칩 밀수와 개인사는 별개", "국내 · 재무장관 발언을 앞세움", 1500, 640))
motion(16, 0, C("잘 보이지", "m3", "제목에서 빠진 것: 조사는 결론까지", "8-K 문장", 1500, 780))
# 20 — 반대편 둘째 목소리
motion(20, 0, C("스카라무치는", "sc", "스카라무치 — FBI는 청원을 받지 않는다", "투자자 · 의견", 1500, 760))
# 22 — 갈림길의 판가름
motion(22, 1, C("몇 주의", "wk", "판가름: 앞으로 몇 주의 조사 일정", "공시가 아니라", 960, 820, 640))
# 24 — 약정의 반대편, 복귀의 뜻 (19.2초 정지)
motion(24, 0, C("SK하이닉스와", "kr", "반대편: SK하이닉스·삼성전자", "메모리 공급사", 520, 880, 600))
motion(24, 0, C("같은 사람이", "same", "계약을 지킬 사람 = 다시 황", "복귀의 뜻", 1300, 880, 600))
# 19 — 판정
el(19, 1, "vd", {"kind": "text", "x": 1590, "y": 560, "text": "판정: 일부만 맞다", "size": 36}, "판정은")

F.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("return2 ok")
