"""뉴스레터 → 채널별 소재 목록 (2026-11-15 사용자: 무료 뉴스레터를 소스 탐색·참조용으로 구독, "진행해주세요").

뉴스레터는 **단서**입니다. 문장을 대본·화면에 옮기지 않고, 영상에 넣을 숫자·발언은 링크를 따라 1차 출처로 확인합니다.
메일 하나를 그대로 쌓지 않고, 소재마다 다섯 칸으로 나눕니다:
    소재(원래 제목) · 원문 링크 · 원자료·통계 · 영상·이미지 출처 · 재사용 조건
그리고 카테고리(market·ai·curiosity·history·issues — 시장·AI·일상·심리·뇌과학·역사·시사)별로 모아
`inbox/newsletters/<YYYYMMDD>.md|json` 에 씁니다.

SAVE(오선) 알림(`[save알림]` 메일, 2026-11-20 개편)은 원문 링크가 없는 **단신 한 줄**이라 따로
`inbox/save/` 에 쌓지 않고, 같은 파일의 다섯 카테고리 중 하나로 들어갑니다(config 의 `headline: true` 소스).
그 행은 원문·기사 칸이 비고 제목에 알림 시각을 붙입니다 — 빈 링크 괄호를 만들지 않습니다.
시장·시사 매일 브리핑은 `daily` 가 그날 파일을 `daily_brief.md` 끝 '⑦ 뉴스레터 화제'로 붙입니다.

메일 가져오기 (클라우드 Python 은 Gmail 에 직접 못 들어감 → 에이전트가 Gmail 커넥터로):
    1) Gmail 검색 `label:뉴스레터 newer_than:2d` (또는 config/newsletters.yaml 의 보낸 사람)
    2) 메일마다 get_message(PLAIN_TEXT) → {"id","sender","subject","date","body"} 를 JSON 으로 `.cache/newsletters/raw/` 에 저장
    3) python -m ytflow newsletters ingest .cache/newsletters/raw/*.json
RSS 는 직접:   python -m ytflow newsletters rss
보기:          python -m ytflow newsletters show [--brand curiosity] [--days 7]
원문 메일 본문은 커밋하지 않습니다(.cache). 커밋하는 것은 제목·링크·분류뿐.
"""
from __future__ import annotations

import base64
import json
import re
from hashlib import sha256
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

from .. import config

KST = timezone(timedelta(hours=9))
CFG = config.ROOT / "config" / "newsletters.yaml"
OUT = config.ROOT / "inbox" / "newsletters"
BRANDS = ("market", "ai", "curiosity", "history", "issues")
BRAND_KO = {"market": "시장", "ai": "AI", "curiosity": "일상·심리·뇌과학", "history": "역사", "issues": "시사"}
KIND_KO = {"primary": "원문", "data": "원자료·통계", "media": "영상·이미지", "news": "보도·글"}
NOISE_SUBJ = re.compile(r"(?i)confirm|welcome|verify|subscription|preferences|update profile|구독 확인|구독해|환영|인증|가입")
EMAIL_ADDRESS = re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}")
GENERIC = re.compile(r"(?i)^(read more|more|here|click here|link|learn more|full story|continue reading|read|sign up|subscribe|"
                     r"keep reading|share this( story| item)?|share on \w+|share via|read the story|"
                     r"view online|this|website|자세히|더 보기|원문|바로가기|기사 보기)\W*$")
# 짧은 라벨은 대개 'Read more' 같은 잡음이라 거부하지만, 한국어 낱말 둘 이상은 소재 이름이다
# (예: '사이드카'·'공매도' — 어피티 머니레터, 2026-11-23).
SHORT_OK = re.compile(r"[가-힣]{2}")
UA = {"User-Agent": "ytflow-newsletters (research)"}


def cfg() -> dict:
    return yaml.safe_load(CFG.read_text(encoding="utf-8"))


# ── 날짜: 한국 08:00 제작 시작 이후 도착은 다음 날 영상 몫 (SAVE 규칙과 별개) ──
def video_day(iso: str) -> str:
    try:
        t = datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(KST)
    except ValueError:
        t = datetime.now(KST)
    d = t.date() + (timedelta(days=1) if t.hour >= 8 else timedelta(0))
    return d.strftime("%Y%m%d")


