"""이어 읽는 시장 — 11월 23일(월) 아침 브리핑: 주말에 정해진 것 — 정부 F4(증안펀드 준비) + 손정의 SK하이닉스 1조 달러 검토 보도 + 베선트 CBS(엔비디아 준법·연준) + 오늘 한국 장.
    python scripts/daily_20261123/make.py && python -m ytflow hybrid 20261123-market-daily
"""
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from ytflow.stages import archive  # noqa: E402

P = ROOT / "projects" / "20261123-market-daily"
DS, NP = "dark-doc", "newsprint"
YH = "야후 파이낸스 종가 · 11월 20일(금) 미국 마감 기준 (한국 21일 06:00)"
F4 = "서울신문(22일 18:22)·더팩트(22일 19:20) 보도 — 정부 보도자료 원문 확인 못 함"
SB = "재경일보(21일)·서울경제(22일) 보도, 외신(디 인포메이션) 인용 — 소프트뱅크 대변인·SK하이닉스 관계자 발언 포함"
CBS = "CBS 'Face the Nation' 녹취 (현지 2026.11.22)"
COOK = "리사 쿡 연준 이사 연설 (2026.11.20, 칠레) · federalreserve.gov"
FUT = "시킹알파 (현지 22일 18:03 ET = 한국 23일 08:03) · 선물 장중 값 · 야간선물은 서울신문 22일 보도"

