"""매뉴얼 지식 그래프 — 영상편집 에이전트의 '정책'을 기계가 읽는 그래프로.

    python -m ytflow manual-graph [--html 파일]   → manual/graph.json (+ 보기 전용 HTML 한 장)
    python -m ytflow manual-ui [--port 8770]     → 그래프 보기 + 매뉴얼 고치기·검토 기록·버전 올리기 (로컬 서버)

매뉴얼(manual/*.md)이 에이전트의 판단 기준이고, 사용자 검토(reviews.md) → 반영 대기 → 버전(CHANGELOG.md)
→ 고친 절·규칙·검사 코드로 이어지는 흐름을 노드와 엣지로 만든다. 사람이 손으로 고치는 원본은 여전히 md 파일이고,
graph.json 은 언제든 다시 만들 수 있는 파생물이다 (docs/31-manual-graph.md).

노드 kind: step · gate · channel · doc · section · rule · check · version · review · theme
엣지 kind: gated_by · contains · defines · belongs_to · enforces · applied_in · approved_in · touched · about · guided_by
"""
from __future__ import annotations

import datetime as dt
import json
import re
import subprocess
from pathlib import Path

from .. import config

ROOT = config.ROOT
MANUAL = ROOT / "manual"
SCHEMA_VERSION = 1

# 피드백 주제 — 기각 사유·버전 요약을 묶는 낱말 (늘릴 때는 여기만)
THEMES = {
    "motion": ("움직임·카메라", ["움직", "카메라", "정적", "멈춰", "확대", "동적", "정신없", "전환", "tilt", "dolly", "슬라이드"]),
    "sound": ("소리·배경음", ["배경음", "효과음", "타격음", "소리", "음질", "웅웅"]),
    "background": ("배경·바탕색", ["배경", "바탕"]),
    "emphasis": ("강조·자막", ["강조", "자막", "키네틱"]),
    "variety": ("스타일 조합·반복", ["스타일", "반복", "패턴", "지도", "단조", "난잡"]),
    "script": ("대본·말투·형식", ["대본", "말투", "오프닝", "진행", "인트로", "끝맺음", "형식"]),
    "depth": ("주제·분석 깊이", ["뻔", "분석", "이슈", "보고서", "사건", "심도", "엮"]),
    "intent": ("의도·시청자", ["의도", "욕망", "시청자", "목표", "유입", "니즈"]),
    "length": ("길이·운영", ["분량", "10분", "운영", "일정", "요일"]),
}

FILE_KEYS = {"README": "README.md"}


def _file_key(p: Path) -> str:
    return "README" if p.stem == "README" else p.stem.split("-")[0]


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.exists() else ""


def _themes(text: str) -> list[str]:
    out = []
    for k, (_, words) in THEMES.items():
        t = text.replace("배경음", "") if k == "background" else text   # '배경음'은 소리 주제
        if any(w in t for w in words):
            out.append(k)
    return out


# ------------------------------------------------------------------ 문서·절
SEC_NUM = re.compile(r"^(G\d|\d+(?:-\d+)*)\.?\s")


def parse_docs() -> tuple[list[dict], list[dict]]:
    docs, secs = [], []
    for p in sorted(MANUAL.glob("*.md")):
        if p.name in ("CHANGELOG.md", "reviews.md", "audit.md"):   # 기록·보고서는 매뉴얼 본문이 아님
            continue
        key = _file_key(p)
        lines = _read(p).splitlines()
        title = next((l.lstrip("# ").strip() for l in lines if l.startswith("# ")), p.stem)
        docs.append({"id": f"doc:{key}", "kind": "doc", "key": key, "file": f"manual/{p.name}", "label": title,
                     "lines": len(lines)})
        heads = [(i, l) for i, l in enumerate(lines) if re.match(r"^#{2,3} ", l)]
        for n, (i, l) in enumerate(heads):
            end = heads[n + 1][0] if n + 1 < len(heads) else len(lines)
            level = len(l) - len(l.lstrip("#"))
            t = l.lstrip("# ").strip()
            m = SEC_NUM.match(t)
            num = m.group(1) if m else f"h{i + 1}"
            vm = re.search(r"\(v(\d+)\b", t)
            short = SEC_NUM.sub("", t, count=1).strip() if m else t
            sid = f"sec:{key}§{num}"
            if any(s["id"] == sid for s in secs):
                sid = f"{sid}@{i + 1}"
            secs.append({"id": sid, "kind": "section", "doc": f"doc:{key}", "num": num, "level": level,
                         "label": re.sub(r"\s*\(v\d+.*$", "", short), "title": t, "line": i + 1,
                         "end": end, "tag_version": int(vm.group(1)) if vm else None,
                         "body": "\n".join(lines[i + 1:end]).strip()[:4000]})
    return docs, secs


# ------------------------------------------------------------------ 단계·게이트·규칙·검사
def parse_pipeline() -> tuple[list[dict], list[dict]]:
    steps, gates = [], {}
    for l in _read(MANUAL / "README.md").splitlines():
        m = re.match(r"\|\s*(\d)\.\s*([^|]+)\|([^|]+)\|([^|]+)\|\s*(G\d)\s*([^|]*)\|", l)
        if m:
            steps.append({"id": f"step:{m.group(1)}", "kind": "step", "n": int(m.group(1)), "label": m.group(2).strip(),
                          "does": m.group(3).strip(), "outputs": m.group(4).strip().replace("`", ""),
                          "gate": f"gate:{m.group(5)}"})
            gates[m.group(5)] = m.group(6).strip()
    gl = [{"id": "gate:G0", "kind": "gate", "key": "G0", "label": "기각 반영", "section": None}]
    gl += [{"id": f"gate:{k}", "kind": "gate", "key": k, "label": v, "section": f"sec:06§{k}"} for k, v in sorted(gates.items())]
    return steps, gl


def parse_rules() -> list[dict]:
    rules, gate = [], None
    for i, l in enumerate(_read(MANUAL / "06-checklist.md").splitlines()):
        m = re.match(r"^## (G\d)", l)
        if m:
            gate = m.group(1)
            continue
        if l.startswith("## "):
            gate = None
        m = re.match(r"^\|\s*(MUST|SHOULD|EYE)([^|]*)\|([^|]+)\|([^|]*)\|", l)
        if gate and m:
            auto = m.group(4).strip()
            rules.append({"id": f"rule:{gate}:{len([r for r in rules if r['gate'] == gate]) + 1}", "kind": "rule",
                          "gate": f"gate:{gate}", "level": m.group(1), "level_note": m.group(2).strip(),
                          "label": m.group(3).strip(), "auto": "✅" in auto, "eye": "EYE" in auto or m.group(1) == "EYE",
                          "line": i + 1})
    return rules


def parse_checks() -> list[dict]:
    """ytflow/stages/checklist.py 의 R.add(...) — 규칙을 실제로 재는 코드."""
    src = _read(ROOT / "ytflow" / "stages" / "checklist.py").splitlines()
    out = []
    for i, l in enumerate(src):
        m = re.search(r"R\.add\(\s*(?:f?\"(G\d)\"|(\w+))\s*,\s*(?:\"(MUST|SHOULD)\"|(\w[\w\s\"'=<>!.()-]*?))\s*,\s*f?\"([^\"]+)\"", l)
        if not m:
            continue
        gate = m.group(1) or "G?"
        level = m.group(3) or "MUST/SHOULD"
        out.append({"id": f"check:{i + 1}", "kind": "check", "gate": f"gate:{gate}", "level": level,
                    "label": m.group(5), "file": "ytflow/stages/checklist.py", "line": i + 1})
    return out


# ------------------------------------------------------------------ 버전·검토
REF_FILE = re.compile(r"(?:manual/)?(README|0[1-9])(?:-[a-z-]+(?:\.md)?)?\s*((?:§\s*[\d-]+\s*(?:[·,]\s*)?)+)")


def _refs(text: str) -> list[str]:
    out = []
    for m in REF_FILE.finditer(text):
        for n in re.findall(r"§\s*([\d-]+)", m.group(2)):
            out.append(f"{m.group(1)}§{n.strip('-')}")
    for m in re.finditer(r"(?:manual/)?(0[1-9])-[a-z-]+(?:\.md)?", text):
        out.append(m.group(1))
    out += [f"gate:{g}" for g in re.findall(r"\b(G[0-8])\b", text)]
    return list(dict.fromkeys(out))


def parse_changelog() -> tuple[list[dict], list[str]]:
    s = _read(MANUAL / "CHANGELOG.md")
    pend = []
    m = re.search(r"## 반영 대기\n(.*?)(?=\n## |\Z)", s, re.S)
    if m:
        pend = [l[2:].strip() for l in m.group(1).splitlines() if l.startswith("- ")]
    versions = []
    for m in re.finditer(r"^## v(\d+) — (\S+)\n(.*?)(?=^## |\Z)", s, re.S | re.M):
        summary, applied = [], []
        for l in m.group(3).splitlines():
            a = re.match(r"^\s+- 반영:\s*\[(\S+) · (\S+) 기각\]\s*(.*)", l)
            if a:
                applied.append({"date": a.group(1), "project": a.group(2), "reason": a.group(3).strip()})
            elif l.startswith("- "):
                summary.append(l[2:].strip())
        v = int(m.group(1))
        text = " ".join(summary)
        versions.append({"id": f"ver:{v}", "kind": "version", "v": v, "date": m.group(2), "label": f"v{v}",
                         "summary": text, "applied": applied, "themes": _themes(text + " ".join(a["reason"] for a in applied))})
    versions.sort(key=lambda x: x["v"])
    return versions, pend


