"""Experimental deterministic SVG frame engine; no I/O, network or video production.
Load using importlib (folder name intentionally excluded from automatic style registry).
"""
import html
import math

MODES = {'evidence_shift', 'orbit_accumulate', 'process_cascade', 'metaphor_reveal', 'source_focus', 'comparison'}
DEFAULT = {
 'motion': {'enter': .45, 'stagger': .55, 'dim': .28, 'ease': 'smooth'},
 'skin': {'background':'#edf1f5','card':'#ffffff','ink':'#152435','accent':'#007e91','radius':24,'font':'sans-serif'},
 'subtitle': {'size':36,'color':'#ffffff','background':'#152435'},
 'sound': {'enabled':False},
}

def progress(t, at, duration, ease='smooth'):
    if not all(math.isfinite(x) for x in (t, at, duration)) or duration <= 0:
        raise ValueError('finite times and positive duration required')
    x = max(0., min(1., (t-at)/duration))
    return x*x*(3-2*x) if ease == 'smooth' else x

def config(overrides=None):
    result = {k:dict(v) for k,v in DEFAULT.items()}
    for key, value in (overrides or {}).items():
        if key not in result: raise ValueError('unknown layer '+key)
        result[key].update(value)
    m=result['motion']
    if m['enter'] <= 0 or m['stagger'] <= 0 or not 0 <= m['dim'] <= 1: raise ValueError('invalid motion')
    if m['ease'] not in ('smooth','linear'): raise ValueError('invalid ease')
    return result

def state(scene, t, overrides=None):
    c=config(overrides); m=c['motion']; mode=scene['mode']
    if mode not in MODES: raise ValueError('unsupported mode')
    labels=scene.get('labels',[])
    if not 1 <= len(labels) <= 4: raise ValueError('1..4 labels per scene; split larger lists')
    if any(len(str(x))>42 for x in labels): raise ValueError('label too long; shorten or split')
    cues=scene.get('cues',[i*m['stagger'] for i in range(len(labels))])
    if len(cues)!=len(labels) or any(not math.isfinite(x) or x<0 for x in cues) or cues != sorted(cues): raise ValueError('invalid cues')
    positions={
      'evidence_shift':[(90,190,820,460),(1010,190,820,460)],
      'orbit_accumulate':[(70,160,610,230),(1240,160,610,230),(70,560,610,230),(1240,560,610,230)],
      'process_cascade':[(980,130+i*170,790,140) for i in range(4)],
      'metaphor_reveal':[(560,240,800,420),(690,700,540,100)],
      'source_focus':[(160,130,1600,650)],
      'comparison':[(90,170,820,550),(1010,170,820,550)],
    }[mode]
    if len(labels)>len(positions): raise ValueError('too many elements for mode')
    items=[]
    for i,(label,at) in enumerate(zip(labels,cues)):
        p=progress(t,at,m['enter'],m['ease']); x,y,w,h=positions[i]
        opacity=p
        if mode=='evidence_shift' and i==0 and len(labels)>1:
            opacity *= 1-(1-m['dim'])*progress(t,cues[1],m['enter'],m['ease'])
        items.append({'text':str(label),'x':x,'y':y+24*(1-p),'w':w,'h':h,'opacity':opacity,'reveal':p})
    return {'mode':mode,'items':items,'progress':progress(t,0,scene.get('duration',4),'linear'),'config':c}

def frame(scene,t,overrides=None):
    """Return a self-contained 1920x1080 SVG; caller owns any authorized output I/O.
    Safe text only: URLs/raw SVG/external media are never interpolated as markup.
    Actual licensed media compositing belongs to a later approved adapter.
    """
    s=state(scene,t,overrides); c=s['config']; sk=c['skin']; e=lambda x:html.escape(str(x),quote=True)
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080"><rect width="1920" height="1080" fill="{e(sk["background"])}"/>']
    if s['mode']=='orbit_accumulate':
        parts.append(f'<circle cx="960" cy="480" r="110" fill="{e(sk["accent"])}"/><path d="M910 480h100M960 430v100" stroke="white" stroke-width="12"/>')
    if s['mode']=='process_cascade':
        parts.append(f'<rect x="100" y="400" width="740" height="38" rx="19" fill="{e(sk["card"])}"/><rect x="100" y="400" width="{740*s["progress"]:.3f}" height="38" rx="19" fill="{e(sk["accent"])}"/>')
    if s['mode']=='metaphor_reveal':
        p=progress(t,0,c['motion']['enter'])
        parts.append(f'<circle cx="960" cy="450" r="240" fill="{e(sk["accent"])}" opacity="{p:.4f}"/>')
    for i,a in enumerate(s['items']):
        x,y,w,h=a['x'],a['y'],a['w'],a['h']
        parts.append(f'<g opacity="{a["opacity"]:.4f}"><rect x="{x}" y="{y:.3f}" width="{w}" height="{h}" rx="{e(sk["radius"])}" fill="{e(sk["card"])}" stroke="{e(sk["ink"])}" stroke-opacity=".08"/>')
        # The bar is an attention underline, not fabricated numeric data.
        parts.append(f'<rect x="{x+35}" y="{y+h-36:.3f}" width="{(w-70)*a["reveal"]:.3f}" height="6" fill="{e(sk["accent"])}"/>')
        text=a['text']; lines=[text[j:j+21] for j in range(0,len(text),21)]
        for j,line in enumerate(lines):
            parts.append(f'<text x="{x+35}" y="{y+55+44*j:.3f}" font-family="{e(sk["font"])}" font-size="32" fill="{e(sk["ink"])}">{e(line)}</text>')
        parts.append('</g>')
    subtitle=scene.get('subtitle','')
    if len(subtitle)>40: raise ValueError('subtitle exceeds one-line safe area')
    if subtitle:
        sub=c['subtitle']
        parts.append(f'<rect x="200" y="925" width="1520" height="90" rx="12" fill="{e(sub["background"])}"/><text x="960" y="984" text-anchor="middle" font-size="{e(sub["size"])}" fill="{e(sub["color"])}">{e(subtitle)}</text>')
    parts.append('</svg>')
    return ''.join(parts)
