"""HyperFrames 모션그래픽 공용 도구 — 불안 편(20261125-knowledge-fear/full/build.py)의 S 클래스를 옮김 (시범작, 2026-11-26).
템포: 조각마다 pause(쉼)를 시간선에 반영 (scripts/anim/tempo_vo.py 의 lines.json).
쓰는 법: setup(lines, plan) → scene(sid) 로 장면을 그리고 → write(work_dir, sfx=[...]).
"""
import json, math, random, re, subprocess
from pathlib import Path

INK, RED, GRN, VIO, YEL, NAVY, BLU = "#2B2F3A", "#D9483B", "#3FAE76", "#A98BF0", "#E8B931", "#22345F", "#7FB2E5"
LIGHT = "#EDE7DA"
L, SC, SCENES, END = [], {}, [], 0.0
LEAD, CHGAP = 0.5, 0.8


def setup(lines, plan):
    """plan = [(sid, 첫 조각 번호, 어두운 바탕?)]"""
    global END
    L[:] = lines; t = LEAD
    for k, x in enumerate(L):
        if k and x["ch"] != L[k - 1]["ch"]:
            t += CHGAP
        x["start"] = round(t, 2); t += x["dur"] + x.get("pause", .22)
    END = round(t + 1.5, 2)
    SC.clear()
    for k, (sid, i0, dark) in enumerate(plan):
        st = 0.0 if k == 0 else round(L[i0]["start"] - .25, 2)
        SC[sid] = {"start": st, "dark": dark, "first": i0}
    for k, (sid, _, _) in enumerate(plan):
        SC[sid]["end"] = SC[plan[k + 1][0]]["start"] if k + 1 < len(plan) else END
        SC[sid]["dur"] = round(SC[sid]["end"] - SC[sid]["start"], 2)


