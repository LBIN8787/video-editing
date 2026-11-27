"""빅테크 빚 편 2판 — 매뉴얼 v146·v147(09 §5-00-1) 기준으로 다시 (2026-11-27 사용자: "이 기준대로 기존 예약 업로드 영상들 다시 검수하고 제작해주세요").

이 편은 바탕 톤의 기준 영상이라 화면은 그대로 두고, 발언과 마디만 바꾼다:
- 재시(세마포) 두 토막(#1·#2, 7초+15초) → 한 구간 57초 (현금이 도는 방식 → 몇 년 뒤 → AWS 1조 달러).
- 위글스워스 두 토막(#6·#7, 13초+8초) → 한 구간 32초 ('AI 호황이 빚으로 굴러가기 시작한 해').
- 재시 #35 → 22초, 크레센치 #38(12초) → 61초 (코어위브 → 프랑스·트러스 → 모든 채권).
- 키네틱 2장(#9·#63) 뺌. 인용 카드 4장은 글 출처(연준 블로그·기사)라 원본 영상이 없어 그대로.
- 원본 받아쓰기: 04_assets/footage/_src/*_tr.json (faster-whisper small).
실행: python projects/20261126-market-deep-dc-funding/02_script/rebuild_v2.py
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
VF = "scale=1664:936,pad=1920:1080:128:0:color=0x15171c"


def mmss(x):
    return f"{int(x // 60)}:{x % 60:04.1f}"


B = {
    "semL_cash": ("sem", "sem_j1a", 261.28, 318.0, False, [
        (261.28, "Now, the way the cash cycle works in a business like AWS is that you have to spend the cash for data centers, servers and networking gear well in advance of when you can monetize it.",
         "AWS 같은 사업에서 현금이 도는 방식은, 데이터센터와 서버·네트워크 장비에 돈을 버는 시점보다 한참 먼저 써야 한다는 겁니다."),
        (272.76, "So when you're growing at this unprecedented rate, you end up having a lot of capex, which creates some headwinds on your short-term free cash flow,",
         "그래서 전례 없는 속도로 크면, 설비투자가 많아지고 단기 잉여현금흐름에는 역풍이 됩니다."),
        (281.22, "but the economics of the business are such that once you get a few years out, with the data centers installed and monetizing the servers and gear in place, you really like the free cash flow and the return on invested capital.",
         "하지만 몇 년 지나 데이터센터가 다 들어서고 서버와 장비로 돈을 벌기 시작하면, 잉여현금흐름과 투하자본수익률이 아주 좋아지는 사업입니다."),
        (297.9, "And I think we're going to be a much larger company, and AWS a much larger business than we ever anticipated.",
         "그리고 아마존은 훨씬 큰 회사가, AWS는 저희가 생각했던 것보다 훨씬 큰 사업이 될 겁니다."),
        (305.32, "We felt AWS could be a few hundred billion-dollar revenue run-rate business. We now believe it can be over a trillion dollars in the next five to ten years.",
         "AWS가 연 매출 수천억 달러 사업이 될 수 있다고 봤는데, 이제는 5~10년 안에 1조 달러를 넘을 수 있다고 봅니다."),
    ]),
    "wiggL": ("wigg", "wigg_a", 134.34, 166.3, True, [
        (134.34, "My view is it's always an incredible year for the bond market. But I think this is an unusual time, because it's really the year when the AI boom became debt-financed.",
         "채권시장은 늘 대단한 해라고 보지만, 올해는 특별합니다. AI 호황이 빚으로 굴러가기 시작한 해거든요."),
        (145.56, "It used to be financed primarily by the huge, prodigious free cash flows of these companies — incredible companies with incredible products.",
         "전에는 주로 이 회사들의 어마어마한 잉여현금으로 돈을 댔습니다. 대단한 제품을 가진 대단한 회사들이죠."),
        (153.62, "But this year they're kind of tapped out of that, and are turning to the bond market, to securitization, to private credit.",
         "그런데 올해는 그 돈을 거의 다 써서, 채권시장으로, 유동화로, 사모 대출로 가고 있습니다."),
        (160.66, "I think if this does break bad at some point, we're going to look at 2026 as the year when it started.",
         "언젠가 이게 나빠진다면, 2026년을 그 시작으로 돌아보게 될 겁니다."),
    ]),
    "semL_players": ("sem", "sem_j2", 502.28, 524.1, False, [
        (502.28, "I think it'll be interesting over time whether all the different players who are building data centers have a broad enough business, with enough services, to build long-term sustainable businesses. We'll have to see.",
         "데이터센터를 짓는 여러 회사가 오래 버틸 사업을 만들 만큼 넓은 사업과 서비스를 가졌는지는, 시간이 지나 봐야 알 겁니다. 지켜봐야죠."),
        (519.68, "It is growing so fast — I can understand why a lot of people are interested in it.", "워낙 빨리 크니까, 많은 사람이 뛰어드는 이유는 이해합니다."),
    ]),
    "cresL": ("cres", "cres", 178.58, 240.0, True, [
        (178.58, "Well, it's not considered to be amongst the strongest. It's not a hyperscaler, so to speak. So what it's showing you is that the bond market is willing to impose discipline on borrowers that may have cash flow that's less clear to them.",
         "코어위브는 가장 튼튼한 쪽으로 여겨지지 않습니다. 이른바 하이퍼스케일러가 아니죠. 그러니 이건, 현금흐름이 덜 분명한 차입자에게 채권시장이 규율을 들이댈 준비가 돼 있다는 걸 보여 줍니다."),
        (197.36, "So it may not apply simply to lower-rated companies. It can eventually apply to high-rated nations. Look at France — considered much better as a credit, but with a very high budget deficit, and the bond market is beginning to impose discipline on it.",
         "신용등급 낮은 회사에만 해당하는 것도 아닙니다. 결국 등급 높은 나라에도 해당될 수 있어요. 프랑스를 보세요. 신용은 훨씬 좋다지만 재정적자가 커서, 채권시장이 규율을 들이대기 시작했습니다."),
        (216.76, "It did so in 2022 when Liz Truss attempted to raise the budget deficit. The bond market said no, and the 10-year yield rose 150 basis points in a few weeks — dramatic for a government bond market. So the CoreWeave story can be applied to all bonds.",
         "2022년 리즈 트러스 총리가 재정적자를 늘리려 하자 채권시장이 안 된다고 했고, 10년물 금리가 몇 주 만에 1.5%포인트 뛰었습니다. 국채시장에선 극적인 일이죠. 그러니 코어위브 이야기는 모든 채권에 적용될 수 있습니다."),
    ]),
}
SCENE = {1: "semL_cash", 6: "wiggL", 35: "semL_players", 38: "cresL"}
DROP = {2, 7, 9, 63}
WHY = [("card_type", "카드로 줄이면 그 사람이 어떤 논리로 말하는지 안 보임 (2026-11-27 사용자)"), ("quote", "원본 영상이 있어 본인 목소리로 (README §2-7)"),
       ("bignum", "숫자 하나로 줄이면 결과만 남음"), ("motionboard", "설명이 먼저 오면 내레이션이 주장을 대신 요약함 (09 §5-00-1)"),
       ("checklist", "목록으로 줄이면 논리가 끊김"), ("bars", "그래프는 주장을 들은 뒤"), ("versus", "맞대기는 말을 들은 뒤"), ("kinetic", "큰 글자 연출은 쓰지 않음"),
       ("footage", "말 없이 화면만 깔면 판단의 주인이 흐려짐"), ("stage", "설명 무대는 주장을 들은 뒤"), ("kb", "사진 위 내레이션은 목소리를 대신 못 함"),
       ("zoomshot", "원문 확대는 근거 장면에서")]

for key, (src, base, a, b, _, _) in B.items():
    f = copy.deepcopy(d["footage"][base])
    f.update(file=f"{key}.mp4", start=mmss(a), end=mmss(b))
    d["footage"][key] = f
    out = P / "04_assets" / "footage" / f["file"]
    if not out.exists():
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.2f}", "-i", str(SRC / f"{src}_full.mp4"), "-t", f"{b - a:.2f}",
                        "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(out)], check=True)

scenes = []
for s in d["scenes"]:
    if s["id"] in DROP:
        continue
    s = copy.deepcopy(s)
    if s["id"] in SCENE:
        key = SCENE[s["id"]]
        _, _, a, b, broadcast, subs = B[key]
        s["clip"] = {"src": key, "lang": "en", "cuts": [{"find": en, "ko": ko} for _, en, ko in subs]}
        if broadcast:   # 방송 자막 띠 → 위로 줄여 아래를 우리 자막 자리로 (09 §5-00-1 7번)
            s["clip"]["vf"] = VF
            s["show_lower"] = False
            s["show_en"] = False
        cuts[f"tmp{s['id']}"] = [{"key": subs[0][1], "start": 0.0, "end": round(b - a, 3), "score": 1.0,
                                  "subs": [{"t": round(t - a, 3), "en": en, "ko": ko} for t, en, ko in subs]}]
        dec = s.setdefault("decide", {"situation": "said", "pick": "bite", "intent": "그 사람의 주장과 논리를 먼저 듣는다", "refs": ["manual/09-market-daily.md#5-00-1"]})
        dec["why"] = f"{s.get('who', '')}의 주장을 본인 말로 끝까지 — '{subs[0][2][:28]}…'"
        for alt, why in WHY:
            if not any(o.get("id") == alt for o in dec.setdefault("over", [])):
                dec["over"].append({"id": alt, "why_not": why})
    if s["id"] == 1:
        s["beats"] = [{"say": "빅테크는 AI 데이터센터 지을 돈을 어디서 구하고, 언제까지 낼 수 있을까요. 이 영상은 그 돈의 출처를 따라갑니다. 11월 18일, 아마존의 앤디 재시 CEO는 이렇게 말했습니다."}]
    scenes.append(s)
for k, s in enumerate(scenes, 1):
    if f"tmp{s['id']}" in cuts:
        cuts[str(k)] = cuts.pop(f"tmp{s['id']}")
    elif str(s["id"]) in cuts and s["type"] == "bite":
        cuts[str(k)] = cuts.pop(str(s["id"])) if str(s["id"]) != str(k) else cuts[str(k)]
    s["id"] = k
cuts = {k: v for k, v in cuts.items() if not k.startswith("tmp") and int(k) <= len(scenes) and scenes[int(k) - 1]["type"] == "bite"}
d["scenes"] = scenes
if d.get("direction"):
    d["direction"]["vocabulary"] = [x for x in d["direction"].get("vocabulary", []) if x != "kinetic"]
hp.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
(P / "02_script" / "cuts.json").write_text(json.dumps(cuts, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(scenes), "장면 · 새 발언", {k: round(v[3] - v[2], 1) for k, v in B.items()})

# 화면 글자까지 '이 채널의 계산/해석' → '가설' (README §2-8)
_t = hp.read_text(encoding="utf-8")
for _a, _b in (("이 채널의 계산", "가설 계산"), ("이 채널 계산", "가설 계산"), ("이 채널의 해석", "가설"), ("이 채널의 정리", "가설"), ("이 채널의 판단", "가설")):
    _t = _t.replace(_a, _b)
hp.write_text(_t, encoding="utf-8")
