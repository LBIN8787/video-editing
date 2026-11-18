"""제작 체크리스트 자동 검사 + 사용자 검토(통과/기각) 기록 + 매뉴얼 버전 올리기.

    python -m ytflow check <프로젝트> [--upto G4]        → 05_edit/checklist.md · checklist.json (MUST 실패 시 종료 코드 1)
    python -m ytflow review <프로젝트> --pass [--note ..]  → manual/reviews.md 에 '통과' (그 매뉴얼 버전을 그대로 씀)
    python -m ytflow review <프로젝트> --reject "이유"     → manual/reviews.md 에 '기각' + manual/CHANGELOG.md '반영 대기'
    python -m ytflow manual-bump "바꾼 기준 요약"          → manual/VERSION +1, 대기 항목을 그 버전으로 확정 (스냅샷 브랜치 manual/vN 으로 백업)

기준: manual/06-checklist.md (사람용 표). 이 파일은 그중 자동으로 잴 수 있는 것만 잰다.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import subprocess
from pathlib import Path

import yaml

from .. import config

MANUAL = config.ROOT / "manual"
GATES = ["G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8"]
BRANDS = ("ai", "market", "curiosity", "issues")

INVEST = ["사세요", "파세요", "매수 추천", "매도 추천", "매수하세요", "매도하세요", "지금이 기회", "지금 사야", "무조건 오", "확실히 오른",
          "수익 보장", "따라 사면", "목표가는", "꼭 사야", "담으세요", "줍줍"]
HYPE = ["충격", "소름", "경악", "역대급", "미쳤다", "이거면 끝"]
UNFINISHED = ["재확인 필요", "TODO", "TBD", "확인 필요]", "XXX"]
REF_NAMES = ["미주일기", "식스시그마", "머니크루", "AI비즈PT", "로제타"]
ISSUE_BANNED = ["범인은", "충들", "틀딱", "한남", "김치녀", "짱깨", "쪽바리", "빨갱이", "토착왜구", "매국노"]   # 단정·집단 비하 (manual/08 §6)
BAD_LICENSE = ["CC BY-SA", "CC-BY-SA", "BY-NC", "BY-ND", "CC BY-NC", "CC BY-ND", "All rights reserved"]
FOOTAGE_TYPES = {"footage", "kb", "journey", "outro"}


def manual_version() -> str:
    f = MANUAL / "VERSION"
    return f.read_text(encoding="utf-8").strip() if f.exists() else "0"


def pending_changes() -> list[str]:
    """기각 사유 중 아직 매뉴얼에 반영되지 않은 것 (CHANGELOG 의 '반영 대기' 절)."""
    f = MANUAL / "CHANGELOG.md"
    if not f.exists():
        return []
    s = f.read_text(encoding="utf-8")
    m = re.search(r"## 반영 대기\n(.*?)(?=\n## |\Z)", s, re.S)
    return [l[2:].strip() for l in (m.group(1).splitlines() if m else []) if l.startswith("- ")]


class Report:
    def __init__(self):
        self.rows: list[dict] = []

    def add(self, gate, level, item, ok, detail=""):
        self.rows.append({"gate": gate, "level": level, "item": item, "ok": bool(ok), "detail": str(detail)})

    def must_fail(self):
        return [r for r in self.rows if r["level"] == "MUST" and not r["ok"]]


def _load(p: Path):
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8")) if p.suffix == ".json" else p.read_text(encoding="utf-8")


def _opening(spec: dict) -> list:
    """여는 부분: 첫 장 표지(chapter) 앞의 장면들. 장 표지가 없으면 앞 3장면 (v38 — '첫 N장면' 같은 숫자 대신 이야기 구조로)."""
    sc = spec.get("scenes", [])
    idx = next((i for i, x in enumerate(sc) if i > 0 and x.get("type") == "chapter"), None)
    return sc[:idx] if idx else sc[:3]


def _texts(spec: dict) -> str:
    out = []
    for s in spec.get("scenes", []):
        for b in s.get("beats", []):
            out.append(b.get("say", ""))
        for k in ("title", "quote", "lines", "caption", "stamp"):
            v = s.get(k)
            out.extend(v if isinstance(v, list) else [v] if isinstance(v, str) else [])
    return "\n".join(out)


def _brand(path: Path) -> tuple[str, str, dict]:
    ed = yaml.safe_load((path / "edit.yaml").read_text(encoding="utf-8")) if (path / "edit.yaml").exists() else {}
    ch = (ed or {}).get("channel", "")
    try:
        brand = config.channel(ch).get("brand", "") if ch else ""
    except Exception:
        brand = ""
    tb = _load(path / "01_research" / "topic_brief.json") or {}
    return tb.get("brand") or brand, ch, ed or {}


def run(path: Path, upto: str = "G8") -> Report:
    R = Report()
    last = GATES.index(upto) if upto in GATES else len(GATES) - 1
    brand, ch, ed = _brand(path)
    res, scr, edt = path / "01_research", path / "02_script", path / "05_edit"
    spec = _load(scr / "hybrid.json") or _load(scr / "scenes.json") or {}
    longform = (ed.get("format") or "longform") == "longform"
    tl = _load(edt / "hybrid_timeline.json") or []

    # 매뉴얼: 기각 사유가 반영되기 전에는 새 영상을 만들지 않는다 (기준을 차곡차곡 쌓기)
    pend = pending_changes()
    R.add("G0", "MUST", "기각 사유가 매뉴얼에 모두 반영됨 (manual/CHANGELOG.md '반영 대기' 비어 있음)", not pend, "; ".join(pend))
    try:   # 피드백·매뉴얼을 바꾼 뒤 그래프를 다시 만들었나 (docs/31 §8)
        from . import manualgraph as _mg
        R.add("G0", "SHOULD", "매뉴얼 그래프가 최신 (python -m ytflow manual-graph)", not _mg.is_stale(), "manual/graph.json")
    except Exception:
        pass

    # G1 주제
    tb = _load(res / "topic_brief.json")
    R.add("G1", "MUST", "topic_brief.json 있음", tb is not None, "01_research/topic_brief.json (schemas/topic_brief.schema.json)")
    tb = tb or {}
    R.add("G1", "MUST", "브랜드(ai/market/curiosity)", brand in BRANDS, brand or "edit.yaml 채널에 brand 없음")
    R.add("G1", "MUST", "욕망·시청자 질문", tb.get("desire") and tb.get("viewer_question"), tb.get("viewer_question", ""))
    R.add("G1", "MUST", "트리거·왜 지금", tb.get("trigger") and tb.get("why_now"), tb.get("trigger", ""))
    sc = tb.get("score") or {}
    tot = sum(int(v) for v in sc.values() if isinstance(v, (int, float)))
    R.add("G1", "MUST", "욕망을 분명히 건드리고, 보여 줄 자료가 있다 (둘 중 하나라도 약하면 만들지 않음, 01 §3)",
          sc.get("desire", 0) >= 2 and sc.get("visuals", 0) >= 2, f"강도 {sc.get('desire')} · 자료 {sc.get('visuals')}")
    R.add("G1", "참고", "욕망 점수 합계 (후보끼리 비교할 때 씀)", True, f"합계 {tot} {sc}")
    R.add("G1", "MUST", "수요 증거 1개 이상", len(tb.get("demand_evidence") or []) >= 1, len(tb.get("demand_evidence") or []))
    R.add("G1", "SHOULD", "후보 3개 비교 기록", len(tb.get("candidates") or []) >= 3, len(tb.get("candidates") or []))
    R.add("G1", "SHOULD", "우리만의 답(our_angle)", bool(tb.get("our_angle")), tb.get("our_angle", ""))
    drv = tb.get("driver") or {}
    R.add("G1", "MUST" if brand == "issues" else "SHOULD", "무엇이 띄우나(driver: 소재·각도·형식 + 근거)",
          drv.get("type") in ("소재", "각도", "형식") and bool(drv.get("why")) and (drv.get("type") != "각도" or bool(drv.get("angle"))),
          f"{drv.get('type', '')} · {drv.get('why', '')[:40]}")

    ed_ch = ""
    try:
        ed_ch = (yaml.safe_load((Path(path) / "edit.yaml").read_text(encoding="utf-8")) or {}).get("channel", "")
    except Exception:
        pass
    if last >= 1 and (ed_ch == "ch-market-daily" or brand == "market"):   # SAVE(오선) 소식 기본 확인 (2026-11-14 사용자, manual/09 §3-0)
        from . import savecheck
        sv = savecheck.read(Path(path) / "01_research")
        R.add("G2", "MUST", "시장: SAVE(오선) 소식 확인 기록 — 상태 '확인함' 또는 '확인 못 함: 이유' (01_research/save_check.md)",
              sv["done"], sv["status"] or "save_check.md 없음 (python -m ytflow daily 가 만듦)")
        R.add("G2", "SHOULD", "시장: SAVE 실제로 확인함 (항목 1개 이상)", sv["done"] and sv["status"].startswith("확인함") and sv["items"] >= 1,
              f"{sv['status']} · 항목 {sv['items']}")
    if last >= 1:  # G2 소스
        foot = spec.get("footage") or {}
        miss = [k for k, v in foot.items() if not (v.get("credit") and v.get("url"))]
        drawn = not foot and any(x.get("type") in ("story", "stage") for x in spec.get("scenes", []))   # 그림판(story)만으로 그린 영상: 자료 화면 없음 (manual/04 §0-4)
        R.add("G2", "MUST", "자료 화면마다 credit·url", bool(foot and not miss) or drawn, f"{len(foot)}개, 빠짐 {miss}" + (" · 직접 그린 그림판" if drawn else ""))
        bad = [k for k, v in foot.items() if any(b.lower() in (v.get("credit", "")).lower() for b in BAD_LICENSE)]
        R.add("G2", "MUST", "금지 라이선스(SA·NC·ND) 없음", not bad, bad)
        srcs = {v.get("url") for v in foot.values()}
        R.add("G2", "참고", "자료 화면 소스 종류 (한 곳에서만 가져오면 화면이 단조로워짐)", not longform or len(srcs) >= 3, f"{len(srcs)}종")

    if last >= 2:  # G3 사실
        fs = _load(res / "factsheet.md") or ""
        links = set(re.findall(r"https?://[^\s)>\]]+", fs))
        R.add("G3", "MUST", "팩트시트 + 출처 링크 3개 이상", fs and len(links) >= (3 if longform else 1), f"링크 {len(links)}개")
        R.add("G3", "SHOULD", "확인 상태 표시(✅/⚠️)", "✅" in fs or "확인" in fs, "")
        R.add("G3", "SHOULD", "'쓰지 않는 것' 목록", "쓰지 않" in fs, "")

    if last >= 3:  # G4 대본
        txt = _texts(spec)
        _it = path / "02_script" / "intent.md"
        if _it.exists():   # 목적 분간 (11 §2-4, 2026-11-18 사용자) — 있는지만 봄, 어느 쪽인지는 D2 에서 사람이
            R.add("G4", "SHOULD", "목적 분간: intent.md 에 '목적:' 정보 습득형/즐길거리형 + 세 질문 (11 §2-4)",
                  bool(re.search(r"^\s*목적\s*:", _it.read_text(encoding="utf-8"), re.M)), "")
        R.add("G4", "MUST", "core_message·question·logic", all(spec.get(k) for k in ("core_message", "question", "logic")), "")
        cnt = {k: len(spec.get(k) or []) for k in ("compare_to", "analogies", "past_cases", "glossary")}
        if brand == "curiosity":   # v38: 호기심은 사실이 이야기 속에 (04 §0-6) — 비유와 대비 숫자만, SHOULD
            R.add("G4", "SHOULD", "curiosity: 비유와 대비가 되는 숫자 — 사실은 이야기 속에서 (04 §0-6)", cnt["analogies"] >= 1 and cnt["compare_to"] >= 1, cnt)
        else:
            R.add("G4", "MUST", "쉬운 대본: 숫자엔 비교 기준, 낯선 개념엔 비유, 과거 사례, 어려운 말 풀이가 있다", all(cnt[k] >= 1 for k in cnt), cnt)
        inv = [w for w in INVEST if w in txt]
        R.add("G4", "MUST", "투자 권유 표현 0개", not inv, inv)
        ref = [w for w in REF_NAMES if w in txt]
        R.add("G4", "MUST", "레퍼런스 채널 이름 0개", not ref, ref)
        unf = [w for w in UNFINISHED if w in txt]
        R.add("G4", "MUST", "미완성 표시 0개", not unf, unf)
        hype = [w for w in HYPE if w in txt]
        R.add("G4", "SHOULD", "과장 단어 0개", not hype, hype)
        import re as _re2   # v16 진행 말투: 연결어미로 문장을 끝내지 않기 (README §2-2)
        _says = [b.get("say", "") for s in spec.get("scenes", []) for b in s.get("beats", [])]
        awk = [m.group(0) for t in _says for m in _re2.finditer(r"[^.?!]{0,14}(?:였|이었|했|었|았|였었)고요[.!]", t)]
        R.add("G4", "MUST", "진행 말투: '~였고요.' 같은 이어 붙인 끝맺음 없음 (README §2-2)", not awk, awk[:3])
        first = " ".join(b.get("say", "") for s in _opening(spec) for b in s.get("beats", []))
        R.add("G4", "SHOULD", "여는 부분에 이 영상의 질문 하나 (시청자가 무엇을 따라가는지 알게)", "?" in first or "까요" in first or "일까" in first, "")
        if brand == "curiosity" and longform and spec.get("scenes"):   # v17 호기심 먼저 (04 §0)
            hk = tb.get("hook") or {}
            R.add("G1", "MUST", "curiosity: 훅 먼저 정하기 (topic_brief.hook: type·line·gap)", bool(hk.get("line") and hk.get("gap")), hk.get("type", ""))
            beats2 = [b.get("say", "") for s in spec["scenes"][:2] for b in s.get("beats", [])]
            words = lambda t: set(_re2.findall(r"[가-힣A-Za-z0-9]{2,}", t))
            hw0 = words(hk.get("line", ""))
            hit = next((i for i, t in enumerate(beats2) if hw0 and len(words(t) & hw0) >= max(2, len(hw0) // 3)), None)
            agenda = next((i for i, t in enumerate(beats2) if "순서" in t), None)
            R.add("G4", "MUST", "curiosity: 여는 장면이 곧 훅 — 소개·순서 예고·설명보다 앞 (04 §0)",
                  hit is not None and hit <= 3 and (agenda is None or hit < agenda), f"훅 박자 {hit} · 순서 예고 {agenda}")
            gap_w = words(hk.get("gap", ""))
            R.add("G4", "MUST", "curiosity: 훅의 질문(gap)이 나옴 (답은 숨김)",
                  any(("?" in t or "까요" in t) and len(words(t) & gap_w) >= 2 for t in [b.get("say", "") for s in spec["scenes"][:4] for b in s.get("beats", [])]),
                  hk.get("gap", "")[:40])   # v24 미주일기 문법: 여는 장면 → 그 일의 크기 → 질문 (첫 네 장면 안)
            # v23 시청자 먼저 (04 §0-6, docs/29): 상권 조사처럼 시청자를 먼저 알고, 대본이 지식 습득으로 치우치지 않게
            aud = (res / "audience.md").read_text(encoding="utf-8") if (res / "audience.md").exists() else ""
            R.add("G1", "MUST", "curiosity: 시청자 조사 01_research/audience.md (주 시청자·유입 경로·유입 이유·끝까지 보는 이유)",
                  all(k in aud for k in ("주 시청자", "유입 경로", "유입 이유", "끝까지 보는 이유")), "docs/29")
            sv = sorted((Path(path) / "02_script").glob("script_v*.md"))
            if sv:   # 사람이 문장마다 ●이야기 / ○지식 으로 표시한 대본
                body = sv[-1].read_text(encoding="utf-8")
                body = body[body.find("## 2."):body.find("## 3.")] if "## 2." in body else body
                cnt = {"●": 0, "○": 0}
                for ln in body.splitlines():
                    if ln[:1] in cnt:
                        cnt[ln[0]] += len([x for x in _re2.split(r"(?<=[.?!])\s+", ln[1:].strip()) if x])
                tot = sum(cnt.values()) or 1
                R.add("G4", "참고", "curiosity: 지식·설명 문장의 몫 (사실이 사람·사건 속에 있는지 — 판단은 대본 검토 D2, 04 §0-6)", cnt["○"] / tot <= 0.30, f"{cnt['○']}/{tot} = {cnt['○'] / tot:.0%} ({sv[-1].name})")
            else:   # 표시가 없으면 낱말로 센 하한 (실제보다 낮게 나옴)
                sents = [x for t in _says for x in _re2.split(r"(?<=[.?!])\s+", t) if x.strip()]
                kn = [x for x in sents if _re2.search(r"\d{4}년|\d|대학|박사|교수|학자|논문|책에|이라고 부릅|알려져|정리했|순서로|첫 번째|두 번째|세 번째", x)]
                R.add("G4", "참고", "curiosity: 지식·설명 문장의 몫 (자동 추정 — 판단은 대본 검토 D2)",
                      len(kn) / max(len(sents), 1) <= 0.30, f"{len(kn)}/{len(sents)}")
            rvw = (Path(path) / "02_script" / "script_review.md")
            R.add("G4", "MUST", "curiosity: 편집 전에 대본만 사용자 검토 통과 (02_script/script_review.md '통과', 04 §0-6)",
                  rvw.exists() and "통과" in rvw.read_text(encoding="utf-8"), "")
            pk = spec.get("package") or {}
            titles = [pk.get("title", "")] + list(pk.get("title_options") or [])
            hw = set(_re2.findall(r"[가-힣A-Za-z0-9]{2,}", (hk.get("line", "") + " " + hk.get("gap", ""))))
            tied = [t for t in titles if t and hw & set(_re2.findall(r"[가-힣A-Za-z0-9]{2,}", t))]
            R.add("G6", "SHOULD", "curiosity: 제목이 훅에서 나옴 (훅과 같은 낱말)", bool(hw) and len(tied) >= max(1, len([t for t in titles if t]) - 1), f"{len(tied)}/{len([t for t in titles if t])}")
        if brand in ("market", "issues") and spec.get("scenes"):   # v18 연결·의미 (03 §0-1)
            fs_all = (res / "factsheet.md").read_text(encoding="utf-8") if (res / "factsheet.md").exists() else ""
            says_all = " ".join(b.get("say", "") for s in spec["scenes"] for b in s.get("beats", []))
            R.add("G3", "MUST" if ch in ("ch-market-daily", "ch-issues-daily") else "SHOULD",
                  "연결·의미: 팩트시트에 '## 해석'(근거 번호와 함께) — 사실만 옮기지 않기 (03 §0-1)", "## 해석" in fs_all, "")
            R.add("G4", "SHOULD", "연결·의미: 대본에서 해석을 해석이라고 밝힘 ('해석'·'의미'·'로 볼 수 있')",
                  any(w in says_all for w in ("해석", "의미", "로 볼 수 있", "라고 봅니다")), "")
        if ch in ("ch-market-daily", "ch-issues-daily"):   # v17 매일 브리핑 (03 §0, 08 §0-2)
            db = _load(res / "daily_brief.json")
            R.add("G1", "MUST", "매일 브리핑: daily_brief.json 있음 (python -m ytflow daily)", db is not None, "01_research/daily_brief.json")
            intro_txt = " ".join(b.get("say", "") for s in spec.get("scenes", [])[:2] for b in s.get("beats", []))
            R.add("G4", "MUST", "매일 브리핑: 첫 두 장면 안에 기준 시각('○일 마감 기준' / '○시 기준') — 인트로 없이 (README §2-1)", "기준" in intro_txt, "")
            if ch == "ch-market-daily":
                fs = (res / "factsheet.md").read_text(encoding="utf-8") if (res / "factsheet.md").exists() else ""
                kinds = [k for k in ("이슈", "보고서", "전망", "실적") if k in fs]
                R.add("G3", "MUST", "매일 시장: 이야기마다 원인 종류(이슈·보고서·전망·실적)와 1차 출처를 팩트시트에", bool(kinds) and "http" in fs, kinds)
                # v26 (03 §0-2, 2026-11-15 사용자): 뻔한 사실 말고 자료를 엮어야 보이는 것 — 자료 지도·말과 행동·매체 프레임
                deep = path.name.endswith(("-analysis", "-weekly", "-review")) or str(tb.get("depth", "")).startswith("심층")
                lvl = "MUST" if deep else "SHOULD"

                def _rows(head):
                    m_ = re.search(r"^## " + head + r"[^\n]*\n(.*?)(?=^## |\Z)", fs, re.S | re.M)
                    rows_ = [ln for ln in (m_.group(1).splitlines() if m_ else []) if ln.strip().startswith("|") and not re.match(r"^\|\s*-", ln.strip())]
                    return [[c.strip() for c in ln.strip().strip("|").split("|")] for ln in rows_[1:]]   # 첫 줄은 머리
                R.add("G1", lvl, "v26: topic_brief 에 known(이미 알려진 것)·new_angle(자료를 엮어야 보이는 것) — 제목·훅은 new_angle 에서 (03 §0-2)",
                      bool(tb.get("known")) and bool(tb.get("new_angle")), (tb.get("new_angle") or "")[:40])
                amap = _rows("자료 지도")
                kinds_ = {k: sum(1 for r_ in amap if any(k in c for c in r_[:3])) for k in ("보고서", "발언", "행동")}
                meant = all(len(r_) >= 5 and r_[4] not in ("", "-") for r_ in amap)
                # v38: 원리(서로 다른 종류의 자료를 맞대 의미를 찾음)는 lvl, 분량은 참고 — 보고서가 없는 주제에 칸 채우기를 막음
                R.add("G3", lvl, "v26: 팩트시트 '## 자료 지도' — 서로 다른 종류(보고서·발언·행동)를 맞대고, 자료마다 의미 칸 (03 §0-2)",
                      len(amap) >= 2 and sum(1 for v in kinds_.values() if v) >= 2 and meant, f"{len(amap)}줄 {kinds_} 의미{'✓' if meant else '빈칸'}")
                R.add("G3", "참고", "v26: 자료 지도 분량 (종류별 줄 수)", len(amap) >= 6 and all(v >= 2 for v in kinds_.values()), f"{len(amap)}줄 {kinds_}")
                if path.name.endswith(("-weekly", "-review")):   # 2026-11-15 사용자: 매주 다음 주 일정·실적 브리핑·분석 (manual/09 §2)
                    sched = _rows("다음 주 일정")
                    has_earn = any("실적" in " ".join(r_) for r_ in sched)
                    R.add("G3", "MUST", "주간: 팩트시트 '## 다음 주 일정' — 한국 시간·볼 것·출처가 있는 지표·실적 일정 (manual/09 §2)", len(sched) >= 1, f"{len(sched)}줄 · 실적 {'있음' if has_earn else '없음'}")
                # v33 머니크루 수준의 깊이 (03 §0-4, docs/31)
                calc_m = re.search(r"^## 직접 계산[^\n]*\n(.*?)(?=^## |\Z)", fs, re.S | re.M)
                wrong_m = re.search(r"^## 틀리는 경우[^\n]*\n(.*?)(?=^## |\Z)", fs, re.S | re.M)
                sig_m = re.search(r"^## 신호[^\n]*\n(.*?)(?=^## |\Z)", fs, re.S | re.M)
                n_calc = len(re.findall(r"^\s*[-|*]\s*\S.*[=×÷→]", calc_m.group(1), re.M)) if calc_m else 0
                n_wrong = len(re.findall(r"^\s*(?:[-*]|\d+[.)])\s*\S", wrong_m.group(1), re.M)) if wrong_m else 0
                n_sig = len([ln for ln in (sig_m.group(1).splitlines() if sig_m else []) if re.search(r"\d", ln) and re.search(r"(?:[-*]|\d+[.)]|\|)\s*\S", ln)])
                R.add("G3", lvl, "v33: 팩트시트 '## 직접 계산' 1개+ (식·출처 숫자) — 연결 비율·민감도 (03 §0-4)", n_calc >= 1, f"{n_calc}개")
                # v38: 있어야 하는 것은 lvl, 셋을 채우는 것은 참고 — 약한 것을 채워 넣지 않게
                R.add("G3", lvl, "v33: 팩트시트 '## 틀리는 경우' — 이 판단이 틀리는 조건 (03 §0-4)", n_wrong >= 1, f"{n_wrong}개")
                R.add("G3", lvl, "v33: 팩트시트 '## 신호' — 숫자 기준선·날짜가 있는 확인 신호 (03 §0-4)", n_sig >= 1, f"{n_sig}개")
                R.add("G3", "참고", "v33: 틀리는 경우·신호 개수", n_wrong >= 3 and n_sig >= 3, f"틀림 {n_wrong} · 신호 {n_sig}")
                hub = tb.get("hub_event") or {}
                no_hub = isinstance(hub, str) and hub.strip().startswith("없음") and len(hub.strip()) > 4   # v38: 흔든 사건이 없는 기간은 "없음: 이유" — 지어내지 않음
                R.add("G1", lvl, "v28: topic_brief hub_event — 시장을 흔든 사건이 있으면 중심축, 없으면 '없음: 이유' (03 §0-3)", bool(hub), str(hub.get("name", ""))[:40] if isinstance(hub, dict) else str(hub)[:40])
                if not no_hub:
                    R.add("G3", lvl, "v28: 팩트시트 '## 파급 경로'·'## 주의할 점' (03 §0-3)", "## 파급 경로" in fs and "## 주의할 점" in fs, "")
                if spec.get("scenes") and isinstance(hub, dict) and hub.get("keyword"):
                    head_say = " ".join(b.get("say", "") for s_ in _opening(spec) for b in s_.get("beats", []))
                    R.add("G4", lvl, "v28: 여는 부분에 중심 사건 (03 §0-3)", hub["keyword"] in head_say, hub["keyword"])
                media = _rows("매체 프레임")
                R.add("G3", lvl, "v26: 팩트시트 '## 매체 프레임' — 매체끼리 어떻게 다르게 읽었나 (제목·강조점·빠진 것, 03 §0-2)", len(media) >= 2, f"{len(media)}곳")
                R.add("G3", "참고", "v26: 매체 프레임 범위 (국내·해외를 함께 보면 프레임 차이가 더 잘 보임)", len(media) >= 4, f"{len(media)}곳")
                mhead = re.search(r"^## 매체 프레임[^\n]*\n(?:[^|\n][^\n]*\n)*?(\|[^\n]*)", fs, re.M)
                R.add("G3", lvl, "v28: 매체 프레임에 '입장' 칸 (낙관·우려·중립, 03 §0-3)", bool(mhead and "입장" in mhead.group(1)), "")
                if spec.get("scenes"):
                    says_m = " ".join(b.get("say", "") for s_ in spec["scenes"] for b in s_.get("beats", []))
                    R.add("G4", lvl, "v26: 대본에 매체가 어떻게 다뤘나 + 말과 행동 맞대기 (03 §0-2)",
                          any(s_.get("type") == "newspapers" for s_ in spec["scenes"]) or ("매체" in says_m and ("보도" in says_m or "기사" in says_m)), "")
                # v36 (manual/09 §3-4·§3-5, 2026-11-17 사용자: "여러 인사이트들 … 부실" · "인터뷰·방송 내용을 영상소스로") — 11/18 회차부터
                if path.name[:8].isdigit() and path.name[:8] >= "20261118":
                    ins = _rows("인사이트")
                    st_ = {k for r_ in ins for k in ("낙관", "우려", "중립") if any(k in c for c in r_)}
                    dom = any(any("국내" in c for c in r_) for r_ in ins)
                    abroad = any(any("해외" in c for c in r_) for r_ in ins)
                    R.add("G3", "MUST", "v36: 팩트시트 '## 인사이트' — 이름·직함 있는 사람·매체의 엇갈리는 해석(입장이 갈림), 원문·근거·출처 (09 §3-4)",
                          len(ins) >= 2 and len(st_) >= 2, f"{len(ins)}줄 · 입장 {sorted(st_)} · 국내 {'✓' if dom else '✗'} 해외 {'✓' if abroad else '✗'}")
                    vm = re.search(r"^## 영상 소스[^\n]*\n(.*?)(?=^## |\Z)", fs, re.S | re.M)
                    vrows = _rows("영상 소스")
                    R.add("G3", "MUST", "v36: 팩트시트 '## 영상 소스' — 인터뷰·방송 원본 후보 1줄+ (못 찾으면 '없음: 이유') (09 §3-5)",
                          bool(vrows) or bool(vm and "없음" in vm.group(1)), f"{len(vrows)}줄")
                    ceo = _rows("CEO 소식")
                    R.add("G3", "SHOULD", "v42: 팩트시트 '## CEO 소식' — 오늘 이야기와 이어지는 경영진의 말·행동 1줄+, 원문·공시 출처 (09 §3-4-2)", len(ceo) >= 1, f"{len(ceo)}줄")
                    if spec.get("scenes"):
                        n_ins = sum(1 for s_ in spec["scenes"] if s_.get("insight"))
                        R.add("G4", "MUST", "v36: 대본에 인사이트 장면 (\"insight\": true — 화면에 '의견' 표시, 사실과 구분) (09 §3-4)", n_ins >= 1, f"{n_ins}개")
                        R.add("G4", "참고", "v36: 인사이트 분량 — 사람·매체의 해석을 넉넉히 다뤘나, 국내·해외를 함께 봤나", n_ins >= 2 and dom and abroad, f"장면 {n_ins} · 팩트시트 {len(ins)}줄 · 국내 {'✓' if dom else '✗'} 해외 {'✓' if abroad else '✗'}")
                        R.add("G4", "SHOULD", "v36: 매체·인물의 원본 발언 장면(bite) 1개+ — 원본이 없으면 인용 카드로 그려짐 (09 §3-5)",
                              any(s_.get("type") == "bite" for s_ in spec["scenes"]), "")
        if ch == "ch-market-daily" and spec.get("scenes"):   # v27 (manual/09 §6, 2026-11-15 사용자: "말은 많은데 45일·60일만 강조된 채 멈춰 있다")
            def _nums(s_):
                return {re.sub(r"[,\s]", "", m_) for m_ in re.findall(r"\d[\d,]*(?:\.\d+)?", s_)}
            bare = []
            for s_ in spec["scenes"]:
                if s_.get("type") in ("chapter", "kinetic", "outro", "intro"):
                    continue
                shown = _nums(json.dumps({k_: v_ for k_, v_ in s_.items() if k_ not in ("beats", "label", "id", "chapter")}, ensure_ascii=False))
                for k_, b_ in enumerate(s_.get("beats", [])):
                    if b_.get("motion") or b_.get("reveal") or b_.get("upto") or b_.get("show_result") or b_.get("show"):
                        continue
                    extra = _nums(b_.get("say", "")) - shown
                    if len(extra) >= 2:
                        bare.append(f"{s_.get('id')}-{k_ + 1}")
            R.add("G4", "MUST", "v27: 말로 숫자를 늘어놓는 순간 화면이 따라 바뀜 — 말은 많은데 화면이 멈춘 박자 없음 (manual/09 §6)", not bare, bare[:8])
        if ch == "ch-market-daily":   # 2026-11-15 사용자: 제목·썸네일에 채널 이름 붙이지 않음, 날짜만 (manual/09 §7)
            pk_ = spec.get("package") or {}
            txts_ = [pk_.get("title", "")] + list(pk_.get("title_options") or []) + [" ".join([th.get("top", ""), *th.get("lines", []), th.get("sub", ""), th.get("headline", "")]) for th in pk_.get("thumbnails") or []]
            named_ = [x[:30] for x in txts_ if "이어 읽는 시장" in x or "이어읽는시장" in x]
            R.add("G6", "MUST", "제목·썸네일에 채널 이름(이어 읽는 시장) 없음 — 날짜만 (manual/09 §7)", not named_, named_[:2])
        if brand == "market":
            tail = [s.get("type") for s in spec.get("scenes", [])[-3:]]
            R.add("G4", "SHOULD", "market: 끝에 확인할 신호(checklist)", "checklist" in tail, tail)

    if brand == "issues" and last >= 3:   # 시사 채널 전용 (manual/08-issues.md §6)
        R.add("G4", "MUST", "issues: 사실 기준 시각(as_of)", bool(tb.get("as_of")), tb.get("as_of", ""))
        sides = [x for x in tb.get("sides") or [] if x.get("source")]
        R.add("G4", "MUST", "issues: 서로 다른 입장 2개 이상(각 출처)", len(sides) >= 2, len(sides))
        txt_all = _texts(spec)
        R.add("G4", "MUST", "issues: 대본에 '기준' 시점 언급", "기준" in txt_all, "")
        bad = [w for w in ISSUE_BANNED if w in txt_all]
        R.add("G4", "MUST", "issues: 단정·비하 금지어 없음", not bad, bad)
        fs2 = _load(res / "factsheet.md") or ""
        links2 = set(re.findall(r"https?://[^\s)>\]]+", fs2))
        doms = {re.sub(r"^https?://(www\.)?", "", u).split("/")[0] for u in links2}
        R.add("G3", "MUST", "issues: 교차 확인 — 당사자 원문과 성향이 다른 매체 등 서로 다른 출처 (08 §2)", len(doms) >= 3, f"{len(links2)}개 / {len(doms)}곳")
        R.add("G4", "SHOULD", "issues: 모르는 것(unknowns) 말하기", bool(tb.get("unknowns")) and "확인되지 않" in txt_all, "")
        voice_sc = [x for x in spec.get("scenes", []) if x.get("type") == "quote" or any(bb.get("lower") for bb in x.get("beats", []))]
        R.add("G4", "SHOULD", "issues: 사람의 목소리 장면 1개 이상 (quote·이름 자막)", bool(voice_sc), len(voice_sc))
        says = [bb.get("say", "") for x in spec.get("scenes", []) for bb in x.get("beats", [])]
        asks = sum(t.count("?") for t in says)
        formal = sum(any(w in t for w in ("것으로 알려졌다", "것으로 전해졌다", "것으로 나타났다")) for t in says)
        R.add("G4", "참고", "issues: 보도문 말투('~것으로 알려졌다')·물음 개수 — 딱딱한 나열·반복 질문 패턴이 아닌지 (11-workflow §3-2)",
              formal <= max(1, len(says) // 10), f"물음 {asks} · 보도문 {formal}/{len(says)}")
        R.add("G1", "SHOULD", "issues: 이름 붙은 시리즈(series)", bool(tb.get("series")), tb.get("series", ""))
        qd = [x["dur"] for x in tl if x.get("type") == "quote"]
        if len(qd) >= 2:
            R.add("G5", "참고", "issues: 양쪽 입장 장면 길이 (같은 무게로 보이는지 눈으로)", min(qd) / max(qd) >= 0.7, [round(x, 1) for x in qd])
    if last >= 3:  # v24 인트로 없음 (README §2-1) · 말투 (README §2-3, 미주일기식)
        sc0 = spec.get("scenes", [])[:1]
        _all = [b.get("say", "") for s in spec.get("scenes", []) for b in s.get("beats", [])]
        greet = [t for t in _all if re.search(r"안녕하세요|구독과 좋아요|구독 ?좋아요|이런 순서로|순서로 (가|따라가) 보겠습니다|시작해 보겠습니다", t)]
        R.add("G4", "MUST", "인트로 없음: 첫 장면이 intro 가 아니고 인사·채널 소개·순서 예고·구독 부탁 없음 (README §2-1)",
              not any(x.get("type") == "intro" for x in sc0) and not greet, [g[:30] for g in greet[:2]])
        bad = [m.group(0) for t in _all for m in re.finditer(r"헐|대박|미쳤|ㅋ|계시죠\?|손을 (한번 )?펴 보세요|부를게요|여러분!", t)]
        R.add("G4", "SHOULD", "말투: 말 걸기·감탄 표현 없음 (README §2-3, 참고용)", not bad, bad[:3])
        sents = [x for t in _all for x in re.split(r"(?<=[.?!])\s+", t) if len(x.strip()) > 3]
        formal = sum(1 for x in sents if re.search(r"(습니다|니다|까요)[.?!]?$", x.strip()))
        avg = sum(len(x) for x in sents) / max(len(sents), 1)
        if brand == "curiosity":   # v38: 어미 비율은 이야기형(호기심)만 — 정보 채널은 어미 혼합 (11-workflow §3-2, 2026-11-17 사용자)
          R.add("G4", "참고", "말투(호기심): '~습니다/~니다' 끝맺음 몫·평균 문장 길이 (차분한 이야기 내레이터인지)",
              formal / max(len(sents), 1) >= 0.8 and avg >= 35, f"{formal / max(len(sents), 1):.0%} · {avg:.0f}자")
    if last >= 6 and longform:  # v24 길이: 롱폼 최소 10분 (README §2-4)
        tl_ = Path(path) / "05_edit" / "hybrid_timeline.json"
        tot_ = sum(x.get("dur", 0) for x in json.loads(tl_.read_text(encoding="utf-8"))) if tl_.exists() else 0
        quick_ = spec.get("format") == "quick"   # 시사 48시간 안 빠른 정리 (08 §1, v34): 5~8분 예외
        min_ = 300 if quick_ else 600
        R.add("G6", "MUST", f"길이: {'빠른 정리 5분' if quick_ else '롱폼 10분'} 이상 — 많이 짧으면 쇼츠로 (README §2-4)", tot_ >= min_, f"{tot_ / 60:.1f}분")
    if last >= 4:  # G5 연출
        from . import backdrop
        bgs = backdrop.plan(spec)
        kinds = set(bgs)
        R.add("G5", "SHOULD", "배경: 한 가지 바탕으로 고정하지 않음 — 장면이 하는 일이 바뀌면 바탕도 바뀜 (05 §0-2)",
              len(kinds) >= 2, sorted(kinds))
        runs = [bgs[i] for i in range(len(bgs) - 2) if bgs[i] != "film" and bgs[i] == bgs[i + 1] == bgs[i + 2]]
        R.add("G5", "참고", "배경: 같은 바탕이 이어지는 구간", not runs, runs)
        from . import stylepick as _sp
        vs = _sp.variety_stats(spec)
        R.add("G5", "참고", "반복 피로: 글씨·도형뿐인 장면이 이어지는 구간 — 자료·지도·그림으로 보여 줄 수 있는지 다시 볼 곳 (05 §0-3)",
              vs["plain_run"] <= 2, f"최장 {vs['plain_run']}연속 (장면 {vs['plain_run_at']})")
        deco = [s.get("id") for s in spec.get("scenes", []) if set(s.get("fx") or []) & {"dust", "leak"}]
        R.add("G5", "참고", "장식 효과(dust·leak)를 쓴 장면 — 내용이 담긴 볼거리 대신 쓰지 않았는지 (05 §0-4)", len(deco) <= 2, deco)
        R.add("G5", "참고", "반복 피로: 볼거리(자료·지도·그림)가 있는 장면의 몫", vs["ratio"] >= 0.6, f"{vs['hooked']}/{vs['n']}")
        R.add("G5", "참고", "반복 피로: 같은 시각 효과가 이어지는 구간 (효과 종류 수는 채우지 않음 — 05 §0-5)",
              not vs["fx_runs"], f"{vs['fx_kinds']} 연속 {vs['fx_runs']}")
        # 바탕색 돌려 쓰기 (v13): 미색 종이 계열만 계속 쓰지 않기 — 직전 두 프로젝트와 같은 바탕 계열이면 경고
        try:
            from . import skin as _skin
            def _fam(sid):
                b = _skin.load(sid).get("palette", {}).get("base") or "#F3EFE6"
                r, g, bb = (int(b.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
                if r + g + bb < 300: return f"dark:{sid}"
                return "cream" if r - bb > 12 else f"light:{sid}"
            cur = _fam((ed.get("edit") or {}).get("skin", "paper-sketch"))
            prevs = []
            for q in sorted(Path(path).parent.iterdir()):
                if q.name < Path(path).name and (q / "edit.yaml").exists() and (q / "05_edit" / "final.mp4").exists():
                    prevs.append(_fam(((yaml.safe_load((q / "edit.yaml").read_text(encoding="utf-8")) or {}).get("edit") or {}).get("skin", "paper-sketch")))
            last2 = prevs[-2:]
            R.add("G5", "SHOULD", "바탕색 돌려 쓰기: 직전 두 편과 같은 바탕 계열(특히 미색 종이)이 아님 (05 §0-6)",
                  not (len(last2) == 2 and all(x == cur for x in last2)), f"이번 {cur} · 직전 {last2}")
        except Exception:
            pass
        if spec.get("scenes"):   # v15 카테고리 개성 (05 §0-7)
            R.add("G5", "SHOULD", "v15: 카테고리 개성 — hybrid.json 에 brand (장 표지·인과 지도·듀오톤이 카테고리답게)",
                  bool(spec.get("brand") or any(s.get("brand") for s in spec["scenes"])), spec.get("brand", ""))
            fo = spec.get("footage") or {}
            keys = list(fo)
            covers = [s.get("bg_src") or (keys[(int(s.get("chapter", 1) or 1) - 1) % len(keys)] if keys and not s.get("look") else None)
                      for s in spec["scenes"] if s.get("type") == "chapter"]   # 대본에 없으면 렌더러가 고르는 것(edit10.prepare)과 같게
            covers = [c for c in covers if c]
            nasa = [c for c in covers if "NASA" in (fo.get(c, {}).get("credit") or "")]
            R.add("G5", "SHOULD", "v15: 장 표지 사진은 주제에 맞게 — 같은 사진 두 번·NASA 사진 2장 이상 없음",
                  len(covers) == len(set(covers)) and len(nasa) <= 1, f"표지 {covers} · NASA {len(nasa)}")
        prev = _prev_episode_signature(path, spec)
        if prev is not None:
            cur = set(vs["signature"])
            jac = len(cur & prev) / max(1, len(cur | prev))
            R.add("G5", "참고", "반복 피로: 같은 채널 직전 편과 화면 구성이 얼마나 겹치나", jac <= 0.7, f"{jac:.0%}")
        types = [s.get("type") for s in spec.get("scenes", [])]
        run3 = [types[i] for i in range(len(types) - 2) if types[i] == types[i + 1] == types[i + 2] and types[i] != "chapter"]
        R.add("G5", "참고", "같은 장면 type 이 이어지는 구간 — 하는 일이 바뀌었는데 화면이 같지 않나", not run3, run3)
        tl = _load(edt / "hybrid_timeline.json") or []
        if tl:
            t, last_f, gap, chap, last_c, cgap = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
            for s in tl:
                if s.get("type") in FOOTAGE_TYPES:
                    gap = max(gap, t - last_f)
                    last_f = t + s["dur"]
                if s.get("type") in ("chapter", "card_type"):
                    cgap = max(cgap, t - last_c)
                    last_c = t
                t += s["dur"]
            gap, cgap = max(gap, t - last_f), max(cgap, t - last_c)
            R.add("G5", "참고", "자료 화면 없이 그래픽만 이어지는 가장 긴 구간", gap <= 45, f"최장 {gap:.0f}초")
            R.add("G5", "참고", "장 전환 없이 이어지는 가장 긴 구간", not longform or cgap <= 200, f"최장 {cgap:.0f}초")
        skin = (ed.get("edit") or {}).get("skin", "paper-sketch")
        from . import stylepick
        ms = stylepick.mix_stats(spec, tl)
        rule = stylepick.MIX_RULES["longform" if longform else "shorts"]
        bb = bool(ms.get("backbone"))   # 뼈대 스타일(무대·이야기 그림판) 영상은 한 스타일이 이끄는 것이 정상
        R.add("G5", "SHOULD", "스타일 조합: 한 스타일로만 만들지 않음 — 장면이 하는 일에 맞춰 섞음 (05 §0-1)", ms["n_recipes"] >= 2,
              f"{ms['n_recipes']}종 {ms['recipes']}")
        cap = 0.85 if bb else rule["max_share"]
        R.add("G5", "참고", "스타일 조합: 가장 많이 쓴 스타일의 몫·겹친 장면·같은 스타일 연속" + (" (뼈대 스타일 영상)" if bb else ""),
              ms["top_share"] <= cap and (bb or (ms["layered_scenes"] >= rule["min_layered"] and ms["max_run"] <= rule["max_run"])),
              f"{ms['top']} {ms['top_share']} · 겹침 {ms['layered_scenes']} · 최장 연속 {ms['max_run']}")
        total = sum(x["dur"] for x in tl) if tl else 5.0 * sum(len(x.get("beats", [])) for x in spec.get("scenes", []))
        es = stylepick.emphasis_stats(spec, total)
        R.add("G5", "참고", "강조 횟수·강조가 겹친 장면 — 기억할 숫자·반전·결론에만 썼는지 (05 §0-1)", es["count"] <= es["limit"] and not es["crowded"],
              f"{es['count']}번 {es['items']} · 겹친 장면 {es['crowded']}")
        R.add("G5", "SHOULD", "핵심 단어 띄우기에 문장을 쓰지 않음 — 자막과 같은 내용을 위에 반복하지 않음 (v3)", not es["bad_words"], es["bad_words"])
        rec = stylepick.skins_for(brand) if brand else set()
        R.add("G5", "SHOULD", "그래픽 팩이 브랜드에 맞는 스타일 등록부 안 (styles/recipes)", not rec or skin in rec, f"{skin} / 등록부 {sorted(rec)}")
        sp = path / "01_research" / "style_pick.json"
        R.add("G5", "SHOULD", "style-pick 기록 (상황에 맞춘 스타일 선택)", sp.exists(), "python -m ytflow style-pick <프로젝트>")
        ep = path / "02_script" / "EDIT_CONTEXT.md"   # 메인 → 주제 레포 → 이 영상 (docs/33)
        R.add("G5", "SHOULD", "edit-plan 기록 (메인·주제 레포에서 이 영상의 상황별 장면·기법을 채움)", ep.exists(),
              "python -m ytflow edit-plan <프로젝트> → 02_script/EDIT_CONTEXT.md")

    if last >= 5:  # G6 완성본
        R.add("G6", "MUST", "final.mp4", (edt / "final.mp4").exists(), "")
        lq = _load(path / "04_assets" / "layout_qa.json")
        _soft = ("stage/crowded", "stage/text", "stage/static")   # v38: 숫자로 감지하는 '붐빔·글자 수·정지'는 참고 — 판단은 D3 화면 확인
        def _split(v):
            v = v if isinstance(v, list) else [v] if v else []
            return [x for x in v if not str(x).startswith(_soft)], [x for x in v if str(x).startswith(_soft)]
        hard, soft = {}, {}
        if isinstance(lq, dict):
            for k, v in lq.items():
                h_, s_ = _split(v)
                if h_: hard[k] = h_
                if s_: soft[k] = s_
        elif isinstance(lq, list):
            h_, s_ = _split(lq)
            if h_: hard["all"] = h_
            if s_: soft["all"] = s_
        R.add("G6", "MUST", "레이아웃 결함 없음 (겹침·잘림·대비·장면 의도 goal/why)", lq is not None and not hard, hard)
        R.add("G6", "참고", "무대 화면: 한꺼번에 보이는 것·글자·멈춘 박자 (한 화면 한 생각인지 눈으로, 04 §0-5)", not soft, soft)
        sq = _load(edt / "sync_qa.json") or {}
        w5 = sq.get("within_0_5s")
        w5_ok = w5 >= 0.95 if w5 is not None else (sq.get("p95_abs_offset") or 9) <= 0.5  # 예전 기록은 p95 로 판정
        ok = w5_ok and abs(sq.get("video_minus_audio_s", 9)) <= 0.1 and (sq.get("median_abs_offset") or 9) <= 0.2
        R.add("G6", "MUST", "싱크 (0.5초 안 ≥95%, 화면−소리 ≤0.1초, 중앙값 ≤0.2초)", ok,
              {k: sq.get(k) for k in ("within_0_5s", "p95_abs_offset", "median_abs_offset", "video_minus_audio_s")})
        dc = _load(edt / "delivery_check.json") or {}
        R.add("G6", "SHOULD", "납품 점검(음량 등)", dc.get("status") == "completed", dc.get("status"))
        mo = _load(edt / "motion.json") or {}
        if mo:  # 완성본을 실제로 잰 움직임 (docs/19 A4) — 대본에 효과를 적은 것만으로는 통과 못 함
            R.add("G6", "참고", "움직임: 화면 변화·정지 화면 몫 (완성본 측정 — 정신없지도 멈춰 있지도 않은지 눈으로, README §2-5)",
                  mo.get("change_events_per_min", 0) >= 8 and mo.get("static_ratio", 1) <= 0.5,
                  f"변화 {mo.get('change_events_per_min')}/분 · 정지 {mo.get('static_ratio')}")
            if brand == "curiosity":   # v25 (2026-11-14 사용자: "사진을 잘 뽑은 정적인 동영상 같다 — 동적인 움직임을 살려라", README §2-5)
                R.add("G6", "참고", "curiosity 움직임: 정지 화면 몫 (사진 슬라이드처럼 멈춰 보이지 않는지 — 숫자를 맞추려 화면을 흔들지 않음)", mo.get("static_ratio", 1) <= 0.3, f"정지 {mo.get('static_ratio')}")
        el = any((path / "03_voice").glob("el*")) or any((path / "03_voice").glob("*eleven*"))
        try:
            el = el or (config.channel(ch).get("tts") or {}).get("backend") == "elevenlabs"
        except Exception:
            pass
        R.add("G6", "SHOULD", "최종 목소리 ElevenLabs", el, "")

    if last >= 6:  # G7 포장
        pk = spec.get("package") or {}
        R.add("G7", "MUST", "제목 후보 3개 + 이유", len(pk.get("title_options") or []) >= 3 and len(pk.get("title_why") or []) >= 3, "")
        tq = _load(edt / "thumbnail_qa.json") or {}
        R.add("G7", "MUST", "썸네일 A/B/C + 점검 ok",
              all((edt / f"thumbnail_{k}.png").exists() and (tq.get(k) or {}).get("ok") for k in "ABC"), "")
        title = pk.get("title", "")
        R.add("G7", "참고", "제목 앞부분에 질문·핵심 (목록에서 잘려도 무슨 영상인지 보이게)", bool(re.search(r"[?？]|왜|까", title[:22])), title[:22])

    if last >= 7:  # G8 보관
        R.add("G8", "MUST", "GitHub Release 업로드", (edt / "release.json").exists(), "")
        epi = config.CHANNELS_DIR / ch / "episodes.md"
        R.add("G8", "MUST", "episodes.md 기록", epi.exists() and path.name in epi.read_text(encoding="utf-8"), ch)

    return R


def write(path: Path, R: Report) -> Path:
    out = path / "05_edit"
    out.mkdir(parents=True, exist_ok=True)
    mf = R.must_fail()
    meta = {"project": path.name, "manual_version": manual_version(), "checked": dt.datetime.now().isoformat(timespec="seconds"),
            "pass": not mf, "rows": R.rows}
    (out / "checklist.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    lines = [f"# 체크리스트 — {path.name}", "",
             f"매뉴얼 v{meta['manual_version']} · {meta['checked']} · **{'통과' if meta['pass'] else f'MUST 실패 {len(mf)}개'}**", "",
             "| 게이트 | 등급 | 항목 | 결과 | 내용 |", "|---|---|---|---|---|"]
    for r in R.rows:
        mark = "✅" if r["ok"] else ("❌" if r["level"] == "MUST" else "ℹ️" if r["level"] == "참고" else "⚠️")
        lines.append(f"| {r['gate']} | {r['level']} | {r['item']} | {mark} | {r['detail'][:80].replace('|', '/')} |")
    lines += ["", "**참고**(ℹ️)는 실패가 아니라 측정값입니다 — 숫자를 맞추지 말고, 표시된 곳이 그 연출의 원리(manual/05 §0-0)에 맞는지 화면 확인(D3)에서 봅니다.",
              "사람 눈 검사(EYE)는 manual/06-checklist.md 끝의 5가지를 확인하세요."]
    (out / "checklist.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out / "checklist.md"


# ------------------------------------------------------------------ 사용자 검토 → 매뉴얼에 쌓기
def review(path: Path, passed: bool, reason: str = "") -> None:
    MANUAL.mkdir(exist_ok=True)
    rv = MANUAL / "reviews.md"
    if not rv.exists():
        rv.write_text("# 검토 기록 — 통과하면 그 매뉴얼 버전을 그대로, 기각하면 기준을 고쳐 다음 버전으로\n\n"
                      "| 날짜 | 프로젝트 | 매뉴얼 | 결과 | 사유·메모 |\n|---|---|---|---|---|\n", encoding="utf-8")
    today = dt.date.today().isoformat()
    ver = manual_version()
    with rv.open("a", encoding="utf-8") as f:
        f.write(f"| {today} | {path.name} | v{ver} | {'통과' if passed else '기각'} | {reason.replace('|', '/')} |\n")
    if not passed:
        cl = MANUAL / "CHANGELOG.md"
        s = cl.read_text(encoding="utf-8")
        item = f"- [{today} · {path.name} 기각] {reason}"
        s = s.replace("## 반영 대기\n", f"## 반영 대기\n{item}\n", 1) if "## 반영 대기\n" in s else s + f"\n## 반영 대기\n{item}\n"
        cl.write_text(s, encoding="utf-8")
        print(f"[review] 기각 기록 → manual/CHANGELOG.md '반영 대기'. 매뉴얼을 고친 뒤 python -m ytflow manual-bump \"요약\"")
    else:
        st = path / "state.json"
        d = json.loads(st.read_text(encoding="utf-8")) if st.exists() else {}
        d["reviewed"] = {"result": "pass", "date": today, "manual_version": ver}
        st.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[review] 통과 기록 (매뉴얼 v{ver} 그대로 유지)")


def bump(summary: str, tag: bool = True) -> str:
    ver = str(int(manual_version() or 0) + 1)
    today = dt.date.today().isoformat()
    cl = MANUAL / "CHANGELOG.md"
    s = cl.read_text(encoding="utf-8")
    pend = pending_changes()
    body = f"## v{ver} — {today}\n- {summary}\n" + "".join(f"  - 반영: {p}\n" for p in pend)
    m = re.search(r"## 반영 대기\n.*?(?=\n## |\Z)", s, re.S)
    if m:
        s = s[:m.start()] + "## 반영 대기\n\n" + body + s[m.end():]
    else:
        s = s.rstrip() + "\n\n## 반영 대기\n\n" + body
    cl.write_text(s, encoding="utf-8")
    (MANUAL / "VERSION").write_text(ver + "\n", encoding="utf-8")
    print(f"[manual] v{ver}: {summary} (반영 {len(pend)}건)")
    if tag:
        print(f"  커밋 후: git push origin HEAD:refs/heads/manual/v{ver}")
    return ver


def _prev_episode_signature(path, spec):
    """같은 채널(edit.yaml 의 channel)의 직전 프로젝트 화면 구성 (type·효과 집합). 없으면 None."""
    import yaml
    from . import stylepick as _sp
    root = Path(path).parent
    try:
        ch = (yaml.safe_load((Path(path) / "edit.yaml").read_text(encoding="utf-8")) or {}).get("channel")
    except Exception:
        return None
    best = None
    for p in sorted(root.iterdir()):
        if p == Path(path) or p.name >= Path(path).name or not (p / "edit.yaml").exists():
            continue
        try:
            if (yaml.safe_load((p / "edit.yaml").read_text(encoding="utf-8")) or {}).get("channel") != ch:
                continue
            sp = json.loads((p / "02_script" / "hybrid.json").read_text(encoding="utf-8"))
        except Exception:
            continue
        best = set(_sp.variety_stats(sp)["signature"])
    return best
