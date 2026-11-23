"""어두운 스튜디오 3D 장면 (studio3d) — motion-metaphor v2 (docs/22: 레퍼런스 재분석).

검은 무대 + 반사 바닥 + 위에서 떨어지는 한 줄기 빛 + 흰·회색 무광 물체 한두 개. 화면 글자는 최소(물체 위 이름표만).
three.js(MIT, tools/external.json 고정)로 그리고, GSAP 시간축의 t 로 매 프레임을 다시 계산한다(결정적 렌더, 탐색 안전).

장면 type "studio3d", preset:
  stack  왼쪽에 큰 덩어리 하나(=공급), 오른쪽에 작은 상자가 하나씩 떨어져 쌓임(=수요) — "A 보다 B 가 N배"
         {"preset":"stack","left":"공급 가능한 용량","right":"수요","n":10}
  swap   두 타일: 하나는 어두워지며 가라앉고, 다른 하나는 떠오르며 빛남 — "A 대신 B"
         {"preset":"swap","out":"무담보 채권","in":"고객 선지급금"}
  glow   가운데 칩(슬랩)이 천천히 돌고, 위로 꼬리표가 떠오르며 빛이 세짐 — "이것의 값이 오른다"
         {"preset":"glow","object":"옛 세대 GPU","tag":"+30~50%"}
박자 시각(beats)에 맞춰 움직임이 시작된다: 첫 박자 = 등장, 둘째 박자 = 핵심 동작.
"""
from __future__ import annotations

import json
import shutil

from .. import config

THREE_DIR = config.ROOT / "tools" / "hyperframes" / "node_modules" / "three"


def available() -> bool:
    return (THREE_DIR / "build" / "three.module.min.js").exists()


def _copy_assets(work):
    a = work / "assets" / "three"
    (a / "env").mkdir(parents=True, exist_ok=True)
    for src, dst in ((THREE_DIR / "build" / "three.module.min.js", a / "three.module.min.js"),
                     (THREE_DIR / "examples" / "jsm" / "environments" / "RoomEnvironment.js", a / "env" / "RoomEnvironment.js")):
        if not dst.exists():
            shutil.copy(src, dst)


