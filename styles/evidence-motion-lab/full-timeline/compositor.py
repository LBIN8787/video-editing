"""Local experimental CPU compositor. Only explicit asset allowlist; never fetch URLs."""
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import io,subprocess,math
from timeline import state
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
class Compositor:
 def __init__(self,doc,assets,size=(1280,720)):
  self.doc,self.assets,self.size=doc,assets,size;self.cache={}
 def media(self,key,t):
  a=self.assets[key]
  if not a.get('available') or a.get('rights')!='verified': raise ValueError('unapproved asset '+key)
  path=Path(a['path']).resolve()
  if not path.is_file(): raise FileNotFoundError(path)
  if a.get('type')=='video':
   raw=subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(path),'-frames:v','1','-f','image2pipe','-vcodec','png','-'])
   return Image.open(io.BytesIO(raw)).convert('RGBA')
  if key not in self.cache:self.cache[key]=Image.open(path).convert('RGBA')
  return self.cache[key].copy()
 def frame(self,t,skin=None):
  w,h=self.size;skin=skin or {};out=Image.new('RGBA',(w,h),skin.get('background','#edf0ed'))
  evaluated=state(self.doc,t,skin)
  for st in evaluated['layers']:
   l=next(x for x in self.doc['layers'] if x['id']==st['id']);p=st['props']
   x,y=p.get('x',l.get('x',.5)),p.get('y',l.get('y',.5));width=int(l.get('width',.4)*w*p.get('scale',1));height=int(l.get('height',.3)*h*p.get('scale',1))
   if width<1 or height<1:continue
   tile=Image.new('RGBA',(width,height),(0,0,0,0));d=ImageDraw.Draw(tile)
   if st['asset']:
    im=self.media(st['asset'],st['media_time']);crop=l.get('crop_box',[0,0,1,1]);c=p.get('crop',0)
    # Animated crop from whole image to explicit normalized focus rectangle.
    box=[(1-c)*v+c*z for v,z in zip([0,0,1,1],crop)]
    im=im.crop((int(box[0]*im.width),int(box[1]*im.height),int(box[2]*im.width),int(box[3]*im.height)))
    if l.get('viewport')=='cover':
     ratio=max(width/im.width,height/im.height);im=im.resize((math.ceil(im.width*ratio),math.ceil(im.height*ratio)),Image.Resampling.LANCZOS)
     # Left/top anchored document view avoids centering text out of the viewport.
     im=im.crop((0,0,width,height));tile.alpha_composite(im)
    else:
     im.thumbnail((width,height),Image.Resampling.LANCZOS);tile.alpha_composite(im,((width-im.width)//2,(height-im.height)//2))
   else:
    fill=l.get('fill',skin.get('card','#ffffff'));radius=int(l.get('radius',14));d.rounded_rectangle((0,0,width-1,height-1),radius=radius,fill=fill)
   if st['text']:
    font=ImageFont.truetype(BOLD if l.get('bold') else FONT,l.get('font_size',26));box=d.textbbox((0,0),st['text'],font=font)
    if box[2]-box[0]>width-24:raise ValueError('text overflow '+l['id'])
    d.text((width/2,height/2),st['text'],font=font,fill=l.get('color','#182329'),anchor='mm')
   if p.get('highlight',0)>0:
    hh=int(height*.08);d.rectangle((0,height-hh,int(width*p['highlight']),height),fill=skin.get('accent','#89c754'))
   if p.get('rotation'):tile=tile.rotate(p['rotation'],Image.Resampling.BICUBIC,expand=True)
   opacity=p.get('opacity',1);tile.putalpha(tile.getchannel('A').point(lambda a:round(a*opacity)))
   out.alpha_composite(tile,(int(x*w-tile.width/2),int(y*h-tile.height/2)))
  return out.convert('RGB')
 def render(self,path,audio=None,fps=30):
  if audio and not Path(audio).is_file():raise FileNotFoundError(audio)
  w,h=self.size;args=['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{w}x{h}','-r',str(fps),'-i','-']
  if audio:args+=['-i',str(audio)]
  args+=['-c:v','libx264','-crf','20','-preset','fast','-pix_fmt','yuv420p']
  if audio:args+=['-c:a','aac','-b:a','128k']
  args+=['-t',str(self.doc['duration']),'-movflags','+faststart',str(path)]
  p=subprocess.Popen(args,stdin=subprocess.PIPE)
  try:
   for f in range(math.ceil(self.doc['duration']*fps)):p.stdin.write(self.frame(f/fps).tobytes())
  finally:p.stdin.close()
  if p.wait():raise RuntimeError('ffmpeg failed')
