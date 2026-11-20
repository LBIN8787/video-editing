"""이어 읽는 시장 — 11월 19일(목) 아침 브리핑: 엔비디아 실적 다음 날 하락 + 연준 의사록(AI 순환 금융) + 앤트로픽 공모(공급자 7곳 사모) + 한국.
    python scripts/daily_20261119/make.py && python -m ytflow hybrid 20261120-market-deep
"""
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from ytflow.stages import archive  # noqa: E402

P = ROOT / "projects" / "20261120-market-deep"
DS, NP = "dark-doc", "newsprint"
YH = "야후 파이낸스 종가 · 11월 19일(목) 마감 기준 · 18일 대비"
ANT = "앤트로픽 공모가 발표 (2026.11.18) · anthropic.com"
HB = "헌터브룩 미디어 보고서 (2026.11.19) · hntrbrk.com"

PHOTOS = {
    "nyse": "New York Stock Exchange Facade 2015.jpg",
    "seoul": "Skyline of Yeouido, a prominent finance district in Seoul.jpg",
    "dc": "Microsoft Data Center Middenmeer, the Netherlands - 1.jpg",
    "racks": "Datacenter Server Racks (22370909788).jpg",
}
KNOWN = {
    "nyse": {"license": "CC BY 2.0", "artist": "작자 미상"},
    "seoul": {"license": "CC BY 4.0", "artist": "작자 미상"},
    "dc": {"license": "CC BY 4.0", "artist": "Hay Kranen"},
    "racks": {"license": "CC BY 2.0", "artist": "작자 미상"},
}


def photos() -> dict:
    fdir = P / "04_assets" / "footage"
    (fdir / "raw").mkdir(parents=True, exist_ok=True)
    out = {}
    for key, title in PHOTOS.items():
        meta = fdir / "raw" / f"{key}.json"
        if meta.exists():
            r = json.loads(meta.read_text(encoding="utf-8"))
        else:
            try:
                r = archive.commons_file(title)
            except Exception:  # noqa: BLE001
                r = None
            if not r:
                k = KNOWN[key]
                r = {"title": title, "license": k["license"], "artist": k["artist"], "page": "https://commons.wikimedia.org/wiki/File:" + title.replace(" ", "_"),
                     "url": "", "credit": f"{k['license']} · {k['artist']} · 위키미디어 공용 · {title.rsplit('.', 1)[0][:50]}"}
            meta.write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
        jpg = fdir / "raw" / f"{key}.jpg"
        if not jpg.exists():
            url = "https://commons.wikimedia.org/wiki/Special:FilePath/" + title.replace(" ", "_") + "?width=1920"
            for _ in range(3):
                subprocess.run(["curl", "-sSL", "-A", "ytflow/1.0 (video research tool)", "-o", str(jpg), url], check=True)
                if jpg.read_bytes()[:2] == b"\xff\xd8":
                    break
                time.sleep(8)
            else:
                jpg.unlink()
                raise SystemExit(f"사진 받기 실패: {title}")
        mp4 = fdir / f"{key}.mp4"
        if not mp4.exists():
            archive.still_to_clip(jpg, mp4, dur=12)
        out[key] = {"file": mp4.name, "credit": r["credit"], "url": r["page"], "license": r["license"]}
    return out


def B(*s):
    return [{"say": x} for x in s]




def M(t, do, **kw):
    return dict(t=t, do=do, **kw)


# 원본 발언 장면(bite) — 2026-11-20 피클이 공식 채널 구간 확인 (inbox/requests/done/20261120-1453-*).
# 클라우드는 유튜브를 못 받으므로 기본은 인용 카드판. PC 에서 원본을 받을 때: python scripts/daily_20261120/make.py --bites
#   → python -m ytflow clip-order / clip-fetch 20261120-market-deep → hybrid (docs/50-clip-lane.md)
BITES = "--bites" in sys.argv
CLIPS = {
    "amodei": {"file": "amodei_nasdaq_20261119.mp4", "url": "https://www.youtube.com/watch?v=FgAtTAgBT2Q", "start": "3:50", "end": "4:05",
               "who": "다리오 아모데이", "credit": "Nasdaq 공식 채널 (YouTube) · 2026.11.19 상장 행사", "license": "인용(20초 이내)"},
    "meeks": {"file": "meeks_cnbc_site_20261119.mp4", "url": "https://www.cnbc.com/video/2026/11/19/anthropics-ipo-should-lift-the-ai-trade-says-paul-meeks.html", "start": "3:16", "end": "3:35",
              "who": "폴 미크스", "credit": "CNBC 공식 영상 · 2026.11.19 Squawk Box", "license": "인용(20초 이내)"},
    "tomlee": {"file": "tomlee_cnbc_site_20261119.mp4", "url": "https://www.cnbc.com/video/2026/11/19/this-is-a-pretty-health-correction-in-tech-says-fundstrats-tom-lee.html", "start": "0:54", "end": "1:13",
               "who": "톰 리", "credit": "CNBC 공식 영상 · 2026.11.19 Closing Bell", "license": "인용(20초 이내)"},
}


def bite(key, chapter, who, role, lead, find, ko, insight=False):
    c = CLIPS[key]
    d = dict(type="bite", chapter=chapter, who=who, role=role, label=f"{c['credit']} · 인용", beats=[{"say": lead}],
             clip={"src": key, "lang": "en", "cuts": [{"find": find, "ko": ko}]})
    if key == "amodei":
        # 나스닥 세로 영상은 발표자의 얼굴과 원본 영어 자막이 보이도록 비율 유지.
        d["clip"]["fit"] = "contain"
        d["show_en"] = False
    else:
        # CNBC 자체 하단 띠와 이름이 겹치지 않게, 이름은 앞 내레이션에서 소개.
        d["show_lower"] = False
        d["label"] = "인용"
    if insight:
        d["insight"] = True
    return d


