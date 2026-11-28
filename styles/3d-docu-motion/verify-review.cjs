'use strict';
const {spawnSync} = require('node:child_process');
const {fs,path,args,file,tool,outDir,run,probe,load,fmt,ffStart,failed} = require('./common.cjs');
function requireIt(condition,msg) { if (!condition) throw Error(msg); }
const clip = s => s.replace('SHA256:','');
function packetList(ffprobe,name,interval) {
  const call = ['-v','error','-select_streams','a:0',...(interval ? ['-read_intervals',interval] : []),
    '-show_packets','-show_data_hash','sha256','-show_entries','packet=pts_time,data_hash','-of','json',name];
  return JSON.parse(run(ffprobe,call,true)).packets.map(p => [Number(p.pts_time),clip(p.data_hash)]);
}
function matchAudio(ffprobe,original,review,start,end) {
  const out = packetList(ffprobe,review);
  requireIt(out.length > 1500, 'Too few copied AAC packets');
  // Input seek can retain AAC preroll from the preceding video keyframe.
  // The MP4 edit list hides negative timestamps. Compare from the actual packet clock.
  const src = packetList(ffprobe,original,fmt(Math.max(0,start+out[0][0]-1))+'%'+fmt(end+1));
  const i = src.findIndex(([stamp,digest], k) => Math.abs(stamp - (start+out[0][0])) < .001 && digest === out[0]?.[1] &&
    out.every((p,j) => p[1] === src[k+j]?.[1]));
  requireIt(i >= 0, 'Review AAC is not a contiguous original packet subsequence');
  const error = Math.max(...out.map(([t],k) => Math.abs((src[i+k][0] - src[i][0]) - (t-out[0][0]))));
  requireIt(error < .000005, 'Unexpected AAC relative packet-clock drift');
  return {reviewPackets:out.length,firstOriginalPts:src[i][0],lastOriginalPts:src[i+out.length-1][0],
    firstReviewPts:out[0][0], lastReviewPts:out.at(-1)[0],maxRelativePtsErrorSeconds:error};
}
function ssim(ff,left,right,crop) {
  const f = (i,label) => '['+i+':v]'+(crop?'crop='+crop.join(':')+',':'')+
    'format=yuv420p,setpts=PTS-STARTPTS['+label+'];';
  const proc=spawnSync(ff,['-hide_banner','-nostdin','-v','info','-xerror','-i',left,'-i',right,
    '-filter_complex_threads','2','-filter_complex',f(0,'a')+f(1,'b')+'[a][b]ssim[out]',
    '-map','[out]','-frames:v','1','-an','-f','null','-'],{encoding:'utf8',windowsHide:true});
  if (proc.error) throw proc.error;
  const val=proc.stderr.match(/All:([0-9.]+)/);
  requireIt(proc.status===0 && val,proc.stderr);
  return Number(val[1]);
}
function main() {
  const a = args(process.argv.slice(2), ['source','plate','v4','v5','out-dir','recipe','ffmpeg','ffprobe','reference-plate','reference-v4','reference-v5'],
    ['source','plate','v4','v5','out-dir']);
  const cfg=load(a.recipe), ff=tool(a.ffmpeg,'ffmpeg'), fp=tool(a.ffprobe,'ffprobe');
  const input={source:file(a.source),plate:file(a.plate), v4:file(a.v4),v5:file(a.v5)};
  for (const k of ['reference-plate','reference-v4','reference-v5']) if (a[k]) input[k]=file(a[k]);
  const dir=outDir(a['out-dir']), zone=cfg.placement.qaZones, fps=cfg.inputs.plate.fps;
  const start=cfg.time.review.start;
  const audio=matchAudio(fp,input.source,input.v5,start,cfg.time.review.endExclusive);
  console.log('Original AAC packet match:',JSON.stringify(audio));
  const plateInfo=probe(fp,input.plate);
  requireIt(Number(plateInfo.streams[0].nb_frames)===cfg.inputs.plate.frames,'Unexpected V2 frame count');
  const decode = ['-i',input.plate,'-map','0:v:0','-an','-f','null','-'];
  run(ff,[...ffStart,...decode]);
  console.log('Rebuilt B decode OK');
  function still(name,frame,id) {
    const src=input[name], abs=['source','reference-v4','reference-v5'].includes(name);
    const out=path.join(dir,id+'-'+name+'.png');
    const t=abs ? fmt(start+frame/fps) : fmt(frame/fps);
    // Input seek is microsecond-based. Round down within 1 ms, so 1/30 s timestamps
    // with recurring decimals select the intended next frame instead of skipping it.
    const seek=fmt(Math.max(0,Number(t)-.001));
    run(ff,[...ffStart,'-ss',seek,'-i',src,'-map','0:v:0','-frames:v','1','-an','-update','1',out]);
    requireIt(fs.existsSync(out),'No extracted frame: '+id+'/'+name);
    return out;
  }
  const rows=[];
  for (const {id,frame} of cfg.time.qa) {
    const paths={};
    for(const name of ['source','plate','v4','v5','reference-plate','reference-v4','reference-v5'])
      if(input[name]) paths[name]=still(name,frame,id);
    const row={id,frame,excerptSec:Number(fmt(frame/fps)),sourceSec:Number(fmt(start+frame/fps)),
      sourceVsV5CardsAndHeader:ssim(ff,paths.source,paths.v5,zone.cardsAndHeader),
      sourceVsV5Subtitles:ssim(ff,paths.source,paths.v5,zone.subtitles),
      v4VsV5ZoomWing:ssim(ff,paths.v4,paths.v5,[280,390,136,530])};
    if (paths['reference-plate']) row.plateVsArchivedB=ssim(ff,paths.plate,paths['reference-plate']);
    if (paths['reference-v4']) row.v4PanelVsArchivedV4=ssim(ff,paths.v4,paths['reference-v4'],[1056,412,432,510]);
    if (paths['reference-v5']) row.v5ZoomVsArchivedV5=ssim(ff,paths.v5,paths['reference-v5'],zone.zoomInterior);
    requireIt(row.sourceVsV5CardsAndHeader > .97 && row.sourceVsV5Subtitles > .97,'Protected zone changed: '+id);
    if (id==='fiber' || id==='copper') requireIt(row.v4VsV5ZoomWing < .95,'Missing V5 enlarged panel: '+id);
    else requireIt(row.v4VsV5ZoomWing > .96,'Unexpected overlay outside V5: '+id);
    rows.push(row);
    console.log(JSON.stringify(row));
  }
  const transition=[];
  for (const frame of [321,322,571,572,573]) {
    const id='edge-'+frame, small=still('v4',frame,id), enlarged=still('v5',frame,id);
    const score=ssim(ff,small,enlarged,[280,390,136,530]);
    const edge={frame,sourceSec:Number(fmt(start+frame/fps)),v4VsV5ZoomWing:score};
    if (input['reference-v4'] && input['reference-v5']) {
      edge.archivedV4VsV5ZoomWing=ssim(ff,still('reference-v4',frame,id),still('reference-v5',frame,id),[280,390,136,530]);
      requireIt((edge.archivedV4VsV5ZoomWing<.96)===(score<.96),'Archived V5 zoom boundary differs at frame '+frame);
    }
    transition.push(edge);
    console.log(JSON.stringify(edge));
  }
  const report={audio,plateDecode:'passed; ffmpeg -xerror ... -f null -',frames:rows,transition};
  fs.writeFileSync(path.join(dir,'verify-report.json'),JSON.stringify(report,null,2)+'\n',{flag:'wx'});
}
try { main(); } catch(e) { failed(e); }
