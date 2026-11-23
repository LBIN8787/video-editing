"""칸 만화 페이지 — 실험 사례를 '실험 순서 = 칸 순서'로 (docs/47, Sprouts 의 구조만 참고).

흰 종이 위에 칸 테두리가 말에 맞춰 그려지고, 칸 안에 합격 화풍 원화(배경 판을 잘라 쓴 것 + 인물·소품 조각)가 채워진다.
그림은 모두 원화. 코드는 칸 테두리·이름표·움직임만.
"""
from __future__ import annotations

import html as H
from pathlib import Path

from PIL import Image


def paper(path: Path) -> Path:
    """종이 바탕 판(아주 옅은 결) — 한 번 만들어 둔다."""
    if not path.exists():
        import numpy as np
        rng = np.random.default_rng(7)
        base = np.ones((1080, 1920, 3)) * np.array([250, 247, 240])
        noise = rng.normal(0, 3.2, (1080, 1920, 1))
        Image.fromarray((base + noise).clip(0, 255).astype("uint8")).save(path)
    return path


class Page:
    def __init__(self, film, sid: str):
        self.f, self.id = film, sid
        paper(film.art / "paper.png")
        self.s = film.set(sid, "paper.png", focus=(960, 540, 1.0))
        self.panels = {}

    def _img(self, name):
        p = self.f.art / name
        return p.as_uri(), Image.open(p).size

    def panel(self, pid, x, y, w, h, plate=None, crop=(0.5, 0.5, 1.0), actors=(), props=(), survey=None, caption=""):
        inner = []
        if plate:
            uri, (pw, ph) = self._img(plate)
            s0 = max(w / pw, h / ph) * crop[2]
            iw, ih = pw * s0, ph * s0
            left = min(0, max(w - iw, w / 2 - crop[0] * iw))
            top = min(0, max(h - ih, h / 2 - crop[1] * ih))
            inner.append(f'<img src="{uri}" style="position:absolute;left:{left:.0f}px;top:{top:.0f}px;width:{iw:.0f}px;height:{ih:.0f}px">')
        for name, ax, ay, ah in actors:
            uri, (aw, ahh) = self._img(f"{name}.png")
            k = ah / ahh
            inner.append(f'<img class="pa" src="{uri}" style="position:absolute;left:{ax - aw*k/2:.0f}px;top:{ay - ah:.0f}px;width:{aw*k:.0f}px;height:{ah:.0f}px">')
        for name, px, py, pwid in props:
            uri, (qw, qh) = self._img(f"{name}.png")
            inner.append(f'<img class="pp" src="{uri}" style="position:absolute;left:{px - pwid/2:.0f}px;top:{py - qh*pwid/qw/2:.0f}px;width:{pwid:.0f}px;opacity:0">')
        if survey:
            uri, (qw, qh) = self._img("survey.png")
            sw = h * 0.95 * qw / qh
            inner.append(f'<img src="{uri}" style="position:absolute;left:{(w - sw)/2:.0f}px;top:{h*0.03:.0f}px;height:{h*0.95:.0f}px">')
            for i, line in enumerate(survey):   # 설문지 그림의 체크박스 줄에 맞춤 (줄 위치는 그림 비율)
                sh = h * 0.95
                fs = min(sw * 0.62 / max(1, len(line)), sh * 0.06)
                inner.append(f'<div class="sl" id="{pid}_l{i}" style="position:absolute;left:{(w - sw)/2 + sw*0.27:.0f}px;'
                             f'top:{h*0.03 + sh*(0.214 + i*0.107) - fs*1.05:.0f}px;font-family:Pen;font-size:{fs:.0f}px;color:#24304a;white-space:nowrap">'
                             + "".join(f'<span class="ch" style="opacity:0;display:inline-block">{H.escape(c) if c != " " else "&nbsp;"}</span>' for c in line) + "</div>")
        cap = (f'<div style="position:absolute;left:14px;top:12px;padding:4px 12px;background:#fffdf7;border:3px solid #2b2118;border-radius:6px;'
               f'font-family:Goth;font-size:26px;color:#2b2118;z-index:3">{H.escape(caption)}</div>') if caption else ""
        self.s.raw(f'<div class="cp" id="{pid}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;opacity:0">'
                   f'<div class="cpi" style="position:absolute;inset:0;overflow:hidden;border-radius:10px;opacity:0">{"".join(inner)}{cap}</div>'
                   f'<div class="cpb" style="position:absolute;inset:-5px;border:6px solid #2b2118;border-radius:12px;clip-path:inset(0 100% 100% 0)"></div></div>', z=6)
        self.panels[pid] = (x, y, w, h)
        return self

    def draw(self, t, pid):
        """칸 테두리가 그려지고(왼쪽 위 → 오른쪽 아래) 안이 채워짐."""
        f = self.f
        f._setv(t, f"#{pid}", {"opacity": 1})
        f._tween(t, f"#{pid} .cpb", {"clipPath": "inset(0 0% 0% 0)"}, .55, "power2.inOut")
        f._tween(t + .35, f"#{pid} .cpi", {"opacity": 1}, .4)
        f._js(f"tl.fromTo('#{pid} .pa',{{y:30,opacity:0}},{{y:0,opacity:1,duration:.45,stagger:.15,ease:'back.out(1.6)',immediateRender:false}},{t + .5:.3f});")
        f._js(f"tl.to('#{pid} .pp',{{opacity:1,duration:.2,stagger:.12}},{t + .6:.3f});")
        f._js(f"tl.fromTo('#{pid} .pp',{{x:-120,rotation:-30}},{{x:0,rotation:0,duration:.6,stagger:.12,ease:'power3.out',immediateRender:false}},{t + .6:.3f});")
        f._sound(t, "whoosh-short", .12)

    def line(self, t, pid, i):
        n = 12
        self.f._js(f"tl.to('#{pid}_l{i} .ch',{{opacity:1,duration:.04,stagger:{0.5/n:.3f}}},{t:.3f});")
        self.f._sound(t, "click-soft", .12)

    def focus(self, t, pid, s=1.45, dur=1.4):
        x, y, w, h = self.panels[pid]
        self.f._cam(t, self.id, x + w / 2, y + h / 2, s, dur)
