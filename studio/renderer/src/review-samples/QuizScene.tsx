import React from 'react';
import {AbsoluteFill,interpolate,useCurrentFrame} from 'remotion';
import {ink,paper,lime,font,clamp} from '../design';
type Props={variant:1|2;phase:string};
export const QuizScene=({variant,phase}:Props)=>{
 const f=useCurrentFrame();const solve=['Solve','Answer','Comment'].includes(phase);const end=['Answer','Comment'].includes(phase);
 return <AbsoluteFill style={{background:paper,color:ink,fontFamily:font,overflow:'hidden'}}>
 <div style={{position:'absolute',inset:0,backgroundImage:'radial-gradient(#19231e13 1.5px, transparent 1.5px)',backgroundSize:'24px 24px'}}/>
 <div style={{position:'absolute',left:80,top:130,fontSize:31,fontWeight:800}}>● 눈으로 푸는 30초 <span style={{opacity:.4,marginLeft:25}}>00{variant}</span></div>
 <div style={{position:'absolute',left:80,top:225,fontSize:28,fontWeight:700,letterSpacing:2,opacity:.6}}>{phase==='Comment'?'여러분의 첫 생각은?':solve?'정답과 풀이':'먼저 골라 보세요'}</div>
 <div style={{position:'absolute',left:80,top:315,width:850,fontSize:86,fontWeight:900,letterSpacing:-5,lineHeight:1.25,wordBreak:'keep-all'}}>{variant===1?<>둘레가 같으면<br/><span style={{background:lime}}>넓이도 같을까?</span></>:<>20% 내리고<br/><span style={{background:lime}}>20% 올리면?</span></>}</div>
 {variant===1?<>
 <div style={{position:'absolute',left:80,top:670,width:850,background:'white',border:`3px solid ${ink}`,borderRadius:22,padding:'30px 20px 10px'}}>
 <svg viewBox="0 0 800 430" width="100%" role="img" aria-label="A 5곱하기5, B 7곱하기3">
 <defs><pattern id="quizgrid" x="60" y="90" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" stroke="#19231e50" fill="none" strokeWidth="1.5"/></pattern></defs>
 <rect x="60" y="90" width="200" height="200" fill={solve?lime:'#dce3d4'} stroke={ink} strokeWidth="4"/>
 <rect x="60" y="90" width="200" height="200" fill="url(#quizgrid)"/>
 <rect x="420" y="130" width="280" height="120" fill="#d5e5ef" stroke={ink} strokeWidth="4"/>
 <rect x="420" y="130" width="280" height="120" fill="url(#quizgrid)"/>
 <g fill={ink} textAnchor="middle" fontFamily={font} fontWeight="700"><text x="160" y="50" fontSize="38">A</text><text x="560" y="50" fontSize="38">B</text><text x="160" y="340" fontSize="34">5 × 5</text><text x="560" y="340" fontSize="34">7 × 3</text><text x="160" y="395" fontSize="34">{solve?'넓이 25':'둘레 20'}</text><text x="560" y="395" fontSize="34">{solve?'넓이 21':'둘레 20'}</text></g></svg></div>
 <div style={{position:'absolute',left:80,top:1210,width:850,boxSizing:'border-box',textAlign:'center',fontSize:43,fontWeight:900,background:solve?lime:ink,color:solve?ink:paper,padding:'17px 27px',borderRadius:15}}>{end?'정답 A · 25 > 21':solve?'넓이 = 안쪽을 채우는 칸':'A가 더 크다 / B가 더 크다 / 같다'}</div>
 </>:<>
 <div style={{position:'absolute',left:80,top:650,width:850,borderTop:`4px solid ${ink}`,paddingTop:30,fontSize:35,fontWeight:700}}>시작 가격 <span style={{float:'right',fontSize:51}}>100원</span></div>
 <div style={{position:'absolute',left:80,top:790,width:850,borderRadius:24,background:ink,color:paper,padding:35,boxSizing:'border-box'}}><div style={{fontSize:35,color:lime}}>① 100원에서 20% 할인</div><div style={{fontSize:125,fontWeight:900,letterSpacing:-6}}>80<span style={{fontSize:55}}>원</span></div><div style={{fontSize:35,lineHeight:1.6}}>② {solve?'80 × 20% = 16원 인상':'그다음 20% 인상의 기준은?'}<br/><span style={{color:lime}}>{solve?'80 + 16 = 96원':'100원일까? 80원일까?'}</span></div></div>
 <div style={{position:'absolute',top:1230,left:80,fontSize:51,fontWeight:900,background:lime,padding:'12px 24px',borderRadius:12}}>{end?'정답 96원 · 기준이 달라요':solve?'80원에 16원을 더합니다':'원래 가격으로 돌아올까요?'}</div>
 </>}
 <div style={{position:'absolute',left:80,top:1630,width:850,fontSize:25,opacity:.65,lineHeight:1.7}}>{variant===1?'조건: 같은 길이 단위 · 둘레와 넓이를 구분합니다.':'조건: 같은 상품에 할인 후 인상을 순서대로 적용합니다.'}<br/>직접 만든 도식과 계산 풀이 · 설명용 애니메이션</div>
 </AbsoluteFill>;
};
