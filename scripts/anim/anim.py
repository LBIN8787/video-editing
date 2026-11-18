"""그린 원화(배경 판 + 인물·소품 조각)를 층으로 놓고 말에 맞춰 움직이는 장면 엔진 (2026-11-18).

사용자: "아직 그림판이나 도형들로 칠한 느낌이 강해요" · "Codex 세션 영상은 전부 불합격, 화풍만 합격".
→ 그림은 사람이 그린 듯한 원화(합격 화풍)로만 채우고, 코드는 '움직임'만 맡는다. 도형·도표를 코드로 그리지 않는다.

    from anim import Film
    f = Film("curiosity", words_json, fps=30)
    s = f.set("paris", plate="paris.png")                        # 배경 판 (사람 없음)
    s.actor("janet", ["janet_walk", "janet_read"], x=700, y=1000, h=620)   # 판 좌표(1920 폭 기준), 발끝 기준
    f.at("자네는").pose("janet", "janet_read")                  # 그 낱말을 말하는 순간
    f.html(out) → render.js 로 프레임 렌더

규칙 (매뉴얼의 원리와 같음):
- 카메라는 이야기가 시점을 옮길 때만 천천히 움직이고, 흔들지 않는다 (2026-11-18 사용자: 흔들지 말 것).
- 인물은 자세를 바꿀 때 예비 동작(살짝 눌림) → 큰 동작 → 자리 잡기. 미끄러지듯 움직이지 않는다.
- 글자는 그림 위 손글씨 한두 낱말만 (화면이 슬라이드가 되지 않게).
"""
from __future__ import annotations

import html as H
import json
from pathlib import Path

from PIL import Image as _Image
import os


class Image:   # 원화가 아직 없을 때(YTFLOW_ANIM_DRY=1) 크기만 가짜로 — 대사 시각 점검용
    @staticmethod
    def open(p):
        if os.environ.get("YTFLOW_ANIM_DRY") and not Path(p).exists():
            class _D: size, width, height = (400, 800), 1672, 941
            return _D()
        return _Image.open(p)

ROOT = Path(__file__).resolve().parents[2]
GSAP = (ROOT / "tools/hyperframes/node_modules/gsap/dist/gsap.min.js").as_uri()
FONTS = (ROOT / "ytflow/assets/fonts").as_uri()
W, HH = 1920, 1080


class Cue:
    def __init__(self, film, t):
        self.f, self.t = film, t

    def __getattr__(self, name):   # f.at("말").pose(...) == f.pose(..., t=그 시각)
        fn = getattr(self.f, "_" + name)
        return lambda *a, **k: (fn(self.t, *a, **k), self)[1]

    def __add__(self, d):
        return Cue(self.f, self.t + d)


