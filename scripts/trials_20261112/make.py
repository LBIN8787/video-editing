"""v15 시험판: 카테고리 개성(장 표지 모양 4종 + 듀오톤 사진) + 증거판 + 칠판.

같은 사실·같은 문장(2026-11-11 네 편에서 이미 검증된 대본)을 새 모양으로만 다시 그린다.
    python scripts/trials_20261112/make.py && python -m ytflow hybrid 20261112-bg-trials
사진: 위키미디어 공용 (퍼블릭 도메인·CC BY 만, 출처는 footage.credit → 화면 오른쪽 위에 표시).
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from ytflow.stages import archive  # noqa: E402

P = ROOT / "projects" / "20261112-bg-trials"
SRC = {k: json.loads((ROOT / f"projects/20261111-{k}/02_script/hybrid.json").read_text(encoding="utf-8"))
       for k in ("issues-aiglasses", "curiosity-hallucination", "market-nvidia", "ai-industry-week")}

# 장 표지 사진 (주제에 맞게, NASA 위성 사진에 고정하지 않음) — (키, 검색어, 파일 제목)
PHOTOS = [("exam", "Richard Huish College Exam Hall", "Richard Huish College Exam Hall.jpg"),
          ("nyse", "NYSE trading floor", "NYSE.jpg"),
          ("dc", "server room data center", "Microsoft Data Center Middenmeer, the Netherlands - 1.jpg")]


def photos() -> dict:
    fdir = P / "04_assets" / "footage"
    (fdir / "raw").mkdir(parents=True, exist_ok=True)
    out = {}
    for k, (key, q, title) in enumerate(PHOTOS):
        meta = fdir / "raw" / f"{key}.json"
        if meta.exists():
            r = json.loads(meta.read_text(encoding="utf-8"))
        else:
            if k:
                time.sleep(15)
            r = archive.commons_file(title)   # 파일 이름으로 한 번만 조회 (검색 q 는 다른 사진을 찾을 때 참고용)
            meta.write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
        jpg = fdir / "raw" / f"{key}.jpg"
        if not jpg.exists():
            subprocess.run(["curl", "-sSL", "-A", "ytflow", "-o", str(jpg), r["url"]], check=True)
        mp4 = fdir / f"{key}.mp4"
        if not mp4.exists():
            archive.still_to_clip(jpg, mp4, dur=12)
        out[key] = {"file": mp4.name, "credit": r["credit"], "url": r["page"], "license": r["license"]}
    return out


def scene(src: str, sid: int) -> dict:
    return json.loads(json.dumps(next(s for s in SRC[src]["scenes"] if s["id"] == sid)))


def main():
    for d in ("01_research", "02_script", "05_edit"):
        (P / d).mkdir(parents=True, exist_ok=True)
    fo = photos()
    S = []

    def ch(src, sid, chapter, brand, look, bg_src=None, sub=None):
        s = scene(src, sid)
        s.update({"chapter": chapter, "brand": brand, "look": look})
        if bg_src:
            s["bg_src"] = bg_src
        if sub:
            s["sub"] = sub
        S.append(s)

    def mp(src, sid, chapter, brand):
        s = scene(src, sid)
        s.update({"chapter": chapter, "brand": brand, "map": SRC[src]["map"]})
        s.pop("fx", None)
        S.append(s)

    # 시사 — 증거판 표지 → 증거판 인과 지도 → 듀오톤(붉은) 사진 표지
    ch("issues-aiglasses", 7, 1, "issues", "board", sub="수능 AI 안경 대책")
    mp("issues-aiglasses", 14, 1, "issues")
    ch("issues-aiglasses", 11, 2, "issues", "photo", "exam")
    # 호기심 — 칠판 표지 → 칠판 인과 지도
    ch("curiosity-hallucination", 8, 3, "curiosity", "chalk")
    mp("curiosity-hallucination", 12, 3, "curiosity")
    # 시장 — 대시보드 표지 → 듀오톤(파랑) 사진 표지
    ch("market-nvidia", 4, 4, "market", "dash")
    ch("market-nvidia", 9, 5, "market", "photo", "nyse")
    # AI — 앱 창 표지 → 듀오톤(청록) 사진 표지
    ch("ai-industry-week", 4, 6, "ai", "window")
    ch("ai-industry-week", 9, 7, "ai", "photo", "dc")
    for i, s in enumerate(S, 1):
        s["id"] = i
    spec = {"title": "v15 시험판 — 카테고리 개성·증거판·칠판·듀오톤", "core_message": "카테고리마다 보는 순간 알 수 있는 화면",
            "brand": None, "scenes": S, "footage": fo, "map": SRC["issues-aiglasses"]["map"], "package": {}}
    (P / "02_script" / "hybrid.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
    (P / "edit.yaml").write_text("# v15 시험판 (docs/21) — 장면마다 brand 가 달라 기본 팩은 dark-doc\n"
                                 "edit:\n  style: hybrid\n  style_ref: hybrid\n  family: source\n  skin: dark-doc\n"
                                 "channel: ch-issues\nformat: longform\n", encoding="utf-8")
    (P / "01_research" / "factsheet.md").write_text(
        "# 시험판 팩트시트\n\n대본 문장은 2026-11-11 네 편(projects/20261111-*)에서 이미 출처 확인한 것을 그대로 씀. 새 사실 없음.\n\n## 사진\n"
        + "".join(f"- {k}: {v['credit']} — {v['url']}\n" for k, v in fo.items()), encoding="utf-8")
    print(P, len(S), "장면")


if __name__ == "__main__":
    main()
