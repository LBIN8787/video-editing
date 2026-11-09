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
    L += ["", f"**기본 그래픽 팩**은 `edit.yaml` 의 `skin: {b.get('skin')}`. 특정 구간만 다른 팩이 맞으면 그 장면에 `\"skin\": \"<팩>\"` (예: 지도 장면만 newsprint, 인용 한 줄만 dark-doc).", "",
          "후보 순위:", ""] + [f"- `{m['id']}` {m['score']:.1f}점 — {', '.join(m['why'])}" for m in res["mix"]]
    L += plan_text(res)
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


# ------------------------------------------------------------------ 조합 규칙 (manual/05 §0-1, 사용자 판정 2026-11-09)
# 한 스타일로만 쭉 가면 불합격. 장면마다 다른 스타일 + 한 장면 안에서 겹치기(layers)가 기본.
MIX_RULES = {"longform": {"min_recipes": 4, "max_share": 0.40, "min_layered": 3, "max_run": 2},
             "shorts": {"min_recipes": 2, "max_share": 0.60, "min_layered": 1, "max_run": 2}}
NEUTRAL = {"chapter", "outro", "intro"}
GOOD_LAYERS = [("kb", "locator", "자료 화면 + 위치 미니 지도 (아카이브 × 지도)"),
               ("kb", "number", "자료 화면 + 큰 숫자 카드 (아카이브 × 데이터)"),
               ("journey", "photo", "지도 이동 + 그곳의 자료 사진 액자 (지도 × 아카이브)"),
               ("footage", "stamp", "원본 영상 + 날짜·장소 타자기 (하이브리드 × 아카이브)"),
               ("bars", "photo", "막대 비교 + 비교 대상의 사진 (데이터 × 아카이브)"),
               ("chart", "number", "주가 그래프 + 그날의 숫자 하나 (데이터, 영상에서 가장 중요한 숫자에만)")]


def type_owner() -> dict:
    out = {}
    for r in load():
        for t in r.get("owns") or []:
            out.setdefault(t, r["id"])
    return out


def mix_stats(spec: dict, timeline: list | None = None) -> dict:
    from . import hybrid  # noqa: F401  (directions 는 hybrid 를 먼저 불러야 함)
    from .directions import LAYER_KINDS
    own = type_owner()
    durs = {s["scene"]: s["dur"] for s in (timeline or [])}
    seq, share, used, layered = [], {}, set(), 0
    for sc in spec.get("scenes", []):
        t = sc.get("type")
        if t in NEUTRAL:
            continue
        rid = sc.get("recipe") or own.get(t, f"?{t}")   # 장면이 스스로 밝힌 스타일(예: 화면 녹화 footage → screen-demo)이 우선
        d = durs.get(sc.get("id"), 5.0 * max(len(sc.get("beats", [])), 1))
        seq.append(rid)
        share[rid] = share.get(rid, 0) + d
        used.add(rid)
        lk = {LAYER_KINDS.get(L.get("kind")) for L in sc.get("layers") or []} - {None, rid}
        used |= lk
        layered += bool(lk)
    tot = sum(share.values()) or 1
    run, best = 1, 1
    for a, b in zip(seq, seq[1:]):
        run = run + 1 if a == b else 1
        best = max(best, run)
    top = max(share.items(), key=lambda kv: kv[1]) if share else ("", 0)
    return {"recipes": sorted(used), "n_recipes": len(used), "top": top[0], "top_share": round(top[1] / tot, 2),
            "layered_scenes": layered, "max_run": best if seq else 0, "sequence": seq}


def plan_text(res: dict) -> list[str]:
    L = ["", "## 조합 계획 (한 스타일로만 만들지 않습니다)", "",
         "| 구간 | 쓸 스타일 (2개 이상 섞기) |", "|---|---|"]
    body = [m["id"] for m in res["mix"] if "body" in (m.get("roles") or []) or "whole" in (m.get("roles") or [])][:3]
    hook = [m["id"] for m in res["mix"] if "hook" in (m.get("roles") or [])][:2]
    end = [m["id"] for m in res["mix"] if "ending" in (m.get("roles") or [])][:2]
    L += [f"| 훅 (첫 30초) | {' + '.join(hook) or '-'} |", f"| 본론 | {' → '.join(body)} (장면마다 번갈아) |", f"| 결론 | {' + '.join(end) or '-'} |", "",
          "한 장면 안에서 겹치기 (`layers`) — 영상마다 3장면 이상, **강조가 아니라 내용**(사진·지도·도장)으로:", ""]
    L += [f"- `{a}` + `{b}`: {why}" for a, b, why in GOOD_LAYERS]
    r = MIX_RULES["longform"]
    L += ["", f"규칙(롱폼): 스타일 {r['min_recipes']}종 이상 · 한 스타일이 {int(r['max_share'] * 100)}% 넘지 않게 · 겹친 장면 {r['min_layered']}개 이상 · "
          f"같은 스타일 {r['max_run'] + 1}장면 연속 금지 · 강조는 1분에 1번 이하, 자막과 같은 문장 반복 금지 (`check` G5 가 검사)"]
    return L


