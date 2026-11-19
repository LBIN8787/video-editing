"""Conform the approved tasting edit and direct the rest of the episode on its narration clock."""
import argparse
from bisect import bisect_right
import json
from pathlib import Path
import subprocess

import cv2
from PIL import Image, ImageOps

from full_direction import cues, regions
from render_full import captions_and_chapters, srt_at
from render_review import Cut, FPS, H, W, caption, label
from render_tasting_v5 import focus_on_blue, load_shots


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def ffmpeg(*args):
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-xerror', *args], check=True)


def artwork(media, work):
    plates = load_shots(media / 'continuity_v5')
    plates['blue'] = focus_on_blue(plates['choose'])
    for name, keys in [
        ('lab_inserts', [None, 'card_doubt', 'key_press', 'wrapper']),
        ('shop_inserts', ['notes', 'counter_reply', 'walk_back', 'saucer']),
    ]:
        for image, key in zip(regions(work / (name + '.png')), keys, strict=True):
            if key:
                plates[key] = ImageOps.fit(image, (W, H), Image.Resampling.LANCZOS)
    with Image.open(work / 'card_record.png') as image:
        plates['card_record'] = ImageOps.fit(image.convert('RGB'), (W, H), Image.Resampling.LANCZOS)
    for key, base, note in [
        ('now', 'saucer', '시식대에서 바로 말한 경우'),
        ('later', 'walk_back', '시식이 끝난 뒤 말한 경우'),
        ('describe', 'answer', '맛의 차이만 말한 경우'),
    ]:
        plates[key] = plates[base].copy()
        label(plates[key], (32, 26), note + '  ·  상황 재구성', True)
    for key, note in [('card_record', '카드 선택 기록 재구성'), ('key_press', '컴퓨터 실험 재구성'),
                      ('wrapper', '초콜릿 실험 재구성')]:
        label(plates[key], (32, 26), note, True)
    shop = Cut(media / 'art')
    for key in ['control_one', 'control_pair']:
        frame = shop.explain.copy()
        label(frame, (32, 26), '병을 그대로 둔 차례  ·  Hall 외 (2010)', True)
        shop.jar(frame, shop.jars[0], (375, 315), 318, shadow=False)
        label(frame, (268, 520), '처음 고른 병')
        if key == 'control_pair':
            shop.jar(frame, shop.jars[0], (883, 315), 318, shadow=False)
            label(frame, (731, 520), '다시 받은 같은 잼')
        plates[key] = frame
    return plates


def body_picture(media, work, old_movie, scenes, groups):
    plates = artwork(media, work)
    directions = read(Path(__file__).with_name('full_v6_cuts.json'))
    assert set(directions) == {s['shot'] for s in scenes}
    edits = [cues(s, directions[s['shot']]) for s in scenes]
    assert all(k in plates or k == 'original' for edit in edits for _, k in edit)
    cap = cv2.VideoCapture(str(old_movie))
    if not cap.set(cv2.CAP_PROP_POS_FRAMES, scenes[0]['start']):
        raise RuntimeError('Cannot locate the first body frame')
    args = ['ffmpeg', '-y', '-v', 'error', '-xerror', '-f', 'rawvideo', '-pix_fmt', 'bgr24',
            '-video_size', f'{W}x{H}', '-framerate', str(FPS), '-i', 'pipe:0', '-an',
            '-vf', 'scale=out_color_matrix=bt709,format=yuv420p', '-c:v', 'libx264',
            '-preset', 'veryfast', '-crf', '16', '-colorspace', 'bt709', '-color_trc', 'bt709',
            '-color_primaries', 'bt709', str(work / 'body.mp4')]
    with subprocess.Popen(args, stdin=subprocess.PIPE) as encoder:
        try:
            for scene, rows, edit in zip(scenes, groups, edits, strict=True):
                starts = [at for at, _ in edit]
                stamp, cached = None, None
                for index in range(scene['frames']):
                    t = index / FPS
                    key = edit[bisect_right(starts, t) - 1][1]
                    if not cap.grab():
                        raise RuntimeError(f"Missing frame in {scene['shot']}")
                    if key == 'original':
                        ok, frame = cap.retrieve()
                        if not ok:
                            raise RuntimeError('Cannot decode source frame')
                        pixels = memoryview(frame)
                    else:
                        line = next((text for a, b, text in rows if a <= t < b), '')
                        if (key, line) != stamp:
                            frame = plates[key].copy()
                            caption(frame, rows, t)
                            cached = frame.tobytes('raw', 'BGR')
                            stamp = key, line
                        pixels = cached
                    encoder.stdin.write(pixels)
                print(scene['shot'], flush=True)
        finally:
            encoder.stdin.close()
            cap.release()
        if encoder.wait():
            raise RuntimeError('Body picture encode failed')
    return edits


