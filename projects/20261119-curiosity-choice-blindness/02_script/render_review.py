"""Render the approved v2 scene and apparatus reveal on the review voice clock."""
import argparse
from functools import lru_cache
import json
import math
from pathlib import Path
import re
import subprocess

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

from review_voice import RATE, FPS

W,H = 1280,720
PARCHMENT = '#f1dfbc'
INK = '#2b241b'
FONT_DIR = Path(__file__).resolve().parents[3] / 'ytflow/assets/fonts'
CAPTION_SIZE = 33


@lru_cache(None)
def font(size,bold=False,role='sans'):
    filename={
        'sans': 'NanumGothic-Bold.ttf' if bold else 'NanumGothic-Regular.ttf',
        'serif': 'NanumMyeongjo-ExtraBold.ttf' if bold else 'NanumMyeongjo-Bold.ttf',
        'pen': 'NanumPenScript-Regular.ttf',
    }[role]
    return ImageFont.truetype(str(FONT_DIR/filename),size)


def ease(t):
    t = max(0,min(t,1))
    return t*t*(3-2*t)


def sprite(sheet,index):
    width = sheet.width//2
    part = sheet.crop((index*width,0,(index+1)*width,sheet.height))
    channel = part.getchannel('A')
    box = channel.point(lambda n: 255 if n>=192 else 0).getbbox()
    # The solid jar defines the bounds. Ignore scattered translucent edge pixels outside it.
    return part.crop(box)


def label(im,xy,txt,night=False):
    draw=ImageDraw.Draw(im)
    f=font(20,True) if night else font(31,role='pen')
    w=math.ceil(f.getlength(txt))+34
    x,y=xy
    draw.rectangle((x,y,x+w,y+37),fill='#29251f' if night else PARCHMENT)
    draw.text((x+17,y+18),txt,font=f,fill=PARCHMENT if night else INK,anchor='lm')


def normalized(word):
    return re.sub(r'[^\w]','',word)


def captions(edit):
    spoken=edit['text'].split()
    words=iter(edit['words'])
    timed=[]
    for source in spoken:
        first=last=next(words)
        actual=normalized(first['text'])
        expected=normalized(source)
        while actual!=expected and expected.startswith(actual):
            last=next(words)
            actual+=normalized(last['text'])
        assert actual==expected,(edit['shot'],source,actual)
        timed.append((first['offset']/1e7,(last['offset']+last['duration'])/1e7,source))
    assert next(words,None) is None,edit['shot']
    groups=[]
    current=[]
    for a,b,text in timed:
        if current and (font(CAPTION_SIZE,True).getlength(' '.join(x[2] for x in current)+' '+text)>1050
                        or a-current[-1][1]>.5):
            groups.append(current)
            current=[]
        current.append((a,b,text))
        if re.search(r'[.!?,][”"]?$',text):
            groups.append(current)
            current=[]
    if current:
        groups.append(current)
    return [(g[0][0],min(g[-1][1]+.21,groups[i+1][0][0] if i+1<len(groups) else edit['frames']/FPS),
             ' '.join(w[2] for w in g)) for i,g in enumerate(groups)]


def caption(im,rows,t):
    for a,b,text in rows:
        if a<=t<b:
            draw=ImageDraw.Draw(im)
            f=font(CAPTION_SIZE,True)
            half=draw.textlength(text,font=f)/2
            x=round(W/2-half-18)
            pad=Image.new('RGBA',(round(half*2)+36,50),(29,30,27,223))
            im.paste(pad,(x,631),pad)
            draw.text((W/2,655),text,font=f,fill='#fff5df',anchor='mm')
            break


