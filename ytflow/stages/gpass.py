"""G 보완 단계 — 시장 대본에 '말할 때 바뀜 + 동사를 연기하는 사물'을 채워 넣는다 (manual/09 §6, docs/64).

2026-11-24 사용자: "아직 업로드 하지 않은 업로드 예정인 영상들 전부 검수해서 g f방식으로 추가 보완해주새요 /
대사와 대본에 따라서 좀 더 정적인 움직임을 보완해주세요"

hybrid.make 가 렌더 직전에 부른다 (시장 브랜드 기본, 대본에 "g_pass": false 면 끔). 대본 파일은 바꾸지 않고 렌더할 때만 더한다
— make.py 로 대본을 다시 만들어도 빠지지 않고, 대본에 직접 적은 motion·panel 이 있으면 그것을 존중한다.

장면별로:
  · checklist — 줄마다 그 줄을 말하는 순간(`t`) 오른쪽 빈자리에 그 줄의 동사·대상을 연기하는 선 아이콘, 숫자가 있으면 그 숫자가 0에서 올라감.
                지난 줄의 사물은 다음 줄이 나올 때 치움 (focus 는 렌더러 기본).
  · motionboard — 앞 박자에 나온 카드를 뒤 박자에서 다시 말하면 그 낱말에 강조(hi).
  · bignum — 박자마다 그 박자의 동사를 연기하는 아이콘 하나 (큰 숫자 오른쪽).
  · quote — 내레이터가 인용문을 읽는 박자면 줄이 읽는 속도대로 나타남.
"""
from __future__ import annotations

import re

# 낱말 → (아이콘, 움직임). 위에서부터 먼저 맞는 것 (구체적인 것을 위에)
LEX: list[tuple[str, str, str]] = [
    (r"보증|대신 갚|대신 내", "handshake", "swing"),
    (r"약정|약속|계약|선주문|장기 계약", "handshake", "swing"),
    (r"회사채|대출|빌려|빚|부채|차입|이자", "receipt", "drop"),
    (r"손상|손실|파산|쓰러|무너|부도|적자|망하|망할", "triangle-alert", "shake"),
    (r"SEC|증권거래위원회|조사|감시|들여다|장부|회계|감사", "search", "beat"),
    (r"사임|물러|떠났|복귀|CEO|최고경영자|CFO|경영진|창업자", "user-round", "pop"),
    (r"연준|중앙은행|정부|재무장관|규제 당국|당국", "landmark", "draw"),
    (r"금리|이자율|국채", "percent", "pop"),
    (r"수출|규제|금지|막았|제재", "ban", "shake"),
    (r"데이터센터|서버|클라우드|네오클라우드", "server", "draw"),
    (r"전력|전기|발전|기가와트", "zap", "beat"),
    (r"HBM|D램|디램|낸드|메모리", "memory-stick", "drop"),
    (r"GPU|칩|반도체|TPU|가속기", "microchip", "drop"),
    (r"공장|생산|증설|생산능력|팹|공급", "factory", "draw"),
    (r"지분|투자|자금|돈을 대|돈이|돈을|현금|펀드|조달|모았|유치|모자라", "coins", "drop"),
    (r"매출|실적|영업이익|이익률|순이익", "chart-column", "pop"),
    (r"값|가격|가격이|단가|프리미엄", "tag", "swing"),
    (r"수요|주문|구매|사는 쪽|고객", "shopping-cart", "pop"),
    (r"기간|며칠|일 걸|회수|만기|속도", "hourglass", "spin"),
    (r"상장|공모|IPO", "bell", "shake"),
    (r"보도|기사|매체|언론|신문", "newspaper", "drop"),
    (r"위험|경고|의심|우려|걱정|거품", "siren", "shake"),
    (r"한국|코스피|계좌|삼성|SK하이닉스|하이닉스", "wallet", "pop"),
    (r"주가|시가총액|지수", "chart-line", "draw"),
    (r"하락|빠졌|빠지|떨어|급락|폭락|줄었|감소|깎", "trending-down", "drop"),
    (r"상승|올랐|오르|늘었|증가|급등|커졌|불어", "trending-up", "pop"),
    (r"순환|고리|돌고|돈다", "refresh-cw", "spin"),
    (r"오픈AI|앤트로픽|모델|챗GPT|AI", "bot", "pop"),
    (r"만약|가정|경우|틀리", "split", "pop"),
    (r"신호|지표|볼 것|확인", "target", "beat"),
    (r"과거|역사|그때|년 전|2000년|닷컴", "calendar-days", "pop"),
]
LOW = {"bot", "wallet"}
NUM = re.compile(r"[-−+]?\d[\d,]*(?:\.\d+)?\s?(?:조|억|만)?\s?(?:달러|원|%|배|일|개월|년|곳|명|개)?")
_ICON_OK: set | None = None


def _icons() -> set:
    global _ICON_OK
    if _ICON_OK is None:
        from .mograph import ICONS
        _ICON_OK = {p.stem for p in ICONS.glob("*.svg")}
    return _ICON_OK


def pick(*texts: str, avoid: str = "") -> tuple[str, str, str] | None:
    """글들(앞 글 우선)에서 가장 먼저 맞는 동사·대상 → (아이콘, 움직임, 맞은 낱말). avoid: 바로 앞 사물과 같은 아이콘은 피함."""
    for txt in texts:
        if not txt:
            continue
        best = None
        for pat, icon, anim in LEX:
            m = re.search(pat, txt)
            if m and icon in _icons() and icon != avoid:
                pos = m.start() + (10000 if icon in LOW else 0)   # 주어(회사·AI)보다 동사·대상을 먼저
                if best is None or pos < best[2]:
                    best = (icon, anim, pos, m.group(0))
        if best:
            return best[0], best[1], best[3]
    return None


