"""다모다란 편 2판 (2026-11-27 사용자 기각 반영) — 1판 hybrid.json + tone2 판의 긴 발언 구간을 엮어 다시 쓴다.

사용자 말(원문은 manual 제안함·REPORT):
- 인터뷰가 너무 짧다 → 그 사람의 주장·논리를 본인 영상으로 충분히 먼저, 의문이 들 때 설명 (설명이 발언을 미리 요약하지 않음)
- 원본 영상이 있는 발언은 인용 카드로 만들지 않는다 (1판 #17 → 영상)
- 큰 글자 키네틱(1판 #3·#30) 없앰
- '여기서부터는 이 채널의 해석/계산' → '가설'
- 배경은 빅테크 빚 편(dc-funding)처럼 먹색 — newsprint(베이지) → dark-doc
- 한국 메모리·한국 시장을 억지로 엮지 않음 → 1판 6장(하이닉스·삼성) 뺌
- 체크리스트 오른쪽 자동 아이콘이 겹쳐 보임 → 이 편은 끔(g_skip)
말투는 1판(~습니다) 그대로 — tone 판의 해요체는 기각됨(2026-11-27 피드백).
발언 구간·번역은 tone2 판(받아쓰기로 맞춘 cuts)을 쓰고, 이어진 문장은 한 구간 + 문장별 자막(subs)으로 묶는다.
실행: python projects/20261127-market-deep-anthropic-damodaran/02_script/rebuild_v2.py <tone2_hybrid.json> <tone2_cuts.json>
"""
import copy
import json
import subprocess
import sys
from pathlib import Path

P = Path(__file__).resolve().parent.parent
v1 = json.loads((P / "02_script" / "hybrid.json").read_text(encoding="utf-8"))
if v1.get("_v2"):
    v1 = json.loads((P / "02_script" / "hybrid_v1.json").read_text(encoding="utf-8"))
else:
    (P / "02_script" / "hybrid_v1.json").write_text(json.dumps(v1, ensure_ascii=False, indent=1), encoding="utf-8")
t2 = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
t2cuts = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
S1 = {s["id"]: s for s in v1["scenes"]}
S2 = {s["id"]: s for s in t2["scenes"]}
SRC = {"IgvDUUn3uuE": P / "04_assets/footage/_src/pg_full.mp4", "9s_ufgiiyLY": P / "04_assets/footage/_src/cw_full.mp4"}


def sec(x):
    m, s = str(x).split(":")
    return int(m) * 60 + float(s)


def one(i, **over):
    s = copy.deepcopy(S1[i])
    s.update(over)
    if s.get("skin") == "newsprint":
        s["skin"] = "dark-doc"
    return s


def say(s, *texts):
    for b, t in zip(s["beats"], texts):
        if t is not None:
            b["say"] = t
    s["beats"] = [b for b, t in zip(s["beats"], texts) if t != ""] if len(texts) == len(s["beats"]) else s["beats"]
    return s


NEW_CUTS = {}


def bite(t2id, intro, cut_idx=None, **over):
    s = copy.deepcopy(S2[t2id])
    if "decide" not in s:
        s["decide"] = {"situation": "said", "pick": "bite", "over": [{"id": "quote", "why_not": "원본 영상이 있어 본인 목소리로 — 글 카드는 원본이 없을 때만 (2026-11-27 사용자)"},
                       {"id": "narration", "why_not": "내레이션이 대신 요약하면 그 사람의 주장·논리가 안 보임 (2026-11-27 사용자)"}],
                       "why": "주장과 논리를 본인 말로 충분히 듣고, 의문이 생긴 곳만 설명", "intent": "이 사람이 무엇을 어떤 논리로 말하는지 먼저 안다",
                       "refs": ["manual/09-market-daily.md"]}
    cuts = t2cuts[str(t2id)]
    cl = s["clip"]["cuts"]
    if cut_idx is not None:   # tone2 #26·#27 처럼 한 원본을 둘로 나눈 것
        cuts = [cuts[k] for k in cut_idx]
        cl = [cl[k] for k in cut_idx]
    s["clip"]["cuts"] = cl
    s["beats"] = [{"say": intro}] if intro else []
    s.update(over)
    # 이어진 문장(앞 끝 = 다음 시작)은 한 구간 + 문장별 자막
    segs = []
    for c in cuts:
        if c.get("start") is None:
            continue
        if segs and abs(c["start"] - segs[-1]["end"]) < 0.06:
            g = segs[-1]
            g["subs"].append({"t": round(c["start"] - g["start"], 3), "ko": c["ko"], "en": c.get("heard", "")})
            g["end"] = c["end"]
        else:
            segs.append({"key": c["key"], "start": c["start"], "end": c["end"], "score": c.get("score", 1),
                         "subs": [{"t": 0, "ko": c["ko"], "en": c.get("heard", "")}]})
    s["_segs"] = segs
    return s


