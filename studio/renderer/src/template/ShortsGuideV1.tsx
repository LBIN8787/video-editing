import React,{useEffect,useState} from 'react';
import {AbsoluteFill,Img,Series,staticFile,delayRender,continueRender,cancelRender} from 'remotion';
import {Audio} from '@remotion/media';
import {BasicCaptions} from '../basic-captions';
import {Frame,Title,Pop,ink,lime,paper} from '../design';
import lock from '../../../../styles/shorts-ai-guide/style-lock.json';
import type {Caption} from '@remotion/captions';
export type GuideScene={id:string;frames:number;step:string;titleLines:string[];items:string[];dark:boolean;image?:string};
export type GuideProps={style_version:string;episode:string;checkedAt:string;source:string;audio:string;captions:Caption[];scenes:GuideScene[]};
const FontGate=()=>{
 const [handle]=useState(()=>delayRender('Load pinned Korean fonts'));
 useEffect(()=>{Promise.all([document.fonts.load('400 40px "Noto Sans CJK KR"'),document.fonts.load('900 84px "Noto Sans CJK KR"')]).then(()=>continueRender(handle)).catch(cancelRender)},[handle]);
 return <style>{`@font-face{font-family:"Noto Sans CJK KR";src:url("${staticFile('fonts/NotoSansCJKkr-Regular.otf')}") format("opentype");font-weight:100 500;font-display:block}@font-face{font-family:"Noto Sans CJK KR";src:url("${staticFile('fonts/NotoSansCJKkr-Bold.otf')}") format("opentype");font-weight:600 1000;font-display:block}`}</style>
};
const GuideCard=({scene,episode,checkedAt,source}:{scene:GuideScene;episode:string;checkedAt:string;source:string})=><Frame episode={episode} checkedAt={checkedAt} source={source} dark={scene.dark} step={scene.step}>
 <Title size={lock.font.titleSize}>{scene.titleLines.map((x,i)=><React.Fragment key={i}>{i>0?<br/>:null}{x}</React.Fragment>)}</Title>
 <div style={{position:'absolute',left:lock.layout.left,top:lock.layout.panelTop,width:lock.layout.width,height:lock.layout.panelHeight,boxSizing:'border-box',padding:36,borderRadius:28,background:scene.dark?'#ffffff0d':'white',border:`2px solid ${scene.dark?'#ffffff25':'#19231e20'}`,overflow:'hidden'}}>
 {scene.image?<Img src={staticFile(scene.image)} style={{width:'100%',height:330,objectFit:'contain',marginBottom:18}}/>:null}
 {scene.items.map((x,i)=><Pop key={i} delay={i*12} style={{display:'flex',alignItems:'center',gap:24,padding:scene.image?'16px 0':'30px 0',borderBottom:i<scene.items.length-1?`1px solid ${scene.dark?'#ffffff25':'#19231e20'}`:'none',fontSize:lock.font.bodySize,lineHeight:1.55,wordBreak:'keep-all'}}><span style={{display:'block',width:18,height:18,flexShrink:0,borderRadius:'50%',background:lime}}/><span>{x}</span></Pop>)}
 </div>
</Frame>;
export const ShortsGuideV1:React.FC<GuideProps>=props=><AbsoluteFill style={{background:paper}}>
 <FontGate/>
 <style>{`.locked-captions > div > div {font-family:"Noto Sans CJK KR",sans-serif!important;font-weight:700!important;background:rgba(25,35,30,.96)!important;border:1px solid #ffffff20;border-radius:14px;font-size:${lock.font.captionSize}px!important;line-height:1.35!important;padding:18px 24px!important;}`}</style>
 <Series>{props.scenes.map(scene=><Series.Sequence key={scene.id} durationInFrames={scene.frames} premountFor={30}><GuideCard scene={scene} episode={props.episode} checkedAt={props.checkedAt} source={props.source}/></Series.Sequence>)}</Series>
 <Audio name="Fixed ElevenLabs narration" src={staticFile(props.audio)}/>
 <div className="locked-captions"><BasicCaptions name="한국어 자막" width={lock.layout.width} captions={props.captions} combineTokensWithinMilliseconds={0} style={{position:'absolute',left:lock.layout.left,top:lock.layout.captionTop,wordBreak:'keep-all'}}/></div>
</AbsoluteFill>;
