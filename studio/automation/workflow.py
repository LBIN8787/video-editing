#!/usr/bin/env python3
"""Local, idempotent Shorts queue. Never publishes to YouTube implicitly."""
import argparse,datetime as dt,hashlib,json,sqlite3,subprocess,urllib.request
from pathlib import Path
from content_policy import validate_manifest
ROOT=Path(__file__).resolve().parent
PROJECT=ROOT.parent/'renderer'
KST=dt.timezone(dt.timedelta(hours=9))
def connect(root=ROOT):
 root.mkdir(parents=True,exist_ok=True)
 c=sqlite3.connect(root/'queue.sqlite3',timeout=30);c.row_factory=sqlite3.Row
 c.execute('CREATE TABLE IF NOT EXISTS jobs(id TEXT PRIMARY KEY, channel TEXT, due TEXT, state TEXT, manifest TEXT, error TEXT, approval TEXT, video_id TEXT UNIQUE)');return c
def plan(c,date):
 day=dt.date.fromisoformat(date)
 # Keep legacy job IDs/channel assignments; add the missing slots per channel.
 channels=['ai','quiz','ai'] if day.toordinal()%2 else ['quiz','ai','quiz']
 channels+=['ai']*(3-channels.count('ai'))+['quiz']*(3-channels.count('quiz'))
 times={'ai':['09:00','14:00','20:00'],'quiz':['09:30','14:30','20:30']}
 counts={'ai':0,'quiz':0}
 for i,channel in enumerate(channels):
  key=f'{date}-{i+1}';hour=times[channel][counts[channel]];counts[channel]+=1
  due=f'{date}T{hour}:00+09:00'
  c.execute('INSERT OR IGNORE INTO jobs(id,channel,due,state) VALUES(?,?,?,?)',(key,channel,due,'needs_script'))
  c.execute("UPDATE jobs SET due=? WHERE id=? AND state NOT IN ('approved','published')",(due,key))
 c.commit()
def inspect_video(path):
 d=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
 v=next(s for s in d['streams'] if s['codec_type']=='video');a=next(s for s in d['streams'] if s['codec_type']=='audio')
 if v['width']!=1080 or v['height']!=1920 or not 10<float(d['format']['duration'])<=60:raise ValueError('Video must be 1080x1920, 10–60 seconds, with audio')
 subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(path),'-f','null','-'],check=True,stdout=subprocess.DEVNULL)
 return hashlib.sha256(path.read_bytes()).hexdigest()
def bind(c,key,manifest):
 d=json.loads(Path(manifest).read_text())
 if not Path(d['file']).is_absolute():d['file']=str((ROOT/d['file']).resolve())
 if not d.get('title') or not d.get('description') or not d.get('source_urls') or not d.get('script_reviewed'):raise ValueError('Needs title, description, sources and reviewed script')
 row=c.execute('SELECT * FROM jobs WHERE id=?',(key,)).fetchone()
 if row is None or row['state']=='published':raise ValueError('Missing job or already published')
 if d.get('channel')!=row['channel']:raise ValueError('Wrong channel')
 if d.get('transition_sfx',True):raise ValueError('Transition sounds must be disabled')
 validate_manifest(d)
 if d.get('composition') and d['composition'] not in ['AIRadar','AIRadar002','AIRadar003','AI001Review','Quiz001','Quiz002']:raise ValueError('Composition is not in the local allowlist')
 c.execute('UPDATE jobs SET manifest=?,state=?,error=NULL,approval=NULL WHERE id=?',(json.dumps(d,ensure_ascii=False),'ready',key));c.commit()
