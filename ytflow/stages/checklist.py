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

    # G1 주제
    tb = _load(res / "topic_brief.json")
    R.add("G1", "MUST", "topic_brief.json 있음", tb is not None, "01_research/topic_brief.json (schemas/topic_brief.schema.json)")
    tb = tb or {}
    R.add("G1", "MUST", "브랜드(ai/market/curiosity)", brand in BRANDS, brand or "edit.yaml 채널에 brand 없음")
    R.add("G1", "MUST", "욕망·시청자 질문", tb.get("desire") and tb.get("viewer_question"), tb.get("viewer_question", ""))
    R.add("G1", "MUST", "트리거·왜 지금", tb.get("trigger") and tb.get("why_now"), tb.get("trigger", ""))
    sc = tb.get("score") or {}
    tot = sum(int(v) for v in sc.values() if isinstance(v, (int, float)))
    R.add("G1", "MUST", "욕망 점수 ≥12, 욕망 강도·보여 줄 자료 ≥2",
          tot >= 12 and sc.get("desire", 0) >= 2 and sc.get("visuals", 0) >= 2, f"합계 {tot} {sc}")
    R.add("G1", "MUST", "수요 증거 1개 이상", len(tb.get("demand_evidence") or []) >= 1, len(tb.get("demand_evidence") or []))
    R.add("G1", "SHOULD", "후보 3개 비교 기록", len(tb.get("candidates") or []) >= 3, len(tb.get("candidates") or []))
    R.add("G1", "SHOULD", "우리만의 답(our_angle)", bool(tb.get("our_angle")), tb.get("our_angle", ""))
    drv = tb.get("driver") or {}
    R.add("G1", "MUST" if brand == "issues" else "SHOULD", "무엇이 띄우나(driver: 소재·각도·형식 + 근거)",
          drv.get("type") in ("소재", "각도", "형식") and bool(drv.get("why")) and (drv.get("type") != "각도" or bool(drv.get("angle"))),
          f"{drv.get('type', '')} · {drv.get('why', '')[:40]}")

    if last >= 1:  # G2 소스
        foot = spec.get("footage") or {}
        miss = [k for k, v in foot.items() if not (v.get("credit") and v.get("url"))]
        R.add("G2", "MUST", "자료 화면마다 credit·url", foot and not miss, f"{len(foot)}개, 빠짐 {miss}")
        bad = [k for k, v in foot.items() if any(b.lower() in (v.get("credit", "")).lower() for b in BAD_LICENSE)]
        R.add("G2", "MUST", "금지 라이선스(SA·NC·ND) 없음", not bad, bad)
        srcs = {v.get("url") for v in foot.values()}
        R.add("G2", "SHOULD", "자료 화면 소스 3종 이상 (롱폼)", not longform or len(srcs) >= 3, f"{len(srcs)}종")

    if last >= 2:  # G3 사실
        fs = _load(res / "factsheet.md") or ""
        links = set(re.findall(r"https?://[^\s)>\]]+", fs))
        R.add("G3", "MUST", "팩트시트 + 출처 링크 3개 이상", fs and len(links) >= (3 if longform else 1), f"링크 {len(links)}개")
        R.add("G3", "SHOULD", "확인 상태 표시(✅/⚠️)", "✅" in fs or "확인" in fs, "")
        R.add("G3", "SHOULD", "'쓰지 않는 것' 목록", "쓰지 않" in fs, "")

    if last >= 3:  # G4 대본
        txt = _texts(spec)
        R.add("G4", "MUST", "core_message·question·logic", all(spec.get(k) for k in ("core_message", "question", "logic")), "")
        cnt = {k: len(spec.get(k) or []) for k in ("compare_to", "analogies", "past_cases", "glossary")}
        need = {"compare_to": 1, "analogies": 2, "past_cases": 1, "glossary": 1}
        R.add("G4", "MUST", "비교 기준≥1·비유≥2·과거 사례≥1·풀이≥1", all(cnt[k] >= n for k, n in need.items()), cnt)
        inv = [w for w in INVEST if w in txt]
        R.add("G4", "MUST", "투자 권유 표현 0개", not inv, inv)
        ref = [w for w in REF_NAMES if w in txt]
        R.add("G4", "MUST", "레퍼런스 채널 이름 0개", not ref, ref)
        unf = [w for w in UNFINISHED if w in txt]
        R.add("G4", "MUST", "미완성 표시 0개", not unf, unf)
        hype = [w for w in HYPE if w in txt]
        R.add("G4", "SHOULD", "과장 단어 0개", not hype, hype)
        first = " ".join(b.get("say", "") for s in spec.get("scenes", [])[:3] for b in s.get("beats", []))
        R.add("G4", "SHOULD", "첫 3장면 안에 질문", "?" in first or "까요" in first or "일까" in first, "")
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
        R.add("G3", "MUST", "issues: 출처 링크 5개 이상·도메인 3곳 이상", len(links2) >= 5 and len(doms) >= 3, f"{len(links2)}개 / {len(doms)}곳")
        R.add("G4", "SHOULD", "issues: 모르는 것(unknowns) 말하기", bool(tb.get("unknowns")) and "확인되지 않" in txt_all, "")
        voice_sc = [x for x in spec.get("scenes", []) if x.get("type") == "quote" or any(bb.get("lower") for bb in x.get("beats", []))]
        R.add("G4", "SHOULD", "issues: 사람의 목소리 장면 1개 이상 (quote·이름 자막)", bool(voice_sc), len(voice_sc))
        says = [bb.get("say", "") for x in spec.get("scenes", []) for bb in x.get("beats", [])]
        asks = sum(t.count("?") for t in says)
        formal = sum(any(w in t for w in ("것으로 알려졌다", "것으로 전해졌다", "것으로 나타났다")) for t in says)
        R.add("G4", "SHOULD", "issues: 말하듯 쓴 대본 — 묻는 문장 3개+, 보도문 말투 10% 이하 (08 §0-1)",
              asks >= 3 and formal <= max(1, len(says) // 10), f"물음 {asks} · 보도문 {formal}/{len(says)}")
        R.add("G1", "SHOULD", "issues: 이름 붙은 시리즈(series)", bool(tb.get("series")), tb.get("series", ""))
        qd = [x["dur"] for x in tl if x.get("type") == "quote"]
        if len(qd) >= 2:
            R.add("G5", "SHOULD", "issues: 양쪽 입장 장면 길이 차 30% 이내", min(qd) / max(qd) >= 0.7, [round(x, 1) for x in qd])
    if last >= 3 and longform:  # v8: 본론 전 MC 오프닝
        sc0 = spec.get("scenes", [])[:2]
        intro = [x for x in sc0 if x.get("type") == "intro" and len(x.get("beats", [])) >= 3]
        R.add("G4", "MUST", "오프닝: 본론 전에 MC 오프닝(intro: 인사·오늘 이야기·순서 예고·시작 멘트, 3박자 이상)", bool(intro),
              "첫 2장면에 intro 없음" if not intro else "")
    if last >= 4:  # G5 연출
        from . import backdrop
        bgs = backdrop.plan(spec)
        kinds = set(bgs)
        R.add("G5", "MUST", "배경: 장면 목적에 맞춰 3종 이상 (한 가지 바탕만 쓰면 불합격, manual 05 §0-2)",
              not longform or len(kinds) >= 3, sorted(kinds))
        runs = [bgs[i] for i in range(len(bgs) - 2) if bgs[i] != "film" and bgs[i] == bgs[i + 1] == bgs[i + 2]]
        R.add("G5", "SHOULD", "배경: 같은 바탕 3장면 연속 없음 (film 제외)", not runs, runs)
        from . import stylepick as _sp
        vs = _sp.variety_stats(spec)
        R.add("G5", "MUST", "반복 피로: 글씨·도형뿐인 장면 3개 연속 금지 (눈요기: 자료·지도·사진 겹치기·시각 효과, 05 §0-3)",
              vs["plain_run"] <= 2, f"최장 {vs['plain_run']}연속 (장면 {vs['plain_run_at']})")
        deco = [s.get("id") for s in spec.get("scenes", []) if set(s.get("fx") or []) & {"dust", "leak"}]
        R.add("G5", "SHOULD", "v10: 장식 효과(dust·leak)는 2장면 이하 — 내용이 담긴 볼거리(사진·지도·사물 그림·정리판) 먼저", len(deco) <= 2, deco)
        R.add("G5", "SHOULD", "반복 피로: 눈요기 있는 장면 60% 이상", vs["ratio"] >= 0.6, f"{vs['hooked']}/{vs['n']}")
        R.add("G5", "SHOULD", "반복 피로: 같은 시각 효과 3장면 연속 없음 · 효과 3종 이상(롱폼)",
              not vs["fx_runs"] and (not longform or len(vs["fx_kinds"]) >= 3), f"{vs['fx_kinds']} 연속 {vs['fx_runs']}")
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
        prev = _prev_episode_signature(path, spec)
        if prev is not None:
            cur = set(vs["signature"])
            jac = len(cur & prev) / max(1, len(cur | prev))
            R.add("G5", "SHOULD", "반복 피로: 같은 채널 직전 편과 화면 구성 겹침 70% 이하 (Jaccard)", jac <= 0.7, f"{jac:.0%}")
        types = [s.get("type") for s in spec.get("scenes", [])]
        run3 = [types[i] for i in range(len(types) - 2) if types[i] == types[i + 1] == types[i + 2] and types[i] != "chapter"]
        R.add("G5", "MUST", "같은 type 3연속 없음", not run3, run3)
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
            R.add("G5", "SHOULD", "자료 화면 공백 ≤45초", gap <= 45, f"최장 {gap:.0f}초")
            R.add("G5", "SHOULD", "장 표지 간격 ≤200초", not longform or cgap <= 200, f"최장 {cgap:.0f}초")
        skin = (ed.get("edit") or {}).get("skin", "paper-sketch")
        from . import stylepick
        ms = stylepick.mix_stats(spec, tl)
        rule = stylepick.MIX_RULES["longform" if longform else "shorts"]
        R.add("G5", "MUST", f"스타일 조합: {rule['min_recipes']}종 이상 섞기 (한 스타일로만 만들면 불합격)", ms["n_recipes"] >= rule["min_recipes"],
              f"{ms['n_recipes']}종 {ms['recipes']}")
        R.add("G5", "MUST", f"한 스타일이 {int(rule['max_share'] * 100)}% 넘지 않음", ms["top_share"] <= rule["max_share"], f"{ms['top']} {ms['top_share']}")
        R.add("G5", "MUST", f"한 장면 안에서 겹친 장면(layers) {rule['min_layered']}개 이상", ms["layered_scenes"] >= rule["min_layered"], ms["layered_scenes"])
        R.add("G5", "MUST", f"같은 스타일 {rule['max_run'] + 1}장면 연속 없음", ms["max_run"] <= rule["max_run"], f"최장 {ms['max_run']}")
        total = sum(x["dur"] for x in tl) if tl else 5.0 * sum(len(x.get("beats", [])) for x in spec.get("scenes", []))
        es = stylepick.emphasis_stats(spec, total)
        R.add("G5", "MUST", f"강조는 아껴서: 1분에 1번 이하 (이 영상 {es['limit']}번까지)", es["count"] <= es["limit"], f"{es['count']}번 {es['items']}")
        R.add("G5", "MUST", "한 장면에 강조 1개까지 (위아래로 같은 내용 반복 금지)", not es["crowded"], f"넘친 장면 {es['crowded']}")
        R.add("G5", "MUST", "핵심 단어 띄우기(words)는 단어 1~3개만", not es["bad_words"], es["bad_words"])
        rec = stylepick.skins_for(brand) if brand else set()
        R.add("G5", "SHOULD", "그래픽 팩이 브랜드에 맞는 스타일 등록부 안 (styles/recipes)", not rec or skin in rec, f"{skin} / 등록부 {sorted(rec)}")
        sp = path / "01_research" / "style_pick.json"
        R.add("G5", "SHOULD", "style-pick 기록 (상황에 맞춘 스타일 선택)", sp.exists(), "python -m ytflow style-pick <프로젝트>")

    if last >= 5:  # G6 완성본
        R.add("G6", "MUST", "final.mp4", (edt / "final.mp4").exists(), "")
        lq = _load(path / "04_assets" / "layout_qa.json")
        R.add("G6", "MUST", "레이아웃 점검 비어 있음", lq is not None and not any(lq.values()) if isinstance(lq, dict) else lq == [],
              "" if lq is None else {k: v for k, v in (lq or {}).items() if v} if isinstance(lq, dict) else lq)
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
            R.add("G6", "SHOULD", "움직임: 화면 변화 ≥8회/분 · 정지 화면 비율 ≤0.5 (완성본 측정, v12 — 차분함이 우선)",
                  mo.get("change_events_per_min", 0) >= 8 and mo.get("static_ratio", 1) <= 0.5,
                  f"변화 {mo.get('change_events_per_min')}/분 · 정지 {mo.get('static_ratio')}")
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
        R.add("G7", "SHOULD", "제목 앞 22자 안에 질문/핵심", bool(re.search(r"[?？]|왜|까", title[:22])), title[:22])

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
        mark = "✅" if r["ok"] else ("❌" if r["level"] == "MUST" else "⚠️")
        lines.append(f"| {r['gate']} | {r['level']} | {r['item']} | {mark} | {r['detail'][:80].replace('|', '/')} |")
    lines += ["", "사람 눈 검사(EYE)는 manual/06-checklist.md 끝의 5가지를 확인하세요."]
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