def parse_reviews() -> list[dict]:
    out = []
    for l in _read(MANUAL / "reviews.md").splitlines():
        m = re.match(r"^\|\s*(\d{4}-\d\d-\d\d)\s*\|\s*([^|]+?)\s*\|\s*v(\d+)\s*\|\s*(통과|기각)\s*\|\s*(.*?)\s*\|$", l)
        if m:
            out.append({"id": f"rev:{len(out) + 1}", "kind": "review", "date": m.group(1), "project": m.group(2),
                        "manual_version": int(m.group(3)), "result": "pass" if m.group(4) == "통과" else "reject",
                        "reason": m.group(5), "themes": _themes(m.group(5))})
    return out


def git_versions() -> dict[int, dict]:
    """manual/VERSION 을 바꾼 커밋마다 그 버전과 함께 바뀐 manual 파일 (얕은 클론이면 있는 만큼만)."""
    out: dict[int, dict] = {}
    try:
        log = subprocess.run(["git", "log", "--format=%H\t%ad\t%s", "--date=short", "--", "manual/VERSION"],
                             cwd=ROOT, capture_output=True, text=True, timeout=30).stdout
    except Exception:
        return out
    for line in log.splitlines():
        sha, date, subj = line.split("\t", 2)
        try:
            v = int(subprocess.run(["git", "show", f"{sha}:manual/VERSION"], cwd=ROOT, capture_output=True,
                                   text=True, timeout=10).stdout.strip())
            files = subprocess.run(["git", "show", "--name-only", "--format=", sha], cwd=ROOT, capture_output=True,
                                   text=True, timeout=10).stdout.split()
            if subprocess.run(["git", "rev-parse", "-q", "--verify", f"{sha}^"], cwd=ROOT, capture_output=True,
                              timeout=10).returncode != 0:
                files = []   # 얕은 클론의 첫 커밋은 모든 파일을 '추가'로 보여 줘서 쓰지 않음
        except Exception:
            continue
        if v not in out:
            out[v] = {"sha": sha, "date": date, "subject": subj,
                      "files": [f for f in files if f.startswith("manual/") and f.endswith(".md")
                                and not f.endswith(("CHANGELOG.md", "reviews.md"))],
                      "other_files": [f for f in files if not f.startswith("manual/")][:40]}
    return out



# ------------------------------------------------------------------ 규칙의 네 층: 영구 원칙 · 작업 기준 · 스타일 기본값 · 실험 기록
TIERS_FILE = MANUAL / "rule_tiers.yaml"
TIER = {
    "principle": "영구 원칙",      # 사실·법·권리·안전 — 어떤 지시가 와도. 진짜 금지, MUST
    "standard": "작업 기준",       # 품질을 위한 제작 방법 — 버전으로 바뀔 수 있음. MUST·SHOULD
    "style": "스타일 기본값",      # 소리·카메라·바탕·스타일 비율 — 금지가 아니라 켜고 끄는 기본값. SHOULD 까지
    "trial": "실험 기록",          # 한 영상·한 시도의 반응 — 다음 시도의 참고, 금지·MUST 로 만들지 않음
}
PRINCIPLE_W = ["투자 권유", "권유", "사세요", "매수", "라이선스", "저작권", "우회", "봇 확인", "API 키", "사적 인물", "사생활", "실명",
               "비하", "범인", "단정 금지어", "유사투자", "복제", "확인 안 된", "확인 실패", "소문", "CC BY-SA", "라이선스 불명", "퍼블릭 도메인",
               "조롱", "편을 들지", "의혹", "커밋", "로고", "제휴", "목표가", "합성이면"]
STYLE_W = ["효과음", "배경음", "타격음", "카메라", "확대", "축소", "바탕", "배경색", "스타일", "3연속", "연속 금지", "type", "강조",
           "키네틱", "전환", "fx", "tilt", "dolly", "NASA", "움직임", "정지 화면", "정지 비율", "화면 변화", "장 표지", "막대 인물",
           "photofill", "words", "곡이", "스킨", "그래픽 팩", "40%", "3종", "4종", "겹친 장면", "plain 장면", "글씨·도형", "콜라주", "boil"]


def _tkey(prefix: str, text: str) -> str:
    import hashlib
    return f"{prefix}:" + hashlib.sha1(_norm(text).encode("utf-8")).hexdigest()[:8]


def load_tiers() -> dict:
    try:
        import yaml
        return (yaml.safe_load(_read(TIERS_FILE)) or {}).get("tiers", {}) or {}
    except Exception:
        return {}


def save_tier(key: str, tier: str, note: str = "", by: str = "사용자", text: str = "") -> None:
    import yaml
    if tier not in TIER and tier != "auto":
        raise ValueError("알 수 없는 층")
    doc = (yaml.safe_load(_read(TIERS_FILE)) or {}) if TIERS_FILE.exists() else {}
    doc.setdefault("tiers", {})
    if tier == "auto":
        doc["tiers"].pop(key, None)
    else:
        doc["tiers"][key] = {k: v for k, v in {"tier": tier, "note": note, "by": by, "text": text[:120],
                                                 "date": dt.date.today().isoformat()}.items() if v}
    head = ("# 규칙의 네 층 — 사람이 확정한 분류 (자동 추정을 덮어씀). manual-ui '한눈에 → 규칙의 층'에서 고칩니다. (docs/31 §9, manual/README §3-1)\n"
            "# principle 영구 원칙(사실·법·권리·안전, 진짜 금지) · standard 작업 기준(품질 방법, 버전으로 바뀜)\n"
            "# style 스타일 기본값(소리·카메라·바탕·비율 — 금지 아님, 켜고 끔) · trial 실험 기록(한 영상의 반응 — 금지·MUST 로 만들지 않음)\n"
            "# key 는 그 줄 글자에서 자동으로 만들어짐 — 글자를 고치면 key 가 바뀌어 자동 추정으로 돌아갑니다 (text 는 알아보기용).\n")
    TIERS_FILE.write_text(head + yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, width=110), encoding="utf-8")


def classify(text: str, absolute: bool = False, vers_applied: dict | None = None, hard: bool | None = None) -> dict:
    """자동 추정: 어느 층인가 + 과적합 후보인가 (스타일 층인데 금지·MUST, 근거가 영상 한 편의 반응)."""
    t = text or ""
    vs = [int(v) for v in re.findall(r"\bv(\d{1,2})\b", t)]
    projects = set()
    for v in vs:
        projects |= set((vers_applied or {}).get(v, []))
    single = bool(vs) and len(projects) == 1 or ("사용자" in t and len(projects) <= 1 and re.search(r"\d{4}-\d\d-\d\d", t))
    hardness = hard if hard is not None else ("MUST" in t or any(w in t for w in ["금지", "쓰지 않", "하지 않", "끈다", "아예 뺌"]))
    if absolute or any(w in t for w in PRINCIPLE_W):
        return {"tier": "principle", "why": "사실·법·권리·안전에 관한 말" if not absolute else "README §3 절대 하지 않는 것", "overfit": False,
                "single": bool(single)}
    if any(w in t for w in STYLE_W):
        of = bool(hardness and single)
        return {"tier": "trial" if of else "style",
                "why": ("스타일 말인데 영상 한 편의 반응에서 금지·MUST 가 됨" if of else "소리·카메라·바탕·스타일 비율에 관한 말 — 기본값"),
                "overfit": bool(hardness), "single": bool(single)}
    return {"tier": "standard", "why": "제작 방법·품질 기준", "overfit": False, "single": bool(single)}


def apply_tier(item: dict, key: str, text: str, ov: dict, **kw) -> None:
    c = classify(text, **kw)
    o = ov.get(key)
    item.update(tier_key=key, tier_auto=c["tier"], why=c["why"], overfit=c["overfit"], single=c["single"])
    if o:
        item.update(tier=o.get("tier", c["tier"]), tier_by=o.get("by", "사용자"), tier_note=o.get("note", ""), tier_fixed=True)
    else:
        item.update(tier=c["tier"], tier_by="자동 추정", tier_note="", tier_fixed=False)
    item["tier_label"] = TIER.get(item["tier"], item["tier"])
    # 과적합 후보: 스타일·실험 층인데 금지·MUST 로 적혀 있음 (사람이 원칙·기준으로 확정했으면 아님)
    # 사람이 스타일로 확정했으면 후보에서 뺌 (실험으로 확정됐는데 금지·MUST 로 적혀 있으면 계속 후보)
    item["overfit"] = c["overfit"] and (item["tier"] == "trial" or (item["tier"] == "style" and not item["tier_fixed"]))


# ------------------------------------------------------------------ 사용자 피드백 기록 (영상 검토가 아닌 말도)
FEEDBACK = MANUAL / "feedback.yaml"
FB_KIND = {"review": "영상 검토", "direction": "방향·기준 요청", "clarify": "뜻 바로잡기", "tool": "도구 요청"}


def parse_feedback() -> list[dict]:
    try:
        import yaml
        items = (yaml.safe_load(_read(FEEDBACK)) or {}).get("feedback", []) or []
    except Exception:
        return []
    out = []
    for i, f in enumerate(items):
        q = str(f.get("quote", "")).strip()
        if not q:
            continue
        out.append({"id": f"fb:{i + 1}", "kind": "feedback", "date": str(f.get("date", "")), "quote": q, "label": q[:60],
                    "fb_kind": f.get("kind", "direction"), "fb_kind_label": FB_KIND.get(f.get("kind", "direction"), f.get("kind", "")),
                    "project": f.get("project", "") or "", "about": str(f.get("about", "") or ""), "note": f.get("note", "") or "",
                    "pending": bool(f.get("pending")), "themes": _themes(q), "scope": f.get("scope", "")})
    return out


