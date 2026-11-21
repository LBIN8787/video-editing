"""메인 레포 → 주제 레포 → 영상 한 편: 상황에 맞춰 편집을 채우는 층 (docs/33).

    python -m ytflow topics                 → 주제 레포마다 물려받은·바꾼·더한 상황 요약
    python -m ytflow edit-plan <프로젝트>    → 02_script/edit_plan.json·md (박자마다 상황 → 장면 종류·연출 기법)
                                             + 02_script/EDIT_CONTEXT.md (이 영상에 적용되는 규칙 묶음 — 에이전트가 먼저 읽음)

메인 = manual/ (원칙·작업 기준) + manual/situations.yaml (공통 상황) + styles/techniques.yaml (연출 기법)
주제 = topics/<brand>/topic.yaml — inherits: main, defaults(스타일 기본값 덮어쓰기), situations(add·override·drop)
영상 = projects/<이름> — edit.yaml 의 channel → channels/<id>/channel.yaml 의 brand → 주제
"""
from __future__ import annotations

import copy
import json
import re
from pathlib import Path

import yaml

from .. import config

ROOT = config.ROOT
MAIN_SIT = ROOT / "manual" / "situations.yaml"
TOPICS = ROOT / "topics"
TECH = ROOT / "styles" / "techniques.yaml"
TECH_STATUS = {"have": "있음", "partial": "비슷한 것 있음", "candidate": "후보", "hold": "보류"}


def _y(p: Path) -> dict:
    try:
        return yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    except Exception:
        return {}


def main_situations() -> dict:
    return _y(MAIN_SIT).get("situations", {}) or {}


def techniques() -> dict:
    return _y(TECH).get("techniques", {}) or {}


def topic_ids() -> list[str]:
    return sorted(p.parent.name for p in TOPICS.glob("*/topic.yaml"))


def load_topic(tid: str) -> dict:
    return _y(TOPICS / tid / "topic.yaml")


def resolve(tid: str | None) -> dict:
    """메인 + 주제 → 이 주제의 유효 규칙. 상황마다 origin: main | override | add."""
    sits = {k: {**v, "id": k, "origin": "main"} for k, v in main_situations().items()}
    t = load_topic(tid) if tid else {}
    s = t.get("situations") or {}
    for k in s.get("drop") or []:
        sits.pop(k, None)
    for k, v in (s.get("override") or {}).items():
        if k in sits:
            base = copy.deepcopy(sits[k])
            base.update(v or {})
            base.update(origin="override", base_scenes=sits[k].get("scenes"), base_techniques=sits[k].get("techniques"))
            sits[k] = base
    for k, v in (s.get("add") or {}).items():
        sits[k] = {**(v or {}), "id": k, "origin": "add"}
    avoid_t = set(t.get("avoid_techniques") or [])
    tq = techniques()
    for v in sits.values():
        v["techniques_ok"] = [x for x in v.get("techniques") or [] if x not in avoid_t]
        v["techniques_blocked"] = [x for x in v.get("techniques") or [] if x in avoid_t]
        v["technique_status"] = {x: (tq.get(x) or {}).get("status", "?") for x in v.get("techniques") or []}
        v["_re"] = [re.compile(p) for p in v.get("signals") or []]
    return {"id": tid or "main", "name": t.get("name", "메인 (주제 없음)"), "topic": t, "situations": sits,
            "defaults": t.get("defaults") or {}, "avoid_techniques": sorted(avoid_t), "manual": t.get("manual") or [],
            "channels": t.get("channels") or [], "look": t.get("look", ""),
            "dropped": (s.get("drop") or []), "overridden": list((s.get("override") or {}).keys()),
            "added": list((s.get("add") or {}).keys())}


def brand_of(path: Path) -> str | None:
    ch = (_y(Path(path) / "edit.yaml")).get("channel")
    if not ch:
        return None
    b = _y(ROOT / "channels" / ch / "channel.yaml").get("brand")
    return b if b and (TOPICS / b / "topic.yaml").exists() else None


