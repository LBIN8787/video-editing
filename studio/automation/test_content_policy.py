import copy,hashlib,json,tempfile,unittest
from pathlib import Path
from content_policy import ROOT,validate_manifest
from workflow import connect,plan,bind,build,approve

class ContentPolicyTests(unittest.TestCase):
 def setUp(self):
  self.good=json.loads((ROOT/'manifests/ai-003-fixed-voice.json').read_text())
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
  asset=Path(self.tmp.name)/'voice.mp3';asset.write_bytes(b'test-narration-fixture')
  self.good['voice']['asset']=str(asset);self.good['voice']['sha256']=hashlib.sha256(asset.read_bytes()).hexdigest()
 def test_current_sample_matches_fixed_voice_and_guide(self):
  self.assertTrue(validate_manifest(self.good))
 def test_switching_voice_or_model_is_rejected(self):
  for key in ['provider','voice_id','model_id']:
   d=copy.deepcopy(self.good);d['voice'][key]='different'
   with self.subTest(key=key),self.assertRaises(ValueError):validate_manifest(d)
 def test_missing_instructions_or_undisclosed_mock_is_rejected(self):
  d=copy.deepcopy(self.good);d['sections']['usage_steps']=[]
  with self.assertRaises(ValueError):validate_manifest(d)
  d=copy.deepcopy(self.good);del d['sections']['application_example']['on_screen_label']
  with self.assertRaises(ValueError):validate_manifest(d)
 def test_changed_audio_and_fallback_are_rejected(self):
  d=copy.deepcopy(self.good);d['voice']['sha256']='changed'
  with self.assertRaises(ValueError):validate_manifest(d)
  d=copy.deepcopy(self.good);d['voice']['fallback_used']=True
  with self.assertRaises(ValueError):validate_manifest(d)
 def test_build_and_approval_recheck_policy_after_binding(self):
  with tempfile.TemporaryDirectory() as t:
   c=connect(Path(t));plan(c,'2026-11-07')
   key=c.execute("SELECT id FROM jobs WHERE channel='ai' LIMIT 1").fetchone()[0]
   manifest=Path(t)/'manifest.json';manifest.write_text(json.dumps(self.good));bind(c,key,manifest)
   bad=copy.deepcopy(self.good);bad['voice']['voice_id']='different'
   c.execute('UPDATE jobs SET manifest=? WHERE id=?',(json.dumps(bad),key));c.commit()
   with self.assertRaises(ValueError):build(c,key)
   c.execute("UPDATE jobs SET state='review' WHERE id=?",(key,));c.commit()
   with self.assertRaises(ValueError):approve(c,key)

if __name__=='__main__':unittest.main()
