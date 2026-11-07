#!/usr/bin/env python3
"""Compile content + cut plan + attention plan + replaceable graphic skin.

Changing a skin never edits the source plans, captions, narration or cut times.
"""
import argparse,hashlib,json,re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PALETTE={'ink','paper','accent','surface','subtle','muted','stroke','onAccent','inverse','inverseText','highlight'}

def digest(value):return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def validate_bundle(d):
 if set(d)!={'content','edit_points','emphasis','skin'}:raise ValueError('Unexpected renderer fields')
 content,cuts,points,skin=d['content'],d['edit_points'],d['emphasis'],d['skin']
 if points.get('reviewed',True) is not True:raise ValueError('Review the independent attention plan before rendering')
 if cuts.get('fps')!=30 or len(cuts.get('cuts',[]))!=len(content.get('scenes',[])):raise ValueError('Cut plan does not match content')
 if len({s['id'] for s in content['scenes']})!=len(content['scenes']):raise ValueError('Duplicate scene id')
 end=0;durations={}
 for cut,scene in zip(cuts['cuts'],content['scenes']):
  if cut['scene_id']!=scene['id'] or type(cut['start_frame'])!=int or cut['start_frame']!=end or type(cut['end_frame'])!=int or cut['end_frame']<=end or cut['transition']!='cut':raise ValueError('Cut timing or scene order changed')
  durations[scene['id']]=cut['end_frame']-end;end=cut['end_frame']
 if not 300<=end<=1800:raise ValueError('Shorts length outside bounds')
 if not content.get('audio'):raise ValueError('Layered final render needs the fixed narration')
 for scene_id,duration in durations.items():
  own=[p for p in points['points'] if p['scene_id']==scene_id];previous=0
  for p in own:
   if type(p['from_frame'])!=int or type(p['to_frame'])!=int or p['from_frame']!=previous or not p['from_frame']<p['to_frame']<=duration or p['focus_index'] not in [0,1,2] or p['method']!='outline' or not p['target'] or not p['label']:raise ValueError('Attention event is outside the shot or unsupported')
   previous=p['to_frame']
  if previous!=duration:raise ValueError('Attention plan must cover every scene')
 if any(p['scene_id'] not in durations for p in points['points']):raise ValueError('Unknown attention scene')
 if set(skin)!={'schema_version','id','name','palette','background','asset_overrides'} or set(skin['palette'])!=PALETTE or skin['background'] not in ['dots','grid','solid']:raise ValueError('Skin may contain graphics fields only')
 if any(not re.fullmatch(r'#[0-9a-fA-F]{6}',c) for c in skin['palette'].values()):raise ValueError('Palette needs hex colors')
 for scene_id,asset in skin['asset_overrides'].items():
  if scene_id not in durations or set(asset)!={'image','label','focus_regions'}:raise ValueError('Invalid graphic replacement')
  if not asset['image'] or not asset['label']:raise ValueError('Image needs a provenance label')
  for region in asset['focus_regions'].values():
   if len(region)!=4 or any(type(x) not in [int,float] or not 0<=x<=1 for x in region) or region[0]+region[2]>1 or region[1]+region[3]>1:raise ValueError('Focus region does not fit the replacement image')
 return {'cut_hash':digest(cuts),'attention_hash':digest(points),'content_hash':digest(content),'caption_hash':digest(content['captions']),'audio':content['audio'],'frames':end,'skin_id':skin['id']}

def compile_package(path,skin_path=None,root=ROOT,check_assets=True):
 root=root.resolve()
 def read(ref):
  file=(root/ref).resolve()
  if not file.is_relative_to(root):raise ValueError('Package references must stay inside the repository')
  return json.loads(file.read_text(encoding='utf-8'))
 package=read(str(path));d={'content':read(package['content_ref']),'edit_points':read(package['edit_points_ref']),'emphasis':read(package['emphasis_ref']),'skin':read(str(skin_path or package['skin_ref']))}
 if package.get('asset_bindings_ref'):
  bindings=read(package['asset_bindings_ref']);d['skin']['asset_overrides'].update(bindings.get(d['skin']['id'],{}))
 evidence=validate_bundle(d)
 if check_assets:
  public=(root/'studio/renderer/public').resolve()
  media=[d['content']['audio']]+[a['image'] for a in d['skin']['asset_overrides'].values()]+[s['visual_data']['image'] for s in d['content']['scenes'] if s['visual']=='image']
  for ref in media:
   file=(public/ref).resolve()
   if not file.is_relative_to(public) or not file.is_file():raise ValueError('Missing public media: '+ref)
  evidence['audio_sha256']=hashlib.sha256((public/d['content']['audio']).read_bytes()).hexdigest()
 return d,evidence

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--package',required=True);p.add_argument('--skin');p.add_argument('--out',type=Path,required=True);a=p.parse_args();d,checks=compile_package(a.package,a.skin);a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');a.out.with_name(a.out.stem+'-checks.json').write_text(json.dumps(checks,indent=2)+'\n',encoding='utf-8');print(json.dumps(checks))
if __name__=='__main__':main()
