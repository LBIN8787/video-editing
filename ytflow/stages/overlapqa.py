"""글자 겹침 검사 — 렌더된 장면 HTML 을 박자 끝마다 멈춰 놓고, 보이는 글자 상자끼리·자막 자리와 겹치는지 실제 위치로 잰다.

2026-11-20 사용자: "자막이랑 영상 글씨가 겹치거나 전체적으로 글씨들이 겹치는 경우가 잦습니다."
layout_qa.json(렌더 전 자체 점검)은 자막 자리를 모르고, 화면에 실제로 그려진 글자 크기도 모른다 → 렌더된 HTML 로 잰다.

    python scripts/overlap_scan.py <프로젝트> [--scenes 6,11]     (hybrid 렌더 끝에 자동으로 돎 → 05_edit/overlap_qa.json)

자막 자리: subs.ass 의 Sub 스타일(글자 크기·아래 여백·상자 테두리)로 한 줄 자막 상자 위쪽 y 를 계산 (기본 약 y 940 아래).
판정: ① 글자 상자 두 개가 겹치는 넓이가 작은 쪽의 12% 이상 ② 글자 상자 아래쪽이 자막 위쪽보다 아래 (출처 줄·자막 자체 제외).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

JS = r"""
(t) => {
  const tl = window.__timelines && window.__timelines.main;
  if (tl) { tl.seek(t, false); }
  const out = [];
  const op = (el) => { let o = 1; for (let e = el; e && e.nodeType === 1; e = e.parentElement) {
      const cs = getComputedStyle(e); if (cs.display === 'none' || cs.visibility === 'hidden') return 0; o *= parseFloat(cs.opacity || '1'); } return o; };
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const seen = new Set();
  while (walker.nextNode()) {
    const n = walker.currentNode; const s = n.textContent.replace(/\s+/g, ' ').trim();
    if (!s) continue;
    let el = n.parentElement; if (!el || seen.has(el)) continue;
    if (el.closest('script,style')) continue;
    const r = document.createRange(); r.selectNodeContents(n); const b = r.getBoundingClientRect();
    if (b.width < 4 || b.height < 4) continue;
    const o = op(el); if (o < 0.15) continue;
    seen.add(el);
    out.push({text: s.slice(0, 40), x: b.left, y: b.top, w: b.width, h: b.height, o: +o.toFixed(2),
              label: !!el.closest('.lbl,[data-role=label]') || (b.top < 50), _el: el});
  }
  // 카드·사진 상자: 바탕색·그림자가 있거나 그림인 요소 (화면 전체 바탕은 뺌)
  const boxes = [];
  for (const el of document.querySelectorAll('#root *')) {
    if (el.matches('script,style,span,svg *')) continue;
    const cs = getComputedStyle(el);
    const solid = (cs.backgroundColor && !/rgba\(\d+, \d+, \d+, 0\)|transparent/.test(cs.backgroundColor)) || cs.boxShadow !== 'none' || el.tagName === 'IMG' || el.tagName === 'VIDEO';
    if (!solid) continue;
    const b = el.getBoundingClientRect();
    if (b.width < 40 || b.height < 30 || (b.width > 1500 && b.height > 800)) continue;
    if (op(el) < 0.15) continue;
    boxes.push({el, x: b.left, y: b.top, w: b.width, h: b.height});
  }
  for (const it of out) {
    it.cover = [];
    for (const bx of boxes) {
      if (bx.el.contains(it._el) || it._el.contains(bx.el)) continue;
      const ix = Math.max(0, Math.min(it.x + it.w, bx.x + bx.w) - Math.max(it.x, bx.x));
      const iy = Math.max(0, Math.min(it.y + it.h, bx.y + bx.h) - Math.max(it.y, bx.y));
      const f = ix * iy / (it.w * it.h);
      if (ix * iy < 60) continue;
      // 글자 위 여러 점에서 맨 위에 보이는 것이 이 카드면 '가려짐'
      let hidden = false;
      const cx = (Math.max(it.x, bx.x) + Math.min(it.x + it.w, bx.x + bx.w)) / 2;   // 겹친 부분 가운데도 본다
      for (const px of [it.x + it.w * 0.1, it.x + it.w * 0.5, it.x + it.w * 0.9, cx]) {
        const top = document.elementFromPoint(px, it.y + it.h / 2);
        if (top && (bx.el === top || bx.el.contains(top)) && !(it._el === top || it._el.contains(top) || top.contains(it._el))) { hidden = true; break; }
      }
      // 카드 위에 온전히 얹힌 글자(f ≥ 0.9)는 정상, 가장자리에 걸치면(0.2~0.9) 문제
      if (hidden || (f >= 0.2 && f < 0.9)) {
        const t = (bx.el.innerText || bx.el.getAttribute('src') || bx.el.id || bx.el.tagName).replace(/\s+/g, ' ').trim().slice(0, 24);
        it.cover.push((hidden ? '가려짐: ' : '걸침: ') + t);
      }
    }
    for (const bx of boxes) {
      if (!bx.el.contains(it._el)) continue;
      if (it.x < bx.x - 3 || it.x + it.w > bx.x + bx.w + 3 || it.y < bx.y - 3 || it.y + it.h > bx.y + bx.h + 3) {
        it.cover.push('넘침: 카드 밖으로 ' + (bx.el.id || bx.el.className || bx.el.tagName));
      }
    }
    it.bottomBox = Math.max(...boxes.filter(bx => bx.el.contains(it._el)).map(bx => bx.y + bx.h), it.y + it.h);
    delete it._el;
  }
  out.push(...boxes.filter(bx => !bx.el.innerText || !bx.el.innerText.trim()).map(bx => ({text: '[' + (bx.el.getAttribute('src') || bx.el.tagName) .split('/').pop().slice(0, 20) + ']',
           x: bx.x, y: bx.y, w: bx.w, h: bx.h, label: false, box: true, cover: [], bottomBox: bx.y + bx.h})));
  return out;
}
"""


def sub_top(ass: Path) -> float:
    """한 줄 자막 상자 위쪽 y (1080 기준)."""
    m = re.search(r"^Style: Sub,[^,]*,(\d+),(?:[^,]*,){12}\d+,([\d.]+),[\d.]+,\d+,\d+,\d+,(\d+)", ass.read_text(encoding="utf-8"), re.M) if ass.exists() else None
    size, outline, mv = (int(m.group(1)), float(m.group(2)), int(m.group(3))) if m else (52, 14, 48)
    return 1080 - mv - outline - size * 1.25


def scan(project: str, only: set[int] | None = None) -> dict:
    from playwright.sync_api import sync_playwright
    pd = ROOT / "projects" / project
    tl = json.loads((pd / "05_edit" / "hybrid_timeline.json").read_text(encoding="utf-8"))
    top = sub_top(pd / "05_edit" / "subs.ass")
    hb = pd / "04_assets" / "hb"
    res = {"subtitle_top": round(top), "scenes": {}}
    with sync_playwright() as p:
        import os
        exe = "/opt/pw-browsers/chromium"
        try:
            br = p.chromium.launch()
        except Exception:  # noqa: BLE001 — 설치된 브라우저 판이 다르면 미리 깔린 Chromium 으로
            br = p.chromium.launch(executable_path=exe if os.path.isfile(exe) else None)
        pg = br.new_page(viewport={"width": 1920, "height": 1080})
        pg.add_init_script("window.__timelines = window.__timelines || {};")   # 렌더할 때는 HyperFrames 가 만들어 줌
        for x in tl:
            sid = x["scene"]
            if only and sid not in only:
                continue
            f = hb / f"scene_{sid:03d}" / "index.html"
            if not f.exists():
                continue
            pg.goto(f.resolve().as_uri())
            pg.wait_for_timeout(400)
            probs = []
            times = [b0 + bd - 0.05 for b0, bd in x.get("beats", [])] or [x["dur"] - 0.1]
            for t in times:
                items = [i for i in pg.evaluate(JS, t) if not i["label"]]
                for i in items:   # ② 자막 자리 (글자를 감싼 카드의 아래쪽까지)
                    if i.get("bottomBox", i["y"] + i["h"]) > top + 4:
                        probs.append({"t": round(t, 1), "kind": "자막과 겹침", "text": i["text"], "bottom": round(i.get("bottomBox", i["y"] + i["h"]))})
                    for c in i.get("cover", []):   # ③ 글자 위·아래로 다른 카드·그림이 겹침
                        probs.append({"t": round(t, 1), "kind": "글자와 카드 겹침", "text": f'{i["text"]} ↔ {c}'})
                items = [i for i in items if not i.get("box")]
                for a in range(len(items)):   # ① 글자끼리
                    for b in range(a + 1, len(items)):
                        A, B = items[a], items[b]
                        ix = max(0, min(A["x"] + A["w"], B["x"] + B["w"]) - max(A["x"], B["x"]))
                        iy = max(0, min(A["y"] + A["h"], B["y"] + B["h"]) - max(A["y"], B["y"]))
                        small = min(A["w"] * A["h"], B["w"] * B["h"])
                        if small and (ix * iy / small >= 0.12 or ix * iy >= 300):
                            probs.append({"t": round(t, 1), "kind": "글자끼리 겹침", "text": f'{A["text"]} ↔ {B["text"]}'})
            uniq = []
            for q in probs:
                k = (q["kind"], q["text"])
                if k not in {(u["kind"], u["text"]) for u in uniq}:
                    uniq.append(q)
            if uniq:
                res["scenes"][str(sid)] = {"type": x["type"], "issues": uniq}
        br.close()
    return res


def run(project: str, only: set[int] | None = None) -> dict:
    """hybrid 렌더 끝에서 부름 — 결과를 05_edit/overlap_qa.json 에 쓰고 요약을 출력 (실패해도 렌더는 그대로)."""
    r = scan(project, only)
    out = ROOT / "projects" / project / "05_edit" / "overlap_qa.json"
    out.write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
    n = sum(len(v["issues"]) for v in r["scenes"].values())
    print(f"[overlap] 자막 위쪽 y≈{r['subtitle_top']} · 겹침 {n}건 · 장면 {len(r['scenes'])}개 → {out}")
    for sid, v in r["scenes"].items():
        for q in v["issues"]:
            print(f"  #{sid} {v['type']} {q['t']}s {q['kind']}: {q['text']}")
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--scenes", default="")
    ap.add_argument("--json", default="05_edit/overlap_qa.json")
    a = ap.parse_args()
    only = {int(s) for s in a.scenes.split(",") if s.strip()} or None
    r = scan(a.project, only)
    out = ROOT / "projects" / a.project / a.json
    out.write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
    n = sum(len(v["issues"]) for v in r["scenes"].values())
    print(f"[overlap] 자막 위쪽 y≈{r['subtitle_top']} · 겹침 {n}건 · 장면 {len(r['scenes'])}개 → {out}")
    for sid, v in r["scenes"].items():
        for q in v["issues"]:
            print(f"  #{sid} {v['type']} {q['t']}s {q['kind']}: {q['text']}")
    sys.exit(1 if n else 0)


if __name__ == "__main__":
    main()
