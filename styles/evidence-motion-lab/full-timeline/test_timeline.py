import unittest
from timeline import *
class Tests(unittest.TestCase):
 def doc(self): return {'duration':10,'layers':[{'id':'a','role':'evidence','in':0,'out':10,'asset':'document','tracks':{'x':[{'t':0,'v':0},{'t':2,'v':1,'ease':'linear'}]}}]}
 def test_interpolation(self): self.assertEqual(state(self.doc(),1)['layers'][0]['props']['x'],.5)
 def test_end_exclusive(self): self.assertEqual(state(self.doc(),10)['layers'],[])
 def test_skin_independence(self): self.assertEqual(state(self.doc(),1,{'color':'red'})['layers'],state(self.doc(),1,{'color':'blue'})['layers'])
 def test_unverified_fails(self): self.assertFalse(readiness(self.doc(),{})['ready'])
 def test_bad_times(self):
  d=self.doc(); d['layers'][0]['out']=11
  with self.assertRaises(ValueError):validate(d)
 def test_duplicate(self):
  d=self.doc();d['layers']*=2
  with self.assertRaises(ValueError):validate(d)
 def test_audio_pending_silent(self):
  d=self.doc();d['audio']=[{'id':'cue','in':0,'out':2,'status':'pending'}];self.assertEqual(state(d,1)['audio'],[])
 def test_media_clock(self):
  d=self.doc();d['layers'][0].update(source_in=20,rate=.5);self.assertEqual(state(d,2)['layers'][0]['media_time'],21)
if __name__=='__main__': unittest.main()
