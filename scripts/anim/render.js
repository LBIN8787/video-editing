// 장면 html → 무음 mp4 (프레임마다 seek → 스크린샷 → ffmpeg). node render.js scene.html out.mp4 [start] [end]
const { chromium } = require('playwright'); const { pathToFileURL } = require('url'); const { spawn } = require('child_process');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto(pathToFileURL(process.argv[2]).href); await p.waitForTimeout(1500);
  await p.evaluate(() => document.fonts.ready);
  const total = await p.evaluate(() => window.TOTAL), fps = 30;
  const a = Number(process.argv[4] || 0), z = Number(process.argv[5] || total), n = Math.ceil((z - a) * fps);
  const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '15', '-tune', 'animation', '-pix_fmt', 'yuv420p', process.argv[3]], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let i = 0; i < n; i++) { await p.evaluate(t => window.seek(t), a + i / fps);
    const buf = await p.screenshot({ type: 'jpeg', quality: 94 }); if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 300 === 0) console.log('frame', i, '/', n); }
  ff.stdin.end(); await new Promise(r => ff.on('close', r)); await b.close(); })();
