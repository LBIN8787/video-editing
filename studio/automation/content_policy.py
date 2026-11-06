"""Editorial and fixed-voice gates. Metadata checks do not prove spoken claims."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def validate_manifest(d,settings=None):
 if settings is None:settings=json.loads((ROOT/'settings.json').read_text())
 channel=d.get('channel');policy=settings.get('channels',{}).get(channel,{})
 if not policy and settings.get('channel_profiles'):
  if channel not in ['ai','quiz']:raise ValueError('Unknown channel')
  profile=ROOT/settings['channel_profiles']/channel/'channel.json'
  policy=json.loads(profile.read_text())
 expected=policy.get('voice',{});actual=d.get('voice',{})
 for key in ['provider','voice_id','model_id']:
  if not expected.get(key) or actual.get(key)!=expected[key]:
   raise ValueError(f'Fixed voice mismatch: {channel}.{key}')
 if actual.get('fallback_used',True):raise ValueError('Voice fallback is forbidden')
 if d.get('composition') and d['composition'] not in policy.get('allowed_compositions',[]):
  raise ValueError('Composition has not been checked for this fixed voice')
 asset=Path(actual.get('asset',''))
 if not asset.is_absolute():asset=ROOT/asset
 if not asset.is_file() or not actual.get('sha256') or hashlib.sha256(asset.read_bytes()).hexdigest()!=actual['sha256']:
  raise ValueError('Missing or changed narration asset')
 if d.get('transition_sfx',True):raise ValueError('Transition sounds must be disabled')
 if channel=='ai':
  if d.get('format_version')!='ai-guide-v1':raise ValueError('Needs AI guide format')
  sections=d.get('sections',{})
  for key in ['news_context','features','usage_steps','application_example','result_check','conditions']:
   value=sections.get(key)
   if not value or (isinstance(value,str) and not value.strip()):raise ValueError('Missing guide section: '+key)
  if not isinstance(sections['usage_steps'],list) or len(sections['usage_steps'])<2:raise ValueError('Needs actionable usage steps')
  example=sections['application_example']
  if not isinstance(example,dict) or not all(example.get(k) for k in ['input','request','expected_output','evidence_type']):raise ValueError('Incomplete application example')
  if example['evidence_type'] not in ['illustrative','executed']:raise ValueError('Unknown example evidence type')
  if example['evidence_type']=='illustrative' and not example.get('on_screen_label'):raise ValueError('Illustrative examples need an on-screen label')
  if example['evidence_type']=='executed' and not example.get('evidence_files'):raise ValueError('Executed examples need evidence files')
  if not d.get('source_checked_at') or not d.get('source_urls'):raise ValueError('Missing source date or links')
 return True