class Cut:
    def __init__(self,art):
        grid=Image.open(art/'tasting.png').convert('RGB')
        w,h=grid.width//2, grid.height//2
        self.plates={}
        for i,key in enumerate(('point','taste','desk','finish')):
            x,y=i%2*w,i//2*h
            # Inset past the contact-sheet rules. No animated camera transform.
            sub=grid.crop((x+2,y+2,x+w-2,y+h-2))
            self.plates[key]=ImageOps.fit(sub,(W,H),method=Image.Resampling.LANCZOS)
        jj=Image.open(art/'jars.png').convert('RGBA')
        self.jars=[sprite(jj,i) for i in (0,1)]
        raw=np.asarray(self.jars[0]).copy()
        yy=np.indices(raw.shape[:2])[0]/raw.shape[0]
        strip=(yy>.32)&(yy<.71)&(raw[:,:,0].astype(float)>1.35*raw[:,:,1])
        raw[strip,:3]=np.clip(raw[strip,:3]*np.array([.48,1.03,1.57])+[12,17,20],0,255).astype('uint8')
        self.blue=Image.fromarray(raw).transpose(Image.Transpose.ROTATE_180)
        self.shadow=Image.new('RGBA',(300,82))
        d=ImageDraw.Draw(self.shadow)
        d.ellipse((32,22,268,68),fill=(26,17,11,168))
        self.shadow=self.shadow.filter(ImageFilter.GaussianBlur(14))
        desk=self.plates['desk']
        surround=Image.new('RGB',(W,H),'#26221f')
        self.explain=Image.blend(desk,surround,.78)
        stock=desk.crop((390,159,1090,675)).resize((W,H),Image.Resampling.LANCZOS)
        self.paper=Image.blend(Image.new('RGB',(W,H),'#f3e9d4'),stock,.105)

    @lru_cache(maxsize=6)
    def spread_plate(self,key):
        return ImageOps.fit(self.plates[key],(566,319),method=Image.Resampling.LANCZOS)

    def spread_story(self,left,right,heading,names,second):
        im=self.paper.copy()
        d=ImageDraw.Draw(im)
        d.text((61,62),heading,font=font(54,True,'serif'),fill='#372b23',stroke_width=0)
        d.line((61,148,1218,148),fill='#ab775b',width=2)
        for shown,key,x,tag in ((True,left,61,names[0]),(second,right,652,names[1])):
            if shown:
                d.text((x,174),tag,font=font(35,role='pen'),fill='#794232')
                d.rectangle((x-1,219,x+567,540),outline='#765e47',width=2)
                im.paste(self.spread_plate(key),(x,220))
        return im

    @lru_cache(maxsize=12)
    def focus(self,key,x,y):
        # Hold the camera. Light on the important jar is separate from the shelf background.
        im=self.plates[key]
        xx,yy=np.meshgrid(np.arange(W),np.arange(H))
        weights=.62+.38*np.exp(-(((xx-x)/310)**2+((yy-y)/250)**2))
        return Image.fromarray((np.asarray(im)*weights[:,:,None]).astype(np.uint8))

    def shopper(self,name,t):
        if name=='choose':
            im=self.plates['point'].copy()
            label(im,(28,24),'시식 상황 재구성',True)
        elif name=='turn_to_taste':
            if t<4.65:
                im=self.plates['point'].copy()
            elif t<11.22:
                x=694 if t<7.43 else 882
                im=self.focus('point',x,561).copy()
            else:
                im=self.plates['taste'].copy()
        elif name=='ask':
            im=self.plates['taste'].copy()
        elif name=='hesitate':
            im=self.plates['taste' if t<3.07 else 'finish'].copy()
        elif t<6.83:
            im=self.focus('point',883,550).copy()
        else:
            im=self.spread_story('point','taste','같은 빨간 병',('고를 때','다시 맛볼 때'),t>=8.37)
        return im

    def jar(self,im,sprite,center,height,angle=0,lift=0,shadow=True):
        x,y=center
        w=round(sprite.width*height/sprite.height)
        obj=sprite.resize((w,height),Image.Resampling.LANCZOS)
        if shadow:
            sh=self.shadow
            im.paste(sh,(round(x-sh.width/2),round(y+height/2-41+lift)),sh)
        if angle:
            obj=obj.rotate(angle,Image.Resampling.BICUBIC,expand=True)
        im.paste(obj,(round(x-obj.width/2),round(y-obj.height/2)),obj)

    def ingredient(self,im,text,x,y,target_x,target_y):
        draw=ImageDraw.Draw(im)
        draw.line((target_x,target_y,x-43,y),fill='#d8ba87',width=2)
        draw.ellipse((target_x-3,target_y-3,target_x+3,target_y+3),fill=PARCHMENT)
        draw.text((x,y),text,font=font(32,True,'serif'),fill=PARCHMENT,anchor='lm')

    def reveal(self,t):
        if t<3.07:
            return self.plates['taste'].copy()
        if t<11.4:
            im=self.plates['desk'].copy()
            slide=1-ease((t-3.07)/.75)
            self.jar(im,self.jars[0],(764+130*slide,350-37*slide),347)
            label(im,(34,27),'마트 실험 재구성  ·  Hall 외 (2010)',True)
            if t>=8.48:
                self.ingredient(im,'두 번째 뚜껑',1008,568,836,518)
            return im
        im=self.explain.copy()
        jar=self.jars[int(t>=15.78)]
        self.jar(im,jar,(610,334),380,shadow=False)
        label(im,(34,27),'두 칸으로 나뉜 실험용 병',True)
        if t>=17.65:
            self.ingredient(im,'계피 사과 잼',869,238,740,238)
        if t>=19.2:
            self.ingredient(im,'자몽 잼',869,430,740,430)
        if t>=21.73:
            self.ingredient(im,'두 칸을 나누는 막',866,336,740,336)
        return im

    def flip(self,t):
        if t<3.9:
            return self.plates['taste'].copy()
        if t<9.48:
            im=self.plates['desk'].copy()
            self.jar(im,self.jars[0],(788,331),330)
            label(im,(34,27),'마트 실험 재구성  ·  Hall 외 (2010)',True)
            return im
        im=self.explain.copy()
        turn=ease((t-11.05)/1.34)
        second=ease((t-17.28)/1.38)
        jar=self.jars[int(turn>=1)]
        self.jar(im,jar,(568,325),350,180*turn,shadow=False)
        if t>=16.92:
            entry=1-ease((t-16.92)/.35)
            self.jar(im,self.blue,(934+340*entry,335),292,
                     180*second,shadow=False)
        if 13.55<=t<16.92:
            self.ingredient(im,'위로 온 자몽 잼',866,237,690,237)
            self.ingredient(im,'아래로 간 사과 잼',866,414,691,414)
        label(im,(34,27),'병을 돌리면 어느 맛이 위로 올까',True)
        return im

    def frame(self,shot,t):
        if shot=='section':
            return self.reveal(t)
        if shot=='flip':
            return self.flip(t)
        if shot=='return':
            return self.plates['point' if t<7.25 else 'taste'].copy()
        return self.shopper(shot,t)


