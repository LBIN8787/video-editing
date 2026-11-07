// 세계 지도 SVG 경로 (world-atlas 2.0.2 · d3-geo · topojson-client) + 지점 좌표 투영. 지도 여정 연출(journey)용.
// 사용: echo '{"W":1920,"H":1080,"points":{"kansas":[-96.8,39.1]}}' | node world_map.mjs <node_modules>
//  → {"countries":[{"id":"840","d":"M..."}],"points":{"kansas":[x,y]}}
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
  const proj = d3.geoNaturalEarth1().fitExtent([[20, 20], [q.W - 20, q.H - 20]], { type: 'Sphere' });
  const path = d3.geoPath(proj);
  const countries = fc.features.map((f) => ({ id: f.id, name: f.properties.name, d: path(f) })).filter((c) => c.d);
  const points = {};
  for (const [k, ll] of Object.entries(q.points || {})) points[k] = proj(ll).map((v) => Math.round(v * 10) / 10);
  process.stdout.write(JSON.stringify({ countries, points, graticule: path(d3.geoGraticule10()), sphere: path({ type: 'Sphere' }) }));
});