def main():
    for d in ("01_research", "02_script", "05_edit"):
        (P / d).mkdir(parents=True, exist_ok=True)
    fo = photos()
    cr = {k: v["credit"].split(" · 위키미디어")[0] for k, v in fo.items()}
    S = []
    s = S.append

    # ── 여는 장면 ──
    s(dict(type="bignum", chapter=0, label=ANT + " · 종가는 보도(CNBC·블룸버그 등 일치)", small="앤트로픽 'ANT' 첫날 종가 · 11월 19일 미국 장 마감 기준", value="97.17달러",
           compare={"label": "첫 거래 (미 동부 11시 48분, 보도)", "value": "111.50달러"},
           beats=[{"say": "11월 19일 목요일 미국 장 마감 기준, 클로드를 만드는 AI 회사 앤트로픽이 나스닥 첫날을 97.17달러로 마쳤습니다. 공모가 83달러보다는 17% 높지만, 첫 거래 가격 111.50달러보다는 13% 가까이 낮습니다. 장이 열린 뒤 잠깐 더 오르다가 밀린 하루였습니다.",
                   "motion": [M("13%", "count", id="ant17", value="-12.9%", label="첫 거래 대비 (계산)", x=1660, y=690, w=400, h=140, fs=56)]},
                  {"say": "그런데 같은 날, 미국의 세 지수는 모두 2% 넘게 내렸습니다. 다우는 5만 선 아래로 내려갔습니다. 보도로는 역대 최대 규모의 공모가 마무리된 날, 앤트로픽도 시장도 왜 함께 밀렸을까요?",
                   "motion": [M("다우", "count", id="dji", value="-2.19%", label="다우 (49,097.06)", x=1660, y=860, w=400, h=140, fs=56)]}]))

    # ── 시장 한 장 ──
    s(dict(type="bars", chapter=0, label=YH, title="19일(목) 미국 장 (%)", unit="", emph=0, skin=DS,
           items=[{"label": "반도체 지수", "value": -2.41, "text": "-2.41", "t": "반도체"}, {"label": "나스닥", "value": -2.25, "text": "-2.25", "t": "나스닥은"},
                  {"label": "다우", "value": -2.19, "text": "-2.19", "t": "다우는"}, {"label": "S&P 500", "value": -2.02, "text": "-2.02", "t": "S&P 500"}],
           beats=[{"say": "먼저 시장 한 장입니다. 나스닥은 2.25%, 다우는 2.19%, S&P 500은 2.02% 내렸습니다. 반도체 지수는 2.41% 빠졌습니다."},
                  {"say": "한 업종의 일이 아니었습니다. 미국 업종 11개 가운데 9개가 내렸고, AI와 거리가 먼 헬스케어도 2% 넘게 빠졌습니다. 공포 지수라 불리는 변동성 지수는 28.44로 16% 가까이 뛰었습니다.",
                   "motion": [M("11개", "count", id="sec", value="9 / 11", label="내린 업종", x=1800, y=560, w=230, h=140, fs=46),
                              M("변동성", "count", id="vix", value="28.44", label="VIX", x=1800, y=740, w=230, h=140, fs=46)]},
                  {"say": "나스닥은 최근 한 달 가장 높았던 10월 21일 종가보다 10.6% 낮아졌습니다. 흔히 조정이라고 부르는 10% 선을 넘은 겁니다.",
                   "motion": [M("10.6%", "count", id="ixic", value="-10.6%", label="나스닥 · 한 달", x=1800, y=380, w=230, h=140, fs=42)]}]))

    # ── 1. 한 달 사이 바뀐 시장 ──
    s(dict(type="chapter", chapter=1, num="1", title="한 달 사이, 갈라진 AI", icon="trending-down", look="board",
           beats=B("하루만 보면 놓치는 것이 있습니다. 한 달 전으로 돌아가 보겠습니다.")))
    s(dict(type="bars", chapter=1, label="야후 파이낸스 종가 · 10월 21일 → 11월 19일 · 등락률은 이 영상의 계산", title="한 달 사이 (%)", unit="", emph=0, skin=DS,
           items=[{"label": "엔비디아", "value": -34.2, "text": "-34.2", "t": "엔비디아는"}, {"label": "마이크론", "value": -24.4, "text": "-24.4", "t": "마이크론"},
                  {"label": "반도체 지수", "value": -18.1, "text": "-18.1", "t": "반도체 지수"}, {"label": "AMD", "value": -11.5, "text": "-11.5", "t": "AMD는"},
                  {"label": "나스닥", "value": -10.6, "text": "-10.6", "t": "나스닥"}, {"label": "브로드컴", "value": 2.6, "text": "+2.6", "t": "브로드컴은"}],
           beats=[{"say": "나스닥이 최근 가장 높았던 10월 21일부터 19일까지, 한 달의 성적입니다. 엔비디아는 34.2% 빠졌습니다. 메모리의 마이크론은 24.4%, 반도체 지수는 18.1% 내렸습니다.", "motion": [M("34.2%", "count", id="nv1m", value="221.97 → 145.98", label="엔비디아 (달러)", x=1800, y=440, w=230, h=170, fs=30)]},
                  {"say": "그런데 AMD는 11.5%로 덜 빠졌고, 나스닥은 10.6% 내렸습니다. 앤트로픽에 칩을 대는 브로드컴은 오히려 2.6% 올랐습니다. 같은 AI 안에서도 길이 갈라진 겁니다.",
                   "motion": [M("2.6%", "count", id="avgo1m", value="+2.6%", label="브로드컴 · 한 달", x=1800, y=660, w=230, h=150, fs=44)]}]))
    s(dict(type="checklist", chapter=1, label="11/15~11/19 회차 팩트시트(상무부 규칙·엔비디아 8-K·연준 의사록·앤트로픽 발표) · 지수는 야후 파이낸스", title="그 한 달에 있었던 일", x=150, text_w=900, skin=NP,
           rows=[{"label": "엔비디아 젠슨 황 사임 — 리더십 질문", "state": "warn", "t": "사임"},
                 {"label": "11월 16일 상무부 원격 접근 규칙 — 19일 효력", "state": "warn", "t": "규칙"},
                 {"label": "11월 18일 연준 의사록 — 추가 인상·'AI 순환 금융'", "state": "warn", "t": "의사록"},
                 {"label": "11월 19일 앤트로픽 상장 · AMD 보고서", "state": "warn", "t": "상장"}],
           beats=[{"say": "그 한 달 동안 무슨 일이 있었는지 이 채널이 차례로 다뤘습니다. 엔비디아의 젠슨 황이 물러나며 리더십 질문이 생겼고, 미국 상무부는 중국이 AI 칩을 빌려 쓰는 길까지 막는 규칙을 냈습니다. 그 규칙이 효력을 가진 날이 바로 19일입니다.", "upto": 2},
                  {"say": "18일에는 연준 의사록이 금리를 더 올릴 수 있다는 뜻과 AI 회사들 사이의 순환 금융을 함께 적었습니다. 그리고 19일, 앤트로픽이 상장했고 AMD 보고서가 나왔습니다. 공포 지수는 한 달 전 16.68에서 28.44로 70% 뛰었습니다.", "upto": 4,
                   "motion": [M("28.44", "count", id="vix1m", value="16.68 → 28.44", label="VIX · 한 달", x=1440, y=820, w=480, h=160, fs=48)]}]))
    s(dict(type="map_causal", chapter=1, look="board", label="자체 해석 · 근거: 야후 파이낸스 한 달 종가(엔비디아·AMD·브로드컴·헬스케어), 지난 회차 팩트시트",
           map={"nodes": {"q": {"label": "질문을 먼저 받은 곳: 엔비디아 -34%", "icon": "circle-alert", "x": 960, "y": 260},
                          "alt": {"label": "'대안': AMD -11% · 브로드컴 +3%", "icon": "shuffle", "x": 400, "y": 600},
                          "d19": {"label": "19일: 대안에도 질문 · 새 주식 1,070억", "icon": "calendar", "x": 1520, "y": 600},
                          "all": {"label": "시장 전체로 (헬스케어 한 달 -0.8% → 하루 -2%)", "icon": "trending-down", "x": 960, "y": 880}},
                "edges": [["q", "alt"], ["alt", "d19"], ["d19", "all"]]},
           beats=[{"say": "여기서부터는 해석입니다. 지난 한 달, 돈은 AI를 통째로 버리지 않았습니다. 질문을 먼저 받은 엔비디아와 그 공급망에서 빠져, 대안으로 여겨진 AMD와 브로드컴 쪽으로 옮겨 갔습니다.",
                   "reveal": ["q", "alt"], "draw": [["q", "alt"]], "active": "alt"},
                  {"say": "19일은 그 흐름이 두 군데서 흔들린 날입니다. 대안이던 AMD에도 질문이 붙었고, 새 주식 1,070억 달러어치가 자리를 요구했습니다. 그리고 한 달 내내 0.8%밖에 안 빠졌던 헬스케어까지 이날은 2% 넘게 내렸습니다. 반도체의 일이 시장 전체로 번진 날입니다.",
                   "reveal": ["d19", "all"], "draw": [["alt", "d19"], ["d19", "all"]], "active": "all"}]))

    # ── 2. 앤트로픽과 대리주 ──
    s(dict(type="chapter", chapter=2, num="2", title="정품이 진열된 날", icon="store", look="photo", bg_src="nyse",
           beats=B("먼저 앤트로픽의 첫날을 시간 순서대로 보겠습니다.")))
    s(dict(type="checklist", chapter=2, label=ANT + " · 첫 거래 시각·가격은 보도(스톡타이탄·패스트컴퍼니) · 한국 시간 환산은 이 영상", title="앤트로픽 첫날 (미국 동부 시각)", x=150, text_w=880, skin=NP,
           rows=[{"label": "공모 9억 8천만 주 · 주당 83달러 (회사 발표)", "state": "ok", "t": "9억 8천만"},
                 {"label": "11시 48분 첫 거래 111.50달러 (+34%)", "state": "ok", "t": "111.50"},
                 {"label": "장중 최고 114.99 · 최저 92.72", "state": "warn", "t": "최고"},
                 {"label": "종가 97.17달러 (+17%)", "state": "ok", "t": "97.17"}],
           beats=[{"say": "회사 발표에 따르면 앤트로픽은 9억 8천만 주를 주당 83달러에 팔았습니다. 첫 거래는 미국 동부 시각 오전 11시 48분, 111.50달러였습니다. 공모가보다 34% 높게 시작한 겁니다.", "upto": 2},
                  {"say": "장중 한때 114.99달러까지 올랐다가 92.72달러까지 밀렸고, 97.17달러에 마쳤습니다. 가장 높았던 값보다는 15% 넘게, 첫 거래 가격보다는 13% 가까이 내려온 종가입니다. 보도된 시가총액은 약 1조 7,700억 달러입니다.", "upto": 4,
                   "motion": [M("1조 7,700억", "count", id="mcap", value="약 1.77조 달러", label="시가총액 (보도)", x=1440, y=820, w=480, h=170, fs=56)]}]))
    if BITES:
        s(bite("amodei", 2, "다리오 아모데이", "앤트로픽 CEO · 11월 19일 나스닥 상장 행사", "상장 종이 울리기 전, 다리오 아모데이 대표는 나스닥 단상에서 이렇게 말했습니다.",
               "And to state it unequivocally, we will pace the training and deployment of AI systems, taking as long as is necessary to have confidence that they are safe and will remain under human control. We will not bend to either business nor political pressure.",
               "분명히 말씀드립니다. 우리는 AI가 안전하고 사람의 통제 아래 있다고 확신할 때까지, 필요한 만큼 시간을 들여 훈련과 배포의 속도를 조절하겠습니다. 사업의 압력에도 정치의 압력에도 굽히지 않겠습니다."))
    s(dict(type="bars", chapter=2, label=YH + " · '대리주' 표현은 CNBC(스톡타이탄 인용)", title="같은 날, 앤트로픽과 '대리주'들 (%)", unit="", emph=0, skin=DS,
           items=[{"label": "앤트로픽 (공모가 대비)", "value": 17.1, "text": "+17.1", "t": "공모가로"}, {"label": "앤트로픽 (첫 거래 대비)", "value": -12.9, "text": "-12.9", "t": "첫 거래 값에"}, {"label": "브로드컴", "value": -2.09, "text": "-2.09", "t": "브로드컴"},
                  {"label": "알파벳", "value": -3.46, "text": "-3.46", "t": "알파벳"}, {"label": "아마존", "value": -3.87, "text": "-3.87", "t": "아마존은"}],
           beats=[{"say": "그런데 미국 방송 CNBC가 앤트로픽의 대리주라고 부른 회사들이 있습니다. 앤트로픽 지분을 크게 가진 아마존과 알파벳, 앤트로픽에 칩을 대는 브로드컴입니다. 상장 전에는 앤트로픽을 직접 살 수 없으니, 이 회사들을 대신 샀다는 뜻입니다. 이건 매체의 표현이고, 실제로 누가 왜 샀는지는 확인된 사실이 아닙니다."},
                  {"say": "앤트로픽 자신부터 보면, 공모가로 주식을 받은 사람에게는 17% 이익이었지만, 장에서 첫 거래 값에 산 사람에게는 13% 가까운 손실이었습니다. 그리고 이 세 회사도 모두 내렸습니다. 아마존 3.87%, 알파벳 3.46%, 브로드컴 2.09%입니다. 알파벳은 오전 한때 4% 넘게 올랐다가 방향을 바꿨습니다. 하루 전만 해도 아마존은 3.82% 올랐던 회사입니다.",
                   "motion": [M("4%", "count", id="goog", value="+4.04% → -3.46%", label="알파벳 장중→종가", x=1800, y=420, w=230, h=190, fs=30)]}]))
    s(dict(type="analogy", chapter=2, label="비유 · 이 영상의 설명", title="정품이 진열되면",
           left={"icon": "package", "label": "정품이 없을 땐 비슷한 물건을", "sub": "아마존·알파벳·브로드컴"}, right={"icon": "store", "label": "정품이 진열되자 정품으로", "sub": "앤트로픽 직접 매수"},
           result={"icon": "wallet", "label": "지갑은 하나 — 대체품을 내놓고 정품을 산다"},
           beats=[{"say": "이렇게 비유할 수 있습니다. 갖고 싶은 정품이 가게에 없을 때, 사람들은 비슷한 물건을 대신 삽니다. 그러다 정품이 진열되면, 대신 샀던 물건을 내놓고 정품을 사러 갑니다."},
                  {"say": "지갑은 하나입니다. 정품 가게 앞 줄이 길어진 만큼, 대체품 가게는 한산해집니다. 19일의 시세가 이 모양과 닮았습니다.", "show_result": True}]))
    s(dict(type="bignum", chapter=2, label=ANT + " · 동시 사모 260억은 앤트로픽 S-1/A 2차 · 합계·배수는 이 영상의 계산", small="19일 한꺼번에 나온 새 주식 (공모 + 동시 사모)", value="약 1,070억 달러",
           compare={"label": "앤트로픽의 12개월 컴퓨트 약속", "value": "707억 달러"},
           beats=[{"say": "숫자로 보면 더 분명합니다. 공모 9억 8천만 주에 83달러를 곱하면 813억 달러입니다. 여기에 지난 회차에서 본 공급자 일곱 곳의 동시 사모 260억 달러를 더하면, 약 1,070억 달러어치 새 주식이 한꺼번에 나왔습니다.",
                   "motion": [M("813억", "count", id="ipo", value="813억 + 260억", label="공모 + 동시 사모 (계산)", x=1600, y=300, w=440, h=130, fs=44)]},
                  {"say": "이 가운데 기존 주주 몫을 빼고 앤트로픽이 받는 돈은 수수료 전 약 1,054억 달러입니다. 앞으로 12개월 안에 내기로 한 컴퓨트 약속 707억 달러의 약 1.5배입니다. 지난 회차 마지막에 물었던 질문, 이 고리를 돌게 하는 돈은 누가 내느냐에 대한 첫 답이 나온 셈입니다. 새 주주들입니다.",
                   "motion": [M("1.5배", "count", id="x15", value="약 1.5배", label="받는 돈 ÷ 12개월 약속 (계산)", x=1600, y=860, w=440, h=140, fs=56)]}]))
    s(dict(type="bignum", chapter=2, label="시가총액은 보도 · 매출은 앤트로픽 S-1/A(1~9월 332억) · 연 환산·배수는 이 영상의 계산", small="앤트로픽 시가총액 ÷ 연 환산 매출", value="약 40배",
           compare={"label": "12개월 안 컴퓨트 약속", "value": "707억 달러"},
           beats=[{"say": "이제 값을 보겠습니다. 보도된 시가총액 1조 7,700억 달러를, 올해 1월부터 9월까지 매출 332억 달러를 1년으로 늘린 약 443억 달러로 나누면, 약 40배입니다. 연 환산 매출의 약 40배를 매긴 겁니다.", "motion": [M("1조 7,700억", "count", id="mc2", value="약 1.77조 달러", label="시가총액 (보도)", x=1600, y=300, w=440, h=130, fs=48)]},
                  {"say": "이 값을 받치려면 매출이 계속 빠르게 커져야 합니다. 앤트로픽은 앞으로 12개월 안에만 707억 달러어치 컴퓨트를 사기로 약속했고, 이번에 받은 돈으로 그 1년 치는 채웠습니다. 다음 1년부터는 매출이 그 몫을 해야 합니다.",
                   "motion": [M("443억", "count", id="ann", value="약 443억 달러", label="연 환산 매출 (계산)", x=1600, y=860, w=440, h=140, fs=50)]}]))
    s(dict(type="map_causal", chapter=2, look="board", label="자체 해석 · 근거: 앤트로픽 공모 발표·S-1/A, 야후 파이낸스 종가, CNBC '대리주' 표현, 섹터 ETF",
           map={"nodes": {"new": {"label": "새 주식 약 1,070억 달러", "icon": "banknote", "x": 960, "y": 260},
                          "proxy": {"label": "대리주: 아마존·알파벳·브로드컴 ↓", "icon": "trending-down", "x": 400, "y": 600},
                          "ant": {"label": "앤트로픽: 공모가 +17% · 첫 거래 -13%", "icon": "trending-up", "x": 1520, "y": 600},
                          "other": {"label": "AI 밖 업종도 ↓ (헬스케어 -2.05%)", "icon": "circle-alert", "x": 960, "y": 880}},
                "edges": [["new", "proxy"], ["new", "ant"], ["proxy", "other"]]},
           beats=[{"say": "여기서부터는 해석입니다. 새 주식 1,070억 달러어치를 사려면, 누군가는 다른 주식을 팔아야 합니다. 앤트로픽 대신 들고 있던 대리주가 팔렸고, 그 돈이 새 주식으로 옮겨 갔습니다. 다만 그 앤트로픽마저 첫 거래 뒤 잠깐 오른 다음 밀렸습니다. 돈이 실제로 이렇게 옮겨 갔는지는 확인된 사실이 아니라, 시세가 보여 주는 모양에 대한 해석입니다. 새 주식이 한꺼번에 많이 나오자, 대체품도 정품도 함께 값이 눌린 하루입니다.",
                   "reveal": ["new", "proxy", "ant"], "draw": [["new", "proxy"], ["new", "ant"]], "active": "new"},
                  {"say": "다만 이것만으로 세 지수의 2% 하락을 다 설명할 수는 없습니다. AI와 거리가 먼 헬스케어와 소재 업종도 2% 넘게 내렸습니다. 공모는 하락의 한 갈래이지, 유일한 이유라고 단정하지 않겠습니다.",
                   "reveal": ["other"], "draw": [["proxy", "other"]], "active": "other"}]))

    # ── 2. AMD ──
    s(dict(type="chapter", chapter=3, num="3", title="'승자'에게 온 질문", icon="circle-help", look="photo", bg_src="dc",
           beats=B("같은 날 반도체에서 가장 크게 빠진 회사는 AMD입니다.")))
    s(dict(type="bars", chapter=3, label=YH + " · 18일은 17일 대비", title="AMD 이틀 (%)", unit="", emph=1, skin=DS,
           items=[{"label": "18일 (수)", "value": 5.31, "text": "+5.31", "t": "18일"}, {"label": "19일 (목)", "value": -7.72, "text": "-7.72", "t": "19일"}],
           beats=[{"say": "AMD는 엔비디아의 경쟁사입니다. 엔비디아가 대표 사임과 중국 문제로 흔들리는 동안, AMD는 그 빈자리를 가져갈 회사로 여겨졌습니다. 18일에도 5.31% 올랐습니다."},
                  {"say": "그런데 19일, AMD는 7.72% 내린 489.19달러에 마쳤습니다. 이틀을 합치면 오히려 2.82% 내린 셈입니다. 하루 사이에 무슨 일이 있었을까요?",
                   "motion": [M("489.19", "count", id="amd", value="489.19달러", label="AMD 19일 종가", x=1440, y=760, w=440, h=150, fs=52)]}]))
    s(dict(type="quote", chapter=3, insight=True, label=HB + " · 헌터브룩 캐피털은 AMD 공매도 포지션 보유(보고서 공시) · 의견이며 사실이 아닙니다", who="헌터브룩 미디어", role="조사 보고서 'AMD Has Its Own China Problem' · 11.19",
           quote="AMD는 정말 엔비디아보다 안전한 대안일까?", keyword="안전한 대안",
           orig="Is AMD really a safer alternative to Nvidia?",
           beats=[{"say": "이날 미국 동부 시각 오전 10시 27분, 조사 매체 헌터브룩이 보고서를 냈습니다. 제목은 AMD에게도 중국 문제가 있다. 첫 질문은 이렇습니다. AMD는 정말 엔비디아보다 안전한 대안일까?", "motion": [M("10시 27분", "count", id="hbt", value="10:27", label="보고서 공개 (미 동부)", x=1500, y=860, w=400, h=140, fs=52)]},
                  {"say": "중요한 점이 하나 있습니다. 같은 보고서에, 계열사인 헌터브룩 캐피털이 AMD 주가가 내리는 쪽에 돈을 걸었다는 공시가 적혀 있습니다. 공매도 포지션을 가진 쪽의 주장이라는 겁니다."}]))
    s(dict(type="checklist", chapter=3, label=HB + " · 보고서의 주장이며 당국 확인 없음 · 로이터·CNBC 독자 확인 못 함", title="보고서의 주장 (확인되지 않음)", x=150, text_w=900, skin=NP,
           rows=[{"label": "2025년 3월 미 상무부 거래 제한 명단에 오른 중국 서버 회사 IEIT", "state": "ok", "t": "IEIT"},
                 {"label": "그 뒤 AMD 펌웨어 새 버전 6개 이상을 제품에 넣음 (최신 10월 19일)", "state": "warn", "t": "6개"},
                 {"label": "IEIT와 이어진 세 회사 펌웨어가 99.94% 같음", "state": "warn", "t": "99.94%"},
                 {"label": "AMD 매출 22.4%가 중국·홍콩 (2025 회계연도)", "state": "warn", "t": "22.4%"}],
           beats=[{"say": "보고서의 주장은 이렇습니다. 미국 상무부는 2025년 3월, 중국 서버 회사 IEIT를 거래 제한 명단에 올렸습니다. 그런데 그 뒤에도 IEIT가 AMD의 펌웨어, 그러니까 칩을 움직이는 기본 소프트웨어의 새 버전을 적어도 여섯 번 자기 제품에 넣었다는 겁니다.", "upto": 2},
                  {"say": "IEIT와 이어진 세 회사의 펌웨어도 99.94% 같았다고 적었고, AMD 매출의 22.4%가 중국과 홍콩에 청구됐다고 짚었습니다. 다만 이것은 보고서의 주장입니다. 로이터와 CNBC는 독자적으로 확인하지 못했다고 밝혔고, 당국의 조치는 아직 없습니다.", "upto": 4,
                   "motion": [M("22.4%", "count", id="cn", value="22.4%", label="중국·홍콩 매출 비중 (보고서 인용)", x=1440, y=820, w=480, h=160, fs=56)]}]))
    s(dict(type="checklist", chapter=3, label=HB + " · 보고서 본문에 적힌 문장 요약", title="보고서가 스스로 적은 한계", x=150, text_w=900, skin=NP,
           rows=[{"label": "돈이 오간 것만으로 AMD의 위반이 입증되지 않는다", "state": "ok", "t": "입증되지"},
                 {"label": "IEIT가 코드를 어떻게 얻었는지, 허가가 있었는지 모른다", "state": "ok", "t": "허가"},
                 {"label": "통관 기록은 서버 속 칩의 주인·행선지를 보여 주지 않는다", "state": "ok", "t": "통관"},
                 {"label": "이 관계들은 AMD 전체 사업에 비해 '비교적 작다'", "state": "ok", "t": "작다"}],
           beats=[{"say": "그런데 이 보고서에는 시장이 덜 주목한 문장들이 있습니다. 보고서 스스로, 돈이 오간 것만으로 AMD가 수출 통제를 어겼다고 입증되지는 않는다고 적었습니다. IEIT가 AMD의 코드를 어떻게 얻었는지, 누가 허가를 받았는지도 모른다고 썼습니다.", "upto": 2},
                  {"say": "통관 기록은 서버 안에 누구의 칩이 들어갔는지, 완성된 서버가 어디로 갔는지 보여 주지 않는다는 점, 그리고 이런 관계가 AMD 전체 사업에 비하면 비교적 작다는 점도 적었습니다. 주가 7.72%가 빠진 보고서가, 스스로는 위반을 단정하지 않은 겁니다.", "upto": 4}]))
    s(dict(type="checklist", chapter=3, label=HB + " · 퉁푸 합작사·싱가포르 매출은 보고서가 AMD 공시를 인용 · 5개국 규칙은 미 상무부(11/17 회차) · 두 번째 보고서(헌터브룩·베어 케이브)는 출처 표시 없는 숫자 많음", title="시장이 값을 매긴 것 — 위반보다 '노출'", x=150, text_w=920, skin=NP,
           rows=[{"label": "매출: 중국·홍콩 22.4% · 싱가포르 12.4% (2025)", "state": "warn", "t": "싱가포르"},
                 {"label": "칩 마무리 대부분: 중국 퉁푸 합작사 (퉁푸 85%·AMD 15%)", "state": "warn", "t": "퉁푸"},
                 {"label": "19일 효력: 싱가포르 등 5개국에 AI 칩·서버 허가 필요", "state": "warn", "t": "5개국"},
                 {"label": "두 번째 보고서: 구매 약속 122억 → 488억 달러 (주장)", "state": "warn", "t": "488억"}],
           beats=[{"say": "그렇다면 시장은 무엇에 값을 매겼을까요. 보고서가 AMD 공시를 인용해 짚은 숫자들입니다. 매출의 22.4%가 중국과 홍콩, 12.4%가 싱가포르에 청구됐습니다. 그리고 칩을 마무리하는 조립과 검사의 대부분을, 중국 퉁푸와 만든 합작사가 맡고 있습니다.", "upto": 2},
                  {"say": "바로 같은 19일, 싱가포르와 말레이시아 등 다섯 나라에 AI 칩과 서버를 보내려면 허가를 받도록 한 상무부 규칙이 효력을 가졌습니다. 같은 날 나온 두 번째 보고서는 AMD의 구매 약속이 작년 말 122억에서 9월 488억 달러로 늘었다고 주장했습니다. 다만 이 보고서의 숫자 상당수에는 출처가 붙어 있지 않습니다.", "upto": 4,
                   "motion": [M("12.4%", "count", id="sg", value="22.4% + 12.4%", label="중국·홍콩 + 싱가포르 매출 (보고서 인용)", x=1440, y=820, w=480, h=160, fs=44)]}]))
    s(dict(type="quote", chapter=3, insight=True, label=HB + " 인터뷰 인용 · 의견이며 사실이 아닙니다", who="윌리엄 라인시", role="전 미 상무부 수출관리 차관 · CSIS 선임 고문",
           quote="허가가 필요하다는 것이, 곧 허가가 거절된다는 뜻은 아니다.", keyword="거절",
           orig="The fact that you have to get a license does not mean automatically that the license will be denied.",
           beats=[{"say": "보고서 안에도 엇갈린 시각이 함께 실렸습니다. 미국 상무부에서 수출 관리를 맡았던 윌리엄 라인시는, 소프트웨어 이전은 하드웨어보다 단속하기가 훨씬 어렵다고 말했습니다. 동시에, 허가가 필요하다는 것이 곧 거절된다는 뜻은 아니라고 했습니다. 사실이 아니라 한 사람의 시각입니다."},
                  {"say": "반면 카네기 국제평화재단의 샘 윈터-레비는, 이번이 진짜 전환점일 것 같다며 누구에게나 팔던 시대가 끝나 가고 있다고 봤습니다. 위반이냐 아니냐는 아직 모릅니다. 하지만 미국 칩 회사의 중국 노출에 매겨지는 값이 바뀌고 있다는 데에는, 이 두 사람의 말과 19일의 주가가 같은 쪽을 가리킵니다."}]))
    s(dict(type="versus", chapter=3, insight=True, label=HB + " · AMD 답변은 로이터 인용 보도 · 의견이며 사실이 아닙니다",
           left={"value": "주장", "label": "헌터브룩: 명단 뒤에도 펌웨어가 갔다", "icon": "file-text"},
           right={"value": "부인", "label": "AMD: 사업 관행을 왜곡했다", "icon": "shield"},
           beats=[{"say": "AMD는 로이터에, 이 주장은 AMD의 사업 관행과 관계를 왜곡한 것이며 회사는 수출 통제법을 지킨다고 답했습니다. 반면 보고서에는, AMD가 자기들의 질문에 답하지 않았다고 적혀 있습니다."},
                  {"say": "어느 쪽이 맞는지는 아직 모릅니다. 확실한 건 시장이 반응한 방식입니다. 엔비디아에게 던져졌던 중국 질문이, 이제 경쟁사에게도 던져질 수 있다는 것. 하루 전의 기대 5%가 그 질문 하나에 사라졌습니다. 그리고 AMD는 앤트로픽의 동시 사모에 약 25억 달러를 넣기로 한 회사이기도 합니다.", "motion": [M("25억", "count", id="amdpp", value="약 25억 달러", label="AMD · 앤트로픽 사모 (S-1/A)", x=960, y=880, w=460, h=140, fs=52)]}]))

    # ── 3. 엇갈린 시각 ──
    s(dict(type="chapter", chapter=4, num="4", title="같은 날, 두 가지 읽기", icon="message-circle", look="board",
           beats=B("이 하루를 이름난 투자자들은 어떻게 읽었을까요?")))
    s(dict(type="quote", chapter=4, insight=True, label="본인 X 게시물 (2026.11.19) · 야후 파이낸스 인용 · 의견이며 사실이 아닙니다", who="모하메드 엘에리언", role="경제학자 · 알리안츠 수석 경제 고문",
           quote="이건 AI의 약속만의 문제가 아니라, AI를 위해 자리를 만드는 문제다.", keyword="자리를",
           orig="remember this isn't just about the promise of AI, but about making room for it",
           beats=[{"say": "경제학자 모하메드 엘에리언은 자기 계정에 이렇게 적었습니다. 이건 AI의 약속만의 문제가 아니라, AI를 위해 자리를 만드는 문제라는 겁니다. 큰 공모를 사려면 다른 걸 팔아야 한다는 뜻입니다. 사실이 아니라 한 사람의 시각입니다."},
                  {"say": "채권 시장에서도 큰 발행이 한꺼번에 나오면, 사려는 돈이 그대로인 한 다른 채권값이 눌립니다. 이 시각을 받치는 숫자는 대리주의 하락입니다. 어긋나는 숫자는, AI와 상관없는 업종도 함께 내렸다는 점입니다."}]))
    s(dict(type="versus", chapter=4, insight=True, label="본인 X 게시물 (2026.11.19) · 야후 파이낸스 인용 · 의견이며 사실이 아닙니다",
           left={"value": "자리", "label": "엘에리언: 공모를 위해 자리를 만든 것", "icon": "move"},
           right={"value": "쏠림", "label": "먼스터: AI에 대한 판결이 아니다", "icon": "users"},
           beats=[{"say": "딥워터 자산운용의 진 먼스터는 조금 다르게 봤습니다. 상장이 AI 주식 전체를 띄울 거라는 기대가 전형적인 집단 사고였고, 오늘의 하락은 AI에 대한 판결이 아니라는 겁니다. 다들 같은 쪽에 서 있었다는 뜻입니다."},
                  {"say": "이 시각을 받치는 숫자는 앤트로픽이 공모가보다 17% 높게 마쳤다는 점입니다. 어긋나는 숫자는 그 앤트로픽도 첫 거래보다 13% 가까이 내렸고, 나스닥은 한 달 사이 10% 넘게 빠졌다는 점입니다. 국내 매체는 상장이 매도 신호였느냐고 물었고, 해외 매체는 자리 만들기라는 말을 제목에 올렸습니다.", "motion": [M("10%", "count", id="ix10", value="-10.6%", label="나스닥 · 한 달 최고 대비", x=960, y=880, w=460, h=140, fs=52)]}]))

    if BITES:
        s(bite("meeks", 4, "폴 미크스", "프리덤 캐피털 마켓 기술 리서치 책임자 · CNBC 19일 장 전", "상장 전 기대부터 들어 보겠습니다. 19일 장 전, 프리덤 캐피털 마켓의 폴 미크스입니다.",
               "So I would expect that you get some sort of relief rally in all these stocks based on this IPO, and I expect it to be up modestly. I don't think that we will push by the end of trading day one, a $2 trillion market cap,",
               "이번 상장으로 이 종목들 전반에 일종의 안도 랠리가 올 거라 봅니다. 상장 첫날은 적당히 오를 것이고, 첫날 마감까지 시가총액 2조 달러에 닿지는 않을 겁니다.", insight=True))
    s(dict(type="versus", chapter=4, insight=True, label="CNBC 인터뷰(미크스·19일 장 전) · 디트릭 발언 — 야후 파이낸스(스톡트위츠) 인용 · 의견이며 사실이 아닙니다",
           left={"value": "안도", "label": "미크스: 장 전 '안도 랠리'", "icon": "trending-up"},
           right={"value": "조정", "label": "디트릭: 급등 뒤 조정도 흔해", "icon": "trending-down"},
           beats=[{"say": "상장 전 기대도 엇갈렸습니다. 프리덤 캐피털 마켓의 기술 리서치 책임자 폴 미크스는 19일 장 전 미국 방송 인터뷰에서, 이 공모가 AI 주식 전체에 안도 랠리를 불러올 것이고 첫날은 적당히 오를 것이라고 봤습니다. 시가총액 2조 달러까지는 못 갈 거라고도 했습니다.", "motion": [M("2조", "count", id="mk2e", value="2조 달러 미만", label="미크스의 첫날 예상", x=590, y=860, w=460, h=140, fs=48)]},
                  {"say": "카슨 그룹의 라이언 디트릭은 과거 대형 상장을 보면 첫날 급등은 흔하지만, 그다음 1년 안에 큰 조정이 오는 것도 흔했다고 짚었습니다. 결과는 반반이었습니다. 앤트로픽은 공모가보다 높게 마쳤고 2조 달러에는 못 미쳤지만, 기대했던 AI 주식 전체의 안도 랠리는 오지 않았습니다. 둘 다 사실이 아니라 한 사람의 시각입니다.",
                   "motion": [M("2조", "count", id="mk2t", value="약 1.77조 달러", label="첫날 시가총액 (보도)", x=1330, y=860, w=460, h=140, fs=48)]}]))
    if BITES:
        s(bite("tomlee", 4, "톰 리", "펀드스트랫 · CNBC 19일 클로징 벨", "장이 끝난 뒤, 펀드스트랫의 톰 리는 이렇게 말했습니다.",
               "I think that we are at that moment where it feels like max pain. But for the patient investor, this is going to have a big payoff.",
               "지금이 고통이 가장 큰 순간처럼 느껴집니다. 하지만 인내하는 투자자에게는 큰 보상이 될 겁니다.", insight=True))
    s(dict(type="versus", chapter=4, insight=True, label="CNBC 인터뷰(톰 리) · 존슨 발언 — 야후 파이낸스(스톡트위츠, 11.20) 인용 · 의견이며 사실이 아닙니다",
           left={"value": "보상", "label": "톰 리: 인내하면 큰 보상", "icon": "hourglass"},
           right={"value": "종이", "label": "존슨: 쏟아지는 주식도 진짜", "icon": "layers"},
           beats=[{"say": "상장 뒤에도 시각은 갈렸습니다. 펀드스트랫의 톰 리는 미국 방송에서, 지금이 고통이 가장 큰 순간처럼 느껴지지만 인내하는 투자자에게는 큰 보상이 있을 것이라고 말했습니다. 하드웨어는 막아도 소프트웨어는 막기 어렵다는 말도 했습니다."},
                  {"say": "반대로 GLJ 리서치의 고든 존슨은 짧게 말했습니다. AI 혁명은 진짜다, 쏟아지는 종이도 진짜다. 여기서 종이는 새로 찍혀 나오는 주식입니다. 이 시각을 받치는 숫자가 하루에 나온 새 주식 약 1,070억 달러입니다. 어긋나는 숫자는, 그 새 주식을 받은 쪽이 공모가보다 17% 높은 값에 첫날을 마쳤다는 점입니다.",
                   "motion": [M("1,070억", "count", id="paper", value="약 1,070억 달러", label="19일 나온 새 주식 (계산)", x=960, y=860, w=460, h=140, fs=48)]}]))

    # ── 4. 한국 ──
    s(dict(type="chapter", chapter=5, num="5", title="한국은 첫 거래 전에 닫혔다", icon="map-pin", look="photo", bg_src="seoul",
           beats=B("그렇다면 한국 시장은 이 하루를 얼마나 반영했을까요?")))
    s(dict(type="bars", chapter=5, label="코스피 한국거래소 잠정(아시아경제) · 종목 한국거래소 종가(야후) · 19일 마감 기준", title="19일 한국 시장 (%)", unit="", emph=0, skin=DS,
           layers=[{"kind": "locator", "at": [126.92, 37.52], "label": "서울 여의도", "beat": 0, "side": "left", "top": 170, "scale": 2.2}],
           items=[{"label": "셀트리온", "value": 3.61, "text": "+3.61", "t": "셀트리온"}, {"label": "SK하이닉스", "value": 3.41, "text": "+3.41", "t": "SK하이닉스는"},
                  {"label": "코스피", "value": 1.39, "text": "+1.39", "t": "코스피는"}, {"label": "삼성전자", "value": 1.13, "text": "+1.13", "t": "삼성전자는"}],
           beats=[{"say": "11월 19일 한국 장 마감 기준, 코스피는 1.39% 오른 5,137.89였습니다. 장중 한때 5천 선 아래로 내려갔다가 되돌아왔습니다. 보도는 앤트로픽 공모 흥행 기대를 이유로 꼽았습니다.",
                   "motion": [M("5,137.89", "count", id="ks", value="5,137.89", label="코스피 19일 종가", x=290, y=500, w=380, h=130, fs=46)]},
                  {"say": "SK하이닉스는 3.41% 오른 118만 3천 원, 삼성전자는 1.13% 올랐습니다. 다만 외국인은 4천억 원대를 팔아, 닷새 연속 순매도였습니다.",
                   "motion": [M("외국인", "count", id="fx", value="4천억 원대", label="외국인 순매도 · 5일째 (잠정)", x=290, y=650, w=380, h=130, fs=42)]},
                  {"say": "한 달로 넓혀 보면 하루의 반등은 작습니다. 10월 21일부터 코스피는 10.4%, 삼성전자는 11.9%, SK하이닉스는 8.6% 내렸습니다. 나스닥의 10.6%와 거의 같은 폭입니다. 한국 시장은 미국 AI 주식과 같은 길을 걸어 왔습니다.",
                   "motion": [M("10.4%", "count", id="ks1m", value="-10.4%", label="코스피 · 10월 21일 대비 (계산)", x=290, y=800, w=380, h=130, fs=44)]}]))
    s(dict(type="map_causal", chapter=5, look="board", label="자체 해석 · 근거: 한국거래소 마감 시각, 앤트로픽 첫 거래 시각(보도), 야후 파이낸스 종가",
           map={"nodes": {"kr": {"label": "19일 15:30 한국 마감: 기대 (+1.39%)", "icon": "map-pin", "x": 960, "y": 260},
                          "ant": {"label": "20일 01:48 앤트로픽 첫 거래", "icon": "clock", "x": 400, "y": 600},
                          "us": {"label": "미국 -2% · AMD 보고서", "icon": "trending-down", "x": 1520, "y": 600},
                          "today": {"label": "20일 한국 장이 처음 받음", "icon": "calendar", "x": 960, "y": 880}},
                "edges": [["kr", "ant"], ["ant", "today"], ["us", "today"]]},
           beats=[{"say": "여기서부터는 해석입니다. 한국 장은 오후 3시 30분에 닫혔고, 앤트로픽의 첫 거래는 한국 시간 20일 새벽 1시 48분이었습니다. 19일 코스피의 상승은 공모 결과가 아니라 공모에 대한 기대의 값이었습니다.",
                   "reveal": ["kr", "ant"], "draw": [["kr", "ant"]], "active": "kr"},
                  {"say": "미국의 2% 하락과 AMD 보고서는 오늘 20일 한국 장이 처음 받습니다. 이 영상을 만드는 지금 한국 장은 진행 중이라, 오늘 숫자는 마감 뒤에 확인해야 합니다. 한국 메모리는 지난 회차에서 본 것처럼 이 고리에 지분이 아니라 공급으로 걸려 있습니다.",
                   "reveal": ["us", "today"], "draw": [["ant", "today"], ["us", "today"]], "active": "today"}]))

    # ── 5. 볼 것 ──
    s(dict(type="chapter", chapter=6, num="6", title="다음 볼 것", icon="calendar", look="board",
           beats=B("이제 이 해석을 확인할 신호들입니다.")))
    s(dict(type="checklist", chapter=6, label="앤트로픽 발표(공모 마감 20일) · 한국거래소 · 연준 일정(보도) · 투자 권유가 아닙니다", title="일정 (한국 시간)", x=150, text_w=900, skin=NP,
           rows=[{"label": "20일(금) 15:30 · 한국 장 마감 — 5천 선 · 외국인 6일째?", "state": "warn", "t": "마감"},
                 {"label": "20일(금) 밤 · 앤트로픽 둘째 날 — 83달러 위를 지키나", "state": "warn", "t": "둘째"},
                 {"label": "AMD 추가 해명 · 당국 반응", "state": "warn", "t": "AMD"},
                 {"label": "12월 10일(목) 새벽 · 연준 금리 결정", "state": "warn", "t": "12월"}],
           beats=[{"say": "오늘 오후 3시 30분 한국 장 마감에서는 코스피가 5천 선을 지키는지, 외국인 매도가 엿새째 이어지는지를 봅니다. 오늘 밤에는 앤트로픽이 둘째 날에도 공모가 83달러 위를 지키는지, 아마존과 알파벳이 함께 움직이는지가 나옵니다.", "upto": 2},
                  {"say": "AMD가 보고서에 대해 더 자세한 자료를 내는지, 당국이 반응하는지도 지켜볼 대목입니다. 그리고 12월 10일 새벽, 연준의 금리 결정이 있습니다.", "upto": 4}]))
    s(dict(type="checklist", chapter=6, label="팩트시트 '틀리는 경우' · 투자 권유가 아닙니다", title="이 해석이 틀리는 경우", x=150, text_w=920, skin=NP,
           rows=[{"label": "다음 주 대리주가 앤트로픽과 함께 오르면", "state": "warn", "t": "대리주"},
                 {"label": "AMD 반박이 확인되고 당국 조치가 없으면", "state": "warn", "t": "반박"},
                 {"label": "공모 뒤에도 나스닥이 계속 빠지면", "state": "warn", "t": "계속"}],
           beats=[{"say": "이 해석이 틀리는 경우도 적어 둡니다. 다음 주 아마존과 알파벳이 앤트로픽과 함께 오른다면, 대리주에서 빠진 돈은 하루짜리 차익 실현이었던 겁니다.", "upto": 1},
                  {"say": "AMD의 반박이 확인되고 당국이 움직이지 않는다면, 19일 하락은 확인되지 않은 주장에 대한 과한 반응이었던 셈입니다. 그리고 공모가 끝난 뒤에도 나스닥이 계속 빠진다면, 그건 자리 만들기가 아니라 AI에 대한 기대 자체가 식고 있다는 뜻일 수 있습니다.", "upto": 3}]))
    s(dict(type="kinetic", chapter=6, beats=[{"say": "새 주식이 들어설 자리를, 시장 전체가 내줬습니다.", "hit": ["자리를", "전체가"]}]))
    s(dict(type="outro", chapter=6, title="20일 낮까지의 소식", sub="출처는 설명란에", clip={"src": "racks", "start": 0},
           beats=B("딱 하나만 기억한다면 이것입니다. 같은 날, 앤트로픽은 공모가보다 높게 마쳤지만 첫 거래 뒤 잠깐 오른 다음 밀렸고, 앤트로픽을 대신 사던 주식들도 내렸습니다. 새 주식 1,070억 달러가 들어설 자리를 시장이 만든 하루였습니다. 그렇다면 다음에 자리를 내줄 곳은 어디일까요?")))
    for i, x in enumerate(S, 1):
        x["id"] = i
    spec = {
        "title": "앤트로픽 상장 날, 시장은 왜 2% 빠졌나 — AMD 공매도와 한 달의 변화",
        "brand": "market",
        "zoom": "off",
        "core_message": "11월 19일 앤트로픽은 첫 거래 111.50달러(보도)에서 잠깐 오른 뒤 밀려 97.17달러로 첫날을 마쳤고(공모가 83달러보다는 높음), 같은 날 3대 지수는 -2%대(다우 5만 아래)였다. CNBC 가 '앤트로픽 대리주'라 부른 아마존(-3.87%)·알파벳(-3.46%)·브로드컴(-2.09%)이 내렸다 — 새 주식 약 1,070억 달러(공모 813억 + 사모 260억)를 사려고 대신 사던 주식을 판 모양(엘에리언 '자리 만들기'), 다만 AI 밖 업종도 내려 공모 하나로 다 설명되진 않는다. 앤트로픽이 받는 약 1,054억은 12개월 약속 707억의 약 1.5배. 같은 날 AMD 는 공매도 포지션을 가진 헌터브룩의 중국 보고서(미확인, AMD 부인)에 -7.72%. 한국은 첫 거래 전에 닫혀(+1.39%) 20일 장이 처음 반영한다.",
        "question": "앤트로픽 상장 날, 앤트로픽도 첫 값에서 밀리고 시장은 2% 빠졌다. 왜?",
        "logic": ["(심층, 2026-11-20 사용자 요청) 1장 한 달 사이 갈라진 AI: 엔비디아 -34.2 … 브로드컴 +2.6 · 한 달의 사건 · 해석(대안으로 옮긴 돈 → 19일 대안에도 질문·시장 전체로)", "여는 장면: 앤트로픽 97.17(공모가 83, +17%) vs 3대 지수 -2%대·다우 5만 아래 → 질문",
                  "시장 한 장: 반도체 -2.41·나스닥 -2.25·다우 -2.19·S&P -2.02 · 업종 9/11 하락·VIX 28.44 · 나스닥 한 달 최고 대비 -10.6%",
                  "1) 앤트로픽: 첫날 타임라인 → 대리주(아마존·알파벳·브로드컴) 하락 → 비유(정품이 진열되면) → 새 주식 1,070억·받는 돈 1,054억 = 12개월 약속의 1.5배 → 해석(같은 지갑이 옮김, 단 AI 밖 업종도 하락)",
                  "2) AMD: 18일 +5.31 → 19일 -7.72 · 헌터브룩 질문 + 공매도 공시 · 주장 4가지(미확인) · AMD 부인 vs 보고서 '답 안 함' · 사모 25억",
                  "3) 엇갈린 시각: 엘에리언(자리 만들기) vs 먼스터(AI 판결 아님) + 받치는/어긋나는 숫자 · 매체 프레임",
                  "4) 한국: 5,137.89(+1.39)·하이닉스 +3.41·외국인 4천억 원대 5일째 → 해석: 첫 거래 전 마감, 20일 장이 첫 반영",
                  "5) 볼 것 4 · 틀리는 경우 3",
                  "마무리: 돈은 AI를 버리지 않았고 정품 쪽으로 줄을 옮겼다 — 다음에 자리를 내줄 곳은?"],
        "compare_to": [{"value": "앤트로픽 97.17달러", "to": "공모가 83달러 (+17%) · 첫 거래 111.50달러 (-12.9%)"},
                       {"value": "새 주식 약 1,070억 달러", "to": "앤트로픽 12개월 약속 707억"},
                       {"value": "AMD -7.72%", "to": "하루 전 +5.31%"},
                       {"value": "나스닥 23,879.20", "to": "10월 21일 26,702.86 (-10.6%)"},
                       {"value": "코스피 5,137.89", "to": "18일 5,067.44 (+1.39%)"}],
        "analogies": [{"a": "정품이 진열되면", "b": "정품이 없을 땐 비슷한 물건(대리주)을 사다가, 정품(앤트로픽)이 진열되자 대체품을 내놓고 정품을 산다 — 지갑은 하나"},
                      {"a": "채권 시장의 큰 발행", "b": "큰 발행이 한꺼번에 나오면 사려는 돈이 그대로인 한 다른 채권값이 눌린다 (엘에리언)"}],
        "past_cases": [{"case": "과거 해외 대형 공모 8건 — 상장 전 10거래일 코스피 평균 -3.0%, 상장 뒤 20거래일 8건 중 6건 상승 (하장권, 11/19 회차)", "lesson": "공모로 쏠린 돈이 상장 뒤 풀리는지는 다음 주 대리주로 확인"},
                       {"case": "11/15~17 엔비디아 — 중국 관련 질문(지역 매출·원격 접근 규칙)이 회사 하나에서 업종으로 번짐", "lesson": "오늘 같은 질문이 AMD 에 옴 — 주장과 확인을 나눠 봄"}],
        "glossary": [{"term": "공모가", "plain": "상장할 때 새 주주에게 파는 주식 한 주의 값"},
                     {"term": "대리주", "plain": "직접 살 수 없는 회사 대신, 그 회사 지분을 가졌거나 그 회사와 거래하는 상장 회사의 주식"},
                     {"term": "공매도", "plain": "주가가 내릴 때 돈을 버는 쪽에 거는 투자"},
                     {"term": "펌웨어", "plain": "칩·기계를 움직이는 기본 소프트웨어"},
                     {"term": "거래 제한 명단(Entity List)", "plain": "미국 상무부가 허가 없이 미국 기술을 넘기지 못하게 정한 회사 목록"}],
        "scenes": S,
        "footage": {**fo, **({k: {kk: vv for kk, vv in v.items()} for k, v in CLIPS.items()} if BITES else {})},
        "package": {
            "title": "앤트로픽 상장·AMD 공매도, 한 달 새 바뀐 AI 시장 | 11월 20일",
            "title_options": ["앤트로픽 상장·AMD 공매도, 한 달 새 바뀐 AI 시장 | 11월 20일", "앤트로픽 상장 날, 시장은 왜 2% 빠졌나 | 11월 20일",
                              "앤트로픽 상장·AMD 공매도·한 달 -18% 반도체, 무엇이 바뀌었나 | 11월 20일",
                              "새 주식 1,070억 달러가 들어온 날 — 다우 5만 붕괴 | 11월 20일"],
            "title_why": ["훅(역설 질문, 답 숨김) + 핫 키워드 '앤트로픽' 앞 20자 안", "장면 + 다룬 종목", "숫자 대비"],
            "thumbnails": [
                {"id": "A", "name": "유명인 따옴표 발언 + 검은 거래소 사진 (photo full)", "layout": "photo", "photo_side": "full", "image": {"file": "04_assets/footage/raw/nyse.jpg", "focus": [0.5, 0.5]},
                 "top": "11월 20일 · 엘에리언", "lines": ["\"AI를 위해", "자리를 만든다\""], "hl": ["자리를"], "sub": "앤트로픽 상장 날, 시장은 -2%", "size": 118, "text_y": 330, "marks": [],
                 "why": ["2026-11-20 사용자: 세 장 다 별로 → 다시 만듦", "docs/49: 이름 있는 사람의 따옴표 발언(채널 안 1.23배)", "검은 사진·빨간 띠·노랑 한 낱말(§7-1 기본 모양)"]},
                {"id": "B", "name": "숫자 대비 (dark)", "layout": "versus", "theme": "dark", "left": {"value": "111.50", "label": "앤트로픽 첫 거래 (달러)"},
                 "right": {"value": "97.17", "label": "종가 (-12.9%)"}, "headline": "첫 값에서 13% 밀린 상장", "hl": ["13%"], "marks": [], "why": ["숫자 둘 대비"]},
                {"id": "C", "name": "검은 데이터센터 사진 + 단정 (photo full, 칩 없음)", "layout": "photo", "photo_side": "full", "image": {"file": "04_assets/footage/raw/dc.jpg", "focus": [0.5, 0.5]},
                 "top": "11월 20일 · AMD 공매도 보고서", "lines": ["AMD에도", "중국 질문"], "hl": ["AMD"], "sub": "보고서 스스로 '위반 입증 안 됨'", "size": 130, "text_y": 330, "marks": [],
                 "why": ["2026-11-20 사용자: 빨강·초록 칩이 싼티 → 칩 빼고 검은 사진 + 노랑 한 낱말"]}]},
    }
    (P / "02_script" / "hybrid.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
    print(P, len(S))


if __name__ == "__main__":
    main()
