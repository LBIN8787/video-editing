"""연출 결정 기록 — 여러 연출·편집·스타일 가운데 '이것'을 고른 근거와 의도를 남긴다 (docs/66, manual/05 §0-9).

2026-11-24 사용자: "단순 다큐를 사용할때만 이를 작성하는 것이 아니라 선택과 방향성 설정에 있어서 이를 기록하라는 것 입니다.
다양한 연출법 편집법 스타일들이 존재하는데 그 다양한 것들 중 이것을 선택한 근거와 의도가 명확해야합니다.
제가 주의하는건 추적 불가능하고 일관성이 없는 단순 슬롭입니다."

방송·대형 제작 팀은 애니메이션 전에 트리트먼트(방향 문서)·스타일 프레임·애니매틱으로 '무엇을 왜'를 먼저 정하고 잠근다
(docs/66 §2). 우리도 렌더 전에 두 층으로 적는다:

hybrid.json 맨 위 — 영상 전체 방향 (한 번):
  "direction": {"pick": "시각 언어 이름 (스타일 등록부 id 또는 한 줄)",
                "over": [{"id": "고려한 다른 스타일 id", "why_not": "이 영상에서 그것으로는 무엇이 안 되나"}],
                "why": "왜 이 방향인가 (질문·소스·시청자)", "intent": "시청자가 이 영상에서 얻을 것",
                "vocabulary": ["이 영상에서 쓰는 장면 종류 — 닫힌 목록"], "refs": ["docs/65-...md", "technique:draw-on", "recipe:..."]}
장면마다 — "decide":
  {"situation": "상황 id (manual/situations.yaml·topics)", "pick": "이 장면 type",
   "over": [{"id": "다른 장면 종류", "why_not": "..."}], "why": "왜 이것", "intent": "이 장면이 끝나면 시청자는 …",
   "refs": [...], "differs": "같은 상황인데 앞 장면과 다른 것을 고른 이유 (그럴 때만)",
   "new_vocab": "vocabulary 밖의 장면 종류를 쓰는 이유 (그럴 때만)"}

검사 (python -m ytflow decide <프로젝트> → 02_script/DIRECTION_LOG.md · direction_log.json):
  추적 가능 — 기록한 pick 이 실제 장면 type 과 같다 · refs 가 실제로 있는 파일·기법·스타일 · 상황 id 가 등록된 것
  근거 있음 — why·intent·over(대안과 버린 이유) 가 있고, 다른 장면의 why 를 그대로 복사하지 않음
  추천과 다르면 — edit-plan 1순위를 over 에 적고 왜 버렸는지 (추천이 틀렸을 수도 있음 — 그것도 기록)
  일관성 — 같은 상황에서 다른 장면을 고르면 differs, vocabulary 밖이면 new_vocab
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from .. import config

SKIP_TYPES = {"chapter", "outro"}   # 장 표지·마무리는 형식이 정해진 자리 — 결정 기록 대상 아님
TODO = "TODO"


def _known() -> dict:
    from . import layers, hybrid
    from .. import config as _c
    rec = {p.stem for p in (_c.ROOT / "styles" / "recipes").glob("*.yaml")}
    return {"types": set(hybrid.RENDER) | {"bite", "kinetic"}, "techniques": set(layers.techniques()), "recipes": rec}


def _ref_ok(ref: str, known: dict) -> bool:
    r = str(ref).strip()
    if r.startswith("technique:"):
        return r.split(":", 1)[1] in known["techniques"]
    if r.startswith("recipe:"):
        return r.split(":", 1)[1] in known["recipes"]
    if r.startswith("type:"):
        return r.split(":", 1)[1] in known["types"]
    if r.startswith("http://") or r.startswith("https://"):
        return True
    return (config.ROOT / r.split("#", 1)[0]).exists()


def _filled(s) -> bool:
    s = str(s or "").strip()
    return bool(s) and TODO not in s


def check(path: Path) -> dict:
    """결과: {"items": [{level, scene, msg}], "rows": [...], "pass": bool}. level: MUST | SHOULD."""
    from . import layers
    spec = json.loads((path / "02_script" / "hybrid.json").read_text(encoding="utf-8"))
    ep = path / "02_script" / "edit_plan.json"
    plan = json.loads(ep.read_text(encoding="utf-8")) if ep.exists() else {}
    rec_by_scene = {s["scene"]: s for s in plan.get("scenes", [])}
    eff = layers.resolve(layers.brand_of(path))
    sits = eff["situations"]
    known = _known()
    items, rows = [], []

    def add(level, scene, msg):
        items.append({"level": level, "scene": scene, "msg": msg})

    d = spec.get("direction") or {}
    if not d:
        add("MUST", 0, "영상 방향(direction) 없음 — 시각 언어 하나를 고른 근거·의도·고려한 대안")
    else:
        for k in ("pick", "why", "intent"):
            if not _filled(d.get(k)):
                add("MUST", 0, f"direction.{k} 비어 있음")
        if not [o for o in d.get("over") or [] if _filled(o.get("why_not"))]:
            add("MUST", 0, "direction.over — 고려한 다른 스타일과 버린 이유가 하나도 없음")
        if not d.get("vocabulary"):
            add("MUST", 0, "direction.vocabulary — 이 영상에서 쓰는 장면 종류(닫힌 목록)가 없음")
        for r in d.get("refs") or []:
            if not _ref_ok(r, known):
                add("MUST", 0, f"direction.refs '{r}' 를 찾을 수 없음 (추적 불가)")
    vocab = set(d.get("vocabulary") or [])

    whys: dict = {}
    first_pick: dict = {}
    for sc in spec.get("scenes", []):
        sid, typ = sc.get("id"), sc.get("type")
        if typ in SKIP_TYPES:
            continue
        dc = sc.get("decide") or {}
        rp = rec_by_scene.get(sid, {})
        rec = rp.get("recommended_scenes") or []
        row = {"scene": sid, "type": typ, "situation": dc.get("situation") or rp.get("situation", ""), "pick": dc.get("pick", ""),
               "rec": rec, "over": [o.get("id") for o in dc.get("over") or []], "why": dc.get("why", ""), "intent": dc.get("intent", ""),
               "refs": dc.get("refs") or [], "differs": dc.get("differs", ""), "new_vocab": dc.get("new_vocab", "")}
        rows.append(row)
        if not dc:
            add("MUST", sid, f"결정 기록(decide) 없음 — {typ} 를 고른 근거·의도·대안")
            continue
        if dc.get("pick") != typ:
            add("MUST", sid, f"기록한 pick '{dc.get('pick')}' ≠ 실제 장면 '{typ}' (기록과 화면이 다르면 추적 불가)")
        sit = dc.get("situation")
        if not sit or sit not in sits:
            add("MUST", sid, f"situation '{sit}' 이 등록된 상황이 아님 (manual/situations.yaml·topics) — 새 상황이면 주제 레포에 먼저")
        for k in ("why", "intent"):
            if not _filled(dc.get(k)):
                add("MUST", sid, f"{k} 비어 있음")
        overs = [o for o in dc.get("over") or [] if _filled(o.get("why_not"))]
        if not overs:
            add("MUST", sid, "over — 고려한 다른 장면 종류와 버린 이유가 하나도 없음")
        for o in dc.get("over") or []:
            if o.get("id") and o["id"] not in known["types"]:
                add("SHOULD", sid, f"over '{o['id']}' 는 등록된 장면 종류가 아님")
        if rec and typ not in rec and rec[0] not in [o.get("id") for o in overs]:
            add("MUST", sid, f"edit-plan 1순위 '{rec[0]}' 대신 '{typ}' — over 에 '{rec[0]}' 와 버린 이유를 적기 (추천이 틀렸으면 그렇게)")
        for r in dc.get("refs") or []:
            if not _ref_ok(r, known):
                add("MUST", sid, f"refs '{r}' 를 찾을 수 없음 (추적 불가)")
        w = str(dc.get("why", "")).strip()
        if w and w in whys:
            add("MUST", sid, f"why 가 장면 {whys[w]} 와 똑같음 (복사한 이유는 이유가 아님)")
        elif w:
            whys[w] = sid
        if vocab and typ not in vocab and not _filled(dc.get("new_vocab")):
            add("MUST", sid, f"'{typ}' 는 direction.vocabulary 밖 — new_vocab 에 이 영상에서 새 장면을 쓰는 이유")
        if sit:
            if sit in first_pick and first_pick[sit][1] != typ and not _filled(dc.get("differs")):
                add("MUST", sid, f"같은 상황 '{sit}' 인데 장면 {first_pick[sit][0]} 은 '{first_pick[sit][1]}', 여기는 '{typ}' — differs 에 이유")
            first_pick.setdefault(sit, (sid, typ))
    return {"items": items, "rows": rows, "direction": d, "pass": not any(i["level"] == "MUST" for i in items)}


def draft(path: Path) -> int:
    """decide 가 없는 장면에 edit-plan 추천으로 뼈대를 채움 — why·intent·why_not 은 TODO (채우기 전엔 검사 실패)."""
    p = path / "02_script" / "hybrid.json"
    spec = json.loads(p.read_text(encoding="utf-8"))
    ep = path / "02_script" / "edit_plan.json"
    plan = {s["scene"]: s for s in (json.loads(ep.read_text(encoding="utf-8")).get("scenes", []) if ep.exists() else [])}
    n = 0
    if not spec.get("direction"):
        spec["direction"] = {"pick": TODO, "over": [{"id": TODO, "why_not": TODO}], "why": TODO, "intent": TODO,
                             "vocabulary": sorted({s["type"] for s in spec["scenes"] if s["type"] not in SKIP_TYPES}), "refs": []}
        n += 1
    for sc in spec["scenes"]:
        if sc["type"] in SKIP_TYPES or sc.get("decide"):
            continue
        rp = plan.get(sc["id"], {})
        rec = [r for r in rp.get("recommended_scenes") or [] if r != sc["type"]]
        sc["decide"] = {"situation": rp.get("situation", TODO), "pick": sc["type"],
                        "over": [{"id": r, "why_not": TODO} for r in rec[:2]] or [{"id": TODO, "why_not": TODO}],
                        "why": TODO, "intent": TODO, "refs": []}
        n += 1
    p.write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return n


def write(path: Path) -> Path:
    r = check(path)
    out = path / "02_script" / "DIRECTION_LOG.md"
    d = r["direction"]
    L = [f"# 연출 결정 기록 — {path.name}", "",
         "여러 연출·편집·스타일 가운데 이것을 고른 근거와 의도 (manual/05 §0-9, docs/66). 렌더 전에 이 한 장으로 검토합니다.", "",
         f"**결과: {'통과' if r['pass'] else '실패 — MUST ' + str(sum(i['level'] == 'MUST' for i in r['items'])) + '개'}**", "",
         "## 영상 방향", ""]
    if d:
        L += [f"- 고른 것: **{d.get('pick', '')}**", f"- 왜: {d.get('why', '')}", f"- 의도: {d.get('intent', '')}"]
        L += [f"- 버린 것: `{o.get('id')}` — {o.get('why_not', '')}" for o in d.get("over") or []]
        L += [f"- 이 영상의 장면 어휘(닫힌 목록): {', '.join(d.get('vocabulary') or [])}", f"- 근거 문서: {', '.join(d.get('refs') or []) or '-'}"]
    else:
        L.append("- (없음)")
    L += ["", "## 장면마다", "", "| 장면 | 상황 | 고른 것 | 추천(edit-plan) | 버린 것 | 왜 | 의도 |", "|---|---|---|---|---|---|---|"]
    for w in r["rows"]:
        L.append(f"| {w['scene']} | {w['situation']} | {w['type']} | {' → '.join(w['rec'])} | {', '.join(x for x in w['over'] if x)} | "
                 f"{w['why']}{' (다른 선택 이유: ' + w['differs'] + ')' if w['differs'] else ''} | {w['intent']} |")
    if r["items"]:
        L += ["", "## 고칠 곳", ""] + [f"- [{i['level']}] 장면 {i['scene']}: {i['msg']}" for i in r["items"]]
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    (path / "02_script" / "direction_log.json").write_text(json.dumps({k: v for k, v in r.items()}, ensure_ascii=False, indent=1), encoding="utf-8")
    return out


def applies(path: Path) -> bool:
    """2026-11-25 이후 영상부터 MUST (그 전 영상은 기록이 없던 시절 — 참고로만)."""
    m = re.match(r"(\d{8})", path.name)
    return bool(m) and m.group(1) >= "20261125"
