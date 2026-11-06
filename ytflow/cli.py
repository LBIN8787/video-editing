"""ytflow 명령줄.

  python -m ytflow benchmark [--video]            # 기준 채널 분석 → data/style_profile.json
  python -m ytflow new "작업명"                     # 영상 프로젝트 생성
  python -m ytflow run <프로젝트> [--until 단계]      # 게이트 전까지 자동 진행
  python -m ytflow approve <프로젝트> topic --pick 2  # 사람 승인
  python -m ytflow stage <프로젝트> <단계>             # 단계 하나만 (재)실행
  python -m ytflow make --topic "주제" [--style paper]  # 자료조사~영상까지 한 번에
  python -m ytflow shorts [--repo owner/name]      # AI·깃허브 트렌드 쇼츠 (9:16)
  python -m ytflow rebuild <프로젝트>              # 클립 받기~가편집 재생성 (PC에서 원본 클립 넣을 때)
  python -m ytflow validate <프로젝트>             # 대본 점검 (에이전트가 직접 쓴 경우 필수)
  python -m ytflow schemas                        # schemas/*.schema.json 내보내기
  python -m ytflow styles                         # 편집 스타일 라이브러리 목록
  python -m ytflow status <프로젝트>
"""
from __future__ import annotations

import argparse

from . import config
from .project import GATE_AFTER, STAGES, Project
from .stages import benchmark, clips, discover, media, report, sources, style, writing

RUNNERS = {
    "discover": lambda p, a: discover.run(p, a.keywords),
    "select": lambda p, a: writing.select(p),
    "research": lambda p, a: writing.research(p),
    "script": lambda p, a: writing.script(p),
    "sources": lambda p, a: sources.run(p),
    "clips": lambda p, a: clips.run(p),
    "voice": lambda p, a: media.voice(p),
    "subtitles": lambda p, a: media.subtitles(p),
    "assets": lambda p, a: media.assets(p),
    "assemble": lambda p, a: media.assemble(p),
    "package": lambda p, a: writing.package(p),
    "report": lambda p, a: report.run(p),
}


def export_schemas() -> None:
    import json as _json
    from .stages.style import StyleRules
    from .stages.writing import ArticleList, Package, Script, TopicShortlist
    out = config.ROOT / "schemas"
    out.mkdir(exist_ok=True)
    for name, model in {"scenes": Script, "shortlist": TopicShortlist, "articles": ArticleList,
                        "upload": Package, "style_rules": StyleRules}.items():
        (out / f"{name}.schema.json").write_text(_json.dumps(model.model_json_schema(), ensure_ascii=False, indent=2),
                                                 encoding="utf-8")
        print("schemas/" + f"{name}.schema.json")


def _isnum(v) -> bool:
    try:
        float(str(v).replace(",", ""))
        return True
    except ValueError:
        return False


def layout_qa(p: Project) -> bool:
    """모든 카드를 정지 화면으로 그려 배치 관리자가 못 푼 겹침을 모은다 (렌더링 없이 빠르게)."""
    from .stages import flat, paper
    st = config.load("pipeline").get("edit", {}).get("style", "sixsigma")
    flat.CURRENT["name"] = "dark" if st == "sixsigma" else "flat"
    ctx = flat._flat() if st in ("flat", "sixsigma") else __import__("contextlib").nullcontext()
    bad = 0
    with ctx:
        for s in p.read_json("script", "scenes.json")["scenes"]:
            c = s.get("card")
            if not c:
                continue
            S = paper.Scene(s["id"])
            paper.LAYOUT.get(c.get("type"), paper.l_text)(S, c)
            if S.issues:
                bad += 1
                print(f"✗ #{s['id']} {c.get('type')}: " + "; ".join(S.issues))
    flat.CURRENT["name"] = "flat"
    print("✓ 겹침 없음" if not bad else f"겹침 남은 카드 {bad}개 → 대본에서 글자를 줄이거나 장면을 나누세요")
    return not bad