scenes = []
add = scenes.append
# 0 — 여는 장면: 그의 말부터 (요약하지 않고)
add(bite(1, "가치평가의 대가로 불리는 뉴욕대 교수 애스워스 다모다란. 상장한 앤트로픽의 값을 직접 계산한 그는, 이렇게 말했습니다."))
add(one(2))
# 1장 — 그의 이야기
add(one(4))
add(bite(5, "그가 앤트로픽에 어떤 이야기를 붙였는지, 본인의 말로 먼저 들어 보겠습니다."))
add(say(one(5), None,
        "그래서 10년 뒤 매출은 1조 달러, 영업이익률은 26.5%. 그의 말대로 지금 매출 1조 달러를 넘는 회사는 하나도 없습니다. 가장 큰 아마존과 월마트가 7,000억 달러대입니다.",
        None))
add(one(6))
add(bite(8, "그 길이 무엇에 달렸는지, 그는 이렇게 말합니다."))
# 2장 — 값의 4분의 3
add(one(9))
add(one(10))
add(bite(11, "그 역시 같은 말을 합니다."))
add(say(one(11, label="가설 · 다모다란 평가표(2026.11.18)를 그대로 다시 짜서 매출 길만 바꾼 계산 · 투자 권유 아님"),
        "여기서부터는 가설입니다. 그가 공개한 표를 그대로 다시 짜서 돌렸더니 주당 75달러 87센트, 그의 76달러와 1% 안으로 맞았습니다. 이 틀에서 다른 건 그대로 두고 매출 길만 바꿔 보겠습니다.",
        None, None, None))
add(say(one(12), "같은 틀로 거꾸로 풀어 봅니다. 11월 25일 주가 82달러 79센트를 넣으면, 2036년 매출이 약 1조 770억 달러여야 합니다.", None))
add(bite(14, "그는 왜 이렇게 밝게 봤을까요. 그리고 자기 숫자를 어떻게 부를까요."))
# 3장 — 약정
add(one(13))
add(one(14))
add(bite(17, "다모다란은 이 약정을 이렇게 봅니다."))
add(bite(19, "그렇다면 당장 위험할까요. 그의 답입니다."))
m16 = one(16)
m16["beats"] = [m16["beats"][0]]
m16["beats"][0]["say"] = ("여기서부터는 가설입니다. 앞으로 12개월 약정 707억 달러를, 회사가 밝힌 10월 말 연 환산 매출 810억 달러와 나란히 놓으면 약 87%. "
                          "버는 돈의 9할 가까이가 이미 약속돼 있는 겁니다. 그가 매출이 빨리 올라야만 숨 쉴 틈이 된다고 한 이유입니다.")
add(m16)
add(bite(20, "공정하게 덧붙이면, 그는 왜 이렇게까지 약속했는지도 이해한다고 했습니다."))
# 4장 — 캐시 우드
add(one(18))
CNBC = {"vf": "scale=1664:936,pad=1920:1080:128:0:color=0x15171c"}
add(bite(22, "상장 다음 날, 주가가 첫날 고점에서 내려오던 때 CNBC에 나온 그는 이렇게 말했습니다.",
         show_lower=False, show_en=False, lower_top=None))
