"""ytflow 명령줄.

  python -m ytflow benchmark [--video]            # 기준 채널 분석 → data/style_profile.json
  python -m ytflow new "작업명"                     # 영상 프로젝트 생성
  python -m ytflow run <프로젝트> [--until 단계]      # 게이트 전까지 자동 진행
  python -m ytflow approve <프로젝트> topic --pick 2  # 사람 승인
  python -m ytflow stage <프로젝트> <단계>             # 단계 하나만 (재)실행
  python -m ytflow status <프로젝트>
"""
from __future__ import annotations

import argparse

from . import config
from .project import GATE_AFTER, STAGES, Project
from .stages import benchmark, clips, discover, media, writing

RUNNERS = {
    "discover": lambda p, a: discover.run(p, a.keywords),
    "select": lambda p, a: writing.select(p),
    "research": lambda p, a: writing.research(p),
    "script": lambda p, a: writing.script(p),
    "clips": lambda p, a: clips.run(p),
    "voice": lambda p, a: media.voice(p),
    "subtitles": lambda p, a: media.subtitles(p),
    "assets": lambda p, a: media.assets(p),
    "assemble": lambda p, a: media.assemble(p),
    "package": lambda p, a: writing.package(p),
}


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
