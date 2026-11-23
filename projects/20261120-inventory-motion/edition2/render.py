from pathlib import Path
from functools import lru_cache
import math, os, sys, json, subprocess
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

HERE=Path(__file__).resolve().parent
WORK=Path(os.environ.get("INVENTORY_WORK",str(HERE)))
SRC=Path(os.environ.get("INVENTORY_AUDIO",str(WORK.parent)))
ART=WORK/'art'
CLOCK=json.loads((SRC/'time.json').read_text(encoding='utf-8-sig'))
S=float(os.environ.get('ART_SCALE','1.5')); W,H=round(1280*S),round(720*S)
RATE=30; FRAMES=960
INK='#19252b'; BLUE='#243a48'; RED='#a73628'; VERM='#cb4a33'; GOLD='#f3c27e'
IVORY='#f3ecdb'; WHITE='#fff9e9'; MUTED='#66655c'
def clamp(x):return max(0,min(1,x))
def norm(t,a,b):return clamp((t-a)/(b-a))
def e(t,a,b):
    k=norm(t,a,b);return k*k*(3-2*k)
def out(t,a,b):return 1-(1-norm(t,a,b))**3
def l(a,b,p):return a+(b-a)*p
def show(t,a,b):return e(t,a,a+.22)*(1-e(t,b-.22,b))
def pix(x):return round(x*S)
def ipt(pt):return tuple(pix(n) for n in pt)
def lin(im,pts,color,w=2):
    ImageDraw.Draw(im).line([ipt(p) for p in pts],fill=color,width=max(1,pix(w)),joint='curve')
def rect(im,box,color,outl=None,w=1):
    x,y,r,b=box
    if r>=x and b>=y:ImageDraw.Draw(im).rectangle(ipt(box),fill=color,outline=outl,width=max(1,pix(w)))
def oval(im,box,color,outl=None,w=1):
    ImageDraw.Draw(im).ellipse(ipt(box),fill=color,outline=outl,width=max(1,pix(w)))
def poly(im,pts,col):ImageDraw.Draw(im).polygon([ipt(p) for p in pts],fill=col)
def dash(im,a,b,col,w=1,step=12):
    length=math.dist(a,b)
    for j in range(0,int(length),step):
        hi=min(j+.55*step,length)
        lin(im,[(l(a[0],b[0],n/length),l(a[1],b[1],n/length)) for n in [j,hi]],col,w)
def bez(p0,p1,p2,p3,n=45):
    return [tuple((1-t)**3*p0[i]+3*(1-t)**2*t*p1[i]+3*(1-t)*t*t*p2[i]+t**3*p3[i] for i in (0,1)) for t in np.linspace(0,1,n)]
def arrow(im,pts,frac=1,color=RED,w=3,head=11):
    n=int((len(pts)-1)*clamp(frac))+1
    if n<2:return
    lin(im,pts[:n],color,w)
    if frac<.95:return
    x,y=pts[n-1];xp,yp=pts[n-2];a=math.atan2(y-yp,x-xp)
    lin(im,[(x+head*math.cos(a+2.62),y+head*math.sin(a+2.62)),(x,y),(x+head*math.cos(a-2.62),y+head*math.sin(a-2.62))],color,w)
REPO=next((p for p in [HERE,*HERE.parents,Path('D:/ytflow/video-editing')] if (p/'ytflow/assets/fonts/NanumPenScript-Regular.ttf').is_file()),None)
FONTS=Path(os.environ.get('WINDIR','C:/Windows'))/'Fonts'
@lru_cache(maxsize=160)
def font(kind,size):
    file={'bold':FONTS/'NotoSansKR-VF.ttf','reg':FONTS/'NotoSansKR-VF.ttf','num':FONTS/'impact.ttf','mono':FONTS/'consolab.ttf','hand':REPO/'ytflow/assets/fonts/NanumPenScript-Regular.ttf'}[kind]
    f=ImageFont.truetype(str(file),size)
    if kind in ('bold','reg'):f.set_variation_by_axes([870 if kind=='bold' else 515])
    return f
