"""리만가설 편 썸네일 A/B/C (1280×720) + 휴대폰 크기 미리보기. 유행 20년 편 thumbnails.py 틀을 가져옴.
prompts/thumbnail.md: 큰 두 줄·강조 한 낱말·오른쪽 아래 재생 시간 자리 비움. 지금의 고리 'AI·리만가설'을 큰 글씨에.
그림은 영상 속 모양(머리와 물음표·린 검사기·리만 원문 쪽지)을 벡터로 다시 그림 — 프레임 조각은 자막·배경 띠가 섞여 버림: python thumbnails.py - <출력 폴더>
'풀렸다' 단정 금지(팩트시트 '쓰지 않는 것') — 물음표·'맞다는데'로."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
HERE = Path(__file__).resolve().parent
FONTS = (HERE.parents[2] / "ytflow" / "assets" / "fonts").as_uri()
V = {
 "A": dict(img=None, side="left", art='<svg class=art style="right:40px;top:60px" width="520" height="600" viewBox="0 0 520 600"><path d="M120,600 L120,470 C40,420 20,330 30,250 C45,120 150,40 270,40 C390,40 470,120 470,240 L500,330 L460,340 L460,420 C460,450 430,460 380,455 L380,600" fill="none" stroke="#1d2024" stroke-width="9"/><text x="215" y="340" font-family="BH" font-size="190" fill="#e2552b">?</text></svg>',
           lines=["AI 리만가설 증명", "아무도 <b>못 읽는다</b>"], small="167년 난제 · 설명만 25만 쪽",
           why="제목의 질문 + 4장(사람이 읽을 설명이 25만 쪽) — 지금의 고리(11-20 AI 리만가설 발표)를 앞에."),
 "B": dict(img=None, side="right", art='<div class=art style="left:50px;top:90px;width:430px;height:540px;border:7px solid #1d2024;border-radius:14px;background:#f3eedf;padding:26px 30px;box-sizing:border-box;font:26px NGX;color:#6f747b;line-height:1.75">'+"".join(f"<div>{w} …<span style=float:right;color:#2e9b57>✓</span></div>" for w in ["theorem","lemma","have","exact","simp","intro","theorem","lemma"])+'</div>',
           lines=["컴퓨터는 <b>맞다</b>는데", "이유는 아무도 몰라"], small="1,700만 줄 · 리만가설",
           why="3장(린 검사기 1,700만 줄 통과) — 영상의 통찰 '맞다 ≠ 이해했다' 그대로."),
 "C": dict(img=None, side="right", art='<div class=art style="left:40px;top:200px;width:560px;height:330px;background:#f3eedf;box-shadow:0 8px 24px #0002;transform:rotate(-3deg);padding:34px;box-sizing:border-box;font:34px NP;color:#1d2024;line-height:1.6">Ueber die Anzahl der Primzahlen …<br>… und es ist <u style=text-decoration-color:#e2552b>sehr wahrscheinlich</u>,<br>dass alle Wurzeln reell sind.<div style="position:absolute;right:30px;bottom:34px;border:6px solid #e2552b;color:#e2552b;font:44px BH;padding:4px 18px;transform:rotate(-8deg)">컴퓨터 검사 통과?</div></div>',
           lines=["167년 전 한 문장", "AI가 <b>풀었나?</b>"], small="리만, 1859 · '매우 그럴듯하다'",
           why="첫 장면·끝 장면(리만 원문 문장 위 '컴퓨터 검사 통과' 도장) — 수미상관. 단정 대신 물음."),
}
HTML = """<!doctype html><html><head><meta charset=utf-8><style>
@font-face{font-family:BH;src:url(F/BlackHanSans-Regular.ttf)}@font-face{font-family:NP;src:url(F/NanumPenScript-Regular.ttf)}@font-face{font-family:NGX;src:url(F/NanumGothic-ExtraBold.ttf)}
body{margin:0;width:1280px;height:720px;overflow:hidden;background:#e8e6e1;font-family:BH;position:relative}
.art{position:absolute}
.panel{display:none}
.t{position:absolute;left:48px;top:220px;color:#1d2024;font-size:92px;line-height:1.14;letter-spacing:-2px}
.t b{color:#e2552b;font-weight:normal}
.R .panel{left:auto;right:0;background:linear-gradient(270deg,rgba(232,230,225,.98) 72%,rgba(232,230,225,0))}.R .t,.R .s{left:auto;right:56px;text-align:right}
.s{position:absolute;left:52px;top:120px;font:34px NGX;color:#6f747b}
</style></head><body>BODY</body></html>"""


def main(art, out):
    art, out = Path(art), Path(out); out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        br = pw.chromium.launch(); pg = br.new_page(viewport={"width": 1280, "height": 720})
        for k, v in V.items():
            body = v["art"]
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


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
