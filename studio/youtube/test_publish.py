import datetime as dt,sqlite3,unittest
from publish import body_for,reserve
class PublishingTests(unittest.TestCase):
 def test_scheduled_upload_is_explicitly_private(self):
  d={'title':'AI 활용법','description':'설명','publish_at':'2099-01-01T09:00:00+09:00'}
  b=body_for(d);self.assertEqual(b['status']['privacyStatus'],'private');self.assertEqual(b['status']['publishAt'],'2099-01-01T00:00:00Z')
 def test_past_and_naive_schedule_are_rejected(self):
  for stamp in ['2020-01-01T09:00:00+09:00','2099-01-01T09:00:00']:
   with self.assertRaises(ValueError):body_for({'title':'AI','description':'d','publish_at':stamp})
 def test_ambiguous_upload_cannot_be_repeated(self):
  c=sqlite3.connect(':memory:');reserve(c,'job-a','hash-a')
  c.execute("UPDATE uploads SET state='uncertain'");c.commit()
  with self.assertRaises(sqlite3.IntegrityError):reserve(c,'job-a','hash-a')
  with self.assertRaises(sqlite3.IntegrityError):reserve(c,'job-b','hash-a')

class UploadIntegrationTests(unittest.TestCase):
 def setUp(self):
  import tempfile,json,hashlib
  from pathlib import Path
  from unittest.mock import patch,MagicMock
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
  root=Path(self.tmp.name);p=root/'channels/ai/channel.json';p.parent.mkdir(parents=True);p.write_text(json.dumps({'account_created':True,'uploads_enabled':True,'youtube_channel_id':'UC-test'}))
  for target,value in [('publish.ROOT',root),('publish.validate_manifest',lambda d:True),('publish.inspect_video',lambda p:'hash-a')]:
   ctx=patch(target,value);ctx.start();self.addCleanup(ctx.stop)
  self.queue=sqlite3.connect(':memory:');self.queue.execute('CREATE TABLE jobs(id TEXT,channel TEXT,state TEXT,manifest TEXT,approval TEXT,due TEXT,video_id TEXT)')
  manifest=json.dumps({'file':'fixture.mp4','sha256':'hash-a','title':'AI','description':'usage','content_mode':'applied_work'})
  self.queue.execute('INSERT INTO jobs VALUES(?,?,?,?,?,?,NULL)',('job-a','ai','approved',manifest,hashlib.sha256(manifest.encode()).hexdigest(),'2099-01-01T09:00:00+09:00'));self.queue.commit()
  self.ledger=sqlite3.connect(':memory:');self.api=MagicMock()
  self.api.channels.return_value.list.return_value.execute.return_value={'items':[{'id':'UC-test','snippet':{'title':'AI 실전노트'}}]}
  self.api.videos.return_value.insert.return_value.next_chunk.return_value=(None,{'id':'video-real-response'})
  self.api.videos.return_value.list.return_value.execute.return_value={'items':[{'id':'video-real-response','snippet':{'channelId':'UC-test'},'status':{'privacyStatus':'private','publishAt':'2099-01-01T00:00:00Z'}}]}
 def test_success_records_remote_id_and_prevents_second_insert(self):
  from publish import publish
  result=publish(self.api,self.queue,self.ledger,'job-a','UC-test',lambda f:object())
  self.assertEqual(result['video_id'],'video-real-response')
  self.assertEqual(self.queue.execute('SELECT state FROM jobs').fetchone()[0],'uploaded')
  with self.assertRaises(ValueError):publish(self.api,self.queue,self.ledger,'job-a','UC-test',lambda f:object())
  self.assertEqual(self.api.videos.return_value.insert.call_count,1)
 def test_timeout_is_uncertain_and_does_not_retry_insert(self):
  from publish import publish
  self.api.videos.return_value.insert.return_value.next_chunk.side_effect=TimeoutError()
  with self.assertRaises(RuntimeError):publish(self.api,self.queue,self.ledger,'job-a','UC-test',lambda f:object())
  self.assertEqual(self.ledger.execute('SELECT state FROM uploads').fetchone()[0],'uncertain')
  with self.assertRaises(sqlite3.IntegrityError):publish(self.api,self.queue,self.ledger,'job-a','UC-test',lambda f:object())
  self.assertEqual(self.api.videos.return_value.insert.call_count,1)
 def test_old_explainer_cannot_be_published_as_actual_use(self):
  import json,hashlib
  from publish import publish
  row=self.queue.execute('SELECT manifest FROM jobs').fetchone();d=json.loads(row[0]);d.pop('content_mode');m=json.dumps(d)
  self.queue.execute('UPDATE jobs SET manifest=?,approval=?',(m,hashlib.sha256(m.encode()).hexdigest()));self.queue.commit()
  with self.assertRaises(ValueError):publish(self.api,self.queue,self.ledger,'job-a','UC-test',lambda f:object())
  self.api.videos.return_value.insert.assert_not_called()
 def test_wrong_connected_channel_cannot_upload(self):
  from publish import publish
  self.api.channels.return_value.list.return_value.execute.return_value={'items':[{'id':'UC-wrong','snippet':{'title':'Other'}}]}
  with self.assertRaises(ValueError):publish(self.api,self.queue,self.ledger,'job-a','UC-test',lambda f:object())
  self.api.videos.return_value.insert.assert_not_called()

if __name__=='__main__':unittest.main()
