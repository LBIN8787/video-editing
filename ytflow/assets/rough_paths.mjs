// rough.js 로 손그림 도형의 SVG 경로를 만든다 (HyperFrames 카드용, 시드 고정 → 매번 같은 결과).
// 사용: node rough_paths.mjs <roughjs 경로>  < shapes.json  > paths.json
// shapes: [{type: rectangle|ellipse|line|linearPath, args: [...], opts: {seed, roughness, stroke, strokeWidth, fill, fillStyle, hachureGap}}]
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const rough = require(process.argv[2]);
const gen = rough.generator();
let buf = '';
process.stdin.on('data', (c) => (buf += c));
process.stdin.on('end', () => {
  const shapes = JSON.parse(buf);
  const out = shapes.map((s) => {
    const dr = gen[s.type](...s.args, s.opts || {});
    return gen.toPaths(dr).map((p) => ({ d: p.d, stroke: p.stroke, w: p.strokeWidth, fill: p.fill }));
  });
  process.stdout.write(JSON.stringify(out));
});
