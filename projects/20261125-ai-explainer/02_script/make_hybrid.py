"""script_v2.md + visual_beats.md(A1~A5) → hybrid.json. python make_hybrid.py (02_script 에서)."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OP = "의견이며 사실이 아닙니다"
CO = "회사 자체 측정"
SRC = "앤트로픽 인스티튜트 'When AI builds itself' (2026, 9/18 업데이트)"
S, CH = [], [0]


def add(sc):
    sc["id"] = len(S) + 1
    sc["chapter"] = CH[0]
    S.append(sc)


def chapter(num, title, icon, say):
    CH[0] = num
    add({"type": "chapter", "num": str(num), "title": title, "icon": icon, "look": "board", "beats": [{"say": say}]})


def quote(who, role, ko, orig, keyword, says, label, insight=True):
    add({"type": "quote", "insight": insight, "who": who, "role": role, "quote": ko, "orig": orig, "keyword": keyword,
         "label": label, "beats": [{"say": s} for s in says]})


def board(title, els, beats, label=""):
    add({"type": "motionboard", "title": title, "theme": "dark", "label": label, "els": els, "beats": beats})


# 고리 (A1) — 같은 좌표를 끝까지 씀
LOOP = {
    "c1": {"kind": "card", "x": 960, "y": 300, "icon": "search", "label": "① 문제 고르기"},
    "c2": {"kind": "card", "x": 1460, "y": 540, "icon": "laptop", "label": "② 설계·코드"},
    "c3": {"kind": "card", "x": 960, "y": 780, "icon": "flask-conical", "label": "③ 실험·결과"},
    "c4": {"kind": "card", "x": 460, "y": 540, "icon": "cpu", "label": "④ 다음 모델"},
    "a12": {"kind": "arrow", "from": "c1", "to": "c2", "bend": 0.25},
    "a23": {"kind": "arrow", "from": "c2", "to": "c3", "bend": 0.25},
    "a34": {"kind": "arrow", "from": "c3", "to": "c4", "bend": 0.25},
    "a41": {"kind": "arrow", "from": "c4", "to": "c1", "bend": 0.25},
}


def loop(extra):
    els = {k: dict(v) for k, v in LOOP.items()}
    els.update(extra)
    return els


# ── 1. 코드의 80% ─────────────────────────────────────────────────
add({"type": "share", "title": "앤트로픽 코드베이스에 새로 합친 코드 (2026년 5월)", "total": "새로 합친 코드 전체", "of": 100,
     "parts": [{"label": "클로드가 씀", "value": 80}], "mark": {"value": 80, "label": "80% 넘게"},
     "label": f"{SRC} · {CO}",
     "beats": [{"say": "2026년 5월, AI 회사 앤트로픽의 개발자들이 회사 코드에 새로 합친 코드 가운데 80% 넘게를 자기 회사 AI, 클로드가 썼습니다.", "show": ["total", "p0", "mark"]},
               {"say": "그리고 이 회사는 공개 글에서 스스로 묻습니다. AI 가 자기 다음 모델을 처음부터 끝까지 혼자 만들 수 있게 되면, 무슨 일이 일어날까."}]})
board("이 영상의 해석", {
    "loop": {"kind": "card", "x": 560, "y": 500, "icon": "refresh-cw", "label": "AI 가 AI 를 만드는 고리"},
    "one": {"kind": "card", "x": 1360, "y": 500, "icon": "search", "label": "남은 한 칸: 무엇을 풀지"},
    "ar": {"kind": "arrow", "from": "loop", "to": "one", "color": "gold"},
    "q": {"kind": "text", "x": 960, "y": 780, "text": "그 칸마저 넘어가나?", "size": 56, "color": "gold"}},
    [{"say": "AI 가 AI 를 만든다. 이 말을 따라가다 보면 하나가 보입니다.", "do": ["loop"]},
     {"say": "이 과정에서 사람에게 남은 일은 점점 한 칸으로 줄어들고 있고, 그 칸은 무엇을 풀지 고르는 일이라는 것.", "do": ["one", "ar"]},
     {"say": "그리고 지금 AI 업계에서 가장 큰 내기는, 그 마지막 칸마저 넘어가느냐입니다.", "do": ["q", {"hi": "one"}]}],
    label="해석 · 이 영상의 주장")

# ── 2. 고리라는 말 ────────────────────────────────────────────────
chapter(1, "고리라는 말", "refresh-cw", "AI 가 만들어지는 과정을 고리 하나로 그려 보겠습니다.")
board("AI 가 만들어지는 고리", loop({
    "who": {"kind": "text", "x": 960, "y": 540, "text": "모든 칸: 사람", "size": 44},
    "eq": {"kind": "text", "x": 960, "y": 540, "text": "모든 칸을 AI 가 = 재귀적 자기개선", "size": 40, "color": "gold"},
    "q": {"kind": "text", "x": 960, "y": 540, "text": "지금 칸마다 누가?", "size": 48, "color": "gold"}}),
    [{"say": "무엇을 연구할지 문제를 고르고, 실험을 설계해 코드를 짜고, 실험을 돌려 결과를 읽고, 그걸로 다음 모델을 만듭니다. 그리고 다시 처음으로.",
      "do": ["c1", "a12", "c2", "a23", "c3", "a34", "c4", "a41"]},
     {"say": "지금까지 이 고리의 모든 칸은 사람이 맡았습니다.", "do": ["who"]},
     {"say": "한 바퀴 돌면 더 나은 모델이 나오고, 그 모델이 다음 바퀴의 연구를 도우면, 다음 바퀴는 더 빨리 돕니다.", "do": [{"hi": "c4"}, {"hi": "a41"}]},
     {"say": "이 고리의 모든 칸을 AI 가 맡게 되면, 그걸 재귀적 자기개선이라고 부릅니다.", "do": [{"hide": "who"}, "eq"]},
     {"say": "그러니 질문은 이겁니다. 지금 이 고리의 칸마다, 누가 일하고 있을까요.", "do": [{"hide": "eq"}, "q"]}],
    label=f"정의: {SRC}")

# ── 3. 숫자 옆의 각주 ─────────────────────────────────────────────
chapter(2, "숫자 옆의 각주", "file-text", "앤트로픽이 공개한 숫자는 대부분 회사가 스스로 잰 것이고, 회사는 숫자 옆에 직접 단서를 붙여 두었습니다. 숫자만큼 그 각주가 중요합니다.")
board("숫자 둘, 그리고 회사가 붙인 각주", {
    "n1": {"kind": "card", "x": 520, "y": 420, "icon": "laptop", "label": "코드의 80% 이상", "value": "80%+"},
    "f1": {"kind": "text", "x": 520, "y": 700, "text": "각주: 줄 수는 양이지 질이 아니다", "size": 34, "color": "gold"},
    "n2": {"kind": "card", "x": 1400, "y": 420, "icon": "trending-up", "label": "1인당 하루 코드 (2024 대비)", "value": "8배"},
    "f2": {"kind": "text", "x": 1400, "y": 700, "text": "각주: 거의 확실히 과장", "size": 34, "color": "gold"}},
    [{"say": "코드의 80% 이상.", "do": ["n1"]},
     {"say": "각주: 코드 줄 수는 불완전한 잣대다. 얼마나 많이 썼는지만 잴 뿐, 얼마나 잘 썼는지는 재지 못한다. 코드의 80% 가 일의 80% 는 아닙니다.", "do": ["f1"]},
     {"say": "개발자 한 사람이 하루에 합치는 코드는 2024년의 여덟 배.", "do": ["n2"]},
     {"say": "각주: 거의 확실히 과장된 숫자.", "do": ["f2", {"dim": "n2"}]}],
    label=f"{SRC} 본문·각주 · {CO}")
add({"type": "bars", "title": "프로그램 속도 올리기 과제 (몇 배 빨라졌나)", "emph": 2, "label": f"{SRC} · 사람: 숙련자 4~8시간 · {CO}",
     "items": [{"label": "숙련된 사람", "value": 4, "text": "약 4배", "t": "숙련자는"},
               {"label": "AI (2025년 5월)", "value": 3, "text": "약 3배", "t": "세"},
               {"label": "AI (2026년 4월)", "value": 52, "text": "약 52배", "t": "쉰두"}],
     "beats": [{"say": "프로그램을 빠르게 만드는 과제에서 숙련자는 몇 시간 들여 네 배쯤. AI 는 1년 사이 세 배에서 쉰두 배로."},
               {"say": "이 숫자에는 회사가 따로 각주를 달지 않았습니다."}]})
add({"type": "bignum", "label": "AP 통신 2026.09.17 보도 — 앤트로픽 발표 원문은 확인 전 · 주도 = 큰 방향만 주면 대부분을 끝까지(사람 감독 아래)",
     "small": "앤트로픽 연구개발 중 클로드가 '주도'한 몫 (보도)", "value": "26%", "compare": {"label": "2월", "value": "0%"},
     "beats": [{"say": "AP 통신은 9월, 앤트로픽이 회사 연구개발의 26% 를 클로드가 주도한다고 밝혔다고 보도했습니다. 사람이 큰 방향만 주면 대부분을 끝까지 해낸다는 뜻이고, 2월엔 0이었다고 합니다."}]})

# ── 4. 남은 한 칸 ─────────────────────────────────────────────────
chapter(3, "남은 한 칸", "user", "그럼 고리로 돌아가 칸마다 채워 보죠.")
board("칸마다, 누가", loop({
    "open": {"kind": "text", "x": 960, "y": 540, "text": "고리는 아직 안 닫힘", "size": 46, "color": "gold"}}),
    [{"say": "코드를 짜는 칸, 이미 상당 부분 AI 입니다.", "do": ["c1", "c2", "c3", "c4", "a12", "a23", "a34", "a41", {"swap": "c2", "text": "② 설계·코드 — AI"}, {"hi": "c2"}]},
     {"say": "실험을 돌리고 결과를 읽는 칸. 앤트로픽은 올해 4월, AI 에이전트들이 스스로 연구를 진행해 성능 격차의 97% 를 메웠다고 밝혔습니다. 같은 과제에서 사람 연구자 둘은 23% 였고요.", "do": [{"swap": "c3", "text": "③ 실험·결과 — AI 97%"}, {"hi": "c3"}]},
     {"say": "그런데 이 시연에도 회사가 직접 붙인 각주가 있습니다. 문제를 고른 것도, 채점 기준을 만든 것도 사람이었다.", "do": [{"swap": "c1", "text": "① 문제 고르기 — 사람"}, {"hi": "c1"}]},
     {"say": "그리고 이 결과는 실제로 서비스하는 큰 모델에는 그대로 옮겨지지 않았다고 했습니다.", "do": [{"swap": "c4", "text": "④ 다음 모델 — 아직"}, {"dim": "a41"}]},
     {"say": "그래서 지금의 고리는 이렇게 생겼습니다. 여러 칸에 AI 가 들어갔지만, 고리의 출발점, 무엇을 풀지 고르는 칸에는 아직 사람 손이 남아 있습니다.", "do": ["open"]}],
    label=f"{SRC} 자율 연구 시연(2026.04) · {CO} · 마지막 문장은 해석")
quote("앤트로픽", "회사 원문 · 자율 연구 시연의 각주 (2026)",
      "문제를 고른 것도, 채점 기준을 만든 것도 여전히 사람이었다.", "humans still chose the problem and created the scoring rubric", "사람",
      ["회사 스스로 적은 이 한 줄이, 지금 고리의 모양을 가장 정확하게 보여 줍니다."], f"{SRC}", insight=False)
quote("고팔 사르마 외", "랜드연구소 보고서 (2026.10.12)",
      "스스로 연구 의제를 정하거나 자기 후계 모델을 설계한다고 공개된 시스템은 없다.", "no disclosed system sets its own research agenda or designs its own successors", "연구 의제",
      ["회사 밖에서 본 결론도 같습니다. 미국 랜드연구소는 지난달 보고서에서, 여러 연구소가 새 코드 대부분을 AI 가 쓴다고 밝히고 있지만, 스스로 연구 의제를 정하거나 자기 후계 모델을 설계한다고 공개된 시스템은 아직 없다고 정리했습니다."],
      f"RAND 'Recursive Self-Improvement and Automated AI R&D' (PE-A5068-1) · {OP}")

# ── 5. 그 칸도 넘어간다는 사람들 ────────────────────────────────────
chapter(4, "그 칸도 넘어간다는 사람들", "trending-up", "그런데 이 마지막 칸도 곧 넘어간다고 보는 사람들이 있습니다. 근거는 셋입니다.")
add({"type": "bignum", "insight": True, "label": f"{SRC} 연구 감각 시험 (n=129, 2026.04) · 대조 묶음 127개 · {CO}",
     "small": "AI 제안이 연구자 선택보다 낫다는 판정", "value": "64%", "compare": {"label": "조건 없이 고른 비교", "value": "약 20%"},
     "beats": [{"say": "첫째, 연구 감각. 앤트로픽은 연구자가 갈림길에서 고른 선택과 AI 의 제안을 비교했습니다. AI 쪽이 낫다는 판정이 64% 였죠."},
               {"say": "다만 사람이 고칠 여지가 있던 장면만 고른 시험이었고, 조건 없이 고른 비교에서는 20% 정도였습니다. 무엇을 할지 고르는 감각이 시험대에 오르기 시작했다는 것, 그리고 아직은 조건이 붙어 있다는 것. 둘 다 사실입니다."}]})
quote("드루브 스리칸스 외", "논문 'Recursive self-improvement of AI research agents' (arXiv 2026.09.22)",
      "8일 동안 사람 없이, 일곱 번 연달아 개선을 찾았다.", "seven successive improvements", "일곱 번",
      ["둘째, 스스로를 고치는 에이전트. 9월에 나온 한 논문에서는 AI 연구 에이전트가 자기 연구 코드를 고치고, 더 나은 판만 남기는 일을 8일 동안 사람 없이 되풀이해, 일곱 번 연달아 개선을 찾아냈습니다. 작은 규모이고 아직 동료 심사 전입니다."],
      "arXiv 2609.26457 (동료 심사 전)", insight=False)
quote("드와케시 파텔", "AI 인터뷰 진행자 · 글 'RSI objections' (2026.11.24)",
      "최고 수준 AI 연구자를 완전히 자동화하는 해, 중앙값 2028년.", "my median year for fully automating the best AI researchers is 2028", "2028",
      ["셋째, 시간표. AI 연구자 인터뷰로 알려진 드와케시 파텔은 이번 주 글에서, 최고 수준의 AI 연구자를 완전히 자동화하는 해를 2028년쯤으로 본다고 했습니다.",
       "그 말대로라면, 무엇을 풀지 고르는 사람도 그 안에 들어갑니다."],
      f"dwarkesh.com/p/rsiobjections · {OP}")

# ── 6. 경고를 의심하는 사람들 ──────────────────────────────────────
chapter(5, "경고를 의심하는 사람들", "eye", "반대편에는 이 이야기 자체를 의심하는 사람들이 있습니다.")
board("반론", {
    "m": {"kind": "card", "x": 400, "y": 470, "icon": "target", "label": "가속 증거가 약하다"},
    "g": {"kind": "card", "x": 960, "y": 470, "icon": "cpu", "label": "GPU 가 속도를 막는다"},
    "r": {"kind": "card", "x": 1520, "y": 470, "icon": "file-text", "label": "아무도 체계적으로 보고 안 함"},
    "s": {"kind": "text", "x": 960, "y": 760, "text": "경고 = 규제를 유리하게? (색스 등)", "size": 40, "color": "gold"}},
    [{"say": "파텔의 같은 글에는 반론도 모여 있습니다. AI 가 더 빨라지고 있다는 증거는 한 연구소의 짧은 측정에 기대고 있고, 결국 비싼 GPU 가 속도를 막을 거라는 지적입니다.", "do": ["m", "g"]},
     {"say": "랜드연구소도, AI 가 연구를 얼마나 빠르게 만들고 있는지는 아무도 체계적으로 보고하지 않아 알기 어렵다고 했습니다.", "do": ["r"]},
     {"say": "그리고 정치 쪽의 비판. 백악관 AI 자문 데이비드 색스를 비롯한 비판자들은, AI 회사들의 위험 경고가 규제를 자기들에게 유리하게 짜려는 시도라고 말합니다. 경고하는 회사가 동시에 가장 앞서 달리는 회사라는 점을 짚는 거죠.", "do": ["s"]}],
    label=f"드와케시 파텔 'RSI objections' (2026.11.24, 반론 요약) · RAND (2026.10.12) · AP (2026.09.27) 보도 · {OP}")

# ── 7. 지켜볼 신호 하나 ──────────────────────────────────────────
chapter(6, "지켜볼 신호 하나", "flag", "앤트로픽은 앞으로의 길을 셋으로 나눴습니다.")
board("세 갈래 길", {
    "p1": {"kind": "card", "x": 400, "y": 460, "icon": "timer", "label": "추세가 멈춤"},
    "p2": {"kind": "card", "x": 960, "y": 460, "icon": "trending-up", "label": "사람이 방향, 효율은 복리"},
    "p3": {"kind": "card", "x": 1520, "y": 460, "icon": "refresh-cw", "label": "고리가 완전히 닫힘"},
    "now": {"kind": "text", "x": 960, "y": 660, "text": "회사: 지금은 여기", "size": 36, "color": "gold"},
    "un": {"kind": "text", "x": 1520, "y": 660, "text": "가장 불확실", "size": 36},
    "ps": {"kind": "text", "x": 960, "y": 820, "text": "제안: 멈출 수 있는 선택지 + 확인할 방법", "size": 38, "color": "gold"}},
    [{"say": "추세가 멈추는 길, 사람이 방향을 정한 채 효율이 계속 쌓이는 길, 그리고 고리가 완전히 닫히는 길.", "do": ["p1", "p2", "p3"]},
     {"say": "회사는 지금 두 번째 길에 있다고 봤고, 세 번째가 가장 불확실하다고 했습니다.", "do": ["now", {"hi": "p2"}, "un"]},
     {"say": "그리고 필요하면 최전선 AI 개발을 늦추거나 잠시 멈출 선택지가 세상에 있어야 한다고 덧붙였습니다.", "do": ["ps"]}],
    label=SRC)
add({"type": "bignum", "label": f"METR 측정 (앤트로픽 원문 인용) · 마지막 문장은 해석",
     "small": "AI 가 혼자 해내는 일의 길이", "value": "4개월마다 2배",
     "beats": [{"say": "이 이야기가 우리 일과 닿는 곳도 같은 칸입니다. 외부 측정에 따르면 AI 가 혼자 해내는 일의 길이는 넉 달마다 두 배로 늘고 있습니다."},
               {"say": "그렇다면 일하는 사람에게 오래 남는 칸도 고리의 첫 칸을 닮아 갈 겁니다. 무엇을 풀지 고르고, 무엇을 잘했다고 칠지 정하는 일."}]})
board("지켜볼 신호", loop({
    "sig": {"kind": "text", "x": 960, "y": 540, "text": "신호: 스스로 연구 의제를 정하는 시스템 — 아직 공개 전", "size": 34, "color": "gold"}}),
    [{"say": "그럼 이 영상의 해석은 언제 틀리게 될까요. 신호는 하나입니다.", "do": ["c1", "c2", "c3", "c4", "a12", "a23", "a34", "a41", {"swap": "c1", "text": "① 문제 고르기 — 사람"}, {"hi": "c1"}]},
     {"say": "랜드연구소가 아직 없다고 한 것. 스스로 연구 의제를 정하는 시스템이 공개되는 날입니다.", "do": ["sig"]},
     {"say": "그날이 오면 고리의 마지막 칸이 넘어간 것이고, 그때부터 AI 뉴스는 지금과 전혀 다른 뉴스가 될 겁니다.", "do": [{"swap": "c1", "text": "① 문제 고르기 — ?"}]}],
    label="RAND (2026.10.12) · 해석")

R12, R70 = "manual/12-visual-storytelling.md", "docs/70-science-explainer-reference.md"
DEC = {
 1: ("metric", "share", [("bignum", "80% 가 '전체 중 몫'이라 막대 하나에 채워야 크기가 보임(S4)"), ("isotype", "100칸 그림은 '코드'라는 대상과 맞는 그림이 없음")], "숫자를 원래 대상(코드 전체) 위에 몫으로", "80% 라는 크기를 눈으로 잡음"),
 2: ("explain", "motionboard", [("stage", "삽화가 아니라 개념 연결"), ("analogy", "비유가 아니라 이 영상의 주장")], "통찰 한 줄을 카드 둘과 질문 하나로", "이 영상이 무엇을 따라가는지 앎"),
 4: ("explain", "motionboard", [("map_causal", "인과 지도는 갈래가 많을 때 — 여기는 닫힌 고리 하나(D1 기준 화면)"), ("timeline", "순서가 아니라 순환")], "3Blue1Brown 식 기준 그림: 고리 하나를 끝까지 들고 감(S1·S3·S6)", "재귀적 자기개선이 고리의 모든 칸을 AI 가 맡는 것임을 앎"),
 6: ("metric", "motionboard", [("bars", "두 숫자의 단위가 다름(몫·배수) — 같은 축에 못 놓음"), ("bignum", "숫자보다 옆의 각주가 핵심이라 둘을 한 화면에")], "숫자 카드 옆에 회사 각주가 붙는 순서(A2)", "회사 숫자에 회사 스스로 단서를 달았음을 앎"),
 7: ("compare", "bars", [("bignum", "사람 대비 AI 의 크기 차이는 같은 축 막대가 정확(E5)"), ("versus", "두 주장의 맞대기가 아님")], "사람 4배 · AI 3배 → 52배를 같은 축에", "1년 사이 변화의 크기를 앎"),
 8: ("metric", "bignum", [("share", "26% 는 보도 숫자라 크게 강조하되 출처 표시가 중요"), ("chart", "두 시점뿐")], "보도 숫자를 2월 0% 와 나란히", "반년 만의 변화를 앎"),
 10: ("explain", "motionboard", [("map_causal", "고리 그림을 다시 써야 '같은 그림 위 변화'가 됨(D1)"), ("checklist", "칸마다 상태 바뀜이 핵심 — 목록이 아님")], "A3: 같은 고리의 칸 라벨이 하나씩 바뀌고 ①만 사람으로 남음 — 기억할 한 장면", "고리의 첫 칸이 아직 사람임을 기억"),
 11: ("said", "quote", [("bite", "원본 영상 없음 — 회사 글"), ("motionboard", "원문 한 줄을 그대로 보여 줘야 함")], "회사의 각주를 원문 그대로", "회사 스스로 인정한 한계를 앎"),
 12: ("said", "quote", [("bite", "보고서라 영상 없음"), ("versus", "같은 쪽(남는다) 근거")], "회사 밖 기관의 같은 결론을 원문으로(11 §3-3 뒷받침)", "독립 기관도 같은 결론임을 앎"),
 14: ("compare", "bignum", [("bars", "두 값이지만 조건이 다른 두 시험 — 막대로 같은 축이면 오해"), ("versus", "두 사람의 주장이 아님")], "64% 와 조건 없는 20% 를 나란히(E5) — 반박 근거와 그 조건", "연구 감각 시험의 크기와 조건을 함께 앎"),
 15: ("said", "quote", [("bite", "논문이라 영상 없음"), ("bignum", "숫자보다 '사람 없이 8일'이 핵심")], "반박 쪽 근거를 원문 구절로", "스스로 고치는 실험이 실제로 있음을 앎"),
 16: ("said", "quote", [("bite", "팟캐스트 원본 구간 미확인 — 글로 인용"), ("bignum", "숫자보다 누구의 시간표인지가 중요")], "반박 쪽 시간표를 이름 있는 사람의 말로", "그 칸이 넘어간다는 쪽의 시간표를 앎"),
 18: ("compare", "motionboard", [("checklist", "반론 셋과 다른 축(색스)을 공간으로 나눠야 함"), ("versus", "셋 이상")], "반론 카드 셋 + 저울 밖 비판 하나", "의심하는 쪽의 근거를 앎"),
 20: ("compare", "motionboard", [("timeline", "시간 순서가 아니라 갈래"), ("versus", "셋")], "세 갈래를 같은 크기로, 회사 위치 표시", "회사가 보는 현재 위치를 앎"),
 21: ("metric", "bignum", [("chart", "곡선 데이터를 직접 갖고 있지 않음"), ("bars", "비교 대상 없음")], "외부 측정 한 줄을 크게 — 내 일과의 연결", "AI 가 맡는 일의 길이가 빨리 늘고 있음을 앎"),
 22: ("explain", "motionboard", [("checklist", "신호는 하나"), ("map_causal", "처음 고리로 돌아와야 수미상관(D5)")], "처음 고리의 ① 칸으로 돌아와 '?'로 바뀜", "앞으로 무엇을 보면 되는지 앎"),
}
DIFF = {6: "장면 1 은 몫 하나라 share, 여기는 숫자 둘과 각주가 한 화면이라 카드 무대",
        8: "앞의 숫자들은 회사 원문, 여기는 보도 숫자라 출처를 크게 단 bignum",
        14: "장면 7 은 같은 단위의 크기 비교라 bars, 여기는 조건이 다른 두 값이라 나란한 bignum",
        18: "장면 14 는 숫자 맞대기, 여기는 반론의 종류를 공간으로 나눔",
        20: "장면 18 은 반론 카드, 여기는 회사가 나눈 길 셋",
        21: "장면 1·8 과 달리 외부 기관 측정 한 줄",
        12: "장면 11 은 회사 원문, 여기는 회사 밖 기관 — 같은 틀로 나란히",
        15: "장면 11·12 는 '남는다' 쪽, 여기는 '넘어간다' 쪽 근거 — 같은 인용 틀로 무게를 맞춤",
        16: "같은 '넘어간다' 쪽의 다른 근거(시간표)",
        22: "장면 10 의 고리를 다시 불러 수미상관"}
REC = {1: ("footage", "추천이 틀림 — 이 주제엔 쓸 자료 화면이 없고(실험실 녹화 없음), 몫은 막대가 정확"),
       4: ("footage", "추천이 틀림 — 보이지 않는 과정이라 실사가 없음, 고리 그림이 기준 화면"),
       6: ("chart", "추천이 틀림 — 시계열이 아니라 숫자와 각주의 짝"),
       7: ("zoomshot", "실제 화면 녹화가 없음 — 수치 비교라 막대"),
       8: ("bite", "원본 영상이 아닌 통신 보도 숫자"),
       12: ("footage", "추천이 틀림 — 보고서라 자료 영상 없음, 원문 한 줄이 증거"),
       16: ("kb", "인물 사진 권리 미확인 — 이름·원문 인용 카드로"),
       18: ("kinetic", "키네틱은 훅·결론 한 문장용 — 여기는 반론 셋을 나란히 보여야 함"),
       22: ("footage", "추천이 틀림 — 처음 고리 그림으로 돌아와야 수미상관")}
for sc in S:
    if sc["type"] == "chapter":
        continue
    sit, pick, over, why, intent = DEC[sc["id"]]
    if sc["id"] in REC:
        over = [REC[sc["id"]]] + list(over)
    assert pick == sc["type"], (sc["id"], pick, sc["type"])
    sc["decide"] = {"situation": sit, "pick": pick, "over": [{"id": a, "why_not": b} for a, b in over], "why": why, "intent": intent, "refs": [R12, R70]}
    if sc["id"] in DIFF:
        sc["decide"]["differs"] = DIFF[sc["id"]]

spec = {
    "asof": "2026년 11월 25일", "brand": "ai", "zoom": "off", "tts_rate": "-4%",
    "title": "AI 가 다음 AI 를 만들기 시작했다 — 사람에게 남은 마지막 칸",
    "core_message": "AI 가 AI 를 만드는 고리에서 사람에게 남은 마지막 칸은 '무엇을 풀지 고르는 일'이고, 업계의 진짜 질문은 그 칸마저 넘어가느냐다.",
    "question": "AI 가 다음 AI 를 만든다는 건 어디까지 사실일까?",
    "logic": ["고리 그림으로 정의", "회사 숫자와 회사의 각주", "칸마다 누가: 첫 칸은 아직 사람", "넘어간다는 쪽의 근거 셋", "의심하는 쪽", "세 갈래와 지켜볼 신호"],
    "compare_to": ["숙련자 약 4배 대비 AI 3배 → 52배", "연구 감각 64% 대비 조건 없는 비교 약 20%", "2월 0% 대비 26% (보도)"],
    "analogies": ["AI 가 만들어지는 과정 = 네 칸짜리 고리"],
    "past_cases": ["2025년 5월 Claude Opus 4 의 최적화 과제 약 3배"],
    "glossary": [{"term": "재귀적 자기개선", "plain": "AI 가 자기 다음 모델을 처음부터 끝까지 스스로 만드는 일이 되풀이되는 것"},
                 {"term": "METR", "plain": "AI 가 혼자 해내는 과제 길이를 재는 외부 평가 기관"}],
    "footage": {"anthropic": {"credit": SRC, "url": "https://www.anthropic.com/institute/recursive-self-improvement", "license": "인용"},
                "rand": {"credit": "RAND PE-A5068-1 (2026.10.12)", "url": "https://www.rand.org/pubs/perspectives/PEA5068-1.html", "license": "인용"},
                "dwarkesh": {"credit": "Dwarkesh Patel (2026.11.24)", "url": "https://www.dwarkesh.com/p/rsiobjections", "license": "인용"}},
    "direction": {"pick": "dark-stage 설명 무대 + 고리 기준 그림 하나 + 이름 있는 시각 인용 (3Blue1Brown 원리 해설)",
                  "over": [{"id": "hook-shorts", "why_not": "실제 화면 녹화 중심 — 이 주제는 원리·구조가 주인공"},
                           {"id": "news-desk", "why_not": "소식 나열이 아니라 한 질문(어느 칸이 남나)을 따라감"}],
                  "why": "보이지 않는 과정(연구 → 모델)을 고리 그림 하나로 잡고 끝까지 같은 그림 위에서 칸을 바꿈 — docs/70 S1·S3·S6",
                  "intent": "끝나면 시청자가 이런 뉴스를 '닫힌 고리냐, 짧아지는 손이냐'로 읽음",
                  "vocabulary": ["share", "motionboard", "bars", "bignum", "quote", "chapter"],
                  "refs": [R12, R70, "manual/11-workflow.md"]},
    "scenes": S,
}
(HERE / "hybrid.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(S), "장면")
