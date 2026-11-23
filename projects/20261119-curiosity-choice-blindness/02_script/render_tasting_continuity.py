"""Render the tasting sequence from the approved art and a fixed-camera hand insert."""
import argparse
from functools import lru_cache
import json
from pathlib import Path
import subprocess

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps

from render_review import W, H, caption, label
from review_voice import FPS

SIZE = (W, H)
RESAMPLE = Image.Resampling.LANCZOS
BICUBIC = Image.Resampling.BICUBIC
REFERENCE = (0.0, 4.306, 8.917, 11.667, 15.463, 18.790, 23.681, 29.600, 32.580, 38.0)

TASTING_ARM = (
    (452, 223), (462, 215), (477, 215), (485, 223), (487, 234), (483, 242),
    (489, 255), (495, 256), (496, 263), (504, 266), (514, 281), (517, 298),
    (513, 322), (504, 344), (482, 360), (463, 372), (444, 411), (424, 461),
    (432, 471), (417, 506), (393, 530), (360, 526), (336, 509), (341, 479),
    (365, 441), (382, 420), (402, 388), (417, 357), (421, 332), (425, 310),
    (434, 290), (442, 275), (453, 261), (470, 246), (468, 243), (459, 239),
)


def progress(time, start, end):
    fraction = max(0.0, min(1.0, (time - start) / (end - start)))
    return fraction * fraction * (3 - 2 * fraction)


def path(time, keys):
    for (start, before), (end, after) in zip(keys, keys[1:]):
        if time < end:
            amount = progress(time, start, end)
            return tuple(a + (b - a) * amount for a, b in zip(before, after))
    return keys[-1][1]


def crop_poses(folder):
    art = Image.open(folder / 'tasting.png').convert('RGB')
    width, height = art.width // 2, art.height // 2
    return {
        key: ImageOps.fit(
            art.crop((column * width + 2, row * height + 2,
                      (column + 1) * width - 2, (row + 1) * height - 2)),
            SIZE, RESAMPLE,
        )
        for key, column, row in (('point', 0, 0), ('taste', 1, 0), ('finish', 1, 1))
    }


def cut_prop(sheet, box, width, anchor):
    image = sheet.crop(box)
    alpha = np.asarray(image.getchannel('A'))
    # The opaque artwork defines the matte. Remove isolated low-alpha fringe pixels.
    strong = cv2.dilate((alpha > 140).astype('uint8'), np.ones((5, 5), np.uint8))
    image.putalpha(Image.fromarray(alpha * strong))
    image = image.resize((width, round(image.height * width / image.width)), RESAMPLE)
    x, y = anchor[0] * image.width, anchor[1] * image.height
    return image, (round(x), round(y))


def put(im, prop, position, angle=0):
    art, anchor = prop
    # Transform only the isolated prop. Its point of contact stays at position.
    angle = round(angle, 1)
    local = Image.new('RGBA', (art.width * 2, art.height * 2))
    origin = (art.width - anchor[0], art.height - anchor[1])
    local.paste(art, origin)
    rotated = local.rotate(angle, BICUBIC, expand=True) if angle else local
    im.paste(rotated, (round(position[0] - rotated.width / 2),
                       round(position[1] - rotated.height / 2)), rotated)


