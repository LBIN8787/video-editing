"""시사 채널 성과 원인 나누기 — 구독자(채널) 덕 / 소재 덕 / 편집·포장 덕 (docs/18 §6).
    python scripts/issues_attribution.py   (먼저 scripts/issues_research.py 로 .cache/issues/channels.json)
방법
 1) 채널 효과: log(조회수) 분산 중 채널 차이로 설명되는 몫(R²). 채널 = 구독자 + 채널 브랜드 + 고정 편집 스타일.
 2) 구독자 대비 퍼짐: log(조회수 중앙값) ~ log(구독자) 직선에서 위/아래 → 같은 구독자 수 대비 '채널 포맷·편집'의 힘.
 3) 소재 효과: 같은 소재(나라·인물·기업·주제어)를 다룬 영상의 채널 내 배수. 2개 채널 이상에서 함께 높으면 '소재 덕'.
 4) 영상별 판정: 배수 ≥ 2 인 영상을 — 소재가 다른 채널에서도 강함(소재형) / 소재는 평범한데 이 영상만(포장·편집형) / 둘 다(혼합).
최신 5편(조회수가 아직 쌓이는 중)은 채널마다 뺀다.
"""
import json, math, re, statistics as st
from collections import defaultdict
from pathlib import Path

TOPICS = {"러시아": r"러시아|푸틴|모스크바", "이란": r"이란|하메네이", "이스라엘": r"이스라엘|네타냐후|가자", "북한": r"북한|김정은|김주애|김여정|평양",
          "미국·트럼프": r"트럼프|미국|백악관", "중국": r"중국|시진핑|베이징", "일본": r"일본|도쿄|엔화", "사우디·중동": r"사우디|네옴|중동|예멘|후티",
          "베네수엘라·남미": r"베네수엘라|마두로|아르헨티나|브라질", "유럽": r"프랑스|독일|영국|스웨덴|유럽", "인도·동남아": r"인도|베트남|동남아|태국|필리핀",
          "전쟁·군사": r"전쟁|공습|미사일|군대|폭격|반군", "경제 위기·몰락": r"몰락|붕괴|망했|망함|무너|위기|파산|추락",
          "AI·빅테크": r"AI|인공지능|엔비디아|오픈AI|챗GPT|빅테크", "기업 근황": r"나이키|쿠팡|삼성|애플|테슬라|이케아|유니클로|만두|브랜드",
          "부동산·물가": r"집값|부동산|전세|월세|물가|가격|비싸", "일자리·청년": r"청년|취업|해고|일자리|MZ|2030|월급|직장",
          "건강·의료": r"암|병원|건강|의사|응급|질환|증상", "사건·범죄": r"살인|범죄|사건|방화|수사|구속|사기",
          "정치(국내)": r"대통령|국회|탄핵|선거|여당|야당|정부"}


