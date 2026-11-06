// 미국 주 경계 SVG 경로 (us-atlas 3.0.1 · d3-geo · topojson-client). 지도 장면용으로 한 번 계산해 캐시한다.
// 사용: node us_states.mjs <node_modules 경로> <폭> <높이>  > states.json   ({"Texas": "M...", ...})
import { createRequire } from 'module';
const [nm, W, H] = process.argv.slice(2);
const require = createRequire(nm + '/');
const topo = require(nm + '/us-atlas/states-10m.json');
const { feature } = require(nm + '/topojson-client');
const d3 = require(nm + '/d3-geo');
const fc = feature(topo, topo.objects.states);
const proj = d3.geoAlbersUsa().fitSize([+W, +H], fc);
const path = d3.geoPath(proj);
const out = {};
for (const f of fc.features) {
  const d = path(f);
  if (d) out[f.properties.name] = { d, c: path.centroid(f).map((v) => Math.round(v)) };
}
process.stdout.write(JSON.stringify(out));
