"""소현세자의 죽음 — 본편 (대본 v2 전체) HyperFrames 생성.
연출 기준: docs/76 레퍼런스 실측(멈추는 순간 없음·문장마다 화면 교체·분위기 층·결정적 순간에만 큰 글자·지도로 위치 잡기)
+ 한 편의 닫힌 어휘: 재현 그림(시차·촛불·먼지) / 실록 종이 / 사건 파일(단서 칸) / 증거판 / 지도 / 가계도 / 판정표.
사용자: "대사가 너무 느려요" → +8%, 쉼 짧게."""
import asyncio, hashlib, json, re, shutil, subprocess, sys
from pathlib import Path
import edge_tts
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
import eng2 as eng
from eng2 import HTML, JS, SFX, DEFS, nid, clip, shot, text, typewriter, stamp, shake, flash, whip, leak, ink, W, H
import geo

EP = Path(r"G:\내 드라이브\ytflow\영상\20261126-history-sohyeon")
HF = EP / "hf_v3"; AS = HF / "assets"; (AS / "fonts").mkdir(parents=True, exist_ok=True)
eng.AS = AS
WORK = Path(__file__).parent / "fullwork"; WORK.mkdir(exist_ok=True)
VOICE, RATE, QRATE = "ko-KR-InJoonNeural", "+8%", "-2%"

# ------------------------------------------------------------------ 대본 v2 (문장 = 박자). q=인용(느리게, 자막 없음), ch=장 첫 박자(앞에 사건 파일 카드)
S = []
def b(k, t, pause=0.25, sub=True, q=False, ch=None):
    S.append(dict(k=k, t=t, pause=pause, sub=sub and not q, q=q, ch=ch))

# 0 콜드 오픈
b("o0", "1645년 4월, 창경궁 환경당.", .35)
b("o1", "촛불 아래, 세상을 떠난 사람의 몸을 씻기고 옷을 입히는 염습이 시작됩니다.")
b("o2", "누워 있는 사람은 조선의 왕세자. 서른셋.", .3)
b("o3", "그 방에 들어갔던 종친 집안 사람 하나가, 훗날 이렇게 전했습니다.", .5)
b("o4", "온몸이 전부 검은빛이었고, 이목구비의 일곱 구멍에서는 모두 선혈이 흘러나왔다.", .3, q=True)
b("o5", "마치 약물에 중독되어 죽은 사람과 같았다.", .7, q=True)
b("o6", "나라의 공식 역사, 조선왕조실록에 남은 문장입니다.", .2)
b("o7", "그리고 이 죽음은, 380년이 넘도록 풀리지 않았습니다.", 1.0, sub=False)
# 1 사건 개요
b("c1_0", "사건을 먼저 정리해 보겠습니다.", .15)
b("c1_1", "죽은 사람. 소현세자. 왕 인조의 맏아들, 다음 왕이 될 사람이었습니다.", .15)
b("c1_2", "때. 1645년 음력 4월 26일. 곳. 창경궁 환경당.", .15, sub=False)
b("c1_3", "청나라에서 8년을 지내고 돌아온 지 두 달 남짓. 4월 23일에 앓아눕고, 나흘째 되던 날 숨을 거둡니다.", .35)
b("c1_4", "공식 기록이 말하는 것은 여기까지, 병을 얻어 죽었다는 것입니다.", .2)
b("c1_5", "그런데 같은 실록이, 저 이상한 얼굴을 적어 두었습니다.", .4)
b("c1_6", "세자는 병으로 죽었을까요, 아니면 누군가에게 죽임을 당했을까요.", .3)
b("c1_7", "단서를 하나씩 보겠습니다.", 1.3)
# 2 단서 1
b("c2_0", "실록의 문장을 다시 읽어 보겠습니다.", .3, ch=1)
b("c2_1", "검은 천으로 얼굴 반쪽만 덮어 놓았으나, 곁에 있는 사람도 그 얼굴빛을 알아볼 수 없어서, 마치 약물에 중독되어 죽은 사람과 같았다.", .6, q=True)
b("c2_2", "이 문장에서 꼭 짚어 둘 것이 두 가지 있습니다.", .2)
b("c2_3", "하나. 이것은 소문을 모은 야사가 아니라, 나라가 펴낸 공식 역사에 실린 증언입니다.", .3)
b("c2_4", "둘. 그런데 이 문장은 '독을 먹었다'고 하지 않습니다.", .2)
b("c2_5", "'중독된 사람과 같았다', 그렇게 보였다고 할 뿐입니다.", .4)
b("c2_6", "본 사람은 있습니다.", .15)
b("c2_7", "하지만 본 것이 무엇 때문이었는지는, 이 단서 하나로는 알 수 없습니다.", .3)
b("c2_8", "그렇다면 이 사람은 누구였고, 누가 그를 위협으로 여겼을까요.", 1.3)
# 3 인물 기록
b("c3_0", "8년 전, 1637년 정월. 한강 남쪽 나루 삼전도.", .2, ch="P")
b("c3_1", "남한산성에서 버티던 인조가 청나라 황제 앞에 무릎을 꿇습니다.", .2)
b("c3_2", "그 곁에 스물다섯의 세자가 있었습니다.", .2)
b("c3_3", "항복의 조건은 사람이었습니다.", .2)
b("c3_4", "세자는 아내 강씨, 동생 봉림대군과 함께 청의 수도 심양으로 끌려갑니다.", .35)
b("c3_5", "인질이라면 갇혀 지내는 모습을 떠올리지만, 심양관의 세자는 달랐습니다.", .2)
b("c3_6", "청나라가 조선에 무언가를 요구할 때마다 세자가 그 앞에 섰고, 요구를 줄이려 버텼습니다.", .2)
b("c3_7", "포로로 끌려온 조선 사람들을 모아 땅을 갈게 하고, 거둔 곡식으로 장사도 했습니다.", .25)
b("c3_8", "그런데 같은 일을, 한양의 기록은 이렇게 적었습니다.", .3)
b("c3_9", "관소의 문이 마치 시장 같았으므로, 상이 그 사실을 듣고 불평스럽게 여겼다.", .5, q=True)
b("c3_10", "왕 곁에서는 이런 말까지 돌았다고 합니다. 세자가 청나라의 힘을 빌려 아버지의 자리를 넘본다는 것.", .25)
b("c3_11", "한 연구자는 인조가 심양관에 사람을 보내 세자를 몰래 살피게 했다고 씁니다.", .4)
b("c3_12", "그리고 1644년. 세계에서 가장 큰 나라의 주인이 바뀝니다.", .25)
b("c3_13", "봄, 반란군이 명나라의 수도 베이징을 무너뜨리고, 명의 마지막 황제는 스스로 목숨을 끊습니다.", .2)
b("c3_14", "몇 주 뒤, 만리장성을 넘어온 청나라 군대가 그 베이징에 들어갑니다.", .2)
b("c3_15", "같은 무렵 유럽은 훗날 '30년 전쟁'이라 불릴 전쟁의 막바지였고, 영국에서는 왕과 의회가 싸우고 있었습니다.", .3)
b("c3_16", "그해 9월, 조선의 세자도 베이징에 들어가 70일 남짓 머뭅니다.", .2)
b("c3_17", "그곳에서 세자가 찾아간 곳은, 서양 사람이 하늘을 재고 달력을 만들던 천문대였습니다.", .2)
b("c3_18", "독일인 예수회 신부, 아담 샬.", .2)
b("c3_19", "청나라는 바로 이 신부의 계산으로 새 달력을 만들어, 이듬해부터 온 나라에 씁니다. 이름은 시헌력.", .25)
b("c3_20", "세자는 그에게서 천문과 수학의 책, 그리고 둥근 지구의 하나를 얻어 돌아옵니다.", .35)
b("c3_21", "무너지는 제국과 일어서는 제국을 모두 본 사람.", .25)
b("c3_22", "그 사람이, 자신을 무릎 꿇린 청나라를 끝내 인정하지 않던 아버지의 조정으로 돌아갑니다.", 1.3)
# 4 단서 2
b("c4_0", "1645년 2월 18일, 세자가 한양에 들어옵니다.", .2, ch=2)
b("c4_1", "세자가 돌아오면 신하들이 모여 축하를 올리는 것이 예법이었습니다.", .2)
b("c4_2", "왕은 그것을 막았습니다.", .3)
b("c4_3", "세자가 베이징에서 가져온 서양의 책과 물건들은, 오히려 왕의 노여움을 더했다고 기록은 전합니다.", .35)
b("c4_4", "8년 만에 돌아온 아들을, 아버지는 반기지 않았습니다.", .3)
b("c4_5", "두 달 뒤, 세자는 앓아눕습니다.", 1.3)
# 5 단서 3
b("c5_0", "4월 23일, 병석에 누운 세자에게 의관 이형익이 침을 놓습니다.", .25, ch=3)
b("c5_1", "이 의관에 대해서는 이런 기록이 남아 있습니다.", .15)
b("c5_2", "석 달 전에 특별히 뽑혀 들어온 사람이었고,", .1)
b("c5_3", "왕의 총애를 받던 후궁 조씨의 집안과 얽힌 인물이었다는 것입니다.", .35)
b("c5_4", "치료를 맡은 사람은 들어온 지 석 달 된 의관.", .2)
b("c5_5", "그리고 사흘 뒤, 세자는 숨을 거둡니다.", 1.3)
# 6 단서 4
b("c6_0", "세자가 죽자, 신하들은 그 의관을 벌하라고 요구합니다.", .2, ch=4)
b("c6_1", "왕은 받아들이지 않습니다.", .2)
b("c6_2", "죽음의 까닭을 따지지도 않습니다.", .2)
b("c6_3", "그리고 입관에 들어갈 사람을 줄이고, 서둘러 관을 닫게 합니다.", .8)
b("c6_4", "다음 왕이 될 아들이 죽었습니다.", .3)
b("c6_5", "그런데 아버지는 묻지 않았습니다.", 1.4)
# 7 단서 5
b("c7_0", "법도대로라면 다음 세자는 세자의 맏아들, 왕의 맏손자였습니다.", .2, ch=5)
b("c7_1", "왕은 세자의 동생 봉림대군을 서둘러 새 세자로 세웁니다.", .3)
b("c7_2", "1646년 초. 왕은 자기 음식에 독이 들어 있었다고 말합니다.", .2)
b("c7_3", "의심을 받은 것은 죽은 세자의 아내, 강빈의 궁녀들.", .15)
b("c7_4", "궁녀들은 모진 국문 속에서도 끝내 죄를 인정하지 않고 숨집니다.", .3)
b("c7_5", "그해 3월. 강빈은 왕을 저주하고 독을 넣게 한 사람으로 몰려 사약을 받습니다.", .2)
b("c7_6", "남편을 잃은 지 1년이 채 되지 않은 때였습니다.", .2)
b("c7_7", "강빈의 친정어머니와 형제들도 화를 피하지 못합니다.", .3)
b("c7_8", "남은 세 아이는 바다 건너 제주도로 보내집니다.", .15)
b("c7_9", "가장 어린 아이는 네 살이었다고 전합니다.", .25)
b("c7_10", "1648년. 맏아들이 제주에서 병으로 숨집니다. 열세 살이었습니다.", .2)
b("c7_11", "그해가 가기 전, 둘째도 세상을 떠납니다.", .8)
b("c7_12", "세자가 죽은 지 4년이 채 안 되어,", .1)
b("c7_13", "세자의 아내와 그 집안, 그리고 세자의 두 아들이 사라졌습니다.", .3)
b("c7_14", "살아남은 것은 막내 하나였습니다.", 1.3)
# 8 반대 증거
b("c8_0", "여기까지 오면 범인이 정해진 것처럼 보입니다.", .2, ch="X")
b("c8_1", "하지만 사건 파일에는, 반대편 증거도 함께 넣어야 합니다.", .3)
b("c8_2", "조선에는 실록 말고도 왕의 곁에서 매일을 적은 기록, 승정원일기가 있습니다.", .2)
b("c8_3", "그 진료 기록에는 세자가 귀국 전후로 기침과 열, 숨 가쁨, 가슴 답답함에 시달렸고,", .1)
b("c8_4", "한때 거의 나았다가 한 달 반쯤 뒤 갑자기 나빠졌다는 내용이 있다고 합니다.", .3)
b("c8_5", "이 기록을 살핀 한 한의사는, 폐렴이 깊어지면 숨이 막히며 온몸이 검푸르게 변할 수 있다고 봅니다.", .2)
b("c8_6", "단서 1의 '검은 얼굴'은 독이 아니라, 병의 마지막 모습일 수도 있다는 것입니다.", .35)
b("c8_7", "그리고 단서 2부터 5까지는, 모두 죽음 '앞뒤'의 일입니다.", .2)
b("c8_8", "왕이 아들을 미워했다는 것, 죽음을 묻지 않았다는 것, 남은 가족을 내쳤다는 것.", .2)
b("c8_9", "이것들은 무겁지만, 그 자체로 세자를 죽게 한 것이 독이었다는 증거는 아닙니다.", 1.3)
# 9 판정
b("c9_0", "판정을 내려 보겠습니다.", .3, ch="V")
b("c9_1", "기록이 확실히 말하는 것.", .15)
b("c9_2", "세자는 돌아온 지 두 달 만에, 앓은 지 나흘 만에 죽었습니다.", .15)
b("c9_3", "왕은 그 죽음을 묻지 않았고, 의관을 벌하지 않았고, 서둘러 관을 닫게 했습니다.", .15)
b("c9_4", "그리고 몇 해 사이 세자의 아내와 그 집안, 두 아들이 사라졌습니다.", .3)
b("c9_5", "기록이 끝내 말하지 않는 것.", .15)
b("c9_6", "세자를 죽게 한 것이 무엇이었는지.", .3)
b("c9_7", "해석과 의심.", .15)
b("c9_8", "독살이라는 의심. 그리고 병이었다는 해석.", .5)
b("c9_9", "판정. 미해결.", 1.6, sub=False)
b("c9_10", "세자를 그렇게 보낸 왕 인조는 4년 뒤인 1649년에 세상을 떠납니다.", .2)
b("c9_11", "같은 해 1월, 바다 건너 영국에서는 의회가 왕을 재판에 세워 처형했습니다.", .3)
b("c9_12", "그리고 1653년. 세자가 베이징에서 본 서양 신부의 달력, 시헌력이 동생 효종의 조정에서 조선의 달력이 됩니다.", .3)
b("c9_13", "세자가 들고 오려던 세계의 한 조각은, 세자 없이 조선에 들어온 셈입니다.", .7)
b("c9_14", "1644년 가을, 베이징의 천문대에서 둥근 지구의를 받아 들었던 세자.", .4)
b("c9_15", "그날 환경당에서 그를 데려간 것은 병이었을까요, 독이었을까요.", .7)
b("c9_16", "여러분의 판정은 어느 쪽입니까.", 3.0, sub=False)
BK = {x["k"]: x for x in S}


async def tts_all():
    for x in S:
        rate = QRATE if x["q"] else RATE
        h = hashlib.md5((x["t"] + rate + VOICE).encode()).hexdigest()[:10]
        mp3 = WORK / f"{x['k']}_{h}.mp3"; js = mp3.with_suffix(".json")
        if not (mp3.exists() and js.exists()):
            for attempt in range(4):
                try:
                    c = edge_tts.Communicate(x["t"], VOICE, rate=rate, boundary="WordBoundary")
                    words, audio = [], bytearray()
                    async for chnk in c.stream():
                        if chnk["type"] == "audio": audio += chnk["data"]
                        elif chnk["type"] == "WordBoundary": words.append([chnk["text"], chnk["offset"] / 1e7, chnk["duration"] / 1e7])
                    break
                except Exception as e:
                    print("tts retry", x["k"], e); await asyncio.sleep(2 + attempt * 3)
            mp3.write_bytes(bytes(audio)); js.write_text(json.dumps(words, ensure_ascii=False), encoding="utf-8")
        x["mp3"] = mp3
        x["words"] = json.loads(js.read_text(encoding="utf-8"))
        x["dur"] = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp3)], capture_output=True, text=True).stdout)