def detect(text: str, eff: dict) -> list[dict]:
    """한 박자 문장 → 상황 후보 (점수 높은 순). 주제가 더한 상황은 더 구체적이라 조금 더 쳐 줌."""
    out = []
    for k, v in eff["situations"].items():
        hits = [m.group(0) for r in v["_re"] for m in [r.search(text or "")] if m]
        if hits:
            score = len(hits) + (0.5 if v["origin"] == "add" else 0.25 if v["origin"] == "override" else 0)
            out.append({"id": k, "score": score, "hits": hits[:4]})
    return sorted(out, key=lambda x: -x["score"])


def _spec(path: Path) -> dict | None:
    f = Path(path) / "02_script" / "hybrid.json"
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except Exception:
        return None


def plan(path: Path, eff: dict | None = None) -> dict:
    path = Path(path)
    tid = brand_of(path)
    eff = eff or resolve(tid)
    spec = _spec(path) or {}
    rows, counts = [], {}
    for i, sc in enumerate(spec.get("scenes") or []):
        beats = sc.get("beats") or ([{"say": sc.get("say", "")}] if sc.get("say") else [])
        agg: dict[str, float] = {}
        brows = []
        for b in beats:
            say = b.get("say", "") or ""
            d = detect(say, eff)
            brows.append({"say": say[:160], "situations": [x["id"] for x in d[:2]], "hits": d[0]["hits"] if d else []})
            for x in d[:2]:
                agg[x["id"]] = agg.get(x["id"], 0) + x["score"]
        top = sorted(agg.items(), key=lambda kv: -kv[1])
        sid = top[0][0] if top else None
        s = eff["situations"].get(sid) if sid else None
        cur = sc.get("type")
        rec = {"scene": i + 1, "type": cur, "chapter": sc.get("chapter"), "situation": sid,
               "situation_name": s.get("name") if s else None, "origin": s.get("origin") if s else None,
               "also": [k for k, _ in top[1:3]], "beats": brows}
        if s:
            counts[sid] = counts.get(sid, 0) + 1
            rec.update(recommended_scenes=s.get("scenes") or [], type_fits=cur in (s.get("scenes") or []) or cur in ("chapter",),
                       techniques=[{"id": t, "status": s["technique_status"].get(t, "?")} for t in s["techniques_ok"]],
                       blocked=s["techniques_blocked"], avoid=s.get("avoid", ""), why=s.get("why", ""))
        rows.append(rec)
    matched = [r for r in rows if r["situation"]]
    return {"project": path.name, "topic": eff["id"], "topic_name": eff["name"], "scenes": rows,
            "coverage": round(len(matched) / len(rows), 2) if rows else 0,
            "fit": round(sum(1 for r in matched if r.get("type_fits")) / len(matched), 2) if matched else 0,
            "counts": dict(sorted(counts.items(), key=lambda kv: -kv[1])), "defaults": eff["defaults"]}


