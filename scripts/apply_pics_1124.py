"""2026-11-24 사용자: "이대로 현재 만든 영상들 보완해주세요" — 오래 멈춰 있던 체크리스트에 오른쪽 그림(pics)을 붙인다.
줄 글은 짧게(자세한 숫자는 그림이 말함), 글 폭은 그림 자리를 비우도록 좁힘, 줄마다 붙던 작은 아이콘(motion)은 뺌.
python scripts/apply_pics_1124.py  (다시 돌려도 같은 결과)"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "projects"

S = {}

# ── 메모리 1부 ──────────────────────────────────────────
S[("memory-chicken", 15)] = dict(
    rows=["2010.10  P/E 3.8 → 28.9배", "2015.7  P/E 6.1 → 38.4배", "2018.7  P/E 5.5 → 4.7배", "2018.12  P/E 2.6 → 17.3배"],
    pics=[
        {"t": "2010년", "kind": "fraction", "date": "2010년 10월 → 1년 뒤", "pe": [3.8, 28.9], "earn": -92, "price": -38, "note": "매출은 +4%인데 이익이 사라짐"},
        {"t": "2015년", "kind": "fraction", "date": "2015년 7월 → 1년 뒤", "pe": [6.1, 38.4], "earn": -90, "price": -35, "note": "주가가 빠졌는데 P/E로는 여섯 배 넘게 비싸짐"},
        {"t": "2018년 7월", "kind": "fraction", "date": "2018년 7월 → 1년 뒤", "pe": [5.5, 4.7], "earn": -14, "price": -26, "note": "1년 반 뒤엔 이익 -69%"},
        {"t": "2018년 12월", "kind": "fraction", "date": "2018년 12월 → 1년 뒤 (예외)", "pe": [2.6, 17.3], "earn": -75, "price": 68, "note": "시장이 회복을 먼저 값에 넣음"},
    ])
S[("memory-chicken", 20)] = dict(
    pics=[
        {"t": "늦게", "kind": "timeline", "steps": ["생산을 정함", "남는 게 보임", "줄인 게 시장에"], "gaps": ["몇 달", "또 몇 달"], "note": "그동안 공장은 계속 만든다"},
        {"t": "장부의", "kind": "bars", "dep": 25, "cash": 15, "price": 30},
        {"t": "쌓아 두는", "kind": "decay", "value": "재고 평가손실 14.3억 달러", "sub": "마이크론, 2023 회계 2분기"},
        {"t": "놓친", "kind": "switch", "customer": "고객", "us": "우리 칩", "rival": "경쟁사 칩"},
        {"t": "버티면", "kind": "survive", "names": ["A 회사", "B 회사", "C 회사"]},
    ])
S[("memory-chicken", 21)] = dict(
    rows=["2022.9  마이크론·키옥시아 먼저", "2022.10  SK하이닉스 뒤따름", "2023.4  삼성전자도 감산", "2023  삼성 반도체 손실 약 14.9조", "더 앞: 2009 키몬다·2012 엘피다"],
    pics=[
        {"t": "마이크론과", "kind": "pins", "head": "누가 먼저 줄였나", "range": [2022.55, 2023.45],
         "ticks": [[2022.75, "2022.10"], [2023.0, "2023.1"], [2023.25, "2023.4"]],
         "items": [{"t": "마이크론과", "at": 2022.72, "name": "마이크론·키옥시아", "say": "먼저 줄임 (9월 말)", "side": "ok", "pos": "up"},
                   {"t": "SK하이닉스가", "at": 2022.8, "name": "SK하이닉스", "say": "10월 뒤따름", "side": "ok", "pos": "up"},
                   {"t": "11월에", "at": 2022.88, "name": "마이크론", "say": "웨이퍼 20% 더 줄임", "side": "ok", "pos": "up"},
                   {"t": "삼성전자는", "at": 2023.27, "name": "삼성전자", "say": "버티다 2023.4 감산", "side": "warn", "pos": "down"}]},
        {"t": "14.9조", "kind": "stat", "icon": "trending-down", "value": "약 14.9조 원", "sub": "2023년 삼성전자 반도체 영업손실"},
        {"t": "키몬다", "kind": "pins", "head": "아무도 먼저 안 줄이고 버티다", "range": [2008.3, 2012.9],
         "ticks": [[2009, "2009"], [2010, "2010"], [2011, "2011"], [2012, "2012"]],
         "items": [{"t": "키몬다", "at": 2009.05, "name": "키몬다 (독일)", "say": "파산", "side": "warn"},
                   {"t": "엘피다가", "at": 2012.1, "name": "엘피다 (일본)", "say": "파산", "side": "warn"}]},
    ])
S[("memory-chicken", 22)] = dict(
    rows=["2007~08  값이 무너져도 증산", "2009.1  키몬다 파산", "2010  삼성 26조 투자 계획", "2010 하반기  D램 1달러 아래", "2012.2  엘피다 파산보호"],
    pics=[
        {"t": "더 늘려서", "kind": "drain", "head": "더 늘려 값을 떨어뜨리면", "names": ["거는 쪽", "약한 경쟁사"], "cash": [330, 200], "rate": [0.4, 1.0],
         "dry": "먼저 마름", "note": "그림은 예시"},
        {"t": "2007년", "kind": "pins", "head": "늘린 쪽(위)과 쓰러진 쪽(아래)", "range": [2006.7, 2013.0],
         "ticks": [[2007, "2007"], [2009, "2009"], [2011, "2011"], [2013, "2013"]],
         "items": [{"t": "2007년", "at": 2007.6, "name": "증산·투자 경쟁", "say": "값이 무너지는 중에도", "side": "ok", "pos": "up"},
                   {"t": "키몬다가", "at": 2009.05, "name": "키몬다", "say": "파산 (2009.1)", "side": "warn"},
                   {"t": "26조", "at": 2010.2, "name": "삼성 26조 투자", "say": "반도체 11조", "side": "ok", "pos": "up"},
                   {"t": "1달러", "at": 2010.75, "name": "D램 1달러 아래", "say": "2010 하반기", "side": "warn"},
                   {"t": "엘피다가", "at": 2012.1, "name": "엘피다", "say": "파산보호 → 마이크론", "side": "warn"}]},
    ])
S[("memory-chicken", 23)] = dict(
    rows=["① 먼저 마르는 쪽이 진다", "② 공장은 2~3년 뒤에", "③ 남은 상대가 안 쓰러진다", "④ 얻는 건 점유율 몇 %"],
    pics=[
        {"t": "먼저", "kind": "drain", "head": "같은 출혈, 누가 먼저 마르나", "names": ["원가·현금 1등", "2등이 건다면"], "cash": [330, 210], "rate": [0.45, 1.0],
         "dry": "자기가 먼저", "note": "그림은 예시"},
        {"t": "공장", "kind": "timeline", "steps": ["늘리기 시작", "그사이 수요 회복", "새 공장 물량"], "gaps": ["", "2~3년"], "boxes": False,
         "note": "상대는 그대로, 값만 깎은 셈"},
        {"t": "남은", "kind": "survive", "stand": True, "names": ["A 회사", "B 회사", "중국 업체"], "shield": [2, "정부가 받침"], "note": "셋 다 크고, 쓰러지지 않는다"},
        {"t": "셋이", "kind": "share", "head": "큰 출혈 끝에 바뀌는 점유율", "segs": [["A", 40, 43], ["B", 35, 33], ["C", 25, 24]],
         "badge": "얻는 건 몇 %p", "note": "그림은 예시"},
    ])
S[("memory-chicken", 31)] = dict(
    rows=["최태원 — 2030년까지 부족", "SK하이닉스 — 2030년까지", "마이크론 CEO — 27·28년 더 빠듯", "KB증권 — 내년 D램값 +40%"],
    pics=[{"t": "최태원", "kind": "pins", "head": "부족은 언제까지? (낙관하는 쪽)", "range": [2026.6, 2030.6],
           "ticks": [[2027, "2027"], [2028, "2028"], [2029, "2029"], [2030, "2030"]],
           "items": [{"t": "최태원", "at": 2030.0, "name": "최태원 회장", "say": "2030년까지 · 웨이퍼 20%+ 모자람", "side": "ok", "pos": "up", "w": 270},
                     {"t": "SK하이닉스도", "at": 2030.0, "name": "SK하이닉스", "say": "수요 > 공급, 2030년까지", "side": "ok", "pos": "down"},
                     {"t": "마이크론", "at": 2027.9, "name": "메로트라 (마이크론)", "say": "27·28년 더 빠듯", "side": "ok", "pos": "up"},
                     {"t": "KB증권은", "at": 2027.3, "name": "KB증권", "say": "내년 D램값 +40%", "side": "ok", "pos": "down"}]}])
S[("memory-chicken", 32)] = dict(
    rows=["TrendForce — 낸드, 1분기부터 하락", "키움증권 — 범용 D램 30%대 하락", "베어드 — 내년 중반 꼭대기", "현물값: D램 -5%, 낸드 -20%"],
    pics=[{"t": "TrendForce", "kind": "pins", "head": "꼭대기는 언제? (신중한 쪽)", "range": [2026.6, 2028.1],
           "ticks": [[2026.85, "지금"], [2027.5, "2027 중반"], [2028, "2028"]],
           "items": [{"t": "TrendForce", "at": 2027.05, "name": "TrendForce", "say": "낸드 계약가 1분기부터 ↓", "side": "warn", "pos": "up"},
                     {"t": "키움증권은", "at": 2027.4, "name": "키움증권", "say": "범용 D램 30%대 ↓", "side": "warn", "pos": "down"},
                     {"t": "베어드는", "at": 2027.5, "name": "베어드", "say": "내년 중반 꼭대기", "side": "warn", "pos": "up"},
                     {"t": "현물값", "at": 2026.85, "name": "현물값 (한 달)", "say": "D램 -5% · 낸드 -20%", "side": "warn", "pos": "down"}]}])
S[("memory-chicken", 36)] = dict(
    rows=["만약 AI 수요가 더 크면", "만약 수요가 값에 민감하면", "만약 정부가 공장을 받치면", "만약 HBM처럼 미리 값을 정하면"],
    pics=[
        {"t": "첫째", "kind": "cond", "if": ["trending-up", "AI 수요가 예상보다 크면"], "then": ["clock", "부족이 길어지고 장기 계약이 버팀"], "tone": "warn"},
        {"t": "둘째", "kind": "cond", "if": ["percent", "수요가 값에 더 민감하면"], "then": ["trending-down", "혼자 줄이는 이익이 작아짐"], "tone": "warn"},
        {"t": "셋째", "kind": "cond", "if": ["landmark", "정부가 공장을 받치면"], "then": ["factory", "값이 내려도 공급이 안 줄어듦"], "tone": "warn"},
        {"t": "넷째", "kind": "cond", "if": ["calendar", "HBM은 1년 전에 값·물량을 정함"], "then": ["git-branch", "일반 메모리와 따로 움직임"], "tone": "warn",
         "note": "SK하이닉스: 내년 HBM 협상 이미 마침"},
    ])

# ── 메모리 2부 ──────────────────────────────────────────
S[("memory-insight", 2)] = dict(
    rows=["최태원 — 사이클이 길어진다", "메로트라 — 2026년 훨씬 넘어 부족", "캔터 — 26·27년 내내 부족", "모닝스타 — 27 말~28 공급이 누름",
          "모건스탠리 — 4분기부터 후반부", "경계현 — 27 하반기부터 값 ↓"],
    pics=[{"t": "최태원", "kind": "pins", "head": "부족은 언제 끝나나 (위 = 길다 · 아래 = 곧)", "range": [2026.6, 2028.7],
           "ticks": [[2027, "2027"], [2028, "2028"]],
           "items": [{"t": "최태원", "at": 2028.55, "name": "최태원", "say": "훨씬 길어진다 →", "side": "ok", "pos": "up", "w": 220},
                     {"t": "마이크론", "at": 2027.2, "name": "메로트라", "say": "2026년 훨씬 넘어", "side": "ok", "pos": "up", "w": 220},
                     {"t": "캔터", "at": 2027.95, "name": "캔터", "say": "26·27년 내내 부족", "side": "ok", "pos": "up", "w": 220},
                     {"t": "모닝스타", "at": 2028.0, "name": "모닝스타", "say": "27말~28 새 공급", "side": "warn", "w": 240},
                     {"t": "모건스탠리", "at": 2026.85, "name": "모건스탠리", "say": "4분기 후반부", "side": "warn", "w": 220},
                     {"t": "경계현", "at": 2027.6, "name": "경계현", "say": "27 하반기 값 ↓", "side": "warn", "w": 220}]}])
S[("memory-insight", 7)] = dict(
    rows=["받침: HBM이 웨이퍼 30%까지", "받침: 고객 수요 절반~2/3만", "어긋남: 돈 내는 AI 회사가 적자", "어긋남: 비싼 메모리가 수요를 깎음", "어긋남: 현물값 이미 하락"],
    pics=[{"t": "받치는", "kind": "balance", "left": "받침", "right": "어긋남",
           "items": [{"t": "HBM이", "side": "ok", "text": "HBM 웨이퍼 30%"},
                     {"t": "마이크론은", "side": "ok", "text": "수요 절반~2/3만"},
                     {"t": "오픈AI는", "side": "warn", "text": "AI 회사 적자"},
                     {"t": "PC가", "side": "warn", "text": "PC·폰 덜 팔림"},
                     {"t": "현물값은", "side": "warn", "text": "현물값 하락"}]}])
S[("memory-insight", 14)] = dict(
    rows=["① 만들기 3~4배 어렵다", "② 세 회사가 값을 지킨다", "③ 고객이 벌면 비싸도 산다"],
    pics=[
        {"t": "첫째", "kind": "growth", "head": "같은 용량에 드는 웨이퍼", "a": ["일반 D램", 1, "1"], "b": ["HBM", 3.5, "3~4배"], "color": "#2E7D4F",
         "badge": "사실로 받쳐짐"},
        {"t": "둘째", "kind": "cond", "if": ["trending-down", "값이 내려갈 때"], "then": ["scale", "규율이 시험받는다"], "tone": "warn",
         "note": "미국: 함께 생산을 조였다는 담합 소송 (판결 전)"},
        {"t": "셋째", "kind": "cond", "if": ["coins", "고객이 메모리로 돈을 버는 동안"], "then": ["shopping-cart", "비싸도 산다"], "tone": "warn",
         "note": "그 고객들은 아직 버는 것보다 쓰는 게 많다"},
    ])
S[("memory-insight", 27)] = dict(
    rows=["12.18 아침 마이크론 실적", "1분기 계약가", "AI 회사의 모집·상장", "중국 증설·감산 언급 시점"],
    pics=[{"t": "첫째", "kind": "lamps", "items": [
        {"t": "첫째", "icon": "calendar", "text": "12.18 마이크론 실적", "tag": "총이익률 버티면 → 낙관", "side": "ok"},
        {"t": "둘째", "icon": "tag", "text": "1분기 계약가", "tag": "범용 먼저 내리면 → 신중", "side": "warn"},
        {"t": "셋째", "icon": "wallet", "text": "AI 회사 모집·상장", "tag": "돈 내는 쪽의 지갑"},
        {"t": "넷째", "icon": "factory", "text": "중국 증설 · 감산 시점", "tag": "공급 쪽"}]}])

# ── 엔비디아 1부 ─────────────────────────────────────────
S[("nvidia-circular", 16)] = dict(
    rows=["투자한 회사 손상 18억 달러", "칩 금융 5,000억 — 집행 0", "젠슨 황 사임 → 크레스 임시 CEO", "네오클라우드 20%+ 하락 (보도)", "SEC 회계 조사 보도 (11.20)"],
    pics=[
        {"t": "손상", "kind": "growth", "head": "투자한 회사 값 깎임 (손상)", "a": ["2분기까지 누적", 2.5, "2.5억"], "b": ["3분기 한 분기", 18, "18억"],
         "badge": "한 분기 만에 일곱 배"},
        {"t": "5,000억", "kind": "empty", "head": "월가 칩 금융 약속 (8월)", "total": "5,000억 달러", "badge": "아직 집행 0",
         "note": "은행: 엔비디아 보증 25%보다 더 요구"},
        {"t": "물러났고", "kind": "swap", "from": ["user", "젠슨 황", "CEO 사임 (11.11)"], "to": ["user", "콜레트 크레스", "CFO → 임시 CEO"],
         "note": "이사회 독립위원회 조사 중"},
        {"t": "네오클라우드", "kind": "drop", "head": "네오클라우드 주가 (국내 보도)", "value": -20, "plus": True, "note": "보증 조건이 분명해진 뒤"},
        {"t": "증권거래위원회가", "kind": "drop", "head": "엔비디아 주가, 11월 20일", "value": -14, "note": "SEC 조사 보도 · 쟁점 미상"},
    ])
S[("nvidia-circular", 19)] = dict(
    rows=["만약 좋은 신용등급을 받으면", "만약 AI 수요가 계속 크면", "만약 칩 값이 빨리 떨어지면", "만약 경쟁사도 같은 방식이면"],
    pics=[
        {"t": "신용등급을", "kind": "cond", "if": ["shield-check", "오픈AI가 좋은 신용등급"], "then": ["unlock", "1,050억 보증이 끝남"], "tone": "ok"},
        {"t": "계속", "kind": "cond", "if": ["trending-up", "AI 수요가 계속 큼"], "then": ["refresh-cw", "고리가 문제없이 돎"], "tone": "ok",
         "note": "지분 투자: 쌓인 평가 이익 > 손실"},
        {"t": "칩 값이", "kind": "cond", "if": ["trending-down", "칩 값이 빨리 떨어짐"], "then": ["landmark", "담보 가치↓ · 은행이 물러섬"], "tone": "warn"},
        {"t": "AMD도", "kind": "cond", "if": ["cpu", "AMD도 오픈AI에 주식 권리"], "then": ["users", "엔비디아만의 문제가 아님"], "tone": "warn",
         "note": "칩 회사들이 고객에게 돈을 대는 경쟁"},
    ])

# ── 엔비디아 2부 ─────────────────────────────────────────
S[("nvidia-insight", 4)] = dict(
    rows=["① 젠슨 황이 떠났다 (11.11)", "② SEC 조사 보도 (확인 안 됨)", "③ 연준: 순환 금융은 위험", "④ 연준: 금리 더 올릴 수도"],
    pics=[
        {"t": "첫째", "kind": "lamps", "items": [
            {"t": "첫째", "icon": "user", "text": "젠슨 황 사임", "tag": "이유는 공시에 없음", "side": "warn"},
            {"t": "둘째", "icon": "search", "text": "SEC 장부 조사 보도", "tag": "익명 소식통", "side": "warn"},
            {"t": "셋째", "icon": "landmark", "text": "연준: 순환 금융 위험", "side": "warn"},
            {"t": "넷째", "icon": "percent", "text": "연준: 금리 더 올릴 수도", "side": "warn"}]},
        {"t": "14%", "kind": "drop", "head": "엔비디아, 11월 20일", "value": -14, "note": "7주 연속 하락 — 2008년 이후 최장"},
    ])
S[("nvidia-insight", 5)] = dict(
    rows=["① 파는 쪽이 돈을 대면 위험이 겹친다", "② 위험은 몇 년 뒤 약속에 쌓인다", "③ 약해지는 곳: 받는 속도·값·담보"],
    pics=[
        {"t": "첫째", "kind": "lamps", "items": [
            {"t": "첫째", "icon": "refresh-cw", "text": "파는 쪽이 돈을 댐", "tag": "매출은 진짜, 위험은 겹침"},
            {"t": "둘째", "icon": "calendar", "text": "위험은 몇 년 뒤에", "tag": "보증 · 임대 · 지분"},
            {"t": "셋째", "icon": "link", "text": "약해지는 곳", "tag": "받는 속도 · 투자 값 · 담보", "side": "warn"}]},
        {"t": "GPU가", "kind": "stat", "icon": "cpu", "value": "GPU는 몇 년 동안 돈을 버나?", "color": "#2B2B2B", "sub": "방어하는 쪽과 비판하는 쪽이 갈리는 숫자"},
    ])
S[("nvidia-insight", 11)] = dict(
    rows=["받침: 매출 절반 빅테크 · 1,158억", "어긋남: 못 받은 칩값 810억·64일", "어긋남: 투자 손상 18억 달러", "어긋남: 네오클라우드 20%+ 하락"],
    pics=[{"t": "받치는", "kind": "balance", "left": "받침", "right": "어긋남",
           "items": [{"t": "빅테크에서", "side": "ok", "text": "매출 절반 빅테크"},
                     {"t": "1,158억", "side": "ok", "text": "3분기 1,158억"},
                     {"t": "810억", "side": "warn", "text": "못 받은 810억"},
                     {"t": "손상은", "side": "warn", "text": "손상 18억"},
                     {"t": "네오클라우드", "side": "warn", "text": "네오클라우드 -20%"}]}])
S[("nvidia-insight", 24)] = dict(
    rows=["의사록: 추가 인상 적절", "쿡 이사: AI 건설 안 줄어", "금리 1%p = 해마다 1억 달러", "8년 셈 흑자 ↓ · 3년 셈 적자 ↑"],
    pics=[
        {"t": "의사록에는", "kind": "lamps", "items": [
            {"t": "의사록에는", "icon": "file-text", "text": "10월 의사록", "tag": "거의 모두 '추가 인상 적절'", "side": "warn"},
            {"t": "쿡 이사는", "icon": "user", "text": "쿡 이사 (11.20)", "tag": "'AI 건설이 줄지 않는다'", "side": "warn"}]},
        {"t": "1%포인트", "kind": "shift", "head": "100억 달러 빚 · 금리 +1%p = 해마다 1억 더", "shift_t": "8년 셈에서는",
         "rows": [{"label": "8년 셈", "a": 17.5, "b": 16.5}, {"label": "3년 셈", "a": -3.3, "b": -4.3}],
         "badge": "금리가 오를수록 '몇 년'의 차이가 비싸진다"},
    ])
S[("nvidia-insight", 25)] = dict(
    rows=["보도: WSJ — SEC 민사 조사", "보도: 로이터 — 회계 문제 가능성", "모름: 언제·무엇을 — SEC 논평 거부", "조사는 위반 판정이 아니다"],
    pics=[{"t": "월스트리트저널", "kind": "twocol", "left": "보도된 것", "right": "모르는 것", "lcolor": "#2B2B2B",
           "items": [{"t": "월스트리트저널", "side": "l", "text": "WSJ 11.17 · 공시가 오도했나"},
                     {"t": "로이터", "side": "l", "text": "로이터 11.20 · 회계 문제 가능성"},
                     {"t": "언제", "side": "r", "text": "언제 시작했나?"},
                     {"t": "무엇을", "side": "r", "text": "무엇을 보나?"},
                     {"t": "논평을", "side": "r", "text": "SEC 논평 거부"}],
           "verdict": {"t": "판정이", "text": "조사 ≠ 위반 판정"}}])
S[("nvidia-insight", 28)] = dict(
    rows=["H100 임대료 버티나 → 황 쪽", "칩 금융, 보증 없이 집행? → 황 쪽", "보증 실제 지급 (지금 0) → 비판 쪽", "회수 64일보다 길어지나 → 비판 쪽"],
    pics=[{"t": "첫째", "kind": "lamps", "items": [
        {"t": "첫째", "icon": "cpu", "text": "H100 임대료가 버티나", "tag": "→ 젠슨 황 쪽", "side": "ok"},
        {"t": "둘째", "icon": "landmark", "text": "칩 금융, 보증 없이 집행?", "tag": "→ 젠슨 황 쪽", "side": "ok"},
        {"t": "셋째", "icon": "hand-coins", "text": "보증 실제 지급 (지금 0)", "tag": "→ 비판 쪽", "side": "warn"},
        {"t": "넷째", "icon": "clock", "text": "회수 64일보다 길어지나", "tag": "→ 비판 쪽", "side": "warn"}]}])

# ── 오픈AI ─────────────────────────────────────────────
S[("openai", 33)] = dict(
    rows=["프라이어 — 성장은 받침, 이익은 아직", "아이스먼 — 근거 있음 (가정형)", "지트론 — 앤트로픽 S-1과 어긋남", "손정의·젠슨 황 — 속도를 늦춤", "알티미터 — 먼 미래, 확인 불가"],
    pics=[{"t": "프라이어의", "kind": "twocol", "left": "근거가 받침", "right": "약함 · 확인 불가", "lcolor": "#2E7D4F",
           "items": [{"t": "아이스먼의", "side": "l", "text": "아이스먼 · 약정·오라클 계약"},
                     {"t": "프라이어의", "side": "r", "text": "프라이어 · 이익은 아직"},
                     {"t": "지트론의", "side": "r", "text": "지트론 · S-1과 어긋남"},
                     {"t": "손정의", "side": "l", "text": "손정의·황 · 속도 늦춤"},
                     {"t": "알티미터의", "side": "r", "text": "알티미터 · 확인 불가"}],
           "verdict": {"t": "장부를", "text": "양쪽 모두 장부는 못 봤다"}}])


def main():
    for (name, sid), spec in S.items():
        p = ROOT / f"20261122-market-deep-{name}" / "02_script" / "hybrid.json"
        doc = json.loads(p.read_text(encoding="utf-8"))
        sc = next(s for s in doc["scenes"] if s["id"] == sid)
        if "rows" in spec:
            assert len(spec["rows"]) == len(sc["rows"]), (name, sid)
            for r, lab in zip(sc["rows"], spec["rows"]):
                r.setdefault("label_full", r["label"])
                r["label"] = lab
        sc["x"], sc["text_w"] = 150, 880
        sc["pics"] = spec["pics"]
        for b in sc["beats"]:
            if b.get("motion"):
                b["motion_off"] = b.pop("motion")
        p.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
        print("ok", name, sid, len(spec["pics"]))


if __name__ == "__main__":
    main()