def main():
    d = json.loads(Path(".cache/issues/channels.json").read_text(encoding="utf-8"))
    V = []
    for ch, v in d.items():
        vids = v["videos"][5:]                       # 최신 5편 제외
        med = st.median([x["views"] for x in vids if x["views"]])
        for x in vids:
            if x["views"] > 0:
                V.append(dict(x, ch=ch, subs=v["subs"], xr=x["views"] / med, lv=math.log10(x["views"])))
    # 1) 채널 효과 R²
    mu = st.mean([v["lv"] for v in V])
    tot = sum((v["lv"] - mu) ** 2 for v in V)
    cm = {c: st.mean([v["lv"] for v in V if v["ch"] == c]) for c in d}
    within = sum((v["lv"] - cm[v["ch"]]) ** 2 for v in V)
    r2 = 1 - within / tot
    print(f"## 1. 조회수 차이 중 '어느 채널이냐'로 설명되는 몫: {r2 * 100:.0f}%  (나머지 {100 - r2 * 100:.0f}% 는 채널 안 차이 = 소재·포장·편집·시기)\n")
    # 2) 구독자 대비 퍼짐
    xs = [math.log10(d[c]["subs"]) for c in d]
    ys = [math.log10(st.median([v["views"] for v in V if v["ch"] == c])) for c in d]
    mx, my = st.mean(xs), st.mean(ys)
    b = sum((a - mx) * (c - my) for a, c in zip(xs, ys)) / sum((a - mx) ** 2 for a in xs)
    a0 = my - b * mx
    print("## 2. 구독자 수 대비 퍼짐 (같은 구독자 수 채널보다 몇 배 더 보나 = 채널 포맷·편집·브랜드의 힘)\n")
    print("| 채널 | 구독자 | 조회수 중앙값 | 구독자로 기대되는 값 | 배수 |\n|---|---|---|---|---|")
    eff = {}
    for c, x, y in zip(d, xs, ys):
        exp = 10 ** (a0 + b * x)
        eff[c] = 10 ** y / exp
        print(f"| {c} | {d[c]['subs'] / 1e4:.0f}만 | {10 ** y / 1e4:.1f}만 | {exp / 1e4:.1f}만 | **{eff[c]:.2f}** |")
    print(f"\n(기울기 {b:.2f}: 구독자가 10배면 조회수 중앙값은 약 {10 ** b:.1f}배 — 구독자 효과는 있지만 비례하지 않음)\n")
    # 3) 소재 효과
    print("## 3. 소재 효과 (채널 안 배수 중앙값, 소재를 다룬 채널 수)\n")
    print("| 소재 | 영상 수 | 다룬 채널 | 배수 중앙값 | 채널별 배수 중앙값 | 판정 |\n|---|---|---|---|---|---|")
    tl = {}
    for t, pat in TOPICS.items():
        sel = [v for v in V if re.search(pat, v["title_ko"] or "")]
        if len(sel) < 5:
            continue
        per = defaultdict(list)
        for v in sel:
            per[v["ch"]].append(v["xr"])
        chm = {c: st.median(x) for c, x in per.items()}
        hi = sum(1 for m in chm.values() if m >= 1.2)
        med = st.median([v["xr"] for v in sel])
        tl[t] = med
        verdict = "**소재가 끈다**" if med >= 1.3 and hi >= 2 else ("한 채널만 강함" if med >= 1.3 else ("약함" if med < 0.9 else "보통"))
        print(f"| {t} | {len(sel)} | {len(per)} | {med:.2f} | " + ", ".join(f"{c.split()[0]} {m:.1f}" for c, m in sorted(chm.items(), key=lambda z: -z[1])) + f" | {verdict} |")
    # 4) 영상별 판정
    print("\n## 4. 잘 된 영상(채널 안 배수 ≥ 2.5)의 원인 판정\n")
    print("| 채널 | 배수 | 제목 | 소재(소재 배수) | 판정 |\n|---|---|---|---|---|")
    out = []
    for v in sorted(V, key=lambda z: -z["xr"]):
        if v["xr"] < 2.5:
            break
        ts = [t for t, pat in TOPICS.items() if re.search(pat, v["title_ko"] or "") and t in tl]
        best = max((tl[t] for t in ts), default=None)
        if best is None:
            kind = "포장·편집형 (분류된 소재 없음 — 생활·사람 이야기)"
        elif best >= 1.3:
            kind = "소재형 + 포장" if v["xr"] >= best * 2.5 else "**소재형**"
        else:
            kind = "**포장·편집형** (소재는 평범)"
        out.append((v, ts, best, kind))
        print(f"| {v['ch'].split()[0]} | {v['xr']:.1f} | {(v['title_ko'] or '')[:42]} | {', '.join(ts) or '-'} ({best:.2f}) | {kind} |" if best else
              f"| {v['ch'].split()[0]} | {v['xr']:.1f} | {(v['title_ko'] or '')[:42]} | - | {kind} |")
    from collections import Counter
    c = Counter(k.split(" ")[0].strip("*") for _, _, _, k in out)
    print(f"\n판정 집계: {dict(c)} (총 {len(out)}편)")
    Path(".cache/issues/attribution.json").write_text(json.dumps({"r2_channel": r2, "efficiency": eff, "topic_lift": tl}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
