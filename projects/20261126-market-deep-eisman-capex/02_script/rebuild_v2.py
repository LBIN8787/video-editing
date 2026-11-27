"""아이스먼 편 2판 — 매뉴얼 v146·v147(09 §5-00-1) 기준으로 다시 (2026-11-27 사용자: "이 기준대로 기존 예약 업로드 영상들 다시 검수하고 제작해주세요").

바꾼 것:
- 발언 10구간(6~13초, 합 96초) → 13구간을 주장 하나 전체로. 원본 전체(Diary of a CEO · Goldman Sachs Exchanges)를 받아 받아쓰기로 다시 고름.
- #13 인용 카드(아이스먼 '파산하면 다음 날 침체') → 원본 영상. 중간선거 뒤 생각을 바꾼 이유도 그의 말로(새 발언).
- 키네틱 2장(#4·#38) 뺌. 여는 #3 의 한국 주가 맞대기(억지 고리)와 '내 하이닉스·삼성' 장 이름을 덜어 냄 — 칩·메모리를 파는 쪽 이야기는 공급사로 자연스럽게만.
- '이 채널의 계산/해석/정리' → '가설'. newsprint → dark-doc. 발언을 되풀이하던 내레이션은 줄임.
실행: python projects/20261126-market-deep-eisman-capex/02_script/rebuild_v2.py
"""
import copy
import json
import subprocess
from pathlib import Path

P = Path(__file__).resolve().parent.parent
SRC = P / "04_assets" / "footage" / "_src"
hp = P / "02_script" / "hybrid.json"
v1p = P / "02_script" / "hybrid_v1.json"
if not v1p.exists():
    v1p.write_text(hp.read_text(encoding="utf-8"), encoding="utf-8")
    (P / "02_script" / "cuts_v1.json").write_text((P / "02_script" / "cuts.json").read_text(encoding="utf-8"), encoding="utf-8")
d = json.loads(v1p.read_text(encoding="utf-8"))
cuts_v1 = json.loads((P / "02_script" / "cuts_v1.json").read_text(encoding="utf-8"))


def mmss(x):
    return f"{int(x // 60)}:{x % 60:04.1f}"


