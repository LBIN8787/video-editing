"""Word-cued direction for the v2 choice-blindness episode."""
from bisect import bisect_right
from functools import lru_cache
import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps

from render_review import Cut, W,H,font,ease,label,normalized

CUTS = {
    'cards_lab': ('lab','card_desk','cards_portrait','handoff'),
    'computer': ('monitor','eye','forms','key'),
    'chocolate': ('chocolate_pick','chocolate_table','chocolate_offer','chocolate_unwrap'),
}
SHOP = {'choose','turn_to_taste','ask','hesitate','question','section','flip'}
CREAM = '#ecdbb9'
DARK = '#27241e'
SOURCES = {
    'science_2005': ('Johansson 외 (2005)','Science · 얼굴 카드 실험','10.1126/science.1111709'),
    'analysis_2006': ('Johansson 외 (2006)','바뀐 카드와 그대로인 카드에 대한 설명','10.1016/j.concog.2006.09.004'),
    'science_2010': ('Hall 외 (2010)','스웨덴 룬드의 슈퍼마켓','10.1016/j.cognition.2010.06.010'),
    'science_2025': ('Grassi 외 (2025)','컴퓨터 사진 선택과 동공 반응','10.3389/fpsyg.2025.1598254'),
    'science_2016': ('Somerville과 McGowan (2016)','익숙한 초콜릿을 고르는 실험','10.1016/j.socec.2016.01.001'),
}
NOTES = {
    'report_13': ('카드를 바꾼 시행','그 자리에서 알아차림   46 / 354','Johansson 외 (2005) · 같은 사람도 여러 차례 참여'),
    'report_time': ('사진을 고를 시간','자유롭게 봤을 때 더 잘 알아챘다','Johansson 외 (2005)'),
    'term': ('선택 맹목','내가 고른 것과 받은 것의 차이를 놓치는 현상','Johansson 외 (2005)'),
    'detect_count': ('바꿔 준 잼만 비교','탐지로 분류된 경우는 약 세 번에 한 번','Hall 외 (2010) · 그 자리·나중의 보고와 맛의 변화 포함'),
    'report_now': ('그 자리에서','숟가락을 내려놓고 바뀌었다고 말한 경우','Hall 외 (2010) · 반응 분류 재구성'),
    'report_later': ('시식을 마친 뒤','아까 이상한 점이 있었다고 답한 경우','Hall 외 (2010) · 반응 분류 재구성'),
    'report_taste': ('맛을 다시 설명할 때','교체는 언급하지 않았지만 맛이 변했다고 한 경우','Hall 외 (2010) · 반응 분류 재구성'),
    'paper_note': ('실험 후 응답','입력을 잘못했거나, 실험의 일부라고 생각했다','Grassi 외 (2025) · 응답 요약'),
    'compare_bounds': ('서로 다른 실험','처음 맛본 잼과 익숙한 초콜릿','제품·참가자·실험 조건이 함께 달랐다'),
}
SOURCE_BACK = {'science_2005':'card_desk','analysis_2006':'card_desk','science_2010':'desk',
               'science_2025':'forms','science_2016':'chocolate_table'}
NOTE_BACK = {'report_13':'card_desk','report_time':'card_desk','term':'card_desk',
             'detect_count':'desk','report_now':'finish','report_later':'desk','report_taste':'taste',
             'paper_note':'forms','compare_bounds':'chocolate_table'}


def regions(path):
    sheet=Image.open(path).convert('RGB')
    w,h=sheet.width//2,sheet.height//2
    return [sheet.crop((x+3,y+3,x+w-3,y+h-3)) for y in (0,h) for x in (0,w)]


def cues(scene, expression):
    words=[normalized(word['text']) for word in scene['words']]
    text=''.join(words)
    times=[word['offset']/1e7 for word,token in zip(scene['words'],words)
           for _ in token]
    first,*changes=expression.split('|')
    rows=[(0,first)]
    cursor=0
    for change in changes:
        phrase,key=change.rsplit(' ',1)
        token=normalized(phrase)
        pos=text.find(token,cursor)
        if pos<0: raise ValueError((scene['shot'],phrase,text[cursor:]))
        rows.append((times[pos],key))
        cursor=pos+len(token)
    return rows


def centered(im,content,mid,ya=(0,0)):
    im.paste(content,(round(mid[0]-content.width/2+ya[0]),round(mid[1]-content.height/2+ya[1])),
             content if content.mode=='RGBA' else None)