class Set:
    def __init__(self, film, sid, plate, w=W, focus=None):
        self.f, self.id, self.plate = film, sid, plate
        im = Image.open(film.art / plate)
        self.pw = w                       # 판을 그릴 폭 (넓은 판은 1920 보다 넓게 → 패닝)
        self.ph = round(im.height * w / im.width)
        self.items = []                   # html 조각
        self.cam0 = focus or (self.pw / 2, self.ph / 2, max(W / self.pw, HH / self.ph))

    def actor(self, aid, poses, x, y, h, par=1.0, flip=False, z=5, show=None):
        """발끝 (x, y), 첫 자세의 키 h. 같은 시트의 조각은 같은 비율로 (자세마다 키가 달라도 실제 크기 유지)."""
        sizes = {p: Image.open(self.f.art / f"{p}.png").size for p in poses}
        k = h / sizes[poses[0]][1]
        imgs = "".join(
            f'<img class="pose" data-p="{p}" src="{(self.f.art / (p + ".png")).as_uri()}" '
            f'style="width:{sizes[p][0]*k:.0f}px;height:{sizes[p][1]*k:.0f}px;left:{-sizes[p][0]*k/2:.0f}px;top:{-sizes[p][1]*k:.0f}px;'
            f'opacity:{1 if p == (show or poses[0]) else 0}">' for p in poses)
        self.items.append((par, z, f'<div class="actor" id="{aid}" style="left:{x}px;top:{y}px"><div class="mv"><div class="sq{" flip" if flip else ""}">{imgs}</div></div></div>'))
        return self

    def prop(self, pid, piece, x, y, w, par=1.0, z=6, rot=0, hidden=True, anchor="center"):
        sz = Image.open(self.f.art / f"{piece}.png").size
        h = sz[1] * w / sz[0]
        top = -h if anchor == "bottom" else -h / 2
        self.items.append((par, z, f'<div class="prop" id="{pid}" style="left:{x}px;top:{y}px;opacity:{0 if hidden else 1}">'
                                   f'<div class="mv" style="transform:rotate({rot}deg)"><img src="{(self.f.art / (piece + ".png")).as_uri()}" '
                                   f'style="width:{w:.0f}px;height:{h:.0f}px;left:{-w/2:.0f}px;top:{top:.0f}px"></div></div>'))
        return self

    def raw(self, html, par=1.0, z=7):
        self.items.append((par, z, html))
        return self

    def text(self, tid, s, x, y, size=84, color="#2b2118", font="pen", rot=-2, z=9, par=1.0, width=None, align="center", shadow=True, card=False):
        fam = {"pen": "Pen", "gothic": "Goth", "serif": "Myeongjo"}[font]
        sh = "text-shadow:0 0 18px rgba(255,250,235,.95),0 0 6px rgba(255,250,235,.95);" if shadow else ""
        wd = f"width:{width}px;margin-left:{-width/2}px;" if width else "transform:translateX(-50%);"
        if card:   # 종이 쪽지 바탕: 처음엔 숨김, enter 때 나타남
            sh = ""
            wd += ("opacity:0;background:rgba(250,245,232,.93);padding:.18em .55em .12em;border-radius:4px;"
                   "box-shadow:0 3px 10px rgba(40,30,20,.28);border:1px solid rgba(90,70,40,.25);")
        self.items.append((par, z, f'<div class="txt" id="{tid}" style="left:{x}px;top:{y}px;{wd}text-align:{align};font-family:{fam};'
                                   f'font-size:{size}px;color:{color};{sh}"><div class="tr" style="transform:rotate({rot}deg)">'
                                   + "".join(f'<span class="ch">{H.escape(c) if c != " " else "&nbsp;"}</span>' for c in s) + "</div></div>"))
        return self

    def counter(self, cid, x, y, size=120, color="#2b2118", font="serif", text="", z=9, par=1.0, align="center", card=False):
        """숫자가 올라가는 글자 (Film._count 로 움직임). 처음엔 숨김."""
        fam = {"pen": "Pen", "gothic": "Goth", "serif": "Myeongjo"}[font]
        tr = "translateX(-50%)" if align == "center" else ("translateX(-100%)" if align == "right" else "none")
        self.items.append((par, z, f'<div class="cnt" id="{cid}" style="position:absolute;left:{x}px;top:{y}px;transform:{tr};'
                                   f'font-family:{fam};font-size:{size}px;color:{color};white-space:nowrap;opacity:0;'
                                   + ("background:rgba(250,245,232,.93);padding:.12em .5em .06em;border-radius:4px;box-shadow:0 3px 10px rgba(40,30,20,.28);" if card else "")
                                   + f'">{H.escape(text)}</div>'))
        return self

    def build(self):
        layers = {}
        for par, z, h in self.items:
            layers.setdefault((par, z), []).append(h)
        out = [f'<div class="layer" data-par="1" style="z-index:1"><img class="plate" src="{(self.f.art / self.plate).as_uri()}" '
               f'style="width:{self.pw}px;height:{self.ph}px"></div>']
        for (par, z), hs in sorted(layers.items(), key=lambda x: x[0][1]):
            out.append(f'<div class="layer" data-par="{par}" style="z-index:{z}">{"".join(hs)}</div>')
        return (f'<div class="set" id="{self.id}" data-cx="{self.cam0[0]}" data-cy="{self.cam0[1]}" data-s="{self.cam0[2]}" '
                f'data-pw="{self.pw}" data-ph="{self.ph}" style="opacity:0">{"".join(out)}</div>')


