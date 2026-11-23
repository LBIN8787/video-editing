from pathlib import Path
from functools import lru_cache
import math, json, wave, sys, subprocess
from PIL import Image, ImageDraw, ImageFont
import numpy as np, cv2

ROOT=Path.cwd()
TIMES=json.loads((ROOT/'time.json').read_text(encoding='utf-8'))
with wave.open(str(ROOT/'voice.wav')) as wav: END=wav.getnframes()/wav.getframerate()
FPS=24
W,H=1280,720
S=1.5
PW,PH=int(W*S),int(H*S)
K='#283b38'; GREEN='#24594d'; MINT='#81ac91'; LIGHT='#bed2af'; DARK='#184a40'; DEEP='#293c38'
PAPER='#f6efdb'; WHITE='#fff9e8'; SECOND='#536459'; GREY='#b0b6a0'; DUST='#d7d5ba'; OCHRE='#f3b765'; BOX='#e6954a'; SHADOW='#b76639'; RED='#a34631'; NIGHT='#233d36'
FONTS={'kr':'C:/Windows/Fonts/malgunbd.ttf','reg':'C:/Windows/Fonts/malgun.ttf','serif':str(Path(__file__).resolve().parents[2] / 'ytflow/assets/fonts/NanumMyeongjo-ExtraBold.ttf'),'num':'C:/Windows/Fonts/consolab.ttf','ital':'C:/Windows/Fonts/georgiai.ttf'}
@lru_cache(maxsize=800)
def font(kind,sz):return ImageFont.truetype(FONTS[kind],sz)
def unit(v):return max(0,min(1,v))
def ramp(t,a,b):return unit((t-a)/(b-a))
def ease(t,a,b):
    x=ramp(t,a,b);return x*x*(3-2*x)
def lerp(a,b,p):return a+(b-a)*p
def key(t,pairs):
    for (a,x),(b,y) in zip(pairs,pairs[1:]):
        if t<b:return lerp(x,y,ease(t,a,b))
    return pairs[-1][1]
def mix(a,b,p):
    av=bytes.fromhex(a[1:]);bv=bytes.fromhex(b[1:]);return '#'+''.join(f'{round(lerp(x,y,p)):02x}' for x,y in zip(av,bv))