def text(im,x,y,s,size,kind='bold',col=INK,align='lm'):
    ImageDraw.Draw(im).text(ipt((x,y)),s,font=font(kind,pix(size)),fill=col,anchor=align,stroke_width=0)
COORDS={'box':(1,0,0,495,502),'truck':(1,496,92,1023,465),'factory':(1,1026,11,1536,464),'hand':(1,0,539,550,969),'stamp':(1,550,492,1005,1012),'clip':(1,1070,486,1536,1024),'gate':(2,0,0,744,509),'ledger':(2,768,0,1536,504),'pen':(2,0,513,764,1024),'openbox':(2,769,512,1536,1024)}
plates={j:Image.open(ART/f).convert('RGBA') for j,f in [(1,'object-plate.png'),(2,'document-plate.png')]}
assets={}
for name,(j,*box) in COORDS.items():
    im=plates[j].crop(box);a=im.getchannel('A');bb=a.point(lambda v:255 if v>90 else 0).getbbox()
    im=im.crop(bb);im.putalpha(im.getchannel('A').point(lambda v:0 if v<18 else min(255,round(v*255/253))))
    assets[name]=im
def rawtxt(im,xy,s,f,col,anchor='mm'):
    ImageDraw.Draw(im).text(xy,s,font=f,fill=col,anchor=anchor)
for no in range(1,4):
    im=assets['box'].copy();ww,hh=im.size
    ft=font('mono',round(ww*.136))
    label=Image.new('RGBA',(round(ww*.39),round(hh*.24)))
    rawtxt(label,(label.width/2,label.height/2),f'{no:02}',ft,BLUE)
    label=label.rotate(-6,resample=Image.Resampling.BICUBIC,expand=True)
    im.alpha_composite(label,(round(ww*.05),round(hh*.43)));assets[f'b{no}']=im
assets['handR']=ImageOps.mirror(assets['hand'])
# Isolate the two hub engravings so their rotation follows road travel without moving the fenders.
for wheel,cx in [('rearhub',.211),('fronthub',.784)]:
    src=assets['truck'];ww,hh=src.size;r=round(ww*.052);cx=round(ww*cx);cy=round(hh*.811)
    tile=src.crop((cx-r,cy-r,cx+r,cy+r));mask=Image.new('L',tile.size)
    ImageDraw.Draw(mask).ellipse((1,1,2*r-2,2*r-2),fill=255);tile.putalpha(mask);assets[wheel]=tile
def scaled(name,w):
    src=assets[name];return src.resize((w,max(1,round(src.height*w/src.width))),Image.Resampling.BICUBIC)
scaled=lru_cache(maxsize=75)(scaled)
def sprite(im,name,x,y,width,anchor=(0,1),angle=0,alpha=1):
    if width<1 or alpha<=.005:return
    a=scaled(name,max(1,pix(width)))
    if abs(angle)>.19:a=a.rotate(angle,Image.Resampling.BICUBIC,expand=True)
    if alpha<.995:
        a=a.copy();a.putalpha(a.getchannel('A').point(lambda c:round(c*alpha)))
    pt=(round(x*S-a.width*anchor[0]),round(y*S-a.height*anchor[1]))
    im.paste(a,pt,a)
def bg(kind):
    pal={'warm':(240,235,222),'dark':(34,44,49),'blue':(220,227,223),'linen':(232,219,196)}
    c=np.array(pal[kind]).reshape(1,1,3)
    rng=np.random.default_rng(4322)
    y,x=np.mgrid[0:H,0:W];v=(.6*((x-W*.48)/W)**2+((y-H*.36)/H)**2)*8
    cloud=cv2.resize(rng.normal(0,1,(24,40)).astype('float32'),(W,H),interpolation=cv2.INTER_CUBIC)
    grain=rng.normal(0,2.65,(H,W)).astype('float32')
    gr=cloud*1.3+grain-v+1+(.4*np.sin(y*.9)+.5*np.cos(x*1.11))
    arr=np.uint8(np.clip(c+gr[:,:,None],0,255))
    im=Image.fromarray(arr);dr=ImageDraw.Draw(im)
    for _ in range(6200):
        a,b=rng.integers(0,W),rng.integers(0,H);ink=tuple(np.clip(c.ravel()+rng.choice([-11,-7,6]),0,255))
        dr.line((a,b,a+rng.integers(1,5),b+rng.integers(-1,2)),fill=ink,width=1)
    return im