CARD = 1.25   # 장 카드가 차지하는 쉼(앞 박자의 쉼에 포함)
def timing():
    t = 0.6
    for x in S:
        x["t0"] = t; x["t1"] = t + x["dur"] + x["pause"]; t = x["t1"]
    return t


def T(k): return BK[k]["t0"]
def E(k): return BK[k]["t1"]
def SPK(k): return BK[k]["t0"] + BK[k]["dur"]          # 말이 끝나는 시각
def w(k, word, n=0):
    hits = [x for x in BK[k]["words"] if x[0].startswith(word)]
    if not hits: print("  !! no word", k, word); return T(k)
    return T(k) + hits[min(n, len(hits) - 1)][1]
def wseq(k, anchor, count):
    """anchor 낱말부터 차례로 count 개 낱말의 시작 시각."""
    ws = BK[k]["words"]; i = next((j for j, x in enumerate(ws) if x[0].startswith(anchor)), 0)
    out = []
    for j in range(count):
        out.append(T(k) + (ws[i + j][1] if i + j < len(ws) else ws[-1][1] + 0.3 * (i + j - len(ws) + 1)))
    return out


# ------------------------------------------------------------------ 자산
IMGS = {"A1": "samples/A1_yeomseup.png", "A2": "samples/A2_samjeondo.png", "A3": "samples/A3_observatory.png", "A4": "art/A4_jeju.png",
        **{n: f"art/{n}_{s}.png" for n, s in [("N1", "farm"), ("N2", "diplomacy"), ("N3", "beijing_fall"), ("N4", "greatwall"), ("N5", "return"),
                                              ("N6", "physician"), ("N7", "coffin"), ("N8", "kangbin"), ("N9", "tray"), ("N10", "scribe"), ("N11", "injo"), ("N12", "shenyang_house")]}}
BASES = []
_shot = shot
def _wstarts():
    return sorted(x["t0"] + w_[1] for x in S for w_ in x.get("words", []))


def shot(img, t0, dur, crop=(0, 0, 1, 1), move=(1.0, 1.08, 0, -2, 0, 0), **k):
    """3초 넘는 그림은 구절 경계마다 다른 부분으로 끊어 보여 줌(넓게 → 세부 → 다른 세부)."""
    BASES.append((t0, t0 + dur, 1, 3.2))
    if dur < 3.0:
        return _shot(img, t0, dur, crop=crop, move=move, **k)
    cx, cy, cw, ch = crop
    var = [crop, (cx + cw * .15, cy + ch * .12, cw * .68, ch * .68), (cx + cw * .02, cy + ch * .22, cw * .72, ch * .72), (cx + cw * .28, cy + ch * .06, cw * .7, ch * .7)]
    n = max(2, round(dur / 2.1)); W_ = _wstarts(); cuts = [t0]
    for i in range(1, n):
        target = t0 + dur * i / n
        c = min((u for u in W_ if t0 + 1.0 < u < t0 + dur - 1.0), key=lambda u: abs(u - target), default=None)
        if c and c - cuts[-1] > 1.0: cuts.append(c)
    cuts.append(t0 + dur); r = None
    for i in range(len(cuts) - 1):
        kk = dict(k)
        if i: kk.pop("fg", None)
        sgn = 1 if i % 2 == 0 else -1
        r = _shot(img, cuts[i], cuts[i + 1] - cuts[i], crop=var[i % 4], move=(1.0, 1.07, sgn, -sgn, 0, -1) if i else move, **kk)
    return r


def music(total):
    M = EP / "real" / "music"; out = AS / "bgm.wav"
    if out.exists(): return
    tracks = [M / "C_ossuary1.mp3", M / "C_ossuary6.mp3", M / "C_ossuary5.mp3"]
    fc = "[0][1]acrossfade=d=4:c1=tri:c2=tri[a];[a][2]acrossfade=d=4:c1=tri:c2=tri,"
    fc += f"atrim=0:{total:.2f},afade=t=in:d=2,afade=t=out:st={total - 4:.2f}:d=4,loudnorm=I=-37.5:TP=-9:LRA=11[o]"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + sum([["-i", str(t)] for t in tracks], []) + ["-filter_complex", fc, "-map", "[o]", "-ar", "48000", "-ac", "2", str(out)], check=True)


REAL = EP / "real"
CRED = json.loads((REAL / "credits.json").read_text(encoding="utf-8"))
RSIZE = {}
def real_assets():
    for k in CRED:
        out = AS / f"{k}.jpg"
        if not out.exists():
            im = Image.open(REAL / f"{k}.jpg").convert("RGB"); im.thumbnail((2400, 2400)); im.save(out, quality=90)
        RSIZE[k] = Image.open(out).size
    # 바탕 무늬: 실록 글자(仁祖實錄 卷四十六) 아주 옅게
    chars = "仁祖實錄卷四十六世子薨"
    cells = "".join(f'<text x="{(i % 6) * 120 + 30}" y="{(i // 6) * 120 + 80}" font-family="Batang,serif" font-size="56" fill="#ffffff" fill-opacity=".035">{chars[i % len(chars)]}</text>' for i in range(36))
    (AS / "pattern.svg").write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="720" height="720">{cells}</svg>', encoding="utf-8")


def credit_text(k):
    c = CRED[k]; a = re.sub(r"\s+", " ", c["artist"]).strip()
    a = "" if a.lower().startswith(("anonymous", "unknown")) else a
    return f"{'사진·그림: ' + a + ' · ' if a else ''}{c['license']} · Wikimedia Commons"


def photo(k, t0, t1, title, sub=None, mode="card", focus=(0.5, 0.5), z=4):
    """실제 자료. mode=card(바탕 위 액자) | full(화면 가득) | inset(오른쪽 위 작은 창)."""
    iw, ih = RSIZE[k]; i = nid("ph"); im = nid("pi")
    CUT = None
    if mode != "inset" and t1 - t0 > 3.2:
        _W = _wstarts(); _mid = (t0 + t1) / 2
        CUT = min((u for u in _W if t0 + 1.2 < u < t1 - 1.0), key=lambda u: abs(u - _mid), default=None)
    if mode == "full":
        inner = (f'<div style="position:absolute;inset:0;overflow:hidden"><img id="{im}" src="assets/{k}.jpg" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:{focus[0] * 100:.0f}% {focus[1] * 100:.0f}%"></div>'
                 '<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.55) 0%,transparent 22%,transparent 70%,rgba(0,0,0,.55) 100%)"></div>')
        JS.append(f'tl.fromTo("#{im}",{{scale:1.0}},{{scale:1.06,duration:{(CUT or t1) - t0:.2f},ease:"none"}},{t0:.3f});')
    elif mode == "inset":
        bw = 620; bh = int(bw * ih / iw)
        if bh > 520: bh = 520; bw = int(bh * iw / ih)
        inner = (f'<div id="{im}" style="position:absolute;right:90px;top:170px;width:{bw}px;height:{bh}px;border:4px solid #f1e6cf;box-shadow:0 24px 60px rgba(0,0,0,.7);overflow:hidden">'
                 f'<img src="assets/{k}.jpg" style="width:100%;height:100%;object-fit:cover"></div>')
        JS.append(f'tl.fromTo("#{im}",{{opacity:0,y:30}},{{opacity:1,y:0,duration:.35,ease:"power2.out"}},{t0:.3f});')
    else:
        mw, mh = 1380, 760; sc = min(mw / iw, mh / ih); bw, bh = int(iw * sc), int(ih * sc)
        x = (W - bw) // 2; y = 150 + (mh - bh) // 2
        inner = (BG_DARK + f'<div id="{im}" style="position:absolute;left:{x}px;top:{y}px;width:{bw}px;height:{bh}px;box-shadow:0 30px 80px rgba(0,0,0,.75);overflow:hidden">'
                 f'<img src="assets/{k}.jpg" style="width:100%;height:100%;object-fit:cover"></div>')
        JS.append(f'tl.fromTo("#{im}",{{opacity:0,scale:.96}},{{opacity:1,scale:1,duration:.35,ease:"power2.out"}},{t0:.3f});'
                  f'tl.to("#{im}",{{scale:1.03,duration:{max(.1, (CUT or t1) - t0 - .35):.2f},ease:"none"}},{t0 + .35:.3f});')
    tx, ty = (110, 60) if mode != "inset" else (W - 90 - bw, 170 + bh + 16)
    tt = (f'<div style="position:absolute;left:{tx}px;top:{ty}px;border-left:6px solid {ACC};padding-left:18px">'
          f'<div style="font:700 {44 if mode != "inset" else 32}px Malgun;color:#f6efe2;text-shadow:0 2px 10px #000">{title}</div>'
          + (f'<div style="font:700 28px Malgun;color:rgba(246,239,226,.75);text-shadow:0 2px 8px #000">{sub}</div>' if sub else "") + '</div>')
    cr = f'<div data-layout-ignore style="position:absolute;right:{56 if mode != "inset" else 90}px;top:{118 if mode != "inset" else 170 + bh + 70}px;font:700 20px Malgun;color:rgba(246,239,226,.6);text-shadow:0 1px 4px #000">{credit_text(k)}</div>'
    if mode != "inset" and t1 - t0 > 3.2:
        c = CUT
        if c:
            ox, oy = focus
            JS.append(f'tl.set("#{im}",{{scale:1.5,transformOrigin:"{ox * 100:.0f}% {oy * 100:.0f}%"}},{c:.3f});tl.to("#{im}",{{scale:1.58,duration:{t1 - c:.2f},ease:"none"}},{c:.3f});')
    clip(inner + tt + cr, t0, t1 - t0, z=z)
    CREDIT_USED.add(k)
    if mode != "inset": BASES.append((t0, t1, z, 4.5))
    return i


CREDIT_USED = set()
ACC = "#e8503a"


def gloss(k, word, s, t1=None):
    """어려운 말 풀이 쪽지 (한 번만 보여 줌)."""
    t = w(k, word); t1 = t1 or E(k); i = nid("gl")
    clip(f'<div id="{i}" style="position:absolute;left:110px;top:760px;padding:12px 24px;background:rgba(10,11,13,.82);border-left:6px solid {ACC};font:700 34px Malgun;color:#f1e6cf">{s}</div>', t, t1 - t, z=31)
    JS.append(f'tl.fromTo("#{i}",{{opacity:0,x:-30}},{{opacity:1,x:0,duration:.3,ease:"power2.out"}},{t:.3f});')


VDIR = AS / "v"
VDUR = {p.stem: float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout) for p in VDIR.glob("*.mp4")}
VUSE = {}
VLABEL = {"C_mukden_drone1": ("선양(심양) 고궁", "청의 첫 궁궐 · 드론 영상 (오늘)"), "C_mukden_drone2": ("선양(심양) 고궁", "드론 영상 (오늘)"),
          "MK_greatwall": ("만리장성", "오늘의 모습"), "MK_palace": ("조선의 궁궐", "오늘의 경복궁")}


def broll(name, t0, t1, z, label=True):
    n = VUSE.get(name, 0); VUSE[name] = n + 1
    span = max(0.1, VDUR[name] - (t1 - t0) - 0.3); ms = (n * 3.7) % span
    i = nid("bv")
    HTML.append(f'<video id="{i}" class="clip" src="assets/v/{name}.mp4" muted playsinline data-start="{t0:.3f}" data-duration="{t1 - t0:.3f}" '
                f'data-media-start="{ms:.2f}" data-track-index="{z}" style="position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover;z-index:{z}"></video>')
    if label and name in VLABEL:
        a, b_ = VLABEL[name]
        clip(f'<div style="position:absolute;left:110px;top:60px;border-left:6px solid {ACC};padding-left:18px"><div style="font:700 44px Malgun;color:#f6efe2;text-shadow:0 2px 10px #000">{a}</div>'
             f'<div style="font:700 28px Malgun;color:rgba(246,239,226,.75);text-shadow:0 2px 8px #000">{b_}</div></div>', t0, t1 - t0, z=z + 1)


POOLS = [("o", ["MK_candle", "MK_smoke", "MK_candles"]), ("c1_", ["MK_ink", "MK_candle", "MK_books"]), ("c2_", ["MK_ink", "MK_smoke", "MK_candle"]),
         ("c3_0", ["MK_snowforest", "MK_raven", "MK_hooves"]), ("c3_1", ["MK_snowpine", "MK_hooves"]), ("c3_2", ["MK_snowforest", "MK_raven"]),
         ("c3_3", ["MK_hooves", "MK_snowpine"]), ("c3_4", ["MK_horses", "MK_hooves"]),
         ("c3_6", ["C_mukden_drone2", "MK_horses"]), ("c3_7", ["C_mukden_drone2", "MK_horses"]), ("c3_8", ["MK_books", "MK_ink"]), ("c3_9", ["MK_ink"]),
         ("c3_10", ["MK_smoke", "MK_candles"]), ("c3_11", ["MK_mistforest"]), ("c3_12", ["MK_flames", "MK_bonfire"]), ("c3_13", ["MK_bonfire", "MK_flames"]),
         ("c3_14", ["MK_hooves", "MK_greatwall"]), ("c3_15", ["MK_flames"]), ("c3_16", ["MK_horses"]), ("c3_17", ["MK_moon", "MK_leaves"]),
         ("c3_18", ["MK_moon", "MK_leaves"]), ("c3_19", ["MK_moon"]), ("c3_20", ["MK_leaves", "MK_moon"]), ("c3_21", ["MK_flames", "MK_hooves"]), ("c3_22", ["MK_leaves", "MK_mist"]),
         ("c4_", ["MK_crow", "MK_snowpine", "MK_palace", "MK_mist"]), ("c5_", ["MK_candle", "MK_smoke", "MK_ink"]),
         ("c6_", ["MK_candles", "MK_smoke", "MK_moon2"]), ("c7_", ["MK_raven", "MK_mist", "MK_rockwaves", "MK_crow"]),
         ("c8_", ["MK_books", "MK_ink", "MK_candle"]), ("c9_", ["MK_candle", "MK_moon", "MK_mistforest", "MK_leaves"])]
SKIP = {"c1_5", "c3_5", "c3_20", "c4_1", "c4_2", "c6_0", "c6_3", "c2_6"}


def beat_at(t):
    for x in S:
        if x["t0"] <= t < x["t1"]: return x["k"]
    return S[-1]["k"]


def pool_for(k):
    best = None
    for p, lst in POOLS:
        if k.startswith(p) and (best is None or len(p) > len(best[0])): best = (p, lst)
    return best[1] if best else ["MK_candle"]


def cutaways():
    W_ = sorted(x["t0"] + w_[1] for x in S for w_ in x["words"])
    nxt = lambda t: next((u for u in W_ if u >= t), None)
    rot = {}
    for a, b_, z, mn in sorted(BASES):
        k = beat_at(a + 0.05)
        if b_ - a < mn or k in SKIP: continue
        pool = pool_for(k); t = a + 1.2
        while True:
            s0 = nxt(t)
            if s0 is None or s0 > b_ - 2.3: break
            e0 = nxt(s0 + 1.4) or s0 + 1.8; e0 = min(e0, s0 + 2.2)
            if b_ - e0 < 0.9: break
            i = rot.get(k[:2], 0); rot[k[:2]] = i + 1
            broll(pool[i % len(pool)], s0, e0, z + 1)
            t = e0 + 1.3


