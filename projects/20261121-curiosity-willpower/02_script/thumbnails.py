"""의지력 편 썸네일 A/B/C (1280×720) + 휴대폰 크기 미리보기. prompts/thumbnail.md: 큰 두 줄·강조 한 낱말·오른쪽 아래 재생 시간 자리 비움.
python thumbnails.py <원화 조각 폴더> <출력 폴더>"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
HERE = Path(__file__).resolve().parent
FONTS = (HERE.parents[2] / "ytflow" / "assets" / "fonts").as_uri()
V = {   # v16 최종본에 맞춤 (2026-11-21 사용자: "썸네일 만들어주시고") — 영상의 첫 장면·결론과 같은 말
 "A": dict(img="kitchen_tl", side="left", css="background-size:1380px auto;background-position:330px 35%;background-repeat:no-repeat",
           lines=["밤 11시에", "<b>무너지는</b> 이유"], small="다이어트 2주째, 냉장고 앞",
           why="영상 첫 문장('밤 11시 냉장고 앞에서 무너진 적')과 같은 장면 — 다이어트 중인 사람이 '내 얘기'로 알아봄. 제목(의지력 질문)은 원인 쪽, 썸네일은 상황 쪽으로 서로 보완."),
 "B": dict(img="lab_tl", side="right", css="background-size:112%;background-position:0% 50%",
           lines=["쿠키 참으면", "먼저 <b>포기</b>했다"], small="1998년 실험",
           why="영상의 핵심 실험 한 장면·한 결과. 제목과 겹치지 않고 '정말?'을 남김."),
 "C": dict(img="kitchen_tr", side="left", css="background-size:1400px auto;background-position:260px 55%;background-repeat:no-repeat",
           lines=["의지력 탓은", "<b>반만</b> 맞다"], small="참을수록 닳는다는 말",
           why="영상의 결론('반만 맞습니다')을 한 줄로 — 치킨으로 가는 손이 '그럼 나머지 반은?'을 부름."),
}
HTML = """<!doctype html><html><head><meta charset=utf-8><style>
@font-face{font-family:BH;src:url(F/BlackHanSans-Regular.ttf)}@font-face{font-family:NGX;src:url(F/NanumGothic-ExtraBold.ttf)}
body{margin:0;width:1280px;height:720px;overflow:hidden;background:#efe7da;font-family:BH;position:relative}
.img{position:absolute;inset:0;background-size:cover;background-position:65% 40%}
.panel{position:absolute;left:0;top:0;bottom:0;width:640px;background:linear-gradient(90deg,rgba(239,231,218,.98) 70%,rgba(239,231,218,0))}
.t{position:absolute;left:48px;top:170px;color:#2b2622;font-size:104px;line-height:1.12;letter-spacing:-2px;text-shadow:0 2px 0 #fff8}
.t b{color:#c8473a;font-weight:normal}
.R .panel{left:auto;right:0;background:linear-gradient(270deg,rgba(239,231,218,.98) 70%,rgba(239,231,218,0))}.R .t,.R .s{left:auto;right:56px;text-align:right}.R .tag{left:auto;right:52px;bottom:auto;top:40px}
.s{position:absolute;left:52px;top:96px;font:34px NGX;color:#8d8274}
.tag{position:absolute;left:52px;bottom:48px;font:24px NGX;color:#fff;background:rgba(20,18,16,.7);padding:6px 16px;border-radius:20px}
.bat{position:absolute;right:120px;top:210px;width:380px;height:170px;border:16px solid #2b2622;border-radius:26px}
.bat i{position:absolute;left:14px;top:14px;bottom:14px;width:22%;background:#c8473a;border-radius:6px}
.bat:after{content:'';position:absolute;right:-48px;top:44px;width:28px;height:52px;background:#2b2622;border-radius:0 8px 8px 0}
.q{position:absolute;right:250px;top:420px;font-size:150px;color:#d9a441}
</style></head><body>BODY</body></html>"""


def main(art, out):
    art, out = Path(art), Path(out); out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        br = pw.chromium.launch(); pg = br.new_page(viewport={"width": 1280, "height": 720})
        for k, v in V.items():
            body = ""
            if v["img"]:
                body += f'<div class=img style="background-image:url({(art / (v["img"] + ".jpg")).as_uri()});{v.get("css", "")}"></div><div class=panel></div>'
            else:
                body += '<div class=bat><i></i></div><div class=q>?</div>'
            body += f'<div class=s>{v["small"]}</div><div class=t>{"<br>".join(v["lines"])}</div>'
            f = out / "_t.html"; f.write_text(HTML.replace("F/", FONTS + "/").replace("BODY", f'<div class="{"R" if v["side"] == "right" else "L"}">{body}</div>'), encoding="utf-8")
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
