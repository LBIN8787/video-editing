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
        if p.name in ("CHANGELOG.md", "reviews.md"):
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

    nodes = steps + gates + channels + docs + secs + rules + checks + versions + reviews + themes
    cur = _read(MANUAL / "VERSION").strip() or "0"
    stats = {
        "manual_version": int(cur),
        "versions": len(versions), "reviews": len(reviews),
        "rejects": sum(r["result"] == "reject" for r in reviews), "passes": sum(r["result"] == "pass" for r in reviews),
        "pending": len(pending), "rules": len(rules), "checks": len(checks), "sections": len(secs),
        "must": sum(r["level"] == "MUST" for r in rules), "auto": sum(r["auto"] for r in rules),
    }
    return {"schema": SCHEMA_VERSION, "generated": dt.datetime.now().isoformat(timespec="seconds"),
            "stats": stats, "pending": pending, "nodes": nodes, "edges": edges}


def write(html_out: str | None = None) -> Path:
    g = build()
    out = MANUAL / "graph.json"
    slim = json.loads(json.dumps(g))
    for n in slim["nodes"]:
        n.pop("body", None)          # 본문은 md 가 원본 — json 에는 구조만
    out.write_text(json.dumps(slim, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    s = g["stats"]
    print(f"[manual-graph] v{s['manual_version']} · 절 {s['sections']} · 규칙 {s['rules']}(MUST {s['must']}) · 검사 코드 {s['checks']} "
          f"· 버전 {s['versions']} · 검토 {s['reviews']}(기각 {s['rejects']}) · 반영 대기 {s['pending']} → {out.relative_to(ROOT)}")
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
        if p.parent != MANUAL.resolve() or p.suffix != ".md":
            raise ValueError("manual/*.md 만 열고 고칠 수 있습니다")
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
                    return self._json({"ok": True})
                if u.path == "/api/bump":
                    summary = (body.get("summary") or "").strip()
                    if not summary:
                        raise ValueError("바꾼 기준 요약을 적어 주세요")
                    v = checklist.bump(summary, tag=False)
                    return self._json({"ok": True, "version": int(v),
                                       "next": f"git add manual && git commit -m \"매뉴얼 v{v}: {summary}\" && git push origin HEAD:refs/heads/manual/v{v}"})
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
