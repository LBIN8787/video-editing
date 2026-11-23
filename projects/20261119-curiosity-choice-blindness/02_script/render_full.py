"""Render the full approved choice-blindness episode and time-aligned review sidecars."""
import argparse
import json
from pathlib import Path
import subprocess

from full_direction import FullDirection
from render_review import W,H,FPS,RATE,captions,caption


TITLE='내가 고르지 않은 잼을 왜 골랐다고 했을까?'
AUDIO_FILTER='volume=4dB,alimiter=limit=0.78:level=0:latency=1'


def master_voice(voice):
    pcm=(voice/'review.pcm').read_bytes()
    # The word boundaries precede the decoded Edge takes by 240 ms.
    # Advance the continuous track into the opening silence without changing its duration.
    lead=round(.24*RATE)*2
    path=voice/'master.pcm'
    path.write_bytes(pcm[lead:]+bytes(lead))
    return path


def srt_at(seconds):
    ms=round(seconds*1000)
    return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'


def captions_and_chapters(timeline):
    groups=[]
    chapter_starts=[]
    srt=[]
    for scene in timeline:
        rows=captions(scene)
        assert rows,scene['shot']
        groups.append(rows)
        t=scene['start']/FPS
        if not chapter_starts or chapter_starts[-1][1]!=scene['chapter']:
            chapter_starts.append((scene['start'],scene['chapter']))
        for a,b,line in rows:
            srt.append(f'{len(srt)+1}\n{srt_at(t+a)} --> {srt_at(t+b)}\n{line}')
    total=timeline[-1]['start']+timeline[-1]['frames']
    ends=[at for at,_ in chapter_starts[1:]]+[total]
    chapter_rows=[dict(start=a,end=b,title=title) for (a,title),b in zip(chapter_starts,ends,strict=True)]
    return groups,chapter_rows,srt


def render(media,edition='final_direction_v3'):
    voice=media/'full_v2'
    out=media/'05_edit'
    timeline=json.loads((voice/'voice-timeline.json').read_text(encoding='utf8'))
    cuts=FullDirection(media/'art',timeline)
    groups,chapters,srt=captions_and_chapters(timeline)
    chapter_ffmeta=[';FFMETADATA1',f'title={TITLE}']
    for row in chapters:
        chapter_ffmeta.extend(('[CHAPTER]',f'TIMEBASE=1/{FPS}',f"START={row['start']}",
                                f"END={row['end']}",f"title={row['title']}"))
    chapters_input=voice/'chapters.ffmeta'
    chapters_input.write_text('\n'.join(chapter_ffmeta)+'\n',encoding='utf8')
    destination=out/(edition+'.mp4')
    pending=destination.with_suffix('.pending.mp4')
    encoder=subprocess.Popen(['ffmpeg','-y','-v','error','-xerror','-f','rawvideo','-pixel_format','rgb24',
       '-framerate',str(FPS),'-video_size',f'{W}x{H}','-i','pipe:0','-f','s16le','-ar',str(RATE),
       '-ac','1','-i',str(master_voice(voice)),'-f','ffmetadata','-i',str(chapters_input),
       '-map','0:v:0','-map','1:a:0','-map_metadata','2','-map_chapters','2',
       '-af',AUDIO_FILTER,'-c:v','libx264','-preset','veryfast',
       '-crf','16','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart',
       str(pending)],stdin=subprocess.PIPE)
    try:
        for scene,rows in zip(timeline,groups,strict=True):
            for frame in range(scene['frames']):
                t=frame/FPS
                im=cuts.frame(scene['shot'],t)
                if im.size!=(W,H) or im.mode!='RGB':
                    raise ValueError((scene['shot'],frame,im.size,im.mode))
                caption(im,rows,t)
                encoder.stdin.write(im.tobytes())
            print(scene['shot'],round((scene['start']+scene['frames'])/FPS,2),flush=True)
        encoder.stdin.close()
        if encoder.wait():
            raise RuntimeError('Production render failed')
    finally:
        if encoder.poll() is None:
            encoder.kill()
            encoder.wait()
    pending.replace(destination)
    (out/(edition+'.srt')).write_text('\n'.join(srt)+'\n',encoding='utf-8-sig')
    (out/(edition+'.chapters.json')).write_text(json.dumps(chapters,ensure_ascii=False,indent=2),encoding='utf8')
    assets=[dict(shot=s['shot'],start=s['start'],frames=s['frames'],cues=cuts.actions.get(s['shot']))
            for s in timeline]
    (out/(edition+'.cues.json')).write_text(json.dumps(assets,ensure_ascii=False,indent=2),encoding='utf8')
    print(f'{chapters[-1]["end"]/FPS:.3f} s · {len(srt)} captions · {len(chapters)} chapters',flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('media',type=Path)
    parser.add_argument('--edition',default='final_direction_v3')
    args=parser.parse_args()
    render(args.media,args.edition)
