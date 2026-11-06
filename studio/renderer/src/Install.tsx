import React from 'react';
import {Frame,Title,Pop,Badge,ink,paper,lime} from './design';
export const Install=()=> <Frame step="04 / 시작하는 방법">
 <Title>설치한 다음,<br/><span style={{background:lime}}>명령어 + 주제.</span></Title>
 <Pop style={{position:'absolute',left:80,top:680,width:850}}><Badge dark>Claude Code 기준</Badge><div style={{marginTop:35,borderLeft:`7px solid ${ink}`,padding:'12px 0 12px 28px',fontSize:46,fontWeight:700,lineHeight:1.5}}>공식 README의<br/>설치 안내부터 따라가세요.</div></Pop>
 <Pop delay={35} style={{position:'absolute',top:1000,left:80,width:850,background:ink,color:paper,borderRadius:25,padding:38,boxSizing:'border-box'}}><div style={{fontFamily:'monospace',fontSize:55,fontWeight:800,color:lime}}>/last30days</div><div style={{marginTop:28,fontSize:47,fontWeight:700}}>PPT AI 도구 비교</div></Pop>
 <div style={{position:'absolute',top:1280,left:80,fontSize:30,opacity:.7}}>일반 채팅창에 입력만 해서 설치되는 기능은 아닙니다.</div>
 </Frame>;
