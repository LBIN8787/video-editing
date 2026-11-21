"""의지력 편 6장 D3 샘플 렌더러 (모션그래픽 + 자막).
python render_ch6.py <출력 mp4> [음성 mp3]
음성이 있으면 문단 사이 쉼(silencedetect)으로 박자 시각을 맞추고 음성을 붙인다.
음성이 없으면 ElevenLabs take 1 길이(117.44초)를 글자 수로 나눠 추정하고 무음으로 렌더한다(시각 검토용).
"""
import re, subprocess, sys, json
from pathlib import Path
from playwright.sync_api import sync_playwright
HERE=Path(__file__).resolve().parent
FPS=30
PARAS=[l.strip() for l in open('/tmp/ch6.txt',encoding='utf-8').read().split('\n\n')] if False else None
def paras():
    t=(HERE/'script_v5.md').read_text(encoding='utf-8'); s=t.index('## 6.'); e=t.index('## 7.')
    return [re.sub(r'^[●○]\s*|^\[마디\]\s*','',l).strip() for l in t[s:e].splitlines() if l.startswith(('●','○','[마디]'))]
def chunks(text,n=28):
    out,cur=[], ''
    for w in text.split():
        if cur and len(cur)+1+len(w)>n: out.append(cur); cur=w
        else: cur=(cur+' '+w).strip()
    return out+[cur] if cur else out
def timing(ps,audio):
    if audio:
        d=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',audio],capture_output=True,text=True).stdout)
        log=subprocess.run(['ffmpeg','-hide_banner','-i',audio,'-af','silencedetect=noise=-35dB:d=0.35','-f','null','-'],capture_output=True,text=True).stderr
        sil=[(float(a),float(b)) for a,b in re.findall(r'silence_start: ([\d.]+)[\s\S]*?silence_end: ([\d.]+)',log)]
        sil=sorted(sorted(sil,key=lambda s:s[1]-s[0],reverse=True)[:len(ps)-1])
        cuts=[(a+b)/2 for a,b in sil]
    else:
        d=117.44; L=[len(p) for p in ps]; tot=sum(L); acc=0; cuts=[]
        for l in L[:-1]: acc+=l; cuts.append(d*acc/tot)
    b=[0.0]+cuts+[d+1.2]
    return [{'t0':b[i],'t1':b[i+1]} for i in range(len(ps))], d
def main():
    out=sys.argv[1]; audio=sys.argv[2] if len(sys.argv)>2 else None
    ps=paras(); P,d=timing(ps,audio); total=P[-1]['t1']
    subs=[]
    for p,pt in zip(ps,P):
        cs=chunks(p); L=sum(len(c) for c in cs); acc=0; span=(pt['t1']-pt['t0'])*0.92
        for c in cs: subs.append((pt['t0']+span*acc/L,c)); acc+=len(c)
    (HERE.parent/'05_edit').mkdir(exist_ok=True)
    (HERE.parent/'05_edit'/'ch6_timing.json').write_text(json.dumps({'audio':bool(audio),'P':P,'duration':d},ensure_ascii=False,indent=1))
    n=int(total*FPS)
    cmd=['ffmpeg','-y','-hide_banner','-loglevel','error','-f','image2pipe','-framerate',str(FPS),'-i','-']
    if audio: cmd+=['-i',audio,'-c:a','aac','-b:a','192k']
    cmd+=['-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-shortest' if audio else '-an',out]
    ff=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    with sync_playwright() as pw:
        br=pw.chromium.launch(); pg=br.new_page(viewport={'width':1920,'height':1080})
        pg.goto((HERE/'ch6_overlay.html').as_uri()); pg.evaluate('document.fonts.ready')
        for f in range(n):
            t=f/FPS; s=''
            for st,c in subs:
                if st<=t: s=c
            pg.evaluate('([t,P,s])=>R(t,P,s)',[t,P,s])
            ff.stdin.write(pg.screenshot(type='jpeg',quality=92))
            if f%300==0: print(f,'/',n,flush=True)
        br.close()
    ff.stdin.close(); ff.wait(); print('done',out,total)
main()
