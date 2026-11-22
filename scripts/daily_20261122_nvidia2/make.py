"""엔비디아 2부 — 순환금융, 누가 맞나: 방어와 비판, 근거끼리 맞대기 (2026-11-22).
2026-11-22 사용자: "2부로 만들어도 되니까 … 여러 인사이트로 확장해주세요. 엔비디아도 마찬가지입니다." · "지금은 약간 개념설명이고 이 개념을 바탕으로 진짜 인사이트와 각각의 근거까지"
형식: 1부(개념) 위에 — 사람마다 원본 발언 → 논리 사슬 → 받치는 근거 → 어긋나는 근거 → 이해관계 → 판정.
실행: python scripts/daily_20261122_nvidia2/make.py   (저장소 루트에서)
"""
import json
import shutil
from pathlib import Path

P1 = Path("projects/20261122-market-deep-nvidia-circular")
P = Path("projects/20261122-market-deep-nvidia-insight")
S = []


def s(d):
    d["id"] = len(S) + 1
    S.append(d)


def M(t, id, value, label, x, y, w, h, fs):
    return {"t": t, "do": "count", "id": id, "value": value, "label": label, "x": x, "y": y, "w": w, "h": h, "fs": fs}


NP = "newsprint"
OP = "의견이며 사실이 아닙니다"

# ── 0. 여는 장면 ──
# 여는 장면: 원본 발언 (2026-11-23 사용자)
s(dict(type="bite", insight=True, label=OP + " · 엔비디아 CEO (당시, 파는 쪽)", who="젠슨 황", role="엔비디아 CEO · 야후 파이낸스 (10월)",
       clip={"src": "huang_life", "lang": "en", "cuts": [
           {"find": "And so people are discovering that what people thought used to be a four -year lifecycle really is probably eight to maybe more.",
            "ko": "그래서 사람들은 4년이라고 생각했던 수명이, 실제로는 8년이거나 그 이상이라는 걸 알아 가고 있습니다."}]},
       beats=[{"say": "엔비디아의 젠슨 황이 지난 10월, AI 빚을 둘러싼 걱정에 이렇게 답했습니다."}]))
s(dict(type="bignum", insight=True, label=OP + " · 젠슨 황(야후 파이낸스 10월) vs 짐 채노스(공매도 투자자)",
       small="GPU 가 돈을 버는 기간 — 젠슨 황 vs 짐 채노스", value="8년 vs 3년",
       beats=[{"say": "공매도 투자자 짐 채노스는 반대로 3년이라고 봅니다. 이 차이가 이 숫자의 운명을 가릅니다."}]))
s(dict(type="bignum", label="엔비디아 3분기(회계 2027) CFO 코멘터리 — 보증 최대 노출 1,180억 달러, 지금까지 실제로 낸 돈 없음 (10월 25일 기준)",
       small="엔비디아가 고객 대신 내겠다고 약속한 돈 (최대) · 지금까지 실제로 낸 돈", value="1,180억 vs 0",
       beats=[{"say": "엔비디아가 고객이 못 내면 대신 내겠다고 약속한 돈은 최대 1,180억 달러이고, 지금까지 실제로 낸 돈은 없습니다. 이 약속이 위험한지 아닌지를 두고, 업계와 월가의 말이 정반대로 갈립니다.",
               "motion": [M("1,180억", "g", "보증 최대 1,180억 달러 · 실제 지급 0", "CFO 코멘터리 (10.25 기준)", 1560, 880, 520, 110, 30)]}]))
s(dict(type="checklist", label="1부(엔비디아 순환금융)에서 본 개념",
       title="1부에서 본 세 가지 도구", x=150, text_w=1000, skin=NP,
       rows=[{"label": "① 파는 쪽이 사는 쪽에 돈을 대면, 매출은 진짜여도 위험이 겹친다", "state": "ok", "t": "첫째"},
             {"label": "② 위험은 오늘이 아니라 몇 년 뒤의 약속에 쌓인다 (보증·임대·지분)", "state": "ok", "t": "둘째"},
             {"label": "③ 고리가 약해지는 곳: 칩값 받는 속도 · 투자한 회사의 값 · 담보 가치", "state": "ok", "t": "셋째"}],
       beats=[{"say": "1부에서 순환금융의 원리를 봤습니다. 첫째, 파는 쪽이 사는 쪽에 돈을 대면 매출은 진짜여도 위험이 겹칩니다. 둘째, 그 위험은 오늘이 아니라 몇 년 뒤의 약속에 쌓입니다. 셋째, 고리는 칩값을 받는 속도와 투자한 회사의 값, 그리고 담보의 가치에서 먼저 약해집니다.", "upto": 3},
              {"say": "이번 2부는 이 도구로 사람들의 말을 뜯어보겠습니다. 미리 말씀드리면, 방어하는 쪽과 비판하는 쪽은 결국 한 가지 숫자에서 갈립니다. GPU가 몇 년 동안 돈을 버느냐입니다."}]))

