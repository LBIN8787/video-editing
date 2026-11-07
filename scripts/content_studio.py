#!/usr/bin/env python3
"""Create repeatable editorial projects; never generates paid media or publishes."""
import argparse,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'studio/automation'))
from work_cases import create_case,safe_case_id,DOMAINS

def slug(value):
 if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',value):raise ValueError('Use lowercase letters, digits and hyphens for IDs')
 return value

def create(channel,topic,episode,style,root=ROOT,work_case=None):
 for value in [channel,topic,episode,style]:slug(value)
 profile=root/'channels'/channel/'channel.json'
 config=json.loads(profile.read_text())
 if style not in config['allowed_styles']:raise ValueError('Style is not allowed for this channel')
 if channel=='ai':
  if not work_case:raise ValueError('AI episodes must link an actual work case; create one first')
  safe_case_id(work_case)
  if not (root/'work-cases'/work_case/'case.json').is_file():raise ValueError('Work case does not exist')
 spec=json.loads((root/'styles'/style/'profile.json').read_text())
 folder=root/'channels'/channel/'episodes'/episode
 if folder.exists():raise FileExistsError('Episode already exists; continue its records instead of overwriting')
 shared=root/'content/topics'/topic;shared.mkdir(parents=True,exist_ok=True)
 for name,text in {
  'sources.json':json.dumps({'topic':topic,'checked_at':None,'sources':[]},ensure_ascii=False,indent=2)+'\n',
  'research.md':'# 조사 원장\n\n## 핵심 질문\n\n## 확인된 사실 / 출처 ID\n\n## 미확인·반론\n\n## 활용과 실행 조건\n',
  'article.md':'# 조사 글 / 안내문 / 칼럼\n\n상태: 초안 작성 전\n\n## 질문과 핵심 주장\n\n## 근거와 설명\n\n## 적용 사례\n\n## 한계와 반론\n\n## 판단과 활용\n'
 }.items():
  p=shared/name
  if not p.exists():p.write_text(text,encoding='utf-8')
 folder.mkdir(parents=True)
 plan={'schema_version':1,'id':episode,'channel':channel,'topic':topic,'style':style,'format':spec['format'],'source_ref':f'content/topics/{topic}/sources.json','research_ref':f'content/topics/{topic}/research.md','article_ref':f'content/topics/{topic}/article.md','voice_ref':f'channels/{channel}/channel.json#/voice','state':'draft','publish_allowed':False}
 if style=='shorts-ai-guide':plan.update(style_version=spec['version'],renderer_ref=f"studio/renderer/src/template/{spec.get('composition','ShortsGuideV1')}.tsx")
 if work_case:plan.update(content_mode='applied_work',work_case_ref=f'work-cases/{work_case}/case.json')
 (folder/'plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (folder/'script.md').write_text('# 대본\n\n'+ '\n\n'.join('## '+x for x in spec['outline'])+'\n',encoding='utf-8')
 (folder/'storyboard.md').write_text('# 장면 구성\n\n| 구간 | 내레이션 | 화면·자료 | 출처 ID | 실제/설명용 |\n|---|---|---|---|---|\n',encoding='utf-8')
 (folder/'review.md').write_text('# 검수\n\n미검수. 출처·내용·고정 보이스·장면·자막·최종 MP4를 확인하기 전 게시하지 않는다.\n',encoding='utf-8')
 return folder

def inspect(root=ROOT):
 rows=[]
 for p in sorted((root/'channels').glob('*/episodes/*/*.json')):
  if p.name not in ['plan.json','episode.json']:continue
  d=json.loads(p.read_text());rows.append({'path':p.parent.relative_to(root).as_posix(),'channel':d['channel'],'style':d['style'],'format':d['format'],'state':d.get('state',d.get('status'))})
 return rows

def main():
 parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
 p=sub.add_parser('new');p.add_argument('--channel',choices=['ai','quiz'],required=True);p.add_argument('--topic',required=True);p.add_argument('--episode',required=True);p.add_argument('--style',required=True);p.add_argument('--work-case')
 p=sub.add_parser('work-case');p.add_argument('--id',required=True);p.add_argument('--domain',choices=DOMAINS,default='video-channel')
 sub.add_parser('inventory');a=parser.parse_args()
 if a.command=='new':print(create(a.channel,a.topic,a.episode,a.style,work_case=a.work_case).relative_to(ROOT))
 elif a.command=='work-case':print(create_case(a.id,domain=a.domain).relative_to(ROOT))
 else:print(json.dumps(inspect(),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
