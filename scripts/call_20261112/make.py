"""코어위브 3분기 어닝콜 해부 (v18): 무엇을 말했나(원문) → 무엇으로 이어지나 → 무슨 뜻인가 (해석은 해석이라고 밝힘).
    python -m ytflow earnings-call 20261112-market-call <공식 녹취록 PDF> --ticker CRWV --period 3Q26
    python scripts/call_20261112/make.py && python -m ytflow hybrid 20261112-market-call
원문: 코어위브 IR 공식 녹취록 (Proofread Transcript) — 01_research/earnings/CRWV_3Q26.txt
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
P = ROOT / "projects" / "20261112-market-call"
SRC = ROOT / "projects" / "20261112-market-daily"
TR = "https://s205.q4cdn.com/133937190/files/content_files/CoreWeave-3Q26-Transcript-_1_.pdf"
AS_OF = "11월 10일 어닝콜 · 11월 12일 기준"
LBL = "코어위브 3분기 어닝콜 공식 녹취록 (2026.11.10)"


def B(*says):
    return [{"say": s} for s in says]


def main():
    for d in ("01_research", "02_script", "05_edit", "04_assets/footage/raw"):
        (P / d).mkdir(parents=True, exist_ok=True)
    for f in (SRC / "04_assets/footage").glob("*.mp4"):
        if not (P / "04_assets/footage" / f.name).exists():
            shutil.copy(f, P / "04_assets/footage" / f.name)
    for f in (SRC / "04_assets/footage/raw").iterdir():
        if not (P / "04_assets/footage/raw" / f.name).exists():
            shutil.copy(f, P / "04_assets/footage/raw" / f.name)
    fo = json.loads((SRC / "02_script/hybrid.json").read_text(encoding="utf-8"))["footage"]
    for f in ("edit.yaml",):
        if not (P / f).exists():
            (P / f).write_text("# 어닝콜 해부 (시장) — manual v18 §0-1\nedit:\n  style: hybrid\n  style_ref: hybrid\n  family: source\nchannel: ch-market-daily\nformat: longform\n", encoding="utf-8")
    if not (P / "state.json").exists():
        (P / "state.json").write_text(json.dumps({"name": P.name, "created": "2026-11-12T00:00:00", "done": [], "approved": []}, indent=2), encoding="utf-8")

    S = []
    s = S.append
    s(dict(type="intro", chapter=0, series="어제 시장, 오늘 아침", as_of=AS_OF, bg_src="dc", agenda_beat=3,
           title_lines=["코어위브 경영진은", "무엇을 말했나"],
           layers=[{"kind": "photo", "src": "dc", "beat": 2, "side": "right", "w": 600, "top": 250, "caption": "데이터센터 예시 · CC BY 4.0 Hay Kranen"}],
           beats=B("안녕하세요. 어제 시장을 오늘 아침에 정리해 드리는, 어제 시장 오늘 아침입니다.",
                   "오늘은 11월 12일 기준으로, 반도체를 하루에 5% 넘게 띄운 코어위브의 어닝콜에서 경영진이 실제로 무슨 말을 했는지 들여다봅니다.",
                   "빚 걱정에 주가가 한 달 새 크게 빠져 있던 회사입니다. 그런데 CEO는 실적 숫자보다 먼저, 돈을 어떻게 마련하는지부터 꺼냈습니다. 무엇을 말했을까요?",
                   "이런 순서로 보겠습니다. 숫자와 약속, 경영진이 한 말 다섯 가지, 그 말이 무엇으로 이어지는지, 그리고 남은 숙제까지요.",
                   "시작하겠습니다.")))
    s(dict(type="bars", chapter=0, label="야후 파이낸스 종가 · 2026.11.10 → 11.11", title="어닝콜 다음 날 (%)", unit="", emph=0,
           layers=[{"kind": "locator", "at": [-74.31, 40.79], "label": "코어위브 본사 · 미국 뉴저지", "beat": 0, "side": "right", "top": 170, "scale": 2.2}],
           items=[{"label": "코어위브", "value": 24.71, "text": "+24.7"}, {"label": "마이크론", "value": 11.89, "text": "+11.9"},
                  {"label": "오라클", "value": 8.81, "text": "+8.8"}, {"label": "반도체 지수", "value": 5.66, "text": "+5.7"}],
           beats=B("먼저 결과부터 보죠. 어닝콜 다음 날 코어위브는 24.7% 올랐고, 마이크론과 오라클, 반도체 지수까지 함께 올랐습니다.",
                   "어닝콜은 실적을 발표한 뒤 경영진이 투자자, 애널리스트와 통화하며 질문에 답하는 자리입니다. 숫자 뒤의 이유와 앞으로의 약속이 여기서 나오죠.")))
    # 1. 숫자와 약속
    s(dict(type="chapter", chapter=1, num="1", title="숫자와 약속", icon="chart-line", look="dash",
           beats=B("먼저 숫자와, 회사가 내놓은 약속입니다.")))
    s(dict(type="bignum", chapter=1, label=LBL, small="3분기 매출 약 37억 달러 · 1년 전보다", value="+168%",
           compare={"label": "회사 전망치", "value": "상단 넘음"},
           beats=B("3분기 매출은 약 37억 달러, 1년 전보다 168% 늘었습니다.",
                   "회사가 앞서 내놓은 전망치의 가장 높은 값도 넘었고, 한 분기 만에 10억 달러 넘게 늘었습니다.")))
    s(dict(type="bars", chapter=1, label=LBL + " · 조정 영업이익률", title="조정 영업이익률 (%)", unit="%", emph=2, fx=["tilt"],
           items=[{"label": "1분기", "value": 1, "text": "1"}, {"label": "2분기", "value": 5, "text": "5"}, {"label": "3분기", "value": 10, "text": "10"}],
           beats=B("더 눈에 띄는 건 남는 돈의 비율, 조정 영업이익률입니다. 1분기 1%, 2분기 5%, 그리고 3분기 10%.",
                   "회사가 연초에 세운 계획보다 한 분기 빨랐습니다. CFO는 영업이익이 두 분기 만에 세 배가 되는 동안 이자는 3분의 1 늘었다며, 이게 이익으로 가는 길이라고 했습니다.")))
    s(dict(type="checklist", chapter=1, label=LBL + " · 가이던스", title="회사가 내놓은 약속",
           rows=[{"label": "올해 매출 130억~133억 달러로 상향", "state": "ok"},
                 {"label": "연말 연간 환산 매출 200억~210억 달러", "state": "ok"},
                 {"label": "조정 순이익 흑자: 2028년 상반기", "state": "warn"}],
           beats=[{"say": "약속도 올렸습니다. 올해 매출 전망을 130억에서 133억 달러로, 연말 기준 1년 치로 환산한 매출은 200억에서 210억 달러로 제시했습니다.", "upto": 2},
                  {"say": "그리고 조정 순이익 기준 흑자는 2028년 상반기로 잡았습니다. 아직은 적자라는 뜻이기도 하죠. 이건 뒤에서 다시 보겠습니다.", "upto": 3}]))
    # 2. 경영진이 한 말 다섯 가지 (원문 + 번역) — 사용자 판정 2026-11-12: 애널리스트 이야기보다 경영진의 주된 말을 명확하게
    s(dict(type="chapter", chapter=2, num="2", title="경영진이 한 말 다섯 가지", icon="messages-square", look="photo", bg_src="dc",
           beats=B("이제 이번 어닝콜의 핵심, 경영진이 직접 한 말입니다. 크게 다섯 가지였습니다.")))
    s(dict(type="quote", chapter=2, label=LBL, who="마이크 인트레이터", role="코어위브 CEO · ① 돈은 이렇게 마련한다",
           quote="지금 금리로는 무담보 채권으로 돈을 빌리지 않겠습니다. 그럴 필요도 없습니다.", keyword="그럴 필요도 없습니다",
           orig="we will not use the unsecured debt market to fund our business at current yields. Nor do we need to.",
           beats=B("첫째는 돈입니다. 최근 시장이 가장 걱정한 게 AI 데이터센터 회사들의 빚이었죠.",
                   "CEO는 이렇게 말했습니다. 지금 금리로는 담보 없는 채권으로 돈을 빌리지 않겠다, 그럴 필요도 없다.")))
    s(dict(type="checklist", chapter=2, label=LBL, title="그럼 돈은 어디서?", fx=["tilt"],
           rows=[{"label": "고객이 미리 내는 돈 — 앞으로 3개월 약 90억 달러", "state": "ok"},
                 {"label": "고객 계약에 묶은 담보 대출 — 계약이 끝날 때 다 갚도록", "state": "ok"},
                 {"label": "평균 차입 금리 7.9% — 1년 새 2.5%p 낮아짐", "state": "ok"},
                 {"label": "2027년까지 회사 차원의 새 조달 50억 달러 미만", "state": "ok"}],
           beats=[{"say": "그럼 돈은 어디서 나올까요? 가장 큰 건 고객이 미리 내는 돈입니다. 앞으로 3개월 동안만 약 90억 달러, 올해 계약의 70%에서 선지급을 받았습니다.", "upto": 1},
                  {"say": "나머지는 고객 계약 하나하나에 묶은 담보 대출입니다. 계약이 끝날 때쯤 빚도 다 갚도록 짜여 있죠. 평균 차입 금리는 7.9%로 1년 새 2.5%포인트 낮아졌습니다.", "upto": 3},
                  {"say": "그래서 2027년까지 회사 차원에서 새로 구할 돈은 50억 달러가 안 된다고 했습니다.", "upto": 4}]))
    s(dict(type="quote", chapter=2, label=LBL, who="마이크 인트레이터", role="코어위브 CEO · ② 수요는 넘친다",
           quote="2027년 말까지 공급할 수 있는 용량보다 검증된 수요가 10배 많습니다.", keyword="10배",
           orig="We have 10x as much qualified demand as available capacity through the end of 2027.",
           beats=B("둘째는 수요입니다. 데이터센터가 너무 많이 지어져서 곧 남아돌 거라는 시각에 대한 답이었습니다.",
                   "CEO는 수요가 공급 가능한 용량의 10배라고 했고, 줄 선 고객에게 다 팔 수도 있지만 더 좋은 조건을 위해 일부러 기다리고 있다고까지 말했습니다.")))
    s(dict(type="quote", chapter=2, label=LBL, who="마이크 인트레이터", role="코어위브 CEO · ③ 옛 장비가 더 비싸게 팔린다",
           quote="처음 들여놓은 클라우드 설비가 웃돈을 받고 다시 계약되고 있습니다.", keyword="웃돈",
           orig="Our original fleet of cloud infrastructure is recontracting at premiums.",
           beats=B("셋째는 가격입니다. CEO는 처음 들여놓은 설비가 웃돈을 받고 다시 계약되고 있다고 했습니다.",
                   "GPU가 몇 년 만에 값어치를 잃는다는 걱정에 대한 답이었죠.")))
    s(dict(type="bignum", chapter=2, label=LBL, small="옛 세대 GPU(암페어·호퍼) 이용료 · 지난 분기보다", value="+30~50%",
           compare={"label": "2027년 재계약 시 추가 투자 없이", "value": "연 약 40억 달러"},
           beats=B("실제로 몇 년 된 옛 세대 GPU의 이용료가 지난 분기보다 30에서 50% 올랐고, 원래 계약보다도 비싸게 다시 팔렸습니다. 새 계약 가격도 7월에 약 25%, 이어서 10%를 더 올렸다고 했습니다.",
                   "2027년에 계약이 끝나는 GPU 13만 개를 지금 가격으로 다시 계약하면, 추가 투자 없이 1년에 40억 달러 가까운 매출이 생긴다고 했습니다.")))
    s(dict(type="quote", chapter=2, label=LBL, who="니틴 아그라왈", role="코어위브 CFO · ④ 성장보다 수익",
           quote="우리는 무슨 대가를 치르더라도 성장만 하는 회사가 아닙니다.", keyword="성장만",
           orig="We are not a growth-at-all-costs business.",
           beats=B("넷째는 절제입니다. CFO는 무슨 대가를 치르더라도 성장만 하는 회사가 아니라고 못 박았습니다.",
                   "계약과 설비가 확정된 뒤에야 돈의 대부분을 쓰고, 계약 하나하나가 비용을 다 덮고 이익이 남도록 짠다는 설명이었습니다.")))
    s(dict(type="quote", chapter=2, label=LBL, who="마이크 인트레이터", role="코어위브 CEO · ⑤ 고객이 넓어진다",
           quote="이제 포춘 500대 기업의 10%가 코어위브 고객입니다.", keyword="10%",
           orig="10% of Fortune 500 companies are now CoreWeave customers.",
           beats=B("다섯째는 고객입니다. 몇몇 AI 연구소에 기대는 회사라는 우려에 대해, CEO는 포춘 500대 기업의 10%가 이제 고객이라고 했습니다.",
                   "올해 새 고객의 절반 넘게가 AI 연구소나 기술 회사가 아닌 다른 업종이었다는 숫자도 함께 내놓았습니다.")))
    s(dict(type="recap", chapter=2, title="경영진이 한 말, 다섯 줄", label="코어위브 3분기 어닝콜 공식 녹취록 정리",
           items=["돈: 무담보 빚 대신 고객 선지급금·계약 담보 대출", "수요: 공급 가능한 용량의 10배",
                  "가격: 옛 장비도 웃돈 받고 재계약", "절제: 계약이 확정된 뒤에 투자",
                  "고객: 포춘 500의 10%, 새 고객 절반은 AI 밖"], new_from=0,
           beats=B("정리하면 다섯 줄입니다. 돈은 빚 대신 고객과 계약에서, 수요는 공급의 10배, 옛 장비도 웃돈을 받고, 투자는 계약이 확정된 뒤에, 그리고 고객은 AI 밖으로 넓어지고 있다.",
                   "실적 숫자보다, 시장이 걱정하던 바로 그 지점들에 경영진이 숫자를 붙여 답했다는 게 이번 어닝콜의 핵심이었습니다.")))
    # 3. 무엇으로 이어지나 (해석)
    s(dict(type="chapter", chapter=3, num="3", title="무엇으로 이어지나", icon="git-branch", look="board", sub="여기서부터는 해석입니다",
           beats=B("여기서부터는 해석입니다. 이 답들이 시장 전체에는 어떤 의미였을까요?")))
    s(dict(type="map_causal", chapter=3, look="board", label="자체 해석 · 근거: 어닝콜 녹취록 · 11월 11일 시세",
           beats=[{"say": "첫째, 고객이 돈을 미리 낸다는 건 수요가 말뿐이 아니라는 신호입니다. 그래서 같은 빚 걱정을 받던 오라클 같은 회사들까지 함께 숨을 돌렸습니다.",
                   "reveal": ["prepay", "real", "orcl"], "draw": [["prepay", "real"], ["real", "orcl"]], "active": "real"},
                  {"say": "둘째, 옛 GPU 값이 오른다면 AI에 들어간 투자를 더 오래 회수할 수 있습니다. GPU가 몇 년 만에 쓸모없어진다는 걱정을 한 번 반박한 셈이죠.",
                   "reveal": ["oldgpu", "payback"], "draw": [["oldgpu", "payback"]], "active": "payback"},
                  {"say": "셋째, 수요가 공급의 10배라면 칩과 메모리는 계속 필요합니다. 마이크론이 오르고, 한국의 SK하이닉스와 삼성전자가 주목받는 이유로 이어집니다.",
                   "reveal": ["demand", "memory"], "draw": [["demand", "memory"]], "active": "memory"}]))
    s(dict(type="analogy", chapter=3, label="자체 정리 (비유)", title="빚 대신 선지급금",
           left={"icon": "landmark", "label": "은행 대출로 짓기", "sub": "다 지은 뒤 팔리길 기다림"},
           right={"icon": "building-2", "label": "분양 대금으로 짓기", "sub": "살 사람이 먼저 돈을 냄"},
           result={"icon": "circle-check", "label": "수요가 진짜인지 돈으로 확인"},
           beats=[{"say": "비유하면 아파트입니다. 은행 대출만으로 지어 놓고 팔리길 기다리는 것과, 살 사람에게 분양 대금을 먼저 받고 짓는 것의 차이죠."},
                  {"say": "뒤쪽은 수요가 진짜라는 걸 돈으로 확인한 겁니다. 시장이 이번 콜에 안도한 핵심이 바로 이 부분이라고 봅니다.", "show_result": True}]))
    s(dict(type="versus", chapter=3, label="야후 파이낸스 종가 · 2026.11.11 → 11.12 · 해석",
           left={"value": "+", "label": "AI 수요 (코어위브 콜)", "icon": "trending-up"}, right={"value": "−", "label": "엔비디아 CEO 거취 보도", "icon": "trending-down"},
           beats=B("한국 투자자에게는 이 그림이 중요합니다. 한쪽엔 AI 수요가 크다는 확인, 다른 쪽엔 장 마감 뒤 나온 엔비디아 CEO 거취 보도가 있습니다.",
                   "오늘 SK하이닉스가 1.8% 내린 건, 두 힘이 부딪친 결과로 볼 수 있습니다. 수요는 그대로인데, 가장 큰 고객 중 하나인 엔비디아의 불확실성이 커진 거죠.")))
    # 4. 남은 숙제
    s(dict(type="chapter", chapter=4, num="4", title="남은 숙제", icon="circle-alert", look="dash",
           beats=B("그렇다고 좋은 이야기만 있었던 건 아닙니다.")))
    s(dict(type="checklist", chapter=4, label=LBL + " · 투자 권유가 아닙니다", title="남은 숙제",
           layers=[{"kind": "photo", "src": "dc", "beat": 0, "side": "right", "w": 460, "top": 610, "caption": "데이터센터 예시 · CC BY 4.0 Hay Kranen"}],
           rows=[{"label": "순손실 7억 900만 달러 — 1년 전 1억 1천만 달러보다 커짐", "state": "warn"},
                 {"label": "이자 비용 8억 4,600만 달러 — 1년 새 약 2.7배", "state": "warn"},
                 {"label": "4분기 이자 비용 10억 5천만~11억 5천만 달러 예상", "state": "warn"}],
           beats=[{"say": "3분기 순손실은 7억 900만 달러로 1년 전보다 커졌습니다. 이자 비용도 8억 4,600만 달러로 1년 새 2.7배가 됐죠.", "upto": 2},
                  {"say": "4분기 이자 비용은 10억 달러를 넘을 걸로 예상했습니다. 영업에서 남는 돈이 이자를 이길 만큼 빨리 커지느냐, 이게 이 회사의 진짜 시험입니다.", "upto": 3}]))
    s(dict(type="kinetic", chapter=4, beats=[{"say": "정리하면, 숫자보다 답이 시장을 움직인 어닝콜이었습니다.", "hit": ["숫자보다", "답이"]}]))
    s(dict(type="checklist", chapter=4, label="11월 12일 기준 · 투자 권유가 아닙니다", title="다음에 확인할 약속",
           rows=[{"label": "연말 가동 전력 1.85GW 이상", "state": "warn"},
                 {"label": "연말 연간 환산 매출 200억~210억 달러", "state": "warn"},
                 {"label": "투자등급 담보 대출 — 금리 7~7.5% 예상, 수주 안에", "state": "warn"}],
           beats=[{"say": "다음에 확인할 약속은 세 가지입니다. 연말까지 가동 전력 1.85기가와트, 연간 환산 매출 200억 달러 이상,", "upto": 2},
                  {"say": "그리고 몇 주 안에 낸다는 투자등급 담보 대출의 금리입니다. 약속대로 7%대라면, 빚 걱정에 대한 오늘의 답이 맞았다는 뜻이겠죠.", "upto": 3}]))
    s(dict(type="outro", chapter=4, title="어제 시장, 오늘 아침", sub="11월 12일 기준 · 출처는 설명란에", clip={"src": "dc", "start": 0},
           beats=B("오늘은 여기까지입니다. 앞으로 다른 기업들의 어닝콜도 이렇게 자세히 들여다보겠습니다. 출처는 설명란에 남겨 두겠습니다.")))
    # 순서: 매출(숫자) → 약속(체크리스트) → 마진(막대) — 같은 스타일 3장면 연속을 피하려고
    S[4], S[5] = S[5], S[4]
    EXTRA = {   # 장면별 눈요기 (사진·지도·카메라 효과, 05 §0-3) — 위치는 글자와 겹치지 않게 (번호 = 0부터)
        3: {"layers": [{"kind": "photo", "src": "dc", "beat": 1, "side": "right", "w": 420, "top": 560, "caption": "데이터센터 예시 · CC BY 4.0"}]},
        4: {"fx": ["dolly"]},
        7: {"fx": ["dolly"]},
        9: {"fx": ["tilt"]},
        10: {"fx": ["dolly"]},
        11: {"fx": ["scan"]},
        12: {"fx": ["tilt"]},
        13: {"fx": ["dolly"]},
        14: {"layers": [{"kind": "photo", "src": "dc", "beat": 0, "side": "right", "w": 420, "top": 600, "caption": "데이터센터 예시 · CC BY 4.0"}]},
        16: {"fx": ["dolly"]},
        17: {"fx": ["tilt"]},
    }
    for k, v in EXTRA.items():
        for kk, vv in v.items():
            S[k].setdefault(kk, vv) if kk == "fx" else S[k].setdefault(kk, vv)
    for i, x in enumerate(S, 1):
        x["id"] = i
    spec = {
        "title": "코어위브 경영진은 무엇을 말했나 — 어닝콜 핵심 다섯 가지와 그 의미",
        "brand": "market",
        "core_message": "코어위브 어닝콜은 실적보다 '빚·공급 과잉·GPU 노후화'라는 시장의 걱정 세 가지에 숫자로 답해 신뢰를 얻었고, 그 답은 AI 인프라 전체(오라클·메모리·한국 반도체)로 이어졌다. 다만 커지는 손실과 이자가 남은 숙제다.",
        "question": "코어위브 경영진은 어닝콜에서 무엇을 말했고, 그게 왜 시장을 움직였을까?",
        "logic": ["실적: 매출 약 37억 달러 +168%, 조정 영업이익률 1%→5%→10%, 연간 전망 상향",
                  "걱정 ① 빚 → 무담보 채권 안 씀, 선지급금 약 90억 달러(3개월), 계약 맞춤 담보 대출, 평균 금리 7.9%",
                  "걱정 ② 공급 과잉 → 검증된 수요가 2027년까지 용량의 10배",
                  "걱정 ③ GPU 노후화 → 옛 GPU 이용료 +30~50%, 2027년 재계약 시 연 약 40억 달러",
                  "의미(해석): 선지급 = 수요가 진짜라는 신호 → 오라클 등 / 옛 GPU 가치 → 투자 회수 기간 / 수요 10배 → 칩·메모리 → 한국 반도체",
                  "남은 숙제: 순손실 7.09억 달러, 이자 8.46억 달러(2.7배), 흑자 2028년 상반기"],
        "compare_to": [{"value": "매출 +168%", "to": "1년 전 같은 분기"}, {"value": "조정 영업이익률 10%", "to": "1분기 1%, 2분기 5%"},
                       {"value": "평균 차입 금리 7.9%", "to": "1년 전보다 2.5%p 높았음"}, {"value": "이자 비용 8.46억 달러", "to": "1년 전 3.1억 달러"}],
        "analogies": [{"a": "선지급금으로 짓기", "b": "아파트를 분양 대금을 먼저 받고 짓는 것"},
                      {"a": "옛 GPU 재계약", "b": "몇 년 탄 중고차가 새 차 때보다 비싸게 다시 팔리는 상황"}],
        "past_cases": [{"case": "2026년 11월 5일 반도체 지수 하루 -12.2% (AI 투자 걱정이 컸던 날)", "lesson": "같은 걱정에 회사가 숫자로 답하면 분위기가 일주일 만에 바뀔 수 있다"}],
        "glossary": [{"term": "어닝콜", "plain": "실적 발표 뒤 경영진이 투자자·애널리스트와 통화하며 질문에 답하는 자리"},
                     {"term": "조정 영업이익률", "plain": "일회성·주식 보상 등을 뺀 영업이익이 매출에서 차지하는 비율"},
                     {"term": "선지급금", "plain": "고객이 서비스를 받기 전에 미리 내는 돈"},
                     {"term": "무담보 채권", "plain": "담보 없이 회사 신용만으로 빌리는 돈 — 금리가 높아질 수 있다"},
                     {"term": "투자등급", "plain": "신용평가사가 '갚을 능력이 충분하다'고 보는 등급"}],
        "scenes": S,
        "map": {"nodes": {"prepay": {"label": "고객 선지급금 약 90억 달러", "icon": "wallet", "x": 290, "y": 330},
                          "real": {"label": "수요가 말뿐이 아니라는 신호", "icon": "circle-check", "x": 900, "y": 330},
                          "orcl": {"label": "같은 빚 걱정 → 오라클 +8.8%", "icon": "trending-up", "x": 1560, "y": 330},
                          "oldgpu": {"label": "옛 GPU 이용료 +30~50%", "icon": "cpu", "x": 290, "y": 560},
                          "payback": {"label": "AI 투자 회수 기간이 길어질 수 있음", "icon": "hourglass", "x": 900, "y": 560},
                          "demand": {"label": "수요가 용량의 10배", "icon": "users", "x": 290, "y": 800},
                          "memory": {"label": "칩·메모리 수요 → 마이크론·한국 반도체", "icon": "microchip", "x": 900, "y": 800}},
                "edges": [["prepay", "real"], ["real", "orcl"], ["oldgpu", "payback"], ["demand", "memory"]]},
        "footage": fo,
        "package": {
            "title": "코어위브 경영진은 무엇을 말했나 | 어닝콜 핵심 다섯 가지",
            "title_options": ["코어위브 경영진은 무엇을 말했나 | 어닝콜 핵심 다섯 가지",
                              "\"빚은 안 쓴다, 수요는 10배\" — 코어위브 CEO가 한 말",
                              "실적보다 답이 움직였다: 코어위브 어닝콜 해부"],
            "title_why": ["훅(CEO가 먼저 꺼낸 말)에서 — 답은 숨김", "경영진 원문 두 마디", "핵심 한 문장"],
            "thumbnails": [
                {"id": "A", "name": "데이터센터 + 질문", "layout": "photo", "photo_side": "full", "image": {"file": "04_assets/footage/raw/dc.jpg", "focus": [0.5, 0.5]},
                 "top": "코어위브 3분기 어닝콜", "lines": ["경영진이 한 말", "다섯 가지"], "hl": ["다섯 가지"], "sub": "빚 · 수요 · 가격 · 절제 · 고객", "size": 120, "text_y": 330, "marks": [],
                 "why": ["훅 그대로"]},
                {"id": "B", "name": "숫자 대비", "layout": "versus", "left": {"value": "1%", "label": "1분기 조정 영업이익률"},
                 "right": {"value": "10%", "label": "3분기"}, "headline": "세 분기 만에 열 배", "hl": [], "marks": [], "why": ["숫자 둘"]},
                {"id": "C", "name": "걱정 셋", "layout": "photo", "photo_side": "full", "image": {"file": "04_assets/footage/raw/nvidia.jpg", "focus": [0.5, 0.5]},
                 "top": "AI 인프라의 걱정", "lines": ["빚·공급 과잉·", "낡은 GPU"], "hl": ["빚"], "sub": "코어위브의 답", "size": 120, "text_y": 330, "marks": [],
                 "why": ["목록형"]}]},
    }
    (P / "02_script" / "hybrid.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
    print(P, len(S), "장면")


if __name__ == "__main__":
    main()