def context_md(eff: dict, p: dict | None = None) -> str:
    """이 영상(또는 주제)에 적용되는 규칙 묶음 — 맷 포콕식 '프로젝트마다 한 번 셋업한 CLAUDE.md' 역할."""
    from . import manualgraph as mg
    tq = techniques()
    L = [f"# 편집 맥락 — {p['project'] if p else eff['name']}", "",
         "> 자동 생성 (python -m ytflow edit-plan). 고치지 말고 메인(manual/·manual/situations.yaml·styles/techniques.yaml)이나 "
         f"주제 레포(topics/{eff['id']}/topic.yaml)를 고친 뒤 다시 만드세요.", "",
         f"**층:** 메인 → 주제 `{eff['id']}` ({eff['name']})" + (f" → 영상 `{p['project']}`" if p else ""), ""]
    L += ["## 1. 메인에서 물려받는 것 (모든 영상)",
          "- 영구 원칙 = `manual/README.md` §3 (진짜 금지) · 규칙의 네 층 = §3-1 (스타일 기본값·실험 기록은 금지 아님)",
          "- 작업 절차 8단계 + check 게이트 G0~G8 = `manual/README.md` §2, `manual/06-checklist.md`",
          "- 인트로 없음·미주일기 문법·길이는 종류·대본이 정함 = README §2-1·§2-3·§2-4 · 말하는 것이 화면에 생긴다 (작업 기준)", ""]
    try:
        g = mg.build()
        bans = [b for b in g["bans"] if b.get("tier") == "principle"]
        L += ["### 영구 원칙 (요약)"] + [f"- {b['text'][:110]}" for b in bans if b.get("absolute")][:7] + [""]
    except Exception:
        pass
    L += [f"## 2. 주제 `{eff['id']}` 가 바꾸는 것", f"- 매뉴얼: {', '.join(eff['manual']) or '-'} · 화면 개성: {eff['look'] or '-'}",
          "- 스타일 기본값 (금지 아님): " + (", ".join(f"`{k}: {v}`" for k, v in eff["defaults"].items()) or "-"),
          f"- 이 주제에서 기본으로 쓰지 않는 기법: {', '.join(eff['avoid_techniques']) or '-'}",
          f"- 더한 상황: {', '.join(eff['added']) or '-'} · 바꾼 상황: {', '.join(eff['overridden']) or '-'} · 뺀 상황: {', '.join(eff['dropped']) or '-'}", ""]
    L += ["## 3. 상황 → 화면 (이 주제의 유효 표)", "| 상황 | 출처 | 1순위 → 2순위 장면 | 연출 기법 (상태) | 피할 것 |", "|---|---|---|---|---|"]
    for k, s in eff["situations"].items():
        tech = ", ".join(f"{t}({TECH_STATUS.get((tq.get(t) or {}).get('status'), '?')})" for t in s["techniques_ok"]) or "-"
        o = {"main": "메인", "override": "주제가 바꿈", "add": "주제가 더함"}[s["origin"]]
        L.append(f"| {s.get('name', k)} | {o} | {' → '.join(s.get('scenes') or [])} | {tech} | {s.get('avoid', '')} |")
    if p:
        L += ["", f"## 4. 이 영상에서 찾은 상황 (장면 {len(p['scenes'])}개 · 상황을 찾은 장면 {int(p['coverage'] * 100)}% · 지금 장면 종류가 추천과 맞는 비율 {int(p['fit'] * 100)}%)",
              "", "| 장면 | 지금 | 상황 | 추천 장면 | 기법 |", "|---|---|---|---|---|"]
        for r in p["scenes"]:
            if not r["situation"]:
                L.append(f"| {r['scene']} | {r['type']} | (못 찾음) | | |")
                continue
            mark = "" if r.get("type_fits") else " ⚠"
            L.append(f"| {r['scene']} | {r['type']}{mark} | {r['situation_name']} | {' → '.join(r['recommended_scenes'])} | "
                     + ", ".join(f"{t['id']}({TECH_STATUS.get(t['status'], '?')})" for t in r["techniques"]) + " |")
        L += ["", "⚠ = 지금 장면 종류가 상황의 추천 목록에 없음 — 틀린 게 아니라 다시 볼 곳. 기법이 '후보'면 아직 렌더러에 없음."]
    return "\n".join(L) + "\n"