add(bite(23, "앤트로픽의 높은 마진이 지켜지겠느냐는 질문에는 이렇게 답합니다.", show_lower=False, show_en=False))
add(one(21))
# 5장 — 갈리는 고리
add(one(22))
add(bite(26, "다모다란은 3분기 성장이 느려진 이유부터 짚습니다."))
add(bite(27, "그리고 더 근본적인 문제를 꺼냅니다."))
add(say(one(24), "정리하면, 다모다란은 대부분의 기업에 가장 비싼 모델은 과하다고 봅니다. 그러면 값을 내려야 하고, 매출이 늘어도 이익률 26.5%가 안 나옵니다.", None))
add(one(25))
# 6장 — 무엇을 보면 되나 (한국 고리 억지로 붙이지 않음)
ch6 = one(26, title="무엇을 보면 되나 — 숫자 넷", icon="search")
ch6["beats"][0]["say"] = "그럼 어느 쪽이 맞는지, 무엇을 보면 될까요. 사라 팔라는 말이 아니라, 지켜볼 숫자입니다."
add(ch6)
add(bite(34, "상장 전날, 그는 자기 숫자를 이렇게 쓰겠다고 했습니다."))
w = one(28, title="지켜볼 숫자 넷")
w["rows"][0]["label_full"] = "앤트로픽 새 컴퓨트 약정: 9,009억에 얼마가 더해지나"
w["beats"][0]["say"] = "볼 숫자는 넷입니다. 첫째, 앤트로픽의 새 컴퓨트 약정. 매출에 자신이 있으면 약정은 더 늘어납니다. 둘째, 첫 분기 실적의 매출 속도와 이익률."
w["beats"][1]["say"] = "셋째, 아마존과 구글의 실적입니다. 아마존은 상장 뒤 앤트로픽 자본의 23.6%를 갖습니다. 앤트로픽 주가가 곧 그 회사들의 평가손익입니다. 넷째, 주가와 다모다란의 76달러입니다."
w["g_skip"] = True
add(w)
x = one(29, label="틀리는 경우 · 근거는 위 원본 발언·424B4·평가표")
x["rows"][2]["label"] = "가설 계산의 한계: 매출만 바꿈"
x["beats"][1]["say"] = "반대로 값을 내리며 크면, 매출이 늘어도 이익률이 안 나와 우드가 틀립니다. 그리고 앞의 가설 계산은 매출만 바꾼 단순 계산입니다. 실제로는 매출이 적으면 컴퓨트도 덜 사는 식으로 다른 숫자도 같이 움직입니다."
x["g_skip"] = True
add(x)
o = one(31, title="앤트로픽의 값, 열쇠는 매출의 속도", sub="출처는 설명란에 · 투자 권유가 아닙니다")
o["beats"][0]["say"] = ("처음으로 돌아가 보겠습니다. 다모다란은 매출이 안 오면 다 무너진다고 했고, 캐시 우드는 확신이 커졌다며 더 샀습니다. "
                        "지금 주가는 그가 낙관이라 부른 길보다 조금 더 밝은 길을 깔고 있습니다. 결국 앤트로픽의 값은 기술이 아니라 매출의 속도에 걸려 있습니다.")
add(o)

# 체크리스트 오른쪽 자동 아이콘: 이 편은 끔 (겹쳐 보인 문제, 2026-11-27 사용자)
for s in scenes:
    if s["type"] == "checklist":
        s["g_skip"] = True

# 상장 전날 녹화 — 번역의 '내일'은 실제 날짜 말로 (올린 날과 보는 날이 달라도 맞게, 09 §9-1)
FIX = {"결국 내일 종가가": "결국 상장 첫날 종가가", "내일 저녁 어디서 끝나느냐죠.": "첫날 저녁 어디서 끝나느냐죠.",
       "내일 저녁 71~72달러에서": "첫날 저녁 71~72달러에서"}
for s in scenes:
    for g in s.get("_segs", []):
        for u in g["subs"]:
            for a, b in FIX.items():
                u["ko"] = u["ko"].replace(a, b)
    for c in (s.get("clip") or {}).get("cuts", []):
        for a, b in FIX.items():
            c["ko"] = c["ko"].replace(a, b)
    if s["type"] == "bite" and s["clip"]["src"].startswith("dmdL"):
        s["dim"] = 0.85   # 밝은 창가 화면에서 이름표·원문 글자 대비 (layout_qa 대비 2.61)

# 발언 장면: 요약 카드·큰 숫자 대신 영상인 이유를 모든 bite 에 (edit-plan 1순위와 다를 때 check G5)
for s in scenes:
    if s["type"] == "bite":
        ov = s["decide"].setdefault("over", [])
        for alt, why in (("card_type", "카드로 줄이면 그 사람이 어떤 논리로 말하는지 안 보임 — 원본 영상이 있으면 영상 (2026-11-27 사용자)"),
                         ("bignum", "숫자 하나로 줄이면 주장이 아니라 결과만 남음 (2026-11-27 사용자)"),
                         ("bars", "그래프는 주장을 들은 뒤 의문이 생긴 곳에서 — 먼저 그 사람의 말 (2026-11-27 사용자)"),
                         ("motionboard", "설명 무대가 먼저 오면 내레이션이 주장을 대신 요약하게 됨 (2026-11-27 사용자)"),
                         ("checklist", "목록으로 줄이면 논리의 흐름이 끊김"), ("versus", "맞대기는 두 사람의 말을 들은 뒤에"),
                         ("share", "몫 나누기는 설명 장면 — 주장은 본인 말로"), ("kinetic", "큰 글자 연출은 쓰지 않음 (2026-11-27 사용자)"),
                         ("footage", "말 없이 화면만 깔면 판단의 주인이 흐려짐")):
            if not any(o.get("id") == alt for o in ov):
                ov.append({"id": alt, "why_not": why})

