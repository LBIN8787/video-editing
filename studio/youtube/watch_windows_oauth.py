"""Wait for this project's downloaded Desktop JSON, then run local owner OAuth."""
import argparse,datetime as dt,json,os,shutil,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def desktop_client(path,project_id):
 try:
  data=json.loads(path.read_text(encoding='utf-8-sig')).get('installed',{})
  return bool(data.get('project_id')==project_id and data.get('client_id') and data.get('client_secret') and data.get('token_uri')=='https://oauth2.googleapis.com/token' and data.get('auth_uri') in ['https://accounts.google.com/o/oauth2/auth','https://accounts.google.com/o/oauth2/v2/auth'])
 except (ValueError,OSError):return False

def main():
 p=argparse.ArgumentParser();p.add_argument('--project-id',required=True);p.add_argument('--downloads',type=Path,default=Path.home()/'Downloads');p.add_argument('--timeout',type=int,default=1200);a=p.parse_args()
 profile=ROOT/'channels/ai/channel.json';expected=json.loads(profile.read_text(encoding='utf-8-sig'))['youtube_channel_id']
 local=ROOT/'studio/youtube/.local';local.mkdir(parents=True,exist_ok=True)
 status=local/'connection-status.json';lock=local/'connection-setup.lock'
 try:fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
 except FileExistsError:raise SystemExit('A setup process may already be running; inspect before starting another')
 with os.fdopen(fd,'w') as f:f.write(str(os.getpid()))
 def mark(stage,**extra):
  status.write_text(json.dumps({'stage':stage,'project_id':a.project_id,'expected_channel_id':expected,'updated_at':dt.datetime.now(dt.timezone.utc).isoformat(),**extra},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 try:
  mark('waiting_for_desktop_json');print('WAITING_FOR_GOOGLE_DESKTOP_JSON',flush=True)
  deadline=time.monotonic()+a.timeout;selected=None
  while time.monotonic()<deadline:
   files=sorted(a.downloads.glob('client_secret*.json'),key=lambda p:p.stat().st_mtime,reverse=True)
   selected=next((f for f in files if desktop_client(f,a.project_id)),None)
   if selected:break
   time.sleep(3)
  if not selected:mark('waiting_timed_out');print('NO_MATCHING_JSON_YET',flush=True);return
  private=local/'client_secret.json';shutil.copy2(selected,private)
  mark('waiting_for_google_consent');print('DESKTOP_JSON_RECEIVED_OPENING_GOOGLE_CONSENT',flush=True)
  env=dict(os.environ,PYTHONUTF8='1')
  with (local/'auth-run.log').open('w',encoding='utf-8') as log:
   result=subprocess.run([sys.executable,str(ROOT/'studio/youtube/auth.py'),'--client',str(private),'--token',str(local/'youtube-token.json'),'--channel-id',expected,'--activate-publishing'],stdout=log,stderr=subprocess.STDOUT,env=env)
  if result.returncode:mark('oauth_failed',exit_code=result.returncode);print('GOOGLE_AUTH_NOT_COMPLETED',flush=True);return
  actual=json.loads(profile.read_text(encoding='utf-8-sig'))
  if actual.get('youtube_channel_id')!=expected or not actual.get('oauth_verified') or not (local/'youtube-token.json').is_file():raise RuntimeError('Missing verified connection result')
  mark('connected',channel_id=expected);print('SUCCESS_CHANNEL_CONNECTED',flush=True)
 finally:lock.unlink(missing_ok=True)
if __name__=='__main__':main()
