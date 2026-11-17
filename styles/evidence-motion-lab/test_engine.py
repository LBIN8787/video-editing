import unittest
import xml.etree.ElementTree as ET
from engine import state,frame,progress,MODES
class TestMotion(unittest.TestCase):
 def test_all_modes_valid_svg(self):
  for mode in MODES:
   for t in (0,.1,.45,1,2,4): ET.fromstring(frame({'mode':mode,'labels':['기술 시험']},t))
 def test_easing_monotonic(self):
  p=[progress(i/100,0,1) for i in range(101)]
  self.assertEqual(p,sorted(p));self.assertEqual((p[0],p[-1]),(0,1))
 def test_dimming(self):
  s={'mode':'evidence_shift','labels':['A','B'],'cues':[0,1]}
  self.assertEqual(state(s,.9)['items'][0]['opacity'],1)
  self.assertAlmostEqual(state(s,2)['items'][0]['opacity'],.28)
 def test_stagger(self):
  s=state({'mode':'process_cascade','labels':['A','B','C']},.5)
  self.assertEqual(s['items'][1]['opacity'],0)
 def test_skin_does_not_change_motion(self):
  s={'mode':'orbit_accumulate','labels':['A','B']}
  self.assertEqual(state(s,1)['items'],state(s,1,{'skin':{'accent':'#123456'}})['items'])
 def test_deterministic(self):
  s={'mode':'comparison','labels':['A','B']}
  self.assertEqual(frame(s,.3),frame(s,.3))
 def test_safe_text(self):
  text=frame({'mode':'source_focus','labels':['<script>bad</script>']},1)
  self.assertNotIn('<script>',text);ET.fromstring(text)
 def test_layout(self):
  for mode in MODES:
   count=1 if mode=='source_focus' else 2
   for a in state({'mode':mode,'labels':['A']*count},1)['items']:
    self.assertGreaterEqual(a['x'],0);self.assertLessEqual(a['x']+a['w'],1920)
    self.assertLess(a['y']+a['h'],925)
 def test_invalid(self):
  for s in ({'mode':'bad','labels':['A']},{'mode':'source_focus','labels':['A','B']},{'mode':'comparison','labels':['A','B'],'cues':[1,0]}):
   with self.assertRaises(ValueError):frame(s,1)
if __name__=='__main__':unittest.main()