def add_feedback(quote: str, kind: str = "direction", project: str = "", about: str = "", note: str = "",
                 pending: bool = False, scope: str = "") -> dict:
    """사용자가 한 말을 그대로 기록 → (선택) 반영 대기 → 그래프 다시 만들기."""
    import yaml
    doc = (yaml.safe_load(_read(FEEDBACK)) or {}) if FEEDBACK.exists() else {}
    doc.setdefault("feedback", [])
    item = {"date": dt.date.today().isoformat(), "kind": kind, "quote": quote.strip()}
    if project:
        item["project"] = project
    if about:
        item["about"] = about.replace("intent:", "")
    if note:
        item["note"] = note
    if pending:
        item["pending"] = True
    if scope:
        if scope not in TIER:
            raise ValueError("scope 는 principle·standard·style·trial 중 하나")
        item["scope"] = scope
    doc["feedback"].append(item)
    head = ("# 사용자 피드백 기록 — 영상 검토(reviews.md) 밖에서 한 말도 원문 그대로 남깁니다. 그래프의 '사용자 원문'이 됩니다.\n"
            "# python -m ytflow feedback \"원문\" [--kind direction|clarify|tool|review] [--project P] [--about 의도ID] [--pending]\n"
            "# kind: direction 방향·기준 요청 · clarify 뜻 바로잡기(모델 해석이 틀렸을 때) · tool 도구 요청 · review 영상에 대한 말\n"
            "# about: 이 말이 바로잡는 의도 ID (manual-ui '의도 정렬'의 intent:xxxx 에서 xxxx) · pending: 매뉴얼 '반영 대기'에도 넣음\n"
            "# scope: 이 말이 어느 층인가 — principle 영구 원칙 · standard 작업 기준 · style 스타일 기본값 · trial 실험 기록(금지로 만들지 않음)\n")
    FEEDBACK.write_text(head + yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, width=110), encoding="utf-8")
    if pending:
        cl = MANUAL / "CHANGELOG.md"
        line = f"- [{item['date']} · 사용자 피드백{' · ' + project if project else ''}{' · 층: ' + TIER[scope] if scope else ''}] {quote.strip()}"
        cl.write_text(_read(cl).replace("## 반영 대기\n", f"## 반영 대기\n{line}\n", 1), encoding="utf-8")
    write()
    return item


def source_hash() -> str:
    """그래프를 만드는 원본(매뉴얼·검토·피드백·판정·용어·레시피·스킨)의 지문 — 그래프가 옛것인지 확인용."""
    import hashlib
    h = hashlib.sha1()
    files = sorted([*MANUAL.glob("*.md"), *MANUAL.glob("*.yaml"), MANUAL / "VERSION",
                    *(ROOT / "styles" / "recipes").glob("*.yaml"), *(ROOT / "skins").glob("*/skin.yaml"), TECHNIQUES,
                    *(ROOT / "topics").glob("*/topic.yaml")])
    for f in files:
        if f.name in ("audit.md", "10-when-to-use.md"):   # 검토 보고서·용도표(생성물)는 그래프 원본이 아님
            continue
        if f.exists():
            h.update(f.name.encode()); h.update(f.read_bytes())
    return h.hexdigest()[:12]


def is_stale() -> bool:
    try:
        g = json.loads(_read(MANUAL / "graph.json"))
    except Exception:
        return True
    return g.get("source_hash") != source_hash()


# ------------------------------------------------------------------ 의도 정렬: 사용자 원문 → 모델 해석 → 규칙 → 코드 → 결과
INTENTS = MANUAL / "intents.yaml"
STATUS = {"aligned": "정렬됨", "over": "과잉 해석", "under": "덜 반영", "drift": "다른 뜻으로", "conflict": "다른 규칙과 충돌",
          "unreviewed": "미검토"}
QUOTE = re.compile(r"[\"“]([^\"”]{6,300})[\"”]")


def _norm(t: str) -> str:
    return re.sub(r"[\s\W_]+", "", t)


def _iid(t: str) -> str:
    import hashlib
    return "intent:" + hashlib.sha1(_norm(t).encode("utf-8")).hexdigest()[:8]


def _user_quotes(line: str) -> list[tuple[str, int | None, str | None]]:
    """한 줄에서 '사용자' 뒤에 오는 따옴표 원문들 → [(원문, 버전, 날짜)]."""
    k = line.find("사용자")
    if k < 0:
        return []
    head = line[:k + 40]
    vm = re.findall(r"\bv(\d+)\b", line[:k + 20])
    dm = re.search(r"\d{4}-\d\d-\d\d", line)
    return [(q.group(1).strip(), int(vm[-1]) if vm else None, dm.group(0) if dm else None)
            for q in QUOTE.finditer(line, k)]


def parse_code() -> list[dict]:
    """ytflow/**/*.py 의 '# vN …' 주석 — 버전이 실제로 구현된 곳."""
    out = []
    for p in sorted((ROOT / "ytflow").rglob("*.py")):
        rel = p.relative_to(ROOT).as_posix()
        for i, l in enumerate(_read(p).splitlines()):
            c = l.find("#")
            doc = l.strip().startswith('"""')
            if c < 0 and not doc:
                continue
            txt = l[c + 1:].strip() if c >= 0 else l.strip().strip('"')
            vs = sorted({int(v) for v in re.findall(r"\bv(\d{1,2})\b", txt) if 1 <= int(v) <= 99})
            if vs:
                out.append({"id": f"code:{rel}:{i + 1}", "kind": "code", "file": rel, "line": i + 1, "versions": vs,
                            "label": txt[:160], "src": l.strip()[:220]})
    return out


def load_annotations() -> dict:
    try:
        import yaml
        return (yaml.safe_load(_read(INTENTS)) or {}).get("intents", {}) or {}
    except Exception:
        return {}


def save_annotation(iid: str, data: dict) -> None:
    """intents.yaml 의 한 의도만 바꿔 씀 (사람이 고치는 원본)."""
    import yaml
    doc = {}
    if INTENTS.exists():
        doc = yaml.safe_load(_read(INTENTS)) or {}
    doc.setdefault("intents", {})
    key = iid.replace("intent:", "")
    cur = doc["intents"].get(key, {}) or {}
    for k in ("quote", "meaning", "not_meant", "note"):
        if k in data:
            cur[k] = data[k]
    if "readings" in data:
        rd = cur.get("readings", {}) or {}
        for ref, v in data["readings"].items():
            if not v or v.get("status", "unreviewed") == "unreviewed" and not v.get("note"):
                rd.pop(ref, None)
            else:
                rd[ref] = {k2: v[k2] for k2 in ("status", "note", "by") if v.get(k2)}
        cur["readings"] = rd
    cur["updated"] = dt.date.today().isoformat()
    doc["intents"][key] = cur
    head = ("# 의도 정렬 — 사용자가 말한 뜻(원문)과 모델이 매뉴얼·코드로 옮긴 해석이 맞는지 사람이 판정해 둔 곳.\n"
            "# 의도 ID 는 원문에서 자동으로 만들어짐 (python -m ytflow manual-graph). 이 파일은 manual-ui '의도 정렬' 탭에서 고칩니다.\n"
            "# status: aligned 정렬됨 · over 과잉 해석 · under 덜 반영 · drift 다른 뜻으로 · conflict 다른 규칙과 충돌 · unreviewed 미검토\n")
    INTENTS.write_text(head + yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, width=110), encoding="utf-8")


POLAR_THEMES = ("motion", "sound", "background", "emphasis", "variety")
PLUS = ["계속 움직", "끊임없", "완전히 멈춘 순간이 없", "멈춘 화면 없", "다가간다", "밀고 들어", "숨 쉰다", "반드시", "켠다"]
MINUS = ["끈다", "기본 끔", "쓰지 않", "고정이 기본", "억지로", "흔들지 않", "덜'이 기본", "낮춥니다", "카메라를 흔들어"]


def polarity_lines(secs: list[dict]) -> list[dict]:
    """지금 매뉴얼에서 같은 주제를 '더 하라'·'덜 하라'로 말하는 줄 (충돌 후보, 자동 추정)."""
    out = []
    for s in secs:
        body = s.get("body", "")
        if "규칙의 네 층" in s.get("title", "") or "기록용 — 지금 기본값이 아닙니다" in body or s["doc"] == "doc:10":   # 설명·기록용·용도표는 규칙 줄이 아님
            continue
        for ln in body.splitlines():
            if ln.lstrip().startswith(">"):   # 인용(사용자 원문·옛 기준)은 규칙 줄이 아님
                continue
            th = _themes(ln)
            if not th:
                continue
            pol = "+" if any(w in ln for w in PLUS) else "-" if any(w in ln for w in MINUS) else None
            if pol:
                for t in [x for x in th if x in POLAR_THEMES]:   # 더 하라/덜 하라 비교는 스타일 주제에만 의미가 있음
                    out.append({"section": s["id"], "theme": t, "pol": pol, "text": ln.strip()[:200]})
    return out


