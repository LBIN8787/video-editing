import unittest
from pathlib import Path
from compositor import Compositor
class Tests(unittest.TestCase):
 def layer(self,**kw):return {'id':'a','role':'demo','in':0,'out':1,**kw}
 def doc(self,l):return {'duration':1,'layers':[l]}
 def test_media_image(self):
  p=Path(__file__).parent/'output/request-ui.png';c=Compositor(self.doc(self.layer(asset='a')),{'a':{'path':str(p),'available':True,'rights':'verified'}});self.assertEqual(c.frame(.5).size,(1280,720))
 def test_denied_asset(self):
  c=Compositor(self.doc(self.layer(asset='a')),{'a':{'available':False}})
  with self.assertRaises(ValueError):c.frame(.5)
 def test_text_overflow(self):
  c=Compositor(self.doc(self.layer(text='abcdef'*40,width=.05)),{})
  with self.assertRaises(ValueError):c.frame(.5)
 def test_video_decode(self):
  p=Path(__file__).parent.parent/'test-output/ai-assistant-motion-test.mp4';c=Compositor(self.doc(self.layer(asset='a')),{'a':{'path':str(p),'available':True,'rights':'verified','type':'video'}});self.assertEqual(c.frame(.5).size,(1280,720))
if __name__=='__main__':unittest.main()
