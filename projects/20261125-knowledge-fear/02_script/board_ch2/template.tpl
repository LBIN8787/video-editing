<!doctype html>
<html><head><meta charset="utf-8">
<script src="assets/gsap.min.js"></script>
<script type="importmap">{"imports":{"three":"./assets/three.module.js"}}</script>
<style>
@font-face{font-family:'NotoKR';src:url('assets/fonts/NotoSansKR-VF.ttf');font-weight:100 900}
@font-face{font-family:'Myeongjo';src:url('assets/fonts/NanumMyeongjo-ExtraBold.ttf')}
@font-face{font-family:'Pen';src:url('assets/fonts/NanumPenScript-Regular.ttf')}
html,body{margin:0;background:#E8E3D9}
#root{position:relative;width:1920px;height:1080px;overflow:hidden;font-family:'NotoKR';color:#22345F}
#gl{position:absolute;left:0;top:0;width:1920px;height:1080px}
.an{position:absolute;left:0;top:0;white-space:nowrap;opacity:0;will-change:transform}
.lab{font-size:30px;font-weight:600;color:#22345F;letter-spacing:-.4px}
.lab small{display:block;font-size:21px;font-weight:500;color:#7A7468}
.pen{font-family:'Pen';font-size:44px;color:#B23A2F}
.card{position:absolute;padding:16px 28px 14px;background:rgba(251,249,244,.97);box-shadow:0 10px 28px rgba(40,34,24,.16);opacity:0}
.card b{display:block;font-size:40px;font-weight:800;color:#1E2A44}
.card span{display:block;font-size:23px;font-weight:500;color:#7A7468;margin-top:3px}
#ctx{position:absolute;left:110px;top:44px;font-size:24px;font-weight:600;color:#8A857A;letter-spacing:1px;opacity:0}
#stamp{position:absolute;left:1270px;top:150px;padding:4px 32px;border:7px solid #B23A2F;border-radius:12px;color:#B23A2F;font-family:Myeongjo;font-size:58px;transform:rotate(-5deg);opacity:0}
#tr{position:absolute;left:0;width:1920px;top:850px;text-align:center;font-family:Myeongjo;font-size:44px;color:#1E2A44;opacity:0}
#hd{position:absolute;left:0;width:1920px;top:70px;text-align:center;opacity:0}
#hd .q{font-size:30px;font-weight:600;color:#8A857A;letter-spacing:1px}
#hd .a{display:inline-block;position:relative;font-family:Myeongjo;font-size:70px;color:#6E6A60;margin-top:8px}
#hd .a i{position:absolute;left:-6px;right:-6px;top:52%;height:7px;background:#B23A2F;transform:scaleX(0);transform-origin:0 50%}
#hd .b{display:block;font-family:Myeongjo;font-size:84px;color:#B23A2F;margin-top:4px;opacity:0}
#hd .b span{background:linear-gradient(rgba(232,185,49,.5),rgba(232,185,49,.5)) no-repeat 0 88%;background-size:0% 38%}
.cap{position:absolute;left:0;width:1920px;top:968px;text-align:center;z-index:50}
.cap span{display:inline-block;background:rgba(29,32,36,.82);color:#fff;font-weight:600;font-size:38px;padding:6px 22px;border-radius:6px;max-width:1720px;line-height:1.35}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="%END%" data-width="1920" data-height="1080" data-layout-allow-overlap>
  <canvas id="gl" width="1920" height="1080"></canvas>
  <div id="ctx">2장 · 경보는 왜 예민할까</div>
  <div class="card" id="nL" style="left:110px;top:96px"><b>조지프 르두</b><span>신경과학자 · 뉴욕대</span></div>
  <div class="card" id="nN" style="left:110px;top:96px"><b>랜돌프 네스</b><span>진화 의학자 · 미시간대</span></div>
  <div id="stamp">연기 감지기 원리</div>
  <div id="tr">"막대기를 뱀으로 착각하는 편이, 뱀을 막대기로 착각하는 것보다 낫다"</div>
  <div id="hd"><div class="q">경보가 예민한 까닭</div><div class="a">고장 나서<i></i></div><div class="b"><span>덜 위험한 쪽을 골라서</span></div></div>
  <!-- 세계에 붙는 표시 (위치는 3D 좌표에서 매 프레임 계산) -->
  <div class="an pen" id="aQ">뱀? 막대기?</div>
  <div class="an lab" id="aEye">눈</div>
  <div class="an lab" id="aBody">몸</div>
  <div class="an lab" id="aSlow" style="color:#2E7D52">느리고 또렷한 길</div>
  <div class="an lab" id="aFast" style="color:#B23A2F">빠르고 흐릿한 길</div>
  <div class="an pen" id="aStick" style="color:#2E7D52">'막대기구나'</div>
  <div class="an lab" id="aToast">살짝 탄 토스트<small>헛경보</small></div>
  <div class="an lab" id="aFire" style="color:#B23A2F">진짜 불<small>놓친 경보</small></div>
  <div class="an lab" id="aQuiet" style="color:#9A948A">울리지 않음</div>
  <div class="an lab" id="aCoin">헛경보<small>잠깐 귀찮음</small></div>
  <div class="an lab" id="aRock" style="color:#B23A2F">놓친 경보<small>목숨</small></div>
  %CAPS%
  %AUD%
</div>
<script>
const tl = gsap.timeline({ paused: true });
tl.fromTo("#ctx", {opacity:0}, {opacity:1, duration:.5}, .3);
tl.fromTo("#nL", {opacity:0, x:-40}, {opacity:1, x:0, duration:.4, ease:"power3.out"}, .6);
tl.to("#nL", {opacity:0, duration:.3}, 17.0);
tl.fromTo("#nL", {opacity:0, x:-40}, {opacity:1, x:0, duration:.4, ease:"power3.out", immediateRender:false}, 29.6);
tl.to("#nL", {opacity:0, duration:.3}, 39.4);
tl.fromTo("#tr", {opacity:0, y:20}, {opacity:1, y:0, duration:.4}, 35.6);
tl.to("#tr", {opacity:0, duration:.3}, 39.3);
tl.fromTo("#nN", {opacity:0, x:-40}, {opacity:1, x:0, duration:.4, ease:"power3.out"}, 40.6);
tl.to("#nN", {opacity:0, duration:.3}, 57.4);
tl.fromTo("#stamp", {opacity:0, scale:2}, {opacity:1, scale:1, duration:.22, ease:"power4.in"}, 67.5);
tl.to("#stamp", {opacity:0, duration:.3}, 70.1);
tl.to("#ctx", {opacity:0, duration:.3}, 70.1);
tl.fromTo("#hd", {opacity:0}, {opacity:1, duration:.4}, 72.4);
tl.fromTo("#hd .a i", {scaleX:0}, {scaleX:1, duration:.3, ease:"power2.out"}, 75.0);
tl.fromTo("#hd .b", {opacity:0, y:20}, {opacity:1, y:0, duration:.35, ease:"back.out(2)"}, 76.4);
tl.fromTo("#hd .b span", {backgroundSize:"0% 38%"}, {backgroundSize:"100% 38%", duration:.6, ease:"power2.out"}, 76.8);
window.__timelines["main"] = tl;
</script>
<script type="module">
import * as THREE from "three";
import { RoundedBoxGeometry } from "./assets/RoundedBoxGeometry.js";
import { RoomEnvironment } from "./assets/RoomEnvironment.js";

const R = new THREE.WebGLRenderer({ canvas: document.getElementById("gl"), antialias: true, preserveDrawingBuffer: true });
R.setPixelRatio(1); R.setSize(1920, 1080, false);
R.shadowMap.enabled = true; R.shadowMap.type = THREE.PCFSoftShadowMap;
R.toneMapping = THREE.ACESFilmicToneMapping; R.toneMappingExposure = 1.0; R.outputColorSpace = THREE.SRGBColorSpace;
const scene = new THREE.Scene(); scene.background = new THREE.Color(0xE8E3D9);
scene.environment = new THREE.PMREMGenerator(R).fromScene(new RoomEnvironment(), 0.04).texture; scene.environmentIntensity = 0.5;
const cam = new THREE.PerspectiveCamera(30, 1920 / 1080, 0.1, 200);
const key = new THREE.DirectionalLight(0xfff1dc, 2.2); key.position.set(-6, 8, 12); key.castShadow = true;
key.shadow.mapSize.set(4096, 4096); key.shadow.radius = 7; key.shadow.blurSamples = 16; key.shadow.bias = -0.0003;
Object.assign(key.shadow.camera, { left: -30, right: 30, top: 14, bottom: -14, near: 1, far: 60 });
scene.add(key, key.target);
scene.add(new THREE.HemisphereLight(0xfffaf0, 0xc9bfae, 0.55));

// 종이 바닥 (넓은 한 판)
const ptex = new THREE.TextureLoader().load("assets/img/paper.jpg"); ptex.colorSpace = THREE.SRGBColorSpace;
ptex.wrapS = ptex.wrapT = THREE.MirroredRepeatWrapping; ptex.repeat.set(4, 1.6);
const paper = new THREE.Mesh(new THREE.PlaneGeometry(80, 30), new THREE.MeshStandardMaterial({ map: ptex, roughness: 1 }));
paper.receiveShadow = true; scene.add(paper);

// ── 도우미
const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
const ss = (a, b, t) => { const x = clamp((t - a) / (b - a)); return x * x * (3 - 2 * x); };
const backOut = x => { x = clamp(x); const c = 1.8; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
const lerp = (a, b, u) => a + (b - a) * u;
const INK = 0x26304a, RED = 0xc8473a, GRN = 0x2f8a5a;
// 선: 종이 위 가는 관(管). 그리는 정도는 drawRange
function tubeLine(points, color, r = 0.035, closed = false) {
  const curve = new THREE.CatmullRomCurve3(points.map(p => new THREE.Vector3(p[0], p[1], 0.04)), closed);
  const geo = new THREE.TubeGeometry(curve, 240, r, 8, closed);
  const m = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ color, roughness: 0.6 }));
  m.castShadow = true; m.userData.n = geo.index.count; geo.setDrawRange(0, 0); scene.add(m); m.userData.curve = curve; return m;
}
const drawTo = (m, u) => { const n = Math.floor(m.userData.n * clamp(u) / 48) * 48; m.geometry.setDrawRange(0, n); m.visible = n > 0; };
function person(color = INK, s = 1) {
  const g = new THREE.Group(); const mat = new THREE.MeshStandardMaterial({ color, roughness: 0.55 });
  const head = new THREE.Mesh(new THREE.SphereGeometry(0.22 * s, 32, 16), mat); head.position.y = 0.95 * s;
  const body = new THREE.Mesh(new THREE.CapsuleGeometry(0.24 * s, 0.55 * s, 8, 24), mat); body.position.y = 0.38 * s;
  g.add(head, body); g.traverse(o => { if (o.isMesh) o.castShadow = true; }); g.position.z = 0.3; scene.add(g); return g;
}

// ═══ A 숲길 (x≈-16) ═══
const pathL = tubeLine([[-15.6, -3.2], [-14.6, -1], [-13.9, 1], [-13.5, 2.8]], 0x5b5f6b, 0.04);
const pathR = tubeLine([[-10.4, -3.2], [-11.4, -1], [-12.1, 1], [-12.5, 2.8]], 0x5b5f6b, 0.04);
const walker = person(INK, 0.9);
const stickMat = new THREE.MeshStandardMaterial({ color: 0x7b5634, roughness: 0.8 });
const stickCurve = new THREE.CatmullRomCurve3([[-14.0, 0.9], [-13.6, 1.15], [-13.2, 0.85], [-12.8, 1.1], [-12.4, 0.88], [-12.05, 1.05]].map(p => new THREE.Vector3(p[0], p[1], 0.12)));
const stick = new THREE.Mesh(new THREE.TubeGeometry(stickCurve, 80, 0.09, 12), stickMat); stick.castShadow = true; scene.add(stick);
const ell = tubeLine(Array.from({ length: 25 }, (_, i) => { const a = i / 24 * Math.PI * 2; return [-13.0 + Math.cos(a) * 1.45, 0.98 + Math.sin(a) * 0.55]; }), RED, 0.025, false);

// ═══ B 두 길 (x≈-5) ═══
const eye = new THREE.Group();
const eyeW = new THREE.Mesh(new THREE.SphereGeometry(0.45, 40, 20), new THREE.MeshPhysicalMaterial({ color: 0xf7f5f0, roughness: 0.3, clearcoat: 0.6 }));
const pupil = new THREE.Mesh(new THREE.SphereGeometry(0.2, 32, 16), new THREE.MeshStandardMaterial({ color: 0x1c2438, roughness: 0.3 })); pupil.position.z = 0.33;
eye.add(eyeW, pupil); eye.position.set(-8.6, -0.6, 0.45); eye.traverse(o => o.castShadow = true); scene.add(eye);
const body2 = person(INK, 1.0); body2.position.set(-1.2, -1.45, 0.3);
const judge = new THREE.Mesh(new RoundedBoxGeometry(1.7, 0.75, 0.3, 4, 0.12), new THREE.MeshStandardMaterial({ color: 0xf6f2ea, roughness: 0.6 }));
judge.position.set(-4.9, 1.75, 0.2); judge.castShadow = true; scene.add(judge);
const jc = document.createElement("canvas"); jc.width = 340; jc.height = 150; const jg = jc.getContext("2d");
jg.fillStyle = "#f6f2ea"; jg.fillRect(0, 0, 340, 150); jg.fillStyle = "#2f8a5a"; jg.font = "700 64px NotoKR, sans-serif"; jg.textAlign = "center"; jg.textBaseline = "middle"; jg.fillText("판단", 170, 80);
const jt = new THREE.CanvasTexture(jc); jt.colorSpace = THREE.SRGBColorSpace;
const jface = new THREE.Mesh(new THREE.PlaneGeometry(1.6, 0.7), new THREE.MeshBasicMaterial({ map: jt, transparent: true }));
jface.position.set(0, 0, 0.16); judge.add(jface);
const slow = tubeLine([[-8.15, -0.4], [-7.2, 1.0], [-5.9, 1.75], [-3.9, 1.75], [-2.6, 0.8], [-1.6, -0.5]], GRN, 0.04);
const fast = tubeLine([[-8.1, -0.65], [-1.7, -0.75]], RED, 0.06);
const pulseF = new THREE.Mesh(new THREE.SphereGeometry(0.13, 20, 10), new THREE.MeshBasicMaterial({ color: 0xff5040 }));
const pulseS = new THREE.Mesh(new THREE.SphereGeometry(0.13, 20, 10), new THREE.MeshBasicMaterial({ color: 0x3fd08a })); scene.add(pulseF, pulseS);

// ═══ Q 르두의 말 (문서 카드, x≈5) ═══
const qc = document.createElement("canvas"); qc.width = 1400; qc.height = 760; const qg = qc.getContext("2d");
qg.fillStyle = "#fbf9f4"; qg.fillRect(0, 0, 1400, 760);
qg.fillStyle = "#8a857a"; qg.font = "600 30px NotoKR, sans-serif"; qg.fillText("THE NIH RECORD · 1997", 70, 90);
qg.fillStyle = "#3b3f48"; qg.font = "400 30px Georgia, serif";
const lines = ["LeDoux has spent years tracing how the brain", "detects danger before we are aware of it.", "", "“You're better off mistaking a stick for a snake", "than a snake for a stick,” he said.", "", "The quick and dirty pathway may be imprecise,", "but it buys precious time."];
lines.forEach((s, i) => { qg.font = (i === 3 || i === 4) ? "italic 700 46px Georgia, serif" : "400 34px Georgia, serif"; qg.fillStyle = (i === 3 || i === 4) ? "#1e2a44" : "#6b6f78"; qg.fillText(s, 70, 170 + i * 66); });
const qt = new THREE.CanvasTexture(qc); qt.colorSpace = THREE.SRGBColorSpace;
const qcard = new THREE.Mesh(new THREE.BoxGeometry(7.0, 3.8, 0.04), [0, 0, 0, 0, new THREE.MeshStandardMaterial({ map: qt, roughness: 0.9 }), 0].map(m => m || new THREE.MeshStandardMaterial({ color: 0xf3efe6 })));
qcard.position.set(5.0, 0.55, 0.1); qcard.castShadow = true; scene.add(qcard);
const hl = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), new THREE.MeshBasicMaterial({ color: 0xe8b931, transparent: true, opacity: 0.38, depthWrite: false }));
scene.add(hl);
// 작게 남는 '판 위의 메모' — 본문 라벨 대신
// (번역은 DOM #tr)

// ═══ C 감지기 (x≈15) ═══
const det = new THREE.Group(); const Rd = 1.45, H = 0.42;
const prof = [new THREE.Vector2(0, 0)]; for (let i = 0; i <= 12; i++) { const a = (i / 12) * Math.PI / 2; prof.push(new THREE.Vector2(Rd - 0.18 + Math.sin(a) * 0.18, H - 0.18 + Math.cos(a) * 0.18)); }
prof.push(new THREE.Vector2(Rd, 0.05), new THREE.Vector2(Rd - 0.05, 0));
const shell = new THREE.Mesh(new THREE.LatheGeometry(prof.reverse(), 96), new THREE.MeshPhysicalMaterial({ color: 0xf4f1ea, roughness: 0.55, clearcoat: 0.25 }));
shell.rotation.x = Math.PI / 2; shell.castShadow = true; det.add(shell);
for (const r of [0.55, 0.78, 1.0]) { const g = new THREE.Mesh(new THREE.TorusGeometry(r, 0.028, 12, 120), new THREE.MeshStandardMaterial({ color: 0xd9d4c9, roughness: 0.7 })); g.position.z = H + 0.002; det.add(g); }
const dome = new THREE.Mesh(new THREE.SphereGeometry(0.34, 48, 24, 0, Math.PI * 2, 0, Math.PI / 2), new THREE.MeshPhysicalMaterial({ color: 0xfaf8f3, roughness: 0.45, clearcoat: 0.4 }));
dome.rotation.x = Math.PI / 2; dome.position.z = H - 0.06; dome.castShadow = true; det.add(dome);
const ledMat = new THREE.MeshStandardMaterial({ color: 0x5a1712, emissive: 0xff2a1a, emissiveIntensity: 0 });
const led = new THREE.Mesh(new THREE.SphereGeometry(0.075, 24, 12), ledMat); led.position.set(0.92, 0.62, H + 0.03); det.add(led);
const rings = Array.from({ length: 6 }, () => { const m = new THREE.Mesh(new THREE.TorusGeometry(1.6, 0.035, 8, 160), new THREE.MeshBasicMaterial({ color: 0xd9483b, transparent: true, opacity: 0 })); m.position.z = 0.2; det.add(m); return m; });
det.scale.setScalar(0.7); scene.add(det);
// 토스트
const bs = new THREE.Shape(); bs.moveTo(-1.05, -1.1); bs.lineTo(1.05, -1.1); bs.lineTo(1.05, 0.55);
bs.bezierCurveTo(1.45, 0.75, 1.35, 1.45, 0.75, 1.4); bs.bezierCurveTo(0.45, 1.6, -0.45, 1.6, -0.75, 1.4); bs.bezierCurveTo(-1.35, 1.45, -1.45, 0.75, -1.05, 0.55); bs.lineTo(-1.05, -1.1);
const tg = new THREE.ExtrudeGeometry(bs, { depth: 0.3, bevelEnabled: true, bevelThickness: 0.06, bevelSize: 0.06, bevelSegments: 4, curveSegments: 24 });
const tc = document.createElement("canvas"); tc.width = tc.height = 512; const gx = tc.getContext("2d");
const grd = gx.createRadialGradient(256, 256, 40, 256, 256, 300); grd.addColorStop(0, "#C98F52"); grd.addColorStop(.7, "#A86A34"); grd.addColorStop(1, "#6E3F1C"); gx.fillStyle = grd; gx.fillRect(0, 0, 512, 512);
let sd = 7; const rnd = () => ((sd = (sd * 16807) % 2147483647) / 2147483647);
for (let i = 0; i < 900; i++) { gx.fillStyle = `rgba(${60 + rnd() * 40},${30 + rnd() * 20},10,${rnd() * .18})`; gx.beginPath(); gx.arc(rnd() * 512, rnd() * 512, rnd() * 5 + 1, 0, 7); gx.fill(); }
const tTex = new THREE.CanvasTexture(tc); tTex.colorSpace = THREE.SRGBColorSpace;
tg.computeBoundingBox(); { const bb = tg.boundingBox, uv = tg.attributes.uv, p = tg.attributes.position; for (let i = 0; i < uv.count; i++) uv.setXY(i, (p.getX(i) - bb.min.x) / (bb.max.x - bb.min.x), (p.getY(i) - bb.min.y) / (bb.max.y - bb.min.y)); }
const toast = new THREE.Mesh(tg, [new THREE.MeshStandardMaterial({ map: tTex, roughness: 0.85 }), new THREE.MeshStandardMaterial({ color: 0x7a4620, roughness: 0.8 })]);
toast.castShadow = true; toast.scale.setScalar(0.62); scene.add(toast);
const sc = document.createElement("canvas"); sc.width = sc.height = 128; const sx = sc.getContext("2d");
const sg = sx.createRadialGradient(64, 64, 0, 64, 64, 64); sg.addColorStop(0, "rgba(78,74,70,.7)"); sg.addColorStop(.5, "rgba(90,86,80,.35)"); sg.addColorStop(1, "rgba(100,96,90,0)"); sx.fillStyle = sg; sx.fillRect(0, 0, 128, 128);
const sTex = new THREE.CanvasTexture(sc);
const puffs = Array.from({ length: 22 }, (_, i) => { const m = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), new THREE.MeshBasicMaterial({ map: sTex, transparent: true, depthWrite: false, opacity: 0 })); m.userData = { off: i * 0.2, sw: 0.25 + (i % 5) * 0.07, ph: i * 1.7 }; scene.add(m); return m; });
// 불꽃
const fl = new THREE.Group();
const flameGeo = (h, r) => { const p = []; for (let i = 0; i <= 32; i++) { const u = i / 32; p.push(new THREE.Vector2(Math.sin(Math.PI * Math.pow(u, .62)) * r * (1 - u * .3), u * h)); } return new THREE.LatheGeometry(p, 64); };
const flameMat = (c0, c1, c2, a) => new THREE.ShaderMaterial({ transparent: true, depthWrite: false, blending: THREE.NormalBlending, uniforms: { uT: { value: 0 }, uA: { value: a } },
  vertexShader: `uniform float uT; varying float vY; varying vec3 vN; varying vec3 vV; void main(){ vec3 p = position; float h = clamp(p.y/2.4,0.,1.); p.x += sin(uT*9.0 + p.y*3.0)*0.10*h*h; p.z += cos(uT*7.0 + p.y*2.5)*0.08*h*h; vY = h; vec4 mv = modelViewMatrix*vec4(p,1.); vN = normalize(normalMatrix*normal); vV = normalize(-mv.xyz); gl_Position = projectionMatrix*mv; }`,
  fragmentShader: `uniform float uA; varying float vY; varying vec3 vN; varying vec3 vV; void main(){ vec3 c = mix(vec3(${c0}), vec3(${c1}), smoothstep(0.,.45,vY)); c = mix(c, vec3(${c2}), smoothstep(.45,1.,vY)); float edge = pow(abs(dot(vN,vV)), 1.4); float a = uA*edge*(1.-smoothstep(.75,1.,vY)); gl_FragColor = vec4(c, clamp(a*1.15,0.,1.)); }` });
const fO = new THREE.Mesh(flameGeo(2.5, 0.95), flameMat("1.0,.55,.12", ".95,.28,.08", ".7,.08,.05", 1.0));
const fM = new THREE.Mesh(flameGeo(1.8, 0.68), flameMat("1.0,.85,.35", "1.0,.55,.12", ".9,.25,.06", 0.9)); fM.position.z = 0.1;
const fC = new THREE.Mesh(flameGeo(1.0, 0.4), flameMat("1.0,.97,.8", "1.0,.85,.4", "1.0,.6,.2", 0.9)); fC.position.set(0, 0.05, 0.2);
fl.add(fO, fM, fC);
const gc = document.createElement("canvas"); gc.width = gc.height = 256; const gg = gc.getContext("2d"); const gr = gg.createRadialGradient(128, 128, 0, 128, 128, 128); gr.addColorStop(0, "rgba(255,170,80,.55)"); gr.addColorStop(1, "rgba(255,120,40,0)"); gg.fillStyle = gr; gg.fillRect(0, 0, 256, 256);
const glow = new THREE.Mesh(new THREE.PlaneGeometry(4.5, 4.5), new THREE.MeshBasicMaterial({ map: new THREE.CanvasTexture(gc), transparent: true, depthWrite: false, opacity: 0.6 })); glow.position.set(0, 1.0, -0.3); fl.add(glow);
const logMat = new THREE.MeshStandardMaterial({ color: 0x5a3d28, roughness: 0.85 });
for (const [r, x] of [[0.38, -0.25], [-0.38, 0.25]]) { const lg = new THREE.Mesh(new THREE.CylinderGeometry(0.19, 0.21, 2.0, 24), logMat); lg.rotation.set(0, 0, Math.PI / 2 + r); lg.position.set(x * .3, -0.05, 0.35); lg.castShadow = true; fl.add(lg); }
const fireLight = new THREE.PointLight(0xff7a30, 0, 9, 1.6); fireLight.position.set(0, 1.2, 1.4); fl.add(fireLight);
fl.scale.setScalar(0.62); scene.add(fl);
// 저울
const bal = new THREE.Group(); const darkMat = new THREE.MeshStandardMaterial({ color: 0x2b3242, roughness: 0.45, metalness: 0.2 });
const post = new THREE.Mesh(new THREE.ConeGeometry(0.45, 1.1, 40), darkMat); post.position.y = -0.55; post.castShadow = true; bal.add(post);
const beam = new THREE.Group(); const bar = new THREE.Mesh(new RoundedBoxGeometry(5.2, 0.14, 0.2, 3, 0.06), darkMat); bar.castShadow = true; beam.add(bar);
const coin = new THREE.Mesh(new THREE.CylinderGeometry(0.42, 0.42, 0.12, 48), new THREE.MeshStandardMaterial({ color: 0xd7a83a, metalness: 0.7, roughness: 0.35 }));
coin.rotation.x = Math.PI / 2; coin.castShadow = true; beam.add(coin);
const rock = new THREE.Mesh(new RoundedBoxGeometry(1.2, 0.95, 0.8, 4, 0.18), new THREE.MeshStandardMaterial({ color: 0x5b606b, roughness: 0.85 })); rock.castShadow = true; beam.add(rock);
bal.add(beam); bal.position.set(15.0, -1.35, 0.4); scene.add(bal);

// ── 세계에 붙는 표시 (3D → 화면 좌표)
const V = new THREE.Vector3();
function pin(id, p, a, dx = 0, dy = 0) {
  const el = document.getElementById(id); V.set(p[0], p[1], p[2] || 0.2).project(cam);
  const x = (V.x * .5 + .5) * 1920 + dx, y = (-V.y * .5 + .5) * 1080 + dy;
  el.style.transform = `translate(${x.toFixed(1)}px,${y.toFixed(1)}px)`; el.style.opacity = a.toFixed(3);
}
const win = (t, a, b, f = 0.3) => ss(a, a + f, t) * (1 - ss(b, b + f, t));

// ── 카메라 길: (시각, x, y, 거리)
const CAM = [[0, -13, 0.2, 13], [17.2, -12.6, 0.2, 12.6], [18.6, -5, 0.4, 13], [29.3, -5.2, 0.4, 12.6], [30.6, 5, 0.5, 11.5], [39.5, 5.1, 0.5, 11.2],
  [41.0, 15, 0.6, 12.4], [57.5, 15.1, 0.5, 12.2], [58.6, 15.1, -0.2, 12.4], [70.0, 15.1, -0.2, 12.2], [72.6, 0, 0.0, 47], [82, 0, 0.0, 46]];
function camAt(t) {
  for (let i = 0; i < CAM.length - 1; i++) { const [t0, x0, y0, z0] = CAM[i], [t1, x1, y1, z1] = CAM[i + 1];
    if (t <= t1) { const u = ss(t0, t1, t); return [lerp(x0, x1, u), lerp(y0, y1, u), lerp(z0, z1, u)]; } }
  const l = CAM[CAM.length - 1]; return [l[1], l[2], l[3]];
}

function renderAt(t) {
  const [cx, cy, cz] = camAt(t);
  cam.position.set(cx + 0.15 * Math.sin(t * 0.21), cy - 0.6, cz); cam.lookAt(cx, cy, 0);
  key.position.set(cx - 6, 8, 12); key.target.position.set(cx, 0, 0);

  // A: 길이 그려지고 사람이 걸어 올라감 → 구불구불한 것 → 멈칫, 뒤로
  drawTo(pathL, ss(0.9, 2.2, t)); drawTo(pathR, ss(1.0, 2.3, t));
  const wIn = ss(2.6, 3.0, t), walk = clamp((t - 3.0) / 10.6), back = ss(13.6, 14.0, t);
  const wy = lerp(-2.9, -0.4, walk) - 0.45 * back;
  walker.position.set(-13 + 0.05 * Math.sin(t * 7) * (1 - ss(13.4, 13.6, t)), wy, 0.3);
  walker.scale.setScalar(0.9 * lerp(1, 0.78, walk) * (0.4 + 0.6 * wIn)); walker.visible = t > 2.6;
  walker.rotation.z = -0.12 * back * (1 - ss(14.4, 15.4, t)) + 0.02 * Math.sin(t * 7) * (1 - ss(13.4, 13.6, t));
  const sIn = ss(8.5, 9.1, t); stick.scale.set(sIn, 1, 1); stick.position.x = (1 - sIn) * -16 * 0; stick.visible = t > 8.5;
  drawTo(ell, ss(10.3, 10.9, t));
  pin("aQ", [-11.4, 1.75], win(t, 10.6, 17.0));

  // B: 눈·판단·몸 → 느린 길 → 빠른 길 → 신호 달림
  const bIn = ss(18.3, 18.8, t);
  eye.scale.setScalar(Math.max(0.001, backOut((t - 18.3) / 0.45))); eye.visible = t > 18.3;
  body2.scale.setScalar(Math.max(0.001, backOut((t - 18.5) / 0.45))); body2.visible = t > 18.5;
  judge.scale.setScalar(Math.max(0.001, backOut((t - 18.9) / 0.45))); judge.visible = t > 18.9;
  pin("aEye", [-8.8, -1.4], win(t, 18.4, 70)); pin("aBody", [-0.55, -0.9], win(t, 18.6, 70));
  drawTo(slow, ss(19.2, 20.8, t)); pin("aSlow", [-6.6, 2.7], win(t, 19.6, 70));
  drawTo(fast, ss(23.9, 24.15, t)); pin("aFast", [-6.0, -1.25], win(t, 24.0, 70));
  const pf = clamp((t - 24.7) / 0.5); pulseF.visible = t > 24.7 && t < 25.4; pulseF.position.copy(fast.userData.curve.getPoint(pf)).setZ(0.2);
  const ps = clamp((t - 24.7) / 3.0); pulseS.visible = t > 24.7 && t < 28.0; pulseS.position.copy(slow.userData.curve.getPoint(ps)).setZ(0.2);
  const hit = clamp((t - 25.2) / 0.5); body2.rotation.z = 0.18 * Math.sin(hit * Math.PI) ; body2.position.x = -1.2 + 0.25 * Math.sin(hit * Math.PI);
  pin("aStick", [-2.2, 1.0], win(t, 27.7, 70));

  // Q: 문서 카드 → 형광펜이 말 위로
  const qIn = ss(29.5, 30.3, t); qcard.position.set(5.0, 0.55 + (1 - qIn) * 6, 0.1 + (1 - qIn) * 2); qcard.rotation.z = (1 - qIn) * 0.15 - 0.015; qcard.visible = t > 29.4;
  const h1 = ss(34.0, 34.8, t), h2 = ss(34.8, 35.4, t);
  hl.visible = t > 34.0; hl.position.set(5.0 - 3.3 + 2.95 * h1 + (h2 > 0 ? 0 : 0), 0.55 + 0.4, 0.14);
  hl.scale.set(Math.max(0.001, 5.9 * h1), 0.42, 1); hl.position.x = 1.7 + 2.95 * h1;
  hl.visible = false; // 두 줄 형광펜으로 대체 ↓
  hlA.visible = t > 34.0; hlA.scale.set(Math.max(0.001, 6.0 * h1), 0.4, 1); hlA.position.set(1.8 + 3.0 * h1, 0.70, 0.14);
  hlB.visible = t > 34.8; hlB.scale.set(Math.max(0.001, 4.2 * h2), 0.4, 1); hlB.position.set(1.8 + 2.1 * h2, 0.37, 0.14);

  // C: 감지기 떨어짐 → 토스트·연기·울림 → 불꽃·침묵
  const d = clamp((t - 42.5) / 0.65); det.position.set(15 + (t > 50.9 && t < 52.9 ? 0.03 * Math.sin(t * 90) : 0), 7 - (7 - 2.0) * backOut(d), 0.6); det.visible = t > 42.4;
  const alarm = t >= 50.9 && t < 52.9, blink = alarm ? (Math.floor((t - 50.9) / 0.22) % 2 === 0 ? 1 : 0.15) : 0;
  ledMat.emissiveIntensity = 4 * blink;
  rings.forEach((m, i) => { const t0 = 50.9 + i * 0.36, u = (t - t0) / 1.0, on = u >= 0 && u <= 1 && t0 < 52.9; m.material.opacity = on ? 0.85 * (1 - u) : 0; const k = 1 + u * 1.3; m.scale.set(k, k, 1); });
  const tin = ss(48.8, 49.4, t), tout = ss(54.4, 55.0, t);
  toast.position.set(11.3 - 8 * (1 - tin), -0.6 - 5 * tout, 0.45); toast.rotation.set(-0.06, 0.3 * (1 - tin) + 0.1, 0.04 * Math.sin(t * .8)); toast.visible = t > 48.7 && t < 55.1;
  pin("aToast", [12.6, 0.4], win(t, 49.4, 54.4));
  puffs.forEach((m, i) => { const { off, sw, ph } = m.userData, life = 1.9, lt = t - 49.3 - off, u = ((lt % life) + life) % life / life, alive = lt > 0 && t < 54.9;
    m.position.set(toast.position.x + 0.05 + Math.sin(ph + u * 4) * sw * (0.4 + u), toast.position.y + 0.5 + u * 2.6, 1.0 + i * 0.01); const k = 0.5 + u * 1.5; m.scale.set(k, k, 1);
    m.material.opacity = alive ? Math.sin(u * Math.PI) * 0.9 * (1 - ss(54.3, 54.9, t)) : 0; });
  const fin = ss(55.2, 55.9, t) * (1 - ss(57.6, 58.2, t)), fk = 1 + 0.06 * Math.sin(t * 13.1) + 0.04 * Math.sin(t * 7.3 + 1.3);
  fl.position.set(18.6, -1.6, 0.6); fl.scale.set(0.62 * fin, 0.62 * fin * fk, 0.62 * fin); fl.visible = fin > 0.001;
  for (const m of [fO, fM, fC]) m.material.uniforms.uT.value = t; fireLight.intensity = 14 * fin * fk;
  pin("aFire", [17.2, 0.6], win(t, 55.6, 57.6)); pin("aQuiet", [16.2, 3.3], win(t, 56.6, 57.6));

  // 저울: 헛경보(동전) 가벼움 vs 놓친 경보(돌) 무거움
  const bIn2 = ss(57.8, 58.3, t); bal.visible = t > 57.8; bal.scale.setScalar(Math.max(0.001, 0.8 * backOut((t - 57.8) / 0.45)));
  const cIn = clamp((t - 58.5) / 0.45), rIn = clamp((t - 61.4) / 0.5), tilt = 0.16 * (1 - Math.exp(-6 * Math.max(0, t - 61.9))) * (1 + 0.25 * Math.exp(-3 * Math.max(0, t - 61.9)) * Math.sin(Math.max(0, t - 61.9) * 9));
  beam.rotation.z = -tilt;
  coin.position.set(-2.1, 0.5 + 3 * (1 - backOut(cIn)) , 0); coin.visible = t > 58.5;
  rock.position.set(2.0, 0.6 + 3.5 * (1 - (rIn < 1 ? rIn * rIn : 1)), 0); rock.visible = t > 61.4;
  pin("aCoin", [11.6, -0.2], win(t, 58.9, 70)); pin("aRock", [17.4, -0.4], win(t, 62.0, 70));

  R.render(scene, cam);
}
const hlMat = new THREE.MeshBasicMaterial({ color: 0xe8b931, transparent: true, opacity: 0.4, depthWrite: false });
const hlA = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), hlMat), hlB = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), hlMat); scene.add(hlA, hlB);
window.addEventListener("hf-seek", e => renderAt(e.detail.time));
document.fonts.ready.then(() => { jg.fillStyle = "#f6f2ea"; jg.fillRect(0, 0, 340, 150); jg.fillStyle = "#2f8a5a"; jg.font = "700 64px NotoKR"; jg.fillText("판단", 170, 80); jt.needsUpdate = true; renderAt(0); });
renderAt(0);
</script>
</body></html>
