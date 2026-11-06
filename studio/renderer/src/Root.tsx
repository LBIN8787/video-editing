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
import {Composition,Folder} from 'remotion';
import {AIRadar} from './AIRadar';
import {Hook} from './Hook';
import {Reveal} from './Reveal';
import {Evidence} from './Evidence';
import {Example} from './Example';
import {Install} from './Install';
import {Limit} from './Limit';
import {Closing} from './Closing';
export const Root=()=> <>
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