# ── 1. 젠슨 황 ──
s(dict(type="chapter", num="1", title="젠슨 황 — 'GPU 는 8년을 번다, 그래서 담보가 된다'", icon="cpu", look="board",
       beats=[{"say": "먼저 가장 강한 방어, 지난달 젠슨 황의 말입니다. 그는 이 인터뷰 몇 주 뒤 CEO에서 물러났지만, 이 논리는 지금도 엔비디아 방어의 중심입니다."}]))
s(dict(type="bite", insight=True, label=OP + " · 같은 인터뷰", who="젠슨 황", role="엔비디아 CEO · 야후 파이낸스 (10월)", show_lower=False,
       clip={"src": "huang_collateral", "lang": "en", "cuts": [
           {"find": "Now when that happens, you might be able to underwrite a loan against the asset itself. Today, most computers don't have value, don't have very little residual value, but people are now recognizing NVIDIA's compute has a great deal of residual value.",
            "ko": "그렇게 되면 그 자산 자체를 담보로 대출을 내줄 수 있습니다. 대부분의 컴퓨터는 남는 가치가 거의 없지만, 사람들은 이제 엔비디아의 컴퓨팅에 남는 가치가 크다는 걸 알아보고 있습니다."}]},
       beats=[{"say": "영상 처음에 들은 '8년' 이야기에서, 그는 이렇게 이었습니다."}]))
s(dict(type="motionboard", label="젠슨 황 야후 파이낸스(2026.10.21) 논리 · 받침: Silicon Data H100 지수 2.88달러(10.24, 2025.12 2.00달러) · 코어위브 3분기 콜(구세대 가격 전 분기 대비 +30~50%) · " + OP,
       title="젠슨 황의 논리 — 오래 벌면, 담보가 되고, 빚이 안전하다",
       els={"a": {"kind": "card", "x": 330, "y": 370, "icon": "cpu", "label": "① 소프트웨어로 계속 새로워짐", "w": 320},
            "b": {"kind": "card", "x": 960, "y": 370, "icon": "hourglass", "label": "② 8년 넘게 돈을 번다", "w": 300},
            "c": {"kind": "card", "x": 1590, "y": 370, "icon": "landmark", "label": "③ 담보 가치 → 빚이 안전", "w": 320},
            "a1": {"kind": "arrow", "from": "a", "to": "b"}, "a2": {"kind": "arrow", "from": "b", "to": "c"},
            "e1": {"kind": "text", "x": 960, "y": 690, "text": "받침: H100 빌리는 값 시간당 2.00 → 2.88달러 (+44%)", "size": 38},
            "e2": {"kind": "text", "x": 960, "y": 800, "text": "받침: 코어위브 구세대 GPU 가격 전 분기보다 30~50% 상승", "size": 38}},
       beats=[{"say": "그의 논리는 세 고리입니다. 엔비디아 GPU는 소프트웨어로 계속 새로워져, 4년이 아니라 8년 넘게 돈을 벌고, 그래서 남는 가치가 커 담보가 되며, 담보가 좋으면 그 빚은 안전하다는 겁니다.",
               "do": ["a", "a1", "b", "a2", "c"], "at": {"a": "소프트웨어로", "b": "8년", "c": "담보가"}},
              {"say": "받치는 숫자도 있습니다. GPU 빌리는 값을 모은 지수에서 H100의 시간당 값은 작년 12월 2달러에서 올해 10월 2.88달러로 44% 올랐습니다. 코어위브도 3분기에 구세대 GPU의 가격이 전 분기보다 30에서 50% 올랐다고 밝혔습니다. 오래된 칩도 여전히 비싸게 빌려 간다는 뜻입니다.",
               "do": ["e1", "e2"], "at": {"e1": "GPU 빌리는", "e2": "코어위브도"}}]))

# ── 2. 크레스 ──
s(dict(type="chapter", num="2", title="콜레트 크레스 — '네오클라우드를 떠받치는 게 아니다'", icon="users", look="board",
       beats=[{"say": "두 번째, 젠슨 황의 자리를 이어받은 콜레트 크레스 임시 CEO입니다."}]))
