"""Make the three review thumbnails and the YouTube handoff sheet from the locked cut."""
import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageOps

from full_direction import FullDirection
from render_full import TITLE
from render_review import W,H,FPS,font


TITLES = [
    (TITLE,'분명 이걸','골랐는데'),
    ('마트 시식대에서, 왜 다른 잼을 내 선택이라고 했을까?','같은 빨간 병','다른 맛'),
    ('왜 ‘쌉쌀해서 골랐다’고 했을까?','내가 고른 게','이거였나?'),
]


def type_lines(im,lines,xy,dark=False):
    d=ImageDraw.Draw(im)
    x,y=xy
    for i,line in enumerate(lines):
        d.text((x,y+97*i),line,font=font(82,True),fill=('#34251c' if dark else '#fff5de') if i==0
               else ('#8d482e' if dark else '#ffd796'))


def thumbnails(edition,out):
    first=edition.plates['point']
    taste=edition.plates['taste']
    a=Image.new('RGB',(W,H),'#232e26')
    leading=first.crop((0,0,928,710))
    a.paste(ImageOps.fit(leading,(704,H),centering=(.35,.43)),(0,0))
    ImageDraw.Draw(a).rectangle((704,0,710,H),fill='#dbc399')
    type_lines(a,TITLES[0][1:],(742,201))

    b=edition.explain.copy()
    edition.jar(b,edition.jars[0],(767,340),385,shadow=False)
    edition.jar(b,edition.jars[0],(1053,344),385,angle=180,shadow=False)
    dark=Image.new('RGB',(602,H),'#27221e')
    b.paste(Image.blend(b.crop((0,0,602,H)),dark,.70),(0,0))
    type_lines(b,TITLES[1][1:],(62,209))

    c=Image.blend(edition.plates['desk'],Image.new('RGB',(W,H),'#f3e0bc'),.78)
    crop=taste.crop((162,17,666,624))
    tile=ImageOps.fit(crop,(610,646),centering=(.47,.46)).convert('RGBA')
    framed=Image.new('RGBA',(tile.width+26,tile.height+26),'#f3e6c9')
    framed.paste(tile,(13,13))
    framed=framed.rotate(-2,Image.Resampling.BICUBIC,expand=True)
    alpha=framed.getchannel('A').filter(ImageFilter.GaussianBlur(9))
    shadow=Image.new('RGBA',framed.size,(65,42,23,0))
    shadow.putalpha(alpha.point(lambda z:z//2))
    c.paste(shadow,(627,34),shadow)
    c.paste(framed,(618,21),framed)
    type_lines(c,TITLES[2][1:],(64,201),dark=True)

    preview=Image.new('RGB',(1200,225))
    for idx,(variant,im) in enumerate(zip('ABC',(a,b,c),strict=True)):
        im.save(out/f'thumbnail_{variant}.png',optimize=True)
        preview.paste(im.resize((400,225),Image.Resampling.LANCZOS),(400*idx,0))
    preview.save(out/'thumbnails.jpg',quality=91)


def description(chapters):
    lines=['마트에서 빨간 잼 병을 가리켰습니다. 같은 병에서 한 숟가락을 더 받았는데, 왜 처음에 피했던 맛이 좋다고 했을까요?',
           '', '스웨덴의 잼 시식 실험에서 시작해, 선택한 카드와 받은 카드가 달라지는 실험, 알아차리고도 바로 말하지 않았을 가능성을 살핀 후속 연구까지 따라갑니다.',
           '', '서윤과 시식대의 대사는 설명을 위한 창작 재구성입니다. 카드와 컴퓨터에 등장하는 사진, 초콜릿 포장은 예시로 제작했습니다.',
           '', '## 챕터', '']
    for row in chapters:
        t=row['start']//FPS
        lines.append(f'{t//60:02d}:{t%60:02d} {row["title"]}')
    lines.extend(['','## 연구 출처','',
      '- Johansson 외 (2005), Science · https://doi.org/10.1126/science.1111709',
      '- Johansson 외 (2006), Consciousness and Cognition · https://doi.org/10.1016/j.concog.2006.09.004',
      '- Hall 외 (2010), Cognition · https://doi.org/10.1016/j.cognition.2010.06.010',
      '- Grassi, Hoeppe, Baytimur & Bartels (2025), Frontiers in Psychology · https://doi.org/10.3389/fpsyg.2025.1598254',
      '- Grassi 외 그림 2B · CC BY 4.0, 논문 그림 일부를 잘라 첫 시행을 강조함. https://creativecommons.org/licenses/by/4.0/',
      '- Somerville과 McGowan (2016), Journal of Behavioral and Experimental Economics · https://doi.org/10.1016/j.socec.2016.01.001',
      '', '#호기심 #인지과학 #심리실험'])
    return '\n'.join(lines)+'\n'


def run(media):
    out=media/'05_edit'
    track=json.loads((media/'full_v2/voice-timeline.json').read_text(encoding='utf8'))
    edition=FullDirection(media/'art',track)
    thumbnails(edition,out)
    opens = [(s['start'],s['chapter']) for i,s in enumerate(track)
             if not i or track[i-1]['chapter']!=s['chapter']]
    chapters=[dict(start=t,title=c) for t,c in opens]
    body=['# 업로드 검토 묶음','','## 제목·썸네일 후보','']
    body.extend(f'- {v} · {title} · 썸네일 문구 “{first} {second}”'
                for v,(title,first,second) in zip('ABC',TITLES,strict=True))
    body += ['','## 더보기 초안','',description(chapters)]
    (out/'youtube.md').write_text('\n'.join(body),encoding='utf8')


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('media',type=Path)
    run(parser.parse_args().media)
