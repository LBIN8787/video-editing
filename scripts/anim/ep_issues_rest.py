"""시사 편 1:23 이후 — 메모리 vs 파운드리 → 쌀 파는 농부의 비유 → 대만의 숫자 → 환율 저울 → 한국은행 보고서(K자형) → 일하는 사람의 수 → HBM과 장기 계약 → 두 시각 → 내 생활 → 볼 신호 → 끝.

화풍: 시사 지면 삽화. 글자는 명조, 숫자는 그 장면 속 물건(화면·간판·종이) 위에. 사람 수는 그린 인물 조각을 줄 세워 센다.
"""

INK, RED, GRN, MUTE = "#1f2a33", "#b23b2a", "#2f6b4a", "#4a5560"


def rest(f, A):
    prev = {"id": "cities"}

    def scene(sid, plate, word, how="push", dur=.8, after=None, focus=None, w=1920):
        s = f.set(sid, plate, w=w, focus=focus or (960, 560, 1.0))
        s._word, s._how, s._dur, s._after = word, how, dur, after
        return s

    def go(s):
        t = f.cue(s._word, s._after)
        f._show(t, s.id, s._how, s._dur, prev["id"])
        f._sound(t, "whoosh" if s._how in ("push", "down", "iris") else "whoosh-short", .18)
        prev["id"] = s.id
        return t

    def back(sid, word, how="push", after=None):
        t = f.cue(word, after)
        f._show(t, sid, how, .8, prev["id"])
        f._sound(t, "whoosh-short", .18)
        prev["id"] = sid
        return t

    def ink(s, tid, text, x, y, size=56, color=INK, shadow=True):
        # shadow=False 는 화면·간판 위에 직접 쓰는 글자, 그 밖은 종이 쪽지 위에
        s.text(tid, text, x, y, size=size, color=color, font="serif", rot=0, shadow=shadow, card=shadow)

    def get(sid):
        return [s for s in f.sets if s.id == sid][0]

    # ── 한국: 메모리 — 값을 따라 출렁 ───────────────────────────
    fb = scene("fab", "fab.png", "한국", "push", after=82)
    for i in range(5):
        fb.prop(f"dr{i}", "dram", 420 + i * 270, 640, 250, z=7, rot=-4 + i * 2)
    fb.prop("tag", "pricetag", 1500, 420, 170, z=8)
    ink(fb, "mem", "한국 — 삼성전자·SK하이닉스의 메모리", 960, 140, 58)
    ink(fb, "same", "여러 회사가 같은 규격으로 사 간다", 960, 220, 44, MUTE)
    ink(fb, "swing", "이익이 가격을 따라 출렁", 960, 860, 64, RED)
    t = go(fb)
    f._enter(t + .2, "mem", "write", .8)
    f._enter(f.cue("메모리입니다"), "dr0", "pop", .5)
    t = f.cue("수많은")
    for i in range(1, 5):
        f._enter(t + i * .2, f"dr{i}", "pop", .4)
        f._sound(t + i * .2, "pop", .06)
    f._enter(t + .4, "same", "write", .8)
    t = f.cue("몰리면")
    f._enter(t, "tag", "pop", .4)
    for n, dy in enumerate([-220, 340, -260, 300, -160]):
        f._move(t + .5 + n * .7, "tag", dy=dy, dur=.6, rot=10 if n % 2 else -10, ease="sine.inOut")
    f._enter(f.cue("출렁입니다"), "swing", "write", .6)

    # ── 대만: 파운드리와 서버 — 미리 받은 주문, 정해진 물량 ─────────────
    fd = scene("foundry", "foundry.png", "대만의", "push", after=101)
    fd.prop("wf", "wafer", 700, 560, 300, z=7)
    fd.prop("gp", "gpu", 1200, 560, 260, z=7)
    ink(fd, "tsmc", "대만 — TSMC, 남이 설계한 칩을 만들어 주는 '파운드리'", 960, 140, 50)
    ink(fd, "ds", "엔비디아·애플의 설계 → 대만의 공장", 960, 860, 52, INK)
    t = go(fd)
    f._enter(t + .2, "tsmc", "write", 1.2)
    f._enter(f.cue("엔비디아나"), "gp", "slide", .6, dx=-300)
    f._enter(f.cue("만들어", after=109), "wf", "pop", .5)
    f._enter(f.cue("만들어", after=109), "ds", "write", .8)
    sv = scene("server", "server.png", "여기에", "push", after=111)
    for i in range(4):
        sv.prop(f"rk{i}", "rack", 500 + i * 300, 980, 200, z=7, anchor="bottom")
    sv.prop("ct", "contract", 1500, 330, 260, z=8)
    ink(sv, "fx", "폭스콘·콴타 — AI 서버 조립", 700, 140, 54)
    ink(sv, "vol", "출렁이는 가격보다, 안정적인 물량", 960, 140, 58, GRN)
    t = go(sv)
    f._enter(t + .3, "fx", "write", .8)
    t = f.cue("주문을")
    f._enter(t, "ct", "drop", .7)
    t2 = f.cue("물량을", after=t)
    for i in range(4):
        f._enter(t2 + i * .25, f"rk{i}", "slide", .5, dx=-200)
        f._sound(t2 + i * .25, "click-soft", .12)
    t = f.cue("언론과", after=123)
    f._leave(t, "fx", "fade", .3)
    f._enter(t + .3, "vol", "write", 1.0)

    # ── 비유: 시장에 쌀을 파는 농부 vs 식당과 계약한 농부 ──────────────
    rm = scene("rmarket", "ricemarket.png", "비유하자면", "wipe")
    rm.actor("fs", ["farmer_sell", "farmer_shake", "farmer_cart"], x=760, y=1050, h=720)
    rm.prop("rtag", "pricetag", 1250, 420, 160, z=8)
    ink(rm, "kr1", "한국 — 시장에 쌀을 내다 파는 농부", 960, 140, 58)
    rs = scene("rest", "restaurant.png", "대만은", "push", after=134)
    rs.actor("fc", ["farmer_shake", "farmer_cart", "farmer_sell"], x=620, y=1050, h=720)
    rs.actor("chef", ["chef"], x=1400, y=1050, h=700)
    for i in range(4):
        rs.prop(f"rsk{i}", "ricesack", 460 + i * 60, 880, 160, z=8, anchor="bottom", hidden=False)
    ink(rs, "tw1", "대만 — 식당과 미리 계약해 둔 농부", 960, 140, 58)
    ink(rs, "ai1", "AI 라는 큰 식당이 문을 열자", 960, 220, 48, RED)
    t = go(rm)
    f._enter(t + .3, "kr1", "write", 1.0)
    t = go(rs)
    f._enter(t + .2, "tw1", "write", 1.0)
    t = f.cue("싸이값이")
    f._show(t, "rmarket", "push", .6, "rest")
    prev["id"] = "rmarket"
    f._enter(t + .2, "rtag", "pop", .4)
    f._move(t + .4, "rtag", dy=-200, dur=.8, ease="back.out(2)")
    f._pose(t + .4, "fs", "farmer_sell")
    t = back("rest", "AI라는")
    f._enter(t, "ai1", "write", .7)
    f._pose(t + .4, "fc", "farmer_cart")
    for i in range(4):
        f._move(t + 1.0 + i * .5, f"rsk{i}", dx=900 - i * 60, dy=-40, dur=.7, ease="power2.in")
        f._leave(t + 1.6 + i * .5, f"rsk{i}", "fade", .2)
        f._sound(t + 1.0 + i * .5, "whoosh-short", .1)

    # ── 숫자: 수출 사상 최대, 성장 8% ───────────────────────────
    pt = scene("port", "port.png", "숫자도", "push")
    pt.counter("ex", 960, 150, 110, INK, text="", card=True)
    pt.counter("ex35", 960, 290, 80, RED, text="", card=True)
    ink(pt, "us", "미국행 AI 서버·고성능 컴퓨팅 장비", 960, 400, 50)
    pt.counter("g8", 960, 860, 100, GRN, text="", card=True)
    ink(pt, "g15", "15년 만에 가장 빠른 성장", 960, 970, 46, MUTE)
    for i in range(5):
        pt.prop(f"cn{i}", "container", -200, 700 - i * 40, 260, z=8, hidden=False)
    t = go(pt)
    f._count(f.cue("6"), "ex", 0, 6400, 1.6, pre="대만 수출 ", suf="억 달러+")
    f._count(f.cue("35"), "ex35", 0, 35, 1.0, pre="1년 만에 +", suf="%")
    t = f.cue("미국으로")
    f._enter(t, "us", "write", .7)
    for i in range(5):
        f._move(t + i * .3, f"cn{i}", dx=2400, dy=-60, dur=2.0, ease="power1.in")
    f._sound(t, "whoosh", .15)
    f._count(f.cue("8", after=166), "g8", 0, 8, .9, pre="성장 ", suf="% 안팎")
    f._enter(f.cue("15년"), "g15", "write", .6)

    # ── 환율: 같은 소득, 다른 저울 ───────────────────────────────
    t = back("exch", "그렇다면", after=173)
    ex = get("exch")
    f._leave(t, "rank", "fade", .2)
    ink(ex, "still", "한국은 제자리였을까?", 760, 160, 64)
    f._enter(t + .2, "still", "write", .8)
    f._cam(t, "exch", 1150, 560, 1.0, .5)
    t = f.cue("1인당", after=185)
    f._leave(t, "still", "fade", .3)
    ink(ex, "usd", "나라끼리 비교할 때는 모두 '달러'로", 760, 160, 56)
    f._enter(t, "usd", "write", .9)
    t = f.cue("약했습니다")
    f._tween(t, "#won .mv", {"scale": .8, "transformOrigin": "50% 100%"}, .8)
    f._tween(t + .2, "#dol .mv", {"scale": .7, "transformOrigin": "50% 100%"}, .8)
    f._sound(t, "whoosh-short", .15)
    sc = scene("scale", "exchange.png", "한쪽", "dissolve", focus=(1150, 560, 1.0))
    sc.prop("bal", "scale", 900, 620, 640, z=7, hidden=False)
    sc.prop("csk", "coinsack", 1130, 300, 150, z=8)
    ink(sc, "lw", "원화 약세 — 무게가 빠지고", 620, 160, 50, RED)
    ink(sc, "rw", "대만달러 강세 — 무게가 더해지고", 1250, 240, 50, GRN)
    t = go(sc)
    f._grade(t, "scale", "blur(3px) brightness(.95)", .01)
    f._enter(t, "lw", "write", .6)
    f._enter(f.cue("다른쪽"), "rw", "write", .6)
    f._enter(f.cue("더해진"), "csk", "drop", .7)
    f._sound(f.cue("더해진") + .5, "impact-bass-2", .15)
    bk = scene("bok", "bok.png", "한국은행", "push", after=211)
    ink(bk, "bq", "\"환율 영향을 빼면 머지않아 4만 달러\" — 한국은행 관계자", 960, 150, 46)
    t = go(bk)
    f._enter(t + .4, "bq", "write", 1.4)
    f._cam(t, "bok", 960, 520, 1.1, 6)
    t = back("exch", "그러니까", after=219)
    f._leave(t, "usd", "fade", .2)
    ink(ex, "mom", "덜 벌어서가 아니라, 달러로 바꾸는 순간의 차이", 760, 160, 46)
    f._enter(t + .4, "mom", "write", 1.2)
    ex.prop("mag", "magnifier", 1640, 330, 360, z=10)
    ink(ex, "itp", "해석 · 환율이라는 확대경", 1640, 620, 40, RED)
    t = f.cue("확대경을")
    f._enter(t - .6, "itp", "write", .5)
    f._enter(t, "mag", "pop", .5)
    f._tween(t + .5, "#wp", {"scale": 1.3}, .6)
    t = f.cue("그렇다고", after=236)
    f._tween(t, "#wp", {"scale": 1}, .5)
    f._leave(t, "mag", "fade", .4)
    f._leave(t, "itp", "fade", .3)
    t = back("port", "대만의", after=240)

    # ── 한국은행 보고서: 진짜였지만 고르지 않았다 ──────────────────────
    t = back("brief", "그리고", after=244)
    br = get("brief")
    for i in ("bd", "bt", "kr", "krn", "tw", "twn", "fix"):
        f._leave(t, i, "fade", .2)
    f._cam(t, "brief", 1125, 340, 1.55, .8)
    ink(br, "rp1", "한국은행 · 11월 13일 보고서", 1125, 170, 44, MUTE, shadow=False)
    ink(br, "rp2", "대만 반도체 경기 호황의 특징과", 1125, 250, 50, INK, shadow=False)
    ink(br, "rp3", "우리 경제에 대한 시사점", 1125, 320, 50, INK, shadow=False)
    ink(br, "rp4", "호황은 진짜, 그러나 고르지 않다", 1125, 420, 56, RED, shadow=False)
    f._enter(f.cue("11월", after=t), "rp1", "write", .5)
    f._enter(f.cue("대만", after=t), "rp2", "write", .8)
    f._enter(f.cue("경제에", after=t), "rp3", "write", .6)
    f._enter(f.cue("고르지", after=t), "rp4", "write", .7)
    ts = scene("tst", "taipei_street.png", "보고서에", "push", after=265)
    ink(ts, "up", "IT 수출 ↗ 이례적 고성장", 1400, 160, 54, GRN)
    ink(ts, "flat", "IT 아닌 산업 → 정체", 520, 560, 54, RED)
    ink(ts, "kk", "'K자형 불균형'", 960, 880, 80, INK)
    ink(ts, "cons", "소비: 주식 호조·재정 지원 뒤에야 회복", 960, 160, 48)
    ink(ts, "birth", "8% 가까운 성장 속에서도 출산율 세계 최하위권", 960, 240, 46, RED)
    t = go(ts)
    f._enter(f.cue("고성장을"), "up", "write", .6)
    f._enter(f.cue("정체돼"), "flat", "write", .6)
    f._enter(f.cue("K자형"), "kk", "write", .7)
    t = f.cue("소비도")
    for i in ("up", "flat", "kk"):
        f._leave(t, i, "fade", .3)
    f._enter(t + .2, "cons", "write", 1.0)
    f._enter(f.cue("출산률이"), "birth", "write", 1.0)

    # ── 일하는 사람의 수: 열 명 중 하나 vs 쉰 명 중 하나 ────────────────
    sk = get("sky")
    for i in range(10):
        sk.prop(f"tw{i}", "fig_worker" if i == 4 else ["fig_a", "fig_b", "fig_c"][i % 3], 520 + i * 100, 470, 70, z=8, anchor="bottom")
    for i in range(50):
        r, c = divmod(i, 25)
        sk.prop(f"ko{i}", "fig_worker" if i == 12 else ["fig_a", "fig_b", "fig_c"][i % 3], 260 + c * 56, 760 + r * 120, 44, z=8, anchor="bottom")
    ink(sk, "twl", "대만 91만 명 · 10.6% — 열 명 중 한 명", 960, 300, 52, GRN)
    ink(sk, "kol", "한국 39만 명 · 1.9% — 쉰 명 중 한 명", 960, 600, 52, RED)
    ink(sk, "itm", "2025년 IT 제조업에서 일하는 사람", 960, 150, 50)
    t = back("sky", "그리고", how="dissolve", after=297)
    for i in ("q2", "asof", "k20"):
        f._leave(t, i, "fade", .1)
    for i in range(4):
        f._tween(t, f"#kw{i}", {"top": -400}, .8, "power2.in")
    f._cam(t, "sky", 960, 540, 1.0, .5)
    f._enter(f.cue("2025년", after=t), "itm", "write", .8)
    t = f.cue("91만")
    f._enter(t, "twl", "write", .8)
    for i in range(10):
        f._enter(t + i * .06, f"tw{i}", "pop", .3)
    f._tween(f.cue("10", after=t) + .3, "#tw4 .mv", {"scale": 1.35, "transformOrigin": "50% 100%"}, .4, "back.out(3)")
    t = f.cue("39만")
    f._enter(t, "kol", "write", .8)
    for i in range(50):
        f._enter(t + i * .025, f"ko{i}", "pop", .25)
    f._tween(f.cue("1", after=t) + .3, "#ko12 .mv", {"scale": 1.45, "transformOrigin": "50% 100%"}, .4, "back.out(3)")
    f._sound(t, "pop", .12)
    sg = scene("shift", "shiftgate.png", "같은", "push", after=322)
    ink(sg, "warm", "월급 받는 사람이 많으면 → 동네 식당·가게로 넓게", 960, 150, 48)
    t = go(sg)
    f._enter(f.cue("많으면", after=t), "warm", "write", 1.2)
    f._cam(t, "shift", 1050, 600, 1.15, 7)
    nb = scene("nbr", "neighborhood.png", "한국은행은", "push", after=330)
    nb.actor("oc", ["owner_cook"], x=1350, y=1050, h=640)
    ink(nb, "slow", "한국의 소비 회복은 대만보다 더딜 수 있다", 760, 150, 50)
    ink(nb, "nar", "온기가 내수로 번지는 길이 좁다", 760, 230, 50, RED)
    t = go(nb)
    f._enter(t + .3, "slow", "write", 1.0)
    f._enter(f.cue("온기가"), "nar", "write", .8)

    # ── HBM: 시장에 내다 팔던 농부가 계약서를 받아 둔다 ──────────────────
    t = back("rmarket", "그렇다면", after=344)
    f._leave(t, "rtag", "fade", .1)
    rmk = get("rmarket")
    ink(rmk, "still2", "계속 '시장에 쌀을 파는 농부'로 남을까?", 960, 230, 52, RED)
    f._enter(t + .3, "still2", "write", 1.0)
    hb = scene("hbm", "hbm.png", "최근의", "push")
    for i in range(4):
        hb.prop(f"hs{i}", "hbmstack", [1260, 1450, 1300, 1490][i], [380, 360, 600, 570][i], 150, z=8)
    hb.prop("hct", "contract", 1560, 300, 220, z=9)
    ink(hb, "hl", "AI 칩 바로 옆, 층층이 쌓은 메모리 'HBM'", 960, 140, 52)
    ink(hb, "hl2", "아무나 사 가는 물건이 아니라, 고객 칩에 맞춰 미리 협의", 960, 900, 46, GRN)
    t = go(hb)
    t2 = f.cue("HBM이라는")
    f._enter(t2, "hl", "write", .9)
    for i in range(4):
        f._enter(f.cue("메모리가", after=t2) + i * .3, f"hs{i}", "drop", .6)
        f._sound(f.cue("메모리가", after=t2) + i * .3 + .4, "click-soft", .15)
    f._enter(f.cue("아무나"), "hl2", "write", 1.2)
    f._enter(f.cue("협의하고"), "hct", "pop", .5)
    hy = scene("hynix", "hynix.png", "스카이닉스는", "push")
    ink(hy, "h1", "SK하이닉스 · 10월 28일 실적 발표", 960, 140, 50, MUTE)
    ink(hy, "h2", "D램·HBM 물량, 2029년까지 사실상 매진 (협의 중 수요 포함)", 960, 230, 46)
    ink(hy, "h3", "내후년까지 생산능력 절반 넘게 장기 계약", 960, 310, 46)
    hy.counter("h4", 960, 820, 100, GRN, text="", card=True)
    hy.prop("hct2", "contract", 1550, 640, 260, z=8)
    ink(hy, "far", "몇 년 치 계약서를 받아 두는 농부 쪽으로", 960, 940, 50, GRN)
    t = go(hy)
    f._enter(t + .3, "h1", "write", .6)
    f._enter(f.cue("2029년까지"), "h2", "write", 1.2)
    f._enter(f.cue("내후년까지"), "h3", "write", 1.0)
    f._enter(f.cue("계약으로"), "hct2", "drop", .6)
    f._count(f.cue("2배를"), "h4", 0, 2, .8, pre="고객 요청 물량 = 공급 가능량의 ", suf="배+")
    f._enter(f.cue("시장에", after=390), "far", "write", 1.0)
    t = back("bok", "한국은행이", after=397)
    f._leave(t, "bq", "fade", .1)
    ink(get("bok"), "late", "한국의 성장세: 대만보다 1년쯤 늦게, 지난해 하반기부터", 960, 150, 46)
    f._enter(t + .3, "late", "write", 1.2)
    # 낙관만 할 수는 없다
    t = back("hynix", "물론", how="dissolve", after=404)
    for i in ("h1", "h2", "h3", "h4", "far"):
        f._leave(t, i, "fade", .2)
    f._grade(t, "hynix", "saturate(.5) brightness(.85)", .8)
    ink(hy, "c1", "삼성전자의 HBM 공급 확대 → '파는 쪽의 힘' 줄 수도", 960, 160, 46, RED)
    ink(hy, "c2", "일부 증권사, 내년 HBM 이익률 전망 하향", 960, 240, 46, RED)
    ink(hy, "c3", "계약서가 두툼해져도, 일하는 사람의 몫은 작다", 960, 860, 52)
    f._enter(f.cue("삼성전자가", after=t), "c1", "write", 1.0)
    f._enter(f.cue("증권사는"), "c2", "write", .9)
    f._enter(f.cue("계약서가", after=420), "c3", "write", 1.0)

    # ── 두 시각: 구조론 vs 착시론 ───────────────────────────────
    fk = scene("fork", "fork.png", "이", "push", after=430)
    fk.actor("an", ["analyst"], x=960, y=1050, h=660)
    ink(fk, "lv", "구조의 문제", 520, 260, 66, GRN)
    ink(fk, "lv1", "수십 년 산업 정책의 결실 · 물량으로 버는 구조", 520, 360, 42, INK)
    ink(fk, "lv2", "→ 한국도 산업의 폭을 넓혀야", 520, 440, 42, INK)
    ink(fk, "rv", "숫자의 착시", 1400, 260, 66, RED)
    ink(fk, "rv1", "환율 + 한 산업 쏠림이 만든 역전", 1400, 360, 42, INK)
    ink(fk, "rv2", "→ 평균 한 줄로는 살림을 못 본다", 1400, 440, 42, INK)
    ink(fk, "mid", "호황은 진짜, 온기는 고르지 않고, 꺾이면 함께 흔들린다", 960, 140, 44, INK)
    ink(fk, "mid2", "AI 를 쓰는 곳이 넓어져야 — 생산성 ↑ 양극화 ↓", 960, 140, 46, GRN)
    t = go(fk)
    f._enter(f.cue("구조의"), "lv", "write", .5)
    f._enter(f.cue("파운드리와", after=437), "lv1", "write", 1.0)
    f._enter(f.cue("넓혀야"), "lv2", "write", .6)
    f._enter(f.cue("숫자의", after=456), "rv", "write", .5)
    f._enter(f.cue("원화", after=460), "rv1", "write", 1.0)
    f._enter(f.cue("판단하기"), "rv2", "write", .6)
    f._cam(f.cue("한국은행의", after=483), "fork", 960, 600, 1.1, 1.5)
    f._enter(f.cue("호황은", after=488), "mid", "write", 1.4)
    t = f.cue("이번", after=497)
    f._leave(t, "mid", "fade", .3)
    f._enter(t + .3, "mid2", "write", 1.2)

    # ── 내 생활: 통장과 뉴스의 숫자 ──────────────────────────────
    lv = scene("living", "living.png", "그렇다면", "push", after=507)
    lv.actor("clk", ["clerk_phone"], x=600, y=1050, h=700)
    ink(lv, "tv1", "1인당 소득 (달러)", 1500, 300, 50, INK, shadow=False)
    ink(lv, "tv2", "반도체 수출 사상 최대", 1500, 380, 46, RED, shadow=False)
    ink(lv, "wal", "내 월급 (원화)", 600, 220, 50)
    ink(lv, "fx2", "환율 ↑ → 월급은 그대로여도 나라 순위 ↓", 960, 900, 48, RED)
    ink(lv, "mid3", "호황 한가운데서 월급 받는 사람이 상대적으로 적다", 960, 900, 46, INK)
    t = go(lv)
    f._enter(f.cue("통장과"), "wal", "write", .5)
    f._enter(f.cue("뉴스의", after=t), "tv1", "write", .6)
    f._enter(f.cue("환율이", after=522), "fx2", "write", 1.0)
    t = f.cue("반도체가", after=527)
    f._enter(t, "tv2", "write", .8)
    t = f.cue("호황의", after=534)
    f._leave(t, "fx2", "fade", .3)
    f._enter(t + .2, "mid3", "write", 1.2)

    # ── 확인 못 한 것, 볼 신호 셋 ───────────────────────────────
    t = back("brief", "아직", after=540)
    for i in ("rp1", "rp2", "rp3", "rp4"):
        f._leave(t, i, "fade", .2)
    ink(br, "u1", "확인하지 못한 것", 1125, 170, 46, RED, shadow=False)
    ink(br, "u2", "대만 2025년 확정치 · IMF 2030년 전망 격차", 1125, 250, 40, INK, shadow=False)
    ink(br, "s0", "앞으로 볼 신호", 1125, 170, 50, GRN, shadow=False)
    ink(br, "s1", "① 내년 3월, 2026년 1인당 소득", 1125, 250, 42, INK, shadow=False)
    ink(br, "s2", "② 원·달러 환율의 방향", 1125, 320, 42, INK, shadow=False)
    ink(br, "s3", "③ HBM 호황이 고용·소비로 번지는지", 1125, 390, 42, INK, shadow=False)
    f._enter(t + .2, "u1", "write", .5)
    f._enter(f.cue("통계당국의"), "u2", "write", 1.2)
    t = f.cue("앞으로", after=557)
    f._leave(t, "u1", "fade", .2)
    f._leave(t, "u2", "fade", .2)
    f._enter(t, "s0", "write", .5)
    f._enter(f.cue("내년", after=t), "s1", "write", .8)
    f._enter(f.cue("환율의", after=t), "s2", "write", .7)
    f._enter(f.cue("HBM의", after=t), "s3", "write", .9)

    # ── 끝: 한 줄의 숫자, 담장 밖까지 ────────────────────────────
    t = back("tst", "3월에", after=580)
    for i in ("cons", "birth"):
        f._leave(t, i, "fade", .1)
    ink(ts, "ln", "소득은 늘었는데, 순위는 밀렸다 / 더 빨리 달렸지만, 길이 갈라졌다", 960, 160, 44)
    f._enter(t + .3, "ln", "write", 2.0)
    wl = scene("wall", "wall.png", "결국", "dissolve", after=597)
    ink(wl, "end1", "누가 더 버느냐보다, 번 돈이 얼마나 많은 사람에게 닿느냐", 960, 160, 48)
    t = go(wl)
    f._enter(t + .3, "end1", "write", 2.0)
    f._cam(t, "wall", 1000, 560, 1.12, 12)
    f._tween(f.end - 1.6, "#stage", {"opacity": 0}, 1.6)