s(dict(type="bite", lower_top=600, insight=True, label=OP + " · 엔비디아 임시 CEO (전 CFO)", who="콜레트 크레스", role="엔비디아 임시 CEO · CNBC (11월 18일)",
       clip={"src": "kress", "lang": "en", "cuts": [
           {"find": "Interesting statement, but no, it is not true. If we want to think about where we are with our hyperscalers, they are the ones that are right now feverishly looking for more focus in terms of the compute that we have available.",
            "ko": "흥미로운 말이지만, 아닙니다. 사실이 아닙니다. 지금 우리가 가진 연산 능력을 가장 애타게 찾는 건 바로 대형 클라우드 회사들입니다."}]},
       beats=[{"say": "실적 다음 날인 지난 18일, CNBC가 물었습니다. 엔비디아가 대형 클라우드 고객을 잃어 가니, 신용도가 낮은 네오클라우드를 떠받치는 것 아니냐고요. 그녀의 답입니다."}]))
s(dict(type="checklist", insight=True, label="받침: 1부(매출 절반 빅테크 · 3분기 매출 1,158억) / 어긋남: CFO 코멘터리(매출채권 810억·회수 64일, 지분 손상 18억) · 국내 보도(보증 조건 명확화 뒤 네오클라우드 20%+ 하락) · " + OP,
       title="크레스의 말 — 받치는 근거와 어긋나는 근거", x=120, text_w=1080, skin=NP,
       rows=[{"label": "받침: 매출의 절반은 여전히 빅테크, 3분기 매출 1,158억 달러", "state": "ok", "t": "받치는"},
             {"label": "어긋남: 받지 못한 칩값 810억, 회수까지 64일로 늘어남", "state": "warn", "t": "어긋나는"},
             {"label": "어긋남: 투자한 회사 손상 18억 달러 (한 분기)", "state": "warn", "t": "손상"},
             {"label": "어긋남: 보증 조건이 알려진 뒤 네오클라우드 주가 20%+ 하락 (보도)", "state": "warn", "t": "네오클라우드"}],
       beats=[{"say": "받치는 근거는 분명합니다. 1부에서 본 것처럼 매출의 절반은 여전히 빅테크에서 나오고, 3분기 매출은 1,158억 달러였습니다.", "upto": 1},
              {"say": "하지만 1부의 세 번째 도구로 보면 어긋나는 숫자가 있습니다. 받지 못한 칩값은 810억 달러로 늘었고 회수까지 64일로 길어졌습니다. 투자한 회사의 손상은 한 분기에 18억 달러였고, 보증 조건이 알려진 뒤 네오클라우드 주가는 20% 넘게 빠졌다는 보도가 나왔습니다. 고객을 잃지 않았다는 말과, 고객 쪽의 돈 사정이 빡빡해진다는 숫자는 함께 맞을 수 있습니다.", "upto": 4}]))

# ── 3. 그라이펠드 ──
s(dict(type="chapter", num="3", title="그라이펠드 — '고리를 넓힌 건 좋다, 하지만 빚이 어디 있는지 모른다'", icon="scale", look="board",
       beats=[{"say": "세 번째는 가운데에 선 목소리입니다. 나스닥 CEO를 지낸 밥 그라이펠드입니다."}]))
s(dict(type="bite", insight=True, label=OP + " · 전 나스닥 CEO", who="밥 그라이펠드", role="전 나스닥 CEO · CNBC (8월)",
       clip={"src": "greifeld_good", "lang": "en", "cuts": [
           {"find": "They have widened the circle where there's more people involved with this financing. And what I like about it is the third parties involved probably will do a market rate setting in terms of what this asset should price at.",
            "ko": "고리를 넓혀 이 금융에 더 많은 사람이 들어오게 했습니다. 좋은 점은, 들어온 제3자들이 이 자산의 값을 시장 금리로 매기게 된다는 겁니다."}]},
       beats=[{"say": "지난 8월 엔비디아가 월가 회사들과 5,000억 달러 규모의 금융 협력을 발표했을 때, 그는 CNBC에서 좋은 점부터 말했습니다."}]))
s(dict(type="bite", insight=True, label=OP + " · 같은 인터뷰, '싫은 점은?'", who="밥 그라이펠드", role="전 나스닥 CEO · CNBC (8월)", show_lower=False,
       clip={"src": "greifeld_bad", "lang": "en", "cuts": [
           {"find": "So one, there's more people in the circle and there's points of leverage in every part of the circle. So we don't really know how much leverage is in the system as we go through that.",
            "ko": "고리에 사람이 많아졌고, 고리의 모든 곳에 빚이 있습니다. 그래서 이 체계에 빚이 얼마나 쌓여 있는지 우리는 잘 모릅니다."}]},
       beats=[{"say": "그리고 싫은 점을 이렇게 말했습니다."}]))