# ------------------------------------------------------------------ 용어 층: '그래서 저게 뭐야?' — 스타일·장면 종류·효과·그래픽 팩·움직임 용어
GLOSSARY = MANUAL / "glossary.yaml"
TECHNIQUES = ROOT / "styles" / "techniques.yaml"
USAGE = MANUAL / "usage.yaml"
TECH_STATUS = {"have": "이미 있음", "partial": "비슷한 것 있음", "candidate": "후보 (아직 없음)", "hold": "보류"}
CAT_LABEL = {"technique": "연출 기법", "style": "편집 스타일", "scene": "장면 종류", "fx": "시각 효과", "skin": "그래픽 팩", "motion": "움직임", "measure": "측정값"}
ANIM_BY_KEY = {"kb": "kenburns", "zoomshot": "zoomshot", "kinetic": "kinetic", "stage": "walk", "story": "draw", "journey": "draw",
               "tilt": "tilt", "dolly": "push", "scan": "scan", "dust": "dust", "leak": "leak", "terminal": "kinetic",
               "chat": "kinetic", "bignum": "beat-motion", "map_causal": "draw", "chapter": "crossfade", "illust": "push",
               "metaphor": "walk", "bite": "cut", "footage": "kenburns", "newsdesk": "layers", "recap": "layers", "isotype": "beat-motion"}


def _code_ref(spec: str) -> dict | None:
    """'파일::그 줄의 글자' → 지금 줄 번호."""
    f, _, needle = spec.partition("::")
    lines = _read(ROOT / f).splitlines()
    for i, l in enumerate(lines):
        if not needle or needle in l:
            return {"file": f, "line": i + 1, "src": l.strip()[:220]}
    return {"file": f, "line": None, "src": "(그 글자를 찾지 못함 — 코드가 바뀌었을 수 있음)"}


def parse_lexicon() -> list[dict]:
    import yaml
    terms: dict[str, dict] = {}

    def T(key, **kw):
        t = terms.setdefault(key, {"id": f"term:{key}", "kind": "term", "key": key, "aliases": [], "code": [],
                                   "scenes": [], "used_by": []})
        for k, v in kw.items():
            if v not in (None, "", []):
                t[k] = v
        return t

    # 장면 종류: 렌더 함수 표 (hybrid.RENDER 와 각 모듈의 등록)
    defs: dict[str, dict] = {}
    for py in sorted((ROOT / "ytflow" / "stages").glob("*.py")):
        rel = py.relative_to(ROOT).as_posix()
        lines = _read(py).splitlines()
        for i, l in enumerate(lines):
            m = re.match(r"\s*def (s_\w+)\(", l)
            if m:
                doc = ""
                if i + 1 < len(lines) and '"""' in lines[i + 1]:
                    doc = lines[i + 1].strip().strip('"').strip()
                defs.setdefault(m.group(1), {"file": rel, "line": i + 1, "src": l.strip(), "doc": doc})
        txt = "\n".join(lines)
        for m in re.finditer(r"\"(\w+)\"\s*:\s*(s_\w+)", txt):
            if m.group(2) in defs or True:
                T(m.group(1), _fn=m.group(2))
        for m in re.finditer(r"RENDER\[\"(\w+)\"\]\s*=\s*(s_\w+)", txt):
            T(m.group(1), _fn=m.group(2))
    for k, t in list(terms.items()):
        fn = t.pop("_fn", None)
        d = defs.get(fn)
        if not d:
            terms.pop(k)
            continue
        t.update(name=k, cat="scene", plain=d["doc"] or f"장면 종류 {k}", aliases=[k],
                 code=[{"file": d["file"], "line": d["line"], "src": d["src"]}],
                 how=f"렌더 함수 {fn}() 가 이 장면을 그림 ({d['file']})", enable=f"hybrid.json 장면의 \"type\": \"{k}\"",
                 anim=ANIM_BY_KEY.get(k))

    # 시각 효과 fx
    dsrc = _read(ROOT / "ytflow" / "stages" / "directions.py")
    fxm = re.search(r"^FX = \{(.*?)^\}", dsrc, re.S | re.M)
    if fxm:
        base = dsrc[:fxm.start()].count("\n")
        for j, l in enumerate(fxm.group(1).splitlines()):
            m = re.match(r"\s*\"(\w+)\":\s*\"([^\"]+)\"", l)
            if m:
                T(f"fx-{m.group(1)}", name=f"{m.group(1)} (시각 효과)", cat="fx", plain=m.group(2), aliases=[m.group(1)],
                  how="장면 그림 위에 효과를 덧붙이는 함수 apply_fx 가 처리", enable=f"hybrid.json 장면의 \"fx\": [\"{m.group(1)}\"]",
                  code=[{"file": "ytflow/stages/directions.py", "line": base + j + 2, "src": l.strip()[:200]},
                        _code_ref("ytflow/stages/directions.py::def apply_fx")], anim=ANIM_BY_KEY.get(m.group(1)))

    # 그래픽 팩 skins
    for sk in sorted((ROOT / "skins").glob("*/skin.yaml")):
        raw = _read(sk)
        first = next((l.lstrip("# ").strip() for l in raw.splitlines() if l.startswith("#")), "")
        try:
            y = yaml.safe_load(raw) or {}
        except Exception:
            y = {}
        k = sk.parent.name
        T(f"skin-{k}", name=f"{y.get('title', k)} ({k})", cat="skin", plain=first or y.get("title", k), aliases=[k],
          how=f"색·글꼴·배경 토큰 묶음 skins/{k}/skin.yaml — 연출은 그대로, 겉모습만 바뀜",
          enable=f"edit.yaml 의 skin: {k}, 또는 장면의 look", code=[{"file": f"skins/{k}/skin.yaml", "line": 1, "src": first[:200]}],
          anim="layers")

    # 편집 스타일 (레시피)
    for rp in sorted((ROOT / "styles" / "recipes").glob("*.yaml")):
        if rp.name.startswith("_"):
            continue
        try:
            y = yaml.safe_load(_read(rp)) or {}
        except Exception:
            continue
        k = y.get("id", rp.stem)
        name = str(y.get("name", k))
        short = re.split(r"\s*[(（]", name)[0].strip()
        sty = ROOT / "styles" / k / "STYLE.md"
        intro = ""
        if sty.exists():
            for l in _read(sty).splitlines()[1:]:
                l2 = l.strip().lstrip(">").strip()
                if l2 and not l2.startswith("#"):
                    intro = l2[:300]
                    break
        scenes = list(dict.fromkeys((y.get("scene_types") or []) + (y.get("owns") or [])))
        fits = y.get("fits") or {}
        T(f"style-{k}", name=name, short=short, cat="style", plain=y.get("when") or intro or name,
          look=name, status=y.get("status", ""), renderer=y.get("renderer", ""), skin=y.get("skin", ""),
          aliases=[k, short] if len(short) >= 4 else [k], scenes=scenes, avoid=y.get("avoid", ""),
          fits=", ".join(f"{a}: {'·'.join(map(str, b))}" for a, b in fits.items() if b), demo=y.get("demo", ""),
          skill=y.get("skill", ""), doc=f"styles/{k}/STYLE.md" if sty.exists() else "", intro=intro,
          how=f"렌더러 {y.get('renderer', '?')} · 장면 종류 {', '.join(scenes) or '-'} · 그래픽 팩 {y.get('skin', '-')}",
          enable=f"style-pick 이 추천하거나 hybrid.json 장면의 \"recipe\": \"{k}\"",
          code=[{"file": f"styles/recipes/{rp.name}", "line": 1, "src": name[:200]}],
          anim=next((ANIM_BY_KEY[s2] for s2 in scenes if s2 in ANIM_BY_KEY), None))
        for s2 in scenes:
            if s2 in terms:
                terms[s2]["used_by"].append(f"term:style-{k}")

    # 연출 기법 카탈로그 (styles/techniques.yaml, docs/32) — 스타일보다 작은 화면 문법, 모두 '스타일 기본값' 층
    try:
        tq = (yaml.safe_load(_read(TECHNIQUES)) or {}).get("techniques", {}) or {}
    except Exception:
        tq = {}
    for k, q in tq.items():
        T(f"tech-{k}", name=q.get("name", k), short=re.split(r"\s*[(（]", str(q.get("name", k)))[0].strip(), cat="technique",
          plain=q.get("plain", ""), look=q.get("look", ""), how=q.get("how", ""), caution=q.get("caution", ""),
          use_when=q.get("use_when", ""), group=q.get("group", ""), tech_status=q.get("status", "candidate"),
          tech_status_label=TECH_STATUS.get(q.get("status", "candidate"), q.get("status", "")),
          tools=q.get("tools") or [], related_keys=q.get("related") or [], anim=q.get("anim"),
          aliases=[a for a in (q.get("aliases") or []) if a], doc="styles/techniques.yaml · docs/32-technique-research.md")

    # 사람이 쓴 용어 사전 (덮어쓰기·추가)
    try:
        gl = (yaml.safe_load(_read(GLOSSARY)) or {}).get("terms", {}) or {}
    except Exception:
        gl = {}
    for k, g in gl.items():
        t = T(k)
        for f in ("name", "cat", "plain", "look", "how", "enable", "anim", "caution"):
            if g.get(f):
                t[f] = g[f]
        t["aliases"] = list(dict.fromkeys((g.get("aliases") or []) + t["aliases"]))
        if g.get("code"):
            t["code"] = [c for c in (_code_ref(x) for x in g["code"]) if c]
        t["curated"] = True
    # 용도표 (manual/usage.yaml) — 기능마다 언제 쓰나·쓰지 않나·대신 (2026-11-15 사용자 요청, manual/10)
    try:
        us = yaml.safe_load(_read(USAGE)) or {}
    except Exception:
        us = {}
    groups = us.get("groups") or {}
    for k, u in (us.get("items") or {}).items():
        t = terms.get(k) or terms.get(f"fx-{k}") or terms.get(f"skin-{k}")
        if not t:
            continue
        g_ = groups.get(u.get("group"), {})
        t.update(group=g_.get("name", u.get("group", "")), group_key=u.get("group", ""), use_when=u.get("when", ""),
                 not_when=u.get("not_when", ""), instead_keys=u.get("instead") or [], usage_situations=u.get("situations") or [],
                 does=u.get("does", ""))
        if u.get("does") and (not t.get("plain") or t["plain"].startswith("장면 종류")):
            t["plain"] = u["does"]
    for t in terms.values():   # 편집 스타일: 레시피의 fits·roles·avoid 로 '언제'
        if t.get("cat") == "style" and not t.get("use_when"):
            fits = t.get("fits", "")
            t["use_when"] = (t.get("plain") if t.get("plain") and t.get("plain") != t.get("name") and t.get("plain") != t.get("intro") else "") or \
                f"맞는 곳 — {fits}" if fits else ""
            t["not_when"] = t.get("not_when") or t.get("avoid", "")
            t["group"] = t.get("group") or "편집 스타일 (장면 묶음)"
    out = []
    for t in terms.values():
        t.setdefault("name", t["key"]); t.setdefault("cat", "scene"); t.setdefault("plain", "")
        t["label"] = t["name"]
        t["cat_label"] = CAT_LABEL.get(t["cat"], t["cat"])
        t["related"] = [f"term:{r}" for r in t.pop("related_keys", []) if r in terms]
        t["instead"] = [f"term:{r}" for r in t.pop("instead_keys", []) if r in terms]
        out.append(t)
    return out


