"""애니메이션 무대 (`stage`) — 호기심 채널 이야기형 v22 (2026-11-14 사용자 기각 반영, manual/04 §0-5).

> "중간중간 너무 난잡하다. 대본을 소제목처럼 글로 쓰거나 사진을 무작정 붙이지 말고, 대본을 바탕으로 애니메이션을. 의도를 명확히."

이야기 그림판(story)과 다른 점:
- 큰 종이에 쌓지 않는다. **화면 한 장(1920×1080)이 무대**이고, 박자마다 필요 없는 것은 퇴장한다.
- 그림은 '나타나기'만 하지 않고 **대본의 동사를 연기**한다: 걷기·쓰러지기·일어나 나가기·모양 바뀌기·미끄러지기·빨려 들어가기·시소 기울기.
- 글자는 한 번에 하나 (연도·숫자·이름·핵심어). 자막 문장을 다시 쓰지 않는다.
- 장면에는 `goal`, 박자에는 `why`(이 그림·움직임이 시청자에게 주는 것)가 반드시 있다 — 없으면 검사 실패.

대본 (02_script/hybrid.json):
  {"type": "stage", "goal": "이 장면이 끝나면 시청자는 ...", "bg": "paper|dark",
   "beats": [{"say": "...", "why": "...", "act": [
       {"t": "카스파로프가", "do": "in", "id": "k", "src": "photo:kasparov.jpg", "x": 560, "y": 760, "w": 360, "caption": "가리 카스파로프"},
       {"t": "체스판", "do": "in", "id": "bd", "src": "gen/chessboard.png", "x": 1180, "y": 800, "h": 300, "from": "drop"},
       {"t": "일어났", "do": "act", "on": "kg", "a": "tip"}]}]}
좌표는 화면(1920×1080) 기준. 그림 조각(gen/)·사진의 y 는 **발밑(아래 끝)**. 자막 자리(y>900)는 비운다.

do:
  in    등장  src = gen/<조각>.png | photo:<사진> | doc:<캡처> | lens:<조각> (로봇의 눈 = 동그란 렌즈)
        from = left|right|top|bottom|drop|pop|rise|fade
  out   퇴장  on = id | [id..] | "all",  to = left|right|up|down|fade
  pose  같은 인물의 다른 자세로 (on, src)          morph  모양이 계속 바뀜 (on, srcs, every)
  to    옮겨 가기 (on, x, y, dur, walk)            act    연기: tip·fall·hop·sink·rise·wobble·squash·shake·grow·shrink·pulse·lift
  fx    작은 표시: ? · ! · sweat · sparkle · smoke · lines · flash
  into  on 이 target 안으로 빨려 들어감            cover  셔터가 내려옴 (on, rect=[x0,y0,x1,y1] 비율)
  text  글자 하나 (kind = year|word|name|num)      count  숫자가 올라감 (to, fmt="{n}만 달러")
  line  선 (from, to, dash)                         dot    점 (x, y, r)
  mark  check|cross|box (on)                        seesaw / tilt  시소 (left, right 조각) · 기울기(deg)
  hl    문서 형광펜 (on, rect)                      bg     paper|dark
"""
from __future__ import annotations

import html as H
from pathlib import Path

W, H_ = 1920, 1080
INK, RED, CREAM, MARK, BLUE = "#22304D", "#C4452F", "#F4EBDD", "#F3D36B", "#2F5D8C"
SHADOW = "drop-shadow(0 14px 14px rgba(30,24,16,.22))"
COUNTED = {"in", "seesaw", "count", "text"}      # 동시에 보이는 것으로 셈 (선·점·표시는 빼고)
MOTION = {"in", "out", "pose", "morph", "to", "act", "fx", "into", "cover", "tilt", "count", "line", "seesaw", "bg", "mark", "hl"}


def _e(s) -> str:
    return H.escape(str(s))