BG={k:bg(k) for k in ['warm','dark','blue','linen']}
def head(im,title,night=False):
    co='#e3dece' if night else INK
    rect(im,(59,57,82,62),VERM)
    text(im,95,60,title,18,'bold',co)
def note(im,x,y,s,col=RED):text(im,x,y,s,36,'hand',col)
def caption(im,t,dark=False):
    idx=max([0]+[i for i,r in enumerate(CLOCK) if t>=r['start']-.04])
    if t>CLOCK[idx]['end']+.34 and idx!=7:return
    cap=CLOCK[idx]['cap'];f=font('reg',pix(28));wi=f.getlength(cap)/S
    col=WHITE if dark else INK
    # A tight paper slip separates the narration from the art only where the words sit.
    rect(im,(640-wi/2-13,644,640+wi/2+13,690),'#1d292f' if dark else '#f7f3e8')
    text(im,640,665,cap,28,'reg',col,'mm')
def ground(im,x1,x2,y,dark=False):
    lin(im,[(x1,y),(x2,y)],'#adad9b' if dark else '#56574f',2)
def shadow(im,x,y,width,depth=10,dark=False):
    # Low stippled contact shadow printed on the same stock.
    for k in range(3):
        co=(['#30393a','#2c3435','#20292b'] if dark else ['#d8d3c3','#c9c3b0','#bab5a3'])[k]
        oval(im,(x+width*.10*k,y-depth/2+k,x+width*(1-.10*k),y+depth/2-k),co)
def date(im,x,y,val,small=False):
    text(im,x,y,val,47 if small else 88,'num',INK)
def factory_scene(t):
    im=BG['warm'].copy();head(im,'가상 계약  /  생산')
    p=e(t,1.77,3.54)
    text(im,59,156,'6월 30일',67,'bold')
    lin(im,[(62,217),(208,217)],RED,3);text(im,225,217,'공장 포장일',23,'reg')
    fx=l(4,15,p);fwidth=l(389,405,p)
    sprite(im,'factory',fx,541,fwidth)
    ground(im,56,1219,552)
    firstx=l(884,663,p);firstw=l(381,183,p)
    # Unsealed cardboard becomes one sealed parcel on the packing beat.
    seal=e(t,1.48,1.76)
    if seal<1:sprite(im,'openbox',firstx,543,l(412,225,p),(.5,1),alpha=1-seal)
    if seal>0:sprite(im,'b1',firstx,543,firstw,(.5,1),alpha=seal)
    for i,(xx,at) in enumerate([(876,2.48),(1092,2.97)]):
        k=out(t,at,at+.52)
        if k:
            shadow(im,xx-83,546,163,7)
            bounce=13*math.sin(norm(t,at+.45,at+.74)*math.pi)
            sprite(im,'b'+str(i+2),xx+l(72,0,k),l(267,543,k)-bounce,183,(.5,1),angle=l(-9,0,k),alpha=min(1,k*2))
    if t>3.46:
        ln=e(t,3.46,4.0)
        lin(im,[(563,315),(563,300),(563+635*ln,300)],RED,2)
        if ln>.94:lin(im,[(1197,300),(1197,315)],RED,2)
        if t>3.90:text(im,879,266,'완성품  3상자',33,'hand',RED,'mm')
    return im
