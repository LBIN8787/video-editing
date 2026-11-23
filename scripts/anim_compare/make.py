"""대본 → 그림·애니메이션 시험: AI 그림 조각(cut) vs 직접 그린 관절 인형(puppet) 비교 (2026-11-14 사용자).
> "보기 잡기 걷기 단어가 아니라 이미지와 애니메이션으로 … 졸라맨을 하지 말라 한 거지 대본에 따른 이미지와 애니메이션을 제작하지 말라 한 게 아니에요"

    python scripts/anim_compare/make.py build      → projects/20261114-anim-ai, 20261114-anim-vec (모라벡 편 #6·#9, 같은 목소리)
    YTFLOW_TTS=edge python -m ytflow hybrid 20261114-anim-ai ; ... 20261114-anim-vec
    python scripts/anim_compare/make.py compare    → projects/20261114-anim-ai/05_edit/compare.mp4
AI 그림: ElevenLabs bytedance-seedream-5.5 (장당 약 98크레딧) — 인물 한 명을 '자세 3개 한 장'으로 만들어 모습이 같게, 흰 배경을 지워 조각으로
(04_assets/story/gen/, 프롬프트는 docs/27-story-animation.md).
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "projects" / "20261113-curiosity-moravec"
CREAM = "#F4EBDD"
FULL = "full"

AI = {
 6: [
  [{"t": "생각해", "do": "bg", "mode": "photo", "src": "laundry.jpg", "credit": "세탁소: L. Hine 1917 PD·의회도서관"},
   {"t": "빨래", "do": "cut", "id": "sh", "src": "gen/shirt_crumpled.png", "x": 1000, "y": 1300, "h": 330, "cam": [1300, 1000, 0.85]},
   {"t": "집어", "do": "move", "on": "sh", "dy": -220, "dur": 0.6, "hop": False, "ease": "back.out(1.6)"},
   {"t": "1초", "do": "count", "id": "s1", "value": "1초", "x": 1700, "y": 860, "fs": 220, "card": True, "label": "우리가 고민하는 시간"}],
  [{"t": "하지만", "do": "bg", "mode": "paper"},
   {"t": "로봇의", "do": "cut", "id": "rb", "src": "gen/robot_stare.png", "x": 900, "y": 1900, "h": 700, "cam": [1250, 1450, 0.85]}],
  [{"t": "소매는", "do": "pose", "on": "rb", "src": "gen/robot_pinch.png"},
   {"t": "소매는", "do": "chip", "id": "q1", "text": "소매는 어디?", "x": 1750, "y": 1180, "fs": 70, "delay": 0.2},
   {"t": "잡아야", "do": "shake", "on": "rb"},
   {"t": "잡아야", "do": "chip", "id": "q2", "text": "어디를 잡지?", "x": 1750, "y": 1400, "fs": 70},
   {"t": "미끄러지면", "do": "pose", "on": "rb", "src": "gen/robot_confused.png"},
   {"t": "미끄러지면", "do": "chip", "id": "q3", "text": "미끄러지면?", "x": 1750, "y": 1620, "fs": 70}],
  [{"t": "체스는", "do": "cut", "id": "bd", "src": "gen/chessboard.png", "x": 2760, "y": 1300, "h": 560, "cam": [3050, 1000, 0.85]},
   {"t": "서른두", "do": "chip", "id": "c1", "text": "말 32개", "x": 3480, "y": 700, "fs": 72},
   {"t": "규칙은", "do": "chip", "id": "c2", "text": "규칙은 고정", "x": 3480, "y": 940, "fs": 72},
   {"t": "여덟", "do": "chip", "id": "c3", "text": "판은 늘 8×8", "x": 3480, "y": 1180, "fs": 72}],
  [{"t": "천과", "do": "circle", "on": "rb", "pad": 30, "cam": FULL},
   {"t": "똑같은", "do": "circle", "on": "bd", "pad": 20, "color": "#2E7D4F"}],
 ],
 9: [
  [{"t": "모라벡은", "do": "bg", "mode": "dark", "cam": [1400, 950, 0.8]},
   {"t": "진화", "do": "line", "id": "tl", "from": [300, 1150], "to": [3540, 1150], "sw": 12, "dur": 1.4, "color": CREAM},
   {"t": "진화", "do": "note", "id": "old", "text": "아주 먼 옛날", "x": 560, "y": 1290, "fs": 64, "color": CREAM, "delay": 0.4},
   {"t": "찾았습니다", "do": "note", "id": "now", "text": "오늘", "x": 3420, "y": 1290, "fs": 64, "color": CREAM}],
  [{"t": "보고", "do": "cut", "id": "bb", "src": "gen/baby_look.png", "x": 800, "y": 1150, "h": 480},
   {"t": "잡고", "do": "pose", "on": "bb", "src": "gen/baby_grab.png"},
   {"t": "걷는", "do": "pose", "on": "bb", "src": "gen/baby_walk.png"},
   {"t": "걷는", "do": "move", "on": "bb", "dx": 1250, "dur": 3.0, "delay": 0.35},
   {"t": "오랜", "do": "arrow", "id": "ar", "from": [700, 1060], "to": [2400, 1060], "bend": -60, "color": "#F3D36B", "sw": 9}],
  [{"t": "느끼지", "do": "chip", "id": "nf", "text": "어려운 줄도 모른다", "x": 1500, "y": 480, "fs": 84, "hl": True}],
  [{"t": "체스나", "do": "cut", "id": "cs", "src": "gen/chessboard.png", "x": 3250, "y": 1130, "h": 330, "cam": [2700, 1000, 0.75]},
   {"t": "한", "do": "circle", "id": "dot", "at": [3440, 1150], "size": [40, 40], "pad": 40}],
  [{"t": "어렵다고", "do": "chip", "id": "f1", "text": "어렵다고 느끼는 것", "x": 1250, "y": 1620, "fs": 80, "cam": FULL},
   {"t": "실제로", "do": "chip", "id": "f2", "text": "실제로 어려운 것", "x": 2650, "y": 1620, "fs": 80, "tone": "dark"},
   {"t": "다를", "do": "note", "id": "ne", "text": "≠", "x": 1960, "y": 1610, "fs": 160, "color": "#F3D36B"}],
 ],
}


def vec_from_ai() -> dict:
    """같은 연출을 관절 인형으로 (그림만 바꿈)."""
    V = {int(k): v for k, v in json.loads(json.dumps(AI)).items()}
    s6 = V[6]
    s6[0][1] = {"t": "빨래", "do": "puppet", "id": "sh", "char": "shirt_crumpled", "x": 1000, "y": 1300, "s": 1.6, "cam": [1300, 1000, 0.85]}
    s6[1][1] = {"t": "로봇의", "do": "puppet", "id": "rb", "char": "robot", "x": 800, "y": 1880, "s": 1.6, "cam": [1250, 1450, 0.85]}
    s6[1].append({"t": "구겨진", "do": "puppet", "id": "cl", "char": "shirt_crumpled", "x": 1400, "y": 1880, "s": 1.3})
    s6[2][0] = {"t": "소매는", "do": "act", "on": "rb", "a": "reach", "ang": 32, "fore": 34}
    s6[2][2] = {"t": "잡아야", "do": "act", "on": "rb", "a": "fumble", "target": "cl"}
    s6[2][4] = {"t": "미끄러지면", "do": "act", "on": "rb", "a": "confused"}
    s6[3][0] = {"t": "체스는", "do": "draw", "id": "bd", "icon": "board", "x": 2760, "y": 1020, "s": 520, "cam": [3050, 1000, 0.85]}
    s9 = V[9]
    s9[1] = [{"t": "보고", "do": "puppet", "id": "bb", "char": "baby", "x": 800, "y": 1150, "s": 1.5},
             {"t": "보고", "do": "act", "on": "bb", "a": "look", "delay": 0.3},
             {"t": "잡고", "do": "puppet", "id": "blk", "char": "block", "x": 1080, "y": 1150, "s": 1.3, "delay": -0.4},
             {"t": "잡고", "do": "act", "on": "bb", "a": "grab", "target": "blk"},
             {"t": "걷는", "do": "act", "on": "bb", "a": "walk", "dx": 1250, "steps": 6, "dur": 0.5, "delay": 0.2},
             s9[1][4]]
    s9[3][0] = {"t": "체스나", "do": "draw", "id": "cs", "icon": "chess", "x": 3250, "y": 950, "s": 300, "cam": [2700, 1000, 0.75]}
    return V


def build():
    spec = json.loads((SRC / "02_script" / "hybrid.json").read_text(encoding="utf-8"))
    S = {s["id"]: s for s in spec["scenes"]}
    for name, draws in (("20261114-anim-ai", AI), ("20261114-anim-vec", vec_from_ai())):
        P = ROOT / "projects" / name
        (P / "02_script").mkdir(parents=True, exist_ok=True)
        (P / "05_edit").mkdir(exist_ok=True)
        (P / "01_research").mkdir(exist_ok=True)
        if not (P / "03_voice").exists():
            subprocess.run(["cp", "-al", str(SRC / "03_voice"), str(P / "03_voice")], check=True)
        (P / "04_assets").mkdir(exist_ok=True)
        if not (P / "04_assets" / "story").exists():
            subprocess.run(["cp", "-al", str(SRC / "04_assets" / "story"), str(P / "04_assets" / "story")], check=True)
        for f in ("edit.yaml", "state.json"):
            shutil.copy(SRC / f, P / f)
        scenes = []
        for sid in (6, 9):
            sc = json.loads(json.dumps(S[sid]))
            for b, d in zip(sc["beats"], draws[sid]):
                b["draw"] = d
            scenes.append(sc)
        out = {k: v for k, v in spec.items() if k not in ("scenes", "package")}
        out["scenes"] = scenes
        (P / "02_script" / "hybrid.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
        print(P)


def compare():
    a = ROOT / "projects" / "20261114-anim-ai" / "05_edit" / "final.mp4"
    v = ROOT / "projects" / "20261114-anim-vec" / "05_edit" / "final.mp4"
    out = ROOT / "projects" / "20261114-anim-ai" / "05_edit" / "compare.mp4"
    font = ROOT / "ytflow" / "assets" / "fonts" / "NanumGothic-ExtraBold.ttf"
    lab = lambda t: (f"drawtext=fontfile='{font}':text='{t}':x=40:y=30:fontsize=40:fontcolor=white:box=1:boxcolor=black@0.6:boxborderw=14")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(a), "-i", str(v), "-filter_complex",
                    f"[0:v]{lab('A · AI 그림 조각 (약 98크레딧/장)')}[a];[1:v]{lab('B · 직접 그린 관절 인형 (무료)')}[b];"
                    "[a][0:a][b][1:a]concat=n=2:v=1:a=1[v][au]", "-map", "[v]", "-map", "[au]",
                    "-c:v", "libx264", "-crf", "20", "-preset", "veryfast", "-c:a", "aac", str(out)], check=True)
    print(out)


if __name__ == "__main__":
    {"build": build, "compare": compare}[sys.argv[1]]()