def assets():
    for k, p in IMGS.items():
        out = AS / f"{k}.jpg"
        if not out.exists(): Image.open(EP / p).convert("RGB").resize((2400, 1350)).save(out, quality=90)
    for f in ["malgunbd.ttf", "batang.ttc"]:
        if not (AS / "fonts" / f).exists(): shutil.copy(rf"C:\Windows\Fonts\{f}", AS / "fonts" / f)
    lst = WORK / "vo.txt"; parts = []
    lead = WORK / "lead.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", "0.6", str(lead)], check=True)
    for x in S:
        wv = WORK / f"p_{x['mp3'].stem}_{x['pause']}.wav"
        if not wv.exists():
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(x["mp3"]), "-af", f"apad=pad_dur={x['pause']}", "-ar", "48000", "-ac", "2", str(wv)], check=True)
        parts.append(wv)
    lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in [lead] + parts), encoding="utf-8")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), str(AS / "vo.wav")], check=True)


# ------------------------------------------------------------------ 공통 조각 (한 편의 닫힌 어휘)
BG_DARK = '<div style="position:absolute;inset:0;background:#111317 url(assets/pattern.svg)"></div>'
LBL = "font:700 34px Malgun;color:#f1e6cf"

def sub_off(*ks):
    for k in ks: BK[k]["sub"] = False


def tag(t0, t1, s, top=86):
    typewriter(t0 + 0.05, t1, s, f"left:96px;top:{top}px;font:700 40px Malgun;color:#efe2c6;letter-spacing:.06em;text-shadow:0 2px 10px #000")


def label(t, t1, title, sub=None, x=110, y=650, color="#a3171b"):
    h = f'<span style="font:700 46px Malgun;color:#f1e6cf">{title}</span>' + (f'<br><span style="font:700 28px Malgun;color:rgba(241,230,207,.75)">{sub}</span>' if sub else "")
    i = text(t, t1 - t, h, f"left:{x}px;top:{y}px;padding:16px 28px;border-left:6px solid {color};background:rgba(0,0,0,.5)")
    JS.append(f'tl.fromTo("#{i}",{{x:-40}},{{x:0,duration:.35,ease:"expo.out"}},{t:.3f});')
    return i


def big(t, t1, s, style, sound="hit"):
    i = text(t, t1 - t, s, style)
    JS.append(f'tl.fromTo("#{i}",{{scale:1.35}},{{scale:1,duration:.4,ease:"expo.out"}},{t:.3f});')
    if sound: SFX.append((sound, t))
    return i


def chip(t, t1, s, x, y, bg="rgba(163,23,27,.9)", size=36, rot=0):
    i = nid("cp")
    clip(f'<div id="{i}" style="position:absolute;left:{x}px;top:{y}px;padding:10px 24px;border-radius:8px;background:{bg};font:700 {size}px Malgun;color:#f6ecd8;transform:rotate({rot}deg);box-shadow:0 10px 24px rgba(0,0,0,.5)">{s}</div>', t, t1 - t, z=30)
    JS.append(f'tl.fromTo("#{i}",{{opacity:0,scale:.6,y:24}},{{opacity:1,scale:1,y:0,duration:.3,ease:"back.out(2)"}},{t:.3f});')
    SFX.append(("tick", t))
    return i


def strike(t, x, y, wdt, t1, color="#e8503a", z=33):
    i = nid("sk")
    clip(f'<svg style="position:absolute;inset:0" width="{W}" height="{H}"><line id="{i}" x1="{x}" y1="{y}" x2="{x + wdt}" y2="{y}" stroke="{color}" stroke-width="10" stroke-linecap="round" stroke-dasharray="{wdt}" stroke-dashoffset="{wdt}"/></svg>', t, t1 - t, z=z)
    JS.append(f'tl.to("#{i}",{{attr:{{"stroke-dashoffset":0}},duration:.3,ease:"power2.out"}},{t:.3f});')
    SFX.append(("whoosh", t + .1))


def darkfade(t0, t1, k=0.15):
    JS.append(f'tl.to("#cam",{{filter:"brightness({k})",duration:{t1 - t0:.2f},ease:"power2.in"}},{t0:.3f});tl.set("#cam",{{filter:"brightness(1)"}},{t1:.3f});')


def camzoom(t0, t1, s0=1.0, s1=1.08):
    JS.append(f'tl.fromTo("#cam",{{scale:{s0}}},{{immediateRender:false,scale:{s1},duration:{t1 - t0:.2f},ease:"sine.inOut"}},{t0:.3f});tl.set("#cam",{{scale:1}},{t1:.3f});')


# --- 실록 종이: 말하는 낱말마다 글자가 맺힘
def paper(t0, t1, header, lines, inkat=None, under=None, x=230, y=120, wdt=1460, hgt=820, fs=60, gap=112, z=3):
    """lines=[(문장, 박자키, 첫낱말)]; inkat=(박자키, 낱말, cx, cy, r); under=(박자키, 낱말, x1, x2, y)"""
    pid = nid("pw")
    clip('<div style="position:absolute;inset:0;background:#0c0b0a"></div>', t0, t1 - t0, z=2)
    HTML.append(f'<div id="{pid}" style="position:absolute;inset:0;z-index:{z}" data-layout-allow-overflow data-layout-allow-overlap>')
    clip(f'<div style="position:absolute;left:{x}px;top:{y}px;width:{wdt}px;height:{hgt}px;border-radius:6px;background:radial-gradient(ellipse at 30% 20%,#e9dcbc,#cdb98d 75%,#a88f63);box-shadow:0 40px 90px rgba(0,0,0,.7)">'
         f'<svg width="{wdt}" height="{hgt}" style="position:absolute;inset:0;opacity:.35"><filter id="{pid}n"><feTurbulence baseFrequency=".9" numOctaves="2" seed="2"/><feColorMatrix values="0 0 0 0 .3 0 0 0 0 .22 0 0 0 0 .12 0 0 0 .6 0"/></filter><rect width="{wdt}" height="{hgt}" filter="url(#{pid}n)"/></svg></div>', t0, t1 - t0, z=3)
    JS.append(f'tl.fromTo("#{pid}",{{rotationX:10,rotationY:-3,scale:.9,y:40,transformPerspective:1800}},{{rotationX:2,rotationY:3,scale:1.03,y:0,duration:{t1 - t0:.2f},ease:"sine.out"}},{t0:.3f});')
    whip(t0)
    text(t0 + 0.1, t1 - t0 - 0.1, header, f"left:{x + 70}px;top:{y + 50}px;font:700 30px Batang;color:#6b5033")
    for n, (ln, k, wd) in enumerate(lines):
        toks = ln.split(); ts = wseq(k, wd, len(toks))
        i = nid("ln"); spans = "".join(f'<span style="opacity:0;filter:blur(6px)">{s} </span>' for s in toks)
        clip(f'<div id="{i}" style="position:absolute;left:{x + 90}px;top:{y + 150 + n * gap}px;font:400 {fs}px Batang;color:#2a1d14">{spans}</div>', ts[0], t1 - ts[0], z=22)
        for j, tt in enumerate(ts):
            JS.append(f'tl.to("#{i} span:nth-child({j + 1})",{{opacity:1,filter:"blur(0px)",duration:.14}},{tt:.3f});')
    if inkat:
        k, wd, cx, cy, r = inkat; ti = w(k, wd); ink(ti, cx, cy, r, t1 - ti)
    if under:
        k, wd, x1, x2, yy = under; tu = w(k, wd); i = nid("ul")
        clip(f'<svg style="position:absolute;inset:0" width="{W}" height="{H}"><line id="{i}" x1="{x1}" y1="{yy}" x2="{x2}" y2="{yy}" stroke="#9a1015" stroke-width="9" stroke-linecap="round" stroke-dasharray="{x2 - x1}" stroke-dashoffset="{x2 - x1}"/></svg>', tu, t1 - tu, z=30)
        JS.append(f'tl.to("#{i}",{{attr:{{"stroke-dashoffset":0}},duration:.4,ease:"power2.out"}},{tu + .1:.3f});')
    return pid   # 호출 쪽에서 HTML.append('</div>')


# --- 지도: 한 장의 땅 모양을 viewBox 로 옮겨 다님
DEFS.append(f'<path id="land" d="{geo.land_path()}"/>')
DEFS.append('<radialGradient id="sea" cx="50%" cy="45%" r="75%"><stop offset="0" stop-color="#18222a"/><stop offset="1" stop-color="#07090b"/></radialGradient>')
PL = {"한양": (126.98, 37.57), "심양": (123.43, 41.8), "베이징": (116.4, 39.9), "산해관": (119.75, 40.0), "제주": (126.53, 33.4),
      "남한산성": (127.18, 37.48), "런던": (-0.13, 51.5), "독일": (10.0, 50.8)}
def vb(lon_c, lat_c, wdeg):
    x, y = geo.P(lon_c, lat_c); ww = wdeg * geo.K; hh = ww * 9 / 16
    return (x - ww / 2, y - hh / 2, ww, hh)


def mapscene(t0, t1, v0, v1, pins=(), routes=(), notes=(), zmove=None, fsw=None):
    """pins=[(이름, 시각, 빨강?)], routes=[(A, B, 시각, 굽힘, 점선?)], notes=[(경도,위도,글,시각,크기배)]"""
    sid = nid("mp"); ww = fsw or v1[2]; fs = ww * 0.034; r = ww * 0.0065
    g = ['<rect x="-400" y="-400" width="1200" height="800" fill="url(#sea)"/>',
         f'<use href="#land" fill="#3b3326" stroke="#a08a63" stroke-width="1.3" vector-effect="non-scaling-stroke"/>']
    # 경위선
    for lo in range(-30, 181, 10):
        x, _ = geo.P(lo, 0); g.append(f'<line x1="{x:.1f}" y1="-90" x2="{x:.1f}" y2="0" stroke="rgba(200,180,140,.10)" stroke-width="1" vector-effect="non-scaling-stroke"/>')
    for la in range(0, 81, 10):
        g.append(f'<line x1="-60" y1="{-la}" x2="160" y2="{-la}" stroke="rgba(200,180,140,.10)" stroke-width="1" vector-effect="non-scaling-stroke"/>')
    later = []
    for (a, bb, t, bend, dash) in routes:
        (x1, y1), (x2, y2) = geo.P(*PL[a]), geo.P(*PL[bb])
        mx, my = (x1 + x2) / 2 - (y2 - y1) * bend, (y1 + y2) / 2 + (x2 - x1) * bend
        i = nid("rt")
        g.append(f'<path id="{i}" d="M{x1:.2f} {y1:.2f} Q{mx:.2f} {my:.2f} {x2:.2f} {y2:.2f}" fill="none" stroke="#e8503a" stroke-width="5" stroke-linecap="round" vector-effect="non-scaling-stroke" pathLength="1" stroke-dasharray="{"0.02 0.02" if dash else "1 1"}" stroke-dashoffset="1" opacity="0"/>')
        later.append(f'tl.set("#{i}",{{opacity:1}},{t:.3f});tl.fromTo("#{i}",{{attr:{{"stroke-dashoffset":1}}}},{{attr:{{"stroke-dashoffset":0}},duration:1.1,ease:"power2.inOut"}},{t:.3f});')
        SFX.append(("whoosh", t + .3))
    for (nm, t, red) in pins:
        x, y = geo.P(*PL[nm]); i = nid("pn")
        g.append(f'<g id="{i}" opacity="0"><circle cx="{x:.2f}" cy="{y:.2f}" r="{r * 2.6:.3f}" fill="none" stroke="{"#e8503a" if red else "#f1e6cf"}" stroke-width="2" vector-effect="non-scaling-stroke"/>'
                 f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.3f}" fill="{"#e8503a" if red else "#f1e6cf"}"/>'
                 f'<text x="{x + r * 3.2:.2f}" y="{y + fs * .35:.2f}" font-family="Malgun" font-weight="700" font-size="{fs:.3f}" fill="#f6ecd8" stroke="#0b0a09" stroke-width="{fs * .12:.3f}" paint-order="stroke">{nm}</text></g>')
        later.append(f'tl.fromTo("#{i}",{{opacity:0}},{{opacity:1,duration:.25}},{t:.3f});')
        SFX.append(("tick", t))
    for (lo, la, s, t, m) in notes:
        x, y = geo.P(lo, la); i = nid("nt")
        g.append(f'<text id="{i}" x="{x:.2f}" y="{y:.2f}" opacity="0" text-anchor="middle" font-family="Malgun" font-weight="700" font-size="{fs * m:.3f}" fill="#f1e6cf" stroke="#0b0a09" stroke-width="{fs * m * .12:.3f}" paint-order="stroke">{s}</text>')
        later.append(f'tl.fromTo("#{i}",{{opacity:0}},{{opacity:1,duration:.3}},{t:.3f});')
    vs0 = " ".join(f"{v:.3f}" for v in v0); vs1 = " ".join(f"{v:.3f}" for v in v1)
    clip(f'<svg id="{sid}" style="position:absolute;inset:0" width="{W}" height="{H}" viewBox="{vs0}" preserveAspectRatio="xMidYMid slice">'
         f'{"".join(g)}</svg>', t0, t1 - t0, z=2)
    if zmove:
        mid, v2 = zmove; vs2 = " ".join(f"{v:.3f}" for v in v2)
        JS.append(f'tl.fromTo("#{sid}",{{attr:{{viewBox:"{vs0}"}}}},{{attr:{{viewBox:"{vs1}"}},duration:{mid - t0:.2f},ease:"power2.inOut"}},{t0:.3f});'
                  f'tl.to("#{sid}",{{attr:{{viewBox:"{vs2}"}},duration:{t1 - mid:.2f},ease:"power2.inOut"}},{mid:.3f});')
    else:
        JS.append(f'tl.fromTo("#{sid}",{{attr:{{viewBox:"{vs0}"}}}},{{attr:{{viewBox:"{vs1}"}},duration:{min(2.2, t1 - t0):.2f},ease:"power3.inOut"}},{t0:.3f});')
    JS.extend(later)


# --- 사건 파일: 단서 다섯 칸 (장마다 같은 판으로 돌아옴)
CLUES = [("염습실의 얼굴", "독처럼 '보였다'"), ("차가운 귀국", "축하를 막은 왕"), ("석 달 전에 온 의관", "들어온 지 석 달"),
         ("묻지 않은 왕", "벌도, 조사도 없음"), ("지워지는 가족", "4년 안에 일가가 사라짐")]
