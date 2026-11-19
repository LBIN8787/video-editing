"""Verify captions, source narration, chapter boundaries and rendered image states."""
import argparse
import json
from pathlib import Path
import subprocess

import cv2
import numpy as np
from PIL import Image,ImageDraw

from render_full import captions_and_chapters
from render_review import CAPTION_SIZE,FPS,RATE,W,font

CHECK_FRAMES=(1.1,31.5,46.1,50.0,119,121,131,163,188,283,296,309.2,314.9,348,411,
              431,494,505.6,507.4,512,558,570,575.4,594,638,657,667,692,750.9,768)


def ass_time(seconds):
    cs=round(seconds*100)
    return f'{cs//360000}:{cs//6000%60:02d}:{cs//100%60:02d}.{cs%100:02d}'


def write_ass(timeline,groups,destination):
    lines=('[Script Info]','ScriptType: v4.00+','PlayResX: 1280','PlayResY: 720',
           '[V4+ Styles]',
           'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, '
           'Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, '
           'Shadow, Alignment, MarginL, MarginR, MarginV, Encoding',
           f'Style: Default,NanumGothic,{CAPTION_SIZE},&H00DFF5FF,&H00FFFFFF,&H00212524,&H00212524,'
           '-1,0,0,0,100,100,0,0,3,2,0,2,30,30,34,1',
           '[Events]','Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text')
    ass=list(lines)
    for shot,rows in zip(timeline,groups,strict=True):
        t=shot['start']/FPS
        ass.extend(f'Dialogue: 0,{ass_time(t+a)},{ass_time(t+b)},Default,,0,0,0,,{line}'
                   for a,b,line in rows)
    destination.write_text('\n'.join(ass)+'\n',encoding='utf8')


def verify(media,edition='final_direction_v3'):
    out=media/'05_edit'
    final=out/(edition+'.mp4')
    voice=media/'full_v2'
    track=json.loads((voice/'voice-timeline.json').read_text(encoding='utf8'))
    groups,chapters,_=captions_and_chapters(track)
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams',
        '-show_chapters','-of','json',str(final)]))
    video,audio=probe['streams'][:2]
    assert video['codec_name']=='h264' and audio['codec_name']=='aac'
    assert len(probe['chapters'])==len(chapters)
    for actual,expected in zip(probe['chapters'],chapters,strict=True):
        assert abs(float(actual['start_time'])-expected['start']/FPS)<.002
        assert actual['tags']['title']==expected['title']
    frames=chapters[-1]['end']
    difference=float(video['duration'])-float(audio['duration'])
    assert int(video['nb_frames'])==frames and abs(difference)<.05
    pcm=np.fromfile(voice/'master.pcm',dtype='<i2')
    decoded=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(final),
       '-map','0:a:0','-f','s16le','-ar',str(RATE),'-']),dtype='<i2')
    assert len(decoded)>=len(pcm)==frames*RATE//FPS

    capture=cv2.VideoCapture(str(final))
    caption_pixels=[]
    correlations=[]
    offsets=[]
    for shot,rows in zip(track,groups,strict=True):
        audio_start=shot['start']*RATE//FPS
        audio_end=audio_start+shot['frames']*RATE//FPS
        correlations.append(float(np.corrcoef(decoded[audio_start:audio_end],pcm[audio_start:audio_end])[0,1]))
        for a,b,txt in rows:
            assert b>a and font(CAPTION_SIZE,True).getlength(txt)<W-55
            sample=shot['start']+round((a+b)/2*FPS)
            capture.set(cv2.CAP_PROP_POS_FRAMES,sample)
            ok,f=capture.read()
            assert ok,sample
            mask=Image.new('L',(W,60))
            ImageDraw.Draw(mask).text((W/2,29),txt,font=font(CAPTION_SIZE,True),fill=255,anchor='mm')
            glyph=np.asarray(mask)>210
            gray=cv2.cvtColor(f[626:686],cv2.COLOR_BGR2GRAY)
            caption_pixels.append(float((gray[glyph]>170).mean()))
            # Find the transferred narration excerpt in the encoded PCM at its expected time.
            start=audio_start+round(a*RATE)
            reference=pcm[start:start+6000].astype(np.float32)
            window=max(0,start-2400)
            search=decoded[window:start+8400].astype(np.float32)
            match=cv2.matchTemplate(search[None,:],reference[None,:],cv2.TM_CCOEFF_NORMED)[0]
            best=int(np.argmax(match))
            assert match[best]>.90, (txt,float(match[best]))
            offsets.append(abs(window+best-start)/RATE)
    assert min(caption_pixels)>.95 and min(correlations)>.99 and max(offsets)<.05
    write_ass(track,groups,out/(edition+'.ass'))
    for sheet_no,start in enumerate(range(0,len(CHECK_FRAMES),12),1):
        selected=CHECK_FRAMES[start:start+12]
        sheet=Image.new('RGB',(1200,((len(selected)+2)//3)*242),'#201d18')
        for i,t in enumerate(selected):
            capture.set(cv2.CAP_PROP_POS_MSEC,t*1000)
            ok,frame=capture.read()
            assert ok,t
            rgb=cv2.cvtColor(cv2.resize(frame,(400,225),interpolation=cv2.INTER_AREA),cv2.COLOR_BGR2RGB)
            x,y=(i%3)*400,(i//3)*242
            sheet.paste(Image.fromarray(rgb),(x,y))
            ImageDraw.Draw(sheet).text((x+4,y+226),f'{int(t)//60:02d}:{t%60:04.1f}',fill='white')
        sheet.save(out/f'{edition}_frames_{sheet_no}.jpg',quality=93)
    capture.release()
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(final),'-map','0:v:0','-map','0:a:0',
                    '-f','null','-'],check=True)
    data=dict(duration_s=frames/FPS,frames=frames,chapters=len(chapters),captions=len(caption_pixels),
              min_caption_pixels=round(min(caption_pixels),4),max_audio_transfer_offset_s=max(offsets),
              video_minus_audio_s=difference,min_audio_correlation=round(min(correlations),5),
              full_decode='pass')
    (out/(edition+'.qa.json')).write_text(json.dumps(data,indent=2),encoding='utf8')
    print(data,flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('media',type=Path)
    parser.add_argument('--edition',default='final_direction_v3')
    args=parser.parse_args()
    verify(args.media,args.edition)