def build(c,key):
 with c:
  if c.execute("UPDATE jobs SET state='building',error=NULL WHERE id=? AND state='ready'",(key,)).rowcount!=1:raise ValueError('Job is not ready or already claimed')
 d=json.loads(c.execute('SELECT manifest FROM jobs WHERE id=?',(key,)).fetchone()[0])
 try:
  validate_manifest(d)
  output=Path(d['file']).resolve()
  if not output.is_file():
   if not d.get('composition'):raise ValueError('No video file or local composition')
   output.parent.mkdir(parents=True,exist_ok=True)
   subprocess.run(['npx','remotion','render','src/index.ts',d['composition'],str(output),'--codec=h264','--browser-executable=/usr/bin/chromium','--concurrency=2'],cwd=PROJECT,check=True)
  digest=inspect_video(output)
  # Reject duplicate videos already prepared/published in the queue.
  for row in c.execute("SELECT id,manifest FROM jobs WHERE id!=? AND state IN ('review','approved','published')",(key,)):
   if json.loads(row['manifest']).get('sha256')==digest:raise ValueError('Duplicate video content')
  d.update(file=str(output),sha256=digest)
  c.execute("UPDATE jobs SET manifest=?,state='review' WHERE id=?",(json.dumps(d,ensure_ascii=False),key));c.commit()
 except Exception as e:
  c.execute("UPDATE jobs SET state='failed',error=? WHERE id=?",(str(e),key));c.commit();raise
def approve(c,key):
 row=c.execute('SELECT * FROM jobs WHERE id=?',(key,)).fetchone()
 if not row or row['state']!='review':raise ValueError('Only QA-passed videos can be approved')
 d=json.loads(row['manifest'])
 validate_manifest(d)
 if inspect_video(Path(d['file']))!=d['sha256']:raise ValueError('File changed since QA')
 approval=hashlib.sha256(row['manifest'].encode()).hexdigest()
 c.execute("UPDATE jobs SET state='approved',approval=? WHERE id=?",(approval,key));c.commit()
def export(c):
 out=ROOT/'upload-bundles';out.mkdir(exist_ok=True)
 for row in c.execute("SELECT * FROM jobs WHERE state='approved'"):
  if hashlib.sha256(row['manifest'].encode()).hexdigest()!=row['approval']:raise ValueError('Approval no longer matches')
  d=json.loads(row['manifest'])
  validate_manifest(d)
  if inspect_video(Path(d['file']))!=d['sha256']:raise ValueError('Approved media changed')
  d.update(job_id=row['id'],publish_at=row['due'],youtube_upload_status='NOT_CONNECTED')
  (out/(row['id']+'.json')).write_text(json.dumps(d,ensure_ascii=False,indent=2))
 return out
def discover():
 out=ROOT/'research'/dt.datetime.now(KST).date().isoformat();out.mkdir(parents=True,exist_ok=True)
 for repo in ['anthropics/skills','hugohe3/ppt-master','mvanhorn/last30days-skill']:
  req=urllib.request.Request('https://api.github.com/repos/'+repo,headers={'User-Agent':'shorts-research'})
  with urllib.request.urlopen(req,timeout=25) as f:d=json.load(f)
  (out/(repo.replace('/','--')+'.json')).write_text(json.dumps({k:d.get(k) for k in ['full_name','stargazers_count','pushed_at','archived','html_url']},indent=2))
 print(out)
def main():
 p=argparse.ArgumentParser();p.add_argument('command',choices=['plan','status','bind','build','approve','export','discover','recover']);p.add_argument('--date',default=dt.datetime.now(KST).date().isoformat());p.add_argument('--id');p.add_argument('--manifest');a=p.parse_args();c=connect()
 if a.command=='plan':plan(c,a.date)
 elif a.command=='status':
  for row in c.execute('SELECT id,channel,due,state,error FROM jobs ORDER BY due'):print(dict(row))
 elif a.command=='bind':bind(c,a.id,a.manifest)
 elif a.command=='build':build(c,a.id)
 elif a.command=='approve':approve(c,a.id)
 elif a.command=='export':print(export(c))
 elif a.command=='discover':discover()
 elif a.command=='recover':
  # Explicit operator recovery only, after checking no old renderer is running.
  c.execute("UPDATE jobs SET state='failed',error='Interrupted build; inspect and re-bind before retry' WHERE id=? AND state='building'",(a.id,));c.commit()
if __name__=='__main__':main()