s(dict(type="motionboard", label="원리 설명 · 그라이펠드 CNBC(2026.8.12) · 월스트리트저널 보도(11.19 무렵, 5,000억 달러 약속 집행 0, 은행이 엔비디아에 25% 넘는 보증 요구)",
       title="시장이 값을 매기기 시작했다 — 그리고 그 값",
       els={"a": {"kind": "card", "x": 400, "y": 400, "icon": "banknote", "label": "월가 5,000억 달러 약속 (8월)", "w": 380},
            "b": {"kind": "card", "x": 1500, "y": 400, "icon": "circle-alert", "label": "집행 0 · 보증 25% 넘게 요구", "w": 380},
            "a1": {"kind": "arrow", "from": "a", "to": "b", "color": "red"},
            "t": {"kind": "text", "x": 700, "y": 760, "text": "시장이 매긴 값: '엔비디아가 더 책임지면'", "size": 38}},
       beats=[{"say": "그의 좋은 점이 맞았다면, 시장은 이 자산에 값을 매기기 시작했습니다. 그런데 그 값이 이렇습니다. 월스트리트저널 보도에 따르면, 8월에 약속된 5,000억 달러는 아직 한 푼도 집행되지 않았고, 은행들은 엔비디아에 25%보다 더 많이 보증해 달라고 요구하고 있습니다.",
               "do": ["a", "a1", "b"], "at": {"a": "8월에", "b": "집행되지"},
               "motion": [M("25%", "g25", "은행 요구: 엔비디아 보증 25% 넘게", "월스트리트저널 보도", 1500, 860, 480, 110, 30)]},
              {"say": "젠슨 황의 말처럼 GPU가 그렇게 좋은 담보라면, 은행이 엔비디아의 보증을 더 요구할 이유가 적습니다. 시장이 매긴 값은, 아직은 엔비디아가 더 책임지면 빌려주겠다는 쪽입니다.",
               "do": ["t"], "at": {"t": "시장이 매긴"}}]))

# ── 4. 비판 ──
s(dict(type="chapter", num="4", title="비판하는 쪽 — 채노스와 버리", icon="circle-alert", look="board",
       beats=[{"say": "이제 비판하는 쪽입니다. 두 사람 모두 같은 곳을 찌릅니다. 젠슨 황의 첫 고리, GPU의 수명입니다."}]))
s(dict(type="quote", insight=True, label="짐 채노스 (공매도 투자자, 엔론 붕괴를 먼저 짚은 인물) · 모틀리풀·야후 파이낸스 보도(2025) · " + OP,
       who="짐 채노스", role="공매도 투자자 · 2025년 인터뷰 (보도)",
       quote="칩이 3년 간다면, 쓴 돈의 3분의 1씩 비용으로 잡아야 한다.", keyword="3년",
       orig="If the chips last for three years, you have to depreciate a third of what you spend.",
       beats=[{"say": "엔론의 붕괴를 먼저 짚었던 공매도 투자자 짐 채노스는, 새 칩이 1년 반마다 나오는데 GPU를 6년에 걸쳐 비용으로 나누는 건 너무 너그럽다고 봅니다. 칩이 3년 간다면 쓴 돈의 3분의 1씩을 매년 비용으로 잡아야 한다는 겁니다."},
              {"say": "그는 GPU를 담보로 한 빚에 대해서도, 수익이 나아지지 않으면 부도가 날 거라고 했습니다. 그리고 올해 9월, 젠슨 황이 엔비디아의 연산은 빌려주기 좋다고 하자, 그렇다면 왜 직접 빌려주지 않느냐고 되물었습니다."}]))
s(dict(type="quote", insight=True, label="마이클 버리 ('빅쇼트' 투자자) · 본인 글을 다룬 보도(2025.11~) — 원문 미대조 · " + OP,
       who="마이클 버리", role="'빅쇼트' 투자자 · 본인 글 (보도)",
       quote="수명을 늘려 잡으면, 비용이 줄고 이익이 커 보인다.", keyword="이익",
       orig="(요약) Hyperscalers are extending useful lives to understate depreciation and inflate earnings.",
       beats=[{"say": "영화 빅쇼트의 실제 인물 마이클 버리도 같은 곳을 봅니다. 그는 대형 클라우드 회사들이 서버와 GPU의 수명을 늘려 잡아 해마다의 비용을 줄이고, 그래서 이익이 실제보다 커 보인다고 주장해 왔습니다. 그의 글을 다룬 보도로 전해진 주장이고, 회사들은 4년에서 6년의 수명이 합당하다고 반박합니다."}]))
