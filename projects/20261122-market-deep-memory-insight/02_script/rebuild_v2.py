"""메모리 2부 2판 — 매뉴얼 v146·v147(09 §5-00-1) 기준으로 다시 (2026-11-27 사용자: "이 기준대로 기존 예약 업로드 영상들 다시 검수하고 제작해주세요").

바꾼 것:
- 발언 5구간(13~18초, 합 79초) → 6구간을 주장 하나 전체로 (최태원 둘·메로트라 둘·아리아·커윈). 원본 전체를 받아 받아쓰기로 다시 고름.
- 아리아 인용 카드(#14) → 원본 영상 발언 (CNBC 원본이 있음). 젠슨 황(#16)은 원본을 찾지 못해 인용 카드 그대로.
- #7 설명 무대는 방금 들은 최태원의 말을 되풀이하지 않게 줄임.
- 키네틱(#29) 뺌 — 그 한 줄은 끝 장면 첫 문장으로.
- newsprint(베이지) → dark-doc (README §2-6, 시장 = 빅테크 빚 편 톤).
실행: python projects/20261122-market-deep-memory-insight/02_script/rebuild_v2.py
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
cuts = json.loads((P / "02_script" / "cuts_v1.json").read_text(encoding="utf-8"))


def mmss(x):
    return f"{int(x // 60)}:{x % 60:04.1f}"


# 새 발언 구간: (원본, 시작초, 끝초, [(구간 안 시각, 영어, 한국어), ...])
B = {
    "cheyL_double": ("chey", 747.58, 787.7, "FWrZTOIVgNg", [
        (0, "That's why I put in the huge money scheduled to expand the fab.", "그래서 생산 시설을 늘리려고 막대한 돈을 투자하기로 한 겁니다."),
        (8.5, "So I already announced that within five years, we're gonna double up our capacity, but for most of the customers, that's not enough. So we need more.",
         "5년 안에 생산능력을 두 배로 늘리겠다고 이미 발표했지만, 대부분의 고객에게는 그것도 모자랍니다. 더 필요하다는 거죠."),
        (21.12, "So that's the kind of problem right now, but physically something is not possible.", "지금 문제는 그겁니다. 물리적으로 안 되는 게 있다는 거죠."),
        (28.96, "That's what we call the AI bottleneck. So right now the memory chip is the AI bottleneck.", "그게 바로 AI 병목입니다. 지금은 메모리 칩이 AI의 병목이에요."),
    ]),
    "cheyL_cycle": ("chey", 1823.5, 1913.4, "FWrZTOIVgNg", [
        (0, "I told you the demand side, but what I really believe is, in the past, the cycle of the memory business depended on the number of people, the number of hardware sets.",
         "수요 쪽을 말씀드렸는데요, 제가 정말 믿는 건 이겁니다. 지난 메모리 사이클은 사람 수, 하드웨어 대수에 달려 있었습니다."),
        (15.34, "You're not going to buy tens of smartphones some day. So the number of people is limited, bounded by the whole market.",
         "스마트폰을 한 번에 열 대씩 사지는 않으니까요. 사람 수에 묶여서 시장 전체에 한계가 있었습니다."),
        (38.06, "But the AI era, I think, is different. You might have ten different AI agents to help you, and all those agents need more memory.",
         "그런데 AI 시대는 다릅니다. 한 사람이 AI 에이전트를 열 개씩 둘 수 있고, 그 에이전트마다 메모리가 더 필요합니다."),
        (52.8, "So that kind of expansion. I don't want to say there is no cycle, but the cycle movement has to change. It's a much longer cycle.",
         "그런 식으로 커지는 겁니다. 사이클이 없다고 말하고 싶진 않지만, 사이클의 움직임은 바뀔 수밖에 없습니다. 훨씬 긴 사이클이 되는 거죠."),
        (68.88, "I'm not really sure, because nobody sees the whole future, but I feel this is not the normal thing we used to see in the memory business.",
         "확실하진 않습니다. 미래를 다 보는 사람은 없으니까요. 하지만 지금은 메모리 사업에서 보던 평범한 상황이 아니라고 느낍니다."),
        (83.64, "So this is a kind of turning point for us — some structural change.", "우리에겐 일종의 전환점, 구조적인 변화라고 봅니다."),
    ]),
    "mehrotraL_short": ("mehrotra", 186.6, 240.1, "-_UQlOXVmXQ", [
        (0, "Of course, the demand for memory has really surged, because of the importance, the value and the capability of memory that is essential for all advanced systems.",
         "메모리 수요는 정말 크게 늘었습니다. 모든 첨단 시스템에 꼭 필요한 메모리의 중요성과 가치, 성능 때문이죠."),
        (13.38, "And yes, there is a shortage, but Micron is working hard to increase supply through these projects in Manassas, Virginia, Boise and New York.",
         "네, 부족한 건 맞습니다. 그래서 마이크론은 버지니아 머내서스, 보이시, 뉴욕의 공장으로 공급을 늘리려 애쓰고 있습니다."),
        (25.94, "And we see this shortage continuing beyond, well beyond the 2026 timeframe.", "그리고 이 부족은 2026년을 넘어, 훨씬 넘어서까지 이어진다고 봅니다."),
        (31.72, "But the important thing is that Micron is working with our customers on long-term supply agreements, so they can have predictability for supply, and Micron can have confidence in the investments we are committing for the long haul.",
         "중요한 건, 고객과 장기 공급 계약을 맺고 있다는 겁니다. 고객은 공급을 내다볼 수 있고, 마이크론은 길게 보고 하는 투자에 확신을 가질 수 있죠."),
    ]),
    "mehrotraL_shell": ("mehrotra", 260.74, 287.7, "-_UQlOXVmXQ", [
        (0, "Of course, what we are doing is building these fabs, which are very long lead time items.", "저희가 짓는 공장은 완공까지 아주 오래 걸리는 시설입니다."),
        (6.1, "As you can see at Boise and New York, it really takes several years just to construct the shell.", "보이시와 뉴욕만 봐도, 건물 껍데기를 짓는 데만 몇 년이 걸립니다."),
        (14.58, "How we equip that shell really depends on our latest assessment of demand at a given time.", "그 껍데기에 장비를 어떻게 채울지는, 그때그때 수요를 새로 따져 보고 정합니다."),
        (23.06, "So the important thing is to have that preparedness to meet the market demand.", "중요한 건 시장 수요에 맞출 준비를 해 두는 거죠."),
    ]),
    "aryaL": ("arya", 34.24, 95.9, "ikTz_0Z9FjU", [
        (0, "Good morning. I think what we are witnessing is what I would call a structural rather than a cyclical shift in the memory industry.",
         "지금 우리가 보는 건, 사이클이 아니라 메모리 산업의 구조적 변화라고 부르고 싶습니다."),
        (8.42, "It is critical to AI. There is no AI without memory, and it is just three or four times harder to create memory chips for AI than for conventional computing.",
         "메모리는 AI에 꼭 필요합니다. 메모리 없는 AI는 없고, AI용 메모리 칩은 일반 컴퓨터용보다 만들기가 서너 배 어렵습니다."),
        (19.08, "The second important thing we are seeing is a lot of discipline among the three scaled memory companies, two in Korea, one in the US, which is Micron. We are seeing real price discipline",
         "두 번째로 중요한 건, 큰 메모리 회사 셋 — 한국 둘, 미국의 마이크론 — 사이에 규율이 생겼다는 겁니다. 값을 지키는 규율이죠."),
        (33.16, "because it's not only hard to create these chips, these companies have been through these up and down cycles many times before. So this time they have newfound pricing discipline.",
         "칩을 만들기 어려워서이기도 하지만, 이 회사들이 오르내리는 사이클을 여러 번 겪었기 때문입니다. 그래서 이번엔 값을 지키는 새 규율이 생겼습니다."),
        (43.9, "And the last thing is very strong free cash flow. Micron can pretty much afford to buy 10 percent of its stock every year with the cash it is generating. So we do think it is different this time.",
         "마지막으로, 이번 사이클엔 잉여현금이 아주 많이 나옵니다. 마이크론은 버는 현금으로 해마다 자기 주식 10%를 살 수 있을 정도예요. 그래서 이번엔 다르다고 봅니다."),
    ]),
    "kerwinL": ("kerwin", 40.0, 110.8, "w-WMH2Qpk1w", [
        (0, "I think the key word there is cycle. We observe what's going on as a super cycle, to use that term, but we think it is a cycle all the same.",
         "핵심 낱말은 '사이클'입니다. 지금 상황을 슈퍼사이클이라 부를 수는 있지만, 그래도 사이클은 사이클이라고 봅니다."),
        (10.72, "These memory chips, whether NAND or DRAM and HBM, are extremely supply constrained. They trade like commodities, and when there's a supply constraint, the market reaches a market clearing price.",
         "낸드든 D램이든 HBM이든, 이 메모리 칩들은 공급이 극도로 모자랍니다. 원자재처럼 거래되니, 공급이 막히면 시장이 값을 맞출 때까지 올라갑니다."),
        (24.98, "So we've seen prices go up and up, and those increases have been accelerating over the last 12 months. That's driven huge fundamentals and skyrocketing stock prices.",
         "그래서 값이 오르고 또 올랐고, 지난 12개월 동안 오르는 속도도 빨라졌습니다. 그게 실적과 주가를 크게 밀어 올렸죠."),
        (39.14, "But again, we think this is finite. We look at the late end of 2027, and more materially 2028, for a whole lot of new supply coming online to put downward pressure on prices.",
         "하지만 이건 끝이 있다고 봅니다. 2027년 말, 더 크게는 2028년에 새 공급이 대거 들어와 값을 끌어내릴 겁니다."),
        (52.76, "So the next 12 months of fundamentals probably look really good. But for long-term investors, we think there is a lot of risk baked into these valuations.",
         "그래서 앞으로 12개월 실적은 아주 좋아 보입니다. 하지만 오래 들고 갈 투자자에게는, 지금 주가에 위험이 많이 들어 있습니다."),
        (62.72, "If you expect a turn down and eventually downward pressure on prices, we believe it's hard to justify the valuations today.",
         "언젠가 꺾이고 값이 내려간다고 본다면, 지금 주가를 정당화하기는 어렵다고 봅니다."),
    ]),
}
OLD = {"cheyL_double": "chey_double", "cheyL_cycle": "chey_cycle", "mehrotraL_short": "mehrotra_short",
       "mehrotraL_shell": "mehrotra_shell", "aryaL": "arya", "kerwinL": "kerwin"}
SCENE = {1: "cheyL_double", 6: "cheyL_cycle", 10: "mehrotraL_short", 11: "mehrotraL_shell", 14: "aryaL", 18: "kerwinL"}

for key, (src, a, b, vid, subs) in B.items():
    f = copy.deepcopy(d["footage"][OLD[key]])
    f.update(file=f"{key}.mp4", start=mmss(a), end=mmss(b))
    d["footage"][key] = f
    out = P / "04_assets" / "footage" / f["file"]
    if not out.exists():
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.2f}", "-i", str(SRC / f"{src}_full.mp4"), "-t", f"{b - a:.2f}",
                        "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(out)], check=True)

WHY = [("card_type", "카드로 줄이면 그 사람이 어떤 논리로 말하는지 안 보임 — 원본 영상이 있으면 영상 (2026-11-27 사용자)"),
       ("quote", "원본 영상이 있어 본인 목소리로 — 글 카드는 원본이 없을 때만 (README §2-7)"),
       ("bignum", "숫자 하나로 줄이면 주장이 아니라 결과만 남음"), ("motionboard", "설명이 먼저 오면 내레이션이 주장을 대신 요약하게 됨 (09 §5-00-1)"),
       ("checklist", "목록으로 줄이면 논리의 흐름이 끊김"), ("bars", "그래프는 주장을 들은 뒤 의문이 생긴 곳에서"),
       ("kinetic", "큰 글자 연출은 쓰지 않음 (2026-11-27 사용자)"), ("footage", "말 없이 화면만 깔면 판단의 주인이 흐려짐")]
scenes = []
for s in d["scenes"]:
    s = copy.deepcopy(s)
    if s["type"] == "kinetic":
        continue
    if s.get("skin") == "newsprint":
        s["skin"] = "dark-doc"
    if s["id"] in SCENE:
        key = SCENE[s["id"]]
        _, a, b, _, subs = B[key]
        if s["type"] == "quote":   # 아리아: 인용 카드 → 원본 영상
            s = {"type": "bite", "insight": True, "label": "의견이며 사실이 아닙니다 · 뱅크오브아메리카 반도체 분석가 · CNBC (2026.6.25, 마이크론 실적 다음 날)",
                 "who": "비벡 아리아", "role": "뱅크오브아메리카 · CNBC (6월)", "id": s["id"], "chapter": s["chapter"],
                 "beats": [{"say": "지난 6월, 마이크론 실적 다음 날 CNBC에 나온 그는 이렇게 말했습니다."}],
                 "decide": {"situation": "said", "pick": "bite", "over": [], "why": "원본 영상이 있어 본인 목소리로 주장 전체를", "intent": "구조적 변화라는 주장과 그 근거 셋을 본인 말로 듣는다",
                            "refs": ["manual/09-market-daily.md#5-00-1"]}}
        s["clip"] = {"src": key, "lang": "en", "cuts": [{"find": en, "ko": ko} for _, en, ko in subs]}
        if key.startswith("chey"):
            s["dim"] = 0.9
        else:   # 방송 화면에 자체 자막 띠·시세판 → 위로 줄여 두고 아래를 우리 자막 자리로 (09 §5-00-1 7번)
            s["clip"]["vf"] = "scale=1664:936,pad=1920:1080:128:0:color=0x15171c"
            s["show_lower"] = False
            s["show_en"] = False
        cuts[str(s["id"])] = [{"key": subs[0][1], "start": 0.0, "end": round(b - a, 3), "score": 1.0,
                               "subs": [{"t": t, "en": en, "ko": ko} for t, en, ko in subs]}]
    if s["type"] == "bite":
        ov = s.setdefault("decide", {"situation": "said", "pick": "bite", "why": "주장을 본인 말로 충분히", "intent": "누가 무엇을 어떤 논리로 말하는지 먼저 안다",
                                     "refs": ["manual/09-market-daily.md#5-00-1"]}).setdefault("over", [])
        for alt, why in WHY:
            if not any(o.get("id") == alt for o in ov):
                ov.append({"id": alt, "why_not": why})
    if s["id"] == 7:   # 방금 들은 최태원의 말을 되풀이하지 않게
        s["beats"][0]["say"] = "그의 말을 그림으로 놓으면 이렇습니다. 예전 수요의 끝은 사람 수였습니다."
        s["beats"][1]["say"] = "AI 비서를 사람마다 여럿 쓰면, 그 끝, 수요의 천장이 사람 수에서 풀립니다."
        s["beats"][2]["say"] = "그래서 사이클이 없어지는 게 아니라 길어진다는 게 그의 결론입니다. 그 근거가 숫자로도 맞는지 따져 보겠습니다."
    if s["type"] == "outro":
        s["beats"][0]["say"] = ("낙관과 신중은 수요를 두고 다투는 게 아니라, 누가 그 수요의 돈을 내고, 언제 공장이 들어오느냐를 두고 다툽니다. "
                                "메모리 부족이 언제 끝나느냐는, 메모리 공장보다 AI 회사들의 지갑과 2027년 말의 새 공장에 달려 있습니다.")
        s["title"] = "메모리 호황의 끝, 열쇠는 AI 회사의 지갑"
        s["sub"] = "출처는 설명란에 · 투자 권유가 아닙니다"
    scenes.append(s)
for k, s in enumerate(scenes, 1):
    if str(s["id"]) in cuts and s["type"] == "bite" and s["id"] != k:
        cuts[str(k)] = cuts.pop(str(s["id"]))
    s["id"] = k
d["scenes"] = scenes
if d.get("direction"):
    d["direction"]["vocabulary"] = [x for x in d["direction"].get("vocabulary", []) if x != "kinetic"]
hp.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
(P / "02_script" / "cuts.json").write_text(json.dumps(cuts, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(scenes), "장면 · 발언", [round(B[k][2] - B[k][1], 1) for k in B], "합", round(sum(B[k][2] - B[k][1] for k in B), 1))

# 썸네일: 확정 스타일 세 장 (02_script/make_thumbs.py) — 자동 단계가 덮지 않게 composite
d = json.loads(hp.read_text(encoding="utf-8"))
d["package"]["thumbnails"] = [{"id": k, "name": n, "layout": "composite", "file": f"05_edit/thumbnail_{k}.png", "why": [w]} for k, n, w in (
    ("A", "인물 — 최태원 + '메모리 호황, 훨씬 길게 간다'", "공급자 당사자 얼굴 + 주어·주장"),
    ("B", "인물 — 커윈 + '메모리 호황, 2027년 말 꺾인다'", "신중한 쪽 주장 + 날짜"),
    ("C", "맞대기 — 최태원 vs 커윈 사진 반반", "두 판단을 한 장에"))]
d["package"]["thumb_note"] = "2판(11-27 재검수): 확정 스타일(make_thumbs.py) — 1판은 빨간 꼬리표·이름표 상자 틀"
hp.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")

PICS_OFF = {15, 28}
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
for _a, _b in (("이 채널의 계산", "가설 계산"), ("이 채널 계산", "가설 계산"), ("이 채널의 해석", "가설"), ("이 채널의 정리", "가설"), ("이 채널의 판단", "가설")):
    _t = _t.replace(_a, _b)
hp.write_text(_t, encoding="utf-8")
