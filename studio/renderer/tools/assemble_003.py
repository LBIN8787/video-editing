from pathlib import Path
import json,math
r=Path(__file__).resolve().parent.parent
words=json.loads((r/'research/episode-003/words.json').read_text())
# ASR checked against the authored script; form short readable caption pages.
caps=[]; group=[]
for w in words:
 if group and (len(' '.join(x['text'] for x in group))+1+len(w['text'])>22 or w['startMs']-group[-1]['endMs']>400):
  caps.append(dict(text=' '.join(x['text'] for x in group),startMs=group[0]['startMs'],endMs=group[-1]['endMs'],timestampMs=group[0]['startMs'],confidence=None,pageBreakAfter=True));group=[]
 group.append(w)
 if w['text'].endswith(('.','?','!')):
  caps.append(dict(text=' '.join(x['text'] for x in group),startMs=group[0]['startMs'],endMs=group[-1]['endMs'],timestampMs=group[0]['startMs'],confidence=None,pageBreakAfter=True));group=[]
if group:caps.append(dict(text=' '.join(x['text'] for x in group),startMs=group[0]['startMs'],endMs=group[-1]['endMs'],timestampMs=group[0]['startMs'],confidence=None,pageBreakAfter=True))
(r/'src/episode-003/captions.json').write_text(json.dumps(caps,ensure_ascii=False,indent=2))
bounds=[0,99,306,561,948,1149,1308,1500]
names=['Hook3','Features3','Setup3','Prompt3','Output3','Check3','Close3']
text="""import React from 'react';
import {Series,staticFile} from 'remotion';
import {Audio} from '@remotion/media';
import {BasicCaptions} from '../basic-captions';
import captions from './captions.json';
import {Hook3,Features3,Setup3,Prompt3,Output3,Check3,Close3} from './Visuals';
export const AIRadar003=()=> <>
<style>{`.ep003-captions > div > div {font-family:"Noto Sans CJK KR",sans-serif!important;font-weight:700!important;background:rgba(25,35,30,.96)!important;border:1px solid #ffffff20;border-radius:14px;font-size:54px!important;line-height:1.35!important;padding:18px 24px!important;}`}</style>
<Series>\n"""
for i,n in enumerate(names):text+=f'<Series.Sequence name="{n}" durationInFrames={{{bounds[i+1]-bounds[i]}}} premountFor={{30}}><{n}/></Series.Sequence>\n'
text+='</Series>\n<Audio name="ElevenLabs · Han Aim · eleven_v4" src={staticFile("episode-003/voice.mp3")}/>\n<div className="ep003-captions"><BasicCaptions name="한국어 자막" width={850} captions={captions} combineTokensWithinMilliseconds={0} style={{position:"absolute",left:80,top:1380,wordBreak:"keep-all"}}/></div></>;\n'
(r/'src/episode-003/AIRadar003.tsx').write_text(text)
p=r/'src/Root.tsx';s=p.read_text();s="import {AIRadar003} from './episode-003/AIRadar003';\n"+s;s=s.replace('export const Root=()=> <>','export const Root=()=> <>\n<Composition id="AIRadar003" component={AIRadar003} durationInFrames={1500} fps={30} width={1080} height={1920} />');p.write_text(s)
