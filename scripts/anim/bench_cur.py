"""호기심 편에 벤치마크 반영 (docs/47, 사용자 11-18 "네, 반영해 주세요").

- 검은 화면 한 줄(심리학 고양이): 질문이 꺾이는 곳·결론 — 여백으로 무게를 준다.
- 어두운 바탕 번호 정리(심리학 고양이): 두 설명을 나란히 정리하고 '둘 다 일부만'.
- 실제 인물 사진(흑백, 퍼블릭 도메인): 처음 등장하는 연구자 — 이야기는 그림, 증거는 실제.
- (실험 칸 만화는 ep_curiosity_rest 의 Page)
"""
from pathlib import Path

from PIL import Image, ImageOps


def black(art: Path) -> None:
    p = art / "black.png"
    if not p.exists():
        Image.new("RGB", (1920, 1080), (10, 10, 12)).save(p)


def photo_card(src: Path, out: Path) -> bool:
    """흑백 사진 + 흰 테두리(옛 인화지 느낌). 원본이 없으면 False."""
    if not src.exists():
        return False
    im = ImageOps.grayscale(Image.open(src)).convert("RGB")
    im.thumbnail((700, 900))
    b = 22
    card = Image.new("RGB", (im.width + 2 * b, im.height + 2 * b + 30), (246, 242, 232))
    card.paste(im, (b, b))
    card.save(out)
    return True


def apply(f, A, refs: Path):
    art = f.art
    black(art)
    W = "#f3efe6"
    k = f.set("blk", "black.png", focus=(960, 540, 1.0))

    def line(tid, text, size=72, y=500, color=W):
        k.text(tid, text, 960, y, size=size, color=color, font="serif", rot=0, shadow=False)

    line("b1", "정말 그럴까?", 92)
    line("b2a", "① 비율 — 케이크가 커질수록 '올해' 조각이 얇아 보인다", 50, 330)
    line("b2b", "② 기억 — 새로 남은 장면이 많을수록 길게 기억된다", 50, 440)
    line("b2c", "둘 다 수수께끼의 일부만 — 아직 정설은 없다", 54, 600, "#e6b85c")
    line("b3", "올해의 끝은, 조금 더 길게 기억되지 않을까요?", 64)

    # (a) 꺾이는 질문
    t = f.cue("그런데", after=221)
    f._show(t, "blk", "cut", 0, "lect")
    f._enter(t + .2, "b1", "write", .8)
    t2 = f.cue("자네의", after=225)
    f._show(t2, "lect", "cut", 0, "blk")
    f._leave(t2, "b1", "fade", .1)
    f._leave(t2, "lq", "fade", .01)
    # (b) 두 설명 정리
    t = f.cue("그렇다고", after=484)
    f._show(t, "blk", "dissolve", .6, "hall")
    f._enter(f.cue("비율로", after=t), "b2a", "write", 1.2)
    f._enter(f.cue("새로운", after=t), "b2b", "write", 1.2)
    f._enter(f.cue("일부만", after=t) - .4, "b2c", "write", 1.0)
    t2 = f.cue("다만", after=501)
    for i in ("b2a", "b2b", "b2c"):
        f._leave(t2, i, "fade", .3)
    f._show(t2, "hall", "dissolve", .6, "blk")
    # (c) 결론 한 줄
    t = f.cue("올해의", after=588)
    f._show(t - .2, "blk", "dissolve", .9, "autumn")
    f._enter(t + .4, "b3", "write", 1.6)

    # 실제 인물 사진 (처음 등장할 때)
    for key, sid, word, after, name, x, y in [
        ("janet", "paris", "자네는", 3, "폴 자네 (1823–1899) · 프랑스 철학자", 1440, 330),
        ("james", "jroom", "윌리엄", 160, "윌리엄 제임스 (1842–1910) · 미국 심리학자", 1180, 380),
    ]:
        if not photo_card(refs / f"{key}.jpg", art / f"photo_{key}.png"):
            print(f"[bench] 사진 없음: {key} — 건너뜀")
            continue
        s = [x_ for x_ in f.sets if x_.id == sid][0]
        s.prop(f"ph_{key}", f"photo_{key}", x, y, 330, z=9, rot=3)
        s.text(f"phn_{key}", name, x, y + 255, size=32, color="#2b2118", font="gothic", rot=0, card=True)
        t = f.cue(word, after=after)
        f._enter(t, f"ph_{key}", "drop", .7)
        f._enter(t + .3, f"phn_{key}", "write", .6)
        f._sound(t + .6, "click-soft", .2)
        f._leave(t + 4.5, f"ph_{key}", "fade", .5)
        f._leave(t + 4.5, f"phn_{key}", "fade", .5)
