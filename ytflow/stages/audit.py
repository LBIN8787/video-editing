"""매뉴얼 정기 검토 — 사람이 시키지 않아도 같은 기준으로 매뉴얼을 잰다 (docs/34).

    python -m ytflow manual-audit            → manual/audit.md · manual/audit.json
    python -m ytflow manual-audit --quiet    → 요약 한 줄만 (정기 작업용)

찾는 것 (항목마다 fix = 판단 없이 고칠 수 있음 / ask = 사용자에게 물어야 함):
  conflict   같은 주제를 '더 하라'·'덜 하라'로 말하는 규칙이 함께 살아 있음          ask
  overfit    스타일·실험 층인데 금지·MUST 로 적힘 (사람이 층을 확정하지 않음)          ask
  pending    반영 대기(CHANGELOG)가 남아 있음                                          ask
  untiered   층(scope)을 정하지 않은 새 피드백                                          ask
  misaligned 의도 정렬에서 '어긋남'으로 판정됐는데 아직 그대로인 해석                   ask
  retired    폐지된 기준이 남은 문장 (인트로·순서 예고·고정 인사·10분 미만 롱폼 …)       fix
  ref        사라진 절(§)·파일을 가리키는 참조                                         fix
  coderef    용어 사전·의도 판정이 가리키는 코드 줄을 못 찾음                           fix
  topic      주제 레포가 없는 장면 종류·연출 기법을 가리킴                              fix
  stale      매뉴얼 그래프가 옛것                                                      fix
  contra     모순 장부(manual/contradictions.yaml)에 열린 모순 — open 은 ask, decided 는 fix
  sweep      모순 점검 차례: 지난 점검 뒤 바뀐 지침 파일(변경분) · 7일 지난 전체 점검        fix
지침 파일(AGENTS·README·skills·prompts·styles STYLE)에도 폐지된 기준·깨진 참조를 잽니다 (2026-11-20).
결과는 지난번 검토와 비교해 '새로 생김'·'해결됨'을 남깁니다.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
from pathlib import Path

from .. import config

ROOT = config.ROOT
MANUAL = ROOT / "manual"
OUT_JSON = MANUAL / "audit.json"
OUT_MD = MANUAL / "audit.md"
CONTRA = MANUAL / "contradictions.yaml"   # 모순 장부 (docs/34 §모순 관리)
SWEEP_DAYS = 7                            # 전체 모순 점검 간격

# 매뉴얼 밖의 지침 파일 — 에이전트가 따라 하는 글이라 매뉴얼과 어긋나면 모순이 됨 (2026-11-20 사용자: "모순되는 지침은 없는지 … 주기적으로")
INSTR_GLOBS = ["AGENTS.md", "README.md", "CLAUDE.md", "skills/*/SKILL.md", "prompts/*.md", "styles/*/STYLE.md",
               "styles/README.md", "channels/*/channel.yaml", "topics/*/topic.yaml", "formats/*.md"]

# 폐지된 기준 — (정규식, 왜 폐지됐나, 예외로 볼 줄의 낱말)
RETIRED = [
    (r"순서 예고", "README §2-1 v24: 순서 예고 없음", ["없", "하지 않", "않", "금지", "아님", "폐지"]),
    (r"안녕하세요", "README §2-1 v24: 인사 없음", ["없", "하지 않", "폐지", "넣지"]),
    (r"진행 멘트를 넣", "README §2-1: 진행 멘트 대신 앞 장 결론 → 다음 질문", []),
    (r"소개\s*→\s*훅|소개에서 자연스럽게", "04 §0 v23·v24: 소개 없이 첫 문장부터 훅", ["폐지"]),
    (r"주말 분석", "09 §2: 일요일 분석글은 기본에서 뺌 — 일요일은 한 주 종합(2026-11-20 사용자)", ["뺍니다", "기본에서"]),
    (r"목소리는 아직 미정|목소리 미정", "09 목소리: Teo 로 결정 (2026-11-13)", []),
    (r"\|\s*intro\b|intro \(바탕|intro 의 이어지는", "README §2-1 v24: 첫 장면은 intro 가 아니라 본론 (check G4 MUST)", ["쓰지 않", "아님", "아니라"]),
    (r"(?:지식|설명)[^|\n]{0,12}(?:≤|이하)\s*30|○ ≤30", "04 §0-6: 지식 문장 비율 기준 폐지 (2026-11-19 사용자: 너무 과적합)", ["폐지", "당시 기록"]),
    (r"카메라가 계속 움직인다|완전히 멈춘 순간이 없게", "README §2-5 v34: 카메라 고정이 기본, 말하는 것이 화면에 생김", ["과잉", "v25 는"]),
    # 2026-11-20 모순 점검에서 정리한 것 (manual/contradictions.yaml) — 다시 생기면 글자로 잡힘
    (r"구독[·과 ]*좋아요", "README §2-1 v24: 구독 부탁·채널명 엔딩 없음", ["넣지 않", "쓰지 않", "없음", "폐지", "레퍼런스", "참고 영상", "않습니다"]),
    (r"오늘 따라갈 길|따라가 보겠습니다", "README §2-1 v24: 순서 예고 없음 — 여는 부분은 질문으로 닫음", ["없음", "않", "폐지"]),
    (r"(?:매일|작업은?) 08:00|10:00 (?:에 )?(?:공개|KST)", "09 §1 2026-11-19: 시장 영상 07:00 제작 · 08:30 공개", ["대신", "v41", "11-17", "옛", "당시"]),
    (r"ElevenLabs[^|\n]{0,40}(?:Seedream|GPT Image|그림|이미지)", "2026-11-20 사용자: ElevenLabs 로 그림을 만들지 않음", ["않", "쓰지", "기록용", "말아", "당시"]),
    (r"edge 초안으로 운영", "09 §2-1 v43: edge 초안은 올리지 않음 (공개본 Teo)", []),
]
LEN_OK = ["쇼츠", "30~45초", "40~55초", "15~40초", "빠른 정리", "5~8분", "1.5~2분", "2~4분", "0:30", "각 ", "장 ", "초", "10~12분", "12~15분", "12~18분", "15분", "20분", "3분마다"]


def _id(*parts) -> str:
    return hashlib.sha1("|".join(map(str, parts)).encode("utf-8")).hexdigest()[:10]


def _secs():
    from . import manualgraph as mg
    return mg.parse_docs()


def _section_at(secs, file_key, line):
    best = None
    for s in secs:
        if s["doc"] == f"doc:{file_key}" and s["line"] <= line:
            if best is None or s["line"] > best["line"]:
                best = s
    return best


def _skip_section(sec) -> bool:
    if not sec:
        return False
    return "규칙의 네 층" in sec.get("title", "") or "기록용 — 지금 기본값이 아닙니다" in sec.get("body", "")


def scan_retired(docs, secs) -> list[dict]:
    out = []
    for d in docs:
        p = ROOT / d["file"]
        for i, ln in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            t = ln.strip()
            if not t or t.startswith(">"):
                continue
            heading = t.startswith("#")
            sec = _section_at(secs, d["key"], i)
            if _skip_section(sec):
                continue
            for pat, why, ok in RETIRED:
                if heading:
                    continue
                if re.search(pat, t) and not any(w in t for w in ok):
                    out.append({"kind": "retired", "level": "fix", "file": d["file"], "line": i, "text": t[:160], "why": why})
    return out


def scan_refs(docs, secs) -> list[dict]:
    """'03 §0-2', 'README §2-5', 'manual/04 §0-6' 같은 참조가 실제 절을 가리키나 + 파일 경로가 있나."""
    keys = {s["id"][4:] for s in secs}
    nums = {}
    for s in secs:
        f = s["doc"][4:]
        nums.setdefault(f, set()).add(s["num"])
    out = []
    pat = re.compile(r"(?:manual/)?\b(README|0[1-9])\b(?:-[a-z-]+(?:\.md)?)?\s*((?:§\s*[\d-]+\s*(?:[·,]\s*)?)+)")
    fpat = re.compile(r"`((?:manual|docs|styles|skins|topics|ytflow|prompts|channels|scripts|schemas)/[\w./<>{}*-]+?\.(?:md|yaml|py|json))`")
    for d in docs:
        p = ROOT / d["file"]
        for i, ln in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            for m in pat.finditer(ln):
                f = m.group(1)
                for n in re.findall(r"§\s*([\d-]+)", m.group(2)):
                    n = n.strip("-")
                    have = nums.get(f, set())
                    if n and not (n in have or any(h.startswith(n + "-") for h in have) or any(n.startswith(h + "-") for h in have if h)):
                        out.append({"kind": "ref", "level": "fix", "file": d["file"], "line": i, "text": f"{f} §{n}",
                                    "why": "그런 절이 없음 — 번호가 바뀌었거나 지워짐"})
            for m in fpat.finditer(ln):
                path = m.group(1)
                if any(c in path for c in "<>{}*"):
                    continue
                if not (ROOT / path).exists():
                    out.append({"kind": "ref", "level": "fix", "file": d["file"], "line": i, "text": path, "why": "파일이 없음"})
    return out


def instr_files() -> list[str]:
    out = []
    for g in INSTR_GLOBS:
        out += sorted(p.relative_to(ROOT).as_posix() for p in ROOT.glob(g) if p.is_file())
    return out


def load_contra() -> dict:
    import yaml
    try:
        d = yaml.safe_load(CONTRA.read_text(encoding="utf-8")) or {}
    except FileNotFoundError:
        d = {}
    d.setdefault("items", [])
    return d


def _git(*args) -> str:
    import subprocess
    try:
        return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, timeout=30).stdout.strip()
    except Exception:
        return ""


def changed_instr(since: str) -> list[str]:
    """지난 모순 점검(커밋) 뒤 바뀐 지침·매뉴얼 파일."""
    if not since or not _git("cat-file", "-t", since):
        return []
    names = _git("diff", "--name-only", f"{since}..HEAD").splitlines()
    watch = set(instr_files())
    return [n for n in names if n in watch or (n.startswith("manual/") and n.endswith(".md")
            and n not in ("manual/CHANGELOG.md", "manual/reviews.md", "manual/audit.md"))]


def scan_models() -> list[dict]:
    """모델 역할(config/models.yaml)을 30일마다 다시 보게 — 새 모델이 나오면 재설정 (2026-11-22 사용자)."""
    f = config.ROOT / "config" / "models.yaml"
    if not f.exists():
        return []
    import yaml
    m = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
    try:
        old = (dt.date.today() - dt.date.fromisoformat(str(m.get("checked")))).days
    except ValueError:
        old = 999
    if old < 30:
        return []
    roles = ", ".join(f"{k}={v.get('model')}" for k, v in (m.get("roles") or {}).items())
    return [{"kind": "proposal", "level": "ask", "file": "config/models.yaml", "line": 0,
             "text": f"모델 역할 다시 점검 ({old}일 지남): {roles}",
             "why": "새 모델이 나왔으면 models.yaml·.claude/agents 를 바꾸고 checked 를 고침 — 바꿀지는 사용자 (manual/11 §1-1)"}]


def scan_contra() -> list[dict]:
    d = load_contra()
    out = []
    for c in d["items"]:
        st = c.get("status", "open")
        if st not in ("open", "decided"):
            continue
        a, b = c.get("a") or {}, c.get("b") or {}
        out.append({"kind": "contra", "level": "ask" if st == "open" else "fix", "file": a.get("file", ""), "line": a.get("line", 0),
                    "text": f"{c.get('id')}: {a.get('file')} ↔ {b.get('file')} — {str(c.get('topic') or c.get('why', ''))[:90]}",
                    "why": ("어느 쪽이 맞는지 사용자 판단 — 답을 decision 에 적고 status: decided" if st == "open"
                            else f"결정됨: {str(c.get('decision', ''))[:80]} → 낡은 쪽을 고치고 status: resolved")})
    today = dt.date.today()
    last = d.get("last_sweep")
    try:
        last_d = dt.date.fromisoformat(str(last)) if last else None
    except ValueError:
        last_d = None
    if not last_d or (today - last_d).days >= SWEEP_DAYS:
        out.append({"kind": "sweep", "level": "fix", "file": "manual/contradictions.yaml", "line": 0,
                    "text": f"전체 모순 점검 차례 (지난 점검 {last or '없음'})",
                    "why": "skills/manual-review §모순 점검 — 주제별(대본·화면·운영·정기 작업)로 지침 전체를 맞대고 장부에 적은 뒤 manual-audit --checked --full"})
    ch = changed_instr(d.get("last_commit", ""))
    if ch:
        out.append({"kind": "sweep", "level": "fix", "file": "manual/contradictions.yaml", "line": 0,
                    "text": f"바뀐 지침 {len(ch)}개 모순 점검: " + ", ".join(ch[:6]) + (" …" if len(ch) > 6 else ""),
                    "why": "바뀐 줄이 다른 지침·정기 작업 지시문과 반대인지 확인 → 장부에 적고 manual-audit --checked"})
    return out


def mark_checked(full: bool = False) -> None:
    """모순 점검을 마쳤다고 장부에 남김 (변경분 기준 커밋 = 지금 HEAD, --full 이면 전체 점검 날짜도)."""
    import yaml
    d = load_contra()
    d["last_commit"] = _git("rev-parse", "HEAD")
    if full:
        d["last_sweep"] = dt.date.today().isoformat()
    head = "\n".join(l for l in CONTRA.read_text(encoding="utf-8").splitlines() if l.startswith("#")) + "\n" if CONTRA.exists() else ""
    body = {k: d[k] for k in ("last_sweep", "last_commit") if d.get(k)}
    body["items"] = d["items"]
    CONTRA.write_text(head + yaml.safe_dump(body, allow_unicode=True, sort_keys=False, width=200), encoding="utf-8")
    print(f"[manual-audit] 모순 점검 기록: 커밋 {d['last_commit'][:8]}" + (f" · 전체 점검 {d['last_sweep']}" if full else ""))


def build() -> dict:
    from . import layers as ly
    from . import manualgraph as mg
    g = mg.build()
    docs, secs = _secs()
    items: list[dict] = []
    N = {n["id"]: n for n in g["nodes"]}

    for c in g.get("conflicts", []):
        items.append({"kind": "conflict", "level": "ask", "file": "", "line": 0,
                      "text": f"{mg.THEMES[c['theme']][0]}: 더 하라 {len(c['plus'])}줄 ↔ 덜 하라 {len(c['minus'])}줄",
                      "why": "같은 주제를 반대로 말하는 규칙이 함께 있음 — 범위(채널·장면)를 적거나 한쪽을 정리",
                      "detail": [p["section"] + " " + p["text"][:80] for p in c["plus"][:3] + c["minus"][:3]]})
    for b in g["bans"]:
        if b.get("overfit"):
            sec = N.get(b["section"], {})
            items.append({"kind": "overfit", "level": "ask", "file": (N.get(sec.get("doc"), {}) or {}).get("file", ""),
                          "line": sec.get("line", 0), "text": b["text"][:160],
                          "why": f"{b['tier_label']} 층인데 금지·MUST 로 적힘 — 기본값 문장으로 바꿀지, 원칙·기준으로 확정할지"})
    for n in g["nodes"]:
        if n["kind"] in ("rule", "check") and n.get("overfit"):
            items.append({"kind": "overfit", "level": "ask", "file": n.get("file", "manual/06-checklist.md"), "line": n.get("line", 0),
                          "text": f"{n['level']} {n['label'][:140]}", "why": f"{n['tier_label']} 층인데 MUST 검사 — 권고로 내릴지"})
    for p in g.get("pending", []):
        items.append({"kind": "pending", "level": "ask", "file": "manual/CHANGELOG.md", "line": 0, "text": p[:160],
                      "why": "반영 대기 — 매뉴얼을 고치고 manual-bump (그동안 check G0 실패)"})
    for n in g["nodes"]:
        if n["kind"] == "feedback" and not n.get("scope") and not n.get("tier_fixed"):
            items.append({"kind": "untiered", "level": "ask", "file": "manual/feedback.yaml", "line": 0, "text": n["quote"][:160],
                          "why": f"이 말의 층이 정해지지 않음 (자동 추정: {n.get('tier_label')}) — 영구 원칙·작업 기준·스타일 기본값·실험 기록 중"})
        if n["kind"] == "intent":
            for r in n.get("readings", []):
                if r["status"] in ("over", "under", "drift", "conflict"):
                    items.append({"kind": "misaligned", "level": "ask", "file": "manual/intents.yaml", "line": 0,
                                  "text": f"“{n['quote'][:80]}” → {r['ref']}", "why": f"{mg.STATUS[r['status']]} 판정이 남아 있음 — 고쳤으면 '정렬됨'으로"})
                elif r["ref"] not in N and r["status"] != "unreviewed":
                    items.append({"kind": "coderef", "level": "fix", "file": "manual/intents.yaml", "line": 0,
                                  "text": f"{n['id']} → {r['ref']}", "why": "판정이 가리키는 절·코드 줄이 없음 (줄이 옮겨짐) — 새 위치로 다시 판정"})
        if n["kind"] == "term":
            for c in n.get("code") or []:
                if c.get("line") is None:
                    items.append({"kind": "coderef", "level": "fix", "file": "manual/glossary.yaml", "line": 0,
                                  "text": f"{n['name']} → {c['file']}", "why": "용어 사전의 code 글자를 그 파일에서 못 찾음"})
    # 용도가 정해지지 않은 기능 (2026-11-15 사용자: 기능마다 언제 쓰는지 먼저 정리) — 새 장면·움직임·효과·팩이 생기면 잡힘
    for t in g["nodes"]:
        if t["kind"] == "term" and t["cat"] in ("scene", "motion", "fx", "skin", "measure", "technique", "style") and not t.get("use_when"):
            items.append({"kind": "nousage", "level": "ask", "file": "manual/usage.yaml", "line": 0, "text": f"{t['cat_label']}: {t['name']}",
                          "why": "언제 쓰나·쓰지 않나·대신이 정해지지 않음 — usage.yaml (스타일은 레시피 when·fits, 기법은 techniques.yaml) 에 초안을 써서 확인받기"})
    # 제안함 (잠금 없이 남긴 것·잠금 중 요청, docs/35) — 잠금을 잡은 쪽이 반영하거나 사용자에게 묻는다
    from . import governance as gv
    for p in gv.proposals("open"):
        items.append({"kind": "proposal", "level": "ask", "file": p["file"], "line": 0, "text": f"[{p.get('kind')}] {p['text'][:140]}",
                      "why": f"{p.get('from_branch')} 의 제안 — 잠금을 잡은 쪽이 반영(feedback·review·매뉴얼 수정) 뒤 제안 파일의 status 를 done 으로"})
    # 주제 레포가 가리키는 장면·기법이 있나
    scene_ok = {t["key"] for t in g["nodes"] if t["kind"] == "term"}
    tech_ok = set(ly.techniques())
    for tid in ly.topic_ids():
        eff = ly.resolve(tid)
        for k, s in eff["situations"].items():
            for sc in s.get("scenes") or []:
                if sc not in scene_ok:
                    items.append({"kind": "topic", "level": "fix", "file": f"topics/{tid}/topic.yaml", "line": 0,
                                  "text": f"{k} → 장면 {sc}", "why": "그런 장면 종류(렌더 함수)가 없음"})
            for t in s.get("techniques") or []:
                if t not in tech_ok:
                    items.append({"kind": "topic", "level": "fix", "file": f"topics/{tid}/topic.yaml", "line": 0,
                                  "text": f"{k} → 기법 {t}", "why": "styles/techniques.yaml 에 없는 기법"})
    items += scan_retired(docs, secs)
    items += scan_refs(docs, secs)
    # 매뉴얼 밖 지침 파일에도 같은 잣대 (절 구분이 없으므로 절 예외 없이)
    instr = [{"file": f, "key": f"instr:{f}"} for f in instr_files()]
    items += [dict(x, kind="retired") for x in scan_retired(instr, secs)]
    items += scan_refs(instr, secs)
    items += scan_contra()
    items += scan_models()
    if mg.is_stale():
        items.append({"kind": "stale", "level": "fix", "file": "manual/graph.json", "line": 0, "text": "매뉴얼 그래프가 옛것",
                      "why": "python -m ytflow manual-graph"})
    for it in items:
        it["id"] = _id(it["kind"], it["file"], it["text"])
    # 지난번과 비교
    prev = {}
    try:
        prev = json.loads(OUT_JSON.read_text(encoding="utf-8"))
    except Exception:
        pass
    prev_ids = {x["id"]: x for x in prev.get("items", [])}
    cur_ids = {x["id"] for x in items}
    for it in items:
        it["new"] = it["id"] not in prev_ids
        it["since"] = prev_ids.get(it["id"], {}).get("since") or dt.date.today().isoformat()
    resolved = [dict(x, resolved=dt.date.today().isoformat()) for x in prev.get("items", []) if x["id"] not in cur_ids]
    log = (prev.get("log") or [])[-30:]
    return {"date": dt.datetime.now().isoformat(timespec="minutes"), "manual_version": g["stats"]["manual_version"],
            "counts": {"fix": sum(1 for x in items if x["level"] == "fix"), "ask": sum(1 for x in items if x["level"] == "ask"),
                       "new": sum(1 for x in items if x["new"]), "resolved": len(resolved)},
            "items": items, "resolved": resolved, "log": log, "fixed_by_agent": []}


KIND = {"proposal": "제안함", "nousage": "용도 미정 기능", "conflict": "충돌 후보", "overfit": "과적합 후보", "pending": "반영 대기", "untiered": "층 미정 피드백", "misaligned": "어긋난 해석",
        "retired": "폐지된 기준이 남음", "ref": "깨진 참조", "coderef": "코드 위치 바뀜", "topic": "주제 레포 오류", "stale": "옛 그래프",
        "contra": "모순", "sweep": "모순 점검 차례"}


def write(quiet: bool = False, note: str = "", fixed: list[str] | None = None) -> dict:
    from . import governance as gv
    if not gv.can_write():   # 보고서(manual/audit.*)는 잠금을 가진 쪽만 씀 — 다른 세션은 읽기만
        a = build()
        print(f"[manual-audit] (읽기만 — 잠금 없음) 고칠 것 {a['counts']['fix']} · 물어볼 것 {a['counts']['ask']}")
        return a
    a = build()
    a["fixed_by_agent"] = [f for f in (fixed or []) if f.strip()]
    entry = {"date": a["date"], "fix": a["counts"]["fix"], "ask": a["counts"]["ask"], "new": a["counts"]["new"],
             "resolved": a["counts"]["resolved"], "note": note}
    a["log"].append(entry)
    OUT_JSON.write_text(json.dumps(a, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    L = [f"# 매뉴얼 정기 검토 — {a['date']} (매뉴얼 v{a['manual_version']})", "",
         "> 자동 생성 (`python -m ytflow manual-audit`, docs/34). **fix** = 판단 없이 고칠 수 있음 → 정기 검토가 고침 · **ask** = 사용자 판단 필요 → 질문으로 남김.", "",
         f"**고칠 것 {a['counts']['fix']} · 물어볼 것 {a['counts']['ask']} · 새로 생김 {a['counts']['new']} · 지난번 뒤 해결됨 {a['counts']['resolved']}**", ""]
    for lvl, title in (("ask", "## 물어볼 것 (사용자 판단)"), ("fix", "## 고칠 것 (판단 불필요)")):
        rows = [x for x in a["items"] if x["level"] == lvl]
        L += [title, ""]
        if not rows:
            L += ["없음", ""]
            continue
        L += ["| 종류 | 위치 | 내용 | 왜 | 처음 본 날 |", "|---|---|---|---|---|"]
        for x in rows:
            where = f"{x['file']}:{x['line']}" if x.get("line") else x.get("file", "")
            L.append(f"| {KIND.get(x['kind'], x['kind'])}{' 🆕' if x['new'] else ''} | {where} | {x['text'].replace('|', '/')[:110]} | {x['why'].replace('|', '/')} | {x['since']} |")
        L.append("")
    if a["fixed_by_agent"]:
        L += ["## 이번 검토에서 고친 것", ""] + [f"- {f}" for f in a["fixed_by_agent"]] + [""]
    if a["resolved"]:
        L += ["## 지난 검토 뒤 해결됨", ""] + [f"- {KIND.get(x['kind'], x['kind'])}: {x['text'][:100]}" for x in a["resolved"][:30]] + [""]
    L += ["## 검토 기록", "", "| 날짜 | 고칠 것 | 물어볼 것 | 새로 | 해결 | 메모 |", "|---|---|---|---|---|---|"]
    L += [f"| {e['date']} | {e['fix']} | {e['ask']} | {e['new']} | {e['resolved']} | {e.get('note', '')} |" for e in a["log"][-14:]]
    OUT_MD.write_text("\n".join(L) + "\n", encoding="utf-8")
    msg = f"[manual-audit] v{a['manual_version']} · 고칠 것 {a['counts']['fix']} · 물어볼 것 {a['counts']['ask']} · 새로 {a['counts']['new']} · 해결 {a['counts']['resolved']} → manual/audit.md"
    print(msg)
    if not quiet:
        for x in a["items"][:40]:
            print(f"  [{x['level']}] {KIND.get(x['kind'], x['kind'])}: {x.get('file', '')}:{x.get('line', '')} {x['text'][:90]}")
    return a
