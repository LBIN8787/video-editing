import React from 'react';
import {interpolate,useCurrentFrame} from 'remotion';
import {Frame,Title,Pop,Badge,lime,clamp} from './design';
export const Reveal=()=>{
 const f=useCurrentFrame();
 return <Frame dark step="01 / 어떤 스킬?">
  <Title>최근 <span style={{color:lime}}>30일</span>의<br/>반응을 한 번에.</Title>
  <Pop delay={5} style={{position:'absolute',top:630,left:70,width:860,textAlign:'center'}}><div style={{fontFamily:'Arial,sans-serif',fontSize:440,lineHeight:1,fontWeight:900,letterSpacing:-35,color:lime}}>30<span style={{fontSize:76,letterSpacing:-6}}>DAYS</span></div></Pop>
  <Pop delay={30} style={{position:'absolute',left:80,top:1140}}><Badge>조사 작업을 맡기는 AI 스킬</Badge><div style={{fontSize:66,fontWeight:800,marginTop:24,letterSpacing:-3}}>/last30days</div></Pop>
 </Frame>;
};