# ── 어느 뉴스레터인가 ──
def which(msg: dict, c: dict) -> dict | None:
    who = (msg.get("sender", "") + " " + msg.get("name", "")).lower()
    for s in c["sources"]:
        match = s.get("match") or []
        subject = s.get("subject")
        if match:
            if not any(m.lower() in who for m in match):
                continue
        elif not subject:   # 보낸 사람도 제목도 없으면 알아볼 수 없음
            continue
        if subject and not re.search(subject, msg.get("subject", "")):
            continue
        return s
    return None


# ── 링크 ──
# Stibee(스티비: 어피티 머니레터·미라클레터 등)의 클릭 추적 주소.
#   https://event.stibee.com/v2/click/<수신자 묶음 base64>/<목적지 base64url>
# 목적지가 주소 안에 그대로 들어 있어 네트워크 요청 없이 해독된다 (2026-11-23 확인).
# 앞 묶음은 구독자·캠페인 번호라 해독해도 쓸 데가 없고, 그대로 두면 공개 목록에 수신자 식별자가 실린다.
STIBEE_CLICK = re.compile(r"https?://event\.stibee\.com/v2/click/[^/\s?#]+/([A-Za-z0-9_\-=]+)")
# Axios 메일의 클릭 주소. `https://link.axios.com/click/<캠페인>/<목적지 base64url>/<해시>` 처럼
# 목적지가 주소 안에 그대로 들어 있다 — 스티비와 같은 방식으로 네트워크 요청 없이 해독한다.
# (2026-11-24 확인: Axios AM·Markets 는 평문 본문 없이 HTML 만 오고 모든 링크가 이 형식이라,
#  풀지 않으면 두 뉴스레터에서 소재가 하나도 남지 않는다.)
AXIOS_CLICK = re.compile(r"https?://link\.axios\.com/click/[^/\s?#]+/([A-Za-z0-9_\-=]+)")


def b64url_text(s: str) -> str:
    """base64url 글자 → utf-8 글자. 패딩은 있어도 없어도 되고, 아니면 빈 글자."""
    t = s.replace("-", "+").replace("_", "/").rstrip("=")
    try:
        return base64.b64decode(t + "=" * (-len(t) % 4), validate=True).decode("utf-8")
    except (ValueError, UnicodeDecodeError):
        return ""


def stibee_dest(url: str) -> str:
    """Stibee 클릭 추적 주소 → 실제 목적지. 형식이 다르거나 해독이 안 되면 빈 글자(주소를 손대지 않음)."""
    m = STIBEE_CLICK.match(url)
    if not m or url[m.end():].strip("/"):   # 뒤에 다른 경로가 붙은 형식은 건드리지 않는다
        return ""
    dest = b64url_text(m.group(1))
    return dest if dest.startswith(("http://", "https://")) else ""


def unwrap(url: str) -> str:
    """추적 주소 안에 든 진짜 주소 꺼내기 — 주소 안에서만 푼다(네트워크 요청 없음).

    Stibee `/v2/click/<묶음>/<base64url 목적지>`, TLDR `/CL0/<인코딩된 주소>/…`,
    흔한 리디렉트 파라미터(`?url=`·`?u=`·`?redirect=`) 순서로 보고, 못 꺼내면 그대로.
    """
    stibee = stibee_dest(url)
    m = re.search(r"/CL0/(https?(?::|%3A)[^/]*(?:/|%2F).+?)/\d+/[0-9a-f-]{20,}", url)
    ax = AXIOS_CLICK.match(url)
    axios = ""
    if ax:
        dest = b64url_text(ax.group(1))
        axios = dest if dest.startswith(("http://", "https://")) else ""
    if stibee:
        url = stibee
    elif axios:
        url = axios
    elif m:
        url = urllib.parse.unquote(m.group(1))
    else:
        q = urllib.parse.parse_qs(urllib.parse.urlsplit(url).query)
        for k in ("url", "u", "redirect", "target", "r"):
            if k in q and q[k][0].startswith("http"):
                url = q[k][0]
                break
    p = urllib.parse.urlsplit(url)
    # xy: FinancialJuice 피드가 모든 기사 주소에 붙이는 피드 출처 표식(?xy=rss) — 사람마다 다른 값이 아니라 공개 표식
    keep = [(k, v) for k, v in urllib.parse.parse_qsl(p.query)
            if k.lower() != "xy" and not k.lower().startswith(("utm_", "mc_", "ref", "_hs", "mkt_"))]
    return urllib.parse.urlunsplit((p.scheme, p.netloc, p.path, urllib.parse.urlencode(keep), ""))


