"""2~4단계 + 9단계: 주제 선정 → 리서치 → 대본(씬 단위) → 업로드 패키지.

모든 프롬프트에 data/style_profile.json 을 넣어 '식스시그마식' 규칙을 따르게 한다.
"""
from __future__ import annotations

import json

from pydantic import BaseModel, Field

from .. import config, llm, yt
from ..project import Project


def _style_block() -> str:
    prof = config.style_profile()
    if not prof:
        return "(스타일 프로필 없음: `ytflow benchmark` 를 먼저 실행하면 품질이 좋아집니다)"
    return json.dumps(prof, ensure_ascii=False, indent=1)


# ---------------------------------------------------------------- 2. 주제 선정
class TopicPick(BaseModel):
    title_working: str
    angle: str = Field(description="기존 영상과 다른 우리만의 관점")
    why_now: str
    source_video_ids: list[str]
    hook_idea: str
    score: int = Field(description="0-100, 클릭 잠재력 x 제작 난이도 역수 x 채널 적합도")
    risks: str


class TopicShortlist(BaseModel):
    picks: list[TopicPick]


def select(project: Project) -> None:
    cands = project.read_json("source", "candidates.json")
    news = project.read_json("source", "news.json")
    niche = config.load("pipeline").get("channel_niche", "")
    user = (f"# 채널 분야\n{niche}\n\n# 스타일 프로필\n{_style_block()}\n\n"
            f"# 유튜브 후보 (outlier = 조회수/구독자)\n{json.dumps(cands, ensure_ascii=False)}\n\n"
            f"# 뉴스\n{json.dumps(news, ensure_ascii=False)}")
    res = llm.structured(config.prompt("topic_select"), user, TopicShortlist)
    picks = sorted(res.picks, key=lambda p: p.score, reverse=True)
    project.write_json("source", "shortlist.json", [p.model_dump() for p in picks])
    lines = ["# 주제 후보 (승인할 번호를 고르세요)\n"]
    for i, p in enumerate(picks, 1):
        lines.append(f"## {i}. {p.title_working}  — {p.score}점\n- 관점: {p.angle}\n- 왜 지금: {p.why_now}\n"
                     f"- 훅: {p.hook_idea}\n- 리스크: {p.risks}\n- 소스: {', '.join(p.source_video_ids)}\n")
    (project.dir("source") / "shortlist.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"[select] {project.dir('source')}/shortlist.md 를 검토 후\n"
          f"         ytflow approve {project.path.name} topic --pick N")
    project.mark_done("select")


def chosen_topic(project: Project) -> dict:
    picks = project.read_json("source", "shortlist.json")
    idx = project.state().get("pick", 1) - 1
    return picks[idx]


# ---------------------------------------------------------------- 3. 리서치
def research(project: Project) -> None:
    topic = chosen_topic(project)
    sub_dir = project.dir("research") / "subs"
    transcripts = []
    for vid in topic["source_video_ids"][:5]:
        vtt = yt.download_subs(vid, sub_dir)
        if vtt:
            text = " ".join(c["text"] for c in yt.parse_vtt(vtt))
            transcripts.append({"video_id": vid, "transcript": text[:20000]})
    notes = project.dir("research") / "my_notes.md"
    extra = notes.read_text(encoding="utf-8") if notes.exists() else ""
    user = (f"# 주제\n{json.dumps(topic, ensure_ascii=False)}\n\n# 소스 영상 자막\n"
            f"{json.dumps(transcripts, ensure_ascii=False)}\n\n# 제작자 메모/추가 자료\n{extra}")
    md = llm.text(config.prompt("research"), user)
    (project.dir("research") / "factsheet.md").write_text(md, encoding="utf-8")
    print(f"[research] {project.dir('research')}/factsheet.md  (출처 표시된 항목만 대본에 사용됩니다)")
    project.mark_done("research")


# ---------------------------------------------------------------- 4. 대본
class Source(BaseModel):
    url: str = Field(description="원본 영상 URL")
    start: str = Field(description="시작 'm:ss' (모르면 빈 문자열)")
    end: str = Field(description="끝 'm:ss' (모르면 빈 문자열)")
    find: str = Field(description="구간을 모를 때 자막에서 찾을 키워드 (아니면 빈 문자열)")
    length: float = Field(description="find 사용 시 클립 길이(초)")


class CardItem(BaseModel):
    label: str
    value: str
    sub: str
    highlight: bool


class Card(BaseModel):
    type: str = Field(description="number_compare | flow | table | bars | headline | text")
    title: str
    items: list[CardItem]
    note: str


