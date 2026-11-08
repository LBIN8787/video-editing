"""상황에 맞는 편집 스타일 고르기 — 등록부(styles/recipes/*.yaml) × 주제 기획서(topic_brief.json).

    python -m ytflow recipes                 # 등록된 스타일(레시피) 목록
    python -m ytflow style-pick <프로젝트>    # 이 영상에 맞는 스타일: 영상 전체 · 훅 · 결론 → 01_research/style_pick.md

스타일을 늘리려면 styles/recipes/_template.yaml 을 복사해 파일 하나만 추가하면 된다 (코드 수정 없음).
채널(브랜드)을 늘리려면 channels/brands.yaml 에 항목 하나 + channels/<라인>/channel.yaml (manual/07-extend.md).
"""
from __future__ import annotations

import json
from pathlib import Path

import yaml

from .. import config

RECIPES = config.ROOT / "styles" / "recipes"
NEED_WORDS = {"footage": ["영상", "영화", "footage", "화면"], "archive": ["기록", "의회도서관", "archive", "사진", "NASA"],
              "map": ["지도", "경로", "어디", "→"], "price": ["시세", "주가", "지수", "price"],
              "screen": ["화면 녹화", "실행 화면", "녹화", "데모"], "statement": ["발언", "인터뷰", "실적 콜", "녹취", "연설"]}
STATUS_BONUS = {"approved": 1.0, "demo": 0.5, "idea": -1.0}


def load() -> list[dict]:
    out = []
    for f in sorted(RECIPES.glob("*.yaml")):
        if f.name.startswith("_"):
            continue
        r = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        r.setdefault("id", f.stem)
        out.append(r)
    return out


def skins_for(brand: str) -> set[str]:
    return {r.get("skin") for r in load() if brand in (r.get("fits") or {}).get("brands", [])}


def score(r: dict, tb: dict) -> tuple[float, list[str]]:
    fits, why = r.get("fits") or {}, []
    brand = tb.get("brand", "")
    if brand and brand not in fits.get("brands", []):
        return -99, ["브랜드 불일치"]
    fmt = tb.get("format", "longform")
    if fmt not in r.get("format", ["longform"]):
        return -99, ["형식 불일치"]
    s = 2.0
    hit = [q for q in fits.get("questions", []) if q == tb.get("question_type")]
    if hit:
        s += 3
        why.append(f"질문 유형 {'·'.join(hit)}")
    moods = tb.get("mood") or []
    mh = [m for m in fits.get("moods", []) if m in moods]
    s += len(mh)
    if mh:
        why.append(f"분위기 {'·'.join(mh)}")
    src = " ".join(tb.get("visual_sources") or []) + " " + tb.get("topic", "")
    for n in fits.get("needs", []):
        if any(w in src for w in NEED_WORDS.get(n, [n])):
            s += 1
            why.append(f"소스 있음({n})")
        else:
            s -= 2
            why.append(f"소스 확인 필요({n})")
    s += STATUS_BONUS.get(r.get("status", "idea"), 0)
    return s, why


def pick(tb: dict) -> dict:
    ranked = sorted(((score(r, tb), r) for r in load()), key=lambda x: -x[0][0])
    ranked = [(s, w, r) for (s, w), r in ranked if s > -50]

    def best(role):
        for s, w, r in ranked:
            if role in r.get("roles", []):
                return {"id": r["id"], "name": r["name"], "score": s, "why": w, "skin": r.get("skin"), "scene_types": r.get("scene_types"),
                        "status": r.get("status"), "skill": r.get("skill"), "demo": r.get("demo")}
        return None

    base = best("whole") or best("body")
    return {"base": base, "hook": best("hook"), "ending": best("ending"),
            "mix": [{"id": r["id"], "score": s, "why": w, "roles": r.get("roles")} for s, w, r in ranked[:5]]}


def run(path: Path) -> Path:
    f = path / "01_research" / "topic_brief.json"
    if not f.exists():
        raise SystemExit("01_research/topic_brief.json 이 없습니다 (manual/01-desire-map.md, prompts/topic_desire.md)")
    tb = json.loads(f.read_text(encoding="utf-8"))
    res = pick(tb)
    (path / "01_research" / "style_pick.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    b = res["base"] or {}
    L = [f"# 스타일 고르기 — {path.name}", "",
         f"브랜드 **{tb.get('brand')}** · 질문 \"{tb.get('viewer_question', '')}\" ({tb.get('question_type', '')}) · 분위기 {tb.get('mood', [])}", "",
         "| 자리 | 스타일 | 그래픽 팩 | 뼈대 장면 | 이유 |", "|---|---|---|---|---|"]
    for role, label in (("base", "영상 전체(기본)"), ("hook", "훅 (첫 30초)"), ("ending", "결론")):
        r = res[role]
        if r:
            L.append(f"| {label} | `{r['id']}` {r['name']} ({r['status']}) | {r['skin']} | {', '.join(r['scene_types'] or [])} | {', '.join(r['why'])} |")
    L += ["", "**그래픽 팩은 영상 전체의 것 하나**만 씁니다 (훅·결론 스타일은 연출 장면 type 만 빌려 옴).",
          f"→ `edit.yaml` 의 `skin: {b.get('skin')}`, 훅·결론 장면 type 은 위 표대로 hybrid.json 에.", "",
          "후보 순위:", ""] + [f"- `{m['id']}` {m['score']:.1f}점 — {', '.join(m['why'])}" for m in res["mix"]]
    out = path / "01_research" / "style_pick.md"
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    return out


def listing() -> str:
    rows = ["| id | 이름 | 상태 | 그래픽 팩 | 브랜드 | 질문 유형 | 자리 |", "|---|---|---|---|---|---|---|"]
    for r in load():
        f = r.get("fits") or {}
        rows.append(f"| {r['id']} | {r.get('name')} | {r.get('status')} | {r.get('skin')} | {','.join(f.get('brands', []))} | "
                    f"{','.join(f.get('questions', []))} | {','.join(r.get('roles', []))} |")
    return "\n".join(rows)
