import copy,json,unittest
from pathlib import Path
from visual_brief import validate_visual_scene
from prepare_visual_short import prepare
from render_short import validate_props

ROOT=Path(__file__).resolve().parents[1]

class VisualWorkflowBoundaryTests(unittest.TestCase):
 def setUp(self):
  self.props=json.loads((ROOT/'channels/ai/episodes/001-last30days/revisions/visual-v2/props.json').read_text())

 def test_content_cannot_smuggle_layout_or_oversized_table(self):
  scene=copy.deepcopy(self.props['scenes'][0]);scene['visual_data']['fontSize']=120
  with self.assertRaises(ValueError):validate_visual_scene(scene)
  scene.update(visual='table',visual_data={'columns':['A','B'],'rows':[['one']]})
  with self.assertRaises(ValueError):validate_visual_scene(scene)

 def test_missing_voice_never_passes_final_render_validation(self):
  with self.assertRaisesRegex(ValueError,'Narration missing'):validate_props(self.props)

 def test_busy_provider_stops_final_preparation(self):
  brief={'channel':'ai','editorial_reviewed':True,'source_urls':['https://example.org'],'source_checked_at':'2026-11-07','content_mode':'historical_illustrative_refresh','core_task':{'input':'a','action':'b','output':'c'},'voice':{'status':'blocked_provider_busy'},'scenes':[{'narration':'내레이션'}]*3}
  with self.assertRaisesRegex(ValueError,'Fixed narration'):prepare(brief,words=[{'text':'내레이션','startMs':0,'endMs':1000}])

if __name__=='__main__':unittest.main()