# ------------------------------------------------------------------ 강조 아껴 쓰기 (사용자 판정 2026-11-09: 남용은 안 쓰는 것만 못하다)
EMPHASIS_PER_MIN = 1.0      # 강조(핵심 단어 띄우기·큰 숫자 카드·메모 쪽지·키네틱 장면)는 1분에 1번 이하
EMPHASIS_MAX_HITS = 3


def emphasis_stats(spec: dict, total_s: float) -> dict:
    items, bad_words, crowded = [], [], []
    for sc in spec.get("scenes", []):
        n = 0
        if sc.get("type") == "kinetic":
            items.append((sc.get("id"), "kinetic"))
            n += 1
        for L in sc.get("layers") or []:
            if L.get("kind") in ("words", "number", "mark"):
                items.append((sc.get("id"), L["kind"]))
                n += 1
                if L["kind"] == "words" and not (1 <= len(L.get("hit") or []) <= EMPHASIS_MAX_HITS):
                    bad_words.append(sc.get("id"))
        for b in sc.get("beats", []):
            if b.get("vox"):
                items.append((sc.get("id"), "vox"))
                n += 1
        if n > 1:
            crowded.append(sc.get("id"))
    limit = max(2, round(total_s / 60 * EMPHASIS_PER_MIN))
    return {"count": len(items), "limit": limit, "items": items, "bad_words": bad_words, "crowded": crowded}


# ---------------------------------------------------------------- 반복 피로 (manual v9, 05 §0-3)
# 글씨·도형만으로 된 자체 제작 장면 = 'plain'. 자료 화면·지도·실제 화면·사진 겹치기·시각 효과가 있으면 '눈요기(hook)'.
PLAIN_TYPES = {"bignum", "bars", "versus", "checklist", "card_type", "analogy", "timeline", "map_causal", "quote",
               "chart", "statement", "explain", "people", "compare_values", "proportion"}
HOOK_TYPES = {"kb", "journey", "choropleth", "zoomshot", "chat", "terminal", "footage", "source", "usmap", "intro", "kinetic"}
HOOK_LAYERS = {"photo", "locator", "mark"}


def visual_hooks(sc: dict) -> list[str]:
    """장면의 눈요기 목록 (비어 있으면 글씨·도형뿐인 plain 장면)."""
    out = []
    if sc.get("type") in HOOK_TYPES or sc.get("clip"):
        out.append(sc.get("type"))
    out += [f"layer:{L.get('kind')}" for L in sc.get("layers") or [] if L.get("kind") in HOOK_LAYERS]
    fx = sc.get("fx") or []
    out += [f"fx:{f}" for f in ([fx] if isinstance(fx, str) else fx)]
    if sc.get("bg") == "photo":
        out.append("bg:photo")
    return out


def variety_stats(spec: dict) -> dict:
    scenes = [s for s in spec.get("scenes", []) if s.get("type") not in NEUTRAL]
    hooks = [visual_hooks(s) for s in scenes]
    run, worst, at = 0, 0, None
    for s, h in zip(scenes, hooks):
        run = 0 if h else run + 1
        if run > worst:
            worst, at = run, s.get("id")
    fxs = [f for h in hooks for f in h if f.startswith("fx:")]
    fx_runs = [scenes[i]["id"] for i in range(len(hooks) - 2)
               if set(f for f in hooks[i] if f.startswith("fx:")) & set(f for f in hooks[i + 1] if f.startswith("fx:"))
               & set(f for f in hooks[i + 2] if f.startswith("fx:"))]
    sig = sorted({f for h in hooks for f in h} | {s.get("type") for s in scenes})
    return {"n": len(scenes), "hooked": sum(1 for h in hooks if h), "ratio": round(sum(1 for h in hooks if h) / max(1, len(scenes)), 2),
            "plain_run": worst, "plain_run_at": at, "fx_kinds": sorted(set(fxs)), "fx_runs": fx_runs, "signature": sig}
