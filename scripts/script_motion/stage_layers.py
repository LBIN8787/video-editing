"""Composite a fixed camera and authored object tracks, sampled on the delivery time base."""
from bisect import bisect_right
from functools import lru_cache
from PIL import Image, ImageOps

@lru_cache(maxsize=50)
def asset(path):
    with Image.open(path) as image:
        return image.convert("RGBA")

def pose(keys,frame):
    i=bisect_right([k[0] for k in keys],frame)-1
    if i<0: return None
    a=keys[i]
    if i==len(keys)-1: return a[1:]
    b=keys[i+1]
    t=(frame-a[0])/(b[0]-a[0])
    t=t*t*(3-2*t)
    return [u+(v-u)*t for u,v in zip(a[1:],b[1:])]

def frames(folder,shot,end):
    stage=shot["composition"]
    layers=stage["layers"]
    count=end-shot["at"]
    ticks={0}
    for layer in layers:
        keys=layer["keys"]
        if not keys or [k[0] for k in keys]!=sorted(set(k[0] for k in keys)):
            raise ValueError("Layer keys must be ordered and unique")
        for i,k in enumerate(keys):
            ticks.add(k[0])
            if i and k[1:]!=keys[i-1][1:]:
                ticks.update(range(keys[i-1][0]+2,min(count,k[0]),2))
    bg=ImageOps.fit(asset(folder/stage["back"]).convert("RGB"),(1280,720),Image.Resampling.LANCZOS)
    for tick in sorted(n for n in ticks if 0<=n<count):
        im=bg.copy()
        for layer in layers:
            state=pose(layer["keys"],tick)
            if state is None: continue
            x,y,opacity,angle=state
            if opacity<=0: continue
            obj=asset(folder/layer["file"])
            if angle:
                obj=obj.rotate(angle,Image.Resampling.BICUBIC,expand=True)
            if opacity<1:
                obj=obj.copy()
                obj.putalpha(obj.getchannel("A").point(lambda v:round(v*opacity)))
            im.paste(obj,(round(x-obj.width/2),round(y-obj.height/2)),obj)
        yield shot["at"]+tick,im
