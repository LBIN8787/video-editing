"""2장 '막대기와 뱀 → 연기 감지기 → 결론' 한 판 시험 (docs/73 진행 문법 + 3D).
한 장 = 한 판: 숲길(A) → 두 길(B) → 르두의 말(Q) → 감지기(C) → 저울 → 전체로 물러남(D). 지우지 않고 카메라가 이동."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
L = json.load(open(HERE / "assets/vo/lines.json", encoding="utf-8"))
END = round(L[-1]["start"] + L[-1]["dur"] + 1.4, 2)
caps = "".join(f'<div class="clip cap" id="cap{x["i"]}" data-start="{x["start"] + .05:.2f}" data-duration="{x["dur"] - .25:.2f}" data-track-index="20"><span>{x["text"]}</span></div>' for x in L)
aud = "".join(f'<audio id="vo{x["i"]}" class="clip" src="assets/vo/{x["file"]}" data-start="{x["start"]}" data-duration="{x["dur"]}" data-track-index="7" data-volume="1"></audio>' for x in L)
SFX = [("pencil.wav", 1.0, .9, .12), ("click-soft.mp3", 8.6, .4, .25), ("impact-bass-2.mp3", 14.4, 1.2, .25), ("whoosh.mp3", 17.3, .57, .22),
       ("pencil.wav", 19.0, 1.2, .12), ("whoosh-short.mp3", 24.7, .57, .25), ("pop.mp3", 27.7, .5, .2), ("whoosh.mp3", 29.4, .57, .22),
       ("pencil.wav", 34.0, 1.0, .12), ("whoosh.mp3", 39.6, .57, .22), ("pop.mp3", 42.6, .5, .22), ("whoosh-short.mp3", 48.8, .57, .2),
       ("chime.mp3", 50.9, 1.2, .28), ("whoosh-cinematic.mp3", 55.2, 1.4, .2), ("click.mp3", 58.6, .4, .25), ("impact-bass-2.mp3", 61.6, 1.2, .25),
       ("click.mp3", 67.5, .4, .3), ("whoosh-cinematic.mp3", 70.2, 1.4, .2), ("pencil.wav", 75.0, .6, .12), ("pop.mp3", 76.5, .5, .2)]
aud += "".join(f'<audio id="sx{k}" class="clip" src="assets/sfx/{f}" data-start="{t}" data-duration="{d}" data-track-index="{8 + k % 3}" data-volume="{v}"></audio>' for k, (f, t, d, v) in enumerate(SFX))
html = (HERE / "template.tpl").read_text(encoding="utf-8").replace("%END%", str(END)).replace("%CAPS%", caps).replace("%AUD%", aud)
(HERE / "index.html").write_text(html, encoding="utf-8")
print("END", END)