class FullDirection(Cut):
    def __init__(self,art,timeline):
        super().__init__(art)
        for stem,labels in CUTS.items():
            for key,im in zip(labels,regions(art/(stem+'.png')),strict=True):
                self.plates[key]=ImageOps.fit(im,(W,H),method=Image.Resampling.LANCZOS)
        self.photos=regions(art/'cards_assets.png')
        paper_page=Image.open(art/'grassi_p7.png').convert('RGB')
        self.fig=paper_page.crop((123,1020,411,1287))
        raw=json.loads(Path(__file__).with_name('full_cues.json').read_text(encoding='utf8'))
        self.actions={s['shot']:cues(s,raw[s['shot']]) for s in timeline if s['shot'] not in SHOP}
        self.attach_context=Image.new('RGB',(W,H),'#191e1a')
        self.screen_region=np.float32([(703,145),(1167,137),(1168,436),(703,436)])
        self.card_bg=Image.blend(self.plates['card_desk'],Image.new('RGB',(W,H),'#392d22'),.17)

    @lru_cache(maxsize=48)
    def printed(self,index,wh=(265,313)):
        w,h=wh
        photo=ImageOps.fit(self.photos[index],(w-26,h-62),method=Image.Resampling.LANCZOS)
        plate=Image.new('RGBA',wh,CREAM)
        plate.paste(photo,(13,13))
        ImageDraw.Draw(plate).line((16,h-38,w-16,h-38),fill='#bfae91',width=1)
        return plate

    def card(self,im,index,mid,angle=0):
        print_image=self.printed(index)
        if angle: print_image=print_image.rotate(angle,Image.Resampling.BICUBIC,expand=True)
        shadow=self.shadow
        centered(im,shadow,(mid[0],mid[1]+print_image.height/2-18))
        centered(im,print_image,mid)

    def cards(self,key,t):
        im=self.card_bg.copy()
        label(im,(34,26),'2005년 카드 실험 재구성  ·  예시 사진',True)
        if key=='cards_pair':
            progress=ease(t/.48)
            self.card(im,0,(371-120*(1-progress),344),angle=3)
            self.card(im,1,(749+110*(1-progress),344),angle=-3)
        elif key=='cards_choose':
            self.card(im,0,(371,344),angle=3)
            self.card(im,1,(749,344),angle=-3)
            label(im,(262,520),'참가자가 고른 쪽')
        elif key=='cards_flip':
            self.card(im,1,(612,338))
            label(im,(526,511),'건네받은 사진')
        else:
            self.card(im,0,(371,344),angle=3)
            self.card(im,1,(749,344),angle=-3)
            label(im,(268,522),'처음 고른 사진')
            label(im,(645,522),'나중에 받은 사진')
        return im

    @lru_cache(maxsize=8)
    def screen(self,key):
        im=self.plates['monitor'].copy()
        glass=Image.new('RGB',(465,302),'#252822')
        d=ImageDraw.Draw(glass)
        if key in ('screen_pair','screen_selected'):
            for j in range(2):
                pic=ImageOps.fit(self.photos[j+2],(205,130))
                glass.paste(pic,(19+j*224,83))
            if key=='screen_selected':
                d.rectangle((15,79,227,217),outline='#e1bd7b',width=4)
                d.text((121,236),'처음 고른 사진',font=font(19,True),fill='#efd5a3',anchor='mt')
        else:
            pic=ImageOps.fit(self.photos[3],(336,208))
            glass.paste(pic,(65,47))
            d.rectangle((63,44,403,258),outline='#c6b37b',width=2)
        src=np.float32([(0,0),(464,0),(464,301),(0,301)])
        tx=cv2.getPerspectiveTransform(src,self.screen_region)
        warp=cv2.warpPerspective(np.asarray(glass),tx,(W,H))
        mask=cv2.warpPerspective(np.full((302,465),255,dtype=np.uint8),tx,(W,H))
        im.paste(Image.fromarray(warp),(0,0),Image.fromarray(mask))
        label(im,(35,26),'컴퓨터 실험 재구성  ·  예시 사진',True)
        return im

    @lru_cache(maxsize=12)
    def document(self,key):
        source=key in SOURCES
        base=(SOURCE_BACK if source else NOTE_BACK)[key]
        who,main,foot=(SOURCES if source else NOTES)[key]
        actor=base in ('taste','finish')
        background=self.plates[base]
        im=Image.blend(background,self.attach_context,.64 if actor else .36)
        mt=Image.new('RGB',(960,313),CREAM)
        surface=background.crop((265,212,535,329)).resize(mt.size)
        mt=Image.blend(mt,surface,.09)
        d=ImageDraw.Draw(mt)
        d.text((55,45),who,fill='#794534',font=font(34,role='pen'))
        d.line((54,99,900,99),fill='#b9a183',width=2)
        f=font(37,True,'serif')
        assert f.getlength(main)<850,key
        d.text((54,138),main,font=f,fill=DARK)
        d.text((54,240),foot,font=font(22),fill='#675945')
        sticker=mt.convert('RGBA').rotate(-1.6,Image.Resampling.BICUBIC,expand=True)
        fs=sticker.getchannel('A').filter(ImageFilter.GaussianBlur(12))
        sd=Image.new('RGBA',sticker.size,(43,28,19,0))
        sd.putalpha(fs.point(lambda n:n//3))
        centered(im,sd,(638,341))
        centered(im,sticker,(636,320))
        return im

    def result(self,key):
        # Fig. 2B from the CC BY publisher PDF, with only its first trial highlighted.
        im=Image.blend(self.plates['forms'],self.attach_context,.45)
        panel=self.fig.resize((365,352),Image.Resampling.LANCZOS)
        im.paste(panel,(754,174))
        d=ImageDraw.Draw(im)
        d.rounded_rectangle((859,226,902,395),radius=4,outline='#80553b',width=3)
        label(im,(33,26),'첫 교체만 보기  ·  Grassi 외 (2025) 그림 2B',True)
        d.rounded_rectangle((159,182,691,525),radius=5,fill=CREAM)
        d.text((205,227),'같은 사진이 바뀐 첫 차례',font=font(33,True,'serif'),fill=DARK)
        if key!='original_intro':
            d.text((205,307),'그 자리에서 알림',font=font(35,role='pen'),fill='#694838')
            d.text((623,305),'10명',font=font(40,True,'serif'),fill='#813d30',anchor='ra')
        if key=='original_second':
            d.text((205,397),'나중에 찾아냄',font=font(35,role='pen'),fill='#3c5850')
            d.text((623,394),'31명',font=font(40,True,'serif'),fill='#2c625b',anchor='ra')
        d.text((205,473),'실험 1 참가자 41명',font=font(21),fill='#624d36')
        return im

    def jar_views(self,key,t):
        im=self.explain.copy()
        # Compare stable color tags with contents instead of using a dashboard.
        first=key in ('control','control_compare')
        end=ease(t/.72)
        self.jar(im,self.jars[0 if first else 1],(386,325),318,shadow=False)
        if key!='control':
            target=self.jars[0] if first else self.jars[1]
            self.jar(im,target,(868+150*(1-end),325),318,angle=180,shadow=False)
        label(im,(35,26),'마트 실험 재구성  ·  Hall 외 (2010)',True)
        label(im,(273,514),'그대로 둔 빨간 병' if first else '처음 · 계피 사과')
        if key!='control':
            label(im,(766,514),'뒤집은 빨간 병' if first else '다시 · 위로 온 자몽')
        return im

    def split(self,left,right):
        im=Image.new('RGB',(W,H),CREAM)
        im.paste(ImageOps.fit(self.plates[left],(632,H),centering=(.31,.40)),(0,0))
        im.paste(ImageOps.fit(self.plates[right],(640,H),centering=(.36,.40)),(640,0))
        return im

    def picture(self,key,t):
        if key.startswith('cards_') and key not in self.plates:
            return self.cards(key,t)
        if key.startswith('screen_'):
            return self.screen(key).copy()
        if key in SOURCES or key in NOTES:
            return self.document(key).copy()
        if key.startswith('original_'):
            return self.result(key)
        if key in ('control','control_compare','two_jams'):
            return self.jar_views(key,t)
        if key in ('focus_red','focus_blue'):
            return self.focus('point',694 if key=='focus_red' else 882,552).copy()
        if key=='fork':
            return self.spread_story('taste','finish','잠깐의 망설임',('맛이 달랐나','바뀌었다고 말할까'),True)
        if key=='eye_compare':
            return self.split('eye','forms')
        if key=='closing_question':
            return self.spread_story('point','finish','선택과 대답 사이',('처음 고른 것','나중에 한 말'),True)
        if key=='final_hold':
            return self.plates['finish'].copy()
        if key=='chocolate_wrap':
            key='chocolate_pick'
        if key.startswith('paper_'):
            im=self.plates['forms'].copy()
            if key=='paper_recall':
                for i,x in enumerate((375,676)):
                    card=ImageOps.fit(self.photos[2+i],(208,132))
                    im.paste(card,(x,x//50+297))
            return im
        return self.acting(key)

    def acting(self,key):
        im=self.plates[key].copy()
        if key in ('lab','handoff','cards_portrait'):
            label(im,(35,26),'얼굴 카드 실험 재구성',True)
        elif key.startswith('chocolate_'):
            label(im,(35,26),'초콜릿 실험 재구성',True)
        return im

    def frame(self,shot,t):
        if shot in SHOP:
            return super().frame(shot,t)
        timeline=self.actions[shot]
        i=bisect_right([at for at,key in timeline],t)-1
        at,key=timeline[i]
        local=t-at
        if local>=2.3:
            return self.steady(key).copy()
        return self.picture(key,local)

    @lru_cache(maxsize=24)
    def steady(self,key):
        return self.picture(key,2.3)