class TastingPose:
    def __init__(self, facing, clean):
        self.original = facing
        arm_mask = Image.new('L', SIZE)
        ImageDraw.Draw(arm_mask).polygon(TASTING_ARM, fill=255)
        arm = facing.convert('RGBA')
        arm.putalpha(arm_mask.filter(ImageFilter.GaussianBlur(.6)))
        arm_box = (319, 207, 530, 542)
        self.arm = arm.crop(arm_box), (354 - arm_box[0], 527 - arm_box[1])
        self.empty = Image.composite(clean, facing, arm_mask.filter(ImageFilter.GaussianBlur(1)))

        # Trace the inner lid of each eye, so the painted irises never escape the lid.
        eyes = (
            (((376, 181), (382, 168), (390, 161), (400, 160), (407, 164),
              (413, 177), (401, 181), (390, 184)), (403, 168, 8, 11)),
            (((447, 155), (451, 142), (456, 138), (463, 140), (468, 148),
              (464, 157), (458, 161), (451, 159)), (457, 149, 5, 10)),
        )
        self.eyes = []
        for contour, (x, y, rx, ry) in eyes:
            clip = Image.new('L', SIZE)
            ImageDraw.Draw(clip).polygon(contour, fill=255)
            area = (x-rx-17, y-ry-9, x+rx+17, y+ry+14)
            white = facing.crop(area)
            eye_clip = clip.crop(area).filter(ImageFilter.GaussianBlur(.4))
            iris = Image.new('L', white.size)
            iris_x, iris_y = x-area[0], y-area[1]
            ImageDraw.Draw(iris).ellipse((iris_x-rx, iris_y-ry, iris_x+rx, iris_y+ry), fill=255)
            iris = Image.fromarray(np.minimum(np.asarray(iris), np.asarray(eye_clip))).filter(
                ImageFilter.GaussianBlur(.6)
            )
            white_pixels = cv2.inpaint(np.asarray(white), np.asarray(iris.point(lambda v: 255 if v > 60 else 0)),
                                       3, cv2.INPAINT_TELEA)
            self.eyes.append((area, Image.fromarray(white_pixels), white, iris, eye_clip))

    @lru_cache(maxsize=64)
    def arm_angle(self, angle):
        if not angle:
            return self.original.copy()
        canvas = self.empty.copy()
        put(canvas, self.arm, (354, 527), angle)
        return canvas

    def frame(self, local):
        angle, gaze_x, gaze_y = path(local, (
            (0, (-5.4, -4, 4)), (.40, (0, -3, 3)), (.76, (0, 0, 1)),
            (1.15, (0, 0, 0)), (2.35, (0, 0, 0)), (3.0, (-2.2, -2, 2)),
            (4.15, (-2.7, -1, 1)), (5.9, (-2.5, 0, 0)), (9.5, (-2.6, 0, 0)),
        ))
        im = self.arm_angle(round(angle, 1)).copy()
        shift_x, shift_y = round(gaze_x), round(gaze_y)
        if shift_x or shift_y:
            for area, white, old, iris, clip in self.eyes:
                shifted = old.transform(old.size, Image.Transform.AFFINE,
                                        (1, 0, -shift_x, 0, 1, -shift_y), BICUBIC)
                moving_alpha = iris.transform(iris.size, Image.Transform.AFFINE,
                                              (1, 0, -shift_x, 0, 1, -shift_y), BICUBIC)
                eye = Image.composite(shifted, white, moving_alpha)
                im.paste(eye, area[:2], clip)
        return im


