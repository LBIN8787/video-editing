"""CI check of shared workflow configuration; does not need private media or OAuth."""
import json
from pathlib import Path
from visual_brief import KINDS

ROOT=Path(__file__).resolve().parents[1]
def read(path):return json.loads((ROOT/path).read_text(encoding='utf-8'))

def main():
 channel=read('channels/ai/channel.json');profile=read('styles/shorts-ai-guide/profile.json')
 assert channel['shorts_style_version']==profile['version']
 lock=read('styles/shorts-ai-guide/'+profile['lock_file'])
 assert lock['version']==profile['version'] and lock['composition']==profile['composition']==channel['preferred_composition']
 assert channel['preferred_composition'] in channel['allowed_compositions']
 assert lock['header']=={'showDate':False,'showEpisodeNumber':False}
 assert channel['voice']['voice_id']==lock['audio']['voiceId'] and channel['voice']['model_id']==lock['audio']['modelId']
 assert not channel['voice']['fallback_allowed'] and not lock['audio']['transitionSfx'] and not lock['audio']['bgm']
 schema=read('schemas/shorts-production-brief.schema.json');template=read('studio/templates/shorts/production-brief.template.json')
 assert set(schema['required'])==set(template) and set(schema['properties']['scenes']['items']['properties']['visual']['enum'])==KINDS
 assert template['voice']['status']=='pending' and template['editorial_reviewed'] is False
 root=(ROOT/'studio/renderer/src/Root.tsx').read_text(encoding='utf-8');assert f'id="{profile["composition"]}"' in root
 for p in (ROOT/'channels/ai/episodes').glob('*/plan.json'):
  data=json.loads(p.read_text(encoding='utf-8'))
  if data.get('active_revision_ref'):assert (ROOT/data['active_revision_ref']).is_file()
 print('Shared style, fixed voice, production template, schema and active revisions agree')

if __name__=='__main__':main()
