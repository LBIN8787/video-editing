"""Conform the approved v6 picture to actual speech without changing dialogue speed."""
import argparse
from difflib import SequenceMatcher
import json
from pathlib import Path
import re
import subprocess
import wave

import cv2
import numpy as np

from render_full import srt_at

FPS = 24
OPENING = 776


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def norm(text):
    return ''.join(char.lower() for char in text if char.isalnum())


def char_span(token, a, b):
    return list(zip(np.linspace(a, b, len(token)+1)[:-1],
                    np.linspace(a, b, len(token)+1)[1:]))


def clocks(media, work):
    scenes = read(media/'full_v2/voice-timeline.json')
    body = scenes[next(i for i,s in enumerate(scenes) if s['shot']=='question'):]
    offset = (body[0]['start']-OPENING)/FPS
    old_end = (body[-1]['start']+body[-1]['frames'])/FPS-offset
    source_chars, source_times = [], []
    for scene in body:
        base = scene['start']/FPS-offset
        for w in scene['words']:
            token = norm(w['text'])
            source_chars.extend(token)
            a = base + w['offset']/1e7
            source_times.extend(char_span(token, a, a+w['duration']/1e7))
    source = ''.join(source_chars)
    mix = {r['take']: r for r in read(work/'mix.json')}
    with wave.open(str(work/'mix.wav'), 'rb') as audio:
        samples = np.frombuffer(audio.readframes(audio.getnframes()), '<i2')
        rate = audio.getframerate()
    end = len(samples)/rate
    old, new = [OPENING/FPS], [OPENING/FPS]
    pos = 0
    matches = {}
    for take in read(work/'takes.json'):
        part = ''.join(norm(row['text']) for row in take['parts'])
        assert source[pos:pos+len(part)] == part, take['id']
        timing = mix[take['id']]
        base = timing['start'] - timing['source_in']
        lo, hi = timing['start'], base + timing['source_out']
        heard, heard_times = [], []
        for word in read(work/(take['id']+'.words.json')):
            token = norm(word['w'])
            a,b = np.clip([base+word['s'],base+word['e']],lo,hi)
            if b>a+.13:
                # ASR can include the silence before a word. Remove leading quiet frames.
                step = rate//100
                buf = samples[round(a*rate):round(b*rate)].astype(float)
                blocks = buf[:len(buf)//step*step].reshape(-1,step)
                activity = np.sqrt(np.mean(blocks**2,axis=1))
                voiced = np.flatnonzero(activity>max(90, activity.max()*.047))
                if voiced.size and voiced[0]>=5:
                    a += (voiced[0]-2)*.01
            heard.extend(token)
            heard_times.extend(char_span(token,a,b))
        align = SequenceMatcher(None, part, ''.join(heard), autojunk=False)
        matches[take['id']] = round(align.ratio(),4)
        assert align.ratio()>.89, (take['id'],align.ratio())
        for i,j,n in align.get_matching_blocks():
            for k in range(n):
                for u,v in zip(source_times[pos+i+k],heard_times[j+k]):
                    if u>old[-1]+.00001 and v>new[-1]+.00001:
                        old.append(u)
                        new.append(v)
        pos+=len(part)
    assert pos==len(source)
    old.append(old_end)
    new.append(end)
    return np.array(old),np.array(new),matches


def seconds(stamp):
    h,m,s = stamp.replace(',','.').split(':')
    return int(h)*3600+int(m)*60+float(s)


def run(media, work):
    before, after, matches = clocks(media,work)
    v6 = media/'05_edit/jam_v6.mp4'
    def mapped(t):
        return t if t<=OPENING/FPS else float(np.interp(t,before,after))
    srt = (media/'05_edit/jam_v6.srt').read_text(encoding='utf-8-sig')
    rows = re.findall(r'([\d:,]+) --> ([\d:,]+)\s*\n([^\n]+)',srt)
    (work/'jam_v7.srt').write_text('\n\n'.join(
        f'{i}\n{srt_at(mapped(seconds(a)))} --> {srt_at(mapped(seconds(b)))}\n{line}'
        for i,(a,b,line) in enumerate(rows,1))+'\n',encoding='utf-8-sig')
    chapters = json.loads(subprocess.check_output(['ffprobe','-v','error','-show_chapters',
                                                  '-of','json',str(v6)]))['chapters']
    meta = [';FFMETADATA1','title=내가 고르지 않은 잼을 왜 골랐다고 했을까?']
    for c in chapters:
        meta.extend(['[CHAPTER]',f'TIMEBASE=1/{FPS}',f"START={round(mapped(float(c['start_time']))*FPS)}",
                     f"END={round(mapped(float(c['end_time']))*FPS)}",'title='+c['tags']['title']])
    (work/'chapters.ffmeta').write_text('\n'.join(meta)+'\n',encoding='utf8')
    frames = round(after[-1]*FPS)
    indexes = np.floor(np.interp(np.arange(OPENING,frames)/FPS,after,before)*FPS+.000001).astype(int)
    cap = cv2.VideoCapture(str(v6))
    cap.set(cv2.CAP_PROP_POS_FRAMES,OPENING)
    cmd = ['ffmpeg','-y','-v','error','-xerror','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720',
           '-framerate',str(FPS),'-i','pipe:0','-vf','scale=out_color_matrix=bt709,format=yuv420p',
           '-c:v','libx264','-crf','16','-preset','veryfast','-colorspace','bt709','-color_trc','bt709',
           '-color_primaries','bt709',str(work/'body.mp4')]
    with subprocess.Popen(cmd, stdin=subprocess.PIPE) as encoder:
        previous=OPENING-1
        for index in indexes:
            if index!=previous:
                for _ in range(previous,index):
                    if not cap.grab():
                        raise RuntimeError(f'Source picture ended before frame {index}')
                ok,frame=cap.retrieve()
                assert ok
                previous=index
            encoder.stdin.write(memoryview(frame))
        encoder.stdin.close()
        if encoder.wait():
            raise RuntimeError('Body encode failed')
    cap.release()
    def ff(*args):
        subprocess.run(['ffmpeg','-y','-v','error','-xerror',*args],check=True)
    ff('-i',str(media/'continuity_v5/tasting_v5.mp4'),'-map','0:v:0','-c','copy',str(work/'head.mp4'))
    playlist=work/'picture.ffconcat'
    playlist.write_text(f'ffconcat version 1.0\nfile head.mp4\nduration {OPENING/FPS}\nfile body.mp4\n',
                        encoding='ascii')
    ff('-f','concat','-i',str(playlist),'-i',str(work/'mix.wav'),'-i',str(work/'chapters.ffmeta'),
       '-map','0:v','-map','1:a','-map_chapters','2','-map_metadata','2','-c:v','copy',
       '-c:a','aac','-b:a','160k','-movflags','+faststart',str(work/'jam_v7.mp4'))
    (work/'conform.json').write_text(json.dumps(dict(frames=frames,captions=len(rows),
        text_match=matches,old_seconds=before.round(5).tolist(),new_seconds=after.round(5).tolist())),
        encoding='utf8')


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('media',type=Path)
    p.add_argument('work',type=Path)
    args=p.parse_args()
    run(args.media,args.work)
