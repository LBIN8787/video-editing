#!/usr/bin/env python3
"""Export reviewed visual props into independent content/cuts/attention/skin files."""
import argparse,json
from pathlib import Path
from render_short import ROOT,validate_props

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--props',type=Path,required=True);p.add_argument('--out-dir',type=Path,required=True);p.add_argument('--packaging',required=True);a=p.parse_args()
 props=json.loads(a.props.read_text(encoding='utf-8'));validate_props(props)
 if props['style_version']!='1.1.1':raise ValueError('Layer export needs reusable visual_data; keep older revisions intact')
 out=a.out_dir.resolve()
 if not out.is_relative_to(ROOT):raise ValueError('Keep the package inside the project')
 names=['content.json','edit-points.json','emphasis.json','asset-bindings.json','production-package.json']
 if any((out/name).exists() for name in names):raise FileExistsError('An authored layer file already exists; continue it instead of overwriting')
 content={k:props[k] for k in ['episode','source','audio','captions']};content['scenes']=[{k:v for k,v in scene.items() if k!='frames'} for scene in props['scenes']]
 cuts=[];cursor=0
 for scene in props['scenes']:
  cuts.append(dict(scene_id=scene['id'],start_frame=cursor,end_frame=cursor+scene['frames'],transition='cut',reason=scene['step']));cursor+=scene['frames']
 package=dict(schema_version=1,episode=props['episode'],content_ref=str((out/'content.json').relative_to(ROOT)),edit_points_ref=str((out/'edit-points.json').relative_to(ROOT)),emphasis_ref=str((out/'emphasis.json').relative_to(ROOT)),skin_ref='styles/shorts-ai-guide/skins/paper-lime.json',asset_bindings_ref=str((out/'asset-bindings.json').relative_to(ROOT)),packaging_ref=a.packaging,publish_allowed=False)
 out.mkdir(parents=True,exist_ok=True)
 for name,data in [('content.json',content),('edit-points.json',{'schema_version':1,'fps':30,'cuts':cuts}),('emphasis.json',{'schema_version':1,'reviewed':False,'points':[]}),('asset-bindings.json',{}),('production-package.json',package)]:
  (out/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('Exported exact cut times. Author and review emphasis.json before compiling a skin.')
if __name__=='__main__':main()