def _number(label: str) -> str:
    """줄 글에서 숫자 하나 (단위 포함) — 가장 큰 의미의 숫자 대신 '처음 나오는 단위 있는 숫자'."""
    for m in NUM.finditer(label):
        s = m.group(0).strip()
        if re.fullmatch(r"(19|20)\d\d\s?년?", s) or re.fullmatch(r"\d{1,2}\s?(일|개월|년)", s):   # 연도·날짜는 숫자 카드로 세지 않음
            continue
        if re.search(r"[조억만%배달러원곳명개]", s):
            return s.replace("−", "-")
    return ""


def _beat_of(sc: dict, word: str) -> int:
    for k, b in enumerate(sc.get("beats") or []):
        if word and word in (b.get("say") or ""):
            return k
    return 0


def _checklist(sc: dict, n: int) -> None:
    if sc.get("panel") or sc.get("g_skip"):
        return
    rows = sc.get("rows") or []
    if not rows:
        return
    xl, tw = sc.get("x", 380), sc.get("text_w", 1000)
    free_l = xl + 100 + tw + 30
    if free_l > 1500:   # 오른쪽 빈자리가 없으면 글을 왼쪽으로 좁힘 (요약 + 움직이는 그림, 09 '요약 + 움직이는 그림')
        sc["x"], sc["text_w"] = 150, min(tw, 1000)
        xl, tw = 150, sc["text_w"]
        free_l = xl + 100 + tw + 30
    cx = (free_l + 1880) / 2
    # 대본에 이미 놓인 사물이 오른쪽 위에 있으면 아래로
    used = [(m.get("x", 0), m.get("y", 0)) for b in sc.get("beats") or [] for m in (b.get("motion") or [])]
    y_icon = 330 if not any(x > free_l - 50 and 200 < y < 520 for x, y in used) else 640
    y_num = y_icon + 210
    prev, prev_icon = None, ""
    for r_i, r in enumerate(rows):
        word = r.get("t") or ""
        k = _beat_of(sc, word)
        b = sc["beats"][k]
        hit = pick(r.get("label", ""), word, b.get("say") or "", avoid=prev_icon)
        if not hit:
            continue
        icon, anim, _ = hit
        prev_icon = icon
        mid = f"g{n}_{r_i}"
        mv = b.setdefault("motion", [])
        if prev:
            for pid in prev:
                mv.append({"t": word, "do": "out", "on": pid, "g": 1})
        mv.append({"t": word, "do": "glyph", "id": mid, "icon": icon, "anim": anim, "size": 140, "x": round(cx), "y": y_icon, "g": 1})
        ids = [mid]
        num = _number(r.get("label", ""))
        if num and not any(y_num - 120 < y < y_num + 120 and x > free_l - 50 for x, y in used):
            mv.append({"t": word, "do": "stat", "id": mid + "n", "value": num, "label": "", "x": round(cx), "y": y_num,
                       "fs": 84, "delay": 0.15, "g": 1})
            ids.append(mid + "n")
        prev = ids


def _motionboard(sc: dict) -> None:
    els = sc.get("els") or {}
    cards = {k: v for k, v in els.items() if v.get("kind") == "card" and v.get("label")}
    shown: set = set()
    for k, b in enumerate(sc.get("beats") or []):
        say = b.get("say") or ""
        acts = b.get("do") or []
        named = {a if isinstance(a, str) else next((a[x] for x in ("hi", "move", "dim", "hide", "swap") if x in a), None) for a in acts}
        if k > 0:
            n_add = 0
            for key, el in cards.items():
                if key not in shown or key in named or n_add >= 2:
                    continue
                words = [w for w in re.split(r"[\s·(),:/]+", el["label"]) if len(w) >= 2]
                w = next((w for w in words if w in say), None)
                if w:
                    acts.append({"hi": key, "t": w, "g": 1})
                    n_add += 1
            b["do"] = acts
        shown |= {a for a in named if a}


def _bignum(sc: dict, n: int) -> None:
    prev = None
    for k, b in enumerate(sc.get("beats") or []):
        hit = pick(b.get("say") or "")
        if not hit:
            continue
        icon, anim, word = hit
        mv = b.setdefault("motion", [])
        if any(m.get("x", 0) > 1450 and 300 < m.get("y", 0) < 640 for m in mv if not m.get("g")):
            continue
        mid = f"gb{n}_{k}"
        if prev:
            mv.append({"t": word, "do": "out", "on": prev, "g": 1})
        mv.append({"t": word, "do": "glyph", "id": mid, "icon": icon, "anim": anim, "size": 150, "x": 1700, "y": 470, "g": 1})
        prev = mid


def _quote(sc: dict) -> None:
    q = re.sub(r"\W", "", sc.get("quote") or "")[:10]
    beats = sc.get("beats") or []
    if q and len(beats) > 1 and q in re.sub(r"\W", "", beats[-1].get("say") or ""):
        sc.setdefault("_read_last", True)


def apply(spec: dict) -> dict:
    """대본(spec)을 제자리에서 보완하고 바꾼 수를 돌려줌."""
    stat = {"checklist": 0, "motionboard": 0, "bignum": 0, "quote": 0}
    for n, sc in enumerate(spec.get("scenes") or []):
        if sc.get("g_skip"):
            continue
        t = sc.get("type")
        if t == "checklist":
            _checklist(sc, n)
        elif t == "motionboard":
            _motionboard(sc)
        elif t == "bignum":
            _bignum(sc, n)
        elif t == "quote":
            _quote(sc)
        else:
            continue
        stat[t] += 1
    return stat
