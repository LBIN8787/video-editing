"""첫영상 A/B 버전 대본 생성 (1회용 스크립트 — 대본 원본 기록용으로 보관).

A안: 뉴스·인터뷰 클립 인용 (식스시그마 방식, 저작권 위험 높음)
B안: 엔비디아·네이버 공식 영상 + 공시 카드 (권장)
내레이션은 공통이고, 화면 소스와 원본 발언(quote) 여부만 다르다.
팩트 근거: 20261105-첫영상/01_research/factsheet.md (F번호)
"""
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from ytflow.project import Project  # noqa: E402
from ytflow.stages.writing import write_script_md  # noqa: E402

BASE = ROOT / "projects" / "20261105-첫영상"

# ---- 소스 영상
BBG = "https://www.youtube.com/watch?v=IMWCcm7uDnk"     # Bloomberg TV, 젠슨 황 인터뷰 (뉴스)
JTBC = "https://www.youtube.com/watch?v=Zlf794eaco8"    # JTBC 뉴스, 3대 주주 보도
YTN = "https://www.youtube.com/watch?v=Y1FymUitqi4"     # YTN, GTC 타이완 '엔비디아♥네이버클라우드'
NEWSPLUS = "https://www.youtube.com/watch?v=f8wykPn9dB8"  # 네이버·브룩필드 1GW 보도
NV_TWIN = "https://www.youtube.com/watch?v=TRc0z_qcze0"   # NVIDIA 공식: AI 팩토리 디지털 트윈
NV_FACTORY = "https://www.youtube.com/watch?v=K6t4tusFZ5c"  # NVIDIA 공식: The AI Factory
NV_TAIPEI = "https://www.youtube.com/watch?v=wSp6AiNIrsY"   # NVIDIA 공식: GTC Taipei 2026 키노트
NV_GTC = "https://www.youtube.com/watch?v=jw_o0xr8MWU"      # NVIDIA 공식: GTC 2026 키노트
NAVER_CLOUD = "https://www.youtube.com/watch?v=OtrnlI0EP28"  # 네이버클라우드 공식 소개 영상
# 기사 (A안 헤드라인 캡처: clips 단계가 헤드라인 부분을 캡처)
KT = "https://www.koreatimes.co.kr/amp/business/tech-science/20260727/nvidia-invests-1-bil-in-naver-for-45-stake"
FOOL = "https://www.fool.com/investing/breakfast-news/2026/11/04/breakfast-news/"
STOCKPLUS = "https://newsroom.stockplus.com/breaking-news/41942"

L_BBG = "2026.07 · Bloomberg Television"
L_DISC = "2026.11.03 · 네이버 정정 공시"


def src(url, start="", end="", find="", length=10.0):
    return {"url": url, "start": start, "end": end, "find": find, "length": length}


def card(type_, title="", items=(), note=""):
    return {"type": type_, "title": title, "note": note,
            "items": [{"label": i[0], "value": i[1] if len(i) > 1 else "", "sub": i[2] if len(i) > 2 else "",
                       "highlight": bool(i[3]) if len(i) > 3 else False} for i in items]}


SHAREHOLDERS = card("number_compare", "납입 후 네이버 주주 순위",
                    [("1대", "국민연금", "9.49%"), ("2대", "블랙록", ""), ("3대 · NEW", "엔비디아", "약 4.13%", 1)],
                    "이해진 의장 4.03% → 약 3.8%")
INVEST_BARS = card("bars", "엔비디아 2026 지분 투자 (억 달러)",
                   [("코어위브 1월", "20"), ("오픈AI 2월", "300", "300"), ("루멘텀 3월", "20"), ("코히어런트 3월", "20"),
                    ("네비우스 3월", "20"), ("마벨 봄", "20"), ("코닝 5월", "5"), ("네이버 7월", "10", "10", 1)],
                   "확인된 8곳 합계 약 415억 달러")
