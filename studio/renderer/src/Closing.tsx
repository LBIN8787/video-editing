import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame,Title,Pop,Badge,lime} from './design';
export const Closing=()=>{
 const f=useCurrentFrame();
 return <Frame dark step="오늘 해볼 한 가지" source="도구: mvanhorn/last30days-skill · 원문 안내는 제작 노트">
  <Title>처음엔<br/><span style={{color:lime}}>주제 하나만.</span></Title>
  <Pop delay={10} style={{position:'absolute',left:80,top:700,fontSize:64,fontWeight:700,lineHeight:1.6,letterSpacing:-3}}>내 일에 쓸 수 있는지<br/>직접 확인해 보세요.</Pop>
  <Pop delay={48} style={{position:'absolute',left:80,top:1070,width:850,borderTop:'3px solid #ffffff40',paddingTop:45}}><Badge>저장하고 따라 해보기</Badge><div style={{fontSize:45,fontWeight:700,marginTop:25,lineHeight:1.5}}>질문 하나 → 최근 반응 → 원문 확인</div></Pop>
 </Frame>;
};