class S:
    def __init__(self, sid):
        self.sid, self.s = sid, SC[sid]
        self.dark = self.s["dark"]
        self.fg = LIGHT if self.dark else INK
        self.body, self.js, self.n = [], [], 0

    def cue(self, i, frac=0.0, off=0.0):
        return round(max(.05, L[i]["start"] + L[i]["dur"] * frac - self.s["start"] + off), 2)

    def add(self, h): self.body.append(h)
    def j(self, s): self.js.append(s)

    def uid(self, p="e"):
        self.n += 1; return f"{self.sid}-{p}{self.n}"

    # ── 붙이기 ──
    def svg(self, inner, sid=None):
        a = f'id="{sid}" ' if sid else ""
        self.add(f'<svg {a}style="position:absolute;left:0;top:0;overflow:visible" width="1920" height="1080">{inner}</svg>')

    def text(self, x, y, s, size=56, color=None, font="pen", extra="", center=False):
        i = self.uid("t"); color = color or self.fg
        al = f"left:0;width:1920px;text-align:center;" if center else f"left:{x}px;"
        fam = {"pen": "Pen", "my": "Myeongjo", "sans": "NotoKR"}[font]
        self.add(f'<div id="{i}" style="position:absolute;{al}top:{y}px;font-family:{fam};font-size:{size}px;color:{color};white-space:nowrap;opacity:0;font-weight:{800 if font == "sans" else 400};{extra}">{s}</div>')
        return i

    def tag(self, x, y, s, bg=RED, fg="#fff", size=40):
        i = self.uid("g")
        self.add(f'<div id="{i}" style="position:absolute;left:{x}px;top:{y}px;padding:8px 26px;border-radius:40px;background:{bg};color:{fg};font-size:{size}px;font-weight:700;white-space:nowrap;opacity:0">{s}</div>')
        return i

    def name(self, x, y, who, what):
        i = self.uid("n")
        bg = "#F6F1E6" if not self.dark else "#2C313B"
        self.add(f'<div id="{i}" style="position:absolute;left:{x}px;top:{y}px;padding:14px 28px;background:{bg};border-left:8px solid {RED};box-shadow:0 10px 20px rgba(0,0,0,.22);opacity:0">'
                 f'<div style="font-size:46px;font-weight:800;color:{self.fg}">{who}</div><div style="font-size:28px;color:{"#9AA0AA" if self.dark else "#6E6A60"};margin-top:2px">{what}</div></div>')
        return i

    def photo(self, x, y, w, h, img, cap="", rot=0, pos="50% 30%"):
        i = self.uid("p")
        self.add(f'<div id="{i}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;padding:14px 14px 10px;background:#FBF9F4;box-shadow:0 14px 26px rgba(30,24,16,.3);transform:rotate({rot}deg);opacity:0">'
                 f'<img src="assets/img/{img}" style="width:{w - 28}px;height:{h}px;object-fit:cover;object-position:{pos}">'
                 f'<div style="font-family:Pen;font-size:36px;color:{INK};text-align:center;margin-top:4px">{cap}</div></div>')
        return i

    # ── 움직임 (역할별 속도) ──
    def pop(self, i, t, d=.3): self.j(f'tl.fromTo("#{i}",{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:{d},ease:"back.out(2.2)"}},{t});')
    def slide(self, i, t, dx=-400, d=.35): self.j(f'tl.fromTo("#{i}",{{opacity:0,x:{dx}}},{{opacity:1,x:0,duration:{d},ease:"power3.out"}},{t});')
    def drop(self, i, t, d=.45): self.j(f'tl.fromTo("#{i}",{{opacity:0,y:-160}},{{opacity:1,y:0,duration:{d},ease:"bounce.out"}},{t});')
    def rise(self, i, t, d=.4): self.j(f'tl.fromTo("#{i}",{{opacity:0,y:60}},{{opacity:1,y:0,duration:{d},ease:"power2.out"}},{t});')
    def fade(self, i, t, d=.35, a=0, b=1): self.j(f'tl.fromTo("#{i}",{{opacity:{a}}},{{opacity:{b},duration:{d}}},{t});')
    def out(self, ids, t, d=.25): self.j(f'tl.to("{",".join("#" + x for x in ids)}",{{opacity:0,duration:{d}}},{t});')
    def stamp(self, i, t): self.j(f'tl.fromTo("#{i}",{{opacity:0,scale:2}},{{opacity:1,scale:1,duration:.22,ease:"power4.in"}},{t});')
    def draw(self, i, t, d=.6, ease="power1.inOut"): self.j(f'tl.fromTo("#{i}",{{drawSVG:"0%"}},{{drawSVG:"100%",duration:{d},ease:"{ease}"}},{t});')
    def spread(self, i, t, d=.5): self.j(f'tl.fromTo("#{i}",{{drawSVG:"50% 50%"}},{{drawSVG:"0% 100%",duration:{d},ease:"power2.out"}},{t});')
    def shake(self, i, t, n=5, amp=10): self.j(f'tl.fromTo("#{i}",{{x:0}},{{x:{amp},duration:.05,repeat:{n},yoyo:true}},{t});')
    def blink(self, i, t, n=3, d=.18): self.j(f'tl.fromTo("#{i}",{{opacity:1}},{{opacity:.15,duration:{d},repeat:{n * 2 - 1},yoyo:true}},{t});')
    def ring(self, i, t, n=2, d=1.0, s=3): self.j(f'tl.fromTo("#{i}",{{scale:.4,opacity:1,transformOrigin:"50% 50%"}},{{scale:{s},opacity:0,duration:{d},repeat:{n - 1},ease:"power1.out"}},{t});')
    def marker(self, i, t, d=.55): self.j(f'tl.fromTo("#{i}",{{backgroundSize:"0% 40%"}},{{backgroundSize:"100% 40%",duration:{d},ease:"power2.out"}},{t});')
    def count(self, i, t, a, b, d=1.0, comma=True):
        v = f'cv{self.uid("c").replace("-", "_")}'
        fmt = 'toLocaleString("en-US")' if comma else 'toString()'
        self.j(f'const {v}={{v:{a}}};tl.fromTo({v},{{v:{a}}},{{v:{b},duration:{d},ease:"power2.out",onUpdate:function(){{document.getElementById("{i}").textContent=Math.round({v}.v).{fmt}}}}},{t});')

    def anotb(self, y, a, b, t_a, t_x, t_b, size=92):
        """'A가 아니라 B' — A 에 줄, B 에 형광펜."""
        ia = self.text(0, y, a, size, font="my", center=True)
        ib = self.uid("b")
        self.add(f'<div style="position:absolute;left:0;width:1920px;top:{y + size + 50}px;text-align:center">'
                 f'<span id="{ib}" class="mk" style="font-family:Myeongjo;font-size:{size}px;color:{RED};opacity:0;display:inline-block">{b}</span></div>')
        ix = self.uid("x")
        self.svg(f'<path id="{ix}" d="M{960 - len(a) * size * .5:.0f},{y + size * .62:.0f} L{960 + len(a) * size * .5:.0f},{y + size * .5:.0f}" stroke="{RED}" stroke-width="10" stroke-linecap="round" fill="none"/>')
        self.rise(ia, t_a); self.draw(ix, t_x, .25); self.pop(ib, t_b, .3); self.marker(ib, t_b + .3)
        return ia, ib, ix

    def fixjs(self):
        seen, out = set(), []
        for x in self.js:
            m = re.match(r'tl\.fromTo\("([^"]+)"', x)
            if m:
                if m.group(1) in seen and "immediateRender" not in x:
                    a, b = x.rsplit("},", 1); x = a + ",immediateRender:false}," + b
                seen.add(m.group(1))
            out.append(x)
        return out

    def html(self):
        bg = "paper_dark.jpg" if self.dark else "paper.jpg"
        d = self.s["dur"]
        return f"""<template>
<style>
@font-face{{font-family:'NotoKR';src:url('assets/fonts/NotoSansKR-VF.ttf');font-weight:100 900}}
@font-face{{font-family:'Pen';src:url('assets/fonts/NanumPenScript-Regular.ttf')}}
@font-face{{font-family:'Myeongjo';src:url('assets/fonts/NanumMyeongjo-ExtraBold.ttf')}}
#root{{position:absolute;inset:0;overflow:hidden;font-family:'NotoKR';color:{self.fg};background:{'#1E2128' if self.dark else '#E8E3D9'}}}
.bg{{position:absolute;inset:-40px;background:url('assets/img/{bg}') center/cover}}
.cam{{position:absolute;inset:0;transform-origin:50% 50%}}
.mk{{background:linear-gradient(rgba(232,185,49,.55),rgba(232,185,49,.55)) no-repeat 0 88%;background-size:0% 40%}}
.dot{{position:absolute;width:14px;height:14px;margin:-7px 0 0 -7px;border-radius:50%;background:#7D8594}}
</style>
<div id="root" data-composition-id="{self.sid}" data-width="1920" data-height="1080" data-layout-allow-overlap>
<div class="bg" id="{self.sid}-bg"></div>
<div class="cam" id="{self.sid}-cam">{''.join(self.body)}</div>
</div>
<script>
gsap.registerPlugin(MotionPathPlugin, DrawSVGPlugin, ScrambleTextPlugin);
const tl = gsap.timeline({{ paused: true }});
tl.fromTo("#{self.sid}-bg", {{x:0}}, {{x:-30, duration:{d}, ease:"none"}}, 0);
tl.fromTo("#{self.sid}-cam", {{scale:1}}, {{scale:1.035, duration:{d}, ease:"sine.inOut"}}, 0);
{''.join(self.fixjs())}
window.__timelines["{self.sid}"] = tl;
</script>
</template>
"""



