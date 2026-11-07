#!/usr/bin/env python3
"""Render content through a versioned style; no paid TTS or upload calls."""
import argparse,hashlib,json,shutil,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
STYLE=ROOT/'styles/shorts-ai-guide';RENDERER=ROOT/'studio/renderer'
def style_lock(version,root=ROOT):
 if version not in ['1.0.0','1.1.0','1.1.1']:raise ValueError('Unsupported style version')
 base=root/'styles/shorts-ai-guide'
 return json.loads((base/('style-lock.json' if version=='1.0.0' else f'versions/{version}/style-lock.json')).read_text(encoding='utf-8'))
def validate_props(d,root=ROOT,allow_silent=False):
 lock=style_lock(d.get('style_version'),root)
 allowed={'style_version','episode','checkedAt','source','audio','captions','scenes'}
 if set(d)!=allowed or d['style_version']!=lock['version']:raise ValueError('Unexpected props or style version')
 if not d['episode'] or not d['checkedAt'] or not d['source'] or len(d['source'])>52:raise ValueError('Missing header/source or source too long')
 public=root/'studio/renderer/public'
 def asset(name):
  p=(public/name).resolve()
  if not p.is_relative_to(public.resolve()) or not p.is_file():raise ValueError('Missing local media asset: '+name)
 if d['audio']:asset(d['audio'])
 elif not allow_silent:raise ValueError('Narration missing; only --silent-preview can render without it')
 total=0
 if not 3<=len(d['scenes'])<=9:raise ValueError('Use 3–9 scenes')
 for scene in d['scenes']:
  fields={'id','frames','step','titleLines','items','dark','image'}
  if d['style_version']=='1.1.1':
   fields.update({'visual','action','visual_data'})
   from visual_brief import validate_visual_scene
   validate_visual_scene(scene)
   if scene['visual']=='image':asset(scene['visual_data']['image'])
  if d['style_version']=='1.1.0':
   fields.update({'visual','action'})
   if scene.get('visual') not in ['inconsistent','consistent','files','prompt','preview','outputs','setup','recap','audio','recognize','extract','sync','local','check']:raise ValueError('Unknown visual block')
   if not scene.get('action') or len(scene['action'])>60:raise ValueError('Needs a short actionable instruction')
   required={'preview':['visual-v2/remotion-poster.png'],'outputs':['visual-v2/remotion-poster.png','visual-v2/whisper-poster.png'],'audio':['visual-v2/voice-waveform.png'],'sync':['visual-v2/voice-waveform.png']}
   for name in required.get(scene['visual'],[]):asset(name)
  if set(scene)-fields:raise ValueError('Scene style overrides are forbidden')
  if not isinstance(scene['frames'],int) or not 1<=scene['frames']<=600:raise ValueError('Invalid scene duration')
  total+=scene['frames']
  if not 1<=len(scene['titleLines'])<=2 or any(not x or len(x)>10 for x in scene['titleLines']):raise ValueError('Title needs 1–2 short lines of at most 10 characters')
  if not 1<=len(scene['items'])<=(2 if scene.get('image') else 3) or any(len(x)>30 for x in scene['items']):raise ValueError('Card text exceeds fixed layout')
  if scene.get('image'):asset(scene['image'])
 if not 300<=total<=1800:raise ValueError('Short must be 10–60 seconds')
 previous=-1
 for cap in d['captions']:
  if not 0<=cap['startMs']<cap['endMs']<=total/30*1000 or cap['startMs']<previous:raise ValueError('Invalid caption timing')
  previous=cap['startMs']
 for item in json.loads((root/'styles/shorts-ai-guide/fonts.json').read_text())['assets']:
  p=public/item['path']
  if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=item['sha256']:raise ValueError('Pinned font missing or changed: '+item['path'])
 return total

def main():
 p=argparse.ArgumentParser();p.add_argument('--props',default=str(RENDERER/'src/template/reference-props.json'));p.add_argument('--out',default=str(RENDERER/'out/shorts-guide-v1-reference.mp4'));p.add_argument('--browser',default=shutil.which('chromium'));p.add_argument('--check-only',action='store_true');p.add_argument('--silent-preview',action='store_true');a=p.parse_args()
 props=Path(a.props).resolve();d=json.loads(props.read_text());frames=validate_props(d,allow_silent=a.silent_preview)
 if a.silent_preview and (d['audio'] or 'PREVIEW' not in Path(a.out).name):raise ValueError('Silent preview requires no narration and a PREVIEW output filename')
 if a.check_only:print(json.dumps({'style_version':d['style_version'],'frames':frames,'valid':True}));return
 if not a.browser:raise ValueError('Pass the installed Chromium path with --browser')
 lock=style_lock(d['style_version']);out=Path(a.out).resolve();out.parent.mkdir(parents=True,exist_ok=True);raw=out.with_name(out.stem+'-raw.mp4')
 subprocess.run(['npx','remotion','render','src/index.ts',lock['composition'],str(raw),'--props',str(props),'--codec=h264','--crf',str(lock['export']['crf']),'--pixel-format=yuv420p','--browser-executable',a.browser,'--concurrency=2'],cwd=RENDERER,check=True)
 audio_args=['-an'] if a.silent_preview else ['-af',f"loudnorm=I={lock['audio']['targetLufs']}:TP={lock['audio']['truePeakDb']}:LRA=8",'-ar','48000','-c:a','aac','-b:a','192k']
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(raw),'-c:v','copy',*audio_args,'-movflags','+faststart',str(out)],check=True)
 subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(out),'-f','null','-'],check=True)
 print(str(out))
if __name__=='__main__':main()
