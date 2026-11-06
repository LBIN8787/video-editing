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
    tf = project.dir("source") / "trends.json"
    trends = json.loads(tf.read_text(encoding="utf-8")) if tf.exists() else {}
    niche = config.load("pipeline").get("channel_niche", "")
    user = (f"# 채널 분야\n{niche}\n\n# 스타일 프로필\n{_style_block()}\n\n"
            f"# 유튜브 후보 (outlier = 조회수/구독자)\n{json.dumps(cands, ensure_ascii=False)}\n\n"
            f"# 뉴스\n{json.dumps(news, ensure_ascii=False)}\n\n"
            f"# 트렌드 레이더 (최근 {trends.get('window_hours', '?')}시간, 여러 매체)\n{json.dumps(trends, ensure_ascii=False)[:60000]}")
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
class Article(BaseModel):
    url: str
    title: str
    publisher: str
    date: str = Field(description="YYYY-MM-DD (모르면 빈 문자열)")
    facts: list[str] = Field(description="이 기사가 뒷받침하는 팩트 번호 (예: F1)")


class ArticleList(BaseModel):
    articles: list[Article]


def research(project: Project) -> None:
    """웹 검색으로 1차 출처를 확인해 팩트시트를 만들고, 인용 가능한 기사 목록을 뽑는다.
    산출물: 01_research/factsheet.md, 01_research/articles.json"""
    topic = chosen_topic(project)
    sub_dir = project.dir("research") / "subs"
    transcripts = []
    for vid in topic.get("source_video_ids", [])[:5]:
        try:
            vtt = yt.download_subs(vid, sub_dir)
        except Exception:
            vtt = None
        if vtt:
            text = " ".join(c["text"] for c in yt.parse_vtt(vtt))
            transcripts.append({"video_id": vid, "transcript": text[:20000]})
    notes = project.dir("research") / "my_notes.md"
    extra = notes.read_text(encoding="utf-8") if notes.exists() else ""
    imported = project.dir("source") / "input.md"  # 가져온 조사 글 (대화형 LLM 답 등): 주장을 하나하나 확인 대상으로
    if imported.exists():
        extra = ("## 가져온 조사 글 (모든 숫자·발언을 1차 출처로 확인하고, 확인 안 되면 '재확인 필요')\n"
                 + imported.read_text(encoding="utf-8") + "\n\n" + extra)
    from datetime import date
    user = (f"# 오늘 날짜\n{date.today().isoformat()}\n\n# 주제\n{json.dumps(topic, ensure_ascii=False)}\n\n"
            f"# 소스 영상 자막 (있으면)\n{json.dumps(transcripts, ensure_ascii=False)}\n\n# 제작자 메모/추가 자료\n{extra}")
    print("[research] 웹 리서치 중 (수 분 걸릴 수 있음)")
    md = llm.text(config.prompt("research"), user, web=True)
    (project.dir("research") / "factsheet.md").write_text(md, encoding="utf-8")
    arts = llm.structured("팩트시트에 인용된 기사·공시·보도자료를 목록으로 뽑으세요. URL 이 적힌 것만, 팩트시트에 있는 그대로.",
                          md, ArticleList)
    project.write_json("research", "articles.json", [x.model_dump() for x in arts.articles])
    print(f"[research] {project.dir('research')}/factsheet.md · 기사 {len(arts.articles)}건")
    project.mark_done("research")


# ---------------------------------------------------------------- 3.5 원고 (칼럼·보고서 / 짧은 안내)
def article(project: Project) -> None:
    """팩트시트(+가져온 글)를 형식에 맞는 '읽는 원고'로 다듬는다 → 01_research/article.md.
    롱폼은 장편 칼럼·보고서 분석, 쇼츠는 짧은 주제 안내 (formats/<형식>.md)."""
    topic = chosen_topic(project)
    fmt = config.video_format()
    rules = (config.FORMATS_DIR / f"{fmt}.md").read_text(encoding="utf-8")
    fact = (project.dir("research") / "factsheet.md").read_text(encoding="utf-8")
    imported = project.dir("source") / "input.md"
    pcfg = config.load("pipeline")
    minutes = pcfg.get("script", {}).get("target_minutes", 9)
    user = (f"# 채널 분야\n{pcfg.get('channel_niche', '')}\n\n# 주제\n{json.dumps(topic, ensure_ascii=False)}\n\n"
            f"# 형식 규칙\n{rules}\n\n# 분량\n영상 약 {minutes}분 (원고 약 {int(minutes * 290)}자)\n\n# 팩트시트\n{fact}")
    if imported.exists():
        user += "\n\n# 가져온 조사 글 (구성 참고용, 숫자는 팩트시트 기준)\n" + imported.read_text(encoding="utf-8")
    md = llm.text(config.prompt("article"), user)
    (project.dir("research") / "article.md").write_text(md, encoding="utf-8")
    print(f"[article] {project.dir('research')}/article.md ({len(md.replace(' ', ''))}자, 형식 {fmt}) — 읽고 고친 뒤 script")
    project.mark_done("article")


