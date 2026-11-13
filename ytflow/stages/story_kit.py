"""이야기 그림판 v2 — 재료와 움직임 (2026-11-13 사용자: "졸라맨·애니메이션 품질이 너무 낮고, 그림 패턴이 매번 똑같다").

조사(docs/26-story-craft.md)에서 가져온 노하우를 코드로:
1. 재료: 졸라맨 대신 **실제 사진 오려 붙이기**(폴라로이드·찢은 가장자리·동그란 인물), **문서·기사 캡처 + 형광펜**, 둥근 아이콘 스티커, 인물 이름 카드, 큰 글자.
2. 같은 손: 모든 재료가 같은 처리(종이 테두리·그림자·살짝 기울임·테이프, 사진은 같은 색 보정) — 섞여도 한 영상으로 보이게.
3. 깊이: 뒤·가운데·앞 세 겹이 카메라가 움직일 때 다른 속도로 움직임(2.5D 패럴랙스), 뒤 겹은 살짝 흐림.
4. 움직임 원칙: 예비 동작·과장 뒤 안착(back.out), 그림자가 떠 있다 내려앉음, 요소마다 등장 방식을 돌려 씀(떨어뜨리기·밀어 넣기·뒤집기·내려놓기·펼치기).
5. 변화는 '새 스타일'이 아니라 배경·구도로: 밝은 종이 → 어두운 종이 → 사진 전체 배경, 단락 사이 검은 화면 거침.
"""
from __future__ import annotations

import hashlib
import html as H
import random

INK, RED, CARD, MARK = "#22304D", "#C4452F", "#FBF8F1", "#F3D36B"
GRADE = "sepia(.16) saturate(.88) contrast(1.06) brightness(1.02)"   # 사진 색을 한 영상 안에서 맞춤 (같은 손)
SHADOW = "drop-shadow(0 16px 22px rgba(30,24,16,.30))"
LIFT = "drop-shadow(0 46px 44px rgba(30,24,16,.22))"
POOL = {   # 등장 방식 돌려 쓰기 (같은 방식 연속 금지)
    "photo": ["drop", "slide", "flip", "place"],
    "doc": ["slide", "unfold", "drop", "place"],
    "sticker": ["pop", "place", "drop"],
    "card": ["slide", "drop", "flip"],
    "big": ["rise", "place"],
    "chip": ["drop", "slide", "place"],
}
LAYER = {"photo": 1, "doc": 1, "card": 1, "sticker": 2, "big": 0, "chip": 2, "note": 2, "stamp": 2}


def _e(s) -> str:
    return H.escape(str(s))


def _rot(mid: str, amp: float = 3.0) -> float:
    h = int(hashlib.md5(mid.encode()).hexdigest()[:6], 16)
    return round(((h % 1000) / 1000 * 2 - 1) * amp, 2)


def torn(seed: str, n: int = 44, j: float = 1.4) -> str:
    """찢은 종이 가장자리 (clip-path polygon, %)."""
    r = random.Random(seed)
    pts = []
    for k in range(n):   # 위 → 오른쪽 → 아래 → 왼쪽
        f = k / n * 4
        side, u = int(f), (f % 1) * 100
        d = r.uniform(0, j)
        pts.append({0: (u, d), 1: (100 - d, u), 2: (100 - u, 100 - d), 3: (d, 100 - u)}[side])
    return "polygon(" + ",".join(f"{x:.1f}% {y:.1f}%" for x, y in pts) + ")"


