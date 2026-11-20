// 그래픽 층 프레임 찍기: node broll_frames.mjs <frames.json> <overlay.html>  → 투명 PNG 를 stdout 으로 이어서 보냄
import { createRequire } from "module";
import fs from "fs";
import { pathToFileURL } from "node:url";
const require = createRequire(import.meta.url);
let pw;
try { pw = require("playwright"); } catch { pw = require(require.resolve("playwright", { paths: ["/opt/node22/lib/node_modules", process.cwd()] })); }
const [, , framesFile, htmlFile, format] = process.argv;
const job = JSON.parse(fs.readFileSync(framesFile, "utf8"));
const flat = format === "jpeg";
const br = await pw.chromium.launch({
  executablePath: process.env.YTFLOW_CHROMIUM || undefined,
  args: flat ? ["--disable-frame-rate-limit", "--disable-gpu-vsync"] : [],
});
const pg = await br.newPage({ viewport: { width: 1920, height: 1080 } });
await pg.goto(pathToFileURL(htmlFile).href);
if (flat) {
  await pg.evaluate(async (scenes) => {
    document.body.style.background = "black";
    const sources = new Set();
    for (const { data, B, D } of scenes) {
      R(data, D / 2, B, D, "");
      for (const img of document.querySelectorAll("#root img")) sources.add(img.src);
    }
    await Promise.all([...sources].map((src) => {
      const img = new Image();
      img.src = src;
      return img.decode();
    }));
    await document.fonts.ready;
  }, job.scenes);
} else {
  await pg.evaluate(() => document.fonts.ready);
}
const cdp = flat ? await pg.context().newCDPSession(pg) : null;
const write = (b) => new Promise((ok) => (process.stdout.write(b) ? ok() : process.stdout.once("drain", ok)));
for (let i = 0; i < job.frames.length; i++) {
  const [si, t, sub] = job.frames[i];
  const s = job.scenes[si];
  await pg.evaluate(([sc, t, B, D, sub]) => R(sc, t, B, D, sub), [s.data, t, s.B, s.D, sub]);
  if (cdp) {
    const frame = await cdp.send("Page.captureScreenshot", { format: "jpeg", quality: 94, optimizeForSpeed: true });
    await write(Buffer.from(frame.data, "base64"));
  } else {
    await write(await pg.screenshot({ type: "png", omitBackground: true }));
  }
  if (i % 300 === 0) process.stderr.write(`  ${i}/${job.frames.length}\n`);
}
await br.close();
