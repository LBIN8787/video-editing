"""어닝콜(실적 발표 뒤 경영진·애널리스트 통화) 정리 — v18, 사용자 요청 2026-11-12:
"실적도 실적이지만 어닝콜 내용까지 자세히 — 코어위브만이 아니라 다른 기업들도".

    python -m ytflow earnings-call <프로젝트> <원문 PDF·텍스트 경로 또는 주소> --ticker CRWV

원문 우선순위 (manual/03 §0-1): ① 회사 IR 의 공식 녹취록(Proofread transcript)·웹캐스트 ② SEC 8-K 실적 보도자료
③ 녹취록 사이트(모틀리풀 등, 이름 오타 주의). 막힌 곳(403·봇 확인)은 우회하지 않음.

결과 01_research/earnings/<TICKER>_<분기>.txt (원문 텍스트) 와 <TICKER>_call.md:
  - 참석자, 준비 발언에서 핵심 낱말(가이던스·수주 잔고·마진·빚·선지급·가격·수요·설비투자·위험)이 든 문장
  - 질의응답 표: 애널리스트(회사) · 질문 요지 · 첫인사(콜에 대한 반응) · 답한 사람
  - 질문 주제 집계 = 시장이 걱정하는 것
여기서 대본으로 옮길 때는 원문 문장(영어) + 번역을 함께 (quote 장면의 "orig").
"""
from __future__ import annotations

import re
import subprocess
from collections import Counter
from pathlib import Path

TOPICS = {
    "자금 조달·빚": ["debt", "financing", "unsecured", "credit", "capital markets", "ddtl", "prepay", "funding", "leverage"],
    "수요·공급": ["demand", "supply", "capacity", "sold out", "oversupply", "backlog"],
    "가격·마진": ["pricing", "price", "margin", "per megawatt", "economics"],
    "설비 투자": ["capex", "capital expenditure", "data center", "power", "gigawatt"],
    "가이던스": ["guidance", "outlook", "expect", "2027", "2028"],
    "규제·정치": ["regulat", "election", "permit", "policy", "tariff", "export"],
    "고객": ["customer", "concentration", "enterprise", "lab", "diversif"],
}
KEY = ["guidance", "backlog", "margin", "debt", "prepay", "pricing", "demand", "capex", "outlook", "risk", "will not", "expect", "record"]
PRAISE = ["thanks for all", "great quarter", "congrat", "nice quarter", "great disclosure", "comforting", "impressive", "strong quarter", "appreciate the"]


def load_text(src: str, out_dir: Path) -> str:
    out_dir.mkdir(parents=True, exist_ok=True)
    p = Path(src)
    if src.startswith("http"):
        p = out_dir / ("_src.pdf" if src.lower().split("?")[0].endswith(".pdf") else "_src.html")
        r = subprocess.run(["curl", "-sSL", "-m", "60", "-A", "Mozilla/5.0", "-o", str(p), "-w", "%{http_code}", src], capture_output=True, text=True)
        if r.stdout.strip() != "200":
            raise SystemExit(f"[earnings] 받기 실패 HTTP {r.stdout.strip()} — 막힌 곳은 우회하지 않습니다. 다른 공식 원문을 찾거나 PC 에서 받아 경로로 주세요.")
    if p.suffix.lower() == ".pdf":
        try:
            t = subprocess.run(["pdftotext", "-layout", str(p), "-"], capture_output=True, text=True, check=True).stdout
        except Exception:  # noqa: BLE001
            import pypdf
            t = "\n".join(pg.extract_text() or "" for pg in pypdf.PdfReader(str(p)).pages)
    else:
        t = p.read_text(encoding="utf-8", errors="ignore")
        if "<html" in t[:2000].lower():
            import html
            t = html.unescape(re.sub(r"<[^>]+>", "\n", re.sub(r"(?s)<script.*?</script>|<style.*?</style>", "", t)))
    t = re.sub(r"\n\s*Page \d+ of \d+\s*\n", "\n", t)
    return t.replace("â€“", "–").replace("â€™", "'")


SPEAKER = re.compile(r"^\s*(Operator|[A-Z][A-Za-z.'\- ]{2,40}),\s*(Chief [A-Za-z ]+|Analyst, [^\n]+|[A-Z][A-Za-z ]*(?:Officer|President|Relations)[^\n]*)\s*$")


