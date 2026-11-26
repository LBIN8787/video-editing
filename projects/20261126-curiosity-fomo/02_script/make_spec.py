"""포모 편 장면 명세: beats.json(← beats.py script_v1.md) + 아래 표 → fomo.json (render_full.py 의 SPEC, 화면 fomo_overlay.html).
유행 20년 편 방식 그대로: shots [그림, kw 번호(-1 = 처음부터), 카메라, 위 띠 글]. 그림 = 한 칸씩 고쳐 그린 원화(지우 칸은 품절 임박 편의 승인된 칸에서,
지우 없는 칸은 승인된 화풍 칸을 참조로 — E:/ytflow-local/fomo, Drive 영상/20261126-curiosity-fomo/art), 실제 자료 ev_przy·ev_whillans(논문 첫 쪽).
모션그래픽: times2(숫자 두 줄), line(척도 문장 한 줄씩 — 시청자 참여), words(생활로 옮긴 세 가지). python make_spec.py"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
A = lambda shots, kw=(), **k: dict(mg="art", shots=shots, kw=list(kw), **k)
P = {
 1: A([["night_wide", -1, "in"]]),
 2: A([["night_wide", -1, "in"], ["night_swipe", 0, "in"]], ["밤 11시,"], stamp="금요일 · 밤 11시"),
 3: A([["story_bbq", -1, "in", "동기들 · 송년회"], ["story_beach", 0, "in", "대학 친구 · 바다"], ["story_line", 1, "in", "후배 · 새벽 줄"]],
      ["다음 스토리는", "그다음은"]),
 4: A([["night_box", -1, "in"], ["night_alone", 0, "in"]], ["그리고 지금,", "'나만"], think="나만 빼고 다 재밌게 사네", thinkk=1),
 5: dict(mg="madi"),
 6: A([["night_think", -1, "in"]]),
 7: A([["hbs_night", -1, "in", "2004년 · 하버드 경영대학원"], ["hbs_write", 0, "in", "학교 신문 · 유머 칼럼"]], ["학교 신문에"]),
 8: A([["hbs_write", -1, "out"], ["hbs_write", 0, "out", "Fear Of Missing Out · 포모"], ["hbs_night", 1, "in", "인스타그램(2010)보다 먼저"],
       ["hbs_night", 2, "out"]], ["영어 앞글자를", "인스타그램이", "시작은"]),
 9: A([["ev_przy", -1, "in", "2013년 · 처음 만든 포모 설문"], ["survey", 0, "in"], ["survey", 1, "in", "내가 없는 곳의 더 좋은 경험 → 불안"]],
      ["연구팀은 포모를", "내가 없는"]),
 10: dict(mg="line", lines=[["속으로 하나씩 세어 보세요", "세어", 0], ["친구들이 나 없이 재밌게 논다는 걸 알면, 걱정된다", "걱정된다", 1],
                           ["친구들이 뭘 하는지 모르면, 불안하다", "불안하다", 2], ["여행을 가서도, 친구들이 뭘 하는지 계속 확인한다", "계속 확인한다", 3]],
          kw=["연구팀이 만든", "'친구들이 나 없이", "'친구들이 뭘", "'여행을"], hold=2.0),
 11: A([["office_meet", -1, "in"]]),
 12: A([["lecture", -1, "in", "대학 1학년 87명 · 2013"], ["survey", 0, "out", "영국 성인 2천여 명 · 젊을수록 높음"]], ["영국 성인"]),
 13: A([["office_meet", -1, "out"]]),
 14: A([["night_think", -1, "in"]], ["'동기들은"], think="동기들은 다 약속이 있겠지", thinkk=0),
 15: A([["ev_whillans", -1, "in", "2017년 · 캐나다 브리티시컬럼비아대 연구팀"], ["ubc_move", 0, "in", "입학 첫해의 신입생들"]], ["입학 첫해의"]),
 16: A([["ubc_form", -1, "in", "2월 · 신입생 1,099명"], ["ubc_form", 0, "in", "① 내 친한 친구는 몇 명?"], ["ubc_form", 1, "in", "② 다른 신입생들은 보통 몇 명?"]],
       ["입학한 뒤", "그리고, 다른"]),
 17: A([["ubc_form", -1, "out"]], hold=1.5),
 18: dict(mg="times2", img="ubc_many", head="친한 친구 수 · 신입생 1,099명", rows=[["내가 답한 평균", "3.6명"], ["남들 짐작", "4명 넘게"]],
          kw=["평균 3.6명이라고", "4명이 넘을"]),
 19: dict(mg="times2", img="ubc_many", head="한 사람씩 보면", rows=[["내가 더 많다", "31%"], ["남들이 더 많다", "48%"]],
          kw=["31퍼센트였습니다.", "48퍼센트,"]),
 20: dict(mg="madi"),
 21: A([["ubc_bubbles", -1, "in"], ["ubc_bubbles", 0, "in", "모두의 답 3.6명 · 모두의 짐작 4명 넘게"], ["ubc_bubbles", 1, "in", "절반 가까이 · '내가 뒤처진 쪽'"]],
       ["모두의 답을", "절반 가까이는"]),
 22: A([["ubc_many", -1, "out", "다른 연구팀 (2017) · 대학생·쇼핑몰 손님·온라인 참가자"]]),
 23: A([["cafeteria", -1, "in"]]),
 24: A([["cafeteria", -1, "in", "함께 → 남들 눈에 띄는 곳"], ["dorm", 0, "in", "혼자 → 잘 안 보이는 곳"]], ["혼자 밥을"]),
 25: A([["cafeteria", -1, "out"], ["dorm", 0, "in"]], ["기숙사"]),
 26: A([["friend_past", -1, "in"], ["friend_past", 0, "in", "일주일 못 본 친구 → 더 크게"]], ["지난 일주일"]),
 27: A([["party_think", -1, "in", "떠오르는 사람 = 가장 활발한 사람"], ["party_think", 0, "in", "덜 떠오르게 하자 → 착각이 사라졌다 (보고)"]], ["그런 사람들이"]),
 28: A([["night_swipe", -1, "in"], ["story_bbq", 0, "in", "올라온 장면"], ["dorm", 1, "in", "올릴 게 없던 금요일"], ["night_swipe", 2, "out"]],
       ["송년회에 간", "오늘 집에", "지우가 넘겨"]),
 29: dict(mg="madi"),
 30: A([["belong_low", -1, "in", "신입생 389명 · 몇 달 간격 두 번"], ["belong_low", 0, "in", "행복감 ↓ · 소속감 ↓"]], ["행복감이"]),
 31: A([["belong_low", -1, "out"]]),
 32: A([["knock", -1, "in"], ["knock", 0, "in", "'훨씬'보다 '조금' → 그해 친구 ↑"]], ["그해 동안"]),
 33: A([["night_alone", -1, "in"]]),
 34: A([["limit_fail", -1, "in"]]),
 35: A([["penn", -1, "in", "2018년 · 펜실베이니아대 · SNS 하루 30분"], ["penn", 0, "in", "외로움 ↓"], ["penn", 1, "in", "제목은 'No More FOMO'"]],
       ["몇 주 뒤,", "정작"]),
 36: dict(mg="times2", img="penn", head="2026 재현 · 서른 살 아래 600여 명", rows=[["제한", "하루 30분 · 3주"], ["원래 하루 사용", "약 3시간"]],
          kw=["3주 동안", "세 시간"]),
 37: dict(mg="times2", img="limit_fail", head="30분 제한을 받은 사람", rows=[["한 주라도 지킨 사람", "10명 중 1명"]],
          shots=[["@mg", -1], ["limit_fail", 1, "in", "1시간으로 늘려도 · 절반 넘게 하루도 못 지킴"], ["limit_fail", 2, "in", "행복감 · 평소처럼 쓴 사람들과 비교"],
                 ["limit_fail", 3, "in", "학술지 출판 전 결과"]],
          kw=["열 명 중", "다른 229명에게", "행복감은,", "아직 학술지에"]),
 38: A([["night_down", -1, "in"]]),
 39: dict(mg="words", head="원리를 생활로 옮기면", lines=[["피드 = 하루 중 한 장면", 0], ["사진이 없는 사람도 떠올리기", 1], ["오래 못 본 친구에게, 내가 먼저", 2]],
          kw=["피드가", "사진이 올라오지", "그리고 오래"]),
 40: A([["night_down", -1, "in"], ["night_swipe", 0, "in"], ["night_names", 1, "in"]], ["다시 집어", "올라오지 않은 이름들을"]),
 41: A([["night_type", -1, "in"]], ["'다음"], say="다음 주에 밥 먹을래?", sayk=0),
 42: A([["night_reply", -1, "in"]], ["'좋아!"], say="좋아! 나도 오늘 집이었어 ㅋㅋ", sayk=0),
 43: dict(mg="madi"),
 44: A([["night_end", -1, "in"]]),
}
beats = json.loads((HERE / "beats.json").read_text(encoding="utf-8"))
assert len(beats) == len(P), (len(beats), len(P))
scenes = []
for b in beats:
    s = dict(b); s.update(P[b["id"]])
    assert (s["mg"] == "madi") == (b["kind"] == "madi"), b["id"]
    for k in s.get("kw", []):
        assert k in s["text"] and s["text"].count(k) == 1, (b["id"], k)
    for sh in s.get("shots", []):
        assert sh[1] < len(s.get("kw", [])), (b["id"], sh)
    scenes.append(s)
(HERE / "fomo.json").write_text(json.dumps({"title": "정말 남들은 나보다 더 재밌게 살까? — 포모의 정체", "version": "v1", "scenes": scenes},
                                         ensure_ascii=False, indent=1), encoding="utf-8")
print(len(scenes), "장면")