def enter(B, did: str, t: float, style: str, rot: float, x: float = 0):
    """등장 + 안착. 그림자가 떠 있다(LIFT) 내려앉음(SHADOW)."""
    js = B.js
    land = f'tl.fromTo("#{did}",{{filter:"{LIFT}"}},{{filter:"{SHADOW}",duration:0.5,ease:"power2.out"}},{t + 0.25:.2f});'
    if style == "drop":
        js.append(f'tl.fromTo("#{did}",{{opacity:0,y:-160,rotation:{rot - 9},scale:1.06}},{{opacity:1,y:0,rotation:{rot},scale:1,duration:0.6,ease:"back.out(1.5)"}},{t:.2f});')
    elif style == "slide":
        dx = -700 if x < 1920 else 700
        js.append(f'tl.fromTo("#{did}",{{opacity:0,x:{dx},rotation:{rot + (6 if dx < 0 else -6)}}},{{opacity:1,x:0,rotation:{rot},duration:0.6,ease:"power3.out"}},{t:.2f});')
    elif style == "flip":
        js.append(f'tl.fromTo("#{did}",{{opacity:0,rotationY:-85,transformPerspective:1600,rotation:{rot}}},{{opacity:1,rotationY:0,duration:0.65,ease:"back.out(1.3)"}},{t:.2f});')
    elif style == "place":   # 위에서 내려놓기 (크게 → 제자리)
        js.append(f'tl.fromTo("#{did}",{{opacity:0,scale:1.22,rotation:{rot + 4}}},{{opacity:1,scale:1,rotation:{rot},duration:0.45,ease:"power3.out"}},{t:.2f});')
    elif style == "unfold":
        js.append(f'tl.fromTo("#{did}",{{opacity:0,scaleY:0.05,transformOrigin:"50% 0%",rotation:{rot}}},{{opacity:1,scaleY:1,duration:0.6,ease:"power2.out"}},{t:.2f});')
    elif style == "rise":
        js.append(f'tl.fromTo("#{did}",{{opacity:0,y:90}},{{opacity:1,y:0,duration:0.8,ease:"power3.out"}},{t:.2f});')
        return
    else:   # pop
        js.append(f'tl.fromTo("#{did}",{{opacity:0,scale:0.3,rotation:{rot - 20}}},{{opacity:1,scale:1,rotation:{rot},duration:0.5,ease:"back.out(2.2)"}},{t:.2f});')
    js.append(land)


def pick_in(B, kind: str, mid: str, given: str | None) -> str:
    if given:
        B.last_in = given
        return given
    pool = POOL.get(kind, ["pop"])
    h = int(hashlib.md5(mid.encode()).hexdigest()[:4], 16)
    cands = [p for p in pool if p != B.last_in] or pool
    B.last_in = cands[h % len(cands)]
    return B.last_in


def tag(text: str, fs: int = 54, col: str = INK) -> str:
    """이름표: 손글씨를 작은 종이 띠 위에 (어떤 배경에서도 읽힘)."""
    return (f'<span style="display:inline-block;background:{CARD};padding:4px 22px 8px;font-family:pen;font-size:{fs}px;color:{col};'
            f'box-shadow:0 4px 10px rgba(0,0,0,.18);white-space:nowrap">{_e(text)}</span>')


