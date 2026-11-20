"""대본 v3(script_v3.md) → 장면표 v3.json. 이야기 = 삽화 칸(art), 설명 = 모션그래픽, 증거 = 실제 사진·이름 카드, 마디 = 무음 검은 화면.
원화가 ARTDIR/<시트>_<칸>.jpg 로 있으면 쓰고, 없으면 '원화 대기' 판. python build_v3.py [ARTDIR]"""
import json, re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ART = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE
s = (HERE / "script_v3.md").read_text(encoding="utf-8").split("---", 1)[1]
P = [re.sub(r"\s*\[[^\]]*\]", "", l[2:]).strip() for l in s.split("\n") if l.startswith(("●", "○"))]
orders = (HERE / "art_orders.md").read_text(encoding="utf-8")
def desc(sheet, q):
    blk = orders.split(f"## {sheet}.png", 1)[1].split("\n## ", 1)[0]
    lab = {"tl": "Top left", "tr": "Top right", "bl": "Bottom left", "br": "Bottom right"}[q]
    m = re.search(lab + r":\s*(.+?)(?= (?:Top|Bottom) (?:left|right):|$)", blk.replace("\n", " "))
    return (m.group(1).strip() if m else "")[:220]
KO = {("night1", "tl"): "이불 속 지우, 화면 불빛에 비친 얼굴과 엄지", ("night1", "tr"): "휴대폰을 쥔 손, 엄지가 위로 넘기는 중",
      ("night1", "bl"): "베개에 볼을 묻고 무료해진 지우", ("night1", "br"): "머리맡 휴대폰으로 뻗는 손",
      ("room", "tl"): "하얀 빈 방, 의자 하나·작은 책상 하나·벽시계", ("room", "tr"): "책상 위 빨간 버튼 하나", ("room", "bl"): "의자에 앉은 참가자 뒷모습",
      ("room", "br"): "버튼 바로 위에 멈춘 손가락", ("lab", "tl"): "2024년 실험실, 모니터 앞 학생", ("lab", "tr"): "위에서 본 지우의 침대 — 밤을 되감기",
      ("lab", "bl"): "문이 늘어선 긴 복도, 문을 열다 다음 문으로 가는 지우", ("lab", "br"): "침대에서 화면을 보는 지우, 머리 위 빈 공간(생각 풍선)",
      ("night2", "tl"): "화면 위에서 멈춘 엄지, 생각하는 지우", ("night2", "tr"): "벽에 기대 한 편에 빠져든 지우", ("night2", "bl"): "창가에서 기지개, 물 한 잔",
      ("night2", "br"): "머리맡 수첩의 세 줄", ("ending", "tl"): "엎어 둔 휴대폰과 물컵", ("ending", "tr"): "누운 지우 위로 번지는 상상 속 바다",
      ("ending", "bl"): "조용한 방, 쉬는 지우", ("ending", "br"): "휴대폰 없이 이불 위에 놓인 손"}
def A(sheet, q, pan=0):
    return {"sheet": sheet, "q": q, "pan": pan, "ok": (ART / f"{sheet}_{q}.jpg").exists(), "desc": KO.get((sheet, q)) or desc(sheet, q)}