s(dict(type="bars", label="원리 설명 · 계산: 같은 GPU 100억 달러어치, 해마다 같은 임대 매출 30억 달러 가정 — 정액 상각",
       title="GPU 100억 달러어치 — 해마다 잡는 비용 (억 달러, 예시) · 3년 채노스 · 6년 회사들 · 8년 젠슨 황", unit="", emph=0, skin="dark-doc",
       items=[{"label": "3년", "value": 33.3, "text": "33.3", "t": "3년으로"},
              {"label": "6년", "value": 16.7, "text": "16.7", "t": "6년으로"},
              {"label": "8년", "value": 12.5, "text": "12.5", "t": "8년이면"}],
       beats=[{"say": "숫자로 보면 차이가 얼마나 큰지 보입니다. 100억 달러어치 GPU가 해마다 30억 달러의 임대 매출을 낸다고 가정해 보겠습니다. 3년으로 나누면 해마다 비용이 33.3억 달러라 3.3억 달러 적자입니다.",
               "motion": [M("3.3억", "d3", "매출 30억 − 비용 33.3억 = 적자 3.3억", "3년으로 나누면 (예시)", 1500, 300, 560, 110, 28)]},
              {"say": "6년으로 나누면 비용이 16.7억 달러라 13.3억 달러 흑자, 8년이면 12.5억 달러라 17.5억 달러 흑자입니다. 같은 칩, 같은 매출인데 수명을 몇 년으로 보느냐에 따라 적자가 흑자가 됩니다. 담보의 값도, 보증의 위험도 모두 이 숫자에 기대고 있습니다.",
               "motion": [M("13.3억", "d6", "6년: 흑자 13.3억 · 8년: 흑자 17.5억", "같은 매출 30억 (예시)", 1500, 440, 560, 110, 28)]}]))

# ── 5. 국내 시각 ──
s(dict(type="quote", insight=True, label="KB증권 (2026.9, 아시아경제 보도) · " + OP,
       who="KB증권", role="국내 증권사 · 9월 리포트 (보도)",
       quote="매출채권이 는 건 돈 받는 시점이 늦어진 것일 뿐이다.", keyword="시점",
       orig="(요약) 2026~28 누적 잉여현금 약 9,600억 달러, 약정 4,220억 달러보다 큼",
       beats=[{"say": "국내 증권가의 시각도 있습니다. KB증권은 지난 9월, 매출채권이 는 건 돈을 받는 시점이 늦어진 것일 뿐이고, 엔비디아가 2026년부터 28년까지 벌 잉여현금이 약 9,600억 달러로, 약정 4,220억 달러보다 크다고 봤습니다. 엔비디아의 위험보다, 그 고리에 걸린 고객들의 위험이 더 크다는 시각과도 이어집니다.",
               "motion": [M("9,600억", "kb", "잉여현금 9,600억 · 약정 4,220억보다 큼", "KB증권 (2026~28, 달러)", 1560, 880, 520, 110, 28)]}]))

# ── 6. 어디서 갈리나 ──
s(dict(type="chapter", num="5", title="두 쪽은 어디서 갈리나", icon="scale", look="board",
       beats=[{"say": "이제 양쪽을 1부의 도구 위에 올려 보겠습니다."}]))
s(dict(type="map_causal", look="board", label="가설 · 근거: 위 인터뷰·보도, 1부 원리",
       map={"nodes": {"life": {"label": "GPU 가 몇 년 돈을 버나 (3년? 8년?)", "icon": "hourglass", "x": 960, "y": 230},
                      "col": {"label": "담보 가치", "icon": "landmark", "x": 380, "y": 560},
                      "debt": {"label": "네오클라우드의 빚", "icon": "cloud", "x": 960, "y": 700},
                      "gua": {"label": "엔비디아의 보증·지분", "icon": "cpu", "x": 1540, "y": 560}},
            "edges": [["life", "col"], ["col", "debt"], ["debt", "gua"]]},
       beats=[{"say": "여기서부터는 가설입니다. 방어하는 쪽과 비판하는 쪽은 결국 한 숫자에서 갈립니다. GPU가 몇 년 동안 돈을 버느냐입니다.", "reveal": ["life"], "active": "life"},
              {"say": "8년이면 담보가 튼튼하고, 네오클라우드의 빚은 갚히고, 엔비디아의 보증은 한 푼도 나가지 않습니다. 3년이면 담보 가치가 먼저 무너지고, 빚이 흔들리고, 그 끝에 엔비디아의 보증과 지분이 있습니다. 1부에서 본 고리가 실제로 끊어지는 순서입니다.",
               "reveal": ["col", "debt", "gua"], "draw": [["life", "col"], ["col", "debt"], ["debt", "gua"]], "active": "gua"},
              {"say": "그리고 지금 GPU 임대료가 오르고 있다는 사실은 양쪽 다 설명할 수 있습니다. 칩이 오래 쓸모 있다는 증거일 수도 있고, 금융이 빡빡해져 남는 칩이 잠긴 결과일 수도 있습니다. 그래서 임대료 하나로는 판가름이 나지 않습니다.", "active": "life"}]))

