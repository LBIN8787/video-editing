import copy,unittest
from compile_edit_package import compile_package,validate_bundle

PACKAGE='channels/ai/episodes/006-whisper/layers/production-package.json'

class LayerBoundaryTests(unittest.TestCase):
 def test_skin_switch_preserves_direction_subtitles_and_narration(self):
  _,a=compile_package(PACKAGE,check_assets=False)
  _,b=compile_package(PACKAGE,'styles/shorts-ai-guide/skins/blueprint.json',check_assets=False)
  for key in ['cut_hash','attention_hash','content_hash','caption_hash','audio','frames']:self.assertEqual(a[key],b[key])
  self.assertNotEqual(a['skin_id'],b['skin_id'])

 def test_skin_cannot_override_timing_or_voice(self):
  d,_=compile_package(PACKAGE,check_assets=False);d['skin']['audio']='another-voice.mp3'
  with self.assertRaises(ValueError):validate_bundle(d)

 def test_emphasis_cannot_escape_its_scene(self):
  d,_=compile_package(PACKAGE,check_assets=False);d['emphasis']['points'][0]['to_frame']=999999
  with self.assertRaises(ValueError):validate_bundle(d)

if __name__=='__main__':unittest.main()
