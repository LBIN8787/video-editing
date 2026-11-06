import React from 'react';
import {useCurrentFrame,interpolate} from 'remotion';
import {Frame2,Title,Pop,Badge,ink,paper,lime,clamp} from './design';
export const Prompt2=()=>{
 const f=useCurrentFrame();const text='이 문서를\n발표용 5장으로 만들고,\n발표자 노트도 넣어 줘.';const n=Math.floor(interpolate(f,[20,95],[0,text.length],clamp));
 return <Frame2 step="04 / 이렇게 요청해 보세요" source="요청 문장은 사용 예시 · 실행 결과가 아닙니다">
 <Title>첫 요청은<br/><span style={{background:lime}}>짧고 구체적으로.</span></Title>
 <div style={{position:'absolute',left:80,top:660,width:850,background:ink,color:paper,borderRadius:25,padding:42,boxSizing:'border-box',minHeight:490}}><div style={{color:lime,fontSize:29,fontWeight:700,marginBottom:28}}>에이전트에 입력할 요청 예시</div><div style={{fontSize:62,fontWeight:800,letterSpacing:-3,lineHeight:1.55,whiteSpace:'pre-line'}}>{text.slice(0,n)}<span style={{opacity:f%24<12?1:0,color:lime}}>▌</span></div></div>
 <Pop delay={110} style={{position:'absolute',left:80,top:1220,display:'flex',gap:18}}><Badge dark>장수</Badge><Badge dark>독자</Badge><Badge dark>노트</Badge></Pop>
 </Frame2>;
};
