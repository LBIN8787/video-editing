"""비교용: 11/13 이어 읽는 시장을 '여러 스타일 혼합'으로 다시 (대본·목소리 그대로, 장면 3개만 바꿈) + 기존 vs 혼합 비교 영상.
    python scripts/remix_20261113/make.py build   → projects/20261113-market-remix (YTFLOW_TTS=edge python -m ytflow hybrid 20261113-market-remix)
    python scripts/remix_20261113/make.py compare → projects/20261113-market-remix/05_edit/compare.mp4
바꾼 곳: #5 체크리스트(공시 4가지) → 뉴스 데스크 카드 + 사람·자리 아이콘 / #9 대결(versus) → 카드 + 돈이 AMD·브로드컴으로 / #14 체크리스트(네이버) → 카드 + 매출 숫자 세기.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "projects" / "20261113-market-daily"
P = ROOT / "projects" / "20261113-market-remix"
CH = {5: "요약 체크리스트 + 말에 맞춰 생기는 그림", 9: "대결 카드 + 돈이 날아가는 화살표", 14: "요약 체크리스트 + 매출 숫자 세기·아이콘"}


def build():
    P.mkdir(parents=True, exist_ok=True)
    for d in ("01_research", "03_voice", "04_assets"):
        if not (P / d).exists():
            subprocess.run(["cp", "-al", str(SRC / d), str(P / d)], check=True)   # 하드링크 (같은 박자 음성·장면 렌더 재사용)
    for f in ("edit.yaml", "state.json"):
        shutil.copy(SRC / f, P / f)
    (P / "02_script").mkdir(exist_ok=True)
    (P / "05_edit").mkdir(exist_ok=True)
    spec = json.loads((SRC / "02_script" / "hybrid.json").read_text(encoding="utf-8"))
    S = {s["id"]: s for s in spec["scenes"]}
    keep = lambda i: {"id": i, "chapter": S[i]["chapter"], "beats": S[i]["beats"]}
    # v2 (2026-11-13 사용자: "한눈에 — 중요 내용 정리(요약)에 애니메이션·그림을 덧붙여 혼용"):
    # 요약 장면(체크리스트·대결)은 그대로 두고, 줄은 핵심 낱말을 말할 때 나타나게 + 오른쪽에 말에 맞춰 생기는 사물
    s5 = dict(S[5]); s5.pop("layers", None)
    s5.update(x=150, text_w=860)
    s5["rows"] = [dict(r, t=t) for r, t in zip(S[5]["rows"], ("사임", "크레스", "의장", "후보"))]
    s5["beats"] = [dict(S[5]["beats"][0], motion=[
                       {"t": "사임", "do": "icon", "id": "seat", "icon": "🪑", "x": 1430, "y": 330, "d": 170, "label": "CEO 자리"},
                       {"t": "크레스", "do": "icon", "id": "kr", "icon": "👩‍💼", "x": 1760, "y": 330, "d": 150, "label": "크레스 (임시)"},
                       {"t": "겸합니다", "do": "arrow", "a": "kr", "b": "seat"}]),
                   dict(S[5]["beats"][1], motion=[
                       {"t": "의장", "do": "icon", "id": "ch", "icon": "🏛️", "x": 1430, "y": 640, "d": 150, "label": "이사회 의장"},
                       {"t": "후보", "do": "icon", "id": "sr", "icon": "🔎", "x": 1760, "y": 640, "d": 150, "label": "CEO 찾는 중"}])]
    S[5] = s5
    s9 = dict(S[9])   # 대결 카드(AMD vs 엔비디아) 그대로 + 돈이 엔비디아에서 AMD 쪽으로 날아감
    s9["beats"] = [dict(S[9]["beats"][0], motion=[   # 대결 장면은 막대 두 개로 그려짐: AMD 막대 위(516,300), 엔비디아 막대 위(960,470)
                       {"do": "anchor", "id": "nvA", "x": 960, "y": 580, "w": 120, "h": 60},
                       {"do": "anchor", "id": "amdA", "x": 516, "y": 300, "w": 160, "h": 90},
                       {"t": "AMD", "do": "icon", "id": "m1", "icon": "💸", "from": "nvA", "x": 740, "y": 250, "d": 110},
                       {"t": "AMD", "do": "arrow", "a": "nvA", "b": "amdA", "delay": 0.2},
                       {"t": "브로드컴", "do": "icon", "id": "av", "icon": "📈", "x": 1480, "y": 330, "d": 140, "label": "브로드컴 +5.54%"},
                       {"t": "브로드컴", "do": "arrow", "a": "nvA", "b": "av", "delay": 0.2}]),
                   S[9]["beats"][1]]
    S[9] = s9
    s14 = dict(S[14]); s14.update(x=150, text_w=880)
    s14["rows"] = [dict(r, t=t) for r, t in zip(S[14]["rows"], ("3조", "여섯", "불확실성"))]
    s14["beats"] = [dict(S[14]["beats"][0], motion=[
                        {"t": "3조", "do": "count", "id": "rev", "value": "34,724억", "label": "3분기 매출 (원)", "x": 1560, "y": 340, "w": 560, "h": 260, "fs": 96},
                        {"t": "여섯", "do": "icon", "id": "six", "icon": "🏆", "x": 1430, "y": 660, "d": 140, "label": "6분기 연속"}]),
                    dict(S[14]["beats"][1], motion=[
                        {"t": "불확실성", "do": "icon", "id": "q", "icon": "❓", "x": 1720, "y": 660, "d": 140, "bg": "#FF5A4E", "label": "AI 협력?"},
                        {"t": "해석", "do": "pulse", "on": "q"}])]
    S[14] = s14
    spec["scenes"] = [S[i] for i in sorted(S)]
    spec["title"] = spec.get("title", "") + " (혼합 스타일 비교판)"
    (P / "02_script" / "hybrid.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
    print(P)


def _tl(p):
    t = json.loads((p / "05_edit" / "hybrid_timeline.json").read_text(encoding="utf-8"))
    out, s = {}, 0.0
    for x in t:
        out[x["scene"]] = (s, x["dur"])
        s += x["dur"]
    return out


def compare():
    sys.path.insert(0, str(ROOT))
    from ytflow.stages import paper
    font = paper.FONT_DIR / "NanumGothic-ExtraBold.ttf"
    a, b = _tl(SRC), _tl(P)
    work = P / "05_edit" / "cmp"
    work.mkdir(parents=True, exist_ok=True)
    parts = []

    def card(name, lines, sec=2.6):
        out = work / f"{name}.mp4"
        dt = "".join(f"drawtext=fontfile='{font}':text='{l}':fontsize={fs}:fontcolor={c}:x=(w-text_w)/2:y={y}," for l, fs, c, y in lines)
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i", f"color=c=0x0E0F11:s=1920x1080:d={sec}:r=30",
                        "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", str(sec), "-vf", dt.rstrip(","), "-c:v", "libx264", "-pix_fmt", "yuv420p",
                        "-c:a", "aac", "-ar", "48000", "-ac", "2", str(out)], check=True)
        parts.append(out)

    def clip(name, src, t0, d, tag, col):
        out = work / f"{name}.mp4"
        vf = (f"drawbox=x=40:y=40:w=560:h=86:color=0x000000@0.75:t=fill,"
              f"drawtext=fontfile='{font}':text='{tag}':fontsize=44:fontcolor={col}:x=68:y=60")
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{t0:.2f}", "-i", str(src), "-t", f"{d:.2f}", "-vf", vf,
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-ar", "48000", "-ac", "2", str(out)], check=True)
        parts.append(out)

    card("t0", [("같은 대본 · 같은 목소리", 56, "0x8A8F98", 380), ("연출만 바꾸면 무엇이 달라지나", 84, "white", 470), ("이어 읽는 시장 · 11월 13일", 40, "0xF5C518", 610)], 3.0)
    for k, sid in enumerate((5, 9, 14), 1):
        card(f"c{sid}", [(f"비교 {k} / 3", 44, "0xF5C518", 400), (CH[sid], 60, "white", 480)])
        clip(f"a{sid}", SRC / "05_edit" / "final.mp4", *a[sid], "기존", "0xC9CDD3")
        clip(f"b{sid}", P / "05_edit" / "final.mp4", *b[sid], "혼합 스타일", "0x3DDC97")
    lst = work / "list.txt"
    lst.write_text("\n".join(f"file '{x.resolve()}'" for x in parts), encoding="utf-8")
    out = P / "05_edit" / "compare.mp4"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c:v", "libx264", "-preset", "medium",
                    "-crf", "20", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out)], check=True)
    print(out)


if __name__ == "__main__":
    {"build": build, "compare": compare}[sys.argv[1]]()
