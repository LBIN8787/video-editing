"""Cut the tasting excerpt to the existing role dialogue and its caption cues."""
import argparse
import json
from pathlib import Path
import subprocess

from PIL import Image, ImageFilter, ImageOps

from render_review import H, W, caption, label
from review_voice import FPS


def load_shots(art):
    def panel(sheet, index):
        width, height = sheet.size
        x, y = index % 2 * (width // 2), index // 2 * (height // 2)
        box = (x + 3, y + 3, x + width // 2 - 3, y + height // 2 - 3)
        return ImageOps.fit(sheet.crop(box), (W, H), Image.Resampling.LANCZOS)

    shots = {}
    for filename, names in [
        ('coverage.png', ['choose', 'open', None, 'answer']),
        ('acting.png', ['take', 'taste', 'ask', 'pause']),
    ]:
        with Image.open(art / filename) as source:
            for index, name in enumerate(names):
                if name:
                    shots[name] = panel(source.convert('RGB'), index)
    with Image.open(art / 'point.png') as source:
        shots['wide'] = ImageOps.fit(source.convert('RGB'), (W, H), Image.Resampling.LANCZOS)
    return shots


def focus_on_blue(shot):
    # Let the viewer find the other flavour without moving either jar.
    ramp = Image.linear_gradient('L').rotate(90).resize((int(W * .44), H))
    mask = Image.new('L', (W, H))
    mask.paste(255, (int(W * .64), 0, W, H))
    mask.paste(ramp, (int(W * .20), 0))
    return Image.composite(shot, shot.filter(ImageFilter.GaussianBlur(3.5)), mask)


def render(art, voice_cut, cues, output):
    shots = load_shots(art)
    focused = focus_on_blue(shots['choose'])
    timeline = json.loads(cues.read_text(encoding='utf-8'))
    cuts = [(0, 'wide'), (4.55, 'choose'), (12.75, 'open'), (15.55, 'take'),
            (18.25, 'taste'), (20.08, 'ask'), (22.88, 'pause'), (27.84, 'answer')]
    command = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-xerror', '-n',
               '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
               '-i', 'pipe:0', '-i', str(voice_cut), '-map', '0:v', '-map', '1:a:0',
               '-c:v', 'libx264', '-crf', '16', '-preset', 'medium', '-vf',
               'scale=out_color_matrix=bt709,format=yuv420p', '-colorspace', 'bt709',
               '-color_trc', 'bt709', '-color_primaries', 'bt709', '-c:a', 'copy',
               '-movflags', '+faststart', str(output)]
    with subprocess.Popen(command, stdin=subprocess.PIPE) as encoder:
        for index in range(round(timeline['anchors'][-1] * FPS)):
            time = index / FPS
            name = next(key for start, key in reversed(cuts) if start <= time)
            picture = shots[name].copy()
            if name == 'choose' and time >= 9.1:
                picture = Image.blend(picture, focused, min(1, (time - 9.1) / .55))
            if time < 2.3:
                label(picture, (28, 24), '시식 상황 재구성', True)
            caption(picture, timeline['captions'], time)
            encoder.stdin.write(picture.tobytes())
        encoder.stdin.close()
        if encoder.wait():
            raise RuntimeError('Tasting excerpt encoding failed')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for argument in ('art', 'voice_cut', 'cues', 'output'):
        parser.add_argument(argument, type=Path)
    args = parser.parse_args()
    render(args.art, args.voice_cut, args.cues, args.output)