def _alias_re(a: str):
    a = a.strip()
    if not a:
        return None
    if re.fullmatch(r"[A-Za-z0-9_\-]+", a):
        if len(a) < 2:
            return None
        return re.compile(r"(?<![\w./\-])" + re.escape(a) + r"(?![\w/\-]|\.json|\.py|\.md)")
    return re.compile(re.escape(a))


def term_matcher(terms: list[dict]):
    pats = []
    for t in terms:
        for a in t["aliases"]:
            r = _alias_re(a)
            if r:
                pats.append((t["id"], r))

    def find(text: str) -> list[str]:
        if not text:
            return []
        return list(dict.fromkeys(tid for tid, r in pats if r.search(text)))
    return find


PROHIBIT = ["금지", "쓰지 않", "하지 않", "넣지 않", "끈다", "기본 끔", "말 것", "하지 말", "않는다", "복제하지", "우회하지"]


def prohibitions(secs: list[dict]) -> list[dict]:
    """지금 매뉴얼에서 '하지 않는 것' 줄 — 절마다 (README §3 은 통째로)."""
    out, seen = [], set()
    for s in secs:
        lines = s.get("body", "").splitlines()
        if "규칙의 네 층" in s.get("title", "") or s["doc"] == "doc:10":   # 층 설명 절·용도표(생성)는 규칙 줄이 아님
            continue
        whole = s["id"] == "sec:README§3"
        for ln in lines:
            t = ln.strip()
            if not t or t.startswith("|---") or t.startswith("```") or t.startswith(">") or "10-when-to-use" in t:
                continue   # 인용(사용자 원문·옛 기준)·용도표 안내는 규칙 줄이 아님
            if whole and re.match(r"^\d+\.", t) or (not whole and any(w in t for w in PROHIBIT)):
                clean = re.sub(r"\*\*|`", "", t).strip("|- ").strip()
                k = _norm(clean)[:60]
                if k in seen:
                    continue
                seen.add(k)
                out.append({"section": s["id"], "text": clean[:260], "themes": _themes(clean), "absolute": whole,
                            "must": "MUST" in t})
    return out

