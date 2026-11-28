'use strict';
const {fs,path,args,file,tool,outDir,run,probe,sha,load,fmt,ffStart,failed} = require('./common.cjs');

function demand(condition, msg) { if (!condition) throw Error(msg); }
function checkVideo(info,w,h,fps,n) {
  const v = info.streams.find(x => x.codec_type === 'video');
  demand(v && v.width === w && v.height === h && v.r_frame_rate === fps+'/1'
    && v.avg_frame_rate === fps+'/1' && Number(v.start_time) === 0
    && Number(v.nb_frames) === n && v.pix_fmt === 'yuv420p', 'Unexpected video format or time base');
}
function build(cfg, offset) {
  const p = cfg.placement, t = cfg.time;
  const n = fmt, delta = v => n(v-offset);
  const spec = p => 'crop='+p.crop.join(':')+',scale='+p.scale.join(':')+':flags=lanczos'+
    ',drawbox=x=0:y=0:w=iw:h=ih:color=0x'+p.border.color+':t='+p.border.width;
  for (const key of ['v4','v5']) {
    const {crop,scale,position,border} = p[key];
    demand(crop.length === 4 && scale.length === 2 && position.length === 2 &&
      [...crop,...scale,...position,border.width].every(v => Number.isInteger(v) && v >= 0) &&
      /^[0-9a-f]{6}$/i.test(border.color),'Invalid placement: '+key);
  }
  const cut = t => '[1:v]trim=start='+n(t.plateIn)+':end='+n(t.plateOutExclusive);
  const set = t => 'setpts=PTS-STARTPTS+'+delta(t.start)+'/TB';
  const overlay = (p,t) => '[0:v][p]overlay='+p.position.join(':')+
    ":enable='gte(t,"+delta(t.start)+")*lt(t,"+delta(t.endExclusive)+")':eof_action=pass:repeatlast=0[out]";
  const fade = (op,[start,end]) => 'fade=t='+op+':st='+n(start)+':d='+n(end-start)+':alpha=1';
  const v4 = [cut(t.v4), spec(p.v4), 'format=yuva420p', fade('in',t.v4.fadeIn),fade('out',t.v4.fadeOut),set(t.v4)].join(',')+
    '[p];'+overlay(p.v4,t.v4);
  const v5 = [cut(t.v5), set(t.v5), spec(p.v5)].join(',')+'[p];'+overlay(p.v5,t.v5);
  return {v4,v5};
}
function audioHash(ff,p) {
  return run(ff,['-hide_banner','-nostdin','-v','error','-i',p,'-map','0:a:0','-c:a','copy','-f','hash','-'],true).trim();
}
async function main() {
  const a = args(process.argv.slice(2), ['mode','source','plate','out-dir','recipe','ffmpeg','ffprobe'], ['mode','source','plate','out-dir']);
  const mode = a.mode;
  demand(mode === 'review' || mode === 'full','--mode must be review or full');
  const cfg = load(a.recipe), src = cfg.inputs.original.video, b = cfg.inputs.plate;
  const ff = tool(a.ffmpeg,'ffmpeg'), fp = tool(a.ffprobe,'ffprobe');
  const original = file(a.source), plate = file(a.plate);
  const oi = probe(fp,original);
  checkVideo(oi,src.width,src.height,src.fps,src.frames);
  demand(oi.streams.some(s => s.codec_type === 'audio' && s.codec_name === 'aac'),'Expected original AAC audio');
  demand(await sha(original) === cfg.inputs.original.sha256,'Original SHA-256 mismatch: select the exact input final.mp4');
  checkVideo(probe(fp,plate),b.width,b.height,b.fps,b.frames);
  const offset = mode === 'review' ? cfg.time.review.start : 0;
  const limit = mode === 'review' ? ['-t',fmt(cfg.time.review.endExclusive-offset)] : [];
  const filters = build(cfg,offset);
  const dir = outDir(a['out-dir']), mid = path.join(dir,mode+'-V4.mp4'), output = path.join(dir,mode+'-V5.mp4');
  const im = cfg.pipeline;
  const [range,space,primaries,trc] = im.color;
  const enc = ['-c:v',im.videoCodec,'-threads',String(im.threads),'-preset',im.preset,'-crf',String(im.crf),
    '-pix_fmt',im.format,'-color_range',range,'-colorspace',space,'-color_primaries',primaries,'-color_trc',trc,
    '-c:a','copy','-movflags','+faststart'];
  const commands = [];
  function render(stage,base,dst,seek) {
    const argv = [...ffStart,...seek,'-i',base,'-i',plate,'-filter_complex_threads','2','-filter_complex',filters[stage],
      '-map','[out]','-map',cfg.inputs.original.audio.selector,...limit,...enc,dst];
    commands.push({bin:ff,argv});
    console.log(stage+' '+mode+' -> '+dst);
    run(ff,argv);
  }
  render('v4',original,mid,offset ? ['-ss',fmt(offset)] : []);
  render('v5',mid,output,[]);
  const info = probe(fp,output);
  checkVideo(info,src.width,src.height,src.fps,mode === 'review' ? cfg.time.review.frames : src.frames);
  const audio = audioHash(ff,output);
  if (mode === 'full') demand(audio === 'SHA256='+cfg.inputs.original.audio.payloadSha256,'Full audio payload hash mismatch');
  const decode = [...ffStart,'-i',output,'-map','0:v:0','-map','0:a:0','-f','null','-'];
  commands.push({bin:ff,argv:decode});
  console.log('Decoding V5 video and audio to null');
  run(ff,decode);
  const report = {mode,audio,plateSha256:await sha(plate),probe:info,commands};
  fs.writeFileSync(path.join(dir,'compose-report.json'),JSON.stringify(report,null,2)+'\n',{flag:'wx'});
  console.log('Complete: '+output+' | '+audio);
}
main().catch(failed);