# 키: (원본, 기준 footage, [(구간 시작, 끝, [(절대 시각, 영어, 한국어), ...]), ...])
B = {
    "eisL_fail": ("eis", "eis_fail", [(1489.12, 1531.75, [
        (1489.12, "And the crazy thing is the entire market is basically an AI trade right now. And you know what else is? So is the US economy.",
         "놀라운 건, 지금 시장 전체가 사실상 AI에 건 거래라는 겁니다. 그리고 또 뭐가 그런지 아세요? 미국 경제도 그렇습니다."),
        (1500.38, "So if this thing fails — I believe in AI as a technology, but I also believed in the internet as a technology, and that didn't stop the dot-com bubble.",
         "그래서 이게 무너진다면요. 저는 AI를 기술로서 믿습니다. 하지만 인터넷도 기술로서 믿었고, 그게 닷컴 거품을 막지는 못했죠."),
        (1516.3, "We could have a situation where one of these two guys fails, everybody stops ordering all the chips, we go into a recession, eventually we work our way out, and then we grow at a better pace. That could happen. I think that's the more likely event.",
         "두 회사 중 하나가 무너지고, 모두가 칩 주문을 멈추고, 침체에 들어갔다가 결국 빠져나와 더 나은 속도로 성장하는 상황이 올 수 있습니다. 저는 그쪽이 더 가능성 높다고 봅니다."),
    ])]),
    "eisL_70": ("eis", "eis_70", [(1306.26, 1339.7, [
        (1306.26, "However, in Nvidia's 10-Q, it also says that 70% of its revenue comes from five customers. That's very concentrated.",
         "그런데 엔비디아 분기 보고서에는, 매출의 70%가 다섯 고객에게서 나온다고도 적혀 있습니다. 아주 몰려 있죠."),
        (1315.5, "Now, in one way or another, those customers are the hyperscalers — Microsoft, Amazon, Google, maybe Oracle a little bit, maybe Meta a little bit.",
         "그 고객들은 어떤 식으로든 하이퍼스케일러입니다. 마이크로소프트, 아마존, 구글, 오라클도 조금, 메타도 조금요."),
        (1328.8, "I'm very careful how I say this: 70% of the AI revenue that Microsoft, Amazon and Google are currently generating is just from these two guys.",
         "조심해서 말하자면, 마이크로소프트·아마존·구글이 지금 버는 AI 매출의 70%가 이 두 회사에서만 나옵니다."),
    ])]),
    "eisL_bankrupt": ("eis", "eis_fail", [(1707.42, 1744.8, [
        (1707.42, "The economy is also very heavily dependent upon the AI story, because US GDP will probably grow 2-ish percent this year. Over half of that, I would say, is all this AI capex.",
         "경제도 AI 이야기에 아주 크게 기대고 있습니다. 올해 미국 성장률이 2% 남짓일 텐데, 제 생각에 그 절반 넘게가 AI 설비투자입니다."),
        (1722.7, "All the money people are spending on the infrastructure — the chips, the equipment, the construction.", "인프라에 쓰는 돈 전부요. 칩, 장비, 건설까지."),
        (1730.34, "If — and it's a big if, I'm not making that prediction right now — but if Anthropic and OpenAI went bankrupt tomorrow, the US would go into a recession the next day, because the whole chain would slow down.",
         "큰 가정이고 지금 그렇게 예측하는 건 아니지만, 앤트로픽과 오픈AI가 갑자기 파산하면 미국은 곧바로 침체에 들어갑니다. 사슬 전체가 느려지니까요."),
    ]), (1779.56, 1819.9, [
        (1779.56, "There's a big difference between a great financial crisis and a bubble. In the great financial crisis, the banks were all at risk of going under. When you can't get your money out of the bank, that's another level of disaster.",
         "대형 금융위기와 거품은 크게 다릅니다. 금융위기 때는 은행들이 다 쓰러질 위험에 있었죠. 은행에서 돈을 못 찾는 건 차원이 다른 재앙입니다."),
        (1798.1, "When companies go bankrupt, it's a recession. The banks will be fine, because they're much better regulated and have much less leverage. So I'm not worried about the banks at all.",
         "회사들이 파산하면 그건 침체입니다. 은행은 괜찮을 겁니다. 규제가 훨씬 세고 빚도 훨씬 적거든요. 은행은 전혀 걱정하지 않습니다."),
        (1810.6, "But you'll have a recession. It's painful. People lose their jobs. But the US is the most dynamic economy in the world — we'll come out of it.",
         "하지만 침체는 옵니다. 아프고, 사람들이 일자리를 잃습니다. 그래도 미국은 세계에서 가장 역동적인 경제라 빠져나올 겁니다."),
    ])]),
    "eisL_change": ("eis", "eis_change", [(1531.82, 1550.5, [
        (1531.82, "(Host) If you had to bet your net worth on one outcome, which outcome would you be betting on?", "(진행자) 전 재산을 한쪽에 건다면, 어느 쪽에 거시겠습니까?"),
        (1540.06, "I was thinking about betting it on that until the midterm elections. — So you've changed it? — I've changed since last week. As Senator Patrick Moynihan once said, facts change, I change.",
         "중간선거 전까지는 그쪽에 걸 생각이었습니다. (바꾸셨어요?) 중간선거 뒤로 바뀌었습니다. 모이니핸 상원의원 말처럼, 사실이 바뀌면 저도 바뀝니다."),
    ])]),
    "eisL_midterm": ("eis", "eis_change", [(1828.38, 1853.0, [
        (1828.38, "Well, the midterms threw a whole wrinkle into this thing. It really depends on how much AI data construction slows. Now it's going to slow. The question is how much.",
         "중간선거가 판을 꼬아 놨습니다. AI 데이터센터 건설이 얼마나 느려지느냐에 달렸어요. 느려지긴 할 겁니다. 문제는 얼마나냐죠."),
        (1841.12, "If Bernie Sanders had his way, there'd be a 100% moratorium on all AI data center construction, and the US would go into recession that night.",
         "버니 샌더스 뜻대로라면 AI 데이터센터 건설이 100% 멈출 거고, 미국은 그날 밤 바로 침체에 들어갑니다."),
    ]), (1885.18, 1917.6, [
        (1885.18, "One trillion dollars' worth of capex goes to zero — just deduct that from GDP, you're in a recession. It's a trillion. If it was 100 billion, it wouldn't be a big deal. The entire economy is hinging on this.",
         "1조 달러 설비투자가 0이 된다면, GDP에서 그만큼 빼 보세요. 침체입니다. 1,000억이면 별일 아니겠지만, 1조예요. 경제 전체가 여기에 걸려 있습니다."),
        (1904.74, "However, if AI data construction slows down, let's say 10, 20%, that might actually be a big positive for certain companies — which is not an intuitively obvious statement.",
         "하지만 AI 데이터센터 건설이 10~20% 정도 느려진다면, 어떤 회사들에는 오히려 큰 호재일 수 있습니다. 바로 와닿는 말은 아니죠."),
    ])]),
    "eisL_slow": ("eis", "eis_slow", [(1919.14, 2012.0, [
        (1919.14, "Part of the problem with the whole AI story is that because it's grown so rapidly, it's costing a fortune. You're spending a trillion dollars this year. If you spent 250 billion instead, you'd get there later, but you wouldn't be spending so much every single year.",
         "AI 이야기의 문제 하나는, 너무 빨리 커서 엄청난 돈이 든다는 겁니다. 올해 1조 달러를 쓰죠. 2,500억만 쓰면 더 늦게 도착하겠지만, 해마다 이렇게 많이 쓰지는 않을 겁니다."),
        (1942.44, "These hyperscalers — Amazon, Microsoft, Google — are the most profitable companies in the history of the planet. They generate cash like lunatics. But because AI data construction is so expensive, Google's cash flow is now negative, Amazon's is negative, Microsoft is borderline.",
         "아마존·마이크로소프트·구글은 지구 역사상 가장 돈을 잘 버는 회사들입니다. 현금을 미친 듯이 벌죠. 그런데 AI 데이터센터가 너무 비싸서, 구글 현금흐름은 이제 마이너스, 아마존도 마이너스, 마이크로소프트는 아슬아슬합니다."),
        (1970.16, "So they're raising capital — not just debt, equity. Google raised 85 billion dollars in equity a few months ago. The last time was when they went public in 2005.",
         "그래서 돈을 구합니다. 빚만이 아니라 주식으로도요. 구글은 몇 달 전 850억 달러어치 주식을 찍었습니다. 마지막으로 그런 게 2005년 상장 때였어요."),
        (1992.78, "So it's possible AI data construction slows down by 10–20%. Mathematically, some of these guys would become cash-flow positive again, and they wouldn't depend on the fixed-income markets anymore — which is what makes this story very tenuous.",
         "그러니 건설이 10~20% 느려질 수 있습니다. 계산상으로 그러면 몇몇은 다시 현금흐름이 플러스가 되고, 더는 채권시장에 기대지 않게 됩니다. 이 이야기를 아슬아슬하게 만드는 게 바로 그 의존이죠."),
    ])]),
    "eisL_peak": ("eis", "eis_peak", [(2240.28, 2280.9, [
        (2240.28, "The thing that really shocked me was he said we don't even have enough poles to get the electricity from here to here. The system of construction is very stressed, because so much money has been poured into this so rapidly.",
         "정말 놀란 건, 그 사람이 전기를 끌어올 전봇대조차 모자란다고 한 겁니다. 너무 많은 돈이 너무 빨리 들어와서 건설 체계 전체가 버거워하고 있어요."),
        (2256.38, "(Host) Are you saying spending is going to slow? — Yes. They'll continue to spend the money they've allocated anyway, but they're just going to get less for their money.",
         "(진행자) 지출이 느려진다는 말씀인가요? 네. 배정한 돈은 어차피 쓸 텐데, 같은 돈으로 얻는 게 줄어들 겁니다."),
        (2267.36, "I think it'll slow. One report I read thinks peak capex will be next year, mid next year, and that it'll slow, really slow. And then some of these companies will start to return to cash-flow positive.",
         "느려질 겁니다. 제가 읽은 한 보고서는 설비투자 정점을 내년 중반으로 보고, 그 뒤 정말 느려진다고 봅니다. 그러면 몇몇 회사는 다시 현금흐름이 플러스로 돌아서겠죠."),
    ])]),
    "sherL_demand": ("gs", "sher_demand", [(1066.32, 1108.9, [
        (1066.32, "Three things would likely forestall or delay this theme from playing out: demand, access to capital, and access to power.",
         "이 흐름을 멈추거나 늦출 수 있는 건 세 가지입니다. 수요, 돈을 구하는 길, 그리고 전력이요."),
        (1075.3, "We don't believe there's a demand problem. Almost any measure across all the TMT research we can do globally affirms that the demand signal is building momentum, not losing momentum.",
         "수요 문제는 없다고 봅니다. 저희가 전 세계에서 하는 기술·미디어·통신 조사의 거의 모든 지표가, 수요 신호가 힘을 잃는 게 아니라 커지고 있다고 말합니다."),
        (1087.34, "But if there's a disruption in the demand curve, you could find yourself in an overbuilt situation. And a sustained disruption in capital behind the build-out could, irrespective of demand, cause the supply-demand imbalance to elongate.",
         "다만 수요가 흔들리면 지나치게 지은 상황이 될 수 있습니다. 그리고 건설에 들어가는 돈줄이 오래 막히면, 수요와 상관없이 수급 불균형이 길어질 수 있죠."),
    ])]),
    "sherL_15": ("gs", "sher_15", [(893.94, 952.2, [
        (893.94, "It's a much slower process for adoption on the enterprise side. Rank-and-file employees, survey after survey, are very reluctant to adopt AI because they believe they're training their own replacement.",
         "기업 쪽 도입은 훨씬 느립니다. 조사마다 보면 일반 직원들은 AI를 꺼립니다. 자기 자리를 대신할 걸 가르친다고 생각하니까요."),
        (909.16, "But in order to stand up the compute, you have to spend the money. We've done work on return on invested capital, anchoring around a bare minimum of 15% plus, and we believe hyperscalers can very easily achieve a 15% plus return.",
         "그래도 컴퓨트를 갖추려면 돈을 써야 합니다. 저희는 투하자본수익률을 따져 봤는데, 최소 15%를 기준으로 잡았고, 하이퍼스케일러는 15% 넘게 아주 쉽게 낸다고 봅니다."),
        (927.78, "We assumed what percentage of the backlog would have to turn into revenue at a certain margin. Most people were positively surprised: you wouldn't even have to approach 100% of the backlog to achieve a 15% return.",
         "받아 둔 주문 중 몇 %가 매출이 돼야 하는지 가정해 봤는데, 다들 좋은 쪽으로 놀랐습니다. 주문의 100% 근처까지 가지 않아도 15%가 나오거든요."),
    ])]),
    "chamL_roi": ("gs", "cham_roi", [(500.0, 535.35, [
        (500.0, "The status quo is budgets get instantiated, but they don't move from experimentation far down the fairway. Then you don't have the explosion of token consumption, which means utilization stays in this gray zone of 75 to 85%.",
         "지금은 예산은 잡히는데, 시험 단계에서 크게 나아가지 못합니다. 그러면 토큰 사용이 폭발하지 않고, 가동률은 75~85%의 애매한 구간에 머뭅니다."),
        (518.02, "And then this utilization problem catches up, because you have a durational mismatch between what you're paying and what you're owning if you're a neocloud.",
         "그러면 그 가동률 문제가 결국 발목을 잡습니다. 네오클라우드라면 내야 하는 돈과 가진 것의 기간이 어긋나 있으니까요."),
        (525.7, "So I think this is the whole game. In the next 18 months, the single most important thing to look at is ROI moves by the end-consuming companies.",
         "그래서 이게 승부 전부라고 봅니다. 앞으로 18개월 동안 가장 중요하게 볼 건, AI를 실제로 쓰는 회사들의 수익이 움직이느냐입니다."),
    ])]),
    "chamL_1pct": ("gs", "cham_1pct", [(544.48, 579.45, [
        (544.48, "There's this weird thing happening: if you graph agentic workflows inside 8090, token consumption is going up and agent loops are going off the charts. There are probably an order of magnitude more agents doing work in my company than humans.",
         "이상한 일이 벌어지고 있습니다. 저희 회사 8090 안의 에이전트 작업을 그려 보면, 토큰 사용이 늘고 에이전트가 도는 횟수가 치솟습니다. 사람보다 에이전트가 열 배쯤 많은 일을 하죠."),
        (561.3, "But if you ask me, what's your ROI today versus yesterday — are you 1% more profitable? Probably not. In fact, I'm 1% less profitable, because more agents running more work costs me more in aggregate, even if the per-token cost is going down.",
         "그런데 전보다 수익이 1%라도 늘었냐고 물으면, 아마 아닙니다. 오히려 1% 줄었어요. 에이전트가 일을 더 많이 하니, 토큰당 값이 내려가도 전체로는 돈이 더 들거든요."),
    ])]),
    "chamL_bump": ("gs", "cham_bump", [(1330.0, 1366.95, [
        (1330.0, "All the predictions about the internet were right. All the productivity gains were right. All the revenue gains were right. But they were wrong about the timing.",
         "인터넷에 대한 예측은 다 맞았습니다. 생산성도, 매출도 다 맞았어요. 틀린 건 시기였습니다."),
        (1340.26, "We went through a clearing process from 2002 — I lived it till really 2007 — and then there was the GFC. We didn't find our footing as an industry until 2010, 2011. That's a long time.",
         "2002년부터 정리 과정을 거쳤고, 저는 2007년까지 그걸 겪었고, 그다음엔 금융위기가 왔습니다. 업계가 다시 자리를 잡은 건 2010, 2011년이었죠. 긴 시간입니다."),
        (1353.92, "I think there's going to be this bump in the road at some point, because you're not going to get the timing right in all scenarios. But the hypers are going to be fine — incredible businesses with pristine balance sheets.",
         "언젠가는 길에 이런 턱이 나올 겁니다. 모든 경우에 시기를 맞힐 순 없으니까요. 하지만 하이퍼스케일러들은 괜찮을 겁니다. 재무가 깨끗한 엄청난 회사들이니까요."),
    ])]),
}
BROADCAST_VF = "scale=1664:936,pad=1920:1080:128:0:color=0x15171c"