class Film:
    def __init__(self, name, art: Path, words: Path, end: float):
        self.name, self.art, self.end = name, Path(art), end
        self.words = json.loads(Path(words).read_text(encoding="utf-8"))
        self.sets, self.js, self.sfx = [], [], []
        self._last = 0.0

    # ---------------------------------------------------------------- 시각
    def cue(self, word, after=None, end=False):
        """그 낱말(받아쓰기 기준, 부분 일치)을 말하기 시작하는 시각. after 이후에서 처음."""
        lo = self._last if after is None else after
        for s, e, w in self.words:
            if s >= lo - 0.05 and word in w.replace(" ", ""):
                self._last = s
                return e if end else s
        raise KeyError(f"cue {word!r} after {lo}")

    def at(self, word, after=None, d=0.0, end=False):
        return Cue(self, (word if isinstance(word, (int, float)) else self.cue(word, after, end)) + d)

    def set(self, sid, plate, w=W, focus=None):
        s = Set(self, sid, plate, w, focus)
        self.sets.append(s)
        return s

    def _js(self, line):
        self.js.append(line)

    def _sound(self, t, name, vol=0.25):
        self.sfx.append((name, round(t, 3), vol))

    # ---------------------------------------------------------------- 움직임 (t 첫 인자)
    def _show(self, t, sid, how="cut", dur=0.8, frm=None):
        """장면 전환. cut · dissolve · wipe(왼→오) · iris(가운데에서 원) · push(옆으로 밀기) · down(아래로 내려가며)."""
        self._js(f"trans({t:.3f},'{sid}','{how}',{dur},{json.dumps(frm)});")

    def _cam(self, t, sid, x, y, s, dur=2.0, ease="power2.inOut"):
        self._js(f"camTo({t:.3f},'{sid}',{x},{y},{s},{dur},'{ease}');")

    def _pose(self, t, aid, p, squash=True):
        self._js(f"pose({t:.3f},'{aid}','{p}',{str(squash).lower()});")

    def _walk(self, t, aid, dx, dur, bob=14, steps=None, dy=0):
        self._js(f"walk({t:.3f},'{aid}',{dx},{dy},{dur},{bob},{steps or max(2, round(dur*2.2))});")

    def _hop(self, t, aid, dx, dur=0.9, hgt=60, dy=0):
        self._js(f"hop({t:.3f},'{aid}',{dx},{dy},{dur},{hgt});")

    def _enter(self, t, iid, how="pop", dur=0.6, dx=0, dy=0):
        """소품·글자 등장. pop(살짝 커지며) · drop(위에서 떨어져 튕김) · slide(dx,dy 에서 미끄러져 들어옴) · fade · write(글자 한 자씩)."""
        self._js(f"enter({t:.3f},'{iid}','{how}',{dur},{dx},{dy});")

    def _leave(self, t, iid, how="fade", dur=0.5, dx=0, dy=0):
        self._js(f"leave({t:.3f},'{iid}','{how}',{dur},{dx},{dy});")

    def _move(self, t, iid, dx=0, dy=0, dur=1.0, rot=None, scale=None, ease="power2.inOut"):
        extra = (f",rotation:'+={rot}'" if rot is not None else "") + (f",scale:{scale}" if scale is not None else "")
        self._js(f"tl.to('#{iid} > .mv',{{x:'+={dx}',y:'+={dy}'{extra},duration:{dur},ease:'{ease}'}},{t:.3f});")

    def _spin(self, t, sel, deg, dur, ease="none"):
        self._js(f"tl.to('{sel}',{{rotation:'+={deg}',duration:{dur},ease:'{ease}'}},{t:.3f});")

    def _tween(self, t, sel, props: dict, dur=1.0, ease="power2.inOut"):
        p = ",".join(f"{k}:{json.dumps(v)}" for k, v in props.items())
        self._js(f"tl.to('{sel}',{{{p},duration:{dur},ease:'{ease}'}},{t:.3f});")

    def _setv(self, t, sel, props: dict):
        p = ",".join(f"{k}:{json.dumps(v)}" for k, v in props.items())
        self._js(f"tl.set('{sel}',{{{p}}},{t:.3f});")

    def _count(self, t, cid, a, b, dur=1.2, pre="", suf="", dec=0, grp=True):
        """grp=False: 천 단위 쉼표 없이 (연도 등)."""
        self._js(f"tl.set('#{cid}',{{opacity:1}},{t:.3f}); (()=>{{const o={{v:{a}}}, el=$('#{cid}');"
                 f"tl.to(o,{{v:{b},duration:{dur},ease:'power2.out',onUpdate:()=>{{el.textContent='{pre}'+o.v.toLocaleString('en-US',{{minimumFractionDigits:{dec},maximumFractionDigits:{dec},useGrouping:{str(grp).lower()}}})+'{suf}';}}}},{t:.3f});}})();")

    def _grade(self, t, sid, filt, dur=1.0):
        """색 바꾸기 (회상·현재 대비): 예 'saturate(.35) brightness(.95)'."""
        self._js(f"tl.to('#{sid}',{{filter:'{filt}',duration:{dur}}},{t:.3f});")

    # ---------------------------------------------------------------- 출력
    def html(self, out: Path, extra_css="", extra_js=""):
        body = "".join(s.build() for s in self.sets)
        js = "\n".join(self.js)
        doc = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Pen;src:url({FONTS}/NanumPenScript-Regular.ttf)}}
