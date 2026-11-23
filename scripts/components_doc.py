"""구성요소 목록(styles/components.yaml)·연출 기법(styles/techniques.yaml) → 만드는 법 한 장 (styles/components.md).

2026-11-20 사용자: "다른 목록들도 마찬가지로 해줘" — 장면 종류처럼 다른 목록도 무엇·언제·켜는 법·구현·움직이는 예시를 한곳에.
목록을 고치면 다시: python scripts/components_doc.py
"""
from __future__ import annotations
import pathlib
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
GALLERY = "https://claude.ai/artifact/K4CRgsyTYsWGCDw5RoCtam"


def esc(s) -> str:
    return str(s or "").replace("|", "／").replace("\n", " ")


def main() -> pathlib.Path:
    comp = yaml.safe_load((ROOT / "styles/components.yaml").read_text(encoding="utf-8"))
    tech = yaml.safe_load((ROOT / "styles/techniques.yaml").read_text(encoding="utf-8"))
    techs = tech.get("techniques", tech)
    techs = techs if isinstance(techs, list) else list(techs.values())
    out = ["<!-- scripts/components_doc.py 가 만든 파일 — 목록(styles/components.yaml·techniques.yaml)을 고친 뒤 다시 만드세요 -->",
           "# 구성요소별 만드는 법 — 화면·글자·그래픽·카메라·전환·소리",
           "",
           "> 사용자 2026-11-20: \"다른 목록들도 마찬가지로 해줘\" — 영상 = 구성요소 카테고리마다 고른 스타일의 조합(`styles/components.yaml`).",
           f"> **움직이는 예시**: 화풍 목록 페이지({GALLERY}) 의 카테고리 칸 ▶ (`media` 열의 영상). 장면 종류는 `styles/hybrid/scenes/`, 화풍은 `styles/looks/README.md`.",
           "",
           "고르는 법: `python -m ytflow look <프로젝트> --set <카테고리>=<id>` → `edit.yaml` 의 `look` (이 영상의 기본값, 장면마다 바꿀 수 있음).",
           ""]
    for cat in comp["categories"]:
        src = cat.get("source") or {}
        out += [f"## {cat['name']} (`{cat['key']}`)", "", f"{esc(cat.get('what'))}", ""]
        if "list" in src:
            out += ["| id | 이름 | 어떻게 보이나 | 언제 | 구현·값 | 예시 |", "|---|---|---|---|---|---|"]
            for k, v in src["list"].items():
                v = v or {}
                impl = v.get("impl") or (f"`{v['family']}` {v.get('weight', '')}" if v.get("family") else "") or \
                    (", ".join(f"{a}={b}" for a, b in (v.get("sub") or {}).items()) if v.get("sub") else "")
                media = f"`{v['media']}`" if v.get("media") else "—"
                st = f" ({v['status']})" if v.get("status") else ""
                out.append(f"| `{k}` | {esc(v.get('name'))}{st} | {esc(v.get('look'))} | {esc(v.get('fits'))}"
                           f"{(' · 피함: ' + esc(v['avoid'])) if v.get('avoid') else ''} | {esc(impl)} | {media} |")
        elif "techniques" in src:
            groups = src["techniques"]
            rows = [t for t in techs if t.get("group") in groups]
            out += ["| 기법 | 상태 | 어떻게 보이나 | 언제 | 주의 | 만드는 법 |", "|---|---|---|---|---|---|"]
            for t in rows:
                out.append(f"| {esc(t.get('name'))} | {esc(t.get('status'))} | {esc(t.get('look'))} | {esc(t.get('use_when'))} | "
                           f"{esc(t.get('caution'))} | {esc(t.get('how'))} |")
        elif "looks" in src:
            out.append(f"→ 화풍 목록 `styles/looks.yaml` 의 `{src['looks']}` — 만드는 법은 `styles/looks/README.md`.")
        elif "scenes" in src:
            out.append("→ 장면 종류마다 `styles/hybrid/scenes/<장면>.md` (박자표·대본 예·예시 영상), 실제 완성본 예시는 `real-examples.md`.")
        elif "bgm" in src:
            out.append(f"→ 배경음 목록 `{src['bgm']}` (곡·라이선스·어울리는 분위기). 기본은 없음 — 어울리는 곡이 확실할 때만(05 §0-5).")
        out.append("")
    p = ROOT / "styles/components.md"
    p.write_text("\n".join(out), encoding="utf-8")
    return p


if __name__ == "__main__":
    print(main())