# id·장 번호 다시 매김, cuts.json·footage
foot = dict(v1["footage"])
cuts_out = {}
for k, s in enumerate(scenes, 1):
    s["id"] = k
    if s["type"] == "bite":
        src = s["clip"]["src"]
        f = copy.deepcopy(t2["footage"][src])
        foot[src] = f
        if src.startswith("cwL"):
            s["clip"].update(CNBC)
        cuts_out[str(k)] = s.pop("_segs")
v2 = copy.deepcopy(v1)
v2["scenes"] = scenes
v2["footage"] = foot
v2["_v2"] = True
v2["direction"]["vocabulary"] = [x for x in v2["direction"]["vocabulary"] if x not in ("kinetic", "quote")]
v2["direction"]["intent"] = "시청자는 다모다란과 우드의 주장을 본인 목소리로 듣고, 지금 주가가 깔고 있는 매출(약 1조 770억)과 그 민감도(절반이면 3분의 1)를 들고 간다"
v2["core_message"] = ("가치평가 교수 다모다란은 앤트로픽 값(주당 76달러 남짓)이 '10년 뒤 매출 1조 달러'에 걸렸고 그 매출이 안 오면 다 무너진다고 했다. "
                      "그의 평가표를 다시 짜 거꾸로 풀면(가설) 11/25 주가 82.79달러는 2036년 매출 약 1.08조 달러를 깔고 있고, 같은 틀에서 매출만 절반이면 값은 3분의 1 남짓이다(가치의 77%가 10년 뒤). "
                      "약정 9,009억 달러는 안 써도 내는 계약이 많아 매출이 늦으면 먼저 아프다. 캐시 우드는 기업 시장 장악·값 대비 성능 맨 앞을 근거로 더 산다 — 둘은 '비싼 자리가 지켜지나'에서 갈린다.")
pk = v2["package"]
pk["title_options"][2] = "다모다란 vs 캐시 우드 — 앤트로픽, 매출 안 오면 무너지나 더 사나"
pk["title_why"][2] = "인물 대결형 (14 §4 제목 각도)"
pk["tags"] = [t for t in pk["tags"] if t not in ("SK하이닉스", "삼성전자", "HBM", "AI 반도체")] + ["앤트로픽 IPO", "AI 버블"]
pk["hashtags"] = ["다모다란", "앤트로픽", "캐시우드"]
pk["thumbnails"] = [{"id": k, "name": n, "layout": "composite", "file": f"05_edit/thumbnail_{k}.png", "why": [w]} for k, n, w in (
    ("A", "인물 — 다모다란 + '앤트로픽, 매출 안 오면 다 무너진다'", "당사자 얼굴 + 주어+그의 경고"),
    ("B", "인물 — 다모다란 + '앤트로픽 주가 버티려면 매출 1조 달러'", "주어 + 숫자 하나"),
    ("C", "맞대기 — 다모다란 vs 캐시 우드 사진 반반", "두 판단을 한 장에, 각자 주어+주장"))]
pk["thumb_note"] = "2판(11-27): 확정 스타일(Noto Sans KR Black·외곽선 없음·주어+주장 두 줄, 02_script/make_thumbs.py) — 1판은 빨간 꼬리표·이름표 상자·VS·주어 없음"
(P / "02_script" / "hybrid.json").write_text(json.dumps(v2, ensure_ascii=False, indent=1), encoding="utf-8")
(P / "02_script" / "cuts.json").write_text(json.dumps(cuts_out, ensure_ascii=False, indent=1), encoding="utf-8")

# 발언 원본 구간 파일 (받아 둔 원본 전체에서 잘라 냄 — clip-fetch 와 같은 1080p·H.264)
fdir = P / "04_assets" / "footage"
for src, f in foot.items():
    if not (src.startswith("dmdL") or src.startswith("cwL")):
        continue
    out = fdir / f["file"]
    if out.exists():
        continue
    vid = f["url"].split("v=")[-1]
    a, b = sec(f["start"]), sec(f["end"])
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.2f}", "-i", str(SRC[vid]), "-t", f"{b - a:.2f}", "-vf", "scale=-2:min(1080\\,ih)",
                    "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(out)], check=True)
print(len(scenes), "장면 ·", sum(1 for s in scenes if s["type"] == "bite"), "발언 ·",
      round(sum(g["end"] - g["start"] for v in cuts_out.values() for g in v), 1), "초")