def validate(p: Project) -> bool:
    """대본 스키마·장면 규칙 점검. 문제를 출력하고 통과 여부를 돌려준다."""
    from .stages.cards import RENDER
    from .stages.writing import Script
    issues = []
    try:
        data = Script.model_validate(p.read_json("script", "scenes.json")).model_dump()
    except Exception as e:  # 스키마 자체가 틀림
        print("✗ scenes.json 스키마 오류:\n", str(e)[:2000])
        return False
    for i, s in enumerate(data["scenes"], 1):
        tag = f"#{s['id']}"
        if s["id"] != i:
            issues.append(f"{tag}: id 는 1부터 순서대로여야 합니다 (기대값 {i})")
        if s["kind"] not in ("narration", "quote"):
            issues.append(f"{tag}: kind={s['kind']} (narration|quote)")
        if s["kind"] == "quote" and not s["quote_en"]:
            issues.append(f"{tag}: quote 장면에 quote_en(원문)이 없습니다")
        if s["visual_type"] == "card" and not s["card"]:
            issues.append(f"{tag}: card 장면에 card 내용이 없습니다")
        if s["card"] and s["card"]["type"] in ("bars", "line"):
            bad = [it["value"] for it in s["card"]["items"] if not _isnum(it["value"])]
            if bad:
                issues.append(f"{tag}: {s['card']['type']} 카드의 value 는 숫자만 (단위는 label/sub 로): {bad[:3]} → 지금은 표로 대체됨")
        if s["card"] and s["card"]["type"] not in RENDER:
            issues.append(f"{tag}: card.type={s['card']['type']} ({' | '.join(RENDER)})")
        src = s.get("source") or {}
        if s["visual_type"] in ("source_video", "screenshot") or s["kind"] == "quote":
            if not (src.get("url") or src.get("query")):
                issues.append(f"{tag}: {s['visual_type']} 장면에 source.url 또는 source.query 가 필요합니다")
        if not s.get("label") and s["visual_type"] != "card":
            issues.append(f"{tag}: label(날짜 · 출처)이 비어 있습니다")
    for x in issues:
        print("✗", x)
    print(("✓ 통과" if not issues else f"문제 {len(issues)}건") + f" — 장면 {len(data['scenes'])}개")
    return not issues


def cmd_make(a) -> None:
    """자료조사 → 대본 → 소스 → 영상 → 업로드 패키지 → 보고서를 한 번에 (승인 게이트는 자동 통과)."""

    p = Project.create(a.name or (a.topic or "auto")[:30])
    if a.style_ref:  # 분석한 레퍼런스의 설정을 그대로 가져온다
        ref = config.STYLES_DIR / a.style_ref / "edit.yaml"
        if not ref.exists():
            raise SystemExit(f"먼저 실행: python -m ytflow style {a.style_ref} <레퍼런스 영상들>")
        (p.path / "edit.yaml").write_text(ref.read_text(encoding="utf-8"), encoding="utf-8")
    if a.style:
        import yaml as _y
        cur = _y.safe_load((p.path / "edit.yaml").read_text(encoding="utf-8")) if (p.path / "edit.yaml").exists() else {}
        cur.setdefault("edit", {})["style"] = a.style
        (p.path / "edit.yaml").write_text(_y.safe_dump(cur, allow_unicode=True), encoding="utf-8")
    p = Project.open(str(p.path))
    print(f"=== make: {p.path.name} (style={config.load('pipeline')['edit']['style']}, ref={a.style_ref or '-'})")
    if a.topic:  # 주제를 직접 준 경우: 소스 탐색·주제 선정 생략
        p.write_json("source", "shortlist.json", [{"title_working": a.topic, "angle": a.angle or "", "why_now": "",
                                                   "source_video_ids": [], "hook_idea": "", "score": 100, "risks": ""}])
        for st in ("discover", "select"):
            p.mark_done(st)
    else:
        RUNNERS["discover"](p, a)
        RUNNERS["select"](p, a)
    stt = p.state()
    stt["pick"] = 1
    p.save_state(stt)
    for g in sorted(set(GATE_AFTER.values())):
        p.approve(g)
    for stage in STAGES[2:]:
        print(f"--- {stage}")
        RUNNERS[stage](p, a)
    print(f"\n✅ 완료: {p.path}/REPORT.md , {p.path}/05_edit/draft.mp4")


