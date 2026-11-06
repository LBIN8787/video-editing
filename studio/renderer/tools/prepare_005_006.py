"""Prepare the two authored episodes from reviewed local Whisper word timings."""
import json, math, re, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[3]
RENDERER = ROOT / 'studio/renderer'
BRIEF = json.loads(Path(__file__).with_name('batch-005-006.json').read_text())

def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def norm(text):
    return re.sub(r'[^가-힣a-z0-9]', '', text.lower())

def stamp(ms):
    return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'

for episode, brief in BRIEF.items():
    folder = ROOT / 'channels/ai/episodes' / brief['folder']
    raw = json.loads((folder / 'whisper-raw.json').read_text())
    words = raw['words']
    captions, group = [], []
    for index, word in enumerate(words):
        text = word['text'].replace('엠피포로', 'MP4로')
        if group and (len(' '.join(w['text'] for w in group)) + len(text) + 1 > 26 or word['startMs'] - group[-1]['endMs'] > 400):
            captions.append(group); group = []
        group.append(dict(word, text=text))
        if text.endswith(('.', '?', '!')):
            captions.append(group); group = []
    if group: captions.append(group)
    captions = [dict(text=' '.join(w['text'] for w in g), startMs=g[0]['startMs'], endMs=g[-1]['endMs'], timestampMs=g[0]['startMs'], confidence=None, pageBreakAfter=True) for g in captions]
    duration = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(RENDERER / f'public/episode-{episode}/voice.mp3')]))
    frames = math.ceil((duration + .3) * 30)
    starts, scenes = [], []
    normalized = [norm(w['text']) for w in words]
    for scene in brief['scenes']:
        target = norm(scene['phrase'])
        candidates = [i for i in range(len(words)) if ''.join(normalized[i:i+5]).startswith(target)]
        if len(candidates) != 1: raise ValueError(f'Ambiguous phrase {episode}: {target}: {candidates}')
        starts.append(round(words[candidates[0]]['startMs'] * 30 / 1000))
    starts[0] = 0
    for i, scene in enumerate(brief['scenes']):
        scenes.append({k:v for k,v in scene.items() if k != 'phrase'} | {'id': str(i+1), 'frames': (starts[i+1] if i+1 < len(starts) else frames) - starts[i]})
    props = dict(style_version='1.0.0', episode=episode, checkedAt='2026.11.07', source=brief['source'], audio=f'episode-{episode}/voice.mp3', captions=captions, scenes=scenes)
    save(folder / 'props.json', props)
    save(folder / 'captions.json', captions)
    (folder / 'captions.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(c['startMs'])} --> {stamp(c['endMs'])}\n{c['text']}" for i,c in enumerate(captions)) + '\n', encoding='utf-8')
    image = Image.new('RGB', (1100, 440), '#19231e'); draw = ImageDraw.Draw(image)
    regular = RENDERER / 'public/fonts/NotoSansCJKkr-Regular.otf'
    bold = RENDERER / 'public/fonts/NotoSansCJKkr-Bold.otf'
    f = ImageFont.truetype(str(regular), 38); h = ImageFont.truetype(str(bold), 44)
    if episode == '005':
        title = '실제 편별 입력 · props.json'
        lines = ['style_version: "1.0.0"', 'episode: "005"', 'audio: "episode-005/voice.mp3"', f'scenes: {len(scenes)}개 · 동일 템플릿 사용']
    else:
        title = '실제 Whisper 추출 → 자막 입력'
        sample = captions[1]
        lines = [f'한국어 · small 모델 · 단어 {len(words)}개', f"{stamp(sample['startMs'])} → {stamp(sample['endMs'])}", sample['text'], '타임스탬프를 유지해 문장별 검수']
    draw.text((38,30), title, font=h, fill='#d4f85a')
    for i,line in enumerate(lines): draw.text((38,115+i*70), line, font=f, fill='#f3f1e8')
    image.save(RENDERER / f'public/episode-{episode}/evidence.png')
    print(json.dumps({'episode':episode,'frames':frames,'seconds':frames/30,'captions':len(captions),'scene_starts':starts}))
