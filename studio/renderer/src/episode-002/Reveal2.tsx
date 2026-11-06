import React from 'react';
import {useCurrentFrame,interpolate} from 'remotion';
import {Frame2,Title,Pop,Badge,lime,ink,paper,clamp} from './design';
export const Reveal2=()=>{
 const f=useCurrentFrame();
 return <Frame2 dark step="01 / 오늘의 AI 스킬">
 <Title>PPT Master<br/><span style={{color:lime}}>수정까지 되는 PPT.</span></Title>
 <Pop delay={8} style={{position:'absolute',left:80,top:690,fontFamily:'Arial,sans-serif',fontSize:200,fontWeight:900,letterSpacing:-12,color:lime}}>.pptx</Pop>
 <Pop delay={60} style={{position:'absolute',left:80,top:1020,width:850,borderTop:'3px solid #ffffff50',paddingTop:28}}><div style={{fontSize:29,letterSpacing:3,opacity:.7}}>어떤 기능을 쓸 수 있나요?</div><div style={{fontSize:48,fontWeight:800,color:lime,lineHeight:1.65,marginTop:15}}>문서 → 발표용 PPTX<br/>글자 · 도형 · 차트 수정<br/>발표자 노트 요청</div></Pop>
 </Frame2>;
};
