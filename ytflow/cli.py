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
from pathlib import Path
import yaml

from . import config
from .project import GATE_AFTER, STAGES, Project
from .stages import benchmark, clips, discover, media, report, scout, sources, style, writing

RUNNERS = {
    "discover": lambda p, a: discover.run(p, a.keywords),
    "scout": lambda p, a: scout.run(p),
    "select": lambda p, a: writing.select(p),
    "research": lambda p, a: writing.research(p),
    "article": lambda p, a: writing.article(p),
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
    from .stages.paper import LAYOUT as RENDER
    from .stages.writing import Script
    from .scriptcheck import check
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
    family = config.style_family()
    errs, warns = check(data, family)
    issues += errs
    for x in issues:
        print("✗", x)
    for x in warns:
        print("⚠", x)
    print(("✓ 통과" if not issues else f"문제 {len(issues)}건") + f" (권고 {len(warns)}건) — 장면 {len(data['scenes'])}개 · 계열 {family}")
    return not issues


def cmd_make(a) -> None:
    """자료조사 → 대본 → 소스 → 영상 → 업로드 패키지 → 보고서를 한 번에 (승인 게이트는 자동 통과)."""

    ch = config.channel(a.channel) if a.channel else {}
    if ch.get("format") == "shorts":  # 쇼츠 채널은 쇼츠 파이프라인으로
        from .stages import shorts
        p = shorts.make(a.name, None, a.topic, ch)
        _log_episode(ch["id"], p)
        return
    imported = Path(a.from_text).read_text(encoding="utf-8") if a.from_text else ""
    if imported and not a.topic:  # 가져온 글의 첫 제목을 주제로
        a.topic = next((l.lstrip("# ").strip() for l in imported.splitlines() if l.strip()), "가져온 글")[:60]
    p = Project.create(a.name or ((ch.get("id", "") + "-") if ch else "") + (a.topic or "auto")[:30])
    if ch:
        a.style_ref = a.style_ref or ch.get("style_ref")
    if not a.style_ref and not a.style:  # 계열의 기본 스타일 (자체 제작 = 미주일기)
        a.style_ref = (config.load("pipeline").get("default_styles") or {}).get(a.family or "infographic")
    if a.style_ref:  # 분석한 레퍼런스의 설정을 그대로 가져온다
        ref = config.STYLES_DIR / a.style_ref / "edit.yaml"
        if not ref.exists():
            raise SystemExit(f"먼저 실행: python -m ytflow style {a.style_ref} <레퍼런스 영상들>")
        (p.path / "edit.yaml").write_text(ref.read_text(encoding="utf-8"), encoding="utf-8")
    if ch:  # 채널 설정을 프로젝트에 얹는다: 분야·키워드·분량·형식
        import yaml as _y
        cur = _y.safe_load((p.path / "edit.yaml").read_text(encoding="utf-8")) if (p.path / "edit.yaml").exists() else {}
        cur.update({"channel": ch["id"], "format": ch.get("format", "longform"), "channel_niche": ch.get("niche", "")})
        cur.setdefault("discover", {})["seed_keywords"] = ch.get("seed_keywords") or []
        cur.setdefault("script", {})["target_minutes"] = ch.get("target_minutes", 9)
        if ch.get("tts"):  # 채널 목소리 (확정되면 channel.yaml 의 tts: {backend: elevenlabs, elevenlabs: {voice_id: ...}})
            cur["tts"] = ch["tts"]
        (p.path / "edit.yaml").write_text(_y.safe_dump(cur, allow_unicode=True, sort_keys=False), encoding="utf-8")
    if imported:
        (p.dir("source") / "input.md").write_text(imported, encoding="utf-8")
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
        RUNNERS["scout"](p, a)  # 주제를 줘도 소스부터 찾는다
    else:  # 소스 먼저: 트렌드 → 화제별 소스 찾기 → 소스가 강한 주제 선정(형식 판단)
        RUNNERS["discover"](p, a)
        RUNNERS["scout"](p, a)
        RUNNERS["select"](p, a)
    if a.plan:  # 기획만: 주제·형식·소스를 사람이 먼저 본다
        print(f"\n📋 기획 완료: {p.dir('source')}/shortlist.md (주제별 형식·소스)\n"
              f"   고른 뒤: python -m ytflow approve {p.path.name} topic --pick N && python -m ytflow run {p.path.name}")
        return
    stt = p.state()
    stt["pick"] = 1
    p.save_state(stt)
    for g in sorted(set(GATE_AFTER.values())):
        p.approve(g)
    for stage in STAGES[STAGES.index("research"):]:
        print(f"--- {stage}")
        RUNNERS[stage](p, a)
    if ch:
        _log_episode(ch["id"], p)
    print(f"\n✅ 완료: {p.path}/REPORT.md , {p.path}/05_edit/final.mp4")


def _log_episode(cid: str, p: Project) -> None:
    """channels/<id>/episodes.md 에 한 줄 추가 (같은 프로젝트면 갱신)."""
    from .stages.media import duration
    f = config.CHANNELS_DIR / cid / "episodes.md"
    final = p.dir("edit") / "final.mp4"
    vid = final if final.exists() else p.dir("edit") / "draft.mp4"
    try:
        title = p.read_json("package", "upload.json")["titles"][0].replace("|", "/")
    except Exception:
        title = p.state().get("name", p.path.name)
    secs = duration(vid) if vid.exists() else 0
    row = (f"| {p.path.name[:8]} | `projects/{p.path.name}` | {title} | {int(secs // 60)}:{int(secs % 60):02d} | "
           f"{'완성' if final.exists() else '가편집'} — REPORT.md 의 남은 일 확인 |")
    lines = [l for l in f.read_text(encoding="utf-8").splitlines() if f"projects/{p.path.name}`" not in l]
    f.write_text("\n".join(lines + [row]) + "\n", encoding="utf-8")
    print(f"[channel] {f} 에 기록")


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
    sub.add_parser("channels", help="운영 채널 목록 (channels/)")
    sp = sub.add_parser("skin-preview", help="같은 연출을 그래픽 스킨마다 렌더해 비교표 만들기 → 05_edit/skin_preview.png")
    sp.add_argument("project")
    sp.add_argument("--scenes", default="12,16,21,24")
    sp.add_argument("--skins", default="paper-sketch,clean-flat,dark-doc")
    th = sub.add_parser("thumbnail", help="제목·썸네일(A/B/C) 만들기 → 05_edit/thumbnail_*.png, package.md")
    th.add_argument("project")
    ck = sub.add_parser("check", help="제작 체크리스트 자동 검사 (manual/06-checklist.md) → 05_edit/checklist.md, MUST 실패 시 종료 코드 1")
    ck.add_argument("project"); ck.add_argument("--upto", default="G8", help="이 게이트까지만 (예: G4 = 대본까지)")
    rv = sub.add_parser("review", help="사용자 검토 기록: --pass 면 매뉴얼 그대로, --reject \"이유\" 면 기준 변경 대기로")
    rv.add_argument("project"); rv.add_argument("--pass", dest="passed", action="store_true")
    rv.add_argument("--reject", default=""); rv.add_argument("--note", default="")
    sub.add_parser("recipes", help="편집 스타일 등록부 목록 (styles/recipes/*.yaml — 파일 하나 추가로 늘림)")
    spk = sub.add_parser("style-pick", help="topic_brief 에 맞는 편집 스타일 추천 (영상 전체·훅·결론) → 01_research/style_pick.md")
    spk.add_argument("project")
    mb = sub.add_parser("manual-bump", help="기각 사유를 반영해 매뉴얼을 고친 뒤 버전 올리기 (manual/VERSION, CHANGELOG)")
    mb.add_argument("summary")
    sq = sub.add_parser("sync-qa", help="완성 영상의 자막·목소리·화면 싱크를 받아쓰기로 재기 → 05_edit/sync_qa.json")
    sq.add_argument("project")
    vi = sub.add_parser("voice-import", help="긴 내레이션 음성(ElevenLabs 웹·커넥터 mp3)을 대본 박자별로 잘라 03_voice 에 넣기")
    vi.add_argument("project")
    vi.add_argument("parts", nargs="+")
    dm = sub.add_parser("demand", help="분야별 수요 분석 (검색 → 채널 → 아웃라이어) → .cache/demand/<날짜>/summary.md")
    dm.add_argument("--channel", default="ch-knowledge")
    dm.add_argument("--top", type=int, default=25)
    ar = sub.add_parser("archive", help="공공 기록 사진·영상 찾기 (미국 의회도서관, 퍼블릭 도메인)")
    ar.add_argument("args", nargs="*")
    hb = sub.add_parser("hybrid", help="하이브리드 스타일 영상 만들기 (02_script/hybrid.json → final.mp4)")
    hb.add_argument("project")
    hb.add_argument("--workers", type=int, default=3)
    vs = sub.add_parser("voice-sample", help="ElevenLabs 목소리 들어 보기 (채널 목소리 고를 때)")
    vs.add_argument("--voice-id", required=True)
    vs.add_argument("--text", default="메타는 석 달 동안 번 돈보다 3억 달러를 더 썼습니다. 그런데 주가는 왜 올랐을까요? 숫자로 따라가 보겠습니다.")
    up = sub.add_parser("upload", help="완성 영상을 Google Drive 의 채널(편집 스타일)별 폴더에 올리기")
    up.add_argument("project", nargs="?")
    up.add_argument("--all", action="store_true", help="영상이 있는 모든 프로젝트")
    up.add_argument("--archive", action="store_true", help="영상과 함께 보관 자료(장면 소스·원본 클립·자막·시세)도 올리기")
    up.add_argument("--to", choices=["github", "drive"], default="github", help="github(기본, 키 불필요: GitHub Release) | drive(Drive 토큰 필요)")
    sub.add_parser("schemas", help="에이전트가 직접 쓰는 파일들의 JSON Schema 를 schemas/ 에 내보내기")
    qa = sub.add_parser("qa", help="카드 화면을 렌더링해 글자·그래프 겹침과 안전 영역 침범을 점검")
    qa.add_argument("project")
    va = sub.add_parser("validate", help="프로젝트의 대본(scenes.json)과 파일을 점검")
    va.add_argument("project")

    mk = sub.add_parser("make", help="자료조사부터 영상·업로드 패키지까지 한 번에")
    mk.add_argument("--topic", help="주제 (없으면 소스 탐색으로 자동 선정)")
    mk.add_argument("--channel", help="채널 id (channels/<id>/channel.yaml: 스타일·형식·키워드·분량·소스 찾기)")
    mk.add_argument("--plan", action="store_true", help="트렌드 → 소스 찾기 → 주제 선정(형식 판단)까지만 하고 멈춤")
    mk.add_argument("--from-text", help="가져온 조사 글(.md/.txt): 대화형 LLM 답·메모를 사실 확인 → 원고 → 영상으로")
    mk.add_argument("--angle", help="관점·방향 메모 (선택)")
    mk.add_argument("--name", help="프로젝트 이름 (선택)")
    mk.add_argument("--style", choices=["sixsigma", "paper", "flat"], help="렌더러 (보통은 --style-ref 로 스타일째 고름)")
    mk.add_argument("--style-ref", help="스타일 id (styles/<id>). 없으면 --family 의 기본 스타일")
    mk.add_argument("--family", choices=["infographic", "source"], default="infographic",
                    help="스타일 계열: infographic(자체 제작 → 미주일기, 기본) | source(원본 영상 → 식스시그마)")
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
                fam = config.style_family(((yaml.safe_load((d / "edit.yaml").read_text(encoding="utf-8")) or {}).get("edit") or {})
                                          if (d / "edit.yaml").exists() else {})
                print(f"{d.name:14} {fam:12} {meta.get('title', '').strip():12} renderer={meta.get('renderer', '').split('#')[0].strip():9} status={meta.get('status', '').split('#')[0].strip()}")
    elif a.cmd == "upload":
        from .stages import upload
        names = [d.name for d in sorted(config.PROJECTS_DIR.iterdir()) if (d / "05_edit").is_dir()] if a.all else ([a.project] if a.project else [])
        for n in names:
            if a.to == "github":
                upload.github_release(Project.open(n), a.archive)
                continue
            upload.run(Project.open(n))
            if a.archive:
                upload.archive(Project.open(n))
        if a.archive and a.all:
            upload.archive_repo()
    elif a.cmd == "voice-sample":
        from .stages.media import _elevenlabs
        ec = dict(config.load("pipeline").get("tts", {}).get("elevenlabs") or {}, voice_id=a.voice_id)
        out = config.ROOT / ".cache" / "voice_samples" / f"{a.voice_id}.mp3"
        out.parent.mkdir(parents=True, exist_ok=True)
        print(f"[voice-sample] {_elevenlabs(a.text, out, ec)}")
    elif a.cmd == "skin-preview":
        from .stages import skin
        skin.preview(Project.open(a.project), [int(x) for x in a.scenes.split(",")], a.skins.split(","))
    elif a.cmd == "thumbnail":
        from .stages import thumbnail
        thumbnail.run(Project.open(a.project))
    elif a.cmd == "check":
        from .stages import checklist
        p = Project.open(a.project)
        R = checklist.run(p.path, a.upto)
        out = checklist.write(p.path, R)
        print(out.read_text(encoding="utf-8"))
        if R.must_fail():
            raise SystemExit(1)
    elif a.cmd == "review":
        from .stages import checklist
        if not a.passed and not a.reject:
            raise SystemExit("--pass 또는 --reject \"이유\" 중 하나를 주세요")
        checklist.review(Project.open(a.project).path, a.passed, a.reject or a.note)
    elif a.cmd == "recipes":
        from .stages import stylepick
        print(stylepick.listing())
    elif a.cmd == "style-pick":
        from .stages import stylepick
        print(stylepick.run(Project.open(a.project).path).read_text(encoding="utf-8"))
    elif a.cmd == "manual-bump":
        from .stages import checklist
        checklist.bump(a.summary)
    elif a.cmd == "sync-qa":
        from .stages import syncqa
        syncqa.run(Project.open(a.project))
    elif a.cmd == "voice-import":
        from .stages import voice_import
        voice_import.run(Project.open(a.project), a.parts)
    elif a.cmd == "demand":
        from .stages import demand
        demand.run(a.channel, a.top)
    elif a.cmd == "archive":
        from .stages import archive
        archive.main(a.args)
    elif a.cmd == "hybrid":
        from .stages import hybrid
        hybrid.make(Project.open(a.project), a.workers)
    elif a.cmd == "channels":
        for d in sorted(config.CHANNELS_DIR.iterdir()):
            if (d / "channel.yaml").exists():
                c = config.channel(d.name)
                n = sum(1 for l in (d / "episodes.md").read_text(encoding="utf-8").splitlines() if l.startswith("| 2")) \
                    if (d / "episodes.md").exists() else 0
                print(f"{c['id']:16} {c.get('format', ''):9} style={c.get('style_ref', ''):14} 에피소드 {n:3}  {c.get('title', '')}")
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
