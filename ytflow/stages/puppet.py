"""관절 인형 (벡터 캐릭터) — 대본의 행동을 그림이 직접 한다 (2026-11-14 사용자: "보기·잡기·걷기 단어가 아니라 이미지와 애니메이션으로").

졸라맨이 아니라 면·색·윤곽이 있는 평면 일러스트 캐릭터. 몸은 조각(머리·몸통·팔·다리)으로 나뉘고 관절을 축으로 돈다.
story 장면에서:
  {"t": "아기", "do": "puppet", "id": "bb", "char": "baby", "x": 900, "y": 1500, "s": 1.6}       # 등장 (y = 발바닥)
  {"t": "보고", "do": "act", "on": "bb", "a": "look"}       # 고개를 좌우로 돌려 둘러봄 + 눈 깜빡
  {"t": "잡고", "do": "act", "on": "bb", "a": "grab", "target": "blk"}   # 팔을 뻗어 물건을 잡음 (물건이 손에 붙음)
  {"t": "걷는", "do": "act", "on": "bb", "a": "walk", "dx": 600, "steps": 4}   # 뒤뚱뒤뚱 걸어감
  robot: look · reach(팔 뻗기) · fumble(집게가 헛집음, 대상이 미끄러짐) · confused(고개 갸웃 + 물음표) · walk
  prop: "block"(나무 블록) · "shirt_crumpled" · "shirt_folded" — {"do": "puppet", "char": "block", ...}
움직임은 행동할 때만 (제자리 흔들림 없음).
"""
from __future__ import annotations

NAVY, CREAM, RED, SKIN, WOOD = "#22304D", "#F4EBDD", "#C4452F", "#F2C9A6", "#D9A066"
SW = 5   # 윤곽선 굵기 (인형 좌표)


def _baby(p: str) -> tuple[str, dict]:
    """좌표: 발바닥 가운데 (0,0), 위로 음수. 키 약 300."""
    leg = lambda side: (f'<g id="{p}_leg{side}" style="transform-origin:{side * 20}px -78px">'
                        f'<rect x="{side * 20 - 15}" y="-80" width="30" height="66" rx="14" fill="{CREAM}" stroke="{NAVY}" stroke-width="{SW}"/>'
                        f'<ellipse cx="{side * 20 + side * 4}" cy="-10" rx="21" ry="12" fill="{NAVY}"/></g>')
    arm = lambda side: (f'<g id="{p}_arm{side}" style="transform-origin:{side * 44}px -150px">'
                        f'<rect x="{side * 44 - 12}" y="-152" width="24" height="64" rx="12" fill="{CREAM}" stroke="{NAVY}" stroke-width="{SW}"/>'
                        f'<circle id="{p}_hand{side}" cx="{side * 44}" cy="-86" r="14" fill="{SKIN}" stroke="{NAVY}" stroke-width="{SW}"/></g>')
    head = (f'<g id="{p}_head" style="transform-origin:0px -168px">'
            f'<circle cx="0" cy="-222" r="58" fill="{SKIN}" stroke="{NAVY}" stroke-width="{SW}"/>'
            f'<path d="M-52,-238 C-46,-292 40,-300 54,-240 C30,-262 -10,-266 -52,-238 Z" fill="{NAVY}"/>'
            f'<path d="M-6,-286 q10,-22 26,-12" fill="none" stroke="{NAVY}" stroke-width="{SW}" stroke-linecap="round"/>'
            f'<g id="{p}_eyes"><ellipse cx="-20" cy="-218" rx="6" ry="8" fill="{NAVY}"/><ellipse cx="20" cy="-218" rx="6" ry="8" fill="{NAVY}"/></g>'
            f'<circle cx="-34" cy="-200" r="9" fill="{RED}" opacity=".35"/><circle cx="34" cy="-200" r="9" fill="{RED}" opacity=".35"/>'
            f'<path d="M-10,-192 q10,9 20,0" fill="none" stroke="{NAVY}" stroke-width="4" stroke-linecap="round"/></g>')
    body = (f'<rect x="-48" y="-168" width="96" height="98" rx="34" fill="{CREAM}" stroke="{NAVY}" stroke-width="{SW}"/>'
            f'<rect x="-46" y="-128" width="92" height="14" fill="{RED}" opacity=".85"/>')
    svg = f'<g id="{p}_body">{leg(-1)}{leg(1)}{arm(-1)}{body}{head}{arm(1)}</g>'
    return svg, {"w": 260, "h": 320, "hand": (44, -86)}


