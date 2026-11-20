// 그래픽 층 프레임 찍기: node broll_frames.mjs <frames.json> <overlay.html>  → 투명 PNG 를 stdout 으로 이어서 보냄
import { createRequire } from "module";
import fs from "fs";
const require = createRequire(import.meta.url);
let pw;
try { pw = require("playwright"); } catch { pw = require(require.resolve("playwright", { paths: ["/opt/node22/lib/node_modules", process.cwd()] })); }
const [, , framesFile, htmlFile] = process.argv;
const job = JSON.parse(fs.readFileSync(framesFile, "utf8"));
const br = await pw.chromium.launch();
const pg = await br.newPage({ viewport: { width: 1920, height: 1080 } });
await pg.goto("file://" + htmlFile);
await pg.evaluate(() => document.fonts.ready);
const write = (b) => new Promise((ok) => (process.stdout.write(b) ? ok() : process.stdout.once("drain", ok)));
for (let i = 0; i < job.frames.length; i++) {
  const [si, t, sub] = job.frames[i];
  const s = job.scenes[si];
  await pg.evaluate(([sc, t, B, D, sub]) => R(sc, t, B, D, sub), [s.data, t, s.B, s.D, sub]);
  await write(await pg.screenshot({ type: "png", omitBackground: true }));
  if (i % 300 === 0) process.stderr.write(`  ${i}/${job.frames.length}\n`);
}
await br.close();