# Ingestion never dereferences email links. Even HEAD can trigger an action.
MANAGEMENT = re.compile(
    r"unsubscribe|subscription|preferences|opt[-_ ]?out|manage[-_ /]?profile|"
    r"confirm|verification|verify|sign[-_ ]?in|log[-_ ]?in|password|"
    r"change[-_ /]?email|update[-_ /]?email|email[-_ /]?change|account[-_ /]?settings|"
    r"subscribers/auth|"
    r"구독.?해지|수신.?거부|이메일.?변경|환경.?설정|본인.?인증", re.I)
PUBLIC_QUERY = {"id", "v", "q", "s", "page", "lang", "language", "year", "month"}
SENSITIVE_QUERY = re.compile(
    r"token|secret|email|recipient|subscriber|signature|auth|session|hash|"
    r"^key$|^code$|^uid$|^cid$|^mid$", re.I)
# 호스트마다 공개로 확인된 쿼리 키 (자료 번호·섹션 이름 같은 공개 표식)
HOST_QUERY = {"eiec.kdi.re.kr": {"num"}, "axios.com": {"stream"}, "naver.com": {"sid"}}


def public_link(url: str, strict: bool = True) -> bool:
    """Conservative publication gate, not proof that a URL is safe to visit.

    strict=True (메일): 긴 경로 한 덩이나 낯선 쿼리도 수신자별 식별자로 본다.
    strict=False (RSS): 공개 피드의 주소는 모든 구독자에게 같다 — 긴 경로는 사람이 읽는
    기사 슬러그일 뿐이라(예: smithsonianmag.com/history/…-crusades-took-form) 그 규칙만 빼고,
    관리·탈퇴 주소·추적 호스트·민감한 쿼리는 그대로 막는다. 2026-11-20 역사 RSS 추가 때 확인.
    """
    try:
        p = urllib.parse.urlsplit(url)
        host = (p.hostname or "").lower()
        if p.scheme not in ("http", "https") or not host or p.username or p.password:
            return False
        decoded = urllib.parse.unquote(url)
        if MANAGEMENT.search(decoded) or EMAIL_ADDRESS.search(decoded):
            return False
        if (host == "beehiiv.com" or host.endswith(".beehiiv.com") or
                host.startswith(("links.", "click.", "email.", "r.", "trk.", "go.")) or
                (host.endswith("substack.com") and p.path.startswith("/redirect")) or
                (host.endswith("list-manage.com") and p.path.startswith("/track"))):
            return False
        # Unknown query keys can be per-recipient identifiers: retain privately
        # for manual canonical-source lookup, never publish or request them.
        pairs = urllib.parse.parse_qsl(p.query, keep_blank_values=True)
        # 호스트별로 공개가 확인된 쿼리 키만 예외로 둔다 (사람마다 다른 값이 아닌 표식):
        #   eiec.kdi.re.kr `num` — 경제정보센터 자료 번호 (2026-11-23)
        #   axios.com `stream` — 뉴스레터 섹션 이름 (2026-11-24, Axios AM·Markets)
        #   naver.com `sid` — 네이버 뉴스 분야 번호 (2026-11-24, 어피티·미라클레터 뉴스 링크)
        extra = next((keys for d, keys in HOST_QUERY.items()
                      if host == d or host.endswith("." + d)), set())
        if any(SENSITIVE_QUERY.search(k) or len(v) > 80 or "@" in v or
               (k.lower() not in PUBLIC_QUERY and k.lower() not in extra) for k, v in pairs):
            return False
        if strict and re.search(r"(?:^|/)[A-Za-z0-9_=-]{48,}(?:/|$)", urllib.parse.unquote(p.path)):
            return False
        return True
    except ValueError:
        return False


def resolve(url: str, timeout: int = 8) -> str:
    """Compatibility helper: offline unwrap only; never follows redirects."""
    return unwrap(url)