SCENE_JS = r"""
import * as THREE from "three";
import { RoomEnvironment } from "three/env/RoomEnvironment.js";
const P = window.__s3d;
const canvas = document.getElementById("s3d");
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(1); renderer.setSize(1920, 1080, false);
renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.0;
renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
const scene = new THREE.Scene();
scene.background = new THREE.Color("#07080b");
scene.fog = new THREE.Fog("#07080b", 14, 34);
const pm = new THREE.PMREMGenerator(renderer);
scene.environment = pm.fromScene(new RoomEnvironment(), 0.04).texture;
const camera = new THREE.PerspectiveCamera(32, 1920 / 1080, 0.1, 100);
// 바닥: 어두운 반광택 (빛 웅덩이가 비침)
const floor = new THREE.Mesh(new THREE.PlaneGeometry(80, 80),
  new THREE.MeshStandardMaterial({ color: "#121419", roughness: 0.32, metalness: 0.35, envMapIntensity: 0.25 }));
floor.rotation.x = -Math.PI / 2; floor.receiveShadow = true; scene.add(floor);
scene.add(new THREE.AmbientLight("#ffffff", 0.08));
const spot = new THREE.SpotLight("#ffffff", 260, 40, Math.PI / 7, 0.55, 1.6);
spot.position.set(0, 13, 3); spot.castShadow = true; spot.shadow.mapSize.set(2048, 2048); spot.shadow.radius = 6;
scene.add(spot); scene.add(spot.target);
const rim = new THREE.DirectionalLight("#9fb7ff", 0.9); rim.position.set(-6, 5, -8); scene.add(rim);
const white = () => new THREE.MeshStandardMaterial({ color: "#e8e8e6", roughness: 0.62, metalness: 0.0, flatShading: true });
const grey = () => new THREE.MeshStandardMaterial({ color: "#8d9096", roughness: 0.7, metalness: 0.05, flatShading: true });

function label(text, opts = {}) {   // 물체 위 이름표: 캔버스에 글자를 그려 판에 붙임
  const c = document.createElement("canvas"); c.width = 1024; c.height = 256;
  const g = c.getContext("2d");
  g.font = `${opts.weight || 800} ${opts.size || 110}px sans-x`;
  const w = Math.min(980, g.measureText(text).width + 120);
  g.fillStyle = opts.bg || "rgba(255,255,255,0.94)";
  const x = (1024 - w) / 2, r = 40; g.beginPath(); g.roundRect(x, 38, w, 180, r); g.fill();
  g.fillStyle = opts.color || "#111318"; g.textAlign = "center"; g.textBaseline = "middle"; g.fillText(text, 512, 132);
  const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 8;
  const m = new THREE.Mesh(new THREE.PlaneGeometry(4, 1), new THREE.MeshBasicMaterial({ map: tex, transparent: true, toneMapped: false }));
  return m;
}
const clamp = (v) => Math.max(0, Math.min(1, v));
const ease = (v) => 1 - Math.pow(1 - clamp(v), 3);
const bounce = (x) => { x = clamp(x); const n = 7.5625, d = 2.75;
  if (x < 1 / d) return n * x * x; if (x < 2 / d) return n * (x -= 1.5 / d) * x + 0.75;
  if (x < 2.5 / d) return n * (x -= 2.25 / d) * x + 0.9375; return n * (x -= 2.625 / d) * x + 0.984375; };
const B0 = P.beats[0] || 0, B1 = P.beats[1] ?? (P.dur * 0.45);
const parts = {};

if (P.preset === "stack") {
  // 같은 크기 상자: 왼쪽 1개(공급) vs 오른쪽 n개(수요) — 'N배'가 눈으로 보이게
  const big = new THREE.Mesh(new THREE.BoxGeometry(1.0, 1.0, 1.0), white()); big.castShadow = true; big.position.set(-3.6, 0.5, 0); scene.add(big);
  const lb = label(P.left); lb.scale.setScalar(0.8); lb.position.set(-3.6, 1.75, 0.2); scene.add(lb);
  const lr = label(P.right); lr.scale.setScalar(0.8); lr.position.set(3.3, 2.75, 0.2); scene.add(lr);
  const cubes = [];
  for (let i = 0; i < P.n; i++) {
    const m = new THREE.Mesh(new THREE.BoxGeometry(1.0, 1.0, 1.0), white()); m.castShadow = true; m.receiveShadow = true;
    const col = i % 5, row = Math.floor(i / 5);
    m.userData.home = new THREE.Vector3(1.15 + col * 1.06 + (row % 2) * 0.2, 0.5 + row * 1.0, (i % 2) * 0.2);
    m.userData.rot = (i * 0.37) % 0.4 - 0.2; scene.add(m); cubes.push(m);
  }
  parts.draw = (t) => {
    big.position.y = 0.5 + (1 - ease((t - B0) / 0.7)) * 6; big.rotation.y = 0.35;
    lb.material.opacity = ease((t - B0 - 0.5) / 0.4); lr.material.opacity = ease((t - B1) / 0.4);
    cubes.forEach((m, i) => {
      const span = Math.max(0.08, Math.min(0.2, (P.dur - B1 - 1.2) / Math.max(1, P.n)));   // 둘째 박자 안에 다 쌓이게
      const t0 = B1 + 0.1 + i * span, k = bounce((t - t0) / 0.5);
      m.visible = t >= t0 - 0.05; const h = m.userData.home;
      m.position.set(h.x, h.y + (1 - k) * 7, h.z); m.rotation.y = m.userData.rot + (1 - k) * 0.8;
    });
    camera.position.set(0.4 + 0.5 * ease(t / P.dur), 3.6, 12.5 - 1.0 * ease(t / P.dur)); camera.lookAt(0.6, 1.2, 0);
    spot.target.position.set(0.5, 0, 0);
  };
} else if (P.preset === "swap") {
  const mk = (txt, x, bright) => {
    const g = new THREE.BoxGeometry(3.2, 3.2, 0.5); const m = new THREE.Mesh(g, bright ? white() : grey());
    m.castShadow = true; m.position.set(x, 1.8, 0); scene.add(m);
    const l = label(txt, { size: 96 }); l.scale.set(0.8, 0.8, 0.8); l.position.set(x, 1.8, 0.27); scene.add(l);
    return { m, l };
  };
  const A = mk(P.out, -2.3, false), Bt = mk(P.in, 2.3, true);
  const glow = new THREE.PointLight("#ffd27a", 0, 9); glow.position.set(2.3, 2.5, 2.5); scene.add(glow);
  parts.draw = (t) => {
    const a = ease((t - B0) / 0.8), s = ease((t - B1) / 1.2);
    A.m.position.y = 1.8 - s * 1.55 + (1 - a) * 5; A.l.position.y = A.m.position.y;
    A.m.material.color.set(new THREE.Color("#8d9096").lerp(new THREE.Color("#2a2c31"), s)); A.l.material.opacity = 1 - 0.75 * s;
    Bt.m.position.y = 1.8 + s * 0.9 + (1 - a) * 5; Bt.l.position.y = Bt.m.position.y; Bt.m.rotation.y = -0.25 + 0.25 * s; Bt.l.rotation.y = Bt.m.rotation.y;
    glow.intensity = 40 * s;
    camera.position.set(0, 3.4, 12.5 - 1.0 * ease(t / P.dur)); camera.lookAt(0, 2.0, 0);
  };
} else {   // glow
  const slab = new THREE.Group();
  const body = new THREE.Mesh(new THREE.BoxGeometry(3.6, 0.5, 3.6), white()); body.castShadow = true; slab.add(body);
  for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) {
    const pin = new THREE.Mesh(new THREE.BoxGeometry(0.55, 0.12, 0.55), grey()); pin.position.set(-1.2 + i * 0.8, 0.3, -1.2 + j * 0.8); slab.add(pin);
  }
  slab.position.set(0, 1.0, 0); scene.add(slab);
  const name = label(P.object, { size: 96 }); name.position.set(0, 0.0, 2.6); name.rotation.x = -0.35; scene.add(name);
  const tag = label(P.tag, { size: 130, bg: "rgba(255,210,122,0.97)" }); tag.position.set(0, 3.6, 0.5); scene.add(tag);
  const up = new THREE.PointLight("#ffd27a", 0, 10); up.position.set(0, 2.6, 1.5); scene.add(up);
  parts.draw = (t) => {
    const a = ease((t - B0) / 0.8), s = ease((t - B1) / 1.0);
    slab.position.y = 1.0 + (1 - a) * 4 + s * 0.35; slab.rotation.y = 0.5 + t * 0.18; slab.rotation.x = 0.12;
    tag.position.y = 3.0 + s * 0.8; tag.material.opacity = s; up.intensity = 35 * s;
    spot.intensity = 200 + 120 * s;
    camera.position.set(Math.sin(t * 0.05) * 1.2, 4.2, 11.5); camera.lookAt(0, 1.6, 0);
  };
}
function drawAt(t) { parts.draw(t); renderer.render(scene, camera); }
window.__draw3d = drawAt;
document.fonts.load("110px sans-x").then(() => {
  // 글자 판은 글꼴이 로드된 뒤 다시 그림
  scene.traverse((o) => { if (o.material && o.material.map && o.material.map.isCanvasTexture) o.material.map.needsUpdate = true; });
  drawAt(window.__s3dT || 0);
  for (const f of [0.3, 0.6, 0.9]) drawAt(P.dur * f);
  drawAt(window.__s3dT || 0); renderer.getContext().finish();
  window.__s3dReady && window.__s3dReady();
});
"""