for key, (src, base, segs) in B.items():
    a, b = segs[0][0], segs[-1][1]
    f = copy.deepcopy(d["footage"][base])
    f.update(file=f"{key}.mp4", start=mmss(a), end=mmss(b))
    d["footage"][key] = f
    out = P / "04_assets" / "footage" / f["file"]
    if not out.exists():
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.2f}", "-i", str(SRC / f"{src}_full.mp4"), "-t", f"{b - a:.2f}",
                        "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(out)], check=True)


def seg_entries(key):
    segs = B[key][2]
    a0 = segs[0][0]
    return [{"key": sub[0][1], "start": round(s0 - a0, 3), "end": round(s1 - a0, 3), "score": 1.0,
             "subs": [{"t": round(t - s0, 3), "en": en, "ko": ko} for t, en, ko in sub]} for s0, s1, sub in segs]


WHY = [("card_type", "카드로 줄이면 그 사람이 어떤 논리로 말하는지 안 보임 — 원본 영상이 있으면 영상 (2026-11-27 사용자)"),
       ("quote", "원본 영상이 있어 본인 목소리로 — 글 카드는 원본이 없을 때만 (README §2-7)"),
       ("bignum", "숫자 하나로 줄이면 주장이 아니라 결과만 남음"), ("motionboard", "설명이 먼저 오면 내레이션이 주장을 대신 요약하게 됨 (09 §5-00-1)"),
       ("checklist", "목록으로 줄이면 논리의 흐름이 끊김"), ("bars", "그래프는 주장을 들은 뒤 의문이 생긴 곳에서"), ("versus", "맞대기는 두 사람의 말을 들은 뒤에"),
       ("kinetic", "큰 글자 연출은 쓰지 않음 (2026-11-27 사용자)"), ("footage", "말 없이 화면만 깔면 판단의 주인이 흐려짐"), ("share", "몫 나누기는 설명 장면"), ("stage", "설명 무대는 주장을 들은 뒤 — 먼저 그 사람의 말"), ("map_causal", "인과 지도는 정리 장면에서"), ("kb", "사진 위 내레이션은 그 사람의 목소리를 대신하지 못함")]
