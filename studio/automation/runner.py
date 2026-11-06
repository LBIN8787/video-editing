#!/usr/bin/env python3
import datetime as dt,json,logging,sys
from pathlib import Path
from workflow import ROOT,KST,connect,plan,build,export,discover
logging.basicConfig(filename=ROOT/'runner.log',level=logging.INFO,format='%(asctime)s %(levelname)s %(message)s')
settings=json.loads((ROOT/'settings.json').read_text())
if not settings['automation_enabled']:
 (ROOT/'health.json').write_text(json.dumps({**settings,'status':'paused_pending_sample_feedback'},ensure_ascii=False,indent=2))
 print('Paused: sample review phase; no planning, research, rendering, or publication scheduled')
 sys.exit(0)
c=connect();today=dt.datetime.now(KST).date().isoformat();plan(c,today)
marker=ROOT/('discovery-'+today+'.done')
if not marker.exists():
 try:discover();marker.write_text(today)
 except Exception:logging.exception('Research failed; no source claims or publication generated')
for row in list(c.execute("SELECT id FROM jobs WHERE state='ready' ORDER BY due")):
 try:build(c,row['id'])
 except Exception:logging.exception('Build failed for %s',row['id'])
try:export(c)
except Exception:logging.exception('Export failed')
counts=dict(c.execute('SELECT state,count(*) FROM jobs WHERE due LIKE ? GROUP BY state',(today+'%',)).fetchall())
(ROOT/'health.json').write_text(json.dumps({'checked_at':dt.datetime.now(KST).isoformat(),'daily_target_total':6,'daily_target_per_channel':3,'today':counts,'youtube_uploader':'not_connected','scheduler':'installation_required'},indent=2))
logging.info('Daily queue: %s',counts)
