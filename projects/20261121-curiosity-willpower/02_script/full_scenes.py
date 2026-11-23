"""의지력 편 전체 장면표: full_beats.json(대본 v5 문단) + 박자마다 화면(mg)·바뀌는 낱말(kw) → full.json.
문단 하나 = 장면 하나. 화면 역할(script_v5 장면 설계): 어떻게 실험했나 = 삽화·동작 도식, 무엇이 나왔나 = 수치·출처,
왜 중요한가 = 서윤의 일상. kw 는 그 낱말을 말하는 순간 화면이 바뀌는 자리(단어 시각으로 맞춤).
python full_scenes.py → full.json"""
import json
from pathlib import Path
HERE = Path(__file__).resolve().parent
beats = json.loads((HERE / "full_beats.json").read_text(encoding="utf-8"))

B98 = "Baumeister 외 (1998), J. Pers. Soc. Psychol. 74(5)"
H16 = "Hagger 외 (2016), Perspect. Psychol. Sci. 11(4)"
D16 = "Dang (2016) 논평, Front. Psychol."
D21 = "Dang 외 (2021), Soc. Psychol. Personal. Sci. 12(1)"
V21 = "Vohs 외 (2021), Psychol. Sci. 32(10)"
D25 = "Dang 외 (2025), J. Pac. Rim Psychol. 19"
CM14 = "Carter·McCullough (2014) · 반론 Hagger·Chatzisarantis (2014)"
IS12 = "Inzlicht·Schmeichel (2012), Perspect. Psychol. Sci. 7(5)"
HO12 = "Hofmann·Vohs·Baumeister (2012), Psychol. Sci. 23(6)"
GD15 = "Galla·Duckworth (2015), J. Pers. Soc. Psychol. 109(3)"
GS06 = "Gollwitzer·Sheeran (2006), Adv. Exp. Soc. Psychol. 38"

