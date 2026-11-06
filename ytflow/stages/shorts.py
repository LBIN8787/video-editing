"""쇼츠 — AI 활용·깃허브 화제 기술을 소재로 9:16 세로 영상(30~50초)을 만든다.

벤치마킹 (2026-11-06, #클로드코드·#ai꿀팁·#claudecode·#ai툴 해시태그의 이번 달 상위 쇼츠, styles/shorts-aitips/STYLE.md):
  - 한국 AI 꿀팁형: 위쪽에 두 줄 훅(흰 상자 + 검은 굵은 글씨)이 끝까지 고정, 아래에 도구·화면 녹화
  - 비교 실험형: 같은 프롬프트로 여러 AI 결과를 2×2 격자로 ("who won??")
  - 그 밖: 밈 자막, 3D 캐릭터 콩트, 실사 데모 (촬영·3D 제작이 필요해 이 파이프라인 범위 밖)

흐름 (python -m ytflow shorts):
  ai_trends   GitHub 검색 API(최근 14일 생성, 별 많은 순) + Hacker News + Google News → 00_source/ai_trends.json
  pick        Claude 가 소재 1개 선택 (한국 시청자에게 쓸모, 놀라움, 따라 하기 쉬움)
  research    저장소 정보·README (GitHub API) + 요약 팩트시트, 저장소 페이지 전체 캡처
  script      훅 두 줄 + 장면 6~10개 (scenes.json 형식 그대로 → voice/subtitles/assemble 재사용)
  render      장면마다 1080×1920: 고정 훅 + 가운데 화면(페이지 스크롤 / 애니메이션 카드 / 큰 글씨)
"""
from __future__ import annotations

import json
import subprocess
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from PIL import Image, ImageDraw
from pydantic import BaseModel, Field

from .. import config, llm
from ..project import Project
from . import paper
from .writing import Card

W, H = 1080, 1920
MEDIA = (40, 470, 1040, 1370)  # 가운데 화면 영역 (x0, y0, x1, y1)


# ---------------------------------------------------------------- 1. 소재 수집
def _gh(path: str) -> dict | None:
    try:
        req = urllib.request.Request("https://api.github.com" + path,
                                     headers={"User-Agent": "ytflow", "Accept": "application/vnd.github+json"})
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read())
    except Exception as e:
        print(f"  ! GitHub {path[:50]} 실패: {str(e)[:80]}")
        return None


def ai_trends() -> dict:
    cfg = config.load("pipeline").get("shorts", {})
    days = int(cfg.get("github_days", 14))
    since = (date.today() - timedelta(days=days)).isoformat()
    repos = {}
    for q in cfg.get("github_queries", ["claude skills", "agent skills", "mcp server", "ai agent", "llm tool"]):
        d = _gh("/search/repositories?" + urllib.parse.urlencode(
            {"q": f"{q} created:>{since}", "sort": "stars", "order": "desc", "per_page": 15}))
        for it in (d or {}).get("items", []):
            age = max((datetime.now(timezone.utc) - datetime.fromisoformat(it["created_at"].replace("Z", "+00:00"))).days, 1)
            repos[it["full_name"]] = {"repo": it["full_name"], "url": it["html_url"], "stars": it["stargazers_count"],
                                      "stars_per_day": round(it["stargazers_count"] / age, 1), "created": it["created_at"][:10],
                                      "description": (it.get("description") or "")[:200], "language": it.get("language"),
                                      "topics": it.get("topics", [])[:8], "query": q}
    from .trends import google_news, hacker_news
    news = []
    for kw in cfg.get("news_keywords", ["AI agent", "Claude Code", "ChatGPT"]):
        news += hacker_news(kw, 72)[:8]
    for kw in cfg.get("news_keywords_ko", ["AI 활용", "클로드 코드", "AI 에이전트"]):
        news += google_news(kw, "ko", 72)[:8]
    ranked = sorted(repos.values(), key=lambda r: r["stars_per_day"], reverse=True)
    return {"generated": datetime.now(timezone.utc).isoformat(), "repos": ranked[:40], "news": news[:60]}


class ShortPick(BaseModel):
    repo: str = Field(description="owner/name (ai_trends 의 repos 중 하나, 소재가 뉴스면 빈 문자열)")
    topic: str = Field(description="쇼츠 주제 한 줄")
    hook_lines: list[str] = Field(description="화면 위 고정 훅 두 줄 (각 14자 이내, 질문·충격·이득)")
    angle: str = Field(description="한국 시청자에게 어떤 쓸모가 있는지")
    why_now: str = Field(description="근거 숫자 (별/일, 생성일, 뉴스)")