PHOTOS = {
    "nyse": "New York Stock Exchange Facade 2015.jpg",
    "seoul": "Skyline of Yeouido, a prominent finance district in Seoul.jpg",
    "son": "Masayoshi Son.jpg",
    "bessent": "Official portrait of Treasury Secretary Scott Bessent (cropped).jpg",
    "fed": "Eccles Building (26088200676).jpg",
}
KNOWN = {
    "nyse": {"license": "CC BY 2.0", "artist": "작자 미상"},
    "seoul": {"license": "CC BY 4.0", "artist": "작자 미상"},
    "son": {"license": "CC BY 2.0", "artist": "작자 미상"},
    "bessent": {"license": "Public domain", "artist": "U.S. Department of the Treasury"},
    "fed": {"license": "Public domain", "artist": "작자 미상"},
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


def main():
    for d in ("01_research", "02_script", "05_edit"):
        (P / d).mkdir(parents=True, exist_ok=True)
    fo = photos()
    S = []
    s = S.append

    # ── 여는 장면: 갈등 — 같은 주말, 반대 방향의 두 숫자 ──
    s(dict(type="versus", chapter=0, label=FUT,
           left={"value": "-6.99%", "label": "코스피200 야간선물 (금요일 밤)", "icon": "trending-down"},
           right={"value": "+1.19%", "label": "나스닥100 선물 (일요일 밤)", "icon": "trending-up"},
           beats=[{"say": "금요일 밤, 한국의 코스피200 야간선물은 6.99% 빠졌습니다. 그런데 일요일 밤 미국의 나스닥100 선물은 1.19% 올랐습니다. 같은 주말, 정반대의 두 숫자입니다."},
                  {"say": "그 사이 일요일 오후, 정부는 부총리와 한국은행 총재, 금융위원장, 금융감독원장이 모인 긴급회의를 열었습니다. 오늘 아침 9시 한국 장은 이 두 숫자 가운데 어느 쪽을 받게 될까요?"}]))

    # ── 시장 한 장 (근거로 한 번만) ──
    s(dict(type="bars", chapter=0, label=YH + " · 한국 20일 마감은 한국거래소 종가(야후)", title="20일(금) 마감 (%)", unit="", emph=0, skin=DS,
           items=[{"label": "미국 반도체 지수", "value": -10.73, "text": "-10.73", "t": "반도체"}, {"label": "나스닥", "value": -5.28, "text": "-5.28", "t": "나스닥"},
                  {"label": "코스피 (폭락 전)", "value": -5.21, "text": "-5.21", "t": "코스피는"}, {"label": "S&P 500", "value": -3.70, "text": "-3.70", "t": "S&P"}],
           beats=[{"say": "출발점부터 짚겠습니다. 11월 20일 금요일 미국 장 마감 기준, 나스닥은 5.28%, S&P 500은 3.70%, 반도체 지수는 10.73% 내렸습니다. 이 하락은 토요일과 일요일 영상에서 자세히 다뤘습니다."},
                  {"say": "중요한 건 순서입니다. 같은 금요일 코스피는 5.21% 내린 4,869.96으로 닫혔는데, 이건 미국 금요일 폭락보다 먼저 닫힌 숫자입니다. 금요일 밤의 충격은 야간선물로만 먼저 반영됐고, 정규장은 오늘이 처음입니다.",
                   "motion": [M("4,869.96", "count", id="ks", value="4,869.96", label="코스피 20일 종가", x=1600, y=860, w=420, h=150, fs=56)]}]))

    # ── 1. 정부 F4 ──
    s(dict(type="chapter", chapter=1, num="1", title="일요일의 긴급회의", icon="landmark", look="photo", bg_src="seoul",
           beats=B("먼저 일요일 오후 정부서울청사에서 열린 회의입니다. 정부는 무엇을 꺼냈을까요?")))
    s(dict(type="checklist", chapter=1, label=F4, title="22일 긴급 시장상황점검회의 (F4)", x=150, text_w=920, skin=NP,
           rows=[{"label": "증권시장안정펀드: 즉시 가동할 수 있게 '준비' 착수", "state": "warn", "t": "증권시장안정펀드"},
                 {"label": "상장사 하루 자기주식 매수 한도: 24일부터 3개월 완화", "state": "ok", "t": "자기"},
                 {"label": "불법 공매도: 3개월 특별 집중 감시", "state": "ok", "t": "공매도"},
                 {"label": "신용융자·반대매매 점검, 반대매매 사전 안내 강화", "state": "ok", "t": "반대매매"}],
           beats=[{"say": "이형일 부총리가 주재한 회의는 2시간 20분쯤 이어졌습니다. 첫째, 증권시장안정펀드, 이른바 증안펀드를 시장 상황에 따라 바로 가동할 수 있도록 준비에 들어갔습니다. 둘째, 상장사가 하루에 살 수 있는 자기 회사 주식의 주문 한도를 24일부터 석 달 동안 풀어 줍니다.", "upto": 2},
                  {"say": "셋째, 금융감독원과 한국거래소가 석 달 동안 불법 공매도를 집중 감시합니다. 빚을 내 산 주식이 강제로 팔리는 반대매매도 점검하고, 미리 알려 주는 안내를 강화한다고 했습니다. 다만 정부 보도자료 원문은 찾지 못해, 보도 두 곳이 일치하는 내용만 옮겼습니다.", "upto": 4}]))
    s(dict(type="motionboard", chapter=1, label="이 영상의 설명 · 근거: F4 보도(서울신문·더팩트) · 2020년 증안펀드는 이코노미스트·뉴시스 보도", title="속도를 늦추는 장치, 이유를 바꾸는 장치",
           els={"why": {"kind": "card", "x": 420, "y": 330, "icon": "cpu", "label": "떨어진 이유: 미국 AI·반도체", "w": 360},
                "price": {"kind": "card", "x": 420, "y": 760, "icon": "trending-down", "label": "코스피", "value": "-5.21%", "vsize": 46, "w": 300},
                "a0": {"kind": "arrow", "from": "why", "to": "price", "label": "이유", "color": "red"},
                "fund": {"kind": "card", "x": 1480, "y": 300, "icon": "piggy-bank", "label": "증안펀드 (준비만)", "w": 320},
                "buy": {"kind": "card", "x": 1480, "y": 560, "icon": "repeat", "label": "자사주 한도 완화", "w": 320},
                "short": {"kind": "card", "x": 1480, "y": 820, "icon": "eye", "label": "공매도 감시", "w": 320},
                "s1": {"kind": "arrow", "from": "fund", "to": "price", "label": "사는 돈", "bend": 0.12},
                "s2": {"kind": "arrow", "from": "buy", "to": "price", "label": "회사가 사는 돈"},
                "s3": {"kind": "arrow", "from": "short", "to": "price", "label": "파는 쪽 감시", "bend": -0.12},
                "slow": {"kind": "text", "x": 960, "y": 180, "text": "속도는 늦추지만, 이유는 그대로", "size": 52, "color": "red"}},
           beats=[{"say": "그림으로 정리해 보겠습니다. 금요일 한국 장을 끌어내린 이유는 미국의 AI와 반도체였습니다. 정부도 회의에서 AI 투자 우려와 수익성 걱정을 원인으로 꼽았습니다.", "do": ["why", "price", "a0"], "at": {"why": "미국의", "price": "끌어내린"}},
                  {"say": "정부가 꺼낸 세 가지는 모두 오른쪽에서 들어오는 힘입니다. 사 주는 돈인 증안펀드, 회사가 자기 주식을 더 사게 하는 길, 그리고 파는 쪽에 대한 감시입니다.", "do": ["fund", "s1", "buy", "s2", "short", "s3"], "at": {"fund": "증안펀드", "buy": "회사가", "short": "감시"}},
                  {"say": "미끄러운 내리막길에 모래를 뿌리는 것과 비슷합니다. 미끄러지는 속도는 줄일 수 있지만, 길의 기울기를 바꾸지는 못합니다. 2020년 3월 코로나 폭락 때도 약 10조 7천억 원 규모의 증안펀드가 만들어졌는데, 하락 폭은 줄였지만 반등으로 이어지지는 못했다는 평가가 나왔습니다.", "do": ["slow", {"hi": "why"}], "at": {"slow": "기울기를"}}]))

    # ── 2. 손정의 ──
    s(dict(type="chapter", chapter=2, num="2", title="1조 달러를 생각한 사람", icon="building-2", look="photo", bg_src="son",
           beats=B("두 번째, 폭락 한가운데서 나온 뜻밖의 보도입니다. 누군가는 SK하이닉스를 통째로 사려 했다는 겁니다.")))
    s(dict(type="checklist", chapter=2, label=SB, title="손정의 SK하이닉스 1조 달러 검토 보도", x=150, text_w=920, skin=NP,
           rows=[{"label": "외신: 손정의, SK하이닉스 약 1조 달러 인수 검토·자금 논의", "state": "warn", "t": "1조"},
                 {"label": "소프트뱅크: 더 이상 적극 검토하지 않는다", "state": "ok", "t": "대변인은"},
                 {"label": "SK하이닉스: 전혀 아는 바 없다", "state": "ok", "t": "관계자는"},
                 {"label": "법: 외국인 인수는 산업부 장관 사전 승인 (첨단전략산업법 13조)", "state": "warn", "t": "승인"}],
           beats=[{"say": "외신 보도를 인용한 서울경제와 재경일보에 따르면, 소프트뱅크의 손정의 회장이 SK하이닉스를 약 1조 달러에 사는 방안을 검토했고, 월가 금융회사들과 자금 조달까지 논의했다고 합니다.", "upto": 1},
                  {"say": "소프트뱅크 대변인은 이 거래를 더 이상 적극적으로 검토하지 않는다고 밝혔고, SK하이닉스 관계자는 전혀 아는 바가 없다고 했습니다. 그리고 법이 있습니다. 첨단 반도체 기술을 가진 회사를 외국인이 사려면, 산업통상자원부 장관의 사전 승인을 받아야 합니다.", "upto": 4}]))
    s(dict(type="bignum", chapter=2, label="이 영상의 계산 · 숫자: 서울경제 보도(SK하이닉스 시가총액 20일 종가 기준, 1조 달러 ≈ 1,347조 원, 소프트뱅크 현금 9월 말) · 5월 1조 달러 돌파는 알자지라(5.29)",
           small="1조 달러 ≈ 1,347조 원 ÷ SK하이닉스 시가총액 777.5조 원", value="1.73배",
           compare={"label": "소프트뱅크 현금 (9월 말)", "value": "343억 달러 ≈ 3%"},
           beats=[{"say": "계산해 보겠습니다. 1조 달러는 약 1,347조 원입니다. 금요일 종가 기준 SK하이닉스의 시가총액은 777조 5천억 원. 지금 값보다 약 73% 비싼, 1.73배를 쳐준 셈입니다. 공교롭게도 1조 달러는, SK하이닉스가 지난 5월 처음 넘어섰던 시가총액입니다.",
                   "motion": [M("73%", "count", id="pr", value="+73%", label="지금 시가총액보다 (계산)", x=1640, y=530, w=400, h=140, fs=56)]},
                  {"say": "그런데 소프트뱅크가 9월 말에 가진 현금은 약 343억 달러, 인수 금액의 3% 남짓입니다. 나머지 97%는 빌리거나 함께 낼 투자자를 찾아야 합니다. 보도도 자금과 승인 문제로 협의가 멈췄다고 전했습니다.",
                   "motion": [M("97%", "count", id="debt", value="97%", label="빌리거나 함께 낼 몫 (계산)", x=1600, y=880, w=400, h=140, fs=56)]},
                  {"say": "그러니 이 보도를 주가의 근거로 삼을 일은 아닙니다. 다만 하나는 보여 줍니다. 반도체가 폭락하던 바로 그 주에도, 웃돈을 크게 얹어서라도 사고 싶은 회사로 SK하이닉스를 본 시각이 있었다는 겁니다. 메모리 회사의 값을 누가 어떻게 매기는지는, 오늘 저녁 6시 심층에서 자세히 다룹니다."}]))

    # ── 3. 베선트 ──
    s(dict(type="chapter", chapter=3, num="3", title="재무장관의 두 질문", icon="message-circle", look="photo", bg_src="bessent",
           beats=B("세 번째는 미국 일요일 아침 방송입니다. 스콧 베선트 미국 재무장관이 엔비디아와 연준에 대해 말했습니다.")))
    s(dict(type="quote", chapter=3, label=CBS + " · 발언 원문", who="스콧 베선트", role="미국 재무장관 · CBS 'Face the Nation'",
           quote="거기서 누가 준법을 책임졌는지 봐야 합니다.", keyword="책임",
           orig="we do need to see who was in charge of compliance there.",
           beats=[{"say": "진행자가 물었습니다. 열흘 안에 엔비디아의 답이 필요하다고 한 지 일주일인데, 답을 받았느냐. 베선트 장관의 대답은 짧았습니다. 아직 받지 못했다는 겁니다."},
                  {"say": "그리고 이렇게 말했습니다. 거기서 누가 준법을 책임졌는지 봐야 한다, 보통은 법무 부서다. 중국으로 칩이 흘러갔는지에 대해, 회사의 아래층에서 알았는지, 중간에서 알았는지, 꼭대기까지 올라갔는지를 보겠다고 했습니다. 질문이 한 사람에서 회사의 구조로 옮겨 간 겁니다."},
                  {"say": "같은 인터뷰에서 베선트 장관은 엔비디아 칩에 대한 수요는 전 세계적으로 거의 무한하다고도 말했습니다. 수요를 의심하는 게 아니라, 장부와 준법을 묻는다는 겁니다. 조사는 진행 중이고, 위반이 확인된 것은 아닙니다."}]))
    s(dict(type="versus", chapter=3, insight=True, label=CBS + " · " + COOK + " · 의견이며 사실이 아닙니다",
           left={"value": "조이면 실수", "label": "베선트(재무장관): 과잉 긴축 우려", "icon": "trending-down"},
           right={"value": "늦으면 뒤처짐", "label": "쿡(연준 이사): 인상 지연 경고", "icon": "trending-up"},
           beats=[{"say": "베선트 장관은 시장 하락의 이유로 여러 가지가 겹쳤다고 하면서, 연준에서 매우 매파적인 발언이 나왔고, 연준이 지나치게 조이면 정책 실수가 될 수 있다고 믿는 사람이 많다고 했습니다. 지난 몇 달 동안 금융 여건이 크게 빡빡해졌다는 겁니다. 사실이 아니라 한 사람의 시각입니다."},
                  {"say": "이틀 전 리사 쿡 연준 이사의 말은 반대였습니다. 금리 인상을 더 기다리면 뒤처질 위험이 있다. 근거는 3%를 넘는 물가였습니다. 한쪽은 이미 너무 조였다고, 다른 쪽은 아직 덜 조였다고 봅니다. 재무장관은 행정부, 연준은 독립 기관이고, 누가 맞는지는 12월 연준 회의가 가립니다.",
                   "motion": [M("3%를", "count", id="inf", value="3% 넘는 물가", label="쿡 이사의 근거", x=1440, y=860, w=440, h=140, fs=46), M("12월", "count", id="fomc", value="12월 10일", label="연준 결정 (한국 시간 새벽)", x=480, y=860, w=440, h=140, fs=46)]}]))

    # ── 해석 ──
    s(dict(type="map_causal", chapter=4, look="board", label="자체 해석 · 근거: F4 보도, 소프트뱅크 보도, CBS 녹취, 쿡 연설, 선물 값(장중)",
           map={"nodes": {"q": {"label": "주말에 정해진 것: 값이 아니라 책임과 속도", "icon": "circle-help", "x": 960, "y": 260},
                          "gov": {"label": "정부: 떨어지는 속도", "icon": "landmark", "x": 380, "y": 640},
                          "nv": {"label": "베선트: 누가 책임자였나", "icon": "file-search", "x": 960, "y": 760},
                          "son": {"label": "손정의: 다른 눈으로 본 값", "icon": "building-2", "x": 1540, "y": 640}},
                "edges": [["gov", "q"], ["nv", "q"], ["son", "q"]]},
           beats=[{"say": "여기서부터는 해석입니다. 주말 동안 새로 정해진 것을 모아 보면, 정부는 떨어지는 속도를, 베선트 장관은 엔비디아에서 누가 책임자였는지를 다뤘습니다. 손정의 보도는 같은 회사를 전혀 다른 값으로 본 눈이 있었다는 걸 보여 줬습니다.",
                   "reveal": ["gov", "nv", "son"], "active": "gov"},
                  {"say": "하지만 금요일 하락의 이유, AI에 들어간 돈이 장부에 어떻게 적혀 있느냐와 연준이 금리를 더 올리느냐는, 주말 사이 하나도 답이 나오지 않았습니다. 주말에 정해진 건 값이 아니라 책임과 속도입니다.",
                   "reveal": ["q"], "draw": [["gov", "q"], ["nv", "q"], ["son", "q"]], "active": "q"}]))

    # ── 볼 것 ──
    s(dict(type="chapter", chapter=5, num="5", title="이번 주 볼 것", icon="calendar", look="board",
           beats=B("이제 오늘부터 이번 주, 이 해석을 확인할 날짜들입니다.")))
    s(dict(type="checklist", chapter=5, label="한국거래소 · F4 보도 · 미 경제분석국(BEA) 일정 · 뉴욕증권거래소 휴장일 · 투자 권유가 아닙니다", title="일정 (한국 시간)", x=150, text_w=920, skin=NP,
           rows=[{"label": "23일(월) 09:00 · 한국 장 — 미국 금요일 첫 반영", "state": "warn", "t": "9시"},
                 {"label": "24일(화) · 자기주식 매수 한도 완화 시작", "state": "warn", "t": "내일부터는"},
                 {"label": "25일(수) 22:30 · 미국 10월 PCE 물가", "state": "warn", "t": "수요일"},
                 {"label": "26일(목) 미국 휴장 · 27일(금) 단축 거래", "state": "warn", "t": "추수감사절"}],
           beats=[{"say": "오늘 아침 9시, 한국 정규장이 미국 금요일을 처음 받습니다. 야간선물의 마이너스 7%와 미국 선물의 반등 사이 어디에서 열리는지, 그리고 삼성전자와 SK하이닉스를 봅니다. 내일부터는 자기 주식 매수 한도가 풀리니, 회사들이 실제로 자사주를 사겠다는 공시가 늘어나는지도 봅니다.", "upto": 2},
                  {"say": "수요일 밤 10시 30분에는 미국 10월 개인소비지출 물가, 연준이 가장 중시하는 물가 지표가 나옵니다. 베선트 장관과 쿡 이사, 어느 쪽 근거가 커지는지 보는 숫자입니다. 목요일은 추수감사절로 미국 장이 쉬고, 금요일은 일찍 닫습니다.", "upto": 4}]))
    s(dict(type="checklist", chapter=5, label="팩트시트 '틀리는 경우' · 투자 권유가 아닙니다", title="이 해석이 틀리는 경우", x=150, text_w=920, skin=NP,
           rows=[{"label": "오늘 정규장이 야간선물만큼 빠지지 않으면", "state": "warn", "t": "야간선물만큼"},
                 {"label": "증안펀드가 실제로 가동되면", "state": "warn", "t": "가동된다면"},
                 {"label": "25일 PCE 물가가 크게 낮으면", "state": "warn", "t": "낮게"}],
           beats=[{"say": "틀리는 경우도 적어 둡니다. 오늘 한국 장이 야간선물만큼 빠지지 않는다면, 미국 선물 반등과 정부 조치가 일부를 받친 것입니다. 증안펀드가 실제로 가동된다면, 준비라는 오늘의 설명은 하루짜리가 됩니다.", "upto": 2},
                  {"say": "그리고 수요일 물가가 크게 낮게 나온다면, 연준이 너무 조인다는 베선트 장관 쪽 근거가 커집니다.", "upto": 3}]))
    s(dict(type="kinetic", chapter=5, beats=[{"say": "주말에 정해진 건 값이 아니라, 책임과 속도였습니다.", "hit": ["책임과", "속도"]}]))
    s(dict(type="outro", chapter=5, title="23일 아침까지의 소식", sub="출처는 설명란에", clip={"src": "seoul", "start": 0},
           beats=B("정부는 미끄러지는 속도를 줄이겠다고 했고, 미국에서는 책임자를 찾기 시작했습니다. 그렇다면 오늘 아침, 시장은 이유와 속도 가운데 어느 쪽을 더 크게 볼까요?")))
    for i, x in enumerate(S, 1):
        x["id"] = i
    spec = {
        "title": "주말에 정해진 것 — 정부의 증안펀드 준비, 손정의 1조 달러 보도, 베선트의 질문",
        "brand": "market",
        "zoom": "off",
        "core_message": "금요일 미국 폭락(나스닥 -5.28%)을 한국은 야간선물(-6.99%)로만 먼저 받았고, 일요일 밤 미국 선물은 반등(+1.19%, 장중)했다. 주말 사이 정부는 F4 회의로 증안펀드 '준비'·자사주 매수 한도 완화(24일부터 3개월)·불법 공매도 감시를 꺼냈고, 손정의가 SK하이닉스를 약 1조 달러(지금 시가총액의 1.73배)에 사는 것을 검토했다가 멈췄다는 보도가 나왔으며, 베선트 재무장관은 엔비디아에서 누가 준법을 책임졌는지 답을 아직 못 받았다고 했다. 주말에 정해진 건 값이 아니라 책임과 속도이고, 금요일 하락의 이유는 그대로다.",
        "question": "같은 주말, 한국 야간선물은 -7%, 미국 선물은 +1%. 오늘 9시 한국 장은 어느 쪽을 받을까?",
        "logic": ["여는 장면: 야간선물 -6.99% vs 나스닥100 선물 +1.19% → 그 사이 정부 긴급회의 → 질문",
                  "시장 한 장: 20일 마감(근거로 한 번) — 코스피 -5.21%는 미국 폭락 전 숫자",
                  "1) F4: 증안펀드 준비·자사주 한도·공매도 감시 → 설명 무대: 속도를 늦추는 장치 vs 이유(모래 비유, 2020년 사례)",
                  "2) 손정의 1조 달러 보도: 소프트뱅크 '더 이상 검토 안 함'·SK하이닉스 '모름'·외국인 인수 승인 → 계산 1.73배·현금 3% → 심층 예고",
                  "3) 베선트 CBS: 엔비디아 준법 책임자(답 아직) · 수요는 무한 → 연준 과잉 긴축 우려 vs 쿡 인상 지연 경고",
                  "해석: 주말에 정해진 건 값이 아니라 책임과 속도",
                  "볼 것: 23일 09:00 한국 장·24일 자사주·25일 PCE·26~27일 휴장 · 틀리는 경우 3"],
        "compare_to": [{"value": "코스피200 야간선물 -6.99%", "to": "나스닥100 선물 +1.19% (일요일 밤, 장중)"},
                       {"value": "1조 달러 ≈ 1,347조 원", "to": "SK하이닉스 시가총액 777.5조 원 (1.73배)"},
                       {"value": "소프트뱅크 현금 343억 달러", "to": "인수 금액 1조 달러의 약 3%"},
                       {"value": "2020년 증안펀드 약 10조 7천억 원", "to": "이번엔 규모·날짜 없는 '준비'"}],
        "analogies": [{"a": "내리막길에 뿌리는 모래", "b": "증안펀드·자사주·공매도 감시는 미끄러지는 속도를 줄이지만 길의 기울기(떨어진 이유)는 바꾸지 못한다"},
                      {"a": "회사의 아래층·중간층·꼭대기", "b": "베선트의 질문 — 칩이 흘러간 것을 회사의 어느 층까지 알았나"}],
        "past_cases": [{"case": "2020년 3월 코로나 폭락 — 증안펀드 약 10조 7천억 원 조성 (보도)", "lesson": "하락 폭은 줄였지만 반등으로 이어지지는 못했다는 평가 — 속도와 방향은 다르다"}],
        "glossary": [{"term": "증안펀드", "plain": "증권시장안정펀드 — 증시가 크게 떨어질 때 금융회사들이 돈을 모아 주식을 사 주는 펀드"},
                     {"term": "야간선물", "plain": "한국 정규장이 끝난 뒤 밤에 거래되는 코스피200 선물 — 밤사이 해외 소식을 먼저 반영"},
                     {"term": "자기주식 매수 한도", "plain": "회사가 하루에 자기 회사 주식을 살 수 있는 주문 수량의 제한"},
                     {"term": "반대매매", "plain": "빚을 내 산 주식의 담보가 모자라면 증권사가 강제로 파는 것"},
                     {"term": "준법(컴플라이언스)", "plain": "회사가 수출 통제 같은 법을 지키도록 감시하는 일"},
                     {"term": "매파", "plain": "물가를 잡으려 금리를 올리자는 쪽"}],
        "scenes": S,
        "footage": fo,
        "package": {
            "title": "정부는 왜 일요일에 증안펀드를 꺼냈나 — 야간선물 -7%, 오늘 코스피 | 11월 23일",
            "title_options": ["정부는 왜 일요일에 증안펀드를 꺼냈나 — 야간선물 -7%, 오늘 코스피 | 11월 23일",
                              "손정의는 왜 폭락 한복판에 SK하이닉스 1조 달러를 생각했나 | 11월 23일",
                              "블랙먼데이 우려 — 주말에 정해진 세 가지, 오늘 9시 한국 장 | 11월 23일"],
            "title_why": ["실험 E1(ops/next.md): 이름 있는 기관 + 의외의 행동 질문형 + 핫 키워드(증안펀드·야간선물 -7%·코스피) 앞 20자 안 + 날짜 끝",
                          "E1 인물형: 손정의 + 의외의 행동 + SK하이닉스",
                          "국내 제목의 공포 키워드(블랙먼데이 우려 — 서울신문 22일 속보 제목) + 오늘 일정"],
            "thumbnails": [
                {"id": "A", "name": "검은 여의도 + 증안펀드 + 야간선물 (photo full)", "layout": "photo", "photo_side": "full", "image": {"file": "04_assets/footage/raw/seoul.jpg", "focus": [0.5, 0.5]},
                 "top": "11월 23일 · 일요일 긴급회의", "lines": ["증안펀드 꺼냈다", "야간선물 -7%"], "hl": ["증안펀드"], "sub": "오늘 9시, 코스피가 처음 받는다", "size": 106, "text_y": 330, "marks": [],
                 "why": ["그날 국내 매체 핫 키워드(증안펀드·블랙먼데이 우려) + 구체 숫자", "manual/09 §7-1 ③ 사건 장소 사진 어둡게"]},
                {"id": "B", "name": "인물 — 손정의 얼굴 + 1조 달러", "layout": "person", "image": {"file": "04_assets/footage/raw/sonface.jpg"},
                 "person": {"name": "손정의", "role": "소프트뱅크 회장"}, "top": "11월 23일 · 외신 보도",
                 "lines": ["SK하이닉스", "1조 달러?"], "hl": ["1조 달러?"], "credit": "사진: 위키미디어 공용 CC BY 2.0 (Masayoshi Son on July 11, 2008)",
                 "why": ["manual/09 §7-1 ⑥ 당사자 얼굴 크게 — docs/55", "실험 E1 인물 + 의외의 행동"]},
                {"id": "C", "name": "숫자 대비 (dark)", "layout": "versus", "theme": "dark", "left": {"value": "-6.99%", "label": "한국 야간선물"},
                 "right": {"value": "+1.19%", "label": "미국 선물 (일요일 밤)"}, "headline": "오늘 코스피는 어느 쪽?", "hl": ["어느 쪽?"], "marks": [],
                 "why": ["갈등이 보이는 숫자 대비 + 질문형 (질문형 공포 훅 후보)"]}],
            "ticker": [{"name": "S&P 500", "chg": "-3.70%"}, {"name": "나스닥", "chg": "-5.28%"}, {"name": "반도체(SOX)", "chg": "-10.73%"}],
            "tags": ["증안펀드", "블랙먼데이", "코스피 전망", "코스피 폭락", "야간선물", "삼성전자", "SK하이닉스", "손정의", "소프트뱅크",
                     "SK하이닉스 인수", "엔비디아", "베선트", "나스닥 폭락", "반도체 폭락", "자사주 매입", "공매도", "연준", "금리 인상", "PCE 물가", "추수감사절 휴장"],
            "hashtags": ["증안펀드", "코스피", "SK하이닉스"]},
    }
    (P / "02_script" / "hybrid.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
    print(P, len(S))


if __name__ == "__main__":
    main()