class Pen:
    def __init__(self,im,x=0,y=0,k=1):
        self.im=im;self.d=ImageDraw.Draw(im);self.x=x;self.y=y;self.k=k
    def sub(self,x=0,y=0,k=1):return Pen(self.im,self.x+x*self.k,self.y+y*self.k,self.k*k)
    def p(self,x,y):return (round(S*(self.x+self.k*x)),round(S*(self.y+self.k*y)))
    def size(self,w):return max(1,round(S*self.k*w))
    def rect(self,x,y,w,h,fill,out=None,lw=2,r=0):
        if w<.1 or h<.1:return
        a=(*self.p(x,y),*self.p(x+w,y+h))
        if r:self.d.rounded_rectangle(a,radius=min(self.size(r),(a[2]-a[0])//2,(a[3]-a[1])//2),fill=fill,outline=out,width=self.size(lw))
        else:self.d.rectangle(a,fill=fill,outline=out,width=self.size(lw))
    def poly(self,pts,fill,out=None,lw=2):
        p=[self.p(x,y) for x,y in pts];self.d.polygon(p,fill)
        if out:self.d.line(p+[p[0]],fill=out,width=self.size(lw),joint='curve')
    def ln(self,pts,col=K,w=2):
        self.d.line([self.p(x,y) for x,y in pts],fill=col,width=self.size(w),joint='curve')
    def oval(self,x,y,w,h,fill,out=None,lw=2):
        if w<.2 or h<.2:return
        self.d.ellipse((*self.p(x,y),*self.p(x+w,y+h)),fill=fill,outline=out,width=self.size(lw))
    def txt(self,x,y,s,sz,col=K,kind='kr',anchor='lm'):
        self.d.text(self.p(x,y),s,font=font(kind,self.size(sz)),fill=col,anchor=anchor)
    def dash(self,x1,y1,x2,y2,col=GREY,w=1,step=10):
        a=math.hypot(x2-x1,y2-y1)
        if a<1:return
        for i in np.arange(0,a,step):
            v=min(a,i+step*.47)
            self.ln([(lerp(x1,x2,i/a),lerp(y1,y2,i/a)),(lerp(x1,x2,v/a),lerp(y1,y2,v/a))],col,w)
    def bez(self,pts,col,w=2,frac=1):
        p0,p1,p2,p3=pts
        def pos(t):
            return tuple((1-t)**3*p0[i]+3*(1-t)**2*t*p1[i]+3*(1-t)*t*t*p2[i]+t**3*p3[i] for i in range(2))
        if frac>.02:self.ln([pos(k*frac/24) for k in range(25)],col,w)
def label(p,x,y,txt,col=GREEN):
    p.txt(x,y,txt,18,col,'kr')
def carton(p,x,y,z=1,n=1,seal=1):
    q=p.sub(x,y,z)
    # Optical perspective, tape straddling lid and front face, and a small batch ticket.
    q.poly([(0,-47),(15,-57),(84,-57),(70,-47)],'#f4bc78',K,2)
    q.poly([(70,-47),(84,-57),(84,-10),(70,0)],SHADOW,K,2)
    q.poly([(0,-47),(70,-47),(70,0),(0,0)],BOX,K,2)
    if seal<.999:
        # Open flaps flatten against the top as the tape head presses the seam.
        gap=(1-seal)*28
        q.poly([(0,-47),(15,-57),(46,-57-gap),(32,-47-gap)],'#f6c48e',K,1.6)
        q.poly([(70,-47),(84,-57),(54,-57-gap),(40,-47-gap)],'#edaa63',K,1.6)
    if seal>.02:
        q.poly([(29,-47),(44,-57),(54,-57),(39,-47)],'#f9d5a0')
        q.rect(29,-47,10,15*seal,'#f9d5a0')
    q.rect(7,-21,23,13,WHITE,None,r=1)
    q.txt(18.5,-15.5,f'{n:02}',9,K,'num','mm')
    for k in [0,3,6,10]:q.ln([(51+k,-11),(51+k,-5)],K,1)
    q.ln([(5,-3),(24,-3)],'#d58845',1)
def shadow(p,x,y,w):p.oval(x,y,w,10,'#c3c3a7')
def factory(p,t):
    # A section through the packing works. The sawtooth roof and lit loading aperture share a baseline.
    p.rect(69,242,38,112,'#9ca995',K,2)
    p.rect(65,235,46,11,LIGHT,K,2)
    for j in range(3):p.ln([(72,252+j*12),(104,252+j*12)],GREEN,2)
    p.poly([(53,331),(110,292),(110,320),(177,279),(177,310),(250,270),(250,300),(355,300),(355,458),(53,458)],'#a9bea4',K,3)
    p.ln([(52,329),(111,290),(111,318),(178,277),(178,308),(251,268),(251,297),(358,297)],GREEN,7)
    p.poly([(53,413),(250,413),(250,457),(53,457)],'#95ad97')
    for i in range(4):
        p.rect(75+i*38,344,29,35,'#e9e6c8',K,2)
        p.ln([(76+i*38,361),(102+i*38,361)],GREEN,2)
        p.ln([(89+i*38,346),(89+i*38,377)],GREEN,2)
    p.rect(65,396,117,32,GREEN,None,r=3);p.txt(123,411,'포장 공장',18,WHITE,'kr','mm')
    p.rect(248,331,110,128,'#718b76',K,3)
    p.rect(259,344,89,110,'#334d44',K,2)
    for i in range(3):p.ln([(261,347+i*8),(345,347+i*8)],'#9fae92',2)
    p.rect(54,455,306,11,'#d5c8a7',K,2)
def belt(p,t):
    p.rect(290,450,498,23,'#8b9f8d',K,3,11)
    for j in range(23):
        x=301+j*21.5;p.oval(x-4.8,456,9.6,9.6,PAPER,K,1)
        a=t*3.1;p.ln([(x,461),(x+3*math.cos(a),461+3*math.sin(a))],GREEN,1)
    for x in [344,475,627,749]:
        p.poly([(x,473),(x+8,473),(x+1,503),(x-5,503)],GREEN,K,1)
    p.ln([(350,491),(745,491)],'#819483',3)
def gate(p,cl):
    p.rect(786,299,88,12,GREEN,K,2)
    for x in [790,857]:
        p.rect(x,309,11,192,'#9daf95',K,2)
        p.rect(x-3,494,17,8,'#c0bda1',K,1)
    p.rect(798,289,64,27,WHITE,K,2,3);p.txt(830,302,'출하',17,GREEN,'kr','mm')
    h=16+cl*130
    p.rect(802,315,53,h,'#d9d4b9',K,2)
    for y in np.arange(322,315+h-3,10):p.ln([(804,y),(852,y)],'#889383',1.2)
    p.rect(800,313+h,57,7,RED if cl>.5 else GREEN,K,1)
    for i in range(5):p.ln([(806+i*10,315+h),(810+i*10,318+h)],WHITE,2)
    p.oval(823,271,13,13,RED if cl>.5 else MINT,K,2)
def truck(p,x,t,travel):
    q=p.sub(x,0)
    shadow(q,2,497,286)
    q.rect(5,434,184,12,'#8d9b82',K,2,2)
    q.rect(0,447,268,22,GREEN,K,3,4)
    q.rect(36,467,78,12,'#82917b',K,2,3)
    q.poly([(185,449),(185,368),(218,368),(240,375),(266,409),(276,416),(276,460),(254,469),(207,467)],'#75a68d',K,3)
    q.poly([(195,378),(216,378),(232,383),(248,407),(195,407)],'#d7e5ce',K,2)
    q.ln([(215,379),(215,405)],GREEN,2)
    q.ln([(193,416),(193,446),(230,446)],GREEN,2)
    q.rect(199,418,10,2,K,None,r=1)
    q.rect(262,424,13,8,'#f5cd7d',K,1,2);q.rect(258,453,23,8,WHITE,K,2,2)
    for xx in [43,219]:
        q.oval(xx-20,463,40,40,K);q.oval(xx-11,472,22,22,'#d7d5b9',K,2)
        a=travel*.045
        for j in range(3):
            th=a+j*math.tau/3;q.ln([(xx,483),(xx+7*math.cos(th),483+7*math.sin(th))],GREEN,2)
def shop(p):
    p.rect(2058,299,214,153,'#dabf8a',K,3)
    p.rect(2050,287,229,22,'#edc998',K,3,4)
    p.rect(2072,314,186,35,WHITE,K,2,3)
    p.txt(2166,331,'고객 창고',20,GREEN,'kr','mm')
    p.rect(2083,360,127,92,'#627f6b',K,2);p.rect(2093,370,108,82,'#425b4f',K,1)
    for i in range(4):p.ln([(2094,373+i*7),(2199,373+i*7)],'#8b9c87',2)
    p.rect(2220,365,26,37,'#eee7ca',K,2);p.ln([(2233,366),(2233,401)],K,1)
    p.rect(1968,448,302,18,'#d1bd95',K,2,2)
    for x in [1989,2050,2228]:p.rect(x,466,10,34,GREEN,K,1)
def backdrop(p):
    p.ln([(-10,505),(2500,505)],'#6d806d',2)
    p.ln([(-10,511),(2500,511)],'#b7bda2',1)
    for i in range(48):
        x=i*52+5;p.ln([(x,517),(x+9,517)],'#d4d2b8',1)
    # Sparse low-contrast silhouettes hold the geography together through the camera track.
    for x in [458,1125,1460,1860]:
        p.ln([(x,451),(x,390),(x+23,390),(x+23,368),(x+46,368),(x+46,407),(x+78,407),(x+78,381),(x+111,381),(x+111,451)],'#cfd1b7',1.3)
    for x in [1230,1475,1690]:
        p.ln([(x,502),(x,329),(x+14,320),(x+30,320)],'#adb79e',3)
        p.oval(x+22,318,15,4,'#adb79e')
def price(p,t):
    z=ease(t,5.28,5.72)*(1-ease(t,8.48,8.94))
    if z<.01:return
    q=p.sub(575,349+(1-z)*22,z)
    q.ln([(0,27),(20,53),(35,65)],RED,2)
    q.poly([(-74,-24),(51,-24),(70,-2),(51,22),(-74,22)],'#ffe4ad',RED,2)
    q.oval(46,-5,8,8,PAPER,RED,1);q.txt(-9,-1,'10만 원',25,RED,'kr','mm')
def rail_label(p,x,y,s,col,tagw):
    p.rect(x,y,tagw,32,PAPER,col,1.8,15);p.txt(x+tagw/2,y+15,s,17,col,'kr','mm')
def contract(p,t):
    a=ease(t,15.15,15.7)*(1-ease(t,19.05,19.58))
    if a<=.01:return
    q=p.sub(908,212-(1-a)*175)
    q.rect(5,6,273,151,'#b9b69c',None,r=4);q.rect(0,0,273,151,WHITE,K,2.5,4)
    q.rect(0,0,9,151,GREEN,None,r=3)
    q.txt(25,25,'계약서 발췌',16,GREEN);q.txt(251,25,'01',16,SECOND,'num','rm')
    q.dash(25,45,249,45,GREY)
    q.txt(25,69,'매출 인식 조건',22,K,'serif')
    a2=ease(t,16.5,17.96)
    q.rect(22,100,191*a2,24,'#f5d88b')
    q.txt(25,111,'고객에게 인도한 때',21,GREEN,'kr')
    q.ln([(25,132),(25+193*ease(t,17.5,18.12),132)],RED,2)
def sig(p,x,y,frac,col=GREEN):
    pts=[(0,7),(12,-9),(7,5),(3,16),(15,3),(26,-9),(20,8),(32,0),(28,10),(43,2),(51,-1),(47,4),(62,2),(77,0)]
    v=max(0,min(len(pts)-1,frac*(len(pts)-1)))
    k=int(v)
    if k < len(pts)-1:
        pts=pts[:k+1]+[(lerp(pts[k][0],pts[k+1][0],v-k),lerp(pts[k][1],pts[k+1][1],v-k))]
    if v>.01:p.ln([(x+a,y+b) for a,b in pts],col,2.7)
def receipt(p,x,y,s,t):
    q=p.sub(x,y,s)
    q.rect(5,5,207,131,'#b8b8a0',None,r=4);q.rect(0,0,207,131,WHITE,K,2.5,4)
    q.rect(0,0,207,7,GREEN)
    q.txt(16,31,'인수증',22,GREEN,'serif');q.txt(190,32,'07.01',17,SECOND,'num','rm')
    q.dash(15,53,190,53,GREY);q.txt(16,73,'수량',14,SECOND);q.txt(190,73,'3상자',17,K,'kr','rm')
    q.txt(16,104,'인수인',14,SECOND);q.ln([(78,113),(190,113)],GREY,1)
    sig(q,91,104,ease(t,25.64,26.23))
def shipment(p,t):
    cam=key(t,[(0,0),(21.57,0),(23.51,1032)])
    zoom=key(t,[(0,1.29),(1.6,1.29),(4.38,1.07),(4.83,1.07),(5.83,1.66),(8.25,1.66),(9.45,1.02),(12.25,1.07),(15.1,1),(19.7,1)])
    anchor=key(t,[(0,404),(4.48,490),(5.85,561)])
    world=p.sub((1-zoom)*anchor-cam,(1-zoom)*478,zoom)
    backdrop(world);factory(world,t);shop(world);belt(world,min(t,9.4)+max(0,min(2,t-19.75)))
    cl=ease(t,9.18,10.15)*(1-ease(t,19.71,20.29))
    gate(world,cl)
    # A tape reel feeds a sprung pressure shoe mounted over the packing line.
    world.rect(355,374,14,78,'#8fa78c',K,2,3)
    world.rect(352,369,48,9,GREEN,K,2,3)
    world.oval(360,346,26,26,'#e7c68b',K,2)
    world.oval(368,354,10,10,PAPER,K,1.5)
    press=sum(max(0,1-abs(t-hit)/.20) for hit in [1.28,2.02,2.83])
    world.ln([(379,364),(397,375),(400,385+9*press)],'#ac7442',3)
    world.rect(391,382+9*press,20,5,GREEN,K,1.5,2)
    travel=773*ease(t,21.28,23.45);tx=873+travel
    truck(world,tx,t,travel)
    # Every numbered parcel stays identifiable across the factory, the lorry and the loading platform.
    for i in [2,1,0]:
        xinit=[612,517,422][i]; queue=[696,602,508][i]
        a=.25+.65*i
        if t<a:continue
        entry=ease(t,a,3.01+.42*i)
        x=lerp(304,xinit,entry);y=450
        x=lerp(x,queue,ease(t,8.92+.32*i,10.42+.55*i))
        load=ease(t,20.05+i*.19,20.93+i*.18)
        xp=tx+[126,66,6][i]
        x=lerp(x,xp,load)
        size=lerp(.72+.28*entry,.69,load)
        y=lerp(y,434,load)-math.sin(math.pi*load)*12
        # Draw the farthest carton first; each lands in its own dock position.
        give=ease(t,23.39+i*.27,24.55+i*.29)
        x=lerp(x,2141-i*78,give);size=lerp(size,.85,give)
        y=lerp(y,447,give)-24*math.sin(math.pi*give)
        carton(world,x,y,size,i+1,ease(t,[1.08,1.82,2.63][i],[1.47,2.21,3.02][i]))
    price(world,t)
    if 11.73<t<19.9:
        a=ease(t,11.73,12.28)*(1-ease(t,19.35,19.9))
        world.ln([(509,376),(509,365),(509+258*a,365),(509+258*a,376)],RED,2)
        if a>.85:rail_label(world,584,329,'재고  3상자',RED,132)
    contract(p,t)

def ledger(p,t):
    # One open ledger lets the empty June entry and the July entry coexist at the same scale.
    a=ease(t,26.65,27.5)
    q=p.sub(347,211+24*(1-a))
    q.rect(2,8,850,320,'#abae96',None,r=12)
    q.rect(0,0,847,320,GREEN,K,3,11)
    for off in [9,6,3]:
        q.poly([(13,10+off),(404,7+off),(421,15+off),(443,7+off),(833,11+off),(833,297+off),(445,292+off),(421,301+off),(402,294+off),(13,299+off)],'#e3d4ad',K,1)
    q.poly([(13,10),(397,6),(421,14),(421,299),(398,291),(13,297)],'#eee7ce',K,1.5)
    q.poly([(421,14),(441,6),(832,10),(832,297),(445,291),(421,299)],WHITE,K,1.5)
    for n in range(5):q.ln([(419-n*1.8,15),(419-n*1.8,296)],mix('#b7ae8d','#e4dbc2',n/5),1.7)
    for n in range(5):q.ln([(424+2*n,14),(424+2*n,296)],mix('#d4c6a2',WHITE,n/5),1.4)
    q.poly([(777,10),(794,10),(794,43),(786,37),(777,43)],RED)
    for xp,month in [(40,'6월'),(452,'7월')]:
        q.txt(xp,54,month,37,GREEN,'serif')
        q.txt(xp+320,56,'매출 장부',16,SECOND,'kr','rm')
        q.ln([(xp,83),(xp+329,83)],GREEN,1.8)
        for j in range(3):q.ln([(xp,135+59*j),(xp+329,135+59*j)],'#c9c6ab',1)
    q.txt(40,111,'06.30',19,SECOND,'num');q.txt(140,110,'포장 완료',20,K)
    q.txt(43,158,'이 주문 매출',15,SECOND);q.txt(360,217,'0원',37,SECOND,'kr','rm')
    q.txt(452,111,'07.01',19,SECOND,'num');q.txt(552,110,'고객 인도',20,K)
    for j in range(3):
        f=ease(t,27.08+.12*j,27.45+.12*j)
        if f>.01:carton(q,453+j*37,174,.37*f,j+1)
    if t>27.62:q.txt(590,162,'3상자 × 10만 원',20,K)
    amt=ease(t,29.40,29.63)
    if amt>0:
        s=1+.13*(1-amt)
        qq=q.sub(619-147*s,223-36*s+8*(1-amt),s)
        qq.rect(0,0,294,69,'#f6dfba',RED,3,4)
        qq.rect(5,5,284,59,None,RED,1,2)
        qq.txt(147,33,'300,000원',39,RED,'kr','mm')
    contact=29.53
    if 28.99<t<30.09:
        h=key(t,[(28.99,-240),(29.31,-113),(contact,0),(29.61,-4),(30.09,-268)])
        # A printer’s stamp arrives just before the imprint and rebounds off the paper.
        f=q.sub(617,220+h)
        f.rect(-90,-37,180,25,'#a1653d',K,2,7);f.rect(-91,-18,182,12,K,None,3,3)
        f.poly([(-21,-37),(-12,-54),(-12,-83),(13,-83),(13,-54),(23,-37)],'#94613e',K,2)
        f.oval(-36,-110,71,40,'#b57a48',K,2)
        f.bez([(-29,-95),(-19,-104),(5,-109),(17,-101)],'#e1b781',2)
def track(p,t):
    # Stable route / changing state, analogous to the fixed baseline in the reference.
    coords=[224,640,1056]
    marks=[3.64,21.79,24.93]
    p.ln([(224,562),(1056,562)],'#c4c7ab',2)
    pos=224+416*ease(t,20.06,21.86)+416*ease(t,22.0,24.93)
    p.ln([(224,562),(pos,562)],GREEN,3)
    for i,(x,tt,s) in enumerate(zip(coords,marks,['포장','출하','고객 인도'])):
        on=t>=tt
        p.oval(x-6,556,12,12,GREEN if on else PAPER,GREEN if on else '#a0ab96',2)
        if on:p.oval(x-2,560,4,4,WHITE)
        p.txt(x,589,s,18,GREEN if on else SECOND,'kr','mm')
def header(p,t):
    p.rect(61,34,28,7,RED);p.txt(100,38,'가상 거래   /   인도 조건',16,GREEN,'kr')
    p.txt(57,105,'이 상자는 언제 매출이 될까?',51,K,'serif')
    p.ln([(61,160),(1218,160)],K,2)
    # Two pinned calendar leaves, one date changes when the lorry can leave.
    x,y=1076,42
    p.rect(x+4,y+5,141,93,'#c0c0a5',K,1,6);p.rect(x,y,141,93,WHITE,K,2,6)
    p.rect(x+1,y+1,139,21,GREEN,None,r=4)
    for xx in [x+27,x+114]:p.rect(xx,y-7,5,15,K,None,r=2)
    july=t>=19.87
    p.txt(x+70,y+10,'출하 달력',13,WHITE,'kr','mm')
    p.txt(x+70,y+57,'07.01' if july else '06.30',37,GREEN if july else RED,'num','mm')
    if 19.72<t<20.07:
        a=ramp(t,19.72,20.07);hh=56*(1-abs(2*a-1))
        p.poly([(x+3,y+23),(x+136,y+23),(x+136,y+23+hh*.7),(x+3,y+23+hh)],'#e5d9b9',GREY,1)
def caption(p,t):
    idx=0
    for j,b in enumerate(TIMES):
        if t+.025>=b['start']:idx=j
    p.rect(0,626,1280,94,NIGHT)
    p.rect(0,626,1280,3,'#8da990')
    p.txt(640,672,TIMES[idx]['cap'],31,WHITE,'kr','mm')
def canvas():
    rng=np.random.default_rng(430)
    yy,xx=np.mgrid[0:PH,0:PW].astype('float32')
    vign=(.45*((xx-PW*.52)/(PW*.60))**2+.50*((yy-PH*.46)/(PH*.68))**2)
    broad=cv2.resize(rng.normal(0,1,(18,28)).astype('float32'),(PW,PH),interpolation=cv2.INTER_CUBIC)
    grain=rng.normal(0,1.15,(PH,PW)).astype('float32')+broad*.90-vign*3.7
    arr=np.clip(np.array([247,241,222])[None,None,:]+grain[:,:,None],0,255).astype('uint8')
    im=Image.fromarray(arr);p=Pen(im)
    for i in range(460):
        x,y=rng.uniform(12,1268),rng.uniform(12,611);length=rng.uniform(.4,2.6)
        p.ln([(x,y),(x+length,y-.25)],'#e0dbc4',.5)
    return im
BASE=canvas()
def frame(t):
    im=BASE.copy();p=Pen(im)
    blend=ease(t,26.78,27.41)
    if blend<1:shipment(p,t)
    if blend>0:
        if blend<1:
            other=BASE.copy();ledger(Pen(other),t)
            im=Image.blend(im,other,blend);p=Pen(im)
        else:ledger(p,t)
    if t>23.85:
        a=ease(t,23.85,24.45);b=ease(t,26.78,27.48)
        receipt(p,lerp(215,67,b),lerp(246,309,b)+35*(1-a),a*(1+.17*b),t)
    im.paste(BASE.crop((0,0,PW,round(161*S))),(0,0))
    im.paste(BASE.crop((0,round(537*S),PW,PH)),(0,round(537*S)))
    header(p,t);track(p,t);caption(p,t)
    return im.resize((W,H),Image.Resampling.LANCZOS)
if __name__=='__main__':
    if 'qa' in sys.argv:
        snaps=[.7,3.8,6.9,10.42,13.8,17.81,20.93,22.7,25.97,27.95,29.52,30.8]
        out=Image.new('RGB',(4*384,3*216))
        for i,t in enumerate(snaps):
            img=frame(t);img.save(ROOT/f'frame-{t:.2f}.jpg',quality=92)
            out.paste(img.resize((384,216),Image.Resampling.LANCZOS),(i%4*384,i//4*216))
        out.save(ROOT/'sheet.jpg',quality=94)
    else:
        cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-i',str(ROOT/'mix.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-preset','veryfast','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-af','loudnorm=I=-15:LRA=7:TP=-1.5,aresample=48000','-movflags','+faststart','-metadata','title=이 상자는 언제 매출이 될까?',str(ROOT/'inventory-to-revenue.mp4')]
        proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
        for i in range(math.ceil(END*FPS)):
            proc.stdin.write(frame(i/FPS).tobytes())
        proc.stdin.close()
        if proc.wait():raise RuntimeError('Encoding failed')