# ------------------------------------------------------------------ 그래프 조립
def build() -> dict:
    docs, secs = parse_docs()
    steps, gates = parse_pipeline()
    rules, checks = parse_rules(), parse_checks()
    versions, pending = parse_changelog()
    reviews = parse_reviews()
    gitv = git_versions()
    sec_by_key = {s["id"][4:]: s for s in secs}
    doc_by_key = {d["key"]: d for d in docs}
    file_to_doc = {d["file"]: d for d in docs}
    edges: list[dict] = []

    def E(s, t, kind, **kw):
        edges.append({"s": s, "t": t, "kind": kind, **kw})

    for st in steps:
        E(st["id"], st["gate"], "gated_by")
    for s in secs:
        E(s["doc"], s["id"], "contains")
    for g in gates:
        if g["section"] and g["section"][4:] in sec_by_key:
            E(g["section"], g["id"], "defines")
    for r in rules:
        E(r["id"], r["gate"], "belongs_to")
    for c in checks:
        E(c["id"], c["gate"], "enforces")

    brands = {}
    try:
        import yaml
        brands = (yaml.safe_load(_read(ROOT / "channels" / "brands.yaml")) or {}).get("brands", {})
    except Exception:
        pass
    channels = []
    for k, b in brands.items():
        channels.append({"id": f"ch:{k}", "kind": "channel", "key": k, "label": b.get("title", k), "desire": b.get("desire", "")})
        d = file_to_doc.get(b.get("manual", ""))
        if d:
            E(f"ch:{k}", d["id"], "guided_by")
    if "09" in doc_by_key and "market" in brands:
        E("ch:market", "doc:09", "guided_by")

    def resolve(ref: str) -> str | None:
        if ref.startswith("gate:"):
            return ref if any(g["id"] == ref for g in gates) else None
        if "§" not in ref:
            return doc_by_key[ref]["id"] if ref in doc_by_key else None
        if ref in sec_by_key:
            return sec_by_key[ref]["id"]
        f, n = ref.split("§")
        cands = [s for k, s in sec_by_key.items() if k.startswith(f"{f}§{n}-") or k == f"{f}§{n}"]
        if cands:
            return cands[0]["id"]
        return doc_by_key[f]["id"] if f in doc_by_key else None

    for v in versions:
        how: dict[str, set] = {}
        for r in _refs(v["summary"]):
            t = resolve(r)
            if t:
                how.setdefault(t, set()).add("changelog")
        for s in secs:
            if s["tag_version"] == v["v"]:
                how.setdefault(s["id"], set()).add("tag")
        g = gitv.get(v["v"])
        if g:
            v["commit"] = {k: g[k] for k in ("sha", "subject", "date", "other_files")}
            for f in g["files"]:
                d = file_to_doc.get(f)
                if d and not any(t.startswith(f"sec:{d['key']}§") for t in how):
                    how.setdefault(d["id"], set()).add("git")
        for t, src in how.items():
            E(v["id"], t, "touched", via=sorted(src))

    # 검토 → 버전
    for rv in reviews:
        if rv["result"] == "pass":
            E(rv["id"], f"ver:{rv['manual_version']}", "approved_in")
            continue
        hit = None
        for v in versions:
            for a in v["applied"]:
                if a["project"] == rv["project"] and a["date"] == rv["date"] and a["reason"][:20] == rv["reason"][:20]:
                    hit = v
        if hit:
            E(rv["id"], hit["id"], "applied_in", how="changelog")
            rv["status"] = "applied"
        elif any(rv["project"] in p and rv["reason"][:20] in p for p in pending):
            rv["status"] = "pending"
        else:
            nxt = next((v for v in versions if v["v"] > rv["manual_version"]), None)
            if nxt:
                E(rv["id"], nxt["id"], "applied_in", how="inferred")
            rv["status"] = "inferred"
    for rv in reviews:
        for t in rv["themes"]:
            E(rv["id"], f"theme:{t}", "about")
    for v in versions:
        for t in v["themes"]:
            E(v["id"], f"theme:{t}", "about")
    themes = [{"id": f"theme:{k}", "kind": "theme", "key": k, "label": lab} for k, (lab, _) in THEMES.items()]

    # 절마다 손댄 버전
    touched_by: dict[str, list[int]] = {}
    for e in edges:
        if e["kind"] == "touched":
            touched_by.setdefault(e["t"], []).append(int(e["s"][4:]))
    for s in secs + docs:
        tv = sorted(set(touched_by.get(s["id"], [])))
        s["versions"] = tv
        s["last_version"] = tv[-1] if tv else None

    # ---- 코드 구현 · 사용자 원문(의도) · 정렬 판정
    codes = parse_code()
    vids = {v["v"] for v in versions}
    for c in codes:
        for vv in c["versions"]:
            if vv in vids:
                E(f"ver:{vv}", c["id"], "implemented_by")
    for c in checks:
        m2 = re.match(r"v(\d+):", c["label"])
        if m2 and int(m2.group(1)) in vids:
            E(f"ver:{m2.group(1)}", c["id"], "implemented_by")

    intents: dict[str, dict] = {}

    def add_intent(quote, ver, date, where, kind):
        if len(re.findall(r"[가-힣]", quote)) < 8:   # 사용자 말이 아닌 따옴표(코드 값·양식 글자)는 빼기
            return
        iid = _iid(quote)
        it = intents.setdefault(iid, {"id": iid, "kind": "intent", "quote": quote, "label": quote[:60], "versions": [],
                                      "date": date, "sources": []})
        if ver and ver in vids and ver not in it["versions"]:
            it["versions"].append(ver)
        if date and (not it["date"] or date < it["date"]):
            it["date"] = date
        if where not in [x["ref"] for x in it["sources"]]:
            it["sources"].append({"ref": where, "kind": kind})

    for sc in secs:
        for k, ln in enumerate([sc["title"]] + sc.get("body", "").splitlines()):
            for q, vv, d in _user_quotes(ln):
                add_intent(q, vv or sc["tag_version"], d, sc["id"], "manual")
    for rv in reviews:
        if rv["reason"]:
            av = next((int(e["t"][4:]) for e in edges if e["s"] == rv["id"] and e["kind"] == "applied_in"), None)
            add_intent(rv["reason"], av, rv["date"], rv["id"], "review")
    for c in codes:
        for q, vv, d in _user_quotes(c["src"]):
            add_intent(q, vv or (c["versions"][-1] if c["versions"] else None), d, c["id"], "code")
    fbs = parse_feedback()
    for f in fbs:
        if not f["about"]:
            add_intent(f["quote"], None, f["date"], f["id"], "feedback")

    # 같은 말을 조금씩 다르게 옮긴 원문은 한 의도로 묶음 (한쪽이 다른 쪽을 품거나 거의 같으면)
    import difflib
    groups: list[list[dict]] = []
    for it in sorted(intents.values(), key=lambda x: -len(_norm(x["quote"]))):
        a = _norm(it["quote"])
        for gr in groups:
            b = _norm(gr[0]["quote"])
            if a in b or difflib.SequenceMatcher(None, a, b).ratio() >= 0.72:
                gr.append(it)
                break
        else:
            groups.append([it])
    merged: dict[str, dict] = {}
    for gr in groups:
        head = gr[0]
        head["variants"] = [x["quote"] for x in gr[1:]]
        head["member_ids"] = [x["id"] for x in gr]
        for x in gr[1:]:
            head["versions"] = sorted(set(head["versions"]) | set(x["versions"]))
            if x["date"] and (not head["date"] or x["date"] < head["date"]):
                head["date"] = x["date"]
            head["sources"] += [s2 for s2 in x["sources"] if s2["ref"] not in [y["ref"] for y in head["sources"]]]
        merged[head["id"]] = head
    intents = merged
    for f in fbs:   # 의도를 바로잡는 말은 그 의도에 붙임
        if f["about"]:
            tgt = next((it for it in intents.values() if "intent:" + f["about"] in it["member_ids"]), None)
            if tgt:
                tgt["sources"].append({"ref": f["id"], "kind": "feedback"})
                tgt.setdefault("clarified", []).append({"date": f["date"], "quote": f["quote"], "ref": f["id"]})
                f["intent"] = tgt["id"]
            else:
                add_intent(f["quote"], None, f["date"], f["id"], "feedback")
                iid = _iid(f["quote"])
                if iid in intents:
                    intents[iid].setdefault("variants", []); intents[iid].setdefault("member_ids", [iid])
                    f["intent"] = iid
        else:
            f["intent"] = next((it["id"] for it in intents.values() if any(s2["ref"] == f["id"] for s2 in it["sources"])), None)

    ann = load_annotations()
    by_ver_targets: dict[int, list[str]] = {}
    for e in edges:
        if e["kind"] in ("touched", "implemented_by") and e["s"].startswith("ver:"):
            by_ver_targets.setdefault(int(e["s"][4:]), []).append(e["t"])
    for it in intents.values():
        it["versions"].sort()
        it["themes"] = _themes(it["quote"])
        a = next((ann[m[7:]] for m in it["member_ids"] if ann.get(m[7:])), {}) or {}
        it["ann_key"] = next((m for m in it["member_ids"] if ann.get(m[7:])), it["id"])
        it["meaning"] = a.get("meaning", "")
        it["not_meant"] = a.get("not_meant", []) or []
        it["note"] = a.get("note", "")
        refs = []
        for vv in it["versions"]:
            E(it["id"], f"ver:{vv}", "interpreted_in")
            refs.append(f"ver:{vv}")
            refs += by_ver_targets.get(vv, [])
        for src in it["sources"]:
            E(it["id"], src["ref"], "quoted_in")
            if src["kind"] in ("manual", "code"):
                refs.append(src["ref"])
        refs += [r for r in (a.get("readings") or {}) if r not in refs]
        it["readings"] = []
        for r in dict.fromkeys(refs):
            ra = (a.get("readings") or {}).get(r, {}) or {}
            it["readings"].append({"ref": r, "status": ra.get("status", "unreviewed"), "note": ra.get("note", ""),
                                   "by": ra.get("by", "")})
        bad = [x for x in it["readings"] if x["status"] in ("over", "under", "drift", "conflict")]
        it["status"] = ("misaligned" if bad else "aligned" if any(x["status"] == "aligned" for x in it["readings"])
                        else "unreviewed")
        it["annotated"] = bool(a)
        for t in it["themes"]:
            E(it["id"], f"theme:{t}", "about")
    intent_nodes = sorted(intents.values(), key=lambda x: (x["date"] or "", x["id"]))

    pol = polarity_lines(secs)
    conflicts = []
    for t in THEMES:
        plus = [p for p in pol if p["theme"] == t and p["pol"] == "+"]
        minus = [p for p in pol if p["theme"] == t and p["pol"] == "-"]
        if plus and minus:
            conflicts.append({"theme": t, "plus": plus[:8], "minus": minus[:8]})

    # ---- 용어 층: 노드마다 그 안에 나오는 스타일·장면·효과·움직임 용어
    lex = parse_lexicon()
    find = term_matcher(lex)
    tnode = {t["id"]: t for t in lex}
    mention: dict[str, list[str]] = {}
    for n in secs + versions + reviews + codes + rules + checks + intent_nodes + fbs + list(_steps_text(steps)):
        text = " ".join(str(n.get(k, "")) for k in ("title", "body", "summary", "reason", "label", "src", "quote", "does"))
        ts = find(text)
        if ts:
            n["terms"] = ts
            for tid in ts:
                mention.setdefault(tid, []).append(n["id"])
    for t in lex:
        t["mentioned_in"] = mention.get(t["id"], [])
        t["scenes"] = [f"term:{x}" for x in t.get("scenes", []) if f"term:{x}" in tnode]
    for t in lex:   # 관련 기존 용어에서 거꾸로도 잇기 (이 장면과 닮은 기법)
        for r in t.get("related", []):
            if r in tnode:
                tnode[r].setdefault("techniques", []).append(t["id"])
    # ---- 레포 층: 메인 → 주제 레포 → 상황 → 영상 (docs/33)
    from . import layers as _ly
    layer_nodes, sit_refs = [], set()
    try:
        corp = _ly.corpus()
    except Exception:
        corp = {}
    main_sits = _ly.main_situations()
    layer_nodes.append({"id": "layer:main", "kind": "layer", "label": "메인 레포 — 편집 매뉴얼", "situations": list(main_sits),
                        "techniques": len(_ly.techniques())})
    for k, v in main_sits.items():
        layer_nodes.append({"id": f"sit:main:{k}", "kind": "situation", "topic": "main", "key": k, "label": v.get("name", k),
                            "origin": "main", "scenes": v.get("scenes") or [], "techniques": v.get("techniques") or [],
                            "avoid": v.get("avoid", ""), "why": v.get("why", ""), "signals": (v.get("signals") or [])[:6]})
        E("layer:main", f"sit:main:{k}", "has")
        sit_refs |= set(v.get("scenes") or [])
    for tid in _ly.topic_ids():
        eff = _ly.resolve(tid)
        c = corp.get(tid, {"projects": [], "situations": {}})
        layer_nodes.append({"id": f"topic:{tid}", "kind": "topic", "key": tid, "label": eff["name"], "look": eff["look"],
                            "defaults": eff["defaults"], "avoid_techniques": eff["avoid_techniques"], "manual": eff["manual"],
                            "channels": eff["channels"], "added": eff["added"], "overridden": eff["overridden"], "dropped": eff["dropped"],
                            "situations": list(eff["situations"]), "projects": c["projects"]})
        E("layer:main", f"topic:{tid}", "inherits")
        for f in eff["manual"]:
            d = file_to_doc.get(f)
            if d:
                E(f"topic:{tid}", d["id"], "guided_by")
        for k, v in eff["situations"].items():
            st = c["situations"].get(k, {})
            sid = f"sit:{tid}:{k}"
            layer_nodes.append({"id": sid, "kind": "situation", "topic": tid, "key": k, "label": v.get("name", k), "origin": v["origin"],
                                "scenes": v.get("scenes") or [], "techniques": v["techniques_ok"], "blocked": v["techniques_blocked"],
                                "base_scenes": v.get("base_scenes"), "avoid": v.get("avoid", ""), "why": v.get("why", ""),
                                "signals": (v.get("signals") or [])[:6], "count": st.get("count", 0), "fit": st.get("fit", 0),
                                "examples": st.get("examples", [])})
            E(f"topic:{tid}", sid, "has")
            if v["origin"] != "add":
                E(sid, f"sit:main:{k}", "from_main")
            sit_refs |= set(v.get("scenes") or [])
        for pr in c["projects"]:
            eid = f"ep:{pr['project']}"
            layer_nodes.append({"id": eid, "kind": "episode", "topic": tid, "label": pr["project"], **pr})
            E(f"topic:{tid}", eid, "episode")
    for n in layer_nodes:
        if n["kind"] == "situation":
            for sc in n["scenes"]:
                if f"term:{sc}" in tnode:
                    E(n["id"], f"term:{sc}", "uses")
            for tq in n["techniques"]:
                if f"term:tech-{tq}" in tnode:
                    E(n["id"], f"term:tech-{tq}", "uses")
    lex = [t for t in lex if t["mentioned_in"] or t["cat"] in ("style", "motion", "measure", "fx", "technique") or t["used_by"]
           or t["key"] in sit_refs]
    bans = prohibitions(secs)
    tiers_ov = load_tiers()
    vers_applied = {v["v"]: sorted({a["project"] for a in v["applied"]}) for v in versions}
    for b in bans:
        sec = next((x for x in secs if x["id"] == b["section"]), {})
        ctx = b["text"] + (f" (v{sec['tag_version']})" if sec.get("tag_version") and "v" not in b["text"][:0] else "")
        apply_tier(b, _tkey("ban", b["text"]), ctx + " " + sec.get("title", ""), tiers_ov, absolute=b["absolute"], vers_applied=vers_applied)
    for r in rules:
        apply_tier(r, _tkey("rule", r["label"]), f"{r['level']} {r['label']}", tiers_ov, vers_applied=vers_applied,
                   hard=r["level"] == "MUST")
    for c in checks:   # 검사 코드 줄도 — 스타일 말인데 MUST 로 막는 검사가 과적합 후보
        apply_tier(c, _tkey("check", c["label"]), f"{c['level']} {c['label']}", tiers_ov, vers_applied=vers_applied,
                   hard=c["level"] == "MUST")
    for rv in reviews:
        if rv["reason"]:
            apply_tier(rv, _tkey("rev", rv["reason"]), rv["reason"], tiers_ov, vers_applied=vers_applied)
            rv["overfit"] = False
    for f in fbs:
        apply_tier(f, _tkey("fb", f["quote"]), f["quote"], tiers_ov, vers_applied=vers_applied)
        if f.get("scope") and not f.get("tier_fixed"):
            f.update(tier=f["scope"], tier_label=TIER[f["scope"]], tier_by="기록할 때 지정", tier_fixed=True)
        f["overfit"] = False

    for f in fbs:
        for t in f["themes"]:
            E(f["id"], f"theme:{t}", "about")
        if f.get("intent"):
            E(f["id"], f["intent"], "clarifies" if f["about"] else "quoted_as")
    nodes = steps + gates + channels + docs + secs + rules + checks + versions + reviews + themes + codes + intent_nodes + lex + fbs + layer_nodes
    cur = _read(MANUAL / "VERSION").strip() or "0"
    stats = {
        "manual_version": int(cur),
        "versions": len(versions), "reviews": len(reviews),
        "rejects": sum(r["result"] == "reject" for r in reviews), "passes": sum(r["result"] == "pass" for r in reviews),
        "pending": len(pending), "rules": len(rules), "checks": len(checks), "sections": len(secs),
        "must": sum(r["level"] == "MUST" for r in rules), "auto": sum(r["auto"] for r in rules),
        "intents": len(intent_nodes), "misaligned": sum(i["status"] == "misaligned" for i in intent_nodes),
        "intents_reviewed": sum(i["annotated"] for i in intent_nodes), "conflicts": len(conflicts), "code": len(codes),
        "terms": len(lex), "bans": len(bans), "feedback": len(fbs),
        "topics": sum(1 for n in layer_nodes if n["kind"] == "topic"), "episodes": sum(1 for n in layer_nodes if n["kind"] == "episode"),
        "main_situations": len(main_sits),
        "tiers": {k: sum(1 for x in bans + rules if x.get("tier") == k) for k in TIER},
        "overfit": sum(1 for x in bans + rules + checks if x.get("overfit")),
        "principle_bans": sum(1 for b in bans if b.get("tier") == "principle"),
    }
    try:   # 정기 검토 결과 (manual-audit, docs/34)
        _au = json.loads((MANUAL / "audit.json").read_text(encoding="utf-8"))
        audit_sum = {"date": _au.get("date"), "counts": _au.get("counts"), "items": _au.get("items", [])[:60],
                     "resolved": _au.get("resolved", [])[:20], "log": (_au.get("log") or [])[-10:],
                     "fixed": _au.get("fixed_by_agent", [])}
    except Exception:
        audit_sum = None
    return {"schema": SCHEMA_VERSION, "generated": dt.datetime.now().isoformat(timespec="seconds"), "source_hash": source_hash(),
            "audit": audit_sum,
            "stats": stats, "pending": pending, "status_labels": STATUS, "conflicts": conflicts, "bans": bans, "tier_labels": TIER,
            "nodes": nodes, "edges": edges}


