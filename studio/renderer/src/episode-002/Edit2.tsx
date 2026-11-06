import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Frame2,Title,Pop,Badge,Slide,lime,ink} from './design';
export const Edit2=()=>{
 const f=useCurrentFrame();
 return <Frame2 dark step="03 / 핵심은 편집 가능한 요소">
 <Title>글자 · 도형 · 차트<br/><span style={{color:lime}}>나중에 손볼 수 있게.</span></Title>
 <Pop delay={4} style={{position:'absolute',left:80,top:690}}><Slide selected label={f<65?'발표 자료':'주간 실적'} style={{width:850,height:440}}/></Pop>
 <Pop delay={55} style={{position:'absolute',left:80,top:1200}}><Badge>PowerPoint에서 편집</Badge></Pop>
 <div style={{position:'absolute',left:80,top:1325,fontSize:26,opacity:.65}}>편집 방식 설명용 모션 · 실제 앱 조작 화면이 아닙니다</div>
 </Frame2>;
};
