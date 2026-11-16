"""styles/motion-catalog.yaml → docs/38-motion-catalog.md (읽는 판). 카탈로그를 고치면 다시 실행.

    python scripts/motion_catalog.py
"""
from __future__ import annotations

from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CAT = ROOT / "styles" / "motion-catalog.yaml"
OUT = ROOT / "docs" / "38-motion-catalog.md"
STATUS = {"have": "✅ 있음", "partial": "◐ 비슷한 것", "registry": "📦 블록 있음", "candidate": "○ 만들어야", "hold": "⏸ 보류"}

HEAD = """# 38. 모션그래픽 카탈로그 — 어떤 것이 있고, 어떤 상황에 쓰나 (2026-11-16)

> 사용자: "모션그래픽도 그래픽별로 스타일을 조사하고 분류해줘" · "즉 어떤 상황에 어떤 모션그래픽을 사용하고 어떤 모션그래픽들이 존재하는지 정리하고싶어"

**원본은 `styles/motion-catalog.yaml`** (이 문서는 `python scripts/motion_catalog.py` 로 만든 읽는 판 — 고칠 때는 YAML 만).
조사 범위: 설치된 HyperFrames 레지스트리 블록 448개(태그로 10종류에 나눔), 이 저장소의 렌더러·장면 종류·스타일, 모션그래픽 스타일 분류 글(아래 출처).
`docs/32`·`styles/techniques.yaml` 은 더 작은 **연출 기법**(글자 쪼개기·모프…), 이 문서는 화면 한 장을 채우는 **모션그래픽 스타일**이다. `docs/37` 은 그것을 **매끄럽게** 만드는 법.

## 0. 한눈에
"""

PICK = """
## 1. 고르는 순서
{steps}

예: "엔비디아 매출이 전년보다 94% 늘었다" → 상황 `metric` → 실적 발표 원문이 있으면 `source-bite` 뒤에, 없으면 `big-number` → 시장 채널이니 `stat-tiles`·`dark-dashboard` 쪽 → 이 1분에 이미 강조를 썼으면 `big-number` 대신 조용한 `line-draw`.
"""

SOURCES = """
## 출처
- HyperFrames 레지스트리 0.8.190 (`hyperframes catalog --json`, 448개, Apache-2.0) — 블록 이름은 `hyperframes add <이름>` 로 설치
- 모션그래픽 스타일 분류: [b2w — 12 motion graphics styles](https://www.b2w.tv/blog/types-of-motion-graphics), [Yans Media — motion graphics styles](https://www.yansmedia.com/blog/best-motion-graphics-styles), [Yans Media — types & use cases](https://www.yansmedia.com/blog/types-of-motion-graphics), [ManyPixels — 9 types](https://www.manypixels.co/blog/motion-design/types), [Blue Forest — animation styles](https://blueforeststudios.squarespace.com/definitive-guide-to-animation-styles), [Biteable — animation styles](https://biteable.com/blog/animation-styles-types/), [moonb — 12 animation styles](https://www.moonb.io/blog/animation-styles), [Yum Yum Videos — animation styles](https://www.yumyumvideos.com/types_of_animation_styles)
  - 공통 결론: 글자(키네틱)·화이트보드가 가장 싸고 빠름, 인포그래픽은 숫자·보고서, 아이소메트릭은 복잡한 구조, 2.5D 는 3D 의 싼 대안(층 나누기가 가장 어려움). 대부분 제작사 블로그라 홍보 성격이 있다.
- 설명형 유튜브 채널의 화면 문법(지도 설명·일관된 일러스트): [Johnny Harris 의 시각 이야기](https://medium.com/@LMK_writing/how-johnny-harris-mastered-visual-storytelling-on-youtube-343ddf9160ec), [Vox 식 지도 애니메이션](https://rizzle.com/blog/post/how-to-create-an-engaging-map-animation-channel-like-vox-youtube), [Digiday — 설명 영상](https://digiday.com/media/publishers-flocking-explainer-videos/), [vidpros — 설명 채널](https://vidpros.com/best-explainer-youtube-channels/) — 레퍼런스 채널의 그림·캐릭터는 복제하지 않고 구조만 (AGENTS 스타일 규칙)
"""