OLD_BITE = {1: "eisL_fail", 2: "sherL_demand", 8: "eisL_70", 13: "eisL_bankrupt", 16: "eisL_change", 18: "eisL_slow", 20: "eisL_peak",
            23: "sherL_15", 27: "chamL_roi", 28: "chamL_1pct", 30: "chamL_bump"}
INTRO = {13: "그가 가장 세게 한 말은 이것입니다.", 16: "인터뷰 중간, 진행자가 이렇게 묻습니다.", 20: "그는 건설 현장에서 들은 이야기부터 꺼냅니다.",
         28: "왜 수익이 아직 안 보이느냐는 질문에, 그는 자기 회사 이야기를 합니다."}
REPL = [("여기서부터는 이 채널의 계산입니다.", "여기서부터는 가설입니다."), ("여기서부터는 이 채널의 해석입니다.", "여기서부터는 가설입니다."),
        ("여기서부터는 이 채널의 정리입니다.", "여기서부터는 가설입니다."), ("한국 반도체에는 꼭 좋은 소식이 아닙니다", "칩과 메모리를 파는 쪽에는 꼭 좋은 소식이 아닙니다")]


def bite_scene(key, sid, ch, intro, template=None):
    who = d["footage"][key]["who"]
    s = copy.deepcopy(template) if template else {"type": "bite", "insight": True, "who": who}
    s.update(type="bite", id=sid, chapter=ch)
    s.pop("quote", None), s.pop("orig", None), s.pop("keyword", None)
    s["beats"] = [{"say": intro}] if intro else s.get("beats", [])[:1]
    s["clip"] = {"src": key, "lang": "en", "cuts": [{"find": en, "ko": ko} for _, _, sub in B[key][2] for _, en, ko in sub]}
    if key == "eisL_midterm":   # 이 구간엔 원본의 설명 카드(DOAC CONTEXT)가 아래쪽에 뜸 → 위로 줄여 우리 자막과 겹치지 않게
        s["clip"]["vf"] = BROADCAST_VF
        s["show_en"] = False
    if key.startswith(("sher", "cham")):   # 골드만 대담은 소리만 있는 팟캐스트(화면 = 정지 표지) — 누가 말하는지 이름표를 켬
        s["show_lower"] = True
        s.pop("lower_top", None)
    dec = s.setdefault("decide", {"situation": "said", "pick": "bite", "why": "주장을 본인 말로 충분히", "intent": "누가 무엇을 어떤 논리로 말하는지 먼저 안다",
                                  "refs": ["manual/09-market-daily.md#5-00-1"]})
    dec["pick"] = "bite"
    dec["why"] = f"{who}의 주장을 본인 말로 끝까지 — '{B[key][2][0][2][0][2][:28]}…'"
    for alt, why in WHY:
        if not any(o.get("id") == alt for o in dec.setdefault("over", [])):
            dec["over"].append({"id": alt, "why_not": why})
    return s


