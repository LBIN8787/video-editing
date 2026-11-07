import importlib.util,json,shutil,tempfile,unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('content_studio',Path(__file__).with_name('content_studio.py'));studio=importlib.util.module_from_spec(spec);spec.loader.exec_module(studio)
class StudioTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
  for name in ['channels','styles']:shutil.copytree(studio.ROOT/name,self.root/name)
  studio.create_case('actual-task',self.root)
 def test_short_and_long_reuse_research_without_overwrite(self):
  a=studio.create('ai','new-topic','test-short','shorts-ai-guide',self.root,work_case='actual-task')
  self.assertTrue((a/'production-brief.json').is_file())
  self.assertEqual(json.loads((a/'production-brief.json').read_text())['voice']['status'],'pending')
  article=self.root/'content/topics/new-topic/article.md';article.write_text('Existing verified article')
  b=studio.create('ai','new-topic','test-long','longform-ai-column',self.root,work_case='actual-task')
  x=json.loads((a/'plan.json').read_text());y=json.loads((b/'plan.json').read_text())
  self.assertEqual(x['style_version'],'1.1.1');self.assertEqual(x['renderer_ref'],'studio/renderer/src/template/ShortsGuideTemplate.tsx');self.assertEqual(x['work_case_ref'],y['work_case_ref']);self.assertEqual(x['article_ref'],y['article_ref']);self.assertEqual(x['voice_ref'],y['voice_ref']);self.assertEqual(article.read_text(),'Existing verified article');self.assertFalse(y['publish_allowed'])
 def test_channel_style_and_ids_cannot_escape_scope(self):
  with self.assertRaises(ValueError):studio.create('quiz','test','test','longform-ai-column',self.root,work_case='actual-task')
  with self.assertRaises(ValueError):studio.create('ai','../escape','test','shorts-ai-guide',self.root,work_case='actual-task')
 def test_actual_case_required_for_new_ai_episode(self):
  with self.assertRaises(ValueError):studio.create('ai','test','test','shorts-ai-guide',self.root)
 def test_existing_episode_is_not_overwritten(self):
  studio.create('ai','test','test','shorts-ai-guide',self.root,work_case='actual-task')
  with self.assertRaises(FileExistsError):studio.create('ai','test','test','shorts-ai-guide',self.root,work_case='actual-task')
if __name__=='__main__':unittest.main()
