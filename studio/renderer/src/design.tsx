import React from 'react';
import styleLock from '../../../styles/shorts-ai-guide/style-lock.json';
import {AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig, spring, staticFile, Img} from 'remotion';

export const ink=styleLock.colors.ink;
export const paper=styleLock.colors.paper;
export const lime=styleLock.colors.accent;
export const font='"Noto Sans CJK KR", sans-serif';
export const clamp={extrapolateLeft:'clamp',extrapolateRight:'clamp'} as const;
export const Frame:React.FC<{children:React.ReactNode;dark?:boolean;step:string;source?:string;episode?:string;checkedAt?:string}>=({children,dark=false,step,source='출처: github.com/mvanhorn/last30days-skill',episode='001',checkedAt='2026.11.06'})=>{
 const f=useCurrentFrame(); const {durationInFrames}=useVideoConfig();
 return <AbsoluteFill style={{backgroundColor:dark?ink:paper,color:dark?paper:ink,fontFamily:font,overflow:'hidden'}}>
  <div style={{position:'absolute',inset:0,backgroundImage:`radial-gradient(${dark?'#ffffff12':'#19231e12'} 1.5px,transparent 1.5px)`,backgroundSize:'24px 24px',opacity:.6}}/>
  <div style={{position:'absolute',top:126,left:80,right:150,display:'flex',alignItems:'center',justifyContent:'space-between',fontSize:30,fontWeight:700,letterSpacing:1}}><span style={{display:'flex',alignItems:'center',gap:15}}><i style={{display:'inline-block',width:17,height:17,borderRadius:'50%',background:dark?lime:ink}}/>AI 실전노트 <span style={{opacity:.4}}>{episode}</span></span><span style={{fontSize:26,opacity:.6}}>{checkedAt}</span></div>
  <div style={{position:'absolute',left:80,top:208,fontSize:29,fontWeight:700,letterSpacing:3,opacity:.65}}>{step}</div>
  {children}
  <div style={{position:'absolute',left:80,right:150,bottom:240,fontSize:24,opacity:.6,lineHeight:1.6}}>{source}<br/>공개 자료 확인 기준 · {checkedAt} KST</div>
  <div style={{position:'absolute',bottom:198,left:80,width:850,height:5,background:dark?'#ffffff25':'#19231e20'}}><div style={{height:5,width:`${100*Math.min(1,f/(durationInFrames-1))}%`,background:dark?lime:ink}}/></div>
 </AbsoluteFill>;
};
export const Title:React.FC<{children:React.ReactNode;size?:number;top?:number}>=({children,size=92,top=300})=><div style={{position:'absolute',left:80,top,width:850,fontSize:size,fontWeight:900,letterSpacing:-5,lineHeight:1.22,wordBreak:'keep-all'}}>{children}</div>;
export const Pop:React.FC<{children:React.ReactNode;delay?:number;style?:React.CSSProperties}>=({children,delay=0,style})=>{
 const f=useCurrentFrame();const {fps}=useVideoConfig();
 return <div style={{opacity:interpolate(f,[delay,delay+styleLock.motion.fadeFrames],[0,1],clamp),translate:`0px ${interpolate(f,[delay,delay+styleLock.motion.riseFrames],[styleLock.motion.risePixels,0],clamp)}px`,scale:1+(1-spring({frame:Math.max(0,f-delay),fps,config:{damping:styleLock.motion.springDamping,stiffness:styleLock.motion.springStiffness}}))*.025,...style}}>{children}</div>;
};
export const Badge:React.FC<{children:React.ReactNode;dark?:boolean}>=({children,dark})=><span style={{display:'inline-block',padding:'11px 20px',fontSize:30,fontWeight:800,borderRadius:100,background:dark?ink:lime,color:dark?paper:ink,letterSpacing:0}}>{children}</span>;
export const Arrow=()=> <svg viewBox="0 0 64 64" width="64" height="64" fill="none" stroke="currentColor" strokeWidth="5"><path d="M10 32h42M35 12l20 20-20 20"/></svg>;
export const SourceShot=({style}:{style?:React.CSSProperties})=><Img src={staticFile('github-source.png')} style={{width:840,borderRadius:20,...style}}/>;