# ---------------------------------------------------------------- 2. 대본
class ShortScene(BaseModel):
    narration: str = Field(description="한 문장 (35자 이내, 구어체)")
    emphasis: list[str] = Field(description="자막에서 노랗게 칠할 단어 1개")
    visual: str = Field(description="page_top | page_readme | page_install | card | big_text | compare")
    big_text: str = Field(description="visual=big_text 일 때 화면 가운데 큰 글씨 (12자 이내)")
    icon: str = Field(description="big_text 와 함께 쓸 아이콘 이름 (선택)")
    card: Card | None = Field(description="visual=card 일 때 카드. number_compare/flow/table 추천 (글자 짧게)")
    compare: list[str] = Field(description="visual=compare 일 때 2~4개 칸의 이름 (예: 전, 후 / ChatGPT, Claude)")


class ShortScript(BaseModel):
    title: str
    hook_lines: list[str]
    scenes: list[ShortScene]


def build(project: Project, repo: str | None, topic: str | None) -> None:
    src, res, scr = project.dir("source"), project.dir("research"), project.dir("script")
    if not repo and not topic:
        print("[shorts] 소재 수집 (GitHub·HN·뉴스)")
        tr = ai_trends()
        project.write_json("source", "ai_trends.json", tr)
        pk = llm.structured(config.prompt("shorts_pick"), json.dumps(tr, ensure_ascii=False)[:60000], ShortPick)
        repo, topic = pk.repo, pk.topic
        project.write_json("source", "pick.json", pk.model_dump())
        print(f"[shorts] 선택: {topic} ({repo})")
    info = {}
    if topic and not repo and config.load("pipeline").get("shorts_mode") == "info":
        # 정보형 쇼츠(경제·기업 상식): 저장소 화면 대신 웹으로 사실을 확인하고 카드·큰 글씨로 보여 준다
        print("[shorts] 정보형: 사실 확인 (웹 검색)")
        facts = llm.text(config.prompt("shorts_facts"), f"# 주제\n{topic}\n\n# 오늘\n{__import__('datetime').date.today()}", web=True)
        (res / "factsheet.md").write_text(facts, encoding="utf-8")
        info = {"mode": "info", "facts": facts[:15000],
                "rule": "저장소가 없으므로 page_* 화면은 쓰지 않습니다. card(숫자) · big_text · compare 만 씁니다. 숫자는 팩트에 있는 것만."}
    if repo:
        meta = _gh(f"/repos/{repo}") or {}
        readme = _gh(f"/repos/{repo}/readme") or {}
        import base64
        text = base64.b64decode(readme.get("content", "")).decode("utf-8", "ignore") if readme.get("content") else ""
        info = {"repo": repo, "url": meta.get("html_url", f"https://github.com/{repo}"), "stars": meta.get("stargazers_count"),
                "forks": meta.get("forks_count"), "created": (meta.get("created_at") or "")[:10],
                "description": meta.get("description"), "license": (meta.get("license") or {}).get("spdx_id"),
                "readme": text[:15000]}
        (res / "repo.json").write_text(json.dumps(info, ensure_ascii=False, indent=1), encoding="utf-8")
        shot = project.dir("assets") / "repo_full.png"
        js = Path(__file__).resolve().parent.parent / "assets" / "capture.js"
        subprocess.run(["node", str(js), "--full", info["url"], str(shot)], capture_output=True, timeout=120)
        if shot.exists():
            im = Image.open(shot)
            if im.height > 7000:
                im.crop((0, 0, im.width, 7000)).save(shot)
    pick = json.loads((src / "pick.json").read_text(encoding="utf-8")) if (src / "pick.json").exists() else {"topic": topic}
    user = (f"# 소재\n{json.dumps(pick, ensure_ascii=False)}\n\n# 저장소 정보·README\n{json.dumps(info, ensure_ascii=False)[:20000]}\n\n"
            f"# 스타일 규칙\n{(config.STYLES_DIR / 'shorts-aitips' / 'script.md').read_text(encoding='utf-8')}")
    print("[shorts] 대본 작성")
    sc = llm.structured(config.prompt("shorts_script"), user, ShortScript)
    data = sc.model_dump()
    project.write_json("script", "shorts.json", data)
    # scenes.json 형식으로 변환 → voice / subtitles / assemble / package 그대로 사용
    scenes = []
    for i, s in enumerate(data["scenes"], 1):
        vt = "card" if s["visual"] == "card" and s.get("card") else ("screenshot" if s["visual"].startswith("page") else "card")
        scenes.append({"id": i, "section": "hook" if i == 1 else ("outro" if i == len(data["scenes"]) else "body-1"),
                       "kind": "narration", "narration": s["narration"], "quote_en": "", "emphasis": s["emphasis"][:1],
                       "label": f"github.com/{repo}" if repo else "", "source": {"url": info.get("url", ""), "start": "", "end": "",
                                                                                   "find": "", "length": 0, "query": ""} if repo else None,
                       "card": s["card"] if s["visual"] == "card" else None, "visual_type": vt,
                       "visual_brief": s["visual"], "image_prompt": "", "shorts": s})
    project.write_json("script", "scenes.json", {"title_working": data["title"], "scenes": scenes})
    from .writing import write_script_md
    write_script_md(project, {"title_working": data["title"], "scenes": scenes})
    for st in ("discover", "select", "research", "script", "sources", "clips"):
        project.mark_done(st)


