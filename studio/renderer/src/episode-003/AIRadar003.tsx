import React from 'react';
import {Series,staticFile} from 'remotion';
import {Audio} from '@remotion/media';
import {BasicCaptions} from '../basic-captions';
import captions from './captions.json';
import {Hook3,Features3,Setup3,Prompt3,Output3,Check3,Close3} from './Visuals';
export const AIRadar003=()=> <>
<style>{`.ep003-captions > div > div {font-family:"Noto Sans CJK KR",sans-serif!important;font-weight:700!important;background:rgba(25,35,30,.96)!important;border:1px solid #ffffff20;border-radius:14px;font-size:54px!important;line-height:1.35!important;padding:18px 24px!important;}`}</style>
<Series>
<Series.Sequence name="Hook3" durationInFrames={99} premountFor={30}><Hook3/></Series.Sequence>
<Series.Sequence name="Features3" durationInFrames={207} premountFor={30}><Features3/></Series.Sequence>
<Series.Sequence name="Setup3" durationInFrames={255} premountFor={30}><Setup3/></Series.Sequence>
<Series.Sequence name="Prompt3" durationInFrames={387} premountFor={30}><Prompt3/></Series.Sequence>
<Series.Sequence name="Output3" durationInFrames={201} premountFor={30}><Output3/></Series.Sequence>
<Series.Sequence name="Check3" durationInFrames={159} premountFor={30}><Check3/></Series.Sequence>
<Series.Sequence name="Close3" durationInFrames={192} premountFor={30}><Close3/></Series.Sequence>
</Series>
<Audio name="ElevenLabs · Han Aim · eleven_v4" src={staticFile("episode-003/voice.mp3")}/>
<div className="ep003-captions"><BasicCaptions name="한국어 자막" width={850} captions={captions} combineTokensWithinMilliseconds={0} style={{position:"absolute",left:80,top:1380,wordBreak:"keep-all"}}/></div></>;
