"""첫 매일 시장 브리핑 (v17·v18): 11월 11일 미국 장 · 11월 12일 한국 장.
    python -m ytflow daily --project 20261112-market-daily     # 전날 시장 훑기 (01_research/daily_brief.md)
    python scripts/daily_20261112/make.py && python -m ytflow hybrid 20261112-market-daily
사실은 factsheet.md 의 출처로 확인한 것만. 사진: 위키미디어 공용 CC BY (출처 표시).
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from ytflow.stages import archive  # noqa: E402

P = ROOT / "projects" / "20261112-market-daily"
AS_OF = "11월 11일 미국 · 12일 한국 마감 기준"

PHOTOS = {  # 키: (위키미디어 파일 이름, 표지로 쓸지)
    "dc": "Microsoft Data Center Middenmeer, the Netherlands - 1.jpg",
    "nvidia": "Nvidia sign.jpg",
}
KNOWN = {   # 위키미디어 검색이 429 로 막힐 때를 위한 확인된 기록 (2026-11-12 조회)
    "dc": {"license": "CC BY 4.0", "artist": "Hay Kranen"},
    "nvidia": {"license": "CC BY 2.0", "artist": "Will Buckner"},
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
            url = r.get("url") or ("https://commons.wikimedia.org/wiki/Special:FilePath/" + title.replace(" ", "_") + "?width=1920")
            subprocess.run(["curl", "-sSL", "-A", "ytflow", "-o", str(jpg), url], check=True)
        mp4 = fdir / f"{key}.mp4"
        if not mp4.exists():
            archive.still_to_clip(jpg, mp4, dur=12)
        out[key] = {"file": mp4.name, "credit": r["credit"], "url": r["page"], "license": r["license"]}
    return out


def B(*says, **kw):
    bs = [{"say": s} for s in says]
    for k, v in kw.items():
        i, key = k.split("_", 1)
        bs[int(i[1:])][key] = v
    return bs


def main():
    for d in ("01_research", "02_script", "05_edit"):
        (P / d).mkdir(parents=True, exist_ok=True)
    fo = photos()
    S = []
    s = S.append
    s(dict(type="intro", chapter=0, series="어제 시장, 오늘 아침", as_of=AS_OF, bg_src="dc",
           title_lines=["실적 하나에 반도체가 날고,", "장이 끝나자 반전"], agenda_beat=3,
           layers=[{"kind": "photo", "src": "nvidia", "beat": 2, "side": "right", "w": 600, "top": 250, "caption": "엔비디아 간판 · CC BY 2.0 Will Buckner"}],
           beats=B("안녕하세요. 어제 시장을 오늘 아침에 정리해 드리는, 어제 시장 오늘 아침입니다.",
                   "오늘은 11월 11일 미국 장과 12일 한국 장을, 마감 기준으로 정리합니다.",
                   "한 회사의 실적 발표에 미국 반도체 주식이 하루 만에 5% 넘게 올랐습니다. 그런데 장이 끝나고 몇 시간 뒤, 정반대 소식이 나왔죠. 무슨 일이 있었을까요?",
                   "이런 순서로 보겠습니다. 반도체를 띄운 코어위브 실적, 장 마감 뒤의 엔비디아, 그리고 오늘 코스피까지요.",
                   "시작하겠습니다.")))
    s(dict(type="bars", chapter=0, label="야후 파이낸스 종가 · 2026.11.10 → 11.11", title="11월 11일 미국 마감 (%)", unit="%", emph=2,
           layers=[{"kind": "locator", "at": [-74.0, 40.71], "label": "미국 뉴욕 · 11월 11일 마감", "beat": 0, "side": "left", "top": 170, "scale": 2.2}],
           items=[{"label": "S&P 500", "value": 1.31, "text": "+1.3"}, {"label": "나스닥", "value": 1.60, "text": "+1.6"},
                  {"label": "필라델피아 반도체 지수", "value": 5.66, "text": "+5.7"}],
           beats=B("먼저 숫자부터 보죠. 11월 11일 미국 S&P 500은 1.3%, 나스닥은 1.6% 올랐습니다.",
                   "그런데 반도체 지수는 5.7%, 시장 전체의 네 배 넘게 올랐습니다. 무엇이 반도체만 이렇게 띄웠을까요?")))
    s(dict(type="chapter", chapter=1, num="1", title="코어위브 실적", icon="server", look="photo", bg_src="dc",
           beats=B("답은 한 회사의 실적 발표에 있었습니다. AI 회사들에게 데이터센터를 빌려주는 코어위브입니다.")))
    s(dict(type="kb", chapter=1, clip={"src": "dc", "start": 0}, move="in", stamp="데이터센터 예시 · 네덜란드 (코어위브 시설 아님)",
           label="자료 사진 · " + fo["dc"]["credit"],
           beats=B("AI를 돌리려면 칩이 가득 찬 거대한 건물, 데이터센터가 필요합니다. 코어위브는 이런 건물을 지어 AI 회사들에게 빌려주죠.")))
    s(dict(type="bignum", chapter=1, label="코어위브 3분기 실적 (11월 10일 발표) · 모틀리풀 보도 / 야후 파이낸스 종가",
           small="코어위브 3분기 매출 · 1년 전보다", value="+168%", compare={"label": "다음 날 주가", "value": "+24.7%"},
           layers=[{"kind": "locator", "at": [-74.31, 40.79], "label": "코어위브 본사 · 미국 뉴저지", "beat": 0, "side": "right", "top": 120, "scale": 2.2}],
           beats=B("11월 10일 장 마감 뒤 나온 3분기 매출은 36억 6천만 달러. 1년 전보다 168% 늘었고, 시장 예상보다도 많았습니다.",
                   "올해 매출 전망도 130억에서 133억 달러로 올렸죠. 다음 날 주가는 24.7% 올랐습니다.")))
    s(dict(type="map_causal", chapter=1, look="board", label="이 영상 팩트시트 F2~F5 정리",
           beats=[{"say": "그런데 왜 다른 회사들까지 올랐을까요? 코어위브는 데이터센터에 370억에서 390억 달러를 쓰겠다고 했습니다. 그 돈으로 칩을 사서 데이터센터를 채우죠. 메모리 칩을 파는 마이크론이 11.9% 오른 이유입니다.",
                   "reveal": ["crwv", "capex", "mu"], "draw": [["crwv", "capex"], ["capex", "mu"]], "active": "mu"},
                  {"say": "또 하나는 빚입니다. AI 데이터센터를 짓는 회사들이 빚을 너무 많이 진다는 걱정이 컸는데, 코어위브는 담보 없는 빚을 줄이고 고객이 미리 내는 돈을 더 쓰겠다고 했습니다. 아파트를 지을 때 대출 대신 분양 대금을 미리 받는 것과 비슷하죠. 같은 걱정을 받던 오라클이 8.8% 오른 이유입니다.",
                   "reveal": ["fund", "orcl"], "draw": [["crwv", "fund"], ["fund", "orcl"]], "active": "orcl"}]))
    s(dict(type="bars", chapter=1, label="야후 파이낸스 종가 · 2026.11.10 → 11.11", title="11월 11일 하루 (%)", unit="%", emph=0,
           fx=["tilt"],
           items=[{"label": "코어위브", "value": 24.71, "text": "+24.7"}, {"label": "마이크론", "value": 11.89, "text": "+11.9"},
                  {"label": "오라클", "value": 8.81, "text": "+8.8"}, {"label": "AMD", "value": 7.32, "text": "+7.3"},
                  {"label": "S&P 500", "value": 1.31, "text": "+1.3"}],
           beats=B("하루 성적표로 보면 이렇습니다. 실적을 낸 코어위브가 가장 많이, 그다음 칩과 데이터센터 회사들이 따라 올랐습니다.",
                   "일주일 전인 11월 5일엔 반도체 지수가 하루에 12% 넘게 떨어졌던 걸 생각하면, 분위기가 꽤 바뀐 셈입니다.")))
    s(dict(type="chapter", chapter=2, num="2", title="장 마감 뒤, 엔비디아", icon="microchip", look="photo", bg_src="nvidia",
           beats=B("그런데 장이 끝나고 몇 시간 뒤, 분위기가 바뀌었습니다.")))
    s(dict(type="kb", chapter=2, clip={"src": "nvidia", "start": 0}, move="in", stamp="엔비디아 · 11.11 정규장 +2.9% → 시간외 약 -9%",
           label="야후 파이낸스 종가 / NBC 뉴스 보도 (시간외) · 사진 " + fo["nvidia"]["credit"],
           beats=B("엔비디아도 이날 정규장에선 2.9% 올라 173달러에 마감했습니다.",
                   "하지만 장 마감 뒤 시간외 거래에서 9% 가까이 떨어졌습니다.")))
    s(dict(type="checklist", chapter=2, label="NBC 뉴스 · 2026.11.11 보도 · 11월 12일 기준", title="확인된 것과 아직 모르는 것",
           layers=[{"kind": "photo", "src": "nvidia", "beat": 0, "side": "right", "w": 460, "top": 610, "caption": "엔비디아 간판 · CC BY 2.0 Will Buckner"}],
           rows=[{"label": "보도: 이사회가 젠슨 황 CEO의 거취를 논의 (WSJ·NYT 등)", "state": "warn"},
                 {"label": "회사: 여러 차례 논평 요청에 답하지 않음", "state": "warn"},
                 {"label": "결정: 발표된 것 없음", "state": "no"}],
           beats=[{"say": "이유는 보도였습니다. 월스트리트저널과 뉴욕타임스 등이, 엔비디아 이사회가 젠슨 황 CEO의 거취를 논의하고 있다고 전했습니다.", "upto": 1},
                  {"say": "회사는 답하지 않았고, 11월 12일 기준으로 결정된 것은 없습니다. 아직은 보도 단계라는 점을 기억해 두세요.", "upto": 3}]))
    s(dict(type="chapter", chapter=3, num="3", title="오늘 코스피", icon="trending-down", look="dash",
           beats=B("그 여파는 오늘 한국 시장에서 보였습니다.")))
    s(dict(type="chart", chapter=3, label="야후 파이낸스 코스피 일별 종가 (^KS11) · 2026.11.12 기준", ticker="^KS11", period="1mo", title="코스피",
           beats=[{"say": "코스피는 11월 10일 4.4%, 11일 2.6% 오르며 이틀 동안 크게 뛰었습니다.", "focus_last": 3, "mark": "-0.61%"},
                  {"say": "그리고 오늘 12일, 0.6% 내린 5,342.73에 마감했습니다."}]))
    s(dict(type="versus", chapter=3, label="야후 파이낸스 종가 · 2026.11.11 → 11.12",
           fx=["tilt"], left={"value": "+1.0%", "label": "삼성전자", "icon": "trending-up"}, right={"value": "-1.8%", "label": "SK하이닉스", "icon": "trending-down"},
           beats=B("종목마다 달랐습니다. 삼성전자는 1% 가까이 올랐지만, 엔비디아에 AI용 메모리를 많이 공급하는 SK하이닉스는 1.8% 내렸습니다.",
                   "증권가에선 엔비디아 소식과 함께, 이틀 동안 크게 오른 뒤 나온 차익 매물과 옵션 만기도 이유로 꼽았습니다.")))
    s(dict(type="kinetic", chapter=3, beats=[{"say": "정리하면, 실적이 띄우고 이슈가 끌어내린 하루였습니다.", "hit": ["실적이", "이슈가"]}]))
    s(dict(type="checklist", chapter=3, label="11월 12일 기준 · 투자 권유가 아닙니다", title="오늘 볼 것",
           rows=[{"label": "엔비디아 이사회 — 공식 발표가 나오는지", "state": "warn"},
                 {"label": "오늘 밤 미국 장 — 시간외 하락이 정규장에서도 이어지는지", "state": "warn"},
                 {"label": "반도체 지수 — 코어위브발 반등이 엔비디아 소식에도 버티는지", "state": "warn"}],
           beats=[{"say": "오늘 볼 것은 세 가지입니다. 엔비디아 이사회의 공식 발표가 나오는지, 오늘 밤 미국 장에서 시간외 하락이 이어지는지,", "upto": 2},
                  {"say": "그리고 코어위브가 살려 낸 반도체 반등이 엔비디아 소식에도 버티는지입니다.", "upto": 3}]))
    s(dict(type="outro", chapter=3, title="어제 시장, 오늘 아침", sub="11월 12일 기준 · 출처는 설명란에", clip={"src": "dc", "start": 0},
           beats=B("오늘 시장 정리는 여기까지입니다. 11월 12일 기준이고, 출처는 모두 설명란에 남겨 두겠습니다.")))
    for i, x in enumerate(S, 1):
        x["id"] = i
    spec = {
        "title": "실적 하나에 반도체가 날고, 장이 끝나자 반전 — 11월 11일 미국·12일 한국 시장",
        "brand": "market",
        "core_message": "코어위브의 좋은 실적이 'AI 투자는 계속된다'는 신호가 되어 반도체·데이터센터 주식을 끌어올렸지만, 장 마감 뒤 엔비디아 CEO 거취 보도로 분위기가 바뀌었고 오늘 코스피는 약보합으로 마쳤다.",
        "question": "무엇이 반도체만 띄웠고, 왜 하루 만에 분위기가 바뀌었을까?",
        "logic": ["11/11 미국: S&P +1.3%, 나스닥 +1.6%, 반도체 지수 +5.7%", "원인(실적): 코어위브 3분기 매출 +168%, 연간 전망 상향, 데이터센터 투자 370~390억 달러",
                  "번진 곳: 칩 수요(마이크론 +11.9%), 빚 걱정 완화(오라클 +8.8%)", "장 마감 뒤(이슈): 엔비디아 CEO 거취 논의 보도 → 시간외 약 -9%",
                  "11/12 한국: 코스피 -0.6%, SK하이닉스 -1.8%, 삼성전자 +1.0%", "오늘 볼 것: 이사회 발표, 미국 정규장, 반도체 반등 지속"],
        "compare_to": [{"value": "반도체 지수 +5.7%", "to": "S&P 500 +1.3% (네 배 넘게)"}, {"value": "코어위브 매출 +168%", "to": "1년 전 같은 분기"},
                       {"value": "11/11 반도체 지수 +5.7%", "to": "11/5 하루 -12.2%"}],
        "analogies": [{"a": "코어위브", "b": "AI 회사에 데이터센터를 빌려주는 임대 사업자 — 세입자가 늘면 들일 칩도 늘어난다"},
                      {"a": "담보 없는 빚 대신 고객 선지급금", "b": "아파트를 지을 때 대출 대신 분양 대금을 미리 받는 것"}],
        "past_cases": [{"case": "2026년 11월 5일 반도체 지수 하루 -12.2%", "lesson": "일주일 만에 AI 반도체에 대한 분위기가 크게 바뀔 수 있다"}],
        "glossary": [{"term": "시간외 거래", "plain": "정규장이 끝난 뒤에도 이어지는 거래. 거래량이 적어 크게 움직이기도 한다"},
                     {"term": "선지급금(선수금)", "plain": "고객이 서비스를 받기 전에 미리 내는 돈"},
                     {"term": "옵션 만기", "plain": "주가지수 옵션 계약이 끝나는 날. 이날은 큰손들의 정리 매매로 지수가 출렁이기도 한다"}],
        "scenes": S,
        "map": {"nodes": {"crwv": {"label": "코어위브 실적·전망 상향", "icon": "server", "x": 300, "y": 400},
                          "capex": {"label": "데이터센터 투자 370~390억 달러", "icon": "building-2", "x": 860, "y": 400},
                          "mu": {"label": "칩 수요 → 마이크론 +11.9%", "icon": "microchip", "x": 1500, "y": 400},
                          "fund": {"label": "담보 없는 빚 대신 고객 선지급금", "icon": "landmark", "x": 860, "y": 740},
                          "orcl": {"label": "빚 걱정 완화 → 오라클 +8.8%", "icon": "trending-up", "x": 1500, "y": 740}},
                "edges": [["crwv", "capex"], ["capex", "mu"], ["crwv", "fund"], ["fund", "orcl"]]},
        "footage": fo,
        "package": {
            "title": "실적 하나에 반도체 5.7%↑, 장 끝나자 엔비디아 -9% | 11월 12일 시장 정리",
            "title_options": ["실적 하나에 반도체 5.7%↑, 장 끝나자 엔비디아 -9% | 11월 12일 시장 정리",
                              "코어위브가 띄운 반도체, 엔비디아 보도에 하루 만에 반전",
                              "반도체 하루 +5.7%, 그리고 시간외 -9% — 무슨 일이 있었나"],
            "title_why": ["[움직임 숫자 + 반전] 매일 브리핑 공식, 날짜로 '오늘 것'임을", "원인 회사 이름 + 반전", "숫자 두 개가 질문을 만듦"],
            "thumbnails": [
                {"id": "A", "name": "엔비디아 간판 + 반전", "layout": "photo", "photo_side": "full", "image": {"file": "04_assets/footage/raw/nvidia.jpg", "focus": [0.5, 0.5]},
                 "top": "11월 12일 시장", "lines": ["반도체 날고,", "장 끝나자 반전"], "hl": ["반전"], "sub": "코어위브 · 엔비디아 · 코스피", "size": 130, "text_y": 330, "marks": [],
                 "why": ["장소(회사) + 반전 한 단어"]},
                {"id": "B", "name": "숫자 대비", "layout": "versus", "left": {"value": "+5.7%", "label": "반도체 지수 (정규장)"},
                 "right": {"value": "-9%", "label": "엔비디아 (시간외)"}, "headline": "같은 날, 반대 방향", "hl": [], "marks": [], "why": ["숫자 둘이 질문을 만듦"]},
                {"id": "C", "name": "데이터센터 + 실적", "layout": "photo", "photo_side": "full", "image": {"file": "04_assets/footage/raw/dc.jpg", "focus": [0.5, 0.5]},
                 "top": "코어위브 3분기", "lines": ["매출 +168%,", "반도체를 띄우다"], "hl": ["+168%"], "sub": "", "size": 130, "text_y": 330, "marks": [],
                 "why": ["원인 숫자 하나"]}]},
    }
    (P / "02_script" / "hybrid.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
    print(P, len(S), "장면")


if __name__ == "__main__":
    main()