def cmd_run(p: Project, a) -> None:
    done = set(p.state()["done"])
    for stage in STAGES:
        if stage not in done or a.force:
            RUNNERS[stage](p, a)
        gate = GATE_AFTER.get(stage)
        if gate and not p.gate_open(gate):
            print(f"\n⏸  '{gate}' 승인 대기. 결과를 확인한 뒤:  python -m ytflow approve {p.path.name} {gate}")
            return
        if a.until and stage == a.until:
            return
    print("\n✅ 전체 완료:", p.path)


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(prog="ytflow", description="벤치마킹 기반 유튜브 제작 자동화")
    sub = ap.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("benchmark", help="기준 채널 분석 → 스타일 프로필")
    b.add_argument("--video", action="store_true", help="저화질 영상을 받아 컷 속도까지 측정")
    b.add_argument("--no-llm", action="store_true", help="수치 통계만 (API 호출 없음)")

    n = sub.add_parser("new", help="영상 프로젝트 생성")
    n.add_argument("name")

    r = sub.add_parser("run", help="게이트 전까지 순서대로 실행")
    r.add_argument("project")
    r.add_argument("--until", choices=STAGES)
    r.add_argument("--force", action="store_true", help="완료된 단계도 다시 실행")
    r.add_argument("--keywords", nargs="*")

    s = sub.add_parser("stage", help="단계 하나만 실행")
    s.add_argument("project")
    s.add_argument("stage", choices=STAGES)
    s.add_argument("--keywords", nargs="*")

    g = sub.add_parser("approve", help="사람 승인 게이트 통과")
    g.add_argument("project")
    g.add_argument("gate", choices=sorted(set(GATE_AFTER.values())))
    g.add_argument("--pick", type=int, help="topic 게이트: shortlist 번호")

    sh = sub.add_parser("shorts", help="AI 활용·깃허브 화제 기술 쇼츠(9:16)를 한 번에")
    sh.add_argument("--repo", help="owner/name (없으면 GitHub·뉴스 트렌드에서 자동 선택)")
    sh.add_argument("--topic", help="주제 (저장소 없이 뉴스·팁 소재)")
    sh.add_argument("--name")

    sy = sub.add_parser("style", help="레퍼런스 영상 파일로 편집 스타일을 분석 → styles/<id>/")
    sy.add_argument("name", help="스타일 id (영문 소문자 권장, 예: mijudiary)")
    sy.add_argument("videos", nargs="+")
    sy.add_argument("--title", help="표시 이름 (예: 미주일기)")

    sub.add_parser("styles", help="스타일 라이브러리 목록")
    sub.add_parser("schemas", help="에이전트가 직접 쓰는 파일들의 JSON Schema 를 schemas/ 에 내보내기")
    qa = sub.add_parser("qa", help="카드 화면을 렌더링해 글자·그래프 겹침과 안전 영역 침범을 점검")
    qa.add_argument("project")
    va = sub.add_parser("validate", help="프로젝트의 대본(scenes.json)과 파일을 점검")
    va.add_argument("project")

    mk = sub.add_parser("make", help="자료조사부터 영상·업로드 패키지까지 한 번에")
    mk.add_argument("--topic", help="주제 (없으면 소스 탐색으로 자동 선정)")
    mk.add_argument("--angle", help="관점·방향 메모 (선택)")
    mk.add_argument("--name", help="프로젝트 이름 (선택)")
    mk.add_argument("--style", choices=["sixsigma", "paper"], help="편집 스타일")
    mk.add_argument("--style-ref", help="ytflow style 로 분석한 레퍼런스 이름 (측정한 색·속도를 적용)")
    mk.add_argument("--keywords", nargs="*")

    rb = sub.add_parser("rebuild", help="소스 클립 받기 → 음성 → 화면 → 자막 → 가편집을 한 번에 (원본 클립을 넣은 뒤)")
    rb.add_argument("project")

    st = sub.add_parser("status")
    st.add_argument("project")

    a = ap.parse_args(argv)
    if a.cmd == "benchmark":
        benchmark.run(with_video=a.video, skip_llm=a.no_llm)
    elif a.cmd == "new":
        p = Project.create(a.name)
        print("생성:", p.path)
    elif a.cmd == "run":
        cmd_run(Project.open(a.project), a)
    elif a.cmd == "stage":
        p = Project.open(a.project)
        RUNNERS[a.stage](p, a)
    elif a.cmd == "approve":
        p = Project.open(a.project)
        if a.gate == "topic" and a.pick:
            stt = p.state()
            stt["pick"] = a.pick
            p.save_state(stt)
        p.approve(a.gate)
        print(f"승인: {a.gate}. 이어서:  python -m ytflow run {p.path.name}")
    elif a.cmd == "shorts":
        from .stages import shorts
        shorts.make(a.name, a.repo, a.topic)
    elif a.cmd == "style":
        style.run(a.name, a.videos, a.title)
    elif a.cmd == "schemas":
        export_schemas()
    elif a.cmd == "qa":
        raise SystemExit(0 if layout_qa(Project.open(a.project)) else 1)
    elif a.cmd == "validate":
        raise SystemExit(0 if validate(Project.open(a.project)) else 1)
    elif a.cmd == "styles":
        for d in sorted(config.STYLES_DIR.iterdir()):
            if d.is_dir() and not d.name.startswith("_") and (d / "STYLE.md").exists():
                head = (d / "STYLE.md").read_text(encoding="utf-8").split("---")[1] if (d / "STYLE.md").read_text(encoding="utf-8").startswith("---") else ""
                meta = dict(l.split(":", 1) for l in head.strip().splitlines() if ":" in l)
                print(f"{d.name:14} {meta.get('title', '').strip():12} renderer={meta.get('renderer', '').split('#')[0].strip():9} status={meta.get('status', '').split('#')[0].strip()}")
    elif a.cmd == "make":
        cmd_make(a)
    elif a.cmd == "rebuild":
        p = Project.open(a.project)
        for stage in ("clips", "voice", "assets", "subtitles", "assemble", "report"):
            RUNNERS[stage](p, a)
    elif a.cmd == "status":
        p = Project.open(a.project)
        stt = p.state()
        has_profile = bool(config.style_profile())
        print(f"{p.path.name}  (스타일 프로필: {'있음' if has_profile else '없음'})")
        for stage in STAGES:
            mark = "✔" if stage in stt["done"] else "·"
            gate = GATE_AFTER.get(stage)
            gs = f"  [게이트 {gate}: {'승인' if p.gate_open(gate) else '대기'}]" if gate else ""
            print(f"  {mark} {stage}{gs}")


if __name__ == "__main__":
    main()