def price_scene(t):
    im=BG['warm'].copy();head(im,'가상 계약  /  주문 단가')
    k=out(t,4.86,5.48)
    shadow(im,95,564,405,15)
    sprite(im,'b1',l(222,302,k),560,l(362,438,k),(.5,1),angle=l(-4,0,k))
    text(im,650,182,'한 상자 가격',32,'bold')
    lin(im,[(651,225),(1119,225)],INK,2)
    k=out(t,5.58,6.12)
    if k>0:
        text(im,645,l(364,336,k),'10',157,'num',RED)
        text(im,809,l(398,372,k),'만 원',71,'bold',RED)
        arrow(im,bez((664,392),(608,431),(540,382),(454,375)),e(t,5.67,6.26),INK,2.8,13)
    q=out(t,6.92,7.43)
    if q:text(im,646,l(500,475,q),'오늘 매출은 얼마일까?',40,'hand',BLUE)
    return im
def shutter(im,x,y,w,f):
    obj=assets['gate'];h=w*obj.height/obj.width
    # The shutter slats travel in fixed side rails. The bottom red rail remains visible while it lowers.
    q=scaled('gate',pix(w));qw,qh=q.size;ix=pix(x);iy=pix(y)
    xa=int(qw*.1);xb=int(qw*.901);yt=int(qh*.09);yb=int(qh*.979)
    rect(im,(x+2,y+4,x+w-2,y+h-3),'#17262b')
    for b in [(0,0,qw,yt),(0,yt,xa,qh),(xb,yt,qw,qh)]:
        a=q.crop(b);im.paste(a,(ix+b[0],iy+b[1]),a)
    sh=round((yb-yt)*(.12+.88*f));slat=q.crop((xa,yb-sh,xb,yb))
    im.paste(slat,(ix+xa,iy+yt),slat)
    return h
def jam(t):
    im=BG['dark'].copy();head(im,'가상 계약  /  출하',True)
    tick=e(t,8.99,9.43)
    text(im,58,162+l(12,0,tick),'출하 지연',71,'bold',WHITE)
    close=e(t,9.32,10.14)
    yy=176+math.sin(norm(t,10.11,10.34)*math.pi*2)*4*(1-norm(t,10.11,10.34))
    shutter(im,825,yy,427,close);ground(im,58,1220,552,True)
    for i,(start,target,bottom,at,width) in enumerate([(106,669,544,9.17,151),(-102,500,544,9.58,154),(-110,586,423,10.65,146)]):
        f=out(t,at,at+1.38)
        if not f and i:continue
        b=l(546,bottom,f)
        if i==2:b-=115*math.sin(math.pi*f)
        sprite(im,'b'+str(i+1),l(start,target,f),b,width,(.5,1),angle=((-5 if i!=2 else 9)*math.sin(math.pi*f)))
    if t>10.24:
        f=e(t,10.24,10.58)
        lin(im,[(774,503),(774+16*f,492)],GOLD,2)
        lin(im,[(778,520),(778+20*f,519)],GOLD,2)
    if t>12.17:
        f=out(t,12.17,12.72)
        text(im,65,l(354,340,f),'재고',62,'bold',GOLD)
        arrow(im,bez((179,391),(235,407),(265,479),(405,472)),e(t,12.32,13.08),GOLD,3,13)
    return im

def contract(t):
    im=BG['warm'].copy();head(im,'가상 계약  /  매출 인식 조건')
    k=out(t,15.04,15.54);xx=l(15,101,k)
    sprite(im,'clip',xx,607,371)
    text(im,xx+63,254,'계약서',47,'bold')
    lin(im,[(xx+62,305),(xx+280,305)],BLUE,2)
    text(im,xx+65,349,'매출 인식 시점',25,'reg')
    text(im,xx+65,404,'고객 인도 시',31,'bold',RED)
    lin(im,[(xx+68,436),(xx+68+181*e(t,16.1,17.14),430)],RED,3)
    slide=out(t,15.42,16.39)
    hx=l(998,705,slide)
    sprite(im,'handR',hx,569,580)
    q=e(t,16.25,17.76)
    boxx=l(646,938,q);by=l(274,395,q)-33*math.sin(math.pi*q)
    if t<17.6:dash(im,(652,427),(866,427),'#9f8973',2,13)
    sprite(im,'b1',boxx,by,167,(.5,1),angle=l(5,0,q))
    if t>17.62:
        text(im,720,198,'인도',57,'bold',INK)
        arrow(im,bez((817,205),(866,194),(915,211),(933,247)),e(t,17.65,18.22),RED,3,12)
    return im