# ---------------------------------------------------------------- 3. 화면
def _base(hook: list[str], cfgp: dict) -> Image.Image:
    """검은 바탕 + 위쪽 고정 훅 (흰 상자 위 검은 굵은 글씨, 줄마다 상자)."""
    bg = paper._rgb(cfgp.get("base", "#0B0B0D"))
    im = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(im)
    y = 170
    for i, line in enumerate(hook[:2]):
        f = paper.fit(paper.SANS_X, line, 78, W - 140)
        w = f.getlength(line)
        bh = f.size + 34
        box = (W / 2 - w / 2 - 26, y, W / 2 + w / 2 + 26, y + bh)
        d.rounded_rectangle(box, radius=10, fill=(255, 255, 255) if i == 0 else paper._rgb(cfgp.get("red", "#FFD43B")))
        d.text((W / 2, y + bh / 2), line, font=f, fill=(15, 15, 15), anchor="mm")
        y += bh + 14
    return im


def _ff(args):
    p = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *args], capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(p.stderr[-2000:])


def render_scene(project: Project, scene: dict, hook: list[str], out: Path, d: float, idx: int) -> None:
    ecfg = config.load("pipeline").get("edit", {})
    cfgp = ecfg.get("paper") or {}
    s = scene.get("shorts") or {}
    work = project.dir("assets") / "work_shorts"
    work.mkdir(exist_ok=True)
    base = work / f"base_{idx:03d}.png"
    im = _base(hook, cfgp)
    mx0, my0, mx1, my1 = MEDIA
    mw, mh = mx1 - mx0, my1 - my0
    vis = s.get("visual", "big_text")
    shot = project.dir("assets") / "repo_full.png"
    if vis.startswith("page") and shot.exists():
        # 저장소 페이지를 가운데 창 안에서 천천히 스크롤 (화면 녹화 느낌)
        page = Image.open(shot)
        # 첫 화면은 전체 폭, README·설치 부분은 본문 열(GitHub 기준 왼쪽 ~880px)만 잘라 크게
        cx0, cx1 = (0, page.width) if vis == "page_top" else (0, min(page.width, 900))
        cw = cx1 - cx0
        sc = mw / cw
        ph = int(page.height * sc)
        start = {"page_top": 0.0, "page_readme": 0.22, "page_install": 0.45}.get(vis, 0.0)
        y0 = int(min(max(ph * start, 0), max(ph - mh, 0)))
        travel = int(min(220, max(ph - mh - y0, 0)))
        im.save(base)
        _ff(["-loop", "1", "-i", str(base), "-loop", "1", "-i", str(shot), "-t", f"{d:.3f}", "-filter_complex",
             f"[1:v]crop={cw}:ih:{cx0}:0,scale={mw}:-2,crop={mw}:{mh}:0:'{y0}+{travel}*t/{d:.3f}'[pg];"
             f"[0:v][pg]overlay={mx0}:{my0},format=yuv420p", "-r", "30", "-c:v", "libx264", "-preset", "veryfast", str(out)])
        return
    if vis == "card" and scene.get("card"):
        from . import flat
        cm = work / f"card_{idx:03d}.mp4"
        flat.CURRENT["name"] = "dark"
        flat.render_card(scene["card"], cm, d, seed=idx)
        flat.CURRENT["name"] = "flat"
        im.save(base)
        ch = int(mw * 1080 / 1920)
        _ff(["-loop", "1", "-i", str(base), "-i", str(cm), "-t", f"{d:.3f}", "-filter_complex",
             f"[1:v]scale={mw}:{ch}[c];[0:v][c]overlay={mx0}:{my0 + (mh - ch) // 2},format=yuv420p",
             "-r", "30", "-c:v", "libx264", "-preset", "veryfast", str(out)])
        return
    dr = ImageDraw.Draw(im)
    red = paper._rgb(cfgp.get("red", "#FFD43B"))
    if vis == "compare" and s.get("compare"):
        names = s["compare"][:4]
        cols = 2
        rows = (len(names) + 1) // 2
        cw, chh = (mw - 20) // cols, (mh - 20) // rows
        for i, n in enumerate(names):
            x, y = mx0 + (i % cols) * (cw + 20), my0 + (i // cols) * (chh + 20)
            dr.rounded_rectangle((x, y, x + cw, y + chh), radius=18, outline=(90, 90, 96), width=3, fill=(24, 24, 28))
            dr.text((x + cw / 2, y + 50), n, font=paper.fit(paper.SANS_X, n, 52, cw - 40), fill=(255, 255, 255), anchor="mm")
        dr.text((W / 2, my1 + 10), "who won?", font=paper.F(paper.SANS_X, 54), fill=red, anchor="mt")
    else:  # big_text: 큰 글씨 + 아이콘
        t = s.get("big_text") or scene["narration"][:12]
        if s.get("icon"):
            from .icons import icon
            ic = icon(s["icon"], 220, red, 2.2)
            if ic:
                im.paste(ic, (W // 2 - 110, my0 + 110), ic)
        f = paper.fit(paper.SANS_X, t, 120, mw - 40)
        dr.text((W / 2, my0 + mh * (0.62 if s.get("icon") else 0.5)), t, font=f, fill=(255, 255, 255), anchor="mm")
    im.save(base)
    # 살짝 다가가는 움직임 + 페이드
    _ff(["-loop", "1", "-i", str(base), "-t", f"{d:.3f}", "-vf",
         f"scale=w='{W}*(1+0.04*t/{d:.3f})':h=-2:eval=frame,crop={W}:{H},fade=t=in:st=0:d=0.15,format=yuv420p",
         "-r", "30", "-c:v", "libx264", "-preset", "veryfast", str(out)])


def assets(project: Project) -> None:
    data = project.read_json("script", "shorts.json")
    scenes = project.read_json("script", "scenes.json")["scenes"]
    durs = {int(k): v for k, v in project.read_json("voice", "durations.json").items()}
    for s in scenes:
        out = project.dir("assets") / f"scene_{s['id']:03d}_anim.mp4"
        render_scene(project, s, data["hook_lines"], out, durs.get(s["id"], 3.0) + 0.12, s["id"])
        print(f"[shorts] #{s['id']} {(s.get('shorts') or {}).get('visual')}")
    project.mark_done("assets")


def make(name: str | None, repo: str | None, topic: str | None, channel: dict | None = None) -> Project:
    ch = channel or {}
    if not topic and not repo and ch.get("sourcing", {}).get("start_from") == "queue":  # 대기열의 첫 소재
        q = config.CHANNELS_DIR / ch["id"] / "queue.md"
        line = next((l for l in (q.read_text(encoding="utf-8").splitlines() if q.exists() else []) if l.startswith("- [ ] ")), "")
        topic = line[6:].split(" — ")[0].strip() or None
        if topic:
            q.write_text(q.read_text(encoding="utf-8").replace(line, line.replace("- [ ] ", "- [x] ", 1)), encoding="utf-8")
            print(f"[shorts] 대기열에서: {topic}")
    p = Project.create(name or (f"{ch['id']}-" if ch else "shorts-") + (repo or topic or "auto").split("/")[-1][:20])
    import yaml as _y
    cur = _y.safe_load((config.STYLES_DIR / ch.get("style_ref", "shorts-aitips") / "edit.yaml").read_text(encoding="utf-8"))
    if ch:
        cur.update({"channel": ch["id"], "format": "shorts", "channel_niche": ch.get("niche", ""),
                    "shorts_mode": "info" if ch.get("sourcing", {}).get("start_from") != "repo" else "repo"})
    (p.path / "edit.yaml").write_text(_y.safe_dump(cur, allow_unicode=True, sort_keys=False), encoding="utf-8")
    p = Project.open(str(p.path))
    build(p, repo, topic)
    from . import media, report, writing
    media.voice(p)
    assets(p)
    media.subtitles(p)
    media.assemble(p)
    writing.package(p)
    report.run(p)
    print(f"✅ 쇼츠 완료: {p.path}/05_edit/draft.mp4")
    return p