scenes, cuts = [], {}
for s in d["scenes"]:
    i = s["id"]
    if i in (3, 4, 38):
        continue
    s = copy.deepcopy(s)
    if s.get("skin") == "newsprint":
        s["skin"] = "dark-doc"
    for b in s.get("beats", []):
        for a, c in REPL:
            b["say"] = b["say"].replace(a, c)
    if i in OLD_BITE:
        s = bite_scene(OLD_BITE[i], i, s["chapter"], INTRO.get(i), s if s["type"] == "bite" else
                       {"type": "bite", "insight": True, "who": "스티브 아이스먼", "role": s.get("role", "'빅쇼트'의 실제 모델 · 투자자"),
                        "label": "의견이며 사실이 아닙니다 · The Diary Of A CEO (현지 11.23 공개) · 28분 30초~30분 20초"})
        cuts[f"tmp{i}"] = seg_entries(OLD_BITE[i])
    if i == 5:
        s["beats"][0]["say"] = "그래서 이 영상의 질문은 하나입니다. AI 투자가 꺾인다면, 반도체 주문은 무엇 때문에, 언제 멈출까요? 먼저 아이스먼이 무엇으로 시장을 읽는지부터 보겠습니다."
    if i == 17:
        s["beats"][0]["say"] = "무엇이 그를 바꿨을까요. 데이터센터를 짓는 허가는 대통령이 아니라 마을과 주가 정합니다. 땅, 물, 전기를 받는 일이 다 지역의 일입니다."
    if i == 19:
        s["beats"][0]["say"] = "골드만 대담의 차마스 팔리하피티야도 같은 곳을 짚었습니다. 빅테크가 빚에 이어 주식까지 찍어 짓고 있다는 겁니다."
    if i == 25:
        s["beats"][0]["say"] = "그런데 맞서던 두 사람이 한 고리에서는 같은 말을 합니다. 아이스먼은 앞에서 들은 대로, 병목은 돈이 아니라 전력이라고 했습니다."
    if i == 35:
        s["title"] = "무엇을 보면 되나 — 먼저 움직일 숫자"
        s["beats"][0]["say"] = "그럼 누가 맞는지 무엇이 먼저 알려 줄까요. 사라 팔라는 말이 아니라, 지켜볼 숫자입니다."
    if s["type"] == "outro":
        s["beats"][0]["say"] = ("처음으로 돌아가 보겠습니다. 아이스먼은 두 회사 중 하나가 무너지면 주문이 멈춘다고 했고, 셰리든은 수요 문제는 없다고 했습니다. "
                                "하지만 아이스먼 자신도 지금은 무너짐보다 느려짐을 더 봅니다. 문제는 꺾이느냐가 아니라, 얼마나 빨리 느려지느냐입니다.")
        s["title"] = "AI 투자, 꺾임이 아니라 느려짐의 속도"
        s["sub"] = "출처는 설명란에 · 투자 권유가 아닙니다"
    scenes.append(s)
    if i == 16:   # 생각을 바꾼 이유 — 그의 말로 (새 발언)
        scenes.append(bite_scene("eisL_midterm", 1600, s["chapter"], "무엇이 바뀌었는지, 그의 말입니다.",
                                 {"type": "bite", "insight": True, "who": "스티브 아이스먼", "role": "'빅쇼트'의 실제 모델 · 투자자",
                                  "label": "의견이며 사실이 아닙니다 · The Diary Of A CEO (현지 11.23 공개) · 30분 30초 무렵"}))
        cuts["tmp1600"] = seg_entries("eisL_midterm")