def run(media):
    clock=json.loads((media/'review_voice/voice-timeline.json').read_text(encoding='utf8'))
    audio=media/'review_voice/review.pcm'
    out=media/'05_edit'
    out.mkdir(exist_ok=True)
    tmp=out/'sample_v2.pending.mp4'
    cut=Cut(media/'art')
    chapters=[';FFMETADATA1','title=내가 고르지 않은 잼을 왜 골랐다고 했을까? · 화면 검토본']
    split=next(s['start'] for s in clock if s['shot']=='section')
    total=sum(s['frames'] for s in clock)
    for a,b,name in ((0,split,'손님 쪽에서 본 시식대'),(split,total,'시식대 뒤편과 병의 단면')):
        chapters.extend(('[CHAPTER]','TIMEBASE=1/24',f'START={a}',f'END={b}',f'title={name}'))
    meta=media/'review_voice/chapters.ffmeta'
    meta.write_text('\n'.join(chapters)+'\n',encoding='utf8')
    cmd=['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-r',str(FPS),'-s',f'{W}x{H}',
         '-i','pipe:0','-f','s16le','-ar',str(RATE),'-ac','1','-i',str(audio),'-f','ffmetadata','-i',str(meta),
         '-map','0:v:0','-map','1:a:0','-map_metadata','2','-map_chapters','2','-af','volume=3dB,alimiter=limit=0.94:latency=1',
         '-c:v','libx264','-preset','veryfast','-crf','16','-pix_fmt','yuv420p',
         '-c:a','aac','-b:a','128k','-movflags','+faststart',str(tmp)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    timing={}
    try:
        for scene in clock:
            shot=scene['shot']
            rows=captions(scene)
            for i in range(scene['frames']):
                t=i/FPS
                im=cut.frame(shot,t)
                caption(im,rows,t)
                proc.stdin.write(im.tobytes())
            timing[shot]=dict(start=scene['start']/FPS,duration=scene['frames']/FPS,caption_count=len(rows))
            print(shot,flush=True)
        proc.stdin.close()
        if proc.wait()!=0:
            raise RuntimeError('Review encode failed')
    finally:
        if proc.poll() is None:
            proc.kill()
            proc.wait()
    tmp.replace(out/'sample_v2.mp4')
    (out/'sample_v2.timeline.json').write_text(json.dumps(timing,ensure_ascii=False,indent=2),encoding='utf8')
    print(f'{total} frames, {total/FPS:.2f} seconds')


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('media',type=Path)
    run(parser.parse_args().media)
