import React from 'react';
import {Frame2,Title,Pop,Badge,Slide,lime,ink,paper,Arrow} from './design';
export const Workflow2=()=> <Frame2 step="02 / 어떤 작업을 하나요?">
 <Title>PDF · Word 문서를<br/><span style={{background:lime}}>발표용 PPT로.</span></Title>
 <Pop style={{position:'absolute',left:80,top:650,display:'flex',gap:18}}><Badge dark>PDF</Badge><Badge dark>DOCX</Badge><Badge dark>주제 한 줄</Badge></Pop>
 <div style={{position:'absolute',left:450,top:775,rotate:'90deg'}}><Arrow/></div>
 <Pop delay={35} style={{position:'absolute',left:80,top:910}}><Slide style={{width:850,height:430}}/></Pop>
 <div style={{position:'absolute',left:80,top:1335,fontSize:25,opacity:.65}}>기능 설명용 그래픽 · 실제 생성 결과가 아닙니다</div>
 </Frame2>;
