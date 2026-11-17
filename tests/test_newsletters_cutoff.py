import importlib.util, sys, types, unittest, tempfile
from pathlib import Path
from unittest.mock import patch
for name in ('ytflow','ytflow.stages'):
    m=types.ModuleType(name);m.__path__=[];sys.modules[name]=m
c=types.ModuleType('ytflow.config');c.ROOT=Path('.');sys.modules['ytflow.config']=c
spec=importlib.util.spec_from_file_location('ytflow.stages.newsletters',Path(__file__).resolve().parents[1] / 'ytflow' / 'stages' / 'newsletters.py')
n=importlib.util.module_from_spec(spec);spec.loader.exec_module(n)
class Schedule(unittest.TestCase):
 def test_boundaries(self):
  for t,want in [('05:59:59','20261118'),('06:00:00','20261118'),('07:00:00','20261118'),('07:59:59','20261118'),('08:00:00','20261119'),('10:00:00','20261119')]:
   with self.subTest(t=t): self.assertEqual(n.video_day('2026-11-18T'+t+'+09:00'),want)
 def test_utc(self): self.assertEqual(n.video_day('2026-11-17T22:59:59Z'),'20261118')
 def test_labels(self): self.assertIn('08:00',n.to_md({'day':'20261118','messages':[],'items':[]}))
 def test_ingest_day_and_idempotency(self):
  it={'title':'Example story','url':'https://example.test/story','date':'2026-11-18T07:30:00+09:00','source':'test','source_name':'Test','brand':'market','kind':'news','reuse':'test','msg':'m1'}
  msg={'id':'m1','date':it['date']}
  with tempfile.TemporaryDirectory() as d, patch.object(n,'OUT',Path(d)),patch.object(n.urllib.request,'urlopen',side_effect=AssertionError('Network forbidden')):
   n.add([it],[msg]);n.add([it],[msg]);data=n._load('20261118')
   self.assertEqual(len(data['items']),1);self.assertEqual(len(data['messages']),1)
   self.assertIn('Example story',n.section(('market',),'2026-11-18'))
 def test_old_bucket_not_silently_migrated(self):
  it={'title':'Example story','url':'https://example.test/story','date':'2026-11-18T07:30:00+09:00','source':'test','source_name':'Test','brand':'market','kind':'news','reuse':'test','msg':'m1'}
  with tempfile.TemporaryDirectory() as d,patch.object(n,'OUT',Path(d)):
   n._save({'day':'20261119','messages':[],'items':[it]});n.add([it],[])
   self.assertEqual(n._load('20261118')['items'],[])
   self.assertEqual(len(n._load('20261119')['items']),1)
if __name__=='__main__':unittest.main()
