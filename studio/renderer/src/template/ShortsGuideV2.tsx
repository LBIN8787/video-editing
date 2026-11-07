import React,{useEffect,useState} from 'react';
import {AbsoluteFill,Img,Series,staticFile,useCurrentFrame,useVideoConfig,interpolate,delayRender,continueRender,cancelRender} from 'remotion';
import {Audio} from '@remotion/media';
import {BasicCaptions} from '../basic-captions';
import type {GuideProps,GuideScene} from './ShortsGuideV1';
import raw005 from '../../../../channels/ai/episodes/005-remotion/captions.json';
import raw006 from '../../../../channels/ai/episodes/006-whisper/captions.json';
import lock from '../../../../styles/shorts-ai-guide/versions/1.1.0/style-lock.json';

export type VisualScene=GuideScene&{visual:string;action:string};
export type VisualProps=Omit<GuideProps,'scenes'>&{scenes:VisualScene[]};
const ink=lock.colors.ink,paper=lock.colors.paper,lime=lock.colors.accent;
const font='"Noto Sans CJK KR",sans-serif';
const clamp={extrapolateLeft:'clamp',extrapolateRight:'clamp'} as const;
const FontGate=()=>{
 const [h]=useState(()=>delayRender('Load pinned Korean fonts'));
 useEffect(()=>{Promise.all([document.fonts.load('400 40px "Noto Sans CJK KR"'),document.fonts.load('900 76px "Noto Sans CJK KR"')]).then(()=>continueRender(h)).catch(cancelRender)},[h]);
 return <style>{`@font-face{font-family:'Noto Sans CJK KR';src:url('${staticFile('fonts/NotoSansCJKkr-Regular.otf')}');font-weight:100 500}@font-face{font-family:'Noto Sans CJK KR';src:url('${staticFile('fonts/NotoSansCJKkr-Bold.otf')}');font-weight:600 1000}`}</style>;
};
const Icon=({type='file',size=76}:{type?:string;size?:number})=><svg width={size} height={size} viewBox="0 0 80 80" fill="none" stroke="currentColor" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round">
 {type==='audio'?<><path d="M14 32h13l17-14v44L27 48H14z"/><path d="M54 27q18 13 0 26M62 15q32 25 0 50"/></>:type==='video'?<><rect x="10" y="15" width="60" height="50" rx="10"/><path d="m33 28 20 12-20 12z"/></>:type==='folder'?<path d="M8 23h25l8 8h31v34H8zM8 23v-9h24l9 9"/>:<><path d="M20 8h28l15 16v48H20zM48 8v18h15M29 39h25M29 50h25M29 61h17"/></>}
 </svg>;
const Tag=({children}:{children:React.ReactNode})=><span style={{display:'inline-block',padding:'9px 18px',borderRadius:50,background:lime,color:ink,fontSize:25,fontWeight:800}}>{children}</span>;
const Arrow=()=> <div style={{fontSize:66,fontWeight:700,color:lime,textAlign:'center'}}>↓</div>;
const Window:React.FC<{name:string;children:React.ReactNode;dark?:boolean}>=({name,children,dark=false})=><div style={{width:'100%',borderRadius:23,overflow:'hidden',border:`2px solid ${dark?'#ffffff30':'#19231e20'}`,background:dark?ink:'#fff',color:dark?paper:ink,boxSizing:'border-box'}}>
 <div style={{height:58,display:'flex',alignItems:'center',gap:10,padding:'0 22px',background:dark?'#ffffff0d':'#f0f1eb',fontSize:25}}><i style={{width:10,height:10,borderRadius:30,background:'#d77869'}}/><i style={{width:10,height:10,borderRadius:30,background:'#d6bd71'}}/><i style={{width:10,height:10,borderRadius:30,background:'#8fb48b'}}/><span style={{marginLeft:14,opacity:.75}}>{name}</span></div>
 <div style={{padding:26}}>{children}</div>
 </div>;
