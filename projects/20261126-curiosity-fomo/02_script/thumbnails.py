"""포모 편 썸네일 A/B/C (1280×720) + 휴대폰 크기 미리보기 — 유행 20년 편 thumbnails.py 를 가져와 V 만 바꿈.
prompts/thumbnail.md: 큰 두 줄·강조 한 낱말·오른쪽 아래 재생 시간 자리 비움. 문구는 영상 속 질문·장면·숫자와 같은 말.
python thumbnails.py <원화 조각 폴더> <출력 폴더>"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
HERE = Path(__file__).resolve().parent
FONTS = (HERE.parents[2] / "ytflow" / "assets" / "fonts").as_uri()
V = {
 "A": dict(img="night_alone", side="left", css="background-size:1280px auto;background-position:430px 0;background-repeat:no-repeat",
           lines=["나만 빼고", "다 <b>재밌게</b> 사나?"], small="금요일 밤 11시",
           why="첫 장면(금요일 밤 이불 속 지우) + 제목의 질문 — 시청자가 겪어 본 바로 그 순간."),
 "B": dict(img="ubc_bubbles", side="right", css="background-size:1280px auto;background-position:-470px 0;background-repeat:no-repeat",
           lines=["신입생 <b>48%</b>", "'남들이 더 많다'"], small="1,099명에게 물었더니",
           why="3장의 반전 숫자(남들이 나보다 친구가 많다고 믿은 학생 48% vs 반대 31%)."),
 "C": dict(img="cafeteria", side="left", css="background-size:1280px auto;background-position:470px 0;background-repeat:no-repeat",
           lines=["남의 삶 말고", "<b>장면</b>만 보인다"], small="포모의 정체",
           why="4장의 답(식당 창 안만 보이고 기숙사 방은 안 보임) — 결론과 같은 말."),
}
HTML = """<!doctype html><html><head><meta charset=utf-8><style>
@font-face{font-family:BH;src:url(F/BlackHanSans-Regular.ttf)}@font-face{font-family:NGX;src:url(F/NanumGothic-ExtraBold.ttf)}
body{margin:0;width:1280px;height:720px;overflow:hidden;background:#efe7da;font-family:BH;position:relative}
.img{position:absolute;inset:0;background-size:cover;background-position:65% 40%}
.panel{position:absolute;left:0;top:0;bottom:0;width:640px;background:linear-gradient(90deg,rgba(239,231,218,.98) 70%,rgba(239,231,218,0))}
.t{position:absolute;left:48px;top:170px;color:#2b2622;font-size:96px;line-height:1.12;letter-spacing:-2px;text-shadow:0 2px 0 #fff8}
.t b{color:#c8473a;font-weight:normal}
.R .panel{left:auto;right:0;background:linear-gradient(270deg,rgba(239,231,218,.98) 70%,rgba(239,231,218,0))}.R .t,.R .s{left:auto;right:56px;text-align:right}
.s{position:absolute;left:52px;top:96px;font:34px NGX;color:#8d8274}
</style></head><body>BODY</body></html>"""


def main(art, out):
    art, out = Path(art), Path(out); out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        br = pw.chromium.launch(); pg = br.new_page(viewport={"width": 1280, "height": 720})
        for k, v in V.items():
            body = f'<div class=img style="background-image:url({(art / (v["img"] + ".jpg")).as_uri()});{v.get("css", "")}"></div><div class=panel></div>'
            body += f'<div class=s>{v["small"]}</div><div class=t>{"<br>".join(v["lines"])}</div>'
            f = out / "_t.html"
            f.write_text(HTML.replace("F/", FONTS + "/").replace("BODY", f'<div class="{"R" if v["side"] == "right" else "L"}">{body}</div>'), encoding="utf-8")
            pg.goto(f.as_uri()); pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(300); pg.screenshot(path=str(out / f"thumbnail_{k}.png"))
        br.close()
    from PIL import Image   # 미리보기: 400px · 휴대폰 목록 168px
    sheet = Image.new("RGB", (3 * 420, 420), "white")
    for i, k in enumerate(V):
        im = Image.open(out / f"thumbnail_{k}.png").convert("RGB")
        sheet.paste(im.resize((400, 225)), (i * 420 + 10, 10)); sheet.paste(im.resize((168, 94)), (i * 420 + 10, 250))
    sheet.save(out / "thumbnail_preview.png")
    (HERE.parent / "05_edit").mkdir(exist_ok=True)
    (HERE.parent / "05_edit" / "thumbnails.md").write_text("# 썸네일 A/B/C\n\n" + "\n".join(
        f"- **{k}** · {' / '.join(l.replace('<b>', '').replace('</b>', '') for l in v['lines'])} — {v['why']}" for k, v in V.items()) + "\n", encoding="utf-8")


main(*sys.argv[1:3])