def _robot(p: str) -> tuple[str, dict]:
    """키 약 360. 오른팔(관절 2개) + 집게."""
    head = (f'<g id="{p}_head" style="transform-origin:0px -230px">'
            f'<line x1="0" y1="-330" x2="0" y2="-300" stroke="{NAVY}" stroke-width="{SW}"/><circle cx="0" cy="-336" r="10" fill="{RED}" stroke="{NAVY}" stroke-width="4"/>'
            f'<rect x="-70" y="-300" width="140" height="80" rx="22" fill="{NAVY}"/>'
            f'<rect x="-56" y="-288" width="112" height="56" rx="14" fill="{CREAM}"/>'
            f'<g id="{p}_eyes"><circle cx="-22" cy="-260" r="9" fill="{NAVY}"/><circle cx="22" cy="-260" r="9" fill="{NAVY}"/></g></g>')
    body = (f'<rect x="-80" y="-224" width="160" height="150" rx="30" fill="{NAVY}"/>'
            f'<rect x="-46" y="-196" width="92" height="50" rx="10" fill="#33456A"/><circle cx="-24" cy="-171" r="8" fill="{RED}"/><circle cx="0" cy="-171" r="8" fill="#F3D36B"/><circle cx="24" cy="-171" r="8" fill="{CREAM}"/>'
            f'<rect x="-60" y="-78" width="120" height="40" rx="12" fill="#33456A"/>'
            f'<circle cx="-40" cy="-28" r="26" fill="{NAVY}" stroke="{CREAM}" stroke-width="6"/><circle cx="40" cy="-28" r="26" fill="{NAVY}" stroke="{CREAM}" stroke-width="6"/>')
    arm = (f'<g id="{p}_arm" style="transform-origin:80px -190px">'
           f'<rect x="76" y="-202" width="100" height="26" rx="13" fill="#33456A" stroke="{NAVY}" stroke-width="4"/>'
           f'<g id="{p}_fore" style="transform-origin:170px -189px">'
           f'<circle cx="170" cy="-189" r="15" fill="{NAVY}"/>'
           f'<rect x="168" y="-200" width="92" height="22" rx="11" fill="#33456A" stroke="{NAVY}" stroke-width="4"/>'
           f'<g id="{p}_grip" style="transform-origin:262px -189px">'
           f'<path id="{p}_f1" d="M258,-196 l34,-16 l6,8 l-30,18 z" fill="{NAVY}" style="transform-origin:262px -192px"/>'
           f'<path id="{p}_f2" d="M258,-182 l34,16 l6,-8 l-30,-18 z" fill="{NAVY}" style="transform-origin:262px -186px"/></g></g></g>')
    svg = f'<g id="{p}_body">{body}{head}{arm}</g>'
    return svg, {"w": 420, "h": 380, "hand": (292, -189)}


