import hashlib,json,tempfile,unittest
from pathlib import Path
from work_cases import create_case,validate_case
class WorkCaseTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
  folder=create_case('real-task',self.root);self.path=folder/'case.json'
  self.evidence=folder/'result.txt';self.evidence.write_text('actual check output')
  self.good={'id':'real-task','domain':'video-channel','status':'partially_tested','objective':'Build a useful work tool','results':['Tool created and checks run'],'limitations':['Live service is not connected'],'public_scope':'Own source and checks','evidence':[{'path':'work-cases/real-task/result.txt','sha256':hashlib.sha256(self.evidence.read_bytes()).hexdigest()}],'metrics':[]}
 def save(self):self.path.write_text(json.dumps(self.good))
 def test_recording_a_task_is_not_proof_of_execution(self):
  with self.assertRaises(ValueError):validate_case('work-cases/real-task/case.json',self.root)
 def test_partial_result_is_usable_only_with_stated_limits(self):
  self.save();self.assertEqual(validate_case('work-cases/real-task/case.json',self.root)['status'],'partially_tested')
  self.good['limitations']=[];self.save()
  with self.assertRaises(ValueError):validate_case('work-cases/real-task/case.json',self.root)
 def test_changed_evidence_invalidates_the_case(self):
  self.save();self.evidence.write_text('changed')
  with self.assertRaises(ValueError):validate_case('work-cases/real-task/case.json',self.root)
 def test_unmeasured_savings_are_not_a_valid_result(self):
  self.good['metrics']=[{'name':'minutes_saved','value':30,'measured':False,'evidence_ref':'work-cases/real-task/result.txt'}];self.save()
  with self.assertRaises(ValueError):validate_case('work-cases/real-task/case.json',self.root)
if __name__=='__main__':unittest.main()