@font-face{{font-family:Goth;src:url({FONTS}/NanumGothic-ExtraBold.ttf)}}
@font-face{{font-family:Myeongjo;src:url({FONTS}/NanumMyeongjo-ExtraBold.ttf)}}
html,body{{margin:0;background:#000;overflow:hidden}}
#stage{{position:relative;width:{W}px;height:{HH}px;overflow:hidden;background:#000}}
.set{{position:absolute;inset:0;overflow:hidden}}
.layer{{position:absolute;left:0;top:0;transform-origin:0 0;will-change:transform}}
.plate{{position:absolute;left:0;top:0;display:block}}
.actor,.prop,.txt{{position:absolute}}
.mv,.sq{{position:absolute;left:0;top:0}}
.sq{{transform-origin:0 0}}
.pose,.prop img{{position:absolute;display:block}}
.txt{{white-space:nowrap;line-height:1.15}} .txt .ch{{display:inline-block;opacity:0}}
.vign{{position:absolute;inset:0;pointer-events:none;z-index:50;background:radial-gradient(ellipse at center,rgba(0,0,0,0) 62%,rgba(0,0,0,.22) 100%)}}
.grain{{position:absolute;inset:-50%;z-index:51;pointer-events:none;opacity:.05;
background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")}}
{extra_css}
</style></head><body><div id="stage">{body}<div class="vign"></div><div class="grain"></div></div>
<script src="{GSAP}"></script><script>
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const tl=gsap.timeline({{paused:true,defaults:{{ease:'power2.inOut'}}}});
const CAM={{}};
$$('.sq.flip').forEach(q=>gsap.set(q,{{scaleX:-1}}));  // 뒤집기는 GSAP 값으로 (CSS 로 두면 자세를 바꿀 때 180도 회전으로 읽혀 위아래가 뒤집힘)
$$('.set').forEach(s=>{{CAM[s.id]={{x:+s.dataset.cx,y:+s.dataset.cy,s:+s.dataset.s}};}});
function applyCam(){{ $$('.set').forEach(s=>{{ const c=CAM[s.id], pw=+s.dataset.pw, ph=+s.dataset.ph;
  // 판 밖이 보이지 않게 가두기
  const sc=Math.max(c.s, {W}/pw, {HH}/ph);
  const hx={W}/2/sc, hy={HH}/2/sc; const x=Math.min(Math.max(c.x,hx),pw-hx), y=Math.min(Math.max(c.y,hy),ph-hy);
  s.querySelectorAll('.layer').forEach(l=>{{ const p=+l.dataset.par;
    const lx=x+(x-pw/2)*(p-1), ly=y+(y-ph/2)*(p-1)*.5;
    l.style.transform=`translate(${{{W}/2-lx*sc}}px,${{{HH}/2-ly*sc}}px) scale(${{sc}})`; }}); }}); }}
function camTo(t,id,x,y,s,d,e){{ tl.to(CAM[id],{{x,y,s,duration:d,ease:e}},t); }}
function hideOthers(id,t){{ $$('.set').forEach(s=>{{ if(s.id!==id) tl.set(s,{{opacity:0,clipPath:'none',zIndex:1}},t); }}); }}  // 장면이 바뀌면 나머지는 모두 숨김
function trans(t,id,how,d,frm){{ const el='#'+id;
  if(how==='cut'||!frm){{ tl.set(el,{{opacity:1,zIndex:2,clipPath:'none',x:0,y:0}},t); if(frm) tl.set('#'+frm,{{opacity:0}},t); hideOthers(id,t); return; }}
  const F='#'+frm; tl.set(F,{{zIndex:1}},t); if(how!=='wipe'&&how!=='iris') tl.set(el,{{clipPath:'none'}},t);
  if(how==='dissolve'){{ tl.fromTo(el,{{opacity:0,zIndex:2}},{{opacity:1,duration:d,immediateRender:false}},t); }}
  else if(how==='wipe'){{ tl.fromTo(el,{{opacity:1,zIndex:2,clipPath:'inset(0 100% 0 0)'}},{{clipPath:'inset(0 0% 0 0)',duration:d,ease:'power2.inOut',immediateRender:false}},t); }}
  else if(how==='iris'){{ tl.fromTo(el,{{opacity:1,zIndex:2,clipPath:'circle(0% at 50% 50%)'}},{{clipPath:'circle(75% at 50% 50%)',duration:d,ease:'power2.in',immediateRender:false}},t); }}
  else if(how==='push'){{ tl.fromTo(el,{{opacity:1,zIndex:2,x:{W}}},{{x:0,duration:d,ease:'power3.inOut',immediateRender:false}},t);
                         tl.to(F,{{x:-{W},duration:d,ease:'power3.inOut'}},t); tl.set(F,{{x:0}},t+d); }}
  else if(how==='down'){{ tl.fromTo(el,{{opacity:1,zIndex:2,y:-{HH}}},{{y:0,duration:d,ease:'power3.inOut',immediateRender:false}},t);
                         tl.to(F,{{y:{HH},duration:d,ease:'power3.inOut'}},t); tl.set(F,{{y:0}},t+d); }}
  tl.set(F,{{opacity:0}},t+d); hideOthers(id,t+d); }}
function pose(t,id,p,sq){{ const a=$('#'+id); const q=a.querySelector('.sq'); const fl=q.classList.contains('flip')?-1:1;
  if(sq){{ tl.to(q,{{scaleY:.94,scaleX:1.04*fl,duration:.09,ease:'power1.in'}},t-.09);
          tl.to(q,{{scaleY:1,scaleX:fl,duration:.45,ease:'elastic.out(1,.5)'}},t); }}
  a.querySelectorAll('.pose').forEach(i=>tl.set(i,{{opacity:i.dataset.p===p?1:0}},t)); }}
function walk(t,id,dx,dy,d,bob,n){{ const m=$('#'+id+' > .mv');
  tl.to(m,{{x:'+='+dx,y:'+='+dy,duration:d,ease:'sine.inOut'}},t);
  for(let i=0;i<n;i++){{ const s=t+i*d/n; tl.to(m.firstChild,{{y:-bob,duration:d/n/2,ease:'sine.out'}},s); tl.to(m.firstChild,{{y:0,duration:d/n/2,ease:'sine.in'}},s+d/n/2); }} }}
function hop(t,id,dx,dy,d,h){{ const m=$('#'+id+' > .mv'), q=m.firstChild; const fl=q.classList.contains('flip')?-1:1;
  tl.to(q,{{scaleY:.9,scaleX:1.06*fl,duration:.12}},t); tl.to(m,{{x:'+='+dx,y:'+='+dy,duration:d,ease:'power1.inOut'}},t+.12);
  tl.to(q,{{y:-h,scaleY:1.06,scaleX:.96*fl,duration:d/2,ease:'power2.out'}},t+.12); tl.to(q,{{y:0,scaleY:1,scaleX:fl,duration:d/2,ease:'power2.in'}},t+.12+d/2);
  tl.to(q,{{scaleY:.93,scaleX:1.05*fl,duration:.08}},t+.12+d); tl.to(q,{{scaleY:1,scaleX:fl,duration:.35,ease:'elastic.out(1,.5)'}},t+.2+d); }}
function enter(t,id,how,d,dx,dy){{ const e=$('#'+id); tl.set(e,{{opacity:1}},t);
  if(e.classList.contains('txt')||how==='write'){{ tl.set(e,{{opacity:1}},t); tl.to(e.querySelectorAll('.ch'),{{opacity:1,duration:.05,stagger:d/Math.max(1,e.querySelectorAll('.ch').length)}},t);
     tl.fromTo(e.querySelectorAll('.ch'),{{y:8}},{{y:0,duration:.25,stagger:d/Math.max(1,e.querySelectorAll('.ch').length),immediateRender:false}},t); return; }}
  const m=e.querySelector('.mv');
  if(how==='pop') tl.fromTo(m,{{scale:.6}},{{scale:1,duration:d,ease:'back.out(2)',immediateRender:false}},t);
  else if(how==='drop') tl.fromTo(m,{{y:'-=500'}},{{y:'+=500',duration:d,ease:'bounce.out',immediateRender:false}},t);
  else if(how==='slide') tl.fromTo(m,{{x:'-='+dx,y:'-='+dy}},{{x:'+='+dx,y:'+='+dy,duration:d,ease:'power3.out',immediateRender:false}},t);
  else tl.fromTo(e,{{opacity:0}},{{opacity:1,duration:d,immediateRender:false}},t); }}
function leave(t,id,how,d,dx,dy){{ const e=$('#'+id), m=e.querySelector('.mv')||e;
  if(how==='slide') tl.to(m,{{x:'+='+dx,y:'+='+dy,duration:d,ease:'power2.in'}},t);
  if(how==='shrink') tl.to(m,{{scale:0,duration:d,ease:'back.in(2)'}},t);
  tl.to(e,{{opacity:0,duration:how==='fade'?d:.15}},how==='fade'?t:t+d-.15); }}
{js}
{extra_js}
tl.set({{}},{{}},{self.end});
window.TOTAL={self.end};
window.seek=t=>{{tl.seek(t,false); applyCam();}};
seek(0);
</script></body></html>"""
        Path(out).write_text(doc, encoding="utf-8")
        Path(out).with_suffix(".sfx.json").write_text(json.dumps(self.sfx), encoding="utf-8")
        return out
