"""Approved 15 s technical test; original procedural graphics, no external assets.
Uses Evidence Motion Lab progress easing, no operating manual changes.
"""
from PIL import Image,ImageDraw,ImageFont
from engine import progress
import math, subprocess, wave, struct
from pathlib import Path
O=Path(__file__).parent/'test-output';O.mkdir(exist_ok=True)
W,H=1280,720;fps=30
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
bold='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
def f(n,b=False):return ImageFont.truetype(bold if b else font,n)
def txt(d,xy,s,n=26,col='#213446',b=False,anchor='mm'):d.text(xy,s,font=f(n,b),fill=col,anchor=anchor)
def smooth(t,a,d=.65):return progress(t,a,d)
def panel(d,box,fill='#ffffff',r=24):
 x,y,x2,y2=box;d.rounded_rectangle((x,y+7,x2,y2+7),radius=r,fill='#dfe7ed');d.rounded_rectangle(box,radius=r,fill=fill)
def node(d,x,y,r=48):
 d.ellipse((x-r,y-r,x+r,y+r),fill='#007e91');d.rounded_rectangle((x-22,y-17,x+22,y+17),radius=7,outline='white',width=3)
 d.ellipse((x-12,y-4,x-6,y+2),fill='white');d.ellipse((x+6,y-4,x+12,y+2),fill='white')
def check(d,x,y,p):
 pts=[(x-13,y),(x-3,y+10),(x+18,y-14)]
 if p<.4:d.line([pts[0],(pts[0][0]+10*p/.4,pts[0][1]+10*p/.4)],fill='#008477',width=5)
 else:d.line(pts[:2]+[(pts[1][0]+21*(p-.4)/.6,pts[1][1]-24*(p-.4)/.6)],fill='#008477',width=5)
def base_frame(t):
 im=Image.new('RGB',(W,H),'#edf2f7');d=ImageDraw.Draw(im)
 # A persistent stage map, not an intro or title card.
 txt(d,(72,62),'AI 비서의 요청 처리 과정',25,b=True,anchor='lm')
 stage=min(2,int(t//5))
 for i,label in enumerate(['요청','할 일','확인']):
  x=955+i*100;d.ellipse((x-8,55,x+8,71),fill='#007e91' if i<=stage else '#cbd5df');txt(d,(x,96),label,18)
 if stage==0:
  p=smooth(t,.2,.85);x=110+35*(1-p)
  panel(d,(x,248,x+365,420));txt(d,(x+36,283),'요청',20,col='#637b8c',anchor='lm');txt(d,(x+36,340),'해야 할 일을 전달합니다',25,b=True,anchor='lm')
  node(d,900,334,76);txt(d,(900,450),'AI 비서',25,b=True)
  d.line((490,334,799,334),fill='#cfdae3',width=4)
  q=smooth(t,1.3,1.4);px=500+295*q
  d.ellipse((px-9,325,px+9,343),fill='#00a9b4')
  if t>2.7:
   z=smooth(t,2.7);d.ellipse((1020,295,1064,339),fill='#d6eee8');check(d,1041,316,z)
  caption='요청을 받으면,'
 elif stage==1:
  u=t-5;node(d,230,333,70)
  for i,label in enumerate(['필요한 정보','실행할 작업','확인할 결과']):
   y=206+i*130;p=smooth(u,.4+i*.5,.65)
   if p>0:
    # Draw connectors first; they stop before cards, never through their text.
    d.line([(305,333),(430,333),(430,y+40),(560,y+40)],fill='#b7cbd6',width=3)
    xx=560+40*(1-p);panel(d,(xx,y,1100+40*(1-p),y+85),r=18)
    d.ellipse((xx+24,y+22,xx+65,y+63),fill='#e0f1f2');txt(d,(xx+45,y+44),str(i+1),20,col='#007e91',b=True)
    txt(d,(xx+95,y+43),label,26,b=True,anchor='lm')
  caption='필요한 일을 찾고,'
 else:
  u=t-10;panel(d,(180,180,1100,514));txt(d,(230,220),'실행 결과',22,col='#637b8c',anchor='lm')
  for i,label in enumerate(['요청과 일치','작업 완료','결과 확인']):
   y=296+i*76;txt(d,(245,y),label,27,b=True,anchor='lm')
   p=smooth(u,.4+i*.65,.75);d.rounded_rectangle((500,y-9,980,y+9),radius=9,fill='#e3ebf0')
   if p>0:d.rounded_rectangle((500,y-9,500+480*p,y+9),radius=9,fill='#66bab9')
   if p==1:check(d,1040,y,smooth(u,1.15+i*.65,.3))
  caption='실행 결과를 확인합니다.'
 # Caption size restrained, consistent baseline, adequate empty space.
 d.rounded_rectangle((270,603,1010,665),radius=15,fill='#213446');txt(d,(640,634),caption,29,col='white')
 return im
def frame(t):
 # 0.4 s dissolve bridges information stages without adding an intro.
 for cut in (5.,10.):
  if cut <= t < cut+.4:
   return Image.blend(base_frame(cut-.001),base_frame(t),smooth(t,cut,.4))
 return base_frame(t)
# Unvoiced quiet procedural interface cues; explicitly not copied source audio.
rate=48000;duration=15
with wave.open(str(O/'cues.wav'),'w') as w:
 w.setnchannels(1);w.setsampwidth(2);w.setframerate(rate)
 out=[]
 for i in range(rate*duration):
  t=i/rate;v=0.
  for at,hz in [(1.3,420),(2.7,520),(5.4,420),(5.9,460),(6.4,500),(11.15,440),(11.8,480),(12.45,520)]:
   a=t-at
   if 0<=a<.14:v+=.045*math.sin(2*math.pi*hz*a)*math.exp(-a*35)*min(1,a/.008)
  out.append(struct.pack('<h',int(32767*v)))
 w.writeframes(b''.join(out))
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r','30','-i','-','-i',str(O/'cues.wav'),'-c:v','libx264','-crf','20','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart','-shortest',str(O/'ai-assistant-motion-test.mp4')],stdin=subprocess.PIPE)
for i in range(fps*duration):p.stdin.write(frame(i/fps).tobytes())
p.stdin.close();assert p.wait()==0
sheet=Image.new('RGB',(1280,1080),'white')
for i,t in enumerate([.7,2.8,5.6,7.5,10.6,13.0]):
 pic=frame(t).resize((640,360));sheet.paste(pic,((i%2)*640,(i//2)*360))
sheet.save(O/'qa-contact-sheet.jpg')
print(O/'ai-assistant-motion-test.mp4')
