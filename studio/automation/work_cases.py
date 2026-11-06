"""Link actual work outputs to reusable, publicly scoped case records."""
import hashlib,json,re
from pathlib import Path
PROJECT=Path(__file__).resolve().parents[2]
DOMAINS=['video-channel','game-development','app-development','agent-setup','other']

def safe_case_id(value):
 if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',value):raise ValueError('Invalid work case ID')
 return value

def create_case(case_id,root=PROJECT,domain='video-channel'):
 safe_case_id(case_id)
 if domain not in DOMAINS:raise ValueError('Unknown work domain')
 folder=root/'work-cases'/case_id
 if folder.exists():raise FileExistsError('Work case exists; continue it instead of overwriting')
 folder.mkdir(parents=True)
 data={'id':case_id,'domain':domain,'status':'planned','objective':'','acceptance_criteria':[],'results':[],'limitations':[],'public_scope':'','evidence':[],'metrics':[]}
 (folder/'case.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 for name,text in {
  'task.md':'# 실제 작업\n\n## 해결할 일과 필요성\n\n## 완료 기준\n\n## 기존 방법과 비교 기준\n\n## 입력 자료 위치 (원문은 비공개)\n',
  'execution.md':'# 적용 기록\n\n## 사용 도구와 실행 환경\n\n## 입력 / 요청 / 수행 단계\n\n## 실제 산출물과 검사\n\n## 실패·수정·남은 일\n',
  'public-case.md':'# 공개용 사례\n\n## 실제 해결하려던 일\n\n## 적용 방법\n\n## 확인한 결과와 증거\n\n## 확인하지 못한 부분\n\n## 다른 사람이 따라 할 방법\n'
 }.items():(folder/name).write_text(text,encoding='utf-8')
 return folder

def validate_case(ref,root=PROJECT):
 root=root.resolve();path=(root/ref).resolve()
 if not path.is_relative_to(root/'work-cases') or not path.is_file():raise ValueError('Missing work case record')
 data=json.loads(path.read_text())
 if data.get('domain') not in DOMAINS:raise ValueError('Missing or unknown work domain')
 if data.get('status') not in ['tested','partially_tested','in_use']:raise ValueError('Work case has no verified execution yet')
 if not data.get('objective') or not data.get('results') or not data.get('public_scope'):raise ValueError('Work case lacks result or public scope')
 if data['status']=='partially_tested' and not data.get('limitations'):raise ValueError('Partial cases must state unfinished work')
 if not data.get('evidence'):raise ValueError('Actual work cases require evidence')
 verified=set()
 for item in data['evidence']:
  asset=(root/item['path']).resolve()
  if not asset.is_relative_to(root) or '.local' in asset.relative_to(root).parts or not asset.is_file():raise ValueError('Invalid public evidence path')
  if hashlib.sha256(asset.read_bytes()).hexdigest()!=item.get('sha256'):raise ValueError('Work evidence changed or is missing')
  verified.add(item['path'])
 for metric in data.get('metrics',[]):
  if metric.get('measured') is not True or metric.get('evidence_ref') not in verified:raise ValueError('Performance claims require measured evidence')
 return data