def split_turns(t: str) -> list[dict]:
    turns, cur = [], None
    for line in t.splitlines():
        m = SPEAKER.match(line)
        if m or line.strip() == "Operator":
            if cur:
                turns.append(cur)
            name = m.group(1) if m else "Operator"
            role = m.group(2) if m else ""
            firm = role.split("Analyst, ", 1)[1].strip() if role.startswith("Analyst, ") else ""
            cur = {"name": name, "role": role, "firm": firm, "analyst": bool(firm), "text": ""}
        elif cur is not None:
            cur["text"] += " " + line.strip()
    if cur:
        turns.append(cur)
    for x in turns:
        x["text"] = re.sub(r"\s+", " ", x["text"]).strip()
    return turns


def sentences(t: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", t) if len(s.strip()) > 30]


def run(project: str, src: str, ticker: str = "", period: str = "") -> Path:
    from ..project import Project
    pr = Project.open(project)
    out = pr.dir("research") / "earnings"
    t = load_text(src, out)
    tk = (ticker or "CO").upper()
    raw = out / f"{tk}_{period or 'call'}.txt"
    raw.write_text(t, encoding="utf-8")
    turns = split_turns(t)
    qa_start = next((i for i, x in enumerate(turns) if "question" in x["text"][:300].lower() and x["name"] == "Operator" and i > 2), len(turns))
    prepared = " ".join(x["text"] for x in turns[:qa_start] if not x["analyst"] and x["name"] != "Operator")
    L = [f"# {tk} 어닝콜 정리 {period}", "", f"원문: {src}", f"원문 텍스트: `{raw.name}` ({len(t.split()):,}단어)", "",
         "> 대본에는 원문 문장(영어)과 번역을 함께 씁니다. 숫자는 보도자료·10-Q 와 대조. 좋은 말과 남은 위험(손실·이자·희석)을 같이.", "",
         "## 참석자"]
    seen = []
    for x in turns:
        k = (x["name"], x["role"])
        if x["name"] != "Operator" and k not in seen:
            seen.append(k)
    L += [f"- {n} — {r}" for n, r in seen]
    L += ["", "## 준비 발언의 핵심 문장 (숫자·약속·위험)"]
    hits = [s for s in sentences(prepared) if any(k in s.lower() for k in KEY) or re.search(r"\$\d|\d+%|\d+ (billion|million)", s)]
    L += [f"- {s}" for s in hits[:45]]
    L += ["", "## 질의응답 — 시장이 묻는 것", "| # | 애널리스트 (회사) | 질문 요지 | 첫마디 (콜에 대한 반응) | 답한 사람 |", "|---|---|---|---|---|"]
    qs, topics = [], Counter()
    for i, x in enumerate(turns[qa_start:], qa_start):
        if not x["analyst"]:
            continue
        ss = sentences(x["text"]) or [x["text"]]
        q = next((s for s in ss if "?" in s), ss[-1])
        opening = ss[0][:110] if any(w in ss[0].lower() for w in PRAISE) else ""
        ans = next((y["name"] for y in turns[i + 1:i + 3] if not y["analyst"] and y["name"] != "Operator"), "")
        for name, words in TOPICS.items():
            if any(w in x["text"].lower() for w in words):
                topics[name] += 1
        qs.append(1)
        L.append(f"| {len(qs)} | {x['name']} ({x['firm']}) | {q[:160].replace('|', '/')} | {opening.replace('|', '/')} | {ans} |")
    L += ["", "## 질문 주제 집계", ", ".join(f"{k} {v}" for k, v in topics.most_common()) or "(없음)", "",
          "## 대본으로 옮길 때 (manual/03 §0-1)",
          "1. 숫자: 실적 vs 예상 vs 회사 가이던스  2. 시장의 걱정에 경영진이 한 답(원문+번역)  3. 애널리스트가 물은 것 = 시장의 걱정",
          "4. 콜의 평가: 주가·애널리스트 반응  5. 남은 숙제(손실·이자·희석·고객 집중)  6. 다음 분기에 확인할 약속"]
    md = out / f"{tk}_call.md"
    md.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"[earnings] 발언 {len(turns)}개 · 질문 {len(qs)}개 → {md}")
    return md