def kind(url: str, c: dict) -> str:
    u = url.lower()
    for k in ("primary", "data", "media"):
        for d in c["links"][k]:
            host = urllib.parse.urlsplit(u).netloc
            if (d.endswith(".") and host.startswith(d)) or (d.startswith(".") and u.split("?")[0].endswith(d)) or d in u:
                return k
    return "news"


def reuse(url: str, c: dict) -> str:
    host = urllib.parse.urlsplit(url).netloc.lower()
    for d, txt in c["reuse"].items():
        if host == d or host.endswith("." + d) or d in url.lower():
            return txt
    return "보도·글: 단서만 (문장 옮기지 않기, 인용은 짧게 출처 표시)"


def skip(url: str, title: str, c: dict, own: list[str]) -> bool:
    low = (url + " " + title).lower()
    if any(s in low for s in c["skip"]):
        return True
    host = urllib.parse.urlsplit(url).netloc.lower()
    path = urllib.parse.urlsplit(url).path.strip("/")
    return any(o in host for o in own) and len(path) < 12   # 뉴스레터 자기 홈 (기사 주소는 남김)


# ── 메일 본문 → 소재 ──
LINK_MD = re.compile(r"\[([^\]\n]{2,240})\]\((https?://[^)\s]+)\)")
# 앵커 글자가 여러 줄인 마크다운 링크: `[` \n `제목` \n `](주소)`
# 평문 파트가 없고 HTML 만 온 메일에 앵커 안에 블록(h3·div)이 들어 있으면 이렇게 나온다(KDI 2026-11-24).
# 줄바꿈을 글자로 인정하지 않으면 제목이 `]` 하나로 잡혀 소재가 통째로 0건이 된다.
LINK_MD_ML = re.compile(r"\[\s{0,2}([^\[\]]{2,400}?)\s{0,2}\]\s*\((https?://[^)\s]+)\)")
LINK_ANGLE = re.compile(r"([^\n<>]{0,240}?)\s*[<(](https?://[^>)\s]+)[>)]")
LINK_BARE = re.compile(r"https?://[^\s<>()\[\]\"']+")


FOOTNOTE_REF = re.compile(r"^\[(\d{1,3})\]$")


def footnote_title(body_before: str, n: str) -> str:
    """맨주소 줄이 `[7]` 뿐일 때, 본문 위쪽에서 같은 각주 번호를 단 줄을 제목으로 찾는다.

    TLDR 평문 본문은 `제목 (5 MINUTE READ) [7]` … 본문 끝 `[7] https://…` 로 온다.
    각주 번호만 있는 줄(참조 목록 자신)은 건너뛰고, 글자가 있는 줄만 쓴다.
    """
    mark = f"[{n}]"
    for line in reversed(body_before.splitlines()):
        if mark not in line:
            continue
        cand = re.sub(r"\s*" + re.escape(mark) + r"\s*$", "", _clean(line)).strip()
        if len(cand) >= 8:
            return cand
    return ""


def _clean(t: str) -> str:
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)   # 마크다운 링크 → 글자만
    t = re.sub(r"https?://\S+", "", t)
    t = re.sub(r"[*#>`]+|(?<!\w)_|_(?!\w)", "", t)
    t = re.sub(r"\((\d+ )?min(ute)? read\)|\(GitHub Repo\)|\(Sponsor\)", "", t, flags=re.I)
    t = re.sub(r"\s+", " ", t).strip(" -–—:|·•")
    return t[:180]