for k, s in enumerate(scenes, 1):
    old = s["id"]
    if f"tmp{old}" in cuts:
        cuts[str(k)] = cuts.pop(f"tmp{old}")
    s["id"] = k
d["scenes"] = scenes
d["package"]["title_options"] = [t.replace("AI 설비투자와 하이닉스", "AI 설비투자는 느려지나") for t in d["package"]["title_options"]]
if d.get("direction"):
    d["direction"]["vocabulary"] = [x for x in d["direction"].get("vocabulary", []) if x != "kinetic"]
hp.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
(P / "02_script" / "cuts.json").write_text(json.dumps(cuts, ensure_ascii=False, indent=1), encoding="utf-8")
tot = sum(s1 - s0 for k in B for s0, s1, _ in B[k][2])
print(len(scenes), "장면 · 발언", len(B), "구간 · 합", round(tot, 1), "초")

# 썸네일: 확정 스타일 세 장 (02_script/make_thumbs.py)
d = json.loads(hp.read_text(encoding="utf-8"))
d["package"]["thumbnails"] = [{"id": k, "name": n, "layout": "composite", "file": f"05_edit/thumbnail_{k}.png", "why": [w]} for k, n, w in (
    ("A", "인물 — 아이스먼 + 'AI 회사 하나 무너지면 칩 주문 멈춘다'", "당사자 얼굴 + 그의 경고(주어 포함)"),
    ("B", "인물 — 아이스먼 + 'AI 설비투자, 무너짐 아닌 느려짐'", "그가 바꾼 판단"),
    ("C", "맞대기 — 아이스먼 '멈춘다' vs 골드만 '없다' (글)", "두 판단을 한 장에 — 골드만은 소리만 있는 대담이라 사진 없음"))]