class Stage:
    def __init__(self, D, sc: dict):
        self.D, self.sc = D, sc
        self.p = f"sg{sc['id']}"
        self.html: list = []
        self.js: list = []
        self.el: dict = {}        # id → {"kind", "x", "y", "w", "h", "poses", "n", "text"}
        self.vis: dict = {}       # id → 보이는 중 (등장 시각)
        self.events: list = []    # (t, "+"/"-", id, kind) — 붐빔 검사
        self.bg_events: list = []
        self.credits: list = []
        self.n = 0
        self.dark = sc.get("bg") == "dark"

    # ---------------------------------------------------------------- 공통
    def _id(self):
        self.n += 1
        return f"{self.p}x{self.n}"

    def sfx(self, name, t):
        self.D.sfx.append((name, t))

    def asset(self, src: str) -> str:
        import os
        import shutil
        f = Path(self.D._proj) / "04_assets" / "story" / src
        name = "story_" + src.replace("/", "_")
        dst = Path(self.D._work) / "assets" / name
        if f.exists() and not dst.exists():
            try:
                os.link(f, dst)
            except OSError:
                shutil.copy(f, dst)
        if not f.exists():
            self.D.qa.append(f"stage/missing: 04_assets/story/{src}")
        return name

    def size(self, src: str) -> tuple[int, int]:
        try:
            from PIL import Image
            return Image.open(Path(self.D._proj) / "04_assets" / "story" / src).size
        except Exception:  # noqa: BLE001
            return (1, 1)

    def show(self, t, mid, kind):
        self.vis[mid] = t
        self.events.append((t, "+", mid, kind))

    def hide(self, t, mid):
        if mid in self.vis:
            del self.vis[mid]
            self.events.append((t, "-", mid, self.el.get(mid, {}).get("kind", "")))

    def enter(self, did, t, how, dur=0.6):
        js = self.js
        if how == "left":
            js.append(f'tl.fromTo("#{did}",{{opacity:0,x:-700}},{{opacity:1,x:0,duration:{dur},ease:"power3.out"}},{t:.2f});')
        elif how == "right":
            js.append(f'tl.fromTo("#{did}",{{opacity:0,x:700}},{{opacity:1,x:0,duration:{dur},ease:"power3.out"}},{t:.2f});')
        elif how == "top":
            js.append(f'tl.fromTo("#{did}",{{opacity:0,y:-500}},{{opacity:1,y:0,duration:{dur},ease:"power3.out"}},{t:.2f});')
        elif how in ("bottom", "rise"):
            js.append(f'tl.fromTo("#{did}",{{opacity:0,y:160}},{{opacity:1,y:0,duration:{dur},ease:"power3.out"}},{t:.2f});')
        elif how == "drop":   # 떨어져 '딱' 자리 잡음 (짧게 눌렸다 펴짐)
            js.append(f'tl.fromTo("#{did}",{{opacity:0,y:-380}},{{opacity:1,y:0,duration:0.42,ease:"power2.in"}},{t:.2f});'
                      f'tl.fromTo("#{did}_a",{{scaleY:0.88,scaleX:1.08}},{{scaleY:1,scaleX:1,duration:0.4,ease:"back.out(3)"}},{t + 0.42:.2f});')
        elif how == "fade":
            js.append(f'tl.fromTo("#{did}",{{opacity:0}},{{opacity:1,duration:{dur}}},{t:.2f});')
        else:   # pop
            js.append(f'tl.fromTo("#{did}",{{opacity:0,scale:0.4}},{{opacity:1,scale:1,duration:0.45,ease:"back.out(2.2)"}},{t:.2f});')

    # ---------------------------------------------------------------- 동작
    def add(self, m: dict, t: float):
        do = m["do"]
        mid = m.get("id") or self._id()
        did = f"{self.p}_{mid}"
        js = self.js
        if do == "in":
            src = m["src"]
            x, y = m.get("x", W / 2), m.get("y", 800)
            if src.startswith("photo:") or src.startswith("doc:"):
                kind, f = src.split(":", 1)
                a = self.asset(f)
                iw, ih = self.size(f)
                w = m.get("w", 420)
                h = round(w * (m.get("ratio") or ih / max(iw, 1)))
                rot = m.get("rot", -2.2 if kind == "photo" else 1.2)
                pad = 18 if kind == "photo" else 0
                cap = (f'<div style="position:absolute;left:0;right:0;bottom:-74px;text-align:center;font-family:pen;font-size:40px;color:{INK}">{_e(m["caption"])}</div>'
                       if m.get("caption") else "")
                top = y - h - pad * 2 - (70 if m.get("caption") else 0)
                self.html.append(f'<div id="{did}" style="position:absolute;left:{x - w / 2 - pad:.0f}px;top:{top:.0f}px;width:{w + pad * 2}px;opacity:0">'
                                 f'<div id="{did}_a" style="transform:rotate({rot}deg);background:{"#FBF8F1" if kind == "photo" else "#fff"};padding:{pad}px {pad}px {pad + (70 if m.get("caption") else 0)}px;'
                                 f'box-shadow:0 18px 34px rgba(30,24,16,.28);position:relative">'
                                 f'<div id="{did}_hl" style="position:relative;width:{w}px;height:{h}px;overflow:hidden">'
                                 f'<img src="assets/{a}" style="width:100%;height:100%;object-fit:cover;object-position:{m.get("focus", "50% 30%")};'
                                 f'filter:{"sepia(.16) saturate(.88) contrast(1.06)" if kind == "photo" else "none"}"></div>{cap}</div></div>')
                self.el[mid] = {"kind": kind, "x": x, "y": y - h / 2, "w": w, "h": h}
                if m.get("credit"):
                    self.credits.append(m["credit"])
            elif src.startswith("lens:"):   # 로봇의 눈: 동그란 렌즈 안의 그림 (조준선)
                f = src[5:]
                a = self.asset(f)
                r = m.get("r", 260)
                self.html.append(f'<div id="{did}" style="position:absolute;left:{x - r}px;top:{y - r}px;width:{2 * r}px;height:{2 * r}px;opacity:0">'
                                 f'<div id="{did}_a" style="position:absolute;inset:0;border-radius:50%;background:#FBF8F1;overflow:hidden;'
                                 f'box-shadow:0 0 0 14px {INK},0 0 0 20px rgba(34,48,77,.25),0 20px 40px rgba(0,0,0,.25)">'
                                 f'<div id="{did}_mv" style="position:absolute;inset:12%">'
                                 f'<img id="{did}_p0" src="assets/{a}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:contain"></div>'
                                 f'<div style="position:absolute;left:50%;top:6%;bottom:6%;border-left:3px solid rgba(196,69,47,.55)"></div>'
                                 f'<div style="position:absolute;top:50%;left:6%;right:6%;border-top:3px solid rgba(196,69,47,.55)"></div></div></div>')
                self.el[mid] = {"kind": "lens", "x": x, "y": y, "w": 2 * r, "h": 2 * r, "n": 1}
            else:   # 그림 조각 (발밑 기준)
                a = self.asset(src)
                iw, ih = self.size(src)
                h = m.get("h", 420)
                w = round(h * iw / max(ih, 1))
                flip = "scaleX(-1)" if m.get("flip") else "none"
                self.html.append(f'<div id="{did}" style="position:absolute;left:{x - w / 2:.0f}px;top:{y - h:.0f}px;width:{w}px;height:{h}px;opacity:0">'
                                 f'<div id="{did}_a" style="position:absolute;inset:0;transform-origin:50% 100%;filter:{SHADOW}">'
                                 f'<div id="{did}_mv" style="position:absolute;inset:0">'
                                 f'<img id="{did}_p0" src="assets/{a}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:contain;transform:{flip}">'
                                 f'</div></div></div>')
                self.el[mid] = {"kind": "cut", "x": x, "y": y - h / 2, "w": w, "h": h, "n": 1, "flip": flip}
            self.enter(did, t, m.get("from", "pop"))
            self.sfx("whoosh-short" if m.get("from") in ("left", "right", "top") else "pop", t)
            self.show(t, mid, "in")
        elif do == "out":
            ons = list(self.vis) if m.get("on") == "all" else ([m["on"]] if isinstance(m.get("on"), str) else m.get("on", []))
            ons = [o for o in ons if o not in m.get("keep", []) and o in self.el]   # 이 장면에 없는 것은 건너뜀 (장면을 나눈 경우)
            to = m.get("to", "fade")
            mv = {"left": "x:-900,", "right": "x:900,", "up": "y:-600,", "down": "y:400,"}.get(to, "")
            for o in ons:
                js.append(f'tl.to("#{self.p}_{o}",{{{mv}opacity:0,duration:{0.5 if mv else 0.35},ease:"power2.in"}},{t:.2f});')
                for mk in self.el.get(o, {}).get("marks", []):
                    js.append(f'tl.to("#{mk}",{{opacity:0,duration:0.3}},{t:.2f});')
                self.hide(t, o)
            if ons and mv:
                self.sfx("whoosh-short", t)
        elif do == "pose" and m.get("on") in self.el:
            on = m["on"]; e = self.el[on]; base = f"{self.p}_{on}"
            k = e["n"]; e["n"] += 1
            a = self.asset(m["src"])
            self._inject(on, f'<img id="{base}_p{k}" src="assets/{a}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:contain;opacity:0;transform:{e.get("flip", "none")}">')
            js.append(f'tl.to("#{base}_a",{{scaleY:0.95,scaleX:1.03,duration:0.1}},{t:.2f});'
                      f'tl.set("#{base}_mv img",{{opacity:0}},{t + 0.1:.2f});tl.set("#{base}_p{k}",{{opacity:1}},{t + 0.1:.2f});'
                      f'tl.to("#{base}_a",{{scaleY:1,scaleX:1,duration:0.35,ease:"back.out(2.5)"}},{t + 0.1:.2f});')
            self.sfx("pop", t)
        elif do == "morph" and m.get("on") in self.el:   # 볼 때마다 모양이 바뀜 (같은 물건)
            on = m["on"]; e = self.el[on]; base = f"{self.p}_{on}"
            ks = []
            for s in m["srcs"]:
                k = e["n"]; e["n"] += 1
                a = self.asset(s)
                self._inject(on, f'<img id="{base}_p{k}" src="assets/{a}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:contain;opacity:0">')
                ks.append(k)
            every = m.get("every", 0.6)
            allk = list(range(e["n"]))
            seq = [ks[i % len(ks)] for i in range(m.get("n", len(ks)))]
            for i, k in enumerate(seq):
                tt = t + i * every
                js.append(f'tl.set("{",".join(f"#{base}_p{j}" for j in allk)}",{{opacity:0}},{tt:.2f});tl.set("#{base}_p{k}",{{opacity:1}},{tt:.2f});'
                          f'tl.fromTo("#{base}_mv",{{scale:0.94,rotation:{(-4, 3, -2, 5)[i % 4]}}},{{scale:1,rotation:0,duration:0.3,ease:"back.out(2)"}},{tt:.2f});')
                self.sfx("click-soft", tt)
        elif do == "to" and m.get("on") in self.el:
            on = m["on"]; e = self.el[on]; base = f"{self.p}_{on}"
            dx = m.get("x", e["x"]) - e["x"]
            dy = m.get("y", e["y"] + e["h"] / 2) - (e["y"] + e["h"] / 2) if "y" in m else 0
            dur = m.get("dur", 1.2)
            sc_ = f",scale:{m['scale']}" if m.get("scale") else ""
            js.append(f'tl.to("#{base}",{{x:"+={dx:.0f}",y:"+={dy:.0f}"{sc_},duration:{dur},ease:"{"none" if m.get("walk") else "power2.inOut"}"}},{t:.2f});')
            if m.get("walk"):
                n = max(2, int(dur / 0.4))
                for k in range(n):
                    js.append(f'tl.to("#{base}_mv",{{y:-18,rotation:{3 if k % 2 else -3},duration:{dur / n / 2:.2f},ease:"sine.out",yoyo:true,repeat:1}},{t + k * dur / n:.2f});')
                    self.sfx("click-soft", t + k * dur / n + dur / n / 2)
            e["x"] += dx
            e["y"] += dy
        elif do == "act" and m.get("on") in self.el:
            self._act(m, t)
        elif do == "fx" and (m.get("on") in self.el or m.get("kind") == "flash"):
            self._fx(m, t)
        elif do == "into" and m.get("on") in self.el and m.get("target") in self.el:   # 빨려 들어감
            e, g = self.el[m["on"]], self.el[m["target"]]
            dx, dy = g["x"] - e["x"], g["y"] - e["y"]
            js.append(f'tl.to("#{self.p}_{m["on"]}",{{x:"+={dx:.0f}",y:"+={dy:.0f}",scale:0.15,rotation:200,opacity:0,duration:0.9,ease:"power2.in"}},{t:.2f});'
                      f'tl.fromTo("#{self.p}_{m["target"]}_a",{{scale:1}},{{scale:1.08,duration:0.18,yoyo:true,repeat:1,ease:"sine.inOut"}},{t + 0.85:.2f});')
            self.sfx("whoosh", t)
            self.sfx("pop", t + 0.9)
            self.hide(t + 0.9, m["on"])
        elif do == "cover" and m.get("on") in self.el:   # 셔터가 내려옴 (문을 닫다) — 그림 안에 넣어 함께 움직임
            x0, y0, x1, y1 = m.get("rect", [0.2, 0.55, 0.8, 0.98])
            self._inject(m["on"], f'<div id="{did}" style="position:absolute;left:{x0 * 100:.1f}%;top:{y0 * 100:.1f}%;width:{(x1 - x0) * 100:.1f}%;height:{(y1 - y0) * 100:.1f}%;'
                                  f'transform-origin:50% 0%;background:repeating-linear-gradient(180deg,#8B95A6 0 16px,#6F7A8C 16px 20px);border:4px solid {INK};border-radius:4px"></div>')
            js.append(f'tl.set("#{did}",{{scaleY:0}},0);tl.to("#{did}",{{scaleY:1,duration:{m.get("dur", 1.1)},ease:"bounce.out"}},{t:.2f});')
            self.sfx("impact-bass-1", t + 0.8)
        elif do in ("text", "count"):
            kind = m.get("kind", "num" if do == "count" else "word")
            x, y = m.get("x", W / 2), m.get("y", 170)
            fs = m.get("fs", {"year": 76, "word": 92, "name": 80, "num": 130}.get(kind, 90))
            col = m.get("color") or (RED if kind in ("word", "num") else (CREAM if self.dark else INK))
            font = "pen" if kind in ("word", "name") else "serif-x"
            txt = m.get("text", "") if do == "text" else m.get("fmt", "{n}").format(n=0)
            self.html.append(f'<div id="{did}" style="position:absolute;left:{x - 900}px;top:{y - fs * 0.6:.0f}px;width:1800px;text-align:center;opacity:0">'
                             f'<span id="{did}_t" style="font-family:{font};font-size:{fs}px;color:{col};white-space:nowrap;line-height:1.2">{_e(txt)}</span>'
                             + (f'<div id="{did}_u" style="margin:4px auto 0;width:{min(900, len(txt) * fs * 0.62):.0f}px;height:6px;background:{RED};transform-origin:0 50%"></div>'
                                if kind == "year" else "") + '</div>')
            js.append(f'tl.fromTo("#{did}",{{opacity:0,y:18}},{{opacity:1,y:0,duration:0.4,ease:"power2.out"}},{t:.2f});')
            if kind == "year":
                js.append(f'tl.set("#{did}_u",{{scaleX:0}},0);')
                js.append(f'tl.to("#{did}_u",{{scaleX:1,duration:0.5,ease:"power2.inOut"}},{t + 0.25:.2f});')
                self.sfx("pencil", t + 0.25)
            if do == "count":
                to = m["to"]
                fmt = m.get("fmt", "{n}")
                js.append(f'(function(){{var o={{v:0}};tl.to(o,{{v:{to},duration:{m.get("dur", 1.4)},ease:"power2.out",onUpdate:function(){{'
                          f'document.getElementById("{did}_t").textContent={fmt!r}.replace("{{n}}",Math.round(o.v).toLocaleString("ko-KR"));}}}},{t:.2f});}})();')
                self.sfx("riser", t)
            self.el[mid] = {"kind": "text", "x": x, "y": y, "w": len(txt) * fs * 0.7, "h": fs * 1.3}
            self.show(t, mid, "text")
        elif do == "line":
            (x0, y0), (x1, y1) = m["from"], m["to"]
            col = m.get("color", CREAM if self.dark else INK)
            dash = 'stroke-dasharray="2 28"' if m.get("dash") else ""
            L = ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5
            self.html.append(f'<svg id="{did}" style="position:absolute;left:0;top:0;overflow:visible" width="{W}" height="{H_}">'
                             f'<line id="{did}_l" x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}" stroke="{col}" stroke-width="{m.get("sw", 10)}" stroke-linecap="round" {dash}/>'
                             f'</svg>')
            js.append(f'tl.fromTo("#{did}",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:{m.get("dur", 1.4)},ease:"power1.inOut"}},{t:.2f});')
            _ = L
            self.el[mid] = {"kind": "line", "x": (x0 + x1) / 2, "y": (y0 + y1) / 2, "w": abs(x1 - x0), "h": abs(y1 - y0) + 10}
            self.sfx("pencil", t)
        elif do == "dot":
            x, y, r = m["x"], m["y"], m.get("r", 16)
            self.html.append(f'<div id="{did}" style="position:absolute;left:{x - r}px;top:{y - r}px;width:{2 * r}px;height:{2 * r}px;border-radius:50%;background:{RED};opacity:0"></div>'
                             f'<div id="{did}_ring" style="position:absolute;left:{x - r * 3}px;top:{y - r * 3}px;width:{6 * r}px;height:{6 * r}px;border-radius:50%;border:5px solid {RED};opacity:0"></div>')
            js.append(f'tl.fromTo("#{did}",{{opacity:0,scale:0}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(3)"}},{t:.2f});'
                      f'tl.fromTo("#{did}_ring",{{opacity:0.9,scale:0.3}},{{opacity:0,scale:1.3,duration:1.0,repeat:2,ease:"power1.out",immediateRender:false}},{t + 0.2:.2f});')
            self.el[mid] = {"kind": "dot", "x": x, "y": y, "w": 2 * r, "h": 2 * r}
            self.sfx("pop", t)
        elif do == "mark" and m.get("on") in self.el:
            e = self.el[m["on"]]
            kind = m.get("kind", "check")
            if kind == "box":   # 테두리 (정해진 세계)
                pad = m.get("pad", 30)
                L, T, ww, hh = e["x"] - e["w"] / 2 - pad, e["y"] - e["h"] / 2 - pad, e["w"] + 2 * pad, e["h"] + 2 * pad
                d = f"M{L},{T} H{L + ww} V{T + hh} H{L} Z"
                col = m.get("color", BLUE)
            elif kind == "cross":
                s = min(e["w"], e["h"]) * 0.45
                d = f"M{e['x'] - s},{e['y'] - s} L{e['x'] + s},{e['y'] + s} M{e['x'] + s},{e['y'] - s} L{e['x'] - s},{e['y'] + s}"
                col = RED
            else:
                cx, cy = e["x"] + e["w"] * 0.32, e["y"] - e["h"] * 0.3
                d = f"M{cx - 50},{cy} L{cx - 12},{cy + 40} L{cx + 62},{cy - 52}"
                col = "#2E7D4F"
            self.html.append(f'<svg style="position:absolute;left:0;top:0;overflow:visible" width="{W}" height="{H_}">'
                             f'<path id="{did}" d="{d}" fill="none" stroke="{col}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" '
                             f'pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" opacity="0"/></svg>')
            js.append(f'tl.set("#{did}",{{opacity:1}},{t:.2f});tl.to("#{did}",{{strokeDashoffset:0,duration:{0.8 if kind == "box" else 0.45},ease:"power2.out"}},{t:.2f});')
            self.sfx("pencil" if kind == "box" else "pop", t)
            self.el.setdefault(m["on"], e).setdefault("marks", []).append(did)
        elif do == "hl" and m.get("on") in self.el:
            x0, y0, x1, y1 = m["rect"]
            self._inject_hl(m["on"], f'<div id="{did}" style="position:absolute;left:{x0 * 100:.1f}%;top:{y0 * 100:.1f}%;width:{(x1 - x0) * 100:.1f}%;height:{(y1 - y0) * 100:.1f}%;'
                                     f'background:{MARK};mix-blend-mode:multiply;opacity:.75;transform-origin:0 50%"></div>')
            js.append(f'tl.set("#{did}",{{scaleX:0}},0);tl.to("#{did}",{{scaleX:1,duration:0.5,ease:"power1.inOut"}},{t:.2f});')
            self.sfx("pencil", t)
        elif do == "seesaw":   # 은유: 시소 (어느 쪽이 '무거운(어려운)'지)
            x, y, w = m.get("x", W / 2), m.get("y", 760), m.get("w", 1100)
            la, ra = self.asset(m["left"]), self.asset(m["right"])
            lh, rh = m.get("lh", 300), m.get("rh", 300)
            liw, lih = self.size(m["left"]); riw, rih = self.size(m["right"])
            lw, rw = round(lh * liw / max(lih, 1)), round(rh * riw / max(rih, 1))
            self.html.append(
                f'<div id="{did}" style="position:absolute;left:0;top:0;width:{W}px;height:{H_}px;opacity:0;pointer-events:none">'
                f'<svg style="position:absolute;left:0;top:0;overflow:visible" width="{W}" height="{H_}"><path d="M{x - 70},{y + 130} L{x},{y + 4} L{x + 70},{y + 130} Z" fill="{INK}"/></svg>'
                f'<div id="{did}_bar" style="position:absolute;left:{x - w / 2}px;top:{y - 14}px;width:{w}px;height:28px;transform-origin:50% 50%">'
                f'<div style="position:absolute;inset:0;background:#B5824E;border:5px solid {INK};border-radius:14px"></div>'
                f'<img id="{did}_L" src="assets/{la}" style="position:absolute;left:{40}px;bottom:24px;width:{lw}px;height:{lh}px;object-fit:contain;filter:{SHADOW}">'
                f'<img id="{did}_R" src="assets/{ra}" style="position:absolute;right:{40}px;bottom:24px;width:{rw}px;height:{rh}px;object-fit:contain;filter:{SHADOW}">'
                f'</div></div>')
            js.append(f'tl.fromTo("#{did}",{{opacity:0,y:60}},{{opacity:1,y:0,duration:0.6,ease:"power3.out"}},{t:.2f});')
            if m.get("deg"):
                js.append(f'tl.set("#{did}_bar",{{rotation:{m["deg"]}}},{t:.2f});')
            self.el[mid] = {"kind": "seesaw", "x": x, "y": y - 150, "w": w, "h": 400}
            self.show(t, mid, "seesaw")
            self.sfx("whoosh-short", t)
        elif do == "tilt" and m.get("on") in self.el:
            js.append(f'tl.to("#{self.p}_{m["on"]}_bar",{{rotation:{m.get("deg", 12)},duration:{m.get("dur", 1.0)},ease:"elastic.out(1,0.45)"}},{t:.2f});')
            self.sfx("impact-bass-1", t + 0.15)
        elif do == "bg":
            self.bg_events.append((t, m.get("mode", "paper")))

    def _inject(self, on, html):
        key = f'<div id="{self.p}_{on}_mv" style="position:absolute;inset:0">'
        key2 = f'<div id="{self.p}_{on}_mv" style="position:absolute;inset:12%">'
        for i, h in enumerate(self.html):
            for k in (key, key2):
                if k in h:
                    self.html[i] = h.replace(k, k + html, 1)
                    return

    def _inject_hl(self, on, html):
        key = f'<div id="{self.p}_{on}_hl" style="position:relative;'
        for i, h in enumerate(self.html):
            if key in h:
                j = h.index(key)
                j = h.index(">", j) + 1
                self.html[i] = h[:j] + h[j:].replace("</div>", html + "</div>", 1)
                return

    def _act(self, m, t):
        on = m["on"]; base = f"{self.p}_{on}"; a = m["a"]; js = self.js
        e = self.el[on]
        if a == "tip":       # 쓰러짐 (기권한 왕)
            js.append(f'tl.to("#{base}_a",{{rotation:{m.get("deg", 82)},duration:0.7,ease:"bounce.out"}},{t:.2f});')
            self.sfx("impact-bass-1", t + 0.45)
        elif a == "fall":    # 넘어짐 (로봇이 걷다가)
            js.append(f'tl.to("#{base}_a",{{rotation:-12,duration:0.18,ease:"sine.out"}},{t:.2f});'
                      f'tl.to("#{base}_a",{{rotation:{m.get("deg", 78)},y:20,duration:0.55,ease:"bounce.out"}},{t + 0.18:.2f});')
            self.sfx("impact-bass-1", t + 0.5)
        elif a == "hop":     # 신나게 통통
            js.append(f'tl.to("#{base}_mv",{{y:-50,duration:0.18,yoyo:true,repeat:{m.get("n", 2) * 2 - 1},ease:"sine.out"}},{t:.2f});')
            self.sfx("pop", t)
        elif a == "sink":    # 주저앉음 (실패)
            js.append(f'tl.to("#{base}_a",{{scaleY:0.82,scaleX:1.06,rotation:-5,duration:0.6,ease:"power2.in"}},{t:.2f});')
            self.sfx("impact-bass-1", t + 0.5)
        elif a == "rise":    # 자리에서 일어나 위로 빠짐
            js.append(f'tl.to("#{base}",{{y:-700,opacity:0,duration:0.9,ease:"power2.in"}},{t:.2f});')
            self.sfx("whoosh", t)
            self.hide(t + 0.9, on)
        elif a == "lift":    # 휙 들어 올림
            js.append(f'tl.to("#{base}_mv",{{y:-90,duration:0.3,ease:"power3.out"}},{t:.2f});tl.to("#{base}_mv",{{y:-70,duration:0.4,ease:"sine.inOut"}},{t + 0.3:.2f});')
            self.sfx("whoosh-short", t)
        elif a == "wobble":  # 흐물흐물·손 흔들기
            js.append(f'tl.to("#{base}_a",{{rotation:6,duration:0.22,yoyo:true,repeat:{m.get("n", 5)},ease:"sine.inOut"}},{t:.2f});'
                      f'tl.to("#{base}_a",{{rotation:0,duration:0.2}},{t + 0.22 * (m.get("n", 5) + 1):.2f});')
        elif a == "squash":
            js.append(f'tl.to("#{base}_a",{{scaleY:0.85,scaleX:1.1,duration:0.12,yoyo:true,repeat:1,ease:"sine.inOut"}},{t:.2f});')
            self.sfx("pop", t)
        elif a == "shake":
            js.append(f'tl.to("#{base}_a",{{x:10,duration:0.06,yoyo:true,repeat:7,ease:"sine.inOut"}},{t:.2f});tl.to("#{base}_a",{{x:0,duration:0.05}},{t + 0.5:.2f});')
            self.sfx("click-soft", t)
        elif a in ("grow", "shrink"):
            js.append(f'tl.to("#{base}_a",{{scale:{m.get("scale", 2.2 if a == "grow" else 1)},duration:0.7,ease:"back.out(1.6)"}},{t:.2f});')
            self.sfx("whoosh-short", t)
        elif a == "pulse":
            js.append(f'tl.to("#{base}_a",{{scale:1.06,duration:0.2,yoyo:true,repeat:1,ease:"sine.inOut"}},{t:.2f});')
            self.sfx("pop", t)
        _ = e

    def _fx(self, m, t):
        kind = m["kind"]; js = self.js
        did = self._id()
        if kind == "flash":   # 사진기 플래시 (신문 기자들)
            self.html.append(f'<div id="{did}" style="position:absolute;inset:0;background:#fff;opacity:0;pointer-events:none"></div>')
            for k in range(m.get("n", 3)):
                js.append(f'tl.set("#{did}",{{opacity:0.75}},{t + k * 0.38:.2f});tl.to("#{did}",{{opacity:0,duration:0.22,ease:"power2.out"}},{t + k * 0.38 + 0.02:.2f});')
                self.sfx("click-soft", t + k * 0.38)
            return
        e = self.el[m["on"]]
        x, y = e["x"] + e["w"] * m.get("dx", 0.38), e["y"] - e["h"] * m.get("dy", 0.42)
        if kind in ("?", "!"):
            self.html.append(f'<div id="{did}" style="position:absolute;left:{x - 60:.0f}px;top:{y - 90:.0f}px;width:120px;text-align:center;font-family:serif-x;'
                             f'font-size:{m.get("fs", 150)}px;line-height:1;color:{RED};opacity:0">{_e(kind)}</div>')
            js.append(f'tl.fromTo("#{did}",{{opacity:0,scale:0.2,rotation:-25}},{{opacity:1,scale:1,rotation:8,duration:0.45,ease:"back.out(3)"}},{t:.2f});')
            if m.get("hold", 2.2):
                js.append(f'tl.to("#{did}",{{opacity:0,duration:0.3}},{t + m.get("hold", 2.2):.2f});')
            self.sfx("pop", t)
        elif kind == "sweat":
            self.html.append(f'<svg id="{did}" style="position:absolute;left:{x - 30:.0f}px;top:{y - 40:.0f}px;overflow:visible;opacity:0" width="60" height="80">'
                             f'<path d="M30 0 C30 0 4 34 4 52 A26 26 0 0 0 56 52 C56 34 30 0 30 0Z" fill="#7FB3E0" stroke="{INK}" stroke-width="4"/></svg>')
            js.append(f'tl.fromTo("#{did}",{{opacity:0,y:-10}},{{opacity:1,y:0,duration:0.25}},{t:.2f});tl.to("#{did}",{{y:60,opacity:0,duration:0.9,ease:"power1.in"}},{t + 0.6:.2f});')
        elif kind == "sparkle":
            stars = "".join(f'<path d="M{sx} {sy - 26} L{sx + 7} {sy - 7} L{sx + 26} {sy} L{sx + 7} {sy + 7} L{sx} {sy + 26} L{sx - 7} {sy + 7} L{sx - 26} {sy} L{sx - 7} {sy - 7}Z" fill="{MARK}" stroke="{INK}" stroke-width="3"/>'
                            for sx, sy in ((40, 40), (150, 0), (110, 110)))
            self.html.append(f'<svg id="{did}" style="position:absolute;left:{x - 90:.0f}px;top:{y - 60:.0f}px;overflow:visible;opacity:0" width="200" height="160">{stars}</svg>')
            js.append(f'tl.fromTo("#{did}",{{opacity:0,scale:0.3}},{{opacity:1,scale:1,duration:0.4,ease:"back.out(3)"}},{t:.2f});tl.to("#{did}",{{opacity:0,duration:0.4}},{t + 1.6:.2f});')
            pass   # 반짝 효과음 없음 (2026-11-14 사용자: "반짝 하며 나오는 효과음은 빼 주세요")
        elif kind == "smoke":
            puffs = "".join(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#B9B4AA" stroke="{INK}" stroke-width="3"/>' for cx, cy, r in ((40, 120, 30), (80, 70, 40), (50, 20, 26)))
            self.html.append(f'<svg id="{did}" style="position:absolute;left:{x - 60:.0f}px;top:{y - 140:.0f}px;overflow:visible;opacity:0" width="140" height="160">{puffs}</svg>')
            js.append(f'tl.fromTo("#{did}",{{opacity:0,y:30,scale:0.5}},{{opacity:0.95,y:-30,scale:1.1,duration:1.4,ease:"power1.out"}},{t:.2f});tl.to("#{did}",{{opacity:0,y:-80,duration:0.8}},{t + 1.5:.2f});')
            self.sfx("whoosh-short", t)
        elif kind == "lines":   # 충격선
            ls = "".join(f'<path d="M{a} {b} L{c} {d}" stroke="{RED}" stroke-width="9" stroke-linecap="round"/>' for a, b, c, d in ((10, 70, 50, 60), (30, 20, 62, 42), (80, 0, 88, 34)))
            self.html.append(f'<svg id="{did}" style="position:absolute;left:{x - 40:.0f}px;top:{y - 40:.0f}px;overflow:visible;opacity:0" width="120" height="100">{ls}</svg>')
            js.append(f'tl.fromTo("#{did}",{{opacity:0,scale:0.4}},{{opacity:1,scale:1,duration:0.25,ease:"back.out(3)"}},{t:.2f});tl.to("#{did}",{{opacity:0,duration:0.3}},{t + 1.0:.2f});')

    # ---------------------------------------------------------------- 마무리
    def finish(self, dur: float):
        D = self.D
        modes = [(0.0, "dark" if self.dark else "paper")] + self.bg_events
        for k, (t, mode) in enumerate(modes):
            if mode != "dark":
                continue
            bid = f"{self.p}bg{k}"
            D.items.append(f'<div id="{bid}" style="position:absolute;inset:0;opacity:0"><div style="position:absolute;inset:0;background:#2C2E34"></div>'
                           f'<img src="assets/{D.bg_name}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;mix-blend-mode:overlay;opacity:.55;filter:grayscale(1) contrast(1.9)">'
                           f'<div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 40%,rgba(255,255,255,.06) 0%,rgba(0,0,0,.35) 100%)"></div></div>')
            D.js.append(f'tl.to("#{bid}",{{opacity:1,duration:{0.01 if t < 0.1 else 0.8}}},{max(t - 0.2, 0):.2f});')
            nxt = [tt for tt, md in modes[k + 1:] if md != "dark"]
            if nxt:
                D.js.append(f'tl.to("#{bid}",{{opacity:0,duration:0.9}},{max(nxt[0] - 0.2, 0):.2f});')
        D.items.append(f'<div id="{self.p}st" data-layout-allow-overflow style="position:absolute;left:0;top:0;width:{W}px;height:{H_}px;overflow:hidden">'
                       + "".join(self.html) + '</div>')
        D.js.extend(self.js)
        # 머무는 동안 아주 천천히 다가감 (정지 화면 방지)
        D.js.append(f'tl.fromTo("#{self.p}st",{{scale:1}},{{scale:1.025,duration:{dur:.2f},ease:"none",transformOrigin:"50% 45%"}},0);')
        fid = f"{self.p}fade"
        D.items.append(f'<div id="{fid}" style="position:absolute;inset:0;background:#000;opacity:1;pointer-events:none"></div>')
        D.js.append(f'tl.to("#{fid}",{{opacity:0,duration:0.45,ease:"power1.out"}},0.05);')
        if self.credits:
            D.label(" · ".join(dict.fromkeys(self.credits))[:150])

    def qa(self, beats: list):
        q = self.D.qa
        if not self.sc.get("goal"):
            q.append("stage/no_goal: 장면 goal(이 장면이 끝나면 시청자는…) 없음 — manual/04 §0-5")
        nowhy = [k + 1 for k, b in enumerate(beats) if not b.get("why")]
        if nowhy:
            q.append(f"stage/no_why: 박자 {nowhy} 에 why(이 그림·움직임의 의도) 없음")
        static = [k + 1 for k, b in enumerate(beats) if not any(a["do"] in MOTION for a in b.get("act", []))]
        if beats and len(static) / len(beats) > 0.3:
            q.append(f"stage/static: 움직임 없는 박자 {static} ({len(static)}/{len(beats)})")
        vis, worst, wt = {}, 0, 0.0
        txt_worst = 0
        for t, sgn, mid, kind in sorted(self.events, key=lambda e: (e[0], e[1] == "+")):
            if sgn == "+":
                vis[mid] = kind
            else:
                vis.pop(mid, None)
            n = sum(1 for k in vis.values() if k in ("in", "seesaw"))
            nt = sum(1 for k in vis.values() if k == "text")
            if n + nt > worst:
                worst, wt = n + nt, t
            txt_worst = max(txt_worst, nt)
        if worst > 4:
            q.append(f"stage/crowded: {wt:.1f}초에 {worst}개가 동시에 보임 (≤4) — 다음 박자에 필요 없는 것은 out")
        if txt_worst > 1:
            q.append(f"stage/text: 글자가 {txt_worst}개 동시에 — 하나만")


def s_stage(D, sc: dict, bt: list, dur: float):
    from . import align
    from .motion2 import word_time
    D._proj = sc["_project_dir"]
    S = Stage(D, sc)
    for k, (b, (t0, d)) in enumerate(zip(sc["beats"], bt)):
        wav = Path(sc["_project_dir"]) / "03_voice" / f"hb_{sc['id']:03d}_{k}.wav"
        try:
            ws = align.transcribe(wav, "ko")
        except Exception:  # noqa: BLE001
            ws = []
        for m in b.get("act", []):
            tt = t0 + (word_time(ws, b["say"], m["t"], d) if m.get("t") else 0.05) + m.get("delay", 0.0)
            S.add(m, max(tt, 0.05))
    S.finish(dur)
    S.qa(sc["beats"])
    D.chapter_tag(sc.get("_chnum", ""), sc.get("_chtitle", ""), dark=S.dark)


def register():
    from . import hybrid
    hybrid.RENDER["stage"] = s_stage
