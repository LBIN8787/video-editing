import React from 'react';
import {Img,staticFile} from 'remotion';
import {Frame2,Title,Pop,Badge,lime,ink} from './design';
export const Closing2=()=> <Frame2 dark step="오늘 해볼 한 가지">
 <Title>처음엔 문서<br/><span style={{color:lime}}>한 장부터.</span></Title>
 <Pop delay={4} style={{position:'absolute',left:80,top:650,width:850,borderRadius:20,overflow:'hidden'}}><Img src={staticFile('episode-002/official-example.webp')} style={{width:850}}/><div style={{fontSize:27,color:lime,padding:'13px 20px',background:'#2c3630'}}>개발자 공개 예시 · 이번 영상에서 생성한 결과 아님</div></Pop>
 <Pop delay={90} style={{position:'absolute',left:80,top:1250,fontSize:44,fontWeight:800}}>예쁜지 + 수정도 되는지 함께 확인.</Pop>
 </Frame2>;