d["package"]["thumb_note"] = "2판(11-27 재검수): 확정 스타일(make_thumbs.py)"
hp.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")

PICS_OFF = set()
# 바탕 톤 통일 (README §2-6): 코르크판(board) 장 표지·인과 지도 → 먹색(noir, 빅테크 빚 편과 같게),
# 발언 화면 위에 1판이 얹던 설명 카드는 뺌 (방송 그래픽과 겹침 — 발언은 그대로 듣게)
d = json.loads(hp.read_text(encoding="utf-8"))
for s in d["scenes"]:
    if s.get("look") == "board":
        s["look"] = "noir"
    if s["type"] == "map_causal":   # 인과 지도에 noir 표지 설정을 주면 글자가 두 번 그려짐 (overlap_qa) → 표지 설정 없이 먹색 바탕만
        s.pop("look", None)
        s["skin"] = "dark-doc"
        for b in s.get("beats", []):   # 강조 상자를 원래 상자 위에 한 번 더 그려 overlap_qa 가 글자 겹침으로 잡음 → 강조 겹그리기 뺌
            b.pop("active", None)
    if s["type"] == "bite":
        for b in s.get("beats", []):
            b.pop("motion", None)
    if s["type"] == "checklist" and s.get("pics") and PICS_OFF and s["id"] in PICS_OFF:
        s.pop("pics")   # 오른쪽 그림 칸의 작은 글씨 대비 부족 (layout_qa)
hp.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")

# 화면 글자까지 '이 채널의 계산/해석' → '가설' (README §2-8)
_t = hp.read_text(encoding="utf-8")
for _a, _b in (("이 채널의 계산", "가설 계산"), ("이 채널 계산", "가설 계산"), ("이 채널의 해석", "가설"), ("이 채널의 정리", "가설"), ("이 채널의 판단", "가설"), ("해석 · 이 채널의 단순 계산", "가설 · 단순 계산"), ("여기서부터는 해석", "여기서부터는 가설")):
    _t = _t.replace(_a, _b)
hp.write_text(_t, encoding="utf-8")
