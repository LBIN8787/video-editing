"""시각 카탈로그 예시 그림 만들기 — 장면 종류(연출)·전환·효과를 실제로 렌더해 3컷 띠 그림으로 (2026-11-20 사용자:
"각 스타일 즉 화풍들 내가 나중에 골라서 이거로 해줘 할 수 있도록 분류하고 예시사진들도 넣어줘 … 모든 연출 화풍 … 결국 시각효과니까").

  python scripts/visual_catalog.py <작업 폴더> [--only statecard,docspot] [--force]

장면 종류마다 예시 대본(저장소의 실제 프로젝트에서 첫 번째 것, 없으면 아래 DEMO)을 작은 프로젝트로 만들어 hybrid 로 렌더하고,
장면 영상에서 세 시점(처음·가운데·끝 무렵)을 뽑아 이어 붙인 그림을 예시 폴더(looks.examples_dir()/scenes/<id>.jpg)에 둔다.
실사·사진이 필요한 장면은 원본이 없으면 색 그라데이션 '실사 자리' 클립으로 대신한다(그림에 그렇게 적힘 — styles/visuals.yaml 의 note).
렌더할 때마다 제작 명세(styles/visuals/<id>.json — 그 대본·렌더러·실제 움직임 순서)도 함께 씀(scripts/visual_spec.py).
그다음 python scripts/visual_spec.py --md (장면별 만드는 법) · python scripts/visual_page.py <out.html> (연출 예시 목록 페이지).
※ scripts/looks_catalog.py 는 '실제 프로젝트에서 쓴 장면'을 구성요소 목록용으로 렌더하고, 이 파일은 장면 종류·전환·겹치기를 예시 대본으로 렌더해 제작 명세를 남김.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
from visual_spec import write_spec  # noqa: E402

SAY = "예시 화면입니다."

DEMO = {
    "afterline": {"type": "afterline", "title": "제재 뒤에도 계속 나온 것",
                  "event": {"name": "어느 회사", "date": "2025년 3월 제재", "tag": "제재 뒤", "mark": "ban"},
                  "items": {"count": 6, "icon": "cpu"}, "headline": {"pre": "새 버전", "emph": "6개 이상"},
                  "beats": [{"say": "한 회사가 제재 명단에 올랐습니다.", "show": ["event"]},
                            {"say": "그런데 제재 뒤에도 새 버전은 계속 나왔습니다.", "show": ["after", "items"]},
                            {"say": "여섯 개가 넘습니다.", "show": ["headline"]}]},
    "spread": {"type": "spread", "title": "정제마진은 어디서 생기나",
               "steps": [{"icon": "droplet", "label": "원유"}, {"icon": "factory", "label": "정유 공장"}, {"icon": "fuel", "label": "휘발유·경유"}],
               "low": {"label": "원유값", "value": 70, "text": "$70"}, "high": {"label": "제품값", "value": 95, "text": "$95"},
               "diff": {"label": "정제마진", "formula": "제품값 − 원유값"},
               "change": {"value": 82, "text": "$82", "label": "제품값만 내려가면 간격이 줄어듦"},
               "beats": [{"say": "원유가 공장을 거쳐 기름이 됩니다.", "show": ["steps"]}, {"say": "두 값의 높이를 봅니다.", "show": ["low", "high"]},
                         {"say": "그 차이가 정제마진입니다.", "show": ["diff"]}, {"say": "제품값이 내려가면 간격이 줄어듭니다.", "show": ["change"]}]},
    "share": {"type": "share", "title": "매출 중 두 지역의 몫", "total": "매출 전체", "of": 100,
              "parts": [{"label": "중국·홍콩", "value": 22}, {"label": "싱가포르", "value": 14}],
              "mark": {"value": 33.3, "label": "3분의 1"}, "sum": {"parts": [0, 1], "label": "합치면 3분의 1 넘게"},
              "beats": [{"say": "매출 전체를 막대 하나로 놓습니다.", "show": ["total", "p0"]}, {"say": "싱가포르를 더합니다.", "show": ["p1"]},
                        {"say": "합치면 3분의 1이 넘습니다.", "show": ["mark", "sum"]}]},
    "motionboard": {"type": "motionboard", "title": "보호예수가 풀리면", "theme": "paper",
                    "els": {"inv": {"kind": "person", "x": 420, "y": 600, "name": "초기 투자자", "role": "상장 전에 산 사람", "tone": "gray"},
                            "buy": {"kind": "person", "x": 1500, "y": 600, "name": "새 투자자", "role": "시장에서 사는 사람"},
                            "stock": {"kind": "card", "x": 700, "y": 640, "icon": "files", "label": "주식"},
                            "free": {"kind": "text", "x": 960, "y": 260, "text": "보호예수 해제", "size": 64, "color": "red"},
                            "note": {"kind": "text", "x": 700, "y": 480, "text": "묶여 있음", "pen": True, "color": "red"},
                            "sell": {"kind": "arrow", "from": "inv", "to": "buy", "label": "매도", "color": "red", "bend": 0.2}},
                    "beats": [{"say": "상장 전에 산 주식은 한동안 묶여 있습니다.", "do": ["inv", "stock", "note"]},
                              {"say": "보호예수가 풀리면 팔 수 있게 됩니다.", "do": ["free", {"hide": "note"}, {"move": "stock", "to": [1180, 640]}]},
                              {"say": "그 물량이 시장으로 나옵니다.", "do": ["buy", "sell", {"hi": "stock"}]}]},
    "statecard": {"type": "statecard", "title": "AI 비서가 대신 하는 일", "hub": {"label": "AI 비서", "icon": "bot"},
                  "cards": [{"id": "hotel", "label": "호텔 예약", "icon": "phone", "sub": "대기 중"},
                            {"id": "shop", "label": "쇼핑몰 결제", "icon": "shopping-cart", "sub": "대기 중"},
                            {"id": "kakao", "label": "메신저", "icon": "smartphone", "sub": "연결됨"}],
                  "beats": [{"say": "AI 비서는 세 곳에 연결돼 있습니다.", "show": "all"},
                            {"say": "호텔에 전화를 걸고 결제도 진행합니다.", "state": {"hotel": "run", "shop": "run"}, "text": {"hotel": "통화 중", "shop": "결제 진행"}},
                            {"say": "호텔은 끝났지만 메신저는 막혔습니다.", "state": {"hotel": "ok"}, "text": {"hotel": "예약 확정", "kakao": "연결 끊김"}, "cut": ["kakao"]}]},
    "docspot": {"type": "docspot", "source": "예시 신문 · 11.09", "headline": "AI 비서, 하루 수백 통 대신 전화 걸어",
                "paras": ["한 AI 비서 서비스가 출시 첫 주에 이용자 대신 건 전화가 크게 늘었다고 회사가 밝혔다.",
                          "회사 쪽은 첫날 433통이던 발신이 닷새 만에 817통으로 늘었다고 설명했다.",
                          "다만 전화를 받은 가게 상당수는 AI 라는 사실을 듣지 못했다고 답했다."],
                "beats": [{"say": "기사 원문을 보겠습니다.", "spot": 0},
                          {"say": "하루 발신이 433통에서 817통으로 늘었습니다.", "spot": 1, "num": {"value": "817통", "label": "닷새 뒤 하루 발신", "sub": "첫날 433통"}},
                          {"say": "그런데 받은 쪽은 AI 인 줄 몰랐습니다.", "spot": 2}]},
}
DEMO.update({   # 누아르 사건 보드 (docs/57) — 가상의 예시 (실제 회사·인물 아님)
    "hubweb": {"type": "hubweb", "skin": "noir", "title": "누가 움직였나",
               "hub": {"label": "누가?", "sub": "이사회 뒤의 손"}, "ruler": ["월", "화", "수", "목"],
               "nodes": [{"id": "a", "label": "대주주 펀드", "sub": "지분 12%", "date": "월", "rel": "지분 매각"},
                         {"id": "b", "label": "사외이사 2명", "sub": "동시 사임", "date": "화"},
                         {"id": "c", "label": "경쟁사 대표", "sub": "같은 날 매수", "from": "a", "date": "수"},
                         {"id": "d", "label": "익명 제보", "sub": "기사 한 줄", "date": "목"}],
               "beats": [{"say": "월요일, 대주주 펀드가 지분을 팔았습니다.", "add": ["a"]},
                         {"say": "화요일, 사외이사 두 명이 함께 물러났습니다.", "add": ["b"]},
                         {"say": "같은 주, 그 지분을 산 사람은 경쟁사 대표였습니다.", "add": ["c"], "hi": "a"},
                         {"say": "그리고 목요일, 익명 제보가 나옵니다.", "add": ["d"], "cut": ["b"]}]},
    "ledger": {"type": "ledger", "skin": "noir", "title": "엇갈린 두 편",
               "left": {"head": "끌어내리려는 자", "sub": "해임 요구"}, "right": {"head": "다시 올리려는 자", "sub": "복귀 요구"},
               "rows": [{"id": "l1", "side": "l", "name": "이사회", "note": "해임 의결", "date": "월"},
                        {"id": "r1", "side": "r", "name": "직원 다수", "note": "복귀 연판장", "date": "화"},
                        {"id": "l2", "side": "l", "name": "새 경영진", "note": "임시 대표 선임", "date": "화"},
                        {"id": "r2", "side": "r", "name": "최대 투자사", "note": "복귀 지지", "date": "수"}],
               "beats": [{"say": "이사회가 대표를 해임합니다.", "add": ["l1"]},
                         {"say": "직원들은 복귀를 요구하는 연판장을 돌립니다.", "add": ["r1", "l2"]},
                         {"say": "최대 투자사까지 복귀 편에 섭니다.", "add": ["r2"]},
                         {"say": "결국 해임은 닷새 만에 뒤집힙니다.", "strike": ["l1"], "verdict": "닷새 만에 뒤집힘"}]},
})
# 같은 장면 종류의 다른 모습 (변형) — id 는 갤러리에 그대로 쓰임
VARIANTS = {
    "chapter@two-line": {"type": "chapter", "num": "1", "look": "two-line", "kicker": "묻지도 않고", "title": "전화를 겁니다",
                         "clip": {"src": "ph", "start": 0}, "beats": [{"say": "첫 번째 문제입니다."}]},
    "footage@chips": {"type": "footage", "clip": {"src": "ph", "start": 0, "frame": "full"}, "label": "실사 자리",
                      "beats": [{"say": "출근길 사람들은 저마다 AI 에게 부탁을 겁니다.", "chips": ["프로틴 싸게 사 줘", "메일 좀 정리해 줘", "미용실 예약해 줘"]}]},
    "chapter@noir": {"type": "chapter", "skin": "noir", "look": "noir", "kicker": "월요일 → 금요일", "title": "닷새 동안 무슨 일이 있었나", "sub": "가상의 예시",
                     "beats": [{"say": "닷새 동안 무슨 일이 있었는지 따라가 봅니다."}]},
    "map_causal@cut": {"type": "map_causal", "title": "부탁에서 결제까지",
                       "map": {"nodes": {"ask": {"label": "사용자 부탁", "icon": "user", "x": 400, "y": 420},
                                         "bot": {"label": "AI 비서", "icon": "bot", "x": 960, "y": 420},
                                         "shop": {"label": "쇼핑몰 결제", "icon": "shopping-cart", "x": 1520, "y": 420},
                                         "msg": {"label": "메신저", "icon": "smartphone", "x": 960, "y": 760}}},
                       "beats": [{"say": "부탁은 AI 비서를 거쳐 결제와 메시지로 이어집니다.", "reveal": ["ask", "bot", "shop", "msg"],
                                  "draw": [["ask", "bot"], ["bot", "shop"], ["bot", "msg"]]},
                                 {"say": "그런데 메시지 쪽 길은 막혔습니다.", "cut": [["bot", "msg"]], "active": "shop"}]},
}
# 전환: 장면 둘(같은 bignum)을 이어 경계 앞뒤를 찍음
TRANSITIONS = ["fade", "push", "wipe", "zoom", "iris", "iris_out"]
SKIP = {"intro"}   # intro 는 채널 소개 장면(v24 인트로 없음 — 쓰지 않음)


def sources() -> dict:
    """장면 종류 → (예시 장면, 그 대본의 공통 키, 출처 파일). 저장소의 실제 프로젝트에서 처음 만난 것."""
    found = {}
    for f in sorted((ROOT / "projects").glob("*/02_script/hybrid.json")):
        try:
            s = json.loads(f.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue
        for sc in s.get("scenes", []):
            t = sc.get("type")
            if t and t not in found and sc.get("beats"):
                found[t] = (sc, {k: v for k, v in s.items() if k not in ("scenes", "title")}, str(f.relative_to(ROOT)))
    return found


def placeholder(path: Path, seconds: float = 20):
    """원본 실사가 없을 때 '실사 자리': 천천히 흐르는 어두운 색 그라데이션."""
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i",
                    f"gradients=s=1920x1080:c0=0x2c3e50:c1=0x8e6e53:c2=0x4b6b7a:n=3:speed=0.02:d={seconds}:r=30",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", str(path)], check=True)


def mini(work: Path, key: str, sc: dict, common: dict) -> Path:
    p = work / key.replace("@", "_")
    if p.exists():
        shutil.rmtree(p)
    for d in ("01_research", "02_script", "03_voice", "04_assets/footage", "05_edit"):
        (p / d).mkdir(parents=True, exist_ok=True)
    (p / "state.json").write_text(json.dumps({"name": key, "done": [], "approved": []}), encoding="utf-8")
    sc = json.loads(json.dumps(sc))
    sc["id"], sc["chapter"] = 1, sc.get("chapter", 0) or 0
    sc.pop("tr", None)
    for b in sc.get("beats", []):
        b["say"] = b.get("say") or SAY
    sc["beats"] = sc["beats"][:4]
    spec = {"title": key, "edit_v10": True, **{k: v for k, v in common.items() if k in ("map", "footage", "brand", "camera", "zoom")}}
    if sc.get("type") == "chapter" and not sc.get("title"):
        sc["title"] = "장 제목"
    spec.setdefault("footage", {})
    spec["footage"] = {k: {**v, "file": "ph.mp4"} for k, v in spec["footage"].items()}
    spec["footage"]["ph"] = {"file": "ph.mp4", "credit": "실사 자리"}
    placeholder(p / "04_assets" / "footage" / "ph.mp4")
    spec["scenes"] = [sc]
    (p / "02_script" / "hybrid.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
    return p


def strip(video: Path, out: Path, n: int = 3, at: list | None = None):
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(video)],
                               capture_output=True, text=True).stdout)
    ts = at or [dur * f for f in (0.3, 0.6, 0.92)][:n]
    tmp = out.with_suffix("")
    ins, parts = [], []
    for k, t in enumerate(ts):
        f = tmp.parent / f"{tmp.name}_{k}.jpg"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{min(t, dur - 0.05):.2f}", "-i", str(video), "-frames:v", "1",
                        "-vf", "scale=640:-2", str(f)], check=True)
        ins += ["-i", str(f)]
        parts.append(f)
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex",
                    "".join(f"[{k}]pad=iw+8:ih:0:0:white[p{k}];" for k in range(len(parts) - 1)) +
                    "".join(f"[p{k}]" for k in range(len(parts) - 1)) + f"[{len(parts) - 1}]hstack={len(parts)}", "-q:v", "4", str(out)], check=True)
    for f in parts:
        f.unlink(missing_ok=True)


def render(p: Path) -> Path:
    from ytflow.project import Project
    from ytflow.stages import hybrid
    try:
        hybrid.make(Project.open(str(p)), workers=2)
    except subprocess.CalledProcessError as e:   # 자막·소리 마스터링 단계 실패는 무시 — 예시 그림은 장면 영상만 씀
        if not (p / "04_assets" / "hb_001.mp4").exists():
            raise
        print(f"[catalog] 마스터링 건너뜀: {str(e)[:120]}")
    return p / "04_assets" / "hb_001.mp4"


def jobs() -> dict:
    """연출 id → (예시 장면, 대본 공통 키, 출처). DEMO·VARIANTS 가 먼저, 나머지는 저장소 프로젝트의 첫 예."""
    from ytflow.stages import hybrid
    found = sources()
    out = {}
    for t in sorted(hybrid.RENDER):
        if t in SKIP:
            continue
        if t in DEMO:
            out[t] = (DEMO[t], {}, "scripts/visual_catalog.py DEMO")
        elif t in found:
            out[t] = found[t]
    for k, sc in VARIANTS.items():
        out[k] = (sc, {}, "scripts/visual_catalog.py VARIANTS")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("work")
    ap.add_argument("--only", default="")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--reverse", action="store_true", help="거꾸로 — 두 번째 일꾼을 함께 돌릴 때 (있는 그림은 건너뜀)")
    a = ap.parse_args()
    from ytflow.stages import hybrid, looks
    work = Path(a.work)
    work.mkdir(parents=True, exist_ok=True)
    exd = looks.examples_dir() / "scenes"
    exd.mkdir(parents=True, exist_ok=True)
    only = {k.strip() for k in a.only.split(",") if k.strip()}
    log: dict = {}
    jobs_ = jobs()
    items = list(jobs_.items())
    for key, (sc, common, src) in (items[::-1] if a.reverse else items):
        if only and key not in only:
            continue
        out = exd / f"{key.replace('@', '_')}.jpg"
        if out.exists() and not a.force:
            log[key] = "있음"
            continue
        try:
            v = render(mini(work, key, sc, common))
            strip(v, out)
            write_spec(key, work, src)   # 제작 명세: 이 그림을 만든 대본·렌더러·실제 움직임 순서 (styles/visuals/<id>.json)
            log[key] = f"ok ← {src}"
        except Exception as e:  # noqa: BLE001
            log[key] = f"실패: {str(e)[:160]}"
            traceback.print_exc()
        print(f"[catalog] {key}: {log[key]}", flush=True)
    # 전환
    if (not only or "transitions" in only) and not a.reverse:
        for tr in TRANSITIONS:
            out = exd / f"tr_{tr}.jpg"
            if out.exists() and not a.force:
                continue
            try:
                p = mini(work, f"tr_{tr}", {"type": "bignum", "small": "앞 장면", "value": "1", "beats": [{"say": "앞 장면입니다."}]}, {})
                spec = json.loads((p / "02_script" / "hybrid.json").read_text(encoding="utf-8"))
                b = {"id": 2, "type": "bignum", "chapter": 0, "small": "다음 장면", "value": "2", "beats": [{"say": "다음 장면입니다."}]}
                if tr == "iris_out":
                    spec["scenes"][0]["iris_out"] = {"x": 960, "y": 480, "r": 220}
                else:
                    b["tr"] = tr
                spec["scenes"].append(b)
                (p / "02_script" / "hybrid.json").write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
                render(p)
                d1 = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                           str(p / "04_assets" / "hb_001.mp4")], capture_output=True, text=True).stdout)
                strip(p / "05_edit" / "hb_work" / "video.mp4", out, at=[d1 - 0.5, d1 - 0.15, d1 + 0.2, d1 + 0.45], n=4)
                write_spec(f"tr_{tr}", work, "scripts/visual_catalog.py TRANSITIONS")
                log[f"tr_{tr}"] = "ok"
            except Exception as e:  # noqa: BLE001
                log[f"tr_{tr}"] = f"실패: {str(e)[:160]}"
                traceback.print_exc()
            print(f"[catalog] tr_{tr}: {log[f'tr_{tr}']}", flush=True)
    (work / "catalog_log.json").write_text(json.dumps(log, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(log, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