A = lambda *shots, **k: dict(mg="art", shots=list(shots), **k)   # shots: [이미지, 시작 kw 번호(-1=처음), 움직임]
C = {
 1: A(["kitchen_tl", -1, "in"], stamp="밤 11:00", kw=["저녁"]),
 2: A(["day_tl", -1, "left"], ["day_tr", 0, "in"], ["day_bl", 1, "right", "coat"], ["kitchen_tr", 2, "in"],
      kw=["점심에는", "퇴근길에는", "그리고 지금"]),
 3: A(["kitchen_tl", -1, "out"], thought="오늘 참을 만큼 참았으니… 이제 바닥났다", kw=["오늘 참을"]),
 4: dict(mg="timeline", kw=["1998년", "그런데 그 뒤", "2025년"]),
 5: dict(mg="madi"),
 6: dict(mg="factcard", kicker="1998 · 원 실험", title="케이스웨스턴리저브대학", rows=["심리학 입문 수업 학생 67명", "끼니를 거르고 실험실에"],
       src=B98, kw=["심리학 입문", "끼니를"]),
 7: A(["lab_tl", -1, "in"], tag="재현 · 실제 사진 아님", kw=[]),
 8: dict(mg="three", src=B98, kw=["한 부류는", "다른 부류는", "나머지는"]),
 9: A(["lab_bl", -1, "in"], ["lab_br", 2, "in"], box="잰 것 · 포기하고 종을 울릴 때까지 버틴 시간", boxk=3, tag="재현 · 실제 사진 아님",
      kw=["학생들은 몰랐지만", "풀 수 없게", "포기하고 종을", "버틴 시간"]),
 10: dict(mg="bars98", src=B98, kw=["18.9분", "20.9분", "8.4분", "절반도"]),
 11: dict(mg="pair", left="lab_tr", right="kitchen_tl", kw=["서윤의 하루"]),
 12: dict(mg="battery", src=B98, kw=["자아 고갈", "쓰면 줄어드는", "많은 연구가"]),
 13: dict(mg="bias", src=CM14, kw=["그런데 실험이", "2014년", "효과가 나온 작은", "이 분석 방법", "미리 계획을"]),
 14: dict(mg="hyp", marks=[], kw=["표시가"]),
 15: dict(mg="labs", n=23, people="2,141명", src=H16, kw=["23개 연구실", "쿠키와 무를", "컴퓨터 과제"]),
 16: dict(mg="etask", kw=["쉬운 집단은", "어려운 집단은", "e가 모음", "두 번째 과제"]),
 17: dict(mg="ci", est=0.04, lo=-0.03, hi=0.11, people="23개 연구실 · 2,141명", note="효과가 있다 해도 아주 작음 · 오차 범위가 0을 포함",
        src=H16, hyp=[], add="q", addk=3, kw=["원래 이론을", "2,141명", "오차 범위", "물음표"]),
 18: dict(mg="madi"),
 19: dict(mg="weak", src=D16, kw=["당준화", "단어를 보고", "충분히"]),
 20: dict(mg="hyp", marks=["q"], fork=True, kw=["결과는"]),
 21: dict(mg="ci", est=0.10, lo=0.02, hi=0.18, people="12개 연구실 · 1,775명", note="작지만 통계적으로 의미 있는 효과", ref=0.62,
        src=D21 + " · 초기 메타분석 d=0.62 (Hagger 외 2010)", hyp=["q"], add="c", addk=2, backk=3, kw=["1,775명", "작지만", "체크 표시", "0.1 정도"]),
 22: dict(mg="ci", est=0.06, lo=-0.02, hi=0.14, people="36개 연구실 · 3,531명", note="미리 정한 주 분석 · 의미 있는 효과 확인 안 됨",
        bayes=True, src=V21, hyp=None, kw=["3,531명", "의미 있는 효과가", "두 통계 가설", "네 배"]),
 23: dict(mg="split21", src=V21, kw=["전체 참가자를", "아주 작지만", "거의 비슷하게"]),
 24: dict(mg="hyp", marks=["q", "c", "q"], verdict=True, kw=["2021년의 결론", "처음의 질문", "아직 답을"]),
 25: dict(mg="ch6", i=0), 26: dict(mg="ch6", i=1), 27: dict(mg="ch6", i=2), 28: dict(mg="ch6", i=3),
 29: dict(mg="ch6", i=4), 30: dict(mg="ch6", i=5), 31: dict(mg="ch6", i=6), 32: dict(mg="madi"),
 33: dict(mg="phenom", src=D25, kw=["하지만 그것이", "지루함이나", "피로나 동기", "수행이 떨어졌다는"]),
 34: dict(mg="process", src=IS12, kw=["2012년", "바닥나는 것이 아니라", "동기와 주의가"]),
 35: A(["kitchen_tr", -1, "in"], focus=True, kw=["즐거운 것을", "열량이 높다는", "맛있겠다는", "같은 치킨도"]),
 36: dict(mg="twohyp", src=IS12, kw=["논문 스스로", "두 설명 가운데", "둘 다"]),
 37: dict(mg="twoq", kw=["하지만 이유를", "그 출발점은"]),
 38: dict(mg="pager", src=HO12, kw=["205명", "호출기를", "무엇을 원하는지", "참으려 했는지", "어떻게 했는지"]),
 39: dict(mg="dayline", src=HO12, kw=["실패하는 경우가", "다만 사람들이"]),
 40: dict(mg="ranklist", then="day_br", src=HO12, kw=["미디어 이용과 일", "서윤의 식탁"]),
 41: dict(mg="tally", src="Hofmann 외 2012 계열 해석 · BPS Research Digest (2012)", kw=["자제력 점수가", "오히려 적었다", "애초에"]),
 42: dict(mg="habits", src=GD15, kw=["여섯 연구", "애써 참는 힘", "몸에 밴"]),
 43: dict(mg="ifthen", src=GS06, kw=["특정 상황에서", "94건", "더 가까이", "목표 자체가", "다른 방법보다"]),
 44: dict(mg="paths", kw=["습관과", "미리 정해 둔", "질문이 하나", "그 순간이 오기"]),
 45: A(["kitchen_tl", -1, "in"], strip=True, stamp="다시, 밤 11:00", kw=["오늘 하루를", "회의에서", "사양한", "장바구니에"]),
 46: A(["kitchen_tl", -1, "in"], ["kitchen_bl", 2, "in"], ["kitchen_br", 3, "in"], kw=["아니면 하루", "그저 지치고", "모든 것을", "내일 비슷한"]),
 47: dict(mg="recap", kw=["1998년의", "2025년의", "다만 그 이유가", "아직 확정"]),
 48: dict(mg="madi"),
}
out = []
for b in beats:
    sc = {**b, **C[b["id"]]}
    for k in sc.get("kw", []):
        assert k in b["text"], (b["id"], k)
    out.append(sc)
(HERE / "full.json").write_text(json.dumps({"title": "의지력은 정말 쓰면 닳을까? 과학자들의 실험이 엇갈린 이유", "voice": "ko-KR-InJoonNeural", "rate": "+4%",
                                            "scenes": out}, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(out), "장면")