# ── 7. 판가름 ──
s(dict(type="checklist", label="가설 · 판가름 신호 — Silicon Data GPU 임대 지수 · 월가 칩 금융 집행 · 엔비디아 다음 실적(2027년 2월 예정)의 보증 지급·매출채권 · 네오클라우드 대출 조건",
       title="무엇이 나오면 누가 맞나", x=120, text_w=1080, skin=NP,
       rows=[{"label": "구세대 GPU(H100) 임대료가 버티나 → 젠슨 황 쪽", "state": "ok", "t": "첫째"},
             {"label": "월가 5,000억 칩 금융이 엔비디아 보증 없이 집행되나 → 젠슨 황 쪽", "state": "ok", "t": "둘째"},
             {"label": "엔비디아 보증에서 실제 지급이 나오나 (지금 0) → 비판 쪽", "state": "warn", "t": "셋째"},
             {"label": "매출채권 회수 기간이 64일보다 길어지나 → 비판 쪽", "state": "warn", "t": "넷째"}],
       beats=[{"say": "판가름 신호는 넷입니다. 첫째, 구세대 GPU인 H100의 임대료가 새 칩이 나와도 버티는지. 버티면 젠슨 황의 8년이 맞아 가는 겁니다. 둘째, 월가의 칩 금융이 엔비디아의 보증 없이 집행되는지입니다.", "upto": 2},
              {"say": "셋째, 엔비디아의 보증에서 실제로 돈이 나가는지. 지금까지는 0입니다. 넷째, 칩값을 받는 데 걸리는 날이 지금의 64일보다 길어지는지입니다. 셋째와 넷째가 움직이면 비판하는 쪽이 맞아 가는 겁니다. 이 신호들도 매일 지켜보겠습니다.", "upto": 4}]))
s(dict(type="kinetic", beats=[{"say": "순환금융이 안전한지는 엔비디아의 말이 아니라, GPU가 실제로 몇 년을 버느냐가 정합니다.", "hit": ["몇 년"]}]))
s(dict(type="outro", title="22일까지의 자료", sub="출처는 설명란에", clip={"src": "dc", "start": 0},
       beats=[{"say": "딱 하나만 기억한다면 이것입니다. 방어하는 쪽은 GPU가 8년을 번다고 하고, 비판하는 쪽은 3년이라고 합니다. 그 차이가 담보와 빚과 보증의 위험을 모두 정합니다. 임대료와 보증 지급, 칩값을 받는 속도를 보면, 어느 쪽이 맞아 가는지 스스로 읽을 수 있습니다."}]))

_ch = 0
for _sc in S:
    if _sc["type"] == "chapter":
        _ch = int(_sc["num"])
    _sc["chapter"] = _ch

P.mkdir(parents=True, exist_ok=True)
for sub in ("04_assets/footage", "01_research"):
    if (P1 / sub).exists() and not (P / sub).exists():
        shutil.copytree(P1 / sub, P / sub)
