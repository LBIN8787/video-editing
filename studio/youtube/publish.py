"""Upload a queue-approved video with a fixed channel and durable duplicate guard."""
import argparse,datetime as dt,hashlib,json,sqlite3,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'studio/automation'))
from content_policy import validate_manifest
from workflow import inspect_video

def body_for(d,now=None):
 now=now or dt.datetime.now(dt.timezone.utc)
 if not d.get('title') or len(d['title'])>100:raise ValueError('Title must be 1–100 characters')
 if not d.get('description') or len(d['description'].encode())>5000:raise ValueError('Description is missing or too long')
 status={'privacyStatus':'private','selfDeclaredMadeForKids':False}
 if d.get('publish_at'):
  stamp=dt.datetime.fromisoformat(d['publish_at'].replace('Z','+00:00'))
  if stamp.tzinfo is None or stamp<=now:raise ValueError('Publish time must be timezone-aware and in the future')
  status['publishAt']=stamp.astimezone(dt.timezone.utc).isoformat().replace('+00:00','Z')
 return {'snippet':{'title':d['title'],'description':d['description'],'categoryId':'28','defaultLanguage':'ko','defaultAudioLanguage':'ko'},'status':status}

def reserve(c,key,digest):
 c.execute('CREATE TABLE IF NOT EXISTS uploads(job_id TEXT PRIMARY KEY,sha256 TEXT UNIQUE,state TEXT,video_id TEXT,error TEXT)')
 with c:c.execute('INSERT INTO uploads(job_id,sha256,state) VALUES(?,?,?)',(key,digest,'uploading'))

def publish(api,queue,ledger,job_id,channel_id,media_factory,now=None):
 from auth import channel_identity
 profile=json.loads((ROOT/'channels/ai/channel.json').read_text())
 if not profile['account_created'] or not profile['uploads_enabled'] or profile.get('youtube_channel_id')!=channel_id:raise ValueError('Channel onboarding is not complete')
 channel_identity(api,channel_id)
 queue.row_factory=sqlite3.Row
 row=queue.execute('SELECT * FROM jobs WHERE id=?',(job_id,)).fetchone()
 if row is None or row['channel']!='ai' or row['state']!='approved':raise ValueError('Needs an approved AI-channel job')
 if hashlib.sha256(row['manifest'].encode()).hexdigest()!=row['approval']:raise ValueError('Approval is stale')
 d=json.loads(row['manifest'])
 if d.get('content_mode') not in profile.get('publish_modes',['applied_work']):raise ValueError('Current channel publishing requires an actual work case')
 validate_manifest(d)
 path=Path(d['file'])
 if inspect_video(path)!=d['sha256']:raise ValueError('Approved video changed')
 d['publish_at']=row['due'];body=body_for(d,now)
 media=media_factory(str(path))
 reserve(ledger,job_id,d['sha256'])
 try:
  request=api.videos().insert(part='snippet,status',body=body,media_body=media,notifySubscribers=False)
  response=None
  while response is None:_,response=request.next_chunk(num_retries=0)
  video_id=response.get('id')
  if not video_id:raise ValueError('Upload returned no video ID')
  with ledger:ledger.execute("UPDATE uploads SET state='uploaded',video_id=? WHERE job_id=?",(video_id,job_id))
  # Save the real remote ID immediately. Do not repeat videos.insert after partial success.
  with queue:queue.execute("UPDATE jobs SET state='uploaded',video_id=? WHERE id=?",(video_id,job_id))
 except Exception as exc:
  with ledger:ledger.execute("UPDATE uploads SET state='uncertain',error=? WHERE job_id=?",(type(exc).__name__,job_id))
  raise RuntimeError('Upload result uncertain; inspect ledger and YouTube Studio before any retry') from exc
 remote=api.videos().list(part='id,snippet,status',id=video_id).execute().get('items',[])
 if len(remote)!=1 or remote[0]['snippet']['channelId']!=channel_id:raise RuntimeError('Upload saved but owner verification failed; do not reupload')
 with ledger:ledger.execute("UPDATE uploads SET state='verified' WHERE job_id=?",(job_id,))
 return {'video_id':video_id,'privacy':remote[0]['status']['privacyStatus'],'publish_at':remote[0]['status'].get('publishAt'),'state':'uploaded_verified'}

def main():
 p=argparse.ArgumentParser();p.add_argument('--job-id',required=True);p.add_argument('--token',required=True);p.add_argument('--channel-id',required=True);p.add_argument('--queue',default=str(ROOT/'studio/automation/queue.sqlite3'));p.add_argument('--ledger',default=str(ROOT/'studio/youtube/.local/uploads.sqlite3'));a=p.parse_args()
 from auth import credentials
 from googleapiclient.discovery import build
 from googleapiclient.http import MediaFileUpload
 api=build('youtube','v3',credentials=credentials(a.token),cache_discovery=False)
 Path(a.ledger).parent.mkdir(parents=True,exist_ok=True)
 result=publish(api,sqlite3.connect(a.queue),sqlite3.connect(a.ledger),a.job_id,a.channel_id,lambda f:MediaFileUpload(f,mimetype='video/mp4',chunksize=8*1024*1024,resumable=True));print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()