M = lambda line, kicker="", size=72, sec=2.8: {"kind": "mg", "mg": "madi", "line": line, "kicker": kicker, "size": size, "silent": sec}
G = lambda **k: {"kind": "mg", **k}
SRC_T = "Tam & Inzlicht (2024), J. Exp. Psychol.: General 153(10)"
SRC_W = "Wilson 외 (2014), Science 345(6192)"
seq = [
 M("새벽 한 시", "1"),
 (0, G(art=A("night1", "tl"), mg="none", stamp="새벽 1:00")),
 (1, G(art=A("night1", "tr", 1), mg="none")),
 (2, G(art=A("night1", "bl"), mg="elapsed", kw=[["사십 분이", "볼 게 없네"]])),
 (3, G(mg="kinetic", words=[["볼 게 이렇게 많은데,", 1.6], ["왜 넘길수록 더 지루할까?", 2.4]], pad=[0, 0.9])),
 M("지루함을 두려워하는 사람들", "2"),
 (4, G(mg="photo", photo="russell.jpg", photoOk=(ART / "russell.jpg").exists(), name="버트런드 러셀", who="철학자 · 『행복의 정복』 (1930)",
       quote="우리는 조상들보다 덜 지루하지만,<br>지루함을 더 두려워한다", kw=[["우리는 조상들보다"]])),
 (5, G(mg="term", term="권태사회", sub="『트렌드 코리아 2027』 — 즐길 거리가 넘칠수록 더 자주 지루해지는 사회", kw=[["권태사회"]])),
 (6, G(mg="kin2", words=[["사람은 지루함을", 0.2], ["얼마나 싫어할까?", 1.0]], pad=[0, 0.6])),
 M("아무것도 없는 방", "3"),
 (7, G(art=A("room", "tl", 1), mg="namecard", name="Wilson · Gilbert 외 (2014)", who="버지니아대 · 하버드대 — Science", kw=[["2014년"]])),
 (8, G(art=A("room", "tr"), mg="none")),
 (9, G(mg="dots", head="15분, 혼자 생각만 하는 동안 버튼을 누른 사람", groups=[{"label": "남자", "total": 18, "on": 12, "cols": 6}, {"label": "여자", "total": 24, "on": 6, "cols": 8}],
       counter=190, counterLabel="한 사람이 누른 횟수", kw=[["남자 참가자는", "여자 참가자는", "190번"]], src=SRC_W)),
 (10, G(art=A("room", "br"), mg="kin2", words=[["다시는 받기 싫다던 아픔이,", 0.2], ["빈 시간보다 나았다", 1.4]], pad=[0, 0.8])),
 (11, G(art=A("night1", "br"), mg="none")),
 M("한 편과 일곱 편", "4"),
 (12, G(mg="skips", head="지루하면 더 넘길까? — 10분 동안 마음대로 넘기기", rows=[["재미있는 영상 묶음", 4], ["지루한 영상 묶음", 8]], kw=[["지루할수록", "재미있는 묶음을", "두 배쯤"]], src=SRC_T)),
 (13, G(art=A("lab", "tl"), mg="namecard", name="케이티 탐 · 마이클 인즐리히트", who="토론토대 (2024) — 「Fast-Forward to Boredom」", kw=[["케이티 탐"]])),
 (14, G(mg="plan2", kw=[["서른다섯 번", "물었습니다"]])),
 (15, G(mg="result", src=SRC_T, kw=[["넘길 수 있었던 쪽", "만족도도", "빠져든", "남는 것도", "유튜브에서"]])),
 (16, G(mg="kin2", words=[["지루해서 넘겼는데,", 0.1], ["넘겨서 더 지루해졌다", 1.3]], pad=[0, 0.6])),
 M("문만 여는 밤", "5"),
 (17, G(art=A("lab", "tr"), mg="none")),
 (18, G(art=A("night1", "tr"), mg="immerse", resets=[0.55, 0.72, 0.86])),
 (19, G(art=A("lab", "br"), mg="bubble", bubble="다음 게 더 재밌지 않을까?", term2="", term2sub="", kw=[["다음 게", "비교됩니다"]])),
 (20, G(art=A("lab", "bl", 1), mg="none")),
 M("영상의 즐거움은 넘기는 데서가 아니라,<br><span class='y'>빠져드는 데서</span> 온다", "탐 · 인즐리히트 (2024)", 60, 3.6),
 (21, G(mg="chips", chips=["결과가 분명했던 건 주로 대학생", "다른 조건에선 엇갈리기도"], kw=[["대학생들", "엇갈리기도"]])),
 M("다음 날 밤", "6"),
 (22, G(art=A("night2", "tl"), mg="none", stamp="새벽 1:00")),
 (23, G(art=A("night2", "tl"), mg="ask", head="① 묻기", opts=["별로라서?", "지루해서?"], kw=[["별로라서", "지루해서 넘기는"]])),
 (24, G(art=A("night2", "tr"), mg="chips", shade=False, head="② 머물기", chips=["처음 몇 초의 어색함만 지나면"], kw=[["처음 몇 초"]])),
 (25, G(art=A("night2", "bl"), mg="chips", shade=False, head="③ 나가기", chips=["물 한 잔", "기지개", "잠깐의 산책"], kw=[["물 한 잔", "기지개", "산책"]])),
 (26, G(art=A("night2", "br"), mg="notes", head="④ 챙기기", items=["다음 달 여행", "주말 약속", "요즘 빠진 취미"], kw=[["떠올리면", "빈 방", "확인했습니다"]])),
 M("다시, 새벽 한 시", "7"),
 (27, G(art=A("ending", "tr"), mg="none")),
 (28, G(mg="recap", words=[["묻기", "넘기기 전에"], ["머물기", "고른 것에"], ["나가기", "화면 밖으로"], ["챙기기", "빈 시간의 생각 하나"]], pad=[0, 0.6])),
 (29, G(art=A("ending", "bl"), mg="endcard", end="지금 보던 이야기에, <span class='y'>1분 더</span>", pad=[0, 3.0])),
]
scenes, used = [], set()
for k, item in enumerate(seq, 1):
    if isinstance(item, tuple):
        i, sc = item; used.add(i)
        sc = {**sc, "beats": [P[i]], "para": i}
    else:
        sc = {**item, "beats": []}
    sc["id"] = k
    scenes.append(sc)
assert used == set(range(len(P))), set(range(len(P))) - used
bad = [(sc["id"], w) for sc in scenes for i, b in enumerate(sc["beats"]) for w in (sc.get("kw") or [[]])[i] if w not in b]
assert not bad, bad
(HERE / "v3.json").write_text(json.dumps({"title": "볼 게 이렇게 많은데, 왜 넘길수록 더 지루할까?", "voice": "ko-KR-InJoonNeural", "rate": "+4%", "scenes": scenes},
                                         ensure_ascii=False, indent=1), encoding="utf-8")
print(len(scenes), "장면 ·", sum(1 for s in scenes if s.get("art")), "삽화 칸 ·", sum(1 for s in scenes if s.get("art", {}).get("ok")), "원화 있음")
