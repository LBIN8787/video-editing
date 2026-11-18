"""AI 편 1:05 이후 — Wallet(토큰·승인·조건) → 원시적인 쇼핑 → 포피(가게가 문을 연다) → 항상 켜진 에이전트 → 세 칸과 빈칸 → 막는 쪽 → 책임 → 연 쪽 → 지금 알아 둘 것 → 끝.

주인공은 앞부분과 같은 에이전트 로봇. 손님(복숭아색 후드)·가게 주인(민트 앞치마)이 함께 연기한다. 글자는 제품 설명 화풍(고딕, 기울임 없음).
"""

NAVY, RED, MINT = "#18334a", "#b5452e", "#1f7a63"


def rest(f, A):
    prev = {"id": "street"}

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

    def lab(s, tid, text, x, y, size=58, color=NAVY):
        s.text(tid, text, x, y, size=size, color=color, font="gothic", rot=0)

    AG = ["agent_walk", "agent_stop", "agent_proud", "agent_work"]
    US = ["usr_phone", "usr_approve", "usr_relax", "usr_worry"]
    OW = ["own_welcome", "own_refuse", "own_shake", "own_think"]

    # ── Wallet: 찾는 데서 멈추지 않고 돈까지 ──────────────────────
    t = f.cue("먼저", after=64)
    f._leave(t, "q2", "fade", .4)
    f._cam(t, "street", 900, 640, 1.5, 2.0)
    f._pose(t + .3, "ag2", "agent_proud")
    m = scene("mall", "mall.png", "9월", "push")
    m.actor("agm", AG, x=-150, y=1000, h=260)
    lab(m, "dots", "9월 · 찾아 주는 에이전트 '닷츠'", 960, 140, 60)
    t = go(m)
    f._walk(t + .2, "agm", 1300, 5.0, bob=10)
    f._enter(f.cue("다치라는"), "dots", "write", .6)
    so = scene("shopopen", "shopopen.png", "이번에", "wipe", after=77)
    so.actor("own", OW, x=1350, y=1010, h=560)
    so.actor("ag4", AG, x=-150, y=1010, h=280, show="agent_walk")
    so.prop("card4", "card", 900, 520, 220, z=8, rot=-8)
    lab(so, "pay", "찾기 → 결제까지", 960, 140, 64)
    t = go(so)
    f._walk(t + .2, "ag4", 950, 2.2, bob=10)
    f._pose(f.cue("가게에", after=t), "ag4", "agent_proud")
    f._enter(f.cue("돈을", after=t), "card4", "pop", .5)
    f._enter(f.cue("돈을", after=t), "pay", "write", .6)
    f._move(f.cue("기능입니다") - .4, "card4", dx=380, dy=40, dur=.8)
    f._pose(f.cue("기능입니다"), "own", "own_welcome")

    # ── 걱정: 내 카드 번호 → 결제 토큰 ─────────────────────────────
    cl = scene("cardlab", "cardlab.png", "걱정은", "push")
    cl.actor("usr", US, x=200, y=1020, h=640, show="usr_worry")
    cl.prop("rcard", "card", 470, 330, 220, z=8, rot=-6)
    cl.prop("tok", "token", 1560, 560, 240, z=8, rot=6)
    lab(cl, "q", "내 카드 번호, AI 에게 맡겨도 될까?", 1000, 140, 60, RED)
    lab(cl, "nums", "번호 · 보안 코드 · 유효기간 모두 다른", 1100, 760, 46, NAVY)
    lab(cl, "once", "일회용 대리인 = 결제 토큰", 1100, 140, 64, MINT)
    t = go(cl)
    f._enter(f.cue("번호를", after=t), "q", "write", .8)
    f._enter(f.cue("번호를", after=t), "rcard", "pop", .5)
    t = f.cue("등록하면")
    f._leave(t - .5, "q", "fade", .3)
    f._move(t, "rcard", dx=170, dy=220, dur=1.0, rot=10, ease="power2.in")
    f._leave(t + .9, "rcard", "fade", .2)
    f._sound(t + .9, "click", .2)
    f._enter(f.cue("토큰이라는"), "tok", "slide", .6, dx=-300)
    f._sound(f.cue("토큰이라는"), "sparkle", .2)
    f._enter(f.cue("번호도"), "nums", "write", .9)
    f._enter(f.cue("일회용"), "once", "write", .7)
    f._pose(f.cue("일회용"), "usr", "usr_relax")
    # 에이전트도 가게도 진짜 번호를 못 본다 → 호텔 카드키
    ho = scene("hotel", "hotel.png", "호텔", "push")
    ho.actor("ag5", AG, x=1400, y=1010, h=300, show="agent_stop")
    ho.prop("hkey", "housekey", 560, 560, 200, z=8, hidden=False)
    ho.prop("kc", "keycard", 960, 560, 230, z=8)
    lab(ho, "hk1", "내 집 열쇠", 560, 380, 52)
    lab(ho, "hk2", "그날만 쓰는 카드키", 1150, 380, 52, MINT)
    t = go(ho)
    f._enter(t + .2, "hk1", "write", .4)
    t = f.cue("대신", after=t)
    f._enter(t, "kc", "pop", .5)
    f._enter(t, "hk2", "write", .5)
    f._move(t + .8, "kc", dx=380, dy=180, dur=.9, rot=15)
    f._pose(t + 1.6, "ag5", "agent_proud")

    # ── 결제 직전에는 반드시 사람이 ─────────────────────────────
    ap = scene("approve", "shopopen.png", "그리고", "dissolve", after=124)
    ap.actor("usr2", US, x=520, y=1020, h=660)
    ap.actor("ag6", AG, x=1500, y=1010, h=280, show="agent_walk")
    ap.prop("cart", "cart", 1200, 820, 300, z=7, anchor="bottom")
    ap.prop("fp", "phone_fp", 900, 470, 240, z=9)
    for i, (tx, wd) in enumerate([("무엇을", "사는지"), ("얼마", "얼마인지"), ("어떤 카드", "카드인지")]):
        lab(ap, f"chk{i}", f"✓ {tx}", 900, 170 + i * 80, 52)
    lab(ap, "fee", "출시 기간 수수료 없음", 960, 160, 58, MINT)
    t = go(ap)
    f._walk(t + .2, "ag6", -300, 1.6, bob=8)
    f._enter(t + .3, "cart", "slide", .9, dx=300)
    for i, wd in enumerate(["사는지", "얼마인지", "카드인지"]):
        f._enter(f.cue(wd, after=t), f"chk{i}", "write", .4)
        f._sound(f.cue(wd, after=t), "click-soft", .2)
    t = f.cue("지문으로")
    f._enter(t - .3, "fp", "pop", .5)
    f._pose(t, "usr2", "usr_approve")
    f._sound(t, "chime", .2)
    t = f.cue("수수료는")
    for i in range(3):
        f._leave(t - .3, f"chk{i}", "fade", .3)
    f._leave(t - .3, "fp", "shrink", .3)
    f._enter(t, "fee", "write", .6)

    # ── 지금 쓸 수 있는 사람은 아주 좁다 ───────────────────────────
    g = scene("gates", "gates.png", "다만", "push", after=144)
    g.actor("ag7", AG, x=-150, y=1000, h=260)
    gl = [("미국 거주", "미국에"), ("18세 이상", "18세"), ("Pro 구독", "프로구독자"), ("미국 발급 카드", "발급된")]
    for i, (tx, wd) in enumerate(gl):
        lab(g, f"g{i}", tx, 696 + i * 226, 300, 40)
    lab(g, "kr", "한국 등 다른 나라: 일정 미발표", 960, 150, 56, RED)
    lab(g, "sum1", "카드 정보는 넘기지 않고, 결정은 사람이", 960, 150, 58, MINT)
    t = go(g)
    for i, (tx, wd) in enumerate(gl):
        tt = f.cue(wd, after=t)
        f._enter(tt, f"g{i}", "write", .4)
        f._walk(tt, "ag7", 850 if i == 0 else 226, 1.0, bob=10)
        f._sound(tt + .5, "click-soft", .2)
    t = f.cue("한국을")
    f._enter(t, "kr", "write", .6)
    f._pose(t, "ag7", "agent_stop")
    t = f.cue("그러니까", after=164)
    f._leave(t, "kr", "fade", .3)
    f._enter(t + .3, "sum1", "write", .8)
    f._pose(t + .3, "ag7", "agent_proud")

    # ── 지금까지의 쇼핑: 유리창 너머로 몰래 ────────────────────────
    sw = scene("window", "shopwindow.png", "그런데", "dissolve", after=174)
    sw.actor("ag8", AG, x=600, y=1010, h=300, show="agent_stop")
    sw.actor("own2", OW, x=1450, y=1000, h=520, show="own_think")
    lab(sw, "prim", "화면 읽기 → 버튼 누르기 → 칸 채우기", 960, 150, 54)
    t = go(sw)
    f._cam(t, "window", 960, 560, 1.12, 4)
    t = f.cue("읽고")
    f._pose(t, "ag8", "agent_work")
    f._enter(t, "prim", "write", 2.5)
    t = f.cue("손을", after=200)
    f._pose(t, "own2", "own_refuse")
    f._sound(t, "error", .12)

    # ── 포피: 가게가 정식으로 문을 열어 준다 ───────────────────────
    pp = scene("poppy", "shopopen.png", "같은", "push", after=204)
    pp.actor("own3", OW, x=1300, y=1010, h=560, show="own_think")
    pp.actor("ag9", AG, x=-150, y=1010, h=280)
    lab(pp, "pname", "개인 에이전트 프로토콜 1.0 · '포피'", 960, 140, 58)
    lab(pp, "pmeta", "10월 메타와 함께 제안", 960, 220, 44, "#4a6070")
    pp.prop("pv", "perm_view", 420, 450, 170, z=9)
    pp.prop("pb", "perm_buy", 620, 450, 170, z=9)
    pp.prop("sh", "shield", 1300, 380, 180, z=9)
    pp.prop("si", "signin", 960, 500, 300, z=9)
    lab(pp, "pc", "손님: 무엇을 허락할지", 520, 620, 42)
    lab(pp, "ps", "가게: 할 수 있는 범위", 1300, 560, 42)
    t = go(pp)
    f._enter(f.cue("포피라고"), "pname", "write", .7)
    f._enter(f.cue("메타와"), "pmeta", "write", .5)
    t = f.cue("열어주는")
    f._pose(t - .6, "own3", "own_welcome")
    f._walk(t - .4, "ag9", 800, 2.0, bob=10)
    f._sound(t, "chime", .15)
    t = f.cue("손님은", after=227)
    f._leave(t, "pname", "fade", .3)
    f._leave(t, "pmeta", "fade", .3)
    f._enter(t + .3, "pc", "write", .5)
    f._enter(f.cue("보기만"), "pv", "pop", .4)
    f._enter(f.cue("주문까지"), "pb", "pop", .4)
    t = f.cue("가게는", after=235)
    f._enter(t, "ps", "write", .5)
    f._enter(t + .3, "sh", "pop", .4)
    f._pose(t, "own3", "own_think")
    t = f.cue("로그인은")
    for i in ("pv", "pb", "sh", "pc", "ps"):
        f._leave(t - .2, i, "fade", .3)
    f._enter(t, "si", "pop", .5)
    # 반응은 빨랐다: 쇼피파이의 모든 가게, 메타의 모든 사용자, 100곳+
    m2 = scene("mall2", "mall.png", "회사", "push", after=245)
    for i in range(12):
        m2.prop(f"mb{i}", "perm_buy", 300 + (i % 6) * 265, 330 + (i // 6) * 300, 110, z=8)
    lab(m2, "shop", "쇼피파이: 모든 가게에 켜 둠", 960, 140, 58)
    lab(m2, "meta", "메타 개인 에이전트: 모든 사용자", 960, 220, 50)
    m2.counter("n100", 960, 860, 110, MINT, font="gothic", text="")
    t = go(m2)
    t2 = f.cue("쇼피파인은")
    f._enter(t2, "shop", "write", .6)
    for i in range(12):
        f._enter(t2 + .6 + i * .12, f"mb{i}", "pop", .35)
        f._sound(t2 + .6 + i * .12, "pop", .06)
    f._enter(f.cue("메타의", after=t2), "meta", "write", .6)
    f._count(f.cue("100곳이"), "n100", 0, 100, 1.0, pre="설계 참여 ", suf="곳+")
    # 돈을 내는 길 + 가게와 대화하는 길
    pz = scene("puzzle", "mall.png", "돈을", "dissolve", after=264)
    pz._grade = True
    pz.prop("p1", "pc_wallet", 560, 540, 330, z=8)
    pz.prop("p2", "pc_talk", 840, 540, 330, z=8)
    pz.prop("p3", "pc_always", 1120, 540, 330, z=8)
    pz.prop("p4", "pc_empty", 1400, 540, 330, z=8)
    t = go(pz)
    f._grade(t, "puzzle", "blur(6px) brightness(.8)", .01)
    f._enter(t + .2, "p1", "slide", .6, dx=-200)
    f._enter(f.cue("가게와", after=t), "p2", "slide", .6, dx=-200)

    # ── 항상 켜져 있는 에이전트 ───────────────────────────────
    ni = scene("night2", "night.png", "지금", "push", after=276)
    ni.actor("ag10", ["agent_stop", "agent_work", "agent_walk", "agent_proud"], x=1330, y=708, h=240)
    ni.prop("ml", "mail", 700, 380, 200, z=8)
    ni.prop("al", "alarm", 1700, 260, 170, z=8)
    lab(ni, "call", "부를 때만 일한다", 700, 160, 60, "#e8fff6")
    lab(ni, "on", "항상 켜져 있는 에이전트", 700, 160, 60, "#e8fff6")
    t = go(ni)
    f._enter(f.cue("부를", after=t), "call", "write", .6)
    t = f.cue("항상", after=285)
    f._leave(t - .3, "call", "fade", .3)
    f._enter(t, "on", "write", .7)
    t = f.cue("매일이")   # 메일이 오거나
    f._enter(t, "ml", "slide", .8, dx=-500)
    f._move(t + .8, "ml", dx=520, dy=260, dur=.8, ease="power2.in")
    f._leave(t + 1.5, "ml", "fade", .2)
    f._pose(t + 1.5, "ag10", "agent_work")
    f._sound(t + 1.5, "notification", .15)
    t = f.cue("시각이")
    f._enter(t, "al", "pop", .4)
    for n in range(6):
        f._tween(t + .4 + n * .12, "#al .mv", {"rotation": 8 if n % 2 else -8}, .1, "none")
    f._sound(t + .4, "chime", .15)
    f._pose(f.cue("잠듭니다"), "ag10", "agent_stop")
    f._leave(f.cue("잠듭니다"), "al", "fade", .4)
    ds = scene("door", "doorstep.png", "사람으로", "push")
    ds.actor("ag11", AG, x=1300, y=1000, h=300, show="agent_stop")
    ds.prop("pcl", "parcel", 700, 900, 300, z=7, anchor="bottom")
    t = go(ds)
    f._enter(f.cue("택배가"), "pcl", "drop", .7)
    f._pose(f.cue("받아"), "ag11", "agent_proud")
    f._walk(f.cue("받아"), "ag11", -400, 1.2, bob=10)
    # 안전장치: 자격 정보는 바깥 보관소에
    lk = scene("locker", "locker.png", "눈여겨볼", "push")
    lk.actor("ag12", AG, x=520, y=1010, h=300, show="agent_stop")
    lk.prop("lcard", "card", 700, 420, 200, z=8, rot=-8)
    lk.prop("lkey", "housekey", 880, 420, 160, z=8)
    lk.prop("ltok", "token", 760, 560, 200, z=8)
    lk.prop("lsh", "shield", 1500, 300, 170, z=8)
    lk.prop("lstop", "hand_stop", 1500, 520, 280, z=8)
    lab(lk, "safe", "안전장치", 960, 130, 66, MINT)
    lab(lk, "quiet", "조용히 시작해서, 신뢰를 쌓아 가라", 960, 130, 56, NAVY)
    t = go(lk)
    f._enter(f.cue("안전장치입니다"), "safe", "write", .5)
    t = f.cue("비밀번호나")
    f._enter(t, "lcard", "pop", .4)
    f._enter(t + .2, "lkey", "pop", .4)
    t = f.cue("바깥에")
    f._move(t, "lcard", dx=800, dy=-60, dur=1.0)
    f._move(t, "lkey", dx=700, dy=-40, dur=1.0)
    f._leave(t + 1.0, "lcard", "fade", .2)
    f._leave(t + 1.0, "lkey", "fade", .2)
    f._sound(t + 1.0, "click", .2)
    t = f.cue("필요할")
    f._enter(t, "ltok", "pop", .4)
    f._pose(t, "ag12", "agent_proud")
    f._enter(f.cue("위험한"), "lsh", "pop", .4)
    t = f.cue("멈춰")
    f._enter(t - .3, "lstop", "pop", .4)
    f._pose(t, "ag12", "agent_stop")
    t = f.cue("처음에는", after=329)
    f._leave(t - .2, "safe", "fade", .2)
    f._enter(t, "quiet", "write", .9)
    # 코그니션: 데빈 앱스
    tm = scene("team", "team.png", "같은", "push", after=334)
    tm.actor("ag13", AG, x=960, y=1000, h=300, show="agent_work")
    for i in range(4):
        tm.prop(f"lm{i}", "mail", 960, 600, 120, z=8)
    lab(tm, "dv", "코그니션 · '데빈 앱스'", 960, 140, 60)
    t = go(tm)
    f._enter(f.cue("데뷔"), "dv", "write", .6)
    t = f.cue("링크")
    for i in range(4):
        f._enter(t + i * .15, f"lm{i}", "fade", .05)
        f._move(t + i * .15, f"lm{i}", dx=[-600, -250, 250, 600][i], dy=-250, dur=.9, ease="power2.out")
        f._leave(t + 1.0 + i * .15, f"lm{i}", "fade", .3)
    f._sound(t, "whoosh-short", .15)
    f._pose(f.cue("잠들었다가"), "ag13", "agent_stop")
    f._pose(f.cue("열면", after=347), "ag13", "agent_work")

    # ── 세 칸이 채워졌다, 빈칸 하나 ─────────────────────────────
    t = f.cue("정리하면")
    f._show(t, "puzzle", "dissolve", .8, "team")
    prev["id"] = "puzzle"
    f._enter(f.cue("일하는", after=t), "p3", "slide", .6, dx=-200)
    t = f.cue("빈칸이")
    f._enter(t, "p4", "pop", .6)
    f._sound(t, "pop", .2)
    pz.text("perm", "파는 쪽, 가게의 허락", 1400, 820, size=60, color=RED, font="gothic", rot=0)
    f._enter(f.cue("허락입니다"), "perm", "write", .6)

    # ── 막는 쪽: 유나이티드·아마존·증권사·은행 ────────────────────
    t = f.cue("처음에", after=369)
    f._show(t, "airport", "push", .8, "puzzle")
    prev["id"] = "airport"
    for i in ("lr", "dua", "d11"):
        f._leave(t, i, "fade", .1)
    f._cam(t, "airport", 1150, 600, 1.1, 1.0)
    rs = [("고객 정보 유출", "정보가"), ("원치 않은 구매", "원하지"), ("연방 규정 위반", "연방")]
    air = [s for s in f.sets if s.id == "airport"][0]
    for i, (tx, wd) in enumerate(rs):
        air.text(f"why{i}", tx, 640, 300 + i * 90, size=54, color=RED, font="gothic", rot=0)
        f._enter(f.cue(wd, after=t), f"why{i}", "write", .5)
        f._sound(f.cue(wd, after=t), "click-soft", .2)
    air.text("fareok", "요금 보기 ✓   예약 ✕", 640, 600, size=58, color=NAVY, font="gothic", rot=0)
    f._enter(f.cue("요금을"), "fareok", "write", .8)
    co = scene("court", "court.png", "아마존은", "push")
    lab(co, "amz", "아마존 · 다른 회사 쇼핑 에이전트에 소송 (지난해 11월)", 960, 150, 50)
    lab(co, "amz2", "법원 명령으로 일시 차단", 960, 230, 46, RED)
    t = go(co)
    f._enter(t + .2, "amz", "write", 1.0)
    f._enter(f.cue("법원"), "amz2", "write", .6)
    bk = scene("bank", "bank.png", "보도에", "push", after=407)
    bk.actor("ag14", AG, x=760, y=1010, h=300, show="agent_stop")
    bk.prop("bl", "padlock", 1250, 600, 200, z=8)
    lab(bk, "bk1", "대형 증권사·은행: 고객 돈을 옮기는 에이전트 차단", 960, 150, 48)
    t = go(bk)
    f._enter(t + .3, "bk1", "write", .9)
    f._enter(t + .5, "bl", "drop", .7)
    sw2 = scene("window2", "shopwindow.png", "오픈", "dissolve", after=413)
    sw2.actor("own4", OW, x=1350, y=1000, h=520, show="own_think")
    sw2.prop("guide", "mail", 900, 500, 240, z=8)
    lab(sw2, "gd", "OpenAI 판매자용 안내서", 960, 150, 56)
    t = go(sw2)
    f._enter(f.cue("판매자용"), "guide", "pop", .5)
    f._enter(f.cue("판매자용"), "gd", "write", .6)

    # ── 흥미로운 사실: 막으면서 규칙을 함께 만든다 ──────────────────
    t = f.cue("시에라의")
    f._show(t, "poppy", "push", .8, "window2")
    prev["id"] = "poppy"
    for i in ("si", "pc", "ps"):
        f._leave(t, i, "fade", .1)
    pp.text("list", "10월 9일 초안 설계 참여 명단: … 유나이티드 항공 …", 960, 160, size=48, color=NAVY, font="gothic", rot=0)
    f._enter(f.cue("명단에"), "list", "write", 1.0)
    t = f.cue("한쪽에서는", after=436)
    f._setv(t, "#airport", {"opacity": 1, "zIndex": 3, "clipPath": "inset(0 50% 0 0)"})
    f._setv(t, "#poppy", {"zIndex": 2})
    f._cam(t, "airport", 1300, 600, 1.15, .01)
    for i in range(3):
        f._leave(t, f"why{i}", "fade", .1)
    f._leave(t, "fareok", "fade", .1)
    f._leave(t, "list", "fade", .3)
    f._sound(t, "whoosh", .2)
    # 누가 보냈는지, 누가 책임지는지 모르는 에이전트
    t = f.cue("이", after=444)
    f._tween(t, "#airport", {"clipPath": "inset(0 0% 0 0)"}, .8)
    air.text("who", "누가 보냈나?  사고 나면 누가 책임지나?", 1150, 320, size=56, color=RED, font="gothic", rot=0)
    f._enter(f.cue("보냈는지"), "who", "write", 1.0)
    # 걸림돌은 기술이 아니라 책임
    cr = scene("cross", "crossroad.png", "여기서부터는", "push")
    cr.actor("ag15", AG, x=960, y=1020, h=280, show="agent_stop")
    lab(cr, "interp", "여기서부터는 해석", 1600, 90, 40, "#4a6070")
    lab(cr, "resp", "걸림돌은 기술이 아니라 책임", 960, 170, 64, RED)
    for i, (tx, x, y) in enumerate([("손님?", 520, 420), ("AI 회사?", 960, 330), ("가게?", 1400, 420)]):
        lab(cr, f"cq{i}", tx, x, y, 58)
    lab(cr, "a1", "배송·반품 → 가게", 1400, 520, 50, MINT)
    lab(cr, "a2", "무단 결제 → 카드사", 960, 430, 50, MINT)
    t = go(cr)
    f._enter(t, "interp", "write", .4)
    f._enter(f.cue("걸림돌은"), "resp", "write", .8)
    for i, wd in enumerate(["손님의", "회사의", "가계의"]):
        f._enter(f.cue(wd, after=464), f"cq{i}", "write", .4)
        f._sound(f.cue(wd, after=464), "click-soft", .2)
    t = f.cue("실제로", after=473)
    f._leave(t, "resp", "fade", .3)
    f._enter(f.cue("배송과", after=t), "a1", "write", .6)
    f._enter(f.cue("카드사가", after=t), "a2", "write", .6)

    # ── 문을 연 쪽 ───────────────────────────────────────────
    a2 = scene("airport2", "airport2.png", "반대로", "push", after=487)
    a2.actor("ag16", AG, x=-150, y=1000, h=280)
    lab(a2, "ex", "익스피디아·부킹닷컴 — OpenAI 와 손잡음", 960, 140, 50, MINT)
    lab(a2, "dl", "델타·아메리칸 — 일부 에이전트 예약 허용", 960, 220, 50, MINT)
    lab(a2, "spl", "같은 항공 업계 안에서도 판단이 갈린다", 960, 860, 54)
    t = go(a2)
    f._enter(f.cue("익스피디아와"), "ex", "write", .8)
    f._enter(f.cue("델타와"), "dl", "write", .8)
    f._walk(f.cue("델타와"), "ag16", 700, 2.2, bob=10)
    f._enter(f.cue("항공업계"), "spl", "write", .8)

    # ── 지금 알아 둘 것 ──────────────────────────────────────
    t = f.cue("그렇다면", after=507)
    f._show(t, "gates", "push", .8, "airport2")
    prev["id"] = "gates"
    f._leave(t, "sum1", "fade", .1)
    gs = [s for s in f.sets if s.id == "gates"][0]
    gs.text("ko", "한국에서 당장은 ✕", 960, 150, size=62, color=RED, font="gothic", rot=0)
    gs.text("ord", "비싼 요금제 → 일부 가게 → 넓게", 960, 150, size=58, color=NAVY, font="gothic", rot=0)
    f._leave(t, "kr", "fade", .1)
    f._enter(f.cue("한국에서"), "ko", "write", .6)
    t = f.cue("순서는")
    f._leave(t - .5, "ko", "fade", .3)
    f._enter(f.cue("처음에는", after=t), "ord", "write", 2.0)
    # 맡기는 것과 직접 하는 것 → 장바구니를 내 앞에
    ap2 = scene("cart2", "shopopen.png", "맡기는", "dissolve", after=538)
    ap2.actor("usr3", US, x=520, y=1020, h=660, show="usr_phone")
    ap2.actor("ag17", AG, x=1500, y=1010, h=280, show="agent_walk")
    ap2.prop("cart2p", "cart", 1100, 820, 300, z=7, anchor="bottom")
    lab(ap2, "who2", "카드 번호 → 에이전트 ✕   승인 → 사람", 960, 150, 54)
    lab(ap2, "sec", "알아서 사 주는 비서 ✕  장바구니를 가져다주는 비서 ○", 960, 150, 48, MINT)
    t = go(ap2)
    f._enter(f.cue("카드", after=t), "who2", "write", 1.0)
    t = f.cue("장바구니를", after=554)
    f._leave(t - .5, "who2", "fade", .3)
    f._enter(t - .3, "sec", "write", 1.2)
    f._enter(t, "cart2p", "slide", 1.0, dx=500)
    f._walk(t, "ag17", -300, 1.0, bob=8)
    f._pose(f.cue("가깝습니다", after=t), "usr3", "usr_approve")
    # 문제가 생기면 어디로
    t = f.cue("문제가", after=559)
    f._show(t, "cross", "push", .8, "cart2")
    prev["id"] = "cross"
    for i in range(3):
        f._leave(t, f"cq{i}", "fade", .1)
    f._leave(t, "interp", "fade", .1)
    cr.text("nr", "AI 회사가 모든 걸 책임지는 구조가 아니다", 960, 170, size=56, color=RED, font="gothic", rot=0)
    f._enter(f.cue("책임져"), "nr", "write", .9)

    # ── 끝: 두 장면 사이의 거리, 볼 신호 셋, 약속 ──────────────────
    t = f.cue("11월", after=579)
    f._setv(t, "#airport", {"opacity": 1, "zIndex": 3, "clipPath": "inset(0 50% 0 0)"})
    f._setv(t, "#street", {"opacity": 1, "zIndex": 2, "clipPath": "inset(0 0 0 50%)", "filter": "none"})
    f._setv(t, "#cross", {"opacity": 0})
    f._leave(t, "who", "fade", .1)
    f._cam(t, "airport", 1300, 600, 1.15, .01)
    f._cam(t, "street", 520, 600, 1.15, .01)
    f._move(t, "ag2", dx=-500, dur=.01)
    f._pose(t, "ag2", "agent_proud")
    f._leave(t, "q2", "fade", .1)
    f._leave(t, "slock9", "fade", .1)
    f._sound(t, "whoosh", .2)
    m3 = scene("mall3", "mall.png", "앞으로", "push")
    sig = [("① OpenAI — Pro·미국 밖으로?", "오픈"), ("② 막던 곳 — '허락된 에이전트' 기준?", "나이트드나"), ("③ 포피를 켜는 큰 가게 수", "포피")]
    for i, (tx, wd) in enumerate(sig):
        lab(m3, f"sg{i}", tx, 960, 200 + i * 100, 54)
    for i in range(12):
        m3.prop(f"mo{i}", "perm_buy", 300 + (i % 6) * 265, 600 + (i // 6) * 200, 100, z=8)
    t = go(m3)
    f._setv(t, "#airport", {"clipPath": "none"})
    f._setv(t, "#street", {"clipPath": "none"})
    for i, (tx, wd) in enumerate(sig):
        f._enter(f.cue(wd, after=t), f"sg{i}", "write", .7)
    t = f.cue("한꺼번에")
    for i in range(12):
        f._enter(t + i * .08, f"mo{i}", "pop", .3)
        f._sound(t + i * .08, "pop", .05)
    en = scene("end", "shopopen.png", "결국", "dissolve", after=616)
    en.actor("usr4", US, x=560, y=1020, h=660, show="usr_relax")
    en.actor("own5", OW, x=1400, y=1010, h=560, show="own_shake")
    en.actor("ag18", AG, x=980, y=1010, h=280, show="agent_proud")
    en.prop("hs", "handshake", 980, 420, 420, z=8)
    lab(en, "prom", "누가 책임지는지에 대한 약속", 960, 150, 62, MINT)
    t = go(en)
    f._enter(f.cue("책임지는지에"), "hs", "pop", .6)
    f._enter(f.cue("약속일지도"), "prom", "write", .8)
    f._cam(f.cue("장바구니를", after=627), "end", 960, 560, 1.12, 5)
    f._tween(f.end - 1.4, "#stage", {"opacity": 0}, 1.4)
