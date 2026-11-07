"""Validate content data for the approved visual template, with no style overrides."""
import math

KINDS={'flow','files','prompt','commands','browser','table','slides','image','check'}
FIELDS={'heading','note','folder','files','nodes','lines','query','results','columns','rows','highlightRows','formula','chart','slideTitle','slideBody','editable','image','checks'}

def text(value,limit=100):
 if not isinstance(value,str) or not value.strip() or len(value)>limit:raise ValueError('Missing or oversized visual text')

def labels(values,maximum=3,limit=52):
 if not isinstance(values,list) or not 1<=len(values)<=maximum:raise ValueError('Wrong number of visual items')
 for value in values:text(value,limit)

def validate_visual_scene(scene):
 kind=scene.get('visual');data=scene.get('visual_data')
 if kind not in KINDS or not isinstance(data,dict) or set(data)-FIELDS:raise ValueError('Unknown visual block or style override')
 text(scene.get('action'),60)
 for key in ['heading','note','folder','query','formula','slideTitle','image']:
  if key in data:text(data[key],100 if key=='image' else 65)
 if kind in ['flow','files']:
  key='nodes' if kind=='flow' else 'files';rows=data.get(key)
  if not isinstance(rows,list) or not 1<=len(rows)<=3:raise ValueError('Use one to three visual nodes')
  for row in rows:
   name='label' if kind=='flow' else 'name'
   if not isinstance(row,dict) or set(row)!={name,'kind'} or row['kind'] not in ['file','folder','audio','video']:raise ValueError('Invalid node')
   text(row[name],32)
  if kind=='files':text(data.get('folder'),32)
 elif kind in ['prompt','commands']:labels(data.get('lines'),3,65 if kind=='commands' else 52)
 elif kind=='browser':
  text(data.get('query'),55);rows=data.get('results')
  if not isinstance(rows,list) or not 1<=len(rows)<=3:raise ValueError('Use up to three result examples')
  for row in rows:
   if not isinstance(row,dict) or set(row)!={'title','detail'}:raise ValueError('Invalid result example')
   text(row['title'],32);text(row['detail'],45)
 elif kind=='table':
  columns=data.get('columns');labels(columns,4,16);rows=data.get('rows')
  if not isinstance(rows,list) or not 1<=len(rows)<=3:raise ValueError('Use one to three readable rows')
  for row in rows:
   if not isinstance(row,list) or len(row)!=len(columns):raise ValueError('Table columns do not match')
   for cell in row:
    if not isinstance(cell,str) or len(cell)>20:raise ValueError('Table cell too long')
  if 'highlightRows' in data and (not isinstance(data['highlightRows'],list) or any(type(i)!=int or not 0<=i<len(rows) for i in data['highlightRows'])):raise ValueError('Invalid row highlight')
  if 'chart' in data:
   chart=data['chart']
   if len(rows)>1 or not isinstance(chart,dict) or set(chart)!={'labels','values'}:raise ValueError('Chart does not fit this table')
   labels(chart['labels'],2,10)
   if len(chart['values'])!=len(chart['labels']) or any(type(v) not in [int,float] or not math.isfinite(v) or v<0 for v in chart['values']) or not max(chart['values']):raise ValueError('Invalid chart data')
 elif kind=='slides':
  text(data.get('slideTitle'),28);labels(data.get('slideBody'),3,30)
  if not isinstance(data.get('editable'),bool):raise ValueError('Choose flat or editable example')
 elif kind=='image':text(data.get('image'),100)
 elif kind=='check':labels(data.get('checks'),3,35)
 return True
