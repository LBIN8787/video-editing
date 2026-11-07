import {LayeredShorts} from './layered/LayeredShorts';
import layeredExample from '../../../channels/ai/episodes/006-whisper/layers/paper-props.json';
import {ShortsCover} from './packaging/ShortsCover';
import {ShortsGuideTemplate} from './template/ShortsGuideTemplate';
import genericExample from '../../../channels/ai/episodes/003-xlsx/revisions/visual-v2/props.json';
import {ShortsGuideV2} from './template/ShortsGuideV2';
import visual005 from '../../../channels/ai/episodes/005-remotion/revisions/visual-v2/props.json';
import visual006 from '../../../channels/ai/episodes/006-whisper/revisions/visual-v2/props.json';
import {ShortsGuideV1} from './template/ShortsGuideV1';
import referenceProps from './template/reference-props.json';
import {AIRadar003} from './episode-003/AIRadar003';
import {Quiz002} from './review-samples/Quiz002';
import {Quiz001} from './review-samples/Quiz001';
import {AI001Review} from './review-samples/AI001Review';
import {Closing2} from './episode-002/Closing2';
import {Setup2} from './episode-002/Setup2';
import {Prompt2} from './episode-002/Prompt2';
import {Edit2} from './episode-002/Edit2';
import {Workflow2} from './episode-002/Workflow2';
import {Reveal2} from './episode-002/Reveal2';
import {Hook2} from './episode-002/Hook2';
import {AIRadar002} from './episode-002/AIRadar002';
import React from 'react';
import {Composition,Folder,Still} from 'remotion';
import {AIRadar} from './AIRadar';
import {Hook} from './Hook';
import {Reveal} from './Reveal';
import {Evidence} from './Evidence';
import {Example} from './Example';
import {Install} from './Install';
import {Limit} from './Limit';
import {Closing} from './Closing';
export const Root=()=> <>
<Composition id="LayeredShorts" component={LayeredShorts} defaultProps={layeredExample} calculateMetadata={({props})=>({durationInFrames:props.edit_points.cuts[props.edit_points.cuts.length-1].end_frame})} durationInFrames={1496} fps={30} width={1080} height={1920}/>
<Still id="ShortsCoverVertical" component={ShortsCover} width={1080} height={1920} defaultProps={{topic:"remotion",headline:["디자인은 고정","내용만 교체"],tool:"Remotion",subline:"같은 스타일로 반복 제작하는 법"}}/>
<Still id="ShortsThumbnailWide" component={ShortsCover} width={1280} height={720} defaultProps={{topic:"remotion",headline:["디자인은 고정","내용만 교체"],tool:"Remotion",subline:"같은 스타일로 반복 제작하는 법"}}/>
<Composition id="ShortsGuideTemplate" component={ShortsGuideTemplate} defaultProps={genericExample} calculateMetadata={({props})=>({durationInFrames:props.scenes.reduce((n,s)=>n+s.frames,0)})} durationInFrames={1500} fps={30} width={1080} height={1920}/>
<Composition id="ShortsGuideV2" component={ShortsGuideV2} defaultProps={visual005} calculateMetadata={({props})=>({durationInFrames:props.scenes.reduce((n,s)=>n+s.frames,0)})} durationInFrames={1376} fps={30} width={1080} height={1920}/>
<Composition id="WhisperVisualGuide" component={ShortsGuideV2} defaultProps={visual006} durationInFrames={1496} fps={30} width={1080} height={1920}/>
<Composition id="ShortsGuideV1" component={ShortsGuideV1} defaultProps={referenceProps} calculateMetadata={({props})=>({durationInFrames:props.scenes.reduce((total,scene)=>total+scene.frames,0)})} durationInFrames={1500} fps={30} width={1080} height={1920} />
<Composition id="AIRadar003" component={AIRadar003} durationInFrames={1500} fps={30} width={1080} height={1920} />
<Composition id="Quiz002" component={Quiz002} durationInFrames={1166} fps={30} width={1080} height={1920} />
<Composition id="Quiz001" component={Quiz001} durationInFrames={1024} fps={30} width={1080} height={1920} />
<Composition id="AI001Review" component={AI001Review} durationInFrames={1211} fps={30} width={1080} height={1920} />
<Composition id="AIRadar" component={AIRadar} durationInFrames={1166} fps={30} width={1080} height={1920} />
<Composition id="AIRadar002" component={AIRadar002} durationInFrames={1599} fps={30} width={1080} height={1920} />
<Folder name="Scenes">
<Composition id="Hook" component={Hook} durationInFrames={131} fps={30} width={1080} height={1920} />
<Composition id="Reveal" component={Reveal} durationInFrames={160} fps={30} width={1080} height={1920} />
<Composition id="Evidence" component={Evidence} durationInFrames={211} fps={30} width={1080} height={1920} />
<Composition id="Example" component={Example} durationInFrames={194} fps={30} width={1080} height={1920} />
<Composition id="Install" component={Install} durationInFrames={178} fps={30} width={1080} height={1920} />
<Composition id="Limit" component={Limit} durationInFrames={119} fps={30} width={1080} height={1920} />
<Composition id="Closing" component={Closing} durationInFrames={173} fps={30} width={1080} height={1920} />
</Folder><Folder name="Episode002-Scenes">
<Composition id="Hook002" component={Hook2} durationInFrames={161} fps={30} width={1080} height={1920} />
<Composition id="Reveal002" component={Reveal2} durationInFrames={233} fps={30} width={1080} height={1920} />
<Composition id="Workflow002" component={Workflow2} durationInFrames={193} fps={30} width={1080} height={1920} />
<Composition id="Edit002" component={Edit2} durationInFrames={169} fps={30} width={1080} height={1920} />
<Composition id="Prompt002" component={Prompt2} durationInFrames={226} fps={30} width={1080} height={1920} />
<Composition id="Setup002" component={Setup2} durationInFrames={224} fps={30} width={1080} height={1920} />
<Composition id="Closing002" component={Closing2} durationInFrames={253} fps={30} width={1080} height={1920} />
</Folder>
</>;
