import React from 'react';
import {Series, staticFile, useVideoConfig} from 'remotion';
import {Audio} from '@remotion/media';
import {BasicCaptions} from './basic-captions';
import {Hook} from './Hook';
import {Reveal} from './Reveal';
import {Evidence} from './Evidence';
import {Example} from './Example';
import {Install} from './Install';
import {Limit} from './Limit';
import {Closing} from './Closing';
export const AIRadar=()=>{const {fps}=useVideoConfig();return <><style>{`.captions-look > div > div {font-family: "Noto Sans CJK KR", sans-serif !important; font-weight: 700 !important; background: rgba(25,35,30,.94) !important; border-radius: 14px; padding: 18px 24px !important;}`}</style><Series>
<Series.Sequence name="Hook" durationInFrames={131} premountFor={fps}>
<Hook />
<Audio name="한국어 내레이션" src={staticFile("voice-0.mp3")} premountFor={fps} volume={1} />
<div className="captions-look"><BasicCaptions name="한국어 자막" premountFor={fps} width={850} combineTokensWithinMilliseconds={0} style={{position:"absolute",left:80,top:1380,wordBreak:"keep-all"}} captions={[
  {
    "text": "AI 소식 아직도 탭 열 개",
    "startMs": 97,
    "endMs": 2305,
    "timestampMs": 97,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "켜서 찾으세요",
    "startMs": 2306,
    "endMs": 3524,
    "timestampMs": 2306,
    "confidence": null,
    "pageBreakAfter": true
  }
]} /></div>
</Series.Sequence>
<Series.Sequence name="Reveal" durationInFrames={160} premountFor={fps}>
<Reveal />
<Audio name="한국어 내레이션" src={staticFile("voice-1.mp3")} premountFor={fps} volume={1} />
<Audio name="전환 틱" src={staticFile("tick.wav")} volume={0.20} premountFor={fps} />
<div className="captions-look"><BasicCaptions name="한국어 자막" premountFor={fps} width={850} combineTokensWithinMilliseconds={0} style={{position:"absolute",left:80,top:1380,wordBreak:"keep-all"}} captions={[
  {
    "text": "최근 30일 반응을 모아주는",
    "startMs": 104,
    "endMs": 1913,
    "timestampMs": 104,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "스킬 last30days입니다",
    "startMs": 1914,
    "endMs": 4436,
    "timestampMs": 1914,
    "confidence": null,
    "pageBreakAfter": true
  }
]} /></div>
</Series.Sequence>
<Series.Sequence name="Evidence" durationInFrames={211} premountFor={fps}>
<Evidence />
<Audio name="한국어 내레이션" src={staticFile("voice-2.mp3")} premountFor={fps} volume={1} />
<Audio name="전환 틱" src={staticFile("tick.wav")} volume={0.20} premountFor={fps} />
<div className="captions-look"><BasicCaptions name="한국어 자막" premountFor={fps} width={850} combineTokensWithinMilliseconds={0} style={{position:"absolute",left:80,top:1380,wordBreak:"keep-all"}} captions={[
  {
    "text": "깃허브 별 약 6.7만 개",
    "startMs": 97,
    "endMs": 1884,
    "timestampMs": 97,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "레딧 엑스 유튜브 반응을 출처와",
    "startMs": 1885,
    "endMs": 4999,
    "timestampMs": 1885,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "함께 정리하죠",
    "startMs": 5000,
    "endMs": 6131,
    "timestampMs": 5000,
    "confidence": null,
    "pageBreakAfter": true
  }
]} /></div>
</Series.Sequence>
<Series.Sequence name="Example" durationInFrames={194} premountFor={fps}>
<Example />
<Audio name="한국어 내레이션" src={staticFile("voice-3.mp3")} premountFor={fps} volume={1} />
<Audio name="전환 틱" src={staticFile("tick.wav")} volume={0.20} premountFor={fps} />
<div className="captions-look"><BasicCaptions name="한국어 자막" premountFor={fps} width={850} combineTokensWithinMilliseconds={0} style={{position:"absolute",left:80,top:1380,wordBreak:"keep-all"}} captions={[
  {
    "text": "예를 들어 요즘 많이 쓰는 PPT",
    "startMs": 95,
    "endMs": 2508,
    "timestampMs": 95,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "AI 도구를 비교해 줘 이렇게",
    "startMs": 2509,
    "endMs": 4286,
    "timestampMs": 2509,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "주제를 넣는 거예요",
    "startMs": 4287,
    "endMs": 5612,
    "timestampMs": 4287,
    "confidence": null,
    "pageBreakAfter": true
  }
]} /></div>
</Series.Sequence>
<Series.Sequence name="Install" durationInFrames={178} premountFor={fps}>
<Install />
<Audio name="한국어 내레이션" src={staticFile("voice-4.mp3")} premountFor={fps} volume={1} />
<Audio name="전환 틱" src={staticFile("tick.wav")} volume={0.20} premountFor={fps} />
<div className="captions-look"><BasicCaptions name="한국어 자막" premountFor={fps} width={850} combineTokensWithinMilliseconds={0} style={{position:"absolute",left:80,top:1380,wordBreak:"keep-all"}} captions={[
  {
    "text": "클로드 코드에서 공식 안내대로",
    "startMs": 97,
    "endMs": 1938,
    "timestampMs": 97,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "설치한 뒤 이 명령어와 주제를",
    "startMs": 1939,
    "endMs": 4201,
    "timestampMs": 1939,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "입력하세요",
    "startMs": 4202,
    "endMs": 5129,
    "timestampMs": 4202,
    "confidence": null,
    "pageBreakAfter": true
  }
]} /></div>
</Series.Sequence>
<Series.Sequence name="Limit" durationInFrames={119} premountFor={fps}>
<Limit />
<Audio name="한국어 내레이션" src={staticFile("voice-5.mp3")} premountFor={fps} volume={1} />
<Audio name="전환 틱" src={staticFile("tick.wav")} volume={0.20} premountFor={fps} />
<div className="captions-look"><BasicCaptions name="한국어 자막" premountFor={fps} width={850} combineTokensWithinMilliseconds={0} style={{position:"absolute",left:80,top:1380,wordBreak:"keep-all"}} captions={[
  {
    "text": "엑스나 유튜브는 추가 연결이",
    "startMs": 100,
    "endMs": 1985,
    "timestampMs": 100,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "필요할 수 있습니다",
    "startMs": 1986,
    "endMs": 3150,
    "timestampMs": 1986,
    "confidence": null,
    "pageBreakAfter": true
  }
]} /></div>
</Series.Sequence>
<Series.Sequence name="Closing" durationInFrames={173} premountFor={fps}>
<Closing />
<Audio name="한국어 내레이션" src={staticFile("voice-6.mp3")} premountFor={fps} volume={1} />
<Audio name="전환 틱" src={staticFile("tick.wav")} volume={0.20} premountFor={fps} />
<div className="captions-look"><BasicCaptions name="한국어 자막" premountFor={fps} width={850} combineTokensWithinMilliseconds={0} style={{position:"absolute",left:80,top:1380,wordBreak:"keep-all"}} captions={[
  {
    "text": "처음엔 주제 하나만 내 일에",
    "startMs": 97,
    "endMs": 2975,
    "timestampMs": 97,
    "confidence": null,
    "pageBreakAfter": true
  },
  {
    "text": "쓸 수 있는지부터 확인하세요",
    "startMs": 2976,
    "endMs": 4894,
    "timestampMs": 2976,
    "confidence": null,
    "pageBreakAfter": true
  }
]} /></div>
</Series.Sequence>
</Series></>;};
