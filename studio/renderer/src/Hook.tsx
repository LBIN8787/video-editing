import React from 'react';
import {interpolate,useCurrentFrame} from 'remotion';
import {Frame,Title,Pop,ink,lime,paper,clamp} from './design';
export const Hook=()=>{
 const f=useCurrentFrame();
 return <Frame step="오늘의 발굴" source="여러 커뮤니티를 한 번에 조사하는 스킬">
  <Title>AI 소식 찾다가<br/><span style={{background:lime,padding:'0 10px'}}>시간 다 쓰죠?</span></Title>
  <div style={{position:'absolute',left:80,top:720,width:850,height:620}}>
   {['GitHub','X','Reddit','YouTube'].map((label,i)=><div key={label} style={{position:'absolute',top:i*83,left:35+i*20,width:700,height:200,border:`3px solid ${ink}`,borderRadius:20,background:paper,rotate:`${(i-1.5)*3}deg`,translate:`${Math.sin(f/15+i)*6}px 0px`,boxShadow:'0px 12px 0 #19231e0a'}}><div style={{borderBottom:`2px solid ${ink}30`,padding:'15px 25px',display:'flex',gap:10,alignItems:'center'}}><i style={{width:12,height:12,borderRadius:100,background:ink}}/><span style={{fontSize:27,marginLeft:12}}>{label}</span></div><div style={{padding:24,fontSize:38,fontWeight:700,opacity:.4}}>새 도구 · 새 스킬 · 또 새 소식…</div></div>)}
   <Pop delay={22} style={{position:'absolute',right:5,top:355,width:230,height:230,borderRadius:'50%',background:lime,border:`4px solid ${ink}`,display:'flex',alignItems:'center',justifyContent:'center',fontSize:68,fontWeight:900,whiteSpace:"nowrap",rotate:'-9deg'}}>탭 10+</Pop>
  </div>
 </Frame>;
};
