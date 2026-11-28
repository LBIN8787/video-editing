"""이야기 대본·말투 측정: 인기 이야기형 영상 자막 vs 우리 대본.
같은 잣대로: 말 속도, 종결 어미 분포, 질문, 인용(대사), 현재/과거, 접속(그리고 vs 그런데·하지만 vs 그러자·결국), 시간·장면 표지, 시청자 부르기, 짧은 문장 비율."""
import re, json, glob, pathlib, statistics as st, sys
SUBS = pathlib.Path(r"E:/ytflow-local/books-video/research/subs"); W = pathlib.Path(r"D:/ytflow/wt-books/projects")
NAME = {"tKOVKfoQZ18": "디바제시카(실화 사건)", "X7E-qbnB3P8": "지무비(영화 리뷰)", "bDQ9nfrMeUo": "무드킹(결말포함)", "y0sWO31MH8E": "미스스한(괴담 실화)",
        "EUJXAsQVCuQ": "이종범(스토리캠프)", "nxDSK2qv_Ww": "명작속주인공심리(노르웨이)", "-8-u_L54hb8": "등불켜진책장(가시나무새)",
        "7rPnDxkyHCI": "역사노트(유럽사)", "2fZG76vonhY": "썬킴(세계사)"}
def vtt(path, limit=600):
    t = open(path, encoding="utf-8").read(); out, prev = [], ""
    for a, txt in re.findall(r"(\d+:\d+:\d+\.\d+) --> [^\n]+\n(.+?)(?=\n\n|\Z)", t, re.S):
        h, m, s = a.split(":"); sec = int(h) * 3600 + int(m) * 60 + float(s)
        if sec > limit: break
        for line in re.sub(r"<[^>]+>", "", txt).split("\n"):
            line = line.strip()
            if line and line != prev and line not in prev: out.append(line); prev = line
    return " ".join(out), min(limit, sec)
# 문장 나누기: 문장부호 또는 종결 어미 뒤 띄어쓰기
END = r"(?:습니다|입니다|니다|어요|아요|에요|예요|죠|지요|거든요|는데요|잖아요|네요|까요|나요|가요|군요|요|다|까|니|지)"
def sents(text):
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"([.?!])\s+", r"\1\n", text)
    text = re.sub(r"(" + END + r")\s+(?=[가-힣A-Z0-9\"'“‘])", r"\1\n", text)
    parts = text.split("\n")
    return [p.strip() for p in parts if len(p.strip()) > 1]
def measure(text, secs):
    S = sents(text); n = len(S) or 1; chars = len(text.replace(" ", ""))
    def rate(pat): return round(sum(1 for s in S if re.search(pat, s)) / n * 100)
    words = len(text.split())
    def per1k(pat): return round(len(re.findall(pat, text)) / max(1, chars) * 1000, 1)
    return {
        "분당 글자": round(chars / secs * 60), "문장 길이 중앙(자)": round(st.median([len(s.replace(' ', '')) for s in S])),
        "짧은 문장(15자↓)%": rate(r"^.{0,15}$"),
        "~습니다·입니다%": rate(r"(습니다|입니다|니다)[.?!]?$"), "~요·~죠·~거든요%": rate(r"(요|죠)[.?!]?$"), "~다(평서)%": rate(r"[^니]다[.?!]?$"),
        "질문%": rate(r"(\?|까요|을까|ㄹ까|나요|가요)[.?!]?$"), "대사·인용%": rate(r"[\"“”']|라고|하고 (말|묻)|라며|냐고|자고"),
        "과거형 서술%": rate(r"(었|았|였|했)(습니다|어요|다|죠)"), "현재형 서술%": rate(r"(ㅂ니다|합니다|습니다|입니다|는데요|어요|아요)$") ,
        "그리고(나열) /1k자": per1k(r"그리고|그다음|그 다음"), "그런데·하지만(반전) /1k자": per1k(r"그런데|하지만|그러나|근데|그렇지만"),
        "그러자·결국(인과) /1k자": per1k(r"그러자|결국|그래서|그 결과|그러니까|때문에"),
        "시간·장면 표지 /1k자": per1k(r"그때|그날|그 순간|바로 그때|그 밤|다음 날|며칠 뒤|몇 시간 뒤|그로부터|어느 날"),
        "시청자 부르기 /1k자": per1k(r"여러분|당신|우리는|우리가|상상해"),
    }
rows = {}
for f in sorted(SUBS.glob("*.ko.vtt")):
    vid = f.name.split(".")[0]; text, secs = vtt(f); rows[NAME.get(vid, vid)] = measure(text, secs)
# 우리 대본
def ours_md(p):
    t = open(p, encoding="utf-8").read().split("## 대본 점검")[0]; L = []
    for line in t.split("\n"):
        s = line.strip()
        if not s or s.startswith(("🎨", "📷", "🗺", "📄", "▣", "---", "#", "|", "(", "⟪", "템플릿", "표기", "화풍")): continue
        L.append(re.sub(r"\s*\[F[^\]]*\]|\s*🔍", "", s))
    return " ".join(L)
def ours_json(p):
    R = json.load(open(p, encoding="utf-8")); return " ".join(l["say"] for s in R["sections"] for l in s["lines"])
for name, path, kind, secs in [("우리 v1 섀클턴", W / "20261127-story-shackleton-endurance/02_script/script.md", "md", 614),
                               ("우리 v1 댜틀로프", W / "20261127-story-dyatlov-pass/02_script/script.md", "md", 635),
                               ("우리 죄와 벌", W / "20261127-books-crime-and-punishment/02_script/script.md", "md", 840),
                               ("우리 v2 에덴 재현", W / "20261127-ref-eden-remake/02_script/remake_full.json", "json", 1271)]:
    text = ours_md(path) if kind == "md" else ours_json(path)
    rows[name] = measure(text, secs)
keys = list(next(iter(rows.values())).keys())
print("| 영상 | " + " | ".join(keys) + " |"); print("|---" * (len(keys) + 1) + "|")
for k, v in rows.items(): print(f"| {k} | " + " | ".join(str(v[x]) for x in keys) + " |")
json.dump(rows, open(r"E:/ytflow-local/books-video/research/tone_metrics.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
