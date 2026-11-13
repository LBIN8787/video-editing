"""이어 읽는 시장 — 11월 14일(토) 주간 분석: 11월 9~13일 (13일 미국·한국 마감 기준, 11/6 종가 대비).
    python -m ytflow daily --project 20261114-market-weekly
    python scripts/daily_20261114/make.py && python -m ytflow hybrid 20261114-market-weekly
"""
import json
import subprocess
import time
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from ytflow.stages import archive  # noqa: E402

P = ROOT / "projects" / "20261114-market-weekly"
AS_OF = "11월 13일 미국·한국 마감 기준 · 주간"
YH = "야후 파이낸스 종가 · 2026.11.6 → 11.13"
K8 = "엔비디아 8-K 공시·보도자료 (2026.11.11~12, SEC)"

PHOTOS = {  # 키: 위키미디어 공용 파일 이름 (CC BY·PD)
    "nvidia": "Nvidia sign.jpg",
    "nyse": "New York Stock Exchange Facade 2015.jpg",
    "fed": "Eccles Building (26088200676).jpg",
    "seoul": "Skyline of Yeouido, a prominent finance district in Seoul.jpg",
    "dc": "Microsoft Data Center Middenmeer, the Netherlands - 1.jpg",
}
KNOWN = {   # 위키미디어 조회가 막힐 때 (2026-11-14 검색 결과)
    "nvidia": {"license": "CC BY 2.0", "artist": "Will Buckner"},
    "nyse": {"license": "CC BY 2.0", "artist": "작자 미상"},
    "fed": {"license": "Public domain", "artist": "Federal Reserve"},
    "seoul": {"license": "CC BY 4.0", "artist": "작자 미상"},
    "dc": {"license": "CC BY 4.0", "artist": "Hay Kranen"},
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
            url = "https://commons.wikimedia.org/wiki/Special:FilePath/" + title.replace(" ", "_") + "?width=1920"   # 썸네일 서버는 429 가 잦음
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


def main():
    for d in ("01_research", "02_script", "05_edit"):
        (P / d).mkdir(parents=True, exist_ok=True)
    fo = photos()
    cr = {k: v["credit"].split(" · 위키미디어")[0] for k, v in fo.items()}
    S = []
    s = S.append
    s(dict(type="intro", chapter=0, series="이어 읽는 시장 · 주간 분석", as_of=AS_OF, bg_src="nyse", agenda_beat=3,
           title_lines=["반등한 한 주,", "왜 주인공만 빠졌나"],
           layers=[{"kind": "photo", "src": "nvidia", "beat": 2, "side": "right", "w": 600, "top": 250, "caption": f"엔비디아 간판 · {cr['nvidia']}"}],
           beats=B("안녕하세요. 어제의 시장을 이어 읽는, 이어 읽는 시장입니다.",
                   "토요일은 한 주를 정리하는 주간 분석입니다. 11월 9일부터 13일까지, 13일 미국과 한국 장 마감 기준으로 정리합니다.",
                   "지난주 목요일, 반도체 지수는 하루에 12% 넘게 빠졌습니다. 이번 주에는 그중 상당 부분을 되찾았죠. 그런데 그 한가운데 있던 엔비디아만, 한 주 동안 13% 가까이 내렸습니다. 반등하는 시장에서, 왜 주인공만 빠졌을까요?",
                   "이번 주를 움직인 흐름 세 가지를 보겠습니다. 급락 뒤의 되돌림, 엔비디아의 빈자리와 돈의 이동, 그리고 다시 오르는 금리와 연준의 AI 경고입니다. 마지막엔 한국 시장과 다음 주 일정까지 정리합니다.",
                   "시작하겠습니다.")))
    s(dict(type="bars", chapter=0, label=YH, title="이번 주 등락 (%, 지난주 금요일 종가 대비)", unit="", emph=2,
           layers=[{"kind": "locator", "at": [-74.0, 40.71], "label": "미국 뉴욕 · 11월 13일 마감", "beat": 0, "side": "left", "top": 170, "scale": 2.2}],
           items=[{"label": "S&P 500", "value": 2.51, "text": "+2.51"}, {"label": "나스닥", "value": 2.27, "text": "+2.27"},
                  {"label": "반도체 지수", "value": 8.05, "text": "+8.05"}, {"label": "코스피", "value": 4.56, "text": "+4.56"}],
           beats=B("먼저 한 주 숫자입니다. 지난주 금요일 종가와 비교하면, S&P 500은 2.51%, 나스닥은 2.27% 올랐습니다.",
                   "반도체 지수는 8.05%, 코스피는 4.56% 올랐습니다. 지난주에 가장 크게 빠졌던 곳이, 이번 주에 가장 크게 되돌린 한 주였습니다.")))
    # 1. 급락 뒤 되돌림
    s(dict(type="chapter", chapter=1, num="1", title="급락 뒤의 되돌림", icon="trending-up", look="photo", bg_src="nyse",
           beats=B("첫 번째 흐름, 급락 뒤의 되돌림입니다. 이번 주를 이해하려면, 지난주 목요일부터 봐야 합니다.")))
    s(dict(type="chart", chapter=1, label="야후 파이낸스 필라델피아 반도체 지수 일별 종가 (^SOX) · 2026.11.13 기준", ticker="^SOX", period="1mo", title="필라델피아 반도체 지수",
           beats=[{"say": "반도체 지수의 한 달 흐름입니다. 11월 5일 목요일, 이 지수는 하루에 12.25% 떨어졌습니다. 지수에 든 30개 종목이 모두 내렸죠. 같은 날 S&P 500은 4.4%, 코스피는 5.3% 빠졌습니다.", "focus_last": 6, "mark": "주간 +8.05%"},
                  {"say": "이번 주에는 월요일 하루에만 6.85% 오르는 등, 한 주 동안 8.05%를 되찾았습니다. 다만 13일 종가 10,146.32는, 급락 직전인 4일의 10,268.65에는 아직 못 미칩니다."}]))
    s(dict(type="checklist", chapter=1, label="AP 보도 (2026.11.5) · 파이낸셜뉴스 (2026.11.10)", title="지난주 급락, 무엇이 겹쳤나", fx=["tilt"], x=150, text_w=860,
           layers=[{"kind": "photo", "src": "nyse", "beat": 0, "side": "right", "w": 440, "top": 620, "caption": f"뉴욕증권거래소 · {cr['nyse']}"}],
           rows=[{"label": "비싸진 대출 → AI 데이터센터 건설이 느려질 수 있다는 걱정", "state": "warn"},
                 {"label": "중간선거 결과 → 데이터센터 건설 제한 가능성", "state": "warn"},
                 {"label": "AI 주가가 너무 올랐다는 거품 논쟁", "state": "warn"},
                 {"label": "이번 주 월요일: 많이 빠진 반도체에 저가 매수", "state": "ok"}],
           beats=[{"say": "보도들은 지난주 급락의 배경으로 세 가지를 꼽았습니다. 대출이 비싸지면서 AI 데이터센터 건설이 느려질 수 있다는 걱정, 중간선거 결과로 데이터센터 건설이 제한될 수 있다는 우려, 그리고 AI 주가가 너무 올랐다는 거품 논쟁입니다.", "upto": 3},
                  {"say": "그리고 이번 주 월요일 반등은, 많이 빠진 반도체에 저가 매수가 들어온 결과로 보도됐습니다. 세 가지 걱정 가운데 풀렸다고 확인된 것은, 아직 없습니다.", "upto": 4}]))
    s(dict(type="analogy", chapter=1, label="자체 정리 (비유) · 여기서부터는 해석입니다", title="되돌림 vs 걱정 해소",
           left={"icon": "arrow-up", "label": "눌린 용수철", "sub": "손을 조금만 떼도 튀어 오름"}, right={"icon": "hand", "label": "누르던 손", "sub": "금리·규제·거품 걱정은 그대로"},
           result={"icon": "circle-alert", "label": "반등 = 가격 되돌림일 수 있다 (걱정 해소와 다름)"},
           beats=[{"say": "여기서부터는 해석입니다. 세게 눌린 용수철은, 손을 조금만 떼도 튀어 오릅니다. 이번 주 반등이 그런 모습에 가깝습니다."},
                  {"say": "하지만 용수철을 누르던 손, 그러니까 금리와 규제, 거품에 대한 걱정은 아직 그대로 있죠. 그래서 이번 주 반등을, 걱정이 끝났다는 신호로 읽기는 이릅니다.", "show_result": True}]))
    # 2. 엔비디아의 빈자리
    s(dict(type="chapter", chapter=2, num="2", title="엔비디아의 빈자리", icon="git-branch", look="dash",
           beats=B("두 번째 흐름입니다. 반도체가 되살아난 한 주, 엔비디아는 왜 반대로 갔을까요?")))
    s(dict(type="versus", chapter=2, label=YH, fx=["tilt"],
           left={"value": "+18.93%", "label": "AMD (브로드컴 +18.16%)", "icon": "trending-up"}, right={"value": "-12.75%", "label": "엔비디아", "icon": "trending-down"},
           beats=B("한 주 성적표입니다. AMD는 18.93%, 브로드컴은 18.16% 올랐습니다. 반면 엔비디아는 186.64달러에서 162.85달러로, 12.75% 내렸습니다.",
                   "같은 반도체 지수 안에서, 한쪽은 20% 가까이 오르고 한쪽은 13% 가까이 빠졌습니다. 업종 전체가 아니라, 엔비디아 한 회사의 이야기였다는 뜻이죠.")))
    s(dict(type="chart", chapter=2, label="야후 파이낸스 엔비디아 일별 종가 (NVDA) · 2026.11.13 기준", ticker="NVDA", period="1mo", title="엔비디아 주가 (달러)",
           beats=[{"say": "날짜별로 보면, 월요일에는 이사회가 최고경영자 관련 보도를 조사한다는 소식에 4.27%, 화요일에 5.47% 내렸습니다.", "focus_last": 5, "mark": "주간 -12.75%"},
                  {"say": "11일 장 마감 뒤에는 공시가 나왔습니다. 젠슨 황이 사장과 CEO, 이사직에서 즉시 물러나고, 콜레트 크레스 최고재무책임자가 임시 CEO를 맡는다는 내용이었죠. 엔비디아는 12일 4.34%, 13일 2.01% 더 내렸습니다."}]))
    s(dict(type="bars", chapter=2, label="야후 파이낸스 종가 · 2026.11.12 → 11.13", title="13일 금요일, 반도체가 다시 꺾이다 (%)", unit="", emph=0, fx=["scan"],
           items=[{"label": "AMD", "value": 8.75, "text": "-8.75"}, {"label": "브로드컴", "value": 4.76, "text": "-4.76"},
                  {"label": "반도체 지수", "value": 3.43, "text": "-3.43"}, {"label": "엔비디아", "value": 2.01, "text": "-2.01"}],
           beats=B("그런데 13일 금요일에는 시장 전체가 약했습니다. S&P 500은 0.40%, 나스닥은 0.91% 내렸고, 반도체 지수는 3.43% 빠졌습니다. 특히 AMD가 8.75%, 브로드컴이 4.76% 내리면서, 엔비디아의 2.01%보다 더 크게 빠졌습니다.",
                   "보도들은 전날 급등한 만큼 차익을 실현한 매물, 그리고 엔비디아 쪽으로 다시 돌아오는 매수를 이유로 들었습니다. 브로드컴은 한 증권사가 고객 쏠림을 이유로 투자의견을 중립으로 낮췄다는 소식도 겹쳤습니다.")))
    s(dict(type="map_causal", chapter=2, look="board", label="자체 해석 · 근거: 엔비디아 8-K, 보도, 11월 9~13일 시세",
           beats=[{"say": "여기서부터는 해석입니다. 한 장으로 이어 보면, 창업자가 떠나면서 리더십에 빈자리가 생겼고, 돈은 하루 이틀 대안으로 쏠렸다가, 금요일에 일부 되돌아왔습니다.",
                   "reveal": ["ceo", "gap", "alt", "back"], "draw": [["ceo", "gap"], ["gap", "alt"], ["alt", "back"]], "active": "back"},
                  {"say": "주가는 기대를 먼저 움직이지만, 실제 칩 주문은 몇 달, 몇 년 단위로 움직입니다. 그래서 이 쏠림이 진짜 주문의 이동인지는, 다음 주 실적 발표가 처음으로 보여 줄 겁니다.",
                   "reveal": ["earn"], "draw": [["gap", "earn"], ["back", "earn"]], "active": "earn"}]))
    # 3. 다시 오르는 금리
    s(dict(type="chapter", chapter=3, num="3", title="금리, 그리고 연준의 AI 경고", icon="landmark", look="photo", bg_src="fed",
           beats=B("세 번째 흐름은 금리, 그리고 연준이 보낸 신호입니다. 주식이 오른 한 주, 채권 시장과 연준에서는 다른 신호가 나왔습니다.")))
    s(dict(type="versus", chapter=3, label="야후 파이낸스 미국 10년물 국채 금리 (^TNX) · 2026.11.6 → 11.13", fx=["dolly"],
           left={"value": "4.86%", "label": "지난주 금요일", "icon": "calendar"}, right={"value": "5.15%", "label": "이번 주 금요일", "icon": "trending-up"},
           beats=B("미국 10년물 국채 금리는 한 주 동안 4.86%에서 5.15%로 올랐습니다. 지난주 급락 때 잠깐 내려갔던 금리가, 다시 5%대로 올라선 거죠.",
                   "같은 한 주, 금값은 4.74%, 비트코인은 9.40% 내렸습니다. 이자가 붙지 않는 자산들이 함께 약했던 한 주였습니다.")))
    s(dict(type="checklist", chapter=3, label="미국 노동통계국 PPI (2026.11.13) · 연준 성명 (2026.10.28)", title="물가와 연준, 확인된 것", fx=["scan"], x=150, text_w=860,
           layers=[{"kind": "photo", "src": "fed", "beat": 0, "side": "right", "w": 440, "top": 620, "caption": f"연준 에클스 빌딩 · {cr['fed']}"}],
           rows=[{"label": "10월 생산자물가: 한 달 +0.3%, 1년 전보다 +6.5%", "state": "warn"},
                 {"label": "그중 에너지: 1년 전보다 +37.0%", "state": "warn"},
                 {"label": "연준: 9월 0.25%p 인상 → 10월 3.75~4% 동결", "state": "ok"},
                 {"label": "10월 회의: 12명 중 2명은 인상 주장", "state": "warn"}],
           beats=[{"say": "금요일 아침에 나온 10월 생산자물가는, 한 달 동안 0.3% 올랐습니다. 1년 전과 비교하면 6.5%나 높고, 그중 에너지 가격은 1년 새 37% 올랐습니다.", "upto": 2},
                  {"say": "연준은 9월에 금리를 0.25%포인트 올린 뒤, 10월에는 3.75에서 4% 사이로 동결했습니다. 성명은 물가가 여전히 높다고 적었고, 12명 가운데 2명은 한 번 더 올리자고 했습니다.", "upto": 4}]))
    s(dict(type="quote", chapter=3, label="연준 FOMC 성명 (2026.10.28)", fx=["dolly"], who="연방공개시장위원회", role="10월 28일 성명",
           quote="물가는 여전히 높다. 위원회는 물가 안정을 이뤄 낼 것이다.", keyword="여전히 높다",
           orig="Inflation remains elevated. ... The Committee will deliver price stability.",
           beats=B("성명의 문장은 짧았습니다. 물가는 여전히 높고, 위원회는 물가 안정을 이뤄 내겠다.",
                   "금리를 내릴 이유보다 올릴 이유를 먼저 적은 셈입니다. 그리고 13일 금요일, 연준은 문서를 하나 더 냈습니다. 1년에 두 번 내는 금융안정보고서입니다.")))
    s(dict(type="quote", chapter=3, label="연준 금융안정보고서 (2026.11.13)", fx=["scan"], who="미국 연방준비제도", role="금융안정보고서 · 11월 13일",
           quote="주가 수준은 여전히 높다. 일부는 '초지능'에 대한 시장의 열광 때문이다.", keyword="열광",
           orig="Measures of equity valuations have remained high, partly driven by market enthusiasm for super intelligence (SI).",
           beats=B("보고서의 첫 요약은 이렇습니다. 주가 수준은 여전히 높고, 그 일부는 초지능, 그러니까 사람을 뛰어넘는 AI에 대한 시장의 열광 때문이다.",
                   "연준이 지금의 주가에 AI 기대가 얹혀 있다고, 공식 문서에 적은 겁니다.")))
    s(dict(type="checklist", chapter=3, label="연준 금융안정보고서 (2026.11.13) · 설문은 연준의 공식 견해가 아님", title="연준 보고서가 AI에 대해 적은 것", fx=["tilt"], x=150, text_w=860,
           layers=[{"kind": "photo", "src": "dc", "beat": 0, "side": "right", "w": 440, "top": 620, "caption": f"데이터센터 · {cr['dc']}"}],
           rows=[{"label": "시장 참가자 23곳 설문: 가장 많이 꼽은 위험 = AI", "state": "warn"},
                 {"label": "걱정 ①: 큰 투자에 비해 불확실한 수익 → AI 주식 급락 가능성", "state": "warn"},
                 {"label": "걱정 ②: AI를 이용한 사이버 공격", "state": "warn"},
                 {"label": "AI 컴퓨팅 채권 발행: 올해 10월까지 6,800억 달러+ (2023년의 약 5배)", "state": "warn"}],
           beats=[{"say": "보고서에 실린 설문에서, 뉴욕 연은이 만난 시장 참가자 23곳이 가장 많이 꼽은 위험이 바로 AI였습니다. 큰 투자에 비해 수익이 불확실해 AI 주식이 급하게 떨어질 수 있다는 걱정, 그리고 AI를 이용한 사이버 공격입니다. 다만 설문 응답은 연준의 공식 견해는 아니라고 보고서는 밝혔습니다.", "upto": 3},
                  {"say": "보고서는 또, 데이터센터 같은 AI 컴퓨팅에 쓰려고 낸 채권이 올해 10월까지 6,800억 달러를 넘었다고 적었습니다. 2023년 한 해 1,300억 달러의 약 다섯 배입니다.", "upto": 4}]))
    s(dict(type="analogy", chapter=3, label="자체 해석 · 근거: 연준 금융안정보고서, AP 보도(11.5), 11월 13일 시세", title="지난주의 걱정 = 연준의 위험 목록",
           left={"icon": "trending-down", "label": "지난주의 걱정", "sub": "AI 투자 수익 · 비싼 빚 · 거품"}, right={"icon": "landmark", "label": "연준 위험 1순위", "sub": "AI 주가 급락 · AI 관련 빚"},
           result={"icon": "circle-alert", "label": "반등했지만, 걱정의 목록은 그대로"},
           beats=[{"say": "여기서부터는 해석입니다. 이 보고서가 금요일 주가를 움직였다고 확인된 건 아닙니다."},
                  {"say": "다만 지난주 급락 때 시장이 걱정한 것, 그러니까 AI 투자가 돈을 벌어 줄지, 그리고 그 투자를 받치는 빚의 문제를, 연준도 같은 날 위험 목록 맨 위에 올린 셈입니다. 그래서 시장은 다음 주 10월 회의 의사록과 엔비디아 실적을, 같은 질문으로 보게 됩니다.", "show_result": True}]))
    # 4. 한국 시장
    s(dict(type="chapter", chapter=4, num="4", title="한국 시장의 한 주", icon="trending-up", look="board",
           beats=B("이제 한국 시장입니다. 한국은 지난주에 더 크게 빠졌고, 이번 주에 더 크게 되돌렸습니다.")))
    s(dict(type="bars", chapter=4, label="야후 파이낸스 종가 · 아주경제·MTN 마감 보도 · 2026.11.6 → 11.13", title="한국 이번 주 등락 (%)", unit="", emph=3,
           layers=[{"kind": "locator", "at": [126.98, 37.57], "label": "서울 · 11월 13일 마감", "beat": 0, "side": "left", "top": 170, "scale": 2.2}],
           items=[{"label": "코스피", "value": 4.56, "text": "+4.56"}, {"label": "삼성전자", "value": 9.17, "text": "+9.17"},
                  {"label": "SK하이닉스", "value": 7.42, "text": "+7.42"}, {"label": "NAVER", "value": 9.31, "text": "-9.31"}],
           beats=B("코스피는 한 주 동안 4.56% 올라 5,290.53에 마감했습니다. 삼성전자는 9.17%, SK하이닉스는 7.42% 올랐습니다.",
                   "반대로 네이버는 9.31% 내렸습니다. 엔비디아와 AI 협력을 키워 온 회사라, 엔비디아 소식에 함께 흔들린 것으로 보도됐습니다.")))
    s(dict(type="bars", chapter=4, label="야후 파이낸스 종가 · 아주경제 마감시황 (2026.11.13)", title="코스피 날짜별 등락 (%)", unit="", emph=5, fx=["tilt"],
           items=[{"label": "6일(금)", "value": 6.02, "text": "-6.02"}, {"label": "9일", "value": 0.81, "text": "-0.81"},
                  {"label": "10일", "value": 4.39, "text": "+4.39"}, {"label": "11일", "value": 2.60, "text": "+2.60"},
                  {"label": "12일", "value": 0.61, "text": "-0.61"}, {"label": "13일", "value": 0.98, "text": "-0.98"}],
           beats=B("날짜별로 보면, 지난주 금요일 코스피는 하루에 6.02% 빠졌고, 이번 주 월요일에도 0.81% 더 내렸습니다. 그 뒤 화요일 4.39%, 수요일 2.60% 오르며 미국의 반등을 따라갔죠.",
                   "하지만 엔비디아 사임 소식 뒤 이틀은 연속으로 내렸습니다. 13일에는 장중 5,500을 넘었다가, 외국인이 5천억 원 넘게 팔면서 0.98% 내린 채 마감했습니다.")))
    s(dict(type="kinetic", chapter=4, beats=[{"say": "되돌림은 빨랐고, 이제 숫자가 답할 차례입니다.", "hit": ["빨랐고,", "숫자가"]}]))
    s(dict(type="checklist", chapter=4, label="11월 14일 기준 일정 (한국 시간) · 투자 권유가 아닙니다", title="다음 주 볼 것", fx=["dolly"],
           rows=[{"label": "18일(수) 새벽 6시 20분 — 엔비디아 3분기 실적, 임시 CEO 체제 첫 발표", "state": "warn"},
                 {"label": "19일(목) 새벽 4시 — 연준 10월 회의 의사록 (예정)", "state": "warn"},
                 {"label": "12월 8~9일 — 연준 회의, 경제 전망과 함께", "state": "warn"}],
           beats=[{"say": "다음 주 볼 것은 세 가지입니다. 먼저 한국 시간 18일 수요일 새벽 6시 20분, 엔비디아 3분기 실적입니다. 임시 CEO 체제에서 나오는 첫 실적이죠.", "upto": 1},
                  {"say": "다음 날인 19일 새벽 4시에는 연준 10월 회의 의사록이 나올 예정입니다. 그리고 그 뒤에는 12월 8일과 9일 연준 회의가 기다리고 있습니다. 세 흐름 모두, 이 일정들에서 첫 답을 듣게 됩니다.", "upto": 3}]))
    s(dict(type="outro", chapter=4, title="이어 읽는 시장", sub="11월 13일 마감 기준 · 출처는 설명란에", clip={"src": "nyse", "start": 0},
           beats=B("오늘 이어 읽는 시장은 여기까지입니다. 출처는 모두 설명란에 남겨 두겠습니다.")))
    for i, x in enumerate(S, 1):
        x["id"] = i
    spec = {
        "title": "반등한 한 주, 왜 주인공만 빠졌나 — 11월 9~13일 주간 분석",
        "brand": "market",
        "core_message": "지난주 급락 뒤 이번 주 반도체는 8% 되돌렸지만 엔비디아만 리더십 공백으로 13% 가까이 빠졌고, 금리는 다시 5%대로 올랐다. 반등은 걱정 해소가 아니라 가격 되돌림에 가깝다. 13일 연준 금융안정보고서도 AI를 금융 시장의 가장 큰 위험으로 꼽았고, 다음 주 엔비디아 실적과 연준 의사록이 첫 답을 준다.",
        "question": "반도체가 되돌린 한 주, 왜 엔비디아만 빠졌을까?",
        "logic": ["주간: S&P +2.51%, 나스닥 +2.27%, 반도체 지수 +8.05%, 코스피 +4.56% (11/6 종가 대비)",
                  "1) 11/5 반도체 -12.25% 급락(데이터센터·선거·거품 걱정, 보도) → 이번 주 저가 매수로 되돌림, 아직 11/4 수준 아래",
                  "2) 엔비디아 -12.75% (조사 보도 → 11/11 CEO 즉시 사임 8-K) vs AMD +18.93%·브로드컴 +18.16% → 13일 되돌림(AMD -8.75%)",
                  "3) 10년물 4.86%→5.15%, 10월 PPI 12개월 +6.5%, 연준 10월 동결(2명 인상 주장), 13일 금융안정보고서: 주가에 AI 열광, 설문 위험 1순위 AI, AI 컴퓨팅 채권 6,800억 달러+",
                  "한국: 코스피 +4.56%, 삼성전자 +9.17%, SK하이닉스 +7.42%, 네이버 -9.31%, 13일 외국인 매도로 -0.98%",
                  "다음 주: 18일 06:20 엔비디아 실적, 19일 04:00 연준 의사록, 12월 8~9일 FOMC"],
        "compare_to": [{"value": "반도체 지수 주간 +8.05%", "to": "11/5 하루 -12.25%, 11/4 종가 10,268.65"},
                       {"value": "엔비디아 -12.75%", "to": "AMD +18.93% (같은 업종)"},
                       {"value": "10년물 5.15%", "to": "지난주 금요일 4.86%"},
                       {"value": "PPI +6.5%", "to": "1년 전 같은 달"}],
        "analogies": [{"a": "눌린 용수철", "b": "세게 눌린 가격은 손만 조금 떼도 튀어 오르지만, 누르던 손(걱정)은 그대로"},
                      {"a": "하루 주가와 주문서", "b": "주가는 기대가 먼저, 칩 주문은 몇 달·몇 년 단위"}],
        "past_cases": [{"case": "2026년 11월 5일 반도체 지수 -12.25%, S&P -4.4%", "lesson": "급락 다음 주의 큰 반등이 곧 걱정 해소를 뜻하지는 않는다"}],
        "glossary": [{"term": "필라델피아 반도체 지수", "plain": "미국에 상장된 주요 반도체 회사 30곳의 주가를 묶은 지수"},
                     {"term": "생산자물가(PPI)", "plain": "기업이 물건·서비스를 팔 때 받는 값의 변화. 소비자 물가보다 먼저 움직이기도 함"},
                     {"term": "의사록", "plain": "연준 회의에서 오간 논의를 3주 뒤에 정리해 공개하는 기록"},
                     {"term": "차익 실현", "plain": "오른 주식을 팔아 이익을 확정하는 것"}],
        "scenes": S,
        "map": {"nodes": {"ceo": {"label": "창업자 CEO 즉시 사임", "icon": "user", "x": 300, "y": 360},
                          "gap": {"label": "리더십 빈자리", "icon": "circle-alert", "x": 800, "y": 360},
                          "alt": {"label": "대안으로 쏠림: AMD·브로드컴", "icon": "trending-up", "x": 1300, "y": 360},
                          "back": {"label": "13일 되돌림 (차익 실현)", "icon": "trending-down", "x": 1620, "y": 760},
                          "earn": {"label": "첫 시험대: 18일 새벽 실적", "icon": "calendar", "x": 800, "y": 760}},
                "edges": [["ceo", "gap"], ["gap", "alt"], ["alt", "back"], ["gap", "earn"], ["back", "earn"]]},
        "footage": fo,
        "package": {
            "title": "반도체 반등한 한 주, 왜 주인공만 빠졌나 | 11월 14일 이어 읽는 시장",
            "title_options": ["반도체 반등한 한 주, 왜 주인공만 빠졌나 | 11월 14일 이어 읽는 시장",
                              "반도체 +8.05% · 엔비디아 -12.75% · 금리 5.15% — 이번 주 시장 세 흐름",
                              "급락 뒤 되돌림, 엔비디아의 빈자리, 다시 오르는 금리 (주간 분석·다음 주 일정)"],
            "title_why": ["훅(반등장에서 주인공만 하락)에서 — 답은 숨김", "숫자 대비 셋", "장면 + 다룬 흐름"],
            "thumbnails": [
                {"id": "A", "name": "엔비디아 간판 + 질문", "layout": "photo", "photo_side": "full", "image": {"file": "04_assets/footage/raw/nvidia.jpg", "focus": [0.5, 0.5]},
                 "top": "11월 14일 이어 읽는 시장 · 주간", "lines": ["반등한 한 주", "왜 주인공만 빠졌나"], "hl": ["주인공만"], "sub": "반도체 · 엔비디아 · 금리", "size": 116, "text_y": 330, "marks": [],
                 "why": ["장면 + 질문"]},
                {"id": "B", "name": "숫자 대비", "layout": "versus", "left": {"value": "+8.05%", "label": "반도체 지수"},
                 "right": {"value": "-12.75%", "label": "엔비디아"}, "headline": "같은 한 주, 반대 방향", "hl": [], "marks": [], "why": ["숫자 둘이 질문"]},
                {"id": "C", "name": "다음 주 일정", "layout": "photo", "photo_side": "full", "image": {"file": "04_assets/footage/raw/fed.jpg", "focus": [0.5, 0.5]},
                 "top": "다음 주 볼 것", "lines": ["18일 엔비디아 실적,", "19일 연준 의사록"], "hl": ["18일", "19일"], "sub": "금리 5.15%", "size": 110, "text_y": 330, "marks": [],
                 "why": ["다음 일정"]}]},
    }
    (P / "02_script" / "hybrid.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
    print(P, len(S))


if __name__ == "__main__":
    main()