def extract(body: str) -> list[tuple[str, str]]:
    """[(제목, 주소)] — 마크다운 링크 → '글 <주소>' → 맨 주소(앞줄을 제목으로) 순서로.

    같은 주소를 두 번 줍지 않는다: 마크다운 링크 안의 주소는 각도괄호·맨주소 규칙에서 빼서,
    '앞 글자가 라벨로 붙는' 중복(2026-11-23 확인)을 만들지 않는다.
    """
    out, md_url_spans, seen_spans = [], [], []
    lines = body.splitlines()
    for rx in (LINK_MD_ML, LINK_MD, LINK_ANGLE):
        for m in rx.finditer(body):
            ua, ub = m.span(2)
            if any(a <= ua and ub <= b for a, b in md_url_spans):
                continue
            if any(a <= m.start() < b for a, b in seen_spans):
                continue
            seen_spans.append(m.span())
            if rx is not LINK_ANGLE:
                md_url_spans.append((ua, ub))
            title, url = _clean(m.group(1)), m.group(2).rstrip("'\"),;")
            if not title or GENERIC.match(title):   # 'Read more' → 앞 줄을 제목으로
                before = body[: m.start()].rstrip().splitlines()
                title = _clean(before[-1]) if before else ""
            out.append((m.start(), title, url))
    for m in LINK_BARE.finditer(body):
        ua, ub = m.span()
        if any(a <= ua and ub <= b for a, b in md_url_spans):
            continue
        if any(a <= m.start() < b for a, b in seen_spans):
            continue
        ln = body.count("\n", 0, m.start())
        title = _clean(lines[ln][: m.start() - (body.rfind("\n", 0, m.start()) + 1)]) or (_clean(lines[ln - 1]) if ln else "")
        if FOOTNOTE_REF.match(title):   # '[7] https://…' — 제목은 각주 번호를 단 앞 줄 (TLDR 평문)
            title = footnote_title(body[: m.start()], FOOTNOTE_REF.match(title).group(1)) or title
        out.append((m.start(), title, m.group(0).rstrip(".,;")))
    return [(t, u) for _, t, u in sorted(out)]   # 본문 순서대로 (원자료 링크를 바로 앞 소재에 붙이려면)


def route(title: str, src: dict, c: dict) -> str:
    bs = src.get("brands") or ["curiosity"]
    if len(bs) == 1:
        return bs[0]
    t = f" {title.lower()} "
    score = {b: sum(1 for w in c["route"].get(b, []) if w in t) for b in bs}
    best = max(bs, key=lambda b: (score[b], -bs.index(b)))
    return best if score[best] else bs[0]


# ── 링크 없는 단신 (SAVE 알림) — 한 줄이 소재 하나 ──
# MacroDroid 가 보내는 본문은 `[app_name] | [notification_title] | 소식` 한 줄입니다.
PIPE_TEMPLATE = re.compile(r"^\s*\[[^\]]*\]\s*\|")
PLACEHOLDER = re.compile(r"\[(?:app_name|notification_title|package_name|text)\]")
NO_LINK_REUSE = "알림 단신: 원문 링크 없음 — 1차 출처로 직접 확인"


def headline_line(line: str) -> str:
    """`[app_name] | [notification_title] | 소식` 에서 소식만. 템플릿이 빈 채로 온 줄은 빈 글자."""
    t = line.strip()
    if PIPE_TEMPLATE.match(t):
        t = t.rsplit("|", 1)[-1].strip()
    if not t or PLACEHOLDER.search(t):
        return ""
    return _clean(t)


def alarm_stamp(iso: str) -> str:
    """표에 적을 알림 시각 `MM-dd HH:mm` (KST)."""
    try:
        return datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(KST).strftime("%m-%d %H:%M")
    except ValueError:
        return ""


def headlines_from(msg: dict, src: dict, c: dict) -> list[dict]:
    """링크 없는 단신: 본문 한 줄 = 소재 하나.

    원문 주소가 없으므로 `url` 은 빈 글자로 두고 표에는 제목·출처·알림 시각만 적습니다
    (빈 링크 괄호를 만들지 않음). 카테고리는 제목 낱말(`route`)로 다섯 칸 중 하나에 넣습니다.
    """
    out, seen = [], set()
    for raw in msg.get("body", "").splitlines():
        title = headline_line(raw)
        key = re.sub(r"\s+", " ", title).lower()
        if len(title) < 4 or EMAIL_ADDRESS.search(title) or key in seen:
            continue
        seen.add(key)
        out.append({"title": title, "url": "", "kind": "news", "reuse": NO_LINK_REUSE,
                    "brand": route(title, src, c), "source": src["id"], "source_name": src["name"],
                    "msg": msg.get("id", ""), "date": msg.get("date", ""),
                    "alarm": alarm_stamp(msg.get("date", ""))})
    return out


