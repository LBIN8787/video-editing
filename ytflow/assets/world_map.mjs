// 세계 지도 SVG 경로 (world-atlas 2.0.2 · d3-geo · topojson-client) + 지점 좌표 투영. 지도 여정 연출(journey)·위치 미니맵(locator)용.
// 사용: echo '{"W":1920,"H":1080,"points":{"kansas":[-96.8,39.1]},"projection":"mercator","center":[10,22]}' | node world_map.mjs <node_modules>
//  → {"countries":[{"id":"840","name":"United States of America","d":"M..."}],"points":{"kansas":[x,y]},"graticule":"M...","frame":[x0,y0,x1,y1]}
// projection: mercator(기본, 직사각형 — 화면을 꽉 채움) | equirect | natural(예전 타원형)
import { createRequire } from 'module';
const nm = process.argv[2];
const require = createRequire(nm + '/');
const topo = require(nm + '/world-atlas/countries-50m.json');
const { feature } = require(nm + '/topojson-client');
const d3 = require(nm + '/d3-geo');
let buf = '';
process.stdin.on('data', (c) => (buf += c));
process.stdin.on('end', () => {
  const q = JSON.parse(buf);
  const fc = feature(topo, topo.objects.countries);
  const kind = q.projection || 'mercator';
  let proj;
  if (kind === 'natural') {
    proj = d3.geoNaturalEarth1().fitExtent([[20, 20], [q.W - 20, q.H - 20]], { type: 'Sphere' });
  } else {
    // 직사각형: 지구 한 바퀴 = 화면 너비 × (scale 배). 남극은 화면 밖으로.
    const k = q.scale || 1.0;
    proj = (kind === 'equirect' ? d3.geoEquirectangular() : d3.geoMercator())
      .scale((q.W * k) / (2 * Math.PI)).center(q.center || [10, 22]).translate([q.W / 2, q.H / 2]);
  }
  const path = d3.geoPath(proj);
  const countries = fc.features
    .filter((f) => f.properties.name !== 'Antarctica')
    .map((f) => ({ id: f.id, name: f.properties.name, d: path(f) }))
    .filter((c) => c.d);
  const points = {};
  for (const [k, ll] of Object.entries(q.points || {})) points[k] = proj(ll).map((v) => Math.round(v * 10) / 10);
  const grat = d3.geoGraticule().extent([[-180, -70], [180.01, 80.01]]).step([20, 20]);
  const tl = proj([-180, 80]), br = proj([180, -70]);
  process.stdout.write(JSON.stringify({ countries, points, graticule: path(grat()), sphere: path({ type: 'Sphere' }),
    frame: [tl[0], tl[1], br[0], br[1]], projection: kind }));
});
