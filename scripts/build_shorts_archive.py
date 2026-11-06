#!/usr/bin/env python3
"""Create a clean restore bundle with pinned fonts, narration and reference MP4."""
import argparse,hashlib,json,re,subprocess,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser();p.add_argument('--out',default=str(ROOT/'studio/renderer/out/AI-Shorts-Automation-v1.0.0.zip'));a=p.parse_args()
 subprocess.run(['git','diff','--quiet'],cwd=ROOT,check=True);subprocess.run(['git','diff','--cached','--quiet'],cwd=ROOT,check=True)
 commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
 tracked=subprocess.check_output(['git','ls-files'],cwd=ROOT,text=True).splitlines()
 prefixes=('channels/','content/','work-cases/','studio/','styles/shorts-ai-guide/','styles/longform-ai-column/','styles/shorts-quiz-explain/','skills/content-studio/','.agents/skills/content-studio/','releases/shorts-ai-guide-v1.0.0/')
 roots={'AGENTS.md','README.md','.gitignore','WINDOWS-START.md','CONNECT-YOUTUBE.cmd','schemas/studio-project.schema.json','schemas/work-case.schema.json'}
 files={name:ROOT/name for name in tracked if name in roots or name.startswith(prefixes) or (name.startswith('scripts/') and name.split('/')[-1] in ['content_studio.py','test_content_studio.py','render_short.py','test_render_short.py','build_shorts_archive.py','sync_skills.py'])}
 assets=['studio/renderer/public/fonts/NotoSansCJKkr-Regular.otf','studio/renderer/public/fonts/NotoSansCJKkr-Bold.otf','studio/renderer/public/episode-003/voice.mp3','studio/renderer/out/shorts-guide-v1-reference.mp4','studio/renderer/out/locked-v1-final.png','studio/renderer/out/repeatability-qa.json']
 for name in assets:
  path=ROOT/name
  if not path.is_file():raise ValueError('Missing restore asset: '+name)
  files[name]=path
 secret=re.compile(rb'gh[pousr]_[A-Za-z0-9]{25,}|sk-[A-Za-z0-9_-]{25,}|-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY|[?&](?:Signature|oobCode|X-Amz-Signature)=')
 records=[]
 for name,path in sorted(files.items()):
  if '/.local/' in name or name.endswith(('.sqlite3','.log','.done')):raise ValueError('Runtime state cannot be archived')
  raw=path.read_bytes()
  if b'\0' not in raw and secret.search(raw):raise ValueError('Credential-like content: '+name)
  records.append({'path':name,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)})
 def version(cmd):return subprocess.check_output(cmd,text=True).splitlines()[0]
 manifest={'archive_version':'1.0.0','style_id':'shorts-ai-guide','style_version':'1.0.0','source_commit':commit,'environment':{'node':version(['node','--version']),'chromium':version(['chromium','--version']),'ffmpeg':version(['ffmpeg','-version'])},'reference':'studio/renderer/out/shorts-guide-v1-reference.mp4','fixed_voice':{'provider':'elevenlabs','name':'Han Aim','model':'eleven_v4'},'repeatability_test':json.loads((ROOT/'studio/renderer/out/repeatability-qa.json').read_text()),'scope':'Restore bundle; not proof of connected OAuth, registered scheduler, Windows execution or live YouTube upload.','files':records}
 out=Path(a.out).resolve();out.parent.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED) as z:
  for name,path in sorted(files.items()):z.write(path,name)
  z.writestr('ARCHIVE-MANIFEST.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 with zipfile.ZipFile(out) as z:
  assert z.testzip() is None
  for item in records:assert hashlib.sha256(z.read(item['path'])).hexdigest()==item['sha256']
 out.with_suffix('.manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 out.with_suffix('.sha256').write_text(hashlib.sha256(out.read_bytes()).hexdigest()+'  '+out.name+'\n')
 print(json.dumps({'file':str(out),'bytes':out.stat().st_size,'files':len(records),'source_commit':commit},indent=2))
if __name__=='__main__':main()