def items_from(msg: dict, c: dict, do_resolve: bool = True) -> list[dict]:
    src = which(msg, c)
    if not src or NOISE_SUBJ.search(msg.get("subject", "")):
        return []
    if src.get("headline"):   # SAVE 알림 — 본문이 링크 없는 한 줄
        return headlines_from(msg, src, c)
    own = [m.lower() for m in src.get("match", [])]
    out, urls = [], set()
    for title, url in extract(msg.get("body", "")):
        # Filter raw link/label BEFORE unwrapping. No email-link HTTP requests,
        # including when do_resolve=True (legacy API compatibility).
        if ((len(title) < 8 and not SHORT_OK.search(title)) or EMAIL_ADDRESS.search(title)
                or MANAGEMENT.search(urllib.parse.unquote(url) + " " + title)):
            continue
        try:
            if skip(url, title, c, own):
                continue
            url = unwrap(url)
        except ValueError:
            continue
        # 해독된 목적지가 탈퇴·설정 주소일 수 있다 — 감싼 주소만 보고 지나치지 않는다
        if MANAGEMENT.search(urllib.parse.unquote(url)):
            continue
        if not public_link(url) or skip(url, title, c, own) or url in urls:
            continue
        urls.add(url)
        k = kind(url, c)
        if out and ((k in ("data", "media") and len(title.split()) <= 4) or title == out[-1]["title"]):   # 'See the data' 같은 짧은 링크 → 앞 소재의 원자료·이미지
            out[-1].setdefault("extra", []).append({"kind": k, "url": url, "reuse": reuse(url, c)})
            continue
        out.append({"title": title, "url": url, "kind": k, "reuse": reuse(url, c), "brand": route(title, src, c),
                    "source": src["id"], "source_name": src["name"], "msg": msg.get("id", ""), "date": msg.get("date", "")})
    return out


# ── 저장 (날짜 파일에 덧붙임, 같은 주소·같은 메일은 한 번만) ──
def _load(day: str) -> dict:
    p = OUT / f"{day}.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"day": day, "messages": [], "items": []}


def _save(d: dict) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{d['day']}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    p = OUT / f"{d['day']}.md"
    p.write_text(to_md(d), encoding="utf-8")
    return p


def message_key(message_id: str) -> str:
    return sha256(message_id.encode("utf-8")).hexdigest() if message_id else ""


def item_key(it: dict) -> tuple:
    """같은 소재인가 — 주소가 있으면 주소, 링크 없는 단신은 제목+날짜."""
    url = (it.get("url") or "").strip()
    if url:
        return ("url", url)
    return ("title", re.sub(r"\s+", " ", (it.get("title") or "")).strip().lower(),
            str(it.get("date") or "")[:10])


def add(items: list[dict], msgs: list[dict]) -> list[Path]:
    """날짜 파일에 덧붙임. 최근 2주에 이미 나온 주소는 새로 넣지 않고 '같이 다룸'에 뉴스레터만 더함."""
    days: dict[str, dict] = {}
    if OUT.exists():
        for p in sorted(p for p in OUT.glob("*.json") if not p.name.startswith("."))[-14:]:   # .lock.json 같은 잠금·보조 파일 제외 (2026-11-20)
            days[p.stem] = _load(p.stem)
    touched = set()
    for m in msgs:
        d = days.setdefault(video_day(m.get("date", "")), _load(video_day(m.get("date", ""))))
        keys = {m.get("id"), m.get("legacy_id")}
        if m.get("id") and keys.isdisjoint(x["id"] for x in d["messages"]):
            d["messages"].append({"id": m["id"], "source": m.get("source", ""), "date": m.get("date", "")})
            touched.add(d["day"])
    for it in items:
        key = item_key(it)
        old = next(((dd, x) for dd in days.values() for x in dd["items"] if item_key(x) == key), None)
        if old:
            dd, x = old
            if it["source"] != x["source"] and it["source"] not in x.setdefault("also", []):
                x["also"].append(it["source"])
                touched.add(dd["day"])
            continue
        d = days.setdefault(video_day(it["date"]), _load(video_day(it["date"])))
        d["items"].append(it)
        touched.add(d["day"])
    return [_save(days[k]) for k in sorted(touched)]


