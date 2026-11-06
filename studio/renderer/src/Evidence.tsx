import React from 'react';
import {interpolate,useCurrentFrame} from 'remotion';
import {Frame,Title,Pop,Badge,lime,ink,clamp,SourceShot} from './design';
export const Evidence=()=>{
 const f=useCurrentFrame();
 return <Frame step="02 / 관심을 받은 이유">
  <Title size={82}>GitHub에서<br/>관심받는 조사 스킬</Title>
  {f<85 ? <Pop style={{position:'absolute',left:80,top:590,width:850,borderRadius:25,background:ink,color:lime,padding:'30px 40px',boxSizing:'border-box'}}><div style={{fontSize:31,letterSpacing:3}}>GITHUB STARS</div><div style={{fontSize:137,fontWeight:900,lineHeight:1.3,letterSpacing:-7}}>★ {Math.round(interpolate(f,[0,24],[60000,66774],clamp)).toLocaleString('en-US')}</div><div style={{fontSize:25,color:'#f3f1e8a0'}}>저장소 전체 별 수 · 품질 점수와는 다릅니다</div></Pop> : <div style={{position:'absolute',top:590,left:80,width:850,height:460,overflow:'hidden',border:`3px solid ${ink}`,borderRadius:22,background:'white'}}><SourceShot style={{width:850,scale:interpolate(f,[85,211],[1,1.055],clamp),transformOrigin:'top left'}}/><div style={{position:'absolute',bottom:0,left:0,right:0,padding:'12px 22px',fontSize:28,background:ink,color:lime,fontWeight:700}}>공식 README 발췌 · 원문 자료 화면</div></div>}
  {f<85 ? <div style={{position:'absolute',left:80,top:950,width:850,display:'flex',gap:16}}>{['Reddit','X','YouTube'].map((t,i)=><Pop key={t} delay={42+i*7} style={{fontSize:40,fontWeight:800,border:`2px solid ${ink}`,padding:'20px 25px',borderRadius:18}}>{t}</Pop>)}</div> : null}
  <Pop delay={75} style={{position:'absolute',top:1100,left:80,width:850}}><div style={{fontSize:66,fontWeight:800,lineHeight:1.4}}>반응을 모아서<br/><span style={{borderBottom:`12px solid ${lime}`}}>출처와 함께 정리</span></div><div style={{fontSize:26,opacity:.6,marginTop:25}}>동작 설명: 공식 README · 소스별 연결 조건 확인</div></Pop>
 </Frame>;
};