class Scene:
    def __init__(self, folder):
        self.poses = crop_poses(folder)
        clean = ImageOps.fit(Image.open(folder/'taste_clean.png').convert('RGB'), SIZE, RESAMPLE)
        self.face = TastingPose(self.poses['taste'], clean)
        self.table = ImageOps.fit(Image.open(folder / 'insert.png').convert('RGB'), SIZE, RESAMPLE)
        sheet = Image.open(folder / 'props.png').convert('RGBA')
        arms = Image.open(folder/'arms.png').convert('RGBA')
        self.pointing = cut_prop(arms, (109, 4, 1414, 305), 760, (.991, .64))
        self.staff = cut_prop(arms, (248, 320, 1558, 622), 840, (.018, .45))
        self.receive = cut_prop(arms, (108, 628, 1364, 939), 850, (.981, .48))
        self.spoon = cut_prop(sheet, (1453, 331, 1736, 384), 196, (.85, .48))
        spoon, spoon_anchor = self.spoon
        spoon_pixels = np.asarray(spoon)
        rgb = spoon_pixels[:, :, :3]
        red = rgb[:, :, 0].astype('int16')
        jam = ((red - rgb[:, :, 2] > 65) & (spoon_pixels[:, :, 3] > 230)).astype('uint8')
        jam[:, 68:] = 0
        empty_spoon = Image.fromarray(cv2.inpaint(rgb, jam, 4, cv2.INPAINT_TELEA))
        empty_spoon.putalpha(spoon.getchannel('A'))
        self.empty_spoon = empty_spoon, spoon_anchor
        self.lid = cut_prop(sheet, (1860, 299, 2093, 417), 199, (.5, .56))

        jar = (409, 311, 621, 520)
        self.jar_front = self.table.crop(jar)
        front_mask = Image.new('L', self.jar_front.size)
        ImageDraw.Draw(front_mask).polygon(((7, 0), (34, 9), (93, 14), (120, 15),
                                          (178, 10), (204, 1), (212, 35),
                                          (212, 196), (180, 209), (29, 209),
                                          (0, 194), (0, 36)), fill=255)
        self.jar_layer = jar[:2], front_mask.filter(ImageFilter.GaussianBlur(.8))
        # Reuse the established kitchen light when a hand moves close to the mat.
        self.shadow = Image.new('L', (210, 64))
        ImageDraw.Draw(self.shadow).ellipse((24, 14, 186, 53), fill=74)
        self.shadow = self.shadow.filter(ImageFilter.GaussianBlur(11))

    def shadow_at(self, im, xy):
        im.paste('#5f361a', (round(xy[0]-105), round(xy[1]-32),
                             round(xy[0]+105), round(xy[1]+32)), self.shadow)

    def choose(self, time):
        im = self.table.copy()
        put(im, self.lid, (513, 288))
        hand = path(time, (
            (4.05, (389, 279, -12)), (4.92, (465, 284, -14)),
            (5.46, (505, 302, -19)), (6.15, (510, 307, -20)),
            (7.06, (509, 306, -20)), (9.11, (503, 298, -17)),
            (9.48, (-35, 326, -5)),
        ))
        put(im, self.pointing, hand[:2], hand[2])
        return im

    def open_jar(self, time):
        im = self.table.copy()
        grip = path(time, (
            (15.15, (1370, 37, 24)), (15.72, (800, 244, 22)),
            (16.26, (579, 269, 30)), (16.59, (575, 268, 36)),
            (17.00, (578, 238, 38)), (17.72, (754, 137, 35)),
            (18.50, (1350, 40, 23)),
        ))
        if time < 16.59:
            lid = (513, 288, 0)
        else:
            lid = (grip[0]-62, grip[1]+20, (grip[2]-36)*.31)
        if lid[0] < 700:
            self.shadow_at(im, (lid[0], 423))
        put(im, self.lid, lid[:2], lid[2])
        put(im, self.staff, grip[:2], grip[2])
        return im

    def pass_spoon(self, time):
        im = self.table.copy()
        move = path(time, (
            (18.45, (1380, 55, 23)), (18.87, (845, 179, 13)),
            (19.29, (642, 270, 15)), (19.72, (648, 298, 15)),
            (20.13, (651, 237, -5)), (20.72, (648, 242, -14)),
            (21.15, (577, 261, -13)), (21.57, (572, 260, -12)),
            (21.79, (519, 275, -13)), (22.42, (180, 373, -19)),
            (23.38, (-184, 449, -27)),
        ))
        handoff = path(time, (
            (20.55, (-92, 396, -9)), (20.94, (380, 330, 12)),
            (21.37, (523, 270, 19)), (21.57, (526, 272, 20)),
        ))
        self.shadow_at(im, (max(135, move[0]-92), 387))
        put(im, self.empty_spoon if time < 19.83 else self.spoon, move[:2], move[2])
        if 19.32 <= time <= 19.98:
            # When it dips, the front rim briefly hides the bowl.
            xy, mask = self.jar_layer
            im.paste(self.jar_front, xy, mask)
        employee = move if time <= 21.57 else path(time, (
            (21.57, (572, 260, -12)), (21.92, (608, 243, 10)),
            (22.31, (1040, -116, 28)), (22.61, (820, 42, 22)),
            (23.18, (575, 268, 3)), (23.36, (572, 254, 5)),
        ))
        if time >= 22.31:
            lid = (513, 288) if time >= 23.18 else (employee[0]-62, employee[1]+20)
            put(im, self.lid, lid)
        put(im, self.staff, employee[:2], employee[2]+30)
        receiver = handoff if time <= 21.57 else (move[0]-46, move[1]+12, 20)
        put(im, self.receive, receiver[:2], receiver[2])
        return im

    def frame(self, time):
        if time < 4.05:
            im = self.poses['point'].copy()
            label(im, (28, 24), '시식 상황 재구성', True)
            return im
        if 9.10 <= time < 11.55:
            # Her eyes stay on the jar as she explains the first taste.
            return self.poses['point'].copy()
        if time < 15.15:
            # The two flavours belong to the two jars. Stay in the same place.
            return self.choose(time)
        if time < 18.48:
            return self.open_jar(time)
        if time < 23.38:
            return self.pass_spoon(time)
        if time < 30.8:
            return self.face.frame(time - 23.38)
        return self.poses['finish'].copy()


def render(folder, audio, cues_path, output):
    timeline = json.loads(cues_path.read_text(encoding='utf-8'))
    anchors = timeline['anchors']
    if len(anchors) != len(REFERENCE) or any(a >= b for a, b in zip(anchors, anchors[1:])):
        raise ValueError('The narration cues must be ordered and cover every action.')
    scene = Scene(folder)
    frames = round(anchors[-1] * FPS)
    command = [
        'ffmpeg', '-hide_banner', '-loglevel', 'error', '-xerror', '-y',
        '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', 'pipe:0',
        '-i', str(audio), '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'libx264',
        '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', '-colorspace', 'bt709',
        '-color_primaries', 'bt709', '-color_trc', 'bt709', '-c:a', 'aac', '-b:a', '160k',
        '-movflags', '+faststart', '-af', 'apad', '-shortest', str(output),
    ]
    with subprocess.Popen(command, stdin=subprocess.PIPE, cwd=folder) as encoder:
        for frame in range(frames):
            time = frame / FPS
            picture = scene.frame(float(np.interp(time, anchors, REFERENCE)))
            caption(picture, timeline['captions'], time)
            encoder.stdin.write(picture.tobytes())
        encoder.stdin.close()
        if encoder.wait():
            raise RuntimeError('FFmpeg did not finish the tasting segment.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('folder', type=Path)
    parser.add_argument('audio', type=Path)
    parser.add_argument('cues', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    render(args.folder, args.audio, args.cues, args.output)