def ingest_messages(msgs: list[dict], c: dict, do_resolve: bool = True) -> list[Path]:
    items, known = [], []
    for m in msgs:
        source = which(m, c)
        if not source or NOISE_SUBJ.search(m.get("subject", "")):
            continue
        key = message_key(m.get("id", ""))
        known.append({"id": key, "legacy_id": m.get("id"), "source": source["id"], "date": m.get("date", "")})
        items.extend(items_from({**m, "id": key}, c, do_resolve))
    out = add(items, known)
    print(f"[newsletters] 메일 {len(msgs)}통 → 뉴스레터 {len(known)}통 · 소재 {len(items)}개")
    for p in out:
        print(f"[newsletters] → {p}")
    return out


def ingest(paths: list[str], do_resolve: bool = True) -> list[Path]:
    msgs = []
    for p in paths:
        x = json.loads(Path(p).read_text(encoding="utf-8"))
        msgs.extend(x if isinstance(x, list) else [x])
    return ingest_messages(msgs, cfg(), do_resolve)


def rss() -> list[Path]:
    """config 의 rss 소스 (Simon Willison 등) — 최근 2일 글."""
    import xml.etree.ElementTree as ET
    c = cfg()
    items = []
    for s in (s for s in c["sources"] if s.get("rss") and s.get("status", "subscribed") == "subscribed"):
        try:   # 피드 하나가 막혀도(403·형식 오류) 나머지는 모음 — 2026-11-18 기술·사업 RSS 11개 추가
            root = ET.fromstring(urllib.request.urlopen(urllib.request.Request(s["rss"], headers=UA), timeout=30).read())
        except Exception as e:  # noqa: BLE001
            print(f"[newsletters] RSS 건너뜀 {s['id']}: {str(e)[:80]}")
            continue
        ns = {"a": "http://www.w3.org/2005/Atom"}
        ents = root.findall("a:entry", ns) or root.findall(".//item")
        for e in ents:
            title = (e.findtext("a:title", None, ns) or e.findtext("title") or "").strip()
            link = e.find("a:link", ns)
            url = link.get("href") if link is not None else (e.findtext("link") or "")
            date = e.findtext("a:updated", None, ns) or e.findtext("a:published", None, ns) or e.findtext("pubDate") or ""
            try:
                t = datetime.fromisoformat(date.replace("Z", "+00:00"))
            except ValueError:
                try:   # RSS 2.0 pubDate (RFC 822: "Thu, 12 Nov 2026 18:06:26 GMT") — 2026-11-17 SemiAnalysis 피드에서 발견
                    from email.utils import parsedate_to_datetime
                    t = parsedate_to_datetime(date)
                except (TypeError, ValueError):
                    continue
            if t.tzinfo is None:   # 시간대 없는 날짜 (디일렉 등 국내 피드) → 한국 시간으로 봄
                t = t.replace(tzinfo=timezone(timedelta(hours=9)))
            if datetime.now(timezone.utc) - t > timedelta(days=2) or not title or not url:
                continue
            try:
                url = unwrap(url)
            except ValueError:
                continue
            if not public_link(url, strict=False) or EMAIL_ADDRESS.search(title):
                continue
            items.append({"title": _clean(title), "url": url, "kind": kind(url, c), "reuse": reuse(url, c), "brand": route(title, s, c),
                          "source": s["id"], "source_name": s["name"], "msg": "rss", "date": t.isoformat()})
    out = add(items, [])
    print(f"[newsletters] RSS 소재 {len(items)}개")
    return out


# ── 보기 ──
def alarm_suffix(x: dict) -> str:
    """링크 없는 단신 행의 꼬리: ` (알림 11-20 17:18)`."""
    if (x.get("url") or "").strip() or not x.get("alarm"):
        return ""
    return f" (알림 {x['alarm']})"


def title_cell(x: dict) -> str:
    return f"{x['title'].replace('|', '/')}{alarm_suffix(x)}"


