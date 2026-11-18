"""Experimental full-video compositor contract. Pure state evaluator, no file I/O.
No copied source artwork; media IDs resolve only through caller-supplied registry.
Seconds throughout; normalized coordinates; additive roles independent of skin.
"""
import math
PROPS={'x','y','scale','rotation','opacity','crop','highlight'}
ROLES={'footage','evidence','demo','illustration','character','diagram','caption','annotation'}
EASE={'linear':lambda x:x,'smooth':lambda x:x*x*(3-2*x),'out_cubic':lambda x:1-(1-x)**3}

def finite(v): return isinstance(v,(int,float)) and math.isfinite(v)
def validate(doc):
    if not finite(doc.get('duration')) or doc['duration']<=0: raise ValueError('duration')
    ids=set()
    for layer in doc['layers']:
        if layer['id'] in ids: raise ValueError('duplicate layer')
        ids.add(layer['id'])
        if layer['role'] not in ROLES: raise ValueError('role')
        if not 0<=layer['in']<layer['out']<=doc['duration']: raise ValueError('layer interval')
        for prop,keys in layer.get('tracks',{}).items():
            if prop not in PROPS or not keys: raise ValueError('track')
            previous=-1
            for k in keys:
                if not finite(k['t']) or not 0<=k['t']<=layer['out']-layer['in'] or k['t']<=previous: raise ValueError('key time')
                if not finite(k['v']) or k.get('ease','smooth') not in EASE: raise ValueError('key value/ease')
                if prop in {'opacity','crop','highlight'} and not 0<=k['v']<=1: raise ValueError('normalized track')
                previous=k['t']
    for cue in doc.get('audio',[]):
        if not 0<=cue['in']<cue['out']<=doc['duration']: raise ValueError('audio interval')
        if cue.get('status') not in {'verified','pending'}: raise ValueError('audio provenance')
    return True

def interpolate(keys,t):
    if t<=keys[0]['t']: return keys[0]['v']
    for a,b in zip(keys,keys[1:]):
        if t<b['t']:
            u=EASE[b.get('ease','smooth')]((t-a['t'])/(b['t']-a['t']))
            return a['v']+(b['v']-a['v'])*u
    return keys[-1]['v']

def state(doc,t,skin=None):
    validate(doc)
    if not finite(t): raise ValueError('time')
    layers=[]
    for l in sorted(doc['layers'],key=lambda a:a.get('z',0)):
        if l['in']<=t<l['out']:
            props={k:interpolate(v,t-l['in']) for k,v in l.get('tracks',{}).items()}
            layers.append({'id':l['id'],'role':l['role'],'asset':l.get('asset'),'media_time':l.get('source_in',0)+(t-l['in'])*l.get('rate',1),'props':props,'text':l.get('text')})
    return {'layers':layers,'audio':[c for c in doc.get('audio',[]) if c['in']<=t<c['out'] and c['status']=='verified'],'skin':dict(skin or {})}

def readiness(doc,assets):
    """Fail closed: timeline duration is not evidence of full reproduction."""
    validate(doc); issues=[]
    for l in doc['layers']:
        a=assets.get(l.get('asset'),{})
        if l.get('asset') and (not a.get('available') or a.get('rights')!='verified'): issues.append('asset:'+l['id'])
        if not l.get('reference_verified'): issues.append('reference:'+l['id'])
    for a in doc.get('audio',[]):
        if a['status']!='verified': issues.append('audio:'+a['id'])
    if not doc.get('full_motion_review'): issues.append('full_motion_review')
    if not doc.get('full_audio_review'): issues.append('full_audio_review')
    return {'ready':not issues,'issues':issues}