def departure(t):
    im=BG['blue'].copy();head(im,'가상 계약  /  출하 재개')
    xcal=61
    text(im,xcal,151,'7월 1일',68,'bold')
    if t<20.01:
        frac=1-e(t,19.58,20.01)
        rect(im,(xcal,102,xcal+232,102+98*frac),'#e9e2c9')
        if frac>.56:text(im,xcal+10,146,'6월 30일',49,'bold',MUTED)
    camera=190*e(t,21.39,23.08)
    ground(im,25,1251,554)
    sprite(im,'factory',-99-camera,538,434)
    shutter(im,229-camera,346,225,1-e(t,19.64,20.32))
    walk=e(t,20.68,23.25);tx=370+731*walk-camera
    y=552-1.6*math.sin(norm(t,20.7,23.25)*math.pi*11)*math.sin(math.pi*walk)
    w=534
    shadow(im,tx+11,y+2,w-23,9)
    for i in range(3):
        k=e(t,19.61+.15*i,20.19+.15*i)
        sprite(im,'b'+str(i+1),tx+9+103*i-54*(1-k),y-.283*w-44*(1-k),95,(0,1),alpha=k)
    sprite(im,'truck',tx,y,w)
    if walk>0:
        hh=w*assets['truck'].height/assets['truck'].width
        for name,cx in [('rearhub',.211),('fronthub',.784)]:
            sprite(im,name,tx+w*cx,y-hh*(1-.811),w*.104,(.5,.5),angle=-731*walk/(w*.089)*180/math.pi)
    if t>21.62:
        arrow(im,bez((623-camera,277),(740-camera,277),(822-camera,277),(1019-camera,277)),e(t,21.62,22.51),RED,3,15)
    return im
def signature(t):
    im=BG['warm'].copy();head(im,'가상 계약  /  고객 인수')
    text(im,56,171,'고객 인도',61,'bold')
    hpos=l(-189,-33,out(t,23.15,23.66))
    sprite(im,'hand',hpos,565,585)
    for i,(x,y,st) in enumerate([(323,402,23.24),(424,399,23.48),(375,320,23.76)]):
        f=out(t,st,st+.72)
        if f:
            sprite(im,'b'+str(i+1),l(x-80,x,f),l(y-101,y,f)-13*math.sin(math.pi*f),105,(.5,1),angle=l(5,0,f),alpha=f)
    c=out(t,23.34,24.15)
    x=l(1030,741,c);sprite(im,'clip',x,615,374)
    text(im,x+68,249,'인수증',44,'bold')
    text(im,x+75,305,'07.01',23,'mono',BLUE);lin(im,[(x+70,333),(x+292,328)],BLUE,1.8)
    text(im,x+76,367,'완성품',22,'reg')
    text(im,x+290,367,'3상자',27,'bold',INK,'rm')
    text(im,x+82,434,'인수인',17,'reg');lin(im,[(x+143,460),(x+304,455)],'#817965',1.5)
    points=[(0,8),(9,-8),(14,-16),(8,3),(2,15),(19,2),(30,-12),(19,12),(42,-4),(33,7),(51,0),(54,4),(69,-1),(78,-2),(89,-5),(100,-4)]
    frac=e(t,25.5,26.18)
    trans=[(x+147+1.28*a,439+b) for a,b in points]
    n=(len(points)-1)*frac;idx=min(len(points)-2,int(n));p=tuple(l(trans[idx][z],trans[idx+1][z],n-idx) for z in [0,1])
    if frac>0:lin(im,trans[:idx+1]+[p],BLUE,2.6)
    if t>24.78:
        f=out(t,24.78,25.51);leave=e(t,26.2,26.87)
        px,py=p;sprite(im,'pen',px+162*(1-f)+130*leave-4,py-96*(1-f)-85*leave+2,426,(0,1),alpha=min(1,1.6*f))
    return im
