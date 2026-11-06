import React from 'react';
import {useCurrentFrame,interpolate} from 'remotion';
import {Frame2,Title,Pop,Slide,ink,lime,clamp} from './design';
export const Hook2=()=>{
 const f=useCurrentFrame();
 return <Frame2 step="오늘의 발굴" source="PPT를 만든 뒤에도 수정할 수 있을까?">
 <Title>AI가 만든 PPT,<br/><span style={{background:lime}}>수정도 되나요?</span></Title>
 <div style={{position:'absolute',top:720,left:95,rotate:'-3deg'}}><Slide/><div style={{position:'absolute',left:0,top:0,width:760,height:425,background:'#19231e08',borderRadius:18}}/></div>
 <Pop delay={34} style={{position:'absolute',left:555,top:1030,borderRadius:20,background:ink,color:lime,padding:'22px 30px',fontSize:46,fontWeight:800,rotate:'6deg'}}>글자 하나만<br/>바꾸고 싶은데…</Pop>
 </Frame2>;
};
