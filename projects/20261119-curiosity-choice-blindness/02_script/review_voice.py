"""Narrate the approved v2 excerpts for the direction review."""
import argparse
import asyncio
from hashlib import sha256
import json
from pathlib import Path
import subprocess

import edge_tts

RATE = 24000
FPS = 24
VOICE = 'ko-KR-InJoonNeural'


CHAPTER_SHOTS = (
    ('choose','turn_to_taste','ask','hesitate','question','recon','rewind','bridge'),
    ('cards_demo','cards_source','cards_response','cards_analysis','cards_record','cards_time','cards_reasons','cards_back'),
    ('jam_intro','section','flip','return','jam_control','jam_limits'),
    ('react','detect','classify','recognize','two_readings'),
    ('computer_design','computer_measure','computer_doubt','computer_results','computer_pupil','computer_scope'),
    ('chocolate_intro','chocolate_test','chocolate_compare','chocolate_return'),
    ('ending_recap','ending_spoon'),
)


def paragraphs():
    script = Path(__file__).with_name('script_v2.md').read_text(encoding='utf8')
    groups = {}
    for line in script.splitlines():
        if line.startswith('## '):
            group = groups.setdefault(line[3:], [])
        elif line.startswith(('● ', '○ ')):
            group.append(line[2:].strip())
    return groups


def excerpts():
    groups = paragraphs()
    opening = groups['같은 빨간 병'][:5]
    experiment = groups['시식대 뒤에서']
    return_to_counter, separator, _ = experiment[3].partition(' 처음 받았던')
    assert separator
    reveal = experiment[1:3] + [return_to_counter]
    ids = ['choose', 'turn_to_taste', 'ask', 'hesitate', 'question', 'section', 'flip', 'return']
    return list(zip(ids, opening + reveal, strict=True))


async def narrate(media, full=False):
    cache = media / 'review_voice'
    cache.mkdir(parents=True, exist_ok=True)
    folder = media / ('full_v2' if full else 'review_voice')
    folder.mkdir(parents=True, exist_ok=True)
    limit = asyncio.Semaphore(3)

    async def make_take(shot, text):
        key = sha256((VOICE + text).encode()).hexdigest()[:12]
        cached = cache / f'{shot}-{key}.pcm'
        boundaries = cached.with_suffix('.json')
        if cached.is_file() and boundaries.is_file():
            return cached.read_bytes(), json.loads(boundaries.read_text(encoding='utf8'))
        async with limit:
            for attempt in range(3):
                audio, words = [], []
                try:
                    source = edge_tts.Communicate(text, VOICE, rate='+10%', boundary='WordBoundary')
                    async for chunk in source.stream():
                        if chunk['type'] == 'audio':
                            audio.append(chunk['data'])
                        elif chunk['type'] == 'WordBoundary':
                            words.append({name:chunk[name] for name in ('offset','duration','text')})
                    if audio and words:
                        break
                    raise RuntimeError('Speech or word boundaries missing')
                except Exception:
                    if attempt == 2:
                        raise
                    await asyncio.sleep(attempt + 1)
        pcm = subprocess.run(['ffmpeg','-v','error','-i','pipe:0','-ac','1','-ar',str(RATE),
                              '-f','s16le','pipe:1'], input=b''.join(audio), capture_output=True, check=True).stdout
        cached.write_bytes(pcm)
        boundaries.write_text(json.dumps(words,ensure_ascii=False),encoding='utf8')
        print(shot, len(pcm)/2/RATE, flush=True)
        return pcm, words

    if full:
        edits = [
            (shot, text, chapter)
            for (chapter, lines), shot_ids in zip(paragraphs().items(),CHAPTER_SHOTS,strict=True)
            for shot, text in zip(shot_ids, lines, strict=True)
        ]
    else:
        edits = [(shot,text,'') for shot,text in excerpts()]
    takes = await asyncio.gather(*(make_take(shot,text) for shot,text,_ in edits))
    clock = []
    cursor = 0
    with (folder/'review.pcm').open('wb') as master:
        for (shot,text,chapter),(pcm,words) in zip(edits,takes,strict=True):
            frames = (len(pcm)//2 + RATE//FPS - 1)//(RATE//FPS)
            clock.append(dict(shot=shot,text=text,chapter=chapter,start=cursor,frames=frames,words=words))
            cursor += frames
            master.write(pcm)
            master.write(bytes(frames*RATE//FPS*2-len(pcm)))
    (folder/'voice-timeline.json').write_text(json.dumps(clock,ensure_ascii=False,indent=2),encoding='utf8')
    print(f'{cursor/FPS:.2f} s')


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('media',type=Path)
    asyncio.run(narrate(parser.parse_args().media))
