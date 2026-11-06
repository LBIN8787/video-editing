import React from 'react';
import {Series,staticFile,useVideoConfig} from 'remotion';
import {Audio} from '@remotion/media';
import {BasicCaptions} from '../basic-captions';
import {Hook2} from './Hook2';
import {Reveal2} from './Reveal2';
import {Workflow2} from './Workflow2';
import {Edit2} from './Edit2';
import {Prompt2} from './Prompt2';
import {Setup2} from './Setup2';
import {Closing2} from './Closing2';
export const AIRadar002=()=>{const {fps}=useVideoConfig();return <><style>{`.captions-look > div > div {font-family:"Noto Sans CJK KR",sans-serif!important;font-weight:700!important;background:rgba(25,35,30,.94)!important;border-radius:14px;padding:18px 24px!important;}`}</style><Series>
<Series.Sequence name="Hook" durationInFrames={161} premountFor={fps}>
<Hook2/>
<Audio name="Supertonic 3 한국어 음성" src={staticFile("episode-002/voice-0.wav")} premountFor={fps}/>
<div className="captions-look"><BasicCaptions name="한국어 자막" premountFor={fps} width={850} combineTokensWithinMilliseconds={0} style={{position:"absolute",left:80,top:1380,wordBreak:"keep-all"}} captions={[
  {
    "text": "AI가 만든 PPT, 글자",
    "startMs": 0,
    "endMs": 2859,
    "timestampMs": 0,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "하나 바꾸려다 막힌 적 있죠?",
    "startMs": 2860,
    "endMs": 4440,
    "timestampMs": 2860,
    "confidence": null,
    "pageBreakAfter": true
  }
]}/></div>
</Series.Sequence>
<Series.Sequence name="Reveal" durationInFrames={274} premountFor={fps}>
<Reveal2/>
<Audio name="Supertonic 3 한국어 음성" src={staticFile("episode-002/voice-1.wav")} premountFor={fps}/>
<div className="captions-look"><BasicCaptions name="한국어 자막" premountFor={fps} width={850} combineTokensWithinMilliseconds={0} style={{position:"absolute",left:80,top:1380,wordBreak:"keep-all"}} captions={[
  {
    "text": "PPT Master는 문서를 발표 자료로",
    "startMs": 0,
    "endMs": 3099,
    "timestampMs": 0,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "바꾸고, 글자와 도형, 차트까지",
    "startMs": 3100,
    "endMs": 6139,
    "timestampMs": 3100,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "수정할 수 있게 만드는 스킬이에요.",
    "startMs": 6140,
    "endMs": 8180,
    "timestampMs": 6140,
    "confidence": null,
    "pageBreakAfter": true
  }
]}/></div>
</Series.Sequence>
<Series.Sequence name="Workflow" durationInFrames={193} premountFor={fps}>
<Workflow2/>
<Audio name="Supertonic 3 한국어 음성" src={staticFile("episode-002/voice-2.wav")} premountFor={fps}/>
<div className="captions-look"><BasicCaptions name="한국어 자막" premountFor={fps} width={850} combineTokensWithinMilliseconds={0} style={{position:"absolute",left:80,top:1380,wordBreak:"keep-all"}} captions={[
  {
    "text": "문서나 주제를 주면, PowerPoint에서",
    "startMs": 0,
    "endMs": 3299,
    "timestampMs": 0,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "고칠 수 있는 파일로 만들어 줘요.",
    "startMs": 3300,
    "endMs": 5600,
    "timestampMs": 3300,
    "confidence": null,
    "pageBreakAfter": true
  }
]}/></div>
</Series.Sequence>
<Series.Sequence name="Edit" durationInFrames={169} premountFor={fps}>
<Edit2/>
<Audio name="Supertonic 3 한국어 음성" src={staticFile("episode-002/voice-3.wav")} premountFor={fps}/>
<div className="captions-look"><BasicCaptions name="한국어 자막" premountFor={fps} width={850} combineTokensWithinMilliseconds={0} style={{position:"absolute",left:80,top:1380,wordBreak:"keep-all"}} captions={[
  {
    "text": "글자, 도형, 차트를 나중에 직접",
    "startMs": 0,
    "endMs": 2919,
    "timestampMs": 0,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "손볼 수 있다는 게 포인트죠.",
    "startMs": 2920,
    "endMs": 4800,
    "timestampMs": 2920,
    "confidence": null,
    "pageBreakAfter": true
  }
]}/></div>
</Series.Sequence>
<Series.Sequence name="Prompt" durationInFrames={226} premountFor={fps}>
<Prompt2/>
<Audio name="Supertonic 3 한국어 음성" src={staticFile("episode-002/voice-4.wav")} premountFor={fps}/>
<div className="captions-look"><BasicCaptions name="한국어 자막" premountFor={fps} width={850} combineTokensWithinMilliseconds={0} style={{position:"absolute",left:80,top:1380,wordBreak:"keep-all"}} captions={[
  {
    "text": "예를 들면 이렇게요.",
    "startMs": 0,
    "endMs": 1780,
    "timestampMs": 0,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "이 문서를 발표용 5장으로",
    "startMs": 2260,
    "endMs": 4139,
    "timestampMs": 2260,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "만들고, 발표자 노트도 넣어 줘.",
    "startMs": 4140,
    "endMs": 6680,
    "timestampMs": 4140,
    "confidence": null,
    "pageBreakAfter": true
  }
]}/></div>
</Series.Sequence>
<Series.Sequence name="Setup" durationInFrames={323} premountFor={fps}>
<Setup2/>
<Audio name="Supertonic 3 한국어 음성" src={staticFile("episode-002/voice-5.wav")} premountFor={fps}/>
<div className="captions-look"><BasicCaptions name="한국어 자막" premountFor={fps} width={850} combineTokensWithinMilliseconds={0} style={{position:"absolute",left:80,top:1380,wordBreak:"keep-all"}} captions={[
  {
    "text": "설치한 프로젝트 폴더에 문서를",
    "startMs": 0,
    "endMs": 2579,
    "timestampMs": 0,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "넣고, AI 채팅에서 제작을",
    "startMs": 2580,
    "endMs": 5359,
    "timestampMs": 2580,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "요청하세요.",
    "startMs": 5360,
    "endMs": 6020,
    "timestampMs": 5360,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "완성 파일은 PowerPoint로 열어",
    "startMs": 6640,
    "endMs": 9079,
    "timestampMs": 6640,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "수정하면 돼요.",
    "startMs": 9080,
    "endMs": 9960,
    "timestampMs": 9080,
    "confidence": null,
    "pageBreakAfter": true
  }
]}/></div>
</Series.Sequence>
<Series.Sequence name="Closing" durationInFrames={253} premountFor={fps}>
<Closing2/>
<Audio name="Supertonic 3 한국어 음성" src={staticFile("episode-002/voice-6.wav")} premountFor={fps}/>
<div className="captions-look"><BasicCaptions name="한국어 자막" premountFor={fps} width={850} combineTokensWithinMilliseconds={0} style={{position:"absolute",left:80,top:1380,wordBreak:"keep-all"}} captions={[
  {
    "text": "처음엔 문서 한 장으로 시작해",
    "startMs": 0,
    "endMs": 2639,
    "timestampMs": 0,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "보세요.",
    "startMs": 2640,
    "endMs": 2920,
    "timestampMs": 2640,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "결과가 예쁜지, 수정도 되는지",
    "startMs": 3640,
    "endMs": 6139,
    "timestampMs": 3640,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "같이 확인하는 거예요.",
    "startMs": 6140,
    "endMs": 7380,
    "timestampMs": 6140,
    "confidence": null,
    "pageBreakAfter": true
  }
]}/></div>
</Series.Sequence>
</Series></>;};
