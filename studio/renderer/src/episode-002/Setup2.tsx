import React from 'react';
import {Frame2,Title,Pop,Badge,ink,lime} from './design';
export const Setup2=()=> <Frame2 step="05 / 시작 전에 알아둘 것">
 <Title>시작은 이렇게.<br/><span style={{background:lime}}>자료 → 요청 → 수정</span></Title>
 <Pop style={{position:'absolute',left:80,top:680,width:850,borderTop:`4px solid ${ink}`,padding:'40px 0'}}><div style={{fontSize:43,fontWeight:800,lineHeight:1.6}}>① Python·에이전트 설치<br/>② 프로젝트 폴더에 문서 넣기<br/>③ 채팅에서 PPT 제작 요청</div></Pop>
 <Pop delay={70} style={{position:'absolute',left:80,top:1010,width:850,background:lime,borderRadius:23,padding:35,boxSizing:'border-box'}}><div style={{fontSize:58,fontWeight:900}}>완성 후 직접 수정</div><div style={{fontSize:43,fontWeight:700,lineHeight:1.5,marginTop:20}}>PowerPoint로 열어 확인<br/>모델 사용료는 별도</div></Pop>
 </Frame2>;
