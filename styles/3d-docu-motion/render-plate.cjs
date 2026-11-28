'use strict';
const {spawn} = require('node:child_process');
const {Readable} = require('node:stream');
const {pipeline} = require('node:stream/promises');
const {pathToFileURL} = require('node:url');
const {launch,wait} = require('./cdp.cjs');
const {fs,path,args,file,tool,outDir,probe,load,ffStart,failed} = require('./common.cjs');

async function main() {
  const a = args(process.argv.slice(2), ['browser','out-dir','scene','recipe','ffmpeg','ffprobe'], ['browser','out-dir']);
  const cfg = load(a.recipe), plate = cfg.inputs.plate;
  const browser = file(a.browser), scene = file(a.scene || path.join(__dirname,plate.scene));
  const ff = tool(a.ffmpeg,'ffmpeg'), fp = tool(a.ffprobe,'ffprobe');
  if (typeof WebSocket !== 'function') throw Error('Node 22+ with built-in WebSocket required');
  const dir = outDir(a['out-dir']), mp4 = path.join(dir,'v2-B-regenerated.mp4');
  const page = await launch(browser, path.join(dir,'chromium-profile'), plate.width, plate.height);
  let proc;
  try {
    await page.call('Page.enable');
    const nav = await page.call('Page.navigate',{url:pathToFileURL(scene).href});
    if (nav.errorText) throw Error(nav.errorText);
    for (let j=0;j<120;j++) {
      if (await page.evaluate('typeof window.frame === "function"')) break;
      if (j === 119) throw Error('Scene did not initialize (local WebGL2 required)');
      await wait(100);
    }
    const props = await page.evaluate('checkProps()');
    console.log('Scene initialized:',JSON.stringify(props));
    async function* frames() {
      for (let i = 0; i < plate.frames; ++i) {
        const jpg = Buffer.from(await page.evaluate('frame(' + (i / plate.fps) + ')'), 'base64');
        if (jpg[0] !== 255 || jpg[1] !== 216) throw Error('Unexpected image format at frame ' + i);
        yield jpg;
        if (i % 90 === 0 || i === plate.frames - 1) console.log('WebGL frame ' + i + '/' + (plate.frames - 1));
      }
    }
    const size = plate.width + ':' + plate.height;
    proc = spawn(ff,[...ffStart,'-f','image2pipe','-framerate',String(plate.fps),'-vcodec','mjpeg','-i','pipe:0',
      '-map','0:v:0','-an','-vf','scale='+size+':in_range=pc:out_range=tv:in_color_matrix=bt601:out_color_matrix=bt709,format=yuv420p,setsar=1',
      '-frames:v',String(plate.frames),'-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p',
      '-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',
      '-map_metadata','-1','-movflags','+faststart',mp4],{windowsHide:true,stdio:['pipe','inherit','inherit']});
    const finished = new Promise((resolve,reject) => {
      proc.once('error',reject);
      proc.once('close',(code,signal) => code === 0 ? resolve() : reject(Error('Plate encode: '+(code ?? signal))));
    });
    await Promise.all([pipeline(Readable.from(frames()),proc.stdin),finished]);
    const info = probe(fp,mp4);
    const v = info.streams[0];
    if (info.streams.length !== 1 || Number(v.nb_frames) !== plate.frames || v.width !== plate.width || v.height !== plate.height) throw Error('Unexpected plate inventory');
    fs.writeFileSync(path.join(dir,'plate-probe.json'),JSON.stringify({scene:props,probe:info},null,2)+'\n',{flag:'wx'});
    console.log('Complete: '+mp4);
  } finally { page.close(); if (proc && proc.exitCode === null) proc.kill(); }
}
main().catch(failed);