def kit(B, m: dict, t: float, mid: str, x: float, y: float, asset) -> bool:
    """새 재료. 처리했으면 True."""
    do = m["do"]
    did = f"{B.p}_{mid}"
    rot = m.get("rot", _rot(mid))
    z = m.get("z", LAYER.get(do, 1))
    out = B.layer(z)
    if do == "photo":   # 실제 사진 오려 붙이기
        src = asset(m["src"])
        w = m.get("w", 640)
        h = m.get("h", round(w * m.get("ratio", 0.72)))
        frame = m.get("frame", "polaroid")
        fx, fy = m.get("focus", [0.5, 0.4])
        img = (f'<img src="assets/{src}" style="display:block;width:{w}px;height:{h}px;object-fit:cover;object-position:{fx * 100:.0f}% {fy * 100:.0f}%;'
               f'filter:{GRADE}">')
        cap = m.get("caption", "")
        if frame == "polaroid":
            inner = (f'<div style="background:{CARD};padding:22px 22px {96 if cap else 22}px">{img}'
                     + (f'<div style="position:absolute;left:0;right:0;bottom:16px;text-align:center;font-family:pen;font-size:{m.get("cfs", 60)}px;color:{INK};white-space:nowrap">{_e(cap)}</div>' if cap else "")
                     + f'</div><div style="position:absolute;left:50%;top:-26px;width:190px;height:52px;margin-left:-95px;background:rgba(236,220,170,.82);transform:rotate({-rot * 1.6 + 3:.1f}deg)"></div>')
            bw, bh = w + 44, h + (118 if cap else 44)
        elif frame == "round":
            inner = (f'<div style="width:{w}px;height:{w}px;border-radius:50%;overflow:hidden;border:14px solid {CARD};box-sizing:border-box">'
                     f'<img src="assets/{src}" style="width:100%;height:100%;object-fit:cover;object-position:{fx * 100:.0f}% {fy * 100:.0f}%;filter:{GRADE}"></div>'
                     + (f'<div style="position:absolute;left:-200px;right:-200px;top:{w + 6}px;text-align:center">{tag(cap)}</div>' if cap else ""))
            bw, bh = w, w
        else:   # cut: 찢은 종이 가장자리 + 종이 테두리
            poly = torn(mid)
            inner = (f'<div style="position:absolute;inset:-14px;background:{CARD};clip-path:{torn(mid + "r", 44, 1.0)}"></div>'
                     f'<div style="position:relative;clip-path:{poly}">{img}</div>'
                     + (f'<div style="position:absolute;left:-200px;right:-200px;top:{h + 18}px;text-align:center">{tag(cap)}</div>' if cap else ""))
            bw, bh = w, h
        out.append(f'<div id="{did}" style="position:absolute;left:{x - bw / 2:.0f}px;top:{y - bh / 2:.0f}px;width:{bw}px;height:{bh}px;'
                   f'transform:rotate({rot}deg);filter:{SHADOW};opacity:0">{inner}</div>')
        enter(B, did, t, pick_in(B, "photo", mid, m.get("in")), rot, x)
        B._sfx("paper", t) if False else B._sfx("whoosh-short", t)
        B.pos[mid] = (x, y, bw, bh)
        if m.get("credit"):
            B.credits.append(m["credit"])
        return True
    if do == "doc":   # 문서·기사 캡처 (종이처럼) — 형광펜은 do: mark
        src = asset(m["src"])
        w = m.get("w", 1300)
        ratio = m.get("ratio", 0.42)
        h = round(w * ratio)
        crop = m.get("crop")   # [y0, y1] 비율: 캡처의 일부만
        pos_y = f"{crop[0] * 100:.0f}%" if crop else "0%"
        out.append(f'<div id="{did}" style="position:absolute;left:{x - w / 2:.0f}px;top:{y - h / 2:.0f}px;width:{w}px;height:{h}px;background:#fff;'
                   f'transform:rotate({rot}deg);filter:{SHADOW};opacity:0;overflow:hidden">'
                   f'<img src="assets/{src}" style="width:100%;height:auto;display:block;transform:translateY(-{(crop[0] if crop else 0) * 100:.0f}%)">'
                   f'<div style="position:absolute;inset:0;background:linear-gradient(115deg,rgba(255,255,255,0) 60%,rgba(0,0,0,.05))"></div></div>')
        _ = pos_y
        enter(B, did, t, pick_in(B, "doc", mid, m.get("in")), rot, x)
        B._sfx("whoosh-short", t)
        B.pos[mid] = (x, y, w, h)
        if m.get("label"):
            B.html_label(x - w / 2 + 40, y + h / 2 + 14, m["label"], t + 0.5)
        return True
    if do == "mark":   # 문서 위 형광펜 (rect = 문서 안 비율 [x0,y0,x1,y1])
        on = m.get("on")
        if on in B.pos:
            x0, y0, x1, y1 = m["rect"]
            hid = f"{B.p}_{on}_hl{len(B.js)}"
            B.js_html_into(on, f'<div id="{hid}" style="position:absolute;left:{x0 * 100:.1f}%;top:{y0 * 100:.1f}%;width:{(x1 - x0) * 100:.1f}%;height:{(y1 - y0) * 100:.1f}%;'
                               f'background:{MARK};mix-blend-mode:multiply;opacity:.85;transform-origin:left center"></div>')
            B.js.append(f'tl.fromTo("#{hid}",{{scaleX:0}},{{scaleX:1,duration:0.55,ease:"power1.inOut"}},{t:.2f});')
            B._sfx("pencil", t)
        return True
    if do == "sticker":   # 둥근 아이콘 스티커 (남색 원 + 크림 아이콘 + 종이 테두리)
        from .story import _children
        d = m.get("d", 230)
        dark = m.get("tone", "navy") == "navy"
        bg, fg = (INK, "#F4EBDD") if dark else (CARD, INK)   # tone: navy(기본) · cream(어두운 배경 위)
        if m.get("color") == "red":
            bg = RED
        kids = "".join(_children(m["icon"]))
        svg = (f'<svg viewBox="-1 -1 26 26" width="{d * 0.56:.0f}" height="{d * 0.56:.0f}" fill="none" stroke="{fg}" stroke-width="1.9" '
               f'stroke-linecap="round" stroke-linejoin="round">{kids}</svg>')
        out.append(f'<div id="{did}" style="position:absolute;left:{x - d / 2:.0f}px;top:{y - d / 2:.0f}px;width:{d}px;height:{d}px;'
                   f'transform:rotate({rot}deg);filter:{SHADOW};opacity:0">'
                   f'<div style="width:100%;height:100%;border-radius:50%;background:{bg};border:10px solid {CARD};box-sizing:border-box;'
                   f'display:flex;align-items:center;justify-content:center">{svg}</div>'
                   + (f'<div style="position:absolute;left:-300px;right:-300px;top:{d + 8}px;text-align:center">{tag(m["label"], m.get("lfs", 52))}</div>' if m.get("label") else "")
                   + '</div>')
        enter(B, did, t, pick_in(B, "sticker", mid, m.get("in")), rot, x)
        B._sfx("pop", t)
        B.pos[mid] = (x, y, d, d)
        return True
    if do == "card":   # 인물·사물 이름 카드 (사진을 쓸 수 없을 때 — 졸라맨 대신)
        w, h = m.get("w", 760), m.get("h", 420)
        out.append(f'<div id="{did}" style="position:absolute;left:{x - w / 2:.0f}px;top:{y - h / 2:.0f}px;width:{w}px;height:{h}px;background:{CARD};'
                   f'transform:rotate({rot}deg);filter:{SHADOW};opacity:0;background-image:repeating-linear-gradient(0deg,transparent 0 63px,rgba(47,93,140,.16) 63px 65px);">'
                   f'<div style="position:absolute;left:0;right:0;top:86px;height:4px;background:{RED};opacity:.75"></div>'
                   f'<div style="position:absolute;left:44px;top:18px;font-family:sans;font-size:40px;color:#6b6f78;white-space:nowrap">{_e(m.get("kicker", ""))}</div>'
                   f'<div style="position:absolute;left:44px;top:118px;font-family:serif-x;font-size:{m.get("fs", 96)}px;color:{INK};white-space:nowrap">{_e(m.get("title", ""))}</div>'
                   f'<div style="position:absolute;left:48px;top:{130 + m.get("fs", 96) * 1.15:.0f}px;font-family:pen;font-size:62px;color:{RED};white-space:nowrap">{_e(m.get("sub", ""))}</div>'
                   f'<div style="position:absolute;right:-16px;top:-30px;width:150px;height:46px;background:rgba(236,220,170,.82);transform:rotate(28deg)"></div></div>')
        enter(B, did, t, pick_in(B, "card", mid, m.get("in")), rot, x)
        B._sfx("whoosh-short", t)
        B.pos[mid] = (x, y, w, h)
        return True
    if do == "big":   # 큰 글자 (연도·핵심 낱말) — 뒤 겹, 천천히 떠오름
        fs = m.get("fs", 300)
        col = m.get("color", INK)
        out.append(f'<div id="{did}" style="position:absolute;left:{x - 1500}px;top:{y - fs * 0.62:.0f}px;width:3000px;text-align:center;font-family:serif-x;'
                   f'font-size:{fs}px;line-height:1.1;color:{col};opacity:0;white-space:nowrap">{_e(m.get("text", ""))}'
                   + (f'<div style="font-family:pen;font-size:{m.get("nfs", 80)}px;color:{RED};margin-top:-10px">{_e(m["note"])}</div>' if m.get("note") else "")
                   + '</div>')
        enter(B, did, t, "rise", 0)
        B.js.append(f'tl.to("#{did}",{{opacity:{m.get("alpha", 1)},duration:0.01}},{t + 0.8:.2f});')
        B.pos[mid] = (x, y, len(m.get("text", "")) * fs * 0.8, fs * 1.2)
        return True
    if do == "bg":   # 배경 바꾸기 (화면 기준): paper · dark · photo
        B.bg_events.append((t, m.get("mode", "paper"), asset(m["src"]) if m.get("src") else None, m.get("credit")))
        return True
    return False
