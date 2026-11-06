import React from 'react';
import {useCurrentFrame,interpolate} from 'remotion';
import {Frame,Title,Pop,Badge,ink,paper,lime,clamp,Arrow} from './design';
export const Example=()=>{
 const f=useCurrentFrame();
 const text='요즘 많이 쓰는\nPPT AI 도구를\n비교해 줘';
 const count=Math.floor(interpolate(f,[8,67],[0,text.length],clamp));
 return <Frame dark step="03 / 이렇게 물어보세요" source="사용법 설명용 예시 · 실제 조사 결과가 아닙니다">
  <Title>내가 궁금한<br/>주제 <span style={{color:lime}}>하나만.</span></Title>
  <div style={{position:'absolute',left:80,top:650,width:850,background:paper,color:ink,borderRadius:24,padding:40,boxSizing:'border-box'}}><div style={{fontSize:29,opacity:.6,marginBottom:28}}>조사 요청 예시</div><div style={{fontSize:75,fontWeight:800,letterSpacing:-4,lineHeight:1.45,whiteSpace:'pre-line',minHeight:326}}>{text.slice(0,count)}<span style={{opacity:f%24<12?1:0,color:'#809627'}}>▌</span></div><div style={{marginTop:35,borderTop:'2px solid #19231e22',paddingTop:25,display:'flex',justifyContent:'space-between',fontSize:30,fontWeight:700}}><span>비교 기준도 함께 요청</span><Arrow/></div></div>
  <Pop delay={83} style={{position:'absolute',left:80,top:1250,display:'flex',gap:15}}><Badge>가격</Badge><Badge>사용 조건</Badge><Badge>원문 링크</Badge></Pop>
 </Frame>;
};