def render(media, work):
    old_movie = media / '05_edit/final_direction_v3.mp4'
    approved = media / 'continuity_v5/tasting_v5.mp4'
    full = read(media / 'full_v2/voice-timeline.json')
    groups, chapters, _ = captions_and_chapters(full)
    first = next(i for i, scene in enumerate(full) if scene['shot'] == 'question')
    original_head = full[first]['start']
    cap = cv2.VideoCapture(str(approved))
    head = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    assert head > 0 and cap.get(cv2.CAP_PROP_FPS) == FPS
    cap.release()
    difference = original_head - head
    edits = body_picture(media, work, old_movie, full[first:], groups[first:])
    ffmpeg('-i', str(approved), '-map', '0:v:0', '-c:v', 'copy', str(work / 'opening.mp4'))
    concat = work / 'picture.ffconcat'
    concat.write_text('ffconcat version 1.0\nfile opening.mp4\nduration '
                      + str(head / FPS) + '\nfile body.mp4\n', encoding='ascii')
    meta = [';FFMETADATA1', 'title=내가 고르지 않은 잼을 왜 골랐다고 했을까?']
    for ch in chapters:
        start = max(0, ch['start'] - difference)
        meta += ['[CHAPTER]', f'TIMEBASE=1/{FPS}', f'START={start}', f"END={ch['end']-difference}",
                 'title=' + ch['title']]
    chapter_path = work / 'chapters.ffmeta'
    chapter_path.write_text('\n'.join(meta) + '\n', encoding='utf8')
    intro_cues = read(media / 'continuity_v4/dialogue_cues.json')['captions']
    subs = list(intro_cues)
    for scene, rows in zip(full[first:], groups[first:], strict=True):
        start = (scene['start'] - difference) / FPS
        subs.extend((start + a, start + b, line) for a, b, line in rows)
    # The reviewed opening has a tiny overlap at the end of "음…". Match its burnt-in priority.
    for i in range(1, len(subs)):
        a, b, text = subs[i]
        subs[i] = (max(a, subs[i-1][1]), b, text)
    (work / 'jam_v6.srt').write_text('\n\n'.join(
        f'{i}\n{srt_at(a)} --> {srt_at(b)}\n{line}'
        for i, (a, b, line) in enumerate(subs, 1)) + '\n', encoding='utf-8-sig')
    audio = (f'[1:a]aresample=48000,apad,atrim=end_sample={head*48000//FPS},'
             'volume=7dB,alimiter=limit=.88:level=0:latency=1[a];'
             f'[2:a]aresample=48000,atrim=start_sample={original_head*48000//FPS},'
             'asetpts=PTS-STARTPTS,volume=-1dB[b];[a][b]concat=n=2:v=0:a=1[voice]')
    ffmpeg('-f', 'concat', '-i', str(concat), '-i', str(approved), '-i', str(old_movie),
           '-i', str(chapter_path), '-filter_complex', audio, '-map', '0:v:0', '-map', '[voice]',
           '-map_metadata', '3', '-map_chapters', '3', '-c:v', 'copy', '-c:a', 'aac', '-b:a',
           '160k', '-movflags', '+faststart', str(work / 'jam_v6.mp4'))
    conform = [{'shot': 'approved_v5', 'start': 0, 'frames': head}]
    for scene, edit in zip(full[first:], edits, strict=True):
        conform.append(dict(shot=scene['shot'], start=scene['start']-difference,
                            frames=scene['frames'], cuts=edit))
    (work / 'jam_v6.edits.json').write_text(json.dumps(conform, ensure_ascii=False, indent=2),
                                            encoding='utf8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('media', type=Path)
    parser.add_argument('work', type=Path)
    args = parser.parse_args()
    render(args.media, args.work)