const Phone=({title='음성에서 자막 만들기',different=false,poster}:{title?:string;different?:boolean;poster?:string})=><div style={{width:252,height:450,borderRadius:26,overflow:'hidden',border:`4px solid ${ink}`,background:different?'#dadcf8':paper,position:'relative',boxShadow:'0 12px 30px #00000015',color:ink}}>
 {poster?<Img src={staticFile(poster)} style={{width:'100%',height:'100%',objectFit:'cover'}}/>:<><div style={{margin:'25px 18px',fontSize:17,fontWeight:800}}>AI 실전노트</div><div style={{margin:'25px 18px',fontWeight:900,fontSize:different?32:27,lineHeight:1.4}}>{title}</div><div style={{margin:18,padding:15,background:different?'#433e7a':'#fff',color:different?'white':ink,borderRadius:12,fontSize:20,lineHeight:1.6}}><Icon size={55} type="video"/><br/>실제 활용 예시</div><div style={{position:'absolute',bottom:different?50:22,left:16,right:16,background:ink,color:'white',padding:10,borderRadius:8,fontSize:17,textAlign:'center'}}>핵심 자막</div></>}
 </div>;
const Pointer=({x,y}:{x:number;y:number})=>{
 const f=useCurrentFrame();
 return <div style={{position:'absolute',left:x,top:y,translate:`${interpolate(f,[0,30],[55,0],clamp)}px ${interpolate(f,[0,30],[45,0],clamp)}px`,color:lime,filter:'drop-shadow(0 2px 3px #0006)'}}><svg width="58" height="70" viewBox="0 0 40 50"><path d="M3 2v37l10-10 8 17 8-4-8-16h16z" fill="currentColor" stroke={ink} strokeWidth="2"/></svg></div>;
};
const FileRow=({name,type='file',active=false}:{name:string;type?:string;active?:boolean})=><div style={{display:'flex',alignItems:'center',gap:22,padding:'20px 16px',borderRadius:14,background:active?'#d4f85a45':'#19231e05',border:active?'2px solid #88a135':'2px solid transparent',marginTop:12,fontSize:31,color:ink}}><Icon type={type} size={54}/><span>{name}</span>{active?<span style={{marginLeft:'auto',color:'#58720b',fontSize:25}}>선택됨</span>:null}</div>;
const Chat=({lines}:{lines:string[]})=>{
 const f=useCurrentFrame();
 return <Window name="AI에 보낼 요청 · 입력 예시"><div style={{display:'flex',gap:16,alignItems:'center',fontSize:28,marginBottom:28}}><div style={{width:44,height:44,background:ink,borderRadius:30,color:lime,textAlign:'center'}}>나</div>필요한 작업을 구체적으로</div>
 {lines.map((line,i)=><div key={line} style={{marginTop:16,padding:'23px 24px',borderRadius:'20px 20px 3px 20px',background:i===0?ink:'#e9efdb',color:i===0?paper:ink,fontSize:35,fontWeight:i===0?800:500,lineHeight:1.5,opacity:interpolate(f,[i*12,i*12+10],[0,1],clamp)}}>{line}</div>)}
 <div style={{display:'flex',justifyContent:'flex-end',marginTop:22}}><Tag>이 문장부터 복사해서 요청</Tag></div></Window>;
};
const Chain=({items}:{items:{label:string;type:string}[]})=><div>{items.map((item,i)=><React.Fragment key={item.label}><div style={{display:'flex',alignItems:'center',gap:26,padding:'26px 30px',borderRadius:23,border:'2px solid #19231e20',background:'#fff',fontSize:37,fontWeight:800,color:ink}}><Icon type={item.type}/>{item.label}</div>{i<items.length-1?<Arrow/>:null}</React.Fragment>)}</div>;