def _prop(kind: str, p: str) -> tuple[str, dict]:
    if kind == "block":
        return (f'<g id="{p}_body"><rect x="-34" y="-68" width="68" height="68" rx="6" fill="{WOOD}" stroke="{NAVY}" stroke-width="{SW}"/>'
                f'<text x="0" y="-22" text-anchor="middle" font-family="serif-x" font-size="44" fill="{RED}">A</text></g>', {"w": 80, "h": 80})
    if kind == "shirt_folded":
        return (f'<g id="{p}_body"><rect x="-90" y="-70" width="180" height="70" rx="10" fill="{RED}" stroke="{NAVY}" stroke-width="{SW}"/>'
                f'<path d="M-90,-46 h180 M-30,-70 q30,18 60,0" fill="none" stroke="{NAVY}" stroke-width="4"/></g>', {"w": 200, "h": 80})
    # shirt_crumpled: 구겨진 덩어리 (주름 선)
    return (f'<g id="{p}_body"><path d="M-110,-6 C-130,-40 -96,-82 -60,-74 C-40,-112 20,-104 34,-80 C70,-104 120,-70 108,-38 C130,-20 112,0 80,-2 Z" '
            f'fill="{RED}" stroke="{NAVY}" stroke-width="{SW}" stroke-linejoin="round"/>'
            f'<path d="M-70,-40 q20,14 40,-6 M-10,-58 q14,20 34,6 M40,-36 q14,16 36,0 M-90,-20 q30,4 50,-8" fill="none" stroke="{NAVY}" stroke-width="4" stroke-linecap="round"/>'
            f'<path d="M86,-50 l26,-14 l8,12" fill="{RED}" stroke="{NAVY}" stroke-width="4"/></g>', {"w": 260, "h": 120})


def build(char: str, p: str) -> tuple[str, dict]:
    if char == "baby":
        return _baby(p)
    if char == "robot":
        return _robot(p)
    return _prop(char, p)