src = json.loads((P1 / "02_script" / "hybrid.json").read_text(encoding="utf-8"))
footage = dict(src["footage"])
footage.update({
    "huang_life": {"file": "huang_yahoo_20261021_life.mp4", "url": "https://www.youtube.com/watch?v=sH5qyeHSdVs", "start": "6:42.0", "end": "6:49.0",
                   "who": "젠슨 황", "rights": "broadcast", "credit": "Yahoo Finance 공식 채널 (YouTube) · 2026.10.21"},
    "huang_collateral": {"file": "huang_yahoo_20261021_collateral.mp4", "url": "https://www.youtube.com/watch?v=sH5qyeHSdVs", "start": "7:04.8", "end": "7:23.0",
                         "who": "젠슨 황", "rights": "broadcast", "credit": "Yahoo Finance 공식 채널 (YouTube) · 2026.10.21"},
    "kress": {"file": "kress_cnbc_20261118.mp4", "url": "https://www.youtube.com/watch?v=Uu-v3YJSgNY", "start": "0:35.2", "end": "0:50.0",
              "who": "콜레트 크레스", "rights": "broadcast", "credit": "CNBC Television 공식 채널 (YouTube) · 2026.11.18"},
    "greifeld_good": {"file": "greifeld_cnbc_20260812_good.mp4", "url": "https://www.youtube.com/watch?v=VVvbvEr4HR0", "start": "0:43.0", "end": "0:57.0",
                      "who": "밥 그라이펠드", "rights": "broadcast", "credit": "CNBC Television 공식 채널 (YouTube) · 2026.8.12"},
    "greifeld_bad": {"file": "greifeld_cnbc_20260812_bad.mp4", "url": "https://www.youtube.com/watch?v=VVvbvEr4HR0", "start": "1:07.2", "end": "1:17.2",
                     "who": "밥 그라이펠드", "rights": "broadcast", "credit": "CNBC Television 공식 채널 (YouTube) · 2026.8.12"},
})
raw = "04_assets/footage/raw/"
ART = "04_assets/thumb_art/"
spec = {
    "title": "엔비디아 순환금융, 누가 맞나 — 방어와 비판, 근거끼리 맞대기 (2부)",
    "brand": "market", "zoom": "off",
    "core_message": "엔비디아 순환금융을 두고 젠슨 황·크레스는 'GPU 는 8년을 벌어 담보가 되고 고객도 그대로'라 하고, 채노스·버리는 '수명을 늘려 잡아 비용을 줄였을 뿐'이라 한다. 그라이펠드는 고리를 넓힌 건 좋지만 빚이 어디 있는지 모른다고 했고, 시장은 아직 엔비디아의 보증을 더 요구한다. 두 쪽은 'GPU 가 몇 년 버느냐'에서 갈리고, 그 숫자가 담보·빚·보증의 위험을 정한다. 판가름은 구세대 GPU 임대료·월가 금융 집행·보증 실제 지급·매출채권 회수 기간.",
    "question": "엔비디아의 순환금융은 안전한가 — 누가, 무엇을 근거로, 어디서 갈리나?",
    "logic": ["여는 장면: 보증 1,180억 vs 지급 0 → 1부의 세 도구 → 갈리는 숫자 예고(GPU 수명)",
              "1) 젠슨 황: 원본(4년이 아니라 8년+) → 원본(담보·잔존가치) → 논리 세 고리 → 받침(H100 임대 +44%, 코어위브 구세대 +30~50%)",
              "2) 크레스: 원본(네오클라우드 떠받치기 아니다) → 받침(빅테크 절반) / 어긋남(매출채권 810억·64일, 손상 18억, 네오클라우드 -20%)",
              "3) 그라이펠드: 원본(좋은 점: 시장 값) → 원본(싫은 점: 빚이 어디 있는지 모름) → 시장이 매긴 값(5,000억 집행 0, 보증 25%+ 요구)",
              "4) 비판: 채노스(3년이면 1/3씩, 부도, 왜 직접 안 빌려주나) · 버리(수명 늘려 이익 부풀림) → 계산(3·6·8년)",
              "5) KB증권(잉여현금 9,600억 > 약정 4,220억)",
              "6) 갈리는 곳: GPU 수명 → 담보 → 빚 → 보증 (임대료는 양쪽 다 설명) → 판가름 신호 넷"],
    "compare_to": [{"value": "보증 최대 1,180억 달러", "to": "실제 지급 0"},
                   {"value": "H100 시간당 2.88달러 (10.24)", "to": "2025년 12월 2.00달러"},
                   {"value": "수명 3년 → 해마다 비용 33.3억", "to": "8년 → 12.5억 (100억어치 예시)"},
                   {"value": "KB 누적 잉여현금 9,600억", "to": "약정 4,220억"}],
    "analogies": [{"a": "중고차 대출", "b": "차가 몇 년 굴러가느냐로 담보 값과 빌려줄 돈이 정해진다 — GPU 도 같다"},
                  {"a": "같은 매출, 다른 이익", "b": "비용을 몇 년에 나누느냐에 따라 적자가 흑자가 된다"}],
    "past_cases": [{"case": "2000년 루슨트 고객 대출(1부)", "lesson": "장비 값이 빨리 떨어지자 대출과 매출을 함께 잃음"}],
    "glossary": [{"term": "감가상각", "plain": "비싼 장비 값을 쓰는 햇수에 나눠 해마다 비용으로 잡는 것"},
                 {"term": "잔존가치", "plain": "다 쓴 뒤에도 남는 값 — 담보 가치를 정함"},
                 {"term": "네오클라우드", "plain": "GPU 를 사서 빌려주는 신생 클라우드 회사 (코어위브 등)"},
                 {"term": "매출채권 회수 기간", "plain": "물건을 넘기고 돈을 받기까지 걸리는 날"}],
    "scenes": S, "footage": footage,
    "package": {
        "title": "\"GPU 는 8년 번다\" vs \"3년이면 끝\" — 엔비디아 순환금융, 누가 맞나 (2부)",
        "title_options": ["\"GPU 는 8년 번다\" vs \"3년이면 끝\" — 엔비디아 순환금융, 누가 맞나 (2부)",
                          "젠슨 황 vs 짐 채노스 — 엔비디아 1,180억 달러 보증, 근거만 따져 보면",
                          "엔비디아 순환금융의 진짜 쟁점은 'GPU 수명'이다"],
        "title_why": ["숫자 대결", "인물 대결 + 숫자", "단정 한 마디"],
        "thumb_pick": "A", "thumb_test": ["A", "B", "D"],
        "tags": ["엔비디아 순환금융", "엔비디아 순환거래", "엔비디아 거품론", "ai 거품", "젠슨황", "콜레트 크레스", "짐 채노스", "마이클 버리", "GPU 감가상각",
                 "코어위브", "코어위브 사태", "엔비디아 주가 하락 이유", "엔비디아 주가 전망", "네오클라우드", "SK하이닉스", "삼성전자"],
        "hashtags": ["엔비디아", "AI거품", "순환금융"],
        "thumbnails": [
            {"id": "A", "name": "인물 — 젠슨 황 + GPU 는 8년을 번다?", "layout": "person", "image": {"file": raw + "jensen_huang_face.jpg", "focus": [0.5, 0.4]},
             "person": {"name": "젠슨 황", "role": "엔비디아 창업자"}, "top": "엔비디아 순환금융 2부", "lines": ["GPU 는", "8년을 번다"], "hl": ["8년을"], "size": 110, "text_y": 230,
             "quote": "4년인 줄 알았던 수명이 8년 이상", "credit": "사진: Anders Eidesvik · CC BY 4.0", "why": ["당사자 얼굴 + 그의 말 (docs/59)"]},
            {"id": "B", "name": "인물 — 젠슨 황(스탠퍼드) + 칩을 담보로 빚을 낸다", "layout": "person", "image": {"file": raw + "jensen_stanford_crop.jpg", "focus": [0.5, 0.3]},
             "person": {"name": "젠슨 황", "role": "엔비디아 창업자"}, "top": "엔비디아 순환금융 2부", "lines": ["칩을 담보로", "빚을 낸다"], "hl": ["담보로"], "size": 104, "text_y": 230,
             "quote": "엔비디아 칩은 남는 가치가 크다", "credit": "사진: Anders Eidesvik · CC BY 4.0", "why": ["당사자 얼굴 + 쟁점"]},
            {"id": "C", "name": "인물 — 젠슨 황 vs 채노스 (8년 vs 3년)", "layout": "person", "image": {"file": raw + "jensen_huang_face.jpg", "focus": [0.5, 0.4]},
             "person": {"name": "젠슨 황", "role": "엔비디아 창업자"}, "top": "엔비디아 순환금융 2부", "lines": ["젠슨 황 '8년'", "채노스 '3년'"], "hl": ["3년'"], "size": 96, "text_y": 230,
             "credit": "사진: Anders Eidesvik · CC BY 4.0", "why": ["인물 + 반대 주장 숫자"]},
            {"id": "D", "name": "숫자 맞대기 — 8년 vs 3년", "layout": "versus", "headline": "GPU 는 몇 년 버나", "hl": ["몇"],
             "left": {"value": "8년", "label": "젠슨 황: 담보가 된다"}, "right": {"value": "3년", "label": "채노스: 1/3씩 비용"},
             "why": ["두 시각을 숫자로"]},
            {"id": "E", "name": "실사 — 기울어지는 GPU·금괴 탑 + 진짜 쟁점은 GPU 수명", "layout": "trend", "image": {"file": ART + "r3_tower.png", "focus": [0.5, 0.5]},
             "credit": "그림: GPT 이미지 생성", "top": "엔비디아 순환금융 2부", "lines": ["진짜 쟁점은", "GPU 수명"], "hl": ["수명"], "accent": "cyan", "sticker": "보증 1,180억, 지급 0",
             "why": ["구조·단정"]}]},
}
(P / "04_assets" / "thumb_art").mkdir(parents=True, exist_ok=True)
for f in ("r3_tower.png", "r1_vault.png"):
    if (P1 / ART / f).exists() and not (P / ART / f).exists():
        shutil.copy2(P1 / ART / f, P / ART / f)
(P / "02_script").mkdir(parents=True, exist_ok=True)
(P / "02_script" / "hybrid.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
print(P, len(S), "장면", sum(len(x["beats"]) for x in S), "박자", sum(len(b["say"]) for x in S for b in x["beats"]), "자")