const Visual=({scene,episode}:{scene:VisualScene;episode:string})=>{
 const f=useCurrentFrame();const durationInFrames=scene.frames;
 const current=Math.min(2,Math.floor(f/(durationInFrames/3)));
 const captions=episode==='005'?raw005:raw006;
 if(scene.visual==='inconsistent')return <><div style={{display:'flex',justifyContent:'space-around',alignItems:'center',paddingTop:25}}><Phone title="같은 채널인데"/><div style={{fontSize:56,color:ink}}>≠</div><Phone title="다른 디자인?" different/></div><div style={{display:'flex',justifyContent:'space-around',marginTop:35}}><Tag>자막은 아래</Tag><Tag>자막이 위로?</Tag></div></>;
 if(scene.visual==='consistent')return <><div style={{display:'flex',justifyContent:'space-around',paddingTop:25}}><Phone title="자막 만드는 법"/><Phone title="회의록 요약법"/></div><div style={{marginTop:40,textAlign:'center',fontSize:37,fontWeight:800,color:ink}}>틀은 그대로 → 제목·내용만 교체</div><div style={{display:'flex',justifyContent:'center',gap:12,marginTop:26}}><Tag>같은 글꼴</Tag><Tag>같은 색상</Tag><Tag>같은 자막 위치</Tag></div></>;
 if(scene.visual==='files')return <><Window name="AI 코딩 도구 · 프로젝트 폴더 열기"><div style={{display:'flex',alignItems:'center',gap:18,fontSize:32,fontWeight:800}}><Icon type="folder" size={54}/>내 쇼츠 프로젝트</div><FileRow name="편집 템플릿 · 디자인 유지" active={current===0}/><FileRow name="새 대본 · 제목과 장면 문구" active={current===1}/><FileRow name="voice.mp3 · 새 내레이션" type="audio" active={current===2}/></Window><div style={{marginTop:28,textAlign:'center'}}><Tag>AI 코딩 도구에서 이 폴더 열기</Tag></div></>;
 if(scene.visual==='prompt')return <Chat lines={scene.items}/>;
 if(scene.visual==='preview')return <><Window name="미리보기 → MP4 출력 · 흐름 재구성"><div style={{display:'flex',gap:30,alignItems:'center'}}><Phone poster="visual-v2/remotion-poster.png"/><div style={{flex:1,fontSize:29,lineHeight:1.8}}><Tag>여기를 확인</Tag><p>제목이 잘리지 않나?</p><p>자막이 음성과 맞나?</p><div style={{position:'relative',background:ink,color:lime,padding:'20px 15px',borderRadius:13,textAlign:'center',fontWeight:900,fontSize:32}}>MP4 출력<Pointer x={170} y={34}/></div></div></div></Window><div style={{marginTop:25,textAlign:'center'}}><Tag>미리보기 이미지: 이번 수정본 실제 프레임</Tag></div></>;
 if(scene.visual==='outputs')return <><div style={{display:'flex',justifyContent:'space-around',paddingTop:12}}><Phone poster="visual-v2/remotion-poster.png"/><Phone poster="visual-v2/whisper-poster.png"/></div><div style={{marginTop:34,textAlign:'center',fontSize:35,fontWeight:800,color:ink}}>같은 편집 틀로 만든 실제 두 영상</div><div style={{display:'flex',justifyContent:'center',gap:18,marginTop:25}}><Tag>Remotion 활용편</Tag><Tag>Whisper 활용편</Tag></div></>;
 if(scene.visual==='setup')return <><Window name="프로젝트 터미널 · 실행 예시" dark><div style={{fontSize:29,opacity:.6,marginBottom:15}}>프로젝트 폴더에서</div><div style={{fontFamily:'monospace',fontSize:35,lineHeight:2.3}}><span style={{color:lime}}>npm ci</span><br/><span style={{color:lime}}>npx remotion studio</span></div></Window><div style={{display:'flex',gap:16,marginTop:30}}><div style={{flex:1,padding:25,borderRadius:20,background:'white',color:ink,fontSize:31,lineHeight:1.7}}>코딩 실행 환경<br/><b>Node.js 필요</b></div><div style={{flex:1,padding:25,borderRadius:20,background:'white',color:ink,fontSize:31,lineHeight:1.7}}>무료 사용 대상?<br/><b>라이선스 확인</b></div></div><div style={{marginTop:25,textAlign:'center'}}><Tag>AI 도구·음성 생성 요금은 별도</Tag></div></>;
 if(scene.visual==='recap')return <Chain items={[{label:'기존 템플릿 열기',type:'folder'},{label:'새 대본·음성 연결',type:'audio'},{label:'미리보기 후 MP4',type:'video'}]}/>;
 if(scene.visual==='audio')return <><Window name="실제 내레이션 파일"><div style={{display:'flex',gap:22,alignItems:'center',fontSize:36,fontWeight:800}}><Icon type="audio"/>voice.mp3</div><div style={{background:ink,borderRadius:18,marginTop:22,padding:'26px 12px',position:'relative'}}><Img src={staticFile('visual-v2/voice-waveform.png')} style={{width:'100%',height:120,objectFit:'fill'}}/><div style={{position:'absolute',top:12,bottom:12,left:`${10+interpolate(f,[0,durationInFrames],[0,90],clamp)}%`,width:3,background:'white'}}/></div></Window><Arrow/><div style={{background:'white',padding:'26px 32px',borderRadius:23,color:ink,fontSize:37,lineHeight:1.6}}>“자동 자막, 매번 처음부터<br/><b>타이핑하세요?</b>”</div><div style={{marginTop:25,textAlign:'center'}}><Tag>이 음성 파일을 자막으로</Tag></div></>;
 if(scene.visual==='recognize')return <Chain items={[{label:'실제 내레이션 파일',type:'audio'},{label:'Whisper로 한국어 인식',type:'file'},{label:'텍스트와 발화 시간 추출',type:'file'}]}/>;
 if(scene.visual==='extract')return <><Window name="Whisper · 실제 실행 설정 재구성"><FileRow name="voice.mp3" type="audio" active/><div style={{marginTop:22,display:'flex',gap:18}}><div style={{flex:1,padding:22,background:'#f0f1eb',borderRadius:13,fontSize:28}}>인식 언어<br/><b style={{fontSize:39}}>한국어 · ko</b></div><div style={{flex:1,padding:22,background:'#f0f1eb',borderRadius:13,fontSize:28}}>단어별 시간<br/><b style={{fontSize:39}}>사용</b></div></div></Window><Arrow/><div style={{display:'flex',justifyContent:'center',gap:22}}><div style={{background:ink,color:lime,padding:24,borderRadius:16,fontSize:34}}>인식 결과.json</div><div style={{background:ink,color:lime,padding:24,borderRadius:16,fontSize:34}}>자막.srt</div></div><div style={{marginTop:25,textAlign:'center',fontSize:28,color:ink}}>설정: language='ko', word_timestamps=True</div></>;
 if(scene.visual==='sync')return <><Window name="실제 자막 일부 · SRT"><div style={{fontFamily:'monospace',fontSize:30,color:'#657051'}}>00:00:03,480 → 00:00:06,780</div><div style={{fontSize:36,lineHeight:1.6,marginTop:16}}>{captions[1].text}</div></Window><div style={{position:'relative',marginTop:32,padding:'24px 18px',borderRadius:18,background:ink,color:paper}}><div style={{fontSize:25,marginBottom:20}}>파형과 자막 시작 위치를 비교</div><Img src={staticFile('visual-v2/voice-waveform.png')} style={{width:'100%',height:90,objectFit:'fill'}}/><div style={{marginTop:18,marginLeft:90,padding:15,borderRadius:8,width:440,background:lime,color:ink,fontSize:27,fontWeight:800}}>위스퍼는 음성을 글로…</div><div style={{position:'absolute',top:60,bottom:12,left:110+interpolate(f,[0,durationInFrames],[0,450],clamp),width:3,background:paper}}/></div><div style={{marginTop:25,textAlign:'center'}}><Tag>파형·자막 연결은 설명용 도식</Tag></div></>;
 if(scene.visual==='local')return <><div style={{border:'3px solid #19231e',borderRadius:25,background:'white',padding:35,color:ink,textAlign:'center'}}><div style={{fontSize:29,marginBottom:20}}>내 컴퓨터 안에서 처리</div><div style={{display:'flex',justifyContent:'center',gap:38,alignItems:'center'}}><Icon type="audio" size={90}/><div style={{fontSize:50}}>→</div><Icon size={90}/></div><div style={{marginTop:25,fontSize:40,fontWeight:900}}>음성 → Whisper → 자막</div></div><div style={{marginTop:30,padding:28,borderRadius:20,background:ink,color:paper,fontSize:31,lineHeight:1.8}}>모델 설치 + 컴퓨터 자원 필요<br/><b style={{color:lime}}>로컬 인식: API 호출료 없음</b><br/>ElevenLabs 음성 생성 요금은 별도</div></>;
 return <><Window name="최종 확인 · 실제 작업 체크리스트">{['제품명과 숫자를 원문 대조','자막 줄바꿈과 발화 시간 확인','최종 영상을 직접 재생'].map((label,i)=><div key={label} style={{display:'flex',gap:20,alignItems:'center',padding:'29px 0',fontSize:34,borderBottom:i===2?'none':'1px solid #19231e20'}}><div style={{border:'3px solid #839451',borderRadius:8,width:37,height:37,background:current>=i?lime:'white',textAlign:'center',fontSize:28,fontWeight:900}}>{current>=i?'✓':''}</div>{label}</div>)}</Window><div style={{marginTop:35,textAlign:'center'}}><Tag>초안은 AI → 검수는 직접</Tag></div></>;
};