def tracker(t0, t1, cur, filled=None, title=None, flip=None, zb=0):
    """cur: 이번에 여는 단서(1~5) 또는 None. filled: 요약이 적힌 단서 수."""
    filled = cur - 1 if filled is None and cur else (filled or 0)
    clip(BG_DARK + '<div style="position:absolute;left:0;right:0;top:110px;text-align:center;font:700 34px Batang;color:#cdb98d;letter-spacing:.4em">사 건 파 일 · 0 0 1</div>', t0, t1 - t0, z=2 + zb)
    whip(t0)
    for n in range(5):
        x = 130 + n * 340; i = nid("tk"); on = (n + 1) == cur
        summ = CLUES[n][1] if n < filled else ("?" if not on else "")
        clip(f'<div id="{i}" style="position:absolute;left:{x}px;top:{300 if not on else 250}px;width:300px;height:{420 if not on else 520}px;border-radius:8px;'
             f'background:{"linear-gradient(#d4bf8e,#bfa46e)" if on else ("#2c2924" if n >= filled else "linear-gradient(#a8946a,#8c7853)")};box-shadow:0 20px 50px rgba(0,0,0,.7);'
             f'opacity:{1 if (on or n < filled) else .45}">'
             f'<div style="position:absolute;left:24px;top:24px;font:700 30px Malgun;color:{"#5a1012" if on else "#3a2c1c" if n < filled else "#8f826d"}">단서 {n + 1}</div>'
             f'<div style="position:absolute;left:24px;right:20px;top:80px;font:700 {38 if on else 32}px Batang;line-height:1.25;color:{"#24180f" if (on or n < filled) else "#6d6455"};word-break:keep-all">{CLUES[n][0] if (on or n < filled) else ""}</div>'
             f'<div style="position:absolute;left:24px;right:20px;bottom:30px;font:700 28px Malgun;line-height:1.3;color:#7a0d10;word-break:keep-all">{summ}</div></div>', t0, t1 - t0, z=20 + zb)
        JS.append(f'tl.fromTo("#{i}",{{y:{80 + n * 20},opacity:0}},{{y:0,opacity:1,duration:.4,ease:"expo.out"}},{t0 + .05 * n:.3f});')
        if on:
            JS.append(f'tl.fromTo("#{i}",{{rotationY:-80,transformPerspective:1200}},{{rotationY:0,duration:.55,ease:"back.out(1.4)"}},{t0 + .25:.3f});')
            SFX.append(("thud", t0 + .5))
    if flip:   # (단서번호, 새 요약, 시각)
        n, s, t = flip; x = 130 + (n - 1) * 340
        chip(t, t1, s, x + 10, 640, bg="rgba(70,74,82,.95)", size=28)


def chapter_card(k, kind):
    """장 첫 박자 앞의 쉼 동안 사건 파일 카드. kind: 1~5 단서, 'P' 인물 기록, 'X' 반대 증거, 'V' 판정."""
    prev = S[[x["k"] for x in S].index(k) - 1]
    t0 = prev["t0"] + prev["dur"] + 0.15; t1 = T(k)
    if isinstance(kind, int):
        tracker(t0, t1, kind, zb=33)
    else:
        title = {"P": ("인물 기록", "이 사람은 누구였나"), "X": ("반대 증거", "승정원일기"), "V": ("판정", "기록이 말하는 것과 말하지 않는 것")}[kind]
        clip(BG_DARK + f'<div id="{nid("fo")}" style="position:absolute;left:460px;top:250px;width:1000px;height:560px;background:linear-gradient(#d4bf8e,#c2a873);border-radius:8px;box-shadow:0 30px 80px rgba(0,0,0,.8)">'
             f'<div style="position:absolute;left:56px;top:50px;font:700 32px Batang;color:#5a4128;letter-spacing:.2em">사건 파일 · 001</div>'
             f'<div style="position:absolute;left:56px;top:150px;font:700 92px Batang;color:#24180f">{title[0]}</div>'
             f'<div style="position:absolute;left:56px;top:290px;width:880px;height:3px;background:#7a5c38"></div>'
             f'<div style="position:absolute;left:56px;top:330px;font:700 44px Malgun;color:#5a4128">{title[1]}</div></div>', t0, t1 - t0, z=53)
        whip(t0)
    SFX.append(("swell", t0 + .1))
    chapter_label(T(k), kind)


CH_SPANS = []
def chapter_label(t, kind):
    name = {1: "단서 1 · 염습실의 얼굴", 2: "단서 2 · 차가운 귀국", 3: "단서 3 · 석 달 전에 온 의관", 4: "단서 4 · 묻지 않은 왕", 5: "단서 5 · 지워지는 가족",
            "P": "인물 기록", "X": "반대 증거", "V": "판정"}[kind]
    CH_SPANS.append((t, name))


# --- 가계도: 단서 5 내내 같은 판 위에서 사람이 하나씩 지워짐
FT = {"king": (960, 170, "왕", "인조"), "sh": (640, 420, "세자 · 1645 사망", "소현세자"), "kang": (300, 420, "세자빈", "강빈"), "kin": (300, 180, "강빈의 친정", "친정 가족"),
      "bong": (1300, 420, "세자의 동생", "봉림대군"), "s1": (440, 720, "맏아들", "첫째"), "s2": (720, 720, "둘째 아들", "둘째"), "s3": (1000, 720, "막내아들", "셋째")}
def family(t0, t1, events):
    """events=[(시각, 동작, 대상)] 동작: dim(지워짐)·heir(다음 세자 화살표)·glow"""
    fid = nid("ft")
    lines = [("king", "sh"), ("king", "bong"), ("sh", "s1"), ("sh", "s2"), ("sh", "s3"), ("kin", "kang")]
    svg = "".join(f'<line x1="{FT[a][0]}" y1="{FT[a][1] + 55}" x2="{FT[c][0]}" y2="{FT[c][1] - 55}" stroke="#8c7a5a" stroke-width="4"/>' for a, c in lines)
    svg += f'<line x1="{FT["kang"][0] + 120}" y1="420" x2="{FT["sh"][0] - 120}" y2="420" stroke="#8c7a5a" stroke-width="4"/><line x1="{FT["kang"][0] + 120}" y1="430" x2="{FT["sh"][0] - 120}" y2="430" stroke="#8c7a5a" stroke-width="4"/>'
    nodes = ""
    for nm, (x, y, s, full) in FT.items():
        dead = nm == "sh"
        nodes += (f'<div id="{fid}{nm}" style="position:absolute;left:{x - 120}px;top:{y - 55}px;width:240px;height:110px;border-radius:10px;'
                  f'background:{"#5b5145" if dead else "#d9c79f"};box-shadow:0 12px 28px rgba(0,0,0,.6);text-align:center;{"filter:grayscale(1);opacity:.6" if dead else ""}">'
                  f'<div style="font:700 40px Batang;color:#24180f;margin-top:12px">{full}</div><div style="font:700 28px Malgun;color:#5a4128">{s}</div></div>')
    clip(BG_DARK + f'<svg style="position:absolute;inset:0" width="{W}" height="{H}">{svg}</svg>' + nodes, t0, t1 - t0, z=3)
    JS.append(f'tl.fromTo("#{fid}king,#{fid}sh,#{fid}kang,#{fid}kin,#{fid}bong,#{fid}s1,#{fid}s2,#{fid}s3",{{opacity:0,y:30}},{{opacity:function(i){{return i==1?.6:1}},y:0,duration:.35,stagger:.06,ease:"expo.out"}},{t0:.3f});')
    ar = nid("ar")
    clip(f'<div id="{ar}" style="position:absolute;left:{FT["s1"][0] - 90}px;top:{FT["s1"][1] + 70}px;width:180px;text-align:center;font:700 32px Malgun;color:#e8503a">▲<br>다음 세자</div>', t0, t1 - t0, z=6)
    JS.append(f'tl.fromTo("#{ar}",{{opacity:0}},{{opacity:1,duration:.3}},{t0 + .6:.3f});')
    for t, act, who in events:
        if act == "dim":
            JS.append(f'tl.to("#{fid}{who}",{{filter:"grayscale(1)",opacity:.28,scale:.94,duration:.45,ease:"power2.out"}},{t:.3f});')
            x, y, _, _ = FT[who]; strike(t, x - 110, y, 220, t1, z=8)
        elif act == "heir":
            dx = FT["bong"][0] - FT["s1"][0]; dy = FT["bong"][1] - FT["s1"][1]
            JS.append(f'tl.to("#{ar}",{{x:{dx},y:{dy - 230},duration:.6,ease:"power3.inOut"}},{t:.3f});'); SFX.append(("whoosh", t))
            JS.append(f'tl.to("#{fid}bong",{{boxShadow:"0 0 0 6px #e8503a, 0 12px 28px rgba(0,0,0,.6)",duration:.3}},{t + .5:.3f});')
        elif act == "glow":
            JS.append(f'tl.to("#{fid}{who}",{{scale:1.12,boxShadow:"0 0 40px 8px rgba(255,200,120,.6)",duration:.5}},{t:.3f});')
    return fid


