#!/usr/bin/env python3
"""Prepare reusable visual props from an authored brief and local word timings.

Never generates speech or publishes. Missing fixed narration stops final prep.
"""
import argparse,hashlib,json,math,re,subprocess,sys
from pathlib import Path
from render_short import ROOT,validate_props
sys.path.insert(0,str(ROOT/'studio/automation'))
from work_cases import validate_case

def norm(value):return re.sub(r'[^가-힣a-z0-9]','',value.lower())

def group_captions(words):
 groups=[];group=[]
 for word in words:
  if group and (len(' '.join(w['text'] for w in group))+len(word['text'])+1>26 or word['startMs']-group[-1]['endMs']>400):groups.append(group);group=[]
  group.append(word)
  if word['text'].endswith(('.', '?', '!')):groups.append(group);group=[]
 if group:groups.append(group)
 return [dict(text=' '.join(w['text'] for w in row),startMs=row[0]['startMs'],endMs=row[-1]['endMs'],timestampMs=row[0]['startMs'],confidence=None,pageBreakAfter=True) for row in groups]

def prepare(brief,words=None,silent=False,root=ROOT):
 if brief.get('channel')!='ai' or brief.get('editorial_reviewed') is not True:raise ValueError('AI brief must be editorially reviewed')
 if not brief.get('source_urls') or not brief.get('source_checked_at'):raise ValueError('Recheck and record official sources')
 for key in ['input','action','output']:
  if not brief.get('core_task',{}).get(key):raise ValueError('State the concrete input, action and output')
 if brief.get('content_mode')=='applied_work':validate_case(brief['work_case_ref'],root)
 elif brief.get('content_mode')!='historical_illustrative_refresh':raise ValueError('Unsupported content mode')
 scenes=brief['scenes'];voice=brief.get('voice',{});profile=json.loads((root/'channels/ai/channel.json').read_text(encoding='utf-8'));expected=profile['voice']
 if not 3<=len(scenes)<=9 or any(not s.get('narration') for s in scenes):raise ValueError('Each scene needs authored narration')
 if silent:
  seconds=brief.get('target_seconds',50)
  if not 10<=seconds<=60:raise ValueError('Preview must fit Shorts length')
  weights=[len(s['narration']) for s in scenes];frames=[round(w/sum(weights)*seconds*30) for w in weights];frames[-1]+=round(seconds*30)-sum(frames)
  output_scenes=[];caps=[];start=0
  for scene,count in zip(scenes,frames):
   row={k:v for k,v in scene.items() if k not in ['narration','start_ms']};row['frames']=count;output_scenes.append(row)
   tokens=scene['narration'].split();total=sum(map(len,tokens));cursor=start/30*1000;items=[]
   for token in tokens:
    end=cursor+len(token)/total*(count/30*1000);items.append(dict(text=token,startMs=round(cursor),endMs=round(end)));cursor=end
   caps.extend(group_captions(items));start+=count
  audio='';mode='estimated_silent_preview'
 else:
  if voice.get('status')!='ready' or not words:raise ValueError('Fixed narration and word timings required; provider busy is not a fallback')
  asset=(root/'studio/renderer/public'/voice['asset']).resolve();public=(root/'studio/renderer/public').resolve()
  if not asset.is_relative_to(public) or not asset.is_file():raise ValueError('Missing local voice asset')
  metadata_path=(root/voice['metadata_ref']).resolve()
  if not metadata_path.is_relative_to(root.resolve()):raise ValueError('Metadata must be inside the project')
  metadata=json.loads(metadata_path.read_text(encoding='utf-8'))
  if any(metadata.get(k)!=expected[k] for k in ['provider','voice_id','model_id']) or metadata.get('fallback_used') is not False:raise ValueError('Fixed voice mismatch')
  if hashlib.sha256(asset.read_bytes()).hexdigest()!=metadata.get('sha256',metadata.get('narration_sha256')):raise ValueError('Voice asset checksum mismatch')
  duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(asset)]));total=math.ceil((duration+.3)*30)
  starts=[];cursor=0
  for scene in scenes:
   if 'start_ms' in scene:ms=scene['start_ms']
   else:
    prefix=norm(scene['narration'])[:12];found=[i for i in range(cursor,len(words)) if ''.join(norm(w['text']) for w in words[i:i+9]).startswith(prefix)]
    if not found:raise ValueError('Scene alignment needs review; supply an approved start_ms: '+scene['id'])
    cursor=found[0]+1;ms=words[found[0]]['startMs']
   starts.append(round(ms*30/1000))
  starts[0]=0;output_scenes=[]
  for i,scene in enumerate(scenes):
   row={k:v for k,v in scene.items() if k not in ['narration','start_ms']};row['frames']=(starts[i+1] if i+1<len(starts) else total)-starts[i];output_scenes.append(row)
  caps=group_captions(words);audio=voice['asset'];mode='reviewed_word_timing'
 props=dict(style_version=profile['shorts_style_version'],episode=brief['episode'],checkedAt=brief['source_checked_at'],source=brief['source_label'],audio=audio,captions=caps,scenes=output_scenes)
 validate_props(props,root,allow_silent=silent)
 return props,dict(timing_mode=mode,publish_allowed=False,voice_status=voice.get('status','pending'))

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--brief',type=Path,required=True);p.add_argument('--words',type=Path);p.add_argument('--out',type=Path,required=True);p.add_argument('--silent-preview',action='store_true');p.add_argument('--export-narration',action='store_true');a=p.parse_args()
 brief=json.loads(a.brief.read_text(encoding='utf-8'))
 if a.export_narration:
  if brief.get('editorial_reviewed') is not True or any(not s.get('narration') for s in brief['scenes']):raise ValueError('Review the authored narration first')
  a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(' '.join(s['narration'] for s in brief['scenes'])+'\n',encoding='utf-8');print(a.out);return
 raw=json.loads(a.words.read_text(encoding='utf-8')) if a.words else None;words=raw.get('words',[]) if isinstance(raw,dict) else raw
 props,status=prepare(brief,words,a.silent_preview);a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(props,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');a.out.with_name(a.out.stem+'-prep-status.json').write_text(json.dumps(status,indent=2)+'\n',encoding='utf-8');print(a.out)
if __name__=='__main__':main()
