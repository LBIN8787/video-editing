"""연기 감지기 대목 A/B: A = 고급 렌더 사물, B = LottieFiles 무료 애니메이션. 같은 자리·같은 시각."""
import json, shutil
from pathlib import Path

BASE = Path("E:/ytflow-local")
SRC3D = BASE / "hf-3d"
LOT = BASE / "hf-lottie/assets/lottie"
REN = BASE / "hf-premium/gen"

CAPS = """<div class="clip cap" id="cap14" data-start="0.45" data-duration="7.26" data-track-index="20"><span>진화 의학자 랜돌프 네스는 같은 원리를, 집 천장에 달린 연기 감지기에 빗댑니다.</span></div>
<div class="clip cap" id="cap15" data-start="8.2" data-duration="9.85" data-track-index="20"><span>연기 감지기는 토스트만 살짝 태워도 요란하게 울리지만, 그 정도로 예민하지 않으면 진짜 불이 났을 때 울리지 않을 수 있습니다.</span></div>
<audio id="vo14" class="clip" src="assets/vo/l14.mp3" data-start="0.4" data-duration="7.51" data-track-index="7" data-volume="1"></audio>
<audio id="vo15" class="clip" src="assets/vo/l15.mp3" data-start="8.15" data-duration="10.1" data-track-index="7" data-volume="1"></audio>
<audio id="sx1" class="clip" src="assets/sfx/whoosh-short.mp3" data-start="1.0" data-duration="0.57" data-track-index="8" data-volume="0.3"></audio>
<audio id="sx2" class="clip" src="assets/sfx/pop.mp3" data-start="1.5" data-duration="0.5" data-track-index="9" data-volume="0.25"></audio>
<audio id="sx3" class="clip" src="assets/sfx/whoosh.mp3" data-start="9.5" data-duration="0.57" data-track-index="8" data-volume="0.25"></audio>
<audio id="sx4" class="clip" src="assets/sfx/chime.mp3" data-start="11.2" data-duration="1.2" data-track-index="9" data-volume="0.3"></audio>
<audio id="sx5" class="clip" src="assets/sfx/whoosh-cinematic.mp3" data-start="14.2" data-duration="1.4" data-track-index="8" data-volume="0.22"></audio>"""