COUNTER = card("table", "반론 세 가지",
               [("① 순환 투자", "투자한 돈이 GPU 구매로 돌아온다", "Barchart 논평"),
                ("② 규모", "엔비디아 1분기 매출의 약 1%", "대신증권"),
                ("③ 네이버의 숙제", "90억 달러 조달 아직 비구속", "Korea Times", 1)])


def N(section, text, emph, visual_type, brief, label, source=None, card_=None):
    return {"section": section, "kind": "narration", "narration": text, "quote_en": "", "emphasis": emph,
            "label": label, "source": source, "card": card_, "visual_type": visual_type, "visual_brief": brief,
            "image_prompt": ""}


def Q(section, en, ko, emph, label, source, brief):
    return {"section": section, "kind": "quote", "narration": ko, "quote_en": en, "emphasis": emph,
            "label": label, "source": source, "card": None, "visual_type": "source_video", "visual_brief": brief,
            "image_prompt": ""}


def build(version: str) -> list[dict]:
    A = version == "A"
    S = []
    add = S.append
    # ---------------- HOOK
    add(N("hook", "11월 6일, 엔비디아가 네이버에 1조 3,412억 원을 넣습니다.", ["1조 3,412억 원"],
          *(("source_video", "JTBC 보도 화면 (소리 끔)", "2026.10.30 · JTBC 뉴스", src(JTBC, "0:00", "0:08"), None) if A else
            ("card", "공시 헤드라인 카드", "2026.11.03 · 네이버 공시(DART)", None,
             card("headline", "엔비디아, 네이버 3대 주주로", [("신주 655만 8,435주 · 주당 20만 4,500원",), ("납입일 2026년 11월 6일", "", "", 1)],
                  "출처: 네이버 정정 공시 (2026.11.03)")))))
    add(N("hook", "그 순간 엔비디아는 국민연금, 블랙록 다음으로 네이버의 3대 주주가 됩니다.", ["3대 주주"],
          "card", "주주 순위", L_DISC, None, SHAREHOLDERS))
    add(N("hook", "올해 엔비디아가 이렇게 지분을 산 회사는 확인된 것만 여덟 곳, 들어간 돈은 400억 달러가 넘습니다.", ["400억 달러"],
          "card", "숫자 카드", "2026 · CNBC, Quartz 집계", None,
          card("number_compare", "", [("올해 지분을 산 회사", "8곳"), ("투자 금액", "400억 달러+", "", 1)])))
    add(N("hook", "칩을 파는 회사가 왜 칩을 사는 회사의 주식을 살까요? 젠슨 황의 말과 공시 숫자로 따라가 보겠습니다.", ["주식"],
          "source_video", "젠슨 황 화면 (소리 끔)",
          L_BBG if A else "2026 · NVIDIA GTC Taipei 키노트",
          src(BBG, "0:44", "0:52") if A else src(NV_TAIPEI, find="NAVER", length=8)))
    add(N("intro", "미리 말씀드리면, 이 영상은 특정 종목을 사거나 팔라는 이야기가 아닙니다.", [],
          "card", "면책 카드", "", None, card("text", "특정 종목의 매수·매도 권유가 아닙니다")))
    # ---------------- BODY-1 젠슨 황의 설명 + 딜 숫자
    if A:
        add(Q("body-1",
              "We're investing a billion dollars in Naver. They're Korea's leading AI cloud. "
              "They're going to scale up 200 megawatts, and they're going to expand across the world.",
              "우리는 네이버에 10억 달러를 투자합니다. 네이버는 한국을 대표하는 AI 클라우드입니다. 200메가와트 규모로 키우고, 세계로 확장할 겁니다.",
              ["10억 달러"], L_BBG, src(BBG, "1:14.0", "1:27.8"), "젠슨 황 인터뷰 원본 (원래 소리)"))
    else:
        add(N("body-1", "젠슨 황은 대만 GTC 기조연설에서 네이버 클라우드를 글로벌 핵심 파트너로 화면에 올렸습니다.", ["네이버 클라우드"],
              "source_video", "키노트 파트너 화면 (소리 끔)", "2026 · NVIDIA GTC Taipei 키노트", src(NV_TAIPEI, find="NAVER", length=10)))
    add(N("body-1", "정리하면, 엔비디아가 밝힌 이유는 네이버가 한국의 대표 AI 클라우드라는 점, 그리고 200메가와트라는 규모입니다.", ["200메가와트"],
          "source_video", "네이버 클라우드 화면 (소리 끔)",
          L_BBG if A else "NAVER Cloud 공식 영상", src(BBG, "1:28", "1:36") if A else src(NAVER_CLOUD, "0:05", "0:15")))
    add(N("body-1", "숫자는 한 번 바뀌었습니다. 7월 발표 땐 지분 약 4.5%, 1조 4,800억 원이었지만, 11월 3일 정정 공시에선 4.13%, 1조 3,412억 원입니다.", ["4.13%"],
          "card", "7월 vs 11월 비교", L_DISC, None,
          card("number_compare", "", [("7월 발표", "4.5%", "약 1조 4,800억 원"), ("11월 확정", "4.13%", "1조 3,412억 원", 1)])))
    add(N("body-1", "달러로는 그대로 10억 달러입니다. 그 사이 환율이 움직이면서 원화 금액과 주식 수만 줄었습니다.", ["10억 달러"],
          "card", "달러 고정 카드", L_DISC, None,
          card("table", "달러는 그대로, 원화만 줄었다", [("7월", "10억 달러", "724만 주 · 약 1조 4,800억 원"),
                                                  ("11월", "10억 달러", "655만 주 · 1조 3,412억 원", 1)])))
    add(N("body-1", "납입일은 10월 30일에서 11월 6일로 밀렸고, 신주 상장은 11월 27일입니다. 새 주식은 1년 동안 팔 수 없다고 알려져 있습니다.", ["11월 6일"],
          "card", "일정 흐름도", "2026.10.30 · 네이버 공시", None,
          card("flow", "일정", [("6월", "", "AI 팩토리 합의"), ("7월 27일", "", "투자 발표"), ("11월 3일", "", "금액 확정"),
                               ("11월 6일", "", "납입", 1), ("11월 27일", "", "신주 상장")])))
    # ---------------- BODY-2 조건
    add(N("body-2", "그런데 숫자보다 더 중요한 건 조건입니다.", ["조건"],
          "source_video", "AI 팩토리 관련 화면 (소리 끔)",
          "2026.07 · NEWSPLUS" if A else "NAVER Cloud 공식 영상",
          src(NEWSPLUS, "0:00", "0:06") if A else src(NAVER_CLOUD, "0:20", "0:26")))
    add(N("body-2", "보도에 따르면 엔비디아 투자는 네이버가 별도로 최소 90억 달러를 조달해야 성립합니다. 브룩필드가 최대 90억 달러를 대겠다는 비구속 조건에 서명해 둔 상태입니다.", ["90억 달러"],
          "card", "조건 표", "2026.07.27 · Korea Times, UPI", None,
          card("table", "엔비디아 투자의 조건", [("엔비디아", "10억 달러", "지분 약 4.13%"), ("브룩필드", "최대 90억 달러", "비구속 텀싯"),
                                         ("조건", "별도 90억 달러 조달", "확정돼야 투자 성립", 1)])))
    add(N("body-2", "그 돈이 향하는 곳은 AI 팩토리, GPU로 가득 채운 데이터센터입니다. 2028년까지 200메가와트, 길게는 1기가와트가 목표입니다.", ["1기가와트"],
          "source_video", "엔비디아 AI 팩토리 영상 (소리 끔)", "NVIDIA · AI Factory 공식 영상", src(NV_TWIN, "0:02", "0:14")))
    add(N("body-2", "돈의 순서를 그려 보면, 엔비디아와 브룩필드의 돈이 네이버로 들어가고, 네이버가 데이터센터를 짓고, 그 안을 채우는 건 엔비디아 GPU입니다.", ["엔비디아 GPU"],
          "card", "돈의 흐름도", "", None,
          card("flow", "돈이 흐르는 순서", [("엔비디아·브룩필드", "투자"), ("네이버", "건설"), ("AI 데이터센터", "구매"), ("엔비디아 GPU", "", "", 1)])))
    add(N("body-2", "엔비디아 입장에서 10억 달러는 열 배짜리 인프라를 움직이는 마중물인 셈입니다.", ["마중물"],
          "card", "10억 → 100억", "", None, card("number_compare", "", [("엔비디아가 넣는 돈", "10억 달러"), ("움직이는 인프라 자금", "100억 달러", "", 1)])))
    # ---------------- BODY-WHY
    if A:
        add(Q("body-why",
              "Well, we don't have enough bits. We're constrained in HBM memories, LPDDR memories. "
              "We're constrained in just about every part of the supply chain. "
              "We're even constrained now with land and power and construction workers to set up the data centers.",
              "메모리가 충분하지 않습니다. HBM도, LPDDR도 부족합니다. 공급망 거의 모든 곳이 막혀 있습니다. 이제는 데이터센터를 지을 땅과 전력, 건설 인력까지 부족합니다.",
              ["공급망"], L_BBG, src(BBG, "3:30.0", "3:45.0"), "젠슨 황 인터뷰 원본 (원래 소리)"))
        add(N("body-why", "젠슨 황 말대로 지금 병목은 칩만이 아닙니다. 땅과 전력, 그리고 그걸 감당할 돈입니다.", ["돈"],
              "source_video", "인터뷰 화면 (소리 끔)", L_BBG, src(BBG, "3:46", "3:54")))
    else:
        add(N("body-why", "엔비디아는 공급망 거의 모든 곳이 부족하다고 말해 왔습니다. 메모리와 전력, 땅, 데이터센터를 지을 인력까지입니다.", ["공급망"],
              "source_video", "AI 팩토리 건설 화면 (소리 끔)", "NVIDIA · AI Factory 공식 영상", src(NV_TWIN, "0:15", "0:30")))
        add(N("body-why", "지금 병목은 칩만이 아닙니다. 땅과 전력, 그리고 그걸 감당할 돈입니다.", ["돈"],
              "source_video", "AI 팩토리 화면 (소리 끔)", "NVIDIA · The AI Factory 공식 영상", src(NV_FACTORY, "0:10", "0:18")))
    add(N("body-why", "그래서 증권가는 왜 하필 네이버인가에 세 가지 답을 냅니다.", ["세 가지"],
          "card", "질문 카드", "", None, card("text", "왜 하필 네이버인가")))
    add(N("body-why", "자체 거대언어모델을 가진 소버린 AI 수요처라는 점, 한 해 2조 원이 넘는 이익과 안정적인 신용등급, 그리고 네이버가 얻는 최신 GPU 우선 공급입니다.", ["2조 원"],
          "card", "세 가지 이유 표", "2026.07 · 머니투데이, 연합인포맥스 분석", None,
          card("table", "증권가가 꼽은 이유", [("① 수요", "소버린 AI", "자체 거대언어모델 보유"),
                                         ("② 갚을 힘", "연 2조 원+ 이익", "안정적 신용등급", 1),
                                         ("③ 네이버가 얻는 것", "GPU 우선 공급", "엔비디아 생태계 편입")])))
    add(N("body-why", "빚이 늘면서 조달 금리가 오른 코어위브와 비교되는 지점입니다.", ["코어위브"],
          "card", "비교 카드", "2026.07 · 연합인포맥스 분석", None,
          card("number_compare", "", [("코어위브", "부채 ↑", "조달 금리 상승"), ("네이버", "2조 원+", "연간 이익", 1)])))
    # ---------------- BODY-3 지분 지도
    add(N("body-3", "6월 대만 GTC 기조연설 화면에는 엔비디아와 네이버 클라우드 사이에 붉은 하트가 올라갔습니다.", ["붉은 하트"],
          "source_video", "GTC 파트너 화면 (소리 끔)",
          "2026.06 · YTN (GTC 타이완 2026)" if A else "2026 · NVIDIA GTC Taipei 키노트",
          src(YTN, "0:24", "0:32") if A else src(NV_TAIPEI, find="NAVER", length=8)))
    add(N("body-3", "올해 엔비디아의 지분 투자를 놓아 보면, 1월 코어위브, 2월 오픈AI 300억 달러, 3월 루멘텀과 코히어런트, 네비우스, 봄에 마벨, 5월 코닝, 그리고 7월 네이버입니다.", ["300억 달러"],
          "card", "지분 투자 막대", "2026 · CNBC, Quartz, PhotonCap", None, INVEST_BARS))
    add(N("body-3", "이 회사들은 두 무리로 나뉩니다. GPU를 사 줄 고객, 그리고 엔비디아가 부품을 사야 하는 공급망입니다.", ["두 무리"],
          "card", "두 무리 표", "", None,
          card("table", "엔비디아 지분 지도", [("고객", "수요를 묶는다", "오픈AI · 코어위브 · 네비우스 · 네이버", 1),
                                         ("공급망", "물량을 묶는다", "루멘텀 · 코히어런트 · 코닝 · 마벨")])))
    add(N("body-3", "고객에게는 지분으로 수요를 붙잡고, 공급사에는 지분으로 부품 물량을 먼저 확보하는 구조입니다.", ["수요"],
          "source_video", "광통신·데이터센터 화면 (소리 끔)",
          "NVIDIA · AI Factory 공식 영상" if A else "2026 · NVIDIA GTC 키노트",
          src(NV_TWIN, "0:40", "0:50") if A else src(NV_GTC, find="Lumentum|Coherent|co-packaged", length=8)))
    add(N("body-3", "그 결과 엔비디아의 AI 기업 지분은 7월 기준 약 990억 달러, 1년 전보다 열 배 넘게 늘었다는 집계가 있습니다.", ["990억 달러"],
          "card", "보유액 비교", "2026.07.26 · Quartz", None,
          card("number_compare", "엔비디아의 AI 기업 지분 보유액", [("1년 전", "약 70억 달러"), ("2026년 7월", "약 990억 달러", "", 1)])))
    # ---------------- TURN
    add(N("turn", "최근에는 엔비디아가 투자한 마벨이, 역시 엔비디아가 투자한 루멘텀을 사들인다는 합병 소식까지 나왔습니다.", ["합병"],
          "card", "합병 흐름도", "2026.11 · Motley Fool, TradingKey 보도", None,
          card("flow", "엔비디아가 투자한 두 회사가 합친다", [("마벨", "+", "엔비디아 지분"), ("루멘텀", "", "엔비디아 지분"), ("합병 회사", "", "엔비디아 = 주주·고객", 1)],
               "금액·조건은 공식 발표로 재확인 필요")))
    add(N("turn", "어느 쪽이 이기든 엔비디아는 합쳐진 회사의 주주이자 큰 고객입니다. 지도 위의 점들이 이어지기 시작한 겁니다.", ["주주이자 큰 고객"],
          "card", "문장 카드", "", None, card("text", "지도 위의 점들이 이어지기 시작했다")))
    # ---------------- BODY-4 반론
    add(N("body-4", "물론 반론도 있습니다. 엔비디아가 넣은 돈이 결국 엔비디아 GPU 구매로 돌아온다면 매출이 부풀려 보일 수 있다는 순환 투자 비판, 그리고 10억 달러는 엔비디아 1분기 매출의 1% 정도라 실적 영향은 작다는 분석입니다.", ["순환 투자"],
          "card", "반론 표", "2026 · Barchart, 대신증권, Korea Times", None, COUNTER))
    add(N("body-4", "네이버 쪽 숙제도 있습니다. 90억 달러 조달은 아직 구속력 있는 계약이 아니고, 엔비디아 기술 의존도는 그만큼 깊어집니다.", ["90억 달러"],
          "card", "반론 표 (③ 강조)", "2026 · Barchart, 대신증권, Korea Times", None, COUNTER))
    # ---------------- TAKEAWAY
    if A:
        add(Q("takeaway",
              "My guess is that the semiconductor industry is probably going to have to be 10 times larger than it is today over the next decade or so.",
              "제 생각에 반도체 산업은 앞으로 10년쯤 동안 지금보다 10배는 커져야 할 겁니다.",
              ["10배"], L_BBG, src(BBG, "2:59.0", "3:11.0"), "젠슨 황 인터뷰 원본 (원래 소리)"))
    else:
        add(N("takeaway", "젠슨 황은 반도체 산업이 앞으로 10년 동안 지금보다 열 배는 커져야 한다고 말해 왔습니다.", ["열 배"],
              "source_video", "키노트 화면 (소리 끔)", "2026 · NVIDIA GTC 키노트", src(NV_GTC, "0:30", "0:40")))
    add(N("takeaway", "정리하면, 엔비디아는 그 열 배를 혼자 만들지 않습니다. 칩을 살 고객과 부품을 만들 회사의 주주 자리를 하나씩 채우고 있고, 네이버는 그 지도에 올라간 첫 한국 회사입니다.", ["첫 한국 회사"],
          "source_video", "젠슨 황/AI 팩토리 화면 (소리 끔)",
          L_BBG if A else "NVIDIA · The AI Factory 공식 영상",
          src(BBG, "3:12", "3:24") if A else src(NV_FACTORY, "0:30", "0:42")))
    # ---------------- OUTRO
    add(N("outro", "다음에 볼 것은 세 가지입니다. 11월 6일 실제 납입 공시, 11월 27일 신주 상장, 그리고 90억 달러 조달이 정식 계약으로 바뀌는지입니다.", ["11월 27일"],
          "card", "다음에 볼 것 표", "", None,
          card("table", "다음에 볼 것", [("11월 6일", "납입 공시", "실제 납입 확인"), ("11월 27일", "신주 상장", "1년 매각 제한", 1),
                                    ("미정", "90억 달러", "정식 계약 전환 여부")])))
    add(N("outro", "엔비디아의 지도에 다음으로 올라갈 한국 회사는 어디일까요?", [],
          "card", "질문 카드", "", None, card("text", "다음으로 올라갈 한국 회사는?")))
    if A:  # 보도 인용 문장은 기사 헤드라인 캡처로 보여 준다 (식스시그마 방식)
        shots = {"달러로는 그대로": (STOCKPLUS, "2026.11.03 · 증권플러스"),
                 "보도에 따르면 엔비디아 투자는": (KT, "2026.07.27 · The Korea Times"),
                 "최근에는 엔비디아가 투자한 마벨이": (FOOL, "2026.11.04 · The Motley Fool")}
        for sc in S:
            for key, (url, label) in shots.items():
                if sc["narration"].startswith(key):
                    sc.update({"visual_type": "screenshot", "card": None, "label": label,
                               "source": src(url), "visual_brief": "기사 헤드라인 캡처"})
    for i, s in enumerate(S, 1):
        s["id"] = i
    return S


for v in ("A", "B"):
    existing = ROOT / "projects" / f"20261105-첫영상-{v.lower()}"
    p = Project(existing) if existing.exists() else Project.create(f"첫영상-{v}")
    for d in ("00_source", "01_research"):
        shutil.copytree(BASE / d, p.path / d, dirs_exist_ok=True)
    st = p.state()
    st.update({"pick": 1, "done": ["discover", "select", "research", "script"], "approved": ["topic", "script"],
               "version": "A: 뉴스·인터뷰 클립 인용" if v == "A" else "B: 공식 영상 + 공시 카드"})
    p.save_state(st)
    data = {"title_working": "엔비디아가 네이버 3대 주주가 되는 날 | 젠슨 황의 지분 지도", "scenes": build(v)}
    p.write_json("script", "scenes.json", data)
    write_script_md(p, data)
    sc = data["scenes"]
    chars = sum(len(s["narration"].replace(" ", "")) for s in sc if s["kind"] == "narration")
    quotes = [s for s in sc if s["kind"] == "quote"]
    print(v, p.path.name, len(sc), "scenes,", len(quotes), "quotes, narration", chars, "chars")