def write_plan(path: Path) -> Path:
    path = Path(path)
    p = plan(path)
    eff = resolve(p["topic"] if p["topic"] != "main" else None)
    d = path / "02_script"
    d.mkdir(parents=True, exist_ok=True)
    md = context_md(eff, p)
    visual_guide = "[표현 방식과 인포그래픽 레퍼런스](../../../manual/12-visual-storytelling.md)"
    guide = "[대본별 화풍과 움직임](../../../docs/42-script-to-motion.md)"
    pinned = d / "motion_edition.json"
    if pinned.is_file():
        edition = json.loads(pinned.read_text(encoding="utf-8-sig"))
        p["visual_handoff"] = {"source": pinned.name, "style": edition["style"], "shots": len(edition["shots"])}
        handoff = (f"**이 편의 연출 판본** · {edition['style']} · [발화별 실제 장면표]({pinned.name})\n\n"
                   f"해당 장면표의 순서·원화·동작을 기본 제작 명령으로 재생한다. 아래 자동 추천은 기획 참고 자료다. {guide} · {visual_guide}")
    elif p["topic"] == "issues":
        handoff = (f"**S5 장면 기획** · {visual_guide}를 참고한다. 기존 스페인독감 편처럼 실제 사진·영상·지면으로 "
                   "사건을 확인하고, 지도·연표·인포그래픽으로 관계를 설명한다. 장면표에 대사, 확인할 근거, "
                   "출처, 자료에서 지목할 부분과 보여 줄 시간을 기록한다.")
    else:
        handoff = (f"**S5 연출 선택** · {visual_guide}로 장면의 표현 방식을 고른다. 행동 중심 장면은 {guide}에 따라 "
                   "시작 상태, 변화가 일어나는 말, 도착 상태와 다음 컷의 첫 자세를 기록한다. "
                   "D3에는 이 장면들이 이어지는 동영상과 화풍 승인 범위를 함께 제시한다.")
    first, _, rest = md.partition("\n")
    md = f"{first}\n\n{handoff}\n\n{rest}"
    (d / "edit_plan.json").write_text(json.dumps(p, ensure_ascii=False, indent=1), encoding="utf-8")
    (d / "EDIT_CONTEXT.md").write_text(md, encoding="utf-8")
    (d / "edit_plan.md").write_text(md.split("## 4.", 1)[-1].join(["## 4.", ""]) if "## 4." in md else md, encoding="utf-8")
    print(f"[edit-plan] {path.name} · 주제 {p['topic']} · 장면 {len(p['scenes'])} · 상황 찾음 {int(p['coverage'] * 100)}% · "
          f"장면 종류 맞음 {int(p['fit'] * 100)}% → 02_script/EDIT_CONTEXT.md, edit_plan.json")
    return d / "EDIT_CONTEXT.md"


def corpus(limit_examples: int = 3) -> dict:
    """모든 영상에 상황 찾기를 돌려, 주제마다 상황이 얼마나·어떤 문장에서 나왔나 (그래프용)."""
    out: dict = {}
    for pdir in sorted((ROOT / "projects").iterdir()):
        if not (pdir / "02_script" / "hybrid.json").exists():
            continue
        tid = brand_of(pdir)
        if not tid:
            continue
        try:
            p = plan(pdir)
        except Exception:
            continue
        t = out.setdefault(tid, {"projects": [], "situations": {}})
        t["projects"].append({"project": pdir.name, "scenes": len(p["scenes"]), "coverage": p["coverage"], "fit": p["fit"],
                              "rows": [{"s": r["scene"], "type": r["type"], "sit": r["situation"], "fit": bool(r.get("type_fits")),
                                        "rec": (r.get("recommended_scenes") or [])[:3],
                                        "say": (r["beats"][0]["say"] if r["beats"] else "")[:90]} for r in p["scenes"]]})
        for r in p["scenes"]:
            if not r["situation"]:
                continue
            s = t["situations"].setdefault(r["situation"], {"count": 0, "fit": 0, "examples": []})
            s["count"] += 1
            s["fit"] += 1 if r.get("type_fits") else 0
            if len(s["examples"]) < limit_examples:
                say = next((b["say"] for b in r["beats"] if r["situation"] in b["situations"]), "")
                s["examples"].append({"project": pdir.name, "scene": r["scene"], "type": r["type"], "say": say[:120],
                                      "fit": bool(r.get("type_fits"))})
    return out


def listing() -> str:
    L = []
    for tid in topic_ids():
        e = resolve(tid)
        L.append(f"{tid:10s} {e['name']} — 상황 {len(e['situations'])} (메인 {sum(1 for s in e['situations'].values() if s['origin'] == 'main')} · "
                 f"바꿈 {len(e['overridden'])} · 더함 {len(e['added'])} · 뺌 {len(e['dropped'])}) · 기본값 {e['defaults']}")
    return "\n".join(L)
