import React from 'react';
import {Series,staticFile,useVideoConfig} from 'remotion';
import {Audio} from '@remotion/media';
import {BasicCaptions} from '../basic-captions';
import {Hook} from '../Hook';
import {Reveal} from '../Reveal';
import {Evidence} from '../Evidence';
import {Example} from '../Example';
import {Install} from '../Install';
import {Limit} from '../Limit';
import {Closing} from '../Closing';
export const AI001Review=()=>{const {fps}=useVideoConfig();return <><style>{`.review-captions > div > div {font-family:"Noto Sans CJK KR",sans-serif!important;font-weight:700!important;background:rgba(25,35,30,.94)!important;border-radius:14px;padding:18px 24px!important;}`}</style><Series>
<Series.Sequence name="Hook" durationInFrames={113} premountFor={fps}><Hook/>
<Audio name="한국어 보이스" src={staticFile("review-samples/AI001Review/voice-0.wav")} premountFor={fps}/>
<div className="review-captions"><BasicCaptions name="한글 자막" premountFor={fps} width={850} combineTokensWithinMilliseconds={0} style={{position:"absolute",left:80,top:1390,wordBreak:"keep-all"}} captions={[{"text": "AI 소식, 아직도 탭 열 개", "startMs": 0, "endMs": 2259, "timestampMs": 0, "confidence": null, "pageBreakAfter": true}, {"text": "켜서 찾으세요?", "startMs": 2260, "endMs": 3080, "timestampMs": 2260, "confidence": null, "pageBreakAfter": true}]}/></div></Series.Sequence>
<Series.Sequence name="Reveal" durationInFrames={163} premountFor={fps}><Reveal/>
<Audio name="한국어 보이스" src={staticFile("review-samples/AI001Review/voice-1.wav")} premountFor={fps}/>
<div className="review-captions"><BasicCaptions name="한글 자막" premountFor={fps} width={850} combineTokensWithinMilliseconds={0} style={{position:"absolute",left:80,top:1390,wordBreak:"keep-all"}} captions={[{"text": "최근 삼십 일 반응을 모아주는", "startMs": 0, "endMs": 2319, "timestampMs": 0, "confidence": null, "pageBreakAfter": true}, {"text": "스킬, 라스트 써티 데이즈입니다.", "startMs": 2320, "endMs": 4700, "timestampMs": 2320, "confidence": null, "pageBreakAfter": true}]}/></div></Series.Sequence>
<Series.Sequence name="Evidence" durationInFrames={217} premountFor={fps}><Evidence/>
<Audio name="한국어 보이스" src={staticFile("review-samples/AI001Review/voice-2.wav")} premountFor={fps}/>
<div className="review-captions"><BasicCaptions name="한글 자막" premountFor={fps} width={850} combineTokensWithinMilliseconds={0} style={{position:"absolute",left:80,top:1390,wordBreak:"keep-all"}} captions={[{"text": "깃허브 별 약 육만 칠천 개.", "startMs": 0, "endMs": 2580, "timestampMs": 0, "confidence": null, "pageBreakAfter": true}, {"text": "레딧, 엑스, 유튜브 반응을 출처와", "startMs": 2880, "endMs": 5719, "timestampMs": 2880, "confidence": null, "pageBreakAfter": true}, {"text": "함께 정리하죠.", "startMs": 5720, "endMs": 6620, "timestampMs": 5720, "confidence": null, "pageBreakAfter": true}]}/></div></Series.Sequence>
<Series.Sequence name="Example" durationInFrames={228} premountFor={fps}><Example/>
<Audio name="한국어 보이스" src={staticFile("review-samples/AI001Review/voice-3.wav")} premountFor={fps}/>
<div className="review-captions"><BasicCaptions name="한글 자막" premountFor={fps} width={850} combineTokensWithinMilliseconds={0} style={{position:"absolute",left:80,top:1390,wordBreak:"keep-all"}} captions={[{"text": "예를 들어, 요즘 많이 쓰는 PPT", "startMs": 0, "endMs": 3139, "timestampMs": 0, "confidence": null, "pageBreakAfter": true}, {"text": "AI 도구를 비교해 줘.", "startMs": 3140, "endMs": 4680, "timestampMs": 3140, "confidence": null, "pageBreakAfter": true}, {"text": "이렇게 주제를 넣는 거예요.", "startMs": 5200, "endMs": 6620, "timestampMs": 5200, "confidence": null, "pageBreakAfter": true}]}/></div></Series.Sequence>
<Series.Sequence name="Install" durationInFrames={193} premountFor={fps}><Install/>
<Audio name="한국어 보이스" src={staticFile("review-samples/AI001Review/voice-4.wav")} premountFor={fps}/>
<div className="review-captions"><BasicCaptions name="한글 자막" premountFor={fps} width={850} combineTokensWithinMilliseconds={0} style={{position:"absolute",left:80,top:1390,wordBreak:"keep-all"}} captions={[{"text": "클로드 코드에서 공식 안내대로", "startMs": 0, "endMs": 2379, "timestampMs": 0, "confidence": null, "pageBreakAfter": true}, {"text": "설치한 뒤, 이 명령어와 주제를", "startMs": 2380, "endMs": 4759, "timestampMs": 2380, "confidence": null, "pageBreakAfter": true}, {"text": "입력하세요.", "startMs": 4760, "endMs": 5480, "timestampMs": 4760, "confidence": null, "pageBreakAfter": true}]}/></div></Series.Sequence>
<Series.Sequence name="Limit" durationInFrames={127} premountFor={fps}><Limit/>
<Audio name="한국어 보이스" src={staticFile("review-samples/AI001Review/voice-5.wav")} premountFor={fps}/>
<div className="review-captions"><BasicCaptions name="한글 자막" premountFor={fps} width={850} combineTokensWithinMilliseconds={0} style={{position:"absolute",left:80,top:1390,wordBreak:"keep-all"}} captions={[{"text": "엑스나 유튜브는 추가 연결이 필요할", "startMs": 0, "endMs": 2879, "timestampMs": 0, "confidence": null, "pageBreakAfter": true}, {"text": "수 있습니다.", "startMs": 2880, "endMs": 3360, "timestampMs": 2880, "confidence": null, "pageBreakAfter": true}]}/></div></Series.Sequence>
<Series.Sequence name="Closing" durationInFrames={170} premountFor={fps}><Closing/>
<Audio name="한국어 보이스" src={staticFile("review-samples/AI001Review/voice-6.wav")} premountFor={fps}/>
<div className="review-captions"><BasicCaptions name="한글 자막" premountFor={fps} width={850} combineTokensWithinMilliseconds={0} style={{position:"absolute",left:80,top:1390,wordBreak:"keep-all"}} captions={[{"text": "처음엔 주제 하나만.", "startMs": 0, "endMs": 2040, "timestampMs": 0, "confidence": null, "pageBreakAfter": true}, {"text": "내 일에 쓸 수 있는지부터 확인하세요.", "startMs": 2380, "endMs": 4620, "timestampMs": 2380, "confidence": null, "pageBreakAfter": true}]}/></div></Series.Sequence>
</Series></>;};