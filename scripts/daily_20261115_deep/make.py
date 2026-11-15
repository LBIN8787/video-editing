"""이어 읽는 시장 — 심층: 젠슨 황 사임, 무엇이 흔들리나 (manual v28: 시장을 흔든 사건이 중심축 → 돈의 약속·순환 금융·연준·한국, 주의할 점, 입장별 해석).
    python scripts/daily_20261115_deep/make.py && python -m ytflow hybrid 20261115-market-deep
"""
import json
import subprocess
import time
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from ytflow.stages import archive  # noqa: E402

P = ROOT / "projects" / "20261115-market-deep"
AS_OF = "11월 15일 오전까지 나온 자료 · 11월 13일 마감 기준"
K8 = "엔비디아 8-K·보도자료 (2026.11.11~12, SEC)"
DS, NP = "dark-doc", "newsprint"   # 배경: 청록(midnight) 대신 호박색·신문지 (2026-11-15 사용자 요청, 이번 편만)
YH = "야후 파이낸스 종가 · 2026.11.6 → 11.13"
FSR = "연준 금융안정보고서 (2026.11.13)"
BOE = "영란은행 금융정책위원회 기록 (2026.9.30)"
BOW = "보먼 연준 부의장 연설 (2026.11.10)"
JEF = "제퍼슨 연준 부의장 연설 (2026.11.13)"
Q2 = "엔비디아 2분기 실적 보도자료·CFO 코멘터리 (2026.8.26, SEC 8-K)"

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


def M(t, do, **kw):
    return dict(t=t, do=do, **kw)