# ---------------------------------------------------------------- 4. 대본
class Source(BaseModel):
    url: str = Field(description="원본 영상 URL")
    start: str = Field(description="시작 'm:ss' (모르면 빈 문자열)")
    end: str = Field(description="끝 'm:ss' (모르면 빈 문자열)")
    find: str = Field(description="구간을 모를 때 자막에서 찾을 키워드 (아니면 빈 문자열)")
    length: float = Field(description="클립 길이(초)")
    query: str = Field("", description="url 을 모를 때 YouTube 에서 찾을 검색어 (sources 단계가 영상을 고른다)")


class CardItem(BaseModel):
    label: str = Field(description="항목 이름 (12자 이내). chart 카드면 표시할 날짜 YYYY-MM-DD")
    value: str = Field(description="값 (10자 이내). bars·line 은 순수 숫자")
    sub: str = Field(description="보조 설명 (18자 이내)")
    highlight: bool
    icon: str = Field("", description="선 아이콘 이름 (ytflow.stages.icons.names(), 예: factory, cpu, zap, trending-down). 없으면 빈 문자열")


class Card(BaseModel):
    type: str = Field(description="chart | number_compare | flow | table | bars | line | headline | text | analogy"
                                  " (analogy: items[0]=실제 숫자·개념, items[1]=일상의 비유)")
    title: str = Field(description="카드 제목 (24자 이내)")
    items: list[CardItem]
    note: str = Field(description="아래 한 줄 메모 (36자 이내, 없으면 빈 문자열)")
    ticker: str = Field("", description="chart 카드: 시세 종목 코드 (NVDA, 005930.KS, ^IXIC 등). 렌더러가 실제 가격을 받아 그린다")
    period: str = Field("", description="chart 카드: 5d | 1mo | 3mo | 6mo | 1y | 2y | 5y")
    icon: str = Field("", description="text 카드의 큰 아이콘 이름 (선택)")
    unit: str = Field("", description="line 카드 값의 단위 (예: 달러, %, USD, KRW)")
    start: str = Field("", description="chart 카드: 과거 기간 시작 YYYY-MM-DD (과거 사례용, 예: 1999-06-01). 비우면 오늘까지 period")
    end: str = Field("", description="chart 카드: 과거 기간 끝 YYYY-MM-DD (비우면 오늘)")


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
    beat: str = Field("", description="이 장면이 논리에서 하는 일: fact | number | why | so_what | analogy | precedent | "
                                      "jargon | question | quote | summary | counter | takeaway | next")
    compare_to: str = Field("", description="beat=number 일 때 비교 기준 (예: '작년 같은 분기 251억 달러', '삼성전자 시총의 약 2배')")
    visual_brief: str = Field(description="편집자/이미지 생성기용 화면 지시")
    image_prompt: str = Field(description="AI 이미지 생성 프롬프트 (영문)")


class Term(BaseModel):
    term: str = Field(description="어려운 말 (예: 잉여현금흐름)")
    plain: str = Field(description="중학생도 알아듣는 한 문장 풀이 (예: 번 돈에서 공장·장비 사는 데 쓴 돈을 빼고 남은 돈)")
    scene_id: int = Field(description="이 말을 처음 풀어 주는 장면 id (처음 나오는 장면과 같거나 바로 앞)")


class Script(BaseModel):
    title_working: str
    core_message: str = Field("", description="시청자가 영상을 다 보고 기억할 한 문장 (숫자 1개 포함, 40자 안팎)")
    logic: list[str] = Field(default_factory=list,
                             description="논리 구조 3~6단계: 무슨 일(사실·숫자) → 왜(원인) → 그래서(결과) → 전에도?(과거 사례) → 반론 → 의미")
    glossary: list[Term] = Field(default_factory=list, description="대본에 나오는 어려운 말과 쉬운 풀이")
    scenes: list[Scene]


