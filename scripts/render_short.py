#!/usr/bin/env python3
"""Render content through a versioned style; no paid TTS or upload calls."""
import argparse,hashlib,json,shutil,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
STYLE=ROOT/'styles/shorts-ai-guide';RENDERER=ROOT/'studio/renderer'
def validate_props(d,root=ROOT):
 lock=json.loads((root/'styles/shorts-ai-guide/style-lock.json').read_text())
 allowed={'style_version','episode','checkedAt','source','audio','captions','scenes'}
 if set(d)!=allowed or d['style_version']!=lock['version']:raise ValueError('Unexpected props or style version')
 if not d['episode'] or not d['checkedAt'] or not d['source'] or len(d['source'])>52:raise ValueError('Missing header/source or source too long')
 public=root/'studio/renderer/public'
 def asset(name):
  p=(public/name).resolve()
  if not p.is_relative_to(public.resolve()) or not p.is_file():raise ValueError('Missing local media asset: '+name)
 asset(d['audio'])
 total=0
 if not 3<=len(d['scenes'])<=9:raise ValueError('Use 3–9 scenes')
 for scene in d['scenes']:
  if set(scene)-{'id','frames','step','titleLines','items','dark','image'}:raise ValueError('Scene style overrides are forbidden')
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
 p=argparse.ArgumentParser();p.add_argument('--props',default=str(RENDERER/'src/template/reference-props.json'));p.add_argument('--out',default=str(RENDERER/'out/shorts-guide-v1-reference.mp4'));p.add_argument('--browser',default=shutil.which('chromium'));p.add_argument('--check-only',action='store_true');a=p.parse_args()
 props=Path(a.props).resolve();d=json.loads(props.read_text());frames=validate_props(d)
 if a.check_only:print(json.dumps({'style_version':d['style_version'],'frames':frames,'valid':True}));return
 if not a.browser:raise ValueError('Pass the installed Chromium path with --browser')
 lock=json.loads((STYLE/'style-lock.json').read_text());out=Path(a.out).resolve();out.parent.mkdir(parents=True,exist_ok=True);raw=out.with_name(out.stem+'-raw.mp4')
 subprocess.run(['npx','remotion','render','src/index.ts',lock['composition'],str(raw),'--props',str(props),'--codec=h264','--crf',str(lock['export']['crf']),'--pixel-format=yuv420p','--browser-executable',a.browser,'--concurrency=2'],cwd=RENDERER,check=True)
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(raw),'-c:v','copy','-af',f"loudnorm=I={lock['audio']['targetLufs']}:TP={lock['audio']['truePeakDb']}:LRA=8",'-ar','48000','-c:a','aac','-b:a','192k','-movflags','+faststart',str(out)],check=True)
 subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(out),'-f','null','-'],check=True)
 print(str(out))
if __name__=='__main__':main()
