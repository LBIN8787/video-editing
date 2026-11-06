"""Launch one local Codex production run; not an installed scheduler."""
import datetime as dt,json,os,shutil,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
 config=json.loads((ROOT/'studio/automation/settings.json').read_text())
 if not config.get('agent_preproduction_enabled'):raise SystemExit('AI preproduction is disabled')
 exe=shutil.which('codex')
 if not exe:raise SystemExit('Install and sign in to Codex on this persistent worker first')
 state=ROOT/'studio/operations/.local';state.mkdir(parents=True,exist_ok=True)
 lock=state/'production.lock'
 try:fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
 except FileExistsError:raise SystemExit('A prior run may still be active; inspect before removing production.lock')
 with os.fdopen(fd,'w') as f:f.write(str(os.getpid()))
 stamp=dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ');report=state/(stamp+'-report.md')
 try:
  with (state/(stamp+'-run.log')).open('w') as log:
   cmd=[exe,'exec','--full-auto','-C',str(ROOT),'--output-last-message',str(report),'-']
   result=subprocess.run(cmd,input=(ROOT/'studio/operations/daily-prompt.md').read_text(),text=True,stdout=log,stderr=subprocess.STDOUT)
  if result.returncode:raise SystemExit('Production run failed; inspect the local log')
  print('Agent run ended. Inspect the report for actual artifacts and blockers: '+str(report))
 finally:lock.unlink(missing_ok=True)
if __name__=='__main__':main()