def _steps_text(steps):
    return steps


ARTIFACT_URL = "https://claude.ai/artifact/8iBFUN2XD5j4SxtLain5uR"   # 공유 페이지 (읽기 전용) — 피드백 뒤 다시 올림 (docs/31 §8)


def usage_md() -> str:
    """manual/10-when-to-use.md — 용도표 (원본: manual/usage.yaml · styles/recipes · styles/techniques.yaml · manual/situations.yaml)."""
    import yaml
    us = yaml.safe_load(_read(USAGE)) or {}
    groups, items = us.get("groups") or {}, us.get("items") or {}
    from . import layers as _ly
    sits = _ly.main_situations()
    for tid in _ly.topic_ids():
        for k, v in ((_ly.load_topic(tid).get("situations") or {}).get("add") or {}).items():
            sits.setdefault(k, {**v, "_topic": tid})
    first = {}
    for k, v in sits.items():
        for i, sc in enumerate(v.get("scenes") or []):
            first.setdefault(sc, []).append(("1순위 " if i == 0 else "") + v.get("name", k) + (f" ({v['_topic']})" if v.get("_topic") else ""))
    L = ["# 10. 언제 무엇을 쓰나 — 기능·연출·편집법 용도표", "",
         "> 2026-11-15 사용자: \"어떤 상황에서 애니메이션을 넣고 언제 그림판을 넣는지 — 기능에 맞추어 그 기능들·연출들·편집법들이 언제 쓰이는지 먼저 정리. 이 둘만이 아니라 전체 모두.\"",
         "> **자동 생성** (`python -m ytflow manual-graph`). 고칠 곳: 장면·움직임·효과·그래픽 팩 `manual/usage.yaml` · 편집 스타일 `styles/recipes/*.yaml`(when·fits·avoid) · 연출 기법 `styles/techniques.yaml` · 상황 `manual/situations.yaml`·`topics/`.",
         "> 모두 '스타일 기본값' 층의 **고르는 기준**이지 금지·필수가 아닙니다 (README §3-1). 원칙(사실·라이선스·권리)은 따로 지킵니다.", "",
         "## 1. 애니메이션 무대(`stage`) vs 이야기 그림판(`story`)", ""]
    cs = us.get("compare_stage_story") or {}
    for key, title in (("stage", "애니메이션 무대 `stage`"), ("story", "이야기 그림판 `story`")):
        c = cs.get(key) or {}
        L += [f"### {title} — {c.get('한마디', '')}", "**쓰는 때**"] + [f"- {x}" for x in c.get("쓰는 때", [])] + \
             ["**쓰지 않는 때**"] + [f"- {x}" for x in c.get("쓰지 않는 때", [])] + [""]
    if cs.get("둘 다"):
        L += [f"**함께:** {cs['둘 다']}", ""]
    L += ["## 2. 기능별 — 장면 종류·움직임·효과·겉모습", "",
          "고르는 순서: 대본의 박자가 **하는 일**(상황) → 그 기능 묶음 → 아래 '언제'가 맞는 것 → '쓰지 않을 때'에 걸리면 '대신'.", ""]
    for gk, g in groups.items():
        rows = [(k, v) for k, v in items.items() if v.get("group") == gk]
        if not rows:
            continue
        L += [f"### {g.get('name', gk)}", f"_{g.get('why', '')}_", "", "| 기능 | 무엇 | 언제 쓰나 | 쓰지 않을 때 | 대신 | 이 기능이 나오는 상황 |", "|---|---|---|---|---|---|"]
        for k, v in rows:
            key = k.replace("fx-", "").replace("skin-", "")
            st = "; ".join(first.get(key, [])[:4])
            L.append(f"| `{key}` | {v.get('does', '')} | {v.get('when', '')} | {v.get('not_when', '')} | {', '.join(v.get('instead') or [])} | {st} |")
        L.append("")
    L += ["## 3. 편집 스타일 (장면을 묶은 레시피) — `styles/recipes`", "", "| 스타일 | 상태 | 언제 (맞는 곳) | 영상 안 자리 | 쓰지 않을 때 |", "|---|---|---|---|---|"]
    for rp in sorted((ROOT / "styles" / "recipes").glob("*.yaml")):
        if rp.name.startswith("_"):
            continue
        try:
            y = yaml.safe_load(_read(rp)) or {}
        except Exception:
            continue
        fits = y.get("fits") or {}
        when = y.get("when") or " · ".join(f"{'·'.join(map(str, v))}" for k2, v in fits.items() if v)
        L.append(f"| `{y.get('id', rp.stem)}` {str(y.get('name', ''))[:30]} | {y.get('status', '')} | {str(when)[:120]} | {', '.join(y.get('roles') or [])} | {str(y.get('avoid', ''))[:90]} |")
    L += ["", "## 4. 연출 기법 (화면 문법) — `styles/techniques.yaml`, docs/32", "", "| 기법 | 상태 | 언제 쓰나 | 주의 (내 피드백) |", "|---|---|---|---|"]
    for k, v in (yaml.safe_load(_read(TECHNIQUES)) or {}).get("techniques", {}).items():
        L.append(f"| {v.get('name', k)} | {TECH_STATUS.get(v.get('status'), '')} | {v.get('use_when', '')} | {v.get('caution', '')} |")
    L += ["", "## 5. 상황 → 기능 (메인 + 주제 레포) — `manual/situations.yaml`, `topics/`", "", "| 상황 | 1순위 → 2순위 장면 | 함께 쓸 기법 | 피할 것 |", "|---|---|---|---|"]
    for k, v in sits.items():
        L.append(f"| {v.get('name', k)}{' (' + v['_topic'] + ')' if v.get('_topic') else ''} | {' → '.join(v.get('scenes') or [])} | {', '.join(v.get('techniques') or [])} | {v.get('avoid', '')} |")
    return "\n".join(L) + "\n"