def script(project: Project) -> None:
    topic = chosen_topic(project)
    pcfg = config.load("pipeline").get("script", {})
    prof = config.style_profile()
    cpm = (prof.get("targets") or {}).get("chars_per_minute") or pcfg.get("chars_per_minute", 330)
    minutes = (prof.get("targets") or {}).get("video_minutes") or pcfg.get("target_minutes", 9)
    if config.load("pipeline").get("channel"):  # 채널 설정의 분량이 우선
        minutes = pcfg.get("target_minutes", minutes)
    fact = (project.dir("research") / "factsheet.md").read_text(encoding="utf-8")
    af = project.dir("research") / "articles.json"
    arts = af.read_text(encoding="utf-8") if af.exists() else "[]"
    art = project.dir("research") / "article.md"
    art_block = (f"# 원고 (이 글을 장면 대본으로 옮깁니다: 문단 순서를 지키고, 문장은 거의 그대로 내레이션으로)\n"
                 f"{art.read_text(encoding='utf-8')}\n\n") if art.exists() else ""
    user = (f"# 스타일 프로필\n{_style_block()}\n\n# 주제\n{json.dumps(topic, ensure_ascii=False)}\n\n{art_block}"
            f"# 팩트시트\n{fact}\n\n# 인용 가능한 기사 (screenshot 장면의 source.url 로만 사용)\n{arts}\n\n# 분량\n약 {minutes}분, 분당 {cpm}자 → 내레이션 총 {int(minutes * cpm)}자 내외")
    ref = config.load("pipeline").get("edit", {}).get("style_ref")
    addendum = config.STYLES_DIR / ref / "script.md" if ref else None
    if addendum and addendum.exists():  # 편집 스타일별 대본 규칙 (styles/<id>/script.md)
        user += f"\n\n# 이 영상의 편집 스타일({ref}) 대본 규칙\n" + addendum.read_text(encoding="utf-8")
    family = config.style_family()
    system = config.prompt("script") + "\n\n" + config.prompt(f"script_{family}") if family != "shorts" else config.prompt("script")
    res = llm.structured(system, user, Script, max_tokens=32000)
    data = res.model_dump()
    from ..scriptcheck import check
    errs, warns = check(data, family)
    if errs:  # 쉬운 설명·논리·화면 비율 점검에 걸리면 한 번 고쳐 쓴다
        print(f"[script] 점검 {len(errs)}건 → 고쳐 쓰기: " + " / ".join(errs[:5]))
        fix = (user + "\n\n# 첫 원고\n" + json.dumps(data, ensure_ascii=False) +
               "\n\n# 점검에서 걸린 것 (모두 고친 전체 원고를 다시 쓰세요)\n" + "\n".join(f"- {x}" for x in errs + warns))
        data = llm.structured(system, fix, Script, max_tokens=32000).model_dump()
    project.write_json("script", "scenes.json", data)
    write_script_md(project, data)
    total = sum(len(s["narration"].replace(" ", "")) for s in data["scenes"])
    print(f"[script] 씬 {len(data['scenes'])}개, {total}자 (~{total / cpm:.1f}분) → {project.dir('script')}/script.md\n"
          f"         수정은 scenes.json 에서. 확인 후: ytflow approve {project.path.name} script")
    project.mark_done("script")


def write_script_md(project: Project, data: dict) -> None:
    """사람이 읽는 대본: 원본 발언은 인용 블록, 화면 지시는 한 줄 요약."""
    md = [f"# {data['title_working']}\n"]
    if data.get("core_message"):
        md.append(f"**핵심 한 문장:** {data['core_message']}\n")
    if data.get("logic"):
        md.append("**논리 구조:** " + " → ".join(data["logic"]) + "\n")
    if data.get("glossary"):
        md.append("**쉬운 말 풀이:**\n" + "\n".join(f"- {g['term']}: {g['plain']} (#{g['scene_id']})" for g in data["glossary"]) + "\n")
    for s in data["scenes"]:
        src = s.get("source") or {}
        rng = f"{src.get('start') or ''}~{src.get('end') or ''}".strip("~") or (f"자막 '{src.get('find')}'" if src.get("find") else "")
        beat = f" ‹{s['beat']}›" if s.get("beat") else ""
        head = f"### #{s['id']} [{s['section']}]{beat} {'🎙 원본 발언' if s.get('kind') == 'quote' else ''} ({s['visual_type']})"
        body = (f"> {s.get('quote_en', '')}\n\n{s['narration']}" if s.get("kind") == "quote" else s["narration"])
        meta = f"라벨: {s.get('label', '')}" + (f"  |  소스: {src.get('url')} {rng}" if src.get("url") else "")
        meta += (f"  |  비교 기준: {s['compare_to']}" if s.get("compare_to") else "") + f"  |  화면: {s['visual_brief']}"
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
