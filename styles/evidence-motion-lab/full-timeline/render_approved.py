"""ONLY previously approved 15s script. No new narration or factual assertions."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,math,wave,struct
from compositor import Compositor,FONT,BOLD
O=Path(__file__).parent/'output';O.mkdir(exist_ok=True)
im=Image.new('RGBA',(900,560),'white');d=ImageDraw.Draw(im)
for j,text in enumerate(['해야 할 일을 전달합니다','필요한 정보','실행할 작업','확인할 결과']):
 y=65+j*125;d.rounded_rectangle((30,y-32,870,y+55),radius=15,fill='#edf2f0');d.text((65,y),text,font=ImageFont.truetype(FONT,32),fill='#20342b')
im.save(O/'request-ui.png')
# Independent procedural symbol, not the source mascot.
im=Image.new('RGBA',(320,320),(0,0,0,0));d=ImageDraw.Draw(im);d.rounded_rectangle((40,40,280,280),radius=75,fill='#167c79');d.rounded_rectangle((85,105,235,205),radius=25,outline='white',width=9)
for x in [120,200]:d.ellipse((x-10,145,x+10,165),fill='white')
im.save(O/'assistant.png')
def keys(a,b,d=.5):return [{'t':0,'v':a},{'t':d,'v':b,'ease':'out_cubic'}]
layers=[]
def add(id,role,start,end,**kw):layers.append(dict(id=id,role=role,**{'in':start,'out':end},**kw))
add('ui','demo',0,5,asset='ui',x=.34,y=.45,width=.53,height=.62,tracks={'opacity':keys(0,1),'crop':[{'t':0,'v':0},{'t':2,'v':0},{'t':3.2,'v':1}]},crop_box=[0,.02,.9,.53],viewport='cover')
add('assistant','character',0,10.4,asset='assistant',x=.78,y=.45,width=.2,height=.36,tracks={'x':[{'t':0,'v':.78},{'t':4.7,'v':.78},{'t':5.6,'v':.2}],'scale':keys(.82,1),'opacity':[{'t':0,'v':1},{'t':9.6,'v':1},{'t':10.4,'v':0}]})
for i,label in enumerate(['필요한 정보','실행할 작업','확인할 결과']):
 start=5.25+i*.55;add('task'+str(i),'annotation',start,10,text=label,x=.63,y=.25+i*.19,width=.5,height=.13,tracks={'opacity':keys(0,1),'x':keys(.7,.63),'highlight':keys(0,1,.8)})
add('results','diagram',10.15,15,x=.5,y=.45,width=.7,height=.6,fill='#ffffff',tracks={'opacity':keys(0,1)})
for i,label in enumerate(['요청과 일치','작업 완료','결과 확인']):
 add('result'+str(i),'annotation',10.3+i*.6,15,text=label,x=.5,y=.27+i*.18,width=.6,height=.12,fill='#eff5f0',tracks={'opacity':keys(0,1),'highlight':keys(0,1,.75)})
for i,text in enumerate(['요청을 받으면,','필요한 일을 찾고,','실행 결과를 확인합니다.']):
 add('caption'+str(i),'caption',i*5,(i+1)*5,text=text,x=.5,y=.88,width=.68,height=.09,fill='#20302c',color='white',font_size=28,z=100)
doc={'duration':15,'layers':layers,'audio':[],'full_motion_review':False,'full_audio_review':False}
assets={x:{'available':True,'rights':'verified','type':'image','path':str(O/y)} for x,y in [('ui','request-ui.png'),('assistant','assistant.png')]}
json.dump(doc,open(O/'approved-test-timeline.json','w'),ensure_ascii=False,indent=2)
# Newly generated quiet cues are tied to actual event times, not copied from the source.
cues=[(0.5,420),(3.2,520),(5.25,420),(5.8,460),(6.35,500),(11.05,440),(11.65,480),(12.25,520)]
rate=48000
with wave.open(str(O/'aligned-cues.wav'),'w') as wav:
 wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(rate)
 samples=[]
 for i in range(rate*15):
  t=i/rate;v=0
  for at,hz in cues:
   a=t-at
   if 0<=a<.14:v+=.035*math.sin(2*math.pi*hz*a)*math.exp(-a*35)*min(1,a/.008)
  samples.append(struct.pack('<h',int(32767*v)))
 wav.writeframes(b''.join(samples))
json.dump({'type':'original procedural cues; no narration; not source reproduction','unit':'seconds','events':cues},open(O/'sound-cues.json','w'),indent=2)
c=Compositor(doc,assets);c.render(O/'approved-test-v03.mp4',audio=O/'aligned-cues.wav')
sheet=Image.new('RGB',(1280,1080),'white')
for i,t in enumerate([.7,3.5,5.8,7.3,10.8,13]):sheet.paste(c.frame(t).resize((640,360)),((i%2)*640,(i//2)*360))
sheet.save(O/'qa.jpg');print(O/'approved-test-v03.mp4')
