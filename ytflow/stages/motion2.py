"""말에 맞춰 움직이는 사물 애니메이션 (모션 무대, docs/25 §5) — 2026-11-13 사용자: "요약문 느낌이 아니라
빠른 템포로 폴더·스킬·스크립트 같은 것이 대본에 맞춰 애니메이션으로 생성되는 느낌".

박자의 낱말을 말하는 순간(받아쓰기 단어 시각) 사물이 생기고·열리고·날아가고·돈다. 훅 쇼츠(hookshort)·뉴스 데스크에서 같이 쓴다.

박자 대본:
  "motion": [
    {"t": "폴더", "do": "folder", "id": "f", "x": 540, "y": 760, "label": "스킬 폴더"},        # 폴더가 튀어나와 뚜껑이 열림
    {"t": "SKILL.md", "do": "file", "id": "doc", "from": "f", "x": 300, "y": 1080, "label": "SKILL.md"},   # 폴더에서 문서가 날아 나와 줄이 써짐
    {"t": "스크립트", "do": "gear", "id": "g", "from": "f", "x": 780, "y": 1080, "label": "스크립트"},      # 톱니가 날아 나와 계속 돎
    {"t": "클로드", "do": "icon", "id": "ai", "icon": "🤖", "x": 540, "y": 420, "label": "클로드"},          # 동그라미 아이콘이 튀어나옴
    {"t": "꺼내", "do": "arrow", "a": "f", "b": "ai"},                                          # 두 사물 사이에 화살표가 그려짐
    {"t": "19만", "do": "count", "id": "n", "value": "19만+", "x": 540, "y": 760, "label": "GitHub 별"},   # 숫자가 0에서 올라감
    {"t": "한 줄", "do": "type", "id": "cmd", "text": "/plugin marketplace add anthropics/skills", "x": 540, "y": 760},  # 터미널에 글자가 쳐짐
    {"t": "끝", "do": "check", "on": "cmd"},                                                    # 초록 체크 도장
    {"t": "디자인", "do": "pulse", "on": "ai"},                                                 # 한 번 커졌다 돌아옴
    {"t": "...", "do": "out", "on": "f"}                                                        # 사라짐
  ]
x·y 는 사물의 가운데 (화면 좌표). t 는 그 박자에서 말하는 낱말(없으면 박자 시작), delay 로 미세 조정.
"""
from __future__ import annotations

import html as H
import re

YEL = "#FFD84D"


def _e(s) -> str:
    return H.escape(str(s))


def word_time(words: list, say: str, target: str, dur: float) -> float:
    """박자 음성 받아쓰기(words)에서 target 을 말하기 시작하는 시각(박자 안 초). 못 찾으면 글자 위치 비율."""
    norm = lambda s: re.sub(r"[^0-9a-z가-힣]", "", s.lower())
    q = norm(target)
    if q:
        for w in words or []:
            nw = norm(w["word"])
            if nw and (q in nw or (len(nw) >= 2 and nw in q and q.startswith(nw))):
                return float(w["start"])
        pos = norm(say).find(q)
        if pos >= 0:
            return dur * pos / max(len(norm(say)), 1)
    return 0.0


