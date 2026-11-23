"""이어 읽는 시장 — 11월 23일(월) 심층: 손정의의 1조 달러 — SK하이닉스는 미친 값인가, 싼 값인가, 왜 사기 어려운가.
    python scripts/daily_20261123_softbank/make.py && python -m ytflow hybrid 20261123-market-deep-softbank-hynix
"""
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from ytflow.stages import archive  # noqa: E402

P = ROOT / "projects" / "20261123-market-deep-softbank-hynix"
DS, NP = "dark-doc", "newsprint"
KX = "한국거래소 종가(야후) · 11월 20일(금) 한국 마감 기준 · 6월 고점은 보도"
SED = "서울경제(2026.11.22) 숫자 · 디 인포메이션 보도(TNW·로이터 인용)"

PHOTOS = {
    "son": "Masayoshi Son.jpg",
    "hynix": "SK Hynix DDR5 form factors.jpg",
    "seoul": "Skyline of Yeouido, a prominent finance district in Seoul.jpg",
    "racks": "Datacenter Server Racks (22370909788).jpg",
}
KNOWN = {
    "son": {"license": "CC BY 2.0", "artist": "작자 미상"},
    "hynix": {"license": "CC BY 4.0", "artist": "작자 미상"},
    "seoul": {"license": "CC BY 4.0", "artist": "작자 미상"},
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


def main():
    for d in ("01_research", "02_script", "05_edit"):
        (P / d).mkdir(parents=True, exist_ok=True)
    fo = photos()
    S = []
    s = S.append

    # ── 여는 장면: 갈등 — 62% 싸진 회사에 73% 웃돈 ──
    s(dict(type="versus", look="duel", chapter=0, label=KX + " · " + SED,
           left={"value": "-61.9%", "label": "주가 (6월 고점 → 20일)", "icon": "trending-down"},
           right={"value": "+73%", "label": "1조 달러의 웃돈", "icon": "trending-up"},
           beats=[{"say": "SK하이닉스 주가는 6월 최고가 291만 9천 원에서, 11월 20일 한국 장 마감 기준 111만 3천 원까지 내려왔습니다. 다섯 달 만에 61.9%가 빠졌습니다.",
                   "motion": [M("291만", "count", id="hi", value="2,919,000원", label="6월 22일 최고가 (보도)", x=480, y=880, w=460, h=130, fs=44), M("111만", "count", id="now", value="1,113,000원", label="11월 20일 종가", x=1440, y=880, w=460, h=130, fs=44)]},
                  {"say": "그런데 바로 그 주, 소프트뱅크의 손정의 회장이 이 회사를 약 1조 달러, 지금 시가총액보다 73% 비싼 값에 사는 방안을 검토했다는 보도가 나왔습니다. 시장은 팔고 있었고, 한 사람은 웃돈을 얹어 사려 했습니다."},
                  {"say": "그렇다면 1조 달러는 미친 값일까요, 아니면 싼 값일까요. 그리고 그 값을 낸다 해도, 왜 실제로는 사기 어려울까요?"}]))
    s(dict(type="checklist", chapter=0, label="이 영상의 정리 · 근거: 반도체 지수(야후), SK하이닉스 3분기 실적, 소프트뱅크 대변인(보도)", title="지금의 의심 — 아는 것과 모르는 것", x=150, text_w=940, skin=NP,
           rows=[{"label": "반도체 폭락 = AI 끝? — 주가 하락은 이익 감소가 아니다", "state": "warn", "t": "AI"},
                 {"label": "이익이 정점? — 3분기 영업이익률 80%, 그다음은 모른다", "state": "warn", "t": "정점"},
                 {"label": "진짜 사려 했나? — 검토는 제안이 아니다", "state": "warn", "t": "제안"}],
           beats=[{"say": "먼저 지금 쏟아지는 의심부터 짚겠습니다. 반도체가 폭락했으니 AI가 끝났느냐. 주가가 빠졌다는 건 사실이지만, 이익이 줄었다는 숫자는 아직 없습니다. SK하이닉스의 3분기 영업이익률은 80%였습니다.", "upto": 2,
                   "motion": [M("80%", "count", id="opm", value="80%", label="3분기 영업이익률", x=1640, y=420, w=380, h=140, fs=56)]},
                  {"say": "다만 이게 꼭대기인지, 그다음이 어떨지는 모릅니다. 그리고 손정의가 진짜 사려 했느냐. 소프트뱅크 대변인은 이 건은 더 이상 적극 검토하지 않는다고 했습니다. 검토였지 제안이 아니었다는 뜻입니다. 이 영상은 그래서 사려 했느냐가 아니라, 그 값이 무엇을 뜻하느냐를 봅니다.", "upto": 3}]))

    # ── 1. 손정의의 논리 ──
    s(dict(type="chapter", chapter=1, num="1", title="손정의는 무엇을 사려 했나", icon="building-2", look="photo", bg_src="son",
           beats=B("첫 번째 시각은 사려 한 사람, 손정의입니다. 그는 무엇을 보고 이 값을 생각했을까요?")))
    s(dict(type="quote", chapter=1, insight=True, label="소프트뱅크그룹 연차보고서 2026 CEO 메시지 (2026.6.24) · 소프트뱅크 월드 2026 기조연설 공식 블로그 (2026.7) · 의견이며 사실이 아닙니다",
           who="손정의", role="소프트뱅크그룹 회장 · 2026년 연차보고서",
           quote="우리는 ASI 시대의 1위 플랫폼 제공자가 되려 합니다.", keyword="1위",
           orig="We aim to become the No. 1 Platform Provider for this new era of ASI.",
           beats=[{"say": "손정의는 올해 연차보고서에서 이렇게 썼습니다. 사람을 넘어서는 인공지능, ASI의 시대에 1위 플랫폼 제공자가 되겠다. 그리고 그 시대에는 거대한 계산을 감당할 반도체가 필요하다고 했습니다."},
                  {"say": "7월 소프트뱅크 월드 기조연설에서는, AI에 해마다 5조 달러의 투자가 필요해질 거라고 말했습니다. 6월 주주총회에서는 AI 거품론을 AI에 대한 모욕이라고까지 했다는 보도입니다. 그 사람의 시각입니다.",
                   "motion": [M("5조", "count", id="t5", value="연 5조 달러", label="손정의가 본 AI 투자 (기조연설)", x=1500, y=860, w=460, h=150, fs=50)]}]))
    s(dict(type="motionboard", chapter=1, label="이 영상이 세운 논리 사슬 — 손정의가 이 순서로 말한 기록은 없음 · 사이메모리는 보도(트렌드포스·테크레이더)", title="손정의의 계산을 이어 붙이면",
           els={"asi": {"kind": "card", "x": 260, "y": 420, "icon": "brain", "label": "ASI 가 온다", "w": 260},
                "chip": {"kind": "card", "x": 700, "y": 420, "icon": "cpu", "label": "돈은 칩·데이터센터로", "w": 300},
                "hbm": {"kind": "card", "x": 1170, "y": 420, "icon": "layers", "label": "칩 중 막힌 곳: HBM", "w": 300},
                "own": {"kind": "card", "x": 1640, "y": 420, "icon": "building-2", "label": "1위 회사를 산다", "color": "red", "w": 290},
                "a1": {"kind": "arrow", "from": "asi", "to": "chip"}, "a2": {"kind": "arrow", "from": "chip", "to": "hbm"},
                "a3": {"kind": "arrow", "from": "hbm", "to": "own", "color": "red"},
                "zam": {"kind": "card", "x": 1170, "y": 800, "icon": "flask-conical", "label": "직접 만들기: 사이메모리", "value": "2029년 목표", "vsize": 36, "w": 340},
                "a4": {"kind": "arrow", "from": "hbm", "to": "zam", "label": "느린 길"},
                "note": {"kind": "text", "x": 960, "y": 200, "text": "우리가 이어 붙인 논리입니다", "size": 44, "color": "red"}},
           beats=[{"say": "그의 말과 행동을 이어 붙이면 이런 사슬이 됩니다. 먼저 밝혀 둘 점은, 이건 이 채널이 세운 논리이고 손정의가 이 순서로 말한 기록은 없다는 겁니다. ASI가 온다, 그러면 돈은 칩과 데이터센터로 간다, 그 칩 가운데 공급이 가장 막힌 곳이 고대역폭 메모리 HBM이다.", "do": ["note", "asi", "a1", "chip", "a2", "hbm"], "at": {"asi": "ASI가", "chip": "칩과", "hbm": "HBM"}},
                  {"say": "실제로 소프트뱅크는 2월, 자회사 사이메모리를 통해 인텔과 HBM을 대신할 메모리를 개발하기로 했습니다. 다만 상용화 목표는 2029회계연도이고, 삼성과 SK하이닉스가 이미 몇 세대 앞서 있다는 회의적인 평가도 있습니다.", "do": ["zam", "a4"], "at": {"zam": "사이메모리"}},
                  {"say": "직접 만드는 길이 느리다면, 남는 길은 이미 1위인 회사를 사는 것입니다. 이 사슬을 받치는 숫자는 SK하이닉스의 3분기 영업이익 83조 3천억 원, 이익률 80%입니다. 어긋나는 숫자도 있습니다. 같은 7월부터 9월, 소프트뱅크 자신은 약 1조 1천억 엔의 순손실을 냈습니다.", "do": ["own", "a3"], "at": {"own": "1위인"}}]))
    s(dict(type="versus", look="duel", chapter=1, label="소프트뱅크 Arm 인수 발표(2016.7.18) · 이번은 서울경제 숫자로 계산",
           left={"value": "43%", "label": "Arm 웃돈 (2016)", "icon": "history"},
           right={"value": "73%", "label": "이번 (20일 종가 대비)", "icon": "building-2"},
           beats=[{"say": "손정의가 웃돈을 얹어 산 건 처음이 아닙니다. 2016년 영국 반도체 설계 회사 Arm을 살 때, 직전 종가보다 43% 비싼 값을 냈습니다. 그때도 1조 엔짜리 단기 대출로 돈을 마련했습니다."},
                  {"say": "이번엔 웃돈이 73%, 크기는 Arm의 약 31배입니다. 판정하자면, 손정의의 논리는 숫자 하나에는 기대고 있습니다. 지금 SK하이닉스가 버는 돈입니다. 하지만 그 돈이 앞으로도 계속 벌린다는 가정 위에 서 있고, 그 가정이 바로 시장이 의심하는 부분입니다."}]))

    # ── 2. 싸다 ──
    s(dict(type="chapter", chapter=2, num="2", title="싸다는 쪽의 근거", icon="trending-up", look="photo", bg_src="hynix",
           beats=B("두 번째 시각은, 이 회사의 주가가 원래부터 싸게 매겨져 있었다는 쪽입니다.")))
    s(dict(type="quote", chapter=2, insight=True, label="한화투자증권 박준영 보고서 · 이데일리 영문 보도 (2026.6.22) · 의견이며 사실이 아닙니다",
           who="박준영", role="한화투자증권 연구원 · 2026년 6월 보고서",
           quote="세계 기술 업종 안에서 부당하게 저평가될 이유가 없다.", keyword="저평가",
           orig="It does not need to be unjustifiably undervalued within the global tech sector.",
           beats=[{"say": "한화투자증권의 박준영 연구원은 6월 보고서에서, SK하이닉스가 앞으로 1년 이익 기준으로 주가수익비율, PER 약 6.6배에 거래된다고 봤습니다. 미국 경쟁사 마이크론은 10배가 넘었습니다. 같은 메모리를 파는데 한국 회사만 싸게 매겨질 이유가 없다는 겁니다.",
                   "motion": [M("6.6배", "count", id="p66", value="6.6배", label="SK하이닉스 선행 PER", x=1180, y=870, w=360, h=130, fs=46),
                              M("10배", "count", id="p10", value="10배+", label="마이크론 (같은 보고서)", x=1600, y=870, w=360, h=130, fs=46)]},
                  {"say": "블룸버그도 6월, 마이크론과의 할인 폭이 정당화하기 어려워 보인다고 썼습니다. 사실이 아니라 이름 있는 기관과 매체의 시각입니다."}]))
    s(dict(type="checklist", chapter=2, label="SK하이닉스 미국 상장(코리아타임스 2026.7.10) · 자사주(중앙일보 2026.8.19) · 모틀리풀(2026.7.14) · 주가는 야후", title="이 시각을 받치는 것, 어긋나는 것", x=150, text_w=940, skin=NP,
           rows=[{"label": "받침: 7월 미국 상장 — 약 265억 달러, 주당 149달러", "state": "ok", "t": "상장"},
                 {"label": "받침: 8월 회사가 40조 원 자사주 매입·소각", "state": "ok", "t": "40조"},
                 {"label": "어긋남: 그 뒤에도 주가 6월 고점 대비 -61.9%", "state": "warn", "t": "61.9"},
                 {"label": "반론: '빨리 풀릴 수 있는 사이클 내기' (모틀리풀)", "state": "warn", "t": "사이클"}],
           beats=[{"say": "이 시각을 받치는 행동이 둘 있습니다. SK하이닉스는 7월 미국 나스닥에 상장해 약 265억 달러를 모았고, 8월에는 40조 원어치 자기 주식을 사서 없애겠다고 했습니다. 회사 스스로 지금 주가가 싸다고 본 셈입니다.", "upto": 2},
                  {"say": "그런데 어긋나는 숫자가 더 큽니다. 상장과 자사주 뒤에도 주가는 6월 고점보다 61.9% 아래입니다. 미국 투자 매체 모틀리풀은 이런 높은 평가는 빨리 풀릴 수 있는 사이클 내기라고 봤습니다.", "upto": 4},
                  {"say": "판정하면, 싸다는 쪽의 근거, 이익에 비해 주가가 낮다는 건 숫자로 맞습니다. 하지만 PER은 지금의 이익이 계속된다는 전제로 계산합니다. 메모리처럼 이익이 크게 오르내리는 업종에서, 시장은 바로 그 전제를 할인하고 있는 겁니다."}]))

    # ── 3. 못 산다 ──
    s(dict(type="chapter", chapter=3, num="3", title="사려면 넘어야 할 세 벽", icon="shield", look="photo", bg_src="seoul",
           beats=B("세 번째 시각은 값이 아니라, 애초에 살 수가 없다는 쪽입니다.")))
    s(dict(type="quote", chapter=3, insight=True, label="머니모닝 코디 알렉산더 (2026.11.21) · 의견이며 사실이 아닙니다",
           who="코디 알렉산더", role="미국 투자 매체 머니모닝",
           quote="원하는 것과, 실제로 집행할 수 있는 자본은 다르다.", keyword="자본",
           orig="Desire and executable capital are different things.",
           beats=[{"say": "미국 투자 매체 머니모닝의 코디 알렉산더는 이번 보도를 두고, 원하는 것과 실제로 집행할 수 있는 자본은 다르다고 썼습니다. 한국 아주경제도 규모와 흩어진 주주, 자금, 규제 때문에 극도로 복잡한 거래라고 봤습니다. 이 주장을 세 벽으로 나눠 보겠습니다."}]))
    s(dict(type="motionboard", chapter=3, label="근거: 서울경제(현금·법), IBTimes(소프트뱅크 시총·SK스퀘어 지분, 아주경제 인용), TNW(오픈AI 투자) · 계산은 이 영상",
           title="돈, 법, 주인",
           els={"sb": {"kind": "card", "x": 200, "y": 560, "icon": "building-2", "label": "소프트뱅크", "w": 300},
                "hx": {"kind": "card", "x": 1720, "y": 560, "icon": "cpu", "label": "SK하이닉스", "w": 300},
                "w1": {"kind": "card", "x": 600, "y": 560, "icon": "wallet", "label": "돈", "value": "현금 3.4%", "vsize": 40, "w": 300},
                "w2": {"kind": "card", "x": 960, "y": 560, "icon": "scale", "label": "법", "value": "장관 사전 승인", "vsize": 40, "w": 300},
                "w3": {"kind": "card", "x": 1320, "y": 560, "icon": "users", "label": "주인", "value": "SK스퀘어 20.67%", "vsize": 40, "w": 300},
                "try": {"kind": "arrow", "from": "sb", "to": "hx", "label": "1조 달러", "color": "red", "bend": -0.35},
                "oai": {"kind": "text", "x": 960, "y": 840, "text": "1조 달러 = 소프트뱅크 시총의 9.2배 · 오픈AI에 이미 약 646억 달러(대출 400억)", "size": 32},
                "lead": {"kind": "text", "x": 960, "y": 140, "text": "값을 내도 넘어야 할 벽 셋", "size": 50, "color": "red"}},
           beats=[{"say": "첫째, 돈입니다. 소프트뱅크의 현금은 약 343억 달러, 1조 달러의 3.4%입니다. 1조 달러는 소프트뱅크 자신의 시가총액보다 9.2배 큽니다. 게다가 이미 오픈AI에 약 646억 달러를 넣기로 했고, 그 일부는 400억 달러짜리 대출로 마련했습니다.", "do": ["lead", "sb", "hx", "try", "w1", "oai"], "at": {"w1": "3.4%", "oai": "오픈AI에"}},
                  {"say": "둘째, 법입니다. 첨단전략산업법 13조에 따라, 국가첨단전략기술을 가진 회사를 외국인이 인수하려면 산업통상자원부 장관의 사전 승인을 받아야 합니다. SK하이닉스의 HBM은 그 한가운데 있는 기술입니다.", "do": ["w2"], "at": {"w2": "13조"}},
                  {"say": "셋째, 주인입니다. 최대주주 SK스퀘어가 20.67%를 갖고 있고, SK 쪽은 이 일에 대해 아는 바가 없다고 했습니다. 파는 사람이 없으면 값은 의미가 없습니다.", "do": ["w3"], "at": {"w3": "20.67%"}}]))
    s(dict(type="checklist", chapter=3, label="미국 대통령령(2018.3.12) · 도시바메모리 매각 보도(탐스하드웨어) · 매그나칩 공시(2021.12.13)", title="나라가 반도체 인수를 막거나 묶은 선례", x=150, text_w=940, skin=NP,
           rows=[{"label": "2018 브로드컴→퀄컴 1,170억 달러: 미국 대통령이 금지", "state": "warn", "t": "퀄컴"},
                 {"label": "2018 도시바메모리 매각: SK하이닉스 의결권 15% 이하로 묶음", "state": "warn", "t": "도시바"},
                 {"label": "2021 매그나칩 14억 달러: 미국 승인 못 받아 무산", "state": "warn", "t": "매그나칩"}],
           beats=[{"say": "나라가 반도체 인수를 막은 일은 처음이 아닙니다. 2018년 브로드컴이 1,170억 달러에 퀄컴을 사려 하자, 미국 대통령이 국가 안보를 이유로 금지했습니다.", "upto": 1},
                  {"say": "같은 해 일본 도시바가 메모리 사업을 팔 때, SK하이닉스는 3,950억 엔을 넣고도 10년 동안 의결권을 15% 이하로 묶이는 조건을 받았습니다. 2021년에는 한국 반도체 회사 매그나칩의 14억 달러 매각이 미국 승인을 못 받아 무산됐습니다.", "upto": 3,
                   "motion": [M("15%", "count", id="v15", value="15% 이하", label="SK하이닉스 의결권 (도시바메모리)", x=1600, y=860, w=420, h=140, fs=48)]},
                  {"say": "판정하면, 못 산다는 쪽의 근거는 돈과 법과 주인, 셋 다 확인되는 숫자와 조문입니다. 다만 못 산다는 것이 비싸다는 뜻은 아닙니다. 이 시각은 값이 아니라 가능성에 대한 답입니다."}]))

    # ── 4. 계산 장 ──
    s(dict(type="chapter", chapter=4, num="4", title="1조 달러가 깔고 있는 이익", icon="calculator", look="board",
           beats=B("이제 이 채널이 직접 계산해 보겠습니다. 1조 달러와 지금 시장 값은, 각각 앞으로의 이익을 얼마로 보고 있을까요?")))
    s(dict(type="bignum", chapter=4, label="이 영상의 계산 · SK하이닉스 2026년 1~3분기 실적(회사 발표) · 시가총액 20일 종가(서울경제) · 3분기 말 순현금 98.7조 원",
           small="1조 달러면 PER (지금 3.4배)", value="5.8배",
           compare={"label": "영업이익 기준 (순현금 뺀 값 ÷ 3분기×4)", "value": "2.0배 → 3.7배"},
           beats=[{"say": "SK하이닉스는 올해 1분기부터 3분기까지 순이익 174조 원을 냈습니다. 1년으로 늘리면 232조 원. 지금 시가총액은 이 이익의 3.4배, 1조 달러를 내도 5.8배입니다.",
                   "motion": [M("232조", "count", id="ni", value="232조 원", label="연환산 순이익 (계산)", x=330, y=880, w=380, h=140, fs=50)]},
                  {"say": "순이익은 영업 밖의 손익으로 흔들리니 영업이익으로도 봅니다. 3분기 영업이익을 네 배 한 333조 원에 비해, 회사가 가진 순현금 98조 7천억 원을 뺀 값은 지금 2.0배, 1조 달러여도 3.7배입니다. 어느 쪽으로 봐도 한 자릿수입니다.",
                   "motion": [M("333조", "count", id="op", value="333조 원", label="3분기 영업이익 × 4", x=1640, y=890, w=420, h=140, fs=50)]}]))
    s(dict(type="bars", chapter=4, label="이 영상의 계산 · 가정: 이익이 꺾인 뒤 '보통' PER 10배 (한화 보고서의 마이크론 비교) · 값 ÷ 10", title="PER 10배라면, 값이 깔고 있는 '오래 갈 이익' (조 원)", unit="", emph=2, skin=DS,
           items=[{"label": "지금 이익", "value": 232.1, "text": "232", "t": "232"},
                  {"label": "1조 달러", "value": 134.7, "text": "135", "t": "1조 달러는"},
                  {"label": "지금 시장", "value": 77.7, "text": "78", "t": "지금 시장"}],
           beats=[{"say": "그런데 이렇게 싸 보이는 데는 이유가 있습니다. 메모리 이익은 꼭대기 뒤에 크게 줄어 왔습니다. 그래서 하나만 가정해 봅니다. 이익이 꺾인 뒤 보통의 값을 PER 10배로 두는 겁니다. 한화 보고서가 비교한 마이크론의 수준입니다."},
                  {"say": "그러면 1조 달러는 오래 갈 이익을 134조 7천억 원으로 본 값입니다. 지금 이익보다 42% 줄어도 괜찮다는 계산입니다. 반면 지금 시장 값 777조 원은 77조 7천억 원, 이익이 67% 줄어드는 것을 깔고 있습니다.",
                   "motion": [M("42%", "count", id="d42", value="-42%", label="1조 달러가 견디는 이익 감소", x=1640, y=330, w=400, h=130, fs=50),
                              M("67%", "count", id="d67", value="-67%", label="지금 시장이 깐 이익 감소", x=1640, y=490, w=400, h=130, fs=50)]},
                  {"say": "가정을 PER 15배로 바꾸면 숫자는 각각 61%, 78% 감소로 바뀝니다. 하지만 순서는 그대로입니다. 1조 달러는 언제나 이익이 덜 줄어든다는 쪽에 건 값입니다.",
                   "motion": [M("15배", "count", id="p15", value="15배일 때 -61% / -78%", label="민감도 (계산)", x=1640, y=650, w=420, h=130, fs=30)]}]))
    s(dict(type="map_causal", chapter=4, look="board", label="자체 해석 · 근거: 위 계산(가정 PER 10배), 한화·블룸버그·머니모닝·모틀리풀 시각, 법·선례",
           map={"nodes": {"q": {"label": "이익 감소에 건 내기의 크기", "icon": "circle-help", "x": 960, "y": 250},
                          "cheap": {"label": "싸다: 이익 대비 값 (PER)", "icon": "trending-up", "x": 380, "y": 650},
                          "bet": {"label": "1조 달러 -42% vs 시장 -67%", "icon": "calculator", "x": 960, "y": 760},
                          "cant": {"label": "못 산다: 돈·법·주인", "icon": "shield", "x": 1540, "y": 650}},
                "edges": [["cheap", "q"], ["bet", "q"], ["cant", "q"]]},
           beats=[{"say": "여기서부터는 해석입니다. 세 시각을 겹쳐 보면, 싸다는 쪽은 이익 대비 값을, 못 산다는 쪽은 돈과 법과 주인을 봅니다. 서로 다른 질문에 답하고 있어서 둘 다 맞을 수 있습니다.",
                   "reveal": ["cheap", "cant"], "active": "cheap"},
                  {"say": "그리고 1조 달러라는 숫자 자체는, 미친 값도 싼 값도 아닙니다. 이익이 얼마나 줄어들지에 대한 내기의 크기가 다를 뿐입니다. 손정의 쪽은 42%, 시장은 67%. 두 값의 차이는 결국 이 한 가지 생각의 차이입니다.",
                   "reveal": ["bet", "q"], "draw": [["cheap", "q"], ["bet", "q"], ["cant", "q"]], "active": "q"}]))

    # ── 5. 판가름 ──
    s(dict(type="chapter", chapter=5, num="5", title="누가 맞았는지 알려 줄 날짜", icon="calendar", look="board",
           beats=B("그렇다면 42%와 67%, 어느 쪽에 가까운지는 언제 알 수 있을까요?")))
    s(dict(type="checklist", chapter=5, label="마이크론·SK하이닉스 IR 일정(관례·보도) · 소프트뱅크 대출 만기(TNW) · DART · 투자 권유가 아닙니다", title="판가름 숫자 (한국 시간)", x=150, text_w=940, skin=NP,
           rows=[{"label": "12월 18일 무렵 · 마이크론 실적 — 메모리 이익률 방향", "state": "warn", "t": "마이크론"},
                 {"label": "2027년 1월 하순 · SK하이닉스 4분기 영업이익 (3분기 83.3조)", "state": "warn", "t": "4분기"},
                 {"label": "2027년 3월 25일 · 소프트뱅크 400억 달러 대출 만기", "state": "warn", "t": "만기"},
                 {"label": "수시 · 승인 신청·SK 공시가 나오나", "state": "warn", "t": "공시"}],
           beats=[{"say": "첫 숫자는 12월 18일 무렵 나올 미국 마이크론의 실적입니다. 같은 메모리 회사의 이익률이 어느 쪽으로 움직이는지가 먼저 보입니다. 그리고 내년 1월 하순, SK하이닉스의 4분기 영업이익이 3분기 83조 3천억 원에서 얼마나 바뀌는지가 핵심입니다.", "upto": 2},
                  {"say": "손정의 쪽에서는 내년 3월 25일, 오픈AI 투자를 위해 빌린 400억 달러의 만기가 옵니다. 그리고 실제로 인수가 다시 시도된다면, 장관 승인 신청이나 SK의 공시로 먼저 드러날 겁니다.", "upto": 4}]))
    s(dict(type="checklist", chapter=5, label="팩트시트 '틀리는 경우' · 투자 권유가 아닙니다", title="이 계산이 틀리는 경우", x=150, text_w=940, skin=NP,
           rows=[{"label": "이익이 42% 넘게 줄면 — 1조 달러는 비싼 값이었다", "state": "warn", "t": "넘게"},
                 {"label": "이익이 67%보다 덜 줄면 — 시장이 과하게 깔았다", "state": "warn", "t": "덜"},
                 {"label": "PER 10배 가정이 틀리면 — 기준이 바뀐다", "state": "warn", "t": "가정"}],
           beats=[{"say": "틀리는 경우도 적어 둡니다. SK하이닉스의 이익이 42% 넘게 줄어든다면, 1조 달러는 비싼 값이었던 겁니다. 반대로 67%보다 덜 줄어든다면, 지금 시장 값이 감소를 지나치게 깔고 있었던 겁니다.", "upto": 2},
                  {"say": "그리고 메모리가 다시 성장 업종처럼 매겨져 보통의 PER이 10배가 아니게 된다면, 이 계산의 기준 자체가 바뀝니다.", "upto": 3}]))
    s(dict(type="kinetic", chapter=5, beats=[{"say": "1조 달러는 값이 아니라, 이익이 얼마나 줄어들지에 건 내기였습니다.", "hit": ["값이", "내기"]}]))
    s(dict(type="outro", chapter=5, title="11월 23일 심층", sub="출처는 설명란에", clip={"src": "hynix", "start": 0},
           beats=B("시장은 이익이 3분의 2쯤 줄어든다고 값을 매겼고, 한 사람은 그 절반도 안 줄어든다고 봤습니다. 내년 1월의 숫자는, 어느 쪽에 더 가까울까요?")))
    for i, x in enumerate(S, 1):
        x["id"] = i
    spec = {
        "title": "손정의의 1조 달러 — SK하이닉스는 미친 값인가, 싼 값인가, 왜 사기 어려운가",
        "brand": "market",
        "zoom": "off",
        "core_message": "6월 고점보다 61.9% 내린 SK하이닉스를 손정의는 지금 시가총액보다 73% 비싼 1조 달러에 사는 것을 검토했다(보도, 소프트뱅크 '더 이상 적극 검토 안 함'). 손정의의 논리는 지금의 이익(3분기 영업이익률 80%)에, '싸다' 쪽은 이익 대비 PER 에, '못 산다' 쪽은 돈(현금 3.4%)·법(장관 사전 승인)·주인(SK스퀘어 20.67%)에 기댄다. 이 채널의 계산(PER 10배 가정)으로는 1조 달러는 이익이 42%까지만 준다에, 지금 시장은 67% 준다에 건 값 — 미친 값도 싼 값도 아닌 내기의 크기 차이다.",
        "question": "6월보다 62% 싸진 회사를 지금 값의 1.73배로 사려 했다. 1조 달러는 미친 값인가, 싼 값인가 — 왜 실제로는 사기 어려운가?",
        "logic": ["여는 장면: 주가 -61.9% vs 웃돈 +73% → 질문 / 지금의 의심(아는 것·모르는 것)",
                  "1) 손정의: 원문(ASI 1위·연 5조 달러) → 우리가 세운 논리 사슬(ASI→칩→HBM→1위 회사) → 받침(영업이익률 80%)·어긋남(소프트뱅크 순손실) → Arm 43% vs 73%, 31배 → 판정",
                  "2) 싸다: 박준영(PER 6.6 vs 마이크론 10+)·블룸버그 → 받침(ADR·자사주)·어긋남(-61.9%, 모틀리풀) → 판정: PER 은 이익 지속 전제",
                  "3) 못 산다: 알렉산더 원문 → 세 벽(돈 3.4%·9.2배·오픈AI / 법 13조 / 주인 20.67%) → 선례(퀄컴·도시바메모리·매그나칩) → 판정: 가능성의 답",
                  "4) 계산: PER 3.4→5.8, EV/영업이익 2.0→3.7 → PER 10배 가정: 1조 달러 -42% vs 시장 -67% (15배면 -61%/-78%) → 해석: 내기의 크기",
                  "5) 판가름: 12.18 마이크론·1월 SK하이닉스 4분기·3.25 소프트뱅크 대출 만기·공시 · 틀리는 경우 3"],
        "compare_to": [{"value": "1조 달러 ≈ 1,347조 원", "to": "SK하이닉스 시가총액 777.5조 원 (+73%)"},
                       {"value": "웃돈 73%", "to": "2016년 Arm 인수 웃돈 43%"},
                       {"value": "소프트뱅크 현금 343억 달러", "to": "1조 달러의 3.4%"},
                       {"value": "PER 5.8배 (1조 달러)", "to": "마이크론 10배+ (한화 보고서)"},
                       {"value": "1조 달러가 깐 이익 감소 -42%", "to": "지금 시장이 깐 -67%"}],
        "analogies": [{"a": "직접 만들기 vs 1위 회사 사기", "b": "사이메모리(2029년 목표)는 느린 길 — 남는 길은 이미 앞선 회사를 사는 것"},
                      {"a": "내기의 크기", "b": "같은 회사의 두 값은 '이익이 얼마나 줄어드나'에 건 판돈의 차이"},
                      {"a": "넘어야 할 세 벽", "b": "돈·법·주인 — 값을 내도 셋 중 하나만 막혀도 못 산다"}],
        "past_cases": [{"case": "2016년 소프트뱅크의 Arm 인수 — 43% 웃돈, 1조 엔 단기 대출", "lesson": "손정의는 전에도 웃돈과 대출로 반도체 회사를 샀다 — 이번은 31배 크기"},
                       {"case": "2018년 브로드컴의 퀄컴 인수 금지 · 도시바메모리 매각의 의결권 15% 조건", "lesson": "나라들은 반도체 회사의 경영권이 외국으로 가는 것을 막거나 묶는다"},
                       {"case": "2021년 매그나칩 매각 무산", "lesson": "승인을 못 받으면 값과 상관없이 끝난다"}],
        "glossary": [{"term": "PER", "plain": "주가수익비율 — 회사 값이 1년 이익의 몇 배인가"},
                     {"term": "웃돈 (경영권 프리미엄)", "plain": "회사를 통째로 살 때 지금 주가보다 더 얹어 주는 값"},
                     {"term": "HBM", "plain": "고대역폭 메모리 — AI 칩 옆에 쌓아 붙이는 빠른 메모리"},
                     {"term": "ASI", "plain": "사람의 지능을 넘어서는 인공지능 (손정의의 표현)"},
                     {"term": "순현금", "plain": "회사가 가진 현금에서 빌린 돈을 뺀 것"},
                     {"term": "사전 승인", "plain": "외국인이 첨단 기술 회사를 사기 전에 정부 허락을 받는 절차"}],
        "scenes": S,
        "footage": fo,
        "package": {
            "title": "손정의는 왜 62% 빠진 SK하이닉스에 1조 달러를 생각했나",
            "title_options": ["손정의는 왜 62% 빠진 SK하이닉스에 1조 달러를 생각했나",
                              "SK하이닉스 1조 달러, 미친 값인가 싼 값인가 — 시장은 이익 -67%를 깔았다",
                              "손정의도 못 사는 회사 — SK하이닉스 앞의 세 벽"],
            "title_why": ["실험 E1: 이름 있는 사람 + 의외의 행동 질문형, 손정의·SK하이닉스·1조 달러 앞 20자 안, 역설(빠졌는데 웃돈) 하나",
                          "계산 결과를 내 계좌 말로", "세 벽 — 못 산다는 쪽"],
            "thumbnails": [
                {"id": "A", "name": "인물 — 손정의 얼굴 + 역설 숫자", "layout": "person", "image": {"file": "04_assets/footage/raw/sonface.jpg"},
                 "person": {"name": "손정의", "role": "소프트뱅크 회장"}, "top": "1조 달러 인수 검토",
                 "lines": ["62% 빠졌는데", "1조 달러?"], "hl": ["1조 달러?"], "credit": "사진: 위키미디어 공용 CC BY 2.0 (Masayoshi Son on July 11, 2008)",
                 "why": ["manual/09 §7-1 ⑥ 당사자 얼굴 크게 (docs/55)", "역설 한 문장 — 브리핑(증안펀드)과 다른 주인공"]},
                {"id": "B", "name": "숫자 대비 (dark)", "layout": "versus", "theme": "dark", "left": {"value": "-42%", "label": "1조 달러가 깐 이익 감소"},
                 "right": {"value": "-67%", "label": "시장이 깐 이익 감소"}, "headline": "SK하이닉스, 누가 맞나", "hl": ["누가"], "marks": [],
                 "why": ["계산 장의 결론 숫자 대비"]},
                {"id": "C", "name": "메모리 사진 + 세 벽 (photo full)", "layout": "photo", "photo_side": "full", "image": {"file": "04_assets/footage/raw/hynix.jpg", "focus": [0.5, 0.5]},
                 "top": "1조 달러 인수 검토", "lines": ["손정의도", "못 사는 회사"], "hl": ["못 사는"], "sub": "돈 · 법 · 주인", "size": 106, "text_y": 330, "marks": [],
                 "why": ["질문형 훅 후보 — 못 산다는 쪽"]}],
            "tags": ["손정의", "소프트뱅크", "SK하이닉스", "SK하이닉스 인수", "SK하이닉스 주가", "SK하이닉스 전망", "1조 달러", "HBM", "메모리 반도체",
                     "반도체 폭락", "PER", "저평가", "경영권 프리미엄", "Arm 인수", "SK스퀘어", "첨단전략산업법", "마이크론", "코스피", "심층 분석"],
            "hashtags": ["손정의", "SK하이닉스", "HBM"]},
    }
    (P / "02_script" / "hybrid.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
    print(P, len(S))


if __name__ == "__main__":
    main()