def main():
    c = yaml.safe_load(CAT.read_text(encoding="utf-8"))
    sit_names = {k: v["name"] for k, v in (yaml.safe_load((ROOT / "manual/situations.yaml").read_text(encoding="utf-8"))["situations"]).items()}
    by_id, fam_of = {}, {}
    for fk, f in c["families"].items():
        for s in f["styles"]:
            by_id[s["id"]] = s
            fam_of[s["id"]] = f["name"]
    cnt = Counter(s["status"] for s in by_id.values())
    L = [HEAD]
    L.append(f"- 그래픽 종류 **{len(c['families'])}** · 모션그래픽 스타일 **{len(by_id)}** · 그림체 **{len(c.get('looks') or [])}** (§6) — "
             + " · ".join(f"{STATUS[k]} {cnt.get(k, 0)}" for k in STATUS))
    L.append("- ✅ 우리 렌더러에 있음 · ◐ 비슷한 것 있음 · 📦 HyperFrames 블록으로 바로 가능(설치됨, 연결만) · ○ 만들어야 함 · ⏸ 지금까지 피드백과 부딪혀 보류")
    L.append("- 모두 '스타일 기본값' 층 — 금지·MUST 아님. 강조 예산(1분 1번)·카메라 계열 횟수 안에서.\n")
    L.append("| 그래픽 종류 | 무엇에 | 스타일 |\n|---|---|---|")
    for f in c["families"].values():
        L.append(f"| **{f['name']}** | {f['plain']} | {' · '.join(s['name'] for s in f['styles'])} |")
    L.append(PICK.format(steps="\n".join(f"{i + 1}. {s}" for i, s in enumerate(c["pick_order"]))))
    L.append("## 2. 상황 → 모션그래픽 (1순위부터)\n상황은 `manual/situations.yaml` (대본 한 박자가 하는 일). `edit-plan` 이 박자마다 상황을 찾는다.\n")
    L.append("| 상황 | 1순위 | 다음 후보 |\n|---|---|---|")
    for k, ids in c["situations"].items():
        first = by_id[ids[0]]
        rest = " · ".join(f"{by_id[i]['name']} {STATUS[by_id[i]['status']][0]}" for i in ids[1:])
        L.append(f"| `{k}` {sit_names.get(k, '')} | **{first['name']}** {STATUS[first['status']][0]} | {rest} |")
    L.append("\n## 3. 채널마다 기본 얼굴\n| 채널 | 얼굴 | 먼저 고르는 것 | 덜 쓰는 것 |\n|---|---|---|---|")
    for k, ch in c["channels"].items():
        L.append(f"| {k} | {ch['face']} | {' · '.join(by_id[i]['name'] for i in ch['lean'])} | {' · '.join(by_id[i]['name'] for i in ch['less'])} |")
    L.append("\n## 4. 그래픽 종류별 전체 목록")
    for fk, f in c["families"].items():
        L.append(f"\n### {f['name']} (`{fk}`)\n{f['plain']}\n")
        L.append("| 스타일 | 어떻게 보이나 | 상황 | 우리 구현 | HyperFrames 블록 | 상태 |\n|---|---|---|---|---|---|")
        for s in f["styles"]:
            when = ", ".join(f"`{w}`" for w in s.get("when", [])) or "—"
            have = ", ".join(f"`{h}`" for h in s.get("have", [])) or "—"
            hf = ", ".join(s.get("hf", [])[:5]) or "—"
            extra = "".join(f"<br>⚠ {s['avoid']}" for _ in [0] if s.get("avoid")) + "".join(f"<br>※ {s['note']}" for _ in [0] if s.get("note"))
            L.append(f"| **{s['name']}** `{s['id']}` | {s['look']}{extra} | {when} | {have} | {hf} | {STATUS[s['status']]} |")
    todo = [s for s in by_id.values() if s["status"] in ("registry", "candidate")]
    L.append("\n## 5. 다음에 붙일 것 (📦·○)\n먼저: 상황 표의 1순위인데 아직 없는 것 → 그다음 채널 얼굴에 들어 있는 것.\n")
    first_ids = {v[0] for v in c["situations"].values()}
    for s in sorted(todo, key=lambda s: (s["id"] not in first_ids, s["status"] != "registry")):
        L.append(f"- **{s['name']}** ({fam_of[s['id']]}, {STATUS[s['status']]}) — {', '.join(s.get('hf', [])[:3]) or '블록 없음'}"
                 + (" · *상황 1순위*" if s["id"] in first_ids else ""))
    looks = c.get("looks") or []
    if looks:
        L.append("\n## 6. 그림체 (애니메이션 스타일) — 두 번째 축\n"
                 "위 §4 는 **무엇을** 그리나(글자·숫자·지도…), 여기는 **어떤 그림체로** 그리나. 둘을 곱해 화면 하나: 예) 숫자·데이터 × 아이소메트릭, 그림·인물 × 클레이.\n"
                 "견본: `python scripts/motion_styles_reel.py` — 같은 장면(동전이 떨어져 성장 탑이 쌓인다)을 12가지 그림체로 렌더 (43초, 1080p).\n"
                 "'끊는 움직임'(⏯)은 일부러 프레임을 끊는 그림체라 `motion-qa` 의 멈칫·점프가 정상이다.\n")
        L.append("| 그림체 | 생김새 | 언제 | 채널 | 제작 부담 | 상태 |\n|---|---|---|---|---|---|")
        for lk in looks:
            st = lk.get("status") or ("have" if lk.get("have") else "candidate")
            extra = (f"<br>⚠ {lk['caution']}" if lk.get("caution") else "") + (" ⏯" if lk.get("stepped") else "")
            have = (" · 우리: " + ", ".join(f"`{h}`" for h in lk["have"])) if lk.get("have") else ""
            L.append(f"| **{lk['name']}** `{lk['id']}` | {lk['look']}{extra} | {lk['when']} | {', '.join(lk.get('fit', []))} | {lk.get('cost', '')} | {STATUS[st]}{have} |")
    L.append(SOURCES)
    OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"→ {OUT.relative_to(ROOT)} ({len(by_id)} 스타일)")


if __name__ == "__main__":
    main()
