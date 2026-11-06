"""Run on the persistent worker's local PC. Never paste tokens into chat."""
import argparse,json,os
from pathlib import Path
SCOPES=['https://www.googleapis.com/auth/youtube.upload','https://www.googleapis.com/auth/youtube.readonly']

def credentials(token_path):
 from google.oauth2.credentials import Credentials
 from google.auth.transport.requests import Request
 p=Path(token_path).expanduser()
 cred=Credentials.from_authorized_user_file(str(p),SCOPES)
 if cred.expired and cred.refresh_token:
  cred.refresh(Request());save_token(p,cred.to_json())
 if not cred.valid:raise ValueError('Reconnect the Google account on the worker PC')
 return cred

def save_token(path,text):
 path=Path(path).expanduser();path.parent.mkdir(parents=True,exist_ok=True)
 fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_TRUNC,0o600)
 with os.fdopen(fd,'w') as f:f.write(text)
 os.chmod(path,0o600)

def channel_identity(api,expected):
 rows=api.channels().list(part='id,snippet',mine=True).execute().get('items',[])
 if len(rows)!=1 or rows[0]['id']!=expected:raise ValueError('Connected channel differs from the explicitly selected channel ID')
 return {'channel_id':rows[0]['id'],'title':rows[0]['snippet']['title']}

def main():
 from google_auth_oauthlib.flow import InstalledAppFlow
 from googleapiclient.discovery import build
 p=argparse.ArgumentParser();p.add_argument('--client',required=True);p.add_argument('--token',required=True);p.add_argument('--channel-id',required=True);p.add_argument('--activate-publishing',action='store_true');a=p.parse_args()
 flow=InstalledAppFlow.from_client_secrets_file(a.client,SCOPES)
 cred=flow.run_local_server(host='localhost',port=0,access_type='offline',prompt='consent',authorization_prompt_message='Open this Google authorization page on this PC: {url}',success_message='Authorization received. You may close this tab.')
 identity=channel_identity(build('youtube','v3',credentials=cred,cache_discovery=False),a.channel_id)
 save_token(Path(a.token),cred.to_json())
 if a.activate_publishing:
  root=Path(__file__).resolve().parents[2]
  profile=root/'channels/ai/channel.json';data=json.loads(profile.read_text());data.update(account_created=True,youtube_channel_id=a.channel_id,uploads_enabled=True,status='ai_pilot',oauth_verified=True);profile.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'connected':identity,'token_saved':True,'publishing_enabled':a.activate_publishing},ensure_ascii=False))
if __name__=='__main__':main()
