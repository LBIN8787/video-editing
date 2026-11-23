"""Mix individual Korean performances on a common, dry mono dialogue bus."""
import argparse
import json
import re
import subprocess
import wave
from pathlib import Path

import numpy as np

RATE = 48000


def read_audio(path):
    data = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(path), '-map', '0:a:0',
                                   '-ac', '1', '-ar', str(RATE), '-f', 'f32le', '-'])
    return np.frombuffer(data, '<f4').copy()


def reduce_reflections(signal):
    # Predict delayed energy from earlier frames. Keep the direct voice and early reflections.
    size, hop = 2048, 512
    window = np.hanning(size)
    padded = np.pad(signal, (size, size + hop))
    frames = np.lib.stride_tricks.sliding_window_view(padded, size)[::hop]
    spectrum = np.fft.rfft(frames * window)
    delays = (4, 5, 6, 7, 8, 9)
    output = np.zeros(len(padded))
    weight = np.zeros(len(padded))
    for first in range(0, len(frames), 640):
        end = min(first + 640, len(frames))
        ids = np.arange(first, end)
        target = spectrum[ids].T
        past = np.stack([spectrum[np.maximum(0, ids-delay)].T for delay in delays], axis=-1)
        power = np.maximum(abs(target)**2, np.mean(abs(target)**2, axis=1, keepdims=True)*.015 + 1e-8)
        weighted = past.conj() / power[:, :, None]
        gram = np.einsum('ftk,ftl->fkl', weighted, past)
        diagonal = np.trace(gram, axis1=1, axis2=2).real / len(delays)
        gram += (diagonal*.04 + .001)[:, None, None] * np.eye(len(delays))
        rhs = np.einsum('ftk,ft->fk', weighted, target)
        taps = np.linalg.solve(gram, rhs[:, :, None])[:, :, 0]
        delayed = np.einsum('ftk,fk->ft', past, taps)
        subtraction = np.minimum(1, abs(target)/(abs(delayed)+1e-8))
        processed = np.fft.irfft((target - .42*delayed*subtraction).T, n=size) * window
        for i, frame in zip(ids, processed):
            output[i*hop:i*hop+size] += frame
            weight[i*hop:i*hop+size] += window**2
    return (output / np.maximum(weight, 1e-8))[size:size+len(signal)].astype('<f4')


def level(audio, target):
    inp = ['ffmpeg', '-hide_banner', '-nostats', '-f', 'f32le', '-ar', str(RATE), '-ac', '1', '-i', '-']
    report = subprocess.run(inp + ['-af', 'ebur128', '-f', 'null', '-'], input=audio.tobytes(),
                            stderr=subprocess.PIPE, check=True).stderr.decode(errors='replace')
    loudness = float(re.findall(r'I:\s*([-\d.]+) LUFS', report)[-1])
    filters = (f'highpass=f=68,equalizer=f=275:t=o:w=1.15:g=-1.1,volume={target-loudness:.3f}dB,'
               'alimiter=limit=.87:level=0:latency=1')
    data = subprocess.check_output(inp + ['-loglevel', 'error', '-af', filters, '-f', 'f32le', '-'],
                                   input=audio.tobytes())
    result = np.frombuffer(data, '<f4').copy()
    assert len(result) == len(audio)
    return result, loudness


def taper(audio):
    ramp = np.linspace(0, 1, min(len(audio)//2, 240))
    audio[:len(ramp)] *= ramp
    audio[-len(ramp):] *= ramp[::-1]
    return audio


def mix(media, work):
    plan = json.loads((work/'takes.json').read_text(encoding='utf8'))
    intro = media/'continuity_v4'
    original = json.loads((intro/'dialogue_cues.json').read_text(encoding='utf8'))
    header = np.zeros(776*RATE//24, dtype='<f4')
    report = []
    for name in {s['source'] for s in original['sections']}:
        sound, loudness = level(reduce_reflections(read_audio(intro/(name+'.mp3'))), -18.0)
        for s in original['sections']:
            if s['source'] != name:
                continue
            sample = taper(sound[round(s['in']*RATE):round(s['out']*RATE)].copy())
            start = round(s['at']*RATE)
            header[start:start+len(sample)] = sample
        report.append(dict(take=name, input_lufs=loudness))
    chunks = [header]
    position = len(header)
    for take in plan:
        raw = read_audio(work/(take['id']+'.mp3'))
        # Remove only outer digital silence. Breath and intra-sentence timing stay in the take.
        active = np.flatnonzero(abs(raw) > .004)
        first = max(0, active[0]-round(.065*RATE))
        last = min(len(raw), active[-1]+round(.11*RATE))
        sound, loudness = level(reduce_reflections(raw[first:last]), -18.0)
        pause = .30 if take['role']=='narrator' else .18
        if take['id'] in ('t07','t08'):
            pause = .06
        gap = np.zeros(round(pause*RATE), dtype='<f4')
        position += len(gap)
        chunks.extend([gap, taper(sound)])
        report.append(dict(take=take['id'], role=take['role'], start=position/RATE,
                           source_in=first/RATE, source_out=last/RATE, input_lufs=loudness))
        position += len(sound)
    audio = np.concatenate(chunks)
    frames = int(np.ceil((len(audio)+RATE*.34)/(RATE/24)))
    audio = np.pad(audio,(0, frames*(RATE//24)-len(audio)))
    with wave.open(str(work/'mix.wav'), 'wb') as f:
        f.setparams((1,2,RATE,0,'NONE','not compressed'))
        f.writeframes(np.round(audio*32767).astype('<i2').tobytes())
    (work/'mix.json').write_text(json.dumps(report, indent=2),encoding='utf8')
    print(frames, len(audio)/RATE, flush=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('media',type=Path)
    p.add_argument('work',type=Path)
    args = p.parse_args()
    mix(args.media,args.work)