class Scene(BaseModel):
    id: int
    section: str = Field(description="hook / intro / body-1 ... / outro")
    kind: str = Field(description="narration(내레이션) | quote(원본 발언: 원래 소리 + 번역 자막)")
    narration: str = Field(description="내레이션 문장. kind=quote 이면 원문 발언의 한국어 번역")
    quote_en: str = Field(description="kind=quote 일 때 원문 발언 (아니면 빈 문자열)")
    label: str = Field(description="화면 왼쪽 위 출처 라벨 'YYYY.MM.DD · 출처'")
    source: Source | None = Field(description="원본 영상을 쓸 때 (visual_type=source_video 또는 kind=quote)")
    card: Card | None = Field(description="visual_type=card 일 때 검은 배경 인포 카드 내용")
    emphasis: list[str] = Field(description="자막에서 색으로 강조할 단어")
    visual_type: str = Field(description="source_video | card | screenshot | stock | ai_image")
    visual_brief: str = Field(description="편집자/이미지 생성기용 화면 지시")
    image_prompt: str = Field(description="AI 이미지 생성 프롬프트 (영문)")


class Script(BaseModel):
    title_working: str
    scenes: list[Scene]


def script(project: Project) -> None:
    topic = chosen_topic(project)
    pcfg = config.load("pipeline").get("script", {})
    prof = config.style_profile()
    cpm = (prof.get("targets") or {}).get("chars_per_minute") or pcfg.get("chars_per_minute", 330)
    minutes = (prof.get("targets") or {}).get("video_minutes") or pcfg.get("target_minutes", 9)
    fact = (project.dir("research") / "factsheet.md").read_text(encoding="utf-8")
    user = (f"# 스타일 프로필\n{_style_block()}\n\n# 주제\n{json.dumps(topic, ensure_ascii=False)}\n\n"
            f"# 팩트시트\n{fact}\n\n# 분량\n약 {minutes}분, 분당 {cpm}자 → 내레이션 총 {int(minutes * cpm)}자 내외")
    res = llm.structured(config.prompt("script"), user, Script, max_tokens=32000)
    data = res.model_dump()
    project.write_json("script", "scenes.json", data)
    write_script_md(project, data)
    total = sum(len(s["narration"].replace(" ", "")) for s in data["scenes"])
    print(f"[script] 씬 {len(data['scenes'])}개, {total}자 (~{total / cpm:.1f}분) → {project.dir('script')}/script.md\n"
          f"         수정은 scenes.json 에서. 확인 후: ytflow approve {project.path.name} script")
    project.mark_done("script")


def write_script_md(project: Project, data: dict) -> None:
    """사람이 읽는 대본: 원본 발언은 인용 블록, 화면 지시는 한 줄 요약."""
    md = [f"# {data['title_working']}\n"]
    for s in data["scenes"]:
        src = s.get("source") or {}
        rng = f"{src.get('start') or ''}~{src.get('end') or ''}".strip("~") or (f"자막 '{src.get('find')}'" if src.get("find") else "")
        head = f"### #{s['id']} [{s['section']}] {'🎙 원본 발언' if s.get('kind') == 'quote' else ''} ({s['visual_type']})"
        body = (f"> {s.get('quote_en', '')}\n\n{s['narration']}" if s.get("kind") == "quote" else s["narration"])
        meta = f"라벨: {s.get('label', '')}" + (f"  |  소스: {src.get('url')} {rng}" if src.get("url") else "")
        meta += f"  |  화면: {s['visual_brief']}"
        md.append(f"{head}\n{body}\n\n_{meta}_\n")
    (project.dir("script") / "script.md").write_text("\n".join(md), encoding="utf-8")


# ---------------------------------------------------------------- 9. 패키지
class Package(BaseModel):
    titles: list[str] = Field(description="A/B 테스트용 제목 5개")
    thumbnail_texts: list[str] = Field(description="썸네일 문구 5개 (8자 내외)")
    thumbnail_concepts: list[str]
    description: str
    tags: list[str]
    pinned_comment: str


def package(project: Project) -> None:
    scenes = project.read_json("script", "scenes.json")
    chapters = project.read_json("edit", "chapters.json") if (project.dir("edit") / "chapters.json").exists() else []
    user = (f"# 스타일 프로필\n{_style_block()}\n\n# 대본\n{json.dumps(scenes, ensure_ascii=False)}\n\n"
            f"# 챕터(초)\n{json.dumps(chapters, ensure_ascii=False)}")
    res = llm.structured(config.prompt("package"), user, Package).model_dump()
    if chapters:
        ch = "\n".join(f"{int(c['t'] // 60):02d}:{int(c['t'] % 60):02d} {c['label']}" for c in chapters)
        res["description"] = f"{res['description']}\n\n{ch}"
    project.write_json("package", "upload.json", res)
    print(f"[package] {project.dir('package')}/upload.json")
    project.mark_done("package")