def main():
    for d in ("01_research", "02_script", "05_edit"):
        (P / d).mkdir(parents=True, exist_ok=True)
    fo = photos()
    cr = {k: v["credit"].split(" · 위키미디어")[0] for k, v in fo.items()}
    S = []
    s = S.append
    PX = "야후 파이낸스 종가 · 사임 공시 전날(11일) → 13일"
    s(dict(type="bars", chapter=0, label="야후 파이낸스 종가 · 사임 공시 전날(11일) → 13일 마감 기준", title="같은 이틀, 엇갈린 성적 (%) · 11월 11일→13일", unit="", emph=2, skin=DS,
           items=[{"label": "메타", "value": 2.05, "text": "+2.05", "t": "메타는"}, {"label": "네이버", "value": -11.22, "text": "-11.22", "t": "네이버는"},
                  {"label": "네비우스", "value": -25.09, "text": "-25.09", "t": "네비우스는"}],
           beats=B("11월 11일 밤 엔비디아 창업자의 사임 소식이 나온 뒤 이틀 동안, 11월 13일 마감 기준으로 엔비디아의 칩을 사는 메타는 2.05% 올랐습니다. 반면 엔비디아와 한국에 AI 공장을 짓기로 한 네이버는 11.22%, 엔비디아가 지분을 가진 네비우스는 25.09% 내렸습니다.",
                   "칩을 사는 쪽은 버텼는데, 엔비디아의 돈과 묶인 쪽은 크게 흔들린 겁니다. 창업자가 떠난 엔비디아에서, 칩보다 먼저 흔들리는 것은 무엇일까요? 공시 원문에서 출발해, 돈이 묶인 곳과 과거의 비슷한 날, 그리고 한국의 계좌까지 따라가 봅니다.")))
    s(dict(type="quote", chapter=0, label=K8, who="엔비디아 이사회", role="8-K 공시 · 11월 11일 자",
           quote="이사회는 젠슨 황의 사장·CEO·이사직 사임을 받아들였다. 즉시 효력.", keyword="즉시",
           orig="the Board of Directors ... accepted the resignation of Jen-Hsun Huang, as NVIDIA's President, Chief Executive Officer and member of the Board, effective immediately.",
           beats=B("11월 11일 장이 끝난 뒤, 엔비디아 이사회는 짧은 공시 한 장을 냈습니다. 33년 동안 회사를 이끈 창업자 젠슨 황의 사임을 받아들였고, 즉시 효력이 생긴다는 내용이었습니다.",
                   "최고재무책임자 콜레트 크레스가 임시 최고경영자를 겸하고, 회사 역사상 처음으로 이사회 의장 자리가 생겼습니다. 이번 주 세계 증시를 가장 크게 흔든 사건입니다.")))
    s(dict(type="chapter", chapter=1, num="1", title="무슨 일이 있었나", icon="calendar", look="photo", bg_src="nvidia",
           beats=B("먼저 일주일을 날짜 순서로 정리하겠습니다.")))
    s(dict(type="checklist", chapter=1, label=K8 + " · 사생활 관련 보도 내용은 다루지 않음", title="엔비디아의 일주일", x=150, text_w=860, skin=NP,
           rows=[{"label": "9일 이사회가 CEO 관련 보도 조사 → 주가 -4.27%", "state": "warn", "t": "9일"},
                 {"label": "11일 장 마감 뒤 사임 수락 (8-K)", "state": "warn", "t": "11일"},
                 {"label": "크레스 CFO 가 임시 CEO 겸임", "state": "ok", "t": "크레스"},
                 {"label": "하비 존스, 회사 첫 이사회 의장", "state": "ok", "t": "의장"},
                 {"label": "18일(수) 06:20 실적은 예정대로", "state": "warn", "t": "18일"}],
           beats=[{"say": "9일 월요일, 이사회가 최고경영자 관련 보도를 조사한다는 소식에 주가가 먼저 흔들렸습니다. 이 영상은 사생활 보도의 내용은 다루지 않고, 공시된 사실과 사업에 미치는 영향만 봅니다.", "upto": 1},
                  {"say": "11일 장 마감 뒤 사임이 공시됐습니다. 크레스 최고재무책임자가 임시 최고경영자를 맡고, 1993년부터 이사였던 하비 존스가 첫 이사회 의장이 됐습니다. 그리고 3분기 실적은 한국 시간 18일 새벽, 예정대로 나옵니다.", "upto": 5,
                   "motion": [M("크레스", "icon", id="kr", icon="👩‍💼", x=1620, y=420, d=170, label="임시 CEO"), M("존스", "icon", id="ch", icon="🏛️", x=1620, y=740, d=170, label="첫 의장")]}]))
    s(dict(type="bars", chapter=1, label="야후 파이낸스 종가 · 11월 13일 마감 기준", title="11월 엔비디아 날짜별 등락 (%) · 한 주 -12.75", unit="", emph=2, skin=DS,
           layers=[{"kind": "locator", "at": [-121.96, 37.37], "label": "미국 산타클라라 · 엔비디아 본사", "beat": 0, "side": "left", "top": 170, "scale": 2.2}],
           items=[{"label": "9일", "value": -4.27, "text": "-4.27", "t": "9일"}, {"label": "10일", "value": -5.47, "text": "-5.47", "t": "10일"},
                  {"label": "12일", "value": -4.34, "text": "-4.34", "t": "12일"}, {"label": "13일", "value": -2.01, "text": "-2.01", "t": "13일"}],
           beats=[{"say": "11월 13일 마감 기준으로 보면, 엔비디아 주가는 이사회 조사 보도가 나온 9일 4.27%, 10일 5.47% 내렸고, 사임 발표 뒤 12일 4.34%, 13일 2.01% 더 내렸습니다. 한 주 동안 12.75%입니다."},
                  {"say": "공시가 나오기 전부터 주가는 먼저 흔들렸고, 공시 뒤에도 이틀을 더 내렸습니다. 회사가 만드는 칩과 제품 계획은 그대로인데도 말입니다."}]))
    s(dict(type="quote", chapter=1, label=K8 + " · 보도자료 (11월 12일)", who="하비 존스", role="엔비디아 이사회 의장 · 11월 12일",
           quote="회사의 운영, 고객과의 약속, 제품 로드맵은 중단 없이 이어질 것으로 기대한다.", keyword="고객과의 약속",
           orig="we expect the company's operations, customer commitments and product roadmap to continue without interruption.",
           beats=B("이사회 의장은 보도자료에서 세 가지가 중단 없이 이어질 것이라고 말했습니다. 회사의 운영, 제품 로드맵, 그리고 고객과의 약속입니다.",
                   "여기서 '고객과의 약속'이라는 말에 주목할 필요가 있습니다. 시장이 무엇을 걱정하는지, 이사회가 먼저 짚은 셈이기 때문입니다.",
                   "운영과 로드맵은 엔지니어와 공급망이 지켜 낼 수 있지만, 고객과의 약속은 결국 돈을 얼마나, 얼마나 오래 대느냐의 문제입니다. 그 결정은 지금까지 창업자의 몫이었습니다.")))
    s(dict(type="chapter", chapter=2, num="2", title="공시에 이미 적혀 있던 위험", icon="landmark", look="board",
           beats=B("이번 사임은 쇼크로 보도됐습니다. 그런데 회사의 공시를 거꾸로 읽어 보면, 이야기가 조금 달라집니다.")))
    s(dict(type="quote", chapter=2, label="엔비디아 10-K (2026.2.25 제출, FY2026) 위험 요인 · SEC", who="엔비디아 연차 보고서", role="위험 요인 · 올해 2월 제출",
           quote="임원과 핵심 인력의 승계 계획, 지식 이전, 원활한 교체에 실패하면 전략과 실행, 장기적 성공에 지장을 줄 수 있다.", keyword="승계",
           orig="Failure to ensure effective succession planning, transfer of knowledge, and smooth transitions involving executives and key employees could hinder our strategic planning, execution, and long-term success.",
           beats=B("엔비디아는 올해 2월에 낸 연차 보고서의 위험 요인에, 임원과 핵심 인력의 승계 계획에 실패하면 장기적 성공에 지장을 줄 수 있다고 적었습니다. 위험 자체는 아홉 달 전부터 공시에 있었던 셈입니다.",
                   "같은 보고서는 황 최고경영자가 1993년 회사를 함께 세운 뒤 줄곧 사장이자 최고경영자, 이사였다고 적고 있습니다. 위험은 알려져 있었고, 진짜 질문은 대비가 있었느냐입니다. 그리고 이번 교체에는 정해진 후임이 없었습니다.")))
    s(dict(type="chapter", chapter=3, num="3", title="시장의 첫 반응", icon="trending-up", look="photo", bg_src="nyse",
           beats=B("돈은 이 소식에 어떻게 움직였을까요?")))
    s(dict(type="bars", chapter=3, label="야후 파이낸스 종가 · 2026.11.6 → 11.13", title="같은 한 주, 반도체 성적표 (%)", unit="", emph=3, skin=DS,
           items=[{"label": "AMD", "value": 18.93, "text": "+18.93", "t": "AMD는"}, {"label": "브로드컴", "value": 18.16, "text": "+18.16", "t": "브로드컴은"},
                  {"label": "반도체 지수", "value": 8.05, "text": "+8.05", "t": "반도체 지수는"}, {"label": "엔비디아", "value": -12.75, "text": "-12.75", "t": "엔비디아는"}],
           beats=[{"say": "같은 한 주, AMD는 18.93%, 브로드컴은 18.16% 올랐고 반도체 지수도 8.05% 올랐습니다. 엔비디아만 12.75% 내렸습니다. 돈이 대안을 찾아 옮겨 간 겁니다."},
                  {"say": "보도에 따르면 사임 발표 다음 날 엔비디아는 장 초반 13% 넘게 빠졌다가 4.34% 하락으로 마감했습니다. 그리고 13일에는 AMD가 8.75% 내리며 쏠림의 일부가 되돌아왔습니다.",
                   "motion": [M("13%", "count", id="iv", value="-13%", label="12일 장 초반 (보도)", x=640, y=830, w=400, h=180, fs=80),
                              M("8.75%", "count", id="amd", value="-8.75%", label="13일 AMD", x=1120, y=830, w=400, h=180, fs=80)]}]))
    s(dict(type="checklist", chapter=3, label="모틀리풀(11.14)·한국경제·헤럴드경제(11.13)·포천(11.11) · 목표가는 다루지 않음", title="엇갈린 해석, 근거는 무엇인가", x=150, text_w=880, skin=NP,
           rows=[{"label": "낙관: 단기 사업 영향은 걱정 안 한다 (번스타인)", "state": "ok", "t": "번스타인"},
                 {"label": "낙관: 루빈 사이클·공급망 확보, 로드맵 2028년까지 (삼성증권)", "state": "ok", "t": "삼성증권"},
                 {"label": "우려: 뚜렷한 후계자도, 2인자도 없다 (멜리우스)", "state": "warn", "t": "멜리우스"},
                 {"label": "우려: 창업자와 오래 얽힌 이사회 (포천, 사임 전날)", "state": "warn", "t": "포천"},
                 {"label": "구분: 경영 불확실성 ≠ 반도체 업황 (유안타)", "state": "ok", "t": "유안타"}],
           beats=[{"say": "해석은 엇갈렸습니다. 낙관하는 쪽의 근거는 확정된 계획입니다. 번스타인의 애널리스트는 단기 사업 영향은 걱정하지 않는다고 했고, 삼성증권은 차세대 루빈 제품과 부품 공급망이 이미 확보됐고 로드맵도 2028년까지 정해져 있다고 짚었습니다.", "upto": 2},
                  {"say": "우려하는 쪽의 근거는 사람입니다. 멜리우스는 뚜렷한 후계자도 운영 2인자도 없다고 했고, 포천은 사임 전날 이미 창업자와 수십 년 얽힌 이사회를 문제로 꼽았습니다. 그리고 유안타증권은, 경영 불확실성과 반도체 업황은 구분해야 한다고 정리했습니다.", "upto": 5}]))
    s(dict(type="chapter", chapter=4, num="4", title="어디가 흔들렸나", icon="git-branch", look="photo", bg_src="dc",
           beats=B("그렇다면 이 소식은 어떤 시장, 어떤 산업을 흔들었을까요? 사임 공시 전날 종가와 13일 종가를, 업종별로 나란히 놓아 보겠습니다.")))
    s(dict(type="bars", chapter=4, label=PX + " · 네비우스는 12일 자체 3분기 실적도 발표", title="AI 클라우드·데이터센터 금융 (%)", unit="", emph=0, skin=DS,
           items=[{"label": "네비우스", "value": -25.09, "text": "-25.09", "t": "네비우스는"}, {"label": "코어위브", "value": -12.57, "text": "-12.57", "t": "코어위브는"},
                  {"label": "블루아울", "value": -4.32, "text": "-4.32", "t": "블루아울도"}, {"label": "오라클", "value": -2.36, "text": "-2.36", "t": "오라클은"}],
           beats=B("가장 크게 흔들린 곳은 엔비디아의 칩을 사서 빌려주는 AI 클라우드였습니다. 네비우스는 이틀 동안 25.09%, 코어위브는 12.57% 내렸습니다. 다만 네비우스는 같은 날 자체 3분기 실적에서 손실이 커졌다고 발표해, 사임만의 영향으로 볼 수는 없습니다.",
                   "데이터센터에 돈을 빌려주는 사모 대출 회사 블루아울도 4.32% 내렸고, AI 클라우드 사업을 키워 온 오라클은 2.36% 내렸습니다. 연준 보고서가 그린 순환 금융의 고리 위에 있는 회사들입니다.")))
    s(dict(type="checklist", chapter=4, label="엔비디아 13F (2026.6.30 기준, 8.14 제출) · 13G (7.20) · SEC", title="엔비디아가 지분을 가진 회사들", x=150, text_w=880, skin=NP,
           layers=[{"kind": "photo", "src": "nvidia", "beat": 1, "side": "right", "w": 420, "top": 620, "caption": f"엔비디아 간판 · {cr['nvidia']}"}],
           rows=[{"label": "인텔 약 300억 달러", "state": "warn", "t": "인텔"},
                 {"label": "코어위브 약 47억 달러 (4,721만 주)", "state": "warn", "t": "코어위브"},
                 {"label": "코히런트 약 31억 · 노키아·시놉시스 각 약 22억 달러", "state": "warn", "t": "코히런트"},
                 {"label": "네비우스 9.3% (대부분 워런트)", "state": "warn", "t": "네비우스"}],
           beats=[{"say": "이 회사들에는 공통점이 있습니다. 엔비디아가 증권 당국에 낸 6월 말 기준 보유 주식 보고서를 보면, 엔비디아는 인텔 주식을 약 300억 달러, 코어위브를 약 47억 달러어치 갖고 있습니다.", "upto": 2},
                  {"say": "광통신 부품 회사 코히런트, 통신 장비 회사 노키아, 반도체 설계 소프트웨어 회사 시놉시스의 지분도 있고, 네비우스는 9.3%를 갖고 있습니다. 엔비디아의 지분 목록이 곧 엔비디아의 공급망과 고객 지도인 셈입니다.", "upto": 4}]))
    s(dict(type="bars", chapter=4, label=PX, title="엔비디아 지분 회사·부품·메모리 (%)", unit="", emph=0, skin=DS,
           items=[{"label": "코히런트", "value": -6.98, "text": "-6.98", "t": "코히런트"}, {"label": "인텔", "value": -4.54, "text": "-4.54", "t": "인텔"},
                  {"label": "노키아", "value": -4.38, "text": "-4.38", "t": "노키아"}, {"label": "마이크론", "value": -4.07, "text": "-4.07", "t": "마이크론은"},
                  {"label": "TSMC", "value": -3.54, "text": "-3.54", "t": "TSMC는"}],
           beats=B("그리고 이 회사들이 함께 내렸습니다. 같은 이틀 동안 코히런트는 6.98%, 인텔은 4.54%, 노키아는 4.38% 내렸습니다.",
                   "엔비디아 칩 옆에 붙는 메모리를 만드는 마이크론은 4.07%, 엔비디아 칩을 생산하는 TSMC는 3.54% 내렸습니다. 엔비디아의 공급망을 따라 흔들림이 번진 모양입니다.")))
    s(dict(type="bars", chapter=4, label=PX, title="버틴 쪽: 고객과 전력 (%)", unit="", emph=1, skin=DS,
           layers=[{"kind": "photo", "src": "dc", "beat": 0, "side": "left", "w": 380, "top": 300, "caption": f"데이터센터 · {cr['dc']}"}],
           items=[{"label": "메타", "value": 2.05, "text": "+2.05", "t": "메타"}, {"label": "컨스텔레이션", "value": 1.99, "text": "+1.99", "t": "컨스텔레이션"},
                  {"label": "구글", "value": 0.79, "text": "+0.79", "t": "구글"}, {"label": "MS", "value": 0.53, "text": "+0.53", "t": "마이크로소프트"},
                  {"label": "브로드컴", "value": 0.52, "text": "+0.52", "t": "브로드컴도"}],
           beats=B("반대로 버틴 쪽도 있습니다. 엔비디아 칩을 사는 고객인 빅테크는 메타 2.05%, 구글 0.79%, 마이크로소프트 0.53% 올랐습니다.",
                   "데이터센터에 전기를 대는 컨스텔레이션 에너지는 1.99%, 경쟁 칩을 만드는 브로드컴도 0.52% 올랐습니다. 같은 이틀 동안 반도체 지수는 3.95% 내렸습니다.")))
    s(dict(type="map_causal", chapter=4, look="board", label="자체 해석 · 근거: 업종별 종가(11일→13일), 엔비디아 13F·13G · 이틀 숫자라 인과 단정 안 함",
           map={"nodes": {"nv": {"label": "엔비디아의 돈·지분·협력", "icon": "handshake", "x": 960, "y": 300},
                          "cl": {"label": "흔들림: AI 클라우드·사모 금융", "icon": "trending-down", "x": 380, "y": 560},
                          "sp": {"label": "흔들림: 지분 공급사·메모리", "icon": "trending-down", "x": 380, "y": 820},
                          "cu": {"label": "버팀: 빅테크 고객·전력", "icon": "trending-up", "x": 1540, "y": 560},
                          "cv": {"label": "겹친 일: 금리↑·네비우스 실적", "icon": "circle-alert", "x": 1540, "y": 820}},
                "edges": [["nv", "cl"], ["nv", "sp"], ["nv", "cu"]]},
           beats=[{"say": "여기서부터는 해석입니다. 엔비디아와 돈, 지분, 협력으로 묶인 곳일수록 더 흔들렸고, 엔비디아의 칩을 사는 고객과 데이터센터의 전력은 버텼습니다. 시장은 이번 일을 AI 수요가 꺾였다는 신호가 아니라, 엔비디아의 돈과 관계가 흔들릴 수 있다는 신호로 읽은 것으로 볼 수 있습니다.",
                   "reveal": ["nv", "cl", "sp", "cu"], "draw": [["nv", "cl"], ["nv", "sp"], ["nv", "cu"]], "active": "cl"},
                  {"say": "다만 이틀의 숫자입니다. 같은 기간 미국 10년물 금리가 5.00%에서 5.15%로 올랐고, 네비우스의 실적도 겹쳤습니다. 함께 움직였다는 것까지가 사실이고, 원인을 하나로 단정할 수는 없습니다.",
                   "reveal": ["cv"], "draw": [], "active": "cv"}]))
    s(dict(type="chapter", chapter=5, num="5", title="칩보다 먼저 흔들리는 것", icon="handshake", look="board",
           beats=B("그런데 업황과 경영을 구분하고 나면, 그 사이에 하나가 남습니다.")))
    s(dict(type="quote", chapter=5, label="헤럴드경제 (2026.11.13) 보도 속 발언 · 유안타증권 이재원 연구원", who="이재원", role="유안타증권 연구원 · 11월 13일",
           quote="창업자의 의지 없이는 어려웠을 의사결정이며, 후임 체제에서도 생태계 지원 속도와 범위가 유지되는지 확인이 필요하다.", keyword="생태계 지원",
           beats=B("같은 연구원은 한 가지를 더 짚었습니다. 엔비디아가 8월에 대형 금융사들과 대규모 인프라 자금을 모으고, 칩의 잔존 가치를 보증하기로 한 결정은, 창업자의 의지 없이는 어려웠을 것이라는 겁니다.",
                   "다올투자증권도 걱정할 점으로 AI 생태계에 대한 금융 지원이 계속될 수 있느냐를 꼽았습니다. 칩도, 로드맵도 아닌, 돈의 약속입니다.")))
    s(dict(type="checklist", chapter=5, label="엔비디아 2분기 실적 보도자료·CFO 코멘터리 (2026.8.26, SEC 8-K)", title="창업자 시절에 건 돈의 약속", x=150, text_w=860, skin=NP,
           rows=[{"label": "부품을 미리 사겠다는 약속: 2,790억 달러 (대부분 메모리)", "state": "warn", "t": "2,790억"},
                 {"label": "고객 데이터센터 임대 보증: 최대 1,085억 달러", "state": "warn", "t": "1,085억"},
                 {"label": "6개 금융사와 금융 플랫폼: 5,000억 달러+ (확정 전)", "state": "warn", "t": "5,000억"},
                 {"label": "대금 회수 기간: 45일 → 60일", "state": "warn", "t": "60일"}],
           beats=[{"say": "그 약속은 8월 공시에 숫자로 남아 있습니다. 부품을 미리 사겠다는 약속이 2,790억 달러, 대부분 메모리입니다. 고객이 빌린 데이터센터의 임대료를 최대 1,085억 달러까지 보증했습니다. 그 가운데 1,050억 달러는 오픈AI가 쓸 오하이오 부지입니다.", "upto": 2,
                   "motion": [M("오픈AI", "icon", id="oa", icon="🏗️", x=1620, y=420, d=170, label="오하이오 부지")]},
                  {"say": "금융사들과 5,000억 달러가 넘는 금융 플랫폼을 만들기로 했고, 대형 고객의 대금 기한도 늘려 돈을 받는 기간이 45일에서 60일로 길어졌습니다. 당시 황 최고경영자는 수요가 가속하고 있다고 말했습니다.", "upto": 4,
                   "motion": [M("가속", "icon", id="ac", icon="🚀", x=1620, y=740, d=170, label="'수요 가속'")]}]))
    s(dict(type="map_causal", chapter=5, look="board", label="자체 해석 · 근거: 엔비디아 공시, 유안타·다올 분석(헤럴드경제), 이사회 보도자료",
           map={"nodes": {"ceo": {"label": "창업자의 결정", "icon": "user", "x": 300, "y": 330},
                          "prom": {"label": "보증·금융 지원·대금 기한", "icon": "handshake", "x": 960, "y": 330},
                          "cust": {"label": "AI 클라우드·오픈AI 데이터센터", "icon": "server", "x": 1620, "y": 330},
                          "ord": {"label": "칩·메모리 주문", "icon": "microchip", "x": 1620, "y": 780},
                          "rev": {"label": "엔비디아 매출", "icon": "trending-up", "x": 960, "y": 780},
                          "q": {"label": "새 체제도 이어갈까?", "icon": "circle-alert", "x": 300, "y": 780}},
                "edges": [["ceo", "prom"], ["prom", "cust"], ["cust", "ord"], ["ord", "rev"], ["rev", "q"], ["q", "prom"]]},
           beats=[{"say": "여기서부터는 해석입니다. 창업자의 결정이 고객에게 보증과 금융 지원을 주고, 그 덕분에 고객은 데이터센터를 짓고, 칩과 메모리를 주문하고, 그 주문이 다시 엔비디아의 매출이 됩니다.",
                   "reveal": ["ceo", "prom", "cust", "ord", "rev"], "draw": [["ceo", "prom"], ["prom", "cust"], ["cust", "ord"], ["ord", "rev"]], "active": "rev"},
                  {"say": "고리의 첫 칸에 있던 사람이 떠났습니다. 새 경영진이 이 약속을 같은 속도로 이어 가느냐가, 이번 사임에서 가장 먼저 확인해야 할 질문입니다. 이사회가 굳이 고객과의 약속을 언급한 이유도 여기에 있다고 봅니다.",
                   "reveal": ["q"], "draw": [["rev", "q"], ["q", "prom"]], "active": "q"}]))
    s(dict(type="chapter", chapter=6, num="6", title="직접 계산해 본 약속의 크기", icon="landmark", look="photo", bg_src="nvidia",
           beats=B("이 약속과 지분이 얼마나 큰지, 공시 숫자로 직접 계산해 보겠습니다.")))
    s(dict(type="bignum", chapter=6, label="계산: 엔비디아 13F·13G 보유 주식 수 × 11일→13일 종가 차이 · 6월 이후 매매는 미반영", small="엔비디아 지분 평가액, 이틀 동안 줄어든 금액", value="약 20.6억 달러",
           compare={"label": "그중 네비우스", "value": "8.64억 달러"}, skin=DS,
           beats=B("엔비디아가 지분을 가진 회사의 주가가 빠지면, 엔비디아의 장부도 함께 줄어듭니다. 6월 말 보유 주식 수에 이틀 동안의 주가 변화를 곱해 보면, 지분 평가액은 약 20.6억 달러 줄었습니다.",
                   "그중 가장 큰 몫은 네비우스로 8.64억 달러입니다. 6월 이후 사고판 내역은 아직 공시되지 않아 실제와는 다를 수 있지만, 사업 관계뿐 아니라 엔비디아 자신의 장부도 함께 흔들렸다는 뜻입니다.")))
    s(dict(type="bignum", chapter=6, label="계산: 엔비디아 2분기 CFO 코멘터리 (2026.8.26) · 보증은 단계적으로 효력", small="고객 임대 보증 최대 1,085억 달러 ÷ 현금·유가증권 566억 달러 (2분기 말)", value="약 1.9배",
           compare={"label": "부품 약속 ÷ 2분기 매출", "value": "약 2.9배"}, skin=DS,
           layers=[{"kind": "photo", "src": "dc", "beat": 1, "side": "right", "w": 340, "top": 640, "caption": f"데이터센터 · {cr['dc']}"}],
           beats=B("두 번째 계산입니다. 엔비디아가 고객의 임대에 선 보증은 최대 1,085억 달러로, 2분기 말 현금과 유가증권 566억 달러의 약 1.9배입니다.",
                   "부품을 사겠다는 약속 2,790억 달러는 2분기 매출의 약 2.9배입니다. 보증은 단계적으로 효력이 생겨 당장 돈이 나가지는 않지만, 그만큼 큰 약속을 임시 경영진이 이어받았다는 뜻입니다.")))
    s(dict(type="chapter", chapter=7, num="7", title="연준이 본 같은 고리", icon="landmark", look="photo", bg_src="fed",
           beats=B("이 고리는 엔비디아 한 회사만의 이야기가 아닙니다. 같은 주, 미국 중앙은행도 이 고리를 짚었습니다.")))
    s(dict(type="map_causal", chapter=7, look="board", label="연준 금융안정보고서 (2026.11.13) Box 2.2 · Box 5.1 (설문은 연준 공식 견해 아님, 비율은 로이터 보도)",
           map={"nodes": {"gpu": {"label": "GPU 회사: 잔존가치 보증·지분 투자", "icon": "microchip", "x": 330, "y": 340},
                          "dev": {"label": "데이터센터 개발사·AI 클라우드", "icon": "server", "x": 1000, "y": 340},
                          "big": {"label": "빅테크: 장기 임차", "icon": "building-2", "x": 1600, "y": 560},
                          "loan": {"label": "그 계약을 담보로 대출", "icon": "landmark", "x": 1000, "y": 790},
                          "buy": {"label": "칩 구매 → GPU 회사 매출", "icon": "trending-up", "x": 330, "y": 790}},
                "edges": [["gpu", "dev"], ["big", "dev"], ["dev", "loan"], ["loan", "buy"], ["buy", "gpu"]]},
           beats=[{"say": "11월 13일 연준의 금융안정보고서는, GPU 회사가 칩의 가치를 보증하고 지분까지 투자하며, 개발사가 그 계약을 담보로 돈을 빌려 다시 칩을 사는 구조를 순환 금융이라고 불렀습니다.",
                   "reveal": ["gpu", "dev", "big", "loan", "buy"], "draw": [["gpu", "dev"], ["big", "dev"], ["dev", "loan"], ["loan", "buy"], ["buy", "gpu"]], "active": "gpu"},
                  {"say": "로이터 보도에 따르면 이 보고서의 설문에서 AI를 금융 위험으로 꼽은 비율은 87%였습니다. 로이터는 이 설문이 엔비디아 최고경영자 사임 전에 이뤄졌다는 점도 짚었습니다. 고리의 맨 앞 칸이 흔들린 것은, 그 뒤의 일입니다.", "active": "buy"}]))
    s(dict(type="bars", chapter=7, label="연준 금융안정보고서 (2026.11.13) Box 2.2", title="AI 컴퓨팅 인프라용 채권 발행 (억 달러)", unit="", emph=1, skin=DS,
           layers=[{"kind": "photo", "src": "fed", "beat": 0, "side": "left", "w": 380, "top": 300, "caption": f"연준 에클스 빌딩 · {cr['fed']}"}],
           items=[{"label": "2023년", "value": 1300, "text": "1,300", "t": "2023년"}, {"label": "2026년 10월까지", "value": 6800, "text": "6,800+", "t": "올해는"}],
           beats=[{"say": "이 고리를 도는 빚도 커졌습니다. AI 컴퓨팅 인프라를 짓느라 발행한 채권은 2023년 한 해 1,300억 달러였는데, 올해는 10월까지 6,800억 달러를 넘었습니다."},
                  {"say": "보고서는 아직 시작하지 않은 임대 계약이 1조 달러, 보증과 장기 계약 약속이 2조 달러를 넘는다고 적었습니다. 엔비디아의 보증은 그 큰 그물의 한 매듭입니다. 빚이 커질수록, 그 매듭을 쥔 사람의 결정도 무거워집니다.",
                   "motion": [M("1조", "count", id="l1", value="1조+", label="미개시 임대", x=1640, y=330, w=420, h=210, fs=100),
                              M("2조", "count", id="l2", value="2조+", label="보증·장기 계약", x=1640, y=620, w=420, h=210, fs=100)]}]))
    s(dict(type="map_causal", chapter=7, look="board", label="자체 해석 · 근거: 연준 보고서 5장 시나리오, 엔비디아 공시, 국내 증권가 분석(서울경제·헤럴드경제)",
           map={"nodes": {"hub": {"label": "젠슨 황 사임", "icon": "user", "x": 960, "y": 300},
                          "slow": {"label": "새 체제가 지원 속도 조절", "icon": "trending-down", "x": 420, "y": 560},
                          "keep": {"label": "지원 유지·로드맵 그대로", "icon": "trending-up", "x": 1500, "y": 560},
                          "chain": {"label": "자금 조달↓·투자↓·주문↓", "icon": "circle-alert", "x": 420, "y": 820},
                          "issue": {"label": "'경영 이슈'로 남음", "icon": "landmark", "x": 1500, "y": 820}},
                "edges": [["hub", "slow"], ["hub", "keep"], ["slow", "chain"], ["keep", "issue"]]},
           beats=[{"say": "여기서부터는 해석입니다. 앞으로의 길은 둘로 갈립니다. 새 경영진이 보증과 금융 지원의 속도를 늦추면, 그 돈에 기대던 AI 클라우드의 자금 조달이 어려워지고, 데이터센터 투자와 칩 주문이 줄 수 있습니다. 연준이 그린 경로와 같은 방향입니다.",
                   "reveal": ["hub", "slow", "chain"], "draw": [["hub", "slow"], ["slow", "chain"]], "active": "chain"},
                  {"say": "반대로 약속과 로드맵이 그대로 이어지면, 이번 일은 시장을 놀라게 한 경영 이슈로 남을 가능성이 큽니다. 어느 쪽인지는 아직 아무도 확인하지 못했습니다.",
                   "reveal": ["keep", "issue"], "draw": [["hub", "keep"], ["keep", "issue"]], "active": "issue"},
                  {"say": "서울경제는 새 경영진의 투자 속도 조절과 미국의 대중국 수출 규제를 여전히 남은 변수로 꼽았습니다. 두 가지 모두 공장이나 기술이 아니라, 사람이 내리는 결정의 문제라는 점이 이번 사건의 성격을 보여 줍니다.", "active": "hub"}]))
    s(dict(type="chapter", chapter=8, num="8", title="창업자가 떠난 날, 같은 틀로", icon="calendar", look="photo", bg_src="nyse",
           beats=B("창업자가 최고경영자 자리에서 물러난 날은 처음이 아닙니다. 과거의 세 번을 같은 틀로 재 보겠습니다.")))
    s(dict(type="bars", chapter=8, label="야후 파이낸스 종가 · 발표일 종가 → 다음 날 (애플은 분할 조정)", title="창업자 CEO 사임 다음 날 주가 (%)", unit="", emph=3, skin=DS,
           items=[{"label": "MS 2000", "value": 4.10, "text": "+4.10", "t": "마이크로소프트는"}, {"label": "애플 2011", "value": -0.67, "text": "-0.67", "t": "애플은"},
                  {"label": "아마존 2021", "value": -1.99, "text": "-1.99", "t": "아마존은"}, {"label": "엔비디아 2026", "value": -4.34, "text": "-4.34", "t": "엔비디아는"}],
           beats=[{"say": "다음 날 주가부터 보겠습니다. 2000년 게이츠가 물러난 다음 날 마이크로소프트는 4.10% 올랐고, 2011년 잡스가 물러난 다음 날 애플은 0.67%, 2021년 베이조스 때 아마존은 1.99% 내렸습니다."},
                  {"say": "엔비디아는 4.34% 내렸습니다. 같은 날 나스닥은 0.39% 내렸으니, 시장보다 약 3.9%포인트 더 빠진 셈입니다. 세 회사보다 첫날 반응이 컸습니다.",
                   "motion": [M("0.39%", "count", id="nq", value="-0.39%", label="같은 날 나스닥", x=560, y=830, w=380, h=170, fs=72)]}]))
    s(dict(type="checklist", chapter=8, label="회사 발표(당시) · 이름과 역할만", title="무엇이 달랐나: 교체의 모양", x=150, text_w=900, skin=NP,
           rows=[{"label": "애플: 후임 쿡 바로 · 잡스는 이사회 의장으로", "state": "ok", "t": "애플"},
                 {"label": "마이크로소프트: 후임 발머 바로 · 게이츠는 회장으로", "state": "ok", "t": "마이크로소프트"},
                 {"label": "아마존: 후임 재시 예고 · 베이조스는 이사회 의장으로", "state": "ok", "t": "아마존"},
                 {"label": "엔비디아: 후임 미정, 임시 CEO · 창업자는 이사회에서도 떠남", "state": "warn", "t": "엔비디아는"}],
           beats=[{"say": "차이는 교체의 모양에 있습니다. 세 회사는 후임이 바로 정해졌고, 떠나는 창업자는 이사회 의장이나 회장으로 남았습니다.", "upto": 3},
                  {"say": "엔비디아는 후임이 정해지지 않아 최고재무책임자가 임시로 겸하고, 창업자는 이사회에서도 떠났습니다. 계획된 교체와 갑작스러운 교체의 차이가, 첫날 반응의 차이로 나타난 것으로 볼 수 있습니다.", "upto": 4}]))
    s(dict(type="bars", chapter=8, label="야후 파이낸스 종가 · 발표일 → 약 1년 뒤", title="1년 뒤: 회사 vs 같은 기간 나스닥 (%)", unit="", emph=0, skin=DS,
           items=[{"label": "애플", "value": 69.12, "text": "+69.12", "t": "애플은"}, {"label": "나스닥 11~12", "value": 24.10, "text": "+24.10", "t": "나스닥의"},
                  {"label": "MS", "value": -54.44, "text": "-54.44", "t": "마이크로소프트는"}, {"label": "나스닥 00~01", "value": -39.16, "text": "-39.16", "t": "39.16%"},
                  {"label": "아마존", "value": -17.83, "text": "-17.83", "t": "아마존은"}, {"label": "나스닥 21~22", "value": -0.52, "text": "-0.52", "t": "0.52%"}],
           beats=B("그렇다면 1년 뒤는 어땠을까요? 애플은 69.12% 올라 같은 기간 나스닥의 24.10%를 크게 앞섰고, 마이크로소프트는 54.44% 내려 닷컴 붕괴로 39.16% 빠진 나스닥보다 더 빠졌습니다.",
                   "아마존은 17.83% 내렸고, 같은 기간 나스닥은 0.52% 내렸습니다. 여기서부터는 해석입니다. 1년 뒤를 가른 것은 창업자가 떠났다는 사실보다 아이폰, 닷컴 붕괴 같은 업황이었습니다. 엔비디아의 1년도 AI 투자라는 업황과, 창업자가 남긴 돈의 약속이 이어지느냐에 달려 있다고 봅니다.")))
    s(dict(type="chapter", chapter=9, num="9", title="한국으로 이어지는 줄", icon="microchip", look="photo", bg_src="seoul",
           beats=B("이 갈림길은 한국 시장과도 이어져 있습니다.")))
    s(dict(type="bars", chapter=9, label="야후 파이낸스 종가 · 아주경제·MTN 마감 보도 · 헤럴드경제(11.13) '안도 랠리'", title="한국, 13일 하루 (%)", unit="", emph=1, skin=DS,
           layers=[{"kind": "locator", "at": [126.98, 37.57], "label": "서울 · 11월 13일 마감", "beat": 0, "side": "left", "top": 170, "scale": 2.2}],
           items=[{"label": "코스피", "value": -0.98, "text": "-0.98", "t": "코스피는"}, {"label": "SK하이닉스", "value": -3.03, "text": "-3.03", "t": "SK하이닉스는"},
                  {"label": "삼성전자", "value": -0.96, "text": "-0.96", "t": "삼성전자는"}],
           beats=[{"say": "사임 소식이 전해진 13일, 국내 매체들은 삼성전자와 SK하이닉스의 안도 랠리를 전했습니다. 엔비디아의 경영 문제와 반도체 업황은 다르다는 해석이었습니다."},
                  {"say": "하지만 마감은 달랐습니다. 장 초반 오름세는 이어지지 못했고, 코스피는 0.98%, SK하이닉스는 3.03%, 삼성전자는 0.96% 내렸습니다. 외국인은 하루에 5천억 원 넘게 팔았습니다. 매체의 제목과 그날의 마감이 달랐다는 것, 그것이 이번 주 한국 시장이 보여 준 신호였습니다.",
                   "motion": [M("5천억", "count", id="fx", value="5천억 원+", label="13일 외국인 순매도", x=1660, y=770, w=320, h=180, fs=64)]}]))
    s(dict(type="bars", chapter=9, label="야후 파이낸스 종가 · 11일 → 13일 · 네이버·SK텔레콤은 엔비디아와 한국 AI 공장 협력(8월 보도자료)", title="한국 AI·반도체, 이틀 등락 (%)", unit="", emph=0, skin=DS,
           layers=[{"kind": "photo", "src": "seoul", "beat": 0, "side": "left", "w": 360, "top": 300, "caption": f"서울 여의도 · {cr['seoul']}"}],
           items=[{"label": "네이버", "value": -11.22, "text": "-11.22", "t": "네이버는"}, {"label": "SK하이닉스", "value": -4.78, "text": "-4.78", "t": "SK하이닉스는"},
                  {"label": "한미반도체", "value": -1.25, "text": "-1.25", "t": "한미반도체는"}, {"label": "삼성전자", "value": 0.0, "text": "0.00", "t": "삼성전자는"},
                  {"label": "SK텔레콤", "value": 1.45, "text": "+1.45", "t": "SK텔레콤은"}],
           beats=B("이틀로 넓혀 보면 차이가 더 분명합니다. 엔비디아와 한국에 AI 공장을 함께 짓기로 한 네이버는 11.22%, SK하이닉스는 4.78%, 고대역폭 메모리 장비를 만드는 한미반도체는 1.25% 내렸습니다.",
                   "반면 삼성전자는 제자리였고, SK텔레콤은 1.45% 올랐습니다. 같은 AI·반도체 업종 안에서도, 엔비디아와 얼마나 깊이 묶여 있느냐에 따라 반응이 갈린 것으로 볼 수 있습니다.")))
    s(dict(type="map_causal", chapter=9, look="board", label="서울경제(11.15)·시대 사설(11.13)·미래에셋(서울경제 인용)·엔비디아 2분기 보도자료 · 마지막 문장은 자체 해석",
           map={"nodes": {"hub": {"label": "젠슨 황 사임", "icon": "user", "x": 960, "y": 300},
                          "cn": {"label": "중국 협상·고객·투자 전략 (서울경제)", "icon": "circle-alert", "x": 380, "y": 560},
                          "hbm": {"label": "HBM 수요는 유지 (미래에셋)", "icon": "microchip", "x": 1540, "y": 560},
                          "dep": {"label": "특정 고객 의존 경계 (사설)", "icon": "circle-alert", "x": 380, "y": 830},
                          "mem": {"label": "메모리 약속이 이어지나", "icon": "handshake", "x": 1540, "y": 830}},
                "edges": [["hub", "cn"], ["hub", "hbm"], ["cn", "dep"], ["hbm", "mem"]]},
           beats=[{"say": "국내 매체들은 질문을 이렇게 정리했습니다. 젠슨 황이 이끌던 중국 수출 협상과 고객 관계, 투자 지원 전략이 바뀌면 삼성전자와 SK하이닉스에도 영향이 갈 수 있다는 것입니다. 반면 미래에셋증권은 주문이 다른 칩으로 옮겨 가도 고대역폭 메모리 수요 자체가 급감할 가능성은 낮다고 봤습니다.",
                   "reveal": ["hub", "cn", "hbm"], "draw": [["hub", "cn"], ["hub", "hbm"]], "active": "hbm"},
                  {"say": "한 사설은 특정 고객에 대한 의존을 경계해야 한다고 썼습니다. 여기서부터는 해석입니다. 엔비디아가 8월에 발표한 SK하이닉스와의 메모리 다년 협력, 그리고 2,790억 달러 부품 약속의 대부분이 메모리라는 점을 함께 보면, 약속이 이어지느냐가 한국에 가장 직접적인 변수라고 볼 수 있습니다.",
                   "reveal": ["dep", "mem"], "draw": [["cn", "dep"], ["hbm", "mem"]], "active": "mem"}]))
    s(dict(type="chapter", chapter=10, num="10", title="주의할 점", icon="circle-alert", look="board",
           beats=B("이런 사건일수록 해석보다 먼저 조심해야 할 것들이 있습니다.")))
    s(dict(type="checklist", chapter=10, label="팩트시트 '주의할 점' · 투자 권유가 아닙니다", title="이번 사건, 이렇게 보지 않기", x=150, text_w=900, skin=NP,
           rows=[{"label": "사생활 보도와 사업 영향은 다른 문제", "state": "warn", "t": "사생활"},
                 {"label": "하루 주가로 결론 내지 않기 (장중 -13% → 마감 -4.34%)", "state": "warn", "t": "하루"},
                 {"label": "대안주 쏠림은 다음 날 되돌아왔다 (AMD -8.75%)", "state": "warn", "t": "대안주"},
                 {"label": "확인 안 된 후속 소식(복귀설 등)은 공시 전까지 단정 금지", "state": "warn", "t": "복귀설"},
                 {"label": "목표가 숫자보다 근거(로드맵·후계·금융 지원)를 보기", "state": "ok", "t": "근거"}],
           beats=[{"say": "첫째, 사생활 보도와 사업 영향은 다른 문제입니다. 둘째, 하루 주가로 결론을 내지 않습니다. 장 초반 13% 넘게 빠졌던 주가는 4.34% 하락으로 마감했고, 대안으로 몰렸던 돈은 다음 날 일부 되돌아왔습니다.", "upto": 3},
                  {"say": "셋째, 복귀설 같은 확인되지 않은 후속 소식은 공시가 나오기 전까지 단정하지 않습니다. 그리고 애널리스트의 목표가 숫자보다, 그 숫자를 만든 근거가 로드맵인지 후계인지 금융 지원인지를 보는 편이 더 오래 쓸모 있습니다.", "upto": 5}]))
    s(dict(type="checklist", chapter=10, label="팩트시트 '틀리는 경우' · 투자 권유가 아닙니다", title="이 해석이 틀리는 경우 셋", x=150, text_w=920, skin=NP,
           rows=[{"label": "① 18일, 약속·보증 그대로 + 새 경영진이 지원 지속을 밝힘", "state": "ok", "t": "첫째"},
                 {"label": "② 업종 하락이 사임보다 금리(10년물 5.15%)·개별 실적 때문", "state": "ok", "t": "둘째"},
                 {"label": "③ 내부 후계자를 빠르게 정식 CEO 로", "state": "ok", "t": "셋째"}],
           beats=[{"say": "이 영상의 해석이 틀릴 수 있는 경우도 적어 둡니다. 첫째, 18일 실적에서 보증과 부품 약속이 그대로이고 새 경영진이 생태계 지원을 이어 간다고 밝히면, 돈의 약속에 대한 걱정은 과했던 것입니다.", "upto": 1},
                  {"say": "둘째, 흔들린 업종의 하락이 사임보다 금리나 개별 실적 때문이었다고 드러나는 경우입니다. 셋째, 이사회가 빠르게 내부 후계자를 정식 최고경영자로 세우면, 과거의 계획된 교체에 가까워져 공백이 짧아집니다.", "upto": 3}]))
    s(dict(type="kinetic", chapter=10, beats=[{"say": "칩보다 먼저 흔들리는 것은, 약속입니다.", "hit": ["칩보다", "약속입니다."]}]))
    s(dict(type="analogy", chapter=10, label="비유 · 과거 비교는 보도(야후 파이낸스, 한 애널리스트의 '스티브 잡스 순간' 비유)", title="악보는 남았고, 지휘자가 바뀌었다",
           left={"icon": "layers", "label": "악보", "sub": "로드맵·공급망: 2028년까지 확정"}, right={"icon": "user", "label": "지휘자", "sub": "템포: 투자·금융 지원의 속도"},
           result={"icon": "circle-alert", "label": "곡은 같아도 템포는 바뀔 수 있다"},
           beats=[{"say": "오케스트라에 비유하면, 악보는 남았고 지휘자가 바뀐 상황입니다. 로드맵과 공급망이라는 악보는 2028년까지 쓰여 있습니다. 하지만 곡의 빠르기, 그러니까 투자와 금융 지원의 속도는 지휘자가 정합니다."},
                  {"say": "한 애널리스트는 이번 일을 2011년 애플의 스티브 잡스 순간에 비유했습니다. 창업자가 떠난 뒤의 평가는, 첫날 주가가 아니라 새 경영진이 내리는 다음 결정들로 정해진다는 뜻입니다.", "show_result": True}]))
    s(dict(type="chapter", chapter=11, num="11", title="확인할 신호 셋", icon="calendar", look="board",
           beats=B("그렇다면 무엇을 보면 어느 쪽인지 알 수 있을까요?")))
    s(dict(type="checklist", chapter=11, label="11월 15일 기준 일정 (한국 시간) · 기준선은 이 영상이 정한 것 · 투자 권유가 아닙니다", title="기준선이 있는 신호", skin=NP,
           rows=[{"label": "① 18일(수) 06:20 — 보증 1,085억·부품 약속 2,790억 달러가 줄었나, 늘었나", "state": "warn"},
                 {"label": "② 매출채권 회수 기간이 60일보다 길어지나", "state": "warn"},
                 {"label": "③ 코어위브 60.77·네비우스 154.69달러 회복 · 미 10년물 5% 아래", "state": "warn"}],
           beats=[{"say": "첫째, 한국 시간 18일 새벽 6시 20분 실적입니다. 매출이 1,058억에서 1,102억 달러 범위 안에 드는지와 함께, 보증 1,085억 달러와 부품 약속 2,790억 달러가 줄었는지 늘었는지를 봅니다. 줄면 속도 조절, 늘면 지속의 신호입니다.", "upto": 1,
                   "motion": [M("1,058억", "count", id="g1", value="1,058~1,102억", label="3분기 매출 범위 (달러)", x=1500, y=820, w=520, h=170, fs=60)]},
                  {"say": "둘째, 돈을 받기까지 걸리는 기간이 60일보다 더 길어지는지입니다. 셋째, 코어위브가 11일 종가 60.77달러를, 네비우스가 154.69달러를 되찾는지, 그리고 미국 10년물 금리가 5% 아래로 내려오는지입니다. 시장이 돈의 관계에 대한 걱정을 거두는지 보여 줄 숫자들입니다.", "upto": 3}]))
    s(dict(type="outro", chapter=11, title="11월 15일까지의 자료", sub="출처는 설명란에", clip={"src": "nvidia", "start": 0},
           beats=B("딱 하나만 기억한다면, 이것입니다. 창업자는 떠났지만 그가 고객에게 걸어 둔 약속은 아직 장부에 남아 있고, 시장은 칩보다 그 약속을 먼저 걱정했습니다. 18일 새벽, 새 경영진은 그 약속을 어떻게 말할까요? 출처는 모두 설명란에 남겨 두겠습니다.")))
    for i, x in enumerate(S, 1):
        x["id"] = i
    spec = {
        "title": "젠슨 황이 떠난 엔비디아, 칩보다 먼저 흔들리는 것 — 돈의 약속·업종별 영향·같은 틀 역사 비교",
        "brand": "market",
        "core_message": "젠슨 황 사임으로 엔비디아는 한 주 12.75% 내렸지만 로드맵·공급망은 확정돼 있다. 먼저 흔들리는 것은 창업자가 건 돈의 약속(보증 최대 1,085억·금융 플랫폼 5,000억+·대금 기한)이고, 그 약속은 연준이 위험 1순위로 꼽은 순환 금융의 한 축이다. 해석은 낙관(확정된 계획)·우려(후계·이사회)·구분(경영≠업황)으로 갈리며, 18일 크레스의 첫 설명이 향방을 가른다.",
        "question": "창업자가 떠난 엔비디아에서, 칩보다 먼저 흔들리는 것은 무엇일까?",
        "logic": ["여는 장면: 11/11 8-K 사임 수락 → 크레스 임시 CEO·존스 첫 의장 → 엔비디아 9·10·12·13일 하락, 주간 -12.75%",
                  "1) 일주일: 9일 조사 보도 → 11일 사임 → 18일 실적 예정대로 · 이사회 '고객과의 약속 중단 없이'",
                  "2) 시장: AMD +18.93%·브로드컴 +18.16% vs 엔비디아 -12.75% → 13일 되돌림 · 해석: 낙관(번스타인·삼성증권) / 우려(멜리우스·포천) / 구분(유안타)",
                  "3) 돈의 약속: 유안타·다올 '생태계 금융 지원 영속성' → 공급 약속 2,790억·보증 1,085억·금융 5,000억+·회수 45→60일 → 해석: 고리의 첫 칸이 비었다",
                  "4) 연준: 순환 금융·AI 위험 87%(사임 전 설문, 로이터) · AI 채권 1,300억→6,800억+, 미개시 임대 1조+·보증 2조+ → 해석: 두 갈래(속도 조절 vs 유지)",
                  "5) 한국: 13일 '안도 랠리' 보도 vs 마감 하락·외국인 5천억+ 매도 · 중국 협상·고객 관계(서울경제), HBM 수요 유지(미래에셋), 의존 경계(사설)",
                  "6) 주의할 점: 사생활≠사업, 하루 주가, 대안주 되돌림, 복귀설, 목표가보다 근거 · 지휘자 비유·잡스 비교(보도)",
                  "신호: 18일 실적의 약속·보증, 07:00 콜, 정식 CEO, 19일 의사록"],
        "compare_to": [{"value": "엔비디아 주간 -12.75%", "to": "AMD +18.93%·반도체 지수 +8.05%"},
                       {"value": "12일 마감 -4.34%", "to": "장 초반 -13%(보도)"},
                       {"value": "보증 최대 1,085억 달러", "to": "같은 분기 매출 962억 달러"},
                       {"value": "AI 인프라 채권 6,800억 달러+", "to": "2023년 1,300억 달러"}],
        "analogies": [{"a": "악보와 지휘자", "b": "로드맵(악보)은 확정, 투자·금융 지원의 속도(템포)는 새 경영진이 정함"},
                      {"a": "고리의 첫 칸", "b": "창업자의 결정 → 보증·금융 → 고객 데이터센터 → 주문 → 매출"}],
        "past_cases": [{"case": "2011년 애플 스티브 잡스 사임 (한 애널리스트의 비교, 보도)", "lesson": "창업자 이후 평가는 첫날 주가가 아니라 새 경영진의 다음 결정들로 정해진다"},
                       {"case": "1990년대 말 통신 투자 붐 (연준 보고서 비교)", "lesson": "빚과 약속으로 이어진 투자 고리는 한 곳이 흔들리면 함께 흔들린다"}],
        "glossary": [{"term": "8-K", "plain": "미국 상장사가 중요한 일이 생기면 며칠 안에 내는 공시"},
                     {"term": "임시 CEO", "plain": "정식 후임을 뽑을 때까지 회사를 맡는 최고경영자"},
                     {"term": "잔존가치 보증", "plain": "칩·장비를 나중에 팔 때 일정 값 이상을 보장해 주는 약속"},
                     {"term": "순환 금융", "plain": "큰 회사가 작은 회사에 돈을 대거나 보증하고, 그 작은 회사가 다시 큰 회사의 제품을 사는 고리"},
                     {"term": "HBM(고대역폭 메모리)", "plain": "AI 칩 옆에 붙어 데이터를 빠르게 주고받는 메모리. SK하이닉스·삼성전자가 만듦"},
                     {"term": "의사록", "plain": "연준 회의에서 오간 논의를 3주 뒤에 공개하는 기록"}],
        "scenes": S,
        "footage": fo,
        "package": {
            "title": "젠슨 황이 떠난 엔비디아, 칩보다 먼저 흔들리는 것 | 11월 15일",
            "title_options": ["젠슨 황이 떠난 엔비디아, 칩보다 먼저 흔들리는 것 | 11월 15일",
                              "보증 1,085억·금융 5,000억 — 창업자가 남긴 약속은 이어질까 | 11월 15일",
                              "젠슨 황 사임의 파급효과: 순환 금융·연준·한국 반도체, 엇갈린 해석까지 | 11월 15일"],
            "title_why": ["new_angle(칩보다 먼저 흔들리는 것) — 답은 숨김", "숫자 + 질문", "사건 + 뻗어 나간 경로 + 해석"],
            "thumbnails": [
                {"id": "A", "name": "엔비디아 간판 + 질문", "layout": "photo", "photo_side": "full", "image": {"file": "04_assets/footage/raw/nvidia.jpg", "focus": [0.5, 0.5]},
                 "top": "11월 15일 · 심층", "lines": ["젠슨 황이 떠난 뒤", "먼저 흔들리는 것"], "hl": ["먼저"], "sub": "칩이 아니라 약속", "size": 112, "text_y": 330, "marks": [],
                 "why": ["사건 + 질문"]},
                {"id": "B", "name": "숫자 대비", "layout": "versus", "left": {"value": "-12.75%", "label": "엔비디아 한 주"},
                 "right": {"value": "1,085억", "label": "남은 보증 (달러)"}, "headline": "주가는 빠졌고, 약속은 남았다", "hl": [], "marks": [], "why": ["사건 숫자 vs 약속 숫자"]},
                {"id": "C", "name": "연준 + 고리", "layout": "photo", "photo_side": "full", "image": {"file": "04_assets/footage/raw/fed.jpg", "focus": [0.5, 0.5]},
                 "top": "젠슨 황 사임 → 순환 금융 → 연준", "lines": ["고리의 첫 칸이", "비었다"], "hl": ["첫 칸"], "sub": "18일 실적에서 볼 것", "size": 110, "text_y": 330, "marks": [],
                 "why": ["구조로 뻗어 나감"]}]},
    }
    (P / "02_script" / "hybrid.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
    print(P, len(S))


if __name__ == "__main__":
    main()