def write(html_out: str | None = None, artifact_out: str | None = None) -> Path:
    try:
        (MANUAL / "10-when-to-use.md").write_text(usage_md(), encoding="utf-8")
    except Exception as e:  # noqa: BLE001
        print(f"[manual-graph] 용도표 만들기 실패: {e}")
    g = build()
    out = MANUAL / "graph.json"
    slim = json.loads(json.dumps(g))
    for n in slim["nodes"]:
        n.pop("body", None)          # 본문은 md 가 원본 — json 에는 구조만
    out.write_text(json.dumps(slim, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    s = g["stats"]
    print(f"[manual-graph] v{s['manual_version']} · 절 {s['sections']} · 규칙 {s['rules']}(MUST {s['must']}) · 검사 코드 {s['checks']} "
          f"· 버전 {s['versions']} · 검토 {s['reviews']}(기각 {s['rejects']}) · 반영 대기 {s['pending']} → {out.relative_to(ROOT)}")
    if artifact_out:
        Path(artifact_out).write_text(page(g, standalone=True, wrap=False), encoding="utf-8")
        print(f"[manual-graph] 공유 페이지용 → {artifact_out} (Artifact 로 {ARTIFACT_URL} 에 다시 올림)")
    if html_out:
        Path(html_out).write_text(page(g, standalone=True, wrap=True), encoding="utf-8")
        print(f"[manual-graph] 보기 전용 HTML → {html_out}")
    return out


TEMPLATE = ROOT / "ytflow" / "assets" / "manual_graph.html"


def page(g: dict | None, standalone: bool, wrap: bool) -> str:
    html = _read(TEMPLATE)
    if g is not None:
        data = json.dumps(g, ensure_ascii=False).replace("</", "<\\/")
        html = html.replace("<!--DATA-->", f"<script>window.__MANUAL_GRAPH__={data};window.__STATIC__={str(standalone).lower()};</script>")
    if wrap:
        html = ('<!doctype html><html lang="ko"><head><meta charset="utf-8">'
                '<meta name="viewport" content="width=device-width,initial-scale=1"></head><body>' + html + "</body></html>")
    return html


# ------------------------------------------------------------------ 로컬 도구 서버
def serve(port: int = 8770, host: str = "127.0.0.1") -> None:
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
    from urllib.parse import parse_qs, urlparse

    from . import checklist

    def manual_file(rel: str) -> Path:
        p = (ROOT / rel).resolve()
        if p.parent != MANUAL.resolve() or p.suffix not in (".md", ".yaml"):
            raise ValueError("manual/*.md · manual/*.yaml 만 열고 고칠 수 있습니다")
        return p

    class H(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _send(self, code, body, ctype="application/json; charset=utf-8"):
            b = body.encode("utf-8") if isinstance(body, str) else body
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(b)))
            self.end_headers()
            self.wfile.write(b)

        def _json(self, obj, code=200):
            self._send(code, json.dumps(obj, ensure_ascii=False))

        def do_GET(self):
            u = urlparse(self.path)
            q = {k: v[0] for k, v in parse_qs(u.query).items()}
            try:
                if u.path in ("/", "/index.html"):
                    return self._send(200, page(None, standalone=False, wrap=True), "text/html; charset=utf-8")
                if u.path == "/api/graph":
                    return self._json(build())
                if u.path == "/api/file":
                    p = manual_file(q["path"])
                    return self._json({"path": q["path"], "text": _read(p)})
                if u.path == "/api/diff":
                    v = int(q["v"])
                    g = git_versions().get(v)
                    if not g:
                        return self._json({"error": f"v{v} 커밋을 git 기록에서 찾지 못했습니다 (얕은 클론일 수 있음)"}, 404)
                    d = subprocess.run(["git", "show", "--format=%h %s%n", g["sha"], "--", "manual/"], cwd=ROOT,
                                       capture_output=True, text=True, timeout=20).stdout
                    return self._json({"v": v, "sha": g["sha"], "diff": d[:200000]})
                if u.path == "/api/git-status":
                    s = subprocess.run(["git", "status", "--short", "--", "manual/"], cwd=ROOT, capture_output=True,
                                       text=True, timeout=10).stdout
                    return self._json({"status": s})
                self._json({"error": "없는 주소"}, 404)
            except Exception as e:  # noqa: BLE001
                self._json({"error": str(e)}, 400)

        def do_POST(self):
            u = urlparse(self.path)
            n = int(self.headers.get("Content-Length") or 0)
            try:
                body = json.loads(self.rfile.read(n) or b"{}")
                if u.path == "/api/file":
                    p = manual_file(body["path"])
                    p.write_text(body["text"].replace("\r\n", "\n"), encoding="utf-8")
                    return self._json({"ok": True, "saved": body["path"]})
                if u.path == "/api/review":
                    proj = (body.get("project") or "").strip()
                    if not proj or "/" in proj or ".." in proj:
                        raise ValueError("프로젝트 이름을 적어 주세요 (projects/ 아래 폴더 이름)")
                    passed = body.get("result") == "pass"
                    reason = (body.get("reason") or "").strip()
                    if not passed and not reason:
                        raise ValueError("기각은 이유가 있어야 매뉴얼에 반영할 수 있습니다")
                    path = ROOT / "projects" / proj
                    if passed and not path.exists():
                        raise ValueError(f"projects/{proj} 폴더가 없습니다")
                    checklist.review(path, passed, reason)
                    write()
                    return self._json({"ok": True})
                if u.path == "/api/pending":
                    cl = MANUAL / "CHANGELOG.md"
                    s = _read(cl)
                    if body.get("remove"):
                        line = f"- {body['remove']}\n"
                        if line not in s:
                            raise ValueError("그 반영 대기 항목을 찾지 못했습니다")
                        s = s.replace(line, "", 1)
                    else:
                        text = (body.get("text") or "").strip()
                        if not text:
                            raise ValueError("내용을 적어 주세요")
                        item = f"- [{dt.date.today().isoformat()} · 직접 기각] {text}"
                        s = s.replace("## 반영 대기\n", f"## 반영 대기\n{item}\n", 1)
                    cl.write_text(s, encoding="utf-8")
                    write()
                    return self._json({"ok": True})
                if u.path == "/api/bump":
                    summary = (body.get("summary") or "").strip()
                    if not summary:
                        raise ValueError("바꾼 기준 요약을 적어 주세요")
                    v = checklist.bump(summary, tag=False)
                    return self._json({"ok": True, "version": int(v),
                                       "next": f"git add manual && git commit -m \"매뉴얼 v{v}: {summary}\" && git push origin HEAD:refs/heads/manual/v{v}"})
                if u.path == "/api/intent":
                    iid = body.get("id", "")
                    if not iid.startswith("intent:"):
                        raise ValueError("의도 ID 가 없습니다")
                    for r in (body.get("readings") or {}).values():
                        if r and r.get("status", "unreviewed") not in STATUS:
                            raise ValueError("알 수 없는 상태")
                    save_annotation(iid, body)
                    write()
                    return self._json({"ok": True})
                if u.path == "/api/tier":
                    save_tier(body.get("key", ""), body.get("tier", ""), (body.get("note") or "").strip(), "사용자", body.get("text", ""))
                    write()
                    return self._json({"ok": True})
                if u.path == "/api/feedback":
                    q = (body.get("quote") or "").strip()
                    if not q:
                        raise ValueError("한 말을 적어 주세요")
                    if body.get("kind", "direction") not in FB_KIND:
                        raise ValueError("알 수 없는 종류")
                    add_feedback(q, body.get("kind", "direction"), (body.get("project") or "").strip(),
                                 (body.get("about") or "").strip(), (body.get("note") or "").strip(), bool(body.get("pending")),
                                 (body.get("scope") or "").strip())
                    return self._json({"ok": True})
                if u.path == "/api/intent-pending":
                    text = (body.get("text") or "").strip()
                    if not text:
                        raise ValueError("내용이 비었습니다")
                    cl = MANUAL / "CHANGELOG.md"
                    item = f"- [{dt.date.today().isoformat()} · 의도 정렬] {text}"
                    cl.write_text(_read(cl).replace("## 반영 대기\n", f"## 반영 대기\n{item}\n", 1), encoding="utf-8")
                    write()
                    return self._json({"ok": True})
                if u.path == "/api/rebuild":
                    write()
                    return self._json({"ok": True})
                self._json({"error": "없는 주소"}, 404)
            except Exception as e:  # noqa: BLE001
                self._json({"error": str(e)}, 400)

    srv = ThreadingHTTPServer((host, port), H)
    print(f"[manual-ui] http://{host}:{port}  (그래프 보기 · 매뉴얼 고치기 · 검토 기록 · 버전 올리기, 끝내려면 Ctrl+C)")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