@lru_cache(maxsize=1)
def inkmark():
    mark=Image.new('RGBA',(pix(404),pix(116)))
    rect(mark,(7,8,395,105),None,RED,3.6);rect(mark,(13,14,389,99),None,RED,1.3)
    text(mark,201,53,'300,000원',59,'bold',RED,'mm')
    ar=np.array(mark);rng=np.random.default_rng(96)
    speck=rng.uniform(0,1,ar.shape[:2])
    wear=cv2.resize(rng.uniform(0,1,(30,96)).astype('float32'),(ar.shape[1],ar.shape[0]),interpolation=cv2.INTER_CUBIC)
    ar[:,:,3]=(ar[:,:,3]*(.84+.16*wear)*np.where(speck<.055+.055*wear,.19,1)).clip(0,255).astype(np.uint8)
    return Image.fromarray(ar).rotate(2.7,Image.Resampling.BICUBIC,expand=True)
def ledger(t):
    im=BG['linen'].copy()
    # Calendar months sit on the facing pages so the stamped amount belongs to only one month.
    entry=out(t,26.88,27.36);x=139;y=629+(1-entry)*80;w=1002
    sprite(im,'ledger',x,y,w)
    top=y-w*assets['ledger'].height/assets['ledger'].width
    def Y(v):return top+v
    text(im,205,Y(129),'6월',65,'bold')
    text(im,716,Y(129),'7월',65,'bold')
    for a in [206,717]:lin(im,[(a,Y(197)),(a+360,Y(197))],INK,2.6)
    text(im,207,Y(238),'06.30',24,'mono',MUTED);text(im,352,Y(235),'포장 완료',25,'reg')
    text(im,717,Y(238),'07.01',24,'mono',MUTED);text(im,870,Y(235),'고객 인도',25,'reg')
    for j in range(3):
        sprite(im,'b'+str(j+1),718+56*j,Y(347),48)
    text(im,905,Y(327),'× 10만 원',22,'reg')
    text(im,209,Y(373),'이 주문의 매출',20,'reg',MUTED)
    text(im,205,Y(439),'0원',52,'bold','#555851')
    impact=29.55
    if t>=impact:
        mark=inkmark()
        im.paste(mark,(pix(906)-mark.width//2,pix(Y(424))-mark.height//2),mark)
    if 28.85<t<30.19:
        if t<impact:bt=l(-30,Y(433),e(t,28.85,impact))
        else:bt=l(Y(433),-70,e(t,impact+.06,30.19))
        sprite(im,'stamp',908,bt,269,(.5,1),angle=l(-8,0,e(t,29.12,impact)))
    return im
def frame(t):
    f=(factory_scene if t<4.86 else price_scene if t<8.99 else jam if t<15.05 else contract if t<19.58 else departure if t<23.15 else signature if t<26.89 else ledger)
    im=f(t);caption(im,t,f is jam)
    return im
def main():
    if '--qa' in sys.argv:
        times=[.45,2.87,4.31,7.66,9.57,13.62,16.76,18.43,20.83,22.48,24.87,25.88,27.97,29.54,30.88]
        sheet=Image.new('RGB',(5*384,3*216))
        for i,t in enumerate(times):
            im=frame(t);im.resize((1280,720),Image.Resampling.LANCZOS).save(WORK/f'v2-{t:.2f}.jpg',quality=93)
            sheet.paste(im.resize((384,216),Image.Resampling.LANCZOS),(i%5*384,i//5*216))
        sheet.save(WORK/'v2-shot-review.jpg',quality=94)
        return
    target=WORK/'inventory-motion-final.mp4'
    cmd=['ffmpeg','-y','-hide_banner','-loglevel','error','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}','-framerate',str(RATE),'-i','-','-i',str(WORK/'mix-v2.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-preset','veryfast','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-af','loudnorm=I=-14.5:LRA=7:TP=-1.5,aresample=48000','-t','32','-movflags','+faststart','-metadata','title=세 상자의 매출 | 출하 기록',str(target)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for i in range(FRAMES):proc.stdin.write(frame(i/RATE).tobytes())
    proc.stdin.close()
    if proc.wait():raise RuntimeError('Encoding failed')
if __name__=='__main__':main()
