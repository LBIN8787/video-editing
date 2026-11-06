import copy,hashlib,importlib.util,json,shutil,tempfile,unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('render_short',Path(__file__).with_name('render_short.py'));renderer=importlib.util.module_from_spec(spec);spec.loader.exec_module(renderer)
class StyleLockTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
  style=self.root/'styles/shorts-ai-guide';style.mkdir(parents=True);shutil.copy2(renderer.STYLE/'style-lock.json',style/'style-lock.json')
  public=self.root/'studio/renderer/public';(public/'fonts').mkdir(parents=True);(public/'voice.mp3').write_bytes(b'fixture-audio');f=public/'fonts/fixture.otf';f.write_bytes(b'fixture-font')
  (style/'fonts.json').write_text(json.dumps({'assets':[{'path':'fonts/fixture.otf','sha256':hashlib.sha256(f.read_bytes()).hexdigest()}]}))
  self.props=json.loads((renderer.RENDERER/'src/template/reference-props.json').read_text());self.props['audio']='voice.mp3'
 def test_same_template_accepts_content_changes(self):
  self.props['episode']='005';self.props['scenes'][0]['titleLines']=['다른 실제 작업','같은 편집 스타일']
  self.assertEqual(renderer.validate_props(self.props,self.root),1500)
 def test_design_cannot_be_overridden_as_content(self):
  self.props['colors']={'accent':'red'}
  with self.assertRaises(ValueError):renderer.validate_props(self.props,self.root)
 def test_wrong_version_and_oversized_text_are_rejected(self):
  self.props['style_version']='2.0.0'
  with self.assertRaises(ValueError):renderer.validate_props(self.props,self.root)
  self.props['style_version']='1.0.0';self.props['scenes'][0]['titleLines']=['너무 긴 제목입니다'*8]
  with self.assertRaises(ValueError):renderer.validate_props(self.props,self.root)
 def test_font_substitution_is_rejected(self):
  (self.root/'studio/renderer/public/fonts/fixture.otf').write_bytes(b'other font')
  with self.assertRaises(ValueError):renderer.validate_props(self.props,self.root)
if __name__=='__main__':unittest.main()