def s_studio3d(D, sc, bt, dur):
    """3D 무대 장면. hybrid 의 HDoc 안에 캔버스 + 모듈 스크립트를 넣고, 메인 시간축이 t 를 넘겨 매 프레임을 다시 그린다."""
    work = getattr(D, "_work", None)
    if work is not None:
        _copy_assets(work)
    beats = [round(b[0], 2) for b in bt]
    P = {"preset": sc.get("preset", "stack"), "beats": beats, "dur": round(dur, 2),
         "left": sc.get("left", ""), "right": sc.get("right", ""), "n": int(sc.get("n", 10)),
         "out": sc.get("out", ""), "in": sc.get("in", ""), "object": sc.get("object", ""), "tag": sc.get("tag", "")}
    D.media.append('<canvas id="s3d" width="1920" height="1080" style="position:absolute;inset:0;width:1920px;height:1080px"></canvas>')
    D.head_extra = ('<script type="importmap">{"imports":{"three":"./assets/three/three.module.min.js","three/env/":"./assets/three/env/"}}</script>'
                    f'<script>window.__s3d={json.dumps(P, ensure_ascii=False)};window.__hf=window.__hf||{{}};window.__hf.buildReady=window.__hf.buildReady||{{}};'
                    'window.__hf.buildReady.s3d=new Promise(function(r){window.__s3dReady=r;});'
                    'window.addEventListener("hf-seek",function(e){var d=e&&e.detail;if(d&&typeof d.time==="number"){window.__s3dT=d.time;window.__draw3d&&window.__draw3d(d.time);}});</script>'
                    f'<script type="module">{SCENE_JS}</script>')
    D.js.append(f'(function(){{const S3={{t:0}};tl.fromTo(S3,{{t:0}},{{t:{dur:.2f},duration:{dur:.2f},ease:"none",'
                f'onUpdate:function(){{window.__s3dT=S3.t;window.__draw3d&&window.__draw3d(S3.t);}}}},0);}})();')
    if sc.get("label"):
        D.label(sc["label"], dark=True)
    D.sfx.append(("whoosh-short", beats[1] if len(beats) > 1 else 0.5))


def register():
    from . import hybrid
    hybrid.RENDER["studio3d"] = s_studio3d
