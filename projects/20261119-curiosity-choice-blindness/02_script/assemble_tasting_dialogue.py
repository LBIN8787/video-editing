"""Assemble the narrator and character takes without changing their speaking speed."""
import argparse
import json
from pathlib import Path
import subprocess
import wave

import numpy as np

SAMPLE_RATE = 48000


def pcm(path):
    result = subprocess.run(
        ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-i', str(path),
         '-ac', '1', '-ar', str(SAMPLE_RATE), '-f', 'f32le', '-'],
        check=True, stdout=subprocess.PIPE,
    )
    return np.frombuffer(result.stdout, dtype='<f4')


def assemble(folder):
    sources = {name: pcm(folder / f'{name}.mp3')
               for name in ('nobel_take', 'seoyoon_acting', 'staff_acting')}
    chunks = []
    sections = []
    current = 0

    def add(name, start, end, silence_after):
        nonlocal current
        audio = sources[name][round(start*SAMPLE_RATE):round(end*SAMPLE_RATE)].copy()
        # A short boundary ramp prevents clicks and preserves the spoken timing.
        ramp = min(144, len(audio)//2)
        audio[:ramp] *= np.linspace(0, 1, ramp)
        audio[-ramp:] *= np.linspace(1, 0, ramp)
        position = current / SAMPLE_RATE
        chunks.extend((audio, np.zeros(round(silence_after*SAMPLE_RATE), dtype=np.float32)))
        current += len(audio) + len(chunks[-1])
        sections.append({'source': name, 'in': start, 'out': end, 'at': position})
        return position

    choose = add('seoyoon_acting', 0, 2.02, .30)
    narration = add('nobel_take', 2.32, 19.16, .28)
    staff = add('staff_acting', 0, 3.96, .26)
    hesitate = add('nobel_take', 23.22, 25.70, .38)
    answer = add('seoyoon_acting', 2.35, 7.98, .20)
    end = current / SAMPLE_RATE

    captions = [
        (choose, choose+.98, '“빨간 병이요.'),
        (choose+1.14, choose+1.94, '이걸로 할게요.”'),
        (narration+.12, narration+3.92, '서윤은 카트에서 한 손을 떼고 빨간 띠를 가리켰습니다.'),
        (narration+4.28, narration+6.36, '사과랑 계피 향이 났거든요.'),
        (narration+6.77, narration+10.24, '자몽의 쌉쌀한 맛이 났던 건 파란 병이었죠.'),
        (narration+10.24, narration+12.48, '직원이 빨간 병을 다시 열었습니다.'),
        (narration+12.48, narration+16.84, '서윤은 그 병에서 뜬 잼을 한 숟가락 더 받아 들었습니다.'),
        (staff, staff+1.10, '“이번엔 어때요?'),
        (staff+1.48, staff+3.83, '아까 그걸 고르신 이유가 궁금해서요.”'),
        (hesitate, hesitate+2.48, '서윤이 잠깐 입을 다뭅니다.'),
        (answer+.13, answer+1.30, '“음…'),
        (answer+1.25, answer+3.84, '끝맛이 살짝 쌉쌀해서요.'),
        (answer+4.21, answer+5.51, '그게 좋았어요.”'),
    ]
    timeline = {
        'anchors': [
            choose, narration+.12, narration+4.28, narration+6.77,
            narration+10.24, narration+12.48, staff, hesitate, answer, end,
        ],
        'captions': captions,
        'sections': sections,
        'roles': {
            'narrator': {'name': 'Nobel Butler', 'voice_id': 'YBRudLRm83BV5Mazcr42'},
            'seoyoon': {'name': 'Kanna - Calm & Friendly', 'voice_id': '5I7B1di44aCL15NkP0jn'},
            'staff': {'name': 'SU-01', 'voice_id': 'fucCZkuDBeKO8ZpPNr6N'},
        },
        'model': 'eleven_v4',
        'purpose': '서윤의 선택과 주저하는 대답, 직원의 일상적인 질문을 다른 배우로 연결한다.',
    }
    mixed = np.concatenate(chunks)
    if abs(mixed).max() > .99:
        mixed *= .99/abs(mixed).max()
    with wave.open(str(folder/'dialogue.wav'), 'wb') as output:
        output.setparams((1, 2, SAMPLE_RATE, 0, 'NONE', 'not compressed'))
        output.writeframes((mixed*32767).astype('<i2').tobytes())
    (folder/'dialogue_cues.json').write_text(
        json.dumps(timeline, ensure_ascii=False, indent=2), encoding='utf-8',
    )
    print(f'{end:.3f}s', json.dumps(timeline['anchors']))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('folder', type=Path)
    assemble(parser.parse_args().folder)