HEAD = """<!doctype html><html><head><meta charset="utf-8">
<script src="assets/gsap.min.js"></script>%EXTRA%
<style>
@font-face{font-family:'NotoKR';src:url('assets/fonts/NotoSansKR-VF.ttf');font-weight:100 900}
html,body{margin:0;background:#E8E3D9}
#root{position:relative;width:1920px;height:1080px;overflow:hidden;font-family:'NotoKR';color:#22345F}
#paper{position:absolute;inset:-30px;background:url('assets/img/paper.jpg') center/cover}
#stage{position:absolute;inset:0;transform-origin:50% 40%}
.obj{position:absolute;opacity:0}
.sh{filter:drop-shadow(0 26px 26px rgba(40,30,20,.28)) drop-shadow(0 6px 8px rgba(40,30,20,.18))}
.lab{position:absolute;font-size:34px;font-weight:700;letter-spacing:-.5px;color:#22345F;white-space:nowrap;opacity:0}
.lab small{display:block;font-size:22px;font-weight:500;color:#7A7468}
#name{position:absolute;left:110px;top:96px;padding:18px 30px 16px;background:rgba(251,249,244,.96);box-shadow:0 10px 28px rgba(40,34,24,.16);opacity:0}
#name b{display:block;font-size:42px;font-weight:800;color:#1E2A44}
#name span{display:block;font-size:24px;font-weight:500;color:#7A7468;margin-top:4px}
.ring{position:absolute;left:960px;top:250px;width:300px;height:300px;margin:-150px 0 0 -150px;border-radius:50%;border:5px solid #D9483B;opacity:0}
.puff{position:absolute;width:160px;height:160px;margin:-80px 0 0 -80px;border-radius:50%;background:radial-gradient(rgba(90,86,80,.55),rgba(90,86,80,0) 70%);opacity:0;filter:blur(4px)}
#glow{position:absolute;left:1400px;top:600px;width:620px;height:620px;margin:-310px 0 0 -310px;border-radius:50%;background:radial-gradient(rgba(255,160,70,.45),rgba(255,140,60,0) 65%);opacity:0}
#led{position:absolute;width:70px;height:70px;margin:-35px 0 0 -35px;border-radius:50%;background:radial-gradient(rgba(255,40,30,.95),rgba(255,40,30,0) 70%);opacity:0}
#quiet{position:absolute;left:960px;top:250px;width:420px;height:420px;margin:-210px 0 0 -210px;border-radius:50%;border:4px dashed #9A948A;opacity:0}
.cap{position:absolute;left:0;width:1920px;top:968px;text-align:center;z-index:50}
.cap span{display:inline-block;background:rgba(29,32,36,.82);color:#fff;font-weight:600;font-size:38px;padding:6px 22px;border-radius:6px;max-width:1720px;line-height:1.35}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="19.2" data-width="1920" data-height="1080" data-layout-allow-overlap>
<div id="paper"></div>
<div id="stage">
%OBJS%
<div class="ring" id="r0"></div><div class="ring" id="r1"></div><div class="ring" id="r2"></div><div class="ring" id="r3"></div>
<div id="quiet"></div>
</div>
<div id="name"><b>랜돌프 네스</b><span>진화 의학자 · 미시간대</span></div>
<div class="lab" id="lt" style="left:720px;top:560px">살짝 탄 토스트<small>헛경보 → 요란하게 울림</small></div>
<div class="lab" id="lf" style="left:1010px;top:560px;color:#B23A2F;text-align:right">진짜 불<small>놓친 경보 → 조용함</small></div>
%CAPS%
</div>
<script>
%PRE%
const tl = gsap.timeline({ paused: true });
tl.fromTo("#paper", {x:0}, {x:-24, duration:19.2, ease:"none"}, 0);
tl.fromTo("#stage", {scale:1}, {scale:1.05, duration:19.2, ease:"sine.inOut"}, 0);
tl.fromTo("#name", {opacity:0, x:-40}, {opacity:1, x:0, duration:.45, ease:"power3.out"}, 0.5);
tl.to("#name", {opacity:0, duration:.3}, 8.0);
// 감지기(또는 종): 위에서 떨어져 자리 잡음
tl.fromTo("#det", {opacity:0, y:-380}, {opacity:1, y:0, duration:.6, ease:"bounce.out"}, 1.0);
// 토스트: 왼쪽에서 들어옴
tl.fromTo("#toast", {opacity:0, x:-420, rotation:-12}, {opacity:1, x:0, rotation:-4, duration:.5, ease:"power3.out"}, 9.5);
tl.fromTo("#lt", {opacity:0, y:14}, {opacity:1, y:0, duration:.3}, 10.0);
// 경보: 흔들림 + 고리 + 빛
tl.fromTo("#det", {rotation:0}, {rotation:4, duration:.06, repeat:31, yoyo:true, ease:"none", immediateRender:false}, 11.2);
["#r0","#r1","#r2","#r3"].forEach((r,i)=>tl.fromTo(r,{opacity:.9,scale:.6},{opacity:0,scale:2.3,duration:1.0,ease:"power1.out",immediateRender:false},11.2+i*.45));
%ALARM%
tl.to("#toast,#lt", {opacity:0, x:-300, duration:.4, ease:"power2.in"}, 13.2);
// 불: 아래에서 피어오름, 감지기는 조용함
tl.fromTo("#fire", {opacity:0, y:160, scale:.7}, {opacity:1, y:0, scale:1, duration:.55, ease:"back.out(1.6)"}, 14.3);
tl.fromTo("#glow", {opacity:0}, {opacity:1, duration:.6}, 14.5);
tl.fromTo("#glow", {scale:1}, {scale:1.08, duration:.18, repeat:17, yoyo:true, ease:"sine.inOut", immediateRender:false}, 15.0);
tl.fromTo("#lf", {opacity:0, y:14}, {opacity:1, y:0, duration:.3}, 14.9);
tl.fromTo("#quiet", {opacity:0, rotation:0}, {opacity:1, rotation:40, duration:2.5, ease:"none"}, 16.3);
tl.fromTo("#det", {filter:"saturate(1) brightness(1)"}, {filter:"saturate(.4) brightness(.92)", duration:.6, immediateRender:false}, 16.3);
%POST%
window.__timelines["main"] = tl;
</script></body></html>"""


def setup(dst):
    dst.mkdir(parents=True, exist_ok=True)
    for sub in ("fonts", "sfx", "img", "vo"):
        if not (dst / "assets" / sub).exists():
            shutil.copytree(SRC3D / "assets" / sub, dst / "assets" / sub)
    shutil.copy(SRC3D / "assets/gsap.min.js", dst / "assets/gsap.min.js")


# ── A: 고급 렌더 사물
A = BASE / "hf-ab-render"; setup(A)
(A / "assets/obj").mkdir(exist_ok=True)
for n in ("detector", "toast", "campfire"):
    shutil.copy(REN / f"{n}.png", A / f"assets/obj/{n}.png")