# ------------------------------------------------------------------ 장면
def build():
    sub_off("c1_2", "o7")
    # ================= 0 콜드 오픈 (샘플 v3 와 같은 연출)
    shot("A1", 0.6, E("o0") - 0.6, crop=(0.55, 0.62, 0.32, 0.32), move=(1.0, 1.12, 0, 0, 0, -3), flick=(55, 45), dust=26)
    tag(T("o0"), E("o0"), "1645년 4월 · 창경궁 환경당")
    mid = w("o1", "세상을")
    shot("A1", T("o1"), mid - T("o1"), move=(1.06, 1.12, 2, -2, 0, 0), fg=("linear-gradient(90deg,#000 0%,#000 30%,transparent 42%)", 2.6), flick=(77, 63), dust=18)
    shot("A1", mid, E("o1") - mid, crop=(0.3, 0.22, 0.55, 0.55), move=(1.0, 1.08, -2, 2, 0, 0), flick=(37, 72), dust=14)
    shot("A1", T("o2"), E("o2") - T("o2"), crop=(0.33, 0.5, 0.42, 0.42), move=(1.0, 1.14, 0, 0, 0, 0), flick=(60, 85), tint="radial-gradient(circle at 50% 50%,transparent 30%,rgba(0,0,0,.55) 75%)")
    t33 = w("o2", "서른셋"); big(t33, E("o2"), "33", "right:180px;top:300px;font:400 220px Batang;color:rgba(240,228,205,.85)")
    shot("A1", T("o3"), E("o3") - T("o3"), crop=(0.0, 0.0, 0.46, 0.46), move=(1.0, 1.1, 0, 2, 0, 0), flick=(95, 95))
    darkfade(E("o3") - 0.45, E("o3"))
    paper(T("o4"), E("o5"), "仁祖實錄 卷四十六 · 인조 23년(1645) 6월 27일",
          [("온몸이 전부 검은빛이었고,", "o4", "온몸이"), ("이목구비의 일곱 구멍에서는", "o4", "이목구비의"), ("모두 선혈이 흘러나왔다.", "o4", "모두"), ("마치 약물에 중독되어 죽은 사람과 같았다.", "o5", "마치")],
          inkat=("o5", "중독되어", 720, 680, 120), under=("o5", "중독되어", 590, 850, 700), fs=64, gap=120)
    SFX.append(("hit", T("o4"))); stamp(E("o5") - 0.9, 0.9, "기록", 1380, 760, size=64); HTML.append("</div>")
    photo("R_sillok", T("o6"), E("o6"), "조선왕조실록", "나라가 펴낸 공식 역사 · 태백산사고본")
    # 사건 파일 · 1645 → 2026
    t7 = T("o7")
    clip(BG_DARK + '<div id="fold" style="position:absolute;left:360px;top:110px;width:1200px;height:860px;background:linear-gradient(#d4bf8e,#c2a873);border-radius:8px 8px 4px 4px;box-shadow:0 30px 80px rgba(0,0,0,.8)">'
         '<div style="position:absolute;left:60px;top:60px;font:700 36px Batang;color:#5a4128;letter-spacing:.2em">사건 파일 · 001</div>'
         '<div style="position:absolute;left:60px;top:150px;font:700 96px Batang;color:#24180f">소현세자의 죽음</div>'
         '<div style="position:absolute;left:60px;top:300px;width:1080px;height:3px;background:#7a5c38"></div></div>', t7, E("o7") - t7, z=2)
    whip(t7); JS.append(f'tl.fromTo("#fold",{{y:900,rotation:4}},{{y:0,rotation:-1.5,duration:.55,ease:"expo.out"}},{t7:.3f});')
    tc = w("o7", "380년이"); cnt = nid("ct")
    clip(f'<div style="position:absolute;left:420px;top:540px;font:700 48px Malgun;color:#5a4128">1645 →</div><div style="position:absolute;left:640px;top:470px;font:400 150px Batang;color:#24180f"><span id="{cnt}">1645</span></div>', tc - 0.6, E("o7") - tc + 0.6, z=25)
    JS.append(f'(function(){{var o={{v:1645}};tl.to(o,{{v:2026,duration:1.2,ease:"power2.inOut",onUpdate:function(){{document.getElementById("{cnt}").textContent=Math.round(o.v)}}}},{tc - 0.5:.3f});}})();')
    for n in range(9): SFX.append(("tick", tc - 0.5 + n * 0.13))
    text(tc + 0.8, E("o7") - tc - 0.8, "380년 넘게 풀리지 않음", "left:420px;top:700px;font:700 54px Malgun;color:#a3171b")
    stamp(E("o7") - 1.1, 1.1, "미해결", 1120, 640, size=110, rot=-14); flash(E("o7") - 0.95, peak=.35)

    # ================= 1 사건 개요 — 증거판
    t8, tE = T("c1_0"), E("c1_3")
    clip(BG_DARK + '<div style="position:absolute;left:0;right:0;top:96px;text-align:center;font:700 34px Batang;color:#cdb98d;letter-spacing:.4em">사 건 개 요</div>', t8, tE - t8, z=2)
    whip(t8); camzoom(t8, tE, 1.1, 1.0)
    def polaroid(img, crop, x, y, rot, t, cap, t1, bright=1.0, z=24):
        i = nid("po"); cx, cy, cw, ch = crop; sc = 1 / cw
        clip(f'<div id="{i}" style="position:absolute;left:{x}px;top:{y}px;width:380px;padding:16px 16px 58px;background:#efe9dc;box-shadow:0 18px 40px rgba(0,0,0,.6);transform-origin:50% 0">'
             f'<div style="width:348px;height:260px;overflow:hidden;position:relative"><img src="assets/{img}.jpg" style="position:absolute;left:{-cx * sc * 100:.1f}%;top:{-cy * sc * 100:.1f}%;width:{sc * 100:.1f}%;height:{(1 / ch) * 100:.1f}%;object-fit:cover;filter:sepia(.35) contrast(1.05) brightness({bright})"></div>'
             f'<div style="position:absolute;left:0;right:0;bottom:12px;text-align:center;font:700 28px Malgun;color:#2a2018">{cap}</div>'
             f'<i style="position:absolute;left:176px;top:-12px;width:28px;height:28px;border-radius:50%;background:radial-gradient(circle at 35% 35%,#e24a4a,#7a0d10)"></i></div>', t, t1 - t, z=z)
        JS.append(f'tl.fromTo("#{i}",{{y:-120,opacity:0,rotation:{rot + 12}}},{{y:0,opacity:1,rotation:{rot},duration:.45,ease:"back.out(1.6)"}},{t:.3f});')
        SFX.append(("thud", t + 0.3)); return i
    def string(t, t1, d, z=26):
        i = nid("str"); clip(f'<svg style="position:absolute;inset:0" width="{W}" height="{H}"><path id="{i}" d="{d}" fill="none" stroke="#b0161b" stroke-width="5" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/></svg>', t, t1 - t, z=z)
        JS.append(f'tl.to("#{i}",{{attr:{{"stroke-dashoffset":0}},duration:1.0,ease:"power2.inOut"}},{t + .2:.3f});')
    polaroid("A3", (0.0, 0.08, 0.5, 0.5), 160, 150, -5, t8 + 0.4, "소현세자 (1612~1645)", tE)
    tk = w("c1_1", "왕"); polaroid("N11", (0.56, 0.24, 0.28, 0.28), 620, 120, 4, tk, "아버지 · 인조", tE, bright=1.9)
    tt = w("c1_2", "때"); polaroid("R_hwangyeong", (0.05, 0.05, 0.9, 0.9), 1100, 160, -3, tt, "창경궁 환경전 (오늘)", tE)
    string(tk, tE, "M350 170 Q 560 300 810 140 T 1290 180")
    td = w("c1_2", "1645년"); text(td, E("c1_2") - td + 0.1, "1645. 4. 26 (음력)", "left:1120px;top:520px;font:700 40px Malgun;color:#f1e6cf;background:#7a0d10;padding:8px 18px;transform:rotate(-3deg)")
    t11 = T("c1_3"); i = nid("tl")
    clip(f'<svg style="position:absolute;inset:0" width="{W}" height="{H}"><line id="{i}" x1="180" y1="640" x2="1740" y2="640" stroke="#e9dcc4" stroke-width="4" stroke-dasharray="1560" stroke-dashoffset="1560"/></svg>', t11, tE - t11, z=27)
    JS.append(f'tl.to("#{i}",{{attr:{{"stroke-dashoffset":0}},duration:.9,ease:"power2.out"}},{t11:.3f});')
    for x, top, bot, t in [(200, "1637", "심양으로", w("c1_3", "청나라에서")), (1240, "1645.2.18", "귀국", w("c1_3", "돌아온")), (1480, "4.23", "앓아누움", w("c1_3", "4월")), (1700, "4.26", "죽음", w("c1_3", "나흘째"))]:
        i = nid("mk")
        clip(f'<div id="{i}"><i style="position:absolute;left:{x - 14}px;top:626px;width:28px;height:28px;border-radius:50%;background:{"#c11c22" if bot == "죽음" else "#e9dcc4"}"></i>'
             f'<div style="position:absolute;left:{x - 110}px;width:220px;top:560px;text-align:center;font:700 34px Malgun;color:#f1e6cf">{top}</div>'
             f'<div style="position:absolute;left:{x - 110}px;width:220px;top:670px;text-align:center;font:700 28px Malgun;color:rgba(241,230,207,.75)">{bot}</div></div>', t, tE - t, z=28)
        JS.append(f'tl.fromTo("#{i}",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.3,ease:"expo.out"}},{t:.3f});'); SFX.append(("tick", t))
    tb = w("c1_3", "두"); i = nid("br")
    clip(f'<div id="{i}" style="position:absolute;left:1240px;top:700px;width:460px;height:24px;border:4px solid #c11c22;border-top:none"><div style="position:absolute;left:0;right:0;top:30px;text-align:center;font:700 34px Malgun;color:#e8503a">두 달 남짓</div></div>', tb, tE - tb, z=29)
    JS.append(f'tl.fromTo("#{i}",{{scaleX:0}},{{scaleX:1,duration:.4,ease:"power3.out",transformOrigin:"0 0"}},{tb:.3f});')
    # 공식 기록: 병사
    photo("R_sillokpage", T("c1_4"), E("c1_4"), "실록의 한 면", "초고(중초본) · 실록은 왕이 죽은 뒤 펴냄")
    stamp(w("c1_4", "병을"), E("c1_4") - w("c1_4", "병을"), "공식 기록 : 병사(病死)", 560, 420, size=72, rot=-4, color="#d8c9a8")
    # 그런데 같은 실록이 — 얼굴 쪽으로 다가가며 붉은 잉크
    shot("A1", T("c1_5"), E("c1_5") - T("c1_5"), crop=(0.36, 0.5, 0.36, 0.36), move=(1.0, 1.25, 0, 0, 0, 0), flick=(60, 80), grade="saturate(.7)")
    ink(w("c1_5", "이상한"), 960, 560, 200, E("c1_5") - w("c1_5", "이상한"), z=8, color="#5e0a0c")
    # 병? / 살해? — 관 앞
    shot("N7", T("c1_6"), E("c1_6") - T("c1_6"), crop=(0.0, 0.3, 0.65, 0.65), move=(1.05, 1.0, 0, 0, 0, 0), flick=(85, 72), dust=10, bright=0.8)
    big(w("c1_6", "병으로"), E("c1_6"), "병?", "left:300px;top:360px;font:700 150px Malgun;color:#f1e6cf", sound="tick")
    big(w("c1_6", "누군가에게"), E("c1_6"), "누군가?", "left:1120px;top:360px;font:700 150px Malgun;color:#e8503a")
    # 단서를 하나씩 — 빈 단서 다섯 칸
    tracker(T("c1_7"), E("c1_7") - CARD, None, filled=0)

    # ================= 2 단서 1 — 염습실의 얼굴
    chapter_card("c2_0", 1)
    photo("R_sillok", T("c2_0"), E("c2_0"), "다시, 실록", "인조실록 · 1645년 6월 27일 기사")
    pid = paper(T("c2_1"), E("c2_1"), "仁祖實錄 · 인조 23년(1645) 6월 27일 — 다시 읽기",
                [("검은 천으로 얼굴 반쪽만 덮어 놓았으나,", "c2_1", "검은"), ("곁에 있는 사람도", "c2_1", "곁에"), ("그 얼굴빛을 알아볼 수 없어서,", "c2_1", "그"),
                 ("마치 약물에 중독되어 죽은 사람과 같았다.", "c2_1", "마치")], under=("c2_1", "같았다", 1340, 1540, 672), fs=58, gap=108)
    HTML.append("</div>")
    # 짚어 둘 두 가지
    t = T("c2_2")
    clip(BG_DARK, t, E("c2_5") - t, z=2); whip(t)
    big(w("c2_2", "두"), E("c2_2"), "짚어 둘 것 2", "left:0;right:0;top:420px;text-align:center;font:700 110px Batang;color:#e9dcc4", sound="thud")
    # 하나: 야사 ✕ / 공식 역사
    t3 = T("c2_3")
    big(w("c2_3", "하나"), E("c2_3"), "①", "left:120px;top:130px;font:700 90px Batang;color:#e8503a", sound="tick")
    i = nid("ys"); clip(f'<div id="{i}" style="position:absolute;left:200px;top:330px;width:620px;height:380px;border-radius:10px;background:#2a2622;border:3px dashed #8c7a5a;text-align:center">'
                        f'<div style="font:700 70px Batang;color:#a99a80;margin-top:100px">야사</div><div style="font:700 34px Malgun;color:#8c7a5a;margin-top:18px">떠도는 이야기 모음</div></div>', w("c2_3", "소문을"), E("c2_3") - w("c2_3", "소문을"), z=10)
    JS.append(f'tl.fromTo("#{i}",{{opacity:0,x:-60}},{{opacity:1,x:0,duration:.35,ease:"expo.out"}},{w("c2_3", "소문을"):.3f});')
    strike(w("c2_3", "아니라"), 220, 520, 580, E("c2_3"))
    camzoom(T("c2_3"), E("c2_3"), 1.0, 1.07)
    i = nid("gs"); tg = w("c2_3", "나라가")
    clip(f'<div id="{i}" style="position:absolute;left:1100px;top:300px;width:640px;height:440px;border-radius:10px;overflow:hidden;box-shadow:0 0 0 6px #e8503a,0 30px 60px rgba(0,0,0,.6)">'
         f'<img src="assets/N10.jpg" style="position:absolute;left:-110%;top:-35%;width:260%;height:260%;object-fit:cover;filter:brightness(1.2)">'
         f'<div style="position:absolute;left:0;right:0;bottom:0;padding:16px;background:rgba(0,0,0,.65);text-align:center;font:700 44px Malgun;color:#f6ecd8">공식 역사 · 실록</div></div>', tg, E("c2_3") - tg, z=10)
    JS.append(f'tl.fromTo("#{i}",{{opacity:0,scale:.85}},{{opacity:1,scale:1,duration:.4,ease:"back.out(1.5)"}},{tg:.3f});'); SFX.append(("thud", tg + .2))
    # 둘: '독을 먹었다' ✕ → '같았다'
    big(w("c2_4", "둘"), E("c2_5"), "②", "left:120px;top:130px;font:700 90px Batang;color:#e8503a", sound="tick")
    ta = w("c2_4", "'독을", 0) if any(x[0].startswith("'독을") for x in BK["c2_4"]["words"]) else w("c2_4", "독을")
    i = text(ta, E("c2_4") - ta, "독을 먹었다", "left:0;right:0;top:360px;text-align:center;font:700 120px Batang;color:#e9dcc4")
    strike(w("c2_4", "않습니다"), 620, 440, 680, E("c2_4"))
    t5 = T("c2_5")
    i = text(t5, E("c2_5") - t5, '중독된 사람과 <span id="hl" style="background:linear-gradient(transparent 55%,rgba(211,38,44,.75) 55%);background-size:0% 100%;background-repeat:no-repeat">같았다</span>',
             "left:0;right:0;top:330px;text-align:center;font:700 110px Batang;color:#f1e6cf")
    JS.append(f'tl.to("#hl",{{backgroundSize:"100% 100%",duration:.4,ease:"power2.out"}},{t5 + 0.9:.3f});')
    chip(w("c2_5", "그렇게"), E("c2_5"), "= 그렇게 보였다", 760, 560, size=54)
    # 본 사람은 있다 → 알 수 없음
    shot("A1", T("c2_6"), E("c2_6") - T("c2_6"), crop=(0.0, 0.0, 0.46, 0.46), move=(1.15, 1.05, 2, 0, 0, 0), flick=(95, 95), bright=1.15)
    label(T("c2_6") + .2, E("c2_6"), "본 사람", "종친 집안 사람 · 실록이 전한 증언", x=1180, y=640)
    tracker(T("c2_7"), E("c2_7"), None, filled=1)
    stamp(w("c2_7", "알"), E("c2_7") - w("c2_7", "알"), "판단 보류", 1460, 140, size=54, rot=-8)
    # 누구였나 / 누가
    shot("A3", T("c2_8"), w("c2_8", "누가") - T("c2_8"), crop=(0.0, 0.05, 0.5, 0.5), move=(1.0, 1.1, 0, 0, 0, 0), grade="saturate(.75)")
    shot("N11", w("c2_8", "누가"), E("c2_8") - w("c2_8", "누가"), crop=(0.58, 0.26, 0.24, 0.24), move=(1.0, 1.15, 0, 0, 0, 0), bright=2.0, flick=(30, 40))
    SFX.append(("hit", w("c2_8", "누가")))

    # ================= 3 인물 기록
    chapter_card("c3_0", "P")
    E_AS = vb(126, 39, 30)
    mapscene(T("c3_0"), E("c3_0"), vb(120, 38, 70), vb(127, 37.6, 8), pins=[("한양", w("c3_0", "한강"), False)],
             notes=[(128.3, 37.15, "삼전도", w("c3_0", "삼전도"), 1.0)])
    tag(T("c3_0"), E("c3_0"), "1637년 정월 · 삼전도")
    photo("R_namhan", T("c3_1"), w("c3_1", "청나라"), "남한산성", "인조가 47일을 버틴 산성 (오늘)", mode="full")
    photo("R_hongtaiji", w("c3_1", "청나라"), w("c3_1", "무릎을"), "청 태종 홍타이지", "항복을 받은 황제")
    photo("R_samjeondo", w("c3_1", "무릎을"), E("c3_1"), "삼전도비", "항복을 새겨 세운 비석 (1639) · 서울 송파")
    shot("A2", T("c3_2"), E("c3_2") - T("c3_2"), crop=(0.0, 0.25, 0.4, 0.4), move=(1.0, 1.12, 0, 0, 0, 0), dust=30)
    big(w("c3_2", "스물다섯의"), E("c3_2"), "25", "right:200px;top:280px;font:400 220px Batang;color:rgba(240,228,205,.85)")
    t = T("c3_3"); clip('<div style="position:absolute;inset:0;background:#080707"></div>', t, E("c3_3") - t, z=2)
    i = text(t + .1, E("c3_3") - t - .1, '항복의 조건', "left:0;right:0;top:330px;text-align:center;font:700 70px Malgun;color:#a99a80")
    big(w("c3_3", "사람이었습니다"), E("c3_3"), "사람", "left:0;right:0;top:440px;text-align:center;font:700 200px Batang;color:#e8503a")
    mapscene(T("c3_4"), E("c3_4"), vb(126, 39.5, 20), vb(125, 39.2, 16), pins=[("한양", T("c3_4") + .1, False), ("심양", w("c3_4", "심양으로"), True)],
             routes=[("한양", "심양", w("c3_4", "수도"), .18, False)])
    for n, (s, wd) in enumerate([("세자", "세자는"), ("세자빈 강씨", "강씨"), ("봉림대군", "봉림대군과")]):
        chip(w("c3_4", wd), E("c3_4"), s, 120, 200 + n * 90, bg="rgba(40,34,26,.92)", size=34)
    # 심양관: 창살이 열림
    t = T("c3_5"); te = E("c3_5")
    broll("C_mukden_drone1", t, te, 1)
    bars = "".join(f'<i style="position:absolute;top:0;bottom:0;left:{60 + n * 150}px;width:26px;background:linear-gradient(90deg,#1a1714,#4a4238,#1a1714)"></i>' for n in range(12))
    bl, br = nid("bl"), nid("br")
    clip(f'<div id="{bl}" style="position:absolute;left:0;top:0;bottom:0;width:960px;overflow:hidden;background:rgba(0,0,0,.55)">{bars}</div><div id="{br}" style="position:absolute;left:960px;top:0;bottom:0;width:960px;overflow:hidden;background:rgba(0,0,0,.55)">{bars}</div>', t, te - t, z=5)
    td_ = w("c3_5", "달랐습니다")
    JS.append(f'tl.to("#{bl}",{{xPercent:-100,duration:.6,ease:"power3.in"}},{td_ - .2:.3f});tl.to("#{br}",{{xPercent:100,duration:.6,ease:"power3.in"}},{td_ - .2:.3f});'); SFX.append(("whoosh", td_))

    shot("N2", T("c3_6"), w("c3_6", "세자가") - T("c3_6"), crop=(0.35, 0.3, 0.6, 0.6), move=(1.0, 1.08, 0, 2, 0, 0), flick=(37, 72))
    shot("N2", w("c3_6", "세자가"), E("c3_6") - w("c3_6", "세자가"), crop=(0.0, 0.05, 0.5, 0.5), move=(1.0, 1.1, 0, 0, 0, 0))
    chip(w("c3_6", "요구를", 1), E("c3_6"), "요구 ↓ 줄이려 버팀", 1180, 760, size=40)
    shot("N1", T("c3_7"), w("c3_7", "거둔") - T("c3_7"), move=(1.05, 1.12, -2, 1, 0, 0), dust=22)
    shot("N12", w("c3_7", "거둔"), E("c3_7") - w("c3_7", "거둔"), crop=(0.42, 0.2, 0.55, 0.55), move=(1.0, 1.1, 2, -2, 0, 0), dust=16)
    chip(w("c3_7", "땅을"), E("c3_7"), "농사", 1400, 220, size=40); chip(w("c3_7", "장사도"), E("c3_7"), "장사", 1560, 300, size=40)
    shot("N10", T("c3_8"), E("c3_8") - T("c3_8"), crop=(0.45, 0.2, 0.45, 0.45), move=(1.0, 1.1, 0, 0, 0, 0), flick=(50, 45))
    pid = paper(T("c3_9"), E("c3_9"), "仁祖實錄 · 한양에 전해진 심양 소식",
                [("관소의 문이 마치 시장 같았으므로,", "c3_9", "관소의"), ("상이 그 사실을 듣고", "c3_9", "상이"), ("불평스럽게 여겼다.", "c3_9", "불평스럽게")],
                under=("c3_9", "불평스럽게", 320, 660, 615), fs=66, gap=130)
    HTML.append("</div>")
    # 소문 — 왕 곁
    t = T("c3_10"); te = E("c3_10")
    shot("N11", t, te - t, crop=(0.45, 0.15, 0.45, 0.45), move=(1.0, 1.12, 0, 0, 0, 0), bright=1.7, flick=(40, 40), dust=12)
    for n, (s, wd, x, y) in enumerate([("청나라의 힘을 빌려…", "청나라의", 180, 300), ("아버지의 자리를…", "아버지의", 1100, 520)]):
        i = text(w("c3_10", wd), te - w("c3_10", wd), s, f"left:{x}px;top:{y}px;font:italic 700 64px Batang;color:rgba(240,220,190,.85);text-shadow:0 0 18px #000")
        JS.append(f'tl.to("#{i}",{{x:{40 if n else -40},y:-30,opacity:.5,duration:{te - w("c3_10", wd):.2f},ease:"none"}},{w("c3_10", wd) + .25:.3f});')
    chip(t + .3, te, "소문 · 출처 한정", 110, 150, bg="rgba(60,60,60,.9)", size=30)
    mapscene(T("c3_11"), E("c3_11"), vb(125, 39.2, 16), vb(125, 39.2, 15), pins=[("한양", T("c3_11"), False), ("심양", T("c3_11"), False)],
             routes=[("한양", "심양", w("c3_11", "심양관에"), -.15, True)])
    chip(T("c3_11") + .3, E("c3_11"), "한 연구자의 서술", 110, 150, bg="rgba(60,60,60,.9)", size=30)
    big(w("c3_11", "몰래"), E("c3_11"), "몰래 살핌", "left:150px;top:560px;font:700 70px Malgun;color:#f1e6cf", sound="tick")
    # 1644
    t = T("c3_12"); clip(BG_DARK, t, E("c3_12") - t, z=2)
    big(w("c3_12", "1644년"), E("c3_12"), "1644", "left:0;right:0;top:300px;text-align:center;font:400 260px Batang;color:#e9dcc4")
    flash(w("c3_12", "1644년"), peak=.4)
    i = text(w("c3_12", "주인이"), E("c3_12") - w("c3_12", "주인이"), "明 → 淸", "left:0;right:0;top:640px;text-align:center;font:700 90px Batang;color:#e8503a")
    shot("N3", T("c3_13"), w("c3_13", "명의") - T("c3_13"), move=(1.0, 1.14, 0, 0, 2, -2))
    photo("R_jingshan", w("c3_13", "명의"), E("c3_13"), "베이징 경산", "명의 마지막 황제 숭정제가 목숨을 끊은 자리")
    tag(T("c3_13"), w("c3_13", "명의"), "1644년 봄 · 베이징")
    flash(w("c3_13", "무너뜨리고"), color="255,150,60", peak=.35); SFX.append(("hit", w("c3_13", "무너뜨리고")))
    broll("MK_greatwall", T("c3_14"), w("c3_14", "넘어온") + 0.3, 4)
    photo("R_shanhai", w("c3_14", "넘어온") + 0.3, w("c3_14", "청나라"), "산해관", "만리장성 동쪽 끝 관문 (옛 그림)")
    mapscene(w("c3_14", "청나라"), E("c3_14"), vb(120, 40.5, 14), vb(118, 40, 9), pins=[("산해관", w("c3_14", "청나라"), False), ("베이징", w("c3_14", "베이징에"), True)],
             routes=[("산해관", "베이징", w("c3_14", "군대가"), .12, False)])
    mapscene(T("c3_15"), E("c3_15"), vb(118, 40, 20), vb(55, 46, 150), zmove=(w("c3_15", "영국에서는"), vb(5, 51, 34)),
             pins=[("베이징", T("c3_15"), False), ("독일", w("c3_15", "유럽은"), True), ("런던", w("c3_15", "영국에서는"), True)],
             notes=[(10, 47.5, "'30년 전쟁' 막바지", w("c3_15", "'30년") if any(x[0].startswith("'30년") for x in BK["c3_15"]["words"]) else w("c3_15", "전쟁"), 1.0),
                    (-1.5, 54.5, "왕과 의회의 내전", w("c3_15", "왕과"), .7)], fsw=vb(5, 51, 34)[2])
    mapscene(T("c3_16"), E("c3_16"), vb(5, 51, 34), vb(121, 40.5, 14), pins=[("심양", T("c3_16") + 1.6, False), ("베이징", w("c3_16", "베이징에"), True)],
             routes=[("심양", "베이징", w("c3_16", "베이징에"), .12, False)])
    big(w("c3_16", "70일"), E("c3_16"), "70일", "left:1300px;top:560px;font:400 150px Batang;color:#f1e6cf", sound="tick")
    shot("A3", T("c3_17"), w("c3_17", "천문대였습니다") - T("c3_17"), crop=(0.38, 0.0, 0.4, 0.4), move=(1.0, 1.1, 0, 0, 0, 2), dust=20)
    photo("R_obs5", w("c3_17", "천문대였습니다"), E("c3_17"), "베이징 고관상대", "명·청의 천문대 · 지금도 남은 관측 기구", mode="full")
    photo("R_schall", T("c3_18"), E("c3_18"), "아담 샬 (1592~1666)", "독일인 예수회 신부 · 천문학자 · 17세기 판화")
    # 시헌력 달력
    t = T("c3_19"); te = E("c3_19"); cal = nid("cal")
    cells = "".join(f'<i id="{cal}c{n}" style="position:absolute;left:{70 + (n % 10) * 64}px;top:{230 + (n // 10) * 64}px;width:54px;height:54px;border:2px solid #7a5c38;opacity:0"></i>' for n in range(50))
    clip(BG_DARK + f'<div style="position:absolute;left:560px;top:120px;width:800px;height:820px;background:radial-gradient(ellipse at 30% 20%,#e9dcbc,#c9b487);box-shadow:0 30px 80px rgba(0,0,0,.7)">'
         f'<div style="position:absolute;left:70px;top:60px;font:700 90px Batang;color:#24180f">時憲曆</div>{cells}</div>', t, te - t, z=2)
    whip(t)
    for n in range(50):
        JS.append(f'tl.to("#{cal}c{n}",{{opacity:1,duration:.05}},{w("c3_19", "새") + n * 0.035:.3f});')
    chip(w("c3_19", "이듬해부터"), te, "1645년부터 청 전역", 1240, 760, size=36)
    stamp(w("c3_19", "시헌력"), te - w("c3_19", "시헌력"), "시헌력", 1000, 560, size=86, rot=-8)
    shot("A3", T("c3_20"), E("c3_20") - T("c3_20"), crop=(0.3, 0.32, 0.38, 0.38), move=(1.0, 1.15, 0, 0, 0, 0), dust=16)
    g = nid("gl"); clip(f'<div id="{g}" style="position:absolute;left:48%;top:50%;width:620px;height:620px;margin:-310px;border-radius:50%;mix-blend-mode:screen;background:radial-gradient(circle,rgba(255,200,120,.55),transparent 65%)"></div>', T("c3_20"), E("c3_20") - T("c3_20"), z=6)
    JS.append(f'tl.fromTo("#{g}",{{opacity:0,scale:.6}},{{opacity:1,scale:1.15,duration:{E("c3_20") - T("c3_20"):.2f},ease:"sine.inOut"}},{T("c3_20"):.3f});')
    for n, (s, wd) in enumerate([("천문서", "천문과"), ("수학서", "수학의"), ("지구의", "둥근")]):
        chip(w("c3_20", wd), E("c3_20"), s, 110, 200 + n * 90, bg="rgba(40,34,26,.92)", size=36)
    # 무너지는 제국 / 일어서는 제국
    t = T("c3_21"); te = E("c3_21"); half = 'position:absolute;top:0;bottom:0;overflow:hidden'; sp = nid("sp")
    clip(f'<div id="{sp}a" style="{half};left:0;width:50%"><img src="assets/N3.jpg" style="position:absolute;left:-40%;top:0;height:100%"></div>'
         f'<div id="{sp}b" style="{half};left:50%;width:50%"><img src="assets/N4.jpg" style="position:absolute;left:-30%;top:0;height:100%"></div>'
         f'<div style="position:absolute;left:50%;top:0;bottom:0;width:4px;background:#c11c22"></div>', t, te - t, z=3)
    JS.append(f'tl.fromTo("#{sp}a",{{xPercent:-100}},{{xPercent:0,duration:.5,ease:"expo.out"}},{t:.3f});tl.fromTo("#{sp}b",{{xPercent:100}},{{xPercent:0,duration:.5,ease:"expo.out"}},{w("c3_21", "일어서는"):.3f});')
    big(w("c3_21", "무너지는"), te, "명 · 무너짐", "left:200px;top:120px;font:700 80px Malgun;color:#f1e6cf", sound="whoosh")
    big(w("c3_21", "일어서는"), te, "청 · 일어섬", "left:1160px;top:120px;font:700 80px Malgun;color:#f1e6cf", sound="whoosh")
    mapscene(T("c3_22"), E("c3_22"), vb(116.4, 39.9, 10), vb(121.5, 38.6, 16), pins=[("베이징", T("c3_22"), False), ("한양", w("c3_22", "조정으로"), True)],
             routes=[("베이징", "한양", w("c3_22", "아버지의"), .2, False)])
    ip = nid("in")
    clip(f'<div id="{ip}" style="position:absolute;right:120px;top:140px;width:520px;height:300px;overflow:hidden;border:3px solid #a3171b;box-shadow:0 20px 50px rgba(0,0,0,.7)"><img src="assets/N11.jpg" style="position:absolute;left:-200%;top:-80%;width:400%;height:400%;object-fit:cover;filter:brightness(2)"></div>', w("c3_22", "아버지의"), E("c3_22") - w("c3_22", "아버지의") - CARD, z=8)
    JS.append(f'tl.fromTo("#{ip}",{{opacity:0,scale:.8}},{{opacity:1,scale:1,duration:.35,ease:"back.out(1.6)"}},{w("c3_22", "아버지의"):.3f});')

    # ================= 4 단서 2 — 차가운 귀국
    chapter_card("c4_0", 2)
    shot("N5", T("c4_0"), E("c4_0") - T("c4_0"), move=(1.1, 1.02, 2, 0, 0, 0), fg=("linear-gradient(90deg,transparent 55%,#000 66%,#000 100%)", 2.2), dust=16)
    tag(T("c4_0"), E("c4_0"), "1645년 2월 18일 · 한양")
    t = T("c4_1"); te = E("c4_2"); rows = nid("rw")
    shot("N5", t, te - t, crop=(0.0, 0.4, 0.6, 0.6), move=(1.0, 1.08, 0, 0, 0, 0), bright=1.1)
    ghosts = "".join(f'<i class="{rows}g" style="position:absolute;left:{220 + (n % 8) * 170}px;top:{480 + (n // 8) * 150}px;width:90px;height:130px;border:3px dashed rgba(255,220,170,.8);border-radius:45px 45px 8px 8px"></i>' for n in range(16))
    clip(f'<div id="{rows}">{ghosts}</div>', w("c4_1", "신하들이"), te - w("c4_1", "신하들이"), z=6)
    JS.append(f'tl.fromTo(".{rows}g",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.25,stagger:.04}},{w("c4_1", "신하들이"):.3f});')
    label(w("c4_1", "축하를"), E("c4_1"), "하례", "돌아온 세자를 축하하는 의식", x=110, y=150)
    JS.append(f'tl.to(".{rows}g",{{opacity:0,y:-30,duration:.25,stagger:.03}},{w("c4_2", "막았습니다") - .1:.3f});')
    stamp(w("c4_2", "막았습니다"), te - w("c4_2", "막았습니다"), "하례 금지", 700, 360, size=110, rot=-8)
    shot("N5", T("c4_3"), E("c4_3") - T("c4_3"), crop=(0.12, 0.25, 0.45, 0.45), move=(1.0, 1.12, 0, 0, 0, 0), dust=14)
    for n, (s, wd) in enumerate([("서양의 책", "서양의"), ("지구의 · 물건", "물건들은")]):
        chip(w("c4_3", wd), E("c4_3"), s, 1300, 200 + n * 90, bg="rgba(40,34,26,.92)", size=36)
    rd = nid("rd"); clip(f'<div id="{rd}" style="position:absolute;inset:0;background:radial-gradient(circle,transparent 30%,rgba(150,10,14,.6));opacity:0"></div>', w("c4_3", "노여움을"), E("c4_3") - w("c4_3", "노여움을"), z=7)
    JS.append(f'tl.to("#{rd}",{{opacity:1,duration:.5}},{w("c4_3", "노여움을"):.3f});'); SFX.append(("hit", w("c4_3", "노여움을")))
    t = T("c4_4"); te = E("c4_4"); sp = nid("sp")
    clip(f'<div id="{sp}a" style="{half};left:0;width:50%"><img src="assets/N5.jpg" style="position:absolute;left:-110%;top:0;height:100%"></div>'
         f'<div id="{sp}b" style="{half};left:50%;width:50%"><img src="assets/N11.jpg" style="position:absolute;left:-146%;top:-30%;height:140%;filter:brightness(1.9)"></div>'
         f'<div style="position:absolute;left:50%;top:0;bottom:0;width:4px;background:#c11c22"></div>', t, te - t, z=3)
    JS.append(f'tl.fromTo("#{sp}a",{{xPercent:-100}},{{xPercent:0,duration:.5,ease:"expo.out"}},{t:.3f});tl.fromTo("#{sp}b",{{xPercent:100}},{{xPercent:0,duration:.5,ease:"expo.out"}},{w("c4_4", "아버지는"):.3f});')
    SFX.append(("whoosh", t)); SFX.append(("whoosh", w("c4_4", "아버지는")))
    big(w("c4_4", "8년"), te, "아들 · 8년 만의 귀국", "left:120px;top:120px;font:700 54px Malgun;color:#f1e6cf", sound=None)
    big(w("c4_4", "반기지"), te, "반기지 않음", "left:1080px;top:120px;font:700 54px Malgun;color:#e8503a", sound="thud")
    shot("N6", T("c4_5"), E("c4_5") - T("c4_5") - CARD, crop=(0.25, 0.1, 0.55, 0.55), move=(1.12, 1.0, 0, 0, 0, 0), flick=(85, 80), bright=.9)
    big(w("c4_5", "두"), E("c4_5") - CARD, "2개월", "right:150px;top:150px;font:400 150px Batang;color:rgba(240,228,205,.9)", sound="tick")

    # ================= 5 단서 3 — 석 달 전에 온 의관
    chapter_card("c5_0", 3)
    shot("N6", T("c5_0"), w("c5_0", "의관") - T("c5_0"), crop=(0.25, 0.1, 0.55, 0.55), move=(1.0, 1.08, 0, 0, 0, 0), flick=(85, 80))
    tag(T("c5_0"), E("c5_0"), "1645년 4월 23일")
    shot("N6", w("c5_0", "의관"), E("c5_0") - w("c5_0", "의관"), crop=(0.0, 0.5, 0.5, 0.5), move=(1.0, 1.15, 0, 0, 0, 0), flick=(80, 60))
    label(w("c5_0", "이형익이"), E("c5_0"), "의관 이형익", "얼굴은 기록에 없음 · 재현", x=1160, y=150)
    # 증거판: 의관 — 조씨 — 왕
    t = T("c5_1"); te = E("c5_4")
    clip(BG_DARK + '<div style="position:absolute;left:0;right:0;top:96px;text-align:center;font:700 34px Batang;color:#cdb98d;letter-spacing:.4em">단 서 3</div>', t, te - t, z=2)
    whip(t); camzoom(t, te, 1.0, 1.06)
    polaroid("N6", (0.0, 0.45, 0.55, 0.55), 220, 200, -4, t + .3, "의관 이형익", te)
    tm = w("c5_2", "석"); i = nid("tl")
    clip(f'<svg style="position:absolute;inset:0" width="{W}" height="{H}"><line id="{i}" x1="200" y1="740" x2="1720" y2="740" stroke="#e9dcc4" stroke-width="4" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/></svg>', tm, te - tm, z=27)
    JS.append(f'tl.to("#{i}",{{attr:{{"stroke-dashoffset":0}},duration:.7,ease:"power2.out"}},{tm:.3f});')
    for x, s, t_ in [(260, "1645년 초 · 특채", w("c5_2", "석")), (1640, "4.23 · 침", w("c5_2", "뽑혀"))]:
        chip(t_, te, s, x - 120, 770, bg="rgba(40,34,26,.92)", size=30)
    big(w("c5_2", "석"), te, "석 달", "left:860px;top:620px;font:700 80px Malgun;color:#e8503a", sound="tick")
    ts = w("c5_3", "후궁"); i = nid("sil")
    clip(f'<div id="{i}" style="position:absolute;left:1240px;top:160px;width:380px;height:334px;background:#efe9dc;box-shadow:0 18px 40px rgba(0,0,0,.6);transform:rotate(3deg)">'
         f'<div style="position:absolute;left:16px;top:16px;width:348px;height:260px;background:#2a2622;text-align:center;font:700 150px Batang;color:#6d6455;line-height:260px">?</div>'
         f'<div style="position:absolute;left:0;right:0;bottom:12px;text-align:center;font:700 28px Malgun;color:#2a2018">후궁 조씨의 집안</div></div>', ts, te - ts, z=24)
    JS.append(f'tl.fromTo("#{i}",{{y:-120,opacity:0}},{{y:0,opacity:1,duration:.45,ease:"back.out(1.6)"}},{ts:.3f});'); SFX.append(("thud", ts + .3))
    polaroid("N11", (0.56, 0.24, 0.28, 0.28), 760, 120, 2, w("c5_3", "왕의"), "총애한 왕 · 인조", te, bright=1.9)
    string(w("c5_3", "얽힌"), te, "M410 210 Q 700 420 1430 180")
    string(w("c5_3", "총애를"), te, "M950 140 Q 1150 60 1430 180", z=25)
    chip(w("c5_3", "얽힌"), te, "한 사전에만 있는 내용", 1240, 560, bg="rgba(60,60,60,.9)", size=28)
    JS.append(f'tl.to("#cam",{{scale:1.18,x:-150,y:90,duration:1.2,ease:"power2.inOut"}},{T("c5_4"):.3f});tl.set("#cam",{{x:0,y:0}},{te:.3f});')
    # 사흘 뒤
    t = T("c5_5"); te = E("c5_5") - CARD
    shot("N7", t, te - t, crop=(0.62, 0.5, 0.36, 0.36), move=(1.0, 1.12, 0, 0, 0, 0), flick=(55, 55))
    cn = nid("dc")
    clip(f'<div style="position:absolute;right:160px;top:160px;font:400 150px Batang;color:rgba(240,228,205,.9)">4.<span id="{cn}">23</span></div>', t + .2, te - t - .2, z=20)
    JS.append(f'(function(){{var o={{v:23}};tl.to(o,{{v:26,duration:1.0,ease:"steps(3)",onUpdate:function(){{document.getElementById("{cn}").textContent=Math.round(o.v)}}}},{w("c5_5", "사흘"):.3f});}})();')
    for n in range(3): SFX.append(("tick", w("c5_5", "사흘") + n * .33))
    SFX.append(("hit", w("c5_5", "숨을")))

    # ================= 6 단서 4 — 묻지 않은 왕
    chapter_card("c6_0", 4)
    t = T("c6_0"); te = E("c6_2")
    shot("N11", t, te - t, crop=(0.2, 0.1, 0.8, 0.8), move=(1.0, 1.12, 0, 0, 0, 0), bright=1.6, flick=(40, 40), dust=12)
    for n in range(5):
        i = nid("pt"); tt = w("c6_0", "벌하라고") + n * .12
        clip(f'<div id="{i}" style="position:absolute;left:{200 + n * 290}px;top:{220 + (n % 2) * 70}px;width:150px;height:430px;background:linear-gradient(#e9dcbc,#cdb98d);box-shadow:0 14px 30px rgba(0,0,0,.6);'
             f'font:700 40px/150px Batang;color:#2a1d14;writing-mode:vertical-rl;padding:30px 0;text-align:center">의관을 벌하소서</div>', tt, E("c6_0") - tt, z=10)
        JS.append(f'tl.fromTo("#{i}",{{y:700,rotation:{(n - 2) * 6}}},{{y:0,rotation:{(n - 2) * 3},duration:.45,ease:"expo.out"}},{tt:.3f});')
    SFX.append(("whoosh", w("c6_0", "벌하라고")))
    chip(T("c6_0") + .3, E("c6_0"), "신하들의 요구", 110, 140, bg="rgba(40,34,26,.92)", size=32)
    stamp(w("c6_1", "받아들이지"), E("c6_1") - w("c6_1", "받아들이지"), "불허", 760, 380, size=150, rot=-10)
    i = nid("ck")
    clip(f'<div id="{i}" style="position:absolute;left:560px;top:330px;width:800px;padding:40px 50px;background:rgba(12,11,10,.85);border:2px solid #8c7a5a">'
         f'<div style="font:700 44px Malgun;color:#cdb98d">죽음의 까닭 조사</div><div style="font:700 96px Batang;color:#e8503a;margin-top:10px">없음</div></div>', T("c6_2"), E("c6_2") - T("c6_2"), z=12)
    JS.append(f'tl.fromTo("#{i}",{{opacity:0,y:40}},{{opacity:1,y:0,duration:.35,ease:"expo.out"}},{T("c6_2"):.3f});'); SFX.append(("thud", w("c6_2", "따지지도")))
    t = T("c6_3"); te = E("c6_3")
    shot("N7", t, te - t, crop=(0.0, 0.3, 0.65, 0.65), move=(1.0, 1.1, 0, 0, 0, -2), flick=(85, 72), dust=10)
    for n in range(4):
        i = nid("pp"); tt = w("c6_3", "줄이고") + n * .1
        clip(f'<i id="{i}" style="position:absolute;left:{1300 + n * 120}px;top:180px;width:70px;height:110px;border-radius:35px 35px 6px 6px;background:rgba(255,220,170,.85)"></i>', w("c6_3", "입관에"), te - w("c6_3", "입관에"), z=9)
        JS.append(f'tl.fromTo("#{i}",{{opacity:0}},{{opacity:1,duration:.2}},{w("c6_3", "입관에"):.3f});')
        if n < 3: JS.append(f'tl.to("#{i}",{{opacity:.08,duration:.25}},{tt:.3f});')
    label(w("c6_3", "입관에"), te, "입관 · 지켜볼 사람을 줄임", None, x=1160, y=330)
    tclose = w("c6_3", "닫게")
    lid = nid("ld"); clip(f'<div id="{lid}" style="position:absolute;left:0;right:0;top:0;height:0;background:#050505"></div>', tclose, te - tclose, z=40)
    JS.append(f'tl.to("#{lid}",{{height:1080,duration:.35,ease:"power4.in"}},{tclose:.3f});')
    shake(tclose + .35); SFX.append(("hit", tclose + .33))
    shot("A3", T("c6_4"), E("c6_4") - T("c6_4"), crop=(0.08, 0.1, 0.38, 0.38), move=(1.05, 1.0, 0, 0, 0, 0), grade="grayscale(.85)", bright=.85)
    shot("N11", T("c6_5"), E("c6_5") - T("c6_5") - CARD, crop=(0.6, 0.27, 0.2, 0.2), move=(1.0, 1.25, 0, 0, 0, 0), bright=2.1)
    darkfade(E("c6_5") - CARD - 0.8, E("c6_5") - CARD, 0.05)

    # ================= 7 단서 5 — 지워지는 가족 (가계도 한 판)
    chapter_card("c7_0", 5)
    tf0 = T("c7_0"); tf1 = E("c7_1")
    family(tf0, tf1, [(w("c7_0", "맏아들"), "glow", "s1"), (w("c7_1", "봉림대군을"), "heir", None)])
    camzoom(tf0, tf1, 1.06, 1.0)
    shot("N9", T("c7_2"), E("c7_2") - T("c7_2"), crop=(0.15, 0.25, 0.7, 0.7), move=(1.0, 1.12, 0, 0, 0, 0), dust=10)
    tag(T("c7_2"), E("c7_2"), "1646년 초")
    big(w("c7_2", "독이"), E("c7_2"), "독?", "right:200px;top:300px;font:700 180px Malgun;color:#e8503a")
    shot("N8", T("c7_3"), E("c7_3") - T("c7_3"), crop=(0.55, 0.25, 0.42, 0.42), move=(1.0, 1.1, 0, 0, 0, 0), flick=(40, 50))
    label(w("c7_3", "강빈의"), E("c7_3"), "강빈", "소현세자의 아내", x=110, y=640)
    shot("N8", T("c7_4"), E("c7_4") - T("c7_4"), crop=(0.0, 0.2, 0.6, 0.6), move=(1.06, 1.0, 0, 0, 0, 0), bright=.7)
    big(w("c7_4", "인정하지"), E("c7_4"), "끝내 인정하지 않음", "left:0;right:0;top:420px;text-align:center;font:700 90px Batang;color:#f1e6cf", sound="thud")
    shot("N9", T("c7_5"), E("c7_5") - T("c7_5"), crop=(0.3, 0.32, 0.45, 0.45), move=(1.0, 1.18, 0, 0, 0, 0))
    tag(T("c7_5"), w("c7_5", "사약을"), "1646년 3월")
    photo("R_yeonghoe", w("c7_5", "사약을"), E("c7_5"), "영회원", "강빈의 무덤 · 경기 광명 (오늘)", mode="full")
    tf2 = T("c7_6"); tf3 = E("c7_7")
    family(tf2, tf3, [(tf2 + .05, "heir", None), (T("c7_6") + .3, "dim", "kang"), (w("c7_7", "친정어머니와"), "dim", "kin")])
    camzoom(tf2, tf3, 1.0, 1.06)
    big(w("c7_6", "1년이"), E("c7_6"), "1년이 채 안 됨", "left:1260px;top:170px;font:700 56px Malgun;color:#e8503a", sound=None)
    mapscene(T("c7_8"), E("c7_8"), vb(127, 36, 22), vb(126.8, 35.6, 18), pins=[("한양", T("c7_8"), False), ("제주", w("c7_8", "제주도로"), True)],
             routes=[("한양", "제주", w("c7_8", "바다"), .2, False)])
    shot("A4", T("c7_9"), E("c7_9") - T("c7_9"), crop=(0.42, 0.12, 0.45, 0.45), move=(1.0, 1.1, 0, 0, 0, 0), dust=30)
    big(w("c7_9", "네"), E("c7_9"), "4살", "right:200px;top:170px;font:400 170px Batang;color:rgba(240,228,205,.9)", sound="tick")
    chip(T("c7_9") + .3, E("c7_9"), "나이는 한 자료에만", 110, 140, bg="rgba(60,60,60,.9)", size=28)
    tf4 = T("c7_10"); tf5 = E("c7_14")
    fid = family(tf4, tf5, [(tf4 + .05, "heir", None), (T("c7_10") + .1, "dim", "kang"), (T("c7_10") + .1, "dim", "kin"), (w("c7_10", "숨집니다"), "dim", "s1"), (w("c7_11", "둘째도"), "dim", "s2"),
                            (w("c7_14", "막내"), "glow", "s3")])
    tag(T("c7_10"), E("c7_10"), "1648년 · 제주")
    big(w("c7_10", "열세"), E("c7_10"), "13", "left:110px;top:600px;font:400 120px Batang;color:#e8503a", sound="tick")
    camzoom(T("c7_12"), E("c7_13"), 1.0, 0.92)
    big(w("c7_12", "4년이"), E("c7_13"), "4년이 채 안 되어", "left:1240px;top:620px;font:700 52px Malgun;color:#f1e6cf", sound=None)
    shot("A4", w("c7_14", "막내"), E("c7_14") - w("c7_14", "막내") - CARD, crop=(0.55, 0.18, 0.3, 0.3), move=(1.0, 1.12, 0, 0, 0, 0), dust=20)

    # ================= 8 반대 증거
    chapter_card("c8_0", "X")
    t = T("c8_0"); te = E("c8_0")
    clip(BG_DARK, t, te - t, z=2); camzoom(t, te, 1.08, 1.0)
    for n, (img, crop, x, y, r, cap, br) in enumerate([("N5", (0.55, 0.1, 0.45, 0.45), 120, 160, -5, "단서 2 · 차가운 귀국", 1), ("N6", (0.0, 0.45, 0.55, 0.55), 520, 520, 4, "단서 3 · 의관", 1),
                                                     ("N7", (0.0, 0.3, 0.65, 0.65), 1300, 520, -3, "단서 4 · 묻지 않음", 1), ("A4", (0.42, 0.12, 0.45, 0.45), 1420, 140, 5, "단서 5 · 가족", 1)]):
        polaroid(img, crop, x, y, r, t + .1 + n * .15, cap, te, bright=br)
    polaroid("N11", (0.56, 0.24, 0.28, 0.28), 770, 200, 0, t + .8, "인조", te, bright=1.9, z=25)
    for d in ["M310 230 Q 600 260 960 280", "M710 600 Q 820 450 960 300", "M1490 600 Q 1200 450 960 300", "M1610 210 Q 1300 200 960 280"]:
        string(t + .9, te, d)
    pv = nid("pv")
    clip(BG_DARK + f'<div id="{pv}" style="position:absolute;left:360px;top:150px;width:1200px;height:780px;background:linear-gradient(#cfc3a6,#b8a782);border-radius:8px;box-shadow:0 30px 80px rgba(0,0,0,.8)">'
         f'<div style="position:absolute;left:60px;top:60px;font:700 36px Batang;color:#3a2c1c;letter-spacing:.2em">사건 파일 · 뒷면</div>'
         f'<div style="position:absolute;left:60px;top:170px;font:700 110px Batang;color:#24180f">반대 증거</div></div>', T("c8_1"), E("c8_1") - T("c8_1"), z=3)
    camzoom(T("c8_1"), E("c8_1"), 1.0, 1.08)
    JS.append(f'tl.fromTo("#{pv}",{{rotationY:90,transformPerspective:1600}},{{rotationY:0,duration:.6,ease:"back.out(1.3)"}},{T("c8_1"):.3f});'); SFX.append(("whoosh", T("c8_1")))
    shot("N10", T("c8_2"), E("c8_2") - T("c8_2"), crop=(0.5, 0.25, 0.42, 0.42), move=(1.0, 1.12, 0, 0, 0, 0), flick=(48, 40), dust=14)
    label(w("c8_2", "승정원일기가"), E("c8_2"), "승정원일기", "왕 곁의 날마다 기록", x=110, y=640, color="#8a8f98")
    t = T("c8_3"); te = E("c8_3")
    shot("N6", t, te - t, crop=(0.25, 0.1, 0.55, 0.55), move=(1.0, 1.1, 0, 0, 0, 0), flick=(85, 80), grade="saturate(.6)")
    for n, wd in enumerate(["기침과", "열,", "숨", "가슴"]):
        s = {"기침과": "기침", "열,": "열", "숨": "숨 가쁨", "가슴": "가슴 답답함"}[wd]
        chip(w("c8_3", wd.rstrip(",")), te, s, 1260, 200 + n * 100, bg="rgba(70,74,82,.95)", size=40)
    # 병세 그림(재구성)
    t = T("c8_4"); te = E("c8_4"); pth = nid("ill")
    clip(BG_DARK + f'<svg style="position:absolute;inset:0" width="{W}" height="{H}"><line x1="200" y1="820" x2="1720" y2="820" stroke="#8c7a5a" stroke-width="3"/><line x1="200" y1="240" x2="200" y2="820" stroke="#8c7a5a" stroke-width="3"/>'
         f'<text x="220" y="230" font-family="Malgun" font-weight="700" font-size="34" fill="#cdb98d">병세 ↑ 나쁨</text>'
         f'<path id="{pth}" d="M210 420 C 400 460, 560 700, 760 740 L 1180 745 C 1300 740, 1380 520, 1460 330 L 1560 280" fill="none" stroke="#e8503a" stroke-width="8" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/></svg>'
         f'<div style="position:absolute;left:1240px;top:270px;font:700 28px Malgun;color:rgba(241,230,207,.6)">재구성 · 설명용 그림 (수치 아님)</div>', t, te - t, z=2)
    whip(t)
    JS.append(f'tl.to("#{pth}",{{attr:{{"stroke-dashoffset":0.42}},duration:1.0,ease:"power1.inOut"}},{w("c8_4", "거의"):.3f});'
              f'tl.to("#{pth}",{{attr:{{"stroke-dashoffset":0}},duration:.7,ease:"power3.in"}},{w("c8_4", "갑자기"):.3f});')
    chip(w("c8_4", "나았다가"), te, "거의 나음", 760, 640, bg="rgba(70,74,82,.95)", size=36)
    chip(w("c8_4", "한"), te, "한 달 반쯤 뒤", 1000, 770, bg="rgba(40,34,26,.92)", size=32)
    big(w("c8_4", "갑자기"), te, "급격히 나빠짐", "left:1240px;top:180px;font:700 60px Malgun;color:#e8503a")
    t = T("c8_5"); te = E("c8_5")
    shot("A1", t, te - t, crop=(0.36, 0.5, 0.36, 0.36), move=(1.1, 1.0, 0, 0, 0, 0), flick=(60, 80))
    bl_ = nid("bl"); clip(f'<div id="{bl_}" style="position:absolute;inset:0;background:rgba(20,50,90,.55);mix-blend-mode:color;opacity:0"></div>', t, te - t, z=6)
    JS.append(f'tl.to("#{bl_}",{{opacity:1,duration:1.2}},{w("c8_5", "검푸르게"):.3f});')
    label(w("c8_5", "한의사는"), te, "한 한의사의 해석", "폐렴 말기 → 몸이 검푸르게", x=110, y=150, color="#8a8f98")
    tracker(T("c8_6"), E("c8_6"), None, filled=5, flip=(1, "병의 마지막 모습?", w("c8_6", "병의")))
    # 앞뒤
    t = T("c8_7"); te = E("c8_9") - CARD; lnid = nid("tl")
    clip(BG_DARK + f'<svg style="position:absolute;inset:0" width="{W}" height="{H}"><line id="{lnid}" x1="140" y1="560" x2="1780" y2="560" stroke="#e9dcc4" stroke-width="4" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/></svg>'
         '<div style="position:absolute;left:910px;top:510px;width:100px;height:100px;border-radius:50%;background:#c11c22;box-shadow:0 0 40px #c11c22"></div>'
         '<div style="position:absolute;left:810px;top:640px;width:300px;text-align:center;font:700 40px Malgun;color:#f1e6cf">죽음 4.26<br><span style="color:#e8503a">원인 ?</span></div>', t, te - t, z=2)
    whip(t); JS.append(f'tl.to("#{lnid}",{{attr:{{"stroke-dashoffset":0}},duration:.8}},{t:.3f});')
    for x, y, s, wd in [(220, 380, "단서 2 · 귀국", "단서"), (540, 380, "단서 3 · 의관", "2부터"), (1180, 380, "단서 4 · 묻지 않음", "5까지는"), (1480, 380, "단서 5 · 가족", "5까지는")]:
        chip(w("c8_7", wd), te, s, x, y, bg="rgba(40,34,26,.92)", size=32)
    big(w("c8_7", "'앞뒤'의") if any(x[0].startswith("'앞뒤'") for x in BK["c8_7"]["words"]) else w("c8_7", "앞뒤"), te, "← 앞 · 뒤 →", "left:0;right:0;top:150px;text-align:center;font:700 70px Malgun;color:#f1e6cf", sound="whoosh")
    for n, (s, wd) in enumerate([("미워함", "미워했다는"), ("묻지 않음", "묻지"), ("가족을 내침", "내쳤다는")]):
        chip(w("c8_8", wd), te, s, 300 + n * 480, 280, bg="rgba(163,23,27,.9)", size=38)
    camzoom(T("c8_8"), te, 1.0, 1.07)
    big(w("c8_9", "증거는"), te, "≠ 독살의 증거", "left:0;right:0;top:770px;text-align:center;font:700 60px Malgun;color:#f1e6cf", sound="thud")

    # ================= 9 판정
    chapter_card("c9_0", "V")
    t = T("c9_0"); te = E("c9_8")
    clip(BG_DARK, t, te - t, z=2)
    big(t + .05, E("c9_0"), "판 정", "left:0;right:0;top:400px;text-align:center;font:700 160px Batang;color:#e9dcc4;letter-spacing:.2em", sound="thud")
    cols = [("기록이 말하는 것", "#d9c79f", 100), ("말하지 않는 것", "#f1e6cf", 720), ("해석과 의심", "#f1e6cf", 1340)]
    heads = [w("c9_1", "기록이"), w("c9_5", "기록이"), w("c9_7", "해석과")]
    for (s, c, x), th in zip(cols, heads):
        i = nid("hd")
        clip(f'<div id="{i}" style="position:absolute;left:{x}px;top:140px;width:520px;height:780px;border-top:8px solid {c};background:rgba(255,255,255,.04)">'
             f'<div style="padding:24px 26px;font:700 46px Malgun;color:{c}">{s}</div></div>', th, te - th, z=5)
        JS.append(f'tl.fromTo("#{i}",{{opacity:0,y:40}},{{opacity:1,y:0,duration:.35,ease:"expo.out"}},{th:.3f});'); SFX.append(("thud", th + .1))
    for n, (s, k) in enumerate([("돌아온 지 두 달, 앓은 지 나흘 만에 죽음", "c9_2"), ("묻지 않음 · 벌하지 않음 · 서둘러 입관", "c9_3"), ("몇 해 사이 아내·그 집안·두 아들이 사라짐", "c9_4")]):
        i = nid("rw"); tt = T(k) + .2
        clip(f'<div id="{i}" style="position:absolute;left:126px;top:{270 + n * 200}px;width:470px;font:700 36px/1.4 Malgun;color:#f1e6cf;word-break:keep-all;border-left:5px solid #a3171b;padding-left:18px">{s}</div>', tt, te - tt, z=6)
        JS.append(f'tl.fromTo("#{i}",{{opacity:0,x:-30}},{{opacity:1,x:0,duration:.35,ease:"expo.out"}},{tt:.3f});'); SFX.append(("tick", tt))
    big(w("c9_6", "세자를"), te, "무엇이<br>죽게 했나", "left:740px;top:300px;width:480px;text-align:center;font:700 64px/1.3 Malgun;color:#f1e6cf", sound=None)
    big(w("c9_6", "무엇이었는지"), te, "?", "left:740px;top:520px;width:480px;text-align:center;font:400 240px Batang;color:#f1e6cf")
    camzoom(T("c9_1"), te, 1.0, 1.06)
    chip(w("c9_8", "독살이라는"), te, "독살 — 의심", 1380, 300, bg="rgba(163,23,27,.9)", size=40)
    chip(w("c9_8", "병이었다는"), te, "병사 — 해석", 1380, 420, bg="rgba(70,74,82,.95)", size=40)
    t = T("c9_9"); te = E("c9_9")
    clip('<div style="position:absolute;inset:0;background:#050505"></div>', t, te - t, z=2)
    text(t + .1, te - t - .1, "판정", "left:0;right:0;top:300px;text-align:center;font:700 70px Malgun;color:#a99a80")
    ink(w("c9_9", "미해결"), 960, 590, 300, te - w("c9_9", "미해결"), z=8, color="#6e0b0e")
    stamp(w("c9_9", "미해결"), te - w("c9_9", "미해결"), "미해결", 700, 470, size=170, rot=-7, color="#d8c9a8"); flash(w("c9_9", "미해결") + .15, peak=.3)
    SFX.append(("hit", w("c9_9", "미해결")))
    # 에필로그
    photo("R_jangneung", T("c9_10"), E("c9_10"), "장릉", "인조의 무덤 · 경기 파주 · 1649년", mode="full")
    mapscene(T("c9_11"), E("c9_11"), vb(122, 38, 30), vb(20, 50, 60), zmove=(w("c9_11", "영국에서는"), vb(0, 52, 18)),
             pins=[("한양", T("c9_11"), False), ("런던", w("c9_11", "영국에서는"), True)],
             notes=[(-0.5, 49.6, "1649.1 찰스 1세 처형", w("c9_11", "처형했습니다"), 1.0)], fsw=vb(0, 52, 18)[2])
    t = T("c9_12"); te = E("c9_12"); cal = nid("cal")
    cells = "".join(f'<i style="position:absolute;left:{70 + (n % 10) * 64}px;top:{230 + (n // 10) * 64}px;width:54px;height:54px;border:2px solid #7a5c38"></i>' for n in range(50))
    clip(BG_DARK + f'<div id="{cal}" style="position:absolute;left:560px;top:120px;width:800px;height:820px;background:radial-gradient(ellipse at 30% 20%,#e9dcbc,#c9b487);box-shadow:0 30px 80px rgba(0,0,0,.7)">'
         f'<div style="position:absolute;left:70px;top:60px;font:700 90px Batang;color:#24180f">時憲曆</div>{cells}</div>', t, te - t, z=2)
    whip(t); JS.append(f'tl.fromTo("#{cal}",{{y:300,rotation:5}},{{y:0,rotation:-1,duration:.5,ease:"expo.out"}},{t:.3f});')
    big(w("c9_12", "1653년"), te, "1653", "left:120px;top:160px;font:400 150px Batang;color:#e9dcc4")
    stamp(w("c9_12", "조선의"), te - w("c9_12", "조선의"), "조선 시행", 980, 600, size=86, rot=-8)
    photo("R_hyojong", w("c9_12", "효종의"), te, "영릉", "효종(봉림대군)의 무덤", mode="inset", z=30)
    camzoom(t, te, 1.0, 1.1)
    chip(w("c9_12", "서양"), te, "베이징에서 본 달력", 120, 680, bg="rgba(163,23,27,.9)", size=34)
    chip(w("c9_12", "효종의"), te, "동생 효종 = 봉림대군", 120, 780, bg="rgba(40,34,26,.92)", size=34)
    shot("A3", T("c9_13"), E("c9_13") - T("c9_13"), crop=(0.3, 0.32, 0.38, 0.38), move=(1.15, 1.0, 0, 0, 0, 0), dust=20, grade="saturate(.6)")
    leak(w("c9_13", "세자"), 1.6)
    leak(T("c9_14") - 0.4, 1.4); SFX.append(("whoosh", T("c9_14")))
    shot("A3", T("c9_14"), E("c9_14") - T("c9_14"), move=(1.04, 1.12, -1, 1, 0, -1), fg=("linear-gradient(90deg,#000 0%,#000 40%,transparent 52%)", 2.4), dust=30)
    tag(T("c9_14"), E("c9_14"), "1644년 가을 · 베이징 천문대")
    t13 = T("c9_15"); sp = nid("sp")
    clip(f'<div id="{sp}a" style="{half};left:0;width:50%"><img src="assets/A3.jpg" style="position:absolute;left:-30%;top:0;height:100%;filter:grayscale(.7) brightness(.7)"></div>'
         f'<div id="{sp}b" style="{half};left:50%;width:50%"><img src="assets/A1.jpg" style="position:absolute;left:-60%;top:0;height:100%;filter:brightness(.6)"></div>'
         f'<div style="position:absolute;left:50%;top:0;bottom:0;width:4px;background:#c11c22"></div>', t13, E("c9_15") - t13, z=3)
    JS.append(f'tl.fromTo("#{sp}a",{{xPercent:-100}},{{xPercent:0,duration:.5,ease:"expo.out"}},{t13:.3f});tl.fromTo("#{sp}b",{{xPercent:100}},{{xPercent:0,duration:.5,ease:"expo.out"}},{t13:.3f});')
    SFX.append(("whoosh", t13))
    big(w("c9_15", "병이었을까요"), E("c9_15"), "병?", "left:330px;top:380px;font:700 170px Malgun;color:#f1e6cf", sound="tick")
    big(w("c9_15", "독이었을까요"), E("c9_15"), "독?", "left:1290px;top:380px;font:700 170px Malgun;color:#e8503a")
    t14 = T("c9_16"); te = E("c9_16")
    clip('<div style="position:absolute;inset:0;background:#050505"></div>', t14, te - t14, z=2)
    text(t14 + 0.2, te - t14 - 0.2, "여러분의 판정은?", "left:0;right:0;top:330px;text-align:center;font:700 64px Malgun;color:#e9e2d4")
    ink(t14 + 1.2, 960, 640, 260, te - t14 - 1.2, z=8, color="#6e0b0e")
    stamp(t14 + 1.5, te - t14 - 1.5, "판정 : 미해결", 690, 560, size=96, rot=-6, color="#d8c9a8")

    # 장 이름 (우상단) — 지금 어느 단서인지
    CH_SPANS.sort()
    for n, (t, name) in enumerate(CH_SPANS):
        t1 = CH_SPANS[n + 1][0] - CARD if n + 1 < len(CH_SPANS) else E("c9_16")
        text(t, t1 - t, name, "right:56px;top:64px;font:700 28px Malgun;color:rgba(241,230,207,.8);letter-spacing:.04em", z=46)
    photo("R_westphalia", w("c3_15", "유럽은"), w("c3_15", "영국에서는"), "베스트팔렌 조약 (1648)", None, mode="inset", z=30)
    photo("R_charles", w("c9_11", "의회가"), E("c9_11"), "찰스 1세 처형 (1649)", None, mode="inset", z=30)
    # 어려운 말 풀이
    gloss("o1", "염습이", "염습 = 죽은 이의 몸을 씻기고 옷을 입히는 일")
    gloss("o3", "종친", "종친 = 왕실의 친척")
    gloss("c7_4", "국문", "국문 = 나라가 죄인을 직접 캐묻는 신문")
    for x in S: eng.subtitle(x)
    HTML.append(f'<audio id="bgm" class="clip" src="assets/bgm.wav" data-start="0" data-duration="{S[-1]["t1"] + 0.2:.2f}" data-track-index="92" data-volume="1"></audio>')


half = 'position:absolute;top:0;bottom:0;overflow:hidden'


async def main():
    await tts_all()
    total = timing() + 0.2
    assets(); real_assets(); music(total)
    build()
    cutaways()
    eng.sfx(SFX, total)
    (HF / "index.html").write_text(eng.page(total), encoding="utf-8")
    json.dump([{k: v for k, v in x.items() if k in ("k", "t", "t0", "t1")} for x in S], open(WORK / "beats.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print("total", round(total, 1), "s, clips", len(HTML), "js", len(JS), "sfx", len(SFX))


asyncio.run(main())
