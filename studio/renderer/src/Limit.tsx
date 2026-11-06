import React from 'react';
import {Frame,Title,Pop,ink,lime} from './design';
export const Limit=()=> <Frame step="05 / 시작 전 확인">
 <Title>소스에 따라<br/>추가 연결이 필요해요.</Title>
 <Pop style={{position:'absolute',top:730,left:80,width:850,borderTop:`4px solid ${ink}`,borderBottom:`4px solid ${ink}`,padding:'48px 0'}}><div style={{fontSize:100,fontWeight:900,letterSpacing:-5}}>X · YouTube</div><div style={{fontSize:46,lineHeight:1.5,marginTop:30}}>인증·추가 도구·API 등<br/>소스별 요구 조건 확인</div></Pop>
 <Pop delay={28} style={{position:'absolute',top:1190,left:80,fontSize:38,fontWeight:700,background:lime,padding:'16px 24px',borderRadius:15}}>연결 방식에 따라 비용이 생길 수 있어요.</Pop>
 </Frame>;