objsA = """<img id="det" class="obj sh" src="assets/obj/detector.png" style="left:780px;top:105px;width:360px">
<div id="led" style="left:956px;top:217px"></div>
<img id="toast" class="obj sh" src="assets/obj/toast.png" style="left:330px;top:480px;width:330px">
""" + "".join(f'<div class="puff" id="p{i}" style="left:{470 + (i % 3) * 30}px;top:520px"></div>' for i in range(9)) + """
<div id="glow"></div>
<img id="fire" class="obj sh" src="assets/obj/campfire.png" style="left:1250px;top:470px;width:330px">"""
alarmA = """tl.fromTo("#led", {opacity:0}, {opacity:1, duration:.11, repeat:17, yoyo:true, ease:"none"}, 11.2);
tl.to("#led", {opacity:0, duration:.1}, 13.2);
for (let i=0;i<9;i++){ const t0=9.9+i*0.35; tl.fromTo("#p"+i,{opacity:0,y:0,x:0,scale:.5},{opacity:.9,y:-150,x:(i%2?30:-30),scale:1.2,duration:1.1,ease:"sine.out"},t0); tl.to("#p"+i,{opacity:0,y:-300,scale:1.8,duration:1.2,ease:"sine.in"},t0+1.1); }"""
html = HEAD.replace("%EXTRA%", "").replace("%OBJS%", objsA).replace("%CAPS%", CAPS).replace("%PRE%", "").replace("%ALARM%", alarmA).replace("%POST%", "")
(A / "index.html").write_text(html, encoding="utf-8")

# ── B: LottieFiles 무료 애니메이션 (데이터를 HTML 안에 넣어 동기 로드, 타임라인이 프레임을 직접 지정)
B = BASE / "hf-ab-lottie"; setup(B)
data = {n: json.load(open(LOT / f"{n}.json", encoding="utf-8")) for n in ("bell", "toaster", "smoke", "flame")}
objsB = """<div id="det" class="obj" style="left:810px;top:90px;width:300px;height:300px"></div>
<div id="toast" class="obj" style="left:330px;top:470px;width:320px;height:350px"></div>
<div id="smoke" class="obj" style="left:330px;top:160px;width:360px;height:360px"></div>
<div id="glow"></div>
<div id="fire" class="obj" style="left:1210px;top:440px;width:400px;height:300px"></div>"""
pre = "const D = " + json.dumps(data, separators=(",", ":")) + ";\n" + """
const mk = (id, d) => lottie.loadAnimation({ container: document.getElementById(id), renderer: "svg", loop: false, autoplay: false, animationData: d });
const A = { det: mk("det", D.bell), toast: mk("toast", D.toaster), smoke: mk("smoke", D.smoke), fire: mk("fire", D.flame) };
// 시각 → 프레임 (loop 는 나머지)
const drive = (a, d, t0, t1, loop) => { const p = { t: 0 }; tl.fromTo(p, { t: 0 }, { t: t1 - t0, duration: t1 - t0, ease: "none",
  onUpdate: () => { const f = p.t * d.fr; a.goToAndStop(loop ? (f % (d.op - d.ip)) + d.ip : Math.min(f + d.ip, d.op - 1), true); } }, t0); };
"""
alarmB = """drive(A.det, D.bell, 11.2, 13.2, true);
drive(A.toast, D.toaster, 9.5, 11.6, false);
tl.fromTo("#smoke", {opacity:0}, {opacity:.85, duration:.4}, 9.9); tl.to("#smoke", {opacity:0, duration:.4}, 13.1);
drive(A.smoke, D.smoke, 9.9, 13.5, true);
drive(A.fire, D.flame, 14.3, 19.2, true);"""
htmlB = HEAD.replace("%EXTRA%", '\n<script src="https://cdn.jsdelivr.net/npm/lottie-web@5.12.2/build/player/lottie_light.min.js"></script>') \
    .replace("%OBJS%", objsB).replace("%CAPS%", CAPS).replace("%PRE%", "").replace("%ALARM%", alarmB).replace("%POST%", "")
htmlB = htmlB.replace("const tl = gsap.timeline({ paused: true });", "const tl = gsap.timeline({ paused: true });\n" + pre)
(B / "index.html").write_text(htmlB, encoding="utf-8")
(B / "assets/lottie_credits.json").write_text((LOT / "credits.json").read_text(encoding="utf-8"), encoding="utf-8")
print("ok")
