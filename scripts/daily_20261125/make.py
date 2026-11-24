"""이어 읽는 시장 — 11월 25일(수) 아침 브리핑: 젠슨 황이 돌아온 다음 날 — 반도체 -7.88%, 엔비디아는 지키고 사슬은 돌려줬다 + 코스피 5,000 회복 뒤 오늘 첫 반영.
    python scripts/daily_20261125/make.py && python -m ytflow hybrid 20261125-market-daily
"""
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from ytflow.stages import archive  # noqa: E402

P = ROOT / "projects" / "20261125-market-daily"
DS, NP = "dark-doc", "newsprint"
YH = "야후 파이낸스 종가 · 11월 24일(화) 미국 마감 기준 (한국 25일 06:00)"
KR = "한국거래소 종가(야후) · 코스피는 보도 4곳(조선비즈·연합뉴스TV·MBC·연합인포맥스) · 11월 24일(화) 15:30 마감 — 미국 화요일 장 전"
K8 = "인스메드 8-K 보도자료 (SEC, 2026.11.24)"
CFO = "엔비디아 3분기 CFO 코멘터리 (SEC, 2026.11.17)"

PHOTOS = {
    "nyse": "New York Stock Exchange Facade 2015.jpg",
    "seoul": "Skyline of Yeouido, a prominent finance district in Seoul.jpg",
    "jensen_huang_face": "Jensen huang stanford 2026-04-30 005.jpg",
}
KNOWN = {
    "nyse": {"license": "CC BY 2.0", "artist": "작자 미상"},
    "seoul": {"license": "CC BY 4.0", "artist": "S h y numis"},
    "jensen_huang_face": {"license": "CC BY 4.0", "artist": "Anders Eidesvik"},
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
    CALC = "이 영상의 계산 · 야후 파이낸스 종가 11월 20일(금)·23일(월)·24일(화) · (23일 − 24일) ÷ (23일 − 20일)"

    # ── 여는 장면: 같은 화요일, 반대 방향 ──
    s(dict(type="versus", chapter=0, label=KR + " · " + YH,
           left={"value": "+6.32%", "label": "코스피 (24일 화) 5,006", "icon": "trending-up"},
           right={"value": "-7.88%", "label": "미국 반도체 지수 (24일 화)", "icon": "trending-down"},
           beats=[{"say": "어제 화요일, 코스피는 젠슨 황의 복귀 소식을 받고 6.32% 올라 5,000선을 되찾았습니다. 그런데 몇 시간 뒤 같은 화요일 미국의 반도체 지수는 7.88% 빠졌습니다."},
                  {"say": "황이 돌아온 지 하루 만입니다. 그런데 이상한 점이 있습니다. 엔비디아는 5.86% 내렸는데, 엔비디아에 메모리를 대는 마이크론은 11% 넘게 빠졌습니다. 주인공보다 주변이 두 배 가까이 더 흔들린 겁니다. 왜 그랬을까요?",
                   "motion": [M("5.86%", "count", id="o1", value="엔비디아 -5.86%", label="24일 종가", x=560, y=880, w=440, h=140, fs=46), M("11%", "count", id="o2", value="마이크론 -11.01%", label="24일 종가", x=1360, y=880, w=440, h=140, fs=46)]}]))

    # ── 시장 한 장 ──
    s(dict(type="bars", chapter=0, label=YH, title="24일(화) 미국 마감 (%)", unit="", emph=3, skin=DS,
           items=[{"label": "다우", "value": 0.85, "text": "+0.85", "t": "다우는"}, {"label": "S&P 500", "value": -0.50, "text": "-0.50", "t": "S&P"},
                  {"label": "나스닥", "value": -1.48, "text": "-1.48", "t": "나스닥은"}, {"label": "미국 반도체 지수", "value": -7.88, "text": "-7.88", "t": "반도체"}],
           beats=[{"say": "숫자부터 보겠습니다. 11월 24일 화요일 미국 장 마감 기준, 다우는 0.85% 올라 50,018로 5만 선을 다시 넘었습니다. S&P 500은 0.50%, 나스닥은 1.48% 내렸습니다.",
                   "motion": [M("50,018로", "count", id="dj", value="50,018.70", label="다우 24일 종가", x=1600, y=420, w=420, h=150, fs=52)]},
                  {"say": "무너진 곳은 한 군데였습니다. 반도체 지수가 7.88% 빠졌습니다. 시장 전체가 아니라 반도체의 하루였다는 뜻입니다. 미국 10년물 국채 금리는 4.90%로 거의 그대로였습니다.",
                   "motion": [M("7.88%", "count", id="sx", value="8,832.5", label="반도체 지수 24일 종가", x=1600, y=860, w=420, h=150, fs=52)]}]))

    # ── 1. 되돌림 ──
    s(dict(type="chapter", chapter=1, num="1", title="주인공은 지켰고, 사슬은 돌려줬다", icon="undo-2", look="photo", bg_src="jensen_huang_face",
           beats=B("첫 번째, 무엇이 얼마나 빠졌는지입니다. 같은 반도체 사슬이라도 빠진 폭이 크게 갈렸습니다.")))
    s(dict(type="bars", chapter=1, label=YH, title="24일(화) 종가 등락 (%)", unit="", emph=0, skin=DS,
           items=[{"label": "코어위브 (엔비디아 고객)", "value": -11.86, "text": "-11.86", "t": "코어위브는"}, {"label": "델 (서버)", "value": -11.83, "text": "-11.83", "t": "델은"},
                  {"label": "마이크론 (메모리 공급)", "value": -11.01, "text": "-11.01", "t": "마이크론은"}, {"label": "AMD (경쟁)", "value": -8.86, "text": "-8.86", "t": "AMD도"},
                  {"label": "엔비디아", "value": -5.86, "text": "-5.86", "t": "엔비디아는"}, {"label": "TSMC (생산)", "value": -3.96, "text": "-3.96", "t": "TSMC는"}],
           beats=[{"say": "엔비디아 칩을 빌려주는 코어위브는 11.86%, 서버를 만드는 델은 11.83%, 메모리를 대는 마이크론은 11.01% 내렸습니다. 경쟁사 AMD도 8.86% 빠졌습니다."},
                  {"say": "엔비디아는 5.86% 내린 155.38달러, 칩을 만들어 주는 TSMC는 3.96% 내렸습니다. 보도들은 전날 급등 뒤의 차익 실현으로 설명했고, 회사들에서 새로 나온 나쁜 소식은 확인되지 않았습니다.",
                   "motion": [M("155.38", "count", id="nv", value="155.38달러", label="엔비디아 24일 종가", x=1600, y=860, w=420, h=150, fs=52)]}]))
    s(dict(type="bars", chapter=1, label=CALC, title="월요일에 오른 만큼 중 화요일에 돌려준 몫 (%)", unit="", emph=0, skin=DS,
           items=[{"label": "엔비디아", "value": 24, "text": "24%", "t": "엔비디아는"}, {"label": "TSMC", "value": 32, "text": "32%", "t": "TSMC도"},
                  {"label": "코어위브", "value": 65, "text": "65%", "t": "코어위브는"}, {"label": "마이크론", "value": 69, "text": "69%", "t": "마이크론은"},
                  {"label": "델", "value": 70, "text": "70%", "t": "델은"}, {"label": "AMD (금요일 아래로)", "value": 138, "text": "138%", "t": "AMD는"}],
           beats=[{"say": "그래서 직접 계산해 봤습니다. 월요일에 오른 만큼 가운데, 화요일에 얼마를 돌려줬는지입니다. 엔비디아는 24%만 돌려줬습니다. 오른 몫의 4분의 3을 지킨 겁니다. 칩을 만드는 TSMC도 32%만 돌려줬습니다.",
                   "motion": [M("4분의 3을", "count", id="k76", value="76% 지킴", label="엔비디아 (계산)", x=1600, y=420, w=420, h=150, fs=52)]},
                  {"say": "반면 코어위브는 65%, 마이크론은 69%, 델은 70%를 돌려줬습니다. 그리고 AMD는 오른 것보다 더 빠져, 금요일 종가보다도 낮아졌습니다. 브로드컴도 마찬가지입니다.",
                   "motion": [M("69%를", "count", id="mu", value="69% 반납", label="마이크론 (계산)", x=1600, y=860, w=420, h=150, fs=52)]}]))
    s(dict(type="motionboard", chapter=1, label="이 영상의 설명 · 근거: 야후 종가 11월 20·23·24일, 돌려준 몫은 이 영상의 계산", title="화요일에 시장이 한 일",
           els={"nv": {"kind": "card", "x": 960, "y": 600, "icon": "cpu", "label": "엔비디아", "value": "76% 지킴", "vsize": 44, "w": 340},
                "mu": {"kind": "card", "x": 400, "y": 300, "icon": "memory-stick", "label": "마이크론", "value": "69% 반납", "vsize": 40, "w": 320},
                "cw": {"kind": "card", "x": 1520, "y": 300, "icon": "server", "label": "코어위브·델", "value": "65~70% 반납", "vsize": 40, "w": 360},
                "amd": {"kind": "card", "x": 1520, "y": 860, "icon": "swords", "label": "AMD·브로드컴", "value": "금요일 아래", "vsize": 40, "w": 360},
                "a1": {"kind": "arrow", "from": "nv", "to": "mu", "label": "함께 실려 오름"},
                "a2": {"kind": "arrow", "from": "nv", "to": "cw", "label": "함께 실려 오름"},
                "big": {"kind": "text", "x": 960, "y": 170, "text": "소식은 남기고, 덤은 돌려줬다", "size": 50, "color": "red"}},
           beats=[{"say": "그림으로 보면 이렇습니다. 시장은 황의 복귀라는 소식 자체는 대부분 남겨 뒀습니다. 엔비디아가 오른 몫의 76%를 지켰으니까요.", "do": ["nv"], "at": {"nv": "소식"}},
                  {"say": "되돌린 건 그 소식에 함께 실려 올랐던 주변입니다. 큰 손님이 돌아왔다고 하루 만에 가게들까지 값을 크게 올렸다가, 다음 날 그 덤을 거의 다 내려놓은 셈입니다.", "do": ["mu", "a1", "cw", "a2"], "at": {"mu": "함께", "cw": "주변입니다"}},
                  {"say": "그리고 경쟁사는, 황이 없는 엔비디아라는 기회가 사라지자 금요일보다 낮아졌습니다. 이건 사실이 아니라 숫자에서 읽은 해석입니다.", "do": ["amd", "big", {"hi": "nv"}], "at": {"amd": "경쟁사는", "big": "해석"}}]))

    # ── 2. 돈은 옮겨 갔다 ──
    s(dict(type="chapter", chapter=2, num="2", title="돈은 떠나지 않고 옮겨 갔다", icon="arrow-right-left", look="board",
           beats=B("두 번째, 반도체에서 빠진 돈이 시장을 떠났는지입니다. 숫자는 아니라고 말합니다.")))
    s(dict(type="bars", chapter=2, label=YH + " · 미국 업종 ETF", title="24일(화) 업종 (%)", unit="", emph=0, skin=DS,
           items=[{"label": "헬스케어", "value": 2.95, "text": "+2.95", "t": "헬스케어로"}, {"label": "필수소비재", "value": 1.66, "text": "+1.66", "t": "생활필수품을"},
                  {"label": "부동산", "value": 1.31, "text": "+1.31", "t": "나머지는"}, {"label": "금융", "value": 0.83, "text": "+0.83", "t": "대부분"},
                  {"label": "기술", "value": -3.26, "text": "-3.26", "t": "기술"}],
           beats=[{"say": "업종별로 보면 기술 업종만 3.26% 빠졌고, 나머지는 대부분 올랐습니다. 가장 많이 오른 건 헬스케어로 2.95%, 생활필수품을 파는 회사들도 1.66% 올랐습니다."},
                  {"say": "다우가 5만 선을 넘은 것도 이 흐름과 맞닿아 있습니다. 다우는 기술주 비중이 나스닥보다 작아, 돈이 반도체에서 다른 업종으로 옮겨 가는 날에는 이렇게 다른 방향으로 움직이곤 합니다."}]))
    s(dict(type="checklist", chapter=2, label=K8 + " · 앤트로픽·소비자신뢰지수는 보도", title="같은 화요일에 있었던 일", x=150, text_w=920, skin=NP,
           rows=[{"label": "사노피, 인스메드 인수 — 주당 175달러, 약 410억 달러 (8-K)", "state": "ok", "t": "사노피가"},
                 {"label": "인수 값: 11월 18일 종가보다 약 46% 웃돈", "state": "ok", "t": "46%"},
                 {"label": "앤트로픽 81.90달러 — 공모가 83달러 아래 첫 마감 (보도)", "state": "warn", "t": "앤트로픽은"},
                 {"label": "11월 소비자신뢰지수 103.3 (보도)", "state": "warn", "t": "소비자신뢰지수는"}],
           beats=[{"say": "헬스케어에는 이유가 하나 더 있었습니다. 프랑스 제약사 사노피가 미국 인스메드를 주당 175달러, 모두 약 410억 달러에 사기로 했습니다. 회사 공시에 따르면 소문이 나기 전 종가보다 약 46% 비싼 값입니다.", "upto": 2},
                  {"say": "반대로 AI 쪽은 무거웠습니다. 보도에 따르면 지난주 상장한 앤트로픽은 처음으로 공모가 아래에서 장을 마쳤습니다. 한편 소비자들의 경기 체감을 보여 주는 소비자신뢰지수는 103.3으로 크게 올랐다고 보도됐습니다.", "upto": 4}]))
    s(dict(type="versus", chapter=2, insight=True, label="UBS 고객 메모(CNBC 인용, 2026.11.24) · 버리 뉴스레터(야후 파이낸스 보도, 2026.11.24) · 의견이며 사실이 아닙니다",
           left={"value": "안 깨졌다", "label": "헤펠레(UBS): AI 투자 이야기는 그대로", "icon": "trending-up"},
           right={"value": "불안한 정상", "label": "버리: 엔비디아의 불안이 돌아왔다", "icon": "trending-down"},
           beats=[{"say": "사람들의 시각은 갈립니다. UBS 글로벌 웰스 매니지먼트의 마크 헤펠레 최고투자책임자는, CNBC가 인용한 고객 메모에서 이번 출렁임을 AI 투자 이야기가 깨졌다는 신호로 보지 않는다고 썼습니다. 엔비디아가 상승분의 4분의 3을 지킨 숫자는 이 시각을 받칩니다.", "motion": [M("4분의", "count", id="i1", value="엔비디아 76% 지킴", label="받치는 숫자 (계산)", x=560, y=900, w=460, h=130, fs=42)]},
                  {"say": "반면 마이클 버리는 자신의 뉴스레터에서, 황의 복귀로 엔비디아에 '불안한 정상'이 돌아왔다고 표현했다고 야후 파이낸스가 전했습니다. 사슬 쪽이 하루 만에 3분의 2를 돌려준 숫자는 이쪽에 가깝습니다. 둘 다 사실이 아니라 한 사람의 시각입니다.", "motion": [M("3분의", "count", id="i2", value="사슬 65~70% 반납", label="받치는 숫자 (계산)", x=1360, y=900, w=460, h=130, fs=42)]}]))

    # ── 해석 ──
    s(dict(type="map_causal", chapter=3, look="board", label="자체 해석 · 근거: 야후 종가 11.20·23·24, 업종 ETF, 인스메드 8-K",
           map={"nodes": {"q": {"label": "소식은 남기고, 덤은 돌려줬다", "icon": "circle-help", "x": 960, "y": 260},
                          "keep": {"label": "남은 것: 엔비디아 76%", "icon": "shield-check", "x": 420, "y": 660},
                          "move": {"label": "옮겨 간 것: 사슬 → 헬스케어·다우", "icon": "arrow-right-left", "x": 1500, "y": 660}},
                "edges": [["keep", "q"], ["move", "q"]]},
           beats=[{"say": "여기서부터는 해석입니다. 화요일 미국 시장은 황의 복귀를 되돌리지 않았습니다. 엔비디아 자체는 오른 몫 대부분을 지켰습니다.",
                   "reveal": ["keep"], "active": "keep"},
                  {"say": "되돌린 건 그 소식에 함께 실려 오른 사슬이었고, 빠진 돈은 시장을 떠나지 않고 헬스케어와 다우 쪽으로 옮겨 갔습니다. 소식은 남기고, 덤은 돌려준 하루로 보입니다.",
                   "reveal": ["move", "q"], "draw": [["keep", "q"], ["move", "q"]], "active": "q"}]))

    # ── 한국 ──
    s(dict(type="chapter", chapter=4, num="4", title="한국은 덤까지 받았다", icon="map-pin", look="photo", bg_src="seoul",
           beats=B("이제 한국입니다. 이번에도 시간 순서가 중요합니다.")))
    s(dict(type="bars", chapter=4, label=KR, title="24일(화) 한국 마감 (%)", unit="", emph=0, skin=DS,
           items=[{"label": "현대차", "value": 11.11, "text": "+11.11", "t": "현대차는"}, {"label": "SK하이닉스", "value": 6.73, "text": "+6.73", "t": "SK하이닉스는"},
                  {"label": "삼성전자", "value": 6.70, "text": "+6.70", "t": "삼성전자는"}, {"label": "코스피", "value": 6.32, "text": "+6.32", "t": "코스피가"}],
           beats=[{"say": "어제 한국 장은 미국 월요일의 급등을 받아, 코스피가 6.32% 오른 5,006.03으로 닫혔습니다. SK하이닉스는 6.73%, 삼성전자는 6.70% 올랐고, 국내 보도에 따르면 황의 복귀 효과로 현대차는 11.11% 뛰었습니다.",
                   "motion": [M("5,006", "count", id="ks", value="5,006.03", label="코스피 24일 종가", x=1600, y=860, w=420, h=150, fs=52)]},
                  {"say": "그런데 이 숫자는 미국 화요일의 되돌림을 모른 채 만들어진 것입니다. 한국 메모리는 사슬로 치면 마이크론과 같은 자리에 있습니다. 오늘 아침 9시 한국 장이 화요일 미국을 처음 받습니다.",
                   "motion": [M("9시", "count", id="k9", value="25일 09:00", label="한국 장 첫 반영", x=1000, y=820, w=420, h=150, fs=50)]}]))

    # ── 볼 것 ──
    s(dict(type="chapter", chapter=5, num="5", title="이번 주 볼 것", icon="calendar", look="board",
           beats=B("이 해석을 확인할 날짜들입니다.")))
    s(dict(type="checklist", chapter=5, label="한국거래소 · 재무부 기한·하원 면담은 보도 · 미 경제분석국(BEA) 일정 · 뉴욕증권거래소 휴장일 · 투자 권유가 아닙니다", title="일정 (한국 시간)", x=150, text_w=920, skin=NP,
           rows=[{"label": "25일(수) 09:00 · 한국 장 — 미국 되돌림 첫 반영", "state": "warn", "t": "9시"},
                 {"label": "25일(수) · 재무부 답변 기한 / 22:30 미국 10월 PCE 물가", "state": "warn", "t": "물가"},
                 {"label": "26일(목) 미국 휴장 · 27일(금) 단축 거래", "state": "warn", "t": "추수감사절로"},
                 {"label": "12월 1일 · 황 하원 비공개 면담 (보도)", "state": "warn", "t": "면담"}],
           beats=[{"say": "오늘 아침 9시, 코스피가 5,000선을 지키는지, 한국 메모리가 마이크론처럼 크게 되돌리는지 봅니다. 오늘은 보도된 재무부의 엔비디아 답변 기한이고, 밤 10시 30분에는 연준이 가장 중시하는 물가 지표가 나옵니다.", "upto": 2},
                  {"say": "목요일은 추수감사절로 미국 장이 쉬고, 금요일은 일찍 닫습니다. 보도대로라면 12월 1일, 황이 하원 위원회와 비공개 면담을 합니다.", "upto": 4}]))
    s(dict(type="checklist", chapter=5, label="팩트시트 '틀리는 경우' · 투자 권유가 아닙니다", title="이 해석이 틀리는 경우", x=150, text_w=920, skin=NP,
           rows=[{"label": "엔비디아도 남은 76%를 며칠 안에 돌려주면", "state": "warn", "t": "엔비디아마저"},
                 {"label": "한국 메모리가 거의 되돌리지 않으면", "state": "warn", "t": "한국"},
                 {"label": "오늘 밤 물가가 높게 나오면", "state": "warn", "t": "높게"}],
           beats=[{"say": "틀리는 경우도 적어 둡니다. 엔비디아마저 남은 몫을 며칠 안에 돌려준다면, 화요일은 사슬만의 되돌림이 아니라 복귀 효과 전체가 빠지는 첫날이었다는 뜻입니다.", "upto": 1},
                  {"say": "오늘 한국 메모리가 거의 되돌리지 않는다면, 어제 한국의 상승은 엔비디아 사슬보다 메모리 자체의 이유에 더 기대고 있었다는 뜻입니다. 그리고 오늘 밤 물가가 높게 나오면, 금리 걱정이 다시 앞에 섭니다.", "upto": 3}]))
    s(dict(type="kinetic", chapter=5, beats=[{"say": "시장은 소식은 남기고, 덤은 돌려줬습니다.", "hit": ["덤은"]}]))
    s(dict(type="outro", chapter=5, title="25일 아침까지의 소식", sub="출처는 설명란에", clip={"src": "seoul", "start": 0},
           beats=B("미국은 하루 만에 덤을 내려놨습니다. 그렇다면 어제 덤까지 받은 한국은, 오늘 얼마를 내려놓게 될까요?")))
    for i, x in enumerate(S, 1):
        x["id"] = i
    DEC = json.loads((Path(__file__).parent / "decide.json").read_text(encoding="utf-8"))
    for x in S:
        d = DEC.get(str(x["id"]))
        if d:
            x["decide"] = {"situation": d[0], "pick": d[1], "why": d[2], "intent": d[3], "over": [{"id": o[0], "why_not": o[1]} for o in d[4]], "refs": ["manual/09-market-daily.md"]}
    spec = json.loads((Path(__file__).parent / "spec.json").read_text(encoding="utf-8"))
    spec["scenes"] = S
    spec["footage"] = fo
    (P / "02_script" / "hybrid.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
    print(P, len(S))


if __name__ == "__main__":
    main()
