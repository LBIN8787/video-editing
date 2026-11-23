"""지우 칸 모아 보기: 기준판(왼쪽) + 이 편에서 지우가 나오는 칸 전부 → Drive art/jiwoo_lineup.jpg. python make_lineup.py <조각 폴더>"""
import os, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
P = Path(sys.argv[1]); D = Path(os.environ["YTFLOW_DRIVE"]); out = D / "영상" / Path(__file__).resolve().parents[1].name / "art" / "jiwoo_lineup.jpg"
J = ["room1_tl", "room1_tr", "room1_bl", "room2_tl", "room2_tr", "room2_br", "room3_tl", "room3_tr", "room4_bl", "room4_br",
     "room5_tl", "room5_tr", "room5_br", "room6_tl", "room6_bl", "room6_br"]
board = Image.open(D / "refs/ch-knowledge/jiwoo_board.png").convert("RGB"); bh = 1290; board = board.resize((int(board.width * bh / board.height), bh))
cw, ch, cols = 480, 270, 4; rows = (len(J) + cols - 1) // cols
sheet = Image.new("RGB", (board.width + 20 + cols * (cw + 6), max(bh, rows * (ch + 52))), "white"); sheet.paste(board, (0, 0))
dr = ImageDraw.Draw(sheet); f = ImageFont.truetype("arial.ttf", 26)
for i, n in enumerate(J):
    x = board.width + 20 + (i % cols) * (cw + 6); y = (i // cols) * (ch + 52)
    sheet.paste(Image.open(P / f"{n}.jpg").resize((cw, ch)), (x, y)); dr.text((x + 6, y + ch + 8), n, fill="black", font=f)
sheet.save(out, quality=88); print(out, sheet.size)