def scene(sid):
    c = S(sid); SCENES.append(c); return c


def write(work, sfx=(), cap_top=960):
    work = Path(work)
    for s in SCENES:
        (work / "compositions" / f"{s.sid}.html").write_text(s.html(), encoding="utf-8")
    caps = "".join(f'<div class="clip cap" id="cap{x["i"]}" data-start="{x["start"] + .05:.2f}" data-duration="{x["dur"] - .1:.2f}" data-track-index="20"><span>{x["text"]}</span></div>' for x in L)
    aud = "".join(f'<audio id="vo{x["i"]}" class="clip" src="assets/vo/{x["file"]}" data-start="{x["start"]}" data-duration="{x["dur"]}" data-track-index="7" data-volume="1"></audio>' for x in L)
    def _d(f):
        return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(work / f)], capture_output=True, text=True).stdout)
    for k, (n, i, fr) in enumerate(sfx):
        f = f"assets/sfx/{n}.{'wav' if n == 'pencil' else 'mp3'}"
        tt = round(L[i]["start"] + L[i]["dur"] * fr, 2)
        aud += f'<audio id="sx{k}" class="clip" src="{f}" data-start="{tt}" data-duration="{min(1.4, _d(f)):.2f}" data-track-index="{8 + k % 3}" data-volume="{0.14 if n in ("pencil", "riser") else 0.24}"></audio>'
    hosts = "".join(f'<div id="{s.sid}" data-composition-id="{s.sid}" data-composition-src="compositions/{s.sid}.html" data-start="{s.s["start"]}" '
                    f'data-duration="{s.s["dur"]}" data-track-index="1" data-track-kind="graphics" data-width="1920" data-height="1080"></div>' for s in SCENES)
    (work / "index.html").write_text(f"""<!doctype html><html><head><meta charset="utf-8">
<script src="assets/gsap.min.js"></script><script src="assets/MotionPathPlugin.min.js"></script><script src="assets/DrawSVGPlugin.min.js"></script><script src="assets/ScrambleTextPlugin.min.js"></script>
<style>
@font-face{{font-family:'NotoKR';src:url('assets/fonts/NotoSansKR-VF.ttf');font-weight:100 900}}
.cap{{position:absolute;left:0;width:1920px;top:{cap_top}px;text-align:center;z-index:50;font-family:'NotoKR'}}
.cap span{{display:inline-block;background:rgba(29,32,36,.82);color:#fff;font-weight:600;font-size:40px;padding:6px 22px;border-radius:6px;max-width:1720px;line-height:1.35}}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{END}" data-width="1920" data-height="1080">
{hosts}{caps}{aud}
</div>
<script>window.__timelines["main"] = gsap.timeline({{ paused: true }});</script>
</body></html>""", encoding="utf-8")
    print("END", END, len(SCENES), {k: (v["start"], v["dur"]) for k, v in SC.items()})