class Stage:
    """사물들을 모아 HTML·GSAP 로 만든다. items(앞), js 에 붙여 쓴다."""

    def __init__(self, prefix: str, w: int = 1080, h: int = 1920):
        self.p = prefix
        self.w, self.h = w, h
        self.pos: dict = {}
        self.items: list = []
        self.svg: list = []
        self.js: list = []
        self.sfx: list = []

    def _box(self, el_id, x, y, w, h, inner, z=5):
        did = f"{self.p}_{el_id}"
        self.items.append(f'<div id="{did}" style="position:absolute;left:{x - w / 2:.0f}px;top:{y - h / 2:.0f}px;width:{w}px;height:{h}px;'
                          f'z-index:{z};opacity:0">{inner}</div>')
        self.pos[el_id] = (x, y, w, h)
        return did

    def _enter(self, did, t, frm=None, x=0, y=0):
        if frm and frm in self.pos:
            fx, fy, _, _ = self.pos[frm]
            self.js.append(f'tl.fromTo("#{did}",{{opacity:0,scale:0.25,x:{fx - x:.0f},y:{fy - y:.0f}}},'
                           f'{{opacity:1,scale:1,x:0,y:0,duration:0.45,ease:"back.out(1.6)"}},{t:.3f});')
            self.sfx.append(("whoosh-short", t))
        else:
            self.js.append(f'tl.fromTo("#{did}",{{opacity:0,scale:0.4,y:40}},{{opacity:1,scale:1,y:0,duration:0.38,ease:"back.out(2.2)"}},{t:.3f});')
            self.sfx.append(("pop", t))

    def add(self, m: dict, t: float, end: float):
        do = m["do"]
        x, y = m.get("x", 540), m.get("y", 760)
        lab = m.get("label", "")
        lab_html = (f'<div style="position:absolute;left:-60px;right:-60px;bottom:-62px;text-align:center;font-family:gx,sans-x;font-size:40px;color:#fff;'
                    f'-webkit-text-stroke:2px #000;paint-order:stroke fill">{_e(lab)}</div>') if lab else ""
        if do == "folder":
            inner = (f'<div style="position:absolute;inset:0;perspective:700px">'
                     f'<div style="position:absolute;left:0;top:20px;width:124px;height:52px;background:#E9A92E;border-radius:14px 14px 0 0"></div>'
                     f'<div style="position:absolute;left:0;top:50px;right:0;bottom:0;background:#E9A92E;border-radius:0 18px 18px 18px"></div>'
                     f'<div style="position:absolute;left:22px;right:22px;top:64px;height:80px;background:#fff;border-radius:6px;opacity:.9"></div>'
                     f'<div class="lid" style="position:absolute;left:0;top:92px;right:0;bottom:0;background:#FFC94A;border-radius:12px 12px 18px 18px;'
                     f'transform-origin:50% 100%;box-shadow:0 -4px 10px rgba(0,0,0,.15)"></div></div>{lab_html}')
            did = self._box(m["id"], x, y, 360, 280, inner)
            self._enter(did, t)
            self.js.append(f'tl.to("#{did} .lid",{{rotateX:-58,duration:0.35,ease:"power2.out"}},{t + 0.45:.3f});')
        elif do == "file":
            lines = "".join(f'<div class="ln" style="height:12px;margin:14px 0 0;width:{w}%;background:#C9CED6;border-radius:6px;transform-origin:left center"></div>'
                            for w in (90, 70, 84, 55))
            inner = (f'<div style="position:absolute;inset:0;background:#fff;border-radius:14px;box-shadow:0 12px 30px rgba(0,0,0,.45);padding:22px 22px">'
                     f'<div style="font-family:gx,sans-x;font-size:38px;color:#111">{_e(m.get("title", lab or "문서"))}</div>{lines}'
                     f'<div style="position:absolute;right:0;top:0;width:44px;height:44px;background:linear-gradient(225deg,#E6E8EC 50%,transparent 50%)"></div></div>')
            did = self._box(m["id"], x, y, 290, 340, inner)
            self._enter(did, t, m.get("from"), x, y)
            self.js.append(f'tl.from("#{did} .ln",{{scaleX:0,duration:0.22,stagger:0.12,ease:"power1.out"}},{t + 0.35:.3f});')
        elif do == "gear":
            inner = (f'<div class="gr" style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:210px;'
                     f'filter:drop-shadow(0 10px 18px rgba(0,0,0,.45))">⚙️</div>{lab_html}')
            did = self._box(m["id"], x, y, 270, 270, inner)
            self._enter(did, t, m.get("from"), x, y)
            spin = max(end - t, 0.5)
            self.js.append(f'tl.to("#{did} .gr",{{rotation:{int(240 * spin)},duration:{spin:.2f},ease:"none"}},{t:.3f});')
        elif do == "icon":
            inner = (f'<div style="position:absolute;inset:0;border-radius:50%;background:{m.get("bg", YEL)};display:flex;align-items:center;'
                     f'justify-content:center;font-size:{m.get("size", 110)}px;box-shadow:0 12px 30px rgba(0,0,0,.45)">{_e(m.get("icon", "★"))}</div>{lab_html}')
            did = self._box(m["id"], x, y, m.get("d", 240), m.get("d", 240), inner)
            self._enter(did, t, m.get("from"), x, y)
        elif do == "count":
            val = str(m.get("value", ""))
            num = re.sub(r"[^\d.]", "", val)
            inner = (f'<div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;'
                     f'background:rgba(246,244,238,.97);border-radius:32px;box-shadow:0 20px 60px rgba(0,0,0,.5)">'
                     f'<div style="font-family:gr,sans;font-size:38px;color:#555">{_e(lab)}</div>'
                     f'<div id="{self.p}_{m["id"]}_n" style="font-family:gx,sans-x;font-size:190px;line-height:1.05;color:#111">{_e(val)}</div></div>')
            did = self._box(m["id"], x, y, 900, 420, inner)
            self._enter(did, t)
            if num and num.replace(".", "").isdigit():
                dec = len(num.split(".")[1]) if "." in num else 0
                i0 = val.index(num[0])
                pre, post = val[:i0], val[i0 + len(num):] if val[i0:i0 + len(num)] == num else val[i0 + 1:]
                self.js.append(f'(function(){{var o={{v:0}};tl.to(o,{{v:{num},duration:0.9,ease:"power2.out",onUpdate:function(){{'
                               f'document.getElementById("{self.p}_{m["id"]}_n").textContent="{_e(pre)}"+o.v.toFixed({dec})+"{_e(post)}";}}}},{t + 0.1:.3f});}})();')
            # 반짝이는 별 몇 개 (숫자 강조)
            for k, (dx, dy) in enumerate(((-380, -170), (390, -150), (-330, 170), (360, 180))):
                sid = f"{did}_s{k}"
                self.items.append(f'<div id="{sid}" style="position:absolute;left:{x + dx - 30}px;top:{y + dy - 30}px;font-size:60px;opacity:0;z-index:6">✨</div>')
                self.js.append(f'tl.fromTo("#{sid}",{{opacity:0,scale:0.2}},{{opacity:1,scale:1.2,duration:0.25}},{t + 0.5 + k * 0.08:.3f});'
                               f'tl.to("#{sid}",{{opacity:0,duration:0.3}},{t + 1.0 + k * 0.08:.3f});')
        elif do == "type":
            text = m.get("text", "")
            inner = (f'<div style="position:absolute;inset:0;background:#0D1117;border-radius:22px;border:2px solid #30363D;box-shadow:0 20px 60px rgba(0,0,0,.6);'
                     f'padding:70px 34px 30px">'
                     f'<div style="position:absolute;left:24px;top:22px;display:flex;gap:12px">'
                     f'<span style="width:20px;height:20px;border-radius:10px;background:#FF5F57"></span><span style="width:20px;height:20px;border-radius:10px;background:#FEBC2E"></span>'
                     f'<span style="width:20px;height:20px;border-radius:10px;background:#28C840"></span></div>'
                     f'<div style="font-family:monospace;font-size:40px;line-height:1.35;color:#7CFFB2;word-break:break-all">&gt; '
                     f'<span id="{self.p}_{m["id"]}_t"></span><span class="cur" style="background:#7CFFB2;color:#7CFFB2">_</span></div></div>')
            did = self._box(m["id"], x, y, 960, m.get("h", 300), inner)
            self._enter(did, t)
            dur = min(max(len(text) * 0.035, 0.6), 1.8)
            self.js.append(f'(function(){{var s={text!r};var o={{n:0}};tl.to(o,{{n:s.length,duration:{dur:.2f},ease:"none",onUpdate:function(){{'
                           f'document.getElementById("{self.p}_{m["id"]}_t").textContent=s.slice(0,Math.round(o.n));}}}},{t + 0.3:.3f});}})();')
            self.sfx.append(("click-soft", t + 0.3))
        elif do == "check":
            on = m.get("on")
            if on in self.pos:
                ox, oy, ow, oh = self.pos[on]
                cid = f"{self.p}_ck_{on}"
                self.items.append(f'<div id="{cid}" style="position:absolute;left:{ox + ow / 2 - 70:.0f}px;top:{oy - oh / 2 - 50:.0f}px;width:120px;height:120px;'
                                  f'border-radius:60px;background:#28C840;color:#fff;font-family:gx,sans-x;font-size:80px;display:flex;align-items:center;justify-content:center;'
                                  f'box-shadow:0 10px 24px rgba(0,0,0,.45);opacity:0;z-index:9">✓</div>')
                self.js.append(f'tl.fromTo("#{cid}",{{opacity:0,scale:2.2,rotation:-30}},{{opacity:1,scale:1,rotation:0,duration:0.3,ease:"power4.in"}},{t:.3f});')
                self.sfx.append(("pop", t + 0.28))
        elif do == "arrow":
            a, b = self.pos.get(m["a"]), self.pos.get(m["b"])
            if a and b:
                import math
                dx, dy = b[0] - a[0], b[1] - a[1]
                L = math.hypot(dx, dy) or 1
                ra, rb = min(a[2], a[3]) / 2 + 14, min(b[2], b[3]) / 2 + 22   # 사물 가장자리에서 가장자리로 (2026-11-13: 옆으로 놓인 사물 사이가 V 자로 그려짐)
                x1, y1 = a[0] + dx / L * ra, a[1] + dy / L * ra
                x2, y2 = b[0] - dx / L * rb, b[1] - dy / L * rb
                bend = min(80, L * 0.15)
                cx, cy = (x1 + x2) / 2 - dy / L * bend, (y1 + y2) / 2 + dx / L * bend
                aid = f"{self.p}_ar_{m['a']}_{m['b']}"
                self.svg.append(f'<path id="{aid}" d="M{x1:.0f},{y1:.0f} Q{cx:.0f},{cy:.0f} {x2:.0f},{y2:.0f}" fill="none" stroke="{YEL}" stroke-width="12" '
                                f'stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" marker-end="url(#{self.p}_head)" opacity="0"/>')
                self.js.append(f'tl.set("#{aid}",{{opacity:1}},{t:.3f});tl.to("#{aid}",{{strokeDashoffset:0,duration:0.4,ease:"power2.inOut"}},{t:.3f});')
                self.sfx.append(("whoosh-short", t))
        if do in ("folder", "file", "gear", "icon") and end - t > 1.2:   # 들어온 뒤 살짝 떠 있음 (정지 화면 방지)
            n = max(1, int((end - t - 0.6) / 0.9))
            self.js.append(f'tl.to("#{self.p}_{m["id"]}",{{y:-10,duration:0.45,ease:"sine.inOut",yoyo:true,repeat:{2 * n - 1}}},{t + 0.6:.3f});')
        if do == "pulse" and m.get("on") in self.pos:
            self.js.append(f'tl.fromTo("#{self.p}_{m["on"]}",{{scale:1}},{{scale:1.18,duration:0.16,yoyo:true,repeat:1,ease:"power1.inOut"}},{t:.3f});')
        elif do == "out" and m.get("on") in self.pos:
            self.js.append(f'tl.to("#{self.p}_{m["on"]}",{{opacity:0,scale:0.6,duration:0.25}},{t:.3f});')

    def finish(self, end: float, keep: bool = False) -> tuple[str, str]:
        """(HTML, JS) — 장면 끝에 모두 사라짐 (keep=True 면 남김)."""
        html = "".join(self.items)
        if self.svg:
            html += (f'<svg style="position:absolute;inset:0;width:100%;height:100%;z-index:4;pointer-events:none" viewBox="0 0 {self.w} {self.h}">'
                     f'<defs><marker id="{self.p}_head" markerWidth="6" markerHeight="6" refX="3" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="{YEL}"/></marker></defs>'
                     f'{"".join(self.svg)}</svg>')
        js = list(self.js)
        if not keep and (self.pos or self.svg):
            js.append(f'tl.to("[id^={self.p}_]",{{opacity:0,duration:0.15}},{end - 0.15:.3f});')
        return html, "\n".join(js)