def act(js: list, sfx: list, p: str, a: str, t: float, info: dict, m: dict, target: tuple | None = None):
    """행동 → GSAP. info: 캐릭터 정보, target: (대상 id, 대상 화면 좌표 차 dx, dy)."""
    E = js.append
    if a == "look":
        E(f'tl.to("#{p}_head",{{rotation:-14,duration:0.35,ease:"power2.inOut"}},{t:.2f});'
          f'tl.to("#{p}_eyes",{{x:-8,duration:0.3}},{t:.2f});'
          f'tl.to("#{p}_head",{{rotation:14,duration:0.6,ease:"power2.inOut"}},{t + 0.5:.2f});'
          f'tl.to("#{p}_eyes",{{x:8,duration:0.4}},{t + 0.55:.2f});'
          f'tl.to("#{p}_head",{{rotation:0,duration:0.4,ease:"power2.inOut"}},{t + 1.25:.2f});'
          f'tl.to("#{p}_eyes",{{x:0,duration:0.3}},{t + 1.3:.2f});'
          f'tl.to("#{p}_eyes",{{scaleY:0.1,transformOrigin:"50% 50%",duration:0.06,yoyo:true,repeat:1}},{t + 1.7:.2f});')
    elif a == "grab":   # 아기: 오른팔을 들어 앞으로 → 물건이 손으로
        E(f'tl.to("#{p}_arm1",{{rotation:-110,duration:0.45,ease:"back.out(1.6)"}},{t:.2f});'
          f'tl.to("#{p}_head",{{rotation:8,duration:0.3}},{t:.2f});')
        if target:
            tid, dx, dy = target
            E(f'tl.to("#{tid}",{{x:{dx:.0f},y:{dy:.0f},scale:0.8,duration:0.4,ease:"power2.in"}},{t + 0.4:.2f});'
              f'tl.to("#{p}_arm1",{{rotation:-60,duration:0.4,ease:"power2.out"}},{t + 0.85:.2f});'
              f'tl.to("#{tid}",{{x:"-=40",y:"+=50",duration:0.4,ease:"power2.out"}},{t + 0.85:.2f});')
        sfx.append(("pop", t + 0.8))
    elif a == "walk":   # 다리 번갈아 + 몸 위아래 + 앞으로 (행동, 제자리 흔들림 아님)
        n, dx = int(m.get("steps", 4)), float(m.get("dx", 500))
        d = float(m.get("dur", 0.5))
        for k in range(n):
            s = 1 if k % 2 == 0 else -1
            tk = t + k * d
            legs = (f'#{p}_leg-1', f'#{p}_leg1') if "baby" in m.get("_char", "baby") else ()
            if legs:
                E(f'tl.to("{legs[0]}",{{rotation:{22 * s},duration:{d / 2:.2f},ease:"sine.inOut"}},{tk:.2f});'
                  f'tl.to("{legs[1]}",{{rotation:{-22 * s},duration:{d / 2:.2f},ease:"sine.inOut"}},{tk:.2f});'
                  f'tl.to("#{p}_arm-1",{{rotation:{-18 * s},duration:{d / 2:.2f}}},{tk:.2f});'
                  f'tl.to("#{p}_arm1",{{rotation:{18 * s},duration:{d / 2:.2f}}},{tk:.2f});')
            E(f'tl.to("#{p}_body",{{y:-14,duration:{d / 2:.2f},ease:"sine.out",yoyo:true,repeat:1}},{tk:.2f});'
              f'tl.to("#{p}_body",{{rotation:{4 * s},transformOrigin:"0px 0px",duration:{d / 2:.2f}}},{tk:.2f});')
        E(f'tl.to("#{p}",{{x:"+={dx:.0f}",duration:{n * d:.2f},ease:"none"}},{t:.2f});'
          f'tl.to("#{p}_leg-1,#{p}_leg1,#{p}_arm-1,#{p}_arm1,#{p}_body",{{rotation:0,duration:0.25}},{t + n * d:.2f});')
        for k in range(n):
            sfx.append(("click-soft", t + k * d + d / 2))
    elif a == "reach":   # 로봇: 팔 들어 앞으로 뻗기
        E(f'tl.to("#{p}_arm",{{rotation:{m.get("ang", 28)},duration:0.6,ease:"power2.inOut"}},{t:.2f});'
          f'tl.to("#{p}_fore",{{rotation:{m.get("fore", 30)},duration:0.6,ease:"power2.inOut"}},{t + 0.1:.2f});'
          f'tl.to("#{p}_f1",{{rotation:-20,duration:0.25}},{t + 0.5:.2f});tl.to("#{p}_f2",{{rotation:20,duration:0.25}},{t + 0.5:.2f});')
        sfx.append(("whoosh-short", t))
    elif a == "fumble":   # 집게가 헛집음: 닫았다 열기 3번, 대상이 미끄러짐
        for k in range(3):
            tk = t + k * 0.55
            E(f'tl.to("#{p}_f1",{{rotation:10,duration:0.12}},{tk:.2f});tl.to("#{p}_f2",{{rotation:-10,duration:0.12}},{tk:.2f});'
              f'tl.to("#{p}_f1",{{rotation:-20,duration:0.15}},{tk + 0.25:.2f});tl.to("#{p}_f2",{{rotation:20,duration:0.15}},{tk + 0.25:.2f});'
              f'tl.to("#{p}_fore",{{rotation:"+=6",duration:0.12,yoyo:true,repeat:1}},{tk:.2f});')
            if target:
                E(f'tl.to("#{target[0]}",{{x:"+={(-1) ** k * 18}",rotation:{(-1) ** k * 6},duration:0.2,ease:"power1.out"}},{tk + 0.12:.2f});')
            sfx.append(("click-soft", tk + 0.1))
    elif a == "confused":
        E(f'tl.to("#{p}_head",{{rotation:-16,duration:0.4,ease:"back.out(2)"}},{t:.2f});'
          f'tl.fromTo("#{p}_q",{{opacity:0,scale:0.2,y:20}},{{opacity:1,scale:1,y:0,duration:0.45,ease:"back.out(2.5)"}},{t + 0.15:.2f});')
        sfx.append(("pop", t + 0.15))
