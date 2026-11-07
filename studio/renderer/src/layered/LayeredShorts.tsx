import React,{useEffect,useState} from 'react';
import {AbsoluteFill,Img,Series,staticFile,useCurrentFrame,delayRender,continueRender,cancelRender} from 'remotion';
import {Audio} from '@remotion/media';
import type {Caption} from '@remotion/captions';
import type {VisualScene} from '../template/ShortsGuideTemplate';
import {VisualBlock} from './VisualBlocks';
import {BasicCaptions} from '../basic-captions';
type ContentScene=Omit<VisualScene,'frames'>;
type Cut={scene_id:string;start_frame:number;end_frame:number;transition:string;reason:string};
type Point={scene_id:string;from_frame:number;to_frame:number;focus_index:number;target:string;label:string;method:string};
type Asset={image:string;label:string;focus_regions:{[key:string]:number[]}};
export type LayeredProps={
 content:{episode:string;source:string;audio:string;captions:Caption[];scenes:ContentScene[]};
 edit_points:{fps:number;cuts:Cut[]};
 emphasis:{points:Point[]};
 skin:{id:string;name:string;palette:{[key:string]:string};background:string;asset_overrides:{[key:string]:Asset}};
};
const Fonts=()=>{const [h]=useState(()=>delayRender('Layered font gate'));useEffect(()=>{Promise.all([document.fonts.load('400 40px NotoLayers'),document.fonts.load('900 76px NotoLayers')]).then(()=>continueRender(h)).catch(cancelRender)},[h]);return <style>{`@font-face{font-family:NotoLayers;src:url('${staticFile('fonts/NotoSansCJKkr-Regular.otf')}');font-weight:100 500}@font-face{font-family:NotoLayers;src:url('${staticFile('fonts/NotoSansCJKkr-Bold.otf')}');font-weight:600 1000}`}</style>};
const Shot=({scene,cut,points,skin,source}:{scene:ContentScene;cut:Cut;points:Point[];skin:LayeredProps['skin'];source:string})=>{
 const frame=useCurrentFrame();const point=points.find(p=>frame>=p.from_frame&&frame<p.to_frame);const asset=skin.asset_overrides[scene.id];const region=asset?.focus_regions[String(point?.focus_index)];
 return <AbsoluteFill style={{color:'var(--ink)'}}>
 <div style={{position:'absolute',left:80,top:110,fontSize:30,fontWeight:800}}>● AI 실전노트</div>
 <div style={{position:'absolute',left:80,top:180,fontSize:26,color:'var(--muted)',fontWeight:700}}>{scene.step}</div>
 <div style={{position:'absolute',left:80,top:242,width:850,fontSize:76,fontWeight:900,lineHeight:1.24,letterSpacing:-4}}>{scene.titleLines.map((s,i)=><div key={i}>{s}</div>)}</div>
 {point?<div style={{position:'absolute',left:92,top:449,fontSize:24,color:'var(--muted)',fontWeight:700}}>지금 볼 곳: {point.label}</div>:null}
 <div style={{position:'absolute',left:80,top:495,width:850,height:800,padding:30,boxSizing:'border-box',border:'2px solid var(--stroke)',borderRadius:28,background:'var(--surface)'}}>
 {asset?<><div style={{position:'relative',width:786,height:690}}><Img src={staticFile(asset.image)} style={{width:'100%',height:'100%',objectFit:'fill'}}/>{point&&region?<div style={{position:'absolute',left:region[0]*786,top:region[1]*690,width:region[2]*786,height:region[3]*690,border:'5px solid var(--accent)',borderRadius:10,boxSizing:'border-box'}}/>:null}</div><div style={{fontSize:22,marginTop:10,color:'var(--muted)'}}>{asset.label}</div></>:<VisualBlock scene={{...scene,frames:cut.end_frame-cut.start_frame}} focusIndex={point?.focus_index??-1}/>}
 </div>
 <div style={{position:'absolute',left:90,top:1320,width:830,fontSize:28,textAlign:'center',color:'var(--muted)',fontWeight:700}}>{scene.action}</div>
 <div style={{position:'absolute',left:80,bottom:238,width:850,fontSize:23,lineHeight:1.6,color:'var(--muted)'}}>{source}<br/>{asset?'실제 수정본 발췌 · 강조 위치는 그래픽 표현':'설명용 그래픽 · 편집점과 강조 대상은 공통 연출 계획'}</div>
 </AbsoluteFill>;
};
export const LayeredShorts:React.FC<LayeredProps>=({content,edit_points,emphasis,skin})=>{
 const styleVars=Object.fromEntries(Object.entries(skin.palette).map(([k,v])=>['--'+k,v]));
 const background=skin.background==='grid'?'linear-gradient(var(--stroke) 1px,transparent 1px),linear-gradient(90deg,var(--stroke) 1px,transparent 1px)':skin.background==='dots'?'radial-gradient(var(--stroke) 1.5px,transparent 1.5px)':'none';
 return <AbsoluteFill style={{...styleVars,background:'var(--paper)',fontFamily:'NotoLayers,sans-serif'} as React.CSSProperties}><Fonts/>
 <div style={{position:'absolute',inset:0,backgroundImage:background,backgroundSize:skin.background==='grid'?'64px 64px':'24px 24px',opacity:.22}}/>
 <Series>{edit_points.cuts.map(cut=><Series.Sequence key={cut.scene_id} durationInFrames={cut.end_frame-cut.start_frame} premountFor={edit_points.fps}><Shot scene={content.scenes.find(s=>s.id===cut.scene_id)!} cut={cut} points={emphasis.points.filter(p=>p.scene_id===cut.scene_id)} skin={skin} source={content.source}/></Series.Sequence>)}</Series>
 <Audio name="고정 음성 · 스킨 교체와 독립" src={staticFile(content.audio)}/>
 <style>{`.layered-captions > div > div {font-family:NotoLayers!important;font-size:50px!important;line-height:1.35!important;font-weight:700!important;background:var(--ink)!important;color:var(--paper)!important;padding:18px 24px!important;border-radius:14px}`}</style>
 <div className="layered-captions"><BasicCaptions name="공통 자막" captions={content.captions} width={850} combineTokensWithinMilliseconds={0} style={{position:'absolute',left:80,top:1380,wordBreak:'keep-all'}}/></div>
 </AbsoluteFill>;
};