const Scene=({scene,episode,source}:{scene:VisualScene;episode:string;source:string})=>{
 const f=useCurrentFrame();
 return <AbsoluteFill style={{background:paper,color:ink,fontFamily:font}}>
 <div style={{position:'absolute',inset:0,backgroundImage:'radial-gradient(#19231e12 1.5px,transparent 1.5px)',backgroundSize:'24px 24px',opacity:.45}}/>
 <div style={{position:'absolute',top:110,left:80,fontSize:30,fontWeight:800,display:'flex',alignItems:'center',gap:15}}><i style={{width:17,height:17,borderRadius:50,background:ink}}/>AI 실전노트</div>
 <div style={{position:'absolute',top:180,left:80,fontSize:26,color:'#657051',fontWeight:700}}>{scene.step}</div>
 <div style={{position:'absolute',left:80,top:242,width:850,fontSize:76,fontWeight:900,letterSpacing:-4,lineHeight:1.24}}>{scene.titleLines.map((s,i)=><React.Fragment key={s}>{i>0?<br/>:null}{s}</React.Fragment>)}</div>
 <div style={{position:'absolute',left:80,top:495,width:850,height:800,boxSizing:'border-box',padding:30,border:'2px solid #19231e20',background:'#ffffffa0',borderRadius:28,opacity:interpolate(f,[0,5],[0,1],clamp)}}><Visual scene={scene} episode={episode}/></div>
 <div style={{position:'absolute',left:90,top:1320,width:830,fontSize:28,color:'#536348',fontWeight:700,textAlign:'center'}}>{scene.action}</div>
 <div style={{position:'absolute',left:80,bottom:238,width:850,fontSize:23,color:'#657051',lineHeight:1.6}}>{source}<br/>{scene.visual==='outputs'?'실제 수정본 프레임':scene.visual==='audio'?'실제 내레이션 파형 · 입력 문장':scene.visual==='sync'?'실제 자막 일부 + 설명용 타임라인': '자체 제작 활용 예시 · 작업 흐름 재구성'}</div>
 </AbsoluteFill>;
};
export const ShortsGuideV2:React.FC<VisualProps>=props=><AbsoluteFill style={{background:paper}}>
 <FontGate/>
 <Series>{props.scenes.map(s=><Series.Sequence key={s.id} durationInFrames={s.frames} premountFor={30}><Scene scene={s} episode={props.episode} source={props.source}/></Series.Sequence>)}</Series>
 <Audio name="고정 ElevenLabs Han Aim 내레이션" src={staticFile(props.audio)}/>
 <style>{`.visual-captions > div > div {font-family:${font}!important;font-weight:700!important;background:${ink}!important;border-radius:14px;font-size:50px!important;line-height:1.35!important;padding:18px 24px!important;}`}</style>
 <div className="visual-captions"><BasicCaptions name="한국어 자막" width={850} captions={props.captions} combineTokensWithinMilliseconds={0} style={{position:'absolute',left:80,top:1380,wordBreak:'keep-all'}}/></div>
 </AbsoluteFill>;