def to_md(d: dict) -> str:
    day = d["day"]
    L = [f"# 뉴스레터 소재 — {day[:4]}-{day[4:6]}-{day[6:]} 영상 몫", "",
         "> 자동 정리한 **단서**입니다. 문장을 대본·화면에 옮기지 않고, 숫자·발언은 링크를 따라 1차 출처로 확인합니다 (docs/36).",
         f"> 메일 {len(d['messages'])}통 · 소재 {len(d['items'])}개 · 한국 08:00 이후 도착분은 다음 날 파일", ""]
    for b in BRANDS:
        its = [x for x in d["items"] if x["brand"] == b]
        if not its:
            continue
        L += [f"## {BRAND_KO[b]} ({len(its)})", "", "| 소재 (원래 제목) | 원문·기사 | 원자료·통계 | 영상·이미지 | 재사용 조건 | 뉴스레터 |", "|---|---|---|---|---|---|"]
        its.sort(key=lambda x: (-len(x.get("also", [])), ["primary", "data", "media", "news"].index(x["kind"])))
        for x in its:
            col = {"primary": [], "news": [], "data": [], "media": []}
            for lk in [x] + x.get("extra", []):
                if not (lk.get("url") or "").strip():
                    continue   # 링크 없는 단신 — 빈 링크 괄호를 만들지 않는다
                host = urllib.parse.urlsplit(lk["url"]).netloc.removeprefix("www.")
                col[lk["kind"]].append(f"[{host}{' (1차)' if lk['kind'] == 'primary' else ''}]({lk['url']})")
            cell = lambda *ks: " ".join(v for k in ks for v in col[k]) or "—"
            rs = " / ".join(dict.fromkeys([x["reuse"]] + [e["reuse"] for e in x.get("extra", [])]))
            also = f" (+{', '.join(x['also'])})" if x.get("also") else ""
            L.append(f"| {title_cell(x)} | {cell('primary', 'news')} | {cell('data')} | {cell('media')} | {rs.replace('|', '/')} | {x['source_name']}{also} |")
        L.append("")
    return "\n".join(L)


def section(brands: tuple[str, ...], day: str, n: int = 15) -> str:
    """daily_brief.md 에 붙일 '⑦ 뉴스레터 화제'. day 는 YYYY-MM-DD 또는 YYYYMMDD (영상 날짜)."""
    d = _load(day.replace("-", ""))
    its = [x for x in d["items"] if x["brand"] in brands]
    L = ["", f"## ⑦ 뉴스레터 화제 ({'·'.join(BRAND_KO[b] for b in brands)}) — 단서, 1차 출처로 확인"]
    if not its:
        L.append(f"(이 날짜 뉴스레터 소재 없음 — `inbox/newsletters/{d['day']}.md`. 수집: docs/36)")
        return "\n".join(L) + "\n"
    its.sort(key=lambda x: (-len(x.get("also", [])), ["primary", "data", "media", "news"].index(x["kind"])))
    for x in its[:n]:
        also = f", 같이 다룸: {', '.join(x['also'])}" if x.get("also") else ""
        tail = f" · {x['url']}" if (x.get("url") or "").strip() else alarm_suffix(x)
        L.append(f"- [{KIND_KO[x['kind']]}] {x['title']} — {x['source_name']}{also}{tail}")
    if len(its) > n:
        L.append(f"- … 나머지 {len(its) - n}개: `inbox/newsletters/{d['day']}.md`")
    return "\n".join(L) + "\n"


def show(brand: str = "", days: int = 1) -> None:
    today = datetime.now(KST).date()
    for k in range(days):
        day = (today - timedelta(days=k)).strftime("%Y%m%d")
        d = _load(day)
        its = [x for x in d["items"] if not brand or x["brand"] == brand]
        if not its:
            continue
        print(f"# {day} ({len(its)})")
        for x in its:
            print(f"  [{BRAND_KO[x['brand']]}/{KIND_KO[x['kind']]}] {x['title'][:80]} — {x['source']} · "
                  f"{x['url'] or '링크 없음'}")


def sources() -> None:
    for s in cfg()["sources"]:
        print(f"  {s['status']:10s} | {s['name'][:28]:28s} | {','.join(s['brands']):24s} | {s['cadence']:8s} | 도착 {s['arrives']}")


def main(argv: list[str]) -> None:
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return
    cmd, rest = argv[0], argv[1:]
    if cmd == "ingest":
        ingest([a for a in rest if not a.startswith("--")], do_resolve="--no-resolve" not in rest)
    elif cmd == "rss":
        rss()
    elif cmd == "show":
        brand = rest[rest.index("--brand") + 1] if "--brand" in rest else ""
        days = int(rest[rest.index("--days") + 1]) if "--days" in rest else 1
        show(brand, days)
    elif cmd == "sources":
        sources()
    else:
        print(__doc__)
